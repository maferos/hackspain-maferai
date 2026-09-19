---
aliases: []
type: "source"
title: "MuJoCo Playground"
citekey: "Zakka2025mujoco"
doi: "10.48550/arXiv.2502.08844"
arxiv: "2502.08844"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2502.08844"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Kevin Zakka", "Baruch Tabanpour", "Qiayuan Liao", "Mustafa Haiderbhai", "Samuel Holt", "Jing Yuan Luo", "Arthur Allshire", "Erik Frey", "Koushil Sreenath", "Lueder A. Kahrs", "Carmelo Sferrazza", "Yuval Tassa", "Pieter Abbeel"]
sha256: ["1227d94174639184a24c907fa1dda4b0639edc6fabdcc7ec4cfe17198c30afe3"]
pdf: "Content/Papers/Zakka2025mujoco.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Zakka2025mujoco.pdf]]

> [!abstract] One-sentence summary
> MuJoCo Playground is an open-source MJX-based framework with a GPU batch renderer that trains robot policies in minutes on one GPU and transfers them zero-shot to quadrupeds, humanoids, a dexterous hand and a Franka arm from state and pixels.

## Abstract

We introduce MuJoCo Playground, a fully open-source framework for robot learning built with MJX, with the express goal of streamlining simulation, training, and sim-to-real transfer onto robots. With a simple "pip install playground", researchers can train policies in minutes on a single GPU. Playground supports diverse robotic platforms, including quadrupeds, humanoids, dexterous hands, and robotic arms, enabling zero-shot sim-to-real transfer from both state and pixel inputs. This is achieved through an integrated stack comprising a physics engine, batch renderer, and training environments. Along with video results, the entire framework is freely available at playground.mujoco.org (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that iterative reward design makes time-to-robot critical, motivating fast simulation for [[Sim-to-real transfer|sim-to-real reinforcement learning]]. (Zakka et al., 2025) `ev:asserted` p. 2 ^zakka2025mujoco-001
- MuJoCo Playground is a fully open-source robot learning framework built on MuJoCo XLA, a JAX-based branch of MuJoCo that runs on GPU. (Zakka et al., 2025) `ev:reported` p. 2 ^zakka2025mujoco-002
- Playground integrates the Madrona batch renderer for on-device rendering, enabling end-to-end training of vision-based policies without teacher-student distillation. (Zakka et al., 2025) `ev:reported` p. 2 ^zakka2025mujoco-003
- The whole pipeline from environment setup to policy optimization can be executed in a single Colab notebook, with most tasks needing minutes of training. (Zakka et al., 2025) `ev:asserted` p. 2 ^zakka2025mujoco-004
- The authors deployed both state-based and vision-based policies across six robotic platforms in less than eight weeks. (Zakka et al., 2025) `ev:reported` p. 2 ^zakka2025mujoco-005
- Playground environments fall into three categories, DeepMind Control Suite, Locomotion and Manipulation, and use robot assets from MuJoCo Menagerie. (Zakka et al., 2025) `ev:reported` p. 2 ^zakka2025mujoco-006
- Locomotion environments cover the quadrupeds Unitree Go1, Spot and Barkour and the humanoids Berkeley Humanoid, Unitree H1 and G1, Booster T1 and OP3. (Zakka et al., 2025) `ev:reported` p. 2 ^zakka2025mujoco-007
- Each locomotion embodiment has a joystick environment that tracks commanded forward and lateral base velocities plus a desired yaw rate. (Zakka et al., 2025) `ev:reported` p. 2 ^zakka2025mujoco-008
- Madrona offers a CUDA software batch ray tracer, used for these experiments, and a Vulkan-based rasterizer as its two rendering backends. (Zakka et al., 2025) `ev:reported` p. 3 ^zakka2025mujoco-009
- Madrona is connected to MJX through low-level JAX primitives that work with JAX transformations such as jit and vmap. (Zakka et al., 2025) `ev:reported` p. 3 ^zakka2025mujoco-010
- The Madrona MJX integration allows [[Domain randomization|per-instance domain randomization]] of geometry size, color, lighting conditions and camera pose. (Zakka et al., 2025) `ev:reported` p. 3 ^zakka2025mujoco-011
- Deformable materials, moving lights and terrain height fields are not yet supported by the renderer and are planned for future work. (Zakka et al., 2025) `ev:asserted` p. 3 ^zakka2025mujoco-012
- State-based policies were trained for all ported DM Control Suite tasks, with most environments training in under 10 minutes on one GPU. (Zakka et al., 2025) `ev:measured` p. 3 ^zakka2025mujoco-013
- End-to-end pixel-based RL training on the DM Control Suite was demonstrated on only one task, CartpoleBalance. (Zakka et al., 2025) `ev:reported` p. 3 ^zakka2025mujoco-014
- The Go1 joystick policy was first trained on flat ground with restricted command ranges within 5 minutes on two RTX 4090 GPUs. (Zakka et al., 2025) `ev:measured` p. 4 ^zakka2025mujoco-015
- Joystick, handstand, footstand and fall recovery policies on the Go1 transferred to reality without additional fine-tuning, coping with uneven terrain. (Zakka et al., 2025) `ev:measured` p. 4 ^zakka2025mujoco-016
- Flat-ground humanoid training lasted under 15 minutes for the Berkeley Humanoid and under 30 minutes for the Unitree G1 and Booster T1. (Zakka et al., 2025) `ev:measured` p. 4 ^zakka2025mujoco-017
- The Berkeley Humanoid joystick policy tracked velocity commands on surfaces ranging from rigid floors to soft and slippery terrains. (Zakka et al., 2025) `ev:measured` p. 4 ^zakka2025mujoco-018
- On the Unitree G1 and Booster T1, the zero-shot policy achieved stable walking and turning on standard indoor floors. (Zakka et al., 2025) `ev:measured` p. 4 ^zakka2025mujoco-019
- The LEAP hand task reorients a 7 cm cube repeatedly from random poses to new SE(3) target orientations without dropping it. (Zakka et al., 2025) `ev:reported` p. 4 ^zakka2025mujoco-020
- The LEAP hand policy runs at 20 Hz with cube pose estimated from a single Intel RealSense D415 camera above the workspace. (Zakka et al., 2025) `ev:reported` p. 4 ^zakka2025mujoco-021
- In simulation, the in-hand cube reorientation policy trains within 30 min on two RTX 4090 GPUs with [[Domain randomization|domain randomization]]. (Zakka et al., 2025) `ev:measured` p. 4 ^zakka2025mujoco-022
- Over 10 hardware trials, the LEAP hand policy achieved a median of 3.5 and a mean of 7.1 consecutive rotations before failure. (Zakka et al., 2025) `ev:measured` p. 5 ^zakka2025mujoco-023
- The most frequent LEAP hand failure occurs when the cube becomes wedged between the fingers and the palm, stalling the policy. (Zakka et al., 2025) `ev:measured` p. 5 ^zakka2025mujoco-024
- The authors suggest that improved camera coverage and more accurate collision geometries could mitigate the observed in-hand failure cases. (Zakka et al., 2025) `ev:asserted` p. 5 ^zakka2025mujoco-025
- The non-prehensile Franka task counts a trial successful when the yoga block is within 3 cm and 10° of the goal pose. (Zakka et al., 2025) `ev:reported` p. 5 ^zakka2025mujoco-026
- The non-prehensile policy outputs motor torques for the arm's seven joints through direct torque control at 200 Hz with the gripper closed. (Zakka et al., 2025) `ev:reported` p. 5 ^zakka2025mujoco-027
- Training of the non-prehensile block policy used stochastic action and observation delays plus a curriculum that widens block displacement and orientation range. (Zakka et al., 2025) `ev:reported` p. 5 ^zakka2025mujoco-028
- In simulation, the non-prehensile yoga block reorientation policy takes 10 minutes to train on 16x A100 devices. (Zakka et al., 2025) `ev:measured` p. 5 ^zakka2025mujoco-029
- Across 35 hardware trials, the non-prehensile reorientation policy achieved a mean real success of 85.7 ± 12.2 percent. (Zakka et al., 2025) `ev:measured` p. 6 ^zakka2025mujoco-030
- On the Franka block task, median position error was 1.95 cm and median rotation error was 1.72 degrees across hardware trials. (Zakka et al., 2025) `ev:measured` p. 6 ^zakka2025mujoco-031
- The pick-cube vision policy maps a 64 × 64 RGB image to a Y-Z plane Cartesian command plus a binary jaw action. (Zakka et al., 2025) `ev:reported` p. 6 ^zakka2025mujoco-032
- The pixel-based pick-cube policy was trained with [[Domain randomization|visual domain randomization]] and a stochastic gripping delay of up to 250 ms. (Zakka et al., 2025) `ev:reported` p. 6 ^zakka2025mujoco-033
- Training the pixel-based pick-cube policy in simulation takes ten minutes on a single RTX 4090. (Zakka et al., 2025) `ev:measured` p. 6 ^zakka2025mujoco-034
- The pixel-based pick-cube policy achieved a 100% success rate in 12 real-world trials on the Franka Emika Panda. (Zakka et al., 2025) `ev:measured` p. 6 ^zakka2025mujoco-035
- The authors report the task can also be solved in full Cartesian or joint space given more camera perspectives and training samples. (Zakka et al., 2025) `ev:asserted` p. 6 ^zakka2025mujoco-036
- LeapCubeReorient training takes about 2080 seconds on one RTX 4090 and about 670 seconds on eight H100 GPUs. (Zakka et al., 2025) `ev:measured` p. 6 ^zakka2025mujoco-037
- With Madrona rendering, the Cartpole and Franka pixel environments unroll at roughly 403,000 and 37,000 steps per second respectively. (Zakka et al., 2025) `ev:measured` p. 6 ^zakka2025mujoco-038
- In PPO training, physics, rendering and inference comprise only 9% and 43% of Cartpole and Franka total training times. (Zakka et al., 2025) `ev:measured` p. 6 ^zakka2025mujoco-039
- The authors conclude the pixel-based training bottleneck shifts from collecting data to processing it in CNN policy updates. (Zakka et al., 2025) `ev:asserted` p. 7 ^zakka2025mujoco-040
- PPO agents trained with Brax and RSL-RL on Go1 joystick both reached successful rewards and gaits within similar wallclock times. (Zakka et al., 2025) `ev:measured` p. 7 ^zakka2025mujoco-041
- The PhysX GPU implementation behind IsaacGym and Isaac Lab is closed-source, which prevents researchers from extending the simulator. (Zakka et al., 2025) `ev:cited` p. 7 ^zakka2025mujoco-042
- Genesis provides an MJX-like rigid-body implementation in Taichi, but its sim-to-real results are still limited to a few locomotion policies. (Zakka et al., 2025) `ev:cited` p. 7 ^zakka2025mujoco-043
- Policies are typically trained with proprioceptive observations in simulation and then distilled offline into vision-based policies, according to prior work. (Zakka et al., 2025) `ev:cited` p. 7 ^zakka2025mujoco-044
- Playground inherits slow just-in-time compilation from MJX's JAX constraints, taking 1-3 minutes on Playground's tasks. (Zakka et al., 2025) `ev:measured` p. 7 ^zakka2025mujoco-045
- Contact computation time scales with the number of possible contacts rather than active contacts, due to JAX's static shape requirement. (Zakka et al., 2025) `ev:asserted` p. 7 ^zakka2025mujoco-046
- The authors state as a limitation that vision-based training using the Madrona renderer is still at an early stage. (Zakka et al., 2025) `ev:asserted` p. 7 ^zakka2025mujoco-047
- PPO and SAC were trained on all ported DM Control Suite environments across 5 seeds on a single A100 GPU. (Zakka et al., 2025) `ev:reported` p. 12 ^zakka2025mujoco-048
- Locomotion policy and value networks are three-layer MLPs with hidden sizes 512, 256 and 128 in an asymmetric actor-critic setup. (Zakka et al., 2025) `ev:reported` p. 18 ^zakka2025mujoco-049
- Locomotion policies are trained on flat terrain for 200 M timesteps and then finetuned on Perlin-noise rough terrain for 100 M timesteps. (Zakka et al., 2025) `ev:reported` p. 18 ^zakka2025mujoco-050
- For Go1JoystickFlatTerrain, different GPU devices and topologies made no material difference in training wallclock time. (Zakka et al., 2025) `ev:measured` p. 18 ^zakka2025mujoco-051
- Locomotion deployments use ros2-control in C++, with each policy inferenced at 50 Hz through ONNX Runtime. (Zakka et al., 2025) `ev:reported` p. 22 ^zakka2025mujoco-052
- The authors performed system identification on the LEAP hand's DYNAMIXEL servo, since the original LEAP simulation relied on manual parameter tuning. (Zakka et al., 2025) `ev:reported` p. 26 ^zakka2025mujoco-053
- The LEAP hand control frequency was reduced from 150 Hz to 20 Hz due to jitter in the low-level USB driver. (Zakka et al., 2025) `ev:reported` p. 26 ^zakka2025mujoco-054
- Block pose for the Franka task is fused from Alvar fiducial tags seen by four commodity RGB cameras around the workspace. (Zakka et al., 2025) `ev:reported` p. 28 ^zakka2025mujoco-055
- Early versions of the non-prehensile policy moved the block too quickly, exceeding the robot's force limit, which torque penalties addressed. (Zakka et al., 2025) `ev:measured` p. 28 ^zakka2025mujoco-056
- The authors report that roughly calibrating the Cartesian increment scale to the training scale drastically improves pick-cube [[Sim-to-real transfer|sim-to-real performance]]. (Zakka et al., 2025) `ev:measured` p. 30 ^zakka2025mujoco-057
- The authors state Madrona MJX batch rendering is competitive with IsaacLab and ManiSkill3, in a comparison they call only rough. (Zakka et al., 2025) `ev:measured` p. 32 ^zakka2025mujoco-058
- Madrona's rendering speed improvements appear to be the primary driver of the measured speed-ups, more than MJX's faster physics. (Zakka et al., 2025) `ev:measured` p. 32 ^zakka2025mujoco-059
- For CartpoleBalance with pixels, policy updates account for 0.91 of total training time per environment step. (Zakka et al., 2025) `ev:measured` p. 36 ^zakka2025mujoco-060
- For PandaPickCubeCartesian, policy updates take 0.57 of training time, with physics at 0.24 and rendering at 0.18. (Zakka et al., 2025) `ev:measured` p. 36 ^zakka2025mujoco-061

## 🎯 Contributions

## 📖 Glossary

- **MJX** — MuJoCo XLA, a JAX-based branch of MuJoCo that runs physics on GPU.
- **Madrona** — GPU entity-component-system with high-throughput batch rendering backends.
- **Batch rendering** — rendering many simulated environment instances in parallel on one device.
- **Sim-to-real transfer** — deploying a simulation-trained policy on physical hardware.
- **Zero-shot transfer** — deployment on hardware with no real-world fine-tuning.
- **Domain randomization** — randomizing simulation parameters in training so policies tolerate real-world variation.
- **Asymmetric actor-critic** — critic receives privileged uncorrupted observations that the actor does not.
- **Teacher-student distillation** — training a state-based policy first, then distilling it into a vision policy.
- **Non-prehensile manipulation** — moving objects by pushing, sliding or tapping rather than grasping.
- **Joystick task** — locomotion task tracking commanded linear velocities and yaw rate.

## ❓ Open questions

- How well does end-to-end pixel-based training in Playground extend beyond CartpoleBalance and the single Franka pick-cube task?
- Would topology-specific hyperparameters (e.g. more environments on larger GPU topologies) further reduce training time?
- Can migrating to Warp or Taichi remove the JAX static-shape contact scaling cost without losing throughput?
- Would multi-camera pose estimation reduce LEAP hand failures from occlusion and cube wedging?
- How does Madrona MJX rendering throughput compare with IsaacLab and ManiSkill3 in a fully controlled benchmark?
- Can the pick-cube policy be solved from pixels in full Cartesian or joint space with realistic sample budgets?
- Will deformable materials, moving lights and height fields in the renderer improve visual sim-to-real transfer?

## 📝 Notes on reading

Version read: arXiv 2502.08844v1 (12 Feb 2025), matching the packet identifier. The registry abstract gives the URL playground.mujoco.org, whereas the PDF abstract gives mujocoplayground.github.io.

Figure 7 (p. 6) prints bar labels "4.4e4 1.9e4" that do not obviously match the 403,000 and 37,000 steps per second stated in the text; the plotted FPS-vs-resolution curves could only be described. Figures 6, 8-16 and 21-24 are reward or throughput curves whose values were not claimed beyond numbers written in captions or text. Figures 23-24 (comparison with IsaacLab and ManiSkill3) carry no numbers in the extracted text.

Per-environment throughput tables (Tables IV, VII, IX) and hyperparameter tables (XII-XXXI) were not claimed cell by cell.

Inconsistency in Section C.4 (p. 26): the simulated environment is first described as sampling a new target on reaching a 0.4 rad tolerance, then as requiring 0.1 rad "as opposed to 0.4 rad in the real-world setup".

The Figure 16 caption names the environment LeapHandReorient while the text and Figure 6 use LeapCubeReorient. Section B.25 lists per-policy finetuning curricula (100 M + 50 M + 100 M timesteps for joystick) that sit awkwardly with the following sentence that all policies are trained for 200 M flat plus 100 M rough timesteps.

The main-text description of "high zero-shot success" for the non-prehensile task rests on Table II: median 100% but mean 85.7 ± 12.2% over 35 trials.

## Suggested new concepts

- GPU-accelerated physics simulation for RL — MJX, IsaacGym, Genesis and ManiSkill3 are recurring alternatives worth comparing in one note.
- Batch rendering for vision-based RL — Madrona-style on-device rendering removes teacher-student distillation and deserves its own concept.
- Sim-to-real transfer via domain randomization — a cross-paper technique used here for dynamics, sensors and visuals.
- Asymmetric actor-critic — privileged-critic training recurs in locomotion and dexterous manipulation papers.
- Direct torque control for sim-to-real manipulation — the 200 Hz torque recipe is presented as broadly useful to practitioners.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Entrenamiento masivo en GPU con MJX (alternativa en F.1).

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
