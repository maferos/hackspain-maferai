---
aliases: []
type: "source"
title: "SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning"
citekey: "Li2025simplevla"
doi: "10.48550/arXiv.2509.09674"
arxiv: "2509.09674"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2509.09674"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Haozhan Li", "Yuxin Zuo", "Jiale Yu", "Yuhao Zhang", "Zhaohui Yang", "Kaiyan Zhang", "Xuekai Zhu", "Yuchen Zhang", "Tianxing Chen", "Ganqu Cui", "Dehui Wang", "Dingxiang Luo", "Yuchen Fan", "Youbang Sun", "Jia Zeng", "Jiangmiao Pang", "Shanghang Zhang", "Yu Wang", "Yao Mu", "Bowen Zhou", "Ning Ding"]
sha256: ["c3f9c608ba58bb274dc6d093e78836603edfe3475278be19ff96b91b0654a3e5"]
pdf: "Content/Papers/Li2025simplevla.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Li2025simplevla.pdf]]

> [!abstract] One-sentence summary
> SimpleVLA-RL extends the veRL framework to online GRPO training of an OpenVLA-OFT policy with binary outcome rewards and exploration tweaks, lifting LIBERO and RoboTwin success rates, one-demonstration performance and sim-to-real transfer over SFT alone.

## Abstract

Vision-Language-Action (VLA) models have recently emerged as a powerful paradigm for robotic manipulation. Despite substantial progress enabled by large-scale pretraining and supervised fine-tuning (SFT), these models face two fundamental challenges: (i) the scarcity and high cost of large-scale human-operated robotic trajectories required for SFT scaling, and (ii) limited generalization to tasks involving distribution shift. Recent breakthroughs in Large Reasoning Models (LRMs) demonstrate that reinforcement learning (RL) can dramatically enhance step-by-step reasoning capabilities, raising a natural question: Can RL similarly improve the long-horizon step-by-step action planning of VLA? In this work, we introduce SimpleVLA-RL, an efficient RL framework tailored for VLA models. Building upon veRL, we introduce VLA-specific trajectory sampling, scalable parallelization, multi-environment rendering, and optimized loss computation. When applied to OpenVLA-OFT, SimpleVLA-RL achieves SoTA performance on LIBERO and even outperforms $π_0$ on RoboTwin 1.0\&2.0 with the exploration-enhancing strategies we introduce. SimpleVLA-RL not only reduces dependence on large-scale data and enables robust generalization, but also remarkably surpasses SFT in real-world tasks. Moreover, we identify a novel phenomenon ``pushcut'' during RL training, wherein the policy discovers previously unseen patterns beyond those seen in the previous training process. Github: https://github.com/PRIME-RL/SimpleVLA-RL (arXiv)

## 🧠 Key ideas (atomic)

