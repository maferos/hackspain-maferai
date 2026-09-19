---
aliases: []
type: "source"
title: "Geometry-aware Manipulability Learning, Tracking and Transfer"
citekey: "Jaquier2018geometry"
doi: "10.48550/arXiv.1811.11050"
arxiv: "1811.11050"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1811.11050"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Noémie Jaquier", "Leonel Rozo", "Darwin G. Caldwell", "Sylvain Calinon"]
sha256: ["f6bed65209b78d575171b5a71182df50d963fd9d600f49b378e9f79d080fac19"]
pdf: "Content/Papers/Jaquier2018geometry.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Jaquier2018geometry.pdf]]

> [!abstract] One-sentence summary
> The paper learns manipulability ellipsoid profiles from demonstrations with a GMM/GMR on the SPD manifold and tracks them with exponentially stable geometry-aware controllers, enabling transfer of posture-dependent task requirements between robots of different kinematics.

## Abstract

Body posture influences human and robots performance in manipulation tasks, as appropriate poses facilitate motion or force exertion along different axes. In robotics, manipulability ellipsoids arise as a powerful descriptor to analyze, control and design the robot dexterity as a function of the articulatory joint configuration. This descriptor can be designed according to different task requirements, such as tracking a desired position or apply a specific force. In this context, this paper presents a novel \emph{manipulability transfer} framework, a method that allows robots to learn and reproduce manipulability ellipsoids from expert demonstrations. The proposed learning scheme is built on a tensor-based formulation of a Gaussian mixture model that takes into account that manipulability ellipsoids lie on the manifold of symmetric positive definite matrices. Learning is coupled with a geometry-aware tracking controller allowing robots to follow a desired profile of manipulability ellipsoids. Extensive evaluations in simulation with redundant manipulators, a robotic hand and humanoids agents, as well as an experiment with two real dual-arm systems validate the feasibility of the approach. (arXiv)

## 🧠 Key ideas (atomic)

