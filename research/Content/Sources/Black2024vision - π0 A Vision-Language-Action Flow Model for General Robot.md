---
aliases: []
type: "source"
title: "π0: A Vision-Language-Action Flow Model for General Robot Control"
citekey: "Black2024vision"
doi: "10.48550/arXiv.2410.24164"
arxiv: "2410.24164"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2410.24164"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Kevin Black", "Noah Brown", "Danny Driess", "Adnan Esmail", "Michael Equi", "Chelsea Finn", "Niccolo Fusai", "Lachy Groom", "Karol Hausman", "Brian Ichter", "Szymon Jakubczak", "Tim Jones", "Liyiming Ke", "Sergey Levine", "Adrian Li-Bell", "Mohith Mothukuri", "Suraj Nair", "Karl Pertsch", "Lucy Xiaoyang Shi", "James Tanner", "Quan Vuong", "Anna Walling", "Haohuan Wang", "Ury Zhilinsky"]
sha256: ["fbdfba56258bdbd220207ba63410c6c943e43a73e97a7a5a47ca0bc74204f821"]
pdf: "Content/Papers/Black2024vision.pdf"
topics: ["[[Optimización y algoritmos]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 59
---

📄 PDF: [[Black2024vision.pdf]]

> [!abstract] One-sentence summary
> π0 attaches a flow matching action expert to a pre-trained PaliGemma VLM and trains it on a large cross-embodiment robot mixture, showing that pre-training plus curated post-training yields dexterous, long-horizon manipulation such as laundry folding and box assembly.

## Abstract

Robot learning holds tremendous promise to unlock the full potential of flexible, general, and dexterous robot systems, as well as to address some of the deepest questions in artificial intelligence. However, bringing robot learning to the level of generality required for effective real-world systems faces major obstacles in terms of data, generalization, and robustness. In this paper, we discuss how generalist robot policies (i.e., robot foundation models) can address these challenges, and how we can design effective generalist robot policies for complex and highly dexterous tasks. We propose a novel flow matching architecture built on top of a pre-trained vision-language model (VLM) to inherit Internet-scale semantic knowledge. We then discuss how this model can be trained on a large and diverse dataset from multiple dexterous robot platforms, including single-arm robots, dual-arm robots, and mobile manipulators. We evaluate our model in terms of its ability to perform tasks in zero shot after pre-training, follow language instructions from people and from a high-level VLM policy, and its ability to acquire new skills via fine-tuning. Our results cover a wide variety of tasks, such as laundry folding, table cleaning, and assembling boxes. (arXiv)

## 🧠 Key ideas (atomic)

- π0 adds [[Flow matching policy|flow matching action outputs]] to the pre-trained PaliGemma vision-language model to generate continuous action distributions for robot control. (Black et al., 2024) `ev:reported` p. 4 ^black2024vision-001
- The authors state that π0 can control robots at frequencies of up to 50 Hz for dexterous tasks such as laundry folding. (Black et al., 2024) `ev:asserted` p. 3 ^black2024vision-002
- π0 uses an [[Action chunking|action chunking]] architecture with [[Flow matching policy|flow matching]], a variant of diffusion, to represent complex continuous action distributions. (Black et al., 2024) `ev:reported` p. 3 ^black2024vision-003
- [[Vision-language-action models|Prior vision-language-action models]] employ [[Action tokenization|autoregressive discretization]] to represent actions in a manner analogous to text tokens. (Black et al., 2024) `ev:cited` p. 3 ^black2024vision-004
- The authors describe π0 as, to their knowledge, the first flow matching [[Vision-language-action models|VLA]] that produces high-frequency action chunks for dexterous control. (Black et al., 2024) `ev:asserted` p. 3 ^black2024vision-005
- Prior dexterous tasks were typically studied at smaller scale, with 10s or 100s of training trajectories equivalent to 10 or less hours. (Black et al., 2024) `ev:cited` p. 3 ^black2024vision-006
- The pre-training mixture combines the authors' own dexterous datasets from 7 robot configurations and 68 tasks with the entire OXE dataset. (Black et al., 2024) `ev:reported` p. 4 ^black2024vision-007
- According to the authors, [[Open X-Embodiment dataset|the OXE dataset]] included in the pre-training mixture contains robot data collected from 22 different robots. (Black et al., 2024) `ev:reported` p. 4 ^black2024vision-008
- The authors describe the pre-trained base model as following language commands and performing a variety of tasks at rudimentary proficiency. (Black et al., 2024) `ev:asserted` p. 4 ^black2024vision-009
- The authors state that using a separate set of weights for robotics-specific action and state tokens led to improved performance. (Black et al., 2024) `ev:asserted` p. 4 ^black2024vision-010
- π0 models the distribution of action chunks conditioned on an observation, using an action horizon of H = 50 for the tasks. (Black et al., 2024) `ev:reported` p. 5 ^black2024vision-011
- Each observation comprises 2 or 3 RGB images per robot, a language command, and a vector of proprioceptive joint angles. (Black et al., 2024) `ev:reported` p. 5 ^black2024vision-012
- At inference, π0 integrates the learned vector field with forward Euler using 10 integration steps, corresponding to δ = 0.1. (Black et al., 2024) `ev:reported` p. 5 ^black2024vision-013
- PaliGemma, an open-source 3 billion parameter VLM, is combined with an action expert of 300M parameters for 3.3 billion parameters total. (Black et al., 2024) `ev:reported` p. 5 ^black2024vision-014
- The π0-small baseline has 470M parameters and does not use VLM initialization, serving to evaluate the benefits of VLM pre-training. (Black et al., 2024) `ev:reported` p. 5 ^black2024vision-015
- 9.1% of the pre-training mixture, counted in timesteps, consists of open-source datasets including [[Open X-Embodiment dataset|OXE]], Bridge v2, and DROID. (Black et al., 2024) `ev:reported` p. 5 ^black2024vision-016
- The authors' own datasets contribute 903M timesteps, of which 106M come from single-arm robots and 797M from dual-arm robots. (Black et al., 2024) `ev:reported` p. 6 ^black2024vision-017
- Each task-robot combination is weighted by n to the power 0.43, where n is its sample count, to down-weight over-represented combinations. (Black et al., 2024) `ev:reported` p. 6 ^black2024vision-018
- Configuration and action vectors are zero-padded to 18 dimensions, the dimensionality of the largest robot in the dataset. (Black et al., 2024) `ev:reported` p. 6 ^black2024vision-019
- Post-training datasets vary by task, from only 5 hours for the simplest tasks to 100 or more hours for the most complex. (Black et al., 2024) `ev:reported` p. 6 ^black2024vision-020
- A high-level VLM policy can decompose tasks such as bussing a table into immediate language subtasks, analogous to SayCan planning. (Black et al., 2024) `ev:reported` p. 6 ^black2024vision-021
- The base model was evaluated without post-training on shirt folding, easy and hard bussing, grocery bagging, and toast removal. (Black et al., 2024) `ev:reported` p. 7 ^black2024vision-022
- Baselines were OpenVLA, a 7B parameter VLA, and Octo, a 93M parameter diffusion-based model, both trained on the same mixture. (Black et al., 2024) `ev:reported` p. 7 ^black2024vision-023
- A compute-parity π0 variant was trained for 160k steps, compared with 700k steps for the main model. (Black et al., 2024) `ev:reported` p. 7 ^black2024vision-024
- Out-of-box scores are normalized and averaged over 10 episodes per task and method, with partial credit for partial success. (Black et al., 2024) `ev:reported` p. 7 ^black2024vision-025
- In out-of-box evaluation, π0 attains the best results on all five tasks, with large improvements over all baselines. (Black et al., 2024) `ev:measured` p. 7 ^black2024vision-026
- Out-of-box, π0 reaches near perfect success rates on shirt folding and on the easier bussing tasks. (Black et al., 2024) `ev:measured` p. 7 ^black2024vision-027
- The parity version of π0, trained for only 160k steps, still outperforms all baselines in the out-of-box tasks. (Black et al., 2024) `ev:measured` p. 7 ^black2024vision-028
- Even π0-small outperforms OpenVLA and Octo in the out-of-box evaluation, although it lacks the VLM pre-training used by the full π0 model. (Black et al., 2024) `ev:measured` p. 7 ^black2024vision-029
- The authors attribute OpenVLA's struggles to its autoregressive discretization architecture, which does not support action chunks. (Black et al., 2024) `ev:asserted` p. 7 ^black2024vision-030
- An OpenVLA model fine-tuned only on UR5e data performs better than cross-embodiment OpenVLA, but remains far below π0. (Black et al., 2024) `ev:measured` p. 7 ^black2024vision-031
- Language-following accuracy of π0 was significantly better than that of π0-small, averaged over 10 trials per task. (Black et al., 2024) `ev:measured` p. 8 ^black2024vision-032
- The authors suggest this language-following gain reflects a significant improvement from the larger pre-trained VLM initialization. (Black et al., 2024) `ev:asserted` p. 8 ^black2024vision-033
- π0 performance improves with intermediate commands from an expert human and, to a lesser degree, from an autonomous high-level policy. (Black et al., 2024) `ev:measured` p. 9 ^black2024vision-034
- Due to its limited language following ability, π0-small overall does not gain from the addition of a high-level expert. (Black et al., 2024) `ev:measured` p. 9 ^black2024vision-035
- Fine-tuning tasks were grouped into tiers by how much they differ from pre-training, from easy stack bowls to hard paper towel replacement. (Black et al., 2024) `ev:reported` p. 9 ^black2024vision-036
- Fine-tuned π0 was compared with OpenVLA and Octo checkpoints, and with ACT and Diffusion Policy trained only on fine-tuning data. (Black et al., 2024) `ev:reported` p. 9 ^black2024vision-037
- Across fine-tuning tasks averaged over 10 trials each, π0 generally outperforms the other methods at varying fine-tuning data amounts. (Black et al., 2024) `ev:measured` p. 9 ^black2024vision-038
- The strongest prior models in fine-tuning are those trained entirely from scratch on the target tasks. (Black et al., 2024) `ev:measured` p. 9 ^black2024vision-039
- On the Tupperware in microwave task, the π0 policy fine-tuned on 5 hours performs similarly to the baselines. (Black et al., 2024) `ev:measured` p. 9 ^black2024vision-040
- On the Tupperware in microwave task, the 1-hour π0 policy is significantly better than the baselines. (Black et al., 2024) `ev:measured` p. 9 ^black2024vision-041
- Pre-training yields larger improvements for tasks that are more similar to the pre-training data, as the authors expected. (Black et al., 2024) `ev:measured` p. 9 ^black2024vision-042
- The pre-trained π0 is frequently better than the non-pre-trained model, sometimes by as much as 2x. (Black et al., 2024) `ev:measured` p. 10 ^black2024vision-043
- Table bussing, box building, to-go box, and packing eggs are complex tasks with no data present in pre-training. (Black et al., 2024) `ev:reported` p. 10 ^black2024vision-044
- The authors were not able to solve these complex tasks with other methods, so they compared against ablations of π0. (Black et al., 2024) `ev:reported` p. 11 ^black2024vision-045
- On complex tasks, the full pre-training and fine-tuning recipe performs best across the board compared with out-of-box and scratch ablations. (Black et al., 2024) `ev:measured` p. 11 ^black2024vision-046
- The full pre-trained π0 model attains more than 50% of the maximum score across all complex tasks, averaged over 10 trials. (Black et al., 2024) `ev:measured` p. 11 ^black2024vision-047
- Many of the more difficult tasks show a very large improvement from the pre-trained model, indicating pre-training is especially useful there. (Black et al., 2024) `ev:measured` p. 11 ^black2024vision-048
- The authors believe this autonomous performance on challenging tasks represents a new state of the art in learned dexterous manipulation. (Black et al., 2024) `ev:asserted` p. 11 ^black2024vision-049
- The fine-tuning experiments include over 20 tasks, where π0 outperforms prior VLA models and dexterous manipulation-specific baselines. (Black et al., 2024) `ev:measured` p. 11 ^black2024vision-050
- Training only on high-quality post-training data yields a brittle model that does not reliably recover from mistakes, the authors state. (Black et al., 2024) `ev:asserted` p. 12 ^black2024vision-051
- The authors state that how pre-training datasets should be composed and weighted remains an open problem. (Black et al., 2024) `ev:asserted` p. 12 ^black2024vision-052
- The authors acknowledge that not all tasks in their evaluation work reliably with the π0 framework. (Black et al., 2024) `ev:asserted` p. 12 ^black2024vision-053
- It remains unclear how to predict how much and what kind of data is needed for near-perfect performance. (Black et al., 2024) `ev:asserted` p. 12 ^black2024vision-054
- Whether universality extends to distinct domains such as autonomous driving, navigation, and legged locomotion is left to future work. (Black et al., 2024) `ev:asserted` p. 12 ^black2024vision-055
- The action expert is downsized to width 1024 and mlp dim 4096, giving about 300M parameters, to speed up inference. (Black et al., 2024) `ev:reported` p. 15 ^black2024vision-056
- The flow matching timestep is sampled from a shifted beta distribution emphasizing noisier timesteps, with cutoff s = 0.999. (Black et al., 2024) `ev:reported` p. 16 ^black2024vision-057
- Temporal ensembling of [[Action chunking|action chunks]] hurt policy performance in early trials, so chunks are executed open-loop without aggregation. (Black et al., 2024) `ev:measured` p. 16 ^black2024vision-058
- Total on-board inference with 3 camera images takes 73 ms on an NVIDIA GeForce RTX 4090 GPU. (Black et al., 2024) `ev:measured` p. 16 ^black2024vision-059

## 🎯 Contributions

## 📖 Glossary

- **Vision-language-action (VLA) model** — a pre-trained VLM further trained to output robot actions.
- **Flow matching** — diffusion variant that learns a vector field transporting noise to data.
- **Action chunk** — a sequence of H future actions predicted at once from one observation.
- **Action expert** — separate transformer weights processing robot state and action tokens alongside the VLM.
- **Cross-embodiment training** — training one model on data from many robot types with different action spaces.
- **OXE (Open X-Embodiment)** — open-source aggregate of robot manipulation datasets from many robots.
- **Post-training** — fine-tuning a pre-trained base model on curated, task-specific high-quality data.
- **π0-small** — 470M-parameter non-VLM baseline used to isolate the value of VLM pre-training.

## ❓ Open questions

- How should the pre-training mixture be composed, and which data types should be added or weighted more?
- How much and what kind of data is needed to reach near-perfect performance on a given task?
- How much positive transfer arises from combining data across very different tasks and robots?
- Does the universality of robot foundation models extend to autonomous driving, navigation, and legged locomotion?
- How much of the π0 versus π0-small gap is due to VLM pre-training rather than model size?

## 📝 Notes on reading

Version read: arXiv 2410.24164v4 (8 Jan 2026). The registry abstract (earlier version) says the model is evaluated on tasks in zero shot after pre-training; the v4 PDF abstract says via direct prompting instead.

Figures 1, 3 and 4 were extracted as garbled glyphs; their content was taken only from the captions. Figures 7, 9, 11 and 13 are bar and line plots whose per-task, per-method values are not in the cached text, so no per-task scores were claimed; only the prose summaries were used.

Inconsistencies inside the paper: the pre-training data are described as over 10,000 hours (p. 3), about 10,000 hours (p. 3) and 10,000 hours (p. 11). Page 12 writes laundry following where laundry folding is meant; page 5 writes pertaining for pre-training; Appendix E writes dyer for dryer. The Appendix E rubric for complex table bussing is worded identically to the out-of-box bussing hard rubric. The flow matching loss and embedding equations (pp. 5 and 15) were extracted with broken sub- and superscripts and were described, not quoted.

The OpenVLA and Octo out-of-box baselines were trained for fewer steps than π0 (time constraints), which the compute-parity variant is meant to address; the π0-small comparison is confounded by model size, as the authors acknowledge.

## Suggested new concepts

- Flow matching policies for robot control — recurring alternative to autoregressive action tokenization and diffusion policies across VLA work.
- Action expert (mixture-of-experts VLA) — a design pattern for grafting continuous action heads onto pre-trained VLMs.
- Cross-embodiment pre-training — central data strategy for generalist robot policies spanning many robot configurations.
- Pre-training/post-training recipe for robot foundation models — the paper's framing of data quality versus diversity, reusable across policies.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — VLA con *action expert* de flow matching (D.1).
- **[[03_aplicaciones_vision_por_computador]]** — VLA con *flow matching*, evaluado en AutoBio

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