- Scaling SFT for VLA models requires many more human-operated robot trajectories, which the authors describe as scarce and prohibitively expensive. (Li et al., 2025) `ev:asserted` p. 3 ^li2025simplevla-001
- Traditional RL methods for robotic tasks typically rely on hand-crafted process rewards, which the authors say severely limit scalability. (Li et al., 2025) `ev:cited` p. 3 ^li2025simplevla-002
- SimpleVLA-RL builds on veRL, a general-purpose LLM RL framework, adding VLA-specific interactive trajectory sampling for end-to-end online RL. (Li et al., 2025) `ev:reported` p. 3 ^li2025simplevla-003
- The authors extend veRL with parallel multi-environment rendering to obtain faster trajectory sampling for scalable VLA reinforcement learning. (Li et al., 2025) `ev:reported` p. 3 ^li2025simplevla-004
- The authors report that their exploration-enhancing strategies yield consistent performance improvements of 10–15% within the framework. (Li et al., 2025) `ev:measured` p. 4 ^li2025simplevla-005
- SimpleVLA-RL assigns each sampled trajectory a binary outcome reward, 1 for success or 0 for failure, from environment feedback. (Li et al., 2025) `ev:reported` p. 6 ^li2025simplevla-006
- SimpleVLA-RL adopts token-based action decoding, with the VLA outputting action token distributions sampled randomly to diversify trajectories. (Li et al., 2025) `ev:reported` p. 6 ^li2025simplevla-007
- The authors state that token-based action decoding is the approach most compatible with PPO-like RL algorithms among current VLA decoders. (Li et al., 2025) `ev:asserted` p. 6 ^li2025simplevla-008
- Trajectory-level rewards are propagated uniformly to the action tokens, so every token in a successful trajectory receives reward 1. (Li et al., 2025) `ev:reported` p. 7 ^li2025simplevla-009
- The authors observe that VLA models tend to converge on a narrow set of solution patterns, largely due to homogeneous training trajectories. (Li et al., 2025) `ev:asserted` p. 8 ^li2025simplevla-010
- Dynamic sampling excludes rollout groups in which all trajectories either succeed or fail, so batches consist solely of mixed-outcome groups. (Li et al., 2025) `ev:reported` p. 8 ^li2025simplevla-011
- When all trajectories in a group share identical rewards, GRPO advantage estimates become zero, resulting in null gradients. (Li et al., 2025) `ev:asserted` p. 8 ^li2025simplevla-012
- Following DAPO, the clipping range in the GRPO training objective is widened from [0.8, 1.2] to [0.8, 1.28]. (Li et al., 2025) `ev:reported` p. 8 ^li2025simplevla-013
- The rollout sampling temperature is increased from 1.0 to 1.6 to encourage the VLA model to generate more diverse trajectories. (Li et al., 2025) `ev:reported` p. 8 ^li2025simplevla-014
- The authors report that the three exploration modifications led to notable improvements in LIBERO-Long success rates during RL training. (Li et al., 2025) `ev:measured` p. 8 ^li2025simplevla-015
- Following DAPO, SimpleVLA-RL removes KL divergence regularization from the objective, which eliminates the need for a reference model. (Li et al., 2025) `ev:reported` p. 9 ^li2025simplevla-016
- The authors argue the KL penalty constrains policy divergence from a fixed reference, potentially limiting exploration of new behaviors. (Li et al., 2025) `ev:asserted` p. 9 ^li2025simplevla-017
- The RoboTwin2.0 evaluation uses 12 tasks grouped into four horizon levels, averaging 256 steps per task overall. (Li et al., 2025) `ev:reported` p. 9 ^li2025simplevla-018
- LIBERO performance is measured as the average success rate across 50 held-out test scenarios for each task. (Li et al., 2025) `ev:reported` p. 10 ^li2025simplevla-019
- RoboTwin2.0 experiments use the Agilex Piper robotic arm with [[Domain randomization|domain-randomized settings]], evaluating each task on 100 held-out test scenarios. (Li et al., 2025) `ev:reported` p. 10 ^li2025simplevla-020
- SimpleVLA-RL is applied to OpenVLA-OFT, which uses LLaMA2-7B as backbone with action chunking and parallel decoding designs. (Li et al., 2025) `ev:reported` p. 10 ^li2025simplevla-021
- The authors' OpenVLA-OFT variant takes only single-view images, language instructions and proprioceptive states, omitting the official wrist camera images. (Li et al., 2025) `ev:reported` p. 10 ^li2025simplevla-022
- Their variant generates action tokens with the LLaMA2 output head and cross-entropy loss, instead of the official MLP with L1 regression. (Li et al., 2025) `ev:reported` p. 10 ^li2025simplevla-023
- Due to these input and architecture differences, the authors could not use official checkpoints and performed SFT from scratch. (Li et al., 2025) `ev:reported` p. 10 ^li2025simplevla-024
- Full-parameter training runs on 8 x NVIDIA A800 80GB GPUs in the authors' training infrastructure. (Li et al., 2025) `ev:reported` p. 11 ^li2025simplevla-025
- Training uses a batch size of 64, a sampling count of 8, a mini-batch size of 128, with temperature 1.6. (Li et al., 2025) `ev:reported` p. 11 ^li2025simplevla-026
- During RL rollouts the policy uses random sampling, whereas evaluation uses greedy sampling with each benchmark tested three times. (Li et al., 2025) `ev:reported` p. 11 ^li2025simplevla-027
- For RoboTwin2.0, the authors use 1,000 demonstrations per task for SFT before RL on 1,000 scenarios per task. (Li et al., 2025) `ev:reported` p. 11 ^li2025simplevla-028
- On four LIBERO task suites, SimpleVLA-RL raises the average success rate of the SFT-tuned OpenVLA-OFT model from 91% to 99%. (Li et al., 2025) `ev:measured` p. 12 ^li2025simplevla-029
- In the LIBERO comparison table, OpenVLA-OFT with SimpleVLA-RL averages 99.1 success, compared with 95.2 for UniVLA. (Li et al., 2025) `ev:measured` p. 10 ^li2025simplevla-030
- On LIBERO-Long, SimpleVLA-RL reaches a 98.5% success rate, a 12% improvement over the 86.5% OpenVLA-OFT baseline. (Li et al., 2025) `ev:measured` p. 12 ^li2025simplevla-031
- On four RoboTwin1.0 dual-arm tasks, SimpleVLA-RL raises OpenVLA-OFT average success from 39.8% to 70.4%, a 30.6% gain. (Li et al., 2025) `ev:measured` p. 12 ^li2025simplevla-032
- Across 12 RoboTwin2.0 dual-arm tasks, SimpleVLA-RL lifts average success from 38.3% to 68.8%, an 80% relative improvement. (Li et al., 2025) `ev:measured` p. 12 ^li2025simplevla-033
- On RoboTwin2.0, the 68.8% average success of SimpleVLA-RL outperforms the 49.2% average reached by the π0 baseline. (Li et al., 2025) `ev:measured` p. 12 ^li2025simplevla-034
- SimpleVLA-RL gains 18.7% points on Put Bottles Dustbin, an extra-long-horizon RoboTwin2.0 task requiring multi-round dual-arm interaction. (Li et al., 2025) `ev:measured` p. 12 ^li2025simplevla-035
- In One-Trajectory SFT, OpenVLA-OFT is fine-tuned with one demonstration per task, merely 10 demonstrations per LIBERO task suite. (Li et al., 2025) `ev:reported` p. 12 ^li2025simplevla-036
- After One-Trajectory SFT plus SimpleVLA-RL, average LIBERO success rises from 48.9% to 96.9%, surpassing the 91% of Full-Trajectory SFT. (Li et al., 2025) `ev:measured` p. 13 ^li2025simplevla-037
- Under One-Trajectory SFT, LIBERO-Long success improves from 17.3% to 91.7% after SimpleVLA-RL is applied to the model. (Li et al., 2025) `ev:measured` p. 13 ^li2025simplevla-038
- The gap between One-Trajectory SFT plus RL at 96.9% and Full-Trajectory SFT plus RL at 99.1% is only 2.2%. (Li et al., 2025) `ev:measured` p. 13 ^li2025simplevla-039
- The authors suggest online RL with outcome feedback can enable further scaling of VLA training even with minimal demonstration data. (Li et al., 2025) `ev:asserted` p. 13 ^li2025simplevla-040
- For generalization tests, nine tasks per LIBERO suite are used for training while the remaining task is held out as unseen. (Li et al., 2025) `ev:reported` p. 13 ^li2025simplevla-041
- The original OpenVLA-OFT model achieves only 0% on LIBERO, so a One-Trajectory SFT base model is used before RL. (Li et al., 2025) `ev:reported` p. 13 ^li2025simplevla-042
- Both SFT and RL achieve over 90% success rates on training tasks, but their performance on unseen tasks diverges significantly. (Li et al., 2025) `ev:measured` p. 13 ^li2025simplevla-043
- SFT exhibits performance degradation on most unseen tasks, often with success rates dropping to 0% during training. (Li et al., 2025) `ev:measured` p. 13 ^li2025simplevla-044
- On LIBERO-Goal's three unseen tasks, SFT success rates immediately drop to 0% at the beginning of training. (Li et al., 2025) `ev:measured` p. 13 ^li2025simplevla-045
- The authors suggest SFT's LIBERO-Goal failure may stem from diverse objects and strategies with few transferable components across tasks. (Li et al., 2025) `ev:asserted` p. 14 ^li2025simplevla-046
- On LIBERO-Goal, SimpleVLA-RL avoids performance degradation and achieves 5%-15% improvements on the three unseen tasks. (Li et al., 2025) `ev:measured` p. 14 ^li2025simplevla-047
- On LIBERO-Object Unseen Task 3, SFT improves from 57.8% to 74.6% but fails on the other two unseen tasks. (Li et al., 2025) `ev:measured` p. 14 ^li2025simplevla-048
- On LIBERO-Object, SimpleVLA-RL gains 36.5% on Unseen Task 2 and 16.4% on Unseen Task 3. (Li et al., 2025) `ev:measured` p. 14 ^li2025simplevla-049
- On LIBERO-Spatial, SFT degrades by 10% on Unseen Task 1 and completely fails on the remaining unseen tasks. (Li et al., 2025) `ev:measured` p. 14 ^li2025simplevla-050
- On LIBERO-Spatial Unseen Task 1, SimpleVLA-RL improves unseen-task performance from 43.3% to 71.8% over the course of training. (Li et al., 2025) `ev:measured` p. 14 ^li2025simplevla-051
- [[Sim-to-real transfer|Sim-to-real experiments]] run OpenVLA-OFT on two AgileX Piper robotic arms, with RDT serving as the baseline model. (Li et al., 2025) `ev:reported` p. 14 ^li2025simplevla-052
- Real-world policies use 1000 simulation trajectories for SFT plus RL on 1000 simulation scenarios, without any real-world demonstrations. (Li et al., 2025) `ev:reported` p. 15 ^li2025simplevla-053
- Each real-world task is tested with 50 trials on clean tabletops that have backgrounds unseen during training. (Li et al., 2025) `ev:reported` p. 15 ^li2025simplevla-054
- In the sim2real tests, SimpleVLA-RL raises average real-world success from 17.5% to 38.5%, surpassing the 23.5% of RDT. (Li et al., 2025) `ev:measured` p. 15 ^li2025simplevla-055
- In the real-world Stack Bowls task, SimpleVLA-RL reaches 70% success, outperforming the RDT baseline at 60%. (Li et al., 2025) `ev:measured` p. 15 ^li2025simplevla-056
- On the real-world Pick Bottle task, the SFT model fails completely, whereas SimpleVLA-RL achieves a 15% success rate. (Li et al., 2025) `ev:measured` p. 15 ^li2025simplevla-057
- In the RoboTwin2.0 move can pot task, demonstrations follow grasp–move–place, yet the RL-trained policy pushes the can into place. (Li et al., 2025) `ev:measured` p. 15 ^li2025simplevla-058
- The authors call this emergent push-driven shortcut 'pushcut', a behavior absent from the demonstration data used for training. (Li et al., 2025) `ev:asserted` p. 15 ^li2025simplevla-059
- In the place a2b left/right task, the RL-trained model pushes Object A into position instead of grasping it. (Li et al., 2025) `ev:measured` p. 16 ^li2025simplevla-060
- The authors argue outcome-level rewards promote such strategies because grasping and pushing yield equivalent rewards upon successful completion. (Li et al., 2025) `ev:asserted` p. 16 ^li2025simplevla-061
- The OpenVLA-OFT base model without trajectory fine-tuning achieves a 0% success rate across all five RoboTwin2.0 failure-mode tasks. (Li et al., 2025) `ev:measured` p. 16 ^li2025simplevla-062
- Without successful rollouts, every trajectory receives zero outcome reward, leaving RL unable to improve performance beyond 0% success. (Li et al., 2025) `ev:measured` p. 16 ^li2025simplevla-063
- The 100-trajectory SFT model improves average success from 7.3% to 25.4% after SimpleVLA-RL on five RoboTwin2.0 tasks. (Li et al., 2025) `ev:measured` p. 16 ^li2025simplevla-064
- The 1000-trajectory SFT model improves average success from 28.2% to 50.4% after SimpleVLA-RL, a 22.2% gain. (Li et al., 2025) `ev:measured` p. 16 ^li2025simplevla-065
- In the pick dual bottles task, the 100-trajectory SFT model improves from 1.2% to 4.3% with RL, a marginal gain. (Li et al., 2025) `ev:measured` p. 17 ^li2025simplevla-066
- The authors conclude that a minimal level of task competence is essential, below which exploration is ineffective for RL. (Li et al., 2025) `ev:asserted` p. 17 ^li2025simplevla-067
- The authors state they publicly released the SimpleVLA-RL code in May 2025 as an early systematic exploration of VLA online RL. (Li et al., 2025) `ev:asserted` p. 18 ^li2025simplevla-068

