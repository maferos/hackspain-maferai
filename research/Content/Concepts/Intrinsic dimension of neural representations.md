---
aliases: []
type: concept
element_type: metric
topic: "[[Neural manifolds in deep networks and motor neuroscience]]"
topics: ["[[Neural manifolds in deep networks and motor neuroscience]]"]
created: 2026-09-19
---

## Working definition

The number of degrees of freedom needed to describe the manifold on which a layer's (or a neural population's) activity vectors lie, typically far smaller than the number of units or neurons.

## Evidence

- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-001]] — The paper studies how the intrinsic dimension of data representations varies across the layers of convolutional networks trained for image classification
- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-019]] — Plotted against relative depth, the ID profiles of 14 models approximately collapsed onto a common hunchback shape
- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-023]] — The authors speculate that progressive reduction of manifold dimensionality could be a feature that allows deep networks to generalize well
- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-026]] — The training-set ID in the last hidden layer predicted top 5-score test performance across networks, with Pearson correlation r = 0.94
- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-037]] — Training reduced the last-hidden-layer ID relative to its initial value, whereas the ID of intermediate layers increased by a large amount
- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-051]] — To the authors, progressive reduction of the ID, rather than gradual flattening, seems to be the key to linearly separable representations
- [[Valeriani2023geometry - The geometry of hidden representations of large transformer#^valeriani2023geometry-001]] — The authors study the intrinsic dimension and neighbor composition of hidden representations in ESM-2 and Image GPT, two self-supervised transformer families.
- [[Valeriani2023geometry - The geometry of hidden representations of large transformer#^valeriani2023geometry-003]] — The authors propose that these models perform reconstruction in three phases: expansion to high intrinsic dimension, compression, then decoding.
- [[Valeriani2023geometry - The geometry of hidden representations of large transformer#^valeriani2023geometry-018]] — In ESM-2 protein language models the ID profile shows three distinct phases: a peak phase, a plateau phase, then a final ascent.
- [[Valeriani2023geometry - The geometry of hidden representations of large transformer#^valeriani2023geometry-039]] — In ESM-2 (650M) the plateau-layer ID substantially decreases in a later training stage, after the initial ID peak has emerged.
- [[Valeriani2023geometry - The geometry of hidden representations of large transformer#^valeriani2023geometry-057]] — The authors state that the relation between low ID after encoding and abstract content is robust in all models considered.
- [[Sussillo2016lfads - LFADS - Latent Factor Analysis via Dynamical Systems#^sussillo2016lfads-008]] — The low-dimensional factors rest on the observation that intrinsic dimensionality of neural recordings tends to be far lower than neurons recorded.
- [[Chung2021neural - Neural population geometry An approach for understanding#^chung2021neural-036]] — In MIND, distances between nearby neural states are defined by transition probabilities, giving intrinsic dimensions relevant for topological task maps.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 4 sources · topic: Neural manifolds in deep networks and motor neuroscience (drafter's packet `q8-neural-manifolds`, confirmed at the gate)
