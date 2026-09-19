---
aliases: ["Zero-shot 6D object pose estimation"]
type: concept
element_type: concept
topic: "[[6D object pose estimation]]"
topics: ["[[6D object pose estimation]]"]
created: 2026-09-18
---

## Working definition

Estimating the 6D pose of objects never seen during training, given only a CAD model or a few reference images at test time, without per-object retraining.

## Evidence

- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-001]] — MegaPose estimates the 6D pose of novel objects, meaning objects unseen during training, given only a region of interest plus a CAD model.
- [[Lin2023sam - SAM-6D Segment Anything Model Meets Zero-Shot 6D Object#^lin2023sam-001]] — SAM-6D addresses zero-shot 6D object pose estimation, detecting all instances of novel objects unseen during training together with their 6D poses in RGB-D images.
- [[Wen2023foundationpose - FoundationPose Unified 6D Pose Estimation and Tracking of#^wen2023foundationpose-001]] — FoundationPose is a unified framework performing 6D pose estimation and tracking of novel objects in both model-based and model-free setups using RGBD images.
- [[Hodan2024bop - BOP Challenge 2023 on Detection, Segmentation and Pose#^hodan2024bop-002]] — Participants of the 2023 challenge competed on six tasks, three from 2022 and three new variants focused on objects unseen during training.
- [[Hodan2024bop - BOP Challenge 2023 on Detection, Segmentation and Pose#^hodan2024bop-004]] — The authors argue that unseen-object methods are practically relevant because they avoid expensive data generation and training for every new object.
- [[Hodan2024bop - BOP Challenge 2023 on Detection, Segmentation and Pose#^hodan2024bop-051]] — GenFlow-MultiHypo16, the best method for 6D localization of unseen objects, reaches 67.4 ARC on the seven core datasets.
- [[Hodan2024bop - BOP Challenge 2023 on Detection, Segmentation and Pose#^hodan2024bop-057]] — The authors state that run time is a significant challenge for 6D localization of unseen objects.
- [[Wen2023foundationpose - FoundationPose Unified 6D Pose Estimation and Tracking of#^wen2023foundationpose-061]] — At the time of submission, FoundationPose was #1 on the BOP leaderboard for 6D localization of unseen objects.
- [[Lin2023sam - SAM-6D Segment Anything Model Meets Zero-Shot 6D Object#^lin2023sam-064]] — The authors conclude that SAM-6D significantly outperforms existing methods on the seven core BOP datasets for novel-object segmentation and pose estimation.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (4 sources) · topic: 6D object pose estimation (drafter's packet `p4-object-pose`, confirmed at the gate)
