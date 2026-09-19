---
aliases: []
type: "source"
title: "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control"
citekey: "Brohan2023rt"
doi: "10.48550/arXiv.2307.15818"
arxiv: "2307.15818"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2307.15818"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Anthony Brohan", "Noah Brown", "Justice Carbajal", "Yevgen Chebotar", "Xi Chen", "Krzysztof Choromanski", "Tianli Ding", "Danny Driess", "Avinava Dubey", "Chelsea Finn", "Pete Florence", "Chuyuan Fu", "Montse Gonzalez Arenas", "Keerthana Gopalakrishnan", "Kehang Han", "Karol Hausman", "Alexander Herzog", "Jasmine Hsu", "Brian Ichter", "Alex Irpan", "Nikhil Joshi", "Ryan Julian", "Dmitry Kalashnikov", "Yuheng Kuang", "Isabel Leal", "Lisa Lee", "Tsang-Wei Edward Lee", "Sergey Levine", "Yao Lu", "Henryk Michalewski", "Igor Mordatch", "Karl Pertsch", "Kanishka Rao", "Krista Reymann", "Michael Ryoo", "Grecia Salazar", "Pannag Sanketi", "Pierre Sermanet", "Jaspiar Singh", "Anikait Singh", "Radu Soricut", "Huong Tran", "Vincent Vanhoucke", "Quan Vuong", "Ayzaan Wahid", "Stefan Welker", "Paul Wohlhart", "Jialin Wu", "Fei Xia", "Ted Xiao", "Peng Xu", "Sichun Xu", "Tianhe Yu", "Brianna Zitkovich"]
sha256: ["0a62dc36bbbfdea232ad45a0ab75c82e9cf535b55333ff22c02d5da1897ccac3"]
pdf: "Content/Papers/Brohan2023rt.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 59
---

📄 PDF: [[Brohan2023rt.pdf]]

> [!abstract] One-sentence summary
> RT-2 co-fine-tunes large web-pretrained vision-language models (PaLI-X, PaLM-E) to emit robot actions as text tokens, roughly doubling generalization over RT-1 and transferring semantic, symbolic and reasoning abilities to real-robot control without new motions.

## Abstract

We study how vision-language models trained on Internet-scale data can be incorporated directly into end-to-end robotic control to boost generalization and enable emergent semantic reasoning. Our goal is to enable a single end-to-end trained model to both learn to map robot observations to actions and enjoy the benefits of large-scale pretraining on language and vision-language data from the web. To this end, we propose to co-fine-tune state-of-the-art vision-language models on both robotic trajectory data and Internet-scale vision-language tasks, such as visual question answering. In contrast to other approaches, we propose a simple, general recipe to achieve this goal: in order to fit both natural language responses and robotic actions into the same format, we express the actions as text tokens and incorporate them directly into the training set of the model in the same way as natural language tokens. We refer to such category of models as vision-language-action models (VLA) and instantiate an example of such a model, which we call RT-2. Our extensive evaluation (6k evaluation trials) shows that our approach leads to performant robotic policies and enables RT-2 to obtain a range of emergent capabilities from Internet-scale training. This includes significantly improved generalization to novel objects, the ability to interpret commands not present in the robot training data (such as placing an object onto a particular number or icon), and the ability to perform rudimentary reasoning in response to user commands (such as picking up the smallest or largest object, or the one closest to another object). We further show that incorporating chain of thought reasoning allows RT-2 to perform multi-stage semantic reasoning, for example figuring out which object to pick up for use as an improvised hammer (a rock), or which type of drink is best suited for someone who is tired (an energy drink). (arXiv)

## 🧠 Key ideas (atomic)

