# Vertical uncap-and-pipette hand

The hand of [`gripper-design/vertical_hand.html`](../../../gripper-design/vertical_hand.html)
for Blender, MuJoCo and Isaac Lab: the forearm comes straight down beside the
vial and a 154 mm U-channel cage hangs from the flange, as wide as the iris
housing plus 4 mm a side. The parabolic cradles hold the vial from the sides on
a beam at the cage's foot, the iris clamp slides straight back along the +Y
plate and lifts on its own column, the micropipette hangs fixed on the vial's
axis above the clamp's path and only goes down. The model ends at the servo head's
top plate: the UR flange and the arm are not part of it. Same parts and numbers as the page
(`uncap-robustness/gripper.py`, `iris_pipette_rig.py`, `params.py`,
`pipette_geometry.py`), one description for everything:
[`scripts/vertical_hand_rig.py`](../../scripts/vertical_hand_rig.py).

Everything here is generated. Do not edit the files by hand; change the rig or
the generator and rerun, from `simulation/`:

```bash
uv run --no-project --python 3.11 --with bpy --with mujoco python scripts/generate_vertical_hand_blend.py
```

| File | For | What |
| --- | --- | --- |
| `vertical_hand.blend` | Blender | The hand rigged: 9 custom properties on the `vertical_hand` root (the page's sliders plus `hand_x`, SI units), every joint an empty driven from them, the reference 60 ml bottle and its cap changing hands by the page's rule (Child Of constraints switched by drivers), the 23-step sequence keyframed at 30 fps (1000 frames, sine easing like the page): the page's 21 steps with the hand advancing 120 mm onto the bottle's axis first and backing away at the end. Check points as empties: `jaw_l_vertex`, `cap_seat`, `tip`, `button`. |
| `vertical_hand.glb` | any glTF viewer, the dashboard | +Y up, the sequence baked, the properties and the step names as extras on the root. |
| `vertical_hand.usdc` (+ `textures/`) | Isaac Sim's stage, Omniverse | Blender's USD export, animation baked. Visual only: no joints, no physics. |
| `vertical_hand.xml` | MuJoCo | The hand alone: 20 joints, 9 actuated (`approach`, `lift`, `jaw_l`, `clamp_x`, `clamp_lift`, `body_yaw`, `cam`, `pip_slide`, `plunger`), the second jaw, the three planets, the six blades and the sun following through joint equalities. Visual meshes in `meshes/`. Every part collides (322 primitives, group 3): boxes for the softened boxes and the cradles (chord boxes along the parabola, liner plus plate), cylinders for the turned parts, rings as circles of boxes with their bores open, the side plates as two slabs plus a hull for the toe. Hand parts collide with the bottle, the cap and the floor, never with each other; only LEDs, bolts, pins and the liners are decoration. Attach it with `<attach model=... body="vertical_hand"/>`. |
| `vertical_hand_scene.xml` | MuJoCo | The hand over a floor with the bottle (hollow: floor disc, wall and neck boxes) and the cap as free bodies, the three welds the page's rule switches, keyframe `home`. `python scripts/vertical_hand_play.py [--view]` plays the sequence and checks it. |
| `vertical_hand.urdf` | Isaac Lab (URDF importer) | The same tree, followers as `<mimic>` joints, meshes by relative path, the same collision primitives as `<collision>` elements (the hulls as `col_*.stl`). Root link `vertical_hand`: import it with a fixed base. The bottle and the cap for Isaac are `../ur10e_iris_pipette/reference_{bottle,cap}.urdf` (the same 60 ml bottle and PP25 cap). |
| `meshes/*.stl` | both | One visual mesh per link and material (`<link>__<material>.stl`) and one `col_<link>_<n>.stl` per convex-hull collision piece, in the link's joint frame, binary, metres. |

Frames: +X from the arm to the bottle, Y across (+Y the clamp's rail, −Y the
pipette's rail), Z up. The clamp's `clamp_x` is 0 centred on the cap and −90 mm
parked back under the pipette. `hand_x` (joint `approach`) slides the whole
hand along X: 0 with the cage on the bottle's axis, −120 mm where the sequence
starts and ends; it is not on the page. The bottle's axis is x = y = 0 and the reference
bottle's base is at z = 0 when `lift_z` = 0; the hand's root sits on the
world's origin and the table is z = 0.

Verified (2026-09-20): the `.blend` (evaluated drivers), the MJCF (sites) and
the URDF (loaded in MuJoCo, which honours `<mimic>`) put the cradle vertices,
the cap seat, a blade tip, the pipette tip and the plunger button where
`vertical_hand_rig.fk` does, within 0.04 µm, at the end of steps 3, 6, 8, 10,
12, 17 and 22, and the URDF's collision geoms land where the MJCF's do within
0.4 µm. The MuJoCo sequence passes its checks (pads at the tool axis,
bottle carried 100 mm, cap up the thread 5.5 mm and back with the clamp, tip
at the dive on the axis, cap back on the neck, bottle set down where it was,
hand back where it started, joints within 2.3 mm / 9.2 mrad of their targets,
nothing of the hand on the floor), with all 322 collision geoms live.
Isaac Lab has not been run on this machine: the URDF's geometry is verified,
the importer's handling of `<mimic>` is not.
