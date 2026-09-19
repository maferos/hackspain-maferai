---
aliases: []
type: "source"
title: "6-PACK: Category-level 6D Pose Tracker with Anchor-Based Keypoints"
citekey: "Wang2019pack"
doi: "10.48550/arXiv.1910.10750"
arxiv: "1910.10750"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1910.10750"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Chen Wang", "Roberto Martín-Martín", "Danfei Xu", "Jun Lv", "Cewu Lu", "Li Fei-Fei", "Silvio Savarese", "Yuke Zhu"]
sha256: ["33b540fc821ba0f49afcca19bd8d99b5120078c9874e60bd92248fd52376d470"]
pdf: "Content/Papers/Wang2019pack.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 66
---

📄 PDF: [[Wang2019pack.pdf]]

> [!abstract] One-sentence summary
> 6-PACK tracks the 6D pose of unseen instances of known categories from RGB-D video by matching a few unsupervised, anchor-based 3D keypoints between frames, clearly beating NOCS, ICP and KeypointNet on NOCS-REAL275 and running at 10 Hz on a real robot.

## Abstract

We present 6-PACK, a deep learning approach to category-level 6D object pose tracking on RGB-D data. Our method tracks in real-time novel object instances of known object categories such as bowls, laptops, and mugs. 6-PACK learns to compactly represent an object by a handful of 3D keypoints, based on which the interframe motion of an object instance can be estimated through keypoint matching. These keypoints are learned end-to-end without manual supervision in order to be most effective for tracking. Our experiments show that our method substantially outperforms existing methods on the NOCS category-level 6D pose estimation benchmark and supports a physical robot to perform simple vision-based closed-loop manipulation tasks. Our code and video are available at https://sites.google.com/view/6packtracking. (arXiv)

## 🧠 Key ideas (atomic)

