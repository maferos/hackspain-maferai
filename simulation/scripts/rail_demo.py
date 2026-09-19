#!/usr/bin/env python3
"""Drive the UR10e along its rail over the MiniHannover bench.

Run from simulation/ after scripts/generate_rail_scene.py. Two motions:

* ``sweep`` --- the carriage runs the length of the bench holding a hand-down
  scan pose. Shows the working envelope.
* ``label`` --- parks the eye-in-hand camera square on one vessel's label after
  another, at the standoff and elevation computer-vision's reader wants, picking
  the approach bearing that is not blocked by a neighbour. This is the motion
  that answers "which compound is in this pot".
* ``visit`` --- picks vessels spread along the bench and visits each one: the
  carriage slides to a station the vessel is reachable from, the arm drops the
  gripper over the cap, holds, then moves on. This is the scanning motion the
  barcode reader needs, not a grasp: the bench population is baked in as static
  geometry, so there is nothing to pick up.

Motion is played back kinematically (mj_forward on interpolated poses) so the
demo is deterministic and cannot knock the glassware over. ``--physics`` instead
drives the position actuators and steps the simulator, which is the honest test
of whether the servos hold the arm up.

Examples:
    mjpython scripts/rail_demo.py --viewer
    python scripts/rail_demo.py --mode visit --video out/rail_visit.mp4
    python scripts/rail_demo.py --camera eih --frames out/eih

On macOS the viewer needs `mjpython`, not `python` --- launch_passive requires
it. Rendering offscreen works under either.
"""
import argparse
import itertools
import shutil
import subprocess
import sys
import time
from pathlib import Path

import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rail_kinematics as rk

FPS = 30
HOVER = 0.22          # gripper height over a cap while scanning it, in metres
SCAN_HEIGHT = 1.28    # pinch height for the sweep pose: over the tallest cap
SCAN_Y = -0.40        # middle of the populated band, in metres


def scan_pose(model: mujoco.MjModel, data: mujoco.MjData) -> np.ndarray:
    """Arm configuration for the sweep: hand down over the middle of the band.

    Args:
        model: Compiled scene.
        data: Scratch data, overwritten.

    Returns:
        The six arm joint angles.

    Raises:
        RuntimeError: If the pose is not reachable, which would mean the rail
            geometry in generate_rail_scene.py has moved.
    """
    station = rk.set_rail(model, data, 0.0)
    target = np.array([station, SCAN_Y, SCAN_HEIGHT])
    if not rk.solve_any(model, data, target):
        raise RuntimeError(f'scan pose unreachable at {target}')
    return data.qpos[rk.arm_qpos(model)].copy()


def sweep_waypoints(model: mujoco.MjModel, data: mujoco.MjData
                    ) -> list[tuple[float, np.ndarray]]:
    """Carriage from one end of the travel to the other, arm pose fixed."""
    pose = scan_pose(model, data)
    lo, hi = model.joint(rk.RAIL_JOINT).range
    home = model.body('rail_carriage').pos[0]
    return [(home + lo, pose), (home + hi, pose), (home + lo, pose)]


def visit_waypoints(model: mujoco.MjModel, data: mujoco.MjData, count: int
                    ) -> list[tuple[float, np.ndarray]]:
    """Stations and arm poses for scanning `count` vessels along the bench.

    Vessels are taken evenly along X so the carriage actually travels, and each
    one contributes three waypoints: above it, down at scanning height, and back
    up.

    Args:
        model: Compiled scene.
        data: Scratch data, overwritten.
        count: How many vessels to visit.

    Returns:
        (carriage X, arm pose) waypoints in order.
    """
    bottles = rk.bottles(model, data)
    picks = [bottles[i] for i in
             np.linspace(0, len(bottles) - 1, count).round().astype(int)]
    out = []
    for bottle in picks:
        low = bottle.cap + np.array([0.0, 0.0, HOVER])
        high = bottle.cap + np.array([0.0, 0.0, HOVER + 0.18])
        station = rk.reach(model, data, low)
        if station is None:
            print(f'  skipping {bottle.sample_id}: no station reaches it')
            continue
        down = data.qpos[rk.arm_qpos(model)].copy()
        rk.set_rail(model, data, station)
        up = down if not rk.solve_any(model, data, high) else \
            data.qpos[rk.arm_qpos(model)].copy()
        out += [(station, up), (station, down), (station, down), (station, up)]
    return out


