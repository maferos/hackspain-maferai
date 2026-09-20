# The vision system, for the demo

Everything to show about the vision system, one folder a chapter. Figures only,
each with its message in the title and its conditions in the note under it; the
record behind every number is the document named beside its chapter.

| folder | chapter | the record |
| --- | --- | --- |
| `0_overview/` | The pipeline on one slide | this page |
| `4_detector_choice/` | Why a detector was trained: pretrained models, prompts, the size floor | [`../BENCHMARK.md`](../BENCHMARK.md), [`../FIXED_CAMERA_BENCHMARK.md`](../FIXED_CAMERA_BENCHMARK.md) |
| `1_dataset/`, `2_training/`, `3_results/` | The trained detector: its data, its training, what it can do | [`../YOLO26_TRAINING.md`](../YOLO26_TRAINING.md) |
| `5_identity/` | Naming a bottle: barcode against ArUco ring, and the silent misread | [`../../README.md`](../../README.md), [`../READ_CONFIDENCE.md`](../READ_CONFIDENCE.md) |
| `6_position/` | From a box to a point on the bench, and the chain end to end | [`../../README.md`](../../README.md) |

The folder numbers are the order the work was filed in, not the order it is
told: tell it 0, 4, 1, 2, 3, 5, 6. The interactive page with all 10,300
training images is https://claude.ai/artifact/9sFAnHGXH6hzXr366sKU12 (private).

**The model:** `yolo26n_full_1920_e100.pt`, YOLO26n, threshold 0.52, backend
`full`. How to use it: [`../../weights/README.md`](../../weights/README.md).
Everything here is MuJoCo, except the pretrained-detector benchmark, which is
five real laboratory photographs; nothing of ours has been scored on a real
photograph.

## The whole system in eight slides

| # | say | show |
| --- | --- | --- |
| 1 | One frame from a wall camera becomes a bench where every bottle has a name and a position | `0_overview/pipeline_on_one_slide.png` |
| 2 | We started with what needs no training. Fourteen pretrained detectors: the words you prompt with matter more than the model, and all of them need about 48 px of bottle. Our camera gives 19 to 48 | `4_detector_choice/pretrained_accuracy_against_speed.png`, `4_detector_choice/size_floor.png` |
| 3 | One epoch of fine-tuning on a laptop CPU, on frames the simulator labels for free, already matched the best pretrained model and beat it on the smallest bottles. So we trained | `4_detector_choice/fine_tuned_against_pretrained.png` |
| 4 | The data: 10,300 rendered frames from every side of the bench | `1_dataset/pose_map_training_set.png`, `1_dataset/examples_by_bench_layout.jpg` |
| 5 | The result: from 3,477 vials missed to 760, from 953 false boxes to 48, and it sees from 25 cm what the old one could not | `3_results/scoreboard_missed_and_false.png`, `3_results/examples_as_the_camera_nears.jpg` |
| 6 | Naming the bottle: a barcode on a 10 ml flask reads from 15 cm, closer than the lens focuses. A ring of ArUco markers reads 38 of 40 bottles from 30 cm, none misread | `5_identity/ean13_against_aruco.png`, `5_identity/wrist_scan_forty_bottles.png` |
| 7 | Placing it: one calibrated camera puts a bottle within 7 to 10 mm, the wrist camera refines that to a tenth of a millimetre | `6_position/end_to_end.png`, `6_position/scan_bench_p05_truth_proposal_refinement.png` |
| 8 | What it still cannot do: a room under 15 % light, a flask hidden behind a larger one, and no real photograph yet | `3_results/recall_by_darkness.png` |

## The trained detector alone, in five slides

| # | say | show |
| --- | --- | --- |
| 1 | We render the training images ourselves, with exact labels: 10,300 frames, 216,876 vials, from every side of the bench | `1_dataset/pose_map_training_set.png` |
| 2 | Not one bench in one room: rows, clusters and crowds of up to 75 flasks, and a lab whose colours, lights, instruments and furniture change | `1_dataset/examples_by_bench_layout.jpg`, `1_dataset/examples_lab_as_it_is_and_varied.jpg` |
| 3 | Training: losses fall, validation rises, nothing overfits | `2_training/curves_100_epochs.png` |
| 4 | The old detector only knew vials the size its one camera showed them: from under a metre it found 45 %. The new one finds 99.8 %, and loses nothing from the robot's own camera. Over all tests: 3,477 vials missed before, 760 after; 953 false boxes before, 48 after | `3_results/examples_as_the_camera_nears.jpg`, `3_results/recall_by_vial_size.png`, `3_results/scoreboard_missed_and_false.png` |
| 5 | On the ten benches this demo shows, none of them trained on: 430 of 435 flasks, no false box | `3_results/demo_benches_as_the_viewer_shows_them/p10.jpg` |

