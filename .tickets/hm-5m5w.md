---
id: hm-5m5w
status: open
deps: [hm-bege, hm-qqrf, hm-lxrb, hm-6age]
links: []
created: 2026-09-20T02:01:16Z
type: task
priority: 1
assignee: Eloi Torrents
parent: hm-o6wf
tags: [wayfinder:task]
---
# Acceptance run: four patterns, zero felled, timed

## Question

Run the metric driver over p01–p04 with the scan, pick and move-aside changes
in place, exercising scan, fetch orders and move-asides, not scan alone.
Pass: zero felled on every pattern, with attempted/completed/skipped counts
reported. Also record seconds per pattern against the Replay cap of 240 s;
where a pattern exceeds it, this ticket decides whether to shorten the scan
or raise the cap (charting left time as a final check, not a design input).
The answer is the table plus that decision.

AFK, unless a pattern fails: then it spawns a ticket and stays open.
