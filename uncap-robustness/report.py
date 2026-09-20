#!/usr/bin/env python3
"""out/results.csv -> out/report.html, one self-contained page.

    python uncap-robustness/report.py              # with representative frames (re-simulated, EGL)
    python uncap-robustness/report.py --no-frames

Every number on the page is computed here from the CSV: the sanity checks
S1-S3, the success rates with Wilson intervals, the tolerances and the
first-failure counts (README.md says how each is defined). Nothing in the
page's text states a result that is not computed from the data.
"""
import argparse
import base64
import csv
import json
import math
import os
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from multiprocessing import Pool
from pathlib import Path

os.environ.setdefault('MUJOCO_GL', 'egl')
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scene  # noqa: E402
import sweep  # noqa: E402


def median(v: list) -> float | None:
    v = sorted(v)
    return v[len(v) // 2] if v else None

RESULTS, OUT, FRAMES = HERE / 'out/results.csv', HERE / 'out/report.html', HERE / 'out/frames'
V1 = HERE / 'out/v1_original_rig.csv'
STAGES = ('table', 'rig_clear', 'grip', 'lift', 'uncap', 'cap_away', 'reach_liquid', 'recap', 'place')
FACTORS = ('pitch', 'approach', 'yaw', 'dx', 'dy')
S2_METRICS_MM = ('pad_height_mm', 'lift_mm', 'tip_submerged_mm', 'cap_to_seat_mm', 'recap_lift_mm', 'placed_error_mm')
S2_METRICS_DEG = ('placed_tilt_deg', 'tilt_in_hand_deg')
FRAME_KEYS = {'': ('away', 'dive', 'end'), 'table': ('grip',), 'rig_clear': ('away',), 'grip': ('grip', 'uncap'), 'lift': ('grip', 'away'),
              'uncap': ('uncap', 'away'), 'cap_away': ('away', 'dive'), 'reach_liquid': ('dive',),
              'recap': ('recap', 'end'), 'place': ('end',)}
NUMERIC = {'bottle', 'fill', 'pitch', 'yaw', 'dx', 'dy'}


def load(path: Path = RESULTS) -> list[dict]:
    rows = []
    with path.open() as f:
        for r in csv.DictReader(f):
            for k, v in r.items():
                if v in ('True', 'False'):
                    r[k] = v == 'True'
                elif v == '':
                    r[k] = None
                elif k not in ('id', 'design', 'varied', 'approach', 'first_failure', 'error'):
                    try:
                        r[k] = float(v)
                    except ValueError:
                        pass
            r['bottle'] = int(r['bottle'])
            r['first_failure'] = r.get('first_failure') or ''
            rows.append(r)
    return rows


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def rate(rows: list[dict]) -> dict:
    k, n = sum(r['success'] for r in rows), len(rows)
    lo, hi = wilson(k, n)
    return {'k': k, 'n': n, 'p': k / n if n else None, 'lo': lo, 'hi': hi}


def sanity(rows: list[dict]) -> list[dict]:
    a = [r for r in rows if r['design'] == 'A']
    nominal = [r for r in a if r['varied'] == 'nominal']
    s1 = [r for r in nominal if r['bottle'] == 60 and r['fill'] == 0.5]
    checks = []
    if s1:
        r = s1[0]
        pad_ok = r.get('pad_height_mm') is not None and abs(r['pad_height_mm'] - r['pad_planned_mm']) <= 5
        checks.append({'name': 'S1', 'what': 'The nominal trial (60 ml, half full) passes every stage',
                       'ok': bool(r['success'] and pad_ok),
                       'detail': (f"first failure: {r['first_failure'] or 'none'}; pads {r.get('pad_height_mm', float('nan')):.1f} mm "
                                  f"on the bottle, planned {r.get('pad_planned_mm', float('nan')):.1f}")})
    else:
        checks.append({'name': 'S1', 'what': 'The nominal trial (60 ml, half full) passes every stage', 'ok': False,
                       'detail': 'not in the results yet'})
    groups = defaultdict(list)
    for r in a:
        if r['varied'] in ('yaw', 'nominal'):
            groups[(r['bottle'], r['fill'])].append(r)
    worst_mm, worst_deg, disagree = 0.0, 0.0, []
    for key, g in groups.items():
        if len({r['first_failure'] for r in g}) > 1:
            disagree.append(f'{key[0]} ml at fill {key[1]:g}: ' + ', '.join(f"yaw {r['yaw']:.0f} → {r['first_failure'] or 'pass'}" for r in g))
        for m in S2_METRICS_MM:
            v = [r[m] for r in g if r.get(m) is not None]
            if len(v) == len(g) and v:
                worst_mm = max(worst_mm, max(v) - min(v))
        for m in S2_METRICS_DEG:
            v = [r[m] for r in g if r.get(m) is not None]
            if len(v) == len(g) and v:
                worst_deg = max(worst_deg, max(v) - min(v))
    checks.append({'name': 'S2', 'what': 'Turning the whole hand about the bottle changes nothing',
                   'ok': not disagree and worst_mm <= 1.0 and worst_deg <= 1.0,
                   'detail': (f'{len(groups)} bottle × fill groups; outcomes differ in {len(disagree)}; widest spread '
                              f'{worst_mm:.2f} mm and {worst_deg:.2f}°'), 'list': disagree})
    div = [r for r in nominal if r.get('diverged')]
    checks.append({'name': 'S3', 'what': 'No nominal trial blew up', 'ok': not div and bool(nominal),
                   'detail': f'{len(div)} of {len(nominal)} nominal trials diverged'})
    return checks


def tolerance(rows: list[dict]) -> dict:
    """Per bottle and numeric factor: the widest run of design-A levels around
    the nominal where every fill succeeds; per bottle, the approaches that do."""
    a = [r for r in rows if r['design'] == 'A']
    out = {}
    for ml in sweep.BOTTLES:
        out[ml] = {}
        for factor, levels in sweep.LEVELS.items():
            ok = {}
            for v in levels:
                cell = [r for r in a if r['bottle'] == ml and r[factor] == v
                        and all(r[f] == sweep.NOMINAL[f] for f in sweep.LEVELS if f != factor)]
                ok[v] = bool(cell) and len(cell) == len(sweep.FILLS) and all(r['success'] for r in cell)
            if factor == 'approach':
                out[ml][factor] = [v for v in levels if ok[v]]
                continue
            nominal = sweep.NOMINAL[factor]
            if not ok.get(nominal):
                out[ml][factor] = None
                continue
            i = levels.index(nominal)
            lo = hi = i
            while lo > 0 and ok[levels[lo - 1]]:
                lo -= 1
            while hi < len(levels) - 1 and ok[levels[hi + 1]]:
                hi += 1
            out[ml][factor] = [levels[lo], levels[hi]]
    return out


def heatmaps(rows: list[dict]) -> dict:
    """Design A: per factor, bottle x level -> successes over the fills."""
    a = [r for r in rows if r['design'] == 'A']
    out = {}
    for factor, levels in sweep.LEVELS.items():
        grid = []
        for ml in sweep.BOTTLES:
            line = []
            for v in levels:
                cell = [r for r in a if r['bottle'] == ml and r[factor] == v
                        and all(r[f] == sweep.NOMINAL[f] for f in sweep.LEVELS if f != factor)]
                fails = Counter(r['first_failure'] for r in cell if not r['success'])
                line.append({'k': sum(r['success'] for r in cell), 'n': len(cell),
                             'fail': fails.most_common(1)[0][0] if fails else ''})
            grid.append(line)
        out[factor] = {'levels': list(levels), 'grid': grid}
    return out


def compare(rows: list[dict]) -> dict | None:
    """v1 (original rig) against this run, bottle by bottle, on the same design."""
    if not V1.exists():
        return None
    old = load(V1)
    ids = {r['id'] for r in rows} & {r['id'] for r in old}
    out = {'n_paired': len(ids), 'bottles': {}}
    for ml in sweep.BOTTLES:
        line = {}
        for name, rs in (('v1', old), ('v2', rows)):
            sel = [r for r in rs if r['bottle'] == ml and r['id'] in ids]
            line[name] = {'A': rate([r for r in sel if r['design'] == 'A']), 'B': rate([r for r in sel if r['design'] == 'B']),
                          'first': dict(Counter(r['first_failure'] or 'success' for r in sel))}
        a = {r['id']: r['success'] for r in old if r['bottle'] == ml and r['id'] in ids}
        b = {r['id']: r['success'] for r in rows if r['bottle'] == ml and r['id'] in ids}
        line['gained'] = sum(1 for i in a if b[i] and not a[i])
        line['lost'] = sum(1 for i in a if a[i] and not b[i])
        out['bottles'][str(ml)] = line
    for name, rs in (('v1', old), ('v2', rows)):
        sel = [r for r in rs if r['id'] in ids]
        out[name] = {'A': rate([r for r in sel if r['design'] == 'A']), 'B': rate([r for r in sel if r['design'] == 'B'])}
    return out


def pick_examples(rows: list[dict]) -> list[dict]:
    ex = []
    for ml in sweep.BOTTLES:
        r = next((r for r in rows if r['design'] == 'A' and r['varied'] == 'nominal' and r['bottle'] == ml and r['fill'] == 0.5), None)
        if r:
            ex.append({'why': f'{ml} ml, nominal', 'row': r})
    seen = {e['row']['first_failure'] for e in ex}
    for stage in STAGES:
        if stage in seen:
            continue
        cands = [r for r in rows if r['first_failure'] == stage]
        cands.sort(key=lambda r: (r['bottle'] != 60, r['design'] != 'A', r['fill'] != 0.5))
        if cands:
            ex.append({'why': f'first failure: {stage}', 'row': cands[0]})
    return ex


def render(example: dict) -> dict:
    import trial
    r = example['row']
    keys = FRAME_KEYS.get(r['first_failure'], ('end',))
    stem = FRAMES / r['id']
    p = {k: r[k] for k in trial.NOMINAL}
    trial.run_trial(p, frames=stem, frame_keys=keys, frame_size=(300, 400))
    shots = []
    for k in keys:
        f = stem.parent / f'{stem.name}_{k}.png'
        if f.exists():
            shots.append({'key': k, 'src': 'data:image/png;base64,' + base64.b64encode(f.read_bytes()).decode()})
    return {'why': example['why'], 'id': r['id'], 'first_failure': r['first_failure'], 'frames': shots}


def commit() -> str:
    try:
        return subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=HERE, capture_output=True, text=True).stdout.strip()
    except OSError:
        return '?'


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--no-frames', action='store_true')
    a = ap.parse_args()
    rows = load()
    b = [r for r in rows if r['design'] == 'B']
    per_bottle = {ml: {'A': rate([r for r in rows if r['bottle'] == ml and r['design'] == 'A']),
                       'B': rate([r for r in b if r['bottle'] == ml]),
                       'stages': {s: sum(1 for r in rows if r['bottle'] == ml and r.get(f'ok_{s}')) for s in STAGES},
                       'n': sum(1 for r in rows if r['bottle'] == ml),
                       'first': Counter(r['first_failure'] or 'success' for r in rows if r['bottle'] == ml)}
                  for ml in sweep.BOTTLES}
    frames = []
    if not a.no_frames:
        FRAMES.mkdir(parents=True, exist_ok=True)
        with Pool(min(12, os.cpu_count() or 4)) as pool:
            frames = pool.map(render, pick_examples(rows))
    keep = ('id', 'design', 'varied', 'bottle', 'fill', 'pitch', 'approach', 'yaw', 'dx', 'dy', 'success', 'first_failure',
            'pad_height_mm', 'lift_mm', 'slip_mm', 'tilt_in_hand_deg', 'blade_slip_turns', 'cap_to_seat_mm', 'cap_off_axis_mm',
            'tip_submerged_mm', 'tip_off_axis_mm', 'bottle_tilt_dive_deg', 'liquid_to_shoulder_mm', 'recap_lift_mm',
            'placed_error_mm', 'placed_tilt_deg', 'liquid_g', 'neck_mm', 'bottle_d_mm', 'wall_s', 'error',
            'seated', 'seat_torque_Nm', 'seat_extra_turns')
    data = {
        'meta': {'commit': commit(), 'date': date.today().isoformat(), 'n': len(rows), 'nA': len(rows) - len(b), 'nB': len(b),
                 'design_n': len(sweep.design()), 'levels': sweep.LEVELS, 'nominal': sweep.NOMINAL, 'fills': sweep.FILLS,
                 'bottles': sweep.BOTTLES, 'stages': STAGES,
                 'wall_median': median([r['wall_s'] for r in rows if r.get('wall_s')]),
                 'sim_s': median([r['sim_s'] for r in rows if r.get('sim_s')]),
                 'timestep_ms': 1e3 * scene.PHYSICS['timestep']},
        'sanity': sanity(rows), 'overall': {'A': rate([r for r in rows if r['design'] == 'A']), 'B': rate(b)},
        'per_bottle': {str(k): {**v, 'first': dict(v['first'])} for k, v in per_bottle.items()},
        'tolerance': {str(k): v for k, v in tolerance(rows).items()}, 'heat': heatmaps(rows),
        'rows': [{k: r.get(k) for k in keep} for r in rows], 'frames': frames,
        'compare': compare(rows),
    }
    page = TEMPLATE.replace('/*DATA*/', 'window.REPORT=' + json.dumps(data, separators=(',', ':')) + ';')
    OUT.write_text(page)
    print(f'wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB): {len(rows)} trials, {len(frames)} examples')
    for c in data['sanity']:
        print(f"  {c['name']} {'ok  ' if c['ok'] else 'FAIL'} {c['detail']}")


TEMPLATE = (HERE / 'report_template.html').read_text() if (HERE / 'report_template.html').exists() else ''

if __name__ == '__main__':
    main()
