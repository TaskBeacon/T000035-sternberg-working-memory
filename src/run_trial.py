from __future__ import annotations

from functools import partial
from typing import Any
from psyflow import StimUnit, next_trial_id, resolve_deadline, set_trial_context
from .utils import TrialSpec


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    task_state: dict[str, int],
    block_id=None,
    block_idx=None,
):
    """Run one Sternberg memory-scanning trial."""
    if not isinstance(condition, dict):
        raise ValueError("Sternberg run_trial requires a scheduled trial-spec condition dict.")
    condition_label = str(condition.get("condition", "")).strip().lower()
    trial_spec = TrialSpec(
        set_size=int(condition["set_size"]),
        memory_items=[str(item) for item in condition["memory_items"]],
        probe_item=str(condition["probe_item"]),
        probe_type=str(condition["probe_type"]),
    )
    trial_id = int(next_trial_id())

    old_key = str(getattr(settings, "old_key", "f")).strip().lower()
    new_key = str(getattr(settings, "new_key", "j")).strip().lower()
    response_keys = [old_key, new_key]
    correct_key = old_key if trial_spec.probe_type == "old" else new_key
    expected_class = "old" if trial_spec.probe_type == "old" else "new"

    memory_set_duration = float(getattr(settings, "memory_set_duration", 1.5))
    retention_duration = float(getattr(settings, "retention_duration", 2.5))
    probe_duration = float(getattr(settings, "probe_duration", 3.0))
    feedback_duration = float(getattr(settings, "feedback_duration", 0.8))
    iti_duration = float(getattr(settings, "iti_duration", 1.0))

    memory_set_display = "  ".join(trial_spec.memory_items)
    memory_set_trigger = settings.triggers.get(f"memory_set_{trial_spec.set_size}_onset") or settings.triggers.get(
        "memory_set_onset"
    )

    block_id_str = str(block_id) if block_id is not None else "block_0"
    block_index = int(block_idx) if block_idx is not None else 0

    trial_data = {
        "condition": condition_label,
        "trial_id": trial_id,
        "block_id": block_id_str,
        "block_idx": block_index,
        "set_size": int(trial_spec.set_size),
        "memory_items": "|".join(trial_spec.memory_items),
        "probe_item": str(trial_spec.probe_item),
        "probe_type": str(trial_spec.probe_type),
        "old_key": old_key,
        "new_key": new_key,
        "correct_key": correct_key,
        "expected_probe_class": expected_class,
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    memory_set = make_unit(unit_label="memory_set").add_stim(
        stim_bank.get_and_format("memory_set_text", memory_set_display=memory_set_display)
    )
    set_trial_context(
        memory_set,
        trial_id=trial_id,
        phase="memory_set",
        deadline_s=resolve_deadline(memory_set_duration),
        valid_keys=[],
        block_id=block_id_str,
        condition_id=condition_label,
        task_factors={
            "stage": "memory_set",
            "set_size": int(trial_spec.set_size),
            "memory_items": list(trial_spec.memory_items),
            "block_idx": block_index,
        },
        stim_id="memory_set_text",
    )
    memory_set.show(duration=memory_set_duration, onset_trigger=memory_set_trigger).to_dict(trial_data)

    retention = make_unit(unit_label="retention").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        retention,
        trial_id=trial_id,
        phase="retention",
        deadline_s=resolve_deadline(retention_duration),
        valid_keys=[],
        block_id=block_id_str,
        condition_id=condition_label,
        task_factors={
            "stage": "retention",
            "set_size": int(trial_spec.set_size),
            "probe_type": str(trial_spec.probe_type),
            "block_idx": block_index,
        },
        stim_id="fixation",
    )
    retention.show(duration=retention_duration, onset_trigger=settings.triggers.get("retention_onset")).to_dict(trial_data)

    probe = make_unit(unit_label="probe_response")
    probe.add_stim(stim_bank.get_and_format("probe_text", probe_item=str(trial_spec.probe_item)))
    probe.add_stim(
        stim_bank.get_and_format(
            "probe_hint",
            old_key=old_key.upper(),
            new_key=new_key.upper(),
        )
    )
    set_trial_context(
        probe,
        trial_id=trial_id,
        phase="probe_response",
        deadline_s=resolve_deadline(probe_duration),
        valid_keys=response_keys,
        block_id=block_id_str,
        condition_id=condition_label,
        task_factors={
            "stage": "probe_response",
            "set_size": int(trial_spec.set_size),
            "probe_type": str(trial_spec.probe_type),
            "probe_item": str(trial_spec.probe_item),
            "expected_response_key": correct_key,
            "expected_probe_class": expected_class,
            "old_key": old_key,
            "new_key": new_key,
            "block_idx": block_index,
        },
        stim_id="probe_text+probe_hint",
    )
    probe.capture_response(
        keys=response_keys,
        duration=probe_duration,
        correct_keys=[correct_key],
        onset_trigger=settings.triggers.get("probe_onset"),
        response_trigger={old_key: settings.triggers.get("probe_old_response"), new_key: settings.triggers.get("probe_new_response")},
        timeout_trigger=settings.triggers.get("probe_timeout"),
    )
    probe.to_dict(trial_data)

    response_key = str(probe.get_state("response", "")).strip().lower()
    timed_out = response_key not in response_keys
    is_correct: bool | None = None if timed_out else (response_key == correct_key)
    score_before = int(task_state.get("total_score", 0))
    if timed_out:
        score_delta = int(getattr(settings, "feedback_score_timeout", 0))
    elif bool(is_correct):
        score_delta = int(getattr(settings, "feedback_score_correct", 1))
    else:
        score_delta = int(getattr(settings, "feedback_score_incorrect", 0))
    score_after = score_before + score_delta
    task_state["total_score"] = int(score_after)
    score_update = {
        "score_before": int(score_before),
        "score_delta": int(score_delta),
        "score_after": int(score_after),
    }

    if timed_out:
        feedback_id = "feedback_timeout"
        feedback_trigger = settings.triggers.get("feedback_timeout_onset")
    elif bool(is_correct):
        feedback_id = "feedback_correct"
        feedback_trigger = settings.triggers.get("feedback_correct_onset")
    else:
        feedback_id = "feedback_incorrect"
        feedback_trigger = settings.triggers.get("feedback_incorrect_onset")

    feedback = make_unit(unit_label="feedback").add_stim(
        stim_bank.get_and_format(
            feedback_id,
            score_delta=score_update["score_delta"],
            score_after=score_update["score_after"],
            correct_key=correct_key.upper(),
        )
    )
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="feedback",
        deadline_s=resolve_deadline(feedback_duration),
        valid_keys=[],
        block_id=block_id_str,
        condition_id=condition_label,
        task_factors={
            "stage": "feedback",
            "set_size": int(trial_spec.set_size),
            "probe_type": str(trial_spec.probe_type),
            "response_key": response_key,
            "is_correct": is_correct,
            "timed_out": bool(timed_out),
            "score_after": score_update["score_after"],
            "block_idx": block_index,
        },
        stim_id=feedback_id,
    )
    feedback.show(duration=feedback_duration, onset_trigger=feedback_trigger).to_dict(trial_data)

    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=resolve_deadline(iti_duration),
        valid_keys=[],
        block_id=block_id_str,
        condition_id=condition_label,
        task_factors={"stage": "inter_trial_interval", "block_idx": block_index},
        stim_id="fixation",
    )
    iti.show(duration=iti_duration, onset_trigger=settings.triggers.get("iti_onset")).to_dict(trial_data)

    rt = probe.get_state("rt", None)
    rt_s = float(rt) if isinstance(rt, (int, float)) else None
    trial_data.update(
        {
            "response_key": "" if timed_out else response_key,
            "probe_timed_out": bool(timed_out),
            "probe_rt": rt_s,
            "probe_rt_s": rt_s,
            "is_correct": bool(is_correct) if is_correct is not None else None,
            "score_before": score_update["score_before"],
            "score_after": score_update["score_after"],
            "score_delta": score_update["score_delta"],
        }
    )
    return trial_data
