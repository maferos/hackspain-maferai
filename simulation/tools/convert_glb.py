#!/usr/bin/env python3
"""Convert a glTF binary (.glb) model into MuJoCo-ready meshes + an MJCF body.

MuJoCo can't read glTF. This walks the default scene's node tree (matrix or TRS per
node), keeps triangle primitives, splits the result into one mesh per material (a
MuJoCo mesh has a single colour), turns glTF's +Y up into +Z up and merges vertices
that share a position, so a mesh the exporter split along UV or normal seams is
closed again. Unlike the .3ds/.dae converters it keeps the source origin, because
our procedural kits already put it at the bottom-centre. Textures are ignored: a
material keeps its baseColorFactor, and glass (KHR_materials_transmission) gets an
alpha of 1 - 0.5 * transmission. Writes <out>/<name>_NN.obj and <out>/<name>.xml.

The meshes use inertia="exact": the kits are thin-walled (hollow bottles, caps), and
MuJoCo's default treats a closed mesh as solid, e.g. 446 g instead of 60 g for the
60 ml amber bottle.

    python tools/convert_glb.py ../assets/amber-bottles/glb/amber_bottle_060ml.glb \
        --name amber_060ml --out assets/amber_bottles --density 2500
"""
from __future__ import annotations

import argparse
import json
import struct
from collections import defaultdict
from pathlib import Path

import numpy as np

COMPONENTS = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
DTYPES = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
Y_UP_TO_Z_UP = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float)


class Glb:
    def __init__(self, path: Path):
        buf = path.read_bytes()
        magic, _, _ = struct.unpack_from("<III", buf, 0)
        if magic != 0x46546C67:
            raise SystemExit(f"{path}: not a binary glTF file")
        n, _ = struct.unpack_from("<II", buf, 12)
        self.json = json.loads(buf[20:20 + n])
        m, _ = struct.unpack_from("<II", buf, 20 + n)
        self.bin = buf[28 + n:28 + n + m]

    def accessor(self, i):
        acc = self.json["accessors"][i]
        view = self.json["bufferViews"][acc["bufferView"]]
        width = COMPONENTS[acc["type"]]
        dtype = np.dtype(DTYPES[acc["componentType"]])
        start = view.get("byteOffset", 0) + acc.get("byteOffset", 0)
        stride = view.get("byteStride", width * dtype.itemsize)
        rows = np.ndarray((acc["count"], width), dtype, self.bin, start, (stride, dtype.itemsize))
        return rows.astype(float) if dtype == np.float32 else rows.astype(np.int64)

    def colour(self, material):
        if material is None:
            return np.array([0.7, 0.7, 0.7, 1.0]), "default"
        mat = self.json["materials"][material]
        rgba = np.array(mat.get("pbrMetallicRoughness", {}).get("baseColorFactor", [1.0, 1.0, 1.0, 1.0]), float)
        transmission = mat.get("extensions", {}).get("KHR_materials_transmission", {}).get("transmissionFactor", 0)
        rgba[3] = min(rgba[3], 1 - 0.5 * transmission)
        return rgba, mat.get("name", f"material_{material}")

    def walk(self, index, parent):
        node = self.json["nodes"][index]
        local = np.eye(4)
        if "matrix" in node:
            local = np.array(node["matrix"], float).reshape(4, 4).T  # glTF is column-major
        else:
            t = np.eye(4)
            t[:3, 3] = node.get("translation", [0, 0, 0])
            x, y, z, w = node.get("rotation", [0, 0, 0, 1])
            r = np.eye(4)
            r[:3, :3] = [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                         [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                         [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]
            s = np.diag([*node.get("scale", [1, 1, 1]), 1])
            local = t @ r @ s
        world = parent @ local
        if "mesh" in node:
            yield node.get("name", f"node_{index}"), world, self.json["meshes"][node["mesh"]]
        for child in node.get("children", []):
            yield from self.walk(child, world)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("src", type=Path)
    p.add_argument("--name", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--density", type=float, default=1000.0, help="kg/m^3 of the wall material (default 1000)")
    p.add_argument("--skip-material", nargs="*", default=[], help="drop primitives with these material names")
    args = p.parse_args()

    glb = Glb(args.src)
    scene = glb.json["scenes"][glb.json.get("scene", 0)]
    parts = defaultdict(list)  # material index -> [(vertices, faces)]
    for root in scene["nodes"]:
        for _, world, mesh in glb.walk(root, Y_UP_TO_Z_UP):
            for prim in mesh["primitives"]:
                if prim.get("mode", 4) != 4:  # triangles only
                    continue
                v = glb.accessor(prim["attributes"]["POSITION"])
                f = (glb.accessor(prim["indices"]).reshape(-1, 3) if "indices" in prim
                     else np.arange(len(v)).reshape(-1, 3))
                v = v @ world[:3, :3].T + world[:3, 3]
                if np.linalg.det(world[:3, :3]) < 0:
                    f = f[:, ::-1]
                parts[prim.get("material")].append((v, f))

    args.out.mkdir(parents=True, exist_ok=True)
    assets, geoms, lo, hi = [], [], np.full(3, np.inf), np.full(3, -np.inf)
    for i, (mat, pieces) in enumerate(sorted(parts.items(), key=lambda kv: (kv[0] is None, kv[0]))):
        rgba, name = glb.colour(mat)
        if name in args.skip_material:
            continue
        offs = np.cumsum([0] + [len(v) for v, _ in pieces[:-1]])
        v = np.vstack([v for v, _ in pieces])
        f = np.vstack([f + o for (_, f), o in zip(pieces, offs)])
        # Merge seam duplicates (positions equal to 0.01 mm), then drop degenerate faces.
        _, first, inverse = np.unique(np.round(v, 5), axis=0, return_index=True, return_inverse=True)
        v, f = v[first], inverse.reshape(-1)[f]
        f = f[(f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2])]
        lo, hi = np.minimum(lo, v.min(0)), np.maximum(hi, v.max(0))
        fname = f"{args.name}_{i:02d}.obj"
        with (args.out / fname).open("w") as out:
            out.writelines(f"v {x:.6f} {y:.6f} {z:.6f}\n" for x, y, z in v)
            out.writelines(f"f {a + 1} {b + 1} {c + 1}\n" for a, b, c in f)
        r, g, b, a = rgba
        assets.append(f'    <mesh name="{args.name}_{i:02d}" file="{fname}" inertia="exact"/>')
        geoms.append(f'      <geom type="mesh" mesh="{args.name}_{i:02d}" rgba="{r:.3f} {g:.3f} {b:.3f} {a:.3f}"'
                     f' density="{args.density:g}"/>  <!-- {name} -->')

    size = hi - lo
    xml = f"""<!-- Generated by tools/convert_glb.py from {args.src.name}; size {size[0]:.3f} x {size[1]:.3f} x {size[2]:.3f} m.
     Source origin kept (bottom-centre for our kits), +Z up. Mesh geoms collide (convex hull) and carry the mass. -->
<mujoco model="{args.name}">
  <asset>
{chr(10).join(assets)}
  </asset>
  <worldbody>
    <body name="{args.name}">
{chr(10).join(geoms)}
    </body>
  </worldbody>
</mujoco>
"""
    (args.out / f"{args.name}.xml").write_text(xml)
    print(f"{args.name}: {len(assets)} meshes, size {size.round(3)} m -> {args.out}")


if __name__ == "__main__":
    main()
