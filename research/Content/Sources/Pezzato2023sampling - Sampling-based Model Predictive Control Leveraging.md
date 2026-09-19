---
aliases: []
type: "source"
title: "Sampling-based Model Predictive Control Leveraging Parallelizable Physics Simulations"
citekey: "Pezzato2023sampling"
doi: "10.48550/arXiv.2307.09105"
arxiv: "2307.09105"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2307.09105"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Corrado Pezzato", "Chadi Salmi", "Elia Trevisan", "Max Spahn", "Javier Alonso-Mora", "Carlos Hernández Corbato"]
sha256: ["4469758cb0cdde16ed2eae12b548429142c2bf2345de2c424ae9195e0cab62f7"]
pdf: "Content/Papers/Pezzato2023sampling.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Pezzato2023sampling.pdf]]

> [!abstract] One-sentence summary
> The paper replaces the explicit dynamics model of MPPI with parallel IsaacGym rollouts, so one cost function suffices for collision avoidance, whole-body control and non-prehensile pushing on real robots.

## Abstract

We present a method for sampling-based model predictive control that makes use of a generic physics simulator as the dynamical model. In particular, we propose a Model Predictive Path Integral controller (MPPI), that uses the GPU-parallelizable IsaacGym simulator to compute the forward dynamics of a problem. By doing so, we eliminate the need for explicit encoding of robot dynamics and contacts with objects for MPPI. Since no explicit dynamic modeling is required, our method is easily extendable to different objects and robots and allows one to solve complex navigation and contact-rich tasks. We demonstrate the effectiveness of this method in several simulated and real-world settings, among which mobile navigation with collision avoidance, non-prehensile manipulation, and whole-body control for high-dimensional configuration spaces. This method is a powerful and accessible open-source tool to solve a large variety of contact-rich motion planning tasks. (arXiv)

## 🧠 Key ideas (atomic)

