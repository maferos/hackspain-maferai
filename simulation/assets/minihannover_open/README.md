# MiniHannover open desk

A separate scene variant with a **6.0 × 2.0 m** worktop at **0.90 m**, centered
at **(-1.5, -0.4, 0)**, the midpoint of the original room's interior bounds.
The original MiniHannover scene and its assets remain unchanged.

The central gantry, divider, splash glass and 187 shelf-mounted sample bottles
are omitted. The wall storage rack and wash-zone drying rack remain. All thirteen
hand-placed samples remain, including seven movable bottles on the desk.

The desk's worktop, legs, cabinet fronts and edge trim use the increased width.
Desk props, balances, mats, ceiling extraction arms, sink and wrist camera move
with the desk; the sink retains its own dimensions and stays centered on the desk's
end. Room walls and perimeter furniture retain their original positions. Clearance
between the worktop and adjacent wall worktops is about 0.75 m on +Y and 0.78 m on -Y.

From `simulation/`:

```bash
python scripts/generate_minihannover_open.py
mjpython scripts/view_model.py models/minihannover_open_scene.xml  # macOS
# Linux: use python instead of mjpython
```

Generated files are `bench.xml`, `lab_room.xml` and
`models/minihannover_open_scene.xml`. Shared props reference the original room's
meshes. Regenerate this variant after updating the source scene or room builders.

Named cameras: `room_entrance`, `room_aisle`, `room_desk`, `room_wash`,
`room_overview`, `general` and `wrist`. Hide geom group 2 to inspect the room from
above. The fixed general camera preserves its calibration; the wrist camera
preserves its pose relative to the second loose bottle. This variant does not
change the computer-vision package's default scene or hard-coded bench bounds;
consumers must select this XML and use its new worktop bounds (X: -4.5 to 1.5,
Y: -1.4 to 0.6).
