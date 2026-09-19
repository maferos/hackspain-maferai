---
aliases: []
type: "source"
title: "OpenVLA: An Open-Source Vision-Language-Action Model"
citekey: "Kim2024openvla"
doi: "10.48550/arXiv.2406.09246"
arxiv: "2406.09246"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2406.09246"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Moo Jin Kim", "Karl Pertsch", "Siddharth Karamcheti", "Ted Xiao", "Ashwin Balakrishna", "Suraj Nair", "Rafael Rafailov", "Ethan Foster", "Grace Lam", "Pannag Sanketi", "Quan Vuong", "Thomas Kollar", "Benjamin Burchfiel", "Russ Tedrake", "Dorsa Sadigh", "Sergey Levine", "Percy Liang", "Chelsea Finn"]
sha256: ["353c37df34458f12f969b14dfd8b77175b727b9cddea7bb891759beddeefe1be"]
pdf: "Content/Papers/Kim2024openvla.pdf"
topics: ["[[Optimización y algoritmos]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Kim2024openvla.pdf]]

> [!abstract] One-sentence summary
> OpenVLA is a 7B-parameter open-source vision-language-action model trained on 970k Open X-Embodiment episodes that beats the 55B RT-2-X on multi-robot manipulation and shows that LoRA fine-tuning and 4-bit quantization make VLAs usable on consumer GPUs.

## Abstract

Large policies pretrained on a combination of Internet-scale vision-language data and diverse robot demonstrations have the potential to change how we teach robots new skills: rather than training new behaviors from scratch, we can fine-tune such vision-language-action (VLA) models to obtain robust, generalizable policies for visuomotor control. Yet, widespread adoption of VLAs for robotics has been challenging as 1) existing VLAs are largely closed and inaccessible to the public, and 2) prior work fails to explore methods for efficiently fine-tuning VLAs for new tasks, a key component for adoption. Addressing these challenges, we introduce OpenVLA, a 7B-parameter open-source VLA trained on a diverse collection of 970k real-world robot demonstrations. OpenVLA builds on a Llama 2 language model combined with a visual encoder that fuses pretrained features from DINOv2 and SigLIP. As a product of the added data diversity and new model components, OpenVLA demonstrates strong results for generalist manipulation, outperforming closed models such as RT-2-X (55B) by 16.5% in absolute task success rate across 29 tasks and multiple robot embodiments, with 7x fewer parameters. We further show that we can effectively fine-tune OpenVLA for new settings, with especially strong generalization results in multi-task environments involving multiple objects and strong language grounding abilities, and outperform expressive from-scratch imitation learning methods such as Diffusion Policy by 20.4%. We also explore compute efficiency; as a separate contribution, we show that OpenVLA can be fine-tuned on consumer GPUs via modern low-rank adaptation methods and served efficiently via quantization without a hit to downstream success rate. Finally, we release model checkpoints, fine-tuning notebooks, and our PyTorch codebase with built-in support for training VLAs at scale on Open X-Embodiment datasets. (arXiv)

## 🧠 Key ideas (atomic)

