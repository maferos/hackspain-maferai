#!/usr/bin/env python3
"""Play the uncap-and-pipette sequence in Isaac Lab, and check that it worked.

The Isaac twin of iris_pipette_play.py: the same plan (iris_pipette_plan.py),
the same checks, on the URDFs generate_iris_pipette_scene.py writes. Run from
simulation/ with Isaac Lab's Python (2.x, Isaac Sim 4.5; see runpod-isaac.md):

    ./isaaclab.sh -p scripts/iris_pipette_isaac.py --headless
    ./isaaclab.sh -p scripts/iris_pipette_isaac.py          # with the GUI

The scene is built here: a ground plane, a dome light, the lift carriage with
the hand and its tooling (``models/iris_pipette_rig.urdf``, fixed base, gravity
off like a servoed arm), the reference bottle and its cap
(``assets/ur10e_iris_pipette/reference_{bottle,cap}.urdf``, free bodies).

PhysX has no weld that can be switched on and off, so the page's parenting
rule (iris_pipette_plan.attachments) is applied by writing the root pose:
while the jaws are closed on it the bottle is set on the hand frame every
step, and the cap on the neck or on the clamp's carrier. The blades still
close on the cap and the pads on the bottle, for the look of it; nothing
depends on the contact. ``assets/ur10e_iris_pipette/FULL_PHYSICS_ISAAC.md``
says how to replace the pose writes with contact and a thread.

NOT YET RUN: there is no Isaac on the machine this was written on. What was
verified is the rig URDF itself, loaded in MuJoCo (which honours ``mimic``):
its bodies sit where iris_pipette_rig.fk puts them, to a micrometre, over the
sequence. Two things only a run can settle: whether the URDF importer turns
``<mimic>`` into PhysX mimic joints (the first check below catches it if not),
and the drive gains, which are the MuJoCo ones.
"""
import argparse
import sys
from pathlib import Path

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()
app = AppLauncher(args).app

import torch  # noqa: E402  (Isaac modules load only after the app starts)

import isaaclab.sim as sim_utils  # noqa: E402
from isaaclab.actuators import ImplicitActuatorCfg  # noqa: E402
from isaaclab.assets import (Articulation, ArticulationCfg, RigidObject,  # noqa: E402
                             RigidObjectCfg)
from isaaclab.utils.math import quat_apply  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import iris_pipette_plan as plan  # noqa: E402
import iris_pipette_rig as rig  # noqa: E402

SIM = Path(__file__).resolve().parents[1]
RIG_URDF = SIM / 'models/iris_pipette_rig.urdf'
BOTTLE_URDF = SIM / 'assets/ur10e_iris_pipette/reference_bottle.urdf'
CAP_URDF = SIM / 'assets/ur10e_iris_pipette/reference_cap.urdf'
# The joints driven, in the order targets are stacked: the plan's, then the sun.
JOINTS = [*rig.ACTUATED, 'sun_input']
PAD_CENTRE = (0.0, -0.0026, 0.01875)   # the two pad boxes' middle, in the pad link
TIP = (-rig.PIVOT[0], -rig.PIVOT[1], 0.0)   # the pipette tip in the swing frame
SEAT = (0.0, 0.0, rig.IRIS['cap_z'])        # where the cap sits in the carrier
GAINS = {   # stiffness, damping, effort: the MuJoCo position actuators'
    'lift': (10000.0, 800.0, 300.0), 'right_driver_joint': (10.0, 0.5, 5.0),
    'clamp_swing': (300.0, 5.0, 20.0), 'cam': (100.0, 2.0, 3.0), 'body_yaw': (150.0, 1.0, 8.0),
    'pipette_slide': (3000.0, 100.0, 100.0), 'pipette_swing': (100.0, 2.0, 5.0),
    'pipette_plunger_slide': (600.0, 5.0, 20.0), 'sun_input': (50.0, 1.0, 3.0),
}


def no_drive() -> sim_utils.UrdfConverterCfg.JointDriveCfg:
    """Import every joint undriven; the actuators below drive the real ones."""
    return sim_utils.UrdfConverterCfg.JointDriveCfg(
        gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(stiffness=0.0, damping=0.0))


