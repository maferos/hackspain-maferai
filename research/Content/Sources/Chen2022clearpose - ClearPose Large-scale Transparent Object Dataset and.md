---
aliases: []
type: "source"
title: "ClearPose: Large-scale Transparent Object Dataset and Benchmark"
citekey: "Chen2022clearpose"
doi: "10.48550/arXiv.2203.03890"
arxiv: "2203.03890"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2203.03890"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Xiaotong Chen", "Huijie Zhang", "Zeren Yu", "Anthony Opipari", "Odest Chadwicke Jenkins"]
sha256: ["aad5a459ac5dde7dabd95ed017dc0346e8fb3b8e0458d1bf39f3d8ac9b83a9d0"]
pdf: "Content/Papers/Chen2022clearpose.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 66
---

📄 PDF: [[Chen2022clearpose.pdf]]

> [!abstract] One-sentence summary
> ClearPose is a 354,481-frame real-world RGB-D dataset of 63 transparent objects with pose, mask, normal and depth labels, used to benchmark depth completion and pose estimation under six hard test conditions.

## Abstract

Transparent objects are ubiquitous in household settings and pose distinct challenges for visual sensing and perception systems. The optical properties of transparent objects leave conventional 3D sensors alone unreliable for object depth and pose estimation. These challenges are highlighted by the shortage of large-scale RGB-Depth datasets focusing on transparent objects in real-world settings. In this work, we contribute a large-scale real-world RGB-Depth transparent object dataset named ClearPose to serve as a benchmark dataset for segmentation, scene-level depth completion and object-centric pose estimation tasks. The ClearPose dataset contains over 350K labeled real-world RGB-Depth frames and 5M instance annotations covering 63 household objects. The dataset includes object categories commonly used in daily life under various lighting and occluding conditions as well as challenging test scenarios such as cases of occlusion by opaque or translucent objects, non-planar orientations, presence of liquids, etc. We benchmark several state-of-the-art depth completion and object pose estimation deep neural networks on ClearPose. The dataset and benchmarking source code is available at https://github.com/opipari/ClearPose. (arXiv)

## 🧠 Key ideas (atomic)

