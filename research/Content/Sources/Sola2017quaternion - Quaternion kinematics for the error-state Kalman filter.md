---
aliases: []
type: "source"
title: "Quaternion kinematics for the error-state Kalman filter"
citekey: "Sola2017quaternion"
doi: "10.48550/arXiv.1711.02508"
arxiv: "1711.02508"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1711.02508"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Joan Solà"]
sha256: ["6a3d3d3933c425eb6cef049290c2b48b71a90f5189e9810575d83d3a922faaca"]
pdf: "Content/Papers/Sola2017quaternion.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 65
---

📄 PDF: [[Sola2017quaternion.pdf]]

> [!abstract] One-sentence summary
> A tutorial-style derivation of Hamilton-convention quaternion and SO(3) calculus (exponential maps, perturbations, Jacobians, integration) applied to a complete IMU-driven error-state Kalman filter with local and global angular errors.

## Abstract

This article is an exhaustive revision of concepts and formulas related to quaternions and rotations in 3D space, and their proper use in estimation engines such as the error-state Kalman filter. The paper includes an in-depth study of the rotation group and its Lie structure, with formulations using both quaternions and rotation matrices. It makes special attention in the definition of rotation perturbations, derivatives and integrals. It provides numerous intuitions and geometrical interpretations to help the reader grasp the inner mechanisms of 3D rotation. The whole material is used to devise precise formulations for error-state Kalman filters suited for real applications using integration of signals from an inertial measurement unit (IMU). (arXiv)

## 🧠 Key ideas (atomic)

