#!/usr/bin/env python3
"""Write a 3D viewer of the uncap-and-pipette hand: UR10e + bottle + iris clamp + micropipette.

Run from simulation/: python scripts/generate_iris_pipette_viewer.py.

Writes ``ur10e_iris_pipette.html`` at the repository root: one file, no network
needed. The assembly is iris_pipette_rig.py's: the page draws its body tree,
moves its joints through JOINT_MAP and plays iris_pipette_plan.py's steps, the
same three things the MJCF, the URDF and the .blend are built from
(generate_iris_pipette_scene.py, generate_iris_pipette_blend.py). Three assets
are combined on the UR10e's tool:

* the hand (wrist_3 flange + Robotiq 2F-85), exactly as in ``ur10e_hand.html``:
  same Menagerie meshes, same finger-linkage fit from hand_linkage.py. It grips
  the bottle from the side, tool horizontal, and takes the unscrewing torque;
* the iris clamp from ``assets/iris_clamp/iris_clamp_sim_asset.zip``, on a
  swing arm with a 90 degree hinge bolted on the gripper body, on the arm's
  side of the bottle. Swung down it sits coaxial on the cap and unscrews it;
  swung up, back over the gripper, it carries the cap clear of the neck;
* the micropipette from ``assets/micropipette/micropipette_asset.zip``, in a
  swing frame hinged on the carriage of a vertical slide beside the bottle,
  with its own plunger actuator. At a fixed height, the tip just over the
  neck, the frame swings the pipette out to the arm's side while the clamp
  works and back in over the bottle, where it seats on a cone; only then does
  the slide take it down.

The bottle's height, diameter and liquid level and the pipette's dive are
set on the page; everything on the hand is placed relative to the neck, which
all the bottles share (the cap and the clamp do not change).

The meshes are read straight out of the two zips, so nothing has to be
extracted into the repo.
"""
import json
import re
import zipfile

import mujoco
import numpy as np

import iris_pipette_plan as plan
import iris_pipette_rig as rig
from generate_hand_viewer import pack, read_obj, three_js
from hand_linkage import (GRIP_MESHES, GRIPPER, MATERIALS, MESH_MATERIAL,
                          RING_HEIGHT, SIM, STUB_LENGTH, STUB_RADIUS, STUB_TOP,
                          UR_MESHES, gripper_bodies, linkage, wrist3_pose)

TEMPLATE = SIM / 'scripts/iris_pipette_viewer_template.html'
OUT = rig.ROOT / 'ur10e_iris_pipette.html'


def read_stl(path, scale=1.0) -> np.ndarray:
    return rig.stl_bytes(path.read_bytes(), scale)


def pad_centre(model, fits, aperture) -> np.ndarray:
    """Centre of the right pad's inner face in the tool frame at an aperture."""
    data = mujoco.MjData(model)
    for name, coef in fits.items():
        data.qpos[model.joint(name).qposadr[0]] = np.polynomial.polynomial.polyval(aperture, coef)
    mujoco.mj_kinematics(model, data)
    pads = [data.geom_xpos[model.geom(f'right_pad{k}').id] for k in (1, 2)]
    return np.mean(pads, axis=0)


def pad_fit(model, fits) -> np.ndarray:
    """How far ahead of the flange the pads' centre is, against the aperture
    (the bottle's diameter), as a cubic; the flange goes that far behind the
    bottle axis."""
    apertures = np.linspace(*rig.PAD_FIT, 23)
    pad_z = [pad_centre(model, fits, a)[2] for a in apertures]
    print(f'pads {pad_z[0] * 1000:.1f} .. {pad_z[-1] * 1000:.1f} mm ahead of the flange '
          f'over Ø{rig.PAD_FIT[0] * 1000:.0f} .. {rig.PAD_FIT[1] * 1000:.0f} mm')
    return np.polynomial.polynomial.polyfit(apertures, pad_z, 3)


def flange_x(fit, bottle_r=rig.BOTTLE_R) -> float:
    return -float(np.polynomial.polynomial.polyval(2 * bottle_r, fit))


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
    meshes = {f'grip/{m}': pack(read_stl(GRIP_MESHES / f'{m}.stl', 0.001)) for m in sorted(names)}
    meshes['grip/wrist3'] = pack(read_obj(UR_MESHES / 'wrist3.obj'))
    with zipfile.ZipFile(rig.IRIS_ZIP) as archive:
        for part in rig.IRIS_PARTS:
            meshes[f'iris/{part}'] = pack(rig.stl_bytes(rig.zip_member(archive, f'meshes/{part}.stl')))
    for parts in rig.PIPETTE_PARTS.values():
        for part in parts:
            meshes[f'pipette/{part}'] = pack(rig.pipette_mesh(part))

    rig.check_clearances()
    fit = pad_fit(model, fits)
    dims = rig.pipette_dims()
    print(f'pipette reaches {(rig.IRIS["bottle_h"] + rig.NECK["h"] - dims["tip_min"]) * 1000:.0f} mm below the neck')

    pos, quat = wrist3_pose()
    data = {
        'aperture': [closed, opened],
        'open_aperture': rig.OPEN_APERTURE,
        'fits': {k: v.tolist() for k, v in fits.items()},
        'bodies': bodies,
        'meshes': meshes,
        'wrist3': {'pos': pos.tolist(), 'quat': quat.tolist()},
        'stub': {'radius': STUB_RADIUS, 'length': STUB_LENGTH, 'top': STUB_TOP,
                 'ring': RING_HEIGHT},
        'materials': {**{k: v[:3] for k, v in MATERIALS.items()},
                      **{k: v[:3] for k, v in rig.RIG_MATERIALS.items()}},
        # Tool frame in the hand frame: +Z (fingers) along +X, jaws closing
        # along Y, flange pad_fit(Ø) behind the bottle axis.
        'tool': {'z': rig.GRIP_Z, 'quat': rig.TOOL_QUAT}, 'pad_fit': fit.tolist(),
        'tree': rig.tree(flange_x(fit)),
        'joint_map': {k: [off, coefs] for k, (off, coefs) in rig.JOINT_MAP.items()},
        'plan': plan.to_json(),
        'pipette': {'stroke': rig.PLUNGER_STROKE, 'ready': rig.TIP_READY, 'dive': rig.TIP_DIVE,
                    'tip_min': dims['tip_min'], 'stow': rig.STOW, 'carriage': rig.CARRIAGE,
                    'rail_top': rig.RAIL_TOP, 'mast_bottom': rig.MAST_BOTTOM},
        'iris': {**rig.IRIS, 'open': rig.IRIS_OPEN, 'contact': rig.ALPHA_CONTACT, 'z': rig.Z_IRIS},
        'bottle': rig.BOTTLE, 'neck': rig.NECK,
        'hinge': rig.HINGE, 'follow': rig.FOLLOW,
    }
    script = f'window.CELL_DATA={json.dumps(data, separators=(",", ":"))};'
    page = TEMPLATE.read_text()
    for marker, inline in (('THREE_JS', three_js()), ('CELL_DATA', script)):
        tag = re.search(rf'<script src="[^"]*"></script><!--{marker}-->', page)
        if tag is None:
            raise RuntimeError(f'no {marker} script tag in {TEMPLATE}')
        page = page.replace(tag.group(0), f'<script>{inline}</script>')
    OUT.write_text(page)
    print(f'wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)')


if __name__ == '__main__':
    main()