## 1_dataset: what the model learns from

| file | what it shows |
| --- | --- |
| `pose_map_training_set.png` | **The angle map.** Where the camera stood in each of the 5,844 training frames. The bench is seen from above: a dot's angle is the side the camera looks from, its distance from the centre is how steeply it looks down (centre = straight down, rim = almost level with the bench), its shade is how far it stands. The orange patch is the robot's wall camera. Right: frames in every elevation by distance cell; the empty cells are the ceiling |
| `pose_maps_by_camera.png` | The same map for all 10,300 frames, one a camera: the wall camera is a single patch, the other three fill the dome |
| `training_frames_by_camera_pose.png` | The training frames by elevation, distance and bearing, stacked by camera: the wall camera is one spike, the rest is what the previous detector never saw |
| `vial_size_by_camera.png` | How tall a vial is in the image, a row a camera. **The point of the whole dataset:** the wall camera shows vials of 12 to 40 px and nothing else; the close camera goes to 260 px |
| `dataset_composition.png` | The 10,300 frames by camera, by bench layout, and how many have the lab varied |
| `sets_train_validation_test.png` | The twenty rendered sets by use: training, validation, and the twelve tests |
| `benches_vials_per_frame_and_positions.png` | Vials a frame by bench layout (from 1 to 80), and a heat map of where they stand on the worktop |
| `light_levels_trained_and_tested.png` | **Darkness values:** the room light of the training frames (55 to 145 %) against the two dim tests (8 to 50 %) |
| `examples_wall_camera.jpg` | The robot's camera: the bench band the detector is given, with its labels |
| `examples_by_camera.jpg` | The other three cameras: any angle, close, low |
| `examples_by_bench_layout.jpg` | Scattered, rows, crowded, several clusters |
| `examples_lab_as_it_is_and_varied.jpg` | The same room as it is, and varied |
| `examples_full_size/` | Twelve training images at full size, cropped to the bench and boxed exactly as the model sees them |

Green boxes are the labels, taken from the simulator's segmentation render, not
drawn by hand. A vial is labelled when at least 30 % of it shows.

## 2_training: how it was trained

YOLO26n, fine-tuned from the previous detector, on the bench crop at 1920 px
(the input the viewer runs), 5,844 training and 750 validation frames, on one
RTX 4090. The same training was run twice: 25 epochs (53 minutes) and 100
epochs (4 h 10 min). Every hyperparameter: `numbers/args_*.yaml`.

| file | what it shows |
| --- | --- |
| `curves_100_epochs.png` | The run that is used: box and class loss, training against validation, and recall, precision, AP50 and AP50-95 on validation, with the epoch that is kept |
| `curves_25_epochs.png` | The same for the 25-epoch run |
| `curves_25_vs_100_epochs.png` | The two runs on the same axes: what 75 more epochs bought (AP50-95 0.899 to 0.907, recall 0.985 to 0.988) |
| `validation_scores_up_close.png` | The 100-epoch run's four validation scores, each on its own scale: still climbing after epoch 25, flat after 85 |
| `learning_rate_and_time.png` | Learning rate of both runs, GPU time, and validation AP50-95 against hours spent: why the 25-epoch run is not the first quarter of the long one |
| `ultralytics_<run>/` | Ultralytics' own plots for backup slides: `results.png`, precision-recall and F1 curves, the confusion matrix, the label statistics, and two training mosaics as the model saw them |

## 3_results: what it can do

