# Detector benchmark: which pretrained model finds vessels in a frame

Question: where are the vessels in the fixed camera's image? The label does not matter, identity comes from
the collar tag (the team later moved to EAN-13 barcodes; see `README.md`). Measured on 18 and 19 September
2026 with pretrained models as downloaded, without training anything, on 5 real laboratory photographs with
11 hand-annotated flasks. Machine: 12-thread CPU, no GPU. The overlays for every run are written to
`results/bench/`, which is gitignored.

The five photographs (Wikimedia Commons downloads), the hand-made boxes and the scripts that ran the
benchmark are local tooling and are not in the repository; this document is the record.

## Decision

Two backends are ready in `labvision/detector.py`, selected by argument. They return `BBox` from
`labvision.scene`, so `scene.locate` consumes them as is:

| backend | model | what for | CPU at 960 px |
|---|---|---|---|
| `world` | YOLO-World large, everyday prompts | best quality: finds all 11 flasks, reliable from a 24 px side. Machine with GPU | 1.9 s/frame |
| `coco` | YOLO11 small, filtered COCO classes | no prompts, the most robust with small, stacked empty beakers. Laptop without GPU | 0.7 s/frame |

Inference resolution **960 px**. At 640 the 100 ml beaker is 35 px from 80 cm and gets lost.

Discarded: Grounding DINO and OWLv2 (9 to 13 s/frame on CPU; OWLv2 draws one box per shelf instead of
one per flask), FastSAM and YOLOE without prompts (a lot of background noise), YOLO-World medium (worse
than small and large, with no clear explanation), Roboflow models fine-tuned on other people's laboratories
(small dataset, no guarantee of transferring to renders).

## Main table (640 px unless stated)

Class-agnostic evaluation: any box with IoU overlap ≥ 0.4 against a reference flask counts.
Recall and precision at each model's best-F1 confidence threshold.

| model | prompts | ms/frame | AP | recall | precision | boxes in the cabinet (~60 vessels) |
|---|---|---|---|---|---|---|
| yolov8l-world | everyday | 1090 | 0.92 | 1.00 | 0.85 | 70 |
| yolov8s-world | everyday | 470 | 0.89 | 0.82 | 1.00 | 21 |
| yoloe-11m | laboratory | 1570 | 0.87 | 1.00 | 0.73 | 6 |
| yolov8l-world | laboratory | 1090 | 0.86 | 0.91 | 0.91 | 13 |
| owlv2-base | everyday | 9100 | 0.80 | 0.82 | 0.75 | 9 |
| yolov8s-world @960 | laboratory | 481 | 0.74 | 0.82 | 0.69 | 31 |
| yoloe-11s @960 | laboratory | 549 | 0.74 | 0.82 | 0.64 | 15 |
| yoloe-11s | everyday | 375 | 0.71 | 0.82 | 0.53 | 46 |
| yolov8s-world | laboratory | 470 | 0.71 | 0.64 | 1.00 | 10 |
| yolo11s-coco | (fixed) | 419 | 0.61 | 0.73 | 0.67 | 86 |
| yolo11s-coco @960 | (fixed) | 724 | 0.60 | 0.73 | 0.67 | 94 |
| grounding-dino-t | everyday | 13465 | 0.58 | 0.82 | 0.56 | 10 |
| yoloe-11s-pf (no prompts) | | 565 | 0.47 | 0.55 | 0.55 | 56 |
| fastsam-s | | 480 | 0.39 | 0.46 | 0.56 | 2 |

Latencies measured with the machine otherwise idle; they vary ±30 % under other loads.

## Prompts matter more than the model

"Laboratory" prompts: glass flask, erlenmeyer flask, beaker, glass bottle, vial, laboratory glassware.
"Everyday" prompts: cup, drinking glass, glass, bottle, jar, beaker, glass flask, vial.

