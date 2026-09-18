# computer-vision

Barcode identity for the lab robot. Every sample on the bench carries a printed
EAN-13 label; the barcode holds nothing but an identifier, and everything the
robot needs to know about the sample is looked up from that identifier in a
table.

Owners: Nacho, Martí (see `AGENTS.md`).

Two halves. **Identity** --- a printed EAN-13 label per sample, and a reader
for it. **Placement** --- turning a detector's bounding box into metres on the
bench, from one camera, using the bench plane in place of a depth sensor. The
first half is everything up to *Why the encoder is hand-written*; the second
is *From a box in the image to a point on the bench*.

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
yields a quad. It closes the thresholded image with a kernel that is long across
the bars and short along them — which melts parallel bars into one solid blob
while leaving text alone — filters the blobs by aspect ratio, rectifies each one,
and reads it against the same module tables the encoder writes with.

**Each kernel is tried both ways round**, wide-and-flat and tall-and-narrow. A
flat kernel bridges the gaps between bars that stand upright and does nothing
for bars that lie flat, so with it alone a label in "ladder" orientation — which
is how the labels sit on the powder bottles — was never found: 35 of the 100
powder labels failed when turned a quarter turn, the 35 that OpenCV's detector
also missed. Everything after the blob is found already worked at any angle.

The two are unioned because a padding rung that decodes one label in a frame
holding four would otherwise mask the three the localiser had already read.

### Measured behaviour

Over the 200 generated labels: **200/200 decode correctly**, 189 through OpenCV
and 11 only through the fallback, all with a quad, at roughly 320 ms/image. It
was 260 ms before the kernels were tried both ways round.

Turned a quarter turn, the 100 powder labels also decode **100/100**, flat and
wrapped round a cylinder at 60, 90 and 120 degrees of arc, at full size and at
3 px/module, with no code ever misread as another.

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

## From a box in the image to a point on the bench

The second half of this package. A detector says *there is a 1 L bottle in
these pixels*; the robot needs *there is a 1 L bottle at (7.21, 2.34, 0.95)*.
One camera can do that, and here is exactly what it takes.

### Why one camera is enough

A pixel is not a point, it is a ray: the object could be anywhere along it,
and that missing degree of freedom is what a second camera or a depth sensor
normally buys back. It can be bought back for free instead, because a vessel
standing on the bench has a coordinate we already know --- its base is on the
bench plane, z = 0.95. Intersect the ray with that plane and all three
coordinates fall out. With an exact box the recovery is exact; nothing is
approximated by the geometry itself.

For glassware this is not merely the cheap option, it is the better one.
Structured-light and stereo depth sensors fail on transparent and specular
surfaces, and depth for glass is an open research problem. A geometric prior
sidesteps the sensor's worst case entirely.

### What has to be known --- yes to both sets of parameters

**Intrinsics are required.** Without a focal length in pixels and a principal
point there is no map from a pixel to a direction at all. The camera here is a
**GoPro in Linear mode**, which is one number: 92 degrees across at 16:9, so
`gopro_intrinsics(1920, 1080)` gives f = 927 px and a 60.4 degree vertical
field of view.

**Linear, not Wide, and that is not a preference.** MuJoCo's cameras are, in
its own documentation, "perfect point cameras" --- a pinhole projection with
no radial term. GoPro's native Wide capture is a fisheye and no pinhole render
can produce it. The published fields of view say which mode is which without
anyone having to take a view:

| Digital lens | H | V published | V a rectilinear lens would give | |
| --- | --- | --- | --- | --- |
| Linear | 92 deg | 61 deg | 60.4 deg | matches |
| Narrow | 73 deg | 45 deg | 45.2 deg | matches |
| Wide | 118 deg | 69 deg | 86.2 deg | does not --- fisheye |

