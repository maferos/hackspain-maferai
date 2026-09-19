---
aliases: []
type: "source"
title: "DFVS: Deep Flow Guided Scene Agnostic Image Based Visual Servoing"
citekey: "Harish2020dfvs"
doi: "10.48550/arXiv.2003.03766"
arxiv: "2003.03766"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2003.03766"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Y V S Harish", "Harit Pandya", "Ayush Gaud", "Shreya Terupally", "Sai Shankar", "K. Madhava Krishna"]
sha256: ["33dd92be94662eedffb72ec8d71387354411fbe3c8a4f81f024a936b6cd22348"]
pdf: "Content/Papers/Harish2020dfvs.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 53
---

📄 PDF: [[Harish2020dfvs.pdf]]

> [!abstract] One-sentence summary
> DFVS drives a camera to a goal view by using network-predicted optical flow as image-based visual servoing features combined with network-estimated depth, and introduces a photo-realistic Habitat benchmark on which it converges on all ten scenes where pose-regression and photometric baselines fail on hard ones.

## Abstract

Existing deep learning based visual servoing approaches regress the relative camera pose between a pair of images. Therefore, they require a huge amount of training data and sometimes fine-tuning for adaptation to a novel scene. Furthermore, current approaches do not consider underlying geometry of the scene and rely on direct estimation of camera pose. Thus, inaccuracies in prediction of the camera pose, especially for distant goals, lead to a degradation in the servoing performance. In this paper, we propose a two-fold solution: (i) We consider optical flow as our visual features, which are predicted using a deep neural network. (ii) These flow features are then systematically integrated with depth estimates provided by another neural network using interaction matrix. We further present an extensive benchmark in a photo-realistic 3D simulation across diverse scenes to study the convergence and generalisation of visual servoing approaches. We show convergence for over 3m and 40 degrees while maintaining precise positioning of under 2cm and 1 degree on our challenging benchmark where the existing approaches that are unable to converge for majority of scenarios for over 1.5m and 20 degrees. Furthermore, we also evaluate our approach for a real scenario on an aerial robot. Our approach generalizes to novel scenarios producing precise and robust servoing performance for 6 degrees of freedom positioning tasks with even large camera transformations without any retraining or fine-tuning. (arXiv)

## 🧠 Key ideas (atomic)

