---
aliases: []
type: "source"
title: "Latent Space Oddity: on the Curvature of Deep Generative Models"
citekey: "Arvanitidis2017latent"
doi: "10.48550/arXiv.1710.11379"
arxiv: "1710.11379"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1710.11379"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Georgios Arvanitidis", "Lars Kai Hansen", "Søren Hauberg"]
sha256: ["8bde633d5fb0b635e4081926e1684b5589d40c2f82dca95acf7a7ffdcdf2278f"]
pdf: "Content/Papers/Arvanitidis2017latent.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Arvanitidis2017latent.pdf]]

> [!abstract] One-sentence summary
> The paper shows that a stochastic generator induces a Riemannian metric on the latent space of deep generative models, proposes an RBF variance network that keeps this geometry well behaved away from data, and demonstrates better clustering, interpolation, latent densities and random walks on VAEs.

## Abstract

Deep generative models provide a systematic way to learn nonlinear data distributions, through a set of latent variables and a nonlinear "generator" function that maps latent points into the input space. The nonlinearity of the generator imply that the latent space gives a distorted view of the input space. Under mild conditions, we show that this distortion can be characterized by a stochastic Riemannian metric, and demonstrate that distances and interpolants are significantly improved under this metric. This in turn improves probability distributions, sampling algorithms and clustering in the latent space. Our geometric analysis further reveals that current generators provide poor variance estimates and we propose a new generator architecture with vastly improved variance estimates. Results are demonstrated on convolutional and fully connected variational autoencoders, but the formalism easily generalize to other deep generative models. (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that the apparent closeness of cross-class latent points near an MNIST class boundary is a misinterpretation of the latent space. (Arvanitidis et al., 2017) `ev:asserted` p. 1 ^arvanitidis2017latent-001
- The authors state that latent space distances lack physical units, making them difficult to interpret in deep generative models. (Arvanitidis et al., 2017) `ev:asserted` p. 1 ^arvanitidis2017latent-002
- Using Taylor's theorem, the paper shows that infinitesimal squared distances in input space are governed locally by the Jacobian product J⊺J. (Arvanitidis et al., 2017) `ev:computed` p. 1 ^arvanitidis2017latent-003
- The authors argue that the latent space of a deep generative model should be seen as a curved space, not a linear Euclidean space. (Arvanitidis et al., 2017) `ev:asserted` p. 2 ^arvanitidis2017latent-004
- In a synthetic two-class example, the shortest curve on the generator surface is rather different from the straight latent interpolation line. (Arvanitidis et al., 2017) `ev:computed` p. 2 ^arvanitidis2017latent-005
- The paper uses the variational autoencoder as a representative generative model, with a Gaussian likelihood whose mean and variance functions are deep neural networks. (Arvanitidis et al., 2017) `ev:reported` p. 2 ^arvanitidis2017latent-006
- The authors note the VAE objective is difficult because poor mean reconstructions can be explained by increasing the corresponding variance. (Arvanitidis et al., 2017) `ev:asserted` p. 3 ^arvanitidis2017latent-007
- Following a common trick, the authors first optimize the generator mean with constant variance, then finally optimize the variance function. (Arvanitidis et al., 2017) `ev:reported` p. 3 ^arvanitidis2017latent-008
- A deterministic generative model with a sufficiently smooth generator can be seen as a surface model, a view going back to Gauss. (Arvanitidis et al., 2017) `ev:cited` p. 3 ^arvanitidis2017latent-009
- Curve lengths along the generator surface can be computed directly in latent space using the local metric M equal to J⊺J. (Arvanitidis et al., 2017) `ev:computed` p. 3 ^arvanitidis2017latent-010
- The paper states that if the generator is sufficiently smooth, the matrix J⊺J defines a Riemannian metric on the latent space. (Arvanitidis et al., 2017) `ev:computed` p. 3 ^arvanitidis2017latent-011
- Following a classic result of differential geometry, shortest latent curves satisfy a system of ordinary differential equations involving the metric. (Arvanitidis et al., 2017) `ev:cited` p. 3 ^arvanitidis2017latent-012
- The authors compute shortest curves by solving the geodesic ordinary differential equations numerically, using the bvp5c solver from Matlab. (Arvanitidis et al., 2017) `ev:reported` p. 4 ^arvanitidis2017latent-013
- The appendix shows the paper's ODE coefficients differ from the Christoffel symbols, but each symbol equals the average of two coefficient-matrix entries. (Arvanitidis et al., 2017) `ev:computed` p. 12 ^arvanitidis2017latent-014
- The paper extends the analysis to stochastic generators that add a variance function times Gaussian noise to a mean function, as in VAEs. (Arvanitidis et al., 2017) `ev:reported` p. 4 ^arvanitidis2017latent-015
- Theorem 1 shows that, for twice-differentiable mean and variance functions, the expected metric is the sum of mean and variance Jacobian products. (Arvanitidis et al., 2017) `ev:computed` p. 4 ^arvanitidis2017latent-016
- The authors note that a smooth metric is easily ensured by using C2-differentiable activations such as tanh, sigmoid, or softplus. (Arvanitidis et al., 2017) `ev:asserted` p. 4 ^arvanitidis2017latent-017
- Citing Tosi et al., Theorem 2 states that the variance of the stochastic metric vanishes when the data dimension goes to infinity. (Arvanitidis et al., 2017) `ev:cited` p. 4 ^arvanitidis2017latent-018
- The authors approximate the stochastic metric by its deterministic expectation, which Theorem 2 suggests is good when data dimension is large. (Arvanitidis et al., 2017) `ev:asserted` p. 4 ^arvanitidis2017latent-019
- The variance term makes induced distances large where the generator is highly uncertain, such that shortest paths tend to avoid these regions. (Arvanitidis et al., 2017) `ev:asserted` p. 4 ^arvanitidis2017latent-020
- The authors stress that no learning is needed to compute the metric, since it derives directly from the generator function. (Arvanitidis et al., 2017) `ev:asserted` p. 4 ^arvanitidis2017latent-021
- The authors argue that practical neural-network variance estimates tend to be arbitrarily poor in latent regions without training data. (Arvanitidis et al., 2017) `ev:asserted` p. 4 ^arvanitidis2017latent-022
- In a two-dimensional toy example, a standard softplus variance network gives off-data variance estimates that are sometimes high and sometimes low. (Arvanitidis et al., 2017) `ev:measured` p. 5 ^arvanitidis2017latent-023
- An informal survey of public VAE implementations found that enforcing a constant unit variance everywhere is common practice. (Arvanitidis et al., 2017) `ev:reported` p. 5 ^arvanitidis2017latent-024
- The authors propose modelling the generator precision with a radial basis function network whose output extrapolates towards zero away from data. (Arvanitidis et al., 2017) `ev:asserted` p. 5 ^arvanitidis2017latent-025
- The RBF precision network uses positive weights to ensure positive precision, plus small positive constants that prevent division by zero. (Arvanitidis et al., 2017) `ev:reported` p. 5 ^arvanitidis2017latent-026
- With the RBF precision model, the variance of the generator increases with the distance from the radial basis function centers. (Arvanitidis et al., 2017) `ev:asserted` p. 5 ^arvanitidis2017latent-027
- In the toy example, the estimated RBF variance function is large outside the data support, which is the desired property. (Arvanitidis et al., 2017) `ev:measured` p. 5 ^arvanitidis2017latent-028
- The proposed variance also increases between the two toy clusters, which the authors read as uncertainty in interpolating between clusters. (Arvanitidis et al., 2017) `ev:measured` p. 5 ^arvanitidis2017latent-029
- RBF centers are estimated with k-means on the encoded training data, after the inference network has already been trained. (Arvanitidis et al., 2017) `ev:reported` p. 5 ^arvanitidis2017latent-030
- The bandwidth formula includes a hyper-parameter a that controls the curvature of the Riemannian metric, meaning how fast it changes. (Arvanitidis et al., 2017) `ev:reported` p. 5 ^arvanitidis2017latent-031
- With the generator mean already trained, the RBF weights are fitted by projected gradient descent to keep them positive. (Arvanitidis et al., 2017) `ev:reported` p. 5 ^arvanitidis2017latent-032
- Under the volume measure sqrt det M, the proposed variance model captures the trend of the data, unlike the standard variance model. (Arvanitidis et al., 2017) `ev:measured` p. 5 ^arvanitidis2017latent-033
- For clustering, the authors build 3 sets of MNIST digits using 1000 random samples per digit, training one VAE per set. (Arvanitidis et al., 2017) `ev:reported` p. 6 ^arvanitidis2017latent-034
- Each MNIST set is subdivided into 10 subsets, on which k-means clustering is run under both Euclidean and Riemannian distances. (Arvanitidis et al., 2017) `ev:reported` p. 6 ^arvanitidis2017latent-035
- For digits {0, 1, 2}, k-means reaches an F-measure of 94.28(±1.14)% under the Riemannian metric versus 77.57(±0.87)% under the linear one. (Arvanitidis et al., 2017) `ev:measured` p. 6 ^arvanitidis2017latent-036
- For digits {3, 4, 7}, k-means reaches an F-measure of 89.54(±1.61)% under the Riemannian metric versus 77.80(±0.91)% under the linear one. (Arvanitidis et al., 2017) `ev:measured` p. 6 ^arvanitidis2017latent-037
- For digits {5, 6, 9}, k-means reaches an F-measure of 81.13(±2.52)% under the Riemannian metric versus 64.93(±0.96)% under the linear one. (Arvanitidis et al., 2017) `ev:measured` p. 6 ^arvanitidis2017latent-038
- Because latent points roughly follow a unit Gaussian, the authors find little structure for Euclidean k-means to discover, so it performs poorly. (Arvanitidis et al., 2017) `ev:measured` p. 6 ^arvanitidis2017latent-039
- The authors conclude from the clustering results that the underlying Riemannian distance is more useful than its Euclidean counterpart. (Arvanitidis et al., 2017) `ev:asserted` p. 6 ^arvanitidis2017latent-040
- On a VAE trained on MNIST digits 0 and 1, Euclidean interpolations seem to change very abruptly when transitioning between classes. (Arvanitidis et al., 2017) `ev:measured` p. 6 ^arvanitidis2017latent-041
- On the same VAE, the Riemannian interpolant gives smoother changes in the generated images than the Euclidean interpolant. (Arvanitidis et al., 2017) `ev:measured` p. 6 ^arvanitidis2017latent-042
- Image auto-correlation along the interpolants is significantly smoother for the Riemannian path than for the Euclidean path, which changes abruptly. (Arvanitidis et al., 2017) `ev:measured` p. 6 ^arvanitidis2017latent-043
- A convolutional VAE trained on video frames also shows smoother changes in generated images under Riemannian interpolation than under Euclidean interpolation. (Arvanitidis et al., 2017) `ev:measured` p. 6 ^arvanitidis2017latent-044
- The authors fit a mixture of two locally adaptive normal distributions to the MNIST data of the interpolation experiment, alongside a mixture of Euclidean normals. (Arvanitidis et al., 2017) `ev:reported` p. 7 ^arvanitidis2017latent-045
- Among the two fitted mixture models, only the Riemannian model's density function reveals the underlying clusters in the latent data. (Arvanitidis et al., 2017) `ev:measured` p. 7 ^arvanitidis2017latent-046
- When 40 points are sampled from each mixture component, the Riemannian model generates high-quality samples. (Arvanitidis et al., 2017) `ev:measured` p. 7 ^arvanitidis2017latent-047
- The Euclidean mixture generates several samples in regions where the generator is not trained, which produce blurry decoded images. (Arvanitidis et al., 2017) `ev:measured` p. 7 ^arvanitidis2017latent-048
- The authors deliberately do not sort generated samples by their likelihood, since this common practice hides low-quality samples. (Arvanitidis et al., 2017) `ev:reported` p. 7 ^arvanitidis2017latent-049
- Practical latent random walk implementations artificially restrict the walk to a hypercube to keep it from drifting outside the data support. (Arvanitidis et al., 2017) `ev:asserted` p. 7 ^arvanitidis2017latent-050
- The authors run unrestricted Brownian motion under both Euclidean and Riemannian metrics in the latent space of the convolutional VAE. (Arvanitidis et al., 2017) `ev:reported` p. 8 ^arvanitidis2017latent-051
- In the convolutional VAE latent space, the Riemannian random walk stays within the data support, whereas the Euclidean walk moves freely. (Arvanitidis et al., 2017) `ev:measured` p. 8 ^arvanitidis2017latent-052
- The authors explain this by the variance term of the metric creating a 'wall' around the data that the random walk only rarely crosses. (Arvanitidis et al., 2017) `ev:asserted` p. 8 ^arvanitidis2017latent-053
- Riemannian Brownian motion is simulated by eigendecomposing the metric at each point and stepping along eigenvectors scaled by inverse square-root eigenvalues. (Arvanitidis et al., 2017) `ev:reported` p. 15 ^arvanitidis2017latent-054
- For the marginal likelihood test, a VAE is trained on MNIST digits 0 and 1, split into 90% training and 10% test data. (Arvanitidis et al., 2017) `ev:reported` p. 13 ^arvanitidis2017latent-055
- With encoder and mean fixed, a standard neural variance function is compared against the RBF model using 32 centers and a = 1. (Arvanitidis et al., 2017) `ev:reported` p. 13 ^arvanitidis2017latent-056
- Test-set marginal likelihood is estimated by Monte Carlo sampling from the prior, using S = 10000 samples. (Arvanitidis et al., 2017) `ev:reported` p. 14 ^arvanitidis2017latent-057
- The proposed RBF variance model achieves a mean test log-marginal likelihood of -50.34, compared with -68.25 for the standard variance function. (Arvanitidis et al., 2017) `ev:measured` p. 14 ^arvanitidis2017latent-058
- The authors attribute this gain to the RBF model assigning minimal density to regions without data, thus attaining higher likelihood elsewhere. (Arvanitidis et al., 2017) `ev:asserted` p. 14 ^arvanitidis2017latent-059
- For the MNIST experiments, the precision network is an RBF model with 64 centers and bandwidth parameter a set to 2. (Arvanitidis et al., 2017) `ev:reported` p. 14 ^arvanitidis2017latent-060
- The MNIST encoder and decoder are multilayer perceptrons with tanh hidden layers of 64 and 32 units, trained with L2 regularization 1e−5. (Arvanitidis et al., 2017) `ev:reported` p. 14 ^arvanitidis2017latent-061
- In the convolutional VAE, the RBF variance output passes through deconvolution layers whose filter weights must be clipped to positive values. (Arvanitidis et al., 2017) `ev:reported` p. 14 ^arvanitidis2017latent-062
- The authors conclude that geometrically informed random walks stayed on the data manifold for much longer runs than Euclidean random walks. (Arvanitidis et al., 2017) `ev:asserted` p. 9 ^arvanitidis2017latent-063
- The authors report that Riemannian LAND mixture components aligned much better with the ground truth group structure in their experiments. (Arvanitidis et al., 2017) `ev:asserted` p. 9 ^arvanitidis2017latent-064
- The authors state that their new variance network provides meaningful uncertainty estimates that also regularize the latent geometry. (Arvanitidis et al., 2017) `ev:asserted` p. 9 ^arvanitidis2017latent-065
- The authors claim the analysis easily extends to more sophisticated generative models, whose latent spaces may carry more flexible nonlinear structures. (Arvanitidis et al., 2017) `ev:asserted` p. 9 ^arvanitidis2017latent-066
- The authors note that GANs also have an explicit generator, so the ideas developed for VAEs extend to them as well. (Arvanitidis et al., 2017) `ev:asserted` p. 9 ^arvanitidis2017latent-067
- Tosi et al. derived a suitable Riemannian metric for Gaussian process latent variable models, whose computational complexity causes practical concerns. (Arvanitidis et al., 2017) `ev:cited` p. 9 ^arvanitidis2017latent-068

## 🎯 Contributions

## 📖 Glossary

- **Riemannian metric** — Smooth function assigning a symmetric positive definite matrix to every latent point.
- **Pull-back metric** — Latent metric J⊺J obtained by mapping infinitesimal latent displacements through the generator.
- **Geodesic** — Shortest curve between two points under a Riemannian metric.
- **Expected metric** — Average of the stochastic metric over generator noise; sum of mean and variance Jacobian terms.
- **Christoffel symbols** — Coefficients of the geodesic differential equation derived from metric derivatives.
- **RBF network** — Network whose outputs are weighted sums of Gaussian radial basis functions around centers.
- **LAND** — Locally adaptive normal distribution using Riemannian Mahalanobis distance in place of Euclidean.
- **Volume measure** — Square root of det M; local volume change from latent to input space.

## ❓ Open questions

- Can the latent space geometry play a role while the generative model is being learned, rather than only after training?
- How well does the expected-metric approximation hold when the data dimension is small, where Theorem 2 gives no guarantee?
- How should the curvature hyper-parameter a be chosen, and how sensitive are the results to it?
- Does the geometric analysis transfer in practice to GANs and flow-based models, which the paper only argues for?
- Can geodesic computation via a boundary value solver scale to high-dimensional latent spaces?

## 📝 Notes on reading

The cached text is arXiv v3 (13 Dec 2021) of 1710.11379, headed as the ICLR 2018 conference paper; the packet metadata lists it as a 2017 arXiv preprint, so the citation year follows the metadata.

Figures 1, 3, 6, 7, 8, 9, 10 and 11 are qualitative (latent maps, interpolated images, sampled digits, random walk frames); their content is claimed only where the text states it. The colour-bar ticks of Figures 4 and 10 were extracted as loose numbers and are not claimed.

The geodesic ODE (Eqs. 7, 8, 22, 23), the RBF precision model (Eq. 11), the bandwidth formula (Eq. 12) and the Jacobian matrices in Appendix B were partly garbled by extraction; only their verbal descriptions were claimed.

Appendix C uses softplus hidden layers and a tanh mean output for the standard variance network, while Appendix D uses tanh hidden layers and a sigmoid mean output; the appendices describe different setups rather than an inconsistency. Appendix C scales MNIST to [−1, 1], Appendix D to [0, 1].

The Figure 4 caption calls log of the summed σ a standard deviation, a loose label.

## Suggested new concepts

- Pull-back Riemannian metric of a generator — central object reused across latent-geometry work on VAEs and GANs.
- Latent space geodesic interpolation — a recurring alternative to linear interpolation in generative models.
- Variance extrapolation in decoders — the failure of neural variance networks away from data matters beyond geometry.
- Locally adaptive normal distribution (LAND) — Riemannian density model reused for latent spaces.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Métrica pullback estocástica y geodésicas latentes (E.3).

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