- OpenVLA is a 7B-parameter open-source [[Vision-language-action models|vision-language-action model]] trained on 970k robot demonstrations from the [[Open X-Embodiment dataset]]. (Kim et al., 2024) `ev:reported` p. 4 ^kim2024openvla-001
- The authors argue that current [[Vision-language-action models|VLAs]] are closed, with limited visibility into model architecture, training procedures, or data mixture. (Kim et al., 2024) `ev:asserted` p. 2 ^kim2024openvla-002
- The authors argue that existing VLA works give no best practices for adapting VLAs to new robots, especially on consumer-grade GPUs. (Kim et al., 2024) `ev:asserted` p. 2 ^kim2024openvla-003
- OpenVLA fine-tunes the Prismatic-7B VLM, which pairs a 600M-parameter visual encoder with a 7B-parameter Llama 2 language model backbone. (Kim et al., 2024) `ev:reported` p. 4 ^kim2024openvla-004
- Prismatic passes input image patches separately through pretrained SigLIP and DinoV2 encoders, then concatenates the resulting feature vectors channel-wise. (Kim et al., 2024) `ev:reported` p. 4 ^kim2024openvla-005
- Following Brohan et al., OpenVLA discretizes each robot action dimension separately into one of 256 bins for token prediction. (Kim et al., 2024) `ev:reported` p. 5 ^kim2024openvla-006
- Bin widths uniformly divide the interval between the 1st and 99th quantile of training actions, ignoring outliers that min-max bounds would include. (Kim et al., 2024) `ev:reported` p. 5 ^kim2024openvla-007
- Since the Llama tokenizer reserves only 100 special tokens, OpenVLA overwrites the 256 least used vocabulary tokens with [[Action tokenization|action tokens]]. (Kim et al., 2024) `ev:reported` p. 5 ^kim2024openvla-008
- OpenVLA is trained with a standard next-token prediction objective, evaluating the cross-entropy loss on the [[Action tokenization|predicted action tokens]] only. (Kim et al., 2024) `ev:reported` p. 5 ^kim2024openvla-009
- At the time of writing, the full [[Open X-Embodiment dataset|OpenX dataset]] comprised more than 70 individual robot datasets with more than 2M robot trajectories. (Kim et al., 2024) `ev:reported` p. 5 ^kim2024openvla-010
- The training data were restricted to manipulation datasets with at least one 3rd person camera that use single-arm end-effector control. (Kim et al., 2024) `ev:reported` p. 5 ^kim2024openvla-011
- Dataset mixture weights follow Octo, which down-weights less diverse datasets and up-weights datasets with larger task and scene diversity. (Kim et al., 2024) `ev:reported` p. 5 ^kim2024openvla-012
- DROID was added at a conservative 10% mixture weight, but its action token accuracy remained low throughout training. (Kim et al., 2024) `ev:measured` p. 5 ^kim2024openvla-013
- DROID was removed from the data mixture for the final third of training to avoid jeopardizing the quality of the final model. (Kim et al., 2024) `ev:reported` p. 5 ^kim2024openvla-014
- In backbone tests, LLaVA improved upon IDEFICS-1 by 35% absolute success rate across five language grounding tasks in a BridgeData V2 sink. (Kim et al., 2024) `ev:measured` p. 6 ^kim2024openvla-015
- The fine-tuned Prismatic VLM policy outperformed the LLaVA policy by roughly 10% absolute success rate across single-object and multi-object grounding tasks. (Kim et al., 2024) `ev:measured` p. 6 ^kim2024openvla-016
- The authors attribute Prismatic's performance advantage to improved spatial reasoning capabilities afforded by the fused SigLIP-DinoV2 vision backbones. (Kim et al., 2024) `ev:asserted` p. 6 ^kim2024openvla-017
- Comparing VLAs with 224 × 224px and 384 × 384px inputs, the authors found no performance difference in their evaluations. (Kim et al., 2024) `ev:measured` p. 6 ^kim2024openvla-018
- Training a VLA with 384 × 384px inputs takes 3x longer, so the final OpenVLA model uses 224 × 224px images. (Kim et al., 2024) `ev:reported` p. 6 ^kim2024openvla-019
- Contrary to VLM findings favouring frozen encoders, fine-tuning the vision encoder during VLA training was found crucial for good VLA performance. (Kim et al., 2024) `ev:measured` p. 6 ^kim2024openvla-020
- The authors hypothesize that the pretrained vision backbone may not capture sufficient fine-grained spatial detail to enable precise robotic control. (Kim et al., 2024) `ev:asserted` p. 6 ^kim2024openvla-021
- Real robot performance continually increased with more training epochs until training action token accuracy surpassed 95%. (Kim et al., 2024) `ev:measured` p. 6 ^kim2024openvla-022
- Unlike typical LLM or VLM runs of one or two epochs, the final OpenVLA training run completes 27 epochs through its dataset. (Kim et al., 2024) `ev:reported` p. 6 ^kim2024openvla-023
- A learning-rate sweep across multiple orders of magnitude gave the best VLA results with a fixed learning rate of 2e-5. (Kim et al., 2024) `ev:measured` p. 6 ^kim2024openvla-024
- The final OpenVLA model was trained on 64 A100 GPUs for 14 days, a total of 21,500 A100-hours, with batch size 2048. (Kim et al., 2024) `ev:reported` p. 6 ^kim2024openvla-025
- During inference in bfloat16 precision without quantization, OpenVLA requires 15GB of GPU memory according to the infrastructure section. (Kim et al., 2024) `ev:measured` p. 6 ^kim2024openvla-026
- Without compilation, speculative decoding or other speed-up tricks, OpenVLA runs at approximately 6Hz on one NVIDIA RTX 4090 GPU. (Kim et al., 2024) `ev:measured` p. 6 ^kim2024openvla-027
- Out-of-the-box evaluation used 170 BridgeData V2 WidowX rollouts over 17 tasks and 60 Google robot rollouts over 12 tasks per method. (Kim et al., 2024) `ev:reported` p. 7 ^kim2024openvla-028
- Baselines were RT-1-X with 35M parameters, Octo with 93M parameters, and RT-2-X, a closed 55B-parameter VLA. (Kim et al., 2024) `ev:reported` p. 8 ^kim2024openvla-029
- On the BridgeData V2 suite, mean success was 70.6% for OpenVLA, 50.6% for RT-2-X, 20.0% for Octo, 18.5% for RT-1-X. (Kim et al., 2024) `ev:measured` p. 26 ^kim2024openvla-030
- On the Google robot suite, mean success was 85.0% for OpenVLA, 78.3% for RT-2-X, 33.3% for RT-1-X, 26.7% for Octo. (Kim et al., 2024) `ev:measured` p. 28 ^kim2024openvla-031
- OpenVLA outperforms the 55B-parameter RT-2-X by 16.5% absolute success rate across 29 evaluation tasks on WidowX and Google Robot embodiments. (Kim et al., 2024) `ev:measured` p. 2 ^kim2024openvla-032
- OpenVLA outperforms RT-2-X in all BridgeData V2 categories except semantic generalization, where RT-2-X achieves higher performance. (Kim et al., 2024) `ev:measured` p. 7 ^kim2024openvla-033
- The authors attribute OpenVLA's gains partly to a larger training dataset of 970k trajectories versus 350k for RT-2-X. (Kim et al., 2024) `ev:asserted` p. 8 ^kim2024openvla-034
- The original BridgeData V2 dataset recorded an all-zero action as the ground-truth action in the first timestep of every demonstration. (Kim et al., 2024) `ev:reported` p. 32 ^kim2024openvla-035
- Filtering out the first transition in every Bridge demonstration was sufficient to mitigate the policy freezing behavior in most cases. (Kim et al., 2024) `ev:measured` p. 32 ^kim2024openvla-036
- To avoid freezing, RT-2-X was evaluated by always querying its second-most-likely action, the workaround also used in Open X-Embodiment. (Kim et al., 2024) `ev:reported` p. 33 ^kim2024openvla-037
- The adaptation experiments fully fine-tune all OpenVLA parameters on small datasets with 10–150 demonstrations of each target task. (Kim et al., 2024) `ev:reported` p. 8 ^kim2024openvla-038
- Fine-tuning targets were a table-mounted Franka-Tabletop setup at 5Hz and a Franka-DROID setup at 15 Hz with non-blocking controllers. (Kim et al., 2024) `ev:reported` p. 9 ^kim2024openvla-039
- Both [[Diffusion Policy]] versions are competitive with or outperform Octo and OpenVLA on narrower single-instruction tasks like Put Carrot in Bowl. (Kim et al., 2024) `ev:measured` p. 9 ^kim2024openvla-040
- The pretrained generalist policies perform better than Diffusion Policy on diverse fine-tuning tasks with multiple objects requiring language conditioning. (Kim et al., 2024) `ev:measured` p. 9 ^kim2024openvla-041
- On Franka-Tabletop, fine-tuned OpenVLA averaged 67.2% success, versus 48.5% for Diffusion Policy and 43.4% for fine-tuned Octo. (Kim et al., 2024) `ev:measured` p. 32 ^kim2024openvla-042
- On Franka-DROID, fine-tuned OpenVLA averaged 58.3% success, versus 38.3% for fine-tuned Octo and 35.0% for Diffusion Policy. (Kim et al., 2024) `ev:measured` p. 32 ^kim2024openvla-043
- OpenVLA (scratch), fine-tuned from Prismatic without [[Cross-embodiment pre-training|OpenX robot pretraining]], averaged 43.4% on Franka-Tabletop and 21.7% on Franka-DROID. (Kim et al., 2024) `ev:measured` p. 32 ^kim2024openvla-044
- OpenVLA is the only approach that achieves at least 50% success rate across all tested tasks in the fine-tuning evaluation. (Kim et al., 2024) `ev:measured` p. 9 ^kim2024openvla-045
- The authors suggest [[Action chunking|action chunking]] and temporal smoothing may help OpenVLA reach Diffusion Policy's dexterity on narrow, highly dexterous tasks. (Kim et al., 2024) `ev:asserted` p. 9 ^kim2024openvla-046
- The full fine-tuning runs of OpenVLA used 8 A100 GPUs for 5-15 hours per task, depending on the dataset size. (Kim et al., 2024) `ev:reported` p. 10 ^kim2024openvla-047
- LoRA fine-tuning matched full fine-tuning performance on Franka-Tabletop tasks while fine-tuning only 1.4% of the model parameters. (Kim et al., 2024) `ev:measured` p. 10 ^kim2024openvla-048
- On the parameter-efficient benchmark, LoRA at rank 32 reached 68.2% success compared with 69.7% for full fine-tuning. (Kim et al., 2024) `ev:measured` p. 10 ^kim2024openvla-049
- Fine-tuning only the last layer reached 30.3% success, the lowest of the parameter-efficient fine-tuning strategies compared on Franka-Tabletop tasks. (Kim et al., 2024) `ev:measured` p. 10 ^kim2024openvla-050
- Freezing the vision encoder during fine-tuning reached 47.0% success, suggesting further adaptation of visual features to the target scene is crucial. (Kim et al., 2024) `ev:measured` p. 10 ^kim2024openvla-051
- Sandwich fine-tuning reached 62.1% success using 64.0 GB of VRAM, versus 163.3 GB for full fine-tuning at batch 16. (Kim et al., 2024) `ev:measured` p. 10 ^kim2024openvla-052
- LoRA ranks 32 and 64 both reached 68.2% success, so the authors recommend a default LoRA rank of r = 32. (Kim et al., 2024) `ev:measured` p. 10 ^kim2024openvla-053
- With LoRA, OpenVLA can be fine-tuned on a new task within 10-15 hours on a single A100 GPU, an 8x compute reduction. (Kim et al., 2024) `ev:measured` p. 10 ^kim2024openvla-054
- On eight BridgeData V2 tasks, 4-bit quantized OpenVLA reached 71.9% success versus 71.3% with bfloat16 inference. (Kim et al., 2024) `ev:measured` p. 10 ^kim2024openvla-055
- 4-bit quantized inference used 7.0 GB of GPU memory, compared with 16.8 GB for bfloat16 inference on the same tasks. (Kim et al., 2024) `ev:measured` p. 10 ^kim2024openvla-056
- With 8-bit quantization, OpenVLA reached 58.1% success on the eight BridgeData V2 tasks, using 10.2 GB of VRAM. (Kim et al., 2024) `ev:measured` p. 10 ^kim2024openvla-057
- On the A5000 evaluation GPU, 8-bit quantized OpenVLA runs at only 1.2Hz, changing system dynamics relative to the 5Hz training controller. (Kim et al., 2024) `ev:measured` p. 11 ^kim2024openvla-058
- Under blocking control, int8 inference reached 74.4% success, comparable to 70.0% for bfloat16 and 68.8% for int4 inference. (Kim et al., 2024) `ev:measured` p. 35 ^kim2024openvla-059
- Training only on BridgeData V2 instead of the [[Open X-Embodiment dataset|OpenX mixture]] dropped mean success on eight Bridge tasks from 76.3% to 45.6%. (Kim et al., 2024) `ev:measured` p. 34 ^kim2024openvla-060
- Removing the DinoV2 encoder from the Bridge-only model lowered mean success from 45.6% to 40.6% on the same eight tasks. (Kim et al., 2024) `ev:measured` p. 34 ^kim2024openvla-061
- The authors report that ablating OpenX training reduced performance across all generalization categories, although language grounding performance was not impacted. (Kim et al., 2024) `ev:measured` p. 33 ^kim2024openvla-062
- Where both were tested, fine-tuning the vision encoder gave 80.0% average success versus 46.7% with a frozen vision encoder. (Kim et al., 2024) `ev:measured` p. 35 ^kim2024openvla-063
- In LIBERO simulation, LoRA fine-tuned OpenVLA reached 76.5% average success, versus 75.1% for fine-tuned Octo and 72.4% for Diffusion Policy. (Kim et al., 2024) `ev:measured` p. 37 ^kim2024openvla-064
- The authors attribute the tighter LIBERO margin to OpenVLA being pretrained purely on real-world robot data with no simulation data. (Kim et al., 2024) `ev:asserted` p. 37 ^kim2024openvla-065
- Filtering no-op actions from LIBERO demonstrations was found crucial, since expressive single-step policies otherwise imitate them and freeze during evaluation. (Kim et al., 2024) `ev:measured` p. 36 ^kim2024openvla-066
- The authors state that OpenVLA currently only supports single-image observations, without multiple images, proprioceptive inputs or observation history. (Kim et al., 2024) `ev:asserted` p. 11 ^kim2024openvla-067
- The authors state that improving inference throughput is critical for high-frequency control setups such as ALOHA, which runs at 50Hz. (Kim et al., 2024) `ev:asserted` p. 11 ^kim2024openvla-068
- OpenVLA does not yet offer very high reliability on the tested tasks, typically achieving <90% success rate according to the authors. (Kim et al., 2024) `ev:measured` p. 11 ^kim2024openvla-069

