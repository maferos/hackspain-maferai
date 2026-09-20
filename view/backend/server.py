"""Backend for the robot viewer frontend.

Serves the rail bench's live MuJoCo cameras while vision_pick scans its samples.
The original YOLO / ArUco perception and robot controller drive the viewport;
the scan's progress and sample identities accompany the camera streams.

It also publishes the full `LabState` that the lab state panels render, on
`ws://localhost:8765/state`: the live scan's own state (scan_state.py), and the
formula chat's requests (`/api/chat`). Scenes without the scan replay the scripted
formulation of `labbridge.mock_run` on separate simulation data. The panel demo
never moves containers in the camera scene.

Usage:
    .venv/bin/python view/backend/server.py
Then open view/frontend (see its README) against this server's port (8000).
"""
from __future__ import annotations

import asyncio
import json
import random
import re
import subprocess
import os
import sys
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path

import mujoco
import numpy as np
from jpeg_encoder import JpegEncoder, PREVIEW_SIZE
from fastapi import Body, FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from scene_patterns import CATALOGUE, build_pattern
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def load_env(path: Path) -> None:
    """Read KEY=value lines from a local .env (gitignored) into the environment.

    For ANTHROPIC_API_KEY, which turns on Claude in the formula chat. Anything
    already set in the environment wins.
    """
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.strip().partition("=")
        if sep and key and not key.startswith("#"):
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


load_env(Path(__file__).with_name(".env"))

# VIEW_SCENE picks the MuJoCo model to render: a bare name resolves under
# simulation/models/, or pass an absolute path. Defaults to the rail bench scan.
# A scene without the scripted run's samples (e.g. minihannover_open_scene.xml)
# still streams live; only the LabState/task feed is skipped for it.
_scene_env = os.environ.get("VIEW_SCENE", "minihannover_rail_scene.xml")
SCENE_PATH = Path(_scene_env)
if not SCENE_PATH.is_absolute():
    SCENE_PATH = REPO_ROOT / "simulation" / "models" / SCENE_PATH

SCAN_ENABLED = SCENE_PATH.name in {
    "minihannover_rail_scene.xml", "minihannover_rail_gripper_scene.xml",
}
if SCAN_ENABLED:
    from live_scan import LiveScan, scan_scene
    SCENE_PATH = scan_scene()

sys.path.insert(0, str(REPO_ROOT / "dashboard" / "bridge"))
sys.path.insert(0, str(REPO_ROOT / "computer-vision"))
from labbridge.mock_run import ACTIVE_BALANCE, RAIL, ScriptedRun  # noqa: E402
from labbridge.mujoco_adapter import vessels, workcell  # noqa: E402
from labbridge.server import StateServer  # noqa: E402
from detector_config import DETECTOR_SPEC, DETECTOR_WEIGHTS, DETECTOR_CONF, REPLAY_WEIGHTS
from catalogue import Catalogue, resolve, shelf_from_tracks  # noqa: E402
from formula_chat import MODEL as CHAT_MODEL, FormulaChat  # noqa: E402


def build_id() -> str:
    """The commit the viewer is running, for the Info panel; "" outside git."""
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT,
                              capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


COMMIT = build_id()

STATE_PORT = int(os.environ.get("VIEW_STATE_PORT", "8765"))
STATE_RATE_HZ = 10
STATE_LOOP_PAUSE_S = 15.0
# Rehearsal knobs: where the scripted run starts (seconds) and how fast it plays.
# LAB_STATE_START=100 LAB_STATE_SPEED=0.25 shows the recovery in slow motion.
STATE_START_S = float(os.environ.get("LAB_STATE_START", "0"))
STATE_SPEED = float(os.environ.get("LAB_STATE_SPEED", "1"))

# Logical camera id -> MuJoCo camera in the loaded scene. `scene` is the fixed
# room GoPro (`general`). `robot` is the camera the robot actually carries: the
# arm's eye-in-hand camera (`arm_eih`) when the scene has an arm, falling back
# to the mocap-mounted `wrist` stand-in otherwise. `hide_groups` lists geom
# groups to hide for that camera.
def resolve_cameras(model: "mujoco.MjModel") -> dict:
    names = {
        mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_CAMERA, i) for i in range(model.ncam)
    }
    robot = "arm_eih" if "arm_eih" in names else "wrist"
    return {
        "robot": {"mj_name": robot, "label": "Robot camera", "hide_groups": []},
        "scene": {"mj_name": "general", "label": "General camera", "hide_groups": []},
    }

FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080
RENDER_FPS = 15
JPEG_QUALITY = 80
PREVIEW_FPS = 5

# Model and threshold are intentionally pinned in detector_config.py.
DETECTOR_CAMERA = "scene"  # logical id; the model only knows the fixed camera
DETECTOR_FRAME_STRIDE = int(os.environ.get("VIEW_DETECTOR_FRAME_STRIDE", "5"))
if DETECTOR_FRAME_STRIDE < 1:
    raise ValueError("VIEW_DETECTOR_FRAME_STRIDE must be at least 1")
# Torch threads: few enough that the renderer keeps its frame rate.
DETECTOR_THREADS = int(os.environ.get("VIEW_DETECTOR_THREADS", "2"))

# When the loaded scene is the railed arm (no LabState-compatible scripted run),
# the viewport would otherwise stand still. Instead it plays rail_demo's `sweep`:
# the carriage runs the length of the bench holding a hand-down scan pose. Posed
# kinematically per frame so it stays smooth and can't knock the glassware over.
RAIL_SWEEP_SPEED = 0.8  # carriage speed, m/s

# --- MuJoCo scene, stepped continuously in a background thread -----------


class SceneRenderer:
    """Steps physics and renders every camera from a single dedicated thread.

    mujoco.Renderer's GL context is bound to the thread that created it, so
    calls to update_scene()/render() must all happen on that one thread —
    calling render from FastAPI's request threadpool produced black frames.
    This thread publishes RGB arrays; a separate encoder compresses the newest
    frame per camera and stream handlers read its cached JPEG bytes.
    """

    def __init__(self, xml_path: Path) -> None:
        self.stop = threading.Event()
        self.model = mujoco.MjModel.from_xml_path(str(xml_path))
        self.data = mujoco.MjData(self.model)
        self.panel_model = self.model
        self.pending_pattern = None
        self.pattern = None
        self.generation = 0
        mujoco.mj_forward(self.model, self.data)
        self.encoder = JpegEncoder(JPEG_QUALITY)
        threading.Thread(target=self.encoder.run_forever, daemon=True).start()
        self._main_watchers: dict[str, int] = {}
        # Latest rendered RGB for the detector, independent of JPEG latency.
        self._latest_rgb: dict[str, np.ndarray] = {}
        self._frame_seq: dict[str, int] = {}
        self._condition = threading.Condition()
        # Guards the viewport's physics and rendering data.
        self._data_lock = threading.Lock()

        # The panel demo gets its own MjData: its kinematic bottle animation
        # must never modify the scene rendered by the camera thread.
        # A scene without the scripted run's samples (e.g. the open lab) still
        # renders its camera streams; only the LabState feed is skipped.
        try:
            self.panel_data = mujoco.MjData(self.model)
            mujoco.mj_forward(self.model, self.panel_data)
            self.run = ScriptedRun(self.model, self.panel_data, vessels(self.model))
        except Exception as exc:  # noqa: BLE001
            print(
                f"[view] no scripted run for {xml_path.name}: {exc!r}; "
                "streaming cameras only, LabState feed disabled",
                file=sys.stderr,
            )
            self.run = None
        self.state_server = StateServer(port=STATE_PORT)

        # Which MuJoCo camera each logical view maps to depends on the scene.
        self.cameras = resolve_cameras(self.model)
        self._scene_options: dict[str, mujoco.MjvOption] = {}
        for info in self.cameras.values():
            opt = mujoco.MjvOption()
            mujoco.mjv_defaultOption(opt)
            for group in info["hide_groups"]:
                opt.geomgroup[group] = 0
            self._scene_options[info["mj_name"]] = opt

        # Optional scripted viewport motion (the rail sweep for the railed scene;
        # None for scenes that just step physics as before).
        self.scan = None
        self._motion = None if SCAN_ENABLED else self._build_rail_sweep()

    def _build_rail_sweep(self) -> dict | None:
        """Precompute rail_demo's `sweep` for the railed scene, else return None.

        The sweep is a list of per-frame rows (carriage X, then six arm joint
        angles) that the render loop plays back kinematically. Any scene without
        the `rail_x` actuator (the benches, the open lab) has no sweep and steps
        physics as before.
        """
        try:
            self.model.actuator("rail_x")
        except KeyError:
            return None
        scripts = str(REPO_ROOT / "simulation" / "scripts")
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        try:
            import rail_demo  # noqa: E402  (pulls in rail_kinematics via sys.path)
            import rail_kinematics as rk  # noqa: E402

            waypoints = rail_demo.sweep_waypoints(self.model, self.data)
            rows = rail_demo.trajectory(self.model, waypoints, speed=RAIL_SWEEP_SPEED)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[view] no rail sweep for {SCENE_PATH.name}: {exc!r}; "
                "viewport is static",
                file=sys.stderr,
            )
            return None
        return {"rows": rows, "arm_qpos": rk.arm_qpos(self.model), "set_rail": rk.set_rail, "i": 0}

    def _advance_motion(self) -> None:
        """Pose the machine at the next sweep frame (caller holds _data_lock)."""
        motion = self._motion
        rows = motion["rows"]
        row = rows[motion["i"] % len(rows)]
        motion["set_rail"](self.model, self.data, float(row[0]))
        self.data.qpos[motion["arm_qpos"]] = row[1:]
        mujoco.mj_forward(self.model, self.data)
        motion["i"] += 1

    def run_forever(self) -> None:
        # One GL context and framebuffer, two viewport sizes. Separate Renderer
        # objects would duplicate GPU resources and switch contexts every frame.
        gl = mujoco.GLContext(FRAME_WIDTH, FRAME_HEIGHT)
        gl.make_current()
        context = mujoco.MjrContext(self.model, mujoco.mjtFontScale.mjFONTSCALE_150.value)
        mujoco.mjr_setBuffer(mujoco.mjtFramebuffer.mjFB_OFFSCREEN, context)
        render_scene = mujoco.MjvScene(self.model, maxgeom=10000)
        camera = mujoco.MjvCamera()
        camera.type = mujoco.mjtCamera.mjCAMERA_FIXED
        period = 1.0 / RENDER_FPS
        names = [info["mj_name"] for info in self.cameras.values()]
        due = dict.fromkeys(names, 0.0)
        was_main = dict.fromkeys(names, False)
        if SCAN_ENABLED:
            self.scan = LiveScan(self.model, self.data, self._data_lock, self.generation)
        while not self.stop.is_set():
            start = time.monotonic()
            if self.pending_pattern is not None:
                model, info, finished = self.pending_pattern
                self.pending_pattern = None
                try:
                    if self.scan:
                        self.scan.close()
                    new_context = mujoco.MjrContext(model, mujoco.mjtFontScale.mjFONTSCALE_150.value)
                    mujoco.mjr_setBuffer(mujoco.mjtFramebuffer.mjFB_OFFSCREEN, new_context)
                    new_scene = mujoco.MjvScene(model, maxgeom=10000)
                    with self._data_lock:
                        self.model = model
                        self.data = mujoco.MjData(model)
                        mujoco.mj_forward(model, self.data)
                        self._motion = None if SCAN_ENABLED else self._build_rail_sweep()
                        self.pattern = info
                    context.free()
                    context, render_scene = new_context, new_scene
                    with self._condition:
                        self._latest_rgb.clear()
                        self.generation += 1
                    if SCAN_ENABLED:
                        self.scan = LiveScan(self.model, self.data, self._data_lock, self.generation)
                    due = dict.fromkeys(names, 0.0)
                except Exception as exc:
                    info['error'] = str(exc)
                finally:
                    finished.set()
            with self._data_lock:
                if self.scan is not None:
                    self.scan.advance(period)
                elif self._motion is not None:
                    self._advance_motion()
                else:
                    mujoco.mj_step(self.model, self.data)
            for name in names:
                main = self._main_watchers.get(name, 0) > 0
                if start < due[name] and main == was_main[name]:
                    continue
                width, height = (FRAME_WIDTH, FRAME_HEIGHT) if main or name == "general" else PREVIEW_SIZE
                camera.fixedcamid = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_CAMERA, name)
                with self._data_lock:
                    mujoco.mjv_updateScene(self.model, self.data, self._scene_options[name],
                                          None, camera, mujoco.mjtCatBit.mjCAT_ALL.value, render_scene)
                viewport = mujoco.MjrRect(0, 0, width, height)
                rgb = np.empty((height, width, 3), dtype=np.uint8)
                mujoco.mjr_render(viewport, render_scene, context)
                mujoco.mjr_readPixels(rgb, None, viewport, context)
                rgb = np.flipud(rgb).copy()
                with self._condition:
                    self._latest_rgb[name] = rgb
                    self._frame_seq[name] = self._frame_seq.get(name, 0) + 1
                self.encoder.submit(name, rgb)
                due[name] = start + 1.0 / (RENDER_FPS if main else PREVIEW_FPS)
                was_main[name] = main
            remaining = period - (time.monotonic() - start)
            if remaining > 0:
                time.sleep(remaining)

    def latest_rgb(self, mj_camera_name: str) -> tuple[np.ndarray | None, int, int]:
        """RGB and sequence number of this camera, independent of JPEG encoding."""
        with self._condition:
            return (self._latest_rgb.get(mj_camera_name),
                    self._frame_seq.get(mj_camera_name, 0), self.generation)

    def watch_main(self, name: str, delta: int) -> None:
        with self._condition:
            self._main_watchers[name] = self._main_watchers.get(name, 0) + delta

    def frames(self, mj_camera_name: str):
        """Legacy MJPEG clients subscribe to the full-resolution camera."""
        last = None
        self.watch_main(mj_camera_name, +1)
        try:
            while True:
                with self.encoder.condition:
                    self.encoder.condition.wait_for(
                        lambda: self.encoder.latest.get((mj_camera_name, False)) is not last)
                    last = self.encoder.latest[mj_camera_name, False]
                yield last
        finally:
            self.watch_main(mj_camera_name, -1)

    def _snapshot_state(self) -> None:
        self.state_server.snapshot(self.run.initial_state(workcell(self.panel_model, self.panel_data, ACTIVE_BALANCE, RAIL)))

    def publish_state_forever(self) -> None:
        """Publishes LabState: the live scan's, or the scripted formulation at STATE_RATE_HZ."""
        if SCAN_ENABLED:
            from scan_state import ScanState
            self.lab = ScanState(self, self.state_server, catalogue)
            self.lab.run_forever()
            return
        if self.run is None:
            return  # scene has no compatible scripted run; cameras still stream
        self.state_server.start()
        self._snapshot_state()
        period = 1.0 / STATE_RATE_HZ
        t0 = time.time() - STATE_START_S / STATE_SPEED
        last: dict = {}
        while True:
            tick = time.time()
            t = (tick - t0) * STATE_SPEED
            if t >= self.run.duration + STATE_LOOP_PAUSE_S * STATE_SPEED:
                t0, last = tick, {}
                self._snapshot_state()
                t = 0.0
            last = self.run.apply(t, self.state_server, last)
            remaining = period - (time.time() - tick)
            if remaining > 0:
                time.sleep(remaining)


