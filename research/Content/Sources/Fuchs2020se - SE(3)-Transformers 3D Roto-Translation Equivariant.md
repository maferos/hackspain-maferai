---
aliases: []
type: "source"
title: "SE(3)-Transformers: 3D Roto-Translation Equivariant Attention Networks"
citekey: "Fuchs2020se"
doi: "10.48550/arXiv.2006.10503"
arxiv: "2006.10503"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2006.10503"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Fabian B. Fuchs", "Daniel E. Worrall", "Volker Fischer", "Max Welling"]
sha256: ["37b2316983ba42e7e04dd9487c97b3e00b7d2d2b7c393d75aa96ed009060d030"]
pdf: "Content/Papers/Fuchs2020se.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Fuchs2020se.pdf]]

> [!abstract] One-sentence summary
> The paper builds a self-attention layer for 3D point clouds and graphs that is exactly equivariant to rotations and translations, and shows it beats both non-equivariant attention and equivariant convolution baselines on N-body, ScanObjectNN and QM9 tasks.

## Abstract

We introduce the SE(3)-Transformer, a variant of the self-attention module for 3D point clouds and graphs, which is equivariant under continuous 3D roto-translations. Equivariance is important to ensure stable and predictable performance in the presence of nuisance transformations of the data input. A positive corollary of equivariance is increased weight-tying within the model. The SE(3)-Transformer leverages the benefits of self-attention to operate on large point clouds and graphs with varying number of points, while guaranteeing SE(3)-equivariance for robustness. We evaluate our model on a toy N-body particle simulation dataset, showcasing the robustness of the predictions under rotations of the input. We further achieve competitive performance on two real-world datasets, ScanObjectNN and QM9. In all cases, our model outperforms a strong, non-equivariant attention baseline and an equivariant model without attention. (arXiv)

## 🧠 Key ideas (atomic)