- This document concentrates on the Hamilton quaternion convention, whose most remarkable property is the algebra defining ijk equal to minus one. (Solà, 2017) `ev:asserted` p. 5 ^sola2017quaternion-001
- Unit quaternions encode rotations in 3D space through a double quaternion product, analogous to unit complex numbers encoding rotations in the plane. (Solà, 2017) `ev:asserted` p. 5 ^sola2017quaternion-002
- The quaternion product is not commutative in general, as revealed by the cross product of the two vector parts in its expression. (Solà, 2017) `ev:computed` p. 7 ^sola2017quaternion-003
- The quaternion product commutes only in the cases where one quaternion is real or where both vector parts are parallel. (Solà, 2017) `ev:computed` p. 7 ^sola2017quaternion-004
- The exponential of a pure quaternion is a unit quaternion, which the author presents as an extension of the Euler formula. (Solà, 2017) `ev:computed` p. 11 ^sola2017quaternion-005
- The unit quaternion group constitutes a double cover of SO(3), a difference the author judges not critical in most of their applications. (Solà, 2017) `ev:asserted` p. 14 ^sola2017quaternion-006
- A rotation matrix representing SO(3) has 9 parameters subject to 6 constraints, leaving 3 degrees of freedom. (Solà, 2017) `ev:computed` p. 15 ^sola2017quaternion-007
- A unit quaternion representing SO(3) has 4 parameters subject to 1 constraint, leaving 3 degrees of freedom. (Solà, 2017) `ev:computed` p. 15 ^sola2017quaternion-008
- The Lie algebra so(3) of skew-symmetric matrices can be interpreted as the tangent space to SO(3), also called the velocity space. (Solà, 2017) `ev:computed` p. 17 ^sola2017quaternion-009
- The pure quaternions constitute the Lie algebra of the unit quaternion sphere, but they form a space of half-velocities rather than velocities. (Solà, 2017) `ev:computed` p. 21 ^sola2017quaternion-010
- Because rotation uses the double product of the quaternion with the vector, the quaternion encodes half the rotation applied to the vector. (Solà, 2017) `ev:computed` p. 21 ^sola2017quaternion-011
- The paper shows that the quaternion sandwich product with the exponential of a rotation vector reproduces the classical vector rotation formula. (Solà, 2017) `ev:computed` p. 23 ^sola2017quaternion-012
- The angle between a unit quaternion and the identity quaternion in four-dimensional space is half the angle rotated in 3D space. (Solà, 2017) `ev:computed` p. 24 ^sola2017quaternion-013
- A quaternion and its negative encode the same rotation, which defines the double cover of SO(3) by unit quaternions. (Solà, 2017) `ev:computed` p. 25 ^sola2017quaternion-014
- The quaternion product composes consecutive rotations in the same order as the corresponding products of rotation matrices do. (Solà, 2017) `ev:computed` p. 26 ^sola2017quaternion-015
- Due to the double cover, quaternion SLERP follows the shortest path only when the two quaternions are separated by an acute angle. (Solà, 2017) `ev:computed` p. 29 ^sola2017quaternion-016
- When the dot product of the two end quaternions is negative, SLERP should replace one quaternion by its negative and start over. (Solà, 2017) `ev:asserted` p. 29 ^sola2017quaternion-017
- For unit quaternions, the left and right quaternion product matrices are proper rotation matrices of four-dimensional space, namely isoclinic rotations. (Solà, 2017) `ev:computed` p. 30 ^sola2017quaternion-018
- A quaternion rotation of a 3D vector corresponds to two chained isoclinic rotations in four-dimensional space, each by half the angle. (Solà, 2017) `ev:computed` p. 32 ^sola2017quaternion-019
- The author states that the isoclinic explanation is incomplete, giving no intuition for why the sandwich product uses the conjugate quaternion. (Solà, 2017) `ev:asserted` p. 33 ^sola2017quaternion-020
- Binary choices on component order, algebra, operator function and operator direction lead to 12 different quaternion convention combinations. (Solà, 2017) `ev:asserted` p. 34 ^sola2017quaternion-021
- According to the author, many works lack a sufficient description of their quaternion with regard to the four binary convention choices. (Solà, 2017) `ev:asserted` p. 34 ^sola2017quaternion-022
- Formulas from different quaternion conventions are not compatible, so the author argues that a clear choice must be made from the start. (Solà, 2017) `ev:asserted` p. 34 ^sola2017quaternion-023
- The chosen Hamilton convention coincides with widely used robotics software libraries such as Eigen, ROS and Google Ceres. (Solà, 2017) `ev:asserted` p. 34 ^sola2017quaternion-024
- The JPL convention is extensively described by Trawny and Roumeliotis, a reference work whose aim and scope are very close to this one. (Solà, 2017) `ev:cited` p. 35 ^sola2017quaternion-025
- Under the Hamilton algebra ij equals k, making the quaternion right-handed so that it turns vectors following the right-hand rule. (Solà, 2017) `ev:cited` p. 36 ^sola2017quaternion-026
- Both the Hamilton and the JPL conventions use the passive interpretation, in which vectors do not move but frames are transformed. (Solà, 2017) `ev:asserted` p. 36 ^sola2017quaternion-027
- The Hamilton convention uses the local-to-global conversion as the default specification of a local frame expressed in a global frame. (Solà, 2017) `ev:asserted` p. 37 ^sola2017quaternion-028
- Numerically equal JPL and Hamilton quaternions mean different things when used in formulas, which the author calls a source of great confusion. (Solà, 2017) `ev:asserted` p. 38 ^sola2017quaternion-029
- The paper defines a plus operator on SO(3) that composes a reference rotation with the exponential of a tangent-space rotation vector. (Solà, 2017) `ev:asserted` p. 38 ^sola2017quaternion-030
- The right Jacobian of SO(3) and its inverse can be computed in closed form, as given by Chirikjian in 2012. (Solà, 2017) `ev:cited` p. 42 ^sola2017quaternion-031
- Because of the Hamilton convention, a local orientation perturbation appears at the right hand side of the composition product. (Solà, 2017) `ev:asserted` p. 44 ^sola2017quaternion-032
- The author finds it convenient to express orientation perturbation covariances in the tangent vector space as a regular 3×3 covariance matrix. (Solà, 2017) `ev:asserted` p. 45 ^sola2017quaternion-033
- Angular rate vectors and small angular perturbations can be transformed between frames with the quaternion or rotation matrix like regular vectors. (Solà, 2017) `ev:computed` p. 47 ^sola2017quaternion-034
- Backward zeroth-order integration is described as the typical method when arriving motion measurements are to be processed in real time. (Solà, 2017) `ev:asserted` p. 49 ^sola2017quaternion-035
- The second-order correction in the first-order quaternion integrator vanishes when consecutive angular rates are collinear, meaning an unchanged rotation axis. (Solà, 2017) `ev:computed` p. 51 ^sola2017quaternion-036
- Unlike zeroth-order integrators, the first-order quaternion integrator does not yield unit quaternions, so users should check and possibly re-normalize the norm. (Solà, 2017) `ev:computed` p. 52 ^sola2017quaternion-037
- Following Madyastha et al., the ESKF orientation error-state is minimal, avoiding over-parametrization and the consequent risk of singular covariance matrices. (Solà, 2017) `ev:cited` p. 52 ^sola2017quaternion-038
- Following Madyastha et al., the error-state is always small, so second-order products are negligible and Jacobians become easy to compute. (Solà, 2017) `ev:cited` p. 52 ^sola2017quaternion-039
- Following Madyastha et al., slow error dynamics allow Kalman filter corrections to be applied at a lower rate than the predictions. (Solà, 2017) `ev:cited` p. 53 ^sola2017quaternion-040
- In the error-state filter, high-frequency IMU data are integrated into a nominal state that does not account for noise or model imperfections. (Solà, 2017) `ev:asserted` p. 53 ^sola2017quaternion-041
- After a filter correction, the estimated error-state mean is injected into the nominal state before the error-state is reset to zero. (Solà, 2017) `ev:asserted` p. 53 ^sola2017quaternion-042
- Most developments define the angular error locally with respect to the nominal orientation, which the author calls the classical approach. (Solà, 2017) `ev:asserted` p. 53 ^sola2017quaternion-043
- Citing Li and Mourikis, the paper notes there exists evidence that a globally-defined angular error has better properties. (Solà, 2017) `ev:cited` p. 53 ^sola2017quaternion-044
- The filter state includes the gravity vector, estimated in the known initial frame rather than assuming a known horizontal orientation. (Solà, 2017) `ev:reported` p. 56 ^sola2017quaternion-045
- Estimating gravity in the initial frame is done to improve linearity, since the velocity equation then becomes linear in gravity. (Solà, 2017) `ev:asserted` p. 56 ^sola2017quaternion-046
- The formulation neglects the Earth rotation rate, which the author notes might become measurable with high-end IMUs having very small noises. (Solà, 2017) `ev:asserted` p. 55 ^sola2017quaternion-047
- Assuming white, uncorrelated and isotropic accelerometer noise lets the rotated noise term be redefined without consequences in the velocity error dynamics. (Solà, 2017) `ev:computed` p. 58 ^sola2017quaternion-048
- The isotropic accelerometer noise assumption cannot be made in cases where the three XYZ accelerometers are not identical. (Solà, 2017) `ev:asserted` p. 58 ^sola2017quaternion-049
- Since the error-state mean is initialized to zero, its linear prediction always returns zero and can be skipped in code. (Solà, 2017) `ev:computed` p. 62 ^sola2017quaternion-050
- The author warns that the covariance prediction must not be skipped, because its perturbation term makes the covariance grow continuously. (Solà, 2017) `ev:asserted` p. 62 ^sola2017quaternion-051
- In a well-designed system, fusing the IMU with other information such as GPS or vision should render the IMU biases observable. (Solà, 2017) `ev:asserted` p. 62 ^sola2017quaternion-052
- The simplest covariance update form is known to have poor numerical stability, so symmetric or Joseph forms may be used instead. (Solà, 2017) `ev:asserted` p. 63 ^sola2017quaternion-053
- Most ESKF implementations neglect the observed error term in the reset Jacobian, which then reduces to an identity and a trivial reset. (Solà, 2017) `ev:asserted` p. 65 ^sola2017quaternion-054
- The full reset Jacobian should produce more precise results, which might be of interest for reducing long-term drift in odometry systems. (Solà, 2017) `ev:asserted` p. 65 ^sola2017quaternion-055
- With a globally-defined angular error, angular rates are still defined locally for convenience, because gyrometers measure them in the body frame. (Solà, 2017) `ev:asserted` p. 66 ^sola2017quaternion-056
- Switching to a globally-defined angular error changes three terms of the error-state transition matrix relative to the local definition. (Solà, 2017) `ev:computed` p. 70 ^sola2017quaternion-057
- With a global angular error, the observed error is injected by left-multiplying the nominal quaternion instead of right-multiplying it. (Solà, 2017) `ev:computed` p. 72 ^sola2017quaternion-058
- Without bias and noise, the angular error transition matrix has a closed-form solution equal to a transposed rotation matrix. (Solà, 2017) `ev:computed` p. 76 ^sola2017quaternion-059
- The paper derives a general closed-form expression for the series needed to build the full IMU error-state transition matrix. (Solà, 2017) `ev:computed` p. 82 ^sola2017quaternion-060
- The author notes that it is unclear how much high-order integration errors impact the performance of real algorithms. (Solà, 2017) `ev:asserted` p. 83 ^sola2017quaternion-061
- Block-wise truncation of the transition matrix is more accurate than system-wide first-order truncation, yet remains easy to obtain and compute. (Solà, 2017) `ev:computed` p. 85 ^sola2017quaternion-062
- Runge-Kutta integration of the transition matrix might be necessary when the dynamic matrix cannot be considered constant over the interval. (Solà, 2017) `ev:asserted` p. 86 ^sola2017quaternion-063
- In the covariance prediction, the dynamic term is exponential in the interval, the measurement term quadratic, and the perturbation term linear. (Solà, 2017) `ev:computed` p. 90 ^sola2017quaternion-064
- For non-isotropic IMUs the trivial impulse Jacobian is not possible, so a proper Jacobian with proper impulse covariances should be used. (Solà, 2017) `ev:asserted` p. 93 ^sola2017quaternion-065

