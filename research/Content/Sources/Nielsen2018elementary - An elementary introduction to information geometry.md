---
aliases: []
type: "source"
title: "An elementary introduction to information geometry"
citekey: "Nielsen2018elementary"
doi: "10.48550/arXiv.1808.08271"
arxiv: "1808.08271"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1808.08271"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Frank Nielsen"]
sha256: ["c691923b1b65547561d8f641d5a5762c3d0d8d39ff8724cd5d4b2cae52a62d6f"]
pdf: "Content/Papers/Nielsen2018elementary.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Nielsen2018elementary.pdf]]

> [!abstract] One-sentence summary
> A self-contained survey of the dualistic differential-geometric structures of information manifolds, from conjugate connections to dually flat Bregman geometry, with applications to natural gradient, hypothesis testing and mixture clustering.

## Abstract

In this survey, we describe the fundamental differential-geometric structures of information manifolds, state the fundamental theorem of information geometry, and illustrate some use cases of these information manifolds in information sciences. The exposition is self-contained by concisely introducing the necessary concepts of differential geometry, but proofs are omitted for brevity. (arXiv)

## 🧠 Key ideas (atomic)

- The author defines information sciences as the fields that study communication between noisy or imperfect data and families of postulated models (Nielsen, 2018) `ev:asserted` p. 1 ^nielsen2018elementary-001
- Amari, the founder of modern information geometry, defined it as a method of exploring the world of information by means of modern geometry (Nielsen, 2018) `ev:cited` p. 1 ^nielsen2018elementary-002
- The exposition is self-contained by concisely introducing the necessary differential geometry concepts, but proofs are omitted for brevity (Nielsen, 2018) `ev:abstract` p. none ^nielsen2018elementary-003
- The author states that geometry allows one to study the invariance of figures in a coordinate-free framework (Nielsen, 2018) `ev:asserted` p. 2 ^nielsen2018elementary-004
- On any smooth manifold, the survey defines two independent structures: a metric tensor field and an affine connection (Nielsen, 2018) `ev:asserted` p. 3 ^nielsen2018elementary-005
- An affine connection is a differential operator that defines covariant derivatives, parallel transport of vectors along smooth curves, and geodesics (Nielsen, 2018) `ev:asserted` p. 6 ^nielsen2018elementary-006
- According to the survey, an affine connection defined on a manifold fully characterizes the curvature and torsion of that manifold (Nielsen, 2018) `ev:asserted` p. 6 ^nielsen2018elementary-007
- For a flat connection, parallel transport does not depend on the path, whereas in general parallel transport is path-dependent (Nielsen, 2018) `ev:asserted` p. 8 ^nielsen2018elementary-008
- The fundamental theorem of Riemannian geometry states that a unique torsion-free affine connection compatible with the metric exists, the Levi-Civita connection (Nielsen, 2018) `ev:asserted` p. 10 ^nielsen2018elementary-009
- In information geometry, a pair of conjugate connections coupled to the metric induces a dual parallel transport that preserves the metric (Nielsen, 2018) `ev:asserted` p. 10 ^nielsen2018elementary-010
- The Riemannian geodesic distance is usually not available in closed form and needs to be approximated or bounded (Nielsen, 2018) `ev:asserted` p. 10 ^nielsen2018elementary-011
- The mean of two conjugate connections is self-conjugate and coincides with the Levi-Civita metric connection (Nielsen, 2018) `ev:asserted` p. 12 ^nielsen2018elementary-012
- Lauritzen introduced statistical manifolds in 1987, a purely geometric construction that may be used outside the field of statistics (Nielsen, 2018) `ev:cited` p. 12 ^nielsen2018elementary-013
- From any pair of conjugate connections, a one-parameter family of alpha-connections can be built, with alpha zero giving the Levi-Civita connection (Nielsen, 2018) `ev:asserted` p. 13 ^nielsen2018elementary-014
- The fundamental theorem of information geometry states that a torsion-free connection of constant curvature has a conjugate with the same constant curvature (Nielsen, 2018) `ev:cited` p. 13 ^nielsen2018elementary-015
- As a corollary, a manifold with conjugate connections is flat for one connection if and only if it is flat for the dual (Nielsen, 2018) `ev:cited` p. 13 ^nielsen2018elementary-016
- Following Eguchi's 1983 construction, a conjugate connection manifold can be defined from any given divergence (Nielsen, 2018) `ev:cited` p. 14 ^nielsen2018elementary-017
- The survey states that self-conjugate connections are obtained when the divergence used to build them is symmetric (Nielsen, 2018) `ev:asserted` p. 11 ^nielsen2018elementary-018
- In the Bregman-induced structure, all Christoffel coefficients of the primal connection vanish, so the information manifold is flat for that connection (Nielsen, 2018) `ev:asserted` p. 15 ^nielsen2018elementary-019
- A dually flat manifold has two global affine coordinate systems related by Legendre-Fenchel transformation, so it can be covered by a single chart (Nielsen, 2018) `ev:asserted` p. 15 ^nielsen2018elementary-020
- The survey counts in general 8 types of geodesic triangles in a dually flat manifold, using primal or dual geodesics (Nielsen, 2018) `ev:asserted` p. 15 ^nielsen2018elementary-021
- Dually flat spaces satisfy dual Pythagorean theorems, in which the divergence adds up along orthogonal primal and dual geodesics (Nielsen, 2018) `ev:cited` p. 16 ^nielsen2018elementary-022
- A divergence-minimizing projection onto a submanifold is unique when the submanifold is flat with respect to the dual connection (Nielsen, 2018) `ev:asserted` p. 16 ^nielsen2018elementary-023
- Kurose reported a Pythagorean theorem for dually constant curvature manifolds that generalizes the Pythagorean theorems of dually flat spaces (Nielsen, 2018) `ev:cited` p. 17 ^nielsen2018elementary-024
- In general, a dually flat space can be built from any smooth strictly convex generator function, according to the survey (Nielsen, 2018) `ev:asserted` p. 17 ^nielsen2018elementary-025
- [[Fisher information matrix|The Fisher information matrix]] is invariant by reparameterization of the sample space, according to the survey citing a textbook (Nielsen, 2018) `ev:cited` p. 19 ^nielsen2018elementary-026
- For any unbiased estimator, the Cramér-Rao lower bound limits the estimator variance from below by the inverse Fisher information divided by sample size (Nielsen, 2018) `ev:cited` p. 19 ^nielsen2018elementary-027
- To visualize the Cramér-Rao bound, the survey repeats 200 runs of maximum likelihood estimation on 100 iid normal samples per grid location (Nielsen, 2018) `ev:computed` p. 19 ^nielsen2018elementary-028
- In the visualization, the centers of the maximum likelihood sample covariance ellipses deviate from the grid locations of the true parameters (Nielsen, 2018) `ev:computed` p. 21 ^nielsen2018elementary-029
- [[Fisher information matrix|The Fisher information matrix]] of an exponential family equals the covariance of its sufficient statistic and the Hessian of the cumulant function (Nielsen, 2018) `ev:asserted` p. 21 ^nielsen2018elementary-030
- The survey notes that the probability simplex of discrete distributions can be modeled either as an exponential family or a mixture family (Nielsen, 2018) `ev:cited` p. 22 ^nielsen2018elementary-031
- Exponential and mixture families equipped with the dual exponential and mixture connections yield dually flat manifolds, since their Christoffel symbols vanish (Nielsen, 2018) `ev:asserted` p. 22 ^nielsen2018elementary-032
- [[Fisher information matrix|The Fisher information metric]] is the unique invariant metric tensor under Markov embeddings, up to a scaling constant (Nielsen, 2018) `ev:cited` p. 23 ^nielsen2018elementary-033
- When the dimension exceeds one, f-divergences are the only invariant and decomposable divergences, as stated in the survey (Nielsen, 2018) `ev:cited` p. 23 ^nielsen2018elementary-034
- By Csiszár's theorem, for alpha between minus one and one, the alpha-topology is equivalent to the total variation topology (Nielsen, 2018) `ev:cited` p. 24 ^nielsen2018elementary-035
- The f-divergences are invariant under diffeomorphisms of the sample space, illustrated with exponential distributions mapped to Rayleigh distributions by square roots (Nielsen, 2018) `ev:asserted` p. 25 ^nielsen2018elementary-036
- The connections induced by invariant standard f-divergences are precisely the expected alpha-connections, with alpha determined by the generator's third derivative at one (Nielsen, 2018) `ev:asserted` p. 25 ^nielsen2018elementary-037
- The curvature of an expected alpha-connection depends both on alpha and on the statistical model considered (Nielsen, 2018) `ev:cited` p. 25 ^nielsen2018elementary-038
- According to the survey, the Fisher-Riemannian manifold of categorical distributions amounts to spherical geometry, a spherical manifold (Nielsen, 2018) `ev:cited` p. 26 ^nielsen2018elementary-039
- Hotelling first proposed the Riemannian geometric structure on parametric probability families in a handwritten note of 1929 (Nielsen, 2018) `ev:cited` p. 26 ^nielsen2018elementary-040
- C. R. Rao independently proposed the same Riemannian modeling of parametric probability families later, in his 1945 paper (Nielsen, 2018) `ev:cited` p. 26 ^nielsen2018elementary-041
- Jeffreys proposed in 1946 to use the volume element of the manifold as an invariant prior, now called the Jeffreys prior (Nielsen, 2018) `ev:cited` p. 26 ^nielsen2018elementary-042
- Using alpha-representations of densities, the survey shows that the alpha-representation of the Fisher information matrix is independent of alpha (Nielsen, 2018) `ev:computed` p. 27 ^nielsen2018elementary-043
- According to the survey, the only [[Bregman divergence|symmetric Bregman divergences]] are squared Mahalanobis distances, which are defined by positive-definite matrices (Nielsen, 2018) `ev:cited` p. 28 ^nielsen2018elementary-044
- The canonical divergence induced by the log-normalizer of an exponential family is shown to recover the reverse Kullback-Leibler divergence (Nielsen, 2018) `ev:computed` p. 29 ^nielsen2018elementary-045
- The dually flat geometry from the Shannon negentropy of a mixture family is shown to induce the forward Kullback-Leibler divergence (Nielsen, 2018) `ev:computed` p. 31 ^nielsen2018elementary-046
- Ordinary gradient descent depends on the parameterization of the function, so two parameterizations may reach different stationary points (Nielsen, 2018) `ev:asserted` p. 33 ^nielsen2018elementary-047
- [[Natural gradient descent]] is recovered from Riemannian gradient descent using a first-order Taylor retraction of the exponential map (Nielsen, 2018) `ev:cited` p. 34 ^nielsen2018elementary-048
- The [[Natural gradient descent|natural gradient]] is invariant under an invertible smooth change of parameterization, according to the survey (Nielsen, 2018) `ev:asserted` p. 34 ^nielsen2018elementary-049
- [[Mirror descent|Bregman mirror descent]] on a Hessian manifold is equivalent to natural gradient descent on the dual Hessian manifold (Nielsen, 2018) `ev:cited` p. 35 ^nielsen2018elementary-050
- In a dually flat space, the natural gradient amounts to the ordinary gradient on the dually parameterized loss function (Nielsen, 2018) `ev:cited` p. 35 ^nielsen2018elementary-051
- Natural evolution strategies relax black-box minimization by minimizing the expected objective under a parametric search distribution (Nielsen, 2018) `ev:cited` p. 35 ^nielsen2018elementary-052
- For exponential and mixture families with the Kullback-Leibler divergence, primal and dual geodesics are straight lines in global affine coordinates (Nielsen, 2018) `ev:asserted` p. 36 ^nielsen2018elementary-053
- The Chernoff information between two distributions of the same exponential family amounts to a [[Bregman divergence]] at the optimal exponent (Nielsen, 2018) `ev:cited` p. 37 ^nielsen2018elementary-054
- The best error exponent distribution is characterized as the intersection of the exponential geodesic with the mixture bisector (Nielsen, 2018) `ev:cited` p. 37 ^nielsen2018elementary-055
- The Kullback-Leibler divergence between two mixtures with prescribed components is equivalent to a [[Bregman divergence]] for the negative differential entropy (Nielsen, 2018) `ev:cited` p. 39 ^nielsen2018elementary-056
- Because the mixture negentropy lacks a closed form, the survey approximates it with Monte Carlo generators, building tractable dually flat manifolds (Nielsen, 2018) `ev:asserted` p. 39 ^nielsen2018elementary-057
- For any symmetric divergence such as the squared Hellinger divergence, the induced conjugate connections coincide with the Levi-Civita connection (Nielsen, 2018) `ev:asserted` p. 40 ^nielsen2018elementary-058
- The survey states that a Riemannian metric distance is never a divergence because rooted distance functions fail to be smooth at extremities (Nielsen, 2018) `ev:asserted` p. 40 ^nielsen2018elementary-059
- Unlike the hyperbolic Fisher-Rao manifold of location-scale families, the Wasserstein manifold of location-scale families has positive curvature (Nielsen, 2018) `ev:cited` p. 41 ^nielsen2018elementary-060
- Amari coined the term information geometry in the preface of his 1985 monograph on differential-geometrical methods in statistics (Nielsen, 2018) `ev:cited` p. 42 ^nielsen2018elementary-061
- The survey did not report the metric, Christoffel and skewness coefficients of the expected alpha-geometry for common parametric models (Nielsen, 2018) `ev:asserted` p. 42 ^nielsen2018elementary-062
- Since an information manifold can be built from any divergence, the author considers generic, ideally axiomatized classes of divergences important (Nielsen, 2018) `ev:asserted` p. 42 ^nielsen2018elementary-063
- This survey is based on the keynote talk given at the 2018 Geometry In Machine Learning workshop, GiMLi (Nielsen, 2018) `ev:reported` p. 44 ^nielsen2018elementary-064
- Monte Carlo estimation of the Kullback-Leibler divergence may produce negative values, since sampled densities do not sum to one (Nielsen, 2018) `ev:asserted` p. 44 ^nielsen2018elementary-065
- The survey proposes estimating extended f-divergences, whose integrand is a [[Bregman divergence|scalar Bregman divergence]], so the Monte Carlo estimates remain non-negative (Nielsen, 2018) `ev:asserted` p. 45 ^nielsen2018elementary-066
- The Kullback-Leibler divergence between two Gaussians with equal covariance equals half the squared Mahalanobis distance for the precision matrix (Nielsen, 2018) `ev:computed` p. 47 ^nielsen2018elementary-067

