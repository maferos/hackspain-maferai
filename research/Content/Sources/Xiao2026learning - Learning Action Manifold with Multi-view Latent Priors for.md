---
aliases: []
type: "source"
title: "Learning Action Manifold with Multi-view Latent Priors for Robotic Manipulation"
citekey: "Xiao2026learning"
doi: "10.48550/arXiv.2605.11832"
arxiv: "2605.11832"
year: 2026
publication_type: "preprint"
url: "https://arxiv.org/abs/2605.11832"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Junjin Xiao", "Dongyang Li", "Yandan Yang", "Shuang Zeng", "Tong Lin", "Xinyuan Chang", "Feng Xiong", "Mu Xu", "Xing Wei", "Zhiheng Ma", "Qing Zhang", "Wei-Shi Zheng"]
sha256: ["538d35b8a9bf621de724bed5d0fc4cb052110d47ab188e68cef715ebeffdb19f"]
pdf: "Content/Papers/Xiao2026learning.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Xiao2026learning.pdf]]

> [!abstract] One-sentence summary
> The paper builds a VLA policy that synthesizes latent novel views to reduce monocular depth ambiguity and predicts clean action chunks directly, reporting higher success and robustness on LIBERO, LIBERO-Plus, RoboTwin 2.0 and a real Franka arm.

## Abstract

