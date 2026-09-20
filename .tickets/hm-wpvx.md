---
id: hm-wpvx
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
# Why the scan's lowest point ends 3 cm below the flask tops

## Question

`vision-pick.md` records that the per-bottle sweep reads with the arm's lowest
point 3 cm *below* the flask tops, although `tallest()` (`vision_pick.py` ~1300)
builds a floor of `BENCH_TOP + tallest vessel + HOVER_MARGIN (0.03)` and
`path_clear()` tests `lowest_point()` against it on the look/hover/slide paths.
Find out, in code and with a headless run on p01 (seed 30), where the floor is
not applied or is applied to the wrong thing (camera site vs whole-arm AABB,
final look pose exempt, `LOOKS` heights overriding, vessel height unknown when
the ring is unread, …). Answer with the exact call sites and a per-look table
of `lowest_point()` minus the flask-top height.

AFK. Write findings to `simulation/notes/scan-floor.md` and link it here.
