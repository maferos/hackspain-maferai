---
aliases: []
type: "source"
title: "KeyPose: Multi-View 3D Labeling and Keypoint Estimation for Transparent Objects"
citekey: "Liu2019keypose"
doi: "10.48550/arXiv.1912.02805"
arxiv: "1912.02805"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1912.02805"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Xingyu Liu", "Rico Jonschkowski", "Anelia Angelova", "Kurt Konolige"]
sha256: ["8cc603278f6fa80b8a358f1ff9df48493c9e1dbd5715bdca858900d61e8d0dbc"]
pdf: "Content/Papers/Liu2019keypose.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Liu2019keypose.pdf]]

> [!abstract] One-sentence summary
> KeyPose builds a robot-assisted multi-view pipeline to label 3D keypoints on transparent objects (the 48k-image TOD dataset) and a stereo-RGB network that predicts those keypoints without a depth sensor, beating a depth-based DenseFusion baseline even when it is given opaque depth.

## Abstract

Estimating the 3D pose of desktop objects is crucial for applications such as robotic manipulation. Many existing approaches to this problem require a depth map of the object for both training and prediction, which restricts them to opaque, lambertian objects that produce good returns in an RGBD sensor. In this paper we forgo using a depth sensor in favor of raw stereo input. We address two problems: first, we establish an easy method for capturing and labeling 3D keypoints on desktop objects with an RGB camera; and second, we develop a deep neural network, called $KeyPose$, that learns to accurately predict object poses using 3D keypoints, from stereo input, and works even for transparent objects. To evaluate the performance of our method, we create a dataset of 15 clear objects in five classes, with 48K 3D-keypoint labeled images. We train both instance and category models, and show generalization to new textures, poses, and objects. KeyPose surpasses state-of-the-art performance in 3D pose estimation on this dataset by factors of 1.5 to 3.5, even in cases where the competing method is provided with ground-truth depth. Stereo input is essential for this performance as it improves results compared to using monocular input by a factor of 2. We will release a public version of the data capture and labeling pipeline, the transparent object database, and the KeyPose models and evaluation code. Project website: https://sites.google.com/corp/view/keypose. (arXiv)

## 🧠 Key ideas (atomic)

