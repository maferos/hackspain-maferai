---
aliases: []
type: "source"
title: "ClearGrasp: 3D Shape Estimation of Transparent Objects for Manipulation"
citekey: "Sajjan2019cleargrasp"
doi: "10.48550/arXiv.1910.02550"
arxiv: "1910.02550"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1910.02550"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Shreeyak S. Sajjan", "Matthew Moore", "Mike Pan", "Ganesh Nagaraja", "Johnny Lee", "Andy Zeng", "Shuran Song"]
sha256: ["283d1d9c4403fe0786b9f338b047c4f0ae14d707d4ad6d31c93c30cb77951b9b"]
pdf: "Content/Papers/Sajjan2019cleargrasp.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Sajjan2019cleargrasp.pdf]]

> [!abstract] One-sentence summary
> ClearGrasp masks unreliable sensor depth on transparent objects and re-completes it from RGB-predicted surface normals and occlusion/contact edges, trained on synthetic renders, raising real robot grasp success on transparent objects.

## Abstract

Transparent objects are a common part of everyday life, yet they possess unique visual properties that make them incredibly difficult for standard 3D sensors to produce accurate depth estimates for. In many cases, they often appear as noisy or distorted approximations of the surfaces that lie behind them. To address these challenges, we present ClearGrasp -- a deep learning approach for estimating accurate 3D geometry of transparent objects from a single RGB-D image for robotic manipulation. Given a single RGB-D image of transparent objects, ClearGrasp uses deep convolutional networks to infer surface normals, masks of transparent surfaces, and occlusion boundaries. It then uses these outputs to refine the initial depth estimates for all transparent surfaces in the scene. To train and test ClearGrasp, we construct a large-scale synthetic dataset of over 50,000 RGB-D images, as well as a real-world test benchmark with 286 RGB-D images of transparent objects and their ground truth geometries. The experiments demonstrate that ClearGrasp is substantially better than monocular depth estimation baselines and is capable of generalizing to real-world images and novel objects. We also demonstrate that ClearGrasp can be applied out-of-the-box to improve grasping algorithms' performance on transparent objects. Code, data, and benchmarks will be released. Supplementary materials available on the project website: https://sites.google.com/view/cleargrasp (arXiv)

## 🧠 Key ideas (atomic)

