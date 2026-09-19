---
aliases: []
type: "source"
title: "Invariant Stochastic Filtering on SE(3) for Inertial-Encoder State Estimation of Serial Rigid Manipulators"
citekey: "Yaqubi2026invariant"
doi: "10.48550/arXiv.2607.00026"
arxiv: "2607.00026"
year: 2026
publication_type: "preprint"
url: "https://arxiv.org/abs/2607.00026"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["S. Yaqubi", "J. Mattila"]
sha256: ["3811a86948779e2940f26dc833ac8c91f3670e33366ce757e1d7f4dd8c28fd00"]
pdf: "Content/Papers/Yaqubi2026invariant.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Yaqubi2026invariant.pdf]]

> [!abstract] One-sentence summary
> The paper derives a modular chain of per-link invariant extended Kalman filters on SE(3) that fuses IMU and joint encoder data with a physically separated noise model, proves chained exponential ultimate boundedness, and shows lower joint-angle RMSE than a coordinate EKF in a two-link simulation.

## Abstract

An invariant extended Kalman filter (IEKF) is developed for state estimation of serial rigid manipulators with an arbitrary number of links, formulated entirely within the Lie group SE(3). The group-affine property of the kinematic equations makes the linearised error dynamics autonomous, so the Riccati equation governs the true error covariance rather than a local approximation. A physically separated noise model treats gyroscope and accelerometer channels independently: the accelerometer provides translational twist via gravity-compensated integration, yielding a measurement covariance that scales with the sample interval in exact analogy with process noise discretisation; a state-dependent Coriolis noise term captures gyroscope noise propagating through the nonlinear dynamics, vanishing at rest and growing with twist magnitude. The filter is structured as a modular chain of per-link IEKFs in which the predicted covariance of each link depends on its predecessor only through the Adjoint-transformed posterior, giving linear computational cost in link count. Exponential ultimate boundedness in mean square is established via a Lie algebra Lyapunov function, with per-link bounds chained through the Adjoint operator norm to yield a stability certificate that is modular and scalable to arbitrary chain length. Numerical results validate the design. (arXiv)

## 🧠 Key ideas (atomic)

