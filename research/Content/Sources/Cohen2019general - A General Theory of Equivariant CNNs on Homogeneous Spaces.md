---
aliases: []
type: "source"
title: "A General Theory of Equivariant CNNs on Homogeneous Spaces"
citekey: "Cohen2019general"
doi: "10.48550/arXiv.1811.02017"
arxiv: "1811.02017"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1811.02017"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Taco Cohen", "Mario Geiger", "Maurice Weiler"]
sha256: ["ae26fab38f6621030b3eb00454ccd1bffdccf7d75b704f7a5a758f4bf91f2b29"]
pdf: "Content/Papers/Cohen2019general.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Cohen2019general.pdf]]

> [!abstract] One-sentence summary
> The paper models G-CNN feature maps as fields over homogeneous spaces and proves that every equivariant linear layer between them is a convolution with an equivariant kernel, giving a unified taxonomy of existing equivariant CNNs.

## Abstract

We present a general theory of Group equivariant Convolutional Neural Networks (G-CNNs) on homogeneous spaces such as Euclidean space and the sphere. Feature maps in these networks represent fields on a homogeneous base space, and layers are equivariant maps between spaces of fields. The theory enables a systematic classification of all existing G-CNNs in terms of their symmetry group, base space, and field type. We also consider a fundamental question: what is the most general kind of equivariant linear map between feature spaces (fields) of given types? Following Mackey, we show that such maps correspond one-to-one with convolutions using equivariant kernels, and characterize the space of such kernels. (arXiv)

## 🧠 Key ideas (atomic)

