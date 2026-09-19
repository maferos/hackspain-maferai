---
aliases: ["action multimodality"]
type: concept
element_type: phenomenon
topic: "[[Visuomotor and vision-language-action robot policies]]"
topics: ["[[Visuomotor and vision-language-action robot policies]]"]
created: 2026-09-18
---

## Working definition

Multimodal action distributions arise when demonstrations contain several distinct valid actions for the same observation, which single-output regression policies average into infeasible actions while expressive generative policies can represent and commit to one mode.

## Evidence

- [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-003]] — By learning the gradient of the action score function, Diffusion Policy can express arbitrary normalizable distributions, including multimodal action distributions.
- [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-028]] — The authors speculate that action multimodality is more pronounced in position-control mode than it is when using velocity control.
- [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action#^chi2023diffusion-029]] — In the Push-T case study, Diffusion Policy learns both the left and right modes, committing to only one mode within each rollout.
- [[Team2024octo - Octo An Open-Source Generalist Robot Policy#^team2024octo-054]] — The authors state the diffusion head likely helps because it can model multi-modal action distributions, unlike the MSE head.
- [[Liu2024rdt - RDT-1B a Diffusion Foundation Model for Bimanual#^liu2024rdt-014]] — A deterministic regression policy may learn the average of action modes, which can yield completely infeasible out-of-distribution actions.
- [[Yang2024equibot - EquiBot SIM(3)-Equivariant Diffusion Policy#^yang2024equibot-006]] — The authors' earlier EquivAct method cannot handle multi-modal training data because of its deterministic architecture.
- [[Yang2024equibot - EquiBot SIM(3)-Equivariant Diffusion Policy#^yang2024equibot-027]] — EquivAct cannot perform well on Push T, which the authors attribute to its deterministic behavior cloning architecture handling multi-modal data poorly.
- [[Chi2024universal - Universal Manipulation Interface In-The-Wild Robot Teaching#^chi2024universal-007]] — The authors state that prior works often use simple policy representations such as MLPs, limiting their capacity to capture multimodal human action distributions.
- [[Braun2024riemannian - Riemannian Flow Matching Policy for Robot Motion Learning#^braun2024riemannian-035]] — Both RFMP and Diffusion Policy learned a multimodal pattern from mirrored letter-L demonstrations on S2

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (6 sources) · topic: Visuomotor and vision-language-action robot policies (drafter's packet `p5-robot-policies`, confirmed at the gate)
