---
aliases: []
type: "source"
title: "Integrating generic sensor fusion algorithms with sound state representations through encapsulation of manifolds"
citekey: "Hertzberg2013integrating"
doi: "10.48550/arXiv.1107.1119"
arxiv: "1107.1119"
year: 2013
publication_type: "preprint"
url: "https://arxiv.org/abs/1107.1119"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Christoph Hertzberg", "René Wagner", "Udo Frese", "Lutz Schröder"]
sha256: ["b8f0be7d5b545c7372f7c6e271dc361cc27cf11f1a719c5c82510fa4b21f1f61"]
pdf: "Content/Papers/Hertzberg2013integrating.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Hertzberg2013integrating.pdf]]

> [!abstract] One-sentence summary
> The paper axiomatizes boxplus/boxminus operators that give estimation algorithms a local vector view of manifold states such as 3D orientations, letting least squares and the UKF run on manifolds with minimal changes, and packages this in the Manifold Toolkit (MTK).

## Abstract

Common estimation algorithms, such as least squares estimation or the Kalman filter, operate on a state in a state space S that is represented as a real-valued vector. However, for many quantities, most notably orientations in 3D, S is not a vector space, but a so-called manifold, i.e. it behaves like a vector space locally but has a more complex global topological structure. For integrating these quantities, several ad-hoc approaches have been proposed. Here, we present a principled solution to this problem where the structure of the manifold S is encapsulated by two operators, state displacement [+]:S x R^n --> S and its inverse [-]: S x S --> R^n. These operators provide a local vector-space view δ; --> x [+] δ; around a given state x. Generic estimation algorithms can then work on the manifold S mainly by replacing +/- with [+]/[-] where appropriate. We analyze these operators axiomatically, and demonstrate their use in least-squares estimation and the Unscented Kalman Filter. Moreover, we exploit the idea of encapsulation from a software engineering perspective in the Manifold Toolkit, where the [+]/[-] operators mediate between a "flat-vector" view for the generic algorithm and a "named-members" view for the problem specific functions. (arXiv)

## 🧠 Key ideas (atomic)

