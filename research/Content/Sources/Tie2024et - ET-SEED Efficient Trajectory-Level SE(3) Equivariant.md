---
aliases: []
type: "source"
title: "ET-SEED: Efficient Trajectory-Level SE(3) Equivariant Diffusion Policy"
citekey: "Tie2024et"
doi: "10.48550/arXiv.2411.03990"
arxiv: "2411.03990"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2411.03990"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Chenrui Tie", "Yue Chen", "Ruihai Wu", "Boxuan Dong", "Zeyi Li", "Chongkai Gao", "Hao Dong"]
sha256: ["093bcbd1cb86934a97705385b88234fa82d89ed47286e047295ca4c177cb5902"]
pdf: "Content/Papers/Tie2024et.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Tie2024et.pdf]]

> [!abstract] One-sentence summary
> ET-SEED is an SE(3) equivariant trajectory diffusion policy that makes only the last denoising step equivariant, improving data efficiency and spatial generalization in simulated and real manipulation.

## Abstract

Imitation learning, e.g., diffusion policy, has been proven effective in various robotic manipulation tasks. However, extensive demonstrations are required for policy robustness and generalization. To reduce the demonstration reliance, we leverage spatial symmetry and propose ET-SEED, an efficient trajectory-level SE(3) equivariant diffusion model for generating action sequences in complex robot manipulation tasks. Further, previous equivariant diffusion models require the per-step equivariance in the Markov process, making it difficult to learn policy under such strong constraints. We theoretically extend equivariant Markov kernels and simplify the condition of equivariant diffusion process, thereby significantly improving training efficiency for trajectory-level SE(3) equivariant diffusion policy in an end-to-end manner. We evaluate ET-SEED on representative robotic manipulation tasks, involving rigid body, articulated and deformable object. Experiments demonstrate superior data efficiency and manipulation proficiency of our proposed method, as well as its ability to generalize to unseen configurations with only a few demonstrations. Website: https://et-seed.github.io/ (arXiv)

## 🧠 Key ideas (atomic)

