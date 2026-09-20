"""A compact two-finger gripper with curved, wrapping jaws, built in memory.

Why it exists (README.md, "v3"): the 2F-85 hangs 37.5 mm below its own axis
and rises 13.5 mm above it, and the clamp's housing comes down to 2.5 mm under
the cap seat. Those two put the gripper's axis in a window that closes for any
bottle whose cap seat is under 57.5 mm, which rules out the 10 and 20 ml amber
bottles on a bare table, whatever the fingertips look like.

This one is drawn around that window instead:

* what hangs below the axis is a jaw, not a base: 16 mm, so the axis can come
  down to 18 mm over the table;
* what rises above it is the same 16 mm, so the axis fits under the clamp from
  a 39 mm cap seat up;
* the drive sits behind the jaws, where there is room;
* each jaw is one **parabolic cradle**, the same pair for every bottle. A
  parabola y = v - x^2 / 2p holds a cylinder of any radius r > p on two
  symmetric lines, at x = +-sqrt(r^2 - p^2): the contact walks outwards as the
  bottle grows, so one shape cradles the 10 ml and the 100 ml alike, and the
  bottle is centred by the pair, not by where the arm put it. With p = 8 mm
  the contact normals stand 43 degrees off the closing direction on the
  smallest bottle and 70 on the widest, so the wide ones are the best held.
  The surface is faceted into convex plates, which is what MuJoCo collides.

The jaws are mirror images and never change; only how far they close does,
and that follows from the bottle's radius: the cradle's vertex sits at
(r^2 + p^2) / 2p from the axis when the curve just touches.
"""
import math

import mujoco
import numpy as np

# Everything in metres, in the tool frame used here: +X from the arm to the
# bottle (the fingers point along it), Y the closing direction, Z up.
JAW = {
    'p': 0.008,                   # the parabola's parameter: y = v - x^2 / 2p
    'half_width': 0.0225,         # how far the cradle runs either side of its vertex,
                                  # stopped where the widest bottle touches (sqrt(r^2 - p^2))
    'facets': 11,                 # convex plates the curve is cut into
    'clearance': 0.0002,          # the cradle stands this far off the bottle before it squeezes
    'liner': 0.003,               # the high-friction liner's thickness
    'half_height': 0.016,         # the jaw's vertical half extent: what hangs below the axis
    'plate': 0.006,               # the backing plate behind the liner
    'open_clear': 0.006,          # what the bottle clears on the way down
    'friction': (1.6, 0.02, 0.0005),   # a soft, grippy elastomer
    'solref': (0.004, 1.0),       # as compliant as the 2F-85's pads
    'mass': 0.12,
}
BODY = {          # the drive, behind the jaws and clear of the widest bottle
    'length': 0.052, 'half_width': 0.032, 'half_height': 0.016, 'mass': 0.7,
}
FRONT_CLEAR = 0.030       # from the bottle's axis to the drive's front face
FLANGE_X = -0.118         # the wrist flange behind the jaws' centre
GAINS = (300000.0, 2000.0, 400.0)   # kp, kv, N: the limit is the grip force
SQUEEZE = 0.0015          # how far past the bottle's centre each jaw is told to go
PAD_GEOMS = tuple(f'{s}_pad{k}' for s in ('left', 'right') for k in range(JAW['facets']))
JOINTS = ('left_jaw', 'right_jaw')


def vertex(bottle_r: float) -> float:
    """How far the cradle's vertex stands from the bottle's axis when the curve
    just touches a cylinder of that radius: (r^2 + p^2) / 2p."""
    p = JAW['p']
    return (bottle_r * bottle_r + p * p) / (2 * p) + JAW['clearance']


def contact_x(bottle_r: float) -> float:
    """Where the two lines of contact sit along the fingers: sqrt(r^2 - p^2)."""
    return math.sqrt(max(0.0, bottle_r * bottle_r - JAW['p'] * JAW['p']))


def contact_angle(bottle_r: float) -> float:
    """The contact normal's angle off the closing direction."""
    return math.acos(min(1.0, JAW['p'] / bottle_r))


