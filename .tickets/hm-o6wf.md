---
id: hm-o6wf
status: open
deps: []
links: []
created: 2026-09-20T02:01:16Z
type: epic
priority: 1
assignee: Eloi Torrents
tags: [wayfinder:map]
---
# Keep the arm from felling flasks

## Destination

The bench scan and the pick in `simulation/scripts/vision_pick.py` (MuJoCo) run
on all ten bench patterns (p01–p10) without felling a single flask, counted
automatically, and the ten Replay videos are re-recorded from that code. The
change is made in place; this map carries execution, not only decisions.

## Notes

- Domain: the rail UR10e + Robotiq gripper over the 6 × 2 m bench. Read
  `simulation/vision-pick.md` (sections "Looks come from outside the bench" and
  "The flyover, tried and set aside") and the lessons in `simulation/README.md`
  before any ticket. The flyover of commit 0f771d0 was reverted for the poses
  it flew, not for its clearance; do not rediscover it. Commit a019202
  (2026-09-20, Nacho) landed during charting: `path_clear` now takes a bench
  keepout `(hull, margin, height)` and `plan`, `carry_pose`, `hover_pose`
  pass it. Ticket bodies assume that code.
- MuJoCo traps (from a gpt-6-astra review of this map, 2026-09-20): geoms
  belong to `MjModel`, not `MjData`, so obstacles cannot be injected into the
  scratch state; `drive()` ramps controls, not measured joints, so the executed
  path lags the checked one; `path_clear` samples at 100 mm / 0.08 rad.
- Tickets are worked by Eloi on macOS (`mjpython` for viewers, plain `python`
  headless). Eki owns MuJoCo and reviews.
- Standing decisions from charting (2026-09-20):
  - Acceptance: zero felled flasks on all ten patterns, measured by an automatic
    metric (does not exist yet; hand-counted so far).
  - Perceived flasks (YOLO box, ArUco ring) become real obstacles for the
    planner, not an ordering preference. Ground truth is for scoring only.
  - Strictness is a parameter: an inflation margin around each perceived flask,
    tuned against the felled metric, not a strict/tolerant switch.
  - No safe path: move one blocking flask out of the way and retry; if that
    also fails, skip the flask and report it.
  - Time is not a design criterion. It is measured once at the acceptance run
    against the Replay cap of 240 s per pattern.
  - Real time (`view/backend/live_scan.py`) picks up any change at once; the
    Replays need the four-step GPU pipeline (record_view_scan → export_rail_animation
    → render_rail_isaaclab → copy MP4s + replayPatterns.json).
- Skills per ticket: grilling + domain-modeling for `wayfinder:grilling`;
  prototype for `wayfinder:prototype`; superpowers:tdd where code is written.

## Decisions so far

<!-- one line per closed ticket: [title](.tickets/<id>.md): gist -->

## Not yet specified

- What the viewer shows when a flask is skipped as unreachable or moved aside:
  track state, caption, event on `ws://localhost:8765/state`, and whether the
  scripted run needs it.
- Whether a moved flask returns to its original spot after the order, and what
  the bench map (`view_bench_map.json`) records meanwhile.
- The 85 mm open gripper among flasks 4–60 mm apart: finger orientation along
  the gap, or a smaller opening, before a neighbour counts as an obstacle.
- Dense clusters where no look or grasp is geometrically possible with this
  camera and gripper, and one neighbour move cannot unlock them: what the
  demo does with such a pattern (drop it, or accept skipped flasks there).

## Out of scope

- Uncap and pipette (`iris_pipette_plan.py`, hand-authored keyframes, separate
  scene): the felling happens on the bench, among flasks; the pipette rig works
  one flask at a time.
- IsaacLab-mlx as a simulator: Isaac only renders a baked MuJoCo trajectory.
