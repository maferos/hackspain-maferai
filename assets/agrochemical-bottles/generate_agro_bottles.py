import bpy, bmesh, math
from math import sin, cos, pi, radians

import os; OUT = os.path.dirname(os.path.abspath(__file__)) + "/"
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
MM = 0.001


# ---------------------------------------------------------------- helpers
def arc(cx, cz, r, a0, a1, n):
    return [(cx + r * cos(radians(a0 + (a1 - a0) * i / n)),
             cz + r * sin(radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def dedupe(pts):
    out = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > 1e-7:
            out.append(p)
    return out


def lathe(bm, profile, nseg, rfunc=None):
    """Revolve profile [(r,z)...]. Points with r==0 become poles."""
    rings = []
    for i, (r, z) in enumerate(profile):
        if r < 1e-9:
            rings.append([bm.verts.new((0, 0, z))])
        else:
            ring = []
            for k in range(nseg):
                t = 2 * pi * k / nseg
                rr = r + (rfunc(i, k) if rfunc else 0.0)
                ring.append(bm.verts.new((rr * cos(t), rr * sin(t), z)))
            rings.append(ring)
    for a, b in zip(rings[:-1], rings[1:]):
        for k in range(nseg):
            k2 = (k + 1) % nseg
            if len(a) == 1 and len(b) == 1:
                continue
            if len(a) == 1:
                bm.faces.new((a[0], b[k], b[k2]))
            elif len(b) == 1:
                bm.faces.new((a[k], a[k2], b[0]))
            else:
                bm.faces.new((a[k], a[k2], b[k2], b[k]))


def helix_thread(bm, r, z0, pitch, turns, depth, width, steps_per_turn=64, inward=False):
    n = int(turns * steps_per_turn)
    sgn = -1 if inward else 1
    rings = []
    for i in range(n + 1):
        t = 2 * pi * i / steps_per_turn
        z = z0 + pitch * i / steps_per_turn
        u = i / n
        s = min(1.0, u / 0.08, (1 - u) / 0.08)
        s = max(s, 0.02)
        d = depth * s
        r0 = r - sgn * 0.3 * MM  # embedded in wall
        prof = [(r0, z - width / 2), (r + sgn * d, z - width / 5),
                (r + sgn * d, z + width / 5), (r0, z + width / 2)]
        rings.append([bm.verts.new((pr * cos(t), pr * sin(t), pz)) for pr, pz in prof])
    for a, b in zip(rings[:-1], rings[1:]):
        for j in range(3):
            bm.faces.new((a[j], b[j], b[j + 1], a[j + 1]))
    bm.faces.new(rings[0])
    bm.faces.new(rings[-1][::-1])


def finish_mesh(bm, name, sharp_deg=35):
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for f in bm.faces:
        f.smooth = True
    lim = radians(sharp_deg)
    for e in bm.edges:
        if len(e.link_faces) == 2 and e.calc_face_angle(0) > lim:
            e.smooth = False
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    return ob


# ---------------------------------------------------------------- bottle
def bottle_profile(D, Hb, neck_d, wall=0.0):
    """Outer profile (wall=0) or inner profile (offset by wall)."""
    R = D / 2 - wall
    rh = max(0.125 * D - wall, 1 * MM)          # heel radius (~11 mm on 1 L)
    rn = neck_d / 2 - 1.6 * MM - wall           # neck wall radius (under threads)
    Hs = 0.60 * D                               # tall domed shoulder
    pu = 0.03 * D + wall                        # concave push-up
    f = 2.0 * MM + wall                         # shoulder->neck fillet
    z_sh = Hb + Hs - (wall * 0.6)
    p = []
    # bottom: slightly concave with a standing ring
    p += [(0, pu)]
    p += [(x * (R - rh), wall + (pu - wall) * (0.5 + 0.5 * cos(pi * x)) ) for x in
          [i / 12 for i in range(1, 12)]]
    p += arc(R - rh, rh + wall, rh, -90, 0, 14)
    # straight body
    p += [(R, Hb * 0.5), (R, Hb)]
    # semi-ogive shoulder (quarter ellipse, vertical tangent below, horizontal above)
    rs = rn + f
    n = 28
    for i in range(1, n + 1):
        t = (pi / 2) * i / n
        p.append((rs + (R - rs) * cos(t), Hb + (z_sh - Hb) * sin(t)))
    p += arc(rs, z_sh + f, f, -90, -180, 8)
    zc = z_sh + f + 1.5 * MM                     # collar (transfer bead) start
    ch, cw = 3.2 * MM, 3.0 * MM
    if wall == 0:
        p += [(rn, zc)]
        p += arc(rn + cw - 1 * MM, zc + 1 * MM, 1 * MM, -90, 0, 5)
        p += arc(rn + cw - 1 * MM, zc + ch - 1 * MM, 1 * MM, 0, 90, 5)
        p += [(rn, zc + ch)]
    finish_h = max(13 * MM, 0.42 * neck_d)
    ztop = zc + ch + finish_h
    p += [(rn, ztop - (0.6 * MM if wall == 0 else 0))]
    if wall == 0:
        p += arc(rn - 0.6 * MM, ztop - 0.6 * MM, 0.6 * MM, 0, 90, 4)
    else:
        p += [(rn, ztop)]
    info = dict(rn=rn, zc=zc, ch=ch, cw=cw, ztop=ztop, finish_h=finish_h, Hs=Hs)
    return dedupe(p), info


def make_bottle(name, D, Hb, neck_d, wall):
    outer, info = bottle_profile(D, Hb, neck_d, 0)
    inner, _ = bottle_profile(D, Hb, neck_d, wall)
    prof = outer + inner[::-1]                   # outside up, over the lip, inside down
    bm = bmesh.new()
    lathe(bm, prof, 96)
    # neck thread (1.6 turns)
    pitch = 4.2 * MM if neck_d > 35 * MM else 3.2 * MM
    helix_thread(bm, info['rn'], info['zc'] + info['ch'] + 3.0 * MM, pitch, 2.0,
                 1.5 * MM, 2.4 * MM)
    ob = finish_mesh(bm, name)
    # approximate capacity from inner profile (to shoulder top)
    vol = 0
    for (r0, z0), (r1, z1) in zip(inner[:-1], inner[1:]):
        vol += pi * (z1 - z0) * (r0 * r0 + r0 * r1 + r1 * r1) / 3
    return ob, info, vol


# ---------------------------------------------------------------- cap
def make_cap(name, neck_d, info, nribs):
    Ri = neck_d / 2 + 0.5 * MM                  # inner radius (clears threads)
    t = 1.6 * MM
    Rc = Ri + t                                  # ribbed-zone base radius
    Rb = Rc + 1.1 * MM                           # tamper band, slightly wider
    hb = 5.0 * MM                                # band height (covers collar)
    hg = 0.9 * MM                                # groove
    Hc = info['finish_h'] + info['ch'] + 2.5 * MM
    rib_d = 0.9 * MM
    ch = 1.4 * MM                                # top rounding
    prof, tag = [], []

    def add(pts, tg=0):
        for q in pts:
            prof.append(q); tag.append(tg)

    add([(0, Hc - t), (Ri, Hc - t), (Ri, hb + 0.5 * MM), (Ri + 1.0 * MM, hb - 0.3 * MM),
         (Ri + 1.0 * MM, 0.4 * MM), (Ri + 1.4 * MM, 0)])
    add(arc(Rb - 0.5 * MM, 0.5 * MM, 0.5 * MM, -90, 0, 4))
    add(arc(Rb - 0.4 * MM, hb - 0.4 * MM, 0.4 * MM, 0, 90, 4))
    add([(Rc - 0.7 * MM, hb), (Rc - 0.7 * MM, hb + hg), (Rc, hb + hg)])
    z1, z2 = hb + hg + 0.3 * MM, Hc - ch - 0.8 * MM
    add([(Rc, z1)])
    add([(Rc, z1 + 0.9 * MM), (Rc, (z1 + z2) / 2), (Rc, z2 - 0.9 * MM)], 1)   # ribbed
    add([(Rc, z2)])
    add(arc(Rc - ch, Hc - ch, ch, 0, 90, 8))
    add([(0, Hc)])
    seg = 8
    pattern = [1.0, 1.0, 0.55, 0.0, 0.0, 0.0, 0.0, 0.55]   # narrow raised rib
    bm = bmesh.new()
    lathe(bm, prof, nribs * seg, lambda i, k: rib_d * pattern[k % seg] if tag[i] else 0.0)
    # internal thread
    pitch = 4.2 * MM if neck_d > 35 * MM else 3.2 * MM
    helix_thread(bm, Ri, hb + 3.5 * MM, pitch, 1.5, 1.2 * MM, 2.2 * MM, inward=True)
    ob = finish_mesh(bm, name, 30)
    return ob, Hc, Rb


# ---------------------------------------------------------------- materials
def material(name, rough, coat):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.92, 0.92, 0.91, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["IOR"].default_value = 1.52
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = 0.25
    m.diffuse_color = (0.92, 0.92, 0.91, 1)
    return m


hdpe = material("HDPE_blanco_satinado", 0.42, 0.0)
pp = material("PP_blanco_tapon", 0.28, 0.15)

# ---------------------------------------------------------------- build set
#        nombre        D     cuerpo  cuello  pared  estrias
SET = [("Bote_100mL",  46,   50,     28,     1.0,   30),
       ("Bote_250mL",  60,   72,     38,     1.1,   32),
       ("Bote_500mL",  74,   94,     45,     1.2,   34),
       ("Bote_1L",     88,   136,    50,     1.3,   36),
       ("Bote_1L_ancho", 102, 88,    63,     1.3,   40),
       ("Bote_2L",     116,  142,    63,     1.5,   40)]

col_b = bpy.data.collections.new("Botes")
col_c = bpy.data.collections.new("Tapones")
col_s = bpy.data.collections.new("Escena")
for c in (col_b, col_c, col_s):
    scene.collection.children.link(c)

x = 0.0
gap = 35 * MM
total_w = sum(s[1] for s in SET) * MM + gap * (len(SET) - 1)
x = -total_w / 2
maxh = 0
for i, (name, D, Hb, nd, wall, nribs) in enumerate(SET):
    D, Hb, nd, wall = D * MM, Hb * MM, nd * MM, wall * MM
    ob, info, vol = make_bottle(name, D, Hb, nd, wall)
    ob.data.materials.append(hdpe)
    cx = x + D / 2
    ob.location = (cx, 0, 0)
    col_b.objects.link(ob)
    cap, Hc, Rb = make_cap(name.replace("Bote", "Tapon"), nd, info, nribs)
    cap.data.materials.append(pp)
    # cap resting on the floor in front of its bottle, slightly offset
    cap.location = (cx + (0.012 if i % 2 else -0.010), -(D / 2 + Rb + 0.035), 0)
    cap.rotation_euler = (0, 0, radians(17 * i))
    col_c.objects.link(cap)
    maxh = max(maxh, info['ztop'])
    print(f"{name}: D={D*1000:.0f} mm, alto sin tapon={info['ztop']*1000:.0f} mm, "
          f"capacidad a ras ~{vol*1e6:.0f} mL, tapon Ø{Rb*2000:.0f}x{Hc*1000:.0f} mm, "
          f"tris={len(ob.data.polygons)}+{len(cap.data.polygons)}")
    x += D + gap

# ---------------------------------------------------------------- scene
me = bpy.data.meshes.new("Suelo")
bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=3)
bm.to_mesh(me); bm.free()
floor = bpy.data.objects.new("Suelo", me)
fm = bpy.data.materials.new("Suelo_gris")
fm.use_nodes = True
fb = fm.node_tree.nodes["Principled BSDF"]
fb.inputs["Base Color"].default_value = (0.35, 0.36, 0.38, 1)
fb.inputs["Roughness"].default_value = 0.6
me.materials.append(fm)
col_s.objects.link(floor)


def area(name, loc, rot, size, power, sy=None):
    l = bpy.data.lights.new(name, 'AREA')
    l.energy = power
    l.size = size
    if sy:
        l.shape = 'RECTANGLE'; l.size_y = sy
    o = bpy.data.objects.new(name, l)
    o.location = loc
    o.rotation_euler = [radians(a) for a in rot]
    col_s.objects.link(o)
    return o


area("Luz_principal", (-0.9, -0.7, 1.0), (50, 0, -50), 0.5, 9, 1.2)   # tall softbox -> vertical highlights
area("Luz_relleno", (1.0, -0.9, 0.6), (65, 0, 48), 1.0, 2.5)
area("Luz_contra", (0.2, 1.0, 0.9), (-60, 0, 170), 0.8, 5)

cam_d = bpy.data.cameras.new("Camara")
cam_d.lens = 55
cam = bpy.data.objects.new("Camara", cam_d)
cam.location = (0.3, -1.6, 0.5)
col_s.objects.link(cam)
tgt = bpy.data.objects.new("Objetivo", None)
tgt.location = (0, -0.04, 0.105)
col_s.objects.link(tgt)
con = cam.constraints.new('TRACK_TO')
con.target = tgt
scene.camera = cam

w = bpy.data.worlds.new("Mundo")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.57, 0.6, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.35
scene.world = w

scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'MILLIMETERS'
scene.render.engine = 'CYCLES'
scene.cycles.samples = 96
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = 1600, 800
scene.view_settings.view_transform = 'Standard'

import os
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT + "agro_bottles_kit.blend")

# GLB with only bottles + caps
for o in scene.objects:
    o.select_set(o.type == 'MESH' and o.name != "Suelo")
try:
    bpy.ops.export_scene.gltf(filepath=OUT + "agro_bottles_kit.glb", use_selection=True)
except Exception as e:
    print("GLB export failed:", e)

scene.render.filepath = OUT + "preview.png"
bpy.ops.render.render(write_still=True)
