---
aliases: []
type: "source"
title: "Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success"
citekey: "Kim2025fine"
doi: "10.48550/arXiv.2502.19645"
arxiv: "2502.19645"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2502.19645"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Moo Jin Kim", "Chelsea Finn", "Percy Liang"]
sha256: ["b860aa1206b6cfb0ce8be177f961379dd6a133d52cc74ac346636e0f4952a596"]
pdf: "Content/Papers/Kim2025fine.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Kim2025fine.pdf]]

> [!abstract] One-sentence summary
> The paper studies how to fine-tune vision-language-action models and proposes OFT, a recipe of parallel decoding, action chunking, continuous actions and L1 regression that makes OpenVLA both faster and more successful in simulation and on a real bimanual robot.

## Abstract

Recent vision-language-action models (VLAs) build upon pretrained vision-language models and leverage diverse robot datasets to demonstrate strong task execution, language following ability, and semantic generalization. Despite these successes, VLAs struggle with novel robot setups and require fine-tuning to achieve good performance, yet how to most effectively fine-tune them is unclear given many possible strategies. In this work, we study key VLA adaptation design choices such as different action decoding schemes, action representations, and learning objectives for fine-tuning, using OpenVLA as our representative base model. Our empirical analysis informs an Optimized Fine-Tuning (OFT) recipe that integrates parallel decoding, action chunking, a continuous action representation, and a simple L1 regression-based learning objective to altogether improve inference efficiency, policy performance, and flexibility in the model's input-output specifications. We propose OpenVLA-OFT, an instantiation of this recipe, which sets a new state of the art on the LIBERO simulation benchmark, significantly boosting OpenVLA's average success rate across four task suites from 76.5% to 97.1% while increasing action generation throughput by 26$\times$. In real-world evaluations, our fine-tuning recipe enables OpenVLA to successfully execute dexterous, high-frequency control tasks on a bimanual ALOHA robot and outperform other VLAs ($π_0$ and RDT-1B) fine-tuned using their default recipes, as well as strong imitation learning policies trained from scratch (Diffusion Policy and ACT) by up to 15% (absolute) in average success rate. We release code for OFT and pretrained model checkpoints at https://openvla-oft.github.io/. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that fine-tuning is crucial for deploying VLAs on novel robots, yet the most effective adaptation approach remains unclear. (Kim et al., 2025) `ev:asserted` p. 1 ^kim2025fine-001
- Autoregressive action generation in LoRA fine-tuned OpenVLA remains too slow, at 3-5 Hz, for high-frequency control at 25-50+ Hz. (Kim et al., 2025) `ev:cited` p. 1 ^kim2025fine-002
- Recent action tokenization schemes achieve 2 to 13× speedups, yet FAST still shows latency of 750 ms between action chunks. (Kim et al., 2025) `ev:cited` p. 1 ^kim2025fine-003
- The study compares three design choices for fine-tuning: action decoding scheme, action representation, and learning objective, using OpenVLA as base model. (Kim et al., 2025) `ev:reported` p. 1 ^kim2025fine-004
- OpenVLA is a 7B-parameter manipulation policy created by fine-tuning the Prismatic VLM on 1M episodes from the Open X-Embodiment dataset. (Kim et al., 2025) `ev:cited` p. 3 ^kim2025fine-005
- Under the original OpenVLA formulation, generating even a single-timestep action takes 0.33 seconds on an NVIDIA A100 GPU. (Kim et al., 2025) `ev:reported` p. 3 ^kim2025fine-006
- OpenVLA was adapted through LoRA fine-tuning given relatively small training datasets, 500 demonstrations versus 1M demonstrations for pretraining. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025fine-007
- Parallel decoding feeds empty action embeddings as decoder input and replaces the causal attention mask with bidirectional attention. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025fine-008
- The L1 regression variant replaces the decoder output embedding layer with an MLP action head that outputs continuous action values. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025fine-009
- The diffusion variant requires multiple forward passes during inference, 50 diffusion steps in this implementation, which impacts deployment latency. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025fine-010
- Low-dimensional robot state is mapped by a separate projection network into the language embedding space as one additional input embedding. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025fine-011
- FiLM projects the average of the task language embeddings into scaling and shifting vectors that modulate the visual features. (Kim et al., 2025) `ev:reported` p. 4 ^kim2025fine-012
- The authors report that treating individual patch embeddings as the features modulated by FiLM results in poor language following. (Kim et al., 2025) `ev:asserted` p. 4 ^kim2025fine-013
- FiLM is applied after self-attention and before the feedforward layer in each vision transformer block, with separate projectors per block. (Kim et al., 2025) `ev:reported` p. 5 ^kim2025fine-014
- FiLM was reserved for the ALOHA experiments, where multiple camera viewpoints lead to a larger presence of spurious visual correlations. (Kim et al., 2025) `ev:reported` p. 5 ^kim2025fine-015
- Each LIBERO task suite provides 500 expert demonstrations across 10 tasks performed by a simulated Franka Emika Panda arm. (Kim et al., 2025) `ev:reported` p. 5 ^kim2025fine-016
- For LIBERO methods using action chunking, chunk size was set to K = 8 to match the Diffusion Policy baseline. (Kim et al., 2025) `ev:reported` p. 5 ^kim2025fine-017
- Parallel decoding with action chunking raised the LIBERO average success rate of fine-tuned OpenVLA from 76.5% to 90.2%. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-018
- On LIBERO-Long, parallel decoding with action chunking raised the success rate of fine-tuned OpenVLA from 53.7% to 86.5%. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-019
- The authors suggest action chunking helps capture temporal dependencies and reduce compounding errors, leading to more reliable task execution. (Kim et al., 2025) `ev:asserted` p. 5 ^kim2025fine-020
- Continuous action variants improved LIBERO success rates by 5% (absolute) over the discrete action variant with parallel decoding and chunking. (Kim et al., 2025) `ev:measured` p. 5 ^kim2025fine-021
- The authors attribute the gain from continuous actions likely to higher precision in the action predictions. (Kim et al., 2025) `ev:asserted` p. 5 ^kim2025fine-022
- L1 regression and diffusion variants achieved comparable LIBERO average success rates of 95.3% and 95.4% respectively. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-023
- OpenVLA-OFT with wrist image and proprioception reached 97.1% average LIBERO success rate, above fine-tuned π0 at 94.2%. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-024
- On LIBERO-Long, OpenVLA-OFT with additional inputs reached 94.5%, above fine-tuned π0 at 85.2% and π0 + FAST at 60.2%. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-025
- Parallel decoding alone raised OpenVLA action generation throughput from 4.2 Hz to 15.9 Hz on an NVIDIA A100 GPU. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-026
- Adding action chunking with K = 8 increased latency by 17% due to longer attention sequences in the decoder. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-027
- Parallel decoding with action chunking reached 108.8 Hz throughput, a 26× speedup over baseline OpenVLA on LIBERO queries. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-028
- The L1 regression variant showed negligible efficiency difference, reaching 109.7 Hz throughput with 0.0729 seconds latency. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-029
- The 50-step diffusion variant had 1.9070 seconds latency but the same 4.2 Hz effective throughput as baseline OpenVLA. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-030
- Diffusion variant success on LIBERO-Long decreased with fewer test-time denoising steps, from 91.1% at 50 steps to 85.7% at 2 steps. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-031
- With a single test-time denoising step, the diffusion variant reached 109.4 Hz throughput but 0.0% LIBERO-Long success. (Kim et al., 2025) `ev:measured` p. 6 ^kim2025fine-032
- Adding a wrist camera image doubles the number of visual patch embeddings passed into the decoder, from 256 to 512. (Kim et al., 2025) `ev:reported` p. 7 ^kim2025fine-033
- With wrist image and proprioceptive inputs added, the fine-tuned OpenVLA policy maintained 71.4 Hz throughput and 0.112 sec latency. (Kim et al., 2025) `ev:measured` p. 7 ^kim2025fine-034
- The OFT recipe combines parallel decoding with action chunking, a continuous action representation, and an L1 regression objective. (Kim et al., 2025) `ev:asserted` p. 7 ^kim2025fine-035
- Fine-tuning the Prismatic VLM directly with OFT, without OpenVLA robot pretraining, lowered LIBERO average success from 97.1% to 91.9%. (Kim et al., 2025) `ev:measured` p. 23 ^kim2025fine-036
- A single OpenVLA-OFT policy trained on all four LIBERO suites combined achieved 96.8% average success, comparable to suite-specific policies. (Kim et al., 2025) `ev:measured` p. 23 ^kim2025fine-037
- In LIBERO, adding FiLM to the combined policy gave 97.0% average success versus 96.8% without FiLM. (Kim et al., 2025) `ev:measured` p. 23 ^kim2025fine-038
- The ALOHA platform comprises two ViperX 300 S arms, three camera viewpoints, and 14-dimensional joint angle state inputs. (Kim et al., 2025) `ev:reported` p. 7 ^kim2025fine-039
- ALOHA was operated at 25 Hz, reduced from the original 50 Hz, with actions representing target absolute joint angles. (Kim et al., 2025) `ev:reported` p. 7 ^kim2025fine-040
- OpenVLA pretraining includes single-arm robot data from a single third-person camera, without robot state inputs, at 3-10 Hz control. (Kim et al., 2025) `ev:reported` p. 7 ^kim2025fine-041
- Four ALOHA tasks were designed to test deformable object manipulation, long-horizon skills, tool usage, and language-driven control. (Kim et al., 2025) `ev:reported` p. 7 ^kim2025fine-042
- The put X into pot task used 300 training demonstrations and 24 evaluation trials, half of them out-of-distribution. (Kim et al., 2025) `ev:reported` p. 8 ^kim2025fine-043
- OpenVLA-OFT+ was fine-tuned on each ALOHA task independently with an action chunk size of K = 25. (Kim et al., 2025) `ev:reported` p. 8 ^kim2025fine-044
- RDT-1B and π0, pretrained on bimanual manipulation data, were fine-tuned using their authors' recommended recipes as VLA baselines. (Kim et al., 2025) `ev:reported` p. 8 ^kim2025fine-045
- In the ALOHA experiments, ACT produced less precise actions than other methods and achieved the lowest overall performance. (Kim et al., 2025) `ev:measured` p. 8 ^kim2025fine-046
- The authors suggest Diffusion Policy's struggle on the larger-dataset put X into pot task indicates limited scalability compared to VLAs. (Kim et al., 2025) `ev:asserted` p. 8 ^kim2025fine-047
- The authors suggest RDT-1B's failure to correct scooping mistakes reflects over-reliance on proprioceptive state over visual feedback. (Kim et al., 2025) `ev:asserted` p. 9 ^kim2025fine-048
- π0 was the strongest ALOHA baseline, showing smoother motions and better reactivity to feedback, with better overall task completion than RDT-1B. (Kim et al., 2025) `ev:measured` p. 9 ^kim2025fine-049
- OpenVLA-OFT+ achieved the highest ALOHA performance across both task execution and language following among the evaluated methods. (Kim et al., 2025) `ev:measured` p. 9 ^kim2025fine-050
- On scoop X into bowl, OpenVLA-OFT+ scored 100.00 points, compared with 93.33 for π0 and 73.33 for RDT-1B. (Kim et al., 2025) `ev:measured` p. 23 ^kim2025fine-051
- On put X into pot, OpenVLA-OFT+ scored 51.25 points, above RDT-1B at 44.17 and π0 at 42.08. (Kim et al., 2025) `ev:measured` p. 23 ^kim2025fine-052
- RDT-1B and π0 were pretrained on substantial bimanual datasets, of 6K episodes and 8K hours of bimanual data respectively. (Kim et al., 2025) `ev:cited` p. 9 ^kim2025fine-053
- The authors suggest the fine-tuning technique can be more crucial than pretraining data coverage for downstream performance. (Kim et al., 2025) `ev:asserted` p. 9 ^kim2025fine-054
- Without FiLM, language following dropped to 33% on both language-dependent ALOHA tasks, equal to randomly choosing the correct instruction. (Kim et al., 2025) `ev:measured` p. 9 ^kim2025fine-055
- Without FiLM, OpenVLA-OFT scored 35.00 points on scoop X into bowl, compared with 100.00 for OpenVLA-OFT+. (Kim et al., 2025) `ev:measured` p. 23 ^kim2025fine-056
- On ALOHA, the original OpenVLA formulation with wrist camera inputs reached 1.8 Hz throughput with 0.543 sec latency. (Kim et al., 2025) `ev:measured` p. 9 ^kim2025fine-057
- OpenVLA-OFT+ reached 77.9 Hz throughput with 0.321 seconds latency when processing three images, robot state and a task command. (Kim et al., 2025) `ev:measured` p. 10 ^kim2025fine-058
- With 25-timestep action chunks, OpenVLA-OFT+ achieves 43× faster throughput than base OpenVLA on the bimanual setup. (Kim et al., 2025) `ev:measured` p. 2 ^kim2025fine-059
- ACT reached the highest ALOHA throughput at 432.8 Hz, combining single-pass L1 regression action generation with a compact architecture. (Kim et al., 2025) `ev:measured` p. 10 ^kim2025fine-060
- OpenVLA-OFT+ throughput of 77.9 Hz approaches the 84.1 Hz of RDT-1B despite OpenVLA being 7× larger. (Kim et al., 2025) `ev:measured` p. 10 ^kim2025fine-061
- On BridgeData V2 WidowX tasks, OpenVLA-OFT averaged 69.2% versus 65.8% for the public OpenVLA checkpoint. (Kim et al., 2025) `ev:measured` p. 16 ^kim2025fine-062
- The BridgeData V2 dataset used contains 50,365 real WidowX robot demonstrations, 25× more than the four LIBERO suites combined. (Kim et al., 2025) `ev:reported` p. 16 ^kim2025fine-063
- The authors state that merely expanding the put X into pot training set proved insufficient for satisfactory language grounding. (Kim et al., 2025) `ev:asserted` p. 16 ^kim2025fine-064
- The authors conclude that simple L1 regression with a high-capacity model such as OpenVLA is quite effective for adapting to novel robots. (Kim et al., 2025) `ev:asserted` p. 10 ^kim2025fine-065
- L1 regression may struggle to model truly multimodal action distributions in which multiple valid actions exist for the same input. (Kim et al., 2025) `ev:asserted` p. 10 ^kim2025fine-066
- Diffusion-based approaches may better capture multimodality in demonstrations, but risk overfitting to suboptimal modes in the training data. (Kim et al., 2025) `ev:asserted` p. 10 ^kim2025fine-067
- OpenVLA without FiLM exhibited poor language grounding on ALOHA, despite showing no such issues in the LIBERO simulation experiments. (Kim et al., 2025) `ev:measured` p. 10 ^kim2025fine-068

