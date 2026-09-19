---
aliases: []
type: "source"
title: "DenseFusion: 6D Object Pose Estimation by Iterative Dense Fusion"
citekey: "Wang2019densefusion"
doi: "10.48550/arXiv.1901.04780"
arxiv: "1901.04780"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1901.04780"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Chen Wang", "Danfei Xu", "Yuke Zhu", "Roberto Martín-Martín", "Cewu Lu", "Li Fei-Fei", "Silvio Savarese"]
sha256: ["e04a4c884ee00ccbbc22470ab002717f1c98bfb089a02cfc195f200da200acef"]
pdf: "Content/Papers/Wang2019densefusion.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Wang2019densefusion.pdf]]

> [!abstract] One-sentence summary
> DenseFusion fuses per-pixel color embeddings with per-point geometric embeddings and refines poses with a learned iterative module, beating ICP-refined RGB-D baselines on YCB-Video and LineMOD at near real-time speed and enabling robot grasping.

## Abstract
A key technical challenge in performing 6D object pose estimation from RGB-D image is to fully leverage the two complementary data sources. Prior works either extract information from the RGB image and depth separately or use costly post-processing steps, limiting their performances in highly cluttered scenes and real-time applications. In this work, we present DenseFusion, a generic framework for estimating 6D pose of a set of known objects from RGB-D images. DenseFusion is a heterogeneous architecture that processes the two data sources individually and uses a novel dense fusion network to extract pixel-wise dense feature embedding, from which the pose is estimated. Furthermore, we integrate an end-to-end iterative pose refinement procedure that further improves the pose estimation while achieving near real-time inference. Our experiments show that our method outperforms state-of-the-art approaches in two datasets, YCB-Video and LineMOD. We also deploy our proposed method to a real robot to grasp and manipulate objects based on the estimated pose. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that existing methods find it difficult to satisfy accurate pose estimation and fast inference simultaneously. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019densefusion-001
- PoseCNN and MCN require post-hoc refinement steps, such as customized ICP or multi-view hypothesis verification, to fully utilize 3D information. (Wang et al., 2019) `ev:cited` p. 1 ^wang2019densefusion-002
- According to the authors, the post-hoc refinement steps of prior RGB-D methods cannot be optimized jointly with the final pose objective. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019densefusion-003
- The authors describe these post-hoc refinement steps as prohibitively slow for real-time applications of 6D pose estimation. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019densefusion-004
- The authors report that driving-oriented end-to-end fusion models, such as Frustum PointNet and PointFusion, fall short under heavy occlusion. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019densefusion-005
- The approach embeds and fuses RGB values and point clouds at per-pixel level, unlike prior work using global crop features or bounding boxes. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019densefusion-006
- The authors state that per-pixel fusion lets the model reason explicitly about local appearance and geometry, which they consider essential under heavy occlusion. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019densefusion-007
- Each 3D point is augmented with 2D information from a task-learned embedding space to form a color-depth space for pose estimation. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019densefusion-008
- The authors integrate an iterative refinement procedure inside the neural network architecture, removing the dependency on a post-processing ICP step. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019densefusion-009
- Methods that predict 2D keypoints and solve poses by PnP become unreliable given low-texture or low-resolution inputs, according to the authors. (Wang et al., 2019) `ev:cited` p. 2 ^wang2019densefusion-010
- The authors argue that generic object pose estimation tasks such as [[YCB-Video dataset|YCB-Video]] demand reasoning over both geometric and appearance information. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019densefusion-011
- The 6D pose is represented as a homogeneous transformation of a rotation in SO(3) and a translation, defined relative to the camera coordinate frame. (Wang et al., 2019) `ev:reported` p. 3 ^wang2019densefusion-012
- The architecture has two stages: semantic segmentation of known object categories from the color image, followed by 6D pose estimation per segmented object. (Wang et al., 2019) `ev:reported` p. 3 ^wang2019densefusion-013
- The second stage receives the masked depth pixels converted to a 3D point cloud plus an image patch cropped by the mask's bounding box. (Wang et al., 2019) `ev:reported` p. 3 ^wang2019densefusion-014
- Unlike the expensive post-hoc refinement of prior methods, the refinement module can be trained jointly with the main architecture. (Wang et al., 2019) `ev:asserted` p. 3 ^wang2019densefusion-015
- Segmented depth pixels are converted into a 3D point cloud with known camera intrinsics before a PointNet-like network extracts geometric features. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019densefusion-016
- The authors argue that processing depth as an additional CNN image channel neglects the intrinsic 3D structure of the depth channel. (Wang et al., 2019) `ev:asserted` p. 4 ^wang2019densefusion-017
- The geometric embedding network is a PointNet variant using average-pooling instead of the commonly used max-pooling as symmetric reduction function. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019densefusion-018
- The color embedding network is a CNN encoder-decoder that maps each image pixel to a per-pixel appearance feature vector. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019densefusion-019
- The authors argue that, under occlusion and segmentation errors, blindly fusing color and geometric features globally would degrade estimation performance. (Wang et al., 2019) `ev:asserted` p. 4 ^wang2019densefusion-020
- Each point's geometric feature is paired with its corresponding image feature pixel by projection onto the image plane using camera intrinsics. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019densefusion-021
- Each per-pixel fused feature is enriched with a global feature obtained through a symmetric reduction function to provide global context. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019densefusion-022
- The network predicts one pose from each densely-fused feature, yielding a set of P predicted poses for the object. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019densefusion-023
- The network also outputs a confidence score for each per-pixel pose prediction, learned in a self-supervised manner. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019densefusion-024
- The per-pixel pose loss is the mean distance between M model points transformed by the ground-truth pose and by the predicted pose. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019densefusion-025
- For symmetric objects, the loss instead uses the distance from each estimated model point to the closest ground-truth model point. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019densefusion-026
- Per-pixel losses are weighted by their confidence, with an added log-confidence regularization term balanced by a hyperparameter w. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019densefusion-027
- The pose estimate that has the highest confidence is used as the final output of the network. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019densefusion-028
- The refinement transforms the input point cloud into the canonical frame estimated from the previous pose, so the cloud implicitly encodes that pose. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019densefusion-029
- A dedicated pose residual estimator predicts a residual pose each iteration, reusing the image feature embedding from the main network. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019densefusion-030
- In practice, joint training of the pose residual estimator starts after the main network has converged. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019densefusion-031
- [[YCB-Video dataset|The YCB-Video dataset]] contains 92 RGB-D videos, each showing a subset of 21 YCB objects in different indoor scenes. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019densefusion-032
- Following PoseCNN, [[YCB-Video dataset|the YCB-Video split]] uses 80 videos for training and 2,949 key frames from 12 remaining videos for testing. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019densefusion-033
- [[YCB-Video dataset|The YCB-Video training set]] also includes the same 80,000 synthetic images released by the PoseCNN authors. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019densefusion-034
- The LineMOD dataset consists of 13 low-textured objects in 13 videos and is used without additional synthetic data. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019densefusion-035
- On YCB-Video, [[ADD and ADD-S metrics|the area under the ADD-S curve]] is reported with a maximum threshold of 0.1m, following PoseCNN. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019densefusion-036
- [[ADD and ADD-S metrics|The percentage of ADD-S below 2cm]] is reported as the minimum tolerance for robot manipulation with most grippers. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019densefusion-037
- The image embedding network consists of a Resnet-18 encoder followed by 4 up-sampling layers as the decoder. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019densefusion-038
- Both the color and the geometric dense feature embeddings have dimension 128 in the implementation. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019densefusion-039
- The iterative refinement module consists of 4 fully connected layers that directly output the pose residual from the global feature. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019densefusion-040
- All experiments in the paper use 2 iterations of the iterative pose refinement module after the initial per-pixel estimate. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019densefusion-041
- On YCB-Video, the full iterative model reaches a mean ADD-S AUC of 93.1 versus 93.0 for PoseCNN+ICP. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019densefusion-042
- The iterative model reaches 96.8 mean ADD-S<2cm on YCB-Video, compared with 93.2 for PoseCNN+ICP and 74.1 for PointFusion. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019densefusion-043
- The per-pixel variant without refinement reaches 95.3 mean ADD-S<2cm, above the 93.2 of PoseCNN+ICP on YCB-Video. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019densefusion-044
- PointFusion reaches a mean ADD-S AUC of 83.9 on YCB-Video, against 88.2 for Ours (single) and 91.2 for Ours (per-pixel). (Wang et al., 2019) `ev:measured` p. 6 ^wang2019densefusion-045
- For the iterative model, the large clamp and extra large clamp reach ADD-S AUC values of 72.9 and 69.8 on YCB-Video. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019densefusion-046
- On YCB-Video, the full iterative model outperforms PoseCNN with ICP refinement by 3.5% on the ADD-S<2cm metric. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019densefusion-047
- The authors conclude that dense fusion has a clear advantage over the global fusion-by-concatenation used in PointFusion. (Wang et al., 2019) `ev:asserted` p. 7 ^wang2019densefusion-048
- Iterative refinement improves performance on the bowl by 29%, a texture-less symmetric object that suffers from [[Pose ambiguity from symmetry|orientation ambiguity]]. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019densefusion-049
- Iterative refinement also improves the banana and the extra large clamp by 6% each on the YCB-Video Dataset. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019densefusion-050
- As occlusion increases, the performance of PointFusion and PoseCNN+ICP degrades significantly in ADD-S<2cm accuracy on YCB-Video. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019densefusion-051
- Under increasing occlusion, both Ours (per-pixel) and Ours (iterative) decrease by only 2% overall in ADD-S<2cm accuracy. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019densefusion-052
- The overall runtime reaches 16 FPS with about 5 objects in each frame, which the authors consider fast enough for real-time application. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019densefusion-053
- PoseCNN+ICP spends 10.4 of its 10.6 seconds per frame on the ICP post-processing step on YCB-Video. (Wang et al., 2019) `ev:measured` p. 8 ^wang2019densefusion-054
- The full method takes 0.06 seconds per frame, split into 0.03 for segmentation, 0.02 for pose estimation and 0.01 for refinement. (Wang et al., 2019) `ev:measured` p. 8 ^wang2019densefusion-055
- The method is approximately 200x faster than PoseCNN with ICP refinement in per-frame runtime on the YCB-Video dataset. (Wang et al., 2019) `ev:measured` p. 8 ^wang2019densefusion-056
- The authors state that their approach localizes the poorly segmented clamp from only the visible part of the object. (Wang et al., 2019) `ev:asserted` p. 8 ^wang2019densefusion-057
- On LineMOD, the iterative model reaches a mean ADD of 94.3, against 79 for SSD-6D+ICP and 73.7 for PointFusion. (Wang et al., 2019) `ev:measured` p. 8 ^wang2019densefusion-058
- Without iterative refinement, the per-pixel model outperforms the state-of-the-art ICP-refined method on LineMOD by 7%. (Wang et al., 2019) `ev:measured` p. 8 ^wang2019densefusion-059
- Iterative refinement adds another 8% improvement on LineMOD over the per-pixel model's mean ADD result. (Wang et al., 2019) `ev:measured` p. 8 ^wang2019densefusion-060
- On LineMOD, pose estimation improves by an average of 0.8 cm in ADD after 2 refinement iterations. (Wang et al., 2019) `ev:measured` p. 8 ^wang2019densefusion-061
- The robot attempts 12 grasps on each of the five objects, giving 60 grasp attempts in total. (Wang et al., 2019) `ev:reported` p. 9 ^wang2019densefusion-062
- The robot succeeds on 73% of the grasps using poses estimated by the proposed approach. (Wang et al., 2019) `ev:measured` p. 9 ^wang2019densefusion-063
- The banana is the most difficult object to grasp, with 7 out of 12 successful attempts. (Wang et al., 2019) `ev:measured` p. 9 ^wang2019densefusion-064
- The authors suggest that banana failures may stem from their plain yellow banana differing from the one in the dataset. (Wang et al., 2019) `ev:asserted` p. 9 ^wang2019densefusion-065
- According to the authors, the results indicate the approach is robust enough for real robotic tasks without explicit domain adaptation. (Wang et al., 2019) `ev:asserted` p. 9 ^wang2019densefusion-066
- The grasping robot is a Toyota HSR with an Asus Xtion RGB-D sensor, a holonomic mobile base and a two-finger gripper. (Wang et al., 2019) `ev:reported` p. 11 ^wang2019densefusion-067
- The model trained on YCB-Video was deployed on the robot without finetuning, although its Asus Xtion camera differs from the Kinect-v2. (Wang et al., 2019) `ev:reported` p. 11 ^wang2019densefusion-068
- A projected model point is counted invisible when its depth differs from the measured depth by more than 20mm. (Wang et al., 2019) `ev:reported` p. 11 ^wang2019densefusion-069

