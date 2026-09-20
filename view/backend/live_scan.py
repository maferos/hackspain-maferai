"""Adapt Martí's vision controller to the viewer's model and camera streams.

No additional HTTP server or dashboard: perception reads a copy of the viewport
state and the original controller drives its physics. The lab panels retain
their independent state publisher.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'simulation/scripts'))
import vision_pick as vp
from detector_config import DETECTOR_WEIGHTS, DETECTOR_CONF


def scan_scene():
    if os.environ.get('VIEW_MACHINE', 'gantry') == 'gantry':
        from generate_gantry_scene import build_scene
        return build_scene()
    return vp.gripper_scene()


class ScanDetector:
    def __init__(self, weights, threshold):
        self.inference_ms = 0
        self.worker = subprocess.Popen(
            [sys.executable, str(Path(__file__).with_name('scan_detector_worker.py')),
             str(weights), str(threshold)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        )

    def detect(self, frame):
        self.worker.stdin.write((json.dumps(frame.shape) + '\n').encode())
        self.worker.stdin.write(memoryview(frame).cast('B'))
        self.worker.stdin.flush()
        line = self.worker.stdout.readline()
        if not line:
            raise RuntimeError('Scan detector stopped; check the backend log')
        result = json.loads(line)
        if 'error' in result:
            raise RuntimeError(result['error'])
        self.inference_ms = result['inference_ms']
        return [(vp.BBox(*row[:4]), row[4], row[5]) for row in result['boxes']]

    def close(self):
        if self.worker.poll() is None:
            self.worker.terminate()
            try:
                self.worker.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.worker.kill()
                self.worker.wait()
        self.worker.stdin.close()
        self.worker.stdout.close()


class ScanPerception(vp.Perception):
    error = None

    def run(self):
        try:
            super().run()
        except (Exception, SystemExit) as exc:
            self.error = str(exc)
            self.ready.set()
            self.finished.set()


class LiveScan:
    def __init__(self, model, data, physics, generation):
        self.model, self.data = model, data
        self.world = vp.World(auto=False)
        self.error = None
        self.detector = self.perception = self.controller = None
        self.started = time.monotonic()
        self.generation = generation
        self.weights, self.conf = DETECTOR_WEIGHTS, DETECTOR_CONF
        try:
            if not self.weights.is_file():
                raise FileNotFoundError(f'Missing detector weights: {self.weights}')
            # rk.load normally names the tool; the viewer compiles seed models
            # itself, so it asks the model which tool is on rather than assuming
            # one. After the weights: a missing file is the cheaper question and
            # the one worth reporting first.
            model.site(vp.rk.pick_tcp(model))
            self.detector = ScanDetector(self.weights, self.conf)
            self.perception = ScanPerception(model, data, physics, self.world,
                                             self.detector, vp.Show(), None)
            from gantry_motion import is_gantry
            if is_gantry(model):
                from gantry_scan import controller
                self.world.scene = 'simulation/models/minihannover_gantry_scene.xml'
            else:
                controller = vp.controller
            self.controller = controller(
                model, data, self.world, self.perception,
                REPO / 'simulation/out/view_bench_map.json',
            )
            self.perception.start()
        except (Exception, SystemExit) as exc:
            self.error = f'Cannot start scan: {exc}'
            if self.detector:
                self.detector.close()
                self.detector = None

    def advance(self, seconds):
        """Called by the renderer while holding the shared physics lock."""
        if self.error or self.perception is None:
            return
        if self.perception.finished.is_set():
            self.error = self.perception.error or 'Scan perception stopped'
            return
        if not self.perception.ready.is_set() or self.world.cycles == 0:
            if time.monotonic() - self.started > 180:
                self.error = 'Scan perception did not produce a frame within 180 seconds'
            return
        try:
            for _ in range(max(1, round(seconds / self.model.opt.timestep))):
                self.world.caption = next(self.controller)
        except (Exception, SystemExit) as exc:
            self.error = f'Scan controller failed: {exc}'

    def snapshot(self):
        tracks = self.world.snapshot()
        named = sum(bool(t.sample) for t in tracks if t.state != 'lost')
        return {
            'status': 'error' if self.error else 'complete' if self.world.scan else
                      'scanning' if self.world.cycles else 'starting',
            'error': self.error,
            'caption': self.world.caption,
            'named': named,
            'tracked': sum(t.state not in ('lost', 'tentative', 'empty') for t in tracks),
            'seconds': round(float(self.data.time), 1),
            'generation': self.generation,
            'events': self.world.events[-5:],
        }

    def detections(self):
        boxes, labels = [], []
        camera = vp.Eyes(self.model, self.data).camera('general')
        for track in self.world.snapshot():
            if track.state in ('lost', 'tentative', 'empty'):
                continue
            if track.bbox is not None:
                box = track.bbox.as_tuple()
            else:
                foot = np.array([*track.xy, vp.rk.BENCH_TOP])
                points = camera.project(np.array([foot, foot + (0, 0, vp.FLASK_HEIGHT)]))
                if not np.all(np.isfinite(points)):
                    continue
                (u, v0), (_, v1) = points
                half = 0.25 * abs(v0 - v1)
                box = (u - half, v1, u + half, v0)
            boxes.append([*box, track.score])
            labels.append(track.sample or f'#{track.id}')
        return {
            'generation': self.generation, 'camera': 'scene',
            'frame': self.world.cycles, 'width': 1920, 'height': 1080,
            'boxes': boxes, 'labels': labels,
            'inference_ms': self.detector.inference_ms if self.detector else 0,
        }

    def close(self):
        # The renderer calls this outside the physics lock. Unblock any pending
        # inference before joining, so a layout cannot retain an old worker.
        if self.perception:
            self.perception.stop.set()
        if self.detector:
            self.detector.close()
        if self.perception and self.perception.ident is not None:
            self.perception.join(timeout=30)
            if self.perception.is_alive():
                raise RuntimeError('Previous scan perception did not stop')
        if self.controller:
            self.controller.close()
