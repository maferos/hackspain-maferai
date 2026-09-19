# Full physics for the uncap-and-pipette hand, in Isaac Lab

How to go from the kinematic sequence that ships to one where the grip, the
blades and the thread work by contact — **in Isaac only**; the MuJoCo scene
stays kinematic. Nothing here has run in Isaac yet: there was no Isaac on the
machine this was written on. Every number below comes from
`scripts/iris_pipette_rig.py`, `scripts/iris_pipette_plan.py`, the MuJoCo run
(`scripts/iris_pipette_play.py`) or the clamp's own asset
(`assets/iris_clamp/iris_clamp_sim_asset.zip`).

## 1. Where it stands

### The objects

| | What | Numbers |
| --- | --- | --- |
| Bottle | the 60 ml amber bottle of `assets/amber-bottles` (`AMBER` in the rig) | Ø40 mm, 95 mm to the lip, straight wall to 65.75 mm, neck from 77.75 mm, bore Ø18.4 mm; 57.8 g (glass mesh × 2500 kg/m³) |
| Cap | its PP25 cap | ribs Ø28.0 mm, tamper band Ø28.8 mm at the bottom 4.1 mm, 18.5 mm tall, underside 78.1 mm up; 2.5 g (mesh × 905 kg/m³) |
| Thread | PP25 | pitch 2.75 mm, 2 turns: the cap rises `CAP_LIFT` = 5.5 mm |

The bottle collides as a hollow ring of boxes (a floor disc, 16 wall boxes up
the straight body, 8 neck boxes around the bore; the shoulder is left open,
nothing reaches it), the cap as one cylinder r 14.4 mm over its full height.
Both are drawn with the kit's meshes.

### MuJoCo today, and what the Isaac script does for each piece

| Mechanism | MuJoCo (`models/iris_pipette_scene.xml`) | Isaac (`scripts/iris_pipette_isaac.py`) |
| --- | --- | --- |
| Bottle carried | weld `hold_bottle` to `hand_frame`, switched on when the jaws close on Ø40 | `place(bottle, hand_frame pose)` every step |
| Cap on the neck / in the clamp | welds `cap_on_bottle` / `cap_in_clamp` (to `carrier`), engaged at the present relative pose | `place(cap, neck or cap_seat pose)` every step |
| Who touches whom | bitmasks, `COLLIDE` in `generate_iris_pipette_scene.py`: pads↔bottle, pipette↔clamp/bottle/floor, nothing else | **nothing — see step 0** |
| Planetary train, blades | tendons + joint equalities from the clamp's MJCF | `<mimic>` (blades ×−1, planets ×3 of the cam); `sun_input` a real joint driven to `yaw − 3·cam` |
| Drives | position actuators, `GAINS` | `ImplicitActuatorCfg`, same gains |
| Start | keyframe `home` | `init_state` from `plan.START` |

The rule that switches the welds and the pose writes is the page's,
`iris_pipette_plan.attachments()`: the bottle rides the hand while the jaws are
closed on it, the cap rides the bottle until the housing turns and the carrier
after.

### Baseline: the MuJoCo run (`python scripts/iris_pipette_play.py`)

The numbers an Isaac run has to reproduce, kinematic or not:

| Check | MuJoCo |
| --- | --- |
| Pads on the bottle at `GRIPPED_AT` (2.5 s) | 43.9 mm up (planned 44 ± 5) |
| Bottle carried at `LIFTED_AT` (3.7 s) | 93.7 mm (want ≥ 90) |
| Cap off its seat at `UNSCREWED_AT` (9.2 s) | 4.8 mm (want ≥ 4.4 = 0.8 · 5.5; the carrier is still catching up with `FOLLOW`) |
| Cap with the clamp at `CAP_AWAY_AT` (10.8 s) | 89 mm off the axis, 0.1 mm from the seat |
| Tip at `DIVED_AT` (14.2 s) | 18.8 mm above the floor (planned 20 ± 2), 0.1 mm off the axis |
| Pipette↔clamp contacts | 0 |
| Cap back at `RECAPPED_AT` (22.6 s) | −0.33 mm from its seat |
| Bottle set down | 0.1 mm from where it was picked, 0° tilt |
| Worst joint tracking | `body_yaw`, 0.042 rad |

