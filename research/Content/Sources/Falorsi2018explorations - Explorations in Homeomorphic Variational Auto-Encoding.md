---
aliases: []
type: "source"
title: "Explorations in Homeomorphic Variational Auto-Encoding"
citekey: "Falorsi2018explorations"
doi: "10.48550/arXiv.1807.04689"
arxiv: "1807.04689"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1807.04689"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Luca Falorsi", "Pim de Haan", "Tim R. Davidson", "Nicola De Cao", "Maurice Weiler", "Patrick Forré", "Taco S. Cohen"]
sha256: ["f6ac3ca0575b0beb76074fcf50182c5d85f2945a0de12d7d2120f08e85bb63c9"]
pdf: "Content/Papers/Falorsi2018explorations.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Falorsi2018explorations.pdf]]

> [!abstract] One-sentence summary
> The paper builds a VAE with SO(3)-valued latent variables by extending the reparameterization trick to compact connected Lie groups, showing that matching latent topology to the data manifold yields continuous, well-structured latent spaces.

## Abstract

The manifold hypothesis states that many kinds of high-dimensional data are concentrated near a low-dimensional manifold. If the topology of this data manifold is non-trivial, a continuous encoder network cannot embed it in a one-to-one manner without creating holes of low density in the latent space. This is at odds with the Gaussian prior assumption typically made in Variational Auto-Encoders (VAEs), because the density of a Gaussian concentrates near a blob-like manifold. In this paper we investigate the use of manifold-valued latent variables. Specifically, we focus on the important case of continuously differentiable symmetry groups (Lie groups), such as the group of 3D rotations $\operatorname{SO}(3)$. We show how a VAE with $\operatorname{SO}(3)$-valued latent variables can be constructed, by extending the reparameterization trick to compact connected Lie groups. Our experiments show that choosing manifold-valued latent variables that match the topology of the latent data manifold, is crucial to preserve the topological structure and learn a well-behaved latent space. (arXiv)

## 🧠 Key ideas (atomic)

