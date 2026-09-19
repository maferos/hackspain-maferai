---
aliases: []
type: "source"
title: "Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges"
citekey: "Bronstein2021geometric"
doi: "10.48550/arXiv.2104.13478"
arxiv: "2104.13478"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2104.13478"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Michael M. Bronstein", "Joan Bruna", "Taco Cohen", "Petar Veličković"]
sha256: ["dcf8212ed37db9ac154ac975b8f9c7d36831cf56b75261679b04ab9814985fc2"]
pdf: "Content/Papers/Bronstein2021geometric.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Bronstein2021geometric.pdf]]

> [!abstract] One-sentence summary
> This monograph derives CNNs, GNNs, Transformers, equivariant networks, mesh CNNs and gated RNNs from one blueprint of symmetry, deformation stability and scale separation, giving a shared language for designing architectures with geometric priors.

## Abstract

The last decade has witnessed an experimental revolution in data science and machine learning, epitomised by deep learning methods. Indeed, many high-dimensional learning tasks previously thought to be beyond reach -- such as computer vision, playing Go, or protein folding -- are in fact feasible with appropriate computational scale. Remarkably, the essence of deep learning is built from two simple algorithmic principles: first, the notion of representation or feature learning, whereby adapted, often hierarchical, features capture the appropriate notion of regularity for each task, and second, learning by local gradient-descent type methods, typically implemented as backpropagation. While learning generic functions in high dimensions is a cursed estimation problem, most tasks of interest are not generic, and come with essential pre-defined regularities arising from the underlying low-dimensionality and structure of the physical world. This text is concerned with exposing these regularities through unified geometric principles that can be applied throughout a wide spectrum of applications. Such a 'geometric unification' endeavour, in the spirit of Felix Klein's Erlangen Program, serves a dual purpose: on one hand, it provides a common mathematical framework to study the most successful neural network architectures, such as CNNs, RNNs, GNNs, and Transformers. On the other hand, it gives a constructive procedure to incorporate prior physical knowledge into neural architectures and provide principled way to build future architectures yet to be invented. (arXiv)

## 🧠 Key ideas (atomic)

