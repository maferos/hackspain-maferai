#!/usr/bin/env python3
"""Play the UR10e hand's pick-and-place in Isaac Lab, and check that it worked.

The Isaac twin of hand_pick.py: the same plan (hand_pick_plan.py), the same
checks, on the URDFs generate_hand_scene.py writes. Run from simulation/ with
Isaac Lab's Python (2.x, Isaac Sim 4.5; see runpod-isaac.md):

    ./isaaclab.sh -p scripts/hand_pick_isaac.py --headless
    ./isaaclab.sh -p scripts/hand_pick_isaac.py          # with the GUI

The scene is built here: a ground plane, a dome light, the carriage + hand
(``models/hand_pick_rig.urdf``, fixed base, gravity off like a servoed arm) and
the amber bottle (``assets/amber_bottles/amber_060ml.urdf``, a free body).

NOT YET RUN: there is no Isaac on the machine this was written on. What was
verified is the rig URDF itself, loaded in MuJoCo (which honours ``mimic``):
its pads sit within 0.3 mm of the MJCF hand's over the whole stroke. Two things
only a run can settle: whether the URDF importer turns ``<mimic>`` into PhysX
mimic joints (the first check below catches it if not), and the drive gains
below, which are first guesses. PhysX mimic joints are soft constraints, so
watch how firmly the pads hold compared with MuJoCo.
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
import hand_pick_plan as plan  # noqa: E402

SIM = Path(__file__).resolve().parents[1]
RIG_URDF = SIM / 'models/hand_pick_rig.urdf'
BOTTLE_URDF = SIM / 'assets/amber_bottles/amber_060ml.urdf'
JOINTS = ['reach', 'lift', 'wrist_3_joint', 'right_driver_joint']
FINGERS = ['right_driver_joint', 'right_spring_link_joint', 'right_follower_joint',
           'left_driver_joint', 'left_spring_link_joint', 'left_follower_joint']
PAD_CENTRE = (0.0, -0.0026, 0.01875)   # the two pad boxes' middle, in the pad link


def no_drive() -> sim_utils.UrdfConverterCfg.JointDriveCfg:
    """Import every joint undriven; the actuators below drive the four real ones."""
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
        joint_pos={'reach': plan.HOME_REACH, 'lift': plan.HOVER, 'wrist_3_joint': 0.0,
                   **{name: 0.0 for name in FINGERS}}),
    actuators={
        'carriage': ImplicitActuatorCfg(joint_names_expr=['reach', 'lift'],
                                        stiffness=10000.0, damping=800.0, effort_limit=200.0),
        'wrist': ImplicitActuatorCfg(joint_names_expr=['wrist_3_joint'],
                                     stiffness=500.0, damping=50.0, effort_limit=56.0),
        # The other finger joints follow this one through their mimic tags.
        'gripper': ImplicitActuatorCfg(joint_names_expr=['right_driver_joint'],
                                       stiffness=10.0, damping=0.5, effort_limit=5.0),
    },
)

# A free rigid body. The importer may still mark its one link as an
# articulation root, which RigidObject refuses, so that is switched off.
BOTTLE = RigidObjectCfg(
    prim_path='/World/Bottle',
    spawn=sim_utils.UrdfFileCfg(
        asset_path=str(BOTTLE_URDF), fix_base=False, joint_drive=no_drive(),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(articulation_enabled=False)),
    init_state=RigidObjectCfg.InitialStateCfg(pos=(*plan.BOTTLE_XY, 0.0)),
)


def main() -> None:
    sim = sim_utils.SimulationContext(sim_utils.SimulationCfg(dt=1 / 240, device=args.device))
    sim.set_camera_view([0.05, -0.65, 0.28], [-0.15, 0.0, 0.08])
    sim_utils.GroundPlaneCfg().func('/World/ground', sim_utils.GroundPlaneCfg())
    light = sim_utils.DomeLightCfg(intensity=2000.0)
    light.func('/World/light', light)
    rig, bottle = Articulation(RIG), RigidObject(BOTTLE)
    sim.reset()

    ids, _ = rig.find_joints(JOINTS, preserve_order=True)
    right, left = rig.find_joints(['right_driver_joint', 'left_driver_joint'], preserve_order=True)[0]
    pads, _ = rig.find_bodies(['left_pad', 'right_pad'], preserve_order=True)
    grip = torch.tensor(PAD_CENTRE, device=sim.device).repeat(len(pads), 1)
    dt = sim.get_physics_dt()
    start = bottle.data.root_pos_w[0].clone()
    held, landed, peak, t = None, None, 0.0, 0.0
    mimic_gap = 0.0   # how far the left driver strays from the right one
    while app.is_running() and t < plan.DURATION + 1.0:
        target = torch.tensor(plan.targets(t), dtype=torch.float32, device=sim.device)
        rig.set_joint_position_target(target.unsqueeze(0), joint_ids=ids)
        rig.write_data_to_sim()
        sim.step()
        t += dt
        rig.update(dt)
        bottle.update(dt)
        rise = float(bottle.data.root_pos_w[0, 2] - start[2])
        peak = max(peak, rise)
        if held is None and t >= plan.HELD_AT:
            held = rise
        q = rig.data.joint_pos[0]
        mimic_gap = max(mimic_gap, float(abs(q[left] - q[right])))
        if landed is None and t >= plan.GRIPPED_AT:
            centres = rig.data.body_pos_w[0, pads] + quat_apply(rig.data.body_quat_w[0, pads], grip)
            landed = float(centres[:, 2].mean() - start[2])

    end = bottle.data.root_pos_w[0]
    up = quat_apply(bottle.data.root_quat_w[0:1], torch.tensor([[0.0, 0.0, 1.0]], device=sim.device))[0]
    tilt = float(torch.rad2deg(torch.arccos(up[2].clamp(-1, 1))))
    moved = float(torch.linalg.norm(end[:2] - start[:2]))
    checks = {
        # If the importer dropped the mimic tags, the fingers are loose and
        # nothing after this means anything.
        f'left finger follows the right (mimic): {mimic_gap * 1000:.1f} mrad off at worst (want <= 20)':
            mimic_gap <= 0.02,
        f'gripped with the pads {landed * 1000:.1f} mm up the bottle (planned {plan.GRASP_Z * 1000:.0f} +- 5)':
            abs(landed - plan.GRASP_Z) <= 0.005,
        f'carried {held * 1000:.1f} mm at t={plan.HELD_AT} s (want >= {0.9 * plan.LIFT * 1000:.0f})':
            held >= 0.9 * plan.LIFT,
        f'set down {moved * 1000:.1f} mm from where it was picked (want <= 10)': moved <= 0.01,
        f'standing {tilt:.1f} deg off vertical (want <= 5)': tilt <= 5,
        f'back on the floor: z {float(end[2] - start[2]) * 1000:+.1f} mm':
            abs(float(end[2] - start[2])) <= 0.003,
    }
    print(f'peak lift {peak * 1000:.1f} mm')
    for label, ok in checks.items():
        print(f'  {"ok  " if ok else "FAIL"} {label}')
    app.close()
    sys.exit(0 if all(checks.values()) else 1)


if __name__ == '__main__':
    main()
