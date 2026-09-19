#!/usr/bin/env python3
"""Generate the perfumery-lab room that surrounds the minihannover bench.

Single source of truth for everything procedural in models/minihannover_scene.xml:
the room shell (sandwich-panel walls, resin floor, modular ceiling with LED panels,
glass partitions, doors), the shelving gantry on the bench with its library of
barcoded sample bottles, the wall bench and its equipment, the entrance storage corner, the wash
zone, the drying rack, the extraction arms and the office seen through the glass.
The bench itself (assets/minihannover/), the sink, the balances and the instruments
are separate assets; the scene composes them.

    python tools/build_labelled_bottles.py   # once, and after any barcode change
    python scripts/generate_lab_room.py

The library is stocked from assets/labelled_bottles/manifest.json, which the first
command writes: every sample of the barcode catalogue that the scene does not place
by hand stands on the gantry, once, in the bottle of its own phase and size.

Writes assets/lab_room/lab_room.xml plus the lathe / row meshes in assets/lab_room/meshes/.
Frame: the bench's frame (origin on the floor at the bench centre, +X along the bench,
+Z up). The entrance is at -X; walking in, the right-hand wall is -Y.

Everything is welded to the world. Decorative pieces are visual only (contype 0);
furniture that a robot could touch (benches, counters, gantry, walls) keeps a box.
"""

from __future__ import annotations

import json
import math
import pathlib

import numpy as np

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "lab_room"
MESHES = OUT / "meshes"

# --- Room (interior, metres) -------------------------------------------------
X0, X1 = -8.5, 5.5        # entrance end wall, far glass partition
Y0, Y1 = -2.9, 2.1        # right wall (-Y), left wall (+Y)
H = 3.0                   # ceiling height
WALL_T = 0.1
PANEL_W = 1.2             # sandwich panel module
GLASS_FROM_X = 2.5        # the right wall turns into glass from here to the far end

# --- Central bench (from assets/minihannover) --------------------------------
BENCH_TOP = 0.90
BENCH_HX, BENCH_HY = 3.0, 0.75

# --- Shelving gantry on the bench spine ---------------------------------------
GANTRY_X0, MODULE, MODULES = -2.4, 1.1, 4
GANTRY_HY = 0.30
SHELF_Z = (1.30, 1.58, 1.86, 2.14)
GANTRY_TOP = 2.42

# --- Wall bench along the right wall -------------------------------------------
WB_X0, WB_X1, WB_DEPTH = -5.0, 2.2, 0.70

# --- Sample library on the gantry ------------------------------------------------
BOTTLES = OUT.parent / "labelled_bottles"
# Samples models/minihannover_scene.xml places itself, in the entrance corner and
# loose on the worktop. A sample is one physical bottle, so they are not shelved too.
PLACED_BY_SCENE = ("PWD-0004", "PWD-0008", "PWD-0012", "PWD-0020", "PWD-0024", "PWD-0026",
                   "SMP-0005", "SMP-0009", "SMP-0013", "SMP-0017", "SMP-0021", "SMP-0030",
                   "SMP-0034")
SHELF_FACE_HALF_WIDTH = MODULE / 2 - 0.045   # clear of the uprights
SHELF_SETBACK = 0.03                         # nearest a bottle front comes to the shelf lip
SHELF_DEPTH_SCATTER = 0.10                   # and how much further back it may stand
SHELF_MIN_GAP = 0.012                        # least air between two bottles on a shelf
SHELF_YAW_SCATTER = 25.0                     # degrees a label may be turned off the aisle


# =============================================================================
# Meshes
# =============================================================================

def lathe(profile, segments=24):
    """Revolve an (r, z) profile, listed bottom to top, about +Z. Rings of radius 0
    collapse to a single pole vertex. Returns (vertices, faces), outward-facing."""
    verts, rings = [], []
    for r, z in profile:
        if r == 0:
            rings.append([len(verts)])
            verts.append((0.0, 0.0, z))
        else:
            ring = []
            for k in range(segments):
                a = 2 * math.pi * k / segments
                ring.append(len(verts))
                verts.append((r * math.cos(a), r * math.sin(a), z))
            rings.append(ring)
    faces = []
    for lo, hi in zip(rings, rings[1:]):
        for k in range(segments):
            k1 = (k + 1) % segments
            if len(lo) == 1 and len(hi) == 1:
                continue
            if len(lo) == 1:
                faces.append((lo[0], hi[k1], hi[k]))
            elif len(hi) == 1:
                faces.append((lo[k], lo[k1], hi[0]))
            else:
                faces.append((lo[k], lo[k1], hi[k1]))
                faces.append((lo[k], hi[k1], hi[k]))
    return np.array(verts, float), np.array(faces, int)


def write_obj(name, mesh):
    v, f = mesh
    MESHES.mkdir(parents=True, exist_ok=True)
    with (MESHES / f"{name}.obj").open("w") as out:
        out.writelines(f"v {x:.5f} {y:.5f} {z:.5f}\n" for x, y, z in v)
        out.writelines(f"f {a + 1} {b + 1} {c + 1}\n" for a, b, c in f)


LATHES = {
    # name: (profile, segments). Everything a lab has that is round.
    "pot": ([(0, 0), (0.15, 0), (0.155, 0.004), (0.155, 0.22), (0.162, 0.225), (0.162, 0.23),
             (0.148, 0.23), (0.148, 0.008), (0, 0.008)], 32),
    "pot_small": ([(0, 0), (0.10, 0), (0.104, 0.004), (0.104, 0.12), (0.108, 0.125),
                   (0.097, 0.125), (0.097, 0.006), (0, 0.006)], 28),
    "lid": ([(0, 0.001), (0.108, 0), (0.105, 0.012), (0.03, 0.03), (0, 0.035)], 28),
    "funnel": ([(0.012, 0), (0.012, 0.09), (0.11, 0.21), (0.114, 0.215), (0.108, 0.215),
                (0.008, 0.095), (0.008, 0)], 24),
    "beaker": ([(0, 0), (0.035, 0), (0.035, 0.095), (0.038, 0.1), (0.033, 0.1), (0.033, 0.003), (0, 0.003)], 20),
    "flask": ([(0, 0), (0.065, 0), (0.066, 0.01), (0.02, 0.15), (0.017, 0.19), (0.019, 0.195),
               (0.015, 0.195), (0.015, 0.155), (0, 0.155)], 20),
    "cylinder": ([(0, 0), (0.045, 0), (0.045, 0.01), (0.018, 0.012), (0.018, 0.3), (0.022, 0.305),
                  (0.016, 0.305), (0.016, 0.014), (0, 0.014)], 16),
    "carboy": ([(0, 0), (0.15, 0), (0.16, 0.02), (0.16, 0.36), (0.12, 0.43), (0.04, 0.46),
                (0.04, 0.49), (0, 0.49)], 28),
    "wash_bottle": ([(0, 0), (0.035, 0), (0.037, 0.01), (0.037, 0.15), (0.02, 0.18), (0.014, 0.19), (0, 0.19)], 16),
    "hood": ([(0.04, 0.2), (0.04, 0.135), (0.155, 0.0), (0.16, 0.0), (0.045, 0.14), (0.045, 0.2)], 24),
    "drum": ([(0, 0), (0.22, 0), (0.22, 0.62), (0, 0.62)], 28),
    "bin": ([(0, 0), (0.17, 0), (0.2, 0.62), (0, 0.62)], 24),
    "bin_lid": ([(0, 0), (0.21, 0), (0.21, 0.01), (0.08, 0.045), (0, 0.05)], 24),
}


def build_meshes():
    names = []
    for name, (profile, seg) in LATHES.items():
        write_obj(name, lathe(profile, seg))
        names.append(name)
    return names


# =============================================================================
# MJCF writer
# =============================================================================

