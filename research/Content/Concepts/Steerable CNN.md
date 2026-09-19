---
aliases: ["steerable G-CNN"]
type: concept
element_type: method
topic: "[[Equivariant networks and rotation representations]]"
topics: ["[[Equivariant networks and rotation representations]]"]
created: 2026-09-18
---

## Working definition

A convolutional network whose feature maps are fields of geometric quantities and whose kernels are linear combinations of pre-computed steerable basis kernels, so every layer is equivariant to rotations (and translations) of the input.

## Evidence

- [[Cohen2019general - A General Theory of Equivariant CNNs on Homogeneous Spaces#^cohen2019general-052]] — For SE(3), equivariant maps are convolutions with matrix-valued kernels on R3 satisfying a rotation constraint, in agreement with 3D Steerable CNNs.
- [[Finzi2020generalizing - Generalizing Convolutional Neural Networks for Equivariance#^finzi2020generalizing-032]] — E(2)-Steerable CNNs report 0.68% error on RotMNIST, lower than every LieConv variant listed in the same table.
- [[Finzi2020generalizing - Generalizing Convolutional Neural Networks for Equivariance#^finzi2020generalizing-033]] — The authors acknowledge that more practical equivariant methods specialized to images exist, such as the steerable CNNs of Weiler and Cesa.
- [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant#^fuchs2020se-005]] — Tensor field networks and 3D steerable CNNs are the works closest to the SE(3)-Transformer, providing SE(3)-equivariant convolutional frameworks for point clouds.
- [[Geiger2022e3nn - e3nn Euclidean Neural Networks#^geiger2022e3nn-058]] — 3D Steerable CNNs articulate filters as a tensor product operation on the spherical harmonic expansion, whereas in Tensor Field Networks the filter is that expansion.
- [[Wang2022so - SO(2)-Equivariant Reinforcement Learning#^wang2022so-051]] — The equivariant models were implemented using the E2CNN steerable CNN library together with PyTorch for all experiments.
- [[Wang2022so - SO(2)-Equivariant Reinforcement Learning#^wang2022so-052]] — The Equivariant DQN is a 7-layer Steerable CNN in the group C4 whose output is an 18-channel 3 × 3 feature map.
- [[Weiler20183d - 3D Steerable CNNs Learning Rotationally Equivariant#^weiler20183d-003]] — Unlike Tensor Field Networks and N-Body networks, which work on irregular point clouds, 3D Steerable CNNs operate on regular 3D grids.
- [[Weiler20183d - 3D Steerable CNNs Learning Rotationally Equivariant#^weiler20183d-008]] — The earlier regular 3D G-CNNs are equivariant only to certain discrete rotations, in contrast to the continuous equivariance of 3D Steerable CNNs.
- [[Weiler20183d - 3D Steerable CNNs Learning Rotationally Equivariant#^weiler20183d-020]] — The authors state that, unlike regular G-CNNs, steerable G-CNNs require special equivariant nonlinearities rather than arbitrary elementwise ones.
- [[Weiler20183d - 3D Steerable CNNs Learning Rotationally Equivariant#^weiler20183d-030]] — On randomly rotated Tetris test blocks, the 3D Steerable CNN achieved 99±2% accuracy, whereas a conventional CNN reached only 27±7% over 17 runs.
- [[Weiler20183d - 3D Steerable CNNs Learning Rotationally Equivariant#^weiler20183d-044]] — The authors note that, due to their rotational equivariance, 3D Steerable CNNs benefit only marginally from rotational data augmentation compared to the baseline.
- [[Weiler20183d - 3D Steerable CNNs Learning Rotationally Equivariant#^weiler20183d-045]] — Despite having 100 times fewer parameters, the 3D Steerable CNN showed a clear accuracy benefit over the baseline on the CATH test set.

## Relations

- RELATES_TO → [[Equivariant neural network]]
  · type: specialises
  · evidence: [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant#^fuchs2020se-005]]

## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 6 sources · topic: Equivariant networks and rotation representations (drafter's packet `p3-equivariance-rotations`, confirmed at the gate)
