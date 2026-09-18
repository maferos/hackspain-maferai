#!/usr/bin/env python3
"""Convert an Autodesk .3ds model into MuJoCo-ready meshes + an MJCF body.

MuJoCo can't read .3ds, and a naive "dump the vertices" conversion breaks on two
things this script handles:

* **Instances.** A keyframer node can place a second copy of a mesh (3ds "instance"
  nodes). The mesh data exists once, so ignoring the keyframer silently drops the copy.
* **Mirrored nodes.** A node with a negative scale reverses the triangle winding; the
  faces are flipped back so normals point outwards.

Each keyframer node is placed with   world = pos + R * S * (local - pivot),
where local = inverse(mesh matrix) * stored vertex. The result is split into one mesh
per material (a MuJoCo mesh has a single colour), scaled to metres, centred in XY and
rested on z = 0 (the source must be Z-up). Writes <out>/part_NN.obj and <out>/<name>.xml.

    python tools/convert_3ds.py model.3ds --name sink --scale 0.0254 --out assets/sink
"""
from __future__ import annotations

import argparse
import struct
from collections import defaultdict
from pathlib import Path

import numpy as np

MAIN, EDITOR, OBJECT, TRIMESH = 0x4D4D, 0x3D3D, 0x4000, 0x4100
VERTICES, FACES, FACE_MATERIAL, MESH_MATRIX = 0x4110, 0x4120, 0x4130, 0x4160
MATERIAL, MAT_NAME, MAT_DIFFUSE = 0xAFFF, 0xA000, 0xA020
COLOR_F, COLOR_24, LIN_COLOR_24 = 0x0010, 0x0011, 0x0012
KEYFRAMER, OBJECT_NODE = 0xB000, 0xB002
NODE_HDR, INSTANCE_NAME, PIVOT = 0xB010, 0xB011, 0xB013
POS_TRACK, ROT_TRACK, SCL_TRACK = 0xB020, 0xB021, 0xB022


class Reader:
    def __init__(self, buf: bytes):
        self.buf = buf

    def chunks(self, start, end):
        while start + 6 <= end:
            cid, length = struct.unpack_from("<HI", self.buf, start)
            if length < 6:
                break
            yield cid, start + 6, min(start + length, end)
            start += length

    def cstring(self, pos):
        stop = self.buf.index(b"\0", pos)
        return self.buf[pos:stop].decode("latin-1"), stop + 1

    def colour(self, start, end):
        for cid, s, _ in self.chunks(start, end):
            if cid in (COLOR_24, LIN_COLOR_24):
                return tuple(c / 255 for c in self.buf[s:s + 3])
            if cid == COLOR_F:
                return struct.unpack_from("<3f", self.buf, s)
        return (0.7, 0.7, 0.7)

    def first_key(self, start, width):
        """First key of a keyframer track (frame 0 is all a static model needs)."""
        (n,) = struct.unpack_from("<I", self.buf, start + 10)
        if n == 0:
            return None
        pos = start + 14
        _, flags = struct.unpack_from("<IH", self.buf, pos)
        pos += 6 + 4 * bin(flags).count("1")  # skip spline parameters
        return struct.unpack_from(f"<{width}f", self.buf, pos)


def axis_angle(angle, axis):
    axis = np.asarray(axis, float)
    norm = np.linalg.norm(axis)
    if norm == 0 or angle == 0:
        return np.eye(3)
    x, y, z = axis / norm
    k = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    return np.eye(3) + np.sin(angle) * k + (1 - np.cos(angle)) * k @ k