## 🎯 Contributions

## 📖 Glossary

- **VLA** — Vision-Language-Action model mapping images and language instructions to robot actions.
- **GRPO** — Group Relative Policy Optimization; critic-free RL normalizing rewards within a group of rollouts.
- **Dynamic sampling** — Discarding rollout groups whose trajectories all succeed or all fail.
- **Clip-Higher** — Asymmetric PPO clipping with a larger upper bound to encourage exploration.
- **Outcome reward** — Binary trajectory-level reward based solely on task success.
- **Action chunk** — Sequence of k actions predicted at once and executed before re-observing.
- **One-Trajectory SFT** — Supervised fine-tuning with a single demonstration per task.
- **Pushcut** — Emergent RL behavior pushing objects instead of the demonstrated grasp-move-place.
- **veRL** — Volcano Engine Reinforcement Learning, a general-purpose RL framework for LLMs.

## ❓ Open questions

- Does the outcome-reward recipe transfer to diffusion-based or flow-matching VLA decoders that lack explicit token distributions?
- How can RL be bootstrapped when the SFT prior has near-zero success, e.g. with process rewards or curricula?
- Would RL directly on real robots add further gains over simulation-only RL for sim-to-real transfer?
- How sensitive are the results to the modified OpenVLA-OFT variant (single view, token head) versus the official model?
- Is the pushcut behaviour always desirable, or can it violate task constraints not captured by the binary reward?

