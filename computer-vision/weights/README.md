# Detector weights

Trained weights are **never committed** — they are hundreds of megabytes and
they change often. Drop the `.pt` files here and the code finds them.

## Where a file goes

Put the file in this folder and give it the name the backend expects:

| Backend | File | What it is |
| --- | --- | --- |
| `mujoco` | `yolo_mujoco.pt` | Trained on MuJoCo renders of this scene. The one to use. |
| `fixedcam` | `yolo26n_fixedcam.pt` | YOLO26n fine-tuned on simulator-labelled crops of the fixed camera. |

Anything else Ultralytics can load works too — pass its path to `--weights`
instead of a backend name.

## Using them

Every script that detects takes `--weights`, and it accepts either a backend
name from `labvision.detector.BACKENDS` or a path:

```bash
python scripts/propose_confirm.py --weights mujoco      # this folder's yolo_mujoco.pt
python scripts/propose_confirm.py --weights weights/something_else.pt
python scripts/propose_confirm.py                       # zero-shot YOLO-World
```

A backend also carries its own confidence threshold, measured at the best-F1
point on validation frames, so naming one picks the threshold too. A bare path
does not, so pass `--threshold` with it or take the 0.25 default.

## Adding a backend

One line in `BACKENDS` in `labvision/detector.py`:

```python
"mujoco": Backend("yolo_mujoco.pt", 0.10),
```

`weights` is looked up in this folder first, then the repository root, then the
working directory, then handed to Ultralytics to download if it is one of their
published names.
