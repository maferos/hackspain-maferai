---
aliases: []
type: "source"
title: "Lie Algebraic Cost Function Design for Control on Lie Groups"
citekey: "Teng2022lie"
doi: "10.48550/arXiv.2204.09177"
arxiv: "2204.09177"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2204.09177"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Sangli Teng", "William Clark", "Anthony Bloch", "Ram Vasudevan", "Maani Ghaffari"]
sha256: ["7a6df199a4405c94039dd8797a3654c09477dc3aa11c0c8c0970e973735ed7db"]
pdf: "Content/Papers/Teng2022lie.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[Teng2022lie.pdf]]

> [!abstract] One-sentence summary
> The paper designs control cost functions on Lie groups as quadratic functions in the Lie algebra, via their gradient under a left-invariant metric, yielding exponentially stable PD tracking on SO(3) that stays fast near a π error and an iLQR that converges faster than DDP with a trace-based cost from a poor initialization.

## Abstract

This paper presents a control framework on Lie groups by designing the control objective in its Lie algebra. Control on Lie groups is challenging due to its nonlinear nature and difficulties in system parameterization. Existing methods to design the control objective on a Lie group and then derive the gradient for controller design are non-trivial and can result in slow convergence in tracking control. We show that with a proper left-invariant metric, setting the gradient of the cost function as the tracking error in the Lie algebra leads to a quadratic Lyapunov function that enables globally exponential convergence. In the PD control case, we show that our controller can maintain an exponential convergence rate even when the initial error is approaching $π$ in SO(3). We also show the merit of this proposed framework in trajectory optimization. The proposed cost function enables the iterative Linear Quadratic Regulator (iLQR) to converge much faster than the Differential Dynamic Programming (DDP) with a well-adopted cost function when the initial trajectory is poorly initialized on SO(3). (arXiv)

## 🧠 Key ideas (atomic)

