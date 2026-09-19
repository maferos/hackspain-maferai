---
aliases: []
type: "source"
title: "Riemannian Score-Based Generative Modelling"
citekey: "Bortoli2022riemannian"
doi: "10.48550/arXiv.2202.02763"
arxiv: "2202.02763"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2202.02763"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Valentin De Bortoli", "Emile Mathieu", "Michael Hutchinson", "James Thornton", "Yee Whye Teh", "Arnaud Doucet"]
sha256: ["059cdfa319a90a127ff3e1e094c7d941a629860f9ebeb24b05418110130c229a"]
pdf: "Content/Papers/Bortoli2022riemannian.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 55
---

📄 PDF: [[Bortoli2022riemannian.pdf]]

> [!abstract] One-sentence summary
> The paper extends score-based diffusion models to Riemannian manifolds by noising with manifold Brownian or Langevin dynamics, proving a manifold time-reversal formula, and sampling with geodesic random walks, which lets generative models respect the geometry of spherical, toroidal, rotation-group and hyperbolic data.

## Abstract

Score-based generative models (SGMs) are a powerful class of generative models that exhibit remarkable empirical performance. Score-based generative modelling (SGM) consists of a ``noising'' stage, whereby a diffusion is used to gradually add Gaussian noise to data, and a generative model, which entails a ``denoising'' process defined by approximating the time-reversal of the diffusion. Existing SGMs assume that data is supported on a Euclidean space, i.e. a manifold with flat geometry. In many domains such as robotics, geoscience or protein modelling, data is often naturally described by distributions living on Riemannian manifolds and current SGM techniques are not appropriate. We introduce here Riemannian Score-based Generative Models (RSGMs), a class of generative models extending SGMs to Riemannian manifolds. We demonstrate our approach on a variety of manifolds, and in particular with earth and climate science spherical data. (arXiv)

## 🧠 Key ideas (atomic)

