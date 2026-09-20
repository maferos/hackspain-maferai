#!/usr/bin/env python3
"""The amber bottle catalogue: dimensions and meshes for every size.

Run from anywhere: python uncap-robustness/bottles.py

Reads ``assets/amber-bottles/glb/amber_bottle_<ml>ml.glb`` (the bottle with
its cap, closed), splits it into the glass and the cap by material, and writes
both as STL into ``cache/``: the glass from the bottle's base, the cap from its
own underside. The dimensions are the generator's own formulas
(``generate_amber_bottles.py``: ``bottle_dims``, ``cap_dims``; that module
needs bpy, so they are repeated here) and are checked against the meshes.
"""
import math
import struct
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'simulation/tools'))
from convert_glb import Y_UP_TO_Z_UP, Glb  # noqa: E402

GLB_DIR = ROOT / 'assets/amber-bottles/glb'
CACHE = HERE / 'cache'
SIZES = (10, 20, 30, 50, 60, 100)
# generate_amber_bottles.py
REF_ML, REF_DIAM, REF_HEIGHT = 60.0, 40.0, 95.0
NECK_FOR_ML = {10: 18, 20: 18, 30: 20, 50: 25, 60: 25, 100: 28}
RIB_DEPTH, THREAD_TURNS = 0.5, 2.0
GLASS_DENSITY, CAP_DENSITY, LIQUID_DENSITY = 2500.0, 905.0, 1000.0
MM = 0.001


def dims(ml: int) -> dict:
    """The bottle's and its cap's dimensions in metres, from the generator's
    formulas. Heights from the bottle's base."""
    k = (ml / REF_ML) ** (1 / 3)
    n = NECK_FOR_ML[ml]
    r, h = REF_DIAM * k / 2, REF_HEIGHT * k
    wall, floor, pushup = 1.2 + 0.8 * k, 2.5 * k, 1.0 * k
    rt = n / 2 - 0.3                      # neck thread crest
    rn = rt - 0.04 * n                    # neck root
    rb = rn - 2.0                         # bore
    hf, hb, hs = 0.55 * n + 1.0, 0.10 * n, 0.30 * 2 * r
    shoulder = h - hf - hb - hs
    neck = shoulder + hs
    cap_h, cap_top = 0.62 * n + 3.0, 1.6
    rc = n / 2 + 1.5                      # cap ribs' crest
    return {
        'ml': ml, 'neck_mm': n, 'r': r * MM, 'h': h * MM, 'wall': wall * MM, 'floor': floor * MM,
        'pushup': pushup * MM, 'shoulder': shoulder * MM, 'neck': neck * MM,
        'neck_r': (rt + 0.25) * MM,       # the tamper bead is the neck's widest point
        'neck_crest': rt * MM, 'neck_root': rn * MM, 'bore': rb * MM,
        'cap_bore': (n / 2 - 0.3 + 0.35) * MM, 'cap_top': cap_top * MM, 'cap_z': (h - (cap_h - cap_top)) * MM, 'cap_h': cap_h * MM,
        'cap_rib_r': rc * MM, 'cap_r': (rc + 0.4) * MM,   # the tamper band, the widest
        'cap_band_h': 0.22 * cap_h * MM, 'pitch': 0.11 * n * MM, 'turns': THREAD_TURNS,
    }


def _split(ml: int) -> dict[str, np.ndarray]:
    """Triangles (n, 3, 3) of the glass and the cap, Z up, bottle frame."""
    glb = Glb(GLB_DIR / f'amber_bottle_{ml:03d}ml.glb')
    parts: dict[str, list] = {}
    scene = glb.json['scenes'][glb.json.get('scene', 0)]
    for root in scene['nodes']:
        for _, world, mesh in glb.walk(root, Y_UP_TO_Z_UP):
            for prim in mesh['primitives']:
                v = glb.accessor(prim['attributes']['POSITION'])
                f = glb.accessor(prim['indices']).reshape(-1, 3)
                v = v @ world[:3, :3].T + world[:3, 3]
                _, name = glb.colour(prim.get('material'))
                part = 'cap' if 'PP' in name else 'glass'
                parts.setdefault(part, []).append(v[f])
    return {k: np.concatenate(v) for k, v in parts.items()}