def label_waypoints(model: mujoco.MjModel, data: mujoco.MjData, count: int
                    ) -> tuple[list[tuple[float, np.ndarray]], list[str]]:
    """Stations and poses for reading `count` labels with the wrist camera.

    Each vessel gets four waypoints: lifted clear at the scan pose, down on the
    label, a dwell there, and back up. Lifting between targets keeps the
    interpolated path from dragging the arm through the glassware.

    Args:
        model: Compiled scene.
        data: Scratch data, overwritten.
        count: How many labels to read.

    Returns:
        The waypoints, and the sample id each one is looking at.
    """
    bottles = rk.bottles(model, data)
    picks = [bottles[i] for i in
             np.linspace(0, len(bottles) - 1, count).round().astype(int)]
    clear = scan_pose(model, data)
    out, captions = [], []
    for bottle in picks:
        found = rk.read_label(model, data, bottle)
        if found is None:
            print(f'  skipping {bottle.sample_id}: no clear line on its label')
            continue
        station, _ = found
        pose = data.qpos[rk.arm_qpos(model)].copy()
        out += [(station, clear), (station, pose), (station, pose),
                (station, clear)]
        captions += [f'travelling to {bottle.sample_id}', bottle.sample_id,
                     bottle.sample_id, f'leaving {bottle.sample_id}']
    return out, captions


def trajectory(model: mujoco.MjModel, waypoints: list[tuple[float, np.ndarray]],
               speed: float, dwell: float = 1.5) -> np.ndarray:
    """Interpolate waypoints into per-frame (rail, arm) rows.

    Segment duration comes from whichever moves further: the carriage at
    `speed` m/s, or the fastest joint at 1.4 rad/s, which is about what a UR10e
    does at a sane tool speed.

    Args:
        model: Compiled scene.
        waypoints: (carriage X, arm pose) pairs.
        speed: Carriage speed in metres per second.
        dwell: Seconds to hold still when two waypoints are identical, which is
            how the modes ask for a pause on a target.

    Returns:
        Array of shape (frames, 7): carriage X then the six joint angles.
    """
    return segmented(model, waypoints, speed, dwell)[0]


def segmented(model: mujoco.MjModel, waypoints: list[tuple[float, np.ndarray]],
              speed: float, dwell: float = 1.5
              ) -> tuple[np.ndarray, np.ndarray]:
    """Interpolate waypoints, and say which segment each frame came from.

    Args:
        model: Compiled scene.
        waypoints: (carriage X, arm pose) pairs.
        speed: Carriage speed in metres per second.
        dwell: Seconds to hold still between identical waypoints.

    Returns:
        The trajectory rows, and the source segment index of each row.
    """
    rows, owners = [], []
    for segment, ((x0, q0), (x1, q1)) in enumerate(itertools.pairwise(waypoints)):
        travel = max(abs(x1 - x0) / speed, float(np.abs(q1 - q0).max()) / 1.4)
        seconds = max(travel, dwell if travel < 1e-6 else 0.35)
        steps = max(int(seconds * FPS), 1)
        for step in range(steps):
            # Cosine ease keeps the carriage from stepping instantly at 6 m/s.
            alpha = 0.5 - 0.5 * np.cos(np.pi * (step + 1) / steps)
            rows.append(np.concatenate([[x0 + alpha * (x1 - x0)],
                                        q0 + alpha * (q1 - q0)]))
            owners.append(segment)
    return np.array(rows), np.array(owners)


def waypoints(model: mujoco.MjModel, data: mujoco.MjData, mode: str,
              count: int) -> list[tuple[float, np.ndarray]]:
    """Build the waypoints for one of the demo modes.

    Args:
        model: Compiled scene.
        data: Scratch data, overwritten.
        mode: ``sweep``, ``visit`` or ``label``.
        count: Vessels to visit, for the modes that visit vessels.

    Returns:
        (carriage X, arm pose) waypoints in order.
    """
    if mode == 'sweep':
        return sweep_waypoints(model, data)
    if mode == 'visit':
        return visit_waypoints(model, data, count)
    return label_waypoints(model, data, count)[0]


def apply(model: mujoco.MjModel, data: mujoco.MjData, row: np.ndarray,
          physics: bool) -> None:
    """Put the machine at one trajectory row, kinematically or by servo."""
    if physics:
        data.ctrl[model.actuator(rk.RAIL_JOINT).id] = (
            row[0] - model.body('rail_carriage').pos[0])
        for name, value in zip(rk.ARM_JOINTS, row[1:]):
            actuator = name.replace('_joint', '').replace('arm_', 'arm_')
            data.ctrl[model.actuator(actuator).id] = value
        for _ in range(round(1 / FPS / model.opt.timestep)):
            mujoco.mj_step(model, data)
    else:
        rk.set_rail(model, data, row[0])
        data.qpos[rk.arm_qpos(model)] = row[1:]
        mujoco.mj_forward(model, data)


