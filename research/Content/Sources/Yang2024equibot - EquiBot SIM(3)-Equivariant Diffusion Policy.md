---
aliases: []
type: "source"
title: "EquiBot: SIM(3)-Equivariant Diffusion Policy"
citekey: "Yang2024equibot"
doi: "10.48550/arXiv.2407.01479"
arxiv: "2407.01479"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2407.01479"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Jingyun Yang", "Zi-ang Cao", "Congyue Deng", "Rika Antonova", "Shuran Song", "Jeannette Bohg"]
sha256: ["00b111de1a9cb716d030567bf3607e43e294c42772231183990f64bca4daadd4"]
pdf: "Content/Papers/Yang2024equibot.pdf"
topics: ["[[Optimización y algoritmos]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 57
---

📄 PDF: [[Yang2024equibot.pdf]]

> [!abstract] One-sentence summary
> EquiBot makes every step of a point-cloud diffusion policy SIM(3)-equivariant, so policies learned from about 5 minutes of human video generalize to unseen object poses, scales and scenes where vanilla and augmented Diffusion Policy fail.

## Abstract

Building effective imitation learning methods that enable robots to learn from limited data and still generalize across diverse real-world environments is a long-standing problem in robot learning. We propose Equibot, a robust, data-efficient, and generalizable approach for robot manipulation task learning. Our approach combines SIM(3)-equivariant neural network architectures with diffusion models. This ensures that our learned policies are invariant to changes in scale, rotation, and translation, enhancing their applicability to unseen environments while retaining the benefits of diffusion-based policy learning such as multi-modality and robustness. We show on a suite of 6 simulation tasks that our proposed method reduces the data requirements and improves generalization to novel scenarios. In the real world, with 10 variations of 6 mobile manipulation tasks, we show that our method can easily generalize to novel objects and scenes after learning from just 5 minutes of human demonstrations in each task. (arXiv)

## 🧠 Key ideas (atomic)

- Existing visuomotor policies learned by imitation are effective in controlled settings but require substantial data and generalize poorly to unseen scenarios. (Yang et al., 2024) `ev:cited` p. 1 ^yang2024equibot-001
- EquiBot is an equivariant policy learning architecture that builds on diffusion models, specifically the CNN-based [[Diffusion Policy]] variant, as its starting point. (Yang et al., 2024) `ev:reported` p. 3 ^yang2024equibot-002
- At test time the policy takes single-view object-centric point clouds and robot proprioception as input and outputs end-effector action sequences. (Yang et al., 2024) `ev:reported` p. 2 ^yang2024equibot-003
- The output actions consist of 6D velocity commands and gripper open-close signals for the robot end-effector. (Yang et al., 2024) `ev:reported` p. 2 ^yang2024equibot-004
- Prior data augmentation approaches increase training time significantly and do not guarantee generalization to unseen appearances, scales and poses, according to the authors. (Yang et al., 2024) `ev:asserted` p. 2 ^yang2024equibot-005
- The authors' earlier EquivAct method cannot handle [[Multimodal action distributions|multi-modal training data]] because of its deterministic architecture. (Yang et al., 2024) `ev:asserted` p. 2 ^yang2024equibot-006
- Diffusion-EDFs produces target end-effector poses and can only solve pick-and-place tasks, according to the related work review. (Yang et al., 2024) `ev:cited` p. 2 ^yang2024equibot-007
- EquiDiff can only handle SO(2)-equivariance with simple 2D trajectories, while EDGI assumes ground-truth scene states as input. (Yang et al., 2024) `ev:cited` p. 2 ^yang2024equibot-008
- By building an equivariant noise prediction network, each diffusion step is made equivariant by construction. (Yang et al., 2024) `ev:asserted` p. 3 ^yang2024equibot-009
- Proposition 1 states that an SO(3)-equivariant prior with SO(3)-equivariant Markov transitions yields an SO(3)-equivariant final density. (Yang et al., 2024) `ev:computed` p. 4 ^yang2024equibot-010
- Equivariance to translation and scaling is achieved through canonicalization before the diffusion process rather than inside the diffusion steps. (Yang et al., 2024) `ev:reported` p. 4 ^yang2024equibot-011
- The SIM(3)-equivariant point cloud encoder outputs a centroid vector and a scalar object scale used to make later inputs position- and scale-invariant. (Yang et al., 2024) `ev:reported` p. 4 ^yang2024equibot-012
- Unlike EquivAct, the encoder is not pre-trained on simulation data but is learned from scratch with the policy. (Yang et al., 2024) `ev:reported` p. 4 ^yang2024equibot-013
- Learning the encoder from scratch removes the need to build task-specific simulation environments and collect custom pre-training data. (Yang et al., 2024) `ev:asserted` p. 4 ^yang2024equibot-014
- The 1D convolution layers become SO(3)-equivariant by treating vector channels of the layer inputs as batch dimensions. (Yang et al., 2024) `ev:reported` p. 5 ^yang2024equibot-015
- FiLM layers are made SO(3)-equivariant by replacing their vanilla linear layers with [[Vector Neurons|vector neuron layers]]. (Yang et al., 2024) `ev:reported` p. 5 ^yang2024equibot-016
- The upsampling layers of the conditional U-net are left unmodified because they are naturally SO(3)-equivariant. (Yang et al., 2024) `ev:reported` p. 5 ^yang2024equibot-017
- Simulation baselines are vanilla Diffusion Policy with a PointNet++ encoder, Diffusion Policy with augmentations, and a re-implementation of EquivAct without pre-training. (Yang et al., 2024) `ev:reported` p. 5 ^yang2024equibot-018
- The DP+Aug baseline rotates observations around the z-axis, scales them uniformly within 0.5 × −1.5×, and adds Gaussian offsets. (Yang et al., 2024) `ev:reported` p. 6 ^yang2024equibot-019
- The three simulated mobile manipulation tasks use two robots on deformable and articulated objects, trained with 50 synthetically generated demonstrations. (Yang et al., 2024) `ev:reported` p. 6 ^yang2024equibot-020
- Push T policies are trained on the same 200 demonstrations as the original Diffusion Policy work. (Yang et al., 2024) `ev:reported` p. 6 ^yang2024equibot-021
- All simulation methods train for 2,000 epochs on 3 seeds, and each bar reports 150 trials of evaluation. (Yang et al., 2024) `ev:reported` p. 6 ^yang2024equibot-022
- Out-of-distribution setups randomize rotation about the z-axis, scale the scene 1× to 2×, add position randomization, or combine all three. (Yang et al., 2024) `ev:reported` p. 6 ^yang2024equibot-023
- The DP baseline performs very well in the Original setup but drops significantly in any of the OOD setups. (Yang et al., 2024) `ev:measured` p. 6 ^yang2024equibot-024
- DP+Aug performs especially well under OOD (R) but suffers significant performance drops under OOD (P) and OOD (R+S+P). (Yang et al., 2024) `ev:measured` p. 7 ^yang2024equibot-025
- The EquivAct baseline performs very well in Cloth Folding but shows subpar performance in Object Covering and Box Closing. (Yang et al., 2024) `ev:measured` p. 7 ^yang2024equibot-026
- EquivAct cannot perform well on Push T, which the authors attribute to its deterministic behavior cloning architecture handling [[Multimodal action distributions|multi-modal data]] poorly. (Yang et al., 2024) `ev:measured` p. 7 ^yang2024equibot-027
- EquiBot performs stably in all four simulated tasks and suffers the least performance drop compared to all baselines. (Yang et al., 2024) `ev:measured` p. 7 ^yang2024equibot-028
- On Robomimic Can and Square, DP performance drops dramatically from 100 to 25 demos, while EquiBot retains relatively higher performance. (Yang et al., 2024) `ev:measured` p. 7 ^yang2024equibot-029
- The authors attribute EquiBot's data efficiency to [[Equivariant neural network|equivariance]] letting it cope with initial object poses not covered by small training sets. (Yang et al., 2024) `ev:asserted` p. 7 ^yang2024equibot-030
- Real robot tasks are learned from 15 human demonstration videos per task, recorded with a ZED 2 stereo camera at 15 Hz. (Yang et al., 2024) `ev:reported` p. 7 ^yang2024equibot-031
- Human hand poses and object point clouds are parsed with off-the-shelf hand detection and segmentation models, then subsampled to 3 Hz. (Yang et al., 2024) `ev:reported` p. 7 ^yang2024equibot-032
- Real experiments use holonomic mobile bases with Kinova Gen3 7 DoF arms, and all methods train for 1,000 epochs. (Yang et al., 2024) `ev:reported` p. 7 ^yang2024equibot-033
- In real Push Chair, EquiBot succeeded 8/10 with a long desk and 10/10 with a round table, versus 0/10 for DP. (Yang et al., 2024) `ev:measured` p. 8 ^yang2024equibot-034
- In real in-distribution Laundry Door Closing, EquiBot succeeded 8/10, compared with 3/10 for DP and 2/10 for DP+Aug. (Yang et al., 2024) `ev:measured` p. 8 ^yang2024equibot-035
- On Luggage Closing with a larger unseen luggage, EquiBot succeeded 6/10 while DP scored 0/10 and DP+Aug 2/10. (Yang et al., 2024) `ev:measured` p. 8 ^yang2024equibot-036
- In Luggage Packing with novel items and translated, rotated layouts, EquiBot scored between 3/10 and 8/10 while DP scored 0/10. (Yang et al., 2024) `ev:measured` p. 8 ^yang2024equibot-037
- EquiBot succeeded 6/10 on Bimanual Folding with a long bath towel and 8/10 on Bimanual Make Bed, where DP scored 0/10. (Yang et al., 2024) `ev:measured` p. 8 ^yang2024equibot-038
- EquiBot does not handle nonlinear changes in object shapes or dynamics by construction, as the authors state in their limitations. (Yang et al., 2024) `ev:asserted` p. 8 ^yang2024equibot-039
- The method does not handle variations in relative positioning of objects when multiple objects are present in the scene. (Yang et al., 2024) `ev:asserted` p. 8 ^yang2024equibot-040
- The method might fail when the scene is partially occluded or when the camera angle changes dramatically. (Yang et al., 2024) `ev:asserted` p. 8 ^yang2024equibot-041
- A SO(3)-equivariant variant using the DP3 encoder showed slightly lower but comparable performance to EquiBot in Cloth Folding. (Yang et al., 2024) `ev:measured` p. 13 ^yang2024equibot-042
- EquiBot significantly outperforms a naive EquivAct extension with a diffusion head for all hyperparameter variations tried in OOD setups. (Yang et al., 2024) `ev:measured` p. 13 ^yang2024equibot-043
- Removing any of rotation, translation or scale equivariance causes performance drops when evaluation is out-of-distribution for the [[Equivariant neural network|removed equivariance]]. (Yang et al., 2024) `ev:measured` p. 14 ^yang2024equibot-044
- On the Push T task, EquiBot achieves more stable in-distribution training performance across checkpoints than the prior EquivAct method. (Yang et al., 2024) `ev:measured` p. 14 ^yang2024equibot-045
- In most real packing tasks, the main failure case was the end-effector opening too early. (Yang et al., 2024) `ev:measured` p. 14 ^yang2024equibot-046
- In Push Chair, Laundry Door Closing and Bimanual Folding, most failures came from incomplete motions or mistimed gripper actions. (Yang et al., 2024) `ev:measured` p. 14 ^yang2024equibot-047
- With 10 laundry door demos, EquiBot had a total missing angle of 17.46◦ versus 140.42◦ for DP. (Yang et al., 2024) `ev:measured` p. 15 ^yang2024equibot-048
- With 10 laundry door demos, DP had 2/10 collision or safety issues, while EquiBot had 0/10 at every demo count. (Yang et al., 2024) `ev:measured` p. 15 ^yang2024equibot-049
- Laundry door success rose from 8/10 to 10/10 for EquiBot and from 3/10 to 7/10 for DP between 10 and 50 demos. (Yang et al., 2024) `ev:measured` p. 15 ^yang2024equibot-050
- The policy uses an observation horizon of 2 steps, a prediction horizon of 16 steps, and an action horizon of 8 steps. (Yang et al., 2024) `ev:reported` p. 18 ^yang2024equibot-051
- Simulation uses a DDPM scheduler with 100 denoising steps, while real robots use DDIM with 8 steps for inference speed. (Yang et al., 2024) `ev:reported` p. 18 ^yang2024equibot-052
- Real robot experiments and simulated mobile manipulation tasks use 1024-point point clouds, which the authors found sufficient. (Yang et al., 2024) `ev:reported` p. 18 ^yang2024equibot-053
- All 3D-vector inputs, including observations and actions, are normalized together because of the SIM(3)-equivariance assumptions. (Yang et al., 2024) `ev:reported` p. 18 ^yang2024equibot-054
- The authors found the alignment module crucial because the hand detection model outputs poses in a different frame from the point cloud. (Yang et al., 2024) `ev:asserted` p. 19 ^yang2024equibot-055
- The authors observed generalization to geometric variations beyond SIM(3), such as non-uniform scaling, although this is not enabled by construction. (Yang et al., 2024) `ev:asserted` p. 21 ^yang2024equibot-056
- The authors hypothesize that equivariance in all policy layers may be conducive to learning a more general feature representation. (Yang et al., 2024) `ev:asserted` p. 21 ^yang2024equibot-057

## 🎯 Contributions

## 📖 Glossary

- **SIM(3)** — Group of 3D similarity transforms: rotation, translation and uniform scaling.
- **Equivariance** — Property that transforming the input transforms the output in the same way.
- **Diffusion Policy** — Visuomotor policy that generates action sequences by iterative denoising from Gaussian noise.
- **Vector neurons** — Network layers acting on 3D vector features that are SO(3)-equivariant by construction.
- **FiLM layer** — Feature-wise affine modulation of activations with parameters predicted from conditioning input.
- **Canonicalization** — Removing centroid and scale from inputs so later layers see position- and scale-invariant values.
- **Action horizon** — Number of predicted actions actually executed before re-planning.
- **EquivAct** — Authors' earlier deterministic SIM(3)-equivariant visuomotor policy with a pre-trained encoder.

## ❓ Open questions

- How can the policy handle nonlinear changes in object shape or dynamics that SIM(3) equivariance does not cover?
- Can per-object modeling let the method cope with changing relative positions between multiple objects?
- Would 3D representations robust to incomplete point clouds fix failures under occlusion or camera angle changes?
- Why does the policy generalize to non-uniform scaling, and what do its intermediate equivariant features encode?
- How does the approach extend to multi-task learning?
- How sensitive is real-world performance to segmentation errors, as seen for the folded comforter?

## 📝 Notes on reading

- Read version: arXiv 2407.01479v2 (29 Oct 2024), marked as the CoRL 2024 paper; the packet lists the venue as arXiv preprint.
- Table 1 (p. 8) is flattened in extraction; its second block is headed "Luggage Closing" but the object variations (T-shirt, Towel Roll, Cap, Shorts) match Luggage Packing, and DP+Aug values appear only for the first block. Column assignments were read with Figure 11 (p. 15) pie counts as a cross-check.
- Main text states 15 human demos per real task (p. 7), while Table 2 (p. 15) evaluates laundry door closing with 10, 25 and 50 demos; the Table 2 EquiBot success at 10 demos (8/10) matches Table 1.
- Figures 4, 5, 7, 8, 9 and 10 are bar/line plots whose values are not in the extracted text; only the authors' prose descriptions were claimed.
- Section 3.1 lists proprioception components with inconsistent superscripts (S(v) vs S(d)); the action definition reuses S(s) for scalars.
- The abstract says 6 simulation tasks: four in Section 4.1.1 (Cloth Folding, Object Covering, Box Closing, Push T) plus Robomimic Can and Square in Section 4.1.2.

## Suggested new concepts

- SIM(3)-equivariant policy — recurring design principle for generalizing manipulation policies across pose and scale.
- Equivariant diffusion — framework for making generative denoising processes respect symmetry groups.
- Learning from human video demonstrations — pipeline turning hand-tracked videos into robot training data.
- Diffusion Policy — base architecture many visuomotor methods extend.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Equivariancia a rotación/traslación/escala (C.6).
- **[[03_aplicaciones_vision_por_computador]]** — Política equivariante a rotación, traslación y escala
