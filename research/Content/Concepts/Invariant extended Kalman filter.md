---
aliases: ["IEKF", "InEKF"]
type: concept
element_type: method
topic: "[[Probability, filtering and generative models on Lie groups]]"
topics: ["[[Probability, filtering and generative models on Lie groups]]"]
created: 2026-09-19
---

## Working definition

An extended Kalman filter for states on a matrix Lie group that linearizes an invariant (left or right group) error instead of a vector difference, so that for group-affine systems the error dynamics are exactly log-linear and independent of the estimate.

## Evidence

- [[Barrau2017invariant - The invariant extended Kalman filter as a stable observer#^barrau2017invariant-001]] — The paper analyzes the invariant extended Kalman filter as a deterministic non-linear observer on Lie groups for continuous-time systems with discrete observations.
- [[Barrau2017invariant - The invariant extended Kalman filter as a stable observer#^barrau2017invariant-026]] — Theorem 4 states the IEKF is an asymptotically stable observer when the linear Kalman stability conditions hold about the true system trajectory.
- [[Barrau2017invariant - The invariant extended Kalman filter as a stable observer#^barrau2017invariant-028]] — During IEKF propagation, the logarithmic error evolution is exact with no higher-order terms, which removes a main difficulty of EKF analysis.
- [[Barrau2017invariant - The invariant extended Kalman filter as a stable observer#^barrau2017invariant-042]] — For the larger initial heading error in the car simulation, the IEKF, adapted to the system structure, completely outperforms the EKF.
- [[Hartley2019contact - Contact-Aided Invariant Extended Kalman Filtering for Robot#^hartley2019contact-001]] — The authors derive an invariant extended Kalman filter for a system of IMU and contact sensor dynamics with forward kinematic correction measurements.
- [[Hartley2019contact - Contact-Aided Invariant Extended Kalman Filtering for Robot#^hartley2019contact-025]] — The linearized observation matrix of the proposed InEKF is independent of the state estimate, unlike the QEKF observation matrix.
- [[Hartley2019contact - Contact-Aided Invariant Extended Kalman Filtering for Robot#^hartley2019contact-034]] — With deterministic dynamics, the difference between true and propagated InEKF error states was always exactly zero regardless of the initial error.
- [[Hartley2019contact - Contact-Aided Invariant Extended Kalman Filtering for Robot#^hartley2019contact-038]] — Because samples are mapped from the Lie algebra, the InEKF closely matches the curved position distribution produced by growing yaw uncertainty.
- [[Yaqubi2026invariant - Invariant Stochastic Filtering on SE(3) for#^yaqubi2026invariant-001]] — An invariant extended Kalman filter is presented for state estimation of serial rigid manipulators with an arbitrary number of links, grounded on SE(3).
- [[Yaqubi2026invariant - Invariant Stochastic Filtering on SE(3) for#^yaqubi2026invariant-004]] — The invariant EKF exploits a group-affine condition under which linearised error dynamics are autonomous, so the Riccati equation governs the true covariance.
- [[Yaqubi2026invariant - Invariant Stochastic Filtering on SE(3) for#^yaqubi2026invariant-021]] — The authors conclude that the IEKF linearisation is exact for the pose kinematics, so the Riccati equation governs the true error covariance.
- [[Yaqubi2026invariant - Invariant Stochastic Filtering on SE(3) for#^yaqubi2026invariant-055]] — The text reports a 24% RMSE reduction of the IEKF relative to the coordinate EKF on all joints.
- [[Brossard2020code - A Code for Unscented Kalman Filtering on Manifolds (UKF-M)#^brossard2020code-047]] — The SE2(3) UKF improves on the invariant EKF of reference 19 during the first 10 seconds of the trajectory.

## Relations

- RELATES_TO → [[Group-affine dynamics]]
  · type: requires
  · evidence: [[Yaqubi2026invariant - Invariant Stochastic Filtering on SE(3) for#^yaqubi2026invariant-004]]

## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 4 sources · topic: Probability, filtering and generative models on Lie groups (drafter's packet `q2-lie-probability`, confirmed at the gate)
