# Task Plot Review

## Evidence Match

- Pass: title and construct match the Sternberg Working Memory Task.
- Pass: rows match configured set3, set5, and set7 memory-load conditions.
- Pass: phase order matches README and `src/run_trial.py`: Memory set -> Retention -> Probe response -> Feedback -> ITI.
- Pass: timing labels match config: 1500 ms memory set, 2500 ms retention, 3000 ms probe, 800 ms feedback, 1000 ms ITI.
- Pass: probe response mapping shows F=OLD and J=NEW.
- Pass: feedback shows correct, incorrect, or timeout with score/total.
- Pass: no adaptive controller or extra decision phase is shown.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
