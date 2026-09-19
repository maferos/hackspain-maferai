---
aliases: []
type: "source"
title: "A Certifably Correct Algorithm for Generalized Robot-World and Hand-Eye Calibration"
citekey: "Wise2025certifably"
doi: "10.48550/arXiv.2507.23045"
arxiv: "2507.23045"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2507.23045"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Emmett Wise", "Pushyami Kaveti", "Qilong Chen", "Wenhao Wang", "Hanumant Singh", "Jonathan Kelly", "David M. Rosen", "Matthew Giamou"]
sha256: ["1e871cb8e178be7db0f4c7039d284ebee80f5024f9045b92dac54d941bd8adf3"]
pdf: "Content/Papers/Wise2025certifably.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Wise2025certifably.pdf]]

> [!abstract] One-sentence summary
> The paper casts multi-sensor, possibly monocular, robot-world and hand-eye calibration as a maximum likelihood QCQP, solves its SDP relaxation with post hoc and a priori global optimality guarantees, and derives identifiability criteria for the generalized problem.

## Abstract

Automatic extrinsic sensor calibration is a fundamental problem for multi-sensor platforms. Reliable and general-purpose solutions should be computationally efficient, require few assumptions about the structure of the sensing environment, and demand little effort from human operators. In this work, we introduce a fast and certifiably globally optimal algorithm for solving a generalized formulation of the robot-world and hand-eye calibration (RWHEC) problem. The formulation of RWHEC presented is "generalized" in that it supports the simultaneous estimation of multiple sensor and target poses, and permits the use of monocular cameras that, alone, are unable to measure the scale of their environments. In addition to demonstrating our method's superior performance over existing solutions through extensive simulated and real experiments, we derive novel identifiability criteria and establish a priori guarantees of global optimality for problem instances with bounded measurement errors. As part of our analysis, we propose a new constraint qualification for nonlinear programs with redundant constraints; this constraint qualification is of independent interest for establishing the exactness of SDP relaxations of QCQPs that have been tightened through the addition of redundant constraints. Finally, we provide a free and open-source implementation of our algorithms and experiments. (arXiv)

## 🧠 Key ideas (atomic)

