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
Robotiq 2F-85 on the flange and an eye-in-hand camera beside it. Menagerie is a git
submodule at `third_party/mujoco_menagerie`; init it once (below), or run
`git clone --recursive` when first cloning the repo.

```bash
git submodule update --init third_party/mujoco_menagerie  # UR10e + 2F-85 meshes (shallow submodule)
python scripts/generate_rail_scene.py        # writes the arm model and the scene
mjpython scripts/rail_demo.py --viewer       # watch it run the bench (macOS)
python scripts/rail_reach.py                 # what it can actually reach, in numbers
```

**Why a rail.** The UR10e reaches 1.30 m, the longest arm in Menagerie, and the
desk is 6 x 2 m. Bolted down it covers a 1.30 m disc; on a rail it covers the lot.
`scripts/rail_reach.py` solves top-down IK for the pinch point 20 mm over every
cap on the bench and counts. The table below was taken over the **full** bench
population, which is the interesting case; the scene as shipped is thinned to
`BENCH_VESSELS` and scores 12/12 trivially. Raise that constant to reproduce it:

| Mounting | Vessels reachable |
| --- | --- |
| Rail, free to stand anywhere along the travel | **187/187** (100%) |
| Rail, but the carriage must stand over the cap | 174/187 (93%) |
| Best single fixed station (scanned over the travel) | 98/187 (52%) |

The middle row is the arm's own inner dead zone rather than a reach limit: it
cannot fold onto a point directly under its shoulder, so the carriage stands off
along the rail --- 21 mm on average, 300 mm at worst --- and the misses vanish.
Run `scripts/rail_reach.py` after any change to the bench population: the
counts move with it, the proportions have not.

**Where the rail sits.** The beam runs along y = 0.30, the desk's back edge strip,
with its underside at 1.36 m: 60 mm over the two balances that stand there. The
`general` wall camera looks at the bench from -Y, so a gantry behind the glassware
shadows the back edge instead of the samples. The arm base ends up 0.55 m over the
worktop, roughly the height its own gripper works at, which is what keeps the full
1.30 m available horizontally instead of spending it on the drop to the bench.

### Wrist camera, live

The arm carries an eye-in-hand camera 90 mm to the side of the tool axis and
30 mm under the flange --- on the wrist, just below it. It is a real object in
the scene, not a bare viewpoint: `scripts/generate_wrist_camera.py` builds a
compact GigE machine-vision camera (Basler ace class body, 29 x 29 x 42 mm, C-mount
lens, heat-sink ribs, connectors and cable) on a steel L-bracket bolted to an
adapter plate at the UR10e's 90 mm tool flange, and `generate_rail_scene.py`
attaches it at exactly the pose the MJCF camera has. So the overview shows the
hardware the pictures come from. `scripts/wrist_view.py`
opens the interactive MuJoCo window and streams that camera to a browser tab at
the same time, so the room and the robot's own view sit side by side:

```bash
.venv/bin/mjpython scripts/wrist_view.py                 # sweep the bench
.venv/bin/mjpython scripts/wrist_view.py --mode label    # read one label after another
```

The tab opens by itself at `http://localhost:8008`; the stream is multipart
JPEG off the standard library's HTTP server, so nothing extra is installed. The
MuJoCo window stays interactive throughout, and `[` / `]` cycles its own camera
if you would rather have the wrist view large and the room small.

**The model's origin is the front face of its lens.** Every part of the camera
sits behind that, so none of it can appear in its own picture --- a camera that
sees its own lens hood shows a black crescent on every frame. It is an easy thing
to break by nudging a mount offset, so `generate_rail_scene.py` compiles the scene
and asserts the clearance on every run, and prints it:
`camera: modelled body clears its own lens by 1.0 mm`.

**The camera looks parallel to the tool axis, not converging on it.** That is
deliberate and was a bug first: the gripper sits on the tool axis, so a camera
that converges there aims straight at the back of its own fingers. Parallel puts
the gripper at the frame edge and whatever the camera is aimed at in the middle.

**Reading a label is an aiming problem, not an angle problem.**
`computer-vision/scripts/wrist_scan.py` wants about 0.30 m of standoff and no
more than ~25 degrees of elevation, because the ArUco bars are rings round the
bottle and from above a ring is an arc. But 93 vessels stand about 9 mm apart on
this bench, so a neighbour is usually in the way. Casting a ray at every label
and counting what the camera can actually see:

| Camera elevation | Approaching every vessel from the rail side | Choosing the bearing per vessel |
| --- | --- | --- |
| 8 degrees | 139/187 (74%) | **187/187** |
| 25 degrees | 167/187 (89%) | 187/187 |
| 45 degrees | 178/187 (95%) | 187/187 |

Coming at a vessel from the right side beats climbing above it. `--mode label`
does exactly that: it tries bearings in turn, skips the ones a neighbour blocks,
and takes the first the arm can hold, at the 8 degrees the reader prefers.

