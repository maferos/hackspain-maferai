---
aliases: ["ACRONYM", "Acronym"]
type: concept
element_type: instrument
topic: "[[Visuomotor and vision-language-action robot policies]]"
topics: ["[[Visuomotor and vision-language-action robot policies]]"]
created: 2026-09-19
---

## Working definition

A large simulated grasp dataset of ShapeNet object meshes, each with many physics-checked parallel-jaw grasps, that is widely used to train and evaluate 6-DoF grasp generators.

## Evidence

- [[Sundermeyer2021contact - Contact-GraspNet Efficient 6-DoF Grasp Generation in#^sundermeyer2021contact-019]] — Training uses the ACRONYM dataset, which consists of 8872 meshes from ShapeNet with 17.7 million simulated grasps under varying friction.
- [[Bukhari2026fast - Fast Generative Grasping via Lie Group-Constrained MeanFlow#^bukhari2026fast-025]] — Training and evaluation use ten ACRONYM shape categories, amounting to 416 object instances with about 780 K valid grasps.
- [[Bukhari2026fast - Fast Generative Grasping via Lie Group-Constrained MeanFlow#^bukhari2026fast-061]] — The authors conclude the model attains grasp quality comparable to multi-step diffusion and flow baselines on ACRONYM at up to 39× lower latency.
- [[Urain2022se - SE(3)-DiffusionFields#^urain2022se-027]] — The grasp model is trained on Acronym successful grasp poses for 90 different mugs, approximately 90K 6DoF grasp poses in total.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 3 sources · topic: Visuomotor and vision-language-action robot policies (drafter's packet `q7-policies-sim`, confirmed at the gate)
