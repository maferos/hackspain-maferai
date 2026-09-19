---
aliases: []
type: "source"
title: "On the Generalization of Equivariance and Convolution in Neural Networks to the Action of Compact Groups"
citekey: "Kondor2018generalization"
doi: "10.48550/arXiv.1802.03690"
arxiv: "1802.03690"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1802.03690"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Risi Kondor", "Shubhendu Trivedi"]
sha256: ["ce6bf070b3683a705a6229e9e505a7b523d495f279e72a26b551833a0d1ecf42"]
pdf: "Content/Papers/Kondor2018generalization.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 56
---

📄 PDF: [[Kondor2018generalization.pdf]]

> [!abstract] One-sentence summary
> The paper proves that, for networks whose layers live on quotient spaces of a compact group, equivariance to the group holds exactly when every layer is a generalized group convolution, giving a theoretical basis for G-CNNs, spherical CNNs and message passing networks.

## Abstract

Convolutional neural networks have been extremely successful in the image recognition domain because they ensure equivariance to translations. There have been many recent attempts to generalize this framework to other domains, including graphs and data lying on manifolds. In this paper we give a rigorous, theoretical treatment of convolution and equivariance in neural networks with respect to not just translations, but the action of any compact group. Our main result is to prove that (given some natural constraints) convolutional structure is not just a sufficient, but also a necessary condition for equivariance to the action of a compact group. Our exposition makes use of concepts from representation theory and noncommutative harmonic analysis and derives new generalized convolution formulae. (arXiv)

## 🧠 Key ideas (atomic)

