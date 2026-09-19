"""Backend for the robot viewer frontend.

Serves two MJPEG camera streams rendered live from the `minihannover_scene`
MuJoCo model (the onboard robot camera and the fixed scene-overview camera),
plus a websocket feed of a mock task log standing in for the robot's real
task planner (none exists in the repo yet).

It also publishes the full `LabState` that the lab state panels render, on
`ws://localhost:8765/state`, driven by the scripted
formulation of `labbridge.mock_run` on separate simulation data. The panel demo
never moves containers in the camera scene.

Usage:
    .venv/bin/python view/backend/server.py
Then open view/frontend (see its README) against this server's port (8000).
"""
from __future__ import annotations

import asyncio
import itertools
import json
import random
import subprocess
import os
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import mujoco
import numpy as np
from jpeg_encoder import JpegEncoder, PREVIEW_SIZE
from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from scene_patterns import CATALOGUE, build_pattern
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
# VIEW_SCENE picks the MuJoCo model to render: a bare name resolves under
# simulation/models/, or pass an absolute path. Defaults to the full bench.
# A scene without the scripted run's samples (e.g. minihannover_open_scene.xml)
# still streams live; only the LabState/task feed is skipped for it.
_scene_env = os.environ.get("VIEW_SCENE", "minihannover_scene.xml")
SCENE_PATH = Path(_scene_env)
if not SCENE_PATH.is_absolute():
    SCENE_PATH = REPO_ROOT / "simulation" / "models" / SCENE_PATH

sys.path.insert(0, str(REPO_ROOT / "dashboard" / "bridge"))
sys.path.insert(0, str(REPO_ROOT / "computer-vision"))
from labbridge.mock_run import ACTIVE_BALANCE, RAIL, ScriptedRun  # noqa: E402
from labbridge.mujoco_adapter import vessels, workcell  # noqa: E402
from labbridge.server import StateServer  # noqa: E402
from labvision.detector import resolve as resolve_detector

STATE_PORT = 8765
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

# Bottle detector on the general camera's live frames, run only while a client
# has the boxes on (see Detector). VIEW_DETECTOR is a labvision backend name or
# a weights path; the default `rail` is the YOLO26n trained on this camera in
# the rail scene, found as computer-vision/weights/yolo26n_rail_general.pt. The
# boxes are drawn raw, so they use that model's best-F1 threshold on the rail
# scene's validation frames, 0.47, not the backend's 0.10, which is set for
# propose_confirm's proposals. VIEW_DETECTOR_CONF overrides the threshold.
DETECTOR_SPEC = os.environ.get("VIEW_DETECTOR", "rail")
DETECTOR_CONF = float(os.environ.get("VIEW_DETECTOR_CONF", "0.47"))
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

# --- Mock task log --------------------------------------------------------
# Stands in for a real task/planner system (none exists in simulation/ yet).
TASK_SCRIPT = [
    "Locating amber bottle on the shelving",
    "Picking up bottle amber_loose_3",
    "Carrying bottle to balance 2",
    "Weighing sample on balance 2",
    "Reading the bottle's barcode",
    "Logging weight to inventory",
    "Returning bottle to the shelf",
    "Moving to the standby position",
]
TASK_DURATION_S = 3.5
MAX_TASK_LOG = 15