- The [[Manipulability ellipsoid|manipulability ellipsoid]] serves as a geometric descriptor of the ability to perform motion and exert force along task directions in a joint configuration. (Jaquier et al., 2018) `ev:cited` p. 1 ^jaquier2018geometry-001
- Lee (1989) stated that solely maximizing the ellipsoid volume to achieve high dexterity in motion may cause a reverse effect on flexibility in force. (Jaquier et al., 2018) `ev:cited` p. 1 ^jaquier2018geometry-002
- The authors argue that predetermining task-dependent manipulability, as in earlier work, requires a demanding analysis that becomes impractical for large sets of tasks. (Jaquier et al., 2018) `ev:asserted` p. 2 ^jaquier2018geometry-003
- Manipulability polytopes provide a more accurate estimate of robot velocity or force generation capabilities than [[Manipulability ellipsoid|manipulability ellipsoids]], according to the cited literature. (Jaquier et al., 2018) `ev:cited` p. 2 ^jaquier2018geometry-004
- The authors state that the calculation of manipulability polytopes is computationally expensive compared with the easily computed [[Manipulability ellipsoid|manipulability ellipsoids]]. (Jaquier et al., 2018) `ev:asserted` p. 2 ^jaquier2018geometry-005
- The paper casts manipulability-based posture variation as a transfer problem in which a teacher demonstrates a time-varying manipulability profile that a learner reproduces. (Jaquier et al., 2018) `ev:asserted` p. 2 ^jaquier2018geometry-006
- Demonstrated manipulability sequences are encoded with a tensor-based Gaussian mixture model and regression that account for ellipsoids lying on the SPD manifold. (Jaquier et al., 2018) `ev:reported` p. 2 ^jaquier2018geometry-007
- Manipulability tracking is formulated like classical inverse kinematics, establishing a first-order differential relationship between the [[Manipulability ellipsoid|manipulability ellipsoid]] and the robot joints. (Jaquier et al., 2018) `ev:reported` p. 2 ^jaquier2018geometry-008
- A model learned from an unplugging task kinesthetically demonstrated to a 14-DoF dual-arm robot is transferred to a different dual-arm system. (Jaquier et al., 2018) `ev:reported` p. 2 ^jaquier2018geometry-009
- The paper defines the [[Manipulability ellipsoid|velocity manipulability ellipsoid]] as J J^T, whose major axis is aligned with the eigenvector of the maximum eigenvalue. (Jaquier et al., 2018) `ev:reported` p. 3 ^jaquier2018geometry-010
- The major axis of the [[Manipulability ellipsoid|velocity manipulability ellipsoid]] indicates the direction of greater velocity generation, which is also the direction of greater perturbation sensitivity. (Jaquier et al., 2018) `ev:cited` p. 3 ^jaquier2018geometry-011
- The set of SPD matrices is not a vector space since it is not closed under addition and scalar product. (Jaquier et al., 2018) `ev:cited` p. 3 ^jaquier2018geometry-012
- A tensor-variate normal distribution maximizing entropy in the tangent space is extended to the SPD manifold to define a Gaussian mixture model. (Jaquier et al., 2018) `ev:reported` p. 5 ^jaquier2018geometry-013
- Gaussian mixture regression on the SPD manifold approximates the conditional distribution by a single Gaussian whose mean is computed iteratively in its tangent space. (Jaquier et al., 2018) `ev:reported` p. 6 ^jaquier2018geometry-014
- In the illustrative example, a simulated 3-DoF teacher robot followed a C-shape trajectory four times to provide demonstrations. (Jaquier et al., 2018) `ev:reported` p. 6 ^jaquier2018geometry-015
- A simulated 5-DoF student robot followed the Cartesian trajectory from classical regression while matching desired manipulability ellipsoids as a secondary task. (Jaquier et al., 2018) `ev:reported` p. 6 ^jaquier2018geometry-016
- The manipulability Jacobian is a tensor representing the linear sensitivity of [[Manipulability ellipsoid|manipulability ellipsoid]] changes to the joint velocity of the robot. (Jaquier et al., 2018) `ev:reported` p. 7 ^jaquier2018geometry-017
- Manipulability Jacobians are derived for the velocity, force and [[Manipulability ellipsoid|dynamic manipulability ellipsoids]], the last using the robot inertia matrix. (Jaquier et al., 2018) `ev:computed` p. 7 ^jaquier2018geometry-018
- The main-task velocity controller maps the logarithmic map between current and desired ellipsoids through the pseudoinverse of the manipulability Jacobian. (Jaquier et al., 2018) `ev:reported` p. 8 ^jaquier2018geometry-019
- For secondary manipulability tracking, the geometry-aware joint velocity command is projected into the nullspace of a Cartesian position controller. (Jaquier et al., 2018) `ev:reported` p. 8 ^jaquier2018geometry-020
- With a simulated 4-DoF planar robot, manipulability tracking as main task reduced the distance to the desired ellipsoid from 1.342 to 0.199. (Jaquier et al., 2018) `ev:measured` p. 8 ^jaquier2018geometry-021
- With manipulability tracking as a secondary objective at a fixed end-effector position, the distance decreased from 2.194 to 0.955. (Jaquier et al., 2018) `ev:measured` p. 8 ^jaquier2018geometry-022
- A Lyapunov analysis based on the affine-invariant distance shows that the proposed velocity-based manipulability tracking controller is exponentially stable. (Jaquier et al., 2018) `ev:computed` p. 9 ^jaquier2018geometry-023
- When manipulability tracking is secondary, the controller does not influence main-task stability because redundancy resolution is carried out in the nullspace. (Jaquier et al., 2018) `ev:asserted` p. 9 ^jaquier2018geometry-024
- An acceleration-based controller resembling a proportional-derivative law tracks desired manipulability and manipulability velocity profiles using the logarithmic map. (Jaquier et al., 2018) `ev:reported` p. 9 ^jaquier2018geometry-025
- Actuator limits are included by weighting the Jacobian with a diagonal matrix of maximum joint velocities or maximum joint torques. (Jaquier et al., 2018) `ev:reported` p. 10 ^jaquier2018geometry-026
- In simulated manipulability tracking, joint q1 moved significantly when given the highest velocity limit among the joints. (Jaquier et al., 2018) `ev:measured` p. 10 ^jaquier2018geometry-027
- The controller gain is proposed as a full SPD matrix proportional to the matricized precision tensor, the inverse of the observed covariance. (Jaquier et al., 2018) `ev:reported` p. 10 ^jaquier2018geometry-028
- With a 10:1 precision ratio on one ellipsoid axis, the robot first fitted that axis before matching the whole manipulability ellipsoid. (Jaquier et al., 2018) `ev:measured` p. 11 ^jaquier2018geometry-029
- With a 3:1 precision ratio on the axis correlation, the robot first aligned its manipulability with the desired ellipsoid orientation. (Jaquier et al., 2018) `ev:measured` p. 11 ^jaquier2018geometry-030
- In the learned C-shape task, the variability-based gain enforced higher precision only at the beginning and end, lowering control efforts in between. (Jaquier et al., 2018) `ev:measured` p. 11 ^jaquier2018geometry-031
- A simulated 6-DoF planar robot tracked a desired manipulability as main task while holding its first joint through the manipulability Jacobian nullspace. (Jaquier et al., 2018) `ev:measured` p. 12 ^jaquier2018geometry-032
- With a 1-state GMM, geometry-aware and Euclidean regression profiles were similar near the component mean but diverged when moving away from it. (Jaquier et al., 2018) `ev:measured` p. 12 ^jaquier2018geometry-033
- The geometry-aware regression extrapolated the rotating behavior of the demonstrated ellipsoids because the recovered trajectory follows a geodesic on the SPD manifold. (Jaquier et al., 2018) `ev:measured` p. 12 ^jaquier2018geometry-034
- In the second main-task test, the Euclidean controller induced a sudden joint configuration change and an abrupt increase in manipulability error. (Jaquier et al., 2018) `ev:measured` p. 13 ^jaquier2018geometry-035
- The Cholesky-based Euclidean tracking controller did not converge to the desired manipulability ellipsoid in either of the two main-task tests. (Jaquier et al., 2018) `ev:measured` p. 13 ^jaquier2018geometry-036
- The Cholesky-Jacobian-based controller converged in both main-task tests but showed a poor convergence rate compared to the geometry-aware approach. (Jaquier et al., 2018) `ev:measured` p. 13 ^jaquier2018geometry-037
- In the second main-task test, final distances were 1.4e−4 for the geometry-aware controller versus 0.455 for the Cholesky-Jacobian controller. (Jaquier et al., 2018) `ev:measured` p. 14 ^jaquier2018geometry-038
- In the first main-task test, the geometry-aware controller reached a final distance of 6e−5, versus 1.3e−4 for the Euclidean controller. (Jaquier et al., 2018) `ev:measured` p. 14 ^jaquier2018geometry-039
- Even with gains lowered to 0.05I, both Euclidean formulations produced sudden joint changes at similar locations along the manipulability path. (Jaquier et al., 2018) `ev:measured` p. 14 ^jaquier2018geometry-040
- The secondary-task comparison added the gradient-based approach of Rozo et al., which minimizes a Stein divergence cost with a scalar gain. (Jaquier et al., 2018) `ev:reported` p. 15 ^jaquier2018geometry-041
- In the two redundancy resolution tests, geometry-aware final distances were 0.416 and 1.101, versus 0.436 and 1.110 for the gradient-based method. (Jaquier et al., 2018) `ev:measured` p. 15 ^jaquier2018geometry-042
- The authors suggest the speed difference may stem from the manipulability Jacobian being more informative about the robot kinematics. (Jaquier et al., 2018) `ev:asserted` p. 16 ^jaquier2018geometry-043
- The Euclidean redundancy controller sometimes converged slightly faster than the proposed method but showed unstable behaviors in other configurations. (Jaquier et al., 2018) `ev:measured` p. 16 ^jaquier2018geometry-044
- Unlike the gradient-based method with a scalar gain, the proposed controller can exploit task variability through a 4th-order covariance tensor gain. (Jaquier et al., 2018) `ev:asserted` p. 16 ^jaquier2018geometry-045
- With manipulability volume maximization, the main ellipsoid axis was often perpendicular to the direction of motion of the 8-DoF planar robot. (Jaquier et al., 2018) `ev:measured` p. 17 ^jaquier2018geometry-046
- The volume maximization approach became unstable when the velocity tracking gain was increased to achieve higher Cartesian velocities. (Jaquier et al., 2018) `ev:measured` p. 17 ^jaquier2018geometry-047
- The robot tracking a desired [[Manipulability ellipsoid|manipulability ellipsoid]] successfully completed the task when higher Cartesian velocities were required. (Jaquier et al., 2018) `ev:measured` p. 17 ^jaquier2018geometry-048
- Compatibility index maximization favored robot configurations that may be close to singularities, with flat and largely elongated ellipsoids. (Jaquier et al., 2018) `ev:measured` p. 17 ^jaquier2018geometry-049
- Simulation evaluations include an Allegro hand with four 4-DoF fingers and NAO and Centauro robots with 25 and 39 DoFs. (Jaquier et al., 2018) `ev:reported` p. 17 ^jaquier2018geometry-050
- For the Allegro hand, the experimenter designed the desired velocity manipulability ellipsoid as a medium-size isotropic ellipsoid. (Jaquier et al., 2018) `ev:reported` p. 18 ^jaquier2018geometry-051
- Manipulability tracking with the Allegro hand was achieved only partially because the hand also had to maintain the initial grasp. (Jaquier et al., 2018) `ev:measured` p. 18 ^jaquier2018geometry-052
- Both Centauro and NAO tracked the desired center of mass manipulability as precisely as possible without compromising the balancing task. (Jaquier et al., 2018) `ev:measured` p. 19 ^jaquier2018geometry-053
- Kinesthetic demonstrations on Baxter aligned the main axis of the dual-arm [[Manipulability ellipsoid|force manipulability ellipsoid]] with the cable extraction direction. (Jaquier et al., 2018) `ev:reported` p. 19 ^jaquier2018geometry-054
- Baxter tracked the desired manipulability ellipsoid while maintaining the required relative distance between its end-effectors during unplugging reproduction. (Jaquier et al., 2018) `ev:measured` p. 20 ^jaquier2018geometry-055
- Manipulability matching on the two Panda robots was not exact, which the authors attribute to physical differences such as arm base positions. (Jaquier et al., 2018) `ev:measured` p. 20 ^jaquier2018geometry-056
- The authors state that tracking precision for a secondary manipulability objective strongly depends on the robot's number of degrees of freedom. (Jaquier et al., 2018) `ev:asserted` p. 20 ^jaquier2018geometry-057
- The tracking approach is local, so its convergence depends on the current robot configuration, which may sometimes limit performance. (Jaquier et al., 2018) `ev:asserted` p. 21 ^jaquier2018geometry-058
- Future work will explore manipulability transfer between humans and robots, building on a statistical analysis of human manipulability ellipsoids. (Jaquier et al., 2018) `ev:asserted` p. 21 ^jaquier2018geometry-059
- The authors plan to optimize the desired manipulability as a function of the learner robot to exploit its capabilities. (Jaquier et al., 2018) `ev:asserted` p. 21 ^jaquier2018geometry-060

