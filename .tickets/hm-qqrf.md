---
id: hm-qqrf
status: open
deps: [hm-wpvx, hm-xk5o]
links: []
created: 2026-09-20T02:01:16Z
type: task
priority: 1
assignee: Eloi Torrents
parent: hm-o6wf
tags: [wayfinder:grilling]
---
# Scan looks that keep the whole arm clear of every flask

## Question

Given the findings of "Why the scan's lowest point ends 3 cm below the flask
tops" and the check from "Perceived flasks as obstacles", change `look()`,
`plan_look()`, `hop()`, `over()`, `straight()` and `travel()` so that every
scan pose and every executed segment is rejected when any `arm_*` geom meets
an inflated perceived flask, the target included. `bearings_outward` becomes
a hard filter followed by a preference. Decide what a look does when no
bearing is clear: skip and mark the track "unread, blocked by <track>", to be
retried after a move-aside.

Done when p01 and p05 scan with zero felled and the metric table shows it.
HITL grilling on the skip semantics, then implement with TDD.
