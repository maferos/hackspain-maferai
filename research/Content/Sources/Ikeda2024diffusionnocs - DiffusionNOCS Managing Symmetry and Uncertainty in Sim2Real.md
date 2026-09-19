---
aliases: []
type: "source"
title: "DiffusionNOCS: Managing Symmetry and Uncertainty in Sim2Real Multi-Modal Category-level Pose Estimation"
citekey: "Ikeda2024diffusionnocs"
doi: "10.48550/arXiv.2402.12647"
arxiv: "2402.12647"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2402.12647"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Takuya Ikeda", "Sergey Zakharov", "Tianyi Ko", "Muhammad Zubair Irshad", "Robert Lee", "Katherine Liu", "Rares Ambrus", "Koichi Nishiwaki"]
sha256: ["333062dde6772dcb6a680a4ff7871655398e438e1dfcd9d68bba826447d3dce2"]
pdf: "Content/Papers/Ikeda2024diffusionnocs.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Ikeda2024diffusionnocs.pdf]]

> [!abstract] One-sentence summary
> DiffusionNOCS predicts NOCS maps with a conditional diffusion model over selectable normal, RGB and DINOv2 inputs, handling symmetric objects through multiple noise samples and, trained only on synthetic renders, leading synthetic-data baselines on NOCS Real 275 and all baselines on average on a new zero-shot benchmark.

## Abstract

This paper addresses the challenging problem of category-level pose estimation. Current state-of-the-art methods for this task face challenges when dealing with symmetric objects and when attempting to generalize to new environments solely through synthetic data training. In this work, we address these challenges by proposing a probabilistic model that relies on diffusion to estimate dense canonical maps crucial for recovering partial object shapes as well as establishing correspondences essential for pose estimation. Furthermore, we introduce critical components to enhance performance by leveraging the strength of the diffusion models with multi-modal input representations. We demonstrate the effectiveness of our method by testing it on a range of real datasets. Despite being trained solely on our generated synthetic data, our approach achieves state-of-the-art performance and unprecedented generalization qualities, outperforming baselines, even those specifically trained on the target domain. (arXiv)

## 🧠 Key ideas (atomic)

