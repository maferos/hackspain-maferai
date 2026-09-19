---
aliases: []
type: "source"
title: "Octo: An Open-Source Generalist Robot Policy"
citekey: "Team2024octo"
doi: "10.48550/arXiv.2405.12213"
arxiv: "2405.12213"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2405.12213"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: [" Octo Model Team", "Dibya Ghosh", "Homer Walke", "Karl Pertsch", "Kevin Black", "Oier Mees", "Sudeep Dasari", "Joey Hejna", "Tobias Kreiman", "Charles Xu", "Jianlan Luo", "You Liang Tan", "Lawrence Yunliang Chen", "Pannag Sanketi", "Quan Vuong", "Ted Xiao", "Dorsa Sadigh", "Chelsea Finn", "Sergey Levine"]
sha256: ["73bff297cfafe523319162124e6b7f96919c0930e0a380f307255c4c7464ac93"]
pdf: "Content/Papers/Team2024octo.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Team2024octo.pdf]]

> [!abstract] One-sentence summary
> Octo is an open-source transformer policy pretrained on 800k Open X-Embodiment trajectories that controls several robots zero-shot and can be finetuned in hours to new sensors, action spaces and embodiments, with ablations of the design choices behind generalist robot policies.

## Abstract

Large policies pretrained on diverse robot datasets have the potential to transform robotic learning: instead of training new policies from scratch, such generalist robot policies may be finetuned with only a little in-domain data, yet generalize broadly. However, to be widely applicable across a range of robotic learning scenarios, environments, and tasks, such policies need to handle diverse sensors and action spaces, accommodate a variety of commonly used robotic platforms, and finetune readily and efficiently to new domains. In this work, we aim to lay the groundwork for developing open-source, widely applicable, generalist policies for robotic manipulation. As a first step, we introduce Octo, a large transformer-based policy trained on 800k trajectories from the Open X-Embodiment dataset, the largest robot manipulation dataset to date. It can be instructed via language commands or goal images and can be effectively finetuned to robot setups with new sensory inputs and action spaces within a few hours on standard consumer GPUs. In experiments across 9 robotic platforms, we demonstrate that Octo serves as a versatile policy initialization that can be effectively finetuned to new observation and action spaces. We also perform detailed ablations of design decisions for the Octo model, from architecture to training data, to guide future research on building generalist robot models. (arXiv)

## 🧠 Key ideas (atomic)

