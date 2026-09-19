#!/usr/bin/env python3
"""Seeded layouts for the flasks that stand on the open bench.

Run from simulation/: python scripts/bottle_patterns.py --list.
generate_minihannover_open.py calls it for the population it writes.

The open desk used to carry one fixed crowd: every liquid sample of the
catalogue, scattered with a single hard-coded seed. That is one distribution,
and a detector trained on one distribution learns that one. A *pattern* is
instead a whole layout derived from a single integer: how many flasks stand on
the bench, how tightly they are packed, whether they sit spread out, in
clusters, in rack-like rows or crowded into one end of the worktop, and which
sizes the crowd is made of. Same seed, same bench, down to the millimetre.

Everything a pattern needs is drawn from the seed in a fixed order, so a seed
is the whole definition; nothing else has to be stored or passed around.
``CATALOGUE`` names the ten seeds picked for the demo --- chosen by walking
seeds 1.. and keeping ten whose counts spread over the 10..75 range and whose
styles cover all four. See ``--search`` for how that list was produced.

Coordinates are the desk's local frame, the one population.json is written in:
x along the 6 m worktop, y across it, origin at its centre on the floor.
"""
import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np

SIM = Path(__file__).resolve().parents[1]

# The strip of worktop the stock may occupy, from the open desk's own layout:
# the work stations, balances and wash zone live outside it.
STRIP_X = (-2.42, 1.90)
STRIP_Y = (-0.43, 0.43)

COUNT_RANGE = (10, 75)      # flasks on the bench, both ends inclusive
STYLES = ('scatter', 'clusters', 'rows', 'crowd')
GAP_RANGE = (0.004, 0.06)   # clear space between two footprints, m
SPAN_RANGE = (0.55, 1.0)    # share of the strip's length the pattern uses
CROWD_SPAN = (0.22, 0.45)   # ... and the much shorter share a crowd uses
MIX_CONCENTRATIONS = (0.35, 1.0, 4.0)   # lopsided / free / near-even size mixes
CLUSTER_RANGE = (2, 6)      # number of knots a clustered pattern has
CLUSTER_SIGMA = (0.07, 0.22)
ROW_CHOICES = (2, 3, 4)
YAW_RANGE = (-180.0, 180.0)

SIZES = ('flask_10ml', 'flask_20ml', 'flask_30ml', 'flask_50ml', 'flask_100ml')

# The ten demo patterns, in growing order of crowd: 16 to 71 flasks, spacing
# from 8 mm (shoulder to shoulder) to 57 mm (an arm's width of bench between
# neighbours), every style represented. Seeds, not names, are the identity ---
# p01 is nothing but a readable handle for seed 30. Produced by ``--search``.
CATALOGUE = (30, 176, 21, 327, 1, 31, 70, 4, 2, 15)

PLACE_ATTEMPTS = 40000      # rejection draws before a pattern gives up on a flask
RELAX = 0.82                # and how much of the gap it keeps when it retries


@dataclass(frozen=True)
class Pattern:
    """A tabletop layout, fully determined by its seed.

    Attributes:
        seed: The integer the whole layout is drawn from.
        name: Readable handle, ``p<NN>`` for a catalogue seed, ``s<seed>`` else.
        count: How many flasks stand on the bench.
        style: One of ``STYLES``; how the positions are distributed.
        gap: Clear space asked for between two footprints, in metres.
        span: Share of the strip's length the flasks are spread over.
        centre: Where that span sits, as a fraction of the strip (0 = left end).
        size_mix: Weight per entry of ``SIZES``, summing to one.
        clusters: Number of knots, for the ``clusters`` style.
        sigma: Spread of a knot in metres, for the ``clusters`` style.
        rows: Number of rows, for the ``rows`` style.
    """

    seed: int
    name: str
    count: int
    style: str
    gap: float
    span: float
    centre: float
    size_mix: tuple[float, ...]
    clusters: int = 0
    sigma: float = 0.0
    rows: int = 0

    @property
    def x_window(self) -> tuple[float, float]:
        """The stretch of worktop this pattern actually uses, in metres."""
        length = STRIP_X[1] - STRIP_X[0]
        half = self.span * length / 2
        middle = STRIP_X[0] + self.centre * length
        # Slide the window back inside the strip rather than clipping it, so a
        # narrow crowd keeps its width wherever its centre landed.
        middle = min(max(middle, STRIP_X[0] + half), STRIP_X[1] - half)
        return middle - half, middle + half

    def summary(self) -> str:
        """One line for --list: seed, name and what the layout looks like."""
        mix = '/'.join(f'{w * 100:.0f}' for w in self.size_mix)
        return (f'{self.name}  seed {self.seed:>3}  {self.count:>2} flasks  '
                f'{self.style:<8} gap {self.gap * 1000:>4.0f} mm  '
                f'span {self.span:.2f}  mix {mix}')


