---
aliases: []
type: "source"
title: "Only Bayes should learn a manifold (on the estimation of differential geometric structure from data)"
citekey: "Hauberg2018only"
doi: "10.48550/arXiv.1806.04994"
arxiv: "1806.04994"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1806.04994"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Søren Hauberg"]
sha256: ["cb96a894f5700fb43cb2c1fc2314cdd1a8c6e5f731d7e057bb3898fe63f26f23"]
pdf: "Content/Papers/Hauberg2018only.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Hauberg2018only.pdf]]

> [!abstract] One-sentence summary
> The paper shows that manifold learners without uncertainty quantification cannot recover the pull-back Riemannian geometry of data away from observations, whereas Gaussian process models can, and it sketches an elementary geometry of stochastic Riemannian metrics.

## Abstract

We investigate learning of the differential geometric structure of a data manifold embedded in a high-dimensional Euclidean space. We first analyze kernel-based algorithms and show that under the usual regularizations, non-probabilistic methods cannot recover the differential geometric structure, but instead find mostly linear manifolds or spaces equipped with teleports. To properly learn the differential geometric structure, non-probabilistic methods must apply regularizations that enforce large gradients, which go against common wisdom. We repeat the analysis for probabilistic methods and find that under reasonable priors, the geometric structure can be recovered. Fully exploiting the recovered structure, however, requires the development of stochastic extensions to classic Riemannian geometry. We take early steps in that regard. Finally, we partly extend the analysis to modern models based on neural networks, thereby highlighting geometric and probabilistic shortcomings of current deep generative models. (arXiv)

## 🧠 Key ideas (atomic)