A rectilinear lens ties its two fields of view together through the frame's
aspect ratio, `V = 2 atan(tan(H/2) * 9/16)`. Linear and Narrow obey that;
Wide misses by 17 degrees. So `gopro_intrinsics(lens="wide")` raises rather
than silently modelling a fisheye as a pinhole. If the real camera does shoot
Wide, de-warp first and hand the Brown-Conrady coefficients to `Intrinsics` ---
a 2 % barrel left uncorrected is 11 px at the frame edge, which out there is
tens of centimetres of bench. On a rendered frame distortion is exactly zero.

**Extrinsics are required, and position alone is not enough.** (7, 0, 3) fixes
where the rays start; which way they point is three more numbers, and they
matter more than anything else here: at this geometry **one degree of pan
moves the answer 44 mm and one degree of tilt 87 mm** --- larger than every
other error in this document combined. Aiming at (7, 2.5, 0.95) fixes two of
the three, and roll is zero by construction, so the camera is fully specified:

| Situation | Call |
| --- | --- |
| Simulation --- exact, nothing to calibrate | `default_camera()`, i.e. `Camera.look_at(intrinsics, (7, 0, 3), (7, 2.5, 0.95))` |
| Reading the pose back out of MuJoCo | `Camera.from_mujoco(intrinsics, data.cam_xpos[i], data.cam_xmat[i])` |
| Real hardware | `Camera.from_correspondences` --- four points on the bench whose (x, y) you measured with a tape, clicked in one frame |

The last row is not optional on a real mount. A bracket is aimed to a degree
or two at best, and a degree is 44 mm, so a physical camera has to be solved
from markers no matter how precisely its nominal aim is specified.

**Unless you take the shortcut, in which case neither is needed.** If every
answer is going to land on the same plane, the whole pinhole model collapses
into one 3x3 homography between pixels and bench coordinates, and it can be
fitted from four known points without a focal length or a pose ever being
named:

```python
homography = homography_from_points(bench_xy, image_uv)   # four points, no calibration
positions = apply_homography(np.linalg.inv(homography), boxes_bottom_centre)
```

`test_camera.py` checks this returns the same matrix the full calibration
builds. The one thing it cannot absorb is lens distortion, which is not a
projective map --- undistort first. Take this route if the camera is fixed and
nothing else needs the camera model; take the full model if you also want
vessel heights, mouths, or a second plane later.

### The room, and what the camera sees of it

14 x 5 x 3 m, origin at a floor corner, X along the long wall. Camera at
(7, 0, 3) --- ceiling height, halfway along the long wall --- aimed at
(7, 2.5, 0.95), the middle of the bench top. That is a 3.23 m line of sight at
**39 degrees of elevation**, which is a decent mounting: below about 30 degrees
the ray meets the plane at a grazing angle and pixel error slides a long way
along it.

For the simulation side, that camera is this, and MuJoCo will render exactly
the projection this package assumes:

```xml
<camera name="bench" pos="7 0 3" mode="targetbody" target="bench"
        fovy="60.4" resolution="1920 1080"/>
```

`fovy` is the vertical field of view, which is the one MuJoCo wants; 60.4
degrees is the Linear lens at 16:9. If you would rather state the optics
physically, `sensorsize="0.00605 0.0034" focal="0.00292 0.00292"` is the same
camera --- the HERO11's measured 2.92 mm lens behind the sensor rectangle that
gives the Linear field of view --- and MuJoCo computes `fovy` from it,
overriding the attribute. Pointing it with `mode="targetbody"` beats writing
a quaternion, and `Camera.from_mujoco` reads whatever pose comes out.

What the frame actually contains, with a 92 x 60.4 degree lens aimed there:

| Image row | What is there |
| --- | --- |
| 0 to 255 | the far wall and above --- **not bench** |
| 255 | the foot of the far wall, bench y = 5.0 |
| 540 | the bench centre, y = 2.5 |
| 1080 | the nearest visible bench, y = 0.76 |

So three quarters of the frame height is usable bench, and the near 0.76 m
strip against the camera's own wall is out of shot. The horizon sits at
v = -221, above the frame entirely, which means no pixel in a valid frame can
fail the horizon test --- if a box trips that guard, the box is malformed.

One number in `scene.py` is still unknown: **the bench footprint**, so
`TABLE_SIZE` is None and the "is it even on the table" check is skipped.