- The paper aims to relate group convolution over a compact group to the looser notions of convolution used in the neural network literature. (Kondor & Trivedi, 2018) `ev:asserted` p. 1 ^kondor2018generalization-001
- The authors state that several practical neural networks implicitly already take advantage of the group theoretic concept of convolution. (Kondor & Trivedi, 2018) `ev:asserted` p. 1 ^kondor2018generalization-002
- To the best of the authors' knowledge, this is the first statement of the connection between equivariance and convolution in neural networks at this generality. (Kondor & Trivedi, 2018) `ev:asserted` p. 1 ^kondor2018generalization-003
- A technical challenge is that layer activations are functions on homogeneous spaces acted on by the group, rather than on the group itself. (Kondor & Trivedi, 2018) `ev:asserted` p. 1 ^kondor2018generalization-004
- The paper does not present new algorithms or neural network architectures, aiming instead to provide language for thinking about generalized equivariance. (Kondor & Trivedi, 2018) `ev:asserted` p. 2 ^kondor2018generalization-005
- The stated goal includes facilitating the development of future neural network architectures for data with non-trivial symmetries. (Kondor & Trivedi, 2018) `ev:asserted` p. 2 ^kondor2018generalization-006
- The work of Ravanbakhsh et al. on parameter sharing is described as close in spirit but only considering discrete groups. (Kondor & Trivedi, 2018) `ev:cited` p. 2 ^kondor2018generalization-007
- Each network layer is modelled as a linear map between function spaces on index sets, followed by a pointwise nonlinearity. (Kondor & Trivedi, 2018) `ev:asserted` p. 2 ^kondor2018generalization-008
- The authors note that in most CNNs the filter width w is quite small, on the order of 3 ∼10. (Kondor & Trivedi, 2018) `ev:asserted` p. 2 ^kondor2018generalization-009
- The number of parameters in CNNs is much smaller than in fully connected feed-forward networks, since only filter values are learned. (Kondor & Trivedi, 2018) `ev:asserted` p. 2 ^kondor2018generalization-010
- Translating the input image of a CNN by any vector translates all higher layers in exactly the same way, called translation equivariance. (Kondor & Trivedi, 2018) `ev:asserted` p. 2 ^kondor2018generalization-011
- Invariance is treated as a special case of equivariance in which the output group action is the identity for all group elements. (Kondor & Trivedi, 2018) `ev:asserted` p. 3 ^kondor2018generalization-012
- Any equivariant network can be made group invariant by adding a final layer, often averaging or histogramming last-layer activations. (Kondor & Trivedi, 2018) `ev:asserted` p. 3 ^kondor2018generalization-013
- The authors describe invariance to reordering the vertices as a hard constraint on any representation a neural network learns in graph learning. (Kondor & Trivedi, 2018) `ev:asserted` p. 3 ^kondor2018generalization-014
- Message passing networks from Gilmer et al. are described as today's state of the art solution for invariance to vertex reordering. (Kondor & Trivedi, 2018) `ev:cited` p. 3 ^kondor2018generalization-015
- Prior work observed that in certain cases, such as the sphere, abstract continuous neural networks are easier to describe than discrete ones. (Kondor & Trivedi, 2018) `ev:cited` p. 3 ^kondor2018generalization-016
- The authors restrict attention to compact groups mainly because compactness guarantees that the Haar measure is essentially unique. (Kondor & Trivedi, 2018) `ev:asserted` p. 4 ^kondor2018generalization-017
- According to the authors, non-compact groups would also cause trouble because their representation theory is much more involved. (Kondor & Trivedi, 2018) `ev:asserted` p. 4 ^kondor2018generalization-018
- The translation group behind traditional CNNs is not compact but remains amenable to the analysis with small modifications, as an exceptional family. (Kondor & Trivedi, 2018) `ev:asserted` p. 4 ^kondor2018generalization-019
- For simplicity of exposition, the results are presented assuming that the group G is countable or finite. (Kondor & Trivedi, 2018) `ev:asserted` p. 4 ^kondor2018generalization-020
- Definition 4 defines convolution of functions on left or right quotient spaces by summing over the group after lifting both functions to it. (Kondor & Trivedi, 2018) `ev:asserted` p. 4 ^kondor2018generalization-021
- When f lives on the group and g on G/H, their convolution is constant on left H-cosets, making it a function on G/H. (Kondor & Trivedi, 2018) `ev:computed` p. 5 ^kondor2018generalization-022
- When f is defined on G/H, the filter g can without loss of generality be taken as a function on H\G. (Kondor & Trivedi, 2018) `ev:computed` p. 5 ^kondor2018generalization-023
- With f on G/H and a filter on H\G/K, the generalized convolution maps functions on G/H to functions on G/K. (Kondor & Trivedi, 2018) `ev:computed` p. 5 ^kondor2018generalization-024
- The authors identify this double-coset case as the definition most relevant to constructing neural networks, since it maps between homogeneous spaces. (Kondor & Trivedi, 2018) `ev:asserted` p. 5 ^kondor2018generalization-025
- Proposition 1 shows that Fourier matrices of functions on quotient spaces are sparse, with columns zero unless the restricted block is trivial. (Kondor & Trivedi, 2018) `ev:computed` p. 6 ^kondor2018generalization-026
- This sparsity resolves why a quotient-space function has as many Fourier matrices of the same sizes as a function on the group. (Kondor & Trivedi, 2018) `ev:computed` p. 6 ^kondor2018generalization-027
- Proposition 2 states that the Fourier transform of a group convolution equals the product of the two Fourier matrices at each irrep. (Kondor & Trivedi, 2018) `ev:computed` p. 6 ^kondor2018generalization-028
- A G-CNN is defined as a network whose linear maps are generalized convolutions with filters defined on double coset spaces of subgroups. (Kondor & Trivedi, 2018) `ev:asserted` p. 6 ^kondor2018generalization-029
- In Theorem 1, a network whose index sets are quotient spaces of a compact group is equivariant exactly when it is a G-CNN. (Kondor & Trivedi, 2018) `ev:computed` p. 6 ^kondor2018generalization-030
- The forward direction of Theorem 1 follows from elementary coset facts, with induction over layers using the transitivity of equivariance. (Kondor & Trivedi, 2018) `ev:computed` p. 7 ^kondor2018generalization-031
- The authors note that the forward-direction proof also holds for vector-valued activations with correspondingly vector-valued filters. (Kondor & Trivedi, 2018) `ev:computed` p. 7 ^kondor2018generalization-032
- Lemma 7 shows that an equivariant linear map between function spaces on homogeneous spaces acts linearly on each corresponding Fourier component. (Kondor & Trivedi, 2018) `ev:computed` p. 13 ^kondor2018generalization-033
- Lemma 10 shows a Fourier-space map on one irrep component is allowable only if it right-multiplies by a fixed matrix. (Kondor & Trivedi, 2018) `ev:computed` p. 14 ^kondor2018generalization-034
- Defining the filter as the inverse Fourier transform of these matrices, the convolution theorem confirms that the equivariant network is a G-CNN. (Kondor & Trivedi, 2018) `ev:computed` p. 14 ^kondor2018generalization-035
- The reverse-direction proof is first given for scalar activations, with the extension to vector-valued activations described as straightforward. (Kondor & Trivedi, 2018) `ev:asserted` p. 14 ^kondor2018generalization-036
- The most common rotation-equivariant approach is described as CNNs with filters replicated at rotational angles, typically multiples of 90 degrees. (Kondor & Trivedi, 2018) `ev:cited` p. 7 ^kondor2018generalization-037
- The authors interpret harmonic networks, which expand local activations in the SO(2) irrep basis with weights, as convolution on the group. (Kondor & Trivedi, 2018) `ev:asserted` p. 7 ^kondor2018generalization-038
- Group theoretic analysis of the equivariance condition used in harmonic networks is stated to be beyond the scope of the paper. (Kondor & Trivedi, 2018) `ev:asserted` p. 7 ^kondor2018generalization-039
- For spherical CNNs, the sphere is identified with the quotient space SO(3)/SO(2), taking the North pole as the origin. (Kondor & Trivedi, 2018) `ev:computed` p. 7 ^kondor2018generalization-040
- By Proposition 1, only the middle column of each Fourier matrix is nonzero for functions on SO(3)/SO(2). (Kondor & Trivedi, 2018) `ev:computed` p. 7 ^kondor2018generalization-041
- Up to constant scaling factors, the entries of that middle column are the customary spherical harmonic expansion coefficients. (Kondor & Trivedi, 2018) `ev:computed` p. 7 ^kondor2018generalization-042
- Spherical CNNs of Cohen et al. are proven SO(3)-equivariant, but that work does not prove the converse that equivariance implies convolution. (Kondor & Trivedi, 2018) `ev:cited` p. 8 ^kondor2018generalization-043
- The spherical CNN algorithm of Cohen et al. requires repeated forward and backward SO(3) fast Fourier transforms to apply the nonlinearity. (Kondor & Trivedi, 2018) `ev:cited` p. 8 ^kondor2018generalization-044
- The authors state that message passing neural networks can also be viewed as group convolutional networks over receptive-field subsets. (Kondor & Trivedi, 2018) `ev:asserted` p. 8 ^kondor2018generalization-045
- The set of all k-subsets of graph vertices is identified with a quotient space of the symmetric group Sn. (Kondor & Trivedi, 2018) `ev:computed` p. 8 ^kondor2018generalization-046
- This k-subset labeling is redundant because it includes non-contiguous subsets, whose labels are simply set to zero. (Kondor & Trivedi, 2018) `ev:asserted` p. 8 ^kondor2018generalization-047
- In the k-subset network, each layer's convolution amounts to multiplying each of the ℓ+1 Fourier matrices by a learnable scalar. (Kondor & Trivedi, 2018) `ev:computed` p. 8 ^kondor2018generalization-048
- The authors conclude that permutation equivariance is a severe constraint that significantly limits the form of the convolutional filters. (Kondor & Trivedi, 2018) `ev:asserted` p. 8 ^kondor2018generalization-049
- The authors argue the framework is still richer than traditional MPNNs, where the labels of the neighbors are simply summed. (Kondor & Trivedi, 2018) `ev:asserted` p. 8 ^kondor2018generalization-050
- The representation theory of symmetric groups is stated to be beyond the scope of the present paper. (Kondor & Trivedi, 2018) `ev:asserted` p. 8 ^kondor2018generalization-051
- The authors argue that their theory gives practitioners a clear prescription for designing neural networks for data with non-trivial symmetries. (Kondor & Trivedi, 2018) `ev:asserted` p. 8 ^kondor2018generalization-052
- The authors argue for Fourier space representations, similar to those in recent harmonic, spherical and Clebsch–Gordan network papers. (Kondor & Trivedi, 2018) `ev:asserted` p. 8 ^kondor2018generalization-053
- The entries of an adjacency matrix are not a homogeneous space of Sn under simultaneous permutation of row and column indices. (Kondor & Trivedi, 2018) `ev:computed` p. 10 ^kondor2018generalization-054
- Split into diagonal and off-diagonal parts, the adjacency matrix entries individually form homogeneous spaces of the symmetric group. (Kondor & Trivedi, 2018) `ev:computed` p. 10 ^kondor2018generalization-055
- The convolution definitions are extended to vector and matrix valued functions to accommodate neural networks with multiple channels. (Kondor & Trivedi, 2018) `ev:asserted` p. 11 ^kondor2018generalization-056

