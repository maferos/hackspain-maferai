# Isaac Sim RTX renders of the lab scene

Rendered on a RunPod GPU (RTX A40, Montreal) with NVIDIA Isaac Sim 4.5, 1920×1080.
Pipeline: MuJoCo scene → `scripts/export_usd.py` (MuJoCo native USD export) →
`scripts/render_usd.py` (Isaac + Replicator, interior lights ×40). See
[`../../runpod-isaac.md`](../../runpod-isaac.md).

- `open/`  — `models/minihannover_open_scene.xml` (shelf-free, centred desk; robot task)
- `full/`  — `models/minihannover_scene.xml` (full perfumery lab, labelled bottles)

Camera names match the authored cameras in each scene.
