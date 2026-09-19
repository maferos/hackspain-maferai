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
