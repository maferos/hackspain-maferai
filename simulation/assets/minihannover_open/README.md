# MiniHannover open desk

A separate scene variant with a **6.0 × 2.0 m** worktop at **0.90 m**, centered
at **(-1.5, -0.4, 0)**, the midpoint of the original room's interior bounds.
The original MiniHannover scene and its assets remain unchanged.

The central gantry, divider and splash glass are omitted. As of catalogue
version 6 the catalogue is **200 liquid samples** (`SMP-0001..SMP-0200`, all
amber flasks, each with a distinct `DICT_4X4_250` ArUco marker). The **187
former shelf samples** stand in a randomly scattered center stock area; there
are **no blank reserve vials and no powder jars** — every bottle on the bench is
a uniquely-labelled catalogue sample. With the thirteen hand-placed samples the
bench carries all **200 distinct labels**. Samples retain their catalogue sizes
(10–100 ml) and barcode identity.

Positions and rotations are deterministic (seed 29), with at least 9 mm between
container footprints. `population.json` records each container's size and local
position. Stock is fixed to the table with simple cylinder collision proxies, as
it was fixed on the original shelves; the seven loose work samples remain movable.
The wall storage rack, drying rack and all thirteen hand-placed samples remain.

The desk's worktop, legs, cabinet fronts and edge trim use the increased width.
Desk props, balances, mats, ceiling extraction arms, sink and wrist camera move
with the desk. The balances, mats, side work tools and loose work samples move
another 0.25 m outward on each side; the balances are centered 0.24 m inside the
long edges. The wrist camera follows its target bottle. Stock occupies local
X = -2.42 to 1.90 m, Y = -0.43 to 0.43 m, leaving the work stations and wash zone clear;
 the sink retains its own dimensions and stays centered on the desk's
end. Room walls and perimeter furniture retain their original positions. Clearance
between the worktop and adjacent wall worktops is about 0.75 m on +Y and 0.78 m on -Y.

From `simulation/`:

```bash
python scripts/generate_minihannover_open.py
mjpython scripts/view_model.py models/minihannover_open_scene.xml  # macOS
# Linux: use python instead of mjpython
```

Generated files are `bench.xml`, `lab_room.xml`, `population.json` and
`models/minihannover_open_scene.xml`. Shared props reference the original room's
meshes. Regenerate this variant after updating the source scene or room builders.

Named cameras: `room_entrance`, `room_aisle`, `room_desk`, `room_wash`,
`room_overview`, `general` and `wrist`. Hide geom group 2 to inspect the room from
above. The fixed general camera preserves its calibration; the wrist camera
preserves its pose relative to the second loose bottle. This variant does not
change the computer-vision package's default scene or hard-coded bench bounds;
consumers must select this XML and use its new worktop bounds (X: -4.5 to 1.5,
Y: -1.4 to 0.6).
