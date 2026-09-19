---
aliases: []
type: "source"
title: "Differentiable Robot Rendering"
citekey: "Liu2024differentiable"
doi: "10.48550/arXiv.2410.13851"
arxiv: "2410.13851"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2410.13851"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Ruoshi Liu", "Alper Canberk", "Shuran Song", "Carl Vondrick"]
sha256: ["ff4671121e2052dfb5a5eb2a11362a96ac9daaaf175af6be4ddffbcb73df20c6"]
pdf: "Content/Papers/Liu2024differentiable.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Liu2024differentiable.pdf]]

> [!abstract] One-sentence summary
> Dr. Robot combines forward kinematics, implicit linear blend skinning and pose-conditioned Gaussian Splatting into a robot model differentiable from pixels to joint angles, enabling single-image pose reconstruction and control driven by vision foundation models (CLIP, video diffusion, point trackers).

## Abstract

Vision foundation models trained on massive amounts of visual data have shown unprecedented reasoning and planning skills in open-world settings. A key challenge in applying them to robotic tasks is the modality gap between visual data and action data. We introduce differentiable robot rendering, a method allowing the visual appearance of a robot body to be directly differentiable with respect to its control parameters. Our model integrates a kinematics-aware deformable model and Gaussians Splatting and is compatible with any robot form factors and degrees of freedom. We demonstrate its capability and usage in applications including reconstruction of robot poses from images and controlling robots through vision language models. Quantitative and qualitative results show that our differentiable rendering model provides effective gradients for robotic control directly from pixels, setting the foundation for the future applications of vision foundation models in robotics. (arXiv)

## 🧠 Key ideas (atomic)

