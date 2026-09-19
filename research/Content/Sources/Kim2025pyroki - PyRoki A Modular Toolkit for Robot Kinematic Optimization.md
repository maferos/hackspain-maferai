---
aliases: []
type: "source"
title: "PyRoki: A Modular Toolkit for Robot Kinematic Optimization"
citekey: "Kim2025pyroki"
doi: "10.48550/arXiv.2505.03728"
arxiv: "2505.03728"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2505.03728"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Chung Min Kim", "Brent Yi", "Hongsuk Choi", "Yi Ma", "Ken Goldberg", "Angjoo Kanazawa"]
sha256: ["bb530aae518b8c378864d15760011f60453246397ff677f3fa9a8a77609aedb9"]
pdf: "Content/Papers/Kim2025pyroki.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 54
---

📄 PDF: [[Kim2025pyroki.pdf]]

> [!abstract] One-sentence summary
> PyRoki is an open-source JAX toolkit that expresses inverse kinematics, trajectory optimization and motion retargeting as composable variables and costs solved by one Levenberg-Marquardt optimizer on CPU, GPU or TPU, and its batched IK runs 1.4-1.7x faster than cuRobo with lower errors.

## Abstract

Robot motion can have many goals. Depending on the task, we might optimize for pose error, speed, collision, or similarity to a human demonstration. Motivated by this, we present PyRoki: a modular, extensible, and cross-platform toolkit for solving kinematic optimization problems. PyRoki couples an interface for specifying kinematic variables and costs with an efficient nonlinear least squares optimizer. Unlike existing tools, it is also cross-platform: optimization runs natively on CPU, GPU, and TPU. In this paper, we present (i) the design and implementation of PyRoki, (ii) motion retargeting and planning case studies that highlight the advantages of PyRoki's modularity, and (iii) optimization benchmarking, where PyRoki can be 1.4-1.7x faster and converges to lower errors than cuRobo, an existing GPU-accelerated inverse kinematics library. (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that existing kinematic optimization tools are fragmented, relying on task-specific C++ routines, CUDA kernels or analytical Jacobians. (Kim et al., 2025) `ev:asserted` p. 1 ^kim2025pyroki-001
- The authors state that low-level specialization tends to restrict existing kinematic optimizers to a single compute platform, either CPU or GPU operation. (Kim et al., 2025) `ev:asserted` p. 1 ^kim2025pyroki-002
- The core idea of PyRoki is that inverse kinematics, trajectory optimization and motion retargeting solve similar optimization problems that one toolkit can express. (Kim et al., 2025) `ev:asserted` p. 1 ^kim2025pyroki-003
- PyRoki provides an interface for specifying kinematic optimization problems through modular variable abstractions combined with composable cost function abstractions. (Kim et al., 2025) `ev:asserted` p. 1 ^kim2025pyroki-004
- PyRoki includes a web-based visualizer, built on viser, that lets users interactively tune cost weights and see the effect on robot motion. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025pyroki-005
- In the authors' feature comparison table, PyRoki is marked as supporting CPU, GPU and TPU, whereas no other listed tool supports TPU. (Kim et al., 2025) `ev:asserted` p. 2 ^kim2025pyroki-006
- In the feature comparison table, cuRobo is marked GPU but not CPU, while TracIK, pink, mink, TrajOpt, Dex-Retargeting and H2O are CPU but not GPU. (Kim et al., 2025) `ev:asserted` p. 2 ^kim2025pyroki-007
- The authors state that all PyRoki code is released under an open-source license and invite users to extend it. (Kim et al., 2025) `ev:reported` p. 2 ^kim2025pyroki-008
- PyRoki separates optimization variables from cost functions, which lets objectives like collision avoidance apply to several tasks without reimplementation. (Kim et al., 2025) `ev:asserted` p. 3 ^kim2025pyroki-009
- PyRoki computes Jacobians of user-defined cost functions by automatic differentiation, while also supporting analytical Jacobians when performance is critical. (Kim et al., 2025) `ev:reported` p. 3 ^kim2025pyroki-010
- PyRoki solves kinematic problems with a Levenberg-Marquardt optimizer that minimizes the weighted sum of squared cost residuals. (Kim et al., 2025) `ev:reported` p. 3 ^kim2025pyroki-011
- The PyRoki optimizer is built on JAX, a high-level array programming interface that enables parallelization on CPU, GPU and TPU. (Kim et al., 2025) `ev:reported` p. 3 ^kim2025pyroki-012
- For efficiency the optimizer automatically computes block-sparse Jacobian matrices, which the authors describe as particularly advantageous for temporally sparse motion planning problems. (Kim et al., 2025) `ev:asserted` p. 3 ^kim2025pyroki-013
- The PyRoki optimizer does not directly handle hard constraints, so joint limits and contact avoidance are represented as differentiable penalties. (Kim et al., 2025) `ev:reported` p. 3 ^kim2025pyroki-014
- PyRoki supports fixed, revolute and prismatic joints, along with the mimic joints commonly found in robot hands. (Kim et al., 2025) `ev:reported` p. 3 ^kim2025pyroki-015
- Kinematic variables in PyRoki can be composed with SE(3) and SO(3) Lie group variables for representing poses and orientations. (Kim et al., 2025) `ev:reported` p. 3 ^kim2025pyroki-016
- The joint pose cost in PyRoki penalizes the logarithm of the relative transform between the current joint pose and the target pose. (Kim et al., 2025) `ev:reported` p. 3 ^kim2025pyroki-017
- The joint limit cost penalizes joint values outside the upper and lower mechanical bounds with a hinge-shaped residual. (Kim et al., 2025) `ev:reported` p. 3 ^kim2025pyroki-018
- The joint regularization cost pulls the solution toward a user-defined default pose, since redundant robots such as 7-DoF arms reach multiple configurations. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025pyroki-019
- The smoothness cost penalizes the difference between consecutive joint configurations, and similar costs can be written for acceleration and jerk. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025pyroki-020
- The manipulability cost penalizes configurations near a singularity using the inverse of Yoshikawa's manipulability measure plus a small constant. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025pyroki-021
- Self and world collision costs convert signed distances between collision geometries into a smooth penalty with a buffer distance, following prior work. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025pyroki-022
- Writing inverse kinematics in PyRoki only requires importing the robot URDF and assembling joint pose, joint limit and regularization costs. (Kim et al., 2025) `ev:asserted` p. 4 ^kim2025pyroki-023
- In the UR5 trajectory optimization example, the trajectory uses the IK costs plus collision avoidance and acceleration and jerk minimization costs. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025pyroki-024
- The initial trajectory linearly interpolates between collision-free start and goal configurations found by inverse kinematics, and may initially be in collision. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025pyroki-025
- Continuous collision between timesteps is handled by connecting each UR5 collision sphere to its next-timestep counterpart to form capsules. (Kim et al., 2025) `ev:reported` p. 5 ^kim2025pyroki-026
- The authors note that the swept-capsule continuous collision cost can be implemented with only a few lines of Python. (Kim et al., 2025) `ev:asserted` p. 5 ^kim2025pyroki-027
- PyRoki's retargeting uses sparse keypoint-based costs that preserve relative distances and angles between joints, treating body and hand cases identically. (Kim et al., 2025) `ev:reported` p. 5 ^kim2025pyroki-028
- Full-body retargeting optimizes robot joint configurations together with learned per-link scaling factors to handle differences in limb proportions between embodiments. (Kim et al., 2025) `ev:reported` p. 5 ^kim2025pyroki-029
- The authors state that keypoint-position costs tend to bring humanoid feet too close together, so they preserve joint relationships instead. (Kim et al., 2025) `ev:cited` p. 5 ^kim2025pyroki-030
- Humanoid retargeting adds floor contact constraints, foot orientation costs, self-collision avoidance, joint limits and a cost keeping the knees apart. (Kim et al., 2025) `ev:reported` p. 5 ^kim2025pyroki-031
- The same motion transfer cost retargeted human motion to Unitree G1 and H1 humanoids of different heights, 127cm and 178cm. (Kim et al., 2025) `ev:reported` p. 5 ^kim2025pyroki-032
- Hand retargeting transfers MANO human hand motions from DexYCB to a Shadow Hand, adding a contact cost between hand and object surfaces. (Kim et al., 2025) `ev:reported` p. 5 ^kim2025pyroki-033
- All quantitative experiments were performed on a desktop PC with an AMD 5955WX CPU and an NVIDIA RTX 4090 GPU. (Kim et al., 2025) `ev:reported` p. 6 ^kim2025pyroki-034
- Re-implementing the Dex-Retargeting vector cost in PyRoki produced visually similar hand motions that capture the same semantic hand poses. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025pyroki-035
- On a human hand trajectory of 621 timesteps, the PyRoki re-implementation reached a keypoint cost of 0.068 ± 0.070, very similar to the original. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025pyroki-036
- The authors report that their global IK approach achieves slightly lower final keypoint costs than the original differential IK of Dex-Retargeting. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025pyroki-037
- For the Fetch mobile manipulator, PyRoki adds the SE(2) base pose as an optimization variable alongside the arm configuration. (Kim et al., 2025) `ev:reported` p. 6 ^kim2025pyroki-038
- A mobile-base IK solution counted as successful if position error was under 5mm and rotation error below 0.05 radians. (Kim et al., 2025) `ev:reported` p. 6 ^kim2025pyroki-039
- With a static base, IK reached a mean position error of 0.616 ± 0.600 m and a 24% success rate in Table II. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025pyroki-040
- Jointly optimizing the Fetch base pose reached a 100% success rate with mean position error of 5.40e-6 ± 4.31e-5 m. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025pyroki-041
- The authors argue that sequentially fixing a base pose before solving arm IK can fail when the chosen base makes the target unreachable. (Kim et al., 2025) `ev:asserted` p. 6 ^kim2025pyroki-042
- IK-Beam starts from 64 seeds, runs 6 parallel Levenberg-Marquardt steps, then keeps the 4 lowest-error seeds for 10 more steps. (Kim et al., 2025) `ev:reported` p. 6 ^kim2025pyroki-043
- On the Franka Panda, analytical Jacobians gave IK-Beam speedups ranging from 3x-19x over autodiff Jacobians across batch sizes and platforms. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025pyroki-044
- At batch size 2000, IK-Beam with analytical Jacobians took 32.8 ms on GPU versus 5534.7 ms on CPU. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025pyroki-045
- At batch size 1, IK-Beam with analytical Jacobians took 5.9 ms on CPU and 3.6 ms on GPU. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025pyroki-046
- The authors find that GPU parallelization helps IK-Beam runtime scale better with increasing batch sizes than CPU execution. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025pyroki-047
- Depending on batch size, IK-Beam implemented in PyRoki is between 1.4x and 1.7x faster than cuRobo for inverse kinematics. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025pyroki-048
- At batch size 1000, IK-Beam solved in 15.54 ms while cuRobo needed 26.37 ms on the Franka Panda benchmark. (Kim et al., 2025) `ev:measured` p. 7 ^kim2025pyroki-049
- On the Franka Panda benchmark at batch size 2000, cuRobo reached a 99.95% success rate while IK-Beam reached 100%. (Kim et al., 2025) `ev:measured` p. 7 ^kim2025pyroki-050
- IK-Beam converged to lower 98th-percentile position and orientation errors than cuRobo at every batch size in Table IV. (Kim et al., 2025) `ev:measured` p. 7 ^kim2025pyroki-051
- The authors believe the accuracy gain over cuRobo is mostly explained by the optimizer, since cuRobo uses L-BFGS while PyRoki uses Levenberg-Marquardt. (Kim et al., 2025) `ev:asserted` p. 6 ^kim2025pyroki-052
- The cuRobo comparison used a modified version of the official cuRobo benchmarking script, reporting 98th-percentile errors over all solutions in each batch. (Kim et al., 2025) `ev:reported` p. 7 ^kim2025pyroki-053
- The authors conclude that the same collision costs can be reused across inverse kinematics, trajectory optimization and humanoid motion retargeting in PyRoki. (Kim et al., 2025) `ev:asserted` p. 7 ^kim2025pyroki-054

