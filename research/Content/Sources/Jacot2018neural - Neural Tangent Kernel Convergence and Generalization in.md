---
aliases: []
type: "source"
title: "Neural Tangent Kernel: Convergence and Generalization in Neural Networks"
citekey: "Jacot2018neural"
doi: "10.48550/arXiv.1806.07572"
arxiv: "1806.07572"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1806.07572"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Arthur Jacot", "Franck Gabriel", "Clément Hongler"]
sha256: ["e052eb972f646747ac4554a294eb62874077e59a5f585f459e2dbd5cb2a0975d"]
pdf: "Content/Papers/Jacot2018neural.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Jacot2018neural.pdf]]

> [!abstract] One-sentence summary
> The paper introduces the Neural Tangent Kernel and proves that, in the infinite-width limit, gradient descent on a fully connected network is kernel gradient descent with a fixed, explicit kernel, linking network training to kernel methods.

## Abstract

At initialization, artificial neural networks (ANNs) are equivalent to Gaussian processes in the infinite-width limit, thus connecting them to kernel methods. We prove that the evolution of an ANN during training can also be described by a kernel: during gradient descent on the parameters of an ANN, the network function $f_θ$ (which maps input vectors to output vectors) follows the kernel gradient of the functional cost (which is convex, in contrast to the parameter cost) w.r.t. a new kernel: the Neural Tangent Kernel (NTK). This kernel is central to describe the generalization features of ANNs. While the NTK is random at initialization and varies during training, in the infinite-width limit it converges to an explicit limiting kernel and it stays constant during training. This makes it possible to study the training of ANNs in function space instead of parameter space. Convergence of the training can then be related to the positive-definiteness of the limiting NTK. We prove the positive-definiteness of the limiting NTK when the data is supported on the sphere and the non-linearity is non-polynomial. We then focus on the setting of least-squares regression and show that in the infinite-width limit, the network function $f_θ$ follows a linear differential equation during training. The convergence is fastest along the largest kernel principal components of the input data with respect to the NTK, hence suggesting a theoretical motivation for early stopping. Finally we study the NTK numerically, observe its behavior for wide networks, and compare it to the infinite-width limit. (arXiv)

## 🧠 Key ideas (atomic)

