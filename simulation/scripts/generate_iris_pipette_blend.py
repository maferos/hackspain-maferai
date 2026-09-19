#!/usr/bin/env python3
"""Build a Blender file of the uncap-and-pipette hand, rigged, from iris_pipette_rig.py.

Run from simulation/ (needs Blender as a module, which only ships for 3.11):

    uv run --no-project --python 3.11 --with bpy --with mujoco \\
        python scripts/generate_iris_pipette_blend.py

Writes ``assets/ur10e_iris_pipette/ur10e_iris_pipette.blend`` and, beside it,
``ur10e_iris_pipette.glb`` (+Y up, the sequence baked, joint metadata as
extras). The same body tree, couplings and sequence as the HTML page
(``ur10e_iris_pipette.html``) and the MuJoCo / Isaac files of
generate_iris_pipette_scene.py, so the four move alike.

The degrees of freedom are custom properties on the ``hand`` root object, the
names of iris_pipette_rig.STATE:

* ``lift_z`` --- the hand frame's height: the bottle's base above the table
  once it is held (m).
* ``grip_aperture`` --- the 2F-85's jaw opening (m); the finger linkage
  follows it through the fit of hand_linkage.py, as in ur10e_hand.blend.
* ``hinge_angle`` --- the clamp's hinge, 0 down on the cap to pi/2 swung up.
* ``iris_angle`` --- the blades' angle; ``housing_turns`` --- the clamp's
  housing, in turns, unscrewing the cap. The sun, cam ring and planets follow
  through the planetary train.
* ``pipette_tip`` --- the tip's height in the hand frame (m); ``swing_angle``
  --- the frame's swing, 0 in over the neck to -80 deg out; ``plunger`` ---
  how far the plunger is pressed (m).

Plus ``wrist_angle`` (wrist_3_joint) and ``fill`` (how full the tip is, for
the render). Every joint is an empty whose rotation or location is a driver
expression built from iris_pipette_rig.JOINT_MAP; the bottle and the cap are
carried by Child Of constraints switched by the same rule the page uses. The
19 steps of iris_pipette_plan.py are keyframed on the properties, 30 fps.
"""
import math
import tempfile
import zipfile
from pathlib import Path

import bpy
import mujoco
import numpy as np
from mathutils import Matrix

import iris_pipette_plan as plan
import iris_pipette_rig as rig
from generate_hand_blend import (add_driver, build_gripper, build_stub, empty,
                                 import_mesh)
from generate_iris_pipette_scene import write_stl
from generate_iris_pipette_viewer import flange_x, pad_fit
from hand_linkage import GRIPPER, UR_MESHES, linkage, wrist3_pose

OUT = rig.SIM / 'assets/ur10e_iris_pipette/ur10e_iris_pipette.blend'
FPS = 30
# The properties: (default, min, max, subtype, description).
PROPS = {
    'lift_z': (plan.START['lift_z'], 0.0, 0.3, 'DISTANCE', 'Hand frame height: the bottle base above the table once held (m)'),
    'grip_aperture': (plan.START['grip_aperture'], 0.0, rig.OPEN_APERTURE, 'DISTANCE', 'Jaw opening between the pads (m)'),
    'hinge_angle': (plan.START['hinge_angle'], 0.0, rig.HINGE_UP, 'ANGLE', 'Clamp hinge: 0 down on the cap, pi/2 swung up over the gripper'),
    'iris_angle': (plan.START['iris_angle'], 0.0, rig.IRIS['blade_max'], 'ANGLE', 'Blade angle: aperture = 2 r_pivot cos(angle)'),
    'housing_turns': (0.0, 0.0, rig.IRIS['turns'] + 0.5, 'NONE', 'Turns of the clamp housing (unscrewing the cap)'),
    'pipette_tip': (plan.START['pipette_tip'], 0.0, rig.TIP_READY, 'DISTANCE', 'Pipette tip height in the hand frame (m)'),
    'swing_angle': (plan.START['swing_angle'], rig.STOW, 0.0, 'ANGLE', 'Pipette frame swing: 0 in over the neck, negative out to the arm side'),
    'plunger': (0.0, 0.0, rig.PLUNGER_STROKE, 'DISTANCE', 'Plunger pressed (m)'),
    'wrist_angle': (0.0, -2 * math.pi, 2 * math.pi, 'ANGLE', 'wrist_3_joint: rotation about the tool axis (rad)'),
    'fill': (0.0, 0.0, 1.0, 'FACTOR', 'How full the tip is (render only)'),
}
# Driver variable names: one letter per state, as in generate_hand_blend.
VAR = {k: chr(ord('a') + i) for i, k in enumerate(rig.STATE)}
MESH_DIR = Path(tempfile.mkdtemp(prefix='iris_pipette_'))


