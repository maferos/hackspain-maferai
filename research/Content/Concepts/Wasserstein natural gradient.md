---
aliases: ["WNG"]
type: concept
element_type: method
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-18
---

## Working definition

A natural gradient in which the parameter-space metric is the pull-back of the Wasserstein-2 metric instead of the Fisher-Rao metric, so the update accounts for a ground metric on sample space and stays defined for models without a density.

## Evidence

- [[Arbel2019kernelized - Kernelized Wasserstein Natural Gradient#^arbel2019kernelized-010]] — Defining the Wasserstein information matrix through distributional derivatives allows the Wasserstein natural gradient to be defined when the model has no density.
- [[Arbel2019kernelized - Kernelized Wasserstein Natural Gradient#^arbel2019kernelized-012]] — Proposition 3 gives a dual formulation of the Wasserstein natural gradient for implicit models as a saddle-point problem over smooth test functions.
- [[Arbel2019kernelized - Kernelized Wasserstein Natural Gradient#^arbel2019kernelized-035]] — Accuracy was assessed on multivariate normal, multivariate log-normal and hyper-sphere uniform models, whose Wasserstein natural gradient has closed form.
- [[Arbel2019kernelized - Kernelized Wasserstein Natural Gradient#^arbel2019kernelized-043]] — On a multivariate normal family, exact WNG allowed larger step sizes than Euclidean gradient, giving faster convergence of the loss.
- [[Arbel2019kernelized - Kernelized Wasserstein Natural Gradient#^arbel2019kernelized-046]] — The dynamics of exact WNG seem to be well approximated by KWNG along the two main PCA directions of the trajectory.
- [[Li2018natural - Natural gradient via optimal transport#^li2018natural-001]] — The paper introduces a Wasserstein natural gradient flow on the parameter space of probability models with discrete sample spaces.
- [[Li2018natural - Natural gradient via optimal transport#^li2018natural-020]] — The Wasserstein natural gradient is derived as the steepest descent direction under a constraint on a second order approximation of the Wasserstein distance.
- [[Li2018natural - Natural gradient via optimal transport#^li2018natural-043]] — Example 3 applies the Wasserstein natural gradient to maximum likelihood estimation by minimizing the Kullback-Leibler divergence from the empirical data distribution.
- [[Li2018natural - Natural gradient via optimal transport#^li2018natural-059]] — With the simple adaptive method and a suitable initial step size, the Wasserstein gradient was faster than the Euclidean and Fisher gradients.
- [[Li2018natural - Natural gradient via optimal transport#^li2018natural-061]] — In the current implementation, the Wasserstein gradient involved heavier computational costs than the Euclidean and Fisher gradients.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 2 sources · topic: Information geometry and natural-gradient optimization (drafter's packet `p1-information-geometry`, confirmed at the gate)