The rig URDF, loaded in MuJoCo (which honours `<mimic>`), puts every body
within 1.41 µm of `iris_pipette_rig.fk` over the sequence. That is all that is
verified on the Isaac side.

## 2. Step 0 — collision filtering and contact scale

**Needed before the kinematic run means anything.** The bitmasks are MuJoCo's;
the URDF has no way to carry them. `models/iris_pipette_rig.urdf` exports 16
`<collision>` elements: the four pad boxes, ten pipette primitives on
`pipette_swing` and `pipette_plunger`, and two invisible envelopes on
`clamp_mount` — `clamp_envelope` (cylinder r 69 mm, 4 mm below to 60 mm above
the iris plane) and `motor_envelope`. With the clamp down the envelope encloses
the cap and the top of the neck, so PhysX pushes the pose-written bottle and
cap against the driven clamp every step.

Reproduce `COLLIDE` with filtered pairs after `sim.reset()` has spawned the
prims (untested; `UsdPhysics.FilteredPairsAPI` is the standard way):

```python
from pxr import UsdPhysics
import isaaclab.sim as sim_utils

stage = sim_utils.get_current_stage()
def ignore(a, b):
    UsdPhysics.FilteredPairsAPI.Apply(stage.GetPrimAtPath(a)).CreateFilteredPairsRel().AddTarget(b)

for body in ('/World/Bottle', '/World/Cap'):
    ignore(body, '/World/Rig/clamp_mount')      # the envelopes: they are for the pipette only
ignore('/World/Cap', '/World/Bottle')             # the cap's solid cylinder swallows the neck
ignore('/World/Cap', '/World/Rig/pipette_swing')  # MuJoCo: the cap meets nothing
```

The cap–bottle pair matters as much as the envelopes: the cap collides as a
solid cylinder r 14.4 mm from its underside up, and the neck's boxes (out to
12.45 mm, up to the lip at 95 mm) sit inside it whenever it is on. Keep that
pair filtered through every stage below: with the scripted thread (stage 3, A)
the cap never needs to rest on the neck; only a real thread (C) replaces both
colliders with the threaded meshes.

(Stage 2 below removes the `clamp_mount`–cap pair, once the blades carry their
own boxes.) The simpler way out is to leave the envelopes out of the URDF: they
exist only for the pipette↔clamp check, and in Isaac that check cannot run
as it is anyway — both are links of one articulation and self-collision is off.
Do it geometrically instead (distance from the pipette primitives to the
envelope cylinder, from the body poses), or enable self-collision and filter
every other pair, which is a lot of pairs.

Contact scale: the parts are millimetres (a 0.4 mm step from the band to the
ribs, a 2.75 mm pitch), PhysX's default contact offset is centimetres, and the
cap weighs 2.5 g. On the bottle, the cap, the pads and the blades:

```python
collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.001, rest_offset=0.0)
```

and `dt = 1/480` (MuJoCo runs at 1 ms; the script uses 1/240). If the cap
jitters between six blades, raise the solver iterations first
(`solver_position_iteration_count=32` on the cap) before giving it a heavier
mass; if you do, write down that it is not 2.5 g any more.

*Done when:* the kinematic run passes the baseline table with no contact
between the clamp and the bottle or cap in the contact report.

## 3. Stage 1 — the bottle held by friction

Drop `place(bottle, ...)`. The pads collide already; give pads and bottle a
material:

```python
physics_material=sim_utils.RigidBodyMaterialCfg(static_friction=1.0, dynamic_friction=0.9)
rigid_props=sim_utils.RigidBodyPropertiesCfg(max_depenetration_velocity=1.0)
```

