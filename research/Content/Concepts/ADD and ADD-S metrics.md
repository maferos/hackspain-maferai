---
aliases: ["ADD(-S)"]
type: concept
element_type: metric
topic: "[[6D object pose estimation]]"
topics: ["[[6D object pose estimation]]"]
created: 2026-09-18
---

## Working definition

Pose-error metrics that average the distance between object model points transformed by the estimated and ground-truth poses, using corresponding points (ADD) or closest points to tolerate symmetric objects (ADD-S).

## Evidence

- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-039]] — Pose accuracy is evaluated with the average distance (ADD) between model points transformed by the ground-truth pose and the estimated pose.
- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-040]] — For symmetric objects, the ADD-S metric computes the average distance using the closest model point instead of the corresponding point.
- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-058]] — With ICP refinement, PoseCNN obtains an ADD area of 17.5 for the bowl on YCB-Video, against 78.3 under the ADD-S metric.
- [[Wang2019densefusion - DenseFusion 6D Object Pose Estimation by Iterative Dense#^wang2019densefusion-036]] — On YCB-Video, the area under the ADD-S curve is reported with a maximum threshold of 0.1m, following PoseCNN.
- [[Wang2019densefusion - DenseFusion 6D Object Pose Estimation by Iterative Dense#^wang2019densefusion-037]] — The percentage of ADD-S below 2cm is reported as the minimum tolerance for robot manipulation with most grippers.
- [[Hodan2018bop - BOP Benchmark for 6D Object Pose Estimation#^hodan2018bop-021]] — Hinterstoisser et al. consider an estimated pose correct if the eADD or eADI error is at most 0.1 times the object diameter.
- [[Hodan2018bop - BOP Benchmark for 6D Object Pose Estimation#^hodan2018bop-022]] — Error eADI can be un-intuitively low because of many-to-one vertex matching established by the search for the closest vertex.
- [[Peng2018pvnet - PVNet Pixel-wise Voting Network for 6DoF Pose Estimation#^peng2018pvnet-034]] — The ADD metric counts a pose correct when the mean transformed model-point distance is less than 10% of the model diameter.
- [[Chen2022clearpose - ClearPose Large-scale Transparent Object Dataset and#^chen2022clearpose-048]] — In the pose benchmark, Accuracy is the percentage of pose estimates on the test set with ADD error less than 10cm.
- [[Labbe2020cosypose - CosyPose Consistent multi-view multi-object 6D pose#^labbe2020cosypose-014]] — The loss enumerates all possible object symmetries to match predicted and ground-truth model vertices instead of finding nearest neighbors as ADD-S does.
- [[Wen2023foundationpose - FoundationPose Unified 6D Pose Estimation and Tracking of#^wen2023foundationpose-054]] — Performance measured by ADD and ADD-S AUC on YCB-Video saturates at 12 reference images for both metrics.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (7 sources) · topic: 6D object pose estimation (drafter's packet `p4-object-pose`, confirmed at the gate)
