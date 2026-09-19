---
aliases: []
type: "source"
title: "TransNet: Transparent Object Manipulation Through Category-Level Pose Estimation"
citekey: "Zhang2023transnet"
doi: "10.48550/arXiv.2307.12400"
arxiv: "2307.12400"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2307.12400"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Huijie Zhang", "Anthony Opipari", "Xiaotong Chen", "Jiyue Zhu", "Zeren Yu", "Odest Chadwicke Jenkins"]
sha256: ["ffa08957c4c4926648cb8115362bf1b7e0c9c3d573534915fcf16de6bd56276a"]
pdf: "Content/Papers/Zhang2023transnet.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 58
---

📄 PDF: [[Zhang2023transnet.pdf]]

> [!abstract] One-sentence summary
> TransNet estimates category-level 6D pose and 3D scale of unseen transparent objects from RGB-D by learning on completed depth, surface normals and ray directions, beating GPV-Pose on ClearPose and driving robot pick-and-place and pouring.

## Abstract

Transparent objects present multiple distinct challenges to visual perception systems. First, their lack of distinguishing visual features makes transparent objects harder to detect and localize than opaque objects. Even humans find certain transparent surfaces with little specular reflection or refraction, like glass doors, difficult to perceive. A second challenge is that depth sensors typically used for opaque object perception cannot obtain accurate depth measurements on transparent surfaces due to their unique reflective properties. Stemming from these challenges, we observe that transparent object instances within the same category, such as cups, look more similar to each other than to ordinary opaque objects of that same category. Given this observation, the present paper explores the possibility of category-level transparent object pose estimation rather than instance-level pose estimation. We propose \textit{\textbf{TransNet}}, a two-stage pipeline that estimates category-level transparent object pose using localized depth completion and surface normal estimation. TransNet is evaluated in terms of pose estimation accuracy on a large-scale transparent object dataset and compared to a state-of-the-art category-level pose estimation approach. Results from this comparison demonstrate that TransNet achieves improved pose estimation accuracy on transparent objects. Moreover, we use TransNet to build an autonomous transparent object manipulation system for robotic pick-and-place and pouring tasks. (arXiv)

## 🧠 Key ideas (atomic)