- Trace function configuration errors, used widely for rotational motion, may lead to slow error convergence when the rotational error is large (Teng et al., 2022) `ev:cited` p. 1 ^teng2022lie-001
- Earlier controllers using the logarithmic error, in references 3 and 16, do not prove the stability property, according to the authors (Teng et al., 2022) `ev:cited` p. 1 ^teng2022lie-002
- The logarithmic-error stability proof in reference 15 is specific to SO(3), making it less general for systems on Lie groups (Teng et al., 2022) `ev:cited` p. 1 ^teng2022lie-003
- Existing Lie group DDP and projection operator methods mainly apply to general Riemannian geometries, not fully utilizing the symmetry of Lie groups (Teng et al., 2022) `ev:cited` p. 1 ^teng2022lie-004
- According to the authors, designing the cost function in the Lie algebra enables a more concise formulation for all connected matrix Lie groups (Teng et al., 2022) `ev:asserted` p. 1 ^teng2022lie-005
- The authors identify bridging the cost function in the Lie algebra with the equation of motion on the group as the key novelty (Teng et al., 2022) `ev:asserted` p. 1 ^teng2022lie-006
- For SO(3), a cost function built from the trace function has a gradient that vanishes when the configuration error becomes large (Teng et al., 2022) `ev:asserted` p. 1 ^teng2022lie-007
- The first contribution is a control framework on Lie groups with the gradient of the cost function described in the corresponding Lie algebra (Teng et al., 2022) `ev:asserted` p. 2 ^teng2022lie-008
- The tracking error is defined on the group as the inverse of the nominal configuration multiplied by the actual configuration (Teng et al., 2022) `ev:asserted` p. 2 ^teng2022lie-009
- The tracking goal is to drive the configuration error from its initial condition to the identity element of the group (Teng et al., 2022) `ev:asserted` p. 2 ^teng2022lie-010
- An error function is defined as a positive definite function on the group that vanishes if and only if the error is identity (Teng et al., 2022) `ev:asserted` p. 2 ^teng2022lie-011
- General cost functions designed on manifolds in prior work introduce difficulties when deriving the gradient or Hessian matrix, according to the authors (Teng et al., 2022) `ev:cited` p. 3 ^teng2022lie-012
- Instead of the error function itself, the authors design its gradient and then show the corresponding error function satisfies stability properties (Teng et al., 2022) `ev:asserted` p. 3 ^teng2022lie-013
- The metric is a left-invariant inner product on the group defined by a positive definite matrix P on Lie algebra coordinates (Teng et al., 2022) `ev:asserted` p. 3 ^teng2022lie-014
- The authors state that P need not be designed for control; only its existence and positive definiteness must be verified (Teng et al., 2022) `ev:asserted` p. 3 ^teng2022lie-015
- Mimicking linear quadratic Lyapunov functions, the gradient of the error function is set linear in the Lie algebra error psi (Teng et al., 2022) `ev:asserted` p. 3 ^teng2022lie-016
- The proposed first-order feedback sets the twist to minus K times psi plus the adjoint-transformed desired twist (Teng et al., 2022) `ev:asserted` p. 3 ^teng2022lie-017
- Via the Lyapunov equation, any gain matrix K with only positive eigenvalues ensures a positive definite P exists for any positive definite Q (Teng et al., 2022) `ev:computed` p. 3 ^teng2022lie-018
- The derivation shows the candidate error function exists as a quadratic function of psi, equal to one half psi-transposed P psi (Teng et al., 2022) `ev:computed` p. 3 ^teng2022lie-019
- Using a Rayleigh quotient argument, the authors show the linear feedback exponentially stabilizes the equilibrium at psi equal to zero (Teng et al., 2022) `ev:computed` p. 3 ^teng2022lie-020
- Since the bounds hold for any psi, the authors conclude the equilibrium at the identity is also globally stable (Teng et al., 2022) `ev:computed` p. 4 ^teng2022lie-021
- Theorem 1 states that half the squared P-norm of the Lie algebra coordinate is a candidate Lyapunov function with gradient X phi-hat (Teng et al., 2022) `ev:computed` p. 4 ^teng2022lie-022
- Theorem 3 states the reconstruction system can be exponentially stabilized to the identity by linear feedback with a positive-eigenvalue gain matrix (Teng et al., 2022) `ev:computed` p. 4 ^teng2022lie-023
- Both the PD controller and the iLQR algorithm are implemented on SO(3), modeling rigid-body rotation with forced Euler-Poincaré equations (Teng et al., 2022) `ev:reported` p. 4 ^teng2022lie-024
- The proposed PD feedback term is minus Kp times the Lie algebra error psi minus Kd times the angular velocity error (Teng et al., 2022) `ev:reported` p. 4 ^teng2022lie-025
- The trajectory optimization adopts the iLQR framework, iterating an LQR backward pass with a forward rollout under the optimal policy (Teng et al., 2022) `ev:reported` p. 4 ^teng2022lie-026
- Instead of the Banach-space calculus used in reference 20, the authors use a Taylor series to linearize the perturbed dynamics (Teng et al., 2022) `ev:reported` p. 5 ^teng2022lie-027
- The linearized perturbed state in the Lie algebra evolves as minus the adjoint of the nominal twist on psi plus the twist difference (Teng et al., 2022) `ev:computed` p. 5 ^teng2022lie-028
- The cost matrices Q, V and S are set by the user and remain constant during all iterations (Teng et al., 2022) `ev:reported` p. 5 ^teng2022lie-029
- The perturbed system is discretized with a zero-order hold before solving a discrete LQR subproblem by dynamic programming (Teng et al., 2022) `ev:reported` p. 5 ^teng2022lie-030
- In their implementation the authors set the line search step length gamma to 1 for simplification (Teng et al., 2022) `ev:reported` p. 5 ^teng2022lie-031
- The PD comparison baseline from references 7 and 11 uses the trace error function, one half the trace of identity minus Psi (Teng et al., 2022) `ev:reported` p. 6 ^teng2022lie-032
- The PD simulation uses proportional gain Kp set to diag(1000, 1000, 1000) with derivative gain Kd set to diag(100, 100, 100) (Teng et al., 2022) `ev:reported` p. 6 ^teng2022lie-033
- The PD test sets an initial rotation error of 0.999π for tracking sinusoidal body-frame angular velocities with inertia diag(1, 3, 5) (Teng et al., 2022) `ev:reported` p. 6 ^teng2022lie-034
- With an initial error approaching π, the error still converges fast under the proposed controller in the time-varying tracking simulation (Teng et al., 2022) `ev:measured` p. 6 ^teng2022lie-035
- The response of the baseline PD controller is much slower at the initial pose when the initial error approaches π (Teng et al., 2022) `ev:measured` p. 6 ^teng2022lie-036
- Via Rodrigues' formula, the baseline proportional feedback equals the sine of the error norm divided by the norm times psi (Teng et al., 2022) `ev:computed` p. 6 ^teng2022lie-037
- This analysis suggests the baseline proportional feedback term approaches 0 when the error norm approaches π (Teng et al., 2022) `ev:computed` p. 6 ^teng2022lie-038
- The authors explain the vanishing baseline gradient near π by the trace error function being bounded with respect to psi (Teng et al., 2022) `ev:asserted` p. 6 ^teng2022lie-039
- The gradient of the proposed error function does not vanish near π, which the authors say enables faster convergence (Teng et al., 2022) `ev:asserted` p. 6 ^teng2022lie-040
- The authors do not give a rigorous exponential stability proof for the second-order system, saying it can follow reference 11 (Teng et al., 2022) `ev:asserted` p. 6 ^teng2022lie-041
- The iLQR is compared against the open-source discrete-time Lie group DDP algorithm of reference 21 as the baseline (Teng et al., 2022) `ev:reported` p. 6 ^teng2022lie-042
- The baseline DDP designs its cost function on the manifold, so its gradient and Hessian must be updated each iteration (Teng et al., 2022) `ev:asserted` p. 6 ^teng2022lie-043
- The proposed iLQR omits the second-order derivative of the discrete dynamics, so only linear convergence is possible for it (Teng et al., 2022) `ev:asserted` p. 6 ^teng2022lie-044
- DDP* is the baseline DDP algorithm with its cost function replaced by the proposed Lie algebra cost function (Teng et al., 2022) `ev:reported` p. 6 ^teng2022lie-045
- The iLQR task rotates a rigid body from the identity to a randomly generated goal pose 0.995π away from the identity (Teng et al., 2022) `ev:reported` p. 6 ^teng2022lie-046
- The trajectory optimization uses a final time of 3 sec, a time step of 0.01 sec, and inertia diag(5, 10, 15) (Teng et al., 2022) `ev:reported` p. 6 ^teng2022lie-047
- The trajectory optimization starts from an initial trajectory with all states at the origin and the input set to 0 (Teng et al., 2022) `ev:reported` p. 7 ^teng2022lie-048
- The cost design penalizes only the terminal state plus the inputs in the stage cost, with Q set to 0 (Teng et al., 2022) `ev:reported` p. 7 ^teng2022lie-049
- The iLQR and the improved DDP both use terminal weight V equal to 1000I with input weight S equal to 0.01I (Teng et al., 2022) `ev:reported` p. 7 ^teng2022lie-050
- The original DDP uses adaptive V and S weights with a goal weight Vg of 1000I on its trace-based configuration cost (Teng et al., 2022) `ev:reported` p. 7 ^teng2022lie-051
- Convergence is measured by the norm of the difference between the final input and the input at each iteration (Teng et al., 2022) `ev:reported` p. 7 ^teng2022lie-052
- The original DDP converges extremely slowly while far from the local optimum, especially during the first 30 iterations (Teng et al., 2022) `ev:measured` p. 7 ^teng2022lie-053
- The iLQR exhibits a linear convergence rate after a few iterations in the SO(3) trajectory optimization example (Teng et al., 2022) `ev:measured` p. 7 ^teng2022lie-054
- When equipped with the proposed cost function, DDP* converges in 7 iterations on the SO(3) trajectory optimization task (Teng et al., 2022) `ev:measured` p. 7 ^teng2022lie-055
- The authors note that the iLQR converges faster during the first 5 iterations of the SO(3) trajectory optimization (Teng et al., 2022) `ev:measured` p. 7 ^teng2022lie-056
- The authors suggest that combining iLQR and DDP* as in reference 21 could take fewer iterations to converge (Teng et al., 2022) `ev:asserted` p. 7 ^teng2022lie-057
- All three methods, iLQR, DDP and DDP*, converged to the same solution in the SO(3) trajectory optimization example (Teng et al., 2022) `ev:measured` p. 7 ^teng2022lie-058
- Prior work in reference 28 has shown that a continuous control law cannot globally stabilize SO(3) due to its topological properties (Teng et al., 2022) `ev:cited` p. 7 ^teng2022lie-059
- The logarithmic map can produce discontinuous values by clamping to the principal branch, so the PD controller can be discontinuous (Teng et al., 2022) `ev:asserted` p. 7 ^teng2022lie-060
- The authors state their PD controller can generate discontinuous control laws which ensure global convergence on the group (Teng et al., 2022) `ev:asserted` p. 7 ^teng2022lie-061
- One future direction named by the authors is combining the proposed framework with perception systems such as references 30 and 31 (Teng et al., 2022) `ev:asserted` p. 7 ^teng2022lie-062
- The authors conclude that the proposed cost function enables global exponential convergence in tracking control on Lie groups (Teng et al., 2022) `ev:asserted` p. 7 ^teng2022lie-063
- The authors conclude that the proposed Lie algebra cost function greatly accelerates trajectory optimization for systems on Lie groups (Teng et al., 2022) `ev:asserted` p. 7 ^teng2022lie-064

