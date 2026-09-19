---
aliases: []
type: "source"
title: "Neural population geometry: An approach for understanding biological and artificial neural networks"
citekey: "Chung2021neural"
doi: "10.48550/arXiv.2104.07059"
arxiv: "2104.07059"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2104.07059"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["SueYeon Chung", "L. F. Abbott"]
sha256: ["154902f4eccb1b24a765543b700b4f23655c2fad2a1a37bb6d6f03a694c180e5"]
pdf: "Content/Papers/Chung2021neural.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Chung2021neural.pdf]]

> [!abstract] One-sentence summary
> This review argues that analysing the geometry of neural manifolds, from linear separability and manifold capacity to topology and dynamics, offers a shared population-level language for explaining how biological and artificial neural networks implement tasks.

## Abstract

Advances in experimental neuroscience have transformed our ability to explore the structure and function of neural circuits. At the same time, advances in machine learning have unleashed the remarkable computational power of artificial neural networks (ANNs). While these two fields have different tools and applications, they present a similar challenge: namely, understanding how information is embedded and processed through high-dimensional representations to solve complex tasks. One approach to addressing this challenge is to utilize mathematical and computational tools to analyze the geometry of these high-dimensional representations, i.e., neural population geometry. We review examples of geometrical approaches providing insight into the function of biological and artificial neural networks: representation untangling in perception, a geometric theory of classification capacity, disentanglement and abstraction in cognitive systems, topological representations underlying cognitive maps, dynamic untangling in motor systems, and a dynamical approach to cognition. Together, these findings illustrate an exciting trend at the intersection of machine learning, neuroscience, and geometry, in which neural population geometry provides a useful population-level mechanistic descriptor underlying task implementation. Importantly, geometric descriptions are applicable across sensory modalities, brain regions, network architectures and timescales. Thus, neural population geometry has the potential to unify our understanding of structure and function in biological and artificial neural networks, bridging the gap between single neurons, populations and behavior. (arXiv)

## 🧠 Key ideas (atomic)

