---
aliases: []
type: "source"
title: "A Code for Unscented Kalman Filtering on Manifolds (UKF-M)"
citekey: "Brossard2020code"
doi: "10.48550/arXiv.2002.00878"
arxiv: "2002.00878"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2002.00878"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Martin Brossard", "Axel Barrau", "Silvere Bonnabel"]
sha256: ["eb24132fe7ed31df50e114feda864a943f1047e376ebc9846117e4c283fd0410"]
pdf: "Content/Papers/Brossard2020code.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Brossard2020code.pdf]]

> [!abstract] One-sentence summary
> The paper presents UKF-M, a simple unscented Kalman filter recipe for states on parallelizable manifolds and Lie groups, released as independent Python and Matlab code with robotics examples for fast prototyping and benchmarking.

## Abstract

The present paper introduces a novel methodology for Unscented Kalman Filtering (UKF) on manifolds that extends previous work by the authors on UKF on Lie groups. Beyond filtering performance, the main interests of the approach are its versatility, as the method applies to numerous state estimation problems, and its simplicity of implementation for practitioners not being necessarily familiar with manifolds and Lie groups. We have developed the method on two independent open-source Python and Matlab frameworks we call UKF-M, for quickly implementing and testing the approach. The online repositories contain tutorials, documentation, and various relevant robotics examples that the user can readily reproduce and then adapt, for fast prototyping and benchmarking. The code is available at https://github.com/CAOR-MINES-ParisTech/ukfm. (arXiv)

## 🧠 Key ideas (atomic)

