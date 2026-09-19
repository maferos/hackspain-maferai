---
aliases: []
type: "source"
title: "Kalib: Easy Hand-Eye Calibration with Reference Point Tracking"
citekey: "Tang2024kalib"
doi: "10.48550/arXiv.2408.10562"
arxiv: "2408.10562"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2408.10562"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Tutian Tang", "Minghao Liu", "Wenqiang Xu", "Cewu Lu"]
sha256: ["c5976e98a5f8b78b04baa5a79934c08e8543312dc6d10751d72cd124cda57179"]
pdf: "Content/Papers/Tang2024kalib.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 66
---

📄 PDF: [[Tang2024kalib.pdf]]

> [!abstract] One-sentence summary
> Kalib calibrates eye-on-base and eye-in-hand cameras without markers, meshes or training by tracking one reference point with an off-the-shelf foundation tracker and solving PnP against forward kinematics, reaching sub-centimetre simulated error.

## Abstract

Hand-eye calibration aims to estimate the transformation between a camera and a robot. Traditional methods rely on fiducial markers, which require considerable manual effort and precise setup. Recent advances in deep learning have introduced markerless techniques but come with more prerequisites, such as retraining networks for each robot, and accessing accurate mesh models for data generation. In this paper, we propose Kalib, an automatic and easy-to-setup hand-eye calibration method that leverages the generalizability of visual foundation models to overcome these challenges. It features only two basic prerequisites, the robot's kinematic chain and a predefined reference point on the robot. During calibration, the reference point is tracked in the camera space. Its corresponding 3D coordinates in the robot coordinate can be inferred by forward kinematics. Then, a PnP solver directly estimates the transformation between the camera and the robot without training new networks or accessing mesh models. Evaluations in simulated and real-world benchmarks show that Kalib achieves good accuracy with a lower manual workload compared with recent baseline methods. We also demonstrate its application in multiple real-world settings with various robot arms and grippers. Kalib's user-friendly design and minimal setup requirements make it a possible solution for continuous operation in unstructured environments. (arXiv)

## 🧠 Key ideas (atomic)

