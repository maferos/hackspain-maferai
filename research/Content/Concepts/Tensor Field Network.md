---
aliases: ["TFN"]
type: concept
element_type: method
topic: "[[Equivariant networks and rotation representations]]"
topics: ["[[Equivariant networks and rotation representations]]"]
created: 2026-09-18
---

## Working definition

An SE(3)-equivariant convolutional network for point clouds whose filters are spherical harmonics times learned radial functions, combined with features through tensor products.

## Evidence

- [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant#^fuchs2020se-005]] — Tensor field networks and 3D steerable CNNs are the works closest to the SE(3)-Transformer, providing SE(3)-equivariant convolutional frameworks for point clouds.
- [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant#^fuchs2020se-006]] — According to the authors, using self-attention instead of convolutions naturally handles edge features, extending tensor field networks to the graph setting.
- [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant#^fuchs2020se-008]] — The angular constraint on filters in tensor field networks has been pointed out in the equivariance literature to limit performance severely.
- [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant#^fuchs2020se-013]] — In tensor field networks, each basis kernel completely constrains the angular form of the learned kernel, leaving only radial learnable freedom.
- [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant#^fuchs2020se-017]] — Removing the attention weights from the SE(3)-Transformer layer recovers a tensor field convolution, according to the authors.
- [[Geiger2022e3nn - e3nn Euclidean Neural Networks#^geiger2022e3nn-058]] — 3D Steerable CNNs articulate filters as a tensor product operation on the spherical harmonic expansion, whereas in Tensor Field Networks the filter is that expansion.
- [[Geiger2022e3nn - e3nn Euclidean Neural Networks#^geiger2022e3nn-059]] — To reduce computational overhead on point clouds, Tensor Field Networks add no weights in the tensor product and apply a linear operation afterward.
- [[Geiger2022e3nn - e3nn Euclidean Neural Networks#^geiger2022e3nn-060]] — In e3nn the difference between Tensor Field Networks and 3D Steerable CNNs is implemented as the uvu versus uvw connection modes.
- [[Weiler20183d - 3D Steerable CNNs Learning Rotationally Equivariant#^weiler20183d-003]] — Unlike Tensor Field Networks and N-Body networks, which work on irregular point clouds, 3D Steerable CNNs operate on regular 3D grids.
- [[Weiler20183d - 3D Steerable CNNs Learning Rotationally Equivariant#^weiler20183d-006]] — In contrast to TFN, the filter basis is derived directly from an equivariance constraint, which lets the authors prove its completeness.
- [[Deng2021vector - Vector Neurons A General Framework for SO(3)-Equivariant#^deng2021vector-002]] — The authors state that Tensor Field Networks and SE(3)-Transformers are hard to incorporate into existing pipelines, being restricted to convolutions.

## Relations

- RELATES_TO → [[Equivariant neural network]]
  · type: specialises
  · evidence: [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant#^fuchs2020se-005]]

## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (4 sources) · topic: Equivariant networks and rotation representations (drafter's packet `p3-equivariance-rotations`, confirmed at the gate)
