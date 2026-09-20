#!/usr/bin/env python3
"""Run the robustness sweep and append every trial to out/results.csv.

    python uncap-robustness/sweep.py --quick          # 8 trials, to see it works
    python uncap-robustness/sweep.py --workers 15     # the whole design (README.md)

Resumable: a trial whose id is already in the CSV is skipped, so an
interrupted sweep continues where it stopped. The design is fixed here and in
README.md before the run:

* A, one factor at a time, for every bottle x fill: around the nominal
  (pitch 0, approach above, yaw 0, dx = dy = 0) each factor alone over its
  levels;
* B, all factors at once, drawn at random (seed 0) for the three bottles
  whose cap the clamp can reach and that clear the table in the nominal pose
  (50, 60, 100 ml; the pilot in README.md).
"""
import argparse
import csv
import random
import sys
import time
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

RESULTS = HERE / 'out/results.csv'
BOTTLES = (10, 20, 30, 50, 60, 100)
FILLS = (0.25, 0.5, 0.8)
LEVELS = {
    'pitch': (-20, -10, -5, 0, 5, 10, 20),
    'approach': ('above', 'side', 'diagonal'),
    'yaw': (0, 90, 180, 270),
    'dx': (-6, -3, 0, 3, 6),
    'dy': (-6, -3, 0, 3, 6),
}
NOMINAL = {'pitch': 0, 'approach': 'above', 'yaw': 0, 'dx': 0, 'dy': 0}
RANDOM_N, RANDOM_BOTTLES, SEED = 240, (50, 60, 100), 0


def trial_id(p: dict) -> str:
    return (f"{p['design']}-{p['bottle']}ml-f{p['fill']:.2f}-p{p['pitch']:+.1f}-{p['approach']}"
            f"-y{p['yaw']:.0f}-x{p['dx']:+.1f}-y{p['dy']:+.1f}")


def design() -> list[dict]:
    trials, seen = [], set()
    for ml in BOTTLES:
        for fill in FILLS:
            for factor, levels in LEVELS.items():
                for v in levels:
                    p = {'design': 'A', 'bottle': ml, 'fill': fill, **NOMINAL, factor: v}
                    p['varied'] = factor if v != NOMINAL[factor] else 'nominal'
                    if trial_id(p) not in seen:
                        seen.add(trial_id(p))
                        trials.append(p)
    rng = random.Random(SEED)
    for _ in range(RANDOM_N):
        trials.append({'design': 'B', 'varied': 'all', 'bottle': rng.choice(RANDOM_BOTTLES), 'fill': rng.choice(FILLS),
                       'pitch': round(rng.uniform(-20, 20), 1), 'approach': rng.choice(LEVELS['approach']),
                       'yaw': round(rng.uniform(0, 360)), 'dx': round(rng.uniform(-6, 6), 1),
                       'dy': round(rng.uniform(-6, 6), 1)})
    for p in trials:
        p['id'] = trial_id(p)
    return trials


def one(p: dict) -> dict:
    import trial
    try:
        out = trial.run_trial({k: p[k] for k in trial.NOMINAL})
    except Exception as e:     # a crash is a result too, and must not stop the sweep
        out = {'error': repr(e), 'success': False, 'first_failure': 'error'}
    return {'id': p['id'], 'design': p['design'], 'varied': p['varied'], **out}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--workers', type=int, default=15)
    ap.add_argument('--quick', action='store_true')
    a = ap.parse_args()
    trials = design()
    if a.quick:
        trials = [t for t in trials if t['bottle'] == 60 and t['fill'] == 0.5][:8]
    RESULTS.parent.mkdir(exist_ok=True)
    done = set()
    if RESULTS.exists():
        with RESULTS.open() as f:
            done = {row['id'] for row in csv.DictReader(f)}
    todo = [t for t in trials if t['id'] not in done]
    print(f'{len(trials)} trials in the design, {len(done)} done, {len(todo)} to run on {a.workers} workers')
    fields = None
    if RESULTS.exists() and done:
        with RESULTS.open() as f:
            fields = next(csv.reader(f))
    start, pending = time.time(), []
    with Pool(a.workers, maxtasksperchild=10) as pool:
        for n, row in enumerate(pool.imap_unordered(one, todo), 1):
            pending.append(row)
            if fields is None and 'error' not in row:     # the header comes from a full row
                fields = ['id', 'design', 'varied', *[k for k in row if k not in ('id', 'design', 'varied')], 'error']
                with RESULTS.open('w', newline='') as f:
                    csv.writer(f).writerow(fields)
            if fields is not None:
                with RESULTS.open('a', newline='') as f:
                    w = csv.DictWriter(f, fields, extrasaction='ignore')
                    for r in pending:
                        w.writerow({k: ('' if v is None else v) for k, v in r.items()})
                pending = []
            left = (time.time() - start) / n * (len(todo) - n)
            print(f'[{n}/{len(todo)}] {row["id"]}: {row.get("first_failure") or "ok"}  (~{left / 60:.0f} min left)',
                  flush=True)


if __name__ == '__main__':
    main()
