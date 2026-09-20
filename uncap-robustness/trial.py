#!/usr/bin/env python3
"""Run one uncap-and-pipette trial with contact physics, and measure it.

    python uncap-robustness/trial.py                                  # the nominal trial
    python uncap-robustness/trial.py --bottle 100 --fill 0.25 --pitch 10 --approach side --dx 3
    python uncap-robustness/trial.py --view                          # watch it
    python uncap-robustness/trial.py --frames out/frames/x       # PNGs at the key moments

The sequence is the shipped one (simulation/scripts/iris_pipette_plan.py, the
19 steps of the page), with four changes: the bottle, the jaws' closing and
the dive follow the bottle under test (plan.keys(bottle_r, dive)); the iris
is commanded past contact to its 76 degree stop, so the force-limited cam
drive decides the squeeze whatever the cap's size; the hand's first descent
and last retreat run along the approach direction; and nothing is welded:
scene.py says what holds what.

The trial's factors: bottle (ml), fill (fraction of the nominal volume),
pitch (deg; positive tilts the fingers down, about the jaw axis through the
pads' centre), approach ('above', 'side' = level from the arm's side,
'diagonal' = 45 degrees down from the arm's side), yaw (deg, the whole hand
about the bottle's nominal axis) and dx, dy (mm, where the bottle really is,
in the hand's axes: x along the fingers, y along the jaws).
"""
import argparse
import math
import os
import sys
import time
from pathlib import Path

if '--frames' in sys.argv:
    os.environ.setdefault('MUJOCO_GL', 'egl')

import mujoco  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gripper  # noqa: E402
import scene  # noqa: E402
from bottles import bottle, liquid_height  # noqa: E402
from scene import rig  # noqa: E402

import iris_pipette_plan as plan  # noqa: E402

NOMINAL = {'bottle': 60, 'fill': 0.5, 'pitch': 0.0, 'approach': 'above', 'yaw': 0.0, 'dx': 0.0, 'dy': 0.0}
APPROACH = {'above': (0.0, 0.0, 1.0), 'side': (-1.0, 0.0, 0.0), 'diagonal': (-math.sqrt(0.5), 0.0, math.sqrt(0.5))}
STANDOFF = 1.0            # the approach offset is lift_z (0 .. Z_LIFT = 100 mm) along the approach direction
DIVE_DEPTH = 0.010        # the tip is sent this far under the liquid's surface ...
FLOOR_CLEAR = 0.003       # ... but no closer than this to the inside floor
RELEASE_AT = 0.875        # the thread lets go here: the kit's helix fades out over its last half turn
                          # (generate_amber_bottles.helix_thread), 1.75 of 2 turns
SAMPLE = 5                # contact and slip bookkeeping every SAMPLE steps
SET_DOWN = 0.002          # how far past the pick height the hand presses when it sets down
RELEASE_FORCE = 25.0      # N a jaw while letting go: at the full grip the cradle's outer
                          # facets drag the bottle back up as they sweep off it
RIG_ACT = ('clamp_swing', 'cam', 'body_yaw', 'pipette_slide', 'pipette_swing', 'pipette_plunger_slide', 'clamp_lift')
# Seating the cap (v2): after the plan's two turns back, the housing keeps turning at the same
# rate until the torque on the cap says it has bottomed out: SEAT_TORQUE held for SEAT_HOLD, read
# by a reaction-torque sensor on the carrier (Trial.cap_torque). The blades slipping on the
# seated cap are the clutch. Calibrated on the nominal trial (README.md): free running 0.05 N m
# with the clamp still, blades slipping on the seated cap 0.12-0.16 N m.
PRELOAD = rig.IRIS['blade_max'] - rig.ALPHA_CONTACT     # 1.18 degrees
SEAT_TORQUE = 0.10        # N m on the cap
SEAT_HOLD = 0.05          # s (0.3 let a firm grip drive the cap 2 mm past its seat)
SEAT_RATE = math.pi * 2 / 3.0          # rad/s, half the plan's rate: it is feeling for the seat
SEAT_LIMIT, SEAT_TIMEOUT = -2 * math.pi, 3.0
# Pre-registered pass rules (README.md). Changing them means rerunning the report, not editing results.
RULES = {'pad_height_tol': 0.005, 'lift_min': 0.9 * rig.Z_LIFT, 'slip_max': 0.003, 'uncap_late_s': 0.3,
         'cap_off_axis_min': 0.04, 'cap_to_seat_max': 0.005, 'submerged_min': 0.003,
         'recap_max': 0.001, 'place_max': 0.010, 'place_tilt_max': 5.0}