- ET-SEED is proposed as a trajectory-level SE(3) equivariant diffusion model that generates action sequences for robot manipulation tasks. (Tie et al., 2024) `ev:asserted` p. 2 ^tie2024et-001
- The authors state that previous trajectory-level equivariant diffusion models assume every transition step of the diffusion process must preserve equivariance. (Tie et al., 2024) `ev:asserted` p. 2 ^tie2024et-002
- The authors argue that training equivariant networks is more challenging than invariant ones, requiring more computation and converging more slowly. (Tie et al., 2024) `ev:asserted` p. 2 ^tie2024et-003
- The authors argue that defining the diffusion process in Euclidean space is not a natural definition and limits expressiveness. (Tie et al., 2024) `ev:asserted` p. 2 ^tie2024et-004
- ET-SEED is designed to restrict equivariant operations during denoising in order to improve sample efficiency and decrease training difficulty. (Tie et al., 2024) `ev:asserted` p. 2 ^tie2024et-005
- Extending equivariant Markov process theory, the authors prove that the full denoising process requires at least only one equivariant transition. (Tie et al., 2024) `ev:computed` p. 2 ^tie2024et-006
- ET-SEED integrates [[Diffusion models on Lie groups|diffusion on the SE(3) manifold]] with SE(3) transformers to build a trajectory-level equivariant diffusion model on SE(3) space. (Tie et al., 2024) `ev:reported` p. 2 ^tie2024et-007
- Most prior works applying SE(3) equivariance to 3D manipulation focus on equivariant pose estimation of the target object or end-effector. (Tie et al., 2024) `ev:cited` p. 2 ^tie2024et-008
- Most previous equivariant manipulation studies either generate only a single 6D pose or fail to guarantee end-to-end equivariance across SE(3). (Tie et al., 2024) `ev:cited` p. 3 ^tie2024et-009
- Diffusion-EDFs and OrbitGrasp introduced SE(3) equivariant diffusion for target grasp pose prediction but lack capability to generate entire manipulation trajectories. (Tie et al., 2024) `ev:cited` p. 3 ^tie2024et-010
- EquiBot extended equivariant diffusion policies to SIM(3) transformations, assuming every transition step in the diffusion process is equivariant. (Tie et al., 2024) `ev:cited` p. 3 ^tie2024et-011
- SE(3)-Diffusion Fields suggests that formulating [[Diffusion models on Lie groups|diffusion on the SE(3) manifold]] improves coverage of multimodal distributions in 6-DoF grasp pose generation. (Tie et al., 2024) `ev:cited` p. 3 ^tie2024et-012
- The observation in ET-SEED is a colored point cloud represented as an N by 6 array of point coordinates and colors. (Tie et al., 2024) `ev:reported` p. 4 ^tie2024et-013
- Each action is defined directly as the desired 6D pose of the end-effector in SE(3), so action sequences are end-effector trajectories. (Tie et al., 2024) `ev:reported` p. 4 ^tie2024et-014
- In ET-SEED, a random trajectory first passes K−1 SE(3) invariant denoising transitions and finally a single SE(3) equivariant transition. (Tie et al., 2024) `ev:reported` p. 4 ^tie2024et-015
- GeoDiff showed that an SE(3) invariant initial distribution with SE(3) equivariant Markov transitions yields an SE(3) invariant final density. (Tie et al., 2024) `ev:cited` p. 5 ^tie2024et-016
- Proposition 1 states that an invariant initial distribution, invariant transitions, one p2-type transition then p3-type transitions give an equivariant marginal. (Tie et al., 2024) `ev:computed` p. 5 ^tie2024et-017
- The authors state that building an SE(3) equivariant network in most implementations takes more computing resources than an invariant version. (Tie et al., 2024) `ev:asserted` p. 5 ^tie2024et-018
- ET-SEED sets the parameter n to 2, giving K−1 invariant denoising steps and one SE(3) equivariant denoising step. (Tie et al., 2024) `ev:reported` p. 5 ^tie2024et-019
- The authors state that existing equivariant backbones cannot output a translation vector anywhere in 3D space, including beyond the object's convex hull. (Tie et al., 2024) `ev:asserted` p. 5 ^tie2024et-020
- ET-SEED assumes the fully noised action follows a Gaussian distribution on SE(3) centred at the identity transformation. (Tie et al., 2024) `ev:reported` p. 6 ^tie2024et-021
- The forward process applies an Exp-mapped perturbation noise to an SE(3) interpolation between the clean action and the identity transformation. (Tie et al., 2024) `ev:reported` p. 6 ^tie2024et-022
- The denoising network takes the observation, the noisy action sequence and the step index, and outputs a relative transformation to the clean sequence. (Tie et al., 2024) `ev:reported` p. 7 ^tie2024et-023
- Proposition 2 states that transforming the input observation by any SE(3) element transforms the denoised action sequence by the same element. (Tie et al., 2024) `ev:computed` p. 7 ^tie2024et-024
- The six simulation tasks are Open Bottle Cap, Open Door, Rotate Triangle, Calligraphy, Cloth Folding and Cloth Fling. (Tie et al., 2024) `ev:reported` p. 8 ^tie2024et-025
- ET-SEED is compared against 3D Diffusion Policy, DP3 with SE(3) data augmentation, and the SIM(3)-equivariant EquiBot baseline. (Tie et al., 2024) `ev:reported` p. 8 ^tie2024et-026
- The DP3+Aug baseline rotates training observations about all three axes by random angles between 0 and 90 degrees. (Tie et al., 2024) `ev:reported` p. 9 ^tie2024et-027
- The DP3+Aug Gaussian offset on observations uses a standard deviation set to 10% of the workspace size. (Tie et al., 2024) `ev:reported` p. 9 ^tie2024et-028
- All methods are evaluated with 20 rollouts averaged over 5 random seeds, reporting success rate and SE(3) geodesic distance. (Tie et al., 2024) `ev:reported` p. 9 ^tie2024et-029
- The authors state that final success rate alone is inadequate for assessing trajectory quality, so they compute per-step geodesic distances. (Tie et al., 2024) `ev:asserted` p. 9 ^tie2024et-030
- With 50 demonstrations on Rotate Triangle New Poses, ET-SEED reached 89±4.18 success versus 86±5.48 for EquiBot and 10±2.74 for DP3. (Tie et al., 2024) `ev:measured` p. 8 ^tie2024et-031
- On Calligraphy New Poses with 25 demonstrations, ET-SEED reached 36±6.52 success, compared with 14±10.84 for EquiBot and 0±0.00 for DP3. (Tie et al., 2024) `ev:measured` p. 8 ^tie2024et-032
- On Fling Garment New Poses with 50 demonstrations, EquiBot reached 64±8.22 success, slightly above the 62±5.70 of ET-SEED. (Tie et al., 2024) `ev:measured` p. 8 ^tie2024et-033
- On Open Door New Poses with 50 demonstrations, EquiBot reached 77±7.58 success against 76±2.24 for ET-SEED. (Tie et al., 2024) `ev:measured` p. 8 ^tie2024et-034
- On Calligraphy New Poses with 25 demonstrations, ET-SEED had a geodesic distance of 0.121 against 4.988 for DP3. (Tie et al., 2024) `ev:measured` p. 8 ^tie2024et-035
- On Fold Garment New Poses with 50 demonstrations, ET-SEED had a geodesic distance of 0.136 against 0.288 for EquiBot. (Tie et al., 2024) `ev:measured` p. 8 ^tie2024et-036
- DP3 and DP3+Aug perform strongly in the Training setting but show a significant performance drop on New Poses. (Tie et al., 2024) `ev:measured` p. 9 ^tie2024et-037
- The authors conclude that merely incorporating data augmentation is insufficient for the model to generalize effectively to unseen poses. (Tie et al., 2024) `ev:asserted` p. 9 ^tie2024et-038
- EquiBot is reported to struggle on complex long-horizon tasks such as Calligraphy and Fold Garment in the simulation benchmark. (Tie et al., 2024) `ev:measured` p. 9 ^tie2024et-039
- The authors attribute the difficulties of EquiBot to maintaining equivariance in each Markov transition of its diffusion process. (Tie et al., 2024) `ev:asserted` p. 9 ^tie2024et-040
- The authors state that ET-SEED consistently outperforms across all six tasks with minimal performance drop on unseen object poses. (Tie et al., 2024) `ev:asserted` p. 9 ^tie2024et-041
- In the Open Door New Pose ablation, ET-SEED averaged 76±2.24 success versus 24±4.48 without SE(3) backbones. (Tie et al., 2024) `ev:measured` p. 9 ^tie2024et-042
- Replacing the SE(3) equivariant denoising process with non-equivariant DDIM lowered Open Door New Pose success to 57±6.52. (Tie et al., 2024) `ev:measured` p. 9 ^tie2024et-043
- The ablation without SE(3) equivariance replaces the backbone with a standard PointNet++ that predicts noise at each step. (Tie et al., 2024) `ev:reported` p. 9 ^tie2024et-044
- Real-world experiments use a Franka arm with Azure Kinect and RealSense cameras fused into point clouds across four tasks. (Tie et al., 2024) `ev:reported` p. 10 ^tie2024et-045
- Objects are segmented from the real scene with SAM2, and the segmented depth image is projected to a point cloud. (Tie et al., 2024) `ev:reported` p. 10 ^tie2024et-046
- Only 20 keyboard-teleoperated demonstrations were collected per real task because demonstration collection was very time-consuming. (Tie et al., 2024) `ev:reported` p. 10 ^tie2024et-047
- Each real task was tested at 10 unseen positions and poses, with one trial per position. (Tie et al., 2024) `ev:reported` p. 10 ^tie2024et-048
- In real-world Open Bottle Cap, ET-SEED reached a success rate of 0.8 against 0.6 for EquiBot and 0.2 for DP3. (Tie et al., 2024) `ev:measured` p. 10 ^tie2024et-049
- In real-world Calligraphy, all three baselines scored a 0.0 success rate, compared with 0.4 for ET-SEED. (Tie et al., 2024) `ev:measured` p. 10 ^tie2024et-050
- In real-world Fold Garment, ET-SEED reached a 0.6 success rate compared with 0.3 for EquiBot. (Tie et al., 2024) `ev:measured` p. 10 ^tie2024et-051
- ET-SEED requires pre-processing to extract segmented object point clouds, since its equivariance is designed for object point clouds. (Tie et al., 2024) `ev:asserted` p. 10 ^tie2024et-052
- ET-SEED assumes that inverse kinematics solvers and controllers let the end-effectors reach any feasible 6D pose. (Tie et al., 2024) `ev:asserted` p. 10 ^tie2024et-053
- The authors state that the 6D end-effector pose action space cannot tackle dexterous manipulation tasks needing higher-dimensional action spaces. (Tie et al., 2024) `ev:asserted` p. 10 ^tie2024et-054
- In the single-step test, the invariant P1Net reached a final loss of 0.0002 against 0.25 for P2Net and 0.27 for P3Net. (Tie et al., 2024) `ev:measured` p. 16 ^tie2024et-055
- The authors observe that higher-type features in P2Net and P3Net increase memory requirements and inference times. (Tie et al., 2024) `ev:measured` p. 16 ^tie2024et-056
- In the multi-step test, the invariant-plus-equivariant diffusion process converges much faster than the purely equivariant process. (Tie et al., 2024) `ev:measured` p. 17 ^tie2024et-057
- The equivariant module predicts each translation as the point cloud mass center plus a rotation matrix applied to an invariant offset. (Tie et al., 2024) `ev:reported` p. 18 ^tie2024et-058
- The authors state that Fold Garment and Fling Garment trajectories are not exactly equivariant because garment deformation differs per initialization. (Tie et al., 2024) `ev:asserted` p. 19 ^tie2024et-059
- In simulation, Open Bottle Cap only requires lifting the cap upward without twisting, due to simulator constraints. (Tie et al., 2024) `ev:reported` p. 19 ^tie2024et-060