- Infinite-width artificial neural networks at initialization are equivalent to Gaussian processes, which connects them to kernel methods. (Jacot et al., 2018) `ev:cited` p. 1 ^jacot2018neural-001
- The loss surface of neural network optimization is highly non-convex, with a high number of saddle points that may slow convergence. (Jacot et al., 2018) `ev:cited` p. 1 ^jacot2018neural-002
- Kernels from the infinite-width Gaussian limit, used in Bayesian inference or support vector machines, yield results comparable to gradient-trained networks. (Jacot et al., 2018) `ev:cited` p. 2 ^jacot2018neural-003
- It seems paradoxical that reasonably large networks fitting random labels still obtain good test accuracy when trained on real data. (Jacot et al., 2018) `ev:cited` p. 2 ^jacot2018neural-004
- The paper describes the training dynamics of the network function of fully connected networks in the infinite-width limit. (Jacot et al., 2018) `ev:asserted` p. 2 ^jacot2018neural-005
- The theoretical results are investigated numerically on an artificial dataset of points on the unit circle and on MNIST. (Jacot et al., 2018) `ev:reported` p. 2 ^jacot2018neural-006
- In the numerical investigation, the authors observe that the behavior of wide networks is close to the theoretical infinite-width limit. (Jacot et al., 2018) `ev:measured` p. 2 ^jacot2018neural-007
- The paper considers fully connected networks with a Lipschitz, twice differentiable nonlinearity that has a bounded second derivative. (Jacot et al., 2018) `ev:reported` p. 2 ^jacot2018neural-008
- The smoothness assumptions on the nonlinearity do not seem to be strictly needed for the results to hold true. (Jacot et al., 2018) `ev:asserted` p. 2 ^jacot2018neural-009
- Parameters consisting of connection matrices and bias vectors are initialized as iid Gaussians N(0, 1) in this setup. (Jacot et al., 2018) `ev:reported` p. 2 ^jacot2018neural-010
- The paper assumes the input distribution is the empirical distribution on a finite dataset, a sum of Dirac measures. (Jacot et al., 2018) `ev:reported` p. 3 ^jacot2018neural-011
- A scalar parameter β > 0 in the network parametrization tunes the influence of the bias on the training. (Jacot et al., 2018) `ev:reported` p. 3 ^jacot2018neural-012
- The factors of one over square root width are key to obtaining consistent asymptotic behavior as hidden layer widths grow to infinity. (Jacot et al., 2018) `ev:asserted` p. 3 ^jacot2018neural-013
- In the numerical experiments the authors take β = 0.1 and a learning rate of 1.0, which is larger than usual. (Jacot et al., 2018) `ev:reported` p. 3 ^jacot2018neural-014
- Even for a convex functional cost, the composite cost over the network parameters is in general highly non-convex. (Jacot et al., 2018) `ev:cited` p. 3 ^jacot2018neural-015
- Convergence of kernel gradient descent to a critical point of the cost is guaranteed if the kernel is positive definite. (Jacot et al., 2018) `ev:computed` p. 4 ^jacot2018neural-016
- If the cost is convex and bounded from below, kernel gradient descent converges to a global minimum as time tends to infinity. (Jacot et al., 2018) `ev:computed` p. 4 ^jacot2018neural-017
- Gradient descent on a random-features linear parametrization is equivalent to kernel gradient descent with a random tangent kernel in function space. (Jacot et al., 2018) `ev:computed` p. 4 ^jacot2018neural-018
- Because the realization function of networks is not linear, the [[Neural Tangent Kernel|NTK]] is random at initialization and varies during training. (Jacot et al., 2018) `ev:computed` p. 5 ^jacot2018neural-019
- Proposition 1 shows that at initialization the output functions tend in law to iid centered Gaussian processes as widths grow. (Jacot et al., 2018) `ev:computed` p. 5 ^jacot2018neural-020
- Theorem 1 proves that at initialization the [[Neural Tangent Kernel|NTK]] converges in probability to a deterministic limiting kernel as layer widths grow. (Jacot et al., 2018) `ev:computed` p. 5 ^jacot2018neural-021
- The [[Neural Tangent Kernel|limiting NTK]] depends only on the choice of nonlinearity, the network depth and the parameter variance at initialization. (Jacot et al., 2018) `ev:computed` p. 5 ^jacot2018neural-022
- Theorem 2 proves that the [[Neural Tangent Kernel|NTK]] stays asymptotically constant during training, uniformly over a time interval, in the infinite-width limit. (Jacot et al., 2018) `ev:computed` p. 6 ^jacot2018neural-023
- The training framework allows directions that depend on another network, as is the case for generative adversarial networks. (Jacot et al., 2018) `ev:asserted` p. 6 ^jacot2018neural-024
- The variation during training of individual hidden-layer activations shrinks as their width grows, as the proof of Theorem 2 shows. (Jacot et al., 2018) `ev:computed` p. 6 ^jacot2018neural-025
- The collective variation of hidden activations remains significant, which allows the parameters of the lower layers to learn. (Jacot et al., 2018) `ev:asserted` p. 6 ^jacot2018neural-026
- The authors postulate that the span of last-layer preactivations becomes dense in function space for many measures and nonlinearities. (Jacot et al., 2018) `ev:asserted` p. 6 ^jacot2018neural-027
- For a non-polynomial Lipschitz nonlinearity, the [[Neural Tangent Kernel|limiting NTK]] restricted to the unit sphere is positive definite for depth L ≥ 2. (Jacot et al., 2018) `ev:computed` p. 6 ^jacot2018neural-028
- For least-squares regression, the training direction norm is strictly decreasing during training, so Theorems 1 and 2 apply. (Jacot et al., 2018) `ev:computed` p. 6 ^jacot2018neural-029
- Under kernel gradient descent on a least-squares cost, the function follows a linear differential equation with an exponential solution. (Jacot et al., 2018) `ev:computed` p. 6 ^jacot2018neural-030
- The map Π has at most NnL positive eigenfunctions, which are the kernel principal components of the data with respect to the kernel. (Jacot et al., 2018) `ev:computed` p. 7 ^jacot2018neural-031
- Convergence during least-squares training is faster along the eigenspaces corresponding to larger eigenvalues of the kernel map. (Jacot et al., 2018) `ev:computed` p. 7 ^jacot2018neural-032
- The authors argue this decomposition motivates early stopping, which focuses convergence on the most relevant kernel principal components. (Jacot et al., 2018) `ev:asserted` p. 7 ^jacot2018neural-033
- Directions with lower eigenvalues are typically the noisier ones; for the RBF kernel they correspond to high frequency functions. (Jacot et al., 2018) `ev:asserted` p. 7 ^jacot2018neural-034
- If the initial function is Gaussian, as for infinite-width networks, the function remains Gaussian at all times during training. (Jacot et al., 2018) `ev:computed` p. 7 ^jacot2018neural-035
- The mean of the limiting function equals the MAP estimate under a Gaussian prior with covariance given by the limiting NTK. (Jacot et al., 2018) `ev:computed` p. 7 ^jacot2018neural-036
- Equivalently, this mean equals kernel ridge regression with the limiting kernel as the regularization goes to zero. (Jacot et al., 2018) `ev:computed` p. 7 ^jacot2018neural-037
- Experiments use fully connected networks of various widths, with equal hidden layer sizes and the ReLU nonlinearity. (Jacot et al., 2018) `ev:reported` p. 7 ^jacot2018neural-038
- In the first two experiments, the input dimension is n0 = 2 and the input elements lie on the unit circle. (Jacot et al., 2018) `ev:reported` p. 7 ^jacot2018neural-039
- The first experiment compares the NTK of depth L = 4 networks at widths n = 500 and 10000 over 10 independent initializations. (Jacot et al., 2018) `ev:reported` p. 8 ^jacot2018neural-040
- Kernels were plotted at initialization and after 200 steps of gradient descent with learning rate 1.0 on the target x1x2. (Jacot et al., 2018) `ev:reported` p. 8 ^jacot2018neural-041
- For the wider network, the NTK shows less variance and is smoother than for the narrower network. (Jacot et al., 2018) `ev:measured` p. 8 ^jacot2018neural-042
- The expectation of the NTK is very close for both network widths in the first experiment. (Jacot et al., 2018) `ev:measured` p. 8 ^jacot2018neural-043
- After 200 steps of training the NTK tends to inflate, an effect much less apparent for n = 10000 than for n = 500. (Jacot et al., 2018) `ev:measured` p. 8 ^jacot2018neural-044
- Networks of widths n = 50 and 1000 were trained for 1000 steps with learning rate 1.0 on 4 unit-circle points. (Jacot et al., 2018) `ev:reported` p. 8 ^jacot2018neural-045
- Network function distributions at both widths appear close in mean and variance to the limiting distribution at convergence. (Jacot et al., 2018) `ev:measured` p. 8 ^jacot2018neural-046
- Even for relatively small widths (n = 50), the NTK gives a good indication of the network function distribution at convergence. (Jacot et al., 2018) `ev:measured` p. 8 ^jacot2018neural-047
- The first 3 principal components of N = 512 MNIST digits were computed with respect to the NTK of an n = 10000 network. (Jacot et al., 2018) `ev:reported` p. 8 ^jacot2018neural-048
- The eigenvalues of the first three MNIST kernel principal components are λ1 = 0.0457, λ2 = 0.00108 and λ3 = 0.00078. (Jacot et al., 2018) `ev:measured` p. 8 ^jacot2018neural-049
- Because the kernel PCA is non-centered, the first MNIST principal component is almost equal to the constant function. (Jacot et al., 2018) `ev:asserted` p. 8 ^jacot2018neural-050
- With β = 1.0 instead of 0.1, the gap between the first and second principal component is about ten times bigger. (Jacot et al., 2018) `ev:measured` p. 9 ^jacot2018neural-051
- The authors state that this larger eigenvalue gap obtained with β = 1.0 makes training of the network more difficult. (Jacot et al., 2018) `ev:asserted` p. 9 ^jacot2018neural-052
- Networks of widths 100, 1000 and 10000 were trained toward a target equal to the initial function plus 0.5 times the second component. (Jacot et al., 2018) `ev:reported` p. 9 ^jacot2018neural-053
- Wider networks deviate less from the straight-line trajectory predicted along the second principal component, in two trials per width. (Jacot et al., 2018) `ev:measured` p. 9 ^jacot2018neural-054
- As the width grows, the trajectory along the second principal component converges to the theoretical infinite-width limit. (Jacot et al., 2018) `ev:measured` p. 9 ^jacot2018neural-055
- Smaller networks appear to converge faster than wider ones in the MNIST principal component experiment. (Jacot et al., 2018) `ev:measured` p. 9 ^jacot2018neural-056
- The authors suggest the faster convergence of smaller networks may be explained by the NTK inflation observed in the first experiment. (Jacot et al., 2018) `ev:asserted` p. 9 ^jacot2018neural-057
- Since the [[Neural Tangent Kernel|NTK]] of large-width networks is more stable during training, larger learning rates can in principle be taken. (Jacot et al., 2018) `ev:asserted` p. 9 ^jacot2018neural-058
- The authors conclude that the [[Neural Tangent Kernel|limiting NTK]] is a powerful tool to understand the generalization properties of neural networks. (Jacot et al., 2018) `ev:asserted` p. 9 ^jacot2018neural-059
- The appendix proofs take the width limits sequentially, which the authors say leads to much simpler proofs than a joint limit. (Jacot et al., 2018) `ev:asserted` p. 11 ^jacot2018neural-060
- The authors state the results could in principle be strengthened to the setting where the minimum hidden width tends to infinity. (Jacot et al., 2018) `ev:asserted` p. 11 ^jacot2018neural-061
- The pre-activations stay Gaussian during training as well, with the same covariance as at initialization. (Jacot et al., 2018) `ev:computed` p. 15 ^jacot2018neural-062
- For a polynomial nonlinearity, the corresponding NTK is not positive definite on the sphere for certain input dimensions. (Jacot et al., 2018) `ev:computed` p. 19 ^jacot2018neural-063

