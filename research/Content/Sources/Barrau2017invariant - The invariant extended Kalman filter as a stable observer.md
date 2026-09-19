---
aliases: []
type: "source"
title: "The invariant extended Kalman filter as a stable observer"
citekey: "Barrau2017invariant"
doi: "10.48550/arXiv.1410.1465"
arxiv: "1410.1465"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1410.1465"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Axel Barrau", "Silvère Bonnabel"]
sha256: ["ca81b8ef0fc135e6d67a9531f30188476a2d927ee47a95e83d0f9da4f8a91e37"]
pdf: "Content/Papers/Barrau2017invariant.pdf"
topics: ["[[Matemáticas]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 70
---

📄 PDF: [[Barrau2017invariant.pdf]]

> [!abstract] One-sentence summary
> The paper characterizes the Lie group systems whose invariant estimation error propagates autonomously and log-linearly, and uses this to prove the invariant EKF is a locally asymptotically stable observer around any trajectory under the linear Kalman conditions, where the standard EKF has no such guarantee and can diverge.

## Abstract

We analyze the convergence aspects of the invariant extended Kalman filter (IEKF), when the latter is used as a deterministic non-linear observer on Lie groups, for continuous-time systems with discrete observations. One of the main features of invariant observers for left-invariant systems on Lie groups is that the estimation error is autonomous. In this paper we first generalize this result by characterizing the (much broader) class of systems for which this property holds. Then, we leverage the result to prove for those systems the local stability of the IEKF around any trajectory, under the standard conditions of the linear case. One mobile robotics example and one inertial navigation example illustrate the interest of the approach. Simulations evidence the fact that the EKF is capable of diverging in some challenging situations, where the IEKF with identical tuning keeps converging. (arXiv)

## 🧠 Key ideas (atomic)

- The paper analyzes the [[Invariant extended Kalman filter|invariant extended Kalman filter]] as a deterministic non-linear observer on Lie groups for continuous-time systems with discrete observations. (Barrau & Bonnabel, 2017) `ev:asserted` p. 1 ^barrau2017invariant-001
- Most papers on EKF stability assume the Kalman covariance eigenvalues about the estimated trajectory are lower and upper bounded by strictly positive scalars. (Barrau & Bonnabel, 2017) `ev:cited` p. 2 ^barrau2017invariant-002
- When the estimate is far from the true state, the EKF linearization yields an unadapted gain that may amplify the error. (Barrau & Bonnabel, 2017) `ev:asserted` p. 2 ^barrau2017invariant-003
- Only a few papers treat EKF stability without the covariance bound assumption, replacing it with second-order properties that can prove difficult to verify. (Barrau & Bonnabel, 2017) `ev:cited` p. 2 ^barrau2017invariant-004
- Beyond general theory, the authors note there are few engineering examples where the EKF is proved to be locally stable. (Barrau & Bonnabel, 2017) `ev:asserted` p. 2 ^barrau2017invariant-005
- In the car example, the time derivative of the plain difference error depends on both true and reference headings individually. (Barrau & Bonnabel, 2017) `ev:computed` p. 4 ^barrau2017invariant-006
- For the non-holonomic car, a non-linear error built from heading and rotated position differences obeys a linear autonomous equation, per Proposition 1. (Barrau & Bonnabel, 2017) `ev:computed` p. 4 ^barrau2017invariant-007
- Theorem 1 proves that state-trajectory independence of the left-invariant error is equivalent to that of the right-invariant error on Lie groups. (Barrau & Bonnabel, 2017) `ev:computed` p. 5 ^barrau2017invariant-008
- Theorem 1 shows the invariant errors are state-trajectory independent if and only if the dynamics satisfy a [[Group-affine dynamics|group-compatibility condition]], equation (7). (Barrau & Bonnabel, 2017) `ev:computed` p. 5 ^barrau2017invariant-009
- Remark 1 verifies that left-invariant dynamics, right-invariant dynamics, and combinations of both satisfy the [[Group-affine dynamics|group-compatibility condition]] (7). (Barrau & Bonnabel, 2017) `ev:computed` p. 6 ^barrau2017invariant-010
- When the Lie group is a vector space with standard addition, condition (7) reduces to affine dynamics, recovering the linear case. (Barrau & Bonnabel, 2017) `ev:computed` p. 6 ^barrau2017invariant-011
- Theorem 2 proves that the logarithm of the invariant error follows a linear differential equation, holding exactly for arbitrarily large errors between trajectories. (Barrau & Bonnabel, 2017) `ev:computed` p. 7 ^barrau2017invariant-012
- The paper derives the IEKF equations for continuous-time dynamics with discrete observations, which had already been done in a restricted setting. (Barrau & Bonnabel, 2017) `ev:asserted` p. 7 ^barrau2017invariant-013
- The authors cast the IEKF in a matrix Lie group framework, described as more handy than the usual abstract Lie group formulation. (Barrau & Bonnabel, 2017) `ev:asserted` p. 2 ^barrau2017invariant-014
- For left-invariant observations, the LIEKF updated error depends only on the error before update, independent of the true state. (Barrau & Bonnabel, 2017) `ev:computed` p. 8 ^barrau2017invariant-015
- For right-invariant observations, the RIEKF error update likewise does not depend on the true state of the system. (Barrau & Bonnabel, 2017) `ev:computed` p. 9 ^barrau2017invariant-016
- In a deterministic context, the noise covariance matrices Q and N are design parameters left free for the user to tune. (Barrau & Bonnabel, 2017) `ev:asserted` p. 9 ^barrau2017invariant-017
- The authors argue known sensor noise characteristics give the engineer a sensible first tuning of the IEKF parameter matrices. (Barrau & Bonnabel, 2017) `ev:asserted` p. 9 ^barrau2017invariant-018
- The IEKF conveys information about its own accuracy through the computed covariance Pt, unlike numerous non-linear observers on Lie groups. (Barrau & Bonnabel, 2017) `ev:asserted` p. 9 ^barrau2017invariant-019
- The authors state Pt has no rigorous interpretation in a deterministic context, although its information may prove useful in applications. (Barrau & Bonnabel, 2017) `ev:asserted` p. 10 ^barrau2017invariant-020
- Frame changes of sensor covariances yield trajectory-dependent tuning matrices, which makes the stability analysis a little more complicated. (Barrau & Bonnabel, 2017) `ev:asserted` p. 10 ^barrau2017invariant-021
- Neglecting second-order terms and treating the modified noise as white are approximations that would require proper justification in a stochastic setting. (Barrau & Bonnabel, 2017) `ev:asserted` p. 11 ^barrau2017invariant-022
- The linearized IEKF error equations mimic those of a Kalman filter designed for an auxiliary linear system with discrete measurements. (Barrau & Bonnabel, 2017) `ev:computed` p. 12 ^barrau2017invariant-023
- The IEKF gains are computed through a standard Riccati equation driven by the matrices A and H of the linearized error. (Barrau & Bonnabel, 2017) `ev:reported` p. 12 ^barrau2017invariant-024
- Deyst and Price proved in 1968 sufficient conditions for the Kalman filter to be a stable observer for linear time-varying deterministic systems. (Barrau & Bonnabel, 2017) `ev:cited` p. 13 ^barrau2017invariant-025
- Theorem 4 states the [[Invariant extended Kalman filter|IEKF]] is an asymptotically stable observer when the linear Kalman stability conditions hold about the true system trajectory. (Barrau & Bonnabel, 2017) `ev:computed` p. 13 ^barrau2017invariant-026
- In Theorem 4, the convergence radius is valid over the whole trajectory, independent of the initialization time. (Barrau & Bonnabel, 2017) `ev:computed` p. 13 ^barrau2017invariant-027
- During [[Invariant extended Kalman filter|IEKF]] propagation, the logarithmic error evolution is exact with no higher-order terms, which removes a main difficulty of EKF analysis. (Barrau & Bonnabel, 2017) `ev:computed` p. 14 ^barrau2017invariant-028
- For the IEKF, the Riccati equation depends on the estimate only through the tuning matrices Q-hat and N-hat. (Barrau & Bonnabel, 2017) `ev:computed` p. 14 ^barrau2017invariant-029
- Unlike usual results, Theorem 4 does not assume that the system linearized around the estimated trajectory is well-behaved. (Barrau & Bonnabel, 2017) `ev:asserted` p. 14 ^barrau2017invariant-030
- With sufficiently many sensors, the authors argue the linearized system around the true trajectory can generally be asserted in advance to possess all desired properties. (Barrau & Bonnabel, 2017) `ev:asserted` p. 14 ^barrau2017invariant-031
- Theorem 5 states that a constant propagation matrix with bounded covariances and a detectable, reachable linearized system guarantees IEKF asymptotic stability. (Barrau & Bonnabel, 2017) `ev:computed` p. 14 ^barrau2017invariant-032
- The mobile robotics example is a non-holonomic car with odometer velocity and steering inputs, observed through GPS position or landmark range-and-bearing. (Barrau & Bonnabel, 2017) `ev:reported` p. 15 ^barrau2017invariant-033
- To fit the framework, the car system is embedded in the matrix Lie group SE(2) of direct planar isometries. (Barrau & Bonnabel, 2017) `ev:reported` p. 15 ^barrau2017invariant-034
- Proposition 3 states the LIEKF is asymptotically stable about any trajectory if displacement between GPS measurements is lower bounded and velocity is bounded. (Barrau & Bonnabel, 2017) `ev:computed` p. 18 ^barrau2017invariant-035
- It seems very difficult to improve the Proposition 3 assumptions, as heading becomes unobservable if the car occupies the same place at every position measurement. (Barrau & Bonnabel, 2017) `ev:asserted` p. 18 ^barrau2017invariant-036
- Proposition 4 states that observing at least two distinct landmarks makes the IEKF asymptotically stable about any bounded trajectory. (Barrau & Bonnabel, 2017) `ev:computed` p. 18 ^barrau2017invariant-037
- In the car simulation, the vehicle drives a 10-meter diameter circle for 40 seconds with 100 Hz odometry and 1 Hz GPS. (Barrau & Bonnabel, 2017) `ev:reported` p. 18 ^barrau2017invariant-038
- Both car filters share identical design parameters, interpretable as odometer and GPS noise covariances, with highly precise linear velocity assumed. (Barrau & Bonnabel, 2017) `ev:reported` p. 18 ^barrau2017invariant-039
- The car simulation tests initial heading errors of 1 and 45 degrees, with the initial position always assumed known. (Barrau & Bonnabel, 2017) `ev:reported` p. 18 ^barrau2017invariant-040
- For a small initial heading error, the EKF and IEKF behave similarly for a long time in the car simulation. (Barrau & Bonnabel, 2017) `ev:measured` p. 18 ^barrau2017invariant-041
- For the larger initial heading error in the car simulation, the [[Invariant extended Kalman filter|IEKF]], adapted to the system structure, completely outperforms the EKF. (Barrau & Bonnabel, 2017) `ev:measured` p. 19 ^barrau2017invariant-042
- The Figure 1 caption states the IEKF keeps ensuring rapid estimation error decrease under a large initial angle error. (Barrau & Bonnabel, 2017) `ev:measured` p. 35 ^barrau2017invariant-043
- The second example estimates the orientation, velocity, and position of a rigid body from inertial sensors and relative landmark observations. (Barrau & Bonnabel, 2017) `ev:reported` p. 19 ^barrau2017invariant-044
- To their knowledge, this is the first application of invariant Lie group observers to full navigation with landmarks, apart from their conference paper. (Barrau & Bonnabel, 2017) `ev:asserted` p. 19 ^barrau2017invariant-045
- The navigation system does not fit the usual autonomous-error framework, yet Theorem 1 shows it still yields an autonomous error equation. (Barrau & Bonnabel, 2017) `ev:computed` p. 19 ^barrau2017invariant-046
- The multiplicative EKF is the industrial state of the art for this navigation example, owing to good performance and easy tuning. (Barrau & Bonnabel, 2017) `ev:asserted` p. 19 ^barrau2017invariant-047
- To the authors' knowledge, the multiplicative EKF is nowhere proved to possess stability properties as a non-linear observer. (Barrau & Bonnabel, 2017) `ev:asserted` p. 19 ^barrau2017invariant-048
- The noisy navigation system is embedded in the group of double homogeneous matrices, as already noticed in the preliminary work. (Barrau & Bonnabel, 2017) `ev:reported` p. 20 ^barrau2017invariant-049
- Proposition 5 states the navigation dynamics function is neither left nor right invariant, yet it satisfies relation (7). (Barrau & Bonnabel, 2017) `ev:computed` p. 20 ^barrau2017invariant-050
- Theorem 6 states that observing three non-collinear points makes the navigation IEKF asymptotically stable about any bounded trajectory. (Barrau & Bonnabel, 2017) `ev:computed` p. 22 ^barrau2017invariant-051
- The Theorem 6 proof shows the stacked matrix of H and H times the propagation matrix has rank 9. (Barrau & Bonnabel, 2017) `ev:computed` p. 22 ^barrau2017invariant-052
- In the navigation simulation, the vehicle drives a 10-meter diameter circle in 30 seconds, observing three features every second. (Barrau & Bonnabel, 2017) `ev:reported` p. 22 ^barrau2017invariant-053
- Inertial measurements arrive at 100 Hz in the navigation simulation, where the IEKF is compared to a state-of-the-art multiplicative EKF. (Barrau & Bonnabel, 2017) `ev:reported` p. 22 ^barrau2017invariant-054
- Both navigation simulations share initial standard deviations of 15 degrees for attitude and 1 meter for position. (Barrau & Bonnabel, 2017) `ev:reported` p. 23 ^barrau2017invariant-055
- The small process noise matrix Q1 was deliberately chosen to challenge EKF-like methods, though reasonable for high-precision inertial navigation. (Barrau & Bonnabel, 2017) `ev:reported` p. 23 ^barrau2017invariant-056
- With the tight tuning Q1, the EKF diverges in the navigation simulation even though no noise was added. (Barrau & Bonnabel, 2017) `ev:measured` p. 23 ^barrau2017invariant-057
- The authors attribute the EKF divergence purely to non-linearity, since small gains cannot correct errors introduced during the transitory phase. (Barrau & Bonnabel, 2017) `ev:asserted` p. 23 ^barrau2017invariant-058
- With the same tuning Q1, the IEKF attitude and position errors go to zero, in accordance with Theorem 6. (Barrau & Bonnabel, 2017) `ev:measured` p. 23 ^barrau2017invariant-059
- With the inflated process noise matrix Q2, the EKF remains much slower to converge than the IEKF in the navigation simulation. (Barrau & Bonnabel, 2017) `ev:measured` p. 23 ^barrau2017invariant-060
- The Figure 2 caption states inflating Q to Q2 prevents the EKF from diverging in the navigation simulation. (Barrau & Bonnabel, 2017) `ev:measured` p. 36 ^barrau2017invariant-061
- The authors argue robust tuning gives no robustness guarantee, since Q and N were chosen for one specific trajectory. (Barrau & Bonnabel, 2017) `ev:asserted` p. 23 ^barrau2017invariant-062
- Arbitrarily inflating Q by several orders of magnitude makes the covariance Pt lose its interpretability as an indication of observer accuracy. (Barrau & Bonnabel, 2017) `ev:asserted` p. 23 ^barrau2017invariant-063
- The authors conclude the IEKF is a viable alternative to the EKF for this navigation problem, given its guaranteed properties. (Barrau & Bonnabel, 2017) `ev:asserted` p. 24 ^barrau2017invariant-064
- The conclusion claims simulations confirm the IEKF is always superior to the EKF, outperforming it in challenging situations. (Barrau & Bonnabel, 2017) `ev:asserted` p. 24 ^barrau2017invariant-065
- The authors state the IEKF remains similar to the EKF in terms of tuning, implementation, and computational load. (Barrau & Bonnabel, 2017) `ev:asserted` p. 24 ^barrau2017invariant-066
- No matrix exponentiation is actually needed for the paper's matrix Lie groups, as closed-form exponential formulas exist. (Barrau & Bonnabel, 2017) `ev:asserted` p. 24 ^barrau2017invariant-067
- Lemma 2 proves the error-propagation flow preserves products, mapping the product of two initial errors to the product of their flows. (Barrau & Bonnabel, 2017) `ev:computed` p. 26 ^barrau2017invariant-068
- The authors note the flow's behavior infinitely close to identity dictates its behavior arbitrarily far from it. (Barrau & Bonnabel, 2017) `ev:asserted` p. 26 ^barrau2017invariant-069
- The Theorem 4 proof shows second-order update terms are compensated by the exponential decay of the linear error flow. (Barrau & Bonnabel, 2017) `ev:computed` p. 27 ^barrau2017invariant-070

## 🎯 Contributions

## 📖 Glossary

- **Invariant extended Kalman filter (IEKF)** — EKF variant for Lie group states, linearizing an invariant error instead of a vector difference.
- **Left-invariant error** — Error inverse(true state) times estimate, invariant to left multiplication of both.
- **Right-invariant error** — Error estimate times inverse(true state), invariant to right multiplication of both.
- **State-trajectory independent propagation** — Error dynamics depending only on the error and inputs, not the true trajectory.
- **Log-linear property** — The Lie logarithm of the invariant error obeys an exact linear differential equation.
- **Matrix Lie group** — Set of invertible square matrices closed under products and inverses, containing identity.
- **SE(2)** — Group of direct planar isometries: planar rotation plus translation.
- **SE2(3)** — Group of double direct spatial isometries holding attitude, velocity and position.
- **Asymptotically stable observer** — Observer whose estimate converges to the true trajectory from sufficiently close initializations.
- **Multiplicative EKF (MEKF)** — Industrial EKF variant linearizing attitude error multiplicatively via a first-order rotation expansion.
- **Robust tuning** — Artificially inflating the process noise matrix Q to avoid EKF convergence problems.

## ❓ Open questions

- Can the local convergence guarantee of the IEKF be extended to a global or quantified basin of attraction?
- How do the deterministic stability results carry over to the stochastic setting, where the neglected terms and white-noise approximations need justification?
- What guarantees hold for systems on Lie groups that do not satisfy the group-compatibility condition (7)?
- How does the IEKF behave on real sensor data rather than the two noise-free simulated scenarios?
- Does the IEKF advantage persist when sensor biases are included in the state, which breaks the group structure used here?

## 📝 Notes on reading

The cached text is arXiv 1410.1465v4 dated 19 Oct 2015; the metadata year is 2017 (the journal publication). Figures 1 and 2 (pp. 35-36) were only readable through their captions; the claimed simulation outcomes rest on the text of Sections 4.4 and 5.4 and the captions, with no numeric error values reported. The tuning matrices of both simulations (N = I2, Q = diag((pi/180)^2, 1e-4, 1e-4) for the car; N with 1e-2 blocks, Q1 with 1e-8 blocks and Q2 with 1e-4 blocks for navigation) are garbled in the extraction and were not claimed as numbers. Internal inconsistencies: Proposition 3 refers to the LIEKF derived in Section 4.2.4, but Section 4.2.4 derives the RIEKF (the LIEKF is in Section 4.2.3); the Proposition 3 bound is written on ut, which the model defines as a function of the steering angle, while the text calls it the input velocity; Section 3.3 is headed IEFK; Section 4.3.2 cites output (40) while Section 4.2.4 uses (43). The introduction (p. 2) says the IEKF is always superior to the EKF, a claim based only on two simulated scenarios. Proofs of Theorem 2 (Appendix B) and Theorem 4 (Appendix C) were read but only their key steps were claimed.

## Suggested new concepts

- Invariant extended Kalman filter — central Lie group filtering method reused across navigation and robotics estimation papers.
- Log-linear error property — the key structural result that makes invariant filter stability analysis tractable.
- Group-affine dynamics — the class of systems satisfying condition (7), generalizing linear systems on Lie groups.
- Observer stability of the EKF — recurring topic contrasting classical EKF assumptions with invariant filtering guarantees.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Error invariante en grupos de Lie y garantías de estabilidad.
- **[[03_aplicaciones_vision_por_computador]]** — IEKF: error autónomo en grupos de Lie