## 🎯 Contributions

## 📖 Glossary
- **6D pose** — Rigid transformation of an object: 3D rotation plus 3D translation relative to the camera.
- **ADD** — Average distance between model points transformed by predicted and ground-truth poses.
- **ADD-S** — Symmetry-invariant ADD using the closest-point distance between transformed model points.
- **Dense fusion** — Per-pixel concatenation of color and geometric embeddings before pose prediction.
- **ICP** — Iterative Closest Point, a registration algorithm aligning point clouds by repeated nearest-neighbour matching.
- **PointNet** — Network processing unordered point sets through per-point features and a symmetric pooling function.
- **Pose residual estimator** — Network predicting a corrective pose update from a point cloud transformed by the previous estimate.
- **Invisible surface percentage** — Share of sampled model surface points occluded given the camera viewpoint.

## ❓ Open questions
- How much does performance depend on the PoseCNN segmentation masks, and how would it change with a stronger or weaker segmenter?
- Does the method extend to unknown or category-level objects without per-object 3D models?
- How does accuracy evolve beyond 2 refinement iterations, and when does refinement stop helping?
- How much would texture mismatches between training models and real objects (as with the banana) be reduced by domain adaptation?
- Would the grasp success of 73% change with an optimized picking order or with stacked configurations allowed?

