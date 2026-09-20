# Robot viewer

Frontend to watch the mini-Hannover MuJoCo scene live: main viewport switchable
between the robot's onboard camera and the fixed scene-overview camera, a
picture-in-picture subwindow showing the other one (click it to swap), and
panels under it that follow the bench scan live, and a chat down the right-hand
side to check a formula against what the scan found.

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

The Balance, Current formula and Formulas asked panels show this scan, in both
modes (see Lab state panels below).

## Run it

The MuJoCo model and confidence threshold are intentionally hardcoded in
`backend/detector_config.py`: `yolo26n_full_1920_e25.pt` at 0.41. Copy the file
into `computer-vision/weights/`. Upgrading the detector requires editing that
code and restarting the backend; environment variables cannot select a model
or override its threshold. Both live scanning and live box detection share
these constants. Missing weights produce an error instead of loading an older
model. Replay's separate model is pinned in the same file.

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
a random bench layout from the four shared `minihannover_open/patterns` seeds.
The next choice excludes the current pattern. To choose a specific scene, open
`http://localhost:5173/?replay=0&scene=3`: `scene=1` through `scene=4` select
`p01` through `p04`. The scene number is independent of its internal random seed. The backend replaces the rail
scene's loose and dynamic bench samples with that catalogue population in
memory, excluding the 10 ml flasks; the reported sample count includes only
the remaining flasks. It never rewrites generated scene files. All connected tabs share the
new layout, and the viewport label shows its seed and sample count. Requests
are deduplicated per page load, including React StrictMode and network retries.
The render thread stops the previous scan and detector worker, installs the new
MuJoCo model and graphics context, and starts a fresh scan. Tracks and identities
from the old layout are discarded. Replay selects the recording for that same seed; switching modes does not
request a new layout. The current Replay recordings exclude 10 ml sample flasks.
The panel demo retains its original model, samples and `RECIPE`, so
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
different layout. Patterns `p01` and `p02` play the double-rail XYZ gantry with Eki's
vertical hand, without the overhead extractors. The corrected marker reader
identified all 7 and 22 vessels respectively; each scan travels left to right
at constant height. Patterns `p03`–`p04` retain their hanging-arm recordings. All four play at
1920×1080, 10 fps, with normal lighting and three render updates per frame.
Their compiled sample models and exported USDs were checked: no 10 ml sample
flasks remain on the scan bench. Replay keeps the current seed when switching
from Real time.

| Pattern | Seed | Flasks | Identified | Video duration | Both views rendered in |
| --- | ---: | ---: | ---: | ---: | ---: |
| p01 | 30 | 7 | 7 | 46.2 s | 138 s |
| p02 | 176 | 22 | 22 | 80.3 s | 235 s |
| p03 | 21 | 29 | 29 | 129.8 s | 381 s |
| p04 | 327 | 33 | 31 | 240 s | 716 s |

Render times were measured on an NVIDIA L4 and include Isaac startup and
MP4 encoding, excluding scan recording, USD export and transfer. The p04
recording stops at the 240-second limit before its scan completes, recorded
as `scan_complete: false` in the replay manifest.

The worktop is one white satin mesh within the USD Table component. Click the small view to swap cameras
without restarting playback. Files live in `frontend/public/renders/seeds/p01/`
through `p04/`; `src/replayPatterns.json` maps seeds to the videos. Replay's
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
Live inference time, image size and track count stay on the viewport label.

For explicitly selected non-scan scenes, the optional detector runs while a
viewer subscribes, every `VIEW_DETECTOR_FRAME_STRIDE` rendered frames (default 5),
using `VIEW_DETECTOR_THREADS` torch threads (default 2). It uses the table crop
and discards intermediate frames rather than queuing inference.

It needs `ultralytics` in the backend's venv and the pinned weights.
The `full` model is the YOLO26n trained on MuJoCo renders of this scene from every
angle, which the backend finds as
`computer-vision/weights/yolo26n_full_1920_e25.pt` (not in git; get it from the
team Drive, `hackathon/weights/yolo26n_full_1920_e25`, and see
`computer-vision/weights/README.md`). The boxes use that backend's own best-F1
threshold, 0.41, pinned in `backend/detector_config.py`. Without the weights the
button is greyed out and says why. Replay uses
`yolo26n_isaac_v2.pt`, trained on Isaac renders with PWD and SMP classes. On the rail scene's test frames the model finds 99 %
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

