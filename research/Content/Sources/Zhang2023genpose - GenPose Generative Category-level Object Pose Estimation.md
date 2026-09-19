---
aliases: []
type: "source"
title: "GenPose: Generative Category-level Object Pose Estimation via Diffusion Models"
citekey: "Zhang2023genpose"
doi: "10.48550/arXiv.2306.10531"
arxiv: "2306.10531"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2306.10531"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Jiyao Zhang", "Mingdong Wu", "Hao Dong"]
sha256: ["9b582ba05ec16be084cad24a6a1336545fe5cfaa173b29e37def4ed0805232c9"]
pdf: "Content/Papers/Zhang2023genpose.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Zhang2023genpose.pdf]]

> [!abstract] One-sentence summary
> GenPose recasts category-level 6D pose estimation from depth as sampling pose candidates with a score-based diffusion model and filtering them with an energy-based diffusion model, tackling the multi-hypothesis issue of symmetric and partially observed objects.

## Abstract

Object pose estimation plays a vital role in embodied AI and computer vision, enabling intelligent agents to comprehend and interact with their surroundings. Despite the practicality of category-level pose estimation, current approaches encounter challenges with partially observed point clouds, known as the multihypothesis issue. In this study, we propose a novel solution by reframing categorylevel object pose estimation as conditional generative modeling, departing from traditional point-to-point regression. Leveraging score-based diffusion models, we estimate object poses by sampling candidates from the diffusion model and aggregating them through a two-step process: filtering out outliers via likelihood estimation and subsequently mean-pooling the remaining candidates. To avoid the costly integration process when estimating the likelihood, we introduce an alternative method that trains an energy-based model from the original score-based model, enabling end-to-end likelihood estimation. Our approach achieves state-of-the-art performance on the REAL275 dataset, surpassing 50% and 60% on strict 5d2cm and 5d5cm metrics, respectively. Furthermore, our method demonstrates strong generalizability to novel categories sharing similar symmetric properties without fine-tuning and can readily adapt to object pose tracking tasks, yielding comparable results to the current state-of-the-art baselines. (arXiv)

## 🧠 Key ideas (atomic)