def rig_material(name: str) -> bpy.types.Material:
    """A principled material in one of the rig's colours (or the 2F-85's)."""
    from generate_hand_blend import material
    from hand_linkage import MATERIALS
    if name in MATERIALS:
        return material(name)
    mat = bpy.data.materials.get(name)
    if mat is None:
        rgba = rig.RIG_MATERIALS[name]
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = rgba
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes['Principled BSDF']
        bsdf.inputs['Base Color'].default_value = rgba
        bsdf.inputs['Roughness'].default_value = 0.35 if name in ('gold', 'bracket') else 0.5
        bsdf.inputs['Metallic'].default_value = 0.7 if name in ('gold', 'bracket', 'housing') else 0.0
        if rgba[3] < 1:
            bsdf.inputs['Alpha'].default_value = rgba[3]
            mat.surface_render_method = 'BLENDED'
    return mat


def unzip_meshes() -> None:
    """The STLs the tree uses, out of the two zips (and the amber bottle's
    OBJs) into a temporary folder."""
    with zipfile.ZipFile(rig.IRIS_ZIP) as archive:
        for part in rig.IRIS_PARTS:
            (MESH_DIR / f'iris_{part}.stl').write_bytes(rig.zip_member(archive, f'meshes/{part}.stl'))
    for part in ('glass', 'cap'):
        write_stl(MESH_DIR / f'amber_{part}.stl', rig.amber_mesh(part))
    with zipfile.ZipFile(rig.PIPETTE_ZIP) as archive:
        for parts in rig.PIPETTE_PARTS.values():
            for part in parts:
                (MESH_DIR / f'pipette_{part}.stl').write_bytes(rig.zip_member(archive, f'meshes/{part}.stl'))


def mesh_data(key: str) -> bpy.types.Mesh:
    """The mesh block for 'iris/body' etc., imported once and shared."""
    name = key.replace('/', '_')
    if name not in bpy.data.meshes:
        before = set(bpy.data.objects)
        bpy.ops.wm.stl_import(filepath=str(MESH_DIR / f'{name}.stl'), forward_axis='Y', up_axis='Z')
        (obj,) = set(bpy.data.objects) - before
        obj.data.name = name
        for poly in obj.data.polygons:
            poly.use_smooth = False
        bpy.data.objects.remove(obj)
    return bpy.data.meshes[name]


def link(obj, parent, pos, quat, mat=None):
    bpy.context.scene.collection.objects.link(obj)
    obj.parent = parent
    obj.location = pos
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = quat
    if mat is not None:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    return obj


def primitive(g: dict) -> bpy.types.Object:
    """A box, cylinder or cone from a tree geom, by its half sizes, along Z."""
    size = g['size']
    if g['type'] == 'box':
        bpy.ops.mesh.primitive_cube_add(size=2.0)
        obj = bpy.context.active_object
        obj.scale = size
    elif g['type'] == 'cone':
        bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=size[0], radius2=0.0, depth=2 * size[1])
        obj = bpy.context.active_object
    else:
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=size[0], depth=2 * size[1])
        obj = bpy.context.active_object
    bpy.ops.object.transform_apply(scale=True)
    bpy.context.scene.collection.objects.unlink(obj)
    obj.name = obj.data.name = g['name']
    return obj