- The authors introduce [[Riemannian diffusion models|Riemannian Score-based Generative Models]], which define the forward noising diffusion directly on the Riemannian manifold instead of on Euclidean space. (De Bortoli et al., 2022) `ev:asserted` p. 1 ^bortoli2022riemannian-001
- The authors note that existing score-based generative models have been applied primarily to data living on Euclidean spaces, meaning manifolds with flat geometry. (De Bortoli et al., 2022) `ev:asserted` p. 1 ^bortoli2022riemannian-002
- The paper lists protein modelling, geological sciences, robotics and high-energy physics among domains whose distributions of interest live on Riemannian manifolds. (De Bortoli et al., 2022) `ev:cited` p. 1 ^bortoli2022riemannian-003
- The authors state that four components are needed: a noising process, a time-reversal formula, an SDE sampler on manifolds, and a drift approximation. (De Bortoli et al., 2022) `ev:asserted` p. 2 ^bortoli2022riemannian-004
- The noising process is Langevin dynamics on the manifold, whose invariant density with respect to the volume form is proportional to exp(-U). (De Bortoli et al., 2022) `ev:reported` p. 3 ^bortoli2022riemannian-005
- On compact manifolds the method targets the uniform distribution, so the drift vanishes and the noising process is simply a Brownian motion. (De Bortoli et al., 2022) `ev:reported` p. 3 ^bortoli2022riemannian-006
- The authors state that, unlike the Riemannian normal, the exponential wrapped Gaussian is easy to sample and its density easy to evaluate. (De Bortoli et al., 2022) `ev:cited` p. 3 ^bortoli2022riemannian-007
- Theorem 3.1 proves that the time-reversal of a manifold diffusion is again a diffusion whose drift adds the Riemannian gradient of the log density. (De Bortoli et al., 2022) `ev:computed` p. 3 ^bortoli2022riemannian-008
- The time-reversal proof extends Theorem 4.9 of Cattiaux et al. (2021) from the Euclidean case to Riemannian manifolds. (De Bortoli et al., 2022) `ev:cited` p. 3 ^bortoli2022riemannian-009
- The authors argue that extrinsic sampling through an ambient embedding needs a projection back onto the manifold at each step, which can accumulate errors. (De Bortoli et al., 2022) `ev:asserted` p. 3 ^bortoli2022riemannian-010
- Diffusions are simulated intrinsically with Geodesic Random Walks, which push a tangent-space Euler–Maruyama step through the exponential map at each iteration. (De Bortoli et al., 2022) `ev:reported` p. 4 ^bortoli2022riemannian-011
- The paper provides a novel extension of geodesic random walk error bounds to the time-inhomogeneous case in Appendix I.2. (De Bortoli et al., 2022) `ev:computed` p. 4 ^bortoli2022riemannian-012
- Proposition 3.3 shows the denoising score matching loss equals twice the implicit score matching loss plus a term independent of the score. (De Bortoli et al., 2022) `ev:computed` p. 4 ^bortoli2022riemannian-013
- The implicit score matching loss needs a divergence costing d Jacobian-vector calls, so a stochastic Hutchinson estimator is necessary in high dimension. (De Bortoli et al., 2022) `ev:asserted` p. 5 ^bortoli2022riemannian-014
- Non-parallelizable manifolds such as S2 lack a global frame, so the score network uses n > d vector fields spanning the tangent bundle. (De Bortoli et al., 2022) `ev:asserted` p. 5 ^bortoli2022riemannian-015
- On compact manifolds the heat kernel is typically available only as an infinite Sturm–Liouville series, unlike the Gaussian Euclidean transition density. (De Bortoli et al., 2022) `ev:asserted` p. 5 ^bortoli2022riemannian-016
- When Laplace–Beltrami eigenpairs are known, as on the torus and sphere, the log heat kernel gradient is approximated by truncating the series. (De Bortoli et al., 2022) `ev:reported` p. 6 ^bortoli2022riemannian-017
- When eigenpairs are unknown, Varadhan asymptotics approximate the score for small times as the inverse exponential map divided by t. (De Bortoli et al., 2022) `ev:reported` p. 6 ^bortoli2022riemannian-018
- Table 2 lists denoising losses with truncation or Varadhan approximations at O(1) cost, while deterministic implicit score matching costs O(d). (De Bortoli et al., 2022) `ev:reported` p. 6 ^bortoli2022riemannian-019
- Theorem 4.1 bounds the Wasserstein-1 distance between generated samples and data by terms in time horizon, score error and step size. (De Bortoli et al., 2022) `ev:computed` p. 7 ^bortoli2022riemannian-020
- The convergence theorem assumes a heat-kernel diagonal bound that holds for spheres, tori, compact matrix groups and their products. (De Bortoli et al., 2022) `ev:asserted` p. 7 ^bortoli2022riemannian-021
- The authors say their bound accounts for time discretization, contrary to the Moser flow bound of Rozen et al., which considers continuous time. (De Bortoli et al., 2022) `ev:asserted` p. 7 ^bortoli2022riemannian-022
- The authors argue that push-forward Euclidean normalizing flows need a homeomorphism to the manifold, limiting them to manifolds topologically equivalent to Rn. (De Bortoli et al., 2022) `ev:asserted` p. 7 ^bortoli2022riemannian-023
- Per Table 3, RSGM training uses score matching costing O(d) or O(1), whereas Riemannian CNF training solves an ODE costing O(dN). (De Bortoli et al., 2022) `ev:reported` p. 8 ^bortoli2022riemannian-024
- The sphere benchmark uses occurrences of volcanic eruptions, earthquakes, floods and wild fires, with 827, 6120, 4875 and 12809 events. (De Bortoli et al., 2022) `ev:reported` p. 8 ^bortoli2022riemannian-025
- The sphere baselines were Riemannian continuous normalizing flows, Moser flows, a mixture of Kent distributions and a stereographic score-based model. (De Bortoli et al., 2022) `ev:reported` p. 8 ^bortoli2022riemannian-026
- The Riemannian score-based model reached a negative log-likelihood of −1.33±0.06 on the Fire dataset over 5 runs. (De Bortoli et al., 2022) `ev:measured` p. 8 ^bortoli2022riemannian-027
- On the Volcano dataset the Riemannian CNF reached a negative log-likelihood of −6.05±0.61, lower than the RSGM value of −4.92±0.25. (De Bortoli et al., 2022) `ev:measured` p. 8 ^bortoli2022riemannian-028
- On the Flood dataset the Riemannian score-based model reached a negative log-likelihood of 0.45±0.17, against 0.57±0.10 for Moser flows. (De Bortoli et al., 2022) `ev:measured` p. 8 ^bortoli2022riemannian-029
- The authors observe that all benchmarked methods perform comparably on these simple sphere tasks, with RSGM marginally better on most datasets. (De Bortoli et al., 2022) `ev:measured` p. 8 ^bortoli2022riemannian-030
- The authors empirically notice that Moser flows are slow to train on the earth science datasets. (De Bortoli et al., 2022) `ev:measured` p. 8 ^bortoli2022riemannian-031
- The authors note that Moser flows and stereographic score-based models are computationally expensive to evaluate on the sphere datasets. (De Bortoli et al., 2022) `ev:measured` p. 8 ^bortoli2022riemannian-032
- The scalability test fits a wrapped Gaussian target with random mean on the torus Td across increasing dimension d. (De Bortoli et al., 2022) `ev:reported` p. 8 ^bortoli2022riemannian-033
- The authors expect Moser flows to fail in high dimension, since their Monte Carlo regularizer needs samples growing as O(ed). (De Bortoli et al., 2022) `ev:asserted` p. 8 ^bortoli2022riemannian-034
- On the high-dimensional torus, [[Riemannian diffusion models|RSGMs]] fit the target well with linear or constant computational cost depending on the divergence estimator. (De Bortoli et al., 2022) `ev:measured` p. 9 ^bortoli2022riemannian-035
- Moser flows scale poorly with torus dimension, to the extent that the authors were unable to train them for d ≥10. (De Bortoli et al., 2022) `ev:measured` p. 9 ^bortoli2022riemannian-036
- The gap between Moser closed-form and ODE likelihoods increases with the torus dimension in Figure 3. (De Bortoli et al., 2022) `ev:measured` p. 9 ^bortoli2022riemannian-037
- On SO3(R) mixtures, RSGMs are compared with Moser flows and an exp-wrapped SGM pushed forward from the Lie algebra so(3). (De Bortoli et al., 2022) `ev:reported` p. 9 ^bortoli2022riemannian-038
- The authors observe [[Riemannian diffusion models|RSGMs]] perform consistently across mixture component counts, whereas exp-wrapped SGMs and Moser flows perform well only in some range. (De Bortoli et al., 2022) `ev:measured` p. 9 ^bortoli2022riemannian-039
- With M = 32 components on SO3(R), RSGM reached a test log-likelihood of 0.20±0.03, against 0.17±0.03 for Moser flows. (De Bortoli et al., 2022) `ev:measured` p. 10 ^bortoli2022riemannian-040
- On every SO3(R) mixture, RSGMs needed 0.1±0.0 thousand score network evaluations, against 0.5 for exp-wrapped SGMs. (De Bortoli et al., 2022) `ev:measured` p. 10 ^bortoli2022riemannian-041
- Figure 4b suggests RSGMs are much more robust to learning rate and diffusion coefficient hyperparameters than exp-wrapped SGMs on SO3(R). (De Bortoli et al., 2022) `ev:measured` p. 10 ^bortoli2022riemannian-042
- On the non-compact hyperbolic plane H2, the authors qualitatively see that both score-based models fit a mixture of wrapped normal distributions. (De Bortoli et al., 2022) `ev:measured` p. 10 ^bortoli2022riemannian-043
- The authors claim the main benefits are scalability to high dimensions, broad manifold applicability, robustness, and the capacity to model complex datasets. (De Bortoli et al., 2022) `ev:asserted` p. 10 ^bortoli2022riemannian-044
- As future work, the authors would like to explore manifolds with a boundary and alternative noising processes. (De Bortoli et al., 2022) `ev:asserted` p. 10 ^bortoli2022riemannian-045
- The authors propose deriving efficient algorithms for Schrödinger bridges on manifolds as another promising extension of this work. (De Bortoli et al., 2022) `ev:asserted` p. 10 ^bortoli2022riemannian-046
- The authors argue Moser flows interpolate in density space, whereas RSGM interpolates in sample space, displacing density rather than creating it. (De Bortoli et al., 2022) `ev:asserted` p. 43 ^bortoli2022riemannian-047
- Density estimation is not directly accessible with RSGM, so the appendix proposes estimating it through the Fisher score. (De Bortoli et al., 2022) `ev:asserted` p. 43 ^bortoli2022riemannian-048
- The authors found stereographic score-based baselines perform less well than intrinsic models, since mapping density near seams sends points to infinity. (De Bortoli et al., 2022) `ev:measured` p. 47 ^bortoli2022riemannian-049
- The score network is a multilayer perceptron with 512 units per layer and sinusoidal activations, implemented in Jax with a modified Geomstats. (De Bortoli et al., 2022) `ev:reported` p. 47 ^bortoli2022riemannian-050
- Models were trained with Adam at batch size 512, using 100-step Euler–Maruyama rollouts without a corrector unless stated. (De Bortoli et al., 2022) `ev:reported` p. 48 ^bortoli2022riemannian-051
- The authors found that training with the denoising score matching loss gave results similar to the sliced score matching default. (De Bortoli et al., 2022) `ev:measured` p. 48 ^bortoli2022riemannian-052
- From N = 5 geodesic random walk steps, approximate forward samples are distributed very closely to the reference samples by MMD. (De Bortoli et al., 2022) `ev:measured` p. 48 ^bortoli2022riemannian-053
- Apart from very small step counts, RSGM log-likelihood on Flood is very robust to the forward-sampling approximation quality. (De Bortoli et al., 2022) `ev:measured` p. 48 ^bortoli2022riemannian-054
- The Varadhan approximation alone yields decent performance, though combining it with heat-kernel truncation can give even better results. (De Bortoli et al., 2022) `ev:measured` p. 48 ^bortoli2022riemannian-055

