# Unscrewing caps in Isaac — plan

> Picks up the item `PIPETTING_PLAN.md` deliberately left out ("unscrewing it is
> a separate job") and its own *Next, in order: 2. Unscrewing caps*.

Target: **a standalone, photoreal clip that argues the three-part gripper can
take the cap off one of our flasks, pipette from it, and screw the cap back
on** — rendered in Isaac Sim RTX, with a measured success rate behind it.

This does **not** go into the MuJoCo bench scene. There, the decap stays
scripted and faked. This is a second, small, high-fidelity scene whose only job
is the mechanism.

Platform: **Isaac Sim 4.5 + Isaac Lab, headless on RunPod** — the stack already
verified in `runpod-isaac.md` and specced in `../propuesta_gpu.md`.

---

## What we already have

More than it looks like. The audit, file by file:

| Have | Where | State |
| --- | --- | --- |
| **A real helical thread on the neck** | `assets/amber-bottles/generate_amber_bottles.py::helix_thread` | Trapezoidal profile swept along a helix, faded in/out over the first and last half turn. Driven by `pitch = 0.11·N`, `tdepth = 0.04·N`, `THREAD_TURNS = 2.0` |
| **Standard neck sizes** | same file, `NECK_FOR_ML = {10:18, 20:18, 30:20, 50:25, 60:25, 100:28}` | PP 18/20/25/28. The 30 ml flask is **PP20: pitch 2.2 mm, thread depth 0.8 mm, 2 turns** |
| **The cap as its own body** | `glb/amber_cap_XXmm.glb`, and `flask_*_cap.obj` in MuJoCo | Separate mesh, separate geom |
| **A procedural Blender pipeline** | `assets/*/generate_*.py`, `bpy`, headless | Parametric, scripted, re-runnable. This is the right place to author the gripper |
| **GLB → MuJoCo conversion** | `tools/convert_glb.py` | Keeps origin, +Y→+Z, merges seams, `inertia="exact"` |
| **A pipette** | `assets/pipette/pipette.xml`, `scripts/generate_pipette.py` | Procedural, fixed tip, 125 mm, radius 2.7 mm, plunger and ejector modelled |
| **Flask internals measured** | `PIPETTING_PLAN.md` | Neck outer Ø 24 mm, **bore Ø 18.4 mm**, 15 mm tall, shoulder tapering from Ø 37.6 mm. Cap Ø 30.2 mm, 18.5 mm tall |
| **Liquid as level + bookkeeping** | `scripts/generate_open_vessels.py`, `scripts/pipetting.py` | Already the chosen approach, already working: 12/12 transfers |
| **MuJoCo → USD export** | `scripts/export_usd.py` | MuJoCo's own `USDExporter`, name sanitising for USD prim paths, runs off Isaac |
| **Isaac RTX render of a USD** | `scripts/render_usd.py`, `scripts/arm_pose_render.py` | Verified on RTX 4090/A5000/A40. `LIGHTMUL≈40` for the closed room |
| **A working RunPod recipe** | `runpod-isaac.md` | REST v2 `dockerEntrypoint` override → sshd → `/isaac-sim/python.sh`. Driver 570/580, Montreal DCs, Ada/Ampere only |

## What is missing

Five things. Two are geometry, three are capability we have never exercised.

### 1. The cap has no internal thread

`cap_dims()` sets `ri = N/2 - 0.3 + 0.35` — *"radio interior (holgura sobre la
rosca)"*. The cap is a **smooth bore with clearance over the neck thread**. It
slips on; it cannot engage.

This is the smallest missing piece and the most important one. `helix_thread()`
already exists and already does the hard part; the cap needs the same helix with
an inward-facing profile, at the mating pitch, with a **controlled radial
clearance** — because that clearance is the number that decides whether a recap
cross-threads, and it has to be a parameter, not an accident.

### 2. The gripper does not exist

