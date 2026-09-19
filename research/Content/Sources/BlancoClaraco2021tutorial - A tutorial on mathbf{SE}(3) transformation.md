---
aliases: []
type: "source"
title: "A tutorial on $\\mathbf{SE}(3)$ transformation parameterizations and on-manifold optimization"
citekey: "BlancoClaraco2021tutorial"
doi: "10.48550/arXiv.2103.15980"
arxiv: "2103.15980"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2103.15980"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["José Luis Blanco-Claraco"]
sha256: ["1c46c46f941021150cdc681b42154a4db628b9d96fb212a32bc4a47bb5bd254a"]
pdf: "Content/Papers/BlancoClaraco2021tutorial.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 58
---

📄 PDF: [[BlancoClaraco2021tutorial.pdf]]

> [!abstract] One-sentence summary
> A technical report that unifies yaw-pitch-roll, quaternion and matrix pose parameterizations, their conversions, compositions and Gaussian uncertainty propagation, and derives the Lie-group Jacobians needed for on-manifold optimization in SLAM and computer vision.

## Abstract

An arbitrary rigid transformation in $\mathbf{SE}(3)$ can be separated into two parts, namely, a translation and a rigid rotation. This technical report reviews, under a unifying viewpoint, three common alternatives to representing the rotation part: sets of three (yaw-pitch-roll) Euler angles, orthogonal rotation matrices from $\mathbf{SO}(3)$ and quaternions. It will be described: (i) the equivalence between these representations and the formulas for transforming one to each other (in all cases considering the translational and rotational parts as a whole), (ii) how to compose poses with poses and poses with points in each representation and (iii) how the uncertainty of the poses (when modeled as Gaussian distributions) is affected by these transformations and compositions. Some brief notes are also given about the Jacobians required to implement least-squares optimization on manifolds, an very promising approach in recent engineering literature. The text reflects which MRPT C++ library functions implement each of the described algorithms. All formulas and their implementation have been thoroughly validated by means of unit testing and numerical estimation of the Jacobians (arXiv)

## 🧠 Key ideas (atomic)