### Which pixel of the box

A box is four numbers and a position is two, so something has to say what
stands for the object. Three ways, in decreasing order of what they need and
increasing order of error:

**`fit`** --- invert the forward model. `predict_bbox` computes the exact box
an upright cylinder of known radius and height would produce, so the position
is just the one whose predicted box matches the observed one: Gauss-Newton on
the four edge residuals, started from the base anchor, converging in two or
three steps and 0.7 ms. It uses all four edges instead of throwing three away,
and it has **no anchor bias at all**. It also returns a residual, which is the
only thing in the pipeline that notices a detection labelled as the wrong
vessel. This is the default whenever the dimensions are known --- and for powders
they are, since `scene.VESSELS` is keyed by `Sample.vessel_class`, so a
decoded barcode indexes straight into it. The liquid `flask_*` classes have
no dimensions recorded anywhere yet, so they fall back to the base anchor
until someone measures them.

**`base`** --- back-project the **bottom-centre** of the box, which images the
contact patch and so is already on the plane. Needs no height. It has one bias
that must be corrected: the lowest pixel of a vessel of radius r is not its
axis but the point of its base circle nearest the camera, so the raw
intersection lands short by exactly r. The direction to push it back is not
"towards the camera along the floor" --- it is the in-plane normal to the
iso-v line, which falls straight out of the Jacobian. Skip that correction and
these bottles land **23 to 59 mm** off, which dwarfs the pixel noise.

**`centre`** --- back-project the **centre** of the box against a plane lifted
to half the vessel height. For when the base is occluded or cropped. Needs the
height, and keeps a residual bias because the box centre is not the image of
the mid-height point under perspective.

Whichever is used, the answer returned is the base centre on the bench; the
mouth, which is where a pipette goes, is that plus the vessel height.

### Measured

Against exact boxes --- `predict_bbox` is the oracle, so ground truth is known
--- over 25 positions spanning a 1.6 m square of bench, mean error in mm:

| Vessel | `fit` | `centre` | `base` | `base`, correction off |
| --- | --- | --- | --- | --- |
| bottle_100ml | 0.00 | 0.7 | 3.2 | 23 |
| bottle_250ml | 0.00 | 1.2 | 4.4 | 30 |
| bottle_500ml | 0.00 | 1.9 | 5.6 | 38 |
| bottle_1000ml | 0.00 | 3.2 | 7.9 | 45 |
| bottle_1000ml_wide | 0.00 | 2.3 | 5.6 | 51 |
| bottle_2000ml | 0.00 | 4.1 | 8.5 | 59 |

The residual on `base` is entirely the box's u-centre drifting off the axis for
off-axis vessels --- feed it the true lowest silhouette pixel instead and the
error is 0.00 mm, which is what says the radius correction itself is right
rather than merely helpful.

There is deliberately no resolution column. These biases are **geometry**: they
come from where the silhouette's extremes sit in the world, and a focal length
only rescales that. Halve the frame and every number in the table is unchanged,
which `test_the_anchor_bias_is_geometry_and_does_not_move_with_resolution`
pins.

### The real limit is resolution, not geometry

Since the geometry contributes nothing, all the error is the detector's,
amplified by how many millimetres of bench a pixel covers. `plane_jacobian`
gives that exactly, and its worst singular value is what `Placement` reports:

| GoPro Linear at | Near edge | Bench centre | Far edge |
| --- | --- | --- | --- |
| 1920 x 1080 | 3.2 mm/px | 5.5 mm/px | 8.4 mm/px |
| 3840 x 2160 (4K) | 1.6 mm/px | 2.7 mm/px | 4.2 mm/px |
| 5312 x 2988 (5.3K) | 1.2 mm/px | 2.0 mm/px | 3.1 mm/px |

Which lands as, for a 1 L bottle at 1080p with the `fit` anchor --- where its
box is about 26 x 72 px:

| Box noise | Mean error | p95 |
| --- | --- | --- |
| 0.5 px | 2 mm | 5 mm |
| 1 px | 4 mm | 9 mm |
| 2 px | 8 mm | 17 mm |
| 3 px | 12 mm | 26 mm |
| 5 px | 21 mm | 50 mm |

