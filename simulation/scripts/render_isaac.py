#!/usr/bin/env python3
"""Headless Isaac Sim render of a trivial scene -> RGB PNG.

De-risk: proves Isaac Sim boots headless on a RunPod GPU and writes a frame to
disk (no display, no WebRTC, no VNC) — the same rendering path Replicator uses
for synthetic-data generation.

Run with Isaac's bundled python inside the container:
    OUT_DIR=/root/out /isaac-sim/python.sh render_isaac.py
"""
import os

OUT = os.environ.get("OUT_DIR", "/root/out")
os.makedirs(OUT, exist_ok=True)

from isaacsim import SimulationApp
sim_app = SimulationApp({"headless": True})

import omni.replicator.core as rep

# fast real-time RTX rasterizer (don't wait for path-tracing to converge)
try:
    rep.settings.set_render_rtx_realtime()
except Exception as e:
    print("warn: set_render_rtx_realtime failed:", e)

# --- trivial scene: ground plane + primitives + a distant light ---
rep.create.plane(scale=10, visible=True)
rep.create.cube(position=(0.0, 0.0, 0.5))
rep.create.sphere(position=(2.0, 0.5, 0.75), scale=0.75)
rep.create.light(light_type="distant", intensity=3000, rotation=(-45, 45, 0))

cam = rep.create.camera(position=(6.0, 6.0, 4.0), look_at=(0.0, 0.0, 0.5))
rp = rep.create.render_product(cam, (1280, 720))

writer = rep.WriterRegistry.get("BasicWriter")
writer.initialize(output_dir=OUT, rgb=True)
writer.attach([rp])

# render a few frames so first-frame warmup settles, then stop
rep.orchestrator.run_until_complete(num_frames=3)

print("DONE -> RGB written under", OUT)
sim_app.close()
