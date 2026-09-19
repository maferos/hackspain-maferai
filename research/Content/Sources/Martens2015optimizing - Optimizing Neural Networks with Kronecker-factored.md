---
aliases: []
type: "source"
title: "Optimizing Neural Networks with Kronecker-factored Approximate Curvature"
citekey: "Martens2015optimizing"
doi: "10.48550/arXiv.1503.05671"
arxiv: "1503.05671"
year: 2015
publication_type: "preprint"
url: "https://arxiv.org/abs/1503.05671"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["James Martens", "Roger Grosse"]
sha256: ["da06b21e402d147a2852a3ca7c63be8b0448d5083053b595d754e9bf6439e1fe"]
pdf: "Content/Papers/Martens2015optimizing.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[Martens2015optimizing.pdf]]

> [!abstract] One-sentence summary
> The paper introduces K-FAC, a Kronecker-factored, efficiently invertible approximation of the neural network Fisher that, with careful damping and momentum, optimizes deep autoencoders far faster per iteration than well-tuned momentum SGD.

## Abstract

We propose an efficient method for approximating natural gradient descent in neural networks which we call Kronecker-Factored Approximate Curvature (K-FAC). K-FAC is based on an efficiently invertible approximation of a neural network's Fisher information matrix which is neither diagonal nor low-rank, and in some cases is completely non-sparse. It is derived by approximating various large blocks of the Fisher (corresponding to entire layers) as being the Kronecker product of two much smaller matrices. While only several times more expensive to compute than the plain stochastic gradient, the updates produced by K-FAC make much more progress optimizing the objective, which results in an algorithm that can be much faster than stochastic gradient descent with momentum in practice. And unlike some previously proposed approximate natural-gradient/Newton methods which use high-quality non-diagonal curvature matrices (such as Hessian-free optimization), K-FAC works very well in highly stochastic optimization regimes. This is because the cost of storing and inverting K-FAC's approximation to the curvature matrix does not depend on the amount of data used to estimate it, which is a feature typically associated only with diagonal or low-rank approximations to the curvature matrix. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that Hessian-free updates are expensive to compute, as they involve running linear conjugate gradient for potentially hundreds of iterations. (Martens & Grosse, 2015) `ev:asserted` p. 2 ^martens2015optimizing-001
- Since its curvature estimate must remain fixed while CG iterates, Hessian-free optimization goes through much less data than SGD in comparable time. (Martens & Grosse, 2015) `ev:asserted` p. 2 ^martens2015optimizing-002
- Methods inverting diagonal, block-diagonal or low-rank curvature approximations provide only limited performance improvement in practice, especially compared to SGD with momentum. (Martens & Grosse, 2015) `ev:cited` p. 2 ^martens2015optimizing-003
- The paper develops [[Kronecker-factored approximate curvature|Kronecker-factored Approximate Curvature]] (K-FAC), an optimization method that approximates [[Natural gradient descent|natural gradient descent]] in neural networks efficiently. (Martens & Grosse, 2015) `ev:asserted` p. 3 ^martens2015optimizing-004
- [[Kronecker-factored approximate curvature|K-FAC]]'s Fisher approximation is neither diagonal nor low-rank, nor block-diagonal with small blocks, yet it can be inverted very efficiently. (Martens & Grosse, 2015) `ev:asserted` p. 3 ^martens2015optimizing-005
- The approximation can be estimated online from arbitrarily large subsets of the training data without increasing the cost of inversion. (Martens & Grosse, 2015) `ev:asserted` p. 3 ^martens2015optimizing-006
- In the first stage, Fisher blocks corresponding to all weights of a layer are approximated as [[Kronecker-factored preconditioning|Kronecker products of much smaller matrices]]. (Martens & Grosse, 2015) `ev:asserted` p. 3 ^martens2015optimizing-007
- In the second stage, the approximated Fisher is further assumed to have an inverse that is either block-diagonal or block-tridiagonal. (Martens & Grosse, 2015) `ev:asserted` p. 3 ^martens2015optimizing-008
- [[Kronecker-factored preconditioning|The Kronecker factorization]] replaces the expectation of a Kronecker product with the Kronecker product of expectations, which the authors call a major approximation. (Martens & Grosse, 2015) `ev:asserted` p. 8 ^martens2015optimizing-009
- The authors state this approximation likely won't become exact under any realistic set of assumptions or as a limiting asymptotic case. (Martens & Grosse, 2015) `ev:asserted` p. 8 ^martens2015optimizing-010
- In an example network, the Kronecker-factored approximation successfully captures the coarse structure of the [[Fisher information matrix|exact Fisher information matrix]]. (Martens & Grosse, 2015) `ev:measured` p. 8 ^martens2015optimizing-011
- The example network had architecture 256-20-20-20-20-20-10 with tanh units, trained to classify a 16x16 down-scaled version of MNIST. (Martens & Grosse, 2015) `ev:reported` p. 9 ^martens2015optimizing-012
- [[Kronecker-factored preconditioning|The Kronecker approximation]] is equivalent to assuming statistical independence between products of unit activities and products of unit input derivatives. (Martens & Grosse, 2015) `ev:computed` p. 9 ^martens2015optimizing-013
- An upper bound on the approximation error will be small if all cumulants of order 3 or higher are small. (Martens & Grosse, 2015) `ev:computed` p. 10 ^martens2015optimizing-014
- In the example network, total approximation error over the middle 4 layers was 2894.4, against a corresponding upper bound of 4134.6. (Martens & Grosse, 2015) `ev:measured` p. 10 ^martens2015optimizing-015
- A block-tridiagonal inverse is argued to be reasonable because gradient computation only uses information from the layer below and the layer above. (Martens & Grosse, 2015) `ev:asserted` p. 11 ^martens2015optimizing-016
- For the example network, the inverse of the Kronecker-factored Fisher exhibits an approximate block-tridiagonal structure, whereas the approximation itself does not. (Martens & Grosse, 2015) `ev:measured` p. 12 ^martens2015optimizing-017
- With the block-diagonal approximation, computing the inverse amounts to inverting 2ℓ smaller matrices using the Kronecker product inverse identity. (Martens & Grosse, 2015) `ev:computed` p. 13 ^martens2015optimizing-018
- Unlike TONGA's per-unit blocks, K-FAC's blocks contain all parameters of a layer and would be impractical to invert as general matrices. (Martens & Grosse, 2015) `ev:asserted` p. 13 ^martens2015optimizing-019
- The block-tridiagonal inverse is obtained by treating it as the precision matrix of a tree-structured Gaussian graphical model with an equivalent directed model. (Martens & Grosse, 2015) `ev:computed` p. 14 ^martens2015optimizing-020
- In the example network, the block-tridiagonal-inverse approximation also approximates the off-tridiagonal blocks of the Kronecker-factored Fisher very well. (Martens & Grosse, 2015) `ev:measured` p. 16 ^martens2015optimizing-021
- The block-diagonal inverse is a reasonably good approximation of the inverse Kronecker-factored Fisher, despite being a rather poor approximation of the matrix itself. (Martens & Grosse, 2015) `ev:measured` p. 16 ^martens2015optimizing-022
- The block-tridiagonal inverse approximation is a significantly better approximation of the inverse than the block-diagonal one, even on the diagonal blocks. (Martens & Grosse, 2015) `ev:measured` p. 16 ^martens2015optimizing-023
- Gradient-side statistics are estimated by sampling targets from the network's predictive distribution and rerunning the backwards phase of backpropagation. (Martens & Grosse, 2015) `ev:reported` p. 19 ^martens2015optimizing-024
- The authors found that just one modified backwards pass is sufficient to obtain a good quality estimate of these statistics in practice. (Martens & Grosse, 2015) `ev:measured` p. 19 ^martens2015optimizing-025
- Running estimates of the Kronecker factors use exponentially decaying averaging with weight ϵ = min{1 −1/k, 0.95} at iteration k. (Martens & Grosse, 2015) `ev:reported` p. 19 ^martens2015optimizing-026
- Hessian-free and related methods must base curvature estimates on data processed all at once, which limits their effectiveness in stochastic optimization. (Martens & Grosse, 2015) `ev:asserted` p. 20 ^martens2015optimizing-027
- The authors found no good choice of λ for which standard adaptive Tikhonov damping gave update quality comparable to exact-Fisher methods such as HF. (Martens & Grosse, 2015) `ev:measured` p. 22 ^martens2015optimizing-028
- One possible explanation offered is that K-FAC's quadratic model, unlike the exact Fisher model, has no guarantee of being accurate to second order. (Martens & Grosse, 2015) `ev:asserted` p. 22 ^martens2015optimizing-029
- K-FAC's damping computes a Tikhonov-damped update proposal and then re-scales it according to a quadratic model computed with the exact Fisher. (Martens & Grosse, 2015) `ev:asserted` p. 22 ^martens2015optimizing-030
- Factored Tikhonov damping adds scaled identity multiples to each Kronecker factor, so each damped diagonal block remains a single Kronecker product. (Martens & Grosse, 2015) `ev:asserted` p. 23 ^martens2015optimizing-031
- The authors found that the factored approximate Tikhonov approach often works better in practice than the exact Tikhonov version. (Martens & Grosse, 2015) `ev:measured` p. 24 ^martens2015optimizing-032
- The re-scaling step estimates only a single scalar quantity from matrix-vector products with the exact Fisher on the current mini-batch. (Martens & Grosse, 2015) `ev:reported` p. 25 ^martens2015optimizing-033
- With re-scaling, K-FAC can be viewed as HF using the approximate Fisher as preconditioner and running CG for only 1 step. (Martens & Grosse, 2015) `ev:asserted` p. 25 ^martens2015optimizing-034
- Without re-scaling, the raw update proposal gives no objective improvement unless the factored Tikhonov damping strength is made very large. (Martens & Grosse, 2015) `ev:measured` p. 25 ^martens2015optimizing-035
- The Levenberg-Marquardt rule for λ was applied every T1 = 5 iterations of K-FAC, from a starting value of λ = 150. (Martens & Grosse, 2015) `ev:reported` p. 26 ^martens2015optimizing-036
- A separate damping strength γ for the approximate Fisher is adjusted greedily every T2 = 20 iterations among three candidate values. (Martens & Grosse, 2015) `ev:reported` p. 27 ^martens2015optimizing-037
- K-FAC's momentum combines the new proposal with the previous update, choosing both coefficients jointly to minimize the exact-Fisher quadratic model. (Martens & Grosse, 2015) `ev:asserted` p. 28 ^martens2015optimizing-038
- Empirically, this momentum provides substantial acceleration in regimes where the gradient signal has a low noise to signal ratio. (Martens & Grosse, 2015) `ev:measured` p. 28 ^martens2015optimizing-039
- For a quadratic objective computed without noise, this momentum makes K-FAC equivalent to preconditioned linear CG with the approximate Fisher preconditioner. (Martens & Grosse, 2015) `ev:computed` p. 28 ^martens2015optimizing-040
- The experiments used data subsets of τ1 = 1/8 and τ2 = 1/4, which seemed to have a negligible effect on update quality. (Martens & Grosse, 2015) `ev:measured` p. 29 ^martens2015optimizing-041
- In a basic implementation of K-FAC, the matrix inverses or SVDs needed for the approximate Fisher inverse can dominate the per-iteration cost. (Martens & Grosse, 2015) `ev:asserted` p. 30 ^martens2015optimizing-042
- Recomputing the approximate Fisher inverse only every T3 = 20 iterations resulted in only a modest decrease in update quality. (Martens & Grosse, 2015) `ev:measured` p. 30 ^martens2015optimizing-043
- Without damping or momentum, [[Kronecker-factored approximate curvature|K-FAC]]'s optimization path through predictive distributions is invariant to a broad class of fixed invertible network transformations. (Martens & Grosse, 2015) `ev:computed` p. 35 ^martens2015optimizing-044
- As a consequence, K-FAC is invariant to choosing logistic sigmoid versus tanh activations, given equivalent initializations and negligible damping. (Martens & Grosse, 2015) `ev:computed` p. 35 ^martens2015optimizing-045
- [[Kronecker-factored approximate curvature|K-FAC]] is invariant to arbitrary affine transformations of the network input, which include many popular training data preprocessing techniques. (Martens & Grosse, 2015) `ev:computed` p. 35 ^martens2015optimizing-046
- Undamped [[Kronecker-factored approximate curvature|block-diagonal K-FAC]] updates equal gradient descent on a transformed network whose unit activities and unit-gradients are centered and whitened. (Martens & Grosse, 2015) `ev:computed` p. 36 ^martens2015optimizing-047
- K-FAC inverts matrices roughly as large as TONGA's, but only two per layer rather than one per unit. (Martens & Grosse, 2015) `ev:asserted` p. 36 ^martens2015optimizing-048
- The closest prior work, by Heskes, proposed a Fisher approximation similar to K-FAC's Kronecker-factored block-diagonal approximation for feed-forward networks. (Martens & Grosse, 2015) `ev:cited` p. 37 ^martens2015optimizing-049
- The authors observed that basic Tikhonov damping cannot produce high quality updates by itself, even when γ is chosen optimally each iteration. (Martens & Grosse, 2015) `ev:measured` p. 37 ^martens2015optimizing-050
- The basic unbiased stochastic approximation of the gradient-side factors was found to work nearly as well as the exact values in practice. (Martens & Grosse, 2015) `ev:measured` p. 37 ^martens2015optimizing-051
- K-FAC was evaluated on the three deep autoencoder problems of Hinton and Salakhutdinov, using the MNIST, CURVES and FACES datasets. (Martens & Grosse, 2015) `ev:reported` p. 39 ^martens2015optimizing-052
- The baseline was SGD with Nesterov-style momentum from Sutskever and colleagues, calibrated to work well on these deep autoencoder problems. (Martens & Grosse, 2015) `ev:reported` p. 39 ^martens2015optimizing-053
- Both methods were implemented in vectorized MATLAB with the Jacket GPU package and run on an NVidia GTX 580 GPU. (Martens & Grosse, 2015) `ev:reported` p. 40 ^martens2015optimizing-054
- On MNIST, results strongly suggest K-FAC's per-iteration rate of progress with momentum tends to a superlinear function of mini-batch size. (Martens & Grosse, 2015) `ev:measured` p. 40 ^martens2015optimizing-055
- For the SGD baseline, increasing the mini-batch size had a much smaller effect on the per-iteration rate of progress. (Martens & Grosse, 2015) `ev:measured` p. 40 ^martens2015optimizing-056
- K-FAC used an exponentially increasing mini-batch schedule starting from m1 = 1000 and reaching the full training set at iteration 500. (Martens & Grosse, 2015) `ev:reported` p. 42 ^martens2015optimizing-057
- With momentum, [[Kronecker-factored approximate curvature|K-FAC]]'s per-iteration rate of progress was orders of magnitude higher than the baseline's on each of the three problems. (Martens & Grosse, 2015) `ev:measured` p. 42 ^martens2015optimizing-058
- Without the momentum technique of Section 7, K-FAC was not significantly faster than the momentum SGD baseline on these problems. (Martens & Grosse, 2015) `ev:measured` p. 42 ^martens2015optimizing-059
- The block-tridiagonal version of K-FAC typically had a per-iteration rate of progress 25% to 40% larger than the block-diagonal version. (Martens & Grosse, 2015) `ev:measured` p. 45 ^martens2015optimizing-060
- Given the higher cost of its iterations, the block-tridiagonal version's per-second rate of progress seemed only moderately higher than the block-diagonal version's. (Martens & Grosse, 2015) `ev:measured` p. 45 ^martens2015optimizing-061
- The authors suggest the block-diagonal version is probably the better overall option due to its greater simplicity and comparable per-second progress. (Martens & Grosse, 2015) `ev:asserted` p. 45 ^martens2015optimizing-062
- The results suggest K-FAC may be much better suited than SGD for massively distributed implementation, requiring far fewer synchronization steps. (Martens & Grosse, 2015) `ev:asserted` p. 45 ^martens2015optimizing-063
- Proposed future work includes extending K-FAC to recurrent or convolutional architectures, which may require specialized approximations of their Fisher matrices. (Martens & Grosse, 2015) `ev:asserted` p. 46 ^martens2015optimizing-064