So at 1080p from 3.2 m **a pixel is worth 5.5 mm of bench**, and a detector
good to a pixel or two lands within a centimetre --- enough to reach into a
50 mm bottle mouth, not enough to be careless about. The levers, in order of
effect: shoot 4K or 5.3K, which the camera does natively and which buys 2x and
2.8x; switch the digital lens from Linear to Narrow, which trades a third of
the field of view for a quarter off the error; move the camera closer; raise
the mounting angle. None of them is a change to the maths.

The wide end is where this gets dangerous. Every step towards a wider lens
spends pixels on wall: Wide would be worse still, and it cannot be rendered or
back-projected as a pinhole anyway. An action camera is the wrong instrument
for a measurement like this, and Linear at 4K is about the best one can be
asked to do.

### Where this stops being true

The plane has to be real. A vessel in a rack, on a shelf, held by the gripper
or knocked over is not at z = 0.95, and the error is systematic rather than
noisy --- 5 cm of unmodelled height at this geometry is about 6 cm of position
error. If vessels can sit at several known heights, classify the surface and
switch planes. If the heights are arbitrary, one camera is not enough and this
approach does not apply.

Three guards are reported rather than assumed away: `clipped` (the box touches
the frame border, so its edges are the frame's and not the object's),
`inside_room` / `on_table`, and the `fit` residual. A detection above the
horizon raises instead --- geometrically, it cannot be standing on the bench.

### Using it

```bash
# Where is this box, and how much is a pixel worth there?
python -m labvision.scene --bbox 300 200 340 280 --vessel bottle_1000ml

# The room's error budget, no detection needed
python -m labvision.scene

# At 4K, or with a narrower digital lens
python -m labvision.scene --width 3840 --height 2160 --lens narrow
```

```python
from labvision import scene
from labvision.camera import Camera

# In simulation the camera is fully specified, so this is exact
camera = scene.default_camera()

# On real hardware, solve the pose from four measured markers on the bench
intrinsics = scene.gopro_intrinsics(1920, 1080)          # or 3840, 2160
camera = Camera.from_correspondences(intrinsics, marker_pixels, marker_world_xyz)

# Per detection
placed = scene.locate(scene.BBox(*box), camera, vessel=scene.VESSELS["bottle_1000ml"])
placed.position          # base centre, metres, on the bench plane
placed.mouth             # where the pipette goes
placed.metres_per_pixel  # what a pixel of detection error costs here
placed.residual_px       # how well the box matches that vessel standing there
```

## Layout

| Path | Purpose |
| --- | --- |
| `labvision/ean13.py` | Check digit, module encode/decode, rendering |
| `labvision/registry.py` | Samples, hash-to-code, lookup table, label PNGs |
| `labvision/reader.py` | Localiser, both decoders, code-to-sample resolution |
| `labvision/camera.py` | Pinhole model, ray-plane intersection, homography |
| `labvision/scene.py` | The room, box anchors, box-to-position |
| `labvision/bottles.py` | Sticks each label onto the bottle of its phase and size |
| `tests/` | 280 tests, plus 25 doctests |
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

# Where on the bench is this detection?
python -m labvision.scene --bbox 300 200 340 280 --vessel bottle_1000ml

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

## Labels on the bottles

```bash
python -m labvision.bottles                 # both kits
python -m labvision.bottles --phase liquid  # one of them
```

Each phase has a kit of bottle models under `assets/`, and every sample gets a
copy of its bottle with its label stuck on:

| Phase | Kit | Bottles | Labelled models |
| --- | --- | --- | --- |
| Liquid | `assets/amber-bottles` | amber glass, closed, white cap | `labelled/SMP-XXXX_<code>.glb`, 100 files, ~31 MB |
| Powder | `assets/agrochemical-bottles` | white HDPE, open | `labelled/PWD-XXXX_<code>.glb`, 100 files, ~60 MB |

