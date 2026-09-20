"""Shared numbers and helpers for the minimal vertical hand (gripper-design/vertical_hand.html).

Every part is a box or a cylinder, so each one is a real collider: in Blender a passive rigid body with
an exact BOX / CYLINDER shape (truncated cones use a convex hull), in MuJoCo a geom of the same size.
Rings are built from box segments for the same reason. Millimetres in, metres out; Z up; +X arm to bottle.
"""
import math
import bpy

MM = 0.001
# ---- the page's numbers ----
REF_CAP_Z = 78.1; GRIP_Z = REF_CAP_Z - 21; Z_IRIS = REF_CAP_Z + 1.5; LIFT_HI = 30.5
GAP, PLATE = 4, 4; HALF_IN = 69 + GAP; HALF_OUT = HALF_IN + PLATE
PARK_X = -90; CAGE = dict(x0=-167, x1=65, z0=45.1, z1=530); HEAD = dict(x0=-167, x1=-45, z0=470)
TIP_READY = Z_IRIS + LIFT_HI + 106 + GAP
# The pose the asset is built in: the clamp parked back and high with the iris open (the sequence's
# start, and the only pose in which a bottle can come up between the cradles), the pipette parked.
CLAMP_POSE = dict(x=PARK_X, lift=LIFT_HI, open=True)
BOTTLE_60 = dict(r=20.0, cap_r=14.4)
vertex = lambda r: (r * r + 64) / 16 + 0.2

PARTS = []          # every solid, for the MJCF: dict(kind, body, name, pos, size, rz, mat)
ROOT = None         # the hand's root empty; parts default to it
JOINTS = []         # MuJoCo slide joints: dict(name, body, axis, range) in metres
SITES = []          # MuJoCo sites: dict(name, body, type, pos, size) in mm

def mat(name, rgb, metal=0.3, rough=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    m.diffuse_color = (*rgb, 1); m['rgba'] = list(rgb) + [1.0]; return m

class Mats:
    def __init__(self):
        self.black = mat('Harness', (0.02, 0.022, 0.026), metal=0.4); self.gray = mat('Links', (0.18, 0.2, 0.23), metal=0.6, rough=0.4)
        self.steel = mat('Steel', (0.6, 0.62, 0.65), metal=0.9, rough=0.25); self.gold = mat('Iris', (0.65, 0.4, 0.05), metal=0.7, rough=0.35)
        self.white = mat('Pipette', (0.85, 0.85, 0.83), metal=0.05); self.blue = mat('PipetteBlue', (0.14, 0.3, 0.72), metal=0.05)
        self.led = mat('LED', (0.1, 0.9, 0.35), metal=0.0)

def _finish(o, name, m, parent, rec):
    parent = parent or ROOT
    o.name = name; o.data.name = name; o.data.materials.append(m); o.parent = parent
    rec.update(name=name, body=parent.name, mat=m.name); PARTS.append(rec); return o

def box(name, x0, x1, y0, y1, z0, z1, m, parent=None, rz=0.0, center=None):
    """An axis-aligned box, or one turned rz about Z around `center` (mm) when given."""
    dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
    c = center if center is not None else ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(c[0] * MM, c[1] * MM, c[2] * MM))
    o = bpy.context.object; o.scale = (dx * MM, dy * MM, dz * MM); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.location = (c[0] * MM, c[1] * MM, c[2] * MM); o.rotation_euler = (0, 0, rz)      # set explicitly: the add operator's location is not kept once the scale is applied
    return _finish(o, name, m, parent, dict(kind='box', pos=c, size=(dx / 2, dy / 2, dz / 2), rz=rz))

def cyl(name, r0, r1, z0, z1, x, y, m, parent=None, seg=48):
    """A cylinder (r0 == r1) or a truncated cone along Z; MuJoCo gets a cylinder of the larger radius."""
    bpy.ops.mesh.primitive_cone_add(vertices=seg, radius1=r0 * MM, radius2=r1 * MM, depth=(z1 - z0) * MM, location=(x * MM, y * MM, (z0 + z1) / 2 * MM))
    o = bpy.context.object; o.location = (x * MM, y * MM, (z0 + z1) / 2 * MM)
    return _finish(o, name, m, parent, dict(kind='cyl', pos=(x, y, (z0 + z1) / 2), size=(max(r0, r1), (z1 - z0) / 2), rz=0.0, cone=r0 != r1))

def ring(name, ro, ri, z0, z1, x, y, m, parent=None, seg=24):
    """A ring as `seg` box segments, each a collider; the bore stays open."""
    rm, t = (ro + ri) / 2, ro - ri; L = 2 * ro * math.sin(math.pi / seg) * 1.02
    for k in range(seg):
        a = k * 2 * math.pi / seg
        box(f'{name}_{k:02d}', -t / 2, t / 2, -L / 2, L / 2, z0, z1, m, parent, rz=a, center=(x + rm * math.cos(a), y + rm * math.sin(a), (z0 + z1) / 2))

def empty(name, parent, x=0.0, y=0.0, z=0.0):
    e = bpy.data.objects.new(name, None); e.empty_display_type = 'ARROWS'; e.empty_display_size = 0.02
    e.parent = parent; e.location = (x * MM, y * MM, z * MM); bpy.context.scene.collection.objects.link(e); return e

def add_collisions():
    """Passive rigid bodies with exact primitive shapes on every mesh."""
    for o in list(bpy.data.objects):
        if o.type != 'MESH': continue
        with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o], selected_editable_objects=[o]):
            bpy.ops.rigidbody.object_add(type='PASSIVE')
        rb = o.rigid_body; rec = next(p for p in PARTS if p['name'] == o.name)
        rb.collision_shape = 'BOX' if rec['kind'] == 'box' else ('CONVEX_HULL' if rec.get('cone') else 'CYLINDER')
        rb.friction = 0.6; rb.restitution = 0.0