def resolve_camera(model: mujoco.MjModel, name: str) -> str:
    """Accept the arm's cameras without their attachment prefix.

    Attaching the arm renames its cameras, so the eye-in-hand one compiles as
    ``arm_eih``. Callers should not have to know that.

    Args:
        model: Compiled scene.
        name: Camera name as the user typed it.

    Returns:
        A camera name that exists in the model.

    Raises:
        ValueError: If neither the plain nor the prefixed name exists.
    """
    known = {mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_CAMERA, i)
             for i in range(model.ncam)}
    for candidate in (name, f'arm_{name}'):
        if candidate in known:
            return candidate
    raise ValueError(f'no camera {name!r}; scene has {sorted(known)}')


def render(model: mujoco.MjModel, data: mujoco.MjData, rows: np.ndarray,
           camera: str, out: Path, physics: bool, width: int, height: int
           ) -> Path:
    """Render the trajectory offscreen to PNG frames, and to mp4 if ffmpeg is on
    the path.

    Args:
        model: Compiled scene.
        data: Data to drive.
        rows: Trajectory rows from :func:`trajectory`.
        camera: Scene camera name.
        out: Output mp4 path, or a directory for frames only.
        physics: Whether to step the simulator instead of posing kinematically.
        width: Frame width in pixels.
        height: Frame height in pixels.

    Returns:
        The directory the frames were written to.
    """
    camera = resolve_camera(model, camera)
    frames_dir = out if out.suffix == '' else out.with_suffix('')
    frames_dir.mkdir(parents=True, exist_ok=True)
    renderer = mujoco.Renderer(model, height=height, width=width)
    from PIL import Image
    for i, row in enumerate(rows):
        apply(model, data, row, physics)
        renderer.update_scene(data, camera=camera)
        Image.fromarray(renderer.render()).save(frames_dir / f'{i:05d}.png')
        if i % 30 == 0:
            print(f'  frame {i}/{len(rows)}')
    renderer.close()

    if out.suffix == '.mp4' and shutil.which('ffmpeg'):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate',
                        str(FPS), '-i', str(frames_dir / '%05d.png'),
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(out)],
                       check=True)
        print(f'wrote {out}')
    return frames_dir


def view(model: mujoco.MjModel, data: mujoco.MjData, rows: np.ndarray,
         physics: bool) -> None:
    """Loop the trajectory in the interactive viewer until the window closes."""
    import mujoco.viewer
    with mujoco.viewer.launch_passive(model, data) as viewer:
        i = 0
        while viewer.is_running():
            start = time.time()
            apply(model, data, rows[i % len(rows)], physics)
            viewer.sync()
            i += 1
            remaining = 1 / FPS - (time.time() - start)
            if remaining > 0:
                time.sleep(remaining)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('sweep', 'visit', 'label'),
                        default='sweep')
    parser.add_argument('--visits', type=int, default=6,
                        help='vessels to scan in visit and label modes')
    parser.add_argument('--speed', type=float, default=0.8,
                        help='carriage speed, m/s')
    parser.add_argument('--dwell', type=float, default=1.5,
                        help='seconds to hold on each target')
    parser.add_argument('--viewer', action='store_true',
                        help='interactive window; needs mjpython on macOS')
    parser.add_argument('--video', type=Path,
                        help='render to this mp4 (frames land beside it)')
    parser.add_argument('--frames', type=Path, help='render PNG frames here')
    parser.add_argument('--camera', default='general',
                        help='general, carriage, eih (eye-in-hand) or any scene camera')
    parser.add_argument('--resolution', default='1280x720')
    parser.add_argument('--physics', action='store_true',
                        help='drive the position actuators and step, rather '
                             'than posing kinematically')
    args = parser.parse_args()

    model, data = rk.load()
    print(f'scene: {rk.SCENE.name}, {len(rk.bottles(model, data))} vessels')
    rows = trajectory(model, waypoints(model, data, args.mode, args.visits),
                      args.speed, args.dwell)
    print(f'{args.mode}: {len(rows)} frames, {len(rows) / FPS:.1f} s, '
          f'carriage {rows[:, 0].min():.2f} .. {rows[:, 0].max():.2f} m')

    mujoco.mj_resetData(model, data)
    if args.physics:
        mujoco.mj_forward(model, data)
    if args.viewer:
        view(model, data, rows, args.physics)
        return
    out = args.video or args.frames
    if out is None:
        print('nothing to do: pass --viewer, --video or --frames')
        return
    width, height = (int(v) for v in args.resolution.split('x'))
    print(f'wrote frames to {render(model, data, rows, args.camera, out, args.physics, width, height)}')


if __name__ == '__main__':
    main()