- The paper asks whether large pretrained vision-language models can be integrated directly into low-level robotic control to boost generalization. (Brohan et al., 2023) `ev:asserted` p. 2 ^brohan2023rt-001
- Prior works incorporating language and vision-language models into robotics generally address only high-level planning, leaving execution to separate low-level controllers. (Brohan et al., 2023) `ev:cited` p. 2 ^brohan2023rt-002
- RT-2 trains pre-existing vision-language models without any new parameters to output [[Action tokenization|robot actions encoded as text]]. (Brohan et al., 2023) `ev:asserted` p. 2 ^brohan2023rt-003
- RT-2 builds on the RT-1 protocol with a similar dataset but expands the model to a large vision-language backbone. (Brohan et al., 2023) `ev:reported` p. 2 ^brohan2023rt-004
- RT-2 adapts two previously proposed VLMs, PaLI-X and PaLM-E, into the variants RT-2-PaLI-X and RT-2-PaLM-E. (Brohan et al., 2023) `ev:reported` p. 5 ^brohan2023rt-005
- The action space comprises 6-DoF end-effector displacement, gripper extension, and a discrete command for terminating the episode. (Brohan et al., 2023) `ev:reported` p. 5 ^brohan2023rt-006
- Continuous action dimensions are discretized uniformly into 256 bins, so each action is represented as 8 integer numbers. (Brohan et al., 2023) `ev:reported` p. 5 ^brohan2023rt-007
- For PaLM-E, the 256 least frequently used tokens are overwritten to represent the action vocabulary. (Brohan et al., 2023) `ev:reported` p. 6 ^brohan2023rt-008
- Robot inputs pair a camera image with a standard VQA prompt asking what action the robot should take for the task instruction. (Brohan et al., 2023) `ev:reported` p. 6 ^brohan2023rt-009
- RT-2 is co-fine-tuned on robot data together with the original web data, rather than fine-tuned on robot data only. (Brohan et al., 2023) `ev:reported` p. 6 ^brohan2023rt-010
- During co-fine-tuning, robot and web data ratios in each batch are balanced by increasing the sampling weight on robot data. (Brohan et al., 2023) `ev:reported` p. 6 ^brohan2023rt-011
- When prompted with a robot-action task, RT-2 decoding is constrained to sample only valid [[Action tokenization|action tokens]]. (Brohan et al., 2023) `ev:reported` p. 6 ^brohan2023rt-012
- RT-2 models run on robots by deployment in a multi-TPU cloud service queried over the network. (Brohan et al., 2023) `ev:reported` p. 6 ^brohan2023rt-013
- The largest evaluated model, RT-2-PaLI-X-55B, can run at a control frequency of 1-3 Hz through the cloud service. (Brohan et al., 2023) `ev:measured` p. 6 ^brohan2023rt-014
- The smaller 5B-parameter version of RT-2-PaLI-X can run at a control frequency of around 5 Hz. (Brohan et al., 2023) `ev:measured` p. 6 ^brohan2023rt-015
- The authors state that RT-2, at 55B parameters, is to their knowledge the largest model ever used for direct closed-loop robotic control. (Brohan et al., 2023) `ev:asserted` p. 6 ^brohan2023rt-016
- The evaluated RT-2 instantiations are built from PaLI-X at 5B and 55B parameters and from PaLM-E at 12B. (Brohan et al., 2023) `ev:reported` p. 7 ^brohan2023rt-017
- The robot demonstration data from RT-1 were collected with 13 robots over 17 months in an office kitchen environment. (Brohan et al., 2023) `ev:cited` p. 7 ^brohan2023rt-018
- The approach and baselines are evaluated with about 6,000 evaluation trajectories on a 7DoF mobile manipulator. (Brohan et al., 2023) `ev:reported` p. 7 ^brohan2023rt-019
- Baselines are RT-1, a 35M parameter transformer, VC-1 and R3M representations on an RT-1 backbone, and MOO. (Brohan et al., 2023) `ev:reported` p. 7 ^brohan2023rt-020
- The unseen evaluations comprise over 280 tasks, mainly pick and place, split into unseen objects, backgrounds and environments with easy and hard cases. (Brohan et al., 2023) `ev:reported` p. 8 ^brohan2023rt-021
- On seen tasks, performance of the RT-2 models is similar to RT-1, with other baselines attaining lower success rates. (Brohan et al., 2023) `ev:measured` p. 8 ^brohan2023rt-022
- On average over generalization evaluations, both RT-2 instantiations give about a 2x improvement over RT-1 and MOO. (Brohan et al., 2023) `ev:measured` p. 8 ^brohan2023rt-023
- Averaged over generalization evaluations, both RT-2 instantiations perform about 6x better than the R3M and VC-1 baselines. (Brohan et al., 2023) `ev:measured` p. 8 ^brohan2023rt-024
- According to the authors, RT-2-PaLM-E seems to outperform RT-2-PaLI-X in the harder versions of the generalization scenarios. (Brohan et al., 2023) `ev:measured` p. 8 ^brohan2023rt-025
- RT-2-PaLM-E under-performs RT-2-PaLI-X on the easier generalization scenarios, giving the two models a similar average performance overall. (Brohan et al., 2023) `ev:measured` p. 8 ^brohan2023rt-026
- The authors suggest the strength of [[Vision-language-action models|VLA models]] lies in transferring generalizable visual and semantic concepts from Internet-scale pretraining data. (Brohan et al., 2023) `ev:asserted` p. 8 ^brohan2023rt-027
- On seen tasks, success rates were 91 for RT-2-PaLI-X-55B, 93 for RT-2-PaLM-E-12B, and 92 for RT-1. (Brohan et al., 2023) `ev:measured` p. 23 ^brohan2023rt-028
- Both RT-2 models reach an unseen-average success rate of 62, compared with 35 for MOO and 32 for RT-1. (Brohan et al., 2023) `ev:measured` p. 23 ^brohan2023rt-029
- In Table 4, the R3M and VC-1 baselines reach unseen-average success rates of 12 and 10 respectively. (Brohan et al., 2023) `ev:measured` p. 23 ^brohan2023rt-030
- On hard unseen environments, success rates are 35 for RT-2-PaLI-X-55B and 33 for RT-2-PaLM-E-12B, versus 14 for RT-1. (Brohan et al., 2023) `ev:measured` p. 23 ^brohan2023rt-031
- On hard unseen objects, success rates are 76 for RT-2-PaLM-E-12B and 62 for RT-2-PaLI-X-55B, versus 43 for RT-1. (Brohan et al., 2023) `ev:measured` p. 23 ^brohan2023rt-032
- On hard unseen backgrounds, success rates are 71 for RT-2-PaLM-E-12B, 48 for RT-2-PaLI-X-55B, and 9 for RT-1. (Brohan et al., 2023) `ev:measured` p. 23 ^brohan2023rt-033
- The PaLM-E-12B pretraining mixture includes robot images for high-level VQA planning, but none include the low-level actions evaluated. (Brohan et al., 2023) `ev:reported` p. 24 ^brohan2023rt-034
- On the open-source Language-Table simulation benchmark, a smaller PaLI 3B model is co-fine-tuned on several prediction tasks including in-domain VQA. (Brohan et al., 2023) `ev:reported` p. 8 ^brohan2023rt-035
- For Language-Table, actions are encoded as text 'X Y' with values from -10 to +10 representing delta 2D Cartesian end-effector setpoints. (Brohan et al., 2023) `ev:reported` p. 8 ^brohan2023rt-036
- On simulated Language-Table tasks, RT-2-PaLI-3B scores 90 ± 10, against 77 ± 4 for LAVA and 74 ± 13 for RT-1. (Brohan et al., 2023) `ev:measured` p. 9 ^brohan2023rt-037
- The quantitative emergent evaluation splits capabilities into three categories: symbol understanding, reasoning, and human recognition. (Brohan et al., 2023) `ev:reported` p. 9 ^brohan2023rt-038
- To reduce variance, RT-1, VC-1 and both RT-2 models are evaluated one after another under identical conditions using A/B testing. (Brohan et al., 2023) `ev:reported` p. 9 ^brohan2023rt-039
- The best RT-2-PaLI-X model achieves more than 3x the average emergent success rate of the next best baseline, RT-1. (Brohan et al., 2023) `ev:measured` p. 9 ^brohan2023rt-040
- Average emergent success rates are 60 for RT-2-PaLI-X-55B and 40 for RT-2-PaLM-E-12B, against 17 for RT-1 and 11 for VC-1. (Brohan et al., 2023) `ev:measured` p. 24 ^brohan2023rt-041
- On math reasoning tasks, RT-2-PaLM-E-12B scores 35, exceeding the 25 of RT-2-PaLI-X-55B and the 5 of RT-1. (Brohan et al., 2023) `ev:measured` p. 24 ^brohan2023rt-042
- The authors attribute the PaLM-E math edge to its different pre-training mixture, making it more capable at math than mostly visual PaLI-X. (Brohan et al., 2023) `ev:asserted` p. 9 ^brohan2023rt-043
- On person recognition, RT-2-PaLI-X-55B averages 53 and RT-2-PaLM-E-12B 43, against 20 for the RT-1 baseline. (Brohan et al., 2023) `ev:measured` p. 24 ^brohan2023rt-044
- RT-2 performs 2x to 3x better than RT-1 on the emergent instructions without any additional robotic demonstrations. (Brohan et al., 2023) `ev:measured` p. 24 ^brohan2023rt-045
- Ablations compare RT-2-PaLI-X at 5B and 55B parameters under training from scratch, fine-tuning on robot data, and co-fine-tuning. (Brohan et al., 2023) `ev:reported` p. 10 ^brohan2023rt-046
- Training the 5B RT-2-PaLI-X model from scratch yields an average generalization success rate of 9. (Brohan et al., 2023) `ev:measured` p. 24 ^brohan2023rt-047
- At 5B, co-fine-tuning averages 44 against 42 for plain fine-tuning on robot data in the generalization ablations. (Brohan et al., 2023) `ev:measured` p. 24 ^brohan2023rt-048
- At 55B, co-fine-tuning averages 63 against 52 for plain fine-tuning on robot data in the generalization ablations. (Brohan et al., 2023) `ev:measured` p. 24 ^brohan2023rt-049
- The authors attribute co-fine-tuning gains to keeping original data, which lets the model not forget concepts learned during VLM training. (Brohan et al., 2023) `ev:asserted` p. 10 ^brohan2023rt-050
- Increasing model size from 5B to 55B results in better generalization performance for RT-2-PaLI-X in the size and training ablations. (Brohan et al., 2023) `ev:measured` p. 10 ^brohan2023rt-051
- A chain-of-thought variant of RT-2-PaLM-E is fine-tuned for a few hundred gradient steps with data adding a natural-language Plan step before action tokens. (Brohan et al., 2023) `ev:reported` p. 10 ^brohan2023rt-052
- Qualitatively, RT-2 with chain-of-thought reasoning is able to answer more sophisticated commands, given a place to plan its actions in natural language first. (Brohan et al., 2023) `ev:measured` p. 10 ^brohan2023rt-053
- The authors view chain-of-thought results as initial evidence that VLM planners can be combined with low-level policies in one [[Vision-language-action models|VLA model]]. (Brohan et al., 2023) `ev:asserted` p. 10 ^brohan2023rt-054
- Web-scale pretraining does not give the robot any ability to perform new motions beyond the skills seen in the robot data. (Brohan et al., 2023) `ev:asserted` p. 11 ^brohan2023rt-055
- The authors believe the motion limitation results from the dataset not being varied enough along the axes of skills. (Brohan et al., 2023) `ev:asserted` p. 11 ^brohan2023rt-056
- The computation cost of large [[Vision-language-action models|VLA models]] is high, so real-time inference may become a major bottleneck for high-frequency control. (Brohan et al., 2023) `ev:asserted` p. 11 ^brohan2023rt-057
- RT-2 seemed to perform poorly at grasping objects by specific parts, such as the handle. (Brohan et al., 2023) `ev:measured` p. 23 ^brohan2023rt-058
- With the current dataset and training method, RT-2 seemed to perform poorly at extended reasoning requiring multiple layers of indirection. (Brohan et al., 2023) `ev:measured` p. 23 ^brohan2023rt-059

