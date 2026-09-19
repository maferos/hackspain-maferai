---
aliases: []
type: "source"
title: "ARC-Calib: Autonomous Markerless Camera-to-Robot Calibration via Exploratory Robot Motions"
citekey: "Chanrungmaneekul2025arc"
doi: "10.48550/arXiv.2503.14701"
arxiv: "2503.14701"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2503.14701"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Podshara Chanrungmaneekul", "Yiting Chen", "Joshua T. Grace", "Aaron M. Dollar", "Kaiyu Hang"]
sha256: ["ea21554398a272ddaa42130da1912285fc89a57b929f27e61a8cde41ee1a4180"]
pdf: "Content/Papers/Chanrungmaneekul2025arc.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 53
---

📄 PDF: [[Chanrungmaneekul2025arc.pdf]]

> [!abstract] One-sentence summary
> ARC-Calib calibrates a fixed camera to a robot without markers or learned models by fitting ellipses to optical-flow keypoint trajectories of single-joint exploratory motions and solving a convex collinearity/coplanarity problem, beating AprilTag hand-eye calibration in mask IoU on a Franka arm.

## Abstract

Camera-to-robot (also known as eye-to-hand) calibration is a critical component of vision-based robot manipulation. Traditional marker-based methods often require human intervention for system setup. Furthermore, existing autonomous markerless calibration methods typically rely on pre-trained robot tracking models that impede their application on edge devices and require fine-tuning for novel robot embodiments. To address these limitations, this paper proposes a model-based markerless camera-to-robot calibration framework, ARC-Calib, that is fully autonomous and generalizable across diverse robots and scenarios without requiring extensive data collection or learning. First, exploratory robot motions are introduced to generate easily trackable trajectory-based visual patterns in the camera's image frames. Then, a geometric optimization framework is proposed to exploit the coplanarity and collinearity constraints from the observed motions to iteratively refine the estimated calibration result. Our approach eliminates the need for extra effort in either environmental marker setup or data collection and model training, rendering it highly adaptable across a wide range of real-world autonomous systems. Extensive experiments are conducted in both simulation and the real world to validate its robustness and generalizability. (arXiv)

## 🧠 Key ideas (atomic)

