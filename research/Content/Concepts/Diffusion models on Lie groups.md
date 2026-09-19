---
aliases: []
type: concept
element_type: method
topic: "[[Probability, filtering and generative models on Lie groups]]"
topics: ["[[Probability, filtering and generative models on Lie groups]]"]
created: 2026-09-19
---

## Working definition

Score-based or denoising diffusion generative models whose noising and denoising processes are defined directly on a Lie group such as SO(3) or SE(3), used to sample multimodal distributions of rotations and rigid poses for pose estimation, grasping, manipulation and protein frames.

## Evidence

- [[Hsiao2023confronting - Confronting Ambiguity in 6D Object Pose Estimation via#^hsiao2023confronting-011]] — IGSO(3), used by earlier SO(3) diffusion models, lacks a closed form, which the authors say poses challenges for computational efficiency
- [[Hsiao2023confronting - Confronting Ambiguity in 6D Object Pose Estimation via#^hsiao2023confronting-013]] — The method samples 6D poses from an image-conditioned distribution using a score-based generative model whose prior is a Gaussian distribution on SE(3)
- [[Hsiao2023confronting - Confronting Ambiguity in 6D Object Pose Estimation via#^hsiao2023confronting-042]] — On T-LESS the SE(3) diffusion model reaches an MSPD of 93.16, against 90.17 for GDRNPP
- [[Hsiao2023confronting - Confronting Ambiguity in 6D Object Pose Estimation via#^hsiao2023confronting-045]] — The SE(3) diffusion model outperforms its R3SO(3) counterpart on all T-LESS metrics, for instance 93.16 against 85.73 MSPD
- [[Ryu2023diffusion - Diffusion-EDFs Bi-equivariant Denoising Generative Modeling#^ryu2023diffusion-001]] — Diffusion-EDFs are presented as an SE(3)-equivariant diffusion-based approach for visual robotic manipulation tasks using point cloud observations.
- [[Ryu2023diffusion - Diffusion-EDFs Bi-equivariant Denoising Generative Modeling#^ryu2023diffusion-006]] — The authors claim this is the first work to address an SE(3)-equivariant diffusion model for visual robotic manipulation.
- [[Urain2022se - SE(3)-DiffusionFields#^urain2022se-006]] — The authors state that SE(3) diffusion models better cover multimodal distributions, leading to better and more sample efficient subsequent robot planning.
- [[Urain2022se - SE(3)-DiffusionFields#^urain2022se-009]] — A diffusion model in SE(3) is a vector field that outputs a vector in R6 for any query pose, conditioned on a noise scale.
- [[Yim2023se - SE(3) diffusion model with application to protein backbone#^yim2023se-001]] — The paper develops theoretical foundations for SE(3) invariant diffusion models on multiple frames, applied to protein backbone generation.
- [[Yim2023se - SE(3) diffusion model with application to protein backbone#^yim2023se-002]] — Before this work no principled methodological framework existed for diffusion on SE(3) that operates on frames and confers group invariance.
- [[Tie2024et - ET-SEED Efficient Trajectory-Level SE(3) Equivariant#^tie2024et-007]] — ET-SEED integrates diffusion on the SE(3) manifold with SE(3) transformers to build a trajectory-level equivariant diffusion model on SE(3) space.
- [[Tie2024et - ET-SEED Efficient Trajectory-Level SE(3) Equivariant#^tie2024et-012]] — SE(3)-Diffusion Fields suggests that formulating diffusion on the SE(3) manifold improves coverage of multimodal distributions in 6-DoF grasp pose generation.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 5 sources · topic: Probability, filtering and generative models on Lie groups (drafter's packet `q2-lie-probability`, confirmed at the gate)