Those figures are for the full bench too. On the thinned scene every label is
visible from every bearing, because there is nothing left to hide behind --- so
do not read the shipped scene as evidence the problem went away.

The population is regenerated upstream and has changed size twice already, so
take the proportions rather than the counts. One thing to know if the unbarcoded
reserve stock comes back: the vessel lookup used to match sample ids with
`[A-Za-z0-9-]+`, which does not match `reserve_000`, and silently measured only
the catalogued samples. The blockers were always all present, so the proportions
held, but the counts were quietly halved. It anchors on the part suffix now.

**Motion.** `scripts/rail_demo.py --mode sweep` runs the carriage end to end in a
hand-down scan pose; `--mode visit` picks vessels along the bench and drops the
gripper over each cap in turn. Playback is kinematic by default so it is
deterministic and cannot knock the glassware over; `--mode label` parks the wrist
camera on one label after another; `--physics` drives the position
actuators and steps the simulator instead, where the arm sags up to 4 degrees at
the shoulder under Menagerie's stock gains. Render with `--video out/rail.mp4`
(needs `ffmpeg`) or `--frames <dir>`, from `--camera general`, `carriage` or `eih`.

### Physics, and picking things up

The demo modes above play back kinematically: poses are written straight to
`qpos` and `mj_forward` resolves them, so MuJoCo detects contacts and does
nothing with them --- the arm passes through the bench. That is deliberate for a
demo that must not knock the glassware over, and useless for manipulation.

`scripts/wrist_view.py --mode pick` is the other thing: every motion goes
through the position actuators, `mj_step` runs the whole way, the arm is stopped
by the bench, vessels it brushes move, and the gripper closes on force feedback.

**The bench is cleared down to `BENCH_VESSELS` (12), all of them liftable.**
The open scene the computer-vision work renders from keeps its full population;
`generate_rail_scene.py` thins the copy the rail scene loads so the manipulation
case is simple to watch and to debug. Raising that constant is how to make the
task harder --- more clutter to reach through, less room for the fingers --- and
each vessel costs 7 qpos and a pile of contacts. Twelve run at about 11x
realtime, and they sit 278 to 453 mm apart.

**The gripper can feel what it holds.** Menagerie's 2F-85 already behaves like
the real one when it closes on something --- the actuator is a position servo on
a tendon with `forcerange="-5 5"`, so the pads stall against the object and keep
squeezing at the limit instead of crushing through. What the scene had no way of
doing was *reporting* it: `nsensor` was 0. `generate_rail_scene.py` now writes a
sensed copy of the gripper carrying the three things the real 2F-85 publishes
over Modbus:

| Sensor | What it gives |
| --- | --- |
| `arm_grip_{right,left}_pad_force` | normal force on each pad |
| `arm_grip_finger_drive` | what the finger servo is putting out |
| `arm_grip_{right,left}_finger` | how far the fingers actually closed |

`rk.read_grip()` turns those into the 2F-85's own object-detected condition:
**fingers stalled short of shut, with force on both pads**. Watch
`finger_drive` during a grasp and it sits at exactly 5.0, the forcerange limit.

`scripts/grasp_test.py` drives the whole approach-close-lift sequence with
physics and scores it:

```
gripper reported an object: 12/12
picked up and still held:   12/12
sensor agreed with reality: 12/12
```

The agreement is the useful column: the gripper's own senses say the same thing
as the vessel's true height, which the test used to peek at and a real cell
cannot see. On the full bench it scores 7 in 10, and those failures are approach
rather than grip --- two closed on thin air and one wedged its pads on two
neighbouring vessels at 600 N, which is the arm shoving, not the gripper
gripping.

Three things that cost time and are easy to hit again:

* **`solve_ik` writes its iterates into `qpos`.** Harmless in a test that resets
  afterwards; in a live loop the arm teleports to the solution and drags
  whatever it was touching. Save and restore around the call.
* **A mesh geom's `xpos` is the mesh's centre, not its authored origin.** The
  compiler re-centres mesh vertices and records the shift in `mesh_pos`. Lifting
  a vessel out of the room without undoing that shift floats it 25 to 47 mm.
* **The pads press on each other at full close** and register a few newtons of
  their own, so "force on the pads" alone reports a hold on nothing. The
  closure threshold has to sit well short of the stop.
* **Damped least squares solves whichever branch its seed is nearest.** Two
  poses 120 mm apart, solved from the same fixed seed, came back in branches the
  servos could not travel between: the arm ended 555 mm from where it was told
  to go and the gripper closed on air. `solve_any` seeds from the arm's current
  pose first now, which took the grasp score from 11 in 12 to 12 in 12.

### Pipetting

`wrist_view.py --mode pipette` draws liquid from the open flasks on the bench
and delivers it into a beaker, with physics running throughout.

```bash
python scripts/generate_rail_scene.py     # TOOL = 'pipette' builds this scene
python scripts/pipette_test.py            # the whole cycle on every flask
mjpython scripts/wrist_view.py --mode pipette
```