The three-part head — two fingers on the pot body, the iris clamp on the cap,
the pipette as the third finger — has no model in any form. Blender kits are
being generated now. What the sim needs beyond the visual mesh:

- Jaw geometry that can actually be a collider, not a decorative shell.
- The differential's **ratio**, and its **rotation stroke**: whether the iris
  turns continuously or has a limited arc. See the open question at the end.
- Joint axes and limits, and where the tool frame sits.

### 3. Nothing in this repo authors physics in Isaac

This is the structural gap and it is easy to miss, because `renders/isaac/`
looks like we have an Isaac pipeline. We have an Isaac **render** pipeline.

`export_usd.py` calls `USDExporter.update_scene()` + `save_scene()` — that
writes one *frame*: visual meshes, materials, cameras, lights. It contains **no
`UsdPhysics` APIs, no colliders, no rigid bodies, no articulations, no joints,
no drives**. `render_usd.py` opens a stage and renders it. `arm_pose_render.py`
poses an arm to hold still with *gravity switched off*.

So there is no path in the repo from "MuJoCo scene" to "thing that simulates in
PhysX". The cap scene has to be **authored natively in USD with physics**, by a
new script. It is not a conversion job.

### 4. SDF colliders, impedance control, mimic joints — all new

None of these appear anywhere in the repo:

- `PhysxCollisionAPI` with **SDF approximation at resolution 256–512** on the
  two thread meshes (precedent: NVIDIA Factory / IndustReal for nut-and-bolt).
- **Mimic joints** for the iris differential (one actuated DOF, N jaws at a
  fixed gear ratio), and closed-loop rigging if the differential is real.
- **Impedance / compliant axial control**, so the cap's Z motion is a
  consequence of thread contact rather than a commanded helix.

### 5. Isaac Lab itself

`propuesta_gpu.md` and `runpod-isaac.md` both stand up the **Isaac Sim**
container. Isaac Lab — the parallel-env layer that makes a randomised success
rate affordable — has never been installed on a pod. It is what turns this from
a video into evidence.

---

## The plan

Each step ends somewhere runnable and something measurably better, the same
discipline as `PIPETTING_PLAN.md`.

### Step 1 — Thread the cap (no GPU, no Blender install) — **done**

`generate_amber_bottles.py` now has `helix_thread_internal()` beside the
existing helix, `make_cap(N, threaded=True)`, and a `--pair <ml>` mode that
writes the mating pair and checks it. Output and numbers in
[`assets/amber-bottles/thread_pair/`](../assets/amber-bottles/thread_pair/).

`bpy` is a pip package — Blender does not need installing:

    uv run --python 3.11 --with bpy python generate_amber_bottles.py --pair 30 --out thread_pair

Two clearances were added as module constants, both sweepable:
`THREAD_CLEARANCE = 0.15 mm` (radial, the one that decides cross-threading) and
`SEAT_CLEARANCE = 0.15 mm` (axial over the lip — without it the cap's ceiling
and the lip are coincident faces, which a rigid solver reads as
interpenetration rather than contact).

*Done:* all four neck sizes screw through 720° in 72 steps with **no BVH face
overlap at any step**. PP20 travels **4.40 mm**, as predicted. The catalogue is
untouched — every kit mesh hashes identically to before the change.

### Step 2 — The thread alone, in Isaac (first GPU day)

A new `scripts/build_cap_scene.py` that authors a USD **from scratch** with
physics: a fixed threaded neck, a free-body cap, both as SDF colliders at 256,
one revolute drive on the cap about the neck axis, gravity on. No arm, no iris,
no pipette.

Run it and try to screw the cap on and off. Sweep `dt`/substeps, contact and
rest offsets (start at the order of the thread clearance), SDF resolution, μ.
Start from Factory's published settings rather than re-deriving them.

*Done when:* the cap screws on from a given start angle and comes off again,
repeatably, with the Z motion emerging from the contact and no interpenetration
spikes in the contact report.