The liquid sizes — 10, 20, 30, 50, 100 ml — are exactly the amber kit's, so no
liquid barcode had to change. The kit also has a 60 ml bottle that no sample
uses: adding a size renumbers the samples, which reissues every liquid barcode.
In the registry the liquid `vessel_class` is still `flask_*ml`; the name predates
the kit and renaming it is a schema change for another day.

Unlike the label PNGs these models **are committed**, so the simulation side can
use them without installing this package. They are deterministic: regenerating
from the same lookup table rewrites them byte for byte, so rerun the command and
commit the result whenever a barcode, the label layout or a kit's bottles
change. A file whose name no longer matches a row of the table is stale and
should be deleted. `test_committed_labelled_bottles_are_not_stale` fails when
they drift.

**The bottle is never chosen, it is looked up.** `labelled_bottle` takes a
registry row and nothing else; the kit comes from that row's `phase` and the
bottle from its `container_ml`, so a 2 L barcode cannot land on a 100 ml bottle,
nor a liquid's on a powder bottle — 100 ml exists in both kits, and the phase
decides which one it is.

The kit's GLBs have no UVs, so the label is not painted on. It is a separate
**sticker mesh**: a thin curved patch 0.2 mm off the bottle's straight wall, with
its own UVs and the label PNG embedded as its texture, added as a child node of
the bottle. The bottle's meshes and materials are carried over byte for byte. The
wall is measured from the GLB, not copied from the kit's generator, so a
regenerated kit needs no change here. The amber files hold a closed bottle, with
the cap listed first, so the bottle is taken to be the tallest mesh in the file.

**On glass the sticker has a back.** The amber bottles are see-through, which a
one-sided sticker handles badly either way: drawn on one side it vanishes when
seen from behind through the bottle, and drawn on both it shows its barcode
mirrored through the glass — which the reader will happily decode, since it
reads mirrored symbols. So on a bottle whose material transmits light the label
gets a second, plain white face turned inwards, as the back of a paper label is.
The opaque HDPE bottles do not need one and do not get one.

The label node carries `extras` a consumer can read without decoding anything:
`code`, `sample_id`, `material`, `container_ml`, `vessel_class`, `module_mm` and
`corners_m` — the label's four corners in the bottle's frame, top-left first,
which are the ground-truth keypoints for the label quad.

### Turned a quarter turn, and why

The label goes on in **ladder orientation**: bars lying flat, stacked up the
bottle, text reading bottom to top. The embedded texture stays an upright label,
identical to the PNG `labvision.registry` writes; it is the sticker's UVs that
turn it. `corners_m` is named in the label's own frame for the same reason, so
its top-left is the sticker's bottom-left as seen on the bottle.

This is about what a cylinder does to a barcode. Seen head-on, a cylinder
squeezes whatever runs *round* it, more towards the edges, and leaves alone
whatever runs *up* it. A barcode's information is entirely in its bar widths.
Upright, those widths run round the bottle and get squeezed unevenly, and the
reader, which expects even modules, gives up. Turned, only the bar *lengths* are
squeezed, and they carry nothing.

All 100 powder labels, projected onto a cylinder and decoded:

| Arc covered | 45° | 55° | 60° | 75° | 90° | 120° |
| --- | --- | --- | --- | --- | --- | --- |
| Upright | 100 | 100 | 86 | 72 | 74 | — |
| Ladder | — | — | 100 | — | 100 | 100 |

Upright there is a cliff just under 60 degrees, and staying below it meant a
20 mm label at 51 % magnification on the 100 ml bottle. Ladder has no such
limit, so the labels are sized by the wall instead.

### Label size follows the bottle

Each label is printed as large as three limits allow: 200 % magnification, which
is the EAN-13 specification's own ceiling; the height of the straight wall less a
3 mm margin; and 90 degrees of circumference, which is there to keep the captions
in view and never binds on this kit.

