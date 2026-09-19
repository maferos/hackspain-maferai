---
aliases: []
type: "source"
title: "Natural gradient via optimal transport"
citekey: "Li2018natural"
doi: "10.48550/arXiv.1803.07033"
arxiv: "1803.07033"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1803.07033"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Wuchen Li", "Guido Montufar"]
sha256: ["c3a8c7d411e5d5cf82700a88f11148ea057cff8d11dc8c4dc6d95f0fc0ef75db"]
pdf: "Content/Papers/Li2018natural.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Li2018natural.pdf]]

> [!abstract] One-sentence summary
> The paper pulls back the discrete L2-Wasserstein Riemannian metric to the parameter space of statistical models, defining a Wasserstein natural gradient that, unlike Fisher-Rao, uses a ground metric on sample space, and tests it on toy flows and maximum likelihood estimation.

## Abstract

We study a natural Wasserstein gradient flow on manifolds of probability distributions with discrete sample spaces. We derive the Riemannian structure for the probability simplex from the dynamical formulation of the Wasserstein distance on a weighted graph. We pull back the geometric structure to the parameter space of any given probability model, which allows us to define a natural gradient flow there. In contrast to the natural Fisher-Rao gradient, the natural Wasserstein gradient incorporates a ground metric on sample space. We illustrate the analysis of elementary exponential family examples and demonstrate an application of the Wasserstein natural gradient to maximum likelihood estimation. (arXiv)

## 🧠 Key ideas (atomic)

