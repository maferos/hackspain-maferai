#!/usr/bin/env python3
"""Play the vertical hand's 21-step uncap-and-pipette sequence in MuJoCo, and check that it worked.

Run from simulation/ after scripts/generate_vertical_hand_blend.py:
    python scripts/vertical_hand_play.py            # headless, prints the checks
    python scripts/vertical_hand_play.py --view     # in the viewer, in real time

The steps of vertical_hand_rig.STEPS (the page's sequence) as position
targets on the eight actuated joints of assets/vertical_hand/vertical_hand_scene.xml.
The bottle and the cap are carried by welds the way the page re-parents them:
the bottle to the hand while the jaws are closed on it, the cap to the bottle
until the housing turns and to the clamp's housing after. A weld is engaged at
the relative pose the bodies have at that moment, so nothing jumps.

It passes when the pads closed on the bottle at the tool axis, the bottle was
carried, the cap rose off the neck while unscrewing and went out with the
clamp, the pipette's tip reached the dive on the bottle's axis, the cap came
back onto the neck, the bottle stood back on the floor where it was, the
joints tracked their targets and nothing of the hand touched the floor.
"""
import argparse
import sys
import time
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vertical_hand_rig as rig  # noqa: E402

SCENE = Path(__file__).resolve().parents[1] / 'assets/vertical_hand/vertical_hand_scene.xml'
B = rig.BOTTLE
# weld -> which attachment turns it on: (rule index in attachments(), wanted value)
WELDS = {'hold_bottle': (0, True), 'cap_on_bottle': (1, False), 'cap_in_clamp': (1, True)}
# when to take the snapshots the checks read (s): just before the step ends
AT = {'gripped': 2, 'lifted': 3, 'unscrewed': 7, 'away': 9, 'dived': 11, 'recapped': 16, 'down': 20}


def engage(model, data, eq: int) -> None:
    """Switch a weld on at the bodies' present relative pose."""
    b1, b2 = model.eq_obj1id[eq], model.eq_obj2id[eq]
    inv = np.zeros(4)
    mujoco.mju_negQuat(inv, data.xquat[b1])
    rel_pos, rel_quat = np.zeros(3), np.zeros(4)
    mujoco.mju_rotVecQuat(rel_pos, data.xpos[b2] - data.xpos[b1], inv)
    mujoco.mju_mulQuat(rel_quat, inv, data.xquat[b2])
    model.eq_data[eq, :3] = 0
    model.eq_data[eq, 3:6] = rel_pos
    model.eq_data[eq, 6:10] = rel_quat
    data.eq_active[eq] = 1


