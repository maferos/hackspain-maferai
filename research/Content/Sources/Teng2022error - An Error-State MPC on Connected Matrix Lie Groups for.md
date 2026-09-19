---
aliases: []
type: "source"
title: "An Error-State MPC on Connected Matrix Lie Groups for Legged Robot Control"
citekey: "Teng2022error"
doi: "10.48550/arXiv.2203.08728"
arxiv: "2203.08728"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2203.08728"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Sangli Teng", "Dianhao Chen", "William Clark", "Maani Ghaffari"]
sha256: ["2a21df1d96f73d22c957281d94b9abd1b3e2bed2d3b7f7383755c6aa0094ce24"]
pdf: "Content/Papers/Teng2022error.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[Teng2022error.pdf]]

> [!abstract] One-sentence summary
> The paper linearizes rigid-body tracking error dynamics in the Lie algebra to build a convex error-state MPC on SE(3), which converges faster in orientation than variational-based MPC in simulation and on the Mini Cheetah quadruped.

## Abstract

This paper reports on a new error-state Model Predictive Control (MPC) approach to connected matrix Lie groups for robot control. The linearized tracking error dynamics and the linearized equations of motion are derived in the Lie algebra. Moreover, given an initial condition, the linearized tracking error dynamics and equations of motion are globally valid and evolve independently of the system trajectory. By exploiting the symmetry of the problem, the proposed approach shows faster convergence of rotation and position simultaneously than the state-of-the-art geometric variational MPC based on variational-based linearization. Numerical simulation on tracking control of a fully-actuated 3D rigid body dynamics confirms the benefits of the proposed approach compared to the baselines. Furthermore, the proposed MPC is also verified in pose control and locomotion experiments on a quadrupedal robot MIT Mini Cheetah. (arXiv)

## 🧠 Key ideas (atomic)

