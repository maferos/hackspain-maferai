# Training the bench detector from simulation: the MuJoCo pipeline, the agreed plan, and how to replicate it in Isaac Sim

This is the whole process behind the bench vial detector (YOLO26n, one class
`amber_bottle`, fixed `general` camera). It covers how the training frames are
generated in MuJoCo, how they are labelled and cropped, how the model is
trained on a rented GPU and scored, and what the next run will be. It also
records everything learned along the way, so another session or teammate can
pick the work up. The last part maps each step onto NVIDIA Isaac Sim.

Written 2026-09-19, 20:00 CEST. Every number is marked as one of these:

- **measured**: from a run that happened, with the script that produced it;
- **agreed**: decided with Martí, not run yet;
- **proposed**: a recommendation nobody has agreed to or run yet.

**Where the code is.** The scripts this document names beyond those already on
`main` (`bench_crop.py`, `viewpoint_study.py`, `dataset_report.py`,
`export_and_time.py`, `limits_sweep.py`, `orbit_study_pod.sh`,
`runs/orbit/train_yolo26_gpu.py`, and the orbit, close, dark and overhead
splits of `fixedcam_dataset.py`) are on the branch `vision/orbit-dataset`. As
of this writing that branch is **uncommitted** in Martí's worktree
`../Hackspain-orbit`. Until it lands on `main`, read those names as
descriptions.

If you are picking this up, read section 7 (the agreed plan) and section 8
(state and next steps) first.

Related documents: `docs/YOLO26_STUDY.md` (where the current model fails, the
training grid), `docs/FIXED_CAMERA_BENCHMARK.md` (benchmark, Isaac converter),
`simulation/runpod-isaac.md` (Isaac Sim on RunPod).

## 1. The target

| | |
| --- | --- |
| Camera | `general`: GoPro Linear, 1920 x 1080, fovy 60.44 (f = 927 px), on the aisle wall 3 m up, looking down at the bench |
| Objects | amber glass vials, 10 to 100 ml, on the rail scene's 6 x 2 m desk (`minihannover_rail_scene.xml`, UR10e on a 6 m rail) |
| Size in the image | 9 to 36 px tall from the wall mount (median 17) |
| Classes | one, `amber_bottle`. Identity is the barcode reader's job, not the detector's |
| Latency | about **100 ms per frame** on the demo laptop's CPU (i5-12450H, no GPU) |
| Baseline to beat | `rail` = `weights/yolo26n_rail_general.pt`, on `rail_test`: AP50 0.990, recall 0.989, precision 0.995, 0.11 false boxes a frame at threshold 0.47 (measured) |

For comparison, on the same `rail_test` frames: the earlier fixed-camera model
scored AP50 0.796, the model trained on Isaac's `lab_dataset_v2` 0.574, and
YOLO-World L with prompts 0.672 (measured). In `labvision/detector.py` the
backend `rail` runs at threshold 0.10, tuned for `propose_confirm`; the viewer
draws boxes from 0.47.

## 2. The pipeline at a glance

```
scene (MJCF, as committed, never written)
  -> per frame, from seed = split.seed + k:
       bottle layout -> arm pose -> light and worktop tint -> camera pose
  -> render RGB + 3 segmentation passes (MuJoCo, EGL on the GPU pod)
  -> gt.json: exact box, visible fraction and "where" for every bottle in view
  -> optional degradation (blur, noise, JPEG, gamma)
  -> select frames (section 7), crop to the bench (bench_crop.py)
  -> fixedcam_to_yolo.py --crop: YOLO labels, one class, bottles >= 30 % visible
  -> train YOLO26 on a rented GPU (runs/rail, runs/orbit)
  -> score by split and by viewpoint (fixedcam_bench.py, viewpoint_study.py)
  -> threshold picked on validation, latency checked on the laptop,
     weights registered as a labvision backend
```

The dataset can be regenerated from its code and seeds alone: the same seeds
give the same frames on any machine, so the images are disposable.

## 3. Generating the frames in MuJoCo

Script: `scripts/fixedcam_dataset.py`. The scene is loaded through
`render_perfumery.Lab`, which adds extra labelled bottles in memory
(`EXTRA_PER_SIZE = 3` of every bottle size of both kits, on top of the scene's
own). Each frame draws the steps below, in this order, from its own seed.

### 3.1 Bottle layout (`lay_out`)

- All movable bottles are parked, then 8 to 34 are stood on free worktop
  (`max_bottles = 34` for the rail splits). A spot is free when a ray cast down
  meets the worktop at the right height and nothing within the bottle's radius.
- 35 % of layouts are a **cluster**: 75 % of the bottles fall within a
  Gaussian of 15 x 12 cm around one point, so they hide each other, as on a
  working bench.
- 10 % of training frames (20 % of test frames) keep the scene's **as-built**
  layout, the one the robot will actually meet.
- Every sample bottle in view is labelled, wherever it stands (bench, shelf,
  room), and tagged with `where`, so the benchmark can score the bench alone
  without the model being taught that a bottle elsewhere is background.

### 3.2 Arm pose (`pose_arm`)

- 75 % of frames: the UR10e reaches a random point 5 to 40 cm above the
  worktop with the rail scene's own IK (`rail_kinematics.reach`), so it leans
  over the bench and hides bottles the way it will when working.
- Otherwise the carriage is parked at a random x along the rail.

### 3.3 Light and materials (`Randomiser.draw`)

| Knob | Training draw |
| --- | --- |
| Light intensity | x U(0.55, 1.45) on every light |
| Light colour | per channel x N(1, 0.035), clipped to 0.9 to 1.1 |
| Headlight | diffuse and ambient each x U(0.55, 1.45) |
| Dark frames | 20 % of wall-mount and 25 % of orbit and close training and validation frames keep only 8 to 50 % of the light |
| Worktop tint | 50 % of frames: the worktop's colour x U(0.78, 1.0), hue within 2 % |

Test splits keep the light nominal, except the dedicated `*_shift` and
`*dark_test` splits. Light is drawn per frame, so varying it adds no frames:
the number of images is set by how well the camera poses are covered, not by
the light (section 7).

### 3.4 The camera: three families of viewpoints

All three render at 1920 x 1080.

