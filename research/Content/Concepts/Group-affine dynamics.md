---
aliases: ["Group affine dynamics", "Group-affine systems", "group affine property", "group-compatibility condition"]
type: concept
element_type: concept
topic: "[[Probability, filtering and generative models on Lie groups]]"
topics: ["[[Probability, filtering and generative models on Lie groups]]"]
created: 2026-09-19
---

## Working definition

The class of dynamics on a Lie group (condition (7) of Barrau and Bonnabel, which includes left- and right-invariant dynamics and reduces to affine dynamics on a vector space) for which the invariant estimation error evolves autonomously and its logarithm obeys an exact linear equation.

## Evidence

- [[Barrau2017invariant - The invariant extended Kalman filter as a stable observer#^barrau2017invariant-009]] — Theorem 1 shows the invariant errors are state-trajectory independent if and only if the dynamics satisfy a group-compatibility condition, equation (7).
- [[Barrau2017invariant - The invariant extended Kalman filter as a stable observer#^barrau2017invariant-010]] — Remark 1 verifies that left-invariant dynamics, right-invariant dynamics, and combinations of both satisfy the group-compatibility condition (7).
- [[Hartley2019contact - Contact-Aided Invariant Extended Kalman Filtering for Robot#^hartley2019contact-002]] — The authors show that the deterministic contact-inertial system satisfies the group affine property, therefore its error dynamics is exactly log-linear.
- [[Hartley2019contact - Contact-Aided Invariant Extended Kalman Filtering for Robot#^hartley2019contact-005]] — Barrau and Bonnabel showed that group affine dynamics on a Lie group give an estimation error satisfying a log-linear autonomous equation.
- [[Yaqubi2026invariant - Invariant Stochastic Filtering on SE(3) for#^yaqubi2026invariant-004]] — The invariant EKF exploits a group-affine condition under which linearised error dynamics are autonomous, so the Riccati equation governs the true covariance.
- [[Yaqubi2026invariant - Invariant Stochastic Filtering on SE(3) for#^yaqubi2026invariant-020]] — The left-invariant pose error is shown to evolve autonomously, independently of the pose estimate, establishing the group-affine property of the pose kinematics.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 3 sources · topic: Probability, filtering and generative models on Lie groups (drafter's packet `q2-lie-probability`, confirmed at the gate)
