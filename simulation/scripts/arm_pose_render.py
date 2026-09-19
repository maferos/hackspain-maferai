#!/usr/bin/env python3
"""Pose a robot arm over the lab bench (hand pointing down) and render an
eye-in-hand camera mounted just below the hand, plus the 'general' overview,
from several base positions.

Env:
  ONLY_ARM=franka|ur10e|kinova_gen3   (default: all three)
  NPOSES=1..4                          (how many base placements, default 3)

Uses the isaacsim articulation API to set joint angles (gravity disabled so the
pose holds), then Replicator BasicWriter to capture. Output: /root/arm_pose/<arm>/pose<i>/{eih,general}
"""
import os, glob, math
import numpy as np
from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
import omni.replicator.core as rep
from pxr import Usd, UsdGeom, UsdLux, UsdPhysics, Gf, Sdf
from isaacsim.core.api import SimulationContext
from isaacsim.core.prims import SingleArticulation, SingleRigidPrim
from isaacsim.core.utils.types import ArticulationAction

W, H = 1600, 900
OUT = os.environ.get("OUT", "/root/arm_pose")
NPOSES = int(os.environ.get("NPOSES", "3"))
ONLY = os.environ.get("ONLY_ARM", "").strip()          # comma-separated arm list ok
TILT = float(os.environ.get("TILT", "0"))              # eye-in-hand tilt from vertical (deg)
SKIP_GENERAL = os.environ.get("SKIP_GENERAL", "") == "1"

# assets root
def assets_root():
    from isaacsim.storage.native import get_assets_root_path
    return get_assets_root_path()
ROOT = assets_root()
ISAAC = f"{ROOT}/Isaac"; ISAACLAB = f"{ISAAC}/IsaacLab"

# lab stage
cands = [c for c in sorted(glob.glob("/root/lab_usd/**/*.usd*", recursive=True))
         if not os.path.basename(c).startswith("._")]
LAB = next((c for c in cands if "frame" in c), cands[0])

# per-arm config: usd, EE link (relative to robot root, +Z approach), down-looking
# joint dict {joint_name: radians}, and eye-in-hand mount offset along +Z_link.
# pose = rough hand-down config (raises the hand ~0.45 m over the base so the
# eye-in-hand, dropped just below the hand, frames a cluster of bottles).
# bases = (x, y, z, yaw_deg) over POPULATED bench areas (avoid the y=-0.55 aisle).
ARMS = {
    "franka": dict(
        usd=f"{ISAACLAB}/Robots/FrankaEmika/panda_instanceable.usd",
        ee="/panda_hand", cam_off=0.06,
        pose={"panda_joint1": 0.0, "panda_joint2": -0.35, "panda_joint3": 0.0,
              "panda_joint4": -1.45, "panda_joint5": 0.0, "panda_joint6": 1.65,
              "panda_joint7": 0.785,
              "panda_finger_joint1": 0.04, "panda_finger_joint2": 0.04},
        bases=[(-3.7, -0.35, 0.9, 0), (-3.1, 0.00, 0.9, 0), (-2.6, -0.30, 0.9, 0),
               (-2.1, -0.15, 0.9, 0), (-1.6, -0.40, 0.9, 0), (-1.1, -0.25, 0.9, 0)],
    ),
    "ur10e": dict(
        usd=f"{ISAAC}/Robots/UniversalRobots/ur10e/ur10e.usd",
        ee="/wrist_3_link/flange", cam_off=0.04,
        pose={"shoulder_pan_joint": 0.0, "shoulder_lift_joint": -1.75,
              "elbow_joint": 1.35, "wrist_1_joint": -1.15,
              "wrist_2_joint": -1.5708, "wrist_3_joint": 0.0},
        bases=[(-3.9, -0.35, 0.9, 0), (-2.8, -0.30, 0.9, 0), (-1.8, -0.40, 0.9, 0)],
    ),
    "kinova_gen3": dict(
        usd=f"{ISAAC}/Robots/Kinova/Gen3/gen3n7_instanceable.usd",
        ee="/end_effector_link", cam_off=0.05,
        pose={"joint_1": 0.0, "joint_2": 0.18, "joint_3": 0.0, "joint_4": 1.10,
              "joint_5": 0.0, "joint_6": 0.95, "joint_7": 1.5708},
        bases=[(-3.8, -0.35, 0.9, 0), (-3.2, 0.00, 0.9, 0), (-2.7, -0.30, 0.9, 0),
               (-2.2, -0.15, 0.9, 0), (-1.7, -0.40, 0.9, 0), (-1.2, -0.25, 0.9, 0)],
    ),
}
if ONLY:
    want = [a.strip() for a in ONLY.split(",") if a.strip()]
    ARMS = {a: ARMS[a] for a in want}

ctx = omni.usd.get_context()

def boost_lights(stage, mul=40.0):
    for p in stage.Traverse():
        if "Light" in p.GetTypeName():
            la = UsdLux.LightAPI(p); a = la.GetIntensityAttr()
            cur = a.Get(); a.Set((1.0 if cur is None else float(cur)) * mul)

