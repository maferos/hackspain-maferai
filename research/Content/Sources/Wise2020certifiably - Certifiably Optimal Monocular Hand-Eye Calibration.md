---
aliases: []
type: "source"
title: "Certifiably Optimal Monocular Hand-Eye Calibration"
citekey: "Wise2020certifiably"
doi: "10.48550/arXiv.2005.08298"
arxiv: "2005.08298"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2005.08298"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Emmett Wise", "Matthew Giamou", "Soroush Khoubyarian", "Abhinav Grover", "Jonathan Kelly"]
sha256: ["5cc86e76b133c9a659f14708f8595df59b0624e736b2cd0a982b8a8bc48b499e"]
pdf: "Content/Papers/Wise2020certifiably.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 55
---

📄 PDF: [[Wise2020certifiably.pdf]]

> [!abstract] One-sentence summary
> The paper extends a convex SDP relaxation of AX = XB hand-eye calibration to a monocular camera with unknown translation scale, proves the relaxation stays tight under bounded noise, and shows on synthetic data that it certifies global optima in about two seconds and beats a linear baseline as noise grows.

## Abstract

Correct fusion of data from two sensors is not possible without an accurate estimate of their relative pose, which can be determined through the process of extrinsic calibration. When two or more sensors are capable of producing their own egomotion estimates (i.e., measurements of their trajectories through an environment), the 'hand-eye' formulation of extrinsic calibration can be employed. In this paper, we extend our recent work on a convex optimization approach for hand-eye calibration to the case where one of the sensors cannot observe the scale of its translational motion (e.g., a monocular camera observing an unmapped environment). We prove that our technique is able to provide a certifiably globally optimal solution to both the known- and unknown-scale variants of hand-eye calibration, provided that the measurement noise is bounded. Herein, we focus on the theoretical aspects of the problem, show the tightness and stability of our solution, and demonstrate the optimality and speed of our algorithm through experiments with synthetic data. (arXiv)

## 🧠 Key ideas (atomic)