- Depth sensing fails for transparent or shiny metallic objects, which violate the opaque lambertian surface assumption of commercial depth sensors (Liu et al., 2019) `ev:asserted` p. 1 ^liu2019keypose-001
- An Azure Kinect sensor returned reasonable depth for an opaque bottle but invalid depth values for its transparent twin (Liu et al., 2019) `ev:measured` p. 1 ^liu2019keypose-002
- The authors present what they call the first method of keypoint-based pose estimation for transparent 3D objects from stereo RGB images (Liu et al., 2019) `ev:asserted` p. 1 ^liu2019keypose-003
- Existing datasets such as LabelFusion, YCB and REAL275 annotate monocular RGBD images of opaque objects rather than stereo images of transparent ones (Liu et al., 2019) `ev:cited` p. 2 ^liu2019keypose-004
- Existing pose datasets require accurate depth and an object CAD model so that alignment algorithms such as iterative closest point apply (Liu et al., 2019) `ev:cited` p. 2 ^liu2019keypose-005
- Following their capture and labeling method, the authors built TOD, a dataset of 48k images from 15 transparent object instances (Liu et al., 2019) `ev:reported` p. 2 ^liu2019keypose-006
- KeyPose predicts 3D keypoints on transparent objects from cropped stereo RGB input, with crops assumed to come from a loose detection stage (Liu et al., 2019) `ev:reported` p. 2 ^liu2019keypose-007
- The authors' method does not assume object rigidity or require a 3D CAD model of each individual object (Liu et al., 2019) `ev:asserted` p. 2 ^liu2019keypose-008
- Hand-labeling 3D keypoints in individual RGB images is described as difficult or impossible due to uncertainty about keypoint depth (Liu et al., 2019) `ev:asserted` p. 3 ^liu2019keypose-009
- A robot arm moves a calibrated stereo camera around the object while AprilTags on a planar form give the camera pose (Liu et al., 2019) `ev:reported` p. 3 ^liu2019keypose-010
- 2D keypoints labeled on a small subset of widely separated views are optimized into 3D positions and reprojected to all images (Liu et al., 2019) `ev:reported` p. 3 ^liu2019keypose-011
- The authors report they can collect and label data for a new object in a few hours (Liu et al., 2019) `ev:reported` p. 3 ^liu2019keypose-012
- A painted opaque twin replaces each transparent object in a second scan to capture registered opaque depth for comparison with depth methods (Liu et al., 2019) `ev:reported` p. 3 ^liu2019keypose-013
- A farthest-point algorithm on camera poses selects annotated images with large baselines to reduce the effect of human 2D labeling error (Liu et al., 2019) `ev:reported` p. 3 ^liu2019keypose-014
- A Monte Carlo simulation based on reprojection errors estimated the random error of labeled 3D keypoints at around 3.4 mm RMSE (Liu et al., 2019) `ev:computed` p. 4 ^liu2019keypose-015
- Crops of 180×120 pixels are taken, with the right crop offset horizontally by 30 pixels to limit rectangle extension (Liu et al., 2019) `ev:reported` p. 4 ^liu2019keypose-016
- The authors state that comparing 3D errors directly introduces a large bias, as these errors grow quadratically with distance (Liu et al., 2019) `ev:asserted` p. 4 ^liu2019keypose-017
- Geometric augmentation is limited to transformations preserving epipolar constraints, namely scaling, Y-axis shear, mirroring and rotation around the X-axis (Liu et al., 2019) `ev:reported` p. 4 ^liu2019keypose-018
- The KeyPose early fusion model stacks the stereo images and feeds them to exponentially dilated 3x3 convolutions that keep resolution constant (Liu et al., 2019) `ev:reported` p. 4 ^liu2019keypose-019
- The number of features stays constant at 48 for instance models and 64 for category models throughout the CNN blocks (Liu et al., 2019) `ev:reported` p. 4 ^liu2019keypose-020
- A late fusion variant uses siamese dilated CNN blocks to predict left and right UV keypoints separately before stereo geometry gives 3D (Liu et al., 2019) `ev:reported` p. 5 ^liu2019keypose-021
- The total loss sums a keypoint UVD loss, a projection loss weighted by α, and a locality loss weighted 0.001 (Liu et al., 2019) `ev:reported` p. 5 ^liu2019keypose-022
- The projection loss weight α ramps from 0 to 2.5 between 1/3 and 2/3 of the training steps for stability (Liu et al., 2019) `ev:reported` p. 5 ^liu2019keypose-023
- For symmetric objects, the total loss is evaluated over allowed keypoint id permutations and the minimum is taken as the final loss (Liu et al., 2019) `ev:reported` p. 5 ^liu2019keypose-024
- KeyPose was trained with a batch size of 32 for a constant number of steps, around 300 epochs (Liu et al., 2019) `ev:reported` p. 6 ^liu2019keypose-025
- The DenseFusion baseline was re-implemented in TensorFlow with added layers regressing 3D positions for each keypoint (Liu et al., 2019) `ev:reported` p. 6 ^liu2019keypose-026
- The authors prefer 3D keypoint Mean Absolute Error over AUC and the <2cm percentage, which were developed for lower-accuracy methods (Liu et al., 2019) `ev:asserted` p. 6 ^liu2019keypose-027
- Instance models used approximately 3000 training samples and 320 test samples, with statistics computed on a held-out texture (Liu et al., 2019) `ev:reported` p. 6 ^liu2019keypose-028
- Averaged over all objects, KeyPose reached an instance-level MAE of 9.9 mm, more than 3.5 times more accurate than DenseFusion (Liu et al., 2019) `ev:measured` p. 6 ^liu2019keypose-029
- KeyPose with stereo RGB outperformed DenseFusion with opaque depth on all objects at instance level (Liu et al., 2019) `ev:measured` p. 6 ^liu2019keypose-030
- In the instance-level results, KeyPose achieved a mean AUC of 90.0, versus 71.9 for DenseFusion with opaque depth (Liu et al., 2019) `ev:measured` p. 6 ^liu2019keypose-031
- DenseFusion with opaque depth performed better than DenseFusion with real depth in almost every case, except cup1 and mug6 (Liu et al., 2019) `ev:measured` p. 6 ^liu2019keypose-032
- For both DenseFusion variants, instance-level 3D errors were large, averaging over 35 mm across the dataset (Liu et al., 2019) `ev:measured` p. 6 ^liu2019keypose-033
- For the bottles category, KeyPose reached an MAE of 5.8 versus 34.2 for DenseFusion with opaque depth (Liu et al., 2019) `ev:measured` p. 6 ^liu2019keypose-034
- For the mugs category on unseen textures, KeyPose reached an MAE of 9.9 versus 17.6 for DenseFusion with opaque depth (Liu et al., 2019) `ev:measured` p. 6 ^liu2019keypose-035
- On the held-out mug0 instance, KeyPose reached an MAE of 15.6 versus 23.5 for DenseFusion with opaque depth (Liu et al., 2019) `ev:measured` p. 6 ^liu2019keypose-036
- In category-level experiments on unseen textures, KeyPose surpassed DenseFusion in accuracy by factors of 2 to 5 (Liu et al., 2019) `ev:measured` p. 7 ^liu2019keypose-037
- Both KeyPose and DenseFusion seem to benefit from having larger numbers of training samples at category level (Liu et al., 2019) `ev:measured` p. 7 ^liu2019keypose-038
- On the unseen mug0 object, KeyPose was more accurate than both DenseFusion variants by a factor of 1.5 (Liu et al., 2019) `ev:measured` p. 7 ^liu2019keypose-039
- Stereo input improved accuracy over monocular input by a factor of 2 for both instance and category training (Liu et al., 2019) `ev:measured` p. 7 ^liu2019keypose-040
- With monocular input the disparity error grows to almost a pixel, while stereo input keeps it at half that (Liu et al., 2019) `ev:measured` p. 7 ^liu2019keypose-041
- The authors conclude that keeping the disparity error low is the key to good 3D estimation from stereo (Liu et al., 2019) `ev:asserted` p. 7 ^liu2019keypose-042
- Late fusion showed a much longer error tail than early fusion, with some large metric errors (Liu et al., 2019) `ev:measured` p. 8 ^liu2019keypose-043
- Without the projection loss, disparity errors rose by 0.09 pixels in the instance case and 0.41 pixels in the category case (Liu et al., 2019) `ev:measured` p. 8 ^liu2019keypose-044
- At an object distance of 0.8 m, a 0.41 pixel disparity error yields a 5.5 mm depth error for their stereo system (Liu et al., 2019) `ev:computed` p. 8 ^liu2019keypose-045
- The comparison of direct UVD regression with the integral approach showed a small bias in favor of regression (Liu et al., 2019) `ev:measured` p. 8 ^liu2019keypose-046
- Without [[Symmetry-aware pose loss|the permutation loss]], the two symmetric side keypoints of the tree object clustered in the center to minimize loss (Liu et al., 2019) `ev:measured` p. 8 ^liu2019keypose-047
- Enlarging the bottle0 crop from 180x120 to 360x240 changed 3D MAE from 4.6 mm to 5.3 mm, a minimal degradation (Liu et al., 2019) `ev:measured` p. 8 ^liu2019keypose-048
- With the fixed-size crop and no rescaling, the apparent size of objects varies by a factor of about 2.5 (Liu et al., 2019) `ev:reported` p. 8 ^liu2019keypose-049
- The authors name detecting transparent objects with their heatmap technique as an area that needs further improvement (Liu et al., 2019) `ev:asserted` p. 8 ^liu2019keypose-050
- The authors list adding more complex backgrounds, varying lighting and multi-object samples to the dataset as future work (Liu et al., 2019) `ev:asserted` p. 8 ^liu2019keypose-051
- The authors state that KeyPose can also be applied to opaque, articulated and deformable objects, though they concentrated on transparent rigid objects (Liu et al., 2019) `ev:asserted` p. 8 ^liu2019keypose-052
- The complete dataset consists of 20 object pairs, though only 15 object pairs are used in the main paper experiments (Liu et al., 2019) `ev:reported` p. 10 ^liu2019keypose-053
- A 3D-printed marker of three orthogonal sticks is used to place the opaque twin at the same pose as the transparent object (Liu et al., 2019) `ev:reported` p. 10 ^liu2019keypose-054
- The sensor head, carried by a Franka Panda arm, combines a Stereolabs ZED stereo camera and a Microsoft Kinect Azure RGBD device (Liu et al., 2019) `ev:reported` p. 10 ^liu2019keypose-055
- The ZED captures dual synchronized RGB images at 1280×720 resolution with a stereo baseline of 0.12 m (Liu et al., 2019) `ev:reported` p. 11 ^liu2019keypose-056
- The authors report that the Kinect Azure depth camera has a random error standard deviation of 17 mm (Liu et al., 2019) `ev:reported` p. 11 ^liu2019keypose-057
- Each scan captures some 400 stereo images and 200 RGBD images before the opaque twin is substituted for another scan (Liu et al., 2019) `ev:reported` p. 11 ^liu2019keypose-058
- Across 600 trajectories, AprilTag reprojection RMSE averaged 1.21 pixels for the left stereo camera and 1.30 pixels for the Kinect (Liu et al., 2019) `ev:measured` p. 11 ^liu2019keypose-059
- Farthest Point Sampling picks 6 images that are farthest apart in position on the scan for manual keypoint labeling (Liu et al., 2019) `ev:reported` p. 16 ^liu2019keypose-060
- For the mug2 object, the mean labeling reprojection RMSE over all scans was 2.28 pixels with a standard deviation of 0.83 (Liu et al., 2019) `ev:measured` p. 16 ^liu2019keypose-061
- Gathering a single scan and labeling it takes about 10 minutes of user work, according to the authors (Liu et al., 2019) `ev:reported` p. 16 ^liu2019keypose-062
- From 10,000 Monte Carlo simulations, the authors conclude their labeling is at least five times more accurate than Azure Kinect depth (Liu et al., 2019) `ev:computed` p. 16 ^liu2019keypose-063
- UNet and an explicit correlation operator were tried as alternative architectures but did not do better than the dilated CNN (Liu et al., 2019) `ev:measured` p. 17 ^liu2019keypose-064
- Even with all augmentations the network overfits, with training MAE around 5mm while testing MAE can be several times that (Liu et al., 2019) `ev:measured` p. 18 ^liu2019keypose-065
- Predicted 3D keypoints can align the objects' CAD models to the camera view using the orthogonal Procrustes algorithm (Liu et al., 2019) `ev:reported` p. 18 ^liu2019keypose-066
- Typical inference runtime for a single sample on an NVidia Titan V GPU is 3 ms, excluding bounding box detection (Liu et al., 2019) `ev:measured` p. 18 ^liu2019keypose-067
- The DenseFusion baseline variant uses the same rough detection bounding boxes as KeyPose instead of object segmentation masks (Liu et al., 2019) `ev:reported` p. 19 ^liu2019keypose-068

