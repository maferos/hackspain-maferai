---
aliases: []
type: "source"
title: "CosyPose: Consistent multi-view multi-object 6D pose estimation"
citekey: "Labbe2020cosypose"
doi: "10.48550/arXiv.2008.08465"
arxiv: "2008.08465"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2008.08465"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Yann Labbé", "Justin Carpentier", "Mathieu Aubry", "Josef Sivic"]
sha256: ["dea7d071c24cfc42eb6174838091b40a8c6ee4924ccafaa9f1ed6bee41da2ef4"]
pdf: "Content/Papers/Labbe2020cosypose.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 65
---

📄 PDF: [[Labbe2020cosypose.pdf]]

> [!abstract] One-sentence summary
> CosyPose combines a DeepIM-style render-and-compare single-view pose estimator with RANSAC object-level matching across views and object-level bundle adjustment, recovering all known objects and uncalibrated camera poses from RGB images and improving on prior results on YCB-Video and T-LESS.

## Abstract

We introduce an approach for recovering the 6D pose of multiple known objects in a scene captured by a set of input images with unknown camera viewpoints. First, we present a single-view single-object 6D pose estimation method, which we use to generate 6D object pose hypotheses. Second, we develop a robust method for matching individual 6D object pose hypotheses across different input images in order to jointly estimate camera viewpoints and 6D poses of all objects in a single consistent scene. Our approach explicitly handles object symmetries, does not require depth measurements, is robust to missing or incorrect object hypotheses, and automatically recovers the number of objects in the scene. Third, we develop a method for global scene refinement given multiple object hypotheses and their correspondences across views. This is achieved by solving an object-level bundle adjustment problem that refines the poses of cameras and objects to minimize the reprojection error in all views. We demonstrate that the proposed method, dubbed CosyPose, outperforms current state-of-the-art results for single-view and multi-view 6D object pose estimation by a large margin on two challenging benchmarks: the YCB-Video and T-LESS datasets. Code and pre-trained models are available on the project webpage https://www.di.ens.fr/willow/research/cosypose/. (arXiv)

## 🧠 Key ideas (atomic)