- Octo is a transformer-based generalist robot policy pretrained on 800k robot demonstrations from the [[Open X-Embodiment dataset]]. (Team et al., 2024) `ev:reported` p. 2 ^team2024octo-001
- The authors describe Octo as the first generalist robot policy that can be effectively finetuned to new observations and action spaces. (Team et al., 2024) `ev:asserted` p. 2 ^team2024octo-002
- The authors describe Octo as the first generalist robot manipulation policy that is fully open-source, including training pipeline, checkpoints and data. (Team et al., 2024) `ev:asserted` p. 2 ^team2024octo-003
- According to the authors, earlier generalist robot policies typically constrain downstream users to a pre-defined set of input observations, such as one camera stream. (Team et al., 2024) `ev:asserted` p. 2 ^team2024octo-004
- [[Open X-Embodiment dataset|The Open X-Embodiment dataset]] contains approximately 1.5M robot episodes, of which the authors curate 800k for Octo training. (Team et al., 2024) `ev:reported` p. 3 ^team2024octo-005
- The RT-X model was trained on a more restricted subset of 350K episodes from the [[Open X-Embodiment dataset]]. (Team et al., 2024) `ev:cited` p. 3 ^team2024octo-006
- Octo passes language instructions through a pretrained t5-base (111M) transformer that produces a sequence of language embedding tokens. (Team et al., 2024) `ev:reported` p. 4 ^team2024octo-007
- Image observations and goal images pass through a shallow convolution stack and are then split into a sequence of flattened patches. (Team et al., 2024) `ev:reported` p. 4 ^team2024octo-008
- In Octo's block-wise masked attention, observation tokens attend causally only to tokens from the same or earlier time steps plus task tokens. (Team et al., 2024) `ev:reported` p. 4 ^team2024octo-009
- Learned readout tokens attend to preceding observation and task tokens but are not attended to by them, acting like BERT's CLS token. (Team et al., 2024) `ev:reported` p. 4 ^team2024octo-010
- A lightweight diffusion action head applied to the readout embeddings predicts [[Action chunking|a chunk of several consecutive actions]], similar to prior work. (Team et al., 2024) `ev:reported` p. 4 ^team2024octo-011
- When new tasks, observations or heads are added during finetuning, the pretrained transformer weights can be wholly retained, according to the authors. (Team et al., 2024) `ev:asserted` p. 4 ^team2024octo-012
- Octo is trained on a mixture of 25 datasets curated from the Open X-Embodiment dataset of robot learning data. (Team et al., 2024) `ev:reported` p. 4 ^team2024octo-013
- Curation removed [[Open X-Embodiment dataset|Open-X datasets]] that contain no image streams, as well as datasets that do not use delta end-effector control. (Team et al., 2024) `ev:reported` p. 4 ^team2024octo-014
- The authors also removed datasets that are too repetitive, have low image resolution, or consist of excessively niche tasks. (Team et al., 2024) `ev:reported` p. 4 ^team2024octo-015
- Datasets roughly categorized as more diverse by tasks and environments receive double weight during Octo training. (Team et al., 2024) `ev:reported` p. 4 ^team2024octo-016
- Gripper action spaces are aligned across datasets such that a gripper command of +1 means open and 0 means closed. (Team et al., 2024) `ev:reported` p. 5 ^team2024octo-017
- Octo uses a conditional diffusion decoding head, with only one transformer forward pass performed per action prediction. (Team et al., 2024) `ev:reported` p. 5 ^team2024octo-018
- The authors found the diffusion parameterization outperformed MSE action heads or discretized action distributions in zero-shot and finetuning evaluations. (Team et al., 2024) `ev:measured` p. 5 ^team2024octo-019
- Finetuning updates the full model with the diffusion objective, a recipe that outperformed recipes freezing subsets of the pretrained parameters. (Team et al., 2024) `ev:measured` p. 5 ^team2024octo-020
- All finetuning experiments use a target dataset of around 100 trajectories and 50k steps with cosine learning rate decay. (Team et al., 2024) `ev:reported` p. 5 ^team2024octo-021
- The ViT-B-sized Octo model was trained for 300k steps with a batch size of 2048 on a TPU v4-128 pod. (Team et al., 2024) `ev:reported` p. 5 ^team2024octo-022
- A finetuning run of the ViT-B-sized model on a single NVIDIA A5000 GPU with 24GB of VRAM takes approximately 5 hours. (Team et al., 2024) `ev:reported` p. 5 ^team2024octo-023
- Octo trains with 2 frames of observation history, since preliminary experiments showed significantly diminishing gains beyond the first additional frame. (Team et al., 2024) `ev:measured` p. 5 ^team2024octo-024
- The language instruction or goal image is randomly zeroed out per training example to enable conditioning on either task modality. (Team et al., 2024) `ev:reported` p. 5 ^team2024octo-025
- The released checkpoints are Octo-Small with 27M parameters and Octo-Base with 93M parameters, alongside finetuning and pretraining code in JAX. (Team et al., 2024) `ev:reported` p. 5 ^team2024octo-026
- Octo is evaluated on 9 robot learning setups at 4 institutions, covering zero-shot control and data-efficient finetuning. (Team et al., 2024) `ev:reported` p. 5 ^team2024octo-027
- The from-scratch baseline is a ResNet visual encoder with FiLM language conditioning and a small diffusion transformer decoder, totalling 28M parameters. (Team et al., 2024) `ev:reported` p. 6 ^team2024octo-028
- The VC-1 baseline uses a ViT-B encoder pretrained on 4,000 hours of ego-centric videos and ImageNet, with an MLP action decoder. (Team et al., 2024) `ev:reported` p. 6 ^team2024octo-029
- The authors found that training their large transformer architecture from scratch overfit quickly on the small finetuning datasets. (Team et al., 2024) `ev:measured` p. 6 ^team2024octo-030
- Zero-shot evaluation used two language tasks per robot from the matching OXE dataset, with 10 trials per task under varying initial conditions. (Team et al., 2024) `ev:reported` p. 7 ^team2024octo-031
- In zero-shot evaluation, Octo had on average a 29% higher success rate than RT-1-X with 35M parameters. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-032
- On the WidowX and RT-1 Robot evaluations, Octo performed similarly to RT-2-X, a model with 55 billion parameters. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-033
- On the WidowX tasks, goal image conditioning achieved a 25% higher success rate than language conditioning for Octo. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-034
- The authors suggest goal images likely provide more information about how to achieve the task than language instructions do. (Team et al., 2024) `ev:asserted` p. 7 ^team2024octo-035
- In the WidowX zero-shot generalization analysis, Octo-Small averaged 85% success on the two in-distribution tasks. (Team et al., 2024) `ev:measured` p. 17 ^team2024octo-036
- In the same generalization analysis, Octo-Small averaged 80% success on tasks involving novel objects, such as putting bread on a plate. (Team et al., 2024) `ev:measured` p. 17 ^team2024octo-037
- In the WidowX generalization analysis, Octo-Small averaged 40% success on tasks set in a novel environment. (Team et al., 2024) `ev:measured` p. 17 ^team2024octo-038
- Octo-Small averaged 5% success on novel skills in the WidowX analysis, including 0% on putting a block in a slot. (Team et al., 2024) `ev:measured` p. 17 ^team2024octo-039
- Across six finetuning setups, finetuned Octo averaged 72% success, compared with 20% for ResNet+Transformer Scratch and 15% for VC-1. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-040
- On average across the six finetuning evaluation setups, Octo outperforms the next best baseline by 52%. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-041
- Finetuned Octo reached 70% success on Berkeley Insertion, which adds force-torque proprioception as a new observation input. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-042
- Finetuned Octo reached 60% success on Berkeley Pick-Up, which uses joint position control as a new action space. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-043
- Finetuned Octo reached 100% success on Berkeley Coke, one of the setups testing a new robot embodiment. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-044
- Finetuned Octo reached 80% success on Berkeley Bimanual, compared with 50% for VC-1 and 20% for training from scratch. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-045
- In the WidowX ablations, Octo-Small reached 83% aggregate success, compared with 60% when trained on the RT-X dataset mix. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-046
- Training on the single-robot Bridge dataset alone lowered aggregate WidowX success to 43% in the data ablation. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-047
- Replacing the diffusion head with [[Action tokenization|discretized action prediction]] lowered aggregate WidowX ablation success to 18%, against 83% for Octo-Small. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-048
- Continuous action prediction with an MSE loss reached 35% aggregate success in the WidowX policy-objective ablation. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-049
- A ResNet-50 plus Transformer architecture reached 70% aggregate WidowX success, below the 83% of the transformer-first Octo-Small. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-050
- The authors found ResNet-based architectures performed better than ViTs when training on small datasets, such as in from-scratch comparisons. (Team et al., 2024) `ev:measured` p. 7 ^team2024octo-051
- In the data ablation, the performance of Octo increased as the number of training datasets increased. (Team et al., 2024) `ev:measured` p. 8 ^team2024octo-052
- The authors suggest that expanding the data mix to even more datasets may further improve policy performance. (Team et al., 2024) `ev:asserted` p. 8 ^team2024octo-053
- The authors state [[Diffusion Policy|the diffusion head]] likely helps because it can model [[Multimodal action distributions|multi-modal action distributions]], unlike the MSE head. (Team et al., 2024) `ev:asserted` p. 8 ^team2024octo-054
- Qualitatively, the diffusion-trained policy acts more decisively than MSE-trained policies, according to the authors' observations. (Team et al., 2024) `ev:measured` p. 8 ^team2024octo-055
- Zero-shot success on UR5 and WidowX tasks improved across Octo-Tiny (10M), Octo-Small (27M) and Octo-Base (93M). (Team et al., 2024) `ev:measured` p. 8 ^team2024octo-056
- The authors found the Base model more robust to initial scene configuration than the Small model. (Team et al., 2024) `ev:measured` p. 8 ^team2024octo-057
- Finetuning results were often stronger when using only a third person camera instead of combining third person and wrist cameras. (Team et al., 2024) `ev:measured` p. 8 ^team2024octo-058
- The authors notice a large difference between language-conditioned and goal-conditioned policy performance of the current Octo model. (Team et al., 2024) `ev:measured` p. 8 ^team2024octo-059
- Only 27% of the Octo training data contains wrist camera information, which the authors see as a likely reason for weak wrist-camera use. (Team et al., 2024) `ev:reported` p. 8 ^team2024octo-060
- Only 56% of the Octo pretraining data contains language annotations, according to the discussion of the model's limitations. (Team et al., 2024) `ev:reported` p. 8 ^team2024octo-061
- Octo was trained and evaluated exclusively on single and dual-arm manipulators, leaving navigation and mobile manipulation robots for future work. (Team et al., 2024) `ev:reported` p. 8 ^team2024octo-062
- Octo's pretraining mixture assigns sampling weights of 17.0% each to the Fractal, Kuka and Bridge datasets. (Team et al., 2024) `ev:reported` p. 14 ^team2024octo-063
- Image patches of size 16 × 16 yield 256 tokens for third-person camera images and 64 tokens for wrist camera images. (Team et al., 2024) `ev:reported` p. 15 ^team2024octo-064
- The diffusion action head is a 3-layer MLP with a hidden dimension of 256, residual connections and layer normalization. (Team et al., 2024) `ev:reported` p. 15 ^team2024octo-065
- Tokenizing images into 16 × 16 patches improved performance over 32 × 32 patches, particularly for grasping and other fine-grained tasks. (Team et al., 2024) `ev:measured` p. 15 ^team2024octo-066
- Zero-shot performance suffered significantly with a small 20k shuffle buffer and trajectory-level interleaving of training frames. (Team et al., 2024) `ev:measured` p. 15 ^team2024octo-067
- Replacing the diffusion head with a simple L2 loss led to hedging policies that move very slowly in WidowX evaluations. (Team et al., 2024) `ev:measured` p. 15 ^team2024octo-068
- Using the frozen t5-base language encoder resulted in better language-conditioned policies than larger encoders or finetuning the encoder. (Team et al., 2024) `ev:measured` p. 15 ^team2024octo-069

