# labbridge

Publishes the `LabState` of the Autonomous Formulation Lab over WebSocket. The
robot viewer (`view/`) reads it for its task, robot and balance panels.

## Protocol

`StateServer` sends JSON messages on `ws://host:8765/state`:

```jsonc
{ "type": "snapshot", "state": { /* full LabState */ } }
{ "type": "state_update", "patch": { "robot": { "fsmState": "DOSING" }, "balance": { "netMass": 1.842 } } }
{ "type": "state_update", "robot_state": "DOSING", "step": "dose-ing-limonene", "balance_g": 1.842, "target_g": 2.5, "elapsed_s": 134.2 }
{ "type": "event", "time": 134.2, "message": "controller switched FAST → SLOW", "level": "info" }
{ "type": "mass_sample", "time": 134.2, "mass": 1.842 }
```

`patch` is a deep partial of `LabState` (arrays replace, objects merge). The
flat `state_update` form exists for a producer that only has a few numbers.
Start with one `snapshot` so the recipe and the plan are known, then send
patches at whatever rate the loop runs. Do not put `balance.history` in
patches: send `mass_sample` messages instead.

`StateServer` keeps the merged state, the recent events and the mass samples,
and `FrameServer` keeps the last frame per camera, so a client that connects
(or reloads) in the middle of a run is complete at once.

The state shape is built by `labbridge/state.py`. Perception fields must hold
what the cameras and the barcode reader produce; simulator poses go under
`evaluator`. Static furniture (bench extent, balances, rail, cameras) goes
under `workcell` in the snapshot.

## Connecting the simulation

The simulation loop imports `labbridge`. It runs two WebSocket servers in
background threads and is safe to call from the synchronous MuJoCo loop:

```python
import sys; sys.path.insert(0, "dashboard/bridge")     # or: pip install -e dashboard/bridge
from labbridge import StateServer, FrameServer, state as S
from labbridge.mujoco_adapter import CameraStreamer, ground_truth, vessels, workcell

state = StateServer(port=8765); state.start()
frames = FrameServer(port=8766); frames.start()
streamer = CameraStreamer(model)                         # mujoco.Renderer + JPEG

# once, when the run starts
snapshot = S.empty_state("RUN-042", workcell(model, data, active_balance="balance_2"))
snapshot["recipe"] = {...}; snapshot["execution"]["steps"] = [S.step(...), ...]
state.snapshot(snapshot)

# every tick (10 Hz is plenty)
state.patch({
    "robot": S.robot_state("DOSING", base_position, ee_position, gripper="attached", ...),
    "balance": {"netMass": scale.read(), "mode": controller.mode, "flowRate": controller.flow_estimate()},
    "perception": S.perception_state("wrist", vessels=detections, barcode=code, ...),
    "execution": {"currentStepId": planner.step_id, "steps": planner.steps()},
    "evaluator": {"groundTruth": ground_truth(data, vessels(model))},
})
state.mass_sample(t, scale.read())
state.event(t, "controller switched FAST -> SLOW")

# a few times per second
frames.push("general", streamer.jpeg(data, "general"))
frames.push("wrist", streamer.jpeg(data, "wrist"))
```

`labbridge.mock_run` is a working reference: it loads the real scene, moves
the free containers kinematically through a scripted run and publishes
everything above. From `dashboard/bridge`, with the repo venv:

```bash
python -m labbridge.mock_run --fps 0 --loop   # state only, no rendering
python -m labbridge.mock_run --fps 1 --loop   # also streams camera frames
python -m labbridge.record_run                # rewrite the viewer's recorded run
```

Rendering on a laptop without a GPU takes about a second per frame; on a GPU
machine the same call streams at camera rate. Dependencies:
`requirements.txt` (`websockets`, `numpy`, `mujoco`, `opencv-python`).
