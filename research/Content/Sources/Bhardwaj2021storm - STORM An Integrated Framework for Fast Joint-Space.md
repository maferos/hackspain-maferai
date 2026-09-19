---
aliases: []
type: "source"
title: "STORM: An Integrated Framework for Fast Joint-Space Model-Predictive Control for Reactive Manipulation"
citekey: "Bhardwaj2021storm"
doi: "10.48550/arXiv.2104.13542"
arxiv: "2104.13542"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2104.13542"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Mohak Bhardwaj", "Balakumar Sundaralingam", "Arsalan Mousavian", "Nathan Ratliff", "Dieter Fox", "Fabio Ramos", "Byron Boots"]
sha256: ["d977ff6dab9f4baa2d7ea1dc2d35596bfc094ab797b5478e5f9a4a3c7cb596b6"]
pdf: "Content/Papers/Bhardwaj2021storm.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Bhardwaj2021storm.pdf]]

> [!abstract] One-sentence summary
> STORM runs sampling-based MPC in a manipulator's joint space on a GPU, using tensorized kinematic rollouts, Halton and B-spline sampling and learned collision costs to control a real Franka Panda reactively at roughly 100 Hz.

## Abstract

Sampling-based model-predictive control (MPC) is a promising tool for feedback control of robots with complex, non-smooth dynamics, and cost functions. However, the computationally demanding nature of sampling-based MPC algorithms has been a key bottleneck in their application to high-dimensional robotic manipulation problems in the real world. Previous methods have addressed this issue by running MPC in the task space while relying on a low-level operational space controller for joint control. However, by not using the joint space of the robot in the MPC formulation, existing methods cannot directly account for non-task space related constraints such as avoiding joint limits, singular configurations, and link collisions. In this paper, we develop a system for fast, joint space sampling-based MPC for manipulators that is efficiently parallelized using GPUs. Our approach can handle task and joint space constraints while taking less than 8ms~(125Hz) to compute the next control command. Further, our method can tightly integrate perception into the control problem by utilizing learned cost functions from raw sensor data. We validate our approach by deploying it on a Franka Panda robot for a variety of dynamic manipulation tasks. We study the effect of different cost formulations and MPC parameters on the synthesized behavior and provide key insights that pave the way for the application of sampling-based MPC for manipulators in a principled manner. We also provide highly optimized, open-source code to be used by the wider robot learning and control community. Videos of experiments can be found at: https://sites.google.com/view/manipulation-mpc (arXiv)

## 🧠 Key ideas (atomic)

