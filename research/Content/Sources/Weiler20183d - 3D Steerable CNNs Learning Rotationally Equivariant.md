---
aliases: []
type: "source"
title: "3D Steerable CNNs: Learning Rotationally Equivariant Features in Volumetric Data"
citekey: "Weiler20183d"
doi: "10.48550/arXiv.1807.02547"
arxiv: "1807.02547"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1807.02547"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Maurice Weiler", "Mario Geiger", "Max Welling", "Wouter Boomsma", "Taco Cohen"]
sha256: ["cb1b094979494f5fb8dad0af247ef5b77ffd9f7f60d8ae63e24239cee584ba5f"]
pdf: "Content/Papers/Weiler20183d.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Weiler20183d.pdf]]

> [!abstract] One-sentence summary
> The paper derives a complete analytic basis of SE(3)-steerable kernels for voxel CNNs, proves such convolutions are the most general equivariant linear maps between fields over R3, and shows strong accuracy and parameter efficiency on rotated Tetris, SHREC17, amino acid environments and a new CATH protein dataset.

## Abstract

We present a convolutional network that is equivariant to rigid body motions. The model uses scalar-, vector-, and tensor fields over 3D Euclidean space to represent data, and equivariant convolutions to map between such representations. These SE(3)-equivariant convolutions utilize kernels which are parameterized as a linear combination of a complete steerable kernel basis, which is derived analytically in this paper. We prove that equivariant convolutions are the most general equivariant linear maps between fields over R^3. Our experimental results confirm the effectiveness of 3D Steerable CNNs for the problem of amino acid propensity prediction and protein structure classification, both of which have inherent SE(3) symmetry. (arXiv)

## 🧠 Key ideas (atomic)

