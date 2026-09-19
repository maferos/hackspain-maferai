# Pipetting on the rail bench — plan

> **Status, 2026-09-19: the MVP runs.** Steps 1, 3, 4, 5 and 7 are done and
> `scripts/pipette_test.py` transfers 12 of 12. Step 2 was deliberately skipped
> in favour of contact exclusions --- see *What the MVP does instead* below.
> Step 6 is the beaker-on-the-bench version.

Target: **the arm draws liquid from an open flask on the bench and dispenses it
into a container that is weighed.** Written 2026-09-19 against
`models/minihannover_rail_scene.xml` at the state where 12 vessels are liftable
and the gripper reports its own grasps.

Four decisions are already taken and everything below assumes them:

| | |
| --- | --- |
| Pipette | fixed tool on the flange, replacing the 2F-85 |
| Liquid | a visual level plus bookkeeping, not particles |
| Destination | a container that gets weighed on a balance |
| Tips | fixed, no disposable tips and no tip rack |

## What the scene already has

* Flasks with a **real neck**: the `flask_*_glass` meshes are hollow, outer
  Ø 24 mm at the neck, **bore Ø 18.4 mm**, 15 mm tall, sitting on a shoulder
  that tapers from Ø 37.6 mm. A pipette tip of Ø 5 mm goes in with room to
  spare.
* A **cap as its own mesh geom** (Ø 30.2 mm, 18.5 mm tall), rigidly part of the
  vessel body. Deleting it is one line; unscrewing it is a separate job and is
  deliberately out of this plan.
* Capacities per vessel in `assets/labelled_bottles/manifest.json`
  (`container_ml`, `diameter_m`, `height_m`), which is what fill levels have to
  respect.
* A `beaker.obj` mesh in `assets/lab_room/meshes/` --- 100 mm tall, Ø 76 mm,
  open at the top --- which is the obvious receiving container.
* Five balances, and an arm that reaches the two on the back strip easily.

## What is missing, and where it comes from

| Missing | How to get it |
| --- | --- |
| **A pipette** | Generate it procedurally, the way `generate_wrist_camera.py` builds the camera: body, finger hook, plunger, ejector, cone and a fixed tip. No mesh conversion, no download. |
| **A mouth the tip can enter** | MuJoCo collides meshes as their **convex hull**, so every vessel is a solid lump today: a 3 mm sphere dropped on the axis of a 89.5 mm flask rests at 92 mm. The single mesh collider has to be replaced by a ring of convex pieces. |
| **Liquid** | Does not exist in any form. A cylinder geom inside each vessel, non-colliding, whose height is the volume, plus the numbers behind it. |
| **A receiving container** | Convert `beaker.obj` into a standalone model under `assets/beaker/`, the way `assets/sink/` and `assets/balance/` were done. |
| **A balance pan** | The balances collide as **one solid box** 1.21 m tall with no pan and no opening --- see the open question at the end. |

## The steps

Each step is meant to end somewhere the scene still loads and something is
measurably better.

### 1. Open the vessels

Drop the `cap` geom when the rail scene thins the bench. One line in
`build_bench`, and the flasks are open.

*Done when:* a ray straight down the axis of every vessel reaches the inside of
the flask instead of stopping on a cap.

### 2. Give the vessels a mouth

Replace each vessel's convex mesh collider with a small set of convex pieces:
a ring of 8 to 12 boxes for the body wall, a ring for the neck at radius
~10.7 mm, and a disc for the floor. The bore stays open, the outside still
collides, and the arm still cannot reach through a bottle.

Costs ~20 collision geoms per vessel, so ~240 over the twelve. Worth watching
the contact count and the step rate; the scene runs at about 11x realtime now.

*Done when:* the sphere-drop test falls to the bottom of the flask instead of
resting on the rim, and `grasp_test.py` still scores 12/12 --- the outside has
not changed.

### 3. Put liquid in them

A `liquid` cylinder geom per vessel, `contype=0 conaffinity=0`, coloured, its
radius the flask's inner radius and its height set from the volume. Fill levels
drawn from a seeded RNG at a fraction of each vessel's `container_ml`, so a
10 ml flask never holds 40 ml and the scene is reproducible.

The bookkeeping lives beside it: a volume per vessel in millilitres, and a
density so a volume can become a mass for the balance.

*Done when:* every vessel shows a level that matches its catalogue capacity,
and the numbers survive a reload.

### 4. Build the pipette and put it on the flange

