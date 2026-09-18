# Amber bottles + white ribbed TE caps (generated 2026-09-18)

Procedural, Blender 5.0, no third-party licences. Regenerate: `blender -b -P generate_amber_bottles.py -- --out .`

- `amber_bottles_kit.blend` / `amber_bottles_kit.glb` — all sizes, one collection per size
- `glb/amber_bottle_XXXml.glb` — bottle (root, extras: capacity_ml, neck_mm, height_mm, diameter_mm, material, cap_z_mm) + cap as child, closed
- `glb/amber_cap_PPnn.glb` — cap alone (PP18/20/25/28)

Sizes: 10 ml Ø22×52 PP18 · 20 ml Ø28×66 PP18 · 30 ml Ø32×75 PP20 · 50 ml Ø38×89 PP25 · 60 ml Ø40×95 PP25 · 100 ml Ø47×113 PP28
Scaling: body k=(V/60)^(1/3); neck snapped to standard PP finish; cap derived from neck.
Conventions: metres, origin bottom-centre, glTF +Y up. Amber glass = Principled transmission + Volume Absorption (exports as KHR_materials_volume).
