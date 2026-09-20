"""Build the rail viewport from the shared four-pattern catalogue in memory.

``build_pattern`` is what the viewer and the USD export call: the rail scene
with one catalogue layout on its bench, compiled without touching the disk.
``pattern_scene`` is the same composition one step earlier, as XML, for the
callers that need a file --- the vision scan loads its scene by path:

    python view/backend/scene_patterns.py --pattern p04 --out out/p04_scene.xml
"""
import argparse
import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

import mujoco

SIM = Path(__file__).resolve().parents[2] / 'simulation'
if str(SIM / 'scripts') not in sys.path:
    sys.path.insert(0, str(SIM / 'scripts'))
import generate_open_vessels as open_vessels  # noqa: E402
PATTERNS = SIM / 'assets/minihannover_open/patterns'
CATALOGUE = json.loads((PATTERNS / 'index.json').read_text())['patterns']


def pattern_scene(scene_path, name):
    """Compose the rail scene with one catalogue layout standing on its bench.

    Every reference to another file is rewritten absolute, so the tree compiles
    from a string or from a file written anywhere.

    Args:
        scene_path: The rail scene to start from.
        name: A catalogue pattern, ``p01`` through ``p04``.

    Returns:
        The composed XML root and the layout's ``pattern``, ``seed``, ``count``
        and ``style``.
    """
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
    containers = [item for item in population['containers']
                  if item['container_ml'] != 10]
    # The open copy of each flask, not the catalogue's own. They are the same
    # bottle with two things added: a liquid column the dosing draws down, and a
    # site at the mouth to aim at. Without them a pattern bench holds no liquid
    # at all --- every dose came out as 0 ml and nothing moved --- while the rail
    # scene's own bench, which has always used these, dosed fine.
    open_vessels.main_for([item['sample_id'] for item in containers])
    for item in containers:
        sample = item['sample_id']
        name = f'dyn_{sample}'
        ET.SubElement(asset, 'model', name=name,
                      file=str(SIM / 'assets/open_vessels' / f'{sample}.xml'))
        body = ET.SubElement(world, 'body', name=name,
                             pos=f"{item['x'] + origin[0]} {item['y'] + origin[1]} {0.9 + origin[2]}",
                             euler=f"0 0 {item['yaw']}")
        ET.SubElement(body, 'freejoint')
        ET.SubElement(body, 'attach', model=name, body=sample, prefix=f'{name}_')
    metadata = {k: population[k] for k in ('pattern', 'seed', 'style')}
    metadata['count'] = len(containers)
    return root, metadata


def build_pattern(scene_path, name):
    """The compiled model of one catalogue layout on the rail bench."""
    root, metadata = pattern_scene(scene_path, name)
    model = mujoco.MjModel.from_xml_string(ET.tostring(root, encoding='unicode'))
    return model, metadata


def main():
    """Write one pattern's scene to a file, for the callers that need a path.

    The file carries absolute asset paths, so it is a scratch build of this
    machine's checkout, not something to commit: write it under
    ``simulation/out/``, which is gitignored.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pattern', required=True, help='p01 through p04')
    parser.add_argument('--scene', type=Path,
                        default=SIM / 'models/minihannover_rail_scene.xml')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root, metadata = pattern_scene(args.scene, args.pattern)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root, space='  ')
    args.out.write_text('<?xml version="1.0" encoding="utf-8"?>\n'
                        + ET.tostring(root, encoding='unicode') + '\n')
    print(f"wrote {args.out}: {metadata['pattern']} (seed {metadata['seed']}, "
          f"{metadata['count']} flasks, {metadata['style']})")


if __name__ == '__main__':
    main()