- **Current task**, in the left drawer under the asked list: what the lab is
  doing now. A task is the bench scan or a formula, and the badge says which.
  Run id (`SCAN-P04` for seed pattern p04), status and
  simulated clock; the scan's tally (flasks named by their ring out of those on
  the bench, still to look at, not samples, out of reach); then the plan around
  the current step: park, survey, each track's ring (named, not a sample, out
  of reach, or next), and the bench map. A `SCRIPTED` badge marks the recorded
  run, which plays when no backend is running.
- **Balance**, the narrow panel at the left of the dock: `balance_2` and the
  mass on its pan, nothing else; 0.000 g when nothing is being dosed.
- **Formulas asked**, the third panel in the dock: one line per formula the
  operator has put to the chat, newest last — its name, its compounds and
  grams, and what became of it: proposed and not sent, sent as `ORD-00n`, or
  rejected at the check with the reason underneath. The chat scrolls away and
  this does not, which is the point of it.

## The brief chat

What the operator types is a **brief** — "something fresh and citrusy for
summer, light" — not a formula. It joins the queue in those words and a model
writes it into a real fragrance when its turn comes (`backend/brief.py`).

**The model is asked for very little on purpose.** Only the creative part: a
name, a family, a product strength, one sentence of description, and a list of
`(compound, percent)`. It is never asked for the formula JSON.
`harness/build_formulas.build_formula` — the same function that built the five
fragrances in `harness/formulas/` — expands a spec that size into the harness
format and refuses anything wrong with it: percentages that do not sum to 100,
a compound outside the catalogue, an ingredient over its IFRA Category 4 limit.
Asking a model for the fifteen fields it would otherwise have to get right is
asking it to be wrong; asking for the two that need taste means a formula that
reaches the queue is correct by construction.

**The palette is the bench, not the catalogue.** The model only sees compounds
the scan has named, with the grams left in the fullest flask of each and its
IFRA ceiling. `brief.py` adds the two checks the builder cannot make, because
they are facts about this bench rather than about perfumery: that the compound
is standing here at all, and that the flask holds the dose. A brief is
therefore composed **when its turn comes**, never when it is sent — while the
scan is still reading the bench the palette is a fraction of it, and a
fragrance written against that is written against ignorance.

**A rejected build is a conversation.** The builder's complaint goes back to
the model, which tries again, up to `brief.ATTEMPTS` times.

`ANTHROPIC_API_KEY` in the gitignored `view/backend/.env` is required: there is
no offline path for briefs. `VIEW_BRIEF_MODEL` picks the model, default
`claude-sonnet-5`. Asking what is on the bench is still answered as a question
rather than taken as a brief.

## Formula chat

The **Formula** panel, which is the whole right-hand column, checks a formula
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

## Tasks: the scan first, then the queue

The lab does one task at a time, and a task is one of two things: **the bench
scan** or **a formula**. They are not the same shape and do not share a bar.

    scan task:     Scan
    formula task:  Formula → Check → Fetch → Done

The scan is always the first task and its only step is the scan itself. A
formula carries no scan stage: the bench is read once, by the lab, and a
formula that runs afterwards does not repeat it.

Nothing else starts beside the scan. A formula sent while the bench is being
read is accepted onto the queue and waits — it is not part of the scan's task,
so it appears in **Formulas asked** as `QUEUED` with its order id, and the
Current task panel stays wholly the scan: its run id, its single-step bar and
its own plan, with no trace of a formula in it. The chat's button says **Add to
queue** while the scan runs.

Waiting is not the same as being deferred. A queued formula is **not checked**
while the scan runs, because which flasks are on the bench is not known yet and
a formula refused for a flask nobody has looked at is a wrong answer given
early. When the scan finishes, the formula at the front of the queue is matched
to the bench **again** — the bench it is judged against is the whole bench, not
the fraction that had been read when it was sent — then checked, planned, and
handed to the arm. The next one waits for that to finish.

`Workflow.pump()` admits one order per call and `ScanState._pump()` calls it
every tick, so a formula sent mid-scan starts by itself when the bench is
mapped. `Workflow.order` is the front of the queue, and `Workflow.waiting()`
the rest.