## 🎯 Contributions

## 📖 Glossary

- **SE(3)** — group of 3D rigid transformations, combining a rotation and a translation.
- **se(3)** — six-dimensional Lie algebra, the tangent space of SE(3), linked by Exp and Log maps.
- **SE(3) equivariance** — transforming the input by T transforms the output by the same T.
- **SE(3) invariance** — output stays unchanged when the input is rigidly transformed.
- **Diffusion policy** — imitation policy that generates actions by iteratively denoising random samples.
- **Geodesic distance on SE(3)** — pose error combining rotation log-norm and translation distance.
- **Type-0 / type-1 features** — scalar features invariant to rotation versus vector features rotating with the input.
- **SE(3) Transformer** — attention network whose features are equivariant to 3D roto-translations.

## ❓ Open questions

- Does the one-equivariant-step design keep its advantage for dexterous hands needing higher-dimensional action spaces?
- How robust is ET-SEED to imperfect object segmentation or cluttered scene point clouds?
- Why does ET-SEED trail EquiBot on some 50-demonstration New Pose cells, such as Open Door and Fling Garment?
- How does the number of invariant steps K affect accuracy and training cost?
- Would the real-world advantage hold with more than 10 trials per task?

## 📝 Notes on reading

Version read: arXiv 2411.03990v2 (2 Mar 2025), marked as the ICLR 2025 conference paper; matches the packet identifier. The registry abstract adds the phrase in an end-to-end manner and a Website link that the PDF abstract lacks.

