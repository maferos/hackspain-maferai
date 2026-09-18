#!/usr/bin/env python3
"""Offscreen EGL render of AutoBio lab scenes to PNG.

Loads AutoBio's prebuilt plugin first, so it needs mujoco==3.3.0 and the
`libmjlab.so.3.3.0` + `model/` + `assets/` tree alongside this script (see
`simulation/runpod-render.md`). Headless: set MUJOCO_GL=egl on a GPU box.

    MUJOCO_GL=egl python3 render_autobio.py lab mani_thermal_cycler pickup
"""
import os
import sys

os.environ.setdefault("MUJOCO_GL", "egl")
import mujoco
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.join(BASE, f"libmjlab.so.{mujoco.__version__}")
SCENES = os.path.join(BASE, "model", "scene")
W, H = 1280, 720

print("mujoco", mujoco.__version__, "MUJOCO_GL", os.environ.get("MUJOCO_GL"))
if not os.path.exists(PLUGIN):
    sys.exit(f"plugin not found: {PLUGIN} (need mujoco==3.3.0)")
mujoco.mj_loadPluginLibrary(PLUGIN)

for name in sys.argv[1:] or ["pickup"]:
    path = os.path.join(SCENES, f"{name}.xml")
    try:
        model = mujoco.MjModel.from_xml_path(path)
    except Exception as exc:
        print(f"FAIL load   {name}: {str(exc).splitlines()[0]}")
        continue
    model.vis.global_.offwidth, model.vis.global_.offheight = W, H
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)                 # authored pose, no settling
    cam = 0 if model.ncam > 0 else -1              # an authored camera if present
    try:
        with mujoco.Renderer(model, height=H, width=W) as renderer:
            renderer.update_scene(data, camera=cam)
            Image.fromarray(renderer.render()).save(os.path.join(BASE, f"{name}.png"))
        print(f"OK   {name}  bodies={model.nbody} cams={model.ncam}")
    except Exception as exc:
        print(f"FAIL render {name}: {str(exc).splitlines()[0]}")
