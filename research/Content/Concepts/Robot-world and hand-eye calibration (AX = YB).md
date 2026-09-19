---
aliases: ["RWHEC", "AX = YB"]
type: concept
element_type: process
topic: "[[Camera-robot calibration and visual servoing]]"
topics: ["[[Camera-robot calibration and visual servoing]]"]
created: 2026-09-19
---

## Working definition

Robot-world and hand-eye calibration jointly estimates two unknown rigid transforms, the sensor-to-hand transform X and the base-to-world or target transform Y, from paired measurements related by AX = YB, and generalizes the classical AX = XB problem to multiple sensors or targets.

## Evidence

- [[Chen2026optimal - Optimal Uncertainty-Aware Calibration for the AX=YB Problem#^chen2026optimal-001]] — The paper designs its calibration framework for the AX = YB problem, stating that it is also compatible with the AX = XB problem.
- [[Chen2026optimal - Optimal Uncertainty-Aware Calibration for the AX=YB Problem#^chen2026optimal-002]] — The authors argue that AX = YB can be transformed into AX = XB, which makes the AX = YB formulation more general.
- [[Chen2026optimal - Optimal Uncertainty-Aware Calibration for the AX=YB Problem#^chen2026optimal-053]] — Four closed-form constructions of AX = YB used within L-HED from the same initial value showed different iterative convergence behaviour.
- [[Wise2025certifably - A Certifably Correct Algorithm for Generalized Robot-World#^wise2025certifably-001]] — The authors use generalized RWHEC to mean a variant of robot-world and hand-eye calibration involving multiple, possibly monocular, sensors or targets
- [[Wise2025certifably - A Certifably Correct Algorithm for Generalized Robot-World#^wise2025certifably-003]] — The authors claim the first theoretical analysis of parameter identifiability for the generalized robot-world and hand-eye calibration problem
- [[Wise2025certifably - A Certifably Correct Algorithm for Generalized Robot-World#^wise2025certifably-004]] — Two-stage closed-form RWHEC solvers, which ignore rotation-translation coupling, can corrupt translation estimates with error from noisy rotation measurements
- [[Wise2025certifably - A Certifably Correct Algorithm for Generalized Robot-World#^wise2025certifably-010]] — The maximum likelihood RWHEC problem is written as a quadratically constrained quadratic program by homogenizing the translation term with an auxiliary variable
- [[Wise2025certifably - A Certifably Correct Algorithm for Generalized Robot-World#^wise2025certifably-042]] — In the single-camera study, both monocular RWHEC solvers returned more accurate estimates than their corresponding known-scale RWHEC methods
- [[Wise2020certifiably - Certifiably Optimal Monocular Hand-Eye Calibration#^wise2020certifiably-054]] — Robot-world calibration, probabilistic cost function variants and robust problem formulations are named as promising extensions of the technique.
- [[Chi2024universal - Universal Manipulation Interface In-The-Wild Robot Teaching#^chi2024universal-010]] — Because the camera is mechanically fixed relative to the fingers, mounting UMI on robots does not require camera-robot-world calibration.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: extra (4 sources) · topic: Camera-robot calibration and visual servoing (drafter's packet `q5-calibration-servoing`, confirmed at the gate)
