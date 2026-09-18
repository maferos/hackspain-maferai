# gc_ms

GC-MS (gas chromatograph with autosampler and mass-selective detector), converted from the
vendor download `../gc-ms/3d-model.3ds.zip` by [`tools/convert_3ds.py`](../../tools/convert_3ds.py):

```bash
unzip -o assets/gc-ms/3d-model.3ds.zip -d /tmp/gcms
python tools/convert_3ds.py /tmp/gcms/3d-model.3ds --name gc_ms --scale 3e-5 --out assets/gc_ms
```

**The scale is an assumption.** The file has no units (extent 31 809 x 17 991 x 30 669).
3e-5 m/unit gives 0.954 x 0.540 x 0.920 m, which matches a GC + MSD bench system
(about 0.95 m wide and 0.54 m deep; the autosampler tower sets the height). Replace it if
you know the exact instrument.

Origin on the floor, centred in X/Y, +Z up, front (autosampler, oven, MSD panel) facing -Y.
Visual meshes don't collide; one box stands in. 65 meshes, 368 k faces.