catalogue = Catalogue()
scene = SceneRenderer(SCENE_PATH)
renderer_thread = threading.Thread(target=scene.run_forever, daemon=True)
renderer_thread.start()
threading.Thread(target=scene.publish_state_forever, daemon=True).start()


class Detector:
    """Finds the bottles in the general camera's live frames while anyone watches.

    The model loads on first use and runs only while a /ws/detections client is
    connected, every DETECTOR_FRAME_STRIDE rendered frames, on the newest frame it has
    made; the boxes lag the picture by one inference, which the static bottles
    do not show. Without ultralytics or the weights, the viewer just offers no
    boxes.
    """

    def __init__(self, renderer: SceneRenderer) -> None:
        self.renderer = renderer
        self.mj_camera = renderer.cameras[DETECTOR_CAMERA]["mj_name"]
        self.error = None
        self.weights = DETECTOR_WEIGHTS
        if not self.weights.is_file():
            self.error = f"Missing detector weights: {self.weights}"
        self.conf = DETECTOR_CONF
        self.watchers = 0
        self.latest: dict | None = None
        self._lock = threading.Lock()

    @property
    def available(self) -> bool:
        return self.error is None

    def watch(self, delta: int) -> None:
        with self._lock:
            self.watchers += delta

    def run_forever(self) -> None:
        if SCAN_ENABLED:
            # The scan owns perception even when no client displays boxes.
            while not self.renderer.stop.is_set():
                scan = self.renderer.scan
                if scan:
                    self.error = scan.error
                    self.weights, self.conf = scan.weights, scan.conf
                    self.latest = scan.detections()
                time.sleep(0.1)
            return
        if not self.available:
            return
        worker = None
        try:
            worker = subprocess.Popen(
                [sys.executable, str(Path(__file__).with_name("yolo_worker.py")),
                 str(self.weights), str(self.conf), str(DETECTOR_THREADS)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            )
            last_seq = None
            while True:
                if worker.poll() is not None:
                    raise RuntimeError(f"YOLO worker exited ({worker.returncode})")
                if self.watchers == 0:
                    time.sleep(0.2)
                    continue
                frame, seq, generation = self.renderer.latest_rgb(self.mj_camera)
                if frame is None or (last_seq is not None and seq - last_seq < DETECTOR_FRAME_STRIDE):
                    time.sleep(0.01)
                    continue
                # Only this detector thread waits for the subprocess. There is
                # one frame in flight, no inference queue and no render lock.
                worker.stdin.write((json.dumps(frame.shape) + "\n").encode())
                worker.stdin.write(memoryview(frame).cast("B"))
                worker.stdin.flush()
                line = worker.stdout.readline()
                if not line:
                    raise RuntimeError("YOLO worker closed its output")
                result = json.loads(line)
                if generation != self.renderer.generation:
                    self.latest = None
                    continue
                if "error" in result:
                    raise RuntimeError(result["error"])
                self.latest = {
                    "generation": generation,
                    "camera": DETECTOR_CAMERA, "frame": seq,
                    "width": int(frame.shape[1]), "height": int(frame.shape[0]),
                    **result,
                }
                last_seq = seq
        except Exception as exc:  # noqa: BLE001
            self.error = f"detector failed: {exc!r}"
            self.latest = None
            print(f"[view] {self.error}", file=sys.stderr)
        finally:
            if worker is not None:
                worker.stdin.close()
                worker.stdout.close()
                if worker.poll() is None:
                    worker.terminate()
                worker.wait()


detector = Detector(scene)
threading.Thread(target=detector.run_forever, daemon=True).start()

# --- FastAPI app -----------------------------------------------------------

@asynccontextmanager
async def viewer_lifespan(app):
    yield
    scene.stop.set()
    await asyncio.to_thread(renderer_thread.join, 30)
    if scene.scan:
        await asyncio.to_thread(scene.scan.close)


app = FastAPI(title="Robot viewer backend", lifespan=viewer_lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/cameras")
def list_cameras():
    return [{"id": cam_id, "label": info["label"]} for cam_id, info in scene.cameras.items()]


pattern_lock = asyncio.Lock()
pattern_requests = {}


@app.post("/api/scene/randomize")
async def randomize_scene(session: str = Query(min_length=1, max_length=100),
                          scene_number: int | None = Query(default=None, alias="scene", ge=1, le=10)):
    """Choose once per page load, including React StrictMode and HTTP retries.

    With ?scene=N, load catalogue scene p01 through p10 by number
    instead of a random one."""
    if not SCAN_ENABLED:
        raise HTTPException(409, "Seeded layouts require the rail scene")
    async with pattern_lock:
        if session in pattern_requests:
            return pattern_requests[session]
        if scene_number is not None:
            choice = next((p for p in CATALOGUE if p['pattern'] == f'p{scene_number:02d}'), None)
            if choice is None:
                raise HTTPException(404, f"No catalogue scene {scene_number}")
        else:
            current = (scene.pattern or {}).get('pattern')
            choice = random.choice([p for p in CATALOGUE if p['pattern'] != current])
        model, info = await asyncio.to_thread(build_pattern, SCENE_PATH, choice['pattern'])
        finished = threading.Event()
        scene.pending_pattern = (model, info, finished)
        if not await asyncio.to_thread(finished.wait, 60):
            raise HTTPException(504, "Timed out loading the layout")
        if 'error' in info:
            raise HTTPException(500, info['error'])
        detector.latest = None
        pattern_requests[session] = info
        if len(pattern_requests) > 100:
            del pattern_requests[next(iter(pattern_requests))]
        return info


# --- Formula chat -------------------------------------------------------------


def scanned_shelf() -> list[dict]:
    """The flasks the live scan has named so far."""
    scan = scene.scan
    return shelf_from_tracks(scan.world.snapshot(), catalogue) if scan and scan.world else []


def scan_progress() -> str:
    scan = scene.scan
    if not SCAN_ENABLED or scan is None or scan.world is None:
        return " (The bench scan is not running.)"
    if scan.world.scan is None:
        return f" (The scan is still going: {len(scanned_shelf())} flasks named so far.)"
    return ""


chat = FormulaChat(catalogue, scanned_shelf, scan_progress)


def lab_state():
    """The scan's LabState publisher, which also holds the order; 409 without the scan."""
    lab = getattr(scene, "lab", None)
    if lab is None or scene.scan is None or scene.scan.world is None:
        raise HTTPException(409, "The bench scan is not running, so there is no robot to send it to.")
    return lab


def dispatch(formula: dict | None) -> dict:
    """Check a proposed formula against the bench as the scan knows it now, and send it."""
    if not formula:
        raise HTTPException(409, "There is no formula yet: type one, or paste its JSON.")
    lab = lab_state()
    lines = [{"compound": i.get("cas") or i.get("compound"), "grams": i.get("grams")}
             for i in formula.get("ingredients", [])]
    resolved = resolve(lines, scanned_shelf(), catalogue,
                       str(formula.get("id") or "CHAT"), str(formula.get("name") or "Chat formula"))
    try:
        order = lab.dispatch(resolved, str(formula.get("source") or "chat"))
    except RuntimeError as exc:
        raise HTTPException(409, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    if order.status == "rejected":
        # The bench cannot make it. Say which line and why, and ask for the
        # compound rather than quietly running the half of it that is there.
        problems = order.check["problems"]
        lines = "; ".join(f"{p['compound']}: {p['reason']}" for p in problems)
        missing = [p["compound"] for p in problems if p["compound"] != "—"]
        names = (" and ".join(missing) if len(missing) < 3
                 else f"{', '.join(missing[:-1])} and {missing[-1]}")
        ask = f" Restock {names} on the bench and I will run it." if missing else ""
        return {"order": order.id, "json": order.doc, "rejected": True,
                "problems": problems,
                "reply": f"I cannot make {resolved['name']}: {lines}.{ask}"}
    waiting = " It starts once the scan has finished." if scene.scan.world.scan is None else ""
    return {"order": order.id, "json": order.doc, "rejected": False,
            "reply": f"{order.id} sent to the robot: {resolved['name']}, "
                     f"{len(order.active_items())} ingredients.{waiting}"}


def with_json(answer: dict) -> dict:
    """Attach the formula as the robot will receive it, for the chat to show."""
    formula = answer.get("formula")
    lab = getattr(scene, "lab", None)
    if formula and lab is not None:
        answer["json"] = lab.workflow.formula_json(formula, formula.get("source", "chat"))
    return answer


@app.get("/api/formulation")
def formulation_info():
    lab = getattr(scene, "lab", None)
    order = lab.workflow.order if lab else None
    return {"available": SCAN_ENABLED, "chat": chat.mode, "bench": scanned_shelf(),
            "executor": lab.workflow.executor if lab else None,
            "order": order.id if order else None, "status": order.status if order else None}


# What the operator types is a brief, not a formula: "something fresh and
# citrusy for summer". The two exceptions are asking what is on the bench, and
# stopping a run — a question and a command, neither of them a brief.
BENCH_QUESTION = re.compile(r"\b(bench|mesa|shelf|what.?s there|qu[eé] hay)\b", re.I)
STOP_WORD = re.compile(r"^\s*(stop|para|detente|halt)\b", re.I)


@app.post("/api/chat")
def chat_message(payload: dict = Body(...)):
    """One chat message. A brief goes on the queue; a question is answered."""
    message = str(payload.get("message") or "").strip()
    if not message:
        raise HTTPException(400, "Empty message")
    if BENCH_QUESTION.search(message) and "?" in message:
        return {"reply": chat.reply(message)["reply"], "formula": None, "action": None}
    if not STOP_WORD.match(message):
        lab = lab_state()
        try:
            order = lab.workflow.submit_brief(message, "chat")
        except RuntimeError as exc:
            raise HTTPException(409, str(exc)) from exc
        lab._pump()
        if order.status == "rejected":
            why = "; ".join(p["reason"] for p in order.check["problems"])
            return {"reply": f"I could not compose that: {why}", "order": order.id,
                    "rejected": True, "problems": order.check["problems"], "action": None}
        if order.composed:
            got = order.composed
            return {"reply": f"{order.id}: {got['name']} — {got['family']}, "
                             f"{len(got['ingredients'])} compounds, {got['product']}. "
                             f"On the queue.",
                    "order": order.id, "rejected": False, "json": order.doc, "action": None}
        return {"reply": f"{order.id} is on the queue. It is composed on the bench "
                         f"once the scan has finished reading it.",
                "order": order.id, "rejected": False, "action": None}
    answer = chat.reply(message, payload.get("history") or [])
    if answer["action"] == "start":
        try:
            sent = dispatch(answer["formula"])
            if sent.get("rejected"):
                # Claude's proposal was fine; the bench is what cannot do it, so
                # the check's own words go through unchanged.
                answer.update(reply=sent["reply"], order=sent["order"], action=None,
                              rejected=True, problems=sent["problems"],
                              formula=None, json=sent["json"])
            else:
                # Claude's own words when it wrote some, with the order they started.
                reply = f"{answer['reply']} ({sent['order']})" if chat.mode == "claude" else sent["reply"]
                answer.update(reply=reply, order=sent["order"], formula=None, json=sent["json"])
        except HTTPException as exc:
            answer.update(reply=exc.detail, action=None, formula=None)
    elif answer["action"] == "stop":
        lab = getattr(scene, "lab", None)
        order = lab.workflow.order if lab else None
        if order is None or order.status not in ("queued", "running"):
            answer.update(reply="The robot has no order running.", action=None)
        else:
            lab.stop_order()
            answer["reply"] = f"{order.id} stopped; the arm finishes what it is holding."
    return with_json(answer)


@app.get("/api/formula")
def formula_current():
    """The current order as the executor reads it (also in simulation/out/formula_order.json)."""
    lab = lab_state()
    order = lab.workflow.order
    if order is None:
        raise HTTPException(404, "No formula has been sent to the robot yet.")
    return {**order.doc, "order": {**order.doc["order"], "status": order.status}}


@app.post("/api/formula")
def formula_submit(payload: dict = Body(...)):
    """Send a formula to the robot: {"formula": <proposal>} from the chat, or the formula JSON itself."""
    formula = payload.get("formula")
    if formula is None:
        answer = chat.reply(json.dumps(payload))
        if not answer.get("formula"):
            raise HTTPException(422, answer["reply"])
        formula = answer["formula"]
    return dispatch(formula)


@app.post("/api/formula/stop")
def formula_stop():
    lab = lab_state()
    order = lab.workflow.order
    if order is None or order.status not in ("queued", "running"):
        raise HTTPException(409, "The robot has no order running.")
    lab.stop_order()
    return {"reply": f"{order.id} stopped; the arm finishes what it is holding."}


@app.post("/api/workflow/report")
def workflow_report(payload: dict = Body(...)):
    """The executor crosses a step off: {"ingredient", "step", "status", "mass"?, "note"?}."""
    lab = lab_state()
    try:
        lab.workflow.report(payload.get("ingredient"), str(payload.get("step")), str(payload.get("status")),
                            payload.get("mass"), payload.get("note"))
    except KeyError as exc:
        raise HTTPException(409, str(exc.args[0] if exc.args else exc)) from exc
    return {"ok": True}


def mjpeg_generator(mj_camera_name: str):
    boundary = b"frame"
    for jpeg in scene.frames(mj_camera_name):
        yield (
            b"--" + boundary + b"\r\n"
            b"Content-Type: image/jpeg\r\n"
            b"Content-Length: " + str(len(jpeg)).encode() + b"\r\n\r\n" + jpeg + b"\r\n"
        )


@app.get("/stream/{camera_id}")
def stream(camera_id: str):
    if camera_id not in scene.cameras:
        return {"error": f"unknown camera '{camera_id}'"}
    mj_name = scene.cameras[camera_id]["mj_name"]
    return StreamingResponse(
        mjpeg_generator(mj_name),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@app.get("/api/info")
def viewer_info():
    """What this viewer is running: the models, the scene and the build.

    The Info panel shows it, so that what is on screen can always be traced to
    a model file and a commit.
    """
    lab = getattr(scene, "lab", None)
    scan = scene.scan
    return {
        "detector": {"backend": DETECTOR_SPEC, "weights": detector.weights.name or None,
                     "conf": detector.conf, "available": detector.available,
                     "error": detector.error, "camera": DETECTOR_CAMERA,
                     "input": f"{FRAME_WIDTH}x{FRAME_HEIGHT}"},
        "scan": {"enabled": SCAN_ENABLED,
                 "weights": Path(scan.weights).name if scan and scan.weights else None,
                 "conf": round(scan.conf, 2) if scan else None},
        "chat": {"mode": chat.mode, "model": CHAT_MODEL if chat.mode == "claude" else None},
        "executor": lab.workflow.executor if lab else None,
        "scene": {"file": SCENE_PATH.name, **(scene.pattern or {})},
        "state": f"ws://localhost:{STATE_PORT}/state",
        "build": COMMIT,
    }


@app.get("/api/detector")
def detector_info():
    return {
        "available": detector.available,
        "camera": DETECTOR_CAMERA,
        "weights": detector.weights.name,
        "conf": detector.conf,
        "pattern": scene.pattern,
        "error": detector.error,
    }


@app.get("/api/scan")
def scan_info():
    if not SCAN_ENABLED:
        return {"status": "disabled"}
    if scene.scan is None:
        return {"status": "starting", "caption": "Preparing the scan", "named": 0, "tracked": 0}
    return scene.scan.snapshot()


@app.websocket("/ws/replay-detections")
async def ws_replay_detections(websocket: WebSocket, pattern: str | None = None):
    """One requested future video frame at a time; never blocks live rendering."""
    await websocket.accept()
    worker = None
    try:
        # Replay uses the pinned model trained on Isaac renders (PWD and SMP).
        weights = REPLAY_WEIGHTS
        renders = REPO_ROOT / "view/frontend/public/renders"
        if pattern is None:
            video = renders / "rail_global.mp4"
        elif pattern in {f"p{i:02d}" for i in range(1, 11)}:
            video = renders / "seeds" / pattern / "rail_global.mp4"
        else:
            await websocket.send_json({"error": "Unknown replay pattern"})
            return
        if not weights.is_file() or not video.is_file():
            await websocket.send_json({"error": "Replay video or YOLO weights missing"})
            return
        worker = await asyncio.create_subprocess_exec(
            sys.executable, str(Path(__file__).with_name("replay_worker.py")),
            str(weights), str(video), stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
        )
        while True:
            line = await asyncio.wait_for(worker.stdout.readline(), timeout=60)
            if not line:
                raise RuntimeError("Replay detector stopped")
            result = json.loads(line)
            if result.get("ready"):
                result["pattern"] = pattern
            await websocket.send_json(result)
            request = await websocket.receive_json()
            worker.stdin.write((json.dumps({"time": float(request["time"])}) + "\n").encode())
            await worker.stdin.drain()
    except WebSocketDisconnect:
        pass
    except Exception as exc:
        try:
            await websocket.send_json({"error": str(exc)})
        except (RuntimeError, WebSocketDisconnect):
            pass
    finally:
        if worker is not None and worker.returncode is None:
            worker.terminate()
            try:
                await asyncio.wait_for(worker.wait(), timeout=3)
            except asyncio.TimeoutError:
                worker.kill()
                await worker.wait()
        try:
            await websocket.close()
        except RuntimeError:
            pass


@app.websocket("/ws/camera/{camera_id}")
async def ws_camera(websocket: WebSocket, camera_id: str, preview: bool = False):
    """Binary JPEG frames without occupying a browser's HTTP connection pool."""
    if camera_id not in scene.cameras:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    camera = scene.cameras[camera_id]["mj_name"]
    if not preview:
        scene.watch_main(camera, +1)
    async def send_frames():
        last = None
        while True:
            jpeg = scene.encoder.latest.get((camera, preview))
            if jpeg is not None and jpeg is not last:
                await websocket.send_bytes(jpeg)
                last = jpeg
            await asyncio.sleep(1 / (PREVIEW_FPS if preview else RENDER_FPS))
    sender = asyncio.create_task(send_frames())
    closed = asyncio.create_task(websocket.receive())
    try:
        done, _ = await asyncio.wait((sender, closed), return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            task.result()
    except WebSocketDisconnect:
        pass
    finally:
        sender.cancel()
        closed.cancel()
        await asyncio.gather(sender, closed, return_exceptions=True)
        if not preview:
            scene.watch_main(camera, -1)


@app.websocket("/ws/detections")
async def ws_detections(websocket: WebSocket):
    """Streams the detector's newest boxes; the detector runs while anyone listens."""
    await websocket.accept()
    detector.watch(+1)
    last_frame = None
    try:
        while True:
            latest = detector.latest
            if (latest is not None and latest["generation"] == scene.generation
                    and latest["frame"] != last_frame):
                await websocket.send_json(latest)
                last_frame = latest["frame"]
            await asyncio.sleep(0.05)
    except WebSocketDisconnect:
        pass
    finally:
        detector.watch(-1)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