## 🎯 Contributions


## 📖 Glossary

- **Equivariance** — a map commutes with group actions: transforming the input transforms the output correspondingly.
- **Compact group** — a topological group whose Haar measure is essentially unique and normalizable.
- **Homogeneous space** — a set on which a group acts transitively, identifiable with a quotient G/H.
- **Quotient space G/H** — the set of left cosets of a subgroup H in group G.
- **Double coset space** — the set of double cosets HgK for subgroups H and K of G.
- **Irreducible representation (irrep)** — a matrix-valued group homomorphism that cannot be split into smaller representations.
- **G-CNN** — a network whose every linear layer is a generalized convolution over group G.
- **Haar measure** — the invariant integration measure on a group used to define group convolution.
- **Schur's lemma** — maps commuting with an irreducible representation are multiples of the identity.

## ❓ Open questions

- How does a group theoretic analysis of the harmonic-network equivariance condition, with its non-pointwise nonlinearity, fit the theorem?
- How do the results extend to non-compact groups beyond the few exceptional families such as the translation group?
- What do the Fourier-space convolutions of symmetric-group networks look like in full, given that their representation theory was left out of scope?
- Can a k-subset network with per-component learnable scalars outperform traditional MPNNs in practice?
- Does the theorem hold for architectures whose nonlinearities are not pointwise, as in Fourier-space networks?

