---
aliases: ["RFM"]
type: concept
element_type: method
topic: "[[Riemannian and Lie-group methods for robot motion and optimization]]"
topics: ["[[Riemannian and Lie-group methods for robot motion and optimization]]"]
created: 2026-09-18
---

## Working definition

Riemannian flow matching trains a continuous normalizing flow on a Riemannian manifold by regressing a vector field onto conditional vector fields defined through a premetric such as geodesic distance, which is simulation-free on manifolds with closed-form geodesics.

## Evidence

- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-001]] — Riemannian Flow Matching learns continuous normalizing flows on general Riemannian manifolds by regressing an implicitly defined target vector field.
- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-002]] — To address the intractability of the target field, RFM regresses onto conditional vector fields that push the base toward individual training examples.
- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-004]] — On simple geometries with closed-form geodesics, such as hyperspheres, hyperbolic space and tori, Riemannian Flow Matching remains completely simulation-free.
- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-006]] — Table 1 marks Riemannian Flow Matching as the only compared method combining simulation-free training, a closed-form target and no divergence.
- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-024]] — On the volcano dataset, Riemannian Flow Matching with geodesic reached test NLL -7.93±1.67, versus -6.61±0.96 for the Riemannian Diffusion Model.
- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-026]] — On earthquake data, Riemannian Flow Matching scored -0.28±0.08 test NLL, behind the Riemannian Diffusion Model at -0.40±0.05.
- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-028]] — On the 7D RNA torus dataset, Riemannian Flow Matching reached test NLL -5.20±0.067, versus -3.70±0.592 for the Riemannian Diffusion Model.
- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-031]] — On high-dimensional tori, Riemannian Flow Matching shows no significant drop in log-likelihood per dimension as dimension increases.
- [[Braun2024riemannian - Riemannian Flow Matching Policy for Robot Motion Learning#^braun2024riemannian-007]] — RFMP accounts for full-pose trajectories by building on the Riemannian extension of flow matching proposed by Chen and Lipman
- [[Braun2024riemannian - Riemannian Flow Matching Policy for Robot Motion Learning#^braun2024riemannian-011]] — RFMP adapts Riemannian flow matching to policies by conditioning the parametrized vector field on the observation vector

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 2 sources · topic: Riemannian and Lie-group methods for robot motion and optimization (drafter's packet `p2-riemannian-robot-motion`, confirmed at the gate)