- 6-PACK is a deep learning approach that tracks the 6D pose of novel instances of known object categories from RGB-D data. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019pack-001
- The method represents an object compactly by a handful of 3D keypoints learned end-to-end without manual supervision. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019pack-002
- Assuming a known 3D model can be brittle in realistic settings where perfect geometry of novel objects is hard to acquire. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019pack-003
- NOCS estimates category-level 6D pose from RGB-D images by transforming every object pixel to [[Normalized Object Coordinate Space|a shared coordinate frame]] as keypoints. (Wang et al., 2019) `ev:cited` p. 1 ^wang2019pack-004
- The authors argue that estimating poses from many crude keypoints makes NOCS susceptible to noise from clutter and occlusion. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019pack-005
- Tracking-by-detection methods such as NOCS cannot leverage temporal information from previous frames, according to the authors. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019pack-006
- 6-PACK estimates object pose by accumulating relative pose changes over time, without requiring a known 3D model. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019pack-007
- An anchor mechanism analogous to 2D detection proposals lets 6-PACK avoid defining and estimating the absolute 6D pose. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019pack-008
- 6-PACK substantially outperforms all baselines on the recently introduced NOCS-REAL275 dataset in category-level 6D tracking. (Wang et al., 2019) `ev:measured` p. 2 ^wang2019pack-009
- Supervised keypoint learning requires large amounts of labelled data, which the authors list as a limitation of prior category-level methods. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019pack-010
- Manually annotated keypoints or bounding box corners may not be the optimal landmarks to track, according to the authors. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019pack-011
- The authors attribute KeypointNet's failure on real data to training on single object models centered at the coordinate origin. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019pack-012
- The anchoring mechanism lets the model generate keypoints only in the most relevant subspace of the 3D scene. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019pack-013
- Category-level 6D pose tracking is defined as continuously estimating the object's change of pose between consecutive timesteps, given its initial pose and category. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019pack-014
- The absolute pose is retrieved by recursively applying each estimated change of pose to the previous pose, starting from the initial pose. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019pack-015
- Given matching keypoint lists from two consecutive frames, the change of pose is recovered by least-squares point set alignment under a rigid-body assumption. (Wang et al., 2019) `ev:reported` p. 2 ^wang2019pack-016
- Each anchor summarizes its surrounding volume with a distance-weighted sum of the features of nearby RGB-D points. (Wang et al., 2019) `ev:reported` p. 3 ^wang2019pack-017
- Searching keypoints around a coarse object centroid is more efficient than searching the entire unconstrained 3D space, the authors state. (Wang et al., 2019) `ev:asserted` p. 3 ^wang2019pack-018
- Based on the estimated inter-frame motion, 6-PACK extrapolates the pose in the next frame to center the next distribution of anchor points. (Wang et al., 2019) `ev:reported` p. 3 ^wang2019pack-019
- To reject initial pose errors, 6-PACK repeats keypoint generation and pose correction a total of T = 10 times. (Wang et al., 2019) `ev:reported` p. 3 ^wang2019pack-020
- The initialization procedure reduces the effort of providing a very accurate initial pose to the category-level tracker, the authors state. (Wang et al., 2019) `ev:asserted` p. 3 ^wang2019pack-021
- A DenseFusion-based network computes fused geometric and color features for the M points inside a cropped, enlarged volume around the predicted pose. (Wang et al., 2019) `ev:reported` p. 3 ^wang2019pack-022
- Anchor weights are a softmax over point distances, used for distance-weighted average pooling of DenseFusion point embeddings into anchor embeddings. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019pack-023
- A two-layer MLP attention network is trained with supervision to give the highest confidence score to the anchor closest to the object centroid. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019pack-024
- A keypoint generation network maps the selected anchor feature to a K × 3 output forming an ordered list of keypoints. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019pack-025
- Because the keypoint list is ordered, no correspondence search between keypoints of consecutive frames is needed to estimate the pose change. (Wang et al., 2019) `ev:asserted` p. 4 ^wang2019pack-026
- The unsupervised keypoint training optimizes a multi-view consistency loss that matches current keypoints to previous keypoints transformed by ground-truth inter-frame motion. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019pack-027
- Multi-view consistency alone does not guarantee useful keypoints for pose estimation, since all keypoints could end up at the same location. (Wang et al., 2019) `ev:asserted` p. 4 ^wang2019pack-028
- The separation loss, defined by Suwajanakorn et al., forces keypoints to keep some distance from each other to avoid degenerate configurations. (Wang et al., 2019) `ev:cited` p. 4 ^wang2019pack-029
- A centroid loss forces the centroid of the generated keypoints onto the object centroid, helping correct noise in the initial pose. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019pack-030
- The overall training loss is a weighted sum of the 6 terms, weighted by their relative magnitude and importance. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019pack-031
- The multi-view consistency and pose losses do not handle symmetric categories well, since rotation along a symmetry axis cannot be identified. (Wang et al., 2019) `ev:asserted` p. 4 ^wang2019pack-032
- For symmetric categories, keypoints are mapped to rotation-invariant coordinates: distance to the symmetry axis, height along it, and relative inter-keypoint angle. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019pack-033
- For symmetric categories, the rotation loss becomes the angular difference between predicted and ground-truth changes in the symmetry axis orientation. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019pack-034
- The authors describe NOCS-REAL275 as the only real-world benchmark dataset for category-level object 6D pose tracking. (Wang et al., 2019) `ev:asserted` p. 5 ^wang2019pack-035
- NOCS-REAL275 contains six categories: bottle, bowl, camera, can, laptop and mug, three of which have axes of symmetry. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019pack-036
- The training set has 275K synthetic frames generated from 1085 ShapeNetCore instance models with random poses, plus seven real videos. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019pack-037
- The test set has six real videos showing three unseen instances per object category, with 3,200 frames in total. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019pack-038
- Evaluation uses the 5°5 cm success percentage, the IoU25 percentage, and mean rotation and translation errors in degrees and centimeters. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019pack-039
- The KeypointNet baseline is an implementation of 6-PACK without the anchor-based attention mechanism, generating keypoints directly in 3D space. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019pack-040
- The full 6-PACK predicts the next-frame pose by extrapolating the last estimated inter-frame pose change with a constant velocity model. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019pack-041
- The ablation without temporal prediction simply uses the previous estimated pose as the predicted pose in the next frame. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019pack-042
- To test robustness to noisy initialization, up to 4cm of uniformly sampled random translation noise was injected into initial poses. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019pack-043
- Robustness to missing frames was measured by uniformly dropping 450 of the 3200 frames from the testing videos. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019pack-044
- 6-PACK outperforms the second-best method, NOCS, by more than 15% in the 5°5 cm metric on NOCS-REAL275. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019pack-045
- 6-PACK outperforms NOCS by 12% in the IoU25 metric on the NOCS-REAL275 testing set of six categories. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019pack-046
- Overall on NOCS-REAL275, 6-PACK reaches 33.3 in the 5°5cm metric, versus 17.0 for NOCS and 16.9 for ICP. (Wang et al., 2019) `ev:measured` p. 5 ^wang2019pack-047
- Overall on NOCS-REAL275, 6-PACK has a mean rotation error of 16.0 degrees, compared with 20.2 for NOCS. (Wang et al., 2019) `ev:measured` p. 5 ^wang2019pack-048
- Overall on NOCS-REAL275, 6-PACK has a mean translation error of 3.5 centimeters, compared with 4.9 for NOCS. (Wang et al., 2019) `ev:measured` p. 5 ^wang2019pack-049
- Overall IoU25 is 94.2 for 6-PACK, slightly below 95.1 for the variant without temporal prediction. (Wang et al., 2019) `ev:measured` p. 5 ^wang2019pack-050
- Temporal prediction raises overall 5°5cm from 32.5 for the variant without it to 33.3 for full 6-PACK. (Wang et al., 2019) `ev:measured` p. 5 ^wang2019pack-051
- On the bowl category in Table I, NOCS scores 62.2 in 5°5cm, higher than 55.0 for 6-PACK. (Wang et al., 2019) `ev:measured` p. 5 ^wang2019pack-052
- KeypointNet frequently loses track of the object, 50.3% across the evaluation set, as revealed by the IoU25 metric. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019pack-053
- According to the authors, 6-PACK avoids losing track of category instances in the evaluation, with IoU25 above 94%. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019pack-054
- Performance of all methods decreases when early frames are excluded, except NOCS, which is a pose estimator rather than a tracker. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019pack-055
- When early frames are excluded, 6-PACK stays more than 10% higher than NOCS in 5°5 cm success throughout the sequence. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019pack-056
- 6-PACK performance drops by only 5% when the first 75 frames are excluded from the success computation. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019pack-057
- On the laptop category, 8 keypoints reach 62.4% in 5°5cm, surpassing 55.2% for 4 keypoints and 48.6% for 16. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019pack-058
- The authors conclude that 8 keypoints offer the best trade-off between information compression and redundancy. (Wang et al., 2019) `ev:asserted` p. 6 ^wang2019pack-059
- The robot platform is a Toyota HSR with an Asus Xtion RGB-D sensor, a holonomic mobile base, and a two-finger gripper. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019pack-060
- On the robot setup, 6-PACK tracks poses at 10 Hz using less than 30% of the GPU storage, around 2 GB. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019pack-061
- An initial coarse pose is obtained by detecting a checkerboard placed to delimit the front face of a bounding box around the target. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019pack-062
- Robot tracking was tested on bowl with 4 instances, bottle with 3, laptop with 2, and can with 2. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019pack-063
- For bowl and bottle, the robot performed a pouring or tossing manipulation task based on tracking at the end of the sequence. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019pack-064
- In the robot tests, 6-PACK tracked the objects without loss in more than 60% of the trials. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019pack-065
- The authors conclude that 6-PACK achieves state-of-the-art performance on a challenging category-based 6D object pose tracking benchmark. (Wang et al., 2019) `ev:asserted` p. 7 ^wang2019pack-066

