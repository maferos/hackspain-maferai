---
aliases: []
type: "source"
title: "ViT-VS: On the Applicability of Pretrained Vision Transformer Features for Generalizable Visual Servoing"
citekey: "Scherl2025vit"
doi: "10.48550/arXiv.2503.04545"
arxiv: "2503.04545"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2503.04545"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Alessandro Scherl", "Stefan Thalhammer", "Bernhard Neuberger", "Wilfried Wöber", "José García-Rodríguez"]
sha256: ["71d4e2ccc81845fd0988d9e61f0fdbd742a6064810c969b24d49ea22638c9fbf"]
pdf: "Content/Papers/Scherl2025vit.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 55
---

📄 PDF: [[Scherl2025vit.pdf]]

> [!abstract] One-sentence summary
> ViT-VS feeds DINOv2 patch correspondences into a classical IBVS controller, reaching learning-based convergence rates without any task-specific training and grasping unseen objects from a same-category reference.

## Abstract

Visual servoing enables robots to precisely position their end-effector relative to a target object. While classical methods rely on hand-crafted features and thus are universally applicable without task-specific training, they often struggle with occlusions and environmental variations, whereas learning-based approaches improve robustness but typically require extensive training. We present a visual servoing approach that leverages pretrained vision transformers for semantic feature extraction, combining the advantages of both paradigms while also being able to generalize beyond the provided sample. Our approach achieves full convergence in unperturbed scenarios and surpasses classical image-based visual servoing by up to 31.2\% relative improvement in perturbed scenarios. Even the convergence rates of learning-based methods are matched despite requiring no task- or object-specific training. Real-world evaluations confirm robust performance in end-effector positioning, industrial box manipulation, and grasping of unseen objects using only a reference from the same category. Our code and simulation environment are available at: https://alessandroscherl.github.io/ViT-VS/ (arXiv)

## 🧠 Key ideas (atomic)