- If data lie near a low-dimensional manifold with non-trivial topology, no continuous invertible mapping to a blob-like prior region exists. (Falorsi et al., 2018) `ev:asserted` p. 1 ^falorsi2018explorations-001
- The authors argue that for representation learning the encoder should be homeomorphic, meaning continuous and invertible with a continuous inverse. (Falorsi et al., 2018) `ev:asserted` p. 1 ^falorsi2018explorations-002
- Encoding such a manifold in a higher-dimensional flat space with a regular VAE puts prior density outside of the embedding. (Falorsi et al., 2018) `ev:asserted` p. 1 ^falorsi2018explorations-003
- In a flat embedding, traversals normal to the manifold either leave the decoding invariant or move out of the data manifold. (Falorsi et al., 2018) `ev:asserted` p. 1 ^falorsi2018explorations-004
- The paper constructs a VAE with latent variables living on a Lie group by generalizing the reparameterization trick. (Falorsi et al., 2018) `ev:reported` p. 2 ^falorsi2018explorations-005
- The authors state that their reparameterization approach for SO(3) extends to general compact connected Lie group VAEs in a straightforward manner. (Falorsi et al., 2018) `ev:asserted` p. 2 ^falorsi2018explorations-006
- The primary technical difficulty is showing the reparameterization's pushforward measure has a density absolutely continuous with respect to the Haar measure. (Falorsi et al., 2018) `ev:asserted` p. 2 ^falorsi2018explorations-007
- The paper proposes a decoder that uses the group action to encourage the latent space to respect the group structure. (Falorsi et al., 2018) `ev:reported` p. 2 ^falorsi2018explorations-008
- Experiments use two synthetic data types: SO(3) embedded in high-dimensional space through a group representation, plus rotated images of a colored cube. (Falorsi et al., 2018) `ev:reported` p. 2 ^falorsi2018explorations-009
- Models with a standard Gaussian latent space show discontinuities when trajectories in the latent space are visualized. (Falorsi et al., 2018) `ev:measured` p. 2 ^falorsi2018explorations-010
- The authors introduce a measure of embedding continuity based on the concept of Lipschitz continuity. (Falorsi et al., 2018) `ev:reported` p. 2 ^falorsi2018explorations-011
- SO(3) is not homeomorphic to R^N, since every continuous path in R^N contracts to a point, unlike in SO(3). (Falorsi et al., 2018) `ev:asserted` p. 3 ^falorsi2018explorations-012
- The reparameterization samples v from a scale-reparameterizable distribution on R3 concentrated around the origin, identified with a Lie algebra element. (Falorsi et al., 2018) `ev:reported` p. 3 ^falorsi2018explorations-013
- Applying the exponential map to the algebra sample gives a group sample concentrated around the identity, relocated by left multiplication with R_mu. (Falorsi et al., 2018) `ev:reported` p. 3 ^falorsi2018explorations-014
- Theorem 1 proves that the pushforward of a Lebesgue-continuous measure through the exponential map is absolutely continuous with respect to Haar measure. (Falorsi et al., 2018) `ev:computed` p. 3 ^falorsi2018explorations-015
- The resulting density on SO(3) is singular at the identity, yet the paper notes it still integrates to 1. (Falorsi et al., 2018) `ev:computed` p. 3 ^falorsi2018explorations-016
- The entropy term of the KL divergence is estimated with Monte Carlo samples that depend only on samples in the Lie algebra. (Falorsi et al., 2018) `ev:computed` p. 4 ^falorsi2018explorations-017
- The authors found that a single Monte Carlo sample suffices for the entropy estimate when mini-batches are used. (Falorsi et al., 2018) `ev:measured` p. 4 ^falorsi2018explorations-018
- For a uniform prior on SO(3), the cross-entropy term reduces to a constant, the negative logarithm of 1/(8 pi squared). (Falorsi et al., 2018) `ev:computed` p. 4 ^falorsi2018explorations-019
- The encoder is split into two parts, one predicting the mean rotation R_mu and another predicting the scale sigma. (Falorsi et al., 2018) `ev:reported` p. 4 ^falorsi2018explorations-020
- The mean encoder is built as a neural network f into a space Y composed with a fixed surjective map to SO(3). (Falorsi et al., 2018) `ev:reported` p. 4 ^falorsi2018explorations-021
- A necessary condition for the mean encoder to learn a homeomorphism is that an embedding of SO(3) into Y exists. (Falorsi et al., 2018) `ev:computed` p. 4 ^falorsi2018explorations-022
- The authors note a naive decoder fed the 9 rotation-matrix entries gives no guarantee that the latent space reflects pose variations. (Falorsi et al., 2018) `ev:asserted` p. 5 ^falorsi2018explorations-023
- The group action decoder learns band-limited Fourier modes of a sphere signal, transformed linearly by Wigner-D-matrices of the latent rotation. (Falorsi et al., 2018) `ev:reported` p. 5 ^falorsi2018explorations-024
- The paper states that mapping rotations to Wigner-D-matrices is a homomorphism that preserves the group structure of SO(3). (Falorsi et al., 2018) `ev:asserted` p. 5 ^falorsi2018explorations-025
- The authors suggest the group action decoder could disentangle content and pose, but leave this for future work. (Falorsi et al., 2018) `ev:asserted` p. 5 ^falorsi2018explorations-026
- Davidson et al. extended Naesseth et al.'s reparameterization to the hyperspherical von Mises-Fisher distribution to capture intrinsically hyperspherical data. (Falorsi et al., 2018) `ev:cited` p. 5 ^falorsi2018explorations-027
- Earlier work defined distributions on homogeneous spaces including Lie groups, but did not concentrate on making those distributions reparameterizable. (Falorsi et al., 2018) `ev:cited` p. 6 ^falorsi2018explorations-028
- Experiments compare manifold topology, decoder architecture, and SO(3) mean parameterization, reporting a negative log likelihood bound via importance sampling. (Falorsi et al., 2018) `ev:reported` p. 6 ^falorsi2018explorations-029
- The latent topologies compared are the Gaussian N-VAE, the hyperspherical S-VAE of Davidson et al., and the proposed SO(3) latent variable. (Falorsi et al., 2018) `ev:reported` p. 6 ^falorsi2018explorations-030
- Mean parameterizations tested are quaternions, Lie algebra, and S2 x S1, which are invalid, plus S2 x S2, which is valid. (Falorsi et al., 2018) `ev:reported` p. 6 ^falorsi2018explorations-031
- The toy data use three copies of Wigner-D-matrices up to order 3, making the embedding space R64. (Falorsi et al., 2018) `ev:reported` p. 7 ^falorsi2018explorations-032
- In the toy experiment the encoder is a 3 layer MLP, while the decoder is the group action decoder. (Falorsi et al., 2018) `ev:reported` p. 7 ^falorsi2018explorations-033
- In the toy experiment the choice of mean parameterization significantly impacts the model's ability to correctly learn the manifold. (Falorsi et al., 2018) `ev:measured` p. 7 ^falorsi2018explorations-034
- In the non-variational toy auto-encoder, S2 x S2 achieves near-perfect reconstructions with a reconstruction error of 0.01. (Falorsi et al., 2018) `ev:measured` p. 7 ^falorsi2018explorations-035
- S2 x S2 is the only toy model without latent discontinuities, scoring 0. on the discontinuity metric. (Falorsi et al., 2018) `ev:measured` p. 7 ^falorsi2018explorations-036
- In the toy VAE, SO(3)-s2s2 obtains the lowest NLL, 10.7, against 18.9 for the 3-dimensional Normal model. (Falorsi et al., 2018) `ev:measured` p. 7 ^falorsi2018explorations-037
- The worst toy models, the 3-dimensional Normal and SO(3) algebra mean, both represent SO(3) by R3 at an intermediate point. (Falorsi et al., 2018) `ev:measured` p. 7 ^falorsi2018explorations-038
- The authors conclude that flat space representing a non-trivial manifold yields a poorly structured latent space and worse likelihoods. (Falorsi et al., 2018) `ev:asserted` p. 7 ^falorsi2018explorations-039
- The sphere-cube training set contains 1M images of an asymmetric colored cube rotated by uniformly sampled SO(3) elements. (Falorsi et al., 2018) `ev:reported` p. 8 ^falorsi2018explorations-040
- The sphere-cube encoder has 5 convolutional layers, while decoders use the group action or a 3 layer MLP. (Falorsi et al., 2018) `ev:reported` p. 8 ^falorsi2018explorations-041
- Following Burgess et al., the KL term is replaced by a squared difference to a target raised from 7 to 15. (Falorsi et al., 2018) `ev:reported` p. 8 ^falorsi2018explorations-042
- The authors found that two additional regularizing loss terms were needed to correctly learn the sphere-cube latent space. (Falorsi et al., 2018) `ev:measured` p. 8 ^falorsi2018explorations-043
- On sphere-cube, SO(3)-action-s2s2 reaches an NLL of 46.90, compared with 64.02 for the 10-dimensional Normal VAE. (Falorsi et al., 2018) `ev:measured` p. 8 ^falorsi2018explorations-044
- Higher-dimensional N-VAEs achieve competitive metrics but only embed SO(3) in a high-dimensional space in an unstructured fashion. (Falorsi et al., 2018) `ev:measured` p. 8 ^falorsi2018explorations-045
- The 10 dimensional Normal model learns disconnected patches of the sphere-cube data manifold, unlike the SO(3) S2 x S2 model. (Falorsi et al., 2018) `ev:measured` p. 8 ^falorsi2018explorations-046
- On sphere-cube, only the continuous S2 x S2 encoding achieves low log likelihood and reconstruction losses among mean parameterizations. (Falorsi et al., 2018) `ev:measured` p. 8 ^falorsi2018explorations-047
- On the sphere-cube experiment, the group action decoder yields significantly higher performance than the simple MLP decoder. (Falorsi et al., 2018) `ev:measured` p. 8 ^falorsi2018explorations-048
- With the MLP decoder, SO(3)-s2s2 reaches an NLL of 123.6, versus 46.90 with the group action decoder. (Falorsi et al., 2018) `ev:measured` p. 8 ^falorsi2018explorations-049
- The authors see SO(3) and similar manifold-valued latent variables as a possible addition for model based RL and computer vision. (Falorsi et al., 2018) `ev:asserted` p. 8 ^falorsi2018explorations-050
- Moving forward, the authors aim to extend their reparameterization theory to other Lie groups such as SE(3). (Falorsi et al., 2018) `ev:asserted` p. 8 ^falorsi2018explorations-051
- A stated limitation is that the approach relies on a priori knowledge about the latent structure of the observed data. (Falorsi et al., 2018) `ev:asserted` p. 8 ^falorsi2018explorations-052
- For the S2 x S1 mean parameterization, the paper shows the required image set is not closed, making the right inverse discontinuous. (Falorsi et al., 2018) `ev:computed` p. 14 ^falorsi2018explorations-053
- S2 x S2 admits a continuous injective map from SO(3), taking the first two rows of the rotation matrix. (Falorsi et al., 2018) `ev:computed` p. 14 ^falorsi2018explorations-054
- The continuity metric flags a path discontinuous when the maximum ratio exceeds gamma times the alpha-th percentile ratio. (Falorsi et al., 2018) `ev:reported` p. 15 ^falorsi2018explorations-055
- The continuity metric is computed over 1000 paths with gamma = 10 and alpha = 90, scoring the discontinuous fraction. (Falorsi et al., 2018) `ev:reported` p. 15 ^falorsi2018explorations-056
- Even with a suitable mean parameterization and group action decoder, the network can still learn a discontinuous latent space. (Falorsi et al., 2018) `ev:asserted` p. 15 ^falorsi2018explorations-057
- The equivariance regularizer enforces that planar pixel rotations match latent rotations about the z-axis via a mean squared error loss. (Falorsi et al., 2018) `ev:reported` p. 16 ^falorsi2018explorations-058
- The continuity regularizer penalizes differences between encodings of image pairs that are nearby on the manifold. (Falorsi et al., 2018) `ev:reported` p. 16 ^falorsi2018explorations-059
- In the regularizer ablation, using both regularizers gives an NLL of 45.18, against 235.24 with neither. (Falorsi et al., 2018) `ev:measured` p. 16 ^falorsi2018explorations-060
- With the equivariance regularizer alone the NLL is 75.62, whereas the continuity regularizer alone gives an NLL of 87.36. (Falorsi et al., 2018) `ev:measured` p. 16 ^falorsi2018explorations-061