## 🎯 Contributions

## 📖 Glossary

- **Lie algebra** — Tangent space of a Lie group at the identity, a vector space.
- **Left-invariant metric** — Inner product on a Lie group unchanged by left translation of tangent vectors.
- **Configuration error** — Group element Psi relating nominal and actual configurations, identity when tracking is exact.
- **Trace error function** — Rotation error one half trace of identity minus Psi; bounded, gradient vanishes near π.
- **Logarithmic map** — Inverse of the exponential map, sending group elements to Lie algebra coordinates.
- **Adjoint map** — Linear action of a group element on its Lie algebra, used to change frames.
- **iLQR** — Iterative LQR: repeated local LQR backward pass and nonlinear forward rollout.
- **DDP** — Differential Dynamic Programming; like iLQR but includes second-order dynamics derivatives.
- **Euler-Poincaré equations** — Reduced equations of motion for rigid-body rotation expressed with body angular velocity.

## ❓ Open questions

- Does the rigorous exponential stability proof for the second-order PD system go through as the authors expect?
- How does the Lie algebra cost behave on non-compact groups such as SE(3), which the paper does not simulate?
- How sensitive is global convergence to the discontinuity introduced by clamping the logarithm to its principal branch, e.g. chattering near π?
- Would a hybrid iLQR then DDP* scheme actually converge in fewer iterations, as suggested?
- How does the approach compare over many random goal poses rather than a single randomly generated one?