- The authors propose [[Model Predictive Path Integral control|an MPPI controller]] that uses the GPU-parallelizable IsaacGym simulator to compute the forward dynamics of the robot and environment. (Pezzato et al., 2023) `ev:asserted` p. 1 ^pezzato2023sampling-001
- In the proposed training-free framework the user designs only a cost function, not the dynamics and contact models of the problem. (Pezzato et al., 2023) `ev:asserted` p. 1 ^pezzato2023sampling-002
- The authors argue that MuJoCo parallelization is constrained by the number of CPU threads, limiting real-time performance when many samples are required. (Pezzato et al., 2023) `ev:asserted` p. 2 ^pezzato2023sampling-003
- Arruda et al. plan pushes with an MPPI controller that uses a forward model learned from 326 real robot pushes. (Pezzato et al., 2023) `ev:cited` p. 2 ^pezzato2023sampling-004
- The authors note that both learned push baselines require a separate controller to convert cartesian motions into joint commands. (Pezzato et al., 2023) `ev:asserted` p. 2 ^pezzato2023sampling-005
- The approximate optimal input sequence is a weighted average of the sampled inputs, of which only the first input is applied. (Pezzato et al., 2023) `ev:cited` p. 2 ^pezzato2023sampling-006
- Instead of an explicit transition function f, the method uses IsaacGym to compute the next state from the current state and input. (Pezzato et al., 2023) `ev:reported` p. 3 ^pezzato2023sampling-007
- Since the K state trajectories are independent of each other, all rollouts are simulated in parallel using the parallelization capabilities of IsaacGym. (Pezzato et al., 2023) `ev:reported` p. 3 ^pezzato2023sampling-008
- Following prior work, input noise is sampled as B-Splines fitted to Halton sequences instead of Gaussian noise, for smoother trajectories. (Pezzato et al., 2023) `ev:reported` p. 3 ^pezzato2023sampling-009
- Unlike that prior work, the sampling variance is not updated online but kept as a constant tuning parameter during execution. (Pezzato et al., 2023) `ev:reported` p. 3 ^pezzato2023sampling-010
- The authors state that updating the sampling variance leads to stagnation of the control over time, which is harmful in contact-rich tasks. (Pezzato et al., 2023) `ev:asserted` p. 3 ^pezzato2023sampling-011
- The inverse temperature β is updated each iteration, multiplied by 0.9 when η exceeds ηmax or by 1.2 when η is below ηmin. (Pezzato et al., 2023) `ev:reported` p. 3 ^pezzato2023sampling-012
- Empirically, keeping the normalization factor η between 5 and 10 gave a good balance for smooth behavior in all performed tasks. (Pezzato et al., 2023) `ev:measured` p. 3 ^pezzato2023sampling-013
- Collision checking uses the IsaacGym contact forces tensor, with a cost proportional to the contact forces exerted on obstacles. (Pezzato et al., 2023) `ev:reported` p. 3 ^pezzato2023sampling-014
- The authors state that this cost allows continuous collision checking at each time step over the horizon with arbitrarily complex shapes. (Pezzato et al., 2023) `ev:asserted` p. 3 ^pezzato2023sampling-015
- Relaxing the collision weight ωc allows contacts required by the task, such as rolling a ball against a wall. (Pezzato et al., 2023) `ev:asserted` p. 3 ^pezzato2023sampling-016
- Object mass and friction are randomized in every rollout from a uniform distribution, to account for uncertainty in environment perception. (Pezzato et al., 2023) `ev:reported` p. 3 ^pezzato2023sampling-017
- Experiments and simulations were conducted on an Alienware laptop with an Nvidia 3070 Ti graphics card. (Pezzato et al., 2023) `ev:reported` p. 4 ^pezzato2023sampling-018
- Real-world tests used a ROS wrapper connecting the robot to the planner, with a motion capture system giving object poses. (Pezzato et al., 2023) `ev:reported` p. 4 ^pezzato2023sampling-019
- Motion planning was benchmarked against optimization fabrics and a ForcesPro MPC in localPlannerBench, with five randomized obstacles over 100 runs. (Pezzato et al., 2023) `ev:reported` p. 4 ^pezzato2023sampling-020
- Path length and clearance showed minimal differences between the three compared methods for both robots in the benchmark. (Pezzato et al., 2023) `ev:measured` p. 4 ^pezzato2023sampling-021
- MPPI reached the goal in 2.7s on average for the point robot, versus 7.4s for fabrics and 6.1s for ForcesPro MPC. (Pezzato et al., 2023) `ev:measured` p. 4 ^pezzato2023sampling-022
- For the Panda arm, the average [[Model Predictive Path Integral control|MPPI]] time to goal was 0.8s, compared with 9.6s for fabrics and 4.2s for ForcesPro MPC. (Pezzato et al., 2023) `ev:measured` p. 4 ^pezzato2023sampling-023
- The authors attribute the faster goal reaching to the perfect representation of robot collision shapes, versus enclosing spheres in the baselines. (Pezzato et al., 2023) `ev:asserted` p. 4 ^pezzato2023sampling-024
- The average MPPI solver time was 55ms for the point robot, against 1.0ms for fabrics and 2.5ms for ForcesPro MPC. (Pezzato et al., 2023) `ev:measured` p. 4 ^pezzato2023sampling-025
- The average MPPI solver time for the Panda was 63ms, against 1.4ms for fabrics and 51ms for ForcesPro MPC. (Pezzato et al., 2023) `ev:measured` p. 4 ^pezzato2023sampling-026
- The authors attribute the higher computational times of their approach in the benchmark to the physics simulations performed by IsaacGym. (Pezzato et al., 2023) `ev:asserted` p. 4 ^pezzato2023sampling-027
- Sampling all DOF at once, including base and gripper, produced fluid motion from start to end with no added heuristics for pick positions. (Pezzato et al., 2023) `ev:measured` p. 5 ^pezzato2023sampling-028
- Across ten pick-and-deliver tasks with the whole-body mobile manipulator, the time taken was 15.67 ± 7.21s. (Pezzato et al., 2023) `ev:measured` p. 5 ^pezzato2023sampling-029
- The high standard deviation is because the cube sometimes falls, but the robot can recover by picking it up from the floor. (Pezzato et al., 2023) `ev:measured` p. 5 ^pezzato2023sampling-030
- Empirically, when the number of samples exceeds 50, a GPU pipeline is computationally cheaper than a CPU pipeline. (Pezzato et al., 2023) `ev:measured` p. 5 ^pezzato2023sampling-031
- Using IsaacGym, all 750 samples required for mobile manipulation are computed in parallel, with the next control input computed online at 25Hz. (Pezzato et al., 2023) `ev:measured` p. 5 ^pezzato2023sampling-032
- Instead of sampling 2D end-effector trajectories, the method samples the control input directly as joint velocities in IsaacGym. (Pezzato et al., 2023) `ev:reported` p. 5 ^pezzato2023sampling-033
- The authors state that sampling joint velocities yields smooth continuous pushes where end-effector repositioning emerges naturally, without learning. (Pezzato et al., 2023) `ev:asserted` p. 5 ^pezzato2023sampling-034
- Since baseline models and data were not provided, the authors compared only against the final results reported in the baseline papers. (Pezzato et al., 2023) `ev:reported` p. 5 ^pezzato2023sampling-035
- The push cost combines weighted distance terms, a push-alignment term keeping the object between robot and goal, and an end-effector alignment term. (Pezzato et al., 2023) `ev:reported` p. 5 ^pezzato2023sampling-036
- The method completes either pushing task in approximately 8 seconds, versus approximately 4 minutes for the replanning baseline of Arruda et al. (Pezzato et al., 2023) `ev:measured` p. 5 ^pezzato2023sampling-037
- Against the Arruda et al. baseline, the method reached a final cost of 0.029 ±0.09 for Pose 1, versus 0.057. (Pezzato et al., 2023) `ev:measured` p. 6 ^pezzato2023sampling-038
- For Pose 2, the final cost of the method was 0.03 ±0.12, compared with 0.079 for the Arruda et al. baseline. (Pezzato et al., 2023) `ev:measured` p. 6 ^pezzato2023sampling-039
- The comparison with Cong et al. pushed 5 objects to 3 goal poses, with 10 pushes per object totaling 150 pushes. (Pezzato et al., 2023) `ev:reported` p. 6 ^pezzato2023sampling-040
- The method took about 3 seconds per push task, whereas the Cong et al. baseline needed about 24 seconds. (Pezzato et al., 2023) `ev:measured` p. 6 ^pezzato2023sampling-041
- Simulated success rates in percent were 100 for objects A and D, versus 93.5 and 91.6 for Cong et al. (Pezzato et al., 2023) `ev:measured` p. 6 ^pezzato2023sampling-042
- For objects B and C, simulated success rates in percent were 93.3 and 96.7, versus 90.9 and 93.9 for the baseline. (Pezzato et al., 2023) `ev:measured` p. 6 ^pezzato2023sampling-043
- For object E, the simulated success rate of the method was 66.7 percent, below the 89.5 percent of Cong et al. (Pezzato et al., 2023) `ev:measured` p. 6 ^pezzato2023sampling-044
- For arm pushing, the mass and friction of manipulated objects had 30% uncertainty on nominal values, sampled uniformly. (Pezzato et al., 2023) `ev:reported` p. 6 ^pezzato2023sampling-045
- In arm pushing rollouts, object size was randomized with zero-mean additive Gaussian noise of 2 mm standard deviation. (Pezzato et al., 2023) `ev:reported` p. 6 ^pezzato2023sampling-046
- The authors state that their method outperforms both baselines in time to completion, accuracy and success rate, except for one manipulated object. (Pezzato et al., 2023) `ev:asserted` p. 6 ^pezzato2023sampling-047
- Transferring to a different robot only required changing the environment and robot URDF in IsaacGym, plus re-tuning the pushing cost. (Pezzato et al., 2023) `ev:reported` p. 6 ^pezzato2023sampling-048
- Box pushing success required placement within 5cm in the x-y direction and within 0.17 radians in rotation. (Pezzato et al., 2023) `ev:reported` p. 6 ^pezzato2023sampling-049
- With the omnidirectional base, box pushing took 9.66 ± 0.84 s over five runs from Pose A. (Pezzato et al., 2023) `ev:measured` p. 6 ^pezzato2023sampling-050
- Over five runs from Pose B, omnidirectional box pushing took 12.84 ± 0.564 s to reach the goal. (Pezzato et al., 2023) `ev:measured` p. 6 ^pezzato2023sampling-051
- Rolling a sphere between two walls with the omnidirectional base took 8.76 ± 0.38 s over five runs from Pose A. (Pezzato et al., 2023) `ev:measured` p. 6 ^pezzato2023sampling-052
- From Pose B, omnidirectional sphere placement between the two walls took 7.45 ± 0.59 s over five runs. (Pezzato et al., 2023) `ev:measured` p. 6 ^pezzato2023sampling-053
- Differential drive pushing of the box to the goal took 18.31s with the same cost function, re-tuned. (Pezzato et al., 2023) `ev:measured` p. 7 ^pezzato2023sampling-054
- In the real-world pushing tasks, samples were rolled out in K = 500 IsaacGym environments initialized to the real-world state at each timestep. (Pezzato et al., 2023) `ev:reported` p. 7 ^pezzato2023sampling-055
- When transferring to the real robot arm, only the cost function weights were re-tuned relative to the simulated experiments. (Pezzato et al., 2023) `ev:reported` p. 7 ^pezzato2023sampling-056
- Real-world push completion times and final position errors were comparable to the simulation results of the Arruda et al. comparison. (Pezzato et al., 2023) `ev:measured` p. 7 ^pezzato2023sampling-057
- Since planning and execution run in real time at 25Hz, the robot can compensate for large perturbations applied by hand. (Pezzato et al., 2023) `ev:measured` p. 7 ^pezzato2023sampling-058
- The authors note that computational demands can be high when the time horizon is extended to several seconds. (Pezzato et al., 2023) `ev:asserted` p. 7 ^pezzato2023sampling-059
- The authors propose that global planners such as A*, RRT or PRM should guide the local planner to avoid local minima. (Pezzato et al., 2023) `ev:asserted` p. 7 ^pezzato2023sampling-060
- The authors state that online system identification to converge to the true model parameters is not performed in their method. (Pezzato et al., 2023) `ev:asserted` p. 8 ^pezzato2023sampling-061
- The authors note that tuning the controller is time-consuming, suggesting autotuning techniques to reduce manual effort. (Pezzato et al., 2023) `ev:asserted` p. 8 ^pezzato2023sampling-062
- The authors conclude that their method outperforms other approaches by a margin for contact-rich tasks in their experiments. (Pezzato et al., 2023) `ev:asserted` p. 8 ^pezzato2023sampling-063