- ARC-Calib is a model-based [[Markerless hand-eye calibration|markerless camera-to-robot calibration]] framework that plans exploratory robot motions to generate trackable visual features for iterative calibration. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 1 ^chanrungmaneekul2025arc-001
- Traditional camera-to-robot calibration methods are typically formulated as solving the [[Hand-eye calibration (AX = XB)|classic AX = XB equation]] with assistance from fiducial markers or chessboards. (Chanrungmaneekul et al., 2025) `ev:cited` p. 1 ^chanrungmaneekul2025arc-002
- The authors note that established marker-based calibration methods, while generalizable, often demand cumbersome manual effort in the system setup process. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 1 ^chanrungmaneekul2025arc-003
- The authors argue that models trained on synthetic data often require real-world finetuning to overcome the [[Sim-to-real transfer|sim-to-real gap]]. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 1 ^chanrungmaneekul2025arc-004
- Because observed keypoint trajectories are motion-oriented without semantic information, the authors state that even traditional optical flow suffices to extract the features. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 1 ^chanrungmaneekul2025arc-005
- [[Markerless hand-eye calibration|Keypoint-based markerless approaches]] detect robot keypoints with deep neural networks, then adapt the perspective-n-point algorithm to estimate the calibration result. (Chanrungmaneekul et al., 2025) `ev:cited` p. 2 ^chanrungmaneekul2025arc-006
- The authors state that inconsistent keypoint detection constrains the calibration accuracy achievable by existing learning-based keypoint markerless calibration methods. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 2 ^chanrungmaneekul2025arc-007
- [[Markerless hand-eye calibration|Rendering-based markerless calibration methods]] often rely on [[Domain randomization|domain-randomized synthetic training data]] to enable robot pose estimation in the real world. (Chanrungmaneekul et al., 2025) `ev:cited` p. 2 ^chanrungmaneekul2025arc-008
- The authors argue that [[Markerless hand-eye calibration|learned markerless calibration networks]] are trained for specific robot embodiments, requiring considerable fine-tuning for additional robots. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 2 ^chanrungmaneekul2025arc-009
- The work addresses camera-to-robot calibration for N-DoF serial robot manipulators, estimating the transformation from the robot base frame to the camera frame. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 2 ^chanrungmaneekul2025arc-010
- Pixel coordinates are normalized with the intrinsic parameters so that the proposed algorithm remains independent of the camera's intrinsic matrix. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 2 ^chanrungmaneekul2025arc-011
- Each exploratory motion consists of a single joint movement, which can be regarded as the rotation of a single rigid body. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 2 ^chanrungmaneekul2025arc-012
- Each exploratory motion is defined by a starting joint configuration, a selected joint, and the change in that joint's configuration. (Chanrungmaneekul et al., 2025) `ev:reported` p. 3 ^chanrungmaneekul2025arc-013
- Motions are selected by randomly generating start configurations and joints, requiring a minimum joint change while avoiding collisions with the environment's collision model. (Chanrungmaneekul et al., 2025) `ev:reported` p. 3 ^chanrungmaneekul2025arc-014
- Keypoints tracked during each exploratory motion are identified by visual features such as strong corners in the camera image. (Chanrungmaneekul et al., 2025) `ev:reported` p. 3 ^chanrungmaneekul2025arc-015
- The number of tracked keypoints per motion is dynamically determined by the tracking algorithm and may vary across different motions. (Chanrungmaneekul et al., 2025) `ev:reported` p. 3 ^chanrungmaneekul2025arc-016
- Under perspective projection, the circular 3D paths of tracked points typically appear on the image plane as ellipses or straight lines. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 3 ^chanrungmaneekul2025arc-017
- The method uses only elliptical keypoint trajectories, because lines from robot motion can be challenging to distinguish from lines caused by tracking noise. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 3 ^chanrungmaneekul2025arc-018
- All ellipses of one motion are fitted jointly by least squares on algebraic distances, constrained to share the same semi-major axis orientation. (Chanrungmaneekul et al., 2025) `ev:reported` p. 3 ^chanrungmaneekul2025arc-019
- Fitted conic solutions that violate the ellipse constraint are discarded, since the least-squares minimization does not explicitly enforce that constraint. (Chanrungmaneekul et al., 2025) `ev:reported` p. 4 ^chanrungmaneekul2025arc-020
- The camera-frame rotational axis is estimated from each fitted ellipse using a closed-form 3D circle orientation solution introduced in prior work. (Chanrungmaneekul et al., 2025) `ev:cited` p. 4 ^chanrungmaneekul2025arc-021
- The cone eigen-decomposition yields four plane-normal solutions, reduced to two candidate rotational axes per trajectory by discarding opposite rotation directions. (Chanrungmaneekul et al., 2025) `ev:reported` p. 4 ^chanrungmaneekul2025arc-022
- Projecting trajectories onto a plane normal to a candidate axis produces 2D circles whose centers lie on the projected rotational axis line. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 4 ^chanrungmaneekul2025arc-023
- The 2D circle-fitting problem yields at most two critical points, and the global minimum is the one with the lower error. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 5 ^chanrungmaneekul2025arc-024
- The reference position line is fitted through the 2D circle centers using RANSAC linear fitting to eliminate outlier trajectories. (Chanrungmaneekul et al., 2025) `ev:reported` p. 5 ^chanrungmaneekul2025arc-025
- The best candidate axis is chosen by a heuristic summing radius-normalized circle-fitting errors over all keypoint trajectories projected onto its plane. (Chanrungmaneekul et al., 2025) `ev:reported` p. 5 ^chanrungmaneekul2025arc-026
- The calibration enforces collinearity and coplanarity constraints introduced in prior pose-estimation work to align robot movements with camera observations. (Chanrungmaneekul et al., 2025) `ev:cited` p. 5 ^chanrungmaneekul2025arc-027
- The rotational axis and joint position of each motion in the robot frame are computed from the starting configuration using forward kinematics. (Chanrungmaneekul et al., 2025) `ev:reported` p. 5 ^chanrungmaneekul2025arc-028
- The collinearity constraint requires each kinematic rotational axis, once rotated into the camera frame, to be collinear with the observed camera-frame axis. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 5 ^chanrungmaneekul2025arc-029
- The rotation is solved independently of translation by eliminating the translation in closed form, then minimizing a squared residual norm. (Chanrungmaneekul et al., 2025) `ev:reported` p. 6 ^chanrungmaneekul2025arc-030
- Rotation-matrix orthogonality and determinant constraints are temporarily relaxed during optimization, then enforced afterwards by projecting the estimate through singular value decomposition. (Chanrungmaneekul et al., 2025) `ev:reported` p. 6 ^chanrungmaneekul2025arc-031
- Without an initial estimate, observations are filtered by trajectory consistency, rejecting ambiguous cases where the top two axis candidates agree too similarly. (Chanrungmaneekul et al., 2025) `ev:reported` p. 6 ^chanrungmaneekul2025arc-032
- Only three observations satisfying the initial filtering conditions are needed to compute an initial camera-to-robot transformation estimate. (Chanrungmaneekul et al., 2025) `ev:reported` p. 6 ^chanrungmaneekul2025arc-033
- With an initial estimate, observations are retained only if their rotational-axis and reference-position reprojection errors fall within predefined thresholds. (Chanrungmaneekul et al., 2025) `ev:reported` p. 6 ^chanrungmaneekul2025arc-034
- Calibration terminates automatically when the dimension-wise range of estimates over a sliding window of h actions stays below a predefined threshold. (Chanrungmaneekul et al., 2025) `ev:reported` p. 7 ^chanrungmaneekul2025arc-035
- The method is evaluated on a Franka Research 3 robot, both in PyBullet simulation and in a real-world setup. (Chanrungmaneekul et al., 2025) `ev:reported` p. 7 ^chanrungmaneekul2025arc-036
- The real-world setup records the robot with a RealSense Camera D415 at 1920×1080 pixels and 30 Hz. (Chanrungmaneekul et al., 2025) `ev:reported` p. 7 ^chanrungmaneekul2025arc-037
- Simulated calibration was run for 10 different camera poses with 5 runs per setup, measuring translational and rotational error. (Chanrungmaneekul et al., 2025) `ev:reported` p. 7 ^chanrungmaneekul2025arc-038
- The simulated monocular camera's intrinsic parameters were set to match those of the real-world camera used in the physical experiments. (Chanrungmaneekul et al., 2025) `ev:reported` p. 7 ^chanrungmaneekul2025arc-039
- In simulation, rotational and translational calibration errors decrease progressively as more observations from exploratory motions are collected. (Chanrungmaneekul et al., 2025) `ev:measured` p. 7 ^chanrungmaneekul2025arc-040
- With just 3 exploratory motions in simulation, ARC-Calib reaches an average rotational calibration error of 0.0225 rad. (Chanrungmaneekul et al., 2025) `ev:measured` p. 7 ^chanrungmaneekul2025arc-041
- With just 3 exploratory motions in simulation, ARC-Calib reaches an average translational calibration error of 0.0786 m. (Chanrungmaneekul et al., 2025) `ev:measured` p. 7 ^chanrungmaneekul2025arc-042
- With 25 exploratory motions in simulation, the rotational calibration error of ARC-Calib drops to 0.0042 rad. (Chanrungmaneekul et al., 2025) `ev:measured` p. 7 ^chanrungmaneekul2025arc-043
- With 25 exploratory motions in simulation, the translational calibration error of ARC-Calib reduces to 0.0065 m. (Chanrungmaneekul et al., 2025) `ev:measured` p. 7 ^chanrungmaneekul2025arc-044
- The real-world evaluation used six different camera poses, running the method until the estimated results converged under its convergence criterion. (Chanrungmaneekul et al., 2025) `ev:reported` p. 7 ^chanrungmaneekul2025arc-045
- The baseline was [[Hand-eye calibration (AX = XB)|traditional AprilTag-based hand-eye calibration]] from a ROS package, with its convergence point manually determined by the operator. (Chanrungmaneekul et al., 2025) `ev:reported` p. 7 ^chanrungmaneekul2025arc-046
- Real-world accuracy was measured as IoU between robot masks rendered from estimated transformations and manually labeled ground truth masks. (Chanrungmaneekul et al., 2025) `ev:reported` p. 7 ^chanrungmaneekul2025arc-047
- In real-world experiments, ARC-Calib achieves an average IoU of 0.94, outperforming the traditional method's average IoU of 0.84. (Chanrungmaneekul et al., 2025) `ev:measured` p. 7 ^chanrungmaneekul2025arc-048
- In real-world experiments, the ARC-Calib calibration process converges after an average of 26.5 selected robot motions. (Chanrungmaneekul et al., 2025) `ev:measured` p. 7 ^chanrungmaneekul2025arc-049
- The authors report that the real-world IoU calibration error trend over motions is similar to the simulated translational and rotational error trends. (Chanrungmaneekul et al., 2025) `ev:measured` p. 7 ^chanrungmaneekul2025arc-050
- The authors state that ARC-Calib is designed to be generalizable across diverse robots and scenarios without pre-trained models or fine-tuning. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 8 ^chanrungmaneekul2025arc-051
- The authors conclude that evaluation in both physical and simulated settings demonstrates the accuracy of the ARC-Calib calibration method. (Chanrungmaneekul et al., 2025) `ev:asserted` p. 8 ^chanrungmaneekul2025arc-052
- The abstract states that pre-trained robot tracking models used by existing markerless calibration methods impede their application on edge devices. (Chanrungmaneekul et al., 2025) `ev:abstract` p. none ^chanrungmaneekul2025arc-053