The driver target is `0.8 · clamp((85 − a)/(85 − 40))` (`plan.driver_target`):
it reaches fully closed as the jaws reach Ø40, so the fingers keep squeezing
and the driver's `effort_limit` (5 N·m) sets how hard. 57.8 g needs little.
PhysX mimic joints are soft: if the left finger lags the right by more than
20 mrad, raise the driver's stiffness before anything else.
`scripts/hand_pick_isaac.py` grips this same bottle with the same gains (also
not yet run); whichever runs first, carry its gains over.

*Done when* (fixed before the run): the bottle rises ≥ 90 mm by `LIFTED_AT`
with no pose write, slips < 2 mm in the pads over the whole carry, and is set
down within 10 mm and 5° of where it was picked.

## 4. Stage 2 — the cap held by the blades

The blades need collision boxes. The clamp's MJCF (`mujoco/iris_clamp.xml` in
the zip) has one per blade, in the blade frame:

```
box  half-size 0.006 0.031 0.00125   pos 0.006 0.031 0.00125   friction 1.5
```

Add them to `blade_k` in `iris_pipette_rig.tree()` under a **new class**,
`collide='blade'`, mapped to `(0, 0)` in `COLLIDE`: the URDF exports every
collider, so Isaac gets them, and MuJoCo keeps ignoring them. (Using the
existing class `'cap'` would make them collide in MuJoCo too.) Then remove the
`clamp_mount`–cap filter of step 0 for the blade links only.

The geometry agrees with the rig. The box's inner face lies at
`r_pivot · cos α` = 55 · cos α mm from the axis, so it is tangent to the Ø28.8
band at `ALPHA_CONTACT` = 74.8°, the angle the page and the simulators close
to; the contact point is 55 · sin α = 53 mm along the 62 mm blade, on it. The
cap's collision cylinder is r 14.4 over its full height and the six blades
stack 15 mm from 1.5 mm above its underside, so all six meet it (the real cap's
ribs are 0.4 mm further in: on the mesh only the lowest blade, on the band,
would touch).

To grip, the cam ring **overshoots**: target `iris_angle = ALPHA_CONTACT + 2°`,
and the cam drive's `effort_limit` (3 N·m) sets the squeeze. Six blades at μ
1.5 on r 14.4 mm give `6 · F · 1.5 · 0.0144 = 0.13 · F` N·m of torque for a
normal force F per blade. The clamp's own demo turned its thread against
0.04 N·m of friction (`cap_spin` frictionloss), so F ≈ 0.3 N per blade would
do; aim for several times that. (The demo's clutch, which let the housing
turn at 0.15 N·m, is not in this rig: `body_yaw` is driven directly, so the
cap only ever sees what the thread resists.)

The hinge tilts the blades: while the cap rises 5.5 mm the clamp follows on a
90 mm arc (`FOLLOW` = 3.5°). Across the 15 mm blade stack that is
15 · tan 3.5° = 0.92 mm of misfit against a cap that goes straight up, plus
90 · (1 − cos 3.5°) = 0.17 mm of sideways travel. The cam's effort limit lets
the blades give way that much rather than crush. If the cap slips anyway, hold
the hinge at 0 during the unscrew and add a sim-only passive slide on
`clamp_mount` (0–10 mm along the clamp axis, lightly sprung) so the clamp
floats up the thread instead of swinging.

*Done when:* at `UNSCREWED_AT` the cap's yaw follows the carrier within 5°, and
at `CAP_AWAY_AT` it is within 5 mm of the seat, held by contact only.

## 5. Stage 3 — the thread

PhysX has no screw joint and no joint equality, so the clamp's MuJoCo recipe
(`bottle_cap.xml`: a thread follower on `cap_lift` + `cap_spin` coupled by
`lift = pitch/2π · spin`, welded to the cap, both switched off after two
turns) does not port.

**A — scripted thread (recommended).** Keep the cap a free body held by the
blades, and while it is on the thread write only what a thread would: its
height and its tilt, from the carrier's yaw.

