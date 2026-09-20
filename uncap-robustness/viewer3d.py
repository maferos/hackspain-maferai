#!/usr/bin/env python3
"""Write an interactive 3D page of the v3 hand playing the sequence.

    python uncap-robustness/viewer3d.py                 # the 60 ml bottle
    python uncap-robustness/viewer3d.py --bottle 10 --fill 0.5

Runs one trial, records every body's pose at 40 Hz, and writes
``out/model.html``: one file, three.js inlined, no network. The page draws
the model as MuJoCo has it — the compact V-groove gripper, the iris clamp, the
micropipette, the bottle and its cap — and plays the 19 steps, with the stage
each moment belongs to and what the trial measured.
"""
import argparse
import base64
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIM = HERE.parent / 'simulation'
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SIM / 'scripts'))

import mujoco  # noqa: E402

import gripper  # noqa: E402
import iris_pipette_plan as plan  # noqa: E402
import scene  # noqa: E402
import trial as trial_mod  # noqa: E402
from bottles import bottle  # noqa: E402
from generate_hand_viewer import pack, three_js  # noqa: E402

OUT = HERE / 'out/model.html'
FPS = 40
TYPES = {int(mujoco.mjtGeom.mjGEOM_PLANE): 'plane', int(mujoco.mjtGeom.mjGEOM_SPHERE): 'sphere',
         int(mujoco.mjtGeom.mjGEOM_CAPSULE): 'capsule', int(mujoco.mjtGeom.mjGEOM_CYLINDER): 'cylinder',
         int(mujoco.mjtGeom.mjGEOM_BOX): 'box', int(mujoco.mjtGeom.mjGEOM_MESH): 'mesh'}


def geometry(model: mujoco.MjModel) -> tuple[list, dict]:
    """Every drawable geom as a dict, plus the meshes it names."""
    geoms, meshes = [], {}
    for g in range(model.ngeom):
        kind = TYPES.get(int(model.geom_type[g]))
        if kind is None:
            continue
        rgba = model.geom_rgba[g].copy()
        mat = model.geom_matid[g]
        if mat >= 0:
            rgba = model.mat_rgba[mat].copy()
        name = model.geom(g).name
        item = {'body': int(model.geom_bodyid[g]), 'type': kind, 'name': name,
                'pos': model.geom_pos[g].tolist(), 'quat': model.geom_quat[g].tolist(),
                'size': model.geom_size[g].tolist(), 'rgba': [round(float(v), 3) for v in rgba],
                'group': int(model.geom_group[g]),
                'collision': bool(model.geom_contype[g] or model.geom_conaffinity[g])}
        if kind == 'mesh':
            mid = int(model.geom_dataid[g])
            key = model.mesh(mid).name
            if key not in meshes:
                a, n = model.mesh_vertadr[mid], model.mesh_vertnum[mid]
                fa, fn = model.mesh_faceadr[mid], model.mesh_facenum[mid]
                v = model.mesh_vert[a:a + n]
                f = model.mesh_face[fa:fa + fn]
                meshes[key] = pack(v[f])
            item['mesh'] = key
        geoms.append(item)
    return geoms, meshes


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--bottle', type=int, default=60)
    ap.add_argument('--fill', type=float, default=0.5)
    ap.add_argument('--pitch', type=float, default=0.0)
    ap.add_argument('--approach', default='above')
    a = ap.parse_args()

    t = trial_mod.Trial({'bottle': a.bottle, 'fill': a.fill, 'pitch': a.pitch, 'approach': a.approach})
    model, data = t.model, t.data
    geoms, meshes = geometry(model)

    # play it, sampling every body's pose
    poses, stamps, steps = [], [], []
    every = max(1, round(1 / (FPS * model.opt.timestep)))
    metrics = t.run(sampler=lambda tp: (poses.append(np.concatenate([data.xpos, data.xquat], axis=1).copy()),
                                        stamps.append(tp),
                                        steps.append(plan.state_at(tp, t.frames)[1])), sample_every=every)
    arr = np.asarray(poses, np.float32)
    d = bottle(a.bottle)
    page = TEMPLATE.replace('/*DATA*/', 'window.MODEL=' + json.dumps({
        'bodies': [model.body(b).name for b in range(model.nbody)],
        'geoms': geoms, 'meshes': meshes,
        'poses': {'shape': list(arr.shape), 'b64': base64.b64encode(arr.tobytes()).decode()},
        'times': [round(x, 3) for x in stamps], 'steps': steps,
        'plan': [[name, seconds] for name, seconds, _ in plan.STEPS],
        'trial': {k: (round(v, 3) if isinstance(v, float) else v) for k, v in metrics.items()
                  if not k.startswith('contacts_')},
        'bottle': {'ml': a.bottle, 'neck': d['neck_mm'], 'diameter_mm': round(2e3 * d['r'], 1),
                   'cap_z_mm': round(1e3 * d['cap_z'], 1), 'fill': a.fill},
        'hand': {'name': scene.HAND, 'axis_below_cap_mm': round(1e3 * scene.VER['axis_below_cap'], 1),
                 'jaw_stroke_mm': round(1e3 * gripper.stroke(d['r']), 1),
                 'parabola_p_mm': round(1e3 * gripper.JAW['p'], 1),
                 'contact_x_mm': round(1e3 * gripper.contact_x(d['r']), 1),
                 'contact_deg': round(math.degrees(gripper.contact_angle(d['r']))),
                 'friction': gripper.JAW['friction'][0],
                 'grip_force_N': gripper.GAINS[2], 'envelope_mm': round(1e3 * gripper.envelope()['below'], 1)},
    }, separators=(',', ':')) + ';').replace('<script src="three"></script>', f'<script>{three_js()}</script>')
    OUT.write_text(page)
    print(f'wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB): {arr.shape[0]} frames, '
          f'{len(geoms)} geoms, {len(meshes)} meshes; trial {metrics["first_failure"] or "ok"}')


TEMPLATE = (HERE / 'viewer3d_template.html').read_text() if (HERE / 'viewer3d_template.html').exists() else ''

if __name__ == '__main__':
    main()
