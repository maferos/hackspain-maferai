---
aliases: []
type: "source"
title: "The Information Geometry of Mirror Descent"
citekey: "Raskutti2013information"
doi: "10.48550/arXiv.1310.7780"
arxiv: "1310.7780"
year: 2013
publication_type: "preprint"
url: "https://arxiv.org/abs/1310.7780"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Garvesh Raskutti", "Sayan Mukherjee"]
sha256: ["51d26f92ec6d35f3d8804a1b7a54f97071d1d7b97ec9738c74a515d5a19ff18e"]
pdf: "Content/Papers/Raskutti2013information.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 57
---

📄 PDF: [[Raskutti2013information.pdf]]

> [!abstract] One-sentence summary
> The paper proves that mirror descent with a Bregman divergence equals natural gradient descent on the dual Riemannian manifold, giving mirror descent a steepest-descent interpretation and asymptotic Fisher efficiency and letting natural gradient run as a first-order method.

## Abstract

Information geometry applies concepts in differential geometry to probability and statistics and is especially useful for parameter estimation in exponential families where parameters are known to lie on a Riemannian manifold. Connections between the geometric properties of the induced manifold and statistical properties of the estimation problem are well-established. However developing first-order methods that scale to larger problems has been less of a focus in the information geometry community. The best known algorithm that incorporates manifold structure is the second-order natural gradient descent algorithm introduced by Amari. On the other hand, stochastic approximation methods have led to the development of first-order methods for optimizing noisy objective functions. A recent generalization of the Robbins-Monro algorithm known as mirror descent, developed by Nemirovski and Yudin is a first order method that induces non-Euclidean geometries. However current analysis of mirror descent does not precisely characterize the induced non-Euclidean geometry nor does it consider performance in terms of statistical relative efficiency. In this paper, we prove that mirror descent induced by Bregman divergences is equivalent to the natural gradient descent algorithm on the dual Riemannian manifold. Using this equivalence, it follows that (1) mirror descent is the steepest descent direction along the Riemannian manifold of the exponential family; (2) mirror descent with log-likelihood loss applied to parameter estimation in exponential families asymptotically achieves the classical Cramér-Rao lower bound and (3) natural gradient descent for manifolds corresponding to exponential families can be implemented as a first-order method through mirror descent. (arXiv)

## 🧠 Key ideas (atomic)

