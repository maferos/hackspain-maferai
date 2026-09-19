---
aliases: ["RDM"]
type: concept
element_type: method
topic: "[[Probability, filtering and generative models on Lie groups]]"
topics: ["[[Probability, filtering and generative models on Lie groups]]"]
created: 2026-09-19
---

## Working definition

The family of diffusion and score-based generative models that extend continuous-time Euclidean diffusion to data on Riemannian manifolds by noising with manifold Brownian or Langevin dynamics and learning the reverse process, trained either by Riemannian score matching or by a Riemannian continuous-time ELBO.

## Evidence

- [[Huang2022riemannian - Riemannian Diffusion Models#^huang2022riemannian-001]] — The paper generalizes continuous-time diffusion models to arbitrary Riemannian manifolds, calling the resulting model class Riemannian Diffusion Models (RDM).
- [[Huang2022riemannian - Riemannian Diffusion Models#^huang2022riemannian-002]] — RDM uses the Stratonovich SDE formulation, for which the conventional chain rule of calculus holds, unlike the Itô formulation used in Euclidean diffusion.
- [[Huang2022riemannian - Riemannian Diffusion Models#^huang2022riemannian-032]] — Unlike the concurrent Riemannian score-based generative models of De Bortoli et al., RDMs are couched within the maximum likelihood framework.
- [[Huang2022riemannian - Riemannian Diffusion Models#^huang2022riemannian-049]] — The authors observe that RDM outperforms the mixture of power spherical distributions baseline across all the toroidal datasets.
- [[Bortoli2022riemannian - Riemannian Score-Based Generative Modelling#^bortoli2022riemannian-001]] — The authors introduce Riemannian Score-based Generative Models, which define the forward noising diffusion directly on the Riemannian manifold instead of on Euclidean space.
- [[Bortoli2022riemannian - Riemannian Score-Based Generative Modelling#^bortoli2022riemannian-035]] — On the high-dimensional torus, RSGMs fit the target well with linear or constant computational cost depending on the divergence estimator.
- [[Bortoli2022riemannian - Riemannian Score-Based Generative Modelling#^bortoli2022riemannian-039]] — The authors observe RSGMs perform consistently across mixture component counts, whereas exp-wrapped SGMs and Moser flows perform well only in some range.
- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-024]] — On the volcano dataset, [[Riemannian flow matching|Riemannian Flow Matching]] with geodesic reached test NLL -7.93±1.67, versus -6.61±0.96 for the Riemannian Diffusion Model.
- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-028]] — On the 7D RNA torus dataset, [[Riemannian flow matching|Riemannian Flow Matching]] reached test NLL -5.20±0.067, versus -3.70±0.592 for the Riemannian Diffusion Model.
- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-029]] — On the Proline dataset, Riemannian Flow Matching scored 0.15±0.027 test NLL, behind the Riemannian Diffusion Model at 0.12±0.011.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 3 sources · topic: Probability, filtering and generative models on Lie groups (drafter's packet `q2-lie-probability`, confirmed at the gate)