RIG = ArticulationCfg(
    prim_path='/World/Rig',
    spawn=sim_utils.UrdfFileCfg(
        asset_path=str(RIG_URDF), fix_base=True, merge_fixed_joints=False,
        joint_drive=no_drive(),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(disable_gravity=True),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            solver_position_iteration_count=16, solver_velocity_iteration_count=4)),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={**{k: v for k, v in rig.joint_values(plan.START).items()},
                   'wrist_3_joint': 0.0, 'right_driver_joint': 0.0}),
    actuators={name: ImplicitActuatorCfg(joint_names_expr=[name], stiffness=kp, damping=kv, effort_limit=f)
               for name, (kp, kv, f) in GAINS.items()},
)


def free_body(name: str, urdf: Path, pos) -> RigidObjectCfg:
    """A free rigid body. The importer may still mark its one link as an
    articulation root, which RigidObject refuses, so that is switched off."""
    return RigidObjectCfg(
        prim_path=f'/World/{name}',
        spawn=sim_utils.UrdfFileCfg(
            asset_path=str(urdf), fix_base=False, joint_drive=no_drive(),
            articulation_props=sim_utils.ArticulationRootPropertiesCfg(articulation_enabled=False)),
        init_state=RigidObjectCfg.InitialStateCfg(pos=pos),
    )


def place(obj: RigidObject, pos: torch.Tensor, quat: torch.Tensor) -> None:
    """Pin a free body to a pose this step: the stand-in for a weld."""
    obj.write_root_pose_to_sim(torch.cat([pos, quat]).unsqueeze(0))
    obj.write_root_velocity_to_sim(torch.zeros(1, 6, device=pos.device))


