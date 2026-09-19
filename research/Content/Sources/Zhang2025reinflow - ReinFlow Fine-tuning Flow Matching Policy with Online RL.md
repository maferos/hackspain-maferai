---
aliases: []
type: "source"
title: "ReinFlow: Fine-tuning Flow Matching Policy with Online RL"
citekey: "Zhang2025reinflow"
doi: "10.48550/arXiv.2505.22094"
arxiv: "2505.22094"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2505.22094"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Tonghe Zhang", "Chao Yu", "Sichang Su", "Yu Wang"]
sha256: ["dff2f6406cb7b07fb18efdbffda74b46d8ca5cfea0548a09176d38ecd8141994"]
pdf: "Content/Papers/Zhang2025reinflow.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 70
---

📄 PDF: [[Zhang2025reinflow.pdf]]

> [!abstract] One-sentence summary
> ReinFlow injects a learnable, bounded Gaussian noise net into a flow matching policy's denoising path so that its action likelihood becomes exact and PPO-style online RL can fine-tune Rectified Flow and Shortcut policies at one to four denoising steps, beating DPPO and FQL on Gym, Franka Kitchen and Robomimic with less wall time.

## Abstract

We propose ReinFlow, a simple yet effective online reinforcement learning (RL) framework that fine-tunes a family of flow matching policies for continuous robotic control. Derived from rigorous RL theory, ReinFlow injects learnable noise into a flow policy's deterministic path, converting the flow into a discrete-time Markov Process for exact and straightforward likelihood computation. This conversion facilitates exploration and ensures training stability, enabling ReinFlow to fine-tune diverse flow model variants, including Rectified Flow [35] and Shortcut Models [19], particularly at very few or even one denoising step. We benchmark ReinFlow in representative locomotion and manipulation tasks, including long-horizon planning with visual input and sparse reward. The episode reward of Rectified Flow policies obtained an average net growth of 135.36% after fine-tuning in challenging legged locomotion tasks while saving denoising steps and 82.63% of wall time compared to state-of-the-art diffusion RL fine-tuning method DPPO [43]. The success rate of the Shortcut Model policies in state and visual manipulation tasks achieved an average net increase of 40.34% after fine-tuning with ReinFlow at four or even one denoising step, whose performance is comparable to fine-tuned DDIM policies while saving computation time for an average of 23.20%. Project webpage: https://reinflow.github.io/ (arXiv)

## 🧠 Key ideas (atomic)

