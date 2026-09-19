---
aliases: []
type: "source"
title: "Direct Sparse Odometry"
citekey: "Engel2016direct"
doi: "10.48550/arXiv.1607.02565"
arxiv: "1607.02565"
year: 2016
publication_type: "preprint"
url: "https://arxiv.org/abs/1607.02565"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Jakob Engel", "Vladlen Koltun", "Daniel Cremers"]
sha256: ["cd85260a38b0b5d0e82c85c37c3540c498a953e39a501d9af5192a35b8284223"]
pdf: "Content/Papers/Engel2016direct.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 58
---

📄 PDF: [[Engel2016direct.pdf]]

> [!abstract] One-sentence summary
> DSO is a monocular visual odometry method that jointly optimizes a photometric error over a sparse, evenly sampled set of pixels with full photometric calibration, outperforming ORB-SLAM on TUM-monoVO and ICL-NUIM while being more sensitive to geometric noise such as rolling shutter.

## Abstract

We propose a novel direct sparse visual odometry formulation. It combines a fully direct probabilistic model (minimizing a photometric error) with consistent, joint optimization of all model parameters, including geometry -- represented as inverse depth in a reference frame -- and camera motion. This is achieved in real time by omitting the smoothness prior used in other direct methods and instead sampling pixels evenly throughout the images. Since our method does not depend on keypoint detectors or descriptors, it can naturally sample pixels from across all image regions that have intensity gradient, including edges or smooth intensity variations on mostly white walls. The proposed model integrates a full photometric calibration, accounting for exposure time, lens vignetting, and non-linear response functions. We thoroughly evaluate our method on three different datasets comprising several hours of video. The experiments show that the presented approach significantly outperforms state-of-the-art direct and indirect methods in a variety of real-world settings, both in terms of tracking accuracy and robustness. (arXiv)

## 🧠 Key ideas (atomic)

