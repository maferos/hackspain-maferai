---
aliases: ["RNEA"]
type: concept
element_type: method
topic: "[[Lie-group kinematics and dynamics of robot arms]]"
topics: ["[[Lie-group kinematics and dynamics of robot arms]]"]
created: 2026-09-19
---

## Working definition

The standard O(n) inverse dynamics method for a kinematic tree, which propagates velocities and accelerations outward from the base in a forward pass and then accumulates wrenches back toward the base to obtain the joint forces.

## Evidence

- [[Mueller2023screw2 - Screw and Lie Group Theory in Multibody Dynamics --#^mueller2023screw2-028]] — In total, the body-fixed recursive Newton-Euler algorithm needs 3 (n −1) frame transformations for a chain of n bodies with 1-DOF joints.
- [[Mueller2023screw2 - Screw and Lie Group Theory in Multibody Dynamics --#^mueller2023screw2-029]] — The body-fixed recursive Newton-Euler algorithm additionally needs 2n−1 Lie brackets for a kinematic chain of n bodies.
- [[Mueller2023screw2 - Screw and Lie Group Theory in Multibody Dynamics --#^mueller2023screw2-031]] — The spatial recursive Newton-Euler algorithm needs n screw coordinate transformations, n second-order tensor transformations, plus 2n −1 Lie brackets.
- [[Mueller2023screw2 - Screw and Lie Group Theory in Multibody Dynamics --#^mueller2023screw2-040]] — The hybrid recursive Newton-Euler algorithm needs 3n −3 translational transformations of screw coordinates, besides n rotational ones.
- [[Mueller2023screw2 - Screw and Lie Group Theory in Multibody Dynamics --#^mueller2023screw2-041]] — The hybrid recursive Newton-Euler algorithm needs 3n −1 Lie brackets, besides n rotational transformations of the inertia tensor.
- [[Mueller2023screw2 - Screw and Lie Group Theory in Multibody Dynamics --#^mueller2023screw2-049]] — Explicit evaluation of the Euler-Jourdain equations leads to the recursive body-fixed inverse dynamics algorithm presented in section 4.1.
- [[Singh2021efficient - Efficient Analytical Derivatives of Rigid-Body Dynamics#^singh2021efficient-006]] — The earlier chain-rule derivation on the two-pass RNEA has O(Nd) complexity, with N bodies and d the depth of the kinematic tree.
- [[Singh2021efficient - Efficient Analytical Derivatives of Rigid-Body Dynamics#^singh2021efficient-018]] — The RNEA and the Articulated-Body Algorithm are the most efficient O(N) algorithms for calculating inverse and forward dynamics respectively.
- [[Cheng2018rmpflow - RMPflow A Computational Graph for Automatic Motion Policy#^cheng2018rmpflow-005]] — RMPflow mimics the Recursive Newton-Euler algorithm in structure but generalizes it beyond rigid-body systems to highly nonlinear transformations and spaces.
- [[Wensing2023coriolis - Coriolis Factorizations and their Connections to Riemannian#^wensing2023coriolis-008]] — Recursive Newton-Euler methods for computing the dynamics first appeared in the late 1970s, motivated by dynamic analysis of walking machines.
- [[Wensing2023coriolis - Coriolis Factorizations and their Connections to Riemannian#^wensing2023coriolis-009]] — Computed-torque control laws require evaluating the Coriolis terms, which recursive Newton-Euler methods can accomplish in O(n) complexity.
- [[Wensing2023coriolis - Coriolis Factorizations and their Connections to Riemannian#^wensing2023coriolis-011]] — Niemeyer's recursive Newton-Euler variant was the first compatible with the Christoffel-consistent factorization, for systems with revolute and prismatic joints.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 4 sources · topic: Lie-group kinematics and dynamics of robot arms (drafter's packet `q1-lie-kinematics`, confirmed at the gate)
