---
aliases: []
type: "source"
title: "Continuous-Time Gaussian Process Motion Planning via Probabilistic Inference"
citekey: "Mukadam2017continuous"
doi: "10.48550/arXiv.1707.07383"
arxiv: "1707.07383"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1707.07383"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Mustafa Mukadam", "Jing Dong", "Xinyan Yan", "Frank Dellaert", "Byron Boots"]
sha256: ["4aaa5b381fe91ec41b1ab8ce03c0a3edcae543b9a864746f31c8a9b7fc522385"]
pdf: "Content/Papers/Mukadam2017continuous.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Mukadam2017continuous.pdf]]

> [!abstract] One-sentence summary
> The paper represents robot trajectories as sparse continuous-time Gaussian processes and casts motion planning as factor-graph inference, yielding the fast batch planner GPMP2 and the incremental replanner iGPMP2.

## Abstract

We introduce a novel formulation of motion planning, for continuous-time trajectories, as probabilistic inference. We first show how smooth continuous-time trajectories can be represented by a small number of states using sparse Gaussian process (GP) models. We next develop an efficient gradient-based optimization algorithm that exploits this sparsity and GP interpolation. We call this algorithm the Gaussian Process Motion Planner (GPMP). We then detail how motion planning problems can be formulated as probabilistic inference on a factor graph. This forms the basis for GPMP2, a very efficient algorithm that combines GP representations of trajectories with fast, structure-exploiting inference via numerical optimization. Finally, we extend GPMP2 to an incremental algorithm, iGPMP2, that can efficiently replan when conditions change. We benchmark our algorithms against several sampling-based and trajectory optimization-based motion planning algorithms on planning problems in multiple environments. Our evaluation reveals that GPMP2 is several times faster than previous algorithms while retaining robustness. We also benchmark iGPMP2 on replanning problems, and show that it can find successful solutions in a fraction of the time required by GPMP2 to replan from scratch. (arXiv)

## 🧠 Key ideas (atomic)

