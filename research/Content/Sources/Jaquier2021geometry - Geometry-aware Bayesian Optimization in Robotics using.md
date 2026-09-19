---
aliases: []
type: "source"
title: "Geometry-aware Bayesian Optimization in Robotics using Riemannian Matérn Kernels"
citekey: "Jaquier2021geometry"
doi: "10.48550/arXiv.2111.01460"
arxiv: "2111.01460"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2111.01460"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Noémie Jaquier", "Viacheslav Borovitskiy", "Andrei Smolensky", "Alexander Terenin", "Tamim Asfour", "Leonel Rozo"]
sha256: ["300c95d15bfc4a4a1f49517af84b55d06c9a35ab32ee59b43a5c487688368753"]
pdf: "Content/Papers/Jaquier2021geometry.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 58
---

📄 PDF: [[Jaquier2021geometry.pdf]]

> [!abstract] One-sentence summary
> The paper derives practical Riemannian Matérn and heat kernels for the torus, spheres, SO(d), hyperbolic space and SPD matrices, extending them to non-compact manifolds through integrals of heat kernels, and shows that geometry-aware Bayesian optimization generally matches or beats Euclidean kernels on benchmarks and simulated robotics tasks.

## Abstract

Bayesian optimization is a data-efficient technique which can be used for control parameter tuning, parametric policy adaptation, and structure design in robotics. Many of these problems require optimization of functions defined on non-Euclidean domains like spheres, rotation groups, or spaces of positive-definite matrices. To do so, one must place a Gaussian process prior, or equivalently define a kernel, on the space of interest. Effective kernels typically reflect the geometry of the spaces they are defined on, but designing them is generally non-trivial. Recent work on the Riemannian Matérn kernels, based on stochastic partial differential equations and spectral theory of the Laplace-Beltrami operator, offers promising avenues towards constructing such geometry-aware kernels. In this paper, we study techniques for implementing these kernels on manifolds of interest in robotics, demonstrate their performance on a set of artificial benchmark functions, and illustrate geometry-aware Bayesian optimization for a variety of robotic applications, covering orientation control, manipulability optimization, and motion planning, while showing its improved performance. (arXiv)

## 🧠 Key ideas (atomic)