## 🎯 Contributions

## 📖 Glossary

- **MPPI** — Model Predictive Path Integral control: sampling-based MPC weighting rollouts by exponentiated cost.
- **Inverse temperature (β)** — MPPI parameter setting how sharply low-cost rollouts dominate the weighted average.
- **Normalization factor (η)** — Sum of unnormalized weights; indicates how many samples carry significant weight.
- **Halton splines** — Input noise built by fitting B-Splines to low-discrepancy Halton sequence samples.
- **Non-prehensile manipulation** — Moving objects without grasping them, for example by pushing or rolling.
- **Domain randomization** — Varying simulated physical parameters so the controller tolerates model mismatch.
- **Warm-start** — Initializing the next optimization with the time-shifted previous solution.
- **Optimization fabrics** — Geometric local motion planning method used as a baseline.

## ❓ Open questions

- How does the approach scale when horizons of several seconds are needed without a global planner?
- Would online system identification of object parameters improve precision over fixed randomization ranges?
- Why did object E reach only 66.7% success, and is this a cost-tuning or a simulation-fidelity issue?
- How much of the sim-to-real transfer depends on motion capture pose estimates rather than onboard perception?
- Can the cost weights be autotuned rather than re-tuned by hand per robot and task?

## 📝 Notes on reading

