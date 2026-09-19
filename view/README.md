# Robot viewer

Frontend to watch the mini-Hannover MuJoCo scene live: main viewport switchable
between the robot's onboard camera and the fixed scene-overview camera, a
picture-in-picture subwindow showing the other one (click it to swap), and a
right-hand panel with the robot's running task log, updated in real time.

- `backend/` — FastAPI server. The default rail scene runs the initial bench
  scan from `simulation/scripts/vision_pick.py` with the Robotiq gripper.
  The fixed `general` camera proposes bottles with YOLO; the arm moves its
  `arm_eih` camera to read their ArUco rings. Both live views stream through
  `/ws/camera/robot` and `/ws/camera/scene` (legacy MJPEG is also available).
- `frontend/` — React + Vite app. Real time shows the scan's cameras, current
  action and identified count. Boxes turn green and gain a sample ID after a
  ring is read. Replay continues to show the recorded Isaac videos.

The scan reuses the original perception and physics controller, in manual mode:
there is no automatic picking after the initial scan. It keeps watching the
bench, and saves its map to `simulation/out/view_bench_map.json`. `/api/scan`
reports startup, progress, completion and errors. Missing weights or a failed
controller are shown in the viewport; they do not fall back to a scripted sweep.
The scan runs independently of the Boxes toggle and the selected viewport mode.
Its speed depends on local physics, rendering and inference performance.

The Tasks, Robot, Balance and Pipeline panels still consume the shared lab state
in both modes. Their scripted formulation is independent of the scan.

## Run it

The viewer uses camera WebSockets so multiple open tabs do not exhaust the
browser's per-host HTTP connection limit. Cameras reconnect automatically
after a backend restart and show “Connecting camera…” until a frame arrives.
The main view requests 1920×1080 at up to 15 FPS; the small preview requests
640×360 at up to 5 FPS. Swapping cameras updates these subscriptions. A camera
used as a main view in another tab retains full rendering quality. The general
camera always renders at 1080p for YOLO, even when displayed as a preview,
but drops to 5 FPS when no main view subscribes. The robot preview renders
directly at 640×360. JPEG compression runs in a separate worker with at most
one waiting frame per camera; rendering never waits for compression.

Live scanning uses the original detector's full camera image and proposal
threshold (0.10 for the rail weights), including its arm mask and flask-size
filter. YOLO runs in a subprocess; ring reading runs on the perception thread.
Replay retains its existing table crop and detection settings.

The default scene (`VIEW_SCENE=minihannover_rail_scene.xml`) uses a generated
gripper copy of the rail bench. Each frontend page load requests
a random bench layout from the ten shared `minihannover_open/patterns` seeds.
The next choice excludes the current pattern. The backend replaces the rail
scene's loose and dynamic bench samples with that catalogue population in
memory; it never rewrites generated scene files. All connected tabs share the
new layout, and the viewport label shows its seed and sample count. Requests
are deduplicated per page load, including React StrictMode and network retries.
The render thread stops the previous scan and detector worker, installs the new
MuJoCo model and graphics context, and starts a fresh scan. Tracks and identities
from the old layout are discarded. Replay selects the recording for that same seed; switching modes does not
request a new layout. The panel demo retains its original model, samples and `RECIPE`, so
the shared scripted-run recording continues to match the panel state.

```sh
# 1. Backend deps, into the same venv simulation/ already uses:
uv pip install --python simulation/.venv/bin/python \
  -r simulation/requirements.txt -r view/backend/requirements.txt

# 2. Fetch the robot assets once, and copy the trained detector weights:
(cd simulation && bash scripts/fetch_menagerie.sh)
# computer-vision/weights/yolo26n_rail_general.pt (see that folder's README)

# 3. Backend (serves streams + scan status + tasks on :8000):
simulation/.venv/bin/python view/backend/server.py

# 4. Frontend (:5173), in another terminal:
cd view/frontend
npm install
npm run dev
```

Then open http://localhost:5173. Set `VITE_BACKEND_URL` if the backend runs
somewhere other than `http://localhost:8000`.

By default the viewport shows the live MuJoCo cameras. Select **Replay** in
the header, or open http://localhost:5173/?replay=1, to play the Isaac Lab
3.0 EA / Isaac Sim 6.1 rail videos for the current seed. The backend supplies
the selected seed; Replay waits for that selection instead of showing a
different layout. The ten provisional camera pairs loop at 960×540, 10 fps
(20.3 seconds), with normal lighting and three render updates per frame.
The worktop is one white satin mesh within the USD Table component. Click the small view to swap cameras
without restarting playback. Files live in `frontend/public/renders/seeds/p01/`
through `p10/`; `src/replayPatterns.json` maps seeds to the videos. Replay's
YOLO WebSocket receives the pattern name and decodes that same recording.