## 🎯 Contributions

## 📖 Glossary

- **Neural Tangent Kernel (NTK)** — Sum over parameters of outer products of network-function derivatives; governs training dynamics.
- **Kernel gradient descent** — Function-space descent where the cost derivative is mapped to a function through a kernel.
- **Infinite-width limit** — Regime where hidden layer widths tend to infinity, making network behavior deterministic or Gaussian.
- **NTK parametrization** — Scaling each layer by one over square root width, with a bias weight β.
- **Kernel principal components** — Eigenfunctions of the kernel operator on the data, ordered by captured variance.
- **Positive-definite kernel** — Kernel whose induced norm is positive for every function nonzero on the data.
- **Early stopping** — Halting training before convergence to avoid fitting low-eigenvalue, noisier directions.

## ❓ Open questions

- Do the results hold without the Lipschitz, twice differentiable, bounded-second-derivative assumptions on the nonlinearity?
- Can the sequential width limits be replaced by a joint limit where the minimum width tends to infinity?
- Is the limiting NTK positive definite for data not supported on the sphere, as the authors postulate?
- How large must a finite network be for the constant-NTK description to hold, and how does the NTK inflation depend on width?
- Does the constant-kernel regime explain generalization of practical networks, given that hidden representations barely change?
- How do the results extend beyond fully connected architectures?

