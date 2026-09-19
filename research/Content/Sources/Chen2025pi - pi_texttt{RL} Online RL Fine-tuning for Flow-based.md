---
aliases: []
type: "source"
title: "$\\pi_\\texttt{RL}$: Online RL Fine-tuning for Flow-based Vision-Language-Action Models"
citekey: "Chen2025pi"
doi: "10.48550/arXiv.2510.25889"
arxiv: "2510.25889"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2510.25889"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Kang Chen", "Zhihao Liu", "Tonghe Zhang", "Zhen Guo", "Si Xu", "Hao Lin", "Hongzhi Zang", "Xiang Li", "Quanlu Zhang", "Zhaofei Yu", "Guoliang Fan", "Tiejun Huang", "Yu Wang", "Chao Yu"]
sha256: ["484e9f8be118be4f7adfd18470abc330e29b1b4cf457d316dc85a63e65299d36"]
pdf: "Content/Papers/Chen2025pi.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Chen2025pi.pdf]]

> [!abstract] One-sentence summary
> πRL makes flow-matching VLAs such as π0 and π0.5 trainable with online PPO through two tractable log-likelihood formulations, Flow-Noise and Flow-SDE, lifting few-shot SFT policies to or above full-dataset baselines on LIBERO, ManiSkill, MetaWorld and CALVIN.

## Abstract

Vision-Language-Action (VLA) models enable robots to understand and perform complex tasks from multimodal input. Although recent work explores using reinforcement learning (RL) to automate the laborious data collection process in scaling supervised fine-tuning (SFT), applying RL to large-scale flow-based VLAs (\eg, $π_0$, $π_{0.5}$) remains challenging due to intractable action log-likelihoods raised from flow matching. We address this challenge with $π_{\texttt{RL}}$, featuring two technical approaches: (1) \textbf{Flow-Noise} models the denoising process as a discrete-time MDP with a learnable noise network for exact log-likelihood computation. (2) \textbf{Flow-SDE} integrates denoising with agent-environment interaction, formulating a two-layer MDP that employs ODE-to-SDE conversion for efficient RL exploration. We evaluate $π_{\texttt{RL}}$ across various benchmarks, with experiments demonstrating that RL yields significant performance improvements in both in-distribution and out-of-distribution settings. (arXiv)

## 🧠 Key ideas (atomic)

