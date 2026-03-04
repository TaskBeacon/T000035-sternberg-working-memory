# Task Logic Audit: Sternberg Working Memory

## 1. Paradigm Intent

- Task: `sternberg_working_memory`
- Primary construct: short-term memory maintenance and item-recognition scanning under load manipulation.
- Manipulated factors:
  - memory-set size (`set3`, `set5`, `set7`)
  - probe type (`old`, `new`)
- Dependent measures:
  - probe RT (`probe_rt_s`)
  - probe accuracy (`is_correct`)
  - timeout rate (`probe_timed_out`)
- Key citations:
  - `W2166667242` (capacity/load framing)
  - `W2063007271` (serial attention in working memory)
  - `W2161908852` (working-memory phase structuring with delay/probe events)
  - `W1969647331` (load-sensitive neural coding rationale)
  - `W2121570466` (short-term memory decoding context)

## 2. Block/Trial Workflow

### Block Structure

- Human profile: `2` blocks x `30` trials (`60` total).
- QA/sim profiles: `1` block x `9` trials for gate speed.
- Condition scheduling:
  - uses built-in `BlockUnit.generate_conditions(...)`
  - labels: `set3`, `set5`, `set7`
  - weights from `TaskSettings.resolve_condition_weights()` (`[1,1,1]`)

### Trial State Machine

1. `memory_set`
   - Trigger: `memory_set_{size}_onset` (`23/25/27`; fallback `20`).
   - Stimulus: formatted memory-set letters.
   - Response: none.
   - Timeout: fixed `timing.memory_set_duration`.
2. `retention`
   - Trigger: `retention_onset` (`30`).
   - Stimulus: fixation (`+`).
   - Response: none.
   - Timeout: fixed `timing.retention_duration`.
3. `probe_response`
   - Trigger: `probe_onset` (`40`).
   - Stimuli: probe letter + OLD/NEW key hint.
   - Response keys: `old_key` / `new_key` (`f` / `j`).
   - Response triggers: `probe_old_response` (`41`), `probe_new_response` (`42`).
   - Timeout trigger: `probe_timeout` (`43`).
4. `feedback`
   - Trigger: `feedback_correct_onset` (`50`) / `feedback_incorrect_onset` (`51`) / `feedback_timeout_onset` (`52`).
   - Stimulus: correctness/timeout feedback and running score.
   - Response: none.
   - Timeout: fixed `timing.feedback_duration`.
5. `inter_trial_interval`
   - Trigger: `iti_onset` (`60`).
   - Stimulus: fixation.
   - Response: none.
   - Timeout: fixed `timing.iti_duration`.

Session wrappers:
- `exp_onset` (`1`), `exp_end` (`2`)
- block wrappers: `block_onset` (`10`), `block_end` (`11`)

## 3. Condition Semantics

- `set3`
  - Meaning: low memory load, 3 encoded letters.
  - Probe can be old/new according to `probe_old_prob=0.5`.
- `set5`
  - Meaning: medium memory load, 5 encoded letters.
  - Probe can be old/new.
- `set7`
  - Meaning: high memory load, 7 encoded letters.
  - Probe can be old/new.

Probe semantics:
- `old`: probe sampled from current memory set; correct key = `old_key`.
- `new`: probe sampled from non-member pool; correct key = `new_key`.

## 4. Response and Scoring Rules

- Response mapping:
  - `F` (`old_key`) = probe was in memory set.
  - `J` (`new_key`) = probe was not in memory set.
  - `SPACE` used only for instruction/break/goodbye pages.
- Missing response:
  - probe key absent or invalid within deadline => timeout.
- Correctness:
  - `is_correct = response_key == correct_key` when not timed out.
- Score update:
  - correct: `+1`
  - incorrect: `0`
  - timeout: `0`
- Primary outputs:
  - `probe_rt_s`, `is_correct`, `probe_timed_out`, `set_size`, `probe_type`

## 5. Stimulus Layout Plan

- `instruction_text`, `block_break`, `good_bye`
  - Centered multi-line text
  - `wrapWidth=980`, height `28-30`
- `memory_set`
  - One centered text object (`memory_set_text`)
  - high contrast white-on-black, height `58`
- `retention` and `inter_trial_interval`
  - centered fixation (`+`)
- `probe_response`
  - `probe_text` at `pos=[0, 50]`
  - `probe_hint` at `pos=[0, -120]`
  - explicit vertical separation prevents overlap
- `feedback`
  - one centered text stimulus selected by outcome class

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` / `exp_end` | 1 / 2 | Session boundary |
| `block_onset` / `block_end` | 10 / 11 | Block boundary |
| `memory_set_onset` | 20 | Generic memory-set onset fallback |
| `memory_set_3_onset` / `memory_set_5_onset` / `memory_set_7_onset` | 23 / 25 / 27 | Load-specific memory-set onsets |
| `retention_onset` | 30 | Delay-period onset |
| `probe_onset` | 40 | Probe presentation onset |
| `probe_old_response` / `probe_new_response` / `probe_timeout` | 41 / 42 / 43 | Probe response classes |
| `feedback_correct_onset` / `feedback_incorrect_onset` / `feedback_timeout_onset` | 50 / 51 / 52 | Feedback classes |
| `iti_onset` | 60 | ITI onset |

## 7. Architecture Decisions (Auditability)

- Use built-in `BlockUnit.generate_conditions(...)` for load-label scheduling (`set3/set5/set7`) and keep trial-specific item/probe sampling in controller logic.
- Keep participant-facing labels and key text in `config/*.yaml` stimuli (`instruction_text`, `probe_hint`, feedback screens), avoiding hardcoded runtime wording.
- Use `TaskSettings.resolve_condition_weights()` as the only weight-resolution path.
- Keep probe decision as the single response phase for clear RT/accuracy interpretation.

## 8. Inference Log

- Decision: set sizes fixed to `3/5/7`.
  - Why inferred: selected references are working-memory load papers, not one single canonical Sternberg implementation spec for this package.
  - Rationale: these loads provide low/mid/high demand while preserving discriminability.
- Decision: fixed phase durations (`1.5 / 2.5 / 3.0 / 0.8 / 1.0` seconds).
  - Why inferred: exact durations vary by modality and study.
  - Rationale: durations keep participant burden manageable and preserve clear phase segmentation.
- Decision: score feedback included although core outcomes are RT/accuracy.
  - Why inferred: classical Sternberg analyses do not require points.
  - Rationale: score is a behavioral engagement aid and does not replace primary dependent measures.
