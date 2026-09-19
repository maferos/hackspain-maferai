---
aliases: []
type: "source"
title: "Optimal Uncertainty-Aware Calibration for the AX=YB Problem"
citekey: "Chen2026optimal"
doi: "10.48550/arXiv.2605.04809"
arxiv: "2605.04809"
year: 2026
publication_type: "preprint"
url: "https://arxiv.org/abs/2605.04809"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Yanjia Chen", "Xiangfei Li", "Huan Zhao", "Yiyuan Hong", "Guanxiao Xia", "Jiexin Zhang", "Han Ding"]
sha256: ["99109f92f5071cac8dba3b5d21f468c7c61f6581a276f91d13a19aa23238d970"]
pdf: "Content/Papers/Chen2026optimal.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Chen2026optimal.pdf]]

> [!abstract] One-sentence summary
> The paper proposes UAL-HED, a Lie-algebra iterative solver for hand-eye and robot-world calibration (AX = YB) that uses a data-driven relative uncertainty metric instead of explicit uncertainty models, and reports lower errors than classical and iterative baselines in simulation and on an industrial robot with a laser tracker.

## Abstract

This article proposes a general optimization framework for solving hand-eye calibration problem. Unlike traditional methods, an iterative algorithm based on Lie algebra that achieves approximately global optimal solutions is developed. During the optimization process, the method strictly preserves the structural constraints of the calibration parameters and enables synchronized updates between calibration parameters. Recognizing that data used in real-word hand-eye calibration often contain uncertainty, especially in over-loading and large workspace industrial robot scenarios, which can significantly degrade accuracy, and accurately modeling such uncertainty is inherently difficult, this article avoids explicit uncertainty modeling. Instead, an uncertainty metric to evaluate the relative uncertainty between data sources is introduced and used to dynamically refine the iterative process. To further enhance convergence efficiency, an effective initial solution generation method that improves overall stability and accuracy is designed. Numerical simulations and real-world experiments validate the effectiveness of the proposed approach, and in synthetic datasets, the proposed approach improves the estimation accuracy by at least 67\% under high-uncertainty conditions compared with the existing methods. (arXiv)

## 🧠 Key ideas (atomic)

