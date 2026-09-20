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
counted by hand. Build the metric: from `truth()` poses at the end of a run
(and at every event), a flask counts as felled when its body z-axis tilts past
a threshold (propose 30°) or its base leaves the bench plane. Add it to the
scan report and to a headless driver that runs the ten patterns of
`scene_patterns.py` in sequence and prints one table: pattern, flasks, named,
felled, seconds. This table is what the acceptance run reads.

AFK. Record the baseline table for the current code as the answer.
