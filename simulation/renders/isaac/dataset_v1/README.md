# Synthetic barcode-detection dataset — v1

Isaac Sim 4.5 RTX renders of the `minihannover_open` perfumery lab bench, labelled
for **object detection by product** (EAN-13 barcode id).

- **300 images**, 1600×900, across **5 camera viewpoints** (`general`, `room_aisle`,
  `room_desk`, `room_entrance`, `room_wash`).
- **80,040 bounding boxes**, **180 barcode categories** (COCO format).
- Semantic-segmentation masks per image.
- Domain randomization: interior light **intensity + colour tint** per frame.

Each bottle mesh is tagged with its barcode id as a Semantics class; since ids are
unique per bottle, a per-class tight 2D box is a per-bottle box labelled by product.

## Where the full dataset lives

The full 356 MB dataset (all images, masks, and `annotations/instances.json`) is on
Google Drive: **General MAFER AI › hackathon › lab_dataset_v1**. This folder only
keeps the reproduction scripts and a visual sample (git can't hold the images/COCO).

## Format (COCO)

```
lab_dataset_v1/
  images/<cam>/rgb_NNNN.png
  masks/<cam>/semantic_NNNN.png
  annotations/instances.json   # images + annotations + categories (name == barcode id)
```

## Reproduce

```bash
# on a RunPod Isaac Sim 4.5 pod (see ../../../runpod-isaac.md)
STATES=60 /isaac-sim/python.sh dataset_gen.py      # tag + render -> /root/dataset
/isaac-sim/python.sh build_coco.py /root/dataset /root/lab_dataset_v1
```

Scripts: [`dataset_gen.py`](../../../scripts/dataset_gen.py),
[`build_coco.py`](../../../scripts/build_coco.py).

## Known limitations / v2

- DR is photometric only (light). Geometric diversity (camera-pose jitter,
  per-bottle spin so barcodes face different ways) is the next step — bottle
  positions are identical across frames in v1.
- `room_overview` (camera above the ceiling) was dropped: it sees no bottles.
- Far-field boxes overlap heavily in dense views (expected).