## 📝 Notes on reading

- Version read: arXiv v1 (2509.09674v1, 11 Sep 2025), matching the packet identifier.
- Figure 3 (p. 8) shows LIBERO-Long training curves annotated with roughly 15% (dynamic sampling), 10% (clip higher) and 15% (higher temperature) gains; only described here.
- Figure 4 (p. 14) plots unseen-task vs seen-task success for SFT and RL per LIBERO suite; described only.
- Inconsistency: the contributions list (p. 4) says LIBERO-Long one-demonstration success rises from 17.1% to 91.7%, while Table 5 and the text (p. 13) give 17.3%.
- Inconsistency: the sim-to-real text (p. 14) lists Stack Bowls, Handover Block, Pick Bottle and Click Bell, but Table 6 lists Place Empty Cup instead of Handover Block.
- Inconsistency: the text (p. 15) says Stack Bowls rises from 32% to 70% (a 96% relative improvement), but Table 6 gives the OpenVLA-OFT SFT value as 38.0; Pick Bottle is 15% in the text versus 14.0 in the table.
- Table 4 headers give short horizon as 100-130 steps, whereas Table 1 gives 112-130 steps; Table 7 labels a column 'Place A2B Lift', likely a typo for Left.
- The OpenVLA-OFT baseline in all comparisons is the authors' own re-trained variant (single view, token head), not the official checkpoint.

## Suggested new concepts

- Outcome-reward RL for VLA policies — a recurring recipe (GRPO, binary success reward) that several VLA RL works build on.
- Dynamic sampling — a generic fix for zero-advantage groups in critic-free RL, used in both LLM and VLA training.
- Sim-to-real transfer via simulation RL — relevant to training real-robot policies from simulated lab scenes.
- Emergent behaviour under sparse rewards (pushcut) — policies discovering strategies absent from demonstrations.
- SFT prior threshold for RL — minimal task competence needed before outcome-reward RL helps.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H4.** RL con recompensa de resultado sobre OpenVLA-OFT que supera al SFT y descubre comportamientos nuevos, una vía para ir más allá de las demostraciones.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