def parse(path: Path):
    r = Reader(path.read_bytes())
    materials, meshes, nodes = {}, {}, []
    for cid, s, e in r.chunks(0, len(r.buf)):
        if cid != MAIN:
            continue
        for cid, s, e in r.chunks(s, e):
            if cid == EDITOR:
                for cid, s2, e2 in r.chunks(s, e):
                    if cid == MATERIAL:
                        name, colour = None, (0.7, 0.7, 0.7)
                        for mid, ms, me in r.chunks(s2, e2):
                            if mid == MAT_NAME:
                                name, _ = r.cstring(ms)
                            elif mid == MAT_DIFFUSE:
                                colour = r.colour(ms, me)
                        if name:
                            materials[name] = colour
                    elif cid == OBJECT:
                        name, pos = r.cstring(s2)
                        for tid, ts, te in r.chunks(pos, e2):
                            if tid == TRIMESH:
                                meshes[name] = read_trimesh(r, ts, te)
            elif cid == KEYFRAMER:
                for nid, ns, ne in r.chunks(s, e):
                    if nid == OBJECT_NODE:
                        nodes.append(read_node(r, ns, ne))
    if not nodes:  # no keyframer: every mesh once, where it is stored
        nodes = [{"name": n, "world": np.eye(4), "raw": True} for n in meshes]
    return materials, meshes, nodes


def read_trimesh(r, start, end):
    verts, faces, groups, matrix = None, None, [], np.eye(4)
    for mid, ms, me in r.chunks(start, end):
        if mid == VERTICES:
            (n,) = struct.unpack_from("<H", r.buf, ms)
            verts = np.frombuffer(r.buf, "<f4", 3 * n, ms + 2).reshape(n, 3).astype(float)
        elif mid == FACES:
            (n,) = struct.unpack_from("<H", r.buf, ms)
            faces = np.frombuffer(r.buf, "<u2", 4 * n, ms + 2).reshape(n, 4)[:, :3].astype(int)
            for sid, ss, _ in r.chunks(ms + 2 + 8 * n, me):
                if sid == FACE_MATERIAL:
                    mat, q = r.cstring(ss)
                    (k,) = struct.unpack_from("<H", r.buf, q)
                    groups.append((mat, np.frombuffer(r.buf, "<u2", k, q + 2).astype(int)))
        elif mid == MESH_MATRIX:
            m = struct.unpack_from("<12f", r.buf, ms)
            matrix[:3, 0], matrix[:3, 1], matrix[:3, 2], matrix[:3, 3] = m[0:3], m[3:6], m[6:9], m[9:12]
    return {"verts": verts, "faces": faces, "groups": groups, "matrix": matrix}


