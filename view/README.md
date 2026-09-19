# Robot viewer

Frontend to watch the mini-Hannover MuJoCo scene live: main viewport switchable
between the robot's onboard camera and the fixed scene-overview camera, a
picture-in-picture subwindow showing the other one (click it to swap), and a
right-hand panel with the robot's running task log, updated in real time.

- `backend/` — FastAPI server. Renders both cameras from
  `simulation/models/minihannover_scene.xml` live with `mujoco.Renderer` and
  serves them as MJPEG (`/stream/robot`, `/stream/scene`), plus a websocket
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