## 🎯 Contributions

## 📖 Glossary

- **Vision-language-action model (VLA)** — a vision-language model fine-tuned to output robot control actions as tokens.
- **Open X-Embodiment (OpenX)** — pooled collection of over 70 robot datasets across many embodiments.
- **Prismatic VLM** — open VLM family fusing SigLIP and DinoV2 visual features with a Llama 2 backbone.
- **Action discretization** — mapping each continuous action dimension into one of 256 quantile-based bins.
- **LoRA** — low-rank adaptation; trains small low-rank matrices added to frozen linear layers.
- **Sandwich fine-tuning** — updating only the vision encoder, token embedding matrix and last layer.
- **Blocking control** — each action finishes executing before the policy predicts the next one.
- **No-op action** — an action with near-zero motion that leaves the gripper state unchanged.

## ❓ Open questions

- What effect does the size of the base VLM have on VLA performance?
- Does co-training on robot action data and Internet-scale vision-language data substantially improve VLA performance?
- What visual features are best suited for VLA models?
- How can OpenVLA support multiple images, proprioception and observation history as inputs?
- Can action chunking or speculative decoding raise throughput enough for 50Hz bimanual control?
- Would a larger mixture weight or model let a VLA fit the diversity of DROID?
- Would adding simulation data to pretraining widen the gains on benchmarks such as LIBERO?