- An [[Invariant extended Kalman filter|invariant extended Kalman filter]] is presented for state estimation of serial rigid manipulators with an arbitrary number of links, grounded on SE(3). (Yaqubi & Mattila, 2026) `ev:asserted` p. 16 ^yaqubi2026invariant-001
- Euler-angle and quaternion EKFs introduce gimbal lock, normalisation constraints, and a linearisation consistency error that does not vanish at convergence. (Yaqubi & Mattila, 2026) `ev:cited` p. 2 ^yaqubi2026invariant-002
- The authors state that existing geometric filters address single bodies and do not propagate uncertainty modularly across kinematic chains. (Yaqubi & Mattila, 2026) `ev:asserted` p. 2 ^yaqubi2026invariant-003
- The [[Invariant extended Kalman filter|invariant EKF]] exploits a [[Group-affine dynamics|group-affine condition]] under which linearised error dynamics are autonomous, so the Riccati equation governs the true covariance. (Yaqubi & Mattila, 2026) `ev:cited` p. 2 ^yaqubi2026invariant-004
- According to the authors, existing work treating the full chain as a monolithic state incurs cubic update cost in link count. (Yaqubi & Mattila, 2026) `ev:asserted` p. 2 ^yaqubi2026invariant-005
- Recovering translational velocity by integrating accelerometer data introduces a sample-interval scaling on the effective noise covariance that is absent for the gyroscope. (Yaqubi & Mattila, 2026) `ev:asserted` p. 2 ^yaqubi2026invariant-006
- The authors claim that existing geometric filters do not address the state-dependent process noise created by gyroscope noise passing through the Coriolis term. (Yaqubi & Mattila, 2026) `ev:asserted` p. 2 ^yaqubi2026invariant-007
- The model considers a serial manipulator with n revolute-jointed rigid links, each with a body-fixed frame, an SE(3) configuration and a body twist. (Yaqubi & Mattila, 2026) `ev:reported` p. 3 ^yaqubi2026invariant-008
- Unmodeled dynamics, friction, and payload uncertainty are represented as a disturbance wrench acting additively on each link's Newton–Euler equation. (Yaqubi & Mattila, 2026) `ev:reported` p. 3 ^yaqubi2026invariant-009
- The disturbance wrench is modelled as zero-mean continuous-time white noise with a positive definite spectral density per link. (Yaqubi & Mattila, 2026) `ev:reported` p. 4 ^yaqubi2026invariant-010
- The gyroscope measurement is modelled as body-fixed angular velocity plus zero-mean Gaussian noise whose covariance comes from the IMU datasheet. (Yaqubi & Mattila, 2026) `ev:reported` p. 4 ^yaqubi2026invariant-011
- Integrating gravity-compensated accelerometer data over one sample interval and stacking it with the gyroscope yields a full body-twist measurement. (Yaqubi & Mattila, 2026) `ev:reported` p. 4 ^yaqubi2026invariant-012
- The stacked IMU covariance multiplies the accelerometer block by the sample interval, an asymmetry the authors call a defining feature of the noise model. (Yaqubi & Mattila, 2026) `ev:asserted` p. 4 ^yaqubi2026invariant-013
- Each revolute encoder is modelled as the joint angle plus Gaussian noise whose variance equals the encoder quantization variance. (Yaqubi & Mattila, 2026) `ev:reported` p. 4 ^yaqubi2026invariant-014
- The per-link filter state is pose and twist, with all Kalman algebra performed on a 12-dimensional Lie algebra error vector. (Yaqubi & Mattila, 2026) `ev:reported` p. 5 ^yaqubi2026invariant-015
- The stacked per-link measurement combines the IMU twist and the encoder angle into a seven-dimensional observation with diagonal noise covariance. (Yaqubi & Mattila, 2026) `ev:reported` p. 5 ^yaqubi2026invariant-016
- Table 1 lists the wrench disturbance covariance as identified from innovation consistency rather than from a sensor datasheet. (Yaqubi & Mattila, 2026) `ev:reported` p. 5 ^yaqubi2026invariant-017
- Corrections are applied by geometric retraction through the exponential map, which keeps the pose estimate on SE(3) without normalisation. (Yaqubi & Mattila, 2026) `ev:reported` p. 6 ^yaqubi2026invariant-018
- The error model gathers four independent noise sources: wrench disturbance, IMU noise, upstream velocity error, and encoder noise with upstream pose error. (Yaqubi & Mattila, 2026) `ev:asserted` p. 6 ^yaqubi2026invariant-019
- The left-invariant pose error is shown to evolve autonomously, independently of the pose estimate, establishing the [[Group-affine dynamics|group-affine property]] of the pose kinematics. (Yaqubi & Mattila, 2026) `ev:computed` p. 6 ^yaqubi2026invariant-020
- The authors conclude that the [[Invariant extended Kalman filter|IEKF]] linearisation is exact for the pose kinematics, so the Riccati equation governs the true error covariance. (Yaqubi & Mattila, 2026) `ev:asserted` p. 6 ^yaqubi2026invariant-021
- A twist-error driving term couples pose error to twist error, which the authors say is absent in single-body IEKF formulations. (Yaqubi & Mattila, 2026) `ev:asserted` p. 7 ^yaqubi2026invariant-022
- The velocity error dynamics are linearised through a Coriolis matrix built from the estimated twist and the link's spatial inertia. (Yaqubi & Mattila, 2026) `ev:computed` p. 7 ^yaqubi2026invariant-023
- The linearised error Jacobian depends on the estimated twist but not on the error, confirming the autonomous error dynamics property. (Yaqubi & Mattila, 2026) `ev:computed` p. 7 ^yaqubi2026invariant-024
- Upstream velocity error and IMU noise enter the same Coriolis path independently, so their covariances add into a total effective twist uncertainty. (Yaqubi & Mattila, 2026) `ev:computed` p. 8 ^yaqubi2026invariant-025
- The noise input matrices have zero pose blocks, so noise drives the pose error only through the identity coupling in the Jacobian. (Yaqubi & Mattila, 2026) `ev:computed` p. 8 ^yaqubi2026invariant-026
- The effective discrete noise covariance is computed exactly with the Van Loan method over each sample interval. (Yaqubi & Mattila, 2026) `ev:reported` p. 9 ^yaqubi2026invariant-027
- The Coriolis noise term vanishes as the estimated twist approaches zero, recovering the wrench-only noise model when the link is at rest. (Yaqubi & Mattila, 2026) `ev:computed` p. 9 ^yaqubi2026invariant-028
- Encoder noise and upstream pose error enter the predicted pose error through the Adjoint of the relative transform plus the unit joint screw. (Yaqubi & Mattila, 2026) `ev:computed` p. 9 ^yaqubi2026invariant-029
- The predicted covariance of each link requires from its predecessor only the posterior pose, the posterior twist, and the posterior covariance. (Yaqubi & Mattila, 2026) `ev:computed` p. 9 ^yaqubi2026invariant-030
- The Kalman update computes the per-link posterior covariance using the Joseph form, which the authors choose for numerical stability. (Yaqubi & Mattila, 2026) `ev:reported` p. 10 ^yaqubi2026invariant-031
- Proposition 1 states that the per-link filter cost per step is O(1) in n, giving a total chain cost of O(n). (Yaqubi & Mattila, 2026) `ev:computed` p. 10 ^yaqubi2026invariant-032
- All per-link filter operations involve fixed-size 12 × 12 matrices that are independent of the number of links in the chain. (Yaqubi & Mattila, 2026) `ev:asserted` p. 10 ^yaqubi2026invariant-033
- The authors note that the Adjoint map is not an isometry under the Euclidean inner product, as SE(3) admits no bi-invariant metric. (Yaqubi & Mattila, 2026) `ev:asserted` p. 11 ^yaqubi2026invariant-034
- Geometric retraction leaves a second-order remainder, which the authors present as its key advantage over first-order linearisation error in coordinate EKFs. (Yaqubi & Mattila, 2026) `ev:asserted` p. 11 ^yaqubi2026invariant-035
- The stability analysis assumes bounded noise covariances and Jacobians, plus uniform complete observability through an observability Gramian bounded below. (Yaqubi & Mattila, 2026) `ev:reported` p. 12 ^yaqubi2026invariant-036
- Theorem 1 establishes per-link exponential ultimate boundedness in mean square, using a Lyapunov function built from the inverse predicted covariance. (Yaqubi & Mattila, 2026) `ev:computed` p. 12 ^yaqubi2026invariant-037
- The per-link bound requires the initial error to be small enough that the second-order remainder of the error recursion is dominated. (Yaqubi & Mattila, 2026) `ev:computed` p. 12 ^yaqubi2026invariant-038
- A small observability constant shrinks the decay rate and enlarges the residual ball, weakening the bound quantitatively without invalidating it. (Yaqubi & Mattila, 2026) `ev:asserted` p. 12 ^yaqubi2026invariant-039
- At zero twist the error Jacobian reduces to a nilpotent double-integrator structure that the authors describe as trivially observable. (Yaqubi & Mattila, 2026) `ev:asserted` p. 12 ^yaqubi2026invariant-040
- Lemma 1 bounds the Adjoint operator norm by the square root of one plus twice the squared distance between frames. (Yaqubi & Mattila, 2026) `ev:computed` p. 13 ^yaqubi2026invariant-041
- The Adjoint amplification factor equals one only for co-located frames and grows with link length, unlike SO(3) where the Adjoint is orthogonal. (Yaqubi & Mattila, 2026) `ev:asserted` p. 13 ^yaqubi2026invariant-042
- Theorem 2 chains the per-link bounds, multiplying each upstream residual by the product of downstream squared Adjoint norm bounds. (Yaqubi & Mattila, 2026) `ev:computed` p. 13 ^yaqubi2026invariant-043
- Since all Adjoint norm bounds are finite geometric constants, the authors conclude that exponential ultimate boundedness holds for any fixed chain length. (Yaqubi & Mattila, 2026) `ev:asserted` p. 13 ^yaqubi2026invariant-044
- Validation uses a numerical simulation of a 3-DOF two-link rigid serial manipulator executing large-amplitude three-dimensional motion. (Yaqubi & Mattila, 2026) `ev:reported` p. 13 ^yaqubi2026invariant-045
- The proposed IEKF is compared against a coordinate EKF and a raw measurement baseline under exact ground truth in simulation. (Yaqubi & Mattila, 2026) `ev:reported` p. 13 ^yaqubi2026invariant-046
- The simulated links have masses of 2.0 and 1.5 kg, with lengths of 0.50 and 0.40 m respectively. (Yaqubi & Mattila, 2026) `ev:reported` p. 14 ^yaqubi2026invariant-047
- Simulated noise uses standard deviations of 0.05 rad/s for the gyroscope, 0.20 m/s2 for the accelerometer, and 0.5 degrees for the encoder. (Yaqubi & Mattila, 2026) `ev:reported` p. 14 ^yaqubi2026invariant-048
- The plant is integrated by fourth-order Runge–Kutta for 15 s with a time step of 5 × 10−3 s. (Yaqubi & Mattila, 2026) `ev:reported` p. 14 ^yaqubi2026invariant-049
- The coordinate EKF baseline uses a flat joint-space state with double-integrator dynamics and encoder-only measurements, making it weaker by design. (Yaqubi & Mattila, 2026) `ev:reported` p. 14 ^yaqubi2026invariant-050
- In the simulation, the IEKF 2σ covariance band consistently envelops the true body-frame twist on the plotted channels. (Yaqubi & Mattila, 2026) `ev:measured` p. 14 ^yaqubi2026invariant-051
- The covariance band is wider for Link 2, whose covariance incorporates upstream estimation uncertainty through the total twist uncertainty term. (Yaqubi & Mattila, 2026) `ev:measured` p. 14 ^yaqubi2026invariant-052
- The IEKF achieves the smallest absolute joint-angle estimation error on all joints, with the advantage most pronounced on the second joint. (Yaqubi & Mattila, 2026) `ev:measured` p. 15 ^yaqubi2026invariant-053
- The text reports that the IEKF achieves a 33% RMSE reduction relative to the raw encoder baseline. (Yaqubi & Mattila, 2026) `ev:measured` p. 15 ^yaqubi2026invariant-054
- The text reports a 24% RMSE reduction of the [[Invariant extended Kalman filter|IEKF]] relative to the coordinate EKF on all joints. (Yaqubi & Mattila, 2026) `ev:measured` p. 15 ^yaqubi2026invariant-055
- In scenario S1 the IEKF joint RMSE is 0.335, 0.334 and 0.525 degrees across the three joint angles. (Yaqubi & Mattila, 2026) `ev:measured` p. 17 ^yaqubi2026invariant-056
- In scenario S1 the coordinate EKF joint RMSE is 0.442, 0.441 and 0.625 degrees across the three joint angles. (Yaqubi & Mattila, 2026) `ev:measured` p. 17 ^yaqubi2026invariant-057
- In scenario S1 the raw encoder baseline gives joint RMSE of 0.503, 0.503 and 0.713 degrees across the three joints. (Yaqubi & Mattila, 2026) `ev:measured` p. 17 ^yaqubi2026invariant-058
- In scenario S2 the IEKF RMSE on the second joint is 0.621 degrees, against 0.625 for the coordinate EKF. (Yaqubi & Mattila, 2026) `ev:measured` p. 17 ^yaqubi2026invariant-059
- The authors attribute IEKF RMSE stability across the two scenarios to amplitude-invariance of the SE(3) geometric error model. (Yaqubi & Mattila, 2026) `ev:asserted` p. 15 ^yaqubi2026invariant-060
- The mean NEES of the IEKF for Link 2 is 3.5, lying within the 95% chi-squared acceptance band [1.7, 16.0]. (Yaqubi & Mattila, 2026) `ev:measured` p. 16 ^yaqubi2026invariant-061
- The authors interpret a mean NEES below the ideal of 7 as a conservative filter resulting from deliberately inflated wrench noise. (Yaqubi & Mattila, 2026) `ev:asserted` p. 16 ^yaqubi2026invariant-062
- In steady state the IEKF end-effector orbit overlaps the true Lissajous orbit, which the authors read as absence of integration drift. (Yaqubi & Mattila, 2026) `ev:measured` p. 16 ^yaqubi2026invariant-063
- The authors propose characterising the observability Gramian in terms of manipulator geometry and trajectory as a natural theoretical continuation. (Yaqubi & Mattila, 2026) `ev:asserted` p. 17 ^yaqubi2026invariant-064
- Augmenting the per-link state with IMU bias vectors is proposed as an extension within the same stochastic framework. (Yaqubi & Mattila, 2026) `ev:asserted` p. 17 ^yaqubi2026invariant-065
- Deployment on a physical platform requires empirical validation of the NEES bounds against experimental ground truth, according to the authors. (Yaqubi & Mattila, 2026) `ev:asserted` p. 17 ^yaqubi2026invariant-066
- The authors suggest the SE(3) error coordinates are well suited to serve as a physical prior for learning-based state estimators. (Yaqubi & Mattila, 2026) `ev:asserted` p. 18 ^yaqubi2026invariant-067