- The authors note that [[Image-based visual servoing|image based visual servoing]] is robust to calibration errors but could lead the robot into a local minimum. (Harish et al., 2020) `ev:asserted` p. 1 ^harish2020dfvs-001
- [[Visual servoing|Direct visual servoing]] skips feature extraction, which helps achieve higher goal-reaching precision at the cost of a smaller convergence basin. (Harish et al., 2020) `ev:cited` p. 1 ^harish2020dfvs-002
- [[Visual servoing|Classical visual servoing]] requires knowledge of the environment depth, which is especially difficult to obtain on robots with a monocular camera. (Harish et al., 2020) `ev:asserted` p. 1 ^harish2020dfvs-003
- Saxena et al. used a deep network to estimate relative camera pose from an image pair, then a [[Position-based visual servoing|traditional PBVS controller]]. (Harish et al., 2020) `ev:cited` p. 1 ^harish2020dfvs-004
- The Saxena et al. network, trained on the Microsoft 7 scenes dataset, generalised well to novel environments but had a limited convergence basin. (Harish et al., 2020) `ev:cited` p. 1 ^harish2020dfvs-005
- Bateux et al. estimated relative camera pose with a Siamese network trained on LabelMe images with homography-generated viewpoint variations. (Harish et al., 2020) `ev:cited` p. 1 ^harish2020dfvs-006
- Yu et al. reached sub-millimeter precision with a Siamese network trained only on a table-top scene, so it requires retraining for novel environments. (Harish et al., 2020) `ev:cited` p. 1 ^harish2020dfvs-007
- Several [[Visual servoing|deep reinforcement learning visual servoing approaches]] are specific to manipulation tasks trained only on scenes with objects lying on a table. (Harish et al., 2020) `ev:cited` p. 1 ^harish2020dfvs-008
- The authors state that the cited deep reinforcement learning visual servoing approaches do not consider full 6 degrees of freedom servoing. (Harish et al., 2020) `ev:cited` p. 1 ^harish2020dfvs-009
- Sampedro et al. applied deep reinforcement learning to aerial robot landing on a moving target but reported results for a single scene. (Harish et al., 2020) `ev:cited` p. 1 ^harish2020dfvs-010
- The approach uses a neural network to estimate the optical flow between images, and this flow serves as the visual features for servoing. (Harish et al., 2020) `ev:reported` p. 5 ^harish2020dfvs-011
- The authors present two methods for estimating scene depth, one under a single-view setting and one under a two-view setting. (Harish et al., 2020) `ev:reported` p. 5 ^harish2020dfvs-012
- The predicted flow features are integrated with depth estimates from a second neural network through the interaction matrix of [[Image-based visual servoing|image based servoing]]. (Harish et al., 2020) `ev:abstract` p. 1 ^harish2020dfvs-013
- According to the abstract, existing approaches are unable to converge for the majority of scenarios beyond 1.5m and 20 degrees. (Harish et al., 2020) `ev:abstract` p. 1 ^harish2020dfvs-014
- According to the abstract, the approach converges for camera transformations of over 3m and 40 degrees on the proposed benchmark. (Harish et al., 2020) `ev:abstract` p. 1 ^harish2020dfvs-015
- According to the abstract, the approach maintains final positioning precision under 2cm and 1 degree on the proposed benchmark. (Harish et al., 2020) `ev:abstract` p. 1 ^harish2020dfvs-016
- The proposed simulation benchmark consists of 10 indoor photo-realistic environments taken from the Habitat simulation engine. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-017
- Benchmark scenes were selected to cover different textures and a variable number of objects, each with one initial and one desired pose. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-018
- Benchmark tasks are classified as easy, medium or hard according to texture amount, image overlap and rotational and translational complexity. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-019
- Easy benchmark tasks contain many distinctive objects with mostly translational motion around 1.4m and small rotation around 15°. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-020
- Medium benchmark tasks contain fewer objects, with rotation near 20° and translation near 1.5m between initial and desired images. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-021
- Hard benchmark tasks have rotation of at least 30° or translation of at least 2m, giving less overlap between images. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-022
- The benchmark evaluates servoing with final translation error, final rotation error, trajectory length and number of iterations as metrics. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-023
- On the benchmark, the Saxena et al. approach converges on easy and medium scenes but has difficulty on hard scenes. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-024
- [[Visual servoing|Photometric visual servoing]] using true depth from the depth sensor is not able to converge in most of the benchmark environments. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-025
- With depth predicted by either the single-view or two-view pipeline, pose error after convergence is on par with ground truth depth. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-026
- The reported mean error of the approach after convergence is 0.025 cm and 1.167 degrees over 10 different benchmark scenes. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-027
- The reported initial mean pose error over the 10 benchmark scenes is 1.76 cm and 22.89 degrees. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-028
- Both photometric visual servoing and the Saxena et al. approach fail to converge on more than half of the benchmark scenarios. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-029
- True-depth simulations were stopped without reaching 100 % convergence, since the authors only wanted to know the precision reachable with true depth. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-030
- In a controller trial on a hard scene, both the flow-depth and depth-network variants converge without any oscillations. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-031
- In the same controller trial, photometric visual servoing and the Saxena et al. approach both diverge from the desired pose. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-032
- In the controller trial, the flow-depth approach takes longer to converge than the depth-network approach. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-033
- In the controller trial, the flow-depth approach produces a much shorter trajectory than the depth-network approach. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-034
- The convergence study increased the distance between initial and desired images in each axis by 0.4 meters up to 4 meters. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-035
- Rotations in the convergence study used three set-points: [10°,10°,25°], [20°,20°,40°] and [30°,30°,50°] in x, y, z. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-036
- Each convergence-study batch used 16 environments randomly selected from the Gibson dataset, with a fixed initial position and varied desired position. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-037
- Convergence was defined as a final translation error less than 4 cm and a final rotation error less than 1°. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-038
- For the Bateux et al. approach, the convergence ratio drastically drops to about 65 percent in the convergence study. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-039
- The flow-depth pipeline shows a convergence ratio of about 90 percent for the [20°,20°,40°] case, with a convergence basin up to 4m. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-040
- For the [30°,30°,50°] rotational change, the approach converges in over 75 percent of cases in most batches. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-041
- In the convergence study, the Bateux et al. approach falls to 40 percent convergence at [20°,20°,50°]. (Harish et al., 2020) `ev:measured` p. 4 ^harish2020dfvs-042
- The real-world validation used a Parrot Bebop-2 drone in an outdoor scenario, without fine-tuning or retraining the networks. (Harish et al., 2020) `ev:reported` p. 4 ^harish2020dfvs-043
- The drone task involved a camera transformation of [0.29, 0.39, 1.27] m in translation between the initial and desired images. (Harish et al., 2020) `ev:reported` p. 5 ^harish2020dfvs-044
- The outdoor drone task involved a camera rotation of [-25.63°,-25.63°,-10.56°] between the initial and desired images. (Harish et al., 2020) `ev:reported` p. 5 ^harish2020dfvs-045
- Qualitatively, the drone smoothly attains the desired pose even with constant illumination variations in the outdoor scenario. (Harish et al., 2020) `ev:measured` p. 5 ^harish2020dfvs-046
- Only qualitative results are presented for the drone experiment because of erroneous odometry of the robot. (Harish et al., 2020) `ev:reported` p. 5 ^harish2020dfvs-047
- In the qualitative benchmark results, all three variants of the approach converge on all ten test cases, including hard scenes. (Harish et al., 2020) `ev:measured` p. 5 ^harish2020dfvs-048
- The authors conclude that their approach showcases precise servoing with a large convergence basin across diverse environments without retraining. (Harish et al., 2020) `ev:asserted` p. 5 ^harish2020dfvs-049
- In Table I, flow-depth final translation errors range from 0.02 to 0.041 m across the ten benchmark scenes. (Harish et al., 2020) `ev:measured` p. 6 ^harish2020dfvs-050
- In Table I, photometric visual servoing ends with rotation errors of 39.65, 43.37 and 53.246 degrees on three hard scenes. (Harish et al., 2020) `ev:measured` p. 6 ^harish2020dfvs-051
- In Table I, the flow-depth variant needs 3831 iterations on one scene, compared with 104 for the true-depth variant. (Harish et al., 2020) `ev:measured` p. 6 ^harish2020dfvs-052
- On one hard scene in Table I, the true-depth variant ends with 11.67 degrees rotation error, versus 0.55 for flow-depth. (Harish et al., 2020) `ev:measured` p. 6 ^harish2020dfvs-053