- The authors develop a geometric error-state MPC for tracking control of systems evolving on a matrix Lie group, specifically SE(3) rigid body motion. (Teng et al., 2022) `ev:asserted` p. 2 ^teng2022error-001
- Euler angle orientation representations are known for singularities in some configurations, according to prior work cited by the authors. (Teng et al., 2022) `ev:cited` p. 1 ^teng2022error-002
- Quaternion representations of robot orientation have ambiguities in representing attitudes, as reported in prior work on rotational stabilization. (Teng et al., 2022) `ev:cited` p. 1 ^teng2022error-003
- Existing geometric MPC approaches either do not exploit SE(3) pose-control symmetry or assume the current trajectory is close to the desired one. (Teng et al., 2022) `ev:cited` p. 1 ^teng2022error-004
- The authors state that the assumption of the current trajectory being close to the desired trajectory might not be satisfied in practice. (Teng et al., 2022) `ev:asserted` p. 1 ^teng2022error-005
- The Euler angle-based convex MPC for quadrupedal locomotion planning needs to assume zero pitch and roll angle. (Teng et al., 2022) `ev:cited` p. 1 ^teng2022error-006
- The linearized state matrix of a representation-free MPC linearized at the current operating point depends on the orientation. (Teng et al., 2022) `ev:cited` p. 2 ^teng2022error-007
- The authors state that this orientation dependence can be avoided by exploiting the symmetry of the system, as done in their work. (Teng et al., 2022) `ev:asserted` p. 2 ^teng2022error-008
- The linearized tracking error dynamics and equations of motion are derived in the Lie algebra, the tangent space at the identity. (Teng et al., 2022) `ev:computed` p. 2 ^teng2022error-009
- Given an initial condition, the linearized dynamics are claimed to be globally valid and to evolve independently of the system trajectory. (Teng et al., 2022) `ev:asserted` p. 2 ^teng2022error-010
- An implementation of the proposed MPC is available for download from the UMich-CURLY Error-State-MPC GitHub repository. (Teng et al., 2022) `ev:reported` p. 2 ^teng2022error-011
- The tracking error is defined as the product of the inverse desired state and the actual state on the Lie group. (Teng et al., 2022) `ev:reported` p. 3 ^teng2022error-012
- The error dynamics are linearized using first-order approximations of the exponential and adjoint maps, dropping second-order terms. (Teng et al., 2022) `ev:computed` p. 3 ^teng2022error-013
- The nonlinear twist dynamics are approximated by a series expansion around an operating point, with the Jacobian obtained via the chain rule. (Teng et al., 2022) `ev:computed` p. 3 ^teng2022error-014
- The authors lift the problem to the Lie algebra so that usual algebraic manipulations and existing QP solvers can be used. (Teng et al., 2022) `ev:asserted` p. 3 ^teng2022error-015
- In the experiments, the linearization operating point is set at the current system states rather than the reference trajectory. (Teng et al., 2022) `ev:reported` p. 4 ^teng2022error-016
- Setting the operating point at the current states exhibits higher stability, as shown in earlier representation-free MPC work. (Teng et al., 2022) `ev:cited` p. 4 ^teng2022error-017
- The cost function regulates the Lie algebra tracking error and its derivative rather than the difference between desired and actual twists. (Teng et al., 2022) `ev:reported` p. 4 ^teng2022error-018
- The authors argue that velocity vectors at different locations on a Lie group cannot be compared directly without a transport map. (Teng et al., 2022) `ev:asserted` p. 4 ^teng2022error-019
- The discrete-time error-state MPC is a quadratic programming problem that can be solved efficiently, for example using OSQP. (Teng et al., 2022) `ev:asserted` p. 4 ^teng2022error-020
- For simplicity, the experiments and simulations use Euler first-order integration to discretize the linearized system matrices. (Teng et al., 2022) `ev:reported` p. 4 ^teng2022error-021
- Simulations track a spiral reference with constant twist on a fully actuated 3D rigid body without gravity. (Teng et al., 2022) `ev:reported` p. 4 ^teng2022error-022
- The simulation study randomly samples 100 initial orientations and positions around the identity for each compared controller. (Teng et al., 2022) `ev:reported` p. 4 ^teng2022error-023
- Baselines are the VBL-based MPC using the compatible orientation error and a simplified version of the proposed method ignoring adjoint terms. (Teng et al., 2022) `ev:reported` p. 4 ^teng2022error-024
- All simulated methods use the same stage costs, control horizon N = 12, the same input constraints, and a Riccati terminal cost. (Teng et al., 2022) `ev:reported` p. 4 ^teng2022error-025
- The authors report no noticeable improvement in tracking performance for horizons longer than N = 12 in simulation. (Teng et al., 2022) `ev:measured` p. 4 ^teng2022error-026
- With the compatible error, the VBL-based MPC shows a much lower convergence rate when the initial orientation error is large. (Teng et al., 2022) `ev:measured` p. 4 ^teng2022error-027
- Prior work guarantees exponential stability with the compatible error only when the initial orientation error is less than 90°. (Teng et al., 2022) `ev:cited` p. 4 ^teng2022error-028
- As the orientation error approaches 180°, the compatible error goes to 0 according to the authors' comparison plot. (Teng et al., 2022) `ev:computed` p. 4 ^teng2022error-029
- In simulation, the position error of the VBL-based MPC converges fast because it is decoupled from the orientation error. (Teng et al., 2022) `ev:measured` p. 4 ^teng2022error-030
- Over 100 simulated trials, the proposed controller outperforms both baselines in orientation tracking according to the accumulated-error histogram. (Teng et al., 2022) `ev:measured` p. 5 ^teng2022error-031
- The proposed controller also outperforms its simplified version in both orientation and position tracking in simulation. (Teng et al., 2022) `ev:measured` p. 5 ^teng2022error-032
- The authors interpret the advantage over the simplified version as demonstrating the success of the linearization scheme. (Teng et al., 2022) `ev:asserted` p. 5 ^teng2022error-033
- The VBL-MPC outperforms the other two methods in position tracking because it deals with position in R3. (Teng et al., 2022) `ev:measured` p. 5 ^teng2022error-034
- In the histogram of 100 trials, the VBL MPC orientation tracking error has a long tail. (Teng et al., 2022) `ev:measured` p. 6 ^teng2022error-035
- Hardware validation uses the MIT Mini Cheetah quadrupedal robot, with a single rigid body model approximating the torso motion. (Teng et al., 2022) `ev:reported` p. 5 ^teng2022error-036
- Legs are modeled as point contacts, with only ground reaction forces acting at contact points under friction cone constraints. (Teng et al., 2022) `ev:reported` p. 5 ^teng2022error-037
- For the convex QP, the lever arms and the orientation in gravity and friction terms are assumed constant over the horizon. (Teng et al., 2022) `ev:reported` p. 5 ^teng2022error-038
- Hardware baselines are the VBL-based MPC and the Euler angle-based convex MPC, without any feedforward term from a high-level planner. (Teng et al., 2022) `ev:reported` p. 5 ^teng2022error-039
- On hardware, the terminal cost matrix is approximated by executing one Riccati recursion step before each MPC application. (Teng et al., 2022) `ev:reported` p. 6 ^teng2022error-040
- The friction coefficient in the friction cone constraints is set to µ = 0.6 for all hardware experiments. (Teng et al., 2022) `ev:reported` p. 6 ^teng2022error-041
- Pose tracking applies step signals in pure roll and in mixed roll and yaw, with all four legs on the ground. (Teng et al., 2022) `ev:reported` p. 6 ^teng2022error-042
- Pose tracking uses control horizon N = 4 and ∆t = 0.025s, with each experiment conducted three times. (Teng et al., 2022) `ev:reported` p. 6 ^teng2022error-043
- The roll reference changes from 0 to -74.5 degrees between 1 and 11 seconds before the robot leans the opposite way. (Teng et al., 2022) `ev:reported` p. 6 ^teng2022error-044
- In the combined reference, roll goes from 0 to -57.3 degrees, with yaw going from 0 to 28.5 degrees. (Teng et al., 2022) `ev:reported` p. 6 ^teng2022error-045
- Without feedforward force at equilibrium, all three controllers show steady-state error in the pose tracking experiments. (Teng et al., 2022) `ev:measured` p. 6 ^teng2022error-046
- The geometric controllers, proposed and VBL-based MPC, have smaller steady-state error than the Euler angle-based MPC in pose tracking. (Teng et al., 2022) `ev:measured` p. 6 ^teng2022error-047
- The VBL-based MPC has a much lower convergence rate than the proposed controller, most visibly when the opposite Euler angle signal is applied. (Teng et al., 2022) `ev:measured` p. 6 ^teng2022error-048
- The convergence rates observed on the robot are consistent with the numerical simulation results, according to the authors. (Teng et al., 2022) `ev:measured` p. 6 ^teng2022error-049
- In roll-only tracking, the proposed MPC and Euler MPC have similar tracking performance since the errors coincide. (Teng et al., 2022) `ev:measured` p. 7 ^teng2022error-050
- With combined roll and yaw signals, the Euler angle-based MPC has a larger steady-state error. (Teng et al., 2022) `ev:measured` p. 7 ^teng2022error-051
- For trotting, controllers plan ground reaction forces that are passed to Whole Body Impulse Control to obtain joint torques. (Teng et al., 2022) `ev:reported` p. 6 ^teng2022error-052
- Trotting uses control horizon N = 10, the shortest horizon that ensures stable walking gaits according to the authors. (Teng et al., 2022) `ev:reported` p. 6 ^teng2022error-053
- The WBIC penalty on deviation from the planned ground reaction force was increased by 1e4 times. (Teng et al., 2022) `ev:reported` p. 6 ^teng2022error-054
- In trotting, the proposed MPC and VBL-MPC track the yaw rate better than the Euler angle-based MPC. (Teng et al., 2022) `ev:measured` p. 6 ^teng2022error-055
- All three controllers track the commanded linear velocity well in the trotting experiments on Mini Cheetah. (Teng et al., 2022) `ev:measured` p. 7 ^teng2022error-056
- The large steady-state error in pose tracking is probably due to friction of the mechanical parts, according to the authors. (Teng et al., 2022) `ev:asserted` p. 7 ^teng2022error-057
- In Mini Cheetah simulation environments, the authors noticed a much smaller steady-state error than observed in the hardware experiments. (Teng et al., 2022) `ev:measured` p. 7 ^teng2022error-058
- The authors believe the larger steady-state error of Euler angle-based MPC is due to the loss of symmetry. (Teng et al., 2022) `ev:asserted` p. 7 ^teng2022error-059
- The authors attribute the faster orientation convergence over variational-based MPC to the quadratic cost function designed in the Lie algebra. (Teng et al., 2022) `ev:asserted` p. 7 ^teng2022error-060
- Comparing different integration techniques within the proposed approach is identified as an interesting future research direction. (Teng et al., 2022) `ev:asserted` p. 4 ^teng2022error-061
- An integration scheme that preserves the Lagrangian could be integrated with the framework in future work. (Teng et al., 2022) `ev:asserted` p. 8 ^teng2022error-062
- Future work includes extending the controller with learning-aided state estimators to enable environmental awareness and more aggressive maneuvers. (Teng et al., 2022) `ev:asserted` p. 8 ^teng2022error-063
- The authors conclude that the approach provides faster convergence when rotation and position are controlled simultaneously, in simulation and experiments. (Teng et al., 2022) `ev:asserted` p. 8 ^teng2022error-064