- The paper presents a general theory of group equivariant CNNs on homogeneous spaces such as Euclidean space or the sphere. (Cohen et al., 2019) `ev:asserted` p. 1 ^cohen2019general-001
- The authors note that, with the proliferation of equivariant layers, it has become difficult to see the relations between the various approaches. (Cohen et al., 2019) `ev:asserted` p. 1 ^cohen2019general-002
- Feature spaces are modelled as fields on a homogeneous space, characterized by a symmetry group G, a subgroup H, plus a representation ρ. (Cohen et al., 2019) `ev:asserted` p. 1 ^cohen2019general-003
- The authors state that the paper contains no truly new mathematics but provides a new formalism for studying equivariant convolutional networks. (Cohen et al., 2019) `ev:asserted` p. 1 ^cohen2019general-004
- The authors argue that describing G-CNNs with fields and fiber bundles makes it possible to apply decades of physics knowledge to machine learning. (Cohen et al., 2019) `ev:asserted` p. 1 ^cohen2019general-005
- The main theorems show that linear equivariant maps between feature spaces are in one-to-one correspondence with equivariant convolution kernels. (Cohen et al., 2019) `ev:computed` p. 2 ^cohen2019general-006
- The space of equivariant kernels can be realized as matrix-valued functions on a group, coset space, or double coset space under linear constraints. (Cohen et al., 2019) `ev:computed` p. 2 ^cohen2019general-007
- A homogeneous space for a group G is a space where any two points are related by some transformation in G. (Cohen et al., 2019) `ev:asserted` p. 2 ^cohen2019general-008
- The sphere is a homogeneous space for SO(3) because any point on the sphere can be mapped to any other via a rotation. (Cohen et al., 2019) `ev:asserted` p. 2 ^cohen2019general-009
- Fixing an origin, its stabilizer subgroup H lets the group G be viewed as a principal bundle over base space G/H with fiber H. (Cohen et al., 2019) `ev:asserted` p. 2 ^cohen2019general-010
- The natural way to transform a ρ-field is the induced representation, combining the action of G on the base space with ρ on the fiber. (Cohen et al., 2019) `ev:asserted` p. 2 ^cohen2019general-011
- A feature space in a classical CNN can be seen as a trivial bundle, with one vector space of channels per position in the plane. (Cohen et al., 2019) `ev:asserted` p. 3 ^cohen2019general-012
- The tangent bundle of the sphere has fibers that look like R2 but is topologically distinct from the product S2 × R2 as a bundle. (Cohen et al., 2019) `ev:asserted` p. 3 ^cohen2019general-013
- For a non-trivial bundle the fibers cannot be continuously aligned simultaneously, so each section value must be kept in its own fiber. (Cohen et al., 2019) `ev:asserted` p. 3 ^cohen2019general-014
- The authors interpret a principal bundle as a bundle of generalized frames, where the action of the subgroup H is a change of frame. (Cohen et al., 2019) `ev:asserted` p. 4 ^cohen2019general-015
- The group H may also include internal symmetries, such as color space rotations, that do not relate to the spatial dimensions of the base space. (Cohen et al., 2019) `ev:asserted` p. 4 ^cohen2019general-016
- Non-trivial principal bundles lack continuous global sections, so fields are represented with local sections on overlapping patches covering G/H. (Cohen et al., 2019) `ev:asserted` p. 4 ^cohen2019general-017
- Feature spaces are defined as spaces of sections of the associated vector bundle, and in physics such a section is simply called a field. (Cohen et al., 2019) `ev:asserted` p. 4 ^cohen2019general-018
- The associated bundle construction works for any principal H-bundle, which the authors say suggests a direction for further generalization. (Cohen et al., 2019) `ev:cited` p. 4 ^cohen2019general-019
- Mackey functions give a concrete global description of a field, but their redundancy makes them unsuitable for computer implementation. (Cohen et al., 2019) `ev:asserted` p. 5 ^cohen2019general-020
- Local sections are unconstrained functions on a trivializing neighbourhood of G/H, mapped to Mackey functions by a lifting isomorphism. (Cohen et al., 2019) `ev:computed` p. 5 ^cohen2019general-021
- The lifting map is analogous to a lifting previously defined in other work for scalar fields, where the representation is the identity. (Cohen et al., 2019) `ev:cited` p. 5 ^cohen2019general-022
- Examples of fields include an RGB image, a field of wind directions on earth, or a diffusion tensor MRI image, each with its own ρ. (Cohen et al., 2019) `ev:asserted` p. 5 ^cohen2019general-023
- In deriving equivariant maps between feature spaces, the authors assume that the group G is locally compact and unimodular. (Cohen et al., 2019) `ev:asserted` p. 5 ^cohen2019general-024
- Theorem 3.1 states that an equivariant map between the considered feature spaces can always be written as a convolution-like integral. (Cohen et al., 2019) `ev:computed` p. 6 ^cohen2019general-025
- The equivariance constraint reduces the two-argument kernel to a one-argument kernel, turning the linear map into a cross-correlation on G. (Cohen et al., 2019) `ev:computed` p. 6 ^cohen2019general-026
- Theorem 3.2 shows that the space of equivariant maps is isomorphic to the space of bi-equivariant kernels on the group G. (Cohen et al., 2019) `ev:computed` p. 6 ^cohen2019general-027
- The constraint on the two-argument kernel can be interpreted as the kernel being a section of a certain associated bundle over G × G. (Cohen et al., 2019) `ev:computed` p. 6 ^cohen2019general-028
- Theorem 3.3 shows that the space of equivariant maps is isomorphic to a space of left-equivariant kernels on the coset space G/H1. (Cohen et al., 2019) `ev:computed` p. 6 ^cohen2019general-029
- Theorem 3.4 characterizes equivariant maps as kernels on the double coset space H2\G/H1 that are equivariant under a stabilizer subgroup. (Cohen et al., 2019) `ev:computed` p. 7 ^cohen2019general-030
- For fields realized as local functions, the equivariant map becomes a ρ1-twisted cross-correlation on G/H1 with an equivariant kernel. (Cohen et al., 2019) `ev:computed` p. 7 ^cohen2019general-031
- For semidirect product groups the ρ1 factor disappears, leaving a standard cross-correlation on G/H1 with an equivariant kernel. (Cohen et al., 2019) `ev:computed` p. 7 ^cohen2019general-032
- In a regular G-CNN, ρ can be realized by permutation matrices, so any pointwise nonlinearity can be used. (Cohen et al., 2019) `ev:asserted` p. 7 ^cohen2019general-033
- For other kinds of representations, special equivariant nonlinearities such as norm, tensor product, or gated nonlinearities must be used. (Cohen et al., 2019) `ev:cited` p. 7 ^cohen2019general-034
- Since the equivariance constraints on kernels are linear, it is sufficient to solve for a basis of H-equivariant kernels combined with learned weights. (Cohen et al., 2019) `ev:asserted` p. 8 ^cohen2019general-035
- On Euclidean pixel grids, the steerable kernel basis is typically pre-sampled on a small grid, then used in a standard convolution routine. (Cohen et al., 2019) `ev:cited` p. 8 ^cohen2019general-036
- On pixel grids, the sampling of the steerable kernel basis requires particular attention since it might introduce aliasing artifacts. (Cohen et al., 2019) `ev:cited` p. 8 ^cohen2019general-037
- For signals sampled on irregular point clouds, the steerable kernel space is typically implemented as an analytical function sampled on the cloud. (Cohen et al., 2019) `ev:cited` p. 8 ^cohen2019general-038
- One spherical CNN approach represents signals and kernels in Fourier space, performing the equivariant convolution by exploiting the Fourier theorem. (Cohen et al., 2019) `ev:cited` p. 8 ^cohen2019general-039
- The most closely related prior theory is analogous to this one but only covers scalar fields, corresponding to a trivial representation. (Cohen et al., 2019) `ev:cited` p. 8 ^cohen2019general-040
- The authors state that a proper treatment of general fields is more difficult, as it requires fiber bundles plus induced representations. (Cohen et al., 2019) `ev:asserted` p. 8 ^cohen2019general-041
- The authors state that their use of fields with block-diagonal ρ can be viewed as a formalization of convolutional capsules. (Cohen et al., 2019) `ev:asserted` p. 8 ^cohen2019general-042
- Mackey rigorously proved results essentially similar to those of the paper, in an abstract form not easily recognized as relevant to equivariant CNNs. (Cohen et al., 2019) `ev:cited` p. 8 ^cohen2019general-043
- For SO(3) with the stabilizer SO(2) of the north pole, the coset space G/H is the sphere S2. (Cohen et al., 2019) `ev:computed` p. 8 ^cohen2019general-044
- For the spherical case, the double coset space H\G/H is the segment [0, π), indexing latitudinal circles around the Z axis. (Cohen et al., 2019) `ev:computed` p. 9 ^cohen2019general-045
- By Theorem 3.4, spherical equivariant kernels are matrix-valued functions on the segment [0, π) that are mostly unconstrained except at the poles. (Cohen et al., 2019) `ev:computed` p. 9 ^cohen2019general-046
- With a trivial representation the spherical kernel is constant on latitudinal orbits, in agreement with prior work that uses isotropic filters. (Cohen et al., 2019) `ev:computed` p. 9 ^cohen2019general-047
- Choosing ρ2 as a regular representation of SO(2) recovers the non-isotropic method of an earlier spherical CNN paper. (Cohen et al., 2019) `ev:computed` p. 9 ^cohen2019general-048
- Spherical CNNs that process vector fields would be possible with the standard 2D representation of SO(2), but this has not been done yet. (Cohen et al., 2019) `ev:asserted` p. 9 ^cohen2019general-049
- For the rigid body motion group SE(3) with stabilizer SO(3), the coset space G/H is the Euclidean space R3. (Cohen et al., 2019) `ev:computed` p. 9 ^cohen2019general-050
- For the SE(3) example, the double coset space indexing spherical shell orbits is the set of radii [0, ∞). (Cohen et al., 2019) `ev:computed` p. 9 ^cohen2019general-051
- For SE(3), equivariant maps are convolutions with matrix-valued kernels on R3 satisfying a rotation constraint, in agreement with [[Steerable CNN|3D Steerable CNNs]]. (Cohen et al., 2019) `ev:computed` p. 9 ^cohen2019general-052
- The authors conclude that the field formalism of modern physics can elegantly describe convolutional networks together with their generalizations. (Cohen et al., 2019) `ev:asserted` p. 9 ^cohen2019general-053
- The authors expect the theory to provide many opportunities for new theoretical insights about deep learning and new equivariant architectures. (Cohen et al., 2019) `ev:asserted` p. 9 ^cohen2019general-054
- The theory only covers fields over homogeneous spaces, which come naturally equipped with a group action to which the network can be equivariant. (Cohen et al., 2019) `ev:asserted` p. 17 ^cohen2019general-055
- The theory idealizes feature maps as fields over a possibly continuous base space, whereas a computer implementation usually discretizes this space. (Cohen et al., 2019) `ev:asserted` p. 17 ^cohen2019general-056
- The authors consider it likely that a sampling theory for discretized deep networks can be developed, though this has not been done yet. (Cohen et al., 2019) `ev:asserted` p. 17 ^cohen2019general-057
- Table 1 classifies existing G-CNNs by symmetry group G, subgroup H, base space G/H, plus the type of field ρ. (Cohen et al., 2019) `ev:asserted` p. 18 ^cohen2019general-058
- In the taxonomy, the classical CNN of LeCun 1990 corresponds to the translation group Z2 with trivial subgroup and a regular field type. (Cohen et al., 2019) `ev:asserted` p. 18 ^cohen2019general-059
- The taxonomy lists spherical CNNs with group SO(3) and subgroup SO(2) on S2, using regular, trivial, or irreducible field types. (Cohen et al., 2019) `ev:asserted` p. 18 ^cohen2019general-060