## 🎯 Contributions


## 📖 Glossary

- **Score-based generative model (SGM)** — Generative model sampling data by simulating the learned time-reversal of a noising diffusion.
- **Stein score** — Gradient of the log density of the noised data distribution.
- **Geodesic Random Walk** — Discrete process moving along geodesics from tangent-space Gaussian steps via the exponential map.
- **Exponential map** — Map sending a tangent vector at a point to the geodesic endpoint on the manifold.
- **Heat kernel** — Transition density of Brownian motion on a manifold.
- **Sturm–Liouville decomposition** — Expansion of the heat kernel in Laplace–Beltrami eigenvalues and eigenfunctions.
- **Varadhan asymptotics** — Small-time approximation of the log heat kernel gradient by the inverse exponential map.
- **Denoising score matching (DSM)** — Score training loss regressing on the gradient of the transition log density.
- **Implicit score matching (ISM)** — Score training loss using the score norm plus its divergence, no transition density.
- **Moser flow** — Continuous normalizing flow on manifolds interpolating densities linearly, avoiding ODE solves during training.
- **Parallelizable manifold** — Manifold admitting d smooth vector fields spanning every tangent space.

## ❓ Open questions

- How do RSGMs extend to manifolds with a boundary, which the convergence analysis and noising processes currently exclude?
- Which alternative noising processes on manifolds would improve sample quality or training efficiency?
- Can efficient Schrödinger bridge algorithms be derived on manifolds to interpolate between two data distributions?
- Does the convergence guarantee extend beyond compact manifolds to the non-compact case, such as hyperbolic space?
- How does RSGM compare quantitatively on hyperbolic space, where only qualitative results are shown?