Open-vocabulary models score each region against the text embedding of the prompt. "cup" and "glass" have
millions of examples in their training data; "beaker" a few dozen. An empty beaker scores 0.4 against "cup"
and 0.08 against "beaker": with a 0.1 threshold it only appears with the former. With the everyday prompts
YOLO-World large goes from 13 to 70 boxes in the cabinet and from 0.91 to 1.00 recall. Rule: short, everyday
nouns, with synonyms; class-agnostic NMS merges the duplicates. "Bin" classes such as hand, robot arm or
table can be added to absorb false positives and then be discarded.

YOLO11 COCO uses no prompts: its 80 classes are fixed. "cup" and "bottle" are among them, very well
trained, and that is why it is the best with small empty beakers. It fails with round-bottom flasks, which
look like none of its classes, and its list cannot be extended without retraining.

## Size and distance

Each annotated photo was shrunk to 7 scales inside a canvas of its own size, simulating the camera moving
further and further away. Fraction of flasks found by flask side in pixels at the network input, pooled
over the 640, 960 and 1280 resolutions:

| model | 12-24 px | 24-48 px | 48-96 px | > 96 px |
|---|---|---|---|---|
| yolov8l-world (everyday) | 12 % | 62 % | 89 % | 87 % |
| yoloe-11s (everyday) | 34 % | 44 % | 82 % | 90 % |
| yolo11s-coco | 62 % | 54 % | 85 % | 80 % |
| yolov8s-world (everyday) | 16 % | 42 % | 74 % | 68 % |

Rule: **reliable from a 48 px side at the network input**; between 24 and 48 it is a coin toss; below
24 it is lost, except COCO with tiny beakers. YOLO-World large at 960 is the only one reliable from 24 px.

Apparent size in the design's fixed camera (1280×720, 60° horizontal field of view) at 80 cm from the table:

| flask | net at 640 | net at 960 | net at 1280 |
|---|---|---|---|
| vial 2 cm | 14 ✗ | 21 ✗ | 28 ✗ |
| test tube 1.5 cm | 10 ✗ | 16 ✗ | 21 ✗ |
| beaker 100 ml, 5 cm | 35 ✗ | 52 ✓ | 69 ✓ |
| beaker 250 ml, 7 cm | 48 borderline | 73 ✓ | 97 ✓ |
| bottle 500 ml, 7.5 cm | 52 ✓ | 78 ✓ | 104 ✓ |
| erlenmeyer 250 ml, 8.5 cm | 59 ✓ | 88 ✓ | 118 ✓ |

Consequences: at 80 cm infer at 960; at 120 cm 1280 would be needed; vials and test tubes do not show up
from the fixed camera at any reasonable height, they belong to the wrist camera or to a rack with a tag.

**Warning for the team's scene.** `labvision/scene.py` sets the camera as a GoPro in Linear mode at 1080p
(f = 927 px, 60° vertical field of view), on the wall 3.23 m from the table. Size of the kit's HDPE bottles
(`scene.VESSELS`) in the frame, side = square root of width times height:

| bottle | 1080p | 4K |
|---|---|---|
| 100 ml | 13×28 px, side 19 | side 38 |
| 250 ml | 17×38, side 25 | side 51 |
| 500 ml | 21×47, side 32 | side 63 |
| 1 L | 25×62, side 40 | side 79 |
| 2 L | 33×70, side 48 | side 97 |

At 1080p only the 2 L reaches the 48 threshold and the 100 ml is lost. And that is inferring at the native
1920 resolution: if the network works at 960, everything is halved and the whole kit disappears. That is why
the detector defaults to the frame size, not 960. Fixes: record or render at 4K, with which everything from
250 ml up is reliable, or use the Narrow lens at 1080p, or move the camera closer. `detector.apparent_size_px`
computes the size for any camera and distance before rendering anything.

With many small empty beakers (cabinet shrunk to half, 960 px): COCO 89 boxes, YOLOE small 68,
YOLO-World large 33, YOLO-World small 7.

## Limitations

Real photos from the side, not top-down renders. 11 references: each flask moves recall by 9 %. Minimum
overlap 0.4 because the boxes were annotated by eye. What carries over to Isaac is the size in pixels:
measure how many pixels a beaker takes up in a render and you know which band you are in.

## When Isaac frames arrive