- The authors apply the Erlangen Programme mindset to deep learning, with the ultimate goal of obtaining a systematisation of the field. (Bronstein et al., 2021) `ev:asserted` p. 6 ^bronstein2021geometric-001
- The authors describe deep learning as having a veritable zoo of neural network architectures for various kinds of data, but few unifying principles. (Bronstein et al., 2021) `ev:asserted` p. 6 ^bronstein2021geometric-002
- Exploiting the known symmetries of a large system is described as a powerful and classical remedy against the curse of dimensionality. (Bronstein et al., 2021) `ev:asserted` p. 8 ^bronstein2021geometric-003
- The authors state that their work does not attempt to accurately summarise the entire existing wealth of research on Geometric Deep Learning. (Bronstein et al., 2021) `ev:asserted` p. 9 ^bronstein2021geometric-004
- If the target function is only known to be 1-Lipschitz, the number of observations required is necessarily exponential in the dimension. (Bronstein et al., 2021) `ev:computed` p. 12 ^bronstein2021geometric-005
- Citing Tsybakov, the authors state Sobolev smoothness assumptions only improve the statistical picture when smoothness scales with dimension, an unrealistic assumption. (Bronstein et al., 2021) `ev:cited` p. 12 ^bronstein2021geometric-006
- Sparsity-promoting regularisation lets fully-connected networks break the curse of dimensionality, at the expense of strong assumptions on the target function. (Bronstein et al., 2021) `ev:cited` p. 12 ^bronstein2021geometric-007
- The authors argue real-world functions of interest tend to exhibit complex long-range correlations that low-dimensional projections cannot express. (Bronstein et al., 2021) `ev:asserted` p. 12 ^bronstein2021geometric-008
- The authors name symmetry and scale separation as the two fundamental principles that give hope for learning from physically-structured data. (Bronstein et al., 2021) `ev:asserted` p. 13 ^bronstein2021geometric-009
- In Convolutional Neural Networks, translational symmetry is built in as a geometric prior through convolutional filters with shared weights. (Bronstein et al., 2021) `ev:asserted` p. 15 ^bronstein2021geometric-010
- In Convolutional Neural Networks, the scale separation prior is built in through pooling operations, according to the authors. (Bronstein et al., 2021) `ev:asserted` p. 15 ^bronstein2021geometric-011
- The authors state that the symmetry prior improves learning efficiency by reducing the space of possible interpolants to those satisfying it. (Bronstein et al., 2021) `ev:asserted` p. 19 ^bronstein2021geometric-012
- Convolutional layers in CNNs are shift-equivariant rather than shift-invariant, since a shifted input shifts the output feature maps equally. (Bronstein et al., 2021) `ev:asserted` p. 20 ^bronstein2021geometric-013
- Small deformations do not form a group because they can be composed into large deformations, violating the closure property. (Bronstein et al., 2021) `ev:computed` p. 24 ^bronstein2021geometric-014
- The authors replace exact invariance with deformation stability, bounding output change by a constant times deformation cost times the signal norm. (Bronstein et al., 2021) `ev:asserted` p. 24 ^bronstein2021geometric-015
- Under approximate translations, the Fourier modulus representation changes by O(1) relative to the signal, however close the deformation is to a shift. (Bronstein et al., 2021) `ev:computed` p. 29 ^bronstein2021geometric-016
- Citing Mallat (2012), the authors state that wavelet decompositions are approximately equivariant to deformations with relative error of order O(ϵ). (Bronstein et al., 2021) `ev:cited` p. 29 ^bronstein2021geometric-017
- A linear G-invariant function depends on its input only through the group average, which for translated images means the average RGB colour. (Bronstein et al., 2021) `ev:computed` p. 31 ^bronstein2021geometric-018
- The authors state that a single local equivariant layer cannot approximate functions with long-range interactions between distant domain points. (Bronstein et al., 2021) `ev:asserted` p. 32 ^bronstein2021geometric-019
- The geometry of the input domain and its symmetry group provide three building blocks: local equivariant maps, global invariant maps, and coarsening. (Bronstein et al., 2021) `ev:asserted` p. 32 ^bronstein2021geometric-020
- The Blueprint composes linear G-equivariant layers, element-wise nonlinearities and local pooling, followed by a G-invariant global pooling layer. (Bronstein et al., 2021) `ev:asserted` p. 33 ^bronstein2021geometric-021
- The authors list CNNs on grids with translations, GNNs on graphs with permutations, and Transformers on complete graphs with permutations. (Bronstein et al., 2021) `ev:asserted` p. 34 ^bronstein2021geometric-022
- Functions on graphs should not depend on node ordering, because nodes are usually not assumed to be provided in any particular order. (Bronstein et al., 2021) `ev:asserted` p. 36 ^bronstein2021geometric-023
- Any linear permutation-equivariant map on sets can be written as a linear combination of two generators, the identity and the average. (Bronstein et al., 2021) `ev:computed` p. 37 ^bronstein2021geometric-024
- As observed by Maron et al. (2018), linear permutation-equivariant functions on graphs are linear combinations of fifteen linear generators. (Bronstein et al., 2021) `ev:cited` p. 37 ^bronstein2021geometric-025
- When the local aggregation function is injective, a GNN step is equivalent to one step of the Weisfeiler-Lehman graph isomorphism test. (Bronstein et al., 2021) `ev:asserted` p. 38 ^bronstein2021geometric-026
- A matrix is circulant exactly when it commutes with the shift, so convolution emerges from the principle of translational symmetry. (Bronstein et al., 2021) `ev:computed` p. 41 ^bronstein2021geometric-027
- On general graphs the Fourier basis depends on graph structure, so Fourier transforms on two different graphs cannot be directly compared. (Bronstein et al., 2021) `ev:asserted` p. 43 ^bronstein2021geometric-028
- The authors derive that every linear translation-equivariant operator on the real line is a convolution, via the Fourier eigenbasis of shifts. (Bronstein et al., 2021) `ev:computed` p. 44 ^bronstein2021geometric-029
- Citing Aflalo et al. (2015), the authors state no other basis attains better truncation error, making the Laplacian eigenbasis optimal for smooth signals. (Bronstein et al., 2021) `ev:cited` p. 57 ^bronstein2021geometric-030
- Spectral convolution on manifolds is geometrically unstable, as high-frequency Laplacian eigenfunctions can change dramatically under small near-isometric domain perturbations. (Bronstein et al., 2021) `ev:asserted` p. 58 ^bronstein2021geometric-031
- A smooth global gauge may not exist on non-parallelisable manifolds such as the sphere, where no smooth non-vanishing tangent field exists. (Bronstein et al., 2021) `ev:asserted` p. 60 ^bronstein2021geometric-032
- Following Wardetzky (2008), the cotangent mesh Laplacian converges to the continuous Laplacian operator when the mesh is infinitely refined. (Bronstein et al., 2021) `ev:cited` p. 67 ^bronstein2021geometric-033
- The authors state that the non-Euclidean Fourier transform appears extremely sensitive to even minor perturbations of the underlying mesh or graph. (Bronstein et al., 2021) `ev:asserted` p. 68 ^bronstein2021geometric-034
- Citing Levie et al. and others, the authors state that polynomial and rational spectral filters are stable under approximate isometric deformations. (Bronstein et al., 2021) `ev:cited` p. 69 ^bronstein2021geometric-035
- Wang et al. (2019a) showed that remeshing-invariant functions of a mesh operator involve only its spectrum, meaning its eigenvalues. (Bronstein et al., 2021) `ev:cited` p. 71 ^bronstein2021geometric-036
- The authors interpret residual networks as a forward Euler discretisation of an ordinary differential equation whose velocity is learned. (Bronstein et al., 2021) `ev:asserted` p. 77 ^bronstein2021geometric-037
- Citing Mei et al. (2021), the authors describe data augmentation as provably sub-optimal in terms of sample complexity. (Bronstein et al., 2021) `ev:cited` p. 78 ^bronstein2021geometric-038
- The authors claim that the vast majority of the GNN literature may be derived from only three flavours of GNN layers. (Bronstein et al., 2021) `ev:asserted` p. 82 ^bronstein2021geometric-039
- The three GNN flavours show representational containment, with convolutional layers contained in attentional ones, themselves contained in message-passing. (Bronstein et al., 2021) `ev:computed` p. 83 ^bronstein2021geometric-040
- Message-passing GNNs typically require unwieldy amounts of memory, as they have to compute vector-valued messages across graph edges. (Bronstein et al., 2021) `ev:asserted` p. 84 ^bronstein2021geometric-041
- On homophilous graphs, convolutional aggregation across neighbourhoods is often a far better choice for regularisation and scalability, the authors state. (Bronstein et al., 2021) `ev:asserted` p. 84 ^bronstein2021geometric-042
- Deep Sets correspond to a convolutional GNN in which each node's neighbourhood contains only itself, equivalently an identity adjacency matrix. (Bronstein et al., 2021) `ev:computed` p. 85 ^bronstein2021geometric-043
- Following Joshi (2020), the authors pose Transformers exactly as attentional GNNs operating over a complete graph of input elements. (Bronstein et al., 2021) `ev:cited` p. 86 ^bronstein2021geometric-044
- Transformer positional encodings relate to the discrete Fourier transform, implicitly representing the assumption that input nodes are connected in a grid. (Bronstein et al., 2021) `ev:asserted` p. 86 ^bronstein2021geometric-045
- The equivariant layer of Satorras et al. (2021) treats node features as scalars, which limits the spatial information it can capture. (Bronstein et al., 2021) `ev:asserted` p. 88 ^bronstein2021geometric-046
- According to the authors, isotropic mesh filters might fail to extract edge-like features, having discarded important directional information. (Bronstein et al., 2021) `ev:asserted` p. 91 ^bronstein2021geometric-047
- An RNN on zero-padded sequences is equivariant to left shifts when the initial summary is a fixed point of R(0, h). (Bronstein et al., 2021) `ev:computed` p. 97 ^bronstein2021geometric-048
- The authors note that using ReLU activations in RNNs may easily lead to exploding gradients, since the update output is unbounded. (Bronstein et al., 2021) `ev:asserted` p. 98 ^bronstein2021geometric-049
- Requiring invariance to time warping yields an RNN update where a learnable gate interpolates between the new update and the previous summary. (Bronstein et al., 2021) `ev:computed` p. 103 ^bronstein2021geometric-050
- SimpleRNNs are not time-warping invariant, since they fully overwrite the summary vector, which corresponds to assuming no time warping. (Bronstein et al., 2021) `ev:computed` p. 103 ^bronstein2021geometric-051
- The authors conclude that the time-warping-invariant form they derived exactly corresponds to the class of gated recurrent neural networks. (Bronstein et al., 2021) `ev:computed` p. 104 ^bronstein2021geometric-052
- Chrono initialisation, dubbed by Tallec and Ollivier (2018), has been empirically shown to improve long-range dependency modelling of gated RNNs. (Bronstein et al., 2021) `ev:cited` p. 104 ^bronstein2021geometric-053
- The authors note that less than 5% of drug candidates make it to the last stage of testing, citing Gaudelet et al. (Bronstein et al., 2021) `ev:cited` p. 106 ^bronstein2021geometric-054
- Stokes et al. (2020) used a graph neural network predicting bacterial growth inhibition to discover that Halicin is a highly potent antibiotic. (Bronstein et al., 2021) `ev:cited` p. 107 ^bronstein2021geometric-055
- A GNN-based ETA predictor from DeepMind is deployed in Google Maps, with relative prediction improvements of 40+% in cities like Sydney. (Bronstein et al., 2021) `ev:cited` p. 110 ^bronstein2021geometric-056
- Citing Morris et al. (2019) and Xu et al. (2018), the authors state that no three-flavour GNN can exceed the WL test's power. (Bronstein et al., 2021) `ev:cited` p. 124 ^bronstein2021geometric-057
- Xu et al. (2018) showed that reaching WL-level power in discrete-feature domains requires an injective aggregation function, with summation as a representative. (Bronstein et al., 2021) `ev:cited` p. 124 ^bronstein2021geometric-058
- The higher-order k-GNN is provably more powerful than standard GNN flavours, but in practice is hard to scale beyond k = 3. (Bronstein et al., 2021) `ev:cited` p. 125 ^bronstein2021geometric-059
- The term Geometric Deep Learning was first introduced by one of the authors in his ERC grant in 2015. (Bronstein et al., 2021) `ev:asserted` p. 130 ^bronstein2021geometric-060

