---
aliases: []
type: concept
element_type: method
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-18
---

## Working definition

An optimization method that preconditions the loss gradient by the inverse of a Riemannian metric on parameter space, usually the Fisher information, so that each step follows steepest descent in the space of model distributions rather than in raw parameter coordinates.

## Evidence

- [[Martens2014new - New Insights and Perspectives on the Natural Gradient Method#^martens2014new-004]] — The paper argues that natural gradient descent should be viewed as a 2nd-order method that uses the Fisher as an alternative to the Hessian
- [[Martens2014new - New Insights and Perspectives on the Natural Gradient Method#^martens2014new-037]] — Natural gradient methods taking finite steps are only approximately invariant to smooth invertible reparameterizations, depending on reparameterization curvature and step-size
- [[Martens2014new - New Insights and Perspectives on the Natural Gradient Method#^martens2014new-042]] — Amari showed that stochastic natural gradient descent with step-sizes shrinking as 1/k is asymptotically Fisher efficient, matching the Cramér-Rao bound
- [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored#^martens2015optimizing-004]] — The paper develops Kronecker-factored Approximate Curvature (K-FAC), an optimization method that approximates natural gradient descent in neural networks efficiently.
- [[Nielsen2018elementary - An elementary introduction to information geometry#^nielsen2018elementary-048]] — Natural gradient descent is recovered from Riemannian gradient descent using a first-order Taylor retraction of the exponential map
- [[Nielsen2018elementary - An elementary introduction to information geometry#^nielsen2018elementary-049]] — The natural gradient is invariant under an invertible smooth change of parameterization, according to the survey
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-005]] — Natural gradient descent, developed by Amari, selects the steepest descent direction along the Riemannian manifold on which the parameter is assumed to lie.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-037]] — Through the equivalence, natural gradient descent can be implemented as a first-order method, which has potential computational benefits.
- [[Arbel2019kernelized - Kernelized Wasserstein Natural Gradient#^arbel2019kernelized-001]] — Applying natural gradient methods is challenging in practice because each parameter update requires inverting the metric tensor of the model.
- [[Li2018natural - Natural gradient via optimal transport#^li2018natural-021]] — The proposed definition replaces the Kullback-Leibler divergence constraint of the standard Fisher-Rao natural gradient with the Wasserstein distance.
- [[Karakida2019pathological - Pathological spectra of the Fisher information metric and#^karakida2019pathological-026]] — The authors note that eigenvalues close to zero can make the inversion of the FIM in natural gradient methods unstable.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-004]] — Exact natural gradient computation is intractable because it requires inverting the Fisher information matrix, according to the authors.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 8 sources · topic: Information geometry and natural-gradient optimization (drafter's packet `p1-information-geometry`, confirmed at the gate)
