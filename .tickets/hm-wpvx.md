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
point 3 cm *below* the flask tops. Since then commit a019202 added a bench
keepout: `path_clear(..., bench=(hull, KEEPOUT_MARGIN, height))` refuses a
move whose arm reaches under `height` anywhere over the hull of the seen
flasks (`lowest_over_hull`, `vision_pick.py` ~995), and `plan`, `carry_pose`
and `hover_pose` now pass it. So the question is what is *still* unchecked:

- `lowest_over_hull` tests each geom's AABB against the hull by its **centre**
  (`inside_hull(world[:, :2])`), so a link whose centre is outside the hull
  margin can still overlap a rim flask. Measure local clearance per flask
  (arm geom to inflated cylinder), not one global lowest point.
- `travel()` (~1371) drives to a station with no `path_clear`; the fallback
  climb `drive(here(), carry)` (~1569) and the "putting back / clear of" moves
  in `pick()` are likewise unchecked. List every `drive()` whose segment was
  not validated.
- `path_clear` samples every 100 mm of rail / 0.08 rad of joint; is that fine
  enough for 4–60 mm gaps? And `drive()` ramps *controls*, not measured joint
  positions: measure how far the executed path lags the checked one.

Answer with the call sites, a per-look table of local clearance on p01 (seed
30) and p05, and the observed servo lag. AFK. Write findings to
`simulation/notes/scan-floor.md` and link it here.
