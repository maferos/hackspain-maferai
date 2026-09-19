---
aliases: []
type: "source"
title: "Riemannian Diffusion Models"
citekey: "Huang2022riemannian"
doi: "10.48550/arXiv.2208.07949"
arxiv: "2208.07949"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2208.07949"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Chin-Wei Huang", "Milad Aghajohari", "Avishek Joey Bose", "Prakash Panangaden", "Aaron Courville"]
sha256: ["4e8afee838bcecb6f4d17cccf6def0a29b558413447faf8ef37bbbc9f1ed6b2d"]
pdf: "Content/Papers/Huang2022riemannian.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Huang2022riemannian.pdf]]

> [!abstract] One-sentence summary
> The paper extends continuous-time diffusion models to arbitrary embedded Riemannian manifolds with a variational likelihood bound, ambient-space divergence estimators and a proof of equivalence to Riemannian score matching, reporting lower test NLL than prior manifold generative models on spheres and tori.

## Abstract

Diffusion models are recent state-of-the-art methods for image generation and likelihood estimation. In this work, we generalize continuous-time diffusion models to arbitrary Riemannian manifolds and derive a variational framework for likelihood estimation. Computationally, we propose new methods for computing the Riemannian divergence which is needed in the likelihood estimation. Moreover, in generalizing the Euclidean case, we prove that maximizing this variational lower-bound is equivalent to Riemannian score matching. Empirically, we demonstrate the expressive power of Riemannian diffusion models on a wide spectrum of smooth manifolds, such as spheres, tori, hyperboloids, and orthogonal groups. Our proposed method achieves new state-of-the-art likelihoods on all benchmarks. (arXiv)

## 🧠 Key ideas (atomic)

