---
aliases: []
type: topic
parent: Optimization and learning on manifolds
created: 2026-09-18
---

## Scope

The geometry of parametric probability models and the optimizers built on it: the Fisher information metric and its variants (Fisher-Rao, Wasserstein), divergences such as the Bregman family and the dually flat structure they induce, steepest descent under a metric (natural gradient, mirror descent, Wasserstein natural gradient), practical approximations of the Fisher (K-FAC, damping, Fisher-vector products), KL-constrained policy updates seen as natural-gradient steps (natural policy gradient, TRPO), and spectral views of wide networks through the Fisher and the Neural Tangent Kernel. It deliberately leaves out the reinforcement-learning machinery that is not geometric (PPO clipping, advantage estimation, Atari and MuJoCo benchmarking), Lie groups and pose representations, equivariant vision networks, Riemannian motion policies for robot control, and robot-learning datasets and policies, which belong to other areas.

## Concepts

- [[Natural gradient descent]] — An optimization method that preconditions the loss gradient by the inverse of a Riemannian metric on parameter space, usually the Fisher information, so that each step follows steepest descent in the space of model distributions rather than in raw parameter coordinates.
- [[Natural policy gradient]] — A policy-gradient method for reinforcement learning that preconditions the policy gradient by the inverse Fisher information of the policy, taking natural-gradient steps with a chosen step size.
- [[Wasserstein natural gradient]] — A natural gradient in which the parameter-space metric is the pull-back of the Wasserstein-2 metric instead of the Fisher-Rao metric, so the update accounts for a ground metric on sample space and stays defined for models without a density.
- [[Trust region policy optimization]] — A policy-optimization algorithm that maximizes a surrogate advantage objective subject to a bound on the average KL divergence between old and new policies, solved with conjugate gradient on Fisher-vector products and a line search.
- [[Bregman divergence]] — The divergence induced by a strictly convex, differentiable function as the gap between the function and its first-order Taylor approximation, which corresponds one-to-one with exponential families and induces a dually flat Hessian geometry.
- [[Neural Tangent Kernel]] — The kernel formed by inner products of a network's output gradients with respect to its parameters, which governs gradient-descent training dynamics in function space and becomes deterministic and constant during training in the infinite-width limit.
- [[Fisher information matrix]] — The expected outer product of log-likelihood gradients under a model's own distribution, which serves as the invariant Riemannian metric on a parametric family and as the curvature matrix that natural-gradient methods invert.
- [[Mirror descent]] — A first-order optimization method that replaces the squared Euclidean proximity term of a gradient step with another proximity function, typically a Bregman divergence, and is equivalent to natural gradient descent on the dual manifold.
- [[Kronecker-factored approximate curvature]] — An approximate natural-gradient optimizer for neural networks that models each layer's Fisher block as the Kronecker product of activation and back-propagated-derivative second-moment matrices, so the curvature can be inverted cheaply.
- [[Kronecker-factored preconditioning]] — Preconditioning a layer's matrix-shaped gradient with the Kronecker product of two small per-dimension matrices, so that a full-matrix preconditioner is approximated with memory and compute that scale with each dimension rather than with their product.
- [[Newton-Schulz orthogonalization]] — An iterative odd-polynomial matrix routine that pushes every singular value of a matrix toward one, approximating its semi-orthogonal factor UV^T without an SVD, and so computes spectral-norm steepest-descent updates such as Muon's.
- [[Elastic weight consolidation]] — A continual-learning regularizer that adds a quadratic penalty anchoring each weight to its value after earlier tasks, with a stiffness set by the diagonal Fisher information, so weights important to old tasks change slowly while the rest stay free to learn.

## Subtopics

## Related topics

## ❓ Open questions

## Problems

- none yet: no problem names this topic as its topic

## History

- 2026-09-18 · Eki Gonzalez Flamarique · parent: root — new area for concepts promoted from the research batch, confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · added 3 concepts — concepts from the gap-research batch (04_huecos_y_ampliacion), confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · parent: root → Optimization and learning on manifolds — grouped under the request's three axes