- Operational-space control methods are inherently local because they only optimize for the next time step, ignoring future actions or states. (Bhardwaj et al., 2021) `ev:asserted` p. 1 ^bhardwaj2021storm-001
- Existing joint-space MPC methods for manipulators are limited to gradient-based approaches, which require differentiable cost and dynamics. (Bhardwaj et al., 2021) `ev:cited` p. 1 ^bhardwaj2021storm-002
- Sampling-based methods such as [[Model Predictive Path Integral control|MPPI]] and CEM make no restrictive assumptions about the cost, dynamics or policy class. (Bhardwaj et al., 2021) `ev:cited` p. 2 ^bhardwaj2021storm-003
- A major criticism of sampling-based MPC for full joint-space control has been its inability to produce smooth, low-jerk trajectories. (Bhardwaj et al., 2021) `ev:cited` p. 2 ^bhardwaj2021storm-004
- STORM, Stochastic Tensor Optimization for Robot Motion, implements a highly parallelized sampling-based MPC control architecture for high-dimensional robots like manipulators. (Bhardwaj et al., 2021) `ev:asserted` p. 2 ^bhardwaj2021storm-005
- The authors claim their implementation reaches a 125Hz control rate on a single GPU, a 100x speedup over existing MPPI manipulation implementations. (Bhardwaj et al., 2021) `ev:asserted` p. 2 ^bhardwaj2021storm-006
- The MPC optimization is hot-started from the previous timestep's solution with a shift operator, usually needing one iteration in practice. (Bhardwaj et al., 2021) `ev:reported` p. 3 ^bhardwaj2021storm-007
- The mean of the Gaussian policy is updated with the same equation as the [[Model Predictive Path Integral control|Model-Predictive Path Integral Control]] algorithm. (Bhardwaj et al., 2021) `ev:reported` p. 4 ^bhardwaj2021storm-008
- [[Model Predictive Path Integral control|Standard implementations of MPPI]] on real systems generally do not update the covariance of the sampling distribution. (Bhardwaj et al., 2021) `ev:cited` p. 4 ^bhardwaj2021storm-009
- The authors observed that updating the covariance leads to better performance with fewer particles, such as stable behavior upon convergence to the goal. (Bhardwaj et al., 2021) `ev:asserted` p. 4 ^bhardwaj2021storm-010
- STORM uses the manipulator's kinematic model as its approximate transition model, with joint accelerations as the commanded action. (Bhardwaj et al., 2021) `ev:reported` p. 4 ^bhardwaj2021storm-011
- States across the whole batch and horizon are computed by one tensor operation instead of iterating over horizon steps. (Bhardwaj et al., 2021) `ev:reported` p. 5 ^bhardwaj2021storm-012
- The authors state that this tensorized state computation is key to achieving the 8ms control latency. (Bhardwaj et al., 2021) `ev:asserted` p. 5 ^bhardwaj2021storm-013
- The stop cost penalizes joint velocities that would prevent the robot from stopping within the horizon under a user-specified maximum acceleration. (Bhardwaj et al., 2021) `ev:reported` p. 5 ^bhardwaj2021storm-014
- A manipulability cost term penalizes small manipulability scores to encourage control policies that avoid future kinematic singularities. (Bhardwaj et al., 2021) `ev:reported` p. 6 ^bhardwaj2021storm-015
- Self-collision distance is predicted by a neural network, jointNERF, with three layers of [256, 128, 64] neurons. (Bhardwaj et al., 2021) `ev:reported` p. 6 ^bhardwaj2021storm-016
- The authors found that positional encoding of joint angles as sine and cosine improves the accuracy of self-collision distance prediction. (Bhardwaj et al., 2021) `ev:asserted` p. 6 ^bhardwaj2021storm-017
- The environment collision cost uses a learned classifier from Danielczuk et al. that operates directly on raw pointcloud data. (Bhardwaj et al., 2021) `ev:reported` p. 6 ^bhardwaj2021storm-018
- The sampling-based approach can handle discrete costs, so collision avoidance is explored without using signed distance fields. (Bhardwaj et al., 2021) `ev:asserted` p. 6 ^bhardwaj2021storm-019
- Control samples are drawn once from a Halton sequence and then transformed by the current Gaussian policy mean and covariance. (Bhardwaj et al., 2021) `ev:reported` p. 7 ^bhardwaj2021storm-020
- Comb filtering of sampled controls does not guarantee smooth trajectories, as neighboring horizon samples can differ greatly in magnitude. (Bhardwaj et al., 2021) `ev:asserted` p. 7 ^bhardwaj2021storm-021
- The proposed smoothing fits degree-3 B-splines to Halton-sampled controls, then sub-samples the curve at finer resolution to obtain joint accelerations. (Bhardwaj et al., 2021) `ev:reported` p. 7 ^bhardwaj2021storm-022
- On a planar reacher task, Halton B-spline sampling found a smooth short path, whereas random B-spline sampling took a longer path. (Bhardwaj et al., 2021) `ev:measured` p. 7 ^bhardwaj2021storm-023
- A per-joint covariance lets each joint's sampling variance adapt independently, instead of one scalar covariance shared across all dimensions. (Bhardwaj et al., 2021) `ev:reported` p. 7 ^bhardwaj2021storm-024
- A set of zero-acceleration null particles lets the robot coast at constant velocity and easily stop at the goal. (Bhardwaj et al., 2021) `ev:reported` p. 7 ^bhardwaj2021storm-025
- When the tracked ball was moved to unreachable positions among obstacles, the robot prioritized collision avoidance over accurate pose reaching. (Bhardwaj et al., 2021) `ev:measured` p. 8 ^bhardwaj2021storm-026
- Under an end-effector orientation constraint while tracking a ball, the controller achieved a median quaternion error of 1.2485%. (Bhardwaj et al., 2021) `ev:measured` p. 8 ^bhardwaj2021storm-027
- The ball-balancing task uses a simplified rolling model that ignores friction and ball inertia, without any system identification. (Bhardwaj et al., 2021) `ev:reported` p. 8 ^bhardwaj2021storm-028
- Across 10 ball-balancing trials, the MPC framework achieved a median error of 3.9 cm in centring the ball on the tray. (Bhardwaj et al., 2021) `ev:measured` p. 9 ^bhardwaj2021storm-029
- The robot did not drop the ball in any of the 10 ball-balancing trials on the real Franka Panda. (Bhardwaj et al., 2021) `ev:measured` p. 9 ^bhardwaj2021storm-030
- The authors conclude that accurate, reactive manipulation can be obtained with relatively simple models and intuitive cost functions within MPC. (Bhardwaj et al., 2021) `ev:asserted` p. 9 ^bhardwaj2021storm-031
- Operation space controllers are among the fastest feedback control algorithms, with methods achieving control latency of 1-2 ms. (Bhardwaj et al., 2021) `ev:cited` p. 9 ^bhardwaj2021storm-032
- Most online replanning methods on high-dimensional systems run with control latencies between 140ms and 1000ms. (Bhardwaj et al., 2021) `ev:cited` p. 10 ^bhardwaj2021storm-033
- Gradient-based joint-space MPC methods that work on real manipulation systems have control latencies in the range 20ms - 125ms. (Bhardwaj et al., 2021) `ev:cited` p. 10 ^bhardwaj2021storm-034
- The learned-collision replanning approach of Danielczuk et al. has a much larger control latency, of 1000 ms, according to the authors. (Bhardwaj et al., 2021) `ev:cited` p. 10 ^bhardwaj2021storm-035
- Hyatt et al. showed that GPU-parallelized sampling-based MPC can run at 200Hz even with a large number of dimensions. (Bhardwaj et al., 2021) `ev:cited` p. 10 ^bhardwaj2021storm-036
- The authors note that at higher speeds the kinematic model might induce significant model bias in the controller. (Bhardwaj et al., 2021) `ev:asserted` p. 11 ^bhardwaj2021storm-037
- The authors suggest that learning a residual dynamics model or a terminal Q-function could mitigate model bias while keeping computation fast. (Bhardwaj et al., 2021) `ev:asserted` p. 11 ^bhardwaj2021storm-038
- The authors suggest performance could be made more robust by directly accounting for state uncertainty in the control loop. (Bhardwaj et al., 2021) `ev:asserted` p. 11 ^bhardwaj2021storm-039
- The MPC pipeline is implemented in PyTorch, with all cost terms and update equations implemented in a batched fashion. (Bhardwaj et al., 2021) `ev:reported` p. 15 ^bhardwaj2021storm-040
- MPC acceleration commands are evaluated at 100Hz and sent to a custom low-level torque controller running at 1000Hz. (Bhardwaj et al., 2021) `ev:reported` p. 15 ^bhardwaj2021storm-041
- The authors found the joint velocity noise read from libfranka prohibitive for precise control with MPC on the real robot. (Bhardwaj et al., 2021) `ev:asserted` p. 15 ^bhardwaj2021storm-042
- A joint state filter predicts the state from the previous commanded acceleration, then incorporates sensor readings with an exponential moving average. (Bhardwaj et al., 2021) `ev:reported` p. 15 ^bhardwaj2021storm-043
- The scene pointcloud is computed once at the start of each run, since only static scenes are considered in this work. (Bhardwaj et al., 2021) `ev:reported` p. 15 ^bhardwaj2021storm-044
- In the latency comparison table, STORM is listed with a control latency of 10 ms and a horizon of 30 steps. (Bhardwaj et al., 2021) `ev:measured` p. 16 ^bhardwaj2021storm-045
- Pose reaching was compared against RRTConnect and RRTStar planners via MoveIt and the Manipulability Motion Control operational space controller. (Bhardwaj et al., 2021) `ev:reported` p. 16 ^bhardwaj2021storm-046
- Manipulability Motion Control was unable to reach a pose requiring a large orientation change, repeatedly resulting in self collisions. (Bhardwaj et al., 2021) `ev:measured` p. 16 ^bhardwaj2021storm-047
- Both STORM and the MoveIt baselines were able to reach the pose requiring a large change in end-effector orientation. (Bhardwaj et al., 2021) `ev:measured` p. 17 ^bhardwaj2021storm-048
- On the remaining poses, STORM reached a median position error of 4.822 mm, worse than every baseline in the comparison. (Bhardwaj et al., 2021) `ev:measured` p. 17 ^bhardwaj2021storm-049
- In pose reaching, STORM's median quaternion error was 0.4619%, compared with 0.00267923% for the Manipulability Motion Control baseline. (Bhardwaj et al., 2021) `ev:measured` p. 17 ^bhardwaj2021storm-050
- Path lengths and maximum joint velocities of STORM were comparable to the baselines in the pose reaching comparison. (Bhardwaj et al., 2021) `ev:measured` p. 17 ^bhardwaj2021storm-051
- The authors attribute STORM's lower pose accuracy to its lower-level controller, which was not tuned extensively. (Bhardwaj et al., 2021) `ev:asserted` p. 17 ^bhardwaj2021storm-052
- In simulated reaching, increasing the number of particles gave a more accurate median position error with a tighter confidence interval. (Bhardwaj et al., 2021) `ev:measured` p. 17 ^bhardwaj2021storm-053
- The sampling strategy generated smooth, low-jerk motions even with 200 particles in the simulated particle-count ablation. (Bhardwaj et al., 2021) `ev:measured` p. 18 ^bhardwaj2021storm-054
- With the self-collision cost used, the robot never entered self collision on colliding targets, at the cost of not reaching the goal. (Bhardwaj et al., 2021) `ev:measured` p. 18 ^bhardwaj2021storm-055
- Without the self-collision cost, at weight 0, the robot spent 2730 timesteps in self collision on colliding target poses. (Bhardwaj et al., 2021) `ev:measured` p. 19 ^bhardwaj2021storm-056
- Joint limit violations fell from 1624 timesteps at weight 0 to zero at joint-limit cost weights of 500 and above. (Bhardwaj et al., 2021) `ev:measured` p. 19 ^bhardwaj2021storm-057
- Increasing the manipulability cost weight improved pose reaching accuracy in 10 simulated runs, up to a certain threshold. (Bhardwaj et al., 2021) `ev:measured` p. 19 ^bhardwaj2021storm-058
- Beyond a certain weight threshold, the manipulability cost interfered with pose reaching, and position accuracy decreased. (Bhardwaj et al., 2021) `ev:measured` p. 19 ^bhardwaj2021storm-059
- A lower weight on the stop cost led to undesirable oscillations near the goal in simulated pose reaching. (Bhardwaj et al., 2021) `ev:measured` p. 19 ^bhardwaj2021storm-060
- With 100 particles, pseudo-random sampling with comb filter could not keep the quaternion error confidence interval within 5%. (Bhardwaj et al., 2021) `ev:measured` p. 19 ^bhardwaj2021storm-061
- In the sampling ablation, Halton sampling achieved less than 5% quaternion error with both 100 and 500 particles. (Bhardwaj et al., 2021) `ev:measured` p. 19 ^bhardwaj2021storm-062
- The very strong comb filtering required for low-jerk motion prevents the robot from ramping up its joint velocity. (Bhardwaj et al., 2021) `ev:measured` p. 21 ^bhardwaj2021storm-063
- Fitting B-splines to sampled actions allows smooth velocity ramp-up but comes at the price of reduced pose accuracy. (Bhardwaj et al., 2021) `ev:measured` p. 21 ^bhardwaj2021storm-064
- A mixed strategy of 0.6 B-spline and 0.4 comb-filtered samples gave accuracy comparable to comb filtering with high joint velocities. (Bhardwaj et al., 2021) `ev:measured` p. 21 ^bhardwaj2021storm-065
- The learned self-collision detector is over 40x faster on average than a baseline using forward kinematics and link distances. (Bhardwaj et al., 2021) `ev:measured` p. 21 ^bhardwaj2021storm-066
- The learned self-collision detector maintains a latency of 0.4-0.6ms even for large batch sizes of query configurations. (Bhardwaj et al., 2021) `ev:measured` p. 21 ^bhardwaj2021storm-067
- The tensorized GPU forward model is over 5x faster than a CPU baseline across horizons with 500 particles. (Bhardwaj et al., 2021) `ev:measured` p. 21 ^bhardwaj2021storm-068

