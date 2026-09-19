---
aliases: []
type: "source"
title: "Old Optimizer, New Norm: An Anthology"
citekey: "Bernstein2024old"
doi: "10.48550/arXiv.2409.20325"
arxiv: "2409.20325"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2409.20325"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Jeremy Bernstein", "Laker Newhouse"]
sha256: ["75e911f6d3ab68ac04e3bfab622b32e052116cd01ca2d2b909731b1aedd7f140"]
pdf: "Content/Papers/Bernstein2024old.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Bernstein2024old.pdf]]

> [!abstract] One-sentence summary
> The paper recasts Adam, Shampoo and Prodigy, with their moving averages switched off, as steepest descent under particular norms, framing optimizer design as choosing a per-layer norm and a step size.

## Abstract

Deep learning optimizers are often motivated through a mix of convex and approximate second-order theory. We select three such methods -- Adam, Shampoo and Prodigy -- and argue that each method can instead be understood as a squarely first-order method without convexity assumptions. In fact, after switching off exponential moving averages, each method is equivalent to steepest descent under a particular norm. By generalizing this observation, we chart a new design space for training algorithms. Different operator norms should be assigned to different tensors based on the role that the tensor plays within the network. For example, while linear and embedding layers may have the same weight space of $\mathbb{R}^{m\times n}$, these layers play different roles and should be assigned different norms. We hope that this idea of carefully metrizing the neural architecture might lead to more stable, scalable and indeed faster training. (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that Adam, Shampoo and Prodigy can be understood as squarely first-order methods without any convexity assumptions. (Bernstein & Newhouse, 2024) `ev:asserted` p. 1 ^bernstein2024old-001
- After their exponential moving averages are disabled, each of the three optimizers is shown to be a variant of steepest descent under a certain norm. (Bernstein & Newhouse, 2024) `ev:computed` p. 1 ^bernstein2024old-002
- The authors describe exponential moving averages as smoothing out the algorithm, making it more robust to mini-batch noise. (Bernstein & Newhouse, 2024) `ev:asserted` p. 1 ^bernstein2024old-003
- Nailing down the precise role of exponential moving averages in these optimizers is perhaps still an open problem, according to the authors. (Bernstein & Newhouse, 2024) `ev:asserted` p. 1 ^bernstein2024old-004
- Steepest descent chooses a weight update minimising a local quadratic model of the loss, with sharpness and norm fixed a priori. (Bernstein & Newhouse, 2024) `ev:asserted` p. 1 ^bernstein2024old-005
- The authors consider steepest descent a squarely first-order method, as it never touches an approximate Hessian during training. (Bernstein & Newhouse, 2024) `ev:asserted` p. 1 ^bernstein2024old-006
- Proposition 1 computes the steepest descent step size as the dual norm of the gradient divided by the sharpness. (Bernstein & Newhouse, 2024) `ev:computed` p. 2 ^bernstein2024old-007
- The steepest descent step direction is the unit vector that maximises the inner product with the gradient, per Proposition 1. (Bernstein & Newhouse, 2024) `ev:computed` p. 2 ^bernstein2024old-008
- Increasing the sharpness decreases the size of the steepest descent solution vector, as illustrated in Figure 1. (Bernstein & Newhouse, 2024) `ev:computed` p. 2 ^bernstein2024old-009
- Changing the norm can change the direction of the steepest descent solution vector when the gradient is not axis-aligned. (Bernstein & Newhouse, 2024) `ev:computed` p. 2 ^bernstein2024old-010
- The authors state that past optimizers implicitly assign different induced matrix norms to network layers, in a somewhat haphazard manner. (Bernstein & Newhouse, 2024) `ev:asserted` p. 2 ^bernstein2024old-011
- Varying the input and output vector norms induces a large family of matrix norms, implying a large family of steepest descent optimizers. (Bernstein & Newhouse, 2024) `ev:asserted` p. 2 ^bernstein2024old-012
- The original Adam paper by Kingma and Ba now has well over 100,000 citations, according to the authors. (Bernstein & Newhouse, 2024) `ev:cited` p. 3 ^bernstein2024old-013
- With exponential moving averages switched off, the updates of Adam, ignoring bias corrections, reduce to sign gradient descent. (Bernstein & Newhouse, 2024) `ev:computed` p. 3 ^bernstein2024old-014
- Tieleman and Hinton already called RMSprop, which Adam builds on, the mini-batch version of just using the gradient sign. (Bernstein & Newhouse, 2024) `ev:cited` p. 3 ^bernstein2024old-015
- Sign descent solves steepest descent under the vector infinity norm, with step size equal to the gradient's ℓ1 norm over sharpness. (Bernstein & Newhouse, 2024) `ev:computed` p. 3 ^bernstein2024old-016
- The authors suggest the infinity norm on the flattened weight space has nothing to do with deep learning; a coincidence is at play. (Bernstein & Newhouse, 2024) `ev:asserted` p. 4 ^bernstein2024old-017
- The infinity norm of the flattened weight vector equals the largest ℓ1 to infinity operator norm across the layers. (Bernstein & Newhouse, 2024) `ev:computed` p. 4 ^bernstein2024old-018
- The authors name the maximum over layers of the ℓ1 to infinity operator norm the max-of-max norm. (Bernstein & Newhouse, 2024) `ev:asserted` p. 4 ^bernstein2024old-019
- Layerwise sign descent solves the matrix-aware steepest descent problem under the max-of-max norm, per Proposition 3. (Bernstein & Newhouse, 2024) `ev:computed` p. 4 ^bernstein2024old-020
- Implicit per-matrix gradient normalization may be a major reason Adam, sign descent and Lion outperform vanilla gradient descent in large language model training. (Bernstein & Newhouse, 2024) `ev:asserted` p. 4 ^bernstein2024old-021
- A variant of the Shampoo optimizer won the external tuning track of the 2024 AlgoPerf training algorithms competition. (Bernstein & Newhouse, 2024) `ev:cited` p. 5 ^bernstein2024old-022
- Shampoo was originally motivated as a generalization of the AdaGrad convex optimizer to tensor spaces. (Bernstein & Newhouse, 2024) `ev:cited` p. 5 ^bernstein2024old-023
- Practitioners usually replace the simple sums in [[Kronecker-factored preconditioning|the left and right Shampoo preconditioners]] with exponential moving averages. (Bernstein & Newhouse, 2024) `ev:cited` p. 5 ^bernstein2024old-024
- With accumulation disabled, Shampoo updates the weights by the semi-orthogonal factor UV^T from the gradient's reduced singular value decomposition. (Bernstein & Newhouse, 2024) `ev:computed` p. 5 ^bernstein2024old-025
- Shampoo without accumulation projects the gradient matrix to the closest semi-orthogonal matrix in Frobenius norm. (Bernstein & Newhouse, 2024) `ev:computed` p. 5 ^bernstein2024old-026
- The closest semi-orthogonal matrix UV^T to the gradient in Frobenius norm is unique if and only if the gradient has full rank. (Bernstein & Newhouse, 2024) `ev:computed` p. 5 ^bernstein2024old-027
- Shampoo without accumulation is steepest descent under the maximum spectral norm over all the matrices in the network. (Bernstein & Newhouse, 2024) `ev:computed` p. 5 ^bernstein2024old-028
- Under the max spectral norm, the step size is the sum over layers of each gradient's singular value trace, divided by the sharpness. (Bernstein & Newhouse, 2024) `ev:computed` p. 6 ^bernstein2024old-029
- The authors present the use of a max norm over layers as a novelty relative to prior stochastic spectral descent work. (Bernstein & Newhouse, 2024) `ev:asserted` p. 6 ^bernstein2024old-030
- The authors state their main contribution here is connecting spectral-norm steepest descent to Shampoo without accumulation. (Bernstein & Newhouse, 2024) `ev:asserted` p. 6 ^bernstein2024old-031
- For a linear predictor under square loss, the loss admits an upper bound quadratic in the spectral norm of the weight perturbation. (Bernstein & Newhouse, 2024) `ev:computed` p. 6 ^bernstein2024old-032
- The square loss bound of Proposition 6 assumes every input is normalized to an ℓ2 norm equal to the square root of the input dimension. (Bernstein & Newhouse, 2024) `ev:computed` p. 6 ^bernstein2024old-033
- Choosing the weight perturbation to minimise this upper bound on the square loss is precisely steepest descent under the spectral norm. (Bernstein & Newhouse, 2024) `ev:computed` p. 6 ^bernstein2024old-034
- Deriving an upper bound on the loss and then minimising it is known generally as majorization-minimization. (Bernstein & Newhouse, 2024) `ev:cited` p. 6 ^bernstein2024old-035
- Table 1 links sign descent, the cousin of Adam, to steepest descent under the vector infinity norm. (Bernstein & Newhouse, 2024) `ev:computed` p. 7 ^bernstein2024old-036
- Table 1 links spectral descent, the cousin of Shampoo, to steepest descent under the Schatten infinity or spectral norm on matrices. (Bernstein & Newhouse, 2024) `ev:computed` p. 7 ^bernstein2024old-037
- The authors argue that viewing Shampoo as a smoothed projection onto semi-orthogonal matrices grounds it in prior spectral descent literature. (Bernstein & Newhouse, 2024) `ev:asserted` p. 7 ^bernstein2024old-038
- Prodigy belongs to recent works that attempt to apply convex theory to design deep learning optimizers that do not require tuning. (Bernstein & Newhouse, 2024) `ev:cited` p. 8 ^bernstein2024old-039
- The authors analyse Algorithm 3 of the Prodigy paper, since this is the version used in its experiments. (Bernstein & Newhouse, 2024) `ev:reported` p. 8 ^bernstein2024old-040
- With exponential moving averages switched off, Prodigy reduces to sign gradient descent with a dynamically chosen step size that warms up automatically. (Bernstein & Newhouse, 2024) `ev:computed` p. 8 ^bernstein2024old-041
- The authors define escape velocity as the unknown but optimal initial step size, reached once the weights escape the initial linearization. (Bernstein & Newhouse, 2024) `ev:asserted` p. 8 ^bernstein2024old-042
- The heuristic doubles a very small initial step size each step until the weights escape the linearization of the loss around initialization. (Bernstein & Newhouse, 2024) `ev:asserted` p. 8 ^bernstein2024old-043
- If the step size were chosen optimally, the directional derivative along the first weight update must vanish, following Cauchy. (Bernstein & Newhouse, 2024) `ev:cited` p. 9 ^bernstein2024old-044
- The authors note that this escape-velocity step size procedure has no reliance on convexity assumptions. (Bernstein & Newhouse, 2024) `ev:asserted` p. 9 ^bernstein2024old-045
- Under dense-gradient and near-initialization assumptions, the next Prodigy step size approximately equals the maximum of the current step size and RMS weight change. (Bernstein & Newhouse, 2024) `ev:computed` p. 9 ^bernstein2024old-046
- While these assumptions hold, the step size at the next step is equivalent to the whole progress made so far. (Bernstein & Newhouse, 2024) `ev:computed` p. 9 ^bernstein2024old-047
- This analysis suggests exponential growth in the Prodigy step size that continues until the weights leave the neighbourhood of initialization. (Bernstein & Newhouse, 2024) `ev:computed` p. 9 ^bernstein2024old-048
- The decision of Prodigy to only let the step size increase and never decrease could be sub-optimal, according to the authors. (Bernstein & Newhouse, 2024) `ev:asserted` p. 9 ^bernstein2024old-049
- The authors suggest one could measure the angle using the most recent weight difference instead of the difference from initialization. (Bernstein & Newhouse, 2024) `ev:asserted` p. 9 ^bernstein2024old-050
- The authors describe Prodigy's step size adjustment, based on the angle between gradient and total weight change, as online line search. (Bernstein & Newhouse, 2024) `ev:asserted` p. 9 ^bernstein2024old-051
- The authors think the norm and step size decisions made by Adam, Shampoo and Prodigy are somewhat arbitrary. (Bernstein & Newhouse, 2024) `ev:asserted` p. 10 ^bernstein2024old-052
- The modular norm of Large and colleagues is the maximum over layers of each layer's norm times a scalar coefficient. (Bernstein & Newhouse, 2024) `ev:cited` p. 10 ^bernstein2024old-053
- The modular norm generalizes the norms that appeared in the propositions for Adam and for Shampoo, according to the authors. (Bernstein & Newhouse, 2024) `ev:asserted` p. 10 ^bernstein2024old-054
- Steepest descent under the modular norm uses a global step size computed as a weighted sum of the gradient dual norms over layers. (Bernstein & Newhouse, 2024) `ev:computed` p. 10 ^bernstein2024old-055
- The ℓ1 to ℓp induced operator norm of a matrix equals the largest ℓp norm among its columns. (Bernstein & Newhouse, 2024) `ev:computed` p. 10 ^bernstein2024old-056
- The ℓp to infinity induced operator norm of a matrix equals the largest dual ℓp norm over its rows. (Bernstein & Newhouse, 2024) `ev:computed` p. 10 ^bernstein2024old-057
- The authors argue linear layers should use the RMS to RMS operator norm, which resolves to a rescaled spectral norm. (Bernstein & Newhouse, 2024) `ev:asserted` p. 11 ^bernstein2024old-058
- Embedding layers, which map one-hot vectors to unit-RMS vectors, should use the ℓ1 to RMS operator norm, according to the authors. (Bernstein & Newhouse, 2024) `ev:asserted` p. 11 ^bernstein2024old-059
- The authors believe that picking the right norms could improve the speed and scalability of neural network training. (Bernstein & Newhouse, 2024) `ev:asserted` p. 11 ^bernstein2024old-060
- The authors report seeing evidence, from prior work, that better layer norms can lead to learning rate transfer across scale. (Bernstein & Newhouse, 2024) `ev:cited` p. 11 ^bernstein2024old-061
- The authors conclude that optimizer design can be viewed as choosing two things, a norm and a step size. (Bernstein & Newhouse, 2024) `ev:asserted` p. 11 ^bernstein2024old-062
- Computing the Shampoo update needs only one inverse matrix square root, of whichever Gram matrix of the gradient has smaller dimension. (Bernstein & Newhouse, 2024) `ev:computed` p. 15 ^bernstein2024old-063
- The authors list SVD, sketching, Newton iteration for inverse roots and [[Newton-Schulz orthogonalization|Newton-Schulz iteration]] as ways to compute the update. (Bernstein & Newhouse, 2024) `ev:reported` p. 15 ^bernstein2024old-064
- [[Newton-Schulz orthogonalization|The Newton-Schulz iteration]] applies a cubic polynomial to each singular value, pushing values in its convergence range toward one. (Bernstein & Newhouse, 2024) `ev:computed` p. 15 ^bernstein2024old-065
- [[Newton-Schulz orthogonalization|The iteration]] converges if the initial matrix has all singular values greater than zero and less than the square root of three. (Bernstein & Newhouse, 2024) `ev:computed` p. 15 ^bernstein2024old-066
- After first posting the paper, the authors learned that [[Newton-Schulz orthogonalization|the iteration]], at least for fixed coefficients, is classical. (Bernstein & Newhouse, 2024) `ev:cited` p. 15 ^bernstein2024old-067
- Which computational method is most useful may depend on the condition number of the gradient or the available computational resources. (Bernstein & Newhouse, 2024) `ev:asserted` p. 15 ^bernstein2024old-068

## 🎯 Contributions

## 📖 Glossary

- **Steepest descent** — update minimising a linear loss term plus a squared-norm penalty scaled by sharpness.
- **Sharpness** — the scalar λ weighting the quadratic norm penalty in steepest descent.
- **Dual norm** — the maximum inner product of a vector with unit-norm vectors.
- **Induced operator norm** — largest ratio of output norm to input norm a matrix achieves.
- **Max-of-max norm** — the maximum over layers of each layer's ℓ1 to ℓ∞ operator norm.
- **Spectral norm** — the ℓ2 to ℓ2 operator norm, equal to a matrix's largest singular value.
- **Semi-orthogonal matrix** — a matrix A with AA^T or A^TA equal to the identity.
- **Modular norm** — maximum over layers of scaled per-layer norms, from Large et al. (2024).
- **Escape velocity** — the unknown optimal initial step size that escapes the initial loss linearization.
- **Majorization-minimization** — design pattern that minimises a derived upper bound on the loss.
- **Newton-Schulz iteration** — polynomial matrix iteration converging to the orthogonal factor UV^T.

## ❓ Open questions

- What is the precise role of exponential moving averages once these optimizers are understood as steepest descent?
- Can the choice of norm and sharpness be turned from an art into a science for a given architecture?
- How should norms be assigned to tensor types beyond linear and embedding layers?
- Would a step size warm-up that can also decrease, or that uses the most recent weight difference, beat Prodigy's rule?
- Does the preliminary cosine-based step size rule hold up in systematic experiments?
- Which way of computing the orthogonalized update is fastest in practice at scale?

## 📝 Notes on reading

Read the arXiv v2 (6 Dec 2024), OPT2024 workshop version, matching the identifier 2409.20325. The paper is theoretical: nearly every result is a proposition with a proof in Appendix B; the only empirical statement is the brief mention of preliminary experiments with a cosine-based step size rule (p. 9), for which no numbers are given. Figure 1 (p. 2) shows norm balls for ℓ2, ℓ1 and ℓ∞ over a colour gradient, illustrating how sharpness scales and norm choice rotates the solution. The math extraction is garbled throughout (ℓ∞ rendered as ℓ8, Greek and operators as stray characters), so equations were paraphrased rather than quoted; Table 1 on p. 7 was reconstructed from the flattened cells. The appendix Newton-Schulz convergence bound (singular values in (0, √3)) was claimed in words.

## Suggested new concepts

- Steepest descent under a norm — unifying lens that recasts Adam, Shampoo and Prodigy as one family of first-order updates.
- Modular norm — per-layer norm assignment that generalizes the Adam and Shampoo norms and underlies later optimizers.
- Newton-Schulz orthogonalization — practical way to compute the spectral-descent update without an SVD.
- Escape velocity step size — automatic warm-up view of parameter-free optimizers such as Prodigy.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H4.** Reinterpreta Adam, Shampoo y Prodigy como descenso más pronunciado bajo normas concretas, la base teórica de elegir la geometría de cada paso.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