- All formulas and their implementation have been thoroughly validated by unit testing and numerical estimation of the Jacobians, the report states. (Blanco-Claraco, 2021) `ev:abstract` p. 2 ^blancoclaraco2021tutorial-001
- The document version history of this technical report dates its very first version to 1/Sep/2010. (Blanco-Claraco, 2021) `ev:reported` p. 4 ^blancoclaraco2021tutorial-002
- The report refers to SE(3) transformations as poses, whose six degrees of freedom justify the alternative name 6D poses. (Blanco-Claraco, 2021) `ev:asserted` p. 9 ^blancoclaraco2021tutorial-003
- The yaw-pitch-roll convention used here applies yaw around Z, then pitch around the modified Y axis, then roll around the modified X axis. (Blanco-Claraco, 2021) `ev:reported` p. 11 ^blancoclaraco2021tutorial-004
- Yaw-pitch-roll and roll-pitch-yaw forms give identical numeric values for any 3D rotation, so both forms are completely equivalent. (Blanco-Claraco, 2021) `ev:cited` p. 11 ^blancoclaraco2021tutorial-005
- The 3D+YPR form is the most compact pose representation, requiring only 6 real parameters, the minimum for 6 degrees of freedom. (Blanco-Claraco, 2021) `ev:asserted` p. 11 ^blancoclaraco2021tutorial-006
- Yaw-pitch-roll angles have two degenerate gimbal-lock cases when pitch approaches ±90◦, where a change in roll becomes a change in yaw. (Blanco-Claraco, 2021) `ev:asserted` p. 11 ^blancoclaraco2021tutorial-007
- In the MRPT library, poses based on quaternions are implemented in the class mrpt::poses::CPose3DQuat, whose quaternion part stays normalized. (Blanco-Claraco, 2021) `ev:reported` p. 12 ^blancoclaraco2021tutorial-008
- Poses based on yaw-pitch-roll angles are implemented in the MRPT C++ class mrpt::poses::CPose3D, according to the implementation notes. (Blanco-Claraco, 2021) `ev:reported` p. 12 ^blancoclaraco2021tutorial-009
- The quaternion part of a 3D+Quat pose may drift from unit length, especially when each component is estimated independently, as in Kalman filters. (Blanco-Claraco, 2021) `ev:asserted` p. 12 ^blancoclaraco2021tutorial-010
- Uncertainty is propagated between parameterizations by first-order linearization of the transforming functions, proposed as a simple, effective approximation. (Blanco-Claraco, 2021) `ev:reported` p. 15 ^blancoclaraco2021tutorial-011
- The scaled unscented transform may give more exact results for large levels of uncertainty but typically requires more computation time. (Blanco-Claraco, 2021) `ev:cited` p. 15 ^blancoclaraco2021tutorial-012
- Converting a normalized quaternion to yaw-pitch-roll angles requires special cases when the discriminant ∆ reaches a magnitude of 1/2. (Blanco-Claraco, 2021) `ev:computed` p. 17 ^blancoclaraco2021tutorial-013
- The storage of 16 elements makes 3D+YPR or 3D+Quat representations more advisable than matrices in many situations, the report argues. (Blanco-Claraco, 2021) `ev:asserted` p. 19 ^blancoclaraco2021tutorial-014
- For composing or inverse composing a pose with a 3D point, matrices require about half the computation time of the other methods. (Blanco-Claraco, 2021) `ev:asserted` p. 19 ^blancoclaraco2021tutorial-015
- Composing a pose with another pose is described as a slightly more efficient operation to carry out with a 3D+Quat representation. (Blanco-Claraco, 2021) `ev:asserted` p. 19 ^blancoclaraco2021tutorial-016
- With uncertainties, transformation matrices are not a reasonable choice due to the quadratic cost of keeping their covariance matrices. (Blanco-Claraco, 2021) `ev:asserted` p. 19 ^blancoclaraco2021tutorial-017
- The report states that the most common representation of a 6D pose with uncertainty in the literature is the 3D+Quat form. (Blanco-Claraco, 2021) `ev:cited` p. 19 ^blancoclaraco2021tutorial-018
- For orthonormal matrices, a more efficient alternative converts the rotation matrix to yaw-pitch-roll angles first, then to a quaternion. (Blanco-Claraco, 2021) `ev:asserted` p. 23 ^blancoclaraco2021tutorial-019
- An approximate pose-point composition Jacobian proposed in earlier work applies only to very small rotations, treating sines as zero, cosines as one. (Blanco-Claraco, 2021) `ev:cited` p. 25 ^blancoclaraco2021tutorial-020
- Any inverse pose composition can be rewritten as a normal pose composition by switching the two arguments, then inverting the pose. (Blanco-Claraco, 2021) `ev:computed` p. 30 ^blancoclaraco2021tutorial-021
- No simple equation exists for composing yaw-pitch-roll poses, so the report recommends converting them to quaternion or matrix form before composing. (Blanco-Claraco, 2021) `ev:asserted` p. 31 ^blancoclaraco2021tutorial-022
- Covariance of composed yaw-pitch-roll poses is obtained by chaining Jacobians of conversion to quaternion form, quaternion composition, conversion back. (Blanco-Claraco, 2021) `ev:computed` p. 32 ^blancoclaraco2021tutorial-023
- Composing two 3D+Quat poses combines a pose-point composition for translation, a quaternion product, a final quaternion normalization function. (Blanco-Claraco, 2021) `ev:computed` p. 32 ^blancoclaraco2021tutorial-024
- In derivative expressions, poses become 12-vectors by vec-expanding the top 3 × 4 submatrix of their transformation matrices. (Blanco-Claraco, 2021) `ev:reported` p. 39 ^blancoclaraco2021tutorial-025
- Although 12-vectors over-parameterize an entity with 6 DOFs, many important operations become linear, enabling exact derivatives in an efficient way. (Blanco-Claraco, 2021) `ev:asserted` p. 39 ^blancoclaraco2021tutorial-026
- Citing a theorem of Von Neumann and Cartan, the report states that a closed subgroup of GL(N, R) is a linear Lie group. (Blanco-Claraco, 2021) `ev:cited` p. 44 ^blancoclaraco2021tutorial-027
- Because SE(3) is isomorphic to a subset of GL(4, R), the report concludes it is also a linear Lie group. (Blanco-Claraco, 2021) `ev:cited` p. 44 ^blancoclaraco2021tutorial-028
- SE(3) is not isomorphic to SO(3) × R3 as a group because the group multiplications of both groups are different. (Blanco-Claraco, 2021) `ev:cited` p. 46 ^blancoclaraco2021tutorial-029
- The Lie algebra se(3) has six 4×4 generator matrices, corresponding to infinitesimal rotations or translations along each axis. (Blanco-Claraco, 2021) `ev:asserted` p. 47 ^blancoclaraco2021tutorial-030
- The SO(3) exponential map is surjective, with a closed-form solution given by the Rodrigues formula from 1840. (Blanco-Claraco, 2021) `ev:cited` p. 48 ^blancoclaraco2021tutorial-031
- An alternative approach for θ = π determines the rotation axis for angles close to π without numerical issues, the report states. (Blanco-Claraco, 2021) `ev:asserted` p. 49 ^blancoclaraco2021tutorial-032
- The SE(3) exponential map has a closed form in which the translation is multiplied by a matrix V that depends on the rotation. (Blanco-Claraco, 2021) `ev:computed` p. 50 ^blancoclaraco2021tutorial-033
- The SE(3) logarithm recovers translation coordinates by applying the inverse of V, for which a closed-form expression exists. (Blanco-Claraco, 2021) `ev:cited` p. 51 ^blancoclaraco2021tutorial-034
- The SE(3) pseudo-exponential exponentiates only the rotation, leaving translation intact, which leads to Jacobians more efficient to evaluate. (Blanco-Claraco, 2021) `ev:asserted` p. 51 ^blancoclaraco2021tutorial-035
- Since MRPT 2.0, pseudo-exponential and pseudo-logarithm maps are available in the namespace mrpt::poses::Lie::SE<n>, for n=2 or 3. (Blanco-Claraco, 2021) `ev:reported` p. 52 ^blancoclaraco2021tutorial-036
- Gradient descent, Gauss-Newton, Levenberg-Marquart and Kalman filters all iteratively improve a state vector to minimize a sum of squared errors. (Blanco-Claraco, 2021) `ev:asserted` p. 53 ^blancoclaraco2021tutorial-037
- These optimization methods are designed to work on flat Euclidean spaces, which raises a problem when SE(3) poses are part of the state vector. (Blanco-Claraco, 2021) `ev:asserted` p. 53 ^blancoclaraco2021tutorial-038
- Stored as vectors, poses take 6, 7, 16 or 12 elements for yaw-pitch-roll, quaternion, full matrix or 3 × 4 submatrix forms. (Blanco-Claraco, 2021) `ev:reported` p. 53 ^blancoclaraco2021tutorial-039
- With yaw-pitch-roll states, additive updates may push the three angles out of their valid ranges, requiring renormalization after each update. (Blanco-Claraco, 2021) `ev:asserted` p. 54 ^blancoclaraco2021tutorial-040
- The 3D+Quat parameterization always has well-defined Jacobians but carries one extra degree of freedom, with the associated optimization problems. (Blanco-Claraco, 2021) `ev:asserted` p. 54 ^blancoclaraco2021tutorial-041
- The report concludes that storing poses in a state vector and trying to optimize them directly is not a good idea. (Blanco-Claraco, 2021) `ev:asserted` p. 54 ^blancoclaraco2021tutorial-042
- The 3D+Quat parameterization is bad to a lesser degree, still usable, having led to good results in computer vision. (Blanco-Claraco, 2021) `ev:cited` p. 54 ^blancoclaraco2021tutorial-043
- Optimization directly on the manifold is gaining popularity in the robotics and computer vision community, although the idea is not new. (Blanco-Claraco, 2021) `ev:cited` p. 54 ^blancoclaraco2021tutorial-044
- On-manifold optimization replaces the additive update with a boxplus operator, composing the state with the exponential map of the increment. (Blanco-Claraco, 2021) `ev:cited` p. 54 ^blancoclaraco2021tutorial-045
- GraphSLAM problems additionally require the boxminus operator, defined as the logarithm of the inverse of x composed with y. (Blanco-Claraco, 2021) `ev:reported` p. 54 ^blancoclaraco2021tutorial-046
- The Jacobian of the SE(3) exponential generator is called the most basic one, since its term appears in all on-manifold optimization problems. (Blanco-Claraco, 2021) `ev:asserted` p. 55 ^blancoclaraco2021tutorial-047
- The SO(3) logarithm Jacobian switches to a constant matrix when cos θ exceeds 0.999999, using a different expression otherwise. (Blanco-Claraco, 2021) `ev:computed` p. 56 ^blancoclaraco2021tutorial-048
- Composing a perturbed pose with a point is an operation needed, for example, in bundle adjustment implementations. (Blanco-Claraco, 2021) `ev:cited` p. 57 ^blancoclaraco2021tutorial-049
- The Jacobian of a point composed with a left-perturbed pose reduces to a 3 × 6 matrix of identity and skew-symmetric blocks. (Blanco-Claraco, 2021) `ev:computed` p. 58 ^blancoclaraco2021tutorial-050
- Graph-SLAM in SE(3) optimizes global poses given a measurement of the relative pose between them, minimizing a composed error. (Blanco-Claraco, 2021) `ev:asserted` p. 59 ^blancoclaraco2021tutorial-051
- The Graph-SLAM error Jacobians with respect to the manifold increments of both poses are 6 × 6 matrices obtained through the chain rule. (Blanco-Claraco, 2021) `ev:computed` p. 60 ^blancoclaraco2021tutorial-052
- The appendix derives the Jacobian of the ideal pinhole projection with respect to the point coordinates relative to the camera. (Blanco-Claraco, 2021) `ev:computed` p. 61 ^blancoclaraco2021tutorial-053
- Separate projection Jacobians are given for problems estimating inverse camera poses, versus problems estimating the actual camera positions. (Blanco-Claraco, 2021) `ev:computed` p. 63 ^blancoclaraco2021tutorial-054
- SE(2) poses have a much simpler structure than SE(3) poses, motivating simpler, more efficient expressions for 2D SLAM problems. (Blanco-Claraco, 2021) `ev:asserted` p. 64 ^blancoclaraco2021tutorial-055
- The simpler SE(2) pseudo maps are more efficient to evaluate than the rigorous maps, so the MRPT formulas use them. (Blanco-Claraco, 2021) `ev:asserted` p. 64 ^blancoclaraco2021tutorial-056
- With translation used directly as local coordinates, the SE(2) pseudo-exponential map has an identity Jacobian. (Blanco-Claraco, 2021) `ev:computed` p. 65 ^blancoclaraco2021tutorial-057
- For SE(2) Graph-SLAM, the error vector is assumed to be the pseudo-logarithm of the pose mismatch. (Blanco-Claraco, 2021) `ev:reported` p. 66 ^blancoclaraco2021tutorial-058

