# Simulation

Physics simulation with [MuJoCo](https://mujoco.readthedocs.io/en/stable/overview.html) and its interactive 3D viewer.
All commands below are run from this `simulation/` folder (`cd simulation`).

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
AutoBio is included as a git submodule (it has no license file, so its assets are referenced rather than copied), and its scenes run in a separate environment (`.venv-autobio`, Python 3.11) from the main `.venv`.

```bash
./setup_autobio.sh     # fetches the AutoBio submodule (third_party/AutoBio), creates .venv-autobio, checks all scenes
.venv-autobio/bin/python scripts/view_autobio.py --list                # available scenes
.venv-autobio/bin/python scripts/view_autobio.py                       # our lab scene (autobio_lab)
.venv-autobio/bin/python scripts/view_autobio.py pickup                # any AutoBio scene
.venv-autobio/bin/python scripts/view_autobio.py mani_thermal_cycler
```

### Lab scene with our instruments

`models/autobio_lab.xml` (the viewer's default scene) is AutoBio's *pick up centrifuge tube* setup
(ALOHA arm, tube rack, 50 ml screw tube) on a 5.0 m x 1.4 m table (`models/big_table.xml`).
The robot arm is in the middle, flanked by the **GC-MS** (`../assets/gc-ms`) on one side and the
**UV-Vis-NIR spectrophotometer** (`../assets/uv-vis-nir`) on the other.

At each end of the table there is an orange circular **spawn zone**. While the viewer runs,
`scripts/spawner.py` sends a lab worker (`models/human_figure.xml`) walking up to one zone at a time
(alternating), and the worker drops a 50 ml tube into the circle before walking away. The default is
one spawn every 3 s of sim time; change it with
`.venv-autobio/bin/python scripts/view_autobio.py --interval 1.5`.
MuJoCo can't add bodies to a running model, so the scene holds a fixed pool (one mocap worker per
zone and 10 tubes parked off-stage at x = 20 m). Tubes are reused oldest-first once all 10 are on the
table. `--check` also runs the spawner and fails if a dropped tube misses the table.

The instruments were converted from the OBJ files in the repo's top-level `assets/` with `tools/convert_instrument.py`,
which splits them into one mesh per material, turns them Z-up, scales them to metres and adds a box
collider. To regenerate (or add another instrument):

```bash
unzip ../assets/uv-vis-nir/3d-model.obj.zip -d /tmp/uv && unzip ../assets/uv-vis-nir/3d-model.mtl.zip -d /tmp/uv
.venv-autobio/bin/python tools/convert_instrument.py /tmp/uv/3d-model.obj --name uv_vis_nir --scale 0.0254   # inches
# gc-ms: --name gc_ms --scale 0.0000314  (source units are arbitrary; this makes it ~1.0 m wide)
```

`python -m mujoco.viewer` can't open most AutoBio scenes because it can't load the plugin first;
use `scripts/view_autobio.py` instead.

## Key MuJoCo concepts

- **MJCF**: MuJoCo's XML model format (see `models/hello.xml`).
- **`mjModel`**: the compiled, constant model description.
- **`mjData`**: the time-varying simulation state; `mujoco.mj_step(model, data)` advances it one timestep.

## Layout

Paths are relative to `simulation/`.

| Path | Purpose |
| --- | --- |
| `requirements.txt` | Python dependencies (`mujoco`, `numpy`) |
| `install.sh` | One-shot environment setup + verification |
| `models/hello.xml` | Demo scene: floor + falling box, sphere, capsule |
| `scripts/check_install.py` | Headless check that loads and steps the model |
| `requirements-autobio.txt` | Pinned MuJoCo 3.3.0 env for AutoBio |
| `third_party/AutoBio` | AutoBio git submodule (models, meshes, plugin) |
| `setup_autobio.sh` | Fetches the AutoBio submodule + creates `.venv-autobio` |
| `scripts/view_autobio.py` | Loads AutoBio's plugin and opens a lab scene in the viewer |
| `models/autobio_lab.xml` | AutoBio pickup scene + GC-MS + UV-Vis-NIR + spawn zones on a big table |
| `models/big_table.xml` | 5.0 m x 1.4 m version of AutoBio's table |
| `models/human_figure.xml` | Stick-figure lab worker used by the spawner |
| `scripts/spawner.py` | Walks workers to the spawn zones and drops tubes |
| `models/instruments/` | MuJoCo meshes generated from `../assets/` |
| `tools/convert_instrument.py` | OBJ/MTL -> MuJoCo mesh + MJCF converter |
| `scripts/view_model.py` | Opens a model in the interactive viewer and simulates it in real time |
