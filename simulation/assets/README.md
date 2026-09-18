# Assets: what works in MuJoCo and in Isaac Lab

Inventory of the 3D assets in this repo and which simulator can actually consume
each one. Everything below marked *verified* was loaded with **MuJoCo 3.13.0**
(the pinned `.venv`) on 2026-09-18; the Isaac Lab column is from the importer's
documented format support and has **not** been executed on this machine.

## Format support

| Format | MuJoCo | Isaac Lab / Isaac Sim |
| --- | --- | --- |
| `.xml` (MJCF) | Native | Via the MJCF importer |
| `.urdf` | Native (URDF subset) | Via the URDF importer → USD |
| `.usd` / `.usda` | No | Native |
| `.obj` | Yes, meshes only | Yes, via the asset importer |
| `.stl` | Yes, **binary only, max 200 000 faces** | Yes |
| `.dae` (COLLADA) | **No** — "no decoder found" | Yes |
| `.fbx` | **No** | Yes |
| `.3ds`, `.max`, `.skp`, `.wrl`, `.igs` | **No** | **No** (need conversion in a DCC tool first) |

MuJoCo also reads its own binary `.msh`. Neither simulator collides against a raw
concave mesh usefully: MuJoCo takes the convex hull, Isaac Sim needs an explicit
convex-decomposition approximation. Model collision with primitives where you can.

## Inventory

| Asset | Usable in MuJoCo | Usable in Isaac Lab | Notes |
| --- | --- | --- | --- |
| [`minihannover/`](minihannover/) | **Yes** — `minihannover.xml`, `minihannover_mesh.xml` | **Yes** — `minihannover.urdf` | Our 6.0 x 1.5 m bench. Purpose-built, metres, box collision. Verified. |
| `gc-ms/` | Only after merging groups (see below) | Via `.obj` / `.fbx` | GC-MS instrument. Scale unknown. |
| `uv-vs-nr/` | Only after merging groups (see below) | Via `.obj` / `.dae` / `.fbx` | UV-Vis-NIR spectrophotometer. Scale unknown. |
| `../third_party/AutoBio` | Yes — MJCF scenes, MuJoCo **3.3.0** + its Linux plugin | Not usable as-is (the plugin is MuJoCo-specific) | Git submodule, not fetched yet; see the main README. |

`minihannover` is the only asset here that is ready to drop into either simulator
without preparation. The two instrument folders are raw vendor downloads.

## Working with the instrument models

The two instrument folders each hold the same model exported in nine or ten
formats, one zip per format. Only `.obj` (+ `.mtl`) and `.stl` are worth
unzipping; the rest need a DCC round-trip.

### MuJoCo imports only the first `g` group of an OBJ — verified

Both instrument OBJs are multi-group, so loading them straight into MuJoCo
silently drops almost all of the geometry:

| File | Face lines in the OBJ | Faces MuJoCo keeps | After stripping `g` lines |
| --- | --- | --- | --- |
| `gc-ms/3d-model.obj` | 185 754 (359 groups) | **204** | 368 717 |
| `uv-vs-nr/3d-model.obj` | 5 761 (2 groups) | **5 180** | 11 213 |

The model still loads without an error, which is what makes this easy to miss.
Merge the groups before use:

```bash
unzip -o gc-ms/3d-model.obj.zip -d /tmp/gcms
grep -v '^g ' /tmp/gcms/3d-model.obj > /tmp/gcms/gc-ms.obj   # one group, all faces
```

Split it into per-group meshes instead if you want separate movable parts.

### The STL exports are over MuJoCo's limit

`3d-model.stl` is a valid 368 717-triangle binary STL, but MuJoCo's STL decoder
rejects anything above 200 000 faces:

```
stl_decoder: number of faces should be between 1 and 200000
```

Use the merged OBJ (no such cap — 368 717 faces load fine) or decimate the mesh.
Isaac Sim has no equivalent limit, but a 369k-triangle visual mesh is worth
decimating anyway.

### The `.skp`, `.stl` and `.wrl` zips are duplicated between the two folders

`gc-ms/` and `uv-vs-nr/` ship **byte-identical** `3d-model.skp.zip`,
`3d-model.stl.zip` and `3d-model.wrl.zip` (same MD5). The other formats differ and
carry different export dates (19 Nov 2015 for GC-MS, 9 Sep 2015 for UV-Vis), so
these three in `uv-vs-nr/` are almost certainly the GC-MS files copied in by
mistake. **Do not trust `uv-vs-nr/3d-model.{skp,stl,wrl}.zip`** — use its `.obj`
or `.dae`, or re-download.

### Scale is unknown

Neither folder carries unit metadata. Measured extents of the merged meshes:

| Asset | Bounding box (model units) |
| --- | --- |
| `gc-ms` | 30 669 x 31 809 x 17 991 |
| `uv-vs-nr` | 25.7 x 31.4 x 40.8 |

Neither is metres. Check one known real dimension of the instrument before
placing it next to `minihannover`, then set the scale explicitly — MJCF:

```xml
<mesh name="gcms" file="gc-ms.obj" scale="0.001 0.001 0.001"/>
```

and `<mesh filename="..." scale="..."/>` in URDF, or the scale field of the Isaac
Sim importer.

### Provenance

Neither instrument folder contains a license or source file. Confirm where they
came from and under what terms before using them outside the hackathon.

## Reproducing these checks

```bash
python scripts/generate_minihannover.py   # regenerate the bench
python scripts/check_install.py           # MuJoCo sanity check
```

The instrument findings above come from loading each mesh in a one-geom MJCF and
reading back `mesh_vertnum` / `mesh_facenum`.
