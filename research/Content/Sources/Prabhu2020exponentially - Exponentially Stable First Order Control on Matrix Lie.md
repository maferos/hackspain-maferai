---
aliases: []
type: "source"
title: "Exponentially Stable First Order Control on Matrix Lie Groups"
citekey: "Prabhu2020exponentially"
doi: "10.48550/arXiv.2004.00239"
arxiv: "2004.00239"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2004.00239"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Valmik Prabhu", "Amay Saxena", "S. Shankar Sastry"]
sha256: ["9a28df3c2eaaf025feaf892f82b30267c02b15d6f24cf4671123d97c049169b1"]
pdf: "Content/Papers/Prabhu2020exponentially.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 53
---

📄 PDF: [[Prabhu2020exponentially.pdf]]

> [!abstract] One-sentence summary
> The paper proves that a first order controller built in exponential coordinates, a feedback term on the logarithm of the configuration error plus a feedforward reference velocity, gives global exponential trajectory tracking on SO(n), SE(n), SU(n) and GL(n, C), and shows it working in simulation and for Cartesian velocity control of a Sawyer arm.

## Abstract

We present a novel first order controller for systems evolving on matrix Lie groups, a major use case of which is Cartesian velocity control on robot manipulators. This controller achieves global exponential trajectory tracking on a number of commonly used Lie groups including the Special Orthogonal Group SO(n), the Special Euclidean Group SE(n), and the General Linear Group over complex numbers GL(n, C). Additionally, this controller achieves local exponential trajectory tracking on all matrix Lie groups. We demonstrate the effectiveness of this controller in simulation on a number of different Lie groups as well as on hardware with a 7-DOF Sawyer robot arm. (arXiv)

## 🧠 Key ideas (atomic)

