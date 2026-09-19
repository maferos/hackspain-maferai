---
aliases: []
type: concept
element_type: method
topic: "[[Visuomotor and vision-language-action robot policies]]"
topics: ["[[Visuomotor and vision-language-action robot policies]]"]
created: 2026-09-18
---

## Working definition

A flow matching policy generates actions by integrating a learned, observation-conditioned velocity field that carries Gaussian noise to actions, a simulation-free alternative to diffusion sampling that usually needs few integration steps.

## Evidence

- [[Black2024vision - π0 A Vision-Language-Action Flow Model for General Robot#^black2024vision-001]] — π0 adds flow matching action outputs to the pre-trained PaliGemma vision-language model to generate continuous action distributions for robot control.
- [[Black2024vision - π0 A Vision-Language-Action Flow Model for General Robot#^black2024vision-003]] — π0 uses an action chunking architecture with flow matching, a variant of diffusion, to represent complex continuous action distributions.
- [[Braun2024riemannian - Riemannian Flow Matching Policy for Robot Motion Learning#^braun2024riemannian-006]] — The authors state their flow matching choice stems from avoiding complex normalizing-flow training procedures and the computationally expensive inference of diffusion models
- [[Braun2024riemannian - Riemannian Flow Matching Policy for Robot Motion Learning#^braun2024riemannian-008]] — The paper adopts the Gaussian conditional flow matching of Lipman et al., with a probability path from a zero-mean normal toward each target sample
- [[Zhang2025reinflow - ReinFlow Fine-tuning Flow Matching Policy with Online RL#^zhang2025reinflow-001]] — ReinFlow is proposed as an online reinforcement learning framework that fine-tunes a family of flow matching policies for continuous robotic control.
- [[Zhang2025reinflow - ReinFlow Fine-tuning Flow Matching Policy with Online RL#^zhang2025reinflow-002]] — ReinFlow injects learnable noise into a flow policy's deterministic path, converting the flow into a discrete-time Markov process for exact likelihood computation.
- [[Zhang2025reinflow - ReinFlow Fine-tuning Flow Matching Policy with Online RL#^zhang2025reinflow-005]] — The authors argue that imitation-trained flow policies lack a built-in exploration mechanism, so robots trained on imperfect data could struggle on challenging tasks.
- [[Zhang2025reinflow - ReinFlow Fine-tuning Flow Matching Policy with Online RL#^zhang2025reinflow-015]] — After fine-tuning the noise network is discarded, recovering a flow matching policy that is still made up of deterministic maps.
- [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World#^intelligence2025vision-012]] — π0.5 is trained in two stages: pre-training with discrete FAST action tokens, then post-training with flow matching for continuous actions.
- [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World#^intelligence2025vision-067]] — The action expert is a smaller transformer with 300M parameters, trained with flow matching over an action horizon of 50.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (4 sources) · topic: Visuomotor and vision-language-action robot policies (drafter's packet `p5-robot-policies`, confirmed at the gate)
