#!/usr/bin/env python3
"""Play the uncap-and-pipette sequence in MuJoCo, and check that it worked.

Run from simulation/ after scripts/generate_iris_pipette_scene.py:
    python scripts/iris_pipette_play.py            # headless, prints the checks
    python scripts/iris_pipette_play.py --view     # in the viewer, in real time

The 19 steps of iris_pipette_plan.py (the page's sequence) as position targets
on the joints of models/iris_pipette_scene.xml. The bottle and the cap are
carried by welds the way the page re-parents them: the bottle to the hand
while the jaws are closed on it, the cap to the bottle until the housing
turns and to the clamp's carrier after. A weld is engaged at the relative
pose the bodies have at that moment, so nothing jumps.

It passes when the pads closed at the planned height on the bottle, the
bottle was carried, the cap rose off the neck while unscrewing and went with
the clamp when it swung up, the pipette's tip reached the dive inside the
bore, the pipette never touched the clamp, the cap came back onto the neck,
the bottle stood back on the floor where it was, and nothing of the rig
touched the floor.
"""
import argparse
import sys
import time
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import iris_pipette_plan as plan  # noqa: E402
import iris_pipette_rig as rig  # noqa: E402

SCENE = Path(__file__).resolve().parents[1] / 'models/iris_pipette_scene.xml'
GRIP_CTRL = 255.0 / plan.DRIVER_CLOSED    # the 2F-85 takes 0..255 for driver 0..0.8
# weld name -> (who carries what): the attachments() key and the value that turns it on
WELDS = {'hold_bottle': ('bottle', 'hand'), 'cap_on_bottle': ('cap', 'bottle'), 'cap_in_clamp': ('cap', 'clamp')}


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
    act = {name: model.actuator(name).id for name in
           ('lift', 'clamp_swing', 'cam', 'body_yaw', 'pipette_slide', 'pipette_swing', 'pipette_plunger_slide')}
    fingers = model.actuator('fingers_actuator').id
    welds = {name: model.equality(name).id for name in WELDS}
    bottle, cap = model.body('bottle').id, model.body('cap').id
    tip, seat = model.site('pipette_tip').id, model.site('cap_seat').id
    start = data.xpos[bottle].copy()
    floor = model.geom('floor').id
    pads = [g for g in range(model.ngeom) if model.geom_type[g] == mujoco.mjtGeom.mjGEOM_BOX
            and model.body(model.geom_bodyid[g]).name.endswith('_pad')]
    pipette_geoms = {g for g in range(model.ngeom) if model.geom(g).name.startswith(('pipette_col_', 'plunger_col_'))}
    clamp_geoms = {model.geom(n).id for n in ('clamp_envelope', 'motor_envelope')}
    bottle_tree = {b for b in range(model.nbody) if model.body_rootid[b] in (bottle, cap)}
    dive = rig.dive_z()

    viewer = mujoco.viewer.launch_passive(model, data) if view else None
    got = {}
    floor_hits, clamp_hits = set(), 0
    track = {}
    wall = time.time()
    while data.time < plan.DURATION + 1.0:
        state, _ = plan.state_at(data.time)
        targets = plan.targets(data.time)
        for name, a in act.items():
            data.ctrl[a] = targets[name]
        data.ctrl[fingers] = targets['right_driver_joint'] * GRIP_CTRL
        # the welds follow the page's parenting rule
        want = plan.attachments(state)
        for name, (what, who) in WELDS.items():
            on = want[what] == who
            if on and not data.eq_active[welds[name]]:
                engage(model, data, welds[name])
            elif not on:
                data.eq_active[welds[name]] = 0
        mujoco.mj_step(model, data)

        for c in data.contact[:data.ncon]:
            pair = {c.geom1, c.geom2}
            if floor in pair and bottle_tree.isdisjoint({model.geom_bodyid[c.geom1], model.geom_bodyid[c.geom2]}):
                floor_hits.add(model.body(model.geom_bodyid[(pair - {floor}).pop()]).name)
            if pair & pipette_geoms and pair & clamp_geoms:
                clamp_hits += 1
        for name in act:
            q = data.qpos[model.joint(name).qposadr[0]]
            track[name] = max(track.get(name, 0.0), abs(q - targets[name]))
        # snapshots for the checks
        for key, at in (('gripped', plan.GRIPPED_AT), ('lifted', plan.LIFTED_AT), ('unscrewed', plan.UNSCREWED_AT),
                        ('away', plan.CAP_AWAY_AT), ('dived', plan.DIVED_AT), ('recapped', plan.RECAPPED_AT)):
            if key not in got and data.time >= at:
                got[key] = {'pads': np.mean(data.geom_xpos[pads], axis=0), 'bottle': data.xpos[bottle].copy(),
                            'cap': data.xpos[cap].copy(), 'seat': data.site_xpos[seat].copy(),
                            'tip': data.site_xpos[tip].copy()}
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
    moved = np.linalg.norm(end[:2] - start[:2])
    landed = got['gripped']['pads'][2] - got['gripped']['bottle'][2]
    carried = got['lifted']['bottle'][2] - start[2]
    cap_rise = got['unscrewed']['cap'][2] - got['unscrewed']['bottle'][2] - rig.IRIS['bottle_h']
    cap_off = np.linalg.norm(got['away']['cap'][:2] - got['away']['bottle'][:2])
    cap_seated = np.linalg.norm(got['away']['cap'] - got['away']['seat'])
    tip_depth = got['dived']['tip'][2] - got['dived']['bottle'][2]
    tip_off = np.linalg.norm(got['dived']['tip'][:2] - got['dived']['bottle'][:2])
    recap = got['recapped']['cap'][2] - got['recapped']['bottle'][2] - rig.IRIS['bottle_h']
    worst = max(track.items(), key=lambda kv: kv[1])
    print('joint tracking, worst error: ' + ', '.join(f'{k} {v:.4f}' for k, v in track.items()))
    checks = {
        f'gripped with the pads {landed * 1000:.1f} mm up the bottle (planned {rig.GRIP_Z * 1000:.0f} +- 5)':
            abs(landed - rig.GRIP_Z) <= 0.005,
        f'carried {carried * 1000:.1f} mm at t={plan.LIFTED_AT:.1f} s (want >= {0.9 * rig.Z_LIFT * 1000:.0f})':
            carried >= 0.9 * rig.Z_LIFT,
        f'cap {cap_rise * 1000:.1f} mm off the shoulder once unscrewed (want >= {0.8 * rig.CAP_LIFT * 1000:.0f})':
            cap_rise >= 0.8 * rig.CAP_LIFT,
        f'cap carried {cap_off * 1000:.0f} mm off the bottle axis, {cap_seated * 1000:.1f} mm from the clamp seat (want >= 40, <= 5)':
            cap_off >= 0.04 and cap_seated <= 0.005,
        f'tip dived to {tip_depth * 1000:.1f} mm above the bottle floor (planned {dive * 1000:.0f} +- 2), {tip_off * 1000:.1f} mm off the axis (bore {rig.NECK["bore"] * 1000:.1f})':
            abs(tip_depth - dive) <= 0.002 and tip_off < rig.NECK['bore'],
        f'pipette-clamp contacts: {clamp_hits}': clamp_hits == 0,
        f'cap back {recap * 1000:.2f} mm from the shoulder (want <= 1)': abs(recap) <= 0.001,
        f'bottle set down {end[2] * 1000:.1f} mm up, {moved * 1000:.1f} mm from where it was picked, tilted {tilt:.1f} deg':
            end[2] < 0.005 and moved <= 0.01 and tilt <= 5,
        f'rig on the floor: {sorted(floor_hits) or "nothing"}': not floor_hits,
        f'worst joint tracking: {worst[0]} off by {worst[1]:.4f}': worst[1] < 0.05,
    }
    for text, ok in checks.items():
        print(('PASS ' if ok else 'FAIL ') + text)
    return all(checks.values())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--view', action='store_true', help='open the viewer and play in real time')
    sys.exit(0 if run(parser.parse_args().view) else 1)
