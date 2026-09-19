---
aliases: []
type: "source"
title: "Coriolis Factorizations and their Connections to Riemannian Geometry"
citekey: "Wensing2023coriolis"
doi: "10.48550/arXiv.2312.14425"
arxiv: "2312.14425"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2312.14425"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Patrick M. Wensing", "Jean-Jacques E. Slotine"]
sha256: ["c11b6bab4c2698c408c9e4ea9ce4b9a8ee202cb541dcd6039ad63a6b71ae4f58"]
pdf: "Content/Papers/Wensing2023coriolis.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Wensing2023coriolis.pdf]]

> [!abstract] One-sentence summary
> The paper links each Coriolis factorization to an affine connection, shows the Christoffel-consistent choice is the torsion-free one that avoids trajectory twisting in passivity-based control, and gives recursive algorithms to compute it for open- and closed-chain robots such as humanoids and quadrupeds.

## Abstract

Many energy-based control strategies for mechanical systems require the choice of a Coriolis factorization satisfying a skew-symmetry property. This paper (a) explores if and when a control designer has flexibility in this choice, (b) develops a canonical choice related to the Christoffel symbols, and (c) describes how to efficiently perform control computations with it for constrained mechanical systems. We link the choice of a Coriolis factorization to the notion of an affine connection on the configuration manifold and show how properties of the connection relate with the associated factorization. In particular, the factorization based on the Christoffel symbols is linked with a torsion-free property that can limit the twisting of system trajectories during passivity-based control. We then develop a way to induce Coriolis factorizations for constrained mechanisms from unconstrained ones, which provides a pathway to use the theory for efficient control computations with high-dimensional systems such as humanoids and quadruped robots with open- and closed-chain mechanisms. A collection of algorithms is provided (and made available open source) to support the recursive computation of passivity-based control laws, adaptation laws, and regressor matrices in future applications. (arXiv)

## 🧠 Key ideas (atomic)

