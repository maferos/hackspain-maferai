---
aliases: []
type: "source"
title: "Orbit: A Unified Simulation Framework for Interactive Robot Learning Environments"
citekey: "Mittal2023orbit"
doi: "10.48550/arXiv.2301.04195"
arxiv: "2301.04195"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2301.04195"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Mayank Mittal", "Calvin Yu", "Qinxi Yu", "Jingzhou Liu", "Nikita Rudin", "David Hoeller", "Jia Lin Yuan", "Ritvik Singh", "Yunrong Guo", "Hammad Mazhar", "Ajay Mandlekar", "Buck Babich", "Gavriel State", "Marco Hutter", "Animesh Garg"]
sha256: ["4e7171df4716689f182079687924cd776e0fc44fcac65d3c7da00c7a90298e36"]
pdf: "Content/Papers/Mittal2023orbit.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Mittal2023orbit.pdf]]

> [!abstract] One-sentence summary
> Orbit is an open-source, modular robot learning framework on NVIDIA Isaac Sim that bundles robots, sensors, motion generators and rigid and deformable benchmark tasks, and reports GPU-parallel throughput gains plus sim-to-real demonstrations on Franka and ANYmal-D.

## Abstract

We present Orbit, a unified and modular framework for robot learning powered by NVIDIA Isaac Sim. It offers a modular design to easily and efficiently create robotic environments with photo-realistic scenes and high-fidelity rigid and deformable body simulation. With Orbit, we provide a suite of benchmark tasks of varying difficulty -- from single-stage cabinet opening and cloth folding to multi-stage tasks such as room reorganization. To support working with diverse observations and action spaces, we include fixed-arm and mobile manipulators with different physically-based sensors and motion generators. Orbit allows training reinforcement learning policies and collecting large demonstration datasets from hand-crafted or expert solutions in a matter of minutes by leveraging GPU-based parallelization. In summary, we offer an open-sourced framework that readily comes with 16 robotic platforms, 4 sensor modalities, 10 motion generators, more than 20 benchmark tasks, and wrappers to 4 learning libraries. With this framework, we aim to support various research areas, including representation learning, reinforcement learning, imitation learning, and task and motion planning. We hope it helps establish interdisciplinary collaborations in these communities, and its modularity makes it easily extensible for more tasks and applications in the future. (arXiv)

## 🧠 Key ideas (atomic)