```python
turns = state['housing_turns']
on_thread = 0.0 < turns < rig.IRIS['turns']          # both ways: unscrewing and recapping
if on_thread:
    yaw = carrier_yaw()                               # measured, from body_quat_w of 'carrier'
    z = rig.IRIS['bottle_h'] + yaw / (2 * math.pi) * rig.IRIS['pitch']
    place(cap, bottle_pos + (0, 0, z), quat_about_z(yaw))   # upright, on the bottle axis
```

The plan already raises the clamp in step with the turns (in step 6
`hinge_angle` eases to `FOLLOW` over the same interval as `housing_turns`), so
the written pose and the blades move together. At two turns stop writing: the
cap is loose and leaves with the clamp by friction alone. On the recap, start
writing again once the housing turns back below two, until it reaches 0; then
release it onto the neck. Check the direction on the first run: in the rig the
housing's yaw is `+2π · turns`, counter-clockwise from above, which unscrews a
right-hand thread.

**C — a real thread, by SDF contact.** The kit has the PP25 pair with real
helices, checked free of interference through the two turns:
`assets/amber-bottles/thread_pair/cap_PP25_threaded.glb` and
`neck_PP25.glb`. Note that `neck_PP25.glb` is the **50 ml** flask (Ø37.6 mm);
the finish is the same, but for this scene regenerate the pair for 60 ml
(`uv run --python 3.11 --with bpy python generate_amber_bottles.py --pair 60 --out thread_pair`
in `assets/amber-bottles/`). This is Step 2 of `simulation/CAP_GRIPPER_PLAN.md`
(SDF colliders at resolution 256–512, contact offsets of the order of the
0.15 mm thread clearance). Do it there first, cap and neck alone; only then
put it under the blades. Until it converges, A.

**B — thread as mimic joints**, rejected: a `cap_lift` prismatic joint
mimicking a `cap_spin` joint (multiplier pitch/2π = 0.000438) turns the cap up
the thread, but a URDF joint cannot be broken at run time, so the cap never
comes off.

*Done when:* the cap is 5.5 ± 1 mm off its seat at `UNSCREWED_AT` and within
1 mm of it at `RECAPPED_AT`.

## 6. The checks

`iris_pipette_isaac.py` already prints the baseline checks; each stage adds its
own and turns off the pose write it replaces.

| Check | Pass | MuJoCo today | Isaac kinematic | Isaac full physics |
| --- | --- | --- | --- | --- |
| Blades follow the cam (mimic) | ≤ 20 mrad | exact (equality) | first check | same |
| Pads on the bottle | 44 ± 5 mm | 43.9 | yes | yes |
| Bottle carried | ≥ 90 mm | 93.7 | yes | stage 1, no pose write; slip < 2 mm |
| Cap off its seat, unscrewed | ≥ 4.4 mm (5.5 ± 1 with a thread) | 4.8 | yes | stage 3 |
| Cap yaw follows the carrier | ≤ 5° | welded | — | stage 2 |
| Cap with the clamp | ≥ 40 mm off axis, ≤ 5 mm from seat | 89 / 0.1 | yes | stage 2, contact only |
| Tip at the dive | 20 ± 2 mm, inside the bore | 18.8, 0.1 off | yes | same |
| Pipette↔clamp | no contact | 0 | geometric only (step 0) | same |
| Cap back on | ≤ 1 mm | −0.33 | yes | stage 3 |
| Bottle set down | ≤ 10 mm, ≤ 5° | 0.1 mm, 0° | yes | stage 1 |

## 7. What stays kinematic

The plunger pushes no liquid in either simulator; the tip's "fill" is a render
colour (page and .blend only); the pipette's collision primitives (from
`micropipette.xml`) only keep it off the clamp, the bottle and the floor.

This rig also answers the open questions of `CAP_GRIPPER_PLAN.md`: the housing
turns continuously (two turns, no regrips), the differential is a real
planetary (one cam ring for the blades, the housing's yaw through the sun),
and the flask is PP25 — PP20 and smaller caps are too small for the blades to
reach inside their 76° limit.
