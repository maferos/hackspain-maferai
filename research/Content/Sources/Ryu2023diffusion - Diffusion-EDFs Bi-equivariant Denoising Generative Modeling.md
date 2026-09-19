---
aliases: []
type: "source"
title: "Diffusion-EDFs: Bi-equivariant Denoising Generative Modeling on SE(3) for Visual Robotic Manipulation"
citekey: "Ryu2023diffusion"
doi: "10.48550/arXiv.2309.02685"
arxiv: "2309.02685"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2309.02685"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Hyunwoo Ryu", "Jiwoo Kim", "Hyunseok An", "Junwoo Chang", "Joohwan Seo", "Taehan Kim", "Yubin Kim", "Chaewon Hwang", "Jongeun Choi", "Roberto Horowitz"]
sha256: ["edeb2b8589c87ee29624c47f7a8e5938267dd29eaed9ea4a1e6e83ca68356b42"]
pdf: "Content/Papers/Ryu2023diffusion.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 65
---

📄 PDF: [[Ryu2023diffusion.pdf]]

> [!abstract] One-sentence summary
> Diffusion-EDFs build a bi-equivariant score-based diffusion model on SE(3) that learns 6-DoF pick-and-place poses from 5 to 10 point-cloud demonstrations without pre-training or segmentation, training far faster than energy-based EDFs while generalizing to unseen instances, poses and clutter.

## Abstract

Diffusion generative modeling has become a promising approach for learning robotic manipulation tasks from stochastic human demonstrations. In this paper, we present Diffusion-EDFs, a novel SE(3)-equivariant diffusion-based approach for visual robotic manipulation tasks. We show that our proposed method achieves remarkable data efficiency, requiring only 5 to 10 human demonstrations for effective end-to-end training in less than an hour. Furthermore, our benchmark experiments demonstrate that our approach has superior generalizability and robustness compared to state-of-the-art methods. Lastly, we validate our methods with real hardware experiments. Project Website: https://sites.google.com/view/diffusion-edfs/home (arXiv)

## 🧠 Key ideas (atomic)

