# Uncap-and-pipette robustness

How robust is it for the UR10e hand to take the cap off a bottle with the
iris clamp, pipette from it and put the cap back? This experiment varies
three things:

- the bottle: the six amber bottles of `assets/amber-bottles`, 10–100 ml, each with its own neck and cap;
- how full the bottle is;
- how the arm comes at the bottle.

It runs in MuJoCo with **contact physics**. Nothing is welded:

- **The bottle** is held only by the pads' friction.
- **The cap** is held by the clamp's blades. It rises on a MuJoCo thread (the iris clamp kit's `bottle_cap.xml` recipe): a slide and a hinge coupled by a joint equality, welded to the cap. The thread lets go at the end of its travel, and catches the cap again only when the cap comes back square and centred.

The shipped scene, `simulation/models/iris_pipette_scene.xml`, is not touched. It plays the same sequence with welds.

This directory is self-contained. It reads the rest of the repository and writes nothing outside itself, so `rm -rf uncap-robustness` leaves the repository as it was.

## The reference hand: this is the one that works

**This design is the ground truth for the uncap-and-pipette hand.** It is what
`scene.HAND = 'v3'` builds, and it is what `out/model.html` plays. Earlier
hands are kept only for comparison: the shipped 2F-85 rig (v1) and the 2F-85
with L fingertips and a raised axis (v2), whose results are in
`out/v1_original_rig.csv` and `results/v2_l_fingertips.csv`.

### What it is

| Part | What | Why |
| --- | --- | --- |
| **Gripper** | Compact, ±16 mm about its own axis, drive behind the jaws (`gripper.py`) | The 2F-85 hangs 37.5 mm below its axis and rises 13.5 above; between the table and the clamp's housing that leaves no room under a 57.5 mm cap seat, so the 10, 20 and 30 ml bottles could not be picked at all |
| **Jaws** | One **parabolic cradle**, `y = v - x²/2p`, p = 8 mm, ±22.5 mm wide, 11 convex facets, the same pair for every bottle | A parabola holds any cylinder wider than 2p on two symmetric lines, and the contact walks outwards with the diameter: ±7.5 mm at 43° on the 10 ml, ±22.3 mm at 70° on the 100 ml. The bottle is centred by the pair, not by where the arm put it |
| **Grip** | 400 N drive, liner friction 1.6; the wedge puts 1500–3300 N into 12–23 contacts | It takes 1–4 N·m to turn a bottle in the cradle, against the 0.5 N·m the cap's seating torque applies. With flat pads it took 0.5 |
| **Release** | 25 N while the jaws open, and the hand presses 2 mm past the pick height first | At the full grip the cradle's outer facets sweep off the bottle and drag it back up with the hand |
| **Layout** | Tool axis at cap seat − 21 mm, flange 118 mm behind the jaws | The one rule that fits all six bottles inside both limits |
| **Clamp** | Its own 20 mm lift (`scene.CLAMP_LIFT`), and the iris stop opened from 76° to 80° | Unscrewed, the cap is still 12 mm inside the neck: swinging it out on the hinge's arc dragged it against the neck and tipped the bottle out of the hand. Now the clamp pulls it straight up first. The 80° stop is what reaches the PP18 and PP20 caps |
| **Recap** | Screwed until the torque on the cap says it is seated (0.10 N·m for 0.05 s, at half rate), not by counting turns | The thread catches the cap about 0.4 turns above where it let go, so two turns back leaves it 1–5 mm high |

### What it does, trial by trial (the pilot, before the sweep)

| Trial | Result |
| --- | --- |
| 60 ml, all four yaws | **every stage passes**; set down 0.1 mm from the pick, recap 0.35 mm, bottle moved 1.7 mm in the hand |
| 100 ml | **every stage passes**; set down 0.7 mm |
| 50 ml, 30 ml | `lift`: the bottle moves 5–7 mm in the hand |
| 10 ml, 20 ml | `reach_liquid`: the pipette cannot reach the liquid, or touches the neck |
| 100 ml at fill 0.25 | `reach_liquid`: the tip stops 10 mm above the surface |
| 60 ml, pitch +5° | `lift` |
| every trial, every size | **no contact with the table**, where the shipped rig hit it on every 10, 20 and 30 ml trial |