- The paper designs its calibration framework for the [[Robot-world and hand-eye calibration (AX = YB)|AX = YB problem]], stating that it is also compatible with the AX = XB problem. (Chen et al., 2026) `ev:asserted` p. 1 ^chen2026optimal-001
- The authors argue that AX = YB can be transformed into [[Hand-eye calibration (AX = XB)|AX = XB]], which makes the [[Robot-world and hand-eye calibration (AX = YB)|AX = YB formulation]] more general. (Chen et al., 2026) `ev:asserted` p. 1 ^chen2026optimal-002
- The study is conducted with the vision measurement system fixed externally in the robot environment, which the authors call readily extendable to robot-mounted sensors. (Chen et al., 2026) `ev:reported` p. 1 ^chen2026optimal-003
- The paper calls system-level or structural uncertainty arising from limited robot precision in hand-eye calibration epistemic uncertainty (EU). (Chen et al., 2026) `ev:asserted` p. 2 ^chen2026optimal-004
- The authors state that epistemic uncertainty sources exhibit dependent rather than independently stochastic behaviour, being systematically mapped from the robot pose. (Chen et al., 2026) `ev:asserted` p. 2 ^chen2026optimal-005
- Robot pose accuracy is often significantly lower than pose repeatability, with resulting errors reaching the millimeter scale in large workspaces or heavy payloads. (Chen et al., 2026) `ev:cited` p. 2 ^chen2026optimal-006
- The authors argue that both epistemic and aleatoric uncertainty ultimately manifest in calibration only through distortions in the source data {Ai} and {Bi}. (Chen et al., 2026) `ev:asserted` p. 2 ^chen2026optimal-007
- The authors state that decoupled methods for solving X and Y are prone to cumulative and propagated errors, unlike synchronous solving. (Chen et al., 2026) `ev:asserted` p. 4 ^chen2026optimal-008
- [[Hand-eye calibration (AX = XB)|Linear hand-eye calibration methods]] minimize algebraic errors, so their achievable accuracy is inherently bounded and sensitive to the uncertainty in the data. (Chen et al., 2026) `ev:cited` p. 4 ^chen2026optimal-009
- The paper notes that there is no bi-invariant distance on SE(3), so solution accuracy may depend on the chosen minimization model. (Chen et al., 2026) `ev:asserted` p. 6 ^chen2026optimal-010
- The authors state that iterating rotation and translation, or X and Y, separately propagates computational errors, making synchronized iteration the optimal method. (Chen et al., 2026) `ev:asserted` p. 6 ^chen2026optimal-011
- Data pair correspondence is checked by requiring the screw rotation angles and pitches of the relative motions Aij and Bij to match within thresholds. (Chen et al., 2026) `ev:reported` p. 6 ^chen2026optimal-012
- The L-HED objective uses a Mahalanobis distance on linearized Lie-algebra residuals to handle the differing physical units of rotation and translation. (Chen et al., 2026) `ev:reported` p. 7 ^chen2026optimal-013
- L-HED updates the Lie-algebra increments of X and Y jointly with a momentum gradient scheme meant to accelerate convergence and reduce oscillations. (Chen et al., 2026) `ev:reported` p. 7 ^chen2026optimal-014
- Small stochastic perturbations are added to the gradient when necessary, to escape local optima and facilitate computing a globally optimal solution. (Chen et al., 2026) `ev:reported` p. 7 ^chen2026optimal-015
- A Lie algebra-based residual metric serves as the heuristic indicator for selecting stochastic perturbations, since unselected perturbations would disrupt convergence properties. (Chen et al., 2026) `ev:reported` p. 8 ^chen2026optimal-016
- The paper states that convexity of its objective requires an affine deviation in the increments and a positive definite weighting covariance matrix. (Chen et al., 2026) `ev:asserted` p. 8 ^chen2026optimal-017
- The authors avoid explicit modeling of the source-data error term, arguing that imprecise uncertainty modeling can degrade the solution accuracy. (Chen et al., 2026) `ev:asserted` p. 9 ^chen2026optimal-018
- Each source dataset is decentralized with its iteratively computed SE(3) mean and covariance, yielding normalized vectors for every data pair. (Chen et al., 2026) `ev:reported` p. 9 ^chen2026optimal-019
- The derivation shows that without uncertainty the norms of the normalized vectors from {Ai} and {Bi} must be equal for each corresponding pair. (Chen et al., 2026) `ev:computed` p. 9 ^chen2026optimal-020
- The inequality between the normalized-vector norms is used as a metric quantifying relative uncertainty between the source datasets {Ai} and {Bi}. (Chen et al., 2026) `ev:asserted` p. 9 ^chen2026optimal-021
- The uncertainty correction combines per-pair norm ratios with covariance ratios, weighted by an influence factor computed from dataset variances. (Chen et al., 2026) `ev:reported` p. 10 ^chen2026optimal-022
- The paper names its relative uncertainty metric the Sharpe Ratio Metric under the Euclidean group, abbreviated SRM@SE(3). (Chen et al., 2026) `ev:asserted` p. 3 ^chen2026optimal-023
- Incorporating SRM@SE(3) into L-HED produces the UAL-HED method, which the authors present for optimization with highly uncertain data sources. (Chen et al., 2026) `ev:asserted` p. 3 ^chen2026optimal-024
- The SI-AH initial solver obtains the rotation of X by singular value decomposition over screw-axis vectors of the relative motions. (Chen et al., 2026) `ev:reported` p. 11 ^chen2026optimal-025
- SI-AH then refines the rotation and translation of X jointly with a Levenberg-Marquardt iteration to eliminate errors from separate solving. (Chen et al., 2026) `ev:reported` p. 11 ^chen2026optimal-026
- In simulation, robot poses are assumed error-free while synthesized camera observations carry robot aleatoric errors, robot epistemic errors and measurement errors. (Chen et al., 2026) `ev:reported` p. 11 ^chen2026optimal-027
- In simulation, the uncertainty metric increased approximately proportionally as the magnitude of injected uncertainty increased across Error Scenarios 1 to 10. (Chen et al., 2026) `ev:measured` p. 12 ^chen2026optimal-028
- High rotational aleatoric uncertainty had a greater impact on the uncertainty metric than high translational aleatoric uncertainty in Error Scenarios 11 to 18. (Chen et al., 2026) `ev:measured` p. 12 ^chen2026optimal-029
- From different initial values, the heuristic error metric of L-HED converged to the same level of accuracy in the simulation study. (Chen et al., 2026) `ev:measured` p. 12 ^chen2026optimal-030
- With an initial value close to the optimal matrices, L-HED reached the designed stopping threshold in 7,734 iterations. (Chen et al., 2026) `ev:measured` p. 12 ^chen2026optimal-031
- With initial values far from the optimal matrices, L-HED convergence was achieved after 30,731 iterations in the simulation. (Chen et al., 2026) `ev:measured` p. 12 ^chen2026optimal-032
- Using the identity matrix as initial value, L-HED still converged, but the number of iterations increased significantly to 128518. (Chen et al., 2026) `ev:measured` p. 12 ^chen2026optimal-033
- Seven methods were compared: L-HED, UAL-HED, SI-AH, dual quaternions, Kronecker product, LMI-SDP optimization and decoupled point cloud matching. (Chen et al., 2026) `ev:reported` p. 13 ^chen2026optimal-034
- Compared to L-HED, UAL-HED reduced the average estimation error of X by 7.1% across six synthetic uncertainty combinations. (Chen et al., 2026) `ev:measured` p. 13 ^chen2026optimal-035
- Compared to L-HED, UAL-HED achieved a 10.6% reduction in the average estimation error of Y on synthesized data. (Chen et al., 2026) `ev:measured` p. 13 ^chen2026optimal-036
- Compared to the LMI method, UAL-HED reduced the average estimation error of X by 81.1% on synthesized data. (Chen et al., 2026) `ev:measured` p. 13 ^chen2026optimal-037
- Compared to the LMI method, UAL-HED achieved a 79.5% reduction in the average estimation error of Y on synthesized data. (Chen et al., 2026) `ev:measured` p. 13 ^chen2026optimal-038
- The decoupled point cloud matching method performed worst, with UAL-HED achieving a 91.7% lower estimation error for X. (Chen et al., 2026) `ev:measured` p. 13 ^chen2026optimal-039
- For Y, UAL-HED reduced the estimation error by 90.6% compared to the point cloud matching method in simulation. (Chen et al., 2026) `ev:measured` p. 13 ^chen2026optimal-040
- Under simple uncertainty combinations, the SI-AH initial solver also performed strongly, even achieving the best result in the first scenario. (Chen et al., 2026) `ev:measured` p. 13 ^chen2026optimal-041
- The authors attribute this to the L-HED heuristic metric not being constructed from the true ideal matrices, risking overfitting near the optimum. (Chen et al., 2026) `ev:asserted` p. 13 ^chen2026optimal-042
- Across the six scenarios, UAL-HED achieved on average a 74.7% lower estimation error than SI-AH for X. (Chen et al., 2026) `ev:measured` p. 14 ^chen2026optimal-043
- Across the six scenarios, UAL-HED achieved on average a 73.5% lower estimation error than SI-AH for Y. (Chen et al., 2026) `ev:measured` p. 14 ^chen2026optimal-044
- For individual synthesized datasets another method may be most accurate, but UAL-HED most frequently attained the highest accuracy in simulation. (Chen et al., 2026) `ev:measured` p. 14 ^chen2026optimal-045
- Under high uncertainty in both source datasets, all seven methods estimated X noticeably less accurately than under low uncertainty. (Chen et al., 2026) `ev:measured` p. 15 ^chen2026optimal-046
- The two decoupled methods showed the greatest decrease in accuracy under high uncertainty, which the authors take to indicate error propagation and accumulation. (Chen et al., 2026) `ev:measured` p. 15 ^chen2026optimal-047
- In these simulations, rotational uncertainty had a greater tendency to disrupt the estimation of calibration parameters than positional uncertainty. (Chen et al., 2026) `ev:measured` p. 15 ^chen2026optimal-048
- L-HED, UAL-HED and SI-AH estimated X with the same accuracy whether only {Ai} or only {Bi} had high uncertainty. (Chen et al., 2026) `ev:measured` p. 15 ^chen2026optimal-049
- As source-data uncertainty increased, the relative effectiveness of UAL-HED compared to L-HED gradually improved in the simulations. (Chen et al., 2026) `ev:measured` p. 15 ^chen2026optimal-050
- Under the simulated conditions, UAL-HED exhibited the smallest variance in the estimation error of X, followed by L-HED. (Chen et al., 2026) `ev:measured` p. 15 ^chen2026optimal-051
- Estimation errors for Y were higher than those for X across all seven methods in the 16-setting simulation study. (Chen et al., 2026) `ev:measured` p. 16 ^chen2026optimal-052
- Four [[Robot-world and hand-eye calibration (AX = YB)|closed-form constructions of AX = YB]] used within L-HED from the same initial value showed different iterative convergence behaviour. (Chen et al., 2026) `ev:measured` p. 16 ^chen2026optimal-053
- After swapping the translational components of X and Y, the ranking of closed-form constructions reversed, which the authors take to confirm their hypothesis. (Chen et al., 2026) `ev:measured` p. 17 ^chen2026optimal-054
- Increasing the number of source data sets improved accuracy for all seven methods, with accuracy tending to stabilize once 100 sets were reached. (Chen et al., 2026) `ev:measured` p. 17 ^chen2026optimal-055
- Under high uncertainty, selecting source data with lower uncertainty metrics gave higher accuracy for four baseline methods than no data selection. (Chen et al., 2026) `ev:measured` p. 18 ^chen2026optimal-056
- Among five residual forms, the homogeneous-transformation-matrix residual most accurately reflected the ground-truth ranking of calibration estimation errors in simulation. (Chen et al., 2026) `ev:measured` p. 18 ^chen2026optimal-057
- Real-world experiments used an ABB IRB 6700 155/2.85 robot with a laser tracker and T-Mac providing 6-DoF measurements. (Chen et al., 2026) `ev:reported` p. 18 ^chen2026optimal-058
- The robot carried an end-effector with a gravity-compensated calculated weight of 47 kg during the real-world calibration experiments. (Chen et al., 2026) `ev:reported` p. 18 ^chen2026optimal-059
- In each of two workspace configurations, 100 source data pairs were collected for estimation, followed by 99 additional pairs for validation. (Chen et al., 2026) `ev:reported` p. 19 ^chen2026optimal-060
- The average uncertainty metric in the large workspace was 1.56 times that of the small workspace in the real-world experiments. (Chen et al., 2026) `ev:measured` p. 19 ^chen2026optimal-061
- According to the authors, UAL-HED achieved the best HTM-based residual in both the high-uncertainty and low-uncertainty real-world workspaces. (Chen et al., 2026) `ev:measured` p. 19 ^chen2026optimal-062
- With UAL-HED in the high-uncertainty workspace, the average position difference between transformed camera data and teach pendant data was 0.293 mm. (Chen et al., 2026) `ev:measured` p. 20 ^chen2026optimal-063
- With UAL-HED in the low-uncertainty workspace, the average position difference between transformed camera data and teach pendant data was 0.158 mm. (Chen et al., 2026) `ev:measured` p. 20 ^chen2026optimal-064
- On validation pairs in the high-uncertainty workspace, UAL-HED had a conversion error of 0.342mm, versus 0.346mm for L-HED. (Chen et al., 2026) `ev:measured` p. 21 ^chen2026optimal-065
- In the high-uncertainty workspace, the baseline conversion errors ranged from 0.671mm for Dual-Quaternion to 1.17mm for Kronecker-Product. (Chen et al., 2026) `ev:measured` p. 21 ^chen2026optimal-066
- In the low-uncertainty workspace, L-HED had a conversion error of 0.193mm, lower than the 0.202mm of UAL-HED. (Chen et al., 2026) `ev:measured` p. 21 ^chen2026optimal-067
- In the abstract, the approach is said to improve estimation accuracy by at least 67% under high uncertainty on synthetic datasets. (Chen et al., 2026) `ev:abstract` p. 1 ^chen2026optimal-068
- The authors conclude that source-data uncertainty significantly impacts calibration accuracy, particularly with a large uncertainty disparity between {Ai} and {Bi}. (Chen et al., 2026) `ev:asserted` p. 21 ^chen2026optimal-069