- The paper develops SE(3)-equivariant convolutional networks, which the authors describe as non-trivial because SE(3) is both non-commutative and non-compact. (Weiler et al., 2018) `ev:asserted` p. 1 ^weiler20183d-001
- At run-time, all that is required to make a 3D convolution equivariant is parameterizing its kernel as a combination of pre-computed steerable basis kernels. (Weiler et al., 2018) `ev:asserted` p. 1 ^weiler20183d-002
- Unlike [[Tensor Field Network|Tensor Field Networks]] and N-Body networks, which work on irregular point clouds, [[Steerable CNN|3D Steerable CNNs]] operate on regular 3D grids. (Weiler et al., 2018) `ev:cited` p. 2 ^weiler20183d-003
- The authors state that point clouds are more general, but regular grids can be processed more efficiently on current hardware. (Weiler et al., 2018) `ev:asserted` p. 2 ^weiler20183d-004
- The authors describe the Clebsch-Gordan coefficient tensors used by TFN and NBN as tricky to work with, having 6 indices and convention dependence. (Weiler et al., 2018) `ev:cited` p. 2 ^weiler20183d-005
- In contrast to [[Tensor Field Network|TFN]], the filter basis is derived directly from an equivariance constraint, which lets the authors prove its completeness. (Weiler et al., 2018) `ev:asserted` p. 2 ^weiler20183d-006
- Regular 3D G-CNNs operating on voxelized data were shown to achieve superior data efficiency over conventional 3D CNNs in medical imaging and 3D model recognition. (Weiler et al., 2018) `ev:cited` p. 2 ^weiler20183d-007
- The earlier regular 3D G-CNNs are equivariant only to certain discrete rotations, in contrast to the continuous equivariance of [[Steerable CNN|3D Steerable CNNs]]. (Weiler et al., 2018) `ev:cited` p. 2 ^weiler20183d-008
- Earlier spherical tensor algebra methods expanded signals in terms of spherical tensor fields, but this expansion was fixed and not learned. (Weiler et al., 2018) `ev:cited` p. 2 ^weiler20183d-009
- Feature spaces are modeled as stacks of fields, each assigning a geometrical quantity such as a scalar, vector or tensor to every point. (Weiler et al., 2018) `ev:asserted` p. 3 ^weiler20183d-010
- Under rigid body motions, information flows within the channels of a single geometrical quantity but not between different quantities, known as Weyl's principle. (Weiler et al., 2018) `ev:cited` p. 3 ^weiler20183d-011
- A rank-2 tensor decomposes into irreducible representations of dimension 1, 3 and 5, namely its trace, anti-symmetric and traceless symmetric parts. (Weiler et al., 2018) `ev:asserted` p. 4 ^weiler20183d-012
- Since any SO(3) representation decomposes into irreducibles of dimension 2l + 1, the networks use only irreducible features in every layer. (Weiler et al., 2018) `ev:asserted` p. 4 ^weiler20183d-013
- Theorem 2 proves that a linear map between the field spaces is equivariant if and only if it is a cross-correlation with a rotation-steerable kernel. (Weiler et al., 2018) `ev:computed` p. 5 ^weiler20183d-014
- Because the steerability constraint is linear in the kernel, the equivariant kernels form a vector space for which the authors compute a basis. (Weiler et al., 2018) `ev:computed` p. 5 ^weiler20183d-015
- The tensor product of Wigner-D representations of orders j and l decomposes into 2 min(j, l) + 1 irreducible representations. (Weiler et al., 2018) `ev:cited` p. 6 ^weiler20183d-016
- The equivariant kernel basis consists of spherical harmonics modulated by an arbitrary continuous radial function, since the constraint restricts only the angular part. (Weiler et al., 2018) `ev:computed` p. 6 ^weiler20183d-017
- Following earlier work, the implementation uses Gaussian radial shells as the radial basis functions that multiply the spherical harmonics of the kernel basis. (Weiler et al., 2018) `ev:reported` p. 6 ^weiler20183d-018
- In the forward pass, basis kernels are linearly combined with learnable weights and stacked into a kernel passed to a standard 3D convolution routine. (Weiler et al., 2018) `ev:reported` p. 6 ^weiler20183d-019
- The authors state that, unlike regular G-CNNs, [[Steerable CNN|steerable G-CNNs]] require special equivariant nonlinearities rather than arbitrary elementwise ones. (Weiler et al., 2018) `ev:asserted` p. 6 ^weiler20183d-020
- The paper introduces a gated nonlinearity that multiplies each non-scalar feature by a sigmoid scalar gate computed with another learnable steerable kernel. (Weiler et al., 2018) `ev:reported` p. 7 ^weiler20183d-021
- Scalar fields do not transform under rotations, so conventional nonlinearities such as ReLUs or sigmoids are applied to them in the network. (Weiler et al., 2018) `ev:reported` p. 7 ^weiler20183d-022
- To prevent aliasing on the discrete grid, a radius-dependent bandlimit restricts which spherical harmonic orders are used, particularly near the kernel origin. (Weiler et al., 2018) `ev:reported` p. 7 ^weiler20183d-023
- The radial Gaussian windows of the kernel basis use integer means up to ⌊s/2⌋ and a fixed width of σ = 0.6. (Weiler et al., 2018) `ev:reported` p. 7 ^weiler20183d-024
- The authors compute the change of basis matrix Q by numerically solving Eq. 14 instead of expressing it through Clebsch-Gordan coefficients. (Weiler et al., 2018) `ev:reported` p. 7 ^weiler20183d-025
- The authors found that performance depends critically on downsampling, with strided convolutions performing poorly compared to smoothing feature maps before subsampling. (Weiler et al., 2018) `ev:measured` p. 7 ^weiler20183d-026
- Applying low pass filtering before downsampling, via a Gaussian strided convolution or average pooling, gave significant improvements of rotational equivariance. (Weiler et al., 2018) `ev:measured` p. 7 ^weiler20183d-027
- Once trained, the steerable network can be converted into a standard 3D CNN by storing only the combined filter bank. (Weiler et al., 2018) `ev:asserted` p. 7 ^weiler20183d-028
- A 4-layer 3D Steerable CNN was trained on 8 kinds of Tetris blocks in fixed orientation and tested on randomly rotated blocks. (Weiler et al., 2018) `ev:reported` p. 8 ^weiler20183d-029
- On randomly rotated Tetris test blocks, the [[Steerable CNN|3D Steerable CNN]] achieved 99±2% accuracy, whereas a conventional CNN reached only 27±7% over 17 runs. (Weiler et al., 2018) `ev:measured` p. 8 ^weiler20183d-030
- The SHREC17 task contains 51300 models of 3D shapes in 55 classes and includes a perturbed category with arbitrarily rotated shapes. (Weiler et al., 2018) `ev:cited` p. 8 ^weiler20183d-031
- Without extensive fine-tuning, the model with 64x64x64 voxel inputs performed comparably to the current state of the art on SHREC17. (Weiler et al., 2018) `ev:measured` p. 8 ^weiler20183d-032
- The authors report that internal fields respond remarkably stably to rotations of the input, shown in a visualization movie rather than a metric. (Weiler et al., 2018) `ev:measured` p. 8 ^weiler20183d-033
- A prior amino acid environment study reported 0.56 accuracy with concentric grid convolutions versus 0.50 with standard regular-grid 3D convolutions. (Weiler et al., 2018) `ev:cited` p. 8 ^weiler20183d-034
- The amino acid model reused the original network with steerable layers, using 32.6M parameters against 61.1M for the regular-grid original. (Weiler et al., 2018) `ev:reported` p. 8 ^weiler20183d-035
- On amino acid propensity prediction, the 3D Steerable CNN obtained a test accuracy of 0.58, improving over the state of the art on this problem. (Weiler et al., 2018) `ev:measured` p. 8 ^weiler20183d-036
- The amino acid environments are oriented by the protein backbone, whereas the CATH shape classification task was chosen to have no inherent orientation. (Weiler et al., 2018) `ev:asserted` p. 8 ^weiler20183d-037
- The authors built a new dataset from CATH version 4.2 at the architecture level, which reflects how secondary structure elements are arranged in space. (Weiler et al., 2018) `ev:reported` p. 9 ^weiler20183d-038
- Keeping CATH architectures with at least 500 proteins left 10 categories, each balanced to 711 structures with no pair above 40% sequence identity. (Weiler et al., 2018) `ev:reported` p. 9 ^weiler20183d-039
- The CATH baseline is a ResNet34-inspired 3D CNN with half the original channels and global pooling, established through a range of architecture experiments. (Weiler et al., 2018) `ev:reported` p. 9 ^weiler20183d-040
- The steerable CATH network allocates equal numbers of fields of order l = 0, 1, 2, 3 in each layer except the last, scalar-only layer. (Weiler et al., 2018) `ev:reported` p. 9 ^weiler20183d-041
- The steerable CATH network contains only 143, 560 parameters, which is more than a factor hundred fewer than the conventional baseline. (Weiler et al., 2018) `ev:reported` p. 9 ^weiler20183d-042
- CATH models were trained for 100 epochs with Adam, using exponential learning rate decay of 0.94 per epoch after a 40-epoch burn-in. (Weiler et al., 2018) `ev:reported` p. 9 ^weiler20183d-043
- The authors note that, due to their [[Equivariant neural network|rotational equivariance]], [[Steerable CNN|3D Steerable CNNs]] benefit only marginally from rotational data augmentation compared to the baseline. (Weiler et al., 2018) `ev:asserted` p. 9 ^weiler20183d-044
- Despite having 100 times fewer parameters, the [[Steerable CNN|3D Steerable CNN]] showed a clear accuracy benefit over the baseline on the CATH test set. (Weiler et al., 2018) `ev:measured` p. 9 ^weiler20183d-045
- The steerable model outperformed the baseline CNN on CATH even when each training split was reduced by increasing powers of two. (Weiler et al., 2018) `ev:measured` p. 9 ^weiler20183d-046
- The authors conclude that convolutions with SO(3)-steerable filters are the most general equivariant maps between fields, establishing SE(3)-equivariant networks as a universal class. (Weiler et al., 2018) `ev:asserted` p. 9 ^weiler20183d-047
- The authors leave a more detailed investigation of the choice of feature types and multiplicities, a network hyperparameter, to future work. (Weiler et al., 2018) `ev:asserted` p. 13 ^weiler20183d-048
- According to the authors, using only scalar fields restricts kernels to be isotropic, whereas higher order representations allow more complex kernels. (Weiler et al., 2018) `ev:asserted` p. 13 ^weiler20183d-049
- The equivariant batch normalization scales each non-scalar field by the inverse square root of the batch average of its squared norms. (Weiler et al., 2018) `ev:reported` p. 13 ^weiler20183d-050
- Norm nonlinearities tended to converge slower than gated nonlinearities in practice, so they were not used in the final experiments. (Weiler et al., 2018) `ev:measured` p. 14 ^weiler20183d-051
- The authors found that gated nonlinearities work better in practice than the norm and tensor product nonlinearities they also tried. (Weiler et al., 2018) `ev:measured` p. 14 ^weiler20183d-052
- To test whether fewer parameters would also help the conventional CNN, the authors trained a series of conventional CNNs with fewer filters per layer. (Weiler et al., 2018) `ev:reported` p. 15 ^weiler20183d-053
- The relative performance gain of the steerable model increases dramatically when the conventional CNN is restricted to the same number of parameters. (Weiler et al., 2018) `ev:measured` p. 15 ^weiler20183d-054
- In the Tetris experiment, the SE3 network has 41k parameters, whereas the unconstrained CNN with the same feature map sizes has 6M. (Weiler et al., 2018) `ev:reported` p. 15 ^weiler20183d-055
- Without low pass filtering, rotated Tetris test accuracy was 36% ± 6% for the SE3 network and 24% ± 4% for the CNN. (Weiler et al., 2018) `ev:measured` p. 16 ^weiler20183d-056
- The SHREC17 steerable network has 142k parameters, against 0.5M for Esteves and 8.4M for Furuya in the comparison table. (Weiler et al., 2018) `ev:reported` p. 16 ^weiler20183d-057
- On SHREC17, the model obtained a total score of 1.11 and micro mAP of 0.661, compared with a total score of 1.13 for Furuya. (Weiler et al., 2018) `ev:measured` p. 16 ^weiler20183d-058
- CATH structures were simplified to Cα atoms, voxelized with each voxel spanning 0.2 nm and Gaussian densities placed at atom positions. (Weiler et al., 2018) `ev:reported` p. 16 ^weiler20183d-059
- Proteins extending beyond a 5 nm sphere around their center of mass were excluded, which the authors say affects only a small fraction. (Weiler et al., 2018) `ev:reported` p. 16 ^weiler20183d-060
- Any two members from different CATH splits are guaranteed to originate from different superfamilies, and every split contains all 10 architectures. (Weiler et al., 2018) `ev:reported` p. 17 ^weiler20183d-061
- The CATH baseline CNN settled on a 0.01 dropout rate in convolutional layers with L1 and L2 regularization values of 10−7. (Weiler et al., 2018) `ev:reported` p. 17 ^weiler20183d-062
- The steerable CATH model used a capsule-wide convolutional dropout rate of 0.1 with L1 and L2 regularization values of 10−8.5. (Weiler et al., 2018) `ev:reported` p. 17 ^weiler20183d-063

