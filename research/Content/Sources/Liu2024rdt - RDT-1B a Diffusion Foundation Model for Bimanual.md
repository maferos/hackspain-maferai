---
aliases: []
type: "source"
title: "RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation"
citekey: "Liu2024rdt"
doi: "10.48550/arXiv.2410.07864"
arxiv: "2410.07864"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2410.07864"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Songming Liu", "Lingxuan Wu", "Bangguo Li", "Hengkai Tan", "Huayu Chen", "Zhengyi Wang", "Ke Xu", "Hang Su", "Jun Zhu"]
sha256: ["fabfa885b63f2d68b8e7868549563c346d4323a596d24ee3e43d0a62b4ef9667"]
pdf: "Content/Papers/Liu2024rdt.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Liu2024rdt.pdf]]

> [!abstract] One-sentence summary
> RDT-1B is a 1.2B-parameter diffusion Transformer policy pre-trained on 46 multi-robot datasets through a physically interpretable unified action space and fine-tuned on 6K+ bimanual episodes, outperforming ACT, OpenVLA and Octo on real-robot generalization, few-shot and dexterity tasks.

## Abstract

Bimanual manipulation is essential in robotics, yet developing foundation models is extremely challenging due to the inherent complexity of coordinating two robot arms (leading to multi-modal action distributions) and the scarcity of training data. In this paper, we present the Robotics Diffusion Transformer (RDT), a pioneering diffusion foundation model for bimanual manipulation. RDT builds on diffusion models to effectively represent multi-modality, with innovative designs of a scalable Transformer to deal with the heterogeneity of multi-modal inputs and to capture the nonlinearity and high frequency of robotic data. To address data scarcity, we further introduce a Physically Interpretable Unified Action Space, which can unify the action representations of various robots while preserving the physical meanings of original actions, facilitating learning transferrable physical knowledge. With these designs, we managed to pre-train RDT on the largest collection of multi-robot datasets to date and scaled it up to 1.2B parameters, which is the largest diffusion-based foundation model for robotic manipulation. We finally fine-tuned RDT on a self-created multi-task bimanual dataset with over 6K+ episodes to refine its manipulation capabilities. Experiments on real robots demonstrate that RDT significantly outperforms existing methods. It exhibits zero-shot generalization to unseen objects and scenes, understands and follows language instructions, learns new skills with just 1~5 demonstrations, and effectively handles complex, dexterous tasks. We refer to https://rdt-robotics.github.io/rdt-robotics/ for the code and videos. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that current bimanual approaches either depend on task-specific primitives or are limited to small-scale models, data and simple tasks. (Liu et al., 2024) `ev:cited` p. 1 ^liu2024rdt-001
- The authors mitigate dual-arm data scarcity through [[Cross-embodiment pre-training|cross-robot pretraining]], which they say amplifies data volume by three orders of magnitude. (Liu et al., 2024) `ev:asserted` p. 1 ^liu2024rdt-002
- Existing cross-robot solutions discard structurally inconsistent robots or keep only invariant features, sacrificing data diversity the authors consider essential for generalization. (Liu et al., 2024) `ev:cited` p. 2 ^liu2024rdt-003
- RDT uses a diffusion transformer (DiT) as its scalable backbone, with special designs for language-conditioned bimanual manipulation. (Liu et al., 2024) `ev:reported` p. 2 ^liu2024rdt-004
- RDT modifies the original DiT structure with MLP decoding, improved normalization, and alternate injection of conditions to suit robotic data. (Liu et al., 2024) `ev:reported` p. 2 ^liu2024rdt-005
- The authors report that RDT outperforms baselines with an improvement of 56% in success rates across a wide spectrum of challenging tasks. (Liu et al., 2024) `ev:measured` p. 2 ^liu2024rdt-006
- The ALOHA dual-arm robot, consisting of two arms with grippers and three cameras, serves as the target robot for hardware evaluation. (Liu et al., 2024) `ev:reported` p. 3 ^liu2024rdt-007
- [[Vision-language-action models|Prior vision-language-action models]] discretize action spaces, which the authors link to quantization errors and uncoordinated behaviors in bimanual manipulation. (Liu et al., 2024) `ev:cited` p. 3 ^liu2024rdt-008
- Octo pre-trained a Transformer-based diffusion policy on a subset of 25 [[Open X-Embodiment dataset|Open X-Embodiment datasets]], with up to 93M parameters. (Liu et al., 2024) `ev:cited` p. 3 ^liu2024rdt-009
- The policy observation combines an RGB image history, low-dimensional robot proprioception, and the control frequency, conditioned on a language instruction. (Liu et al., 2024) `ev:reported` p. 3 ^liu2024rdt-010
- The authors state that available data for a specific dual-arm robot is particularly scarce, under 10K trajectories, due to high hardware costs. (Liu et al., 2024) `ev:asserted` p. 4 ^liu2024rdt-011
- RDT is first pre-trained on [[Cross-embodiment pre-training|a large-scale multi-robot dataset]] that is mostly single-arm, then fine-tuned on a target-robot dataset. (Liu et al., 2024) `ev:reported` p. 4 ^liu2024rdt-012
- The authors state their goal is enhancing bimanual generalizability with multi-robot data rather than developing a cross-embodiment model for various robots. (Liu et al., 2024) `ev:asserted` p. 4 ^liu2024rdt-013
- A deterministic regression policy may learn [[Multimodal action distributions|the average of action modes]], which can yield completely infeasible out-of-distribution actions. (Liu et al., 2024) `ev:cited` p. 5 ^liu2024rdt-014
- The authors argue that diffusion sampling overhead is minor for actions, since they have a much lower dimension than images. (Liu et al., 2024) `ev:asserted` p. 5 ^liu2024rdt-015
- The authors describe robotic physics quantities as having nonlinear dynamics, potential high-frequency changes, and an unstable numerical range, unlike images. (Liu et al., 2024) `ev:asserted` p. 5 ^liu2024rdt-016
- RDT predicts a whole [[Action chunking|action chunk]] in one shot to encourage temporal consistency and to alleviate error accumulation over time. (Liu et al., 2024) `ev:reported` p. 5 ^liu2024rdt-017
- The denoising network is trained by minimizing a mean-squared error between the clean action and its estimate from a noisy action. (Liu et al., 2024) `ev:reported` p. 5 ^liu2024rdt-018
- Low-dimensional inputs, including proprioception, the action chunk and the control frequency, are encoded with MLPs using Fourier features. (Liu et al., 2024) `ev:reported` p. 6 ^liu2024rdt-019
- Image inputs are encoded by the pre-trained SigLIP vision encoder, whose weights stay fixed during training to save GPU memory. (Liu et al., 2024) `ev:reported` p. 6 ^liu2024rdt-020
- Language instructions are encoded by the pre-trained T5-XXL language model, whose weights are also fixed during training to save GPU memory. (Liu et al., 2024) `ev:reported` p. 6 ^liu2024rdt-021
- Stochastic independent masking across modalities during encoding aims to prevent overreliance on exterior views at the expense of wrist-camera details. (Liu et al., 2024) `ev:reported` p. 6 ^liu2024rdt-022
- The loss curves show that large-scale pre-training tends to be very unstable or even explode without QKNorm and RMSNorm. (Liu et al., 2024) `ev:measured` p. 6 ^liu2024rdt-023
- Without the nonlinear MLP decoder, RDT cannot effectively capture nonlinear dynamics and loses the ability to accomplish dexterous tasks. (Liu et al., 2024) `ev:measured` p. 6 ^liu2024rdt-024
- Simultaneous injection of image and text tokens tends to overshadow text-related information, impairing instruction following in the authors' ablation. (Liu et al., 2024) `ev:measured` p. 6 ^liu2024rdt-025
- Alternating Condition Injection alternates image and text tokens in successive layers' cross-attention rather than injecting both in every layer. (Liu et al., 2024) `ev:reported` p. 7 ^liu2024rdt-026
- The unified action space places each element of a robot's action vector at the position matching its physical meaning, padding the remaining positions. (Liu et al., 2024) `ev:reported` p. 7 ^liu2024rdt-027
- The pre-training collection includes 46 datasets of various robots, with a total size of 1M+ trajectories and 21TB. (Liu et al., 2024) `ev:reported` p. 7 ^liu2024rdt-028
- The self-collected fine-tuning dataset contains 6K+ trajectories spanning 300+ challenging tasks, from pick-and-place to plugging cables. (Liu et al., 2024) `ev:reported` p. 7 ^liu2024rdt-029
- The fine-tuning dataset uses 100+ rigid and non-rigid objects of various sizes and textures in 15+ different rooms. (Liu et al., 2024) `ev:reported` p. 7 ^liu2024rdt-030
- The authors use GPT-4-Turbo to rewrite the human-annotated instructions, aiming to increase the text diversity of the fine-tuning dataset. (Liu et al., 2024) `ev:reported` p. 7 ^liu2024rdt-031
- RDT is scaled to 1.2B parameters and pre-trained on 48 H100 80GB GPUs for a month, giving 1M training steps. (Liu et al., 2024) `ev:reported` p. 8 ^liu2024rdt-032
- Fine-tuning the model takes three days on the same GPUs, running for 130K steps in total. (Liu et al., 2024) `ev:reported` p. 8 ^liu2024rdt-033
- At inference, DPM-Solver++ reduces the diffusion steps needed to sample an action chunk from 100 steps to 5 steps. (Liu et al., 2024) `ev:reported` p. 8 ^liu2024rdt-034
- RDT achieves an action chunk inference frequency of 6 Hz on the target robot's onboard RTX 4090 24GB GPU. (Liu et al., 2024) `ev:measured` p. 8 ^liu2024rdt-035
- The average action inference frequency of RDT reaches 381 Hz, counted as actions per second on the target robot. (Liu et al., 2024) `ev:measured` p. 8 ^liu2024rdt-036
- Evaluation uses seven real-robot tasks probing unseen objects, unseen scenes, instruction following, few-shot learning, and dexterity. (Liu et al., 2024) `ev:reported` p. 9 ^liu2024rdt-037
- Baselines are ACT, the 7B-parameter OpenVLA using discretization, and the diffusion-based Octo whose largest version has only 93M parameters. (Liu et al., 2024) `ev:reported` p. 9 ^liu2024rdt-038
- Success rate, computed by dividing successful trials by total trials, is the main metric of the real-robot experiments. (Liu et al., 2024) `ev:reported` p. 9 ^liu2024rdt-039
- Handover, Fold Shorts, and Robot Dog are each tested with 25 trials on the ALOHA dual-arm robot. (Liu et al., 2024) `ev:reported` p. 9 ^liu2024rdt-040
- In the ablation, RDT without diffusion modeling scores 12.5 on the unseen-object task, against 50 for the full RDT. (Liu et al., 2024) `ev:measured` p. 9 ^liu2024rdt-041
- RDT trained from scratch without pre-training scores 0 on the unseen-object ablation task, against 50 for the pre-trained RDT. (Liu et al., 2024) `ev:measured` p. 9 ^liu2024rdt-042
- The 166M-parameter RDT (small) scores 25 on instruction following in the ablation, against 100 for the full RDT. (Liu et al., 2024) `ev:measured` p. 9 ^liu2024rdt-043
- The authors attribute RDT's advantage to diffusion with a powerful architecture, arguing discretization and VAE lack accuracy and expressiveness respectively. (Liu et al., 2024) `ev:asserted` p. 9 ^liu2024rdt-044
- In Wash Cup and Pour Water, RDT's performance on unseen scenarios is not much different from that on seen ones. (Liu et al., 2024) `ev:measured` p. 9 ^liu2024rdt-045
- RDT understands which hand to use and how much water to pour, even though it never saw words like one-third. (Liu et al., 2024) `ev:measured` p. 9 ^liu2024rdt-046
- In Wash Cup, OpenVLA and Octo score 0 on every sub-task for the seen cup and both unseen cups. (Liu et al., 2024) `ev:measured` p. 10 ^liu2024rdt-047
- On Fold Shorts with one demonstration, RDT reaches a total success of 68, against 40 from scratch and 0 for ACT. (Liu et al., 2024) `ev:measured` p. 10 ^liu2024rdt-048
- In the 5-shot Handover task, RDT reaches a total success of 40, while ACT, OpenVLA and Octo all score 0. (Liu et al., 2024) `ev:measured` p. 10 ^liu2024rdt-049
- In Robot Dog, RDT makes the dog walk straight with a success of 48, compared with 32 for ACT. (Liu et al., 2024) `ev:measured` p. 10 ^liu2024rdt-050
- The authors suggest the black joystick on a black remote probably makes ACT prone to failure in the Robot Dog task. (Liu et al., 2024) `ev:asserted` p. 10 ^liu2024rdt-051
- The authors attribute RDT's few-shot learning of handover and folding skills, whose action patterns differ greatly from known skills, to [[Cross-embodiment pre-training|large-scale pre-training]]. (Liu et al., 2024) `ev:asserted` p. 10 ^liu2024rdt-052
- RDT (scratch) performs poorly on unseen objects and scenes, which the authors read as showing pre-training knowledge is critical for generalization. (Liu et al., 2024) `ev:asserted` p. 10 ^liu2024rdt-053
- During training, each input from the various modalities is independently masked with a probability of 10% in the encoding stage. (Liu et al., 2024) `ev:reported` p. 19 ^liu2024rdt-054
- The Physically Interpretable Unified Action Space has a dimensionality of 128, meant to include all the main physical quantities of robots. (Liu et al., 2024) `ev:reported` p. 19 ^liu2024rdt-055
- For single-arm robots, the arm is mapped to the right-arm positions of the unified action vector in RDT pre-training. (Liu et al., 2024) `ev:reported` p. 20 ^liu2024rdt-056
- The authors increased sampling weights of slow-convergent datasets during pre-training, based on their observed intermediate loss results. (Liu et al., 2024) `ev:reported` p. 20 ^liu2024rdt-057
- Instead of strict normalization, the authors roughly align dataset scales by unifying the units of physical quantities such as metres and radians. (Liu et al., 2024) `ev:reported` p. 21 ^liu2024rdt-058
- The authors argue that rescaling physical quantities would destroy shared properties across datasets and impair the model's ability to transfer across robots. (Liu et al., 2024) `ev:asserted` p. 21 ^liu2024rdt-059
- Historical proprioceptions are excluded from the inputs to prevent the model from learning shortcuts using the low-dimensional inputs only. (Liu et al., 2024) `ev:reported` p. 21 ^liu2024rdt-060
- For each fine-tuning task, GPT-4-Turbo generates 100 expanded instructions and one simplified instruction to augment the manual annotations. (Liu et al., 2024) `ev:reported` p. 21 ^liu2024rdt-061
- To separate padding from real zeros, a 0-1 availability vector is concatenated with action and proprioception, giving a 256-dimensional vector. (Liu et al., 2024) `ev:reported` p. 23 ^liu2024rdt-062
- The authors empirically observe a general positive correlation between sampled-action MSE on training data and deployment performance on the robot. (Liu et al., 2024) `ev:measured` p. 24 ^liu2024rdt-063
- The authors did not apply Classifier-Free Guidance, finding it brought unstable robot arm behavior without improving model performance. (Liu et al., 2024) `ev:measured` p. 24 ^liu2024rdt-064
- The autonomous mobility of the Cobot Mobile ALOHA was not used during training or inference, so evaluated tasks remain static bimanual manipulation. (Liu et al., 2024) `ev:reported` p. 24 ^liu2024rdt-065
- Due to scheduling reasons, fine-tuning started from the 500K pre-training checkpoint instead of the final 1M checkpoint. (Liu et al., 2024) `ev:reported` p. 25 ^liu2024rdt-066
- In Pour Water-R-2/3, RDT made one pouring mistake and one water-level mistake across the 8 trials shown. (Liu et al., 2024) `ev:measured` p. 28 ^liu2024rdt-067

