---
aliases: ["pull-back metric"]
type: concept
element_type: concept
topic: "[[Neural manifolds in deep networks and motor neuroscience]]"
topics: ["[[Neural manifolds in deep networks and motor neuroscience]]"]
created: 2026-09-19
---

## Working definition

The Riemannian metric induced on a latent or configuration space by a smooth map into another metric space, computed as the Jacobian transpose times the target metric times the Jacobian so that local lengths match those measured in the target space.

## Evidence

- [[Arvanitidis2021pulling - Pulling back information geometry#^arvanitidis2021pulling-010]] — For an immersion parametrizing the likelihood, the latent pullback metric is the Jacobian transpose times the Fisher-Rao matrix times the Jacobian.
- [[Arvanitidis2021pulling - Pulling back information geometry#^arvanitidis2021pulling-011]] — The pullback metric is identical to the Fisher-Rao metric obtained when the latent variable is treated as the model parameters.
- [[Arvanitidis2021pulling - Pulling back information geometry#^arvanitidis2021pulling-028]] — The Fisher-Rao pullback was on par with the existing Euclidean pullback in learning geometric structure on the MNIST ones.
- [[BeikMohammadi2022reactive - Reactive Motion Generation on Learned Riemannian Manifolds#^beikmohammadi2022reactive-015]] — The joint-space pullback metric composes the forward kinematics Jacobian with the Jacobians of the decoder mean and variance networks.
- [[Ratliff2018riemannian - Riemannian Motion Policies#^ratliff2018riemannian-018]] — The RMP pullback transforms a task space policy into configuration space with the pullback metric J transpose A J.
- [[Ratliff2018riemannian - Riemannian Motion Policies#^ratliff2018riemannian-045]] — The baseline replaces each pullback metric with an equivalently scaled identity metric, representing the best-scaled pseudoinverse solution.
- [[Hauberg2018only - Only Bayes should learn a manifold (on the estimation of#^hauberg2018only-007]] — The pull-back metric is defined as the Jacobian Gram matrix of the mapping scaled by 1/D, giving a local latent inner product.
- [[Hauberg2018only - Only Bayes should learn a manifold (on the estimation of#^hauberg2018only-008]] — The pull-back metric is invariant to reparametrizations of the manifold because it corresponds to the data-space inner product measured locally on the manifold.
- [[Hauberg2018only - Only Bayes should learn a manifold (on the estimation of#^hauberg2018only-017]] — For geodesics to stay on the manifold, the author argues that the pull-back metric must take large values away from the data.
- [[Hauberg2018only - Only Bayes should learn a manifold (on the estimation of#^hauberg2018only-023]] — Under the Gaussian process model, the stochastic pull-back metric follows a non-central Wishart distribution at each latent point.
- [[Li2018natural - Natural gradient via optimal transport#^li2018natural-014]] — The metric on the parameter space is defined as the pull-back of the Wasserstein metric, making the parametrization an isometric embedding.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: top-down (5 sources) · topic: Neural manifolds in deep networks and motor neuroscience (drafter's packet `q8-neural-manifolds`, confirmed at the gate)
