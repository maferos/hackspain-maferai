# hackspain-maferai

Physics simulation with [MuJoCo](https://mujoco.readthedocs.io/en/stable/overview.html) and its interactive 3D viewer.

## Installation

Requires Python 3.10+ (Linux, macOS or Windows). The `mujoco` pip wheel ships the
native engine **and** the OpenGL viewer, so there is nothing else to download.

```bash
./install.sh                 # creates .venv, installs requirements.txt, runs a sanity check
source .venv/bin/activate
```

Manual alternative:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/check_install.py
```

On Debian/Ubuntu the viewer needs the OpenGL runtime: `sudo apt-get install -y libgl1 libegl1`.

## 3D visualizer

```bash
# Interactive viewer that runs the simulation from our script (launch_passive)
python scripts/view_model.py [models/hello.xml]

# Standalone viewer app (drag & drop any MJCF/URDF file onto the window)
python -m mujoco.viewer
python -m mujoco.viewer --mjcf=models/hello.xml
```

On macOS, run passive-viewer scripts with `mjpython` instead of `python`.

Viewer controls: double-click to select a body, Ctrl + right-drag to push it,
Space to pause, Backspace to reset, and the left/right panels toggle rendering options.

## AutoBio lab scenes

[AutoBio](https://github.com/autobio-bench/AutoBio) ([paper](https://arxiv.org/abs/2505.14030)) provides
MuJoCo models of a biology lab (centrifuges, pipettes, thermal cycler/mixer, tube racks, robot arms).
Its scenes need AutoBio's prebuilt plugin `libmjlab.so.3.3.0`, which only works with **MuJoCo 3.3.0**,
so they run in a separate environment (`.venv-autobio`, Python 3.11) from the main `.venv`.

```bash
./setup_autobio.sh     # clones AutoBio into third_party/AutoBio (git-ignored), creates .venv-autobio, checks all scenes
.venv-autobio/bin/python scripts/view_autobio.py --list                # available scenes
.venv-autobio/bin/python scripts/view_autobio.py pickup                # open a scene in the 3D viewer
.venv-autobio/bin/python scripts/view_autobio.py mani_thermal_cycler
```

`python -m mujoco.viewer` can't open most AutoBio scenes because it can't load the plugin first;
use `scripts/view_autobio.py` instead.

## Key MuJoCo concepts

- **MJCF**: MuJoCo's XML model format (see `models/hello.xml`).
- **`mjModel`**: the compiled, constant model description.
- **`mjData`**: the time-varying simulation state; `mujoco.mj_step(model, data)` advances it one timestep.

## Layout

| Path | Purpose |
| --- | --- |
| `requirements.txt` | Python dependencies (`mujoco`, `numpy`) |
| `install.sh` | One-shot environment setup + verification |
| `models/hello.xml` | Demo scene: floor + falling box, sphere, capsule |
| `scripts/check_install.py` | Headless check that loads and steps the model |
| `requirements-autobio.txt` | Pinned MuJoCo 3.3.0 env for AutoBio |
| `setup_autobio.sh` | Fetches AutoBio + creates `.venv-autobio` |
| `scripts/view_autobio.py` | Loads AutoBio's plugin and opens a lab scene in the viewer |
| `scripts/view_model.py` | Opens a model in the interactive viewer and simulates it in real time |
