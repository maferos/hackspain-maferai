# Robot viewer

Frontend to watch the mini-Hannover MuJoCo scene live: main viewport switchable
between the robot's onboard camera and the fixed scene-overview camera, a
picture-in-picture subwindow showing the other one (click it to swap), and
side panels that follow the bench scan live, with a chat to check a formula
against what the scan found.

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

The Tasks, Robot, Balance and Pipeline panels show this scan, in both modes
(see Lab state panels below).

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
`full`, is the YOLO26n trained on MuJoCo renders of this scene from every
angle, which the backend finds as
`computer-vision/weights/yolo26n_full_1920_e25.pt` (not in git; get it from the
team Drive, `hackathon/weights/yolo26n_full_1920_e25`, and see
`computer-vision/weights/README.md`). The boxes use that backend's own best-F1
threshold, 0.41; `VIEW_DETECTOR_CONF` overrides it. Without the weights the
button is greyed out and says why. Replay stays on
`yolo26n_rail_general.pt`, the model scored against those Isaac videos. On the rail scene's test frames the model finds 99 %
of the bottles on the bench at 99.6 % precision
(`computer-vision/scripts/fixedcam_bench.py`, splits `rail_*`).

## Lab state panels

The same backend also publishes the full `LabState` (see
`dashboard/bridge/README.md` for the protocol) on `ws://localhost:8765/state`.
With the scan, that state is the scan itself (`backend/scan_state.py`, a few
times a second): vision_pick's tracks and what their rings said, the arm's
joints and gripper, the controller's caption, and its log as events. Nothing is
scripted; a panel with nothing to show says it is waiting. Scenes without the
scan still replay the scripted formulation of
`dashboard/bridge/labbridge/mock_run.py` (recipe FRG-031). It needs
`websockets` in the venv (listed in `backend/requirements.txt`).

- **Robot tasks**: run id (`SCAN-P06` for seed pattern p06), status and
  simulated clock; the scan's tally (flasks named by their ring out of those on
  the bench, still to look at, not samples, out of reach); then the plan around
  the current step: park, survey, each track's ring (named, not a sample, out
  of reach, or next), and the bench map. A `SCRIPTED` badge marks the recorded
  run, which plays when no backend is running.
- **Robot** under the viewport: the controller's state and caption, the track
  or sample it is working on, the ring it read, the gripper (open or holding),
  and the carriage on the rail.
- **Balance**: `balance_2`, with the mass the executor reports for the
  ingredient being dosed, against its target; 0.000 g when nothing is.
- **Pipeline**, under the chat: camera cycle, live YOLO time, tracks on the
  bench and how many a ring placed, rings named, the controller, the rail, and
  the bench map. The footer is the scan's latest log line.

## Formula chat

The **Formula** panel between the tasks and the Pipeline checks a formula
against the flasks the scan has named by their rings, never against the
simulator's list, and shows it as the JSON the robot will receive (the `{ }`
button on the proposal, with copy):

| Type | And |
| --- | --- |
| `What's on the bench?` | the compounds the scan has identified, with their sample ids |
| `1.2 g geraniol, 0.5 g nerol` (either order, `1,2 g`, Spanish names) | the formula, each line with the flask the scan found or "not identified on the bench" |
| `40 % geraniol, 60 % nerol, total 2 g` | the same from percentages |
| `FRG-101`, `5 g of FRG-103` | one of the five formulas in `harness/formulas`, scaled (3 g by default) |
| JSON, pasted, dropped on the panel or loaded with `{ }` | the same check; any `harness/formulas` file, this viewer's own order JSON, `[{"compound", "grams"}]` lines, or `{"id": "FRG-101", "batch_g": 3}` |
| **Send to robot**, or `send` / `dale` | the formula becomes the robot's order (below) |
| **Stop**, or `stop` / `para` | the order stops |

Without `ANTHROPIC_API_KEY` a small parser (`backend/formula_chat.py`) reads
the forms above and the panel says `OFFLINE PARSER`; with the key and
`anthropic` in the venv, Claude (`VIEW_CHAT_MODEL`, default `claude-opus-5`)
reads free-form requests and proposes formulas from the identified flasks.
Once an order is running the robot narrates in the chat each step it crosses
off, with the order's clock.

## The order and its workflow

A formula sent to the robot becomes an order (`backend/workflow.py`), `ORD-001`
onwards, one at a time:

    order:        Scan → Formula → Check → Dose → QC → Done
    ingredient:   locate → pick → carry → dose → verify → return

The panels follow it: the task panel's stage bar and one row per ingredient
with its steps as dots, crossed off as they finish, and below it the plan with
the done steps struck through; the header's status line (`ORD-001 · Dose 2/3 ·
01:23`); the Balance panel with the ingredient being dosed against its target;
the Pipeline's order, executor and QC rows; and the chat's narration.

**For the executor.** The order is written to
`simulation/out/formula_order.json` and served at `GET /api/formula`: the
`harness/formulas` format (`material`, `cas`, `batch_g`, `concentrate_pct`,
`samples`), plus for each line the flask the scan found (`sample_id`,
`located: {x, y, track}`) or why there is none (`problem`), the balance
(`balance_2`) and the tolerance (±0.010 g). The executor reports each step, in
process with `scene.lab.workflow.report(...)` or over HTTP:

```sh
curl -X POST localhost:8000/api/workflow/report -H 'Content-Type: application/json' \
  -d '{"ingredient": "SMP-0014", "step": "dose", "status": "active", "mass": 0.84, "note": "slow pour"}'
```

`ingredient` is the sample id, the compound or the ingredient id; `status` is
active, completed, failed or skipped; `mass` is the net balance reading for that
ingredient, which also draws the Balance chart. Reporting a step finishes the
ones before it. The backend crosses off by itself what it can see: the scan
naming the flask (locate), the controller's captions and the gripper (pick,
return), and the reported mass against the target (verify). The order closes
with QC when every step is done. `backend/example_executor.py` is a working
client of all this that does not move the arm, for trying the panels:

```sh
VIEW_FORMULA_EXECUTOR=external python view/backend/server.py
python view/backend/example_executor.py --speed 2
```

`VIEW_FORMULA_EXECUTOR` picks who takes the order: `fetch` (the default until
the real executor exists) has the arm fetch each flask through the scan
controller's own pick, locate → pick → return, and says it was fetched, not
dosed; `external` leaves the order to an executor that reports.

The camera, tasks and Pipeline are always shown. Robot and Balance
open and close from the buttons in the header, and the edges between views
drag to resize them (double-click an edge to reset it). The layout is
remembered in the browser.

To rehearse a moment of the scripted run (scenes without the scan), start the
backend part-way and slowed down:

```sh
LAB_STATE_START=100 LAB_STATE_SPEED=0.25 simulation/.venv/bin/python view/backend/server.py
```

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