- ReinFlow is proposed as an online reinforcement learning framework that fine-tunes a family of [[Flow matching policy|flow matching policies]] for continuous robotic control. (Zhang et al., 2025) `ev:asserted` p. 1 ^zhang2025reinflow-001
- ReinFlow injects learnable noise into a [[Flow matching policy|flow policy]]'s deterministic path, converting the flow into a discrete-time Markov process for exact likelihood computation. (Zhang et al., 2025) `ev:asserted` p. 1 ^zhang2025reinflow-002
- The authors describe ReinFlow as the first online RL algorithm to stably fine-tune flow matching policies, especially in very few or one denoising step. (Zhang et al., 2025) `ev:asserted` p. 2 ^zhang2025reinflow-003
- Prior work suggests scaling demonstration quantity may not be a panacea, as success rate quickly plateaus when only the number of demonstrations increases. (Zhang et al., 2025) `ev:cited` p. 1 ^zhang2025reinflow-004
- The authors argue that [[Flow matching policy|imitation-trained flow policies]] lack a built-in exploration mechanism, so robots trained on imperfect data could struggle on challenging tasks. (Zhang et al., 2025) `ev:asserted` p. 2 ^zhang2025reinflow-005
- For conditional flows governed by a neural ODE, the log probability could be challenging to obtain and unstable to backpropagate through. (Zhang et al., 2025) `ev:asserted` p. 2 ^zhang2025reinflow-006
- Estimating a flow's log probability with the continuous-time divergence integral introduces Monte-Carlo trace error and discretization error that grows with fewer denoising steps. (Zhang et al., 2025) `ev:cited` p. 5 ^zhang2025reinflow-007
- In ReinFlow each denoising transition is a normal distribution whose mean follows the velocity field and whose standard deviation comes from a noise injection network. (Zhang et al., 2025) `ev:reported` p. 5 ^zhang2025reinflow-008
- The noise is conditioned on the current denoised action and time to preserve the Markov property of the flow process. (Zhang et al., 2025) `ev:asserted` p. 5 ^zhang2025reinflow-009
- The authors state that the joint log probability of the noise-injected denoising chain is exact even for arbitrarily large step sizes, unlike the trace estimate. (Zhang et al., 2025) `ev:asserted` p. 5 ^zhang2025reinflow-010
- Theorem 4.1 gives a policy gradient for policies described by a discrete-time Markov process, weighting the summed per-step transition log-probabilities by the advantage. (Zhang et al., 2025) `ev:computed` p. 6 ^zhang2025reinflow-011
- With [[Action chunking|action chunking]], the log probability of a chunk equals the sum of the log probabilities of its internal actions under conditional independence. (Zhang et al., 2025) `ev:computed` p. 25 ^zhang2025reinflow-012
- The authors implement the advantage form of the policy gradient with the PPO clipped surrogate loss, citing its stability as the reason. (Zhang et al., 2025) `ev:reported` p. 6 ^zhang2025reinflow-013
- The noise injection network is trained jointly with the velocity network using the same policy gradient loss as the velocity net. (Zhang et al., 2025) `ev:reported` p. 7 ^zhang2025reinflow-014
- After fine-tuning the noise network is discarded, recovering [[Flow matching policy|a flow matching policy]] that is still made up of deterministic maps. (Zhang et al., 2025) `ev:reported` p. 7 ^zhang2025reinflow-015
- Empirically, the authors find that the noise level naturally decays when the success rate converges to 100%. (Zhang et al., 2025) `ev:measured` p. 7 ^zhang2025reinflow-016
- The noise network output passes through a Tanh with an affine transform, bounding the noise standard deviation between σmin and σmax. (Zhang et al., 2025) `ev:reported` p. 28 ^zhang2025reinflow-017
- For state-input tasks, the noise injection network adds a parameter increase below 6% relative to the pre-trained velocity network. (Zhang et al., 2025) `ev:reported` p. 29 ^zhang2025reinflow-018
- In the Robomimic visual tasks, the noise network adds between 14.59% and 18.91% of the velocity network's parameter count. (Zhang et al., 2025) `ev:reported` p. 29 ^zhang2025reinflow-019
- ReinFlow can regularize toward the pre-trained policy by minimizing a tractable upper bound on the Wasserstein-2 distance between the two policies. (Zhang et al., 2025) `ev:reported` p. 7 ^zhang2025reinflow-020
- Entropy regularization in ReinFlow uses the negative per-symbol entropy rate of the denoising chain, which has closed form for Gaussian transitions. (Zhang et al., 2025) `ev:reported` p. 7 ^zhang2025reinflow-021
- By default, the authors adopt entropy regularization for state-input tasks, with no regularization for visual manipulation tasks. (Zhang et al., 2025) `ev:reported` p. 7 ^zhang2025reinflow-022
- Gym locomotion experiments cover Hopper, Walker2d, Ant and Humanoid, with medium or medium-expert demonstrations collected from the D4RL dataset. (Zhang et al., 2025) `ev:reported` p. 8 ^zhang2025reinflow-023
- For the Humanoid task, the pre-training data is sampled from the authors' own pre-trained SAC agent rather than from D4RL. (Zhang et al., 2025) `ev:reported` p. 8 ^zhang2025reinflow-024
- In Franka Kitchen, a Franka robot completes four state-based manipulation tasks sequentially, pre-trained on complete, mixed, or partial teleoperated demonstrations. (Zhang et al., 2025) `ev:reported` p. 8 ^zhang2025reinflow-025
- Robomimic Can, Square and Transport data are processed following DPPO, containing fewer and lower-quality demonstrations than proficient human data. (Zhang et al., 2025) `ev:reported` p. 8 ^zhang2025reinflow-026
- In the sparse-reward manipulation tasks, the agent receives a reward of +1 only upon task completion, otherwise receiving zero. (Zhang et al., 2025) `ev:reported` p. 27 ^zhang2025reinflow-027
- The main baselines are DPPO, an online RL method for diffusion policies, and FQL, an offline RL method for flow policies. (Zhang et al., 2025) `ev:reported` p. 8 ^zhang2025reinflow-028
- Policies fine-tuned with ReinFlow achieved an average episode reward net increase of 135.36% in OpenAI Gym locomotion tasks using D4RL datasets. (Zhang et al., 2025) `ev:measured` p. 31 ^zhang2025reinflow-029
- ReinFlow fine-tuning yielded an average success rate increase of 31.29% in the three Franka Kitchen tasks. (Zhang et al., 2025) `ev:measured` p. 31 ^zhang2025reinflow-030
- Across the three Robomimic visual manipulation tasks, ReinFlow-S and ReinFlow-R improved pre-trained success rate by an average of 45.77%. (Zhang et al., 2025) `ev:measured` p. 8 ^zhang2025reinflow-031
- Across all manipulation tasks, policies fine-tuned with ReinFlow achieved an average success rate increase of 40.34% over the pre-trained policies. (Zhang et al., 2025) `ev:measured` p. 31 ^zhang2025reinflow-032
- The introduction reports a wall time reduction of 62.82% for all tasks compared with the diffusion RL method DPPO. (Zhang et al., 2025) `ev:measured` p. 2 ^zhang2025reinflow-033
- The PDF abstract reports that Rectified Flow policies saved 82.63% of wall time versus DPPO in legged locomotion tasks. (Zhang et al., 2025) `ev:abstract` p. 1 ^zhang2025reinflow-034
- In Hopper-v2, fine-tuning with ReinFlow-R raised the average episode reward from 1431.80±27.57 to 3205.33±32.09, a 123.87% net increase. (Zhang et al., 2025) `ev:measured` p. 32 ^zhang2025reinflow-035
- In Humanoid-v3, fine-tuning with ReinFlow-R raised the average episode reward from 1926.48±41.48 to 5076.12±37.47, a 163.49% net increase. (Zhang et al., 2025) `ev:measured` p. 32 ^zhang2025reinflow-036
- In Ant-v2, ReinFlow-R raised episode reward from 1230.54±8.18 to 4009.18±44.60, reported as a 225.81% net increase. (Zhang et al., 2025) `ev:measured` p. 32 ^zhang2025reinflow-037
- In image-based Transport, ReinFlow-S raised success rate from 30.17±2.46% to 88.67±4.40%, a net increase of 58.50%. (Zhang et al., 2025) `ev:measured` p. 32 ^zhang2025reinflow-038
- In image-based Square, ReinFlow-R raised success rate from 25.00±1.47% to 74.83±0.24%, a net increase of 49.83%. (Zhang et al., 2025) `ev:measured` p. 32 ^zhang2025reinflow-039
- In image-based Can, ReinFlow-S raised success rate from 57.83±1.25% to 98.50±0.71%, a net increase of 40.67%. (Zhang et al., 2025) `ev:measured` p. 32 ^zhang2025reinflow-040
- In Kitchen-partial, ReinFlow-S raised success rate from 40.00±0.28% to 84.59±12.38%, a net increase of 44.59%. (Zhang et al., 2025) `ev:measured` p. 32 ^zhang2025reinflow-041
- ReinFlow reached Robomimic success rates comparable to DPPO while requiring significantly fewer fine-tuning steps and less wall-clock time. (Zhang et al., 2025) `ev:measured` p. 8 ^zhang2025reinflow-042
- ReinFlow used one denoising step in Can and Square and a four-step flow in Transport, against five-step DDIM in DPPO. (Zhang et al., 2025) `ev:reported` p. 8 ^zhang2025reinflow-043
- In Gym and Franka Kitchen, ReinFlow uses 4 denoising steps where DPPO uses 10, which the authors link to reduced wall time. (Zhang et al., 2025) `ev:reported` p. 26 ^zhang2025reinflow-044
- The authors report that in Gym and Franka Kitchen benchmarks ReinFlow achieves the best overall efficiency and performance improvement. (Zhang et al., 2025) `ev:measured` p. 8 ^zhang2025reinflow-045
- In Hopper-v2, one iteration took 11.715 ± 0.123 seconds for ReinFlow-R versus 99.046 ± 0.890 seconds for DPPO. (Zhang et al., 2025) `ev:measured` p. 30 ^zhang2025reinflow-046
- In image-based Transport, ReinFlow-S took 558.359 ± 0.915 seconds per iteration, longer than DPPO's 419.317 ± 17.493 seconds. (Zhang et al., 2025) `ev:measured` p. 30 ^zhang2025reinflow-047
- FQL is more sample efficient than DPPO and ReinFlow in simpler Gym tasks such as Hopper and Walker2d. (Zhang et al., 2025) `ev:measured` p. 31 ^zhang2025reinflow-048
- In more complex locomotion tasks, FQL generally struggles and is asymptotically inferior to both DPPO and ReinFlow. (Zhang et al., 2025) `ev:measured` p. 31 ^zhang2025reinflow-049
- The authors observe that a multi-step FQL policy may struggle to match the reward achieved by pure behavior cloning pre-training. (Zhang et al., 2025) `ev:measured` p. 26 ^zhang2025reinflow-050
- Scaling inference steps or pre-training data quantity does not consistently improve the reward of Rectified Flow policies in Hopper-v2. (Zhang et al., 2025) `ev:measured` p. 9 ^zhang2025reinflow-051
- ReinFlow consistently improves the success rate or reward over the pre-trained policies regardless of the pre-training scale. (Zhang et al., 2025) `ev:measured` p. 9 ^zhang2025reinflow-052
- Fine-tuning a Square policy pre-trained on 16 episodes failed, which the authors attribute to an overly low initial success rate. (Zhang et al., 2025) `ev:measured` p. 32 ^zhang2025reinflow-053
- A Square policy pre-trained on 100 episodes rose from 25.14% to an average fine-tuned success rate of 77.40%. (Zhang et al., 2025) `ev:measured` p. 33 ^zhang2025reinflow-054
- ReinFlow's effectiveness is not affected by altering the time sampling distribution used to pre-train the flow matching policy. (Zhang et al., 2025) `ev:measured` p. 9 ^zhang2025reinflow-055
- Conditioning the noise network on both observations and time often yields a higher success rate than conditioning on observations alone. (Zhang et al., 2025) `ev:measured` p. 9 ^zhang2025reinflow-056
- In Humanoid-v3, state-time noise conditioning reached 5076.12 ± 37.47 reward versus 4987.39 ± 97.82 with state-only conditioning. (Zhang et al., 2025) `ev:measured` p. 35 ^zhang2025reinflow-057
- In Ant, small noise leads to limited exploration, while moderate noise enables rapid improvement with up to three times higher rewards. (Zhang et al., 2025) `ev:measured` p. 10 ^zhang2025reinflow-058
- In Kitchen-complete, noise std 0.001 gave 70.42% ± 3.21% success versus 99.08% ± 1.01% with noise std 0.16. (Zhang et al., 2025) `ev:measured` p. 35 ^zhang2025reinflow-059
- The authors state reducing noise proves beneficial for visuomotor policies, precision-critical tasks, longer denoising chains, and weakly pre-trained models. (Zhang et al., 2025) `ev:asserted` p. 10 ^zhang2025reinflow-060
- Adding entropy regularization, especially in locomotion tasks, is generally more effective than constraining the policy with a W2 regularizer. (Zhang et al., 2025) `ev:measured` p. 10 ^zhang2025reinflow-061
- The authors suggest the W2 constraint enforced by offline FQL helps explain why it underperforms compared with their online approach. (Zhang et al., 2025) `ev:asserted` p. 10 ^zhang2025reinflow-062
- In Kitchen-complete, entropy regularization with α = 0.1 raised success rate from 96.17 ± 3.65% to 99.00±0.75% over three seeds. (Zhang et al., 2025) `ev:measured` p. 34 ^zhang2025reinflow-063
- In Kitchen-complete, increasing the denoising step number K improves the reward at the beginning of fine-tuning. (Zhang et al., 2025) `ev:measured` p. 34 ^zhang2025reinflow-064
- During evaluation without injected noise, the authors observed that the reward is often higher than the noise-injected version. (Zhang et al., 2025) `ev:measured` p. 29 ^zhang2025reinflow-065
- The authors find clipping denoised actions beneficial during fine-tuning, since it helps prevent injected noise from disrupting the integration path. (Zhang et al., 2025) `ev:asserted` p. 29 ^zhang2025reinflow-066
- Critic warm-up before actor updates is described as crucial for stable training, particularly for larger models with visual inputs. (Zhang et al., 2025) `ev:asserted` p. 29 ^zhang2025reinflow-067
- The authors state that future work should explore a sample-efficient implementation of ReinFlow and its adaptation to real-world RL. (Zhang et al., 2025) `ev:asserted` p. 10 ^zhang2025reinflow-068
- Reducing ReinFlow's sensitivity to noise magnitude, or auto-tuning these hyperparameters, is named as an open direction by the authors. (Zhang et al., 2025) `ev:asserted` p. 10 ^zhang2025reinflow-069
- The experiments use relatively small networks, and scaling ReinFlow to large flow-based [[Vision-language-action models|vision-language-action models]] remains an open challenge. (Zhang et al., 2025) `ev:asserted` p. 10 ^zhang2025reinflow-070