## 🎯 Contributions


## 📖 Glossary

- **AX = YB** — Hand-eye plus robot-world calibration equation with two unknown rigid transforms X and Y.
- **AX = XB** — Classical hand-eye calibration equation with one unknown transform from relative motions.
- **HECPs** — Hand-eye calibration parameters, the unknown transforms X and Y.
- **Aleatoric uncertainty (AU)** — Random, typically Gaussian-modelled measurement noise in calibration source data.
- **Epistemic uncertainty (EU)** — Pose-dependent, structural error from limited robot pose accuracy.
- **L-HED** — Lie algebra-based heuristic escape descent: synchronized X, Y iteration with stochastic local-minimum escape.
- **UAL-HED** — L-HED corrected by the SRM@SE(3) relative uncertainty metric.
- **SRM@SE(3)** — Sharpe Ratio Metric on SE(3), a relative uncertainty measure between two source datasets.
- **SI-AH** — Scale-invariant analytical heuristic method providing initial X, Y estimates via screw invariants.
- **Robot pose accuracy (RPA)** — Ability of a robot to reach a commanded pose in space.
- **Robot pose repeatability (RPR)** — Ability of a robot to return consistently to the same pose.
- **Bi-invariant metric** — A distance invariant under both left and right group multiplication; SE(3) lacks one.

