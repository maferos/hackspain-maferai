---
aliases: []
type: "source"
title: "Geometric Impedance Control on SE(3) for Robotic Manipulators"
citekey: "Seo2022geometric"
doi: "10.48550/arXiv.2211.07945"
arxiv: "2211.07945"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2211.07945"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Joohwan Seo", "Nikhil Potu Surya Prakash", "Alexander Rose", "Jongeun Choi", "Roberto Horowitz"]
sha256: ["624f9f5e6c553aa2fde1be9ebc1daea2ec77a9a21028c684cb040efa526f25d8"]
pdf: "Content/Papers/Seo2022geometric.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 65
---

📄 PDF: [[Seo2022geometric.pdf]]

> [!abstract] One-sentence summary
> The paper derives left-invariant position and velocity error vectors on SE(3) and builds two geometric impedance control laws with Lyapunov stability proofs, which reduce tracking errors versus a conventional spatial-frame impedance controller in a UR5e simulation.

## Abstract

After its introduction, impedance control has been utilized as a primary control scheme for robotic manipulation tasks that involve interaction with unknown environments. While impedance control has been extensively studied, the geometric structure of SE(3) for the robotic manipulator itself and its use in formulating a robotic task has not been adequately addressed. In this paper, we propose a differential geometric approach to impedance control. Given a left-invariant error metric in SE(3), the corresponding error vectors in position and velocity are first derived. We then propose the impedance control schemes that adequately account for the geometric structure of the manipulator in SE(3) based on a left-invariant potential function. The closed-loop stabilities for the proposed control schemes are verified using Lyapunov function-based analysis. The proposed control design clearly outperformed a conventional impedance control approach when tracking challenging trajectory profiles. (arXiv)

## 🧠 Key ideas (atomic)

