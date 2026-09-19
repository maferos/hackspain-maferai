---
aliases: []
type: "source"
title: "cuRobo: Parallelized Collision-Free Minimum-Jerk Robot Motion Generation"
citekey: "Sundaralingam2023curobo"
doi: "10.48550/arXiv.2310.17274"
arxiv: "2310.17274"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2310.17274"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Balakumar Sundaralingam", "Siva Kumar Sastry Hari", "Adam Fishman", "Caelan Garrett", "Karl Van Wyk", "Valts Blukis", "Alexander Millane", "Helen Oleynikova", "Ankur Handa", "Fabio Ramos", "Nathan Ratliff", "Dieter Fox"]
sha256: ["cffeaf2d4e7a396f0d0ae99b2213688f19a24f756cccb828bd16fca223abc561"]
pdf: "Content/Papers/Sundaralingam2023curobo.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Sundaralingam2023curobo.pdf]]

> [!abstract] One-sentence summary
> cuRobo solves manipulator motion generation as a GPU-parallel global optimization (collision-free IK, many-seed L-BFGS trajectory optimization with particle initialization, a parallel geometric planner), producing minimum-jerk collision-free trajectories about 60x faster than Tesseract and running on edge devices, released as an open library.

## Abstract

This paper explores the problem of collision-free motion generation for manipulators by formulating it as a global motion optimization problem. We develop a parallel optimization technique to solve this problem and demonstrate its effectiveness on massively parallel GPUs. We show that combining simple optimization techniques with many parallel seeds leads to solving difficult motion generation problems within 50ms on average, 60x faster than state-of-the-art (SOTA) trajectory optimization methods. We achieve SOTA performance by combining L-BFGS step direction estimation with a novel parallel noisy line search scheme and a particle-based optimization solver. To further aid trajectory optimization, we develop a parallel geometric planner that plans within 20ms and also introduce a collision-free IK solver that can solve over 7000 queries/s. We package our contributions into a state of the art GPU accelerated motion generation library, cuRobo and release it to enrich the robotics community. Additional details are available at https://curobo.org (arXiv)

## 🧠 Key ideas (atomic)

