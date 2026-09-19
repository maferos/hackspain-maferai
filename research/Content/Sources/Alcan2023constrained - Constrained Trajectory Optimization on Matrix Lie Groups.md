---
aliases: []
type: "source"
title: "Constrained Trajectory Optimization on Matrix Lie Groups via Lie-Algebraic DDP"
citekey: "Alcan2023constrained"
doi: "10.48550/arXiv.2301.02018"
arxiv: "2301.02018"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2301.02018"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Gokhan Alcan", "Fares J. Abu-Dakka", "Ville Kyrki"]
sha256: ["cb09da56341cd33ac71ec0c1cfa3a95f19c68bf4ac5a9a901358baef6274c3a4"]
pdf: "Content/Papers/Alcan2023constrained.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Alcan2023constrained.pdf]]

> [!abstract] One-sentence summary
> The paper proposes an augmented Lagrangian constrained DDP that works in the Lie algebra on the backward pass and on the manifold on the forward pass, so generic nonlinear constraints can be handled on any matrix Lie group; in SE(3) and quadrotor simulations it converged in fewer iterations than SLSQP and IPOPT.

## Abstract

Matrix Lie groups are an important class of manifolds commonly used in control and robotics, and optimizing control policies on these manifolds is a fundamental problem. In this work, we propose a novel computationally efficient approach for trajectory optimization on matrix Lie groups using an augmented Lagrangian-based constrained discrete Differential Dynamic Programming (DDP). The method involves lifting the optimization problem to the Lie algebra during the backward pass and retracting back to the manifold during the forward pass. Unlike previous approaches that addressed constraint handling only for specific classes of matrix Lie groups, the proposed method provides a general solution for nonlinear constraint handling across generic matrix Lie groups. We evaluate the effectiveness of the proposed DDP method in handling constraints within a mechanical system characterized by rigid body dynamics in SE(3), assessing its computational efficiency compared to existing direct optimization solvers. Additionally, the method demonstrates robustness under external disturbances when applied as a Lie-algebraic feedback control policy on SE(3), and in optimizing a quadrotor's trajectory in a challenging realistic scenario. Experiments show that the proposed approach effectively manages general constraints defined on configuration, velocity, and inputs during optimization, while also maintaining stability under external disturbances when executing the resultant control policy in closed-loop. (arXiv)

## 🧠 Key ideas (atomic)