## 🎯 Contributions


## 📖 Glossary

- **Invariant extended Kalman filter (IEKF)** — EKF on a Lie group using an invariant error, giving state-independent error dynamics.
- **Group-affine property** — Condition under which the invariant error evolves autonomously, independently of the state estimate.
- **Twist** — Six-vector of angular and translational velocity of a rigid body, an element of se(3).
- **Adjoint map** — Linear map transforming twists between frames of a rigid-body transformation.
- **Geometric retraction** — Applying a Lie algebra correction through the exponential map so the estimate stays on the group.
- **Exponential ultimate boundedness (EUB)** — Mean-square error decays exponentially into a bounded residual ball.
- **NEES** — Normalised estimation error squared; a chi-squared consistency test for a filter's covariance.
- **Joseph form** — Covariance update form that preserves symmetry and positive definiteness numerically.
- **Uniform complete observability** — Observability Gramian over a window is bounded below uniformly in time.

## ❓ Open questions

- Under which manipulator geometries and trajectories is the uniform complete observability assumption guaranteed?
- Does the filter keep its RMSE and NEES behaviour on a physical manipulator with real IMU biases and non-Gaussian noise?
- How does the chained residual ball, growing with the product of link lengths, behave for long chains (six or seven links) in practice?
- How does the per-link IEKF compare with a monolithic full-chain IEKF or with baselines that also use IMU data, rather than an encoder-only coordinate EKF?
- How can Lie group consistency be preserved when learned corrections are added to the estimator?

