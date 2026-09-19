---
aliases: ["YCB-V"]
type: concept
element_type: instrument
topic: "[[6D object pose estimation]]"
topics: ["[[6D object pose estimation]]"]
created: 2026-09-18
---

## Working definition

An RGB-D video dataset of 21 household YCB objects in 92 videos with 6D pose annotations, released with PoseCNN and widely used to evaluate object pose estimators.

## Evidence

- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-028]] — The YCB-Video dataset provides 6D pose annotations of 21 YCB objects in 92 videos with a total of 133,827 frames.
- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-030]] — To avoid annotating every frame, object poses were manually specified only in the first frame of each YCB-Video video.
- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-034]] — The authors state that the 133,827 images make YCB-Video two full orders of magnitude larger than the LINEMOD dataset.
- [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose#^xiang2017posecnn-036]] — PoseCNN is trained on 80 YCB-Video videos and tested on 2,949 key frames extracted from the 12 remaining videos.
- [[Wang2019densefusion - DenseFusion 6D Object Pose Estimation by Iterative Dense#^wang2019densefusion-032]] — The YCB-Video dataset contains 92 RGB-D videos, each showing a subset of 21 YCB objects in different indoor scenes.
- [[Wang2019densefusion - DenseFusion 6D Object Pose Estimation by Iterative Dense#^wang2019densefusion-033]] — Following PoseCNN, the YCB-Video split uses 80 videos for training and 2,949 key frames from 12 remaining videos for testing.
- [[Wang2019densefusion - DenseFusion 6D Object Pose Estimation by Iterative Dense#^wang2019densefusion-034]] — The YCB-Video training set also includes the same 80,000 synthetic images released by the PoseCNN authors.
- [[Wang2019densefusion - DenseFusion 6D Object Pose Estimation by Iterative Dense#^wang2019densefusion-011]] — The authors argue that generic object pose estimation tasks such as YCB-Video demand reasoning over both geometric and appearance information.
- [[Labbe2020cosypose - CosyPose Consistent multi-view multi-object 6D pose#^labbe2020cosypose-034]] — Using the same PoseCNN detections, the single-view method reaches 89.8 AUC of ADD-S on YCB-Video versus 88.1 for DeepIM.
- [[Wen2023foundationpose - FoundationPose Unified 6D Pose Estimation and Tracking of#^wen2023foundationpose-048]] — On YCB-Video model-based pose tracking, the method reaches an all-frames ADD AUC of 96.0 without re-initialization.
- [[Hodan2024bop - BOP Challenge 2023 on Detection, Segmentation and Pose#^hodan2024bop-042]] — On the TUD-L and YCB-V datasets, the authors observe that Task 1 accuracy metrics start to saturate.
- [[Peng2018pvnet - PVNet Pixel-wise Voting Network for 6DoF Pose Estimation#^peng2018pvnet-052]] — On YCB-Video, PVNet reaches 73.4 ADD(-S) AUC, compared with 72.8 for Oberweger and 61.0 for PoseCNN.
- [[Geist2024learning - Learning with 3D rotations, a hitchhiker's guide to SO(3)#^geist2024learning-043]] — The authors hypothesize that quaternions perform well on YCB-Video because the dataset mostly contains small angles.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 7 sources · topic: 6D object pose estimation (drafter's packet `p4-object-pose`, confirmed at the gate)