- The review surveys geometric approaches to neural population activity as a tool for understanding both biological and artificial neural networks. (Chung & Abbott, 2021) `ev:asserted` p. 2 ^chung2021neural-001
- Manifold-like representations arise when a set of neurons in a biological or artificial network shows variability in response to stimuli or [[Neural population dynamics|recurrent dynamics]]. (Chung & Abbott, 2021) `ev:asserted` p. 1 ^chung2021neural-002
- Patterns of activity across neurons or units correspond to manifold-like representations such as lines, surfaces, trajectories, subspaces and clouds of points in neural state space. (Chung & Abbott, 2021) `ev:cited` p. 2 ^chung2021neural-003
- Mainstream neuroscience analysis tools have transitioned from single-neuron approaches to population-level frameworks, driven by advances in recording techniques. (Chung & Abbott, 2021) `ev:cited` p. 2 ^chung2021neural-004
- The authors state that geometric analysis provides an approach suitable for addressing challenges posed by mixed selectivity and task variability in large populations. (Chung & Abbott, 2021) `ev:asserted` p. 2 ^chung2021neural-005
- A number of large-scale task-optimized ANNs have outperformed traditional neuronal models in accounting for neural activity. (Chung & Abbott, 2021) `ev:cited` p. 2 ^chung2021neural-006
- An often-heard objection is that using ANNs to model neural circuits merely replaces one complicated system with an equally complicated system. (Chung & Abbott, 2021) `ev:cited` p. 2 ^chung2021neural-007
- The authors propose that ANNs can serve as a testbed for developing population-level analysis techniques, even when these target neuroscience applications. (Chung & Abbott, 2021) `ev:asserted` p. 2 ^chung2021neural-008
- Neural population structures in real data are often not technically manifolds, mainly due to neural noise and also sparse input sampling. (Chung & Abbott, 2021) `ev:asserted` p. 3 ^chung2021neural-009
- The review defines neural population geometry as the configurations of neural manifolds embedded in the ambient neural state space. (Chung & Abbott, 2021) `ev:asserted` p. 3 ^chung2021neural-010
- Object or perceptual manifolds are sensory population structures arising from identity-preserving variabilities in the input stimulus space. (Chung & Abbott, 2021) `ev:asserted` p. 3 ^chung2021neural-011
- It has been hypothesized that ventral visual stream processing transforms object representations so that they become untangled, meaning linearly separable. (Chung & Abbott, 2021) `ev:cited` p. 3 ^chung2021neural-012
- Dividing two sets of neural population activities is more difficult when the separating surface must be curved rather than a hyperplane. (Chung & Abbott, 2021) `ev:asserted` p. 3 ^chung2021neural-013
- The temporal straightening hypothesis posits that visual processing also serves to straighten temporal response trajectories, easing prediction of future activity. (Chung & Abbott, 2021) `ev:cited` p. 3 ^chung2021neural-014
- Straightening of response trajectories occurs when natural video sequences are presented, but not when artificial video sequences are presented. (Chung & Abbott, 2021) `ev:cited` p. 4 ^chung2021neural-015
- In a context-switching task, an efficient solution lets transitions between contexts be accomplished by rotating or translating a dividing surface in state space. (Chung & Abbott, 2021) `ev:asserted` p. 4 ^chung2021neural-016
- Recordings from prefrontal cortex and hippocampus, plus task-trained networks, indicate disentangled representations quantified by a geometric measure called the parallelism score. (Chung & Abbott, 2021) `ev:cited` p. 4 ^chung2021neural-017
- Abstract, disentangled representations do not simply discard information about variables other than the abstracted ones, according to the cited work. (Chung & Abbott, 2021) `ev:cited` p. 4 ^chung2021neural-018
- Neuronal variability makes each repeated stimulus correspond not to a single point but to a point cloud in neural state space. (Chung & Abbott, 2021) `ev:asserted` p. 4 ^chung2021neural-019
- In this perspective, invariant object discrimination becomes the problem of separating neural manifolds, such as a dog manifold and a cat manifold. (Chung & Abbott, 2021) `ev:cited` p. 4 ^chung2021neural-020
- Statistical-physics theory formally connects object manifold capacity, a generalization of perceptron capacity, to manifold dimension, radius and correlation structure. (Chung & Abbott, 2021) `ev:cited` p. 5 ^chung2021neural-021
- The same level of linear separability can be achieved across different combinations of geometrical properties of object manifolds. (Chung & Abbott, 2021) `ev:cited` p. 5 ^chung2021neural-022
- A tradeoff between manifold dimensionality and radius lets large-dimension small-size and small-dimension large-size manifolds reach similar capacities. (Chung & Abbott, 2021) `ev:cited` p. 6 ^chung2021neural-023
- Manifold capacity also measures the storage capacity of a representation, meaning the maximum number of object classes that can be read out linearly. (Chung & Abbott, 2021) `ev:asserted` p. 6 ^chung2021neural-024
- According to manifold capacity theory, small manifold dimensions and radii predict high manifold capacity in a representation. (Chung & Abbott, 2021) `ev:cited` p. 6 ^chung2021neural-025
- Manifold capacity theory has shown how categorical information emerges across layers in ANNs for visual object recognition, speech recognition and language prediction. (Chung & Abbott, 2021) `ev:cited` p. 6 ^chung2021neural-026
- Promising preliminary results in mouse and macaque visual cortex show that manifold capacity theory can also be applied directly to neural data. (Chung & Abbott, 2021) `ev:cited` p. 6 ^chung2021neural-027
- Linear dimensionality reduction such as PCA finds the higher-dimensional embedding space rather than the curved intrinsic surface of neural data. (Chung & Abbott, 2021) `ev:asserted` p. 6 ^chung2021neural-028
- Nonlinear dimensionality reduction methods such as Isomap, LLE, tSNE, MDS, PHATE and UMAP assume topologically simple underlying manifolds. (Chung & Abbott, 2021) `ev:cited` p. 6 ^chung2021neural-029
- Common nonlinear dimensionality reduction methods can fail to capture neural manifold structure when the underlying topology is complex. (Chung & Abbott, 2021) `ev:asserted` p. 7 ^chung2021neural-030
- Chaudhuri et al. used Spline Parameterization for Unsupervised Decoding (SPUD) to discover the ring structure underlying the mammalian head direction system. (Chung & Abbott, 2021) `ev:cited` p. 7 ^chung2021neural-031
- SPUD relies on persistent homology, in which persistent features determine the intrinsic dimension used to discover non-trivial topological structure. (Chung & Abbott, 2021) `ev:cited` p. 7 ^chung2021neural-032
- In the SPUD study, mouse head direction could be decoded from a one-dimensional ring in post-subiculum and anterodorsal thalamus population activity. (Chung & Abbott, 2021) `ev:cited` p. 10 ^chung2021neural-033
- In the SPUD study, the one-dimensional ring structure encoding head direction was also found during sleep, despite the lack of sensory input. (Chung & Abbott, 2021) `ev:cited` p. 10 ^chung2021neural-034
- Manifold Inference from Neural Dynamics (MIND) was used to characterize CA1 hippocampal activity during a foraging and sound manipulation task. (Chung & Abbott, 2021) `ev:cited` p. 7 ^chung2021neural-035
- In MIND, distances between nearby neural states are defined by transition probabilities, giving [[Intrinsic dimension of neural representations|intrinsic dimensions]] relevant for topological task maps. (Chung & Abbott, 2021) `ev:cited` p. 7 ^chung2021neural-036
- In a closed dynamical system, [[Neural population dynamics|state-space trajectories]] cannot cross themselves, since one point cannot have two different rates of change. (Chung & Abbott, 2021) `ev:asserted` p. 8 ^chung2021neural-037
- A tangling index was introduced to identify when [[Neural population dynamics|trajectories of recorded neural populations]] actually cross or come close to crossing. (Chung & Abbott, 2021) `ev:cited` p. 8 ^chung2021neural-038
- During a cycling task, tangling was much lower in primary motor cortex than in primary sensory cortex or in muscle activity. (Chung & Abbott, 2021) `ev:cited` p. 8 ^chung2021neural-039
- Low tangling in primary motor cortex supports the idea that the motor cortex acts as a generator during the cycling task. (Chung & Abbott, 2021) `ev:asserted` p. 8 ^chung2021neural-040
- The highlighted tangling study suggests that motor cortex activity may be less driven by input dynamics, rendering better robustness to noise. (Chung & Abbott, 2021) `ev:cited` p. 10 ^chung2021neural-041
- During the cycling task, supplementary motor area activity followed a helical trajectory representing the sequence of cycles made. (Chung & Abbott, 2021) `ev:cited` p. 8 ^chung2021neural-042
- Motor cortex activity repeated across cycles of the cycling task, unlike the helical trajectory seen in supplementary motor area activity. (Chung & Abbott, 2021) `ev:cited` p. 8 ^chung2021neural-043
- Model recurrent neural networks developed a helical representation when required to keep track of the number of cycles generated. (Chung & Abbott, 2021) `ev:cited` p. 8 ^chung2021neural-044
- [[Neural population dynamics|Dynamic motifs in recurrent networks]] have long been related to cognitive functions, such as fixed points to memory and line attractors to integration. (Chung & Abbott, 2021) `ev:cited` p. 8 ^chung2021neural-045
- In macaque frontal cortex during a time reproduction task, experience was shown to warp neural population representations. (Chung & Abbott, 2021) `ev:cited` p. 8 ^chung2021neural-046
- Experience-driven warping of frontal population representations allows prior statistics to be incorporated into the map from sensory representation to motor output. (Chung & Abbott, 2021) `ev:cited` p. 8 ^chung2021neural-047
- Geometric analysis of recurrent networks trained on time reproduction revealed how trajectory curvature supports an underlying Bayesian computation. (Chung & Abbott, 2021) `ev:cited` p. 8 ^chung2021neural-048
- The authors argue that neural population geometry can serve as a more accurate population-level descriptor than simple task-level probes. (Chung & Abbott, 2021) `ev:asserted` p. 9 ^chung2021neural-049
- Representations with the same level of task capacity can have different geometric configurations, according to the cited manifold capacity work. (Chung & Abbott, 2021) `ev:cited` p. 9 ^chung2021neural-050
- The authors describe dimensionality as an important population-level metric capturing task information and representational redundancy. (Chung & Abbott, 2021) `ev:asserted` p. 9 ^chung2021neural-051
- Invariant object classification capacity is determined not only by an object manifold's dimension but also, crucially, by its radius. (Chung & Abbott, 2021) `ev:cited` p. 9 ^chung2021neural-052
- Future theory may need to formally connect representational geometric properties to encoded task information for a larger array of tasks. (Chung & Abbott, 2021) `ev:asserted` p. 9 ^chung2021neural-053
- The authors call for uncovering the relationship between population geometry and specific biophysical properties of neurons as a future direction. (Chung & Abbott, 2021) `ev:asserted` p. 9 ^chung2021neural-054
- In neural geometry underlying Bayesian computation, trajectory curvatures are linked to the distributions of priors encoded by each neuron. (Chung & Abbott, 2021) `ev:cited` p. 9 ^chung2021neural-055
- In deep networks for visual object recognition, a single layer of homogenous units exhibits a trade-off between various geometric transformations. (Chung & Abbott, 2021) `ev:cited` p. 9 ^chung2021neural-056
- Common network motifs involve beneficial changes to multiple geometric properties, suggesting a benefit of heterogeneity in neural populations. (Chung & Abbott, 2021) `ev:cited` p. 9 ^chung2021neural-057
- Different brain regions relevant for distinct tasks may implement optimal neural geometry engendered by specific neuronal constraints. (Chung & Abbott, 2021) `ev:asserted` p. 9 ^chung2021neural-058
- The authors suggest the neural population geometry approach may hold a key for unifying descriptions of structure and function across biological and artificial networks. (Chung & Abbott, 2021) `ev:asserted` p. 9 ^chung2021neural-059
- Manifold capacity is defined as a critical number of linearly separable category manifolds per neuron in a given neural representation. (Chung & Abbott, 2021) `ev:cited` p. 10 ^chung2021neural-060
- The parallelism score characterizes the degree to which coding directions are parallel for different sets of training conditions. (Chung & Abbott, 2021) `ev:cited` p. 11 ^chung2021neural-061
- Parallelism-conforming representations were observed in dorsolateral prefrontal cortex, anterior cingulate cortex and hippocampus of monkeys performing a serial reversal-learning task. (Chung & Abbott, 2021) `ev:cited` p. 11 ^chung2021neural-062