## 🎯 Contributions

## 📖 Glossary

- **Vision-language-action model (VLA)** — A pretrained vision-language model fine-tuned to output robot actions as text tokens.
- **Co-fine-tuning** — Fine-tuning jointly on robot trajectories and the original web vision-language data.
- **Action tokenization** — Discretizing each continuous action dimension into bins mapped to vocabulary tokens.
- **Symbol tuning** — Training a model to repurpose existing vocabulary tokens with new meanings.
- **Output constraint** — Restricting decoding to valid action tokens when a robot-action task is prompted.
- **Emergent capability** — A skill arising from web pretraining transfer, absent from the robot demonstrations.
- **Chain-of-thought (plan step)** — A natural-language plan generated before the action tokens.
- **Language-Table** — Open-source simulated tabletop pushing benchmark with language instructions.

## ❓ Open questions

- Can new motor skills be acquired through other data sources such as human videos, since web pretraining adds no new motions?
- Can quantization or distillation make VLA models run at higher control rates or on low-cost on-robot hardware?
- How would RT-2 perform with openly available VLMs rather than proprietary PaLI-X and PaLM-E?
- Would more diverse interaction-dynamics data let VLAs control unseen object dynamics, such as rolling or off-centre pushed objects?
- How does chain-of-thought RT-2 compare quantitatively with the base model, given only qualitative evaluation?
- How does the balance of robot versus web data in the co-fine-tuning mixture affect generalization?

