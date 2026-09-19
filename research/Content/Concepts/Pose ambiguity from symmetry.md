---
aliases: []
type: concept
element_type: phenomenon
topic: "[[Equivariant networks and rotation representations]]"
topics: ["[[Equivariant networks and rotation representations]]"]
created: 2026-09-18
---

## Working definition

The situation in which several object or camera poses are indistinguishable in the observation because of symmetric shape, symmetric scenes or occlusion, so a single-answer pose estimator or error metric is ill-posed.

## Evidence

- [[Hodan2018bop - BOP Benchmark for 6D Object Pose Estimation#^hodan2018bop-008]] — The authors state that their pose-error function deals well with pose ambiguity of symmetric or partially occluded objects, unlike the Hinterstoisser function.
- [[Hodan2018bop - BOP Benchmark for 6D Object Pose Estimation#^hodan2018bop-016]] — The error eVSD is calculated only over the visible part of the model surface, so indistinguishable poses are treated as equivalent.
- [[Hodan2018bop - BOP Benchmark for 6D Object Pose Estimation#^hodan2018bop-058]] — Very low scores of 3D-local-feature and learning-based methods on T-LESS are likely caused by object symmetries and similarities.
- [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-005]] — Unlike symmetry-aware methods, the approach tries to capture object symmetries in the multimodal predictions without explicit supervision of symmetry types.
- [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-015]] — The Multimodal Bingham Network predicts a multimodal Bingham distribution to capture different modes lying in the data, thus dissolving ambiguities.
- [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-020]] — The unimodal network grants predictions uncertainty information but cannot handle ambiguities such as objects with rotational symmetries.
- [[Geist2024learning - Learning with 3D rotations, a hitchhiker's guide to SO(3)#^geist2024learning-055]] — Occluded or symmetric objects may make the rotation learning problem ill-posed, as pointed out by Saxena et al.
- [[Mohlin2020probabilistic - Probabilistic orientation estimation with matrix Fisher#^mohlin2020probabilistic-051]] — Early in training, the predicted distribution for a symmetric table is almost uniform on the plane spanned by its ambiguous axes.
- [[Mohlin2020probabilistic - Probabilistic orientation estimation with matrix Fisher#^mohlin2020probabilistic-058]] — Since the matrix Fisher distribution is unimodal, it poorly models classes with rotational symmetries, the authors conclude.
- [[Wang2019densefusion - DenseFusion 6D Object Pose Estimation by Iterative Dense#^wang2019densefusion-049]] — Iterative refinement improves performance on the bowl by 29%, a texture-less symmetric object that suffers from orientation ambiguity.
- [[Peng2018pvnet - PVNet Pixel-wise Voting Network for 6DoF Pose Estimation#^peng2018pvnet-026]] — Symmetric objects are rotated to a canonical pose during training to remove ambiguities of keypoint locations, following earlier work.
- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-014]] — Since coarse estimation is framed as classification, the method can implicitly handle object symmetries, as multiple poses can be classified as correct.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 7 sources · topic: Equivariant networks and rotation representations (drafter's packet `p3-equivariance-rotations`, confirmed at the gate)