## 🎯 Contributions

## 📖 Glossary

- **Natural gradient** — Gradient preconditioned by the inverse Fisher, measuring change in the model's predictive distribution.
- **Fisher information matrix** — Expected outer product of log-likelihood gradients under the model's predictive distribution.
- **Empirical Fisher** — Fisher variant using training targets instead of targets sampled from the model.
- **Kronecker product** — Block matrix product whose inverse factorizes as the Kronecker product of inverses.
- **Generalized Gauss-Newton matrix (GGN)** — Positive semi-definite Hessian approximation, equal to the Fisher for exponential-family losses.
- **Hessian-free optimization (HF)** — Second-order method optimizing local quadratic models with linear conjugate gradient.
- **Tikhonov damping** — Adding a multiple of the identity to the curvature matrix, akin to trust regions.
- **Levenberg-Marquardt rule** — Adjusts damping strength from the ratio of actual to predicted objective reduction.
- **Block-tridiagonal inverse** — Inverse whose nonzero blocks lie only on and adjacent to the diagonal.

## ❓ Open questions

- Why does the factored Tikhonov approach often work better than exact Tikhonov damping, which the authors call somewhat mysterious?
- Is there an argument for why activities and backpropagated derivatives should be approximately jointly Gaussian, justifying the Kronecker factorization?
- Can the Kronecker-factored block-diagonal approximation be interpreted as the Hessian of a self-evidently intrinsic measure?
- How should K-FAC handle gradient stochasticity more principledly than a pre-determined increasing mini-batch schedule?
- How should the Fisher approximation be specialized for recurrent or convolutional architectures?
- Would the block-tridiagonal version win overall with approximate or parallel SVD computation?