- The paper introduces UKF-M, a novel and general method for unscented Kalman filtering on manifolds, supported by independent Python and Matlab implementations. (Brossard et al., 2020) `ev:asserted` p. 1 ^brossard2020code-001
- The authors present their main methodological contribution as a framework for unscented Kalman filtering on manifolds that is simpler than existing methods. (Brossard et al., 2020) `ev:asserted` p. 1 ^brossard2020code-002
- The authors state that the versatility of their framework allows direct application to all manifolds encountered in practice. (Brossard et al., 2020) `ev:asserted` p. 1 ^brossard2020code-003
- According to the authors, the methodology spares the analytic computation of Jacobians, contrary to the EKF, making it well suited to fast prototyping. (Brossard et al., 2020) `ev:asserted` p. 1 ^brossard2020code-004
- Cited work reports that using the Lie group SE2(3) has led to drastic improvement of Kalman filters for robot state estimation. (Brossard et al., 2020) `ev:cited` p. 1 ^brossard2020code-005
- Cited work reports that using the group SEk(n), introduced for simultaneous localization and mapping, makes the EKF consistent or convergent. (Brossard et al., 2020) `ev:cited` p. 1 ^brossard2020code-006
- Earlier unscented filters in references 7 and 8 rely on the Levi-Civita connection, whose differential geometry the authors call difficult to master. (Brossard et al., 2020) `ev:cited` p. 2 ^brossard2020code-007
- Several earlier unscented filtering methods cited by the authors are reserved for the specific groups SO(3) and SE(3) only. (Brossard et al., 2020) `ev:cited` p. 2 ^brossard2020code-008
- A cited sigma-point Kalman filter on Lie groups requires more knowledge of Lie theory than the present paper, according to the authors. (Brossard et al., 2020) `ev:cited` p. 2 ^brossard2020code-009
- A smooth manifold of dimension d is called parallelizable when d smooth vector fields form a basis of the tangent space at every point. (Brossard et al., 2020) `ev:asserted` p. 2 ^brossard2020code-010
- The paper states that all Lie groups are parallelizable manifolds, a notion much broader than the simple cylinder example. (Brossard et al., 2020) `ev:asserted` p. 2 ^brossard2020code-011
- The authors note that not all manifolds are parallelizable, an issue they later address by over-parameterizing the state. (Brossard et al., 2020) `ev:asserted` p. 2 ^brossard2020code-012
- The belief on the manifold is defined through a user-chosen smooth map phi applied to the mean estimate and a Gaussian tangent vector. (Brossard et al., 2020) `ev:asserted` p. 3 ^brossard2020code-013
- The map phi is required to return the mean at zero perturbation with an identity Jacobian with respect to the perturbation. (Brossard et al., 2020) `ev:asserted` p. 3 ^brossard2020code-014
- The authors stress that the resulting distribution on the manifold is not Gaussian, being Gaussian only in the coordinates of phi. (Brossard et al., 2020) `ev:asserted` p. 3 ^brossard2020code-015
- For rotation matrices in SO(3), phi can be chosen as the rotation multiplied by the exponential of the wedged tangent vector. (Brossard et al., 2020) `ev:asserted` p. 3 ^brossard2020code-016
- A canonical choice of phi is an exponential map obtained by integrating the weighted sum of vector fields for one unit of time. (Brossard et al., 2020) `ev:asserted` p. 3 ^brossard2020code-017
- When the exponential map has no closed form, the paper says one resorts to simpler retractions for the map phi. (Brossard et al., 2020) `ev:asserted` p. 3 ^brossard2020code-018
- The Bayesian update passes 2d sigma points through the measurement function to approximate the posterior of the tangent error with the unscented transform. (Brossard et al., 2020) `ev:reported` p. 4 ^brossard2020code-019
- The authors view this update as a Kalman update on the error, in the vein of error state Kalman filtering. (Brossard et al., 2020) `ev:asserted` p. 4 ^brossard2020code-020
- The updated mean estimate is obtained by applying phi to the prior estimate and the posterior mean of the tangent error. (Brossard et al., 2020) `ev:asserted` p. 4 ^brossard2020code-021
- When the manifold is a vector space, the approximation used in the update holds up to first order in the small dispersions. (Brossard et al., 2020) `ev:asserted` p. 4 ^brossard2020code-022
- Computing the propagated mean as a weighted mean on the manifold is an optimization route that earlier unscented filters have advocated. (Brossard et al., 2020) `ev:cited` p. 5 ^brossard2020code-023
- To keep the implementation simple and analogous to the EKF, the authors propagate the mean through the noise-free state model. (Brossard et al., 2020) `ev:asserted` p. 5 ^brossard2020code-024
- State-error sigma points are passed through the noise-free model, then mapped back to Euclidean space by the inverse of phi to compute their covariance. (Brossard et al., 2020) `ev:reported` p. 5 ^brossard2020code-025
- The method requires a local inverse of phi that recovers the tangent perturbation up to second-order terms in its norm. (Brossard et al., 2020) `ev:asserted` p. 5 ^brossard2020code-026
- Sigma points for the process noise yield a second covariance matrix that is added to the propagated state-error covariance. (Brossard et al., 2020) `ev:reported` p. 5 ^brossard2020code-027
- The scale parameter alpha that sets the sigma-point weights is generally chosen between 10−3 and 1 in this filter. (Brossard et al., 2020) `ev:reported` p. 5 ^brossard2020code-028
- Propagating the mean with the model while computing covariance with sigma points was done earlier for pose compounding on SE(3). (Brossard et al., 2020) `ev:cited` p. 5 ^brossard2020code-029
- On a Lie group, choosing phi as the estimate right-multiplied by the exponential corresponds to left concentrated Gaussians on the group. (Brossard et al., 2020) `ev:asserted` p. 5 ^brossard2020code-030
- The paper gives two Lie group retractions, left or right multiplication by the exponential, each inverted with the group logarithm. (Brossard et al., 2020) `ev:asserted` p. 6 ^brossard2020code-031
- The group SEk(d) recovers SE(3), SE(2) and SO(3) as special cases for particular choices of the integers k and d. (Brossard et al., 2020) `ev:asserted` p. 6 ^brossard2020code-032
- The authors write that SEk(d) seems to cover virtually all robotics applications where the Lie group methodology has been useful so far. (Brossard et al., 2020) `ev:asserted` p. 6 ^brossard2020code-033
- The mixed case places the state in a group times a vector space, typically to estimate extra parameters such as sensor biases. (Brossard et al., 2020) `ev:asserted` p. 6 ^brossard2020code-034
- Cited robotics work has largely argued that the Lie group structure of SE(3) is more relevant for poses than SO(3)×R3. (Brossard et al., 2020) `ev:cited` p. 7 ^brossard2020code-035
- For IMU and GNSS fusion, the state may be divided into an SE2(3) vehicle state and IMU biases in R6. (Brossard et al., 2020) `ev:reported` p. 7 ^brossard2020code-036
- The authors released a Python package and a Matlab toolbox of UKF-M, described as wholly independent implementations of the method. (Brossard et al., 2020) `ev:reported` p. 7 ^brossard2020code-037
- The Python package follows the class-object paradigm, with heavy documentation produced through the Sphinx documentation generator. (Brossard et al., 2020) `ev:reported` p. 7 ^brossard2020code-038
- The Matlab toolbox contains equivalent functions without classes, since the authors believe well chosen function names suit Matlab use better. (Brossard et al., 2020) `ev:asserted` p. 7 ^brossard2020code-039
- Designing a filter requires a model with functions f and h, the maps phi and its inverse, noise covariances, and initial estimates. (Brossard et al., 2020) `ev:reported` p. 7 ^brossard2020code-040
- The paper states that noise covariance values are commonly guided by the model and then tuned by the practitioner. (Brossard et al., 2020) `ev:asserted` p. 7 ^brossard2020code-041
- A quick comparison indicates the SE2(3) filter with right multiplications outperforms the other filters, notably the naive SO(3)×R6 filter. (Brossard et al., 2020) `ev:measured` p. 7 ^brossard2020code-042
- The code includes examples for 2D localization, 3D attitude estimation, inertial navigation, 2D SLAM, KITTI IMU-GNSS fusion, and a 2-sphere pendulum. (Brossard et al., 2020) `ev:reported` p. 8 ^brossard2020code-043
- For each example the authors simulate Monte-Carlo data to benchmark UKFs and EKFs with accuracy and consistency metrics. (Brossard et al., 2020) `ev:reported` p. 9 ^brossard2020code-044
- The inertial navigation comparison uses large initial heading and position errors of 45 degrees and 1 m respectively. (Brossard et al., 2020) `ev:reported` p. 9 ^brossard2020code-045
- In this inertial navigation test, the UKF based on the SE2(3) exponential clearly outperforms the EKF and the SO(3)×R6 UKF. (Brossard et al., 2020) `ev:measured` p. 9 ^brossard2020code-046
- The SE2(3) UKF improves on the [[Invariant extended Kalman filter|invariant EKF]] of reference 19 during the first 10 seconds of the trajectory. (Brossard et al., 2020) `ev:measured` p. 9 ^brossard2020code-047
- When the manifold is not parallelizable, one cannot define a global uncertainty representation through a single map phi. (Brossard et al., 2020) `ev:asserted` p. 9 ^brossard2020code-048
- The authors feel that covering a manifold with patches induces discontinuities at patch borders that will inevitably degrade filter performance. (Brossard et al., 2020) `ev:asserted` p. 9 ^brossard2020code-049
- The authors consider it undesirable that a patch-based filter wholly depends on the way the patches are chosen. (Brossard et al., 2020) `ev:asserted` p. 9 ^brossard2020code-050
- The paper states that a number of homogeneous spaces may be lifted to a Lie group, which is a parallelizable manifold. (Brossard et al., 2020) `ev:asserted` p. 9 ^brossard2020code-051
- The authors provide a novel script simulating a spherical pendulum whose two position components are measured, for example by a monocular camera. (Brossard et al., 2020) `ev:reported` p. 9 ^brossard2020code-052
- A footnote states that generalizations to the Stiefel manifold, and hence the Grassmann manifold, are then straightforward. (Brossard et al., 2020) `ev:asserted` p. 9 ^brossard2020code-053
- The authors link the discontinuities of patch coverings of the 2-sphere to the theorem that a hairy ball cannot be combed. (Brossard et al., 2020) `ev:cited` p. 10 ^brossard2020code-054
- The 2-sphere dynamics are lifted into SO(3) by writing the state as a rotation matrix applied to a fixed vector. (Brossard et al., 2020) `ev:reported` p. 10 ^brossard2020code-055
- Under linearization, the distribution of the lifted sphere state is approximately Gaussian with covariance obtained from a linear map of P. (Brossard et al., 2020) `ev:computed` p. 10 ^brossard2020code-056
- The authors see the main problem in designing manifold filters as often lacking coordinates to write down the filter equations. (Brossard et al., 2020) `ev:asserted` p. 10 ^brossard2020code-057
- The updated covariance is computed from local information at the prior estimate, although it should encode dispersion at the updated estimate. (Brossard et al., 2020) `ev:asserted` p. 10 ^brossard2020code-058
- The authors conclude it is up to the user to define how Gaussians are transported over the manifold between estimates. (Brossard et al., 2020) `ev:asserted` p. 10 ^brossard2020code-059
- In Lie group state estimation, cited work finds that the transport operations giving the best performances are not torsion free. (Brossard et al., 2020) `ev:cited` p. 11 ^brossard2020code-060
- When the best transport operation is unclear, the authors suggest using their code for quick benchmarking of alternative choices. (Brossard et al., 2020) `ev:asserted` p. 11 ^brossard2020code-061
- The authors interpret the SE2(3) versus SO(3)×R6 structures as particular choices of parallelization, and hence of transport operation. (Brossard et al., 2020) `ev:asserted` p. 11 ^brossard2020code-062