- Most current methods regress a single pose from partial input and therefore must craft symmetry handling such as extensive labeling and heuristic operations. (Ikeda et al., 2024) `ev:asserted` p. 1 ^ikeda2024diffusionnocs-001
- The authors posit that a probabilistic pose method with multi-modal inputs can significantly improve performance when ambiguities are present at deployment. (Ikeda et al., 2024) `ev:asserted` p. 1 ^ikeda2024diffusionnocs-002
- The authors note a lack of existing benchmarks suitable for evaluating [[Category-level object pose estimation|zero-shot category-level pose estimation]] in novel real-world settings. (Ikeda et al., 2024) `ev:asserted` p. 1 ^ikeda2024diffusionnocs-003
- According to the authors, current state-of-the-art instance and [[Category-level object pose estimation|category-level object pose estimation methods]] are almost exclusively correspondence-based approaches. (Ikeda et al., 2024) `ev:cited` p. 2 ^ikeda2024diffusionnocs-004
- Wang et al. designed [[Symmetry-aware pose loss|loss functions for specific symmetry types]], which the authors attribute to the deterministic nature of their training. (Ikeda et al., 2024) `ev:cited` p. 2 ^ikeda2024diffusionnocs-005
- Zhang et al. used a generative diffusion approach to estimate poses from partial point clouds, naturally handling all symmetry types. (Ikeda et al., 2024) `ev:cited` p. 2 ^ikeda2024diffusionnocs-006
- Instead of point clouds, DiffusionNOCS estimates [[Normalized Object Coordinate Space|dense canonical maps]] from multi-modal image inputs that recover both pose and partial geometry. (Ikeda et al., 2024) `ev:asserted` p. 2 ^ikeda2024diffusionnocs-007
- At inference the method assumes a given depth image, 2D bounding box and category ID, and can accommodate additional inputs such as RGB. (Ikeda et al., 2024) `ev:reported` p. 2 ^ikeda2024diffusionnocs-008
- The model is trained only on synthetic data rendered from openly available 3D models, yielding RGB images, depth images and category IDs. (Ikeda et al., 2024) `ev:reported` p. 2 ^ikeda2024diffusionnocs-009
- DiffusionNOCS uses a DDPM to estimate [[Normalized Object Coordinate Space|NOCS maps]], which enables multiple possible maps to be predicted from multiple noise samples. (Ikeda et al., 2024) `ev:reported` p. 2 ^ikeda2024diffusionnocs-010
- The denoising process is conditioned on images and category IDs and trained with a pixelwise MSE loss on the predicted noise. (Ikeda et al., 2024) `ev:reported` p. 3 ^ikeda2024diffusionnocs-011
- The noise estimator is a 2D U-Net with ResNet blocks, with conditioning images concatenated to the noise before the U-Net. (Ikeda et al., 2024) `ev:reported` p. 3 ^ikeda2024diffusionnocs-012
- Training uses a discrete DDPM denoising scheduler with 1000 iterations as the noise scheduler for the model. (Ikeda et al., 2024) `ev:reported` p. 3 ^ikeda2024diffusionnocs-013
- At inference a DPM-solver reduces the denoising iterations from 1000 to 10, improving time efficiency for real-world robotics applications. (Ikeda et al., 2024) `ev:reported` p. 3 ^ikeda2024diffusionnocs-014
- The network is conditioned on four types of information: surface normals, RGB images, DINOv2 semantic features, and category IDs. (Ikeda et al., 2024) `ev:reported` p. 3 ^ikeda2024diffusionnocs-015
- Surface normals computed from input depth serve as scale and translation invariant conditioning, decoupling these parameters from the NOCS estimator. (Ikeda et al., 2024) `ev:reported` p. 3 ^ikeda2024diffusionnocs-016
- The authors argue unprocessed depth entangles scale, translation and camera intrinsics, requiring large amounts of data to avoid overfitting. (Ikeda et al., 2024) `ev:asserted` p. 3 ^ikeda2024diffusionnocs-017
- RGB is added as conditioning because geometry alone can be ambiguous for reflective objects or semantically rich but geometrically simple objects. (Ikeda et al., 2024) `ev:asserted` p. 3 ^ikeda2024diffusionnocs-018
- ViT-S DINOv2 features of dimension 384 are reduced with PCA, following Goodwin et al., because high dimensions slow inference and training. (Ikeda et al., 2024) `ev:reported` p. 4 ^ikeda2024diffusionnocs-019
- During training each condition is dropped at a certain rate and replaced by a zero-filled tensor of the same dimension. (Ikeda et al., 2024) `ev:reported` p. 4 ^ikeda2024diffusionnocs-020
- Condition dropout lets a single network take whichever inputs are available at inference time without re-training. (Ikeda et al., 2024) `ev:reported` p. 4 ^ikeda2024diffusionnocs-021
- With all conditions dropped, the model performs unconditional diffusion and can still recover plausible NOCS maps from noise alone. (Ikeda et al., 2024) `ev:measured` p. 4 ^ikeda2024diffusionnocs-022
- Conditioning on surface normals reconstructs a hollow bottle, whereas RGB information alone recovers a filled bottle in the Figure 4 example. (Ikeda et al., 2024) `ev:measured` p. 4 ^ikeda2024diffusionnocs-023
- Training images are rendered on white background from 162 camera poses created by icosahedron sampling with 2 subdivision levels. (Ikeda et al., 2024) `ev:reported` p. 4 ^ikeda2024diffusionnocs-024
- Lighting augmentation based on the Phong reflection model is applied with the normal maps at training time. (Ikeda et al., 2024) `ev:reported` p. 4 ^ikeda2024diffusionnocs-025
- Cutout with random rectangle, circle, triangle and ellipse shapes is applied to improve robustness against occlusion. (Ikeda et al., 2024) `ev:reported` p. 4 ^ikeda2024diffusionnocs-026
- 6D pose and scale are estimated by registering masked depth points to [[Normalized Object Coordinate Space|NOCS map points]] with TEASER++. (Ikeda et al., 2024) `ev:reported` p. 5 ^ikeda2024diffusionnocs-027
- The inlier rate from the TEASER++ rotation estimate is treated as the confidence value of each estimated pose. (Ikeda et al., 2024) `ev:reported` p. 5 ^ikeda2024diffusionnocs-028
- Multiple noises are input as a batch at inference, and the pose with the highest confidence is selected as the final result. (Ikeda et al., 2024) `ev:reported` p. 5 ^ikeda2024diffusionnocs-029
- The authors suggest multiple high-confidence poses could let grasping or placing select poses under collision or kinematics constraints. (Ikeda et al., 2024) `ev:asserted` p. 5 ^ikeda2024diffusionnocs-030
- Evaluation uses two benchmarks comprising four real-world datasets: NOCS Real 275, TYO-L, YCB-V and HOPE. (Ikeda et al., 2024) `ev:reported` p. 5 ^ikeda2024diffusionnocs-031
- The NOCS Real benchmark contains objects of 6 categories placed in 6 environments, spanning a total of 2.75K test images. (Ikeda et al., 2024) `ev:reported` p. 5 ^ikeda2024diffusionnocs-032
- On NOCS Real 275, 2D boxes and category IDs come from precomputed MaskRCNN results for fair comparison with previous works. (Ikeda et al., 2024) `ev:reported` p. 5 ^ikeda2024diffusionnocs-033
- The zero-shot Generalization Benchmark comprises TYO-L, YCB-V and HOPE, three datasets commonly used for instance-level pose estimation. (Ikeda et al., 2024) `ev:reported` p. 5 ^ikeda2024diffusionnocs-034
- In the benchmark, the HOPE dataset contains 10 highly occluded multi-object scenes with a very diverse pose distribution. (Ikeda et al., 2024) `ev:reported` p. 5 ^ikeda2024diffusionnocs-035
- The TYO-L dataset features 21 single-object scenes with five different lighting conditions and four different backgrounds. (Ikeda et al., 2024) `ev:reported` p. 5 ^ikeda2024diffusionnocs-036
- Ground-truth masks are used for all baselines and the proposed method during inference on the generalization benchmark. (Ikeda et al., 2024) `ev:reported` p. 5 ^ikeda2024diffusionnocs-037
- Training renders 20 ShapeNet models per target category, giving 162 images per instance at 160 x 160 pixels. (Ikeda et al., 2024) `ev:reported` p. 6 ^ikeda2024diffusionnocs-038
- For the can category, the generalization metric is made invariant to the symmetry axis direction, since objects appear in arbitrary poses. (Ikeda et al., 2024) `ev:reported` p. 6 ^ikeda2024diffusionnocs-039
- Input representations are randomly dropped at a 25% rate during training, with DDPM time steps set to 1000. (Ikeda et al., 2024) `ev:reported` p. 6 ^ikeda2024diffusionnocs-040
- At inference, 6 different noises generate 6 possible NOCS maps, and the pose with the highest confidence is selected. (Ikeda et al., 2024) `ev:reported` p. 6 ^ikeda2024diffusionnocs-041
- Using 10 DPM-solver time steps, the default configuration takes 0.855s on a Tesla V100 GPU. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-042
- Trained only on synthetic data, the RGB-DINO-N variant scores 35.0, 66.6 and 77.1 mAP at 5°5cm, 10°5cm and 15°5cm on NOCS Real 275. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-043
- The former best synthetic-only methods on NOCS Real 275 score 16.9 at 5°5cm, 44.9 at 10°5cm and 52.8 at 15°5cm. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-044
- Despite synthetic-only training, the method outperforms NOCS, ShapePrior and CenterSnap trained on real and synthetic data on NOCS Real 275. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-045
- GenPose, trained on synthetic and real data, scores higher on NOCS Real 275 with 50.6, 84.0 and 89.7 mAP. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-046
- Combining surface normals and DINO features improves over normals alone by over 10 percent on the 10°5cm and 15°5cm metrics. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-047
- On NOCS Real 275, DINOv2 features are more effective than RGB as an additional conditioning modality alongside surface normals. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-048
- On the generalization benchmark, the synthetic-data ShapePrior baseline scores average mAPs of 14.4, 31.2 and 38.4. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-049
- The authors report average generalization mAPs of 29.2 (5°5cm), 51.7 (10°5cm) and 57.1 (15°5cm) with synthetic training only. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-050
- Averaged over TYO-L, YCB-V and HOPE, the method outperforms all baseline methods trained on real data. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-051
- Real-data methods dominate YCB-V scores, which the authors explain by its similarity with NOCS: upright objects in well-lit scenes near the camera. (Ikeda et al., 2024) `ev:asserted` p. 6 ^ikeda2024diffusionnocs-052
- For a bowl, 20 rotations estimated from 20 noise images are widely distributed around one axis, reflecting axial symmetry. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-053
- For a mug with a visible handle, the estimated rotations show well defined peaks, indicating the handle resolves pose ambiguity. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-054
- For a mug with an invisible handle, the rotation distribution correlates with possible poses, identifying a possible handle direction. (Ikeda et al., 2024) `ev:measured` p. 6 ^ikeda2024diffusionnocs-055
- In the generalization benchmark, DualPoseNet reaches 87.5 mAP at 15°5cm on YCB-V while scoring 14.1 on HOPE. (Ikeda et al., 2024) `ev:measured` p. 7 ^ikeda2024diffusionnocs-056
- On TYO-L, the DINO-N variant reaches 43.5, 60.2 and 66.0 mAP, against 22.5, 28.8 and 32.2 for DualPoseNet. (Ikeda et al., 2024) `ev:measured` p. 7 ^ikeda2024diffusionnocs-057
- With depth partially missing on a black laptop, RGB-D DiffusionNOCS can still estimate the NOCS map and reconstruct the lacking point cloud. (Ikeda et al., 2024) `ev:measured` p. 7 ^ikeda2024diffusionnocs-058
- With one noise sample, performance peaks at 6 PCA dimensions, scoring 30.0, 54.1 and 63.4 mAP on NOCS Real 275. (Ikeda et al., 2024) `ev:measured` p. 7 ^ikeda2024diffusionnocs-059
- Raising noise samples from 1 to 6 with 6-dimensional PCA gives more than a 10 percent improvement on 10°5cm and 15°5cm. (Ikeda et al., 2024) `ev:measured` p. 7 ^ikeda2024diffusionnocs-060
- Inference time rises from 0.386 s with one noise sample to 0.855 s with six and 1.147 s with nine. (Ikeda et al., 2024) `ev:measured` p. 7 ^ikeda2024diffusionnocs-061
- The authors conclude the probabilistic approach handles symmetric objects without special data annotations and heuristics at training time. (Ikeda et al., 2024) `ev:asserted` p. 7 ^ikeda2024diffusionnocs-062
- The authors conclude that dense correspondences from multi-modal inputs faithfully recover partial object geometry even in the presence of lacking depth. (Ikeda et al., 2024) `ev:asserted` p. 8 ^ikeda2024diffusionnocs-063

