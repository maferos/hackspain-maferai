"""
generate_pasteur_pipette.py — 3 ml graduated polyethylene Pasteur (transfer) pipette.

Run headless:  blender -b -P generate_pasteur_pipette.py -- --out <dir>

Conventions (same as reagent_jars_kit):
  * metres, origin at the TIP (bottom-centre), axis +Z towards the bulb
  * visual  : one smooth mesh, ~5k tris, translucent LDPE material
  * collision: 3 convex pieces (bulb, stem_upper, stem_lower) -> valid for
    MuJoCo (mesh = convex hull) and Isaac Lab / PhysX (convex hull per mesh)
Outputs: .blend, .glb, meshes/*.obj (+Z up), optional .usd
"""
import bpy, bmesh, math, sys, os, json
from mathutils import Vector

# ----------------------------------------------------------------- params (mm)
TOTAL_LEN   = 155.0     # standard 3 ml transfer pipette
BULB_R      = 6.6
BULB_CYL_Z0 = 116.0     # bottom of the cylindrical bulb section
BULB_CYL_Z1 = TOTAL_LEN - BULB_R   # top of cylinder, hemisphere above
STEM_R_TOP  = 3.1       # stem just below the shoulder
STEM_R_TIP  = 1.15      # outer radius at the tip
TIP_BORE_R  = 0.55      # bore of the tip (visual only)
SHOULDER = [(106.0, STEM_R_TOP), (111.0, 4.2), (114.5, 6.0), (BULB_CYL_Z0, BULB_R)]
# graduation rings: (z_mm, label) — 0.5 ml steps, labelled every 1 ml
GRADS = [(40.0, None), (54.0, "1"), (67.0, None), (79.0, "2"), (90.0, None), (100.0, "3")]
RIDGE_H, RIDGE_W = 0.22, 1.0
MASS_KG = 0.0012        # ~1.2 g for a 3 ml LDPE transfer pipette
MM = 0.001

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = args[args.index("--out") + 1] if "--out" in args else os.getcwd()
os.makedirs(os.path.join(OUT, "meshes"), exist_ok=True)


# --------------------------------------------------------------- lathe helper
def stem_radius(z):
    """Outer radius of the tapered stem at height z (mm), linear taper."""
    t = min(max(z / SHOULDER[0][0], 0.0), 1.0)
    return STEM_R_TIP + (STEM_R_TOP - STEM_R_TIP) * t


def lathe(name, profile, segments=48, close_bottom=True, close_top=True, scale=MM):
    """profile: list of (z, r) with z increasing. r==0 at an end -> pole."""
    bm = bmesh.new()
    rings = []
    for (z, r) in profile:
        if r <= 1e-6:
            rings.append([bm.verts.new((0, 0, z * scale))])
            continue
        ring = [bm.verts.new((r * math.cos(2 * math.pi * i / segments) * scale,
                              r * math.sin(2 * math.pi * i / segments) * scale,
                              z * scale)) for i in range(segments)]
        rings.append(ring)
    for a, b in zip(rings[:-1], rings[1:]):
        if len(a) == 1:
            for i in range(segments):
                bm.faces.new((a[0], b[i], b[(i + 1) % segments]))
        elif len(b) == 1:
            for i in range(segments):
                bm.faces.new((a[i], b[0], a[(i + 1) % segments]))
        else:
            for i in range(segments):
                bm.faces.new((a[i], a[(i + 1) % segments], b[(i + 1) % segments], b[i]))
    if close_bottom and len(rings[0]) > 1:
        bm.faces.new(list(reversed(rings[0])))
    if close_top and len(rings[-1]) > 1:
        bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob


def hemisphere_profile(z0, r, n=10, top=True):
    """(z, r) points of a hemisphere of radius r sitting on z0 (top) or hanging from z0 (bottom)."""
    pts = []
    for i in range(1, n + 1):
        a = (math.pi / 2) * i / n
        pts.append((z0 + (r * math.sin(a) if top else -r * math.sin(a)), r * math.cos(a)))
    return pts


# ------------------------------------------------------------------- scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'MILLIMETERS'

# ---- visual profile: tip bore -> outer tip -> stem with ridges -> shoulder -> bulb -> dome
vis = [(0.0, TIP_BORE_R), (0.0, STEM_R_TIP)]
z = 2.0
grad_iter = iter(GRADS)
next_g = next(grad_iter, None)
while z < SHOULDER[0][0]:
    if next_g and next_g[0] - RIDGE_W / 2 <= z:
        gz = next_g[0]
        rb = stem_radius(gz)
        vis += [(gz - RIDGE_W / 2, stem_radius(gz - RIDGE_W / 2)),
                (gz - RIDGE_W / 2 + 0.15, rb + RIDGE_H),
                (gz + RIDGE_W / 2 - 0.15, rb + RIDGE_H),
                (gz + RIDGE_W / 2, stem_radius(gz + RIDGE_W / 2))]
        z = gz + RIDGE_W / 2 + 3.0
        next_g = next(grad_iter, None)
        continue
    vis.append((z, stem_radius(z)))
    z += 6.0
vis += SHOULDER
vis += [(BULB_CYL_Z1, BULB_R)]
vis += hemisphere_profile(BULB_CYL_Z1, BULB_R, n=12, top=True)   # ends at r=0 pole

visual = lathe("PasteurPipette_visual", vis, segments=48, close_bottom=True, close_top=False)
me = visual.data
for p in me.polygons:
    p.use_smooth = True
me.use_auto_smooth = True
me.auto_smooth_angle = math.radians(35)