MATERIALS = {
    # name: attributes. Palette: white, very light grey, amber, blue accents, red rack.
    "panel": 'rgba="0.93 0.93 0.91 1" specular="0.35" shininess="0.5"',
    "panel_joint": 'rgba="0.74 0.75 0.75 1"',
    "floor": 'rgba="0.80 0.81 0.81 1" specular="0.3" shininess="0.6" reflectance="0.12"',
    "ceiling": 'rgba="0.95 0.95 0.94 1" specular="0.05" emission="0.45"',
    "led": 'rgba="0.98 0.99 1.0 1" emission="1"',
    "grille": 'rgba="0.55 0.57 0.58 1"',
    "worktop": 'rgba="0.95 0.95 0.94 1" specular="0.8" shininess="0.9" reflectance="0.3"',
    "white": 'rgba="0.94 0.94 0.93 1" specular="0.3" shininess="0.4"',
    "white_matte": 'rgba="0.92 0.92 0.91 1" specular="0.1"',
    "shelf": 'rgba="0.95 0.95 0.95 1" specular="0.4" shininess="0.5"',
    "seam": 'rgba="0.80 0.81 0.81 1"',
    "amber": 'rgba="0.55 0.24 0.04 0.82" specular="0.9" shininess="0.95"',
    "sample_hdpe": 'rgba="0.92 0.92 0.91 1" specular="0.25" shininess="0.4"',
    "sample_cap": 'rgba="0.93 0.93 0.91 1" specular="0.3" shininess="0.5"',
    "glass": 'rgba="0.80 0.90 0.95 0.15" specular="0.9" shininess="0.95" reflectance="0.1"',
    "glass_clear": 'rgba="0.88 0.94 0.97 0.30" specular="0.9" shininess="0.95"',
    "frosted": 'rgba="0.96 0.97 0.98 0.75"',
    "aluminium": 'rgba="0.76 0.78 0.80 1" specular="0.7" shininess="0.7"',
    "steel": 'rgba="0.72 0.73 0.74 1" specular="0.8" shininess="0.6"',
    "black": 'rgba="0.05 0.05 0.06 1" specular="0.9" shininess="0.9"',
    "dark": 'rgba="0.18 0.19 0.20 1"',
    "grey_device": 'rgba="0.80 0.81 0.80 1" specular="0.3"',
    "screen": 'rgba="0.10 0.16 0.22 1" emission="0.25"',
    "orange": 'rgba="0.93 0.40 0.10 1"',
    "blue_hdpe": 'rgba="0.05 0.28 0.72 1" specular="0.15"',
    "blue_motor": 'rgba="0.10 0.30 0.70 1" specular="0.5"',
    "stripe_blue": 'rgba="0.10 0.35 0.75 1"',
    "cream": 'rgba="0.93 0.91 0.84 1" specular="0.3"',
    "hdpe_white": 'rgba="0.93 0.93 0.90 0.85" specular="0.2"',
    "kraft": 'rgba="0.60 0.45 0.28 1" specular="0.05"',
    "tape": 'rgba="0.65 0.48 0.28 1" specular="0.3" shininess="0.2"',
    "cardboard": 'rgba="0.72 0.58 0.40 1" specular="0.05"',
    "red_rack": 'rgba="0.75 0.10 0.08 1" specular="0.3"',
    "navy_rack": 'rgba="0.10 0.14 0.32 1" specular="0.3"',
    "galvanised": 'rgba="0.68 0.70 0.71 1" specular="0.5"',
    "foil": 'rgba="0.80 0.80 0.82 1" specular="1" shininess="1"',
    "paper": 'rgba="0.98 0.98 0.97 1"',
    "bag": 'rgba="0.95 0.95 0.93 0.55"',
    "red_cap": 'rgba="0.80 0.10 0.10 1"',
    "coat": 'rgba="0.95 0.96 0.97 1"',
    "skin": 'rgba="0.80 0.64 0.52 1"',
    "cap_blue": 'rgba="0.55 0.72 0.90 1"',
    "trousers": 'rgba="0.20 0.22 0.28 1"',
    "desk": 'rgba="0.86 0.84 0.80 1"',
}


class Mjcf:
    def __init__(self):
        self.lines = []
        self.assets = []   # extra <asset> lines: meshes and textures from other folders
        self.n = {}
        self.bevel_meshes = {}

    def uid(self, stem):
        self.n[stem] = self.n.get(stem, -1) + 1
        return f"{stem}_{self.n[stem]}"

    def add(self, line, indent=3):
        self.lines.append("  " * indent + line)

    def comment(self, text):
        self.lines.append("")
        self.add(f"<!-- {text} -->")

    def box(self, stem, center, half, mat, solid=False, group=1, euler=None, name=True):
        """Axis-aligned box from centre and half-sizes. solid=True keeps a collider."""
        if stem == "pull":
            # Stand-off stainless handle with two mounting posts.
            cx, cy, cz = center
            hx, hy, hz = half
            axis = 0 if hx > hz else 2
            a, b = list(center), list(center)
            a[axis] -= half[axis] * 0.85
            b[axis] += half[axis] * 0.85
            self.rod("handle_grip", a, b, 0.006, mat)
            for end in (a, b):
                back = list(end)
                back[1] -= hy
                front = list(end)
                front[1] += hy
                self.rod("handle_mount", back, front, 0.008, mat)
            return
        if stem == "box":
            self.carton(center, half, mat, solid, euler)
            return
        col = "" if solid else ' contype="0" conaffinity="0"'
        rot = f' euler="{" ".join(f"{a:g}" for a in euler)}"' if euler else ""
        nm = f'name="{self.uid(stem)}" ' if name else ""
        # Millimetre bevels catch highlights without changing placement or collision.
        beveled = min(half) >= 0.009 and mat in {
            "white", "white_matte", "worktop", "desk", "grey_device", "cardboard", "cream", "dark"}
        shape = f'type="box" size="{fmt(half)}"'
        if beveled:
            key = tuple(float(h) for h in half)
            if key not in self.bevel_meshes:
                radius = min(0.006, min(half) * 0.22)
                vertices = []
                for axis in range(3):
                    for sx in (-1, 1):
                        for sy in (-1, 1):
                            for sz in (-1, 1):
                                vertices.extend(sign * (h if i == axis else h - radius)
                                                for i, (sign, h) in enumerate(zip((sx, sy, sz), half)))
                self.bevel_meshes[key] = (f"bevel_{len(self.bevel_meshes)}", vertices)
            mesh_name = self.bevel_meshes[key][0]
            shape = f'type="mesh" mesh="{mesh_name}"'
            if solid:
                self.add(f'<geom type="box" pos="{fmt(center)}" size="{fmt(half)}"{rot} '
                         'group="3" rgba="0 0 0 0"/>')
            col = ' contype="0" conaffinity="0"'
        self.add(f'<geom {nm}{shape} pos="{fmt(center)}"{rot} '
                 f'material="{mat}"{col} group="{group}"/>')

    def carton(self, center, half, mat, solid, euler):
        """Sealed shipping carton, with all details in the rotated local frame."""
        hx, hy, hz = half
        rot = f' euler="{fmt(euler)}"' if euler else ""
        self.add(f'<frame pos="{fmt(center)}"{rot}>')
        self.box("carton_shell", (0, 0, 0), half, mat, solid=solid)
        self.box("carton_seam", (0, 0, hz + 0.0003), (0.001, hy - 0.004, 0.0003), "kraft")
        self.box("packing_tape", (0, 0, hz + 0.0007), (0.025, hy - 0.003, 0.0003), "tape")
        for side in (-1, 1):
            self.box("tape_end", (0, side * (hy + 0.0006), hz - 0.026), (0.025, 0.0004, 0.026), "tape")
            self.box("shipping_label", (hx * 0.32, side * (hy + 0.001), 0), (hx * 0.43, 0.0004, hz * 0.35), "paper")
            for k in range(17):
                self.box("barcode", (hx * 0.02 + k * hx * 0.035, side * (hy + 0.0016), -hz * 0.05),
                         (0.0007 if k % 3 else 0.0014, 0.0002, hz * 0.15), "dark")
            for k in range(2):
                self.box("label_line", (hx * 0.32, side * (hy + 0.0016), hz * (0.18 + k * 0.08)),
                         (hx * (0.27 - k * 0.05), 0.0002, 0.001), "grille")
        self.add('</frame>')

    def ellipsoid(self, stem, center, radii, mat):
        self.add(f'<geom name="{self.uid(stem)}" type="ellipsoid" pos="{fmt(center)}" '
                 f'size="{fmt(radii)}" material="{mat}" contype="0" conaffinity="0" group="1"/>')

    def span(self, stem, lo, hi, mat, **kw):
        """Box between two corners."""
        lo, hi = np.asarray(lo, float), np.asarray(hi, float)
        self.box(stem, (lo + hi) / 2, np.abs(hi - lo) / 2, mat, **kw)

    def cyl(self, stem, center, r, hz, mat, solid=False, euler=None, kind="cylinder"):
        col = "" if solid else ' contype="0" conaffinity="0"'
        rot = f' euler="{" ".join(f"{a:g}" for a in euler)}"' if euler else ""
        size = f"{r:g} {hz:g}" if kind != "sphere" else f"{r:g}"
        self.add(f'<geom name="{self.uid(stem)}" type="{kind}" pos="{fmt(center)}" size="{size}"{rot} '
                 f'material="{mat}"{col} group="1"/>')

    def rod(self, stem, a, b, r, mat, kind="capsule"):
        """Capsule / cylinder between two points."""
        col = ' contype="0" conaffinity="0"'
        self.add(f'<geom name="{self.uid(stem)}" type="{kind}" fromto="{fmt(a)} {fmt(b)}" size="{r:g}" '
                 f'material="{mat}"{col} group="1"/>')

    def mesh(self, stem, mesh, pos, mat, euler=None, group=1):
        rot = f' euler="{" ".join(f"{a:g}" for a in euler)}"' if euler else ""
        self.add(f'<geom name="{self.uid(stem)}" type="mesh" mesh="{mesh}" pos="{fmt(pos)}"{rot} '
                 f'material="{mat}" contype="0" conaffinity="0" group="{group}"/>')

    def attach(self, model, body, pos, yaw=0.0):
        prefix = self.uid(model)
        q = f' euler="0 0 {yaw:g}"' if yaw else ""
        self.add(f'<frame pos="{fmt(pos)}"{q}>')
        self.add(f'  <attach model="{model}" body="{body}" prefix="{prefix}_"/>')
        self.add("</frame>")