- Transparent materials, being both refractive and specular, do not adhere to the geometric light path assumptions made in classic stereo vision algorithms. (Sajjan et al., 2019) `ev:asserted` p. 1 ^sajjan2019cleargrasp-001
- Many robotic manipulation algorithms that use 3D data such as RGB-D images or point clouds cannot be immediately applied to transparent objects. (Sajjan et al., 2019) `ev:cited` p. 1 ^sajjan2019cleargrasp-002
- Rather than estimating all geometry from scratch, ClearGrasp corrects the initial depth estimates produced by commodity RGB-D cameras. (Sajjan et al., 2019) `ev:asserted` p. 1 ^sajjan2019cleargrasp-003
- The authors conjecture that [[Transparent object depth completion|correcting initial RGB-D depth]] is more practical, letting depth from non-transparent surfaces inform the depth of transparent surfaces. (Sajjan et al., 2019) `ev:asserted` p. 1 ^sajjan2019cleargrasp-004
- The authors state that refractive and specular patterns on transparent objects provide stronger visual cues for their curvature than for their absolute depth. (Sajjan et al., 2019) `ev:asserted` p. 1 ^sajjan2019cleargrasp-005
- The authors report finding that inferring surface normals from RGB data is substantially more reliable than directly inferring depth values. (Sajjan et al., 2019) `ev:asserted` p. 1 ^sajjan2019cleargrasp-006
- Mixing synthetic training data with real-world out-of-domain images without transparent objects let the model generalize better to real images and novel objects. (Sajjan et al., 2019) `ev:measured` p. 2 ^sajjan2019cleargrasp-007
- The authors construct a large-scale synthetic dataset of over 50,000 RGB-D images for training and testing transparent object geometry estimation. (Sajjan et al., 2019) `ev:reported` p. 2 ^sajjan2019cleargrasp-008
- The real-world test benchmark contains 286 RGB-D images of transparent objects together with their ground truth geometries. (Sajjan et al., 2019) `ev:reported` p. 2 ^sajjan2019cleargrasp-009
- The authors state that prior depth inference and [[Transparent object depth completion|depth completion works]] do not explicitly handle transparent objects, whose 3D ground truth is hard to obtain. (Sajjan et al., 2019) `ev:asserted` p. 2 ^sajjan2019cleargrasp-010
- Prior transparent-geometry methods often assume a specific capturing procedure, a known background pattern, a sensor type, or a known object 3D model. (Sajjan et al., 2019) `ev:cited` p. 2 ^sajjan2019cleargrasp-011
- ClearGrasp does not require prior knowledge of the objects' 3D models or of the camera position, unlike model-fitting approaches such as Lysenkov et al. (Sajjan et al., 2019) `ev:asserted` p. 2 ^sajjan2019cleargrasp-012
- In the authors' trials, very high quality rendering and 3D models were required to synthesize representative imagery of transparent objects. (Sajjan et al., 2019) `ev:asserted` p. 2 ^sajjan2019cleargrasp-013
- Type I depth errors on transparent objects are missing depth values, commonly caused by specular highlights on the object surface. (Sajjan et al., 2019) `ev:asserted` p. 3 ^sajjan2019cleargrasp-014
- Type II errors cause the sensor to report the depth of surfaces behind the object instead of the depth of the object itself. (Sajjan et al., 2019) `ev:asserted` p. 3 ^sajjan2019cleargrasp-015
- Inaccurate non-zero depth estimates are difficult to detect using standard depth completion, which would only propagate them into corrupted reconstructions. (Sajjan et al., 2019) `ev:asserted` p. 3 ^sajjan2019cleargrasp-016
- ClearGrasp adopts the [[Transparent object depth completion|depth completion pipeline]] of Zhang and Funkhouser, adding a network that predicts pixel-wise masks of transparent surfaces. (Sajjan et al., 2019) `ev:reported` p. 3 ^sajjan2019cleargrasp-017
- The predicted transparent-surface mask is used to remove all depth pixels corresponding to transparent surfaces from the input depth image. (Sajjan et al., 2019) `ev:reported` p. 3 ^sajjan2019cleargrasp-018
- The transparent segmentation, surface normal and boundary detection networks all use Deeplabv3+ with a DRN-D-54 backbone. (Sajjan et al., 2019) `ev:reported` p. 3 ^sajjan2019cleargrasp-019
- The surface normal network output is L2 normalized to ensure that the estimated surface normals are unit vectors. (Sajjan et al., 2019) `ev:reported` p. 3 ^sajjan2019cleargrasp-020
- The boundary detection network labels each pixel as non-edge, occlusion boundary, or contact edge between two objects. (Sajjan et al., 2019) `ev:reported` p. 3 ^sajjan2019cleargrasp-021
- Contact edges, though not used directly by the optimization, help the network distinguish between different types of edges in color images. (Sajjan et al., 2019) `ev:asserted` p. 3 ^sajjan2019cleargrasp-022
- Boundary training uses a weighted cross-entropy loss in which boundary pixels weigh 5x more than background pixels. (Sajjan et al., 2019) `ev:reported` p. 3 ^sajjan2019cleargrasp-023
- The global optimization minimizes a weighted sum of squared errors over depth, neighbour smoothness and surface normal consistency terms. (Sajjan et al., 2019) `ev:reported` p. 3 ^sajjan2019cleargrasp-024
- In the experiments, the optimization weights were set to λD = 1000, λS = 0.001 and λN = 1.0. (Sajjan et al., 2019) `ev:reported` p. 3 ^sajjan2019cleargrasp-025
- The synthetic dataset uses 9 CAD models of real-world transparent plastic objects, with 4 held out from training to test generalization. (Sajjan et al., 2019) `ev:reported` p. 4 ^sajjan2019cleargrasp-026
- Synthetic scenes used 33 HDRI lighting environments and 65 textures for the ground plane underneath the transparent objects. (Sajjan et al., 2019) `ev:reported` p. 4 ^sajjan2019cleargrasp-027
- Each synthetic scene drops between 1 and 5 CAD objects above a plane so that they come to rest according to physics. (Sajjan et al., 2019) `ev:reported` p. 4 ^sajjan2019cleargrasp-028
- The final synthetic training set contains over 13,000 images of 3 objects each and 5000 images each of another 2 objects. (Sajjan et al., 2019) `ev:reported` p. 4 ^sajjan2019cleargrasp-029
- For real-world ground truth, one set of objects was spray painted with a rough stone texture, which gives much better depth than flat color. (Sajjan et al., 2019) `ev:reported` p. 4 ^sajjan2019cleargrasp-030
- A GUI overlaying camera frames let each transparent object be replaced by an identical spray-painted instance at the same position. (Sajjan et al., 2019) `ev:reported` p. 4 ^sajjan2019cleargrasp-031
- The real-world validation set consists of 173 images of 5 known objects that were also used in the synthetic training data. (Sajjan et al., 2019) `ev:reported` p. 4 ^sajjan2019cleargrasp-032
- The real-world test set consists of 113 images of 5 novel objects, including 3 new glass objects absent from the synthetic dataset. (Sajjan et al., 2019) `ev:reported` p. 4 ^sajjan2019cleargrasp-033
- Depth is evaluated at 144x256p resolution with RMSE, median relative error, and δ thresholds of 1.05, 1.10 and 1.25. (Sajjan et al., 2019) `ev:reported` p. 5 ^sajjan2019cleargrasp-034
- Despite never being trained on real transparent objects, the models achieved very similar RMSE and Rel scores on known objects across domains. (Sajjan et al., 2019) `ev:measured` p. 5 ^sajjan2019cleargrasp-035
- The authors observe large surface normal errors when transparent objects occlude novel opaque objects in real-world images. (Sajjan et al., 2019) `ev:measured` p. 5 ^sajjan2019cleargrasp-036
- The authors attribute better Real-novel than Syn-novel results to three glass objects whose thicker material shows more evident refraction characteristics. (Sajjan et al., 2019) `ev:asserted` p. 5 ^sajjan2019cleargrasp-037
- The authors report that ClearGrasp generalizes to novel object shapes, achieving better depth results than on known objects in both domains. (Sajjan et al., 2019) `ev:measured` p. 5 ^sajjan2019cleargrasp-038
- The better results on novel objects are likely due to their smaller size, which causes relatively smaller depth reconstruction errors. (Sajjan et al., 2019) `ev:asserted` p. 5 ^sajjan2019cleargrasp-039
- The authors state that a mask true positive rate above 95% is critical for removing all the incorrect initial depth values. (Sajjan et al., 2019) `ev:asserted` p. 5 ^sajjan2019cleargrasp-040
- On real-world known objects, ClearGrasp reached a depth RMSE of 0.039 with 97.25 percent of pixels within δ1.25. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-041
- On real-world novel objects, ClearGrasp reached a depth RMSE of 0.028 with 79.18 percent of pixels within δ1.05. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-042
- Mean surface normal error rose from 15.64 degrees on synthetic known objects to 21.93 degrees on real known objects. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-043
- Transparent mask IoU dropped from 0.93 on synthetic known objects to 0.63 on real known objects, while true positive rate stayed near 96. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-044
- The monocular baseline DenseDepth, trained on the same data, had a depth RMSE of 0.270 against 0.038 for full ClearGrasp. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-045
- Removing the transparent mask raised depth RMSE from 0.038 to 0.054, matching the DeepCompletion baseline error. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-046
- Removing contact edges gave the largest ablation error, with depth RMSE rising to 0.061 from 0.038 for the full model. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-047
- Removing boundary edge weights raised depth RMSE to 0.049, compared with 0.038 for the full ClearGrasp model. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-048
- A normal model trained on out-of-domain real-world data without synthetic data was not able to pick up transparent objects, with mean error 43.92. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-049
- Pre-training on MP+SN before synthetic training lowered median normal error from 24.74 to 18.72 degrees. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-050
- Each grasping algorithm was trained with 500 trial and error attempts, then tested with 50 attempts. (Sajjan et al., 2019) `ev:reported` p. 6 ^sajjan2019cleargrasp-051
- ClearGrasp improved suction grasping success on piles of transparent objects from 64% to 86% on a real robot. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-052
- ClearGrasp improved parallel-jaw grasping success on piles of transparent objects from 12% to 72% on a real robot. (Sajjan et al., 2019) `ev:measured` p. 6 ^sajjan2019cleargrasp-053
- The authors suggest future work may explicitly leverage lighting information during inference to improve accuracy under different lighting conditions. (Sajjan et al., 2019) `ev:asserted` p. 6 ^sajjan2019cleargrasp-054
- The authors state that the biggest limitation is that a region fully enclosed by an occlusion boundary has indeterminate depth. (Sajjan et al., 2019) `ev:asserted` p. 10 ^sajjan2019cleargrasp-055
- Cluttered scenes where transparent objects occlude each other make surface normal and occlusion boundary prediction challenging, leading to output depth errors. (Sajjan et al., 2019) `ev:measured` p. 10 ^sajjan2019cleargrasp-056
- Under bright directional lighting, caustics cause the model to mistakenly identify shadows of transparent objects as transparent objects. (Sajjan et al., 2019) `ev:measured` p. 10 ^sajjan2019cleargrasp-057
- The synthetic dataset does not contain accurate caustics due to limitations of the Cycles rendering engine, according to the authors. (Sajjan et al., 2019) `ev:asserted` p. 10 ^sajjan2019cleargrasp-058
- The authors report that data augmentation significantly improved results on patterned backgrounds, bright caustics, directional lights, and varying backgrounds. (Sajjan et al., 2019) `ev:measured` p. 11 ^sajjan2019cleargrasp-059
- A Deeplabv3+ DRN-54 at 256 input gave a mean normal error of 22.5, against 34.9 for Resnet101 at 512. (Sajjan et al., 2019) `ev:measured` p. 11 ^sajjan2019cleargrasp-060
- The results indicate that a smaller input image size, which effectively increases receptive field width, performs better for normal estimation. (Sajjan et al., 2019) `ev:measured` p. 11 ^sajjan2019cleargrasp-061