- The method aims to estimate accurate 6D poses of multiple known objects in a 3D scene captured by multiple cameras with unknown positions. (Labbé et al., 2020) `ev:asserted` p. 1 ^labbe2020cosypose-001
- Most prior RGB-based pose methods treat objects independently, estimating each object pose from a single input image. (Labbé et al., 2020) `ev:cited` p. 2 ^labbe2020cosypose-002
- Single-view candidate 6D poses are noisy because they suffer from depth ambiguities inherent to single-view methods. (Labbé et al., 2020) `ev:asserted` p. 2 ^labbe2020cosypose-003
- The approach assumes known 3D object models but no prior information on the number or type of objects in the scene. (Labbé et al., 2020) `ev:reported` p. 4 ^labbe2020cosypose-004
- The pipeline has three stages: single-view object candidate generation, cross-view object candidate matching, and global scene refinement of all poses. (Labbé et al., 2020) `ev:reported` p. 5 ^labbe2020cosypose-005
- Unlike depth-based object-level SLAM approaches, the method exploits only RGB images to estimate the 3D structure of the scene. (Labbé et al., 2020) `ev:asserted` p. 4 ^labbe2020cosypose-006
- The multi-view single-object method of Li et al. aggregates per-view pose candidates while assuming that camera poses are known. (Labbé et al., 2020) `ev:cited` p. 3 ^labbe2020cosypose-007
- Unlike prior works limited to a single instance of each object, the method handles scenes with multiple instances of the same object. (Labbé et al., 2020) `ev:asserted` p. 4 ^labbe2020cosypose-008
- Stage 1 obtains object detections in each view with an off-the-shelf 2D detector such as FasterRCNN or RetinaNet. (Labbé et al., 2020) `ev:reported` p. 6 ^labbe2020cosypose-009
- The [[Render-and-compare pose refinement|single-view pose refiner]] replaces the FlowNet backbone of DeepIM with a more recent EfficientNet-B3 network followed by spatial average pooling. (Labbé et al., 2020) `ev:reported` p. 19 ^labbe2020cosypose-010
- Unlike DeepIM, the network omits auxiliary flow and mask predictions, which the authors say makes the method simpler to train. (Labbé et al., 2020) `ev:asserted` p. 19 ^labbe2020cosypose-011
- The network predicts rotation with the parametrization of Zhou et al., previously shown to give more stable CNN training than quaternions. (Labbé et al., 2020) `ev:cited` p. 6 ^labbe2020cosypose-012
- The training loss disentangles the prediction of xy translation, relative depth and rotation, following the recommendations of Simonelli et al. (Labbé et al., 2020) `ev:reported` p. 21 ^labbe2020cosypose-013
- The loss enumerates all possible object symmetries to match predicted and ground-truth model vertices instead of finding nearest neighbors as [[ADD and ADD-S metrics|ADD-S]] does. (Labbé et al., 2020) `ev:reported` p. 20 ^labbe2020cosypose-014
- The network uses focal lengths of the camera equivalent to the cropped images instead of fixing focal lengths to 1 as DeepIM does. (Labbé et al., 2020) `ev:reported` p. 6 ^labbe2020cosypose-015
- Using cropped focal lengths makes the network predict xy translations in pixels, so it can become invariant to input camera intrinsics. (Labbé et al., 2020) `ev:asserted` p. 20 ^labbe2020cosypose-016
- Coarse estimation reuses the same network architecture with a canonical input pose that renders the object 1 meter from the camera. (Labbé et al., 2020) `ev:reported` p. 21 ^labbe2020cosypose-017
- The authors generate [[Synthetic training data for 6D pose estimation|one million synthetic training images]] on each dataset in addition to the real training images provided. (Labbé et al., 2020) `ev:reported` p. 21 ^labbe2020cosypose-018
- Each synthetic image places 3 to 9 randomly sampled objects in a 50 cm box with randomly sampled orientations. (Labbé et al., 2020) `ev:reported` p. 21 ^labbe2020cosypose-019
- Half of the synthetic images show objects flying in the air, the other half physically feasible configurations obtained after physics simulation. (Labbé et al., 2020) `ev:reported` p. 21 ^labbe2020cosypose-020
- On T-LESS, synthetic images are generated from CAD models only, with random textures following prior work on [[Domain randomization|domain randomization]]. (Labbé et al., 2020) `ev:reported` p. 22 ^labbe2020cosypose-021
- Training applies Gaussian blur, contrast, brightness, color and sharpness augmentation from the Pillow library to the input RGB images. (Labbé et al., 2020) `ev:reported` p. 22 ^labbe2020cosypose-022
- Networks are trained with Adam and synchronous distributed training on 32 GPUs, with a total batch size of 1024. (Labbé et al., 2020) `ev:reported` p. 22 ^labbe2020cosypose-023
- Each network is trained for 80k iterations on synthetic data only, then for another 80k iterations on real and synthetic images. (Labbé et al., 2020) `ev:reported` p. 22 ^labbe2020cosypose-024
- In the second training phase, the real training images account for around 25% of each batch of training images. (Labbé et al., 2020) `ev:reported` p. 22 ^labbe2020cosypose-025
- For objects with symmetry axes, the symmetry set is discretized using 64 rotation angles around each symmetry axis. (Labbé et al., 2020) `ev:reported` p. 7 ^labbe2020cosypose-026
- Two-view candidate pair selection uses RANSAC, which hypothesizes a relative camera pose and counts consistent pairs of object candidates as inliers. (Labbé et al., 2020) `ev:reported` p. 7 ^labbe2020cosypose-027
- Relative camera pose hypotheses are built from two sampled candidate pairs, which in most cases is sufficient to disambiguate object symmetries. (Labbé et al., 2020) `ev:reported` p. 8 ^labbe2020cosypose-028
- Relative camera pose hypotheses supported by fewer than three inlier pairs of object candidates are discarded during two-view selection. (Labbé et al., 2020) `ev:reported` p. 8 ^labbe2020cosypose-029
- Object candidates not validated by any other view appear as isolated vertices of the candidate graph and are removed. (Labbé et al., 2020) `ev:reported` p. 8 ^labbe2020cosypose-030
- Each connected component of the candidate graph is associated with a unique physical object seen from different views. (Labbé et al., 2020) `ev:reported` p. 8 ^labbe2020cosypose-031
- Scene refinement solves an object-level bundle adjustment that minimizes a symmetry-aware reprojection loss over all object and camera poses. (Labbé et al., 2020) `ev:reported` p. 9 ^labbe2020cosypose-032
- The global consensus optimization over all object and camera poses is solved with the Levenberg-Marquart algorithm. (Labbé et al., 2020) `ev:reported` p. 9 ^labbe2020cosypose-033
- Using the same PoseCNN detections, the single-view method reaches 89.8 AUC of ADD-S on [[YCB-Video dataset|YCB-Video]] versus 88.1 for DeepIM. (Labbé et al., 2020) `ev:measured` p. 10 ^labbe2020cosypose-034
- On YCB-Video, the single-view method reaches 84.5 AUC of ADD(-S) versus 81.9 for the previous state-of-the-art DeepIM. (Labbé et al., 2020) `ev:measured` p. 10 ^labbe2020cosypose-035
- On the T-LESS SiSo task, the method scores 63.8 on evsd < 0.3 versus 29.5 for Pix2Pose and 26.8 for Implicit. (Labbé et al., 2020) `ev:measured` p. 10 ^labbe2020cosypose-036
- On the T-LESS evsd < 0.3 metric, the coarse plus refinement solution achieves a 34.2% absolute improvement over existing state-of-the-art methods. (Labbé et al., 2020) `ev:measured` p. 10 ^labbe2020cosypose-037
- Removing data augmentation during training drops the T-LESS SiSo evsd < 0.3 score from 63.8 to 37.0. (Labbé et al., 2020) `ev:measured` p. 10 ^labbe2020cosypose-038
- Replacing the loss, network or rotation parametrization with DeepIM-style components lowers the T-LESS score to 60.1, 59.5 and 61.0 respectively. (Labbé et al., 2020) `ev:measured` p. 10 ^labbe2020cosypose-039
- The authors describe data augmentation as crucial on T-LESS, where training uses only synthetic data and real object images on dark background. (Labbé et al., 2020) `ev:asserted` p. 11 ^labbe2020cosypose-040
- On YCB-Video, [[Synthetic training data for 6D pose estimation|pre-training the model on synthetic data]] yields an improvement of approximately 2 points on the AUC of ADD(-S). (Labbé et al., 2020) `ev:measured` p. 22 ^labbe2020cosypose-041
- Stage 1 only keeps object detections with a score above 0.3 in order to limit the number of detections. (Labbé et al., 2020) `ev:reported` p. 11 ^labbe2020cosypose-042
- Stage 2 uses a RANSAC 3D inlier threshold of C = 2 cm, with the same hyper-parameters on both datasets. (Labbé et al., 2020) `ev:reported` p. 11 ^labbe2020cosypose-043
- A maximum of 2000 RANSAC iterations per pair of views is used, reached only for the most complex T-LESS scenes. (Labbé et al., 2020) `ev:reported` p. 11 ^labbe2020cosypose-044
- Scene refinement runs 100 Levenberg-Marquart iterations, although the optimization typically converges in less than 10 iterations. (Labbé et al., 2020) `ev:reported` p. 11 ^labbe2020cosypose-045
- To avoid recall penalties, unverified initial candidates are added to the predictions with confidence scores strictly lower than full reconstruction predictions. (Labbé et al., 2020) `ev:reported` p. 11 ^labbe2020cosypose-046
- With 5 views on YCB-Video, the method reaches 93.4 AUC of ADD-S versus 80.2 for Li et al., without known camera poses. (Labbé et al., 2020) `ev:measured` p. 12 ^labbe2020cosypose-047
- On the T-LESS ViVo task, AUC of ADD-S rises from 72.1 with 1 view to 78.9 with 8 views. (Labbé et al., 2020) `ev:measured` p. 12 ^labbe2020cosypose-048
- On the T-LESS ViVo task, evsd < 0.3 rises from 62.6 with 1 view to 71.6 with 8 views. (Labbé et al., 2020) `ev:measured` p. 12 ^labbe2020cosypose-049
- On 1000 T-LESS ViVo images, mAP@ADD-S<0.1d rises from 55.0 with 1 view to 69.0 with 8 views. (Labbé et al., 2020) `ev:measured` p. 12 ^labbe2020cosypose-050
- Global scene refinement reduces the average ADD-S error of inlier candidates on YCB-Video from 6.40 to 5.05 mm. (Labbé et al., 2020) `ev:measured` p. 12 ^labbe2020cosypose-051
- On T-LESS, global scene refinement reduces the average ADD-S error of inlier candidates from 4.43 to 3.19 mm. (Labbé et al., 2020) `ev:measured` p. 12 ^labbe2020cosypose-052
- On randomly sampled groups of 5 YCB-Video views, the feature-based SfM software COLMAP outputs camera poses in only 67% of cases. (Labbé et al., 2020) `ev:measured` p. 12 ^labbe2020cosypose-053
- On the same 5-view YCB-Video groups, the method outputs camera poses in 95% of cases, compared with COLMAP. (Labbé et al., 2020) `ev:measured` p. 13 ^labbe2020cosypose-054
- On groups of 8 T-LESS views, COLMAP outputs camera poses only in 4% of cases, compared to 74% for the method. (Labbé et al., 2020) `ev:measured` p. 13 ^labbe2020cosypose-055
- Using ground-truth camera poses instead of recovered ones improves results within 1% for T-LESS with 4 views and YCB-Video with 5 views. (Labbé et al., 2020) `ev:measured` p. 13 ^labbe2020cosypose-056
- With 8 T-LESS views, ground-truth camera poses improve results within 3% over the camera poses recovered automatically by the method. (Labbé et al., 2020) `ev:measured` p. 13 ^labbe2020cosypose-057
- For 4 views with 6 2D detections per view, the approach takes approximately 320 ms to predict the state of the scene. (Labbé et al., 2020) `ev:measured` p. 13 ^labbe2020cosypose-058
- Of that time, candidate pose estimation takes 190 ms, candidate association 40 ms and scene refinement 90 ms. (Labbé et al., 2020) `ev:measured` p. 13 ^labbe2020cosypose-059
- The authors argue the results make a step towards visually driven robotic manipulation in unconstrained scenarios with moving cameras. (Labbé et al., 2020) `ev:asserted` p. 13 ^labbe2020cosypose-060
- Distractor objects most often yield 6D pose estimates inconsistent across views, which lets the matching stage filter them as outliers. (Labbé et al., 2020) `ev:asserted` p. 35 ^labbe2020cosypose-061
- Two incorrect object candidates consistent across at least two views produce an incorrect object in the reconstructed scene. (Labbé et al., 2020) `ev:asserted` p. 35 ^labbe2020cosypose-062
- A candidate that is correct in one view but not matched in any other view is missing from the final reconstruction. (Labbé et al., 2020) `ev:asserted` p. 35 ^labbe2020cosypose-063
- The authors suggest that reprojecting detections from other views, as in guided matching, could recover such missing objects. (Labbé et al., 2020) `ev:asserted` p. 35 ^labbe2020cosypose-064
- Positioning a camera requires at least three object candidate inliers in its view: two to position it and one to validate. (Labbé et al., 2020) `ev:asserted` p. 40 ^labbe2020cosypose-065

