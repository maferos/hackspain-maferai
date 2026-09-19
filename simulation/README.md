# simulation

Physics simulation with [MuJoCo](https://mujoco.readthedocs.io/en/stable/overview.html) and its interactive 3D viewer.

All commands below are run from this directory (`simulation/`).

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

## Lab furniture

`minihannover` is our own 6.0 x 1.5 m lab bench (work surface at 0.90 m), generated
for both simulators from a single script:

```bash
python scripts/generate_minihannover.py                       # regenerate the assets
python scripts/view_model.py models/minihannover_scene.xml    # look at it (perfumery lab around the bench, 14 x 5 x 3 m)
```

It ships as MJCF (boxes, and a mesh variant), URDF for the Isaac Lab importer, and an
OBJ interchange mesh. See [`assets/minihannover/README.md`](assets/minihannover/README.md).

The [open-desk variant](assets/minihannover_open/README.md) removes the central
shelving and centers a wider 6 × 2 m desk in the room:

```bash
python scripts/generate_minihannover_open.py
mjpython scripts/view_model.py models/minihannover_open_scene.xml  # macOS
```

## Robot arm on a rail

The open-desk scene gets a UR10e riding a 6 m linear rail over the bench. The arm
is [Menagerie's](https://github.com/google-deepmind/mujoco_menagerie) UR10e with a
Robotiq 2F-85 on the flange and an eye-in-hand camera beside it.

```bash
bash scripts/fetch_menagerie.sh              # UR10e + 2F-85 only, ~47 MB, gitignored
python scripts/generate_rail_scene.py        # writes the arm model and the scene
mjpython scripts/rail_demo.py --viewer       # watch it run the bench (macOS)
python scripts/rail_reach.py                 # what it can actually reach, in numbers
```

**Why a rail.** The UR10e reaches 1.30 m, the longest arm in Menagerie, and the
desk is 6 x 2 m. Bolted down it covers a 1.30 m disc; on a rail it covers the lot.
`scripts/rail_reach.py` solves top-down IK for the pinch point 20 mm over every
cap on the bench and counts:

| Mounting | Vessels reachable |
| --- | --- |
| Rail, free to stand anywhere along the travel | **93/93** |
| Rail, but the carriage must stand over the cap | 85/93 |
| Best single fixed station (scanned over the travel) | 52/93 |

The middle row is the arm's own inner dead zone rather than a reach limit: it
cannot fold onto a point directly under its shoulder, so the carriage stands off
along the rail --- 26 mm on average, 300 mm at worst --- and the misses vanish.

**Where the rail sits.** The beam runs along y = 0.30, the desk's back edge strip,
with its underside at 1.36 m: 60 mm over the two balances that stand there. The
`general` wall camera looks at the bench from -Y, so a gantry behind the glassware
shadows the back edge instead of the samples. The arm base ends up 0.55 m over the
worktop, roughly the height its own gripper works at, which is what keeps the full
1.30 m available horizontally instead of spending it on the drop to the bench.

**Motion.** `scripts/rail_demo.py --mode sweep` runs the carriage end to end in a
hand-down scan pose; `--mode visit` picks vessels along the bench and drops the
gripper over each cap in turn. Playback is kinematic by default so it is
deterministic and cannot knock the glassware over; `--physics` drives the position
actuators and steps the simulator instead, where the arm sags up to 4 degrees at
the shoulder under Menagerie's stock gains. Render with `--video out/rail.mp4`
(needs `ffmpeg`) or `--frames <dir>`, from `--camera general`, `carriage` or `eih`.

## AutoBio lab scenes

[AutoBio](https://github.com/autobio-bench/AutoBio) ([paper](https://arxiv.org/abs/2505.14030)) provides
MuJoCo models of a biology lab (centrifuges, pipettes, thermal cycler/mixer, tube racks, robot arms).
Its scenes need AutoBio's prebuilt plugin `libmjlab.so.3.3.0`, which only works with **MuJoCo 3.3.0**,
AutoBio is included as a git submodule (it has no license file, so its assets are referenced rather than copied), and its scenes run in a separate environment (`.venv-autobio`, Python 3.11) from the main `.venv`.

> **Platform note:** the shipped plugin is a Linux `.so`; it does not load on macOS. Run the AutoBio scenes on Linux (or in a container / cloud GPU box).

```bash
./setup_autobio.sh     # fetches the AutoBio submodule (third_party/AutoBio), creates .venv-autobio, checks all scenes
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
| `models/minihannover_scene.xml` | Demo scene: a perfumery lab (14 x 5 x 3 m) around the `minihannover` bench: a shelving library of 187 barcoded sample bottles, one sink, five balances, GC-MS and UV-Vis-NIR, and thirteen hand-placed barcoded sample bottles, powders and liquids mixed: six in the entrance corner, seven loose and movable on the bench. Nothing is sorted, on purpose: where a bottle stands says nothing about what it is. Two cameras belong to the vision system, both a GoPro in Linear mode at 1080p (`fovy` 60.44, `resolution` 1920 x 1080): `general`, fixed on the right wall at ceiling height at (-1.5, -2.9, 3), which is (7, 0, 3) in `computer-vision`'s room frame, and `wrist`, on a mocap body 0.30 m in front of a bottle on the bench, standing in for the arm's wrist camera |
| `scripts/fetch_menagerie.sh` | Sparse-fetches the UR10e and Robotiq 2F-85 from MuJoCo Menagerie into `third_party/` |
| `scripts/generate_rail_scene.py` | Builds `assets/ur10e_2f85/` and `models/minihannover_rail_scene.xml` (open desk + gantry + arm) |
| `scripts/rail_kinematics.py` | Bench-vessel lookup and top-down damped-least-squares IK, shared by the two rail scripts |
| `scripts/rail_demo.py` | Drives the carriage along the rail: sweep or per-vessel visit, viewer or offscreen render |
| `scripts/rail_reach.py` | Reachability report: rail vs one fixed station, over every vessel on the bench |
| `models/minihannover_rail_scene.xml` | The open-desk scene plus a 6 m gantry carrying a UR10e + Robotiq 2F-85 with an eye-in-hand camera |
| `scripts/check_install.py` | Headless check that loads and steps the model |
| `requirements-autobio.txt` | Pinned MuJoCo 3.3.0 env for AutoBio |
| `third_party/AutoBio` | AutoBio git submodule (models, meshes, plugin) |
| `setup_autobio.sh` | Fetches the AutoBio submodule + creates `.venv-autobio` |
| `scripts/view_autobio.py` | Loads AutoBio's plugin and opens a lab scene in the viewer |
| `scripts/view_model.py` | Opens a model in the interactive viewer and simulates it in real time |
| `assets/sink/` | Lab sink for MuJoCo (converted OBJ meshes + MJCF + vendor .3ds) |
| `assets/balance/` | Analytical balance for MuJoCo (converted OBJ meshes + MJCF) |
| `assets/lab_room/` | The perfumery-lab room (generated by `scripts/generate_lab_room.py`) |
| `assets/gc_ms/`, `assets/uv_vis_nir/` | The two instruments, converted for MuJoCo |
| `assets/labelled_bottles/` | All 200 catalogued samples as MuJoCo bodies, each bottle carrying a ring of eight ArUco markers as a texture (`marker_id` in the lookup table; it was an EAN-13 label before) (built by `tools/build_labelled_bottles.py`). These are what the scene uses |
| `assets/amber_bottles/`, `assets/reagent_jars/`, `assets/agro_bottles/` | Bottle / jar kits from `../assets/`, converted for MuJoCo without labels. No longer placed in the scene |
| `scripts/generate_lab_room.py` | Generates the lab room around the bench |
| `tools/convert_glb.py` | Converts a glTF binary (.glb) model into MuJoCo meshes + MJCF |
| `tools/convert_dae.py` | Converts a COLLADA (.dae) model into MuJoCo meshes + MJCF |
| `tools/convert_3ds.py` | Converts a .3ds model (instances, mirrors) into MuJoCo meshes + MJCF |
| `assets/minihannover/` | `minihannover` lab bench: MJCF + URDF + OBJ (generated) |
| `scripts/generate_minihannover.py` | Single source of truth for the `minihannover` assets |
| `assets/README.md` | Which assets each simulator can consume, and their gotchas |
| `assets/gc-ms/`, `assets/uv-vs-nr/` | Raw vendor 3D models of the instruments (sources of `gc_ms/`, `uv_vis_nir/`) |
