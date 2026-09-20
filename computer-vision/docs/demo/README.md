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
| 4 | The old detector found 45 % of the vials from under a metre. The new one finds 99.8 %, and loses nothing from the robot's own camera | `3_results/all_tests_three_models.png`, `3_results/limits_before_and_after.png` |
| 5 | On the ten benches this demo shows, none of them trained on: 430 of 435 flasks, no false box | `3_results/demo_benches_as_the_viewer_shows_them/p10.jpg` |

## 1_dataset: what the model learns from

| file | what it shows |
| --- | --- |
| `pose_map_training_set.png` | **The angle map.** Where the camera stood in each of the 5,844 training frames. The bench is seen from above: a dot's angle is the side the camera looks from, its distance from the centre is how steeply it looks down (centre = straight down, rim = almost level with the bench), its shade is how far it stands. The orange patch is the robot's wall camera. Right: frames in every elevation by distance cell; the empty cells are the ceiling |
| `dataset_composition.png` | The 10,300 frames by camera, by bench layout, and how many have the lab varied |
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
| `ultralytics_<run>/` | Ultralytics' own plots for backup slides: `results.png`, precision-recall and F1 curves, the confusion matrix, the label statistics, and two training mosaics as the model saw them |

## 3_results: what it can do

| file | what it shows |
| --- | --- |
| `all_tests_three_models.png` | Recall and false boxes a frame on twelve tests no model trained on, for the previous detector and both runs. The headline is `close`: 0.45 to 1.00 |
| `limits_before_and_after.png` | Recall as the camera nears (0.31 to 1.00 at 25 cm), tilts (0.89 to 0.99 at 10 degrees) and as the light goes. The dark is the one limit that did not move: no dark frame was trained on, by decision |
| `demo_benches_by_seed.png` | The ten catalogued benches (p01 to p10), seed by seed, from any angle |
| `demo_benches_as_the_viewer_shows_them/` | Each of the ten benches in the viewer's own frame: the `general` camera at 1920 x 1080, the band the detector is given left bright, found flasks in green, missed ones in red. 430 of 435; the five missed each stand behind a larger flask with only the cap showing |
| `predictions_on_validation_frames/` | The model's boxes on validation frames (`*_pred.jpg`) next to the truth (`*_truth.jpg`) |

One colour means one detector on every figure: orange the previous one, green
the 25-epoch run, blue the 100-epoch run.

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
sweeps, the ten demo benches and the dataset's counts.

```bash
python computer-vision/scripts/demo_figures.py
```

redraws `dataset_composition.png`, the three curve figures and the three
results figures. The pose map is drawn by `scripts/pose_map.py`, the bench
frames by `scripts/demo_patterns_check.py` (on the branch
`vision/orbit-dataset`), and the example sheets from the dataset report's
samples; those need the rendered frames or the weights.
