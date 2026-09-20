# Findings about files outside this directory

Checked against HEAD `de976ce`. Nothing outside `uncap-robustness/` was changed.

## 1. The rig is placed on the cap seat, so bottles shorter than ~75 mm put the gripper into the table

- **Files:** `simulation/scripts/iris_pipette_rig.py` (`GRIP_Z = IRIS['bottle_h'] - 0.034`, `BOTTLE['h']` minimum 0.075). Owner: simulation (Eki).
- **What:** every part of the hand is placed relative to the neck. The page's slider says so, and does not go below 75 mm to the cap.
  - The 10, 20 and 30 ml amber bottles have their cap seat at 39.7, 53.3 and 61.6 mm.
  - With the hand on their neck, the gripper sits 38, 25 and 16 mm lower than for the 60 ml bottle, below the table.
  - The sweep records these as `table` failures.
  - The 50 ml bottle (72.5 mm, below the page's 75 mm floor) still clears the table in the pilot.
- **Repro:** `simulation/.venv/bin/python uncap-robustness/trial.py --bottle 30`
- **Is it a bug?** No. The page states the limit. But no amber bottle under 50 ml can be handled with the rig as laid out, and PP18/PP20 caps are also too small for the blades (`FULL_PHYSICS_ISAAC.md`).

## 1b. Measured: whatever the fingers, the cap seat must be at ≥ 57.5 mm

Measured on the rig as shipped, with the clamp down on the cap:

- **Table limit.** The gripper's axis must sit ≥ 39.5 mm above the table: the `base_mount` disc hangs 37.5 mm below it, plus 2 mm of margin.
- **Clamp limit.** The axis must sit ≤ cap seat − 18 mm. The housing reaches 2.5 mm under the seat, and the gripper rises 13.5 mm above its axis within the housing's footprint, plus 2 mm of margin.

Consequences:

- L fingertips move the pads, not the axis. They cannot make the 10 ml (cap at 39.7 mm) or the 20 ml (53.3 mm) bottle graspable on a bare table.
- The shipped layout (axis at cap − 34 mm) also leaves out the 30 ml bottle, which fits with the axis at cap − 20 mm. That is the v2 hand in README.md.
- The real UR10e wrist is 51 mm below the pads when the tool is level. In the shipped scene it is drawn only, not collided, so the scene cannot show that the wrist would hit first.

**Owner:** simulation (Eki). **Where:** `simulation/scripts/iris_pipette_rig.py` (`GRIP_Z`, `HINGE`) and the stub in `generate_iris_pipette_scene.py`.

## 1c. The shipped plan screws the cap back by counting turns

- **What.** `iris_pipette_plan.STEPS`, step 15, turns the housing from 2 turns back to 0: the same count it unscrewed.
- **Why it matters.** With a physical thread, the cap is caught again where the clamp brings it back, about 0.4 turns higher than where it let go. It then ends 1–5 mm high: 11 of the v1 failures.
- **In the shipped scene** it is harmless: the cap is welded there.
- **Fix, if the plan is ever driven on real hardware or a threaded simulation:** screw to a torque, not to a count. v2 does that here.

## 2. Carried over, not new: the Isaac script's collisions

`simulation/assets/ur10e_iris_pipette/FULL_PHYSICS_ISAAC.md`, step 0, already documents it: the clamp envelopes and the cap's solid cylinder collide with the pose-written bottle and cap in `iris_pipette_isaac.py`. This experiment's `scene.py` solves the same problem in MuJoCo with its own contact classes (`MASKS`) and a hollow cap.

## 3. What the reference hand needed, for whoever ports it

The hand in README.md's "reference hand" section is this directory's answer, and
three of its parts are changes to the shipped design, not to the model:

- **A compact gripper.** The 2F-85's envelope (37.5 mm below its axis) is what
  rules out the small bottles, not the fingertips.
- **A 20 mm lift on the clamp.** Unscrewed, the cap is still 12 mm inside the
  neck. Pulling it straight out instead of swinging it out on the hinge's arc
  takes the bottle's tilt in the hand from 14–26° down to 0.4–3.1°.
- **Screwing the cap back to a torque, not to a turn count.** See 1c.

The first two are mechanical and would have to be built; the third is a change
to `iris_pipette_plan.py`'s step 15 and to whatever drives it.

## Not a finding

MuJoCo's default contact stiffness let this experiment's bottle sink 5 mm into the floor, which is why `scene.PHYSICS['solid_solref']` exists. The shipped `iris_pipette_scene.xml` does not show it: its bottle rests 0.15 mm into the floor, checked at `de976ce`.