- Mathematically sound state representations often form non-Euclidean topological spaces, for example the orientation group SO(3) within inertial navigation systems. (Hertzberg et al., 2013) `ev:asserted` p. 1 ^hertzberg2013integrating-001
- Minimal three-parameter orientation parameterizations such as Euler angles have singularities, analogous to gimbal lock, where small state changes need very large parameter changes. (Hertzberg et al., 2013) `ev:cited` p. 2 ^hertzberg2013integrating-002
- Overparameterizing orientations as unit quaternions or rotation matrices, treated as R4 or R3×3, requires re-normalizing them as needed. (Hertzberg et al., 2013) `ev:cited` p. 2 ^hertzberg2013integrating-003
- Both ad-hoc approaches require representation-specific modifications that tightly couple the state representation to the sensor fusion algorithm. (Hertzberg et al., 2013) `ev:asserted` p. 2 ^hertzberg2013integrating-004
- The approach rests on the observation that sensor fusion algorithms employ inherently local operations on states within a neighborhood around some reference. (Hertzberg et al., 2013) `ev:asserted` p. 2 ^hertzberg2013integrating-005
- The authors propose encapsulating manifold structure in two operators, boxplus mapping S×R^n to S and boxminus mapping S×S to R^n. (Hertzberg et al., 2013) `ev:asserted` p. 2 ^hertzberg2013integrating-006
- The generic algorithm uses ⊟ and ⊞ in place of vector subtraction and addition, treating the state space otherwise as a black box. (Hertzberg et al., 2013) `ev:asserted` p. 2 ^hertzberg2013integrating-007
- The C++ implementation currently provides manifold primitives for R^n, SO(2), SO(3) and S2, from which compound states are generated automatically. (Hertzberg et al., 2013) `ev:reported` p. 2 ^hertzberg2013integrating-008
- Placing Euler-angle singularities in an unused workspace region, the authors argue, creates a failure mode that is easily forgotten. (Hertzberg et al., 2013) `ev:asserted` p. 3 ^hertzberg2013integrating-009
- Normalizing quaternions after each step produces counteracting updates that, according to the authors, at least slow down convergence. (Hertzberg et al., 2013) `ev:asserted` p. 3 ^hertzberg2013integrating-010
- With a redundant normalization degree of freedom, many algorithms such as Gauss-Newton fail due to singular equations. (Hertzberg et al., 2013) `ev:cited` p. 3 ^hertzberg2013integrating-011
- For Lie groups, the Lie group/algebra representation summarized by Strasdat et al. is equivalent to the ⊞-method with s⊞δ = s·exp δ. (Hertzberg et al., 2013) `ev:asserted` p. 3 ^hertzberg2013integrating-012
- The framework is claimed to be more generic than Lie-group approaches, being applicable to manifolds that are not Lie groups, such as S2. (Hertzberg et al., 2013) `ev:asserted` p. 3 ^hertzberg2013integrating-013
- Updating an EKF covariance with the Jacobian of quaternion normalization makes the covariance singular, which the authors consider problematic. (Hertzberg et al., 2013) `ev:asserted` p. 4 ^hertzberg2013integrating-014
- Kraft and Sipos modify the unscented transform with special quaternion operations for adding a perturbation and taking a difference. (Hertzberg et al., 2013) `ev:cited` p. 4 ^hertzberg2013integrating-015
- The von Mises-Fisher distribution can model only isotropic distributions, which is usually not the case for sensor fusion posteriors. (Hertzberg et al., 2013) `ev:asserted` p. 4 ^hertzberg2013integrating-016
- Translating an INS state R3 × SO(3) × R3 into R9 with Euler angles loses the mathematical structure of the state space. (Hertzberg et al., 2013) `ev:asserted` p. 5 ^hertzberg2013integrating-017
- Treating states as flat vectors makes index bookkeeping in process and measurement models cumbersome and error-prone in practice, the authors state. (Hertzberg et al., 2013) `ev:asserted` p. 5 ^hertzberg2013integrating-018
- A ⊞-manifold is defined as a quadruple of a subset of R^s, operators ⊞ and ⊟, and an open neighborhood V of zero. (Hertzberg et al., 2013) `ev:asserted` p. 6 ^hertzberg2013integrating-019
- The axioms require x⊞0 = x, x⊞(y⊟x) = y for all y, and (x⊞δ)⊟x = δ for δ in V. (Hertzberg et al., 2013) `ev:asserted` p. 6 ^hertzberg2013integrating-020
- A fourth axiom requires the distance between x⊞δ1 and x⊞δ2 to be at most the norm of δ1 minus δ2. (Hertzberg et al., 2013) `ev:asserted` p. 6 ^hertzberg2013integrating-021
- The ⊞-manifold definition does not require x⊞δ or y⊟x to be smooth in the reference state x. (Hertzberg et al., 2013) `ev:asserted` p. 7 ^hertzberg2013integrating-022
- Gaussians on ⊞-manifolds are defined as N(µ, Σ) := µ ⊞ N(0, Σ), with µ a manifold element and Σ an ordinary matrix. (Hertzberg et al., 2013) `ev:asserted` p. 7 ^hertzberg2013integrating-023
- The expected value on a ⊞-manifold is defined as the state minimizing the expected squared ⊟-distance to the random variable. (Hertzberg et al., 2013) `ev:asserted` p. 7 ^hertzberg2013integrating-024
- The expected value can be computed iteratively as µk+1 = µk ⊞ E(X ⊟ µk), starting from a sufficiently close initial guess. (Hertzberg et al., 2013) `ev:cited` p. 7 ^hertzberg2013integrating-025
- The covariance of a ⊞-manifold distribution is defined as the expectation of the outer product of X⊟E X with itself. (Hertzberg et al., 2013) `ev:asserted` p. 8 ^hertzberg2013integrating-026
- The ⊟ operator induces a metric d(x, y) = ‖y⊟x‖, which for the INS orientation is the angle between two orientations. (Hertzberg et al., 2013) `ev:computed` p. 8 ^hertzberg2013integrating-027
- The covariance of a ⊞-manifold Gaussian N(µ, Σ) is slightly smaller than Σ, which can be practically ignored when Σ is small. (Hertzberg et al., 2013) `ev:asserted` p. 8 ^hertzberg2013integrating-028
- For planar rotations stored as angles modulo 2π, the ⊟ operator normalizes the angle difference to the interval [−π, π). (Hertzberg et al., 2013) `ev:asserted` p. 9 ^hertzberg2013integrating-029
- For 3D rotation matrices, x⊞δ = x exp δ via the Rodriguez formula, with unique parametrization for angles below π. (Hertzberg et al., 2013) `ev:asserted` p. 9 ^hertzberg2013integrating-030
- The unit quaternion ⊞ uses q·exp(δ/2), with the factor 2 making the induced metric the angle between two orientations. (Hertzberg et al., 2013) `ev:asserted` p. 9 ^hertzberg2013integrating-031
- Adapting Gauss-Newton to ⊞-manifolds needs only small changes: perturbations are added with ⊞ and measurement-space values are compared with ⊟. (Hertzberg et al., 2013) `ev:asserted` p. 10 ^hertzberg2013integrating-032
- The manifold UKF mean update cannot be a simple ⊞ application, since the covariance would remain expressed relative to the old mean. (Hertzberg et al., 2013) `ev:asserted` p. 13 ^hertzberg2013integrating-033
- Sigma point propagation fails for standard deviations larger than the range V, so the standard deviation must stay within V/2. (Hertzberg et al., 2013) `ev:asserted` p. 13 ^hertzberg2013integrating-034
- For 2D and 3D orientation, an angular standard deviation of π/2 is allowed, which the authors call no practical limitation. (Hertzberg et al., 2013) `ev:asserted` p. 13 ^hertzberg2013integrating-035
- MTK, the Manifold Toolkit, is implemented in C++ using the Boost Preprocessor library and the Eigen matrix library. (Hertzberg et al., 2013) `ev:reported` p. 14 ^hertzberg2013integrating-036
- In MTK, each manifold class must provide a DOF enum plus boxplus and boxminus methods as its common interface. (Hertzberg et al., 2013) `ev:reported` p. 14 ^hertzberg2013integrating-037
- MTK provides a preprocessor macro that generates a compound manifold class with named members from a list of simple manifolds. (Hertzberg et al., 2013) `ev:reported` p. 14 ^hertzberg2013integrating-038
- SLoM, a sparse least squares framework built on MTK, automatically infers which measurement depends on which variables and exploits this sparsity. (Hertzberg et al., 2013) `ev:reported` p. 15 ^hertzberg2013integrating-039
- Using MTK and UKFoM, a minimalistic but working INS-GPS filter is implemented in about 50 lines of C++ code. (Hertzberg et al., 2013) `ev:reported` p. 15 ^hertzberg2013integrating-040
- The synthetic dataset uses 100 Hz accelerometer and gyroscope readings and 4 Hz GPS with white noise of σp = 0.75 m. (Hertzberg et al., 2013) `ev:reported` p. 17 ^hertzberg2013integrating-041
- Over 50 Monte Carlo runs, the ⊞-method INS-GPS filter reached time-averaged errors of 0.415 m, 1.58 × 10−2 rad and 0.141 m/s. (Hertzberg et al., 2013) `ev:measured` p. 17 ^hertzberg2013integrating-042
- The filter's NEES and NMEE largely remain within their 95% probability regions, as expected for a consistent filter. (Hertzberg et al., 2013) `ev:measured` p. 17 ^hertzberg2013integrating-043
- UKFs using Euler angles or scaled axis orientation fail once the orientation approaches singularity, in this synthetic INS-GPS experiment. (Hertzberg et al., 2013) `ev:measured` p. 18 ^hertzberg2013integrating-044
- The ⊞-method is very slightly better than a plain quaternion UKF, a difference the authors call not very relevant. (Hertzberg et al., 2013) `ev:measured` p. 18 ^hertzberg2013integrating-045
- The authors claim the ⊞-method is conceptually more elegant rather than substantially better performing than the plain quaternion approach. (Hertzberg et al., 2013) `ev:asserted` p. 18 ^hertzberg2013integrating-046
- Computation time per predict step was 21 µs for the ⊞-method versus 28 µs for Euler angles on an Intel Xeon E5420. (Hertzberg et al., 2013) `ev:measured` p. 18 ^hertzberg2013integrating-047
- A GPS update took 32 µs with the ⊞-method, compared with 23 µs for Euler angles or scaled axis. (Hertzberg et al., 2013) `ev:measured` p. 18 ^hertzberg2013integrating-048
- The Euler-angle UKF operates normally until t = 60 s, when approaching the singularity makes it inconsistent. (Hertzberg et al., 2013) `ev:measured` p. 18 ^hertzberg2013integrating-049
- The scaled axis UKF becomes inconsistent at t = 80 s near the singularity but recovers in the end. (Hertzberg et al., 2013) `ev:measured` p. 19 ^hertzberg2013integrating-050
- The plain quaternion UKF reached time-averaged errors of 0.434 m, 1.71 × 10−2 rad and 0.160 m/s over 50 Monte Carlo runs. (Hertzberg et al., 2013) `ev:measured` p. 19 ^hertzberg2013integrating-051
- The plain quaternion UKF NEES is slightly too low by about 1, probably from process noise assigned to the quaternion norm. (Hertzberg et al., 2013) `ev:measured` p. 19 ^hertzberg2013integrating-052
- For pose graph Gauss-Newton, the four-dimensional quaternion fails due to rank deficiency, so the pseudo measurement |q| = 1 was added. (Hertzberg et al., 2013) `ev:reported` p. 19 ^hertzberg2013integrating-053
- On the Stanford parking garage dataset, Gauss-Newton with Euler angles is clearly inferior to all other representations but still converges. (Hertzberg et al., 2013) `ev:measured` p. 20 ^hertzberg2013integrating-054
- The sphere400 dataset consists of 400 three-dimensional poses and about 780 noisy constraints generated by a virtual robot on a sphere. (Hertzberg et al., 2013) `ev:reported` p. 21 ^hertzberg2013integrating-055
- On sphere400 with added noise, the ⊞-method clearly outperforms the singular Euler-angle and matrix exponential representations. (Hertzberg et al., 2013) `ev:measured` p. 21 ^hertzberg2013integrating-056
- At the highest noise level of 0.1 rad/m, the quaternion representation is slightly better than the ⊞-method per iteration. (Hertzberg et al., 2013) `ev:measured` p. 21 ^hertzberg2013integrating-057
- Computation time per step was 63 ms for the 4D quaternion and 42 ms for the ⊞-approach on sphere400. (Hertzberg et al., 2013) `ev:measured` p. 21 ^hertzberg2013integrating-058
- Euler angle and matrix exponential steps took 80 ms and 62 ms, probably due to code that was not hand-tuned. (Hertzberg et al., 2013) `ev:measured` p. 21 ^hertzberg2013integrating-059
- The authors conjecture that axiom (11d) holds for SO(n) in general, having proved it for n = 2 and n = 3. (Hertzberg et al., 2013) `ev:asserted` p. 25 ^hertzberg2013integrating-060
- The popular stereographic projection cannot be extended to a ⊞-manifold, because it violates Axiom (11b). (Hertzberg et al., 2013) `ev:computed` p. 26 ^hertzberg2013integrating-061
- The SPmap representation is continuous in both pose and perturbation vector, which the ⊞ axiomatization cannot achieve. (Hertzberg et al., 2013) `ev:asserted` p. 30 ^hertzberg2013integrating-062
- The authors' stated contribution over SPmap is an axiomatized, more general view not limited to quotients of SE(3). (Hertzberg et al., 2013) `ev:asserted` p. 30 ^hertzberg2013integrating-063