## 🎯 Contributions

## 📖 Glossary

- **Neural state space** — Space whose coordinates are the activities of individual neurons or units.
- **Neural manifold** — Low-dimensional structure of population activity embedded in high-dimensional neural state space.
- **Neural population geometry** — The configuration of neural manifolds embedded in the ambient neural state space.
- **Untangling** — Transforming representations so object categories become linearly separable.
- **Manifold capacity** — Critical number of linearly separable category manifolds per neuron in a representation.
- **Parallelism score** — Degree to which coding directions are parallel across different sets of conditions.
- **Tangling index** — Measure of how close population trajectories come to crossing themselves.
- **Persistent homology** — Topological technique using persistent features to infer intrinsic structure and dimension.
- **SPUD** — Spline Parameterization for Unsupervised Decoding; recovers topology of population activity.
- **MIND** — Manifold Inference from Neural Dynamics; defines state distances via transition probabilities.
- **Mixed selectivity** — Neuron selectivity to multiple coding variables at once.

## ❓ Open questions

- How can the formal link between representational geometry and encoded task information be extended to a larger array of tasks?
- Which biological properties (cell types, connectivity, activation profiles, sparsity) constrain and shape task-encoding geometry?
- Can geometric measures serve as testable population-level hypotheses rather than only descriptive tools?
- How can manifold capacity theory be applied robustly to noisy, sparsely sampled neural recordings rather than ANN activations?
- Which complementary geometric measures beyond dimensionality are needed for a full account of computation?