## 🎯 Contributions

## 📖 Glossary

- **Visual servoing** — Controlling a robot toward a desired pose using image measurements from a camera.
- **PBVS** — Pose based visual servoing; minimizes estimated pose difference in 3D Cartesian space.
- **IBVS** — Image based visual servoing; minimizes feature error directly in image space.
- **Interaction matrix** — Jacobian linking image feature motion to camera velocity; needs scene depth.
- **Photometric visual servoing** — Direct servoing that uses raw image intensities as features.
- **Convergence basin** — Range of initial pose offsets from which the servoing reaches the goal.
- **Convergence ratio** — Fraction of trials reaching the goal within the translation and rotation thresholds.

## ❓ Open questions

- How accurate is the drone positioning quantitatively once reliable odometry or external ground truth is available?
- How much does flow-depth iteration count (up to 3831) matter for real-time control on hardware?
- Why does the true-depth variant leave 11.67 degrees rotation error on one hard scene while network depth does not?
- Does the approach hold under dynamic scenes, occlusions or large appearance changes beyond illumination?
- How do single-view and two-view depth estimation compare in accuracy and failure modes?

## 📝 Notes on reading

- The cached text has no content for pages 2 and 3, so the method section (flow network, depth networks, control law, possibly FlowNet 2.0 [16] and DenseDepth [17]) was not read; method claims rest on the abstract and conclusion only.
- Figures 5, 6 and 7 are plots/photos extracted as garbled glyphs; only their captions were used. Fig. 6 plots convergence ratio versus translation for three rotation set-points.
- Table I (p. 6) is extracted as a column stream; its row-to-scene assignment was inferred from the order of values (10 scenes x metrics T. err, R. err, Tj. len, Iter; columns I. err, [3], [4], T.depth, D.net, F.depth). In the last scene the values 36.05 53.246 29.24 appear on one line.
- Unit inconsistency: the text (p. 4) gives mean final error 0.025 cm and initial mean error 1.76 cm, whereas Table I reports translation errors in meters (for example I. err 1.42 to 2.54); the cm values are probably meters.
- Inconsistency: the convergence study (p. 4) lists set-points [10°,10°,25°], [20°,20°,40°], [30°,30°,50°], but reports Bateux et al. dropping to 40 percent at [20°,20°,50°]; the Bateux drop to 65 percent is stated around 2.4cm, 12° in x and y and 1.2cm, 30° in z, units that look inconsistent with the 0.4 m steps.
- The abstract claims positioning under 2cm and 1 degree, while Table I shows several final rotation errors above 1 degree (for example 8.39 for flow-depth in one scene).
- Version read: arXiv preprint 2003.03766.

## Suggested new concepts

- Optical-flow-based visual servoing — dense learned flow as IBVS features is a recurring alternative to pose regression.
- Learned monocular depth for servoing — depth networks replacing depth sensors in the interaction matrix is a reusable design choice.
- Visual servoing benchmark in photo-realistic simulation — Habitat/Gibson scenes as standard test-beds for generalisation of servoing methods.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Flujo aprendido más matriz de interacción

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
