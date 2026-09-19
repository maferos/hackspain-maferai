---
aliases: []
type: concept
element_type: process
topic: "[[Visuomotor and vision-language-action robot policies]]"
topics: ["[[Visuomotor and vision-language-action robot policies]]"]
created: 2026-09-19
---

## Working definition

Deploying a policy or perception model trained in simulation on a physical robot, which works only insofar as the model survives the gap between simulated and real dynamics, sensing and appearance.

## Evidence

- [[Mittal2023orbit - Orbit A Unified Simulation Framework for Interactive Robot#^mittal2023orbit-016]] — Actuator models inject real-world characteristics such as delays or torque saturation, which can help sim-to-real transfer of control policies.
- [[Mittal2023orbit - Orbit A Unified Simulation Framework for Interactive Robot#^mittal2023orbit-045]] — The authors state that this sim-to-real transfer indicates the viability of the simulated contact dynamics for contact-rich tasks.
- [[Tobin2017domain - Domain Randomization for Transferring Deep Neural Networks#^tobin2017domain-005]] — The authors view sim-to-real transfer for object localization as a stepping stone to transferring general-purpose manipulation behaviors.
- [[Zakka2025mujoco - MuJoCo Playground#^zakka2025mujoco-001]] — The authors argue that iterative reward design makes time-to-robot critical, motivating fast simulation for sim-to-real reinforcement learning.
- [[Zakka2025mujoco - MuJoCo Playground#^zakka2025mujoco-057]] — The authors report that roughly calibrating the Cartesian increment scale to the training scale drastically improves pick-cube sim-to-real performance.
- [[Chen2025pi - pi_texttt{RL} Online RL Fine-tuning for Flow-based#^chen2025pi-065]] — Due to the low sample efficiency of online RL, the framework currently relies on sim-to-real deployment rather than real-world RL training.
- [[Ren2024diffusion - Diffusion Policy Policy Optimization (DPPO)#^ren2024diffusion-059]] — For sim-to-real transfer, noise with 0.03 standard deviation was added to DPPO's sampled actions to simulate an imperfect controller.
- [[Li2025simplevla - SimpleVLA-RL Scaling VLA Training via Reinforcement Learning#^li2025simplevla-052]] — Sim-to-real experiments run OpenVLA-OFT on two AgileX Piper robotic arms, with RDT serving as the baseline model.
- [[Lu2023markerless - Markerless Camera-to-Robot Pose Estimation via#^lu2023markerless-013]] — Instead of modelling domain distributions as domain adaptation does, the authors perform sim-to-real transfer by directly training on real-world data.
- [[Fang2022anygrasp - AnyGrasp Robust and Efficient Grasp Perception in Spatial#^fang2022anygrasp-058]] — The authors conclude that the frequently adopted sim-to-real technology in the grasping community is insufficient for their setting.
- [[Chanrungmaneekul2025arc - ARC-Calib Autonomous Markerless Camera-to-Robot Calibration#^chanrungmaneekul2025arc-004]] — The authors argue that models trained on synthetic data often require real-world finetuning to overcome the sim-to-real gap.
- [[Li2025labutopia - LabUtopia High-Fidelity Simulation and Hierarchical#^li2025labutopia-067]] — The authors state as a limitation that the benchmark operates entirely within simulation, leaving the sim-to-real gap for future work.
- [[Wyk2021geometric - Geometric Fabrics Generalizing Classical Mechanics to#^wyk2021geometric-047]] — The robot experiments were run only in simulation, the authors arguing that the sim-to-real gap is minimal for pure motion generation.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 11 sources · topic: Visuomotor and vision-language-action robot policies (drafter's packet `q7-policies-sim`, confirmed at the gate)