## 📝 Notes on reading

Version read: arXiv 1806.07572v4 (10 Feb 2020), the NIPS 2018 paper with appendix; matches the packet identifier.

Figures 1, 2 and 3 are plots only described in the text: Fig. 1 shows the NTK Θ(4)(x0, x) on the unit circle for n = 500 and 10000 at t = 0 and t = 200; Fig. 2 shows network functions near convergence for n = 50 and 1000 against the 10th, 50th and 90th percentiles of the limiting Gaussian; Fig. 3 shows MNIST on its 2nd and 3rd kernel principal components, the deviation ||ht|| from the straight line, and the convergence ||gt|| along the 2nd component for n = 100, 1000, 10000.

Equations throughout (recursions for Σ and Θ, the least-squares solution, appendix bounds) are garbled by extraction; rates such as O(1/√nL) and n^-3/2 in the proof of Theorem 2 were not claimed as numbers.

The introduction calls the kernel the neural tangent network (p. 2), an evident typo for neural tangent kernel.

The main-text statements of Theorems 1 and 2 omit the word sequentially; the appendix versions state the limits are taken sequentially.

## Suggested new concepts

- Neural Tangent Kernel — central object linking wide-network training to kernel methods, reused across many later theory papers.
- Infinite-width limit of neural networks — shared regime for NNGP and NTK results that deserves one consolidating note.
- Kernel gradient descent — function-space view of training that recurs in analyses of optimization and generalization.
- Lazy training — the regime where hidden activations barely move during training, implied by the constant NTK.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Geometría del espacio de funciones (E.1).

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
