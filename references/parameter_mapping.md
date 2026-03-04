# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `P001` | `task.conditions` | `['set3','set5','set7']` | `W2166667242` | Capacity and load effects are central; multiple memory-load levels are required to probe scanning/maintenance cost. | inferred | Encoded as set-size labels for built-in condition scheduler. |
| `P002` | `task.condition_weights` | `[1,1,1]` | `W2063007271` | Balanced coverage across working-memory load levels supports stable condition-wise comparisons. | inferred | Explicit config-level weight policy. |
| `P003` | `task.set_sizes` | `[3,5,7]` | `W2166667242` | Mid-range memory-set sizes are commonly used to manipulate load while avoiding floor/ceiling behavior. | inferred | Not all sources use identical values; documented as inferred implementation choice. |
| `P004` | `task.probe_old_prob` | `0.5` | `W2063007271` | Old/new recognition requires both match and non-match probes. | inferred | Balanced old/new probability. |
| `P005` | `task.letter_pool` | `['B','D','F','G','H','K','L','M','P','Q','R','T']` | `W2121570466` | Verbal-symbol working-memory tasks use simple, visually distinct symbols/letters. | inferred | Excludes ambiguous characters to reduce perceptual confounds. |
| `P006` | `task.old_key` / `task.new_key` | `f` / `j` | `W2063007271` | Binary old/new decision requires two response alternatives. | implementation | Key labels are config-driven for localization/portability. |
| `P007` | `timing.memory_set_duration` | `1.5` | `W2161908852` | Encoding stage duration should allow stable item registration before retention. | inferred | Duration tuned for desktop deployment. |
| `P008` | `timing.retention_duration` | `2.5` | `W2161908852` | Delay period isolates maintenance from encoding/probe phases. | inferred | Fixed retention interval. |
| `P009` | `timing.probe_duration` | `3.0` | `W2063007271` | Probe-response stage captures recognition RT and decision accuracy. | inferred | Timeout included for non-response handling. |
| `P010` | `timing.feedback_duration` | `0.8` | `W1969647331` | Short feedback supports engagement without dominating trial timing. | inferred | Behavioral adaptation for participant-facing runs. |
| `P011` | `timing.iti_duration` | `1.0` | `W2161908852` | ITI separates events for cleaner phase-wise analysis. | inferred | Fixed ITI. |
| `P012` | `task.total_blocks` / `task.trial_per_block` | `2` / `30` | `W2063007271` | Repeated sampling per load condition is needed for robust RT/accuracy estimates. | inferred | Human profile totals 60 trials. |
| `P013` | `task.feedback_score_correct` | `1` | `W2063007271` | Correctness can be accumulated as an engagement metric in behavioral variants. | implementation | Scoring is auxiliary; primary outcomes remain RT/accuracy. |
| `P014` | `triggers.map.memory_set_3_onset` / `..._5_...` / `..._7_...` | `23 / 25 / 27` | `W1969647331` | Load-sensitive analyses require explicit event markers by memory-set size. | implementation | Size-indexed onset triggers. |
| `P015` | `triggers.map.probe_onset` | `40` | `W2063007271` | Probe onset anchors the recognition-response event. | implementation | Shared across set sizes. |
| `P016` | `triggers.map.probe_old_response` / `probe_new_response` / `probe_timeout` | `41 / 42 / 43` | `W2063007271` | Response class and timeout events must be disambiguated for analysis. | implementation | Key- and timeout-specific trigger mapping. |
| `P017` | `triggers.map.feedback_correct_onset` / `feedback_incorrect_onset` / `feedback_timeout_onset` | `50 / 51 / 52` | `W2121570466` | Behavioral outcome phase is represented separately from probe event. | implementation | Feedback-valence trigger split. |
| `P018` | `triggers.map.exp_onset` / `exp_end` / `block_onset` / `block_end` / `iti_onset` | `1 / 2 / 10 / 11 / 60` | `W2161908852` | Session and block boundaries are required for auditability and downstream event modeling. | implementation | Contract-aligned global markers. |
