# Full physics for the uncap-and-pipette hand, in Isaac Lab

What ships (`scripts/iris_pipette_isaac.py`, `scripts/iris_pipette_play.py`)
plays the sequence **kinematically**: every joint has a position drive, and the
bottle and the cap change hands by rule, not by contact — the page's rule
(`iris_pipette_plan.attachments()`): the bottle rides on the hand frame while
the jaws are closed on it, the cap rides on the bottle until the housing turns
and on the clamp's carrier after. MuJoCo does it with three welds switched at
run time; Isaac, which has no switchable weld, by writing the two bodies' root
poses every step. The pads squeeze the bottle and the blades close on the cap
for the look of it; nothing depends on the contact.

This note is how to make it real **in Isaac only** — the MuJoCo scene stays as
it is. Three things have to be replaced, in order of difficulty: the grip, the
cap in the blades, and the thread. Everything below is untested: there was no
Isaac on the machine this was written on.

## 1. The bottle held by friction

Drop the `place(bottle, ...)` call in `iris_pipette_isaac.py`. The 2F-85's pad
boxes already collide (the URDF carries them as `<collision>`), the bottle
URDF is a ring of boxes with `friction="1"` in the MJCF; in Isaac set the
materials explicitly:

```python
rigid_props=sim_utils.RigidBodyPropertiesCfg(max_depenetration_velocity=1.0, linear_damping=0.5)
physics_material=sim_utils.RigidBodyMaterialCfg(static_friction=1.0, dynamic_friction=0.9)
```

on the bottle and the pads (`/World/Rig/.*_pad`). The driver joint's target is
already `0.8 · clamp((85 − a)/(85 − 52))` — fully closed on the bottle, so the
fingers keep squeezing and the actuator's `effort_limit` (5 N·m) sets how
hard. PhysX mimic joints are soft: if the left finger lags the right by more
than 20 mrad (the first check), raise the driver's stiffness before touching
anything else. `scripts/hand_pick_isaac.py` does exactly this grip on the 60 ml
amber bottle; start from its gains.

## 2. The cap held by the blades

Drop `place(cap, ...)` while `attachments(state)['cap'] == 'clamp'`. The
blades need collision boxes: they are in the clamp's own MJCF
(`assets/iris_clamp/iris_clamp_sim_asset.zip`, `mujoco/iris_clamp.xml`), one
per blade in the blade frame:

```
box  size 0.006 0.031 0.00125   pos 0.006 0.031 0.00125   friction 1.5
```

Add them to `blade_k` in `iris_pipette_rig.tree()` with `collide='cap'` (the
generator writes them to both MJCF and URDF) and give the cap's cylinder the
matching material. Then let the cam ring **overshoot**: `ALPHA_CONTACT`
(75.3°, blades tangent to the Ø28 mm cap) is where the page stops; the target
that grips is a few degrees past it, e.g. `iris_angle = ALPHA_CONTACT + 2°`,
with the cam drive's `effort_limit` (3 N·m) deciding the squeeze. Six blades
with `friction 1.5` at 14 mm radius give about `6 · F · 1.5 · 0.014` N·m of
thread torque; the clamp's demo (`mujoco/demo_unscrew.py`) needed 0.04 N·m to
turn the thread and reached it with 0.45 N·m on the sun.

Mind the hinge: while the cap unscrews it rises 5 mm on the thread and the
clamp follows on a 90 mm arc (`FOLLOW` = 3.2°), so the blades tilt 3.2° against
a cap that goes straight up. Soft contacts absorb ~1.5 mm of that; if the cap
slips, add a sim-only axial slide on `clamp_mount` (0–10 mm along the clamp
axis, unactuated, lightly sprung) so the clamp can float up the thread.

## 3. The thread

PhysX has no screw joint and no tendon equality, so the MuJoCo recipe
(`bottle_cap.xml`: a `cap_lift` slide + `cap_spin` hinge on a thread follower,
a joint equality `lift = pitch/2π · spin`, a weld to the cap, both switched
off after 2 turns) does not port. Two options:

**A — scripted thread (recommended).** Keep the cap a free body. While the
blades hold it and `0 < turns < 2` (in either direction), write its root pose
from the measured housing yaw each step:

```
z   = bottle_shoulder + (yaw / 2π) · pitch        (pitch 2.5 mm)
yaw = carrier yaw
```

Once `turns ≥ 2` stop writing: the cap is loose, held by blade friction alone,
and swings away with the clamp. On the way back, resume writing when the
clamp is on the neck and the blades hold the cap, until `turns = 0`; then
release it onto the neck. This is `place()` with a different pose, so it is a
dozen lines in `iris_pipette_isaac.py`; the contact does the holding, the
script does only what a thread would.

**B — thread as mimic joints.** Give the bottle URDF a `cap` link on a
`cap_spin` continuous joint and a `cap_lift` prismatic joint that
`<mimic joint="cap_spin" multiplier="0.000398">` (pitch / 2π). PhysX then
turns the cap up the thread when the blades spin it. It cannot **release**:
a URDF joint cannot be broken at run time, so the cap never comes off. Only
useful for a scene that stops at "unscrewed", or with a second, cap-less
bottle swapped in — documented, not used.

## Checks to add

- Grip: the bottle's rise at `LIFTED_AT` ≥ 90 mm without a pose write.
- Blades: at `UNSCREWED_AT` the cap's yaw follows the carrier within 5°, and
  at `CAP_AWAY_AT` it is still within 5 mm of the seat, held by contact only.
- Thread: the cap's height at `UNSCREWED_AT` is `shoulder + 5 mm ± 1`.
- Nothing else changes: the tip's dive and the recap checks stay as they are.

## What stays kinematic

The pipette's plunger has no liquid behind it in either simulator, the tip's
"fill" is a render colour (page and .blend only), and the pipette's own
collision primitives (from `micropipette.xml`) only keep it off the clamp,
the bottle and the floor.
