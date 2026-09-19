# The YOLO26 plan: one model, one resolution, then more benches and more labs

Written 2026-09-19, late evening. This is the single plan. It replaces section 7
of `YOLO26_TRAINING_PIPELINE.md` ("the agreed plan") and "The runs" of
`YOLO26_STUDY.md` (the grid of seven runs), which were written in parallel and
disagreed. Those two documents stay as the record of what was measured and how
the pipeline works; what to do next is here.

Every line is one of: **decided** (by Martí), **measured**, **done**, or
**proposed** (nobody has agreed to it or run it).

## 1. What is decided

| | |
| --- | --- |
| Model | **YOLO26n only.** `s` and `m` are dropped: the nano already scores 0.99 on the view the robot uses, and what it lacks is data, not capacity (measured, section 3) |
| Input | **The bench band at the frames' native 1920 px**, which is what the demo runs. On `main` the live viewer crops rows 30 to 75 % of the frame at full width (1920 x 486, `view/backend/table_crop.py`) and predicts at native size (`yolo_worker.py`); the replay does the same at 1280; `vision_pick.py` predicts on the whole 1920 px frame. Training crops each frame to the bench with `bench_crop.py` (1920 x 448 to 576 from the wall mount) and trains at `imgsz 1920` |
| Demo machine | A teammate's **Mac with a GPU and 128 GB**. `vision_pick.py` already picks `mps`. Nothing has been timed there; the nano on a 1920 x 512 band is expected to be far inside 100 ms on it (proposed: confirm with one command, section 6) |
| Data | **MuJoCo renders only** |
| Light | Its variety matters less than elevation and distance. It is drawn per frame and costs no frames either way; the dark frames are left out of training and kept as tests |
| Start from | `weights/yolo26n_rail_general.pt` (`rail`), not COCO |

What this closes: the n-versus-s question, every run at 960 or 1280 px, and
OpenVINO or int8 as a requirement. OpenVINO stays as the fallback if the demo
ever has to run on the i5 laptop: nano on the band, 80 ms median (measured).

## 2. What exists

- **9,400 rendered frames, 123,657 labelled vials** (done), on the RunPod volume
  `hackspain-orbit-dataset` (`mwd17cd5k8`, EU-RO-1, `/workspace/fixedcam`), with
  the exact code beside them. Wall mount 3,550, orbit 3,600, close 1,800, extra
  tests 450. Record and how to regenerate:
  `docs/presentacion/dataset_viales/README.md` in the main checkout; labels of
  every frame locally in `fuentes/etiquetas_gt.tgz`.
- **The review page** (done): https://claude.ai/artifact/3anS7TBxGczCNA2Rtf1TK8
  (private), and offline in `dataset_viales/pagina/index.html`: polar map of
  every camera pose, coverage by elevation and bearing, thumbnails, samples.
- **The code** (done, **uncommitted**, branch `vision/orbit-dataset`): renderer
  splits, `bench_crop.py`, `fixedcam_to_yolo.py --crop`, `dataset_report.py`,
  `viewpoint_study.py`, `limits_sweep.py`, `export_and_time.py`,
  `runs/orbit/train_yolo26_gpu.py` (now with `--weights`), `orbit_study_pod.sh`.
- **A correction made while writing this** (done): an edit of mine had cut the
  training splits to 3,500 frames and changed their elevation and dark share,
  which would have made the same seeds render different frames than the ones
  on the volume. `fixedcam_dataset.py` is back to what rendered the 9,400,
  checked line by line against `pod/codigo_render.tgz`; the only differences
  left are additions (the `low_*` splits below).

## 3. What the measurements say (measured, detector `rail`)

