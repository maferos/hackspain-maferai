---
aliases: ["Markerless camera-to-robot calibration"]
type: concept
element_type: method
topic: "[[Camera-robot calibration and visual servoing]]"
topics: ["[[Camera-robot calibration and visual servoing]]"]
created: 2026-09-19
---

## Working definition

Markerless hand-eye calibration estimates the camera-to-robot transform from images of the robot itself, using keypoints, rendered masks, tracked points or exploratory motions instead of fiducial boards or tags.

## Evidence

- [[Chanrungmaneekul2025arc - ARC-Calib Autonomous Markerless Camera-to-Robot Calibration#^chanrungmaneekul2025arc-001]] — ARC-Calib is a model-based markerless camera-to-robot calibration framework that plans exploratory robot motions to generate trackable visual features for iterative calibration.
- [[Chanrungmaneekul2025arc - ARC-Calib Autonomous Markerless Camera-to-Robot Calibration#^chanrungmaneekul2025arc-006]] — Keypoint-based markerless approaches detect robot keypoints with deep neural networks, then adapt the perspective-n-point algorithm to estimate the calibration result.
- [[Chanrungmaneekul2025arc - ARC-Calib Autonomous Markerless Camera-to-Robot Calibration#^chanrungmaneekul2025arc-008]] — Rendering-based markerless calibration methods often rely on domain-randomized synthetic training data to enable robot pose estimation in the real world.
- [[Chanrungmaneekul2025arc - ARC-Calib Autonomous Markerless Camera-to-Robot Calibration#^chanrungmaneekul2025arc-009]] — The authors argue that learned markerless calibration networks are trained for specific robot embodiments, requiring considerable fine-tuning for additional robots.
- [[Chen2023easyhec - EasyHeC Accurate and Automatic Hand-eye Calibration via#^chen2023easyhec-003]] — According to the authors, the performance of learning-based markerless calibration approaches largely depends on the scale and quality of their training data.
- [[Chen2023easyhec - EasyHeC Accurate and Automatic Hand-eye Calibration via#^chen2023easyhec-006]] — EasyHeC is presented as a markerless, white-box hand-eye calibration system that eliminates the laborious manual design of robot joint poses.
- [[Lu2023markerless - Markerless Camera-to-Robot Pose Estimation via#^lu2023markerless-002]] — The authors argue that lacking online calibration limits vision-based robot control, since minor bumps or repetitive use can throw calibrations off.
- [[Tang2024kalib - Kalib Easy Hand-Eye Calibration with Reference Point#^tang2024kalib-002]] — Networks in prior markerless methods must be retrained when the robot's appearance is altered, for example by extra sensors or new end-effectors
- [[Tang2024kalib - Kalib Easy Hand-Eye Calibration with Reference Point#^tang2024kalib-005]] — Kalib is proposed as an automatic hand-eye calibration method needing only the robot kinematic chain and a predefined reference point on the robot
- [[Tang2024kalib - Kalib Easy Hand-Eye Calibration with Reference Point#^tang2024kalib-009]] — Pioneering markerless methods used Structure-from-Motion to estimate camera motion, working only under the eye-in-hand setting
- [[Tang2024kalib - Kalib Easy Hand-Eye Calibration with Reference Point#^tang2024kalib-054]] — In such cases, markerless methods can be applied as a post-hoc remedy to minimize the impact of calibration accidents
- [[Chen2023easyhec - EasyHeC Accurate and Automatic Hand-eye Calibration via#^chen2023easyhec-014]] — Marker-free Structure-from-Motion calibration methods are described as unsuitable for tracking robot motion in the eye-to-hand setting.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 4 sources · topic: Camera-robot calibration and visual servoing (drafter's packet `q5-calibration-servoing`, confirmed at the gate)