def fmt(v):
    return " ".join(f"{x:.4f}".rstrip("0").rstrip(".") if abs(x) > 1e-9 else "0" for x in v)


# =============================================================================
# Room
# =============================================================================

def shell(m):
    m.comment("Walls: white sandwich panels, joints every 1.2 m, skirting. Boxes sit outside the interior.")
    # Left wall (+Y) and end wall (-X) are all panels; right wall (-Y) is panels up to GLASS_FROM_X.
    m.span("wall", (X0 - WALL_T, Y1, 0), (X1, Y1 + WALL_T, H), "panel", solid=True)
    m.span("wall", (X0 - WALL_T, Y0 - WALL_T, 0), (X0, Y1 + WALL_T, H), "panel", solid=True)
    m.span("wall", (X0 - WALL_T, Y0 - WALL_T, 0), (GLASS_FROM_X, Y0, H), "panel", solid=True)
    for x in np.arange(X0 + PANEL_W, X1, PANEL_W):
        m.span("joint", (x - 0.003, Y1 - 0.001, 0), (x + 0.003, Y1, H), "panel_joint")
        if x < GLASS_FROM_X:
            m.span("joint", (x - 0.003, Y0, 0), (x + 0.003, Y0 + 0.001, H), "panel_joint")
    for y in np.arange(Y0 + PANEL_W, Y1, PANEL_W):
        m.span("joint", (X0, y - 0.003, 0), (X0 + 0.001, y + 0.003, H), "panel_joint")
    # Coved skirting in the floor colour.
    m.span("skirt", (X0, Y1 - 0.012, 0), (X1, Y1, 0.10), "seam")
    m.span("skirt", (X0, Y0, 0), (GLASS_FROM_X, Y0 + 0.012, 0.10), "seam")
    m.span("skirt", (X0, Y0, 0), (X0 + 0.012, Y1, 0.10), "seam")

    m.comment("Glass partitions: the far end wall and the last stretch of the right wall.")
    glass_wall(m, axis="x", at=X1, lo=Y0, hi=Y1)
    glass_wall(m, axis="y", at=Y0, lo=GLASS_FROM_X, hi=X1)

    m.comment("Doors: entrance in the end wall, side door in the left wall near the drying rack.")
    door(m, (X0, 0.85), facing=(1, 0))
    door(m, (4.3, Y1), facing=(0, -1))


def glass_wall(m, axis, at, lo, hi):
    t = 0.02
    if axis == "x":
        m.span("glass", (at, lo, 0), (at + t, hi, H), "glass", solid=True)
        span = lambda a, b, z0, z1, d=0.03: m.span("profile", (at - d, a, z0), (at + t + d, b, z1), "aluminium")
    else:
        m.span("glass", (lo, at - t, 0), (hi, at, H), "glass", solid=True)
        span = lambda a, b, z0, z1, d=0.03: m.span("profile", (a, at - t - d, z0), (b, at + d, z1), "aluminium")
    for s in np.linspace(lo, hi, int(round((hi - lo) / 1.2)) + 1):  # mullions
        span(s - 0.02, s + 0.02, 0, H)
    span(lo, hi, 0, 0.06)      # base rail
    span(lo, hi, H - 0.05, H)  # head rail
    for z in (1.0, 1.45):      # manifestation bands
        if axis == "x":
            m.span("band", (at - 0.001, lo, z), (at + t + 0.001, hi, z + 0.10), "frosted")
        else:
            m.span("band", (lo, at - t - 0.001, z), (hi, at + 0.001, z + 0.10), "frosted")


def door(m, where, facing):
    """A white swing door drawn on the wall face: leaf, frame, lever handle."""
    fx, fy = facing
    w, h, d = 1.0, 2.1, 0.02
    if fx:  # in an X wall, spans Y
        x, yc = where
        m.span("door", (x, yc - w / 2, 0), (x + d, yc + w / 2, h), "white", group=1)
        m.span("door_frame", (x, yc - w / 2 - 0.05, h), (x + d + 0.005, yc + w / 2 + 0.05, h + 0.05), "white_matte")
        for s in (-1, 1):
            m.span("door_frame", (x, yc + s * (w / 2 + 0.025) - 0.025, 0), (x + d + 0.005, yc + s * (w / 2 + 0.025) + 0.025, h), "white_matte")
        hy = yc + w / 2 - 0.08
        m.rod("handle", (x + d, hy, 1.05), (x + d + 0.05, hy, 1.05), 0.008, "steel", kind="cylinder")
        m.rod("handle", (x + d + 0.05, hy, 1.05), (x + d + 0.05, hy - 0.13, 1.05), 0.01, "steel")
    else:  # in a Y wall, spans X
        xc, y = where
        m.span("door", (xc - w / 2, y - d, 0), (xc + w / 2, y, h), "white", group=1)
        m.span("door_frame", (xc - w / 2 - 0.05, y - d - 0.005, h), (xc + w / 2 + 0.05, y, h + 0.05), "white_matte")
        for s in (-1, 1):
            m.span("door_frame", (xc + s * (w / 2 + 0.025) - 0.025, y - d - 0.005, 0), (xc + s * (w / 2 + 0.025) + 0.025, y, h), "white_matte")
        hx = xc - w / 2 + 0.08
        m.rod("handle", (hx, y - d, 1.05), (hx, y - d - 0.05, 1.05), 0.008, "steel", kind="cylinder")
        m.rod("handle", (hx, y - d - 0.05, 1.05), (hx + 0.13, y - d - 0.05, 1.05), 0.01, "steel")


def ceiling(m):
    m.comment('Ceiling (group 2: press "2" in the viewer to hide it and look in from above): '
              "modular tiles, LED panels along the room axis, linear air grilles.")
    m.box("ceiling", ((X0 + X1) / 2, (Y0 + Y1) / 2, H + 0.02), ((X1 - X0) / 2 + WALL_T, (Y1 - Y0) / 2 + WALL_T, 0.02),
          "ceiling", group=2)
    for x in np.arange(X0 + 0.6, X1, 0.6):
        m.span("tile_joint", (x - 0.004, Y0, H - 0.001), (x + 0.004, Y1, H), "panel_joint", group=2)
    for y in np.arange(Y0 + 0.6, Y1, 0.6):
        m.span("tile_joint", (X0, y - 0.004, H - 0.001), (X1, y + 0.004, H), "panel_joint", group=2)
    for y in (-1.65, 0.0, 1.45):
        for x in np.arange(X0 + 1.0, X1 - 0.5, 1.5):
            m.box("led", (x, y, H - 0.006), (0.6, 0.15, 0.006), "led", group=2)
    for y in (-0.9, 0.9):
        for x in np.arange(X0 + 1.8, X1 - 1.0, 3.0):
            m.box("grille", (x, y, H - 0.004), (0.6, 0.04, 0.004), "grille", group=2)


