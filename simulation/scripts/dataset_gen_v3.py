#!/usr/bin/env python3
"""Synthetic lab dataset v3 — real GEOMETRIC domain randomization.

Fix vs v2: raw USD xformOp edits between Replicator renders do NOT reach the
render (Fabric caches transforms; only attribute edits like light intensity
propagate). So poses are written through Isaac's Fabric-aware XFormPrim API,
which the arm-posing path proved does render.

Per state: every bottle is reshuffled to a new collision-avoided spot on the
worktop and spun about its vertical axis, and lights are re-randomized. RGB +
tight 2D boxes (barcode id) + semantic/instance masks per camera. Cameras stay
at their 5 base poses (jittering them via Fabric flipped the general view, and
the reshuffle already gives strong geometric diversity).

    STATES=60 /isaac-sim/python.sh dataset_gen_v3.py     # 5 cams x 60 = 300 frames
"""
import os, glob, re, random, collections, math
import numpy as np
from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
import omni.replicator.core as rep
from pxr import Usd, UsdGeom, UsdLux, Gf, Semantics
from isaacsim.core.api import SimulationContext
from isaacsim.core.prims import XFormPrim

W, H = 1600, 900
OUT = os.environ.get("OUT", "/root/dataset_v3")
STATES = int(os.environ.get("STATES", "60"))
SEED = int(os.environ.get("SEED", "13"))
CAMS = ["general", "room_aisle", "room_desk", "room_entrance", "room_wash"]
CAM_ROT, CAM_TRA = 3.0, 0.15
XMIN, XMAX, YMIN, YMAX = -4.3, 1.3, -1.25, 0.45
MIN_DIST = 0.085
EXCL = [(-3.35, -1.16), (-1.7, -1.16), (-0.2, -1.16), (-2.5, 0.36), (-0.75, 0.36)]
EXCL_R = 0.40
random.seed(SEED); np.random.seed(SEED)

cands = [c for c in sorted(glob.glob("/root/lab_usd/**/*.usd*", recursive=True))
         if not os.path.basename(c).startswith("._")]
LAB = next((c for c in cands if "frame" in c), cands[0])

ctx = omni.usd.get_context(); ctx.open_stage(LAB); stage = ctx.get_stage()
tc = Usd.TimeCode(stage.GetStartTimeCode()) if stage.HasAuthoredTimeCodeRange() else Usd.TimeCode.EarliestTime()
xc = UsdGeom.XformCache(tc)

# tag bottle meshes + collect wrapper prims, grouped by bottle
pat = re.compile(r'(SMP|PWD)_(\d{4})')
classes = set(); parents = []; seen = set(); by_bottle = collections.defaultdict(list)
for m in stage.Traverse():
    if m.GetTypeName() != "Mesh":
        continue
    mm = pat.search(str(m.GetPath()))
    if not mm:
        continue
    s = Semantics.SemanticsAPI.Apply(m, "Semantics")
    s.CreateSemanticTypeAttr().Set("class"); s.CreateSemanticDataAttr().Set(mm.group(0))
    classes.add(mm.group(0))
    par = m.GetParent(); pp = str(par.GetPath())
    if pp not in seen:
        seen.add(pp); parents.append((pp, par, "_body_" in pp)); by_bottle[mm.group(0)].append(pp)
print(f"tagged {len(classes)} classes, {len(parents)} parts", flush=True)

# base world pose per part
part_paths = [pp for pp, _, _ in parents]
base_pos = np.array([list(xc.GetLocalToWorldTransform(pr).ExtractTranslation()) for _, pr, _ in parents])
def quat_wxyz(M):
    q = M.ExtractRotationQuat(); im = q.GetImaginary()
    return [q.GetReal(), im[0], im[1], im[2]]
base_quat = np.array([quat_wxyz(xc.GetLocalToWorldTransform(pr)) for _, pr, _ in parents])
# bottle centre (body xy) per part, and bottle index per part
bcentre = {}
for cid, pps in by_bottle.items():
    body = next((pp for pp in pps if dict((p, b) for p, _, b in parents)[pp]), pps[0])
    bp = base_pos[part_paths.index(body)]
    bcentre[cid] = (bp[0], bp[1])
