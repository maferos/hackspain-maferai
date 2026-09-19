---
aliases: []
type: "source"
title: "Equivariant Diffusion Policy"
citekey: "Wang2024equivariant"
doi: "10.48550/arXiv.2407.01812"
arxiv: "2407.01812"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2407.01812"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Dian Wang", "Stephen Hart", "David Surovik", "Tarik Kelestemur", "Haojie Huang", "Haibo Zhao", "Mark Yeatman", "Jiuguang Wang", "Robin Walters", "Robert Platt"]
sha256: ["3e4ed85a4bae7b5322f5e2d8fb00461ee436a31a574d030c68d4aed3c9593c1f"]
pdf: "Content/Papers/Wang2024equivariant.pdf"
topics: ["[[Optimización y algoritmos]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Wang2024equivariant.pdf]]

> [!abstract] One-sentence summary
> Equivariant Diffusion Policy builds SO(2) rotational symmetry into the denoising network of a 6-DoF diffusion policy, improving sample efficiency over Diffusion Policy in MimicGen simulation and on a real Franka robot trained from 20 to 60 demonstrations.

## Abstract

Recent work has shown diffusion models are an effective approach to learning the multimodal distributions arising from demonstration data in behavior cloning. However, a drawback of this approach is the need to learn a denoising function, which is significantly more complex than learning an explicit policy. In this work, we propose Equivariant Diffusion Policy, a novel diffusion policy learning method that leverages domain symmetries to obtain better sample efficiency and generalization in the denoising function. We theoretically analyze the $\mathrm{SO}(2)$ symmetry of full 6-DoF control and characterize when a diffusion model is $\mathrm{SO}(2)$-equivariant. We furthermore evaluate the method empirically on a set of 12 simulation tasks in MimicGen, and show that it obtains a success rate that is, on average, 21.9% higher than the baseline Diffusion Policy. We also evaluate the method on a real-world system to show that effective policies can be learned with relatively few training samples, whereas the baseline Diffusion Policy cannot. (arXiv)

## 🧠 Key ideas (atomic)

- A key drawback of Diffusion Policy is that its denoising function is more complex than a standard policy function. (Wang et al., 2024) `ev:asserted` p. 1 ^wang2024equivariant-001
- The authors embed task symmetry into the diffusion process using equivariant neural models as an inductive bias to make the denoising function easier to learn. (Wang et al., 2024) `ev:asserted` p. 1 ^wang2024equivariant-002
- The authors state their paper is the first to study equivariant diffusion models in the context of visuomotor policy learning. (Wang et al., 2024) `ev:asserted` p. 1 ^wang2024equivariant-003
- In simulation on 12 MimicGen tasks with 100 demos, the method outperformed baseline Diffusion Policy by an average success rate of 21.9%. (Wang et al., 2024) `ev:measured` p. 2 ^wang2024equivariant-004
- The authors theoretically demonstrate SO(2)-equivariance for 6-DoF manipulation control, which prior methods leveraged in a less expressive SE(2) action space. (Wang et al., 2024) `ev:asserted` p. 2 ^wang2024equivariant-005
- Prior molecular-generation work showed that leveraging SO(3) domain symmetries in the diffusion process dramatically improves sample efficiency. (Wang et al., 2024) `ev:cited` p. 2 ^wang2024equivariant-006
- EDGI extends Diffuser to equivariant diffusion planning with improved performance but relies on the ground-truth state as its input. (Wang et al., 2024) `ev:cited` p. 2 ^wang2024equivariant-007
- Ryu et al. proposed bi-equivariant diffusion models for visual robotic manipulation, but those models are limited to open-loop settings. (Wang et al., 2024) `ev:cited` p. 2 ^wang2024equivariant-008
- Prior equivariant manipulation work considered either SE(3) open-loop or SE(2) closed-loop action spaces, whereas this paper studies SE(3) closed-loop actions. (Wang et al., 2024) `ev:asserted` p. 2 ^wang2024equivariant-009
- Implicit policies built on energy-based models are challenging to train due to the necessity of a substantial volume of negative samples. (Wang et al., 2024) `ev:cited` p. 2 ^wang2024equivariant-010
- Actions specify a desired SE(3) gripper pose plus an open-width command, in either absolute (position) or relative (velocity) control. (Wang et al., 2024) `ev:reported` p. 3 ^wang2024equivariant-011
- The SE(3) pose is vectorized for additive noising during diffusion, then the noise-free action vector is orthogonalized after denoising. (Wang et al., 2024) `ev:reported` p. 3 ^wang2024equivariant-012
- Diffusion Policy by Chi et al. learns a noise prediction network trained with a squared-error loss against the added Gaussian noise. (Wang et al., 2024) `ev:cited` p. 3 ^wang2024equivariant-013
- Proposition 1 states the noise prediction function is SO(2)-equivariant whenever the expert policy being modeled is SO(2)-equivariant. (Wang et al., 2024) `ev:computed` p. 3 ^wang2024equivariant-014
- The authors argue this result implies equivariant neural networks have the correct inductive bias to model the noise prediction function. (Wang et al., 2024) `ev:asserted` p. 3 ^wang2024equivariant-015
- Proposition 2 shows that irreducible SO(2) representations exist describing how rotations about the world z-axis act on SE(3) gripper actions. (Wang et al., 2024) `ev:computed` p. 4 ^wang2024equivariant-016
- In absolute control, the simplified action vector consists of a 6D rotation, a three-element translation, then the gripper open width. (Wang et al., 2024) `ev:computed` p. 4 ^wang2024equivariant-017
- In relative control, a change-of-basis matrix decomposes the conjugation action into six trivial, four frequency-one plus one frequency-two irreducible representations. (Wang et al., 2024) `ev:computed` p. 4 ^wang2024equivariant-018
- The network comprises equivariant encoders, a denoising stage, then an equivariant decoder, all implemented with the escnn library. (Wang et al., 2024) `ev:reported` p. 5 ^wang2024equivariant-019
- Encoders produce embeddings in the regular representation of a discrete rotation subgroup, with one feature vector per group element. (Wang et al., 2024) `ev:reported` p. 5 ^wang2024equivariant-020
- A shared 1D Temporal U-Net processes each group element's embedding pair, so the output is an equivariant noise embedding in the regular representation. (Wang et al., 2024) `ev:reported` p. 5 ^wang2024equivariant-021
- Equivariant layers are implemented in the group C8, with an equivariant ResNet-18 encoding the agent-view image in the image version. (Wang et al., 2024) `ev:reported` p. 15 ^wang2024equivariant-022
- The voxel version replaces the equivariant ResNet with an 8-layer 3D equivariant convolutional encoder over the voxel grid. (Wang et al., 2024) `ev:reported` p. 16 ^wang2024equivariant-023
- The method is evaluated with either image or voxel input on 12 manipulation tasks from the MimicGen benchmark. (Wang et al., 2024) `ev:reported` p. 5 ^wang2024equivariant-024
- In the image version, image rotation mismatches ground-truth state rotation since the agent-view camera is not orthogonally top-down. (Wang et al., 2024) `ev:asserted` p. 5 ^wang2024equivariant-025
- The voxel version eliminates this symmetry mismatch as the rotation of the voxel grid aligns with the ground-truth state rotation. (Wang et al., 2024) `ev:asserted` p. 5 ^wang2024equivariant-026
- The authors add a rotation augmentation to the voxel version to better leverage equivariance, following their Section 4 analysis. (Wang et al., 2024) `ev:reported` p. 5 ^wang2024equivariant-027
- Simulation baselines include Diffusion Policy with a 1D Temporal UNet, Diffusion Policy with a transformer, DP3, plus ACT. (Wang et al., 2024) `ev:reported` p. 5 ^wang2024equivariant-028
- The UNet Diffusion Policy baseline shares the same UNet architecture as the method but does not have any equivariant structure. (Wang et al., 2024) `ev:reported` p. 5 ^wang2024equivariant-029
- Voxel inputs are constructed from four cameras, whereas the image-based methods directly use RGB images from two cameras. (Wang et al., 2024) `ev:reported` p. 6 ^wang2024equivariant-030
- Simulation results report the maximum task success rate among 50 evaluations throughout training, averaged over three seeds. (Wang et al., 2024) `ev:reported` p. 6 ^wang2024equivariant-031
- With absolute pose control, the voxel-input method outperformed the baselines in 11 out of the 12 environments, Hammer Cleanup D1 excepted. (Wang et al., 2024) `ev:measured` p. 6 ^wang2024equivariant-032
- With RGB inputs, the method outperformed all RGB baselines in every simulated environment except Kitchen D1. (Wang et al., 2024) `ev:measured` p. 6 ^wang2024equivariant-033
- In relative pose control, the method with RGB input was only marginally better than the baselines in simulation. (Wang et al., 2024) `ev:measured` p. 6 ^wang2024equivariant-034
- Averaged over 12 tasks with 100 demos, the voxel absolute-control method reached a success rate of 63.9 versus 42.0 for DiffPo-C. (Wang et al., 2024) `ev:measured` p. 6 ^wang2024equivariant-035
- Trained with 200 demos, the voxel absolute-control method outperformed all baselines trained with 1000 demos when averaged over all environments. (Wang et al., 2024) `ev:measured` p. 7 ^wang2024equivariant-036
- With 1000 demos in absolute control, the RGB variant averaged 79.7, exceeding the voxel variant's average of 77.9. (Wang et al., 2024) `ev:measured` p. 6 ^wang2024equivariant-037
- In relative control with 1000 demos, the voxel variant averaged 70.2, versus 70.3 for the BC RNN baseline. (Wang et al., 2024) `ev:measured` p. 6 ^wang2024equivariant-038
- In the ablation, the authors find the equivariant structure is the more important factor compared with the voxel input. (Wang et al., 2024) `ev:measured` p. 7 ^wang2024equivariant-039
- Removing the equivariant structure lowered the 100-demo average success by 17.6, whereas removing the voxel input lowered it by 10.3. (Wang et al., 2024) `ev:measured` p. 19 ^wang2024equivariant-040
- The authors hypothesize that equivariance should be more useful when there is greater variance in initial object poses. (Wang et al., 2024) `ev:asserted` p. 7 ^wang2024equivariant-041
- Tasks were qualitatively grouped into high, intermediate or low equivariance levels by the randomness of their initial object poses. (Wang et al., 2024) `ev:reported` p. 7 ^wang2024equivariant-042
- High-equivariance tasks generally benefit more from injecting symmetry into the network architecture than the other task groups. (Wang et al., 2024) `ev:measured` p. 7 ^wang2024equivariant-043
- The authors interpret strong results on intermediate and low-equivariance tasks as indicating that symmetry helps even when tasks are partially symmetric. (Wang et al., 2024) `ev:asserted` p. 7 ^wang2024equivariant-044
- The real system uses a Franka Emika arm fitted with fin-ray fingers plus three Intel Realsense D455 cameras. (Wang et al., 2024) `ev:reported` p. 7 ^wang2024equivariant-045
- Real demonstrations were gathered by an operator with a 6DoF mouse, with observations recorded at 5Hz. (Wang et al., 2024) `ev:reported` p. 7 ^wang2024equivariant-046
- The real-robot experiments use DDIM to reduce the number of denoising steps to 16, following prior work. (Wang et al., 2024) `ev:reported` p. 8 ^wang2024equivariant-047
- The real-robot baseline uses the same voxel input with a non-equivariant 3D convolutional encoder of approximately equal parameter count. (Wang et al., 2024) `ev:reported` p. 8 ^wang2024equivariant-048
- Across six real-world tasks, the method succeeded in 80% to 95% of 20 trials using 20 to 60 demonstrations. (Wang et al., 2024) `ev:measured` p. 8 ^wang2024equivariant-049
- The method achieved an 80% success rate on the long-horizon real-world Bagel Baking task with 58 demonstrations. (Wang et al., 2024) `ev:measured` p. 8 ^wang2024equivariant-050
- In real-world Bagel Baking, all failures of the method were attributed by the authors to the joint limits of the robot. (Wang et al., 2024) `ev:measured` p. 8 ^wang2024equivariant-051
- The voxel Diffusion Policy baseline scored at most 60% on the six real tasks, with 0% on Letter Alignment. (Wang et al., 2024) `ev:measured` p. 8 ^wang2024equivariant-052
- The authors state a limitation that symmetry mismatch in the vision system leads to partial utilization of the power of equivariance. (Wang et al., 2024) `ev:asserted` p. 8 ^wang2024equivariant-053
- Even with voxel input, the arm occasionally appearing in the voxel grid could break symmetry, as could camera noise. (Wang et al., 2024) `ev:asserted` p. 8 ^wang2024equivariant-054
- Incorrect equivariance, as shown in prior work, may harm performance when the model's symmetry conflicts with the demonstration. (Wang et al., 2024) `ev:cited` p. 8 ^wang2024equivariant-055
- The authors note their Section 4.2 theory could apply to other policy learning pipelines, but this is not demonstrated. (Wang et al., 2024) `ev:asserted` p. 8 ^wang2024equivariant-056
- Extending the method to navigation, locomotion or mobile manipulation is named by the authors as a key future direction. (Wang et al., 2024) `ev:asserted` p. 8 ^wang2024equivariant-057
- Simulation training uses DDPM with 100 denoising steps for both training and evaluation, with a batch size of 128. (Wang et al., 2024) `ev:reported` p. 17 ^wang2024equivariant-058
- The denoising process outputs a sequence of 16 action steps, of which eight steps are executed during evaluation. (Wang et al., 2024) `ev:reported` p. 17 ^wang2024equivariant-059
- Coffee Preparation D1 has the largest maximum out-of-plane rotation in its demonstrations among the simulated tasks, at 59.0 degrees. (Wang et al., 2024) `ev:measured` p. 17 ^wang2024equivariant-060
- With 100 demos, random-rotation augmentation on an unconstrained CNN averaged 53.3 versus 63.9 for the equivariant network with voxels. (Wang et al., 2024) `ev:measured` p. 20 ^wang2024equivariant-061
- CNN with augmentation occasionally outperformed equivariant networks on simpler tasks like Stack, but performed poorly on more challenging tasks. (Wang et al., 2024) `ev:measured` p. 19 ^wang2024equivariant-062
- With 200 demos, an SE(2) action variant scored 0.0 on Coffee Preparation D1, versus 85.3 for the SE(3) version. (Wang et al., 2024) `ev:measured` p. 20 ^wang2024equivariant-063
- On Threading D2, the SE(2) action variant reached 12.7 versus 40.0 for the SE(3) action version. (Wang et al., 2024) `ev:measured` p. 20 ^wang2024equivariant-064
- The authors attribute the Threading gap to the SE(3) agent's ability to wiggle out-of-plane rotation for precise tool insertion. (Wang et al., 2024) `ev:asserted` p. 20 ^wang2024equivariant-065
- On four Robomimic tasks with 100 demos, the method achieved similar or slightly better performance than the original Diffusion Policy. (Wang et al., 2024) `ev:measured` p. 20 ^wang2024equivariant-066
- Averaged over the Robomimic settings, Equivariant Diffusion Policy scored 90.4 versus 87.9 for the original Diffusion Policy. (Wang et al., 2024) `ev:measured` p. 21 ^wang2024equivariant-067
- The authors attribute the smaller Robomimic gains to minimal initial-state randomness, making the symmetry of their method less advantageous. (Wang et al., 2024) `ev:asserted` p. 20 ^wang2024equivariant-068
- Trained on three oven poses in Bagel Baking, the policy zero-shot generalized to unseen rotations, except a bottom-right corner pose. (Wang et al., 2024) `ev:measured` p. 21 ^wang2024equivariant-069

## 🎯 Contributions

## 📖 Glossary

- **Diffusion Policy** — Behavior cloning policy that generates actions by iteratively denoising random noise conditioned on observations.
- **Equivariance** — Property where transforming a function's input transforms its output by the corresponding group action.
- **SO(2)** — Group of planar rotations, here rotations about the world gravity (z) axis.
- **Cyclic group C8** — Discrete subgroup of SO(2) containing eight rotations, used to build equivariant layers.
- **Regular representation** — Group action on features that cyclically permutes one feature vector per group element.
- **Irreducible representation** — Smallest rotation-block representation; frequency ω rotates a 2D vector by ω times the angle.
- **Noise prediction function** — Network predicting the Gaussian noise added to an action at a given denoising step.
- **Absolute pose control** — Action gives the target gripper pose directly in the world frame (position control).
- **Relative pose control** — Action gives a pose change applied to the current gripper pose (velocity control).
- **6D rotation representation** — Rotation encoded by two columns of the rotation matrix, avoiding discontinuities.
- **MimicGen** — Simulation benchmark and data generation system for robot manipulation from human demonstrations.
- **Out-of-plane rotation** — Gripper rotation component not about the vertical axis; beyond SE(2) actions.

## ❓ Open questions

- Would an equivariant version of BC RNN, which performed well in relative pose control, match or beat Equivariant Diffusion Policy?
- Can a vision system free of symmetry corruption (arm in the voxel grid, camera noise, non-top-down views) recover the full benefit of equivariance?
- How much does incorrect equivariance hurt when demonstrations are not rotationally symmetric, and can it be detected or relaxed automatically?
- Does the SO(2) action-representation theory transfer to navigation, locomotion or mobile manipulation?
- Why does the RGB variant slightly beat the voxel variant at 1000 demos in absolute control, and does the equivariance gain vanish with abundant data?
- Why does the equivariant model lose to baselines on some tasks at 1000 demos (e.g. Hammer Cleanup D1, Kitchen D1)?

## 📝 Notes on reading

- Version read: arXiv 2407.01812v3 (15 Oct 2024), the CoRL 2024 camera-ready; the packet identifier is the same arXiv record.
- Figures 1, 2, 3, 5, 7 and 11 could only be described from captions: Fig. 1 shows rotating state and noisy trajectory yields a rotated denoised trajectory; Fig. 2 shows the equivariant gradient field of the denoising function; Fig. 3 shows encoder, per-group-element U-Net denoiser and decoder; Fig. 5b shows per-task improvement grouped by equivariance level (values not extractable).
- The change-of-basis matrices and 16×16 / 9×9 representation matrices in Appendices B and C (Eqs. 7, 8, 13, 14) are garbled in extraction and were not claimed.
- Table 1 bold markers (best result, difference above 10%) and blue/red colouring are lost in extraction; per-cell Table 1 and Table 6 values were claimed only via the Table 2 averages.
- Real-robot action recording device is written as '3DCon-nexion' across a line break; the claim omits the brand.
- Inconsistency: Appendix L says 'Figure 6 shows the five tasks' while Figure 6 and Table 3 list six real-world tasks.
- Inconsistency: Section 5.1 says the voxel method outperforms baselines in 11 of 12 environments, but Table 1 also shows it trailing the best baseline at 1000 demos in several tasks; the claim concerns the overall best result per task as the authors frame it.
- The Robomimic 'Average' column in Table 11 averages seven PH/MH settings; its standard errors (±2.3, ±3.2) overlap considerably.

## Suggested new concepts

- Equivariant diffusion policy — a distinct policy class combining equivariant networks with diffusion-based behavior cloning.
- SO(2)-equivariance in 6-DoF action spaces — the representation-theoretic treatment of how planar rotations act on SE(3) gripper actions, reusable beyond diffusion.
- Symmetry mismatch in perception — a recurring limitation where camera viewpoint or clutter breaks the symmetry an equivariant model assumes.
- Equivariance via data augmentation vs. equivariant architectures — a design trade-off the paper measures directly.
- Task equivariance level — the idea of grading tasks by initial-pose randomness to predict how much symmetry priors help.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Difusión con denoiser equivariante (C.6).
- **[[03_aplicaciones_vision_por_computador]]** — Diffusion Policy con *denoiser* equivariante