def ensure_zero_gravity(stage):
    sc = None
    for p in stage.Traverse():
        if p.GetTypeName() == "PhysicsScene":
            sc = UsdPhysics.Scene(p); break
    if sc is None:
        sc = UsdPhysics.Scene.Define(stage, Sdf.Path("/physicsScene"))
    sc.CreateGravityMagnitudeAttr().Set(0.0)

def general_cam(stage):
    return next((str(p.GetPath()) for p in stage.Traverse()
                 if p.GetTypeName() == "Camera" and "general" in p.GetName().lower()
                 and "Omniverse" not in str(p.GetPath())), None)

def render_cam(campath, outdir):
    os.makedirs(outdir, exist_ok=True)
    rp = rep.create.render_product(campath, (W, H))
    wr = rep.WriterRegistry.get("BasicWriter")
    wr.initialize(output_dir=outdir, rgb=True)
    wr.attach([rp])
    rep.orchestrator.run_until_complete(num_frames=2)
    wr.detach(); rp.destroy()

for name, cfg in ARMS.items():
    for i, (bx, by, bz, yaw) in enumerate(cfg["bases"][:NPOSES]):
        print(f"\n===== {name} pose{i} base=({bx},{by},{bz}) yaw={yaw} =====", flush=True)
        ctx.open_stage(LAB)
        stage = ctx.get_stage()
        boost_lights(stage)
        ensure_zero_gravity(stage)
        try: rep.settings.set_render_rtx_realtime()
        except Exception as e: print("rtx warn", e)

        base_path = f"/World/Arm_{name}"
        base = UsdGeom.Xform.Define(stage, Sdf.Path(base_path))
        base.AddTranslateOp().Set(Gf.Vec3d(bx, by, bz))
        base.AddRotateZOp().Set(float(yaw))
        robot_path = f"{base_path}/robot"
        prim = stage.DefinePrim(robot_path, "Xform")
        prim.GetReferences().AddReference(cfg["usd"])
        if not prim.IsLoaded(): prim.Load()
        ee_path = robot_path + cfg["ee"]

        # articulation posing (rough hand-down pose; gravity is 0 so it holds)
        sim = SimulationContext(stage_units_in_meters=1.0)
        sim.reset()
        art = SingleArticulation(prim_path=robot_path, name=f"arm_{name}_{i}")
        art.initialize()
        dof = list(art.dof_names)
        pose = dict(cfg["pose"])
        # optional per-run tuning: POSE_OVERRIDE="wrist_1_joint:-2.2,elbow_joint:1.4"
        for kv in os.environ.get("POSE_OVERRIDE", "").split(","):
            if ":" in kv:
                k, v = kv.split(":"); pose[k.strip()] = float(v)
        q = np.zeros(len(dof), dtype=np.float32)
        for jn, val in pose.items():
            if jn in dof:
                q[dof.index(jn)] = val
        art.set_joint_positions(q)
        art.apply_action(ArticulationAction(joint_positions=q))
        for _ in range(3):
            sim.step(render=True)

        # read the ACTUAL hand world position, then drop the eye-in-hand camera
        # just below it looking straight down (world) so it always frames the bench.
        ee_rigid = SingleRigidPrim(prim_path=ee_path, name=f"ee_{name}_{i}")
        ee_rigid.initialize()
        pos, quat = ee_rigid.get_world_pose()
        pos = np.asarray(pos, dtype=float)
        print("  dof:", dof, flush=True)
        print("  q  :", [round(float(x), 3) for x in q], flush=True)
        print("  hand world pos:", [round(float(v), 3) for v in pos], flush=True)

        # eye-in-hand: just below the hand, but clamped to a fixed height above
        # the bench so it always frames a wide cluster of bottles (not one cap).
        BENCH_Z, CAM_H = 0.9, 0.70
        cam_z = min(float(pos[2]) - cfg["cam_off"], BENCH_Z + CAM_H)
        eye = Gf.Vec3d(float(pos[0]), float(pos[1]), cam_z)
        # straight down, or tilted TILT deg toward +y (shows bottle sides/labels)
        t = math.radians(TILT)
        tgt = eye + Gf.Vec3d(0.0, math.sin(t), -math.cos(t))
        view = Gf.Matrix4d().SetLookAt(eye, tgt, Gf.Vec3d(0, 1, 0))
        cam_path = f"/World/eih_cam_{name}_{i}"
        cam = UsdGeom.Camera.Define(stage, Sdf.Path(cam_path))
        UsdGeom.Xformable(cam.GetPrim()).AddTransformOp().Set(view.GetInverse())
        cam.GetFocalLengthAttr().Set(18.0)
        cam.GetClippingRangeAttr().Set(Gf.Vec2f(0.01, 100.0))
        sim.render()

        render_cam(cam_path, os.path.join(OUT, name, f"pose{i}", "eih"))
        print("  rendered eih", flush=True)
        gc = None if SKIP_GENERAL else general_cam(stage)
        if gc:
            render_cam(gc, os.path.join(OUT, name, f"pose{i}", "general"))
            print("  rendered general", flush=True)
        sim.stop()

print("\nALL DONE", flush=True)
app.close()
