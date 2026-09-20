#!/usr/bin/env python3
"""Record the viewer's actual vision-driven initial scan for offline RTX rendering."""
import argparse
import json
import os
from pathlib import Path
import sys
import threading
import time

import mujoco
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(REPO / 'view/backend'), str(REPO / 'computer-vision')]
from live_scan import LiveScan, scan_scene, vp
from scene_patterns import build_pattern
from labvision.detector import resolve


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pattern', default='p01')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--fps', type=int, default=10, choices=(10, 15, 30))
    parser.add_argument('--max-time', type=float, default=600)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    # Match the viewer's detector defaults without importing its HTTP server.
    if not os.environ.get('VIEW_DETECTOR'):
        try:
            resolve('full')
            os.environ['VIEW_DETECTOR'] = 'full'
            os.environ.setdefault('VIEW_DETECTOR_CONF', '0.41')
        except FileNotFoundError:
            pass
    model, metadata = build_pattern(scan_scene(), args.pattern)
    data = mujoco.MjData(model)
    vp.rk.rest(model, data)
    mujoco.mj_forward(model, data)
    mujoco.mj_saveModel(model, str(args.out / 'scene.mjb'))
    physics = threading.Lock()
    scan = LiveScan(model, data, physics, 0)
    if scan.controller is not None:
        scan.controller.close()
        scan.controller = vp.controller(model, data, scan.world, scan.perception, args.out / 'bench_map.json')
    states, captions = [], []
    started, last_log, next_sample = time.monotonic(), -1, 0.0
    try:
        while data.time < args.max_time:
            tick = time.monotonic()
            with physics:
                scan.advance(1 / 30)
                if data.time >= next_sample:
                    states.append(data.qpos.copy())
                    captions.append(scan.world.caption)
                    next_sample += 1 / args.fps
                status = scan.snapshot()
            if scan.error:
                raise RuntimeError(scan.error)
            if int(data.time) // 10 != last_log:
                last_log = int(data.time) // 10
                print(json.dumps(status), flush=True)
            if scan.world.scan:
                (args.out / 'bench_map.json').write_text(json.dumps(scan.world.scan, indent=2)+'\n')
                break
            if time.monotonic() - started > args.max_time * 3 + 180:
                raise TimeoutError('Scan exceeded wall-clock limit')
            time.sleep(max(0.001, 1 / 30 - (time.monotonic() - tick)))
        else:
            raise TimeoutError('Scan did not complete before max-time')
        np.savez_compressed(args.out / 'trajectory.npz', qpos=np.asarray(states))
        (args.out / 'captions.json').write_text(json.dumps(captions)+'\n')
        metadata.update(mode='scan', fps=args.fps, frames=len(states),
                        duration_seconds=len(states)/args.fps, mujoco_version=mujoco.__version__,
                        detector=str(scan.weights), threshold=scan.conf, scan=status,
                        animation='Recorded view LiveScan controller and perception; offline RTX rendering')
        (args.out / 'recording.json').write_text(json.dumps(metadata, indent=2)+'\n')
        print('SCAN RECORDING COMPLETE', json.dumps(metadata), flush=True)
    finally:
        scan.close()


if __name__ == '__main__':
    main()
