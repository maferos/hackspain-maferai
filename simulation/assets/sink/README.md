# sink

Detailed procedural lab sink, **1.502 × 0.754 m**, worktop at **0.92 m**.
Includes a tapered rounded basin, rolled rim, ribbed drainboards, backsplash,
strainer, gooseneck mixer tap with aerator, waste trap, frame and leveling feet.

Regenerate the active MJCF asset from `simulation/`:

```bash
python scripts/generate_sink.py
```

The generator shares the room's material palette and beveled visual geometry.
The basin has separate wall and floor colliders, leaving its opening accessible.
Frame and worktop use simple colliders; small fittings are visual only.
The original vendor archive and `part_*.obj` meshes are retained as reference;
`convert_3ds.py` is no longer the generator for the active `sink.xml`.

## Frame convention

Origin on the floor, centred in X and Y, +Z up. Place it at `z = 0`.

## Files

| File | Purpose |
| --- | --- |
| `sink.xml` | Generated MJCF: detailed visuals and separate frame / basin colliders |
| `part_00.obj` … `part_05.obj` | Original vendor meshes, retained as reference |
| `3d-model.3ds.zip` | Vendor source |

`sink.xml` has a single `sink` body, so attach it (not `<include>`) to place several:

```xml
<asset><model name="sink" file="../assets/sink/sink.xml"/></asset>
...
<frame pos="4.051 0 0"><attach model="sink" body="sink" prefix="right_"/></frame>
```

See `models/minihannover_scene.xml`.