## ❓ Open questions

- Why does UAL-HED not beat L-HED in the low-uncertainty real-world workspace conversion error (Table 9), despite the text claiming it is consistently best?
- How sensitive are L-HED iteration counts and final accuracy to the stochastic perturbation magnitude and escape criterion?
- Can the closed-form construction be chosen automatically from the data, since the best form depends on the relative translation magnitudes of X and Y?
- Does the SRM@SE(3) metric remain informative for camera-based (not laser-tracker) sensing with larger aleatoric noise?
- Where does the abstract's figure of at least 67% improvement come from, given that the body reports different percentages?
- How does runtime scale, given convergence can require over a hundred thousand iterations from a poor initial value?

## 📝 Notes on reading

Version read: arXiv preprint 2605.04809v1, typeset with a SAGE journal template (placeholder journal title and DOI).

The abstract's "at least 67%" improvement figure is not found in the body text; Section 5.1.4 reports 7.1%/10.6% versus L-HED, 81.1%/79.5% versus LMI, 91.7%/90.6% versus point cloud matching and 74.7%/73.5% versus SI-AH.

Inconsistency: Section 5.1.4 (p. 13) says dual quaternions are better for X and the Kronecker product for Y, whereas Section 5.1.5 (p. 16) says dual quaternions are more accurate for Y, the opposite of the trend for X. The Y comparison was therefore not claimed.

