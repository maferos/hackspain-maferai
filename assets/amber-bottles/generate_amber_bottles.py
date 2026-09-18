"""
generate_amber_bottles.py  —  Blender 4.2+ / 5.x
=================================================
Genera frascos redondos de vidrio ámbar (referencia: 60 ml, Ø40 x 95 mm, cuello PP 25 mm)
y su tapón blanco de PP estriado con anillo precinto (tamper-evident), escalados
"racionalmente" a 10 / 20 / 30 / 50 / 60 / 100 ml.

Regla de escalado
-----------------
* Cuerpo: escala uniforme k = (V / 60)^(1/3)   →  Ø = 40·k ,  H = 95·k
  (con esto el volumen del cuerpo crece linealmente con la capacidad nominal;
  los resultados coinciden ±1 mm con los frascos reales de farmacia).
* Cuello: NO se escala de forma continua, se ajusta a una boca PP estándar
  (18 / 20 / 25 / 28 mm) según la tabla NECK_FOR_ML. El tapón se deriva del cuello.

Uso
---
    blender -b -P generate_amber_bottles.py -- --out ./amber-bottles
    # o con el módulo bpy (pip install bpy):
    python generate_amber_bottles.py --out ./amber-bottles

Salida (en --out):
    amber_bottles_kit.blend      todo, una colección por tamaño
    amber_bottles_kit.glb        todo
    glb/amber_bottle_XXXml.glb   frasco (root, con extras) + tapón (hijo), cerrado
    glb/amber_cap_XXmm.glb       tapón suelto por tamaño de boca

Convenciones: metros, origen en el centro de la base, glTF +Y up.
Extras (custom properties) en el frasco: capacity_ml, neck_mm, height_mm, diameter_mm, material.
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector

# ----------------------------------------------------------------------------
# PARÁMETROS
# ----------------------------------------------------------------------------
REF_ML, REF_DIAM, REF_HEIGHT, REF_NECK = 60.0, 40.0, 95.0, 25.0   # mm
SIZES = [10, 20, 30, 50, 60, 100]
NECK_FOR_ML = {10: 18, 20: 18, 30: 20, 50: 25, 60: 25, 100: 28}   # boca PP (mm)

BOTTLE_SEGS = 96          # segmentos radiales del frasco
RIBS = 36                 # costillas del tapón (30–40)
SEGS_PER_RIB = 4          # 4 → costilla cuadrada (2 cresta + 2 valle)
RIB_DEPTH = 0.5           # mm
THREAD_TURNS = 2.0
LAYOUT_GAP = 0.03         # m, separación entre tamaños en la escena

MM = 0.001


# ----------------------------------------------------------------------------
# GEOMETRÍA AUXILIAR
# ----------------------------------------------------------------------------
def arc(cx, cz, rad, a0, a1, n):
    """Puntos (r,z) de un arco de a0 a a1 grados, sin el punto inicial."""
    return [(cx + rad * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cz + rad * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(1, n + 1)]


def lathe(bm, profile, segs, mod=None):
    """
    Revoluciona un perfil abierto [(r, z, tag), ...] (mm) alrededor de Z.
    Los puntos con r≈0 se convierten en un único vértice (tapa/fondo).
    mod(row_index, tag, seg_index) -> incremento radial (mm) para estriados.
    Devuelve lista de filas (cada fila = lista de BMVerts).
    """
    rows = []
    for i, (r, z, tag) in enumerate(profile):
        if r < 1e-6:
            rows.append([bm.verts.new((0.0, 0.0, z * MM))])
            continue
        ring = []
        for j in range(segs):
            a = 2 * math.pi * j / segs
            rr = r + (mod(i, tag, j) if mod else 0.0)
            ring.append(bm.verts.new((rr * math.cos(a) * MM, rr * math.sin(a) * MM, z * MM)))
        rows.append(ring)
    for a, b in zip(rows, rows[1:]):
        if len(a) == 1 and len(b) == 1:
            continue
        if len(a) == 1:
            for j in range(segs):
                bm.faces.new((a[0], b[j], b[(j + 1) % segs]))
        elif len(b) == 1:
            for j in range(segs):
                bm.faces.new((a[j], a[(j + 1) % segs], b[0]))
        else:
            for j in range(segs):
                bm.faces.new((a[j], a[(j + 1) % segs], b[(j + 1) % segs], b[j]))
    return rows


def helix_thread(bm, r_root, pitch, turns, z0, depth, width, segs_per_turn=48):
    """
    Rosca: perfil trapezoidal barrido por una hélice. La altura del filete se
    atenúa en la primera y última media vuelta para fundirse con el cuello.
    r_root: radio del cuello (mm); z0: z (mm) del inicio de la hélice.
    """
    emb = 0.25  # cuánto se hunde el perfil dentro del cuello (evita huecos)
    prof = [(-emb, -width / 2), (depth, -width * 0.18), (depth, width * 0.18), (-emb, width / 2)]
    n = int(turns * segs_per_turn)
    rings = []
    for s in range(n + 1):
        t = s / segs_per_turn                    # vueltas recorridas
        th = 2 * math.pi * t
        fade = min(1.0, t / 0.5, (turns - t) / 0.5)
        fade = max(fade, 0.0)
        z = z0 + pitch * t
        ring = []
        for (u, v) in prof:
            rr = r_root + (u if u < 0 else u * fade)
            ring.append(bm.verts.new((rr * math.cos(th) * MM, rr * math.sin(th) * MM, (z + v) * MM)))
        rings.append(ring)
    m = len(prof)
    for a, b in zip(rings, rings[1:]):
        for k in range(m):
            bm.faces.new((a[k], b[k], b[(k + 1) % m], a[(k + 1) % m]))
    bm.faces.new(rings[0][::-1])
    bm.faces.new(rings[-1])


def finish_mesh(bm, name, sharp_rows=(), sharp_vertical_rows=(), rows=None):
    """Convierte bmesh en objeto, normales fuera, suavizado + aristas marcadas."""
    if rows:
        def mark(a, b):
            e = bm.edges.get((a, b))
            if e:
                e.smooth = False
        for ri in sharp_rows:                       # aristas horizontales (anillos)
            ring = rows[ri]
            if len(ring) > 1:
                for j in range(len(ring)):
                    mark(ring[j], ring[(j + 1) % len(ring)])
        for ri in sharp_vertical_rows:              # aristas verticales (costillas)
            a, b = rows[ri], rows[ri + 1]
            if len(a) == len(b) and len(a) > 1:
                for j in range(len(a)):
                    mark(a[j], b[j])
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for f in bm.faces:
        f.smooth = True
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.update()
    return bpy.data.objects.new(name, me)


# ----------------------------------------------------------------------------
# DIMENSIONES POR TAMAÑO
# ----------------------------------------------------------------------------
def bottle_dims(ml):
    k = (ml / REF_ML) ** (1.0 / 3.0)
    N = NECK_FOR_ML[ml]
    d = dict(ml=ml, k=k, N=N,
             R=REF_DIAM * k / 2,            # radio cuerpo
             H=REF_HEIGHT * k,              # altura total sin tapón
             w=1.2 + 0.8 * k,               # espesor pared
             tb=2.5 * k,                    # espesor fondo
             pu=1.0 * k,                    # push-up del fondo
             fb=3.0 * k,                    # radio del canto de la base
             # cuello (función de la boca PP)
             rt=N / 2 - 0.3,                # radio cresta rosca
             rn=N / 2 - 0.3 - 0.04 * N,     # radio raíz cuello
             rb=N / 2 - 0.3 - 0.04 * N - 2.0,  # radio interior boca
             hf=0.55 * N + 1.0,             # altura del terminado (labio→cordón)
             hb=0.10 * N,                   # altura zona cordón precinto
             pitch=0.11 * N,
             tdepth=0.04 * N)
    d['hs'] = 0.30 * d['R'] * 2            # altura hombro
    return d


def cap_dims(N):
    rv = N / 2 + 1.5 - RIB_DEPTH           # radio valle (zona estriada)
    return dict(N=N, rv=rv, rc=rv + RIB_DEPTH,
                Hc=0.62 * N + 3.0,          # altura total
                hband=(0.62 * N + 3.0) * 0.22,  # anillo precinto
                hg=0.8, gdepth=0.6,         # ranura
                ch=0.8,                     # chaflán superior
                tt=1.6,                     # espesor de la tapa
                ri=N / 2 - 0.3 + 0.35)      # radio interior (holgura sobre la rosca)


# ----------------------------------------------------------------------------
# FRASCO
# ----------------------------------------------------------------------------
def make_bottle(d):
    R, H, w, tb, pu, fb = d['R'], d['H'], d['w'], d['tb'], d['pu'], d['fb']
    rt, rn, rb, hf, hb, hs = d['rt'], d['rn'], d['rb'], d['hf'], d['hb'], d['hs']
    zs = H - hf - hb - hs                  # inicio del hombro
    zn = zs + hs                           # inicio del cuello (base del cordón)
    P = []
    T = lambda pts, tag='': [(r, z, tag) for r, z in pts]
    # --- exterior, de abajo arriba
    P += T([(0, pu), (R - fb - 1.0, 0.25), (R - fb, 0.0)])
    P += T(arc(R - fb, fb, fb, -90, 0, 6))
    P += T([(R, zs)], 'body')
    for i in range(1, 13):                 # hombro en S (cos-blend)
        t = i / 12
        P.append((rn + (R - rn) * (1 + math.cos(math.pi * t)) / 2, zs + hs * t, 'shoulder'))
    # cordón precinto (bead) — trapecio
    z0 = zn + 0.3
    P += T([(rn, z0), (rt + 0.25, z0 + 0.35), (rt + 0.25, z0 + hb - 0.35), (rn, z0 + hb)], 'bead')
    # cuello + labio
    P += T([(rn, H - 0.5), (rn - 0.45, H), (rb + 0.35, H), (rb, H - 0.35)], 'lip')
    # --- interior, de arriba abajo
    P += T([(rb, zn + w)], 'bore')
    Ri = R - w
    for i in range(11, -1, -1):
        t = i / 12
        P.append((rb + (Ri - rb) * (1 + math.cos(math.pi * t)) / 2, zs - w * 0.6 + (hs + w * 0.6) * t, 'ishoulder'))
    fi = 1.5 * d['k']
    P += T([(Ri, tb + fi)])
    P += T(arc(Ri - fi, tb + fi, fi, 0, -90, 5))
    P += T([(Ri - fi - 1.0, tb + 0.15), (0, tb + pu * 0.6)])

    bm = bmesh.new()
    rows = lathe(bm, P, BOTTLE_SEGS)
    sharp = [i for i, p in enumerate(P) if p[2] == 'bead' or p[2] == 'lip']
    # rosca
    zthr = H - 1.6 - THREAD_TURNS * d['pitch']
    helix_thread(bm, rn, d['pitch'], THREAD_TURNS, zthr, d['tdepth'], d['pitch'] * 0.62)
    ob = finish_mesh(bm, f"Bottle_{d['ml']:03d}ml", sharp_rows=sharp, rows=rows)
    ob['capacity_ml'] = d['ml']
    ob['neck_mm'] = d['N']
    ob['height_mm'] = round(H, 1)
    ob['diameter_mm'] = round(2 * R, 1)
    ob['material'] = 'amber glass type III'
    ob['cap_z_mm'] = round(H - (cap_dims(d['N'])['Hc'] - cap_dims(d['N'])['tt']), 2)
    return ob


# ----------------------------------------------------------------------------
# TAPÓN
# ----------------------------------------------------------------------------
def make_cap(N):
    c = cap_dims(N)
    rv, rc, Hc, hband, hg, gd, ch, tt, ri = (c[k] for k in ('rv', 'rc', 'Hc', 'hband', 'hg', 'gdepth', 'ch', 'tt', 'ri'))
    rband = rc + 0.4                       # el precinto es algo más ancho que el estriado
    zg = hband + hg                        # techo de la ranura
    P = [
        (0, Hc, ''),
        (rv - ch, Hc, 'top'),
        (rv, Hc - ch, 'topedge'),
        (rv, Hc - ch - 1.0, 'ribstart'),   # franja lisa fina bajo el chaflán
        (rv, Hc - ch - 1.35, 'rib'),
        (rv, zg + 0.35, 'rib'),
        (rv, zg, 'ribend'),
        (rv - gd, zg, 'groove'),           # ranura fina
        (rv - gd, hband, 'groove'),
        (rband, hband, 'band'),            # anillo precinto liso
        (rband, 0.5, 'band'),
        (rband - 0.5, 0.0, 'bandbot'),
        (ri, 0.0, 'inner'),
        (ri, Hc - tt, 'inner'),
        (0, Hc - tt, ''),
    ]
    segs = RIBS * SEGS_PER_RIB
    half = SEGS_PER_RIB // 2

    def mod(i, tag, j):
        if tag != 'rib':
            return 0.0
        return RIB_DEPTH if (j % SEGS_PER_RIB) < half else 0.0

    bm = bmesh.new()
    rows = lathe(bm, P, segs, mod)
    sharp_rows = [i for i, p in enumerate(P) if p[2] in ('groove', 'band', 'bandbot', 'inner')]
    sharp_v = [i for i, p in enumerate(P) if p[2] == 'rib'][:-1]
    ob = finish_mesh(bm, f"Cap_PP{N}", sharp_rows=sharp_rows, sharp_vertical_rows=sharp_v, rows=rows)
    ob['neck_mm'] = N
    ob['height_mm'] = round(Hc, 1)
    ob['diameter_mm'] = round(2 * rband, 1)
    ob['material'] = 'white PP, ribbed, tamper-evident band'
    return ob


# ----------------------------------------------------------------------------
# MATERIALES
# ----------------------------------------------------------------------------
def _set(node, names, value):
    for n in names:
        if n in node.inputs:
            node.inputs[n].default_value = value
            return


def mat_amber():
    if 'Amber_Glass' in bpy.data.materials:
        return bpy.data.materials['Amber_Glass']
    m = bpy.data.materials.new('Amber_Glass')
    if not m.use_nodes:
        m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes['Principled BSDF']
    _set(p, ['Base Color'], (0.62, 0.28, 0.05, 1.0))
    _set(p, ['Roughness'], 0.05)
    _set(p, ['IOR'], 1.52)
    _set(p, ['Transmission Weight', 'Transmission'], 1.0)
    va = nt.nodes.new('ShaderNodeVolumeAbsorption')
    va.inputs['Color'].default_value = (0.85, 0.40, 0.06, 1.0)
    va.inputs['Density'].default_value = 250.0
    out = nt.nodes['Material Output']
    nt.links.new(va.outputs['Volume'], out.inputs['Volume'])
    for attr, val in (('blend_method', 'BLEND'), ('surface_render_method', 'BLENDED')):
        try:
            setattr(m, attr, val)
        except Exception:
            pass
    return m


def mat_white_pp():
    if 'White_PP' in bpy.data.materials:
        return bpy.data.materials['White_PP']
    m = bpy.data.materials.new('White_PP')
    if not m.use_nodes:
        m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    _set(p, ['Base Color'], (0.93, 0.93, 0.91, 1.0))
    _set(p, ['Roughness'], 0.32)
    _set(p, ['IOR'], 1.49)
    _set(p, ['Specular IOR Level', 'Specular'], 0.5)
    return m


# ----------------------------------------------------------------------------
# ESCENA + EXPORT
# ----------------------------------------------------------------------------
def export_glb(objs, path):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    kw = dict(filepath=path, export_format='GLB', use_selection=True,
              export_apply=True, export_extras=True, export_yup=True)
    try:
        bpy.ops.export_scene.gltf(**kw)
    except TypeError:
        kw.pop('export_yup', None)
        bpy.ops.export_scene.gltf(**kw)


def main(out_dir):
    os.makedirs(os.path.join(out_dir, 'glb'), exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.length_unit = 'MILLIMETERS'
    amber, white = mat_amber(), mat_white_pp()

    all_objs, x = [], 0.0
    caps_done = {}
    for ml in SIZES:
        d = bottle_dims(ml)
        col = bpy.data.collections.new(f"Amber_{ml:03d}ml")
        scene.collection.children.link(col)

        bottle = make_bottle(d)
        bottle.data.materials.append(amber)
        cap = make_cap(d['N'])
        cap.name = f"Cap_{ml:03d}ml_PP{d['N']}"
        cap.data.materials.append(white)
        col.objects.link(bottle)
        col.objects.link(cap)
        cap.parent = bottle
        cap.location = (0, 0, bottle['cap_z_mm'] * MM)

        # export en el origen, después se coloca en la escena
        export_glb([bottle, cap], os.path.join(out_dir, 'glb', f"amber_bottle_{ml:03d}ml.glb"))
        if d['N'] not in caps_done:
            solo = make_cap(d['N'])
            solo.data.materials.append(white)
            scene.collection.objects.link(solo)
            export_glb([solo], os.path.join(out_dir, 'glb', f"amber_cap_PP{d['N']}.glb"))
            bpy.data.objects.remove(solo)
            caps_done[d['N']] = True

        bottle.location.x = x + d['R'] * MM
        x += 2 * d['R'] * MM + LAYOUT_GAP
        all_objs += [bottle, cap]
        print(f"{ml:4d} ml  Ø{2*d['R']:5.1f} x {d['H']:5.1f} mm  cuello PP{d['N']}  "
              f"tapón Ø{cap['diameter_mm']} x {cap['height_mm']} mm")

    export_glb(all_objs, os.path.join(out_dir, 'amber_bottles_kit.glb'))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out_dir, 'amber_bottles_kit.blend'))


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    out = argv[argv.index('--out') + 1] if '--out' in argv else 'amber-bottles'
    main(os.path.abspath(out))