def stroke(bottle_r: float) -> float:
    """How far the vertex retracts so the bottle clears the cradle's edges on
    the way down: the edge is `half_width^2 / 2p` ahead of the vertex."""
    edge = JAW['half_width'] ** 2 / (2 * JAW['p'])
    return edge + bottle_r + JAW['open_clear']


def mouth(bottle_r: float) -> float:
    """The gap between the open jaws' innermost points, either side of the axis."""
    return stroke(bottle_r) - JAW['half_width'] ** 2 / (2 * JAW['p'])


def envelope() -> dict:
    """What the gripper occupies about its axis, for the layout rules."""
    return {'below': max(JAW['half_height'], BODY['half_height']),
            'above': max(JAW['half_height'], BODY['half_height']), 'flange_x': FLANGE_X}


def _facets(side: int) -> list[tuple[tuple, tuple, tuple]]:
    """The parabola cut into chords, as (pos, euler in degrees, half size) in
    the jaw's frame with the cradle's vertex at the origin and the bottle at
    -side y. The same plates on both jaws, mirrored."""
    p, W, n = JAW['p'], JAW['half_width'], JAW['facets']
    xs = np.linspace(-W, W, n + 1)
    out = []
    for a, b in zip(xs[:-1], xs[1:]):
        ya, yb = -a * a / (2 * p), -b * b / (2 * p)      # towards the bottle as |x| grows
        mid = np.array([(a + b) / 2, side * (ya + yb) / 2, 0.0])
        along = np.array([b - a, side * (yb - ya), 0.0])
        length = float(np.linalg.norm(along))
        psi = math.degrees(math.atan2(along[1], along[0]))
        normal = np.array([-along[1], along[0], 0.0]) / length * side   # away from the bottle
        pos = mid + normal * (JAW['liner'] / 2) * side
        out.append((tuple(pos), (0.0, 0.0, psi), (length / 2, JAW['liner'] / 2, JAW['half_height'])))
    return out


def add(spec: mujoco.MjSpec, parent: str, mask: tuple[int, int], rig_mask: tuple[int, int],
        bottle_r: float, mount_quat=(0.5, -0.5, -0.5, -0.5)) -> None:
    """Add the gripper to `parent` (the wrist link, whose frame is the arm's
    tool frame) and lay it out in the hand's own axes: +X towards the bottle,
    Y closing, Z up. The jaws are the same for every bottle; `bottle_r` only
    sets how far they have to travel."""
    s = stroke(bottle_r)
    mount = spec.body(parent).add_body(name='grip_mount', quat=list(mount_quat))
    base_x = -FLANGE_X - FRONT_CLEAR - BODY['length'] / 2
    base = mount.add_body(name='grip_base', pos=[base_x, 0, 0])
    base.add_geom(name='grip_body', type=mujoco.mjtGeom.mjGEOM_BOX,
                  size=[BODY['length'] / 2, BODY['half_width'], BODY['half_height']],
                  rgba=[0.26, 0.28, 0.31, 1], mass=BODY['mass'], contype=rig_mask[0], conaffinity=rig_mask[1])
    arm = FRONT_CLEAR + BODY['length'] / 2
    for side, name in ((+1, 'left'), (-1, 'right')):
        jaw = base.add_body(name=f'{name}_jaw', pos=[arm, 0, 0])
        jaw.add_joint(name=f'{name}_jaw', type=mujoco.mjtJoint.mjJNT_SLIDE, axis=[0, side, 0],
                      range=[-s - SQUEEZE, 0.0], damping=20.0, armature=0.02)
        for k, (pos, euler, half) in enumerate(_facets(side)):
            g = jaw.add_geom(name=f'{name}_pad{k}', type=mujoco.mjtGeom.mjGEOM_BOX, size=list(half),
                             pos=[pos[0], side * s + pos[1], pos[2]], euler=list(euler),
                             rgba=[0.13, 0.14, 0.16, 1], mass=JAW['mass'] / JAW['facets'],
                             contype=mask[0], conaffinity=mask[1],
                             friction=list(JAW['friction']), solref=list(JAW['solref']))
            g.priority = 1        # the jaws' own friction and solref rule the contact
        back = JAW['liner'] + JAW['plate'] / 2
        jaw.add_geom(name=f'{name}_jaw_back', type=mujoco.mjtGeom.mjGEOM_BOX,
                     size=[JAW['half_width'] + JAW['plate'], JAW['plate'] / 2, JAW['half_height']],
                     pos=[0, side * (s + back), 0], rgba=[0.26, 0.28, 0.31, 1], mass=0,
                     contype=rig_mask[0], conaffinity=rig_mask[1])
        jaw.add_geom(name=f'{name}_jaw_arm', type=mujoco.mjtGeom.mjGEOM_BOX,
                     size=[arm / 2, JAW['plate'] / 2, JAW['half_height'] / 2],
                     pos=[-arm / 2, side * (s + back), 0], rgba=[0.26, 0.28, 0.31, 1], mass=0,
                     contype=rig_mask[0], conaffinity=rig_mask[1])
    for name in JOINTS:
        spec.add_actuator(name=name, target=name, trntype=mujoco.mjtTrn.mjTRN_JOINT,
                          gainprm=[GAINS[0]] + [0] * 9, biastype=mujoco.mjtBias.mjBIAS_AFFINE,
                          biasprm=[0, -GAINS[0], -GAINS[1]] + [0] * 7,
                          ctrlrange=[-s - SQUEEZE, 0.0], forcerange=[-GAINS[2], GAINS[2]])


