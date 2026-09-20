---
id: hm-lxrb
status: open
deps: [hm-xk5o]
links: []
created: 2026-09-20T02:01:16Z
type: task
priority: 1
assignee: Eloi Torrents
parent: hm-o6wf
tags: [wayfinder:grilling]
---
# Collision-checked approach and retreat for pick

## Question

`plan_grasp()` and `travel()` pass no flask check, and `pick()` always
approaches fully open, then puts the flask back where it was. Decide the safe
pick shape and make grasp **yaw and opening first-class**:

- Two vertically aligned Cartesian endpoints do not give a vertical move:
  `plan()` interpolates in joint space. Generate Cartesian descent and lift
  waypoints with a continuous IK branch, and check each segment.
- Search a small set of grasp yaws (fingers along the widest gap) and
  vessel-sized pre-openings; the 85 mm aperture is not the gripper's outside
  width (finger thickness, knuckles, camera housing, closing sweep).
- The target is exempt only at the finger pads. Neighbours are obstacles
  throughout.
- Loaded transport and release: the held vessel is moving collision geometry;
  check the lift, the travel to the balance or parking spot, and the release.
  After release, drop `refined_xy` and re-seed from the fixed camera (the
  flask settles up to 30 mm away).
- No collision-free grasp: return "blocked by <track>" so the move-aside
  ticket can act.

Done when a fetch order on p01 and p05 (`VIEW_FORMULA_EXECUTOR=fetch`) picks,
carries and releases every named flask with zero felled. HITL grilling, then
TDD.