## The order and its workflow

A formula the queue has admitted becomes an order (`backend/workflow.py`),
`ORD-001` onwards, one running at a time:

    order:        Formula → Check → Fetch → Done
    ingredient:   locate → pick → carry → dose → verify → return

The panels follow it: the Current task panel's stage bar and one row per
ingredient with its steps as dots, crossed off as they finish, and below it the
plan with the done steps struck through; the header's status line (`ORD-001 ·
Fetch 2/3 · 01:23`); the Balance panel with the mass on the pan; and the chat's
narration.

**Every failure shows on the stage that failed**, never at the end: a rejected
formula stops at Check with the rest of the bar skipped, a dose that failed
marks Fetch, and Done never fails on someone else's behalf.

### The plan under each ingredient

An order that passes the check is planned by `harness/formula_to_actions`, the
same planner `harness/run_formula.py` runs offline, but against the bench this
scan is looking at rather than a lookup table from another machine.
`backend/actions.py` is the bridge: it turns the scan's shelf into the entries
the planner reads, asks the compiled scene which bottles have a free joint, and
maps each of the planner's ten verbs onto the executor step that crosses it off.

Each ingredient therefore shows its ten primitives — locate, traverse,
approach, read barcode, verify id, pick, to balance, dose, weigh, return — with
the line of English a VLA would be given and, where a skill exists behind it
(`pick`, `place`), a chip naming it. The five before the pick all belong to
`locate`, because travelling to a flask, approaching it and reading its ring is
one act for this scan and they finish together. Dosing and weighing are shown
dimmed: `armlab` has no skill for either, and the plan says so rather than
inventing one.

The plan is read-only. The six steps still run the order; the heap is the same
order spelled out the way the robot would be told. It is planned once, when the
order is made, and an order the planner cannot handle simply has none.

### The check, and what a flask still holds

The check is where a formula is accepted or refused, and it refuses whole. A
formula the bench can only half make is not run with the half it has: the order
goes to `rejected`, not a step of it is attempted, the Check stage is marked
failed with the reasons, the chat says which line and why, and a toast over the
viewport asks for the compound to be restocked. Two things fail it:

- **A compound no flask on the bench carries** — the scan never named one.
- **A flask without enough left in it.** Flasks are not full. The lookup table
  carries a capacity and no level, so `catalogue.Levels` invents one per sample,
  derived from the sample id, so every machine and every restart agrees; about
  one flask in six starts nearly empty. `resolve` picks the *fullest* flask of a
  compound, not the biggest, and a dose larger than what is in it fails the
  check — `only 0.4 g left in SMP-0039 (50 ml flask)`. Dosing draws the level
  down, so the next formula's check sees what the last one used. Millilitres are
  read as grams (`G_PER_ML`); the catalogue carries no densities.

`Levels.set_ml` puts a flask at a known level, for tests and for staging a demo
where the check has to fail on cue.

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

Three columns. The **formulas drawer** down the left stacks Formulas asked over
Current formula; the camera has the middle to itself, top to bottom; the right
column carries the Balance and Info side by side, half of it each, over the
Formula chat. Both side columns take their space from the camera rather than
covering it, and Formulas, Balance and Info each open and close from their
button in the header — the readout row disappears when both of its panels are
closed, leaving the chat the whole column. The edges between views drag to
resize them, including the split between the two drawer panels and the one
under the readouts (double-click an edge to reset it), and the layout is
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

Copy the Drive `General MAFER AI/hackathon/yolo26n_isaac_v2/best.pt` weights to
`computer-vision/weights/yolo26n_isaac_v2.pt` (pinned in `backend/detector_config.py`).
Replay detection uses Isaac v2 weights on full frames at 1600 px, with an
initial confidence cutoff of 0.25 (not a calibrated best-F1 threshold for these
videos). It requires Ultralytics in the backend environment. Box coordinates
remain in the original video's pixels; playback retains its original resolution.
The backend and frontend must use the
same `view/frontend/public/renders/seeds/<pattern>/rail_global.mp4`. Videos
continue playing without detection once the seed has been selected. Restart
the backend after upgrading from the single-video replay so it can acknowledge
the selected pattern; the frontend rejects boxes from an older backend.