- Dr. Robot is a robot self-model based on Gaussian Splatting that is fully differentiable from visual appearance to control parameters (Liu et al., 2024) `ev:asserted` p. 1 ^liu2024differentiable-001
- The authors argue a differentiable self-model lets visual rewards be optimized with gradients instead of evolutionary algorithms or reinforcement learning (Liu et al., 2024) `ev:asserted` p. 2 ^liu2024differentiable-002
- The paper cites growing evidence that visual foundation models can provide robust and generalizable signals for robot control (Liu et al., 2024) `ev:cited` p. 2 ^liu2024differentiable-003
- The authors state that a differentiable robot rendering model needs three properties: full-body differentiability, deformability, and efficiency in rendering (Liu et al., 2024) `ev:asserted` p. 2 ^liu2024differentiable-004
- The robot image is modelled as a pinhole-camera projection of a differentiable function of the robot pose (Liu et al., 2024) `ev:asserted` p. 2 ^liu2024differentiable-005
- Dr. Robot models the robot's appearance in its canonical pose with Gaussian Splatting, rendered from a given viewpoint by a differentiable rasterizer (Liu et al., 2024) `ev:asserted` p. 2 ^liu2024differentiable-006
- Forward kinematics represents each joint's pose relative to the base joint as a product of rigid transformations along the kinematic chain (Liu et al., 2024) `ev:asserted` p. 2 ^liu2024differentiable-007
- The method adapts Linear Blend Skinning to 3D Gaussians, projecting Gaussian positions to targets conditioned on a pose via differentiable forward kinematics (Liu et al., 2024) `ev:asserted` p. 2 ^liu2024differentiable-008
- A pose-conditioned appearance deformation model changes the spherical harmonics, scale, opacity, covariance of the 3D Gaussians given a pose (Liu et al., 2024) `ev:asserted` p. 2 ^liu2024differentiable-009
- Each canonical Gaussian carries 27-dimensional spherical harmonics coefficients plus an opacity to represent its appearance during rendering (Liu et al., 2024) `ev:reported` p. 3 ^liu2024differentiable-010
- During optimization, each Gaussian can split into two after every N steps to densify the represented volume (Liu et al., 2024) `ev:reported` p. 3 ^liu2024differentiable-011
- In the canonical model, Gaussians with low opacity are truncated during optimization to reduce memory consumption (Liu et al., 2024) `ev:reported` p. 3 ^liu2024differentiable-012
- Following SMPL, the model learns linear blend skinning to represent geometric deformations of the robot across poses (Liu et al., 2024) `ev:reported` p. 3 ^liu2024differentiable-013
- The authors state that Gaussian splitting with truncation makes classical LBS incompatible, since classical LBS assumes a fixed vertex set (Liu et al., 2024) `ev:asserted` p. 3 ^liu2024differentiable-014
- Implicit LBS maps an arbitrary 3D coordinate to weights giving the influence of each of the J joint transforms (Liu et al., 2024) `ev:asserted` p. 3 ^liu2024differentiable-015
- An implicit appearance deformation function predicts changes in each Gaussian's rotation, scaling, opacity, spherical harmonics given the pose (Liu et al., 2024) `ev:asserted` p. 3 ^liu2024differentiable-016
- The implicit LBS function shares the same MLP architecture as the appearance deformation function, except for input and output dimensions (Liu et al., 2024) `ev:reported` p. 3 ^liu2024differentiable-017
- The full robot model is learned by minimizing mean-squared error between rendered predictions and observed images from given camera viewpoints (Liu et al., 2024) `ev:reported` p. 4 ^liu2024differentiable-018
- At test time, robot actions can be planned by optimizing them through image gradients of objectives such as foundation-model visual rewards (Liu et al., 2024) `ev:asserted` p. 4 ^liu2024differentiable-019
- Training data were rendered in MuJoCo from the robot URDF, covering 10k poses each captured from 12 viewpoints (Liu et al., 2024) `ev:reported` p. 4 ^liu2024differentiable-020
- Appearance was evaluated by PSNR against ground truth, geometry by Chamfer distance between posed Gaussian positions and ground-truth pointclouds (Liu et al., 2024) `ev:reported` p. 4 ^liu2024differentiable-021
- Baselines were Deformable Gaussians, nearest-neighbour retrieval over 1000 samples, a random training sample, plus a no-deform ablation (Liu et al., 2024) `ev:reported` p. 4 ^liu2024differentiable-022
- Using LBS as a prior for geometric deformation had a significant positive impact on fidelity compared with the K-plane-based Deformable Gaussians (Liu et al., 2024) `ev:measured` p. 4 ^liu2024differentiable-023
- The fidelity gap over Deformable Gaussians is described as particularly notable for long robot arms with many chained joints, such as the Panda Arm (Liu et al., 2024) `ev:measured` p. 4 ^liu2024differentiable-024
- Dr. Robot's PSNR ranged from 27.77 on Unitree H1 to 33.25 on xArm7 across the ten robots in Table 1 (Liu et al., 2024) `ev:measured` p. 5 ^liu2024differentiable-025
- On Franka Panda, Dr. Robot scored a PSNR of 32.84, against 27.09 without appearance deformation, 16.52 for K-plane (Liu et al., 2024) `ev:measured` p. 5 ^liu2024differentiable-026
- The no-deform ablation had lower PSNR than the full model on all ten robots, for example 29.75 versus 31.44 on Shadow Hand (Liu et al., 2024) `ev:measured` p. 5 ^liu2024differentiable-027
- Dr. Robot's Chamfer distance ranged from 0.052 on Shadow Hand to 0.399 on Google Robot in Table 1 (Liu et al., 2024) `ev:measured` p. 5 ^liu2024differentiable-028
- On UR5 the no-deform ablation had a lower Chamfer distance, 0.104, than the full model at 0.207 (Liu et al., 2024) `ev:measured` p. 5 ^liu2024differentiable-029
- Robot pose estimation jointly optimizes robot pose with camera pose from one monocular RGB image by minimizing image reconstruction error (Liu et al., 2024) `ev:reported` p. 5 ^liu2024differentiable-030
- Pose reconstruction was evaluated on Panda-3CAM, around 10K images with corresponding robot poses, using L1 joint-angle error (Liu et al., 2024) `ev:reported` p. 5 ^liu2024differentiable-031
- Optimization started from scratch on each video's first frame, warm-starting later frames from the previous frame's joint with camera poses (Liu et al., 2024) `ev:reported` p. 5 ^liu2024differentiable-032
- The baseline Robopose refines joint angles with a network comparing the image to a rendering from the robot CAD model (Liu et al., 2024) `ev:cited` p. 5 ^liu2024differentiable-033
- On single-image robot pose reconstruction, Dr. Robot outperformed the previous state-of-the-art method, Robopose, by 32.9% according to the authors (Liu et al., 2024) `ev:measured` p. 5 ^liu2024differentiable-034
- The method performed consistently better than Robopose across three camera platforms with different fields of view and mounting positions (Liu et al., 2024) `ev:measured` p. 5 ^liu2024differentiable-035
- On Panda-3cam Azure, the joint-angle error was 9.33 for Dr. Robot versus 16.8 for Robopose (Liu et al., 2024) `ev:measured` p. 6 ^liu2024differentiable-036
- On the Panda-3cam Kinect360 sequence, Dr. Robot's reported joint-angle error was 12.52 compared with 14.37 for Robopose (Liu et al., 2024) `ev:measured` p. 6 ^liu2024differentiable-037
- On Panda-3cam Realsense, Dr. Robot's error was 17.83 with standard deviation 5.5, against 24.57 with 3.71 for Robopose (Liu et al., 2024) `ev:measured` p. 6 ^liu2024differentiable-038
- The authors report the reconstruction can recover gripper poses when visible, which they describe as challenging for prior works (Liu et al., 2024) `ev:measured` p. 5 ^liu2024differentiable-039
- The method also permits reconstruction with known camera or robot parameters, or using multiple views at once (Liu et al., 2024) `ev:asserted` p. 5 ^liu2024differentiable-040
- Optimizing Shadow Hand joint angles with CLIP gradients alone produced semantically meaningful hand poses matching given language prompts (Liu et al., 2024) `ev:measured` p. 6 ^liu2024differentiable-041
- The CLIP-guided optimization of hand gestures operated in the 24-dimensional action space of the Shadow Hand robot (Liu et al., 2024) `ev:reported` p. 6 ^liu2024differentiable-042
- For text-to-pose optimization, the authors used openai/clip-vit-base-patch32 from Huggingface as the CLIP model scoring image-text similarity (Liu et al., 2024) `ev:reported` p. 14 ^liu2024differentiable-043
- The authors conclude Dr. Robot can connect directly with off-the-shelf large-scale vision-language models through image gradients (Liu et al., 2024) `ev:asserted` p. 6 ^liu2024differentiable-044
- The paper cites recent work using generative video models for robot planning, which trains separate inverse dynamics models (Liu et al., 2024) `ev:cited` p. 6 ^liu2024differentiable-045
- The authors argue Dr. Robot's reconstruction ability makes it a drag-and-drop replacement for an inverse dynamics model in video planning (Liu et al., 2024) `ev:asserted` p. 6 ^liu2024differentiable-046
- Stable Video Diffusion was fine-tuned on 100 episodes from the ASU Table Top dataset conditioned on language prompt embeddings (Liu et al., 2024) `ev:reported` p. 7 ^liu2024differentiable-047
- Robot actions were recovered from videos generated for novel language prompts by optimizing the reconstruction loss of Section 3.2 (Liu et al., 2024) `ev:reported` p. 7 ^liu2024differentiable-048
- The video model, SVD-XT, was fine-tuned on 256x256 videos at 10fps, taking 12 hours on 2 A100 GPUs (Liu et al., 2024) `ev:reported` p. 14 ^liu2024differentiable-049
- To condition SVD-XT on language, the authors replaced its OpenCLIP laion2b_s32b_b79k image embeddings with text embeddings from the same model (Liu et al., 2024) `ev:reported` p. 14 ^liu2024differentiable-050
- Initial images with prompts for the shown generated videos came from 12 validation episodes not seen during training (Liu et al., 2024) `ev:reported` p. 14 ^liu2024differentiable-051
- Motion retargeting is performed by matching keypoint trajectories from a video point tracker instead of estimating kinematic structure correspondences (Liu et al., 2024) `ev:asserted` p. 7 ^liu2024differentiable-052
- The retargeting loss sums per-timestep Chamfer distances between tracked robot points with goal points, since the points lack correspondence (Liu et al., 2024) `ev:reported` p. 7 ^liu2024differentiable-053
- Gradients from point-track Chamfer distances were back-propagated through tracker, image, robot model to optimize 24/37-dimensional control parameters (Liu et al., 2024) `ev:measured` p. 7 ^liu2024differentiable-054
- Canonical Gaussians are initialized from 10,000 points sampled uniformly on the robot mesh, then trained 2,000 steps with L1 loss (Liu et al., 2024) `ev:reported` p. 14 ^liu2024differentiable-055
- Full training takes 15-30 minutes on a single NVIDIA 3090 GPU depending on the robot embodiment (Liu et al., 2024) `ev:reported` p. 14 ^liu2024differentiable-056
- The implicit skinning module with the appearance deformation module are 4-layer MLPs of 256 hidden dimensions using Fourier-feature coordinate encodings (Liu et al., 2024) `ev:reported` p. 14 ^liu2024differentiable-057
- The robot model is not designed to adapt to environmental lighting effects such as low-light conditions (Liu et al., 2024) `ev:asserted` p. 8 ^liu2024differentiable-058
- The authors note the lighting gap between real and rendered robot could lead to noisy gradients (Liu et al., 2024) `ev:asserted` p. 8 ^liu2024differentiable-059
- Test-time fine-tuning of the Gaussian model to minimize the real-rendered gap is proposed as a promising future direction (Liu et al., 2024) `ev:asserted` p. 8 ^liu2024differentiable-060
- Future work could connect the rendering framework with Gaussian-Splatting-based differentiable physics to model robot-environment interaction differentiably (Liu et al., 2024) `ev:asserted` p. 8 ^liu2024differentiable-061
- The authors conclude that experiments confirm the model provides efficient and effective gradients for controlling robots directly from pixel data (Liu et al., 2024) `ev:asserted` p. 9 ^liu2024differentiable-062
- The authors believe Dr. Robot will bridge increasingly capable text-to-image and text-to-video models with robotic control (Liu et al., 2024) `ev:asserted` p. 2 ^liu2024differentiable-063