| Bottle | Sticker (round x up) | Module | Magnification | Arc | Bound by |
| --- | --- | --- | --- | --- | --- |
| Liquid 10 ml | 12.3 x 25.3 mm | 0.21 mm | 63 % | 63° | wall height |
| Liquid 20 ml | 17.9 x 36.8 mm | 0.30 mm | 92 % | 73° | wall height |
| Liquid 30 ml | 21.2 x 43.5 mm | 0.36 mm | 109 % | 76° | wall height |
| Liquid 50 ml | 25.4 x 52.0 mm | 0.43 mm | 130 % | 76° | wall height |
| Liquid 100 ml | 34.0 x 69.7 mm | 0.58 mm | 174 % | 81° | wall height |
| Powder 100 ml | 18.7 x 38.3 mm | 0.32 mm | 96 % | 46° | wall height |
| Powder 250 ml | 28.5 x 58.5 mm | 0.48 mm | 147 % | 54° | wall height |
| Powder 500 ml | 38.4 x 78.7 mm | 0.65 mm | 197 % | 59° | wall height |
| Powder 1 L | 38.9 x 79.9 mm | 0.66 mm | 200 % | 50° | magnification |
| Powder 2 L | 38.9 x 79.9 mm | 0.66 mm | 200 % | 38° | magnification |

Every liquid label fills its wall top to bottom, so it cannot be made larger
without changing the label itself: the amber bottles are simply short. The 10 ml
one is 52 mm tall with 31 mm of straight wall, and its label comes out at 63 %.
Stood upright instead, and kept under the 55 degrees an upright label survives,
the same label would be 11 mm wide at 27 %. The amber labels also wrap further
round their narrow bottles than the powder ones, up to 81 degrees, which is well
inside what ladder orientation was measured to take.

At the reader's floor of two pixels per module the 10 ml liquid label needs about
10 px/mm in the frame, the 100 ml powder label about 6, and the 1 L and 2 L
about 3.
`test_embedded_label_decodes_flat_and_wrapped` pins the decode for every size as
a camera would see it, and
`test_ladder_labels_survive_far_more_wrap_than_upright_ones` pins the table above.

**What this does not show.** The wrap test is a head-on orthographic projection
of a clean texture. A rendered frame adds perspective, a bottle turned partly
away, lighting and the camera's resolution, none of which are tested here yet.

## Not done yet

The labels are on their bottles as GLB, which Isaac Lab can import but MuJoCo
cannot: MuJoCo needs the sticker as an OBJ plus a PNG texture, and the scene in
`simulation/` still uses the unlabelled bottles. Wiring the labelled ones into
the MuJoCo scene, and carrying the label corners as pose-model
keypoints so the quad comes from the network rather than the localiser, is the
next step and is not part of this work.

On the placement side, three things are open and each is small:

- **The bench footprint**, so `on_table` stops returning None.
- **A rendered end-to-end check.** The MuJoCo frame conversion is pinned
  against the hand-written back-projection that was measured in simulation,
  but nothing here has yet been run against a frame rendered from this room
  with the camera in the README's MJCF snippet.
- **The real camera's pose**, if a physical GoPro ever replaces the rendered
  one: four markers and `Camera.from_correspondences`, because a bracket is
  never aimed to better than a degree and a degree is 44 mm.
- **Flask dimensions.** `VESSELS` carries the measured agrochemical bottles;
  the five `flask_*` classes the registry knows about have no dimensions
  recorded anywhere yet, so they need `radius` and `height` passed by hand.

## The detector: from a frame to boxes

`labvision/detector.py` is the piece between the frame and everything above:
it says *there is a vessel in these pixels*. The barcode inside the box gives
the identity, `scene.locate` turns the box into a bench position. Nothing was
trained: ten pretrained detectors were benchmarked on real lab photographs and
two were kept. The full write-up, with overlays for every model and photo, is
`docs/BENCHMARK.md` at the repo root (in Spanish) and
https://claude.ai/artifact/FvnEarQtYJLTaUpLs1AXp4.

| backend | model | when | CPU, 960 px input |
| --- | --- | --- | --- |
| `world` | YOLO-World large, everyday prompts | best quality; reliable down to 24 px of vessel side | 1.9 s/frame |
| `coco` | YOLO11 small, COCO classes filtered to bottle/cup/glass/vase/bowl | no prompts; most robust on small empty vessels; a laptop | 0.7 s/frame |