def geom_object(g: dict, parent) -> bpy.types.Object:
    if g['type'] == 'mesh':
        obj = bpy.data.objects.new(g['name'], mesh_data(g['mesh']))
    else:
        obj = primitive(g)
    return link(obj, parent, g['pos'], g['quat'], rig_material(g['material']))


def expression(joint: str) -> str:
    """JOINT_MAP as a Blender simple expression in the VAR letters."""
    offset, coefs = rig.JOINT_MAP[joint]
    terms = [f'{c:.9g}*{VAR[k]}' for k, c in coefs.items()]
    if offset:
        terms.insert(0, f'{offset:.9g}')
    return ' + '.join(terms).replace('+ -', '- ')


def drive(obj, path: str, index: int, hand, expr: str, states) -> None:
    """A driver on obj.path[index] from state properties of the hand root."""
    fcurve = obj.driver_add(path, index)
    driver = fcurve.driver
    driver.type = 'SCRIPTED'
    for k in states:
        var = driver.variables.new()
        var.name = VAR[k]
        var.type = 'SINGLE_PROP'
        var.targets[0].id = hand
        var.targets[0].data_path = f'["{k}"]'
    driver.expression = expr


def build_tree(tree: list[dict], hand, wrist) -> dict:
    """One empty per body, a driven pivot per joint, an object per visible geom."""
    groups = {'wrist_3_link': wrist}
    for b in tree:
        frame = empty(b['name'] if b['joint'] is None else f'{b["name"]}_mount', groups[b['parent']],
                      b['pos'], b['quat'], 0.01)
        j = b['joint']
        if j is not None:
            pivot = empty(j['name'], frame, size=0.012)
            pivot.rotation_mode = 'XYZ'
            (axis,) = np.flatnonzero(j['axis'])
            sign = float(np.sign(j['axis'][axis]))
            expr = expression(j['name'])
            if sign < 0:
                expr = f'-({expr})'
            _, coefs = rig.JOINT_MAP[j['name']]
            path = 'location' if j['type'] == 'slide' else 'rotation_euler'
            (pivot.lock_location if j['type'] == 'slide' else pivot.lock_rotation)[:] = (True, True, True)
            drive(pivot, path, int(axis), hand, expr, coefs)
            pivot['joint'] = j['type']
            pivot['axis'] = j['axis']
            pivot['range'] = j['range'] or [-1e9, 1e9]
            pivot['coupling'] = f'{j["name"]} = ' + ' + '.join(f'{c:.6g} * {k}' for k, c in coefs.items())
            frame = pivot
        groups[b['name']] = frame
        for s in b['sites']:
            groups[s['name']] = empty(s['name'], frame, s['pos'], size=0.008)
        for g in b['geoms']:
            if g['visible']:
                geom_object(g, frame)
    return groups


def child_of(obj, target):
    """A Child Of constraint that puts obj at target's frame: no inverse, which
    Blender would otherwise set on assigning the target."""
    c = obj.constraints.new('CHILD_OF')
    c.target = target
    c.set_inverse_pending = False
    c.inverse_matrix = Matrix.Identity(4)
    return c


def build_bottle(hand, groups):
    """The reference bottle (the 60 ml amber one), its liquid and the PP25
    cap, carried as the page carries them."""
    bottle = link(bpy.data.objects.new('bottle', mesh_data('amber/glass')), None, (0, 0, 0), (1, 0, 0, 0),
                  rig_material('bottle'))
    for poly in bottle.data.polygons:
        poly.use_smooth = True
    R, level, floor = rig.BOTTLE_R - rig.AMBER['wall'], rig.BOTTLE['level'], rig.AMBER['floor']
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=R - 0.0005, depth=level - floor)
    liquid = bpy.context.active_object
    liquid.name = liquid.data.name = 'liquid'
    liquid.parent = bottle
    liquid.location = (0, 0, floor + (level - floor) / 2)
    liquid.data.materials.append(rig_material('liquid'))
    # held: in the hand frame (their origins coincide when the bottle stands on the table)
    hold = child_of(bottle, groups['hand_frame'])
    drive(hold, 'influence', -1, hand,
          f'1 if {VAR["grip_aperture"]} <= {2 * rig.BOTTLE_R + 0.0005:.6g} else 0', ['grip_aperture'])
    cap = link(bpy.data.objects.new('cap', mesh_data('amber/cap')), None, (0, 0, 0), (1, 0, 0, 0), rig_material('cap'))
    on_bottle = empty('cap_on_bottle', bottle, (0, 0, rig.IRIS['bottle_h']), size=0.008)
    for target, expr in ((on_bottle, f'1 if {VAR["housing_turns"]} <= 1e-4 else 0'),
                         (groups['cap_seat'], f'1 if {VAR["housing_turns"]} > 1e-4 else 0')):
        drive(child_of(cap, target), 'influence', -1, hand, expr, ['housing_turns'])
    return bottle, cap


