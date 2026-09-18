# computer-vision

Barcode identity for the lab robot. Every sample on the bench carries a printed
EAN-13 label; the barcode holds nothing but an identifier, and everything the
robot needs to know about the sample is looked up from that identifier in a
table.

Owners: Nacho, Martí (see `AGENTS.md`).

## The idea in one line

```
sample record --sha256--> 12 digits --EAN-13--> printed label
                              |
                       lookup_table.json
                              |
        label --reader--> code --> the sample record back again
```

The barcode is a *pointer*, not a container. Nothing about the material, the
volume or the lot is recoverable from the bars alone — resolving a code always
means consulting the table. That keeps the label stable when a record's
contents change, and keeps the printed symbol to a fixed 95 modules.

## Hash to code

EAN-13 carries twelve free decimal digits plus a check digit, which is far less
than a SHA-256 digest, so the digest is **truncated**:

| Step | Value |
| --- | --- |
| Canonical payload | `SMP-0001\|Limonene\|5989-27-5\|liquid\|10\|LOT-50378` |
| `sha256(payload)` | `59443a004775eea7...` |
| `int(digest, 16) mod 10^9` | `694390669` |
| Prefix `200`, append check digit | `2006943906698` |

The `200` prefix is the GS1 range reserved for internal and in-store codes, so
these will never collide with a real retail product.

Nine digits is about 30 bits. For a hundred samples a collision is very
unlikely, but "very unlikely" is not "impossible", so `build_registry` checks
for one and re-hashes the loser with an incrementing salt until it lands
somewhere free. The salt is recorded in the table, so the mapping stays
reproducible rather than depending on insertion luck.

Because the code is derived from the record, **changing any field changes the
barcode**. Re-print a label after editing a sample.

## Generating the labels

**The label images are not in the repo.** They are deterministic build output —
one command regenerates all 200, byte-identically:

```bash
python -m labvision.registry barcodes
```

That writes one PNG per sample — `barcodes/SMP-XXXX_<code>.png` for liquids and
`barcodes/PWD-XXXX_<code>.png` for powders — and rewrites
`barcodes/lookup_table.json`. Takes a few seconds.

What **is** committed is `barcodes/lookup_table.json` — the lookup table itself,
200 entries keyed by barcode. That one matters: it is the mapping, it is small
and diffable, and a decoded barcode is meaningless without it.

The images are left out because they are ~7 MB of binaries that would be
rewritten wholesale by any change to the renderer. Nothing is lost: the table
pins every code, and the generator is reproducible from it.

Flags worth knowing — `python -m labvision.registry --help`:

| Flag | Effect |
| --- | --- |
| `--count N` | Generate only the first N of the catalogue (liquids first) |
| `--module-px N` | Pixels per barcode module (default 4, floor is 2) |
| `--no-images` | Rewrite only the lookup table |
| `--seed N` | Change the lot numbers, and so every barcode |

## The reader

Two decoders sit behind one `decode_image` call, and their results are merged
rather than raced.

**OpenCV** (`cv2.barcode.BarcodeDetector`) is the primary decoder. It has two
awkward habits worth knowing:

- **It will not find a barcode that fills the frame.** It searches a fixed set of
  scales relative to the image, so a tight crop is invisible to it. The setters
  that used to widen those scales — `setDetectorScales`, `setGradientThreshold` —
  are **no longer exposed** on OpenCV 4.9, so conditioning the image is the only
  lever left. `decode_image` therefore works through a ladder of white padding
  and upscaling.
- **It does not return corner coordinates.** `detectAndDecodeMulti` hands back an
  empty points vector even on a successful decode, on every build tested here.

**The localiser + scanline reader** is the fallback, and the only path that
yields a quad. It closes the thresholded image with a wide, short horizontal
kernel — which melts parallel bars into one solid blob while leaving text alone
— filters the blobs by aspect ratio, rectifies each one, and reads it against
the same module tables the encoder writes with.

The two are unioned because a padding rung that decodes one label in a frame
holding four would otherwise mask the three the localiser had already read.

### Measured behaviour

Over the 200 generated labels: **200/200 decode correctly**, 189 through OpenCV
and 11 only through the fallback, all with a quad, at roughly 260 ms/image.