def jaw_target(aperture: float, bottle_r: float, open_aperture: float = 0.085) -> float:
    """Where each jaw is told to go for the plan's aperture: wide open at
    `open_aperture`, and SQUEEZE past touching once the plan says it is closed
    on the bottle. The drive stalls on the bottle at its force limit, which is
    the grip force."""
    s, v = stroke(bottle_r), vertex(bottle_r)
    span = max(1e-6, open_aperture - 2 * bottle_r)
    t = min(1.0, max(0.0, (aperture - 2 * bottle_r) / span))
    return (t * s + (1 - t) * (v - SQUEEZE)) - s      # 0 when open, v - SQUEEZE - s when closed


def grip_lines(bottle_r: float) -> int:
    """How many lines of contact hold the bottle: two per jaw, where the
    parabola meets the cylinder."""
    return 4


if __name__ == '__main__':
    e = envelope()
    print(f"envelope: {1e3 * e['below']:.0f} mm below the axis, {1e3 * e['above']:.0f} above; "
          f"flange {1e3 * FLANGE_X:.0f} mm behind the jaws")
    print(f"axis must sit >= {1e3 * (e['below'] + 0.002):.1f} mm over the table and <= cap seat - "
          f"{1e3 * (e['above'] + 0.0045):.1f} mm")
    print(f"jaws: one parabola, p = {1e3 * JAW['p']:.0f} mm, +-{1e3 * JAW['half_width']:.1f} mm wide, "
          f"{JAW['facets']} facets, {GAINS[2]:.0f} N, friction {JAW['friction'][0]}")
    for ml, cap, r in ((10, 39.7, 11.0), (20, 53.3, 13.85), (30, 61.6, 15.85),
                       (50, 72.5, 18.8), (60, 78.1, 20.0), (100, 93.9, 23.7)):
        lo, hi = 1e3 * (e['below'] + 0.002), cap - 1e3 * (e['above'] + 0.0045)
        axis = cap - 21
        rr = r / 1e3
        print(f'{ml:4d} ml: axis {axis:5.1f} in [{lo:.1f}, {hi:.1f}] {"ok" if lo <= axis <= hi else "OUT"}; '
              f'vertex at {1e3 * vertex(rr):5.1f} mm, contacts at +-{1e3 * contact_x(rr):4.1f} mm '
              f'({math.degrees(contact_angle(rr)):4.1f} deg), stroke {1e3 * stroke(rr):5.1f}, '
              f'mouth {1e3 * mouth(rr):5.1f} mm')