## 🎯 Contributions


## 📖 Glossary

- **Homogeneous space** — A space on which a group acts transitively; isomorphic to a coset space G/H.
- **Stabilizer subgroup** — The subgroup H of transformations that leave a chosen origin fixed.
- **Fiber bundle** — A space locally looking like a product of a base space with a fiber.
- **Principal bundle** — A fiber bundle whose fibers are copies of a group acting freely and transitively.
- **Associated vector bundle** — Bundle obtained by replacing principal-bundle fibers with a vector space carrying representation ρ.
- **Field** — A section of an associated vector bundle; a stack of feature maps.
- **Mackey function** — A function on G satisfying f(gh) = ρ(h⁻¹)f(g), encoding a section redundantly.
- **Induced representation** — The action of G on fields, combining base-space motion with fiber transformation by ρ.
- **Double coset space** — The space H2\G/H1 of H2-orbits in the coset space G/H1.
- **Semidirect product** — A group G = N ⋊ H with normal subgroup N, simplifying the twist function.
- **Steerable kernel basis** — A precomputed basis of equivariant kernels combined with learned weights.

## ❓ Open questions

- How can the theory be extended from homogeneous spaces to general manifolds or arbitrary principal bundles?
- Can a sampling theory, analogous to signal processing sampling theorems, justify discretizing the continuous fields used in G-CNNs?
- How well do spherical CNNs with vector-field features (standard SO(2) representation) perform in practice?
- Which choice of field type ρ is best for a given task and symmetry group?

