---
aliases: []
type: "source"
title: "BOP Challenge 2023 on Detection, Segmentation and Pose Estimation of Seen and Unseen Rigid Objects"
citekey: "Hodan2024bop"
doi: "10.48550/arXiv.2403.09799"
arxiv: "2403.09799"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2403.09799"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Tomas Hodan", "Martin Sundermeyer", "Yann Labbe", "Van Nguyen Nguyen", "Gu Wang", "Eric Brachmann", "Bertram Drost", "Vincent Lepetit", "Carsten Rother", "Jiri Matas"]
sha256: ["c94145f10e53118ba275591faf6469e2bf29ca07bf19f322fd354f0dc968e5d2"]
pdf: "Content/Papers/Hodan2024bop.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Hodan2024bop.pdf]]

> [!abstract] One-sentence summary
> The BOP Challenge 2023 report defines six model-based detection, segmentation and 6D localization tasks, adds unseen-object variants with a 5-minute onboarding limit, and shows that the best unseen-object method reaches 2020 seen-object accuracy while run time and occluded-object detection remain the main gaps.

## Abstract

We present the evaluation methodology, datasets and results of the BOP Challenge 2023, the fifth in a series of public competitions organized to capture the state of the art in model-based 6D object pose estimation from an RGB/RGB-D image and related tasks. Besides the three tasks from 2022 (model-based 2D detection, 2D segmentation, and 6D localization of objects seen during training), the 2023 challenge introduced new variants of these tasks focused on objects unseen during training. In the new tasks, methods were required to learn new objects during a short onboarding stage (max 5 minutes, 1 GPU) from provided 3D object models. The best 2023 method for 6D localization of unseen objects (GenFlow) notably reached the accuracy of the best 2020 method for seen objects (CosyPose), although being noticeably slower. The best 2023 method for seen objects (GPose) achieved a moderate accuracy improvement but a significant 43% run-time improvement compared to the best 2022 counterpart (GDRNPP). Since 2017, the accuracy of 6D localization of seen objects has improved by more than 50% (from 56.9 to 85.6 AR_C). The online evaluation system stays open and is available at: http://bop.felk.cvut.cz/. (arXiv)

## 🧠 Key ideas (atomic)