- Bayesian optimization is of growing interest in robotics for controller tuning, policy adaptation, and robot design problems. (Jaquier et al., 2021) `ev:cited` p. 1 ^jaquier2021geometry-001
- Three-dimensional rotations in robotics can be viewed as elements of the Lie group SO(3) or of the sphere S3. (Jaquier et al., 2021) `ev:cited` p. 2 ^jaquier2021geometry-002
- Incorporating geometric structure into Bayesian optimization was recently shown to improve performance on several tasks despite a naïve kernel approximation. (Jaquier et al., 2021) `ev:cited` p. 2 ^jaquier2021geometry-003
- The approach formulates a Matérn kernel as an integral of a squared-exponential kernel to define Riemannian Matérn kernels on non-compact manifolds. (Jaquier et al., 2021) `ev:asserted` p. 2 ^jaquier2021geometry-004
- This formulation generalizes the earlier work of Borovitskiy et al., which applies only to compact Riemannian manifolds. (Jaquier et al., 2021) `ev:asserted` p. 2 ^jaquier2021geometry-005
- The paper introduces new Riemannian Matérn kernels for the special orthogonal group, symmetric positive definite matrices, and hyperbolic space. (Jaquier et al., 2021) `ev:asserted` p. 2 ^jaquier2021geometry-006
- The authors state that the general formulation avoids determining valid length scales as required in prior geometry-aware Bayesian optimization work. (Jaquier et al., 2021) `ev:asserted` p. 2 ^jaquier2021geometry-007
- According to the authors, the more general Riemannian Matérn kernel formulation provides theoretical guarantees of positive-definiteness. (Jaquier et al., 2021) `ev:asserted` p. 2 ^jaquier2021geometry-008
- The squared exponential geodesic distance expression is not a valid kernel for all length scales simultaneously on non-Euclidean domains. (Jaquier et al., 2021) `ev:cited` p. 3 ^jaquier2021geometry-009
- The authors build on the Laplace–Beltrami spectral approach because it does not require numerically solving stochastic partial differential equations. (Jaquier et al., 2021) `ev:asserted` p. 3 ^jaquier2021geometry-010
- The acquisition function is optimized at each iteration with trust region methods on Riemannian manifolds as introduced by Absil et al. (Jaquier et al., 2021) `ev:reported` p. 3 ^jaquier2021geometry-011
- When the search space is a subset of a manifold, a constrained trust region algorithm handling linear constraints is employed. (Jaquier et al., 2021) `ev:reported` p. 3 ^jaquier2021geometry-012
- Riemannian Matérn kernels derived from Whittle's stochastic partial differential equations are well-defined for all Riemannian manifolds and hyperparameter values. (Jaquier et al., 2021) `ev:asserted` p. 4 ^jaquier2021geometry-013
- The main difficulty of the SPDE-based definition is its implicit form, which gives no practical expressions for computing the kernel. (Jaquier et al., 2021) `ev:asserted` p. 4 ^jaquier2021geometry-014
- For compact manifolds, Borovitskiy et al. express Matérn kernels as an infinite series over Laplace–Beltrami eigenpairs of the manifold. (Jaquier et al., 2021) `ev:cited` p. 4 ^jaquier2021geometry-015
- In practice, the kernel is computed by calculating eigenpairs analytically or numerically, then truncating the infinite sum. (Jaquier et al., 2021) `ev:reported` p. 4 ^jaquier2021geometry-016
- Numerical eigenpair computation with meshes and finite element methods scales exponentially with manifold dimension, so the paper does not focus on it. (Jaquier et al., 2021) `ev:asserted` p. 4 ^jaquier2021geometry-017
- For non-compact manifolds, Matérn kernels are defined as integrals of squared exponential kernels, also known as heat kernels, over length scales. (Jaquier et al., 2021) `ev:asserted` p. 4 ^jaquier2021geometry-018
- In the Euclidean case, the integral relation follows from writing the Matérn spectral measure, the T distribution, as a gamma mixture of Gaussians. (Jaquier et al., 2021) `ev:computed` p. 4 ^jaquier2021geometry-019
- The integral-defined Matérn kernel is proven positive definite whenever the respective heat kernel is positive definite. (Jaquier et al., 2021) `ev:computed` p. 17 ^jaquier2021geometry-020
- On the torus, Laplace–Beltrami eigenfunctions are the 1-periodic Euclidean Laplacian eigenfunctions: sines and cosines with frequencies that are integer multiples of 2π. (Jaquier et al., 2021) `ev:computed` p. 5 ^jaquier2021geometry-021
- On the d-dimensional sphere, the squared exponential kernel can be written as a function only of the geodesic distance. (Jaquier et al., 2021) `ev:computed` p. 5 ^jaquier2021geometry-022
- The heat kernel for SO(d) is taken from the literature as a sum over highest weights involving characters of irreducible representations. (Jaquier et al., 2021) `ev:cited` p. 18 ^jaquier2021geometry-023
- Hyperbolic space is often used to embed hierarchical data such as trees or graphs, owing to exponential volume growth of balls. (Jaquier et al., 2021) `ev:cited` p. 6 ^jaquier2021geometry-024
- Explicit hyperbolic heat kernel formulas from the literature cover dimensions 2 and 3, with Millson's recurrence formula handling dimensions above 3. (Jaquier et al., 2021) `ev:cited` p. 6 ^jaquier2021geometry-025
- Riemannian structures transferred to SPD matrices through matrix exponential or factor-product maps often poorly capture the geometry of SPD matrices. (Jaquier et al., 2021) `ev:cited` p. 6 ^jaquier2021geometry-026
- Identifying SPD matrices with the quotient GL(d)/O(d) gives a non-compact manifold, hence the method of Borovitskiy et al. does not apply. (Jaquier et al., 2021) `ev:asserted` p. 6 ^jaquier2021geometry-027
- Explicit heat kernel formulas for SPD matrices are available in the literature for dimensions 2 and 3, common in robotics problems. (Jaquier et al., 2021) `ev:cited` p. 6 ^jaquier2021geometry-028
- For dimension 2, Sawyer's SPD heat kernel formula contains a one-dimensional integral that may be evaluated numerically. (Jaquier et al., 2021) `ev:cited` p. 6 ^jaquier2021geometry-029
- A product of Matérn kernels on factor manifolds with separate length scales enables automatic relevance determination in the product Riemannian setting. (Jaquier et al., 2021) `ev:asserted` p. 6 ^jaquier2021geometry-030
- The product of Matérn kernels does not generally coincide with the Matérn kernel on the product manifold, except for infinite smoothness with equal length scales. (Jaquier et al., 2021) `ev:computed` p. 6 ^jaquier2021geometry-031
- All experiments use expected improvement as acquisition function, with each optimization repeated 30 times from 5 random initial samples. (Jaquier et al., 2021) `ev:reported` p. 7 ^jaquier2021geometry-032
- Benchmark test functions are projected onto the manifolds S5, SO(3), the SPD manifold S2++, and the hyperbolic space H3. (Jaquier et al., 2021) `ev:reported` p. 7 ^jaquier2021geometry-033
- For SPD benchmarks, the search domain is restricted to matrices whose eigenvalues lie in the interval [0.001; 5]. (Jaquier et al., 2021) `ev:reported` p. 7 ^jaquier2021geometry-034
- Geometry-aware Bayesian optimization is compared against classical Bayesian optimization with Euclidean kernels using constrained Euclidean acquisition optimization. (Jaquier et al., 2021) `ev:reported` p. 7 ^jaquier2021geometry-035
- On sphere and SPD manifolds, comparisons also include a naïve Riemannian squared exponential kernel that replaces Euclidean distance with geodesic distance. (Jaquier et al., 2021) `ev:reported` p. 7 ^jaquier2021geometry-036
- For SPD matrices, comparisons also include a product kernel on the eigendecomposition and a kernel on vectorized Cholesky factors. (Jaquier et al., 2021) `ev:reported` p. 7 ^jaquier2021geometry-037
- On the benchmark functions, geometry-aware algorithms generally match or outperform their Euclidean counterparts in regret after 200 iterations. (Jaquier et al., 2021) `ev:measured` p. 7 ^jaquier2021geometry-038
- Performance differences are more pronounced in higher dimensions and on manifolds that depart more significantly from the Euclidean setting. (Jaquier et al., 2021) `ev:measured` p. 7 ^jaquier2021geometry-039
- Among the benchmark manifolds, the hyperbolic manifold H3 shows the most pronounced difference between geometry-aware and Euclidean kernels. (Jaquier et al., 2021) `ev:measured` p. 7 ^jaquier2021geometry-040
- Surprisingly, the naïve Riemannian squared exponential kernel, which may become ill-defined for certain length scales, performs competitively in some settings. (Jaquier et al., 2021) `ev:measured` p. 7 ^jaquier2021geometry-041
- The authors suggest this may occur because small length scales keep the naïve kernel out of the problematic regime. (Jaquier et al., 2021) `ev:asserted` p. 7 ^jaquier2021geometry-042
- Geometry-aware Matérn kernels with smoothness 2.5 outperform squared exponential ones on test functions with uneven landscapes, such as Ackley. (Jaquier et al., 2021) `ev:measured` p. 7 ^jaquier2021geometry-043
- Taking geometry into account generally results in faster, more data-efficient convergence with lower variance on the benchmarks. (Jaquier et al., 2021) `ev:measured` p. 7 ^jaquier2021geometry-044
- The authors note that these geometry-aware gains come at the cost of more complex algorithmic implementation. (Jaquier et al., 2021) `ev:asserted` p. 7 ^jaquier2021geometry-045
- In the orientation experiment, Bayesian optimization samples orientation references for a velocity-controlled robot around a prior orientation. (Jaquier et al., 2021) `ev:reported` p. 7 ^jaquier2021geometry-046
- In the manipulability task, an 8-degree-of-freedom planar robot tracks a desired [[Manipulability ellipsoid|manipulability ellipsoid]] in its nullspace during a Cartesian velocity trajectory. (Jaquier et al., 2021) `ev:reported` p. 8 ^jaquier2021geometry-047
- Optimization searches the desired manipulability on S2++ to minimize end-effector jerk with manipulability aligned to the movement direction. (Jaquier et al., 2021) `ev:reported` p. 8 ^jaquier2021geometry-048
- For path planning, a 4-connected grid graph on R2 is embedded into H2 using learned embeddings in the Lorentz model. (Jaquier et al., 2021) `ev:reported` p. 8 ^jaquier2021geometry-049
- The robotics experiments show a moderate performance improvement with geometry-aware Bayesian optimization, mirroring the benchmark results. (Jaquier et al., 2021) `ev:measured` p. 8 ^jaquier2021geometry-050
- The authors note that performance gains may depend on both the manifold geometry and the cost function landscape. (Jaquier et al., 2021) `ev:asserted` p. 8 ^jaquier2021geometry-051
- An additional orientation experiment shows less-pronounced improvements, as low dimensionality may make Euclidean and Riemannian kernels very similar. (Jaquier et al., 2021) `ev:measured` p. 8 ^jaquier2021geometry-052
- The authors conclude that their explicit kernel formulas enable the use of geometry-aware Bayesian optimization in novel settings. (Jaquier et al., 2021) `ev:asserted` p. 8 ^jaquier2021geometry-053
- The orientation cost weights are 1.0 for orientation error, 1e−4 for torques, and 1 for manipulability. (Jaquier et al., 2021) `ev:reported` p. 13 ^jaquier2021geometry-054
- The path planning environment is a 9 × 9 grid with a circle-shaped obstacle of radius 1 centered at (4, 4). (Jaquier et al., 2021) `ev:reported` p. 13 ^jaquier2021geometry-055
- Additional benchmarks show more pronounced geometry-aware gains in higher dimensions, for instance on S5 compared with S3. (Jaquier et al., 2021) `ev:measured` p. 13 ^jaquier2021geometry-056
- Gains are more pronounced in the main orientation experiment than in the additional one, which the authors attribute to its uneven cost landscape. (Jaquier et al., 2021) `ev:measured` p. 14 ^jaquier2021geometry-057
- On connected complete manifolds of bounded geometry, the Riemannian squared exponential kernel coincides with the heat kernel of the manifold. (Jaquier et al., 2021) `ev:cited` p. 15 ^jaquier2021geometry-058