## 🎯 Contributions


## 📖 Glossary

- **MPPI** — Model-Predictive Path Integral control: sampling-based MPC weighting rollouts by exponentiated cost.
- **CEM** — Cross-Entropy Method: iteratively refits a sampling distribution to the lowest-cost samples.
- **Operational-space control (OSC)** — Task-space costs projected into joint space through the Jacobian, optimizing one step.
- **Halton sequence** — Low-discrepancy quasi-random sequence built from prime bases for more uniform sampling.
- **Comb filter** — Weighted sum of neighbouring control samples along the horizon to smooth trajectories.
- **Manipulability score** — Volume of the Jacobian ellipsoid; collapses to zero at kinematic singularities.
- **Null particles** — Fixed zero-acceleration control sequences added to the sampled batch.
- **Stop cost** — Penalty on joint velocities too high to stop within the MPC horizon.
- **Shift operator** — Moves the previous solution forward one step to warm-start the next optimization.
- **SceneCollisionNet** — Learned classifier predicting robot-scene collisions from raw point clouds.

## ❓ Open questions

- How does STORM handle dynamic scenes, where the environment point cloud must be processed in real time rather than once at start?
- How much model bias does the kinematic model introduce at higher speeds, and does a residual dynamics model or terminal Q-function fix it without losing speed?
- Can a better-tuned low-level controller close the millimetre-level pose accuracy gap to MoveIt and Manipulability Motion Control?
- Would explicitly accounting for state uncertainty in the control loop make the controller more robust?
- How should the mix ratio between B-spline and comb-filtered samples be chosen for a given task?