def read_node(r, start, end):
    name, pivot = None, np.zeros(3)
    pos, rot, scl = np.zeros(3), np.eye(3), np.ones(3)
    for cid, s, e in r.chunks(start, end):
        if cid == NODE_HDR:
            name, _ = r.cstring(s)
        elif cid == PIVOT:
            pivot = np.array(struct.unpack_from("<3f", r.buf, s))
        elif cid == POS_TRACK and (k := r.first_key(s, 3)):
            pos = np.array(k)
        elif cid == ROT_TRACK and (k := r.first_key(s, 4)):
            rot = axis_angle(-k[0], k[1:])  # 3ds stores the angle negated
        elif cid == SCL_TRACK and (k := r.first_key(s, 3)):
            scl = np.array(k)
    world = np.eye(4)
    world[:3, :3] = rot @ np.diag(scl)
    world[:3, 3] = pos - world[:3, :3] @ pivot
    return {"name": name, "world": world, "raw": False}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("src", type=Path)
    p.add_argument("--name", required=True)
    p.add_argument("--scale", type=float, required=True, help="model units -> metres")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--skip-node", type=int, nargs="*", default=[],
                   help="drop these keyframer nodes, by index (see --list)")
    p.add_argument("--center-x", type=int, nargs="*", default=[],
                   help="move these nodes along X so each is centred on the rest of the model")
    p.add_argument("--recolor", nargs="*", default=[], metavar="MATERIAL=R,G,B",
                   help="override a material's diffuse colour (0-1), e.g. Color_I13=0.92,0.92,0.91")
    p.add_argument("--list", action="store_true", help="print the nodes and their bounds, then exit")
    args = p.parse_args()

    materials, meshes, nodes = parse(args.src)
    for item in args.recolor:
        mat, rgb = item.split("=")
        materials[mat] = tuple(float(c) for c in rgb.split(","))
    placed = {}  # node index -> (mesh, vertices, faces)
    for i, node in enumerate(nodes):
        if i in args.skip_node or node["name"] not in meshes:
            continue
        mesh = meshes[node["name"]]
        # Stored vertices already include the mesh matrix; undo it, then place the node.
        xf = node["world"] if node["raw"] else node["world"] @ np.linalg.inv(mesh["matrix"])
        faces = mesh["faces"]
        if np.linalg.det(xf[:3, :3]) < 0:
            faces = faces[:, ::-1]  # a mirror reverses the winding
        placed[i] = (mesh, mesh["verts"] @ xf[:3, :3].T + xf[:3, 3], faces)

    if args.list:
        for i, node in enumerate(nodes):
            state = f"{placed[i][1].min(0).round(2)} .. {placed[i][1].max(0).round(2)}" if i in placed else "skipped"
            print(f"{i:3d}  {node['name']:20s} {state}")
        return

    rest = np.vstack([v for i, (_, v, _) in placed.items() if i not in args.center_x])
    centre = (rest[:, 0].min() + rest[:, 0].max()) / 2
    for i in args.center_x:
        v = placed[i][1]
        v[:, 0] += centre - (v[:, 0].min() + v[:, 0].max()) / 2

    parts = defaultdict(lambda: ([], []))  # material -> (vertex arrays, face arrays)
    counts = defaultdict(int)
    for mesh, verts, faces in placed.values():
        grouped = mesh["groups"] or [("default", np.arange(len(faces)))]
        for mat, idx in grouped:
            vs, fs = parts[mat]
            vs.append(verts)
            fs.append((faces[idx], counts[mat]))
            counts[mat] += len(verts)

    merged = {}
    for mat, (vs, fs) in parts.items():
        merged[mat] = (np.vstack(vs) * args.scale, np.vstack([f + off for f, off in fs]))
    allv = np.vstack([v for v, _ in merged.values()])
    lo, hi = allv.min(0), allv.max(0)
    offset = np.array([-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]])
    size = hi - lo

    args.out.mkdir(parents=True, exist_ok=True)
    assets, geoms = [], []
    for i, (mat, (v, f)) in enumerate(sorted(merged.items())):
        v = v + offset
        used = np.unique(f)  # drop vertices no face of this material uses
        remap = np.full(len(v), -1)
        remap[used] = np.arange(len(used))
        fname = f"part_{i:02d}.obj"
        with (args.out / fname).open("w") as out:
            out.writelines(f"v {x:.6f} {y:.6f} {z:.6f}\n" for x, y, z in v[used])
            out.writelines(f"f {a + 1} {b + 1} {c + 1}\n" for a, b, c in remap[f])
        rr, gg, bb = materials.get(mat, (0.7, 0.7, 0.7))
        mat = mat + " (recoloured)" if any(r.startswith(mat + "=") for r in args.recolor) else mat
        assets.append(f'    <mesh name="{args.name}_{i:02d}" file="{fname}" inertia="shell"/>')
        geoms.append(f'      <geom type="mesh" mesh="{args.name}_{i:02d}" rgba="{rr:.3f} {gg:.3f} {bb:.3f} 1"'
                     f' contype="0" conaffinity="0" group="1"/>  <!-- {mat} -->')

    hx, hy, hz = size / 2
    xml = f"""<!-- Generated by tools/convert_3ds.py from {args.src.name}; size {size[0]:.3f} x {size[1]:.3f} x {size[2]:.3f} m.
     Origin on the floor, centred in X and Y, +Z up. Visual meshes don't collide; one box stands in. -->
<mujoco model="{args.name}">
  <asset>
{chr(10).join(assets)}
  </asset>
  <worldbody>
    <body name="{args.name}">
{chr(10).join(geoms)}
      <geom name="{args.name}_collision" type="box" size="{hx:.4f} {hy:.4f} {hz:.4f}" pos="0 0 {hz:.4f}" group="3" rgba=".5 .5 .5 .3"/>
    </body>
  </worldbody>
</mujoco>
"""
    (args.out / f"{args.name}.xml").write_text(xml)
    print(f"{args.name}: {len(placed)} of {len(nodes)} nodes, {len(merged)} meshes, size {size.round(3)} m -> {args.out}")


if __name__ == "__main__":
    main()