## 🎯 Contributions

## 📖 Glossary

- **NOCS** — Normalized Object Coordinate Space; per-pixel canonical 3D coordinates of an object in [0,1].
- **Category-level pose estimation** — estimating 6D pose and size of unseen instances within known object categories.
- **DDPM** — Denoising Diffusion Probabilistic Model; generates samples by iteratively denoising Gaussian noise.
- **DPM-solver** — fast ODE solver that samples diffusion models in about 10 steps.
- **DINOv2** — self-supervised vision transformer foundation model producing dense semantic features.
- **TEASER++** — fast, certifiable point cloud registration algorithm robust to outlier correspondences.
- **5°5cm mAP** — mean average precision of poses within 5 degrees rotation and 5 cm translation error.
- **Condition dropout** — randomly zeroing conditioning inputs during training so any subset works at inference.

## ❓ Open questions

- How does the method perform with predicted rather than ground-truth masks on the generalization benchmark?
- Can the 0.855s inference time with 6 noise samples be reduced enough for closed-loop robotic manipulation?
- Does the approach scale beyond the six NOCS categories and 20 ShapeNet models per category?
- Is the TEASER++ inlier rate a calibrated confidence, and how well does it rank correct over incorrect hypotheses?
- Why does adding RGB to DINO-N not help, and slightly hurt, on the generalization benchmark at 10°5cm and 15°5cm?

