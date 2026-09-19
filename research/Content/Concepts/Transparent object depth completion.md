---
aliases: ["Transparent depth completion"]
type: concept
element_type: process
topic: "[[6D object pose estimation]]"
topics: ["[[6D object pose estimation]]"]
created: 2026-09-18
---

## Working definition

Recovering accurate depth for transparent objects, whose refraction and specular reflection leave RGB-D sensor depth missing or wrong, typically by predicting a corrected depth map from the RGB image and the raw depth.

## Evidence

- [[Chen2022clearpose - ClearPose Large-scale Transparent Object Dataset and#^chen2022clearpose-036]] — ImplicitDepth and TransCG serve as depth completion baselines, both trained following their original papers' iterations and hyper-parameters.
- [[Chen2022clearpose - ClearPose Large-scale Transparent Object Dataset and#^chen2022clearpose-038]] — The authors suggest this implies methods using DFNet can outperform designs using voxel-based PointNet for transparent depth completion.
- [[Chen2022clearpose - ClearPose Large-scale Transparent Object Dataset and#^chen2022clearpose-039]] — Both depth completion methods perform poorly in Translucent Cover scenes and achieve their best performance in New Background scenes.
- [[Fang2022transcg - TransCG A Large-Scale Real-World Dataset for Transparent#^fang2022transcg-045]] — Unless specified, all depth completion metrics are calculated on the transparent areas given by the transparent masks.
- [[Fang2022transcg - TransCG A Large-Scale Real-World Dataset for Transparent#^fang2022transcg-055]] — The authors conclude that their real-world dataset is more universal than previous synthetic datasets for training depth completion models.
- [[Fang2022transcg - TransCG A Large-Scale Real-World Dataset for Transparent#^fang2022transcg-034]] — For grasping, the refined depth from DFNet builds a scene point cloud that is passed to GraspNet-baseline for grasp pose detection.
- [[Jiang2023robotic - Robotic Perception of Transparent Objects A Review#^jiang2023robotic-004]] — The authors frame current research as addressing two key problems: locating transparent objects and accurately estimating their depth.
- [[Jiang2023robotic - Robotic Perception of Transparent Objects A Review#^jiang2023robotic-051]] — DREDS is the only dataset providing raw depth data in simulation, enabling sim-to-real transfer for end-to-end depth reconstruction.
- [[Jiang2023robotic - Robotic Perception of Transparent Objects A Review#^jiang2023robotic-046]] — ClearGrasp is the first large-scale depth reconstruction dataset for transparent objects, with 50k synthetic images and 286 real images.
- [[Sajjan2019cleargrasp - ClearGrasp 3D Shape Estimation of Transparent Objects for#^sajjan2019cleargrasp-004]] — The authors conjecture that correcting initial RGB-D depth is more practical, letting depth from non-transparent surfaces inform the depth of transparent surfaces.
- [[Sajjan2019cleargrasp - ClearGrasp 3D Shape Estimation of Transparent Objects for#^sajjan2019cleargrasp-017]] — ClearGrasp adopts the depth completion pipeline of Zhang and Funkhouser, adding a network that predicts pixel-wise masks of transparent surfaces.
- [[Sajjan2019cleargrasp - ClearGrasp 3D Shape Estimation of Transparent Objects for#^sajjan2019cleargrasp-010]] — The authors state that prior depth inference and depth completion works do not explicitly handle transparent objects, whose 3D ground truth is hard to obtain.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 4 sources · topic: 6D object pose estimation (drafter's packet `p4-object-pose`, confirmed at the gate)
