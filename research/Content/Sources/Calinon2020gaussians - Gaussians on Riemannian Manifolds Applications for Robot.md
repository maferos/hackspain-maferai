---
aliases: []
type: "source"
title: "Gaussians on Riemannian Manifolds: Applications for Robot Learning and Adaptive Control"
citekey: "Calinon2020gaussians"
doi: "10.48550/arXiv.1909.05946"
arxiv: "1909.05946"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/1909.05946"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Sylvain Calinon"]
sha256: ["486ab24354634ffc3e1e8866a2100225d8dcbcedeb1137481216d99defcddb1d"]
pdf: "Content/Papers/Calinon2020gaussians.pdf"
topics: ["[[Matemáticas]]", "[[Optimización y algoritmos]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]", "[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[Calinon2020gaussians.pdf]]

> [!abstract] One-sentence summary
> A practitioner-oriented overview showing how Gaussians defined by a manifold mean and a tangent-space covariance extend clustering, regression, fusion and MPC to non-Euclidean robot data, illustrated on sEMG prosthetic control and underwater teleoperation.

## Abstract

This article presents an overview of robot learning and adaptive control applications that can benefit from a joint use of Riemannian geometry and probabilistic representations. The roles of Riemannian manifolds, geodesics and parallel transport in robotics are first discussed. Several forms of manifolds already employed in robotics are then presented, by also listing manifolds that have been underexploited but that have potentials in future robot learning applications. A varied range of techniques employing Gaussian distributions on Riemannian manifolds is then introduced, including clustering, regression, information fusion, planning and control problems. Two examples of applications are presented, involving the control of a prosthetic hand from surface electromyography (sEMG) data, and the teleoperation of a bimanual underwater robot. Further perspectives are finally discussed, with suggestions of promising research directions. (arXiv)

## 🧠 Key ideas (atomic)

- The article surveys robot learning and adaptive control applications that can benefit from jointly using Riemannian geometry and probabilistic representations. (Calinon, 2020) `ev:asserted` p. 1 ^calinon2020gaussians-001
- Robotics data such as joint angles, rigid body motions, unit quaternions and SPD matrices have varied geometries that are sometimes underexploited. (Calinon, 2020) `ev:cited` p. 1 ^calinon2020gaussians-002
- Several robotics techniques use Riemannian geometry components without an explicit link to the framework, which can limit potential extensions. (Calinon, 2020) `ev:asserted` p. 1 ^calinon2020gaussians-003
- The author cites computing orientation errors with a logarithmic map in inverse kinematics as an implicit use of Riemannian geometry. (Calinon, 2020) `ev:asserted` p. 1 ^calinon2020gaussians-004
- The article aims to highlight links between existing techniques and to catalogue missing links that could be explored in further research. (Calinon, 2020) `ev:asserted` p. 1 ^calinon2020gaussians-005
- The author argues that Riemannian geometry offers a principled and simple way to extend algorithms developed for Euclidean data to other manifolds. (Calinon, 2020) `ev:asserted` p. 1 ^calinon2020gaussians-006
- Riemannian manifolds can recast constrained optimization problems in Euclidean space as unconstrained problems that inherently account for the data geometry. (Calinon, 2020) `ev:asserted` p. 1 ^calinon2020gaussians-007
- The paper adopts a practitioner perspective, conveying the main intuitions behind the algorithms sometimes at the expense of a more rigorous treatment. (Calinon, 2020) `ev:asserted` p. 2 ^calinon2020gaussians-008
- Didactic source codes accompany the paper in the PbDlib library, maintained as independent Matlab and C++ versions. (Calinon, 2020) `ev:reported` p. 2 ^calinon2020gaussians-009
- The Cartesian product of two Riemannian manifolds is also a Riemannian manifold, allowing joint distributions on any combination of manifolds. (Calinon, 2020) `ev:asserted` p. 2 ^calinon2020gaussians-010
- The logarithmic map is the inverse of the exponential map, which sends a tangent vector onto the geodesic starting at the base point. (Calinon, 2020) `ev:asserted` p. 2 ^calinon2020gaussians-011
- Parallel transport moves vectors between tangent spaces such that the inner product between two vectors in a tangent space is conserved. (Calinon, 2020) `ev:asserted` p. 2 ^calinon2020gaussians-012
- A covariance matrix can be parallel transported through its eigendecomposition, which for many robotics manifolds is equivalent to a linear mapping. (Calinon, 2020) `ev:asserted` p. 3 ^calinon2020gaussians-013
- The most common manifolds in robotics are homogeneous, providing simple analytic expressions for exponential and logarithmic mapping and parallel transport. (Calinon, 2020) `ev:asserted` p. 3 ^calinon2020gaussians-014
- Tracking gains defined as full SPD matrices instead of scalars let the controller take into account the coordination of different control variables. (Calinon, 2020) `ev:asserted` p. 3 ^calinon2020gaussians-015
- Sensory data in human-robot collaboration can be preprocessed with sliding windows into spatial covariances, which are SPD matrices. (Calinon, 2020) `ev:cited` p. 3 ^calinon2020gaussians-016
- Hyperbolic manifolds are currently underexploited in robotics despite potential for representing dynamical systems, Toeplitz/Hankel matrices or autoregressive models. (Calinon, 2020) `ev:cited` p. 4 ^calinon2020gaussians-017
- In hyperbolic manifolds the circumference of a circle grows exponentially with its radius, giving a convenient representation for hierarchies. (Calinon, 2020) `ev:asserted` p. 4 ^calinon2020gaussians-018
- The Grassmann manifold is largely underrepresented in robotics, although it could encode nullspaces and projection operators in a probabilistic way. (Calinon, 2020) `ev:asserted` p. 4 ^calinon2020gaussians-019
- With a smoothly varying metric, the Riemannian formulation is coordinate independent, so geodesic paths are invariant to the choice of local coordinates. (Calinon, 2020) `ev:cited` p. 4 ^calinon2020gaussians-020
- In VAEs with C2 differentiable activations, the metric J⊤J from the decoder Jacobian can replace latent linear interpolations with geodesics. (Calinon, 2020) `ev:cited` p. 4 ^calinon2020gaussians-021
- For manifolds with nonconstant curvature, the geodesic optimization problem is most often nonconvex and can be computationally heavy to solve. (Calinon, 2020) `ev:asserted` p. 4 ^calinon2020gaussians-022
- Discrete differential geometry could link discrete planners such as probabilistic roadmaps to their continuous counterparts in Riemannian geometry, the author suggests. (Calinon, 2020) `ev:asserted` p. 4 ^calinon2020gaussians-023
- Some Lie groups such as SO(3) can be endowed with a bi-invariant Riemannian metric, giving them the structure of a Riemannian manifold. (Calinon, 2020) `ev:asserted` p. 4 ^calinon2020gaussians-024
- Distinctive vocabulary and notation in the literature hinder some links between applications exploiting Riemannian geometry and those exploiting Lie theory. (Calinon, 2020) `ev:asserted` p. 4 ^calinon2020gaussians-025
- The paper represents a manifold Gaussian by a Karcher/Fréchet mean on the manifold and a covariance in the tangent space of that mean. (Calinon, 2020) `ev:reported` p. 5 ^calinon2020gaussians-026
- Distortions arise when points are too far from the mean, but the author states this distortion is negligible in most robotics applications. (Calinon, 2020) `ev:asserted` p. 5 ^calinon2020gaussians-027
- This distortion is strongly attenuated in a mixture of Gaussians, as each Gaussian models a limited region of the manifold. (Calinon, 2020) `ev:asserted` p. 5 ^calinon2020gaussians-028
- The geometric mean is computed by a Gauss-Newton iteration that averages logarithmic maps in the tangent space and updates with an exponential map. (Calinon, 2020) `ev:reported` p. 5 ^calinon2020gaussians-029
- In practice the Gauss-Newton mean estimation converges in a couple of iterations, typically less than 10 for the accuracy the applications require. (Calinon, 2020) `ev:asserted` p. 5 ^calinon2020gaussians-030
- A GMM on a manifold is estimated by Expectation-Maximization, with the Gauss-Newton mean procedure performed in the M-step. (Calinon, 2020) `ev:reported` p. 5 ^calinon2020gaussians-031
- On the S2 manifold, a GMM computed in a single tangent space at the origin introduces distortions resulting in poor modeling of the data. (Calinon, 2020) `ev:computed` p. 5 ^calinon2020gaussians-032
- Representing covariances in the tangent spaces of the means results in a much better fit than representing the GMM in a single tangent space. (Calinon, 2020) `ev:computed` p. 5 ^calinon2020gaussians-033
- Gaussian conditioning on a manifold is evaluated locally by iteration, using a covariance parallel transported to the input and current output estimate. (Calinon, 2020) `ev:reported` p. 6 ^calinon2020gaussians-034
- The product of K Gaussians on a Riemannian manifold is locally evaluated by iterating an update with covariances transported to the current mean. (Calinon, 2020) `ev:cited` p. 6 ^calinon2020gaussians-035
- MPC is described as a linear quadratic tracking problem with velocity commands and a linear system, but the approach can be generalized to other controllers. (Calinon, 2020) `ev:reported` p. 6 ^calinon2020gaussians-036
- The reference signal tracked by the controller can be represented by a GMM to form a stepwise trajectory. (Calinon, 2020) `ev:cited` p. 6 ^calinon2020gaussians-037
- MPC is extended to Riemannian manifolds by working in the tangent space of the current state, the point introducing the least distortions. (Calinon, 2020) `ev:reported` p. 6 ^calinon2020gaussians-038
- In the manifold MPC formulation, the control cost matrix R is assumed isotropic and thus does not need to be transported. (Calinon, 2020) `ev:reported` p. 6 ^calinon2020gaussians-039
- On S2, the manifold MPC computations are repeated at each time step to reproduce a movement whose reference is encoded as a GMM. (Calinon, 2020) `ev:computed` p. 7 ^calinon2020gaussians-040
- GMR computes output distributions online with a computation time independent of the number of datapoints used to train the model. (Calinon, 2020) `ev:cited` p. 7 ^calinon2020gaussians-041
- Earlier regression methods from Gaussian mixtures on Riemannian manifolds only partially exploit the manifold structure in Gaussian conditioning. (Calinon, 2020) `ev:cited` p. 7 ^calinon2020gaussians-042
- One earlier orientation GMM formulated logarithm and exponential transformations in a single tangent space at the origin instead of locally. (Calinon, 2020) `ev:cited` p. 7 ^calinon2020gaussians-043
- The paper proposes extending Gaussian mixture regression to input and/or output data lying on symmetric positive definite matrix manifolds. (Calinon, 2020) `ev:asserted` p. 7 ^calinon2020gaussians-044
- As the covariance of SPD datapoints is a 4th-order tensor, a parallel transport method exploiting their supersymmetry properties is used. (Calinon, 2020) `ev:cited` p. 7 ^calinon2020gaussians-045
- GMR on the SPD manifold is applied to predict wrist movement from spatial covariances computed from surface electromyography data. (Calinon, 2020) `ev:reported` p. 7 ^calinon2020gaussians-046
- Compared to Euclidean GMR, GMR on the SPD manifold improved the detection of wrist movement for most of the participants. (Calinon, 2020) `ev:measured` p. 7 ^calinon2020gaussians-047
- GMR on the SPD manifold proved to be efficient to detect transitions between wrist movements in the sEMG application. (Calinon, 2020) `ev:measured` p. 7 ^calinon2020gaussians-048
- For the first participant in Table I, rest RMSE was 0.29 with SPD GMR versus 0.47 with Euclidean GMR. (Calinon, 2020) `ev:measured` p. 8 ^calinon2020gaussians-049
- For the second participant in Table I, SPD GMR had higher wrist flexion RMSE than Euclidean GMR, 0.43 versus 0.35. (Calinon, 2020) `ev:measured` p. 8 ^calinon2020gaussians-050
- For the third participant in Table I, wrist supination RMSE was 0.22 with SPD GMR versus 0.42 with Euclidean GMR. (Calinon, 2020) `ev:measured` p. 8 ^calinon2020gaussians-051
- Within DexROV, TP-GMM is used with the manifold MPC to teleoperate an underwater robot by a teleoperator wearing an exoskeleton. (Calinon, 2020) `ev:reported` p. 8 ^calinon2020gaussians-052
- Because of long communication delays, locations of objects or tools of interest differ between the teleoperator side and the robot side. (Calinon, 2020) `ev:asserted` p. 8 ^calinon2020gaussians-053
- Motions relative to the robot and a valve are encoded as GMMs in two coordinate systems, then fused through products of Gaussians. (Calinon, 2020) `ev:reported` p. 8 ^calinon2020gaussians-054
- Using a Riemannian manifold framework, endeffector orientations on S3 are encoded uniquely in a representation that does not contain singularities. (Calinon, 2020) `ev:asserted` p. 8 ^calinon2020gaussians-055
- The approach was tested in field trials offshore of Marseille, with 7 extended dives performed in 4 different sites. (Calinon, 2020) `ev:reported` p. 8 ^calinon2020gaussians-056
- The dives covered 8m, 30m, 48m and 100m water depths, with the robot connected via satellite to a Brussels teleoperation center. (Calinon, 2020) `ev:reported` p. 8 ^calinon2020gaussians-057
- The article concludes that many robot learning and adaptive control challenges can be recast as statistical modeling and information fusion on Riemannian manifolds. (Calinon, 2020) `ev:asserted` p. 8 ^calinon2020gaussians-058
- The author flags performing all computations in a single tangent space, instead of the closest tangent spaces, as a potential misuse. (Calinon, 2020) `ev:asserted` p. 8 ^calinon2020gaussians-059
- For domain adaptation, sensory data from different subjects or days should use parallel transport instead of only recentering the data. (Calinon, 2020) `ev:cited` p. 9 ^calinon2020gaussians-060
- Grassmann manifolds seem particularly promising for robotics problems with high dimensional datapoints and only few training data. (Calinon, 2020) `ev:asserted` p. 9 ^calinon2020gaussians-061
- Grassmann manifolds are also promising for hierarchical problems such as inverse kinematics of redundant robots, providing a geometric interpretation of nullspaces. (Calinon, 2020) `ev:asserted` p. 9 ^calinon2020gaussians-062
- The author suggests a wide range of metric learning problems in robotics could benefit from a Riemannian geometry treatment. (Calinon, 2020) `ev:asserted` p. 9 ^calinon2020gaussians-063
- The supplementary material gives exponential maps, logarithmic maps and parallel transport for sphere, hyperbolic, SPD and Grassmann manifolds. (Calinon, 2020) `ev:reported` p. 11 ^calinon2020gaussians-064

## 🎯 Contributions

## 📖 Glossary

- **Riemannian manifold** — Smooth manifold with a positive definite metric tensor defining lengths and angles.
- **Tangent space** — Local Euclidean linearization of the manifold at a point.
- **Exponential map** — Maps a tangent vector to the manifold along the corresponding geodesic.
- **Logarithmic map** — Inverse of the exponential map, from manifold point to tangent vector.
- **Geodesic** — Minimum-length curve between two points on a Riemannian manifold.
- **Parallel transport** — Moves vectors between tangent spaces while preserving inner products.
- **Karcher/Fréchet mean** — Point minimizing summed squared geodesic distances to the data.
- **SPD manifold** — Manifold of symmetric positive definite matrices, e.g. covariances or stiffness.
- **Grassmann manifold** — Manifold of all p-dimensional linear subspaces of a d-dimensional space.
- **GMR** — Gaussian mixture regression: conditioning a joint-density GMM to predict outputs.
- **TP-GMM** — Task-parameterized GMM encoding motion in several frames, fused by Gaussian products.
- **LQT** — Linear quadratic tracking: quadratic-cost control tracking a reference with precision matrices.

## ❓ Open questions

- How large are the tangent-space distortions of the manifold Gaussian when data spread far from the mean, and when do they stop being negligible?
- How can geodesic computation on manifolds with nonconstant curvature be made fast enough for online robot control?
- Can hyperbolic manifolds give a useful probabilistic treatment of planning trees such as RRT or of other hierarchical structures?
- Can Grassmann manifolds provide probabilistic encodings of nullspaces and projection operators for redundant robots?
- Why did the SPD GMR give higher error than Euclidean GMR for some motions of the second participant in Table I?
- How do the manifold MPC and fusion methods extend to nonlinear systems and non-isotropic control costs?

## 📝 Notes on reading

- Version read: arXiv 1909.05946v4 (30 Mar 2020), matching the packet identifier.
- This is an overview paper: the sEMG and underwater results are summaries of earlier work ([5] and [41]); the paper reports no new quantitative experiment beyond Table I, which is taken from [5].
- Table I: the extraction lists six rows alternating SPD and Euclidean (R) without participant labels; the participant order (first, second, third) is inferred from row order. Most rows show SPD GMR lower than Euclidean GMR, but for the second participant SPD is higher for wrist extension (0.36 vs 0.35) and flexion (0.43 vs 0.35) and carries larger standard deviations, consistent with the text saying 'most of the participants'.
- Figures 1 to 9 (clustering, fusion, tracking, MPC on S2, GMM in single vs local tangent spaces, GMR on SPD, TP-GMM for DexROV) are described only qualitatively.
- Equations for Gaussian conditioning, product of Gaussians, MPC (eqs. 1 to 3) and the supplementary maps (eqs. 4 to 21) are partly garbled by extraction and were not claimed in detail.
- Equation 3 in the extracted text writes the state update with a Log map where an Exp map would be expected; this may be an extraction or typesetting issue.

## Suggested new concepts

- Riemannian Gaussian (tangent-space covariance) — the core representation reused across clustering, regression, fusion and control.
- Parallel transport of covariances — needed whenever Gaussians defined at different points are combined.
- Gaussian mixture regression on SPD manifolds — regression with covariance-valued inputs or outputs, e.g. sEMG spatial covariances.
- Model predictive control on Riemannian manifolds — tracking GMM references on orientation or SPD states.
- Task-parameterized GMM — multi-frame motion encoding fused by products of Gaussians.
- Hyperbolic embeddings for robot planning — flagged by the author as an underexploited direction.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Gaussianas, geodésicas y transporte paralelo en variedades para aprendizaje robótico.
- **[[02_optimizacion_y_algoritmos]]** — GMM/GMR/LQR en variedades (C.4).