- The paper generalizes continuous-time diffusion models to arbitrary Riemannian manifolds, calling the resulting model class [[Riemannian diffusion models|Riemannian Diffusion Models]] (RDM). (Huang et al., 2022) `ev:asserted` p. 1 ^huang2022riemannian-001
- [[Riemannian diffusion models|RDM]] uses the Stratonovich SDE formulation, for which the conventional chain rule of calculus holds, unlike the Itô formulation used in Euclidean diffusion. (Huang et al., 2022) `ev:asserted` p. 3 ^huang2022riemannian-002
- The authors take an extrinsic view, defining the manifold of interest as a submanifold embedded in a higher-dimensional Euclidean ambient space. (Huang et al., 2022) `ev:asserted` p. 2 ^huang2022riemannian-003
- The authors state that defining the SDEs in ambient-space coordinates greatly simplifies the implementation of the theory developed using the intrinsic view. (Huang et al., 2022) `ev:asserted` p. 2 ^huang2022riemannian-004
- The embedding assumption loses no generality, since any Riemannian manifold can be isometrically embedded into a Euclidean space by the Nash embedding theorem. (Huang et al., 2022) `ev:cited` p. 3 ^huang2022riemannian-005
- Theorem 1 gives a stochastic instantaneous change-of-variable formula for the Riemannian SDE density by applying Feynman-Kac to the Fokker Planck equation. (Huang et al., 2022) `ev:computed` p. 3 ^huang2022riemannian-006
- Theorem 2 derives a Riemannian continuous-time ELBO from Girsanov's change of measure and Jensen's inequality, which serves as the training objective. (Huang et al., 2022) `ev:computed` p. 4 ^huang2022riemannian-007
- The authors state that their Riemannian CT-ELBO strictly generalizes the Euclidean CT-ELBO previously introduced by Huang et al. (2021). (Huang et al., 2022) `ev:asserted` p. 2 ^huang2022riemannian-008
- Proposition 1 shows that on an embedded submanifold the Riemannian divergence equals the trace of the ambient Jacobian sandwiched between tangential projections. (Huang et al., 2022) `ev:computed` p. 4 ^huang2022riemannian-009
- Intrinsic-coordinate divergence estimation, as used by Mathieu and Nickel, requires local coordinates that may be difficult to obtain for some manifolds. (Huang et al., 2022) `ev:asserted` p. 4 ^huang2022riemannian-010
- The authors note that in intrinsic methods the inverse scaling by the metric volume term might result in numerical instability and high variance. (Huang et al., 2022) `ev:asserted` p. 4 ^huang2022riemannian-011
- Rozen et al. showed that the Riemannian divergence equals the ambient Euclidean divergence when the vector field is built with the closest-point projection. (Huang et al., 2022) `ev:cited` p. 4 ^huang2022riemannian-012
- The authors note that the closest-point projection map required by the Moser Flow approach may not always be easily obtained. (Huang et al., 2022) `ev:asserted` p. 5 ^huang2022riemannian-013
- The QR-based method builds an orthogonal tangent basis by projecting d random ambient vectors onto the tangent space and applying a QR decomposition. (Huang et al., 2022) `ev:reported` p. 5 ^huang2022riemannian-014
- With the QR basis the divergence reduces to a sum of d vector-Jacobian products, each computable in O(m) time with reverse-mode autograd. (Huang et al., 2022) `ev:computed` p. 5 ^huang2022riemannian-015
- The authors state that the QR-based divergence computation does not require the closest-point projection onto the manifold. (Huang et al., 2022) `ev:asserted` p. 5 ^huang2022riemannian-016
- When QR is too expensive, a projected Hutchinson estimator projects a Gaussian or Rademacher vector onto the tangent subspace before applying the trace estimator. (Huang et al., 2022) `ev:reported` p. 5 ^huang2022riemannian-017
- The paper presents the projected Hutchinson method as a scalable unbiased estimator of the Riemannian divergence of the parametrized vector field. (Huang et al., 2022) `ev:asserted` p. 2 ^huang2022riemannian-018
- The inference SDE is fixed to a Riemannian Langevin diffusion whose drift is half the Riemannian gradient of the log prior density. (Huang et al., 2022) `ev:reported` p. 5 ^huang2022riemannian-019
- If the prior satisfies a log-Sobolev inequality, the marginal of the inference process converges to the prior at a linear rate in KL divergence. (Huang et al., 2022) `ev:cited` p. 5 ^huang2022riemannian-020
- For compact manifolds the prior is set to the uniform density, which reduces the inference SDE to the extrinsic construction of Brownian motion. (Huang et al., 2022) `ev:reported` p. 5 ^huang2022riemannian-021
- With the fixed-inference parameterization, inference samples can be drawn cheaply by numerical integration without requiring a stringent error tolerance. (Huang et al., 2022) `ev:asserted` p. 5 ^huang2022riemannian-022
- Proposition 2 proves that the drift correction term vanishes when the diffusion matrix is the tangential projection, which simplifies the Riemannian CT-ELBO. (Huang et al., 2022) `ev:computed` p. 5 ^huang2022riemannian-023
- Variance is reduced by importance sampling the time integral, using a proposal density on the time interval parameterized by a 1D monotone flow. (Huang et al., 2022) `ev:reported` p. 6 ^huang2022riemannian-024
- Since the objective's gradient with respect to the proposal is zero in expectation, the proposal is instead trained to minimize the estimator's second moment. (Huang et al., 2022) `ev:computed` p. 6 ^huang2022riemannian-025
- The authors state that importance sampling over the time integral avoids carefully designing the noise schedule of the inference process. (Huang et al., 2022) `ev:asserted` p. 2 ^huang2022riemannian-026
- Theorem 3 constructs a family of inference and generative SDEs, indexed by lambda, that induce the same marginal densities when the score is known. (Huang et al., 2022) `ev:computed` p. 6 ^huang2022riemannian-027
- Setting lambda equal to 1 in the marginally equivalent family of SDEs gives rise to an equivalent ordinary differential equation. (Huang et al., 2022) `ev:computed` p. 6 ^huang2022riemannian-028
- Theorem 4 shows that maximizing the Riemannian CT-ELBO of the plug-in reverse process is equivalent to minimizing the Riemannian score-matching loss. (Huang et al., 2022) `ev:computed` p. 7 ^huang2022riemannian-029
- With lambda set to 0, the vector trained by the fixed-inference objective is an approximate score, allowing extraction of an equivalent ODE. (Huang et al., 2022) `ev:computed` p. 7 ^huang2022riemannian-030
- The authors describe Euclidean maximum-likelihood continuous-time diffusion models as the flat-geometry special case that their theory completely generalizes. (Huang et al., 2022) `ev:asserted` p. 7 ^huang2022riemannian-031
- Unlike the concurrent Riemannian score-based generative models of De Bortoli et al., [[Riemannian diffusion models|RDMs]] are couched within the maximum likelihood framework. (Huang et al., 2022) `ev:asserted` p. 7 ^huang2022riemannian-032
- The authors state that their approach is also applicable to non-compact manifolds such as hyperbolic spaces, which they demonstrate in experiments. (Huang et al., 2022) `ev:asserted` p. 7 ^huang2022riemannian-033
- In the experiments the variational function a is parametrized by an MLP and trained by maximizing the simplified Riemannian CT-ELBO. (Huang et al., 2022) `ev:reported` p. 7 ^huang2022riemannian-034
- Spherical experiments model earth-science event datasets of volcanoes, earthquakes, floods and fires compiled by Mathieu and Nickel. (Huang et al., 2022) `ev:reported` p. 7 ^huang2022riemannian-035
- The earth datasets contain 827 volcano, 6120 earthquake, 4875 flood and 12809 fire records according to the dataset-size row of Table 1. (Huang et al., 2022) `ev:reported` p. 8 ^huang2022riemannian-036
- Earth-dataset test NLL means and standard deviations are computed over 5 runs with different splits of each dataset. (Huang et al., 2022) `ev:reported` p. 8 ^huang2022riemannian-037
- The baseline NLL values in the earth-dataset table are taken from De Bortoli et al. (2022), as the table caption states. (Huang et al., 2022) `ev:cited` p. 8 ^huang2022riemannian-038
- On the volcano dataset RDM obtains a test NLL of −6.61±0.97, lower than −5.56±0.26 for Riemannian score-based models. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022riemannian-039
- On the earthquake dataset RDM obtains a test NLL of −0.40±0.05, lower than −0.21±0.03 for Riemannian score-based models. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022riemannian-040
- On the flood dataset RDM obtains a test NLL of 0.43±0.07, lower than 0.52±0.02 for Riemannian score-based models. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022riemannian-041
- On the fire dataset RDM obtains a test NLL of −1.38±0.05, lower than −1.24±0.07 for Riemannian score-based models. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022riemannian-042
- On the earthquake dataset, learning an importance sampling proposal effectively lowers the variance of Riemannian CT-ELBO optimization, as shown in Figure 2. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022riemannian-043
- On the earthquake dataset, learning an importance sampling proposal also speeds up training of the Riemannian CT-ELBO, according to Figure 2. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022riemannian-044
- Toroidal experiments use 500 high-resolution proteins compiled by Lovell et al. and 113 RNA sequences listed by Murray et al. (Huang et al., 2022) `ev:reported` p. 8 ^huang2022riemannian-045
- Protein backbone conformation is modelled on a 2D torus after discarding the one torsion angle that is normally 180°. (Huang et al., 2022) `ev:reported` p. 8 ^huang2022riemannian-046
- Each RNA nucleotide is described by 7 backbone torsion angles, so the RNA density is modelled on a 7D torus. (Huang et al., 2022) `ev:reported` p. 8 ^huang2022riemannian-047
- The protein data are divided by the type of side chain attached to the amino acid, resulting in 4 separate datasets. (Huang et al., 2022) `ev:reported` p. 8 ^huang2022riemannian-048
- The authors observe that [[Riemannian diffusion models|RDM]] outperforms the mixture of power spherical distributions baseline across all the toroidal datasets. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022riemannian-049
- The advantage of RDM over the power spherical mixture baseline is most noticeable for the RNA data, which has higher dimensionality. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022riemannian-050
- On the RNA torus dataset RDM obtains a test NLL of −3.70±0.592, compared with 4.08±0.368 for the MoPS baseline. (Huang et al., 2022) `ev:measured` p. 9 ^huang2022riemannian-051
- On the General protein dataset RDM obtains a test NLL of 1.04±0.012, compared with 1.15±0.002 for the MoPS baseline. (Huang et al., 2022) `ev:measured` p. 9 ^huang2022riemannian-052
- On the Proline dataset RDM obtains a test NLL of 0.12±0.011, compared with 0.27±0.008 for the MoPS baseline. (Huang et al., 2022) `ev:measured` p. 9 ^huang2022riemannian-053
- In the Glycine integration ablation, using fewer numerical time steps tends to underestimate the loss relative to direct Brownian motion sampling. (Huang et al., 2022) `ev:measured` p. 9 ^huang2022riemannian-054
- In the Glycine ablation, the model trained with 100 integration time steps is already indistinguishable from the one trained with direct sampling. (Huang et al., 2022) `ev:measured` p. 9 ^huang2022riemannian-055
- The authors find numerical integration is not a significant overhead, since experiments take approximately the same wall-clock time with identical setups. (Huang et al., 2022) `ev:measured` p. 9 ^huang2022riemannian-056
- The authors attribute the low integration overhead to the inference path not involving the neural module a. (Huang et al., 2022) `ev:asserted` p. 9 ^huang2022riemannian-057
- The Lorentz-norm projection onto the hyperboloid is not the closest-point projection in Euclidean distance, contrary to the claim made by Skopek et al. (Huang et al., 2022) `ev:computed` p. 31 ^huang2022riemannian-058
- Hyperbolic experiments model synthetic datasets first introduced by Bose et al. and Lou et al. to demonstrate the generality of the framework. (Huang et al., 2022) `ev:reported` p. 9 ^huang2022riemannian-059
- For the non-compact hyperbolic manifold, the prior is a standard normal on the yz-plane with a drift so that inference samples revert to the origin. (Huang et al., 2022) `ev:reported` p. 9 ^huang2022riemannian-060
- On the hyperboloid the model learns the density with respect to the Euclidean-induced metric, which relates to the Lorentzian density by a volume change. (Huang et al., 2022) `ev:reported` p. 30 ^huang2022riemannian-061
- The SO(3) experiment uses the synthetic multimodal density from Brofos et al., viewing the group as a submanifold embedded in 3×3 matrices. (Huang et al., 2022) `ev:reported` p. 9 ^huang2022riemannian-062
- For the hyperbolic experiments an ActNorm layer is added to the first MLP layer, which the authors find adds extra numerical stability. (Huang et al., 2022) `ev:reported` p. 33 ^huang2022riemannian-063
- Gradients are disconnected from the numerical solver, which yields slightly biased variance-minimization updates while still giving substantial variance reduction. (Huang et al., 2022) `ev:asserted` p. 33 ^huang2022riemannian-064
- All experiments run on a single NVIDIA Tesla V100 or Quadro RTX 8000 GPU for a maximum of 30 hours. (Huang et al., 2022) `ev:reported` p. 33 ^huang2022riemannian-065
- Models are evaluated with an importance-weighted bound called KELBO using K = 100 samples, which is tighter than the Riemannian CT-ELBO. (Huang et al., 2022) `ev:reported` p. 34 ^huang2022riemannian-066
- The authors experimented with K up to 1000 and found the results stop changing much for K above 100. (Huang et al., 2022) `ev:measured` p. 34 ^huang2022riemannian-067
- SDEs are integrated with the Stratonovich-Heun method, each iteration followed by a closest-point projection back onto the manifold. (Huang et al., 2022) `ev:reported` p. 34 ^huang2022riemannian-068
- The authors acknowledge their numerical integration and divergence estimation choices may not apply out of the box to higher dimensional problems. (Huang et al., 2022) `ev:asserted` p. 13 ^huang2022riemannian-069