## 🎯 Contributions

## 📖 Glossary

- **Manipulability ellipsoid** — SPD matrix describing a robot's velocity or force capability along task directions.
- **SPD manifold** — Riemannian manifold of symmetric positive definite matrices, the interior of a convex cone.
- **Affine-invariant distance** — Riemannian distance between SPD matrices based on the matrix logarithm.
- **Exponential / logarithmic map** — Mappings between the SPD manifold and its tangent space at a point.
- **Parallel transport** — Moves tangent-space elements between tangent spaces while preserving their angles.
- **Manipulability Jacobian** — Tensor relating joint velocities to the time derivative of the manipulability ellipsoid.
- **Dynamic manipulability** — Ellipsoid measuring end-effector acceleration capability for given joint torques, using the inertia matrix.
- **Compatibility index** — Distance from ellipsoid center to its surface along a specified task direction.
- **GMR** — Gaussian mixture regression: conditioning a Gaussian mixture model to retrieve outputs from inputs.

## ❓ Open questions

- How well does manipulability transfer work from humans to robots, rather than robot-to-robot?
- Can the desired manipulability be optimized for the learner when it can exceed the teacher's manipulability?
- Can the local tracking method be complemented by a search over initial postures to avoid poor convergence?
- How much would balancing controllers that allow foot repositioning improve center of mass manipulability tracking on legged robots?
- How does the approach behave with more GMM components and higher-dimensional ellipsoids in real demonstrations?