- [[BOP benchmark|The BOP Challenge 2023]] was the fifth in a series of public challenges recording the state of the art in 6D object pose estimation. (Hodan et al., 2024) `ev:reported` p. 1 ^hodan2024bop-001
- Participants of the 2023 challenge competed on six tasks, three from 2022 and three [[Novel-object 6D pose estimation|new variants focused on objects unseen during training]]. (Hodan et al., 2024) `ev:reported` p. 1 ^hodan2024bop-002
- In the new tasks, methods had to onboard novel 3D object models within at most 5 minutes per object on 1 GPU. (Hodan et al., 2024) `ev:reported` p. 1 ^hodan2024bop-003
- The authors argue that [[Novel-object 6D pose estimation|unseen-object methods]] are practically relevant because they avoid expensive data generation and training for every new object. (Hodan et al., 2024) `ev:asserted` p. 1 ^hodan2024bop-004
- The challenge primarily focuses on the practical scenario where only 3D object models and synthesized images are available at training or onboarding time. (Hodan et al., 2024) `ev:reported` p. 1 ^hodan2024bop-005
- The introduction of the unseen-object tasks was encouraged by recent breakthroughs in foundation models and their few-shot learning capabilities. (Hodan et al., 2024) `ev:asserted` p. 1 ^hodan2024bop-006
- Since 2017, the accuracy of 6D localization of seen objects improved by more than 50%, from 56.9 to 85.6 ARC. (Hodan et al., 2024) `ev:measured` p. 1 ^hodan2024bop-007
- In 2020 the learning-based CosyPose ended the dominance of point-pair-feature methods at the price of a significantly higher run time. (Hodan et al., 2024) `ev:measured` p. 1 ^hodan2024bop-008
- In the 2019 challenge, depth-based methods mostly built on point pair features clearly outperformed RGB-only methods, all of which used deep networks. (Hodan et al., 2024) `ev:measured` p. 2 ^hodan2024bop-009
- For the 2020 challenge the organizers provided [[Synthetic training data for 6D pose estimation|350K physically-based rendered training images]] produced with BlenderProc2. (Hodan et al., 2024) `ev:reported` p. 2 ^hodan2024bop-010
- [[Synthetic training data for 6D pose estimation|The PBR training images]] helped DNN-based methods catch up with PPF-based methods in the 2020 challenge. (Hodan et al., 2024) `ev:measured` p. 2 ^hodan2024bop-011
- In 2022, DNN-based methods for 6D object localization clearly outperformed PPF-based methods in both accuracy and speed. (Hodan et al., 2024) `ev:measured` p. 2 ^hodan2024bop-012
- In 2022 the gap between methods trained only on PBR images and methods also trained on real images noticeably shrank. (Hodan et al., 2024) `ev:measured` p. 2 ^hodan2024bop-013
- Since 2022 the challenge also evaluates 2D detection and segmentation, to address most recent pose methods, which first detect or segment objects. (Hodan et al., 2024) `ev:reported` p. 2 ^hodan2024bop-014
- Direct comparison of prior unseen-object methods had been difficult due to variations in the detection stage and the training data used. (Hodan et al., 2024) `ev:asserted` p. 2 ^hodan2024bop-015
- CNOS, a model-based method for detecting and segmenting unseen objects, was employed as the default 2D detection and segmentation method. (Hodan et al., 2024) `ev:reported` p. 2 ^hodan2024bop-016
- [[Synthetic training data for 6D pose estimation|Synthetic training data from MegaPose]] were used as the unified training dataset for the unseen-object tasks. (Hodan et al., 2024) `ev:reported` p. 2 ^hodan2024bop-017
- Methods were not required but were encouraged through dedicated awards to use the unified detection and training solutions. (Hodan et al., 2024) `ev:reported` p. 2 ^hodan2024bop-018
- The best 2023 seen-object method, GPose, achieved a 42.6% run time improvement over GDRNPP, the best 2022 counterpart. (Hodan et al., 2024) `ev:measured` p. 2 ^hodan2024bop-019
- Pose errors are computed with three functions: Visible Surface Discrepancy, Maximum Symmetry-Aware Surface Distance, and Maximum Symmetry-Aware Projection Distance. (Hodan et al., 2024) `ev:reported` p. 2 ^hodan2024bop-020
- The per-dataset accuracy ARD is defined as the average of the Average Recall scores for VSD, MSSD and MSPD. (Hodan et al., 2024) `ev:reported` p. 3 ^hodan2024bop-021
- The overall accuracy on the core datasets, ARC, is defined as the average of the per-dataset accuracy scores. (Hodan et al., 2024) `ev:reported` p. 3 ^hodan2024bop-022
- 2D detection accuracy follows COCO and averages precision over IoU thresholds from 0.5 to 0.95 per object. (Hodan et al., 2024) `ev:reported` p. 3 ^hodan2024bop-023
- Only annotated instances with at least 10% of their projected surface visible need to be detected or localized. (Hodan et al., 2024) `ev:reported` p. 3 ^hodan2024bop-024
- In the 2D detection tasks, ground-truth bounding boxes are amodal, covering the whole object silhouette including occluded parts. (Hodan et al., 2024) `ev:reported` p. 3 ^hodan2024bop-025
- For unseen-object onboarding, methods may render images of the 3D models but may not use any real images. (Hodan et al., 2024) `ev:reported` p. 3 ^hodan2024bop-026
- The object representation must remain fixed after onboarding and cannot be updated on test images. (Hodan et al., 2024) `ev:reported` p. 3 ^hodan2024bop-027
- [[BOP benchmark|BOP]] includes twelve datasets in a unified format, seven of which were selected as core datasets. (Hodan et al., 2024) `ev:reported` p. 4 ^hodan2024bop-028
- All test images in [[BOP benchmark|the BOP datasets]] are real, while training images may be real or synthetic. (Hodan et al., 2024) `ev:reported` p. 4 ^hodan2024bop-029
- For Tasks 4–6, the organizers provided over 2M images showing more than 50K diverse objects, originally synthesized for MegaPose. (Hodan et al., 2024) `ev:reported` p. 4 ^hodan2024bop-030
- Symmetry transformations are not available for the MegaPose training objects, which come from Google Scanned Objects and ShapeNetCore. (Hodan et al., 2024) `ev:reported` p. 4 ^hodan2024bop-031
- In total 65 methods were fully evaluated on Task 1, 14 on Task 4, 3 on Task 5, and 4 on Task 6. (Hodan et al., 2024) `ev:reported` p. 5 ^hodan2024bop-032
- A method had to use a fixed set of hyper-parameters across all objects and datasets in the challenge. (Hodan et al., 2024) `ev:reported` p. 5 ^hodan2024bop-033
- Onboarding could use as many BOP 2020 BlenderProc images as would fit in 5 minutes, counting 2 seconds per rendered image. (Hodan et al., 2024) `ev:reported` p. 5 ^hodan2024bop-034
- Camera angle ranges and camera-object distance ranges from test poses were the only test-set information allowed during training and onboarding. (Hodan et al., 2024) `ev:reported` p. 5 ^hodan2024bop-035
- The authors observe that GenFlow tends to fail on challenging cases with heavy object occlusion in sample LM-O and YCB-V images. (Hodan et al., 2024) `ev:measured` p. 5 ^hodan2024bop-036
- Among the 16 new 2023 entries on Task 1, three outperform GDRNPP, the best method from the 2022 challenge. (Hodan et al., 2024) `ev:measured` p. 5 ^hodan2024bop-037
- GPose2023 achieves 85.6 ARC on Task 1, outperforming GDRNPP by 1.9 ARC with less than half the inference time. (Hodan et al., 2024) `ev:measured` p. 5 ^hodan2024bop-038
- GPose2023 uses the same pose estimation method as GDRNPP, combined with coordinate-guided pose refinement and an improved YOLOv8-based detector. (Hodan et al., 2024) `ev:reported` p. 5 ^hodan2024bop-039
- Without pose refinement, RGB-only variants GPose2023-RGB and ZebraPoseSAT-EffnetB4 reach an average inference time of about 0.25 seconds per image. (Hodan et al., 2024) `ev:measured` p. 5 ^hodan2024bop-040
- On Task 1, accuracy gains are most notable on the industrial ITODD, T-LESS, and HB datasets. (Hodan et al., 2024) `ev:measured` p. 5 ^hodan2024bop-041
- On the TUD-L and [[YCB-Video dataset|YCB-V]] datasets, the authors observe that Task 1 accuracy metrics start to saturate. (Hodan et al., 2024) `ev:measured` p. 5 ^hodan2024bop-042
- GDet2023, based on YOLOv8, achieves 79.8 APC in 2D detection of seen objects, a +2.5 APC gain over YOLOX. (Hodan et al., 2024) `ev:measured` p. 5 ^hodan2024bop-043
- Trained only on [[Synthetic training data for 6D pose estimation|synthetic PBR images]], the YOLOv8-based detector still achieves 76.9 APC on seen-object detection. (Hodan et al., 2024) `ev:measured` p. 5 ^hodan2024bop-044
- In 2D segmentation of seen objects, ZebraPoseSAT achieves a +3.2 APC improvement by predicting masks from default GDRNPP detections. (Hodan et al., 2024) `ev:measured` p. 5 ^hodan2024bop-045
- Vidal-Sensors18, a 2019 point-pair-feature method using depth only, reaches 56.9 ARC with 3.22s per image on Task 1. (Hodan et al., 2024) `ev:measured` p. 6 ^hodan2024bop-046
- CosyPose-ECCV20-SYNT+REAL-ICP, the best 2020 entry in Table 3, reaches 69.8 ARC at 13.74s per image. (Hodan et al., 2024) `ev:measured` p. 6 ^hodan2024bop-047
- GDRNPP-PBRReal-RGBD-MModel-Fast reaches 80.5 ARC on Task 1 with an average processing time of 0.23s per image. (Hodan et al., 2024) `ev:measured` p. 6 ^hodan2024bop-048
- MegaPose, the Task 4 baseline, estimates coarse pose by template matching against renderings, then refines the pose by [[Render-and-compare pose refinement|render-and-compare]]. (Hodan et al., 2024) `ev:reported` p. 7 ^hodan2024bop-049
- The RGB-only MegaPose entry achieves 54.9 ARC, improving to 62.8 ARC with RGB-D images and Teaser++ refinement. (Hodan et al., 2024) `ev:measured` p. 7 ^hodan2024bop-050
- GenFlow-MultiHypo16, the best method for [[Novel-object 6D pose estimation|6D localization of unseen objects]], reaches 67.4 ARC on the seven core datasets. (Hodan et al., 2024) `ev:measured` p. 7 ^hodan2024bop-051
- The authors call GenFlow's accuracy comparable to CosyPose, the best 2020 method for 6D localization of seen objects. (Hodan et al., 2024) `ev:measured` p. 7 ^hodan2024bop-052
- GenFlow improves MegaPose's coarse pose stage by running the coarse network in a GMM-based hierarchical manner. (Hodan et al., 2024) `ev:reported` p. 7 ^hodan2024bop-053
- For refinement, GenFlow adapts a recurrent flow network to estimate a visibility mask and uses a differentiable PnP solver. (Hodan et al., 2024) `ev:reported` p. 7 ^hodan2024bop-054
- GenFlow-MultiHypo16 improved run time 4x compared to MegaPose but still takes 34.58s per image on Task 4. (Hodan et al., 2024) `ev:measured` p. 7 ^hodan2024bop-055
- SAM6D is the fastest Task 4 method by a significant margin at 3.87s per image, reaching 61.6 ARC. (Hodan et al., 2024) `ev:measured` p. 7 ^hodan2024bop-056
- The authors state that run time is a significant challenge for [[Novel-object 6D pose estimation|6D localization of unseen objects]]. (Hodan et al., 2024) `ev:asserted` p. 7 ^hodan2024bop-057
- CNOS-FastSAM, the best unseen-object method, reaches 42.8 mAPC in 2D detection of unseen objects on Task 5. (Hodan et al., 2024) `ev:measured` p. 7 ^hodan2024bop-058
- CNOS-FastSAM reaches 41.2 mAP in 2D segmentation of unseen objects on Task 6 of the challenge. (Hodan et al., 2024) `ev:measured` p. 7 ^hodan2024bop-059
- CNOS-FastSAM's unseen-object segmentation accuracy is comparable to Mask R-CNN, which reached 40.5 mAPC in 2020 after training on more than 1M images. (Hodan et al., 2024) `ev:measured` p. 7 ^hodan2024bop-060
- CNOS-FastSAM relies on DINOv2 features extracted from only 200 rendered reference views of each target object. (Hodan et al., 2024) `ev:reported` p. 7 ^hodan2024bop-061
- All submitted unseen-object detection and segmentation approaches rely on SAM-like methods to segment object instances in the image. (Hodan et al., 2024) `ev:reported` p. 7 ^hodan2024bop-062
- Amodal detection of occluded instances leads to a gap of 37 mAPC between CNOS and GDet2023. (Hodan et al., 2024) `ev:measured` p. 7 ^hodan2024bop-063
- Combined with default GDRNPPDet detections, GenFlow-MultiHypo16 achieves 79.2 ARC, only 5.9 ARC behind GDRNPPDet plus GPose2023. (Hodan et al., 2024) `ev:measured` p. 7 ^hodan2024bop-064
- The authors conclude that better unseen-object detection methods would provide great potential for improving unseen-object pose localization. (Hodan et al., 2024) `ev:asserted` p. 7 ^hodan2024bop-065
- Although accuracy starts saturating on seen-object tasks, top methods still need to improve efficiency to support real-time applications. (Hodan et al., 2024) `ev:asserted` p. 8 ^hodan2024bop-066
- The authors identify great potential in improving detection of occluded objects for the unseen-object tasks. (Hodan et al., 2024) `ev:asserted` p. 8 ^hodan2024bop-067
- The organizers plan a harder future variant in which only reference images of each object are provided for onboarding. (Hodan et al., 2024) `ev:asserted` p. 8 ^hodan2024bop-068

