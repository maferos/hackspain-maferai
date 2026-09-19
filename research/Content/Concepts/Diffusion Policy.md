---
aliases: []
type: concept
element_type: method
topic: "[[Visuomotor and vision-language-action robot policies]]"
topics: ["[[Visuomotor and vision-language-action robot policies]]"]
created: 2026-09-18
---

## Working definition

Diffusion Policy represents a visuomotor policy as a conditional denoising diffusion process over robot action sequences, conditioned on observations, so that it can represent multimodal action distributions learned from demonstrations.

## Evidence

- [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-001]] — Diffusion Policy represents a robot visuomotor policy as a conditional denoising diffusion process over the robot action space.
- [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-003]] — By learning the gradient of the action score function, Diffusion Policy can express arbitrary normalizable distributions, including multimodal action distributions.
- [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-005]] — According to the authors, Diffusion Policy bypasses the negative-sampling requirement by learning the gradient of the energy function.
- [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-007]] — In the vision-conditioned diffusion policy, visual observations are treated as conditioning instead of as part of the joint data distribution.
- [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-011]] — Diffusion Policy outperformed the prior state-of-the-art on all tested benchmarks, with an average success-rate improvement of 46.9%.
- [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-014]] — Diffusion Policy approximates the conditional distribution p(At|Ot) instead of the joint distribution p(At,Ot) used by Janner et al. for planning.
- [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-043]] — In the ablation with simulated latency, Diffusion Policy maintained peak performance with latency up to 4 steps.
- [[Chi2024universal - Universal Manipulation Interface In-The-Wild Robot Teaching#^chi2024universal-023]] — All experiments in the paper use Diffusion Policy as the policy learning framework, with ACT suggested as a potential drop-in replacement.
- [[Yang2024equibot - EquiBot SIM(3)-Equivariant Diffusion Policy#^yang2024equibot-002]] — EquiBot is an equivariant policy learning architecture that builds on diffusion models, specifically the CNN-based Diffusion Policy variant, as its starting point.
- [[Braun2024riemannian - Riemannian Flow Matching Policy for Robot Motion Learning#^braun2024riemannian-028]] — The authors hypothesize that the jerkier Diffusion Policy trajectories result from the inherent stochasticity of diffusion models during inference
- [[Braun2024riemannian - Riemannian Flow Matching Policy for Robot Motion Learning#^braun2024riemannian-033]] — Diffusion Policy does not guarantee trajectories stay on the manifold, and some S-on-S2 trajectories entered the sphere
- [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model#^kim2024openvla-040]] — Both Diffusion Policy versions are competitive with or outperform Octo and OpenVLA on narrower single-instruction tasks like Put Carrot in Bowl.
- [[Team2024octo - Octo An Open-Source Generalist Robot Policy#^team2024octo-054]] — The authors state the diffusion head likely helps because it can model multi-modal action distributions, unlike the MSE head.

## Relations

- RELATES_TO → [[Multimodal action distributions]]
  · type: solves
  · evidence: [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-003]]

## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 6 sources · topic: Visuomotor and vision-language-action robot policies (drafter's packet `p5-robot-policies`, confirmed at the gate)
