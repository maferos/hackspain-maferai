#!/usr/bin/env python3
"""Write a self-contained 3D viewer of the UR10e hand: wrist stub + flange + 2F-85.

Run from simulation/: python scripts/generate_hand_viewer.py.

Writes ``assets/ur10e_hand/ur10e_hand.html``: one file, no network needed. The
meshes are the Menagerie files themselves, base64 inside the page, and the two
sliders are the same two degrees of freedom as ``ur10e_hand.blend`` --- the
wrist roll and the jaw aperture, with the finger linkage following the aperture
through the fit in hand_linkage.py.

three.js r128 is taken from the iris clamp viewer already in the repo (MIT,
embedded there for the same reason: the file has to open offline).

Also writes ``ur10e_hand_data.js`` beside it: the same data as a script of its
own, which the template loads, so ``scripts/hand_viewer_template.html`` opens
and previews directly (with three.js from cdnjs) without generating first.
"""
import base64
import json
import re

import mujoco
import numpy as np

from hand_linkage import (GRIP_MESHES, GRIPPER, MATERIALS, MESH_MATERIAL,
                          OUT_DIR, RING_HEIGHT, SIM, STUB_LENGTH, STUB_RADIUS,
                          STUB_TOP, UR_MESHES, gripper_bodies, linkage,
                          wrist3_pose)

TEMPLATE = SIM / 'scripts/hand_viewer_template.html'
THREE_SOURCE = SIM.parent / 'assets/iris_clamp/pinza_iris_desenroscador_3d.html'
OUT = OUT_DIR / 'ur10e_hand.html'
# The same data as a script of its own, so the template previews as is.
DATA_OUT = OUT_DIR / 'ur10e_hand_data.js'


def read_stl(path) -> np.ndarray:
    """Triangles of a binary STL, (n, 3, 3), in the file's units."""
    raw = path.read_bytes()
    count = int(np.frombuffer(raw, np.uint32, 1, 80)[0])
    record = np.dtype([('normal', '<f4', 3), ('v', '<f4', (3, 3)), ('attr', '<u2')])
    return np.frombuffer(raw, record, count, 84)['v'].astype(np.float64)


def read_obj(path) -> np.ndarray:
    """Triangles of a Wavefront OBJ, (n, 3, 3); fans any polygon."""
    vertices, triangles = [], []
    for line in path.read_text().splitlines():
        if line.startswith('v '):
            vertices.append([float(x) for x in line.split()[1:4]])
        elif line.startswith('f '):
            idx = [int(tok.split('/')[0]) - 1 for tok in line.split()[1:]]
            triangles += [(idx[0], idx[k], idx[k + 1]) for k in range(1, len(idx) - 1)]
    return np.array(vertices)[np.array(triangles)]


def pack(triangles: np.ndarray) -> dict:
    """Weld a triangle soup into an indexed mesh, base64 for the page."""
    positions, index = np.unique(triangles.reshape(-1, 3).round(7), axis=0,
                                 return_inverse=True)
    index = index.ravel()
    wide = len(positions) > 65535
    return {
        'p': base64.b64encode(positions.astype('<f4').tobytes()).decode(),
        'i': base64.b64encode(index.astype('<u4' if wide else '<u2').tobytes()).decode(),
        'wide': wide,
    }


def three_js() -> str:
    """The embedded three.js r128 block from the iris clamp viewer."""
    page = THREE_SOURCE.read_text()
    match = re.search(r'<script>(/\* three\.js r128 \(MIT\).*?)</script>', page, re.DOTALL)
    if match is None:
        raise RuntimeError(f'no embedded three.js r128 in {THREE_SOURCE}')
    return match.group(1)


def main() -> None:
    closed, opened, fits = linkage()
    model = mujoco.MjModel.from_xml_path(str(GRIPPER))

    bodies, names = [], set()
    for b, name, parent, pos, quat, joint, jpos, meshes in gripper_bodies(model):
        bodies.append({'id': b, 'name': name, 'parent': parent,
                       'pos': pos.tolist(), 'quat': quat.tolist(),
                       'joint': joint, 'jpos': jpos.tolist(),
                       'meshes': [[m, MESH_MATERIAL[m]] for m in meshes]})
        names.update(meshes)
    meshes = {m: pack(read_stl(GRIP_MESHES / f'{m}.stl') * 0.001) for m in sorted(names)}
    meshes['wrist3'] = pack(read_obj(UR_MESHES / 'wrist3.obj'))
    pos, quat = wrist3_pose()

    data = {
        'aperture': [closed, opened],
        'fits': {k: v.tolist() for k, v in fits.items()},
        'bodies': bodies,
        'meshes': meshes,
        'wrist3': {'pos': pos.tolist(), 'quat': quat.tolist()},
        'stub': {'radius': STUB_RADIUS, 'length': STUB_LENGTH, 'top': STUB_TOP,
                 'ring': RING_HEIGHT},
        'materials': {k: v[:3] for k, v in MATERIALS.items()},
    }
    script = f'window.HAND_DATA={json.dumps(data, separators=(",", ":"))};'
    page = TEMPLATE.read_text()
    for marker, inline in (('THREE_JS', three_js()), ('HAND_DATA', script)):
        tag = re.search(rf'<script src="[^"]*"></script><!--{marker}-->', page)
        if tag is None:
            raise RuntimeError(f'no {marker} script tag in {TEMPLATE}')
        page = page.replace(tag.group(0), f'<script>{inline}</script>')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page)
    DATA_OUT.write_text(script + '\n')
    print(f'wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)')


if __name__ == '__main__':
    main()