## 📝 Notes on reading

Version read: arXiv 1503.05671v7 (8 Jun 2020), matching the packet identifier. Figures 2, 3, 5 and 6 show Fisher and inverse-Fisher matrices as images; only their captions and the text describing them were used. Figures 9, 10 and 11 (error curves) were extracted as raw axis ticks and legends; only the textual summaries were claimed. On p. 2 the counts of HF updates versus diagonal-method updates appear as garbled superscripts (∼102 and ∼104 −105, presumably 10^2 and 10^4-10^5) and were not claimed. The ℓ2 coefficient η on p. 39 is printed as 10−5 (presumably 10^-5) and was not claimed. The appendices (pp. 49-58: proofs, inversion of Kronecker-sum matrices, the Fisher-vector product trick) were not claimed beyond what the main text states. Related-work points not claimed for volume: the FANG method as precursor of the graphical-model view (p. 11) and the concurrent empirical-Fisher method of Povey et al. (p. 38).

## Suggested new concepts

- K-FAC (Kronecker-factored Approximate Curvature) — widely reused second-order optimizer family that later papers extend to convolutional and distributed settings.
- Natural gradient descent — the core idea K-FAC approximates; links information geometry and second-order optimization.
- Fisher information matrix — central curvature object whose approximations define many optimizers.
- Tikhonov damping and trust regions — damping design is presented as crucial for any practical second-order method.
- Hessian-free optimization — main prior second-order baseline that K-FAC is positioned against.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — K-FAC: gradiente natural escalable (B.3).

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
