---
aliases: []
type: "source"
title: "MegaPose: 6D Pose Estimation of Novel Objects via Render & Compare"
citekey: "Labbe2022megapose"
doi: "10.48550/arXiv.2212.06870"
arxiv: "2212.06870"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2212.06870"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Yann Labbé", "Lucas Manuelli", "Arsalan Mousavian", "Stephen Tyree", "Stan Birchfield", "Jonathan Tremblay", "Justin Carpentier", "Mathieu Aubry", "Dieter Fox", "Josef Sivic"]
sha256: ["b3fae7874a49074eb0070136d77235540adf3fe4ff8526943535c12b230d95dd"]
pdf: "Content/Papers/Labbe2022megapose.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Labbe2022megapose.pdf]]

> [!abstract] One-sentence summary
> MegaPose estimates the 6D pose of objects never seen in training from a CAD model and a region of interest, using a render-and-compare refiner and a classification-based coarse estimator trained on 2 million synthetic images of thousands of objects, reaching accuracy competitive with object-specific methods on BOP.

## Abstract

We introduce MegaPose, a method to estimate the 6D pose of novel objects, that is, objects unseen during training. At inference time, the method only assumes knowledge of (i) a region of interest displaying the object in the image and (ii) a CAD model of the observed object. The contributions of this work are threefold. First, we present a 6D pose refiner based on a render&compare strategy which can be applied to novel objects. The shape and coordinate system of the novel object are provided as inputs to the network by rendering multiple synthetic views of the object's CAD model. Second, we introduce a novel approach for coarse pose estimation which leverages a network trained to classify whether the pose error between a synthetic rendering and an observed image of the same object can be corrected by the refiner. Third, we introduce a large-scale synthetic dataset of photorealistic images of thousands of objects with diverse visual and shape properties and show that this diversity is crucial to obtain good generalization performance on novel objects. We train our approach on this large synthetic dataset and apply it without retraining to hundreds of novel objects in real images from several pose estimation benchmarks. Our approach achieves state-of-the-art performance on the ModelNet and YCB-Video datasets. An extensive evaluation on the 7 core datasets of the BOP challenge demonstrates that our approach achieves performance competitive with existing approaches that require access to the target objects during training. Code, dataset and trained models are available on the project page: https://megapose6d.github.io/. (arXiv)

## 🧠 Key ideas (atomic)