- Diffusion-EDFs are presented as an [[Diffusion models on Lie groups|SE(3)-equivariant diffusion-based approach]] for visual robotic manipulation tasks using point cloud observations. (Ryu et al., 2023) `ev:asserted` p. 1 ^ryu2023diffusion-001
- Diffusion-EDFs are described as a diffusion-based alternative to EDFs with a significantly reduced training time of ×15 faster. (Ryu et al., 2023) `ev:asserted` p. 1 ^ryu2023diffusion-002
- Equivariant Descriptor Fields require more than 10 hours to learn from only a few demonstrations, due to inefficient energy-based model training. (Ryu et al., 2023) `ev:cited` p. 1 ^ryu2023diffusion-003
- The authors state that earlier diffusion policies such as SE(3)-Diffusion Fields require numerous demonstrations to learn manipulation tasks. (Ryu et al., 2023) `ev:cited` p. 1 ^ryu2023diffusion-004
- The method is designed to be trained end-to-end from only 5∼10 human demonstrations without any pre-training or object segmentation. (Ryu et al., 2023) `ev:asserted` p. 1 ^ryu2023diffusion-005
- The authors claim this is the first work to address an [[Diffusion models on Lie groups|SE(3)-equivariant diffusion model]] for visual robotic manipulation. (Ryu et al., 2023) `ev:asserted` p. 1 ^ryu2023diffusion-006
- The target end-effector pose distribution is modelled as bi-equivariant with respect to the scene point cloud and grasp point cloud. (Ryu et al., 2023) `ev:reported` p. 3 ^ryu2023diffusion-007
- The diffused marginal is guaranteed bi-equivariant for every bi-equivariant initial distribution exactly when the diffusion kernel is bi-equivariant. (Ryu et al., 2023) `ev:computed` p. 3 ^ryu2023diffusion-008
- The Brownian diffusion kernel on SE(3) is shown to be left invariant but not right invariant under group actions. (Ryu et al., 2023) `ev:computed` p. 3 ^ryu2023diffusion-009
- The authors show that there exists no square-integrable kernel on the SE(3) manifold that is bi-invariant. (Ryu et al., 2023) `ev:computed` p. 3 ^ryu2023diffusion-010
- Bi-equivariant diffusion kernels are implemented with an equivariant diffusion frame selection mechanism that depends on the observed point clouds. (Ryu et al., 2023) `ev:reported` p. 3 ^ryu2023diffusion-011
- With the Brownian kernel, only an equivariant diffusion origin selection, not a full frame selection, is needed for a bi-equivariant kernel. (Ryu et al., 2023) `ev:computed` p. 4 ^ryu2023diffusion-012
- The score model is trained with a mean squared error loss that does not require integrating the frame-dependent diffusion kernel. (Ryu et al., 2023) `ev:reported` p. 4 ^ryu2023diffusion-013
- The minimizer of this loss is derived to be the score of the diffused marginal, not the score of the kernel. (Ryu et al., 2023) `ev:computed` p. 4 ^ryu2023diffusion-014
- Instead of autograd packages, the target Brownian score is computed with an explicit form the authors describe as more stable. (Ryu et al., 2023) `ev:reported` p. 4 ^ryu2023diffusion-015
- The rotational score is modelled as the sum of a spin term with an orbital term built from translational score fields. (Ryu et al., 2023) `ev:reported` p. 4 ^ryu2023diffusion-016
- Each score field combines two different EDFs, one encoding the scene point cloud, the other encoding the grasped-object point cloud. (Ryu et al., 2023) `ev:reported` p. 4 ^ryu2023diffusion-017
- The diffusion origin is sampled among grasp points in proportion to the number of scene points within a contact radius r. (Ryu et al., 2023) `ev:reported` p. 5 ^ryu2023diffusion-018
- The authors find that contact-based origin selection lets the model attend to contact-rich relevant sub-geometries without explicit supervision. (Ryu et al., 2023) `ev:asserted` p. 5 ^ryu2023diffusion-019
- The original EDFs have small receptive fields due to memory constraints, which the authors see as a problem for denoising. (Ryu et al., 2023) `ev:cited` p. 5 ^ryu2023diffusion-020
- A U-Net-like multiscale EDF architecture is proposed to maintain a wide receptive field without losing local high-frequency details. (Ryu et al., 2023) `ev:reported` p. 5 ^ryu2023diffusion-021
- The feature extractor is a deep SE(3)-equivariant GNN encoder that runs only once at the beginning of the denoising process. (Ryu et al., 2023) `ev:reported` p. 5 ^ryu2023diffusion-022
- The field model is a much shallower GNN evaluated at each denoising step to compute field values at query points. (Ryu et al., 2023) `ev:reported` p. 5 ^ryu2023diffusion-023
- Equiformer is used as the SE(3)-equivariant backbone GNN, with skip connections added through point pooling layers. (Ryu et al., 2023) `ev:reported` p. 5 ^ryu2023diffusion-024
- The query weight field that weights each query point is implemented as an EDF with a single scalar type-0 output. (Ryu et al., 2023) `ev:reported` p. 6 ^ryu2023diffusion-025
- The simulation benchmark compares Diffusion-EDFs with R-NDFs and SE(3)-Diffusion Fields on mug and bottle pick-and-place tasks. (Ryu et al., 2023) `ev:reported` p. 6 ^ryu2023diffusion-026
- Generalization is assessed on previously unseen object instances, object poses, clutters of distracting objects, or all three combined. (Ryu et al., 2023) `ev:reported` p. 6 ^ryu2023diffusion-027
- All models in the simulation benchmark are trained with ten task demonstrations performed by humans. (Ryu et al., 2023) `ev:reported` p. 6 ^ryu2023diffusion-028
- Training data use five object instances in only upright poses, each demonstrated for two different pick or place poses. (Ryu et al., 2023) `ev:reported` p. 25 ^ryu2023diffusion-029
- Training Diffusion-EDFs took 20∼45 minutes for a single pick or place task with an RTX 3090 GPU. (Ryu et al., 2023) `ev:measured` p. 6 ^ryu2023diffusion-030
- Simulated evaluations use SAPIEN with nine ceiling-mounted depth cameras, assuming perfect observation to remove point cloud processing effects. (Ryu et al., 2023) `ev:reported` p. 24 ^ryu2023diffusion-031
- A floating gripper-only robot that teleports to pre-pick or pre-place poses removes kinematic and motion planning failures from evaluation. (Ryu et al., 2023) `ev:reported` p. 24 ^ryu2023diffusion-032
- Simulated success is judged by turning off environment collision and checking the object's z-axis position to detect falls. (Ryu et al., 2023) `ev:reported` p. 24 ^ryu2023diffusion-033
- R-NDFs use pre-trained weights learned from 150 gigabytes of category-specific object geometry for mugs, bowls and bottles. (Ryu et al., 2023) `ev:reported` p. 25 ^ryu2023diffusion-034
- Naively pre-training NDFs on meshes reconstructed from the ten task demonstrations gave less than 5% success rate. (Ryu et al., 2023) `ev:measured` p. 25 ^ryu2023diffusion-035
- SE(3)-Diffusion Fields are trained with SO(3) rotational data augmentation because their overall architecture is not equivariant. (Ryu et al., 2023) `ev:reported` p. 25 ^ryu2023diffusion-036
- The authors report that Diffusion-EDFs outperform both baselines in almost all scenarios despite no pre-training or segmented inputs. (Ryu et al., 2023) `ev:measured` p. 6 ^ryu2023diffusion-037
- In the default simulated setup, Diffusion-EDFs reached total success rates of 0.95 on mugs versus 0.83 on bottles. (Ryu et al., 2023) `ev:measured` p. 7 ^ryu2023diffusion-038
- With previously unseen instances, Diffusion-EDFs reached total success rates of 0.92 on mugs versus 0.90 on bottles. (Ryu et al., 2023) `ev:measured` p. 7 ^ryu2023diffusion-039
- With previously unseen poses, Diffusion-EDFs reached total success rates of 0.96 on mugs versus 0.79 on bottles. (Ryu et al., 2023) `ev:measured` p. 7 ^ryu2023diffusion-040
- With previously unseen clutters, Diffusion-EDFs reached total success rates of 0.91 on mugs versus 0.87 on bottles. (Ryu et al., 2023) `ev:measured` p. 7 ^ryu2023diffusion-041
- With unseen instances, poses and clutters combined, Diffusion-EDFs reached total success rates of 0.79 on mugs versus 0.87 on bottles. (Ryu et al., 2023) `ev:measured` p. 7 ^ryu2023diffusion-042
- With segmented inputs in the default setup, R-NDFs reached total success rates of 0.81 on mugs versus 0.67 on bottles. (Ryu et al., 2023) `ev:measured` p. 7 ^ryu2023diffusion-043
- Without object segmentation, R-NDFs achieved zero success rates, which the authors attribute to the lack of locality in their design. (Ryu et al., 2023) `ev:measured` p. 6 ^ryu2023diffusion-044
- Without object segmentation, SE(3)-Diffusion Fields achieved success rates lower than 15% in all simulated scenarios. (Ryu et al., 2023) `ev:measured` p. 26 ^ryu2023diffusion-045
- The authors suggest the low SE(3)-DiffusionFields success rates are presumably due to their lack of SE(3)-equivariance. (Ryu et al., 2023) `ev:asserted` p. 6 ^ryu2023diffusion-046
- Real hardware experiments use a Franka Emika Panda arm with two Intel RealSense D415 RGB-D cameras. (Ryu et al., 2023) `ev:reported` p. 26 ^ryu2023diffusion-047
- The scene point cloud is built with RTAB-Map 3D SLAM from wrist camera views, using forward kinematics instead of visual odometry. (Ryu et al., 2023) `ev:reported` p. 26 ^ryu2023diffusion-048
- The grasp point cloud is captured by an external camera while the robot rotates the grasped object by 360◦. (Ryu et al., 2023) `ev:reported` p. 26 ^ryu2023diffusion-049
- Diffusion-EDFs learned the real mug-on-a-hanger task from only ten human demonstrations, including unseen instances in oblique poses. (Ryu et al., 2023) `ev:measured` p. 6 ^ryu2023diffusion-050
- Diffusion-EDFs learned the sequential bowls-on-dishes task in correct red-green-blue order from only ten human demonstrations. (Ryu et al., 2023) `ev:measured` p. 7 ^ryu2023diffusion-051
- The authors state that the bowls-on-dishes task requires scene-level comprehension, which is impossible for methods relying on object segmentation. (Ryu et al., 2023) `ev:asserted` p. 7 ^ryu2023diffusion-052
- Diffusion-EDFs learned the bottles-on-a-shelf task from four human demonstrations, each consisting of three sequential pick-and-place subtasks. (Ryu et al., 2023) `ev:measured` p. 8 ^ryu2023diffusion-053
- On real hardware, the authors achieved over 90% success rate for all subtasks except mug placement and bottle picking. (Ryu et al., 2023) `ev:measured` p. 27 ^ryu2023diffusion-054
- Real-robot mug placement and bottle picking reached success rates roughly around 80%, according to the authors. (Ryu et al., 2023) `ev:measured` p. 27 ^ryu2023diffusion-055
- Most errors in those two subtasks came from a slight positional inaccuracy of less than a centimeter. (Ryu et al., 2023) `ev:measured` p. 27 ^ryu2023diffusion-056
- For mugs and bottles, generating 20 poses for picking took 5∼6 seconds on the real-world setup. (Ryu et al., 2023) `ev:measured` p. 27 ^ryu2023diffusion-057
- Training each real-world model took less than 24 minutes for mug picking with an RTX3090 GPU. (Ryu et al., 2023) `ev:measured` p. 27 ^ryu2023diffusion-058
- An auxiliary diffusion-time-conditioned energy function is trained to sort generated poses by quality before motion planning is attempted. (Ryu et al., 2023) `ev:reported` p. 27 ^ryu2023diffusion-059
- Lacking a contrastive mechanism, the diffusion-trained energy function often assigns too low energy values to outlier poses. (Ryu et al., 2023) `ev:asserted` p. 27 ^ryu2023diffusion-060
- The Langevin sampler uses k1 = 0.5 for step size scheduling with k2 = 1.0 for temperature scheduling. (Ryu et al., 2023) `ev:reported` p. 22 ^ryu2023diffusion-061
- One limitation stated by the authors is that Diffusion-EDFs are unable to perform control-level or trajectory-level inference. (Ryu et al., 2023) `ev:asserted` p. 9 ^ryu2023diffusion-062
- Another stated limitation is the necessary grasp observation procedure, which prevents application of the method to closed-loop inference. (Ryu et al., 2023) `ev:asserted` p. 9 ^ryu2023diffusion-063
- Real-world approach directions rely on predefined task-specific motion primitives, since the work only infers the target pose itself. (Ryu et al., 2023) `ev:asserted` p. 26 ^ryu2023diffusion-064
- The authors note real hardware success rates may largely differ across systems depending on observation, calibration and motion planning quality. (Ryu et al., 2023) `ev:asserted` p. 27 ^ryu2023diffusion-065

