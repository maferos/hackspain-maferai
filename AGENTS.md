# hackspain-maferai

Hackathon project. Two components:

- `simulation/` — **Eki**, **Eloi**
- `computer-vision/` — **Nacho**, **Martí**
- `view/` — robot viewer for the demo (React + Vite frontend, FastAPI backend), see its README
- `dashboard/bridge/` — `labbridge`, publishes the lab state the viewer's panels read

## Team

Four people, split into two pairs:

| Component         | People       |
| ----------------- | ------------ |
| Simulation        | Eki, Eloi    |
| Computer Vision   | Nacho, Martí |

### Simulation ownership

| Who  | Platform | Focus                                                                                          |
| ---- | -------- | ---------------------------------------------------------------------------------------------- |
| Eki  | Linux    | MuJoCo + AutoBio (`simulation/`); AutoBio is Linux-only                                         |
| Eloi | macOS    | IsaacLab-mlx — the Apple Silicon (MLX/Metal) port of Isaac Lab (external repo, `../IsaacLab-mlx`) |

## Conventions

- Everything in this repo is written in English.

## One dashboard

The demo has exactly one dashboard: `view/` (frontend in `view/frontend`,
backend in `view/backend`). Do not start a second frontend, copy the viewer
into another folder or keep a private variant: parallel versions drift apart
and each teammate ends up showing something different.

- Change `view/` in place, in small commits, and pull before you start
  (`git pull origin main`).
- The camera viewport is Eloi's; the panels (Balance, Robot tasks and Pipeline
  in the dock under it, Formula down the right) are Martí's. The Real time /
  Replay switch only picks the viewport's source; the panels always read the
  lab state.
- The side panels read the lab state on `ws://localhost:8765/state`
  (`dashboard/bridge/labbridge`). Without a publisher they play the recorded
  scripted run in `view/frontend/public/scripted-run.json`, so everyone sees
  the same panels with only `npm run dev`.
- When the scene's samples or the scripted run change, update `RECIPE` in
  `dashboard/bridge/labbridge/mock_run.py` and regenerate the recording with
  `python -m labbridge.record_run` from `dashboard/bridge`.