- MegaPose estimates the [[Novel-object 6D pose estimation|6D pose of novel objects]], meaning objects unseen during training, given only a region of interest plus a CAD model. (Labbé et al., 2022) `ev:asserted` p. 1 ^labbe2022megapose-001
- Current state-of-the-art learning-based pose methods require hours or days to generate synthetic data for each object and train the model. (Labbé et al., 2022) `ev:cited` p. 1 ^labbe2022megapose-002
- [[Category-level object pose estimation|Category-level pose estimation methods]] generalize to novel instances of known classes but not to instances outside their training categories. (Labbé et al., 2022) `ev:cited` p. 1 ^labbe2022megapose-003
- The authors argue that non-learned pipeline components cannot benefit from training on large data to gain robustness to noise, occlusions or object variability. (Labbé et al., 2022) `ev:asserted` p. 2 ^labbe2022megapose-004
- The approach splits pose estimation into 2D detection, coarse pose estimation, and [[Render-and-compare pose refinement|iterative refinement via render and compare]], taking inspiration from CosyPose. (Labbé et al., 2022) `ev:reported` p. 2 ^labbe2022megapose-005
- Detection of novel objects is outside the scope of the paper, which focuses on the coarse and refinement networks for 6D pose. (Labbé et al., 2022) `ev:asserted` p. 2 ^labbe2022megapose-006
- In existing [[Render-and-compare pose refinement|render-and-compare refiners]], object appearance and coordinate system are encoded in the network weights, leading to poor generalization on novel objects. (Labbé et al., 2022) `ev:cited` p. 2 ^labbe2022megapose-007
- Direct regression methods for coarse pose estimation are trained with [[Symmetry-aware pose loss|symmetry-specific losses]], requiring object symmetries to be known in advance. (Labbé et al., 2022) `ev:cited` p. 2 ^labbe2022megapose-008
- The shape and coordinate system of a novel object are given to the refiner by rendering multiple synthetic views of its CAD model. (Labbé et al., 2022) `ev:reported` p. 2 ^labbe2022megapose-009
- [[Synthetic training data for 6D pose estimation|The synthetic training dataset]] consists of 2 million photorealistic images depicting over 20K models in physically plausible configurations. (Labbé et al., 2022) `ev:reported` p. 2 ^labbe2022megapose-010
- When depth is available, the RGB and depth images are concatenated before being passed into the network. (Labbé et al., 2022) `ev:reported` p. 3 ^labbe2022megapose-011
- For each rendered pose hypothesis, the coarse network predicts a score classifying whether the hypothesis lies within the basin of attraction of the refiner. (Labbé et al., 2022) `ev:reported` p. 4 ^labbe2022megapose-012
- The highest-scoring pose hypothesis from the coarse network is used as the initial pose for the refinement step. (Labbé et al., 2022) `ev:reported` p. 4 ^labbe2022megapose-013
- Since coarse estimation is framed as classification, the method can implicitly handle [[Pose ambiguity from symmetry|object symmetries]], as multiple poses can be classified as correct. (Labbé et al., 2022) `ev:asserted` p. 4 ^labbe2022megapose-014
- The refiner renders images so the anchor point projects to the image center, letting the network infer it from multiple distinct viewpoints. (Labbé et al., 2022) `ev:reported` p. 4 ^labbe2022megapose-015
- Both the coarse and refiner networks consist of a ResNet-34 backbone followed by spatial average pooling and a single fully-connected layer. (Labbé et al., 2022) `ev:reported` p. 5 ^labbe2022megapose-016
- The refiner network outputs 9 values that specify the translation and rotation of the pose update. (Labbé et al., 2022) `ev:reported` p. 5 ^labbe2022megapose-017
- Refiner training perturbations sample rotation as random Euler angles with a standard deviation of 15 degrees in each axis. (Labbé et al., 2022) `ev:reported` p. 5 ^labbe2022megapose-018
- The coarse model is trained with binary cross entropy, taking positives from the refiner perturbation distribution and sufficiently distinct poses as negatives. (Labbé et al., 2022) `ev:reported` p. 5 ^labbe2022megapose-019
- [[BOP benchmark|The seven core BOP datasets]] used for evaluation exhibit 132 different objects in cluttered scenes with occlusions. (Labbé et al., 2022) `ev:reported` p. 6 ^labbe2022megapose-020
- Using PPF and SIFT pose hypotheses, MegaPose coarse selection plus refinement achieves a +10.7 AR score improvement over Zephyr on YCB-V. (Labbé et al., 2022) `ev:measured` p. 6 ^labbe2022megapose-021
- Averaged across the YCB-V and LM-O datasets, the approach reaches an AR score of 59.7 compared to 55.7 for Zephyr. (Labbé et al., 2022) `ev:measured` p. 6 ^labbe2022megapose-022
- With Mask-RCNN detections, the MegaPose coarse estimator alone reaches a mean AR score of 16.2 across the seven BOP datasets. (Labbé et al., 2022) `ev:measured` p. 6 ^labbe2022megapose-023
- The [[Render-and-compare pose refinement|RGB-D refinement network]] improves the coarse estimates by +41.0 mean AR score on the BOP datasets. (Labbé et al., 2022) `ev:measured` p. 6 ^labbe2022megapose-024
- The full MegaPose coarse plus refiner pipeline reaches a mean BOP AR of 54.5 with RGB input. (Labbé et al., 2022) `ev:measured` p. 6 ^labbe2022megapose-025
- The full MegaPose coarse plus refiner pipeline reaches [[BOP benchmark|a mean BOP AR]] of 57.2 with RGB-D input. (Labbé et al., 2022) `ev:measured` p. 6 ^labbe2022megapose-026
- MegaPose performance is competitive with the learning-based CosyPose refiner, which reaches 57.0 mean AR, without being trained on the test objects. (Labbé et al., 2022) `ev:measured` p. 6 ^labbe2022megapose-027
- SurfEmb performs better than MegaPose on BOP, reaching a mean AR of 75.2 with BFGS plus ICP refinement on RGB-D. (Labbé et al., 2022) `ev:measured` p. 6 ^labbe2022megapose-028
- According to the authors, SurfEmb heavily relies on knowledge of the objects for training and cannot generalize to novel objects. (Labbé et al., 2022) `ev:cited` p. 6 ^labbe2022megapose-029
- Applying the [[Render-and-compare pose refinement|MegaPose RGB-D refiner]] to CosyPose coarse estimates improves accuracy by +23.7 AR on average across BOP datasets. (Labbé et al., 2022) `ev:measured` p. 6 ^labbe2022megapose-030
- The RGB-only MegaPose refiner on CosyPose coarse estimates reaches mean AR 59.6, above 57.0 for the CosyPose refiner trained on BOP objects. (Labbé et al., 2022) `ev:measured` p. 6 ^labbe2022megapose-031
- The authors credit this to training on thousands of various objects, whereas CosyPose is trained on only tens of objects per dataset. (Labbé et al., 2022) `ev:asserted` p. 6 ^labbe2022megapose-032
- One [[Render-and-compare pose refinement|iteration of the refiner]] takes approximately 50 milliseconds on a RTX 2080 GPU, which the authors deem suitable for online tracking. (Labbé et al., 2022) `ev:measured` p. 7 ^labbe2022megapose-033
- Five refiner iterations are 5 times faster than the object-specific SurfEmb refiner, which takes around 1 second per image crop. (Labbé et al., 2022) `ev:measured` p. 7 ^labbe2022megapose-034
- On ModelNet, the RGB-D refiner reaches average recall of 97.6, 98.9 and 97.5 for the (5°, 5cm), ADD (0.1d) and Proj2D metrics. (Labbé et al., 2022) `ev:measured` p. 7 ^labbe2022megapose-035
- On ModelNet, the RGB-D refiner outperforms LatentFusion, which reaches 85.5, 94.3 and 94.7 on the same three recall metrics. (Labbé et al., 2022) `ev:measured` p. 7 ^labbe2022megapose-036
- For the ModelNet comparison, ShapeNet categories overlapping the ModelNet test categories were removed from training to evaluate on novel categories. (Labbé et al., 2022) `ev:reported` p. 7 ^labbe2022megapose-037
- For the [[Render-and-compare pose refinement|RGB-only refiner]], BOP5 average recall rises from 52.0 to 61.7 as rendered views increase from 1 to 4. (Labbé et al., 2022) `ev:measured` p. 8 ^labbe2022megapose-038
- Removing rendered normal maps from the 4-view RGB-only refiner lowers ModelNet ADD(0.1d) recall from 96.1 to 83.1. (Labbé et al., 2022) `ev:measured` p. 8 ^labbe2022megapose-039
- Scaling training objects from 10 + 100 to 1000 + 20000 GSO+ShapeNet models raises ModelNet ADD(0.1d) recall from 28.7 to 96.1. (Labbé et al., 2022) `ev:measured` p. 8 ^labbe2022megapose-040
- The authors suggest performance could improve as more datasets of high-quality CAD models like GSO become available. (Labbé et al., 2022) `ev:asserted` p. 8 ^labbe2022megapose-041
- Training the refiner on 1000 GSO objects alone gives 62.2 BOP5 average recall, compared with 61.7 for GSO plus ShapeNet. (Labbé et al., 2022) `ev:measured` p. 8 ^labbe2022megapose-042
- The authors hypothesize that the value of GSO for BOP performance is due to its high-quality textured objects. (Labbé et al., 2022) `ev:asserted` p. 8 ^labbe2022megapose-043
- Training on the 132 BOP test objects themselves gives 62.6 BOP5 average recall, a small benefit over GSO-based training. (Labbé et al., 2022) `ev:measured` p. 8 ^labbe2022megapose-044
- The most common failure mode of MegaPose is inaccurate initial pose estimates from the coarse model, which the refiner cannot correct. (Labbé et al., 2022) `ev:asserted` p. 8 ^labbe2022megapose-045
- The coarse model uses M = 520 pose hypotheses per object, which take around 2.5 seconds to render and evaluate. (Labbé et al., 2022) `ev:measured` p. 8 ^labbe2022megapose-046
- In a tracking scenario, the coarse model runs once at the initial frame, after which the refiner tracks the object at 20Hz. (Labbé et al., 2022) `ev:reported` p. 8 ^labbe2022megapose-047
- The authors state that detecting any unknown object given only a CAD model remains a difficult problem still to be solved. (Labbé et al., 2022) `ev:asserted` p. 8 ^labbe2022megapose-048
- The refiner loss follows CosyPose but uses no symmetry information, which is typically unavailable for large CAD datasets like ShapeNet. (Labbé et al., 2022) `ev:reported` p. 13 ^labbe2022megapose-049
- The refiner loss is summed over K = 3 refinement iterations, without backpropagating gradients through rendering and iterations. (Labbé et al., 2022) `ev:reported` p. 14 ^labbe2022megapose-050
- Coarse training places 104 cameras around each perturbed pose, giving one positive and 103 negatives for the classifier. (Labbé et al., 2022) `ev:reported` p. 15 ^labbe2022megapose-051
- At test time, P = 5 random orientations each expand into 104 viewpoints, giving a total of 520 pose hypotheses. (Labbé et al., 2022) `ev:reported` p. 15 ^labbe2022megapose-052
- Training takes respectively 32 and 48 hours for the coarse and refiner models, using 32 V-100 GPUs. (Labbé et al., 2022) `ev:reported` p. 15 ^labbe2022megapose-053
- Selecting among Halcon PPF hypotheses, the MegaPose coarse network reaches 61.6 AR on YCB-V versus 59.8 for Zephyr scoring. (Labbé et al., 2022) `ev:measured` p. 16 ^labbe2022megapose-054
- On LM-O, the MegaPose coarse network reaches 52.1 AR, compared with 45.8 for Zephyr scoring of the same hypotheses. (Labbé et al., 2022) `ev:measured` p. 16 ^labbe2022megapose-055
- A regression-based coarse network similar to CosyPose collapsed during training, giving performance close to zero on the BOP datasets. (Labbé et al., 2022) `ev:measured` p. 16 ^labbe2022megapose-056
- The authors hypothesize the regression collapse stems from symmetric training objects producing ambiguous gradients during training. (Labbé et al., 2022) `ev:asserted` p. 16 ^labbe2022megapose-057
- Increasing the number of coarse pose hypotheses from M=104 to M=520 improves performance on BOP5 by +11.4 AR. (Labbé et al., 2022) `ev:measured` p. 16 ^labbe2022megapose-058
- Beyond M=520 the performance improvement is marginal, with 4608 coarse pose hypotheses adding only +0.9 AR. (Labbé et al., 2022) `ev:measured` p. 16 ^labbe2022megapose-059
- In a qualitative grasping experiment, a RealSense D415 camera on a Franka Emika Panda gripper provided single RGB images for MegaPose. (Labbé et al., 2022) `ev:reported` p. 17 ^labbe2022megapose-060
- The orientation of textureless objects that look similar under different viewpoints, such as a red bowl, may be incorrectly predicted. (Labbé et al., 2022) `ev:measured` p. 18 ^labbe2022megapose-061
- A CAD model with incorrect scale leads to incorrect object depth estimates, due to the scale/depth ambiguity in RGB images. (Labbé et al., 2022) `ev:asserted` p. 18 ^labbe2022megapose-062
- The approach correctly estimated poses of LineMOD Occlusion objects whose low-fidelity CAD models have poor textures or missing geometry. (Labbé et al., 2022) `ev:measured` p. 20 ^labbe2022megapose-063