Also verified: rotation from 0 to 90 degrees, upside-down labels, Gaussian noise
at sigma 12, 3x3 blur, 0.45x downscaling, low contrast, four labels in one
frame, and tight crops that fill the frame. The one hard requirement is that the
**whole symbol including its quiet zones is inside the image** — clip a corner
and it stops decoding.

## The resolution floor

EAN-13 is 95 modules wide, and OpenCV needs roughly **two pixels per module**, so
a label must be about **190 px wide in the frame** to decode.

This is why `render_symbol` takes *pixels per module* rather than a target
width: the caller pins the module width exactly instead of inferring it from an
image size. The default of 4 px/module gives a 460 px label, comfortably clear
of the floor.

The same floor is what forces a two-stage pipeline on real frames — locate the
label at low resolution, then rectify and decode the crop from the
full-resolution frame, never from the downscaled one.

## Why the encoder is hand-written

`python-barcode` would have done the encoding. It is installed here as a test
dependency, and the reason we do not use it for the real thing is narrower than
"one less dependency":

**It cannot decode.** The package is encode-only — there is no reader, scanner
or decoder anywhere in it. So `decode_modules` and the L/G/R tables have to
exist regardless, for `reader.py` to work at all. Using the library would
replace only the encode half and leave the two halves resting on different
tables, which is exactly what the round-trip tests are there to catch.

So the tables are ours, and `python-barcode` is used as an **independent
oracle** instead: `test_ean13.py` checks our check digit and our full 95-module
pattern against it over 1000 random codes. They agree exactly. That is more
value than importing it would have given, and the tests skip cleanly on a
machine without it.

The one genuine ergonomic win is that `render_symbol` takes *pixels per module*
directly. `python-barcode` gets there too, via `module_width` in millimetres
times `dpi`, and lands within a pixel across the symbol — so this is a
convenience, not a capability the library lacks.

## Layout

| Path | Purpose |
| --- | --- |
| `labvision/ean13.py` | Check digit, module encode/decode, rendering |
| `labvision/registry.py` | Samples, hash-to-code, lookup table, label PNGs |
| `labvision/reader.py` | Localiser, both decoders, code-to-sample resolution |
| `tests/` | 108 tests, plus 17 doctests |
| `barcodes/lookup_table.json` | The committed lookup table, 200 entries |

## Usage

```bash
# requirements.txt adds PyPI as an extra index, so this works without touching
# your global pip.conf and without a valid CodeArtifact token
pip install -r requirements.txt

# Generate all 200 labels and the lookup table (labels are gitignored)
python -m labvision.registry barcodes

# Read a label back and resolve it
python -m labvision.reader barcodes/SMP-0001_2006943906698.png \
                        barcodes/PWD-0001_2005217175150.png

# Anything OpenCV can open, several files at once, as JSON
python -m labvision.reader photo.jpg --table barcodes/lookup_table.json --json

pytest tests
pytest --doctest-modules labvision
```

`python -m labvision.registry --help` covers `--count`, `--seed`, `--module-px`
and `--no-images`.

### From Python

```python
from pathlib import Path

import cv2

from labvision import reader, registry

table = registry.load_table(Path("barcodes/lookup_table.json"))
for detection, record in reader.resolve(
    reader.decode_image(cv2.imread("frame.png")), table
):
    print(detection.code, record["material"], detection.corners)
```

## Sample catalogue

**200 barcodes: two phases, each a full cross product of compounds x container
sizes.**

| Phase | Compounds | Containers | Ids | Codes |
| --- | --- | --- | --- | --- |
| Liquid | 20 | flasks — 10, 20, 30, 50, 100 ml | `SMP-0001..0100` | 100 |
| Powder | 20 | bottles — 100, 250, 500, 1000, 2000 ml | `PWD-0001..0100` | 100 |

Material varies slowest, so `SMP-0001..0005` are Limonene at each flask size and
`PWD-0001..0005` are Vanillin at each bottle size. Only the lot number is
random, under `DEFAULT_SEED`.

**Each phase has its own labware**, so there are ten vessel classes: five
flasks — `flask_10ml`, `flask_20ml`, `flask_30ml`, `flask_50ml`, `flask_100ml` —
and five bottles — `bottle_100ml`, `bottle_250ml`, `bottle_500ml`,
`bottle_1000ml`, `bottle_2000ml`.