- The authors propose an augmented Lagrangian-based constrained DDP algorithm for trajectory optimization on matrix Lie groups. (Alcan et al., 2023) `ev:asserted` p. 2 ^alcan2023constrained-001
- The method lifts the optimization problem to the Lie algebra during the backward pass by computing cost gradients in that algebra. (Alcan et al., 2023) `ev:reported` p. 4 ^alcan2023constrained-002
- In the forward pass, the method retracts to the manifold by integrating the dynamics with the optimal policy from the backward pass. (Alcan et al., 2023) `ev:reported` p. 4 ^alcan2023constrained-003
- The authors state that earlier DDP-based geometric control methods considered only specific matrix Lie groups, omitted state constraints, or handled constraints for particular groups. (Alcan et al., 2023) `ev:cited` p. 2 ^alcan2023constrained-004
- The authors describe the cited MPC methods on SO(3) and SE(3) as restricted to specific matrix Lie groups. (Alcan et al., 2023) `ev:cited` p. 3 ^alcan2023constrained-005
- Boutselis and Theodorou showed that DDP on Lie groups has significantly better convergence rates than Sequential Quadratic Programming methods. (Alcan et al., 2023) `ev:cited` p. 3 ^alcan2023constrained-006
- Teng et al. improved the convergence of DDP for matrix groups by designing the control objective in its Lie algebra. (Alcan et al., 2023) `ev:cited` p. 3 ^alcan2023constrained-007
- Both the Boutselis–Theodorou and Teng et al. DDP approaches formulate trajectory optimization on matrix Lie groups in an unconstrained framework. (Alcan et al., 2023) `ev:cited` p. 3 ^alcan2023constrained-008
- Liu and Liu extended the Lie-group DDP of Boutselis and Theodorou by imposing SO(3) constraints on the trajectory optimization. (Alcan et al., 2023) `ev:cited` p. 3 ^alcan2023constrained-009
- The authors state the SO(3)-constrained DDP of Liu and Liu is not generalizable to nonlinear constraints on generic matrix Lie groups. (Alcan et al., 2023) `ev:asserted` p. 3 ^alcan2023constrained-010
- The problem considers systems whose states lie in the tangent bundle of a matrix Lie group, as configuration and velocity pairs. (Alcan et al., 2023) `ev:reported` p. 3 ^alcan2023constrained-011
- The constrained problem includes input box limits and a vector of differentiable nonlinear state constraints enforced at every time step. (Alcan et al., 2023) `ev:reported` p. 4 ^alcan2023constrained-012
- The authors seek feasible, possibly not globally optimal solutions, since finding the global minimum numerically is likely infeasible for high-dimensional nonlinear systems. (Alcan et al., 2023) `ev:asserted` p. 4 ^alcan2023constrained-013
- The perturbed state dynamics follow the error-state approach of Teng et al., defining configuration error as the nominal configuration inverse times the perturbed one. (Alcan et al., 2023) `ev:reported` p. 4 ^alcan2023constrained-014
- The perturbed state dynamics are linear in the configuration error but nonlinear in terms of the velocity dynamics. (Alcan et al., 2023) `ev:computed` p. 5 ^alcan2023constrained-015
- Constraints are approximated up to second order around the nominal state trajectory within the DDP framework. (Alcan et al., 2023) `ev:reported` p. 5 ^alcan2023constrained-016
- The authors propose mapping the geodesic distance between group elements to the tangent space of the current configuration and handling constraints there. (Alcan et al., 2023) `ev:asserted` p. 5 ^alcan2023constrained-017
- Configuration avoidance is formulated as an inequality constraint using an n-sphere centred at the avoided configuration with a restricted radius. (Alcan et al., 2023) `ev:reported` p. 5 ^alcan2023constrained-018
- Augmented Lagrangian methods keep Lagrange multiplier estimates, allowing convergence without penalty terms increasing infinitely, unlike the pure penalty method. (Alcan et al., 2023) `ev:cited` p. 5 ^alcan2023constrained-019
- A binary vector marks active constraints so satisfied constraints with near-zero dual variables add no penalty cost. (Alcan et al., 2023) `ev:reported` p. 6 ^alcan2023constrained-020
- The outer loop updates the Lagrange multipliers and multiplies the penalty by a fixed rate after each inner DDP solve. (Alcan et al., 2023) `ev:reported` p. 6 ^alcan2023constrained-021
- The outer loop continues while maximum constraint violation or maximum complementary dual exceeds a small threshold, within an iteration limit. (Alcan et al., 2023) `ev:reported` p. 6 ^alcan2023constrained-022
- Using a first-order dynamics approximation as in iLQR reduces computational cost but increases the iterations needed for convergence. (Alcan et al., 2023) `ev:asserted` p. 6 ^alcan2023constrained-023
- The forward pass updates the nominal trajectory by simulating the dynamics on the manifold itself starting from the initial state. (Alcan et al., 2023) `ev:reported` p. 7 ^alcan2023constrained-024
- Multiple controllers are generated in parallel during the backward pass by varying the regularization parameter ρ. (Alcan et al., 2023) `ev:reported` p. 7 ^alcan2023constrained-025
- The lowest-cost closed-loop rollout among the parallel controllers becomes the next nominal trajectory if it also improves on the previous iteration. (Alcan et al., 2023) `ev:reported` p. 8 ^alcan2023constrained-026
- Large regularization values make control updates more conservative, with better numerical stability but slower convergence, which the authors liken to Levenberg-Marquardt. (Alcan et al., 2023) `ev:asserted` p. 8 ^alcan2023constrained-027
- The method is implemented in Python with the jax library, chosen for easy parallelization and automatic differentiation. (Alcan et al., 2023) `ev:reported` p. 8 ^alcan2023constrained-028
- The initial penalty parameter was set to µ=1 and iteratively multiplied by γ=10 in the augmented Lagrangian outer loop. (Alcan et al., 2023) `ev:reported` p. 8 ^alcan2023constrained-029
- The constraint satisfaction tolerance threshold εc was set to 1e−3 for the augmented Lagrangian convergence check. (Alcan et al., 2023) `ev:reported` p. 8 ^alcan2023constrained-030
- Backward-pass regularization uses nρ=7, with ρ values spanning from an aggressive ρ0=1e−4 to a conservative ρ7=1000. (Alcan et al., 2023) `ev:reported` p. 8 ^alcan2023constrained-031
- The SE(3) test rotates the rigid body from identity to Rz(170◦) while translating it from (2, 2, 2) to (6, 2, 2). (Alcan et al., 2023) `ev:reported` p. 8 ^alcan2023constrained-032
- The SE(3) constraint-handling task must be completed within 6 seconds using a fixed time step of ∆t=0.1. (Alcan et al., 2023) `ev:reported` p. 8 ^alcan2023constrained-033
- During the SE(3) task, the configuration Rz(90◦) is considered unsafe and must be avoided by the optimized trajectory. (Alcan et al., 2023) `ev:reported` p. 9 ^alcan2023constrained-034
- A spherical obstacle at (4, 2, 2) with a radius of 1 must also be avoided in the SE(3) task. (Alcan et al., 2023) `ev:reported` p. 9 ^alcan2023constrained-035
- All inputs were restricted between -7.5 and 7.5 in the SE(3) constrained trajectory optimization task. (Alcan et al., 2023) `ev:reported` p. 9 ^alcan2023constrained-036
- Angular velocities were bounded at 0.5 when position x was less than 3, otherwise the upper bound became 2.0. (Alcan et al., 2023) `ev:reported` p. 9 ^alcan2023constrained-037
- The configuration avoidance constraint required the log-map distance from Rz(90) to be at least 0.4. (Alcan et al., 2023) `ev:reported` p. 9 ^alcan2023constrained-038
- Resultant SE(3) trajectories showed rotations around the x and y axes used to bypass the unsafe orientation. (Alcan et al., 2023) `ev:computed` p. 9 ^alcan2023constrained-039
- The spherical obstacle required a more circuitous route, with deviations along each axis yielding a collision-free trajectory. (Alcan et al., 2023) `ev:computed` p. 9 ^alcan2023constrained-040
- The angular velocity ωz saturated at 0.5 between 2-2.5 seconds, satisfying the position-dependent velocity constraint. (Alcan et al., 2023) `ev:computed` p. 9 ^alcan2023constrained-041
- For disturbance rejection, the DDP solution is used as a Lie-algebraic feedback policy combining optimal inputs with time-varying gains on the log-map configuration error. (Alcan et al., 2023) `ev:reported` p. 9 ^alcan2023constrained-042
- The disturbance test adds zero-mean Gaussian noise with σw = 0.001 to the SE(3) velocity dynamics. (Alcan et al., 2023) `ev:reported` p. 9 ^alcan2023constrained-043
- Open-loop and feedback policies were compared using 1000 sampled trajectories under noisy dynamics after converging on the deterministic system. (Alcan et al., 2023) `ev:reported` p. 9 ^alcan2023constrained-044
- Using the obtained feedback gains significantly reduced state variance compared with the open-loop policy, particularly in the vicinity of the goal points. (Alcan et al., 2023) `ev:computed` p. 9 ^alcan2023constrained-045
- The benchmark used SciPy's SLSQP optimizer and the Interior Point Optimizer IPOPT on the same SE(3) constrained task. (Alcan et al., 2023) `ev:reported` p. 10 ^alcan2023constrained-046
- The proposed DDP converged in less than 40 iterations, whereas IPOPT and SQP required 125 and 250 iterations, respectively. (Alcan et al., 2023) `ev:computed` p. 10 ^alcan2023constrained-047
- The authors attribute the gap to direct methods increasing decision variables as the horizon expands, searching a space with numerous equality and inequality constraints. (Alcan et al., 2023) `ev:asserted` p. 10 ^alcan2023constrained-048
- The quadrotor is modeled as an under-actuated rigid body driven by four motors whose speeds are assumed to be controlled nearly instantaneously. (Alcan et al., 2023) `ev:reported` p. 10 ^alcan2023constrained-049
- The quadrotor task moves from (3, 0.25, 2) to (2, 5, 2) within 4 seconds using a fixed time step ∆t = 0.02. (Alcan et al., 2023) `ev:reported` p. 10 ^alcan2023constrained-050
- Two rectangular boxes of dimensions (1.5, 0.1, 3.0) located at (0, 2.5, 3.0) and (3.6, 2.5, 3.0) must be avoided by the quadrotor. (Alcan et al., 2023) `ev:reported` p. 10 ^alcan2023constrained-051
- A configuration attainment constraint forced the quadrotor to achieve Ry(90) while passing between the boxes, testing for gimbal lock. (Alcan et al., 2023) `ev:reported` p. 10 ^alcan2023constrained-052
- The optimized quadrotor achieved the Ry(90) rotation without experiencing gimbal lock between time steps 1.2 - 1.9 sec. (Alcan et al., 2023) `ev:computed` p. 11 ^alcan2023constrained-053
- The optimized quadrotor trajectory required zero input during the Ry(90) rotation phase between 1.2 and 1.9 seconds. (Alcan et al., 2023) `ev:computed` p. 11 ^alcan2023constrained-054
- The quadrotor increased its z-position at the beginning, which the authors explain as preventing a fall during the zero-input period. (Alcan et al., 2023) `ev:asserted` p. 11 ^alcan2023constrained-055
- The authors conclude the method surpasses previous DDP methods restricted to specific matrix Lie groups by offering a more versatile solution. (Alcan et al., 2023) `ev:asserted` p. 11 ^alcan2023constrained-056
- The authors attribute faster convergence than direct methods to inherently incorporating the dynamics and leveraging second-order information for more accurate updates. (Alcan et al., 2023) `ev:asserted` p. 11 ^alcan2023constrained-057
- A stated limitation is that the deterministic transition dynamics of the controlled systems are assumed to be known. (Alcan et al., 2023) `ev:asserted` p. 11 ^alcan2023constrained-058
- Future work could learn the dynamics within the matrix Lie group representation to address the known-dynamics assumption. (Alcan et al., 2023) `ev:asserted` p. 11 ^alcan2023constrained-059
- The authors suggest incorporating model and measurement uncertainties with closed-loop uncertainty propagation could significantly enhance the robustness of the approach. (Alcan et al., 2023) `ev:asserted` p. 11 ^alcan2023constrained-060

