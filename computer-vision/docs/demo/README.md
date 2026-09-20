# The bench vial detector, for the demo

Everything to show about how the detector was trained, in the order it is told:
the data, the training, the results. The full account is
[`../YOLO26_TRAINING.md`](../YOLO26_TRAINING.md); the interactive page with all
10,300 images is https://claude.ai/artifact/9sFAnHGXH6hzXr366sKU12 (private).

**The model:** `yolo26n_full_1920_e100.pt`, YOLO26n, threshold 0.52, backend
`full`. How to use it: [`../../weights/README.md`](../../weights/README.md).
Everything here is MuJoCo; nothing has been scored on a real photograph.

## The story in five slides

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
```

Neither needs a GPU, the weights or the rendered frames. These do:
`scripts/demo_tables.py` rebuilds `frames.csv` and `test_vials.csv` from the
rendered sets and the boxes `viewpoint_study.py` cached; `scripts/demo_strips.py`
draws the three `examples_as_*.jpg` strips from `limits_sweep.py`'s frames and
the two weights; the first pose map is drawn by `scripts/pose_map.py` and the
bench frames by `scripts/demo_patterns_check.py` (both on the branch
`vision/orbit-dataset`); the example sheets come from the dataset report's
samples.
