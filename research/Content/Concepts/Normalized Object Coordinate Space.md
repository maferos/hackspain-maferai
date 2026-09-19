---
aliases: ["NOCS"]
type: concept
element_type: concept
topic: "[[6D object pose estimation]]"
topics: ["[[6D object pose estimation]]"]
created: 2026-09-19
---

## Working definition

A canonical unit-cube coordinate frame in which all instances of a category are consistently oriented and scaled, so that a network can predict per-pixel canonical coordinates (a NOCS map) and recover pose and size by aligning them with observed depth.

## Evidence

- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-004]] — In the Normalized Object Coordinate Space, all instances within a category are consistently oriented inside a common normalized space.
- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-006]] — The NOCS map captures the normalized shape of visible object parts by predicting dense correspondences between object pixels and the NOCS.
- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-012]] — NOCS is a 3D space within a unit cube, where each shape is uniformly scaled so its tight bounding-box diagonal has length 1.
- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-013]] — The authors argue NOCS maps are more robust than bounding boxes since they can operate when the object is only partially visible.
- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-028]] — The NOCS representation does not take symmetries into account, which resulted in large errors for some object classes.
- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-034]] — Pose and size come from aligning the NOCS point cloud to the masked depth point cloud with the Umeyama algorithm and RANSAC.
- [[Wang2019normalized - Normalized Object Coordinate Space for Category-Level 6D#^wang2019normalized-044]] — The authors interpret that predicting dense NOCS maps provides detailed information about object shape, parts, and visibility, which is critical for pose estimation.
- [[Ikeda2024diffusionnocs - DiffusionNOCS Managing Symmetry and Uncertainty in Sim2Real#^ikeda2024diffusionnocs-007]] — Instead of point clouds, DiffusionNOCS estimates dense canonical maps from multi-modal image inputs that recover both pose and partial geometry.
- [[Ikeda2024diffusionnocs - DiffusionNOCS Managing Symmetry and Uncertainty in Sim2Real#^ikeda2024diffusionnocs-010]] — DiffusionNOCS uses a DDPM to estimate NOCS maps, which enables multiple possible maps to be predicted from multiple noise samples.
- [[Ikeda2024diffusionnocs - DiffusionNOCS Managing Symmetry and Uncertainty in Sim2Real#^ikeda2024diffusionnocs-027]] — 6D pose and scale are estimated by registering masked depth points to NOCS map points with TEASER++.
- [[Wang2019pack - 6-PACK Category-level 6D Pose Tracker with Anchor-Based#^wang2019pack-004]] — NOCS estimates category-level 6D pose from RGB-D images by transforming every object pixel to a shared coordinate frame as keypoints.
- [[Jiang2023robotic - Robotic Perception of Transparent Objects A Review#^jiang2023robotic-067]] — The authors suggest transparent objects without distinct features can negatively influence NOCS prediction, resulting in poor pose estimation accuracy.

## Relations

- RELATES_TO → [[Category-level object pose estimation]]
  · type: solves
  · evidence: [[Wang2019pack - 6-PACK Category-level 6D Pose Tracker with Anchor-Based#^wang2019pack-004]]

## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 4 sources · topic: 6D object pose estimation (drafter's packet `q6-category-pose`, confirmed at the gate)