- The paper states that transparent objects lack consistent RGB color features across scenes, since their appearance depends on background, lighting and organization. (Chen et al., 2022) `ev:asserted` p. 1 ^chen2022clearpose-001
- The paper states that RGB-D cameras give inaccurate depth on transparent or translucent materials due to the lack of reliable reflections. (Chen et al., 2022) `ev:asserted` p. 1 ^chen2022clearpose-002
- The authors aim to complement recent transparent object perception work by providing a large-scale, real-world RGB-D transparent object dataset. (Chen et al., 2022) `ev:asserted` p. 2 ^chen2022clearpose-003
- In the comparison table, ClearPose lists 63 objects, 350K real RGB-D frames and about 5M pose annotations. (Chen et al., 2022) `ev:reported` p. 2 ^chen2022clearpose-004
- StereObj1M frame and pose annotation counts in the table are estimates, because that dataset was not publicly available at submission time. (Chen et al., 2022) `ev:reported` p. 2 ^chen2022clearpose-005
- According to the authors, most existing transparent object datasets are relatively small-scale, with no more than 50K real-world frames. (Chen et al., 2022) `ev:asserted` p. 3 ^chen2022clearpose-006
- The authors note that existing transparent datasets include few cluttered scenes, typically with less than 3 objects per image. (Chen et al., 2022) `ev:asserted` p. 3 ^chen2022clearpose-007
- ClearPose is labeled with ground truth pose, depth, instance-level segmentation masks and surface normals, among other labels. (Chen et al., 2022) `ev:reported` p. 3 ^chen2022clearpose-008
- Object categories include bottles, cups, wine cups, containers, bowls, plates, spoons, knives, forks and some chemical lab supplies. (Chen et al., 2022) `ev:reported` p. 3 ^chen2022clearpose-009
- Labeling uses ProgressLabeller, which combines visual SLAM, an interactive graphical interface and multi-view silhouette matching to align object poses. (Chen et al., 2022) `ev:reported` p. 4 ^chen2022clearpose-010
- The authors state that ProgressLabeller enables rapid annotation and avoids the broken depth problem caused by transparent objects. (Chen et al., 2022) `ev:asserted` p. 4 ^chen2022clearpose-011
- TOD and StereObj1M use RGB stereo cameras with AprilTags, solving object poses from manually annotated keypoints triangulated across views. (Chen et al., 2022) `ev:cited` p. 4 ^chen2022clearpose-012
- TOD recorded ground truth depth by placing opaque counterparts of the same shape at the transparent objects' poses in separate collects. (Chen et al., 2022) `ev:cited` p. 4 ^chen2022clearpose-013
- The authors describe replacing transparent objects with opaque counterparts, as in ClearGrasp, as extremely inefficient for data collection. (Chen et al., 2022) `ev:asserted` p. 4 ^chen2022clearpose-014
- TransCG attaches all objects to a large visual IR marker so that an optical tracking algorithm can estimate their 6D poses. (Chen et al., 2022) `ev:cited` p. 5 ^chen2022clearpose-015
- The ClearPose labeling pipeline assumes static scenes during video capture and backgrounds with adequate RGB features for visual SLAM. (Chen et al., 2022) `ev:reported` p. 5 ^chen2022clearpose-016
- StereObj1M benchmarked KeyPose and PVNet on more challenging objects and scenes, where both achieved lower ADD-S AUC accuracy. (Chen et al., 2022) `ev:cited` p. 5 ^chen2022clearpose-017
- The two-stage method of Xu et al. reportedly outperformed DenseFusion fed with ClearGrasp output depth by a large margin. (Chen et al., 2022) `ev:cited` p. 6 ^chen2022clearpose-018
- ClearPose includes 49 household objects, among them 14 water cups, 9 wine cups, 5 bottles, 6 bowls and 5 containers. (Chen et al., 2022) `ev:reported` p. 6 ^chen2022clearpose-019
- The dataset also contains 14 chemical supply objects, including a syringe, reagent bottles, graduated cylinders, a funnel, a flask and a beaker. (Chen et al., 2022) `ev:reported` p. 6 ^chen2022clearpose-020
- All images were collected with a RealSense L515 RGB-depth camera at a raw resolution of 1280×720. (Chen et al., 2022) `ev:reported` p. 6 ^chen2022clearpose-021
- After pose annotation, the central part of each image is cropped and reshaped to 640×480 for reduced storage and faster training. (Chen et al., 2022) `ev:reported` p. 6 ^chen2022clearpose-022
- For training, the 63 objects are separated into 5 subsets, each collected in 4-5 scenes with different backgrounds. (Chen et al., 2022) `ev:reported` p. 6 ^chen2022clearpose-023
- Each training scene is scanned by a hand-held camera moving around the tabletop at 3 different heights under 3 lighting conditions. (Chen et al., 2022) `ev:reported` p. 6 ^chen2022clearpose-024
- The test set covers six cases: new backgrounds, heavy occlusion, translucent covers, opaque distractors, liquid filling and non-planar configurations. (Chen et al., 2022) `ev:reported` p. 7 ^chen2022clearpose-025
- Heavy occlusion test scenes each hold about 25 objects that form multiple layers of occlusion when viewed from the table's side. (Chen et al., 2022) `ev:reported` p. 7 ^chen2022clearpose-026
- Opaque distractor test scenes place transparent objects together with YCB and HOPE objects that did not appear in training. (Chen et al., 2022) `ev:reported` p. 7 ^chen2022clearpose-027
- In total, the dataset contains 354,481 RGB-D frames captured in 51 scenes, according to the authors' statistics. (Chen et al., 2022) `ev:measured` p. 7 ^chen2022clearpose-028
- The dataset contains 5,052,429 object instance annotations with 6 DoF poses, segmentation masks, surface normals and ground truth depth images. (Chen et al., 2022) `ev:measured` p. 7 ^chen2022clearpose-029
- The authors report roughly even viewpoint coverage for most objects, computed by projecting object orientations onto a unit sphere. (Chen et al., 2022) `ev:measured` p. 7 ^chen2022clearpose-030
- Plates, forks and large bowls have reduced viewpoint coverage because they can only be placed in certain orientations. (Chen et al., 2022) `ev:reported` p. 7 ^chen2022clearpose-031
- ORB-SLAM3 sometimes could not estimate camera pose in extreme transparent clutter, where background RGB features are heavily distorted. (Chen et al., 2022) `ev:reported` p. 8 ^chen2022clearpose-032
- Ground truth depth images are generated by overlaying rendered object CAD model depth onto the original depth images. (Chen et al., 2022) `ev:reported` p. 8 ^chen2022clearpose-033
- Labeling one scene takes around 30 minutes with this pipeline, including visual SLAM, manual pose alignment and output rendering. (Chen et al., 2022) `ev:reported` p. 8 ^chen2022clearpose-034
- For benchmarking, around 200K images are selected for training, with 2K images randomly sampled for each of six test cases. (Chen et al., 2022) `ev:reported` p. 9 ^chen2022clearpose-035
- ImplicitDepth and TransCG serve as [[Transparent object depth completion|depth completion baselines]], both trained following their original papers' iterations and hyper-parameters. (Chen et al., 2022) `ev:reported` p. 9 ^chen2022clearpose-036
- TransCG surpassed ImplicitDepth in most depth completion tests on ClearPose while using fewer training iterations. (Chen et al., 2022) `ev:measured` p. 9 ^chen2022clearpose-037
- The authors suggest this implies methods using DFNet can outperform designs using voxel-based PointNet for [[Transparent object depth completion|transparent depth completion]]. (Chen et al., 2022) `ev:asserted` p. 9 ^chen2022clearpose-038
- Both [[Transparent object depth completion|depth completion methods]] perform poorly in Translucent Cover scenes and achieve their best performance in New Background scenes. (Chen et al., 2022) `ev:measured` p. 9 ^chen2022clearpose-039
- The authors state that Filled Liquid, Opaque Distractor and Non Planar variations do not substantially impact depth completion accuracy. (Chen et al., 2022) `ev:measured` p. 9 ^chen2022clearpose-040
- On New Background scenes, TransCG reached an RMSE of 0.03 and δ1.05 of 86.50, versus 0.07 and 67.00 for ImplicitDepth. (Chen et al., 2022) `ev:measured` p. 10 ^chen2022clearpose-041
- On Translucent Cover scenes, TransCG reached δ1.05 of 23.44, close to the 22.85 obtained by ImplicitDepth. (Chen et al., 2022) `ev:measured` p. 10 ^chen2022clearpose-042
- On Non Planar test scenes of ClearPose, ImplicitDepth reached a δ1.05 of 20.34, compared with 55.31 for TransCG. (Chen et al., 2022) `ev:measured` p. 10 ^chen2022clearpose-043
- The authors re-implemented the transparent pose estimation method of Xu et al. because it had no publicly available source code. (Chen et al., 2022) `ev:reported` p. 9 ^chen2022clearpose-044
- The Xu et al. re-implementation trains Mask R-CNN for instance segmentation and DeepLabv3 for surface normal estimation in its first stage. (Chen et al., 2022) `ev:reported` p. 11 ^chen2022clearpose-045
- Xu et al. is compared with FFB6D, a state-of-the-art RGB-D pose estimator originally designed for opaque objects. (Chen et al., 2022) `ev:reported` p. 11 ^chen2022clearpose-046
- FFB6D was run with raw, ground truth and TransCG-completed depth in different training and testing combinations. (Chen et al., 2022) `ev:reported` p. 11 ^chen2022clearpose-047
- In the pose benchmark, Accuracy is the percentage of pose estimates on the test set with [[ADD and ADD-S metrics|ADD error]] less than 10cm. (Chen et al., 2022) `ev:reported` p. 12 ^chen2022clearpose-048
- On New Background, FFB6D trained and tested on ground truth depth reached 59.694 accuracy, versus 44.264 with raw depth. (Chen et al., 2022) `ev:measured` p. 11 ^chen2022clearpose-049
- On Opaque Distractor scenes, Xu et al. reached 42.630 accuracy, compared with at most 2.3525 for any FFB6D variant. (Chen et al., 2022) `ev:measured` p. 11 ^chen2022clearpose-050
- On Filled Liquid scenes, Xu et al. reached 34.500 accuracy, compared with 16.228 for FFB6D trained and tested on ground truth. (Chen et al., 2022) `ev:measured` p. 11 ^chen2022clearpose-051
- On Translucent Cover scenes, FFB6D with raw depth reached 5.5617 accuracy, compared with 13.433 when trained and tested on ground truth. (Chen et al., 2022) `ev:measured` p. 11 ^chen2022clearpose-052
- Within FFB6D, the upper bound performance appears when the network is both trained and tested on ground truth depth. (Chen et al., 2022) `ev:measured` p. 12 ^chen2022clearpose-053
- The authors conclude that inaccurate depth would be the difficulty for transparent object pose estimation. (Chen et al., 2022) `ev:asserted` p. 12 ^chen2022clearpose-054
- New Background is generally the easiest pose estimation test case, with accuracy dropping a lot in the other scenarios. (Chen et al., 2022) `ev:measured` p. 13 ^chen2022clearpose-055
- Xu et al. is much better than FFB6D variants in Opaque Distractor and Filled Liquid scenes, according to the authors. (Chen et al., 2022) `ev:measured` p. 13 ^chen2022clearpose-056
- The authors suggest unseen colors mixing in transparent objects may add noise to FFB6D keypoint regression as one possible reason. (Chen et al., 2022) `ev:asserted` p. 13 ^chen2022clearpose-057
- Pose estimation accuracy on transparent objects remains much worse than on opaque objects, which reach ADD-S around 90 on public datasets. (Chen et al., 2022) `ev:asserted` p. 13 ^chen2022clearpose-058
- ClearPose excludes colored transparent materials, objects with markers or labels, and objects with opaque parts, focusing on pure transparency. (Chen et al., 2022) `ev:reported` p. 13 ^chen2022clearpose-059
- The benchmark does not include a complete list of recent state-of-the-art approaches due to compute and time limitations. (Chen et al., 2022) `ev:reported` p. 13 ^chen2022clearpose-060
- The authors propose [[Category-level object pose estimation|category-level pose estimation for transparent objects]] as an extension, since ClearPose has categories with similar shape. (Chen et al., 2022) `ev:asserted` p. 13 ^chen2022clearpose-061
- Because of transparency or translucency, some image pixels could belong to more than one object in cluttered and covered scenes. (Chen et al., 2022) `ev:asserted` p. 14 ^chen2022clearpose-062
- The authors conclude there is still much room for improvement in heavy clutter, liquid-filled objects and translucent-covered scenes. (Chen et al., 2022) `ev:asserted` p. 14 ^chen2022clearpose-063
- The 3D CAD models were manually created in Blender from measured real object sizes, with dimensions verified during labeling. (Chen et al., 2022) `ev:reported` p. 17 ^chen2022clearpose-064
- The RealSense camera records aligned RGB-depth pairs around 30Hz under normal room light, and 10-20Hz in other scenes. (Chen et al., 2022) `ev:reported` p. 17 ^chen2022clearpose-065
- FFB6D requires eight 3D keypoints per object, generated at equal intervals along the symmetric axis for axial-symmetric objects. (Chen et al., 2022) `ev:reported` p. 18 ^chen2022clearpose-066