Inconsistency: p. 19 says UAL-HED consistently achieves the best performance in both workspaces, but Table 9 (p. 21) lists L-HED at 0.193mm and UAL-HED at 0.202mm in the low-uncertainty workspace.

Inconsistency: p. 15 refers to "two decoupled methods", but p. 13 identifies only point cloud matching as decoupled.

Table 3 (p. 14) is garbled in extraction: the translational columns of the PCM and SI-AH rows are shifted or duplicated, and the translational Y columns show near-identical values across all methods; per-cell values were not claimed. Table 1 and Table 2 column alignment is also partly lost.

Figures 5-26 (uncertainty metric trends, convergence curves, error bars, workspace sketches, 6-DoF difference plots) could only be described from their captions and surrounding text. Figure 1 (framework) and Figure 3 extracted as scattered symbols.

Several cross-references read "Section" with no number (Algorithm 1 inputs, p. 9), and p. 9 cites Equation (42) where the uncertainty correction appears to be Equation (43). The laser tracker is spelled "Lecia AT 960" in the text.

## Suggested new concepts

- Hand-eye and robot-world calibration (AX = YB) — central formulation shared by camera-robot registration papers.
- Epistemic vs aleatoric uncertainty in robot calibration — distinguishes pose-dependent robot error from sensor noise.
- Lie-group optimization on SE(3) — common machinery for pose estimation and calibration solvers.
- Robot pose accuracy vs repeatability — key constraint for non-teaching, vision-guided industrial tasks.
- Calibration data selection — choosing informative, low-uncertainty pose pairs improves calibration accuracy.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H5.** Iteración en el álgebra de Lie para AX=YB que repondera según la incertidumbre relativa entre cinemática y visión.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
