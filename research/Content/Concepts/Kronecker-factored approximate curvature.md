---
aliases: ["K-FAC", "KFAC"]
type: concept
element_type: method
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-18
---

## Working definition

An approximate natural-gradient optimizer for neural networks that models each layer's Fisher block as the Kronecker product of activation and back-propagated-derivative second-moment matrices, so the curvature can be inverted cheaply.

## Evidence

- [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored#^martens2015optimizing-004]] — The paper develops Kronecker-factored Approximate Curvature (K-FAC), an optimization method that approximates natural gradient descent in neural networks efficiently.
- [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored#^martens2015optimizing-005]] — K-FAC's Fisher approximation is neither diagonal nor low-rank, nor block-diagonal with small blocks, yet it can be inverted very efficiently.
- [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored#^martens2015optimizing-044]] — Without damping or momentum, K-FAC's optimization path through predictive distributions is invariant to a broad class of fixed invertible network transformations.
- [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored#^martens2015optimizing-046]] — K-FAC is invariant to arbitrary affine transformations of the network input, which include many popular training data preprocessing techniques.
- [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored#^martens2015optimizing-047]] — Undamped block-diagonal K-FAC updates equal gradient descent on a transformed network whose unit activities and unit-gradients are centered and whitened.
- [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored#^martens2015optimizing-058]] — With momentum, K-FAC's per-iteration rate of progress was orders of magnitude higher than the baseline's on each of the three problems.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-007]] — K-FAC is described as a scalable approximation to natural gradient whose per-update cost is comparable to an SGD update.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-014]] — K-FAC approximates each layer's Fisher block as the Kronecker product of activation second moments and backpropagated-derivative second moments.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-016]] — The K-FAC approximate natural gradient update only requires computations on matrices comparable in size to the layer weight matrix.
- [[Arbel2019kernelized - Kernelized Wasserstein Natural Gradient#^arbel2019kernelized-060]] — KFAC also seems to suffer a drop in performance in the ill-conditioned case, which might result from its isotropic damping term.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (3 sources) · topic: Information geometry and natural-gradient optimization (drafter's packet `p1-information-geometry`, confirmed at the gate)