**Wall mount (`rail_*`)**: the `general` camera where it is mounted, jittered in
training by N(0, 7 cm) per axis, clipped to 15 cm, and turned by N(0, 2) degrees
about a random axis, clipped to 5 degrees. The shift only goes into the room and
down (measured bug: the mount is flush with the wall and the ceiling, and a
third of the jittered frames of an earlier split put the lens inside them and
came out flat grey with no bottle in view).

**Orbit (`orbit_*`)**: the camera stands anywhere in the room and looks at an
**aim point** on the bench (`Randomiser.orbit`):

1. Aim point: 70 % of the time a bottle standing on the bench, moved in x and
   y by N(0, spread), with spread = `AIM_SPREAD_M` (25 cm) scaled by the
   split's distance range against the orbit's; otherwise a uniform point of
   the worktop. Its height is 0 to 10 cm above the worktop.
2. Direction from the aim point: azimuth U(0, 360) degrees; elevation U(30, 85)
   degrees above the bench plane (below 30 the view grazes the bench); 20 % of
   poses are **overhead**, U(70, 88) degrees (short of 90, where a look-at has
   no up).
3. Distance to the aim point: U(1, 3.5) m.
4. Lens: fovy U(48, 72) degrees around the GoPro's 60.44; roll N(0, 4)
   degrees, clipped to 8.
5. Checks, else redraw (up to 200 tries): the camera is inside the room box
   (`ORBIT_ROOM`, inside the walls, under the ceiling at 2.85 m, short of the
   corridor); nothing blocks the first 85 % of the line of sight to the aim
   point (the last stretch may cross bottles and the arm); and a ray from
   outside to the lens meets nothing, so the lens is not inside a wall, the
   shelf or the arm.
6. Pose: `look_at_quat(position, aim)` then the roll about the line of sight.

The ceiling limits the steep views from afar: with the worktop at 0.90 m and
the ceiling cap at 2.85 m, a camera can rise at most about 1.95 m over its aim
point, so at 2.5 to 3.5 m the elevation cannot pass about 34 to 51 degrees.
Those cells of the grid in section 7 are empty for that reason (measured).

**Close (`close_*`)**: the same sampler at 0.35 to 1 m, so a bottle is 30 to
300 px tall. The aim spread is 7.5 cm here: with the orbit's 25 cm, 2 of the
first 4 preview frames showed no vial, because the frame is only about half a
metre wide this close (measured, then fixed).

Bottle heights in the dataset preview (measured, sampled frames):

| Family | Frames sampled | Boxes | Height p5 / p50 / p95 / max |
| --- | ---: | ---: | --- |
| wall mount | 76 | 1,575 | 14 / 22 / 35 / 39 px |
| orbit | 96 | 1,177 | 13 / 31 / 66 / 129 px |
| close | 56 | 248 | 33 / 78 / 174 / 261 px |

### 3.5 Degradation (`degrade`)

30 % of training frames (100 % of `*_shift` frames) are degraded after
rendering, as a real camera and its encoder would: gamma U(0.8, 1.25) and
contrast U(0.85, 1.1); 70 % a Gaussian blur of sigma U(0.3, 1.2); 80 % sensor
noise of sigma U(1, 6); 80 % JPEG at quality 55 to 95. The parameters drawn are
stored in the frame's record.

### 3.6 Ground truth (`render_perfumery.Lab.render`)

The simulator's state writes the truth and nothing else; the detector only ever
sees the RGB frame. Each frame has three segmentation passes:

- **visible**: every geom except see-through glass (alpha < 0.6), so a bottle
  behind a draft shield still counts as visible. Gives the visible box, `xyxy`;
- **samples only**: the full, unoccluded silhouette of every sample bottle.
  Gives `full_xyxy`, and `visible_frac` = visible pixels / full pixels;
- **category map**: sample, shelf bottle, glassware, balance, instrument,
  other. Used to say what a false box fired on.

A bottle is labelled for training when `visible_frac >= 0.3`
(`fixedcam_crops.MIN_VISIBLE`); the ones hidden further are left out rather
than taught as bottles the model cannot see.

Measured bug: NVIDIA's EGL multisamples the offscreen buffer, so at edges a
segmentation pixel averaged two geoms' id colours and read back as a third geom
or an id past the last one. Segmentation now has its own renderer with
`offsamples = 0`; the boxes are identical to those rendered on Windows.

### 3.7 Splits and seeds

Frame `k` of a split uses seed `split.seed + k`, and every split has its own
range of seeds, so no layout, light or pose is shared between train, val and
test. Tests keep the light nominal and the frames clean unless their name says
otherwise.

| Split | Camera | Frames | Role |
| --- | --- | ---: | --- |
| `rail_train` / `rail_val` | wall mount, jittered | 3,000 / 300 | training (the `rail` model used 1,500 / 150) |
| `rail_test` | wall mount, nominal | 150 | the camera the robot uses; no run may lose here |
| `rail_test_shift` | wall mount, strong light, degraded | 100 | proxy for another renderer or a real GoPro |
| `orbit_train` / `orbit_val` / `orbit_test` | orbit, 1 to 3.5 m | 3,000 / 300 / 300 | any angle over 30 degrees |
| `close_train` / `close_val` / `close_test` | orbit, 0.35 to 1 m | 1,500 / 150 / 150 | near views |
| `dark_test`, `orbit_dark_test` | wall mount / orbit, 8 to 50 % light | 150 each | dim room |
| `overhead_test` | orbit, 70 to 88 degrees | 150 | looking straight down |
| `test_open` | wall mount, the open scene (another lab) | 100 | never trained on; not in the render yet |

### 3.8 The render that exists (measured)

Every split of the table except `test_open`: **9,400 frames** (7,500 train,
750 val, 1,150 test), **123,657 labelled vials**. Rendered in 18 min on an RTX
4090 pod in RunPod's EU-RO-1 (32 CPUs, 24 parallel parts, about $0.32; pod
deleted since). Every elevation x bearing cell (6 bands x 12 bearings) holds at
least 35 training frames. Flagged by `dataset_report.py`: 188 frames with no
vial (close views of free worktop, kept as negatives) and 153 with low
contrast (141 dark by design, 12 close views of the white worktop); none with
the camera inside geometry, and no vial lost to the crop.