## 🎯 Contributions

## 📖 Glossary

- **Information manifold** — a manifold with a metric tensor and a pair of conjugate connections.
- **Affine connection** — differential operator defining covariant derivatives, parallel transport and geodesics on a manifold.
- **Conjugate connections** — pair of connections whose dual parallel transport preserves the metric.
- **Levi-Civita connection** — the unique torsion-free connection compatible with a given metric.
- **Amari-Chentsov tensor** — totally symmetric cubic tensor, the difference of conjugate Christoffel symbols.
- **Statistical manifold** — manifold equipped with a metric tensor and a totally symmetric cubic tensor.
- **Dually flat manifold** — manifold flat for both conjugate connections, induced by a Bregman generator.
- **Bregman divergence** — divergence built from a strictly convex potential function and its gradient.
- **Fisher information metric** — Riemannian metric given by the Fisher information matrix of a parametric family.
- **f-divergence** — separable statistical divergence defined by a convex generator f with f(1)=0.
- **Fisher-Rao distance** — geodesic length distance of the Fisher-Riemannian manifold.
- **Natural gradient** — gradient premultiplied by the inverse metric, giving the Riemannian steepest descent direction.
- **Chernoff information** — best error exponent of Bayesian binary hypothesis testing.
- **Mixture family** — convex combinations of prescribed component distributions.