- The Coriolis and centripetal terms, which depend quadratically on velocity, can be factored into a Coriolis matrix that is linear in velocity. (Wensing & Slotine, 2023) `ev:asserted` p. 1 ^wensing2023coriolis-001
- Many Coriolis factorizations of the same Coriolis and centripetal terms are possible, as a two-dimensional example from prior work illustrates. (Wensing & Slotine, 2023) `ev:cited` p. 1 ^wensing2023coriolis-002
- In passivity-based control applications, the Coriolis matrix is often additionally required to make the mass-matrix derivative minus twice the Coriolis matrix skew-symmetric. (Wensing & Slotine, 2023) `ev:asserted` p. 1 ^wensing2023coriolis-003
- Earlier works often used the Christoffel-symbol factorization, with some suggesting it is unique in satisfying the factorization and skew-symmetry conditions. (Wensing & Slotine, 2023) `ev:cited` p. 1 ^wensing2023coriolis-004
- For a point mass in three dimensions, any scalar function times the velocity cross-product matrix gives a valid skew-symmetric Coriolis factorization. (Wensing & Slotine, 2023) `ev:computed` p. 2 ^wensing2023coriolis-005
- The canonical Christoffel factorization generalizes to non-coordinate basis vector fields through the Riemannian connection, ensuring a torsion-free property. (Wensing & Slotine, 2023) `ev:asserted` p. 2 ^wensing2023coriolis-006
- The results give broader theoretical backing to a previous Coriolis matrix algorithm, which is shown to apply to systems with local kinematic loops. (Wensing & Slotine, 2023) `ev:asserted` p. 2 ^wensing2023coriolis-007
- [[Recursive Newton-Euler algorithm|Recursive Newton-Euler methods]] for computing the dynamics first appeared in the late 1970s, motivated by dynamic analysis of walking machines. (Wensing & Slotine, 2023) `ev:cited` p. 2 ^wensing2023coriolis-008
- Computed-torque control laws require evaluating the Coriolis terms, which [[Recursive Newton-Euler algorithm|recursive Newton-Euler methods]] can accomplish in O(n) complexity. (Wensing & Slotine, 2023) `ev:cited` p. 2 ^wensing2023coriolis-009
- In many passivity-based control developments, satisfying the skew-symmetry property of the Coriolis matrix plays a critical role in Lyapunov arguments. (Wensing & Slotine, 2023) `ev:cited` p. 2 ^wensing2023coriolis-010
- Niemeyer's [[Recursive Newton-Euler algorithm|recursive Newton-Euler variant]] was the first compatible with the Christoffel-consistent factorization, for systems with revolute and prismatic joints. (Wensing & Slotine, 2023) `ev:cited` p. 2 ^wensing2023coriolis-011
- The authors show in hindsight that Niemeyer's method was Christoffel-consistent for a broader class of mechanisms than originally claimed. (Wensing & Slotine, 2023) `ev:asserted` p. 2 ^wensing2023coriolis-012
- In contact detection, freedom in choosing the Coriolis matrix is moot, since its transposed product with velocity is identical for any skew-symmetric factorization. (Wensing & Slotine, 2023) `ev:asserted` p. 2 ^wensing2023coriolis-013
- A closely related variant of an earlier Coriolis matrix algorithm was independently developed in the Pinocchio C/C++ dynamics package. (Wensing & Slotine, 2023) `ev:cited` p. 2 ^wensing2023coriolis-014
- The authors state that symbolic calculation of the Christoffel symbols is not tractable for high-degree-of-freedom mechanical systems. (Wensing & Slotine, 2023) `ev:asserted` p. 4 ^wensing2023coriolis-015
- Available numerical algorithms compute Christoffel symbols for restricted mechanism classes, such as prismatic and revolute joints, but not for systems with closed kinematic loops. (Wensing & Slotine, 2023) `ev:cited` p. 4 ^wensing2023coriolis-016
- Humanoid and quadruped robots are frequently modeled with a 6-DoF free joint described by generalized velocities to avoid Euler-angle representation singularities. (Wensing & Slotine, 2023) `ev:asserted` p. 4 ^wensing2023coriolis-017
- Geodesics of an arbitrary affine connection need not be extremal-length curves of the kinetic-energy metric, unlike geodesics of the Riemannian connection. (Wensing & Slotine, 2023) `ev:asserted` p. 4 ^wensing2023coriolis-018
- A connection is compatible with the metric if and only if its contorsion tensor is anti-symmetric in its first and third arguments. (Wensing & Slotine, 2023) `ev:cited` p. 5 ^wensing2023coriolis-019
- On a Riemannian manifold, the Riemannian connection is the unique affine connection that is both metric-compatible and torsion-free. (Wensing & Slotine, 2023) `ev:cited` p. 5 ^wensing2023coriolis-020
- A connection gives the same geodesics as the Riemannian connection if and only if its contorsion tensor is anti-symmetric in its second and third arguments. (Wensing & Slotine, 2023) `ev:computed` p. 5 ^wensing2023coriolis-021
- Among all connections with Riemannian geodesics, the Riemannian connection is the only one that is torsion-free. (Wensing & Slotine, 2023) `ev:computed` p. 5 ^wensing2023coriolis-022
- For non-coordinate basis fields, the generalized Christoffel symbols equal their symmetrized part plus half a structure-constant term. (Wensing & Slotine, 2023) `ev:computed` p. 5 ^wensing2023coriolis-023
- A connection is metric-compatible with Riemannian geodesics if and only if its contorsion tensor is totally anti-symmetric in every pair of arguments. (Wensing & Slotine, 2023) `ev:computed` p. 6 ^wensing2023coriolis-024
- The proof of uniqueness in low dimensions rests on the absence of three-forms on manifolds of dimension one or two. (Wensing & Slotine, 2023) `ev:computed` p. 6 ^wensing2023coriolis-025
- A connection is metric-compatible if and only if its associated Coriolis matrix makes the mass-matrix derivative minus twice it skew-symmetric. (Wensing & Slotine, 2023) `ev:computed` p. 6 ^wensing2023coriolis-026
- A connection gives the Riemannian geodesics if and only if its Coriolis matrix produces the same Coriolis terms as the Christoffel-based factorization. (Wensing & Slotine, 2023) `ev:computed` p. 7 ^wensing2023coriolis-027
- A skew-symmetric Coriolis factorization giving the correct dynamics is unique for systems with one or two degrees of freedom. (Wensing & Slotine, 2023) `ev:computed` p. 7 ^wensing2023coriolis-028
- For systems with three or more degrees of freedom, there are infinitely many skew-symmetric Coriolis factorizations that give the correct dynamics. (Wensing & Slotine, 2023) `ev:computed` p. 7 ^wensing2023coriolis-029
- The passivity-based tracking analysis uses the Slotine-Li controller, built on a sliding variable equal to velocity minus reference velocity. (Wensing & Slotine, 2023) `ev:reported` p. 7 ^wensing2023coriolis-030
- The point-mass tracking example used an estimated mass of 0.9 kg against a true mass of 1 kg. (Wensing & Slotine, 2023) `ev:reported` p. 8 ^wensing2023coriolis-031
- The desired point-mass trajectory was a straight line traversed with time-varying velocity along a single Cartesian axis. (Wensing & Slotine, 2023) `ev:reported` p. 8 ^wensing2023coriolis-032
- With the torsion-free zero Coriolis matrix, the point-mass trajectory converged to near-zero error, not exactly zero due to model mismatch. (Wensing & Slotine, 2023) `ev:computed` p. 8 ^wensing2023coriolis-033
- The factorization of minus five times the velocity cross-product matrix produced higher-frequency trajectories than the torsion-free factorization. (Wensing & Slotine, 2023) `ev:computed` p. 8 ^wensing2023coriolis-034
- The authors judge the torsional trajectory's higher-frequency content comparatively undesirable for deployment on a physical system. (Wensing & Slotine, 2023) `ev:asserted` p. 8 ^wensing2023coriolis-035
- More extreme factorizations, such as minus ten times the cross-product matrix, yield trajectories with even higher frequency content. (Wensing & Slotine, 2023) `ev:computed` p. 8 ^wensing2023coriolis-036
- The torsional factorization's Coriolis terms caused a counterproductive upward acceleration that sent the point mass further from the target. (Wensing & Slotine, 2023) `ev:computed` p. 8 ^wensing2023coriolis-037
- Conventional Lyapunov analysis masks the difference between the two factorizations, as the Lyapunov rate expression is independent of the Coriolis matrix choice. (Wensing & Slotine, 2023) `ev:computed` p. 8 ^wensing2023coriolis-038
- The Lyapunov function evolution was nearly identical for the torsion-free and torsional factorizations in the point-mass example. (Wensing & Slotine, 2023) `ev:computed` p. 9 ^wensing2023coriolis-039
- The induced mass matrix on a constrained submanifold equals the transposed velocity map times the full mass matrix times that map. (Wensing & Slotine, 2023) `ev:computed` p. 9 ^wensing2023coriolis-040
- Inducing a connection by projection from the Riemannian connection on the larger manifold gives the Riemannian connection on the submanifold. (Wensing & Slotine, 2023) `ev:computed` p. 9 ^wensing2023coriolis-041
- The Coriolis matrix of an induced connection equals A-transpose C A plus A-transpose H times the time derivative of A. (Wensing & Slotine, 2023) `ev:computed` p. 9 ^wensing2023coriolis-042
- Under this transformation law, skew-symmetry of the unconstrained Coriolis matrix carries over to the Coriolis matrix of the constrained system. (Wensing & Slotine, 2023) `ev:computed` p. 9 ^wensing2023coriolis-043
- Under this transformation law, a factorization giving correct dynamics on the unconstrained manifold also gives correct dynamics on the submanifold. (Wensing & Slotine, 2023) `ev:computed` p. 10 ^wensing2023coriolis-044
- Under this transformation law, the Christoffel-consistent factorization of the unconstrained system induces the Christoffel-consistent factorization of the constrained system. (Wensing & Slotine, 2023) `ev:computed` p. 10 ^wensing2023coriolis-045
- For a single rigid body using its body twist, the paper gives a closed-form Christoffel-consistent factorization built from spatial inertia and cross-product matrices. (Wensing & Slotine, 2023) `ev:computed` p. 10 ^wensing2023coriolis-046
- Stacking body Jacobians into the velocity map yields the constrained Christoffel-consistent Coriolis matrix directly from the block-diagonal maximal-coordinate one. (Wensing & Slotine, 2023) `ev:computed` p. 11 ^wensing2023coriolis-047
- The resulting open-chain formula is equivalent to one in earlier work, implying that work's algorithm computes the Christoffel-consistent matrix for any open-chain mechanism. (Wensing & Slotine, 2023) `ev:computed` p. 11 ^wensing2023coriolis-048
- The added generality does not affect the O(Nd) computational complexity of the algorithm, where d is the depth of the kinematic tree. (Wensing & Slotine, 2023) `ev:computed` p. 11 ^wensing2023coriolis-049
- Earlier theory had established Christoffel consistency of that algorithm for mechanisms comprised of revolute, prismatic, and helical joints. (Wensing & Slotine, 2023) `ev:cited` p. 11 ^wensing2023coriolis-050
- The new theory justifies that this property extends to a considerably larger class, including spherical joints, universal joints and floating bases. (Wensing & Slotine, 2023) `ev:computed` p. 11 ^wensing2023coriolis-051
- Implementations of the Christoffel-consistent Coriolis algorithm are available in MATLAB and in recent versions of the Pinocchio C/C++ package. (Wensing & Slotine, 2023) `ev:reported` p. 11 ^wensing2023coriolis-052
- For closed-chain systems, one option projects the Coriolis matrix of a spanning tree to minimal coordinates through the transformation law. (Wensing & Slotine, 2023) `ev:asserted` p. 12 ^wensing2023coriolis-053
- A second option uses constraint embedding, grouping bodies in local loop closures into clusters so that the cluster topology becomes a tree. (Wensing & Slotine, 2023) `ev:asserted` p. 12 ^wensing2023coriolis-054
- With clusters, the Christoffel-consistent Coriolis matrix takes the same form as for open chains, generalizing the earlier algorithm to clusters. (Wensing & Slotine, 2023) `ev:computed` p. 12 ^wensing2023coriolis-055
- Recursive regressor computation and many other adaptive control algorithms carry over to local loop closures modeled with constraint embedding. (Wensing & Slotine, 2023) `ev:asserted` p. 12 ^wensing2023coriolis-056
- The Christoffel-symbol algorithm is a case where recursive algorithms do not carry over directly to constraint-embedded local loop closures. (Wensing & Slotine, 2023) `ev:asserted` p. 12 ^wensing2023coriolis-057
- With generalized coordinates, the Christoffel-consistent Coriolis matrix equals half the velocity derivative of the Coriolis and centripetal terms. (Wensing & Slotine, 2023) `ev:computed` p. 13 ^wensing2023coriolis-058
- With generalized speeds, this derivative formula can break down, since the generalized Christoffel symbols are not guaranteed symmetric in their last two indices. (Wensing & Slotine, 2023) `ev:computed` p. 13 ^wensing2023coriolis-059
- The derivative-based construction with generalized speeds requires a correction term involving the structure constants of the basis vector fields. (Wensing & Slotine, 2023) `ev:computed` p. 13 ^wensing2023coriolis-060
- The derivative-based approach might be more straightforward for users with access to an efficient auto-differentiation package such as CasADi. (Wensing & Slotine, 2023) `ev:asserted` p. 13 ^wensing2023coriolis-061
- The authors conclude that torsion leads to control-output oscillations that could incite unmodeled high-frequency vibrations in mechanical systems. (Wensing & Slotine, 2023) `ev:asserted` p. 13 ^wensing2023coriolis-062
- The authors state that the O(Nd) complexity for open-chain systems promotes use of this Coriolis matrix for humanoids and quadruped robots. (Wensing & Slotine, 2023) `ev:asserted` p. 13 ^wensing2023coriolis-063
- The authors suggest the algorithms may be considered beyond passivity-based control, for example when taking covariant derivatives in other contexts. (Wensing & Slotine, 2023) `ev:asserted` p. 14 ^wensing2023coriolis-064
- The dedicated generalized Christoffel symbol algorithm has complexity linear in the number of clusters and quadratic in tree depth, for a fixed cluster library. (Wensing & Slotine, 2023) `ev:computed` p. 16 ^wensing2023coriolis-065
- Appendix B provides an O(Nc) algorithm for Slotine-Li direct adaptive control of mechanisms with constraint-embedded local loop closures. (Wensing & Slotine, 2023) `ev:asserted` p. 16 ^wensing2023coriolis-066
- Cluster-level forces in the adaptive control recursion remain linear in the inertia parameters of each body within the cluster. (Wensing & Slotine, 2023) `ev:computed` p. 16 ^wensing2023coriolis-067
- The parameter update term reduces to each cluster regressor transposed times the difference between true and reference cluster velocities. (Wensing & Slotine, 2023) `ev:computed` p. 17 ^wensing2023coriolis-068
- Regressors for generalized momentum, gravity, the transposed Coriolis product, kinetic energy and potential-energy rate are computed in one unified recursive algorithm. (Wensing & Slotine, 2023) `ev:asserted` p. 18 ^wensing2023coriolis-069