- Both [[Mirror descent|mirror descent]] and natural gradient descent generalize online gradient descent to parameters that lie on a non-Euclidean manifold. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 1 ^raskutti2013information-001
- In online learning, an algorithm predicts a sequence of parameters that incur a loss at each iterate, with the goal of minimizing regret. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 1 ^raskutti2013information-002
- The authors state that gradient descent is the direction of steepest descent if the parameters lie in a Euclidean space. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 1 ^raskutti2013information-003
- When parameters lie on non-Euclidean manifolds, such as mean parameters of Poisson or Bernoulli families, ambient-space gradient descent is not the steepest descent direction. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 1 ^raskutti2013information-004
- [[Natural gradient descent]], developed by Amari, selects the steepest descent direction along the Riemannian manifold on which the parameter is assumed to lie. (Raskutti & Mukherjee, 2013) `ev:cited` p. 1 ^raskutti2013information-005
- Manifolds induced by the [[Fisher information matrix|Fisher information matrices]] of parametric families are a well-known statistical example of Riemannian manifolds. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 2 ^raskutti2013information-006
- In Table 1, the [[Fisher information matrix|Fisher information metric]] of the Poisson(λ) family on the half-line is the reciprocal of λ. (Raskutti & Mukherjee, 2013) `ev:reported` p. 2 ^raskutti2013information-007
- When the Fisher information equals the identity matrix, as for the Gaussian family in Table 1, the Riemannian manifold corresponds to standard Euclidean space. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 2 ^raskutti2013information-008
- The natural gradient descent step subtracts the step-size times the inverse Riemannian metric multiplied by the gradient of the loss. (Raskutti & Mukherjee, 2013) `ev:reported` p. 2 ^raskutti2013information-009
- If the manifold is Euclidean space with identity metric, the natural gradient step corresponds to the standard gradient descent step. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 2 ^raskutti2013information-010
- Theorem 1 of Amari proves that the natural gradient algorithm steps in the direction of steepest descent along the Riemannian manifold. (Raskutti & Mukherjee, 2013) `ev:cited` p. 2 ^raskutti2013information-011
- [[Mirror descent]], developed by Nemirovski and Yudin, rewrites the gradient step as an iterative penalized optimization with a proximity function other than squared ℓ2 error. (Raskutti & Mukherjee, 2013) `ev:cited` p. 2 ^raskutti2013information-012
- Setting the proximity function to half the squared ℓ2 distance recovers the standard gradient descent update, hence [[Mirror descent|mirror descent]] generalizes online gradient descent. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 2 ^raskutti2013information-013
- [[Bregman divergence|The Bregman divergence]] is a standard choice of proximity function since it corresponds to the Kullback-Leibler divergence for different exponential families. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 2 ^raskutti2013information-014
- [[Bregman divergence|The Bregman divergence]] induced by a strictly convex twice-differentiable function G equals G(θ) minus G(θ′) minus the inner product of ∇G(θ′) with θ−θ′. (Raskutti & Mukherjee, 2013) `ev:cited` p. 2 ^raskutti2013information-015
- Table 2 gives exp(θ) as the convex function G generating the Bregman divergence associated with the Poisson family. (Raskutti & Mukherjee, 2013) `ev:reported` p. 3 ^raskutti2013information-016
- Table 2 gives log(1 + exp(θ)) as the convex function G generating the Bregman divergence associated with the Bernoulli family. (Raskutti & Mukherjee, 2013) `ev:reported` p. 3 ^raskutti2013information-017
- The authors note that [[Bregman divergence|Bregman divergences]] are widely used in statistical inference, optimization, machine learning, and information geometry. (Raskutti & Mukherjee, 2013) `ev:cited` p. 3 ^raskutti2013information-018
- There is a one-to-one correspondence between [[Bregman divergence|Bregman divergences]] and exponential families, which the authors exploit for estimation in exponential families. (Raskutti & Mukherjee, 2013) `ev:cited` p. 3 ^raskutti2013information-019
- The paper proves that [[Mirror descent|mirror descent]] with a [[Bregman divergence]] step is equivalent to the natural gradient step along the dual Riemannian manifold. (Raskutti & Mukherjee, 2013) `ev:computed` p. 3 ^raskutti2013information-020
- The proof of equivalence combines convex analysis with connections between Bregman divergences and Riemannian manifolds developed in earlier work by Amari and Cichocki. (Raskutti & Mukherjee, 2013) `ev:reported` p. 3 ^raskutti2013information-021
- The authors state that steepest descent along a manifold and Fisher efficiency were known for natural gradient descent but not for mirror descent. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 3 ^raskutti2013information-022
- If G is strictly convex and twice differentiable, its convex conjugate H is also strictly convex and twice differentiable. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 3 ^raskutti2013information-023
- The gradient maps g of G and h of its convex conjugate H are inverses of each other. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 4 ^raskutti2013information-024
- The [[Bregman divergence|dual Bregman divergence]] induced by H satisfies BH(µ, µ′) = BG(h(µ′), h(µ)), which the authors call straightforward to show. (Raskutti & Mukherjee, 2013) `ev:computed` p. 4 ^raskutti2013information-025
- Following Amari and Cichocki, every [[Bregman divergence]] and its dual induce a pair of primal and dual Riemannian manifolds with Hessian metrics. (Raskutti & Mukherjee, 2013) `ev:cited` p. 4 ^raskutti2013information-026
- Since G is strictly convex and twice differentiable, its Hessian is positive definite for all θ, hence it defines a Riemannian metric. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 4 ^raskutti2013information-027
- For the Gaussian family the primal and dual manifolds coincide, with both parameter spaces equal to Rp and identity Hessians. (Raskutti & Mukherjee, 2013) `ev:computed` p. 4 ^raskutti2013information-028
- For the Bernoulli family, the dual manifold is [0, 1] with metric the reciprocal of p(1−p), consistent with Table 1. (Raskutti & Mukherjee, 2013) `ev:computed` p. 4 ^raskutti2013information-029
- Minimizing the mirror descent objective by differentiation yields an update in which g(θ) decreases by the step-size times the loss gradient. (Raskutti & Mukherjee, 2013) `ev:computed` p. 5 ^raskutti2013information-030
- Applying the chain rule in the dual coordinate µ turns the mirror descent update into a step preconditioned by the inverse Hessian of H. (Raskutti & Mukherjee, 2013) `ev:computed` p. 5 ^raskutti2013information-031
- By Theorem 1 of Amari, [[Mirror descent|mirror descent]] with [[Bregman divergence]] induced by G follows the steepest descent direction along the dual manifold of H. (Raskutti & Mukherjee, 2013) `ev:computed` p. 5 ^raskutti2013information-032
- As far as the authors are aware, no interpretation of mirror descent in terms of Riemannian manifolds had been provided before. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 5 ^raskutti2013information-033
- Natural gradient descent is a second-order method since it requires computing the metric tensor, the Hessian of H. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 5 ^raskutti2013information-034
- [[Mirror descent]] is a first-order method since each step simply requires the derivatives of the loss f and of G. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 5 ^raskutti2013information-035
- The authors state that first-order methods are preferred for many large-scale statistical inference problems, since derivatives are significantly less intensive to compute than Hessians. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 5 ^raskutti2013information-036
- Through the equivalence, [[Natural gradient descent|natural gradient descent]] can be implemented as a first-order method, which has potential computational benefits. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 5 ^raskutti2013information-037
- The authors note that prior work on the statistical theory of mirror descent has largely focused on regret analysis rather than statistical efficiency. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 5 ^raskutti2013information-038
- The statistical problem considered is parameter estimation in natural parameter exponential families with density h(y) exp(⟨θ, y⟩ − G(θ)). (Raskutti & Mukherjee, 2013) `ev:reported` p. 6 ^raskutti2013information-039
- The exponential family density can be re-expressed through the Bregman divergence between the natural parameter θ and h(y). (Raskutti & Mukherjee, 2013) `ev:computed` p. 6 ^raskutti2013information-040
- Under the standard log loss, the mirror descent objective for the natural parameter uses the Bregman divergence between θ and h(yt). (Raskutti & Mukherjee, 2013) `ev:computed` p. 6 ^raskutti2013information-041
- For the mean parameter µ, the natural gradient step minimizes the log loss written as the dual Bregman divergence between yt and µ. (Raskutti & Mukherjee, 2013) `ev:computed` p. 6 ^raskutti2013information-042
- The authors state that a parallel argument holds when mirror descent uses the mean parameter and natural gradient uses the natural parameter. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 6 ^raskutti2013information-043
- The Cramér-Rao theorem bounds the covariance of any unbiased estimator of µ from T independent samples below by the Hessian of H over T. (Raskutti & Mukherjee, 2013) `ev:cited` p. 6 ^raskutti2013information-044
- A sequence of estimators is asymptotically Fisher efficient if T times its covariance converges to the Hessian of H as T grows. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 6 ^raskutti2013information-045
- Using Theorem 2 of Amari together with the equivalence, the authors conclude that [[Mirror descent|mirror descent]] is Fisher efficient for the mean parameter. (Raskutti & Mukherjee, 2013) `ev:computed` p. 6 ^raskutti2013information-046
- Corollary 1 states that [[Mirror descent|mirror descent]] applied to the log loss with step-sizes 1/t asymptotically achieves the Cramér-Rao lower bound. (Raskutti & Mukherjee, 2013) `ev:computed` p. 7 ^raskutti2013information-047
- The authors note that any non-infinitesimal step in the direction of the manifold gradient moves off the manifold, for any curved manifold. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 7 ^raskutti2013information-048
- This observation motivated algorithms by Bonnabel in which the update step is constrained to remain on the manifold. (Raskutti & Mukherjee, 2013) `ev:cited` p. 7 ^raskutti2013information-049
- The online steepest descent step of Bonnabel applies the exponential map at the current point to the negative scaled Riemannian gradient. (Raskutti & Mukherjee, 2013) `ev:cited` p. 7 ^raskutti2013information-050
- The exponential map is extremely difficult to evaluate in general since it is the solution of a system of second-order differential equations. (Raskutti & Mukherjee, 2013) `ev:cited` p. 7 ^raskutti2013information-051
- A standard strategy replaces the exponential map with a computable retraction, which yields an approximate Riemannian gradient descent step. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 7 ^raskutti2013information-052
- The retraction µ + v, the first-order Taylor approximation of the exponential map, yields the natural gradient descent step of Amari. (Raskutti & Mukherjee, 2013) `ev:cited` p. 7 ^raskutti2013information-053
- The authors conclude that [[Mirror descent|mirror descent]] can be viewed as an easily computable first-order approximation to steepest descent on Bregman-induced Riemannian manifolds. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 7 ^raskutti2013information-054
- The authors state that implementing the natural gradient step as a first-order method through mirror descent has computational gains for larger datasets. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 8 ^raskutti2013information-055
- An open direction is whether adaptive step-size choices from Amari that exploit Riemannian structure can improve the performance of mirror descent. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 8 ^raskutti2013information-056
- The authors propose characterizing the geometry of mirror descent for other proximity functions, such as ℓp-norms, as a useful future direction. (Raskutti & Mukherjee, 2013) `ev:asserted` p. 8 ^raskutti2013information-057

