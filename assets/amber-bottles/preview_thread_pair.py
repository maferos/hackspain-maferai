"""Cutaway renders of the threaded pair, straight out of bpy. No Blender app."""
import sys, os, math, bpy, bmesh
sys.path.insert(0, os.path.abspath('assets/amber-bottles'))
import generate_amber_bottles as G
from mathutils import Matrix, Vector

OUT = sys.argv[sys.argv.index('--out') + 1]
ML = 30
LENS = 50.0          # mm
SENSOR = 36.0        # mm
os.makedirs(OUT, exist_ok=True)


def cut_near_half(ob, rot=0.0):
    """Remove the half of the object nearest the camera (y < 0), so the camera
    at -y looks straight into the cross-section. `rot` pre-rotates about Z so
    the cut plane stays put when the cap is screwed round."""
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    if rot:
        bm.transform(Matrix.Rotation(rot, 4, 'Z'))
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
                           plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_inner=True)
    bm.to_mesh(me)
    bm.free()
    me.update()
    return ob


def mat(name, rgb, rough=0.4):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*rgb, 1.0)
    p.inputs['Roughness'].default_value = rough
    return m


def shot(name, objs, centre, width, extra=''):
    """Frame a subject `width` metres across, seen slightly from above."""
    for o in bpy.data.objects:
        if o.type == 'MESH':
            o.hide_render = o not in objs
    cam = bpy.data.objects['Cam']
    dist = LENS * width / SENSOR * 1.15
    cam.data.lens = LENS
    cam.data.clip_start = 0.001          # the scene is centimetres across
    cam.data.clip_end = 10.0
    cam.location = (Vector(centre)
                    + Vector((0.18, -0.96, 0.22)).normalized() * dist)
    cam.rotation_euler = (Vector(centre) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    for i, L in enumerate(LIGHTS):        # keep the key light on the camera side
        L.location = cam.location + Vector(LIGHT_OFF[i]) * dist
        L.rotation_euler = (Vector(centre) - L.location).to_track_quat('-Z', 'Y').to_euler()
        L.data.energy = LIGHT_W[i] * (dist ** 2) * 400
    bpy.context.view_layer.update()
    bpy.context.scene.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    print('->', name, extra, flush=True)


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 128
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1400, 1000
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.compression = 100   # lossless, just smaller on disk
sc.world = bpy.data.worlds.new('W')
sc.world.use_nodes = True
sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.05, 0.055, 0.07, 1)

cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam'))
sc.collection.objects.link(cam)
sc.camera = cam

LIGHT_OFF = [(0.5, 0.2, 0.9), (-1.1, 0.3, 0.2), (0.3, 1.6, 0.6)]
LIGHT_W = [1.0, 0.45, 0.30]
LIGHTS = []
for off in LIGHT_OFF:
    L = bpy.data.lights.new('L', 'AREA')
    L.size = 0.25
    ob = bpy.data.objects.new('L', L)
    sc.collection.objects.link(ob)
    LIGHTS.append(ob)

d = G.bottle_dims(ML)
c = G.cap_dims(d['N'])
glass = mat('Glass', (0.62, 0.30, 0.07), 0.3)
ppc = mat('CapThreaded', (0.34, 0.58, 0.86))
pp = mat('CapPlain', (0.90, 0.90, 0.88))
CAPZ = None

# --- the pair: closed, then screwed off, both cut open
bottle = G.make_bottle(d)
bottle.data.materials.append(glass)
sc.collection.objects.link(bottle)
CAPZ = bottle['cap_z_mm'] * G.MM
cut_near_half(bottle)
neck_c = (0, 0, (d['H'] - 7) * G.MM)

cap = None
for label, turns in (('01_pair_closed.png', 0.0), ('02_pair_half_turn.png', 0.5),
                     ('03_pair_one_turn.png', 1.0), ('04_pair_two_turns.png', 2.0)):
    if cap:
        bpy.data.objects.remove(cap)
    cap = G.make_cap(d['N'], threaded=True)
    cap.data.materials.append(ppc)
    sc.collection.objects.link(cap)
    cut_near_half(cap, rot=2 * math.pi * turns)
    cap.location = (0, 0, CAPZ + c['pitch'] * turns * G.MM)
    shot(label, {bottle, cap}, neck_c, 0.034, f'{turns} vueltas')

# --- the cap alone, cut open: the internal helix, unmistakable
bpy.data.objects.remove(cap)
solo = G.make_cap(d['N'], threaded=True)
solo.data.materials.append(ppc)
sc.collection.objects.link(solo)
cut_near_half(solo)
shot('05_cap_cutaway.png', {solo}, (0, 0, c['Hc'] * 0.45 * G.MM), 0.030)

# --- side by side with the catalogue's smooth bore
smooth = G.make_cap(d['N'], threaded=False)
smooth.data.materials.append(pp)
sc.collection.objects.link(smooth)
cut_near_half(smooth)
smooth.location = (0.030, 0, 0)
shot('06_smooth_vs_threaded.png', {solo, smooth},
     (0.015, 0, c['Hc'] * 0.45 * G.MM), 0.062, 'liso (der) vs roscado (izq)')
print('done')
