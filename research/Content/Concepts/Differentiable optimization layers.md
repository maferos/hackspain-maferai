---
aliases: []
type: concept
element_type: method
topic: "[[Riemannian and Lie-group methods for robot motion and optimization]]"
topics: ["[[Riemannian and Lie-group methods for robot motion and optimization]]"]
created: 2026-09-18
---

## Working definition

A differentiable optimization layer embeds a classical solver step, such as a Gauss-Newton or least-squares update, inside a neural network's computation graph so that gradients can be backpropagated through the solution to train the network end to end.

## Evidence

- [[Teed2021droid - DROID-SLAM Deep Visual SLAM for Monocular, Stereo, and#^teed2021droid-014]] — Each update comes from a differentiable Dense Bundle Adjustment layer that computes a Gauss-Newton step on poses and dense per-pixel depth.
- [[Teed2021droid - DROID-SLAM Deep Visual SLAM for Monocular, Stereo, and#^teed2021droid-026]] — During training, backpropagation is performed through the Dense Bundle Adjustment layer, which is implemented as part of the computation graph.
- [[Teed2021droid - DROID-SLAM Deep Visual SLAM for Monocular, Stereo, and#^teed2021droid-060]] — The authors find the SLAM system unstable and prone to failure when the DBA layer is not used during training.
- [[Teed2021tangent - Tangent Space Backpropagation for 3D Transformation Groups#^teed2021tangent-044]] — A differentiable least squares layer performs 3 Gauss-Newton updates, and the library backpropagates through them to train the network.
- [[Wang2022pypose - PyPose A Library for Robot Learning with Physics-based#^wang2022pypose-005]] — CvxpyLayer treats convex optimization as a differentiable neural network layer but does not support Lie group operations or 2nd-order optimizers.
- [[Wang2022pypose - PyPose A Library for Robot Learning with Physics-based#^wang2022pypose-006]] — Theseus takes non-linear optimization as network layers but adopts rotation matrices, which the authors call memory inefficient for practical robotic applications.
- [[Wang2022pypose - PyPose A Library for Robot Learning with Physics-based#^wang2022pypose-054]] — The planning example maps depth sensor inputs directly into kinodynamically feasible trajectories, using the SE3 LieTensor as a differential optimization layer.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 3 sources · topic: Riemannian and Lie-group methods for robot motion and optimization (drafter's packet `p2-riemannian-robot-motion`, confirmed at the gate)