The team's renders come from `../simulation/scripts/render_dataset.py` (MuJoCo, `../simulation/out/<scene>/`)
or from AutoBio on RunPod (`../simulation/runpod-render.md`). Steps:

1. Put the frames in a folder, e.g. `data/isaac/rgb/` (PNG or JPG). If there are labels, in
   `data/isaac/labels/` as `<frame>.txt` in YOLO format (class cx cy w h, normalised) or `<frame>.json`
   with `{"boxes": [[x1,y1,x2,y2], ...]}`.
2. See what each backend finds, with overlays in `results/detect/` (from `computer-vision/`):
   ```
   python -m labvision.detector ../data/isaac/rgb --backend both --barcodes
   ```
   The summary line prints the median side of the boxes in pixels: if it is below 48, the problem is the
   camera or the resolution, not the model.
3. With labels, measure properly and regenerate the report:
   ```
   python scripts/isaac_to_gt.py data/isaac/rgb --labels data/isaac/labels --out data/isaac/gt.json
   python scripts/bench_detectors.py --images data/isaac/rgb --gt data/isaac/gt.json --models yolov8l-world,yolo11s-coco --imgsz 960 --out results/bench_isaac
   python scripts/bench_report.py --bench results/bench_isaac --out results/bench_isaac/report --scale none
   ```
4. If a render looks different from the real photos and both backends fail, it is time for fine-tuning
   with renderer-labelled frames, not for trying more models.

## Size experiment at 1080p on renders (19 September)

`scripts/render_bottles.py` builds in MuJoCo the scene from `scene.py` with the 6 × 1.5 m minihannover
table and the bottle kit at random positions, and produces exact boxes by segmentation.
`scripts/size_experiment.py` runs the detector at native resolution and classifies the size of each box by
geometry: it fits the five classes with `locate(anchor="fit")` and the one with the lowest residual wins.

**Finding for Nacho:** `Vessel.silhouette_height_m` adds the cap height to the body, but in the kit the cap
wraps around the neck and only adds 1 mm (the closed 1 L measures 217 mm, not 242). With its height the
geometry classified everything one size down, even with exact boxes. With the kit's height it gets it right.
The script carries both as `--cap-model scene|kit`. What remains after that is the shoulder: the cylinder
model puts the top edge 2 to 6 px too high, and that is what the 2 L still struggles with.

Short table, everything between 2.9 and 3.5 m, 177 bottles, YOLO-World large / COCO:

| bottle | found | correct size among those found | position error |
|---|---|---|---|
| 100 ml | 95 % / 80 % | 100 % / 100 % | 5 mm |
| 250 ml | 96 % / 72 % | 100 % / 100 % | 6 mm |
| 500 ml | 100 % / 78 % | 100 % / 100 % | 7 mm |
| 1 L | 100 % / 89 % | 100 % / 97 % | 9 mm |
| 2 L | 100 % / 87 % | 97 % / 82 % | 12 mm |

6 m table, from 2.9 to 4.4 m, 347 bottles, by distance to the camera:

| distance | n | found | correct size among those found |
|---|---|---|---|
| under 3.0 m | 21 | 91 % / 48 % | 100 % / 80 % |
| 3.0 to 3.5 m | 98 | 87 % / 41 % | 88 % / 95 % |
| 3.5 to 4.0 m | 154 | 58 % / 47 % | 92 % / 92 % |
| over 4.0 m | 74 | 23 % / 49 % | 82 % / 81 % |

Conclusion: at 1080p the size can be told apart whenever the bottle is found; what fails at a distance is
finding it. Past 3.5 m YOLO-World loses the small ones and past 4 m it loses three out of four. The fixes
are those of the previous section: 4K, Narrow lens or a closer camera.

Scripts: `scripts/bench_detectors.py` (table and overlays), `scripts/bench_scale.py` (size and distance),
`scripts/bench_report.py` (HTML page) and `scripts/isaac_to_gt.py` (label converter) are the local tooling
mentioned at the top, not in the repository. `scripts/render_bottles.py` and `scripts/size_experiment.py`
(the size experiment) are.
