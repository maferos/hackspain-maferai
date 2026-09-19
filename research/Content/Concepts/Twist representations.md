---
aliases: []
type: concept
element_type: concept
topic: "[[Lie-group kinematics and dynamics of robot arms]]"
topics: ["[[Lie-group kinematics and dynamics of robot arms]]"]
created: 2026-09-19
---

## Working definition

The four ways of expressing a rigid body's velocity as a six-vector (body-fixed, spatial, hybrid and mixed), which differ in the point where velocity is measured and the frame it is resolved in, and which change the cost of recursive kinematics and dynamics algorithms.

## Evidence

- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-015]] — The paper introduces four twist definitions, body-fixed, spatial, hybrid, and mixed, which differ by reference point and resolving frame.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-037]] — The body-fixed twist of each body follows recursively from its predecessor's twist through an adjoint transformation plus the contribution of its joint.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-039]] — Body-fixed twists are left-invariant vector fields on SE (3), since they are unaffected by a change of the inertial frame.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-045]] — The author states the spatial twist recursion is the simplest possible, since body twists are added without any coordinate transformation.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-051]] — With hybrid twists, body inertia properties must be resolved in the inertial frame, so they become configuration dependent in the motion equations.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-053]] — Mixed twists are used in multibody dynamics modeling because the Newton-Euler equations with respect to the center of mass become decoupled.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-057]] — According to the author, a conclusive computational analysis comparing all four twist representations has not yet been reported.
- [[Mueller2023screw2 - Screw and Lie Group Theory in Multibody Dynamics --#^mueller2023screw2-025]] — Recursive methods using different twist representations give algorithmically equivalent methods with different computational costs, according to the author.
- [[Mueller2023screw2 - Screw and Lie Group Theory in Multibody Dynamics --#^mueller2023screw2-044]] — The description of the multibody geometry is independent from the chosen representation of twists, according to the author.
- [[Mueller2023screw2 - Screw and Lie Group Theory in Multibody Dynamics --#^mueller2023screw2-057]] — The author states that the potential benefit of spatial or hybrid twists for closed-form equations of motion remains to be explored.
- [[Mueller2023screw2 - Screw and Lie Group Theory in Multibody Dynamics --#^mueller2023screw2-066]] — Most O (n) algorithms in the literature used the hybrid representation of twists, according to the author.
- [[Mueller2023screw - Screw and Lie Group Theory in Multibody Kinematics --#^mueller2023screw-055]] — The paper tabulates the transformations relating the four twist forms and the three joint screw coordinate representations to one another.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 2 sources · topic: Lie-group kinematics and dynamics of robot arms (drafter's packet `q1-lie-kinematics`, confirmed at the gate)
