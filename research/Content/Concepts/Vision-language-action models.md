---
aliases: ["VLA"]
type: concept
element_type: framework
topic: "[[Visuomotor and vision-language-action robot policies]]"
topics: ["[[Visuomotor and vision-language-action robot policies]]"]
created: 2026-09-18
---

## Working definition

Vision-language-action models are pre-trained vision-language models further trained to output robot actions from images and language instructions, so that web-scale visual and semantic knowledge transfers to robot control.

## Evidence

- [[Black2024vision - π0 A Vision-Language-Action Flow Model for General Robot#^black2024vision-004]] — Prior vision-language-action models employ autoregressive discretization to represent actions in a manner analogous to text tokens.
- [[Black2024vision - π0 A Vision-Language-Action Flow Model for General Robot#^black2024vision-005]] — The authors describe π0 as, to their knowledge, the first flow matching VLA that produces high-frequency action chunks for dexterous control.
- [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World#^intelligence2025vision-001]] — π0.5 is a vision-language-action model built on π0 that uses co-training on heterogeneous tasks to enable broad generalization.
- [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model#^kim2024openvla-001]] — OpenVLA is a 7B-parameter open-source vision-language-action model trained on 970k robot demonstrations from the Open X-Embodiment dataset.
- [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model#^kim2024openvla-002]] — The authors argue that current VLAs are closed, with limited visibility into model architecture, training procedures, or data mixture.
- [[Liu2024rdt - RDT-1B a Diffusion Foundation Model for Bimanual#^liu2024rdt-008]] — Prior vision-language-action models discretize action spaces, which the authors link to quantization errors and uncoordinated behaviors in bimanual manipulation.
- [[Zhang2025reinflow - ReinFlow Fine-tuning Flow Matching Policy with Online RL#^zhang2025reinflow-070]] — The experiments use relatively small networks, and scaling ReinFlow to large flow-based vision-language-action models remains an open challenge.
- [[Brohan2023rt - RT-2 Vision-Language-Action Models Transfer Web Knowledge#^brohan2023rt-027]] — The authors suggest the strength of VLA models lies in transferring generalizable visual and semantic concepts from Internet-scale pretraining data.
- [[Brohan2023rt - RT-2 Vision-Language-Action Models Transfer Web Knowledge#^brohan2023rt-054]] — The authors view chain-of-thought results as initial evidence that VLM planners can be combined with low-level policies in one VLA model.
- [[Brohan2023rt - RT-2 Vision-Language-Action Models Transfer Web Knowledge#^brohan2023rt-057]] — The computation cost of large VLA models is high, so real-time inference may become a major bottleneck for high-frequency control.
- [[Pertsch2025fast - FAST Efficient Action Tokenization for#^pertsch2025fast-003]] — The authors argue that highly correlated action tokens diminish the effectiveness of the next-token prediction objective used in autoregressive VLAs.
- [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World#^intelligence2025vision-008]] — Prior works show that co-training VLAs with VLM data mixtures can improve generalization to new objects or unseen scene backgrounds.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 7 sources · topic: Visuomotor and vision-language-action robot policies (drafter's packet `p5-robot-policies`, confirmed at the gate)