```bash
export MUJOCO_GL=egl
for i in $(seq 0 23); do
  python computer-vision/scripts/fixedcam_dataset.py --splits rail_train --part $i/24 &
done; wait
python computer-vision/scripts/fixedcam_dataset.py --splits rail_train --merge
```

`--part i/n` renders every n-th frame from the i-th into
`gt.part<i>of<n>.json`; `--merge` joins them into `gt.json`. For scale: 1,900
frames took 2.5 min with 8 processes on an A40, and the laptop's CPU takes
about 2 s a frame. `scripts/orbit_study_pod.sh` does render, convert, train and
score unattended and skips every stage whose output is already there, so a
dropped pod resumes.

Where it is: RunPod network volume `hackspain-orbit-dataset` (id
`mwd17cd5k8`, 25 GB, EU-RO-1), frames at `/workspace/fixedcam` (7.4 GB), and
the exact code that rendered them at `/workspace/code`. A training pod created
in EU-RO-1 with that `networkVolumeId` mounts it with no upload. The A40's data
centre (CA-MTL-1) offers no network volumes. Martí validates the frames in a
private artifact (section 8.1) built from `dataset_report.py`'s output.

## 4. Cropping

**At inference: the bench band (measured).** From the wall mount the bench
always lies between rows 352 and 800 of the 1080. Running `rail` on that
1920 x 448 band alone gives the same accuracy as the whole frame (AP50 0.990,
recall 0.993, 1.2 false boxes a frame at threshold 0.10) in about 0.40x the
time: about 93 ms instead of 233 ms with PyTorch on the laptop's CPU. With
OpenVINO fp16 at a fixed 1920 x 512 input it is 80 ms median (90th percentile
103 ms) with the CPU half busy, against 154 ms for the whole frame
(`scripts/export_and_time.py`). Pass `imgsz=(512, 1920)` to `predict`, or
OpenVINO recompiles on every call and runs about 5x slower. On `main` the
viewer already crops live and replay frames to a fixed band, 30 to 75 % of the
frame's height at full width (`view/backend/table_crop.py`; replay runs `rail`
at 1280 px and 0.47). `labvision/detector.py` does not crop yet, and
`bench_crop.py` (below) computes the band from the camera instead of fixed
fractions.

**At training: every frame cropped to the bench (implemented).**
`scripts/bench_crop.py` projects the worktop box (x -4.5 to 1.5 m, y -1.4 to
0.6 m, from the bench top at z 0.90 m to above the tallest vial at 1.10 m) with
the frame's own camera (`cam_pos`, `cam_xmat`, `fovy_deg` from `gt.json`), pads
it by 8 px and snaps it to multiples of 32 px, the network's stride. From the
wall camera that is a band of about 1920 x 448 to 576 (the jitter moves it); an
orbit frame keeps about 78 % of its pixels on average. `fixedcam_to_yolo.py
--crop` cuts the images and moves the labels, and drops a vial the crop leaves
with under 60 % of its box (`bench_crop.KEEP`). The crop needs only the
camera's pose and field of view, so the same function serves the real camera
from its calibration. What it buys: no training pixels spent on walls and
ceiling, more bottles per mosaic, and the model sees each view as it will run.

**Cropping and training speed.** Ultralytics trains on imgsz x imgsz mosaics,
so at a fixed `imgsz` a cropped image costs the same GPU time per step as a
whole one. The crop changes what a step contains, not what it costs. What cuts
the time per epoch is tiling (proposed):

1. crop to the bench, as above;
2. cut the crop into 640 x 640 tiles at native resolution, overlapping by
   25 % so no vial is always cut, and train at `imgsz 640`: a step costs a
   ninth of one at 1920, and the 9 to 36 px vials stay 9 to 36 px;
3. keep only 10 to 20 % of the tiles with no vial, preferring those with
   boxes, drums or shelving in them;
4. shrink close views to 640 instead of tiling them, so their 30 to 300 px
   vials become 10 to 100 px and are not cut.

Estimated gain: 2 to 3x less time per epoch, and tiles fit in RAM with large
batches. Validate on whole bench crops, not tiles, since that is how the
detector runs; a convolutional model usually transfers from tiles to the
larger input when the object size is unchanged, but this has to be measured.
`scripts/fixedcam_crops.py` already tiles at 384 px for CPU training and can be
adapted.

## 5. Training

**The `rail` run (measured).** `runs/rail/train_yolo26n_gpu.py`: YOLO26n from
COCO weights, whole frames at `imgsz 1920`, batch 8, `cache="ram"`, random
scale held to +-25 % (the vials are tiny), patience 20. 48 s an epoch on 1,500
frames on an A40; stopped by hand at epoch 20 with validation flat. 1,500
frames of one view were enough for AP50 0.990 on that view.

**Model size.** The nano is the only one that meets 100 ms on the laptop's CPU.
`m` takes over a second a frame there; `s` only fits the budget on a GPU. On an
A40 the nano takes 6 ms a frame at 1600 px, so on a GPU either size fits, and
choosing n or s is choosing where the detector runs.

Latency on the laptop's CPU, idle, PyTorch (measured):

| Input | YOLO26n | YOLO26s |
| --- | ---: | ---: |
| 1920 px whole frame | 233 ms | 507 ms |
| 1920 x 448 bench band | about 93 ms (80 ms with OpenVINO fp16) | about 162 ms (estimate) |
| 1280 px | 135 ms (AP50 0.977) | 262 ms |
| 960 px | 71 ms (AP50 0.919) | 181 ms |
| 640 px | 38 ms | 123 ms |

The wider grid of `docs/YOLO26_STUDY.md` (n, s and m on rail, rail + orbit,
and all, plus a third of the data) is ready in `scripts/orbit_study_pod.sh`.
Its rules: ship the nano if it is within 1 point of `s` in recall on
`orbit_test` and `close_test`; no run may lose on `rail_test`; if the full data
beats a third of it by more than 1 point, render more before training longer.

## 6. Scoring

- `scripts/fixedcam_bench.py compare ... --splits rail_test,rail_test_shift`:
  AP50, recall, precision and false boxes a frame per split, with the worktop
  filter (`labvision/evaluation.py`).