# ---- embossed numerals (visual only) on the +X side of the stem
for gz, label in GRADS:
    if not label:
        continue
    bpy.ops.object.text_add()
    t = bpy.context.object
    t.data.body = label
    t.data.size = 2.6 * MM
    t.data.extrude = 0.12 * MM
    t.data.align_x = 'CENTER'
    t.data.align_y = 'CENTER'
    r = stem_radius(gz + 3.0)
    t.location = (r * MM, 0.0, (gz + 3.0) * MM)
    t.rotation_euler = (math.radians(90), 0, math.radians(90))
    bpy.ops.object.convert(target='MESH')
    t.name = f"Numeral_{label}"
    t.select_set(True)
visual.select_set(True)
bpy.context.view_layer.objects.active = visual
bpy.ops.object.join()
visual = bpy.context.object

# ---- material: translucent LDPE
mat = bpy.data.materials.new("LDPE_translucent")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.90, 0.92, 0.95, 1.0)
bsdf.inputs["Roughness"].default_value = 0.32
bsdf.inputs["IOR"].default_value = 1.51
bsdf.inputs["Alpha"].default_value = 0.55
if "Transmission Weight" in bsdf.inputs:
    bsdf.inputs["Transmission Weight"].default_value = 0.35
mat.blend_method = 'BLEND'
mat.shadow_method = 'HASHED'
mat.show_transparent_back = False
visual.data.materials.append(mat)

# ---- custom properties (exported as glTF extras)
visual["capacity_ml"] = 3.0
visual["material"] = "LDPE (low-density polyethylene)"
visual["length_m"] = TOTAL_LEN * MM
visual["mass_kg"] = MASS_KG
visual["origin"] = "tip, +Z towards bulb"

# ---- collision: three convex pieces (16 segments, low poly)
col_bulb = lathe("col_bulb",
                 [(SHOULDER[0][0], SHOULDER[0][1])] + SHOULDER[1:] + [(BULB_CYL_Z1, BULB_R)]
                 + hemisphere_profile(BULB_CYL_Z1, BULB_R, n=5, top=True),
                 segments=16, close_top=False)
z_mid = 52.0
col_up = lathe("col_stem_upper",
               [(z_mid - 1.0, stem_radius(z_mid - 1.0)), (SHOULDER[0][0] + 1.0, STEM_R_TOP + 0.05)],
               segments=16)
col_lo = lathe("col_stem_lower",
               [(0.0, STEM_R_TIP), (z_mid + 1.0, stem_radius(z_mid + 1.0))],
               segments=16)
collisions = [col_bulb, col_up, col_lo]
col_coll = bpy.data.collections.new("collision")
scene.collection.children.link(col_coll)
for c in collisions:
    scene.collection.objects.unlink(c)
    col_coll.objects.link(c)
    c.display_type = 'WIRE'
    c.hide_render = True

# ---- lights + camera for a preview render
bpy.ops.object.light_add(type='AREA', location=(0.15, -0.2, 0.3))
bpy.context.object.data.energy = 8
bpy.context.object.data.size = 0.3
bpy.ops.object.light_add(type='AREA', location=(-0.2, 0.15, 0.2))
bpy.context.object.data.energy = 4
bpy.context.object.data.size = 0.4
bpy.ops.object.camera_add(location=(0.30, -0.30, 0.22))
scene.camera = bpy.context.object
scene.camera.data.lens = 55
bpy.ops.object.empty_add(location=(0, 0, 0.075))
target = bpy.context.object
trk = scene.camera.constraints.new('TRACK_TO'); trk.target = target
trk.track_axis = 'TRACK_NEGATIVE_Z'; trk.up_axis = 'UP_Y'
bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0, -0.0001))
floor = bpy.context.object
fm = bpy.data.materials.new("floor"); fm.use_nodes = True
fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.85, 0.85, 0.83, 1)
floor.data.materials.append(fm)
floor.hide_viewport = True  # keep out of exports (we export by selection)

# ------------------------------------------------------------------ exports
def select_only(objs):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]

# OBJ, +Z up for MuJoCo / URDF
for o in [visual] + collisions:
    select_only([o])
    fname = "pipette_visual.obj" if o is visual else f"pipette_{o.name}.obj"
    bpy.ops.wm.obj_export(filepath=os.path.join(OUT, "meshes", fname),
                          export_selected_objects=True, forward_axis='Y', up_axis='Z',
                          export_materials=False, export_normals=True, export_uv=False,
                          apply_modifiers=True)

# glTF (visual + collision nodes, extras)
select_only([visual] + collisions)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "pasteur_pipette.glb"),
                          export_format='GLB', use_selection=True,
                          export_extras=True, export_apply=True, export_yup=True)

# USD (if this Blender build has it)
try:
    select_only([visual] + collisions)
    bpy.ops.wm.usd_export(filepath=os.path.join(OUT, "pasteur_pipette.usd"),
                          selected_objects_only=True, export_materials=True)
    print("USD exported")
except Exception as e:
    print("USD export not available:", e)

# .blend
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "pasteur_pipette.blend"))

# preview render (Cycles CPU, low samples)
try:
    floor.hide_viewport = False
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 48
    scene.cycles.device = 'CPU'
    scene.cycles.use_denoising = False
    scene.view_layers[0].cycles.use_denoising = False
    scene.render.resolution_x, scene.render.resolution_y = 600, 900
    scene.render.filepath = os.path.join(OUT, "pasteur_pipette_preview.png")
    scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.9, 0.92, 0.95, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.6
    bpy.ops.render.render(write_still=True)
except Exception as e:
    print("Render skipped:", e)

json.dump({"length_m": TOTAL_LEN * MM, "bulb_radius_m": BULB_R * MM,
           "mass_kg": MASS_KG, "capacity_ml": 3.0,
           "tris_visual": len(visual.data.polygons)},
          open(os.path.join(OUT, "pipette_meta.json"), "w"), indent=2)
print("DONE tris:", len(visual.data.polygons))
