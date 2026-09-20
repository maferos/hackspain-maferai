# Vertical uncap-and-pipette hand

The hand of [`gripper-design/vertical_hand.html`](../../../gripper-design/vertical_hand.html)
for Blender, MuJoCo and Isaac Lab: the forearm comes straight down beside the
vial, a harness under the UR flange carries the three servos, the parabolic
cradles hold the vial from the sides, the iris clamp slides in over the cap on
a Y rail and lifts on its own column, the micropipette parked outboard swings
onto the axis and goes down the neck. Same parts and numbers as the page
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
| `vertical_hand.blend` | Blender | The hand rigged: 9 custom properties on the `vertical_hand` root (the page's sliders, SI units), every joint an empty driven from them, the reference 60 ml bottle and its cap changing hands by the page's rule (Child Of constraints switched by drivers), the 23-step sequence keyframed at 30 fps (970 frames, sine easing like the page). Check points as empties: `jaw_l_vertex`, `cap_seat`, `tip`, `button`. |
| `vertical_hand.glb` | any glTF viewer, the dashboard | +Y up, the sequence baked, the properties and the step names as extras on the root. |
| `vertical_hand.usdc` (+ `textures/`) | Isaac Sim's stage, Omniverse | Blender's USD export, animation baked. Visual only: no joints, no physics. |
| `vertical_hand.xml` | MuJoCo | The hand alone: 20 joints, 9 actuated (`lift`, `jaw_l`, `clamp_y`, `clamp_lift`, `body_yaw`, `cam`, `pip_slide`, `pip_swing`, `plunger`), the second jaw, the three planets, the six blades and the sun following through joint equalities. Visual meshes in `meshes/`, collision as primitives: the cradle liners as chord boxes, the blades as boxes, the pipette's tip and shaft as a cylinder. Attach it with `<attach model=... body="vertical_hand"/>`. |
| `vertical_hand_scene.xml` | MuJoCo | The hand over a floor with the bottle (hollow: floor disc, wall and neck boxes) and the cap as free bodies, the three welds the page's rule switches, keyframe `home`. `python scripts/vertical_hand_play.py [--view]` plays the sequence and checks it. |
| `vertical_hand.urdf` | Isaac Lab (URDF importer) | The same tree, followers as `<mimic>` joints, meshes by relative path, collision as above. Root link `vertical_hand`: import it with a fixed base. The bottle and the cap for Isaac are `../ur10e_iris_pipette/reference_{bottle,cap}.urdf` (the same 60 ml bottle and PP25 cap). |
| `meshes/*.stl` | both | One visual mesh per link and material (`<link>__<material>.stl`), in the link's joint frame, binary, metres. |

Frames: +X from the arm to the bottle, Y across (+Y the clamp's rail, −Y the
pipette's mast), Z up. The bottle's axis is x = y = 0 and the reference
bottle's base is at z = 0 when `lift_z` = 0; the hand's root sits on the
world's origin and the table is z = 0.

Verified (2026-09-20): the `.blend` (evaluated drivers), the MJCF (sites) and
the URDF (loaded in MuJoCo, which honours `<mimic>`) put the cradle vertices,
the cap seat, a blade tip, the pipette tip and the plunger button where
`vertical_hand_rig.fk` does, within 0.04 µm, at the end of steps 2, 5, 7, 9,
12, 17 and 23. The MuJoCo sequence passes its checks (pads at the tool axis,
bottle carried 100 mm, cap up the thread 5.5 mm and out with the clamp, tip
at the dive on the axis, cap back on the neck, bottle set down where it was,
joints within 2.1 mm / 9.2 mrad of their targets, nothing on the floor).
Isaac Lab has not been run on this machine: the URDF's geometry is verified,
the importer's handling of `<mimic>` is not.