- The authors represent trajectories as continuous-time functions mapping time to robot state, assumed to be sampled from a Gaussian process. (Mukadam et al., 2017) `ev:asserted` p. 2 ^mukadam2017continuous-001
- Through the GP formulation, the authors view motion planning as probabilistic inference, encoding feasibility in a likelihood function. (Mukadam et al., 2017) `ev:asserted` p. 2 ^mukadam2017continuous-002
- The duality between inference and optimization lets the authors perform factor-graph inference by solving sparse least squares problems. (Mukadam et al., 2017) `ev:asserted` p. 2 ^mukadam2017continuous-003
- The paper provides a revised and extended version of the authors' previous work, adding a proof of GPMP2 linear-system sparsity. (Mukadam et al., 2017) `ev:reported` p. 2 ^mukadam2017continuous-004
- Despite probabilistic completeness guarantees, sampling-based algorithms may be difficult to use in real-time applications due to computational challenges. (Mukadam et al., 2017) `ev:cited` p. 3 ^mukadam2017continuous-005
- Trajectory optimization methods are very fast compared with sampling-based planners but only find locally optimal solutions. (Mukadam et al., 2017) `ev:asserted` p. 3 ^mukadam2017continuous-006
- The authors state that, to their knowledge, Gaussian processes had not previously been used in motion planning. (Mukadam et al., 2017) `ev:asserted` p. 3 ^mukadam2017continuous-007
- The GP defines a prior on the space of trajectories that encourages smoothness encoded by the kernel K. (Mukadam et al., 2017) `ev:asserted` p. 4 ^mukadam2017continuous-008
- Conditioning this GP on a fictitious goal observation yields a Gauss-Markov model with an exactly sparse tridiagonal precision matrix. (Mukadam et al., 2017) `ev:computed` p. 5 ^mukadam2017continuous-009
- The linear model is sufficient for the manipulators considered, though the framework could be extended to non-linear models. (Mukadam et al., 2017) `ev:asserted` p. 5 ^mukadam2017continuous-010
- Exploiting the Gauss-Markov prior, interpolation at any time is computed in O(1) from only the two adjacent support states. (Mukadam et al., 2017) `ev:computed` p. 6 ^mukadam2017continuous-011
- During optimization, collision costs at interpolated states are accumulated to nearby support states, which alone are then updated. (Mukadam et al., 2017) `ev:reported` p. 6 ^mukadam2017continuous-012
- [[Gaussian Process Motion Planning|GPMP]] combines the Gaussian process trajectory representation with a gradient descent-based optimization algorithm for motion planning. (Mukadam et al., 2017) `ev:reported` p. 6 ^mukadam2017continuous-013
- [[Gaussian Process Motion Planning|The GPMP objective]] combines an obstacle cost functional with a GP prior cost weighted by a trade-off parameter lambda. (Mukadam et al., 2017) `ev:reported` p. 6 ^mukadam2017continuous-014
- Unlike CHOMP, [[Gaussian Process Motion Planning|GPMP]] augments the trajectory with velocities and accelerations, obtaining them directly from the state rather than finite differencing. (Mukadam et al., 2017) `ev:reported` p. 7 ^mukadam2017continuous-015
- The authors state [[Gaussian Process Motion Planning|GPMP's gradient-based scheme]] converges slowly, requiring many iterations to reach a feasible solution. (Mukadam et al., 2017) `ev:asserted` p. 8 ^mukadam2017continuous-016
- Unlike Toussaint's message-passing inference, the authors solve planning inference as nonlinear least squares using the Smoothing and Mapping framework. (Mukadam et al., 2017) `ev:asserted` p. 8 ^mukadam2017continuous-017
- In GPMP2, the optimal trajectory is the maximum a posteriori estimate under a GP prior and a collision-free likelihood. (Mukadam et al., 2017) `ev:reported` p. 9 ^mukadam2017continuous-018
- Interpolated obstacle factors are binary factors relating the obstacle cost at an interpolated time to its two adjacent support states. (Mukadam et al., 2017) `ev:reported` p. 10 ^mukadam2017continuous-019
- Each GPMP2 iteration linearizes the obstacle cost around the current trajectory, converting the problem into a linear least squares problem. (Mukadam et al., 2017) `ev:reported` p. 11 ^mukadam2017continuous-020
- The authors prove that the GPMP2 linear system is block tridiagonal, allowing efficient solution by sparse Cholesky decomposition. (Mukadam et al., 2017) `ev:computed` p. 11 ^mukadam2017continuous-021
- The authors attribute GPMP2's efficiency over GPMP to structure-exploiting iterations combined with the quadratic convergence of Gauss-Newton or Levenberg-Marquardt. (Mukadam et al., 2017) `ev:asserted` p. 11 ^mukadam2017continuous-022
- When the goal configuration changes, updating the Bayes tree with the new goal changes only its root node. (Mukadam et al., 2017) `ev:asserted` p. 12 ^mukadam2017continuous-023
- iGPMP2 is the incremental variant of GPMP2 that uses the iSAM2 incremental solver to solve replanning problems. (Mukadam et al., 2017) `ev:reported` p. 12 ^mukadam2017continuous-024
- GPMP2 and iGPMP2 were implemented with the GTSAM library and released as the open-source C++ library gpmp2. (Mukadam et al., 2017) `ev:reported` p. 13 ^mukadam2017continuous-025
- [[Gaussian Process Motion Planning|GPMP]] employs a constant-acceleration, jerk-minimizing prior with a Markovian state of configuration position, velocity and acceleration. (Mukadam et al., 2017) `ev:reported` p. 13 ^mukadam2017continuous-026
- GPMP2 uses Levenberg-Marquardt with initial damping 0.01, stopping after 100 iterations or a relative error decrease below 10−4. (Mukadam et al., 2017) `ev:reported` p. 13 ^mukadam2017continuous-027
- GPMP2 uses a constant-velocity prior with a Markovian state comprising configuration position and velocity, unlike GPMP. (Mukadam et al., 2017) `ev:reported` p. 13 ^mukadam2017continuous-028
- The authors state that GPMP2 computation scales only quadratically with the size of the state. (Mukadam et al., 2017) `ev:asserted` p. 14 ^mukadam2017continuous-029
- The GPMP2 obstacle cost applies a hinge loss to the signed distance of each sphere representing the robot body. (Mukadam et al., 2017) `ev:reported` p. 14 ^mukadam2017continuous-030
- Signed distances are queried by trilinear interpolation on a precomputed signed distance field stored in a voxel grid. (Mukadam et al., 2017) `ev:reported` p. 14 ^mukadam2017continuous-031
- Motion constraints are handled softly in GPMP2, as prior knowledge on trajectory states with very small uncertainties. (Mukadam et al., 2017) `ev:reported` p. 15 ^mukadam2017continuous-032
- Experiments used a 7-DOF WAM arm dataset of 24 unique planning problems in a lab environment. (Mukadam et al., 2017) `ev:reported` p. 15 ^mukadam2017continuous-033
- The second dataset used PR2's 7-DOF right arm with 198 unique planning problems in four different environments. (Mukadam et al., 2017) `ev:reported` p. 15 ^mukadam2017continuous-034
- Baselines were TrajOpt, CHOMP, RRT-Connect and LBKPIECE, with all benchmarks run on a single thread of a 3.4GHz Intel Core i7 CPU. (Mukadam et al., 2017) `ev:reported` p. 15 ^mukadam2017continuous-035
- All algorithms were allowed a maximum of 10 seconds per problem and counted successful if a feasible solution was found. (Mukadam et al., 2017) `ev:reported` p. 16 ^mukadam2017continuous-036
- The authors found the range [0.001, 0.02] works well for the obstacle cost weight sigma_obs, with larger arms needing larger values. (Mukadam et al., 2017) `ev:measured` p. 16 ^mukadam2017continuous-037
- Using interpolation during optimization gives GPMP2 a 30 −50% speedup of average and maximum runtime versus no interpolation. (Mukadam et al., 2017) `ev:measured` p. 16 ^mukadam2017continuous-038
- On the WAM dataset, TrajOpt-11 has the lowest runtime but solves only 20% of the problems. (Mukadam et al., 2017) `ev:measured` p. 16 ^mukadam2017continuous-039
- On the PR2 dataset, GPMP2-intp is twice as fast as TrajOpt-11 with a slightly higher success rate. (Mukadam et al., 2017) `ev:measured` p. 16 ^mukadam2017continuous-040
- On the PR2 dataset, GPMP2-intp is slightly behind RRT-Connect in success rate but is 30 times faster. (Mukadam et al., 2017) `ev:measured` p. 16 ^mukadam2017continuous-041
- The authors report GPMP2 always converges well before the maximum time limit, with all failures due to infeasible local minima. (Mukadam et al., 2017) `ev:measured` p. 16 ^mukadam2017continuous-042
- On the WAM dataset, GPMP2-intp averaged 0.121 s with a 91.7% success rate across 24 problems. (Mukadam et al., 2017) `ev:measured` p. 17 ^mukadam2017continuous-043
- GPMP2-no-intp reached 100.0% success on the WAM dataset, with an average time of 0.384 s. (Mukadam et al., 2017) `ev:measured` p. 17 ^mukadam2017continuous-044
- On the WAM dataset, RRT-Connect matched GPMP2-intp's 91.7% success but averaged 1.87 s per problem. (Mukadam et al., 2017) `ev:measured` p. 17 ^mukadam2017continuous-045
- On the PR2 dataset, GPMP2-intp averaged 0.11 s per problem with 79.3% success over 198 problems. (Mukadam et al., 2017) `ev:measured` p. 17 ^mukadam2017continuous-046
- GPMP succeeded on 36.9% of the 198 PR2 problems, averaging 1.7 s per successful problem. (Mukadam et al., 2017) `ev:measured` p. 17 ^mukadam2017continuous-047
- Compared with CHOMP, [[Gaussian Process Motion Planning|GPMP]] is more expensive per iteration, primarily from computing the Hessian needed for workspace acceleration. (Mukadam et al., 2017) `ev:measured` p. 17 ^mukadam2017continuous-048
- GPMP needed fewer iterations than CHOMP, averaging 12.0 with interpolation versus 26.4 for CHOMP on the WAM dataset. (Mukadam et al., 2017) `ev:measured` p. 17 ^mukadam2017continuous-049
- The replanning benchmark assigns a new goal configuration at the middle time-step of each planned trajectory. (Mukadam et al., 2017) `ev:reported` p. 18 ^mukadam2017continuous-050
- On 72 WAM replanning problems, iGPMP2 averaged 8.07 ms versus 65.68 ms for GPMP2, both at 100.0% success. (Mukadam et al., 2017) `ev:measured` p. 18 ^mukadam2017continuous-051
- On 54 PR2 replanning problems, iGPMP2 averaged 6.17 ms versus 27.30 ms for GPMP2 replanning from scratch. (Mukadam et al., 2017) `ev:measured` p. 18 ^mukadam2017continuous-052
- On the PR2 replanning problems, iGPMP2's success rate was 66.7%, compared with 88.9% for GPMP2. (Mukadam et al., 2017) `ev:measured` p. 18 ^mukadam2017continuous-053
- The authors offer three possible explanations for iGPMP2's lower success: old-trajectory initialization, partial relinearization in iSAM2, and no step damping. (Mukadam et al., 2017) `ev:asserted` p. 18 ^mukadam2017continuous-054
- On PR2, iGPMP2 had 81.5% success on the 27 problems whose goal change had L2 distance below 2.0. (Mukadam et al., 2017) `ev:measured` p. 18 ^mukadam2017continuous-055
- For the remaining 27 PR2 problems with goal distance at least 2.0, iGPMP2 had only 51.9% success. (Mukadam et al., 2017) `ev:measured` p. 18 ^mukadam2017continuous-056
- Unlike sampling-based methods, the proposed algorithms do not guarantee probabilistic completeness, as the authors acknowledge. (Mukadam et al., 2017) `ev:asserted` p. 19 ^mukadam2017continuous-057
- The authors note this trajectory optimization strategy may not work on harder planning problems like mazes where sampling-based methods excel. (Mukadam et al., 2017) `ev:asserted` p. 19 ^mukadam2017continuous-058
- The main stated drawback of the approach is its limited ability to handle motion constraints like nonlinear inequality constraints. (Mukadam et al., 2017) `ev:asserted` p. 19 ^mukadam2017continuous-059
- The authors conclude that GPMP2 is consistently faster, often several times faster, than its nearest competitors. (Mukadam et al., 2017) `ev:asserted` p. 19 ^mukadam2017continuous-060
- The authors conclude iGPMP2 solves replanning problems an order of magnitude faster than resolving from scratch with GPMP2. (Mukadam et al., 2017) `ev:asserted` p. 19 ^mukadam2017continuous-061

## 🎯 Contributions

## 📖 Glossary

- **Gaussian process (GP)** — Distribution over functions where any finite set of values is jointly Gaussian.
- **Support state** — One of the sparse states that parameterize the continuous-time trajectory.
- **GP interpolation** — Querying the trajectory between support states via GP regression, here in constant time.
- **LTV-SDE** — Linear time-varying stochastic differential equation generating the structured GP prior kernel.
- **Factor graph** — Bipartite graph of variable and factor nodes representing a factored probability function.
- **MAP inference** — Choosing the trajectory that maximizes the posterior given prior and likelihood.
- **Bayes tree** — Directed tree of cliques derived from a Bayes net, enabling incremental inference.
- **iSAM2** — Incremental smoothing and mapping solver that updates a Bayes tree with new factors.
- **Signed distance field (SDF)** — Precomputed voxel grid of distances to the nearest obstacle surface.
- **Hinge loss** — Obstacle cost that is zero beyond a safety distance and linear inside it.

## ❓ Open questions

- Can sequential quadratic programming be integrated into GPMP2 to handle nonlinear inequality constraints exactly?
- How can iGPMP2 decide when to relinearize or reinitialize without losing its incremental speed advantage?
- How does GPMP2 behave with nonlinear dynamics models instead of the linear constant-velocity prior?
- Would a jerk-minimizing prior in GPMP2 pay off on fast systems such as quadrotors?
- How far do graph-based initializations (GPMP-GRAPH) close the gap to sampling-based planners on maze-like problems?

## 📝 Notes on reading

Version read: arXiv v3 (22 Nov 2018), the extended journal-style version of the 2016 ICRA (GPMP) and RSS (GPMP2) papers; the packet identifier is the same arXiv record.

Inconsistency: the text on p. 16 says TrajOpt-11 solves 20% of WAM problems, while Table 1.A on p. 17 prints 20.8.

Figure 13 (p. 17) gives the per-iteration timing breakdown (forward kinematics, Jacobians, Hessians, solution update, collision checking) only as bars; no values were claimed from it. Figures 2-12 are illustrations (GP prior samples, interpolation, factor graphs, Bayes trees, sphere model, likelihood map, sigma_obs effect) and were only described.

Equations extracted from the PDF (matrices B, M, Phi, Q) are partly garbled in the cached text but the surrounding prose is readable.

## Suggested new concepts

- GPMP2 — widely used factor-graph trajectory optimizer that other planning notes will reference.
- Gauss-Markov GP trajectory prior — sparse continuous-time prior shared by estimation and planning work.
- Motion planning as probabilistic inference — a recurring framing linking planning, control and estimation.
- Incremental replanning via Bayes tree — reuse of SLAM incremental inference for fast replanning.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H3.** GPMP2 formula la planificación como inferencia con prior GP y Gauss-Newton disperso, sustituto con PDF de la familia CHOMP/TrajOpt.