## 🎯 Contributions

## 📖 Glossary

- **Homeomorphism** — continuous invertible map whose inverse is also continuous; preserves topology.
- **Lie group** — group that is also a smooth manifold, e.g. continuous symmetries like rotations.
- **Lie algebra** — tangent space of a Lie group at the identity; infinitesimal generators.
- **Exponential map** — maps Lie algebra elements to group elements; surjective for compact connected groups.
- **SO(3)** — group of 3D rotation matrices with orthonormal columns and determinant one.
- **Haar measure** — natural invariant measure on a Lie group.
- **Reparameterization trick** — writing samples as differentiable functions of parameters and fixed noise for gradient estimation.
- **Wigner-D-matrix** — irreducible representation matrix of SO(3); rotates spherical-harmonic Fourier coefficients.
- **Group action decoder** — decoder rotating learned Fourier modes by the latent rotation before rendering.
- **Mean parameterization** — how network outputs are mapped onto SO(3) to give the posterior mean.

## ❓ Open questions

- Can the reparameterization be extended to non-compact groups such as SE(3) with the same guarantees?
- How can arbitrary latent manifolds be learned when their topology is not known in advance?
- Can the group action decoder disentangle content from pose when the encoder also infers the Fourier modes?
- Could normalizing flows be applied on SO(3) to obtain more flexible posteriors?
- Can a discontinuity-free latent space be learned without the continuity regularizer, which needs pairs of nearby frames?

## 📝 Notes on reading

- Version read: arXiv preprint 1807.04689v1, presented at the ICML 2018 workshop on Theoretical Foundations and Applications of Deep Generative Models.
- Equations (4)-(9) and the appendix derivations (10)-(28) are garbled in the extraction; only their verbal statements were claimed.
- Figures 4.2, 6.1, A.1, A.2 and G.1 (latent trajectories, interpolations, discontinuity plots, equivariance decodings) could only be described.
- Table 1 prints the discontinuity values as "1." and "0." (extraction of 1.0 and 0.0); claims keep "0." as printed.
- Table 2 reports the SO(3) models with both regularizers and the Normal models with neither, so the comparison is not regularizer-matched.
- The introduction says the reparameterization extends to compact connected Lie groups, but the conclusion names SE(3), which is not compact, as the next target.

## Suggested new concepts

- Manifold-valued latent variables — recurring idea of matching latent topology to data topology in generative models.
- Reparameterization on Lie groups — general technique enabling VAEs with group-valued latents.
- Homeomorphic encoder — design criterion for encoders that preserve data-manifold topology.
- Latent continuity metric — Lipschitz-based diagnostic for discontinuities in learned embeddings.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Latentes en $SO(3)$ por razones topológicas (§7)

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