## 📝 Notes on reading

Read the arXiv v2 preprint (14 Sep 2021), matching the packet identifier.

Inconsistencies inside the paper:
- Control rate: the abstract and p. 5 give less than 8ms (125Hz), Table 1 (p. 16) lists STORM at 10 ms, and Appendix A.1 (p. 15) says MPC commands are evaluated at 100Hz.
- Danielczuk et al. latency: p. 10 says 1000 ms, Table 1 (p. 16) lists "Sampling MPC [17]" at 100 ms with horizon 40.
- Appendix B.2 says six hard poses were selected; the Table 2 caption reports medians across 5 poses excluding the first.
- Appendix C.3.2 (p. 21) points to Fig. 14 for comb filtering vs B-splines, but those results are in Fig. 13; Fig. 14 is the timing benchmark.
- Fig. 9 caption says MPPI and MoveIt reach the hard pose, where the text says STORM.
- The comb filter formula on p. 7 repeats u_{t,h-1} for c3, likely a typo for h-2.
- Table 2 position error is in mm, so STORM's 4.822 mm is roughly an order of magnitude worse than the baselines despite the text calling it millimeter-level.

Figures described only: Fig. 5 (position tracking and orientation error below 3% over about 120 s), Fig. 7 (ball trajectories in tray frame), Figs. 10-13 (ablation box plots), Fig. 14 (timing plots, no numeric axes extracted). Equations in sections 2-3 were partially garbled in extraction but the cost definitions were readable.

## Suggested new concepts

- Sampling-based model-predictive control — central family (MPPI, CEM) compared across several vault sources on manipulation control.
- Low-discrepancy action sampling — Halton-based sampling for MPC is a reusable technique distinct from STORM itself.
- Learned collision cost — neural self- and scene-collision checks used inside a control loop recur across robotics papers.
- GPU-tensorized rollouts — batching kinematic rollouts on GPU is the enabler of real-time sampling MPC.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H3.** MPC por muestreo en espacio articular y en GPU para manipuladores, con colisión, límites y manipulabilidad como costes.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