- πRL is an online RL fine-tuning framework for flow-based vision-language-action models, featuring the Flow-Noise and Flow-SDE formulations. (Chen et al., 2025) `ev:asserted` p. 2 ^chen2025pi-001
- The authors identify the fundamental challenge of RL for flow-based VLAs as characterizing a log-likelihood for the executed actions. (Chen et al., 2025) `ev:asserted` p. 2 ^chen2025pi-002
- According to the authors, directly computing the exact likelihood of flow-based VLAs is inaccurate with few denoising steps. (Chen et al., 2025) `ev:asserted` p. 3 ^chen2025pi-003
- The deterministic nature of ODE sampling in flow-based VLAs precludes exploration, making their implementation within RL non-trivial, the authors state. (Chen et al., 2025) `ev:asserted` p. 3 ^chen2025pi-004
- Flow-Noise adds a learnable noise network to the denoising process and models denoising as a discrete-time MDP for exact log-likelihood estimation. (Chen et al., 2025) `ev:asserted` p. 2 ^chen2025pi-005
- In Flow-Noise, the noise network is trained jointly with the velocity but discarded after fine-tuning, leaving a deterministic policy for inference. (Chen et al., 2025) `ev:reported` p. 4 ^chen2025pi-006
- Flow-SDE converts the deterministic ODE denoising into an equivalent SDE that preserves the marginal probability density of the generated actions. (Chen et al., 2025) `ev:asserted` p. 4 ^chen2025pi-007
- Flow-SDE builds a two-layer MDP that couples the inner denoising process with the outer policy-environment interaction loop, following DPPO. (Chen et al., 2025) `ev:asserted` p. 4 ^chen2025pi-008
- In the two-layer MDP, reward is granted only upon completion of the denoising process and interaction with the environment. (Chen et al., 2025) `ev:reported` p. 5 ^chen2025pi-009
- Flow-SDE uses hybrid ODE-SDE rollouts, sampling one random denoising time per step for SDE exploration while remaining steps stay deterministic ODE updates. (Chen et al., 2025) `ev:reported` p. 5 ^chen2025pi-010
- Policies are optimized with PPO, treating each action chunk as a single macro-step whose reward is the sum of per-step rewards. (Chen et al., 2025) `ev:reported` p. 5 ^chen2025pi-011
- For π0.5, the critic network attaches directly to the VLM output, giving a value estimate from integrated image, language and state inputs. (Chen et al., 2025) `ev:reported` p. 6 ^chen2025pi-012
- For π0, the critic value is approximated by averaging action-expert value estimates across the entire denoising trajectory. (Chen et al., 2025) `ev:reported` p. 6 ^chen2025pi-013
- During the RL stage, the VLM parameters are frozen and the 300M action expert of the 3.3B model is exclusively fine-tuned. (Chen et al., 2025) `ev:reported` p. 13 ^chen2025pi-014
- Experiments were conducted on 8 NVIDIA H100 80GB GPUs using the RLinf codebase with co-located environment, rollout and actor models. (Chen et al., 2025) `ev:reported` p. 13 ^chen2025pi-015
- Across the four benchmarks, the π0 model achieves a maximum average improvement of +29.2% over its SFT baseline. (Chen et al., 2025) `ev:measured` p. 6 ^chen2025pi-016
- Across the four benchmarks, π0.5 with Flow-SDE shows a +31.0 increase in average success rate over its SFT baseline. (Chen et al., 2025) `ev:measured` p. 7 ^chen2025pi-017
- On LIBERO, few-shot SFT of π0.5 followed by RL reaches 98.3% success, outperforming the 96.9% full-dataset SFT baseline. (Chen et al., 2025) `ev:measured` p. 6 ^chen2025pi-018
- For few-shot π0 on LIBERO, the SFT baseline averages only 57.6%, indicating the model struggles with limited demonstration data. (Chen et al., 2025) `ev:measured` p. 14 ^chen2025pi-019
- On LIBERO, πRL raises few-shot π0 to 96.1% with Flow-SDE and 97.6% with Flow-Noise, surpassing the 94.2% full-dataset π0 SFT. (Chen et al., 2025) `ev:measured` p. 14 ^chen2025pi-020
- After few-shot SFT, πRL boosts the π0.5 LIBERO-Long success rate from 43.9% to 94.0%, a 50.1% improvement. (Chen et al., 2025) `ev:measured` p. 14 ^chen2025pi-021
- For π0.5, only 40 trajectories provided a unified few-shot SFT checkpoint across all four LIBERO task suites. (Chen et al., 2025) `ev:reported` p. 13 ^chen2025pi-022
- The ManiSkill benchmark spans 4,352 pick-and-place combinations built from 16 object types, 17 receptacles and 16 table scenes. (Chen et al., 2025) `ev:reported` p. 14 ^chen2025pi-023
- ManiSkill SFT data consist of 16,384 episodes synthesized with the MPLib motion planning suite, each with 15 additional frames appended. (Chen et al., 2025) `ev:reported` p. 14 ^chen2025pi-024
- The ManiSkill reward gives 1.0 for correct object placement and an auxiliary 0.1 for successful gripper-object attachment. (Chen et al., 2025) `ev:reported` p. 15 ^chen2025pi-025
- On in-distribution ManiSkill tasks, πRL increases the success rate of π0 from 38.4% to 77.8%. (Chen et al., 2025) `ev:measured` p. 15 ^chen2025pi-026
- On in-distribution ManiSkill tasks, πRL improves the success rate of π0.5 from 40.1% to 90.9%. (Chen et al., 2025) `ev:measured` p. 15 ^chen2025pi-027
- On CALVIN Scene D, Flow-SDE raises the average completed subtasks of π0.5 from 3.838 to 4.717 over SFT. (Chen et al., 2025) `ev:measured` p. 15 ^chen2025pi-028
- On CALVIN, the Len-5 success rate of π0.5 with Flow-SDE rises from 61.3% under SFT to 87.0%. (Chen et al., 2025) `ev:measured` p. 15 ^chen2025pi-029
- For π0.5 on CALVIN, the Flow-SDE gain over SFT grows from 7.0% on Len-1 tasks to 25.7% on Len-5 sequences. (Chen et al., 2025) `ev:measured` p. 16 ^chen2025pi-030
- On MetaWorld MT50, the RL fine-tuned π0 and π0.5 models achieve average success rates of 85.8% and 70.7%, respectively. (Chen et al., 2025) `ev:measured` p. 16 ^chen2025pi-031
- Both RL fine-tuned models on MetaWorld MT50 surpass the 68.2% average success rate of the SmolVLA baseline. (Chen et al., 2025) `ev:measured` p. 16 ^chen2025pi-032
- On the SIMPLER benchmark with a WidowX-250S arm, πRL increases the average success rate of π0 from 67.2% to 86.7%. (Chen et al., 2025) `ev:measured` p. 18 ^chen2025pi-033
- With Flow-Noise on SIMPLER, π0.5 average success improves from 59.2 under SFT to 79.1 after RL. (Chen et al., 2025) `ev:measured` p. 17 ^chen2025pi-034
- Deployed zero-shot on a real Franka Panda pick-and-place task, the RL-tuned policy achieves a 40% success rate. (Chen et al., 2025) `ev:measured` p. 18 ^chen2025pi-035
- In that zero-shot real-world deployment, the SFT baseline trained on 20 motion-planner trajectories fails to complete the task. (Chen et al., 2025) `ev:measured` p. 18 ^chen2025pi-036
- In-distribution RL gains transfer to OOD scenarios in ManiSkill and CALVIN, where the domain shift primarily stems from environmental variations. (Chen et al., 2025) `ev:measured` p. 7 ^chen2025pi-037
- In the MetaWorld OOD setting with distinct manipulation tasks, performance fluctuates during RL without showing significant improvement. (Chen et al., 2025) `ev:measured` p. 7 ^chen2025pi-038
- The authors suggest the benefits of RL are primarily localized to action-level refinement rather than broader cross-task generalization. (Chen et al., 2025) `ev:asserted` p. 7 ^chen2025pi-039
- On ManiSkill OOD tests, π0.5 with Flow-Noise raises the average OOD success rate from 26.4 to 53.4. (Chen et al., 2025) `ev:measured` p. 14 ^chen2025pi-040
- For π0.5 on ManiSkill, Flow-SDE enhances the in-distribution success rate by 126.7% and the OOD success by 102.3%. (Chen et al., 2025) `ev:measured` p. 17 ^chen2025pi-041
- For π0.5, the 73.9% gain in ManiSkill visual generalization trails the 126.7% increase observed in the training environment. (Chen et al., 2025) `ev:measured` p. 17 ^chen2025pi-042
- The authors suggest this visual gap likely stems from freezing the VLM backbone during RL, restricting adaptation to novel textures. (Chen et al., 2025) `ev:asserted` p. 17 ^chen2025pi-043
- Trained on CALVIN ABC environments and evaluated zero-shot on Scene D, the RL policy reaches 79.1% versus the 61.3% SFT baseline. (Chen et al., 2025) `ev:measured` p. 17 ^chen2025pi-044
- On MetaWorld ML45, the model retains the OOD skills learned during the SFT phase throughout the RL training process. (Chen et al., 2025) `ev:measured` p. 17 ^chen2025pi-045
- ManiSkill OOD tests indicate that the semantic generalization of both the SFT and the RL models remains limited. (Chen et al., 2025) `ev:measured` p. 22 ^chen2025pi-046
- On LIBERO-Long with π0, the critic placed after the VLM exhibits slightly superior performance, lower value loss and higher explained variance. (Chen et al., 2025) `ev:measured` p. 7 ^chen2025pi-047
- A four-layer MLP critic leads to a more accurate value approximation than a one-layer MLP, with enhanced performance and training stability. (Chen et al., 2025) `ev:measured` p. 8 ^chen2025pi-048
- On LIBERO-Goal, the one-layer MDP converges most rapidly, but final success rates remain consistent across all three MDP formulations. (Chen et al., 2025) `ev:measured` p. 8 ^chen2025pi-049
- The hybrid two-layer MDP achieves a 2× speedup over the standard two-layer approach, with update times of 428.6 versus 814.2 seconds. (Chen et al., 2025) `ev:measured` p. 8 ^chen2025pi-050
- The one-layer MDP yields no substantial wall-clock time advantage over the standard two-layer model, as full denoising trajectories must be recalculated. (Chen et al., 2025) `ev:measured` p. 8 ^chen2025pi-051
- On LIBERO-Spatial, SFT train-stage success degrades from 62.3 to 46.6 as the Flow-SDE noise level rises from 0.2 to 0.8. (Chen et al., 2025) `ev:measured` p. 9 ^chen2025pi-052
- After RL on LIBERO-Spatial, π0 reaches 98.1 eval success at noise level 0.8, versus 73.1 at noise level 0.2. (Chen et al., 2025) `ev:measured` p. 9 ^chen2025pi-053
- In Flow-SDE on LIBERO-Spatial, training with minimal noise leads to instability, characterized by a significantly higher clip fraction. (Chen et al., 2025) `ev:measured` p. 10 ^chen2025pi-054
- The authors attribute the low-noise training instability to the substantially larger gradient magnitudes associated with low-noise regimes. (Chen et al., 2025) `ev:asserted` p. 10 ^chen2025pi-055
- On LIBERO-Spatial, the SFT train-stage success rate is 9.4 with one denoising step, versus 56.1 with four steps. (Chen et al., 2025) `ev:measured` p. 9 ^chen2025pi-056
- According to the authors, increasing the number of denoise steps enhances rollout performance but increases training complexity and computational overhead. (Chen et al., 2025) `ev:asserted` p. 10 ^chen2025pi-057
- Larger action chunk sizes yield marginal performance gains but lead to less reliable advantage estimation, evidenced by diminished explained variance. (Chen et al., 2025) `ev:measured` p. 10 ^chen2025pi-058
- With Flow-SDE on LIBERO, PPO reaches 96.0 average success for π0, compared with 90.0 for GRPO. (Chen et al., 2025) `ev:measured` p. 18 ^chen2025pi-059
- For π0.5 with Flow-SDE on LIBERO, PPO averages 97.9 success versus 91.5 for GRPO, from a 77.1 SFT baseline. (Chen et al., 2025) `ev:measured` p. 18 ^chen2025pi-060
- Fine-tuning the VLM with LoRA jointly with the action expert shows no evident benefit on LIBERO over a frozen VLM. (Chen et al., 2025) `ev:measured` p. 19 ^chen2025pi-061
- A cosine-annealing learning rate scheduler prevents the KL divergence from escalating in π0.5 RL training on LIBERO-Long. (Chen et al., 2025) `ev:measured` p. 20 ^chen2025pi-062
- Applied to GR00T N1.5 with Flow-SDE and PPO, πRL raises few-shot LIBERO average success from 52.5% to 89.9%. (Chen et al., 2025) `ev:measured` p. 21 ^chen2025pi-063
- For GR00T, dropout layers in the expert model were replaced with identity layers, since dropout is recognized to destabilize online RL. (Chen et al., 2025) `ev:reported` p. 21 ^chen2025pi-064
- Due to the low sample efficiency of online RL, the framework currently relies on [[Sim-to-real transfer|sim-to-real deployment]] rather than real-world RL training. (Chen et al., 2025) `ev:asserted` p. 10 ^chen2025pi-065
- The current noise injection strategy exhibits a performance drop during the ODE-to-SDE conversion, which the authors list as a limitation. (Chen et al., 2025) `ev:asserted` p. 21 ^chen2025pi-066
- In the authors' experiments, Flow-CPS sampling mitigated the ODE-SDE precision error but yielded limited RL improvement. (Chen et al., 2025) `ev:measured` p. 21 ^chen2025pi-067