## 🎯 Contributions

## 📖 Glossary

- **Parallelizable manifold** — manifold with d smooth vector fields forming a tangent-space basis everywhere.
- **Retraction (phi)** — smooth map sending a mean and tangent vector to a point on the manifold.
- **Unscented transform** — deterministic sigma-point sampling that propagates mean and covariance through nonlinear functions.
- **Sigma points** — 2d perturbations built from the covariance square root, used by the UKF.
- **SE2(3)** — group of double direct isometries encoding orientation, velocity and position for inertial navigation.
- **SEk(d)** — group of multiple spatial isometries, generalizing SE(3), SE(2) and SO(3).
- **Lifting** — rewriting a homogeneous-space state as a Lie group element to regain parallelizability.
- **Mixed case** — state living in a Lie group times a Euclidean space, e.g. with biases.

## ❓ Open questions

- How much does the choice of retraction (left versus right multiplication) matter across the other shipped examples beyond inertial navigation?
- Is propagating the mean with the noise-free model measurably worse than computing a weighted manifold mean in strongly nonlinear cases?
- How should the covariance be transported from the prior to the updated estimate in a principled way?
- Does the SE2(3) UKF keep its advantage over the invariant EKF after the first 10 seconds of the trajectory?
- Which homogeneous spaces encountered in robotics cannot be conveniently lifted to a Lie group?

