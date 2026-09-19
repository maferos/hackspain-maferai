---
aliases: []
type: topic
parent: Geometry of motion and representation
created: 2026-09-19
---

## Scope

How the motion of articulated robots is modelled with screw and Lie group theory: forward kinematics as products of joint-screw exponentials, the choice of twist representation, recursive O(n) inverse and forward dynamics and their derivatives, Lie-algebraic tools such as the Baker-Campbell-Hausdorff formula used to linearise or differentiate motion on SE(3) and SO(3), and kinematic performance descriptors such as the manipulability ellipsoid. It does not cover learning or optimisation on manifolds in general (Riemannian optimisation, Riemannian motion policies, diffusion or flow models on Lie groups), which belong to the Riemannian and Lie-group methods area, nor rotation representations inside neural networks.

## Concepts

- [[Product of exponentials formula]] — A way of writing the forward kinematics of an open chain as a product of matrix exponentials of the joint screws, one per joint, times a reference configuration, without needing joint frames or Denavit-Hartenberg parameters.
- [[Twist representations]] — The four ways of expressing a rigid body's velocity as a six-vector (body-fixed, spatial, hybrid and mixed), which differ in the point where velocity is measured and the frame it is resolved in, and which change the cost of recursive kinematics and dynamics algorithms.
- [[Recursive Newton-Euler algorithm]] — The standard O(n) inverse dynamics method for a kinematic tree, which propagates velocities and accelerations outward from the base in a forward pass and then accumulates wrenches back toward the base to obtain the joint forces.
- [[Manipulability ellipsoid]] — An ellipsoid, given by a symmetric positive definite matrix such as J J^T, that describes how easily a robot in a given joint configuration can move or exert force along each task direction.
- [[Baker-Campbell-Hausdorff formula]] — A series of nested Lie brackets that expresses the logarithm of a product of two group exponentials as a single Lie algebra element, used to expand, linearise or differentiate motion on matrix Lie groups.

## Subtopics

## Related topics

## ❓ Open questions

## Problems

- none yet: no problem names this topic as its topic

## History

- 2026-09-19 · Eki Gonzalez Flamarique · parent: root — new area for concepts promoted from the gap-research batch (04_huecos_y_ampliacion), confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · parent: root → Geometry of motion and representation — grouped under the request's three axes
