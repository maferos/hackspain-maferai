---
aliases: []
type: "source"
title: "Geoopt: Riemannian Optimization in PyTorch"
citekey: "Kochurov2020geoopt"
doi: "10.48550/arXiv.2005.02819"
arxiv: "2005.02819"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2005.02819"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Max Kochurov", "Rasul Karimov", "Serge Kozlukov"]
sha256: ["39746ffed2db3524c72fb3bf5ad0277acf35bfddd4170c46e967e7418138dd2d"]
pdf: "Content/Papers/Kochurov2020geoopt.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Kochurov2020geoopt.pdf]]

> [!abstract] One-sentence summary
> The paper describes Geoopt, a PyTorch library whose Manifold interface and Riemannian SGD/Adam optimizers let geometric deep learning models train manifold-valued parameters as drop-in replacements for standard PyTorch optimization.

## Abstract

Geoopt is a research-oriented modular open-source package for Riemannian Optimization in PyTorch. The core of Geoopt is a standard Manifold interface that allows for the generic implementation of optimization algorithms. Geoopt supports basic Riemannian SGD as well as adaptive optimization algorithms. Geoopt also provides several algorithms and arithmetic methods for supported manifolds, which allow composing geometry-aware neural network layers that can be integrated with existing models. (arXiv)

## 🧠 Key ideas (atomic)