## 🎯 Contributions

## 📖 Glossary

- **SE(3)** — group of 3D rigid transformations, rotation plus translation, as 4×4 matrices.
- **SO(3)** — group of 3×3 proper rotation matrices with determinant +1.
- **3D+YPR** — pose as a 3D translation plus yaw, pitch and roll angles.
- **3D+Quat** — pose as a 3D translation plus a unit quaternion; seven parameters.
- **Gimbal lock** — yaw-pitch-roll degeneracy at pitch ±90° where roll and yaw coincide.
- **Lie algebra** — tangent space of a Lie group at its identity element.
- **Exponential map** — maps Lie algebra elements onto the group manifold.
- **Boxplus** — manifold generalization of addition: state composed with exponential of the increment.
- **Boxminus** — manifold difference: logarithm of the inverse of x times y.
- **Pseudo-exponential** — SE(3) retraction exponentiating only rotation, keeping translation intact.
- **MRPT** — C++ robotics library that implements every formula in the report.

## ❓ Open questions

- How does first-order linearized covariance propagation compare numerically with the scaled unscented transform at large uncertainty?
- How large are the timing differences behind the claim that matrices halve pose-point composition cost, given no benchmark is reported?
- How does the pseudo-exponential retraction affect convergence of SE(3) optimization compared with the true exponential map?
- Which tolerances and test cases were used in the unit-test validation of the formulas and Jacobians?