## 📝 Notes on reading

- Version read: arXiv 1802.03690v3 (10 Nov 2018), which carries the ICML 2018 (PMLR 80) proceedings footer; the packet identifier is the arXiv record.
- Purely theoretical paper: no experiments or datasets; claims rest on derivations (`computed`) or on the authors' framing (`asserted`).
- Equations, commutative diagrams and the schematic sparsity figures on p. 3 and p. 6 are garbled in the extraction; the sparsity schematics were only described.
- Inconsistencies inside the paper: p. 5 says the double-coset convolution maps to Y = H/K while the preceding text gives G/K; p. 6 refers to equation (19) (the Euclidean convolution theorem in the Appendix) where (14) seems meant; p. 13 cites a broken 'Section ??'; the reverse-direction proof on p. 14 begins 'Since N is a G-CNN' and cites Lemma 8 where the equivariance assumption and Lemma 7 appear intended.
- Theorem 1 as paraphrased on p. 1 says 'if and only if'; the formal statement on p. 6 adds the constraint that each index set is a quotient space G/Hℓ.
- Proposition 1 is proved assuming irreps adapted to the subgroup (p. 12).
- The MPNN example on p. 8 names the stabilizer both Sn−k × Sk and Sk × Sn−k and uses Sn/(Sn−ℓ × Sℓ) for layer index sets; the notation was not claimed verbatim.

## Suggested new concepts

- Group equivariant convolutional network (G-CNN) — central architecture class that this theorem characterizes, linking several vault papers.
- Equivariance — the core symmetry property that recurs across geometric deep learning sources.
- Noncommutative Fourier transform on groups — the tool that turns group convolutions into matrix products across irreps.
- Homogeneous space / quotient space — the domain on which equivariant layer activations live.
- Spherical CNN — concrete SO(3) instance discussed here and in related work.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Convolución ⇔ equivariancia para grupos compactos.