## 🎯 Contributions

## 📖 Glossary

- **Riemannian Matérn kernel** — Matérn kernel defined via SPDEs and Laplace–Beltrami spectra on a Riemannian manifold.
- **Heat kernel** — Fundamental solution of the heat equation; the Riemannian squared exponential kernel.
- **Laplace–Beltrami operator** — Generalization of the Laplacian to functions on Riemannian manifolds.
- **Geodesic distance** — Length of the shortest path between two points along a manifold.
- **SPD manifold** — Space of symmetric positive definite matrices, e.g. stiffness or manipulability ellipsoids.
- **Hyperbolic space** — Complete simply-connected manifold with constant negative curvature −1.
- **Special orthogonal group SO(d)** — Group of d-dimensional rotation matrices with determinant 1.
- **Expected improvement** — Acquisition function scoring candidates by their expected gain over the current best.
- **Riemannian trust region** — Optimization method solving local quadratic subproblems in tangent spaces of a manifold.
- **Automatic relevance determination** — Separate length scale per input factor, learned to weight each factor.

## ❓ Open questions

- How do Riemannian Matérn kernels perform on real robot hardware rather than simulated scenarios?
- Can explicit SPD heat kernels beyond dimension 3 be made tractable for higher-dimensional gain or stiffness matrices?
- How much of the naïve kernel's competitive performance is due to lower numerical error versus small learned length scales?
- How should the truncation level of eigen-series and characters be chosen to balance accuracy and cost?
- Does geometry-aware Bayesian optimization scale to high-dimensional product manifolds such as full robot joint tori?