def lights(m):
    m.comment("Cool, even overhead light: a row of soft spots along each aisle, no hard shadows.")
    for y in (-1.65, 1.45):
        for x in np.arange(X0 + 1.75, X1, 3.0):
            m.add(f'<light name="{m.uid("ceiling_light")}" pos="{fmt((x, y, H - 0.05))}" dir="0 0 -1" '
                  f'diffuse="0.26 0.27 0.29" specular="0.08 0.08 0.08" cutoff="75" exponent="1" '
                  f'castshadow="false"/>')
    m.add('<light name="key_light" pos="0 -0.6 2.95" dir="0 0.1 -1" diffuse="0.25 0.25 0.26" cutoff="80" castshadow="true"/>')


# =============================================================================
# Central bench
# =============================================================================

def central_bench(m):
    m.comment("Worktop finish: glossy white laid over the minihannover slab (visual only, 0.2 mm proud) "
              "and a thin orange edge profile on the near stretch.")
    m.box("worktop_finish", (0, 0, BENCH_TOP - 0.0248), (BENCH_HX + 0.0005, BENCH_HY + 0.0005, 0.025), "worktop")
    m.span("edge_profile", (-3.0, -BENCH_HY - 0.003, BENCH_TOP - 0.012), (-1.0, -BENCH_HY - 0.0005, BENCH_TOP - 0.004), "orange")

    m.comment("Under-bench units on both sides: drawers, doors and knee spaces.")
    kinds = ["drawers", "knee", "door", "drawers", "knee", "door", "drawers", "knee", "drawers", "door"]
    unit = 2 * BENCH_HX / len(kinds)
    for side in (-1, 1):
        for i, kind in enumerate(kinds if side < 0 else kinds[::-1]):
            x0 = -BENCH_HX + i * unit
            y_out, y_in = side * (BENCH_HY - 0.02), side * 0.05
            ylo, yhi = sorted((y_out, y_in))
            if kind == "knee":
                m.span("modesty", (x0 + 0.01, min(y_in, 0.05 * side) - 0.01, 0.10), (x0 + unit - 0.01, max(y_in, 0.05 * side) + 0.01, 0.84), "white_matte")
                continue
            m.span("unit", (x0 + 0.005, ylo, 0.10), (x0 + unit - 0.005, yhi, 0.85), "white")
            m.span("plinth", (x0, ylo + 0.03 * (side < 0), 0), (x0 + unit, yhi - 0.03 * (side > 0), 0.10), "seam")
            front = y_out + side * 0.001
            if kind == "drawers":
                for z in (0.33, 0.58):
                    m.span("drawer_gap", (x0 + 0.02, front - 0.001, z), (x0 + unit - 0.02, front + 0.001, z + 0.004), "panel_joint")
                for z in (0.80, 0.55, 0.30):
                    m.span("pull", (x0 + unit / 2 - 0.06, front, z - 0.006), (x0 + unit / 2 + 0.06, front + side * 0.012, z + 0.006), "steel")
            else:
                m.span("pull", (x0 + unit - 0.06, front, 0.62), (x0 + unit - 0.048, front + side * 0.012, 0.78), "steel")


def gantry(m):
    x0, x1 = GANTRY_X0, GANTRY_X0 + MODULE * MODULES
    m.comment("Shelving gantry on the bench spine: 4 modules x 4 shelves, centre divider, "
              "top panel, splash glass under the bottom shelf.")
    for i in range(MODULES + 1):
        x = x0 + i * MODULE
        m.span("upright", (x - 0.015, -GANTRY_HY, BENCH_TOP), (x + 0.015, GANTRY_HY, GANTRY_TOP + 0.02), "shelf", solid=True)
    for z in SHELF_Z:
        m.span("shelf", (x0, -GANTRY_HY, z - 0.012), (x1, GANTRY_HY, z), "shelf", solid=True)
        for s in (-1, 1):  # front lip
            m.span("shelf_lip", (x0, s * GANTRY_HY - 0.004, z), (x1, s * GANTRY_HY + 0.004, z + 0.02), "shelf")
    m.span("gantry_top", (x0 - 0.02, -GANTRY_HY - 0.02, GANTRY_TOP), (x1 + 0.02, GANTRY_HY + 0.02, GANTRY_TOP + 0.025), "shelf", solid=True)
    m.span("divider", (x0, -0.004, SHELF_Z[0]), (x1, 0.004, GANTRY_TOP), "white_matte")
    m.span("splash_glass", (x0, -0.005, BENCH_TOP), (x1, 0.005, SHELF_Z[0] - 0.012), "glass_clear", solid=True)

    library(m)


def library(m):
    """Scatter the barcode catalogue over the gantry: one bottle per sample.

    Every sample the scene does not place by hand stands here once, and deliberately
    in no order at all. Powder bottles and liquid flasks, large and small, are dealt
    at random over all four shelves and both faces; along a shelf the gaps are
    uneven, some bottles are pushed further back than others, and every label is
    turned a little off the aisle. The point is a library a detector cannot learn by
    position: nothing about where a bottle stands says what it is.

    Bottles never overlap along a shelf, so none hides another's label outright.
    They are the light stand-ins from assets/labelled_bottles (a kit bottle is
    14 000 to 50 000 triangles, a stand-in about 1 500), but the sticker is the real
    one, at half the texture resolution. Geoms are named lib_<sample id>_<part>, so
    a render's segmentation says which sample it is looking at.
    """
    manifest = json.loads((BOTTLES / "manifest.json").read_text())
    vessels = manifest["vessels"]
    samples = {k: v for k, v in manifest["samples"].items() if k not in PLACED_BY_SCENE}
    width_of = {k: vessels[v["vessel_class"]]["diameter_m"] for k, v in samples.items()}
    part_material = {"body": "sample_hdpe", "cap": "sample_cap", "glass": "amber"}
    scatter = np.random.default_rng(11)

    # Deal the samples out: each goes to a face drawn at random from those that
    # still have room for it, so some faces end up crowded and some nearly bare.
    faces = [(z, i, side) for z in SHELF_Z for side in (-1, 1) for i in range(MODULES)]
    stock = {face: [] for face in faces}
    room = {face: 2 * SHELF_FACE_HALF_WIDTH - SHELF_MIN_GAP for face in faces}
    for sample_id in scatter.permutation(sorted(samples)):
        need = width_of[sample_id] + SHELF_MIN_GAP
        open_faces = [face for face in faces if room[face] >= need]
        face = open_faces[scatter.integers(len(open_faces))]
        stock[face].append(str(sample_id))
        room[face] -= need

    m.comment(f"Sample library: {len(samples)} barcoded bottles, one per catalogue sample that "
              "the scene does not place itself, scattered over the gantry in no order: powders "
              "(white HDPE) and liquids (amber glass) mixed on every shelf.")
    used_meshes = set()
    for (z, i, side), chunk in stock.items():
        xc = GANTRY_X0 + (i + 0.5) * MODULE
        # Split the slack at random between the gaps, ends included.
        slack = room[(z, i, side)] * scatter.dirichlet(np.ones(len(chunk) + 1))
        x = -SHELF_FACE_HALF_WIDTH
        for sample_id, before in zip(chunk, slack):
            vessel, width = samples[sample_id]["vessel_class"], width_of[sample_id]
            x += before + SHELF_MIN_GAP + width / 2
            # Walking along the +Y face the shelf reads the other way round.
            px = xc - side * x
            py = side * (GANTRY_HY - SHELF_SETBACK - width / 2
                         - scatter.uniform(0, SHELF_DEPTH_SCATTER))
            yaw = (0 if side < 0 else 180) + scatter.uniform(-SHELF_YAW_SCATTER, SHELF_YAW_SCATTER)
            x += width / 2
            for part in vessels[vessel]["parts"]:
                if part == "label_back":
                    continue   # nobody sees a shelved bottle from behind: the divider
                sticker = part == "label"
                mesh = f"{vessel}_label" if sticker else f"{vessel}_shelf_{part}"
                used_meshes.add(mesh)
                material = f"lbl_{sample_id}" if sticker else part_material[part]
                m.add(f'<geom name="lib_{sample_id}_{part}" type="mesh" mesh="{mesh}" '
                      f'pos="{fmt((px, py, z))}" euler="0 0 {yaw:.1f}" material="{material}" '
                      f'contype="0" conaffinity="0" group="1"/>')
            m.assets.append(f'<texture name="lbl_{sample_id}" type="2d" '
                            f'file="../labelled_bottles/textures/shelf/{sample_id}.png"/>')
            m.assets.append(f'<material name="lbl_{sample_id}" texture="lbl_{sample_id}" '
                            f'specular="0.05" shininess="0.1"/>')
    for mesh in sorted(used_meshes):
        m.assets.append(f'<mesh name="{mesh}" file="../labelled_bottles/meshes/{mesh}.obj" '
                        f'inertia="shell"/>')


