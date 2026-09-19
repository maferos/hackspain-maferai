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
  main { flex: 1; display: grid; place-items: center; padding: 18px; }
  img { max-width: 100%; max-height: 78vh; border-radius: 6px;
        border: 1px solid #2a2e35; background: #000; }
  #caption { font-variant-numeric: tabular-nums; color: #e8e6e1; }
</style></head>
<body>
  <header>
    <h1>Eye-in-hand camera &middot; UR10e wrist</h1>
    <p><span id="caption">&hellip;</span></p>
  </header>
  <main><img src="/stream.mjpg" alt="wrist camera"></main>
  <script>
    setInterval(async () => {
      try {
        document.getElementById('caption').textContent =
          await (await fetch('/caption')).text();
      } catch (e) { /* the run ended; keep the last frame on screen */ }
    }, 250);
  </script>
</body></html>
"""


class Feed:
    """The latest wrist frame, handed from the simulation loop to the server."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._jpeg: bytes | None = None
        self._caption = 'starting'
        self._tick = 0

    def publish(self, jpeg: bytes, caption: str) -> None:
        """Replace the current frame."""
        with self._lock:
            self._jpeg, self._caption, self._tick = jpeg, caption, self._tick + 1

    def latest(self) -> tuple[bytes | None, int]:
        """The current frame and a counter that changes when it does."""
        with self._lock:
            return self._jpeg, self._tick

    @property
    def caption(self) -> str:
        """What the camera is looking at."""
        with self._lock:
            return self._caption


class Handler(http.server.BaseHTTPRequestHandler):
    """Serves the page, the MJPEG stream and the caption."""

    feed: Feed

    def do_GET(self) -> None:
        if self.path.startswith('/stream'):
            self._stream()
        elif self.path.startswith('/caption'):
            self._send(self.feed.caption.encode(), 'text/plain; charset=utf-8')
        else:
            self._send(PAGE.encode(), 'text/html; charset=utf-8')

    def _send(self, body: bytes, content_type: str) -> None:
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _stream(self) -> None:
        self.send_response(200)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Type',
                         'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()
        seen = -1
        try:
            while True:
                jpeg, tick = self.feed.latest()
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('sweep', 'visit', 'label'),
                        default='sweep')
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
    parser.add_argument('--no-browser', action='store_true',
                        help='do not open the tab automatically')
    args = parser.parse_args()

    width, height = (int(v) for v in args.resolution.split('x'))
    model, data = rk.load()
    points, labels = captions_for(args.mode, model, data, args.visits)
    rows, owners = rd.segmented(model, points, args.speed, args.dwell)
    print(f'{args.mode}: {len(rows)} frames, {len(rows) / rd.FPS:.1f} s, '
          f'carriage {rows[:, 0].min():.2f} .. {rows[:, 0].max():.2f} m')

    feed = Feed()
    server = serve(feed, args.port)
    url = f'http://localhost:{args.port}'
    print(f'wrist camera streaming at {url}  (ctrl-c or close the window to stop)')
    if not args.no_browser:
        webbrowser.open(url)

    mujoco.mj_resetData(model, data)
    renderer = mujoco.Renderer(model, height=height, width=width)
    try:
        with mujoco.viewer.launch_passive(model, data, show_left_ui=False,
                                          show_right_ui=False) as viewer:
            frame = 0
            while viewer.is_running():
                started = time.time()
                row = rows[frame % len(rows)]
                rd.apply(model, data, row, physics=False)
                renderer.update_scene(data, camera='arm_eih')
                buffer = io.BytesIO()
                Image.fromarray(renderer.render()).save(
                    buffer, format='JPEG', quality=args.quality)
                feed.publish(buffer.getvalue(), labels[owners[frame % len(rows)]])
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