## 🎯 Contributions

## 📖 Glossary

- **Bimanual manipulation** — Robot manipulation that coordinates two arms, typically with grippers, on one task.
- **Diffusion policy** — Policy that samples actions by iteratively denoising Gaussian noise conditioned on observations.
- **Diffusion Transformer (DiT)** — Transformer backbone used as the denoising network of a diffusion model.
- **Action chunk** — Sequence of future actions predicted in one shot instead of a single step.
- **Physically Interpretable Unified Action Space** — Shared 128-dimensional vector where each slot has a fixed physical meaning across robots.
- **Alternating Condition Injection (ACI)** — Feeding image and text tokens to cross-attention in alternating layers.
- **QKNorm** — Normalization of queries and keys inside attention to avoid numerical instability.
- **RMSNorm** — Layer normalization variant that rescales by root mean square without centering.
- **DPM-Solver++** — Fast diffusion sampler that cuts the number of denoising steps.
- **Multi-modality (actions)** — Several distinct valid action modes for the same observation and instruction.

## ❓ Open questions

- How much of the gain comes from the unified action space itself, since no ablation isolates it from pre-training data volume?
- Do the real-robot success rates hold with more than 8 to 25 trials per task and per condition?
- Would baselines fine-tuned on the full 6K-episode dataset perform differently if their convergence problems were solved?
- Does the model transfer to dual-arm robots other than the ALOHA-style target robot?
- Why did Classifier-Free Guidance destabilize arm behavior, and could a tuned guidance scale help?
- How does performance change when fine-tuning starts from the 1M-step checkpoint instead of the 500K one?