## 📝 Notes on reading

This is a short review (Current Opinion style) with no experiments of its own: almost every result is attributed to cited work, so claims are mostly `cited` or `asserted`, and no numeric results are reported. Figures 1 and 2 are schematic panels adapted from cited studies (straightening, parallelism, object manifolds and capacity, SPUD, MIND, M1/SMA trajectories, DMFC Bayesian profiles); they are described only. Fig. 2 caption calls SPUD "Spine Parameterization" and MIND "Manifold Inference for Neural Dynamics", while the body text uses "Spline" and "from". The page 10–11 annotations of highlighted papers add details (SPUD sleep result, parallelism brain regions, motor-cortex robustness) that were cited with those page locators. The body text contains a small typo on p. 8 ("providing s neural representation"). Version read: arXiv preprint 2104.07059.

## Suggested new concepts

- Neural population geometry — umbrella framing linking representational geometry across neuroscience and deep learning.
- Manifold capacity — quantitative link between manifold dimension/radius and linear separability, reusable for probing learned representations.
- Representation untangling — recurring hypothesis in perception and motor control about why hierarchies reshape representations.
- Parallelism score — geometric measure of abstraction and cross-condition generalization.
- Trajectory tangling — dynamical criterion to distinguish generator regions from input-driven ones.
- Topological manifold discovery — methods (SPUD, MIND, persistent homology) for recovering non-trivial topology from population data.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** Revisión que unifica la geometría de poblaciones (capacidad de variedades, dimensión, desenmarañamiento) en corteza y en redes profundas; el puente teórico que faltaba entre neurociencia y deep learning.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