- Regression-based training supervises the network for a single pose even when a partially observed point cloud admits multiple feasible pose hypotheses. (Zhang et al., 2023) `ev:asserted` p. 2 ^zhang2023genpose-001
- Partial observation can worsen the issue, since a mug with an obstructed handle may look the same from certain views. (Zhang et al., 2023) `ev:asserted` p. 2 ^zhang2023genpose-002
- Previous studies proposed ad-hoc fixes such as special network architectures or augmented ground-truth poses for symmetric objects. (Zhang et al., 2023) `ev:cited` p. 2 ^zhang2023genpose-003
- The authors argue that these ad-hoc solutions cannot fundamentally resolve the multi-hypothesis issue due to their lack of generality. (Zhang et al., 2023) `ev:asserted` p. 2 ^zhang2023genpose-004
- GenPose formulates [[Category-level object pose estimation|category-level object pose estimation]] as conditional generative modeling of the pose distribution given a partially observed point cloud. (Zhang et al., 2023) `ev:asserted` p. 2 ^zhang2023genpose-005
- Estimating likelihoods directly from score-based models requires a highly time-consuming integration process, which the authors consider impractical for real-time use. (Zhang et al., 2023) `ev:cited` p. 5 ^zhang2023genpose-006
- At test time, GenPose samples a group of pose candidates for an unseen point cloud with the score-based diffusion model. (Zhang et al., 2023) `ev:reported` p. 3 ^zhang2023genpose-007
- Pose candidates are ranked by the energy model output, and the lowest-ranked 1 −δ% of candidates are filtered out, e.g. δ = 60%. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023genpose-008
- The diffusion process uses a Variance-Exploding SDE with hyper-parameters σmin = 0.01 and σmax = 50 for the pose noise schedule. (Zhang et al., 2023) `ev:reported` p. 4 ^zhang2023genpose-009
- The score network is trained with denoising score matching, whose optimum equals the score of the perturbed conditional pose distribution. (Zhang et al., 2023) `ev:cited` p. 4 ^zhang2023genpose-010
- Pose candidates are sampled by solving the Probability Flow ODE from t = 1 to t = ϵ with an RK45 ODE solver. (Zhang et al., 2023) `ev:reported` p. 5 ^zhang2023genpose-011
- The score network encodes the partially observed point cloud into a global geometry feature using a PointNet++ backbone. (Zhang et al., 2023) `ev:reported` p. 5 ^zhang2023genpose-012
- The score network is implemented without any ad-hoc design for symmetric objects, relying on common feature extractors and feed-forward MLPs. (Zhang et al., 2023) `ev:reported` p. 5 ^zhang2023genpose-013
- The pose is represented as a 9-D variable made of a continuous 6-D rotation representation plus a translation vector. (Zhang et al., 2023) `ev:reported` p. 5 ^zhang2023genpose-014
- The authors argue that plain mean pooling can include low-likelihood outlier poses, which can negatively impact the pooled pose estimate. (Zhang et al., 2023) `ev:asserted` p. 5 ^zhang2023genpose-015
- The energy model is trained by supervising its energy-induced gradient with the same denoising score-matching objective used for the score model. (Zhang et al., 2023) `ev:reported` p. 5 ^zhang2023genpose-016
- The optimal energy model equals the log-likelihood up to a constant, so it can still rank candidates as a surrogate likelihood. (Zhang et al., 2023) `ev:computed` p. 5 ^zhang2023genpose-017
- Training an energy-based diffusion model directly is described as difficult and time-inefficient due to second-order derivatives in the objective. (Zhang et al., 2023) `ev:asserted` p. 5 ^zhang2023genpose-018
- Following prior work, the energy is parameterized as the inner product of the pose with a score-shaped network output. (Zhang et al., 2023) `ev:cited` p. 5 ^zhang2023genpose-019
- Retained candidate translations are pooled by vanilla averaging to form the translation of the final output pose. (Zhang et al., 2023) `ev:reported` p. 6 ^zhang2023genpose-020
- Retained rotations are averaged as quaternions by taking the maximum-eigenvalue eigenvector of a 4 × 4 matrix, solved with QUEST. (Zhang et al., 2023) `ev:reported` p. 6 ^zhang2023genpose-021
- For pose tracking, the PF-ODE is warm-started around the previous frame's estimate and solved from t = 0.1 to t = ϵ. (Zhang et al., 2023) `ev:reported` p. 6 ^zhang2023genpose-022
- Training and evaluation use the CAMERA and REAL275 datasets, which share 6 daily object categories including bottle, bowl and mug. (Zhang et al., 2023) `ev:reported` p. 6 ^zhang2023genpose-023
- CAMERA is a mixed-reality synthetic dataset of rendered objects on real backgrounds, with 275K training images and 25K test images. (Zhang et al., 2023) `ev:reported` p. 6 ^zhang2023genpose-024
- REAL275 contains 7 training scenes with 4.3K images and 6 test scenes with 2.75K images of real objects. (Zhang et al., 2023) `ev:reported` p. 6 ^zhang2023genpose-025
- Accuracy is reported as mean Average Precision under the 5◦2cm, 5◦5cm, 10◦2cm and 10◦5cm rotation and translation thresholds. (Zhang et al., 2023) `ev:reported` p. 6 ^zhang2023genpose-026
- Following NOCS, rotation error around the symmetry axis is ignored for symmetric objects, namely bottles, bowls and cans. (Zhang et al., 2023) `ev:reported` p. 6 ^zhang2023genpose-027
- Mugs are treated as symmetric objects when the handle is not visible and as non-symmetric objects when it is visible. (Zhang et al., 2023) `ev:reported` p. 7 ^zhang2023genpose-028
- For fair comparison, inference uses the same MaskRCNN instance masks as previous work to segment the observed objects. (Zhang et al., 2023) `ev:reported` p. 7 ^zhang2023genpose-029
- Each input point cloud given to the score-based and energy-based diffusion models consists of 1024 points. (Zhang et al., 2023) `ev:reported` p. 7 ^zhang2023genpose-030
- All experiments ran on a single RTX3090 with a batch size of 192, implemented in PyTorch. (Zhang et al., 2023) `ev:reported` p. 7 ^zhang2023genpose-031
- On REAL275, GenPose reaches 52.1 on 5◦2cm and 60.9 on 5◦5cm mAP using depth input without any category prior. (Zhang et al., 2023) `ev:measured` p. 7 ^zhang2023genpose-032
- On REAL275, GenPose reaches 72.4 on 10◦2cm and 84.0 on 10◦5cm, above every deterministic baseline listed in Table 1. (Zhang et al., 2023) `ev:measured` p. 7 ^zhang2023genpose-033
- The authors report exceeding GPV-Pose by more than 20% on both the strict 5◦2cm and 5◦5cm metrics on REAL275. (Zhang et al., 2023) `ev:measured` p. 7 ^zhang2023genpose-034
- Compared with DPDN, which uses RGB-D input and a category prior, GenPose gains over 10% on the 5◦5cm metric. (Zhang et al., 2023) `ev:measured` p. 7 ^zhang2023genpose-035
- With 4.4 M parameters, GenPose has the fewest network parameters among the methods reporting a parameter count in Table 1. (Zhang et al., 2023) `ev:measured` p. 7 ^zhang2023genpose-036
- When the candidate nearest to ground truth is selected among K=50 hypotheses, GenPose reaches 82.0 on 5◦2cm on REAL275. (Zhang et al., 2023) `ev:measured` p. 7 ^zhang2023genpose-037
- The authors interpret the nearest-to-ground-truth results as showing tremendous potential of conditional generative models for [[Category-level object pose estimation|category-level pose estimation]]. (Zhang et al., 2023) `ev:asserted` p. 7 ^zhang2023genpose-038
- On 10◦2cm, raising the number of candidates from 10 to 50 improves the δ = 60% result from 67.9 to 72.4. (Zhang et al., 2023) `ev:measured` p. 8 ^zhang2023genpose-039
- Raising the number of candidates from 50 to 100 gives a marginal gain, from 72.4 to 72.6 at δ = 60%. (Zhang et al., 2023) `ev:measured` p. 8 ^zhang2023genpose-040
- In the ablation, keeping 20% of candidates gives lower 10◦2cm scores than keeping 60% for every tested K. (Zhang et al., 2023) `ev:measured` p. 8 ^zhang2023genpose-041
- Keeping all candidates at δ = 100% also scores lower than δ = 60%, with 69.7 versus 72.4 at K = 50. (Zhang et al., 2023) `ev:measured` p. 8 ^zhang2023genpose-042
- Given the difficulty of training an energy model that precisely matches the actual distribution, the authors regard it primarily as an outlier detector. (Zhang et al., 2023) `ev:asserted` p. 8 ^zhang2023genpose-043
- With mean pooling, energy ranking reaches 52.1 on 5◦2cm on REAL275, against 49.4 for random ranking. (Zhang et al., 2023) `ev:measured` p. 8 ^zhang2023genpose-044
- Choosing a single random candidate without mean pooling yields 13.5 on the 5◦2cm metric on REAL275. (Zhang et al., 2023) `ev:measured` p. 8 ^zhang2023genpose-045
- Ranking candidates by their distance to ground truth gives an upper bound of 62.1 on 5◦2cm, which energy ranking does not reach. (Zhang et al., 2023) `ev:measured` p. 8 ^zhang2023genpose-046
- The energy model output shows a general negative correlation with pose error when plotted over sampled pose candidates. (Zhang et al., 2023) `ev:measured` p. 8 ^zhang2023genpose-047
- The energy model distinguishes poses with large error differences but performs poorly when distinguishing among poses with low errors. (Zhang et al., 2023) `ev:measured` p. 8 ^zhang2023genpose-048
- Against RBP-Pose on REAL275, GenPose raises the average 5◦2cm on symmetric categories from 55.9 to 70.2. (Zhang et al., 2023) `ev:measured` p. 9 ^zhang2023genpose-049
- On asymmetric categories, the average 5◦2cm rises from 21.3 for RBP-Pose to 32.2 for GenPose on REAL275. (Zhang et al., 2023) `ev:measured` p. 9 ^zhang2023genpose-050
- For the mug category, 5◦2cm rises from 18.9 with RBP-Pose to 35.7 with GenPose on REAL275. (Zhang et al., 2023) `ev:measured` p. 9 ^zhang2023genpose-051
- For the camera category, GenPose reaches 2.9 on 5◦2cm, compared with 1.3 for RBP-Pose on REAL275. (Zhang et al., 2023) `ev:measured` p. 9 ^zhang2023genpose-052
- When bowls are unseen in training, GenPose keeps 64.5 on 5◦2cm while RBP-Pose drops to 0.0. (Zhang et al., 2023) `ev:measured` p. 9 ^zhang2023genpose-053
- With cans unseen in training, GenPose scores 62.5 on 5◦2cm, compared with 7.3 for SAR-Net and 0.8 for RBP-Pose. (Zhang et al., 2023) `ev:measured` p. 9 ^zhang2023genpose-054
- With bottles unseen in training, GenPose scores 39.0 on 5◦2cm, against 11.7 for SAR-Net and 4.3 for RBP-Pose. (Zhang et al., 2023) `ev:measured` p. 9 ^zhang2023genpose-055
- The authors hypothesize that this out-of-distribution generalization arises from the learned point cloud feature space placing unseen categories near seen ones. (Zhang et al., 2023) `ev:asserted` p. 9 ^zhang2023genpose-056
- A t-SNE of ScoreNet point cloud features shows can and bottle features intermingling, consistent with their symmetrical cylindrical shapes. (Zhang et al., 2023) `ev:measured` p. 10 ^zhang2023genpose-057
- In the same t-SNE analysis, point cloud features from the bowl category lie close to features from mugs. (Zhang et al., 2023) `ev:measured` p. 10 ^zhang2023genpose-058
- For tracking, a perturbed ground-truth pose serves as the initial object pose, following the CAPTRA and CATRE protocol. (Zhang et al., 2023) `ev:reported` p. 10 ^zhang2023genpose-059
- In REAL275 tracking averaged over 6 categories, GenPose reaches 71.5 on 5◦5cm versus 57.2 for CATRE. (Zhang et al., 2023) `ev:measured` p. 10 ^zhang2023genpose-060
- In tracking, GenPose has a mean rotation error of 4.2 degrees, lower than 6.8 degrees for CATRE. (Zhang et al., 2023) `ev:measured` p. 10 ^zhang2023genpose-061
- In tracking, CATRE keeps a lower mean translation error than GenPose, 1.2 cm against 1.5 cm on REAL275. (Zhang et al., 2023) `ev:measured` p. 10 ^zhang2023genpose-062
- GenPose runs pose tracking at 17.18 FPS on REAL275, compared with 89.21 FPS for the CATRE baseline. (Zhang et al., 2023) `ev:measured` p. 10 ^zhang2023genpose-063
- The authors state that single-frame pose estimation efficiency is still limited by the costly sampling process of the score-based model. (Zhang et al., 2023) `ev:asserted` p. 10 ^zhang2023genpose-064
- As future work, the authors may use reinforcement learning to train an agent that actively increases the likelihood of estimated poses. (Zhang et al., 2023) `ev:asserted` p. 10 ^zhang2023genpose-065
- On CAMERA, GenPose outperforms the RBP-Pose baseline by a margin of 6.4% on the strict 5◦2cm metric. (Zhang et al., 2023) `ev:measured` p. 16 ^zhang2023genpose-066
- On the CAMERA dataset, GenPose reaches 79.9 on 5◦2cm and 84.4 on 5◦5cm with 4.4 M parameters. (Zhang et al., 2023) `ev:measured` p. 17 ^zhang2023genpose-067
- GenPose was integrated with a UFACTORY xArm6 arm and RealSense D435 camera for pouring, stacking and handover demonstrations. (Zhang et al., 2023) `ev:reported` p. 17 ^zhang2023genpose-068
- The authors note that evaluating on synthesized or human-collected datasets may introduce data bias into their results. (Zhang et al., 2023) `ev:asserted` p. 18 ^zhang2023genpose-069