- Given an RGB-D image of a scene with transparent objects, TransNet estimates the 6D pose plus 3D scale of each object for manipulation. (Zhang et al., 2023) `ev:asserted` p. 1 ^zhang2023transnet-001
- The authors state that common commercially available depth sensors record mostly invalid or inaccurate depth values within the transparent region of objects. (Zhang et al., 2023) `ev:asserted` p. 1 ^zhang2023transnet-002
- The color appearance of transparent objects is highly dependent on background, viewing angle, material and lighting condition, due to reflection and refraction. (Zhang et al., 2023) `ev:asserted` p. 1 ^zhang2023transnet-003
- Recent works grasp transparent objects by completing the missing depth values, followed by the use of a geometry-based grasp engine. (Zhang et al., 2023) `ev:cited` p. 1 ^zhang2023transnet-004
- Instance-level transparent object poses could be estimated from keypoints on stereo RGB images, a light-field camera, or a single RGB-D image. (Zhang et al., 2023) `ev:cited` p. 1 ^zhang2023transnet-005
- To the best of the authors' knowledge, TransNet is [[Category-level object pose estimation|the first category-level pose estimation approach]] developed specifically for transparent objects. (Zhang et al., 2023) `ev:asserted` p. 2 ^zhang2023transnet-006
- ClearGrasp trained three DeepLabv3+ models to learn transparency mask, surface normal, and boundary, using depth completion for robotic grasping tasks. (Zhang et al., 2023) `ev:cited` p. 2 ^zhang2023transnet-007
- The authors state that [[Category-level object pose estimation|category-level pose techniques for opaque objects]] require high-quality depth input provided by objects with Lambertian light reflectance. (Zhang et al., 2023) `ev:asserted` p. 2 ^zhang2023transnet-008
- TransNet first applies a fine-tuned Mask R-CNN to obtain each object's bounding box, segmentation mask and category label from the image. (Zhang et al., 2023) `ev:reported` p. 2 ^zhang2023transnet-009
- In the first stage, depth completion plus surface normal estimation are applied on RGB-D patches to obtain depth-normal pairs through cross-task consistency learning. (Zhang et al., 2023) `ev:reported` p. 2 ^zhang2023transnet-010
- In the second stage, the pose is estimated separately in four decoder modules for object translation, x-axis, z-axis, and scale. (Zhang et al., 2023) `ev:reported` p. 2 ^zhang2023transnet-011
- TransNet uses TransCG for depth completion, with a U-Net surface normal estimator that takes the completed depth as its input. (Zhang et al., 2023) `ev:reported` p. 3 ^zhang2023transnet-012
- The depth completion and surface normal networks are first trained separately with L2 losses, then trained together using a cross-task consistency loss. (Zhang et al., 2023) `ev:reported` p. 3 ^zhang2023transnet-013
- After cross-task consistency training, the depth completion and surface normal networks are frozen and used to generate input for the second stage. (Zhang et al., 2023) `ev:reported` p. 3 ^zhang2023transnet-014
- The generalized point cloud concatenates RGB, ray direction, estimated depth and estimated surface normal, sampling N pixels within the transparent mask. (Zhang et al., 2023) `ev:reported` p. 3 ^zhang2023transnet-015
- TransNet encodes the generalized point cloud with Pointformer, a multi-stage transformer-based point cloud embedding method, to produce per-point object features. (Zhang et al., 2023) `ev:reported` p. 3 ^zhang2023transnet-016
- A Point Pooling layer, an MLP with max-pooling, extracts global features that are concatenated with local features plus a one-hot category label. (Zhang et al., 2023) `ev:reported` p. 3 ^zhang2023transnet-017
- The translation decoder learns a 3D residual from a prior computed as the average predicted 3D coordinate over the sampled pixels. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023transnet-018
- Rotation is decoupled into separately estimated x-axis and z-axis, with learned confidence values handling regressed axes that are not orthogonal. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023transnet-019
- The scale decoder learns a residual from a scale prior defined as the average scale of all object CAD models within each category. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023transnet-020
- Evaluation used 33 object instances from 3 ClearPose categories, namely bowl, water cup, and wine cup, from the Clearpose dataset. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023transnet-021
- The training set uses 25 of the objects, totaling 190K RGB-D images, all of which were used to train the models. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023transnet-022
- Testing used 8 objects not seen during training, uniformly sampled into a representative 5K image test set out of 60K test images. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023transnet-023
- For experiments in the ablation study and baseline comparison, input patches were generated from ground truth instance segmentations of the objects. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023transnet-024
- For the robot experiments, input patches were generated by a Mask R-CNN model fine-tuned on the Clearpose dataset instead of ground truth. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023transnet-025
- Image patches were generated from object bounding boxes and re-scaled to a fixed shape of 256 × 256 pixels before entering TransNet. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023transnet-026
- Cross-task consistency training used the AdamW optimizer with a learning rate of 1e−3, following the perceptual loss strategy of Zamir et al. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023transnet-027
- The second stage was trained with the Ranger optimizer, using a linear warm-up for the first 1000 iterations of training. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023transnet-028
- All pose estimation experiments were trained on a 16G RTX3080 GPU until loss convergence, according to the implementation details. (Zhang et al., 2023) `ev:reported` p. 5 ^zhang2023transnet-029
- Pose accuracy was measured with 3D intersection over union at 25%, 50% and 75% thresholds, following GPV-Pose and FS-Net. (Zhang et al., 2023) `ev:reported` p. 5 ^zhang2023transnet-030
- The baseline, GPV-Pose, is a state-of-the-art categorical opaque object pose model, trained with estimated depth from TransCG for fair comparison. (Zhang et al., 2023) `ev:reported` p. 5 ^zhang2023transnet-031
- On the Clearpose dataset, TransNet outperformed the GPV-Pose baseline in most of the pose estimation metrics reported in Table I. (Zhang et al., 2023) `ev:measured` p. 5 ^zhang2023transnet-032
- On the 3D75 metric, TransNet reached 39.9 against 13.2 for GPV-Pose, around a 3 × improvement. (Zhang et al., 2023) `ev:measured` p. 5 ^zhang2023transnet-033
- On the strict 5◦5cm metric, TransNet reached 22.7 against 2.7 for GPV-Pose, around an 8 × improvement. (Zhang et al., 2023) `ev:measured` p. 5 ^zhang2023transnet-034
- With estimated depth as input, Pointformer embedding reached 28.4 on 3D75, compared with 17.6 for 3D-GCN embedding. (Zhang et al., 2023) `ev:measured` p. 6 ^zhang2023transnet-035
- With ground truth depth as input, 3D-GCN embedding reached 70.9 on 5◦5cm, compared with 61.9 for Pointformer embedding. (Zhang et al., 2023) `ev:measured` p. 6 ^zhang2023transnet-036
- The authors suggest Pointformer shares information across the whole point cloud, possibly contributing to increased robustness when input data is noisy. (Zhang et al., 2023) `ev:asserted` p. 5 ^zhang2023transnet-037
- The authors argue that given depth with large uncertainty, transformer-based embedding might be more powerful than nearest-neighbour embedding methods. (Zhang et al., 2023) `ev:asserted` p. 5 ^zhang2023transnet-038
- Adding estimated surface normals to the generalized point cloud raised 3D75 from 28.4 to 34.4 in the ablation study. (Zhang et al., 2023) `ev:measured` p. 6 ^zhang2023transnet-039
- The authors infer that surface normals serve as a good complement when depth estimation is not accurate, as in the transparent setting. (Zhang et al., 2023) `ev:asserted` p. 5 ^zhang2023transnet-040
- Adding ray-direction input raised 3D50 from 61.6 to 81.6 in the ablation study comparing trial 3 with trial 4. (Zhang et al., 2023) `ev:measured` p. 6 ^zhang2023transnet-041
- The authors hypothesize that ray-direction input is critical for the network to model accurate 3D spatial relationships between points. (Zhang et al., 2023) `ev:asserted` p. 6 ^zhang2023transnet-042
- Adding cross-task consistency training raised the 5◦5cm metric from 13.0 to 15.8 in the TransNet ablation study. (Zhang et al., 2023) `ev:measured` p. 6 ^zhang2023transnet-043
- Cross-task consistency lowered the surface normal mean angular error from 11.43 to 8.96 degrees on depth-normal pair estimation. (Zhang et al., 2023) `ev:measured` p. 6 ^zhang2023transnet-044
- Depth completion RMSE stayed nearly unchanged with cross-task consistency, at 0.056 without it versus 0.057 with it. (Zhang et al., 2023) `ev:measured` p. 6 ^zhang2023transnet-045
- Training a separate model per category raised 5◦5cm from 15.8 to 22.7 compared with training one model on multiple categories. (Zhang et al., 2023) `ev:measured` p. 6 ^zhang2023transnet-046
- The ablation study informed Trial 6 as the final TransNet architecture, which was the one used in the robot experiments. (Zhang et al., 2023) `ev:reported` p. 5 ^zhang2023transnet-047
- The authors note that the trial 1 model and GPV-Pose both use 3D-GCN, differing only in using the generalized point cloud. (Zhang et al., 2023) `ev:asserted` p. 6 ^zhang2023transnet-048
- The authors hypothesize that ray-direction information degrades after being multiplied directly with noisy depth to form the GPV-Pose point cloud input. (Zhang et al., 2023) `ev:asserted` p. 6 ^zhang2023transnet-049
- The robot experiments used a Fetch robot with an Intel RealSense L515 camera, the same sensor used in the ClearPose dataset. (Zhang et al., 2023) `ev:reported` p. 6 ^zhang2023transnet-050
- For grasping, the approach direction is orthogonal to the object's symmetrical axis, with the grasp location at the object's center point. (Zhang et al., 2023) `ev:reported` p. 6 ^zhang2023transnet-051
- For placing, target gripper poses align the object's estimated bottom surface parallel to the target location surface with a 2 cm offset. (Zhang et al., 2023) `ev:reported` p. 6 ^zhang2023transnet-052
- In pick-and-place with water cups, the robot picked 16/20 times (80%) and placed 12/16 picked cups successfully (75%). (Zhang et al., 2023) `ev:measured` p. 7 ^zhang2023transnet-053
- In pick-and-place with wine cups, the robot picked 13/20 times (65%) and placed 12/13 picked cups successfully (92.3%). (Zhang et al., 2023) `ev:measured` p. 7 ^zhang2023transnet-054
- In pouring with a water cup and bowl, the robot picked 15/20 times (75%) and poured successfully 10/15 times (66.7%). (Zhang et al., 2023) `ev:measured` p. 7 ^zhang2023transnet-055
- In pouring with a wine cup and bowl, the robot picked 14/20 times (70%) and poured successfully 11/14 times (78.6%). (Zhang et al., 2023) `ev:measured` p. 7 ^zhang2023transnet-056
- The poses and scales used by the robot are output directly from TransNet without any additional post-processing step. (Zhang et al., 2023) `ev:reported` p. 7 ^zhang2023transnet-057
- The authors report observing a performance gap between perceiving glass and plastic objects, suggesting object material information as a future direction. (Zhang et al., 2023) `ev:asserted` p. 7 ^zhang2023transnet-058