## 🎯 Contributions

## 📖 Glossary

- **Coriolis factorization** — Matrix C linear in velocity with C times velocity equal to Coriolis/centripetal terms.
- **Skew-symmetry property** — Mass-matrix derivative minus twice C is skew-symmetric; used in passivity arguments.
- **Affine connection** — Rule for differentiating vector fields along others on a manifold.
- **Riemannian (Levi-Civita) connection** — Unique metric-compatible, torsion-free connection of a Riemannian manifold.
- **Christoffel symbols** — Coefficients of the Riemannian connection in a chosen basis.
- **Contorsion tensor** — Difference between the Riemannian connection and another connection.
- **Torsion-free** — Connection whose parallel transport does not twist vectors around a curve.
- **Metric compatibility** — Parallel transport preserves inner products defined by the kinetic-energy metric.
- **Generalized speeds** — Velocity variables along non-coordinate basis vector fields, e.g. body twists.
- **Constraint embedding** — Grouping bodies in local loop closures into clusters forming a tree.
- **Slotine-Li regressor** — Matrix making passivity-based control torque linear in inertial parameters.

## ❓ Open questions

- How much does the torsion-induced high-frequency content matter on physical hardware, beyond the simulated point-mass example?
- Can the freedom among the infinitely many skew-symmetric factorizations (n of three or more) be exploited for control objectives rather than avoided?
- How can the Christoffel-symbol algorithm be made to carry over recursively to constraint-embedded loop closures as other algorithms do?
- Do the computational tools for covariant derivatives benefit geometry-based optimization, observers, or differential-flatness and controllability analyses in practice?
- How do the gains of the torsion-free factorization compare in whole-body passivity-based quadratic-programming controllers on humanoids?