The network input defaults to the frame's own size, not the usual 640 or 960,
because at this scene's range downscaling pushes the whole bottle kit under
the size floor (next section). A 1080p frame therefore costs about four times
the figures above on a CPU; on a GPU it is still real time.

```python
from labvision.detector import Detector, attach_barcodes
from labvision.scene import VESSELS, default_camera, locate

boxes = Detector("world").detect(frame)          # or Detector("coco")
attach_barcodes(frame, boxes)                     # sets box.barcode when a label decodes
placement = locate(boxes[0].bbox, default_camera(), vessel=VESSELS["bottle_1000ml"])
```

Over a folder of frames, an image or a video, writing overlays and one JSON
line per frame to `results/detect/`:

```bash
python -m labvision.detector ../simulation/out/minihannover_scene --backend both
python -m labvision.detector frames/ --backend coco --barcodes --device cuda:0
```

The label a detector gives is not the identity. A beaker called `cup` is
normal; YOLO-World's "cup" and "glass" prompts are what make empty glassware
appear at all, and lab vocabulary on its own loses half of it. The threshold
per backend is the best-F1 point from the benchmark; override with `--score`.

### The size floor

What decides whether a vessel is found is how many pixels it covers at the
network input, not which model looks at it. Measured by shrinking the
annotated photographs step by step:

| vessel side at the network input | found |
| --- | --- |
| under 24 px | lost (COCO still gets 6 in 10 on tiny cups) |
| 24 to 48 px | a coin toss |
| 48 px and up | 8 to 9 in 10, and no better above 96 px |

`apparent_size_px` predicts that number for a vessel, a range and a camera.
For the scene's camera -- the GoPro in Linear mode, 3.23 m from the bench,
f = 927 px at 1080p -- the bottle kit comes out as follows, side being the
geometric mean of width and height, at the frame's own resolution:

| bottle | 1080p | 4K |
| --- | --- | --- |
| 100 ml | 13 x 28 px, side 19 | side 38 |
| 250 ml | 17 x 38 px, side 25 | side 51 |
| 500 ml | 21 x 47 px, side 32 | side 63 |
| 1 L | 25 x 62 px, side 40 | side 79 |
| 2 L | 33 x 70 px, side 48 | side 97 |

At 1080p only the 2 L bottle reaches the reliable floor and the 100 ml one is
lost outright; every size in between is a coin toss. And that is already at
the native 1920 px input: inferring at 960 halves every side and nothing in
the kit survives, which is why the detector defaults to the frame's own size.
What makes this camera usable, in order of preference, and the test suite
pins the 1080p numbers:

- Capture or render at **4K** and infer at 3840: everything from 250 ml up is
  reliable and the 100 ml bottle becomes a coin toss instead of a loss.
- The **Narrow** digital lens at 1080p, which trades field of view for the
  same gain (`gopro_intrinsics(lens="narrow")`).
- Bring the camera closer; at 1.5 m the 1080p numbers double.

Barcodes are a separate, harder floor: EAN-13 needs about 190 px of label
width to decode, which no overview camera delivers. The fixed camera proposes
a box, the wrist camera reads the label; `attach_barcodes` is for the
close-up frame.

### When rendered frames arrive

1. Put the frames anywhere, e.g. `simulation/out/<scene>/` from
   `render_dataset.py`, with the bottle kit placed on the bench.
2. `python -m labvision.detector <folder> --backend both` and look at the
   overlays. The summary line prints the median box side in pixels; if it is
   under 48, fix the camera or the resolution before judging the model.
3. With ground-truth boxes, run the benchmark proper (see
   `docs/BENCHMARK.md`, section "Cuando lleguen frames de Isaac"; the
   conversion script `scripts/isaac_to_gt.py` accepts YOLO `.txt` labels).
4. If both backends fail on renders that pass the size floor, the next step
   is a fine-tune on renderer-labelled frames, not another pretrained model.
