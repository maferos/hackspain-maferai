# Read confidence: how sure is the reader that this is the right sample?

Question: when the wrist camera reads a bottle, can the reader say **with what probability** the code it
extracted is the right one? A corrupted read that still resolves to a valid sample would chain the wrong
compound to the scanned pot, and nothing downstream could tell that apart from a correct read.

This document is the argument and the measurements behind it. **Nothing here is implemented yet** — it
exists so the team can read it and decide. Work branch: `ng/read-confidence`.

Measured on 19 September 2026, `opencv-python` 4.9.0, macOS / Python 3.11, against
`DICT_4X4_250` and the 200-row `barcodes/lookup_table.json`.

## The failure that matters is the silent one

A marker that fails to read is harmless: the arm steps closer and tries again — that is exactly what
`scripts/wrist_scan.py` already does. The dangerous outcome is a read that returns a **valid but wrong
id**, because every id resolves through the lookup table to a real sample.

So the useful question is not "did it read?" but "how likely is this the right bottle?". Today the
pipeline cannot answer it at all.

## What the reader gives us today: nothing

`detector.detectMarkers(frame)` returns corners and ids and no more. The soft information it computed
internally — the per-cell grey levels before thresholding, and how many bits had to be corrected — is
discarded. There is no confidence, no runner-up, no bit-error count.

Worth stating plainly: **there is no ArUco reader in `labvision/`**. `detectMarkers` appears only in
`scripts/aruco_experiment.py`, `scripts/ring_experiment.py` and `scripts/wrist_scan.py`. The only library
reader is `labvision/reader.py`, which is EAN-13.

## Measured: how far apart the codewords actually are

Rendering all 250 markers and comparing their 4x4 bit matrices, minimised over the four rotations:

| Quantity | Value |
|---|---|
| Minimum inter-marker Hamming distance | **3** |
| Minimum self-distance under rotation | 4 |
| `dictionary.maxCorrectionBits` | 1 |
| Default `DetectorParameters.errorCorrectionRate` | 0.6 |
| Pairs at distance 3 among the 200 ids in use | **637** |

`Dictionary::identify` corrects `int(maxCorrectionBits * errorCorrectionRate)` bits, which on the defaults
is `int(1 * 0.6) = 0`. Verified by flipping bits in a clean marker and calling `dictionary.identify`:

| Flipped bits | rate 0.6 (default) | rate 1.0 | rate 2.0 |
|---|---|---|---|
| 0 | id 0 | id 0 | id 0 |
| 1 | rejected | id 0 | id 0 |
| 2 | rejected | rejected | id 0 |
| 3 | rejected | rejected | **id 31** |

The last cell is the whole problem in one line: marker 0, corrupted in three cells, reported confidently as
marker 31. **Raising `errorCorrectionRate` buys read rate and pays for it in silent misidentification.**

The defaults are therefore the safe setting, and a silent misread needs at least three flipped bits landing
exactly on one of those 637 neighbouring codewords. Rare — but it is eight chances per bottle per frame,
since the ring carries eight copies, over many frames, and nothing currently measures it.

### Reproducing the numbers

```python
import cv2, itertools, numpy as np
d = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

def bits(i):                                   # read the marker back out of its own render
    img = cv2.aruco.generateImageMarker(d, i, 60)
    cell = img.reshape(6, 10, 6, 10).mean(axis=(1, 3))
    return (cell[1:5, 1:5] > 127).astype(int)

R = np.stack([bits(i).flatten() for i in range(250)])
rots = lambda v: [np.rot90(v.reshape(4, 4), k).flatten() for k in range(4)]
print(min(min(int((R[a] != r).sum()) for r in rots(R[b]))
          for a, b in itertools.combinations(range(250), 2)))    # -> 3

b = bits(0); b[0, 0] ^= 1; b[0, 1] ^= 1; b[0, 2] ^= 1
print(d.identify(b.astype(np.uint8), 2.0))                       # -> (True, 31, 0)
```

## Why "just pick ids further apart" does not work here

Only a subset of the dictionary is ever printed, so the ids in use could be chosen for maximum separation
instead of being assigned `0..N-1` as `registry.build_registry` does now. Greedy max-min-distance subsets
of `DICT_4X4_250`:

| Target minimum distance | Ids available |
|---|---|
| 4 | 88 |
| 5 | 25 |
| 6 | 10 |
| 7 | 4 |

The catalogue has 200 samples. This only helps a much smaller catalogue. Real separation means a larger
dictionary — `DICT_5X5_250` has `maxCorrectionBits` 2, `DICT_6X6_250` has 5 — and both cost module size,
which is precisely what bought the ring its read range over the one-sided EAN-13 label. **The trade-off is
range against separation, not a free improvement.**

## The proposed solution

The lever that makes this tractable is unusual and worth naming: **the code space is tiny and fully
known**. 250 dictionary ids, of which only the registry's rows are possible. So the posterior over ids can
be computed by *exact enumeration* — no learned model, no approximation.

**1. Soft-decision decoding, per marker.** Instead of thresholding each cell to a hard bit: rectify the
quad from the corners OpenCV already returns, measure each cell's grey level against black/white references
taken from the marker's own border, and score every candidate id and rotation by summing per-cell
log-likelihoods. An ambiguous grey cell then contributes little evidence rather than a confident wrong bit.
Output per marker: `p_top`, the margin over the runner-up, and diagnostics (px/module, viewing angle, the
least certain cell).

**2. Ring consensus.** Eight copies of the same id round the bottle, so their log-likelihoods add, and
their disagreement is itself the alarm. The honest caveat: the copies are only approximately independent —
they share pose, blur and lighting error, which does not average out — so the fusion needs a calibrated
tempering exponent, not a naive product, or the number will be overconfident.

**3. Registry prior.** Only ids present in `lookup_table.json` are possible, and a work order narrows it
further. A top candidate outside the table is already evidence of corruption; `reader.resolve` computes
exactly that today and throws it away.

**4. Cross-symbology agreement.** Every row carries both a `marker_id` and an EAN-13 `code`. The two
symbologies fail differently, so agreement between them is a strong near-independent check. There is also
free evidence being discarded in EAN-13: `reader.decode_scanline` samples up to 48 rows and **returns on
the first one that decodes**. Tallying all of them costs almost nothing, and the check digit already bounds
the residual error at 1/10.

**5. Calibration and the decision rule.** A number called "confidence" is worthless until a reliability
diagram shows that reads scored 0.99 are right 99% of the time. The render pipeline gives ground truth for
free — `wrist_scan.py` and `ring_experiment.py` already sweep distance, yaw and roll. The honest
deliverable is an **operating point**, silent-error rate against re-scan rate, not an accuracy figure. And
three outcomes rather than two: **accept** / **re-scan from another view** / **flag for a human**.

### Shape of the API

Extend `Detection` with `confidence`, `posterior` (top-k alternatives) and `evidence` (bits corrected,
votes, copies seen, px/module), with defaults that keep current callers working. Add a bottle-level
`ScanResult` that fuses markers and frames, since the unit the robot cares about is "which sample is this
bottle", not "what did this one symbol say".

### Order of work

1. `labvision/markers.py` — an ArUco reader as a library API, instrumented from the start: how many of the
   ring's copies were detected, whether they agree, and the corrected-bit count (recomputable against the
   canonical codeword for the returned id).
2. Scanline votes in the EAN-13 reader. Cheap, no new maths, immediate signal.
3. Soft-decision posterior per marker, plus ring fusion.
4. Calibration harness, reliability diagram, threshold policy.
5. Cross-symbology agreement, if both labels survive on the bottle.

## Open decisions

- **Scope.** ArUco ring only, or ArUco and EAN-13 required to agree?
- **Dictionary.** Does the cost of one wrong chaining justify evaluating `DICT_5X5_250`, losing read range,
  or do we stay on 4x4 and confine ourselves to *measuring* the residual risk?
- **Operating point.** What re-scan rate is acceptable in exchange for what silent-error rate? This has to
  be argued from the consequences in the lab, not picked because it looks good.

## Related

- `README.md` — "The bottles carry an ArUco ring", and the range measurements behind the switch
- `docs/BENCHMARK.md` — the detector side of the vision stack
- `scripts/aruco_experiment.py`, `scripts/ring_experiment.py` — the existing sweeps that would become the
  calibration set
