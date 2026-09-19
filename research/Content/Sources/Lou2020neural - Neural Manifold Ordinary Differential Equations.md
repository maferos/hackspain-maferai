---
aliases: []
type: "source"
title: "Neural Manifold Ordinary Differential Equations"
citekey: "Lou2020neural"
doi: "10.48550/arXiv.2006.10254"
arxiv: "2006.10254"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2006.10254"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Aaron Lou", "Derek Lim", "Isay Katsman", "Leo Huang", "Qingxuan Jiang", "Ser-Nam Lim", "Christopher De Sa"]
sha256: ["d782e6c62c6b7570c90eabf5f235b0322d8558da9787aacd43192b9e0e2c4ea7"]
pdf: "Content/Papers/Lou2020neural.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Lou2020neural.pdf]]

> [!abstract] One-sentence summary
> The paper generalizes Neural ODEs to arbitrary smooth manifolds through a dynamic chart method, yielding Manifold Continuous Normalizing Flows that beat earlier hyperbolic and spherical flows on density estimation and variational inference.

## Abstract

To better conform to data geometry, recent deep generative modelling techniques adapt Euclidean constructions to non-Euclidean spaces. In this paper, we study normalizing flows on manifolds. Previous work has developed flow models for specific cases; however, these advancements hand craft layers on a manifold-by-manifold basis, restricting generality and inducing cumbersome design constraints. We overcome these issues by introducing Neural Manifold Ordinary Differential Equations, a manifold generalization of Neural ODEs, which enables the construction of Manifold Continuous Normalizing Flows (MCNFs). MCNFs require only local geometry (therefore generalizing to arbitrary manifolds) and compute probabilities with continuous change of variables (allowing for a simple and expressive flow construction). We find that leveraging continuous manifold dynamics produces a marked improvement for both density estimation and downstream tasks. (arXiv)

## 🧠 Key ideas (atomic)