This paper tackles spatial perception and manipulation challenges in Vision-Language-Action (VLA) models. To address depth ambiguity from monocular input, we leverage a pre-trained multi-view diffusion model to synthesize latent novel views and propose a Geometry-Guided Gated Transformer (G3T) that aligns multi-view features under 3D geometric guidance while adaptively filtering occlusion noise. To improve action learning efficiency, we introduce Action Manifold Learning (AML), which directly predicts actions on the valid action manifold, bypassing inefficient regression of unstructured targets like noise or velocity. Experiments on LIBERO, RoboTwin 2.0, and real-robot tasks show our method achieves superior success rate and robustness over SOTA baselines. Project page: https://junjxiao.github.io/Multi-view-VLA.github.io/. (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that 2D-image VLA methods have limited spatial awareness due to irreversible depth loss when projecting 3D space onto images. (Xiao et al., 2026) `ev:asserted` p. 1 ^xiao2026learning-001
- According to the authors, using explicit 3D inputs such as RGB-D requires costly extra hardware that limits overall scalability. (Xiao et al., 2026) `ev:asserted` p. 1 ^xiao2026learning-002
- The authors state that spatial features from 3D foundation models face monocular depth ambiguity when robots use a single RGB camera. (Xiao et al., 2026) `ev:asserted` p. 1 ^xiao2026learning-003
- The authors argue that regressing noise or velocity targets imposes an optimization burden that becomes more pronounced as action dimensionality increases. (Xiao et al., 2026) `ev:asserted` p. 1 ^xiao2026learning-004
- The framework uses a pre-trained multi-view diffusion model to synthesize latent representations of novel views from a single main camera image. (Xiao et al., 2026) `ev:reported` p. 2 ^xiao2026learning-005
- The Geometry-Guided Gated Transformer uses a monocular 3D geometric prior to guide the alignment of the synthesized multi-view latent features. (Xiao et al., 2026) `ev:reported` p. 2 ^xiao2026learning-006
- An adaptive gating mechanism in G3T is designed to aggregate informative views while suppressing noise from occluded regions. (Xiao et al., 2026) `ev:reported` p. 2 ^xiao2026learning-007
- The Action Manifold Hypothesis posits that successful actions reside on a low-dimensional smooth manifold shaped by physics, task goals, and environmental constraints. (Xiao et al., 2026) `ev:asserted` p. 2 ^xiao2026learning-008
- Action Manifold Learning directly predicts clean action chunks on the action manifold, unlike traditional diffusion policies that predict noise or velocity. (Xiao et al., 2026) `ev:reported` p. 2 ^xiao2026learning-009
- A dense 3D structural prior is extracted from the main view as the last-layer hidden state of the VGGT spatial encoder. (Xiao et al., 2026) `ev:reported` p. 4 ^xiao2026learning-010
- Left and right novel views are generated in latent space by the 6B LongCat-Image-Edit model, conditioned on target view prompts. (Xiao et al., 2026) `ev:reported` p. 4 ^xiao2026learning-011
- Synthesizing in latent space lets the authors reduce latent resolution to 256 × 256 and limit denoising steps to 2. (Xiao et al., 2026) `ev:reported` p. 4 ^xiao2026learning-012
- Since the generative module is frozen during policy training, latent features of the synthesized views are pre-computed and cached for the dataset. (Xiao et al., 2026) `ev:reported` p. 4 ^xiao2026learning-013
- Semantic and geometric features are fused by standard cross-attention, with semantic features as queries and spatial features as keys and values. (Xiao et al., 2026) `ev:reported` p. 4 ^xiao2026learning-014
- G3T operates through three sequential stages: cross-view alignment, adaptive gated fusion, and geometric consistency refinement of the spatial features. (Xiao et al., 2026) `ev:reported` p. 5 ^xiao2026learning-015
- Cross-view alignment projects VGGT and multi-view tokens to a shared dimension, concatenates them, and applies residual multi-head self-attention. (Xiao et al., 2026) `ev:reported` p. 5 ^xiao2026learning-016
- The gated fusion predicts a per-token sigmoid gate from concatenated left and right features to weight the two synthesized views. (Xiao et al., 2026) `ev:reported` p. 5 ^xiao2026learning-017
- The action generator is a Diffusion Transformer that takes multimodal features, robot state, and a noisy action chunk, and outputs clean actions. (Xiao et al., 2026) `ev:reported` p. 6 ^xiao2026learning-018
- The network is trained with a velocity-consistent loss, which the authors report yields better stability and convergence than direct action regression. (Xiao et al., 2026) `ev:asserted` p. 6 ^xiao2026learning-019
- At inference, each predicted clean action is converted to a velocity and integrated with a numerical ODE solver such as Euler. (Xiao et al., 2026) `ev:reported` p. 7 ^xiao2026learning-020
- The model is built on the StarVLA codebase, using Qwen3-VL 4B as VLM and a 16-layer DiT action expert. (Xiao et al., 2026) `ev:reported` p. 7 ^xiao2026learning-021
- Training used 4 NVIDIA H20 GPUs with batch size 16 per GPU for 30K steps, taking approximately 27 hours. (Xiao et al., 2026) `ev:reported` p. 7 ^xiao2026learning-022
- LIBERO comprises four suites, Spatial, Object, Goal, and Long, each containing 10 tasks with 500 expert demonstrations per task. (Xiao et al., 2026) `ev:reported` p. 8 ^xiao2026learning-023
- LIBERO-Plus extends LIBERO with controllable perturbations across seven dimensions, including camera viewpoints, lighting, background textures, and visual noise. (Xiao et al., 2026) `ev:reported` p. 8 ^xiao2026learning-024
- On LIBERO-Plus, all compared methods are trained only on standard LIBERO data, without fine-tuning on LIBERO-Plus. (Xiao et al., 2026) `ev:reported` p. 6 ^xiao2026learning-025
- RoboTwin 2.0 tests bi-manual manipulation, training on a mix of clean and heavily randomized scenes with random backgrounds, clutter, and table heights. (Xiao et al., 2026) `ev:reported` p. 8 ^xiao2026learning-026
- The method achieves an average success rate of 98.6% on LIBERO across the four suites with a unified model. (Xiao et al., 2026) `ev:measured` p. 8 ^xiao2026learning-027
- On LIBERO, Spatial Forcing averages 98.5 and X-VLA 98.1, close behind the 98.6 of the proposed method. (Xiao et al., 2026) `ev:measured` p. 6 ^xiao2026learning-028
- On zero-shot LIBERO-Plus, the method scores 85.7 total, compared with 78.9 for UnifoLM-VLA-0 and 69.6 for OpenVLA-OFT. (Xiao et al., 2026) `ev:measured` p. 6 ^xiao2026learning-029
- Under LIBERO-Plus camera perturbations, the method scores 89.6, against 65.1 for π0-Fast and 56.4 for OpenVLA-OFT. (Xiao et al., 2026) `ev:measured` p. 6 ^xiao2026learning-030
- Under LIBERO-Plus robot perturbations, the method scores 60.1, lower than the 69.5 reached by UnifoLM-VLA-0. (Xiao et al., 2026) `ev:measured` p. 6 ^xiao2026learning-031
- On RoboTwin 2.0, the method averages 85.18 in clean and 86.06 in randomized settings using a single model. (Xiao et al., 2026) `ev:measured` p. 6 ^xiao2026learning-032
- On RoboTwin 2.0, the X-VLA baseline averages 72.80 in clean and 72.84 in randomized settings. (Xiao et al., 2026) `ev:measured` p. 6 ^xiao2026learning-033
- In the feature interaction ablation, run without spatial features or AML, last-layer features with direct conditioning performed best. (Xiao et al., 2026) `ev:measured` p. 9 ^xiao2026learning-034
- For fusing VLM and spatial features, cross-attention scores 71.1 on LIBERO-Plus, versus 69.6 for Q-former and 68.9 for concatenation. (Xiao et al., 2026) `ev:measured` p. 7 ^xiao2026learning-035
- In the G3T ablation, G3T totals 77.9 on LIBERO-Plus, versus 77.4 for self-attention and 75.8 for concatenation. (Xiao et al., 2026) `ev:measured` p. 8 ^xiao2026learning-036
- In the component ablation, the baseline uses monocular visual features and the standard GR00T-N1 action head without added modules. (Xiao et al., 2026) `ev:reported` p. 9 ^xiao2026learning-037
- In the component ablation on LIBERO-Plus, the result rises from 66.4 for the baseline to 85.7 for the full framework. (Xiao et al., 2026) `ev:measured` p. 8 ^xiao2026learning-038
- A lightweight DPT depth head on frozen features compares monocular VGGT features with G3T-fused features under identical training settings. (Xiao et al., 2026) `ev:reported` p. 9 ^xiao2026learning-039
- In depth estimation on LIBERO, G3T features lower AbsRel from 3.5614 to 3.3353 relative to monocular VGGT features. (Xiao et al., 2026) `ev:measured` p. 8 ^xiao2026learning-040
- In the same depth test, the δ1 accuracy rises from 0.0265 with VGGT features to 0.0791 with G3T features. (Xiao et al., 2026) `ev:measured` p. 8 ^xiao2026learning-041
- According to the authors, high gate values concentrate on reliable structures such as object boundaries, distinct textures, and visible surfaces. (Xiao et al., 2026) `ev:asserted` p. 10 ^xiao2026learning-042
- From LIBERO to perturbed LIBERO-Plus, the method's average success drops by 12.9, compared with 27.5 for OpenVLA-OFT. (Xiao et al., 2026) `ev:measured` p. 8 ^xiao2026learning-043
- On LIBERO Spatial tasks the method degrades by 8.0 under perturbation, falling from 98.8 to 90.8. (Xiao et al., 2026) `ev:measured` p. 8 ^xiao2026learning-044
- AML is compared with the GR00T velocity-prediction head using a Qwen3-VL backbone, a 0.16B action expert, and no 3D modules. (Xiao et al., 2026) `ev:reported` p. 10 ^xiao2026learning-045
- With 4 denoising steps and action chunk 8, AML scores 71.0 on LIBERO-Plus versus 69.3 for GR00T. (Xiao et al., 2026) `ev:measured` p. 9 ^xiao2026learning-046
- With 2 denoising steps and action chunk 8, AML scores 69.7 total on LIBERO-Plus versus 67.2 for GR00T. (Xiao et al., 2026) `ev:measured` p. 9 ^xiao2026learning-047
- Increasing the action chunk to 30 drops GR00T to 45.7 on LIBERO-Plus, a change of -23.6. (Xiao et al., 2026) `ev:measured` p. 9 ^xiao2026learning-048
- Increasing the action chunk to 30 drops AML to 62.8 on LIBERO-Plus, a change of -8.2. (Xiao et al., 2026) `ev:measured` p. 9 ^xiao2026learning-049
- The authors interpret AML's robustness at minimal sampling steps as indicating a more structured optimization landscape. (Xiao et al., 2026) `ev:asserted` p. 12 ^xiao2026learning-050
- The real-world evaluation uses four manipulation tasks on a single Franka Emika Panda arm, with 20 demonstration episodes per task. (Xiao et al., 2026) `ev:reported` p. 12 ^xiao2026learning-051
- Each real-world model is evaluated over 10 independent trials per task, after joint fine-tuning of one unified model for 30K steps. (Xiao et al., 2026) `ev:reported` p. 12 ^xiao2026learning-052
- The method reaches real-world success rates of 70, 60, 60, and 70 on stack block, insert cube, place cylinder, and place cup. (Xiao et al., 2026) `ev:measured` p. 9 ^xiao2026learning-053
- OpenVLA-OFT reaches real-world success rates of 60, 40, 30, and 30 on the same four tasks. (Xiao et al., 2026) `ev:measured` p. 9 ^xiao2026learning-054
- Zero-shot tests change object attributes in language instructions while keeping the manipulation primitive, using color-object combinations absent from training. (Xiao et al., 2026) `ev:reported` p. 12 ^xiao2026learning-055
- In the clean zero-shot context, the method succeeds in 50, 60, 50, and 70 on the four unseen tasks. (Xiao et al., 2026) `ev:measured` p. 12 ^xiao2026learning-056
- In the cluttered zero-shot context, the method reaches 50, 40, 30, and 40, versus at most 20 for π0. (Xiao et al., 2026) `ev:measured` p. 12 ^xiao2026learning-057
- The authors state that iterative view generation during inference still prevents real-time responsiveness, despite reduced sampling steps and resolution. (Xiao et al., 2026) `ev:asserted` p. 12 ^xiao2026learning-058
- The authors suggest this latency bottleneck makes online view synthesis currently impractical for high-frequency control tasks. (Xiao et al., 2026) `ev:asserted` p. 12 ^xiao2026learning-059
- As future work, the authors plan to distill the diffusion model's geometric reasoning directly into the VLA backbone. (Xiao et al., 2026) `ev:asserted` p. 12 ^xiao2026learning-060
- Prior 3D-enhanced VLA work injects geometric features from point clouds, depth maps, or voxels, according to the related work survey. (Xiao et al., 2026) `ev:cited` p. 3 ^xiao2026learning-061