## 🎯 Contributions

## 📖 Glossary

- **⊞ (boxplus)** — Operator adding a small vector perturbation δ in R^n to a manifold state.
- **⊟ (boxminus)** — Operator returning the vector perturbation that maps one manifold state onto another.
- **⊞-manifold** — Manifold subset of R^s with ⊞, ⊟ and neighborhood V satisfying four axioms.
- **Manifold** — Space locally homeomorphic to R^n but with a more complex global topology.
- **SO(3)** — The group of 3D rotations, representable as orthonormal matrices or unit quaternions.
- **Unscented Kalman Filter (UKF)** — Derivative-free Kalman filter propagating deterministically chosen sigma points through nonlinear models.
- **Sigma points** — Deterministic samples on the 1σ contour approximating a Gaussian in the UKF.
- **NEES** — Normalized estimation error squared, a filter consistency statistic.
- **MTK** — Manifold Toolkit, C++ library generating compound ⊞-manifold classes from primitives.
- **SLoM** — Sparse Least Squares on Manifolds, generic optimizer built on MTK.
- **UKFoM** — Generic Unscented Kalman Filter on manifolds implementation built on MTK.
- **Gimbal lock** — Singularity where small orientation changes need very large parameter changes.

## ❓ Open questions

- Does axiom (11d) hold for SO(n) with V = Bπ(0) for every n, beyond the proven cases n = 2 and n = 3?
- Is there a general result establishing the 1-Lipschitz axiom for arbitrary connected Lie groups with the exponential-map construction?
- What is the induced metric of the ⊞-structure on projective spaces P^n?
- How can the axiomatization allow different representatives of the same equivalence class to define different ⊞ coordinate systems, as SPmap does?
- How large is the practical effect of the slight covariance inconsistency of ⊞-manifold Gaussians when Σ is not small relative to V?