def bench_props(m):
    top = BENCH_TOP
    m.comment("Balance mats with red/orange frames (the balances themselves are attached by the scene).")
    for x, y in ((-1.85, -0.51), (0.75, 0.51)):
        m.box("mat", (x, y, top + 0.002), (0.17, 0.19, 0.002), "dark")
        for dx, dy, hx, hy in ((0, 0.185, 0.17, 0.008), (0, -0.185, 0.17, 0.008), (0.165, 0, 0.008, 0.19), (-0.165, 0, 0.008, 0.19)):
            m.box("mat_frame", (x + dx, y + dy, top + 0.0025), (hx, hy, 0.0025), "orange")

    m.comment("Platform scale at the near end of the bench, with its indicator and cable.")
    m.box("platform_base", (-2.72, -0.25, top + 0.04), (0.2, 0.2, 0.04), "grey_device", solid=True)
    m.box("platform_pan", (-2.72, -0.25, top + 0.085), (0.21, 0.21, 0.005), "steel", solid=True)
    m.box("indicator", (-2.72, 0.35, top + 0.08), (0.12, 0.05, 0.08), "grey_device", solid=True, euler=(0.3, 0, 0))
    m.box("indicator_screen", (-2.72, 0.302, top + 0.1), (0.07, 0.003, 0.025), "screen", euler=(0.3, 0, 0))
    m.rod("cable", (-2.72, -0.04, top + 0.01), (-2.70, 0.15, top + 0.008), 0.004, "dark")
    m.rod("cable", (-2.70, 0.15, top + 0.008), (-2.72, 0.30, top + 0.02), 0.004, "dark")

    m.comment("Work stations: white trays with pipettes and smelling strips, beakers, tent cards.")
    for x, s in ((-1.35, -1), (-0.55, 1), (0.25, -1), (1.55, 1)):
        y = s * 0.52
        m.box("tray", (x, y, top + 0.006), (0.16, 0.11, 0.006), "white_matte")
        for k in range(4):
            m.rod("pipette", (x - 0.12, y - 0.06 + k * 0.03, top + 0.016), (x + 0.1, y - 0.06 + k * 0.03, top + 0.016), 0.004, "glass_clear", kind="cylinder")
        m.mesh("beaker", "beaker", (x + 0.24, y - s * 0.04, top), "glass_clear")
        for k in range(5):  # smelling strips in the beaker
            a = (k - 2) * 0.12
            m.box("strip", (x + 0.24 + 0.02 * math.sin(a), y - s * 0.04, top + 0.13), (0.004, 0.0004, 0.07), "paper", euler=(0, a, 0))
        # Tent card: two leaning leaves.
        for tilt in (0.25, -0.25):
            m.box("tent_card", (x - 0.25, y + s * (0.08 + 0.012 * (tilt > 0)), top + 0.045), (0.06, 0.0006, 0.047), "paper", euler=(tilt, 0, 0))
        m.mesh("beaker", "beaker", (x - 0.12, y + s * 0.12, top), "glass_clear")

    m.comment("Wash zone at the head of the bench, by the sink: induction hob, covered pot, "
              "deionised-water carboy with a blue tap, wash bottles, funnel.")
    m.box("hob", (2.35, -0.5, top + 0.03), (0.3, 0.2, 0.03), "black", solid=True)
    m.box("hob_frame", (2.35, -0.5, top + 0.029), (0.305, 0.205, 0.029), "steel")
    m.mesh("pot", "pot_small", (2.3, -0.5, top + 0.06), "steel")
    m.mesh("pot_lid", "lid", (2.3, -0.5, top + 0.185), "steel")
    m.mesh("carboy", "carboy", (2.8, -0.35, top), "hdpe_white")
    m.cyl("carboy_cap", (2.8, -0.35, top + 0.5), 0.045, 0.02, "black")
    m.rod("carboy_handle", (2.8, -0.42, top + 0.44), (2.8, -0.28, top + 0.44), 0.012, "black")
    m.rod("carboy_tap", (2.8, -0.51, top + 0.06), (2.8, -0.56, top + 0.06), 0.015, "blue_hdpe", kind="cylinder")
    for k, (x, y) in enumerate(((2.55, -0.2), (2.62, -0.13), (2.48, -0.14))):
        m.mesh("wash_bottle", "wash_bottle", (x, y, top), "hdpe_white")
        m.cyl("wash_cap", (x, y, top + 0.2), 0.018, 0.012, "red_cap")
        m.rod("wash_nozzle", (x, y, top + 0.21), (x - 0.05, y, top + 0.25), 0.003, "hdpe_white")
    m.mesh("funnel", "funnel", (2.05, -0.2, top), "hdpe_white")

    m.comment("Drying rack at the far end: white plastic-coated wire grid with pegs, drip tray, "
              "flasks and cylinders hung upside down.")
    x0, x1, yb = 2.12, 2.92, 0.12
    m.box("drip_tray", ((x0 + x1) / 2, yb + 0.12, top + 0.012), ((x1 - x0) / 2, 0.12, 0.012), "white_matte")
    for x in np.linspace(x0, x1, 9):
        m.rod("rack_wire", (x, yb, top + 0.02), (x, yb, top + 0.78), 0.004, "white", kind="cylinder")
    for z in np.linspace(top + 0.03, top + 0.78, 7):
        m.rod("rack_wire", (x0, yb, z), (x1, yb, z), 0.004, "white", kind="cylinder")
    m.rod("rack_foot", (x0, yb, top + 0.02), (x0, yb + 0.22, top + 0.02), 0.006, "white", kind="cylinder")
    m.rod("rack_foot", (x1, yb, top + 0.02), (x1, yb + 0.22, top + 0.02), 0.006, "white", kind="cylinder")
    items = ["flask", "cylinder", "flask", "flask", "cylinder", "flask", "flask", "flask"]
    for k, x in enumerate(np.linspace(x0 + 0.06, x1 - 0.06, 8)):
        z = top + (0.52 if k % 2 == 0 else 0.3) + (0.2 if items[k] == "cylinder" else 0)
        m.rod("peg", (x, yb, z), (x, yb + 0.12, z + 0.05), 0.004, "white")
        mesh = items[k]
        length = 0.305 if mesh == "cylinder" else 0.195
        if z - length < top + 0.05:
            continue
        m.mesh("drying", mesh, (x, yb + 0.1, z + 0.05), "glass_clear", euler=(180, 0, 0))


def snorkels(m):
    m.comment("Articulated fume-extraction arms (snorkels) hanging over the bench.")
    for x, s in ((-1.9, -1), (-0.45, 1), (1.0, -1), (2.35, 1)):
        base = np.array([x, s * 0.55, H])
        elbow1 = base + (0.0, s * 0.05, -0.45)
        elbow2 = elbow1 + (0.35, s * 0.1, -0.05)
        hood = elbow2 + (0.05, s * 0.05, -0.28)
        m.cyl("snorkel_mount", base - (0, 0, 0.03), 0.07, 0.03, "white", kind="cylinder")
        for a, b in ((base, elbow1), (elbow1, elbow2), (elbow2, hood + (0, 0, 0.2))):
            m.rod("snorkel_tube", a, b, 0.038, "white")
        for p in (elbow1, elbow2):
            m.cyl("snorkel_joint", p, 0.05, 0.0, "grey_device", kind="sphere")
        m.mesh("snorkel_hood", "hood", hood, "white")


# =============================================================================
# Right wall bench, entrance corner, far end
# =============================================================================