- The paper introduces a [[Wasserstein natural gradient]] flow on the parameter space of probability models with discrete sample spaces. (Li & Montufar, 2018) `ev:asserted` p. 2 ^li2018natural-001
- Chentsov's classic result characterizes the [[Fisher information matrix|Fisher-Rao metric]] as the only one, up to scaling, invariant under natural embeddings by Markov morphisms. (Li & Montufar, 2018) `ev:cited` p. 1 ^li2018natural-002
- Static and dynamic optimal transport formulations, equivalent on continuous state spaces, lead to different metrics on the simplex of discrete probability distributions. (Li & Montufar, 2018) `ev:cited` p. 2 ^li2018natural-003
- The authors attribute this difference to the discrete sample space not being a length space, with no continuous path between two nodes. (Li & Montufar, 2018) `ev:asserted` p. 6 ^li2018natural-004
- For the static linear programming formulation, the authors state there is no Riemannian metric tensor on the discrete probability simplex. (Li & Montufar, 2018) `ev:cited` p. 2 ^li2018natural-005
- Earlier work connecting optimal transport and information geometry focused on the distance function induced by linear programming on discrete sample spaces. (Li & Montufar, 2018) `ev:cited` p. 2 ^li2018natural-006
- Other works studied the Gaussian family with the L2-Wasserstein metric, where the corresponding density submanifold is totally geodesic. (Li & Montufar, 2018) `ev:cited` p. 2 ^li2018natural-007
- The authors state that their discussion applies to arbitrary parametric models, in contrast to the earlier works on the Gaussian family. (Li & Montufar, 2018) `ev:asserted` p. 2 ^li2018natural-008
- The ground metric on the discrete sample space is encoded as a weighted graph whose edge weights equal the inverse squared ground distance. (Li & Montufar, 2018) `ev:asserted` p. 5 ^li2018natural-009
- The discrete Wasserstein distance is defined through a dynamical variational problem constrained by a discrete continuity equation on the weighted graph. (Li & Montufar, 2018) `ev:asserted` p. 6 ^li2018natural-010
- The probability weight assigned to each graph edge in the discrete kinetic energy is the average of its two endpoint probabilities. (Li & Montufar, 2018) `ev:asserted` p. 6 ^li2018natural-011
- In primal coordinates, the Wasserstein inner product on the simplex interior is given by the pseudo-inverse of a linear weighted Laplacian matrix. (Li & Montufar, 2018) `ev:asserted` p. 8 ^li2018natural-012
- The authors name the simplex with this metric the Wasserstein statistical manifold, avoiding the term discrete density manifold to prevent confusion. (Li & Montufar, 2018) `ev:asserted` p. 8 ^li2018natural-013
- The metric on the parameter space is defined as the [[Pullback metric|pull-back of the Wasserstein metric]], making the parametrization an isometric embedding. (Li & Montufar, 2018) `ev:asserted` p. 9 ^li2018natural-014
- The parametrization is assumed to have a Jacobi matrix of full rank d, so that the map is locally injective. (Li & Montufar, 2018) `ev:reported` p. 9 ^li2018natural-015
- Lemma 6 shows that the pulled-back metric is positive definite and smooth, so the parameter space is a smooth Riemannian manifold. (Li & Montufar, 2018) `ev:computed` p. 9 ^li2018natural-016
- The authors derive a cotangent geodesic flow on parameter space, calling its two equations the continuity equation and the Hamilton-Jacobi equation. (Li & Montufar, 2018) `ev:computed` p. 10 ^li2018natural-017
- Theorem 7 gives the Wasserstein gradient flow on parameter space as the negative inverse metric tensor applied to the Euclidean parameter gradient. (Li & Montufar, 2018) `ev:computed` p. 11 ^li2018natural-018
- When the parametrization is the identity map, the flow on parameter space reduces to the Wasserstein gradient flow on the discrete probability simplex. (Li & Montufar, 2018) `ev:computed` p. 11 ^li2018natural-019
- The [[Wasserstein natural gradient]] is derived as the steepest descent direction under a constraint on a second order approximation of the Wasserstein distance. (Li & Montufar, 2018) `ev:computed` p. 11 ^li2018natural-020
- The proposed definition replaces the Kullback-Leibler divergence constraint of the standard [[Natural gradient descent|Fisher-Rao natural gradient]] with the Wasserstein distance. (Li & Montufar, 2018) `ev:asserted` p. 12 ^li2018natural-021
- The Wasserstein structure also provides a Hessian operator on parameter space, which the authors use to define displacement convexity there. (Li & Montufar, 2018) `ev:asserted` p. 12 ^li2018natural-022
- Remark 3 relates the displacement convexity of the KL divergence to a Ricci curvature lower bound on sample space. (Li & Montufar, 2018) `ev:cited` p. 12 ^li2018natural-023
- Theorem 9 characterizes λ-convexity of a linear potential on a compact parameter space through an inequality involving discrete Bakry-Emery Gamma operators. (Li & Montufar, 2018) `ev:computed` p. 13 ^li2018natural-024
- For the identity parametrization on a continuous sample space, this convexity condition becomes the requirement that Hess f dominates λI. (Li & Montufar, 2018) `ev:computed` p. 13 ^li2018natural-025
- Two time discretizations of the flow are given: a forward Euler natural gradient method and a backward Euler Jordan-Kinderlehrer-Otto scheme. (Li & Montufar, 2018) `ev:reported` p. 14 ^li2018natural-026
- The authors suggest implementing the natural Wasserstein gradient with the forward Euler method, which is usually easier to implement than backward Euler. (Li & Montufar, 2018) `ev:asserted` p. 14 ^li2018natural-027
- The backward Euler method is described as usually unconditionally stable, which allows a large step size for computations. (Li & Montufar, 2018) `ev:asserted` p. 14 ^li2018natural-028
- With homogeneous degree one ground costs on three states, the static optimal transport gives a Finslerian rather than a Riemannian metric. (Li & Montufar, 2018) `ev:computed` p. 15 ^li2018natural-029
- Numerical geodesics were computed with a direct method from optimal control, discretizing time and minimizing the sum by gradient descent. (Li & Montufar, 2018) `ev:reported` p. 15 ^li2018natural-030
- On a three state path graph, Wasserstein geodesics between three fixed distributions form a triangle revealing a non Euclidean geometry of the simplex. (Li & Montufar, 2018) `ev:computed` p. 15 ^li2018natural-031
- In that geodesic triangle, the path connecting q1 and q3 bends towards q2, which does not happen for the other two paths. (Li & Montufar, 2018) `ev:computed` p. 16 ^li2018natural-032
- The authors read this bending as state 2 being treated differently from states 1 and 3 as a result of the ground metric. (Li & Montufar, 2018) `ev:asserted` p. 16 ^li2018natural-033
- The exponential geodesic triangle between the same three distributions is symmetric and makes no distinction between the three states. (Li & Montufar, 2018) `ev:computed` p. 16 ^li2018natural-034
- Example 2 applies the Wasserstein gradient flow to minimizing the expectation of a potential over the independence model of two binary variables. (Li & Montufar, 2018) `ev:reported` p. 16 ^li2018natural-035
- The four joint states of the two binary variables are connected by a square graph whose edge weights encode the inverse squared ground metric. (Li & Montufar, 2018) `ev:reported` p. 17 ^li2018natural-036
- The potential in Example 2 is taken from earlier work and takes the values 0, −2, −4 and 6 on the four states. (Li & Montufar, 2018) `ev:reported` p. 18 ^li2018natural-037
- On the independence model, the Wasserstein gradient direction depends on the ground metric on sample space, which is encoded in the edge weights. (Li & Montufar, 2018) `ev:computed` p. 18 ^li2018natural-038
- The attraction regions of the two local minimizers change dramatically as the edge weight between b and d varies over 0.1, 1 and 10. (Li & Montufar, 2018) `ev:computed` p. 18 ^li2018natural-039
- When the edge weight between b and d is small, the flow from d towards the local minimum b is suppressed. (Li & Montufar, 2018) `ev:computed` p. 19 ^li2018natural-040
- The Fisher-Rao gradient flow for the same objective is independent of the ground metric on sample space, unlike the Wasserstein flow. (Li & Montufar, 2018) `ev:computed` p. 18 ^li2018natural-041
- The authors interpret these results as showing that different ground metrics give different displacement convexity and different convergence regions. (Li & Montufar, 2018) `ev:asserted` p. 18 ^li2018natural-042
- Example 3 applies the [[Wasserstein natural gradient]] to maximum likelihood estimation by minimizing the Kullback-Leibler divergence from the empirical data distribution. (Li & Montufar, 2018) `ev:reported` p. 18 ^li2018natural-043
- The experiments use hierarchical log-linear k-interaction models on binary variables, parametrized either by orthogonal characters or by non-orthogonal monomials. (Li & Montufar, 2018) `ev:reported` p. 20 ^li2018natural-044
- The Wasserstein metric in these experiments uses the uniformly weighted graph of the binary cube, following the Hamming distance as ground metric. (Li & Montufar, 2018) `ev:reported` p. 20 ^li2018natural-045
- A few target distributions on binary vectors were sampled uniformly at random from a uniform Dirichlet distribution for the experiments. (Li & Montufar, 2018) `ev:reported` p. 20 ^li2018natural-046
- For each target distribution, the model was initialized at the uniform distribution, with the parameter vector set to zero. (Li & Montufar, 2018) `ev:reported` p. 20 ^li2018natural-047
- The Euclidean, Fisher and Wasserstein gradients were compared as preconditioners in the same gradient descent iteration with a learning rate. (Li & Montufar, 2018) `ev:reported` p. 20 ^li2018natural-048
- The simple adaptive step size method started from an initial learning rate of 0.001 in the maximum likelihood experiments. (Li & Montufar, 2018) `ev:reported` p. 21 ^li2018natural-049
- The learning rate was scaled down by a factor of 3/4 at every iteration where the divergence did not decrease. (Li & Montufar, 2018) `ev:reported` p. 21 ^li2018natural-050
- The authors also tried backtracking line search and Adam as alternative methods for choosing the step size in these experiments. (Li & Montufar, 2018) `ev:reported` p. 21 ^li2018natural-051
- Optimization stopped when the infinity norm of the expectation parameter matched the data expectation parameter to within 1 percent. (Li & Montufar, 2018) `ev:reported` p. 21 ^li2018natural-052
- The reported divergence minimization experiments use random target distributions on binary vectors with n = 7 over k-interaction models. (Li & Montufar, 2018) `ev:reported` p. 22 ^li2018natural-053
- All methods achieved similar divergence values, except the Euclidean gradient with non-orthogonal parametrization, which did not always reach the minimum. (Li & Montufar, 2018) `ev:measured` p. 21 ^li2018natural-054
- For the Fisher and Wasserstein gradients, the learning paths were virtually identical under the two model parametrizations, as expected for covariant gradients. (Li & Montufar, 2018) `ev:measured` p. 21 ^li2018natural-055
- For the Euclidean gradient, the learning paths and the number of iterations were heavily dependent on the model parametrization. (Li & Montufar, 2018) `ev:measured` p. 21 ^li2018natural-056
- With the Euclidean gradient, the orthogonal basis was usually a much better choice than the non-orthogonal basis in these experiments. (Li & Montufar, 2018) `ev:measured` p. 21 ^li2018natural-057
- The authors state that comparing iteration counts is difficult, since different methods work best with different step sizes. (Li & Montufar, 2018) `ev:asserted` p. 21 ^li2018natural-058
- With the simple adaptive method and a suitable initial step size, the [[Wasserstein natural gradient|Wasserstein gradient]] was faster than the Euclidean and Fisher gradients. (Li & Montufar, 2018) `ev:measured` p. 21 ^li2018natural-059
- When Adam was used to adapt the step size, the orthogonal Euclidean, Fisher and Wasserstein gradients performed comparably. (Li & Montufar, 2018) `ev:measured` p. 21 ^li2018natural-060
- In the current implementation, the [[Wasserstein natural gradient|Wasserstein gradient]] involved heavier computational costs than the Euclidean and Fisher gradients. (Li & Montufar, 2018) `ev:measured` p. 21 ^li2018natural-061
- The authors conclude that, with a suitable step size, the Wasserstein gradient can be a competitive optimization method. (Li & Montufar, 2018) `ev:asserted` p. 21 ^li2018natural-062
- The authors state that further experiments are needed on learning rate effects and on the interplay of ground metric, model and problem. (Li & Montufar, 2018) `ev:asserted` p. 21 ^li2018natural-063
- The authors state that exploring efficient computation and approximation approaches will be important for applications of the Wasserstein gradient. (Li & Montufar, 2018) `ev:asserted` p. 21 ^li2018natural-064
- The authors suggest that many studies from information geometry will have a natural analog or extension in the Wasserstein statistical manifold. (Li & Montufar, 2018) `ev:asserted` p. 22 ^li2018natural-065
- The authors suggest the ground metric could have a positive effect on generalization by introducing preferences in the hypothesis space. (Li & Montufar, 2018) `ev:asserted` p. 23 ^li2018natural-066
- The authors state that the specific form of such a ground metric regularization still needs to be developed and investigated. (Li & Montufar, 2018) `ev:asserted` p. 23 ^li2018natural-067

