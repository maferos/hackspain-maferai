---
aliases: []
type: concept
element_type: method
topic: "[[Visuomotor and vision-language-action robot policies]]"
topics: ["[[Visuomotor and vision-language-action robot policies]]"]
created: 2026-09-19
---

## Working definition

Training on many simulated environments with randomized textures, lighting, camera, geometry or dynamics, so that the real world looks like just another variation and a model trained only in simulation transfers.

## Evidence

- [[Tobin2017domain - Domain Randomization for Transferring Deep Neural Networks#^tobin2017domain-003]] — Domain randomization trains a model on many randomized simulated environments instead of a single simulated environment to expose it to wide variability.
- [[Tobin2017domain - Domain Randomization for Transferring Deep Neural Networks#^tobin2017domain-004]] — The work focuses on transferring from low-fidelity simulated camera images, although domain randomization could in principle apply to any reality-gap component.
- [[Tobin2017domain - Domain Randomization for Transferring Deep Neural Networks#^tobin2017domain-054]] — The authors infer that in the low data regime, texture randomization is more important than object position randomization.
- [[Tobin2017domain - Domain Randomization for Transferring Deep Neural Networks#^tobin2017domain-066]] — The authors suggest domain randomization could be an important tool for making deep reinforcement learning policies useful on real robots.
- [[Labbe2020cosypose - CosyPose Consistent multi-view multi-object 6D pose#^labbe2020cosypose-021]] — On T-LESS, synthetic images are generated from CAD models only, with random textures following prior work on domain randomization.
- [[Chanrungmaneekul2025arc - ARC-Calib Autonomous Markerless Camera-to-Robot Calibration#^chanrungmaneekul2025arc-008]] — Rendering-based markerless calibration methods often rely on domain-randomized synthetic training data to enable robot pose estimation in the real world.
- [[Li2025simplevla - SimpleVLA-RL Scaling VLA Training via Reinforcement Learning#^li2025simplevla-020]] — RoboTwin2.0 experiments use the Agilex Piper robotic arm with domain-randomized settings, evaluating each task on 100 held-out test scenarios.
- [[Zakka2025mujoco - MuJoCo Playground#^zakka2025mujoco-011]] — The Madrona MJX integration allows per-instance domain randomization of geometry size, color, lighting conditions and camera pose.
- [[Zakka2025mujoco - MuJoCo Playground#^zakka2025mujoco-022]] — In simulation, the in-hand cube reorientation policy trains within 30 min on two RTX 4090 GPUs with domain randomization.
- [[Zakka2025mujoco - MuJoCo Playground#^zakka2025mujoco-033]] — The pixel-based pick-cube policy was trained with visual domain randomization and a stochastic gripping delay of up to 250 ms.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: extra (5 sources) · topic: Visuomotor and vision-language-action robot policies (drafter's packet `q7-policies-sim`, confirmed at the gate)