## 🎯 Contributions


## 📖 Glossary

- **3D keypoint** — A labeled semantic 3D point on an object whose positions together describe its pose.
- **Opaque twin** — A painted opaque copy of a transparent object, placed at its pose to capture depth.
- **UVD** — Image coordinates U, V plus stereo disparity D, convertible to XYZ via a reprojection matrix.
- **Early fusion** — Stacking both stereo crops at the network input so disparity is learned implicitly.
- **Late fusion** — Predicting keypoints separately per stereo image, then triangulating with stereo geometry.
- **Projection loss** — Squared error of predicted keypoints reprojected into the wide label views.
- **Permutation loss** — Minimum loss over allowed keypoint id permutations for symmetric objects.
- **Farthest Point Sampling (FPS)** — Greedy selection of mutually distant camera poses for labeling.
- **AprilTag** — Fiducial marker used to estimate camera pose from known tag positions.
- **TOD** — Transparent Object Dataset of stereo images with 3D keypoint labels and registered depth.

## ❓ Open questions

- Would tight crops with rescaling be more accurate than the fixed-size crop used here?
- Can the UV heatmap reliably serve as the transparent-object detection stage that KeyPose assumes?
- How does KeyPose perform with complex backgrounds, varying lighting and multiple objects per scene?
- How much does generalization to unseen objects improve with more instances per category, given only seven mugs?
- Can training or model changes reduce the gap between training MAE (about 5 mm) and test MAE?
- Does the method transfer to articulated or deformable objects, which the authors claim but do not test?