STAGES = ('table', 'rig_clear', 'grip', 'lift', 'uncap', 'cap_away', 'reach_liquid', 'recap', 'place')
PAIRS = {  # contact class pairs worth counting, by the OR of the two contypes
    'pads_bottle': scene.PADS | scene.BOTTLE, 'blades_cap': scene.BLADES | scene.CAP,
    'pipette_bottle': scene.PIPETTE | scene.BOTTLE, 'pipette_clamp': scene.PIPETTE | scene.CLAMP,
    'rig_floor': scene.RIG | scene.FLOOR, 'pads_floor': scene.PADS | scene.FLOOR,
    'pipette_floor': scene.PIPETTE | scene.FLOOR, 'rig_bottle': scene.RIG | scene.BOTTLE,
    'clamp_rig': scene.CLAMP | scene.RIG, 'clamp_pads': scene.CLAMP | scene.PADS, 'pipette_rig': scene.PIPETTE | scene.RIG,
}


def zrot(a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def rel_pose(data, frame: int, body: int) -> tuple[np.ndarray, np.ndarray]:
    """A body's position and rotation matrix in another body's frame."""
    r = data.xmat[frame].reshape(3, 3)
    return r.T @ (data.xpos[body] - data.xpos[frame]), r.T @ data.xmat[body].reshape(3, 3)


def angle_between(a: np.ndarray, b: np.ndarray) -> float:
    return math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b))))))


def engage_weld(model, data, eq: int) -> None:
    """Switch a weld on at the bodies' present relative pose (iris_pipette_play.engage)."""
    b1, b2 = model.eq_obj1id[eq], model.eq_obj2id[eq]
    inv = np.zeros(4)
    mujoco.mju_negQuat(inv, data.xquat[b1])
    pos, quat = np.zeros(3), np.zeros(4)
    mujoco.mju_rotVecQuat(pos, data.xpos[b2] - data.xpos[b1], inv)
    mujoco.mju_mulQuat(quat, inv, data.xquat[b2])
    model.eq_data[eq, :3] = 0
    model.eq_data[eq, 3:6] = pos
    model.eq_data[eq, 6:10] = quat
    data.eq_active[eq] = 1


PRISTINE: dict[int, np.ndarray] = {}   # each shared model's equality data as compiled


