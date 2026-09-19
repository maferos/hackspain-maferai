#!/usr/bin/env python3
"""Synthetic lab dataset v2 — adds GEOMETRIC domain randomization on top of v1.

Per state, every bottle is spun about its own vertical axis (so its barcode faces
a new direction) and nudged a couple of cm, each of the 5 scene cameras gets a
small pose jitter, and the interior lights are re-randomized. Then RGB + tight 2D
boxes (labelled by barcode id) + semantic/instance masks are written per camera.

    STATES=60 /isaac-sim/python.sh dataset_gen_v2.py     # 5 cams x 60 = 300 frames
"""
import os, glob, re, random, collections
from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
import omni.replicator.core as rep
from pxr import Usd, UsdGeom, UsdLux, Gf, Sdf, Semantics

W, H = 1600, 900
OUT = os.environ.get("OUT", "/root/dataset_v2")
STATES = int(os.environ.get("STATES", "60"))
SEED = int(os.environ.get("SEED", "11"))
CAMS = ["general", "room_aisle", "room_desk", "room_entrance", "room_wash"]
POS_JIT = 0.02        # bottle xy jitter (m)
CAM_ROT = 3.0         # camera rot jitter (deg)
CAM_TRA = 0.15        # camera translate jitter (m)
random.seed(SEED)

cands = [c for c in sorted(glob.glob("/root/lab_usd/**/*.usd*", recursive=True))
         if not os.path.basename(c).startswith("._")]
LAB = next((c for c in cands if "frame" in c), cands[0])

ctx = omni.usd.get_context()
ctx.open_stage(LAB)
stage = ctx.get_stage()
tc = Usd.TimeCode(stage.GetStartTimeCode()) if stage.HasAuthoredTimeCodeRange() else Usd.TimeCode.EarliestTime()
xcache = UsdGeom.XformCache(tc)

# --- tag bottle meshes by barcode + collect their Mesh_Xform wrappers ---
pat = re.compile(r'(SMP|PWD)_(\d{4})')
classes = set()
parents = {}          # parent path -> (prim, is_body)
by_bottle = collections.defaultdict(list)   # barcode -> [parent path]
for m in stage.Traverse():
    if m.GetTypeName() != "Mesh":
        continue
    mm = pat.search(str(m.GetPath()))
    if not mm:
        continue
    sem = Semantics.SemanticsAPI.Apply(m, "Semantics")
    sem.CreateSemanticTypeAttr().Set("class")
    sem.CreateSemanticDataAttr().Set(mm.group(0))
    classes.add(mm.group(0))
    par = m.GetParent(); pp = str(par.GetPath())
    if pp not in parents:
        parents[pp] = (par, "_body_" in pp)
        by_bottle[mm.group(0)].append(pp)
print(f"tagged across {len(classes)} classes, {len(parents)} bottle parts", flush=True)

# capture base world matrices BEFORE editing ops
base_M = {pp: Gf.Matrix4d(xcache.GetLocalToWorldTransform(pr)) for pp, (pr, _) in parents.items()}
# bottle centre = body part xy (fallback: mean)
centre = {}
for cid, pps in by_bottle.items():
    body = next((pp for pp in pps if parents[pp][1]), pps[0])
    t = base_M[body].ExtractTranslation()
    centre[cid] = Gf.Vec3d(t[0], t[1], 0.0)
part_of = {pp: cid for cid, pps in by_bottle.items() for pp in pps}

# replace each part's ops with a single transform op we drive per state
part_ops = {}
for pp, (pr, _) in parents.items():
    xf = UsdGeom.Xformable(pr)
    xf.ClearXformOpOrder()
    part_ops[pp] = xf.AddTransformOp()

# --- cameras: capture base, replace Camera_Xform ops with a transform op ---
def cam_prim(nm):
    return next((p for p in stage.Traverse()
                 if p.GetTypeName() == "Camera" and nm in p.GetName().lower()
                 and "Omniverse" not in str(p.GetPath())), None)