- [[Hand-eye calibration (AX = XB)|Traditional hand-eye calibration]] usually relies on boards with fiducial markers that must be printed precisely, mounted flatly, and carefully positioned (Tang et al., 2024) `ev:cited` p. 1 ^tang2024kalib-001
- Networks in [[Markerless hand-eye calibration|prior markerless methods]] must be retrained when the robot's appearance is altered, for example by extra sensors or new end-effectors (Tang et al., 2024) `ev:asserted` p. 1 ^tang2024kalib-002
- Generating training data for prior markerless methods requires the robot's precise mesh models and textures, which may not always be available (Tang et al., 2024) `ev:asserted` p. 1 ^tang2024kalib-003
- The authors frame [[Hand-eye calibration (AX = XB)|hand-eye calibration]] as fundamentally establishing correspondence between specific image pixels and their respective coordinates on the robot (Tang et al., 2024) `ev:asserted` p. 1 ^tang2024kalib-004
- Kalib is proposed as an [[Markerless hand-eye calibration|automatic hand-eye calibration method]] needing only the robot kinematic chain and a predefined reference point on the robot (Tang et al., 2024) `ev:asserted` p. 2 ^tang2024kalib-005
- DREAM and CtRNet detect 2D structural keypoints of the robot with neural networks and estimate camera pose using PnP (Tang et al., 2024) `ev:cited` p. 2 ^tang2024kalib-006
- Direct 6D pose estimation of robots is reported to be noisy and sensitive to light conditions, occlusion, and the sim-to-real gap (Tang et al., 2024) `ev:cited` p. 2 ^tang2024kalib-007
- EasyHeC refines an estimated 6D pose through mask prediction and differentiable rendering, which also requires a precise mesh model (Tang et al., 2024) `ev:cited` p. 2 ^tang2024kalib-008
- [[Markerless hand-eye calibration|Pioneering markerless methods]] used Structure-from-Motion to estimate camera motion, working only under the eye-in-hand setting (Tang et al., 2024) `ev:cited` p. 2 ^tang2024kalib-009
- An off-the-shelf foundation model tracks the 2D image coordinates of the reference point across the frames recording robot motion (Tang et al., 2024) `ev:reported` p. 2 ^tang2024kalib-010
- The 3D coordinates of the reference point in the robot base frame are computed from recorded joint positions using forward kinematics (Tang et al., 2024) `ev:reported` p. 4 ^tang2024kalib-011
- A Perspective-n-Point solver then estimates the camera-to-robot transformation from the 2D–3D correspondences of the tracked reference point (Tang et al., 2024) `ev:reported` p. 3 ^tang2024kalib-012
- The authors note eye-in-hand and eye-on-base settings are dual, since the base-to-end-effector transform follows from forward kinematics (Tang et al., 2024) `ev:asserted` p. 3 ^tang2024kalib-013
- A suitable reference point should be rigidly attached to the kinematic chain, generally unobstructed in view, and show clear visual features (Tang et al., 2024) `ev:asserted` p. 3 ^tang2024kalib-014
- The method tracks a point on the robot's surface rather than internal joints, whose surface projections may vary with different movements (Tang et al., 2024) `ev:asserted` p. 3 ^tang2024kalib-015
- Suggested reference points include the flange center for arms without end-effectors, or the closed fingertips' center for parallel grippers (Tang et al., 2024) `ev:asserted` p. 3 ^tang2024kalib-016
- The initial reference point position on the first frame is annotated by a single mouse click, the only manual annotation required (Tang et al., 2024) `ev:reported` p. 4 ^tang2024kalib-017
- The off-the-shelf tracking models are used without retraining or finetuning, relying on their pretraining on large-scale datasets (Tang et al., 2024) `ev:reported` p. 4 ^tang2024kalib-018
- SpatialTracker was chosen as the tracking module because it achieves a good balance between accuracy and inference speed (Tang et al., 2024) `ev:reported` p. 4 ^tang2024kalib-019
- Synchronization frames, where the arm completely stops before capture, are introduced to counter motion blur and timing mismatches between robot and camera (Tang et al., 2024) `ev:reported` p. 4 ^tang2024kalib-020
- Unsynchronized frames are still processed by the tracker to keep track, but are excluded from camera pose estimation (Tang et al., 2024) `ev:reported` p. 4 ^tang2024kalib-021
- Making every frame a synchronization frame is time-consuming but yields the most precise results, according to the authors (Tang et al., 2024) `ev:asserted` p. 4 ^tang2024kalib-022
- As few as 10-20 synchronization frames can be enough for a reasonable calibration result, which gradually improves with more frames (Tang et al., 2024) `ev:measured` p. 4 ^tang2024kalib-023
- Camera pose is solved with the SQPnP solver implemented in OpenCV, chosen for consistently fast and globally optimal solutions (Tang et al., 2024) `ev:reported` p. 4 ^tang2024kalib-024
- Unlike structural keypoint methods, Kalib can work with as few as one point pair per frame, accumulating correspondences across frames (Tang et al., 2024) `ev:asserted` p. 4 ^tang2024kalib-025
- The reference point should traverse the workspace broadly rather than along a single line, avoiding collinear arrangements that are a known PnP limitation (Tang et al., 2024) `ev:asserted` p. 4 ^tang2024kalib-026
- For eye-in-hand calibration, the robot topology is conceptually reversed, turning the setup into its dual eye-on-base problem (Tang et al., 2024) `ev:reported` p. 4 ^tang2024kalib-027
- In eye-in-hand mode, the reference point is where the robot base shell intersects the robot's x axis (Tang et al., 2024) `ev:reported` p. 4 ^tang2024kalib-028
- Simulation experiments used a Franka Emika Panda robot in RFUniverse, recording 20 video segments of 10 seconds each (Tang et al., 2024) `ev:reported` p. 5 ^tang2024kalib-029
- The simulated camera was configured with a resolution of 1920 × 1080 at 30 Hz and a field of view of 60 degrees (Tang et al., 2024) `ev:reported` p. 5 ^tang2024kalib-030
- Real-world evaluation used 60 video segments from DROID, a dataset of 564 scenes with two eye-on-base cameras at 1280 × 720 (Tang et al., 2024) `ev:reported` p. 5 ^tang2024kalib-031
- Real-world accuracy was measured indirectly as IoU between robot masks rendered from estimated extrinsics and manually labeled first-frame masks (Tang et al., 2024) `ev:reported` p. 5 ^tang2024kalib-032
- Kalib was compared with DREAM, EasyHeC, and a traditional marker-based method implemented in the easy handeye ROS toolbox (Tang et al., 2024) `ev:reported` p. 5 ^tang2024kalib-033
- In simulation, the zero-shot tracking error on the reference point quickly converges within ±10 pixels of ground truth (Tang et al., 2024) `ev:measured` p. 5 ^tang2024kalib-034
- The simulated tracking error shows no sign of divergence over the whole 300 frames evaluated (Tang et al., 2024) `ev:measured` p. 5 ^tang2024kalib-035
- In simulation, mean translational and rotational errors are reported as around 0.3 cm and 0.5 degrees respectively (Tang et al., 2024) `ev:measured` p. 2 ^tang2024kalib-036
- In simulated eye-on-base calibration, Kalib reached mean absolute translational errors of 0.30, 0.45 and 0.60 cm on x, y and z (Tang et al., 2024) `ev:measured` p. 5 ^tang2024kalib-037
- Kalib's simulated eye-on-base mean rotational error was 0.01 rad, matching the traditional method and DREAM (Tang et al., 2024) `ev:measured` p. 5 ^tang2024kalib-038
- In simulated eye-on-base calibration, EasyHeC had lower y and z errors than Kalib, at 0.20 and 0.17 cm (Tang et al., 2024) `ev:measured` p. 5 ^tang2024kalib-039
- DREAM showed simulated eye-on-base translational errors of 0.90, 1.01 and 1.13 cm on x, y and z, all higher than Kalib's (Tang et al., 2024) `ev:measured` p. 5 ^tang2024kalib-040
- In simulated eye-in-hand calibration, Kalib had x, y and z errors of 0.48, 0.52 and 0.77 cm (Tang et al., 2024) `ev:measured` p. 5 ^tang2024kalib-041
- The traditional marker-based method had simulated eye-in-hand errors of 0.65, 0.42 and 1.44 cm on x, y and z (Tang et al., 2024) `ev:measured` p. 5 ^tang2024kalib-042
- EasyHeC and DREAM were compared only in the eye-on-base setting because they are not designed for eye-in-hand (Tang et al., 2024) `ev:reported` p. 5 ^tang2024kalib-043
- EasyHeC may struggle when the robot is self-occluded or partially visible, likely due to its differentiable renderer and gradient-based optimizer (Tang et al., 2024) `ev:asserted` p. 5 ^tang2024kalib-044
- The tracking module runs at approximately 5 frames per second on a single RTX 3090 GPU (Tang et al., 2024) `ev:measured` p. 5 ^tang2024kalib-045
- Each Kalib calibration process takes around 2 minutes, whereas EasyHeC takes around 15 minutes per calibration (Tang et al., 2024) `ev:measured` p. 5 ^tang2024kalib-046
- EasyHeC and DREAM require several extra hours to generate the Panda robot dataset for training their networks (Tang et al., 2024) `ev:asserted` p. 6 ^tang2024kalib-047
- On the DROID test set, Kalib achieved a mean IoU of 0.80, compared with 0.77 for EasyHeC (Tang et al., 2024) `ev:measured` p. 6 ^tang2024kalib-048
- The traditional calibration used to construct DROID achieved a higher mean IoU of 0.87 on the same test set (Tang et al., 2024) `ev:measured` p. 6 ^tang2024kalib-049
- The authors attribute Kalib's lower DROID IoU partly to sequences where the arm moves primarily along a straight line (Tang et al., 2024) `ev:asserted` p. 6 ^tang2024kalib-050
- Other DROID failures arise when the reference point leaves the frame or is occluded by manipulated objects, causing tracking loss (Tang et al., 2024) `ev:asserted` p. 6 ^tang2024kalib-051
- Excluding these cases, 9 out of 60 sequences, raises Kalib's mean IoU on the DROID test set to 0.85 (Tang et al., 2024) `ev:measured` p. 6 ^tang2024kalib-052
- Figure 3 shows a DROID case indicating that traditional methods can accidentally fail, even in expert-made datasets (Tang et al., 2024) `ev:asserted` p. 6 ^tang2024kalib-053
- In such cases, [[Markerless hand-eye calibration|markerless methods]] can be applied as a post-hoc remedy to minimize the impact of calibration accidents (Tang et al., 2024) `ev:asserted` p. 6 ^tang2024kalib-054
- In real-world examples, EasyHeC fails when the arm is partially visible, whereas Kalib works with both full and partial views (Tang et al., 2024) `ev:measured` p. 6 ^tang2024kalib-055
- Across 10 random simulated scenes, mean calibration error quickly converges below 0.1 cm or 1 degree after 10 frames (Tang et al., 2024) `ev:measured` p. 6 ^tang2024kalib-056
- With 3 pairs of points, the PnP module fails to give reasonable results, although this is theoretically feasible (Tang et al., 2024) `ev:measured` p. 6 ^tang2024kalib-057
- The surface reference point achieved the lowest and most stable tracking error compared with the structural keypoints Joint 0 to Joint 6 (Tang et al., 2024) `ev:measured` p. 7 ^tang2024kalib-058
- With Gaussian noise added to ground-truth 2D positions, mean calibration error stays below 1 cm when σ ≤10 px (Tang et al., 2024) `ev:computed` p. 7 ^tang2024kalib-059
- The authors conclude that the PnP algorithm can handle the noise from the tracking module in their setting (Tang et al., 2024) `ev:asserted` p. 7 ^tang2024kalib-060
- Kalib was used to simultaneously calibrate eye-in-hand and eye-on-base Realsense D415 cameras on a Flexiv Rizon 4 arm in a kitchen (Tang et al., 2024) `ev:reported` p. 7 ^tang2024kalib-061
- Further real-world tests covered a dual-arm mobile robot with two xArm 6 arms and a Shadow Dexterous Hand on a UR10 arm (Tang et al., 2024) `ev:reported` p. 7 ^tang2024kalib-062
- These robot systems had been modified from factory settings, which would typically require retraining for current neural network-based methods (Tang et al., 2024) `ev:asserted` p. 7 ^tang2024kalib-063
- The authors conclude that Kalib needs neither a calibration board nor the robot's exact 3D mesh model (Tang et al., 2024) `ev:asserted` p. 7 ^tang2024kalib-064
- The tracking module may lose track when the background is extremely noisy or motion blur occurs due to low ambient light (Tang et al., 2024) `ev:asserted` p. 7 ^tang2024kalib-065
- The authors expect the method to benefit immediately from future advances in tracking algorithms under difficult conditions (Tang et al., 2024) `ev:asserted` p. 7 ^tang2024kalib-066