## 🎯 Contributions

## 📖 Glossary

- **Flow matching policy** — Robot policy generating actions by integrating a learned velocity field from Gaussian noise.
- **Rectified Flow (1-ReFlow)** — Flow model with a straight-line path between noise and data samples.
- **Shortcut Model** — Flow variant trained so one large step matches two smaller steps.
- **Noise injection network** — Learnable network outputting bounded per-dimension noise std along the denoising path.
- **DPPO** — Diffusion Policy Policy Optimization; PPO fine-tuning of diffusion policies via a bilevel MDP.
- **FQL** — Flow Q-Learning; offline RL that distills a one-step flow policy against a Q function.
- **Per-symbol entropy rate** — Block entropy of a sequence divided by its length, used as regularizer.
- **Action chunking** — Policy outputs several future actions from one observation, executed open-loop.
- **Critic warm-up** — Training the critic for some iterations before updating the actor.

## ❓ Open questions

- Does ReinFlow transfer to real-robot online RL, where sample efficiency matters more than wall time?
- Can an off-policy variant (Eq. 11 with SAC) match PPO-based ReinFlow while using fewer samples?
- How can the noise std bounds σmin and σmax be auto-tuned or removed?
- Does the noise-net parameter overhead stay small when scaling to large flow-based VLA models such as π0?
- Why is ReinFlow-S slower per iteration than DPPO in Transport, and does the wall-time advantage hold for long-horizon visual tasks?
- Why does fine-tuning fail when the pre-trained success rate is very low (16-episode Square), and can exploration settings rescue it?