| where | recall | false boxes a frame |
| --- | ---: | ---: |
| wall mount (`rail_test`) | 0.993 | 1.5 |
| any bearing, 1 to 3.5 m, 30 to 85 degrees | 0.970 | 5.0 |
| overhead, 70 to 88 degrees | 0.962 | 7.3 |
| close, 0.35 to 1 m | 0.635 | 4.3 |
| low camera, 20 / 10 degrees | 0.939 / 0.885 | 13.6 / 10.9 |
| light at 15 % / 10 % / 6 % | 0.951 / 0.511 / 0.000 | none appear |

- The failure is the size of the bottle in the picture: trained on 9 to 36 px,
  `rail` breaks a bottle over 64 px into cap, label and body and misses it over
  96 px. Most false boxes from above and from near are those fragments.
- The angle is not a failure between 30 and 75 degrees. Below 30 it is.
- Light is a cliff under 15 %, not a slope, and the detector goes quiet there
  rather than wrong. Not worth training frames (decided).
- `YOLO26_TRAINING_PIPELINE.md` quotes 0.81 recall looking straight down. That
  was 42 bottles of `orbit_test`; `overhead_test` gives 0.962. The problem from
  above is false boxes, not misses.
- On the as-built bench `rail` boxes 247 of 247 vials.

## 4. Phase 1: the model for the demo (no new render)

Selection from the 9,400 frames, as agreed in the pipeline document and
unchanged: no dark frames; wall mount 1,500 train and 150 val; orbit and close
on a grid of 4 elevation bands by 5 distance bands, at most 200 frames a cell,
spread over 12 bearings: 2,752 of 3,426. **About 4,250 training and 470
validation frames.**

1. `scripts/select_frames.py` (to write): reads each split's `gt.json`, writes
   `sel_train` and `sel_val` folders with hard-linked frames. Deterministic:
   sorted by seed, cells filled round-robin over the bearings. It can be written
   and checked here against `etiquetas_gt.tgz` before any pod exists: the cell
   counts must match the table in the pipeline document.
2. Pod in EU-RO-1 mounting the volume. `fixedcam_to_yolo.py sel_train:train
   sel_val:val --crop`.
3. `runs/orbit/train_yolo26_gpu.py DATA --size n --imgsz 1920 --weights
   weights/yolo26n_rail_general.pt --name n_sel_1920`, random scale +-50 %,
   patience 12. **45 to 70 min, about 1 USD** (estimate: 48 s an epoch on 1,500
   frames measured, scaled by frames, 20 to 30 epochs).
4. Score: `viewpoint_study.py` on all seven tests with the threshold from the
   cropped validation frames; `limits_sweep.py` for the before and after of
   section 3 (its frames are rendered already and reused).
5. Accept if it does not lose on `rail_test` (0.990 AP50, 0.993 recall), and
   gains on `close_test` (0.543 AP50) and `orbit_test` (0.964).
6. Time it on the Mac (section 6), register it in `labvision/detector.py` with
   its threshold, and make `labvision` crop with `bench_crop` so the viewer's
   fixed band and the library agree.

One ablation is worth its 25 minutes (proposed): the same run on a third of the
selection. If the full selection wins by more than a point, Phase 2 should add
frames rather than only variety.

Dropped from earlier plans: the 640 px tiles (they buy training time, which at
one hour is not the constraint, and they are unproven at inference) and the
seven-run grid.

## 5. Phase 2: more benches and more labs

The 9,400 frames cover where the camera stands very widely, and one bench in
one room. Two things are missing, in this order of value.

### 5.1 Bench layouts: the seeded patterns already on `main`

`simulation/scripts/bottle_patterns.py` (Nacho, `f3a0f46`) draws a whole
worktop from one integer: 10 to 75 flasks, spacing 4 to 60 mm, scattered,
clustered, **in rack-like rows** or **crowded into one stretch**, from five
flask sizes. Ten are catalogued, `p01` (16 flasks, spread) to `p10` (71 in
rows), and since `f0f2505` the viewer on `main` builds the rail scene with one
of the ten, at random, on every page load (`view/backend/scene_patterns.py`) —
so **the demo already shows benches the detector was never trained on**. The dataset's own
`lay_out` stands 8 to 34 bottles, scattered or in one Gaussian cluster: no
rows, nothing over 34, nothing tighter than its free-spot test allows.