Procedural, in the scene's own palette, mounted where the 2F-85 is now. The
tool frame moves to the tip, so `TCP_SITE` becomes the tip rather than the
gripper's pinch point, and `rail_reach.py` and the IK keep working unchanged.

The eye-in-hand camera stays where it is and keeps looking down the tool axis,
which is what makes the insertion watchable.

*Done when:* the reach report runs against the tip and the wrist camera shows
the tip over a flask mouth.

### 5. Insert, aspirate, dispense

The motion: over the mouth, down the bore to a depth that stays under the
liquid surface, aspirate, withdraw, travel, dispense into the beaker.

Aspiration and dispensing are state changes gated on geometry: the tip has to
be inside the bore and below the surface, checked from the simulation rather
than assumed. That is the part worth having --- it is what tells us when the
approach is wrong.

*Done when:* a `pipette_test.py` mirroring `grasp_test.py` runs the full cycle
on every vessel and reports how many transfers landed, with the volumes before
and after.

### 6. Weigh it

The beaker's contents become a mass, and the mass is reported. See the open
question.

### 7. Show it

`wrist_view.py --mode pipette`: the same two views and telemetry panel, with
the gripper rows replaced by tip depth, volume in the pipette, volume in the
source and the dispensed mass.

## Risks worth knowing now

* **The bore is 18.4 mm and the servos settle to a few millimetres.** That is
  comfortable, but only after the pose settles: reading the tool before it has
  caught up gave errors of 20 to 47 mm earlier in this work. Insertion has to
  wait for the settle, the same as the grasp does.
* **Headroom over the balances.** The gantry beam's underside is at 1.36 m and
  the balances top out at 1.21 m. A beaker on top of one leaves very little
  room for a pipette above it. Measure before committing to a position.
* **Contact count.** Hollowing twelve vessels adds a few hundred collision
  geoms. If the step rate drops too far, hollow only the vessels being
  pipetted from and leave the rest convex.

## Open question: what the liquid is weighed in, and on

The balances in the scene are **a single solid collision box** 1.21 m tall.
There is no pan and no opening, so nothing can be put "on the balance" as the
model stands. Three ways out, in increasing cost:

1. **Beaker on the bench beside the balance**, mass reported in the telemetry
   panel. Nothing new to model, and the pipetting story is complete; the
   weighing is notional.
2. **Give one balance a real pan**: split its collision into a base, the shield
   walls and a pan surface at the right height, so a beaker can stand inside.
   Asset surgery on `assets/balance/`, and the draft shield has to be open
   enough for a pipette to come down.
3. **Model a simple open pan balance** as a new asset and stand it on the
   bench. Clean geometry, no shield in the way, but it is another asset and the
   scene already has five balances that would then look inconsistent.

Recommendation: **1 to get the cycle working end to end, then 2**. The pan is
independent of everything in steps 1 to 5 and should not block them.


## What the MVP does instead of step 2

Hollow collision shells were not built. The tip body is excluded from contact
with the vessels and the beaker instead, so it travels down a bore while the
barrel above it still collides with everything. It costs no geometry and no
step rate, and the alignment it gives up is measured and reported by
`pipetting.entry()` rather than enforced by contact.

The consequence to know: **a badly aimed tip passes through the glass instead
of striking the rim.** The refusal to aspirate still fires, so a miss is
visible, but it is a number rather than a collision. Hollowing is the fix when
fidelity matters more than speed.

## What the MVP measures

```
12 open flasks holding 250.8 ml between them; tip radius 2.7 mm
transferred: 12/12
beaker now holds 6.08 ml = 5.53 g at 0.91 g/ml
tip alignment: 1.1 mm mean, 1.5 mm worst
```

Two geometry problems that only showed up once it ran, both fixed:

* **The cone jammed in the neck.** With a 56 mm tip, the cone above it --- 11.6
  mm across --- sat level with a 12 mm bore while the tip was down at the
  liquid, wedged, and stopped the arm on four flasks. The tip is 125 mm now,
  which is what a real 1000 ul tip is anyway.
* **Aiming just under the surface left the tip above it.** The servos land
  within a few millimetres, which is the same order as "2 mm below the
  surface". Aiming a quarter of the way down the column removes the failure
  mode and costs nothing.

## Next, in order

1. Hollow the vessels properly, so a miss is a collision rather than a number.
2. Give a balance a real pan and stand the beaker on it.
3. Tip racks and disposable tips, if the demo wants the full lab cycle.
4. Unscrewing caps, which is independent of all of the above.