## 🎯 Contributions

## 📖 Glossary

- **Matrix Lie group** — A group of matrices forming a smooth manifold, such as SO(3) or SE(3).
- **Lie algebra** — The tangent space of a Lie group at the identity element.
- **Adjoint map** — Lie algebra isomorphism that changes the reference frame of a twist.
- **Error-state MPC** — Predictive controller whose state is the tracking error rather than the absolute state.
- **Compatible error** — Orientation error built from the skew part of relative rotations; loses scale near 180°.
- **Variational-based linearization (VBL)** — Linearization of Lie group dynamics along a given trajectory via variations.
- **Ground reaction force (GRF)** — Contact force exerted by the ground on a robot foot.
- **Whole Body Impulse Control (WBIC)** — Hierarchical controller mapping planned contact forces and tasks to joint torques.

## ❓ Open questions

- How do zero-order hold or Lagrangian-preserving integration schemes change performance compared with Euler first-order integration?
- Can the global validity of the linearization be turned into formal convergence guarantees for the constrained MPC?
- How much of the hardware steady-state error would be removed by feedforward terms or friction compensation?
- Does the body-frame position treatment remain slower than R3-based baselines in more dynamic locomotion tasks?
- How does the controller behave when lever arms and orientation vary strongly within the horizon?

## 📝 Notes on reading

Read from arXiv 2203.08728v2 (23 Jan 2023), matching the packet identifier. Figures 2, 3 and 5 (simulation trajectories, error curves, histograms) and Figures 8 to 10 (hardware error convergence and trotting tracking) are extracted as bare axis numbers; only their captions were used. Equations (6) to (26) are partly garbled in extraction; derivation steps were described rather than transcribed. The trotting timestep is printed as 0.0.25s on p. 6, which is a typo in the paper and was not claimed. No quantitative error values (e.g. RMSE) are reported in text; all comparative results are qualitative, from captions and prose.

## Suggested new concepts

- Error-state MPC on Lie groups — a recurring control design pattern linking geometric control and convex MPC for legged robots.
- Compatible vs logarithmic orientation error — the choice of error metric governs convergence rate for large orientation errors.
- Single rigid body model for quadrupeds — the common centroidal approximation behind convex MPC locomotion controllers.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — MPC convexo de estado de error en $\mathfrak{g}$ (C.2).

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