def wall_bench(m):
    y_back, y_front = Y0, Y0 + WB_DEPTH
    m.comment("Right wall bench: white low units with open leg bays, glossy top.")
    m.span("wb_top", (WB_X0, y_back, BENCH_TOP - 0.04), (WB_X1, y_front + 0.02, BENCH_TOP), "worktop", solid=True)
    bays = ["units", "open", "units", "open", "units", "open", "units", "units"]
    w = (WB_X1 - WB_X0) / len(bays)
    for i, kind in enumerate(bays):
        x0 = WB_X0 + i * w
        if kind == "open":
            m.span("wb_side", (x0 - 0.01, y_back, 0), (x0 + 0.01, y_front, BENCH_TOP - 0.04), "white")
            continue
        m.span("wb_unit", (x0 + 0.004, y_back, 0.1), (x0 + w - 0.004, y_front - 0.02, BENCH_TOP - 0.04), "white", solid=True)
        m.span("plinth", (x0, y_back, 0), (x0 + w, y_front - 0.06, 0.1), "seam")
        m.span("door_gap", (x0 + w / 2 - 0.002, y_front - 0.021, 0.12), (x0 + w / 2 + 0.002, y_front - 0.019, BENCH_TOP - 0.06), "panel_joint")
        for s in (-1, 1):
            m.span("pull", (x0 + w / 2 + s * 0.03 - 0.006, y_front - 0.02, 0.62), (x0 + w / 2 + s * 0.03 + 0.006, y_front - 0.005, 0.78), "steel")

    top = BENCH_TOP
    m.comment("Wall-bench equipment, entrance to far end: bulky grey unit with vents, microwave, "
              "overhead stirrer on a stand, second stand, controller with display, trays, boxes.")
    y = y_back + 0.35
    m.box("device", (-4.55, y, top + 0.2), (0.3, 0.25, 0.2), "grey_device", solid=True)
    for k in range(8):
        m.box("vent", (-4.249, y - 0.14 + k * 0.04, top + 0.2), (0.001, 0.012, 0.12), "dark")
    m.box("microwave", (-3.85, y + 0.05, top + 0.15), (0.25, 0.2, 0.15), "white", solid=True)
    m.box("microwave_door", (-3.9, y + 0.251, top + 0.15), (0.18, 0.002, 0.12), "black")
    stand_x = -2.6  # overhead stirrer: base plate, rod, clamp, blue motor, shaft
    m.box("stand_base", (stand_x, y, top + 0.01), (0.12, 0.18, 0.01), "dark")
    m.rod("stand_rod", (stand_x, y - 0.12, top + 0.02), (stand_x, y - 0.12, top + 0.85), 0.007, "steel", kind="cylinder")
    m.box("clamp", (stand_x, y - 0.05, top + 0.6), (0.02, 0.07, 0.02), "steel")
    m.cyl("stirrer_motor", (stand_x, y + 0.04, top + 0.62), 0.045, 0.11, "blue_motor", kind="cylinder")
    m.rod("stirrer_shaft", (stand_x, y + 0.04, top + 0.5), (stand_x, y + 0.04, top + 0.15), 0.004, "steel", kind="cylinder")
    m.mesh("beaker", "beaker", (stand_x, y + 0.04, top + 0.02), "glass_clear")
    m.box("stand_base", (-2.1, y, top + 0.01), (0.1, 0.15, 0.01), "dark")
    m.rod("stand_rod", (-2.1, y - 0.1, top + 0.02), (-2.1, y - 0.1, top + 0.7), 0.007, "steel", kind="cylinder")
    m.box("clamp", (-2.1, y - 0.04, top + 0.45), (0.018, 0.06, 0.018), "steel")
    m.box("controller", (-1.35, y, top + 0.07), (0.16, 0.14, 0.07), "grey_device", solid=True)
    m.box("controller_display", (-1.35, y + 0.141, top + 0.09), (0.06, 0.001, 0.025), "screen")
    m.box("hotplate", (-0.85, y + 0.05, top + 0.05), (0.13, 0.17, 0.05), "white", solid=True)
    m.cyl("hotplate_top", (-0.85, y + 0.02, top + 0.101), 0.09, 0.002, "grey_device", kind="cylinder")
    for x in (-0.25, 0.25):
        m.box("tray", (x, y + 0.05, top + 0.03), (0.2, 0.15, 0.03), "white_matte")
    for x, dz in ((0.85, 0.12), (1.2, 0.09), (1.2, 0.27)):
        m.box("box", (x, y, top + dz), (0.16, 0.2, 0.09), "cardboard", solid=dz < 0.2)

    m.comment("Under the wall bench: kraft fibre drums with metal rings and blue carboys.")
    for x in (-3.88, -3.42):  # open bay 1
        drum(m, x, Y0 + 0.3)
    drum(m, -2.08, Y0 + 0.3)  # open bay 3
    for x in (-1.62, -0.3, 0.1):  # open bays 3 and 5
        jerrycan(m, x, Y0 + 0.3, 0)
    m.comment("Perforated white step stool.")
    m.span("stool", (-3.1, Y0 + 0.78, 0), (-2.7, Y0 + 1.08, 0.26), "white", solid=True)
    for dx in np.linspace(-0.14, 0.14, 5):
        for dy in (-0.07, 0.0, 0.07):
            m.cyl("stool_hole", (-2.9 + dx, Y0 + 0.93 + dy, 0.2601), 0.012, 0.0005, "dark", kind="cylinder")


def drum(m, x, y):
    m.mesh("drum", "drum", (x, y, 0), "kraft")
    for z in (0.02, 0.31, 0.6):
        m.cyl("drum_ring", (x, y, z), 0.226, 0.012, "steel", kind="cylinder")
    m.cyl("drum_lid", (x, y, 0.625), 0.224, 0.006, "dark", kind="cylinder")


def jerrycan(m, x, y, z0, yaw=0.0):
    m.box("jerrycan", (x, y, z0 + 0.17), (0.13, 0.09, 0.17), "blue_hdpe", solid=True, euler=(0, 0, yaw) if yaw else None)
    m.rod("jerrycan_handle", (x - 0.08, y, z0 + 0.37), (x + 0.02, y, z0 + 0.37), 0.015, "blue_hdpe")
    m.cyl("jerrycan_cap", (x + 0.08, y, z0 + 0.36), 0.025, 0.02, "blue_hdpe", kind="cylinder")


