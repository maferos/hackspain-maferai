---
aliases: []
type: "source"
title: "Learning Lie Group Symmetry Transformations with Neural Networks"
citekey: "Gabel2023learning"
doi: "10.48550/arXiv.2307.01583"
arxiv: "2307.01583"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2307.01583"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Alex Gabel", "Victoria Klein", "Riccardo Valperga", "Jeroen S. W. Lamb", "Kevin Webster", "Rick Quax", "Efstratios Gavves"]
sha256: ["6872036f55ff9e1624606273be9758226922108f34921cd242519ff598fbd653"]
pdf: "Content/Papers/Gabel2023learning.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 49
---

📄 PDF: [[Gabel2023learning.pdf]]

> [!abstract] One-sentence summary
> The paper learns the generator of an unknown one-parameter Lie subgroup and the distribution of its transformation parameters from pairs of images, recovering rotations and translations on MNIST with a naive model and multimodal parameter distributions with a latent autoencoder model.

## Abstract

The problem of detecting and quantifying the presence of symmetries in datasets is useful for model selection, generative modeling, and data analysis, amongst others. While existing methods for hard-coding transformations in neural networks require prior knowledge of the symmetries of the task at hand, this work focuses on discovering and characterizing unknown symmetries present in the dataset, namely, Lie group symmetry transformations beyond the traditional ones usually considered in the field (rotation, scaling, and translation). Specifically, we consider a scenario in which a dataset has been transformed by a one-parameter subgroup of transformations with different parameter values for each data point. Our goal is to characterize the transformation group and the distribution of the parameter values. The results showcase the effectiveness of the approach in both these settings. (arXiv)

## 🧠 Key ideas (atomic)

