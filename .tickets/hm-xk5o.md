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
planner never collision-checks a flask; the keepout of a019202 only bounds
height over the hull. Decide how the perceived flasks enter the check.

Representation. Geoms live in `MjModel`, not `MjData`, so "inject geoms into
the scratch state" is not an option without a second compiled planning model
or preallocated proxy geoms (and contact masks then decide which pairs are
checked). Start instead with an **analytic test**: every `arm_*` geom's world
AABB (centre `p + R c`, half-extents `|R| h`, ingredients already in
`lowest_over_hull`) against an upright cylinder per track from `refined_xy`
(else `seen_xy`) with the vessel's height and radius, inflated by a margin.
Overlap is a conservative rejection; add a tighter narrow phase only where
false positives kill tight grasps.

Also decide:
- The margin: one global `FLASK_MARGIN` versus per-track from perception error
  (≈8 mm box, <1 mm ring).
- Obstacle lifetime: a `lost` track stays an obstacle until a camera has seen
  the spot clear; undetected vessels need a conservative bootstrap.
- The target is **never** exempt during a look. During a grasp only the
  finger pads may meet the target; the rest of the arm may not.
- Sampling: clearance-dependent subdivision of `path_clear` instead of fixed
  100 mm / 0.08 rad steps.

Prototype on p01 and p05 and report: looks and grasps still feasible at
margins 0, 5, 10, 20 mm; the check's cost per sample; and, on the tightest
perceived clusters, which flasks remain readable / pickable / unlockable by
one neighbour move / skipped, enumerating grasp yaws and pre-openings (see
"Collision-checked approach and retreat for pick"). That last table is the
cheapest early test of whether the whole route can reach zero felled.

HITL: react to the prototype with Eloi. The answer names the function
signature the scan and pick tickets will call.
