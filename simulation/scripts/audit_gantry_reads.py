#!/usr/bin/env python3
"""Save recorded hand-camera reads and score localization against simulator truth.

Ground truth is used only in this offline audit, never to choose scan targets.
"""
import argparse
import json
from pathlib import Path
import re
import sys

import cv2
import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'view/backend'))
import vision_pick as vp
from labvision.perception import refine_identity, refine_marker, refine_cap, ring_geometry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('recording', type=Path)
    args = parser.parse_args()
    folder = args.recording
    out = folder/'read-audit'
    out.mkdir(exist_ok=True)
    model = mujoco.MjModel.from_binary_path(str(folder/'scene.mjb'))
    data = mujoco.MjData(model)
    states = np.load(folder/'trajectory.npz')['qpos']
    captions = json.loads((folder/'captions.json').read_text())
    frames = {}
    for index, caption in enumerate(captions):
        match = re.search(r'(?:looking at|reading) track (\d+)', caption)
        if match:
            frames[int(match[1])] = index
    eyes = vp.Eyes(model, data)
    rows = vp.rows_by_marker(vp.registry.load_table(vp.DEFAULT_TABLE))
    reader = vp.MarkerReader()
    report = []
    try:
        for track, frame in frames.items():
            data.qpos[:] = states[frame]
            mujoco.mj_forward(model, data)
            image = eyes.frame('arm_eih')
            camera = eyes.camera('arm_eih')
            truth = vp.truth(model, data)
            observations = []
            for identity in vp.identify_frame(image, rows, reader=reader):
                if not identity.row or not identity.frontal:
                    continue
                vessel = identity.row['vessel_class']
                radius, height = ring_geometry(vessel)
                old = refine_marker(camera, identity.frontal.corners, radius, height)
                new = refine_identity(camera, identity, vessel)
                actual = next((p for name,p in truth.items() if name.endswith(identity.sample_id)), None)
                surface = ('cap' if any(refine_cap(camera, marker.corners, vessel) is not None
                                        for marker in identity.read) else 'ring')
                for marker in identity.read:
                    cv2.polylines(image, [marker.corners.astype(np.int32)], True, (0,255,0), 2)
                    cv2.putText(image, f'{identity.sample_id} [{surface}]', tuple(marker.corners[0].astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,255), 1)
                observations.append({'sample':identity.sample_id, 'surface':surface, 'ring_xy':old, 'corrected_xy':new,
                    'ring_error_mm': float(np.linalg.norm(np.array(old)-actual[:2])*1000) if old and actual is not None else None,
                    'corrected_error_mm': float(np.linalg.norm(np.array(new)-actual[:2])*1000) if new and actual is not None else None})
            cv2.imwrite(str(out/f'track-{track:03d}.png'),image)
            report.append({'track':track,'frame':frame,'observations':observations})
    finally:
        eyes.close()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    errors=[o for r in report for o in r['observations'] if o['corrected_error_mm'] is not None]
    print(json.dumps({'views':len(report),'observations':len(errors),
        'ring_median_mm':float(np.median([o['ring_error_mm'] for o in errors])),
        'corrected_median_mm':float(np.median([o['corrected_error_mm'] for o in errors])),
        'corrected_max_mm':max(o['corrected_error_mm'] for o in errors)},indent=2))


if __name__ == '__main__':
    main()