def pattern_for(seed: int) -> Pattern:
    """Draw the whole layout for one seed.

    The draw order is part of the contract: inserting a call here renumbers
    every existing pattern, so new knobs go at the end.

    Args:
        seed: Any non-negative integer.

    Returns:
        The pattern that seed stands for.
    """
    rng = np.random.default_rng(seed)
    count = int(rng.integers(COUNT_RANGE[0], COUNT_RANGE[1] + 1))
    style = STYLES[int(rng.integers(len(STYLES)))]
    gap = float(rng.uniform(*GAP_RANGE))
    span_range = CROWD_SPAN if style == 'crowd' else SPAN_RANGE
    span = float(rng.uniform(*span_range))
    centre = float(rng.uniform(0.0, 1.0))
    concentration = float(rng.choice(MIX_CONCENTRATIONS))
    size_mix = tuple(float(w) for w in rng.dirichlet(np.full(len(SIZES), concentration)))
    clusters = int(rng.integers(*CLUSTER_RANGE)) if style == 'clusters' else 0
    sigma = float(rng.uniform(*CLUSTER_SIGMA)) if style == 'clusters' else 0.0
    rows = int(rng.choice(ROW_CHOICES)) if style == 'rows' else 0
    name = f'p{CATALOGUE.index(seed) + 1:02d}' if seed in CATALOGUE else f's{seed}'
    return Pattern(seed=seed, name=name, count=count, style=style, gap=gap,
                   span=span, centre=centre, size_mix=size_mix,
                   clusters=clusters, sigma=sigma, rows=rows)


def by_name(handle: str) -> Pattern:
    """Look a pattern up by catalogue name (``p03``), or by raw seed (``23``)."""
    if handle.isdigit():
        return pattern_for(int(handle))
    if handle.startswith('s') and handle[1:].isdigit():
        return pattern_for(int(handle[1:]))
    if handle.startswith('p') and handle[1:].isdigit():
        index = int(handle[1:]) - 1
        if 0 <= index < len(CATALOGUE):
            return pattern_for(CATALOGUE[index])
    raise SystemExit(f'unknown pattern {handle!r}; try --list')


def catalogue() -> list[Pattern]:
    """The ten demo patterns, in catalogue order."""
    return [pattern_for(seed) for seed in CATALOGUE]