- The SE(3)-Transformer is a self-attention module for 3D point clouds and graphs that is equivariant under continuous 3D roto-translations. (Fuchs et al., 2020) `ev:asserted` p. 1 ^fuchs2020se-001
- The SE(3)-Transformer explicitly designs its attention weights to be invariant to the global pose of the input point cloud. (Fuchs et al., 2020) `ev:asserted` p. 2 ^fuchs2020se-002
- The SE(3)-Transformer designs its value embedding to be equivariant to global pose, generalising the translational weight-tying of convolutions to 3D. (Fuchs et al., 2020) `ev:asserted` p. 2 ^fuchs2020se-003
- The authors state that [[Equivariant neural network|SE(3)-equivariance]] restricts learnable functions to a subspace respecting task symmetries, which reduces the number of learnable parameters. (Fuchs et al., 2020) `ev:asserted` p. 2 ^fuchs2020se-004
- [[Tensor Field Network|Tensor field networks]] and [[Steerable CNN|3D steerable CNNs]] are the works closest to the SE(3)-Transformer, providing SE(3)-equivariant convolutional frameworks for point clouds. (Fuchs et al., 2020) `ev:cited` p. 2 ^fuchs2020se-005
- According to the authors, using self-attention instead of convolutions naturally handles edge features, extending [[Tensor Field Network|tensor field networks]] to the graph setting. (Fuchs et al., 2020) `ev:asserted` p. 2 ^fuchs2020se-006
- The authors describe employing equivariant self-attention as one of the first examples of a nonlinear equivariant layer. (Fuchs et al., 2020) `ev:asserted` p. 2 ^fuchs2020se-007
- The angular constraint on filters in [[Tensor Field Network|tensor field networks]] has been pointed out in the equivariance literature to limit performance severely. (Fuchs et al., 2020) `ev:cited` p. 2 ^fuchs2020se-008
- Besides roto-translation invariance, the proposed self-attention mechanism is also equivariant to permutations of the input point labels. (Fuchs et al., 2020) `ev:asserted` p. 2 ^fuchs2020se-009
- The authors introduce a Pytorch implementation of spherical harmonics that is 10x faster than Scipy when run on CPU. (Fuchs et al., 2020) `ev:measured` p. 2 ^fuchs2020se-010
- On GPU, the authors' Pytorch spherical harmonics implementation is reported to be 100 −1000× faster than the Scipy implementation. (Fuchs et al., 2020) `ev:measured` p. 2 ^fuchs2020se-011
- For a ScanObjectNN model, the new spherical harmonics give a ≈22× speed up of the forward pass compared with SH from lielearn. (Fuchs et al., 2020) `ev:measured` p. 2 ^fuchs2020se-012
- In [[Tensor Field Network|tensor field networks]], each basis kernel completely constrains the angular form of the learned kernel, leaving only radial learnable freedom. (Fuchs et al., 2020) `ev:cited` p. 4 ^fuchs2020se-013
- Neighbourhoods in the SE(3)-Transformer are computed with nearest-neighbour methods or may already be defined, such as molecular bonding structure. (Fuchs et al., 2020) `ev:reported` p. 5 ^fuchs2020se-014
- Neighbourhoods reduce the computational complexity of the attention mechanism from quadratic in the number of points to linear. (Fuchs et al., 2020) `ev:asserted` p. 5 ^fuchs2020se-015
- Each SE(3)-Transformer layer combines invariant edge-wise attention weights, equivariant value messages and a linear or attentive self-interaction layer. (Fuchs et al., 2020) `ev:asserted` p. 5 ^fuchs2020se-016
- Removing the attention weights from the SE(3)-Transformer layer recovers a [[Tensor Field Network|tensor field convolution]], according to the authors. (Fuchs et al., 2020) `ev:asserted` p. 5 ^fuchs2020se-017
- Removing the dependence of the value matrix on relative positions turns the SE(3)-Transformer layer into a conventional attention mechanism. (Fuchs et al., 2020) `ev:asserted` p. 5 ^fuchs2020se-018
- The layer is SE(3)-equivariant provided the attention weights are invariant, because it is a linear combination of equivariant value messages. (Fuchs et al., 2020) `ev:computed` p. 5 ^fuchs2020se-019
- Invariant attention weights come from a normalised inner product between an equivariant query at node i and equivariant keys along each edge. (Fuchs et al., 2020) `ev:computed` p. 6 ^fuchs2020se-020
- According to the authors, attention weights add angular degrees of freedom to the tensor field kernel without breaking equivariance. (Fuchs et al., 2020) `ev:asserted` p. 6 ^fuchs2020se-021
- The fixed angular dependence of equivariant kernels is seen as overconstraining the expressiveness of the kernels. (Fuchs et al., 2020) `ev:asserted` p. 6 ^fuchs2020se-022
- Self-interaction acts as a learnable skip connection, which is crucial because points do not attend to themselves in the SE(3)-Transformer. (Fuchs et al., 2020) `ev:asserted` p. 6 ^fuchs2020se-023
- The authors propose attentive self-interaction, replacing learned scalar self-interaction weights with SE(3)-invariant weights output by an MLP. (Fuchs et al., 2020) `ev:asserted` p. 6 ^fuchs2020se-024
- Scalar edge information can be incorporated into the value and key weight matrices as an input to the radial network. (Fuchs et al., 2020) `ev:asserted` p. 6 ^fuchs2020se-025
- Equivariance error is the unsquared normalised distance between transformed outputs and outputs of transformed inputs, averaged over uniformly sampled SO(3)-transformations. (Fuchs et al., 2020) `ev:reported` p. 7 ^fuchs2020se-026
- The N-body experiment adapts the Kipf et al. dataset, in which five particles carry positive or negative charges that attract or repel. (Fuchs et al., 2020) `ev:reported` p. 7 ^fuchs2020se-027
- Given position, velocity and charge at one time step, the network predicts relative location and velocity 500 time steps into the future. (Fuchs et al., 2020) `ev:reported` p. 7 ^fuchs2020se-028
- For N-body simulations, the authors trained an SE(3)-Transformer with 4 equivariant layers, each followed by an attentive self-interaction layer. (Fuchs et al., 2020) `ev:reported` p. 7 ^fuchs2020se-029
- On N-body position prediction, the SE(3)-Transformer reached MSE 0.0076, versus 0.0139 for Set Transformer and 0.0151 for Tensor Field. (Fuchs et al., 2020) `ev:measured` p. 7 ^fuchs2020se-030
- On N-body velocity prediction, the SE(3)-Transformer reached MSE 0.075, versus 0.101 for Set Transformer and 0.125 for Tensor Field. (Fuchs et al., 2020) `ev:measured` p. 7 ^fuchs2020se-031
- The SE(3)-Transformer's position equivariance error was 3.2 · 10−7, compared with 0.167 for the non-equivariant Set Transformer. (Fuchs et al., 2020) `ev:measured` p. 7 ^fuchs2020se-032
- The authors conclude the equivariance error shows their approach is fully rotation equivariant up to the precision of the computations. (Fuchs et al., 2020) `ev:measured` p. 7 ^fuchs2020se-033
- ScanObjectNN provides point clouds of 2902 objects across 15 different categories for real-world object classification. (Fuchs et al., 2020) `ev:reported` p. 8 ^fuchs2020se-034
- On ScanObjectNN, only point coordinates were used as input, with object categories serving as the training labels. (Fuchs et al., 2020) `ev:reported` p. 8 ^fuchs2020se-035
- As ScanObjectNN objects are aligned with the gravity axis, deploying a fully SO(3) invariant model results in a performance loss. (Fuchs et al., 2020) `ev:measured` p. 8 ^fuchs2020se-036
- The SE(3)-Transformer +z variant additionally feeds the z-component as a type-0 field and the x, y position as a type-1 field. (Fuchs et al., 2020) `ev:reported` p. 8 ^fuchs2020se-037
- The SE(3)-Transformer +z reached 85.0% accuracy on the ScanObjectNN object-only category using 128 input points. (Fuchs et al., 2020) `ev:measured` p. 8 ^fuchs2020se-038
- The fully equivariant SE(3)-Transformer reached 72.8 % accuracy on ScanObjectNN object-only, above Tensor Field at 63.1%. (Fuchs et al., 2020) `ev:measured` p. 8 ^fuchs2020se-039
- Tensor Field +z reached 81.0% accuracy on ScanObjectNN, below the 85.0% of SE(3)-Transformer +z with the same 128 points. (Fuchs et al., 2020) `ev:measured` p. 8 ^fuchs2020se-040
- PointGLR, pre-trained on the larger ModelNet40 dataset, reached 87.2% ScanObjectNN accuracy using 1024 input points. (Fuchs et al., 2020) `ev:cited` p. 8 ^fuchs2020se-041
- The reported SE(3)-Transformer ScanObjectNN performance is averaged over 5 runs, with a standard deviation of 0.7%. (Fuchs et al., 2020) `ev:measured` p. 8 ^fuchs2020se-042
- The authors describe their ScanObjectNN performance as competitive with models specifically designed for object classification despite a much lower number of input points. (Fuchs et al., 2020) `ev:asserted` p. 8 ^fuchs2020se-043
- When the training set presents a rotation-invariant problem, the +z model learns to ignore the additional symmetry-breaking input. (Fuchs et al., 2020) `ev:measured` p. 8 ^fuchs2020se-044
- QM9 contains 134k molecules with up to 29 atoms per molecule, used here for 6 property regression tasks. (Fuchs et al., 2020) `ev:reported` p. 9 ^fuchs2020se-045
- On QM9 εHOMO, the SE(3)-Transformer reached a mean absolute error of 35.0±.9 meV, versus 40 meV for TFN. (Fuchs et al., 2020) `ev:measured` p. 9 ^fuchs2020se-046
- On QM9 polarizability α, the SE(3)-Transformer reached .142±.002 bohr3 mean absolute error, lower than the .223 of TFN. (Fuchs et al., 2020) `ev:measured` p. 9 ^fuchs2020se-047
- LieConv(T3) achieved lower QM9 errors than the SE(3)-Transformer on several tasks, including 25 meV on εLUMO versus 33.0±.7 meV. (Fuchs et al., 2020) `ev:measured` p. 9 ^fuchs2020se-048
- The authors suggest that LieConv(T3) using a left-regular representation of SE(3), unlike irreducible representations, may explain its success. (Fuchs et al., 2020) `ev:asserted` p. 9 ^fuchs2020se-049
- The authors describe their QM9 results as not state-of-the-art but competitive, especially against Cormorant and TFN. (Fuchs et al., 2020) `ev:asserted` p. 9 ^fuchs2020se-050
- The authors conclude that adding attention to a roto-translation-equivariant model consistently led to higher accuracy in their experiments. (Fuchs et al., 2020) `ev:asserted` p. 9 ^fuchs2020se-051
- Specifically for large neighbourhoods, the authors found attention to be essential for convergence of the equivariant model. (Fuchs et al., 2020) `ev:asserted` p. 9 ^fuchs2020se-052
- Compared to conventional attention, adding the [[Equivariant neural network|equivariance constraints]] increased performance in all of the authors' experiments. (Fuchs et al., 2020) `ev:asserted` p. 9 ^fuchs2020se-053
- The authors state that guaranteed robustness to rotations and translations obviates the need for training-time data augmentation. (Fuchs et al., 2020) `ev:asserted` p. 9 ^fuchs2020se-054
- The authors are investigating the SE(3)-Transformer for early-stage suitability classification of molecules for inhibiting the coronavirus reproductive cycle. (Fuchs et al., 2020) `ev:asserted` p. 9 ^fuchs2020se-055
- For ScanObjectNN, the models used up to 200 of the 2024 available points per sample with up to 40 nearest neighbours. (Fuchs et al., 2020) `ev:reported` p. 18 ^fuchs2020se-056
- Swapping attention for convolution to obtain the Tensor Field baseline required decreasing the model size to obtain stable training. (Fuchs et al., 2020) `ev:measured` p. 18 ^fuchs2020se-057
- Storing intermediate associated Legendre polynomial computations speeds up average computation time by a factor of ∼10 on CPU. (Fuchs et al., 2020) `ev:measured` p. 18 ^fuchs2020se-058
- ScanObjectNN models were trained for 60000 steps with batch size 10 using Adam with a starting learning rate of 1e-2. (Fuchs et al., 2020) `ev:reported` p. 19 ^fuchs2020se-059
- Experiments with up to 2048 input points on ScanObjectNN gave no performance improvements over the 128 or 200 points used. (Fuchs et al., 2020) `ev:measured` p. 19 ^fuchs2020se-060
- Limited to 128 points, the SE(3)-Transformer reached 85.0 ± 0.7%, above DGCNN at 82.2 ± 0.8% and PointGLR at 81.5 ± 1.0%. (Fuchs et al., 2020) `ev:measured` p. 19 ^fuchs2020se-061
- In an input-point ablation, the SE(3)-Transformer reached 79.2% accuracy on ScanObjectNN when given 16 input points. (Fuchs et al., 2020) `ev:measured` p. 19 ^fuchs2020se-062
- For all tested training set sizes on ScanObjectNN, the SE(3)-Transformer outperformed the Set Transformer, a non-equivariant attention network. (Fuchs et al., 2020) `ev:measured` p. 19 ^fuchs2020se-063
- The authors state their results are in line with [[Equivariant neural network|equivariance]] decreasing sample complexity but do not give definitive support. (Fuchs et al., 2020) `ev:asserted` p. 19 ^fuchs2020se-064
- The N-body data comprised 5k training and 1k test simulations of 5 charged particles in a 3d setup. (Fuchs et al., 2020) `ev:reported` p. 20 ^fuchs2020se-065
- QM9 experiments used the exact same train/validation/test splits as Anderson et al., of sizes 100k/18k/13k. (Fuchs et al., 2020) `ev:reported` p. 20 ^fuchs2020se-066
- The QM9 architecture has 7 multihead attention layers interspersed with norm nonlinearities, followed by a TFN layer and max pooling. (Fuchs et al., 2020) `ev:reported` p. 20 ^fuchs2020se-067
- Switching from representation degrees {0, 1} to {0, 1, 2} gave a big performance improvement across the authors' SE(3)-Transformer experiments. (Fuchs et al., 2020) `ev:measured` p. 22 ^fuchs2020se-068
- The authors recommend representation degrees up to 2 when computation time and memory usage are a concern, and 3 otherwise. (Fuchs et al., 2020) `ev:asserted` p. 22 ^fuchs2020se-069