## 🎯 Contributions

## 📖 Glossary

- **VLA (vision-language-action model)** — Robot policy built by fine-tuning a pretrained vision-language model to output low-level actions.
- **Parallel decoding** — Generating all action outputs in one forward pass using empty embeddings and bidirectional attention.
- **Action chunking** — Predicting and executing a sequence of future actions without intermediate replanning.
- **OFT (Optimized Fine-Tuning)** — Recipe combining parallel decoding, action chunking, continuous actions and L1 regression.
- **OFT+** — OFT augmented with FiLM language conditioning, used for the ALOHA experiments.
- **FiLM** — Feature-wise linear modulation: language-derived scale and shift vectors applied to visual features.
- **LIBERO** — Simulated Franka manipulation benchmark with Spatial, Object, Goal and Long task suites.
- **ALOHA** — Low-cost real bimanual manipulation platform with two arms and three cameras.
- **LoRA** — Parameter-efficient fine-tuning via low-rank adapter matrices added to pretrained weights.
- **Throughput** — Total robot actions generated per second by the policy.

## ❓ Open questions

- How well does OFT with L1 regression handle truly multimodal demonstration datasets?
- Do OFT's benefits extend to large-scale VLA pretraining, or is a more expressive objective like diffusion needed there?
- Why does OpenVLA without FiLM ground language poorly on ALOHA but not in LIBERO: missing bimanual pretraining data or other factors?
- Would the recipe transfer to other base VLAs beyond OpenVLA?
- Can latency (not only throughput) be reduced enough for closed-loop reactivity within an executed chunk?