- Orbit is presented as a unified and modular open-source framework for robot learning that is built on NVIDIA Isaac Sim. (Mittal et al., 2023) `ev:asserted` p. 1 ^mittal2023orbit-001
- Simulators designed mainly for vision, such as Habitat or ManipulaTHOR, offer decent rendering throughput but simplify low-level interactions such as grasping. (Mittal et al., 2023) `ev:cited` p. 1 ^mittal2023orbit-002
- Physics simulators such as Isaac Gym or SAPIEN do not include physically-based rendering, deformable object simulation or ROS support out-of-the-box. (Mittal et al., 2023) `ev:cited` p. 1 ^mittal2023orbit-003
- The standardized benchmark suite comprises eleven rigid object manipulation, thirteen deformable object manipulation, and two locomotion environments. (Mittal et al., 2023) `ev:reported` p. 2 ^mittal2023orbit-004
- Table I lists Orbit with PhysX 5.1 as its physics engine and Omniverse RTX as its renderer. (Mittal et al., 2023) `ev:reported` p. 2 ^mittal2023orbit-005
- Orbit supports procedural generation, mesh scans and game-based interfaces as the three methods for designing scenes. (Mittal et al., 2023) `ev:reported` p. 2 ^mittal2023orbit-006
- A Material Point Method solver for cutting and plastic deformation of soft objects is currently under development for Orbit. (Mittal et al., 2023) `ev:asserted` p. 2 ^mittal2023orbit-007
- Prior robot learning frameworks built on MuJoCo or Bullet focus mainly on rigid object manipulation tasks. (Mittal et al., 2023) `ev:cited` p. 2 ^mittal2023orbit-008
- Frameworks on MuJoCo or Bullet need CPU clusters for massive parallelization, since their underlying physics engines are CPU-based. (Mittal et al., 2023) `ev:cited` p. 2 ^mittal2023orbit-009
- PhysX SDK 5 features GPU-based hardware acceleration, signed-distance field collision checking, and FEM-based solvers for deformable body simulation. (Mittal et al., 2023) `ev:cited` p. 2 ^mittal2023orbit-010
- Several existing frameworks use classic rasterization, which the authors say limits the photo-realism of the generated images. (Mittal et al., 2023) `ev:cited` p. 2 ^mittal2023orbit-011
- Recent frameworks with physically-based renderers mainly support camera-based sensors, which is insufficient for mobile robot applications needing LiDAR range sensors. (Mittal et al., 2023) `ev:cited` p. 2 ^mittal2023orbit-012
- Orbit's design comprises a World, analogous to the real world, and an Agent, the computation graph behind the embodied system. (Mittal et al., 2023) `ev:asserted` p. 3 ^mittal2023orbit-013
- Orbit includes command-line scripts that convert URDF, obj and stl assets into USD, automatically adding colliders and friction materials. (Mittal et al., 2023) `ev:reported` p. 3 ^mittal2023orbit-014
- The framework currently includes actuator models for two actuator types: Direct Control (DC) motors and Series Elastic Actuators (SEA). (Mittal et al., 2023) `ev:reported` p. 3 ^mittal2023orbit-015
- Actuator models inject real-world characteristics such as delays or torque saturation, which can help [[Sim-to-real transfer|sim-to-real transfer]] of control policies. (Mittal et al., 2023) `ev:asserted` p. 3 ^mittal2023orbit-016
- Orbit diverges from the Isaac Sim practice of updating every sensor at each simulation step, which causes overhead in parallelized scenes. (Mittal et al., 2023) `ev:asserted` p. 3 ^mittal2023orbit-017
- Each sensor instance has its own internal timer governing its reading frequency, and returns previously obtained values between timesteps. (Mittal et al., 2023) `ev:reported` p. 4 ^mittal2023orbit-018
- Agent nodes are either perception-based, turning inputs into another representation, or action-based, turning inputs into action commands. (Mittal et al., 2023) `ev:asserted` p. 4 ^mittal2023orbit-019
- Separating the task logic from the world lets the same world definition serve different tasks specified through extrinsic reward signals. (Mittal et al., 2023) `ev:asserted` p. 4 ^mittal2023orbit-020
- In the cube-lifting example, a task-space inverse kinematics controller typically runs at 50 Hz, below the 1000 Hz joint controller. (Mittal et al., 2023) `ev:cited` p. 4 ^mittal2023orbit-021
- Orbit supports 4 mobile platforms, 7 robotic arms, and 6 end-effectors that can be composed into systems such as legged mobile manipulators. (Mittal et al., 2023) `ev:reported` p. 4 ^mittal2023orbit-022
- The authors state that the right choice of necessary and sufficient tasks to demonstrate intelligent behaviors remains an open question. (Mittal et al., 2023) `ev:asserted` p. 4 ^mittal2023orbit-023
- Orbit currently supports Keyboard, Gamepad (Xbox controller) and Spacemouse devices for teleoperating the robot in real time. (Mittal et al., 2023) `ev:reported` p. 5 ^mittal2023orbit-024
- Orbit includes GPU-based implementations of differential IK, operational-space control, and joint-level control that compute commands for several robots. (Mittal et al., 2023) `ev:reported` p. 5 ^mittal2023orbit-025
- Orbit provides CPU implementations of RMPFlow for fixed-arm manipulators and OCS2 for whole-body control of mobile manipulators. (Mittal et al., 2023) `ev:reported` p. 5 ^mittal2023orbit-026
- Orbit includes pre-trained legged locomotion policies that track base velocity commands, to support traversability estimation and path-planning research. (Mittal et al., 2023) `ev:reported` p. 5 ^mittal2023orbit-027
- The current tasks mainly focus on skills such as grasping, screwing, stacking, pushing/pulling, pouring, folding, and walking. (Mittal et al., 2023) `ev:reported` p. 5 ^mittal2023orbit-028
- Orbit provides reinforcement learning wrappers to rl-games, RSL-rl, and stable-baselines-3, making the underlying environment agnostic to the RL framework. (Mittal et al., 2023) `ev:reported` p. 5 ^mittal2023orbit-029
- Although PPO parameter settings were kept the same, the RL frameworks differed in performance and training time due to implementation differences. (Mittal et al., 2023) `ev:measured` p. 5 ^mittal2023orbit-030
- With 2048 environments, the GPU-optimized RSL-rl and rl-games frameworks reached a training speed of 50,000-75,000 frames per second. (Mittal et al., 2023) `ev:measured` p. 5 ^mittal2023orbit-031
- Training with stable-baselines3 reached 6,000-18,000 FPS, lower than the GPU-optimized RSL-rl and rl-games frameworks in the same comparison. (Mittal et al., 2023) `ev:measured` p. 5 ^mittal2023orbit-032
- Orbit can store teleoperated demonstration data in the format used by robomimic for training imitation learning models. (Mittal et al., 2023) `ev:reported` p. 5 ^mittal2023orbit-033
- For Franka-LiftCube, 2000 trajectories were collected for each of four settings of fixed or random start and desired positions. (Mittal et al., 2023) `ev:reported` p. 5 ^mittal2023orbit-034
- Trained on these demonstrations, BC and BC-RNN both reached a success rate of 1.00 on Franka-LiftCube with an unchanged evaluation setup. (Mittal et al., 2023) `ev:measured` p. 6 ^mittal2023orbit-035
- When goal states changed, BC reached a success rate of 0.89 on Franka-LiftCube, whereas BC-RNN kept 1.00. (Mittal et al., 2023) `ev:measured` p. 6 ^mittal2023orbit-036
- When initial states changed, BC reached a success rate of 0.47 against 0.88 for BC-RNN over 100 trials. (Mittal et al., 2023) `ev:measured` p. 6 ^mittal2023orbit-037
- When both initial and goal states changed, BC reached a success rate of 0.43 against 0.87 for BC-RNN. (Mittal et al., 2023) `ev:measured` p. 6 ^mittal2023orbit-038
- In interactive motion planning, the user selects an object in the GUI and previews grasp poses and RMP-generated robot motion sequences. (Mittal et al., 2023) `ev:reported` p. 6 ^mittal2023orbit-039
- Joint commands are sent over ZMQ to the Franka computer, where a quintic interpolator upsamples 60 Hz simulator commands to 1000 Hz. (Mittal et al., 2023) `ev:reported` p. 6 ^mittal2023orbit-040
- Real Franka experiments used two configurations, one with the Franka Emika hand and one with an Allegro hand, each with three tasks. (Mittal et al., 2023) `ev:reported` p. 6 ^mittal2023orbit-041
- The ANYmal-D locomotion policy was trained entirely in simulation using an actuator network for the legged base. (Mittal et al., 2023) `ev:reported` p. 6 ^mittal2023orbit-042
- To make the locomotion policy robust, training randomized the ANYmal-D base mass within a range of 22 ± 5 kg. (Mittal et al., 2023) `ev:reported` p. 6 ^mittal2023orbit-043
- On the ANYmal-D robot, the policy trained in simulation runs at 50 Hz, with the actuator net functioning at 200 Hz. (Mittal et al., 2023) `ev:reported` p. 7 ^mittal2023orbit-044
- The authors state that this [[Sim-to-real transfer|sim-to-real transfer]] indicates the viability of the simulated contact dynamics for contact-rich tasks. (Mittal et al., 2023) `ev:asserted` p. 7 ^mittal2023orbit-045
- Deformable body accuracy was tested with a clamped beam of silicone elastomer tracked by motion capture markers under gravity. (Mittal et al., 2023) `ev:reported` p. 7 ^mittal2023orbit-046
- Damped oscillations in the simulated clamped-beam data follow closely the collected real-world data, which indicates potential for sim-to-real deformable manipulation. (Mittal et al., 2023) `ev:measured` p. 7 ^mittal2023orbit-047
- Throughput comparisons ran on a workstation with a 16-core AMD Ryzen 5950X, 64 GB RAM, and an NVIDIA 3090RTX. (Mittal et al., 2023) `ev:reported` p. 7 ^mittal2023orbit-048
- For a fair comparison, the environments were adapted to share the same action space, simulation frequency, and control decimation. (Mittal et al., 2023) `ev:reported` p. 7 ^mittal2023orbit-049
- In the throughput tests, CPU-vectorized frameworks crashed due to insufficient memory at around 200-300 environments. (Mittal et al., 2023) `ev:measured` p. 7 ^mittal2023orbit-050
- GPU-based parallelization in Orbit achieved a throughput ∼10x faster than CPU-vectorized frameworks for rigid body environments. (Mittal et al., 2023) `ev:measured` p. 7 ^mittal2023orbit-051
- GPU-based parallelization in Orbit achieved a throughput ∼3x faster than DEDO for the deformable cloth-hanging environment. (Mittal et al., 2023) `ev:measured` p. 7 ^mittal2023orbit-052
- Orbit performs at par with IsaacGym in rigid-body simulation throughput, since both use the same physics engine. (Mittal et al., 2023) `ev:measured` p. 7 ^mittal2023orbit-053
- In the cloth hanging task, increasing the number of points in the cloth mesh adversely affects Orbit's throughput. (Mittal et al., 2023) `ev:measured` p. 7 ^mittal2023orbit-054
- The authors observe that a higher cloth mesh resolution produces more accurate simulation but requires more computation time. (Mittal et al., 2023) `ev:measured` p. 7 ^mittal2023orbit-055
- In their future work section, the authors state that Orbit can simulate physics at up to 125,000 FPS. (Mittal et al., 2023) `ev:asserted` p. 8 ^mittal2023orbit-056
- Camera rendering is currently bottlenecked to a total of 270 FPS for ten cameras rendering 640 × 480 images on an RTX 3090. (Mittal et al., 2023) `ev:measured` p. 8 ^mittal2023orbit-057
- Quantitatively studying the fidelity of the entire simulator, including rendering, sensors and physics, remains an area for future exploration. (Mittal et al., 2023) `ev:asserted` p. 8 ^mittal2023orbit-058
- The authors plan to support loading assets directly in native formats such as URDF and OBJ instead of USD. (Mittal et al., 2023) `ev:asserted` p. 8 ^mittal2023orbit-059
- The authors state that IsaacGymEnvs and OmniIsaacGymEnvs are limited in integration with RL libraries beyond RL-Games. (Mittal et al., 2023) `ev:asserted` p. 9 ^mittal2023orbit-060
- According to the authors, Isaac Gym does not include deformable-rigid interaction, high-fidelity rendering, or support for ROS. (Mittal et al., 2023) `ev:asserted` p. 9 ^mittal2023orbit-061