The cached text is arXiv v3 (21 Jan 2025), labelled the IEEE RA-L accepted version; the PDF abstract is worded differently from the registry abstract. Figures 3 and 4 (path length, clearance and time distributions against fabrics and ForcesPro MPC) are plots only; their per-run values were not claimed. In Table II the reported standard deviations (±0.09, ±0.12) are larger than the means (0.029, 0.03), which is unusual for a non-negative cost and is not explained. Table IV reports 12.84 ± 0.564 with inconsistent precision. The real-world arm pushing is reported only qualitatively as comparable to simulation, with no numeric table. The control rate of 25Hz is given for whole-body control and real-world pushing; dt = 0.04 in the tuning footnotes is consistent with it. The mobile manipulator cost terms are given by name without weights. Background MPPI equations and related-work details (MuJoCo predictive sampling, LSTM push models) were left unclaimed to keep the note within volume.

## Suggested new concepts

- Simulator-as-dynamics-model MPC — a distinct design pattern where a physics engine replaces an explicit model inside sampling-based control.
- Model Predictive Path Integral control — core sampling-based MPC method that several vault sources build on.
- Contact-force collision cost — using simulator contact tensors as a collision penalty instead of geometric distance checks.
- Rollout-level domain randomization — randomizing physics per rollout inside a controller to handle model uncertainty online.
- GPU-parallel physics simulation — enabler for large sample counts in real-time planning and learning.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H3.** Usa un simulador físico paralelo como modelo de MPPI, receta trasladable a MuJoCo/MJX para tareas con contacto en AutoBio.