## 🎯 Contributions


## 📖 Glossary

- **Novel object** — Object whose CAD model is available only at inference, never seen in training.
- **Render & compare** — Refinement by rendering the object at the current pose and comparing with the image.
- **Basin of attraction** — Range of initial pose errors the refiner can still correct to the true pose.
- **Anchor point** — 3D reference point on the object whose translation the pose update predicts.
- **AR score** — BOP average recall combining several pose error metrics.
- **BOP5** — Mean recall over LM-O, T-LESS, TUD-L, IC-BIN and YCB-V.
- **ADD (0.1d)** — Recall of poses with mean model-point distance below 10% of object diameter.
- **Coarse pose estimation** — Selecting an initial pose hypothesis before iterative refinement.

## ❓ Open questions

- How can novel objects be detected zero-shot from only a CAD model, to complete the pipeline?
- Can the refiner's basin of attraction be enlarged so fewer coarse hypotheses are needed?
- How can the coarse model disambiguate objects whose poses differ only in fine details, such as scissors handles?
- How much does performance degrade when CAD model scale or geometry is wrong beyond the qualitative examples shown?
- Would a faster coarse estimator (e.g., template-based) keep accuracy while cutting the 520-hypothesis runtime?

## 📝 Notes on reading

Read the arXiv v1 preprint (2212.06870v1, CoRL 2022 version), matching the packet identifier.

