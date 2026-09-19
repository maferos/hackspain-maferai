---
aliases: ["Hand-eye calibration", "AX = XB"]
type: concept
element_type: process
topic: "[[Camera-robot calibration and visual servoing]]"
topics: ["[[Camera-robot calibration and visual servoing]]"]
created: 2026-09-19
---

## Working definition

Hand-eye calibration estimates the fixed rigid transform between a camera and a robot, or between two rigidly linked egomotion sensors, classically by solving AX = XB from paired relative motions, usually observed through a fiducial target.

## Evidence

- [[Chanrungmaneekul2025arc - ARC-Calib Autonomous Markerless Camera-to-Robot Calibration#^chanrungmaneekul2025arc-002]] — Traditional camera-to-robot calibration methods are typically formulated as solving the classic AX = XB equation with assistance from fiducial markers or chessboards.
- [[Chanrungmaneekul2025arc - ARC-Calib Autonomous Markerless Camera-to-Robot Calibration#^chanrungmaneekul2025arc-046]] — The baseline was traditional AprilTag-based hand-eye calibration from a ROS package, with its convergence point manually determined by the operator.
- [[Chen2023easyhec - EasyHeC Accurate and Automatic Hand-eye Calibration via#^chen2023easyhec-001]] — Traditional hand-eye calibration methods rely on markers such as ArUco tags or checkerboard patterns to link robot and camera frames.
- [[Chen2023easyhec - EasyHeC Accurate and Automatic Hand-eye Calibration via#^chen2023easyhec-007]] — EasyHeC replaces the transformation-equivalence objective AX = XB with a loss function grounded in per-pixel segmentation of the robot arm.
- [[Chen2026optimal - Optimal Uncertainty-Aware Calibration for the AX=YB Problem#^chen2026optimal-002]] — The authors argue that AX = YB can be transformed into AX = XB, which makes the AX = YB formulation more general.
- [[Chen2026optimal - Optimal Uncertainty-Aware Calibration for the AX=YB Problem#^chen2026optimal-009]] — Linear hand-eye calibration methods minimize algebraic errors, so their achievable accuracy is inherently bounded and sensitive to the uncertainty in the data.
- [[Tang2024kalib - Kalib Easy Hand-Eye Calibration with Reference Point#^tang2024kalib-001]] — Traditional hand-eye calibration usually relies on boards with fiducial markers that must be printed precisely, mounted flatly, and carefully positioned
- [[Tang2024kalib - Kalib Easy Hand-Eye Calibration with Reference Point#^tang2024kalib-004]] — The authors frame hand-eye calibration as fundamentally establishing correspondence between specific image pixels and their respective coordinates on the robot
- [[Wise2020certifiably - Certifiably Optimal Monocular Hand-Eye Calibration#^wise2020certifiably-001]] — The paper extends a certifiably optimal hand-eye calibration method to the case where one sensor cannot observe its translational scale.
- [[Wise2020certifiably - Certifiably Optimal Monocular Hand-Eye Calibration#^wise2020certifiably-005]] — The common AX = XB hand-eye formulation can be applied to any egomotion-capable sensor, including stereo cameras, 3D lidar units and GNSS-INS devices.
- [[Wise2020certifiably - Certifiably Optimal Monocular Hand-Eye Calibration#^wise2020certifiably-006]] — The authors prove that the SDP relaxation of the hand-eye calibration QCQP is guaranteed to be tight when measurement noise is bounded.
- [[Wise2020certifiably - Certifiably Optimal Monocular Hand-Eye Calibration#^wise2020certifiably-009]] — An earlier experimental investigation concluded that coupled nonlinear optimization gives more accurate hand-eye solutions under noise than decoupled closed-form methods.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 5 sources · topic: Camera-robot calibration and visual servoing (drafter's packet `q5-calibration-servoing`, confirmed at the gate)
