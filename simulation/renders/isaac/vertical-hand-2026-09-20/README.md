# Vertical hand animation rendered with Isaac Lab

Eki's 23-step uncap-and-pipette animation from commit `7bff5de`, including approach and retreat. Source: `simulation/assets/vertical_hand/vertical_hand.usdc`, with its baked Blender animation and reference 60 ml bottle.

`vertical_hand.mp4`: 1920x1080, 30 fps, 1,000 frames (33.333 seconds). Rendered on NVIDIA L4 using Isaac Lab 3.0 EA / Isaac Sim 6.1 RTX Real-Time, DLSS and three updates per frame. Camera framing, studio floor and lights were adjusted for visibility. The animation is USD playback, not an Isaac physics or mimic-joint validation.

Measured render time including Isaac startup and MP4 encoding: 126.405 seconds. Complete video decode and frame count verified.

Reproduce with the Isaac Lab Python environment:

```bash
OMNI_KIT_ACCEPT_EULA=YES python simulation/scripts/render_vertical_hand_isaaclab.py \
  --export simulation/assets/vertical_hand --out simulation/out/vertical-hand-isaac \
  --quality final --subframes 2 --light-multiplier 1 --headless --enable_cameras
```

## Underside camera

`vertical_hand_underside.mp4` uses the same 1,000 animation frames at 30 fps, with a close view looking upward into the jaws and cap mechanism. A low fill light reveals the internal parts. Render time: 108.283 seconds. Select `--camera underside` with the command above to reproduce it.