## 🎯 Contributions


## 📖 Glossary

- **Eye-to-hand calibration** — estimating the fixed camera's pose relative to the robot base frame.
- **Exploratory motion** — a single-joint rotation the robot executes to create trackable image trajectories.
- **AX = XB** — classic hand-eye calibration equation solved from paired robot and camera motions.
- **Perspective-n-point (PnP)** — estimating camera pose from known 3D points and their 2D projections.
- **Algebraic distance** — value of the conic equation at a point, used as fitting residual.
- **Collinearity constraint** — observed and kinematic rotation axes must coincide after applying the calibration rotation.
- **Coplanarity constraint** — kinematic joint position must lie on the plane defined by observed axis data.
- **RANSAC** — robust fitting that repeatedly samples subsets to reject outlier data.
- **IoU** — intersection over union between rendered and ground-truth masks.

## ❓ Open questions

- Does ARC-Calib generalize to robots other than the Franka Research 3, as claimed but not tested?
- How does accuracy compare against learning-based markerless methods such as keypoint- or rendering-based approaches?
- How robust is the ellipse-based pipeline to occlusion, low texture or poor lighting on the robot links?
- Can the number of motions needed (average 26.5 in the real world) be reduced by active rather than random motion selection?
- How sensitive are results to the filtering and convergence thresholds, which are not reported numerically?
- Does the method hold for cameras with low resolution or frame rate, below 1920×1080 at 30 Hz?