## 🎯 Contributions

## 📖 Glossary

- **Riemannian CT-ELBO** — Continuous-time evidence lower bound on log-likelihood for diffusions defined on a Riemannian manifold.
- **Riemannian divergence** — Divergence of a vector field computed with respect to the manifold metric and volume.
- **Tangential projection** — Orthogonal projection of an ambient vector onto the tangent space of an embedded manifold.
- **Closest-point projection** — Map sending an ambient point to the nearest manifold point in Euclidean distance.
- **Stratonovich SDE** — Stochastic differential equation whose integral obeys the ordinary chain rule of calculus.
- **Projected Hutchinson estimator** — Unbiased trace estimator using random vectors projected onto the tangent space.
- **Riemannian Langevin diffusion** — Noise process whose drift is half the Riemannian gradient of the log prior.
- **KELBO** — Importance-weighted lower bound averaging K trajectory likelihoods inside the logarithm.
- **Marginally equivalent SDEs** — Different SDEs that induce the same family of marginal densities over time.
- **MoPS** — Mixture of power spherical distributions, used as the baseline on tori.

## ❓ Open questions

- Do the QR and projected Hutchinson divergence estimators remain accurate and affordable on high-dimensional manifolds, which the authors say may not work out of the box?
- How does RDM compare quantitatively on hyperbolic and SO(3) data, where only qualitative density plots are shown?
- Would learning a time reparameterization reduce variance further than the importance-sampling proposal the authors chose for simplicity?
- How much does the gradient disconnection from the numerical solver bias the importance sampler in practice?
- How large is the gap between the Riemannian CT-ELBO or KELBO and the exact likelihood from the equivalent ODE?