Measure before rendering at scale (proposed, minutes):

1. `pattern_test`: the ten catalogued patterns, each from the wall mount, 10
   orbit poses and 5 close poses: 160 frames.
2. Score `rail` and the Phase 1 model on it, broken down by pattern style and
   spacing. If rows at 4 mm spacing score like the rest, skip 5.1's training
   render; if not, the gap sizes it.

Then, if needed:

| split | frames | what |
| --- | ---: | --- |
| `pattern_train` | 1,500 | a pattern seed drawn per frame from seeds that exclude the catalogued ten; 500 wall mount, 700 orbit, 300 close |
| `pattern_val` | 150 | the same, other seeds |
| `pattern_test` | 160 | the catalogued `p01` to `p10` only: the benches of the demo are the test |

How (proposed): the viewer already builds the rail scene with a pattern in
memory (`scene_patterns.build_pattern`), so the patterns are known to fit the
rail scene's desk. Two routes, to be chosen after reading that builder against
`render_perfumery.Lab`, which the truth code depends on:

- load the pattern's model as the viewer does and teach `Lab` to find its
  flasks (exactly the demo's benches; needs `Lab`'s sample bookkeeping, the
  segmentation ids and the movable-bottle list to work on that model);
- or give `lay_out` a second mode that takes the flask positions and sizes from
  `bottle_patterns` for the frame's seed and stands `Lab`'s own movable bottles
  there (arm, light, camera and truth code run unchanged; the flasks are the
  dataset's labelled vials rather than the pattern's own).

Either way 75 flasks need more than today's 34 movable bottles. Raising
`EXTRA_PER_SIZE` changes the model and therefore every frame of every existing
seed, so it must be a per-split setting, with the regression test that the
first 16 frames of `rail_train` still match the volume's.

### 5.2 Lab dispositions: the room around the bench

Measured earlier with the camera held fixed: moving to another scene cost 0.19
AP50. That is larger than anything camera placement cost. The rail scene holds
enough to rearrange into many labs without modelling a new one (inventory in
section 10.3 of the pipeline document): 7 instruments as bodies of their own,
1,409 static geoms of furniture and clutter, 213 textures, 398 materials, 11
lights. Per frame, with the bench, rail and arm left where they are:

1. **appearance**: colours and textures of walls, floor, worktop and furniture;
   lights moved or switched off;
2. **arrangement**: balances, GC-MS and UV-Vis moved along the bench or taken
   off it; chairs, cartons, drums and racks moved or hidden; brown boxes, clear
   bottles and amber reagent bottles added near the vials as negatives;
3. **another lab entirely**: the open scene, never trained on, as `test_open`.

These are drawn in the same frames as 5.1, so they cost no frames: a
`pattern_train` frame has its own bench, its own room and its own camera.
`lab_test` (150 frames, held-out seeds) and `test_open` (100) measure it. Check
first, on 20 frames by eye: that swapping textures at run time renders, that a
moved instrument never lands on a vial, and that `bench_crop` still frames the
bench.

Every draw is recorded in the frame's `randomisation` (pattern seed, style,
count, spacing; which instruments moved where; which materials changed), as
the camera pose is today, so the page and the scoring can group by it.

### 5.3 Low cameras

`low_train` / `low_val` / `low_test` (done in code, not rendered): 15 to 30
degrees above the bench, 0.5 to 3.5 m, 600 / 100 / 100 frames, from new seeds.
Measured need: 0.885 to 0.939 recall and 11 to 14 false boxes a frame there.

### 5.4 The Phase 2 render and run