- The paper argues that most manifold learning schemes do not support elementary operations such as interpolation, distances and measure. (Hauberg, 2018) `ev:asserted` p. 1 ^hauberg2018only-001
- Embedding methods fundamentally describe the data manifold only at observed data points, making the learned representation space a discrete space. (Hauberg, 2018) `ev:asserted` p. 2 ^hauberg2018only-002
- A smooth invertible rotation that preserves a unit Gaussian latent distribution can substantially change pairwise Euclidean distances in a VAE latent space. (Hauberg, 2018) `ev:computed` p. 2 ^hauberg2018only-003
- Because the VAE gives no guarantee on which latent space is recovered, Euclidean latent distances and straight-line interpolations are effectively arbitrary. (Hauberg, 2018) `ev:asserted` p. 2 ^hauberg2018only-004
- The analysis shows that even with infinite noise-free data, a non-probabilistic estimate of the mapping cannot recover the true Riemannian structure. (Hauberg, 2018) `ev:computed` p. 2 ^hauberg2018only-005
- The key finding is that uncertainty quantification is a prerequisite for learning an operational representation, as the usual smoothness regularization introduces a harmful bias. (Hauberg, 2018) `ev:asserted` p. 2 ^hauberg2018only-006
- The [[Pullback metric|pull-back metric]] is defined as the Jacobian Gram matrix of the mapping scaled by 1/D, giving a local latent inner product. (Hauberg, 2018) `ev:asserted` p. 3 ^hauberg2018only-007
- The [[Pullback metric|pull-back metric]] is invariant to reparametrizations of the manifold because it corresponds to the data-space inner product measured locally on the manifold. (Hauberg, 2018) `ev:asserted` p. 3 ^hauberg2018only-008
- The guiding example draws data uniformly on a unit circle, nonlinearly embeds it in a 1000-dimensional space, and adds Gaussian noise. (Hauberg, 2018) `ev:reported` p. 4 ^hauberg2018only-009
- With a universal kernel and infinite data, kernel ridge regression recovers the true pull-back metric near the training data. (Hauberg, 2018) `ev:computed` p. 4 ^hauberg2018only-010
- With a Gaussian kernel, both the kernel ridge regression mapping and its pull-back metric tend to zero far from the data. (Hauberg, 2018) `ev:computed` p. 5 ^hauberg2018only-011
- In the guiding example, geodesics under the Gaussian-kernel ridge regression metric systematically shy away from the data. (Hauberg, 2018) `ev:measured` p. 5 ^hauberg2018only-012
- Data-free latent regions act as teleports, since moving through regions where the metric is zero costs nothing in length. (Hauberg, 2018) `ev:asserted` p. 5 ^hauberg2018only-013
- Adding a linear term to the Gaussian kernel makes the metric far from the data a scaled Euclidean metric, implying a flat learned manifold. (Hauberg, 2018) `ev:computed` p. 5 ^hauberg2018only-014
- In the guiding example, geodesics under the Gaussian plus linear kernel are almost straight lines, so the data structure is not recovered. (Hauberg, 2018) `ev:measured` p. 5 ^hauberg2018only-015
- Girosi et al. showed that most regularizers are low-pass filters that avoid wiggly regression functions. (Hauberg, 2018) `ev:cited` p. 5 ^hauberg2018only-016
- For geodesics to stay on the manifold, the author argues that the [[Pullback metric|pull-back metric]] must take large values away from the data. (Hauberg, 2018) `ev:asserted` p. 5 ^hauberg2018only-017
- A loose sufficient condition is that the smallest metric eigenvalue away from data tends to the squared manifold radius. (Hauberg, 2018) `ev:computed` p. 6 ^hauberg2018only-018
- Regularizing towards large derivatives goes against common wisdom, since functions with large derivatives in regions of little data are generally unstable. (Hauberg, 2018) `ev:asserted` p. 6 ^hauberg2018only-019
- The smoother the assumptions on the mapping, the more geodesics are drawn away from the data, off the manifold. (Hauberg, 2018) `ev:asserted` p. 6 ^hauberg2018only-020
- The author concludes that one must choose between giving up correct manifold geometry and giving up stable learning, neither being desirable. (Hauberg, 2018) `ev:asserted` p. 6 ^hauberg2018only-021
- The Bayesian setting models the mapping as component-wise conditionally independent Gaussian processes, which is a Gaussian process latent variable model. (Hauberg, 2018) `ev:reported` p. 6 ^hauberg2018only-022
- Under the Gaussian process model, the [[Pullback metric|stochastic pull-back metric]] follows a non-central Wishart distribution at each latent point. (Hauberg, 2018) `ev:cited` p. 7 ^hauberg2018only-023
- The variance of each metric entry vanishes at rate 1/D, so in high dimensions the stochastic metric becomes deterministic. (Hauberg, 2018) `ev:computed` p. 7 ^hauberg2018only-024
- With a Gaussian kernel, the expected metric coincides with the true pull-back metric near the data. (Hauberg, 2018) `ev:computed` p. 7 ^hauberg2018only-025
- Away from data, the expected metric adds an isotropic term equal to the product of the Gaussian kernel parameters. (Hauberg, 2018) `ev:computed` p. 7 ^hauberg2018only-026
- In the guiding example, geodesics under the Gaussian process expected metric approximately follow circular arcs, in line with the theoretical analysis. (Hauberg, 2018) `ev:measured` p. 7 ^hauberg2018only-027
- The author cautions that accurate learning of manifold geometry requires data sampled sufficiently densely on the manifold, so recovery is not guaranteed. (Hauberg, 2018) `ev:asserted` p. 7 ^hauberg2018only-028
- The author argues that uncertainty plays the role of topology, since holes in the manifold can only be seen through uncertainty. (Hauberg, 2018) `ev:asserted` p. 7 ^hauberg2018only-029
- Under a stochastic Euclidean metric, the expected distance grows with both the mean and the variance of the basis. (Hauberg, 2018) `ev:computed` p. 8 ^hauberg2018only-030
- The curve minimizing expected energy over the stochastic manifold is the geodesic under the deterministic expected Riemannian metric. (Hauberg, 2018) `ev:computed` p. 8 ^hauberg2018only-031
- Minimizing expected curve energy balances minimizing expected curve length against minimizing curve variance, rather than minimizing expected length alone. (Hauberg, 2018) `ev:computed` p. 9 ^hauberg2018only-032
- For a zero-mean Gaussian process prior manifold, minimizing expected curve energy also minimizes expected curve length. (Hauberg, 2018) `ev:computed` p. 10 ^hauberg2018only-033
- Under a random metric, the expected integral over the manifold is computed with the expected volume measure. (Hauberg, 2018) `ev:computed` p. 10 ^hauberg2018only-034
- The analysis indicates that the expected measure is perhaps more suitable than the measure of the expected metric suggested by Arvanitidis et al. (Hauberg, 2018) `ev:asserted` p. 10 ^hauberg2018only-035
- For the posterior GP-LVM, the expected volume measure involves a confluent hypergeometric function of the first kind. (Hauberg, 2018) `ev:computed` p. 11 ^hauberg2018only-036
- In the guiding example, the GP-LVM expected volume measure shows no visual difference from the volume measure of the expected metric. (Hauberg, 2018) `ev:measured` p. 11 ^hauberg2018only-037
- The author suggests the simpler volume measure of the expected metric may be a good approximation to the expected volume measure for the GP-LVM. (Hauberg, 2018) `ev:asserted` p. 11 ^hauberg2018only-038
- In the guiding example, geodesics of an autoencoder with a smooth feed-forward mapping are almost straight lines. (Hauberg, 2018) `ev:measured` p. 11 ^hauberg2018only-039
- In VAEs the noise term does not form a smooth process, so sample paths are not smooth and their pull-back metrics can be questioned. (Hauberg, 2018) `ev:asserted` p. 11 ^hauberg2018only-040
- Scaled by D, the VAE expected metric equals the sum of the Gram matrices of the mean and standard deviation network Jacobians. (Hauberg, 2018) `ev:cited` p. 11 ^hauberg2018only-041
- In the guiding example, a naive VAE with smooth feed-forward mean and standard deviation networks yields almost straight geodesics. (Hauberg, 2018) `ev:measured` p. 12 ^hauberg2018only-042
- The author attributes the naive VAE failure to the standard deviation network being a poor proxy for uncertainty, since smooth uncertainty interpolation is nonsensical. (Hauberg, 2018) `ev:asserted` p. 12 ^hauberg2018only-043
- In the guiding example, a VAE whose inverse standard deviation is a positive RBF network recovers the geometry of the data manifold. (Hauberg, 2018) `ev:measured` p. 12 ^hauberg2018only-044
- Unlike for the GP-LVM, the VAE shows significant differences between the measure of the expected metric and the sampled expected measure. (Hauberg, 2018) `ev:measured` p. 12 ^hauberg2018only-045
- The author takes the somewhat arbitrary VAE measures as a hint that the RBF inverse-variance network does not fit the data excellently. (Hauberg, 2018) `ev:asserted` p. 12 ^hauberg2018only-046
- The GP-LVM achieves a correlation of 0.996819 between true and estimated geodesic lengths in the guiding example. (Hauberg, 2018) `ev:measured` p. 12 ^hauberg2018only-047
- The KRM and KRM+ridge kernel methods reach geodesic length correlations of 0.843259 and 0.892995, respectively. (Hauberg, 2018) `ev:measured` p. 12 ^hauberg2018only-048
- The autoencoder, VAE and RBF VAE reach geodesic length correlations of 0.974833, 0.975200 and 0.982504 in the guiding example. (Hauberg, 2018) `ev:measured` p. 12 ^hauberg2018only-049
- The GP-LVM and RBF VAE obtain Hausdorff distances of 0.858773 and 0.788519 between estimated and ground-truth geodesics. (Hauberg, 2018) `ev:measured` p. 12 ^hauberg2018only-050
- Other methods obtain larger Hausdorff distances, from 2.825305 for the autoencoder to 5.443746 for KRM. (Hauberg, 2018) `ev:measured` p. 12 ^hauberg2018only-051
- For deterministic models, short curves correlate better with ground-truth lengths than long curves, consistent with a locally Euclidean Riemannian model. (Hauberg, 2018) `ev:measured` p. 13 ^hauberg2018only-052
- Shao et al. and Chen et al. consider VAE pull-back metrics using only the mean of the mapping, effectively analysing autoencoders. (Hauberg, 2018) `ev:cited` p. 13 ^hauberg2018only-053
- Shao et al. speculated that most data manifolds are flat, which the author argues is most likely incorrect and an artifact of ignoring uncertainty. (Hauberg, 2018) `ev:asserted` p. 13 ^hauberg2018only-054
- The author argues that biasing geodesics towards data works around a deeper problem, as such curves may not be geodesics under any metric. (Hauberg, 2018) `ev:asserted` p. 13 ^hauberg2018only-055
- The author states that methods which do not quantify their uncertainty cannot meaningfully capture the geometry of a data manifold. (Hauberg, 2018) `ev:asserted` p. 13 ^hauberg2018only-056
- The author claims to develop an elementary theory of stochastic Riemannian manifolds, which appears to be the first of its kind. (Hauberg, 2018) `ev:asserted` p. 13 ^hauberg2018only-057
- Since deep generative model sample paths are not continuous, the author suggests enforcing a geometric analysis on them is perhaps not a good idea. (Hauberg, 2018) `ev:asserted` p. 13 ^hauberg2018only-058
- The author states that current deep generative models provide rather poor estimators of uncertainty, which is essential for estimating manifold geometry. (Hauberg, 2018) `ev:asserted` p. 14 ^hauberg2018only-059
- The guiding example uses N = 200 numbers sampled uniformly over the interval [0, 2π] as circle angles. (Hauberg, 2018) `ev:reported` p. 16 ^hauberg2018only-060
- Off-manifold Gaussian noise with standard deviation σ = 0.1 is added to data embedded in a D = 1000 dimensional space. (Hauberg, 2018) `ev:reported` p. 16 ^hauberg2018only-061
- The latent variables are fixed to the first two data dimensions and shared across all models to allow direct comparison. (Hauberg, 2018) `ev:reported` p. 16 ^hauberg2018only-062
- The VAE with RBF precision is less well behaved than the GP-LVM, indicating its variance estimation leaves something to be desired. (Hauberg, 2018) `ev:measured` p. 16 ^hauberg2018only-063

