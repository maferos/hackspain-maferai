#!/usr/bin/env python3
"""Convert a COLLADA (.dae) model into MuJoCo-ready meshes + an MJCF body.

MuJoCo can't read .dae. This walks the visual scene (node matrices, nested nodes,
instance_geometry), keeps the <triangles>/<polylist> primitives (SketchUp's edge
<lines> are dropped), splits the result into one mesh per material (a MuJoCo mesh has
a single colour), converts to metres via <unit>, turns Y-up into Z-up, centres it in
XY and rests it on z = 0. Writes <out>/part_NN.obj and <out>/<name>.xml.

    python tools/convert_dae.py model.dae --name balance --out assets/balance
"""
from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import numpy as np

NS = "{http://www.collada.org/2005/11/COLLADASchema}"


def floats(el):
    return np.array(el.text.split(), float) if el is not None and el.text else np.zeros(0)


class Dae:
    def __init__(self, path: Path):
        self.root = ET.parse(path).getroot()
        self.ids = {e.get("id"): e for e in self.root.iter() if e.get("id")}
        unit = self.root.find(f"{NS}asset/{NS}unit")
        self.metres = float(unit.get("meter")) if unit is not None else 1.0
        up = self.root.find(f"{NS}asset/{NS}up_axis")
        self.up = up.text.strip() if up is not None else "Y_UP"

    def material_name(self, material_id):
        return (self.ids[material_id].get("name") or material_id) if material_id in self.ids else "default"

    def ref(self, url):
        return self.ids[url.lstrip("#")]

    def colour(self, material_id):
        """Diffuse RGBA of a material; a texture (or no material) counts as mid grey."""
        if material_id not in self.ids:
            return np.array([0.7, 0.7, 0.7, 1.0])
        effect = self.ref(self.ids[material_id].find(f"{NS}instance_effect").get("url"))
        tech = effect.find(f"{NS}profile_COMMON/{NS}technique")
        shader = next(iter(tech), None) if tech is not None else None
        rgba = np.array([0.7, 0.7, 0.7, 1.0])
        if shader is None:
            return rgba
        col = shader.find(f"{NS}diffuse/{NS}color")
        if col is None:
            col = shader.find(f"{NS}emission/{NS}color")
        if col is not None:
            rgba = floats(col)
        transparent = shader.find(f"{NS}transparent")
        amount = shader.find(f"{NS}transparency/{NS}float")
        amount = float(amount.text) if amount is not None else 1.0
        if transparent is not None and transparent.find(f"{NS}color") is not None:
            t = floats(transparent.find(f"{NS}color"))
            if transparent.get("opaque") == "RGB_ZERO":  # SketchUp glass: 0 = opaque, 1 = clear
                rgba[3] = 1 - amount * (0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2])
            else:  # A_ONE, the default
                rgba[3] = t[3] * amount
        return rgba

    def triangles(self, geometry):
        """Yield (material symbol, vertices, faces) for each triangle primitive."""
        mesh = geometry.find(f"{NS}mesh")
        if mesh is None:
            return
        vert_src = {v.get("id"): v.find(f"{NS}input[@semantic='POSITION']").get("source")
                    for v in mesh.findall(f"{NS}vertices")}
        for prim in list(mesh.findall(f"{NS}triangles")) + list(mesh.findall(f"{NS}polylist")):
            inputs = prim.findall(f"{NS}input")
            stride = max(int(i.get("offset")) for i in inputs) + 1
            vin = next(i for i in inputs if i.get("semantic") == "VERTEX")
            src = self.ref(vert_src[vin.get("source").lstrip("#")])
            verts = floats(src.find(f"{NS}float_array")).reshape(-1, 3)
            idx = np.array(prim.find(f"{NS}p").text.split(), int).reshape(-1, stride)[:, int(vin.get("offset"))]
            if prim.tag == f"{NS}polylist":  # fan-triangulate each polygon
                counts = np.array(prim.find(f"{NS}vcount").text.split(), int)
                tris, start = [], 0
                for n in counts:
                    tris += [(idx[start], idx[start + k], idx[start + k + 1]) for k in range(1, n - 1)]
                    start += n
                faces = np.array(tris, int).reshape(-1, 3)
            else:
                faces = idx.reshape(-1, 3)
            yield prim.get("material"), verts, faces

    def walk(self, node, parent=np.eye(4)):
        """Yield (node path, world matrix, instance_geometry) for the whole node tree."""
        world = parent.copy()
        for child in node:
            if child.tag == f"{NS}matrix":
                world = world @ floats(child).reshape(4, 4)
            elif child.tag == f"{NS}translate":
                t = np.eye(4)
                t[:3, 3] = floats(child)
                world = world @ t
            elif child.tag == f"{NS}scale":
                world = world @ np.diag([*floats(child), 1])
        for child in node:
            if child.tag == f"{NS}instance_geometry":
                yield node.get("name") or node.get("id"), world, child
            elif child.tag == f"{NS}node":
                yield from self.walk(child, world)
            elif child.tag == f"{NS}instance_node":
                yield from self.walk(self.ref(child.get("url")), world)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("src", type=Path)
    p.add_argument("--name", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--skip", type=int, nargs="*", default=[],
                   help="drop these geometry instances, by index (see --list)")
    p.add_argument("--skip-material", nargs="*", default=[],
                   help="drop faces with these material names (e.g. SketchUp's back faces, material_0)")
    p.add_argument("--mass", type=float, help="total mass in kg (default: 1000 kg/m^3 over the collision box)")
    p.add_argument("--double-sided", action="store_true",
                   help="also write every face reversed (for single-sided exports; MuJoCo culls back faces)")
    p.add_argument("--list", action="store_true", help="print the geometry instances and their bounds, then exit")
    args = p.parse_args()

    dae = Dae(args.src)
    scene = dae.ref(dae.root.find(f"{NS}scene/{NS}instance_visual_scene").get("url"))
    up = np.eye(4)
    if dae.up == "Y_UP":
        up[:3, :3] = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
    elif dae.up == "X_UP":
        up[:3, :3] = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]

    parts = defaultdict(list)  # material id -> [(vertices, faces)]
    for i, (path, world, inst) in enumerate(dae.walk(scene, up)):
        bind = {m.get("symbol"): m.get("target").lstrip("#")
                for m in inst.iter(f"{NS}instance_material")}
        geometry = dae.ref(inst.get("url"))
        pieces = []
        for symbol, verts, faces in dae.triangles(geometry):
            v = (verts @ world[:3, :3].T + world[:3, 3]) * dae.metres
            f = faces[:, ::-1] if np.linalg.det(world[:3, :3]) < 0 else faces
            pieces.append((bind.get(symbol, symbol), v[np.unique(f)], v, f))
        if args.list:
            used = np.vstack([u for _, u, _, _ in pieces]) if pieces else None
            box = f"{used.min(0).round(3)} .. {used.max(0).round(3)}" if used is not None else "no triangles"
            mats = sorted({str(m) for m, *_ in pieces})
            print(f"{i:3d}  {geometry.get('name') or geometry.get('id'):24s} {box}  {mats}")
            continue
        if i in args.skip:
            continue
        for mat, _, v, f in pieces:
            if dae.material_name(mat) in args.skip_material:
                continue
            parts[mat].append((v, f))
    if args.list:
        return

    merged = {}
    for mat, pieces in parts.items():
        offs = np.cumsum([0] + [len(v) for v, _ in pieces[:-1]])
        merged[mat] = (np.vstack([v for v, _ in pieces]), np.vstack([f + o for (_, f), o in zip(pieces, offs)]))
    allv = np.vstack([v[np.unique(f)] for v, f in merged.values()])
    lo, hi = allv.min(0), allv.max(0)
    offset = np.array([-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]])
    size = hi - lo

    args.out.mkdir(parents=True, exist_ok=True)
    assets, geoms = [], []
    for i, (mat, (v, f)) in enumerate(sorted(merged.items(), key=lambda kv: str(kv[0]))):
        v = v + offset
        used = np.unique(f)  # drop vertices no face of this material uses
        remap = np.full(len(v), -1)
        remap[used] = np.arange(len(used))
        if args.double_sided:
            f = np.vstack([f, f[:, ::-1]])
        fname = f"part_{i:02d}.obj"
        with (args.out / fname).open("w") as out:
            out.writelines(f"v {x:.6f} {y:.6f} {z:.6f}\n" for x, y, z in v[used])
            out.writelines(f"f {a + 1} {b + 1} {c + 1}\n" for a, b, c in remap[f])
        r, g, b, a = dae.colour(mat)
        name = dae.material_name(mat)
        assets.append(f'    <mesh name="{args.name}_{i:02d}" file="{fname}" inertia="shell"/>')
        geoms.append(f'      <geom type="mesh" mesh="{args.name}_{i:02d}" rgba="{r:.3f} {g:.3f} {b:.3f} {a:.3f}"'
                     f' contype="0" conaffinity="0" density="0" group="1"/>  <!-- {name} -->')

    hx, hy, hz = size / 2
    mass = f' mass="{args.mass:g}"' if args.mass else ""
    xml = f"""<!-- Generated by tools/convert_dae.py from {args.src.name}; size {size[0]:.3f} x {size[1]:.3f} x {size[2]:.3f} m.
     Origin on the floor, centred in X and Y, +Z up. Visual meshes don't collide and carry no mass; one box stands in. -->
<mujoco model="{args.name}">
  <asset>
{chr(10).join(assets)}
  </asset>
  <worldbody>
    <body name="{args.name}">
{chr(10).join(geoms)}
      <geom name="{args.name}_collision" type="box" size="{hx:.4f} {hy:.4f} {hz:.4f}" pos="0 0 {hz:.4f}"{mass} group="3" rgba=".5 .5 .5 .3"/>
    </body>
  </worldbody>
</mujoco>
"""
    (args.out / f"{args.name}.xml").write_text(xml)
    print(f"{args.name}: {len(merged)} meshes, size {size.round(3)} m -> {args.out}")


if __name__ == "__main__":
    main()