## 🎯 Contributions

## 📖 Glossary

- **Bi-equivariance** — Pose distribution transforming consistently under both scene transformations (left) and grasped-object transformations (right).
- **Equivariant Descriptor Field (EDF)** — SO(3)-equivariant, translation-invariant vector field on R3 generated from a point cloud.
- **Score function** — Gradient of the log-probability, here a Lie-algebra-valued field over SE(3) poses.
- **IGSO(3)** — Isotropic Gaussian distribution on SO(3), the rotational part of Brownian diffusion on SE(3).
- **Annealed Langevin MCMC** — Sampler that follows learned scores while gradually decreasing diffusion time toward zero.
- **Diffusion origin selection** — Choosing the reference point for diffusion, here near contact-rich points of the grasp.
- **Query points** — Points sampled from the grasp cloud where score fields are evaluated and weighted.
- **R-NDFs** — Relational Neural Descriptor Fields, an SE(3)-equivariant baseline relying on category-specific pre-training.

## ❓ Open questions

- Can the bi-equivariant score model be extended to infer approach directions or full trajectories rather than only target poses?
- Can point cloud segmentation remove the separate grasp observation step and enable closed-loop inference?
- How would results change with noisy simulated observations instead of the perfect observations assumed in the benchmark?
- Why does bottle placement stay lower than mug placement across simulated scenarios?
- Can an energy function be trained with a contrastive term so that too-low-energy outliers need no heuristic rejection?
- How does the method scale to object categories and tasks with far less structured contact geometry than mugs and bottles?