- [[Visual servoing|Classical visual servoing methods]] show limited robustness to image perturbations and typically require the exact target object instance, according to the authors. (Scherl et al., 2025) `ev:asserted` p. 1 ^scherl2025vit-001
- [[Visual servoing|Learning-based visual servoing methods]] require task-specific training, extensive data generation or predefined object models, which the authors say hinders real-world deployment. (Scherl et al., 2025) `ev:asserted` p. 1 ^scherl2025vit-002
- The authors hypothesize that pretrained Vision Transformers combine the advantages of classical and learning-based visual servoing through semantically robust features. (Scherl et al., 2025) `ev:asserted` p. 1 ^scherl2025vit-003
- ViT-VS is a visual servoing framework that combines [[Image-based visual servoing|image-based visual servoing]] with DINOv2 features, requiring no task-specific training or fine-tuning. (Scherl et al., 2025) `ev:asserted` p. 1 ^scherl2025vit-004
- The authors state that ViT rotation invariance can cause convergence to incorrect orientations, specifically for in-plane rotations of ±90° and 180°. (Scherl et al., 2025) `ev:asserted` p. 1 ^scherl2025vit-005
- Traditional feature extractors such as SIFT and SURF have been observed to struggle with occlusions, varying illumination and complex environments. (Scherl et al., 2025) `ev:cited` p. 2 ^scherl2025vit-006
- Direct Visual Servoing achieves lower positioning error than classical approaches but suffers from a limited convergence domain, according to prior work. (Scherl et al., 2025) `ev:cited` p. 2 ^scherl2025vit-007
- Pretrained ViTs are described as showing strong zero-shot capabilities and generalization across related object categories in earlier studies. (Scherl et al., 2025) `ev:cited` p. 2 ^scherl2025vit-008
- The pipeline extracts DINOv2 patch embeddings and establishes correspondences between desired and current images using cosine similarity and a cyclical distance metric. (Scherl et al., 2025) `ev:reported` p. 2 ^scherl2025vit-009
- Correspondences are randomly selected from the top-K matches to maintain spatial diversity of features across the image. (Scherl et al., 2025) `ev:reported` p. 2 ^scherl2025vit-010
- Matching adopts the best buddy pairs concept, finding each patch's nearest neighbour in the current image and mapping it back to the desired image. (Scherl et al., 2025) `ev:reported` p. 3 ^scherl2025vit-011
- The authors state that spreading correspondences across the image is crucial for robust convergence by preventing feature concentration in distinctive regions. (Scherl et al., 2025) `ev:asserted` p. 3 ^scherl2025vit-012
- Hierarchical feature binning combines each patch with surrounding rings of neighbours through average pooling, enriching descriptors at extra computational cost. (Scherl et al., 2025) `ev:reported` p. 3 ^scherl2025vit-013
- DINOv2 operates at input resolutions between 224 × 224 and 518 × 518 pixels, so input images must be resized within this range. (Scherl et al., 2025) `ev:reported` p. 3 ^scherl2025vit-014
- When the desired image includes background, Segment Anything is used to create foreground segmentation masks. (Scherl et al., 2025) `ev:reported` p. 3 ^scherl2025vit-015
- Initial rotation compensation evaluates matching at four rotations (0°, 90°, 180°, -90°) and picks the one maximizing mean cosine similarity. (Scherl et al., 2025) `ev:reported` p. 3 ^scherl2025vit-016
- The selected optimal rotation is applied to the robot before the visual servoing loop starts, aligning current and desired image orientations. (Scherl et al., 2025) `ev:reported` p. 4 ^scherl2025vit-017
- The controller follows [[Image-based visual servoing|classical IBVS]], computing camera velocity from the pseudoinverse of an interaction matrix approximated with depth-image values. (Scherl et al., 2025) `ev:reported` p. 4 ^scherl2025vit-018
- An exponential moving average filter is applied to each velocity component to dampen fluctuations introduced by randomized feature selection. (Scherl et al., 2025) `ev:reported` p. 4 ^scherl2025vit-019
- Features come from DINOv2 ViT-Small/14 pretrained on ImageNet1k, using layer 11 tokens with patch size and stride of 14 pixels. (Scherl et al., 2025) `ev:reported` p. 4 ^scherl2025vit-020
- Unless stated otherwise, the method uses a 308 × 308 pixel input with β = 1 binning and 24 feature pairs per iteration. (Scherl et al., 2025) `ev:reported` p. 4 ^scherl2025vit-021
- Real-world experiments use a Universal Robots UR5 mounted on a MiR100 mobile base with an Intel RealSense D435i camera. (Scherl et al., 2025) `ev:reported` p. 4 ^scherl2025vit-022
- The simulation replicates the DMLVS environment, with a virtual 640 × 480 camera and a 60 × 80cm "hollywood poster" target. (Scherl et al., 2025) `ev:reported` p. 4 ^scherl2025vit-023
- Following DMLVS, 500 distinct initial camera poses are generated, sampled within a 1.2m×1.2m×0.3m cuboid around the desired position. (Scherl et al., 2025) `ev:reported` p. 4 ^scherl2025vit-024
- The sampled starting poses yield average initial position errors of 46.42 ± 16.99cm and orientation errors of 74.12 ± 27.71°. (Scherl et al., 2025) `ev:reported` p. 5 ^scherl2025vit-025
- Perturbed runs apply colour jitter, random erasing and Gaussian blur, with parameters taken from the DMLVS codebase. (Scherl et al., 2025) `ev:reported` p. 5 ^scherl2025vit-026
- A run counts as converged when velocities are close to zero and initial position and rotation errors drop by more than 90%. (Scherl et al., 2025) `ev:reported` p. 5 ^scherl2025vit-027
- Classical SIFT, ORB and AKAZE baselines replicate the ViT-VS matching strategy, using 24 top-ranked matches for servoing. (Scherl et al., 2025) `ev:reported` p. 5 ^scherl2025vit-028
- ViT-VS converged in 100% of unperturbed simulation runs, on par with DMLVS but without object- or scene-specific finetuning. (Scherl et al., 2025) `ev:measured` p. 5 ^scherl2025vit-029
- Under image perturbations ViT-VS reached a 76.6% convergence rate, compared with 76.0 for the finetuned DMLVS. (Scherl et al., 2025) `ev:measured` p. 6 ^scherl2025vit-030
- The classical baseline [[Image-based visual servoing|ORB IBVS]] converged in 98.6 percent of unperturbed runs and 58.4 percent of perturbed runs. (Scherl et al., 2025) `ev:measured` p. 6 ^scherl2025vit-031
- Under perturbation, ViT-VS achieved a relative convergence rate improvement of 31.2% over the best [[Image-based visual servoing|classical IBVS method]]. (Scherl et al., 2025) `ev:measured` p. 1 ^scherl2025vit-032
- With perturbations, ViT-VS had a translational end error of 21.54 ± 12.11 versus 19.29 ± 12.81 for DMLVS. (Scherl et al., 2025) `ev:measured` p. 5 ^scherl2025vit-033
- With perturbations, ViT-VS had a rotational end error of 1.83 ± 0.98° compared with 1.92 ± 1.28° for DMLVS. (Scherl et al., 2025) `ev:measured` p. 5 ^scherl2025vit-034
- ViT-VS end errors are higher than those of [[Image-based visual servoing|classical IBVS methods]], which the authors attribute to coarse ViT feature maps. (Scherl et al., 2025) `ev:asserted` p. 5 ^scherl2025vit-035
- With DINOv2-small, feature maps are 1/14 of the input resolution, so correspondences are matched in a 22 × 22 space. (Scherl et al., 2025) `ev:reported` p. 5 ^scherl2025vit-036
- ViT-VS reached a translational APE of 17.14 ± 6.65cm, comparable to 16.60 ± 5.66cm for ORB IBVS. (Scherl et al., 2025) `ev:measured` p. 5 ^scherl2025vit-037
- Among non-finetuned methods, ViT-VS had the best rotational APE of 16.34 ± 5.05° and the best length ratio of 1.21 ± 0.39. (Scherl et al., 2025) `ev:measured` p. 5 ^scherl2025vit-038
- Without rotation compensation, ViT-VS convergence dropped to 83.8% unperturbed and 57.2% perturbed, from 100.0% and 76.6% respectively. (Scherl et al., 2025) `ev:measured` p. 5 ^scherl2025vit-039
- Feature binning had a larger impact on frame rate than the choice of DINOv2 backbone size, averaged over 100 runs. (Scherl et al., 2025) `ev:measured` p. 5 ^scherl2025vit-040
- Evaluating the smoothing parameter α from 0.5 to 0.9, lower values reduced length ratios but increased end-positioning error. (Scherl et al., 2025) `ev:measured` p. 5 ^scherl2025vit-041
- The authors chose α of 0.8 as the standard configuration, balancing length ratio against end error. (Scherl et al., 2025) `ev:reported` p. 5 ^scherl2025vit-042
- A real robot run on the poster converged from an initial error including −153.08° rotation to a final error below 0.5cm per axis. (Scherl et al., 2025) `ev:measured` p. 6 ^scherl2025vit-043
- In the detailed real robot experiment, initial rotation compensation selected 180° as the best starting rotation. (Scherl et al., 2025) `ev:measured` p. 6 ^scherl2025vit-044
- In the industrial use case, the MiR100 base arrives at the work cell with a positioning uncertainty of ±10cm. (Scherl et al., 2025) `ev:reported` p. 6 ^scherl2025vit-045
- ViT-VS achieved a 100% success rate over 20 box lifting trials with boxes of different appearances on the mobile manipulator. (Scherl et al., 2025) `ev:measured` p. 6 ^scherl2025vit-046
- For box manipulation, β = 2 binning with 224 × 224 input was used to focus on geometry rather than texture. (Scherl et al., 2025) `ev:reported` p. 6 ^scherl2025vit-047
- Category-level grasping used two unseen instances each of mug, toy car and shoe, with 5 picking tries per instance. (Scherl et al., 2025) `ev:reported` p. 7 ^scherl2025vit-048
- The grasping motion is predefined for the seen reference instance, while ViT-VS positions the end effector relative to the unseen object. (Scherl et al., 2025) `ev:reported` p. 7 ^scherl2025vit-049
- Category-level grasping achieved success rates of 100% for shoes, 90% for mugs, and 80% for toy cars. (Scherl et al., 2025) `ev:measured` p. 7 ^scherl2025vit-050
- Across the three categories, grasping unseen instances reached a mean success rate of 90% over n = 30 trials. (Scherl et al., 2025) `ev:measured` p. 2 ^scherl2025vit-051
- The failed mug grasp occurred when the mug slipped out of the gripper after successful convergence and grasp. (Scherl et al., 2025) `ev:measured` p. 7 ^scherl2025vit-052
- Both toy car failures were table plane collisions, one of which followed an incorrect rotation from initial rotation compensation. (Scherl et al., 2025) `ev:measured` p. 7 ^scherl2025vit-053
- The authors conclude that pretrained ViT features give convergence rates comparable to learning-based methods while remaining applicable without finetuning. (Scherl et al., 2025) `ev:asserted` p. 8 ^scherl2025vit-054
- Future work will address positioning errors, which the authors say are dictated by the resolution of the ViT feature maps. (Scherl et al., 2025) `ev:asserted` p. 8 ^scherl2025vit-055