cam_info = {}   # nm -> (cam_path, xform_op, base_M)
for nm in CAMS:
    cp = cam_prim(nm)
    if not cp:
        print("skip", nm, flush=True); continue
    xw = cp.GetParent()                      # Camera_Xform_<nm> holds the transform
    bM = Gf.Matrix4d(xcache.GetLocalToWorldTransform(xw))
    xf = UsdGeom.Xformable(xw); xf.ClearXformOpOrder()
    op = xf.AddTransformOp()
    op.Set(bM)
    cam_info[nm] = (str(cp.GetPath()), op, bM)
print(f"{len(cam_info)} cameras", flush=True)

# --- lights ---
lights = []
for p in stage.Traverse():
    if "Light" in p.GetTypeName():
        la = UsdLux.LightAPI(p); b = la.GetIntensityAttr().Get()
        lights.append((la, float(b) if b is not None else 1.0))

try:
    rep.settings.set_render_rtx_realtime()
except Exception as e:
    print("rtx warn", e)

writers = []
for nm, (cp, op, bM) in cam_info.items():
    rp = rep.create.render_product(cp, (W, H))
    wr = rep.WriterRegistry.get("BasicWriter")
    wr.initialize(output_dir=os.path.join(OUT, nm), rgb=True,
                  bounding_box_2d_tight=True,
                  semantic_segmentation=True, colorize_semantic_segmentation=True,
                  instance_id_segmentation=True, colorize_instance_id_segmentation=True)
    wr.attach([rp]); writers.append(nm)
print(f"{len(writers)} cameras ready; generating {STATES} states", flush=True)

def spin_shift(C, deg, dx, dy):
    # world-space transform: rotate about vertical axis through C, then shift xy
    W = Gf.Matrix4d().SetTranslate(-C)
    W = W * Gf.Matrix4d().SetRotate(Gf.Rotation(Gf.Vec3d(0, 0, 1), deg))
    W = W * Gf.Matrix4d().SetTranslate(C + Gf.Vec3d(dx, dy, 0.0))
    return W

def cam_jitter():
    r = Gf.Rotation(Gf.Vec3d(1, 0, 0), random.uniform(-CAM_ROT, CAM_ROT)) \
        * Gf.Rotation(Gf.Vec3d(0, 1, 0), random.uniform(-CAM_ROT, CAM_ROT)) \
        * Gf.Rotation(Gf.Vec3d(0, 0, 1), random.uniform(-CAM_ROT, CAM_ROT))
    d = Gf.Matrix4d().SetRotate(r)
    d = d * Gf.Matrix4d().SetTranslate(Gf.Vec3d(*(random.uniform(-CAM_TRA, CAM_TRA) for _ in range(3))))
    return d

for s in range(STATES):
    mult = random.uniform(28, 52); warm = random.uniform(0.88, 1.12)
    for la, base in lights:
        la.GetIntensityAttr().Set(base * mult)
        la.CreateColorAttr().Set(Gf.Vec3f(min(1.0, warm), 1.0, min(1.0, 2 - warm)))
    # bottles: one spin+shift per bottle, applied to all its parts
    for cid, pps in by_bottle.items():
        deg = random.uniform(0, 360)
        dx, dy = random.uniform(-POS_JIT, POS_JIT), random.uniform(-POS_JIT, POS_JIT)
        Wm = spin_shift(centre[cid], deg, dx, dy)
        for pp in pps:
            part_ops[pp].Set(base_M[pp] * Wm)
    # cameras: small pose jitter in local frame
    for nm, (cp, op, bM) in cam_info.items():
        op.Set(cam_jitter() * bM)
    rep.orchestrator.run_until_complete(num_frames=1)
    if (s + 1) % 10 == 0:
        print(f"  state {s+1}/{STATES}", flush=True)

print("ALL DONE", flush=True)
app.close()
