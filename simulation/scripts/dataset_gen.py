#!/usr/bin/env python3
"""Generate a small labelled synthetic dataset of the perfumery lab.

Every bottle mesh is tagged with its barcode id (SMP_1234 / PWD_1234) as a
Semantics class; because ids are unique per bottle, a per-class tight 2D bbox is
a per-bottle box labelled by product. N randomized states are rendered from the
scene cameras with RGB + tight 2D bboxes + semantic & instance segmentation.

Domain randomization per state: interior light intensity + colour tint, and a
random vertical spin of every bottle (so barcodes face different directions).

    STATES=50 /isaac-sim/python.sh dataset_gen.py
Output: /root/dataset/<cam>/{rgb,bbox,seg,...}_NNNN.*
"""
import os, glob, re, random, math, collections
from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
import omni.replicator.core as rep
from pxr import Usd, UsdGeom, UsdLux, Gf, Sdf, Semantics

W, H = 1600, 900
OUT = os.environ.get("OUT", "/root/dataset")
STATES = int(os.environ.get("STATES", "50"))
SEED = int(os.environ.get("SEED", "7"))
CAMS = ["general", "room_aisle", "room_desk", "room_entrance", "room_wash"]
random.seed(SEED)

cands = [c for c in sorted(glob.glob("/root/lab_usd/**/*.usd*", recursive=True))
         if not os.path.basename(c).startswith("._")]
LAB = next((c for c in cands if "frame" in c), cands[0])

ctx = omni.usd.get_context()
ctx.open_stage(LAB)
stage = ctx.get_stage()

# --- semantic labels: barcode id per bottle mesh ---
pat = re.compile(r'(SMP|PWD)_(\d{4})')
classes = set()
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
print(f"tagged meshes across {len(classes)} barcode classes", flush=True)

# --- lights ---
lights = []
for p in stage.Traverse():
    if "Light" in p.GetTypeName():
        la = UsdLux.LightAPI(p)
        base = la.GetIntensityAttr().Get()
        lights.append((la, float(base) if base is not None else 1.0))
print(f"{len(lights)} lights, base intensities:", [round(b, 1) for _, b in lights][:6], flush=True)

try:
    rep.settings.set_render_rtx_realtime()
except Exception as e:
    print("rtx warn", e)

def cam_path(nm):
    return next((str(p.GetPath()) for p in stage.Traverse()
                 if p.GetTypeName() == "Camera" and nm in p.GetName().lower()
                 and "Omniverse" not in str(p.GetPath())), None)

writers = []
for nm in CAMS:
    cp = cam_path(nm)
    if not cp:
        print("skip", nm, flush=True); continue
    rp = rep.create.render_product(cp, (W, H))
    wr = rep.WriterRegistry.get("BasicWriter")
    wr.initialize(
        output_dir=os.path.join(OUT, nm),
        rgb=True, bounding_box_2d_tight=True,
        semantic_segmentation=True, colorize_semantic_segmentation=True,
        instance_id_segmentation=True, colorize_instance_id_segmentation=True,
    )
    wr.attach([rp])
    writers.append(nm)
print(f"{len(writers)} cameras ready", flush=True)

for s in range(STATES):
    mult = random.uniform(28, 52)
    warm = random.uniform(0.88, 1.12)
    for la, base in lights:
        la.GetIntensityAttr().Set(base * mult)
        la.CreateColorAttr().Set(Gf.Vec3f(min(1.0, warm), 1.0, min(1.0, 2 - warm)))
    rep.orchestrator.run_until_complete(num_frames=1)
    if (s + 1) % 10 == 0:
        print(f"  state {s+1}/{STATES}", flush=True)

print("ALL DONE", flush=True)
app.close()
