---
aliases: []
type: "source"
title: "Differential Dynamic Programming on Lie Groups"
citekey: "Boutselis2018differential"
doi: "10.48550/arXiv.1809.07883"
arxiv: "1809.07883"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1809.07883"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["George I. Boutselis", "Evangelos Theodorou"]
sha256: ["0c48cd345d5394f841d446621067b8dd0f92e373b8c049660d5db2f525b3cce4"]
pdf: "Content/Papers/Boutselis2018differential.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Boutselis2018differential.pdf]]

> [!abstract] One-sentence summary
> The paper derives a coordinate-free Differential Dynamic Programming algorithm for discrete-time optimal control on Lie groups, with second-order dynamics expansions, a convergence proof, and a satellite-attitude simulation in which it beats an SQP solver.

## Abstract

We develop a discrete-time optimal control framework for systems evolving on Lie groups. Our work generalizes the original Differential Dynamic Programming method, by employing a coordinate-free, Lie-theoretic approach for its derivation. A key element lies, specifically, in the use of quadratic expansion schemes for cost functions and dynamics defined on manifolds. The obtained algorithm iteratively optimizes local approximations of the control problem, until reaching a (sub)optimal solution. On the theoretical side, we also study the conditions under which convergence is attained. Details about the behavior and implementation of our method are provided through a simulated example on T SO(3). (arXiv)

## 🧠 Key ideas (atomic)

