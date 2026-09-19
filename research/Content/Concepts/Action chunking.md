---
aliases: []
type: concept
element_type: method
topic: "[[Visuomotor and vision-language-action robot policies]]"
topics: ["[[Visuomotor and vision-language-action robot policies]]"]
created: 2026-09-18
---

## Working definition

Action chunking has a policy predict a sequence of several future actions from one observation and execute them (fully or partly) before re-planning, which shortens the effective decision horizon and makes motion more temporally consistent.

## Evidence

- [[Zhao2023learning - Learning Fine-Grained Bimanual Manipulation with Low-Cost#^zhao2023learning-007]] — The authors state that predicting chunks of k actions reduces the effective horizon of the task k-fold, mitigating compounding errors.
- [[Zhao2023learning - Learning Fine-Grained Bimanual Manipulation with Low-Cost#^zhao2023learning-009]] — The action chunking policy is implemented with Transformers and trained as a conditional VAE to capture the variability in human demonstration data.
- [[Zhao2023learning - Learning Fine-Grained Bimanual Manipulation with Low-Cost#^zhao2023learning-027]] — A naive action chunking implementation incorporates new observations abruptly every k steps, which can result in jerky robot motion.
- [[Zhao2023learning - Learning Fine-Grained Bimanual Manipulation with Low-Cost#^zhao2023learning-054]] — Adding action chunking to BC-ConvMLP and VINN gives consistent trends, suggesting chunking is generally beneficial for imitation learning in these settings.
- [[Black2024vision - π0 A Vision-Language-Action Flow Model for General Robot#^black2024vision-003]] — π0 uses an action chunking architecture with flow matching, a variant of diffusion, to represent complex continuous action distributions.
- [[Black2024vision - π0 A Vision-Language-Action Flow Model for General Robot#^black2024vision-058]] — Temporal ensembling of action chunks hurt policy performance in early trials, so chunks are executed open-loop without aggregation.
- [[Liu2024rdt - RDT-1B a Diffusion Foundation Model for Bimanual#^liu2024rdt-017]] — RDT predicts a whole action chunk in one shot to encourage temporal consistency and to alleviate error accumulation over time.
- [[Team2024octo - Octo An Open-Source Generalist Robot Policy#^team2024octo-011]] — A lightweight diffusion action head applied to the readout embeddings predicts a chunk of several consecutive actions, similar to prior work.
- [[Zhang2025reinflow - ReinFlow Fine-tuning Flow Matching Policy with Online RL#^zhang2025reinflow-012]] — With action chunking, the log probability of a chunk equals the sum of the log probabilities of its internal actions under conditional independence.
- [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model#^kim2024openvla-046]] — The authors suggest action chunking and temporal smoothing may help OpenVLA reach Diffusion Policy's dexterity on narrow, highly dexterous tasks.
- [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-006]] — The policy combines high-dimensional action-sequence prediction with receding-horizon control to continuously re-plan its action in a closed-loop manner.
- [[Braun2024riemannian - Riemannian Flow Matching Policy for Robot Motion Learning#^braun2024riemannian-012]] — Inspired by diffusion policies, RFMP predicts a receding horizon of actions to achieve temporal consistency and smoothness in the predicted actions
- [[Pertsch2025fast - FAST Efficient Action Tokenization for#^pertsch2025fast-010]] — For high-frequency robot data, binning tokenization can easily produce hundreds of tokens per action chunk, making training challenging and inference slow.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 9 sources · topic: Visuomotor and vision-language-action robot policies (drafter's packet `p5-robot-policies`, confirmed at the gate)
