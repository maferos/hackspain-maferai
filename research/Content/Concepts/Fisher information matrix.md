---
aliases: ["FIM", "Fisher information metric", "Fisher-Rao metric"]
type: concept
element_type: concept
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-18
---

## Working definition

The expected outer product of log-likelihood gradients under a model's own distribution, which serves as the invariant Riemannian metric on a parametric family and as the curvature matrix that natural-gradient methods invert.

## Evidence

- [[Nielsen2018elementary - An elementary introduction to information geometry#^nielsen2018elementary-026]] — The Fisher information matrix is invariant by reparameterization of the sample space, according to the survey citing a textbook
- [[Nielsen2018elementary - An elementary introduction to information geometry#^nielsen2018elementary-030]] — The Fisher information matrix of an exponential family equals the covariance of its sufficient statistic and the Hessian of the cumulant function
- [[Nielsen2018elementary - An elementary introduction to information geometry#^nielsen2018elementary-033]] — The Fisher information metric is the unique invariant metric tensor under Markov embeddings, up to a scaling constant
- [[Li2018natural - Natural gradient via optimal transport#^li2018natural-002]] — Chentsov's classic result characterizes the Fisher-Rao metric as the only one, up to scaling, invariant under natural embeddings by Markov morphisms.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-006]] — Manifolds induced by the Fisher information matrices of parametric families are a well-known statistical example of Riemannian manifolds.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-007]] — In Table 1, the Fisher information metric of the Poisson(λ) family on the half-line is the reciprocal of λ.
- [[Martens2014new - New Insights and Perspectives on the Natural Gradient Method#^martens2014new-005]] — When the loss is a negative log-likelihood, the Fisher equals the expected loss Hessian under the model's distribution rather than the training distribution
- [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored#^martens2015optimizing-011]] — In an example network, the Kronecker-factored approximation successfully captures the coarse structure of the exact Fisher information matrix.
- [[Karakida2019pathological - Pathological spectra of the Fisher information metric and#^karakida2019pathological-011]] — The FIM for cross-entropy loss equals the regression FIM with a softmax-derived coefficient matrix Q inserted between the Jacobian and its transpose.
- [[Karakida2019pathological - Pathological spectra of the Fisher information metric and#^karakida2019pathological-026]] — The authors note that eigenvalues close to zero can make the inversion of the FIM in natural gradient methods unstable.
- [[Schulman2015trust - Trust Region Policy Optimization#^schulman2015trust-032]] — TRPO estimates the Fisher information matrix analytically from the Hessian of the KL divergence rather than from the covariance of gradients.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-004]] — Exact natural gradient computation is intractable because it requires inverting the Fisher information matrix, according to the authors.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (8 sources) · topic: Information geometry and natural-gradient optimization (drafter's packet `p1-information-geometry`, confirmed at the gate)
