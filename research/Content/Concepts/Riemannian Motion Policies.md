---
aliases: ["RMP"]
type: concept
element_type: method
topic: "[[Riemannian and Lie-group methods for robot motion and optimization]]"
topics: ["[[Riemannian and Lie-group methods for robot motion and optimization]]"]
created: 2026-09-18
---

## Working definition

A Riemannian motion policy pairs a desired-acceleration policy for a subtask with a state-dependent positive semi-definite metric that weights its directional importance, so that many subtask policies can be combined into one reactive robot controller.

## Evidence

- [[Cheng2018rmpflow - RMPflow A Computational Graph for Automatic Motion Policy#^cheng2018rmpflow-015]] — An RMP pairs a continuous desired-acceleration policy with a differentiable positive semi-definite inertia matrix that defines its directional importance.
- [[Cheng2018rmpflow - RMPflow A Computational Graph for Automatic Motion Policy#^cheng2018rmpflow-023]] — Barrier-type collision avoidance RMPs use velocity-dependent inertia matrices, so the RMP can be turned off when the robot heads away.
- [[Cheng2018rmpflow - RMPflow A Computational Graph for Automatic Motion Policy#^cheng2018rmpflow-026]] — The authors show RMPflow is coordinate-free, meaning subtask RMPs designed for one robot can transfer to another with the same task-space behaviors.
- [[Jaquier2022riemannian - Riemannian geometry as a unifying theory for robot motion#^jaquier2022riemannian-044]] — The authors hypothesize that robot motion may be adapted to external conditions by artificially shaping the Riemannian metric, inspired by Riemannian motion policies
- [[Wyk2021geometric - Geometric Fabrics Generalizing Classical Mechanics to#^wyk2021geometric-002]] — Earlier work on Riemannian Motion Policies demonstrated that removing the restrictions of classical mechanics can result in powerful design tools.
- [[Wyk2021geometric - Geometric Fabrics Generalizing Classical Mechanics to#^wyk2021geometric-003]] — The authors state that RMPs sacrifice theoretical insight for expressivity, forcing practitioners to gain experience before becoming proficient.
- [[Wyk2021geometric - Geometric Fabrics Generalizing Classical Mechanics to#^wyk2021geometric-009]] — The authors now view Geometric Dynamical Systems, an earlier stable class of RMPs, as better expressed as Finsler systems, which are unbent fabrics.
- [[Wyk2021geometric - Geometric Fabrics Generalizing Classical Mechanics to#^wyk2021geometric-065]] — Earlier RMP results used high gains on forcing potentials and damping terms to reject the irrelevant geometric terms that resulted from coupled metrics.
- [[Wyk2021geometric - Geometric Fabrics Generalizing Classical Mechanics to#^wyk2021geometric-059]] — The robot reached 16 targets with the geometric fabric policy, compared with 11 targets with the RMP, in the dynamic obstacle task.
- [[Wyk2021geometric - Geometric Fabrics Generalizing Classical Mechanics to#^wyk2021geometric-060]] — The geometric fabric policy yielded a 0.4% collision rate versus 8.18% for the RMP, measured as the percentage of time steps in collision.
- [[Wyk2021geometric - Geometric Fabrics Generalizing Classical Mechanics to#^wyk2021geometric-062]] — The authors state that the RMP had to balance repulsion against target acquisition, a compromise that resulted in diminished performance.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 3 sources · topic: Riemannian and Lie-group methods for robot motion and optimization (drafter's packet `p2-riemannian-robot-motion`, confirmed at the gate)
