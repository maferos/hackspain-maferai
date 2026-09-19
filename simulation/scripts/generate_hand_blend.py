#!/usr/bin/env python3
"""Build a Blender file of the UR10e's hand alone: wrist stub + flange + 2F-85.

Run from simulation/ (needs Blender as a module, which only ships for 3.11):

    uv run --no-project --python 3.11 --with bpy --with mujoco \\
        python scripts/generate_hand_blend.py

Writes ``assets/ur10e_hand/ur10e_hand.blend``. The kinematics and constants
live in hand_linkage.py, shared with generate_hand_viewer.py.

The rail scene's arm (``assets/ur10e_2f85/ur10e_2f85.xml``, ``TOOL='gripper'``)
cut down to what is past the last wrist joint. Shoulder, elbow and the first
two wrist joints are dropped; a fixed cylinder stands in for the arm the hand
comes out of. Two degrees of freedom are left, both custom properties on the
``hand`` root object:

* ``wrist_angle`` --- rotation of ``wrist_3_joint`` in radians, about the tool
  axis. Turns the flange and everything on it; the stub stays put.
* ``grip_aperture`` --- the jaw opening in metres, 0 (closed) to 0.085 (open),
  measured between the two pads. The fingers are a closed four-bar linkage per
  side; every link angle follows the aperture through a polynomial fitted to
  MuJoCo's own solution of that linkage, so the pads stay parallel and the
  links stay joined exactly as they do in simulation.
"""
import bpy
import mujoco
import numpy as np

from hand_linkage import (GRIP_MESHES, GRIPPER, MATERIALS, MESH_MATERIAL,
                          OUT_DIR, RING_HEIGHT, STUB_LENGTH, STUB_RADIUS,
                          STUB_TOP, UR_MESHES, gripper_bodies, linkage,
                          wrist3_pose)

OUT = OUT_DIR / 'ur10e_hand.blend'


def horner(coef: np.ndarray, var: str) -> str:
    """A polynomial as a driver expression Blender evaluates without Python."""
    expr = f'{coef[-1]:.6g}'
    for c in coef[-2::-1]:
        expr = f'({c:.6g} + {var}*{expr})'
    return expr


def material(name: str) -> bpy.types.Material:
    """Get or make a plain principled material in one of the MJCF colours."""
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = MATERIALS[name]
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes['Principled BSDF']
        bsdf.inputs['Base Color'].default_value = MATERIALS[name]
        bsdf.inputs['Roughness'].default_value = 0.5
    return mat


def empty(name, parent=None, pos=(0, 0, 0), quat=(1, 0, 0, 0), size=0.02):
    """Add an empty at a pose relative to its parent."""
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = 'ARROWS'
    obj.empty_display_size = size
    bpy.context.scene.collection.objects.link(obj)
    obj.parent = parent
    obj.location = pos
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = quat
    return obj


def import_mesh(path, name: str, parent, mat: str, scale=1.0,
                pos=(0, 0, 0), quat=(1, 0, 0, 0)):
    """Import one mesh file as-is (MJCF axes, no Blender axis conversion)."""
    before = set(bpy.data.objects)
    if path.suffix == '.stl':
        bpy.ops.wm.stl_import(filepath=str(path), global_scale=scale,
                              forward_axis='Y', up_axis='Z')
    else:
        bpy.ops.wm.obj_import(filepath=str(path), global_scale=scale,
                              forward_axis='Y', up_axis='Z')
    (obj,) = set(bpy.data.objects) - before
    obj.name = obj.data.name = name
    obj.data.materials.clear()
    obj.data.materials.append(material(mat))
    obj.parent = parent
    obj.location = pos
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = quat
    for poly in obj.data.polygons:
        poly.use_smooth = False
    return obj


