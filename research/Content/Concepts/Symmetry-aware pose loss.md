---
aliases: ["Symmetry-aware loss", "Symmetry loss"]
type: concept
element_type: method
topic: "[[6D object pose estimation]]"
topics: ["[[6D object pose estimation]]"]
created: 2026-09-19
---

## Working definition

A pose training loss that does not penalise predictions equivalent under an object's symmetry, either by taking the minimum over the symmetric ground-truth poses or by matching each predicted model point to the closest ground-truth point.

## Evidence

- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-029]] — The symmetric loss takes the minimum loss over ground truth NOCS maps rotated about a predefined symmetry axis for each category.
- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-051]] — Without the symmetry loss, REAL275 regression accuracy at (5°, 5 cm) drops from 8.1 to 1.3 mAP.
- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-052]] — On CAMERA25, removing the symmetry loss lowers regression (5°, 5 cm) mAP from 29.2 to 14.7.
- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-025]] — ShapeMatch-Loss (SLOSS) measures, like ICP, the offset between each point of the estimated model orientation and the closest ground-truth model point.
- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-026]] — SLOSS does not require the specification of object symmetries, unlike a modified PLOSS that would enumerate all correct orientations.
- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-027]] — SLOSS will not penalize rotations that are equivalent with respect to the 3D shape symmetry of the object.
- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-063]] — The authors attribute the gains on the symmetric Eggbox and Glue objects to training with ShapeMatch-Loss, which respects object symmetry.
- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-068]] — The authors note that SLOSS sometimes results in local minimums in the pose space, similar to ICP.
- [[Ikeda2024diffusionnocs - DiffusionNOCS Managing Symmetry and Uncertainty in Sim2Real#^ikeda2024diffusionnocs-005]] — Wang et al. designed loss functions for specific symmetry types, which the authors attribute to the deterministic nature of their training.
- [[Hsiao2023confronting - Confronting Ambiguity in 6D Object Pose Estimation via#^hsiao2023confronting-002]] — The authors argue that symmetry-aware losses depend on symmetry annotations, which are particularly challenging to obtain for intricate shapes or occluded objects
- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-008]] — Direct regression methods for coarse pose estimation are trained with symmetry-specific losses, requiring object symmetries to be known in advance.
- [[Liu2019keypose - KeyPose Multi-View 3D Labeling and Keypoint Estimation for#^liu2019keypose-047]] — Without the permutation loss, the two symmetric side keypoints of the tree object clustered in the center to minimize loss

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 6 sources · topic: 6D object pose estimation (drafter's packet `q6-category-pose`, confirmed at the gate)
