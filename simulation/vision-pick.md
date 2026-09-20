# Vision pick: the cameras direct the arm

`scripts/vision_pick.py` joins the three pieces of the project into one running
loop: the YOLO detector (Martí), the box-to-bench-coordinates and ArUco ring
code in `computer-vision/labvision` (Nacho, Eloi's catalogue), and the UR10e on
its rail with physics grasping (Nacho).

```
 fixed camera ─► YOLO boxes ─► propose(): box ∩ bench plane ─► tracked bottles (x, y), ~8 mm
   (perception thread: runs all the time, whatever the arm is doing)     │
                                                                         ▼
 wrist camera ◄── the initial scan flies it over the bench; ◄── controller picks the next job
      │           a pick takes it 0.36 m from the bottle, 25° up
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
| nothing | the **initial scan** first: the arm is raised where it stands, and the rail then flies the wrist camera over the bench in passes, reading every ring that goes by, and writes `out/bench_map.json`; then it picks each named bottle and puts it back |
| `--headless --manual` | the initial scan only; it stops once the bench is mapped |
| `--no-scan` | no initial scan: the arm looks at and picks each detection as it comes |
| press `M` in the MuJoCo window, or **move a bottle** on the page | a named bottle is put somewhere else; its track is lost, a new one appears, the arm reads it and logs `SMP-0013 moved 160 cm` |
| double-click a bottle, Ctrl + right-drag | the same, by hand |
| `--manual`, then **pick** on a row of the page | the arm only looks; it picks what you ask for |
| `--headless --perturb-at 100 --video out/run.mp4` | no window; writes what the cameras saw and prints the score |

## For the demo

A script that shows the point in about two minutes:

1. Start it. The page fills with yellow boxes: "the fixed camera sees bottles
   and knows where they stand, not what they are."
2. The arm rises and flies the wrist camera the length of the bench, three
   passes at different aims and heights, going to no bottle and stopping at
   none. Boxes turn green with a sample id as the camera goes past them: "now
   it knows which sample, to under a millimetre."
3. The log says the initial scan is done and the bench is mapped. Then the arm
   picks each bottle on the gripper's own force sensing and puts it back.
4. Press `M`. The log says the track is lost, a new box appears elsewhere, the
   arm goes there and the log says which sample moved and how far.

Use `--manual` if you would rather choose the bottle yourself in front of the
judges. Have the `--video` recording of a good run ready as the fallback.

## Measured

### The initial scan

**The scan is a flyover.** It used to go to each proposal in turn: the arm
parked at one end of the rail, then flew the wrist camera down to 0.36 m from
each bottle at 25 degrees above level to read its ring. That named 19 of 19,
but at that pose the lowest part of the hand stands 3 cm *below* the top of the
bench, and between looks it waited 3 cm over the tallest flask --- it knocked
bottles over. It also cost a trip to every bottle.

It now goes to no bottle at all. The arm is raised where it stands, the fixed
camera surveys the bench from under it, and the rail then carries the wrist
camera the length of the bench in passes while it reads every ring that passes
through the frame. Three things set a pass:

* **It looks across the bench, not down at it.** A label ring is a band round
  the side of a vessel, so from straight above it is edge on: flown in the carry
  pose, which points the hand down, the whole rail read one ring in nineteen.
  Each pass tilts the hand instead --- 50, 65 and 40 degrees below level --- and
  each tilt lands on a different strip of bench.
* **It flies as low as what stands under it allows.** A 10 ml flask carries a
  6.6 mm marker against the 100 ml flask's 14.1 mm, and a marker has to be about
  a dozen pixels across to decode, so the small vessels only read from close to.
  At every read the arm takes the lowest height whose *whole* arm stays
  `SCAN_CLEARANCE` (12 cm) over the tallest vessel the cameras know of within
  60 cm along the rail, and climbs again before it reaches a taller one. The
  heights it knows how to hold are solved once each, 5 cm apart.
* **It stops at nothing.** A read is asked for every 15 cm of travel and folded
  in as it lands. The passes run in rounds until a round names nothing new.

What the air cannot read is still visited, nearest first, once the passes are
done: `look` tries its raised looks before it brings the hand down to anything,
so that is the exception and no longer the way in.

`--headless --manual --light`, rail-trained weights, the gripper scene, the
integrated-graphics laptop, 2026-09-20:

| | the per-bottle sweep | the flyover |
| --- | --- | --- |
| bottles on the bench (truth) | 19 | 19 |
| named from the air | --- | **16, none wrongly** |
| named at all | **19, none wrongly** | the three the air missed are looked at afterwards; that step is not in the run above |
| the arm's lowest point over the flask tops, while it reads from the air | −3 cm | **+12 cm, whatever the pass** |
| trips to a bottle | 19 | **3**, and only after the passes |
| position error of the named, median / max | 0.4 mm / 2.6 mm | **0.5 mm / 2.3 mm** |
| first round of three passes | 181 s of simulated time | 254 s |

14 of them were named in the first round of passes, 16 by the middle of the
second: the two the second round adds are the flasks at the aisle edge, which
only the highest pass reaches, and the fixed camera had boxed neither. The run
above was stopped at its 500 s limit, in the second round, with every pass still
reading; the three left for a look are a 10 ml flask at the aisle edge, a 30 ml
flask directly under the arm, and one more on the edge.

Two things went in after that run and have not been flown end to end yet: the
per-pass preferred height, and the looks that pick up what the air missed. The
looks are the same `look` the scan used to use for everything, which names 19 of
19 on this bench, so the expectation is 19 of 19 with three trips instead of
nineteen --- but it is an expectation, not a measurement.

What a pass can read was measured pose by pose before it was flown: the arm
posed at each pass's height, the rail stepped by hand, every ring in the frame
read. That is where the three aims and the two heights come from, and it says
what the limits are. A 10 ml flask's marker is 6.6 mm: at 1.45 m the camera
reads the far side of the bench and misses it; at 1.25 m it reads it and loses
the far side. Neither height alone does better than 15 of 19; the passes differ
in height for that reason.

The old per-bottle sweep is still in the file (`look`, `plan_slide`, `hop`,
`over`), because a **pick** still needs a close look to place the bottle to a
millimetre before the gripper closes. Nothing in the scan uses it.

What made the per-bottle sweep work is what makes the flyover work:
**the wrist camera keeps every ring it reads, not only the one it
went for** (`rings_in_view`, `World.sighted`). Each ring is placed by its own
geometry, the same way `confirm()` places the target's. What happens to it
depends on where it lands:

* **Near a track nobody has named:** it names that track, which then needs no
  look of its own. That is 5 tracks on this bench.
* **Near nothing:** it is a bottle the fixed camera never boxed. It becomes a
  track only the wrist camera has seen, and the fixed camera not seeing it
  does not count against it. SMP-0009, SMP-0120 and SMP-0125 stand on the
  aisle edge, where the fixed camera misses them. Three of the four
  ingredients of the demo recipe FRG-031 are among them.
* **Off the worktop, or more than 1.2 m from the lens:** it is dropped. One
  read on this bench was a shelf bottle 4.9 m away.

**Found is not reachable.** All four FRG-031 ingredients (SMP-0009, SMP-0120,
SMP-0125, SMP-0021) stand on the aisle edge, at y = -1.11 to -1.27. The scan
names all four, but `plan_grasp` finds no grasp for any of them: from the rail
at y = 0.30 they are beyond the UR10e's reach. Asked from the page, the arm
logs `named, but the gripper cannot reach`. Every scanned flask between
y = -0.81 and -0.28 can be grasped, and so can the two on the back strip at
y = +0.43 and +0.47. SMP-0130, under the gantry beam, cannot. For the recipe
to run, its ingredients have to stand in that band, or the recipe has to use
samples that do.

SMP-0044's box lands 6.3 cm from the bottle, and `confirm()` takes a ring more
than 5 cm off to be a neighbour's. Its own look now names it through the same
path, since 8 cm is still well under the 10 cm between any two vessels.

Before this, 15 were named and the scan took 206 s. Two things made the looks
cheaper:

* **Fewer looks.** 11 instead of 16: neighbours name 5 boxed tracks without a visit.
* **A race is fixed.** The perception thread used to read the wrist frame from
  the state it had copied at the top of its cycle. That copy could be a whole
  cycle old, with the arm still on its way to the view. The frame then read
  nothing and the arm tried a second bearing. It now copies the state again
  right before it reads.

`out/bench_map.json` follows the format in `SCANNING_PLAN.md`. Each named
bottle is keyed by its sample id, with its catalogue row, the ring-refined
position, how many markers were read and `found_by` (fixed or wrist camera). A
proposal the ring did not name is kept as `UNK-*` with its position, because
the arm must not hit it. `scored` grades each entry against the simulator and
is the only field that reads it. The plan's merge rules for a second pass are
not implemented: this is the first pass only.

**The hand stays still.** This was measured on the per-bottle sweep, which the
flyover has replaced; the flyover turns the hand once per pass and not at all in
between. The arm moved as little as it could between views, and the hand hardly
turned. Measured from the camera's orientation through the whole scan, recorded
at 15 fps on the default bench with the same 19 flasks:

| | first version | now |
| --- | --- | --- |
| total turning of the hand | 4299 degrees | 1114 degrees |
| wrist joints, summed | 5778 degrees | 2279 degrees |
| scan time | 148 s | 109 s |
| named | 19 of 19 | 19 of 19 |

Four changes do it:

* **One way of looking per row.** Every flask in the front row is looked at
  from the rail side, with the same gaze, and the back strip from the aisle
  side. The scan does the front row on the way out and the back strip on the
  way back, so the hand turns round once, not every time the route crosses
  between the rows.
* **Slide, don't reshape.** A view is solved from the pose the arm is waiting
  in, with the carriage standing where it stood relative to the camera
  (`plan_slide`). The camera then moves along a straight line with its
  orientation fixed (`straight`): IK every 10 cm, each from the one before.
  Where that line would hit something, such as the balances on the back strip,
  it goes straight up, across and down instead (`over`), still without
  turning. The rail does most of the travelling.
* **Never a full turn.** The UR10e's joints turn through two full turns, so
  IK can return an angle 360 degrees away from where the joint stands. A servo
  sent there spins the hand round to arrive where it almost was: 341 degrees
  in one move, measured. Every IK answer, and every servo goal in `drive` and
  `glide`, is taken the nearest way round (`unwrap`).
* **Stay over the flasks.** Between views the arm waits just over the tallest
  flask on the bench: its lowest point is at least 3 cm over the top of it
  (`HOVER_MARGIN`), about 20 cm lower than the carry pose. The tallest comes
  from the ring's vessel once a flask is named, and from the height of the
  fixed camera's box before that, which comes out a little tall on purpose.
  The moves are checked against that height, because `blocked()` ignores the
  free flasks. When a slide cannot be made, the arm tries once through the
  carry pose lowered to that height (`hub_pose`), and only after that climbs
  to the carry pose.

What still turns the hand, in that run:
* **177 degrees, once:** from the hand-down carry pose to the first view.
* **150 degrees, once:** between the two rows.
* **455 degrees:** SMP-0048, which stands at y = -0.28, close to the rail. The camera
  has no room to look at it from the rail side at 0.36 m, so it looks from
  60 degrees round, and it reaches that through the carry pose. A closer,
  steeper view from the rail side (0.26 m, 35 degrees) reads its ring. As the
  scan's second choice, though, it left the next views in another orientation,
  and the scan named 18 of 19 instead of 19, so it is not used.
* **94 degrees:** the flask on the aisle edge at full reach.
Fixing those needs a planner that works in the camera's space around
obstacles, not joint-space moves checked afterwards.

A ring misread is guarded against. Measured once: a single bit error on
SMP-0044's ring read as SMP-0018, 5 mm from it. Two rings placed within 3 cm of
each other in one frame are one bottle. The one with more markers read wins,
and a tie names neither. A ring that lands on a bottle already named something
else is ignored.

The viewer (`view/`) runs this same scan on its rail scene; see
`view/README.md`.

**What the scan cannot find.** A flask gets on the map in one of two ways: the
fixed camera boxes it, or its ring shows up in a wrist frame. The flyover covers
the whole rail rather than only the places with a proposal in them, so a flask
with no box is no longer a special case --- but a ring it never reads still
leaves the flask on the map as `UNK-*`, with its position and no name, and the
arm will not pick what it cannot name. Two things stop a ring being read: the
marker is too small at that range (the 10 ml flasks, at the aisle edge) or the
ring is too edge on (the strip directly under the arm). Both are answered by
where the passes fly, and both are worth another pass rather than a lower one:
the floor under the arm is what keeps the bottles standing.

### The whole loop

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