## 📝 Notes on reading

Version read: arXiv 2309.02685v3 (28 Nov 2023), including the supplementary material (pp. 13-31).

Table 1 (p. 7) lost its checkmark columns (Without Pretraining, Without Obj. Seg., Without Rot. Aug.) in extraction. Baselines appear as two blocks of values; the second block (all 0.00 for R-NDFs, low values with n/a for SE(3)-DiffusionFields) was read as the unsegmented setting, matching the text on p. 6 and p. 26. Only Diffusion-EDFs' total columns and the default R-NDFs segmented totals were claimed; per-cell pick/place values were not claimed. Rows marked § test segmented baselines without clutter.

The abstract and introduction say 5 to 10 demonstrations, while the bottles-on-a-shelf task used four demonstrations (each with three sequential subtasks). The abstract says training in less than an hour, but the bowl-placing model took less than 1.3 hours (p. 27); the paper notes the one-hour figure excludes bowl placing and assumes three GPUs in parallel.

The ×15 speedup over EDFs (p. 1) is stated without a side-by-side training-time table in the text. The introduction misspells the method as Diffuion-EDFs.

Figures 1, 2, 7, 8, 9 (overview, multiscale architecture, modules, origin-selection rationale, learned query weights highlighting the mug handle and bottle bottom) and Figures 10-13 (real-world pose samples) were described only; the query weight visualization is qualitative.

Real-robot success rates (p. 27) are approximate (over 90%, roughly around 80%) and the >90% sample-quality figure with the energy critic is subject to human evaluation.

## Suggested new concepts

- Bi-equivariance in manipulation — scene (left) and grasp (right) equivariance recur across EDF-family methods and relational rearrangement.
- Diffusion models on Lie groups — SE(3)/SO(3) score-based generative modelling is shared with protein docking and grasp generation work.
- Equivariant Descriptor Fields — the base representation extended here, used by several pick-and-place learning methods.
- Contact-based locality in equivariant policies — local sub-geometry focus explains robustness to clutter and unsegmented scenes.
- Energy-based critic for sample ranking — reused to filter infeasible or unconverged generated poses before motion planning.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H4.** Difusión bi-equivariante en $SE(3)$ (respecto a la escena y a la pinza) sobre campos de descriptores; aprende pick-and-place con 5-10 demostraciones.

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