## 🎯 Contributions


## 📖 Glossary

- **Ground metric** — Distance between sample points, here encoded by edge weights of a graph.
- **Wasserstein statistical manifold** — Parameter space of a model carrying the pulled-back discrete L2-Wasserstein metric.
- **Natural gradient** — Gradient preconditioned by the inverse metric tensor of a Riemannian geometry on parameters.
- **Fisher-Rao metric** — Riemannian metric on probability models from the Fisher information matrix.
- **Benamou-Brenier formula** — Dynamical formulation of the Wasserstein distance as minimal kinetic action along density paths.
- **Linear weighted Laplacian** — Graph Laplacian whose edge weights are scaled by averaged endpoint probabilities.
- **Displacement convexity** — Geodesic convexity of a functional with respect to the Wasserstein metric.
- **JKO scheme** — Backward Euler (proximal) time discretization of a Wasserstein gradient flow.
- **Length space** — Space where distance equals the infimum length of continuous connecting curves.
- **k-interaction model** — Hierarchical log-linear model with interactions among at most k variables.

## ❓ Open questions

- Can the Wasserstein metric on probability manifolds be characterized by an invariance requirement of Chentsov type?
- Is there a weighted graph structure for which the corresponding Wasserstein metric recovers the Fisher metric?
- What specific form should a ground-metric-based regularization take to improve generalization?
- How should natural ground metrics be defined, and should they be fixed in advance or trained?
- How do learning rate, ground metric, model and optimization problem interact in practice?
- Which efficient computation or approximation schemes can reduce the higher cost of the Wasserstein gradient?

