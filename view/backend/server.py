"""Backend for the robot viewer frontend.

Serves two MJPEG camera streams rendered live from the `minihannover_scene`
MuJoCo model (the onboard robot camera and the fixed scene-overview camera),
plus a websocket feed of a mock task log standing in for the robot's real
task planner (none exists in the repo yet).

It also publishes the full `LabState` that the lab state panels render, on
`ws://localhost:8765/state`, driven by the scripted
formulation of `labbridge.mock_run` over this same scene. The script moves the
free containers kinematically, so the camera streams show it too.

Usage:
    .venv/bin/python view/backend/server.py
Then open view/frontend (see its README) against this server's port (8000).
"""
from __future__ import annotations

import asyncio
import itertools
import json
import subprocess
import os
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import cv2
import mujoco
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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
    Instead this thread renders into `_latest_jpeg` and HTTP handlers (on
    whatever thread) just read the latest cached bytes.
    """

    def __init__(self, xml_path: Path) -> None:
        self.model = mujoco.MjModel.from_xml_path(str(xml_path))
        self.data = mujoco.MjData(self.model)
        mujoco.mj_forward(self.model, self.data)
        self._latest_jpeg: dict[str, bytes] = {}
        # The RGB behind each camera's latest JPEG, for the detector.
        self._latest_rgb: dict[str, np.ndarray] = {}
        self._frame_seq = 0
        self._condition = threading.Condition()
        # Guards `data` between the physics/render thread and the state thread.
        self._data_lock = threading.Lock()

        # Scripted formulation that drives the dashboard's LabState and moves
        # the free containers; the console reads it on ws://:STATE_PORT/state.
        # A scene without the scripted run's samples (e.g. the open lab) still
        # renders its camera streams; only the LabState feed is skipped.
        try:
            self.run = ScriptedRun(self.model, self.data, vessels(self.model))
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

    def _encode(self, mj_camera_name: str, renderer: "mujoco.Renderer") -> tuple[bytes, np.ndarray]:
        with self._data_lock:
            renderer.update_scene(self.data, camera=mj_camera_name, scene_option=self._scene_options[mj_camera_name])
        frame = renderer.render()  # RGB
        bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ok, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
        if not ok:
            raise RuntimeError("JPEG encode failed")
        return buf.tobytes(), frame

    def run_forever(self) -> None:
        renderer = mujoco.Renderer(self.model, height=FRAME_HEIGHT, width=FRAME_WIDTH)
        period = 1.0 / RENDER_FPS
        mj_camera_names = [info["mj_name"] for info in self.cameras.values()]
        while True:
            start = time.time()
            with self._data_lock:
                if self._motion is not None:
                    self._advance_motion()
                else:
                    mujoco.mj_step(self.model, self.data)
            rendered = {name: self._encode(name, renderer) for name in mj_camera_names}
            with self._condition:
                for name, (jpeg, rgb) in rendered.items():
                    self._latest_jpeg[name] = jpeg
                    self._latest_rgb[name] = rgb
                self._frame_seq += 1
                self._condition.notify_all()
            remaining = period - (time.time() - start)
            if remaining > 0:
                time.sleep(remaining)

    def latest_rgb(self, mj_camera_name: str) -> tuple[np.ndarray | None, int]:
        """The camera's newest rendered RGB frame and the render loop's frame count."""
        with self._condition:
            return self._latest_rgb.get(mj_camera_name), self._frame_seq

    def frames(self, mj_camera_name: str):
        """Yields each newly rendered JPEG for the given camera, blocking between them."""
        last = None
        while True:
            with self._condition:
                self._condition.wait_for(lambda: self._latest_jpeg.get(mj_camera_name) is not last)
                last = self._latest_jpeg[mj_camera_name]
            yield last

    def _snapshot_state(self) -> None:
        with self._data_lock:
            self.state_server.snapshot(self.run.initial_state(workcell(self.model, self.data, ACTIVE_BALANCE, RAIL)))

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
            with self._data_lock:
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
                frame, seq = self.renderer.latest_rgb(self.mj_camera)
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
                if "error" in result:
                    raise RuntimeError(result["error"])
                self.latest = {
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
        "error": detector.error,
    }


@app.websocket("/ws/camera/{camera_id}")
async def ws_camera(websocket: WebSocket, camera_id: str):
    """Binary JPEG frames without occupying a browser's HTTP connection pool."""
    if camera_id not in scene.cameras:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    camera = scene.cameras[camera_id]["mj_name"]
    last = None
    try:
        while True:
            # Immutable bytes are published by one render thread. Do not take
            # its lock here: rendering holds it across GL work, which would
            # block FastAPI's event loop and all other camera connections.
            jpeg = scene._latest_jpeg.get(camera)
            if jpeg is not None and jpeg is not last:
                await websocket.send_bytes(jpeg)
                last = jpeg
            await asyncio.sleep(1 / RENDER_FPS)
    except WebSocketDisconnect:
        pass


@app.websocket("/ws/detections")
async def ws_detections(websocket: WebSocket):
    """Streams the detector's newest boxes; the detector runs while anyone listens."""
    await websocket.accept()
    detector.watch(+1)
    last_frame = None
    try:
        while True:
            latest = detector.latest
            if latest is not None and latest["frame"] != last_frame:
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