Inconsistencies inside the paper: the Table 1 caption says Zephyr is row 11, but Zephyr is row 6 and row 11 is the MegaPose coarse-only model. The text on p. 6 says the refiner is applied to CosyPose coarse estimates in row 11, but the CosyPose coarse-only row is row 8. Coarse runtime for M = 520 is given as around 2.5 seconds (p. 8), 1.6 seconds (p. 16), and the appendix mentions a 4s figure from an earlier line 276; the appendix also compares M=520 against 0.3 seconds for M=120 after discussing M=104. Refiner perturbation translation standard deviations of (0.02, 0.02, 0.05) are labelled centimeters (pp. 5, 14), which looks implausibly small; not claimed.

Figures only described: Fig. 1 (training/inference/robot overview), Fig. 2 (coarse and refiner architecture), Fig. 3 qualitative coarse vs refined results, Fig. 4 training images, Fig. 5 TUD-L illumination robustness, Fig. 6 per-object YCB-V success rates (values not extractable), Fig. 7 failure modes, Fig. 8 low-fidelity CAD models. Appendix equations for the pose update, anchor-point dependency, loss and depth normalization were extracted with broken layout; only their stated conclusions are claimed.

## Suggested new concepts

- Render-and-compare pose refinement — core technique shared by DeepIM, CosyPose and MegaPose.
- Novel-object 6D pose estimation — distinct task setting (CAD model at test time only) with its own benchmarks and methods.
- Classification-based coarse pose scoring — alternative to regression that handles symmetries without explicit labels.
- Large-scale synthetic training data for pose — object diversity as the driver of generalization.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Pose de objetos nuevos con solo CAD

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
