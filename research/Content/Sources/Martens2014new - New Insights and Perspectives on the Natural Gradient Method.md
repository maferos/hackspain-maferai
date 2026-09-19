---
aliases: []
type: "source"
title: "New Insights and Perspectives on the Natural Gradient Method"
citekey: "Martens2014new"
doi: "10.48550/arXiv.1412.1193"
arxiv: "1412.1193"
year: 2014
publication_type: "preprint"
url: "https://arxiv.org/abs/1412.1193"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["James Martens"]
sha256: ["751f91031561cb5de4cd6255b11732feced7036a6b54534793c2fdccebde9fac"]
pdf: "Content/Papers/Martens2014new.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Martens2014new.pdf]]

> [!abstract] One-sentence summary
> Recasts natural gradient descent as a 2nd-order method whose Fisher often equals the Generalized Gauss-Newton matrix, which motivates damping, criticizes the empirical Fisher, qualifies parameterization invariance, and gives precise convergence bounds for stochastic 2nd-order methods on convex quadratics.

## Abstract

Natural gradient descent is an optimization method traditionally motivated from the perspective of information geometry, and works well for many applications as an alternative to stochastic gradient descent. In this paper we critically analyze this method and its properties, and show how it can be viewed as a type of 2nd-order optimization method, with the Fisher information matrix acting as a substitute for the Hessian. In many important cases, the Fisher information matrix is shown to be equivalent to the Generalized Gauss-Newton matrix, which both approximates the Hessian, but also has certain properties that favor its use over the Hessian. This perspective turns out to have significant implications for the design of a practical and robust natural gradient optimizer, as it motivates the use of techniques like trust regions and Tikhonov regularization. Additionally, we make a series of contributions to the understanding of natural gradient and 2nd-order methods, including: a thorough analysis of the convergence speed of stochastic natural gradient descent (and more general stochastic 2nd-order methods) as applied to convex quadratics, a critical examination of the oft-used "empirical" approximation of the Fisher matrix, and an analysis of the (approximate) parameterization invariance property possessed by natural gradient methods (which we show also holds for certain other curvature, but notably not the Hessian). (arXiv)

## 🧠 Key ideas (atomic)