- Geoopt is a research-oriented modular open-source package for [[Riemannian optimization]] built on top of the PyTorch dynamic computation graph backend. (Kochurov et al., 2020) `ev:asserted` p. 1 ^kochurov2020geoopt-001
- Building on PyTorch lets Geoopt use auto-differentiation, GPU acceleration and model export such as ONNX for geometric deep learning. (Kochurov et al., 2020) `ev:asserted` p. 1 ^kochurov2020geoopt-002
- Geoopt optimizers implement the interface of native PyTorch optimizers, serving as a drop-in replacement for them during training. (Kochurov et al., 2020) `ev:asserted` p. 1 ^kochurov2020geoopt-003
- The only difference from standard PyTorch training is how parameters are declared, with manifold parameters created through geoopt.Parameter. (Kochurov et al., 2020) `ev:asserted` p. 1 ^kochurov2020geoopt-004
- All native PyTorch tensors handed to Geoopt optimizers are treated by those optimizers as regular Euclidean parameters. (Kochurov et al., 2020) `ev:reported` p. 1 ^kochurov2020geoopt-005
- Work on the package is mostly motivated by experiments with hyperbolic embeddings and hyperbolic neural networks, according to the authors. (Kochurov et al., 2020) `ev:asserted` p. 1 ^kochurov2020geoopt-006
- Geoopt provides several models of hyperbolic space, including the Poincaré ball model, the Hyperboloid model and a κ-Stereographic model. (Kochurov et al., 2020) `ev:reported` p. 1 ^kochurov2020geoopt-007
- The general κ-Stereographic model generalizes hyperbolic, Euclidean and spherical geometries within one model, following Bachmann et al. (Kochurov et al., 2020) `ev:cited` p. 1 ^kochurov2020geoopt-008
- A Figure 1 example declares a 10 by 10 Stiefel manifold parameter and optimizes it with RiemannianAdam. (Kochurov et al., 2020) `ev:reported` p. 1 ^kochurov2020geoopt-009
- The Riemannian gradient descent update moves the point along the [[Exponential map|exponential map]] of the negative learning-rate-scaled ascent direction. (Kochurov et al., 2020) `ev:asserted` p. 1 ^kochurov2020geoopt-010
- In Geoopt, points and directions are represented numerically through embeddings of manifolds into ambient vector spaces, often the identity map. (Kochurov et al., 2020) `ev:reported` p. 2 ^kochurov2020geoopt-011
- Geoopt obtains the Euclidean derivative of the objective, defined in ambient space, with PyTorch's backward operation. (Kochurov et al., 2020) `ev:reported` p. 2 ^kochurov2020geoopt-012
- A single Geoopt operation, egrad2rgrad, converts the Euclidean derivative into the Riemannian ascent direction on the manifold using the inner product. (Kochurov et al., 2020) `ev:reported` p. 2 ^kochurov2020geoopt-013
- The authors state that designing a general-purpose manifold optimization package accounting for possible use-cases may not be a tractable problem. (Kochurov et al., 2020) `ev:asserted` p. 2 ^kochurov2020geoopt-014
- Geoopt is specifically concerned with geometric deep learning research, with development guided by a couple of rather pragmatic principles. (Kochurov et al., 2020) `ev:asserted` p. 2 ^kochurov2020geoopt-015
- The first design principle is smooth integration with the PyTorch ecosystem, including compatibility with third-party experiment management systems built on PyTorch. (Kochurov et al., 2020) `ev:asserted` p. 2 ^kochurov2020geoopt-016
- A second design principle is support for broadcasting in all operations, together with broadcasting semantics for product manifolds. (Kochurov et al., 2020) `ev:asserted` p. 2 ^kochurov2020geoopt-017
- The authors note that Poincaré disk and Lorentz models have unbounded numerical error as points get far from the origin. (Kochurov et al., 2020) `ev:asserted` p. 2 ^kochurov2020geoopt-018
- Whenever possible, algorithms in Geoopt are implemented to work even with float32 precision, as part of a robustness principle. (Kochurov et al., 2020) `ev:asserted` p. 2 ^kochurov2020geoopt-019
- The instabilities of specific Geoopt functions are described appropriately in the package documentation, under the robustness and numerical stability principle. (Kochurov et al., 2020) `ev:asserted` p. 2 ^kochurov2020geoopt-020
- Efficiency and extendibility come after integration, broadcasting and robustness, which the authors describe as concerned with not getting in the way. (Kochurov et al., 2020) `ev:asserted` p. 2 ^kochurov2020geoopt-021
- The basic primitive of Geoopt is ManifoldTensor, a multi-dimensional array that stores a reference to its containing Manifold. (Kochurov et al., 2020) `ev:reported` p. 2 ^kochurov2020geoopt-022
- ManifoldTensor inherits from torch.Tensor and torch.nn.Parameter to ensure compatibility with the rest of the PyTorch ecosystem. (Kochurov et al., 2020) `ev:asserted` p. 2 ^kochurov2020geoopt-023
- By convention, simple product manifolds in Geoopt are implemented with broadcasting along the first dimensions of the array. (Kochurov et al., 2020) `ev:reported` p. 2 ^kochurov2020geoopt-024
- More complex product manifold cases in Geoopt are handled by the geoopt.ProductManifold class instead of the simple broadcasting convention. (Kochurov et al., 2020) `ev:reported` p. 2 ^kochurov2020geoopt-025
- Efficient [[Riemannian optimization]] in Geoopt requires update-step optimizations such as merging retractions followed by parallel transport. (Kochurov et al., 2020) `ev:asserted` p. 2 ^kochurov2020geoopt-026
- In product manifolds, Geoopt computes the adaptive term per manifold parameter, exploiting product structure as in Bécigneul and Ganea. (Kochurov et al., 2020) `ev:reported` p. 2 ^kochurov2020geoopt-027
- Because geoopt.Manifold inherits from torch.nn.Module, a manifold is captured by state dict and its own parameters can be optimized for. (Kochurov et al., 2020) `ev:reported` p. 2 ^kochurov2020geoopt-028
- The minimal method set of a Manifold subclass comprises retraction, vector transport, inner product and the egrad2rgrad conversion. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-029
- Geoopt uses retraction as a first-order approximation of the [[Exponential map|exponential map]] during optimization, often keeping a separate expmap method. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-030
- For some manifolds, Geoopt provides variants that perform the [[Exponential map|actual exponential map]] instead of retraction during optimization. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-031
- Vector transport in Geoopt maps tangent vectors at source points to tangent vectors at target points, approximating parallel transport to first order. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-032
- Points and tangent vectors in Geoopt are always represented by coordinates in the assumed ambient vector space of the manifold. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-033
- For PoincareBall, the embedding coincides with the natural global chart, which the authors attribute to negative curvature and conformality of the model. (Kochurov et al., 2020) `ev:asserted` p. 3 ^kochurov2020geoopt-034
- On a sphere, Geoopt takes the extrinsic approach of assuming an ambient vector space instead of using local charts. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-035
- The authors acknowledge the ambient-coordinate representation is somewhat restrictive, complicating tiling-based parameterizations of hyperbolic space by Yu and De Sa. (Kochurov et al., 2020) `ev:asserted` p. 3 ^kochurov2020geoopt-036
- Extending Geoopt requires implementing retraction or exponential map, parallel or vector transport, and making these methods properly broadcastable. (Kochurov et al., 2020) `ev:asserted` p. 3 ^kochurov2020geoopt-037
- The authors state that making new manifold methods properly broadcastable might be the hardest part of extending Geoopt. (Kochurov et al., 2020) `ev:asserted` p. 3 ^kochurov2020geoopt-038
- Geoopt implements the Sphere manifold for unit-norm constrained problems such as embeddings and eigenvalue problems. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-039
- Geoopt implements the Stiefel manifold of matrices with orthonormal columns, intended for basis reconstruction problems. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-040
- Geoopt implements the Birkhoff polytope of doubly stochastic matrices, following Douik and Hassibi, for inferring permutations in data. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-041
- For hyperbolic deep learning, Geoopt offers the Stereographic model and the Lorentz manifold as supported manifolds. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-042
- Product and Scaled manifolds in Geoopt allow combining and extending any of the other supported manifolds. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-043
- Geoopt provides RiemannianAdam, a Riemannian version of the popular Adam optimizer, plus a SparseRiemannianAdam variant supporting sparse gradients. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-044
- Geoopt provides RiemannianSGD with Nesterov momentum, plus a SparseRiemannianSGD variant that supports sparse gradients during optimization. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-045
- Geoopt provides a robust implementation of the Poincaré ball model along with methods for performing supplementary hyperbolic math. (Kochurov et al., 2020) `ev:asserted` p. 3 ^kochurov2020geoopt-046
- Geoopt includes a unified Möbius arithmetic implementation covering negative curvature and the positive-curvature stereographic model of a sphere. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-047
- Derivatives with respect to curvature are supported over the whole domain, including zero curvature, making curvature optimization possible in Geoopt. (Kochurov et al., 2020) `ev:reported` p. 3 ^kochurov2020geoopt-048
- The authors present Geoopt as a general-purpose optimization library for PyTorch, noting that [[Riemannian optimization|manifold optimization]] appears in many applications. (Kochurov et al., 2020) `ev:asserted` p. 4 ^kochurov2020geoopt-049
- Citing Arjovsky et al., the authors note unitary transition matrices keep RNN gradient norms unchanged, helping learn long-range dependencies. (Kochurov et al., 2020) `ev:cited` p. 4 ^kochurov2020geoopt-050
- Stiefel manifold parameterizations used in recurrent networks, following Helfrich et al., also help avoid vanishing or exploding gradients. (Kochurov et al., 2020) `ev:cited` p. 4 ^kochurov2020geoopt-051
- In computer vision, doubly stochastic matrices can be used to match keypoints between views, as shown by Birdal and Simsekli. (Kochurov et al., 2020) `ev:cited` p. 4 ^kochurov2020geoopt-052
- For time series classification, covariance matrices of stationary representations are passed to SPD neural networks, as in cited prior work. (Kochurov et al., 2020) `ev:cited` p. 4 ^kochurov2020geoopt-053
- Riemannian batch normalization for SPD matrices by Brooks et al. further improves time series classification benchmarks and training stability. (Kochurov et al., 2020) `ev:cited` p. 4 ^kochurov2020geoopt-054
- The authors state that Geoopt makes implementing hyperbolic extensions of message passing simpler, as demonstrated by Chami et al. (Kochurov et al., 2020) `ev:cited` p. 4 ^kochurov2020geoopt-055
- An extensible hyperbolic message passing framework may rely on torch geometric, modifying the aggregate method in its MessagePassing class. (Kochurov et al., 2020) `ev:asserted` p. 4 ^kochurov2020geoopt-056
- The authors report Geoopt has helped research in computer vision, navigation, optimal transport, time-series analysis and hyperbolic deep learning. (Kochurov et al., 2020) `ev:cited` p. 4 ^kochurov2020geoopt-057
- Geoopt tries to fill the niche of [[Riemannian optimization]] in PyTorch, which the authors call important for geometric deep learning research. (Kochurov et al., 2020) `ev:asserted` p. 4 ^kochurov2020geoopt-058
- PyManOpt and GeomStats are named as notable Riemannian optimization projects that existed prior to Geoopt. (Kochurov et al., 2020) `ev:cited` p. 4 ^kochurov2020geoopt-059
- The authors state that the main distinction between Geoopt and other [[Riemannian optimization]] solutions is in the interface. (Kochurov et al., 2020) `ev:asserted` p. 4 ^kochurov2020geoopt-060
- PyManOpt is a Python re-implementation of Manopt that closely follows the original interface of solving a Problem built from manifold and cost. (Kochurov et al., 2020) `ev:cited` p. 4 ^kochurov2020geoopt-061
- The authors acknowledge that PyManOpt provides a broader collection of algorithms and manifolds than Geoopt, including trusted region methods and Nelder-Mead. (Kochurov et al., 2020) `ev:asserted` p. 4 ^kochurov2020geoopt-062
- Geomstats is designed around the fit-transform semantics of sklearn, unlike Geoopt's PyTorch-style interfaces for neural networks. (Kochurov et al., 2020) `ev:asserted` p. 4 ^kochurov2020geoopt-063
- Geoopt users define neural networks and cost functions in the usual PyTorch way without constructing a PyManOpt Problem. (Kochurov et al., 2020) `ev:asserted` p. 4 ^kochurov2020geoopt-064
- The authors argue that keeping a PyTorch fork up to date demands a considerable and continuous maintenance effort. (Kochurov et al., 2020) `ev:asserted` p. 4 ^kochurov2020geoopt-065
- According to the authors, using a fork complicates integration with third-party libraries that could pin specific PyTorch versions. (Kochurov et al., 2020) `ev:asserted` p. 4 ^kochurov2020geoopt-066
- Geoopt avoids such infrastructural costs of forking and aims to keep the bar low for both new contributors and users. (Kochurov et al., 2020) `ev:asserted` p. 4 ^kochurov2020geoopt-067

