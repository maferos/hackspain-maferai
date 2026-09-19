---
aliases: []
type: "source"
title: "π0.5: a Vision-Language-Action Model with Open-World Generalization"
citekey: "Intelligence2025vision"
doi: "10.48550/arXiv.2504.16054"
arxiv: "2504.16054"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2504.16054"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Physical Intelligence", "Kevin Black", "Noah Brown", "James Darpinian", "Karan Dhabalia", "Danny Driess", "Adnan Esmail", "Michael Equi", "Chelsea Finn", "Niccolo Fusai", "Manuel Y. Galliker", "Dibya Ghosh", "Lachy Groom", "Karol Hausman", "Brian Ichter", "Szymon Jakubczak", "Tim Jones", "Liyiming Ke", "Devin LeBlanc", "Sergey Levine", "Adrian Li-Bell", "Mohith Mothukuri", "Suraj Nair", "Karl Pertsch", "Allen Z. Ren", "Lucy Xiaoyang Shi", "Laura Smith", "Jost Tobias Springenberg", "Kyle Stachowicz", "James Tanner", "Quan Vuong", "Homer Walke", "Anna Walling", "Haohuan Wang", "Lili Yu", "Ury Zhilinsky"]
sha256: ["6a1029fd8ab6944b74cf22f5e5d30e60bc15699d964b2900af799b807a34b64c"]
pdf: "Content/Papers/Intelligence2025vision.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Intelligence2025vision.pdf]]

> [!abstract] One-sentence summary
> π0.5 co-trains a single vision-language-action model on mobile-robot, other-robot, subtask, verbal-instruction and web data, and shows it can clean kitchens and bedrooms in homes never seen in training.

## Abstract

In order for robots to be useful, they must perform practically relevant tasks in the real world, outside of the lab. While vision-language-action (VLA) models have demonstrated impressive results for end-to-end robot control, it remains an open question how far such models can generalize in the wild. We describe $π_{0.5}$, a new model based on $π_{0}$ that uses co-training on heterogeneous tasks to enable broad generalization. $π_{0.5}$\ uses data from multiple robots, high-level semantic prediction, web data, and other sources to enable broadly generalizable real-world robotic manipulation. Our system uses a combination of co-training and hybrid multi-modal examples that combine image observations, language commands, object detections, semantic subtask prediction, and low-level actions. Our experiments show that this kind of knowledge transfer is essential for effective generalization, and we demonstrate for the first time that an end-to-end learning-enabled robotic system can perform long-horizon and dexterous manipulation skills, such as cleaning a kitchen or bedroom, in entirely new homes. (arXiv)

## 🧠 Key ideas (atomic)