The arm carries a **pipette on the flange instead of the gripper**: a
single-channel micropipette with a fixed 125 mm tip, generated by
`scripts/generate_pipette.py`. `TOOL = 'gripper'` in `generate_rail_scene.py`
puts the Robotiq back and `grasp_test.py` works again; the tool centre point
follows whichever is fitted, so the IK and the reach report do not change.

The flasks are **open and part filled**. `scripts/generate_open_vessels.py`
writes a copy of each catalogue vessel with the cap geom deleted, a liquid
column inside, and a site at the mouth. Fill levels are a seeded fraction of
each vessel's catalogued capacity, clamped to what it geometrically holds, so a
10 ml flask never contains 40 ml.

**The liquid is a level and a number, not a fluid.** MuJoCo has no fluid solver,
and hundreds of spheres per flask would be slow, unstable and ugly at this
scale. What is *not* faked is whether the pipette may draw: aspirating needs the
tip down the bore and under the surface, checked against the running simulation,
so a bad approach fails the way it would on a bench.

```
12 open flasks holding 250.8 ml between them; tip radius 2.7 mm
transferred: 12/12
beaker now holds 6.08 ml = 5.53 g at 0.91 g/ml
the balance reads 5.5341 g
tip alignment: 1.1 mm mean, 1.5 mm worst
```

**The flasks are hollow for collision, not just for looks.** MuJoCo collides a
mesh as its convex hull, so the glass was a solid slug and a tip could only be
put inside it by excluding the contact. Each vessel now carries three rings of
overlapping boxes --- body, shoulder and neck --- plus a base disc, so the
outside is still solid and the bore is genuinely open. A tip 12 mm off the axis
strikes the glass; 8 mm goes down the bore. It costs about 37 collision geoms
per vessel and the scene still runs at 12.8x realtime.

**The beaker stands on a balance, and the balance reads out.**
`scripts/generate_open_balance.py` trims every mesh of the balance above
200 mm, throwing away the draft shield's roof, and replaces the single
collision box with a housing, a weighing pan and four shield walls. It also
throws away `part_04` --- the moulded "0.0000", which is extruded geometry and
not a texture, because this model has no textures at all --- and builds five
seven-segment digits in the plane of the original display. `pipetting.show_mass`
switches the segments by writing `geom_rgba`, which both the interactive viewer
and the offscreen renderer read every frame, so the number climbs as the
pipette delivers. Over 9.9999 g it reads dashes, the way a real balance shows
an over-range. That balance is also moved out in front of the rail: left where
it stood on the back strip, the beaker's rim sat at 1.08 m, which put the
pipette's flange at 1.34 --- 20 mm under the gantry beam with the whole wrist
in the way.

One regression worth knowing: with the flasks hollow, `grasp_test.py` scores 11
of 12 rather than 12. The staves give the pads a slightly different surface
than a smooth convex hull, and one grasp is now marginal. The gripper's own
sensors still agree with reality on all twelve.

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
| `third_party/mujoco_menagerie` | MuJoCo Menagerie git submodule (shallow); provides the UR10e + Robotiq 2F-85 meshes the rail scene needs |
| `scripts/fetch_menagerie.sh` | Optional: sparse-fetches only the UR10e and Robotiq 2F-85 (~47 MB) in place of the full submodule checkout |
| `scripts/generate_rail_scene.py` | Builds `assets/ur10e_2f85/` and `models/minihannover_rail_scene.xml` (open desk + gantry + arm) |
| `scripts/rail_kinematics.py` | Bench-vessel lookup and top-down damped-least-squares IK, shared by the two rail scripts |
| `scripts/rail_demo.py` | Drives the carriage along the rail: sweep or per-vessel visit, viewer or offscreen render |
| `scripts/generate_wrist_camera.py` | Builds `assets/wrist_camera/`, the machine-vision camera modelled on the wrist |
| `scripts/wrist_view.py` | Interactive scene plus a live browser stream of the wrist camera |
| `scripts/generate_pipette.py` | Builds the micropipette that mounts on the flange |
| `scripts/generate_open_vessels.py` | Opens catalogue flasks and puts liquid in them |
| `scripts/generate_open_balance.py` | Cuts the roof off a balance, gives it a pan, and builds a readout that can change |
| `scripts/generate_beaker.py` | Wraps the lab room's beaker mesh as the receiving container |
| `scripts/pipetting.py` | Liquid levels, and the rules for drawing and delivering |
| `scripts/pipette_test.py` | Runs the full transfer on every flask and scores it |
| `scripts/grasp_test.py` | Drives approach, force-feedback close and lift on every dynamic vessel, and scores it |
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
| `assets/robotiq_2f85_sensed/` | Menagerie's 2F-85 with touch sites and the sensors that report a grasp (generated) |
| `assets/wrist_camera/` | The eye-in-hand camera as geometry: lens, body, bracket and flange plate (generated) |
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