## 🎯 Contributions

## 📖 Glossary

- **6D pose** — Rigid 3D rotation plus 3D translation of an object relative to a camera.
- **Render-and-compare** — Refining a pose by comparing a rendering at the current estimate with the image.
- **Object candidate** — A per-view 2D detection with its label and estimated 6D pose.
- **Symmetric distance** — Average point error between two poses, minimized over the object's symmetry transformations.
- **Object-level bundle adjustment** — Joint refinement of object and camera poses minimizing multi-view reprojection error of model points.
- **ADD-S** — Average closest-point distance between model points under predicted and ground-truth poses.
- **evsd** — BOP visual surface discrepancy error; symmetry-invariant and accounts for object visibility.
- **SiSo / ViVo** — BOP evaluation tasks: single instance single object versus varying instances varying objects.
- **RANSAC** — Robust estimation by sampling minimal hypotheses and scoring them by inlier count.

## ❓ Open questions

- Would requiring more associated candidates per physical object and more views reliably suppress consistent mistakes from similar viewpoints?
- Can guided matching, reprojecting detections into views where they were missed, recover objects seen correctly in only one view?
- How can cameras be positioned in views with fewer than three reliable object candidates, for example by combining with local features?
- Can temporal continuity in video bring the roughly 320 ms per-scene cost to real-time rates?
- How does the method behave with objects outside the database that closely resemble database objects across many views?
- Would the pipeline transfer to category-level or unknown objects without exact 3D models?