def entrance_corner(m):
    top = BENCH_TOP
    m.comment("Entrance corner: L-shaped counter (the pot, HDPE jars and bottles on it are "
              "attached below), sachets and papers.")
    m.span("counter", (X0, Y0, 0), (X0 + 1.5, Y0 + 0.7, top), "white", solid=True)
    m.span("counter", (X0, Y0 + 0.7, 0), (X0 + 0.7, Y0 + 1.6, top), "white", solid=True)
    m.span("counter_top", (X0, Y0, top - 0.03), (X0 + 1.52, Y0 + 0.72, top), "worktop")
    m.span("counter_top", (X0, Y0 + 0.7, top - 0.03), (X0 + 0.72, Y0 + 1.62, top), "worktop")
    m.mesh("pot", "pot", (X0 + 0.35, Y0 + 0.35, top), "steel")
    for s in (-1, 1):
        m.rod("pot_handle", (X0 + 0.35 + s * 0.16, Y0 + 0.35, top + 0.19), (X0 + 0.35 + s * 0.2, Y0 + 0.35, top + 0.19), 0.012, "steel")
    for k, (x, y, a) in enumerate(((X0 + 0.95, Y0 + 0.2, 0.3), (X0 + 1.08, Y0 + 0.28, -0.4), (X0 + 0.4, Y0 + 1.25, 0.1))):
        m.box("sachet", (x, y, top + 0.004 + 0.003 * k), (0.07, 0.1, 0.003), "foil", euler=(0, 0, a))
    for k, (x, y, a) in enumerate(((X0 + 1.3, Y0 + 0.45, 0.1), (X0 + 0.25, Y0 + 1.1, -0.2), (X0 + 0.3, Y0 + 1.42, 0.3))):
        m.box("paper", (x, y, top + 0.001 + 0.0005 * k), (0.105, 0.1485, 0.0005), "paper", euler=(0, 0, a))

    m.comment("Stainless two-tier trolley with bags of powder, papers and jars.")
    tx, ty = X0 + 1.95, Y0 + 0.5
    for dx in (-0.38, 0.38):
        for dy in (-0.23, 0.23):
            m.rod("trolley_post", (tx + dx, ty + dy, 0.08), (tx + dx, ty + dy, 0.9), 0.012, "steel", kind="cylinder")
            m.cyl("trolley_wheel", (tx + dx, ty + dy, 0.05), 0.05, 0.015, "dark", euler=(90, 0, 0), kind="cylinder")
    for z in (0.25, 0.85):
        m.box("trolley_tray", (tx, ty, z), (0.4, 0.25, 0.012), "steel", solid=True)
    m.rod("trolley_handle", (tx - 0.38, ty - 0.23, 0.98), (tx - 0.38, ty + 0.23, 0.98), 0.012, "steel", kind="cylinder")
    for k, (dx, dy) in enumerate(((-0.2, -0.08), (0.05, 0.08), (0.22, -0.05))):
        m.box("powder_bag", (tx + dx, ty + dy, 0.9), (0.09, 0.13, 0.04), "bag", euler=(0, 0, 0.3 * k))
    m.box("bag_on_shelf", (tx - 0.1, ty, 0.3), (0.12, 0.15, 0.04), "bag")
    m.box("paper", (tx + 0.25, ty + 0.1, 0.9 + 0.013), (0.105, 0.1485, 0.0005), "paper", euler=(0, 0, 0.2))

    m.comment("Blue HDPE carboy on the floor.")
    jerrycan(m, X0 + 1.2, Y0 + 1.0, 0, yaw=0.4)

    m.comment("Tall flammables safety cabinet (cream, blue stripe on the door edge), lidded bin, boxes.")
    cx0, cx1 = X0 + 0.25, X0 + 0.85
    m.span("safety_cabinet", (cx0, Y1 - 0.5, 0), (cx1, Y1, 1.95), "cream", solid=True)
    m.span("cabinet_stripe", (cx1 - 0.05, Y1 - 0.502, 0.05), (cx1 - 0.01, Y1 - 0.5, 1.9), "stripe_blue")
    m.span("cabinet_gap", ((cx0 + cx1) / 2 - 0.002, Y1 - 0.502, 0.05), ((cx0 + cx1) / 2 + 0.002, Y1 - 0.5, 1.9), "panel_joint")
    m.box("warning_label", ((cx0 + cx1) / 2 - 0.12, Y1 - 0.503, 1.4), (0.05, 0.001, 0.05), "orange")
    m.mesh("bin", "bin", (X0 + 1.1, Y1 - 0.3, 0), "white")
    m.mesh("bin_lid", "bin_lid", (X0 + 1.1, Y1 - 0.3, 0.62), "white")
    m.box("box", (X0 + 1.5, Y1 - 0.25, 0.15), (0.2, 0.2, 0.15), "cardboard", solid=True)
    m.box("box", (X0 + 1.52, Y1 - 0.25, 0.39), (0.17, 0.15, 0.09), "cardboard", euler=(0, 0, 0.2))

    m.comment("Storage 'niche': industrial rack, red uprights and navy beams, holding boxes.")
    rx0, rx1 = -6.0, -5.1
    for x in (rx0, rx1):
        for yy in (Y0 + 0.02, Y0 + 0.55):
            m.span("rack_upright", (x - 0.03, yy - 0.02, 0), (x + 0.03, yy + 0.02, 2.2), "red_rack", solid=True)
    for z in (0.12, 0.8, 1.45, 2.1):
        for yy in (Y0 + 0.02, Y0 + 0.55):
            m.span("rack_beam", (rx0, yy - 0.02, z - 0.05), (rx1, yy + 0.02, z + 0.05), "navy_rack")
        m.span("rack_deck", (rx0, Y0, z + 0.05), (rx1, Y0 + 0.57, z + 0.065), "galvanised", solid=True)
    for k, (x, z, hz) in enumerate(((-5.78, 0.065, 0.14), (-5.32, 0.065, 0.2), (-5.75, 0.815, 0.18), (-5.3, 0.815, 0.12),
                                   (-5.55, 1.465, 0.2), (-5.78, 2.115, 0.1), (-5.32, 2.115, 0.15))):
        m.box("box", (x, Y0 + 0.28, z + hz), (0.2, 0.22, hz), "cardboard" if k % 3 else "white_matte")


def instrument_bench(m):
    m.comment("Instrument bench on the left wall for the GC-MS and the UV-Vis-NIR (attached by the scene).")
    x0, x1 = -6.6, -3.8
    m.span("ib_top", (x0, Y1 - 0.75, BENCH_TOP - 0.04), (x1, Y1, BENCH_TOP), "worktop", solid=True)
    for x in np.linspace(x0 + 0.05, x1 - 0.05, 4):
        m.span("ib_leg", (x - 0.03, Y1 - 0.7, 0), (x + 0.03, Y1 - 0.64, BENCH_TOP - 0.04), "white")
        m.span("ib_leg", (x - 0.03, Y1 - 0.1, 0), (x + 0.03, Y1 - 0.04, BENCH_TOP - 0.04), "white")
        for yy in (Y1 - 0.67, Y1 - 0.07):
            m.cyl("ib_leveling_foot", (x, yy, 0.016), 0.042, 0.016, "dark")
            m.cyl("ib_foot_stem", (x, yy, 0.044), 0.013, 0.025, "steel")
        m.span("ib_crossmember", (x - 0.022, Y1 - 0.7, 0.77), (x + 0.022, Y1 - 0.04, 0.82), "white")
    for yy in (Y1 - 0.67, Y1 - 0.07):
        m.span("ib_apron", (x0 + 0.03, yy - 0.022, 0.78), (x1 - 0.03, yy + 0.022, 0.855), "white")
    m.span("ib_rail", (x0, Y1 - 0.1, 0.12), (x1, Y1 - 0.04, 0.16), "white")


def far_end(m):
    m.comment("Far end: workstation against the glass (desk, monitor, office chair).")
    dx, dy = X1 - 0.4, -1.9
    m.span("desk_top", (dx - 0.35, dy - 0.75, 0.72), (dx + 0.35, dy + 0.75, 0.75), "white", solid=True)
    for sy in (-0.7, 0.7):
        m.span("desk_leg", (dx - 0.33, dy + sy - 0.02, 0), (dx + 0.33, dy + sy + 0.02, 0.72), "white")
    m.box("monitor", (dx + 0.15, dy, 1.05), (0.02, 0.3, 0.18), "dark")
    m.box("monitor_screen", (dx + 0.129, dy, 1.05), (0.001, 0.28, 0.16), "screen")
    m.rod("monitor_stand", (dx + 0.18, dy, 0.75), (dx + 0.18, dy, 0.9), 0.02, "dark", kind="cylinder")
    m.box("keyboard", (dx - 0.1, dy, 0.76), (0.07, 0.22, 0.01), "dark")
    chair(m, dx - 0.7, dy + 0.1, yaw=0.3)


def chair(m, x, y, yaw=0.0):
    for k in range(5):
        a = yaw + 2 * math.pi * k / 5
        m.rod("chair_star", (x, y, 0.08), (x + 0.3 * math.cos(a), y + 0.3 * math.sin(a), 0.06), 0.015, "dark")
        m.cyl("chair_wheel", (x + 0.3 * math.cos(a), y + 0.3 * math.sin(a), 0.03), 0.028, 0.0, "dark", kind="sphere")
    m.rod("chair_column", (x, y, 0.08), (x, y, 0.44), 0.025, "steel", kind="cylinder")
    m.box("chair_seat", (x, y, 0.47), (0.24, 0.24, 0.035), "dark")
    bx, by = x - 0.24 * math.cos(yaw), y - 0.24 * math.sin(yaw)
    m.box("chair_back", (bx, by, 0.8), (0.03, 0.22, 0.24), "dark", euler=(0, -0.1, math.degrees(yaw)))


def office_beyond(m):
    m.comment("Beyond the glass: the neighbouring lab/office (desks, monitors, staff in coats and caps).")
    m.span("office_floor", (X1 + 0.02, -6.0, 0.0), (X1 + 5.0, Y1 + 2.0, 0.002), "floor")
    m.span("office_wall", (X1 + 5.0, -6.0, 0), (X1 + 5.1, Y1 + 2.0, H), "panel")
    m.span("corridor_floor", (-1.0, -6.0, 0.0), (X1 + 0.02, Y0 - 0.02, 0.002), "floor")
    m.span("corridor_wall", (-1.0, -6.1, 0), (X1 + 5.0, -6.0, H), "panel")
    m.span("office_ceiling", (X1 + 0.02, -6.0, H), (X1 + 5.0, Y1 + 2.0, H + 0.04), "ceiling", group=2)
    m.span("corridor_ceiling", (-1.0, -6.0, H), (X1 + 0.02, Y0 - 0.02, H + 0.04), "ceiling", group=2)
    m.span("office_wall", (X1 + 0.02, Y1 + 2.0, 0), (X1 + 5.0, Y1 + 2.1, H), "panel")
    for x, y in ((X1 + 1.6, -1.8), (X1 + 1.6, 0.6), (X1 + 3.4, -1.8), (X1 + 3.4, 0.6)):
        m.span("office_desk", (x - 0.4, y - 0.8, 0.72), (x + 0.4, y + 0.8, 0.75), "desk")
        for sy in (-0.75, 0.75):
            m.span("office_desk_leg", (x - 0.38, y + sy - 0.02, 0), (x + 0.38, y + sy + 0.02, 0.72), "dark")
        m.box("office_monitor", (x + 0.2, y, 1.02), (0.02, 0.28, 0.17), "dark")
        m.box("office_screen", (x + 0.179, y, 1.02), (0.001, 0.26, 0.15), "screen")
        chair(m, x - 0.6, y, yaw=0.0)
    person(m, X1 + 1.0, -0.5, facing=0.0)
    person(m, X1 + 2.6, 1.3, facing=math.pi)
    person(m, 3.8, -4.2, facing=math.pi / 2)