### Why powders are in bottles

The powder sizes are not free choices: they are the white HDPE bottles in
`assets/agrochemical-bottles`, which is what the simulation renders powders in.
A powder row has to name a bottle that exists as a mesh, and
`test_powder_sizes_match_the_bottle_kit` checks each size against the kit's
`glb/` files.

| `container_ml` | Kit object | Body Ø | Height without cap |
| --- | --- | --- | --- |
| 100 | `Bote_100mL` | 46 mm | 97 mm |
| 250 | `Bote_250mL` | 60 mm | 131 mm |
| 500 | `Bote_500mL` | 74 mm | 164 mm |
| 1000 | `Bote_1L` | 88 mm | 216 mm |
| 2000 | `Bote_2L` | 116 mm | 245 mm |

The kit has a sixth bottle, the wide-mouth `Bote_1L_ancho`. It is left out of
the catalogue because it shares its nominal capacity with `Bote_1L`, and
`container_ml` could not tell the two apart.

Version 3 of the table put powders in the flask series instead, so that a
detector could not read "powder" off the vessel shape and skip the barcode.
That shortcut is open again — a bottle means powder — and it is accepted: phase
only tells the robot how to dispense, while the compound, which is what the
barcode is for, is still a full cross product against bottle size. Moving
powders changed every powder barcode; the 100 liquid codes are the same as in
version 3.

### Phase is a property of the compound, not a choice

A compound is solid or liquid at room temperature; it does not get to be both.
`POWDER_MATERIALS` carries each one's melting point as a comment, which is the
evidence for it being there:

| Compound | mp °C | | Compound | mp °C |
| --- | --- | --- | --- | --- |
| Camphor | 175–177 | | Vanillin | 81–83 |
| Maltol | 160–164 | | Phenylacetic acid | 76–78 |
| Musk ketone | 135–137 | | Ethylvanillin | 76–78 |
| Cinnamic acid | 133 | | Coumarin | 69–71 |
| Sclareolide | 120–124 | | Tonalide | 54 |
| Ethyl maltol | 89–92 | | Indole | 52–54 |
| Thymol | 49–51 | | Cedryl acetate | 44–46 |
| Benzyl cinnamate | 39 | | Menthol | 36–38 |
| Piperonal | 35–37 | | Exaltolide | 35 |
| Methyl cinnamate | 34–38 | | Diphenyl ether | 27–29 |

Four of these — **Camphor, Vanillin, Thymol and Menthol** — were originally in
the liquid list. They are not liquids, and moving them is why the liquid codes
were reissued when powders were added. Their replacements are Phenylethyl
alcohol, Methyl salicylate, Linalyl acetate and cis-3-Hexen-1-ol.

Two borderline cases stay in the liquid list deliberately: **Anethole**
(mp 20–21 °C) and **alpha-Terpineol** (mp ~35 °C) are both solid on a cold
bench, but are supplied and handled as liquids commercially.

`test_no_compound_appears_in_both_phases` and
`test_cas_numbers_are_unique_across_the_catalogue` keep this honest.

### Why a cross product and not two cycling lists

The earlier version cycled 20 materials against 5 vessel classes in step. Since
5 divides 20, that locked each compound to exactly one vessel size — Limonene
was always the 50 ml tube — covering just 20 of the 100 possible pairs.

That is fine for exercising the barcode path and wrong for training data: a
vision model could learn *flask size implies compound* and never read the
barcode at all. `test_compound_is_not_correlated_with_container_size` guards it.

### A note on the flask sizes

10, 20, 50 and 100 ml are standard volumetric-flask capacities (ISO 1042). 30 ml
is **not** in that series — its neighbour there is 25 ml — but it is a common
amber storage-bottle size for aroma chemicals, which is the closer analogue for
a raw-material inventory. Change one entry in `FLASK_VOLUMES_ML` and regenerate
if you want strict ISO sizes.

## Not done yet

The label is currently a standalone PNG. Wiring it onto a vessel in the MuJoCo
scene as a textured geom, and carrying the label corners as pose-model
keypoints so the quad comes from the network rather than the localiser, is the
next step and is not part of this work.