## 📝 Notes on reading

Version read: arXiv 2502.19645v2 (28 Apr 2025), matching the packet identifier.

Unit inconsistency: Related Work (p. 2) gives parallel-decoding latency as 0.07 ms (single-arm) and 0.321 ms (bimanual), while Tables II and III (pp. 6, 10) report 0.0735 and 0.321 in seconds; the ms figures appear to be a typo and were not claimed.

The 26× speedup (LIBERO, K = 8) and the 43× speedup (ALOHA, K = 25) refer to different setups; the 43× is stated in the introduction (p. 2) without an explicit table row computing it.

Figures 4 and 5 (ALOHA task completion and language following) are bar charts whose values could not be read from the extracted text; per-task values were instead taken from Tables X-XIII (p. 23). Per-task BridgeData V2 scores (Table XVI, p. 24) were not claimed individually; the per-task picture is mixed (OFT lower on three of six tasks).

The fold shorts task is saturated: all methods score 100 (Table X), so it does not discriminate between methods.

## Suggested new concepts

- Action chunking — recurring technique across imitation learning and VLA policies, central to throughput and success gains here.
- Parallel decoding for VLAs — a distinct alternative to autoregressive token generation that other VLA papers may adopt or compare against.
- FiLM language conditioning — general conditioning mechanism reused for language grounding in robot policies.
- LIBERO benchmark — standard simulation benchmark likely to be cited by many VLA sources in the vault.
- ALOHA platform — common bimanual real-robot testbed for dexterous manipulation.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H4.** OpenVLA-OFT: receta de fine-tuning de VLA con acciones continuas, chunks, decodificación paralela y pérdida L1, validada en ALOHA bimanual.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
