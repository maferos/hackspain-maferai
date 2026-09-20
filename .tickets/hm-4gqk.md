---
id: hm-4gqk
status: open
deps: [hm-5m5w]
links: []
created: 2026-09-20T02:01:16Z
type: task
priority: 2
assignee: Eloi Torrents
parent: hm-o6wf
tags: [wayfinder:task]
---
# Re-record the ten Replays on an NVIDIA GPU

## Question

Regenerate the Replay videos from the accepted code: for each pattern
`record_view_scan.py --pattern pNN`, `export_rail_animation.py`,
`render_rail_isaaclab.py` on a RunPod L4 (see `simulation/runpod-isaac.md`),
then copy `rail_global.mp4` and `rail_robot.mp4` into
`view/frontend/public/renders/seeds/pNN/` and update
`view/frontend/src/replayPatterns.json`. Also refresh the scripted run if the
panels' events changed (`python -m labbridge.record_run`). The answer records
the render job ids, durations and the commit that ships the MP4s.

Task; AFK where the GPU is scriptable, HITL checklist for the RunPod parts.