- `scripts/viewpoint_study.py WEIGHTS --pick-on rail_val,orbit_val,close_val
  --splits ...`: the same broken down by camera elevation, distance, bottle
  height in pixels and distance from the frame's centre.
- `scripts/limits_sweep.py WEIGHTS --sweeps light,range,elevation`: renders the
  same layouts while one condition moves (light 100 % to 2 %; distance 0.25 to
  3.5 m; elevation 10 to 88 degrees) and reports where recall breaks.
- The threshold is always the best-F1 threshold on the validation splits,
  never on test. It moves with the views: 0.47 whole frame for `rail`, 0.62 on
  `orbit_test`.

What scoring the current model on the new views found (measured, `rail`,
threshold 0.10):

| Test set | Recall | False boxes a frame | AP50 |
| --- | ---: | ---: | ---: |
| `rail_test` | 0.993 | 1.48 | 0.990 |
| `orbit_test` | 0.970 | 4.95 | 0.964 |
| `close_test` | 0.635 | 4.25 | 0.543 |

- The angle is not the problem, the size of the bottle in the picture is:
  recall stays 0.97 to 1.00 up to 75 degrees of elevation and drops to 0.22
  for bottles 96 to 160 px tall and to 0 above 160 px, because `rail` never saw
  a bottle over 36 px. It breaks a large one into cap, label and body, each
  boxed as a small bottle: 266 of the 396 false boxes on `orbit_test`.
- The rest of the false boxes are on things the wall mount never shows up
  close: cardboard boxes, the brown drums under the bench, the shelf rack.
- Recall in the frame's corners is 0.83; looking straight down (75 to 90
  degrees) it is 0.81.
- On the as-built bench `rail` finds 247 of 247 vials, so the misses of the
  robot's scan are downstream of the detector.

## 7. The agreed plan: a reduced training set (agreed 2026-09-19)

Martí's priorities: many elevations and distances; the variety of light matters
less; fewer training images, so training is fast. Light costs nothing (section
3.3), so dropping the dark frames is about focus, not count. The count comes
down by covering an elevation x distance grid evenly instead of taking every
frame.

### 7.1 Selecting from the existing render (no new render)

Each frame's record in `gt.json` holds its elevation, distance, bearing and
whether it is dark, so the set is selected from the 9,400 frames already on the
volume:

- **Leave out** the dark frames (they stay in the dark tests).
- **Wall mount:** 1,500 training frames of the 2,405 non-dark `rail_train`
  frames, and 150 validation frames of the 251 non-dark in `rail_val`.
- **Orbit and close:** a grid of 4 elevation bands x 5 distance bands, at most
  200 frames a cell, spread evenly over 12 bearings (every 30 degrees).

Non-dark `orbit_train` + `close_train` frames per cell, as rendered (measured),
and what a cap of 200 keeps:

| Elevation \ distance | 0.35-0.6 m | 0.6-1.0 m | 1.0-1.75 m | 1.75-2.5 m | 2.5-3.5 m | kept |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 30-45 degrees | 116 | 141 | 283 | 278 | 223 | 857 |
| 45-60 degrees | 103 | 158 | 310 | 228 | 13 | 674 |
| 60-75 degrees | 129 | 163 | 354 | 128 | 0 | 620 |
| 75-88 degrees | 113 | 211 | 387 | 88 | 0 | 601 |
| **all** | | | | | | **2,752** of 3,426 |

The empty and nearly empty cells at 2.5 to 3.5 m are the ceiling (section
3.4): those views do not exist in this room. The cap is a ceiling per cell, not
a target. Frames with no vial stay in; they are negatives.

| | Train | Val | Test |
| --- | ---: | ---: | ---: |
| Wall mount | 1,500 | 150 | 150 `rail_test` + 100 `rail_test_shift` |
| Orbit + close grid | 2,752 | 322 (all non-dark `orbit_val` + `close_val`) | 300 `orbit_test` + 150 `close_test` + 150 `overhead_test` |
| Reported, not decisive | | | 150 `dark_test` + 150 `orbit_dark_test` |
| **Total** | **about 4,250** | **about 470** | **850 + 300** |

That is about 4,250 training frames instead of 7,500 or of the 10,500 a
separate lab set would add (section 10.3).

### 7.2 Optional additions (each needs a small new render)

- `test_open`, 100 frames of another lab, never trained on: minutes on a pod.
  It is the only measure of how the model does in a room it has not seen.
- Low cameras, 10 to 30 degrees (eye height across the bench): about 600
  training and 100 test frames, which needs an elevation range per split in
  `fixedcam_dataset.py`. Measure first with `limits_sweep.py --sweeps
  elevation`, which already goes down to 10 degrees: if the model holds there,
  skip it.

### 7.3 The training run

- YOLO26n, fine-tuned from `weights/yolo26n_rail_general.pt` rather than COCO,
  expected to converge in about 20 epochs instead of 30 (estimate).
  `runs/orbit/train_yolo26_gpu.py` has no `--weights` flag yet (it loads
  `yolo26<size>.pt`); add one, as `runs/rail/train_yolo26n_gpu.py` has.
- Every frame cropped to the bench, `imgsz 1920`, random scale +-50 % (bottle
  heights span 30x), patience 12, `cache="ram"`.
- Or, to train about 2 to 3x faster, 640 px tiles (section 4), validated on
  whole bench crops.
- Optional, for precision: mine hard negatives. Run `rail` over the training
  frames and repeat 2 to 3x the tiles where it fires on boxes, drums or
  shelving (a third of its false boxes on the new views).
- On a pod in EU-RO-1 mounting the volume.

### 7.4 Time and cost

| Step | Time | Cost |
| --- | --- | --- |
| Selection and conversion on the pod | minutes | cents |
| Training at 1920, about 2.3 min an epoch, 20 to 30 epochs | **45 to 70 min** (estimate) | about $1 |
| Training on 640 px tiles | **20 to 30 min** (estimate) | under $0.50 |
| Scoring all tests | 10 to 15 min | cents |

The estimates scale the one measurement (48 s an epoch on 1,500 frames at 1920
on an A40) with the number of frames. The first epoch on the pod gives the real
figure.

