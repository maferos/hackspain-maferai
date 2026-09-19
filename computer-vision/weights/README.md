# Detector weights

Trained weights are **never committed** — they are megabytes of binary and they
change often. Drop the `.pt` files here and the code finds them.

## The current version: `yolo26n_full_1920_e25.pt`

**This is the detector to use on MuJoCo frames, from 20 September 2026.** It
replaces `yolo26n_rail_general.pt`, which should no longer be the default
anywhere.

| | |
| --- | --- |
| File | `yolo26n_full_1920_e25.pt` (5.8 MB) |
| Backend name | `full` |
| Model | YOLO26n, one class, `amber_bottle` |
| **Threshold** | **0.41**, its best-F1 point on validation |
| Input | the part of the frame the bench occupies, at the frame's own 1920 px width, which is how the viewer already runs the detector |
| Where to get it | team Drive, **General MAFER AI › hackathon › weights › yolo26n_full_1920_e25**, with its scores, hyperparameters and training curves beside it |
| Trained on | 5,844 MuJoCo renders of the rail scene: the wall camera, any angle at 1 to 3.5 m, close views under a metre, low cameras, benches in rows, clusters and crowds of up to 75 flasks, and a varied lab in seven frames of ten. 25 epochs from `yolo26n_rail_general.pt` |

Why it replaces the old one, on test frames neither model trained on (recall,
old to new, each at its own validation threshold):

| view | recall | false boxes a frame |
| --- | --- | --- |
| the robot's wall camera | 0.991 → 0.998 | 0.11 → 0.14 |
| the ten demo bench patterns, wall camera | 0.993 → 0.998 | 0.10 → 0.08 |
| the ten demo bench patterns, any angle | 0.909 → 0.999 | 1.39 → 0.04 |
| any angle, 1 to 3.5 m | 0.948 → 0.995 | 0.68 → 0.05 |
| close, under 1 m | 0.447 → 0.999 | 0.81 → 0.05 |
| straight down | 0.853 → 0.999 | 1.13 → 0.02 |
| low cameras, 15 to 30 degrees | 0.770 → 0.978 | 0.90 → 0.35 |
| another lab layout, any angle | 0.921 → 0.999 | 0.82 → 0.09 |

It is never worse at finding vials, and much better wherever the camera is not
the wall mount. From the wall mount it draws slightly more false boxes (0.14 a
frame against 0.11). All of this is MuJoCo: it has not been scored on Isaac
renders or on real photographs. The whole account, and how it was trained, is
in `docs/YOLO26_TRAINING.md`.

### Making each program use it

Copy the file into this folder, then:

| Program | What it loads if you do nothing | How to use the current version |
| --- | --- | --- |
| Anything that takes `--weights` (`propose_confirm.py`, `viewpoint_study.py`, …) | whatever you name | `--weights full`: the name brings the 0.41 threshold with it |
| `simulation/scripts/vision_pick.py` | the first of its `DETECTORS` on disk, still `yolo26n_rail_general.pt` at 0.10 | `--weights computer-vision/weights/yolo26n_full_1920_e25.pt --threshold 0.41` (a bare path would otherwise run at 0.10) |
| The viewer, `view/backend/server.py` | backend `rail` at 0.47 | `VIEW_DETECTOR=full VIEW_DETECTOR_CONF=0.41` in its environment |
| `harness/build_lookup_table.py` | backend `rail` | the committed `lookup_table.json` was made with the old detector: build it again with the new one before relying on it |

The programs' built-in defaults still name the old file, so that a checkout
without the new weights keeps working. Until those defaults are changed, use
the flags and variables above.

## Every file

Put the file in this folder under the name its backend expects:

| Backend | File | What it is |
| --- | --- | --- |
| `full` | `yolo26n_full_1920_e25.pt` | **The current version.** See above. |
| `rail`, `mujoco` | `yolo26n_rail_general.pt` | The previous detector: YOLO26n trained on the wall camera's renders alone. Superseded; keep it only to compare against or to fine-tune from. |
| `fixedcam` | `yolo26n_fixedcam.pt` | An earlier YOLO26n fine-tuned on crops of the gantry scene. Superseded. |

Anything else Ultralytics can load works too — pass its path to `--weights`
instead of a backend name.

## Using them

Every script that detects takes `--weights`, and it accepts either a backend
name from `labvision.detector.BACKENDS` or a path:

```bash
python scripts/propose_confirm.py --weights full        # this folder's yolo26n_full_1920_e25.pt, at 0.41
python scripts/propose_confirm.py --weights weights/something_else.pt
python scripts/propose_confirm.py                       # zero-shot YOLO-World
```

A backend also carries its own confidence threshold, measured at the best-F1
point on validation frames, so naming one picks the threshold too. A bare path
does not, so pass `--threshold` with it or take the 0.25 default.

## Adding a backend

One line in `BACKENDS` in `labvision/detector.py`:

```python
"full": Backend("yolo26n_full_1920_e25.pt", 0.41),
```

`weights` is looked up in this folder first, then the repository root, then the
working directory, then handed to Ultralytics to download if it is one of their
published names.
