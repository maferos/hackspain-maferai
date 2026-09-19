---
aliases: []
type: "source"
title: "e3nn: Euclidean Neural Networks"
citekey: "Geiger2022e3nn"
doi: "10.48550/arXiv.2207.09453"
arxiv: "2207.09453"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2207.09453"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Mario Geiger", "Tess Smidt"]
sha256: ["c04b2de728eb8c0d06405043ee4fb0eea666ac6c9615a396f1579a35d4bceedc"]
pdf: "Content/Papers/Geiger2022e3nn.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 66
---

📄 PDF: [[Geiger2022e3nn.pdf]]

> [!abstract] One-sentence summary
> The paper presents e3nn, a PyTorch library whose general TensorProduct, spherical harmonics and irrep primitives let researchers compose any E(3)-equivariant network for 3D data.

## Abstract

We present e3nn, a generalized framework for creating E(3) equivariant trainable functions, also known as Euclidean neural networks. e3nn naturally operates on geometry and geometric tensors that describe systems in 3D and transform predictably under a change of coordinate system. The core of e3nn are equivariant operations such as the TensorProduct class or the spherical harmonics functions that can be composed to create more complex modules such as convolutions and attention mechanisms. These core operations of e3nn can be used to efficiently articulate Tensor Field Networks, 3D Steerable CNNs, Clebsch-Gordan Networks, SE(3) Transformers and other E(3) equivariant networks. (arXiv)

## 🧠 Key ideas (atomic)