def write_stl(path: Path, tris: np.ndarray) -> None:
    tris = np.asarray(tris, np.float32)
    normals = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    normals /= np.maximum(np.linalg.norm(normals, axis=1, keepdims=True), 1e-12)
    rec = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
    data = np.zeros(len(tris), rec)
    data['n'], data['v'] = normals, tris
    path.write_bytes(b'\0' * 80 + struct.pack('<I', len(tris)) + data.tobytes())


def volume(tris: np.ndarray) -> float:
    return float(np.einsum('ij,ij->i', tris[:, 0], np.cross(tris[:, 1], tris[:, 2])).sum() / 6)


@lru_cache(maxsize=None)
def bottle(ml: int) -> dict:
    """Dimensions, masses and the cached mesh files of one size."""
    d = dims(ml)
    glass_stl, cap_stl = CACHE / f'glass_{ml:03d}ml.stl', CACHE / f'cap_{ml:03d}ml.stl'
    parts = _split(ml)
    if not glass_stl.exists() or not cap_stl.exists():
        CACHE.mkdir(exist_ok=True)
        cap = parts['cap'].copy()
        cap[..., 2] -= d['cap_z']
        write_stl(glass_stl, parts['glass'])
        write_stl(cap_stl, cap)
    d['glass_stl'], d['cap_stl'] = str(glass_stl), str(cap_stl)
    d['glass_mass'] = volume(parts['glass']) * GLASS_DENSITY
    d['cap_mass'] = volume(parts['cap']) * CAP_DENSITY
    d['mesh'] = _measure(parts, d)
    return d


def _measure(parts: dict, d: dict) -> dict:
    """What the meshes say, for the check against the formulas."""
    g, c = parts['glass'].reshape(-1, 3), parts['cap'].reshape(-1, 3)
    rg, rc = np.hypot(g[:, 0], g[:, 1]), np.hypot(c[:, 0], c[:, 1])
    body = g[:, 2] < d['shoulder'] + 1e-4   # the straight wall is one row of the lathe
    lip = np.abs(g[:, 2] - d['h']) < 0.0006
    return {'r': float(rg[body].max()), 'h': float(g[:, 2].max()), 'cap_z': float(c[:, 2].min()),
            'cap_r': float(rc.max()), 'cap_h': float(c[:, 2].max() - c[:, 2].min()),
            'bore': float(rg[lip].min())}


def liquid_height(d: dict, fill: float) -> float:
    """Height of the liquid above the inside floor for a fraction of the
    nominal volume, with the body taken as a straight cylinder (every fill
    swept stays below the shoulder; checked by the caller)."""
    ri = d['r'] - d['wall']
    return fill * d['ml'] * 1e-6 / (math.pi * ri * ri)


def main() -> None:
    print(f'{"ml":>4} {"neck":>4} {"Ø mm":>6} {"H mm":>6} {"cap_z":>6} {"cap Ø":>6} {"bore Ø":>6} '
          f'{"glass g":>7} {"cap g":>6}  worst formula-vs-mesh')
    for ml in SIZES:
        d = bottle(ml)
        m = d['mesh']
        worst = max(abs(d[k] - m[k]) for k in ('r', 'h', 'cap_z', 'cap_r', 'cap_h', 'bore'))
        print(f'{ml:4d} PP{d["neck_mm"]:<2d} {2e3 * d["r"]:6.1f} {1e3 * d["h"]:6.1f} {1e3 * d["cap_z"]:6.1f} '
              f'{2e3 * d["cap_r"]:6.1f} {2e3 * d["bore"]:6.1f} {1e3 * d["glass_mass"]:7.1f} '
              f'{1e3 * d["cap_mass"]:6.2f}  {1e3 * worst:.2f} mm')
        for fill in (0.25, 0.5, 0.8):
            if d['floor'] + liquid_height(d, fill) > d['shoulder']:
                print(f'     fill {fill}: liquid reaches the shoulder')


if __name__ == '__main__':
    main()