## 📝 Notes on reading

- Version read: arXiv v1 preprint (16 Aug 2022, under review), matching the packet identifier arXiv:2208.07949.
- Table 1 and Table 2 captions say bold marks the best results up to statistical significance, but bolding is lost in the extracted text; the claims compare numbers only. In Table 1 RDM has the lowest mean NLL on all four earth datasets, though the volcano standard deviation (0.97) is large.
- Table 2 also reports Glycine (RDM 1.97±0.012 vs MoPS 2.08±0.009) and Pre-Pro (RDM 1.24±0.004 vs MoPS 1.34±0.019); these rows were not claimed separately to keep the note under the claim cap.
- The MoPS mixture size is printed as 4, 096 in the extraction (likely 4,096 components); it was not claimed.
- Figures 1 to 7 (earth densities, variance-reduction curves, integration ablation, Ramachandran plots, hyperbolic and SO(3) densities, Lorentz projection sketch) could only be described from captions and text.
- Hyperbolic and SO(3) results are qualitative only: no NLL table is given for them, although the abstract claims state-of-the-art likelihoods on all benchmarks.
- Appendix equations and proofs (Theorems 1 to 4, Propositions 1 to 4) are extracted with broken layout; claims describe results, not formulas.
- Hyperparameter Tables 3 and 4 (activations, widths, Adam learning rates) and integration Tables 5 and 6 were read but only summarized; the Orthogonal group row of Table 3 lists 256 hidden layers, possibly an extraction or typesetting error.
- The NeurIPS checklist on pages 13 to 14 still contains template instructions.

## Suggested new concepts

- Riemannian diffusion models — a model family for generative modelling on manifolds that several papers compare against.
- Riemannian divergence estimation — QR, projected Hutchinson, intrinsic and closest-point methods are recurring design choices for manifold likelihoods.
- Closest-point projection — central to Moser Flow and SDE integration on manifolds, and costly for hyperboloids and orthogonal groups.
- Continuous-time ELBO — the variational bound linking diffusion likelihood training to score matching in Euclidean and Riemannian settings.
- Importance sampling over diffusion time — a variance reduction alternative to hand-designed noise schedules.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H2.** Da la formulación variacional (ELBO en tiempo continuo) de la difusión en variedades, complementaria a la visión por score.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