The lab
state panels read the state publisher on :8765: either this backend, or
`python -m labbridge.mock_run --fps 0 --loop` from `dashboard/bridge`, which
renders nothing and uses far less memory. Without a publisher they play the
recorded scripted run in `frontend/public/scripted-run.json`, so the panels
show the same formulation with only `npm run dev`. After changing the scripted
run, regenerate it with `python -m labbridge.record_run` from `dashboard/bridge`.

## Bottle boxes

In Real time, the scan's tracked bottles are drawn over the general camera.
The header's **Boxes** button toggles the overlay; its setting is remembered.
Unidentified tracks show a number; confirmed samples show their catalogue ID in
green. Bottles found only by the wrist camera get a projected box as well.
Perception continues with boxes hidden and while Replay is selected. The
Pipeline retains live inference time, image size and track count from the scan.

For explicitly selected non-scan scenes, the optional detector runs while a
viewer subscribes, every `VIEW_DETECTOR_FRAME_STRIDE` rendered frames (default 5),
using `VIEW_DETECTOR_THREADS` torch threads (default 2). It uses the table crop
and discards intermediate frames rather than queuing inference.

It needs `ultralytics` in the backend's venv and the weights: `VIEW_DETECTOR`
names a `labvision.detector` backend or a weights path, and the default,
`rail`, is the YOLO26n trained on this camera in the rail scene, which the
backend finds as `computer-vision/weights/yolo26n_rail_general.pt` (not in git;
get it from the team Drive, `hackathon/yolo26n_rail_general`, and see
`computer-vision/weights/README.md`). The boxes use its best-F1 threshold,
0.47, rather than the backend's 0.10, which is set for `propose_confirm`'s
proposals; `VIEW_DETECTOR_CONF` overrides it. Without the weights the button is
greyed out and says why. On the rail scene's test frames the model finds 99 %
of the bottles on the bench at 99.6 % precision
(`computer-vision/scripts/fixedcam_bench.py`, splits `rail_*`).

## Lab state panels

The same backend also publishes the full `LabState` (see
`dashboard/bridge/README.md` for the protocol) on `ws://localhost:8765/state`.
It is driven by the scripted formulation in
`dashboard/bridge/labbridge/mock_run.py` (recipe FRG-031, four liquids,
one recovery: the Eugenol flask is displaced in the demo state). This script
uses separate MuJoCo data for the panels; it never moves bottles in the
camera scene. The live scan remains independent. It needs `websockets` in the venv (listed
in `backend/requirements.txt`).

When that state is connected, the frontend shows it (`src/LabTaskPanel.jsx`,
`src/LabPanels.jsx`); without it, the task panel falls back to the mocked log
above.

- **Robot tasks**: run id, status and clock, a `SCRIPTED` badge while the
  sequence is not the real planner, then the formula with each ingredient
  crossed off once added (with its deviation from target, and a progress bar on
  the one being dosed), then the plan around the current step, grouped by
  ingredient: the last few steps done, the active one (amber while it is
  recovering), and the next three.
- **Robot** and **Balance** under the viewport: the rail with the balances and
  the carriage, and the current dose's net mass rising towards its target. A
  panel lights its top edge while its module is working.
- **Pipeline**, under the tasks: the modules from camera to mass check, each
  with its status and live figure, and the latest event.

The camera, tasks and Pipeline are always shown. Robot and Balance
open and close from the buttons in the header, and the edges between views
drag to resize them (double-click an edge to reset it). The layout is
remembered in the browser.

To rehearse a moment, start the backend part-way and slowed down:

```sh
LAB_STATE_START=100 LAB_STATE_SPEED=0.25 simulation/.venv/bin/python view/backend/server.py
```

The recovery starts at about 101 s and the recipe completes at about 172 s.

Replace `ScriptedRun` with the real planner when it exists; the state contract
stays the same.

Replay also supports **Boxes** on the general camera. With the backend running,
`/ws/replay-detections` performs one inference at a time on the video's current
time plus the previous request's measured round-trip latency (capped at one
second). A separate process decodes the future frame; the displayed video never
waits for inference. Early results wait for their video timestamp, and boxes
older than 500 ms disappear. Loops and seeking invalidate obsolete results.
The viewport label shows measured inference and round-trip times; the side
panels continue to read live lab state.

Copy the Drive `General MAFER AI/hackathon/yolo26n_rail_general/yolo26n_rail_general.pt` weights to
`computer-vision/weights/yolo26n_rail_general.pt` (or set `VIEW_REPLAY_WEIGHTS`).
Replay detection uses rail weights at 1280 px and confidence 0.47, and requires
Ultralytics in the backend environment. It crops the fixed general camera to
the table band (30–75% of frame height, full width) before inference, removing
background while preserving the samples. Boxes are translated back to full-video
coordinates; playback stays at its original resolution. Recheck this crop if
the camera framing changes. The backend and frontend must use the
same `view/frontend/public/renders/seeds/<pattern>/rail_global.mp4`. Videos
continue playing without detection once the seed has been selected. Restart
the backend after upgrading from the single-video replay so it can acknowledge
the selected pattern; the frontend rejects boxes from an older backend.