## 🎯 Contributions

## 📖 Glossary

- **VLA** — Vision-Language-Action model mapping images and language instructions to robot actions.
- **G3T** — Geometry-Guided Gated Transformer fusing VGGT features with synthesized view latents through gating.
- **Action Manifold Learning (AML)** — training the action expert to output clean action chunks, not noise or velocity.
- **a-prediction** — diffusion or flow target set to the clean action itself rather than noise or velocity.
- **VGGT** — Visual Geometry Grounded Transformer, a 3D foundation model used here as monocular geometric prior.
- **LIBERO-Plus** — LIBERO extension with seven perturbation dimensions for zero-shot robustness evaluation.
- **RoboTwin 2.0** — bi-manual manipulation benchmark with strong domain randomization, 50 tasks.
- **Action chunk** — a sequence of future actions over a horizon predicted in one pass.

## ❓ Open questions

- How much inference latency does online view synthesis add, and at which control frequency does it become prohibitive? The paper gives no timing numbers.
- Does AML's advantage over velocity prediction hold for multi-arm or whole-body action spaces, which motivate it but are not tested with a larger expert?
- Would distilling the multi-view prior into the VLA backbone keep the robustness gains seen on LIBERO-Plus?
- How sensitive are results to the quality of synthesized views, e.g. more than 2 denoising steps or more than two virtual views?
- How does the method compare with real multi-camera or RGB-D inputs on the same tasks?
- Real-world results rest on 10 trials per task; how stable are the reported gaps?

