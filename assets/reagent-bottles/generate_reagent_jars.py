"""
generate_reagent_jars.py — Plastic reagent jars + powders for a virtual perfumery lab.

Runs headless with the `bpy` wheel (Blender 5.0+) or from inside Blender:
    blender --background --python generate_reagent_jars.py -- --out /path/to/out
Everything is built procedurally (no external assets), real-world scale in metres,
origin at the bottom-centre of each asset, +Z up (exported to glTF as +Y up).

Outputs (in --out):
    reagent_jars_kit.blend        all assets, one collection per asset
    reagent_jars_kit.glb          everything in one file
    glb/<asset>.glb               one file per asset
    labels/<material>.png         label textures (swap freely)
    preview.png                   Cycles render of the whole kit
"""
import bpy, bmesh, math, os, random, sys
from mathutils import Vector, noise

# ----------------------------------------------------------------------------- config
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.abspath(argv[argv.index("--out") + 1]) if "--out" in argv else os.path.abspath("out")
os.makedirs(os.path.join(OUT, "glb"), exist_ok=True)
os.makedirs(os.path.join(OUT, "labels"), exist_ok=True)
random.seed(7)

# Wide-mouth lab jars, real sizes (mm): name, outer diameter, height, cap colour
JAR_SIZES = [
    ("30ml",   36,  48, "white"),
    ("60ml",   46,  58, "white"),
    ("125ml",  56,  78, "blue"),
    ("250ml",  70, 100, "blue"),
    ("500ml",  86, 132, "black"),
    ("1000ml", 106, 176, "black"),
]
# Perfumery raw materials that are sold as powders/crystals (name, CAS, powder RGB, fill fraction)
POWDERS = [
    ("Vanillin",        "121-33-5",   (0.96, 0.94, 0.86), 0.62),
    ("Ethyl Maltol",    "4940-11-8",  (0.98, 0.98, 0.97), 0.55),
    ("Coumarin",        "91-64-5",    (0.97, 0.97, 0.95), 0.70),
    ("Musk Ketone",     "81-14-1",    (0.93, 0.90, 0.62), 0.45),
    ("Ambroxan",        "6790-58-5",  (0.99, 0.99, 0.98), 0.50),
    ("Benzoin Resinoid","9000-05-9",  (0.72, 0.48, 0.20), 0.40),
]
CAP_COLOURS = {"white": (0.92, 0.92, 0.90), "blue": (0.05, 0.22, 0.60), "black": (0.02, 0.02, 0.02)}
MM = 0.001

# ----------------------------------------------------------------------------- helpers
def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)

def new_collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col

def mesh_object(name, bm, col, mat=None, smooth=True):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    col.objects.link(ob)
    if mat: ob.data.materials.append(mat)
    return ob

