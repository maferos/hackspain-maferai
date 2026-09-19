---
aliases: []
type: "source"
title: "PoseCNN: A Convolutional Neural Network for 6D Object Pose Estimation in Cluttered Scenes"
citekey: "Xiang2017posecnn"
doi: "10.48550/arXiv.1711.00199"
arxiv: "1711.00199"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1711.00199"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Yu Xiang", "Tanner Schmidt", "Venkatraman Narayanan", "Dieter Fox"]
sha256: ["d19a33a45655a713e8028f6be0538fcbf7f7365a80e12dbc68e1f651b639b421"]
pdf: "Content/Papers/Xiang2017posecnn.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Xiang2017posecnn.pdf]]

> [!abstract] One-sentence summary
> PoseCNN decouples 6D object pose into pixel-wise labeling, voted 2D center plus depth for translation, and quaternion regression for rotation, adds a symmetry-aware ShapeMatch-Loss and releases the YCB-Video dataset, reaching state-of-the-art RGB-D accuracy on OccludedLINEMOD.

## Abstract

Estimating the 6D pose of known objects is important for robots to interact with the real world. The problem is challenging due to the variety of objects as well as the complexity of a scene caused by clutter and occlusions between objects. In this work, we introduce PoseCNN, a new Convolutional Neural Network for 6D object pose estimation. PoseCNN estimates the 3D translation of an object by localizing its center in the image and predicting its distance from the camera. The 3D rotation of the object is estimated by regressing to a quaternion representation. We also introduce a novel loss function that enables PoseCNN to handle symmetric objects. In addition, we contribute a large scale video dataset for 6D object pose estimation named the YCB-Video dataset. Our dataset provides accurate 6D poses of 21 objects from the YCB dataset observed in 92 videos with 133,827 frames. We conduct extensive experiments on our YCB-Video dataset and the OccludedLINEMOD dataset to show that PoseCNN is highly robust to occlusions, can handle symmetric objects, and provide accurate pose estimation using only color images as input. When using depth data to further refine the poses, our approach achieves state-of-the-art results on the challenging OccludedLINEMOD dataset. Our code and dataset are available at https://rse-lab.cs.washington.edu/projects/posecnn/. (arXiv)

## 🧠 Key ideas (atomic)