class Trial:
    def __init__(self, p: dict):
        self.p = {**NOMINAL, **p}
        p = self.p
        self.d = d = bottle(int(p['bottle']))
        self.model = scene.build(int(p['bottle']))
        self.data = mujoco.MjData(self.model)
        self.z0 = scene.hand_z0(d)
        self.yaw, self.pitch = math.radians(p['yaw']), math.radians(p['pitch'])
        self.dir = zrot(self.yaw) @ np.array(APPROACH[p['approach']])
        # the dive, in the hand frame: under the surface, above the floor
        self.h_liq = liquid_height(d, p['fill'])
        inside_floor = -self.z0 + d['floor']
        self.dive = max(inside_floor + self.h_liq - DIVE_DEPTH, inside_floor + FLOOR_CLEAR)
        self.frames = plan.keys(bottle_r=d['r'], dive=self.dive)
        self.clamp_up = False          # the clamp's lift: set by the run when the thread lets go
        self.bottle_at = zrot(self.yaw) @ np.array([p['dx'], p['dy'], 0.0]) * 1e-3

    # --- the script ---------------------------------------------------------

    def carriage(self, t: float) -> tuple[dict, dict]:
        state, step = plan.state_at(t, self.frames)
        along = self.dir if step in (0, len(plan.STEPS) - 1, -1) else np.array([0.0, 0.0, 1.0])
        c = np.array([0.0, 0.0, self.z0]) + along * state['lift_z'] * STANDOFF
        # setting down, the hand presses SET_DOWN past the pick height, so the bottle rests
        # on the table before the jaws let go: the cradle's outer facets drag it up otherwise
        if step >= len(plan.STEPS) - 2 and state['lift_z'] < 0.002:
            c[2] -= SET_DOWN
        return {'cx': c[0], 'cy': c[1], 'cz': c[2], 'cyaw': self.yaw, 'cpitch': self.pitch}, state

    def rig_targets(self, state: dict) -> dict:
        s = dict(state)
        # the iris closes onto this cap and past it by a fixed preload: the v1 squeeze on the PP25 cap
        # (its 76 degree stop was 1.2 degrees past contact), never past the v2 stop
        span = rig.ALPHA_CONTACT - rig.IRIS_OPEN
        closed = min(scene.V2['blade_max'], math.acos(self.d['cap_r'] / rig.IRIS['r_pivot']) + PRELOAD)
        s['iris_angle'] = rig.IRIS_OPEN + (state['iris_angle'] - rig.IRIS_OPEN) / span * (closed - rig.IRIS_OPEN)
        j = rig.joint_values(s)
        out = {n: j[n] for n in RIG_ACT if n in j}
        # the clamp's own lift: up the moment the thread lets the cap go, so it comes
        # straight out of the neck instead of being dragged out along the hinge's arc;
        # back down when the clamp is over the neck again, to screw it on
        out['clamp_lift'] = scene.CLAMP_LIFT['stroke'] if self.clamp_up else 0.0
        if scene.HAND == 'v3':      # the curved jaws: told past the bottle's centre, the drive stalls on it
            out.update(dict.fromkeys(gripper.JOINTS,
                                     gripper.jaw_target(state['grip_aperture'], self.d['r'], rig.OPEN_APERTURE)))
        else:
            out['fingers'] = 255.0 * plan.driver_target(state['grip_aperture'], self.d['r']) / plan.DRIVER_CLOSED
        return out

    def reset(self) -> None:
        self.clamp_up = False
        m, d = self.model, self.data
        # the model is compiled once per process and shared by its trials: undo
        # what a trial writes into it (the thread's weld pose, on re-engaging)
        PRISTINE.setdefault(id(m), m.eq_data.copy())
        m.eq_data[:] = PRISTINE[id(m)]
        mujoco.mj_resetData(m, d)
        d.eq_active[:] = m.eq_active0
        self.fill_mass = scene.set_fill(m, d, self.d, self.h_liq)
        targets, state = self.carriage(0.0)
        for n, q in targets.items():
            d.qpos[m.joint(n).qposadr[0]] = q
        for n, q in rig.joint_values(state).items():
            if n != 'lift':                        # the carriage stands in for the lift
                d.qpos[m.joint(n).qposadr[0]] = q
        if scene.HAND == 'v3':                     # the jaws start where they are told to
            for n in gripper.JOINTS:
                d.qpos[m.joint(n).qposadr[0]] = gripper.jaw_target(state['grip_aperture'], self.d['r'],
                                                                   rig.OPEN_APERTURE)
        for body, z in (('bottle', 0.0), ('cap', self.d['cap_z'])):
            adr = m.joint(body).qposadr[0]
            d.qpos[adr:adr + 7] = [*self.bottle_at[:2], z, 1, 0, 0, 0]
        mujoco.mj_forward(m, d)

    # --- the run -----------------------------------------------------------

    def run(self, viewer=None, frames: Path | None = None, trace: list | None = None,
            frame_keys: tuple | None = None, frame_size: tuple = (540, 720),
            sampler=None, sample_every: int = 0) -> dict:
        m, d = self.model, self.data
        self.reset()
        ids = {n: m.body(n).id for n in ('bottle', 'cap', 'hand_frame', 'thread_follower')}
        act = {n: m.actuator(n).id for n in (*scene.CARRIAGE, *RIG_ACT)}
        if scene.HAND == 'v3':
            act.update({n: m.actuator(n).id for n in gripper.JOINTS})
        else:
            act['fingers'] = m.actuator('fingers_actuator').id
        eqs = [m.equality(n).id for n in ('thread_screw', 'thread_weld')]
        lift_q, spin_q = m.joint('cap_lift').qposadr[0], m.joint('cap_spin').qposadr[0]
        yaw_q = m.joint('body_yaw').qposadr[0]
        blade_slip = None
        k = self.d['pitch'] / (2 * math.pi)
        travel = self.d['turns'] * self.d['pitch']
        pads = [m.geom(n).id for n in scene.PAD_GEOMS]
        yaw_a = m.actuator('body_yaw').id
        seat_step0, seat_step1 = plan.step_end(14), plan.step_end(15)   # 'Screw the cap back'
        seated, seat_torque, seat_extra, hold_s, yaw_hold, above, holding = False, None, None, 0.0, None, 0.0, False
        tip, seat = m.site('pipette_tip').id, m.site('cap_seat').id
        ct = m.geom_contype
        counts = dict.fromkeys(PAIRS, 0)
        first_table_hit = None
        snaps, released, reengaged = {}, None, None
        grip_rel = None
        slip, tilt_in_hand, track = 0.0, 0.0, 0.0
        start = d.xpos[ids['bottle']].copy()
        when = {'gripped': plan.GRIPPED_AT, 'lifted': plan.LIFTED_AT, 'unscrewed': plan.UNSCREWED_AT,
                'away': plan.CAP_AWAY_AT, 'dived': plan.DIVED_AT, 'recapped': plan.RECAPPED_AT}
        carry_end = plan.step_end(17)
        recap_from = plan.step_end(14)       # 'Screw the cap back' starts
        back_down = plan.step_end(13) + 0.6  # 'Swing the clamp back down onto the neck' is under way
        release_step = plan.step_end(18)     # 'Open the gripper and lift the hand clear'
        jaw_q = ([m.joint(n).qposadr[0] for n in gripper.JOINTS] if scene.HAND == 'v3' else None)
        jaw_act = ([m.actuator(n).id for n in gripper.JOINTS] if scene.HAND == 'v3' else [])
        jaw_force = m.actuator_forcerange[jaw_act].copy() if jaw_act else None
        softened = False
        shots = {'grip': plan.GRIPPED_AT, 'uncap': plan.UNSCREWED_AT, 'away': plan.CAP_AWAY_AT,
                 'dive': plan.DIVED_AT, 'recap': plan.RECAPPED_AT, 'end': plan.DURATION}
        if frame_keys is not None:
            shots = {k: v for k, v in shots.items() if k in frame_keys}
        renderer = cam = None
        if frames is not None:
            frames.parent.mkdir(parents=True, exist_ok=True)
            renderer = mujoco.Renderer(m, *frame_size)
            cam = mujoco.MjvCamera()
            cam.distance, cam.azimuth, cam.elevation = 0.5, 140 + self.p['yaw'], -18
        wall, n, diverged = time.time(), 0, False
        end_t = plan.DURATION + 0.5
        tp, dt = 0.0, m.opt.timestep          # the plan's clock: it waits while the cap is seated
        while tp < end_t:
            if self.clamp_up and tp >= back_down:     # the clamp is over the neck again
                self.clamp_up = False
            targets, state = self.carriage(tp)
            targets.update(self.rig_targets(state))
            # the bottle sits deep in the cradle: the hand waits for the jaws to report open
            # before it lifts away, or it carries the bottle back up with it
            if jaw_q is not None and tp >= release_step and max(abs(d.qpos[j]) for j in jaw_q) > 0.004:
                targets['cz'] = self.z0 - SET_DOWN
            if jaw_act and not softened and tp >= plan.step_end(17):     # let go gently
                m.actuator_forcerange[jaw_act] = [[-RELEASE_FORCE, RELEASE_FORCE]] * len(jaw_act)
                softened = True
            if yaw_hold is not None:                                  # seated: hold the housing there
                targets['body_yaw'] = yaw_hold
            elif holding:                                             # turning on past the plan's zero
                targets['body_yaw'] = max(SEAT_LIMIT, -SEAT_RATE * hold_s)
            for name, a in act.items():
                d.ctrl[a] = targets[name]
            mujoco.mj_step(m, d)
            n += 1
            # seating, by the torque the housing's drive feels
            if holding:                                        # only while turning past the plan's zero
                force = abs(self.cap_torque(ids['cap']))
                above = above + dt if force >= SEAT_TORQUE else 0.0
                if above >= SEAT_HOLD:
                    seated, seat_torque = True, force
                    yaw_hold = float(d.qpos[yaw_q])
                    seat_extra = max(0.0, -yaw_hold / (2 * math.pi))
                    holding = False
            if holding:
                hold_s += dt
                if hold_s >= SEAT_TIMEOUT:
                    holding = False
                    yaw_hold = max(SEAT_LIMIT, -SEAT_RATE * hold_s)
            elif yaw_hold is None and reengaged is not None and tp >= seat_step1 and hold_s == 0.0:
                holding = True                                        # the plan's turns are done, the cap is not seated
            if not holding:
                tp += dt
            # the thread: lets go at the end of its travel, catches the cap again on the way back
            lift = d.qpos[lift_q]
            if released is None and lift >= RELEASE_AT * travel:
                d.eq_active[eqs] = 0
                released = tp
                self.clamp_up = True             # pull the cap straight out of the neck
                blade_slip = (d.qpos[yaw_q] - d.qpos[spin_q]) / (2 * math.pi)
            elif released is not None and reengaged is None and tp >= recap_from:
                pos, rot = rel_pose(d, ids['bottle'], ids['cap'])
                h = pos[2] - self.d['cap_z']
                if (math.hypot(pos[0], pos[1]) < 0.001 and angle_between(rot[:, 2], np.array([0, 0, 1])) < 3.0
                        and -0.0005 <= h <= travel + 0.0015):
                    d.qpos[lift_q], d.qpos[spin_q] = h, h / k
                    mujoco.mj_kinematics(m, d)
                    engage_weld(m, d, eqs[1])
                    d.eq_active[eqs[0]] = 1
                    reengaged = tp
            if sampler is not None and sample_every and n % sample_every == 0:
                sampler(tp)                    # for viewer3d.py: the poses, as they happen
            if trace is not None and n % 100 == 0:
                cpos, crot = rel_pose(d, ids['bottle'], ids['cap'])
                trace.append({'t': tp, 'sim': d.time, 'turns': state['housing_turns'], 'yaw_force': float(d.actuator_force[yaw_a]),
                              'cap_torque': self.cap_torque(ids['cap']),
                              'bottle_in_hand': rel_pose(d, ids['hand_frame'], ids['bottle'])[0].copy(), 'lift': float(d.qpos[lift_q]),
                              'spin': float(d.qpos[spin_q]), 'yaw': float(d.qpos[m.joint('body_yaw').qposadr[0]]),
                              'hinge': float(d.qpos[m.joint('clamp_swing').qposadr[0]]),
                              'cam': float(d.qpos[m.joint('cam').qposadr[0]]), 'cap': cpos.copy(),
                              'cap_tilt': angle_between(crot[:, 2], np.array([0, 0, 1])),
                              'seat': float(np.linalg.norm(d.xpos[ids['cap']] - d.site_xpos[seat])),
                              'eq': d.eq_active[eqs].copy(), 'nblade': int(np.count_nonzero(
                                  (ct[d.contact.geom1[:d.ncon]] | ct[d.contact.geom2[:d.ncon]]) == PAIRS['blades_cap']))})
            if n % SAMPLE == 0:
                if not np.isfinite(d.qpos).all() or d.warning[mujoco.mjtWarning.mjWARN_BADQACC].number:
                    diverged = True
                    break
                if d.ncon:
                    pair = ct[d.contact.geom1[:d.ncon]] | ct[d.contact.geom2[:d.ncon]]
                    for key, code in PAIRS.items():
                        c = int(np.count_nonzero(pair == code))
                        counts[key] += c
                        if c and key in ('rig_floor', 'pads_floor', 'pipette_floor') and first_table_hit is None:
                            first_table_hit = tp
                if plan.LIFTED_AT <= tp <= carry_end:     # from a settled grasp to the set-down
                    pos, rot = rel_pose(d, ids['hand_frame'], ids['bottle'])
                    if grip_rel is None:
                        grip_rel = (pos, rot[:, 2])
                    slip = max(slip, float(np.linalg.norm(pos - grip_rel[0])))
                    tilt_in_hand = max(tilt_in_hand, angle_between(rot[:, 2], grip_rel[1]))
                for name in scene.CARRIAGE:
                    q = d.qpos[m.joint(name).qposadr[0]]
                    track = max(track, abs(q - targets[name]) * (1000 if name in ('cx', 'cy', 'cz') else 180 / math.pi))
            for key, at in when.items():
                if key not in snaps and tp >= at:
                    snaps[key] = self.snapshot(ids, pads, tip, seat, lift_q)
            if renderer is not None:
                for key, at in list(shots.items()):
                    if tp >= at:
                        cam.lookat[:] = d.xpos[ids['bottle']] + [0, 0, 0.1]
                        renderer.update_scene(d, cam)
                        write_png(frames.parent / f'{frames.name}_{key}.png', renderer.render())
                        del shots[key]
            if viewer is not None:
                if not viewer.is_running():
                    break
                if n % 20 == 0:
                    viewer.sync()
                    time.sleep(max(0.0, d.time - (time.time() - wall)))
        if jaw_act:
            m.actuator_forcerange[jaw_act] = jaw_force       # the model is shared: hand it back as it was
        out = self.metrics(snaps, counts, released, reengaged, first_table_hit, slip, tilt_in_hand,
                           track, start, ids, lift_q, diverged, time.time() - wall)
        out['blade_slip_turns'] = blade_slip
        out.update({'seated': seated, 'seat_torque_Nm': seat_torque, 'seat_extra_turns': seat_extra,
                    'seat_hold_s': round(hold_s, 3)})
        return out

    def cap_torque(self, cap: int) -> float:
        """The torque the blades put on the cap about its own axis (N m): what a
        reaction-torque sensor on the carrier reads."""
        m, d = self.model, self.data
        axis, centre, total, f6 = d.xmat[cap].reshape(3, 3)[:, 2], d.xpos[cap], 0.0, np.zeros(6)
        ct = m.geom_contype
        for k in range(d.ncon):
            c = d.contact[k]
            code = ct[c.geom1] | ct[c.geom2]
            if code != PAIRS['blades_cap']:
                continue
            mujoco.mj_contactForce(m, d, k, f6)
            f = c.frame.reshape(3, 3).T @ f6[:3]            # on geom2, from geom1
            if ct[c.geom2] != scene.CAP:
                f = -f
            total += float(np.dot(np.cross(c.pos - centre, f), axis))
        return total

    def snapshot(self, ids, pads, tip, seat, lift_q) -> dict:
        d = self.data
        rb = d.xmat[ids['bottle']].reshape(3, 3)
        return {'bottle': d.xpos[ids['bottle']].copy(), 'bottle_rot': rb.copy(), 'cap': d.xpos[ids['cap']].copy(),
                'pads': d.geom_xpos[pads].mean(0), 'tip': d.site_xpos[tip].copy(), 'seat': d.site_xpos[seat].copy(),
                'lift': float(d.qpos[lift_q])}

    def metrics(self, snaps, counts, released, reengaged, table_hit, slip, tilt_in_hand, track,
                start, ids, lift_q, diverged, wall) -> dict:
        p, bd, R = self.p, self.d, RULES
        out = {**{f: p[f] for f in NOMINAL}, 'neck_mm': bd['neck_mm'], 'bottle_d_mm': 2e3 * bd['r'],
               'liquid_mm': 1e3 * self.h_liq, 'liquid_g': 1e3 * self.fill_mass, 'dive_target_mm': 1e3 * self.dive,
               'diverged': diverged, 'wall_s': round(wall, 2), 'sim_s': round(self.data.time, 2),
               **{f'contacts_{k}': v for k, v in counts.items()},
               'table_hit_s': table_hit, 'thread_released_s': released, 'thread_reengaged_s': reengaged,
               'slip_mm': 1e3 * slip, 'tilt_in_hand_deg': tilt_in_hand, 'track_worst': track}

        def in_bottle(s, key):   # a point in the bottle's frame at a snapshot
            return s['bottle_rot'].T @ (s[key] - s['bottle'])

        planned_pad = bd['cap_z'] - (rig.IRIS['bottle_h'] - scene.PADS_Z)
        ok = {'table': table_hit is None,
              'rig_clear': counts['clamp_rig'] + counts['clamp_pads'] + counts['pipette_rig'] == 0}
        if 'gripped' in snaps:
            s = snaps['gripped']
            out['pad_height_mm'] = 1e3 * in_bottle(s, 'pads')[2]
            out['pad_planned_mm'] = 1e3 * planned_pad
            ok['grip'] = counts['pads_bottle'] > 0 and abs(in_bottle(s, 'pads')[2] - planned_pad) <= R['pad_height_tol']
        if 'lifted' in snaps:
            out['lift_mm'] = 1e3 * (snaps['lifted']['bottle'][2] - start[2])
            ok['lift'] = out['lift_mm'] >= 1e3 * R['lift_min'] and slip <= R['slip_max']
        if 'unscrewed' in snaps:
            s = snaps['unscrewed']
            out['cap_rise_mm'] = 1e3 * (in_bottle(s, 'cap')[2] - bd['cap_z'])
            out['blade_contacts'] = counts['blades_cap']
            # the cap ran the thread to its end (RELEASE_AT of the travel) by the end of the step, +0.3 s
            ok['uncap'] = released is not None and released <= plan.UNSCREWED_AT + R['uncap_late_s']
        if 'away' in snaps:
            s = snaps['away']
            c = in_bottle(s, 'cap')
            out['cap_off_axis_mm'] = 1e3 * math.hypot(c[0], c[1])
            out['cap_to_seat_mm'] = 1e3 * float(np.linalg.norm(s['cap'] - s['seat']))
            ok['cap_away'] = out['cap_off_axis_mm'] >= 1e3 * R['cap_off_axis_min'] and out['cap_to_seat_mm'] <= 1e3 * R['cap_to_seat_max']
        if 'dived' in snaps:
            s = snaps['dived']
            tip = in_bottle(s, 'tip')
            axis = s['bottle_rot'][:, 2]
            surface = s['bottle'] + axis * (bd['floor'] + self.h_liq)     # on the axis: volume kept when tilted
            tilt = angle_between(axis, np.array([0, 0, 1]))
            ri = bd['r'] - bd['wall']
            out['tip_off_axis_mm'] = 1e3 * math.hypot(tip[0], tip[1])
            out['tip_height_mm'] = 1e3 * tip[2]
            out['tip_submerged_mm'] = 1e3 * float(surface[2] - s['tip'][2])
            out['bottle_tilt_dive_deg'] = tilt
            out['liquid_to_shoulder_mm'] = 1e3 * (bd['shoulder'] - bd['floor'] - self.h_liq - ri * math.tan(math.radians(tilt)))
            ok['reach_liquid'] = (out['tip_off_axis_mm'] < 1e3 * bd['bore'] and tip[2] < bd['h']
                                  and out['tip_submerged_mm'] >= 1e3 * R['submerged_min']
                                  and counts['pipette_bottle'] == 0 and counts['pipette_clamp'] == 0)
        if 'recapped' in snaps:
            out['recap_lift_mm'] = 1e3 * float(self.data.qpos[lift_q]) if reengaged else None
            fin_pos, fin_rot = rel_pose(self.data, ids['bottle'], ids['cap'])
            out['cap_end_mm'] = 1e3 * float(np.linalg.norm(fin_pos - [0, 0, bd['cap_z']]))
            ok['recap'] = (reengaged is not None and self.data.eq_active[self.model.equality('thread_weld').id] == 1
                           and abs(self.data.qpos[lift_q]) <= R['recap_max'] and out['cap_end_mm'] <= 2.0)
        end = self.data.xpos[ids['bottle']]
        up = self.data.xmat[ids['bottle']].reshape(3, 3)[:, 2]
        out['placed_error_mm'] = 1e3 * float(np.linalg.norm(end[:2] - start[:2]))
        out['placed_tilt_deg'] = angle_between(up, np.array([0, 0, 1]))
        out['placed_z_mm'] = 1e3 * float(end[2] - start[2])
        ok['place'] = (not diverged and out['placed_error_mm'] <= 1e3 * R['place_max']
                       and out['placed_tilt_deg'] <= R['place_tilt_max'] and abs(out['placed_z_mm']) <= 5)
        for stage in STAGES:
            out[f'ok_{stage}'] = bool(ok.get(stage, False)) and not diverged
        out['first_failure'] = 'diverged' if diverged else next((s for s in STAGES if not out[f'ok_{s}']), '')
        out['success'] = out['first_failure'] == ''
        return out