- The authors use generalized RWHEC to mean a variant of [[Robot-world and hand-eye calibration (AX = YB)|robot-world and hand-eye calibration]] involving multiple, possibly monocular, sensors or targets (Wise et al., 2025) `ev:asserted` p. 2 ^wise2025certifably-001
- The authors claim the first certifiably globally optimal solver for a multi-sensor extrinsic calibration problem (Wise et al., 2025) `ev:asserted` p. 2 ^wise2025certifably-002
- The authors claim the first theoretical analysis of parameter identifiability for the [[Robot-world and hand-eye calibration (AX = YB)|generalized robot-world and hand-eye calibration problem]] (Wise et al., 2025) `ev:asserted` p. 2 ^wise2025certifably-003
- [[Robot-world and hand-eye calibration (AX = YB)|Two-stage closed-form RWHEC solvers]], which ignore rotation-translation coupling, can corrupt translation estimates with error from noisy rotation measurements (Wise et al., 2025) `ev:asserted` p. 3 ^wise2025certifably-004
- Horn et al. (2023) use a dual quaternion pose representation to cast generalized RWHEC as a quadratically constrained quadratic program (Wise et al., 2025) `ev:cited` p. 3 ^wise2025certifably-005
- The authors state that poorer dual quaternion performance is most likely because unit quaternions form a double cover of SO(3) (Wise et al., 2025) `ev:asserted` p. 3 ^wise2025certifably-006
- The work extends the multi-frame RWHEC formulation of Wang et al. (2022) to monocular sensors within a maximum likelihood estimation framework (Wise et al., 2025) `ev:asserted` p. 4 ^wise2025certifably-007
- The probabilistic formulation assumes the robot measurements Ai are noiseless, with all noise placed on the camera measurements Bi (Wise et al., 2025) `ev:asserted` p. 6 ^wise2025certifably-008
- Camera measurement noise is modelled as isotropic Gaussian on translation with a Langevin-distributed right perturbation on rotation (Wise et al., 2025) `ev:asserted` p. 6 ^wise2025certifably-009
- The [[Robot-world and hand-eye calibration (AX = YB)|maximum likelihood RWHEC problem]] is written as a quadratically constrained quadratic program by homogenizing the translation term with an auxiliary variable (Wise et al., 2025) `ev:computed` p. 6 ^wise2025certifably-010
- Each SO(3) variable uses redundant quadratic orthogonality constraints plus cross-product constraints that replace the cubic determinant condition (Wise et al., 2025) `ev:asserted` p. 7 ^wise2025certifably-011
- For targets of unknown scale, the monocular model includes an unknown scale factor α that the scaled translation variables absorb (Wise et al., 2025) `ev:asserted` p. 7 ^wise2025certifably-012
- The authors omit a positivity constraint on α, assuming it is positive at global optima under low or moderate noise (Wise et al., 2025) `ev:asserted` p. 7 ^wise2025certifably-013
- The multi-sensor problem is modelled as a bipartite directed graph whose edges each hold all observations of one target by one camera (Wise et al., 2025) `ev:asserted` p. 8 ^wise2025certifably-014
- The monocular multi-sensor extension is limited to a single target or to targets sharing the same unknown scale (Wise et al., 2025) `ev:asserted` p. 8 ^wise2025certifably-015
- A generalized Schur complement yields a reduced QCQP whose objective depends only on the rotation variables (Wise et al., 2025) `ev:computed` p. 10 ^wise2025certifably-016
- The Lagrangian dual of the reduced problem is a semidefinite program maximizing the dual variable of the homogenizing constraint (Wise et al., 2025) `ev:computed` p. 10 ^wise2025certifably-017
- A duality gap small relative to machine precision gives a post hoc certificate of global optimality for the primal solution (Wise et al., 2025) `ev:asserted` p. 10 ^wise2025certifably-018
- For a weakly connected problem graph with exact rotations, uniquely determining one rotation implies the whole rotation-only problem has a unique solution (Wise et al., 2025) `ev:computed` p. 11 ^wise2025certifably-019
- In a weakly connected graph, one sensor-target pair with measurements related by rotations about two distinct axes suffices for a unique rotational solution (Wise et al., 2025) `ev:computed` p. 11 ^wise2025certifably-020
- The authors leave uniqueness results for the more complex monocular case of the generalized problem for future work (Wise et al., 2025) `ev:asserted` p. 11 ^wise2025certifably-021
- The same single-vertex uniqueness result extends to the full SE(3) standard generalized problem with exact pose measurements (Wise et al., 2025) `ev:computed` p. 12 ^wise2025certifably-022
- The authors indicate a practitioner can make all parameters identifiable by exciting the platform about two axes for one target-sensor pair (Wise et al., 2025) `ev:asserted` p. 13 ^wise2025certifably-023
- The authors state that their identifiability analysis is limited to the noise-free case, focusing on motion that practitioners can design (Wise et al., 2025) `ev:asserted` p. 13 ^wise2025certifably-024
- The authors prove the Abadie constraint qualification holds at every point of SO(3) for their redundant quadratic constraint encoding (Wise et al., 2025) `ev:computed` p. 13 ^wise2025certifably-025
- The authors state the constraint qualification result applies to any QCQP whose only constrained variables lie in SO(3) or SE(3) (Wise et al., 2025) `ev:asserted` p. 14 ^wise2025certifably-026
- If exact measurements give a unique solution that is also an unconstrained minimizer, the SDP relaxation is tight in a neighbourhood of those measurements (Wise et al., 2025) `ev:computed` p. 14 ^wise2025certifably-027
- The authors describe this as, to their knowledge, the first a priori global optimality guarantee of its kind for multi-sensor calibration (Wise et al., 2025) `ev:asserted` p. 14 ^wise2025certifably-028
- Approximating the size of the SDP-tightness region around noise-free instances is computationally impractical with presently available tools, the authors note (Wise et al., 2025) `ev:asserted` p. 14 ^wise2025certifably-029
- The first simulated system is a manipulator with a hand-mounted camera observing a fiducial target, giving one X and one Y (Wise et al., 2025) `ev:reported` p. 14 ^wise2025certifably-030
- The second simulated system has a hand-mounted target observed by four stationary cameras, giving four X variables and one Y (Wise et al., 2025) `ev:reported` p. 14 ^wise2025certifably-031
- Simulations used translation noise of σ = 1 cm or σ = 5 cm with rotation concentrations κ = 125 or κ = 12 (Wise et al., 2025) `ev:reported` p. 15 ^wise2025certifably-032
- The standard-scale benchmarks were Shah, Wang et al., Horn et al., Dornaika and Horaud, and the authors' local on-manifold solver LOM (Wise et al., 2025) `ev:reported` p. 15 ^wise2025certifably-033
- Single-sphere camera trajectories satisfied the two-axis identifiability conditions but were empirically observed to lack a unique monocular RWHEC solution (Wise et al., 2025) `ev:measured` p. 15 ^wise2025certifably-034
- Identifiable monocular instances were created by collecting measurements on two spheres, one with unit radius and one with radius 0.3 m (Wise et al., 2025) `ev:measured` p. 15 ^wise2025certifably-035
- In the single-camera study, the two-stage closed-form solvers of Shah and Wang et al. were generally the least accurate methods (Wise et al., 2025) `ev:measured` p. 15 ^wise2025certifably-036
- In the single-camera known-scale study, the proposed method and LOM outperformed the other methods by up to 50 mm (Wise et al., 2025) `ev:measured` p. 15 ^wise2025certifably-037
- The accuracy of LOM degraded significantly when it was randomly initialized in the single-camera known-scale study (Wise et al., 2025) `ev:measured` p. 16 ^wise2025certifably-038
- The proposed method returned the same global minimizer for any initialization in the single-camera known-scale study (Wise et al., 2025) `ev:measured` p. 16 ^wise2025certifably-039
- At κ = 12 and σ = 1 cm, the proposed method had 15.1 mm X-translation error versus 65.5 mm for Shah (Wise et al., 2025) `ev:measured` p. 17 ^wise2025certifably-040
- In monocular single-camera simulations at κ = 125, σ = 1 cm, randomly initialized LOM had 578 mm X-translation error versus 4.71 mm (Wise et al., 2025) `ev:measured` p. 18 ^wise2025certifably-041
- In the single-camera study, both [[Robot-world and hand-eye calibration (AX = YB)|monocular RWHEC solvers]] returned more accurate estimates than their corresponding known-scale RWHEC methods (Wise et al., 2025) `ev:measured` p. 16 ^wise2025certifably-042
- In the multi-camera study, the gap between randomly initialized LOM and the proposed method was larger than in the single-sensor case (Wise et al., 2025) `ev:measured` p. 16 ^wise2025certifably-043
- The closed-form method of Wang et al. was more accurate than the globally optimal dual quaternion method of Horn et al. in multi-camera simulations (Wise et al., 2025) `ev:measured` p. 16 ^wise2025certifably-044
- In multi-camera simulations at κ = 125, σ = 1 cm, the proposed method had 0.992 mm X-translation error versus 12.11 mm for Horn (Wise et al., 2025) `ev:measured` p. 18 ^wise2025certifably-045
- The real-world rig carried eight Point Grey Blackfly S USB cameras, OptiTrack markers, and a VectorNav VN-100 IMU (Wise et al., 2025) `ev:reported` p. 17 ^wise2025certifably-046
- A total of sixteen AprilTags served as fiducial markers, with OptiTrack markers on a single tag providing ground truth (Wise et al., 2025) `ev:reported` p. 17 ^wise2025certifably-047
- Camera extrinsic ground truth was approximated with the Kalibr toolbox, which the authors treat only as a rough proxy for the true solution (Wise et al., 2025) `ev:reported` p. 17 ^wise2025certifably-048
- Gross outliers were rejected with RANSAC, counting a measurement pair as inlier within 0.6 m and 60◦ of the estimated pose (Wise et al., 2025) `ev:reported` p. 20 ^wise2025certifably-049
- The estimated AprilTag translation was within 12 cm, or 8% of the ground-truth distance, and 6◦ of OptiTrack ground truth (Wise et al., 2025) `ev:measured` p. 20 ^wise2025certifably-050
- Estimated camera calibration parameters were on average within about 3 cm and 1◦ of the parameters estimated by Kalibr (Wise et al., 2025) `ev:measured` p. 20 ^wise2025certifably-051
- The estimated AprilTag scale was 2.5% smaller than the hand-measured value in the real-world experiment (Wise et al., 2025) `ev:measured` p. 20 ^wise2025certifably-052
- The authors state additional experiments are needed to determine whether the monocular method reliably improves accuracy with noisy marker sizes (Wise et al., 2025) `ev:asserted` p. 20 ^wise2025certifably-053
- AprilTag 20 translation error was 11.5 cm for the proposed known-scale method and 7.94 cm for its unknown-scale variant (Wise et al., 2025) `ev:measured` p. 21 ^wise2025certifably-054
- The relative suboptimality bound was −6.41e-9 for the known-scale real data and 8.55e-9 for the monocular case (Wise et al., 2025) `ev:measured` p. 21 ^wise2025certifably-055
- The longest observed runtime was approximately five minutes, for the global solver on the monocular real-world experiment (Wise et al., 2025) `ev:measured` p. 21 ^wise2025certifably-056
- COSMO solved the synthetic problems with the multiple-X sparsity pattern substantially faster, taking at most seven seconds (Wise et al., 2025) `ev:measured` p. 21 ^wise2025certifably-057
- The authors conclude their rotation-matrix MLE formulation is superior to dual quaternion-based methods, based on their experiments (Wise et al., 2025) `ev:asserted` p. 22 ^wise2025certifably-058
- The method can serve as a certification step for other, potentially faster, generalized RWHEC solvers that lack formal guarantees (Wise et al., 2025) `ev:asserted` p. 22 ^wise2025certifably-059
- The current MLE formulation assumes isotropic translation and rotation noise, which the authors list as a direction for future work (Wise et al., 2025) `ev:asserted` p. 22 ^wise2025certifably-060
- The authors state none of their presented methods are robust, with one cleaned dataset used for every comparison (Wise et al., 2025) `ev:asserted` p. 25 ^wise2025certifably-061
- Including both redundant orthogonality constraints acts as duality strengthening, increasing the number of noisy problem instances exactly solvable by the approach (Wise et al., 2025) `ev:asserted` p. 25 ^wise2025certifably-062