## 🎯 Contributions

## 📖 Glossary

- **Depth completion** — Recovering missing or wrong depth values in a sensor depth image.
- **ADD** — Average Euclidean distance between corresponding model points at ground truth and predicted pose.
- **ADD-S** — Symmetric variant using each predicted point's minimum distance to the ground-truth point cloud.
- **ProgressLabeller** — SLAM-based interactive tool aligning CAD models to multi-view RGB-D video for pose labels.
- **δ1.05** — Percentage of pixels whose predicted-to-true depth ratio lies within 1.05.
- **Non-planar configuration** — Objects placed on surfaces at multiple heights rather than one table plane.

## ❓ Open questions

- How do RGB-only pose estimators compare with RGB-D methods on transparent objects with broken depth?
- How well does category-level pose estimation work on ClearPose's shape-similar categories?
- Which detection and segmentation annotation rules suit pixels shared by several overlapping transparent objects?
- Why does training on ground truth and testing on completed depth not improve FFB6D over raw depth?
- How do these perception results transfer to grasping and manipulation in the six test scenarios?

## 📝 Notes on reading

The cached text is arXiv 2203.03890v2 (21 Jul 2022), including supplementary material on pp. 17–19; the supplement's figures (setup photos, keypoint sets) could only be described.

Inconsistency: the text on p. 9 says Filled Liquid, Opaque Distractor and Non Planar do not substantially impact depth completion accuracy, but Table 2 (p. 10) shows ImplicitDepth RMSE rising from 0.07 (New Background) to 0.14–0.18 in those scenes and TransCG δ1.05 dropping to 52.43 and 55.31 in Opaque Distractor and Non Planar.

The benchmark introduction (p. 9) announces both instance-level and category-level RGB-D pose estimation, but only instance-level results (Table 3) appear.

The sentence on p. 12 that ground-truth-trained, completed-depth-tested FFB6D "almost display the same accuracy" does not name its comparison; Table 3 shows it close to the raw/raw variant, which is how it was claimed.

Table 1's StereObj1M counts are estimates by the authors; Trans10K has segmentation labels only. Figures 1–8 (sample images, object CAD models, viewpoint coverage, annotation pipeline, qualitative results, multi-layer appearance) were described, not claimed.

## Suggested new concepts

- Transparent object depth completion — a recurring task with several benchmarked methods (ImplicitDepth, TransCG, ClearGrasp) worth its own note.
- Multi-layer transparent appearance — pixels belonging to several objects challenges standard masks and NMS, a distinct annotation problem.
- SLAM-based pose annotation — marker-free labeling via visual SLAM and silhouette alignment, reusable beyond this dataset.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Benchmark de pose de objetos transparentes (con líquidos)

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