## ❓ Open questions

- Which generic, axiomatized classes of divergences best suit applications, given that any divergence induces an information manifold?
- How to compute or tightly bound Fisher-Rao distances when geodesics have no closed form?
- How fast do Monte Carlo dually flat approximations of mixture manifolds converge in practice?
- How do the dualistic structures extend to non-parametric and quantum information geometry?

## 📝 Notes on reading

Read the arXiv v2 (6 Sep 2020) PDF; it cites works from 2019 and 2020 although the registry year is 2018. The paper is a survey; most claims are theorems or statements attributed to cited work, with proofs omitted. Figures 8, 14 and 15 are small numerical illustrations (Cramér-Rao ellipses, a three-component mixture family, w-GMM clustering) described but not quantified. Many equations are garbled in the extracted text (fractions, sub/superscripts, matrices), e.g. the Fisher information matrices in eqs. 83-92 and the determinant test in eq. 71; no numeric claims were taken from them. Eq. 20 as extracted reads ∇X∇Y X rather than ∇X∇Y Z, likely a typo in the source. Figure 10 (overview of information manifold types) and Figure 16 (classes of divergences) are diagrams only described here.

## Suggested new concepts

- Dually flat manifold — central structure linking Bregman divergences, exponential families and mixture families across many applications.
- Conjugate connections — the core dualistic idea separating information geometry from Riemannian geometry.
- Fisher information metric — unique invariant metric, basis of Fisher-Rao distance, natural gradient and Cramér-Rao bound.
- Natural gradient — parameterization-invariant optimization method with links to mirror descent.
- Bregman divergence — canonical divergence of dually flat spaces used in clustering and projections.
- f-divergence — unique class of separable invariant divergences, including KL, Hellinger and total variation.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Introducción autocontenida a la geometría de la información.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