## 🎯 Contributions

## 📖 Glossary

- **IBVS** — Image-based visual servoing: control driven directly by image feature errors.
- **PBVS** — Position-based visual servoing: control driven by estimated pose differences.
- **Interaction matrix** — Jacobian relating image feature motion to camera velocity.
- **Best buddy pairs** — Mutual nearest-neighbour matches between two descriptor sets.
- **Cyclical distance** — Distance between a patch and its round-trip match; zero means perfect consistency.
- **Feature binning** — Pooling each patch descriptor with neighbouring patches to add context.
- **Length ratio** — Executed trajectory length divided by the ideal trajectory length.
- **APE** — Absolute Pose Error, cumulated deviation from the optimal PBVS trajectory.
- **DINOv2** — Self-supervised pretrained Vision Transformer family producing general-purpose patch features.

## ❓ Open questions

- Can positioning accuracy be improved beyond the limit set by the 1/14 resolution of ViT feature maps?
- How can frame rate be raised enough for real-time servoing with higher binning or larger backbones?
- Does the four-angle rotation compensation handle intermediate in-plane rotations or rotations outside the image plane?
- How would ViT-VS perform with larger DINOv2 backbones or other foundation-model features?
- Can grasp poses also transfer across instances, instead of being predefined for the seen reference object?

