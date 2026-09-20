# Mafer.ai at HackSpain 2026

Our entry for the Theker track: a robot that prepares fragrance formulas from
a bench of flasks. The operator types a formula into the viewer's chat, or a
brief such as "something fresh and citrusy for summer, light" that a model turns
into one. The robot scans the bench with a fixed camera, drives its wrist camera
over each flask to read the ArUco ring that names the sample, and checks the
formula against what it found: every compound has to be on the bench, in a
flask with enough left for the dose. It then picks each flask in turn while the
panels follow the order step by step, down to the mass on the balance pan. The
lab is a UR10e on a rail, simulated in MuJoCo; the demo also replays the same
scan rendered in Isaac Sim.

Presentation video: https://youtu.be/kdZ4qXKVD1E

Each part has its own README:

- [`simulation/`](simulation/) — robotic lab-automation simulation with MuJoCo + AutoBio. See [`simulation/README.md`](simulation/README.md).
- [`computer-vision/`](computer-vision/) — computer-vision pipeline: barcode identity, single-camera placement and the vessel detector. See [`computer-vision/README.md`](computer-vision/README.md); the detector choice and its benchmark are in [`computer-vision/docs/BENCHMARK.md`](computer-vision/docs/BENCHMARK.md).
- [`view/`](view/) — robot viewer for the live demo: Isaac Sim renders or live MuJoCo streams, plus task, robot and balance panels. See [`view/README.md`](view/README.md).
- [`dashboard/bridge/`](dashboard/bridge/) — `labbridge`, which publishes the lab state the viewer reads over WebSocket. See [`dashboard/bridge/README.md`](dashboard/bridge/README.md).

## Team

- Eki Gonzalez
- Nacho Gris
- Martí Martinez
- Eloi Torrents

## Requirements

- Python 3.10+ with [`uv`](https://docs.astral.sh/uv/); `simulation/install.sh` creates the venv the viewer backend also uses. The `mujoco` wheel ships the engine and viewer, but AutoBio needs its own MuJoCo 3.3.0 venv and only runs on Linux.
- Node for the viewer frontend (`npm install` in `view/frontend`).
- The MuJoCo Menagerie submodule for the UR10e and gripper meshes: `git submodule update --init third_party/mujoco_menagerie` from `simulation/`.
- The trained YOLO weights, which are not in git: copy them from the team Drive into `computer-vision/weights/` (see its README).
- A GPU is optional. CPU is enough for the simulation and the panels; detection and rendering are real time only with CUDA or MPS. The Isaac Sim replay videos were rendered on an NVIDIA L4 and are checked in.
- `ANTHROPIC_API_KEY` in `view/backend/.env` for the brief and formula chat; without it the chat falls back to an offline parser.