- Impedance control was first proposed by Hogan in 1985 to solve the positioning problem of a manipulator end-effector. (Seo et al., 2022) `ev:cited` p. 1 ^seo2022geometric-001
- Prior work shows impedance control enables an engineering trade-off between positioning accuracy requirements and robustness against unmodeled interactions. (Seo et al., 2022) `ev:cited` p. 1 ^seo2022geometric-002
- To deal with unknown environments, impedance control is often combined with adaptive, behavior cloning or reinforcement learning algorithms in prior work. (Seo et al., 2022) `ev:cited` p. 1 ^seo2022geometric-003
- Tracking errors in Cartesian space impedance control are often calculated separately as translation and orientation errors in the spatial frame. (Seo et al., 2022) `ev:asserted` p. 1 ^seo2022geometric-004
- The authors state that most schemes separating translation and orientation errors do not adequately consider the geometry of SE(3). (Seo et al., 2022) `ev:asserted` p. 1 ^seo2022geometric-005
- Earlier impedance works using spatial springs on SE(3) did not provide results involving time-varying trajectories or a stability analysis. (Seo et al., 2022) `ev:cited` p. 1 ^seo2022geometric-006
- In prior controllers, desired and current Cartesian velocities are directly compared even though they lie in different tangent spaces of SE(3). (Seo et al., 2022) `ev:cited` p. 1 ^seo2022geometric-007
- Since SE(3) has no bi-invariant error metric, position error vectors need to be defined consistently with the selected error metric. (Seo et al., 2022) `ev:cited` p. 1 ^seo2022geometric-008
- The authors argue that using spatial frame-based error vectors for left-invariant metrics is inconsistent with the geometry of SE(3). (Seo et al., 2022) `ev:asserted` p. 1 ^seo2022geometric-009
- The paper defines position and velocity errors in the end-effector body frame, lying on its tangent space, before deriving impedance control laws. (Seo et al., 2022) `ev:asserted` p. 2 ^seo2022geometric-010
- The authors present the work as an extension of Lee et al. (2010) from SO(3) to SE(3) and to robotic manipulators. (Seo et al., 2022) `ev:asserted` p. 2 ^seo2022geometric-011
- Unlike Lee et al., which uses a scalar gain, the rotational potential function here uses a matrix impedance gain. (Seo et al., 2022) `ev:asserted` p. 2 ^seo2022geometric-012
- The authors state they present complete stability analyses for both controllers, which had previously been omitted for SE(3). (Seo et al., 2022) `ev:asserted` p. 2 ^seo2022geometric-013
- The authors argue that error vectors consistent with SE(3) tasks will be critical to learning variable impedance gains in assembly operations. (Seo et al., 2022) `ev:asserted` p. 2 ^seo2022geometric-014
- The paper considers manipulators with revolute joints, whose forward kinematics are written as a [[Product of exponentials formula|product of matrix exponentials]] of joint twists. (Seo et al., 2022) `ev:reported` p. 2 ^seo2022geometric-015
- The end-effector velocity in the body frame is computed from the joint velocities through the body Jacobian matrix. (Seo et al., 2022) `ev:reported` p. 2 ^seo2022geometric-016
- The manipulator dynamics are rewritten in an operational space formulation by mapping inertia, Coriolis and gravity terms through the body Jacobian. (Seo et al., 2022) `ev:reported` p. 3 ^seo2022geometric-017
- The analysis assumes the end-effector lies in a region of SE(3) where the body Jacobian is full-rank, that is, non-singular. (Seo et al., 2022) `ev:reported` p. 3 ^seo2022geometric-018
- The SE(3) error function is defined as half the squared Frobenius norm of the identity minus the relative configuration between desired and actual poses. (Seo et al., 2022) `ev:asserted` p. 3 ^seo2022geometric-019
- The error function equals the trace of the identity minus the relative rotation plus half the squared position error. (Seo et al., 2022) `ev:computed` p. 3 ^seo2022geometric-020
- The authors state that their error function is the non-weighted version of one error function proposed by Bullo and Murray (1999). (Seo et al., 2022) `ev:asserted` p. 3 ^seo2022geometric-021
- Park (1995) defines a comparable SE(3) distance but uses the bi-invariant logarithm-based metric for the SO(3) part. (Seo et al., 2022) `ev:cited` p. 3 ^seo2022geometric-022
- The authors show that the proposed SE(3) error function is left-invariant, unchanged under an arbitrary left translation of both configurations. (Seo et al., 2022) `ev:computed` p. 3 ^seo2022geometric-023
- As suggested by Park (1995), body-frame coordinates are natural to use for left-invariant error metrics in SE(3). (Seo et al., 2022) `ev:cited` p. 3 ^seo2022geometric-024
- The position error vector is derived by perturbing the configuration with a right translation, as Lee et al. did for SO(3). (Seo et al., 2022) `ev:computed` p. 3 ^seo2022geometric-025
- The desired body velocity is translated to the current configuration through an Adjoint map before the velocity error vector is formed. (Seo et al., 2022) `ev:computed` p. 3 ^seo2022geometric-026
- The authors show that the velocity error vector can be utilized to represent the error on the tangent space at the current configuration. (Seo et al., 2022) `ev:computed` p. 4 ^seo2022geometric-027
- Impedance control is treated as dissipative control design, using a Lyapunov function similar to the total mechanical energy of the system. (Seo et al., 2022) `ev:asserted` p. 4 ^seo2022geometric-028
- The potential function weights the error function with symmetric positive definite stiffness matrices for orientation and translation. (Seo et al., 2022) `ev:asserted` p. 4 ^seo2022geometric-029
- The weighting is motivated by recent variable impedance techniques that require multiple and varying compliance gains along different coordinates. (Seo et al., 2022) `ev:cited` p. 4 ^seo2022geometric-030
- The authors note that an intuitive impedance law using gain-weighted error vectors does not act in the gradient direction of the Lyapunov function. (Seo et al., 2022) `ev:computed` p. 4 ^seo2022geometric-031
- The geometric impedance control law instead uses the elastic force derived from the left-invariant potential function, following Bullo and Murray. (Seo et al., 2022) `ev:asserted` p. 4 ^seo2022geometric-032
- Theorem 4 shows the Lyapunov function of the closed loop with the first geometric law is dissipative without external disturbance. (Seo et al., 2022) `ev:computed` p. 4 ^seo2022geometric-033
- The dissipative property shows that the closed-loop system under the first geometric law is at least stable in the sense of Lyapunov. (Seo et al., 2022) `ev:computed` p. 4 ^seo2022geometric-034
- Theorem 5 proves, with a strict Lyapunov function, that the desired-trajectory equilibrium of the first law is asymptotically stable in the reachable set. (Seo et al., 2022) `ev:computed` p. 5 ^seo2022geometric-035
- The strict Lyapunov proof requires sufficiently large gains or a sufficiently small epsilon to make the matrix Q positive definite. (Seo et al., 2022) `ev:computed` p. 5 ^seo2022geometric-036
- A second geometric law uses a reference velocity and reference acceleration, following exact compensation tracking designs from Sadegh and Horowitz. (Seo et al., 2022) `ev:asserted` p. 5 ^seo2022geometric-037
- Theorem 6 proves that the equilibrium of the closed loop under the second geometric control law is asymptotically stable in the reachable set. (Seo et al., 2022) `ev:computed` p. 5 ^seo2022geometric-038
- With the second control law the effective end-effector stiffness changes, so the stiffness gains should be chosen with care. (Seo et al., 2022) `ev:asserted` p. 5 ^seo2022geometric-039
- When the scalar gain lambda approaches zero, the second control law becomes identical to the first geometric control law. (Seo et al., 2022) `ev:computed` p. 5 ^seo2022geometric-040
- The stability of the first law is restricted by the selection of trajectories and gains through its dependence on matrix norms. (Seo et al., 2022) `ev:asserted` p. 6 ^seo2022geometric-041
- The authors state that the second law gives more generalized stability results because its gain does not depend on those matrix norms. (Seo et al., 2022) `ev:asserted` p. 6 ^seo2022geometric-042
- Simulations use a UR5e robot model implemented in Matlab R2021a with the robotics toolbox of Corke (2002). (Seo et al., 2022) `ev:reported` p. 6 ^seo2022geometric-043
- The benchmark is a conventional impedance controller using spatial-frame error vectors that does not consider geometrical aspects of SE(3). (Seo et al., 2022) `ev:reported` p. 6 ^seo2022geometric-044
- The authors describe the benchmark as very similar to Caccavale et al. (1999), differing only in the rotational error representation. (Seo et al., 2022) `ev:asserted` p. 6 ^seo2022geometric-045
- Only the first geometric control law was simulated, since it enables a fair comparison with the benchmark controller. (Seo et al., 2022) `ev:reported` p. 6 ^seo2022geometric-046
- Both controllers were given the same desired impedance gains and started from the same initial condition in the simulation. (Seo et al., 2022) `ev:reported` p. 6 ^seo2022geometric-047
- In the simulation, the translational stiffness was set to diag([200, 60, 80]) with the damping gain kd = 50. (Seo et al., 2022) `ev:reported` p. 6 ^seo2022geometric-048
- In the simulation, the rotational stiffness matrix was set to diag([10, 30, 100]) for both compared impedance controllers. (Seo et al., 2022) `ev:reported` p. 6 ^seo2022geometric-049
- The simulations use a dynamic trajectory with rapid motion, combining sinusoidal desired positions with a constant desired orientation. (Seo et al., 2022) `ev:reported` p. 6 ^seo2022geometric-050
- Both the proposed and benchmark controllers showed perfect trajectory tracking performance once they had converged in the simulation. (Seo et al., 2022) `ev:measured` p. 6 ^seo2022geometric-051
- The proposed control law improved the reduction of initial errors compared with the benchmark, especially in the translational part. (Seo et al., 2022) `ev:measured` p. 6 ^seo2022geometric-052
- The RMS tracking error along x was 0.0137 for the proposed controller versus 0.0317 for the benchmark. (Seo et al., 2022) `ev:measured` p. 6 ^seo2022geometric-053
- The RMS tracking error along y was 0.1256 for the proposed controller versus 0.1992 for the benchmark. (Seo et al., 2022) `ev:measured` p. 6 ^seo2022geometric-054
- The RMS tracking error along z was 0.0178 for the proposed controller versus 0.0183 for the benchmark. (Seo et al., 2022) `ev:measured` p. 6 ^seo2022geometric-055
- The RMS value of the potential function was 6.3624 for the proposed controller versus 6.5693 for the benchmark. (Seo et al., 2022) `ev:measured` p. 6 ^seo2022geometric-056
- The RMS value of the Lyapunov function was 6.6556 for the proposed controller versus 7.2622 for the benchmark. (Seo et al., 2022) `ev:measured` p. 6 ^seo2022geometric-057
- The authors attribute the gain mainly to the proposed law reducing translational and orientational errors simultaneously rather than separately. (Seo et al., 2022) `ev:asserted` p. 6 ^seo2022geometric-058
- The Matlab code implementing the proposed controller is provided in a public GitHub repository by the first author. (Seo et al., 2022) `ev:reported` p. 6 ^seo2022geometric-059
- A PD-like control with gravity compensation can be utilized when the Jacobian matrix is numerically near singular, the authors remark. (Seo et al., 2022) `ev:asserted` p. 6 ^seo2022geometric-060
- The authors state this PD-like form solves end-effector positioning even without dynamic parameters and without solving inverse kinematics. (Seo et al., 2022) `ev:asserted` p. 6 ^seo2022geometric-061
- The authors conclude that the stability analysis shows the closed-loop system with the geometric impedance control is asymptotically stable. (Seo et al., 2022) `ev:asserted` p. 7 ^seo2022geometric-062
- As future work, the authors plan to combine the geometric impedance control with reinforcement learning for robotic manipulation tasks. (Seo et al., 2022) `ev:asserted` p. 7 ^seo2022geometric-063
- The authors expect an improvement in performance over state-of-the-art methods once the geometric controller is combined with learning. (Seo et al., 2022) `ev:asserted` p. 7 ^seo2022geometric-064
- The authors also plan to study robotic tasks better encoded as velocity fields instead of desired trajectories. (Seo et al., 2022) `ev:asserted` p. 7 ^seo2022geometric-065