def person(m, x, y, facing):
    """Static staff figure in a local +X-facing frame, with a relaxed bent-arm pose."""
    m.add(f'<frame pos="{x:g} {y:g} 0" euler="0 0 {math.degrees(facing):g}">')
    for side in (-1, 1):
        yy = side * 0.095
        m.ellipsoid("shoe", (0.055, yy, 0.055), (0.145, 0.064, 0.05), "dark")
        m.rod("trouser_calf", (0, yy, 0.13), (-0.025, yy, 0.47), 0.059, "trousers")
        m.rod("trouser_thigh", (-0.025, yy, 0.47), (0, yy, 0.86), 0.075, "trousers")
        shoulder = (0, side * 0.19, 1.39)
        elbow = (0.035, side * 0.235, 1.16)
        wrist = (0.17, side * 0.20, 1.05 + 0.06 * (side > 0))
        m.rod("sleeve_upper", shoulder, elbow, 0.066, "coat")
        m.rod("sleeve_lower", elbow, wrist, 0.048, "coat")
        m.ellipsoid("hand", (wrist[0] + 0.036, wrist[1], wrist[2] - 0.026), (0.052, 0.028, 0.061), "skin")
        m.ellipsoid("thumb", (wrist[0] + 0.055, wrist[1] - side * 0.027, wrist[2]), (0.024, 0.017, 0.031), "skin")
        m.box("coat_pocket", (0.128, side * 0.105, 1.04), (0.004, 0.045, 0.055), "white_matte")
        m.rod("pocket_stitch", (0.134, side * 0.105 - 0.044, 1.084), (0.134, side * 0.105 + 0.044, 1.084), 0.0015, "seam")
    # One continuous coat silhouette instead of separate capsule body segments.
    if "coat_mesh" not in m.bevel_meshes:
        vertices = []
        for z, rx, ry in ((0.78, 0.125, 0.19), (0.83, 0.14, 0.195),
                           (1.12, 0.13, 0.17), (1.36, 0.13, 0.195),
                           (1.43, 0.10, 0.17), (1.47, 0.065, 0.075)):
            for i in range(32):
                a = math.tau * i / 32
                vertices.extend((rx * math.cos(a), ry * math.sin(a), z))
        m.bevel_meshes["coat_mesh"] = ("staff_coat", vertices)
    m.mesh("coat_body", "staff_coat", (0, 0, 0), "coat")
    m.rod("coat_seam", (0.142, 0, 0.84), (0.134, 0, 1.37), 0.002, "seam")
    for z in (1.0, 1.10, 1.20, 1.30):
        m.ellipsoid("coat_button", (0.14, 0, z), (0.003, 0.007, 0.007), "white_matte")
    for side in (-1, 1):
        m.rod("collar", (0.075, side * 0.065, 1.47), (0.131, side * 0.055, 1.35), 0.024, "white")
    m.box("id_badge", (0.135, -0.09, 1.32), (0.004, 0.032, 0.043), "stripe_blue")
    m.box("id_insert", (0.14, -0.09, 1.32), (0.001, 0.026, 0.026), "paper")
    m.rod("neck", (0, 0, 1.44), (0, 0, 1.54), 0.048, "skin")
    m.ellipsoid("head", (0, 0, 1.615), (0.087, 0.078, 0.119), "skin")
    m.ellipsoid("jaw", (0.026, 0, 1.556), (0.068, 0.061, 0.048), "skin")
    m.ellipsoid("nose", (0.088, 0, 1.614), (0.027, 0.018, 0.028), "skin")
    for side in (-1, 1):
        m.ellipsoid("ear", (0, side * 0.078, 1.61), (0.022, 0.012, 0.033), "skin")
        m.ellipsoid("eye", (0.077, side * 0.034, 1.644), (0.009, 0.016, 0.008), "white")
        m.ellipsoid("pupil", (0.085, side * 0.034, 1.644), (0.003, 0.006, 0.006), "dark")
        m.rod("eyebrow", (0.079, side * 0.019, 1.661), (0.073, side * 0.051, 1.663), 0.003, "trousers")
    m.rod("mouth", (0.085, -0.021, 1.579), (0.085, 0.021, 1.579), 0.002, "kraft")
    m.ellipsoid("disposable_cap", (-0.013, 0, 1.713), (0.09, 0.087, 0.048), "cap_blue")
    m.add('</frame>')


def cameras(m):
    m.comment("Cameras along the video's path: entrance corner, down the aisle, the library, "
              "the wash zone, the drying rack. Plus a top-down overview (hide group 2).")
    views = {
        "entrance": ((X0 + 0.5, Y0 + 1.2, 1.65), (X0 + 4.0, -0.3, 1.1)),
        "aisle": ((-4.2, -1.45, 1.6), (0.0, -0.9, 1.2)),
        "library": ((-0.4, -2.2, 1.55), (-0.4, 0.0, 1.6)),
        "wash": ((1.6, -1.6, 1.6), (3.0, -0.3, 1.0)),
        "drying_rack": ((1.2, 1.4, 1.6), (2.6, 0.2, 1.2)),
        "far_end": ((-1.0, 1.4, 1.7), (X1, -0.8, 1.2)),
        "overview": (((X0 + X1) / 2, -0.4, 13.5), ((X0 + X1) / 2, -0.39, 0.0)),
    }
    for name, (eye, target) in views.items():
        eye, target = np.array(eye, float), np.array(target, float)
        f = (target - eye) / np.linalg.norm(target - eye)
        right = np.cross(f, (0, 0, 1))
        right = right / np.linalg.norm(right) if np.linalg.norm(right) > 1e-6 else np.array([1.0, 0, 0])
        up = np.cross(right, f)
        fovy = 60 if name != "overview" else 50
        m.add(f'<camera name="{name}" pos="{fmt(eye)}" xyaxes="{fmt(right)} {fmt(up)}" fovy="{fovy}"/>')


def main() -> None:
    mesh_names = build_meshes()
    m = Mjcf()
    shell(m)
    ceiling(m)
    lights(m)
    central_bench(m)
    gantry(m)
    bench_props(m)
    snorkels(m)
    wall_bench(m)
    entrance_corner(m)
    instrument_bench(m)
    far_end(m)
    office_beyond(m)
    cameras(m)

    materials = "\n".join(f'    <material name="{k}" {v}/>' for k, v in MATERIALS.items())
    meshes = "\n".join([f'    <mesh name="{n}" file="meshes/{n}.obj" inertia="shell"/>' for n in mesh_names]
                       + [f"    {line}" for line in m.assets])
    meshes += "\n" + "\n".join(
        f'    <mesh name="{name}" vertex="{fmt(vertices)}"/>'
        for name, vertices in m.bevel_meshes.values())
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<!-- Generated by scripts/generate_lab_room.py - do not edit by hand.
     Perfumery lab around the minihannover bench: interior {X1 - X0:g} x {Y1 - Y0:g} x {H:g} m,
     x in [{X0:g}, {X1:g}], y in [{Y0:g}, {Y1:g}], in the bench's frame. Attach body "lab_room"
     at the origin. Ceiling geoms are in group 2. -->
<mujoco model="lab_room">
  <asset>
{materials}
{meshes}
  </asset>
  <worldbody>
    <body name="lab_room">
{chr(10).join(m.lines)}
    </body>
  </worldbody>
</mujoco>
"""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "lab_room.xml").write_text(xml)
    print(f"lab_room: {sum(1 for l in m.lines if '<geom' in l)} geoms, {len(mesh_names)} meshes -> {OUT}")


if __name__ == "__main__":
    main()