- The proposed sparse-direct formulation optimizes a photometric error defined directly on the images, without incorporating any geometric prior (Engel et al., 2016) `ev:asserted` p. 2 ^engel2016direct-001
- Jin et al. already proposed a sparse direct formulation in 2003, which was based on an extended Kalman filter (Engel et al., 2016) `ev:cited` p. 2 ^engel2016direct-002
- Sparse indirect methods such as ORB-SLAM estimate 3D geometry from keypoint matches using a geometric error without geometry prior (Engel et al., 2016) `ev:cited` p. 2 ^engel2016direct-003
- Adding a geometry prior introduces correlations between geometry parameters, which render statistically consistent joint optimization in real time infeasible (Engel et al., 2016) `ev:asserted` p. 3 ^engel2016direct-004
- The authors found that geometry priors can introduce a bias, thereby reducing rather than increasing long-term, large-scale accuracy (Engel et al., 2016) `ev:asserted` p. 3 ^engel2016direct-005
- The authors describe DSO as, to their knowledge, the only fully direct method jointly optimizing the full likelihood for all model parameters (Engel et al., 2016) `ev:asserted` p. 3 ^engel2016direct-006
- Optimization runs in a sliding window where old camera poses, as well as points leaving the field of view, are marginalized (Engel et al., 2016) `ev:reported` p. 3 ^engel2016direct-007
- With reduced settings, DSO still outperforms state-of-the-art indirect methods when running at 5× real-time speed, the authors report (Engel et al., 2016) `ev:measured` p. 3 ^engel2016direct-008
- On high, non-real-time settings, DSO creates semi-dense models that are similar in density to those of LSD-SLAM (Engel et al., 2016) `ev:measured` p. 3 ^engel2016direct-009
- 3D points are represented as inverse depth in a reference frame, so each point has one degree of freedom (Engel et al., 2016) `ev:reported` p. 3 ^engel2016direct-010
- In an example sequence spanning indoor to outdoor scenes, exposure time varied by a factor of more than 500, from 0.018 to 10.5ms (Engel et al., 2016) `ev:measured` p. 4 ^engel2016direct-011
- The method is formulated for the pinhole camera model, with radial distortion removed in a preprocessing step (Engel et al., 2016) `ev:reported` p. 4 ^engel2016direct-012
- Each frame is photometrically corrected as the very first step, using the inverse response function divided by lens attenuation (Engel et al., 2016) `ev:reported` p. 4 ^engel2016direct-013
- The photometric error of a point is a weighted SSD over a small neighborhood of 8 pixels arranged in a slightly spread pattern (Engel et al., 2016) `ev:reported` p. 4 ^engel2016direct-014
- An affine brightness transfer function with logarithmically parametrized scale allows operation on sequences without known exposure times (Engel et al., 2016) `ev:reported` p. 5 ^engel2016direct-015
- A point is parametrized by one parameter, its inverse depth in the reference frame, in contrast to three unknowns in indirect models (Engel et al., 2016) `ev:asserted` p. 5 ^engel2016direct-016
- Following Leutenegger et al., the total photometric error is optimized in a sliding window using the Gauss-Newton algorithm (Engel et al., 2016) `ev:reported` p. 6 ^engel2016direct-017
- First Estimate Jacobians are used to maintain consistency, because adding linearizations around different evaluation points eliminates non-linear null-spaces (Engel et al., 2016) `ev:reported` p. 6 ^engel2016direct-018
- The geometric Jacobian is evaluated only for the center pixel of each point, without notable observed effect on accuracy on the used datasets (Engel et al., 2016) `ev:measured` p. 6 ^engel2016direct-019
- DSO keeps a window of up to Nf active keyframes, using Nf = 7 by default (Engel et al., 2016) `ev:reported` p. 7 ^engel2016direct-020
- If a frame's final RMSE exceeds twice that of the previous frame, recovery tries up to 27 small rotations, each taking approximately 0.5ms (Engel et al., 2016) `ev:reported` p. 8 ^engel2016direct-021
- Frames with less than 5% of their points visible in the newest keyframe are marginalized (Engel et al., 2016) `ev:reported` p. 8 ^engel2016direct-022
- Dropping observations of remaining points when marginalizing a keyframe discards about half of all residuals in practice, which the authors call suboptimal (Engel et al., 2016) `ev:measured` p. 8 ^engel2016direct-023
- DSO aims to keep a fixed number of Np = 2000 active points in the optimization, equally distributed across space (Engel et al., 2016) `ev:reported` p. 9 ^engel2016direct-024
- Candidate points are selected with a region-adaptive gradient threshold, computed per 32 × 32 block as median absolute gradient plus gth = 7 (Engel et al., 2016) `ev:reported` p. 9 ^engel2016direct-025
- Two further passes with decreased gradient threshold at block-sizes 2d then 4d add weaker-gradient points, capturing weak intensity variations such as those on white walls (Engel et al., 2016) `ev:reported` p. 9 ^engel2016direct-026
- The TUM monoVO dataset provides 50 photometrically calibrated sequences comprising 105 minutes of video recorded in dozens of different environments (Engel et al., 2016) `ev:reported` p. 10 ^engel2016direct-027
- The EuRoC MAV dataset contains 11 stereo-inertial sequences comprising 19 minutes of video, without photometric calibration or exposure times (Engel et al., 2016) `ev:reported` p. 10 ^engel2016direct-028
- The ICL-NUIM dataset contains 8 ray-traced sequences comprising 4.5 minutes of video from two indoor environments (Engel et al., 2016) `ev:reported` p. 10 ^engel2016direct-029
- In total the evaluation comprises 500 runs on TUM-monoVO, 220 runs on EuRoC MAV, plus 80 runs on ICL-NUIM (Engel et al., 2016) `ev:reported` p. 10 ^engel2016direct-030
- Evaluation against the open-source LSD-SLAM or SVO implementations was attempted, but both methods consistently fail on most of the sequences (Engel et al., 2016) `ev:measured` p. 11 ^engel2016direct-031
- The direct sparse approach clearly outperforms ORB-SLAM in accuracy on the TUM-monoVO dataset as well as the synthetic ICL-NUIM dataset (Engel et al., 2016) `ev:measured` p. 11 ^engel2016direct-032
- The direct sparse approach clearly outperforms ORB-SLAM in robustness on the TUM-monoVO dataset as well as the synthetic ICL-NUIM dataset (Engel et al., 2016) `ev:measured` p. 11 ^engel2016direct-033
- On the EuRoC MAV dataset, ORB-SLAM achieves a better accuracy than DSO, but with lower robustness (Engel et al., 2016) `ev:measured` p. 11 ^engel2016direct-034
- The authors attribute ORB-SLAM's better EuRoC accuracy partly to many small loops that its local mapping component implicitly closes (Engel et al., 2016) `ev:asserted` p. 11 ^engel2016direct-035
- When restricted to keypoints observed within the last tmax = 10s, ORB-SLAM performs similar to DSO in accuracy but is less robust (Engel et al., 2016) `ev:measured` p. 12 ^engel2016direct-036
- The 5× real-time setting reduces to Np=800 points, Nf=6 active frames, 424×320 resolution, at most 4 Gauss-Newton iterations per keyframe (Engel et al., 2016) `ev:reported` p. 12 ^engel2016direct-037
- DSO is a pure visual odometry, whereas ORB-SLAM is a full SLAM system whose additional abilities were neglected or switched off in this comparison (Engel et al., 2016) `ev:asserted` p. 12 ^engel2016direct-038
- Known exposure times seem to have little effect on accuracy when photometric calibration components are incrementally disabled on TUM-monoVO (Engel et al., 2016) `ev:measured` p. 13 ^engel2016direct-039
- Removing vignette together with response calibration slightly decreases the overall accuracy on the TUM-monoVO dataset (Engel et al., 2016) `ev:measured` p. 13 ^engel2016direct-040
- A naïve brightness constancy assumption, as used in LSD-SLAM or SVO, clearly performs worst because it does not account for automatic exposure changes (Engel et al., 2016) `ev:measured` p. 13 ^engel2016direct-041
- The benefit of using more active points quickly flattens off after Np = 500 points on the TUM-monoVO dataset (Engel et al., 2016) `ev:measured` p. 13 ^engel2016direct-042
- The number of active frames has little influence after Nf = 7 in the parameter study on the TUM-monoVO dataset (Engel et al., 2016) `ev:measured` p. 13 ^engel2016direct-043
- A fixed-lag marginalization strategy that always marginalizes the oldest keyframe, instead of using the distance score, performs significantly worse (Engel et al., 2016) `ev:measured` p. 13 ^engel2016direct-044
- The gradient threshold for point selection seems to have a sweet spot around gth = 7, though its overall impact is relatively low (Engel et al., 2016) `ev:measured` p. 13 ^engel2016direct-045
- Restricting point candidates to FAST corners only significantly decreases performance compared with the default gradient-based point selection (Engel et al., 2016) `ev:measured` p. 13 ^engel2016direct-046
- The default setting Tkf = 1 results in 8 keyframes per second, which is easily achieved in real time (Engel et al., 2016) `ev:measured` p. 14 ^engel2016direct-047
- Taking fewer than 4 keyframes per second reduces robustness, mainly in situations with strong occlusions or dis-occlusions, such as walking through doors (Engel et al., 2016) `ev:measured` p. 14 ^engel2016direct-048
- Taking more than 15 keyframes per second decreases accuracy, because keyframes are then marginalized earlier, accumulating linearizations around less accurate points (Engel et al., 2016) `ev:measured` p. 14 ^engel2016direct-049
- DSO's performance quickly deteriorates with added geometric noise, whereas ORB-SLAM is much less affected on the TUM-monoVO dataset (Engel et al., 2016) `ev:measured` p. 14 ^engel2016direct-050
- For δg > 1.5 there likely exists no state with all residuals within the linearization validity radius, so optimization fails entirely (Engel et al., 2016) `ev:asserted` p. 15 ^engel2016direct-051
- This result suggests the direct model is more susceptible to inaccurate intrinsic camera calibration than the indirect approach (Engel et al., 2016) `ev:asserted` p. 15 ^engel2016direct-052
- DSO is slightly more robust than ORB-SLAM to photometric noise simulated as added blur on the TUM-monoVO dataset (Engel et al., 2016) `ev:measured` p. 15 ^engel2016direct-053
- The authors argue the indirect model is superior for smartphones or off-the-shelf webcams, designed to capture videos for human consumption (Engel et al., 2016) `ev:asserted` p. 15 ^engel2016direct-054
- The authors argue the direct approach offers superior performance on data captured with dedicated cameras for machine vision (Engel et al., 2016) `ev:asserted` p. 15 ^engel2016direct-055
- The parameter study indicates that simply using more data does not increase tracking accuracy, although it makes the 3D models denser (Engel et al., 2016) `ev:asserted` p. 16 ^engel2016direct-056
- The authors believe differing noise robustness is one main explanation for the recent revival of direct formulations after a decade of indirect dominance (Engel et al., 2016) `ev:asserted` p. 16 ^engel2016direct-057
- The main challenge is greatly increased non-convexity from including the image in the error function, which is likely to restrict the model to video processing (Engel et al., 2016) `ev:asserted` p. 16 ^engel2016direct-058