def write_png(path: Path, img: np.ndarray) -> None:
    import struct
    import zlib
    h, w, _ = img.shape
    raw = b''.join(b'\0' + img[y].tobytes() for y in range(h))
    def chunk(t, b):
        return struct.pack('>I', len(b)) + t + b + struct.pack('>I', zlib.crc32(t + b))
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


def run_trial(p: dict, frames: Path | None = None, **kw) -> dict:
    return Trial(p).run(frames=frames, **kw)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--bottle', type=int, default=NOMINAL['bottle'])
    ap.add_argument('--fill', type=float, default=NOMINAL['fill'])
    ap.add_argument('--pitch', type=float, default=NOMINAL['pitch'])
    ap.add_argument('--approach', choices=tuple(APPROACH), default=NOMINAL['approach'])
    ap.add_argument('--yaw', type=float, default=NOMINAL['yaw'])
    ap.add_argument('--dx', type=float, default=NOMINAL['dx'])
    ap.add_argument('--dy', type=float, default=NOMINAL['dy'])
    ap.add_argument('--view', action='store_true')
    ap.add_argument('--frames', type=Path)
    a = ap.parse_args()
    p = {k: getattr(a, k) for k in NOMINAL}
    trial = Trial(p)
    if a.view:
        import mujoco.viewer
        with mujoco.viewer.launch_passive(trial.model, trial.data) as v:
            out = trial.run(viewer=v)
    else:
        out = trial.run(frames=a.frames)
    for key, value in out.items():
        print(f'  {key:24s} {value:.3f}' if isinstance(value, float) else f'  {key:24s} {value}')
    sys.exit(0 if out['success'] else 1)


if __name__ == '__main__':
    main()
