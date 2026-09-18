# uv_vis_nir

UV-Vis-NIR spectrophotometer, converted from the vendor download `../uv-vs-nr/3d-model.dae.zip`
by [`tools/convert_dae.py`](../../tools/convert_dae.py):

```bash
unzip -o assets/uv-vs-nr/3d-model.dae.zip -d /tmp/uv
python tools/convert_dae.py /tmp/uv/3d-model.dae --name uv_vis_nir --out assets/uv_vis_nir \
    --mass 80 --double-sided
```

The DAE declares inches, which gives 1.00 x 0.65 m and a 0.30 m body; the 0.646 m total
height is the sample-compartment lid, modelled open. The export is single-sided and
MuJoCo culls back faces, hence `--double-sided`. Origin on the floor, centred in X/Y,
+Z up, front (display, sample compartment) facing -Y. 80 kg box collider.