## 🎯 Contributions

## 📖 Glossary

- **Hand-eye calibration** — estimating the rigid transformation between a camera and a robot.
- **Eye-on-base (EoB)** — camera fixed relative to the robot base; unknown transform camera-to-base.
- **Eye-in-hand (EiH)** — camera rigidly mounted on the end-effector; unknown transform camera-to-end-effector.
- **Perspective-n-Point (PnP)** — estimating camera pose from known 3D points and their 2D image projections.
- **SQPnP** — a consistently fast, globally optimal PnP solver available in OpenCV.
- **Reference point** — a predefined, visually distinct point rigidly attached to the robot's kinematic chain.
- **Synchronization frame** — a frame captured after the arm fully stops, giving synchronized joint and image data.
- **Point tracking** — recovering the image motion of chosen pixels across video frames.
- **Forward kinematics** — computing link poses from joint positions along the kinematic chain.

## ❓ Open questions

- How accurate is Kalib on real robots quantitatively, beyond the indirect mask-IoU proxy and qualitative mask overlays?
- Can the straight-line and occluded DROID sequences be detected automatically before trusting a calibration?
- How does calibration accuracy depend on the choice and exact 3D placement of the reference point on custom tools?
- Would tracking several reference points per frame improve robustness where a single point leaves the view?
- How sensitive is the eye-in-hand variant to error in the measured base reference coordinate x_ref?
- Does accuracy hold for small or reflective end-effectors whose surface offers weak visual features?