## 🎯 Contributions

## 📖 Glossary

- **Gaussian Splatting** — Scene representation of 3D Gaussians rendered by a fast differentiable rasterizer.
- **Linear Blend Skinning (LBS)** — Deforms points as weighted combinations of joint transforms along a skeleton.
- **Implicit LBS** — Neural function mapping any 3D point to per-joint skinning weights.
- **Forward kinematics** — Computing link poses from joint angles via chained rigid transforms.
- **Chamfer distance** — Symmetric nearest-neighbour distance between two unordered point sets.
- **PSNR** — Peak signal-to-noise ratio; higher means rendered image closer to ground truth.
- **Test-time optimization** — Solving for actions by gradient descent at inference, without extra training.
- **Motion retargeting** — Transferring motion from one embodiment to another.

## ❓ Open questions

- How much does the real-to-rendered gap (lighting, background, occlusion) degrade gradient quality on real robots outside Panda-3CAM?
- Are robot actions recovered from generated videos physically executable, and how often do they succeed when run on hardware?
- Why does the no-deform ablation beat the full model on UR5 Chamfer distance, and does appearance deformation ever hurt geometry?
- Can the model be trained from real images rather than MuJoCo renders from the URDF?
- How does the approach scale to contact-rich tasks once differentiable physics is added?