## 📝 Notes on reading

- Version read: arXiv preprint 2307.15818v1 (28 Jul 2023), matching the packet identifier.
- Figures 2, 3, 4, 6, 8, 9 and 10 are images; only their captions and the appendix tables were available. Figure 4 and Figure 6 results were claimed from Appendix Tables 4, 5 and 6.
- Inconsistency: Table 4 gives RT-2-PaLI-X-55B an unseen average of 62, while the same configuration (55B co-fine-tuning) in Table 6 averages 63 with identical per-column values.
- Inconsistency: Section 4.2 says RT-2-PaLI-X achieves more than 3x RT-1's average emergent success, while Appendix H.2 says 2x to 3x; Table 5 averages (60 vs 17) support the former for PaLI-X, and PaLM-E (40) is roughly 2x.
- Table 4 column order is Seen, then Easy/Hard for unseen objects, backgrounds and environments, then Unseen Average; values were read in that order and cross-checked against Table 6.
- The RT-2-PaLM-E-12B row label in Table 4 carries a footnote marker ('12B1'), pointing to the note that PaLM-E pretraining includes robot images without low-level actions.
- Appendix G text places the object-dynamics failures in the Language Table setting, but the Figure 9 caption says real-world; not claimed as a location.
- Section 4.4 says chain-of-thought is trained on RT-2 with PaLM-E, while Figure 10 examples are also RT-2-PaLM-E; results are qualitative only.

## Suggested new concepts

- Vision-language-action models — RT-2 names this model class; later VLA work (OpenVLA, pi0) builds directly on it.
- Co-fine-tuning with web data — a training recipe that preserves pretrained concepts and improves robot generalization.
- Action tokenization — the discretize-and-tokenize scheme is a reusable design choice for language-model policies.
- Emergent capabilities in robot policies — semantic transfer from web pretraining to commands absent in robot data.
- Chain-of-thought for robot control — joint natural-language planning and action generation in one policy.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — VLA con acciones como tokens
