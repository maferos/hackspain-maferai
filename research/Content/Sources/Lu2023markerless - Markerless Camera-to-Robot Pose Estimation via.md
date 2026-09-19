---
aliases: []
type: "source"
title: "Markerless Camera-to-Robot Pose Estimation via Self-supervised Sim-to-Real Transfer"
citekey: "Lu2023markerless"
doi: "10.48550/arXiv.2302.14332"
arxiv: "2302.14332"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2302.14332"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Jingpei Lu", "Florian Richter", "Michael C. Yip"]
sha256: ["3b7dd4dbcd76a0ab47bc47cf702d3c4b21a84eae9b5fbef595796050b457bd4c"]
pdf: "Content/Papers/Lu2023markerless.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Lu2023markerless.pdf]]

> [!abstract] One-sentence summary
> CtRNet estimates the camera-to-robot pose from a single RGB image with a keypoint detector and a differentiable PnP solver, and is transferred from simulation to real robots by self-supervision from foreground segmentation and differentiable rendering, reaching rendering-level accuracy at keypoint-level speed.

## Abstract

Solving the camera-to-robot pose is a fundamental requirement for vision-based robot control, and is a process that takes considerable effort and cares to make accurate. Traditional approaches require modification of the robot via markers, and subsequent deep learning approaches enabled markerless feature extraction. Mainstream deep learning methods only use synthetic data and rely on Domain Randomization to fill the sim-to-real gap, because acquiring the 3D annotation is labor-intensive. In this work, we go beyond the limitation of 3D annotations for real-world data. We propose an end-to-end pose estimation framework that is capable of online camera-to-robot calibration and a self-supervised training method to scale the training to unlabeled real-world data. Our framework combines deep learning and geometric vision for solving the robot pose, and the pipeline is fully differentiable. To train the Camera-to-Robot Pose Estimation Network (CtRNet), we leverage foreground segmentation and differentiable rendering for image-level self-supervision. The pose prediction is visualized through a renderer and the image loss with the input image is back-propagated to train the neural network. Our experimental results on two public real datasets confirm the effectiveness of our approach over existing works. We also integrate our framework into a visual servoing system to demonstrate the promise of real-time precise robot pose estimation for automation tasks. (arXiv)

## 🧠 Key ideas (atomic)

