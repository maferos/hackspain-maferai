---
aliases: ["PBVS", "pose-based visual servoing"]
type: concept
element_type: method
topic: "[[Camera-robot calibration and visual servoing]]"
topics: ["[[Camera-robot calibration and visual servoing]]"]
created: 2026-09-19
---

## Working definition

Position-based visual servoing first estimates the relative 3D pose between the current and desired camera configurations from images and then drives the robot with a Cartesian control law on that pose error.

## Evidence

- [[Bateux2017visual - Visual Servoing from Deep Neural Networks#^bateux2017visual-007]] — The network is integrated with a position-based visual servoing control scheme that the authors describe as robust to occlusions and lighting variations.
- [[Bateux2017visual - Visual Servoing from Deep Neural Networks#^bateux2017visual-014]] — The resulting control scheme is pose-based visual servoing, which is globally asymptotically stable provided the estimated displacement is stable and correct enough.
- [[Chen2023cns - CNS Correspondence Encoded Neural Image Servo Policy#^chen2023cns-002]] — Position-based visual servoing, which estimates relative pose with an extra object model, suffers from imprecise object models and camera intrinsics.
- [[Chen2023cns - CNS Correspondence Encoded Neural Image Servo Policy#^chen2023cns-007]] — The neural policy is supervised by PBVS, which the authors state intrinsically has a larger convergence basin than IBVS.
- [[Chen2023cns - CNS Correspondence Encoded Neural Image Servo Policy#^chen2023cns-028]] — Supervision uses PBVS velocities whose linear part is divided by the ground-truth distance from scene centre to camera at the desired pose.
- [[Harish2020dfvs - DFVS Deep Flow Guided Scene Agnostic Image Based Visual#^harish2020dfvs-004]] — Saxena et al. used a deep network to estimate relative camera pose from an image pair, then a traditional PBVS controller.
- [[Lu2023markerless - Markerless Camera-to-Robot Pose Estimation via#^lu2023markerless-051]] — The visual servoing experiment runs on a Baxter robot, with PBVS based purely on RGB images from a single camera.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: extra (4 sources) · topic: Camera-robot calibration and visual servoing (drafter's packet `q5-calibration-servoing`, confirmed at the gate)