## 🎯 Contributions

## 📖 Glossary

- **SE(3)** — Group of 3D rigid body motions, combining rotations and translations.
- **Steerable kernel** — Convolution kernel whose rotated version equals a representation-transformed copy of itself.
- **Induced representation** — Action of SE(3) on a field, moving fibers and rotating them by ρ.
- **Irreducible representation** — Representation with no invariant subspace; for SO(3) of dimension 2l + 1.
- **Wigner-D matrix** — Irreducible SO(3) representation matrix of order l acting on 2l + 1 dimensions.
- **Intertwiner** — Linear map between feature spaces that commutes with the group action.
- **Gated nonlinearity** — Scales a non-scalar field by a sigmoid of an associated learned scalar field.
- **Norm nonlinearity** — Nonlinearity acting on a feature vector's norm while preserving its orientation.
- **Spherical harmonics** — Angular basis functions Y^J solving the rotational constraint on each kernel subspace.
- **CATH architecture level** — CATH classification tier describing the spatial arrangement of secondary structure elements.

## ❓ Open questions

- How should the types and multiplicities of fields be chosen per layer; the authors leave this to future work.
- Can a proper initialization scale for norm nonlinearity biases make them converge as fast as gated nonlinearities?
- How does the grid-based approach compare in accuracy and cost with point-cloud models such as TFN on the same tasks?
- How much rotational equivariance is lost to discretization and aliasing on coarse grids, measured quantitatively?
- Does the data-efficiency advantage on CATH hold with full-atom inputs rather than Cα-only densities?

