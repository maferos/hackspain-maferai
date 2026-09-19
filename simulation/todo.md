# Simulation — map & TODO (Eloi's lane)

Wayfinder map for the simulation lane, kept as plain markdown (no issue tracker).

## Destination

An integrated demo: a **simulated lab-automation task that emits camera frames**
for the computer-vision team to process. First value = **get images to CV fast**
so they can start; the polished pipeline (Isaac Sim + Replicator on RunPod) follows.

## Notes

- Scope: **Eloi's lane only**. Eki drives the MuJoCo/AutoBio lane separately.
- This map carries **execution**, not just decisions (hackathon: we ship).
- Platform: **NVIDIA Isaac Sim/Lab on RunPod is primary** — a real NVIDIA GPU
  renders Isaac Lab cameras natively, which removes the whole "port cameras to
  Apple/Metal" problem. IsaacLab-mlx on the Mac is optional local dev only.

## Decisions so far

- **Scope = Eloi's lane only.** The MuJoCo/AutoBio lane is Eki's.
- **RunPod (NVIDIA Isaac Sim) is the primary platform**; IsaacLab-mlx demoted to
  optional local dev.
- **Fastest image source = MuJoCo offscreen render on the Mac**, using Eki's
  `minihannover` bench scene (lab-relevant and verified on MuJoCo 3.13) — no
  cloud, no AutoBio Linux plugin. See `scripts/render_dataset.py`.
- **Real labelled dataset = Isaac Sim + Replicator on RunPod**, built in parallel.
- **No interactive Isaac Sim on RunPod.** WebRTC (the official path) needs a UDP
  media port and RunPod blocks UDP; noVNC works over TCP but NVIDIA doesn't
  support the GUI over a virtual display (fragile, RTX-4090/Isaac-4.0 only). So:
  interact in **local MuJoCo**, keep Isaac Sim on RunPod **headless** (render to
  disk); noVNC-over-SSH only as a throwaway. See `runpod-interactive.md`.

## Open

- [ ] **Batch 2 — usable detection data**: objects on the bench (instruments /
      simple primitives) + **segmentation masks** + **depth** from the same
      `render_dataset.py`. Turns bench-only frames into a real CV dataset.
- [ ] **Re-render the arm montage on the de-cluttered open USD (needs an idle GPU).**
      The `minihannover_open` scene now drops the solid/powder jars (working tree:
      `generate_minihannover_open.py` filters stock to `phase == liquid`, 407 → 313
      containers), verified good via `render_usd.py` (bright, de-cluttered bench).
      `arm_pose_render.py` needs re-running to refresh `renders/isaac/arms/` — **no
      code change needed**. Root cause of the "black lab" seen on 2026-09-19 was
      **NOT** our scene change and **NOT** the script: it was **GPU contention** —
      every black arm render happened while a second Isaac RTX process (Eki's
      `dataset_gen*.py`) was running on the same A40; the one render made with the GPU
      idle (`render_usd.py`, 08:45) came out bright. Proof: re-exporting the *old*
      with-solids USD (md5 943931c…, the one that made the committed bright renders)
      and running the unmodified script now *also* renders black while Eki's job runs.
      Diagnostics confirmed geometry+lights+load were all fine at capture, so it's a
      renderer-level conflict between two concurrent Isaac contexts, not the data.
      **Action:** run `ONLY_ARM=franka NPOSES=1` on an **idle** GPU to confirm bright,
      then the full `arm_pose_render.py`, rebuild the montages, done.
      **Coordinate with Eki:** the pod is shared and `dataset_gen*.py` reads
      `/root/lab_usd`; agree on which USD it should hold (de-cluttered =
      md5 467b67ddb776b117d7dd729f7e4df611) before swapping it.

## Not yet specified (fog)

- **CV contract**: resolution / FPS / frame count / label format — pin once the CV
  team reacts to batch 1.
- **Final lab task**: which task, which robot arm, what it manipulates.
- **Replicator dataset**: reuse `minihannover` (URDF→USD) so sim and CV share the
  same bench? Domain-randomisation ranges?
- Whether **AutoBio** frames (Eki, Linux) are needed for extra lab realism.

## Out of scope

- **numi-lab** — Apple-native Metal sim; RunPod renders cameras natively, so no
  longer needed. Reference only.
- **Porting Isaac Lab cameras to MLX/Metal** — mooted by using RunPod.

## Done

- [x] **Isaac Sim on RunPod de-risked** (2026-09-18) — official image
      `nvcr.io/nvidia/isaac-sim:4.5.0` runs headless on an RTX A5000; one 1280×720
      RGB frame rendered to disk via Replicator and pulled back (~$0.15, ~11 min
      end to end). Key unlock: the image's ENTRYPOINT is fixed (streaming app) and
      RunPod's GraphQL/`runpodctl` can't override it, but **REST v2** (`POST
      https://rest.runpod.io/v1/pods`) exposes `dockerEntrypoint` — set it to
      `bash -lc` + an sshd bootstrap and you get a shell. Recipe in
      `runpod-isaac.md`; `scripts/render_isaac.py` + `scripts/runpod_isaac_sshd_boot.sh`.
- [x] **Batch 1 shipped to CV** — 128 RGB frames (640×480) of the `minihannover`
      bench from randomised camera poses + `frames.json`. Generated with
      `scripts/render_dataset.py`; zipped at `out/minihannover_batch1.zip`.
      Bench-only: enough for CV to scaffold their pipeline, not yet a labelled set.