## 🎯 Contributions

## 📖 Glossary

- **Direct method** — Visual odometry that optimizes a photometric error on raw pixel intensities instead of keypoints.
- **Indirect method** — Method that first extracts correspondences, then optimizes a geometric (reprojection) error.
- **Sparse method** — Uses and reconstructs only a selected set of independent points, without geometry prior.
- **Photometric calibration** — Model of response function, vignetting and exposure mapping irradiance to pixel intensity.
- **Inverse depth** — Point parametrization by reciprocal depth along a reference-frame pixel ray.
- **Marginalization** — Removing old variables via the Schur complement while keeping their information as a prior.
- **First Estimate Jacobians** — Evaluating Jacobians at a fixed linearization point to preserve null-spaces and consistency.
- **Absolute trajectory error (eate)** — Translational RMSE of the trajectory after Sim(3) alignment.
- **Alignment error (ealign)** — TUM-monoVO drift metric computed from loop-closure ground truth.

## ❓ Open questions

- Would tightly integrating a rolling-shutter model close the gap to indirect methods on commodity cameras?
- How much would tightly coupled IMU integration improve pose initialization and remove the recovery-tracking step?
- Can the direct sparse energy be integrated into iSAM or double-window bundle adjustment despite its higher non-convexity?
- Could learned, unbiased geometry priors improve long-term accuracy rather than degrade it?
- How does DSO compare once loop closure is added, versus full ORB-SLAM with loop closure enabled?
- How does performance change with other (invertible) camera models instead of pinhole-rectified images?