- The paper extends a [[Hand-eye calibration (AX = XB)|certifiably optimal hand-eye calibration method]] to the case where one sensor cannot observe its translational scale. (Wise et al., 2020) `ev:asserted` p. 1 ^wise2020certifiably-001
- The unknown-scale case permits the method to be used with sensor pairs that include a monocular camera observing an unmapped environment. (Wise et al., 2020) `ev:asserted` p. 1 ^wise2020certifiably-002
- The problem formulation requires only that the scene contain sufficient geometric features for each sensor to produce an egomotion estimate. (Wise et al., 2020) `ev:asserted` p. 1 ^wise2020certifiably-003
- The authors state that robot operation inevitably causes unintentional changes to the extrinsic transformation through thermal expansion, metal fatigue or collisions. (Wise et al., 2020) `ev:asserted` p. 1 ^wise2020certifiably-004
- The common [[Hand-eye calibration (AX = XB)|AX = XB hand-eye formulation]] can be applied to any egomotion-capable sensor, including stereo cameras, 3D lidar units and GNSS-INS devices. (Wise et al., 2020) `ev:cited` p. 1 ^wise2020certifiably-005
- The authors prove that the SDP relaxation of the [[Hand-eye calibration (AX = XB)|hand-eye calibration QCQP]] is guaranteed to be tight when measurement noise is bounded. (Wise et al., 2020) `ev:computed` p. 1 ^wise2020certifiably-006
- The authors describe their proof of global optimality in the presence of noise as the first of its kind for hand-eye calibration. (Wise et al., 2020) `ev:asserted` p. 2 ^wise2020certifiably-007
- An open source Python implementation of the algorithm and experiments is released on GitHub under utiasSTARS/certifiable-calibration. (Wise et al., 2020) `ev:reported` p. 2 ^wise2020certifiably-008
- An earlier experimental investigation concluded that coupled nonlinear optimization gives more accurate [[Hand-eye calibration (AX = XB)|hand-eye solutions]] under noise than decoupled closed-form methods. (Wise et al., 2020) `ev:cited` p. 2 ^wise2020certifiably-009
- A prior study of the unknown scale case proposed a second-order cone programming solution without any optimality guarantees. (Wise et al., 2020) `ev:cited` p. 2 ^wise2020certifiably-010
- The method eschews a probabilistic cost function in favour of the simplicity of a classic geometric hand-eye formulation. (Wise et al., 2020) `ev:asserted` p. 2 ^wise2020certifiably-011
- The authors state that the method advances the state of the art by including the monocular camera case with analytic global optimality guarantees. (Wise et al., 2020) `ev:asserted` p. 2 ^wise2020certifiably-012
- Convex SDP relaxations have been applied to rotation averaging, SLAM, registration, relative pose estimation and hand-eye calibration. (Wise et al., 2020) `ev:cited` p. 2 ^wise2020certifiably-013
- The rotation group SO(3) can be described entirely through quadratic orthogonality and cyclic cross-product constraints on a 3×3 matrix. (Wise et al., 2020) `ev:cited` p. 2 ^wise2020certifiably-014
- Monocular camera egomotion is modelled as a rotation plus a translation multiplied by an unknown, unobservable scaling factor α. (Wise et al., 2020) `ev:asserted` p. 3 ^wise2020certifiably-015
- Calibration is posed as a QCQP minimizing the summed squared Frobenius norms of AX = XB error matrices over T time steps. (Wise et al., 2020) `ev:asserted` p. 3 ^wise2020certifiably-016
- Given an optimal rotation, the translation and scale are recovered in closed form by solving a linear system from the cost matrix. (Wise et al., 2020) `ev:computed` p. 3 ^wise2020certifiably-017
- A Schur complement reduces the cost matrix to a rotation-only problem that excludes the translation and scale variables. (Wise et al., 2020) `ev:computed` p. 3 ^wise2020certifiably-018
- Homogenizing the SO(3) constraints with a scalar variable yields a set of 22 homogeneous quadratic equality constraints. (Wise et al., 2020) `ev:computed` p. 3 ^wise2020certifiably-019
- The Lagrangian dual of the reduced problem is an SDP that can be efficiently solved with any generic interior-point solver. (Wise et al., 2020) `ev:computed` p. 4 ^wise2020certifiably-020
- The primal rotation is recovered from the nullspace of the positive semidefinite dual matrix Z at the optimal dual parameters. (Wise et al., 2020) `ev:computed` p. 4 ^wise2020certifiably-021
- A zero duality gap between primal and dual costs for a candidate solution pair serves as a post-hoc certificate of global optimality. (Wise et al., 2020) `ev:asserted` p. 4 ^wise2020certifiably-022
- The tightness proofs use an orthogonal relaxation over O(3), which allows reflections in addition to rotations. (Wise et al., 2020) `ev:asserted` p. 4 ^wise2020certifiably-023
- Proposition 1 shows that any noise-free instance of the orthogonal relaxation exhibits strong duality, with a zero duality gap. (Wise et al., 2020) `ev:computed` p. 4 ^wise2020certifiably-024
- Corollary 1 extends noise-free strong duality to the known-scale case and to any formulation with redundant constraints. (Wise et al., 2020) `ev:computed` p. 5 ^wise2020certifiably-025
- Lemma 1's condition of platform rotation about two distinct axes is a common observability criterion in similar extrinsic calibration formulations. (Wise et al., 2020) `ev:cited` p. 5 ^wise2020certifiably-026
- Lemma 1 proves the noise-free known-scale cost is strictly convex given rotations about two unique axes and a translation span condition. (Wise et al., 2020) `ev:computed` p. 5 ^wise2020certifiably-027
- Theorem 1 proves that strong duality holds for known-scale measurements within some positive bound of a noise-free instance satisfying Lemma 1. (Wise et al., 2020) `ev:computed` p. 5 ^wise2020certifiably-028
- Theorem 2 extends the stability property of Theorem 1 to the unknown-scale case by showing the Lagrangian Hessian is corank-one. (Wise et al., 2020) `ev:computed` p. 6 ^wise2020certifiably-029
- The authors leave the exact quantification of the measurement error bound for strong duality as future work. (Wise et al., 2020) `ev:asserted` p. 6 ^wise2020certifiably-030
- Experiments focus primarily on synthetic data where measurement statistics and the ground truth extrinsic transformation are known exactly. (Wise et al., 2020) `ev:reported` p. 6 ^wise2020certifiably-031
- The runtime of the algorithm was on the order of two seconds throughout all experiments without tuning optimization parameters. (Wise et al., 2020) `ev:measured` p. 6 ^wise2020certifiably-032
- Right-singular vectors of Z with singular values less than 10−3 were used to form the primal solution during certification. (Wise et al., 2020) `ev:reported` p. 6 ^wise2020certifiably-033
- Extracted rotations were checked for membership in SO(3) by requiring the Frobenius norm of R transpose R minus identity below 10−3. (Wise et al., 2020) `ev:reported` p. 6 ^wise2020certifiably-034
- Solutions with a duality gap greater than 0.01% of the primal cost were rejected as not certified optimal. (Wise et al., 2020) `ev:reported` p. 6 ^wise2020certifiably-035
- Synthetic trajectories were generated on a smooth undulating surface, with the sensor x-axis tangent to the trajectory and z-axis normal to the surface. (Wise et al., 2020) `ev:reported` p. 6 ^wise2020certifiably-036
- All simulated camera translation vectors were scaled by a positive factor α before zero-mean Gaussian noise was added. (Wise et al., 2020) `ev:reported` p. 6 ^wise2020certifiably-037
- Rotational noise was injected into each measured rotation matrix of both sensors via a left perturbation on SO(3). (Wise et al., 2020) `ev:reported` p. 6 ^wise2020certifiably-038
- Rotations of the simulated rigid body were about all 3 axes with magnitudes ranging from 0.05 rad to 0.3 rad. (Wise et al., 2020) `ev:reported` p. 7 ^wise2020certifiably-039
- Each noise setting was evaluated over 100 trials, counting how often the solver found and certified a globally optimal solution. (Wise et al., 2020) `ev:reported` p. 7 ^wise2020certifiably-040
- Translational noise standard deviations in the certification experiment were 1%, 10%, 50% and 100% of the translation magnitude. (Wise et al., 2020) `ev:reported` p. 7 ^wise2020certifiably-041
- Additional tests with rotational noise standard deviations up to 3 rad showed rotational noise did not affect solution optimality at those magnitudes. (Wise et al., 2020) `ev:measured` p. 7 ^wise2020certifiably-042
- The default formulation, with no redundant or right-handedness constraints, achieved a global optimum in 100% of trials at 1% translational noise. (Wise et al., 2020) `ev:measured` p. 7 ^wise2020certifiably-043
- Adding redundant column orthogonality constraints to row orthogonality improved the stability of the approach to measurement noise. (Wise et al., 2020) `ev:measured` p. 7 ^wise2020certifiably-044
- Including right-handedness constraints, which prohibit reflections, also increased the robustness of the solver to measurement noise. (Wise et al., 2020) `ev:measured` p. 7 ^wise2020certifiably-045
- The certification results mirror those of the known-scale predecessor method, which the authors say Theorem 1 retroactively predicts. (Wise et al., 2020) `ev:asserted` p. 7 ^wise2020certifiably-046
- The baseline is a suboptimal linear method solving the unconstrained problem via SVD, then projecting onto the nearest orthogonal matrix. (Wise et al., 2020) `ev:reported` p. 7 ^wise2020certifiably-047
- At low noise, the certifiable dual method and the linear baseline perform similarly in extrinsic calibration accuracy. (Wise et al., 2020) `ev:measured` p. 7 ^wise2020certifiably-048
- As noise increases, the certifiable dual method outperforms the linear baseline, which the authors say highlights the importance of global optimality. (Wise et al., 2020) `ev:measured` p. 7 ^wise2020certifiably-049
- Accuracy histograms covered translational noise standard deviations of 0.5% and 1% combined with rotational noise of 1% and 1.5%. (Wise et al., 2020) `ev:reported` p. 8 ^wise2020certifiably-050
- In the accuracy histograms, the globally optimal method has far less rotational and translational error than the simple linear approach. (Wise et al., 2020) `ev:measured` p. 8 ^wise2020certifiably-051
- The authors conclude that the zero-duality-gap region is large enough to accommodate severe sensor noise in their experiments. (Wise et al., 2020) `ev:asserted` p. 7 ^wise2020certifiably-052
- The authors defer extensive experimentation of the algorithm on real-world datasets to a planned sequel of this theoretical paper. (Wise et al., 2020) `ev:asserted` p. 7 ^wise2020certifiably-053
- [[Robot-world and hand-eye calibration (AX = YB)|Robot-world calibration]], probabilistic cost function variants and robust problem formulations are named as promising extensions of the technique. (Wise et al., 2020) `ev:asserted` p. 7 ^wise2020certifiably-054
- The authors state that no certifiable algorithm for joint spatiotemporal extrinsic calibration has, to their knowledge, been proposed. (Wise et al., 2020) `ev:asserted` p. 7 ^wise2020certifiably-055

