---
aliases: []
type: "source"
title: "Pymanopt: A Python Toolbox for Optimization on Manifolds using Automatic Differentiation"
citekey: "Townsend2016pymanopt"
doi: "10.48550/arXiv.1603.03236"
arxiv: "1603.03236"
year: 2016
publication_type: "preprint"
url: "https://arxiv.org/abs/1603.03236"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["James Townsend", "Niklas Koep", "Sebastian Weichwald"]
sha256: ["ead0e9f60f58289464dc4d68fa2b6ca82b327c07df1f3ec945bbff28faf87c65"]
pdf: "Content/Papers/Townsend2016pymanopt.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 40
---

📄 PDF: [[Townsend2016pymanopt.pdf]]

> [!abstract] One-sentence summary
> Pymanopt is a Python port of the Manopt approach to Riemannian optimization that computes gradients and Hessians by automated differentiation (Autograd, Theano, TensorFlow), so users only define a manifold, a cost and a solver.

## Abstract

Optimization on manifolds is a class of methods for optimization of an objective function, subject to constraints which are smooth, in the sense that the set of points which satisfy the constraints admits the structure of a differentiable manifold. While many optimization problems are of the described form, technicalities of differential geometry and the laborious calculation of derivatives pose a significant barrier for experimenting with these methods. We introduce Pymanopt (available at https://pymanopt.github.io), a toolbox for optimization on manifolds, implemented in Python, that---similarly to the Manopt Matlab toolbox---implements several manifold geometries and optimization algorithms. Moreover, we lower the barriers to users further by using automated differentiation for calculating derivative information, saving users time and saving them from potential calculation and implementation errors. (arXiv)

## 🧠 Key ideas (atomic)

- Pymanopt is a Python toolbox for [[Riemannian optimization|optimization on manifolds]] that implements several manifold geometries and optimization algorithms, similarly to the Manopt Matlab toolbox. (Townsend et al., 2016) `ev:reported` p. 1 ^townsend2016pymanopt-001
- The authors state that technicalities of differential geometry and laborious calculation of derivatives pose a significant barrier to experimenting with manifold optimization methods. (Townsend et al., 2016) `ev:asserted` p. 1 ^townsend2016pymanopt-002
- Pymanopt uses automated differentiation to calculate derivative information, which the authors say saves users time and potential calculation and implementation errors. (Townsend et al., 2016) `ev:asserted` p. 1 ^townsend2016pymanopt-003
- Optimization on manifolds, or [[Riemannian optimization]], minimizes a cost function over a search space that admits the structure of a differentiable manifold. (Townsend et al., 2016) `ev:asserted` p. 1 ^townsend2016pymanopt-004
- Familiar sets that qualify as manifolds include the unit sphere, positive definite matrices, orthogonal matrices and the Grassmann manifold of subspaces. (Townsend et al., 2016) `ev:asserted` p. 1 ^townsend2016pymanopt-005
- The authors use the term automated differentiation to cover both automatic differentiation and symbolic differentiation for the automatic calculation of derivatives. (Townsend et al., 2016) `ev:asserted` p. 1 ^townsend2016pymanopt-006
- Manopt allows the user to pass a function's gradient and Hessian to state of the art solvers that exploit this information over the manifold. (Townsend et al., 2016) `ev:cited` p. 1 ^townsend2016pymanopt-007
- The authors state that working out and implementing gradients and higher order derivatives is laborious and error prone, particularly for matrix or tensor objectives. (Townsend et al., 2016) `ev:asserted` p. 2 ^townsend2016pymanopt-008
- Manopt's Riemannian Trust Regions solver, described by Absil et al., requires second order directional derivatives or a numerical approximation thereof. (Townsend et al., 2016) `ev:cited` p. 2 ^townsend2016pymanopt-009
- Pymanopt supports a variety of modern Python libraries for automated differentiation of cost functions acting on vectors, matrices or higher rank tensors. (Townsend et al., 2016) `ev:reported` p. 2 ^townsend2016pymanopt-010
- The authors state that combining [[Riemannian optimization|manifold optimization]] with automated differentiation enables a rapid prototyping workflow that was previously unavailable to practitioners. (Townsend et al., 2016) `ev:asserted` p. 2 ^townsend2016pymanopt-011
- The authors state that in Pymanopt the Riemannian Trust Regions solver is just as easy to use as derivative-free or first order methods. (Townsend et al., 2016) `ev:asserted` p. 2 ^townsend2016pymanopt-012
- The authors state that [[Riemannian optimization|optimization on manifolds]] is superior to free Euclidean optimization followed by projecting parameters back onto the search space each iteration. (Townsend et al., 2016) `ev:asserted` p. 2 ^townsend2016pymanopt-013
- Hosseini and Sra fit mixture of Gaussian models by optimizing over a product manifold of positive definite covariance matrices as an alternative to EM. (Townsend et al., 2016) `ev:cited` p. 2 ^townsend2016pymanopt-014
- The manifold method of Hosseini and Sra is reported to be on par with expectation maximization for mixture of Gaussian parameter inference. (Townsend et al., 2016) `ev:cited` p. 2 ^townsend2016pymanopt-015
- The manifold method of Hosseini and Sra is reported to show less variability in running times than the traditional expectation maximization algorithm. (Townsend et al., 2016) `ev:cited` p. 2 ^townsend2016pymanopt-016
- Further cited applications of manifold optimization include matrix completion, robust PCA, dimension reduction for ICA, kernel ICA and similarity learning. (Townsend et al., 2016) `ev:cited` p. 2 ^townsend2016pymanopt-017
- At the time of writing, a search for manifold optimization on the IEEE Xplore Digital Library listed 1065 results. (Townsend et al., 2016) `ev:reported` p. 2 ^townsend2016pymanopt-018
- At the time of writing, the Manopt toolbox itself was referenced in 90 papers indexed by Google Scholar. (Townsend et al., 2016) `ev:reported` p. 2 ^townsend2016pymanopt-019
- Pymanopt is written in Python and uses NumPy and SciPy for its computation and linear algebra operations. (Townsend et al., 2016) `ev:reported` p. 2 ^townsend2016pymanopt-020
- At the time of writing, Pymanopt is compatible with cost functions defined using the Autograd, Theano or TensorFlow libraries. (Townsend et al., 2016) `ev:reported` p. 2 ^townsend2016pymanopt-021
- Pymanopt itself and all of its required software are open source, with no dependence on any proprietary software. (Townsend et al., 2016) `ev:reported` p. 2 ^townsend2016pymanopt-022
- Theano calculates derivatives using symbolic differentiation combined with rule-based optimizations, whereas Autograd and TensorFlow use reverse-mode automatic differentiation. (Townsend et al., 2016) `ev:reported` p. 2 ^townsend2016pymanopt-023
- Much of the structure of Pymanopt is based on that of the Manopt Matlab toolbox, according to its authors. (Townsend et al., 2016) `ev:reported` p. 3 ^townsend2016pymanopt-024
- For this early release, the authors implemented all of the solvers and a number of the manifolds found in Manopt. (Townsend et al., 2016) `ev:reported` p. 3 ^townsend2016pymanopt-025
- The authors plan to implement more of Manopt's functionality in later releases, based on the needs of users. (Townsend et al., 2016) `ev:asserted` p. 3 ^townsend2016pymanopt-026
- The codebase is modular and thoroughly commented to make extension to further solvers, manifolds or differentiation backends as straightforward as possible. (Townsend et al., 2016) `ev:reported` p. 3 ^townsend2016pymanopt-027
- Both user and developer documentation are available for Pymanopt, alongside a GitHub repository for raising issues and requesting features. (Townsend et al., 2016) `ev:reported` p. 3 ^townsend2016pymanopt-028
- All automated differentiation in Pymanopt is performed behind the scenes, so the amount of setup code required from the user is minimal. (Townsend et al., 2016) `ev:reported` p. 3 ^townsend2016pymanopt-029
- Usually a user only needs to instantiate a manifold, define a cost function on it, and instantiate a Pymanopt solver. (Townsend et al., 2016) `ev:reported` p. 3 ^townsend2016pymanopt-030
- The worked example seeks a rank k positive semi-definite matrix that best approximates a given symmetric matrix under a pseudo-Huber loss. (Townsend et al., 2016) `ev:reported` p. 3 ^townsend2016pymanopt-031
- In the example, points on the fixed-rank PSD manifold are parameterized as Y times its transpose, with Y an n by k matrix. (Townsend et al., 2016) `ev:reported` p. 3 ^townsend2016pymanopt-032
- In the example code, the cost function is written with autograd.numpy and uses a pseudo-Huber parameter delta of .5. (Townsend et al., 2016) `ev:reported` p. 3 ^townsend2016pymanopt-033
- The example wraps the manifold and cost in a Pymanopt Problem object and solves it with the TrustRegions solver. (Townsend et al., 2016) `ev:reported` p. 4 ^townsend2016pymanopt-034
- The toolbox examples folder includes inference in mixture of Gaussian models using manifold optimization instead of the expectation maximization algorithm. (Townsend et al., 2016) `ev:reported` p. 4 ^townsend2016pymanopt-035
- The authors state that Pymanopt lets users experiment with different state of the art manifold solvers, like Riemannian Trust Regions, without extra effort. (Townsend et al., 2016) `ev:asserted` p. 4 ^townsend2016pymanopt-036
- Changing the cost to the Frobenius norm, a p-norm or a more complex function requires just a small change in the cost definition. (Townsend et al., 2016) `ev:asserted` p. 4 ^townsend2016pymanopt-037
- For problems of greater complexity, the authors argue Pymanopt offers a significant advantage over toolboxes that require manual differentiation. (Townsend et al., 2016) `ev:asserted` p. 4 ^townsend2016pymanopt-038
- According to the authors, gradients and Hessians only need to be derived if they are required for other analysis of a problem. (Townsend et al., 2016) `ev:asserted` p. 4 ^townsend2016pymanopt-039
- The authors believe these advantages, with potential extension to large-scale applications using TensorFlow, could lead to significant progress in manifold optimization applications. (Townsend et al., 2016) `ev:asserted` p. 4 ^townsend2016pymanopt-040

## 🎯 Contributions

## 📖 Glossary

- **Riemannian optimization** — Optimization of a cost function over a smooth search space forming a differentiable manifold.
- **Automated differentiation** — Umbrella term here for automatic and symbolic calculation of derivatives by software.
- **Reverse-mode automatic differentiation** — Computes gradients by propagating derivatives backward through the recorded computation, as in Autograd and TensorFlow.
- **Symbolic differentiation** — Derives derivative expressions from the symbolic form of a function, as in Theano.
- **Riemannian Trust Regions** — Second-order manifold solver needing directional second derivatives or an approximation of them.
- **Grassmann manifold** — Set of p-dimensional linear subspaces of an n-dimensional Euclidean space.
- **Pseudo-Huber loss** — Smooth robust loss, quadratic near zero and roughly linear for large residuals.
- **Projected gradient descent** — Euclidean step followed by projection of parameters back onto the constraint set.

## ❓ Open questions

- How does Pymanopt's runtime compare with Manopt using hand-coded gradients and Hessians on the same problems?
- What overhead does automated differentiation add to second-order solvers such as Riemannian Trust Regions at large scale?
- Does the suggested TensorFlow-based large-scale extension deliver the progress the authors anticipate?
- Which Manopt manifolds were not yet ported in this early release?

## 📝 Notes on reading

The cached text is arXiv:1603.03236v4 (8 Sep 2016), which carries the JMLR 17 (2016) header, so it matches the published version; the packet identifier is the arXiv record. The paper is a short software description: it reports no benchmark, runtime or accuracy experiment of its own, so no claim is `ev:measured`. The performance comparison with EM is attributed to Hosseini and Sra (2015) and is claimed as cited. The pseudo-Huber loss and PSD manifold definitions on p. 3 were extracted with broken math layout; the claims describe them in words rather than copying the formulas. The code listing spans pp. 3-4.

## Suggested new concepts

- Riemannian optimization — the general method behind Pymanopt and Manopt, likely shared by several robotics and estimation sources in the vault.
- Automatic differentiation — the enabling technique Pymanopt relies on, relevant beyond this paper.
- Riemannian Trust Regions — a named second-order solver that recurs in manifold optimization literature.
- Manopt — the Matlab toolbox Pymanopt ports, cited as the design reference.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Toolbox de variedades con autodiff (A.6).

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
