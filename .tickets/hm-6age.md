---
id: hm-6age
status: open
deps: [hm-lxrb]
links: []
created: 2026-09-20T02:01:16Z
type: task
priority: 2
assignee: Eloi Torrents
parent: hm-o6wf
tags: [wayfinder:grilling]
---
# Moving a flask out of the way: where it goes and when

## Question

When a look or a grasp is blocked by a neighbour, the arm moves that
neighbour aside and retries (charting decision). Decide: which neighbour
(the one named in "blocked by"), where it is placed (a parking strip on the
bench that is known free — candidates: the rail-side edge y ≈ 0.0 or the
bench end outside the pattern strip), the limit (one move per target, no
recursion), and what the tracks and `view_bench_map.json` record so the moved
flask stays named. Whether it returns afterwards is fog until this is decided.

Done when the crowded case on p01 that skips today is scanned and picked
after one move-aside, zero felled. HITL grilling, then TDD.