## 🎯 Contributions

## 📖 Glossary

- **Multi-hypothesis issue** — several feasible poses for one partial point cloud, from symmetry or occlusion.
- **Category-level pose estimation** — estimating 6D pose of unseen instances of known categories without CAD models.
- **Score-based diffusion model** — generative model learning gradients of log-density under progressively added noise.
- **Energy-based diffusion model** — network outputting a scalar energy whose gradient matches the score.
- **Denoising score matching** — training objective regressing noise-perturbed samples toward clean data to learn scores.
- **Probability Flow ODE** — deterministic ODE whose solutions share marginals with the diffusion SDE.
- **VE SDE** — variance-exploding diffusion where noise scale grows geometrically between σmin and σmax.
- **6-D rotation representation** — two columns of a rotation matrix, continuous unlike quaternions or Euler angles.
- **5◦2cm metric** — share of poses with rotation error under 5 degrees and translation under 2 cm.
- **REAL275** — real-world category-level pose benchmark with 6 household object categories.

## ❓ Open questions

- Can faster diffusion samplers (consistency models, distillation) bring single-frame inference to real time without losing accuracy?
- How can the energy model be improved to discriminate among low-error candidates, closing the gap to the ground-truth ranking bound?
- Does cross-category generalization extend beyond categories that share symmetry properties with training categories?
- Why does the camera category stay near 3% on 5◦2cm, and would RGB features help?
- How does GenPose behave on transparent or specular objects where depth is unreliable?