## 🎯 Contributions

## 📖 Glossary

- **Hand-eye calibration** — Estimating the fixed transform between two rigidly linked sensors from their egomotion (AX = XB).
- **Extrinsic calibration** — Determining the rigid-body transformation between the reference frames of two sensors.
- **QCQP** — Quadratically-constrained quadratic program; here nonconvex because of the SO(3) constraints.
- **SDP relaxation** — Convex semidefinite program obtained as the Lagrangian dual of a QCQP.
- **Duality gap** — Difference between primal and dual costs; zero certifies global optimality.
- **Tightness** — Property that the relaxation's optimum equals the original nonconvex problem's optimum.
- **SDP stability** — Tightness persisting under small perturbations of the noise-free problem data.
- **Corank-one** — A square matrix whose rank is one less than its dimension.
- **Right-handedness constraint** — Constraint excluding reflections so that an orthogonal matrix is a proper rotation.

## ❓ Open questions

- How large is the measurement error bound ε within which strong duality holds, quantitatively?
- How does the certifiable monocular method perform on real-world sensor datasets?
- Can the approach be combined with a probabilistic (maximum-likelihood) cost function while keeping certifiability?
- Can a certifiable algorithm be built for joint spatiotemporal (time-offset plus extrinsic) calibration?
- How does the method behave with degenerate motion that violates the two-axis rotation condition of Lemma 1?

