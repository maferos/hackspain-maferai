#!/usr/bin/env python3
"""Record the viewer's scan and optional chat brief execution for offline RTX rendering."""
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
    parser.add_argument('--brief', help='Submit this chat brief and record the complete formula run')
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
        from gantry_motion import is_gantry
        if is_gantry(model):
            from gantry_scan import controller
        else:
            controller = vp.controller
        scan.controller = controller(model, data, scan.world, scan.perception, args.out / 'bench_map.json')
    workflow = executor = None
    if args.brief:
        import anthropic
        from catalogue import Catalogue, shelf_from_tracks
        from workflow import Workflow
        from scan_state import FetchExecutor
        env_path = REPO / 'view/backend/.env'
        for line in env_path.read_text().splitlines() if env_path.is_file() else []:
            key, sep, value = line.strip().partition('=')
            if sep and key and not key.startswith('#'):
                os.environ.setdefault(key.strip(), value.strip().strip("'\""))
        catalogue = Catalogue()
        workflow = Workflow(catalogue, lambda: shelf_from_tracks(scan.world.snapshot(), catalogue),
                            executor='fetch', order_file=args.out / 'formula_order.json',
                            scene_model=lambda: (model, data), scene_name=args.pattern,
                            scan_done=lambda: scan.world.scan is not None,
                            client=anthropic.Anthropic(timeout=90, max_retries=1))
        workflow.submit_brief(args.brief, 'chat')
    liquid_ids = np.asarray([i for i in range(model.ngeom)
                             if (mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, i) or '')
                             .endswith('_liquid')], dtype=int)
    states, captions, liquid_sizes, liquid_positions = [], [], [], []
    finished_at = None
    scan_saved = False
    started, last_log, next_sample = time.monotonic(), -1, 0.0
    try:
        while data.time < args.max_time:
            tick = time.monotonic()
            with physics:
                scan.advance(1 / 30)
                if data.time >= next_sample:
                    states.append(data.qpos.copy())
                    captions.append(scan.world.caption)
                    liquid_sizes.append(model.geom_size[liquid_ids].copy())
                    liquid_positions.append(model.geom_pos[liquid_ids].copy())
                    next_sample += 1 / args.fps
                status = scan.snapshot()
            if scan.error:
                raise RuntimeError(scan.error)
            if int(data.time) // 10 != last_log:
                last_log = int(data.time) // 10
                print(json.dumps(status), flush=True)
            if scan.world.scan:
                if not scan_saved:
                    (args.out / 'bench_map.json').write_text(json.dumps(scan.world.scan, indent=2)+'\n')
                    scan_saved = True
                if workflow is None:
                    break
                if executor is None:
                    order = workflow.pump()
                    if order.status == 'rejected':
                        raise RuntimeError(f'Chat brief rejected: {order.check}')
                    (args.out / 'composed.json').write_text(json.dumps(order.composed, indent=2)+'\n')
                    executor = FetchExecutor(workflow, scan.world)
                    executor.start()
                workflow.observe(scan.world.snapshot(), scan.world.caption or '', False)
                order = workflow.order
                if order.status not in ('queued', 'running') and not executor.thread.is_alive():
                    with scan.world.lock:
                        idle = not scan.world.commands and scan.world.caption.startswith('idle:')
                    if idle:
                        finished_at = finished_at or data.time
                        if data.time - finished_at >= 2:
                            break
            if time.monotonic() - started > args.max_time * 3 + 180:
                raise TimeoutError('Scan exceeded wall-clock limit')
            time.sleep(max(0.001, 1 / 30 - (time.monotonic() - tick)))
        else:
            raise TimeoutError('Scan did not complete before max-time')
        np.savez_compressed(args.out / 'trajectory.npz', qpos=np.asarray(states),
                            liquid_ids=liquid_ids, liquid_sizes=np.asarray(liquid_sizes),
                            liquid_positions=np.asarray(liquid_positions))
        (args.out / 'captions.json').write_text(json.dumps(captions)+'\n')
        metadata.update(mode='scan', fps=args.fps, frames=len(states),
                        duration_seconds=len(states)/args.fps, mujoco_version=mujoco.__version__,
                        detector=str(scan.weights), threshold=scan.conf, scan=status,
                        animation='Recorded view LiveScan controller and perception; offline RTX rendering')
        if workflow:
            metadata.update(mode='brief', brief=args.brief, order_status=workflow.order.status,
                            composed=workflow.order.composed)
        (args.out / 'recording.json').write_text(json.dumps(metadata, indent=2)+'\n')
        print('SCAN RECORDING COMPLETE', json.dumps(metadata), flush=True)
    finally:
        if executor:
            executor.stop()
        scan.close()


if __name__ == '__main__':
    main()