| file | what it shows |
| --- | --- |
| `all_tests_three_models.png` | Recall and false boxes a frame on twelve tests no model trained on, for the previous detector and both runs. The headline is `close`: 0.45 to 1.00 |
| `limits_before_and_after.png` | Recall as the camera nears (0.31 to 1.00 at 25 cm), tilts (0.89 to 0.99 at 10 degrees) and as the light goes. The dark is the one limit that did not move: no dark frame was trained on, by decision |
| `scoreboard_missed_and_false.png` | **The one-slide summary.** All 37,261 test vials pooled: vials missed 3,477, 740, 760; false boxes 953, 164, 48 |
| `recall_by_vial_size.png` | **Why the previous detector failed.** Recall by vial height in pixels: it holds between 12 and 64 px, the sizes the wall camera shows, and falls to zero past 96 px. The retrained one is flat at 1.00 |
| `recall_by_elevation_and_distance.png` | Recall of the three detectors by elevation band and by distance band, moving-camera tests |
| `recall_by_pose_cell_before_and_after.png` | The angle grid, scored: recall in every elevation by distance cell, before (0.11 straight down at under 60 cm) and after (0.96 to 1.00 everywhere) |
| `missed_vials_on_the_pose_map.png` | The angle map, scored: every bright test frame where its camera stood, darker and larger the more vials were missed. Every vial found in 782 of 1,394 frames before, 1,322 after |
| `recall_by_darkness.png` | **Darkness.** Left, the two dim tests binned by the light each frame was rendered at; right, the same 12 benches as the light goes, at both thresholds. Holds to 15 %, gone under 10 %, for every detector |
| `examples_as_the_light_goes.jpg` | One bench at 100, 30, 15, 10 and 6 % light, both detectors: found vials green, missed red |
| `examples_as_the_camera_nears.jpg` | One bench from 3.5 m to 25 cm, both detectors. At 25 cm: 0 of 5 before, 5 of 5 after. The best single picture of the improvement |
| `examples_as_the_camera_tilts.jpg` | One bench from straight down to 10 degrees above the worktop, both detectors |
| `recall_by_occlusion_crowding_position.png` | What makes a vial hard: how much of it shows, how many vials share the frame, how far from the centre it is. What is left after retraining is occlusion |
| `recall_by_bench_layout_and_lab.png` | Recall on each bench layout, and in the lab as it is against varied. None is left behind |
| `threshold_sensitivity.png` | Recall and false boxes a frame as the confidence threshold moves, with each detector's operating point: the retrained curves are flat round theirs |
| `demo_benches_by_seed.png` | The ten catalogued benches (p01 to p10), seed by seed, from any angle |
| `demo_benches_as_the_viewer_shows_them/` | Each of the ten benches in the viewer's own frame: the `general` camera at 1920 x 1080, the band the detector is given left bright, found flasks in green, missed ones in red. 430 of 435; the five missed each stand behind a larger flask with only the cap showing |
| `predictions_on_validation_frames/` | The model's boxes on validation frames (`*_pred.jpg`) next to the truth (`*_truth.jpg`) |

One colour means one detector on every results and training figure: orange the
previous one, green the 25-epoch run, blue the 100-epoch run. On the dataset
figures the same four colours name the cameras instead: orange the wall camera
(the one the previous detector was trained on), blue any angle, yellow low,
green close.

## 0_overview

| file | what it shows |
| --- | --- |
| `pipeline_on_one_slide.png` | The six stages, wall camera to bench memory, each with the number that backs it |

## 4_detector_choice: why a detector was trained

| file | what it shows |
| --- | --- |
| `pretrained_accuracy_against_speed.png` | Fourteen pretrained detectors on five real lab photographs: average precision against seconds a frame on a CPU. YOLO-World L with everyday words is top left; Grounding DINO and OWLv2 cost 9 to 13 s |
| `prompts_matter.png` | The same YOLO-World L with two vocabularies: recall 0.91 to 1.00 on real photographs, AP50 0.58 to 0.85 on our renders |
| `size_floor.png` | **The reason for everything after.** Recall of pretrained detectors by bottle side in pixels (reliable from 48 px), and the side of the kit's bottles from the wall camera: 19 to 48 px at 1080p |
| `found_by_distance.png` | Rendered bottles found by distance to the wall camera: past 4 m YOLO-World finds 23 % |
| `fine_tuned_against_pretrained.png` | YOLO26n fine-tuned for one epoch on a CPU against YOLO-World L and YOLO26s COCO, on the robot's scene, a scene never seen and a degraded camera: AP50 with 95 % intervals, recall, false boxes |
| `recall_by_bottle_and_size.png` | The same three models by bottle of the kit and by apparent size: training pays on the smallest bottles |
| `worktop_filter.png` | False boxes a frame before and after keeping only what stands on the bench plane: 65 to 3.9 and 17.5 to 1.8, no bottle lost |
| `examples_three_models_same_frames.jpg` | The three models' boxes on the same test frames |

