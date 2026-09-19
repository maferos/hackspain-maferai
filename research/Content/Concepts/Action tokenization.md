---
aliases: []
type: concept
element_type: method
topic: "[[Visuomotor and vision-language-action robot policies]]"
topics: ["[[Visuomotor and vision-language-action robot policies]]"]
created: 2026-09-18
---

## Working definition

Action tokenization turns continuous robot actions into discrete tokens that a sequence model can predict with next-token prediction, from naive per-dimension binning to compressed or learned tokenizers.

## Evidence

- [[Brohan2023rt - RT-2 Vision-Language-Action Models Transfer Web Knowledge#^brohan2023rt-003]] — RT-2 trains pre-existing vision-language models without any new parameters to output robot actions encoded as text.
- [[Brohan2023rt - RT-2 Vision-Language-Action Models Transfer Web Knowledge#^brohan2023rt-012]] — When prompted with a robot-action task, RT-2 decoding is constrained to sample only valid action tokens.
- [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model#^kim2024openvla-008]] — Since the Llama tokenizer reserves only 100 special tokens, OpenVLA overwrites the 256 least used vocabulary tokens with action tokens.
- [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model#^kim2024openvla-009]] — OpenVLA is trained with a standard next-token prediction objective, evaluating the cross-entropy loss on the predicted action tokens only.
- [[Pertsch2025fast - FAST Efficient Action Tokenization for#^pertsch2025fast-001]] — Prior autoregressive robot policies typically tokenize continuous actions with a naive per-dimension, per-timestep binning scheme, as in RT-1, RT-2 and OpenVLA.
- [[Pertsch2025fast - FAST Efficient Action Tokenization for#^pertsch2025fast-007]] — FAST+ is a universal action tokenizer trained on 1M real robot action trajectories covering diverse embodiments, action spaces and control frequencies.
- [[Pertsch2025fast - FAST Efficient Action Tokenization for#^pertsch2025fast-008]] — The authors find that vector-quantized action tokenizers fail on high-frequency tasks requiring fine-grained control, despite performing well at coarse, low-fidelity reconstruction.
- [[Pertsch2025fast - FAST Efficient Action Tokenization for#^pertsch2025fast-009]] — Binning tokenization discretizes each action dimension independently into N uniform bins over the training range, most commonly with N = 256.
- [[Pertsch2025fast - FAST Efficient Action Tokenization for#^pertsch2025fast-044]] — Tokenizers that compress action targets, FAST and FSQ, lead to substantially more efficient training than the naive binning tokenization of prior VLAs.
- [[Black2024vision - π0 A Vision-Language-Action Flow Model for General Robot#^black2024vision-004]] — Prior vision-language-action models employ autoregressive discretization to represent actions in a manner analogous to text tokens.
- [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World#^intelligence2025vision-012]] — π0.5 is trained in two stages: pre-training with discrete FAST action tokens, then post-training with flow matching for continuous actions.
- [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World#^intelligence2025vision-017]] — Discrete action representations are less well-suited for real-time inference because they require expensive autoregressive decoding.
- [[Team2024octo - Octo An Open-Source Generalist Robot Policy#^team2024octo-048]] — Replacing the diffusion head with discretized action prediction lowered aggregate WidowX ablation success to 18%, against 83% for Octo-Small.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 6 sources · topic: Visuomotor and vision-language-action robot policies (drafter's packet `p5-robot-policies`, confirmed at the gate)
