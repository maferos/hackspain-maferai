---
aliases: []
type: concept
element_type: framework
topic: "[[Equivariant networks and rotation representations]]"
topics: ["[[Equivariant networks and rotation representations]]"]
created: 2026-09-18
---

## Working definition

A neural network constrained by its architecture so that transforming the input by a group element, such as a rotation or translation, transforms the output in the corresponding way, giving guaranteed rather than learned symmetry.

## Evidence

- [[Wang2022so - SO(2)-Equivariant Reinforcement Learning#^wang2022so-001]] — Equivariant neural networks structure the model architecture such that it is constrained to represent only functions with the desired invariance properties.
- [[Wang2022so - SO(2)-Equivariant Reinforcement Learning#^wang2022so-002]] — The authors argue that data augmentation yields only approximate equivariance, whereas equivariant networks guarantee it and often generalize better.
- [[Wang2022so - SO(2)-Equivariant Reinforcement Learning#^wang2022so-007]] — The authors state that data augmentation methods are often less sample efficient than equivariant networks, which inject an inductive bias into the architecture.
- [[Wang2022so - SO(2)-Equivariant Reinforcement Learning#^wang2022so-043]] — The authors suggest equivariant models are important for learning from demonstration, not only for unstructured reinforcement learning.
- [[Geiger2022e3nn - e3nn Euclidean Neural Networks#^geiger2022e3nn-012]] — Many papers have documented improved accuracy on training tasks when going from invariant to equivariant models, even within the same framework.
- [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant#^fuchs2020se-004]] — The authors state that SE(3)-equivariance restricts learnable functions to a subspace respecting task symmetries, which reduces the number of learnable parameters.
- [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant#^fuchs2020se-053]] — Compared to conventional attention, adding the equivariance constraints increased performance in all of the authors' experiments.
- [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant#^fuchs2020se-064]] — The authors state their results are in line with equivariance decreasing sample complexity but do not give definitive support.
- [[Finzi2020generalizing - Generalizing Convolutional Neural Networks for Equivariance#^finzi2020generalizing-047]] — The authors conclude that added equivariances are especially important in the low data regime of the equivariance demonstration.
- [[Yang2024equibot - EquiBot SIM(3)-Equivariant Diffusion Policy#^yang2024equibot-030]] — The authors attribute EquiBot's data efficiency to equivariance letting it cope with initial object poses not covered by small training sets.
- [[Yang2024equibot - EquiBot SIM(3)-Equivariant Diffusion Policy#^yang2024equibot-044]] — Removing any of rotation, translation or scale equivariance causes performance drops when evaluation is out-of-distribution for the removed equivariance.
- [[Weiler20183d - 3D Steerable CNNs Learning Rotationally Equivariant#^weiler20183d-044]] — The authors note that, due to their rotational equivariance, 3D Steerable CNNs benefit only marginally from rotational data augmentation compared to the baseline.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (6 sources) · topic: Equivariant networks and rotation representations (drafter's packet `p3-equivariance-rotations`, confirmed at the gate)