About 2,900 new frames (`pattern_*` 1,810, `low_*` 800, `lab_test` 150,
`test_open` 100; 160 of them the first measurement). At the measured 9,400
frames in 17 minutes on the 4090 pod: **about 6 minutes, under 0.20 USD**.
Training set: the 4,250 of Phase 1 plus 2,100, fine-tuned from the Phase 1
model: **about 1.5 hours, 1.50 USD** (estimate). Accepted on the same rules
plus: gains on `pattern_test` and `lab_test`, does not lose on anything Phase 1
won.

## 6. Timing on the Mac (proposed, five minutes of the teammate's time)

```bash
python scripts/export_and_time.py rail --format torch --device mps --band 512
python scripts/export_and_time.py rail --format coreml --band 512
python scripts/export_and_time.py rail --format torch --device mps --imgsz 1920
```

The first is what the viewer does today, the second is the faster path if the
first is not enough, the third is `vision_pick.py`'s whole frame. `rail`'s
architecture is the new model's, so this can be done before training. The
CoreML and MPS paths of the script have not been run anywhere yet. The
detector shares the GPU with the MuJoCo render, so time it with the viewer
running.

## 7. The review page: adding benches and labs to the map (proposed)

The page is built by `dataset_viales/fuentes/build_page2.py` from
`dataset_report.py`'s `data.json`: one row of 14 columns per frame, drawn as a
polar map (centre overhead, rim 30 degrees), a coverage grid of elevation by
bearing, histograms, thumbnails and samples.

1. `dataset_report.py`: read the new `randomisation` fields into new columns:
   bench style (scattered, cluster, rows, crowded, as built), pattern id,
   vials on the bench, tightest spacing, lab variant (appearance and
   arrangement ids), and the `low` family.
2. Polar map: extend the rim from 30 to 15 degrees; colour or filter the dots
   by bench style and by lab variant, next to today's camera family.
3. A second coverage grid: **bench style by camera family and distance band**,
   the counterpart of elevation by bearing, with the same "every cell holds at
   least N" check. A third, smaller: lab variant by camera family.
4. Two histograms: vials per frame (today it stops at 34; the patterns go to
   75) and tightest spacing.
5. Samples: a row per bench style and per lab variant, cropped and boxed as
   training sees them, so rows of touching flasks can be checked by eye.
6. Publish as version 3 of the same artifact. A version holds 255 files and the
   page has 218 (94 thumbnail sheets, 124 samples); 2,900 more frames are 29
   more sheets, so sheets go to 200 thumbnails each or the samples are thinned.

## 8. Order, and what waits for whom

| # | step | needs | time |
| --- | --- | --- | --- |
| 1 | Commit the branch's code | Martí's OK to commit | minutes |
| 2 | `select_frames.py`, checked against the local labels | nothing | an hour of work |
| 3 | Time `rail` on the Mac (section 6) | the teammate | 5 min |
| 4 | Phase 1 training and scoring | Martí's OK on the frames (the artifact), a pod | 1.5 h, about 1.50 USD |
| 5 | `pattern_test`: render and score `rail` and the new model | the pattern mode of `lay_out` | half a day of work, minutes of pod |
| 6 | Lab randomisation, checked on 20 frames | nothing | half a day to a day |
| 7 | Phase 2 render, page version 3, training | steps 5 and 6 | 2 h, about 2 USD |
| 8 | Wire the crop and the new backend into `labvision` and the viewer | a model accepted | an hour |

Steps 2, 3, 5 and 6 do not wait for each other.

## 9. Open points

- **What "lab dispositions" covers.** This plan reads it as both the bench
  patterns (5.1) and the room (5.2). If only one was meant, the other drops out
  without touching the rest.
- **Whether Phase 1 waits for Phase 2.** Proposed: no. Phase 1 is an hour and
  gives the demo a model tonight; Phase 2 fine-tunes from it.
- **The step to reality** is still the largest unknown and is outside this
  plan by decision: no real photograph has been scored.