## 📝 Notes on reading

Version read: arXiv:2202.02763v3 (22 Nov 2022), the NeurIPS 2022 camera-ready with supplementary; this matches the packet identifier.

Table 4 is captioned as negative log-likelihood (lower is better). On Volcano the Riemannian CNF (−6.05±0.61) scores lower than RSGM (−4.92±0.25), yet the text says RSGM performs marginally better on most datasets; the Fire and Flood rows favour RSGM, Earthquake ties with the stereographic model. The bold marks were lost in extraction, so which entries the authors bolded could not be checked.

Theorem 4.1 is printed with an equals sign (W1(L(YN), p0) = C(...)); the following sentence treats it as an upper bound.

Inconsistency between main text and appendix on the torus target: Sec. 6.2 says the wrapped Gaussian has unit variance, App. O.2 says standard deviation of 0.2.

Inconsistency on the SO3(R) mixture: Table 5 reports M = 16, 32 and 64 components, while App. O.3 says K = 32 mixture components are chosen. App. O.3 also writes SO3(Rd) and so(n) in places where SO3(R) and so(3) are meant.

Figure 3 (torus steps per second and bits per dimension vs dimension) and Figure 4b (SO3 hyperparameter heatmaps) were only partly legible; the heatmap numbers were not claimed cell by cell. Figure 5 in App. O.1 (DSM ablation grid over τ and J on Flood) is a heatmap whose rows could not be reliably aligned to τ values.

The appendix pages were read selectively (App. A, E, G, K, L, M, N, O); the full proofs in App. H–J were not claimed.

## Suggested new concepts

- Geodesic Random Walk — intrinsic SDE simulation scheme on manifolds reused across manifold diffusion and sampling work.
- Riemannian diffusion models — family of generative models on manifolds (RSGM, Riemannian diffusion, flow matching on manifolds) relevant to pose and rotation generation in robotics.
- Heat kernel approximation on manifolds — truncated eigen-expansions versus Varadhan asymptotics as a recurring numerical tool.
- Moser flow — competing manifold continuous-flow baseline that appears across manifold generative modelling benchmarks.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H2.** Fundamento teórico de la difusión por score en variedades compactas como SO(3), base de los generadores de agarres y acciones del corpus.
