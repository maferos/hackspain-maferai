---
aliases: []
type: concept
element_type: instrument
topic: "[[6D object pose estimation]]"
topics: ["[[6D object pose estimation]]"]
created: 2026-09-18
---

## Working definition

The standard benchmark for model-based 6D object pose estimation, combining real-image datasets in a unified format, symmetry-aware pose-error functions (VSD, MSSD, MSPD) and an online leaderboard run as a series of public challenges.

## Evidence

- [[Hodan2018bop - BOP Benchmark for 6D Object Pose Estimation#^hodan2018bop-004]] — The benchmark provides eight datasets in a unified format, including two new datasets focusing on varying lighting conditions.
- [[Hodan2018bop - BOP Benchmark for 6D Object Pose Estimation#^hodan2018bop-009]] — An online evaluation system at bop.felk.cvut.cz allows continuous submission of new results to the benchmark.
- [[Hodan2024bop - BOP Challenge 2023 on Detection, Segmentation and Pose#^hodan2024bop-001]] — The BOP Challenge 2023 was the fifth in a series of public challenges recording the state of the art in 6D object pose estimation.
- [[Hodan2024bop - BOP Challenge 2023 on Detection, Segmentation and Pose#^hodan2024bop-028]] — BOP includes twelve datasets in a unified format, seven of which were selected as core datasets.
- [[Hodan2024bop - BOP Challenge 2023 on Detection, Segmentation and Pose#^hodan2024bop-029]] — All test images in the BOP datasets are real, while training images may be real or synthetic.
- [[Lin2023sam - SAM-6D Segment Anything Model Meets Zero-Shot 6D Object#^lin2023sam-031]] — Pose estimation is evaluated by mean Average Recall over the VSD, MSSD and MSPD error functions of the BOP benchmark.
- [[Lin2023sam - SAM-6D Segment Anything Model Meets Zero-Shot 6D Object#^lin2023sam-029]] — SAM-6D is evaluated on the seven core BOP datasets: LM-O, T-LESS, TUD-L, IC-BIN, ITODD, HB and YCB-V.
- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-020]] — The seven core BOP datasets used for evaluation exhibit 132 different objects in cluttered scenes with occlusions.
- [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &#^labbe2022megapose-026]] — The full MegaPose coarse plus refiner pipeline reaches a mean BOP AR of 57.2 with RGB-D input.
- [[Wen2023foundationpose - FoundationPose Unified 6D Pose Estimation and Tracking of#^wen2023foundationpose-061]] — At the time of submission, FoundationPose was #1 on the BOP leaderboard for 6D localization of unseen objects.

## Relations

- RELATES_TO → [[Pose ambiguity from symmetry]]
  · type: solves
  · evidence: [[Hodan2018bop - BOP Benchmark for 6D Object Pose Estimation#^hodan2018bop-008]]

## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 5 sources · topic: 6D object pose estimation (drafter's packet `p4-object-pose`, confirmed at the gate)
