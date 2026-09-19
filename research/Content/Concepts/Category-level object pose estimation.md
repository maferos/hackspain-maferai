---
aliases: ["Category-level 6D pose estimation", "Category-level pose estimation"]
type: concept
element_type: concept
topic: "[[6D object pose estimation]]"
topics: ["[[6D object pose estimation]]"]
created: 2026-09-19
---

## Working definition

Estimating the 6D pose, and usually the 3D size, of previously unseen object instances that belong to categories known at training time, without an exact CAD model of each instance.

## Evidence

- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-003]] — The paper presents, to the authors' knowledge, the first method for category-level 6D pose and size estimation of multiple objects.
- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-059]] — The authors conclude that their category-level approach can also achieve state-of-the-art performance on standard 6D pose estimation benchmarks.
- [[Zhang2023genpose - GenPose Generative Category-level Object Pose Estimation#^zhang2023genpose-005]] — GenPose formulates category-level object pose estimation as conditional generative modeling of the pose distribution given a partially observed point cloud.
- [[Zhang2023genpose - GenPose Generative Category-level Object Pose Estimation#^zhang2023genpose-038]] — The authors interpret the nearest-to-ground-truth results as showing tremendous potential of conditional generative models for category-level pose estimation.
- [[Zhang2023transnet - TransNet Transparent Object Manipulation Through#^zhang2023transnet-006]] — To the best of the authors' knowledge, TransNet is the first category-level pose estimation approach developed specifically for transparent objects.
- [[Zhang2023transnet - TransNet Transparent Object Manipulation Through#^zhang2023transnet-008]] — The authors state that category-level pose techniques for opaque objects require high-quality depth input provided by objects with Lambertian light reflectance.
- [[Ikeda2024diffusionnocs - DiffusionNOCS Managing Symmetry and Uncertainty in Sim2Real#^ikeda2024diffusionnocs-003]] — The authors note a lack of existing benchmarks suitable for evaluating zero-shot category-level pose estimation in novel real-world settings.
- [[Ikeda2024diffusionnocs - DiffusionNOCS Managing Symmetry and Uncertainty in Sim2Real#^ikeda2024diffusionnocs-004]] — According to the authors, current state-of-the-art instance and category-level object pose estimation methods are almost exclusively correspondence-based approaches.
- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-003]] — Category-level pose estimation methods generalize to novel instances of known classes but not to instances outside their training categories.
- [[Chen2022clearpose - ClearPose Large-scale Transparent Object Dataset and#^chen2022clearpose-061]] — The authors propose category-level pose estimation for transparent objects as an extension, since ClearPose has categories with similar shape.
- [[YenChen2020inerf - iNeRF Inverting Neural Radiance Fields for Pose Estimation#^yenchen2020inerf-007]] — The authors know of only one prior work providing RGB-only category-level pose estimation, the analysis-by-synthesis method of Chen et al.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 7 sources · topic: 6D object pose estimation (drafter's packet `q6-category-pose`, confirmed at the gate)