## 📝 Notes on reading

Read the arXiv v1 preprint (2503.14701v1, 18 Mar 2025), matching the packet identifier.

Inconsistencies: Fig. 1 caption speaks of the transformation from the camera to the robot, while Eq. (1) and Sec. V describe Tbc as robot base frame to camera frame (and Sec. V intro says camera frame to robot frame). The ellipse constraint in Eq. (5) is printed as 4AC − B² = 0, whereas an ellipse requires 4AC − B² > 0; likely a typo or extraction issue. The abstract claims generalizability across diverse robots, but all experiments use only a Franka Research 3. Real-world pose figure is referenced as shown in 9 (missing Fig.).

Figures described only: Fig. 7 plots rotational (rad) and translational (m) simulation error against 3 to 25 exploratory motions; Fig. 8 plots real-world IoU against motions for ARC-Calib (solid) and traditional calibration (dashed) per camera setup; Fig. 9 overlays robot masks from both methods for 6 camera poses. The motion-selection description on p. 3 is random sampling, although the introduction speaks of a planning module that actively selects motions. Threshold values for filtering and convergence, and the window size h, are not given. Equations with subscripts and superscripts are partly garbled in the extraction but the method text is readable.

## Suggested new concepts

- Markerless camera-to-robot calibration — a recurring problem class with keypoint, rendering and motion-based families worth comparing.
- Hand-eye calibration (AX = XB) — the classical baseline many calibration papers build on or compare against.
- Circle pose from ellipse projection — a reusable geometric tool for recovering 3D circle orientation from images.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H5.** Calibración autónoma basada en modelo que explota restricciones de coplanaridad y colinealidad de movimientos exploratorios del brazo.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