## 📝 Notes on reading

Read the arXiv v2 (24 Mar 2025) of 2408.10562. Figures 4 to 7 (tracking error box plots, error vs number of frames, per-joint tracking error on a log axis, sensitivity curve) are only described in the text; values were claimed only where the text states them. Table I (qualitative comparison with Board, SfM, Keypoint, Mask and 6D Pose methods) lost its check marks in extraction; only its prose was used. Equations 1 to 3 are garbled in the cached text but are described in words.

Inconsistencies: the introduction gives rotational error of around 0.5 degrees, while Table II reports rotational error in radians (0.01 rad EoB, 0.07 rad EiH, the latter roughly 4 degrees). In Table II, the traditional EoB method has a lower z error (0.10 cm) than Kalib (0.60 cm), and EasyHeC beats Kalib on y and z; the paper's framing of superiority rests mainly on x error, setup effort and occlusion robustness. The tracking section cites errors within ±10 pixels, while the sensitivity section says tracking error stays within several pixels. Real-world robot demonstrations (Flexiv, xArm, Shadow Hand, pointing experiment on a ChArUco board) are qualitative only.

## Suggested new concepts

- Markerless hand-eye calibration — a recurring family of methods (keypoint, mask, 6D pose, point tracking) worth comparing in one note.
- Point tracking with visual foundation models — SpatialTracker, CoTracker and similar zero-shot trackers reused as calibration front-ends.
- Perspective-n-Point — core solver shared by many calibration and pose estimation papers.
- Eye-in-hand vs eye-on-base duality — the reduction lets one pipeline handle both camera mountings.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H5.** Calibración sin marcadores ni reentrenamiento que sigue un punto del robot con un modelo fundacional y resuelve PnP con la cinemática.