- The authors introduce Neural Manifold ODEs as a generalization of Neural ODEs, used to build Manifold Continuous Normalizing Flows on manifolds. (Lou et al., 2020) `ev:asserted` p. 2 ^lou2020neural-001
- Without additional constraints, evaluating the determinant in the change of variables takes O(D3) time, where D is the dimension of z. (Lou et al., 2020) `ev:asserted` p. 2 ^lou2020neural-002
- Continuous Normalizing Flows build the flow with a Neural ODE whose continuous change of variables requires only the trace of the dynamics Jacobian. (Lou et al., 2020) `ev:cited` p. 2 ^lou2020neural-003
- The authors state that preexisting manifold normalizing flow works, reviewed in their related work section, do not generalize to arbitrary manifolds. (Lou et al., 2020) `ev:asserted` p. 2 ^lou2020neural-004
- The authors derive a manifold analogue of the adjoint method to compute gradients of Neural Manifold ODEs in backward mode. (Lou et al., 2020) `ev:asserted` p. 2 ^lou2020neural-005
- The dynamic chart method realizes Neural Manifold ODEs by integrating local dynamics in Euclidean space between smooth chart transitions. (Lou et al., 2020) `ev:reported` p. 2 ^lou2020neural-006
- The first manifold flow projects onto Euclidean space, which the authors call flawed since it requires a manifold diffeomorphic to Euclidean space. (Lou et al., 2020) `ev:cited` p. 2 ^lou2020neural-007
- According to the authors, the existence of antipodal points implies that the sphere is not diffeomorphic to Euclidean space. (Lou et al., 2020) `ev:asserted` p. 2 ^lou2020neural-008
- The authors state that the Tangent Coupling and Wrapped Hyperboloid Coupling flows do not generalize to topologically nontrivial manifolds. (Lou et al., 2020) `ev:asserted` p. 3 ^lou2020neural-009
- In the authors' experiments, the Tangent Coupling and Wrapped Hyperboloid Coupling flows do not seem to conclusively outperform the earlier projection flow. (Lou et al., 2020) `ev:measured` p. 3 ^lou2020neural-010
- The authors argue the Wrapped Hyperboloid Coupling construction is not intrinsic to hyperbolic space, since it relies on the hyperboloid equation. (Lou et al., 2020) `ev:asserted` p. 3 ^lou2020neural-011
- The primary recursive sphere flow of earlier tori and spheres work uses non-global diffeomorphisms to the cylinder, so densities are not defined everywhere. (Lou et al., 2020) `ev:cited` p. 3 ^lou2020neural-012
- The authors do not compare directly against an earlier Lie group flow, since Lie groups are not general while Riemannian manifolds are. (Lou et al., 2020) `ev:asserted` p. 3 ^lou2020neural-013
- The authors note that hyperbolic space is diffeomorphic to Euclidean space, whereas spheres and tori are not. (Lou et al., 2020) `ev:asserted` p. 4 ^lou2020neural-014
- Unlike Neural ODEs, the forward mode requires explicit manifold methods, whereas the backward pass can be defined solely through a Euclidean ODE. (Lou et al., 2020) `ev:asserted` p. 4 ^lou2020neural-015
- Projection solvers require additional structure: the manifold must be the level set of some smooth function on an ambient Euclidean space. (Lou et al., 2020) `ev:asserted` p. 4 ^lou2020neural-016
- Implicit solvers that work locally through charts can be applied to any manifold and do not require a level set representation. (Lou et al., 2020) `ev:asserted` p. 5 ^lou2020neural-017
- Theorem 4.1 shows that, given an ambient Euclidean embedding, the manifold adjoint state satisfies an ODE resembling the Euclidean adjoint method. (Lou et al., 2020) `ev:computed` p. 5 ^lou2020neural-018
- The authors argue the embedding assumption loses no generality, since the Whitney Embedding Theorem guarantees an embedding with d = 2n. (Lou et al., 2020) `ev:asserted` p. 5 ^lou2020neural-019
- The dynamic chart method is motivated by a dynamic manifold trivialization technique previously introduced for Riemannian gradient descent. (Lou et al., 2020) `ev:cited` p. 5 ^lou2020neural-020
- Proposition 5.1 shows that mapping a local Euclidean ODE solution through the chart gives a valid local solution of the manifold ODE. (Lou et al., 2020) `ev:computed` p. 6 ^lou2020neural-021
- Proposition 5.2 shows that a finite collection of charts suffices to cover the ODE solution curve over the whole integration interval. (Lou et al., 2020) `ev:computed` p. 6 ^lou2020neural-022
- Under the dynamic chart forward pass, a Neural Manifold ODE block is a composition of Neural ODE blocks and chart transitions. (Lou et al., 2020) `ev:asserted` p. 6 ^lou2020neural-023
- For Riemannian manifolds, exponential map charts are used, switching to a new exponential map chart when the local solution nears the injectivity radius. (Lou et al., 2020) `ev:reported` p. 7 ^lou2020neural-024
- The authors claim the dynamic chart method allows faster evaluations by sidestepping repeated, expensive Lie and Riemannian exponential map calls. (Lou et al., 2020) `ev:asserted` p. 7 ^lou2020neural-025
- The authors argue that the dynamic chart method avoids catastrophic gradient instability that arises when solver error pushes gradients off their domain. (Lou et al., 2020) `ev:asserted` p. 7 ^lou2020neural-026
- MCNF log probabilities combine the continuous change of variables inside each Neural ODE block with log-determinants of the chart maps. (Lou et al., 2020) `ev:computed` p. 7 ^lou2020neural-027
- The determinant of the exponential map derivative can be evaluated analytically for the hyperboloid and the sphere, as shown in prior work. (Lou et al., 2020) `ev:cited` p. 7 ^lou2020neural-028
- The authors avoid diffeomorphism issues from antipodal points on the sphere by restricting chart domains to never include these conjugate points. (Lou et al., 2020) `ev:asserted` p. 7 ^lou2020neural-029
- Experiments cover density estimation and variational inference, taking the manifold to be either hyperbolic space or the sphere. (Lou et al., 2020) `ev:reported` p. 7 ^lou2020neural-030
- Hyperbolic density estimation baselines are Wrapped Hyperboloid Coupling and Projected NVP, which learns RealNVP over a projection of the hyperboloid. (Lou et al., 2020) `ev:reported` p. 8 ^lou2020neural-031
- On the sphere, MCNF is compared with the recursive construction of earlier work, using non-compact projection for the circle flow. (Lou et al., 2020) `ev:reported` p. 8 ^lou2020neural-032
- As visualized in Figures 3 and 4, the MCNF flows match complex target densities with significant improvement over the baselines. (Lou et al., 2020) `ev:measured` p. 8 ^lou2020neural-033
- MCNF is able to fit discontinuous and multi-modal target densities that the baseline methods cannot fit in these experiments. (Lou et al., 2020) `ev:measured` p. 8 ^lou2020neural-034
- The authors attribute the baseline failures to their struggle with reducing probability mass in areas of low target density. (Lou et al., 2020) `ev:asserted` p. 8 ^lou2020neural-035
- Variational inference experiments train hyperbolic and Euclidean VAEs on Binarized Omniglot and Binarized MNIST, comparing flow layers in the latent space. (Lou et al., 2020) `ev:reported` p. 8 ^lou2020neural-036
- On MNIST with latent dimension 2, MCNF reaches 138.14 average negative test log likelihood, versus 139.58 for Tangent Coupling. (Lou et al., 2020) `ev:measured` p. 8 ^lou2020neural-037
- On MNIST with latent dimension 4, MCNF reaches 113.47 negative test log likelihood, versus 113.78 for Wrapped Hyperboloid Coupling. (Lou et al., 2020) `ev:measured` p. 8 ^lou2020neural-038
- On MNIST with latent dimension 6, MCNF reaches 99.89 negative test log likelihood, versus 100.06 for PRNVP and 100.64 for CNF. (Lou et al., 2020) `ev:measured` p. 8 ^lou2020neural-039
- On Omniglot with latent dimension 2, MCNF reaches 152.98 negative test log likelihood, versus 153.93 for RealNVP and 153.97 for HVAE. (Lou et al., 2020) `ev:measured` p. 8 ^lou2020neural-040
- On Omniglot with latent dimension 6, Euclidean RealNVP reaches 137.21 negative test log likelihood, slightly below MCNF at 137.29. (Lou et al., 2020) `ev:measured` p. 8 ^lou2020neural-041
- The authors report that their continuous flow regime is more expressive and learns better than all hyperbolic baselines in Table 1. (Lou et al., 2020) `ev:measured` p. 8 ^lou2020neural-042
- In low latent dimensions, MCNF and the other hyperbolic models tend to outperform Euclidean models on Omniglot and MNIST. (Lou et al., 2020) `ev:measured` p. 8 ^lou2020neural-043
- In high latent dimension, even the baseline hyperbolic VAE does not consistently outperform the Euclidean VAE on these datasets. (Lou et al., 2020) `ev:measured` p. 8 ^lou2020neural-044
- The authors conclude their method is completely general, as it does not require anything beyond local manifold structure. (Lou et al., 2020) `ev:asserted` p. 9 ^lou2020neural-045
- The authors expect Manifold Continuous Normalizing Flows to be applied to topologically nontrivial data in lattice quantum field theory. (Lou et al., 2020) `ev:asserted` p. 9 ^lou2020neural-046
- For hyperbolic space, the base distribution is the hyperbolic wrapped normal, sampled through parallel transport and the exponential map. (Lou et al., 2020) `ev:reported` p. 14 ^lou2020neural-047
- For the sphere, the authors use a von Mises-Fisher base distribution, arguing a wrapped normal is flawed between conjugate points. (Lou et al., 2020) `ev:asserted` p. 14 ^lou2020neural-048
- The derivative of the spherical logarithmic map is derived explicitly, due to numerical instability of higher order derivatives of some functions. (Lou et al., 2020) `ev:reported` p. 16 ^lou2020neural-049
- Since hyperbolic space needs only one chart, its Manifold ODE can model the full dynamics in the tangent space alone. (Lou et al., 2020) `ev:reported` p. 17 ^lou2020neural-050
- Density estimation trains on batches of 200 target samples, with MCNF and hyperbolic baselines using at most 1,000,000 samples. (Lou et al., 2020) `ev:reported` p. 18 ^lou2020neural-051
- The spherical baseline needed at least 5,000,000 samples, so it was allowed to train until its density converged. (Lou et al., 2020) `ev:measured` p. 18 ^lou2020neural-052
- MCNF achieves better results than the spherical baseline with, frequently, over an order of magnitude fewer samples, though sample efficiency was not investigated in detail. (Lou et al., 2020) `ev:measured` p. 18 ^lou2020neural-053
- For density estimation, MCNF dynamics use a network of hidden dimension 32 with 4 linear layers, tanh activations and a Runge-Kutta 4 solver. (Lou et al., 2020) `ev:reported` p. 19 ^lou2020neural-054
- For continuous flows in variational inference, dynamics are a two-layer network of hidden size 128 with tanh activations. (Lou et al., 2020) `ev:reported` p. 19 ^lou2020neural-055
- In practice, the time interval is split uniformly into segments, with the solution learned locally through exponential map charts at segment endpoints. (Lou et al., 2020) `ev:reported` p. 19 ^lou2020neural-056
- The authors note that local dynamics may still drive the solver toward the edges of the injectivity ball, causing instability. (Lou et al., 2020) `ev:asserted` p. 20 ^lou2020neural-057
- They suggest a local Lipschitz bound, below the injectivity radius divided by segment length, to keep the local solution inside the ball. (Lou et al., 2020) `ev:asserted` p. 20 ^lou2020neural-058
- The antipodal test uses a von Mises-Fisher target with concentration 30, and a base von Mises-Fisher with concentration 3. (Lou et al., 2020) `ev:reported` p. 20 ^lou2020neural-059
- On a sphere target concentrated at the antipode of the base mean, MCNF with just one chart fails to learn the density. (Lou et al., 2020) `ev:measured` p. 20 ^lou2020neural-060
- With 16 charts, MCNF learns the antipodal target density well, which the authors take as validation of the dynamic chart method. (Lou et al., 2020) `ev:measured` p. 20 ^lou2020neural-061
- With a two-dimensional hyperbolic latent space, a trained MCNF generates MNIST samples that resemble real digits. (Lou et al., 2020) `ev:measured` p. 21 ^lou2020neural-062

