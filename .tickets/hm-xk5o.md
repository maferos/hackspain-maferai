---
id: hm-xk5o
status: open
deps: []
links: []
created: 2026-09-20T02:01:16Z
type: task
priority: 1
assignee: Eloi Torrents
parent: hm-o6wf
tags: [wayfinder:prototype]
---
# Perceived flasks as obstacles: representation and inflation margin

## Question

`blocked()` (`vision_pick.py` ~917) deliberately ignores free bodies, so the
planner never collision-checks a flask. Decide how the perceived flasks enter
the check:

- Representation: a cylinder per track from `refined_xy` (else `seen_xy`) with
  the vessel's height and radius (from `vessel_class` when named, else the YOLO
  box), inflated by a margin parameter. Candidates: inject mocap/scratch geoms
  into the scratch state that `blocked()` already runs `mj_forward` on, versus
  an analytic test of every `arm_*` geom AABB against the cylinders.
- The margin: one global `FLASK_MARGIN` versus per-track from perception error.
- Where the target flask is exempt (grasp must touch it) and where it is not
  (the look must not).

Prototype both representations on p01 and p05 and report: looks and grasps
still feasible at margins 0, 5, 10, 20 mm, and the check's cost per
`path_clear()` sample. Pick one; the answer names the function signature the
scan and pick tickets will call.

HITL: react to the prototype with Eloi.
