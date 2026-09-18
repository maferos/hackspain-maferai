# minihannover

A lab bench: **6.0 m (X) × 1.5 m (Y)**, work surface **0.90 m** above the floor.

All files here are generated from one source of truth,
[`scripts/generate_minihannover.py`](../../scripts/generate_minihannover.py) — edit the
constants at the top of that script and re-run it rather than editing these files:

```bash
python scripts/generate_minihannover.py
```

## Frame convention

Shared by every file below: origin **on the floor**, centred in X and Y, +X along
the length, +Z up. So the asset can be dropped at `z = 0` on any ground plane and
the work surface is at `z = 0.90`.

## Files

| File | Purpose |
| --- | --- |
| `minihannover.xml` | MJCF, boxes only — no external files, loads and `<include>`s anywhere |
| `minihannover_mesh.xml` | MJCF, mesh visual + box collision (the usual MuJoCo split) |
| `minihannover.urdf` | URDF for the Isaac Lab / Isaac Sim importer |
| `minihannover.obj` / `.mtl` | Interchange mesh, metres, referenced by both of the above |

Both MJCF variants and the URDF describe the *same* seven boxes: one worktop slab
plus three pairs of legs (a 6 m top needs the mid support). Collision is always box
primitives — never the mesh — because a table is non-convex and a convex hull of it
would be a solid block.

Mass is 355.8 kg (worktop 700 kg/m³, legs 800 kg/m³); the URDF carries the exact
composite inertia about the centre of mass at `z = 0.823`.

## MuJoCo

```bash
python scripts/view_model.py models/minihannover_scene.xml   # bench on a floor
python scripts/view_model.py assets/minihannover/minihannover_mesh.xml
```

To place it in your own scene:

```xml
<include file="../assets/minihannover/minihannover.xml"/>
```

The body has **no joint**, so it is welded to the world — what you want for a bench.
Add a `<freejoint/>` inside the `<body>` to make it a movable rigid body instead.

Use `minihannover.xml` (boxes) for anything you `<include>`: MuJoCo resolves `meshdir`
relative to the *main* model file, so `minihannover_mesh.xml` only finds `minihannover.obj`
when it is itself the main file, or when the including scene sets
`<compiler meshdir="../assets/minihannover"/>`.

## Isaac Lab

Import the URDF and convert it to USD:

```bash
# Isaac Lab's converter (writes minihannover.usd next to the URDF)
python scripts/tools/convert_urdf.py \
    assets/minihannover/minihannover.urdf minihannover.usd --fix-base
```

Then reference it from a scene config:

```python
from isaaclab.assets import RigidObjectCfg
from isaaclab.sim import UsdFileCfg

bench = RigidObjectCfg(
    prim_path="{ENV_REGEX_NS}/Minihannover",
    spawn=UsdFileCfg(usd_path="<...>/minihannover.usd"),
)
```

Use `--fix-base` (or `articulation_props`/a static collider) so the bench is anchored:
the URDF is a single fixed link with no joints, matching the MuJoCo model.

Isaac Sim can also import `minihannover.obj` directly if you only need the visual
mesh, and Isaac Lab ships a MJCF importer that reads `minihannover.xml` as well.
