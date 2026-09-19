"""The UR10e hand shared by generate_hand_blend.py and generate_hand_viewer.py.

What is past the arm's last wrist joint: the wrist_3 flange and the Robotiq
2F-85 on it, plus the constants both generators need to place them. Both files
take the finger linkage from the same fit, so the .blend and the HTML viewer
open and close the gripper identically.

Frame: the tool frame of the arm. Origin on the flange face, +Z the approach
direction (the fingers point along +Z), the arm behind it along -Z.
"""
from pathlib import Path

import mujoco
import numpy as np

SIM = Path(__file__).resolve().parents[1]
MENAGERIE = SIM / 'third_party/mujoco_menagerie'
UR_MESHES = MENAGERIE / 'universal_robots_ur10e/assets'
GRIP_MESHES = MENAGERIE / 'robotiq_2f85/assets'
GRIPPER = SIM / 'assets/robotiq_2f85_sensed/2f85_sensed.xml'
OUT_DIR = SIM / 'assets/ur10e_hand'

# Where the gripper hangs off wrist_3_link: the arm MJCF's attachment_site.
FLANGE_POS = np.array([0.0, 0.1, 0.0])
FLANGE_QUAT = np.array([-1.0, 1.0, 0.0, 0.0]) / np.sqrt(2)

# The stand-in for the arm: the wrist housing's radius (eef_collision geom).
# It ends at the back of the wrist3 flange mesh, STUB_TOP behind the flange face.
STUB_RADIUS = 0.046
STUB_LENGTH = 0.15
STUB_TOP = -0.024
RING_HEIGHT = 0.012

# Colours from the two MJCFs (MuJoCo's default rgba for the unassigned pad).
MATERIALS = {
    'linkgray': (0.82, 0.82, 0.82, 1),
    'urblue': (0.49, 0.678, 0.8, 1),
    'grip_black': (0.149, 0.149, 0.149, 1),
    'grip_gray': (0.4627, 0.4627, 0.4627, 1),
    'grip_pad': (0.5, 0.5, 0.5, 1),
}
MESH_MATERIAL = {'base_mount': 'grip_black', 'base': 'grip_black',
                 'driver': 'grip_gray', 'coupler': 'grip_black',
                 'spring_link': 'grip_black', 'follower': 'grip_black',
                 'pad': 'grip_pad', 'silicone_pad': 'grip_black'}

POLY_DEGREE = 4
PAD_HALF_THICKNESS = 0.004   # pad_box1/2 half-size along the pad normal


def wrist3_pose() -> tuple[np.ndarray, np.ndarray]:
    """Pose of the wrist3.obj mesh in the tool frame.

    The mesh is in the wrist_3_link frame and the tool frame is the flange site
    in it, so the mesh sits at the inverse of the site's pose.
    """
    pos, quat = np.zeros(3), np.zeros(4)
    mujoco.mju_negPose(pos, quat, FLANGE_POS, FLANGE_QUAT)
    return pos, quat


def sweep_linkage() -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Close the gripper step by step in MuJoCo and record the linkage.

    Returns:
        The aperture at each step, and each finger joint's angle at each step.
    """
    model = mujoco.MjModel.from_xml_path(str(GRIPPER))
    model.opt.gravity[:] = 0
    data = mujoco.MjData(model)
    pads = [model.geom(f'{side}_pad1').id for side in ('left', 'right')]
    joints = [model.joint(j).name for j in range(model.njnt)]
    apertures, angles = [], {name: [] for name in joints}
    for ctrl in np.linspace(0, 255, 52):
        data.ctrl[0] = ctrl
        for _ in range(1500):
            mujoco.mj_step(model, data)
        # Inner faces of the two pads, along the line between them.
        left, right = data.geom_xpos[pads[0]], data.geom_xpos[pads[1]]
        apertures.append(np.linalg.norm(right - left) - 2 * PAD_HALF_THICKNESS)
        for name in joints:
            angles[name].append(data.qpos[model.joint(name).qposadr[0]])
    return np.array(apertures), {k: np.array(v) for k, v in angles.items()}


def fit_linkage(apertures, angles) -> dict[str, np.ndarray]:
    """Fit every joint angle as a polynomial in the aperture.

    Returns:
        Coefficients per joint, lowest power first.

    Raises:
        RuntimeError: If a fit misses a sampled angle by more than 0.01 rad.
    """
    fits = {}
    for name, q in angles.items():
        coef = np.polynomial.polynomial.polyfit(apertures, q, POLY_DEGREE)
        error = np.abs(np.polynomial.polynomial.polyval(apertures, coef) - q).max()
        if error > 0.01:
            raise RuntimeError(f'{name}: fit off by {error:.4f} rad')
        fits[name] = coef
    return fits


def linkage() -> tuple[float, float, dict[str, np.ndarray]]:
    """Sweep and fit the linkage.

    Returns:
        The closed and open apertures (m) and the per-joint fits.
    """
    apertures, angles = sweep_linkage()
    closed, opened = float(apertures.min()), float(apertures.max())
    print(f'aperture {closed * 1000:.1f} .. {opened * 1000:.1f} mm')
    return closed, opened, fit_linkage(apertures, angles)


def gripper_bodies(model: mujoco.MjModel):
    """Walk the 2F-85's bodies, parents first.

    Yields:
        (body id, name, parent id (0 = the flange), pos, quat, joint name or
        None, joint pos, names of its visual meshes).
    """
    for b in range(1, model.nbody):
        body = model.body(b)
        joint, jpos = None, np.zeros(3)
        if model.body_jntnum[b]:
            j = model.body_jntadr[b]
            joint, jpos = model.joint(j).name, model.jnt_pos[j].copy()
            assert np.allclose(model.jnt_axis[j], (1, 0, 0)), joint
        meshes = []
        for g in range(model.body_geomadr[b],
                       model.body_geomadr[b] + model.body_geomnum[b]):
            geom = model.geom(g)
            if geom.type[0] == mujoco.mjtGeom.mjGEOM_MESH and geom.group[0] == 2:
                meshes.append(model.mesh(geom.dataid[0]).name)
        yield (b, body.name, int(body.parentid[0]), body.pos.copy(),
               body.quat.copy(), joint, jpos, meshes)