- The paper formulates a Lie-theoretic, coordinate-free version of Differential Dynamic Programming for discrete-time optimal control of systems evolving on Lie groups. (Boutselis & Theodorou, 2018) `ev:asserted` p. 1 ^boutselis2018differential-001
- The authors state that, to their knowledge, the controls literature lacks a rigorous extension of DDP to non-flat configuration manifolds. (Boutselis & Theodorou, 2018) `ev:asserted` p. 1 ^boutselis2018differential-002
- Differential Dynamic Programming was originally proposed by Mayne and Jacobson for solving discrete and continuous optimal control problems. (Boutselis & Theodorou, 2018) `ev:cited` p. 1 ^boutselis2018differential-003
- The authors describe scalability, fast convergence rate, and feedback control policies as some of the major attributes of DDP. (Boutselis & Theodorou, 2018) `ev:asserted` p. 1 ^boutselis2018differential-004
- Earlier works using DDP in geometric control briefly provided the final form of the algorithm for certain matrix Lie groups and problem definitions. (Boutselis & Theodorou, 2018) `ev:cited` p. 1 ^boutselis2018differential-005
- Those earlier geometric DDP expressions were justified on the basis of the traditional, vector-based DDP formulation of Mayne and Jacobson. (Boutselis & Theodorou, 2018) `ev:cited` p. 1 ^boutselis2018differential-006
- The authors judge that prior geometric optimal control approaches based on necessary optimality conditions depend heavily on problem specifications. (Boutselis & Theodorou, 2018) `ev:cited` p. 1 ^boutselis2018differential-007
- In contrast to earlier geometric DDP works, the paper considers second-order expansions of the dynamics to help increase the convergence rate. (Boutselis & Theodorou, 2018) `ev:asserted` p. 1 ^boutselis2018differential-008
- The derivation follows the original DDP method, with each step modified to account for Lie group formulations of dynamics and costs. (Boutselis & Theodorou, 2018) `ev:asserted` p. 1 ^boutselis2018differential-009
- The problem is a discrete-time, finite-horizon optimal control problem with running costs, a terminal cost, and a fixed initial state. (Boutselis & Theodorou, 2018) `ev:reported` p. 3 ^boutselis2018differential-010
- The derivation assumes the problem admits a solution, with the cost and state transition maps twice differentiable at every time step. (Boutselis & Theodorou, 2018) `ev:reported` p. 3 ^boutselis2018differential-011
- The authors seek a method giving tractable solutions, possibly at the expense of global optimality, since global minima are tedious to obtain numerically. (Boutselis & Theodorou, 2018) `ev:asserted` p. 3 ^boutselis2018differential-012
- Perturbed state trajectories are written in exponential coordinates about the nominal trajectory, with the perturbation vectors lying in the Lie algebra. (Boutselis & Theodorou, 2018) `ev:reported` p. 3 ^boutselis2018differential-013
- The value function expansion assumes a twice differentiable value function on a group endowed with the (0), (+), or (-) Cartan connection. (Boutselis & Theodorou, 2018) `ev:reported` p. 3 ^boutselis2018differential-014
- Left-trivializing the value function differential and Hessian lets the whole algorithm be derived by solely using operations on the Lie algebra and its dual. (Boutselis & Theodorou, 2018) `ev:computed` p. 3 ^boutselis2018differential-015
- By defining a basis for the Lie algebra and its dual, all algorithm steps can be implemented through standard matrix/vector products. (Boutselis & Theodorou, 2018) `ev:asserted` p. 4 ^boutselis2018differential-016
- Minimizing the quadratic Q-function expansion yields a locally optimal control deviation with a feedforward term plus a feedback term in the state perturbation. (Boutselis & Theodorou, 2018) `ev:computed` p. 4 ^boutselis2018differential-017
- Mimicking Euclidean DDP work by Liao, an external parameter gamma in (0,1] scales the feedforward part of the control update. (Boutselis & Theodorou, 2018) `ev:reported` p. 4 ^boutselis2018differential-018
- The authors argue that gamma allows descent directions even when the quadratic expansions do not fully capture the nature of the problem. (Boutselis & Theodorou, 2018) `ev:asserted` p. 4 ^boutselis2018differential-019
- The trivialized gradient and Hessian of the value function are backpropagated along the nominal trajectory, starting from the terminal-cost derivatives. (Boutselis & Theodorou, 2018) `ev:computed` p. 4 ^boutselis2018differential-020
- In Algorithm 1, the line-search parameter is repeatedly multiplied by a factor h in (0,1) until the new cost does not exceed the nominal cost. (Boutselis & Theodorou, 2018) `ev:reported` p. 5 ^boutselis2018differential-021
- Earlier geometric DDP works employed a first-order linearization for mechanical systems, for which they did not provide a mathematical proof. (Boutselis & Theodorou, 2018) `ev:cited` p. 5 ^boutselis2018differential-022
- The paper derives a second-order expansion of the state perturbations for generic classes of discrete mechanical dynamics using the [[Baker-Campbell-Hausdorff formula]]. (Boutselis & Theodorou, 2018) `ev:computed` p. 5 ^boutselis2018differential-023
- The mechanical system state is decomposed into a pose on a Lie group and a body-fixed velocity in its Lie algebra. (Boutselis & Theodorou, 2018) `ev:reported` p. 5 ^boutselis2018differential-024
- The simplest discretization is forward Euler, pairing a reconstruction equation for the pose with an explicit update of the body-fixed velocity. (Boutselis & Theodorou, 2018) `ev:reported` p. 5 ^boutselis2018differential-025
- The pose-perturbation expansion neglects third-order terms in the time step, since one typically has a time step no larger than 0.1. (Boutselis & Theodorou, 2018) `ev:reported` p. 6 ^boutselis2018differential-026
- The authors remark that the [[Baker-Campbell-Hausdorff formula|Baker-Campbell-Hausdorff expansion]] used for the pose perturbation does not depend on the selected affine connection. (Boutselis & Theodorou, 2018) `ev:asserted` p. 6 ^boutselis2018differential-027
- Implicit integrators achieve improved numerical performance compared to explicit discretization methods, according to the works the authors cite. (Boutselis & Theodorou, 2018) `ev:cited` p. 6 ^boutselis2018differential-028
- For implicit transition dynamics, the required derivatives of the velocity update are obtained through implicit differentiation of the discrete dynamics equation. (Boutselis & Theodorou, 2018) `ev:computed` p. 6 ^boutselis2018differential-029
- For implicit transition dynamics, the Hessians of the velocity update rely explicitly on its first-order derivatives. (Boutselis & Theodorou, 2018) `ev:computed` p. 7 ^boutselis2018differential-030
- Earlier Euclidean analyses showed that, under some mild conditions, the original DDP method will always converge to a solution. (Boutselis & Theodorou, 2018) `ev:cited` p. 7 ^boutselis2018differential-031
- The authors note that those earlier Euclidean convergence analyses were limited to optimal control problems with terminal costs only. (Boutselis & Theodorou, 2018) `ev:cited` p. 7 ^boutselis2018differential-032
- Theorem V.1 shows the cost derivative along the DDP update equals minus gamma times a sum of Q-function terms, plus second-order terms in gamma. (Boutselis & Theodorou, 2018) `ev:computed` p. 7 ^boutselis2018differential-033
- The convergence analysis in Assumption V.1 assumes that the search space of the control sequence is compact. (Boutselis & Theodorou, 2018) `ev:reported` p. 7 ^boutselis2018differential-034
- The convergence analysis assumes that the control Hessian of the Q function remains positive definite at every time step. (Boutselis & Theodorou, 2018) `ev:reported` p. 7 ^boutselis2018differential-035
- Corollary V.1 states that, under these assumptions, Algorithm 1 will converge to a stationary solution of the optimal control problem. (Boutselis & Theodorou, 2018) `ev:computed` p. 8 ^boutselis2018differential-036
- Positive definiteness of the control Hessian of Q is enforced by adding a regularization parameter times the identity at each time step. (Boutselis & Theodorou, 2018) `ev:reported` p. 8 ^boutselis2018differential-037
- The authors state that a theoretical analysis of the convergence rate of DDP on Lie groups is a topic under investigation. (Boutselis & Theodorou, 2018) `ev:asserted` p. 8 ^boutselis2018differential-038
- The simulated example is a rigid satellite whose state evolves on the tangent bundle TSO(3), discretized with the forward Euler method. (Boutselis & Theodorou, 2018) `ev:reported` p. 8 ^boutselis2018differential-039
- The satellite cost penalizes high control inputs as well as terminal attitude and body-fixed velocity far from the desired values. (Boutselis & Theodorou, 2018) `ev:reported` p. 8 ^boutselis2018differential-040
- The authors observe that the resulting matrix expressions for the Q and value-function derivatives accord, up to first order only, with earlier geometric DDP works. (Boutselis & Theodorou, 2018) `ev:asserted` p. 9 ^boutselis2018differential-041
- Convergence was declared when the absolute change in cost between consecutive iterations fell to 10−8 or below. (Boutselis & Theodorou, 2018) `ev:reported` p. 9 ^boutselis2018differential-042
- When the control Hessian of Q was not positive definite, the regularization parameter was multiplied by 1.9 until the condition held. (Boutselis & Theodorou, 2018) `ev:reported` p. 9 ^boutselis2018differential-043
- The line-search reduction factor h in step 21 of Algorithm 1 was set to 1/3 in the simulations. (Boutselis & Theodorou, 2018) `ev:reported` p. 9 ^boutselis2018differential-044
- In the satellite attitude simulations, DDP was initialized with a nominal control sequence consisting entirely of zero controls. (Boutselis & Theodorou, 2018) `ev:reported` p. 9 ^boutselis2018differential-045
- According to Table I, the simulations used a time step of 0.01 and a final time of 3 for the satellite problem. (Boutselis & Theodorou, 2018) `ev:reported` p. 9 ^boutselis2018differential-046
- According to Table I, the satellite inertia tensor was set to diag(10,11.1,13) with the control torque matrix equal to the identity. (Boutselis & Theodorou, 2018) `ev:reported` p. 9 ^boutselis2018differential-047
- The first-order linearization scheme does much better than the full second-order expansion at the early stages of optimization. (Boutselis & Theodorou, 2018) `ev:measured` p. 9 ^boutselis2018differential-048
- The first-order linearization scheme fails to give superlinear convergence in the simulated satellite attitude control problem. (Boutselis & Theodorou, 2018) `ev:measured` p. 9 ^boutselis2018differential-049
- Using the second-order terms makes the control Hessian of Q non positive definite in the first iterations, which slows down cost improvement. (Boutselis & Theodorou, 2018) `ev:measured` p. 9 ^boutselis2018differential-050
- As the solution is approached, the higher-order expansion terms allow for quadratic-like convergence rates in the simulated example. (Boutselis & Theodorou, 2018) `ev:measured` p. 9 ^boutselis2018differential-051
- The authors propose starting with linear terms only and switching to the full expansion once the relative cost falls below a bound sigma. (Boutselis & Theodorou, 2018) `ev:asserted` p. 9 ^boutselis2018differential-052
- With the switching bound sigma set to 0.1, the switch to the full expansion occurred after the first DDP iteration. (Boutselis & Theodorou, 2018) `ev:measured` p. 9 ^boutselis2018differential-053
- As a benchmark, MATLAB's built-in SQP implementation solved the same problem with all states and controls stacked as decision variables. (Boutselis & Theodorou, 2018) `ev:reported` p. 9 ^boutselis2018differential-054
- The SQP benchmark received derivative information for the cost and constraints, with a dynamics feasibility tolerance of 10−6. (Boutselis & Theodorou, 2018) `ev:reported` p. 9 ^boutselis2018differential-055
- DDP and the SQP benchmark reach the same solution, but DDP requires much fewer iterations to get there. (Boutselis & Theodorou, 2018) `ev:measured` p. 9 ^boutselis2018differential-056
- The MATLAB implementation of DDP converged in 1.9 s, with the SQP solver being approximately 300 times slower. (Boutselis & Theodorou, 2018) `ev:measured` p. 9 ^boutselis2018differential-057
- The SQP solver did not yield feasible dynamics until the 9th iteration of the benchmark comparison. (Boutselis & Theodorou, 2018) `ev:measured` p. 9 ^boutselis2018differential-058
- The authors attribute the SQP gap to a larger decision vector, many equality constraints, and cubic scaling with the time horizon. (Boutselis & Theodorou, 2018) `ev:asserted` p. 9 ^boutselis2018differential-059
- The authors conclude that geometric DDP preserved important characteristics of the original scheme and outperformed standard optimization methods in simulation. (Boutselis & Theodorou, 2018) `ev:asserted` p. 9 ^boutselis2018differential-060
- The authors state that a convergence-rate analysis of geometric DDP is necessary to establish the properties of the algorithm. (Boutselis & Theodorou, 2018) `ev:asserted` p. 9 ^boutselis2018differential-061
- The work relies on the Cartan-Schouten connections, and for a different affine connection the form of Algorithm 1 is expected to vary. (Boutselis & Theodorou, 2018) `ev:asserted` p. 10 ^boutselis2018differential-062
- The authors suggest a stochastic version of DDP on Lie groups could further increase its applicability to real autonomous systems. (Boutselis & Theodorou, 2018) `ev:asserted` p. 10 ^boutselis2018differential-063
- In Figure 3, the combined scheme using higher-order terms from the second iteration obtains the solution in fewer steps than either scheme alone. (Boutselis & Theodorou, 2018) `ev:measured` p. 10 ^boutselis2018differential-064
- For all three Cartan-Schouten connections, only a symmetric second-order term remains in the quadratic value-function expansion. (Boutselis & Theodorou, 2018) `ev:computed` p. 10 ^boutselis2018differential-065
- A direct Taylor expansion of the pose-perturbation map gives a first-order result matching the linear terms of the [[Baker-Campbell-Hausdorff formula|BCH-based expansion]]. (Boutselis & Theodorou, 2018) `ev:computed` p. 11 ^boutselis2018differential-066
- The authors prefer the [[Baker-Campbell-Hausdorff formula|BCH formula]] for quadratic terms, noting it yields a connection-independent scheme relying on simple group operations. (Boutselis & Theodorou, 2018) `ev:asserted` p. 11 ^boutselis2018differential-067

