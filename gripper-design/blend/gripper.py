"""The parabolic gripper: beam and servo on the hand; each jaw its own body (a MuJoCo slide joint along Y) with the
hub pad, tab, carriage and combed wings. Built at the open stroke of the largest bottle; the Blender pose shows it
closed on the 60 ml through the jaw empties' offset, which the MJCF ignores (joint zero = open)."""
from hand_common import *

STROKE_OPEN = 31.64 + 23.71 + 6          # gripper.py stroke(r) on the 100 ml: EDGE + r + open_clear
JAW_TRAVEL = STROKE_OPEN                 # to the vertices meeting

def wing_bands(s):                       # the comb: +Y jaw two outer bands, -Y jaw the middle one, 1 mm apart
    H, third = 16, (32 - 2) / 3
    return [(-H, -H + third), (H - third, H)] if s > 0 else [(-H + third + 1, H - third - 1)]

def build(root, M, r_shown=BOTTLE_60['r']):
    box('beam', -31, -25, -HALF_IN, HALF_IN, GRIP_Z - 8, GRIP_Z + 8, M.gray)
    box('grip_servo', -52, -32, -22, 22, GRIP_Z - 8, GRIP_Z + 8, M.black)
    g, back = STROKE_OPEN, 9
    for s, tag in ((1, 'P'), (-1, 'N')):
        jaw = empty(f'jaw_{tag}', root, y=-s * (STROKE_OPEN - vertex(r_shown)))     # Blender only: shown closed on the 60 ml
        JOINTS.append(dict(name=f'jaw_{tag}', body=f'jaw_{tag}', axis=(0, -s, 0), range=(0, JAW_TRAVEL * MM)))
        y = lambda v: s * (g + v)
        lo, hi = sorted((y(0), y(back))); box(f'jaw_{tag}_pad', -12, 12, lo, hi, GRIP_Z - 16, GRIP_Z + 16, M.gray, jaw)
        lo, hi = sorted((y(-5), y(back))); box(f'jaw_{tag}_carriage', -30, -24, lo, hi, GRIP_Z - 12, GRIP_Z + 12, M.black, jaw)
        lo, hi = sorted((y(3), y(back))); box(f'jaw_{tag}_tab', -24, -10, lo, hi, GRIP_Z - 16, GRIP_Z + 16, M.gray, jaw)
        for side, st in ((1, 'R'), (-1, 'L')):                            # wings: straight 6 mm slabs, hub edge to wing tip, combed
            xa, ya, xb, yb = side * 12, g - 9, side * 22.5, g - 31.6
            L = math.hypot(xb - xa, yb - ya); ang = math.atan2(s * (yb - ya), xb - xa)
            for i, (z0, z1) in enumerate(wing_bands(s)):
                box(f'jaw_{tag}_wing_{st}{i}', -L / 2, L / 2, -3, 3, GRIP_Z + z0, GRIP_Z + z1, M.gray, jaw, rz=ang,
                    center=((xa + xb) / 2, s * (ya + yb) / 2, GRIP_Z + (z0 + z1) / 2))
        # the touch site over the whole cradle face, pad and wings, for the pad-force sensor (MuJoCo only)
        SITES.append(dict(name=f'{"right" if s > 0 else "left"}_pad_touch', body=f'jaw_{tag}', type='box',
                          pos=(0, s * (g - 16), GRIP_Z), size=(24, 17, 16)))