## 🎯 Contributions


## 📖 Glossary

- **Mirror descent** — first-order method replacing squared ℓ2 proximity in gradient steps with another proximity function.
- **Natural gradient descent** — gradient step preconditioned by the inverse Riemannian metric, following steepest descent on the manifold.
- **Bregman divergence** — G(θ) − G(θ′) − ⟨∇G(θ′), θ − θ′⟩ for strictly convex G.
- **Convex conjugate** — H(µ) = sup over θ of ⟨θ, µ⟩ − G(θ).
- **Dual Riemannian manifold** — mean-parameter space Φ = ∇G(Θ) with Hessian metric ∇²H of the conjugate.
- **Fisher efficiency** — estimator covariance asymptotically attaining the Cramér-Rao lower bound.
- **Exponential map** — sends a tangent vector to the endpoint of the unit-time geodesic along it.
- **Retraction** — computable approximation of the exponential map, e.g. µ + v.

## ❓ Open questions

- Can Amari's adaptive, Riemannian-aware step-size choices improve the performance of mirror descent?
- What geometry does mirror descent induce for proximity functions that are not Bregman divergences, such as ℓp-norms?
- How does mirror descent relate to other online algorithms such as projected gradient descent?
- Does the first-order implementation of natural gradient deliver practical speed-ups on real large-scale problems (no experiments are reported)?
- What are the finite-sample (non-asymptotic) efficiency properties of mirror descent in exponential families?

