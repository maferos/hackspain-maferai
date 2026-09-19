#!/usr/bin/env python3
"""Measure what the railed UR10e can actually reach on the MiniHannover bench.

Run from simulation/ after scripts/generate_rail_scene.py:
    python scripts/rail_reach.py

For every vessel on the bench it solves top-down inverse kinematics for the
gripper's pinch point 20 mm over the cap, and reports three cases:

* the rail, free to stand anywhere along its travel;
* the best single fixed station, found by scanning the travel --- what you would
  get by bolting the arm down instead of railing it;
* the same, but forbidden to stand off along the rail, which isolates how much
  of the win is the arm's own inner dead zone rather than its reach.

The answer is geometric only. It ignores collisions, so "reachable" means the
arm can hold that pose, not that it can get there without knocking a flask over.
"""
import argparse

import numpy as np
import rail_kinematics as rk

CLEARANCE = 0.02   # pinch point over the cap, in metres


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stations', type=int, default=25,
                        help='fixed stations to try when scanning the travel')
    args = parser.parse_args()

    model, data = rk.load()
    bottles = rk.bottles(model, data)
    targets = [b.cap + np.array([0.0, 0.0, CLEARANCE]) for b in bottles]
    lo, hi = model.joint(rk.RAIL_JOINT).range
    home = model.body('rail_carriage').pos[0]
    base_z = float(data.body('arm_base').xpos[2])
    base_y = float(data.body('arm_base').xpos[1])

    print(f'scene      {rk.SCENE.name}')
    print(f'vessels    {len(bottles)}  '
          f'x {min(b.x for b in bottles):+.2f} .. {max(b.x for b in bottles):+.2f} m, '
          f'y {min(b.y for b in bottles):+.2f} .. {max(b.y for b in bottles):+.2f} m')
    print(f'arm base   y {base_y:+.2f} m, z {base_z:.2f} m '
          f'({base_z - rk.BENCH_TOP:.2f} m over the worktop)')
    print(f'rail       {home + lo:+.2f} .. {home + hi:+.2f} m ({hi - lo:.2f} m travel)\n')

    stations = [rk.reach(model, data, t) for t in targets]
    railed = sum(s is not None for s in stations)
    print(f'rail, free to stand anywhere      {railed:3d}/{len(bottles)}'
          f'  ({railed / len(bottles):.0%})')

    no_standoff = 0
    for bottle, target in zip(bottles, targets):
        rk.set_rail(model, data, bottle.x)
        no_standoff += rk.solve_any(model, data, target)
    print(f'rail, carriage always over the cap {no_standoff:3d}/{len(bottles)}'
          f'  ({no_standoff / len(bottles):.0%})')

    best_x, best_hits = None, -1
    for x in np.linspace(home + lo, home + hi, args.stations):
        rk.set_rail(model, data, float(x))
        hits = sum(rk.solve_any(model, data, t) for t in targets)
        if hits > best_hits:
            best_x, best_hits = float(x), hits
    print(f'best single fixed station         {best_hits:3d}/{len(bottles)}'
          f'  ({best_hits / len(bottles):.0%})  at x = {best_x:+.2f} m\n')

    offsets = [abs(s - b.x) for s, b in zip(stations, bottles) if s is not None]
    if offsets:
        print(f'standoff used: {np.mean(offsets) * 1000:.0f} mm mean, '
              f'{max(offsets) * 1000:.0f} mm worst')
    missed = [b.sample_id for b, s in zip(bottles, stations) if s is None]
    if missed:
        print(f'unreachable: {len(missed)} -> {", ".join(missed[:8])}')


if __name__ == '__main__':
    main()