## 📝 Notes on reading

Version read: arXiv 2402.12647v2 (5 Mar 2024), a preprint submitted to the IEEE.

Inconsistencies inside the paper:
- NOCS Real 275: the text (p. 6) reports 66.7 at 10°5cm for the full method, but Table I gives 66.6 for RGB-DINO-N; 66.7 is the DINO-N row. Table III (p. 7) also gives 66.6. The claim uses the table value.
- Generalization benchmark: the text (p. 6) reports averages of 29.2 / 51.7 / 57.1, which mixes rows of Table II (p. 7): 29.2 is RGB-DINO-N at 5°5cm, while 51.7 and 57.1 are DINO-N; RGB-DINO-N scores 50.4 and 55.9 at 10°5cm and 15°5cm.
- DINOv2 PCA: p. 4 gives the original feature dimension as 384, while the implementation details (p. 6) say PCA reduces it from 382 to 6.
- The text says the best prior synthetic methods score 16.9 / 44.9 / 52.8; these come from two methods (CPPF for the first two, ShapePrior S for the third).
- Section IV-B generalization text says the method outperforms all real-data methods on average; Table II shows GenPose (S+R) at 29.0 at 5°5cm against 29.2 for RGB-DINO-N, a narrow margin.

Figures described only: Fig. 1 (overview of multiple pose hypotheses for mugs), Fig. 3 (PCA-colored DINOv2 features), Fig. 5 (camera poses and synthetic renders), Fig. 7 (qualitative poses on four datasets), Fig. 8 (20 poses on a unit sphere), Fig. 9 (point cloud completion of a black laptop). Equation 3 (the can symmetry-axis error) is garbled in extraction.

## Suggested new concepts

- Normalized Object Coordinate Space (NOCS) — the dense canonical-map representation underlying many category-level pose methods.
- Diffusion models for pose estimation — generative handling of multi-modal pose distributions from symmetry, shared with GenPose.
- Condition dropout for selectable modalities — a training trick letting one network use any subset of sensor inputs.
- Zero-shot sim-to-real category-level pose — training only on synthetic renders and evaluating on unseen real datasets.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H7.** Demuestra pose por categoría entrenada solo con datos sintéticos que generaliza a datos reales, lo que respalda el pipeline sim-to-real con AutoBio.
