from __future__ import annotations

from contextlib import nullcontext
from functools import partial
from pathlib import Path
import random

import pandas as pd
from psychopy import core

from psyflow import (
    BlockUnit,
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    reset_trial_counter,
    runtime_context,
)

from src import run_trial


MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def _parse_args(task_root: Path) -> TaskRunOptions:
    return parse_task_run_options(
        task_root=task_root,
        description="Run Sternberg Working Memory task in human/qa/sim mode.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )


def run(options: TaskRunOptions):
    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path))
    mode = options.mode

    output_dir: Path | None = None
    runtime_scope = nullcontext()
    runtime_ctx = None
    participant_id = "sim001"
    if mode in ("qa", "sim"):
        runtime_ctx = context_from_config(task_dir=task_root, config=cfg, mode=mode)
        output_dir = runtime_ctx.output_dir
        runtime_scope = runtime_context(runtime_ctx)
        if runtime_ctx.session is not None:
            participant_id = str(runtime_ctx.session.participant_id or "sim001")

    with runtime_scope:
        _run_impl(
            mode=mode,
            cfg=cfg,
            output_dir=output_dir,
            participant_id=participant_id,
        )


def _run_impl(*, mode: str, cfg: dict, output_dir: Path | None, participant_id: str):
    if mode == "qa":
        subject_data = {"subject_id": "qa"}
    elif mode == "sim":
        subject_data = {"subject_id": participant_id}
    else:
        subform = SubInfo(cfg["subform_config"])
        subject_data = subform.collect()

    settings = TaskSettings.from_dict(cfg["task_config"])
    if mode in ("qa", "sim") and output_dir is not None:
        settings.save_path = str(output_dir)
    settings.add_subinfo(subject_data)

    if mode == "qa" and output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        settings.res_file = str(output_dir / "qa_trace.csv")
        settings.log_file = str(output_dir / "qa_psychopy.log")
        settings.json_file = str(output_dir / "qa_settings.json")

    settings.triggers = cfg["trigger_config"]
    trigger_runtime = initialize_triggers(mock=True) if mode in ("qa", "sim") else initialize_triggers(cfg)

    win, kb = initialize_exp(settings)
    stim_bank = StimBank(win, cfg["stim_config"]).preload_all()
    settings.save_to_json()

    trigger_runtime.send(settings.triggers.get("exp_onset"))

    StimUnit("instruction_text", win, kb, runtime=trigger_runtime).add_stim(
        stim_bank.get_and_format(
            "instruction_text",
            old_key=str(getattr(settings, "old_key", "f")).upper(),
            new_key=str(getattr(settings, "new_key", "j")).upper(),
        )
    ).wait_and_continue()

    all_data = []
    task_state = {"total_score": 0}
    reset_trial_counter()
    total_blocks = int(getattr(settings, "total_blocks", 1))
    condition_labels = [str(label) for label in list(getattr(settings, "conditions", ["set3", "set5", "set7"]))]
    condition_weights = settings.resolve_condition_weights()

    for block_i in range(total_blocks):
        block_seed = getattr(settings, "overall_seed", 2025)
        if isinstance(getattr(settings, "block_seed", None), list) and block_i < len(settings.block_seed):
            block_seed = settings.block_seed[block_i]
        if block_seed is None:
            block_seed = int(getattr(settings, "overall_seed", 2025)) + block_i * 1009
        block_rng = random.Random(int(block_seed))

        block = (
            BlockUnit(
                block_id=f"block_{block_i}",
                block_idx=block_i,
                settings=settings,
                window=win,
                keyboard=kb,
            )
            .generate_conditions(condition_labels=condition_labels, weights=condition_weights, order="random")
            .on_start(lambda b: trigger_runtime.send(settings.triggers.get("block_onset")))
            .on_end(lambda b: trigger_runtime.send(settings.triggers.get("block_end")))
                .run_trial(
                    partial(
                        run_trial,
                        stim_bank=stim_bank,
                        trigger_runtime=trigger_runtime,
                        rng=block_rng,
                        task_state=task_state,
                        block_id=f"block_{block_i}",
                        block_idx=block_i,
                    )
            )
            .to_dict(all_data)
        )

        block_trials = block.get_all_data()
        answered = [t for t in block_trials if not bool(t.get("probe_timed_out", False))]
        correct = [t for t in answered if bool(t.get("is_correct", False))]
        block_acc = (len(correct) / len(answered)) if answered else 0.0
        block_score = int(block_trials[-1].get("score_after", task_state["total_score"])) if block_trials else int(task_state["total_score"])

        if block_i < (total_blocks - 1):
            StimUnit("block", win, kb, runtime=trigger_runtime).add_stim(
                stim_bank.get_and_format(
                    "block_break",
                    block_num=block_i + 1,
                    total_blocks=total_blocks,
                    block_acc=block_acc,
                    score_after=block_score,
                )
            ).wait_and_continue()

    answered = [t for t in all_data if not bool(t.get("probe_timed_out", False))]
    correct = [t for t in answered if bool(t.get("is_correct", False))]
    final_acc = (len(correct) / len(answered)) if answered else 0.0
    final_score = int(all_data[-1].get("score_after", task_state["total_score"])) if all_data else int(task_state["total_score"])
    StimUnit("goodbye", win, kb, runtime=trigger_runtime).add_stim(
        stim_bank.get_and_format(
            "good_bye",
            final_acc=final_acc,
            total_score=final_score,
            total_trials=len(all_data),
        )
    ).wait_and_continue(terminate=True)

    trigger_runtime.send(settings.triggers.get("exp_end"))

    df = pd.DataFrame(all_data)
    df.to_csv(settings.res_file, index=False)

    trigger_runtime.close()
    core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = _parse_args(task_root)
    run(options)


if __name__ == "__main__":
    main()