## 🎯 Contributions

## 📖 Glossary

- **Category-level pose estimation** — Estimating 6D pose and scale of unseen objects belonging to categories seen in training.
- **Generalized point cloud** — Per-pixel concatenation of RGB, ray direction, completed depth and surface normal features.
- **Ray direction** — Unit vector from camera origin to each pixel, encoding intrinsics and pixel position.
- **Cross-task consistency** — Training depth and normal networks so their predictions agree with each other.
- **Depth completion** — Filling missing or wrong sensor depth values, here within transparent object regions.
- **3D IoU (3D25/50/75)** — Share of estimates whose 3D box overlap exceeds 25, 50 or 75 percent.
- **5◦5cm metric** — Share of pose estimates with rotation error under 5 degrees and translation under 5 cm.
- **Pointformer** — Multi-stage transformer-based point cloud embedding network, from 6D-ViT.

## ❓ Open questions

- How much of the gap to opaque-object pose accuracy could material-aware (glass versus plastic) modeling close?
- How does TransNet behave in heavily cluttered scenes beyond the qualitative failures shown in Figure 4?
- How well does TransNet generalize beyond the three ClearPose categories (bowl, water cup, wine cup)?
- How much does pose accuracy drop when predicted Mask R-CNN segmentations replace the ground truth masks used in the ablations?
- Would a single multi-category model close the gap to per-category models with more training data?