## 🎯 Contributions

## 📖 Glossary

- **Pull-back metric** — Latent-space metric from the mapping's Jacobian, measuring data-space inner products locally.
- **Geodesic** — Locally length-minimizing curve; here a curve of minimal curve energy.
- **Curve energy** — Integral of squared metric speed along a curve; minimizers have constant velocity.
- **Riemannian volume measure** — Square root of the metric determinant, used for integration on manifolds.
- **Teleport** — Data-free latent region where the metric vanishes, letting geodesics move at no cost.
- **Stochastic Riemannian metric** — Random metric induced by a stochastic mapping such as a Gaussian process.
- **Expected metric** — Mean of a stochastic metric; its geodesics minimize expected curve energy.
- **GP-LVM** — Gaussian process latent variable model mapping latent points to data with GPs.
- **Non-central Wishart distribution** — Distribution of Gram matrices of Gaussian matrices with nonzero mean.
- **Hausdorff distance** — Maximum over both curves of distance to the nearest point on the other curve.

## ❓ Open questions

- How large must the metric be away from data to guarantee geodesics stay on the manifold (a tight bound)?
- Which measure, the expected volume measure or the measure of the expected metric, is preferable in practice for VAEs?
- Can smoothness be introduced into deep generative model sample paths without sacrificing computational efficiency?
- What principled methods give deep generative models reliable uncertainty estimates away from data?
- Which curves define the most natural interpolants on a stochastic manifold, given energy and length minimizers differ?
- How does geometry recovery degrade when data is sampled sparsely on the manifold?