## 🎯 Contributions


## 📖 Glossary

- **Inverse kinematics (IK)** — recovering a joint configuration that achieves a desired end-effector pose.
- **Trajectory optimization** — solving for a continuous sequence of joint configurations under costs such as smoothness and collision.
- **Motion retargeting** — transferring motion from a source embodiment, such as a human, to a different target robot.
- **Levenberg-Marquardt (LM)** — damped nonlinear least-squares solver interpolating between Gauss-Newton and gradient descent.
- **Block-sparse Jacobian** — Jacobian whose nonzeros form blocks, as when each timestep couples only to its neighbours.
- **Manipulability measure** — Yoshikawa's scalar measuring how far a configuration is from a kinematic singularity.
- **IK-Beam** — PyRoki's beam-search IK: 64 seeds, prune to best 4, 16 LM steps total.
- **Mimic joint** — joint whose position is a fixed function of another joint, common in robot hands.

## ❓ Open questions

- How does PyRoki handle problems needing hard constraints, given that constraints are only approximated by differentiable penalties?
- Is the accuracy advantage over cuRobo really due to LM versus L-BFGS, or to IK-Beam's seeding and pruning schedule?
- How does TPU performance compare with GPU and CPU? The paper claims TPU support but reports no TPU benchmark.
- How do the trajectory optimization and collision costs compare quantitatively with cuRobo or TrajOpt motion planning (success rate, time)?
- Do the retargeted humanoid and hand motions remain physically feasible when executed on real robots or in a dynamics simulator?

