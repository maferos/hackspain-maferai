# Detector weights

Trained weights are **never committed** — they are hundreds of megabytes and
they change often. Drop the `.pt` files here and the code finds them.

## Where a file goes

Put the file in this folder and give it the name the backend expects:

| Backend | File | What it is |
| --- | --- | --- |
| `rail` | `yolo26n_rail_general.pt` | YOLO26n trained on the rail scene's own general-camera renders. The one to use. |
| `fixedcam` | `yolo26n_fixedcam.pt` | YOLO26n fine-tuned on simulator-labelled crops of the fixed camera. |

Anything else Ultralytics can load works too — pass its path to `--weights`
instead of a backend name.

## Using them

Every script that detects takes `--weights`, and it accepts either a backend
name from `labvision.detector.BACKENDS` or a path:

```bash
python scripts/propose_confirm.py --weights rail        # this folder's yolo26n_rail_general.pt
python scripts/propose_confirm.py --weights weights/something_else.pt
python scripts/propose_confirm.py                       # zero-shot YOLO-World
```

A backend also carries its own confidence threshold, measured at the best-F1
point on validation frames, so naming one picks the threshold too. A bare path
does not, so pass `--threshold` with it or take the 0.25 default.

## Adding a backend

One line in `BACKENDS` in `labvision/detector.py`:

```python
"rail": Backend("yolo26n_rail_general.pt", 0.10),
```

`weights` is looked up in this folder first, then the repository root, then the
working directory, then handed to Ultralytics to download if it is one of their
published names.
