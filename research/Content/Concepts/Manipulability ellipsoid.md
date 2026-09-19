---
aliases: []
type: concept
element_type: metric
topic: "[[Lie-group kinematics and dynamics of robot arms]]"
topics: ["[[Lie-group kinematics and dynamics of robot arms]]"]
created: 2026-09-19
---

## Working definition

An ellipsoid, given by a symmetric positive definite matrix such as J J^T, that describes how easily a robot in a given joint configuration can move or exert force along each task direction.

## Evidence

- [[Jaquier2018geometry - Geometry-aware Manipulability Learning, Tracking and#^jaquier2018geometry-001]] — The manipulability ellipsoid serves as a geometric descriptor of the ability to perform motion and exert force along task directions in a joint configuration.
- [[Jaquier2018geometry - Geometry-aware Manipulability Learning, Tracking and#^jaquier2018geometry-004]] — Manipulability polytopes provide a more accurate estimate of robot velocity or force generation capabilities than manipulability ellipsoids, according to the cited literature.
- [[Jaquier2018geometry - Geometry-aware Manipulability Learning, Tracking and#^jaquier2018geometry-005]] — The authors state that the calculation of manipulability polytopes is computationally expensive compared with the easily computed manipulability ellipsoids.
- [[Jaquier2018geometry - Geometry-aware Manipulability Learning, Tracking and#^jaquier2018geometry-008]] — Manipulability tracking is formulated like classical inverse kinematics, establishing a first-order differential relationship between the manipulability ellipsoid and the robot joints.
- [[Jaquier2018geometry - Geometry-aware Manipulability Learning, Tracking and#^jaquier2018geometry-010]] — The paper defines the velocity manipulability ellipsoid as J J^T, whose major axis is aligned with the eigenvector of the maximum eigenvalue.
- [[Jaquier2018geometry - Geometry-aware Manipulability Learning, Tracking and#^jaquier2018geometry-011]] — The major axis of the velocity manipulability ellipsoid indicates the direction of greater velocity generation, which is also the direction of greater perturbation sensitivity.
- [[Jaquier2018geometry - Geometry-aware Manipulability Learning, Tracking and#^jaquier2018geometry-017]] — The manipulability Jacobian is a tensor representing the linear sensitivity of manipulability ellipsoid changes to the joint velocity of the robot.
- [[Jaquier2018geometry - Geometry-aware Manipulability Learning, Tracking and#^jaquier2018geometry-018]] — Manipulability Jacobians are derived for the velocity, force and dynamic manipulability ellipsoids, the last using the robot inertia matrix.
- [[Jaquier2018geometry - Geometry-aware Manipulability Learning, Tracking and#^jaquier2018geometry-048]] — The robot tracking a desired manipulability ellipsoid successfully completed the task when higher Cartesian velocities were required.
- [[Jaquier2018geometry - Geometry-aware Manipulability Learning, Tracking and#^jaquier2018geometry-054]] — Kinesthetic demonstrations on Baxter aligned the main axis of the dual-arm force manipulability ellipsoid with the cable extraction direction.
- [[Jaquier2021geometry - Geometry-aware Bayesian Optimization in Robotics using#^jaquier2021geometry-047]] — In the manipulability task, an 8-degree-of-freedom planar robot tracks a desired manipulability ellipsoid in its nullspace during a Cartesian velocity trajectory.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 2 sources · topic: Lie-group kinematics and dynamics of robot arms (drafter's packet `q1-lie-kinematics`, confirmed at the gate)
