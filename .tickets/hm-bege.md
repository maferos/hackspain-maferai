---
id: hm-bege
status: open
deps: []
links: []
created: 2026-09-20T02:01:16Z
type: task
priority: 1
assignee: Eloi Torrents
parent: hm-o6wf
tags: [wayfinder:task]
---
# Count felled flasks automatically across the ten patterns

## Question

The acceptance criterion is zero felled flasks on p01–p10, but the planner only
reads truth for position error; "flasks knocked over" in `vision-pick.md` was
counted by hand. Build the metric from `truth()` poses:

- A flask is felled when its body z-axis tilts past a threshold (propose 30°)
  or it leaves the bench top **while no track holds it** (a commanded lift is
  not a fall; a drop after release is).
- Latch the failure through the whole run, not only at the end: a flask that
  falls and is later set upright still counts.
- Report attempted / completed / skipped work per phase (looks, picks,
  move-asides) alongside felled, so "skip everything" cannot read as success.

Add it to the scan report and to a headless driver that runs the ten patterns
of `scene_patterns.py` in sequence, scan and fetch orders both, and prints one
table: pattern, flasks, named, picked, skipped, felled, seconds.

AFK. Record the baseline table for the current code (after a019202) as the
answer.