## 📝 Notes on reading

Version read: arXiv 1310.7780v2 (29 Apr 2014). The registry abstract above differs from the abstract printed in this PDF version (the PDF abstract frames the result as an equivalence of two online learning algorithms). The paper is purely theoretical: it contains no experiments or numerical evaluations, so all results rest on derivation and on theorems cited from Amari (1998).

Tables 1–3 (Fisher information, Bregman divergences and their duals for Gaussian, Poisson and Bernoulli families) are garbled in the extraction: fractions are split across lines; only simple entries were claimed. Table 3's Bernoulli H(µ) entry appears as "η log µ + (1 −µ) log(1 −µ)", where η is likely a typo for µ. Equation (5) has a stray closing bracket, and page 6 writes p(y | η) where µ is meant. The proof of Theorem 1 is a short chain-rule argument; its equations were paraphrased rather than transcribed.

## Suggested new concepts

- Mirror descent — central first-order online optimization method, linked here to information geometry.
- Natural gradient descent — Amari's Riemannian steepest-descent method, recurring across optimization and learning papers.
- Bregman divergence — proximity function tying convex duality, exponential families and Riemannian metrics.
- Dually flat (Hessian) Riemannian manifolds — primal/dual manifold pair induced by a convex function and its conjugate.
- Fisher efficiency and the Cramér-Rao bound — optimality criterion for estimators used to evaluate online algorithms.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Equivalencia descenso espejo ↔ gradiente natural (B.6).