## 📝 Notes on reading

Read the arXiv preprint v2 (7 Oct 2016), matching the packet identifier.

Figures 10 and 12-21 are cumulative error plots whose axes and legends were extracted as number lists; results were taken only from the text and captions. The legend of Figure 12 is garbled in extraction ('secret Message e′ s (multiplier)').

Inconsistency: the methodology says all sequences are run forwards and backwards '5 times each', then 'we run each method 10 times each'; Figures 13 and 14 say 10 times each, while the stated total of 500 TUM-monoVO runs (50 sequences × 2 directions) matches 5 runs per direction. The per-sequence repetition count was not claimed.

Inconsistency: the text says Tkf = 1 gives 8 keyframes per second, while Figure 18's legend lists x1 as approximately 7.5 KF/s.

The abstract says DSO outperforms state-of-the-art direct and indirect methods, but in the body direct baselines (LSD-SLAM, SVO) were not quantitatively compared because they failed on most sequences; on EuRoC ORB-SLAM is more accurate.

The equations (photometric error, Gauss-Newton system, Schur complement marginalization) are partly garbled in extraction and were described rather than transcribed.

## Suggested new concepts

- Direct vs. indirect visual odometry — the paper's taxonomy (sparse/dense × direct/indirect) is a recurring framing across SLAM literature.
- Photometric camera calibration — response, vignetting and exposure modelling is reused by later direct methods and datasets.
- Sliding-window marginalization — the Schur-complement windowed optimization with First Estimate Jacobians is a shared VO/VIO building block.
- Rolling-shutter sensitivity of direct methods — a limitation relevant when choosing cameras for vision pipelines.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Odometría directa fotométrica en $SE(3)$

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
