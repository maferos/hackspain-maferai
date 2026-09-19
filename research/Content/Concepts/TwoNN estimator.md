---
aliases: []
type: concept
element_type: method
topic: "[[Neural manifolds in deep networks and motor neuroscience]]"
topics: ["[[Neural manifolds in deep networks and motor neuroscience]]"]
created: 2026-09-19
---

## Working definition

An intrinsic-dimension estimator that fits the Pareto distribution followed by the ratio of each point's second to first nearest-neighbour distance, needing only those two distances per point.

## Evidence

- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-002]] — Intrinsic dimension is estimated with TwoNN, a global estimator based on the ratio of second to first nearest-neighbour distances
- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-003]] — According to the authors, TwoNN can be applied even when the data manifold is curved, topologically complex and sampled non-uniformly
- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-004]] — Under TwoNN, the ratio of second to first neighbour distances follows a Pareto distribution with parameter d + 1
- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-005]] — For finite samples, TwoNN moderately underestimates IDs larger than ∼20, especially when the density of the data is non-uniform
- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-030]] — PC-ID, the number of components describing 90% of the variance, was about one or two orders of magnitude larger than the TwoNN ID
- [[Ansuini2019intrinsic - Intrinsic dimension of data representations in deep neural#^ansuini2019intrinsic-033]] — The authors interpret the TwoNN versus PCA discrepancy as pointing to strong non-linearities in correlations not captured by the covariance matrix
- [[Valeriani2023geometry - The geometry of hidden representations of large transformer#^valeriani2023geometry-005]] — Intrinsic dimension is measured with the TwoNN estimator, which needs only the distances from each point to its first two nearest neighbors.
- [[Valeriani2023geometry - The geometry of hidden representations of large transformer#^valeriani2023geometry-007]] — The study adopts the TwoNN implementation of the DADApy library for its intrinsic dimension analysis of hidden representations.
- [[Valeriani2023geometry - The geometry of hidden representations of large transformer#^valeriani2023geometry-065]] — The reported ID values are TwoNN estimates on the dataset decimated by a factor of 4, where scale dependence was low.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: extra (2 sources) · topic: Neural manifolds in deep networks and motor neuroscience (drafter's packet `q8-neural-manifolds`, confirmed at the gate)