## 📝 Notes on reading

Read the arXiv v2 (27 Oct 2018), the NIPS 2018 camera-ready with the supplementary material appended (pp. 13–17).

Figure 3 (p. 8) plots SHREC17 score (micro mAP + macro mAP) against parameter count; the steerable model sits near the top with the fewest parameters. Figure 4 (p. 9) plots CATH test accuracy (about 0.50–0.65) against training set reduction factors 2^0–2^4, with the steerable CNN above the 3D CNN throughout; exact values are not tabulated, so the leftmost accuracy is not claimed. Figure 6 (p. 15) plots test accuracy against parameter count for conventional CNNs of varying width. Figure 2 shows the angular kernel basis for j = l = 1 (identity, curl, gradient of divergence).

Table 1 (p. 15, Tetris architecture) is garbled in extraction (superscript sizes such as 363, 403 read as integers); per-layer sizes are not claimed. The CATH grid size "503vx" (p. 16) is likely 50^3 voxels but is garbled and not claimed. The Figure 1 caption writes Ind_{SO(3)}^{SE(2)}, apparently a typo for SE(3).

The body (p. 9) and supplement (p. 17) both state the baseline has 15, 878, 764 parameters; only the ratio and the steerable count are claimed. The amino acid comparison model on p. 8 also has 75.3M parameters in its concentric representation.

## Suggested new concepts

- Steerable CNN — general framework of equivariant networks using fields and steerable kernels, shared across 2D and 3D works.
- SE(3) equivariance — central symmetry property for molecular and volumetric learning, recurring across many sources.
- Gated nonlinearity — equivariant activation introduced here and reused in later equivariant architectures.
- Kernel aliasing in discretized equivariant convolutions — practical issue with specific remedies (bandlimits, low pass downsampling).
- CATH protein structure benchmark — dataset introduced here for rotation-invariant protein classification.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Convoluciones equivariantes a SE(3) en datos volumétricos.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
