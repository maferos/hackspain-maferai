# dashboard

Mission-control console for the MaferAI Autonomous Formulation Lab. One screen,
no scrolling at 1920×1080, that shows a judge what the autonomous system is
doing: **PERCEIVE → IDENTIFY → PLAN → MOVE → DOSE → VERIFY**.

React 19 + TypeScript + Vite + Tailwind CSS 4 + Lucide icons. No chart
library; the mass chart is SVG.

## Run

```bash
cd dashboard
npm install
npm run dev        # http://localhost:5173
npm run build      # typecheck + production bundle in dist/
```

The package has its own `.npmrc` pointing at the public npm registry, so it
installs regardless of any private registry configured globally.

## Demo mode (default)

Opens on a deterministic replay of recipe `FRG-031` (Fougère Accord 01, four
ingredients, 10.000 g) in the simulation's own workcell: the minihannover
bench of `simulation/models/minihannover_scene.xml` (6.0 × 1.5 m centred on
the origin, worktop at z = 0.90 m), its five balances, its `general` and
`wrist` cameras, and its seven free containers with their real sample IDs
(SMP-0009 Linalool, PWD-0012 Coumarin, SMP-0021 Eugenol, PWD-0026 Menthol on
the aisle side; SMP-0013, PWD-0008 and SMP-0017 on the far side). The
formulation vessel sits on `balance_2`.

The scene has no robot yet. The demo assumes a Franka Panda on a linear rail
along the aisle edge (`ROBOT` in `src/state/demo/recipe.ts`), which is what
lets one arm serve containers 3 m apart. A fixed base is a rail with a single
position and needs no UI change: the console draws whatever `workcell` and
`robot.basePosition` say.

The header has play/pause, restart and a speed toggle (1×, 2×, 4×). The demo
runs about 2 min 50 s at 1× and includes one autonomous recovery: the Eugenol
flask is displaced while the arm approaches it, the pose is invalidated, the
planner re-detects and reacquires it.

Every panel is driven by the same timeline, so when dosing starts the plan row
highlights, the robot state becomes `DOSING`, the balance target changes, the
mass curve rises through FAST → SLOW → PULSE, the pipeline lights up the dosing
module and the event log records the transitions.

Sample IDs and EAN-13 codes are the real rows of
`computer-vision/barcodes/lookup_table.json`; the wrist-camera view draws the
real bars for the real code.

URL parameters:

| Parameter | Effect |
| --- | --- |
| `?speed=2` | playback speed |
| `?loop=1` | restart a few seconds after completion (for an unattended booth) |
| `?mode=live` | start in live mode |
| `?url=ws://host:8765/state` | live state endpoint (WebSocket, or an `http(s)://` SSE URL) |
| `?sim=…`, `?simRobot=…`, `?simWrist=…` | image source per camera, see below |
| `?cam=overview|robot|wrist` | pin a camera instead of following the robot |

The same defaults can be set in a `.env.local` file with `VITE_LAB_URL`,
`VITE_SIM_SOURCE`, `VITE_SIM_ROBOT_SOURCE` and `VITE_SIM_WRIST_SOURCE`.

## Live mode

`LiveSource` connects to a WebSocket (`ws://`, `wss://`) or an EventSource
(`http://`, `https://`) and applies JSON messages to the state. Components do
not change between modes. Message shapes (`src/state/sources/protocol.ts`):

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
patches at whatever rate the loop runs. The connection reconnects every 3 s.
Do not put `balance.history` in patches: send `mass_sample` messages and the
chart grows on its own.

`labbridge.StateServer` keeps the merged state, the recent events and the mass
samples, and `FrameServer` keeps the last frame per camera, so a console that
connects (or reloads) in the middle of a run is complete at once.

The full state shape is `src/state/types.ts`. Perception fields must hold what
the cameras and the barcode reader produce; simulator poses go under
`evaluator`, which the viewport labels as ground truth. Static furniture
(bench extent, balances, rail, cameras) goes under `workcell` in the snapshot.

## Connecting the simulation

`bridge/` is a small Python package, `labbridge`, that the simulation loop
imports. It runs two WebSocket servers in background threads and is safe to
call from the synchronous MuJoCo loop:

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

Then open the console with:

```
http://localhost:5173/?mode=live&url=ws://localhost:8765/state
    &sim=ws://localhost:8766/frames/general
    &simRobot=ws://localhost:8766/frames/general
    &simWrist=ws://localhost:8766/frames/wrist
```

Any camera slot without a stream falls back to the schematic. Add `&cam=wrist`
to pin a camera instead of following the robot.

`labbridge.mock_run` is a working reference: it loads the real scene, streams
its cameras, moves the free containers kinematically through a scripted run
and publishes everything above. From `dashboard/bridge`, with the repo venv:

```bash
python -m labbridge.mock_run --fps 1 --loop
```

Rendering on a laptop without a GPU takes about a second per frame; on a GPU
machine the same call streams at camera rate. Dependencies:
`bridge/requirements.txt` (`websockets`, `numpy`, `mujoco`, `opencv-python`).

## Simulator viewport

`SimulationViewport` shows one camera at a time (Overview, Robot, Wrist cam)
and follows the camera the robot is using unless one is pinned. Each camera
takes its image from a `ViewportSource`:

| `sim=` value | Source |
| --- | --- |
| `schematic` (default) | top-down workcell drawn from state |
| `video:/clip.mp4`, `*.mp4`, `*.webm` | HTML video element |
| `mjpeg:http://host/stream` | multipart JPEG stream |
| `ws://host:9000/frames` | JPEG/PNG frames over a WebSocket, binary or `{"type":"frame","data":"<base64>"}` |

The overlays (camera, rate, executing action, target box) are drawn over
whichever source is active.

## Structure

```
src/
  App.tsx                     grid layout
  config.ts                   URL / env configuration
  state/
    types.ts                  LabState and friends
    LabStateProvider.tsx      useLabState()
    emptyState.ts
    sources/                  LabStateSource, DemoSource, LiveSource, protocol
    demo/                     recipe + bench, dosing profile, timeline
  components/
    HeaderStatus.tsx
    viewport/                 SimulationViewport, SchematicView, WristView, StreamView, overlays
    execution/                ExecutionPanel, RecipeSummary, IngredientRow, ExecutionTimeline
    balance/                  BalancePanel, MassChart
    RobotTelemetry.tsx
    PerceptionPanel.tsx
    pipeline/                 AutonomyPipeline, PipelineNode
    EventLog.tsx
    ui/                       Panel, KeyValue, StatusDot
  lib/                        format, math, ean13, useSize
```

The layout is a CSS grid sized in `rem`, and the root font size scales with
the viewport width, so 1920×1080 and 1440×900 show the same composition.
Below 1280 px the panels stack and the page scrolls.
