# Sternberg Working Memory Task

| Field | Value |
|---|---|
| Name | Sternberg Working Memory Task |
| Version | v0.1.0-dev |
| URL / Repository | https://github.com/TaskBeacon/T000035-sternberg-working-memory |
| Short Description | Item-recognition working-memory task with set-size manipulation (Sternberg-style). |
| Created By | TaskBeacon |
| Date Updated | 2026-03-04 |
| PsyFlow Version | v0.1.x |
| PsychoPy Version | 2024.x |
| Modality | behavior |
| Maturity | smoke_tested |
| Language | English |
| Voice Name | en-US-AriaNeural |

## 1. Task Overview

This task implements a Sternberg-style working-memory paradigm for item-recognition under memory-load manipulation. Each trial presents a short memory set of letters, enforces a brief maintenance interval, and then probes whether a single letter belonged to the just-presented set. Participants respond `OLD` or `NEW`, allowing the task to capture both recognition accuracy and probe reaction time under different load levels.

The current implementation keeps the experimental design explicit and auditable. Block-level load scheduling is handled by the native `BlockUnit.generate_conditions(...)` path, while trial-level stimulus details are expanded from the current load label into a concrete trial specification (`memory_items`, `probe_item`, `probe_type`, `correct_key`) immediately before execution. This preserves clear separation between experimental conditions, task logic, and runtime state.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| Instruction | Participant reads task instructions and key mapping. |
| Block execution | Trials are generated from set-size conditions and run with trigger-locked phases. |
| Block break | Performance summary is shown between blocks. |
| End screen | Final summary (accuracy/score/trials) and exit key. |

### Trial-Level Flow

| Step | Description |
|---|---|
| `memory_set` | Show the letter set for the current trial (size 3/5/7). |
| `retention` | Central fixation period with no response. |
| `probe_response` | Show probe item; participant responds `OLD` (`F`) or `NEW` (`J`). |
| `feedback` | Correct/incorrect/timeout feedback and score update. |
| `inter_trial_interval` | Fixation-only ITI before next trial. |

### Controller Logic

| Component | Description |
|---|---|
| Controller usage | No task-local controller is used because this task has no adaptive response-time or duration-control requirement. |
| `sample_trial_spec(...)` | Samples memory-set letters and old/new probe item from the configured pool using pure helper logic. |
| Trial-local scoring | Applies score delta directly from feedback config and stores cumulative score in minimal runtime state. |
| `next_trial_id()` | Provides auditable sequential trial IDs without controller state. |

### Other Logic

| Component | Description |
|---|---|
| Condition scheduler | Uses `BlockUnit.generate_conditions` with optional `task.condition_weights`. |
| Set-size parsing | Runtime parses load from labels such as `set3`, `set5`, `set7`. |

## 3. Configuration Summary

All settings are defined in `config/config.yaml`.

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | Participant identifier (3 digits). |
| `age` | Participant age. |
| `gender` | Participant gender choice. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `fullscreen` | `false` |
| `bg_color` | `black` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `memory_set_text` | `text` | Displays letters to memorize. |
| `probe_text` | `text` | Displays current probe item. |
| `probe_hint` | `text` | OLD/NEW key mapping reminder during probe phase. |
| `feedback_*` | `text` | Outcome and score feedback text. |
| `fixation` | `text` | Central `+` for retention and ITI. |

### d. Timing

| Phase | Duration |
|---|---|
| `memory_set_duration` | `1.5 s` |
| `retention_duration` | `2.5 s` |
| `probe_duration` | `3.0 s` |
| `feedback_duration` | `0.8 s` |
| `iti_duration` | `1.0 s` |

### e. Triggers

| Event | Code |
|---|---|
| `exp_onset` / `exp_end` | `1` / `2` |
| `block_onset` / `block_end` | `10` / `11` |
| `memory_set_3_onset` / `memory_set_5_onset` / `memory_set_7_onset` | `23` / `25` / `27` |
| `probe_onset` | `40` |
| `probe_old_response` / `probe_new_response` / `probe_timeout` | `41` / `42` / `43` |
| `feedback_correct_onset` / `feedback_incorrect_onset` / `feedback_timeout_onset` | `50` / `51` / `52` |
| `iti_onset` | `60` |

### f. Randomization and Feedback Parameters

| Parameter | Value |
|---|---|
| `task.overall_seed` | `35035` |
| `task.probe_old_prob` | `0.5` |
| `task.feedback_score_correct` | `1` |
| `task.feedback_score_incorrect` | `0` |
| `task.feedback_score_timeout` | `0` |

## 4. Methods (for academic publication)

A Sternberg-style short-term memory scanning design was implemented with load manipulation through memory-set size (`3`, `5`, `7`). Each trial comprised a memory-set encoding stage, a retention delay, and a probe-recognition response stage requiring binary old/new discrimination.

Performance metrics include probe response time and accuracy, with optional score accumulation for participant feedback. Event triggers are emitted per phase to support synchronized acquisition workflows.

## 5. Implementation Notes

- The same task flow is used across `human`, `qa`, and `sim` modes; mode-specific behavior is limited to subject acquisition, trigger mocking, and runtime context wiring.
- Trial IDs come from framework-native `next_trial_id()`, not a task-local controller object.
- Deterministic trial sampling uses `task.overall_seed` together with per-block seeds from `TaskSettings`, so QA and sim can reproduce the same load-balanced block schedule and trial material sequence.
- The task deliberately does not define a `controller` because there is no adaptive response-window, staircase, or dynamic timing requirement in this paradigm.

## 6. Outputs and Review Status

- Human runs write participant-specific CSV/JSON/log outputs under `outputs/human`.
- QA mode writes smoke-test artifacts under `outputs/qa`, including trace/event reports used by `psyflow-qa`.
- Simulation profiles cover both scripted and sampler responders so the probe response phase, expected response key, and score updates can be checked without manual interaction.
- The task has been promoted to `smoke_tested` after passing local `psyflow-validate`, `psyflow-qa`, and both simulation profiles.
