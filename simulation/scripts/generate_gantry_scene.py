#!/usr/bin/env python3
"""Build an XYZ double-rail gantry carrying Eki's vertical hand directly.

Run with simulation/.venv/bin/python simulation/scripts/generate_gantry_scene.py.
The output is a mechanical prototype; the UR10e scan planner is not compatible.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

SIM = Path(__file__).resolve().parents[1]
OUT = SIM / 'models/minihannover_gantry_scene.xml'


def build_scene() -> Path:
    # Reuse the current bench and balance layout without regenerating its assets.
    from vision_pick import gripper_scene
    root = ET.parse(gripper_scene()).getroot()
    root.set('model', 'minihannover_gantry_scene')
    assets, world = root.find('asset'), root.find('worldbody')
    assets.remove(assets.find('model[@name="ur10e_2f85"]'))
    ET.SubElement(assets, 'model', name='gantry_hand',
                  file='../assets/vertical_hand_minimal/vertical_hand_minimal.xml')
    # Look below the front rail so it cannot mask the sample survey.
    camera = world.find("camera[@name='general']")
    camera.set('pos', '-1.5 -2.9 1.95')
    camera.attrib.pop('xyaxes', None)
    camera.attrib.pop('euler', None)
    camera.set('quat', '0.82806723 0.56062881 0 0')
    camera.set('fovy', '80')
    for name in ('rail', 'rail_carriage'):
        world.remove(world.find(f'body[@name="{name}"]'))
    for tag in ('actuator', 'keyframe'):
        node = root.find(tag)
        if node is not None:
            root.remove(node)

    def box(parent, name, pos, size, material='gantry', **kwargs):
        return ET.SubElement(parent, 'geom', name=name, type='box',
                             pos=pos, size=size, material=material, **kwargs)

    fixed = ET.SubElement(world, 'body', name='gantry_frame')
    for side, y in (('front', -1.60), ('back', .80)):
        box(fixed, f'gantry_rail_{side}', f'-1.5 {y} 2.10', '3.35 .055 .07')
        for end, x in (('left', -4.75), ('right', 1.75)):
            box(fixed, f'gantry_post_{side}_{end}', f'{x} {y} 1.015', '.055 .055 1.015')
    bridge = ET.SubElement(world, 'body', name='gantry_bridge', pos='-1.5 -.4 2.24', gravcomp='1')
    ET.SubElement(bridge, 'joint', name='gantry_x', type='slide', axis='1 0 0',
                  range='-3 3', damping='200', armature='20')
    box(bridge, 'gantry_crossbeam', '0 0 0', '.065 1.26 .065', mass='30')
    for side, y in (('front', -1.2), ('back', 1.2)):
        box(bridge, f'gantry_runner_{side}', f'0 {y} -.07', '.18 .10 .05', 'carriage', mass='5')
    cross = ET.SubElement(bridge, 'body', name='gantry_cross_carriage', gravcomp='1')
    ET.SubElement(cross, 'joint', name='gantry_y', type='slide', axis='0 1 0',
                  range='-.95 .95', damping='100', armature='10')
    box(cross, 'gantry_y_plate', '0 0 -.11', '.12 .14 .045', 'carriage', mass='4')
    # The hand's mounting face is 532 mm above its local origin. Its cap seat
    # at 57.1 mm starts at world z=1.5751; Z travel brings it down to z=.9451.
    lift = ET.SubElement(cross, 'body', name='gantry_lift', pos='0 0 -.19', gravcomp='1')
    ET.SubElement(lift, 'joint', name='gantry_z', type='slide', axis='0 0 1',
                  range='-.63 0', damping='100', armature='5')
    box(lift, 'gantry_z_column', '0 0 .34', '.025 .03 .34', mass='3')
    box(lift, 'gantry_hand_mount', '0 0 .01', '.09 .085 .01', 'carriage', mass='1')
    frame = ET.SubElement(lift, 'frame', pos='.106 0 -.532')
    ET.SubElement(frame, 'attach', model='gantry_hand', body='vertical_hand', prefix='arm_grip_')
    box(lift, 'gantry_camera_crossbar', '.15 -.25 -.01', '.15 .012 .012', 'carriage', mass='.1')
    box(lift, 'gantry_camera_bracket', '0 -.125 -.01', '.012 .125 .012', 'carriage', mass='.1')
    box(lift, 'gantry_camera_drop', '.30 -.25 -.295', '.012 .012 .295', 'carriage', mass='.1')
    box(lift, 'gantry_camera_housing', '.30 -.275 -.575', '.025 .015 .015', 'carriage', mass='.05')
    ET.SubElement(lift, 'camera', name='arm_eih', pos='.30 -.25 -.60',
                  xyaxes='1 0 0 0 .70710678 .70710678', fovy='60.44', resolution='1920 1080')
    ET.SubElement(world, 'camera', name='gantry_overview', pos='-4.4 -2.7 2.7',
                  xyaxes='.621 -.784 0 .283 .224 .932', fovy='60')
    # Sliding guide surfaces constrain motion through joints, not friction contacts.
    contact = root.find('contact')
    if contact is None:
        contact = ET.SubElement(root, 'contact')
    for first, second in (('gantry_frame', 'gantry_bridge'),
                          ('gantry_bridge', 'gantry_lift')):
        ET.SubElement(contact, 'exclude', body1=first, body2=second)
    actuators = ET.SubElement(root, 'actuator')
    for axis, limits in (('x', '-3 3'), ('y', '-.95 .95'), ('z', '-.63 0')):
        ET.SubElement(actuators, 'position', name=f'gantry_{axis}', joint=f'gantry_{axis}',
                      kp='60000', kv='3000', ctrlrange=limits, forcerange='-4000 4000')
    ET.indent(root, space='  ')
    OUT.write_text('<?xml version="1.0" encoding="utf-8"?>\n'
                   '<!-- Generated by scripts/generate_gantry_scene.py. -->\n'
                   + ET.tostring(root, encoding='unicode') + '\n')
    return OUT


if __name__ == '__main__':
    import mujoco
    path = build_scene()
    model = mujoco.MjModel.from_xml_path(str(path))
    print(f'{path}: {model.nq} positions, {model.nu} actuators')
