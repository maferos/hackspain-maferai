# GPU proposal — MiniHannover lab simulation & synthetic data

Why the project needs a GPU, what hardware/driver actually works, and what to
provision. Requirements below are grounded in what we ran this hackathon (Isaac
Sim 4.5 RTX on a rented NVIDIA A40), not guesswork.

## 1. Why we need a GPU

The `simulation/` → `computer-vision/` pipeline is GPU-bound end to end:

- **Photoreal synthetic data (the core deliverable).** We render the perfumery
  lab with **NVIDIA Isaac Sim 4.5 (RTX path tracing)** and auto-label every
  bottle by its EAN-13 barcode, producing COCO detection data + segmentation
  masks for the CV team. RTX ray tracing runs **only on the GPU** — there is no
  CPU fallback that is remotely usable. Example already produced: 300–500 frames,
  ~130k labelled boxes across 180 barcode classes.
- **Robot manipulation simulation.** Isaac Lab / MuJoCo for the arm (Franka /
  UR10e / Kinova) with eye-in-hand cameras — physics + rendering, GPU-accelerated.
- **CV model training.** The detector/reader the CV lane trains on this data is
  itself GPU work (CUDA).
- **Iteration speed.** Isaac cold start is ~4–5 min, then ~5 s/frame; a full
  5-camera randomized state is ~47 s. Domain randomization at dataset scale means
  thousands of renders — only practical on a GPU.

Today we rent GPUs ad-hoc on RunPod. It works, but we've hit **availability and
proxy flakiness** mid-run (an in-progress render became unreachable because the
provider's TCP proxy dropped, even though the pod stayed "running"). A stable,
correctly-specced GPU removes that risk and the per-hour meter.

## 2. Hard requirements (Isaac Sim 4.5)

| Requirement | Needed | Why / evidence |
| --- | --- | --- |
| **RT cores (RTX)** | Mandatory | Isaac renders via RTX. Non-RTX GPUs (e.g. A100/H100 datacenter compute cards) render poorly or not at all — they lack RT cores. |
| **Architecture** | **Ampere (sm_86) or Ada (sm_89)** | Verified working: A40 (Ampere). **Blackwell (RTX 5090, sm_120) does NOT work with Isaac 4.5** — it segfaults at startup. |
| **VRAM** | **≥ 24 GB**, 48 GB recommended | The lab scene is ~13.5k USD prims / ~3.3k meshes; on the A40 (48 GB) it ran comfortably. 24 GB is the floor; 48 GB gives headroom for bigger scenes, higher res and batching. |
| **Driver** | **570.x or 580.x** | Verified: driver **570.195.03 works**. **595.x is too new** → segfault at `_wait_for_viewport`. Older than 570 lacks the CUDA 12.x driver API Isaac 4.5 needs. |
| **CUDA** | 12.x driver API (Isaac ships CUDA 11.8 runtime) | Provided by driver ≥ 570; do not need a system CUDA install. |
| **OS / stack** | Linux + Docker + `nvidia-container-toolkit` | We run the official `nvcr.io/nvidia/isaac-sim:4.5.0` image (headless, `ACCEPT_EULA=Y`). |
| **ECC** | Prefer **off** for rendering | iray warns ECC reduces render performance; fine to leave on, better off. |

### Do NOT provision
- **RTX 5090 / 5080 / any Blackwell** — unsupported by Isaac 4.5 (segfault).
- **Driver 595+** — too new, segfaults. Pin to 570/580.
- **Compute-only cards without RT cores** (A100, H100) — no usable RTX path.

## 3. Recommended cards

| Card | VRAM | Arch | Fit |
| --- | --- | --- | --- |
| **NVIDIA L40S** | 48 GB | Ada (sm_89) | **Best datacenter option** — modern, RT cores, big VRAM, well supported. |
| **NVIDIA A40** | 48 GB | Ampere (sm_86) | **Proven this session.** Solid, widely available on cloud. |
| **RTX A6000** | 48 GB | Ampere | Workstation equivalent of the A40. |
| **RTX 4090** | 24 GB | Ada (sm_89) | **Cheapest capable** option; great for a local dev box. 24 GB is enough for the current scene. |

## 4. Provisioning options

1. **Cloud on-demand (current)** — RunPod / similar, A40 ≈ **$0.49/h**.
   Flexible and cheap per hour, but subject to availability and the proxy issue
   we hit. Good for bursts; **pin the data center to one that ships driver
   570/580** (Montreal / `CA-MTL-*` gave us 570) and check `nvidia-smi` before
   rendering.
2. **Reserved cloud instance** — a fixed L40S/A40 with a known-good driver for
   the length of the project. Predictable, no re-provisioning, no proxy roulette.
3. **Local workstation** — a single **RTX 4090 (24 GB)** or **A6000 (48 GB)**
   box. Best iteration speed (no cold-start pod, no network), one-time cost,
   reusable well beyond the hackathon.

## 5. Recommendation

- **Short term (hackathon):** keep cloud on-demand, but **standardize on A40 or
  L40S with driver 570/580** and a data center that provides it, to stop losing
  runs to driver/proxy issues.
- **If the work continues past the hackathon:** a **local RTX 4090 (24 GB)** dev
  box for day-to-day iteration, plus **cloud L40S (48 GB)** bursts for large
  dataset generation. This is the cheapest path that also removes the
  availability risk.

---

**One-line ask:** one NVIDIA **RTX-class GPU, Ampere or Ada, ≥ 24 GB (48 GB
preferred), driver 570/580** — cloud A40/L40S now, ideally an RTX 4090 / A6000
workstation if the project continues. Avoid Blackwell (RTX 5090) and driver 595+.
