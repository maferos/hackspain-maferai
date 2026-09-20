# Double-rail gantry

The XYZ prototype mounts Eki's `vertical_hand_minimal` directly beneath a
vertical slide. Two longitudinal rails support a transverse moving bridge.
The UR10e is absent; the bench, vessels and balance covers retain their source
scene configuration.

Generate and compile it from the repository root:

```sh
simulation/.venv/bin/python simulation/scripts/generate_gantry_scene.py
```

Output: `simulation/models/minihannover_gantry_scene.xml`. Cameras: `general`,
`gantry_overview`, and the hand-mounted `arm_eih`.

The bridge travels 6 m along X; its carriage travels 1.9 m along Y; the vertical
slide travels 0.63 m. At home, the pinch site is at (-1.394, -0.4, 1.5751) m.
`gantry_motion.move_to(model, data, target)` positions that site in world XYZ
and rejects targets outside travel before changing joint positions or controls.
The original hand actuator still controls the jaws.

The model compiles and has been checked for Cartesian target accuracy, travel
limit rejection, unwanted guide contacts at home, and finite state over 250
physics steps. Joint-constrained mating guide surfaces are excluded from mutual
collision. Other objects still collide.

View now uses this MuJoCo machine by default. `VIEW_MACHINE=arm` selects the
previous UR10e scene. Both global and hand camera streams use the same gantry
state. The hand camera is mounted on a physical bracket and looks down at 45
degrees, at 1920 × 1080, to read the vessels' lateral marker rings. The global
camera sits below the front rail to retain a clear survey of the bench.

For native MuJoCo inspection and manual joint controls on macOS:

```sh
simulation/.venv/bin/mjpython simulation/scripts/view_gantry.py --pattern p01
```

Use the viewer's Control panel for `gantry_x`, `gantry_y`, `gantry_z` and the
hand's finger actuator. Native manual controls are direct joint controls and
do not run the automated path checker.

`view/backend/gantry_scan.py` drives the XYZ position servos from YOLO proposals
and reads identities through the existing marker reader. It raises the hand,
translates, then lowers, checking each path at 1 cm intervals against MuJoCo
contacts before execution. Unexpected external contacts stop the controller.
The p01 integration run detected seven vessels and reported seven identities
in 36.7 simulated seconds. This is a scan result, not validation of every seed
or of marker localization accuracy.

Automated manipulation and dispensing are not configured for the gantry.
The whole work envelope has not been validated against every room obstacle;
unreachable or blocked scan views are reported instead of forcing a move.
Recorded Replay videos still show their previously rendered machines.