## 🎯 Contributions


## 📖 Glossary

- **Normalizing flow** — Generative model mapping a simple density through an invertible map with tractable change of variables.
- **Continuous Normalizing Flow (CNF)** — Normalizing flow defined by a Neural ODE, using the trace of the dynamics Jacobian.
- **Neural Manifold ODE** — Manifold ODE whose vector field is parameterized by a neural network.
- **Manifold Continuous Normalizing Flow (MCNF)** — Continuous normalizing flow built from a Neural Manifold ODE on an arbitrary manifold.
- **Chart** — Smooth bijection between an open subset of Euclidean space and a region of the manifold.
- **Dynamic chart method** — Solving a manifold ODE by switching local charts during integration, each solved in Euclidean space.
- **Exponential map** — Map sending a tangent vector to the manifold point reached along a geodesic of that length.
- **Injectivity radius** — Radius within which the exponential map at a point is a diffeomorphism.
- **Conjugate points** — Points, such as sphere antipodes, where exponential map charts stop being diffeomorphisms.
- **Adjoint method** — Computes ODE gradients by solving a backward adjoint ODE instead of differentiating through the solver.
- **von Mises-Fisher distribution** — Directional distribution on the sphere with mean direction and concentration parameter.

## ❓ Open questions

- Does the dynamic chart method scale to high-dimensional manifolds with conjugate points, beyond the two-dimensional sphere tested?
- Would a non-uniform time-domain split of charts give benefits without prior knowledge of local manifold topology?
- How should the local Lipschitz constraint be enforced in practice for complicated densities on manifolds with conjugate points?
- Why does the hyperbolic advantage fade in higher latent dimensions, as seen for Omniglot in Table 1?
- Do MCNFs deliver the anticipated gains on real topologically nontrivial data such as lattice field theory, motion estimation or protein structure?
- How does sample efficiency of MCNF compare with discrete manifold flows when studied systematically?

