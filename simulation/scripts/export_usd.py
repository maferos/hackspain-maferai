#!/usr/bin/env python3
"""Export a MuJoCo scene to USD with MuJoCo's native USD exporter.

Runs on plain python (mujoco + pxr[usd-core] + pillow), NO Isaac needed. MuJoCo
loads the full scene (all <include>s resolved, 319 meshes) and writes a USD
package that Isaac can then render.

    python3 export_usd.py /root/scene/models/minihannover_scene.xml /root/out
"""
import sys, re, mujoco
from mujoco.usd import exporter as usd_exporter

# MuJoCo names can contain characters USD rejects in prim paths (e.g. '-' in
# asset names like gc-ms / uv-vs-nr), which makes Xform.Define fail with an empty
# path. Sanitise every generated name to [A-Za-z0-9_].
def _sanitise(cls, *methods):
    for m in methods:
        orig = getattr(cls, m, None)
        if orig:
            setattr(cls, m, (lambda o: (lambda self, x: re.sub(r"[^A-Za-z0-9_]", "_", o(self, x))))(orig))
_sanitise(usd_exporter.USDExporter, "_get_geom_name")

scene = sys.argv[1] if len(sys.argv) > 1 else "/root/scene/models/minihannover_scene.xml"
outroot = sys.argv[2] if len(sys.argv) > 2 else "/root/out"

m = mujoco.MjModel.from_xml_path(scene)
d = mujoco.MjData(m)
mujoco.mj_forward(m, d)

cam_names = [mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_CAMERA, i) for i in range(m.ncam)]
print("scene:", scene, "| bodies", m.nbody, "geoms", m.ngeom, "meshes", m.nmesh)
print("cameras:", cam_names, flush=True)

exp = usd_exporter.USDExporter(
    model=m,
    max_geom=20000,
    output_directory="lab_usd",
    output_directory_root=outroot,
    light_intensity=6000,
    camera_names=cam_names,
    verbose=False,
)
exp.update_scene(data=d)
exp.save_scene(filetype="usdc")
print("SAVED USD package under", outroot + "/lab_usd", flush=True)