def main() -> None:
    sim = sim_utils.SimulationContext(sim_utils.SimulationCfg(dt=1 / 240, device=args.device))
    sim.set_camera_view([0.55, -0.55, 0.35], [0.0, 0.05, 0.15])
    sim_utils.GroundPlaneCfg().func('/World/ground', sim_utils.GroundPlaneCfg())
    light = sim_utils.DomeLightCfg(intensity=2000.0)
    light.func('/World/light', light)
    rig_art = Articulation(RIG)
    bottle = RigidObject(free_body('Bottle', BOTTLE_URDF, (0.0, 0.0, 0.0)))
    cap = RigidObject(free_body('Cap', CAP_URDF, (0.0, 0.0, rig.IRIS['bottle_h'])))
    sim.reset()

    ids, _ = rig_art.find_joints(JOINTS, preserve_order=True)
    cam, blade = rig_art.find_joints(['cam', 'blade_3'], preserve_order=True)[0]
    pads, _ = rig_art.find_bodies(['left_pad', 'right_pad'], preserve_order=True)
    (hand_frame,), _ = rig_art.find_bodies(['hand_frame'])
    (carrier,), _ = rig_art.find_bodies(['carrier'])
    (swing,), _ = rig_art.find_bodies(['pipette_swing'])
    dev = sim.device
    pad_centre = torch.tensor(PAD_CENTRE, device=dev).repeat(len(pads), 1)
    tip_local, seat_local = torch.tensor([TIP], device=dev), torch.tensor([SEAT], device=dev)
    neck = torch.tensor([0.0, 0.0, rig.IRIS['bottle_h']], device=dev)
    dt = sim.get_physics_dt()
    start = bottle.data.root_pos_w[0].clone()
    got, mimic_gap, t = {}, 0.0, 0.0
    while app.is_running() and t < plan.DURATION + 1.0:
        state, _ = plan.state_at(t)
        targets = plan.targets(t)
        targets['sun_input'] = targets['body_yaw'] - 3.0 * targets['cam']
        target = torch.tensor([targets[j] for j in JOINTS], dtype=torch.float32, device=dev)
        rig_art.set_joint_position_target(target.unsqueeze(0), joint_ids=ids)
        rig_art.write_data_to_sim()
        # the page's parenting rule, as pose writes
        where = plan.attachments(state)
        if where['bottle'] == 'hand':
            place(bottle, rig_art.data.body_pos_w[0, hand_frame], rig_art.data.body_quat_w[0, hand_frame])
        if where['cap'] == 'clamp':
            pos = rig_art.data.body_pos_w[0, carrier] + quat_apply(rig_art.data.body_quat_w[0, carrier:carrier + 1], seat_local)[0]
            place(cap, pos, rig_art.data.body_quat_w[0, carrier])
        else:
            place(cap, bottle.data.root_pos_w[0] + quat_apply(bottle.data.root_quat_w[0:1], neck.unsqueeze(0))[0],
                  bottle.data.root_quat_w[0])
        sim.step()
        t += dt
        for obj in (rig_art, bottle, cap):
            obj.update(dt)
        q = rig_art.data.joint_pos[0]
        mimic_gap = max(mimic_gap, float(abs(q[blade] + q[cam])))
        for key, at in (('gripped', plan.GRIPPED_AT), ('lifted', plan.LIFTED_AT), ('unscrewed', plan.UNSCREWED_AT),
                        ('away', plan.CAP_AWAY_AT), ('dived', plan.DIVED_AT), ('recapped', plan.RECAPPED_AT)):
            if key not in got and t >= at:
                centres = rig_art.data.body_pos_w[0, pads] + quat_apply(rig_art.data.body_quat_w[0, pads], pad_centre)
                got[key] = {
                    'pads': centres.mean(0), 'bottle': bottle.data.root_pos_w[0].clone(), 'cap': cap.data.root_pos_w[0].clone(),
                    'seat': rig_art.data.body_pos_w[0, carrier] + quat_apply(rig_art.data.body_quat_w[0, carrier:carrier + 1], seat_local)[0],
                    'tip': rig_art.data.body_pos_w[0, swing] + quat_apply(rig_art.data.body_quat_w[0, swing:swing + 1], tip_local)[0]}

    end = bottle.data.root_pos_w[0]
    up = quat_apply(bottle.data.root_quat_w[0:1], torch.tensor([[0.0, 0.0, 1.0]], device=dev))[0]
    tilt = float(torch.rad2deg(torch.arccos(up[2].clamp(-1, 1))))
    moved = float(torch.linalg.norm(end[:2] - start[:2]))
    landed = float(got['gripped']['pads'][2] - got['gripped']['bottle'][2])
    carried = float(got['lifted']['bottle'][2] - start[2])
    cap_rise = float(got['unscrewed']['cap'][2] - got['unscrewed']['bottle'][2]) - rig.IRIS['bottle_h']
    cap_off = float(torch.linalg.norm(got['away']['cap'][:2] - got['away']['bottle'][:2]))
    cap_seated = float(torch.linalg.norm(got['away']['cap'] - got['away']['seat']))
    dive = rig.dive_z()
    tip_depth = float(got['dived']['tip'][2] - got['dived']['bottle'][2])
    tip_off = float(torch.linalg.norm(got['dived']['tip'][:2] - got['dived']['bottle'][:2]))
    recap = float(got['recapped']['cap'][2] - got['recapped']['bottle'][2]) - rig.IRIS['bottle_h']
    checks = {
        # If the importer dropped the mimic tags, the blades are loose and
        # nothing after this means anything.
        f'blades follow the cam ring (mimic): {mimic_gap * 1000:.1f} mrad off at worst (want <= 20)': mimic_gap <= 0.02,
        f'gripped with the pads {landed * 1000:.1f} mm up the bottle (planned {rig.GRIP_Z * 1000:.0f} +- 5)':
            abs(landed - rig.GRIP_Z) <= 0.005,
        f'carried {carried * 1000:.1f} mm at t={plan.LIFTED_AT:.1f} s (want >= {0.9 * rig.Z_LIFT * 1000:.0f})':
            carried >= 0.9 * rig.Z_LIFT,
        f'cap {cap_rise * 1000:.1f} mm off its seat once unscrewed (want >= {0.8 * rig.CAP_LIFT * 1000:.0f})':
            cap_rise >= 0.8 * rig.CAP_LIFT,
        f'cap carried {cap_off * 1000:.0f} mm off the bottle axis, {cap_seated * 1000:.1f} mm from the clamp seat (want >= 40, <= 5)':
            cap_off >= 0.04 and cap_seated <= 0.005,
        f'tip dived to {tip_depth * 1000:.1f} mm above the bottle floor (planned {dive * 1000:.0f} +- 2), {tip_off * 1000:.1f} mm off the axis':
            abs(tip_depth - dive) <= 0.002 and tip_off < rig.NECK['bore'],
        f'cap back {recap * 1000:.2f} mm from its seat (want <= 1)': abs(recap) <= 0.001,
        f'bottle set down {float(end[2]) * 1000:.1f} mm up, {moved * 1000:.1f} mm from where it was picked, tilted {tilt:.1f} deg':
            float(end[2]) < 0.005 and moved <= 0.01 and tilt <= 5,
    }
    for label, ok in checks.items():
        print(f'  {"ok  " if ok else "FAIL"} {label}')
    app.close()
    sys.exit(0 if all(checks.values()) else 1)


if __name__ == '__main__':
    main()
