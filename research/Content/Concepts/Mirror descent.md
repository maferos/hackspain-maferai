---
aliases: []
type: concept
element_type: method
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-18
---

## Working definition

A first-order optimization method that replaces the squared Euclidean proximity term of a gradient step with another proximity function, typically a Bregman divergence, and is equivalent to natural gradient descent on the dual manifold.

## Evidence

- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-001]] — Both mirror descent and natural gradient descent generalize online gradient descent to parameters that lie on a non-Euclidean manifold.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-012]] — Mirror descent, developed by Nemirovski and Yudin, rewrites the gradient step as an iterative penalized optimization with a proximity function other than squared ℓ2 error.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-013]] — Setting the proximity function to half the squared ℓ2 distance recovers the standard gradient descent update, hence mirror descent generalizes online gradient descent.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-020]] — The paper proves that mirror descent with a Bregman divergence step is equivalent to the natural gradient step along the dual Riemannian manifold.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-032]] — By Theorem 1 of Amari, mirror descent with Bregman divergence induced by G follows the steepest descent direction along the dual manifold of H.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-035]] — Mirror descent is a first-order method since each step simply requires the derivatives of the loss f and of G.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-046]] — Using Theorem 2 of Amari together with the equivalence, the authors conclude that mirror descent is Fisher efficient for the mean parameter.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-047]] — Corollary 1 states that mirror descent applied to the log loss with step-sizes 1/t asymptotically achieves the Cramér-Rao lower bound.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-054]] — The authors conclude that mirror descent can be viewed as an easily computable first-order approximation to steepest descent on Bregman-induced Riemannian manifolds.
- [[Nielsen2018elementary - An elementary introduction to information geometry#^nielsen2018elementary-050]] — Bregman mirror descent on a Hessian manifold is equivalent to natural gradient descent on the dual Hessian manifold

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (2 sources) · topic: Information geometry and natural-gradient optimization (drafter's packet `p1-information-geometry`, confirmed at the gate)