## 📝 Notes on reading

- The cached text is arXiv v2 (dated 23 Apr 2025) of arXiv 2312.14425; the packet identifier is the same arXiv record.
- Page 1 carries a roadmap figure (Fig. 1) whose embedded LaTeX image data was extracted as long base64 strings; only its labels (propositions, theorems, torsion-free, same geodesics) are readable.
- Figs. 4, 5 and 7 (page 8) survive only as axis tick values; Fig. 6 (3D trajectory, torsion-free vs. with torsion) is described only in the text. No numerical error values were claimed from them.
- Complexity superscripts are garbled in extraction (e.g. the all-Christoffel-symbols cost printed as O(N 2d) on page 11, and the dedicated algorithm as O(Nd2) and O(Ncd2) on pages 11 and 16); they were paraphrased in words rather than copied.
- Algorithms 1-4 (pages 13, 16, 17, 18) are pseudocode and were summarized, not claimed line by line.
- The paper's four motivating questions (page 1) and the section on passivity-based whole-body controllers (page 2) were read but not claimed separately to stay under the claim budget.
- Minor typos in the paper: Corrolary (acknowledgements), reoganizing, Riemmannian.

## Suggested new concepts

- Christoffel-consistent Coriolis matrix — canonical skew-symmetric factorization used across passivity-based and adaptive robot control.
- Affine connection view of Coriolis factorizations — ties robot dynamics modeling choices to Riemannian geometry.
- Constraint embedding — enables recursive dynamics and adaptive-control algorithms for mechanisms with local loop closures.
- Passivity-based adaptive control (Slotine-Li) — recurring control framework whose computation this paper extends.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Relación entre elección de $C(q,\dot q)$, conexiones afines y pasividad.