class TaskLog:
    """Cycles through TASK_SCRIPT, one task 'active' at a time, mock in real time."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._entries: list[dict] = []
        self._script = itertools.cycle(enumerate(TASK_SCRIPT))
        self._next_id = 0
        self._advance()

    def _advance(self) -> None:
        with self._lock:
            for entry in self._entries:
                if entry["status"] == "active":
                    entry["status"] = "done"
            _, label = next(self._script)
            self._next_id += 1
            self._entries.append(
                {
                    "id": self._next_id,
                    "label": label,
                    "status": "active",
                    "started_at": datetime.now(timezone.utc).isoformat(),
                }
            )
            if len(self._entries) > MAX_TASK_LOG:
                self._entries.pop(0)

    def snapshot(self) -> list[dict]:
        with self._lock:
            return [dict(e) for e in self._entries]

    def run_forever(self) -> None:
        while True:
            time.sleep(TASK_DURATION_S)
            self._advance()


task_log = TaskLog()
threading.Thread(target=task_log.run_forever, daemon=True).start()

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
        self._motion = self._build_rail_sweep()

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
        while True:
            start = time.monotonic()
            if self.pending_pattern is not None:
                model, info, finished = self.pending_pattern
                self.pending_pattern = None
                try:
                    new_context = mujoco.MjrContext(model, mujoco.mjtFontScale.mjFONTSCALE_150.value)
                    mujoco.mjr_setBuffer(mujoco.mjtFramebuffer.mjFB_OFFSCREEN, new_context)
                    new_scene = mujoco.MjvScene(model, maxgeom=10000)
                    with self._data_lock:
                        self.model = model
                        self.data = mujoco.MjData(model)
                        mujoco.mj_forward(model, self.data)
                        self._motion = self._build_rail_sweep()
                        self.pattern = info
                    context.free()
                    context, render_scene = new_context, new_scene
                    with self._condition:
                        self._latest_rgb.clear()
                        self.generation += 1
                    due = dict.fromkeys(names, 0.0)
                except Exception as exc:
                    info['error'] = str(exc)
                finally:
                    finished.set()
            with self._data_lock:
                if self._motion is not None:
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
        """Replays the scripted formulation and publishes LabState patches at STATE_RATE_HZ."""
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


scene = SceneRenderer(SCENE_PATH)
threading.Thread(target=scene.run_forever, daemon=True).start()
threading.Thread(target=scene.publish_state_forever, daemon=True).start()


class Detector:
    """Finds the bottles in the general camera's live frames while anyone watches.

    The model loads on first use and runs only while a /ws/detections client is
    connected, every DETECTOR_FRAME_STRIDE rendered frames, on the newest frame it has
    made; the boxes lag the picture by one inference, which the static bottles
    do not show. Without ultralytics or the weights, the viewer just offers no
    boxes.
    """

    def __init__(self, renderer: SceneRenderer, spec: str) -> None:
        self.renderer = renderer
        self.mj_camera = renderer.cameras[DETECTOR_CAMERA]["mj_name"]
        self.error = None
        try:
            path, _ = resolve_detector(spec)
        except FileNotFoundError as exc:
            path, self.error = "", str(exc)
        self.weights = Path(path)
        if self.error is None and not self.weights.exists():
            self.error = f"no weights at {path}"
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


detector = Detector(scene, DETECTOR_SPEC)
threading.Thread(target=detector.run_forever, daemon=True).start()

# --- FastAPI app -----------------------------------------------------------

app = FastAPI(title="Robot viewer backend")
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
async def randomize_scene(session: str = Query(min_length=1, max_length=100)):
    """Choose once per page load, including React StrictMode and HTTP retries."""
    if SCENE_PATH.name != "minihannover_rail_scene.xml":
        raise HTTPException(409, "Seeded layouts require the rail scene")
    async with pattern_lock:
        if session in pattern_requests:
            return pattern_requests[session]
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


@app.websocket("/ws/replay-detections")
async def ws_replay_detections(websocket: WebSocket, pattern: str | None = None):
    """One requested future video frame at a time; never blocks live rendering."""
    await websocket.accept()
    worker = None
    try:
        weights = Path(os.environ.get("VIEW_REPLAY_WEIGHTS", str(
            REPO_ROOT / "computer-vision/weights/yolo26n_rail_general.pt")))
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


@app.websocket("/ws/tasks")
async def ws_tasks(websocket: WebSocket):
    await websocket.accept()
    last_sent = None
    try:
        while True:
            current = task_log.snapshot()
            if current != last_sent:
                await websocket.send_json({"tasks": current})
                last_sent = current
            await asyncio.sleep(0.3)
    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