## 🎯 Contributions


## 📖 Glossary

- **SE(3)** — The group of 3D rotations and translations (roto-translations).
- **Equivariance** — Transforming the input produces a corresponding, predictable transformation of the output.
- **Type-ℓ vector** — Feature of length 2ℓ+1 transforming under the ℓ-th Wigner-D matrix.
- **Wigner-D matrix** — Irreducible representation of SO(3), of size (2ℓ+1)×(2ℓ+1).
- **Tensor field network (TFN)** — SE(3)-equivariant point-cloud convolution with spherical-harmonic angular and learned radial kernels.
- **Clebsch-Gordan coefficients** — Change-of-basis matrices decomposing tensor products of irreps into direct sums.
- **Self-interaction** — Per-node mixing of channels within one representation degree, akin to 1x1 convolution.
- **Attentive self-interaction** — Self-interaction whose weights come from an MLP over invariant inner products.
- **Equivariance error (∆EQ)** — Normalised distance between transformed outputs and outputs of transformed inputs.

## ❓ Open questions

- Would cascaded pooling via attention let the SE(3)-Transformer benefit from more than 128/200 input points?
- Does equivariance measurably reduce sample complexity, given the ScanObjectNN evidence is not definitive?
- Can combining equivariant attention with recurrent models (e.g. an LSTM) handle multi-step trajectory prediction?
- Would a left-regular representation, as in LieConv, close the QM9 gap to the best models?
- Can elements of dedicated point-classification architectures be combined with this geometric inductive bias for further gains?

## 📝 Notes on reading

Read the arXiv v3 (24 Nov 2020), the NeurIPS 2020 camera-ready version. Figure 3 (N-body predictions under input rotation) and Figure 4 (ScanObjectNN accuracy vs. maximum test rotation, with and without training augmentation) could only be described; their plotted values were not claimed. Figure 5 (spherical harmonics speed vs. lie_learn on CPU/GPU) gives only log-scale curves. Table 2 column order was garbled by extraction but values align with model names in order. Minor inconsistencies: the introduction says ≈22× speed up, Appendix C says ∼22×; Appendix D.1.1 says 2024 available points per sample while D.1.2 mentions experiments with up to 2048 points. Appendix D.2 states the linear baseline is SE(3) equivariant. The equivariance-error equations and associated Legendre polynomial recursions were only partially legible and were not claimed.

## Suggested new concepts

- SE(3)-equivariant attention — a family of geometric attention mechanisms central to 3D point-cloud and molecular learning.
- Tensor field networks — the equivariant convolution baseline this and many later models build on.
- Spherical harmonics and Wigner-D representations — the mathematical machinery underlying irreducible-representation equivariant networks.
- Equivariance error metric — a reusable way to verify exactness of learned symmetry.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Atención equivariante a $SE(3)$
