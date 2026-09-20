# Vertical uncap-and-pipette hand

The hand of [`gripper-design/vertical_hand.html`](../../../gripper-design/vertical_hand.html)
for Blender, MuJoCo and Isaac Lab: the forearm comes straight down beside the
vial and a 154 mm U-channel cage hangs from the flange, as wide as the iris
housing plus 4 mm a side. The parabolic cradles hold the vial from the sides on
a beam at the cage's foot, the iris clamp slides straight back along the +Y
plate and lifts on its own column, the micropipette hangs fixed on the vial's
axis above the clamp's path and only goes down. Same parts and numbers as the page
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
| `vertical_hand.blend` | Blender | The hand rigged: 8 custom properties on the `vertical_hand` root (the page's sliders, SI units), every joint an empty driven from them, the reference 60 ml bottle and its cap changing hands by the page's rule (Child Of constraints switched by drivers), the 21-step sequence keyframed at 30 fps (916 frames, sine easing like the page). Check points as empties: `jaw_l_vertex`, `cap_seat`, `tip`, `button`. |
| `vertical_hand.glb` | any glTF viewer, the dashboard | +Y up, the sequence baked, the properties and the step names as extras on the root. |
| `vertical_hand.usdc` (+ `textures/`) | Isaac Sim's stage, Omniverse | Blender's USD export, animation baked. Visual only: no joints, no physics. |
| `vertical_hand.xml` | MuJoCo | The hand alone: 19 joints, 8 actuated (`lift`, `jaw_l`, `clamp_x`, `clamp_lift`, `body_yaw`, `cam`, `pip_slide`, `plunger`), the second jaw, the three planets, the six blades and the sun following through joint equalities. Visual meshes in `meshes/`, collision as primitives: the cradle liners as chord boxes, the blades as boxes, the pipette's tip and shaft as a cylinder. Attach it with `<attach model=... body="vertical_hand"/>`. |
| `vertical_hand_scene.xml` | MuJoCo | The hand over a floor with the bottle (hollow: floor disc, wall and neck boxes) and the cap as free bodies, the three welds the page's rule switches, keyframe `home`. `python scripts/vertical_hand_play.py [--view]` plays the sequence and checks it. |
| `vertical_hand.urdf` | Isaac Lab (URDF importer) | The same tree, followers as `<mimic>` joints, meshes by relative path, collision as above. Root link `vertical_hand`: import it with a fixed base. The bottle and the cap for Isaac are `../ur10e_iris_pipette/reference_{bottle,cap}.urdf` (the same 60 ml bottle and PP25 cap). |
| `meshes/*.stl` | both | One visual mesh per link and material (`<link>__<material>.stl`), in the link's joint frame, binary, metres. |

Frames: +X from the arm to the bottle, Y across (+Y the clamp's rail, −Y the
pipette's rail), Z up. The clamp's `clamp_x` is 0 centred on the cap and −90 mm
parked back under the pipette. The bottle's axis is x = y = 0 and the reference
bottle's base is at z = 0 when `lift_z` = 0; the hand's root sits on the
world's origin and the table is z = 0.

Verified (2026-09-20): the `.blend` (evaluated drivers), the MJCF (sites) and
the URDF (loaded in MuJoCo, which honours `<mimic>`) put the cradle vertices,
the cap seat, a blade tip, the pipette tip and the plunger button where
`vertical_hand_rig.fk` does, within 0.04 µm, at the end of steps 2, 5, 7, 9,
11, 16 and 21. The MuJoCo sequence passes its checks (pads at the tool axis,
bottle carried 100 mm, cap up the thread 5.5 mm and back with the clamp, tip
at the dive on the axis, cap back on the neck, bottle set down where it was,
joints within 2.3 mm / 9.2 mrad of their targets, nothing on the floor).
Isaac Lab has not been run on this machine: the URDF's geometry is verified,
the importer's handling of `<mimic>` is not.
