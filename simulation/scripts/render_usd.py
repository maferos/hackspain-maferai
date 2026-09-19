#!/usr/bin/env python3
"""Render a USD scene headless with Isaac Sim + Replicator.

    OUT_DIR=/root/out/lab_isaac /isaac-sim/python.sh render_usd.py /root/out/lab.usd [cam1 cam2 ...]

- Opens the (imported) stage, adds a dome light if it has none (so an imported
  MJCF scene isn't pitch black), and renders RGB from each camera prim found
  (or the camera paths passed on the CLI). Falls back to a default camera.
"""
import os, sys
from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
import omni.replicator.core as rep
from pxr import Usd, UsdGeom, UsdLux, Gf, Sdf

usd_path = sys.argv[1] if len(sys.argv) > 1 else "/root/out/lab.usd"
cli_cams = sys.argv[2:]
OUT = os.environ.get("OUT_DIR", "/root/out/lab_isaac")
os.makedirs(OUT, exist_ok=True)
W = int(os.environ.get("W", 1600)); H = int(os.environ.get("H", 900))

ctx = omni.usd.get_context()
ctx.open_stage(usd_path)
stage = ctx.get_stage()
print("opened", usd_path, "up-axis", UsdGeom.GetStageUpAxis(stage), flush=True)

try:
    rep.settings.set_render_rtx_realtime()
except Exception as e:
    print("rtx realtime warn:", e)

cams = [str(p.GetPath()) for p in stage.Traverse() if p.GetTypeName() == "Camera"]
lights = [str(p.GetPath()) for p in stage.Traverse() if "Light" in p.GetTypeName()]
print("cameras:", cams, flush=True)
print("lights:", lights, flush=True)

# The scene is a CLOSED room, so a DomeLight (sky) can't get in — the interior
# ceiling lights are what matter, and MuJoCo exports them far too dim for RTX.
# Boost every existing light's intensity. Tune with LIGHTMUL.
mul = float(os.environ.get("LIGHTMUL", "40"))
boosted = 0
for lp in lights:
    la = UsdLux.LightAPI(stage.GetPrimAtPath(lp))
    a = la.GetIntensityAttr()
    cur = a.Get()
    a.Set((1.0 if cur is None else float(cur)) * mul)
    boosted += 1
print(f"boosted {boosted} interior lights x{mul}", flush=True)
if not lights:
    dome = UsdLux.DomeLight.Define(stage, Sdf.Path("/World/FillDome"))
    dome.CreateIntensityAttr(1500.0)

targets = cli_cams or cams
if not targets:
    cam = UsdGeom.Camera.Define(stage, Sdf.Path("/World/RenderCam"))
    xf = UsdGeom.Xformable(cam.GetPrim())
    xf.AddTranslateOp().Set(Gf.Vec3d(-8.0, -1.7, 1.65))
    xf.AddRotateXYZOp().Set(Gf.Vec3f(75, 0, -70))
    targets = ["/World/RenderCam"]
    print("no cameras found; created /World/RenderCam", flush=True)

for campath in targets:
    name = campath.rstrip("/").split("/")[-1]
    rp = rep.create.render_product(campath, (W, H))
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(output_dir=os.path.join(OUT, name), rgb=True)
    writer.attach([rp])
    rep.orchestrator.run_until_complete(num_frames=2)
    writer.detach()
    rp.destroy()
    print("rendered", campath, "->", os.path.join(OUT, name), flush=True)

print("DONE", flush=True)
app.close()