## 🎯 Contributions

## 📖 Glossary

- **Type I error** — missing depth on a transparent surface, commonly caused by specular highlights.
- **Type II error** — sensor returns the depth of the background behind a transparent object.
- **Occlusion boundary** — pixel edge where depth is discontinuous between surfaces.
- **Contact edge** — boundary where one object touches another surface, without depth discontinuity.
- **Depth completion** — filling missing or removed depth pixels from RGB-derived cues and remaining depth.
- **Global optimization (depth)** — solving for depth that fits observed depth, smoothness and predicted normals.
- **DRN** — Dilated Residual Network, a backbone with enlarged receptive field.
- **HDRI** — high dynamic range image used as an environment light source in rendering.
- **Caustics** — bright light patterns formed by refraction or reflection through transparent material.
- **δ threshold** — share of pixels whose predicted/true depth ratio lies within a bound.

## ❓ Open questions

- How can depth be recovered for regions fully enclosed by an occlusion boundary, where normals alone leave depth indeterminate?
- Would rendering with accurate caustics remove the shadow-as-object failure mode, or is augmentation enough?
- How does the approach scale to dense clutter with mutually occluding transparent objects?
- Does explicit lighting information at inference improve robustness across lighting conditions?
- How well does the method transfer to liquid-filled or tinted transparent containers, which the benchmark does not include?