part_cid = [next(cid for cid, pps in by_bottle.items() if pp in pps) for pp in part_paths]
Cxy = np.array([bcentre[c] for c in part_cid])
dxy = base_pos[:, :2] - Cxy                      # part offset from bottle centre

# camera render paths (kept at their base pose — reshuffle gives the diversity)
cam_render_paths = []
for nm in CAMS:
    cp = next((p for p in stage.Traverse() if p.GetTypeName() == "Camera"
               and nm in p.GetName().lower() and "Omniverse" not in str(p.GetPath())), None)
    if not cp:
        print("skip", nm, flush=True); continue
    cam_render_paths.append(str(cp.GetPath()))
print(f"{len(cam_render_paths)} cameras", flush=True)

# lights (USD attr edits propagate fine)
lights = [(UsdLux.LightAPI(p), (UsdLux.LightAPI(p).GetIntensityAttr().Get() or 1.0))
          for p in stage.Traverse() if "Light" in p.GetTypeName()]

# --- Fabric-aware views ---
sim = SimulationContext(stage_units_in_meters=1.0)
sim.reset()
parts_view = XFormPrim(part_paths)

try: rep.settings.set_render_rtx_realtime()
except Exception as e: print("rtx warn", e)

writers = []
for cp in cam_render_paths:
    nm = cp.split("/")[-1]
    rp = rep.create.render_product(cp, (W, H))
    wr = rep.WriterRegistry.get("BasicWriter")
    wr.initialize(output_dir=os.path.join(OUT, nm.replace("Camera_", "").replace("Camera", "")),
                  rgb=True, bounding_box_2d_tight=True,
                  semantic_segmentation=True, colorize_semantic_segmentation=True,
                  instance_id_segmentation=True, colorize_instance_id_segmentation=True)
    wr.attach([rp]); writers.append(nm)
print(f"{len(writers)} cameras ready; generating {STATES} states", flush=True)

def reshuffle():
    placed = []
    for _ in by_bottle:
        for _t in range(40):
            x = random.uniform(XMIN, XMAX); y = random.uniform(YMIN, YMAX)
            if any((x-ex)**2+(y-ey)**2 < EXCL_R**2 for ex, ey in EXCL): continue
            if any((x-px)**2+(y-py)**2 < MIN_DIST**2 for px, py in placed): continue
            break
        placed.append((x, y))
    return placed

bottle_ids = list(by_bottle.keys())
bottle_part_idx = [[part_paths.index(pp) for pp in by_bottle[c]] for c in bottle_ids]

for s in range(STATES):
    mult = random.uniform(28, 52); warm = random.uniform(0.88, 1.12)
    for la, base in lights:
        la.GetIntensityAttr().Set(base * mult)
        la.CreateColorAttr().Set(Gf.Vec3f(min(1.0, warm), 1.0, min(1.0, 2 - warm)))
    # per-bottle new centre + spin -> per-part world pose
    centers = reshuffle()
    theta = np.zeros(len(part_paths)); newC = np.zeros((len(part_paths), 2))
    for bi, (cx, cy) in enumerate(centers):
        th = random.uniform(0, 2 * math.pi)
        for pi in bottle_part_idx[bi]:
            theta[pi] = th; newC[pi] = (cx, cy)
    ct, st = np.cos(theta), np.sin(theta)
    rdx = ct * dxy[:, 0] - st * dxy[:, 1]
    rdy = st * dxy[:, 0] + ct * dxy[:, 1]
    new_pos = np.stack([newC[:, 0] + rdx, newC[:, 1] + rdy, base_pos[:, 2]], axis=1)
    a, d = np.cos(theta/2), np.sin(theta/2)          # spin quat (about world Z) x base
    w0, x0, y0, z0 = base_quat[:, 0], base_quat[:, 1], base_quat[:, 2], base_quat[:, 3]
    new_quat = np.stack([a*w0 - d*z0, a*x0 - d*y0, a*y0 + d*x0, a*z0 + d*w0], axis=1)
    parts_view.set_world_poses(positions=new_pos.astype(np.float32),
                               orientations=new_quat.astype(np.float32))
    app.update()                 # flush Fabric pose writes before the render
    rep.orchestrator.run_until_complete(num_frames=1)
    if (s + 1) % 10 == 0:
        print(f"  state {s+1}/{STATES}", flush=True)

print("ALL DONE", flush=True)
app.close()