## 🎯 Contributions

## 📖 Glossary

- **Flow matching** — Generative method learning a vector field that transports Gaussian noise to target actions.
- **Flow-Noise** — πRL variant injecting learnable noise per denoising step for tractable log-likelihoods.
- **Flow-SDE** — πRL variant converting the denoising ODE to a marginal-preserving SDE inside a two-layer MDP.
- **Two-layer MDP** — Inner denoising MDP embedded in the outer agent-environment MDP.
- **Hybrid ODE-SDE rollout** — Sampling where only one random denoising step is stochastic, the rest deterministic.
- **Action chunk** — Sequence of consecutive actions executed from a single observation.
- **GAE** — Generalized Advantage Estimation, a low-variance advantage estimator used by PPO.
- **Explained variance** — Fraction of return variance captured by the critic's value predictions.
- **Real2Sim2Real** — Building a simulator from a real scene, training there, then deploying back to reality.

## ❓ Open questions

- Can RL fine-tuning of flow-based VLAs extend to entirely novel task objectives, where MetaWorld ML45 showed no stable OOD gains?
- Can an ODE-to-SDE conversion preserve the action distribution without the performance drop seen at conversion?
- Would jointly tuning the VLM help on benchmarks with more scene variability than LIBERO?
- Can online RL become sample-efficient enough for direct real-world training instead of sim-to-real?
- How far can smarter mixed ODE-SDE rollout schedules reduce Flow-SDE training cost?
- Does the 40% real-world success hold over more tasks and trials than the single reported pick-and-place?