## 🎯 Contributions

## 📖 Glossary

- **Error-state Kalman filter (ESKF)** — Filter estimating a small error around a large-signal nominal state integrated separately.
- **Nominal state** — Large-signal state integrated from IMU data without noise or model imperfections.
- **Hamilton convention** — Right-handed quaternion convention, real part first, local-to-global passive operator.
- **JPL convention** — Left-handed quaternion convention, real part last, global-to-local passive operator.
- **Exponential map (Exp)** — Map from a rotation vector in the tangent space to a rotation element.
- **Double cover** — Property that q and −q encode the same 3D rotation.
- **Right Jacobian of SO(3)** — Maps parameter variations to tangent-space variations at Exp of the parameter.
- **SLERP** — Spherical linear interpolation between two orientations at constant angular speed.
- **Isoclinic rotation** — 4D rotation with equal-magnitude angles in two invariant orthogonal planes.
- **Transition matrix** — Matrix exponential of the dynamic matrix over one step, propagating the error state.

## ❓ Open questions

- What is a geometrical intuition for why the sandwich product uses the conjugate quaternion rather than q itself?
- How much do high-order integration errors of the transition matrix actually affect real filter performance?
- How much does a globally-defined angular error improve accuracy over the local one in practice?
- How much long-term odometry drift does the full, non-trivial reset Jacobian actually remove?
- How should the formulation change for non-isotropic IMUs with non-identical axis sensors?

