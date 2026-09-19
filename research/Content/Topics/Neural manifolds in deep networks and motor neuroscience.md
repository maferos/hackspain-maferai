---
aliases: []
type: topic
parent: Geometry of motion and representation
created: 2026-09-19
---

## Scope

The geometry of neural representations in artificial networks and in recorded brain activity: how the intrinsic dimension of hidden representations changes across layers and training, how population activity forms manifolds whose dimension, radius and separability can be measured, how latent population dynamics are inferred from spiking data, and the pullback metrics that give learned latent spaces a Riemannian geometry. It covers the estimators and theories used for these measurements (TwoNN, manifold capacity, sequential latent-variable models). It deliberately leaves out robot motion generation on Riemannian manifolds and Lie groups, natural-gradient optimisation and information geometry of parameter spaces, and brain-machine interface decoding as an engineering problem, except where they supply a construction such as the pullback metric.

## Concepts

- [[Intrinsic dimension of neural representations]] — The number of degrees of freedom needed to describe the manifold on which a layer's (or a neural population's) activity vectors lie, typically far smaller than the number of units or neurons.
- [[Pullback metric]] — The Riemannian metric induced on a latent or configuration space by a smooth map into another metric space, computed as the Jacobian transpose times the target metric times the Jacobian so that local lengths match those measured in the target space.
- [[Neural population dynamics]] — The time evolution of the joint activity of a population of neurons, viewed as trajectories of a possibly input-driven dynamical system in a low-dimensional neural state space.
- [[TwoNN estimator]] — An intrinsic-dimension estimator that fits the Pareto distribution followed by the ratio of each point's second to first nearest-neighbour distance, needing only those two distances per point.

## Subtopics

## Related topics

## ❓ Open questions

## Problems

- none yet: no problem names this topic as its topic

## History

- 2026-09-19 · Eki Gonzalez Flamarique · parent: root — new area for concepts promoted from the gap-research batch (04_huecos_y_ampliacion), confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · parent: root → Geometry of motion and representation — grouped under the request's three axes