## 📝 Notes on reading

- Version read: arXiv v1 preprint (2307.12400v1, 23 Jul 2023), matching the packet identifier.
- Table I full row (Clearpose): GPV-Pose 95.4 / 65.1 / 13.2 / 2.7 / 12.5 / 15.5 versus TransNet 97.3 / 80.3 / 39.9 / 22.7 / 45.4 / 50.6 (3D25, 3D50, 3D75, 5◦5cm, 10◦5cm, 10◦10cm); only the headline 3D75 and 5◦5cm rows were claimed.
- Figure 4 caption (qualitative only, not claimed): the bottom row shows inaccurate TransNet estimates in heavily cluttered scenes; ground-truth x-axis is used to draw boxes for axially symmetric objects.
- Table II checkmark columns are garbled in the extraction; which modality each trial lacks was inferred from the text on pp. 5–6 (trial 2 lacks normals, trial 3 lacks ray direction).
- Inconsistency: Table II trial 2 (Pointformer, estimated depth) lists 10◦5cm 8.0 and 10◦10cm 29.6, while the identical configuration in Table III lists 29.6 and 35.3; the other four values match. The 8.0 looks like a typo. These trial-2 values were not claimed.
- Inconsistency: the dataset paragraph (p. 4) lists the robot objects as 1 bowl and 1 wine cup from the test set plus 1 new wine cup and 2 new water cups, while the robot section (p. 6) says 3 water cups, 2 wine cups and 1 bowl.
- The text says Pointformer beats 3D-GCN on most metrics with estimated depth; with ground-truth depth (Table III), 3D-GCN is higher on 5◦5cm, 10◦5cm and 10◦10cm.
- Table IV shows cross-task consistency barely changes depth metrics (δ1.25 even drops from 98.89 to 98.57); the gain is mainly in surface normals (11.25◦ accuracy 56.75 to 73.62). Consistency also raised 3D75 from 34.4 to 39.2 (trial 4 to 5).
- The Clearpose test objects total 60K images, but experiments use only a 5K uniformly sampled subset.
- Figures 1, 2, 3 and 5 are described only (pipeline overview, architecture diagram, object sets, robot demos).
- The paper compares against one baseline only (GPV-Pose); the conclusion speaks of 'baselines' in the plural.

## Suggested new concepts

- Transparent object depth completion — recurring prerequisite for transparent object grasping and pose pipelines (ClearGrasp, TransCG, Dex-NeRF).
- Category-level object pose estimation — core task family (NOCS, GPV-Pose, FS-Net) that TransNet extends to transparent objects.
- Cross-task consistency learning — training scheme from Zamir et al. used to couple depth and surface normal predictions.
- ClearPose dataset — large-scale transparent object RGB-D benchmark used for training and evaluation here.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H7.** Une la pose por categoría con los objetos transparentes e incluye pick-and-place y vertido robótico con vasos.

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