## 🎯 Contributions

## 📖 Glossary

- **Riemannian optimization** — Optimization of an objective whose parameters are constrained to lie on a smooth Riemannian manifold.
- **Tangent space** — Vector space of directions at a manifold point, written TpM.
- **Exponential map** — Operation mapping a tangent vector at a point to the geodesic endpoint it reaches.
- **Retraction** — First-order approximation of the exponential map used in optimization updates.
- **Vector transport** — First-order approximation of parallel transport moving tangent vectors between points.
- **egrad2rgrad** — Geoopt operation converting an ambient Euclidean gradient into a Riemannian gradient on the manifold.
- **Stiefel manifold** — Set of matrices with orthonormal columns, satisfying XᵀX = I.
- **Birkhoff polytope** — Set of doubly stochastic square matrices, with rows and columns summing to one.
- **Poincaré ball** — Conformal model of hyperbolic space inside the unit ball.
- **κ-Stereographic model** — Curvature-parameterized model unifying hyperbolic, Euclidean and spherical geometries.
- **ManifoldTensor** — Geoopt tensor subclass storing a reference to the manifold it lives on.

## ❓ Open questions

- How does Geoopt's runtime and numerical accuracy compare with PyManOpt, Geomstats or McTorch on the same problems?
- How much do the float32-oriented stability measures reduce NaNs far from the origin in the Poincaré and Lorentz models?
- Can tiling-based hyperbolic parameterizations be supported despite the ambient-coordinate representation?
- Does Riemannian Adam with per-manifold adaptive terms converge faster than Riemannian SGD in Geoopt's target applications?

## 📝 Notes on reading

The paper is a short software description with no experiments, benchmarks or quantitative results; every claim is a design, implementation or literature statement. Read from the arXiv version (arXiv:2005.02819v5, 17 Jul 2020). The PDF carries an ICML 2020 proceedings footer with "PMLR 108", while the registry lists it as an arXiv preprint; the footer looks like a template artefact. Figure 1 is a code listing creating a Stiefel parameter optimized with RiemannianAdam; Figure 2 depicts a gradient descent step on the Poincaré disk and could only be described. The update-rule equations on page 1 and the manifold set definitions on page 3 are partly garbled by extraction (braces and symbols lost). Author names with diacritics (Bécigneul, Balažević) are garbled in the text layer.

## Suggested new concepts

- Riemannian optimization — the core technique the library implements, shared with other manifold optimization tools.
- Hyperbolic neural networks — the main motivating application for Geoopt and a distinct research line.
- Retraction and vector transport — first-order approximations central to practical manifold optimizers.
- Riemannian adaptive optimization — Adam-style methods on manifolds, the basis of RiemannianAdam.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — `RiemannianAdam`/`RiemannianSGD` en PyTorch (A.5–A.6).

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
