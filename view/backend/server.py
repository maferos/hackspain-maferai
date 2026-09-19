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
import os
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import cv2
import mujoco
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
from labbridge.mock_run import ACTIVE_BALANCE, RAIL, ScriptedRun  # noqa: E402
from labbridge.mujoco_adapter import vessels, workcell  # noqa: E402
from labbridge.server import StateServer  # noqa: E402

STATE_PORT = 8765
STATE_RATE_HZ = 10
STATE_LOOP_PAUSE_S = 15.0
# Rehearsal knobs: where the scripted run starts (seconds) and how fast it plays.
# LAB_STATE_START=100 LAB_STATE_SPEED=0.25 shows the recovery in slow motion.
STATE_START_S = float(os.environ.get("LAB_STATE_START", "0"))
STATE_SPEED = float(os.environ.get("LAB_STATE_SPEED", "1"))

# Logical camera id -> MuJoCo camera name in the scene. These are the vision
# system's own two cameras (see minihannover_scene.xml): `general`, the fixed
# room GoPro, and `wrist`, the mocap-mounted stand-in for the arm's future
# wrist camera. `hide_groups` lists geom groups to hide for that camera.
CAMERAS = {
    "robot": {"mj_name": "wrist", "label": "Robot camera (wrist)", "hide_groups": []},
    "scene": {"mj_name": "general", "label": "General camera", "hide_groups": []},
}

FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080
RENDER_FPS = 15
JPEG_QUALITY = 80

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

        self._scene_options: dict[str, mujoco.MjvOption] = {}
        for info in CAMERAS.values():
            opt = mujoco.MjvOption()
            mujoco.mjv_defaultOption(opt)
            for group in info["hide_groups"]:
                opt.geomgroup[group] = 0
            self._scene_options[info["mj_name"]] = opt

    def _encode(self, mj_camera_name: str, renderer: "mujoco.Renderer") -> bytes:
        with self._data_lock:
            renderer.update_scene(self.data, camera=mj_camera_name, scene_option=self._scene_options[mj_camera_name])
        frame = renderer.render()  # RGB
        bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ok, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
        if not ok:
            raise RuntimeError("JPEG encode failed")
        return buf.tobytes()

    def run_forever(self) -> None:
        renderer = mujoco.Renderer(self.model, height=FRAME_HEIGHT, width=FRAME_WIDTH)
        period = 1.0 / RENDER_FPS
        mj_camera_names = [info["mj_name"] for info in CAMERAS.values()]
        while True:
            start = time.time()
            with self._data_lock:
                mujoco.mj_step(self.model, self.data)
            with self._condition:
                for mj_name in mj_camera_names:
                    self._latest_jpeg[mj_name] = self._encode(mj_name, renderer)
                self._condition.notify_all()
            remaining = period - (time.time() - start)
            if remaining > 0:
                time.sleep(remaining)

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
    return [{"id": cam_id, "label": info["label"]} for cam_id, info in CAMERAS.items()]


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
    if camera_id not in CAMERAS:
        return {"error": f"unknown camera '{camera_id}'"}
    mj_name = CAMERAS[camera_id]["mj_name"]
    return StreamingResponse(
        mjpeg_generator(mj_name),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


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