- The paper presents a first order tracking controller for fully actuated systems whose state evolves on a matrix Lie group. (Prabhu et al., 2020) `ev:asserted` p. 1 ^prabhu2020exponentially-001
- A major use case of the controller is Cartesian velocity control of the end effector on robot manipulators. (Prabhu et al., 2020) `ev:asserted` p. 1 ^prabhu2020exponentially-002
- Most Cartesian controllers use local parameterizations of end effector rotation, such as Euler angles, which exhibit singularities like gimbal lock. (Prabhu et al., 2020) `ev:asserted` p. 1 ^prabhu2020exponentially-003
- The authors state that, to their knowledge, no one had yet proven a globally stable Cartesian velocity controller. (Prabhu et al., 2020) `ev:asserted` p. 1 ^prabhu2020exponentially-004
- Whitney did initial work on first order Cartesian control using a pseudoinverse-Jacobian based controller with local coordinates. (Prabhu et al., 2020) `ev:cited` p. 1 ^prabhu2020exponentially-005
- Khatib developed a second order Cartesian controller by defining Cartesian analogs of the inertia, Coriolis and gravity terms of computed torque control. (Prabhu et al., 2020) `ev:cited` p. 1 ^prabhu2020exponentially-006
- Lynch and Park's Modern Robotics presents a Cartesian control law very similar to this one, but without a proof. (Prabhu et al., 2020) `ev:cited` p. 1 ^prabhu2020exponentially-007
- Lewis and Bullo defined controllers for fully actuated systems on Riemannian manifolds with almost-global asymptotic tracking and local exponential convergence. (Prabhu et al., 2020) `ev:cited` p. 1 ^prabhu2020exponentially-008
- In SO(3) the measure zero set excluded from almost-global stability is the set of all rotations of exactly 180◦. (Prabhu et al., 2020) `ev:asserted` p. 2 ^prabhu2020exponentially-009
- Lee extended the work of Lewis and Bullo with a hierarchical UAV controller giving almost-global asymptotic tracking of position and yaw. (Prabhu et al., 2020) `ev:cited` p. 2 ^prabhu2020exponentially-010
- The authors consider it likely that their results could be useful in state estimation for SLAM and quantum computing error correction. (Prabhu et al., 2020) `ev:asserted` p. 2 ^prabhu2020exponentially-011
- Common groups including SO(n), SE(n), SU(n) and GL(n, C) possess globally surjective exponential maps, whereas GL(n, R) does not. (Prabhu et al., 2020) `ev:asserted` p. 3 ^prabhu2020exponentially-012
- Near the identity the exponential map is always locally surjective, at least in the region where the exponent norm is below ln 2. (Prabhu et al., 2020) `ev:asserted` p. 3 ^prabhu2020exponentially-013
- The logarithm on SE(3) can be made globally well defined by restricting its output to elements with ||ω|| ≤ π. (Prabhu et al., 2020) `ev:asserted` p. 4 ^prabhu2020exponentially-014
- The SE(3) logarithm is discontinuous exactly at rigid transforms whose rotational component is a rotation of π radians. (Prabhu et al., 2020) `ev:asserted` p. 4 ^prabhu2020exponentially-015
- The system is modelled as left-invariant, so the control input is the body velocity of the system state. (Prabhu et al., 2020) `ev:reported` p. 4 ^prabhu2020exponentially-016
- Right-invariant systems, where the control input is the spatial velocity, admit equivalent results that this paper does not derive. (Prabhu et al., 2020) `ev:asserted` p. 4 ^prabhu2020exponentially-017
- The authors assume the reference trajectory on the Lie group is differentiable with a piece-wise continuous derivative. (Prabhu et al., 2020) `ev:reported` p. 4 ^prabhu2020exponentially-018
- The state error is defined as the logarithm of the configuration error, the inverse system pose multiplied by the desired pose. (Prabhu et al., 2020) `ev:reported` p. 4 ^prabhu2020exponentially-019
- If the state error dynamics equal minus k times the state error, the error converges exponentially to zero with rate k. (Prabhu et al., 2020) `ev:computed` p. 4 ^prabhu2020exponentially-020
- Lemma 1 proves local exponential tracking in part of the region where the spectral radius of gTD minus identity is below 1. (Prabhu et al., 2020) `ev:computed` p. 5 ^prabhu2020exponentially-021
- The local proof assumes the configuration error commutes with its derivative, an assumption the closed loop is then shown to satisfy. (Prabhu et al., 2020) `ev:computed` p. 5 ^prabhu2020exponentially-022
- The authors identify the reliance on a local power-series representation of the matrix logarithm as the primary flaw of Lemma 1. (Prabhu et al., 2020) `ev:asserted` p. 5 ^prabhu2020exponentially-023
- To avoid needing an analytic logarithm, the authors derive the time derivative of log(g) using the [[Baker-Campbell-Hausdorff formula]]. (Prabhu et al., 2020) `ev:computed` p. 5 ^prabhu2020exponentially-024
- Lemma 3 represents the time derivative of the state error as a formal series of commutators of the state error and spatial velocity. (Prabhu et al., 2020) `ev:computed` p. 5 ^prabhu2020exponentially-025
- For SO(n), SE(n), GL(n, C) and SU(n), Theorem 1 yields global exponential stability of the tracking controller. (Prabhu et al., 2020) `ev:computed` p. 5 ^prabhu2020exponentially-026
- Under the control law the spatial velocity of the configuration error commutes with the state error, so all commutator terms vanish. (Prabhu et al., 2020) `ev:computed` p. 6 ^prabhu2020exponentially-027
- The control input is the sum of a feedback term on the state error and a feedforward reference body velocity term. (Prabhu et al., 2020) `ev:asserted` p. 6 ^prabhu2020exponentially-028
- The feedforward term rewrites the body velocity of the reference trajectory in the system tool frame through a similarity transform. (Prabhu et al., 2020) `ev:asserted` p. 6 ^prabhu2020exponentially-029
- The feedback term is the velocity that, executed for 1 second, brings the instantaneous tool frame to the desired frame. (Prabhu et al., 2020) `ev:asserted` p. 6 ^prabhu2020exponentially-030
- Theorem 2 extends exponential tracking to a discrete-time control law for a positive gain with k∆t < 2 and small enough time step. (Prabhu et al., 2020) `ev:computed` p. 6 ^prabhu2020exponentially-031
- The discrete-time proof neglects all terms of second or higher order in the time step when expanding products of exponentials. (Prabhu et al., 2020) `ev:computed` p. 7 ^prabhu2020exponentially-032
- In discrete time the state error is multiplied by (1 −k∆t) each step, vanishing exponentially when |1 −k∆t| < 1. (Prabhu et al., 2020) `ev:computed` p. 7 ^prabhu2020exponentially-033
- The SE(3) simulation tracked a helical trajectory with constant body velocity [0.5, 0.5, 0.3, 0.5, 0.3, 0.7]T using control gain k = 1. (Prabhu et al., 2020) `ev:reported` p. 7 ^prabhu2020exponentially-034
- In the simulations the actual trajectory started at an arbitrary configuration whose initial error had spectral radius greater than 1. (Prabhu et al., 2020) `ev:reported` p. 7 ^prabhu2020exponentially-035
- In the SE(3) simulation the system exponentially converges to the desired helical trajectory from its offset starting configuration. (Prabhu et al., 2020) `ev:measured` p. 7 ^prabhu2020exponentially-036
- In the SU(4) simulation the desired trajectory was randomly determined with constant body velocity, starting at the origin. (Prabhu et al., 2020) `ev:reported` p. 7 ^prabhu2020exponentially-037
- With control gain k = 1 the SU(4) system exponentially converges to its randomly determined desired trajectory in simulation. (Prabhu et al., 2020) `ev:measured` p. 7 ^prabhu2020exponentially-038
- The GL0(4, R) simulation used a desired trajectory built by randomly selecting a body velocity for each time step. (Prabhu et al., 2020) `ev:reported` p. 7 ^prabhu2020exponentially-039
- In GL0(4, R), the general linear group subset with positive determinant, the simulated system exponentially converges to the desired trajectory. (Prabhu et al., 2020) `ev:measured` p. 7 ^prabhu2020exponentially-040
- The simulations report both the Frobenius norm of gTD minus identity and the Frobenius norm of log(gTD) as tracking error. (Prabhu et al., 2020) `ev:reported` p. 6 ^prabhu2020exponentially-041
- On a 7-DOF Sawyer arm the controller is implemented on SE(3) to perform Cartesian velocity control of the end-effector. (Prabhu et al., 2020) `ev:reported` p. 7 ^prabhu2020exponentially-042
- On the Sawyer the body velocity command is converted to a spatial velocity, then mapped to joint velocities through the Jacobian pseudoinverse. (Prabhu et al., 2020) `ev:reported` p. 7 ^prabhu2020exponentially-043
- Forward kinematics and the Jacobian were computed from Sawyer's pre-calibrated URDF with the OROCOS Kinematics and Dynamics Library. (Prabhu et al., 2020) `ev:reported` p. 7 ^prabhu2020exponentially-044
- The hardware test tracked a helical trajectory with a fixed random desired orientation, starting the arm away in position and orientation. (Prabhu et al., 2020) `ev:reported` p. 7 ^prabhu2020exponentially-045
- With gain k = 1 the Sawyer end-effector quickly converges to the desired trajectory, then tracks it with negligible steady-state error. (Prabhu et al., 2020) `ev:measured` p. 7 ^prabhu2020exponentially-046
- The Frobenius-norm error metric of gTD minus identity shows the Sawyer configuration error converging exponentially to zero. (Prabhu et al., 2020) `ev:measured` p. 7 ^prabhu2020exponentially-047
- The authors find the controller easy to implement on the Sawyer hardware, requiring minimal tuning for effective trajectory tracking. (Prabhu et al., 2020) `ev:asserted` p. 7 ^prabhu2020exponentially-048
- Developing the control law in exponential coordinates lets the authors sidestep the task of finding easily-differentiable Lyapunov functions. (Prabhu et al., 2020) `ev:asserted` p. 8 ^prabhu2020exponentially-049
- The control law was intuitive enough that the authors had their undergraduate robotics course implement it as a homework assignment. (Prabhu et al., 2020) `ev:reported` p. 8 ^prabhu2020exponentially-050
- The authors suggest the [[Baker-Campbell-Hausdorff formula|modified BCH formula]] of Lemma 3 may yield bounds when the control input does not commute with the error. (Prabhu et al., 2020) `ev:asserted` p. 8 ^prabhu2020exponentially-051
- The authors feel this approach could be a way to tackle robustness or underactuated control in further research. (Prabhu et al., 2020) `ev:asserted` p. 8 ^prabhu2020exponentially-052
- Further work could represent a second order controller in exponential coordinates to compare with the Lagrangian approach of Maithripala. (Prabhu et al., 2020) `ev:asserted` p. 8 ^prabhu2020exponentially-053