- π0.5 is a [[Vision-language-action models|vision-language-action model]] built on π0 that uses co-training on heterogeneous tasks to enable broad generalization. (Intelligence et al., 2025) `ev:asserted` p. 1 ^intelligence2025vision-001
- During the first training phase, 97.6% of training examples do not come from mobile manipulators performing household tasks. (Intelligence et al., 2025) `ev:reported` p. 2 ^intelligence2025vision-002
- π0.5 can carry out long-horizon manipulation skills 10 to 15 minutes in length, cleaning an entire kitchen or bedroom from a high-level prompt. (Intelligence et al., 2025) `ev:measured` p. 2 ^intelligence2025vision-003
- At each inference step, the model predicts the low-level robot action chunk conditioned on a semantic subtask it predicted first. (Intelligence et al., 2025) `ev:reported` p. 2 ^intelligence2025vision-004
- The authors argue that low-level action inference benefits from [[Cross-embodiment pre-training|action data collected by other robots]], including simpler static robots elsewhere. (Intelligence et al., 2025) `ev:asserted` p. 2 ^intelligence2025vision-005
- The authors argue that high-level inference benefits from web semantic examples, high-level annotation prediction, and verbal commands from human supervisors. (Intelligence et al., 2025) `ev:asserted` p. 2 ^intelligence2025vision-006
- To their knowledge, the work is the first end-to-end learning-enabled robotic system performing long-horizon dexterous manipulation in entirely new homes. (Intelligence et al., 2025) `ev:asserted` p. 3 ^intelligence2025vision-007
- Prior works show that co-training [[Vision-language-action models|VLAs]] with VLM data mixtures can improve generalization to new objects or unseen scene backgrounds. (Intelligence et al., 2025) `ev:cited` p. 3 ^intelligence2025vision-008
- Unlike prior hierarchies using two separate models, π0.5 uses the same exact model for high-level subtask inference and low-level action inference. (Intelligence et al., 2025) `ev:reported` p. 3 ^intelligence2025vision-009
- Unlike embodied chain-of-thought methods, the high-level inference of π0.5 runs at a lower frequency than low-level action inference. (Intelligence et al., 2025) `ev:reported` p. 3 ^intelligence2025vision-010
- Earlier demonstrations of end-to-end generalization to new environments involve relatively simple tasks, typically less than a minute in length. (Intelligence et al., 2025) `ev:cited` p. 4 ^intelligence2025vision-011
- π0.5 is trained in two stages: pre-training with [[Action tokenization|discrete FAST action tokens]], then post-training with [[Flow matching policy|flow matching]] for continuous actions. (Intelligence et al., 2025) `ev:reported` p. 4 ^intelligence2025vision-012
- During pre-training, all tasks in the mixture, including tasks with robot actions, are represented with discrete tokens. (Intelligence et al., 2025) `ev:reported` p. 5 ^intelligence2025vision-013
- In the model's factorization, the action distribution depends only on the predicted subtask text, not on the overall task prompt. (Intelligence et al., 2025) `ev:reported` p. 5 ^intelligence2025vision-014
- Image patch, textual prompt, and continuous action tokens use bidirectional attention instead of the standard causal attention of LLMs. (Intelligence et al., 2025) `ev:reported` p. 5 ^intelligence2025vision-015
- In π0.5, the robot proprioceptive state is discretized and input to the model as text tokens. (Intelligence et al., 2025) `ev:reported` p. 5 ^intelligence2025vision-016
- [[Action tokenization|Discrete action representations]] are less well-suited for real-time inference because they require expensive autoregressive decoding. (Intelligence et al., 2025) `ev:cited` p. 5 ^intelligence2025vision-017
- The training loss combines text-token cross entropy, including FAST action tokens, with a flow-matching term weighted by a trade-off parameter. (Intelligence et al., 2025) `ev:reported` p. 5 ^intelligence2025vision-018
- The authors find that first pre-training with actions mapped to text tokens leads to stable pre-training of the VLA model. (Intelligence et al., 2025) `ev:asserted` p. 5 ^intelligence2025vision-019
- At inference, subtask text tokens are decoded autoregressively, followed by 10 denoising steps conditioned on them to produce actions. (Intelligence et al., 2025) `ev:reported` p. 5 ^intelligence2025vision-020
- The mobile manipulator data comprise about 400 hours of household tasks recorded in about 100 different home environments. (Intelligence et al., 2025) `ev:reported` p. 6 ^intelligence2025vision-021
- Non-mobile arms are lighter and easier to transport, which allowed a more diverse dataset in a wider range of homes. (Intelligence et al., 2025) `ev:reported` p. 6 ^intelligence2025vision-022
- The [[Cross-embodiment pre-training|laboratory cross-embodiment data]] span single-arm and dual-arm manipulators with static and mobile bases, plus the [[Open X-Embodiment dataset|open-source OXE dataset]]. (Intelligence et al., 2025) `ev:reported` p. 6 ^intelligence2025vision-023
- Robot data with multiple subtasks were manually annotated with semantic subtask descriptions to train joint subtask and action prediction. (Intelligence et al., 2025) `ev:reported` p. 6 ^intelligence2025vision-024
- The model is also trained to predict relevant bounding boxes in the current observation before predicting the subtask. (Intelligence et al., 2025) `ev:reported` p. 6 ^intelligence2025vision-025
- Web data cover image captioning, question answering, and object localization, drawn from CapsFusion, COCO, Cambrian-7M, PixMo, and VQAv2. (Intelligence et al., 2025) `ev:reported` p. 6 ^intelligence2025vision-026
- All action data are normalized to [−1, 1] using the 1% and 99% quantile of each action dimension per dataset. (Intelligence et al., 2025) `ev:reported` p. 7 ^intelligence2025vision-027
- Pre-training with discrete tokens runs for 280k gradient steps before the second stage, called post-training, begins. (Intelligence et al., 2025) `ev:reported` p. 7 ^intelligence2025vision-028
- Post-training optimizes the combined objective with α = 10.0 for 80k additional steps, starting the action expert from random weights. (Intelligence et al., 2025) `ev:reported` p. 7 ^intelligence2025vision-029
- The post-training action dataset consists of MM and ME robot data filtered to successful episodes below a fixed length threshold. (Intelligence et al., 2025) `ev:reported` p. 7 ^intelligence2025vision-030
- Verbal instruction demonstrations are collected by expert users teleoperating the robot in real time with language subtask commands. (Intelligence et al., 2025) `ev:reported` p. 7 ^intelligence2025vision-031
- Both mobile platforms have two 6 DoF arms with parallel jaw grippers, a wheeled holonomic base, and a torso lift mechanism. (Intelligence et al., 2025) `ev:reported` p. 7 ^intelligence2025vision-032
- The total dimensionality of the state and action spaces is 18 or 19, depending on the platform. (Intelligence et al., 2025) `ev:reported` p. 7 ^intelligence2025vision-033
- The model directly commands target poses for arms, gripper, and torso lift, and target base velocities, at 50 Hz. (Intelligence et al., 2025) `ev:reported` p. 7 ^intelligence2025vision-034
- Commanded targets are tracked with simple PD controllers, without any additional trajectory planning or collision detection. (Intelligence et al., 2025) `ev:reported` p. 7 ^intelligence2025vision-035
- All experiments are conducted in environments unseen in training, using mock homes for comparisons and three real homes for final evaluation. (Intelligence et al., 2025) `ev:reported` p. 7 ^intelligence2025vision-036
- In three real homes absent from training, π0.5 was able to consistently succeed on a variety of kitchen and bedroom tasks. (Intelligence et al., 2025) `ev:measured` p. 8 ^intelligence2025vision-037
- Many of the real-home tasks involve multiple stages lasting about 2 to 5 minutes, given a simple high-level command such as placing dishes. (Intelligence et al., 2025) `ev:reported` p. 8 ^intelligence2025vision-038
- The authors find that π0.5's performance in the mock evaluation setups is representative of its performance in real homes. (Intelligence et al., 2025) `ev:measured` p. 8 ^intelligence2025vision-039
- Scaling experiments compare models post-trained on mobile manipulation data from 3, 12, 22, 53, 82, and 104 locations. (Intelligence et al., 2025) `ev:reported` p. 8 ^intelligence2025vision-040
- Each scaling model trains for 40k steps, chosen such that every model sees the same number of unique data samples. (Intelligence et al., 2025) `ev:reported` p. 8 ^intelligence2025vision-041
- Average performance across the four mock-home test tasks generally improves as the number of training locations increases. (Intelligence et al., 2025) `ev:measured` p. 9 ^intelligence2025vision-042
- The final 104-location model attains similar performance to a control trained directly on data from the test homes. (Intelligence et al., 2025) `ev:measured` p. 9 ^intelligence2025vision-043
- Baselines without the other co-training tasks in pre-training perform significantly worse, even when trained on data from the test environment. (Intelligence et al., 2025) `ev:measured` p. 9 ^intelligence2025vision-044
- As the number of training locations increases, both the language following rate and the task success rate improve. (Intelligence et al., 2025) `ev:measured` p. 9 ^intelligence2025vision-045
- Performance on in-distribution objects improves more quickly than on out-of-distribution objects as training locations are added. (Intelligence et al., 2025) `ev:measured` p. 9 ^intelligence2025vision-046
- Excluding [[Cross-embodiment pre-training|either cross-embodiment source]], ME or CE data, significantly degrades performance on the end-to-end mock home tasks. (Intelligence et al., 2025) `ev:measured` p. 9 ^intelligence2025vision-047
- Excluding both ME and CE data harms mock-home task performance even more than excluding either source alone. (Intelligence et al., 2025) `ev:measured` p. 9 ^intelligence2025vision-048
- Removing web data does not produce a statistically significant difference in end-to-end mock-home task performance. (Intelligence et al., 2025) `ev:measured` p. 10 ^intelligence2025vision-049
- Removing web data causes significantly worse language following performance on out-of-distribution objects from unseen categories. (Intelligence et al., 2025) `ev:measured` p. 10 ^intelligence2025vision-050
- The authors conjecture that web data, with its broad knowledge of physical objects, lets the model follow commands about unseen object categories. (Intelligence et al., 2025) `ev:asserted` p. 10 ^intelligence2025vision-051
- π0.5 significantly outperforms both π0 and the enhanced π0-FAST+Flow variant in the mock home test environments. (Intelligence et al., 2025) `ev:measured` p. 10 ^intelligence2025vision-052
- The advantage of π0.5 over π0 holds even when π0 training is extended up to 300k training steps. (Intelligence et al., 2025) `ev:measured` p. 10 ^intelligence2025vision-053
- The full π0.5 model with high-level and low-level inference performs best, outperforming even the human HL oracle baseline. (Intelligence et al., 2025) `ev:measured` p. 11 ^intelligence2025vision-054
- The implicit HL ablation, trained with subtask data but without runtime high-level inference, is the second best model. (Intelligence et al., 2025) `ev:measured` p. 11 ^intelligence2025vision-055
- The verbal instruction dataset constitutes only about 11% of the high-level mobile manipulation examples used in training. (Intelligence et al., 2025) `ev:reported` p. 11 ^intelligence2025vision-056
- Excluding the verbal instruction data yields a significantly weaker model in the high-level inference evaluation. (Intelligence et al., 2025) `ev:measured` p. 11 ^intelligence2025vision-057
- Using zero-shot GPT-4 as the high-level policy attains the worst performance among the high-level inference methods compared. (Intelligence et al., 2025) `ev:measured` p. 11 ^intelligence2025vision-058
- The authors report persistent challenges with unfamiliar drawer handles and with cabinets that are physically hard for the robot to open. (Intelligence et al., 2025) `ev:asserted` p. 11 ^intelligence2025vision-059
- The authors report that high-level subtask inference is sometimes easily distracted, such as repeatedly closing and opening a drawer. (Intelligence et al., 2025) `ev:asserted` p. 11 ^intelligence2025vision-060
- The authors suggest richer context and memory could make the model significantly more capable in settings with more partial observability. (Intelligence et al., 2025) `ev:asserted` p. 11 ^intelligence2025vision-061
- Standard evaluations use 10 trials per task in four locations, for a total of 40 evaluations per policy. (Intelligence et al., 2025) `ev:reported` p. 17 ^intelligence2025vision-062
- In language following trials the target is placed beyond distractors, so a policy ignoring commands should reach only about 20% accuracy. (Intelligence et al., 2025) `ev:reported` p. 18 ^intelligence2025vision-063
- π0.5 follows language at a much higher rate than π0, which the authors take as showing the importance of discrete token training. (Intelligence et al., 2025) `ev:measured` p. 18 ^intelligence2025vision-064
- For Items in Drawer, performance drops substantially when cross-embodiment data or web data are removed from the training mixture. (Intelligence et al., 2025) `ev:measured` p. 18 ^intelligence2025vision-065
- Dishes in Sink remains relatively robust to removing web data but degrades when [[Cross-embodiment pre-training|cross-embodiment data]] are excluded. (Intelligence et al., 2025) `ev:measured` p. 18 ^intelligence2025vision-066
- The action expert is a smaller transformer with 300M parameters, trained with [[Flow matching policy|flow matching]] over an action horizon of 50. (Intelligence et al., 2025) `ev:reported` p. 19 ^intelligence2025vision-067
- Unlike π0, π0.5 injects the flow-matching timestep into each action expert layer through a separate MLP and adaptive RMSNorm. (Intelligence et al., 2025) `ev:reported` p. 19 ^intelligence2025vision-068
- Action expert embeddings do not attend to FAST action tokens, to avoid information leakage between the two action representations. (Intelligence et al., 2025) `ev:reported` p. 19 ^intelligence2025vision-069