## 📝 Notes on reading

Read the arXiv v5 preprint (1 Mar 2021, Sage template, 24 pages) of arXiv:1811.11050; the later journal version may differ. The PDF abstract says "this article" where the registry abstract says "this paper". Most results are shown only in figures (Figs. 3-20); only Tables 1-3 give numeric distances. Table 2 includes "after jump" columns for Euclidean (2.997 / 3.977) and Cholesky (3.385 / 1.944) controllers in the second test; the column-to-value alignment in the extracted text was read as Euclidean, after jump, Cholesky, after jump, Cholesky Jacobian, geometry-aware. The NAO sentence on p. 19 ("both the balancing task and the lower number of DoF constrain NAO to closely match the desired manipulability") appears to mean the constraints prevent close matching; not claimed. Computational times (3.5 ms and 4.2 ms) were measured with non-optimized Matlab code on a 2.7GHz laptop. Equations throughout are partially garbled by extraction and were not claimed beyond their described role. The experimental real-robot evaluation is qualitative (figures only).

## Suggested new concepts

- Manipulability ellipsoid — central robotics descriptor reused across control, learning and design papers.
- Riemannian geometry of SPD matrices — underpins geometry-aware learning and control of covariance-like quantities.
- Manipulability transfer — learning posture-dependent task requirements from demonstrations beyond trajectories and forces.
- Gaussian mixture regression on manifolds — probabilistic learning from demonstration for non-Euclidean data.
- Nullspace redundancy resolution — standard mechanism for secondary objectives in redundant robots.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H1.** Trata el elipsoide de manipulabilidad de Yoshikawa como matriz SPD y lo aprende y sigue con el Jacobiano de manipulabilidad en la variedad SPD.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