## 📝 Notes on reading

Read the arXiv v2 (18 May 2020) with supplementary material (pages 10–19), matching the packet identifier.

Inconsistencies inside the paper: the abstract says 15 clear objects in five classes, while the contributions list says 6 classes; the abstract gives a 1.5 to 3.5 improvement factor, while Section 5.2 reports factors of 2 to 5 for category models. The ablation text cites Tables 6 and 4, and the supplement says the complete dataset has 20 object pairs of which 15 are used.

Table 4 (architecture and loss ablation) lost its checkmark columns in extraction: the rows of 3D MAE (bottle0: 10.0, 7.9, 5.4, 4.7, 4.6; bottles: 10.1, 10.6, 9.9, 6.0, 5.8) cannot be mapped to configurations with certainty, so per-column values were not claimed. The text states column 2 is late fusion and column 3 is without projection loss. Table 6 lost its checkmarks too; the 26.4 / 12.8 mm tree0 mapping to without / with permutation loss is inferred from the text and from Table 1 (tree 12.8).

Table 1 and Tables 2–3 are flattened; only headline means and a few category cells were claimed. Figures 1, 7, 8, 9 and 13–21 were described only through their captions. Equations for the losses (1–5) and the depth–disparity relation (6) are partly garbled in extraction.

## Suggested new concepts

- Transparent object perception — depth sensors fail on transparent objects, a recurring problem for lab glassware manipulation.
- Stereo keypoint pose estimation — predicting sparse 3D keypoints directly from stereo pairs as an alternative to depth-based pose.
- Multi-view label propagation — lifting a few 2D annotations to 3D labels across a whole robot-captured sequence.
- Opaque twin technique — a way to obtain ground-truth depth for transparent objects in real data.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Pose de objetos transparentes desde estéreo, sin profundidad

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