- Feature-point matching methods for 6D pose need rich textures on objects, so they are unable to handle texture-less objects. (Xiang et al., 2017) `ev:cited` p. 1 ^xiang2017posecnn-001
- For template-based pose estimation methods, occlusions between objects significantly reduce the recognition performance, according to prior work. (Xiang et al., 2017) `ev:cited` p. 1 ^xiang2017posecnn-002
- Methods that regress image pixels to 3D object coordinates to establish 2D-3D correspondences cannot handle symmetric objects, the authors state. (Xiang et al., 2017) `ev:cited` p. 1 ^xiang2017posecnn-003
- PoseCNN is a convolutional neural network for end-to-end 6D object pose estimation that internally decouples the estimation of rotation from translation. (Xiang et al., 2017) `ev:asserted` p. 2 ^xiang2017posecnn-004
- PoseCNN is trained to perform three related tasks: pixel-wise semantic labeling, 3D translation estimation, and 3D rotation regression. (Xiang et al., 2017) `ev:reported` p. 1 ^xiang2017posecnn-005
- The authors argue that ignoring symmetries during training gives inconsistent loss signals, such as a high loss on an orientation correct under symmetry. (Xiang et al., 2017) `ev:asserted` p. 2 ^xiang2017posecnn-006
- The first stage of the network consists of 13 convolutional layers and 4 max-pooling layers, whose features are shared across all tasks. (Xiang et al., 2017) `ev:reported` p. 2 ^xiang2017posecnn-007
- The semantic labeling branch fuses two feature maps at 1/8 and 1/16 resolution, upsampling them to full image size to score each pixel. (Xiang et al., 2017) `ev:reported` p. 3 ^xiang2017posecnn-008
- The semantic labeling branch, inspired by fully convolutional networks for segmentation, is trained with a softmax cross entropy loss. (Xiang et al., 2017) `ev:reported` p. 3 ^xiang2017posecnn-009
- The authors argue that semantic labeling gives richer object information and handles occlusions better than detection with bounding boxes. (Xiang et al., 2017) `ev:asserted` p. 3 ^xiang2017posecnn-010
- The network estimates 3D translation by localizing the 2D object center in the image and predicting its distance from the camera. (Xiang et al., 2017) `ev:reported` p. 3 ^xiang2017posecnn-011
- The authors argue that directly regressing image features to translation is not generalizable since objects can appear at any image location. (Xiang et al., 2017) `ev:asserted` p. 3 ^xiang2017posecnn-012
- Assuming known camera intrinsics, Tx and Ty are recovered from the 2D center and the depth Tz through a pinhole projection equation. (Xiang et al., 2017) `ev:reported` p. 3 ^xiang2017posecnn-013
- For each pixel, the network regresses a unit vector toward the object center plus the center depth, rather than the raw displacement vector. (Xiang et al., 2017) `ev:reported` p. 4 ^xiang2017posecnn-014
- The authors state that the unit-length center direction is scale-invariant and therefore easier to train, which they verified experimentally. (Xiang et al., 2017) `ev:asserted` p. 4 ^xiang2017posecnn-015
- A Hough voting layer combines semantic labels and center directions, with each labeled pixel voting for image locations along its predicted ray. (Xiang et al., 2017) `ev:reported` p. 4 ^xiang2017posecnn-016
- The object center is selected as the image location with the maximum voting score for each object class. (Xiang et al., 2017) `ev:reported` p. 4 ^xiang2017posecnn-017
- For multiple instances of one class, non-maximum suppression is applied to the voting scores, then locations above a threshold are kept. (Xiang et al., 2017) `ev:reported` p. 4 ^xiang2017posecnn-018
- The center depth Tz is computed as the mean of the depths predicted by the inlier pixels that voted for that center. (Xiang et al., 2017) `ev:reported` p. 4 ^xiang2017posecnn-019
- Each object's bounding box is generated as the 2D rectangle enclosing all inlier pixels, then used for 3D rotation regression. (Xiang et al., 2017) `ev:reported` p. 4 ^xiang2017posecnn-020
- The 3D rotation is regressed by pooling first-stage features inside each bounding box with two RoI pooling layers into three fully connected layers. (Xiang et al., 2017) `ev:reported` p. 4 ^xiang2017posecnn-021
- For each object class, the last fully connected layer outputs a 3D rotation represented as a quaternion. (Xiang et al., 2017) `ev:reported` p. 4 ^xiang2017posecnn-022
- PoseLoss (PLOSS) measures the average squared distance between 3D model points rotated by the estimated orientation and by the ground-truth orientation. (Xiang et al., 2017) `ev:reported` p. 4 ^xiang2017posecnn-023
- PLOSS does not handle symmetric objects appropriately, since a symmetric object can have multiple correct 3D rotations. (Xiang et al., 2017) `ev:asserted` p. 4 ^xiang2017posecnn-024
- [[Symmetry-aware pose loss|ShapeMatch-Loss (SLOSS)]] measures, like ICP, the offset between each point of the estimated model orientation and the closest ground-truth model point. (Xiang et al., 2017) `ev:reported` p. 4 ^xiang2017posecnn-025
- [[Symmetry-aware pose loss|SLOSS]] does not require the specification of object symmetries, unlike a modified PLOSS that would enumerate all correct orientations. (Xiang et al., 2017) `ev:asserted` p. 4 ^xiang2017posecnn-026
- [[Symmetry-aware pose loss|SLOSS]] will not penalize rotations that are equivalent with respect to the 3D shape symmetry of the object. (Xiang et al., 2017) `ev:asserted` p. 5 ^xiang2017posecnn-027
- [[YCB-Video dataset|The YCB-Video dataset]] provides 6D pose annotations of 21 YCB objects in 92 videos with a total of 133,827 frames. (Xiang et al., 2017) `ev:reported` p. 2 ^xiang2017posecnn-028
- The LINEMOD dataset provides manual annotations for around 1,000 images for each of its 15 objects. (Xiang et al., 2017) `ev:cited` p. 5 ^xiang2017posecnn-029
- To avoid annotating every frame, object poses were manually specified only in the first frame of each [[YCB-Video dataset|YCB-Video]] video. (Xiang et al., 2017) `ev:reported` p. 5 ^xiang2017posecnn-030
- The camera trajectory is tracked through the depth video with object poses fixed relative to one another, then refined by global optimization. (Xiang et al., 2017) `ev:reported` p. 5 ^xiang2017posecnn-031
- The 21 objects were selected from the YCB set due to their high-quality 3D models and good visibility in depth. (Xiang et al., 2017) `ev:reported` p. 5 ^xiang2017posecnn-032
- Videos were recorded with an Asus Xtion Pro Live RGB-D camera in fast-cropping mode, giving 640x480 RGB images at 30 FPS. (Xiang et al., 2017) `ev:reported` p. 5 ^xiang2017posecnn-033
- The authors state that the 133,827 images make [[YCB-Video dataset|YCB-Video]] two full orders of magnitude larger than the LINEMOD dataset. (Xiang et al., 2017) `ev:asserted` p. 5 ^xiang2017posecnn-034
- The authors note annotation accuracy suffers from rolling shutter, object model inaccuracies, slight RGB-depth asynchrony, and uncertain camera intrinsic and extrinsic parameters. (Xiang et al., 2017) `ev:asserted` p. 5 ^xiang2017posecnn-035
- PoseCNN is trained on 80 [[YCB-Video dataset|YCB-Video]] videos and tested on 2,949 key frames extracted from the 12 remaining videos. (Xiang et al., 2017) `ev:reported` p. 5 ^xiang2017posecnn-036
- OccludedLINEMOD is one LINEMOD video of 1,214 frames with ground-truth poses annotated for eight objects under significant occlusion. (Xiang et al., 2017) `ev:cited` p. 5 ^xiang2017posecnn-037
- For training on both datasets, [[Synthetic training data for 6D pose estimation|80,000 synthetic images]] were generated by randomly placing objects in a scene. (Xiang et al., 2017) `ev:reported` p. 5 ^xiang2017posecnn-038
- Pose accuracy is evaluated with [[ADD and ADD-S metrics|the average distance (ADD)]] between model points transformed by the ground-truth pose and the estimated pose. (Xiang et al., 2017) `ev:reported` p. 6 ^xiang2017posecnn-039
- For symmetric objects, [[ADD and ADD-S metrics|the ADD-S metric]] computes the average distance using the closest model point instead of the corresponding point. (Xiang et al., 2017) `ev:reported` p. 6 ^xiang2017posecnn-040
- On OccludedLINEMOD, a pose is considered correct when the average distance is smaller than 10% of the 3D model diameter. (Xiang et al., 2017) `ev:reported` p. 6 ^xiang2017posecnn-041
- On YCB-Video, the area under the accuracy-threshold curve is reported while varying the distance threshold up to a maximum of 10cm. (Xiang et al., 2017) `ev:reported` p. 6 ^xiang2017posecnn-042
- The first 13 convolutional layers and first two fully connected layers are initialized with VGG16 weights trained on ImageNet. (Xiang et al., 2017) `ev:reported` p. 6 ^xiang2017posecnn-043
- During training of the network, no gradient is back-propagated via the Hough voting layer that localizes the object centers. (Xiang et al., 2017) `ev:reported` p. 6 ^xiang2017posecnn-044
- The baseline variant regresses each pixel to its 3D object coordinate and recovers the pose with pre-emptive RANSAC instead of rotation regression. (Xiang et al., 2017) `ev:reported` p. 6 ^xiang2017posecnn-045
- When depth is available, poses are refined with ICP using projective data association and a point-plane residual term. (Xiang et al., 2017) `ev:reported` p. 6 ^xiang2017posecnn-046
- Since ICP is not robust to local minima, multiple perturbed poses are refined and the best is selected by an alignment metric. (Xiang et al., 2017) `ev:reported` p. 6 ^xiang2017posecnn-047
- With PLOSS, rotation errors for the wood block and the large clamp span from 0 to 180 degrees, indicating network confusion. (Xiang et al., 2017) `ev:measured` p. 6 ^xiang2017posecnn-048
- With SLOSS, rotation errors concentrate at 180 degrees for the wood block and at 0 and 180 degrees for the large clamp. (Xiang et al., 2017) `ev:measured` p. 6 ^xiang2017posecnn-049
- Using color only, PoseCNN reaches an overall ADD area of 53.7 on YCB-Video, compared with 15.1 for the 3D coordinate regression network. (Xiang et al., 2017) `ev:measured` p. 7 ^xiang2017posecnn-050
- Using color only, PoseCNN reaches an overall ADD-S area of 75.9 on YCB-Video, compared with 29.8 for 3D coordinate regression. (Xiang et al., 2017) `ev:measured` p. 7 ^xiang2017posecnn-051
- With ICP refinement, PoseCNN reaches overall areas under the accuracy-threshold curve of 79.3 ADD and 93.0 ADD-S on YCB-Video. (Xiang et al., 2017) `ev:measured` p. 7 ^xiang2017posecnn-052
- The 3D coordinate regression network with ICP reaches overall areas of 74.5 ADD and 90.1 ADD-S on YCB-Video, below PoseCNN with ICP. (Xiang et al., 2017) `ev:measured` p. 7 ^xiang2017posecnn-053
- The authors attribute the color-only gain to center localization constraining the 3D translation estimate even when the object is occluded. (Xiang et al., 2017) `ev:asserted` p. 7 ^xiang2017posecnn-054
- The authors state that PoseCNN provides better initial 6D poses for ICP, whose convergence depends critically on the initial pose. (Xiang et al., 2017) `ev:asserted` p. 7 ^xiang2017posecnn-055
- The authors identify the tuna fish can as more difficult to handle, since it is small and has less texture. (Xiang et al., 2017) `ev:asserted` p. 7 ^xiang2017posecnn-056
- The authors report the network is confused by the large clamp and the extra large clamp, which have the same appearance. (Xiang et al., 2017) `ev:asserted` p. 7 ^xiang2017posecnn-057
- With ICP refinement, PoseCNN obtains an ADD area of 17.5 for the bowl on YCB-Video, against 78.3 under [[ADD and ADD-S metrics|the ADD-S metric]]. (Xiang et al., 2017) `ev:measured` p. 7 ^xiang2017posecnn-058
- The authors state that the 3D coordinate regression network cannot handle symmetric objects such as the banana and the bowl very well. (Xiang et al., 2017) `ev:asserted` p. 7 ^xiang2017posecnn-059
- Using color only on 7 OccludedLINEMOD objects, PoseCNN outperforms the prior color-based state of the art by a large margin, especially at small reprojection thresholds. (Xiang et al., 2017) `ev:measured` p. 7 ^xiang2017posecnn-060
- With ICP, PoseCNN reaches a mean accuracy of 78.0 on OccludedLINEMOD, above 76.7 for Michel et al. and 76.3 for Hinterstoisser et al. (Xiang et al., 2017) `ev:measured` p. 8 ^xiang2017posecnn-061
- With ICP, PoseCNN reaches 72.2 on Eggbox and 76.7 on Glue, compared with 65.5 from Hinterstoisser et al. and 73.8 from Michel et al. (Xiang et al., 2017) `ev:measured` p. 8 ^xiang2017posecnn-062
- The authors attribute the gains on the symmetric Eggbox and Glue objects to training with [[Symmetry-aware pose loss|ShapeMatch-Loss]], which respects object symmetry. (Xiang et al., 2017) `ev:asserted` p. 8 ^xiang2017posecnn-063
- On the Cat object of OccludedLINEMOD, PoseCNN+ICP reaches 52.2, below the 57.8 obtained by Michel et al. (Xiang et al., 2017) `ev:measured` p. 8 ^xiang2017posecnn-064
- The authors explain that color-only accuracies are much lower since the threshold on OccludedLINEMOD is usually smaller than 2cm. (Xiang et al., 2017) `ev:asserted` p. 8 ^xiang2017posecnn-065
- The authors conclude that their results indicate it is feasible to accurately estimate 6D object poses in cluttered scenes using vision data only. (Xiang et al., 2017) `ev:asserted` p. 8 ^xiang2017posecnn-066
- The authors suggest this opens the path to cameras with resolution and field of view going far beyond current depth camera systems. (Xiang et al., 2017) `ev:asserted` p. 8 ^xiang2017posecnn-067
- The authors note that [[Symmetry-aware pose loss|SLOSS]] sometimes results in local minimums in the pose space, similar to ICP. (Xiang et al., 2017) `ev:asserted` p. 8 ^xiang2017posecnn-068