def add_driver(obj, path, index, hand, prop, expr):
    """Drive obj.path[index] from a custom property on the hand root."""
    fcurve = obj.driver_add(path, index)
    driver = fcurve.driver
    driver.type = 'SCRIPTED'
    var = driver.variables.new()
    var.name = 'a'
    var.type = 'SINGLE_PROP'
    var.targets[0].id = hand
    var.targets[0].data_path = f'["{prop}"]'
    driver.expression = expr
    assert driver.use_self is False


def build_stub(hand):
    """The fixed cylinder the hand comes out of, behind the flange."""
    stub = empty('arm_stub', hand)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=STUB_RADIUS,
                                        depth=STUB_LENGTH)
    body = bpy.context.active_object
    body.name = body.data.name = 'arm_stub_housing'
    body.parent = stub
    body.location = (0, 0, STUB_TOP - STUB_LENGTH / 2)
    body.data.materials.append(material('linkgray'))
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=STUB_RADIUS + 0.001,
                                        depth=RING_HEIGHT)
    ring = bpy.context.active_object
    ring.name = ring.data.name = 'arm_stub_ring'
    ring.parent = stub
    ring.location = (0, 0, STUB_TOP - RING_HEIGHT / 2)
    ring.data.materials.append(material('urblue'))
    for obj in (body, ring):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_auto_smooth()


def build_gripper(wrist, hand, fits):
    """Mirror the 2F-85's body tree, one pivot per finger joint."""
    model = mujoco.MjModel.from_xml_path(str(GRIPPER))
    frames = {0: wrist}
    for b, name, parent, pos, quat, joint, jpos, meshes in gripper_bodies(model):
        frame = empty(f'{name}_mount', frames[parent], pos, quat, 0.01)
        if joint:
            pivot = empty(joint, frame, jpos, size=0.01)
            pivot.rotation_mode = 'XYZ'
            pivot.lock_rotation = (True, True, True)
            add_driver(pivot, 'rotation_euler', 0, hand, 'grip_aperture',
                       horner(fits[joint], 'a'))
            frame = empty(name, pivot, -jpos, size=0.01)
        else:
            frame.name = name
        frames[b] = frame
        # Import the file, not MuJoCo's re-centred copy: its vertices are
        # already in the body frame.
        for mesh in meshes:
            import_mesh(GRIP_MESHES / f'{mesh}.stl', f'{name}_{mesh}', frame,
                        MESH_MATERIAL[mesh], scale=0.001)


def main() -> None:
    closed_gap, open_gap, fits = linkage()

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'

    hand = empty('hand', size=0.08)
    hand['wrist_angle'] = 0.0
    hand.id_properties_ui('wrist_angle').update(
        min=-2 * np.pi, max=2 * np.pi, subtype='ANGLE', step=100,
        description='wrist_3_joint: rotation about the tool axis (rad)')
    hand['grip_aperture'] = open_gap
    hand.id_properties_ui('grip_aperture').update(
        min=closed_gap, max=open_gap, subtype='DISTANCE',
        step=0.1, precision=4,
        description='Jaw opening between the pads (m): 0.085 open, 0 closed')

    build_stub(hand)

    # wrist_3_link: rotates about the tool axis, carries the flange and gripper.
    wrist = empty('wrist_3_joint', hand, size=0.06)
    wrist.rotation_mode = 'XYZ'
    wrist.lock_rotation = (True, True, True)
    add_driver(wrist, 'rotation_euler', 2, hand, 'wrist_angle', 'a')
    pos, quat = wrist3_pose()
    import_mesh(UR_MESHES / 'wrist3.obj', 'wrist_3_link', wrist, 'linkgray',
                pos=pos, quat=quat)
    build_gripper(wrist, hand, fits)

    # A camera and light so F12 shows something straight away.
    cam = bpy.data.objects.new('camera', bpy.data.cameras.new('camera'))
    scene.collection.objects.link(cam)
    cam.location = (0.30, -0.24, 0.24)
    cam.data.lens = 50
    track = cam.constraints.new('TRACK_TO')
    track.target = empty('camera_target', pos=(0, 0, 0.03), size=0.01)
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
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