def keyframe_sequence(hand, scene) -> None:
    """The plan's keys on the properties; the last step opens the jaws, then lifts."""
    frames = plan.keys()
    (t_last, last), (t_prev, prev) = frames[-1], frames[-2]
    mid = dict(prev)
    mid['grip_aperture'] = last['grip_aperture']
    frames = frames[:-1] + [((t_prev + t_last) / 2, mid), (t_last, last)]
    for t, state in frames:
        frame = 1 + round(t * FPS)
        for k in (*rig.STATE, 'fill'):
            hand[k] = state[k]
            hand.keyframe_insert(f'["{k}"]', frame=frame)
    scene.frame_start, scene.frame_end = 1, 1 + round((plan.DURATION + plan.TAIL) * FPS)
    scene.render.fps = FPS
    # the page's easing: a half cosine into and out of every key
    try:
        action = hand.animation_data.action
        fcurves = getattr(action, 'fcurves', None)
        if fcurves is None or not len(fcurves):     # slotted actions (Blender >= 4.4)
            fcurves = [f for layer in action.layers for strip in layer.strips
                       for bag in strip.channelbags for f in bag.fcurves]
        for fcurve in fcurves:
            for kp in fcurve.keyframe_points:
                kp.interpolation, kp.easing = 'SINE', 'EASE_IN_OUT'
    except Exception as exc:   # noqa: BLE001 - the file is still right, only the easing differs
        print(f'could not set the easing: {exc}')
    for k in (*rig.STATE, 'fill'):
        hand[k] = frames[0][1][k]
    scene.frame_set(1)


def check(hand, groups, cap, tree, fx) -> None:
    """The rigged file against iris_pipette_rig.fk at the states the sequence passes.

    Raises:
        RuntimeError: If the tip, the cap seat or the cap is off by over a micrometre.
    """
    worst = 0.0
    for n in (3, 6, 8, 10, 13):
        state, _ = plan.state_at(plan.step_end(n) - 1e-6)
        for k in rig.STATE:
            hand[k] = state[k]
        for obj in (hand, cap, cap.parent or hand):
            obj.update_tag()              # a property set from Python does not tag the drivers by itself
        bpy.context.view_layer.update()
        joints = rig.joint_values(state)
        root = {'wrist_3_link': (np.array([fx, 0, rig.GRIP_Z + state['lift_z']]), np.array(rig.TOOL_QUAT))}
        poses = rig.fk(tree, joints, root)
        for name in ('pipette_tip', 'cap_seat', 'pipette_swing', 'blade_3', 'hand_frame', 'clamp_swing', 'clamp_mount', 'carrier', 'pipette_slide'):
            err = float(np.linalg.norm(np.array(groups[name].matrix_world.translation) - poses[name][0]))
            if err > 1e-6:
                print(f'  step {n}: {name} off by {err * 1000:.3f} mm: blender {np.array(groups[name].matrix_world.translation).round(4)} vs fk {poses[name][0].round(4)}')
            worst = max(worst, err)
        where = plan.attachments(state)
        cap_expected = poses['cap_seat'][0] if where['cap'] == 'clamp' else np.array([0, 0, rig.IRIS['bottle_h']]) + (
            [0, 0, state['lift_z']] if where['bottle'] == 'hand' else [0, 0, 0])
        cap_err = float(np.linalg.norm(np.array(cap.matrix_world.translation) - cap_expected))
        if cap_err > 1e-6:
            print(f'  step {n}: cap off by {cap_err * 1000:.3f} mm: blender {np.array(cap.matrix_world.translation).round(4)} vs '
                  f'{cap_expected.round(4)} ({where}); influences {[c.influence for c in cap.constraints]}')
        worst = max(worst, cap_err)
    print(f'Blender rig vs iris_pipette_rig.fk: within {worst * 1e6:.2f} um')
    if worst > 1e-6:
        raise RuntimeError('the .blend and the rig tree disagree')


