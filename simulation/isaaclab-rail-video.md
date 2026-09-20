# Rail videos with Isaac Lab

The two outputs are `rail_global.mp4` and `rail_robot.mp4`, both 1920×1080
at 30 fps. They share the same animation time for every frame. The robot view
uses the actual `arm_eih` camera from the rail scene.

The source MJCF and its existing rail trajectory are baked to an animated USD.
Isaac Lab launches Isaac Sim's RTX renderer to produce the final images. This
is animation playback, not a new PhysX simulation or a trained robot policy.
The default sweep lasts about 20 seconds; `visit` and `label` are also available.

## Export the current scene

Use a separate Python environment with `mujoco>=3.13,<4`, `usd-core`, `numpy`
and `pillow`. Do not install `usd-core` into Isaac Sim's environment: it ships
its own USD libraries.

```sh
python simulation/scripts/export_rail_animation.py --out out/rail-export --mode sweep
```

The exporter preserves camera poses and vertical field of view, and records
the frame count, frame rate and USD path in `animation.json`. It reads the
current rail XML and assets without regenerating them.

## Render with Isaac Lab 3.0 Early Access

Use the `v3.0.0-EA` checkout with its `isaacsim` extra (Isaac Sim 6.1 and
Python 3.12). From that checkout:

```sh
uv sync --extra isaacsim
OMNI_KIT_ACCEPT_EULA=YES uv run --extra isaacsim python /path/to/simulation/scripts/render_rail_isaaclab.py \
  --export /path/to/out/rail-export --out /path/to/out/rail-videos \
  --headless --enable_cameras
```

FFmpeg must be installed at `/usr/bin/ffmpeg`. For a short preview add
`--limit 2 --start-frame 250` and use a separate output directory. `--light-multiplier` adjusts
the imported room lights and `--subframes` controls RTX accumulation.

DLSS antialiasing is enabled explicitly: Replicator defaults to FXAA, which
produces noisy real-time path-traced images in this configuration. The script
drives Kit updates directly with a paused timeline to keep both cameras in sync.

Verified on NVIDIA L4 with driver 595.91.07, Isaac Lab `v3.0.0-EA` and
Isaac Sim 6.1. No driver downgrade is needed for this configuration.

The renderer saves first, middle and final frame PNGs, encoder logs, and a
`render.json` manifest alongside the videos. Use these to inspect framing,
motion and lighting before publishing the videos.

## Provisional videos for all ten seeds

The exporter accepts `--pattern p01` through `p10` and uses the same in-memory
scene builder as `view/backend/scene_patterns.py`. The shared population JSON
files determine the exact bottle identities and poses. `--fps 10` samples the
existing 30 fps trajectory every third frame, keeping its motion speed.

The renderer's `--quality draft` uses 960×540 and two Kit updates per captured
frame. It preserves normal lighting, shadows, reflections and DLSS: aggressive
lighting reductions made the scene unreadable during validation. The final
profile retains 1080p and five updates per frame.

From the Isaac Lab machine, with the EULA accepted:

```sh
OMNI_KIT_ACCEPT_EULA=YES python simulation/scripts/render_rail_patterns.py \
  --export-python /path/to/export-env/bin/python \
  --isaac-python /path/to/IsaacLab3/.venv/bin/python \
  --out out/rail-patterns --quality draft
```

This produces a pair of synchronized MP4s per pattern, sample PNGs, individual
manifests and logs, and a batch `index.json`. Use `--patterns p01 p02` for a
subset. The batch stops on a failed export or render; it only indexes completed
pairs. For final production use `--quality final` to export at 30 fps and render
at 1080p. Drafts are separate artifacts from the existing viewer replay videos.

## Table object and material

`rail_usd_table.prepare_table` authors `/World/Table` as one USD component,
containing the beveled worktop and six legs. It deactivates the original visual
parts and overlapping source slab, so the rendered worktop has only one mesh.
The source MJCF collision geometry and its dimensions remain unchanged.

MuJoCo's USD exporter maps shininess to metalness, turning the glossy white
worktop into 90% metal. The table now uses an explicit `UsdPreviewSurface`
material with white diffuse color, metallic 0, roughness 0.45 and IOR 1.5.
This correction runs in both the exporter and renderer, including cached USD
exports. The helper is idempotent. `--quality draft --subframes 2` renders
three Kit updates per frame for the corrected seed replays.

## Record the viewer's vision-driven initial scan

`record_view_scan.py` runs the actual `view/backend/live_scan.py` perception and
controller on a separate model, without starting a dashboard or changing the
running viewer. It stops when the initial scan completes and stores the model,
full joint states, captions and the scan's bench map. The model snapshot embeds
geometry and textures; recording and export must use the same MuJoCo version.

```sh
simulation/.venv/bin/python simulation/scripts/record_view_scan.py \
  --pattern p01 --fps 10 --out simulation/out/scan-p01
# In the separate MuJoCo + USD export environment:
python simulation/scripts/export_rail_animation.py \
  --recording simulation/out/scan-p01 --out out/scan-p01-usd
# In Isaac Lab, keep normal lighting and three render updates per frame:
python simulation/scripts/render_rail_isaaclab.py --export out/scan-p01-usd \
  --out out/scan-p01-videos --quality draft --subframes 2 --headless --enable_cameras
```

Perception and physical motion run during recording; Isaac Lab renders the
resulting states offline. The video therefore reproduces the controller's real
scan, while no new perception or control decisions are made by Isaac Lab.
The bench map reports what the scan actually identified, including misses.

To record a chat request through the end of its formula run, add `--brief`:

```sh
simulation/.venv/bin/python simulation/scripts/record_view_scan.py \
  --pattern p01 --fps 10 --out simulation/out/gantry-p01-citrus-woody \
  --brief 'Fragancia citrica con notas woody'
```

This submits the text to the same `Workflow.submit_brief` used by `/api/chat`.
It waits for the scan, asks Claude to compose from the identified compounds,
then runs the viewer's `FetchExecutor` and gantry controller. The API key comes
from the environment or the gitignored `view/backend/.env`. The output also
contains `composed.json` and `formula_order.json`; rejected briefs stop recording
with an error rather than substituting a canned formula.

The gantry mimes uncapping and pipetting while changing the source and beaker
liquid levels. These levels are recorded alongside joint states and exported
as animated cylinder positions and scales. Export and render use the same
commands above; `--quality final --subframes 2` produces both views at 1080p.
This is a camera recording of the simulated run, not a recording of the chat UI.
