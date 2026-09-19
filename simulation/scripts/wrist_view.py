#!/usr/bin/env python3
"""Watch the wrist camera live while the arm works the bench.

Opens the interactive MuJoCo window and, at the same time, streams what the
eye-in-hand camera sees to a browser tab, so the two views sit side by side:
the room on one side, the robot's own view on the other.

Run from simulation/, under mjpython --- launch_passive needs it on macOS:

    .venv/bin/mjpython scripts/wrist_view.py                    # sweep the bench
    .venv/bin/mjpython scripts/wrist_view.py --mode label       # read labels
    .venv/bin/mjpython scripts/wrist_view.py --mode label --visits 10

The browser tab is opened automatically at http://localhost:8008. Nothing is
installed for it: the stream is multipart JPEG off the standard library's HTTP
server, which every browser has played since 1995.

The arm is driven kinematically, the same as scripts/rail_demo.py, so the
motion is deterministic and cannot knock the glassware over. The MuJoCo window
is fully interactive meanwhile --- orbit, zoom, and `[` / `]` to cycle its own
camera, `arm_eih` among them if you would rather have the wrist view large and
the room small.
"""
import argparse
import http.server
import io
import json
import sys
import threading
import time
import webbrowser
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import grasp_test as gt
import pipette_test as pt
import pipetting as pip
import rail_demo as rd
import rail_kinematics as rk

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Wrist camera</title>
<style>
  :root { color-scheme: dark; }
  body { margin: 0; background: #14161a; color: #e8e6e1;
         font: 15px/1.5 ui-sans-serif, system-ui, sans-serif;
         display: flex; flex-direction: column; min-height: 100vh; }
  header { padding: 14px 18px; border-bottom: 1px solid #2a2e35; }
  h1 { margin: 0; font-size: 15px; font-weight: 600; letter-spacing: .01em; }
  p { margin: 2px 0 0; color: #9aa0a8; font-size: 13px; }
  main { flex: 1; display: grid; grid-template-columns: 1fr 260px; gap: 18px;
          align-items: start; padding: 18px; }
  @media (max-width: 860px) { main { grid-template-columns: 1fr; } }
  .views { display: grid; gap: 12px; grid-template-columns: 1fr 1fr; }
  @media (max-width: 1200px) { .views { grid-template-columns: 1fr; } }
  figure { margin: 0; }
  figcaption { font-size: 11px; letter-spacing: .08em; text-transform: uppercase;
               color: #6f757d; margin: 0 0 6px; font-weight: 600; }
  img { width: 100%; border-radius: 6px; border: 1px solid #2a2e35;
        background: #000; display: block; }
  #caption { font-variant-numeric: tabular-nums; color: #e8e6e1; }
  dl { margin: 0; display: grid; grid-template-columns: auto 1fr; gap: 6px 12px;
       font-size: 13px; font-variant-numeric: tabular-nums; }
  dt { color: #9aa0a8; }
  dd { margin: 0; text-align: right; }
  h2 { font-size: 11px; letter-spacing: .08em; text-transform: uppercase;
       color: #6f757d; margin: 18px 0 8px; font-weight: 600; }
  h2:first-child { margin-top: 0; }
  .on { color: #7fd18b; } .off { color: #6f757d; }
  aside { border: 1px solid #2a2e35; border-radius: 6px; padding: 14px 16px; }
</style></head>
<body>
  <header>
    <h1>MiniHannover rail &middot; overview and wrist camera</h1>
    <p><span id="caption">&hellip;</span></p>
  </header>
  <main>
    <div class="views">
      <figure>
        <figcaption>Overview</figcaption>
        <img src="/view/overview.mjpg" alt="overview">
      </figure>
      <figure>
        <figcaption>Eye in hand</figcaption>
        <img src="/view/wrist.mjpg" alt="wrist camera">
      </figure>
    </div>
    <aside>
      <h2>Liquid</h2>
      <dl>
        <dt>Beaker</dt><dd><span id="beaker_ml">-</span> ml</dd>
        <dt>Beaker mass</dt><dd><span id="beaker_g">-</span> g</dd>
        <dt>On the bench</dt><dd><span id="on_bench_ml">-</span> ml</dd>
        <dt>Tip height</dt><dd><span id="tip_z">-</span> m</dd>
      </dl>
      <h2>Machine</h2>
      <dl>
        <dt>Carriage X</dt><dd><span id="carriage_x">-</span> m</dd>
        <dt>Tool</dt><dd><span id="tool">-</span></dd>
      </dl>
      <h2>Simulation</h2>
      <dl>
        <dt>Contacts</dt><dd><span id="contacts">-</span></dd>
        <dt>Sim clock</dt><dd><span id="sim_time">-</span> s</dd>
        <dt>Speed</dt><dd><span id="speed">-</span>x</dd>
      </dl>
    </aside>
  </main>
  <script>
    const put = (id, v) => { document.getElementById(id).textContent = v; };
    setInterval(async () => {
      try {
        const t = await (await fetch('/telemetry')).json();
        put('caption', t.caption);
        for (const k of ['beaker_ml','beaker_g','on_bench_ml','tip_z',
                         'carriage_x','contacts','sim_time','speed'])
          if (k in t) put(k, t[k]);
        put('tool', t.tool.join(', '));
      } catch (e) { /* the run ended; keep the last frame on screen */ }
    }, 200);
  </script>
</body></html>
"""


class Feed:
    """The latest wrist frame, handed from the simulation loop to the server."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._frames: dict[str, bytes] = {}
        self._state: dict[str, object] = {'caption': 'starting'}
        self._tick = 0

    def publish(self, frames: dict[str, bytes],
                state: dict[str, object]) -> None:
        """Replace the current frames and the readings that go with them."""
        with self._lock:
            self._frames, self._state = frames, state
            self._tick += 1

    def latest(self, view: str) -> tuple[bytes | None, int]:
        """One view's current frame, and a counter that changes when it does."""
        with self._lock:
            return self._frames.get(view), self._tick

    @property
    def state(self) -> dict[str, object]:
        """The readings that went with the latest frame."""
        with self._lock:
            return dict(self._state)


class Handler(http.server.BaseHTTPRequestHandler):
    """Serves the page, the MJPEG stream and the caption."""

    feed: Feed

    def do_GET(self) -> None:
        if self.path.startswith('/view/'):
            self._stream(self.path[len('/view/'):].split('.')[0])
        elif self.path.startswith('/telemetry'):
            self._send(json.dumps(self.feed.state).encode(),
                       'application/json; charset=utf-8')
        elif self.path.startswith('/caption'):
            self._send(str(self.feed.state.get('caption', '')).encode(),
                       'text/plain; charset=utf-8')
        else:
            self._send(PAGE.encode(), 'text/html; charset=utf-8')

    def _send(self, body: bytes, content_type: str) -> None:
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _stream(self, view: str) -> None:
        self.send_response(200)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Type',
                         'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()
        seen = -1
        try:
            while True:
                jpeg, tick = self.feed.latest(view)
                if jpeg is None or tick == seen:
                    time.sleep(1 / 90)
                    continue
                seen = tick
                self.wfile.write(b'--frame\r\nContent-Type: image/jpeg\r\n'
                                 b'Content-Length: ' + str(len(jpeg)).encode()
                                 + b'\r\n\r\n' + jpeg + b'\r\n')
        except (BrokenPipeError, ConnectionResetError):
            pass          # the tab was closed or reloaded

    def log_message(self, *args) -> None:
        """Stay quiet; the interesting output is the simulation's."""


def serve(feed: Feed, port: int) -> http.server.ThreadingHTTPServer:
    """Start the viewer's HTTP server on a daemon thread.

    Args:
        feed: Frame source the handlers read from.
        port: TCP port to listen on.

    Returns:
        The running server.
    """
    handler = type('BoundHandler', (Handler,), {'feed': feed})
    server = http.server.ThreadingHTTPServer(('127.0.0.1', port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def captions_for(mode: str, model: mujoco.MjModel, data: mujoco.MjData,
                 count: int) -> tuple[list[tuple[float, np.ndarray]], list[str]]:
    """Waypoints for a mode, with a caption per segment.

    Args:
        model: Compiled scene.
        data: Scratch data, overwritten.
        mode: ``sweep``, ``visit`` or ``label``.
        count: Vessels to visit, for the modes that visit vessels.

    Returns:
        The waypoints and one caption per waypoint.
    """
    if mode == 'label':
        return rd.label_waypoints(model, data, count)
    points = rd.waypoints(model, data, mode, count)
    return points, ['sweeping the bench'] * len(points)


def pick_programme(model: mujoco.MjModel, data: mujoco.MjData, count: int):
    """Run pick-and-place on the dynamic vessels, stepping physics throughout.

    A generator: it yields a caption after every simulation step, so the caller
    can render and sync between steps. Everything the arm does goes through the
    position actuators and ``mj_step``, which is the point --- the arm stops at
    the bench instead of passing through it, the vessels it brushes move, and
    the gripper closes until its own sensors say it has something.

    Args:
        model: Compiled scene.
        data: Data to run in.
        count: How many vessels to work through before looping.

    Yields:
        A short line describing what is happening.
    """
    ids = gt.actuators(model)
    grip_id = model.actuator('arm_grip_fingers_actuator').id
    home = model.body('rail_carriage').pos[0]
    steps_per_second = round(1 / model.opt.timestep)

    def drive(station, pose, grip, seconds, caption, stop_on_grip=False):
        start = np.array([data.ctrl[i] for i in ids])
        goal = np.concatenate([[station - home], pose])
        # Give a long move long enough to arrive: a fixed time is fine for the
        # short hops and leaves the arm still flying on the way across 6 m.
        move = np.abs(goal - start)
        seconds = max(seconds, float(move[0]) / 0.6, float(move[1:].max()) / 0.9)
        # Three quarters ramp, one quarter sitting on the target: a position
        # servo lags, and reading the tool before it has caught up is what made
        # the first grasps close 20 to 47 mm off the vessel.
        total = max(int(seconds * steps_per_second), 1)
        ramp = max(int(total * 0.7), 1)
        for step in range(total):
            alpha = 0.5 - 0.5 * np.cos(np.pi * min(step + 1, ramp) / ramp)
            for i, value in zip(ids, start + alpha * (goal - start)):
                data.ctrl[i] = value
            if grip is not None:
                data.ctrl[grip_id] = grip(step, total)
            mujoco.mj_step(model, data)
            yield caption
            if stop_on_grip and step > total * 0.25 and \
                    rk.read_grip(model, data).holding:
                return

    mujoco.mj_resetData(model, data)
    mujoco.mj_forward(model, data)
    vessels = [b for b in rk.bottles(model, data) if b.dynamic][:count]
    while True:
        for bottle in vessels:
            grasp = rk.BENCH_TOP + (bottle.top - rk.BENCH_TOP) * gt.GRASP_FRACTION
            above = np.array([bottle.x, bottle.y, grasp + gt.APPROACH])
            on = np.array([bottle.x, bottle.y, grasp])
            # solve_ik writes its iterates straight into qpos, so the running
            # state has to be put back afterwards or the arm teleports to the
            # solution and the vessels it was touching jump with it.
            saved = (data.qpos.copy(), data.qvel.copy())
            station = rk.reach(model, data, above)
            q_above = data.qpos[rk.arm_qpos(model)].copy()
            if station is not None:
                rk.set_rail(model, data, station)
                solved = rk.solve_any(model, data, on)
                q_on = data.qpos[rk.arm_qpos(model)].copy()
            data.qpos[:], data.qvel[:] = saved
            mujoco.mj_forward(model, data)
            if station is None or not solved:
                continue

            tag = bottle.sample_id
            yield from drive(station, q_above, lambda *_: gt.OPEN, 4.0,
                             f'travelling to {tag}')
            yield from drive(station, q_on, lambda *_: gt.OPEN, 2.0,
                             f'reaching into the field for {tag}')
            yield from drive(station, q_on,
                             lambda i, n: gt.SHUT * min((i + 1) / (n * 0.5), 1.0),
                             1.5, f'closing on {tag}', stop_on_grip=True)
            settled = data.ctrl[grip_id]
            got = rk.read_grip(model, data).holding
            verb = 'lifting' if got else 'nothing to lift from'
            yield from drive(station, q_above, lambda *_, g=settled: g, 1.5,
                             f'{verb} {tag}')
            yield from drive(station, q_above, lambda *_, g=settled: g, 1.0,
                             f'holding {tag}' if got else f'missed {tag}')
            yield from drive(station, q_on, lambda *_, g=settled: g, 1.5,
                             f'putting {tag} back')
            yield from drive(station, q_on, lambda *_: gt.OPEN, 0.8,
                             f'releasing {tag}')
            yield from drive(station, q_above, lambda *_: gt.OPEN, 1.2,
                             f'clear of {tag}')


def pipette_programme(model: mujoco.MjModel, data: mujoco.MjData, count: int):
    """Draw from flask after flask and deliver into the beaker, with physics.

    A generator yielding a caption after every simulation step, so the caller
    can render between steps. Liquid only moves when the tip is genuinely down
    the bore and under the surface; a miss is reported, not fudged.

    Args:
        model: Compiled scene.
        data: Data to run in.
        count: Flasks to work through before looping.

    Yields:
        A short line describing what is happening.
    """
    ids = gt.actuators(model)
    home = model.body('rail_carriage').pos[0]
    per_second = round(1 / model.opt.timestep)

    def drive(station, pose, seconds, caption):
        start = np.array([data.ctrl[i] for i in ids])
        goal = np.concatenate([[station - home], pose])
        move = np.abs(goal - start)
        seconds = max(seconds, float(move[0]) / 0.6, float(move[1:].max()) / 0.9)
        total = max(int(seconds * per_second), 1)
        ramp = max(int(total * 0.7), 1)
        for step in range(total):
            alpha = 0.5 - 0.5 * np.cos(np.pi * min(step + 1, ramp) / ramp)
            for i, value in zip(ids, start + alpha * (goal - start)):
                data.ctrl[i] = value
            mujoco.mj_step(model, data)
            yield caption

    mujoco.mj_resetData(model, data)
    mujoco.mj_forward(model, data)
    vessels = pip.containers(model, data)
    beaker = vessels['beaker']
    tool = pip.Pipette()
    flasks = [v for k, v in sorted(vessels.items()) if k != 'beaker'][:count]
    pip.sync(model, vessels, tool)
    pip.show_mass(model, beaker.mass)

    while True:
        for flask in flasks:
            axis = data.body(flask.body).xpos
            over = np.array([float(axis[0]), float(axis[1]),
                             float(data.site(flask.mouth).xpos[2]) + pt.CLEARANCE])
            saved = (data.qpos.copy(), data.qvel.copy())
            station = rk.reach(model, data, over)
            q_over = data.qpos[rk.arm_qpos(model)].copy()
            q_down = solved = None
            if station is not None:
                rk.set_rail(model, data, station)
                down = over.copy()
                down[2] = pt.target_depth(flask, data)
                solved = rk.solve_any(model, data, down)
                q_down = data.qpos[rk.arm_qpos(model)].copy()
            data.qpos[:], data.qvel[:] = saved
            mujoco.mj_forward(model, data)
            if station is None or not solved:
                continue

            tag = flask.name
            yield from drive(station, q_over, 3.0, f'over {tag}')
            yield from drive(station, q_down, 2.0, f'entering {tag}')
            drew = pip.aspirate(model, data, flask, tool, 0.5)
            yield from drive(station, q_down, 0.8,
                             f'drawing from {tag}' if drew else f'missed {tag}')
            yield from drive(station, q_over, 1.5, f'withdrawing from {tag}')
            if not drew:
                continue

            mouth = data.site(beaker.mouth).xpos
            into = np.array([float(mouth[0]), float(mouth[1]),
                             float(mouth[2]) - 0.01])
            clear = into + np.array([0.0, 0.0, pt.CLEARANCE + 0.05])
            saved = (data.qpos.copy(), data.qvel.copy())
            station = rk.reach(model, data, clear)
            q_clear = data.qpos[rk.arm_qpos(model)].copy()
            q_into = None
            if station is not None:
                rk.set_rail(model, data, station)
                if rk.solve_any(model, data, into):
                    q_into = data.qpos[rk.arm_qpos(model)].copy()
            data.qpos[:], data.qvel[:] = saved
            mujoco.mj_forward(model, data)
            if station is None or q_into is None:
                continue
            # Over the beaker first, then down into it: going straight at it
            # sweeps the arm through the balance and knocks it off the pan.
            yield from drive(station, q_clear, 3.0, 'carrying to the beaker')
            yield from drive(station, q_into, 1.2, 'lowering into the beaker')
            pip.dispense(model, data, beaker, tool)
            pip.show_mass(model, beaker.mass)
            yield from drive(station, q_into, 1.0,
                             f'beaker now {beaker.volume:.2f} ml '
                             f'= {beaker.mass:.2f} g')
            yield from drive(station, q_clear, 1.2, 'clear of the beaker')


def telemetry(model: mujoco.MjModel, data: mujoco.MjData, caption: str,
              speed: float) -> dict[str, object]:
    """Everything worth putting on screen, read from the running simulation."""
    carriage = float(data.body('rail_carriage').xpos[0])
    tool = data.site(rk.TCP_SITE).xpos
    out = {
        'caption': caption,
        'sim_time': round(float(data.time), 2),
        'speed': round(speed, 2),
        'contacts': int(data.ncon),
        'carriage_x': round(carriage, 3),
        'tool': [round(float(v), 3) for v in tool],
    }
    if rk.TCP_SITE == 'arm_grip_pinch':
        grip = rk.read_grip(model, data)
        out |= {'pad_right': round(grip.right, 2),
                'pad_left': round(grip.left, 2),
                'finger_drive': round(grip.drive, 2),
                'closure': round(grip.closure, 3),
                'holding': grip.holding}
    else:
        vessels = pip.containers(model, data)
        beaker = vessels['beaker']
        out |= {'beaker_ml': round(beaker.volume, 2),
                'beaker_g': round(beaker.mass, 2),
                'on_bench_ml': round(sum(v.volume for k, v in vessels.items()
                                         if k != 'beaker'), 1),
                'tip_z': round(float(tool[2]), 3),
                'holding': False}
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',
                        choices=('pipette', 'pick', 'sweep', 'visit', 'label'),
                        default='pipette',
                        help='pipette draws from each open flask and delivers '
                             'into the beaker; pick grasps and lifts vessels '
                             'with the gripper fitted. Both step physics. The '
                             'others are kinematic playback.')
    parser.add_argument('--visits', type=int, default=6,
                        help='vessels to visit in visit and label modes')
    parser.add_argument('--speed', type=float, default=0.8,
                        help='carriage speed, m/s')
    parser.add_argument('--dwell', type=float, default=1.5,
                        help='seconds to hold on each target')
    parser.add_argument('--port', type=int, default=8008)
    parser.add_argument('--resolution', default='960x540',
                        help='streamed frame size')
    parser.add_argument('--quality', type=int, default=80,
                        help='JPEG quality of the stream')
    parser.add_argument('--overview', default='general',
                        help='scene camera for the second view: general, '
                             'carriage, or any camera in the scene')
    parser.add_argument('--no-browser', action='store_true',
                        help='do not open the tab automatically')
    args = parser.parse_args()

    width, height = (int(v) for v in args.resolution.split('x'))
    model, data = rk.load()
    programme = rows = owners = labels = None
    if args.mode == 'pipette':
        mujoco.mj_forward(model, data)
        vessels = pip.containers(model, data)
        programme = pipette_programme(model, data, args.visits)
        print(f'pipette: physics stepped at {model.opt.timestep * 1000:.0f} ms, '
              f'{len(vessels) - 1} open flasks holding '
              f'{sum(v.volume for k, v in vessels.items() if k != "beaker"):.1f} ml')
    elif args.mode == 'pick':
        mujoco.mj_forward(model, data)
        liftable = sum(1 for b in rk.bottles(model, data) if b.dynamic)
        programme = pick_programme(model, data, args.visits)
        print(f'pick: physics stepped at {model.opt.timestep * 1000:.0f} ms, '
              f'{liftable} liftable vessels, gripper closing on force feedback')
    else:
        points, labels = captions_for(args.mode, model, data, args.visits)
        rows, owners = rd.segmented(model, points, args.speed, args.dwell)
        print(f'{args.mode}: {len(rows)} frames, {len(rows) / rd.FPS:.1f} s, '
              f'carriage {rows[:, 0].min():.2f} .. {rows[:, 0].max():.2f} m')

    feed = Feed()
    server = serve(feed, args.port)
    url = f'http://localhost:{args.port}'
    print(f'overview and wrist camera streaming at {url}  '
          '(ctrl-c or close the window to stop)')
    if not args.no_browser:
        webbrowser.open(url)

    if programme is None:
        mujoco.mj_resetData(model, data)
    renderer = mujoco.Renderer(model, height=height, width=width)
    views = {'overview': args.overview, 'wrist': 'arm_eih'}
    steps_per_frame = max(round(1 / rd.FPS / model.opt.timestep), 1)
    try:
        with mujoco.viewer.launch_passive(model, data, show_left_ui=False,
                                          show_right_ui=False) as viewer:
            frame, clock = 0, time.time()
            while viewer.is_running():
                started = time.time()
                if programme is not None:
                    # One frame is several physics steps; the programme yields
                    # after each one.
                    caption = 'done'
                    for _ in range(steps_per_frame):
                        caption = next(programme)
                else:
                    row = rows[frame % len(rows)]
                    rd.apply(model, data, row, physics=False)
                    caption = labels[owners[frame % len(rows)]]
                frames = {}
                for label, camera in views.items():
                    renderer.update_scene(data, camera=camera)
                    buffer = io.BytesIO()
                    Image.fromarray(renderer.render()).save(
                        buffer, format='JPEG', quality=args.quality)
                    frames[label] = buffer.getvalue()
                now = time.time()
                speed = steps_per_frame * model.opt.timestep / max(now - clock, 1e-6)
                clock = now
                feed.publish(frames, telemetry(model, data, caption, speed))
                viewer.sync()
                frame += 1
                remaining = 1 / rd.FPS - (time.time() - started)
                if remaining > 0:
                    time.sleep(remaining)
    except KeyboardInterrupt:
        pass
    finally:
        renderer.close()
        server.shutdown()
        print('stopped')


if __name__ == '__main__':
    main()