- Natural gradient descent has been successfully applied to problems such as blind source separation, reinforcement learning, and neural network training (Martens, 2014) `ev:cited` p. 3 ^martens2014new-001
- For models with very many parameters such as large neural networks, computing the exact natural gradient is impractical because the Fisher matrix is extremely large (Martens, 2014) `ev:asserted` p. 3 ^martens2014new-002
- The classical parameterization invariance interpretation breaks down unless the step-size becomes arbitrarily small, since practical natural gradient updates operate in the default parameter space (Martens, 2014) `ev:asserted` p. 3 ^martens2014new-003
- The paper argues that [[Natural gradient descent|natural gradient descent]] should be viewed as a 2nd-order method that uses the Fisher as an alternative to the Hessian (Martens, 2014) `ev:asserted` p. 4 ^martens2014new-004
- When the loss is a negative log-likelihood, [[Fisher information matrix|the Fisher]] equals the expected loss Hessian under the model's distribution rather than the training distribution (Martens, 2014) `ev:computed` p. 10 ^martens2014new-005
- The Fisher equals the Generalized Gauss-Newton matrix when the output distribution is an exponential family whose natural parameters are given by the network output (Martens, 2014) `ev:computed` p. 20 ^martens2014new-006
- Distributions satisfying this equivalence include normal distributions parameterized by their mean and multinomial distributions with softmax probabilities, matching squared error and cross-entropy losses (Martens, 2014) `ev:computed` p. 20 ^martens2014new-007
- Prior work by Heskes showed the Fisher and the classical Gauss-Newton matrix are equivalent in the case of the squared error loss (Martens, 2014) `ev:cited` p. 19 ^martens2014new-008
- Concurrently, Pascanu and Bengio showed that the GGN and the Fisher are equivalent for several common losses such as cross-entropy and squared error (Martens, 2014) `ev:cited` p. 19 ^martens2014new-009
- Unlike the Fisher, the GGN definition is sensitive to where the dividing line between the loss function and the network is drawn (Martens, 2014) `ev:asserted` p. 14 ^martens2014new-010
- Unlike the Hessian, the GGN is positive semi-definite, so it never models the curvature of the objective as negative in any direction (Martens, 2014) `ev:asserted` p. 15 ^martens2014new-011
- Attempts combining the Hessian with trust-region or negative-curvature handling have yielded lackluster results for neural network optimization compared to GGN-based methods (Martens, 2014) `ev:cited` p. 16 ^martens2014new-012
- The author speculates that a GGN-based 2nd-order method will rely less on trust-regions because negative curvature is somewhat less trustworthy than positive curvature (Martens, 2014) `ev:asserted` p. 16 ^martens2014new-013
- Because each training case contributes a PSD term without cancellation, the GGN can be more robustly estimated from training subsets than the Hessian (Martens, 2014) `ev:asserted` p. 16 ^martens2014new-014
- The GGN fails to model the curvature coming from the network function, as opposed to the curvature coming from the loss function (Martens, 2014) `ev:asserted` p. 16 ^martens2014new-015
- Chen showed that, for squared error with a single output, the GGN uniquely yields a non-negative local quadratic approximation vanishing on an appropriate subspace (Martens, 2014) `ev:cited` p. 17 ^martens2014new-016
- Botev et al. observed that for piece-wise linear activations such as RELUs the GGN and the Hessian coincide on the diagonal blocks (Martens, 2014) `ev:cited` p. 17 ^martens2014new-017
- Recent wide-network results lend support to the idea that modeling curvature in the network function may be pointless for neural network optimization (Martens, 2014) `ev:cited` p. 18 ^martens2014new-018
- Fisher matrix-vector products can be computed via a linearized forward pass, then multiplication by the predictive distribution's Fisher, then standard backprop (Martens, 2014) `ev:asserted` p. 19 ^martens2014new-019
- A straight line in parameter space does not yield a straight line in distribution space, so large natural gradient steps may veer off target (Martens, 2014) `ev:asserted` p. 22 ^martens2014new-020
- When the Fisher equals the GGN, the negative natural gradient with unit scaling minimizes the GGN-based local quadratic model of the objective (Martens, 2014) `ev:computed` p. 22 ^martens2014new-021
- Reducing the step-size may be too crude a fix for poor natural gradient updates, because it affects all eigen-directions of the Fisher equally (Martens, 2014) `ev:asserted` p. 22 ^martens2014new-022
- The 2nd-order view motivates applying update damping techniques such as Tikhonov regularization and trust-region methods to natural gradient optimization (Martens, 2014) `ev:asserted` p. 23 ^martens2014new-023
- In Hessian-free optimization, Tikhonov-damped GGN updates applied with a step-size of 1 made much more progress than updates computed without damping (Martens, 2014) `ev:cited` p. 23 ^martens2014new-024
- The empirical Fisher takes the expectation of gradient outer-products over the training targets instead of over the model's predictive distribution (Martens, 2014) `ev:asserted` p. 23 ^martens2014new-025
- The empirical Fisher is often incorrectly called the Fisher or the Gauss-Newton matrix, though it is not equivalent to either in general (Martens, 2014) `ev:asserted` p. 23 ^martens2014new-026
- The empirical Fisher has rank at most |S|, whereas the rank of the Fisher is bounded by |S| times the rank of FR (Martens, 2014) `ev:computed` p. 23 ^martens2014new-027
- In a one-dimensional quadratic example, empirical-Fisher-preconditioned iterations fail to converge unless ξ < 1 and step-sizes go to zero sufficiently fast (Martens, 2014) `ev:computed` p. 24 ^martens2014new-028
- In the same example, the exact-Fisher iteration converges linearly with rate |1 −α| for any fixed step-size satisfying 0 < α < 2 (Martens, 2014) `ev:computed` p. 24 ^martens2014new-029
- Stochastic methods such as diagonal AdaGrad, RMSProp and Adam are all based on diagonal approximations of the empirical Fisher matrix (Martens, 2014) `ev:asserted` p. 25 ^martens2014new-030
- Estimating the empirical Fisher as an equally weighted average of all past gradients, as in AdaGrad, tends not to work well in practice (Martens, 2014) `ev:cited` p. 26 ^martens2014new-031
- An exponentially decayed running average works better, at least pre-asymptotically, as it can naturally forget very old contributions based on stale parameters (Martens, 2014) `ev:asserted` p. 26 ^martens2014new-032
- The author interprets the constant λ as a Tikhonov damping parameter, implying that no single fixed value suits the entire course of optimization (Martens, 2014) `ev:asserted` p. 26 ^martens2014new-033
- The exponent ξ = 3/4 first appeared in the diagonal CG preconditioner of Hessian-free optimization to make curvature estimates more conservative (Martens, 2014) `ev:cited` p. 27 ^martens2014new-034
- The online approximate Newton method of Hazan et al. achieves a better regret bound than the one shown for AdaGrad (Martens, 2014) `ev:cited` p. 27 ^martens2014new-035
- If curvature matrices satisfy the Jacobian transformation condition, preconditioned updates in two parameterizations agree approximately, with zero error for affine reparameterizations (Martens, 2014) `ev:computed` p. 29 ^martens2014new-036
- [[Natural gradient descent|Natural gradient methods]] taking finite steps are only approximately invariant to smooth invertible reparameterizations, depending on reparameterization curvature and step-size (Martens, 2014) `ev:computed` p. 30 ^martens2014new-037
- Curvature matrices of the form E[J⊤AJ], including the GGN, the Fisher and the empirical Fisher, satisfy the sufficient invariance condition (Martens, 2014) `ev:computed` p. 30 ^martens2014new-038
- The Hessian does not satisfy the sufficient condition for approximate parameterization invariance, except in certain special cases (Martens, 2014) `ev:computed` p. 30 ^martens2014new-039
- With the Fisher as curvature, the local quadratic model equals a sum of Fisher-weighted squared distances between optimal and linearly predicted output changes (Martens, 2014) `ev:computed` p. 31 ^martens2014new-040
- This interpretation lets the natural gradient be defined as the minimum-norm model minimizer even when the Fisher is not invertible (Martens, 2014) `ev:computed` p. 32 ^martens2014new-041
- Amari showed that stochastic [[Natural gradient descent|natural gradient descent]] with step-sizes shrinking as 1/k is asymptotically Fisher efficient, matching the Cramér-Rao bound (Martens, 2014) `ev:cited` p. 32 ^martens2014new-042
- Amari's Fisher efficiency proof assumes the Fisher is computed on the full training distribution rather than stochastically estimated from mini-batches (Martens, 2014) `ev:asserted` p. 33 ^martens2014new-043
- With minibatch Fisher estimates, which often work well in practice, a Fisher efficiency result like Amari's will likely no longer hold (Martens, 2014) `ev:asserted` p. 34 ^martens2014new-044
- Amari's proof also assumes realizability, meaning the optimal model distribution coincides with the training distribution (Martens, 2014) `ev:asserted` p. 34 ^martens2014new-045
- For a convex quadratic, the expected iterate of the stochastic 2nd-order iteration progresses independently of the gradient noise distribution (Martens, 2014) `ev:computed` p. 37 ^martens2014new-046
- For a quadratic objective, the expected excess objective decomposes into a term from the iterate variance and a term from the mean's error (Martens, 2014) `ev:computed` p. 38 ^martens2014new-047
- With a fixed step-size, the expected objective tends to the optimum plus an additive factor correlated with the step-size and gradient noise covariance (Martens, 2014) `ev:computed` p. 39 ^martens2014new-048
- The noise-dependent term for 2nd-order optimization with B = H∗ is no worse than twice that of the 1st-order case (Martens, 2014) `ev:computed` p. 41 ^martens2014new-049
- Stochastic 2nd-order methods with learning rates 1/(k+a+1) can, for certain problems, beat similarly decayed SGD's asymptotic objective by a large constant factor (Martens, 2014) `ev:computed` p. 5 ^martens2014new-050
- The convergence analysis assumes a gradient noise covariance constant with respect to θ, which the author calls somewhat unrealistic (Martens, 2014) `ev:asserted` p. 36 ^martens2014new-051
- With Polyak averaging, the asymptotic bound on the expected objective notably depends on neither the step-size nor the curvature matrix (Martens, 2014) `ev:computed` p. 42 ^martens2014new-052
- Larger step-sizes raise per-iterate variance but also decorrelate the iterates faster, and these effects exactly cancel in the limit (Martens, 2014) `ev:computed` p. 42 ^martens2014new-053
- An exponentially-decayed moving average of iterates typically works much better in practice than uniform averaging (Martens, 2014) `ev:asserted` p. 42 ^martens2014new-054
- Under realizability, simple stochastic gradient descent with averaging achieves a similar asymptotic convergence speed to Fisher efficient stochastic natural gradient descent (Martens, 2014) `ev:computed` p. 43 ^martens2014new-055
- The averaging bounds show that 2nd-order optimization improves the noise-independent term that depends on the starting point (Martens, 2014) `ev:computed` p. 43 ^martens2014new-056
- The noise-independent term may often matter more in practice, for example with a fixed iteration budget or with early-stopping (Martens, 2014) `ev:asserted` p. 44 ^martens2014new-057
- With averaging, the noise-independent term shrinks quadratically rather than exponentially as with a fixed step-size (Martens, 2014) `ev:computed` p. 44 ^martens2014new-058
- The averaging bound of Flammarion and Bach fails to establish convergence, since its 4α tr(Σg) term is constant in k (Martens, 2014) `ev:asserted` p. 45 ^martens2014new-059
- Local convergence bounds assuming quadratic objectives are always improved by the Hessian, so they fail to explain the observed GGN superiority (Martens, 2014) `ev:asserted` p. 45 ^martens2014new-060
- The author states that a completely rigorous account of the global convergence of GGN-based optimization remains elusive, even assuming convexity (Martens, 2014) `ev:asserted` p. 45 ^martens2014new-061