- Coordinates and coordinate systems make 3D geometry and geometric tensors challenging for machine learning because they are sensitive to 3D symmetries. (Geiger & Smidt, 2022) `ev:asserted` p. 2 ^geiger2022e3nn-001
- The authors motivate building symmetry into 3D models by eliminating data augmentation, described as a 500-fold increase in brute-force training. (Geiger & Smidt, 2022) `ev:asserted` p. 2 ^geiger2022e3nn-002
- Invariant models, which operate only on scalars, cannot predict an l > 0 quantity that would change with rotation of the input data. (Geiger & Smidt, 2022) `ev:asserted` p. 2 ^geiger2022e3nn-003
- Models restricted to l = 0 and l = 1 are expressive enough to be universal, fitting any equivariant function of output l ≤1. (Geiger & Smidt, 2022) `ev:cited` p. 2 ^geiger2022e3nn-004
- Models including internal representations of order l = 2 have been observed to display a better learning curve than models with only l ≤1. (Geiger & Smidt, 2022) `ev:cited` p. 3 ^geiger2022e3nn-005
- The authors state that implementing equivariant neural networks can be technical and error prone, which motivated them to develop a Python library. (Geiger & Smidt, 2022) `ev:asserted` p. 3 ^geiger2022e3nn-006
- e3nn is built to take care of the intricacies of geometric tensor algebra so that users can focus on building trainable modules. (Geiger & Smidt, 2022) `ev:asserted` p. 3 ^geiger2022e3nn-007
- In January 2021 the many different functions of early e3nn versions were fused into a unified parameterizable operation called TensorProduct. (Geiger & Smidt, 2022) `ev:reported` p. 3 ^geiger2022e3nn-008
- Most symmetry-aware neural networks used in the molecules and materials community are invariant models whose operations act on scalar quantities. (Geiger & Smidt, 2022) `ev:cited` p. 3 ^geiger2022e3nn-009
- DimeNet uses angular information between triplets of atoms by pre-computing these angles and using the resulting scalars in network operations. (Geiger & Smidt, 2022) `ev:cited` p. 3 ^geiger2022e3nn-010
- Restricted equivariant methods that use only scalar or vector operations are a strict subset of the operations allowed in an equivariant network. (Geiger & Smidt, 2022) `ev:cited` p. 3 ^geiger2022e3nn-011
- Many papers have documented improved accuracy on training tasks when going from invariant to [[Equivariant neural network|equivariant models]], even within the same framework. (Geiger & Smidt, 2022) `ev:cited` p. 3 ^geiger2022e3nn-012
- An important goal for e3nn is to provide a flexible framework expressing the most general equivariant operations for all forms of 3D data. (Geiger & Smidt, 2022) `ev:asserted` p. 4 ^geiger2022e3nn-013
- The authors state that all the related methods they discuss can be succinctly articulated with the operations of e3nn. (Geiger & Smidt, 2022) `ev:asserted` p. 4 ^geiger2022e3nn-014
- e3nn and Euclidean neural networks have been applied to diverse tasks, including prediction of phonon density of states and of interatomic potentials. (Geiger & Smidt, 2022) `ev:cited` p. 4 ^geiger2022e3nn-015
- e3nn implements parity equivariance so that its models are equivariant to O(3) rather than only to SO(3). (Geiger & Smidt, 2022) `ev:reported` p. 4 ^geiger2022e3nn-016
- The ReduceTensorProduct class decomposes tensors of arbitrary rank, including index symmetry constraints, onto a direct sum of irreps of O(3). (Geiger & Smidt, 2022) `ev:reported` p. 4 ^geiger2022e3nn-017
- The authors emphasize that the e3nn methods are useful for any tensor computations, not only in a deep learning context. (Geiger & Smidt, 2022) `ev:asserted` p. 4 ^geiger2022e3nn-018
- In Euclidean neural networks all data are typed by how they transform under the Euclidean group, described by group representations. (Geiger & Smidt, 2022) `ev:asserted` p. 5 ^geiger2022e3nn-019
- The data types of e3nn are the irreducible representations of O(3), which factorize into the irreps of SO(3) and of parity. (Geiger & Smidt, 2022) `ev:reported` p. 5 ^geiger2022e3nn-020
- Irreducible representations are used because they are the smallest representations and any finite dimensional O(3) representation decomposes onto them. (Geiger & Smidt, 2022) `ev:asserted` p. 5 ^geiger2022e3nn-021
- The irreps of SO(3) are indexed by an integer l, with the l-irrep having dimension 2l + 1. (Geiger & Smidt, 2022) `ev:cited` p. 5 ^geiger2022e3nn-022
- A symmetric 3 × 3 Cartesian matrix decomposes into one l = 0 trace scalar plus 5 symmetric traceless l = 2 components. (Geiger & Smidt, 2022) `ev:computed` p. 6 ^geiger2022e3nn-023
- The cross product of two vectors gives rise to an even quantity, a pseudovector, which does not change under inversion of the frame. (Geiger & Smidt, 2022) `ev:asserted` p. 6 ^geiger2022e3nn-024
- Requiring each individual network operation to be equivariant guarantees equivariance of the entire network, since compositions of equivariant functions are equivariant. (Geiger & Smidt, 2022) `ev:computed` p. 6 ^geiger2022e3nn-025
- e3nn requires learned parameters to be scalars, which implies that the weights are invariant under any choice of coordinate system. (Geiger & Smidt, 2022) `ev:reported` p. 6 ^geiger2022e3nn-026
- For memory and computation reasons, e3nn opted to use real numbers for its irreducible representations instead of the usual complex basis. (Geiger & Smidt, 2022) `ev:reported` p. 7 ^geiger2022e3nn-027
- e3nn obtains the representations in the usual basis using code from QuTip, then applies a change of basis to real numbers. (Geiger & Smidt, 2022) `ev:reported` p. 7 ^geiger2022e3nn-028
- The e3nn spherical harmonics are normalized to unit norm on the unit sphere, a normalization named norm in the e3nn code. (Geiger & Smidt, 2022) `ev:reported` p. 7 ^geiger2022e3nn-029
- Once the basis of irreps is fixed, the spherical harmonics on the unit sphere are unique up to the choice of their sign. (Geiger & Smidt, 2022) `ev:computed` p. 8 ^geiger2022e3nn-030
- When extended from the unit sphere to the full space R3, the spherical harmonics can be chosen to be polynomials of the position. (Geiger & Smidt, 2022) `ev:computed` p. 8 ^geiger2022e3nn-031
- e3nn fixes the sign of each spherical harmonic order by building it from the lower order and Y1 with Clebsch-Gordan coefficients. (Geiger & Smidt, 2022) `ev:reported` p. 8 ^geiger2022e3nn-032
- e3nn contains efficient functions to convert back and forth between truncated spherical harmonic coefficients and a function evaluated on a sphere grid. (Geiger & Smidt, 2022) `ev:reported` p. 10 ^geiger2022e3nn-033
- The sphere grid used in e3nn is made of necklaces around the y axis, chosen to improve the performance of the transformation. (Geiger & Smidt, 2022) `ev:reported` p. 10 ^geiger2022e3nn-034
- Via a change of basis, the tensor product of two vectors decomposes into a scalar, a pseudovector and 5 even l = 2 components. (Geiger & Smidt, 2022) `ev:computed` p. 11 ^geiger2022e3nn-035
- e3nn relaxes the definition of tensor product to any bilinear, equivariant operation that acts on irreps and outputs irreps. (Geiger & Smidt, 2022) `ev:reported` p. 11 ^geiger2022e3nn-036
- In e3nn the tensor product paths, constrained by the allowed output orders and parities, are the building blocks of tensor product operations. (Geiger & Smidt, 2022) `ev:reported` p. 11 ^geiger2022e3nn-037
- FullyConnectedTensorProduct is a simplified interface to the general TensorProduct, which is defined by input irreps, output irreps and a set of weighted paths. (Geiger & Smidt, 2022) `ev:reported` p. 12 ^geiger2022e3nn-038
- Weights are initialized as a normalization constant times a Gaussian parameter, chosen so every path contributes equally with output amplitude near one. (Geiger & Smidt, 2022) `ev:reported` p. 12 ^geiger2022e3nn-039
- e3nn gets the Clebsch-Gordan coefficients from QuTip and applies its change of basis to convert them into the real basis. (Geiger & Smidt, 2022) `ev:reported` p. 12 ^geiger2022e3nn-040
- Each output of an e3nn tensor product is a sum of paths scaled by a constant ensuring output components have variance 1. (Geiger & Smidt, 2022) `ev:reported` p. 13 ^geiger2022e3nn-041
- Besides the uvw weight connection mode, e3nn provides sparser connection modes such as uvu, with further modes uuu and uvuv described in the library. (Geiger & Smidt, 2022) `ev:reported` p. 13 ^geiger2022e3nn-042
- The authors prove that the TensorProduct class can represent any bi-linear equivariant operation combining two sets of irreps into irreps. (Geiger & Smidt, 2022) `ev:computed` p. 13 ^geiger2022e3nn-043
- The ReducedTensorProduct operation can deduce that a rank 4 symmetric Cartesian tensor has only 21 rather than 81 degrees of freedom. (Geiger & Smidt, 2022) `ev:computed` p. 14 ^geiger2022e3nn-044
- The ReducedTensorProduct class takes an index formula specifying permutation symmetries of the indices, plus the irrep decomposition of each index. (Geiger & Smidt, 2022) `ev:reported` p. 14 ^geiger2022e3nn-045
- The reduction algorithm solves the permutation and rotation symmetries independently, because the two symmetries commute, and merges the results at the end. (Geiger & Smidt, 2022) `ev:computed` p. 14 ^geiger2022e3nn-046
- The authors argue that solving the linear system for only one irrep component suffices, since the reduced tensor is a representation. (Geiger & Smidt, 2022) `ev:asserted` p. 15 ^geiger2022e3nn-047
- For tensors made from products of vectors, e3nn can apply the change of basis by performing tensor products instead of matrix multiplication. (Geiger & Smidt, 2022) `ev:reported` p. 15 ^geiger2022e3nn-048
- Using TensorProduct and spherical harmonics, the authors implemented a point convolution, a voxel convolution and an equivariant transformer from earlier work. (Geiger & Smidt, 2022) `ev:reported` p. 16 ^geiger2022e3nn-049
- The paper gives example code for a module computing a weight-parameterized polynomial of positions that is equivariant under all E(3) transformations. (Geiger & Smidt, 2022) `ev:reported` p. 16 ^geiger2022e3nn-050
- In all e3nn modules the weights are initialized with a normalized Gaussian of mean 0 and variance 1. (Geiger & Smidt, 2022) `ev:reported` p. 17 ^geiger2022e3nn-051
- e3nn favors component normalization, aiming for a vector x in Rd to have squared norm d so components have magnitude about 1. (Geiger & Smidt, 2022) `ev:reported` p. 17 ^geiger2022e3nn-052
- According to the authors, their initialization scheme gives all preactivations mean 0 and variance 1 at initialization. (Geiger & Smidt, 2022) `ev:asserted` p. 17 ^geiger2022e3nn-053
- The authors state that all layers learn as the width goes to infinity because their initialization satisfies the Maximal Update Parametrization. (Geiger & Smidt, 2022) `ev:asserted` p. 17 ^geiger2022e3nn-054
- e3nn uses µP shifted by θ = 1/2, with the learning rate set proportional to the number of features. (Geiger & Smidt, 2022) `ev:reported` p. 17 ^geiger2022e3nn-055
- It has been observed that the exponent of the learning curve is different for equivariant neural networks, not merely shifted by a constant. (Geiger & Smidt, 2022) `ev:cited` p. 18 ^geiger2022e3nn-056
- The authors state that they have no theoretical explanation for the change of learning curve exponent in equivariant networks. (Geiger & Smidt, 2022) `ev:asserted` p. 18 ^geiger2022e3nn-057
- [[Steerable CNN|3D Steerable CNNs]] articulate filters as a tensor product operation on the spherical harmonic expansion, whereas in [[Tensor Field Network|Tensor Field Networks]] the filter is that expansion. (Geiger & Smidt, 2022) `ev:asserted` p. 18 ^geiger2022e3nn-058
- To reduce computational overhead on point clouds, [[Tensor Field Network|Tensor Field Networks]] add no weights in the tensor product and apply a linear operation afterward. (Geiger & Smidt, 2022) `ev:asserted` p. 18 ^geiger2022e3nn-059
- In e3nn the difference between [[Tensor Field Network|Tensor Field Networks]] and 3D Steerable CNNs is implemented as the uvu versus uvw connection modes. (Geiger & Smidt, 2022) `ev:reported` p. 18 ^geiger2022e3nn-060
- In irrep space, the activation functions of spherical CNNs require a Fourier transform and a reverse transform, according to the authors. (Geiger & Smidt, 2022) `ev:asserted` p. 18 ^geiger2022e3nn-061
- Clebsch-Gordan Networks can be expressed with e3nn primitives as a TensorSquare nonlinearity followed by a Linear layer. (Geiger & Smidt, 2022) `ev:asserted` p. 19 ^geiger2022e3nn-062
- The authors conclude that e3nn is a general framework for composable E(3) equivariant operations for learning on 3D data and beyond. (Geiger & Smidt, 2022) `ev:asserted` p. 19 ^geiger2022e3nn-063
- Because all equivariant operations are distilled into a few core building blocks, the authors say optimization efforts can focus on these classes. (Geiger & Smidt, 2022) `ev:asserted` p. 19 ^geiger2022e3nn-064
- The framework does not impose specific training operations but gives users building blocks, much as PyTorch or TensorFlow provide autodifferentiation APIs. (Geiger & Smidt, 2022) `ev:asserted` p. 19 ^geiger2022e3nn-065
- Models built with e3nn using high order representations with l > 1 are more data-efficient than models limited to scalars and vectors. (Geiger & Smidt, 2022) `ev:cited` p. 19 ^geiger2022e3nn-066