## 📝 Notes on reading

Version read: arXiv v1 (2605.11832v1, 12 May 2026), matching the identifier. The registry abstract omits LIBERO-Plus, which the PDF abstract lists among the evaluations.

Table 7 (component ablation, p. 8): the checkmark columns are garbled in extraction, so only the baseline (66.4) and full framework (85.7) rows are claimed; the intermediate values (71.1, 68.0, 70.2, 72.4, 77.9) could not be assigned to configurations reliably. The text (p. 9) says each addition gives a consistent gain, but the listed values are not monotonic in the printed order.

Table 10 (AML efficiency, p. 9): the denoising-step and chunk columns are partly garbled; the row assignment used (4 steps/chunk 8, 2/8, 10/8, 4/10, 4/30) was inferred from the layout.

Table 3 lists only a subset of the 50 RoboTwin 2.0 tasks; the averages are stated for all tasks. The text (p. 9) says over 80% success on RoboTwin 2.0, while Table 3 gives 85.18 and 86.06. Table 9's perturbed column reuses LIBERO-Plus results under a per-suite split.

Fig. 1(d), Fig. 5 (depth visualization) and Fig. 6 (gate maps) are qualitative and only described. Absolute depth metrics in Table 8 are poor for both methods (δ1 below 0.1), so the probe mostly shows relative improvement.

The model is fine-tuned from reference [89] (ABot-M0, overlapping authors), whose title already names action manifold learning; the paper does not discuss how AML differs from that prior work.

## Suggested new concepts

- Action manifold hypothesis — the claim that valid robot actions lie on a low-dimensional manifold, motivating clean-action prediction.
- Latent novel-view synthesis for VLA — using image-editing diffusion to produce virtual views as a geometric prior from one camera.
- Clean-target (x/a-prediction) flow matching — recurring design choice for generative policies versus noise or velocity targets.
- LIBERO-Plus — robustness benchmark increasingly used to compare VLA policies under perturbation.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** Trabajo de 2026 que hace que una VLA prediga acciones directamente sobre la variedad de acciones válidas, la hipótesis de la variedad aplicada a la cabeza de acción.