## 📝 Notes on reading

- Version read: arXiv v1 (2505.03728v1, 6 May 2025), matching the packet identifier.
- Inconsistency: the text on p. 6 says the static-base IK achieves "only a 15% success rate", while Table II on the same page gives a 24% success rate for the static base. Claims use the table value.
- The text says optimized-base mean position error is "under 0.005mm"; Table II gives 5.40e-6 m (about 0.0054 mm), slightly above that bound. Claimed the table value only.
- Table IV: the cuRobo position-error column has no unit in the extracted header while IK-Beam's is labelled mm; per-cell error values were not claimed individually.
- The collision activation function in Eq. (1) is partly garbled in the extraction; its piecewise form was described only qualitatively.
- Figures 1-5 (robot gallery, web viewer, UR5 trajectory, retargeting, Dex-Retargeting cost curve) were described only through their captions.
- Table I is a documented-feature comparison by the authors, not an experiment.
- The 1.4-1.7x speedup is stated in the text (p. 6); from Table IV the time ratios range roughly 1.40x to 1.70x across batch sizes.

## Suggested new concepts

- Composable cost functions for kinematic optimization — a design pattern shared by PyRoki, TrajOpt and cuRobo that unifies IK, planning and retargeting.
- Levenberg-Marquardt for inverse kinematics — the solver choice the authors credit for accuracy gains over L-BFGS.
- Keypoint-based motion retargeting — relative-distance and angle costs with per-link scaling, reusable across humanoids and hands.
- Cross-platform JAX robotics — running the same robotics optimizer on CPU, GPU and TPU.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H1.** Toolkit JAX (CPU/GPU/TPU) de IK, trayectorias y retargeting del autor de jaxlie; más rápido que cuRobo en IK según sus autores.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