def run(view: bool) -> bool:
    model = mujoco.MjModel.from_xml_path(str(SCENE))
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, model.key('home').id)
    mujoco.mj_forward(model, data)
    act = {model.actuator(a).name: a for a in range(model.nu)}
    slide = {name: model.jnt_type[model.joint(name).id] == mujoco.mjtJoint.mjJNT_SLIDE for name in act}
    welds = {name: model.equality(name).id for name in WELDS}
    bottle, cap = model.body('bottle').id, model.body('cap').id
    tip, seat = model.site('tip').id, model.site('cap_seat').id
    jaw_l, jaw_r = model.site('jaw_l_vertex').id, model.site('jaw_r_vertex').id
    start = data.xpos[bottle].copy()
    floor = model.geom('floor').id
    loose = {bottle, cap}
    snapshots_at = {k: rig.step_end(n) - 0.05 for k, n in AT.items()}

    viewer = None
    if view:
        viewer = mujoco.viewer.launch_passive(model, data)
    got, track, floor_hits, pad_touch = {}, {}, set(), 0
    wall = time.time()
    while data.time < rig.DURATION + rig.TAIL:
        state, _ = rig.state_at(data.time)
        targets = rig.joints(state)
        for name, a in act.items():
            data.ctrl[a] = targets[name]
        want = rig.attachments(state, B)
        for name, (idx, on) in WELDS.items():
            if want[idx] == on and not data.eq_active[welds[name]]:
                engage(model, data, welds[name])
            elif want[idx] != on:
                data.eq_active[welds[name]] = 0
        mujoco.mj_step(model, data)

        for c in data.contact[:data.ncon]:
            bodies = {model.geom_bodyid[c.geom1], model.geom_bodyid[c.geom2]}
            if floor in (c.geom1, c.geom2) and not bodies & loose:
                floor_hits.add(model.body((bodies - {model.geom_bodyid[floor]}).pop()).name)
            names = {model.geom(c.geom1).name, model.geom(c.geom2).name}
            if 'bottle_col' in names and any(n.startswith('jaw_') for n in names):
                pad_touch += 1
        for name, a in act.items():
            q = data.qpos[model.joint(name).qposadr[0]]
            track[name] = max(track.get(name, 0.0), abs(q - targets[name]))
        for key, at in snapshots_at.items():
            if key not in got and data.time >= at:
                got[key] = dict(bottle=data.xpos[bottle].copy(), cap=data.xpos[cap].copy(), seat=data.site_xpos[seat].copy(),
                                tip=data.site_xpos[tip].copy(), jaws=(data.site_xpos[jaw_l] + data.site_xpos[jaw_r]) / 2)
        if viewer is not None:
            if not viewer.is_running():
                return False
            viewer.sync()
            ahead = data.time - (time.time() - wall)
            if ahead > 0:
                time.sleep(ahead)

    end = data.xpos[bottle]
    up = data.xmat[bottle].reshape(3, 3)[:, 2]
    tilt = np.degrees(np.arccos(np.clip(up[2], -1, 1)))
    g = got
    checks = [
        ('pads closed at the tool axis, 57.1 mm up the bottle', g['gripped']['jaws'][2] - g['gripped']['bottle'][2], (rig.GRIP_Z * rig.MM - 0.003, rig.GRIP_Z * rig.MM + 0.003)),
        ('bottle carried 100 mm', g['lifted']['bottle'][2] - start[2], (0.095, 0.105)),
        ('cap up the thread 5.5 mm while unscrewing', g['unscrewed']['cap'][2] - g['unscrewed']['bottle'][2] - B['cap_z'] * rig.MM, (0.0044, 0.0066)),
        ('cap back with the clamp, 90 mm off the axis', np.linalg.norm(g['away']['cap'][:2] - g['away']['bottle'][:2]), (0.085, 0.095)),
        ('cap on its seat in the clamp', np.linalg.norm(g['away']['cap'] - g['away']['seat']), (0.0, 0.001)),
        ('tip at the dive, 20 mm over the floor', g['dived']['tip'][2] - g['dived']['bottle'][2], (0.018, 0.022)),
        ('tip on the axis', np.linalg.norm(g['dived']['tip'][:2] - g['dived']['bottle'][:2]), (0.0, 0.001)),
        ('cap back on the neck', g['recapped']['cap'][2] - g['recapped']['bottle'][2] - B['cap_z'] * rig.MM, (-0.001, 0.001)),
        ('bottle set down where it was (mm)', np.linalg.norm(end[:2] - start[:2]) * 1000, (0.0, 1.0)),
        ('bottle upright at the end (deg)', tilt, (0.0, 0.5)),
        ('bottle on the floor at the end', end[2], (-0.001, 0.001)),
        ('worst slide tracking (mm)', max(v for k, v in track.items() if slide[k]) * 1000, (0.0, 3.0)),
        ('worst hinge tracking (mrad)', max(v for k, v in track.items() if not slide[k]) * 1000, (0.0, 10.0)),
    ]
    ok = True
    for name, value, (lo, hi) in checks:
        good = lo <= value <= hi
        ok &= good
        print(f'  {"ok " if good else "BAD"} {name}: {value:.4g} (want {lo:.4g}..{hi:.4g})')
    print(f'  {"ok " if not floor_hits else "BAD"} hand off the floor' + (f': {sorted(floor_hits)}' if floor_hits else ''))
    print(f'  pad-bottle contacts seen: {pad_touch}; worst tracking per joint: ' +
          ', '.join(f'{k} {v * 1000:.2f}' for k, v in sorted(track.items())))
    ok &= not floor_hits
    print('PASS' if ok else 'FAIL')
    return ok


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--view', action='store_true', help='play in the viewer in real time')
    sys.exit(0 if run(parser.parse_args().view) else 1)