## 🎯 Contributions

## 📖 Glossary

- **Category-level 6D tracking** — tracking position and orientation of unseen instances of a known object category.
- **Anchor** — grid point around the predicted object location carrying a pooled local RGB-D feature.
- **Multi-view consistency loss** — penalizes keypoints that do not follow the ground-truth inter-frame motion.
- **5°5 cm** — percentage of estimates with rotation error below 5° and translation error below 5 cm.
- **IoU25** — percentage of predictions whose 3D box overlap with ground truth exceeds 25%.
- **NOCS** — category-level pose estimator mapping each object pixel to a normalized canonical coordinate space.
- **DenseFusion** — network fusing per-point color and geometry features for 6D pose estimation.
- **Symmetry-invariant coordinates** — (d, h, θ) keypoint coordinates unaffected by rotation around a symmetry axis.

## ❓ Open questions

- Why does full 6-PACK fall below NOCS on bowl in 5°5cm, and is this linked to the symmetry handling?
- How does tracking behave over sequences much longer than the NOCS-REAL275 test videos, given that pose errors accumulate recursively?
- Can the tracker recover after losing an object (under 60% loss-free robot trials leaves many failures)?
- How does the method extend to categories with no single common symmetry axis or to articulated objects?
- How sensitive is performance to the number of keypoints for categories other than laptop?
- How would 6-PACK perform with an automatic detector for initialization instead of a checkerboard or ground-truth pose?

## 📝 Notes on reading

Version read: arXiv 1910.10750v1 (23 Oct 2019), matching the packet identifier.

Table I (p. 5) was extracted as a single column of values; it was read in column order NOCS, ICP, KeypointNet, Ours w/o temporal, Ours, per category and metric (5°5cm, IoU25, Rerr, Terr). Only overall rows and a few per-category rows were claimed.

Fig. 4 (p. 6) axis labels are garbled in extraction; only its caption was used. The caption says initial poses carry translation noise between ±2 cm, while the text on p. 6 says up to 4cm of noise is injected; these are compatible as a range but stated differently.

The 8-keypoint laptop result on p. 6 (62.4%) equals the Table I laptop entry for Ours w/o temporal (62.4), not the full model (63.5).

The text says KeypointNet loses track 50.3% across the evaluation set, while Table I gives KeypointNet an overall IoU25 of 53.0; the 50.3% figure is not directly derivable from the table.

The headline gain of more than 15% over NOCS in 5°5 cm corresponds to 33.3 vs 17.0 in Table I, an absolute difference in percentage points.

The introduction cites Generalized-ICP [40] as the registration baseline, while the baselines list cites point-to-plane ICP in Open3D [50]. The text refers to Fig. IV-B for the symmetry figure, which is Fig. 3.

## Suggested new concepts

- Category-level 6D pose tracking — a distinct problem setting from instance-level tracking and from per-frame category-level pose estimation.
- Unsupervised 3D keypoint discovery — shared by KeypointNet and 6-PACK; keypoints learned only from pose objectives.
- NOCS-REAL275 benchmark — the reference real-world dataset for category-level pose methods.
- Anchor-based attention for 3D localization — transfers 2D detection anchors to bounded 3D keypoint search.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H7.** Seguimiento 6D en tiempo real a nivel de categoría mediante puntos clave, útil para seguir frascos durante el transporte y el vertido.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