## 📝 Notes on reading

Read the arXiv preprint v3 (5 Sep 2024), matching the packet identifier arXiv:2406.09246.

Figures 3, 4 and 5 (bar charts of success rates) came through the extraction as loose numbers without labels; per-task values were taken from Tables 4, 6 and 7 instead. Figure 6 (inference speed per GPU) was extracted only as N/A, so no per-GPU throughput was claimed. Qualitatively, the paper reports that RT-1-X and Octo often fail to manipulate the correct object when distractors are present (p. 8), and that 4-bit models run at 3Hz on the A5000 (p. 11).

Inconsistencies inside the paper: the infrastructure section gives 15GB of GPU memory for bfloat16 inference, while Table 2 lists 16.8 GB. Appendix D.4 refers to the quantization experiments as Section 5.3, but they are in Section 5.4. The 20.4% gain over Diffusion Policy appears only in the abstract; Table 7 averages do not state it directly. Footnote 4 says Sections 5.3 and 5.4 use a smaller variant pretrained on the Octo mixture with a SigLIP-only vision backbone, so those numbers are not from the released DinoSigLIP OpenVLA. The claim that OpenVLA reaches at least 50% on all fine-tuning tasks refers to per-task aggregates in Fig. 5; Table 7 lists 40.0% for Put Carrot in Bowl (OOD). Table 10 evaluations use different initial configurations and are not directly comparable to other Bridge results.

## Suggested new concepts

- Vision-language-action models — a core model class for generalist robot policies that several vault sources will share.
- Action tokenization — discretizing continuous robot actions into language-model tokens is a reusable design choice across VLAs.
- Parameter-efficient fine-tuning for robot policies — LoRA and related methods decide whether large policies can be adapted on lab hardware.
- Open X-Embodiment dataset — the shared pretraining corpus behind OpenVLA, Octo and RT-X models.
- Quantized policy inference — ties model precision to control frequency and closed-loop dynamics.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — VLA abierto con fine-tuning LoRA (D.1).
- **[[03_aplicaciones_vision_por_computador]]** — VLA abierto ajustable con LoRA, acciones $\Delta$ discretizadas

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