## 🎯 Contributions

## 📖 Glossary

- **Natural gradient** — The gradient multiplied by the inverse of the model's Fisher information matrix.
- **Fisher information matrix** — Expected outer product of log-likelihood gradients under the model's own distribution.
- **Empirical Fisher** — Fisher variant taking the expectation over training targets instead of model samples.
- **Generalized Gauss-Newton matrix (GGN)** — PSD Hessian approximation obtained by linearizing the network inside a convex loss.
- **Tikhonov damping** — Adding a multiple of the identity to the curvature matrix to limit update size.
- **Fisher efficiency** — Asymptotically attaining the Cramér-Rao lower bound on estimator variance.
- **Realizability** — The optimal model distribution coincides exactly with the training distribution.
- **Polyak averaging** — Averaging the optimizer's iterates to reduce the variance of the final estimate.
- **Parameterization invariance** — Optimizer path unchanged under smooth invertible reparameterization of the model.

## ❓ Open questions

- Can the observed advantages of the GGN over the Hessian be rigorously justified for neural networks, given proper damping in both cases?
- Are there situations where the Fisher and the GGN are distinct and one is clearly preferable?
- When does the pre-asymptotic advantage of stochastic 2nd-order methods over SGD with Polyak averaging matter in practice, and can it be characterized rigorously?
- To what degree does Fisher efficiency hold approximately when the Fisher is estimated from mini-batches with decayed averaging?
- Can the convergence analysis be extended to gradient noise covariance that varies with θ, covering linear least-squares?
- How does the regret analysis of AdaGrad-like methods relate to classical stochastic 2nd-order methods based on curvature?

