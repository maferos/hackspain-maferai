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

## Seeded flask patterns

The bench above is one crowd: every catalogue flask, scattered with seed 29.
That is a single distribution, and anything trained or demoed on it only ever
sees that one. A **pattern** is a whole worktop layout derived from one integer
(`scripts/bottle_patterns.py`):

| Drawn from the seed | Range |
| ------------------- | ----- |
| How many flasks stand on the bench | 10 – 75 |
| Spacing between footprints | 4 – 60 mm |
| Layout style | `scatter`, `clusters`, `rows`, `crowd` (everything in one stretch) |
| Stretch of the strip used, and where it sits | 22 – 100 % of 4.32 m |
| Size mix | weights over the five flask classes, 10 – 100 ml |

Yaw stays fully random, as it always was: nothing about a bottle's facing says
what it is. Flasks keep their catalogue identity — a pattern draws a *class* by
its size mix and then takes an unused sample of that class, so every bottle on
the bench is still a uniquely barcoded sample.

Ten patterns are catalogued, chosen so the counts and the spacings spread out
and all four styles appear (`bottle_patterns.py --search` re-runs that walk):

| Pattern | Seed | Flasks | Style | Spacing | Stretch of bench used |
| ------- | ---- | ------ | ----- | ------- | --------------------- |
| `p01` | 30 | 16 | scatter | 28 mm | 2.56 m (x = -1.14 … 1.42) |
| `p02` | 176 | 24 | crowd | 12 mm | 1.88 m (x = 0.02 … 1.90) |
| `p03` | 21 | 29 | crowd | 38 mm | 1.66 m (x = -2.42 … -0.76) |
| `p04` | 327 | 35 | rows | 17 mm | 3.51 m (x = -2.42 … 1.09) |
| `p05` | 1 | 41 | rows | 57 mm | 2.66 m (x = -0.76 … 1.90) |
| `p06` | 31 | 46 | crowd | 8 mm | 1.62 m (x = -1.19 … 0.43) |
| `p07` | 70 | 52 | clusters | 45 mm | 3.00 m (x = -1.10 … 1.90) |
| `p08` | 4 | 57 | crowd | 33 mm | 1.92 m (x = -2.42 … -0.50) |
| `p09` | 2 | 65 | clusters | 21 mm | 3.96 m (x = -2.42 … 1.54) |
| `p10` | 15 | 71 | rows | 50 mm | 3.05 m (x = -2.42 … 0.63) |

Same seed, same bench, down to the millimetre. Spacing is what the seed asked
for; if a crowd cannot fit, it is relaxed in steps and the population file
records what was actually reached (`gap_m` against `gap_requested_m`).

```bash
python scripts/bottle_patterns.py --list                      # the ten
python scripts/bottle_patterns.py --seed 314                  # any other seed
python scripts/generate_minihannover_open.py --all-patterns   # rewrite patterns/*.json
python scripts/generate_minihannover_open.py --pattern p06    # build that scene
python scripts/generate_minihannover_open.py --pattern s314   # ... or an off-catalogue seed
mjpython scripts/view_model.py models/minihannover_open_scene_p06.xml
```

`patterns/<name>.json` is the definition and is committed: the same schema as
`population.json` plus the pattern's own header. The room and scene XML a seed
expands into (`lab_room_p06.xml`, `models/minihannover_open_scene_p06.xml`) are
generated files, gitignored, and cost about a fifth of a second to rebuild. The
default build is untouched — no flags means the same 187-flask bench as before,
byte for byte.

From `simulation/`:

```bash
python scripts/generate_minihannover_open.py
mjpython scripts/view_model.py models/minihannover_open_scene.xml  # macOS
# Linux: use python instead of mjpython
```

Generated files are `bench.xml`, `lab_room.xml`, `population.json`,
`patterns/*.json` and `models/minihannover_open_scene.xml`. Shared props reference the original room's
meshes. Regenerate this variant after updating the source scene or room builders.

Named cameras: `room_entrance`, `room_aisle`, `room_desk`, `room_wash`,
`room_overview`, `general` and `wrist`. Hide geom group 2 to inspect the room from
above. The fixed general camera preserves its calibration; the wrist camera
preserves its pose relative to the second loose bottle. This variant does not
change the computer-vision package's default scene or hard-coded bench bounds;
consumers must select this XML and use its new worktop bounds (X: -4.5 to 1.5,
Y: -1.4 to 0.6).
