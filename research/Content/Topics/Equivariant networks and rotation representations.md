---
aliases: []
type: topic
parent: Computer vision for manipulation
created: 2026-09-18
---

## Scope

How learning systems handle 3D rotations and rigid motions: network architectures that are equivariant or invariant to rotation, translation or scale groups by construction (steerable convolutions, vector neurons, tensor field networks, equivariant policies), how rotations are represented as network outputs or inputs (continuity, double cover, SVD and Gram-Schmidt mappings), probability distributions over rotations for uncertain pose, and the pose ambiguity that object symmetries cause for estimators and evaluation metrics. It deliberately excludes the general Lie-group mathematics of SO(3) and SE(3) (exponential maps, tangent spaces, Riemannian optimization), which belong to the Lie-group area, and it excludes 6D pose pipelines, benchmarks and datasets as such (render-and-compare refinement, BOP, YCB-Video) except where symmetry-induced ambiguity is the point.

## Concepts

- [[Steerable CNN]] — A convolutional network whose feature maps are fields of geometric quantities and whose kernels are linear combinations of pre-computed steerable basis kernels, so every layer is equivariant to rotations (and translations) of the input.
- [[Vector Neurons]] — A building block for SO(3)-equivariant point-cloud networks in which each neuron is a 3D vector instead of a scalar, with linear layers, non-linearities, pooling and normalization redesigned so that rotating the input rotates every latent feature.
- [[Rotation representation continuity]] — Whether the map from a rotation to the vector a network predicts is continuous, a property no representation of 3D rotations in four or fewer dimensions (Euler angles, axis-angle, quaternions) can have, and whose absence hampers learning when rotations are the network output.
- [[Pose ambiguity from symmetry]] — The situation in which several object or camera poses are indistinguishable in the observation because of symmetric shape, symmetric scenes or occlusion, so a single-answer pose estimator or error metric is ill-posed.
- [[Equivariant neural network]] — A neural network constrained by its architecture so that transforming the input by a group element, such as a rotation or translation, transforms the output in the corresponding way, giving guaranteed rather than learned symmetry.
- [[Tensor Field Network]] — An SE(3)-equivariant convolutional network for point clouds whose filters are spherical harmonics times learned radial functions, combined with features through tensor products.
- [[Bingham distribution]] — An antipodally symmetric probability distribution on unit quaternions used to express uncertainty over 3D rotations, whose mixtures can represent several plausible orientations at once.

## Subtopics

## Related topics

## ❓ Open questions

## Problems

- none yet: no problem names this topic as its topic

## History

- 2026-09-18 · Eki Gonzalez Flamarique · parent: root — new area for concepts promoted from the research batch, confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · parent: root → Computer vision for manipulation — grouped under the request's three axes