## 📝 Notes on reading

The cached text is arXiv v2 of the report (Technical report #012010, last update 08/04/2022), while the metadata year is 2021. Nearly all equations and Jacobian matrices were garbled by extraction (matrix layouts broken into one symbol per line), so no individual matrix entries were claimed; only their sizes and structure as stated in prose. Figures 1.1 to 1.4, 8.1 and A.1 (pose schematics, yaw-pitch-roll convention, quaternion axis, manifold and tangent space, pinhole camera axes) could only be described. The validation by unit testing appears only in the abstract (p. 2), with no test results in the body. Efficiency statements (matrices about half the time for pose-point composition, quaternions slightly better for pose-pose composition) are given without measurements. Typos in the source: Von Newman for Von Neumann (p. 44), Levenberg-Marquart (p. 53), 3D+Quad (p. 31), and a self-referencing range §B.2.1–B.2.1 (p. 64). The version history (pp. 3–4) lists equation fixes, including a transpose in Eq. (7.13). Much of the content is textbook background (group, manifold, Lie group definitions in chapter 8) and MRPT code snippets, which were not claimed one by one.

## Suggested new concepts

- On-manifold optimization — core technique linking pose estimation, SLAM and bundle adjustment across sources.
- SE(3) Lie group — foundational structure for pose representation, exponential maps and Jacobians.
- Gimbal lock — recurring pitfall of Euler-angle parameterizations in estimation and optimization.
- Linearized covariance propagation — first-order uncertainty transfer used throughout robotics state estimation.
- Pseudo-exponential retraction — cheaper alternative to the exact SE(3) exponential map in solvers.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H1.** Tutorial con los Jacobianos de composición, Exp y Log en SE(3) y el esquema Gauss-Newton en la variedad que usa la IK por LM del proyecto.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