## 📝 Notes on reading

Version read: arXiv preprint v1 (2607.00026v1, 21 Jun 2026), stated to be under review.

Inconsistencies between text and Table 2 (p. 17): the text (p. 15) says the CEKF RMSE grows from S1 to S2 while the IEKF RMSE remains stable, but in Table 2 the No-filter and CEKF rows are identical across S1 and S2, and the IEKF θ2 RMSE rises from 0.525 (S1) to 0.621 (S2), nearly equal to the CEKF's 0.625. The claimed 33% and 24% reductions on all joints match only θ1y and θ1z; for θ2 in S1 the table implies roughly 26% versus no filter and 16% versus CEKF. The scenarios are labelled by amplitude Ay = 0.25 m (S1) and 0.40 m (S2), while the setup on p. 14 gives a 0.25 Lissajous amplitude and Ay,2 = 0.10 m; how S2 was generated is not described.

The NEES is said to be computed on the nf = 7 dimensions of the measurement vector rather than on the 12-dimensional error state, so it is closer to an innovation consistency test; the acceptance band [1.7, 16.0] is given without the number of runs or window used.

The section roadmap (p. 2-3) skips Section 4 and assigns Jacobian derivation to Section 5; the observation Jacobian is said to be derived in Section 7.1. Only one simulated two-link (3-DOF) chain is used; there is no hardware experiment. Figures 1-4 are plots only (twists with 2σ bands, joint-angle errors, RMSE bars, NEES trace); values were taken from the text and Table 2. Equations in the cached text are partly garbled by extraction but the surrounding prose is readable.

## Suggested new concepts

- Invariant extended Kalman filter — core estimator family on Lie groups; recurs across legged, inertial and manipulator state estimation.
- Group-affine systems — the structural condition that makes IEKF error dynamics autonomous; useful to link related filters.
- IMU-encoder fusion for manipulator state estimation — practical sensing setup relevant to robot arm proprioception.
- Modular per-link estimation on kinematic chains — linear-cost alternative to monolithic full-chain filters.
- NEES consistency testing — standard check of filter covariance calibration used across estimation papers.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H2.** Aplica el IEKF en SE(3) eslabón a eslabón a brazos seriales con garantías de estabilidad, el caso exacto de un manipulador de laboratorio.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