- Restricting the hypothesis space of neural networks using known properties of data has been shown to improve performance in a variety of tasks. (Gabel et al., 2023) `ev:cited` p. 1 ^gabel2023learning-001
- The authors state that methods hard-coding transformations all require prior knowledge about symmetries to restrict the function space of a network. (Gabel et al., 2023) `ev:asserted` p. 1 ^gabel2023learning-002
- The authors argue that algorithms discovering and quantifying symmetries may play a crucial role in informing model selection for scientific discovery or computer vision. (Gabel et al., 2023) `ev:asserted` p. 2 ^gabel2023learning-003
- The work addresses qualitatively detecting the presence of symmetries with respect to one-parameter subgroups within a given dataset. (Gabel et al., 2023) `ev:asserted` p. 2 ^gabel2023learning-004
- The scenario assumes every point of a dataset was acted on by a one-parameter subgroup with a different parameter value per point. (Gabel et al., 2023) `ev:reported` p. 2 ^gabel2023learning-005
- The stated goal is to characterise the group of transformations as well as the distribution from which the parameters were sampled. (Gabel et al., 2023) `ev:asserted` p. 2 ^gabel2023learning-006
- The authors propose a naive model that successfully manages to identify the underlying one-parameter subgroup of the transformed dataset. (Gabel et al., 2023) `ev:asserted` p. 2 ^gabel2023learning-007
- A second autoencoder model learns one-parameter subgroup transformations in latent space and is capable of extracting the overall shape of the parameter distributions. (Gabel et al., 2023) `ev:asserted` p. 2 ^gabel2023learning-008
- The cost of the autoencoder model is that its latent one-parameter subgroup is not necessarily identical to the subgroup in pixel space. (Gabel et al., 2023) `ev:asserted` p. 2 ^gabel2023learning-009
- The semi-supervised setting learns the generator from pairs of an observation and its transformed version, with parameters drawn from an unknown distribution. (Gabel et al., 2023) `ev:reported` p. 2 ^gabel2023learning-010
- The authors describe the matrix Lie group formulation as more restrictive, since groups such as translations cannot be written as matrix multiplication. (Gabel et al., 2023) `ev:asserted` p. 2 ^gabel2023learning-011
- For two-dimensional data the generator is parametrised as a linear operator in the basis {1, x, y} with a coefficient matrix α. (Gabel et al., 2023) `ev:reported` p. 3 ^gabel2023learning-012
- In this basis the generator can express one-parameter subgroups of the affine group, including translation, rotation, and isotropic scaling. (Gabel et al., 2023) `ev:asserted` p. 3 ^gabel2023learning-013
- The authors state the parametrisation can be generalized to any functional form of the generator by augmenting the basis accordingly. (Gabel et al., 2023) `ev:asserted` p. 3 ^gabel2023learning-014
- Images are vectorised from a regularly-sampled grid, so the generator becomes a matrix operator whose exponential is the matrix exponential. (Gabel et al., 2023) `ev:reported` p. 3 ^gabel2023learning-015
- Derivative operators at discrete grid locations are built with Shannon-Whittaker interpolation, assuming the sampled function is periodic. (Gabel et al., 2023) `ev:reported` p. 4 ^gabel2023learning-016
- The authors note that alternative interpolation techniques can be used, since the method does not depend on any specific one. (Gabel et al., 2023) `ev:asserted` p. 4 ^gabel2023learning-017
- The naive model learns generator coefficients shared across the dataset, with an MLP predicting the parameter from each input pair. (Gabel et al., 2023) `ev:reported` p. 4 ^gabel2023learning-018
- The naive model objective is a reconstruction loss between the exponentially transformed input and the observed transformed data point. (Gabel et al., 2023) `ev:reported` p. 4 ^gabel2023learning-019
- The matrix exponential in the naive model can be costly to compute and difficult to optimise in high dimensions. (Gabel et al., 2023) `ev:asserted` p. 4 ^gabel2023learning-020
- The cost of the matrix exponential in a single forward pass is roughly O(n3) using the algorithm of Al-Mohy and Higham. (Gabel et al., 2023) `ev:cited` p. 4 ^gabel2023learning-021
- The latent model adds an MLP autoencoder mapping inputs to a lower-dimensional latent space where the exponential is taken instead. (Gabel et al., 2023) `ev:reported` p. 4 ^gabel2023learning-022
- Enforcing good reconstruction of the autoencoder alone does not enforce commutativity of the diagram linking data-space and latent-space transformations. (Gabel et al., 2023) `ev:asserted` p. 4 ^gabel2023learning-023
- The latent model loss is a weighted sum of autoencoder reconstruction, original-space and latent-space transformation reconstruction, plus a Lasso term. (Gabel et al., 2023) `ev:reported` p. 4 ^gabel2023learning-024
- The generator learned in latent space and the generator of the original-space action are not necessarily the same one-parameter subgroup. (Gabel et al., 2023) `ev:asserted` p. 5 ^gabel2023learning-025
- In both models the decomposition of the parameter-generator product is unique only up to a constant, so generators are recovered up to scale. (Gabel et al., 2023) `ev:asserted` p. 5 ^gabel2023learning-026
- The one-parameter subgroup can only be deduced from the generator coefficients relative to one another, not in absolute terms. (Gabel et al., 2023) `ev:asserted` p. 5 ^gabel2023learning-027
- The models recover a scaled approximation for the distribution of the transformation parameters rather than the exact distribution. (Gabel et al., 2023) `ev:asserted` p. 5 ^gabel2023learning-028
- The authors leave the fully unsupervised setting for future work, saying the method could in principle apply without substantial architectural changes. (Gabel et al., 2023) `ev:asserted` p. 5 ^gabel2023learning-029
- Experiments use MNIST digits transformed with either 2D rotations or translations in one direction, with parameters sampled from multimodal distributions. (Gabel et al., 2023) `ev:reported` p. 5 ^gabel2023learning-030
- Signals are regularly sampled from a grid with n = 28 and vectorised into points in R784. (Gabel et al., 2023) `ev:reported` p. 5 ^gabel2023learning-031
- The naive model uses a fully-connected 3-layer MLP trained jointly with the generator coefficients using Adam with a learning rate of 0.001. (Gabel et al., 2023) `ev:reported` p. 5 ^gabel2023learning-032
- Updating the generator coefficients roughly 10 times for every MLP update was found to be beneficial during training. (Gabel et al., 2023) `ev:measured` p. 5 ^gabel2023learning-033
- After a few hundred training steps, coefficients not corresponding to the generator of the dataset symmetry drop to zero. (Gabel et al., 2023) `ev:measured` p. 5 ^gabel2023learning-034
- The coefficients that do correspond to the dataset symmetry settle to values compatible with those of the ground truth generator. (Gabel et al., 2023) `ev:measured` p. 5 ^gabel2023learning-035
- Figure 4 shows the learned coefficients converging to the ground-truth non-zero coefficients for both rotated MNIST and translated MNIST. (Gabel et al., 2023) `ev:measured` p. 6 ^gabel2023learning-036
- The latent model uses 3-layer MLPs for the parameter network, the encoder, and the decoder, with the latent space set to nZ = 25. (Gabel et al., 2023) `ev:reported` p. 6 ^gabel2023learning-037
- After every epoch of roughly 500 steps, the predicted parameters were collected in a histogram to show their distribution. (Gabel et al., 2023) `ev:reported` p. 6 ^gabel2023learning-038
- The latent model clearly recovers multimodal parameter distributions, showing the same number of modes as the ground truth distribution. (Gabel et al., 2023) `ev:measured` p. 6 ^gabel2023learning-039
- Rao & Ruderman (1998) and Miao & Rao (2007) were the first works learning one-parameter subgroup symmetries from observations, using MAP inference. (Gabel et al., 2023) `ev:cited` p. 7 ^gabel2023learning-040
- Sohl-Dickstein et al. (2010) do not consider characterizing the distribution of the subgroup parameter, according to the authors. (Gabel et al., 2023) `ev:cited` p. 7 ^gabel2023learning-041
- Dehmamy et al. (2021) require knowledge of the specific transformation parameter for each input pair, unlike the proposed model. (Gabel et al., 2023) `ev:cited` p. 7 ^gabel2023learning-042
- Benton et al. (2020) learn invariance groups with an objective constraining the network parameters and the augmentation parameter distribution. (Gabel et al., 2023) `ev:cited` p. 7 ^gabel2023learning-043
- Keurti et al. (2023) and Zhu et al. (2021) have learned transformations of a one-parameter subgroup in latent space. (Gabel et al., 2023) `ev:cited` p. 7 ^gabel2023learning-044
- The authors state that learned symmetries can be incorporated into equivariant models after training or used for data augmentation downstream. (Gabel et al., 2023) `ev:asserted` p. 7 ^gabel2023learning-045
- The framework is presented as performing symmetry detection in pixel-space without assuming any inductive biases are present in the data a priori. (Gabel et al., 2023) `ev:asserted` p. 7 ^gabel2023learning-046
- The authors state their generator parametrisation lets non-compact groups such as translation be naturally incorporated into the framework. (Gabel et al., 2023) `ev:asserted` p. 7 ^gabel2023learning-047
- The authors acknowledge that learning both the generator coefficients and the parameter distribution was not accomplished by one model in this work. (Gabel et al., 2023) `ev:asserted` p. 7 ^gabel2023learning-048
- The authors suggest composing the method into multiple layers could handle datasets expressing multiple symmetries, ideally with one symmetry per layer. (Gabel et al., 2023) `ev:asserted` p. 7 ^gabel2023learning-049