## 🎯 Contributions

## 📖 Glossary

- **Irrep** — irreducible representation; smallest group representation containing no smaller representation.
- **Parity** — behavior under inversion x to -x; even (p = 1) or odd (p = -1).
- **Pseudovector** — vector-like quantity that is even under parity, e.g. a cross product.
- **Tensor product path** — one independent bilinear equivariant map from two input irreps to one output irrep.
- **Clebsch-Gordan coefficients** — change of basis decomposing a tensor product into irreps; also Wigner 3j symbols.
- **Spherical harmonics** — equivariant functions from the sphere to an irrep, forming a basis for spherical functions.
- **Connection mode** — weight sharing pattern (uvw, uvu, uuu, uvuv) between multiplicities in a tensor product.
- **Component normalization** — scaling so a d-dimensional vector has squared norm d.
- **Maximal Update Parametrization** — initialization and scaling rule ensuring all layers learn as width grows to infinity.

## ❓ Open questions

- Why do equivariant networks change the exponent of the learning curve rather than only shifting it? The authors give no theoretical explanation.
- How does the computational cost of the general TensorProduct compare with specialized implementations of the same architectures? The paper reports no benchmarks.
- When are restricted scalar and vector operations sufficient, and when do higher-l internal representations become necessary?

## 📝 Notes on reading

