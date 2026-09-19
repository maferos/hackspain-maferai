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
```

The detector's weights are gitignored and have to be copied by hand to
`computer-vision/runs/fixedcam/yolo26n_fixedcam.pt` (ask Martí, 20 MB). The
detector picks CUDA or Apple MPS by itself.

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

## What it does not do yet

* **The detector sees 12 of the 19 bottles.** The seven it misses stand at the
  edges of the frame, where the wide lens leans them 30 degrees. 4K, YOLO-World
  and sweeping a camera along the rail did no better: it is training data. A
  bottle it cannot see, the arm never visits. For the demo, keep the bottles in
  the middle 4 m of the bench, or retrain with bottles at the edges.
* **Not tested in the interactive viewer or on a GPU.** Only headless runs were
  made. The `M` key, the page's buttons and mouse dragging go through the same
  code as `--perturb-at` and the scripted run, but nobody has pressed them yet.
* **It picks and puts back; it does not yet carry a bottle to a balance.** The
  pieces are there (`plan()` checks any pose and path); the task is not written.
* **The React viewer in `view/` still shows its scripted mock.** Feeding it this
  loop's tracks through `labvision.world.to_dashboard` is the next link.

The design notes and the three ways IK fooled the arm are in the
[README](README.md#the-cameras-direct-the-arm).