### What is still open

- **`lift` on the 50 and 30 ml**, and under tilt: 5–7 mm of movement in the hand, against a 3 mm rule.
- **`reach_liquid` on the short bottles**: the pipette's reach is set by the rig's rail, not by the gripper.
- **The recap over-tightens** on some trials (up to 2 mm past the seat): the torque detector reacts after the housing has already turned. A torque-limited clutch would be the honest fix.
- **The full 600-trial sweep has not been run on this design.** The CSVs in `results/` are the earlier hands'.

### Reproduce it

```bash
simulation/.venv/bin/python uncap-robustness/trial.py --bottle 60 --view   # watch it
simulation/.venv/bin/python uncap-robustness/viewer3d.py                   # -> out/model.html
simulation/.venv/bin/python uncap-robustness/sweep.py --workers 16         # the 600 trials
```

## Run

From the repository root, with the simulation venv:

```bash
simulation/.venv/bin/python uncap-robustness/bottles.py        # the six bottles, formulas checked against the meshes
simulation/.venv/bin/python uncap-robustness/trial.py          # the nominal trial; --view to watch it
simulation/.venv/bin/python uncap-robustness/sweep.py --workers 15   # 600 trials -> out/results.csv (resumable)
simulation/.venv/bin/python uncap-robustness/report.py         # -> out/report.html
```

A single trial with any factors:

```bash
simulation/.venv/bin/python uncap-robustness/trial.py --bottle 100 --fill 0.25 --pitch 10 --approach side --dx 3 --view
```

## Files

| File | What |
| --- | --- |
| `bottles.py` | The catalogue: the generator's own formulas (`generate_amber_bottles.py`, which needs bpy), checked against the meshes (worst 0.00 mm), and the glass and cap split out of each GLB into `cache/` |
| `gripper.py` | The reference gripper: the parabolic cradle, its drive, and where each jaw has to go for a given bottle |
| `viewer3d.py` | Plays one trial and writes `out/model.html`: the model in 3D, the 19 steps, the trial's numbers |
| `scene.py` | One MuJoCo model per bottle, built with `MjSpec`. It uses the shipped attachable rig as it is, plus: a 6-DoF carriage (x, y, z, yaw, pitch about the pads' centre); the kit's blade collision boxes; the hand frame slid to the bottle's diameter (the rig's slotted plate, `pad_fit`); the free bottle with a hollow collision, the liquid's mass and the thread; the hollow cap; the contact classes |
| `trial.py` | One trial: the shipped 19-step plan (`iris_pipette_plan.py`) fitted to the bottle, metrics, pass/fail per stage |
| `sweep.py` | The design below, run on a process pool, appended to `out/results.csv` |
| `report.py` | CSV → statistics, the sanity checks, representative frames → `out/report.html` |
| `FINDINGS.md` | What this turned up about files outside this directory |

## The trial

The sequence is the page's 19 steps, with four changes:

1. **The bottle.** The jaws close on the bottle under test.
2. **The dive.** The pipette dives to 10 mm under the liquid, but no closer than 3 mm to the inside floor.
3. **The iris.** It is commanded past contact to the blades' 76° stop, so the cam drive's force limit (3 N·m) is the squeeze whatever the cap.
4. **The approach.** The hand's first descent and its last retreat run along the approach direction.

The hand is placed where the clamp meets the bottle's cap, because the rig is built around the cap seat.

### Factors and levels