## 🎯 Contributions

## 📖 Glossary

- **Geometric Deep Learning Blueprint** — Composition of equivariant layers, nonlinearities, local pooling and a final invariant global pooling.
- **G-invariance** — Output unchanged when the group G acts on the input signal.
- **G-equivariance** — Group action on the input transforms the output in the same way.
- **Deformation stability** — Output change bounded by how far a transformation is from the symmetry group.
- **Scale separation** — Prior that a function factorises through coarse-grained versions of the domain.
- **Homogeneous space** — Domain where a group can map any point to any other point.
- **Gauge** — A choice of local frame for tangent or feature spaces at each point.
- **Circulant matrix** — Matrix built from circular shifts of one vector; equivalent to discrete convolution.
- **Weisfeiler-Lehman test** — Iterative colour-refinement test giving a necessary condition for graph isomorphism.
- **Time warping** — Monotonically increasing differentiable remapping of time, an automorphism of the time domain.

## ❓ Open questions

- What rigorous theory explains the trade-off between depth and filter size in CNN architectures?
- What general theory explains why normalisation layers help optimisation?
- What are the statistical learning benefits of scale separation, which the authors defer to future work?
- How can latent graph inference balance a discrete structure-learning objective with gradient-based downstream training?
- How should GNNs be designed to extrapolate beyond the size and distribution of their training graphs?
- How can equivariant networks efficiently use general tensor-valued features rather than scalar node features?