## 🎯 Contributions

## 📖 Glossary

- **Differential Dynamic Programming (DDP)** — Iterative trajectory optimizer using local quadratic expansions of the value function along a nominal trajectory.
- **Lie group** — Smooth manifold with a compatible group structure, e.g. rotations SO(3) or rigid motions SE(3).
- **Lie algebra** — Tangent space at the group identity, where perturbations and linearizations are expressed.
- **Exponential map** — Map from the Lie algebra to the group, used as local coordinates around nominal states.
- **Cartan-Schouten connection** — One of three left-invariant affine connections, (-), (+), (0), with connection function kappa times the bracket.
- **Baker-Campbell-Hausdorff formula** — Series expressing the product of two group exponentials as a single exponential.
- **Q function** — Running cost plus next-step value function, expanded to second order to compute control updates.
- **TSO(3)** — Tangent bundle of the rotation group, the state space of rigid-body attitude with angular velocity.
- **Trivialized derivative** — Derivative pulled back to the Lie algebra or its dual via left translation.

## ❓ Open questions

- Can locally quadratic convergence of DDP on Lie groups be proven theoretically, rather than only observed in simulation?
- How does Algorithm 1 change for affine connections other than the Cartan-Schouten family?
- What would a stochastic version of DDP on Lie groups look like, and how would it perform on real autonomous systems?
- How does the method handle control or state constraints, which the problem formulation does not include?
- How robust is the heuristic switching rule (bound sigma) between first- and second-order expansions across problems?