## 📝 Notes on reading

Read the arXiv v1 preprint (arXiv:2008.08465v1, 19 Aug 2020), which matches the packet identifier; it includes a long appendix (pp. 18–41). Tables 1 and 2 were extracted as flattened columns but were readable; values were claimed from their headline rows. Figures 1–18 (qualitative reconstructions, training images, the 2D matching illustration, and the failure cases) could only be described: they show inlier/outlier candidates, distractor filtering, 3D NMS removing duplicate labels, and camera failures when only two objects are visible. Small inconsistencies: the appendix rounds the T-LESS data-augmentation result to around 37% vs 64%, while Table 1b gives 37.0 vs 63.8; EfficientNet is cited as [40] in Sec. 3.2 but as [41] (the rotation paper) in Appendix A; Appendix C refers to relative camera pose sampling as Sec. 3.2 while it is described in Sec. 3.3. The learning rate is printed as 3.10−4 in the extracted text and was not claimed. Duplicate objects are removed by 3D NMS in the visualized reconstruction; the paper does not state clearly whether the quantitative results also use this step.

## Suggested new concepts

- Object-level bundle adjustment — a reusable idea: refine camera and object poses jointly using object models instead of point features.
- Multi-view 6D pose consistency — cross-view verification of pose hypotheses as a filter for false positives in cluttered scenes.
- Render-and-compare pose refinement — the DeepIM/CosyPose family underlies many later 6D pose estimators.
- Object symmetry handling in pose estimation — symmetric distances and losses recur across pose estimation and evaluation metrics.
- BOP benchmark — the standard evaluation protocol and datasets (T-LESS, YCB-Video) for 6D object pose.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — *Render-and-compare* y BA a nivel de objeto (varias cámaras)

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
