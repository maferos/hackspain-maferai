---
aliases: []
type: concept
element_type: concept
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-18
---

## Working definition

The divergence induced by a strictly convex, differentiable function as the gap between the function and its first-order Taylor approximation, which corresponds one-to-one with exponential families and induces a dually flat Hessian geometry.

## Evidence

- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-014]] — The Bregman divergence is a standard choice of proximity function since it corresponds to the Kullback-Leibler divergence for different exponential families.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-015]] — The Bregman divergence induced by a strictly convex twice-differentiable function G equals G(θ) minus G(θ′) minus the inner product of ∇G(θ′) with θ−θ′.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-018]] — The authors note that Bregman divergences are widely used in statistical inference, optimization, machine learning, and information geometry.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-019]] — There is a one-to-one correspondence between Bregman divergences and exponential families, which the authors exploit for estimation in exponential families.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-020]] — The paper proves that mirror descent with a Bregman divergence step is equivalent to the natural gradient step along the dual Riemannian manifold.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-025]] — The dual Bregman divergence induced by H satisfies BH(µ, µ′) = BG(h(µ′), h(µ)), which the authors call straightforward to show.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-026]] — Following Amari and Cichocki, every Bregman divergence and its dual induce a pair of primal and dual Riemannian manifolds with Hessian metrics.
- [[Raskutti2013information - The Information Geometry of Mirror Descent#^raskutti2013information-032]] — By Theorem 1 of Amari, mirror descent with Bregman divergence induced by G follows the steepest descent direction along the dual manifold of H.
- [[Nielsen2018elementary - An elementary introduction to information geometry#^nielsen2018elementary-044]] — According to the survey, the only symmetric Bregman divergences are squared Mahalanobis distances, which are defined by positive-definite matrices
- [[Nielsen2018elementary - An elementary introduction to information geometry#^nielsen2018elementary-054]] — The Chernoff information between two distributions of the same exponential family amounts to a Bregman divergence at the optimal exponent
- [[Nielsen2018elementary - An elementary introduction to information geometry#^nielsen2018elementary-056]] — The Kullback-Leibler divergence between two mixtures with prescribed components is equivalent to a Bregman divergence for the negative differential entropy
- [[Nielsen2018elementary - An elementary introduction to information geometry#^nielsen2018elementary-066]] — The survey proposes estimating extended f-divergences, whose integrand is a scalar Bregman divergence, so the Monte Carlo estimates remain non-negative

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 2 sources · topic: Information geometry and natural-gradient optimization (drafter's packet `p1-information-geometry`, confirmed at the gate)
