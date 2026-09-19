# Synthetic barcode-detection dataset — v2

> **Correction (superseded by [v3](../dataset_v3/README.md)).** v2's intended
> geometric randomization (bottle spin) **did not actually apply**: raw USD
> `xformOp` edits between Replicator renders don't reach the render (Fabric
> caches transforms; only attribute edits like light intensity propagate). So
> v2 is effectively v1 with 500 frames of **lighting-only** variation — same
> bottle layout every frame. v3 fixes this by writing poses through Isaac's
> Fabric-aware `XFormPrim` API (verified: bottles move ~300 px between frames).
> Use v3 for geometric diversity; v2 remains valid extra lighting-augmented data.

Isaac Sim 4.5 RTX renders of the `minihannover_open` lab bench, labelled for
detection by product (EAN-13 barcode id).

- **500 images**, 1600×900, across 5 cameras (`general`, `room_aisle`,
  `room_desk`, `room_entrance`, `room_wash`).
- **133,400 bounding boxes**, **180 barcode categories** (COCO), + semantic masks.

## What varies per frame (vs v1)

| | v1 | v2 |
|---|----|----|
| Light intensity + colour | ✅ | ✅ |
| **Bottle spin** (barcode faces a new direction) | ✗ | ✅ each bottle, about its own vertical axis |
| **Bottle position jitter** (±2 cm) | ✗ | ✅ |
| **Camera pose jitter** (±3°, ±0.15 m) | ✗ | ✅ per camera |

The spin is the key add for barcode CV: see `spin_comparison.png` — the same
camera, two frames, with barcodes rotated to different orientations. Implemented
as a world-space transform `base·W` where `W` rotates each bottle part about the
shared bottle axis (so parts stay together and spin in place, no orbiting).

## Full dataset

The full 585 MB dataset (images + masks + `annotations/instances.json`) is on
Google Drive: **General MAFER AI › hackathon › lab_dataset_v2**. This folder keeps
the generator and a visual sample only.

## Reproduce

```bash
STATES=100 /isaac-sim/python.sh dataset_gen_v2.py   # -> /root/dataset_v2
/isaac-sim/python.sh build_coco.py /root/dataset_v2 /root/lab_dataset_v2
```

Scripts: [`dataset_gen_v2.py`](../../../scripts/dataset_gen_v2.py),
[`build_coco.py`](../../../scripts/build_coco.py). Supersedes
[`dataset_v1`](../dataset_v1/README.md).

## Next
Bottle layout still repeats (same positions ± jitter). A full reshuffle onto the
worktop (with collision-free placement), random occluders, and material/background
variation would be the next diversity step.
