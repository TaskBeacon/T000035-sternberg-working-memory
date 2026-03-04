# Task Plot Audit

- generated_at: 2026-03-04T19:47:53
- mode: existing
- task_path: E:\Taskbeacon\T000035-sternberg-working-memory

## 1. Inputs and provenance

- E:\Taskbeacon\T000035-sternberg-working-memory\README.md
- E:\Taskbeacon\T000035-sternberg-working-memory\config\config.yaml
- E:\Taskbeacon\T000035-sternberg-working-memory\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |---|---|
- | `memory_set` | Show the letter set for the current trial (size 3/5/7). |
- | `retention` | Central fixation period with no response. |
- | `probe_response` | Show probe item; participant responds `OLD` (`F`) or `NEW` (`J`). |
- | `feedback` | Correct/incorrect/timeout feedback and score update. |
- | `inter_trial_interval` | Fixation-only ITI before next trial. |

## 3. Evidence extracted from config/source

- set3: phase=memory set, deadline_expr=_deadline_s(memory_set_duration), response_expr=n/a, stim_expr='memory_set_text'
- set3: phase=retention, deadline_expr=_deadline_s(retention_duration), response_expr=n/a, stim_expr='fixation'
- set3: phase=probe response, deadline_expr=_deadline_s(probe_duration), response_expr=probe_duration, stim_expr='probe_text+probe_hint'
- set3: phase=feedback, deadline_expr=_deadline_s(feedback_duration), response_expr=n/a, stim_expr=feedback_id
- set3: phase=inter trial interval, deadline_expr=_deadline_s(iti_duration), response_expr=n/a, stim_expr='fixation'
- set5: phase=memory set, deadline_expr=_deadline_s(memory_set_duration), response_expr=n/a, stim_expr='memory_set_text'
- set5: phase=retention, deadline_expr=_deadline_s(retention_duration), response_expr=n/a, stim_expr='fixation'
- set5: phase=probe response, deadline_expr=_deadline_s(probe_duration), response_expr=probe_duration, stim_expr='probe_text+probe_hint'
- set5: phase=feedback, deadline_expr=_deadline_s(feedback_duration), response_expr=n/a, stim_expr=feedback_id
- set5: phase=inter trial interval, deadline_expr=_deadline_s(iti_duration), response_expr=n/a, stim_expr='fixation'
- set7: phase=memory set, deadline_expr=_deadline_s(memory_set_duration), response_expr=n/a, stim_expr='memory_set_text'
- set7: phase=retention, deadline_expr=_deadline_s(retention_duration), response_expr=n/a, stim_expr='fixation'
- set7: phase=probe response, deadline_expr=_deadline_s(probe_duration), response_expr=probe_duration, stim_expr='probe_text+probe_hint'
- set7: phase=feedback, deadline_expr=_deadline_s(feedback_duration), response_expr=n/a, stim_expr=feedback_id
- set7: phase=inter trial interval, deadline_expr=_deadline_s(iti_duration), response_expr=n/a, stim_expr='fixation'

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 4
- screens_per_timeline: 6
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.031, right=0.033, blank=0.124
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0307, 'right_ratio': 0.0331, 'blank_ratio': 0.124}

## 7. Output files and checksums

- E:\Taskbeacon\T000035-sternberg-working-memory\references\task_plot_spec.yaml: sha256=4748e28e9e020b4030cd954fba1aa4271b90d35b70803170831de23cd7bbd23b
- E:\Taskbeacon\T000035-sternberg-working-memory\references\task_plot_spec.json: sha256=998a3ff559aab9e970a9041a4f24f516234657e4db15943eab92c6e0bd430a5f
- E:\Taskbeacon\T000035-sternberg-working-memory\references\task_plot_source_excerpt.md: sha256=cfac700ad1ee097857df1a6405fadfc2b96350b9d66ff3f6e92e5de6fa50b3c1
- E:\Taskbeacon\T000035-sternberg-working-memory\task_flow.png: sha256=fbdc8251f0196ed507702f6ee3c30c840282dc936dc6049569687d6b1319aa51

## 8. Inferred/uncertain items

- set3:memory set:heuristic numeric parse from 'float(getattr(settings, 'memory_set_duration', 1.5))'
- set3:retention:heuristic numeric parse from 'float(getattr(settings, 'retention_duration', 2.5))'
- set3:probe response:heuristic numeric parse from 'float(getattr(settings, 'probe_duration', 3.0))'
- set3:feedback:heuristic numeric parse from 'float(getattr(settings, 'feedback_duration', 0.8))'
- set3:inter trial interval:heuristic numeric parse from 'float(getattr(settings, 'iti_duration', 1.0))'
- set5:memory set:heuristic numeric parse from 'float(getattr(settings, 'memory_set_duration', 1.5))'
- set5:retention:heuristic numeric parse from 'float(getattr(settings, 'retention_duration', 2.5))'
- set5:probe response:heuristic numeric parse from 'float(getattr(settings, 'probe_duration', 3.0))'
- set5:feedback:heuristic numeric parse from 'float(getattr(settings, 'feedback_duration', 0.8))'
- set5:inter trial interval:heuristic numeric parse from 'float(getattr(settings, 'iti_duration', 1.0))'
- set7:memory set:heuristic numeric parse from 'float(getattr(settings, 'memory_set_duration', 1.5))'
- set7:retention:heuristic numeric parse from 'float(getattr(settings, 'retention_duration', 2.5))'
- set7:probe response:heuristic numeric parse from 'float(getattr(settings, 'probe_duration', 3.0))'
- set7:feedback:heuristic numeric parse from 'float(getattr(settings, 'feedback_duration', 0.8))'
- set7:inter trial interval:heuristic numeric parse from 'float(getattr(settings, 'iti_duration', 1.0))'
- collapsed equivalent condition logic into representative timeline: set3, set5, set7
- unparsed if-tests defaulted to condition-agnostic applicability: bool(is_correct); timed_out
