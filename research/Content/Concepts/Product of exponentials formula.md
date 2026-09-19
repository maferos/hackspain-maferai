---
aliases: ["POE formula"]
type: concept
element_type: method
topic: "[[Lie-group kinematics and dynamics of robot arms]]"
topics: ["[[Lie-group kinematics and dynamics of robot arms]]"]
created: 2026-09-19
---

## Working definition

A way of writing the forward kinematics of an open chain as a product of matrix exponentials of the joint screws, one per joint, times a reference configuration, without needing joint frames or Denavit-Hartenberg parameters.

## Evidence

- [[Mueller2023screw2 - Screw and Lie Group Theory in Multibody Dynamics --#^mueller2023screw2-006]] — The product of exponentials formula, introduced by Brockett, is the central relation of Lie group algorithms for tree-topology multibody systems.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-007]] — The term product of exponentials has been used for open kinematic chains since Brockett introduced it in his work on robotic manipulators.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-026]] — For multi-DOF joints, relative configuration can be written as one exponential of summed joint screws or as a product of exponentials.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-028]] — The body-fixed product-of-exponentials formulation needs only the relative reference configurations of adjacent bodies and joint screw coordinates in a body frame.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-029]] — In the spatial product-of-exponentials formula, joint screws and absolute reference configurations are all expressed in the inertial frame at q = 0.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-030]] — The zero reference formulation was first reported by Gupta using frame transformation matrices, and later introduced by Brockett as the POE formula.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-061]] — A forthcoming paper will address general-topology multibody systems, with loop closure constraints formulated in the form of a product of exponentials.
- [[Seo2022geometric - Geometric Impedance Control on SE(3) for Robotic#^seo2022geometric-015]] — The paper considers manipulators with revolute joints, whose forward kinematics are written as a product of matrix exponentials of joint twists.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 3 sources · topic: Lie-group kinematics and dynamics of robot arms (drafter's packet `q1-lie-kinematics`, confirmed at the gate)