## 📝 Notes on reading

Read the arXiv v3 preprint (dated January 30, 2026, arXiv stamp 29 Jan 2026). The author list printed in the PDF includes Bingwen Wei and Jiakai Zhou, who are absent from the registry metadata.

Inconsistencies inside the paper: (1) Table 3 gives π0 Flow-SDE LIBERO average 96.1 (+38.5), while Table 9 reports the same PPO run as 96.0 (+38.4). (2) Appendix C.1 says πRL reaches 98.3% despite using only a single trajectory for SFT, but the same section states π0.5 few-shot SFT uses 40 trajectories. (3) The ManiSkill ID text on p. 15 pairs π0 Flow-Noise (77.8%) with π0.5 Flow-SDE (90.9%) without saying so. (4) The CALVIN OOD paragraph (p. 17) mentions 'identical D→D training settings' while describing ABC→D evaluation. (5) Section 5.3.3 calls 0.08 and 0.16 bounds on log-variance for learnable noise.

Figures described only: Fig. 5 (OOD curves on CALVIN, ManiSkill, MetaWorld), Figs. 6–11 (ablation curves), Figs. 13–16 (VLM LoRA, scheduler, ManiSkill critic warm-up, episode length; the expert episode length is marked 34.5±2.6). Equations on pp. 3–6 were partly garbled in extraction; formulas were not claimed. Per-cell values of Table 7 (ManiSkill OOD breakdown) and hyperparameter Tables 11–13 were not claimed individually. SFT data details (58 of 1,692 LIBERO demonstrations for π0, 208 for Long) and binary LIBERO rewards were left unclaimed to stay within the claim budget.

## Suggested new concepts

- Flow-based VLA reinforcement learning — the paper frames log-likelihood tractability as the central obstacle for RL on flow-matching policies.
- ODE-to-SDE conversion for flow policies — reused from Flow-GRPO to create exploration while preserving marginals; key design choice with noise-level trade-offs.
- Two-layer MDP for denoising policies — couples generative denoising steps with environment steps; shared with DPPO.
- Real2Sim2Real with Gaussian Splatting — simulator construction used for zero-shot real deployment of RL-tuned VLAs.
- Few-shot SFT plus RL — pattern where RL on sparse demonstrations matches full-dataset SFT.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H4.** Extiende DPPO y ReinFlow a VLA de flujo (pi0, pi0.5) con Flow-Noise y Flow-SDE para obtener log-verosimilitudes tratables en RL online.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