## 📝 Notes on reading

Read the arXiv v1 preprint (2204.09177v1, 20 Apr 2022), which matches the identifier. Figures 2 to 4 (tracking responses, convergence curves, converged trajectories) could only be described from their captions; no numeric values were claimed from them. Fig. 3 caption says the original DDP converges extremely slowly in the first 30 iterations. Table III labels the third column Improved DDP, which corresponds to DDP* in the text. Definition 3 concludes global stability where global exponential stability seems intended. Proposition 2 writes the gradient of h with respect to h, apparently a typo for X. Definition 5 refers to the inner product as (4), which is the logarithm equation number. Equations were extracted with broken sub- and superscripts; claims paraphrase them in words. The PD simulation is only qualitatively reported (converges fast versus much slower), with no numeric convergence times.

## Suggested new concepts

- Lie algebra cost function — central design idea: quadratic cost in Lie algebra coordinates with gradient shaped by a left-invariant metric.
- Geometric PD control on SO(3) — recurring baseline family for attitude and UAV control with trace-based errors.
- Iterative LQR on Lie groups — trajectory optimization method that recurs across legged and aerial robotics work.
- Topological obstruction to global stabilization on SO(3) — explains why discontinuous control laws are needed for global convergence.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Costes en el álgebra con convergencia exponencial (C.2, F.4).