- The authors formulate collision-free manipulator motion generation as a global motion optimization problem solved with many parallel optimization seeds. (Sundaralingam et al., 2023) `ev:asserted` p. 5 ^sundaralingam2023curobo-001
- State-of-the-art motion generation solutions take 0.5s to 10s on modern CPUs, depending on the complexity of the task. (Sundaralingam et al., 2023) `ev:cited` p. 5 ^sundaralingam2023curobo-002
- The authors argue that pipelines passing only a single best seed to a local optimizer limit their ability to find better local optima. (Sundaralingam et al., 2023) `ev:asserted` p. 5 ^sundaralingam2023curobo-003
- The robot kinematics and signed distance CUDA kernels are reported to be up to 10,000x faster than existing CPU-based methods. (Sundaralingam et al., 2023) `ev:measured` p. 5 ^sundaralingam2023curobo-004
- The continuous collision checking formulation needs only a point signed distance function, enabling swept checks across primitives, meshes and occupancy maps. (Sundaralingam et al., 2023) `ev:asserted` p. 5 ^sundaralingam2023curobo-005
- The GPU solver is 23×, 80×, and 87× faster than CPU solvers for IK, collision-free IK, and collision-free trajectory optimization respectively. (Sundaralingam et al., 2023) `ev:measured` p. 6 ^sundaralingam2023curobo-006
- The cuRobo inverse kinematics solver can solve 37000 IK problems per second, which is 23× faster than TracIK. (Sundaralingam et al., 2023) `ev:measured` p. 6 ^sundaralingam2023curobo-007
- cuRobo solves 7600 collision-free IK problems per second, 80× faster than using TracIK with Bullet for collision checking. (Sundaralingam et al., 2023) `ev:measured` p. 6 ^sundaralingam2023curobo-008
- The pipeline first solves collision-free IK, then generates trajectory seeds, then runs trajectory optimization over many seeds in parallel. (Sundaralingam et al., 2023) `ev:reported` p. 6 ^sundaralingam2023curobo-009
- After trajectory optimization, a new dt is found by scaling the trajectory to the robot's limits before rerunning optimization with it. (Sundaralingam et al., 2023) `ev:reported` p. 7 ^sundaralingam2023curobo-010
- The robot's volume is approximated by a set of spheres, reducing world collision checks to sphere-origin distances minus the radius. (Sundaralingam et al., 2023) `ev:reported` p. 7 ^sundaralingam2023curobo-011
- The authors empirically found that only 50% of sphere pairs end up in the self-collision set across many widely used manipulators. (Sundaralingam et al., 2023) `ev:measured` p. 8 ^sundaralingam2023curobo-012
- The world collision cost becomes quadratic within a buffer distance η of an obstacle surface, mitigating the discontinuity at the surface boundary. (Sundaralingam et al., 2023) `ev:reported` p. 8 ^sundaralingam2023curobo-013
- A speed metric scales each sphere's collision cost by its velocity, encouraging the optimizer to move around obstacles instead of through them. (Sundaralingam et al., 2023) `ev:reported` p. 8 ^sundaralingam2023curobo-014
- Continuous collision checking sweeps from each sphere waypoint backward and forward to the midpoints, keeping gradient computations parallelizable across timesteps. (Sundaralingam et al., 2023) `ev:reported` p. 9 ^sundaralingam2023curobo-015
- The continuous collision implementation assumes spheres move linearly between waypoints, which is not true for links attached through revolute joints. (Sundaralingam et al., 2023) `ev:asserted` p. 9 ^sundaralingam2023curobo-016
- cuRobo implements three world representations: oriented bounding boxes, watertight meshes via Warp's BVH, and nvblox ESDF maps from depth cameras. (Sundaralingam et al., 2023) `ev:reported` p. 9 ^sundaralingam2023curobo-017
- cuRobo approximates its constraints as cost terms with large weights, yielding a box-constrained nonconvex problem for a quasi-Newton solver. (Sundaralingam et al., 2023) `ev:reported` p. 10 ^sundaralingam2023curobo-018
- The authors built their optimizers around L-BFGS because of its combined performance and relative simplicity that aids parallelization. (Sundaralingam et al., 2023) `ev:asserted` p. 11 ^sundaralingam2023curobo-019
- The line search evaluates a predefined discrete set of step magnitudes in parallel, selecting the best using Armijo and Wolfe conditions. (Sundaralingam et al., 2023) `ev:reported` p. 11 ^sundaralingam2023curobo-020
- When no magnitude in the discrete set satisfies the line search conditions, a very small magnitude of 0.01 acts as a noisy step. (Sundaralingam et al., 2023) `ev:reported` p. 11 ^sundaralingam2023curobo-021
- The authors found that a noisy perturbation, instead of stopping when line search fails, greatly increased the convergence rate on trajectory optimization. (Sundaralingam et al., 2023) `ev:measured` p. 11 ^sundaralingam2023curobo-022
- A few iterations of particle-based optimization, inspired by sampling-based controllers such as MPPI, are run over the initialization before L-BFGS. (Sundaralingam et al., 2023) `ev:reported` p. 11 ^sundaralingam2023curobo-023
- The geometric planner parallelizes node sampling, k-nearest-neighbour search, and steering from sampled nodes to their nearest graph nodes on the GPU. (Sundaralingam et al., 2023) `ev:reported` p. 12 ^sundaralingam2023curobo-024
- Evaluation uses 800 motionbenchmaker problems and 1800 mpinets problems for the 7-joint Franka Emika Panda across 12 scene types. (Sundaralingam et al., 2023) `ev:reported` p. 13 ^sundaralingam2023curobo-025
- cuRobo is compared against Tesseract, which combines Bullet continuous collision detection, OMPL geometric planning and TrajOpt trajectory optimization. (Sundaralingam et al., 2023) `ev:reported` p. 13 ^sundaralingam2023curobo-026
- The cuRobo-GP geometric planner found a path on 99.8% of the dataset, compared with Tesseract-GP's 98.6%. (Sundaralingam et al., 2023) `ev:measured` p. 14 ^sundaralingam2023curobo-027
- With trajectory optimization, cuRobo failed on 5 problems while Tesseract failed on 38, giving success rates of 99.8% and 98.53%. (Sundaralingam et al., 2023) `ev:measured` p. 14 ^sundaralingam2023curobo-028
- The authors attribute cuRobo's five failures to its cuboid collision checker, which approximates cylindrical obstacles as cuboids. (Sundaralingam et al., 2023) `ev:asserted` p. 15 ^sundaralingam2023curobo-029
- cuRobo reduces C-space path length on average by 53%, 39%, and 10% compared with Tesseract-GP, cuRobo-GP, and Tesseract respectively. (Sundaralingam et al., 2023) `ev:measured` p. 15 ^sundaralingam2023curobo-030
- cuRobo's paths are 26% shorter than Tesseract's paths on the 98th percentile of the benchmark dataset. (Sundaralingam et al., 2023) `ev:measured` p. 15 ^sundaralingam2023curobo-031
- Kunz and Stilman's widely used time-parameterization technique bounds velocity and acceleration but does not bound jerk along the trajectory. (Sundaralingam et al., 2023) `ev:cited` p. 16 ^sundaralingam2023curobo-032
- cuRobo produces trajectories with a 1.23x lower mean and 1.62x lower 98th percentile motion time than Tesseract. (Sundaralingam et al., 2023) `ev:measured` p. 17 ^sundaralingam2023curobo-033
- Compared with time-optimal Tesseract-TG, cuRobo trajectories are 0.3 seconds slower both on average and at the 98th percentile. (Sundaralingam et al., 2023) `ev:measured` p. 17 ^sundaralingam2023curobo-034
- cuRobo's minimum-jerk optimization yields trajectories with 12x lower jerk on average than Tesseract-TG's time-optimal reparameterization. (Sundaralingam et al., 2023) `ev:measured` p. 17 ^sundaralingam2023curobo-035
- cuRobo generates trajectories with 4x lower jerk on average than Tesseract, which does not minimize jerk. (Sundaralingam et al., 2023) `ev:measured` p. 17 ^sundaralingam2023curobo-036
- On the desktop PC, Tesseract takes 2.95 seconds on average compared with 50ms for cuRobo, a 60× speedup. (Sundaralingam et al., 2023) `ev:measured` p. 18 ^sundaralingam2023curobo-037
- At the 98th percentile, cuRobo takes 260 milliseconds while Tesseract takes 22 seconds, giving an 83× speedup in planning. (Sundaralingam et al., 2023) `ev:measured` p. 18 ^sundaralingam2023curobo-038
- On the Jetson Orin, cuRobo is 28× and 21× faster than Tesseract on average at MAXN and 15W respectively. (Sundaralingam et al., 2023) `ev:measured` p. 19 ^sundaralingam2023curobo-039
- Recording optimization iterations in CUDA Graphs reduced planning time by 10x compared with calling the kernels individually from Python. (Sundaralingam et al., 2023) `ev:measured` p. 19 ^sundaralingam2023curobo-040
- cuRobo-GP takes 0.02 seconds on average versus 1.5 seconds for Tesseract-GP, a 101× speedup in geometric planning. (Sundaralingam et al., 2023) `ev:measured` p. 20 ^sundaralingam2023curobo-041
- cuRobo's trajectory optimization is 87× and 145× faster than TrajOpt on average and at the 75th percentile respectively. (Sundaralingam et al., 2023) `ev:measured` p. 20 ^sundaralingam2023curobo-042
- The rejection-sampling approach to collision-free IK using TracIK failed on 20% of the problems tested. (Sundaralingam et al., 2023) `ev:measured` p. 21 ^sundaralingam2023curobo-043
- cuRobo's forward kinematics becomes up to 891x faster than CPU methods at a batch size of 100k. (Sundaralingam et al., 2023) `ev:measured` p. 23 ^sundaralingam2023curobo-044
- cuRobo's full motion generation pipeline runs at 30ms on median on a modern PC across the benchmarking dataset. (Sundaralingam et al., 2023) `ev:measured` p. 23 ^sundaralingam2023curobo-045
- Mean position error on the UR5e was 0.00117 radians for min-acc and 0.00085 radians for min-jerk, both within encoder accuracy. (Sundaralingam et al., 2023) `ev:measured` p. 25 ^sundaralingam2023curobo-046
- On the UR10, mean position error was 0.00250 radians for min-acc and 0.00133 radians for min-jerk. (Sundaralingam et al., 2023) `ev:measured` p. 25 ^sundaralingam2023curobo-047
- cuRobo planning takes about 6% of the cycle time on average, allowing the next motion to be planned after executing the current one. (Sundaralingam et al., 2023) `ev:measured` p. 27 ^sundaralingam2023curobo-048
- Increasing the collision activation distance from 0cm to 2.5cm improved success rate by 27%, the largest impact among collision cost components. (Sundaralingam et al., 2023) `ev:measured` p. 28 ^sundaralingam2023curobo-049
- Adding continuous swept collision checking improves success rate by 4% compared with only using an activation distance of 2.5cm. (Sundaralingam et al., 2023) `ev:measured` p. 28 ^sundaralingam2023curobo-050
- Combining these collision techniques with particle initialization and many parallel seeds raised single-attempt success from 38% to 85%. (Sundaralingam et al., 2023) `ev:measured` p. 29 ^sundaralingam2023curobo-051
- On an RTX 4090, compute time changes by only 8ms from 4 to 48 seeds, versus 158ms and 417ms on the Orin. (Sundaralingam et al., 2023) `ev:measured` p. 30 ^sundaralingam2023curobo-052
- Initializing trajectory optimization with the geometric planner raises success but doubles the planning time on most problems. (Sundaralingam et al., 2023) `ev:measured` p. 30 ^sundaralingam2023curobo-053
- Noisy line search achieved the highest single-seed success rate of 75.69% among the compared line search methods. (Sundaralingam et al., 2023) `ev:measured` p. 30 ^sundaralingam2023curobo-054
- Noisy line search had the lowest final position error of 2.86 mm, whereas no line search ended with 4 mm. (Sundaralingam et al., 2023) `ev:measured` p. 30 ^sundaralingam2023curobo-055
- Replacing L-BFGS with gradient descent, keeping the noisy line search, succeeded on 46% of the problems. (Sundaralingam et al., 2023) `ev:measured` p. 31 ^sundaralingam2023curobo-056
- The approach is currently limited to planning full motions from a static state, not reactive motion generation at fixed rates. (Sundaralingam et al., 2023) `ev:asserted` p. 32 ^sundaralingam2023curobo-057
- The approach does not tackle partial perception, instead assuming that a complete representation of the world can be obtained. (Sundaralingam et al., 2023) `ev:asserted` p. 33 ^sundaralingam2023curobo-058
- The current cost terms focus on kinematic trajectory optimization, without optimizing over contacts or the robot's dynamics. (Sundaralingam et al., 2023) `ev:asserted` p. 33 ^sundaralingam2023curobo-059
- The five point stencil derivatives reduced the number of iterations required to converge by 50%, compared with earlier schemes. (Sundaralingam et al., 2023) `ev:measured` p. 36 ^sundaralingam2023curobo-060

