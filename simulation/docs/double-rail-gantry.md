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

This is a mechanical prototype. The existing UR10e scan planner, which assumes
six rotary joints and an orientable wrist camera, does not drive this model.
The hand camera has fixed orientation. Automated scanning needs a Cartesian
path planner and a compatible camera strategy. XYZ positioning alone is not
an obstacle-avoidance planner; the full work envelope has not been collision
validated against room equipment. Current View and recorded Replay videos
continue using their existing scenes.