## 🎯 Contributions

## 📖 Glossary

- **Vision-language-action model (VLA)** — a vision-language model fine-tuned to output robot actions from images and instructions.
- **Co-training** — training one model jointly on several heterogeneous datasets and task types.
- **Action expert** — separate, smaller transformer weights that generate continuous actions via flow matching.
- **FAST tokenizer** — compression-based scheme that turns robot action chunks into discrete tokens.
- **Flow matching** — generative method that learns a vector field to denoise samples into actions.
- **Action chunk** — a sequence of future actions predicted together in one inference step.
- **High-level subtask inference** — predicting a short semantic subtask label before emitting low-level actions.
- **Verbal instruction (VI) data** — demonstrations where experts command a learned policy step by step in language.
- **Cross-embodiment data** — robot data from platforms other than the target mobile manipulator.

## ❓ Open questions

- How much of the gain from web data would persist with larger or different web mixtures, given no significant effect on end-to-end task scores?
- Can richer context and memory solve tasks that require navigating between rooms or remembering where objects are stored?
- How could more complex user preferences and instructions be supported, and would synthetic annotations suffice?
- Which other supervision modalities, beyond verbal instructions, could people use to give robots contextual knowledge?
- Why does the full model outperform a human high-level oracle, and does this hold beyond the four evaluated tasks?
- How would the recipe transfer to embodiments or domains without a medium-sized target-platform dataset?