## 📝 Notes on reading

Version read: arXiv 2505.22094v7 (8 Jan 2026), marked as NeurIPS 2025 camera-ready; reference numbers in the PDF differ by one from the registry abstract (e.g. DPPO [42] vs [43]).

Inconsistencies: the wall-time saving versus DPPO is given as 82.63% (abstract, locomotion), 62.82% (introduction, all tasks) and over 50% (conclusion); the registry abstract's 23.20% computation-time saving for manipulation is not found in the body. Table 4a lists ReinFlow-S in Ant-v2 as 225.81%, identical to ReinFlow-R, although its values (2088.06 to 4106.31) imply about 97%; likely a copy error. Eq. (26) is garbled in extraction (Fine-tuned minus Fine-tuned over Pre-trained). Table 7b has four task columns but three values per row, so per-task Gym noise bounds could not be assigned. The paper names the ant environment Ant-v2 in main experiments and Ant-v0 in sensitivity analysis and Table 3, and Ant-v3 in Table 2. Section 4.4 says entropy regularization is default for state tasks, but Table 8 sets α = 0.00 for Franka Kitchen. In Fig. 6b the W2 coefficient is called β in text but α appears in the legend.

Figures only described: Fig. 1 (Gym wall-clock reward curves vs DPPO and FQL), Fig. 2 (Kitchen completion vs samples), Fig. 3 (Robomimic success vs samples, including a Gaussian baseline), Fig. 4 (scaling of data and steps; time distributions), Fig. 5 (noise conditioning), Fig. 6 (noise std sweep in Ant; W2 vs entropy in Humanoid), Figs. 11-12 (other diffusion RL baselines: DIPO, IDQL, DRWR, QSM, DQL, DAWR), Fig. 13 (Kitchen at K = 1, 2, 4). The NeurIPS checklist (pp. 15-21) was skipped.

## Suggested new concepts

- Noise-injected flow policy — a general recipe for making deterministic ODE policies tractable for policy gradients; likely reused by other flow-RL papers.
- Online RL fine-tuning of generative robot policies — umbrella concept linking ReinFlow, DPPO, FQL, Flow-GRPO and related methods.
- Policy gradient for Markov-process policies — the theorem that lets any multi-step stochastic action generator be optimized with PPO.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — RL para políticas de flujo con ruido aprendible (D.2).