## 📝 Notes on reading

The cached text is the arXiv v2 preprint (2 May 2021), a 160-page monograph with no experiments of its own; claims are therefore `asserted`, `computed` (derivations) or `cited`. Locators use the cache page markers, which run four pages ahead of the printed page numbers (e.g. cache p. 12 is printed page 8). Pages 133 to 160 are the bibliography and carry no claims. Many figures (Figures 2, 3, 6, 8, 12, 15, 17, 20, 21) are only described in captions; Figure 15's architecture diagrams and the Figure 14 convolution example extracted as garbled number grids and were not claimed. Equations are partly garbled by extraction (fractions, sums, integrals), so claims describe results in words rather than quoting formulas. Section 4.3 refers back to Section 5.3 (as we have seen in Section 5.3) although that section comes later in the text. Section 5.4 (Transformers) and Section 6 (applications) summarise other groups' results; application numbers such as 40+% for Google Maps come from a margin note and are reported, not measured, by the authors.

## Suggested new concepts

- Geometric Deep Learning Blueprint — a unifying template reused across CNNs, GNNs, Transformers and mesh networks.
- Deformation stability — a softer notion than invariance that recurs in scattering, spectral filters and graph stability results.
- Gauge equivariance — a symmetry acting separately on feature spaces at each point, central to mesh and manifold CNNs.
- Weisfeiler-Lehman expressivity — the standard yardstick for GNN expressive power and higher-order variants.
- Time warping invariance — links gated RNNs and chrono initialisation to a symmetry principle.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Blueprint unificado del aprendizaje profundo geométrico.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