## 📝 Notes on reading

This is a tutorial/derivation document with no experiments or datasets: every claim rests on derivation, the author's recommendations, or cited works; no `measured` evidence exists. Version read is arXiv v1 (1711.02508v1, dated November 2017), matching the identifier.

Figures described only: Fig. 1 (vector rotation around an axis), Figs. 2-3 (exponential map diagrams for rotation matrix and quaternion), Fig. 4 (double cover illustration), Fig. 5 (rotation composition), Figs. 6-7 (SLERP on the unit sphere and shortest-path correction), Figs. 8-10 (rotations and isoclinic rotations in R4), Fig. 11 (manifold, tangent space, plus/minus operators), Fig. 12 (right Jacobian), Figs. 13-14 (integration schemes).

Most equations and the large matrices (Tables 1, 2, 4; Eqs. 270, 311, 381, 387, 400-402) are flattened and partly garbled by text extraction; only statements in prose were claimed. The Runge-Kutta appendix is stated to be taken from Wikipedia. Minor typos exist in the source (e.g., a [y] instead of [u] in Eq. 348, 'error-estate').

## Suggested new concepts

- Error-state Kalman filter — core estimation architecture for IMU fusion, reused across VIO and SLAM work.
- Quaternion conventions (Hamilton vs JPL) — a recurring source of implementation bugs when mixing libraries or papers.
- Lie-group perturbation calculus on SO(3) — plus/minus operators and Jacobians underpin on-manifold estimation.
- IMU preintegration and transition-matrix discretization — closed-form versus truncated versus Runge-Kutta trade-offs.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Cuaterniones, perturbaciones de rotación, derivadas e integración.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