## 🎯 Contributions

## 📖 Glossary

- **6D pose** — Rigid transformation of an object: 3D rotation plus 3D translation relative to the camera.
- **Hough voting** — Pixels cast votes for candidate locations; the maximum-score location is selected as the detection.
- **ADD** — Mean distance between model points under ground-truth and estimated poses.
- **ADD-S** — ADD variant using closest-point distances, tolerant to object symmetries.
- **ShapeMatch-Loss (SLOSS)** — Rotation loss matching each rotated model point to the closest ground-truth model point.
- **PoseLoss (PLOSS)** — Rotation loss on squared distances between corresponding rotated model points.
- **RoI pooling** — Crops and pools feature maps inside a region of interest to a fixed size.
- **ICP** — Iterative Closest Point: aligns a model to depth points by iteratively minimizing residuals.
- **YCB-Video** — RGB-D video dataset with 6D pose annotations of 21 YCB objects.
- **OccludedLINEMOD** — LINEMOD video subset with eight annotated objects under heavy occlusion.

## ❓ Open questions

- How can the local minima that SLOSS sometimes produces in the pose space be avoided, as the authors ask for more efficient symmetry handling?
- Can color-only PoseCNN reach the tight (under 2cm) ADD thresholds on OccludedLINEMOD without depth-based ICP refinement?
- How well does training on 80,000 randomly composed synthetic images transfer to real scenes, given the authors caution about real-to-rendered generalization?
- How to disambiguate objects with identical appearance but different size, such as the large and extra large clamps?
- How much do YCB-Video annotation errors (rolling shutter, model inaccuracies, sensor asynchrony, calibration) bound the measurable accuracy?
- Would back-propagating gradients through the Hough voting layer improve end-to-end training?