Figures 1, 5 and 6 were read only through their captions and axis labels. Figure 5 shows P1Net loss falling almost to 0 while P2Net and P3Net losses do not decrease obviously; Figure 6 shows the Inv+Eqv process converging faster than Pure Eqv. Figure 1(a) bar values are not recoverable from the extraction.

Tables 1 and 2 extracted as flattened rows; cells were matched by column order (T 25, T 50, NP 25, NP 50 per task). Inconsistency: the text says ET-SEED consistently outperforms across all six tasks, but Table 1 shows EquiBot higher on Open Door NP 50 (77 vs 76) and Fling Garment NP 50 (64 vs 62). In Table 2, the DP3+Aug rows for Fold Garment and Fling Garment are identical (1.318, 0.976, 1.524, 1.219), which may be a copy error. The ablation full-model value 76±2.24 matches the Table 1 Open Door NP 50 cell, suggesting the ablation used 50 demonstrations, though this is not stated.

The real-world results use single trials at 10 positions, so each success rate rests on 10 rollouts. Proof equations in appendices B and C were partly garbled in extraction and were not claimed beyond the proposition statements.

## Suggested new concepts

- SE(3) equivariant diffusion policy — a recurring family (EquiBot, Equivariant Diffusion Policy, ET-SEED) for data-efficient manipulation.
- Diffusion on Lie groups — diffusion defined on SE(3) or SO(3) manifolds rather than Euclidean space recurs across grasping and pose estimation.
- Equivariant Markov kernel conditions — the weaker invariant-then-equivariant condition could apply beyond manipulation.
- 3D Diffusion Policy (DP3) — a common point-cloud diffusion baseline for manipulation benchmarks.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H4.** Política de difusión equivariante en SE(3) a nivel de trayectoria que aprende con pocas demostraciones, de modo que el fine-tuning no tiene que reaprender la simetría.