## 🎯 Contributions

## 📖 Glossary

- **Matrix Lie group** — A group of invertible matrices that is also a smooth manifold, e.g. SO(3), SE(3).
- **Lie algebra** — The tangent space of a Lie group at the identity, a vector space.
- **Tangent bundle** — The set of all configuration and velocity pairs of a system on a manifold.
- **Differential Dynamic Programming (DDP)** — Iterative optimal control method using second-order expansions in backward and forward passes.
- **Iterative LQR (iLQR)** — DDP variant using only first-order dynamics derivatives, a Gauss-Newton approximation.
- **Augmented Lagrangian** — Constrained optimization that adds multiplier and penalty terms, updating multipliers in an outer loop.
- **Error-state** — Deviation of configuration and velocity from a nominal trajectory, expressed in the Lie algebra.
- **Adjoint map** — Linear map ad_ξ given by the Lie bracket, describing infinitesimal frame changes.
- **Gimbal lock** — Loss of one rotational degree of freedom when two Euler-angle axes align.
- **SE(3)** — Special Euclidean group of 3D rigid-body rotations and translations.

## ❓ Open questions

- How does the method perform when the transition dynamics are unknown and must be learned on the Lie group?
- How do model and measurement uncertainties, with closed-loop uncertainty propagation, change constraint satisfaction on matrix Lie groups?
- How does wall-clock time compare with SLSQP and IPOPT, given that the comparison is reported in iterations only?
- Does the approach transfer from simulation to physical robots such as real quadrotors?
- How sensitive is convergence to the choice of initial penalty µ, update rate γ and the regularization set P?