## 📝 Notes on reading

Read the arXiv v2 preprint (14 Oct 2019), matching the packet identifier.

Figures 1, 2, 4, 5, 6, 7, 10, 11 and 12 are qualitative (pipeline overview, rendered samples, benchmark capture, failure cases, ablation and baseline comparisons) and were only described, not claimed.

Inconsistencies inside the paper: the full model row of Table II (RMSE 0.038, REL 0.048, MAE 0.027) differs slightly from the Real-known row of Table I (0.039, 0.053, 0.029) although both appear to be on the real-known set. The text says novel objects give better results than known objects in both domains, but on synthetic data the novel REL (0.071) and δ1.05 (42.95) are worse than known (0.047, 71.23); only RMSE is better. Table III's MP+SN+Syn row equals the Table I Real-known normal row, suggesting Table III is on real-known. Table III's Syn-only row lists median 24.74 above mean 21.59 and repeats 24.74 in the 11.25 column, likely a typo. The Method overview points to Sec. III-B for the robotic application, which is actually Sec. III-D. The MAE column in Tables I and II is not defined in the metrics paragraph. Table I shows the mask TP as a percentage-like number (96.30) without a unit.

## Suggested new concepts

- Transparent object depth estimation — a recurring perception gap for RGB-D sensing that several manipulation papers address.
- Depth completion via surface normals and occlusion boundaries — the Zhang and Funkhouser optimization reused here deserves its own note.
- Synthetic-to-real transfer with out-of-domain real data mixing — a training strategy this paper measures directly.
- Contact edges vs occlusion boundaries — a boundary taxonomy that measurably affects depth completion.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Completado de profundidad para objetos transparentes