## 🎯 Contributions

## 📖 Glossary

- **Generalist robot policy (GRP)** — Policy mapping observations to low-level actions across tasks, environments and robot systems.
- **Open X-Embodiment (OXE)** — Pooled collection of robot learning datasets across many embodiments; about 1.5M episodes.
- **Readout token** — Learned token that reads transformer embeddings without influencing them; feeds the action head.
- **Action chunking** — Predicting a sequence of several future actions at each policy step.
- **Diffusion action head** — Small network producing actions by iterative denoising, conditioned on transformer embeddings.
- **Hindsight goal relabeling** — Assigning a future state of the same trajectory as the goal image.
- **Block-wise masked attention** — Attention mask letting token groups attend only to allowed earlier or task groups.
- **Receding horizon control** — Executing only the first actions of a predicted chunk before re-planning.

## ❓ Open questions

- How should a pretraining data mixture be curated and weighted, beyond the authors' manual heuristics?
- Would more wrist-camera and language-annotated pretraining data close the wrist-camera and language-conditioning gaps?
- Can generalist policies learn from sub-optimal or online interaction data instead of optimal demonstrations only?
- Does the recipe transfer to navigation and mobile manipulation robots?
- How can novel-skill generalization (5% in the WidowX analysis) be improved?
- Why do proprioceptive inputs hurt pretraining, and can causal confusion be avoided?
- How to balance compute cost against image resolution when choosing patch size?