## 📝 Notes on reading
- Version read: arXiv v1 preprint (1901.04780v1, 15 Jan 2019), matching the packet identifier.
- The 3.5% gain over PoseCNN+ICP is stated on the ADD-S<2cm metric (p. 7) and as 'pose accuracy' in the introduction (p. 2); Table 1 means give 96.8 vs 93.2, a difference of 3.6.
- The '200x faster' claim (p. 2, Table 3 caption) is approximate; Table 3 totals 10.6 s vs 0.06 s per frame (about 177x). The text also says 'two order of magnitude faster' (p. 7).
- The per-object refinement gains on p. 7 (bowl 29%, banana 6%, extra large clamp 6%) match the ADD-S<2cm column of Table 1, not the AUC column; the paper does not say which metric it means.
- Figure 5 (performance vs occlusion) is only a plot; beyond the 2% drop stated in the text, its curves were not claimed.
- Figure 6 shows ADD values per refinement iteration (0.029 to 0.007 m across initial and three iterations) for LineMOD examples, while the text says 2 iterations are used; the per-panel values were not claimed.
- Table captions say symmetric objects are in bold, but the bold formatting is lost in the extraction.
- The LineMOD comparison mixes RGB-only (BB8, PoseCNN+DeepIM) and RGB-D methods; baseline numbers come from other papers.
- The segmentation stage reuses the PoseCNN segmentation network; all YCB-Video comparisons use the same PoseCNN masks.

## Suggested new concepts
- Dense per-pixel RGB-D fusion — a recurring design pattern for occlusion-robust 6D pose estimation worth comparing across methods.
- Learned iterative pose refinement — a differentiable alternative to ICP that trades post-processing cost for a trained residual network.
- ADD / ADD-S metrics — the standard 6D pose evaluation metrics used across YCB-Video and LineMOD benchmarks.
- YCB-Video dataset — a core benchmark for household-object pose estimation relevant to robot manipulation.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — *Baseline* RGB-D entrenable con datos propios
