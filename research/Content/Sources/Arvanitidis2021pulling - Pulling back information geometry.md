---
aliases: []
type: "source"
title: "Pulling back information geometry"
citekey: "Arvanitidis2021pulling"
doi: "10.48550/arXiv.2106.05367"
arxiv: "2106.05367"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2106.05367"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Georgios Arvanitidis", "Miguel González-Duque", "Alison Pouplin", "Dimitris Kalatzis", "Søren Hauberg"]
sha256: ["4b2174eb59d28c6ecbc76c92f512012ee020eb3816a6d67bea5d3e8e8d98e46a"]
pdf: "Content/Papers/Arvanitidis2021pulling.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 58
---

📄 PDF: [[Arvanitidis2021pulling.pdf]]

> [!abstract] One-sentence summary
> The paper pulls the Fisher-Rao metric of the decoder's distribution space back to a VAE latent space, giving identifiable latent geometries for almost any decoder with a differentiable KL divergence rather than only Gaussian ones.

## Abstract

Latent space geometry has shown itself to provide a rich and rigorous framework for interacting with the latent variables of deep generative models. The existing theory, however, relies on the decoder being a Gaussian distribution as its simple reparametrization allows us to interpret the generating process as a random projection of a deterministic manifold. Consequently, this approach breaks down when applied to decoders that are not as easily reparametrized. We here propose to use the Fisher-Rao metric associated with the space of decoder distributions as a reference metric, which we pull back to the latent space. We show that we can achieve meaningful latent geometries for a wide range of decoder distributions for which the previous theory was not applicable, opening the door to `black box' latent geometries. (arXiv)

## 🧠 Key ideas (atomic)

- For non-Gaussian decoders, the authors state that no useful approach exists for treating the associated random manifold as deterministic. (Arvanitidis et al., 2021) `ev:asserted` p. 1 ^arvanitidis2021pulling-001
- The key idea is to reinterpret the decoder as spanning a deterministic manifold in the space of probability distributions rather than observation space. (Arvanitidis et al., 2021) `ev:asserted` p. 1 ^arvanitidis2021pulling-002
- The approach is applicable to any family of decoders for which the KL-divergence can be differentiated, allowing work from a single codebase. (Arvanitidis et al., 2021) `ev:asserted` p. 2 ^arvanitidis2021pulling-003
- The authors state that non-identifiability of latent representations implies it is improper to view the latent space as Euclidean. (Arvanitidis et al., 2021) `ev:asserted` p. 2 ^arvanitidis2021pulling-004
- The earlier Gaussian-decoder metric adds a standard-deviation Jacobian term to the mean Jacobian term, giving shortest paths that follow the data. (Arvanitidis et al., 2021) `ev:cited` p. 3 ^arvanitidis2021pulling-005
- Pulling back the Euclidean metric through the Gaussian reparametrization is a strategy that can only extend to location-scale distributions, per the authors. (Arvanitidis et al., 2021) `ev:asserted` p. 3 ^arvanitidis2021pulling-006
- The authors propose shifting focus from the observation space to the parameter space of the decoder distribution, leveraging classical information geometry metrics. (Arvanitidis et al., 2021) `ev:asserted` p. 3 ^arvanitidis2021pulling-007
- A known information geometry result states the Fisher-Rao metric is the second order approximation of the KL-divergence between perturbed distributions. (Arvanitidis et al., 2021) `ev:cited` p. 3 ^arvanitidis2021pulling-008
- The central idea considers the decoder as a map from latent space to parameter space, equipped with the appropriate Fisher-Rao metric. (Arvanitidis et al., 2021) `ev:asserted` p. 4 ^arvanitidis2021pulling-009
- For an immersion parametrizing the likelihood, the [[Pullback metric|latent pullback metric]] is the Jacobian transpose times the Fisher-Rao matrix times the Jacobian. (Arvanitidis et al., 2021) `ev:computed` p. 4 ^arvanitidis2021pulling-010
- The [[Pullback metric|pullback metric]] is identical to the Fisher-Rao metric obtained when the latent variable is treated as the model parameters. (Arvanitidis et al., 2021) `ev:computed` p. 4 ^arvanitidis2021pulling-011
- The authors argue the approach applies to any type of decoders, as distances are measured over the manifold spanned in parameter space. (Arvanitidis et al., 2021) `ev:asserted` p. 4 ^arvanitidis2021pulling-012
- To keep shortest paths within the data support, the decoder is designed to extrapolate to uncertain distributions outside that support. (Arvanitidis et al., 2021) `ev:reported` p. 4 ^arvanitidis2021pulling-013
- With an isotropic Gaussian likelihood, the minimal-length curve in parameter space does not take the given data into account. (Arvanitidis et al., 2021) `ev:measured` p. 4 ^arvanitidis2021pulling-014
- Solving the geodesic ODE system requires inordinate computational resources, since its evaluation relies on the decoder Jacobian plus its derivatives. (Arvanitidis et al., 2021) `ev:asserted` p. 4 ^arvanitidis2021pulling-015
- The curve energy is proportional to a sum of KL divergences between consecutive points along a finely discretized latent curve. (Arvanitidis et al., 2021) `ev:computed` p. 4 ^arvanitidis2021pulling-016
- Shortest-path curves are represented as cubic splines with fixed end-points, whose KL-based energy is minimized by standard free-form optimization. (Arvanitidis et al., 2021) `ev:reported` p. 4 ^arvanitidis2021pulling-017
- For categorical decoders, the Fisher-Rao distance on the simplex coincides with the spherical distance between square-rooted parameters on the unit sphere. (Arvanitidis et al., 2021) `ev:computed` p. 5 ^arvanitidis2021pulling-018
- Inspired by black-box variational inference, the authors propose black-box random geometry, which assumes access to a differentiable KL divergence for the decoder. (Arvanitidis et al., 2021) `ev:asserted` p. 5 ^arvanitidis2021pulling-019
- Without a closed-form KL divergence, Monte Carlo estimates using the reparametrization trick still provide derivatives through automatic differentiation. (Arvanitidis et al., 2021) `ev:reported` p. 5 ^arvanitidis2021pulling-020
- Computing the Fisher-Rao metric as the KL Hessian fares poorly with current automatic differentiation tools, where higher-order derivatives are often incompatible with batching. (Arvanitidis et al., 2021) `ev:asserted` p. 5 ^arvanitidis2021pulling-021
- Each diagonal latent metric element is approximated as twice the KL divergence under a small basis perturbation, divided by epsilon squared. (Arvanitidis et al., 2021) `ev:computed` p. 5 ^arvanitidis2021pulling-022
- Off-diagonal metric elements are approximated from the KL of a paired perturbation minus each single-perturbation KL, divided by epsilon squared. (Arvanitidis et al., 2021) `ev:computed` p. 5 ^arvanitidis2021pulling-023
- Uncertainty regularization in the Euclidean versus Fisher-Rao comparison used transition networks to ensure high uncertainty outside the support of the data. (Arvanitidis et al., 2021) `ev:reported` p. 5 ^arvanitidis2021pulling-024
- To compare pullbacks, four VAEs were trained on a subset of MNIST composed of the digits with label 1. (Arvanitidis et al., 2021) `ev:reported` p. 6 ^arvanitidis2021pulling-025
- Two of these VAEs used Gaussian decoders with the Euclidean metric pulled back through the decoder Jacobian. (Arvanitidis et al., 2021) `ev:reported` p. 6 ^arvanitidis2021pulling-026
- The other two VAEs approximated the pullback of the Fisher-Rao metric by using the KL divergence locally. (Arvanitidis et al., 2021) `ev:reported` p. 6 ^arvanitidis2021pulling-027
- The [[Pullback metric|Fisher-Rao pullback]] was on par with the existing Euclidean pullback in learning geometric structure on the MNIST ones. (Arvanitidis et al., 2021) `ev:measured` p. 6 ^arvanitidis2021pulling-028
- Uncertainty regularization played an instrumental role in learning a sensible geometric structure, for the Euclidean as well as the Fisher-Rao pullback. (Arvanitidis et al., 2021) `ev:measured` p. 6 ^arvanitidis2021pulling-029
- The toy experiment pulled back Fisher-Rao metrics from Normal, Bernoulli, Beta, Dirichlet, Exponential distributions onto noisy circular two-dimensional latent data. (Arvanitidis et al., 2021) `ev:reported` p. 6 ^arvanitidis2021pulling-030
- The approximated pulled-back metric induced a meaningful geometry in the toy latent space, recovering the true circular structure of the data. (Arvanitidis et al., 2021) `ev:measured` p. 6 ^arvanitidis2021pulling-031
- In the toy experiment with the Bernoulli distribution, the authors notice that some of the shortest paths fail to converge. (Arvanitidis et al., 2021) `ev:measured` p. 7 ^arvanitidis2021pulling-032
- The authors hypothesize the regularization is not strong enough, since Bernoulli distributions with parameters close to 1/2 are already highly entropic. (Arvanitidis et al., 2021) `ev:asserted` p. 7 ^arvanitidis2021pulling-033
- For human motion capture, the authors build a VAE whose decoder distribution is a product of von Mises-Fisher distributions. (Arvanitidis et al., 2021) `ev:reported` p. 7 ^arvanitidis2021pulling-034
- The motion capture data tracked 26 different bones, so the VAE decodes to a product of 26 von Mises-Fisher distributions. (Arvanitidis et al., 2021) `ev:reported` p. 20 ^arvanitidis2021pulling-035
- Because the von Mises-Fisher KL has no closed-form expression, the authors resort to a Monte Carlo estimate with off-the-shelf tools. (Arvanitidis et al., 2021) `ev:reported` p. 7 ^arvanitidis2021pulling-036
- On the CMU walking sequence 69_06, the computed latent shortest paths follow the trend of the data. (Arvanitidis et al., 2021) `ev:measured` p. 7 ^arvanitidis2021pulling-037
- The latent shortest paths reflect the underlying periodic nature of the observed walking motion, as seen in the figure. (Arvanitidis et al., 2021) `ev:measured` p. 7 ^arvanitidis2021pulling-038
- Sampling along the straight latent line between two random points traverses uncharted territory, ending up creating an implausible motion. (Arvanitidis et al., 2021) `ev:measured` p. 7 ^arvanitidis2021pulling-039
- Sampling along the shortest path between the same two latent points consistently generates meaningful poses, in contrast to the line. (Arvanitidis et al., 2021) `ev:measured` p. 7 ^arvanitidis2021pulling-040
- On the von Mises-Fisher latent grid, the approximate metric appears well-estimated both within and outside the support of the data. (Arvanitidis et al., 2021) `ev:measured` p. 7 ^arvanitidis2021pulling-041
- The metric approximation error grows at the support boundaries, where the distribution changes from concentrated von Mises-Fisher to uniform. (Arvanitidis et al., 2021) `ev:measured` p. 7 ^arvanitidis2021pulling-042
- Some approximated metrics have negative determinant, showing that the numerical approximations are imprecise at the boundary of the support. (Arvanitidis et al., 2021) `ev:measured` p. 7 ^arvanitidis2021pulling-043
- A locally adaptive normal distribution was fitted in latent space, requiring normalization according to the measure induced by the approximated metric. (Arvanitidis et al., 2021) `ev:reported` p. 7 ^arvanitidis2021pulling-044
- The fitted LAND density follows the data, since shortest paths under the approximated Riemannian metric also follow the data. (Arvanitidis et al., 2021) `ev:measured` p. 8 ^arvanitidis2021pulling-045
- A Bernoulli VAE modeled whether MovieLens 25M users had watched each of the 60 most popular movies in the dataset. (Arvanitidis et al., 2021) `ev:reported` p. 8 ^arvanitidis2021pulling-046
- The preprocessed MovieLens dataset is composed of 10000 users rating whether they have seen some of 60 selected movies. (Arvanitidis et al., 2021) `ev:reported` p. 21 ^arvanitidis2021pulling-047
- Along the pulled-back Fisher-Rao shortest path, decoded users follow others with similar movie preferences, as cosine similarity is only locally high. (Arvanitidis et al., 2021) `ev:measured` p. 8 ^arvanitidis2021pulling-048
- The linear latent interpolation between the same two points failed to capture a local notion of movie preference. (Arvanitidis et al., 2021) `ev:measured` p. 8 ^arvanitidis2021pulling-049
- The authors suggest other geometries over distributions, such as the Wasserstein geometry, may apply equally well as Fisher-Rao. (Arvanitidis et al., 2021) `ev:asserted` p. 9 ^arvanitidis2021pulling-050
- The largest practical hurdle is that the proposed methodology only works well for decoders with well-calibrated uncertainties. (Arvanitidis et al., 2021) `ev:asserted` p. 9 ^arvanitidis2021pulling-051
- The decoder should yield high entropy in regions of little training data to ensure shortest paths follow the trend of the data. (Arvanitidis et al., 2021) `ev:asserted` p. 9 ^arvanitidis2021pulling-052
- Uncertainty regularization trains KMeans on encoded training latent codes, using distance to cluster centers as a proxy for closeness to data. (Arvanitidis et al., 2021) `ev:reported` p. 17 ^arvanitidis2021pulling-053
- For the Normal distribution, the approximated metric's relative Frobenius error was εr = 5.32 · 10−4 ± 9.63 · 10−4. (Arvanitidis et al., 2021) `ev:measured` p. 21 ^arvanitidis2021pulling-054
- For the Beta distribution, the approximated metric's relative Frobenius error was εr = 1.73 · 10−5 ± 1.17 · 10−5. (Arvanitidis et al., 2021) `ev:measured` p. 21 ^arvanitidis2021pulling-055
- Approximating each diagonal metric element requires one KL divergence, costing two forward passes through the decoder network. (Arvanitidis et al., 2021) `ev:computed` p. 22 ^arvanitidis2021pulling-056
- Each off-diagonal metric element requires computing the KL three times, which corresponds to six forward passes through the decoder network. (Arvanitidis et al., 2021) `ev:computed` p. 22 ^arvanitidis2021pulling-057
- Fitting the LAND with Monte Carlo KL metric approximations is prohibited by computational cost, for example with a von Mises-Fisher likelihood. (Arvanitidis et al., 2021) `ev:asserted` p. 23 ^arvanitidis2021pulling-058

## 🎯 Contributions

## 📖 Glossary

- **Pullback metric** — Latent-space metric obtained by mapping tangent vectors through the decoder Jacobian into a metric space.
- **Fisher-Rao metric** — Riemannian metric on a distribution's parameter space, the expected outer product of score functions.
- **Statistical manifold** — Parameter space of a density family equipped with the Fisher-Rao information matrix.
- **Identifiability problem** — Different latent representations giving equally good density estimates, making latent coordinates arbitrary.
- **Black-box random geometry** — Computing latent shortest paths and metrics using only a differentiable KL divergence of the decoder.
- **Uncertainty regularization** — Forcing the decoder to output maximum-uncertainty distributions far from training latent codes.
- **LAND** — Locally adaptive normal distribution: a Gaussian generalized to learned Riemannian manifolds.
- **Curve energy** — Integral of squared speed under the metric; its minimizers are shortest paths.

## ❓ Open questions

- How can decoder uncertainties be calibrated in a principled way, beyond current heuristics, so shortest paths follow the data?
- Are there more stable numerical approximations of the pulled-back metric near the boundary of the data support?
- Would the Wasserstein geometry, or divergences other than the KL, give better latent geometries than Fisher-Rao?
- How can the Bernoulli uncertainty regularization be strengthened so all shortest paths converge?
- Can the Monte Carlo metric approximation be made cheap enough to fit models like the LAND directly?

## 📝 Notes on reading

The version read is arXiv 2106.05367v2 (23 Apr 2022), which carries the AISTATS 2022 (PMLR 151) proceedings header; the packet year is 2021.

Inconsistencies inside the paper: Proposition 3.1 (p. 3) calls the Fisher-Rao metric the second order approximation of the KL-divergence, while Proposition A.1 (p. 11) calls it the first order approximation with the same formula. The MovieLens user filter reads less than 30 movies (p. 8), more than two and less than 30 (Table 6, p. 21), and between 2 and 30 (Sec. D.6, p. 22). Sec. D.5 (p. 21) says Proposition A.1 shows the system of equations for the metric approximation, which is Proposition 3.4 / C.4. Table 3 (p. 19) gives MNIST layers as Linear(728, 2) and Linear(2, 728).

Figures described only: Fig. 1 (random manifold in observation space vs deterministic manifold in distribution space), Fig. 2 (conceptual Gaussian manifold), Fig. 3 (latent shortest path vs minimal-length curve in H), Fig. 4 (four MNIST latent spaces with volume measure and geodesics), Fig. 5 (toy latent spaces for five distributions), Fig. 6 (motion capture geodesics and decoded poses), Fig. 7 (metric approximation error, LAND density), Fig. 8 (movie-preference cosine similarities), Fig. 9 (view counts). The extracted equations of the von Mises-Fisher Fisher-Rao matrix (p. 13) and the Python curve_energy listing (pp. 18-19) are partly garbled; no numbers were claimed from them.

## Suggested new concepts

- Pullback metric — core construction for latent geometries of generative models, reused across many latent-geometry papers.
- Fisher-Rao metric — the reference metric of information geometry used here to generalize latent geometry beyond Gaussian decoders.
- Uncertainty regularization for decoders — calibrated decoder uncertainty is the stated main practical requirement for latent geodesics to follow data.
- Black-box random geometry — a distribution-agnostic recipe for latent shortest paths from KL divergences alone.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** Tira hacia atrás la métrica de Fisher-Rao al latente para cualquier decodificador y une la geometría latente con el gradiente natural del corpus.