## 🎯 Contributions

## 📖 Glossary

- **Matrix Lie group** — A continuous group of invertible square matrices forming a smooth manifold.
- **Lie algebra** — The tangent space of a Lie group at the identity element.
- **Body velocity** — Group velocity left-rotated into the body frame, g⁻¹ġ.
- **Spatial velocity** — Group velocity right-rotated into the spatial frame, ġg⁻¹.
- **Exponential coordinates** — Lie algebra element whose matrix exponential equals a given group element.
- **Configuration error** — Inverse system pose times desired pose; identity when tracking perfectly.
- **State error** — Logarithm of the configuration error, an element of the Lie algebra.
- **Baker-Campbell-Hausdorff formula** — Series of commutators giving log of a product of two exponentials.
- **Left-invariant system** — System whose control input is the body velocity of its state.
- **Almost-global stability** — Convergence from all initial states except a nowhere dense measure zero set.

## ❓ Open questions

- Can bounds or convergence guarantees be obtained from the Lemma 3 series when the control input does not commute with the error?
- How robust is the controller to disturbances, model error or actuator limits?
- Can the approach be extended to underactuated systems on Lie groups?
- What is the region of convergence on groups whose exponential map is not surjective, such as GL(n, R)?
- How does a second order controller in exponential coordinates compare with Lagrangian geometric controllers?
- How large can the discrete time step be before the neglected higher-order terms break convergence?
- How does tracking behave near the SE(3) logarithm discontinuity at rotations of π radians?