## 📝 Notes on reading

Read the arXiv v3 (25 Dec 2023), the NeurIPS 2023 camera-ready version. The registry abstract states the 50%/60% thresholds; the PDF abstract does not.

Inconsistencies inside the paper: (1) p. 7 text calls GPV-Pose the current SOTA and claims a gain of more than 20% on both 5◦2cm and 5◦5cm, but Table 1 gives GPV-Pose 32.0/42.9 against 52.1/60.9, i.e. about 18 points on 5◦5cm; RBP-Pose (38.2/48.1) and DPDN (46.0/50.7) score higher than GPV-Pose in the same table. (2) The Table 2 text names the candidate count M while the table and elsewhere use K. (3) Table 1 and Table 7 list 2.2 M parameters for the Ours(K=10/50) rows versus 4.4 M for Ours, without explanation (4.4 likely counts score plus energy networks). (4) Tracking initialization: Sec 3.3 samples around the previous pose with variance σ2(0.1), while Algorithm 1 (p. 18) writes 0.12I. (5) Appendix B refers to Figure 2 for the qualitative comparison, which is actually Figure 7.

Table 4 extraction lost the symmetric flag for the camera row and the mug row's flag is '-'; per-category numbers for camera and laptop were read from the recovered cells. Figures 3, 4, 5, 8 and 9 (energy-error scatter, SO(3) rotation distributions, t-SNE, per-category curves, robot tasks) could only be described from captions and text.

## Suggested new concepts

- Multi-hypothesis issue in pose estimation — recurring problem for symmetric and occluded objects, relevant to vessel/bottle pose in the lab scene.
- Score-based diffusion for pose estimation — generative alternative to regression that other pose papers may build on.
- Energy-based candidate ranking — cheap surrogate likelihood for filtering diffusion samples, reusable beyond pose.
- Category-level object pose estimation — core task family (NOCS, REAL275/CAMERA benchmarks) for the vision pipeline.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H7.** Plantea la pose por categoría como difusión condicional con múltiples hipótesis, adecuada para objetos casi simétricos como los frascos.
