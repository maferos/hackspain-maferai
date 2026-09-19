#!/usr/bin/env python3
"""Pass 1 - introspect candidate robot arms on the lab bench and render the
default pose. Prints each arm's joints / link tree / DOF so pass 2 can set
correct down-looking poses and parent an eye-in-hand camera to the hand link.

    /isaac-sim/python.sh arm_introspect.py

Renders to /root/arm_probe/<arm>/{general,topdown}. Cheap validation of:
referencing the cloud USD, placement on the bench, and articulation names.
"""
import os
from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
import omni.replicator.core as rep
from pxr import Usd, UsdGeom, UsdLux, UsdPhysics, Gf, Sdf

LAB = "/root/lab_usd/lab_usd.usdc"  # fixed up below if the package name differs
OUT = "/root/arm_probe"
W, H = 1600, 900
os.makedirs(OUT, exist_ok=True)

# --- resolve the Omniverse assets root (function name moved across versions) ---
def assets_root():
    for mod, fn in [
        ("isaacsim.storage.native", "get_assets_root_path"),
        ("isaacsim.core.utils.nucleus", "get_assets_root_path"),
        ("omni.isaac.nucleus", "get_assets_root_path"),
        ("omni.isaac.core.utils.nucleus", "get_assets_root_path"),
    ]:
        try:
            m = __import__(mod, fromlist=[fn])
            r = getattr(m, fn)()
            if r:
                print("assets root via", mod, "->", r, flush=True)
                return r
        except Exception as e:
            print("  (no)", mod, e)
    raise RuntimeError("no assets root")

ROOT = assets_root()
ISAAC = f"{ROOT}/Isaac"
ISAACLAB = f"{ISAAC}/IsaacLab"

ARMS = {
    "franka":     f"{ISAACLAB}/Robots/FrankaEmika/panda_instanceable.usd",
    "ur10e":      f"{ISAAC}/Robots/UniversalRobots/ur10e/ur10e.usd",
    "kinova_gen3": f"{ISAAC}/Robots/Kinova/Gen3/gen3n7_instanceable.usd",
}

# base placement on the bench (bench top ~z=0.9); a clear-ish central spot
BASE_POS = Gf.Vec3d(-2.0, -0.55, 0.9)

# locate the actual lab usd file inside the package dir (mujoco exporter puts
# the stage under frames/frame_*.usdc)
import glob
cands = [c for c in sorted(glob.glob("/root/lab_usd/**/*.usd*", recursive=True))
         if not os.path.basename(c).startswith("._")]  # skip macOS AppleDouble
LAB = next((c for c in cands if "frame" in c and c.endswith((".usdc", ".usd", ".usda"))),
           cands[0] if cands else LAB)
print("LAB stage:", LAB, "| candidates:", cands, flush=True)

ctx = omni.usd.get_context()

def boost_lights(stage, mul=40.0):
    n = 0
    for p in stage.Traverse():
        if "Light" in p.GetTypeName():
            la = UsdLux.LightAPI(p); a = la.GetIntensityAttr()
            cur = a.Get(); a.Set((1.0 if cur is None else float(cur)) * mul); n += 1
    print("  boosted", n, "lights", flush=True)

def describe_arm(stage, root_path):
    prim = stage.GetPrimAtPath(root_path)
    joints, links = [], []
    for p in Usd.PrimRange(prim):
        t = p.GetTypeName()
        if t in ("PhysicsRevoluteJoint", "PhysicsPrismaticJoint"):
            joints.append((str(p.GetPath()).replace(root_path, ""), t))
        if t == "Xform":
            links.append(str(p.GetPath()).replace(root_path, ""))
    print(f"  DOF-joints ({len(joints)}):", flush=True)
    for jp, jt in joints:
        print("    ", jt.replace("Physics", "").replace("Joint", ""), jp, flush=True)
    print(f"  Xform links ({len(links)}): last 12 ->", links[-12:], flush=True)
    # candidate end-effector link by name
    kw = ("hand", "tool", "bracelet", "end_effector", "wrist_3", "gripper", "tcp")
    ee = [l for l in links if any(k in l.lower() for k in kw)]
    print("  EE candidates:", ee, flush=True)

for name, usd in ARMS.items():
    print("\n===== ARM:", name, "=====", flush=True)
    print("  usd:", usd, flush=True)
    ctx.open_stage(LAB)
    stage = ctx.get_stage()
    # clean parent xform I control for placement; reference the arm on a child so
    # the arm USD's own root xformOps don't collide with mine.
    base_path = f"/World/Arm_{name}"
    base = UsdGeom.Xform.Define(stage, Sdf.Path(base_path))
    base.AddTranslateOp().Set(BASE_POS)
    ap = f"{base_path}/robot"
    prim = stage.DefinePrim(ap, "Xform")
    prim.GetReferences().AddReference(usd)
    if not prim.IsLoaded():
        prim.Load()
    describe_arm(stage, ap)
    boost_lights(stage)
    try:
        rep.settings.set_render_rtx_realtime()
    except Exception as e:
        print("  rtx warn", e)
    # top-down cam above the base, oriented via look-at (up-axis aware)
    up_axis = UsdGeom.GetStageUpAxis(stage)
    up_vec = Gf.Vec3d(0, 0, 1) if up_axis == "Z" else Gf.Vec3d(0, 1, 0)
    eye = Gf.Vec3d(BASE_POS) + up_vec * 1.7      # 1.7 m "above" the base
    target = Gf.Vec3d(BASE_POS) + Gf.Vec3d(0, 0.0, 0.0)
    img_up = Gf.Vec3d(0, 1, 0) if up_axis == "Z" else Gf.Vec3d(0, 0, -1)
    view = Gf.Matrix4d().SetLookAt(eye, target, img_up)
    tp = f"/World/probe_topdown_{name}"
    cam = UsdGeom.Camera.Define(stage, Sdf.Path(tp))
    xf = UsdGeom.Xformable(cam.GetPrim())
    xf.AddTransformOp().Set(view.GetInverse())
    cam.GetFocalLengthAttr().Set(18.0)
    print("  stage up-axis:", up_axis, flush=True)
    # find general cam actual path (prim name contains 'general', not OmniverseKit)
    gcam = next((str(p.GetPath()) for p in stage.Traverse()
                 if p.GetTypeName() == "Camera" and "general" in p.GetName().lower()
                 and "Omniverse" not in str(p.GetPath())), None)
    targets = {"topdown": tp}
    if gcam:
        targets["general"] = gcam
        print("  general cam:", gcam, flush=True)
    else:
        print("  WARN no general cam found", flush=True)
    for label, campath in targets.items():
        if not stage.GetPrimAtPath(campath).IsValid():
            print("  skip", label, "(no cam", campath, ")", flush=True); continue
        rp = rep.create.render_product(campath, (W, H))
        wr = rep.WriterRegistry.get("BasicWriter")
        wr.initialize(output_dir=os.path.join(OUT, name, label), rgb=True)
        wr.attach([rp])
        rep.orchestrator.run_until_complete(num_frames=2)
        wr.detach(); rp.destroy()
        print("  rendered", label, "<-", campath, flush=True)

print("\nALL DONE", flush=True)
app.close()
