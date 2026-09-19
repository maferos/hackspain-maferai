---
aliases: ["VN"]
type: concept
element_type: method
topic: "[[Equivariant networks and rotation representations]]"
topics: ["[[Equivariant networks and rotation representations]]"]
created: 2026-09-18
---

## Working definition

A building block for SO(3)-equivariant point-cloud networks in which each neuron is a 3D vector instead of a scalar, with linear layers, non-linearities, pooling and normalization redesigned so that rotating the input rotates every latent feature.

## Evidence

- [[Deng2021vector - Vector Neurons A General Framework for SO(3)-Equivariant#^deng2021vector-003]] — The Vector Neuron representation extends classical scalar neurons to 3D vectors, so latent features become ordered sequences of 3-vectors.
- [[Deng2021vector - Vector Neurons A General Framework for SO(3)-Equivariant#^deng2021vector-006]] — Vector neuron versions of PointNet and DGCNN were implemented and tested on classification, segmentation, and reconstruction as downstream tasks.
- [[Deng2021vector - Vector Neurons A General Framework for SO(3)-Equivariant#^deng2021vector-012]] — For each output vector neuron, the VN non-linearity learns two weight matrices that linearly map the input to a feature and a direction.
- [[Deng2021vector - Vector Neurons A General Framework for SO(3)-Equivariant#^deng2021vector-013]] — VN-ReLU keeps the feature unchanged when its inner product with the learned direction is non-negative, otherwise removing its component along that direction.
- [[Deng2021vector - Vector Neurons A General Framework for SO(3)-Equivariant#^deng2021vector-056]] — The authors suggest generalizing vector neurons to other transformation groups such as the full affine group, noting uniform scalings are straightforward.
- [[Huang2022edge - Edge Grasp Network A Graph-Based SE(3)-invariant Approach#^huang2022edge-017]] — Rotational invariance is obtained in two ways: training with SO(3) data augmentation, or building the network from SO(3)-equivariant Vector Neurons.
- [[Huang2022edge - Edge Grasp Network A Graph-Based SE(3)-invariant Approach#^huang2022edge-039]] — The Vector Neurons version is about three times slower at inference than EdgeGraspNet, taking 89 ms against 28 ms.
- [[Huang2022edge - Edge Grasp Network A Graph-Based SE(3)-invariant Approach#^huang2022edge-043]] — In test-loss curves, the Vector Neurons version learned fastest, while base EdgeGraspNet with augmentation converged to approximately the same level.
- [[Huang2022edge - Edge Grasp Network A Graph-Based SE(3)-invariant Approach#^huang2022edge-044]] — Without either Vector Neurons or data augmentation, the Edge Grasp Network overfits, which the authors take as evidence that SO(3) symmetry helps.
- [[Huang2022edge - Edge Grasp Network A Graph-Based SE(3)-invariant Approach#^huang2022edge-055]] — In the Vector Neurons version, equivariance is kept until the edge feature, then made invariant by multiplying with a network-generated matrix.
- [[Simeonov2021neural - Neural Descriptor Fields SE(3)-Equivariant Object#^simeonov2021neural-019]] — Rotation equivariance is obtained with Vector Neurons, an architecture giving the occupancy network full SO(3) equivariance.
- [[Simeonov2021neural - Neural Descriptor Fields SE(3)-Equivariant Object#^simeonov2021neural-020]] — Combining mean-centering with Vector Neurons yields complete SE(3) equivariance, which the authors state guarantees generalization to object poses unobserved during training.
- [[Yang2024equibot - EquiBot SIM(3)-Equivariant Diffusion Policy#^yang2024equibot-016]] — FiLM layers are made SO(3)-equivariant by replacing their vanilla linear layers with vector neuron layers.

## Relations

- RELATES_TO → [[Equivariant neural network]]
  · type: specialises
  · evidence: [[Simeonov2021neural - Neural Descriptor Fields SE(3)-Equivariant Object#^simeonov2021neural-019]]

## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 4 sources · topic: Equivariant networks and rotation representations (drafter's packet `p3-equivariance-rotations`, confirmed at the gate)
