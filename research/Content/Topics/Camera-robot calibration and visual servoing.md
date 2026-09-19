---
aliases: []
type: topic
parent: Computer vision for manipulation
created: 2026-09-19
---

## Scope

How a camera is tied geometrically to a robot and how image measurements then close the control loop: extrinsic hand-eye and robot-world calibration (AX = XB, AX = YB), its marker-based, markerless and certifiably optimal solvers, camera-to-robot pose estimation used as online calibration, and visual servoing controllers (image-based, position-based, direct and learned). It deliberately excludes object 6D pose estimation for its own sake, camera intrinsic calibration, and end-to-end visuomotor policies that do not servo to a goal image or pose; those belong to their own areas.

## Concepts

- [[Markerless hand-eye calibration]] — Markerless hand-eye calibration estimates the camera-to-robot transform from images of the robot itself, using keypoints, rendered masks, tracked points or exploratory motions instead of fiducial boards or tags.
- [[Hand-eye calibration (AX = XB)]] — Hand-eye calibration estimates the fixed rigid transform between a camera and a robot, or between two rigidly linked egomotion sensors, classically by solving AX = XB from paired relative motions, usually observed through a fiducial target.
- [[Visual servoing]] — Visual servoing controls a robot or camera velocity in closed loop from visual feedback so that the current image, or the pose estimated from it, converges to a desired one.
- [[Robot-world and hand-eye calibration (AX = YB)]] — Robot-world and hand-eye calibration jointly estimates two unknown rigid transforms, the sensor-to-hand transform X and the base-to-world or target transform Y, from paired measurements related by AX = YB, and generalizes the classical AX = XB problem to multiple sensors or targets.
- [[Image-based visual servoing]] — Image-based visual servoing computes the camera velocity directly from the error between current and desired image features through the pseudoinverse of an interaction matrix, without reconstructing the relative pose.
- [[Position-based visual servoing]] — Position-based visual servoing first estimates the relative 3D pose between the current and desired camera configurations from images and then drives the robot with a Cartesian control law on that pose error.

## Subtopics

## Related topics

## ❓ Open questions

## Problems

- none yet: no problem names this topic as its topic

## History

- 2026-09-19 · Eki Gonzalez Flamarique · parent: root — new area for concepts promoted from the gap-research batch (04_huecos_y_ampliacion), confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · parent: root → Computer vision for manipulation — grouped under the request's three axes