## 📝 Notes on reading

Version read: arXiv 1711.00199v3 (26 May 2018), matching the packet identifier.

Fig. 7 (rotation-error histograms, PLOSS vs SLOSS) is described only through the text; its caption says three symmetric objects while the text and panels name two (wood block, large clamp). Fig. 8(a) per-object accuracy-threshold curves and Fig. 8(b) reprojection curves are not readable in the extraction; only the text's qualitative statements about 8(b) were claimed. Fig. 9 shows qualitative examples only.

The text says Fig. 8(b) covers 7 objects, although OccludedLINEMOD annotates eight; which object is excluded is not stated.

Table III prints 0.93 for Cat under PoseCNN Color, unlike the one-decimal format of the other entries; it may be a typo for 9.3 and was not claimed. Table II cells for each of the 21 objects were not claimed individually beyond the ALL row and the bowl.

The method reference [29] (Tekin et al.) is dated 2018 in the bibliography of this 2017 preprint's v3.

Further paper statements left unclaimed to stay within the claim budget: the 128-dimensional center-regression embedding with smoothed L1 loss, PLOSS being very similar to a quaternion regression loss, and the potential application to the Amazon Picking Challenge.

## Suggested new concepts

- Hough voting for object center localization — reused by later keypoint and pose methods as an occlusion-robust alternative to direct center detection.
- Symmetry-aware pose loss — ShapeMatch-Loss and ADD-S form a recurring pattern for handling symmetric objects in training and evaluation.
- YCB-Video dataset — a standard 6D pose benchmark that many later papers report on.
- Decoupled translation and rotation estimation — a design choice separating center-plus-depth translation from rotation regression.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Regresión directa de pose, pérdida para simetrías, YCB-Video

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
