#!/usr/bin/env python3
"""Render both cameras of a baked rail USD animation with Isaac Lab and RTX.

Run with the Isaac Lab Python environment, --headless --enable_cameras.
The two MP4s always receive the same animation time and frame count.
"""
import argparse
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import time

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--export', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
parser.add_argument('--limit', type=int, default=0)
parser.add_argument('--start-frame', type=int, default=0)
parser.add_argument('--light-multiplier', type=float, default=20)
parser.add_argument('--subframes', type=int, default=None)
parser.add_argument('--quality', choices=('draft', 'final'), default='final')
AppLauncher.add_app_launcher_args(parser)
# Isaac Lab 3 enables rendering by default and no longer registers these
# legacy CLI flags, but AppLauncher still accepts the corresponding settings.
for flag in ('--headless', '--enable_cameras'):
    if flag not in parser._option_string_actions:
        parser.add_argument(flag, action='store_true')
args = parser.parse_args()
if args.subframes is None:
    args.subframes = 1 if args.quality == 'draft' else 4
width, height = (960, 540) if args.quality == 'draft' else (1920, 1080)
if args.limit < 0 or args.start_frame < 0 or args.subframes < 0:
    parser.error('Frame counts and start frame must be nonnegative')
launcher = AppLauncher(args)
app = launcher.app

import numpy as np
import omni.replicator.core as rep
import omni.timeline
import omni.usd
from PIL import Image
from pxr import UsdLux
from rail_usd_table import prepare_table


def main():
    args.out.mkdir(parents=True, exist_ok=True)
    metadata = json.loads((args.export/'animation.json').read_text())
    if args.start_frame >= metadata['frames']:
        raise ValueError('Start frame must precede the end of the animation')
    ctx = omni.usd.get_context()
    ctx.open_stage(str((args.export/metadata['usd']).resolve()))
    while ctx.get_stage_loading_status()[2] > 0:
        app.update()
    stage = ctx.get_stage()
    prepare_table(stage)
    for prim in stage.Traverse():
        if prim.IsA(UsdLux.BoundableLightBase) or prim.IsA(UsdLux.NonboundableLightBase):
            intensity = UsdLux.LightAPI(prim).GetIntensityAttr()
            intensity.Set(float(intensity.Get() or 1) * args.light_multiplier)
    rep.settings.set_render_rtx_realtime(antialiasing="DLSS")
    timeline = omni.timeline.get_timeline_interface()
    fps = metadata['fps']
    count = min(args.limit or metadata['frames'], metadata['frames'] - args.start_frame)
    cameras = [('global', 'general'), ('robot', 'arm_eih')]
    products, annotators, encoders, logs = [], [], [], []
    try:
        for label, name in cameras:
            path = f'/World/Camera_Xform_{name}/Camera_{name}'
            if not stage.GetPrimAtPath(path).IsValid():
                raise RuntimeError(f'Missing camera: {path}')
            product = rep.create.render_product(path, (width, height))
            annotator = rep.AnnotatorRegistry.get_annotator('rgb')
            annotator.attach([product])
            products.append(product)
            annotators.append(annotator)
            log = (args.out/f'{label}-ffmpeg.log').open('wb')
            logs.append(log)
            encoders.append(subprocess.Popen([
                '/usr/bin/ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo',
                '-pix_fmt', 'rgb24', '-s', f'{width}x{height}', '-r', str(fps), '-i', '-',
                '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
                '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                str(args.out/f'rail_{label}.mp4')], stdin=subprocess.PIPE, stderr=log))
        # This is USD animation playback, not a Replicator simulation. Drive
        # Kit rendering directly so paused time does not depend on Replicator's
        # physics-time capture scheduler (which changed in Isaac Sim 6.1).
        timeline.pause()
        timeline.set_current_time(args.start_frame / fps)
        for warmup in range(20):
            app.update()
            if warmup % 5 == 0:
                print(f'WARMUP {warmup+1}/20', flush=True)
        started = time.time()
        for frame in range(count):
            timeline.set_current_time((args.start_frame + frame) / fps)
            for _ in range(args.subframes + 1):
                app.update()
            for (label, _), annotator, encoder in zip(cameras, annotators, encoders):
                rgb = np.ascontiguousarray(annotator.get_data()[..., :3])
                if rgb.shape != (height, width, 3) or rgb.dtype != np.uint8:
                    raise RuntimeError(f'Invalid {label} frame: {rgb.shape}, {rgb.dtype}')
                encoder.stdin.write(rgb.tobytes())
                if frame in {0, count//2, count-1}:
                    Image.fromarray(rgb).save(args.out/f'{label}_{frame:05d}.png')
            if frame % 30 == 0:
                print(f'RENDER {frame+1}/{count}; elapsed {time.time()-started:.1f}s', flush=True)
        for encoder in encoders:
            encoder.stdin.close()
            if encoder.wait() != 0:
                raise RuntimeError('Video encoding failed; see ffmpeg log')
        (args.out/'render.json').write_text(json.dumps(dict(
            **metadata, rendered_frames=count, resolution=[width, height], quality=args.quality,
            renderer=f'Isaac Lab / Isaac Sim {version("isaacsim")} RTX Real-Time',
            isaaclab_package_version=version('isaaclab'),
            light_multiplier=args.light_multiplier, subframes=args.subframes,
            antialiasing='DLSS', start_frame=args.start_frame,
            table_object='/World/Table', table_material='white satin, metallic 0, roughness 0.45'), indent=2)+'\n')
        print('RENDER COMPLETE', flush=True)
    finally:
        for encoder in encoders:
            if encoder.poll() is None:
                if not encoder.stdin.closed:
                    encoder.stdin.close()
                encoder.wait()
        for log in logs:
            log.close()
        for annotator in annotators:
            annotator.detach()
        for product in products:
            product.destroy()


try:
    main()
finally:
    app.close()