## 📝 Notes on reading

The cached text is arXiv 1811.02017v2 (9 Jan 2020), the NeurIPS 2019 camera-ready version, while the packet venue says arXiv preprint. The paper is purely theoretical: it contains no experiments or numerical results, so all claims are derivations, definitions, or citations. Many equations (Eqs. 5-14, 29-46) are garbled by extraction (fractured sub/superscripts, integral signs split across lines); claims describe theorem statements in words rather than transcribing formulas. Proofs of Theorems 3.2-3.3 are partly deferred to supplementary material; Appendix B gives the bi-equivariance proofs and the KC-KD isomorphism. Figures 1-7 (SO(3) as an SO(2) bundle, tangent bundle of S2, scalar-to-vector field map, cylinder vs Möbius strip, planar vector field rotation, quotients of SO(3) and SE(3), Cayley diagram of D3) are illustrations only. Table 1 (p. 18) uses ditto marks that extraction flattened; only its headline rows were claimed. Minor typos in the paper: 'nog just' (p. 4), 'lattitude' (p. 9), 'ismorphism' (p. 16).

## Suggested new concepts

- Group equivariant CNN (G-CNN) — central architecture class unified by this theory and many related papers.
- Induced representation — the transformation law of feature fields, reused across equivariant network theory.
- Steerable CNN — the practical implementation family (steerable kernel bases) described and classified here.
- Homogeneous space — the base-space notion that defines the scope of the theory.
- Equivariant kernel constraint — the linear constraint characterizing all equivariant linear layers.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Teoría de campos y núcleos steerable sobre $G/H$.