## 📝 Notes on reading

- Version read: arXiv v1 preprint (2503.04545v1, 6 Mar 2025), submitted to IEEE.
- Table I lists end error in [mm], while page 5 text quotes the same values (19.29 ± 12.81, 21.54 ± 12.11) in cm; the unit is inconsistent, so translational end-error claims omit the unit.
- Page 5 text says ViT-VS under perturbation improves over "all ... deep learning-based methods"; Table I shows 76.6 vs DMLVS 76.0, a marginal difference, and the abstract more cautiously says learning-based convergence rates are "matched".
- The introduction (p. 1) calls ViTs rotation invariant, whereas Section III-B (p. 3) says ViTs are "not inherently rotation invariant"; the text is internally inconsistent on this point.
- Page 7 says "10 tries per object category" (2 instances × 5), consistent with Table II's six 5-try rows and n = 30 overall.
- Fig. 4 (frame rates per configuration) and Fig. 5 (α sweep) are plots only; numeric frame rates were not extractable from the text.
- The 31.2% relative improvement matches Table I perturbed rates (76.6 vs ORB 58.4).

## Suggested new concepts

- Visual servoing with foundation-model features — a recurring pattern of zero-shot correspondence feeding classical controllers.
- Image-based visual servoing (IBVS) — core control scheme used and compared across many servoing papers.
- DINOv2 dense correspondences — pretrained ViT patch matching reused for pose, grasping and servoing.
- Category-level manipulation — transferring a task from one reference instance to unseen same-category objects.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H5.** IBVS con features DINOv2 preentrenadas que no necesita entrenamiento por tarea y es candidato directo para la aproximación fina con cámara de muñeca.