## 📝 Notes on reading

- Version read: arXiv 2405.12213v2 (26 May 2024), matching the packet identifier.
- Figures 1, 2, 3 (dataset pie chart), 4, 6 (model scaling curve) and 5 (zero-shot bar chart) could only be described; per-robot zero-shot success rates in Fig. 5 were not extractable as numbers.
- Table II (p. 7) gives only aggregate ablation rates; the per-task breakdown is Table VI (p. 17). Its caption says "averaged over 40 trials across two language-conditioned tasks and two goal-conditioned tasks".
- Inconsistency: Table I caption says each finetuning domain averages 20 trials, but Appendix F says Berkeley Bimanual was evaluated with 10 trials.
- Inconsistency: Fig. 4 caption lists joint position control for "Berkeley Bimanual" as a new action space, while Section IV-B lists only Berkeley Pick-Up for new action spaces.
- Appendix F, Stanford Coffee, says "a single 3rd-person wrist observation", which is self-contradictory as extracted.
- Octo-Tiny (10M) appears only in the scaling study; it is not among the released checkpoints listed on p. 5.
- The first author field reads "Octo Model Team"; the citation uses "Team" to match the citekey.

## Suggested new concepts

- Generalist robot policy — recurring category (RT-X, RoboCat, GNM, Octo) worth a hub note.
- Open X-Embodiment dataset — the shared pretraining corpus for several cross-embodiment policies.
- Diffusion policy action head — design choice with ablation evidence here versus MSE and discrete heads.
- Action chunking — recurring technique in imitation learning policies.
- Cross-embodiment finetuning — adapting a pretrained policy to new sensors, action spaces and robots.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Política generalista con cabeza de difusión, fácil de ajustar