## 📝 Notes on reading

Version read is arXiv 1803.07033v5 (15 Apr 2021), while the registry year is 2018; the packet identifier is the arXiv record, so versions may differ in details.

Figures 1 and 2 (geodesic triangles in the simplex and exponential parameter space), Figures 3 and 4 (Wasserstein vs Fisher-Rao vector fields on the independence model) and Figure 5 (divergence values, iterations, normalized area histograms) were only described from captions and text; per-model values in Figure 5 were not claimed.

Internal inconsistencies: Theorem 9 refers to a second fundamental form in "Proposition ??" (broken reference); p. 18 cites "Theorem 14" for displacement convexity, which is Theorem 9; p. 13 refers to "the gradient flow (7)" where (12) is meant; p. 15 writes c12π23 where c23π23 appears intended. Equation extraction is garbled throughout (fractions such as q1 = 1/8(6, 1, 1) split across lines), so the distributions in (17) and the objective polynomial were not claimed with numbers.

The abstract promises only elementary examples; the MLE evidence is from a few random targets with n = 7, and no quantitative timing or iteration numbers are given in the text.

## Suggested new concepts

- Wasserstein natural gradient — central object of the paper and a counterpart to Fisher-Rao natural gradient in optimization notes.
- Discrete optimal transport on graphs — the graph-based dynamical Wasserstein metric underlies several related works by the same authors.
- Displacement convexity — geodesic convexity notion linking sample space Hessians to optimization landscapes on parameter space.
- Information geometry vs optimal transport — recurring comparison of Fisher-Rao and Wasserstein geometries worth a hub note.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Gradiente natural de Wasserstein (B.8).
