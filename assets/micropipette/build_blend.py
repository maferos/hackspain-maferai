"""
Build micropipette.blend inside Blender (4.x / 5.x) from the same parametric geometry.

    blender -b -P build_blend.py -- /path/to/out/micropipette.blend

Creates: one mesh object per part, parented to 3 empties (Body / Plunger / Ejector)
so the moving parts can be animated; PBR materials; smooth shading + auto-smooth;
scene units = metres; also re-exports micropipette.glb next to the .blend.
"""
import sys, os, math
import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pipette_geometry import build_parts, MATERIALS, JOINTS, LINK_MASS, D

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else "micropipette.blend"

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.unit_settings.system = "METRIC"; sc.unit_settings.length_unit = "METERS"; sc.unit_settings.scale_length = 1.0

mats = {}
for k, v in MATERIALS.items():
    m = bpy.data.materials.new(f"pip_{k}"); m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = v["rgba"]
    bsdf.inputs["Roughness"].default_value = v["rough"]
    bsdf.inputs["Metallic"].default_value = 0.0
    if k == "display":
        bsdf.inputs["Roughness"].default_value = 0.1
    mats[k] = m

root = bpy.data.objects.new("Micropipette", None); sc.collection.objects.link(root)
root.empty_display_type = "PLAIN_AXES"; root.empty_display_size = 0.02
root["units"] = "m"; root["origin"] = "tip bottom-centre"; root["mass_kg"] = sum(LINK_MASS.values())
links = {}
for ln in ("body", "plunger", "ejector"):
    e = bpy.data.objects.new(f"Link_{ln}", None); sc.collection.objects.link(e)
    e.parent = root; e.empty_display_type = "ARROWS"; e.empty_display_size = 0.01
    e["mass_kg"] = LINK_MASS[ln]
    if ln in JOINTS:
        e["joint_axis"] = "Z"; e["joint_range_m"] = list(JOINTS[ln]["range"])
        # lock everything except Z translation so the empty behaves like a slide joint
        e.lock_location = (True, True, False); e.lock_rotation = (True, True, True)
        c = e.constraints.new("LIMIT_LOCATION"); c.use_min_z = c.use_max_z = True
        c.min_z, c.max_z = JOINTS[ln]["range"]; c.owner_space = "LOCAL"
    links[ln] = e

for name, verts, faces, mat, link in build_parts():
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(map(float, v)) for v in verts], [], [tuple(map(int, f)) for f in faces])
    me.update(); me.validate()
    for p in me.polygons: p.use_smooth = True
    me.materials.append(mats[mat])
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob)
    ob.parent = links[link]
    # sharpen the hard edges (box parts stay flat, lathe parts get a 35° auto-smooth)
    if len(faces) > 12:
        mod = ob.modifiers.new("Smooth by Angle", "NODES")
        try:
            bpy.ops.object.select_all(action="DESELECT"); ob.select_set(True); bpy.context.view_layer.objects.active = ob
            ob.modifiers.remove(mod)
            bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
        except Exception:
            pass
    else:
        for p in me.polygons: p.use_smooth = False

# simple lighting/camera so the file renders straight away
cam = bpy.data.cameras.new("Cam"); co = bpy.data.objects.new("Camera", cam); sc.collection.objects.link(co)
co.location = (0.32, -0.42, 0.28); co.rotation_euler = (math.radians(75), 0, math.radians(37)); sc.camera = co
cam.lens = 85
li = bpy.data.lights.new("Key", "AREA"); li.energy = 60; li.size = 0.5
lo = bpy.data.objects.new("Key", li); sc.collection.objects.link(lo); lo.location = (0.3, -0.3, 0.6)
lo.rotation_euler = (math.radians(35), 0, math.radians(45))
sc.render.engine = "BLENDER_EEVEE_NEXT" if hasattr(bpy.types, "SceneEEVEE") else "BLENDER_EEVEE"

os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT))
glb = os.path.splitext(os.path.abspath(OUT))[0] + ".glb"
bpy.ops.object.select_all(action="DESELECT")
for ob in root.children_recursive: ob.select_set(True)
root.select_set(True)
bpy.ops.export_scene.gltf(filepath=glb, use_selection=True, export_apply=True, export_yup=True, export_extras=True)
print("saved", OUT, "and", glb)