## 🎯 Contributions

## 📖 Glossary

- **SE(3)** — Special Euclidean group of rigid-body poses combining a rotation and a translation.
- **Left-invariant error function** — Error unchanged when both actual and desired poses are left-multiplied by one transform.
- **Impedance control** — Control regulating the mass-spring-damper relation between end-effector motion and contact forces.
- **Adjoint map** — Linear map transforming a twist between coordinate frames of SE(3).
- **Body Jacobian** — Matrix mapping joint velocities to end-effector velocity expressed in the body frame.
- **Elastic force fg** — Wrench obtained as the gradient of the SE(3) potential function in the cotangent space.
- **Variable impedance control** — Impedance control whose stiffness and damping gains change over time or task.

## ❓ Open questions

- Does the geometric controller keep its advantage on a physical robot with model errors and contact, rather than in a noise-free simulation?
- How does the second (exact compensation) control law perform in simulation, since only the first law was benchmarked?
- Does using left-invariant error vectors actually speed up or stabilise learning of variable impedance gains with reinforcement learning?
- How sensitive is the tracking advantage to the chosen gains and trajectory, given a single scenario was reported?

## 📝 Notes on reading

- Version read: arXiv 2211.07945v4 (5 Mar 2025), marked as the final version presented at IFAC World Congress 2023; the identifier is the arXiv preprint.
- Figures 1 and 2 (p. 6) plot x, y, z tracking and a bird-eye x-y view for t = 0 to 10 s; described only, no claims from them.
- Equations are extracted with broken layout (matrices, hats, subscripts); claims describe definitions in words rather than transcribing formulas.
- On p. 3 the text says the right translation of the error function does not satisfy equation (14), which appears to mean the invariance relation (15).
- The abstract says the proposed design clearly outperformed the benchmark, but Table 1 shows near-identical RMS z error (0.0178 vs 0.0183) and only a single simulated scenario.
- Table 1 gives RMS values without units.

## Suggested new concepts

- Geometric impedance control — a family of SE(3)-consistent impedance controllers that recurs across manipulation and learning papers.
- Left-invariant error metric on SE(3) — the choice of error metric and body-frame error vectors underpins controller consistency.
- Variable impedance control — stiffness and damping as learned actions links control and reinforcement learning literature.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H3.** Control de impedancia con potencial invariante a izquierda en SE(3) para ejecutar trayectorias con contacto seguro.