> This step is the whole risk. Half a day, and if it does not converge, we find
> out before the gripper exists and can fall back to a helical mimic joint and
> say so honestly.

### Step 3 — The gripper as one articulation

Take the Blender head, export to USD, author the physics in
`build_cap_scene.py`:

| Chain | Joints |
| --- | --- |
| Two fingers | Prismatic or revolute, **force drive** — grip force must be a reportable output, so not position control |
| Iris clamp | One actuated DOF + N jaws on mimic joints at the differential's ratio; cap rotation as a revolute about the pot axis |
| Pipette | Prismatic plunger + rigid tip, reusing the 125 mm / r 2.7 mm geometry that already works |

Fingers close on the flask body; check they hold against the cap's breakaway
torque before touching the iris.

*Done when:* the head closes on a 30 ml flask, holds it against an applied
torque, and reports the normal force it needed.

### Step 4 — The cycle, as a state machine

Not a policy. Scripted, the way `pipette_test.py` is scripted:

1. Approach; fingers close on the body at force F.
2. Iris descends, closes on the cap.
3. Unscrew: rotate, **axial motion under low Z stiffness** so it follows the
   helix by contact. 2 turns = 720°, 4.4 mm.
4. If the iris stroke is limited: release, rotate back, re-clamp. Count cycles.
5. Cap out, stays in the iris.
6. Pipette descends into the 18.4 mm bore, plunger aspirates. Volume analytic,
   reusing `pipetting.py` — **no particles**, same decision as the bench.
7. **Recap**: align, find the thread start, screw under impedance.

*Done when:* the full cycle runs once, end to end, and the volume bookkeeping
closes.

### Step 5 — The number

Randomise initial flask pose (±2 mm, ±5°) and μ; run N envs in parallel under
Isaac Lab. Report: **recap success rate**, regrips per cap, breakaway torque,
required finger force, cycle time.

*Done when:* there is a line like `recapped 47/50 at ±2 mm / ±5°` to put on a
slide.

### Step 6 — The render

Same USD, RTX path tracing, via the existing `render_usd.py` path and the
RunPod recipe. Remember `LIGHTMUL` — though this is a close-up on a small rig,
not the closed room, so the lighting will need its own pass.

*Done when:* there is a clip.

---

## Risks worth knowing now

- **Step 2 is the project.** Everything after it is assembly. If SDF thread
  contact does not converge, nothing downstream matters, so it goes first and
  alone.
- **Isaac Sim 4.5 is picky and we know exactly how.** Ada/Ampere only — no
  Blackwell. Driver **570/580**, not 595+. Pin `CA-MTL-*`. Check `nvidia-smi`
  before every run. All of this is already written down in `runpod-isaac.md`
  and all of it cost real time to learn.
- **Do not share the pod.** Two concurrent Isaac RTX contexts on one A40 render
  each other black — see `todo.md`. Coordinate with whoever else is rendering.
- **Isaac Lab on 4.5 is unproven here.** If it fights the container, the
  fallback is N sequential runs in Isaac Sim: slower, same number, still
  evidence.
- **Moving to Isaac Sim 5.x re-opens everything** the GPU proposal pinned. Do
  not do it mid-plan without a reason.
- **`convert_glb.py` drops textures.** Fine for a mechanism clip; remember it if
  the cap is supposed to look branded.

## Open questions, for the mechanism side

These change the plan and only the team can answer them:

1. **Does the iris rotate continuously, or through a limited arc?** At 2.0 turns
   (720°), a 120° stroke means 6 regrips per cap and a 180° stroke means 4.
   Every regrip is a chance to drop the cap or cross-thread on the way back.
   This is the biggest single unknown.
2. **Is the differential real** — one motor producing both clamping and
   rotation — or are they two actuators? A real one is a closed loop and needs
   rigging; two actuators are trivial and we say so out loud.
3. **Which flask?** The plan assumes the 30 ml, PP20. Any of the catalogue works
   once the cap is threaded, but the clearance is per neck size.