- The document states it is a draft and is dated January 2021 on page 2, while the arXiv version (2207.09453v1) is from July 2022.
- The paper is a software and mathematics description; it reports no experiments of its own. Data-efficiency statements rest on cited work (Batzner et al.).
- Section 3 calls the class ReduceTensorProduct, while Section 7.4 and the code use ReducedTensorProduct(s).
- Equations for the real change of basis (Eq. 5), path formulas (Eqs. 16, 19-21) and the reduction pseudo code were garbled in extraction; their structure is summarized in prose only.
- Figure 1 shows the polynomials from successive tensor products of x with itself, with spherical harmonics as the highest irrep of each polynomial order. Figure 2 shows the necklace sphere grid and a random signal cut at L = 5. Figure 3 diagrams the four paths of the example tensor product. Figure 4 sketches a learning curve with a slope change for equivariant models.
- References [24] and [25] are duplicates (both SchNet).

## Suggested new concepts

- E(3)-equivariant neural networks — the architecture family e3nn unifies; central to 3D learning notes.
- Tensor product of irreps — the core bilinear operation reused by NequIP, MACE and similar models.
- Spherical harmonics as equivariant features — recurring embedding of relative geometry in equivariant networks.
- Learning curve exponent under equivariance — an empirical claim spanning several papers that lacks theory.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Biblioteca general $E(3)$-equivariante (irreps)

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
