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

`plan()`, `plan_grasp()` and `travel()` pass no floor and no flask check, so
a pick can sweep through neighbours. Decide the safe pick shape: carry pose
above the target at the flask-top floor, vertical descent onto the target
(target exempt from the check, neighbours not), grasp, vertical lift back to
the floor, then travel. Decide how the gripper opening is chosen among close
neighbours and what happens when no collision-free grasp exists (return
"blocked by <track>" so the move-aside ticket can act).

Done when a fetch order on p01 and p05 (`VIEW_FORMULA_EXECUTOR=fetch`) picks
every named flask with zero felled. HITL grilling, then TDD.