## 5_identity: naming the bottle

| file | what it shows |
| --- | --- |
| `ean13_against_aruco.png` | Module size, reading distance and tolerated turn of an EAN-13 label against one ArUco marker, for the ten vessels: ten times the module, 4 to 12 times the reach, but lost 10 to 20 degrees off square, which is why the label became a ring of eight |
| `wrist_scan_forty_bottles.png` | The same forty bottles read by the wrist camera with each label: read from 0.30 m (where a GoPro focuses), had to come closer, not read. Ring 38 / 2 / 0, barcode from the aisle 12 / 25 / 3 |
| `marker_separation_and_silent_misreads.png` | The risk that remains: marker ids left at each minimum distance against a 200-sample catalogue, and what the reader reports with 0 to 3 cells flipped at two correction settings. Proposed work, not implemented: `../READ_CONFIDENCE.md` |

## 6_position: from a box to a point on the bench

| file | what it shows |
| --- | --- |
| `which_pixel_of_the_box.png` | Mean position error of four ways to turn a box into a bench point, by bottle: from 23 to 59 mm with the bottom of the box as is, to 0 fitting the known silhouette |
| `millimetres_per_pixel.png` | Bench covered by one pixel at 1080p, 4K and 5.3K, and position error against box noise: 5.5 mm a pixel at the bench centre |
| `end_to_end.png` | The whole chain on 12 random benches: 77 bottles, 74 proposed, 74 named, 0 wrong; and position error from the wall camera alone (10 mm median) and after the wrist (0.1 mm) |
| `radius_bias.png` | Why the wall camera's error is bias and not noise: each flask class is off by the radius assumed before it is named |
| `scan_bench_p05_*.png` | The catalogue bench p05 scanned: truth, proposal and refinement on the bench (offsets drawn 20x), per-bottle residuals, the errors at true scale on each flask's footprint, and the anatomy of one proposal |

On these chapters' figures the colours are: orange ours (the trained detector),
violet YOLO-World or the EAN-13 label, teal the COCO model or ArUco.

## If someone asks

- **Is it tested on images it trained on?** No frame seed is shared between
  training, validation and test, and the ten demo benches were kept out of
  training altogether.
- **Why not a bigger model?** The nano already found 99 % from the robot's
  camera; what it lacked was data from other views, not capacity.
- **Does it work on a real camera?** Not measured. Every number here is MuJoCo.
- **What does it still miss?** A flask hidden behind a larger one (the wrist
  camera reads those), a room with under 15 % of its light, and low cameras a
  little (0.975).

## Redrawing the figures

`numbers/` holds what every figure is drawn from: the two runs' per-epoch
logs and hyperparameters, the twelve tests of the three detectors, the limits
sweeps, the ten demo benches, the dataset's counts, one row for every rendered
frame (`frames.csv`: camera pose, vials, bench layout, lab, light) and one row
for every vial a detector had to find (`test_vials.csv`: its size, how much of
it shows, the pose and light of its frame, and the score each detector found it
at).

```bash
python computer-vision/scripts/demo_figures.py          # the headline figures
python computer-vision/scripts/demo_figures_detail.py   # everything per frame or per vial
python computer-vision/scripts/demo_figures_pipeline.py # chapters 0, 4, 5 and 6
```

None needs a GPU, the weights or the rendered frames. `numbers/vision_pipeline.json`
holds the tables of chapters 0, 4, 5 and 6, copied from the documents it names. These do:
`scripts/demo_tables.py` rebuilds `frames.csv` and `test_vials.csv` from the
rendered sets and the boxes `viewpoint_study.py` cached; `scripts/demo_strips.py`
draws the three `examples_as_*.jpg` strips from `limits_sweep.py`'s frames and
the two weights; the first pose map is drawn by `scripts/pose_map.py` and the
bench frames by `scripts/demo_patterns_check.py` (both on the branch
`vision/orbit-dataset`); the example sheets come from the dataset report's
samples.
