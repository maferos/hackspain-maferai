# Mafer arm branding

`mafer-logo.svg` is the original supplied brand artwork, including the symbol
and the outlined “mafer” wordmark. `mafer-label.png` is its white-backed label
texture, cropped with padding to `viewBox="230 180 1540 350"` and rasterized
at 1540 × 350 with `rsvg-convert --background-color white`.

`scripts/generate_rail_scene.py` adds a 280 mm wide curved label to both sides
of the UR10e upper arm. The labels move with the link and have no collisions
or added mass. Regenerate the arm with `build_arm()` or regenerate the scene
normally; the branding is preserved. Existing recordings must be rendered
again to show the updated arm.
