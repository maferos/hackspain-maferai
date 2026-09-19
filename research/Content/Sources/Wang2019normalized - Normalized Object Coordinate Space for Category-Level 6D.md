---
aliases: []
type: "source"
title: "Normalized Object Coordinate Space for Category-Level 6D Object Pose and Size Estimation"
citekey: "Wang2019normalized"
doi: "10.48550/arXiv.1901.02970"
arxiv: "1901.02970"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1901.02970"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["He Wang", "Srinath Sridhar", "Jingwei Huang", "Julien Valentin", "Shuran Song", "Leonidas J. Guibas"]
sha256: ["d99c86f41430df0e41c7375cd4bf561405bed1d971303f39ffc2c11e21053931"]
pdf: "Content/Papers/Wang2019normalized.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 65
---

📄 PDF: [[Wang2019normalized.pdf]]

> [!abstract] One-sentence summary
> The paper introduces NOCS, a shared normalized canonical space per category, and a Mask R-CNN extension that predicts NOCS maps which, combined with depth, give metric 6D pose and size of unseen object instances, supported by the CAMERA mixed-reality and REAL275 datasets.

## Abstract

The goal of this paper is to estimate the 6D pose and dimensions of unseen object instances in an RGB-D image. Contrary to "instance-level" 6D pose estimation tasks, our problem assumes that no exact object CAD models are available during either training or testing time. To handle different and unseen object instances in a given category, we introduce a Normalized Object Coordinate Space (NOCS)---a shared canonical representation for all possible object instances within a category. Our region-based neural network is then trained to directly infer the correspondence from observed pixels to this shared object representation (NOCS) along with other object information such as class label and instance mask. These predictions can be combined with the depth map to jointly estimate the metric 6D pose and dimensions of multiple objects in a cluttered scene. To train our network, we present a new context-aware technique to generate large amounts of fully annotated mixed reality data. To further improve our model and evaluate its performance on real data, we also provide a fully annotated real-world dataset with large environment and instance variation. Extensive experiments demonstrate that the proposed method is able to robustly estimate the pose and size of unseen object instances in real environments while also achieving state-of-the-art performance on standard 6D pose estimation benchmarks. (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that instance-level 6D pose methods, which need exact CAD models and sizes, cannot be used for objects never seen before. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019normalized-001
- Category-level 3D object detection methods estimate viewpoint-dependent 3D bounding boxes that do not encode the precise orientation of objects, according to the authors. (Wang et al., 2019) `ev:cited` p. 1 ^wang2019normalized-002
- The paper presents, to the authors' knowledge, the first method for [[Category-level object pose estimation|category-level 6D pose and size estimation]] of multiple objects. (Wang et al., 2019) `ev:asserted` p. 1 ^wang2019normalized-003
- In [[Normalized Object Coordinate Space|the Normalized Object Coordinate Space]], all instances within a category are consistently oriented inside a common normalized space. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019normalized-004
- A convolutional neural network jointly estimates the object class, instance mask, and a NOCS map of multiple objects from a single RGB image. (Wang et al., 2019) `ev:reported` p. 2 ^wang2019normalized-005
- [[Normalized Object Coordinate Space|The NOCS map]] captures the normalized shape of visible object parts by predicting dense correspondences between object pixels and the NOCS. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019normalized-006
- The mixed reality method automatically generates 275K training and 25K testing images of ShapeNetCore objects composited with real tabletop scenes. (Wang et al., 2019) `ev:reported` p. 2 ^wang2019normalized-007
- The real-world dataset contains 18 different scenes with ground truth 6D pose and size annotations for 6 categories and 42 unique instances. (Wang et al., 2019) `ev:reported` p. 2 ^wang2019normalized-008
- The authors state their datasets are, to their knowledge, the largest and most comprehensive for 6D pose and size estimation. (Wang et al., 2019) `ev:asserted` p. 2 ^wang2019normalized-009
- Prior category-level pose methods constrain rotation prediction to the gravity direction only, giving just four degrees of freedom. (Wang et al., 2019) `ev:cited` p. 2 ^wang2019normalized-010
- The method runs at 0.5 s per frame, which the authors compare with ∼70 s and 25 mins per frame for two alternative approaches. (Wang et al., 2019) `ev:measured` p. 3 ^wang2019normalized-011
- [[Normalized Object Coordinate Space|NOCS]] is a 3D space within a unit cube, where each shape is uniformly scaled so its tight bounding-box diagonal has length 1. (Wang et al., 2019) `ev:reported` p. 3 ^wang2019normalized-012
- The authors argue [[Normalized Object Coordinate Space|NOCS maps]] are more robust than bounding boxes since they can operate when the object is only partially visible. (Wang et al., 2019) `ev:asserted` p. 3 ^wang2019normalized-013
- The CNN does not use the depth map because the authors want to exploit RGB datasets without depth, like COCO, to improve performance. (Wang et al., 2019) `ev:asserted` p. 3 ^wang2019normalized-014
- The CNN is built upon the Mask R-CNN framework, extended to jointly predict NOCS maps in addition to class labels and instance masks. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019normalized-015
- The CAMERA approach composites synthetic foreground objects into real background images with plausible physical locations, lighting, and scale. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019normalized-016
- The CAMERA backgrounds are 553 real RGB-D images of 31 indoor scenes, 4 of which were set aside for validation. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019normalized-017
- The six object categories are bottle, bowl, camera, can, laptop, and mug, with an extra distractor category of other objects. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019normalized-018
- The curated ShapeNetCore collection consists of 1085 individual object instances, of which 184 instances were set aside for validation. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019normalized-019
- A plane detection algorithm segments supporting surfaces in real images, on which synthetic objects are placed at randomly sampled locations and orientations. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019normalized-020
- In total the authors render 300K composited images with CAMERA, of which 25K are set aside for validation. (Wang et al., 2019) `ev:reported` p. 4 ^wang2019normalized-021
- The mixed reality compositing technique was implemented in the Unity game engine with custom plugins for plane detection and point sampling. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019normalized-022
- The real data comprise 8K RGB-D frames, 4300 for training, 950 for validation and 2750 for testing, captured with a Structure Sensor. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019normalized-023
- Real training and testing subsets each use 6 categories with 3 unique instances per category; validation uses 1 instance per category. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019normalized-024
- Each of the three NOCS heads outputs a 28×28×N map per region of interest, where N is the number of categories. (Wang et al., 2019) `ev:reported` p. 5 ^wang2019normalized-025
- The authors' experiments revealed that pixel classification of NOCS values with B = 32 bins performed better than direct regression. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019normalized-026
- For regression the NOCS heads use a soft L1 loss, quadratic for errors up to 0.1 and linear above it. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019normalized-027
- [[Normalized Object Coordinate Space|The NOCS representation]] does not take symmetries into account, which resulted in large errors for some object classes. (Wang et al., 2019) `ev:measured` p. 6 ^wang2019normalized-028
- [[Symmetry-aware pose loss|The symmetric loss]] takes the minimum loss over ground truth NOCS maps rotated about a predefined symmetry axis for each category. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019normalized-029
- The authors found that at most 6 rotations about the symmetry axis are enough to handle most symmetric categories. (Wang et al., 2019) `ev:asserted` p. 6 ^wang2019normalized-030
- The ResNet50 backbone, RPN and FPN are initialized with weights trained on 2D instance segmentation on the COCO dataset. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019normalized-031
- Training uses a batch size of 2, an initial learning rate of 0.001, and SGD with a momentum of 0.9. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019normalized-032
- Training proceeds in three stages of 10K, 3K and 70K iterations, progressively unfreezing ResNet50 layers and dividing the learning rate by 10. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019normalized-033
- Pose and size come from aligning [[Normalized Object Coordinate Space|the NOCS point cloud]] to the masked depth point cloud with the Umeyama algorithm and RANSAC. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019normalized-034
- For the symmetric categories bottle, bowl, and can, the predicted 3D bounding box may rotate freely about the vertical axis without penalty. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019normalized-035
- Knowing of no other category-level method, the authors built a baseline of Mask R-CNN without NOCS heads plus ICP alignment to a random category model. (Wang et al., 2019) `ev:reported` p. 6 ^wang2019normalized-036
- Trained only on the CAMERA training set, the method achieves an mAP of 83.9% for 3D IoU at 50% on CAMERA25. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-037
- On CAMERA25 with CAMERA-only training, the method achieves an mAP of 40.9% for the strict (5°, 5 cm) pose metric. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-038
- For REAL275, each minibatch samples images from CAMERA*, 20K COCO images, and REAL* with probabilities of 60%, 20%, and 20%. (Wang et al., 2019) `ev:reported` p. 7 ^wang2019normalized-039
- On the REAL275 real-world test set, the best NOCS model achieves an mAP of 76.4% for 3D IoU at 50%. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-040
- On REAL275, the best NOCS model achieves an mAP of 10.2% at (5°, 5 cm) and 23.1% at (10°, 5 cm). (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-041
- On REAL275, the Mask R-CNN plus ICP baseline achieves an mAP of 43.8% for 3D IoU at 50%. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-042
- On REAL275, the baseline achieves an mAP of 0.8% for both the (5°, 5 cm) and (10°, 5 cm) metrics. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-043
- The authors interpret that predicting [[Normalized Object Coordinate Space|dense NOCS maps]] provides detailed information about object shape, parts, and visibility, which is critical for pose estimation. (Wang et al., 2019) `ev:asserted` p. 7 ^wang2019normalized-044
- In the training-data ablation on REAL275, using only CAMERA* data results in poor performance, which the authors attribute to domain gap. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-045
- Training only on REAL*, or on REAL* and COCO, tends to overfit to the training data due to small dataset size. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-046
- Training on CAMERA* with COCO and REAL* gives the best results in the data ablation, reaching 72.4 AP at 3D IoU 50%. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-047
- With COCO and REAL*, non-context-aware composited data reaches 71.7 AP at 3D IoU 50%, versus 72.4 for context-aware CAMERA data. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-048
- Pixel classification is consistently better than regression for NOCS prediction on both the CAMERA25 and REAL275 evaluation sets. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-049
- In the architecture ablation, using 32 bins is best for pose estimation, while 128 bins is better on detection. (Wang et al., 2019) `ev:measured` p. 7 ^wang2019normalized-050
- Without [[Symmetry-aware pose loss|the symmetry loss]], REAL275 regression accuracy at (5°, 5 cm) drops from 8.1 to 1.3 mAP. (Wang et al., 2019) `ev:measured` p. 8 ^wang2019normalized-051
- On CAMERA25, removing [[Symmetry-aware pose loss|the symmetry loss]] lowers regression (5°, 5 cm) mAP from 29.2 to 14.7. (Wang et al., 2019) `ev:measured` p. 8 ^wang2019normalized-052
- The OccludedLINEMOD dataset has 9 object instances, each with a CAD model, and 1214 images annotated with ground truth 6D pose. (Wang et al., 2019) `ev:reported` p. 8 ^wang2019normalized-053
- For OccludedLINEMOD, 15% of the dataset is randomly selected for training and supplemented with 15000 synthetic images. (Wang et al., 2019) `ev:reported` p. 8 ^wang2019normalized-054
- On OccludedLINEMOD, the 32-bin classification network achieves a detection rate of 94.7% and an mAP of 88.4% for 3D IoU at 50%. (Wang et al., 2019) `ev:measured` p. 8 ^wang2019normalized-055
- On OccludedLINEMOD, the 32-bin network achieves an mAP of 13.9% at (5°, 5 cm) and 33.5% at (10°, 5 cm). (Wang et al., 2019) `ev:measured` p. 8 ^wang2019normalized-056
- On OccludedLINEMOD, PoseCNN without iterative pose refinement achieves an mAP of only 1.7%, as reported in prior work. (Wang et al., 2019) `ev:cited` p. 8 ^wang2019normalized-057
- On OccludedLINEMOD the method achieves 30.2% mAP on 2D projection at 5 pixel, versus 17.2% reported for PoseCNN. (Wang et al., 2019) `ev:measured` p. 8 ^wang2019normalized-058
- The authors conclude that [[Category-level object pose estimation|their category-level approach]] can also achieve state-of-the-art performance on standard 6D pose estimation benchmarks. (Wang et al., 2019) `ev:asserted` p. 8 ^wang2019normalized-059
- A stated limitation is that pose estimation is conditioned on region proposals and category predictions, which could be incorrect and hurt results. (Wang et al., 2019) `ev:asserted` p. 8 ^wang2019normalized-060
- A stated limitation is that the approach relies on the depth image to lift NOCS predictions to real-world coordinates. (Wang et al., 2019) `ev:asserted` p. 8 ^wang2019normalized-061
- The authors suggest future work should investigate estimating category-level 6D pose and size directly from RGB images alone. (Wang et al., 2019) `ev:asserted` p. 8 ^wang2019normalized-062
- With 640×360 input, the network runs at around 4 fps on an Intel Xeon Gold 5122 desktop with a NVIDIA TITAN Xp. (Wang et al., 2019) `ev:measured` p. 9 ^wang2019normalized-063
- On average, the implementation takes 210 ms for neural network inference and 34 ms for pose alignment with the Umeyama algorithm. (Wang et al., 2019) `ev:measured` p. 9 ^wang2019normalized-064
- Observed failure modes on real data include missing detection, wrong classification, and inconsistency in the predicted coordinate maps. (Wang et al., 2019) `ev:measured` p. 9 ^wang2019normalized-065

## 🎯 Contributions

## 📖 Glossary

- **NOCS** — Normalized Object Coordinate Space: a unit-cube canonical space shared by all instances of a category.
- **NOCS map** — Per-pixel image of predicted NOCS coordinates, i.e. dense pixel-to-canonical-shape correspondences.
- **Category-level pose estimation** — Estimating pose of unseen instances of known categories without their exact CAD models.
- **CAMERA** — Context-Aware MixEd ReAlity: compositing synthetic objects onto detected planes in real tabletop images.
- **REAL275** — The paper's real-world RGB-D test set of 2.75K annotated frames.
- **Umeyama algorithm** — Closed-form least-squares estimate of similarity transform (scale, rotation, translation) between point sets.
- **(5°, 5 cm) metric** — Average precision of poses with rotation error under 5° and translation error under 5 cm.
- **Symmetry loss** — Loss taking the minimum over ground truths rotated about a category's symmetry axis.

## ❓ Open questions

- Can category-level 6D pose and size be estimated from RGB alone, without depth to lift NOCS predictions?
- How can errors in region proposals and category predictions be kept from propagating into the pose estimate?
- How well does NOCS generalize beyond the six tabletop categories, e.g. to articulated or highly variable shapes?
- How much of the remaining sim-to-real gap is closed by more real training data versus better compositing realism?
- Can symmetries be handled without hand-defining a per-category symmetry axis and rotation set?

## 📝 Notes on reading

Read the arXiv v2 preprint (23 Jun 2019), which includes supplementary appendices A–D on pp. 9–11.

Inconsistencies inside the paper: p. 3 gives 0.5 s per frame, while Appendix A (p. 9) reports around 4 fps (210 ms + 34 ms). The REAL275 (5°, 5 cm) result is 10.2% in the text (p. 7) but 10.0 for the 32-bin network in Table 2 (p. 8); the text does not say which network variant produced the 10.2%. The regression row on REAL275 reads 23.7 for (10°, 10cm) in Table 1 but 23.1 in Table 2. Table 1's caption says "3D25 and 3D25" where the second should be 3D50. In Table 2, removing the symmetry loss raises REAL275 3D detection AP (82.7 vs 79.6) while pose accuracy collapses.

Tables 1 and 2 were extracted as columns of numbers; rows were reconstructed from the column order and only headline values were claimed. Figures 6, 7, 9 and 13 are AP-vs-threshold plots and a comparison chart whose values are not in the text; they were not claimed. Figures 1–5, 8, 10–12 are illustrations or qualitative results.

The OccludedLINEMOD PoseCNN 1.7% figure is taken by the authors from DeepIM [30], not re-run; the text does not name the metric it refers to.

## Suggested new concepts

- Normalized Object Coordinate Space (NOCS) — a canonical per-category representation reused by much later category-level pose work.
- Category-level 6D pose estimation — a problem setting distinct from instance-level pose, central to manipulating unseen lab objects.
- Context-aware mixed reality data generation — a sim-to-real data strategy relevant to our simulated lab scenes.
- Symmetry-aware pose loss — a general technique for rotationally symmetric objects such as bottles and vials.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H7.** Introduce la pose y el tamaño por categoría (NOCS, CAMERA, REAL275), clave para frascos de 6 tamaños sin CAD por instancia.
