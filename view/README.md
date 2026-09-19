# Robot viewer

Frontend to watch the mini-Hannover MuJoCo scene live: main viewport switchable
between the robot's onboard camera and the fixed scene-overview camera, a
picture-in-picture subwindow showing the other one (click it to swap), and a
right-hand panel with the robot's running task log, updated in real time.

- `backend/` — FastAPI server. Renders both cameras from
  `simulation/models/minihannover_scene.xml` live with `mujoco.Renderer` and
  serves binary JPEGs over WebSocket (`/ws/camera/robot`, `/ws/camera/scene`),
  with legacy MJPEG endpoints (`/stream/robot`, `/stream/scene`), plus a websocket
  (`/ws/tasks`) with the task log. The task log is currently **mocked** — no
  real task/planner system exists in `simulation/` yet, so it just cycles
  through a scripted list of plausible lab actions. Swap in real data by
  replacing `TaskLog` in `backend/server.py`.
- `frontend/` — React + Vite app that renders the two streams and the task
  panel.

The two camera streams are the vision system's own cameras, defined at the
end of `simulation/models/minihannover_scene.xml`: `general` (the fixed
room GoPro) and `wrist` (a mocap-mounted stand-in for the future arm's wrist
camera — it doesn't move on its own yet, see the comment there for how to
fly it around).

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

Live YOLO processes only the table band (30–75% of image height, full width),
using the same crop as Replay. It retains the live input's pixel scale and
translates detections back to full-frame coordinates. The camera stream stays
uncropped. Recheck `view/backend/table_crop.py` when camera framing changes.

```sh
# 1. Backend deps, into the same venv simulation/ already uses:
uv pip install --python simulation/.venv/bin/python \
  -r simulation/requirements.txt -r view/backend/requirements.txt

# 2. Backend (serves streams + tasks on :8000):
simulation/.venv/bin/python view/backend/server.py

# 3. Frontend (:5173), in another terminal:
cd view/frontend
npm install
npm run dev
```

Then open http://localhost:5173. Set `VITE_BACKEND_URL` if the backend runs
somewhere other than `http://localhost:8000`.

By default the viewport shows the live MuJoCo cameras. Select **Replay** in
the header, or open http://localhost:5173/?replay=1, to play the Isaac Lab
3.0 EA / Isaac Sim 6.1 rail videos without a backend. The global and robot
cameras loop together at 1080p, 30 fps (20.267 seconds); click the small view
to swap cameras without restarting playback. The files are bundled in
`frontend/public/renders/rail_global.mp4` and `rail_robot.mp4`.

The lab
state panels read the state publisher on :8765: either this backend, or
`python -m labbridge.mock_run --fps 0 --loop` from `dashboard/bridge`, which
renders nothing and uses far less memory. Without a publisher they play the
recorded scripted run in `frontend/public/scripted-run.json`, so the panels
show the same formulation with only `npm run dev`. After changing the scripted
run, regenerate it with `python -m labbridge.record_run` from `dashboard/bridge`.

## Bottle boxes

In Real time the bottle detector's boxes are drawn over the general camera,
wherever that camera is shown; the header's **Boxes** button turns them off and
on, and the choice is remembered in this browser. The backend runs the
detector while a viewer has Boxes or Pipeline open, every 5 rendered camera frames
(`VIEW_DETECTOR_FRAME_STRIDE`), with `VIEW_DETECTOR_THREADS` (2) torch
threads so the streams keep their frame rate; the boxes lag the picture by one
inference (about 0.4 s on a laptop CPU).
The first detection runs immediately. Between detections the last boxes stay
visible. If inference takes longer than 5 frames, it skips ahead to the newest
frame instead of building a queue.
YOLO runs in a separate Python subprocess, so its preprocessing and torch
inference cannot hold the renderer's Python interpreter lock. Only the
detector thread waits for results; camera rendering and streaming continue.
The Pipeline's Object detection row uses the live detector's inference time,
input size and detection count. Opening Pipeline keeps this feed active even
with Boxes off or the viewport in Replay. It shows an offline/waiting state
when no live measurement is available, rather than scripted timing figures.

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
camera scene. The rail sweep remains independent. It needs `websockets` in the venv (listed
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

The camera is always shown; the other views (Robot, Balance, tasks, Pipeline)
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
same `view/frontend/public/renders/rail_global.mp4`. Videos still play without
the backend or weights; only detection becomes unavailable.