## 📝 Notes on reading

- Version read: arXiv 2111.01460v2 (18 Mar 2023) of the CoRL 2021 paper; the packet identifier matches this arXiv record.
- Figures 2–5 (log10 regret curves and final-regret distributions) were extracted as garbled axis labels; no per-method regret values were claimed.
- The cost functions for the orientation, manipulability and path-planning tasks and the kernel formulas (1)–(9) were partly garbled in extraction; only their verbal descriptions were claimed.
- The paper gives two different explanations for weaker gains in the additional orientation experiment: low dimensionality (p. 8) and the uneven cost landscape of the main experiment (p. 14).
- The naïve kernel's competitive performance on the additional manipulability experiment is attributed on p. 14 to low dimensionality and small length scales.

## Suggested new concepts

- Geometry-aware Bayesian optimization — recurring framework for optimizing robot parameters on manifolds, shared with earlier Jaquier et al. work.
- Riemannian Matérn kernel — central kernel family for Gaussian processes on manifolds, reused across GP and BO papers.
- Heat kernel on manifolds — the bridge that lets Matérn kernels extend to non-compact spaces.
- Manipulability ellipsoid — robotics quantity living on the SPD manifold, repeatedly used as an optimization target.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — BO en $SO(3)$, esferas, SPD (C.4, F.7 ruta C).

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