## 🎯 Contributions

## 📖 Glossary

- **USD (Universal Scene Description)** — Hierarchical file format used in Omniverse to store assets, materials and attributes.
- **Actuator model** — Model injecting real actuator effects, such as delays or torque saturation, into simulation.
- **Series Elastic Actuator (SEA)** — Actuator with an elastic element between motor and load.
- **Differential IK** — Inverse kinematics mapping desired end-effector pose changes to joint position commands.
- **Operational-space control (OSC)** — Task-space controller computing joint torques from desired end-effector dynamics.
- **Control decimation** — Number of physics steps per control step.
- **PBD** — Position-based dynamics, a particle solver used here for cloth.
- **FEM** — Finite-element method, used by PhysX 5 for stable deformable body simulation.
- **ZMQ (ZeroMQ)** — Lightweight messaging library used to stream joint commands to a real robot.

## ❓ Open questions

- How faithful is the full simulator (rendering, sensors, physics) when measured quantitatively rather than by qualitative rollouts?
- Can camera rendering throughput approach the physics throughput, beyond 270 FPS for ten 640 × 480 cameras?
- Which set of tasks is necessary and sufficient to demonstrate intelligent behavior?
- How should mesh resolution be tuned to trade cloth simulation accuracy against throughput?
- How well do rigid-body manipulation policies trained in Orbit transfer to hardware beyond the showcased Franka tasks?