## 🎯 Contributions

## 📖 Glossary

- **RWHEC** — Robot-world and hand-eye calibration: estimate X and Y from AiX = YBi.
- **Generalized RWHEC** — RWHEC with multiple, possibly monocular, sensors and/or targets.
- **QCQP** — Quadratically constrained quadratic program.
- **Shor relaxation** — Standard SDP relaxation of a QCQP obtained by lifting to a matrix variable.
- **Tight relaxation** — SDP relaxation whose optimum equals the original nonconvex problem's optimum.
- **Duality gap certificate** — Primal minus dual objective bounding a solution's suboptimality post hoc.
- **Abadie constraint qualification (ACQ)** — Weak regularity condition guaranteeing Lagrange multipliers exist at a solution.
- **Langevin distribution** — Distribution over SO(3) with a mode and concentration κ.
- **Identifiability** — Noise-free data determine the calibration parameters uniquely.
- **Double cover** — Unit quaternions q and −q map to the same rotation.
- **LOM** — The authors' local on-manifold nonlinear least-squares RWHEC solver in Ceres.

## ❓ Open questions

- What are identifiability conditions for the monocular (unknown-scale) generalized RWHEC problem?
- How large is the region of SDP tightness around noise-free instances, and can it be estimated practically?
- Can multiple-edge cases that together yield uniqueness be characterized completely?
- Does adding α ≥ 0 matter in extremely noisy monocular instances?
- Can a robust (e.g. truncated least squares) objective handle data-association outliers while preserving the QCQP structure and tightness?
- Can the formulation handle anisotropic noise and multiple unknown target scales?
- Does the monocular method reliably improve accuracy when fiducial marker sizes are noisy?