## 🎯 Contributions

## 📖 Glossary

- **6D object pose** — 3D rotation plus 3D translation mapping an object model into camera space.
- **6D localization** — Pose estimation when the objects and instance counts in the image are given.
- **Onboarding** — Limited stage where a method learns a new object from its 3D model.
- **Seen / unseen objects** — Objects present, or absent, in the training data of a method.
- **ARC** — Average of per-dataset Average Recall scores over the seven BOP core datasets.
- **APC** — COCO-style Average Precision averaged over the BOP core datasets.
- **VSD / MSSD / MSPD** — The three BOP pose-error functions used to compute Average Recall.
- **PBR images** — Physically-based rendered synthetic training images, generated here with BlenderProc.
- **Amodal box** — Bounding box covering the whole object silhouette, including occluded parts.
- **Modal mask** — Segmentation mask covering only the visible part of an object.
- **Point pair features (PPF)** — Classical depth-based descriptors pairing oriented surface points for pose voting.
- **Render-and-compare** — Refining a pose by comparing renderings of the model with the image.

## ❓ Open questions

- How can unseen-object 6D localization be made fast enough for real-time use while keeping GenFlow-level accuracy?
- How much of the seen/unseen pose gap would close with better amodal detection of occluded unseen objects?
- How will methods perform when onboarding uses only reference images instead of 3D mesh models?
- Are TUD-L and YCB-V still informative benchmarks once Task 1 metrics saturate on them?
- Would identifying symmetries for the MegaPose training objects change unseen-object results?