## 📝 Notes on reading

The cached text is the JMLR 21 (2020) version, arXiv:1412.1193v11 (19 Sep 2020), while the citekey and metadata year point to the 2014 arXiv preprint; claims are cited with the metadata year 2014 but page locators refer to this 76-page version. Figure 1 (p. 22) sketches how a straight parameter-space step along the natural gradient curves away from its distribution-space target; it is only described here. Many equations (Theorems 3, 5, 6 and their bounds, pp. 37-45) were extracted with broken layout; their exact expressions were not claimed, only their qualitative conclusions. Appendices A-E (pp. 47-71) contain proofs and technical lemmas; no separate claims were drawn from them. The example of the noise term scaling as Omega(n^2/k) on p. 41 was not claimed because the exponent was garbled in extraction. The abstract's phrase 'certain other curvature' reads 'certain other curvature matrices' in the PDF.

## Suggested new concepts

- Generalized Gauss-Newton matrix — central curvature matrix linking natural gradient to 2nd-order optimization, reused across K-FAC and Hessian-free methods.
- Empirical Fisher — widely used but criticized approximation underlying Adam, RMSProp and AdaGrad preconditioners.
- Update damping (Tikhonov / trust region) — key practical ingredient that makes curvature-based optimizers robust.
- Fisher efficiency — asymptotic optimality notion often cited in favor of natural gradient, with important caveats.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Fisher = Gauss-Newton generalizada; amortiguamiento y trust regions (B.2).
