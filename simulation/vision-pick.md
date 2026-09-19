# Vision pick: the cameras direct the arm

`scripts/vision_pick.py` joins the three pieces of the project into one running
loop: the YOLO detector (Martí), the box-to-bench-coordinates and ArUco ring
code in `computer-vision/labvision` (Nacho, Eloi's catalogue), and the UR10e on
its rail with physics grasping (Nacho).

```
 fixed camera ─► YOLO boxes ─► propose(): box ∩ bench plane ─► tracked bottles (x, y), ~8 mm
   (perception thread: runs all the time, whatever the arm is doing)     │
                                                                         ▼
 wrist camera ◄── IK flies it 0.36 m from the bottle, 25° up ◄── controller picks the next job
      │
      ▼
 confirm(): ArUco ring ─► sample id + vessel ─► exact (x, y), < 1 mm ─► grasp on force feedback ─► lift
```

Nothing the arm decides reads the simulator's state. It knows about a bottle
only what the cameras told it.

## Is it real time?

**The design is; this laptop is not.** Two loops run at once and neither waits
for the other: physics and the arm run at simulated real time, and perception
runs on its own thread as fast as the machine renders and detects.

| | Integrated graphics, CPU torch (measured) | Discrete GPU (expected, not measured) |
| --- | --- | --- |
| Physics + arm motion | real time | real time |
| One perception cycle (render 1080p + YOLO + tracks) | 1 to 2.5 s | well under 0.1 s |
| A moved bottle is noticed after | 3.5 to 5 s | under a second |
| Look at a bottle and pick it | ~24 s of arm motion | the same; it is motion, not compute |

So on a laptop with a GPU the detections follow the bench live. What stays slow
anywhere is the arm: it moves at a safe 0.6 m/s and 0.9 rad/s, and a look plus a
pick is about 24 s per bottle. The GPU column has **not been run**: the first
thing to do on a teammate's machine is start it and read "perception cycle" on
the page.

## Run it

```bash
cd simulation
bash scripts/fetch_menagerie.sh      # UR10e + 2F-85 models, gitignored, once
pip install -r ../computer-vision/requirements.txt   # ultralytics, opencv
python scripts/vision_pick.py        # mjpython on macOS
python scripts/vision_pick.py --light   # integrated graphics: see below
```

Run it from a checkout of `main`. (If `scripts/vision_pick.py` is not there, the
folder is on another branch: `git branch --show-current`.)

**On a laptop without a real GPU, pass `--light`.** The MuJoCo window and the
perception thread both draw the room's 1.1 million triangles, and together on
integrated graphics a perception cycle took 7 to 68 s: the page stays empty for
a minute and a half and it looks dead. `--light` stops drawing the meshes that
stand off the bench (the GC-MS by the door is a third of the total). No decision
changes --- nothing off the worktop is ever a proposal, and the detector finds
the same bottles --- and the cycle drops to 2 to 3 s with the first boxes on
the page 18 s after start.

The detector's weights are gitignored and have to be copied by hand (ask Martí,
20 MB each). It uses the first of these it finds:

1. `computer-vision/runs/rail/yolo26n_rail_general.pt` (or `computer-vision/weights/`)
   --- trained on this scene's own camera. **Use this one**: on the loop's bench it
   finds the same 12 bottles as the older model with no false box, against ten.
2. `computer-vision/runs/fixedcam/yolo26n_fixedcam.pt` --- the fallback.

The detector picks CUDA or Apple MPS by itself, and the first line it prints
says which weights and device it took.

The rail scene ships with the **pipette** on the flange, and a pipette cannot
pick a bottle up. So the first run builds a gripper copy of the scene with
Nacho's generator (`models/minihannover_rail_gripper_scene.xml`, gitignored) and
loads that; the pipetting scene is left exactly as it was.

It opens the MuJoCo window and a page at http://localhost:8009 with the fixed
camera and its boxes, the wrist camera, the table of tracked bottles and the log.

| Do this | And this happens |
| --- | --- |
| nothing | the arm looks at every detection in turn, names it by its ring, picks it, puts it back |
| press `M` in the MuJoCo window, or **move a bottle** on the page | a named bottle is put somewhere else; its track is lost, a new one appears, the arm reads it and logs `SMP-0013 moved 160 cm` |
| double-click a bottle, Ctrl + right-drag | the same, by hand |
| `--manual`, then **pick** on a row of the page | the arm only looks; it picks what you ask for |
| `--headless --perturb-at 100 --video out/run.mp4` | no window; writes what the cameras saw and prints the score |

## For the demo

A script that shows the point in about two minutes:

1. Start it. The page fills with yellow boxes: "the fixed camera sees bottles
   and knows where they stand, not what they are."
2. The arm goes to the first one, the wrist view shows the ring, the box turns
   green with a sample id: "now it knows which sample, to under a millimetre."
3. It picks it up on the gripper's own force sensing and puts it back.
4. Press `M`. The log says the track is lost, a new box appears elsewhere, the
   arm goes there and the log says which sample moved and how far.

Use `--manual` if you would rather choose the bottle yourself in front of the
judges. Have the `--video` recording of a good run ready as the fallback.

## Measured

330 s of simulated time on the shipped scene, one bottle moved 1.6 m at t = 100 s,
headless on the integrated-graphics laptop:

| | |
| --- | --- |
| tracks the fixed camera held | 15 |
| named by their ring | 11, none wrongly |
| picks attempted / lifted / closed on air | 9 / 9 / 0 |
| named but out of reach | 1, under the gantry beam |
| position error of the named, median | 1.5 mm |
| moved bottle: new track seen / old track lost | 3.5 s / 5.3 s after the move |

On `main`'s scene (open flasks, pipetting balance, 200 s, same laptop): 6 picks,
6 lifted, none on air, 5 rings checked right against truth. The detector also
boxes beakers, the funnel, the pot and the wash bottles there; boxes bigger than
a flask would look where they stand are dropped (34 proposals down to 22), and
the arm looks first at what the detector scores 0.5 or better, which on this
scene is every real bottle. The position error the report prints after a run is
larger (about 12 mm) than the ring's, on purpose: once a bottle has been put
back down its ring position is spent and the fixed camera's stands in.

With the rail-trained weights, same scene and laptop, 200 s: 12 tracks and all
of them real bottles, 6 picks, 6 lifted, none on air.

## What it does not do yet

* **The detector sees 15 of the 19 bottles.** The four it misses stand on the
  aisle edge and the far left corner, where the wide lens leans them 30 degrees.
  A bottle it cannot see, the arm never visits, so for the demo keep them off
  the very edge. *Correction:* this file first said 12 of 19 and blamed the
  detector for all seven. Three of those were this script's own fault: it kept
  only detections within +-3 by +-1 m of the origin, and the bench runs from
  x = -4.5 to 1.5 and y = -1.4 to 0.6. The bounds now come from the generator.
* **Not tested on a GPU, and nobody has pressed `M` or the page's buttons.** The
  interactive viewer was started three times running on the integrated-graphics
  laptop and tracked 15 bottles within 18 s each time; the keys and buttons go
  through the same code as `--perturb-at`, but no hand has tried them.
* **It picks and puts back; it does not yet carry a bottle to a balance.** The
  pieces are there (`plan()` checks any pose and path); the task is not written.
* **The React viewer in `view/` still shows its scripted mock.** Feeding it this
  loop's tracks through `labvision.world.to_dashboard` is the next link.

The design notes and the three ways IK fooled the arm are in the
[README](README.md#the-cameras-direct-the-arm).