| Factor | Meaning | Levels (design A) | Range (design B) |
| --- | --- | --- | --- |
| `bottle` | amber bottle, ml | 10, 20, 30, 50, 60, 100 | 50, 60, 100 |
| `fill` | fraction of the nominal volume | 0.25, 0.5, 0.8 | same |
| `pitch` | deg; the hand tilted about the jaw axis through the pads' centre, + tilts the fingers down | −20, −10, −5, 0, 5, 10, 20 | U(−20, 20) |
| `approach` | the first descent and last retreat: `above` (vertical), `side` (level, from the arm's side), `diagonal` (45° down from the arm's side) | all three | random |
| `yaw` | deg; the whole hand about the bottle's axis | 0, 90, 180, 270 | U(0, 360) |
| `dx`, `dy` | mm; where the bottle really is, in the hand's axes (x along the fingers, y along the jaws) | −6, −3, 0, 3, 6 | U(−6, 6) |

**Design A** varies one factor at a time around the nominal (pitch 0, above, yaw 0, dx = dy = 0), for every bottle × fill: 360 trials.

**Design B** varies all factors at once, 240 trials, drawn with seed 0. It is limited to the three bottles that clear the table in the nominal pose (see the pilot).

### Pass rules, stage by stage (fixed before the sweep; `trial.RULES`)

