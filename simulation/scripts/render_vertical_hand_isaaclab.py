#!/usr/bin/env python3
"""Render the baked vertical-hand USD sequence with Isaac Lab and RTX.

Pass --export with vertical_hand.usdc, --out, --quality final,
--subframes 2, --light-multiplier 1, --headless and --enable_cameras.
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
parser.add_argument('--camera', choices=('overview', 'underside'), default='overview')
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
from pxr import Usd, UsdLux, UsdGeom, Gf



def main():
    args.out.mkdir(parents=True, exist_ok=True)
    metadata_path = args.export / 'animation.json'
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text())
    else:
        source = Usd.Stage.Open(str(args.export / 'vertical_hand.usdc'))
        fps = source.GetTimeCodesPerSecond()
        count = int(source.GetEndTimeCode() - source.GetStartTimeCode() + 1)
        if source.GetStartTimeCode() != 1:
            raise ValueError('The vertical-hand animation must start at USD frame 1')
        metadata = dict(frames=count, fps=fps, duration_seconds=count / fps,
                        usd='vertical_hand.usdc', animation='Vertical hand 23-step sequence')
        del source
    if args.start_frame >= metadata['frames']:
        raise ValueError('Start frame must precede the end of the animation')
    ctx = omni.usd.get_context()
    ctx.open_stage(str((args.export/metadata['usd']).resolve()))
    while ctx.get_stage_loading_status()[2] > 0:
        app.update()
    stage = ctx.get_stage()

    for prim in stage.Traverse():
        if prim.IsA(UsdLux.BoundableLightBase) or prim.IsA(UsdLux.NonboundableLightBase):
            intensity = UsdLux.LightAPI(prim).GetIntensityAttr()
            intensity.Set(float(intensity.Get() or 1) * args.light_multiplier)
    # Presentation camera and lighting; keep the source animation untouched.
    camera = UsdGeom.Camera.Define(stage, '/RenderCamera')
    camera.GetFocalLengthAttr().Set(32.0)
    camera.GetHorizontalApertureAttr().Set(36.0)
    camera.GetVerticalApertureAttr().Set(20.25)
    camera.GetClippingRangeAttr().Set(Gf.Vec2f(0.01, 100.0))
    eye, target = (Gf.Vec3d(1.25,-0.38,0.65), Gf.Vec3d(-0.09,0,0.31))
    if args.camera == 'underside':
        eye, target = Gf.Vec3d(0.45,-0.1,0.02), Gf.Vec3d(-0.04,0,0.23)
    camera.AddTransformOp().Set(Gf.Matrix4d().SetLookAt(eye, target, Gf.Vec3d(0,0,1)).GetInverse())
    for prim in stage.Traverse():
        if prim.IsA(UsdLux.DomeLight):
            dome = UsdLux.DomeLight(prim)
            dome.GetTextureFileAttr().Clear()
            dome.GetIntensityAttr().Set(500.0)
        elif prim.IsA(UsdLux.DistantLight):
            light = UsdLux.DistantLight(prim)
            light.GetIntensityAttr().Set(1800.0)
            light.GetAngleAttr().Set(8.0)
    if args.camera == 'underside':
        fill = UsdLux.RectLight.Define(stage, '/UndersideFill')
        fill.GetWidthAttr().Set(0.5)
        fill.GetHeightAttr().Set(0.5)
        fill.GetIntensityAttr().Set(2500.0)
        UsdGeom.Xformable(fill).AddTransformOp().Set(
            Gf.Matrix4d().SetLookAt(eye, target, Gf.Vec3d(0,0,1)).GetInverse())
    floor = UsdGeom.Cube.Define(stage, '/StudioFloor')
    floor.GetSizeAttr().Set(1.0)
    floor.AddTranslateOp().Set(Gf.Vec3d(0,0,-0.011))
    floor.AddScaleOp().Set(Gf.Vec3d(200,200,0.02))
    floor.GetDisplayColorAttr().Set([Gf.Vec3f(0.26,0.28,0.32)])
    rep.settings.set_render_rtx_realtime(antialiasing="DLSS")
    timeline = omni.timeline.get_timeline_interface()
    fps = metadata['fps']
    count = min(args.limit or metadata['frames'], metadata['frames'] - args.start_frame)
    cameras = [(args.camera, 'camera')]
    products, annotators, encoders, logs = [], [], [], []
    try:
        for label, name in cameras:
            path = '/RenderCamera'
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
                str(args.out/('vertical_hand.mp4' if args.camera == 'overview' else 'vertical_hand_underside.mp4'))], stdin=subprocess.PIPE, stderr=log))
        # This is USD animation playback, not a Replicator simulation. Drive
        # Kit rendering directly so paused time does not depend on Replicator's
        # physics-time capture scheduler (which changed in Isaac Sim 6.1).
        timeline.pause()
        timeline.set_current_time((args.start_frame + 1) / fps)
        for warmup in range(20):
            app.update()
            if warmup % 5 == 0:
                print(f'WARMUP {warmup+1}/20', flush=True)
        started = time.time()
        for frame in range(count):
            timeline.set_current_time((args.start_frame + frame + 1) / fps)
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
            asset='vertical_hand.usdc', source_commit='7bff5de', animation_start_frame=1, camera=args.camera), indent=2)+'\n')
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