def main() -> None:
    closed_gap, open_gap, fits = linkage()
    fx = flange_x(pad_fit(mujoco.MjModel.from_xml_path(str(GRIPPER)), fits))
    tree = rig.tree(fx)
    unzip_meshes()

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'

    hand = empty('hand', size=0.08)
    for k, (default, lo, hi, subtype, text) in PROPS.items():
        hand[k] = float(default)
        ui = {'min': lo, 'max': hi, 'description': text, 'step': 0.1 if subtype == 'DISTANCE' else 100, 'precision': 4}
        if subtype != 'NONE':
            ui['subtype'] = subtype
        hand.id_properties_ui(k).update(**ui)
    hand.lock_location = (True, True, True)
    drive(hand, 'location', 2, hand, VAR['lift_z'], ['lift_z'])

    # the tool frame in the hand frame: stub, wrist_3_joint, flange, 2F-85
    tool = empty('tool', hand, *rig.tool_pose(fx), size=0.04)
    build_stub(tool)
    wrist = empty('wrist_3_joint', tool, size=0.06)
    wrist.rotation_mode = 'XYZ'
    wrist.lock_rotation = (True, True, True)
    add_driver(wrist, 'rotation_euler', 2, hand, 'wrist_angle', 'a')
    pos, quat = wrist3_pose()
    import_mesh(UR_MESHES / 'wrist3.obj', 'wrist_3_link', wrist, 'linkgray', pos=pos, quat=quat)
    build_gripper(wrist, hand, fits)

    groups = build_tree(tree, hand, wrist)
    bottle, cap = build_bottle(hand, groups)
    check(hand, groups, cap, tree, fx)
    keyframe_sequence(hand, scene)

    # A camera and light so F12 shows something straight away.
    cam = bpy.data.objects.new('camera', bpy.data.cameras.new('camera'))
    scene.collection.objects.link(cam)
    cam.location = (0.75, -0.6, 0.45)
    cam.data.lens = 50
    track = cam.constraints.new('TRACK_TO')
    track.target = empty('camera_target', pos=(0, 0.03, 0.2), size=0.01)
    scene.camera = cam
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN'))
    sun.data.energy = 4
    sun.rotation_euler = (0.6, 0.3, 0.8)
    scene.collection.objects.link(sun)
    world = bpy.data.worlds.new('world')
    world.color = (0.35, 0.35, 0.38)
    scene.world = world

    OUT.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), check_existing=False)
    OUT.with_suffix('.blend1').unlink(missing_ok=True)   # Blender's backup
    glb = OUT.with_suffix('.glb')
    bpy.ops.export_scene.gltf(filepath=str(glb), export_format='GLB', export_yup=True, export_apply=True,
                              export_animations=True, export_animation_mode='SCENE', export_extras=True)
    print(f'wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB) and {glb.name} ({glb.stat().st_size / 1e6:.1f} MB)')

    # It has to come back with its properties.
    bpy.ops.wm.open_mainfile(filepath=str(OUT))
    hand = bpy.data.objects['hand']
    missing = [k for k in PROPS if k not in hand]
    if missing:
        raise RuntimeError(f'properties lost on reopening: {missing}')
    print(f'reopened: {len(bpy.data.objects)} objects, properties {", ".join(PROPS)}')


if __name__ == '__main__':
    main()