- Marker-based calibration usually requires multiple runs with different robot configurations, after which the robot base and camera are assumed static. (Lu et al., 2023) `ev:asserted` p. 1 ^lu2023markerless-001
- The authors argue that lacking [[Markerless hand-eye calibration|online calibration]] limits vision-based robot control, since minor bumps or repetitive use can throw calibrations off. (Lu et al., 2023) `ev:asserted` p. 1 ^lu2023markerless-002
- Current robot pose estimation approaches are mainly classified into two categories: keypoint-based methods and rendering-based methods. (Lu et al., 2023) `ev:cited` p. 2 ^lu2023markerless-003
- Keypoint-based methods are the most popular approach for robot pose estimation because of their fast inference speed. (Lu et al., 2023) `ev:asserted` p. 2 ^lu2023markerless-004
- Keypoint-based performance is limited by keypoint detectors often trained in simulation, so it is ultimately hampered by the sim-to-real gap. (Lu et al., 2023) `ev:asserted` p. 2 ^lu2023markerless-005
- Rendering-based methods can achieve better performance by using the entire robot shape as observation, which provides dense correspondence. (Lu et al., 2023) `ev:asserted` p. 2 ^lu2023markerless-006
- Because iterative render-and-compare is time- and energy-consuming, rendering-based methods are more suitable for offline estimation with stationary robot and camera. (Lu et al., 2023) `ev:asserted` p. 2 ^lu2023markerless-007
- At inference, CtRNet uses keypoints to obtain the fast inference speed of keypoint-based robot pose estimation methods. (Lu et al., 2023) `ev:asserted` p. 2 ^lu2023markerless-008
- During training, CtRNet leverages the high performance of rendering-based methods to overcome the sim-to-real gap faced by keypoint methods. (Lu et al., 2023) `ev:asserted` p. 2 ^lu2023markerless-009
- The authors leverage foreground segmentation to supervise pose estimation because segmenting the robot is simpler than estimating its pose. (Lu et al., 2023) `ev:asserted` p. 2 ^lu2023markerless-010
- The network is first pretrained on synthetic data, then transferred to the real world by a self-supervised pipeline without manual labels. (Lu et al., 2023) `ev:reported` p. 2 ^lu2023markerless-011
- A differentiable renderer produces a robot silhouette image of the estimated pose, which is compared directly to the segmentation result. (Lu et al., 2023) `ev:reported` p. 2 ^lu2023markerless-012
- Instead of modelling domain distributions as domain adaptation does, the authors perform [[Sim-to-real transfer|sim-to-real transfer]] by directly training on real-world data. (Lu et al., 2023) `ev:asserted` p. 3 ^lu2023markerless-013
- The self-supervised objective minimizes the difference between the rendered silhouette image and the mask image from foreground segmentation. (Lu et al., 2023) `ev:reported` p. 3 ^lu2023markerless-014
- CtRNet's parameters were pretrained with synthetic data, where the keypoint and segmentation labels are obtained freely. (Lu et al., 2023) `ev:reported` p. 3 ^lu2023markerless-015
- During self-training on real data, the segmentation module and the pose module take turns learning from each other. (Lu et al., 2023) `ev:reported` p. 3 ^lu2023markerless-016
- The pose estimation module consists of a keypoint detector and a PnP solver using 2D-3D point correspondences. (Lu et al., 2023) `ev:reported` p. 3 ^lu2023markerless-017
- Robot silhouettes are rendered with the PyTorch3D differentiable renderer, using a silhouette renderer that applies no lighting or shading. (Lu et al., 2023) `ev:reported` p. 3 ^lu2023markerless-018
- The pose module is optimized with an L2 image loss between the rendered silhouette and the predicted robot mask. (Lu et al., 2023) `ev:reported` p. 4 ^lu2023markerless-019
- The L2 loss is chosen because segmentation accuracy for robot pose estimation has been shown to transfer from simulation to reality. (Lu et al., 2023) `ev:cited` p. 4 ^lu2023markerless-020
- Segmentation layers are refined with a weighted binary cross-entropy loss against the rendered image, to avoid noisy training signals. (Lu et al., 2023) `ev:reported` p. 4 ^lu2023markerless-021
- Each training sample is weighted by an exponential of its negative scaled PnP reprojection error, so poorly converged samples count exponentially less. (Lu et al., 2023) `ev:reported` p. 4 ^lu2023markerless-022
- CtRNet uses a ResNet50 backbone, with Atrous Spatial Pyramid Pooling layers producing the segmentation mask at input resolution. (Lu et al., 2023) `ev:reported` p. 5 ^lu2023markerless-023
- The keypoint detector, sharing the segmentation backbone, applies a spatial softmax on heatmaps to compute expected 2D keypoint locations. (Lu et al., 2023) `ev:reported` p. 5 ^lu2023markerless-024
- Gradients through the PnP solver are obtained by implicit differentiation, applying the implicit function theorem to its stationarity condition. (Lu et al., 2023) `ev:reported` p. 5 ^lu2023markerless-025
- The DREAM-real dataset contains around 50K RGB images of a Franka Emika Panda arm recorded with 3 different cameras. (Lu et al., 2023) `ev:reported` p. 5 ^lu2023markerless-026
- Pose accuracy is evaluated with the average distance (ADD) metric, alongside the area-under-the-curve (AUC) over ADD thresholds. (Lu et al., 2023) `ev:reported` p. 5 ^lu2023markerless-027
- The Baxter dataset contains 100 RGB images of a Rethink Baxter left arm captured with an Azure Kinect camera. (Lu et al., 2023) `ev:reported` p. 6 ^lu2023markerless-028
- Pretraining on synthetic data runs for 1000 epochs at a 1e-5 learning rate with the Adam optimizer. (Lu et al., 2023) `ev:reported` p. 6 ^lu2023markerless-029
- Self-supervised training on real-world data runs for 500 epochs at a 1e-6 learning rate, with gradients clipped at 10. (Lu et al., 2023) `ev:reported` p. 6 ^lu2023markerless-030
- On DREAM-real, CtRNet was trained at (320×240) resolution, with keypoints scaled up by a factor of 2 for evaluation. (Lu et al., 2023) `ev:reported` p. 6 ^lu2023markerless-031
- Overall on DREAM-real, CtRNet reaches 85.962 AUC, compared with 80.094 for RoboPose and 68.584 for DREAM-H. (Lu et al., 2023) `ev:measured` p. 6 ^lu2023markerless-032
- Overall on DREAM-real, CtRNet and RoboPose both obtain a mean ADD of 0.020 metres, as reported in Table 1. (Lu et al., 2023) `ev:measured` p. 6 ^lu2023markerless-033
- CtRNet reaches 89.928 AUC on Panda 3CAM-AK in Table 1, above RoboPose's 76.497 on that camera. (Lu et al., 2023) `ev:measured` p. 6 ^lu2023markerless-034
- On the Panda 3CAM-XK camera, the rendering-based RoboPose outperforms CtRNet, with 85.926 AUC against 79.465. (Lu et al., 2023) `ev:measured` p. 6 ^lu2023markerless-035
- For the Baxter comparison, the authors implemented a differentiable-rendering baseline whose robot masks come from the pretrained foreground segmentation. (Lu et al., 2023) `ev:reported` p. 6 ^lu2023markerless-036
- On Baxter, the differentiable-rendering baseline reaches 81.15 ADD AUC, against 83.93 for CtRNet and 40.63 for DREAM-Q. (Lu et al., 2023) `ev:measured` p. 6 ^lu2023markerless-037
- On Baxter, Aruco Marker calibration gives a mean 3D error of 2447.34 mm in Table 2. (Lu et al., 2023) `ev:measured` p. 6 ^lu2023markerless-038
- On the Baxter dataset, CtRNet outperforms all other compared methods on both 2D and 3D evaluations. (Lu et al., 2023) `ev:measured` p. 7 ^lu2023markerless-039
- On Baxter 2D evaluation, CtRNet achieves 93.94 AUC for PCK with an average reprojection error of 11.62 pixels. (Lu et al., 2023) `ev:measured` p. 7 ^lu2023markerless-040
- On Baxter 3D evaluation, CtRNet achieves 83.93 AUC for ADD with an average ADD of 63.81mm. (Lu et al., 2023) `ev:measured` p. 7 ^lu2023markerless-041
- On Baxter, 99 percent of CtRNet estimates have under 50 pixel reprojection error, less than 2 percent of the image resolution. (Lu et al., 2023) `ev:measured` p. 7 ^lu2023markerless-042
- On Baxter, 88 percent of CtRNet estimates localize the end-effector with less than 100mm distance error. (Lu et al., 2023) `ev:measured` p. 7 ^lu2023markerless-043
- The ablation pretrains with 500, 1000, 2000, 4000 or 8000 synthetic samples before self-supervised training on Baxter. (Lu et al., 2023) `ev:reported` p. 7 ^lu2023markerless-044
- Doubling the pretraining dataset size significantly improves convergence of the self-training process at the beginning, in the Baxter ablation. (Lu et al., 2023) `ev:measured` p. 7 ^lu2023markerless-045
- For the Baxter dataset, the convergence improvement saturates after having more than 2000 pretraining samples. (Lu et al., 2023) `ev:measured` p. 7 ^lu2023markerless-046
- The Baxter dataset used in the ablation captures 20 different robot poses from a fixed camera position. (Lu et al., 2023) `ev:reported` p. 7 ^lu2023markerless-047
- The authors suggest the required number of pretraining samples might vary according to the complexity of the environment. (Lu et al., 2023) `ev:asserted` p. 7 ^lu2023markerless-048
- With 500 pretraining samples, mean ADD on Baxter is 2167.30 mm, against 63.81 mm with 8000 samples. (Lu et al., 2023) `ev:measured` p. 8 ^lu2023markerless-049
- In Table 3, AUC ADD rises from 47.62 with 500 pretraining samples to 82.98 with 2000 samples. (Lu et al., 2023) `ev:measured` p. 8 ^lu2023markerless-050
- The visual servoing experiment runs on a Baxter robot, with [[Position-based visual servoing|PBVS]] based purely on RGB images from a single camera. (Lu et al., 2023) `ev:reported` p. 8 ^lu2023markerless-051
- In [[Visual servoing|visual servoing]], CtRNet achieves 0.002m averaged translational error on the end-effector at a 30Hz loop rate. (Lu et al., 2023) `ev:measured` p. 8 ^lu2023markerless-052
- In the visual servoing trials, CtRNet achieves 0.002rad averaged rotational error on the robot end-effector. (Lu et al., 2023) `ev:measured` p. 8 ^lu2023markerless-053
- In visual servoing, DREAM yields a 0.235 mean translational error in metres, compared with 0.046 for differentiable rendering. (Lu et al., 2023) `ev:measured` p. 8 ^lu2023markerless-054
- In one selected trial, the servoing system could not converge with DREAM because poor pose estimation gave an unreachable target pose. (Lu et al., 2023) `ev:measured` p. 8 ^lu2023markerless-055
- With the differentiable renderer, the servoing system takes more than 10 seconds to converge in the selected trial. (Lu et al., 2023) `ev:measured` p. 8 ^lu2023markerless-056
- With CtRNet, the servoing system converges much faster, in ≤5 seconds, during the selected trial. (Lu et al., 2023) `ev:measured` p. 8 ^lu2023markerless-057
- The authors conclude that CtRNet achieves state-of-the-art robot pose estimation performance while maintaining high-speed inference. (Lu et al., 2023) `ev:asserted` p. 8 ^lu2023markerless-058
- For future work, the authors would like to explore vision-based robot control in an unstructured environment. (Lu et al., 2023) `ev:asserted` p. 8 ^lu2023markerless-059
- Synthetic data store only robot pose and configuration pairs, with mask and keypoint labels generated on-the-fly during training. (Lu et al., 2023) `ev:reported` p. 12 ^lu2023markerless-060
- Synthetic images randomize joint configuration, camera position, scene lights, virtual object positions, backgrounds, and robot mesh colour. (Lu et al., 2023) `ev:reported` p. 12 ^lu2023markerless-061
- Qualitatively on DREAM-real, the robot mask shows enhanced quality after self-supervised training, preserving fine corner and boundary details. (Lu et al., 2023) `ev:measured` p. 12 ^lu2023markerless-062
- The authors believe the high-quality segmentation mask is the key to their state-of-the-art pose estimation performance. (Lu et al., 2023) `ev:asserted` p. 12 ^lu2023markerless-063
- Training with the segmentation loss consistently yields better Baxter pose estimation by a considerable margin, given enough pretraining samples. (Lu et al., 2023) `ev:measured` p. 13 ^lu2023markerless-064
- With 500 pretraining samples, CtRNet without segmentation loss reaches 65.26 AUC ADD, against 47.62 with it. (Lu et al., 2023) `ev:measured` p. 14 ^lu2023markerless-065
- The authors attribute the low-sample advantage to segmentation layers not being affected by many inaccurately detected keypoints. (Lu et al., 2023) `ev:asserted` p. 14 ^lu2023markerless-066
- When robot parts lie outside the camera frustum, keypoint detection produces false positives that undermine robot pose estimation. (Lu et al., 2023) `ev:asserted` p. 14 ^lu2023markerless-067
- The authors suggest the PnP reprojection error can be used during inference to indicate pose estimation confidence. (Lu et al., 2023) `ev:asserted` p. 14 ^lu2023markerless-068