def pick_samples(pattern: Pattern, samples: dict, vessels: dict) -> list[dict]:
    """Choose which catalogue flasks make up this pattern's crowd.

    A sample's size is fixed by the catalogue, so the pattern cannot ask for a
    50 ml flask and put any label on it: it draws a *class* by the size mix and
    then takes an unused sample of that class. Classes run out (the catalogue
    holds 40 of each), and when one does its weight is spread over the rest.

    Args:
        pattern: The layout being built.
        samples: ``manifest['samples']``, already filtered to what may be used.
        vessels: ``manifest['vessels']``, for the class dimensions.

    Returns:
        One record per flask: sample id, vessel class and footprint radius.
    """
    rng = np.random.default_rng(pattern.seed + 1_000)
    pools = {size: [k for k, v in sorted(samples.items())
                    if v['vessel_class'] == size] for size in SIZES}
    for pool in pools.values():
        rng.shuffle(pool)
    available = sum(len(pool) for pool in pools.values())
    if pattern.count > available:
        raise SystemExit(f'pattern {pattern.name} wants {pattern.count} flasks, '
                         f'catalogue offers {available}')
    weights = np.array(pattern.size_mix, float)
    records = []
    for _ in range(pattern.count):
        live = np.array([len(pools[size]) > 0 for size in SIZES])
        share = np.where(live, weights, 0.0)
        share = share / share.sum() if share.sum() > 0 else live / live.sum()
        size = SIZES[int(rng.choice(len(SIZES), p=share))]
        sample_id = pools[size].pop()
        records.append(dict(sample_id=sample_id, vessel_class=size,
                            radius=vessels[size]['diameter_m'] / 2))
    return records


def _draw(pattern: Pattern, rng, radius: float, window: tuple[float, float],
          knots) -> tuple[float, float]:
    """One candidate position for a flask of the given radius."""
    lo, hi = window[0] + radius, window[1] - radius
    y_lo, y_hi = STRIP_Y[0] + radius, STRIP_Y[1] - radius
    if pattern.style == 'clusters':
        cx, cy = knots[int(rng.integers(len(knots)))]
        return (float(np.clip(rng.normal(cx, pattern.sigma), lo, hi)),
                float(np.clip(rng.normal(cy, pattern.sigma), y_lo, y_hi)))
    return float(rng.uniform(lo, hi)), float(rng.uniform(y_lo, y_hi))


def _scatter(pattern: Pattern, records: list[dict], gap: float, rng) -> list[dict] | None:
    """Place every flask by rejection sampling, or give up and return None."""
    window = pattern.x_window
    knots = None
    if pattern.style == 'clusters':
        cluster_rng = np.random.default_rng(pattern.seed + 2_000)
        knots = [(cluster_rng.uniform(window[0] + 0.1, window[1] - 0.1),
                  cluster_rng.uniform(STRIP_Y[0] + 0.1, STRIP_Y[1] - 0.1))
                 for _ in range(pattern.clusters)]
    placed: list[dict] = []
    for record in records:
        radius = record['radius']
        for _ in range(PLACE_ATTEMPTS):
            x, y = _draw(pattern, rng, radius, window, knots)
            if all((x - p['x'])**2 + (y - p['y'])**2
                   > (radius + p['radius'] + gap)**2 for p in placed):
                break
        else:
            return None
        placed.append(dict(record, x=x, y=y))
    return placed


def _rows(pattern: Pattern, records: list[dict], gap: float, rng) -> list[dict] | None:
    """Stand the flasks in rack-like rows, with uneven gaps along each row."""
    window = pattern.x_window
    depth = STRIP_Y[1] - STRIP_Y[0]
    # Rows sit evenly across the strip, each one jittered a little so the bench
    # reads as hand-filled rather than printed.
    offsets = [STRIP_Y[0] + depth * (i + 1) / (pattern.rows + 1)
               for i in range(pattern.rows)]
    lanes: list[list[dict]] = [[] for _ in offsets]
    for i, record in enumerate(records):
        lanes[i % pattern.rows].append(record)
    placed = []
    for lane, y0 in zip(lanes, offsets):
        needed = sum(2 * r['radius'] + gap for r in lane)
        slack = (window[1] - window[0]) - needed
        if slack < 0:
            return None
        share = rng.dirichlet(np.ones(len(lane) + 1)) * slack if lane else []
        x = window[0]
        for record, before in zip(lane, share):
            x += before + gap / 2 + record['radius']
            y = float(np.clip(rng.normal(y0, 0.02),
                              STRIP_Y[0] + record['radius'],
                              STRIP_Y[1] - record['radius']))
            placed.append(dict(record, x=float(x), y=y))
            x += record['radius'] + gap / 2
    return placed