## 📝 Notes on reading

Read the arXiv v1 preprint (2004.00239v1, 1 Apr 2020), matching the packet identifier.

The hardware and simulation results are shown only as plots (Fig. 2a-c, Fig. 3, Fig. 4a-b); no convergence rates, errors or timings are tabulated, so the results are qualitative ("exponentially converges", "negligible error in steady state").

Inconsistencies inside the paper: Section III-B says su(n) is the set of skew-Hermitian matrices in Cn×n, while Section V-B says su(4) is skew-hermitian matrices in R4×4. The abstract and Section IV claim global exponential tracking, but Theorem 1's statement first says "local exponential trajectory tracking within the region in which the exponential map is surjective". The hardware section says it uses the controller defined in Theorem 2 (discrete time). The introduction states the local proof has a small radius of convergence. Theorem 2 requires k∆t < 2 but the proof only argues |1 − k∆t| < 1 after a first-order approximation, so the discrete result is approximate in ∆t. Many equations (BCH series, matrix expansions) are garbled in the extraction and were not claimed beyond their stated conclusions.

## Suggested new concepts

- Cartesian velocity control — central robot-manipulator use case for Lie group controllers and pseudoinverse-Jacobian mapping.
- Exponential coordinates on Lie groups — the parameterization the controller and its proofs are built on.
- Baker-Campbell-Hausdorff formula — key tool for differentiating the Lie group logarithm, reusable across geometric control.
- Geometric control on Lie groups — broader field (Brockett, Bullo, Lewis, Lee) this paper extends.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H5.** Controlador de velocidad cartesiana en grupos de Lie matriciales con convergencia exponencial global en SE(n), base teórica de la ley PBVS con Log.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
