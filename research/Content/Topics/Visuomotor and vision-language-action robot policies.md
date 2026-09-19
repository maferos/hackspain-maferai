---
aliases: []
type: topic
parent: Optimization and learning on manifolds
created: 2026-09-18
---

## Scope

Learned policies that map camera images (and often language instructions and proprioception) directly to low-level robot actions, trained mainly by imitation of demonstrations: how the action output is represented (action chunks, discrete action tokens, diffusion or flow-matching generative heads), the model classes built on them (Diffusion Policy, ACT-style chunked policies, vision-language-action models built on pre-trained VLMs), the pooled multi-robot corpora and cross-embodiment pre-training that feed them, and the recurring problem of multimodal demonstration data. It includes online RL fine-tuning of such generative policies where it acts on the same policy classes. It deliberately excludes the geometry of the action space itself (Lie groups, Riemannian flow matching, equivariant layers), optimisation theory such as natural gradients, hand-crafted Riemannian motion policies, and object-pose perception pipelines, which belong to their own areas even when a policy paper uses them.

## Concepts

- [[Action chunking]] — Action chunking has a policy predict a sequence of several future actions from one observation and execute them (fully or partly) before re-planning, which shortens the effective decision horizon and makes motion more temporally consistent.
- [[Diffusion Policy]] — Diffusion Policy represents a visuomotor policy as a conditional denoising diffusion process over robot action sequences, conditioned on observations, so that it can represent multimodal action distributions learned from demonstrations.
- [[Action tokenization]] — Action tokenization turns continuous robot actions into discrete tokens that a sequence model can predict with next-token prediction, from naive per-dimension binning to compressed or learned tokenizers.
- [[Open X-Embodiment dataset]] — The Open X-Embodiment dataset is a pooled open collection of more than 70 robot manipulation datasets from many robot embodiments, used as the shared pre-training corpus of generalist policies such as RT-X, Octo, OpenVLA and π0.
- [[Vision-language-action models]] — Vision-language-action models are pre-trained vision-language models further trained to output robot actions from images and language instructions, so that web-scale visual and semantic knowledge transfers to robot control.
- [[Flow matching policy]] — A flow matching policy generates actions by integrating a learned, observation-conditioned velocity field that carries Gaussian noise to actions, a simulation-free alternative to diffusion sampling that usually needs few integration steps.
- [[Cross-embodiment pre-training]] — Cross-embodiment pre-training trains one policy on pooled data from many different robots before adapting it to a target robot, so that data from other embodiments improves generalization where target-robot data are scarce.
- [[Multimodal action distributions]] — Multimodal action distributions arise when demonstrations contain several distinct valid actions for the same observation, which single-output regression policies average into infeasible actions while expressive generative policies can represent and commit to one mode.
- [[Sim-to-real transfer]] — Deploying a policy or perception model trained in simulation on a physical robot, which works only insofar as the model survives the gap between simulated and real dynamics, sensing and appearance.
- [[ACRONYM dataset]] — A large simulated grasp dataset of ShapeNet object meshes, each with many physics-checked parallel-jaw grasps, that is widely used to train and evaluate 6-DoF grasp generators.
- [[Domain randomization]] — Training on many simulated environments with randomized textures, lighting, camera, geometry or dynamics, so that the real world looks like just another variation and a model trained only in simulation transfers.

## Subtopics

## Related topics

## ❓ Open questions

## Problems

- none yet: no problem names this topic as its topic

## History

- 2026-09-18 · Eki Gonzalez Flamarique · parent: root — new area for concepts promoted from the research batch, confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · added 3 concepts — concepts from the gap-research batch (04_huecos_y_ampliacion), confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · parent: root → Optimization and learning on manifolds — grouped under the request's three axes
