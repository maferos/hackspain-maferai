---
aliases: []
type: concept
element_type: method
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-19
---

## Working definition

Preconditioning a layer's matrix-shaped gradient with the Kronecker product of two small per-dimension matrices, so that a full-matrix preconditioner is approximated with memory and compute that scale with each dimension rather than with their product.

## Evidence

- [[Gupta2018shampoo - Shampoo Preconditioned Stochastic Tensor Optimization#^gupta2018shampoo-006]] — Shampoo retains the tensor structure of the gradient and maintains a separate preconditioner matrix for each of the gradient's dimensions.
- [[Gupta2018shampoo - Shampoo Preconditioned Stochastic Tensor Optimization#^gupta2018shampoo-016]] — In the matrix case, Shampoo instead maintains smaller left and right matrices containing second-moment information of the accumulated gradients.
- [[Gupta2018shampoo - Shampoo Preconditioned Stochastic Tensor Optimization#^gupta2018shampoo-018]] — Constructing the left and right preconditioners costs computation cubic in each dimension separately, substantially lower than full-matrix methods cubic in their product.
- [[Gupta2018shampoo - Shampoo Preconditioned Stochastic Tensor Optimization#^gupta2018shampoo-020]] — After flattening, the matrix Shampoo update is equivalent to a gradient step preconditioned by the Kronecker product of the two root matrices.
- [[Gupta2018shampoo - Shampoo Preconditioned Stochastic Tensor Optimization#^gupta2018shampoo-023]] — K-FAC approximates the Fisher matrix of each network layer by a Kronecker product of two smaller matrices, relying on independence assumptions.
- [[Vyas2024soap - SOAP Improving and Stabilizing Shampoo using Adam#^vyas2024soap-002]] — Morwani et al. (2024) showed that Shampoo with minor modifications, such as power 1/2, is close to the optimal Kronecker approximation of Adagrad.
- [[Vyas2024soap - SOAP Improving and Stabilizing Shampoo using Adam#^vyas2024soap-010]] — Algorithm 3, SOAP, can be interpreted as running Adam in the eigenspace of Shampoo's preconditioner.
- [[Bernstein2024old - Old Optimizer, New Norm An Anthology#^bernstein2024old-024]] — Practitioners usually replace the simple sums in the left and right Shampoo preconditioners with exponential moving averages.
- [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored#^martens2015optimizing-007]] — In the first stage, Fisher blocks corresponding to all weights of a layer are approximated as Kronecker products of much smaller matrices.
- [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored#^martens2015optimizing-009]] — The Kronecker factorization replaces the expectation of a Kronecker product with the Kronecker product of expectations, which the authors call a major approximation.
- [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored#^martens2015optimizing-013]] — The Kronecker approximation is equivalent to assuming statistical independence between products of unit activities and products of unit input derivatives.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-009]] — ACKTR uses a Kronecker-factored approximation to [[Natural policy gradient|natural policy gradient]] that allows the covariance matrix of the gradient to be inverted efficiently.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 5 sources · topic: Information geometry and natural-gradient optimization (drafter's packet `q4-geometric-finetuning`, confirmed at the gate)