## 📝 Notes on reading

The cached text is arXiv 1806.04994v3 (26 Sep 2019), described as the 2nd revision. The registry abstract differs from the abstract printed in this PDF: the registry version adds that non-probabilistic methods must use regularizations enforcing large gradients and says recovery holds under reasonable priors, while the PDF abstract says probabilistic methods naturally recover the structure.

Figures 1, 2, 3, 5, 6 and 7 could only be described: Fig. 3 shows geodesics for Gaussian kernel ridge regression (teleports), Gaussian+linear kernel (near straight), and GP regression (following the circle); Fig. 6 shows geodesics for an autoencoder, a naive VAE, an RBF-precision VAE and its expected measure; Fig. 7 plots ground-truth versus estimated geodesic lengths per model.

Table 1 labels two kernel methods KRM and KRM+ridge, but the text never defines these labels; Fig. 7 names them kernel regression with Gaussian kernel and with Gaussian+linear kernel, so the mapping between labels is not certain and was not claimed.

Many equations (e.g. geodesic ODE 2.7, measures 4.25 and 4.28) are garbled by extraction and were only claimed qualitatively. The kernel analysis assumes noise-free data, while the guiding example adds noise; the author states the analysis also holds under noise.

## Suggested new concepts

- Pull-back metric — central object for defining latent-space geometry of generative models from their decoders.
- Stochastic Riemannian geometry — extends geodesics and integration to random metrics from probabilistic mappings.
- Uncertainty as topology — the idea that predictive uncertainty reveals holes and boundaries of data manifolds.
- Latent space identifiability — reparametrization arbitrariness of VAE latent spaces motivates invariant geometric tools.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** Demuestra que solo los modelos probabilísticos recuperan la geometría diferencial de la variedad de datos, lo que justifica las métricas pullback con incertidumbre para geodésicas de movimiento.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