## 🎯 Contributions


## 📖 Glossary

- **Camera-to-robot pose** — the 6-DOF transform between the camera frame and the robot base frame.
- **PBVS** — position-based visual servoing: control driven by 3D poses inferred from images.
- **PnP** — Perspective-n-Point: solving camera pose from 2D-3D point correspondences.
- **ADD** — average distance between points transformed by estimated and ground-truth poses.
- **PCK** — percentage of correct keypoints within a pixel threshold.
- **Differentiable rendering** — rendering whose output gradients flow back to pose or shape parameters.
- **Spatial softmax** — operator returning the expected 2D location of maximal activation per heatmap channel.
- **Domain Randomization** — randomizing simulation parameters so real data falls within training variation.

## ❓ Open questions

- How well does the self-supervised transfer work when the camera moves across many viewpoints, since the Baxter set has 20 poses from one fixed camera?
- Can the method handle robots partially outside the camera frustum without false-positive keypoints?
- How does CtRNet perform on robots beyond the Panda and Baxter, given separate networks are trained per robot?
- Why does the w/ Lseg model collapse to 2167.30 mm mean ADD with 500 pretraining samples while w/o Lseg stays at 184.45 mm?
- Would the approach hold in unstructured environments with clutter and occlusion of the robot?

## 📝 Notes on reading