## 📝 Notes on reading

Read the arXiv preprint v1 (2504.16054v1, 22 Apr 2025). Most quantitative results (Figures 7 to 13, 15 to 17) are bar charts whose values were not extracted into the text; only the directions and significance statements given in the prose and captions are claimed. Figure 3 is inconsistent about the backbone size: it labels the pre-trained VLM as SigLIP (400M) + Gemma (2B) in one panel and Gemma (2.6B) in another; Appendix E calls it the 2B VLM initialized from PaliGemma. Appendix E states an action horizon of 50, i.e. H = 49. Equation (1) and the Beta timestep distribution were partly garbled by extraction and are only paraphrased. The paper describes π0-FAST+Flow as trained via a joint diffusion and FAST formulation, while Equation (1) uses flow matching. The Ray Bradbury epigraph in the introduction was not claimed.

## Suggested new concepts

- Hierarchical VLA inference — one model predicting a subtask then actions recurs across recent VLA work and deserves comparison.
- Co-training data mixtures for robot policies — ablations here isolate the value of each data source.
- Verbal instruction demonstrations — a new supervision modality for teaching high-level robot policies.
- Hybrid discrete/continuous action training — FAST tokens in pre-training with a flow-matching expert in post-training.
- Open-world robot evaluation in unseen homes — a protocol distinct from evaluating in training-like scenes.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Co-entrenamiento heterogéneo para la generalización

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