| Stage | Passes when |
| --- | --- |
| `table` | no pad, pipette or gripper geom touches the floor, at any time |
| `grip` | the pads touch the bottle, and their centre is within 5 mm of the planned height on it, at `GRIPPED_AT` |
| `lift` | the bottle rose ≥ 90 mm by `LIFTED_AT`, and it moved < 3 mm in the hand between `LIFTED_AT` and the set-down |
| `uncap` | the cap ran the thread to its end (0.875 of 2 turns × pitch: the kit's helix fades out over its last half turn) by `UNSCREWED_AT` + 0.3 s |
| `cap_away` | at `CAP_AWAY_AT` the cap is ≥ 40 mm off the bottle's axis and ≤ 5 mm from the clamp's seat |
| `reach_liquid` | at `DIVED_AT` the tip is inside the bore and ≥ 3 mm under the liquid's surface (a plane square to gravity through the liquid's height on the bottle's axis), and the pipette never touched the bottle or the clamp |
| `recap` | the thread caught the cap again, ran it down to ≤ 1 mm, and the cap is within 2 mm of its seat at the end, after the iris opened |
| `place` | at the end the bottle stands within 10 mm of where it was picked, tilted ≤ 5°, on the floor |

A trial succeeds when every stage passes. `first_failure` is the first stage in that order that did not pass. A trial whose state blew up is `diverged`.

### Sanity checks (the harness is suspect if any fails; the report says so first)

- **S1 — the nominal case works.** The nominal trial (60 ml, fill 0.5) passes every stage, and its pads land within 5 mm of the plan (the shipped scene: 43.9 mm).
- **S2 — yaw changes nothing.** The problem is symmetric about the bottle's axis, so across the four yaws of design A, for every bottle × fill:
  - success and `first_failure` must agree;
  - pad height, lift, tip depth, cap to seat, recap and placement must agree within 1 mm, and tilts within 1°.
- **S3 — nothing diverges** at the nominal of any bottle.

S2 assumes the design is not sitting on a threshold. A violation traced to a real mechanical limit (the grip's torque capacity against the cap's seating torque, which is 20 % lower on the 30 ml bottle for its smaller radius) is reported as a finding, and named as such. A violation with no such trace means the harness is wrong, as it was twice: the shared model and the pad priority.

### What the report computes

These are computed from the CSV, never written by hand:

- **Success rate** overall, per bottle, per stage, and per level of each factor, with a Wilson 95 % interval.
- **Tolerance** per bottle and factor: the widest run of design-A levels around the nominal where all three fills succeed. It is reported as "none" if the nominal itself fails.
- **First failures**, per bottle and factor.

## Calibration, done on the nominal trial only, then frozen (`scene.PHYSICS`)

Each change was made to get the nominal trial right, and each is a fix, not tuning for a result:

| Change | Why |
| --- | --- |
| `timestep` 0.5 ms | The thread's weld and equality (solref 2 ms) need at least 2 steps per time constant |
| `solid_solref` 2 ms on the floor, the bottle, the cap, the blades and the thread's end stop | With MuJoCo's default (20 ms) the 86 g bottle sank 5 mm into the floor, and the cap sagged 1.8 mm past the thread's end stop, so the thread never reached its end |
| Hollow cap (a ring and a ceiling that meet the neck) and a 24-box neck up to the thread crest | With a solid cap nothing guided it back onto the neck: it came back 13–16° askew and never caught the thread |
| `noslip_iterations` 10 | Without it the cap crept in the blades while the clamp held it sideways, from 94° to 99°, then jammed on the neck and was thrown out. Trials run 3× slower |
| Release at 0.875 of the thread's travel | The kit's helix fades over its last half turn (`generate_amber_bottles.helix_thread`); at 0.97 the 3 % blade slip kept the cap engaged when the clamp swung away |
| The re-engagement is only armed from step 15 on ("Screw the cap back") | It first re-engaged the instant after release, during the unscrew: a harness bug |
| Slip in the hand is measured from `LIFTED_AT`, not `GRIPPED_AT` | A bottle off-centre by `dy` is still being centred by the jaws at `GRIPPED_AT`. That is centring, not slip. `lift` still requires ≥ 90 mm |
| `uncap` passes on the thread reaching its end by `UNSCREWED_AT` + 0.3 s, not on the cap's rise at `UNSCREWED_AT` | The rise was sampled 0.08 s before the release and passed by 0.09 mm: the rule measured the sampling instant, not the unscrew |

### A first sweep, thrown away

The first full run, `results/invalid_run1_shared_model.csv`, is kept only as evidence. It is not a result, for three reasons:

- Each worker process compiles a bottle's model once and reuses it across its trials. Re-engaging the thread writes the weld's relative pose into `model.eq_data`, so a later trial started with the cap welded where an earlier one had left it.
- **S2 caught it.** The four yaws of one bottle disagreed.
- **S1 caught it too.** The nominal trial slipped 40 mm, when it had passed on its own.

`Trial.reset()` now restores the equality data. The nominal gives the same numbers before and after another trial in the same process. The sweep was rerun from scratch.

### Pilot (15 trials, before the sweep, with the calibration above)

| Trial | Result |
| --- | --- |
| 10, 20, 30 ml, nominal | `table`. The rig sits on the cap seat, so on bottles shorter than the 60 ml it is 38, 25 and 16 mm lower, and the gripper hits the table |
| 50, 60, 100 ml, nominal | pass |
| 60 ml, yaw 90 / 180 / 270 | pass, metrics within 0.3 mm of yaw 0 (S2 holds on the pilot) |
| 60 ml, side and diagonal approach | pass |
| 60 ml, pitch +10 | `lift`: the bottle slid 6.5 mm in the pads |
| 60 ml, pitch −10 | `table` |
| 60 ml, dx +3 | `recap`: the thread ran the cap down to 1.37 mm only |
| 60 ml, dy +3 | `lift` (measured from `GRIPPED_AT`; this is what moved the slip reference to `LIFTED_AT`) |

## v2: seat the cap by torque, raise the grip with L fingertips, iris to 80°

The v1 sweep (`out/v1_original_rig.csv`, original rig, valid) raised two questions after the report was read. The answers shaped v2. All of v2 is in this directory, as in-memory changes to the shipped rig. `simulation/` is not touched until v2 is validated.

### 1. The `recap` failures were an artifact of the script

- **What happened.** In all 11 of them the thread had caught the cap again, and the cap sat 1.0–4.8 mm high.
- **Why.** The thread catches the cap where the clamp brings it back: 0.4 turns higher than where it let go, because the clamp comes down at its follow height. The script then turned the housing back exactly the 2 turns it had unscrewed.
- **What a real capper does.** It turns until the torque rises.
- **v2.** After the plan's two turns back, the housing keeps turning at the same rate, until the torque the blades put on the cap reaches `SEAT_TORQUE` = 0.10 N·m for 0.3 s, or until 1 extra turn.
  - The torque is `Trial.cap_torque`: what a reaction-torque sensor on the carrier would read.
  - The plan's clock waits meanwhile.
  - The blades slipping on the seated cap are the clutch.
- **Calibration, nominal trial only.**
  - Running freely with the clamp still: ~0.05 N·m.
  - Blades slipping on a seated cap: 0.12–0.16 N·m.
  - The detector is armed only after the plan's zero, because while the clamp still moves the running torque peaks at 0.27 N·m.
- **Rule.** The `recap` rule is unchanged: ≤ 1 mm.

### 2. The small bottles hit the table: that is real, and only partly fixable

What hits the table is the 2F-85's `base_mount`, the Ø75 disc on the tool axis, 37.5 mm below it. The tool axis is caught between two limits:

- **Table:** it must be ≥ 39.5 mm above the table.
- **Clamp:** with the clamp down on the cap, its housing reaches 2.5 mm under the cap seat, and the gripper parts inside its footprint rise 13.5 mm above the axis. So the axis must be ≤ cap seat − 18 mm.

So the cap seat must be at ≥ 57.5 mm, whatever the fingers look like.

- **10 ml** (cap seat 39.7 mm): cannot be done on the table with this architecture.
- **20 ml** (53.3 mm): cannot be done either.
- **30 ml** (61.6 mm): fits, if the axis is raised.

The v2 hand (`scene.V2`):

- **Axis raised.** The gripper's axis moves to cap − 20 mm (it was cap − 34, `GRIP_Z`), so the base clears the table 14 mm sooner.
- **L fingertips.** Each pad moves 15 mm down, on the same face plane (`scene._l_fingertips`), so the pads grip where they did: 43.1 mm up the hand frame, against 44.1 mm in v1.
- **Iris to 80°.** The stop moves from 76° to 80°, so the blades reach the PP18 (Ø21.8, 78.6°) and PP20 (Ø23.8, 77.5°) caps.
  - The squeeze stays v1's: the iris closes to the contact angle of *this* cap plus 1.18°, which is v1's stop past the PP25 contact.
  - Commanding the 80° stop with the cam's full 3 N·m squeezed the cap with ~45 N instead of ~10 N. That spun the bottle in the pads (54 mm), a change of squeeze, not of reach.
  - The robot learns the contact angle by closing until the blades stall; the script uses the cap's radius.
- **New stage `rig_clear`, after `table`:** the clamp's envelope and the pipette never touch the gripper. The raised gripper is 5 mm under the folded clamp by geometry.
- **Kept on purpose:** the approach, the carriage, the pass rules, the sanity checks and the design (A 360 + B 240, seed 0, B over 50/60/100 ml), so v1 and v2 compare trial by trial.

### A v2 sweep, thrown away: the L pads lost the gripper's contact priority

`results/invalid_v2_pad_priority.csv` is kept as evidence, not as a result.

- **What S2 saw.** Turning the hand about the bottle changed the outcome in 7 of the 18 bottle × fill groups, by as much as 92 mm. It is a symmetric problem, so that cannot be physics.
- **The bug.** `_l_fingertips` copied the pads' size, position, friction, `solref`, `solimp` and `condim`, but not `priority`. The 2F-85's pads carry `priority = 1` so that their own friction (0.7) and `solref` (4 ms) govern the contact. Without it the pair takes the maximum friction of the two geoms (the bottle's 1.0) and a mixed, stiffer `solref`.
- **What it did.** With the wrong contact parameters the grip lost the cap's seating torque: once the cap bottomed out and the housing kept turning, the bottle spun out of the pads (up to 105 mm). Whether it did depended on the contact ordering, which the yaw changes — hence S2.
- **How it was traced.** Reverting the v2 changes one at a time; with the 2F-85's own pads instead of the L copies, all four yaws passed. Then `priority` alone reproduced the difference.
- **The fix.** `_l_fingertips` now carries `priority`, `solmix`, `margin` and `gap` as well. With it, 50, 60 and 100 ml pass all four yaws within 0.1 mm, and the nominal repeats exactly.

### v2 pilot (13 trials, before the sweep)

| Trial | v1 | v2 |
| --- | --- | --- |
| 10 ml nominal | `table` | `table` (the architecture's limit) |
| 20 ml nominal | `table` | `table` (the architecture's limit). It still unscrews and recaps |
| 30 ml nominal | `table` | **pass**: the blades at 78.7° grip the PP20 cap, recap 0.22 mm |
| 50, 60, 100 ml nominal | pass | pass; seated at 0.14–0.24 N·m after 0.2–0.3 extra turns |
| 60 ml, yaw 90 / side approach | pass | pass |
| 60 ml, dx +3 | `recap` (1.37 mm) | recap 0.12 mm; now `lift` (slip 3.02 mm, 3 mm rule) |
| 60 ml, pitch +5 | `lift` | recap −0.19 mm; `lift` (slip 3.16 mm) |
| 60 ml, dy −3 | `lift` | `lift` (slip 55 mm) |
| 100 ml, fill 0.25 | `reach_liquid` | `reach_liquid` |
| every trial | — | 0 contacts clamp↔gripper and pipette↔gripper |

### What the v2 sweep found (600 trials, after the fix)

- **S1 holds** (the nominal 60 ml passes) and **S3 holds** (nothing diverged).
- **S2 fails in 3 of the 18 groups**, down from 7 before the priority fix. Each one is a threshold, and each is named:
  - **30 ml at fill 0.25 and 0.5.** The bottle spins out of the pads (51–53 mm) under the cap's seating torque, in 2 of the 4 yaws. Its radius is 15.9 mm against the 60 ml's 20, so the grip has ~20 % less torque capacity for the same torque. The 30 ml bottle sits on that limit.
  - **100 ml at fill 0.8.** The thread leaves the cap 1.06 mm high at one yaw and 0.09 mm at another: the recap rule is ≤ 1 mm, so one crosses it.
  - Neither has a harness cause: the model is deterministic (the nominal repeats exactly), and 50 and 60 ml agree across all four yaws.
- **Against v1, on the same 600 trials:** one factor at a time, 84 successes against 67; all factors at once, 4 against 3.
  - **30 ml: 0 → 14.** The raised axis and the 80° iris are what it took.
  - **60 ml: 22 → 26**, **50 ml: 36 → 37**, **100 ml: 12 → 11.**
  - The cap now seats: 186 of the 305 recaps seat by torque, the rest close inside the extra turn.
- **What v2 costs: 51 `rig_clear` failures**, all of them the pipette's body against the gripper's finger links. The gripper's axis is 14 mm higher, so its links reach into the corridor the pipette dives through. It shows up when the jaws close further than the bottle's diameter, which happens when the bottle is off-centre or has slipped.

### v2 limits

- **The 80° stop** has not been checked in CAD: blade-to-blade clearance and the cam slot.
- **The L fingertips** are rigid boxes on the pad bodies, with no compliance. The bracket is drawn, not collided.
- **The visual cheeks** stay where the v1 rig puts them (the hinge brackets on the gripper's top face). They are drawn only, so they may float by the 14 mm the gripper rose.
- **The seat detector** reads the torque on the cap directly. A real one would read it through the carrier's own friction.

## Limits

- **The liquid** is a mass and a height, not a fluid. "Reaching the liquid" is geometric. The spill margin (`liquid_to_shoulder_mm`) says how close the tilted surface comes to the shoulder.
- **The thread** is the kit's kinematic recipe, not threads in contact. When it catches the cap depends on the capture window (≤ 1 mm off the axis, ≤ 3° tilt, within the thread's travel + 1.5 mm).
- **The carriage** stands in for the arm, with no arm kinematics or reach: the approach is a direction, not a joint path.
- **The rig** is placed on the cap seat for every bottle, as the page places it. That is why the short bottles fail at the table. It is the shipped layout, not a new one.