## 📝 Notes on reading

The cached text is arXiv v2 (16 Feb 2024) of 2301.04195; the packet identifier is the arXiv record. Table I (p. 2) is garbled in extraction: header columns and row values no longer align (rows carry 15 values against 16 feature columns), so no per-feature comparison was claimed beyond Orbit's engine and renderer. Fig. 7 (RL return curves), Fig. 11 (clamped beam), Fig. 12 and Fig. 13 (throughput curves) could only be described from their captions and text. Inconsistencies: the abstract names 16 robotic platforms, while Sec. IV lists 4 mobile platforms, 7 arms and 6 end-effectors (17); the abstract says wrappers to 4 learning libraries, while Sec. V-A names three RL wrappers plus robomimic data export; the abstract says more than 20 benchmark tasks, while the contributions list 11 + 13 + 2 = 26.

## Suggested new concepts

- GPU-parallel robot simulation — central to Orbit, Isaac Gym and ManiSkill2 throughput comparisons.
- Actuator network — learned actuator model used for sim-to-real legged locomotion.
- Sim-to-real transfer — recurring evaluation axis for simulation frameworks.
- Deformable object simulation (FEM vs PBD) — solver choice drives fidelity and throughput trade-offs.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H7.** Artículo de referencia de Isaac Lab (antes Orbit): entornos de manipulación, sensores y aprendizaje paralelo en GPU; base del port IsaacLab-mlx del equipo.