## 📝 Notes on reading

Version read: arXiv v1 (2410.13851v1, 17 Oct 2024), matching the identifier.

Inconsistencies inside the paper: the text names the Table 1 baseline Deformable Gaussians [9], but the table row is labelled K-plane, and reference [9] is titled 4D Gaussian Splatting. Table 1 also carries a Nearest Neighbor (prev) row that the baseline description does not explain. The 32.9% improvement over Robopose is not traced to a specific average of the Table 2 values; units of the Table 2 errors (degrees assumed) are not stated. Appendix A.1 writes LRS where the main text says LBS; p. 2 writes Gaussian splitting for splatting. Appendix A.2 says the CLIP dot product is minimized, while Sec. 3.3.1 describes maximizing CLIP similarity; Eq. 9 also writes min over a similarity. The Table 1 K-plane Chamfer values for Unitree G1 and Unitree GO1 are both 95.880, possibly a copy error.

Figures described only: Fig. 1 overview; Fig. 3 qualitative comparison with Deformable Gaussians; Fig. 4 pose overlays on Realsense, Kinect 360, Azure images; Fig. 5 CLIP optimization steps for Shadow Hand gestures; Fig. 6 recovered joint vectors for pick-up prompts (the page-7 numeric joint arrays are figure text and were not claimed); Fig. 7 point-tracker retargeting.

## Suggested new concepts

- Differentiable robot rendering — a distinct interface linking pixel-space objectives to joint-space control that other robot-vision papers may reuse.
- Implicit linear blend skinning for Gaussians — a general technique for articulating Gaussian Splatting assets with changing point sets.
- Video models as planners with inverse dynamics — recurring pattern where generated videos are converted to actions.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H5.** Modelo Gaussian Splatting del robot diferenciable respecto a sus parámetros de control, útil para recuperar pose y calibrar desde píxeles.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