## 🎯 Contributions

## 📖 Glossary

- **L-BFGS** — Limited-memory quasi-Newton optimizer estimating the Hessian from a short history of gradients.
- **Noisy line search** — Parallel evaluation of fixed step magnitudes, falling back to a tiny step on failure.
- **Activation distance (η)** — Buffer distance near obstacles or limits where a smooth quadratic cost starts.
- **Speed metric** — Scaling a sphere's collision cost by its velocity to discourage passing through obstacles.
- **Continuous collision checking** — Checking collisions along the motion between timesteps, not only at waypoints.
- **ESDF** — Euclidean signed distance field; voxel map of distance to the nearest obstacle surface.
- **Collision-free IK** — Inverse kinematics that also enforces self- and world-collision avoidance.
- **Five point stencil** — Finite-difference scheme using five adjacent samples to estimate time derivatives.
- **CUDA Graph** — Recorded sequence of GPU kernel launches replayed to cut launch overhead.
- **Motion Time** — Planned trajectory duration, (n−1)·dt, equal to execution time under perfect tracking.

## ❓ Open questions

- Can the approach be extended to global reactive motion generation at a fixed solve rate, given its long 98th percentile times?
- How do cuRobo's mesh and depth-camera (nvblox) collision checkers perform on the benchmark compared with the cuboid checker?
- Would a GPU-friendly Gauss-Newton or robotics-specific solver converge faster or allow hard constraints?
- How does exact curved sphere motion between waypoints, instead of the linear assumption, change continuous collision checking results?
- How does cuRobo compare against CPU SIMD-vectorized geometric planning (Thomason et al.) once code is available?
- Can a single set of cost weights work for trajectories of any length without the timestep re-optimization step?
- How can learned or partial world representations be integrated for motion generation in unknown environments?