def place(pattern: Pattern, records: list[dict]) -> tuple[list[dict], float]:
    """Give every flask of the pattern a position and a yaw.

    Large flasks go down first: the tightest patterns leave little room, and a
    100 ml flask dropped last into a bench full of 10 ml ones never fits. When
    the asked-for gap turns out to be impossible --- 75 flasks packed 60 mm
    apart into a quarter of the worktop is --- the gap is relaxed in steps
    rather than failing, and the gap actually reached is returned so the
    population file records what the bench really looks like.

    Args:
        pattern: The layout being built.
        records: Flasks from ``pick_samples``.

    Returns:
        The placed flasks, and the gap that worked, in metres.
    """
    ordered = sorted(records, key=lambda r: -r['radius'])
    gap = pattern.gap
    for _ in range(24):
        rng = np.random.default_rng(pattern.seed + 3_000)
        build = _rows if pattern.style == 'rows' else _scatter
        placed = build(pattern, ordered, gap, rng)
        if placed is not None:
            for flask in placed:
                flask['yaw'] = float(rng.uniform(*YAW_RANGE))
            return placed, gap
        gap *= RELAX
    raise SystemExit(f'pattern {pattern.name}: {pattern.count} flasks do not fit '
                     f'on {pattern.span:.2f} of the strip at any spacing')


def describe(pattern: Pattern, placed: list[dict], gap: float) -> dict:
    """The header of a population file: everything but the flasks themselves."""
    return dict(
        seed=pattern.seed,
        pattern=pattern.name,
        style=pattern.style,
        count=len(placed),
        gap_m=round(gap, 5),
        gap_requested_m=round(pattern.gap, 5),
        span=round(pattern.span, 4),
        x_window=[round(v, 4) for v in pattern.x_window],
        size_mix={size: round(w, 4) for size, w in zip(SIZES, pattern.size_mix)},
        clusters=pattern.clusters,
        rows=pattern.rows,
    )


def search(limit: int = 600, wanted: int = 10, apart: int = 5,
           gap_apart: float = 0.004) -> list[Pattern]:
    """Walk seeds and keep a spread-out set --- how ``CATALOGUE`` was chosen.

    A seed is kept when both its count and its spacing sit clear of every seed
    already kept, so the ten differ in crowd *and* in how tight that crowd is;
    a first pass only keeps seeds bringing in a style not yet represented, so
    the ten cover all four. The thresholds are the loosest pair that still
    fills ten slots: ask for six apart in count, or 5 mm in spacing, and the
    walk saturates at nine and seven.

    Args:
        limit: Highest seed to consider.
        wanted: How many patterns to keep.
        apart: Smallest allowed difference between two kept counts.
        gap_apart: Smallest allowed difference between two kept spacings, m.

    Returns:
        The chosen patterns, from the smallest crowd to the largest.
    """
    kept: list[Pattern] = []
    for style_first in (True, False):
        for seed in range(1, limit + 1):
            if len(kept) >= wanted:
                break
            pattern = pattern_for(seed)
            if any(abs(pattern.count - k.count) < apart for k in kept):
                continue
            if any(abs(pattern.gap - k.gap) < gap_apart for k in kept):
                continue
            if style_first and pattern.style in {k.style for k in kept}:
                continue
            kept.append(pattern)
    return sorted(kept, key=lambda p: p.count)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--list', action='store_true',
                        help='print the ten catalogue patterns')
    parser.add_argument('--seed', type=int, help='describe one seed instead')
    parser.add_argument('--search', action='store_true',
                        help='re-run the walk that picked the catalogue seeds')
    args = parser.parse_args()
    if args.search:
        for pattern in search():
            print(pattern.summary())
        print('seeds:', tuple(p.seed for p in search()))
    elif args.seed is not None:
        print(pattern_for(args.seed).summary())
    else:
        for pattern in catalogue():
            print(pattern.summary())


if __name__ == '__main__':
    main()
