#!/usr/bin/env python3
"""Export and render the shared ten-layout catalogue, with separate Python environments."""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export-python', type=Path, required=True)
    parser.add_argument('--isaac-python', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--quality', choices=('draft', 'final'), default='draft')
    parser.add_argument('--reuse-exports', action='store_true', help='Reuse existing USD exports with matching pattern and FPS')
    parser.add_argument('--patterns', nargs='+', help='Defaults to all catalogue layouts')
    args = parser.parse_args()
    scripts = Path(__file__).resolve().parent
    catalogue = json.loads((scripts.parent / 'assets/minihannover_open/patterns/index.json').read_text())['patterns']
    selected = args.patterns or [p['pattern'] for p in catalogue]
    if set(selected) - {p['pattern'] for p in catalogue}:
        parser.error('Unknown pattern')
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for pattern in selected:
        print(f'PATTERN {pattern}: export', flush=True)
        export = out / 'exports' / pattern
        rendered = out / pattern
        fps = 10 if args.quality == 'draft' else 30
        existing = export / 'animation.json'
        cached = json.loads(existing.read_text()) if args.reuse_exports and existing.exists() else {}
        if cached.get('pattern') != pattern or cached.get('fps') != fps:
            with (out / f'{pattern}-export.log').open('w') as log:
                subprocess.run([str(args.export_python.absolute()), str(scripts / 'export_rail_animation.py'),
                                '--pattern', pattern, '--fps', '10' if args.quality == 'draft' else '30',
                                '--out', str(export)], stdout=log, stderr=subprocess.STDOUT, check=True)
        print(f'PATTERN {pattern}: render', flush=True)
        with (out / f'{pattern}-render.log').open('w') as log:
            subprocess.run([str(args.isaac_python.absolute()), str(scripts / 'render_rail_isaaclab.py'),
                            '--export', str(export), '--out', str(rendered), '--quality', args.quality,
                            '--headless', '--enable_cameras'], stdout=log, stderr=subprocess.STDOUT, check=True)
        manifest = json.loads((rendered / 'render.json').read_text())
        results.append(dict(pattern=pattern, seed=manifest['seed'], count=manifest['count'],
                            fps=manifest['fps'], frames=manifest['rendered_frames'],
                            resolution=manifest['resolution'], global_video=f'{pattern}/rail_global.mp4',
                            robot_video=f'{pattern}/rail_robot.mp4'))
        (out / 'index.json').write_text(json.dumps(dict(quality=args.quality, patterns=results), indent=2)+'\n')
        print(f'PATTERN {pattern}: complete', flush=True)


if __name__ == '__main__':
    main()