## 📝 Notes on reading

The cached text contains the paper twice: a single-column rendering on pages 1-13 and a two-column rendering of the same arXiv v2 (11 Mar 2020) on pages 14-21. All claims cite the first rendering (pages 1-11); pages 12-13 and 20-21 are references only.

Figure 2 plots position error norm (m) against time (0-30 s) for EKF, SO(3)×R6 UKF, the EKF of reference 19 and SE2(3) UKF; curve values could not be read from the extraction, so only the text's qualitative comparison is claimed. Figure 3 (patches on the 2-sphere) was only described.

The experiments are small illustrative simulations; no tables of numeric accuracy or consistency results appear in the paper, which points to the code documentation for benchmarks.

Equation (9) prints K = PξyPyy without the inverse, while Algorithm 1 line 7 uses the inverse of Pyy; likely an extraction or typesetting slip. Snippet 3 writes hat_hat where hat_chi is defined, an apparent typo in the paper's code.

## Suggested new concepts

- Unscented Kalman filter on manifolds — general sigma-point filtering via retractions, reusable across estimation papers.
- Parallelizable manifold — the structural condition that makes a global uncertainty representation possible.
- Retraction-based uncertainty representation — the concentrated-Gaussian idea shared by invariant EKF and Lie group UKF work.
- SE2(3) group — recurring state representation for IMU-based navigation with strong filter benefits.
- UKF-M library — open-source tool practitioners may use to benchmark manifold filters.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H2.** UKF genérico en variedades mediante retracciones y sin Jacobianos, con código Python listo para filtrar la pose del efector o de los objetos.

<!-- ingest-checker dropped 3 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