## 📝 Notes on reading

Version read: arXiv 2507.23045v2 (4 May 2026), typeset as an International Journal of Robotics Research manuscript ("©The Author(s) 2026", DOI to be assigned). The registry title spells "Certifably"; the PDF title reads "Certifiably". The PDF author list writes "Qilong Cheng" whereas the metadata has "Qilong Chen".

Numbering inconsistency inside the paper: results introduced as Theorem 2 / Theorem 4 / Theorem 7 in the text are labelled Corollary 2, Corollary 4 and Proposition 7.

Equations and matrix definitions (e.g. Eqs. 35–48, 70–73) are garbled in the extraction; the count of DQ formulations appears as "22N" (presumably 2^(2N)) and was not claimed. COSMO tolerances and Ceres tolerances were extracted with lost superscripts and were not claimed.

Table 1 (method feature matrix, p. 3) lost its check marks in extraction; only the representation column is readable. Figures 1–10 are described only by captions (kinematic loop diagrams, bipartite graph, rig photos, trajectory, observability grid, sparsity patterns).

Single-camera headline improvement "up to 50 mm and 3 degrees" spans pages 15–16; only the 50 mm part was claimed. The known-scale real-world duality gap is slightly negative (−6.41e-9), which the authors attribute to floating point roundoff.

## Suggested new concepts

- Certifiable estimation — SDP relaxations with duality-gap certificates recur across SLAM, registration and calibration papers.
- Hand-eye calibration — core calibration problem family (AX = XB / AX = YB) relevant to robot-mounted cameras.
- Constraint qualification for redundant constraints — reusable tool for proving tightness of relaxations tightened with redundant constraints.
- Parameter identifiability in calibration — excitation conditions (two rotation axes) determining well-posed calibration.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H5.** Resuelve AX=YB con varios sensores y patrones con garantías globales y criterios de identificabilidad para planificar las poses de calibración.
