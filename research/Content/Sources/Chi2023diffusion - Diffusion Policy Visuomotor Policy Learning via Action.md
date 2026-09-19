---
aliases: []
type: "source"
title: "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion"
citekey: "Chi2023diffusion"
doi: "10.48550/arXiv.2303.04137"
arxiv: "2303.04137"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2303.04137"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Cheng Chi", "Zhenjia Xu", "Siyuan Feng", "Eric Cousineau", "Yilun Du", "Benjamin Burchfiel", "Russ Tedrake", "Shuran Song"]
sha256: ["b65c474b696a4802d8f1457d86b637ce2c5521412570d3aa928cd54563babc8f"]
pdf: "Content/Papers/Chi2023diffusion.pdf"
topics: ["[[Optimización y algoritmos]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 70
---

📄 PDF: [[Chi2023diffusion.pdf]]

> [!abstract] One-sentence summary
> Diffusion Policy casts a visuomotor robot policy as a conditional denoising diffusion process over action sequences, outperforming prior behavior-cloning methods across 15 simulated and real-world manipulation tasks.

## Abstract

This paper introduces Diffusion Policy, a new way of generating robot behavior by representing a robot's visuomotor policy as a conditional denoising diffusion process. We benchmark Diffusion Policy across 12 different tasks from 4 different robot manipulation benchmarks and find that it consistently outperforms existing state-of-the-art robot learning methods with an average improvement of 46.9%. Diffusion Policy learns the gradient of the action-distribution score function and iteratively optimizes with respect to this gradient field during inference via a series of stochastic Langevin dynamics steps. We find that the diffusion formulation yields powerful advantages when used for robot policies, including gracefully handling multimodal action distributions, being suitable for high-dimensional action spaces, and exhibiting impressive training stability. To fully unlock the potential of diffusion models for visuomotor policy learning on physical robots, this paper presents a set of key technical contributions including the incorporation of receding horizon control, visual conditioning, and the time-series diffusion transformer. We hope this work will help motivate a new generation of policy learning techniques that are able to leverage the powerful generative modeling capabilities of diffusion models. Code, data, and training details is publicly available diffusion-policy.cs.columbia.edu (arXiv)

## 🧠 Key ideas (atomic)

- [[Diffusion Policy]] represents a robot visuomotor policy as a conditional denoising diffusion process over the robot action space. (Chi et al., 2023) `ev:asserted` p. 1 ^chi2023diffusion-001
- Instead of directly outputting an action, the policy infers the action-score gradient conditioned on visual observations for K denoising iterations. (Chi et al., 2023) `ev:asserted` p. 1 ^chi2023diffusion-002
- By learning the gradient of the action score function, [[Diffusion Policy]] can express arbitrary normalizable distributions, including [[Multimodal action distributions|multimodal action distributions]]. (Chi et al., 2023) `ev:asserted` p. 1 ^chi2023diffusion-003
- Training energy-based policies often requires negative sampling to estimate an intractable normalization constant, which is known to cause training instability. (Chi et al., 2023) `ev:cited` p. 2 ^chi2023diffusion-004
- According to the authors, [[Diffusion Policy]] bypasses the negative-sampling requirement by learning the gradient of the energy function. (Chi et al., 2023) `ev:asserted` p. 2 ^chi2023diffusion-005
- The policy combines [[Action chunking|high-dimensional action-sequence prediction]] with receding-horizon control to continuously re-plan its action in a closed-loop manner. (Chi et al., 2023) `ev:asserted` p. 2 ^chi2023diffusion-006
- In the [[Diffusion Policy|vision-conditioned diffusion policy]], visual observations are treated as conditioning instead of as part of the joint data distribution. (Chi et al., 2023) `ev:asserted` p. 2 ^chi2023diffusion-007
- The policy extracts the visual representation once regardless of the denoising iterations, which the authors say drastically reduces the computation. (Chi et al., 2023) `ev:asserted` p. 2 ^chi2023diffusion-008
- The proposed time-series diffusion transformer aims to minimize the over-smoothing effects of typical CNN-based models on high-frequency action changes. (Chi et al., 2023) `ev:asserted` p. 2 ^chi2023diffusion-009
- Diffusion Policy is evaluated on 15 tasks from 4 benchmarks under the behavior cloning formulation, in simulated and real-world environments. (Chi et al., 2023) `ev:reported` p. 2 ^chi2023diffusion-010
- [[Diffusion Policy]] outperformed the prior state-of-the-art on all tested benchmarks, with an average success-rate improvement of 46.9%. (Chi et al., 2023) `ev:measured` p. 6 ^chi2023diffusion-011
- The 46.9% figure averages per-task relative improvements of the maximum Diffusion Policy performance over the maximum baseline performance, ignoring mh results. (Chi et al., 2023) `ev:computed` p. 17 ^chi2023diffusion-012
- At each time step the policy predicts Tp steps of actions from To observation steps, executing Ta steps without re-planning. (Chi et al., 2023) `ev:reported` p. 3 ^chi2023diffusion-013
- [[Diffusion Policy]] approximates the conditional distribution p(At|Ot) instead of the joint distribution p(At,Ot) used by Janner et al. for planning. (Chi et al., 2023) `ev:asserted` p. 3 ^chi2023diffusion-014
- The authors state that excluding observation features from the output of the denoising process significantly improves inference speed. (Chi et al., 2023) `ev:asserted` p. 3 ^chi2023diffusion-015
- Excluding observation features from the denoising output also helps make end-to-end training of the vision encoder feasible, according to the authors. (Chi et al., 2023) `ev:asserted` p. 3 ^chi2023diffusion-016
- The CNN-based variant adopts the 1D temporal CNN from Janner et al., modified to condition action generation on observations through FiLM. (Chi et al., 2023) `ev:reported` p. 3 ^chi2023diffusion-017
- Inpainting-based goal-state conditioning was removed from the CNN variant due to incompatibility with a receding prediction horizon. (Chi et al., 2023) `ev:asserted` p. 4 ^chi2023diffusion-018
- The authors found the CNN-based backbone to work well on most tasks out of the box without much hyperparameter tuning. (Chi et al., 2023) `ev:asserted` p. 4 ^chi2023diffusion-019
- The CNN backbone performs poorly when desired action sequences change quickly and sharply, likely due to temporal convolutions preferring low-frequency signals. (Chi et al., 2023) `ev:asserted` p. 4 ^chi2023diffusion-020
- In state-based experiments, most of the best-performing policies are achieved with the transformer backbone, especially at high task complexity. (Chi et al., 2023) `ev:measured` p. 4 ^chi2023diffusion-021
- The authors found the transformer backbone to be more sensitive to hyperparameters, a difficulty they note is not unique to Diffusion Policy. (Chi et al., 2023) `ev:asserted` p. 4 ^chi2023diffusion-022
- The authors recommend starting with the CNN-based implementation on new tasks, switching to the transformer if task complexity limits performance. (Chi et al., 2023) `ev:asserted` p. 4 ^chi2023diffusion-023
- The visual encoder is a standard ResNet-18 without pretraining, trained end-to-end, with spatial softmax pooling replacing global average pooling. (Chi et al., 2023) `ev:reported` p. 4 ^chi2023diffusion-024
- The Square Cosine Schedule proposed in iDDPM was empirically found to work best for the control tasks of the authors. (Chi et al., 2023) `ev:measured` p. 4 ^chi2023diffusion-025
- In real-world experiments, DDIM with 100 training iterations with 10 inference iterations enables 0.1s inference latency on a Nvidia 3080 GPU. (Chi et al., 2023) `ev:measured` p. 4 ^chi2023diffusion-026
- Diffusion Policy with a position-control action space consistently outperforms Diffusion Policy with velocity control, as shown in the ablation. (Chi et al., 2023) `ev:measured` p. 4 ^chi2023diffusion-027
- The authors speculate that [[Multimodal action distributions|action multimodality]] is more pronounced in position-control mode than it is when using velocity control. (Chi et al., 2023) `ev:asserted` p. 5 ^chi2023diffusion-028
- In the Push-T case study, Diffusion Policy learns [[Multimodal action distributions|both the left and right modes]], committing to only one mode within each rollout. (Chi et al., 2023) `ev:measured` p. 5 ^chi2023diffusion-029
- In the same Push-T case study, BET fails to commit to a single mode, which the authors attribute to lacking temporal action consistency. (Chi et al., 2023) `ev:measured` p. 5 ^chi2023diffusion-030
- The authors report that BC-RNN and IBC often get stuck in real-world experiments when idle actions are not explicitly removed from training. (Chi et al., 2023) `ev:asserted` p. 5 ^chi2023diffusion-031
- The noise-prediction network approximates the negative score function, which is independent of the intractable normalization constant Z(o,θ). (Chi et al., 2023) `ev:computed` p. 6 ^chi2023diffusion-032
- For a linear system with linear feedback demonstrations and Tp = 1, DDIM sampling with the optimal denoiser converges to a = −Ks. (Chi et al., 2023) `ev:computed` p. 6 ^chi2023diffusion-033
- The control-theory analysis shows that perfectly cloning a state-dependent behavior requires the learner to implicitly learn a task-relevant dynamics model. (Chi et al., 2023) `ev:computed` p. 6 ^chi2023diffusion-034
- Robomimic comprises 5 tasks with proficient-human demonstrations plus mixed proficient/non-proficient demonstrations for 4 tasks, giving 9 variants in total. (Chi et al., 2023) `ev:reported` p. 6 ^chi2023diffusion-035
- Simulation results are averaged over the last 10 checkpoints across 3 training seeds with 50 environment initializations each. (Chi et al., 2023) `ev:reported` p. 7 ^chi2023diffusion-036
- Due to a bug in the evaluation code, only 22 environment initializations were used for the robomimic tasks, for all methods alike. (Chi et al., 2023) `ev:reported` p. 7 ^chi2023diffusion-037
- On state-based ToolHang, DiffusionPolicy-T reached 1.00/0.87 success, compared with 0.67/0.31 for LSTM-GMM in the state policy benchmark. (Chi et al., 2023) `ev:measured` p. 7 ^chi2023diffusion-038
- On the visual Transport mh variant, DiffusionPolicy-C reached 0.89/0.69 success, compared with 0.44/0.24 for the LSTM-GMM baseline. (Chi et al., 2023) `ev:measured` p. 7 ^chi2023diffusion-039
- Diffusion Policy outperforms baselines on Block Push by a large margin, with a 32% improvement on the p2 metric. (Chi et al., 2023) `ev:measured` p. 8 ^chi2023diffusion-040
- Diffusion Policy outperforms baselines on the Kitchen task by a large margin, with a 213% improvement on the p4 metric. (Chi et al., 2023) `ev:measured` p. 8 ^chi2023diffusion-041
- The action-horizon ablation confirmed a consistency-responsiveness trade-off, with a horizon of 8 steps found optimal for most tested tasks. (Chi et al., 2023) `ev:measured` p. 8 ^chi2023diffusion-042
- In the ablation with simulated latency, [[Diffusion Policy]] maintained peak performance with latency up to 4 steps. (Chi et al., 2023) `ev:measured` p. 8 ^chi2023diffusion-043
- The authors find velocity control more affected by latency than position control, likely due to compounding error effects. (Chi et al., 2023) `ev:measured` p. 8 ^chi2023diffusion-044
- Training ViT-B/16 from scratch on the robomimic Square task reached only 22% success rate, likely due to the limited amount of data. (Chi et al., 2023) `ev:measured` p. 8 ^chi2023diffusion-045
- Training with a frozen pretrained vision encoder yielded poor performance, which the authors read as diffusion policy preferring different representations. (Chi et al., 2023) `ev:measured` p. 8 ^chi2023diffusion-046
- Finetuning the CLIP-trained ViT-B/16 with a 10x smaller learning rate reached 98% success rate with only 50 epochs of training. (Chi et al., 2023) `ev:measured` p. 8 ^chi2023diffusion-047
- On real-world Push-T, Diffusion Policy reached 95% success rate with 0.8 average IoU, compared with 0.84 for the human demonstrations. (Chi et al., 2023) `ev:measured` p. 9 ^chi2023diffusion-048
- On real-world Push-T, the best-performing IBC and LSTM-GMM variants reached 0% and 20% success rate respectively. (Chi et al., 2023) `ev:measured` p. 9 ^chi2023diffusion-049
- With the pretrained R3M encoder, Diffusion Policy achieved an 80% success rate on real-world Push-T but predicted jittery actions. (Chi et al., 2023) `ev:measured` p. 9 ^chi2023diffusion-050
- The authors conclude that end-to-end training is still the most effective way to incorporate visual observation into Diffusion Policy. (Chi et al., 2023) `ev:measured` p. 9 ^chi2023diffusion-051
- When the T block was shifted during fine adjustments, Diffusion Policy immediately re-planned to push from the opposite direction. (Chi et al., 2023) `ev:measured` p. 9 ^chi2023diffusion-052
- The authors suggest the perturbation experiment indicates Diffusion Policy may be able to synthesize novel behavior in response to unseen observations. (Chi et al., 2023) `ev:asserted` p. 9 ^chi2023diffusion-053
- Diffusion Policy completed the real-world mug flipping task with 90% success rate over 20 trials. (Chi et al., 2023) `ev:measured` p. 10 ^chi2023diffusion-054
- On 20 in-distribution initial conditions of mug flipping, the LSTM-GMM policy failed to grasp the mug in all trials. (Chi et al., 2023) `ev:measured` p. 10 ^chi2023diffusion-055
- On sauce pouring, Diffusion Policy achieved close-to-human performance, with 0.74 compared with 0.79 for the human demonstrator. (Chi et al., 2023) `ev:measured` p. 11 ^chi2023diffusion-056
- On periodic sauce spreading, Diffusion Policy achieved close-to-human coverage, with 0.77 compared with 0.79 for the human demonstrator. (Chi et al., 2023) `ev:measured` p. 11 ^chi2023diffusion-057
- LSTM-GMM failed to lift the ladle after successfully scooping sauce in 15 out of 20 of the pouring trials. (Chi et al., 2023) `ev:measured` p. 11 ^chi2023diffusion-058
- The sauce tasks were trained with the same Push-T hyperparameters, with successful policies achieved on the first attempt. (Chi et al., 2023) `ev:reported` p. 11 ^chi2023diffusion-059
- Without haptic feedback, an expert was unable to complete a single bimanual egg beater demonstration out of 10 trials. (Chi et al., 2023) `ev:measured` p. 11 ^chi2023diffusion-060
- Diffusion Policy completed the bimanual egg beater task with 55% success rate over 20 trials, trained using 210 demonstrations. (Chi et al., 2023) `ev:measured` p. 11 ^chi2023diffusion-061
- Diffusion Policy completed the bimanual mat unrolling task with 75% success rate over 20 trials, trained using 162 demonstrations. (Chi et al., 2023) `ev:measured` p. 12 ^chi2023diffusion-062
- Diffusion Policy completed the bimanual shirt folding task with 75% success rate over 20 trials, trained using 284 demonstrations. (Chi et al., 2023) `ev:measured` p. 12 ^chi2023diffusion-063
- The implementation inherits limitations from behavior cloning, such as suboptimal performance with inadequate demonstration data, the authors acknowledge. (Chi et al., 2023) `ev:asserted` p. 13 ^chi2023diffusion-064
- Diffusion Policy has higher computational costs and inference latency compared to simpler methods like LSTM-GMM, the authors acknowledge. (Chi et al., 2023) `ev:asserted` p. 13 ^chi2023diffusion-065
- The authors conclude that their results strongly indicate policy structure poses a significant performance bottleneck during behavior cloning. (Chi et al., 2023) `ev:asserted` p. 13 ^chi2023diffusion-066
- Because DDPMs clip predictions to [−1,1], common zero-mean unit-variance normalization makes some region of the action space inaccessible. (Chi et al., 2023) `ev:asserted` p. 16 ^chi2023diffusion-067
- During tuning, increasing the number of parameters in CNN-based Diffusion Policy always improved performance, the authors report. (Chi et al., 2023) `ev:measured` p. 16 ^chi2023diffusion-068
- An observation horizon of 2 was found good for most tasks, for both state and image observations. (Chi et al., 2023) `ev:measured` p. 16 ^chi2023diffusion-069
- Diffusion Policy outperformed LSTM-GMM at every training dataset size in the Push-T and Square data-efficiency ablation. (Chi et al., 2023) `ev:measured` p. 16 ^chi2023diffusion-070

## 🎯 Contributions

## 📖 Glossary

- **DDPM** — Denoising Diffusion Probabilistic Model; generates outputs by iteratively denoising Gaussian noise.
- **DDIM** — Diffusion sampler that decouples training and inference denoising iterations, allowing fewer inference steps.
- **Receding-horizon control** — Executing part of a predicted action sequence, then re-planning from new observations.
- **Action horizon (Ta)** — Number of predicted action steps executed before the policy re-plans.
- **Observation horizon (To)** — Number of past observation steps the policy conditions on.
- **FiLM** — Feature-wise Linear Modulation; conditions network layers via learned per-channel scale and bias.
- **Implicit policy (IBC)** — Policy defined by an energy-based model, selecting actions that minimize energy.
- **LSTM-GMM** — Recurrent policy with Gaussian-mixture action head; BC-RNN from robomimic.
- **BET** — Behavior Transformer; clusters actions with k-means and predicts per-cluster offsets.
- **Multimodal action distribution** — Several distinct valid actions exist for the same observation.

## ❓ Open questions

- Can diffusion model acceleration methods (new noise schedules, solvers, consistency models) make Diffusion Policy suitable for high-rate control?
- How would Diffusion Policy perform in reinforcement learning paradigms that exploit suboptimal and negative data?
- Would the performance gap between vision encoder architectures become larger on more complex tasks?
- Can transformer-based Diffusion Policy be made less hyperparameter-sensitive with better training techniques or more data?
- How does Diffusion Policy behave when the plant or demonstrator policy is nonlinear, beyond the linear control-theory sanity check?

## 📝 Notes on reading

Version read: arXiv v5 (14 Mar 2024), the journal extension of the RSS 2023 conference paper; it matches the packet identifier arXiv:2303.04137.

Inconsistencies inside the paper and with the registry: the registry abstract says 12 tasks, while the PDF abstract, introduction, evaluation and conclusion say 15 tasks. Section 3.4 states DDIM with 10 inference iterations on real-world experiments, while Appendix A.4 and Table 7 give 16 inference iterations. The Franka Kitchen text gives 566 demonstrations, while Table 3 lists 656 PH demonstrations. The real-world Push-T text refers to Fig 6 for the UR5 setup, which is Table 6; Appendix C.1.2 refers to Fig. 7 for IBC training difficulty, which is Fig. 6. Fig 10 labels the pouring metric IoU while the text calls both results coverage. The Table 4 caption says PushBlock while the text says Block Push. Section 4.2 says Diffusion Policy with position control consistently outperforms velocity control; Fig 4 shows this only for Square and Kitchen p4.

Figures described only: Fig 1 (policy representations), Fig 2 (architecture overview), Fig 4 (velocity vs position control bars), Fig 5 (action horizon and latency curves), Fig 6 (IBC training instability curves), Fig 14 (observation horizon ablation), Fig 15 (data efficiency curves), Figs 16-21 (bimanual rollout states). Values from these plots were not claimed.

Tables 1 and 2 report (max performance)/(average of last 10 checkpoints); only headline rows were claimed. Tables 7 and 8 (hyperparameters) were extracted as broken column streams and were not claimed per task.

## Suggested new concepts

- Diffusion Policy — a widely used visuomotor policy class that later work builds on and compares against.
- Action chunking / receding-horizon action prediction — a design choice shared across many imitation-learning policies.
- Position vs velocity control action spaces — the paper shows the choice interacts with policy class.
- Implicit behavioral cloning (energy-based policies) — main contrast class for training stability arguments.
- Multimodal action distributions in behavior cloning — a recurring challenge motivating several policy representations.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Políticas de difusión con *action chunks* (C.5, F.6).
- **[[03_aplicaciones_vision_por_computador]]** — Política visuomotora por difusión, rotación 6D