## 📝 Notes on reading

Version read: arXiv 2005.08298v5 (17 Nov 2021), which matches the packet identifier. The abstract printed in the PDF differs slightly from the registry abstract (e.g. 'requires' vs 'is not possible without'; 'convex relaxation' vs 'solution').

Figure 3 is a bar plot of the percentage of 100 trials certified optimal per constraint set (R, R+H, R+C, R+C+H) at translational noise of 1%, 10%, 50% and 100%; the individual bar heights are not recoverable from the extracted text, so only the text's statements about it were claimed.

Figure 4 shows histograms of translation error [m], rotation error [rad] and scale error for the dual and linear methods at four noise settings; bin counts are not readable in the extraction.

The equations (Lagrangian matrices P1, P2, Equations 8–33) are partly garbled by extraction; only their described roles were claimed.

Minor internal inconsistencies: Problem 3 is labelled the dual of Problem 2 while the text derives the Lagrangian of Problem 1; the proof of Lemma 1 writes tat in Equation (30) where Condition (22) has tai. Theorem 1's statement refers to Problem 4 although its title says Problem 5.

The certification thresholds (10−3 singular value, 0.01% duality gap) were chosen empirically, as footnote 3 states.

## Suggested new concepts

- Certifiable perception — recurring idea of algorithms that return a global optimality certificate, shared with SE-Sync and TEASER.
- Hand-eye calibration (AX = XB) — core calibration problem relevant to camera-robot setups in the lab.
- SDP relaxation tightness and stability — the theoretical tool used here to guarantee global optimality under noise.
- Scale ambiguity in monocular egomotion — needed wherever a monocular camera is calibrated against a metric sensor.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H5.** Relajación SDP de la calibración mano-ojo con escala desconocida y certificado de optimalidad global, complemento riguroso de Park-Martin.