## 📝 Notes on reading

Read the arXiv v2 (16 Apr 2024), matching the packet identifier.

Inconsistencies inside the paper: the abstract states a 43% run-time improvement of GPose over GDRNPP, while the body (p. 2) gives 42.6%; Table 3 times (2.67s vs 6.26s) are the basis. The abstract and conclusions say GenFlow "reached" CosyPose accuracy, but the tables give 67.4 ARC (GenFlow-MultiHypo16, Table 4) versus 69.8 ARC (CosyPose-ECCV20-SYNT+REAL-ICP, Table 3); the body (p. 7) uses the weaker word "comparable". SAM6D-CNOSmask receives the Task 4 award for the best fast method (less than 1s per image) on p. 8, yet Table 4 and the text list it at 3.87s per image. Task 6 accuracy is written "41.2 mAP" while Task 5 uses "mAPC". GPose2023 is cited as [61,67] in the text but [39,61] in Table 3. The MegaPose example-image panel is captioned "Table 2" although it is a figure.

Figure 1 (accuracy vs run time, 2017–2023) and Figure 3 (qualitative GPose vs GenFlow with depth error maps) were only described. Tables 1, 3 and 4 were extracted column-wise with some cells merged (e.g. T-LESS row of Table 1); only headline rows were claimed.

## Suggested new concepts

- BOP benchmark — the standard evaluation suite and metrics (ARC, APC) for model-based 6D pose estimation.
- Unseen-object pose estimation — model-based pose estimation of novel objects after short onboarding, a distinct task family.
- Object onboarding — time- and resource-bounded stage for learning new objects from CAD models.
- Physically-based rendered training data — synthetic PBR images that narrowed the sim-to-real gap for pose methods.
- Render-and-compare pose refinement — the refinement strategy shared by MegaPose, GenFlow and related methods.
- Foundation-model segmentation for novel objects — SAM/DINOv2-based pipelines like CNOS for zero-shot detection.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Benchmark, métricas VSD/MSSD/MSPD y formato de datos