### 7.5 When the new model is accepted

1. It does not lose on `rail_test` against `rail` (AP50 0.990, recall 0.993 at
   0.10). That is the camera the demo uses.
2. It gains on `orbit_test` and `close_test`, where `rail` is at 0.964 and
   0.543 AP50.
3. On the laptop, bench crop and OpenVINO, it runs in 100 ms or less
   (`export_and_time.py --format openvino` at the crop's shape).
4. Data check: trained on a third of the selection, is it more than 1 point
   worse? If so, the selection was too small. Add frames back from the volume
   before training longer.

## 8. State and next steps (handoff)

### 8.1 Where everything is

| What | Where |
| --- | --- |
| This document | `computer-vision/docs/YOLO26_TRAINING_PIPELINE.md` on `main` (and a copy in `../Hackspain-orbit`) |
| Dataset code | `C:\Users\marti\Documents\Hackspain-orbit`, branch `vision/orbit-dataset` from `main` e0ae666, **nothing committed**: `fixedcam_dataset.py`, `fixedcam_to_yolo.py`, `fixedcam_twin.py` changed; `bench_crop.py`, `dataset_report.py`, `viewpoint_study.py`, `limits_sweep.py`, `export_and_time.py`, `orbit_study_pod.sh`, `runs/orbit/` new. `docs/YOLO26_STUDY.md` is already on `main` (b855374) |
| Frames (9,400) | RunPod network volume `hackspain-orbit-dataset` (`mwd17cd5k8`), EU-RO-1, `/workspace/fixedcam`; the code that rendered them at `/workspace/code` |
| Labels and report, locally | `gt.json` of every split and the report in the scratchpad of session 36ec724d, `orbit/final/` (a temporary folder: copy what is needed) |
| Validation artifact (Martí's, private) | https://claude.ai/artifact/3anS7TBxGczCNA2Rtf1TK8 |
| Current weights | `computer-vision/weights/yolo26n_rail_general.pt` (backend `rail`) |
| RunPod access | key in `~/.runpod-render/api_key` on Martí's laptop (never print it); pods `isaac-render-*` are Eloi's |

### 8.2 Next steps, in order

1. Martí validates the frames in the artifact. Nothing is trained before his
   OK.
2. Commit the branch's code. Push only when Martí says so, fetching `main`
   first: it moves fast.
3. Write the selection of section 7.1 as a script (for example
   `scripts/select_frames.py`) that writes filtered split folders (`sel_train`,
   `sel_val`) with their `gt.json` and hard-linked frames, so
   `fixedcam_to_yolo.py sel_train:train sel_val:val --crop` runs unchanged.
   Make it deterministic: sort by seed and fill each cell round-robin over the
   12 bearings.
4. Add `--weights` to `runs/orbit/train_yolo26_gpu.py`; train as in 7.3 on a
   pod in EU-RO-1 mounting the volume.
5. Score with `viewpoint_study.py` and `fixedcam_bench.py`, threshold from the
   cropped validation frames; apply the rules of 7.5.
6. Time it on the laptop with `export_and_time.py --format openvino`.
7. Put the bench crop in `labvision/detector.py` (from the camera's
   calibration, through `bench_crop`), register the new weights as a backend
   with their threshold, and set the viewer's display threshold. The viewer's
   own fixed band (`view/backend/table_crop.py`) should then match it.
8. Delete the pod when done. Keep the volume until Martí says otherwise.

Later, in this order of value for cost: the optional additions of 7.2, tiles
and hard negatives (section 4 and 7.3), lab randomisation (section 10.3), and
Isaac frames (section 11).

### 8.3 Open decisions for Martí

- Low cameras (10 to 30 degrees): train on them, or only measure the limit?
- 1920 whole crops or 640 px tiles: the tiles are faster to train but not yet
  proven at inference.
- Where the 100 ms must hold: on the laptop's CPU (nano, crop, OpenVINO) or on
  an NVIDIA GPU (then `s` is affordable).
- Lab randomisation (section 10.3) as a second phase: yes or no.

### 8.4 Gotchas met on the way

- **Laptop network:** only ports 80 and 443 get out, so no SSH to pods. Drive
  them through a small upload server behind RunPod's HTTPS proxy
  (`https://<pod>-8000.proxy.runpod.net`): PUT a tarball, the boot script
  unpacks it and runs `pod_run.sh`, progress in `/root/out/STAGE`.
- **Pod image:** `runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04`
  boots in about 30 s; a 2.4.0 image hung 16 min. Pin `allowedCudaVersions`
  to 12.8 and 13.0 (driver 570/580).
- **Network volumes** exist in EU-RO-1, not in CA-MTL-1.
- **Windows to pod:** shell scripts checked out on Windows have CRLF endings;
  strip `\r` on the pod. Tar with `--owner=0 --group=0 --numeric-owner`, or
  root's untar fails on uid 197609. Git Bash's `tar` reads `C:` as a remote
  host: pass `--force-local`.
- **Ultralytics** nests `project=runs/x` under `runs/detect/`.
- **OpenVINO** needs a fixed `imgsz` at `predict`, or it recompiles every call.
- **The laptop's CPU** throttles under load (it fell to 20 % in an overnight
  run): run one heavy job at a time, and read timings taken under load as
  ratios.
- **A bug on `main`** since `773c702`: `render_perfumery.Lab(scene=...)`
  ignores `rp.SCENE`, so the `rail_*` splits of `fixedcam_dataset.py` render
  the gantry scene with no arm, and the IK crashes. Fixed on the branch only
  (`load_lab` and `fixedcam_twin.py` pass the scene).

## 9. What we learned

1. **The size of a bottle in the picture limited the current model, not the
   angle.** `rail` holds 0.97 recall at any elevation up to 75 degrees but
   breaks bottles taller than about 96 px into parts, because it never saw one
   over 36 px. Near views fix that; more bearings alone would not have.
2. **The look of the lab moves the scores more than the camera does.** With
   the camera fixed, a new scene cost 0.19 AP50, and between MuJoCo and Isaac
   the models nearly stopped working. Angles are covered now; appearance is not
   (section 10).
3. **The image count follows the coverage of camera poses.** Light, tint and
   degradation are drawn per frame and cost nothing. 1,500 frames were enough
   for one view, so the grid needs a few hundred frames a cell at most.
4. **The room shapes the grid.** The ceiling rules out steep views from far
   away. Cap the cells; do not try to fill them.
5. **Cropping to the bench is free accuracy-wise and 2.5x faster at
   inference.** At training it only saves time together with tiling at a
   smaller `imgsz`.
6. **The threshold belongs to the view.** 0.47 for the wall mount, 0.62 for
   orbit views: always pick it on validation frames of the views that will be
   run.
7. **The detector is not the scan's bottleneck.** It boxes 247 of 247 vials on
   the as-built bench. The fixed camera does miss 3 at the aisle edge, and the
   wrist camera reads those. The two-camera design (the fixed camera proposes,
   the wrist camera confirms) is what absorbs a detector's misses and false
   boxes.
8. **Check the renders, not only the numbers.** Every rendering bug was found
   by looking at frames: grey frames from a lens inside the wall, wrong
   segmentation ids from multisampling, the wrong scene loaded silently, empty
   close views from too wide an aim spread.
9. **Isaac Sim** (details in 11.1): layouts that never move leak between
   splits; boxes come per mesh part; unlabelled bottles become negatives; pose
   edits must go through Fabric; camera axes differ between APIs; prim paths
   say `SMP_0001`, not `SMP-0001`.

## 10. Edge cases, and how the robot adapts to a new lab

The render covers where the camera stands very widely, but only in one lab:
every frame is the rail scene, with the same room, bench, objects and amber
vials. Camera placement is what changes most visibly from one lab to another,
but it is not the only thing that changes, and it is not the one that has cost
the most so far. With the camera held fixed, moving from the gantry scene to
the open scene dropped the fine-tuned nano from AP50 0.864 to 0.675
(`docs/FIXED_CAMERA_BENCHMARK.md`).

### 10.1 What can change, and what the dataset covers

| Case | Covered by the render? | What is known |
| --- | --- | --- |
| Camera at another bearing or height, 30 to 88 degrees above the bench | yes | `rail` already holds 0.97 recall on `orbit_test` |
| Camera below 30 degrees (eye height, across the bench) | no | `limits_sweep.py` can measure it down to 10 degrees |
| Camera much nearer, so bottles are large (60 to 300 px) | yes, `close_*` | `rail` fell to 0.22 recall at 96 to 160 px and 0 above 160 px |
| Looking straight down | yes, overhead poses + `overhead_test` | `rail` recall 0.81 at 75 to 90 degrees |
| Bottles in the frame's corners | partly | `rail` recall 0.83 there |
| Another lens: wide or fisheye, distortion, other resolution | fovy 48 to 72 only, no distortion, always 1920 x 1080 | undistort from calibration first |
| Another room: walls, floor, bench material, clutter | no (worktop tint only) | a new scene cost 0.19 AP50 with the camera fixed |
| Look-alike objects: brown boxes, drums, amber reagent bottles | only what the scene holds | 1.6 false boxes a frame on boxes, drums and the shelf rack from orbit views |
| Other containers: clear glass, white HDPE, vials in racks, other caps | no, amber vials only | the model will miss them or box them unpredictably |
| Dense packing and occlusion by the arm | yes: 35 % clusters, arm in every frame | a bottle under 30 % visible is not labelled, so it will not be found either |
| Dim room | rendered, left out of the reduced training set | reported by `dark_test` and `orbit_dark_test` |
| Windows, backlight, glare and reflections on glass | no | never rendered |
| Real sensor: noise, blur, JPEG, exposure | 30 % of training frames degraded | a degraded camera cost the earlier nano 0.10 AP50 |
| Motion blur | no | |
| Simulation to reality: real glass, real textures | no | the largest unknown: no real photograph has been scored yet |
| Operating threshold | set per view on validation | 0.47 on the wall mount, 0.62 on orbit views |
| Latency on the lab's computer | 100 ms only with the nano, the crop and OpenVINO on a CPU | a GPU takes any size in a few ms |

### 10.2 How the robot adapts to a new lab (proposed)

1. **Calibrate the fixed camera** (intrinsics and pose relative to the bench).
   It gives the bench crop, the pixel-to-bench mapping, and whether the lens
   needs undistorting.
2. **Photograph the bench 20 to 50 times** with vials placed at random.
   Label them: pseudo-label with YOLO-World and correct by hand, as was done
   for Isaac's unlabelled vials. Score the model on them and set the threshold
   there.
3. **Fine-tune if recall is short**, on those photographs mixed with the
   simulated frames: minutes on a rented GPU.
4. **Lean on the two cameras.** The fixed camera proposes and the wrist camera
   confirms by reading the label. A false box costs one look, not a wrong
   pick. The wrist camera also finds vials the fixed camera misses, which is
   how the scan reaches 19 of 19.
5. **For a lab that is different in kind**, build its twin (MuJoCo or Isaac)
   and run this pipeline on it.

### 10.3 Lab randomisation, a possible second phase (proposed)

No new lab has to be modelled: the rail scene already holds enough to rearrange
into many. Measured inventory of `minihannover_rail_scene.xml`:

- 7 instruments as bodies of their own (the sink, 5 balances, the GC-MS and
  the UV-Vis-NIR), so they can be moved without editing the XML;
- the rest of the room as one static body of 1,409 geoms: chairs, cartons,
  drums, racks, office desks, people, fume extraction arms, the drying rack;
  grouped by object, they can be moved or hidden per frame through the model's
  geom poses;
- 213 textures, 398 materials and 11 lights.

Per frame, keeping the bench, the rail and the arm where they are (the robot's
workspace):

1. **appearance**, the cheapest and the one aimed at the gap measured in
   section 9: textures and colours of walls, floor, worktop and furniture from
   the existing textures, lights moved, dimmed or switched off;
2. **arrangement**: instruments and furniture moved, removed or repeated, plus
   look-alike distractors (brown boxes, clear bottles, amber reagent bottles)
   as negatives;
3. **scenes**: train on the gantry and rail scenes and keep the open scene out
   as the unseen lab.

Randomising the lab in the same frames as the camera costs no extra frames;
a separate `lab_*` set of 3,000 / 300 / 300 was the other option. Measure it
on `test_open` and on held-out seeds. Swapping textures at run time has to be
checked on about 20 frames first. Estimated effort: half a day to a day of
work, minutes of rendering.

Other ways to improve the model, by expected gain for cost: hard negatives
(7.3); native resolution for the small vials (tiles give it for free); a
threshold per view; OpenVINO for headroom within 100 ms (80 ms measured on the
crop), which could make room for a larger input or `s`; confirming a vial over
2 or 3 frames of the still fixed camera (`vision_pick` already tracks
detections); Isaac frames and real photographs for the step to reality.

## 11. Replicating it in Isaac Sim

### 11.1 What Isaac already has, and what went wrong before

- The Isaac scene is the MuJoCo scene exported to USD:
  `simulation/scripts/export_usd.py` (MuJoCo's own USD exporter, no Isaac
  needed) writes `lab_usd/`, with every name sanitised to `[A-Za-z0-9_]`, so
  `SMP-0001` becomes `SMP_0001` in prim paths. Eloi's
  `simulation/scripts/dataset_gen_v3.py` renders it with Replicator's
  `BasicWriter`. Setup: `simulation/runpod-isaac.md` (official image
  `nvcr.io/nvidia/isaac-sim:4.5.0`, the `dockerEntrypoint` override, about
  4.5 min to first boot, no RTX 5090, driver 570/580).
- `lab_dataset_v1` and `v2` never moved the bottles (only light and a small
  camera jitter changed). A random frame split then leaks, and a model learns
  positions. `v3` reshuffles every bottle each state.
- Isaac boxed every mesh of a bottle separately (body, cap, label): 133,400
  boxes were 48,100 bottles. `isaac_dataset_to_yolo.py` merges them by union
  per (image, sample id).
- About 220 `stock_reserve` vials had no semantic label, so no box: positives
  taught as background. They were pseudo-labelled with YOLO-World as a stopgap.
- `v3` found that raw USD `xformOp` edits between renders do not reach the
  render (Fabric caches transforms), while light attribute edits do. Poses go
  through `isaacsim.core.prims.XFormPrim.set_world_poses` followed by
  `app.update()` before the render.
- Moving the cameras through Fabric flipped the `general` view in `v3`, so v3
  kept the cameras at their base poses. A likely cause is an axis convention:
  USD and MuJoCo cameras both look down -Z with +Y up, while Isaac's `Camera`
  helper defaults to a "world" convention (+X forward, +Z up). Check which one
  the call assumes.
- The model trained on Isaac's `v2` scored AP50 0.780 on its held-out camera
  but 0.574 on MuJoCo's `rail_test`, and MuJoCo-trained models found almost
  nothing on Isaac frames: the renderer gap is large in both directions.
- The MuJoCo twin camera did not overlay Isaac's `general` view exactly
  (fovy 36.28 in the twin), so intrinsics must be checked, not assumed.

### 11.2 Recommended approach: MuJoCo plans every frame, Isaac renders it (proposed)

Rather than re-implement the layout sampler, the IK, the ray checks and the
camera sampler in Isaac, let `fixedcam_dataset.py` draw each frame exactly as
it does now and write the resulting state; an Isaac script then only applies
that state and renders. Both simulators then show the same frame, which gives:

- the same distributions of layouts, arm poses, angles and distances, with no
  second implementation to keep in step;
- paired frames, so the renderer gap is measured frame by frame, and a
  MuJoCo + Isaac mix differs only in appearance;
- a check of Isaac's truth: its boxes should match MuJoCo's boxes of the same
  frame.

Steps:

1. **Export the rail scene.** `python simulation/scripts/export_usd.py
   simulation/models/minihannover_rail_scene.xml OUT` with the extra bottles of
   `EXTRA_PER_SIZE` included (they are added in memory by `render_perfumery`,
   so the export must go through the same `Lab` object, not the XML alone).
   Render at 1920 x 1080, not the 1600 x 900 of v1 to v3, so the crop and the
   pixel sizes match the GoPro.
2. **Dump the state per frame.** Add a `--dump-state` flag to
   `fixedcam_dataset.py` that writes, next to `gt.json`, for each frame: the
   world pose (position and quaternion) of every geom that is not where the
   export put it (bottles, parked bottles, arm links, carriage), the camera's
   `cam_xpos`, `cam_xmat` and fovy, and the light and tint draws. `gt.json`
   already stores the camera and the randomisation; the geom poses are what is
   missing. Geom poses rather than joint angles, because the exporter writes one
   prim per geom and Isaac then needs no IK and no articulation.
3. **Apply it in Isaac**, per frame:
   - geoms: `XFormPrim(paths).set_world_poses(positions, orientations)`, then
     `app.update()` (the path v3 proved);
   - camera: one Replicator camera per render product, its world pose set from
     `cam_xpos` and `cam_xmat` (the two simulators share the -Z forward, +Y up
     convention). Isaac uses square pixels and ignores the USD vertical
     aperture, so set `focalLength = f_px * horizontalAperture / 1920` with
     `f_px = 540 / tan(fovy / 2)`: 10.12 mm for fovy 60.44 with the default
     20.955 mm aperture;
   - lights: intensity and colour attribute edits, the recorded scale on top of
     the base multiplier (`render_usd.py` uses `LIGHTMUL = 40` because the
     exporter's lights are far too dim for RTX; v3 drew 28 to 52);
   - worktop tint: the worktop material's diffuse colour input;
   - render with `rep.orchestrator.step(rt_subframes=...)` of 4 or more, so the
     real-time renderer does not ghost after every bottle teleports.
4. **Degrade after rendering** with the same `degrade()` and the parameters
   recorded for that frame in `gt.json`, so the degraded frames match too.
5. **Truth.** `BasicWriter` with `rgb`, `bounding_box_2d_tight` (visible box
   and `occlusionRatio`), `bounding_box_2d_loose` (full box), `camera_params`
   and `instance_id_segmentation`. Label every sample bottle, including the
   `stock_reserve` ones: every mesh of a bottle gets the class of its sample
   id. Then `scripts/isaac_replicator_to_gt.py` writes the same `gt.json`,
   camera fields (`cam_pos`, `cam_xmat`, `fovy_deg`) included, so
   `fixedcam_to_yolo.py --crop` and everything else downstream run unchanged.
   Two fixes the converter needs first:
   - its sample-id pattern is `(SMP|PWD)-\d{4}` but the exported prims say
     `SMP_0001`: accept `[-_]` and normalise to the hyphen;
   - it pairs boxes per prim, so it keeps one box per mesh part: merge the
     parts by union per (frame, sample id), as `isaac_dataset_to_yolo.py` does,
     and combine their visible fractions weighted by pixels.
6. **Acceptance test before rendering at scale**, on 50 frames: for each
   bottle, the IoU between Isaac's box and MuJoCo's box of the same frame. A
   median under about 0.8, or boxes offset all one way, means a camera pose,
   axis or focal length error. Look at a contact sheet with both boxes drawn.
   Also check see-through glass: MuJoCo's truth does not let glass hide a
   bottle; if Isaac's occlusion ratio does, bottles behind a draft shield will
   fall under the 30 % visibility floor and turn into unlabelled positives.

For the reduced plan of section 7, replay only the selected frames: about
4,250 training and 470 validation frames, plus the test splits.

### 11.3 If the Isaac scene stops being the MuJoCo export

If Eloi's scene diverges (other assets, other layout), the samplers have to be
re-implemented in Isaac. The numbers to copy:

| Step | MuJoCo (`fixedcam_dataset.py`) | Isaac |
| --- | --- | --- |
| Bottle layout | 8 to 34 bottles on free worktop, 35 % clusters (15 x 12 cm), 10 % as-built | a Python sampler as in v3's `reshuffle`, poses through `XFormPrim` |
| Arm | 75 % IK reach 5 to 40 cm above the worktop, else parked | joint targets from `rail_kinematics.reach` run offline, or recorded MuJoCo poses |
| Light | x0.55 to 1.45, colour 3.5 % | `UsdLux` intensity and colour edits |
| Worktop | 50 % tinted x0.78 to 1.0 | material diffuse colour |
| Wall mount | +-15 cm into the room and down, +-5 degrees | camera pose per frame |
| Orbit | aim point 70 % at a bottle +-25 cm; azimuth 0 to 360; elevation 30 to 85 (20 % at 70 to 88); 1 to 3.5 m; fovy 48 to 72; roll +-8 | same numbers, pose per frame; cover the grid of 7.1 |
| Close | the same at 0.35 to 1 m, aim spread 7.5 cm | same |
| Line of sight | MuJoCo ray casts | PhysX scene queries need colliders, which the export may lack; alternatively render `distance_to_camera` and reject a frame whose aim pixel is nearer than 85 % of the range or whose image is nearly flat |
| Degradation | `degrade()` after rendering | the same function |
| Truth | segmentation passes, `visible_frac` | tight and loose boxes, `occlusionRatio` |

Whatever the route, never split a static layout by random frames, and hold out
seeds (or whole cameras) for validation and test, as in section 3.7.

### 11.4 The experiments to run on Isaac frames (proposed)

1. Render `isaac_rail_test` (the `rail_test` seeds) and `isaac_orbit_test`, and
   score today's `rail` on them. This measures the gap with no training.
2. Fine-tune the MuJoCo-trained model on Isaac's training frames alone.
3. Fine-tune on a MuJoCo + Isaac mix, half and half to start.
4. Score all three on the MuJoCo and the Isaac test sets with
   `viewpoint_study.py`, threshold picked on the mixed validation set. Keep a
   model only if it does not lose on MuJoCo's `rail_test` and gains on Isaac's.

A handful of real photographs of the bench, labelled by hand, would be worth
more than any of these: they are the only test of the step to the real camera.

### 11.5 Time and cost

| Step | Where | Time | Cost |
| --- | --- | --- | --- |
| MuJoCo render, 9,400 frames | RTX 4090, EU-RO-1, 24 parts | 18 min (measured) | about $0.32 |
| Isaac pod start | A5000 or A40 | about 6 min image pull + 4.5 min first boot (measured) | about $0.10 |
| Isaac render | A40 | unknown: measure on the first 50 frames | |
| Training, nano, 1,500 frames | A40 | 48 s an epoch (measured) | |
| Training, nano, the reduced set | RTX 4090 or A40 | 45 to 70 min at 1920, 20 to 30 min on tiles (estimate) | about $0.50 to $1 |

## 12. Files

| File | What it does |
| --- | --- |
| `scripts/fixedcam_dataset.py` | renders the splits: layout, arm, light, camera, degradation, truth |
| `scripts/render_perfumery.py` | `Lab`: scene, extra bottles, segmentation truth |
| `simulation/scripts/rail_kinematics.py` | the arm's IK used to pose it |
| `scripts/bench_crop.py` | the part of a frame the bench occupies, from the camera's pose and field of view |
| `scripts/fixedcam_to_yolo.py` | `gt.json` to a YOLO dataset, one class, `--crop` to the bench |
| `scripts/fixedcam_crops.py` | crops and tiles for training at a smaller size |
| `scripts/dataset_report.py` | statistics and samples of a rendered dataset, for its validation artifact |
| `runs/rail/train_yolo26n_gpu.py` | the `rail` run |
| `runs/orbit/train_yolo26_gpu.py` | the next runs, any model size and input size |
| `scripts/orbit_study_pod.sh` | render, convert, train and score unattended on a pod |
| `scripts/fixedcam_bench.py` | scores by split |
| `scripts/viewpoint_study.py` | scores by elevation, distance, bottle size and position in the frame |
| `scripts/limits_sweep.py` | finds where a detector breaks as light, distance or elevation moves |
| `scripts/export_and_time.py` | exports to OpenVINO, CoreML or keeps PyTorch, and times whole `predict` calls on this machine |
| `scripts/isaac_replicator_to_gt.py` | Replicator `BasicWriter` output to the same `gt.json` |
| `scripts/isaac_dataset_to_yolo.py` | Isaac COCO datasets (v1 to v3) to YOLO, merging mesh parts |
| `simulation/scripts/export_usd.py` | MuJoCo scene to USD for Isaac |
| `simulation/scripts/dataset_gen_v3.py` | Isaac Replicator generator with per-state reshuffle |
