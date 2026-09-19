---
aliases: []
type: concept
element_type: method
topic: "[[6D object pose estimation]]"
topics: ["[[6D object pose estimation]]"]
created: 2026-09-18
---

## Working definition

Iteratively correcting a 6D object pose estimate by rendering the object model at the current pose and letting a network compare the rendering with the observed image to predict a pose update.

## Evidence

- [[Hodan2024bop - BOP Challenge 2023 on Detection, Segmentation and Pose#^hodan2024bop-049]] — MegaPose, the Task 4 baseline, estimates coarse pose by template matching against renderings, then refines the pose by render-and-compare.
- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-005]] — The approach splits pose estimation into 2D detection, coarse pose estimation, and iterative refinement via render and compare, taking inspiration from CosyPose.
- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-007]] — In existing render-and-compare refiners, object appearance and coordinate system are encoded in the network weights, leading to poor generalization on novel objects.
- [[Labbe2020cosypose - CosyPose Consistent multi-view multi-object 6D pose#^labbe2020cosypose-010]] — The single-view pose refiner replaces the FlowNet backbone of DeepIM with a more recent EfficientNet-B3 network followed by spatial average pooling.
- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-024]] — The RGB-D refinement network improves the coarse estimates by +41.0 mean AR score on the BOP datasets.
- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-030]] — Applying the MegaPose RGB-D refiner to CosyPose coarse estimates improves accuracy by +23.7 AR on average across BOP datasets.
- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-033]] — One iteration of the refiner takes approximately 50 milliseconds on a RTX 2080 GPU, which the authors deem suitable for online tracking.
- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-038]] — For the RGB-only refiner, BOP5 average recall rises from 52.0 to 61.7 as rendered views increase from 1 to 4.
- [[Lin2023sam - SAM-6D Segment Anything Model Meets Zero-Shot 6D Object#^lin2023sam-046]] — The PEM outperforms existing methods under various mask predictions without using the time-intensive render-based refiner of MegaPose.
- [[Wen2023foundationpose - FoundationPose Unified 6D Pose Estimation and Tracking of#^wen2023foundationpose-021]] — Unlike MegaPose, the refiner renders a single view at the coarse pose, which the authors observed suffices for refinement.
- [[Wen2023foundationpose - FoundationPose Unified 6D Pose Estimation and Tracking of#^wen2023foundationpose-023]] — The refinement network predicts translation and rotation updates separately, each processed by its own transformer encoder before linear projection.
- [[Wen2023foundationpose - FoundationPose Unified 6D Pose Estimation and Tracking of#^wen2023foundationpose-065]] — At test time, pose refinement runs 5 iterations for pose estimation but a single iteration for tracking.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 5 sources · topic: 6D object pose estimation (drafter's packet `p4-object-pose`, confirmed at the gate)