## 🎯 Contributions

## 📖 Glossary

- **One-parameter subgroup** — A differentiable homomorphism from the real line into a Lie group G.
- **Generator** — Linear differential operator whose exponential yields the one-parameter subgroup action on data.
- **Matrix exponential** — Power series of a matrix operator, used here to apply the learned transformation.
- **Shannon-Whittaker interpolation** — Reconstruction of a band-limited signal from equally spaced samples.
- **Symmetry detection** — Discovering which transformations leave data or object identity invariant, from observations.
- **Latent model** — Autoencoder variant learning the subgroup action in a low-dimensional latent space.
- **Lasso term** — Penalty on generator coefficients encouraging sparse coefficient solutions.

## ❓ Open questions

- Can a single model learn both the generator coefficients and the parameter distribution, which the naive and latent models each achieve only in part?
- How can the pixel-space subgroup be recovered from the latent-space generator, given the two need not coincide?
- Does the method work in the fully unsupervised setting where only a labelled transformed dataset is available?
- Can stacked layers disentangle datasets that express multiple symmetries at once?
- How does the approach scale beyond 28 by 28 MNIST, given the roughly cubic cost of the matrix exponential?
- Do the results hold for non-affine transformations or other bases, which the paper says are possible but does not test?
- How sensitive are results to the loss weights and to the 10-to-1 update ratio between coefficients and MLP?

## 📝 Notes on reading

Version read: arXiv v1 (2307.01583v1, 4 Jul 2023), a short workshop paper for TAG-ML at ICML 2023; the packet identifier is the same arXiv record.

Results are only qualitative: Figure 4 (coefficient trajectories for rotation and translation in x) and Figure 5 (histograms of predicted parameters for unimodal, bimodal, 3-mode and 5-mode distributions) are described, with no numeric error metrics, baselines, or tables. Figure 4 gives the ground-truth coefficients as −α22 = α13 = 1 for rotation and α11 = 1 for translation.

Inconsistencies inside the paper: Eq. (5) indexes coefficients as α11, α12, α23 in the first term and α12, α22, α23 in the second, while Eq. (6) uses α11, α12, α13 and α21, α22, α23, so Eq. (5) appears to contain typos. The paragraph Recovering the group (p. 5) swaps the roles of Lα and L˜α relative to the definitions on p. 4. Section 3.2 calls the first architecture the main model while its subsection names it the naive model. The latent model experiment says fθ was trained jointly with αij, though the latent model learns ˜α. The intro says the naive model identifies the subgroup and the latent model extracts distribution shapes; the experiments report coefficients only for the naive model and distributions only for the latent model, which matches the Discussion limitation. The abstract says the results showcase effectiveness in both settings, but no quantitative evaluation is given.

The naive model code is said to be available, but the link did not survive extraction.

## Suggested new concepts

- Lie group symmetry discovery — a recurring task of learning unknown generators from data that links several related works cited here.
- One-parameter subgroup — the basic mathematical object the method learns; deserves its own definition note.
- Lie algebra generator parametrisation — the choice of basis determines which transformations can be learned, a design lever shared across methods.
- Equivariant neural networks — the downstream consumer of discovered symmetries, repeatedly contrasted with hard-coded approaches.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Descubrimiento de generadores de simetrías

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