- Read the arXiv v2 preprint (21 Mar 2023), which includes supplementary material on pages 12-14.
- Figure 1 (p. 1) plots speed versus normalized AUC for Aruco, DREAM variants, Opt. Keypoints, RoboPose, Diff. Rendering and CtRNet; only described, not claimed.
- Figures 4, 6, 7 and 9 are qualitative or plots; Figure 5 plots self-training loss versus epochs per pretraining size.
- Table 2 reports PCK@50 pixel as 0.99 and ADD@100 mm as 0.88 (fractions), which the text restates as 99 and 88 percent.
- The main-text ablation says improvement saturates after 2000 pretraining samples; the supplementary segmentation-loss ablation says after 4000.
- The overall DREAM comparison in text (+17.378 AUC, -17.457 error) matches the DREAM-H row of Table 1, though the text says only DREAM.
- Eq. (10) writes O(Tc_b, p, K, Tc_b), apparently a typo for O(o, p, K, Tc_b).
- Table 1 extraction of some DREAM rows is split across lines but the values are readable.

## Suggested new concepts

- Self-supervised sim-to-real transfer — training on unlabeled real data with rendering-based image losses, an alternative to domain randomization.
- Differentiable PnP via implicit differentiation — lets keypoint detectors train end-to-end through a geometric solver.
- Markerless hand-eye calibration — online camera-to-robot pose estimation without fiducials, relevant to camera-based lab automation.
- Position-based visual servoing — control paradigm that depends directly on camera-to-robot pose quality.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H5.** CtRNet estima el extrínseco cámara-robot sin marcadores con keypoints y PnP, autosupervisado con renderizado diferenciable de siluetas.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