## 📝 Notes on reading

- Version read: arXiv 2410.07864v2 (1 Mar 2025), marked as ICLR 2025 conference paper; matches the packet identifier.
- Figure 1 (p. 2) is garbled in extraction: overall scores 68.2%, 34.8%, 12.2%, 1.7%, 1.6% and a 'pre-training boost by 33.4%' cannot be reliably assigned to methods; not claimed.
- Figure 4b (p. 6) prints 32, 62.5, 12, 12.5 for RDT, w/o MLP and w/o ACI on Dexterity and Instruction Following; the mapping of values to bars is ambiguous, so only the qualitative findings were claimed. These models were not pre-trained.
- Table 3 (p. 10) is flattened into a single column; per-subtask values for Wash Cup, Pour Water and the Pour Water-L-1/3 / R-2/3 columns are ambiguous in grouping. Only unambiguous totals (Fold Shorts, Handover, Robot Dog walk straight) and all-zero rows were claimed.
- The dataset sampling weight formula on p. 20 (initial weight as a function of dataset size Nj, apparently a square root) is garbled in extraction.
- The abstract says 'over 6K+ episodes'; the body uses 6K+ trajectories and 3M+ frames. The body says the collection is the largest to date, a claim not independently checked.
- The 56% improvement (p. 2) is not tied in the text to a specific computation; App. H describes how the Figure 1 overall score is averaged across dimensions.
- OpenVLA and Octo were fine-tuned only on task-relevant demonstrations (about 100 episodes per task) because full-dataset fine-tuning did not converge, whereas RDT used the full fine-tuning set and ACT used 90% of it; this asymmetry matters for the comparison.

## Suggested new concepts

- Unified action space for cross-embodiment pre-training — recurring design choice for mixing heterogeneous robot datasets without discarding structure.
- Diffusion policy — core action-modeling approach contrasted with regression, VAE and discretized VLA policies.
- Action chunking — widely used technique to reduce compounding error and improve temporal consistency.
- Cross-robot pre-training then target-robot fine-tuning — general data-scarcity strategy for bimanual and lab robotics.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Modelo bimanual evaluado en AutoBio (harness en el repo)

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
