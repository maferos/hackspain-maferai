---
aliases: []
type: concept
element_type: process
topic: "[[Visuomotor and vision-language-action robot policies]]"
topics: ["[[Visuomotor and vision-language-action robot policies]]"]
created: 2026-09-18
---

## Working definition

Cross-embodiment pre-training trains one policy on pooled data from many different robots before adapting it to a target robot, so that data from other embodiments improves generalization where target-robot data are scarce.

## Evidence

- [[Liu2024rdt - RDT-1B a Diffusion Foundation Model for Bimanual#^liu2024rdt-002]] — The authors mitigate dual-arm data scarcity through cross-robot pretraining, which they say amplifies data volume by three orders of magnitude.
- [[Liu2024rdt - RDT-1B a Diffusion Foundation Model for Bimanual#^liu2024rdt-012]] — RDT is first pre-trained on a large-scale multi-robot dataset that is mostly single-arm, then fine-tuned on a target-robot dataset.
- [[Liu2024rdt - RDT-1B a Diffusion Foundation Model for Bimanual#^liu2024rdt-052]] — The authors attribute RDT's few-shot learning of handover and folding skills, whose action patterns differ greatly from known skills, to large-scale pre-training.
- [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World#^intelligence2025vision-005]] — The authors argue that low-level action inference benefits from action data collected by other robots, including simpler static robots elsewhere.
- [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World#^intelligence2025vision-023]] — The laboratory cross-embodiment data span single-arm and dual-arm manipulators with static and mobile bases, plus the open-source OXE dataset.
- [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World#^intelligence2025vision-047]] — Excluding either cross-embodiment source, ME or CE data, significantly degrades performance on the end-to-end mock home tasks.
- [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World#^intelligence2025vision-066]] — Dishes in Sink remains relatively robust to removing web data but degrades when cross-embodiment data are excluded.
- [[Pertsch2025fast - FAST Efficient Action Tokenization for#^pertsch2025fast-060]] — The generalist π0-FAST is trained on the π0 cross-embodied data mixture, which includes 903M timesteps from the authors' own datasets.
- [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model#^kim2024openvla-044]] — OpenVLA (scratch), fine-tuned from Prismatic without OpenX robot pretraining, averaged 43.4% on Franka-Tabletop and 21.7% on Franka-DROID.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (4 sources) · topic: Visuomotor and vision-language-action robot policies (drafter's packet `p5-robot-policies`, confirmed at the gate)