## 📝 Notes on reading

- The cached text is the arXiv v1 preprint (1809.07883v1, 20 Sep 2018); its title adds the subtitle "Derivation, Convergence Analysis and Numerical Results".
- Most of the paper is mathematical derivation (equations 3–52); equations were extracted with broken layout and are described in words rather than transcribed.
- Table I (p. 9) is partly garbled: the weighting matrices SR, SΩ appear as "104I3", likely 10^4 I3; this value and the desired attitude Rotx(30°)Rotz(70°) were not claimed.
- Figure 2 (p. 10) shows the obtained quaternion attitude, body-fixed velocities and controls over 3 time units; Figure 3 plots ||U − U*|| per iteration for first-order, second-order and combined schemes; Figure 4 plots total cost per iteration for DDP versus SQP. Only the captions' statements were claimed.
- The convergence section derives descent for small gamma; the regularization and line-search are the practical devices that enforce Assumption V.1 in the implementation.

## Suggested new concepts

- Differential Dynamic Programming — core trajectory-optimization method that several control papers in the vault build on.
- Optimal control on Lie groups — geometric, coordinate-free formulation of control for rotating and rigid-body systems.
- Baker-Campbell-Hausdorff formula — recurring tool for linearizing dynamics on matrix Lie groups.
- Sequential quadratic programming as a trajectory-optimization baseline — frequent benchmark against shooting methods like DDP.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — DDP libre de coordenadas en grupos de Lie (C.2).