## 📝 Notes on reading

- Version read: arXiv v1 (1107.1119v1, dated 6 Jul 2011, cs.RO); the packet year 2013 corresponds to a later published version, which may differ.
- Figures 4 to 14 are plots (trajectories, RMS error norms, NEES/NMEE curves, residual sum of squares over iterations) whose axis values are garbled in the extraction; only the numbers stated in captions and text were claimed.
- Figure 14 caption: for noise levels 0.01 and 0.1 rad/m the median of 31 runs is plotted, and curves ending early mean more than half the optimizations hit a singularity; per-representation iteration counts are not readable.
- Equations (26), (27), (30), (31), (106), (112) and (114) are partly garbled in the extraction; their content was only paraphrased at the level of the surrounding text.
- Section 6.1.4 states per-step timings as pairs (predict/GPS update): 21/32 µs (⊞), 28/23 µs (Euler), 25/23 µs (scaled axis), 21/33 µs (quaternion); the ⊞-method is not the fastest for the GPS update.
- The code listing for the colored-noise measurement model returns s.pos+s.bias although the state member is declared as gps_bias, a minor inconsistency in the paper.
- Figure 10 (colored noise, σ2b = 5m, T = 1800s) shows the ⊞-method filter consistent with a growing position error, which the caption attributes to bias drift.

## Suggested new concepts

- Boxplus method (⊞/⊟ encapsulation) — a general pattern for running vector-space estimators on manifold states, reused across SLAM and filtering literature.
- Error-state / manifold Kalman filtering — the UKF-on-manifolds construction relates to error-state filters used in IMU fusion and deserves a comparative note.
- Orientation representations (Euler angles, scaled axis, quaternions, rotation matrices) — trade-offs in singularities and normalization recur across robotics estimation papers.
- Filter consistency metrics (NEES, NMEE) — standard tools for validating estimator uncertainty that other notes can link to.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Operadores $\boxplus/\boxminus$ que encapsulan la variedad para algoritmos genéricos.

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
