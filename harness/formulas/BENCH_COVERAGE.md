# Which bench can make which formula

A formula is a requirement; a bench is what happens to be standing on it. The two
are set independently, and crossing them is what decides whether a run is worth
watching. This table is that crossing, for the five formulas against the ten
bench populations in `simulation/assets/minihannover_open/patterns/`.

It exists because the default rail bench makes almost none of them. FRG-101 asks
for 18 materials and resolves 5, and for a long time that looked like a detector
problem. It is not: the trained YOLO26n identifies **every liftable bottle on
that bench**, and so does a perfect detector reading the simulator's own labels.
Both still give 5. The limit is the population, and the only way to move it is to
put different bottles on the bench.

## Coverage

Ingredients the bench can supply, out of the formula's total. Every bottle a
pattern places is attached with a `<freejoint>`
(`view/backend/scene_patterns.py`), so for these populations *present* and
*liftable* are the same thing and the number is the executable ceiling.

| | p01 | p02 | p03 | p04 | p05 | p06 | p07 | p08 | **p09** | p10 | default bench |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **FRG-101** Orange Blossom Water | 7 | 8 | 13 | 14 | 13 | 17 | 13 | 15 | **18/18** | 17 | 5/18 |
| **FRG-102** Modern Damask Rose | 5 | 7 | 5 | 8 | 11 | 12 | 9 | 12 | **14/14** | 12 | 3/14 |
| **FRG-103** Lily of the Valley Garden | 4 | 8 | 7 | 9 | 12 | 13 | 12 | 12 | **15/15** | 12 | 5/15 |
| **FRG-104** Night Spice | 5 | 9 | 8 | 8 | 11 | 15 | 14 | 14 | 16/17 | 16 | 6/17 |
| **FRG-105** Green Fruit | 4 | 8 | 8 | 12 | 12 | 17 | 14 | 15 | **18/18** | 16 | 2/18 |

## The patterns

| | style | seed | bottles | distinct materials |
| --- | --- | --- | --- | --- |
| p01 | scatter | 30 | 16 | 12 |
| p02 | crowd | 176 | 24 | 21 |
| p03 | crowd | 21 | 29 | 21 |
| p04 | rows | 327 | 35 | 25 |
| p05 | rows | 1 | 41 | 31 |
| p06 | crowd | 31 | 46 | 38 |
| p07 | clusters | 70 | 52 | 31 |
| p08 | crowd | 4 | 57 | 34 |
| **p09** | clusters | 2 | 65 | **39** |
| p10 | rows | 15 | 71 | 37 |

The catalogue holds 40 liquids. Bottle count and coverage are only loosely
related --- p10 puts out the most bottles and still loses to p09, because it
spends them on sizes of materials it already has.

## Use p09

It completes four of the five formulas. Nothing else completes any.

The near misses are worth knowing, since they are one bottle wide: p06 lacks
only Linalool for FRG-101 and FRG-105, and p10 lacks only alpha-Terpineol for
FRG-101.

**FRG-104 cannot be completed by any pattern.** Its best is p09 at 16/17, short
of Anethole; p10 also reaches 16, short of Phenylethyl alcohol. Making Night
Spice needs a population authored for it.

## The held-out set

`validation/` holds five more formulas, written by the same script from the same
catalogue but kept out of whatever the first five get tuned against. They were
not consulted while choosing p09, which makes them the honest test of it --- and
p09 completes four of those five too:

| | | on p09 |
| --- | --- | --- |
| **FRG-201** | Hyacinth Field | **16/16** |
| **FRG-202** | Pine Trail | **17/17** |
| **FRG-203** | Marzipan Anise | 18/19 |
| **FRG-204** | Citrus Mint | **17/17** |
| **FRG-205** | Violet Powder | **16/16** |

The one miss is Anethole again, the same bottle FRG-104 wants. Two formulas out
of ten blocked by one absent material is a sharper argument for authoring a
population than any of the coverage numbers above.

They are asked for by id like the others --- `run_formula.py FRG-203` --- since a
run on unseen input that costs extra keystrokes is a run nobody makes.

## What it looks like when it works

FRG-101 on p09, every ingredient resolved and no bottle welded down:

```
ok    heap     18/18 executable, 180 actions
  ok    Limonene              2.540 g  SMP-0001   10 ml
  ok    Linalyl acetate       1.600 g  SMP-0091   10 ml
  ...
  ok    Citral                0.200 g  SMP-0020  100 ml
  ...
  18/18 executable, 0 unliftable, 0 not on this bench
```

Most ingredients land in a 10 ml flask --- the smallest that holds the dose ---
but Citral takes the 100 ml and Nerol the 50 ml, because p09 placed no smaller
flask of those. That is the tie-break in `formula_to_actions.choose` working, not
a defect.

Against the default bench the same formula covers 30.3 % of the concentrate by
mass: Limonene at 25.4 % is absent and Linalool at 12 % is welded scenery. On p09
it covers all of it.

That whole run is committed as `harness/FRG-101_p09_actions.json` --- 18 resolved
ingredients and the 180 actions they expand into --- so the shape of the heap can
be read without a bench, a scan or the pattern script. It is an output, not an
input: nothing reads it back, and `run_formula.py` will write a fresh one over
`simulation/out/` on any run.

## Reproducing this

The patterns are applied in memory by `view/backend/scene_patterns.build_pattern`
for the viewer. The harness scans scenes by path, so the population has to be
written out as a scene first; that step is not yet a committed script.

Once the scene exists:

    simulation/.venv/bin/python harness/run_formula.py FRG-101 \
        --scene simulation/out/minihannover_rail_p09.xml --method gt

Drop `--method gt` to scan with the detector instead. Note the cost: p09 puts 65
bottles on the bench against the default 25, and the confirming pass renders a
view per bottle it cannot already name.

## A caveat on these numbers

Coverage is counted by intersecting each ingredient's five candidate sample ids
with the ids a pattern places. It answers "could this bench supply it", which is
a fact about the population alone. It does not ask whether the arm can reach the
bottle where the pattern put it: `rail_kinematics.reach` can fail on a station
the carriage cannot serve, and a crowded population can put one bottle behind
another. Those only show up in a real scan.