## 📝 Notes on reading

Version read: arXiv 2301.02018v3 (14 Oct 2024); the PDF title reads 'Lie-Algebraic Differential Dynamic Programming' where the registry title abbreviates it as DDP.

All experiments are numerical simulations, so their results are coded `ev:computed`.

Inconsistency on p. 9: the constraint set (41) and the task text define the unsafe configuration as Rz(90), but the results paragraph says rotations were observed to avoid the unsafe configuration of Rx(90◦); this looks like a typo in the paper.

Figures 2, 3, 5 and 6 (state, velocity and input trajectories; open-loop vs closed-loop spread under noise; the quadrotor path between boxes) and Fig. 4 (log ||U − U*|| vs iterations) were only described through the text; plot axis values extracted from the figures were not claimed. The stochastic comparison gives no numeric variance values, only the qualitative statement.

Equations (10), (11), (15), (19) and the algorithms were partly garbled by text extraction; the derivation steps were summarised rather than claimed term by term. The second-order logm approximation (17) used for configuration constraints, the ellipsoidal generalisation of restricted regions, and the jax autodiff of Jacobians and Hessians are described in the paper but were not claimed separately.

In the implementation, P={ρi = 10i−4|i = 0, ..., nρ} lost its superscript in extraction (it means 10^(i−4)).

## Suggested new concepts

- Lie-algebraic DDP — a family of DDP methods on matrix Lie groups (Boutselis and Theodorou, Teng et al., this paper) worth one note comparing them.
- Augmented Lagrangian constrained DDP — the outer-loop multiplier and penalty scheme used across constrained DDP/iLQR solvers such as ALTRO.
- Error-state dynamics on Lie groups — the linearised configuration-error model underlying both error-state MPC and this DDP.
- Configuration avoidance constraint — formulating unsafe orientations as tangent-space n-sphere constraints is reusable beyond DDP.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — DDP con restricciones en el álgebra (C.2).
