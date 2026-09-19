"""Build the rail viewport from the shared ten-pattern catalogue in memory."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import mujoco

SIM = Path(__file__).resolve().parents[2] / 'simulation'
PATTERNS = SIM / 'assets/minihannover_open/patterns'
CATALOGUE = json.loads((PATTERNS / 'index.json').read_text())['patterns']


def build_pattern(scene_path, name):
    entry = next(p for p in CATALOGUE if p['pattern'] == name)
    population = json.loads((PATTERNS / entry['file']).read_text())
    root = ET.parse(scene_path).getroot()
    asset, world = root.find('asset'), root.find('worldbody')
    # Resolve top-level references before compiling from a string. Child model
    # assets continue resolving relative to their own XML files.
    for element in root.iter():
        if 'file' in element.attrib:
            element.set('file', str((scene_path.parent / element.get('file')).resolve()))
    for body in list(world.findall('body')):
        if body.get('name', '').startswith(('dyn_', 'loose_')):
            world.remove(body)
    for model in list(asset.findall('model')):
        if model.get('name', '').startswith('dyn_'):
            asset.remove(model)
    # Match the desk-local origin authored by the room generator.
    room_path = next(m.get('file') for m in asset.findall('model') if m.get('name') == 'lab_room')
    room = ET.parse(room_path).getroot()
    desk = next(f for f in room.iter('frame') if any(
        g.get('name') == 'worktop_finish_0' for g in f.findall('geom')))
    origin = list(map(float, desk.get('pos').split()))
    for item in population['containers']:
        sample = item['sample_id']
        name = f'dyn_{sample}'
        # The open, part-filled copy when there is one, so the pipette can draw
        # from it; scripts/generate_open_vessels.py writes them.
        opened = SIM / 'assets/open_vessels' / f'{sample}.xml'
        ET.SubElement(asset, 'model', name=name, file=str(
            opened if opened.exists() else SIM / 'assets/labelled_bottles' / f'{sample}.xml'))
        body = ET.SubElement(world, 'body', name=name,
                             pos=f"{item['x'] + origin[0]} {item['y'] + origin[1]} {0.9 + origin[2]}",
                             euler=f"0 0 {item['yaw']}")
        ET.SubElement(body, 'freejoint')
        ET.SubElement(body, 'attach', model=name, body=sample, prefix=f'{name}_')
    model = mujoco.MjModel.from_xml_string(ET.tostring(root, encoding='unicode'))
    return model, {k: population[k] for k in ('pattern', 'seed', 'count', 'style')}
