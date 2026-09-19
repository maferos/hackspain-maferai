---
aliases: ["OXE", "OpenX"]
type: concept
element_type: data-modality
topic: "[[Visuomotor and vision-language-action robot policies]]"
topics: ["[[Visuomotor and vision-language-action robot policies]]"]
created: 2026-09-18
---

## Working definition

The Open X-Embodiment dataset is a pooled open collection of more than 70 robot manipulation datasets from many robot embodiments, used as the shared pre-training corpus of generalist policies such as RT-X, Octo, OpenVLA and π0.

## Evidence

- [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model#^kim2024openvla-001]] — OpenVLA is a 7B-parameter open-source vision-language-action model trained on 970k robot demonstrations from the Open X-Embodiment dataset.
- [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model#^kim2024openvla-010]] — At the time of writing, the full OpenX dataset comprised more than 70 individual robot datasets with more than 2M robot trajectories.
- [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model#^kim2024openvla-060]] — Training only on BridgeData V2 instead of the OpenX mixture dropped mean success on eight Bridge tasks from 76.3% to 45.6%.
- [[Team2024octo - Octo An Open-Source Generalist Robot Policy#^team2024octo-001]] — Octo is a transformer-based generalist robot policy pretrained on 800k robot demonstrations from the Open X-Embodiment dataset.
- [[Team2024octo - Octo An Open-Source Generalist Robot Policy#^team2024octo-005]] — The Open X-Embodiment dataset contains approximately 1.5M robot episodes, of which the authors curate 800k for Octo training.
- [[Team2024octo - Octo An Open-Source Generalist Robot Policy#^team2024octo-006]] — The RT-X model was trained on a more restricted subset of 350K episodes from the Open X-Embodiment dataset.
- [[Team2024octo - Octo An Open-Source Generalist Robot Policy#^team2024octo-014]] — Curation removed Open-X datasets that contain no image streams, as well as datasets that do not use delta end-effector control.
- [[Black2024vision - π0 A Vision-Language-Action Flow Model for General Robot#^black2024vision-008]] — According to the authors, the OXE dataset included in the pre-training mixture contains robot data collected from 22 different robots.
- [[Black2024vision - π0 A Vision-Language-Action Flow Model for General Robot#^black2024vision-016]] — 9.1% of the pre-training mixture, counted in timesteps, consists of open-source datasets including OXE, Bridge v2, and DROID.
- [[Liu2024rdt - RDT-1B a Diffusion Foundation Model for Bimanual#^liu2024rdt-009]] — Octo pre-trained a Transformer-based diffusion policy on a subset of 25 Open X-Embodiment datasets, with up to 93M parameters.
- [[Pertsch2025fast - FAST Efficient Action Tokenization for#^pertsch2025fast-061]] — The open-source datasets BRIDGE v2, DROID and OXE make up 9.1% of the generalist π0-FAST training mixture.
- [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World#^intelligence2025vision-023]] — The laboratory cross-embodiment data span single-arm and dual-arm manipulators with static and mobile bases, plus the open-source OXE dataset.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 6 sources · topic: Visuomotor and vision-language-action robot policies (drafter's packet `p5-robot-policies`, confirmed at the gate)