def lathe(profile, segments=64, knurl=None, angle=2 * math.pi, close=True):
    """profile: list of (r, z). Returns a bmesh of the surface of revolution.
    knurl: (amplitude, count, zmin, zmax) radial ripple applied between zmin..zmax."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    rings = []
    steps = segments if close else segments + 1
    for i in range(steps):
        a = angle * i / segments
        ring = []
        for (r, z) in profile:
            rr = r
            if knurl and r > 0 and knurl[2] <= z <= knurl[3]:
                rr = r * (1 + knurl[0] * math.sin(knurl[1] * a))
            ring.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a), z)))
        rings.append(ring)
    bm.verts.ensure_lookup_table()
    n = len(profile)
    for i in range(segments):
        a, b = rings[i], rings[(i + 1) % steps]
        for j in range(n - 1):
            try:
                f = bm.faces.new((a[j], b[j], b[j + 1], a[j + 1]))
            except ValueError:
                continue
            u0, u1 = i / segments, (i + 1) / segments
            for l, (u, v) in zip(f.loops, ((u0, j / (n - 1)), (u1, j / (n - 1)), (u1, (j + 1) / (n - 1)), (u0, (j + 1) / (n - 1)))):
                l[uv].uv = (u, v)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm

def arc(cx, cz, r, a0, a1, n):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cz + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def displace_top(ob, z_top, amp, scale, tol=1e-5):
    me = ob.data
    for v in me.vertices:
        if v.co.z >= z_top - tol:
            p = Vector((v.co.x * scale, v.co.y * scale, 0))
            n1 = noise.noise(p) * amp
            n2 = noise.noise(p * 3.1 + Vector((7, 3, 0))) * amp * 0.35
            v.co.z += n1 + n2
    me.update()

def principled(name, base, rough=0.5, metallic=0.0, transmission=0.0, ior=1.45, alpha=1.0,
               sheen=0.0, specular=0.5, image=None, normal_image=None, normal_scale=8.0, normal_strength=0.8):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*base, 1)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["IOR"].default_value = ior
    bsdf.inputs["Alpha"].default_value = alpha
    bsdf.inputs["Sheen Weight"].default_value = sheen
    bsdf.inputs["Specular IOR Level"].default_value = specular
    if transmission:
        bsdf.inputs["Transmission Weight"].default_value = transmission
        m.surface_render_method = "BLENDED" if hasattr(m, "surface_render_method") else None
    if image:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = image
        tex.location = (-400, 300)
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    if normal_image:
        tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-1000, -200)
        mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-800, -200)
        mp.inputs["Scale"].default_value = (normal_scale, normal_scale, 1)
        tex = nt.nodes.new("ShaderNodeTexImage"); tex.location = (-600, -200)
        tex.image = normal_image; tex.image.colorspace_settings.name = "Non-Color"
        nm = nt.nodes.new("ShaderNodeNormalMap"); nm.location = (-300, -200)
        nm.inputs["Strength"].default_value = normal_strength
        nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], tex.inputs["Vector"])
        nt.links.new(tex.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    return m

def make_grain_normal(path, size=256, seed=3):
    """Tileable fine-grain normal map for powders (numpy noise -> height -> normals)."""
    import numpy as np
    from PIL import Image
    rng = np.random.default_rng(seed)
    h = np.zeros((size, size))
    for octave, amp in ((1, 0.15), (2, 0.25), (4, 0.6), (8, 1.0)):
        n = rng.random((size, size))
        k = max(1, size // (32 * octave))
        if k > 1:                                       # box blur with wrap-around keeps it tileable
            for ax in (0, 1):
                n = sum(np.roll(n, o, axis=ax) for o in range(-k, k + 1)) / (2 * k + 1)
        h += amp * n
    h = (h - h.min()) / (h.max() - h.min())
    dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 6.0
    dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 6.0
    nz = np.ones_like(h)
    norm = np.sqrt(dx * dx + dy * dy + nz * nz)
    rgb = np.stack([(-dx / norm + 1) / 2, (dy / norm + 1) / 2, (nz / norm + 1) / 2], -1)
    Image.fromarray((rgb * 255).astype(np.uint8)).save(path)
    img = bpy.data.images.load(path); img.pack()
    return img

# ----------------------------------------------------------------------------- label textures
def make_label_png(name, cas, path, w=1024, h=512):
    from PIL import Image, ImageDraw, ImageFont
    fdir = "/usr/share/fonts/truetype/dejavu/"
    def font(f, s):
        try: return ImageFont.truetype(fdir + f, s)
        except Exception: return ImageFont.load_default()
    im = Image.new("RGB", (w, h), (250, 249, 245))
    d = ImageDraw.Draw(im)
    d.rectangle([12, 12, w - 13, h - 13], outline=(40, 40, 40), width=6)
    d.rectangle([12, 12, w - 13, 120], fill=(30, 30, 30))
    d.text((40, 34), "PERFUMERY LAB  ·  RAW MATERIAL", font=font("DejaVuSans-Bold.ttf", 44), fill=(250, 249, 245))
    fs = 120 if len(name) < 12 else 88
    d.text((40, 150), name.upper(), font=font("DejaVuSans-Bold.ttf", fs), fill=(20, 20, 20))
    d.text((40, 300), f"CAS {cas}", font=font("DejaVuSansMono.ttf", 52), fill=(60, 60, 60))
    d.text((40, 370), "Powder · ≥ 99 %  ·  Store cool & dry, tightly closed", font=font("DejaVuSans.ttf", 36), fill=(60, 60, 60))
    d.line([40, 430, w - 40, 430], fill=(40, 40, 40), width=4)
    d.text((40, 445), "Net wt. —— g     Lot ——————     Exp ——/————", font=font("DejaVuSansMono.ttf", 34), fill=(60, 60, 60))
    im.save(path)
    img = bpy.data.images.load(path)
    img.pack()
    return img

# ----------------------------------------------------------------------------- materials
MAT = {}
def build_materials():
    MAT["HDPE"] = principled("HDPE_White", (0.93, 0.93, 0.91), rough=0.55, specular=0.35, sheen=0.1)
    MAT["PET"] = principled("PET_Clear", (1, 1, 1), rough=0.06, transmission=1.0, ior=1.57, specular=0.5)
    for k, c in CAP_COLOURS.items():
        MAT["cap_" + k] = principled(f"Cap_PP_{k.capitalize()}", c, rough=0.4, specular=0.45)
    MAT["steel"] = principled("Stainless_Steel", (0.8, 0.8, 0.8), rough=0.28, metallic=1.0)
    MAT["polystyrene"] = principled("Polystyrene_White", (0.97, 0.97, 0.97), rough=0.25, specular=0.5)
    grain = make_grain_normal(os.path.join(OUT, "labels", "powder_grain_normal.png"))
    for (name, cas, rgb, _) in POWDERS:
        key = name.lower().replace(" ", "_")
        MAT["powder_" + key] = principled("Powder_" + name.replace(" ", ""), rgb, rough=0.9, specular=0.2, sheen=0.3,
                                          normal_image=grain, normal_scale=6.0, normal_strength=1.0)
        img = make_label_png(name, cas, os.path.join(OUT, "labels", key + ".png"))
        MAT["label_" + key] = principled("Label_" + name.replace(" ", ""), (1, 1, 1), rough=0.6, specular=0.3, image=img)

# ----------------------------------------------------------------------------- jar parts
def jar_profile(R, H, t=1.4 * MM, bevel=2.5 * MM):
    Rn = R * 0.82                  # neck outer radius (wide mouth)
    sh = R - Rn                    # shoulder radius
    Hs = H - (sh + 9 * MM)         # shoulder start; neck is 9 mm tall
    p = [(0, 0)]
    p += arc(R - bevel, bevel, bevel, -90, 0, 5)            # bottom bevel -> outer wall
    p += [(R, Hs)]
    p += arc(Rn, Hs, sh, 0, 90, 6)[1:]                      # outer shoulder (quarter round) -> (Rn, Hs+sh)
    p += [(Rn, H - 0.6 * MM), (Rn - 0.6 * MM, H), (Rn - t, H)]   # rim
    p += [(Rn - t, Hs + sh)]                                # inner neck
    p += arc(Rn, Hs, sh - t, 90, 0, 6)[1:]                  # inner shoulder -> (R - t, Hs)
    p += [(R - t, t + bevel)]
    p += arc(R - bevel, t + bevel, bevel - t, 0, -90, 4)[1:]  # inner bottom bevel
    p += [(0, t)]
    return p, Rn, Hs + sh

def make_jar(name, D, H, cap_colour, powder, clear):
    col = new_collection(name)
    R = D * 0.5 * MM; Hm = H * MM
    prof, Rn, Hn = jar_profile(R, Hm)
    body = mesh_object(name + "_Body", lathe(prof, 72), col, MAT["PET" if clear else "HDPE"])
    # cap: cup with knurled grip
    tc = 1.6 * MM; Hc = 11 * MM; Rc = Rn + 2.2 * MM; b = 1.6 * MM
    cp = [(0, Hc)] + arc(Rc - b, Hc - b, b, 90, 0, 5) + [(Rc, 0), (Rc - tc, 0), (Rc - tc, Hc - tc), (0, Hc - tc)]
    cap = mesh_object(name + "_Cap", lathe(cp, 96, knurl=(0.02, 36, 0.5 * MM, Hc - 2 * MM)), col, MAT["cap_" + cap_colour])
    cap.location.z = Hm + 1.5 * MM - Hc
    # powder fill: solid cylinder with a noisy top
    pname, cas, rgb, fill = powder
    key = pname.lower().replace(" ", "_")
    Ri = R - 1.4 * MM - 0.3 * MM
    zf = max(8 * MM, Hn * fill)
    pp = [(0, 1.6 * MM), (Ri, 1.6 * MM), (Ri, zf)] + [(Ri * (1 - i / 12), zf) for i in range(1, 13)]
    pw = mesh_object(name + "_Powder", lathe(pp, 72), col, MAT["powder_" + key])
    displace_top(pw, zf, 1.2 * MM, 1 / (R * 0.5))
    if not clear:
        pw.hide_render = False   # still exported; visible when the cap is removed
    # label: partial cylinder wrapped ~200°, UVs u=angle v=height
    lab = make_label(name + "_Label", R + 0.25 * MM, 9 * MM, Hm - 18 * MM, MAT["label_" + key], col)
    for o in (cap, pw, lab):
        o.parent = body
        o.matrix_parent_inverse = body.matrix_world.inverted()
    body["asset"] = name; body["capacity_ml"] = int(name.split("_")[1][:-2]); body["material"] = "PET" if clear else "HDPE"
    body["powder"] = pname; body["powder_cas"] = cas
    return col, body

def make_label(name, r, z0, z1, mat, col, span_deg=200, seg=40):
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    a0 = math.radians(-90 - span_deg / 2)
    rows = []
    for i in range(seg + 1):
        a = a0 + math.radians(span_deg) * i / seg
        rows.append((bm.verts.new((r * math.cos(a), r * math.sin(a), z0)),
                     bm.verts.new((r * math.cos(a), r * math.sin(a), z1)), i / seg))
    for i in range(seg):
        (v0, v1, u0), (w0, w1, u1) = rows[i], rows[i + 1]
        f = bm.faces.new((v0, w0, w1, v1))
        # label reads left→right when viewed from the front (−Y)
        for l, (u, v) in zip(f.loops, ((u0, 0), (u1, 0), (u1, 1), (u0, 1))):
            l[uv].uv = (u, v)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = mesh_object(name, bm, col, mat)
    return ob

# ----------------------------------------------------------------------------- loose powder, weigh boat, spatula
def make_powder_pile(name, powder, radius=18 * MM, height=9 * MM):
    col = new_collection(name)
    pname, cas, rgb, _ = powder
    key = pname.lower().replace(" ", "_")
    height = radius * 0.72                      # tan(36°) — typical angle of repose of a fine powder
    n = 36
    prof = [(radius * 1.04, 0)]
    for i in range(n + 1):
        f = i / n                                  # 0 at base, 1 at apex
        r = radius * (1 - f)
        z = height * (f ** 1.15) * (1 - 0.12 * (1 - f) ** 4)     # cone, slightly concave flank, soft apex
        prof.append((r, z + 1e-6))
    ob = mesh_object(name, lathe(prof, 96), col, MAT["powder_" + key])
    me = ob.data
    for v in me.vertices:
        if v.co.z > 1e-4:
            p = Vector((v.co.x, v.co.y, v.co.z)) * 140
            fade = min(1.0, v.co.z / (2 * MM))
            v.co.z += (noise.noise(p) * 0.45 * MM + noise.noise(p * 2.3) * 0.25 * MM) * fade
            j = 1 + noise.noise(p * 0.5 + Vector((3, 3, 3))) * 0.05
            v.co.x *= j; v.co.y *= j
    me.update()
    ob["asset"] = name; ob["powder"] = pname; ob["powder_cas"] = cas
    return col, ob

def make_weigh_boat(name, size=45 * MM, height=8 * MM, t=0.4 * MM):
    col = new_collection(name)
    bm = bmesh.new()
    def square(s, z, corner=0.3):
        # rounded square outline
        pts = []
        h = s / 2; c = s * corner * 0.5
        segs = [((h - c, -h), (h - c, -h + c), 0, 8, -90, 0), ((h, h - c), (h - c, h - c), 0, 8, 0, 90),
                ((-h + c, h), (-h + c, h - c), 0, 8, 90, 180), ((-h, -h + c), (-h + c, -h + c), 0, 8, 180, 270)]
        for (_, ctr, _, n, a0, a1) in segs:
            for i in range(n):
                a = math.radians(a0 + (a1 - a0) * i / n)
                pts.append(bm.verts.new((ctr[0] + c * math.cos(a), ctr[1] + c * math.sin(a), z)))
        return pts
    inner_b = square(size * 0.62, 0)
    outer_t = square(size, height)
    n = len(inner_b)
    bm.faces.new(inner_b)
    for i in range(n):
        bm.faces.new((inner_b[i], inner_b[(i + 1) % n], outer_t[(i + 1) % n], outer_t[i]))
    # pour spout: pull one corner up slightly
    for v in outer_t[6:10]:
        v.co.z += 2 * MM; v.co.x *= 1.06; v.co.y *= 1.06
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, t))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if sum(f.normal.z for f in bm.faces) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)   # normals point up / into the dish
    ob = mesh_object(name, bm, col, MAT["polystyrene"])
    sol = ob.modifiers.new("Solidify", "SOLIDIFY"); sol.thickness = t; sol.offset = -1
    ob["asset"] = name
    return col, ob

def make_spatula(name, length=180 * MM):
    col = new_collection(name)
    # handle: rounded rod along +X
    r = 1.8 * MM
    bm = lathe([(0, 0), (r, 0), (r, length * 0.72), (0, length * 0.72)], 24)
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=__import__("mathutils").Matrix.Rotation(math.radians(90), 3, "Y"))
    bmesh.ops.translate(bm, verts=bm.verts, vec=(length * 0.14, 0, r))
    handle = mesh_object(name + "_Handle", bm, col, MAT["steel"])
    # flat blade end
    bmb = bmesh.new()
    bmesh.ops.create_cube(bmb, size=1.0)
    bmesh.ops.scale(bmb, verts=bmb.verts, vec=(length * 0.16, 7 * MM, 0.8 * MM))
    bmesh.ops.translate(bmb, verts=bmb.verts, vec=(length * 0.07, 0, r))
    blade = mesh_object(name + "_Blade", bmb, col, MAT["steel"], smooth=False)
    bev = blade.modifiers.new("Bevel", "BEVEL"); bev.width = 0.35 * MM; bev.segments = 3
    # scoop end: half ellipsoid shell
    bms = bmesh.new()
    bmesh.ops.create_uvsphere(bms, u_segments=32, v_segments=16, radius=1.0)
    bmesh.ops.delete(bms, geom=[v for v in bms.verts if v.co.z > 0.05], context="VERTS")
    bmesh.ops.scale(bms, verts=bms.verts, vec=(14 * MM, 6 * MM, 3.5 * MM))
    bmesh.ops.translate(bms, verts=bms.verts, vec=(length * 0.86 + 6 * MM, 0, 3.5 * MM + r))
    scoop = mesh_object(name + "_Scoop", bms, col, MAT["steel"])
    sol = scoop.modifiers.new("Solidify", "SOLIDIFY"); sol.thickness = 0.5 * MM
    for o in (blade, scoop):
        o.parent = handle; o.matrix_parent_inverse = handle.matrix_world.inverted()
    handle["asset"] = name
    return col, handle

# ----------------------------------------------------------------------------- export
def export_collection(col, path):
    bpy.ops.object.select_all(action="DESELECT")
    for o in col.all_objects: o.select_set(True)
    bpy.context.view_layer.objects.active = col.all_objects[0]
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True,
                              export_apply=True, export_yup=True, export_materials="EXPORT",
                              export_image_format="AUTO", export_extras=True)

def render_preview(assets, path):
    sc = bpy.context.scene
    # floor
    bpy.ops.mesh.primitive_plane_add(size=3)
    floor = bpy.context.object; floor.name = "Preview_Floor"
    floor.data.materials.append(principled("Bench_Grey", (0.35, 0.36, 0.37), rough=0.35))
    # lay the assets out in two rows: HDPE jars in front, everything else behind
    rows = [[a for a in assets if a[0].name.endswith("_hdpe")],
            [a for a in assets if a[0].name.endswith("_pet")],
            [a for a in assets if not a[0].name.startswith("jar_")]]
    for y, row in zip((0.0, 0.16, 0.30), rows):
        width = sum(max(o.dimensions.x for o in col.all_objects) for col, _ in row) + 0.02 * (len(row) - 1)
        x = -width / 2
        for (col, root) in row:
            w = max(o.dimensions.x for o in col.all_objects)
            root.location.x = x + w / 2 - (min(o.bound_box[0][0] for o in col.all_objects) + w / 2 if "spatula" in col.name else 0)
            root.location.y = y
            x += w + 0.02
    # camera + light
    cam = bpy.data.objects.new("Preview_Cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam); sc.camera = cam
    cam.location = (0.0, -0.70, 0.62); cam.rotation_euler = (math.radians(50), 0, 0)
    cam.data.lens = 40
    sun = bpy.data.objects.new("Preview_Sun", bpy.data.lights.new("sun", "SUN"))
    sc.collection.objects.link(sun); sun.rotation_euler = (math.radians(45), math.radians(15), math.radians(30))
    sun.data.energy = 3.0
    world = bpy.data.worlds.new("World"); sc.world = world; world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.7, 0.75, 0.8, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    sc.render.engine = "CYCLES"; sc.cycles.samples = 48; sc.cycles.use_denoising = False
    sc.cycles.device = "CPU"
    sc.render.resolution_x = 1600; sc.render.resolution_y = 800
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    for o in (cam, sun, floor): bpy.data.objects.remove(o)

# ----------------------------------------------------------------------------- main
def main():
    clear_scene()
    build_materials()
    assets = []
    for i, (sz, D, H, capc) in enumerate(JAR_SIZES):
        assets.append(make_jar(f"jar_{sz}_hdpe", D, H, capc, POWDERS[i % len(POWDERS)], clear=False))
    for i, (sz, D, H, capc) in enumerate(JAR_SIZES[:4]):
        assets.append(make_jar(f"jar_{sz}_pet", D, H, capc, POWDERS[(i + 3) % len(POWDERS)], clear=True))
    assets.append(make_powder_pile("powder_pile_vanillin", POWDERS[0]))
    assets.append(make_powder_pile("powder_pile_benzoin", POWDERS[5], radius=14 * MM, height=7 * MM))
    assets.append(make_weigh_boat("weigh_boat_45mm"))
    assets.append(make_spatula("micro_spatula_180mm"))
    for (col, root) in assets:
        export_collection(col, os.path.join(OUT, "glb", col.name + ".glb"))
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "reagent_jars_kit.glb"), export_format="GLB",
                              export_apply=True, export_yup=True, export_extras=True)
    render_preview(assets, os.path.join(OUT, "preview.png"))
    for (col, root) in assets: root.location = (0, 0, 0)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "reagent_jars_kit.blend"), compress=True)
    print("DONE", OUT)

main()