## 📝 Notes on reading

Version read: arXiv v2 (3 Nov 2023), matching the packet's arXiv identifier; the paper notes it extends an ICRA 2023 version with jerk minimization, five point stencil derivatives, timestep optimization and a faster desktop CPU (Appendix F, p. 57).

Inconsistency: p. 13 states the mpinets dataset contains 1800 problems (800 + 1800 = 2600 total, as used throughout), while Appendix B.1 (p. 39) says 1600 problems from mpinets. The 1800 figure was claimed.

Inconsistency: p. 31 text gives the gradient-descent 98th percentile position error as 4.94cm versus L-BFGS 2.72cm, while Figure 31 labels the axis in mm; the unit is uncertain, so the number was not claimed.

The contributions list (p. 6) states geometric planning within 20 ms, whereas the median summary (Figure 20, p. 24) shows 16 ms and the text mean is 0.02 seconds. Figure 13's caption mentions Tesseract on an i7 desktop while the text describes an AMD Ryzen 9 7950x PC.

Figures described only (no claims): Figure 2 pipeline diagram, Figure 4 continuous collision illustration, Figures 21-25 real-robot scenes and tracking plots, Figure 27 speed-metric visualization, Figure 32 convergence curves, Figures 34-42 appendix plots and diagrams. Kernel timing Tables 3-5 (p. 49), joint transformation Tables 6-7 (p. 50) and Algorithms 7-12 (pp. 51-56) were not claimed cell by cell. Equations were partly garbled in extraction (e.g., dotted derivative symbols rendered as digits and colons).

## Suggested new concepts

- GPU-parallel trajectory optimization — many-seed batched optimization as an alternative to sequential CPU planning pipelines.
- Continuous collision checking via point signed distance — representation-agnostic swept collision checks relevant to perception-driven planning.
- Minimum-jerk trajectory generation — link between jerk minimization and real-robot tracking accuracy on industrial arms.
- Sphere-based robot collision models — common geometric approximation enabling fast batched self and world collision queries.
- Noisy line search — parallel discrete step-size selection with a fallback perturbation, reusable in other batched solvers.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H1.** Referencia de IK y trayectorias libres de colisión en GPU con miles de semillas paralelas.