## 📝 Notes on reading

Read the arXiv v1 preprint (2006.10254v1, June 2020, marked as under review). Figures 1, 2, 3, 4, 5, 6 and 7 are qualitative visualizations and were described rather than claimed as numbers. Table 1 extracted cleanly; only headline rows were claimed. Several equations (Equations 3, 4, 20, 21, 28) and Tables 2 and 3 were garbled by extraction and were not claimed. Inconsistency: Appendix C.2 cites reference [38] for the discrete spherical flows, whereas the related work and Section 7.1 cite [39] for that construction. In Omniglot dimension 4 and 6, the Euclidean RealNVP matches or slightly beats MCNF, so the abstract's marked improvement holds mainly against manifold baselines.

## Suggested new concepts

- Dynamic chart method — a general technique for integrating ODEs on manifolds via switching local charts, reusable beyond flows.
- Manifold normalizing flows — the family of density models on non-Euclidean spaces compared in this paper.
- Continuous normalizing flows — the Euclidean base construction that MCNF generalizes.
- Conjugate points — the topological obstacle that motivates multi-chart integration on spheres.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H2.** Flujos continuos (ODE) definidos en cartas de la variedad: densidades exactas en $S^2$, $SO(3)$ o espacios hiperbólicos, precursor de los flujos riemannianos usados para poses.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
