---
aliases: []
type: "source"
title: "RMPflow: A Computational Graph for Automatic Motion Policy Generation"
citekey: "Cheng2018rmpflow"
doi: "10.48550/arXiv.1811.07049"
arxiv: "1811.07049"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1811.07049"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Ching-An Cheng", "Mustafa Mukadam", "Jan Issac", "Stan Birchfield", "Dieter Fox", "Byron Boots", "Nathan Ratliff"]
sha256: ["069d06920ffdffd1e9ec3d4b562a1c016f81a9f9f803c59d271d25a6251f550c"]
pdf: "Content/Papers/Cheng2018rmpflow.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Cheng2018rmpflow.pdf]]

> [!abstract] One-sentence summary
> RMPflow combines per-subtask Riemannian Motion Policies over a tree of task maps into one provably stable, coordinate-free global policy, and in cluttered reaching it avoided collisions that isotropic potential-field baselines could not.

## Abstract

We develop a novel policy synthesis algorithm, RMPflow, based on geometrically consistent transformations of Riemannian Motion Policies (RMPs). RMPs are a class of reactive motion policies designed to parameterize non-Euclidean behaviors as dynamical systems in intrinsically nonlinear task spaces. Given a set of RMPs designed for individual tasks, RMPflow can consistently combine these local policies to generate an expressive global policy, while simultaneously exploiting sparse structure for computational efficiency. We study the geometric properties of RMPflow and provide sufficient conditions for stability. Finally, we experimentally demonstrate that accounting for the geometry of task policies can simplify classically difficult problems, such as planning through clutter on high-DOF manipulation systems. (arXiv)

## 🧠 Key ideas (atomic)

- The authors develop a motion generation and control framework that enables globally stable controller design within intrinsically non-Euclidean spaces. (Cheng et al., 2018) `ev:asserted` p. 1 ^cheng2018rmpflow-001
- The authors state that planning techniques modeling non-Euclidean task-space behavior are often computationally intensive, sensitive to noise, and unresponsive to perturbation. (Cheng et al., 2018) `ev:cited` p. 1 ^cheng2018rmpflow-002
- Operational Space Control accounts for internal geometry from the robot kinematic structure but assumes simple Euclidean geometry in task spaces. (Cheng et al., 2018) `ev:cited` p. 2 ^cheng2018rmpflow-003
- The authors argue that obstacle avoidance relying on extrinsic potential functions leads to undesirable deceleration when the robot is close to obstacles. (Cheng et al., 2018) `ev:asserted` p. 2 ^cheng2018rmpflow-004
- RMPflow mimics the [[Recursive Newton-Euler algorithm]] in structure but generalizes it beyond rigid-body systems to highly nonlinear transformations and spaces. (Cheng et al., 2018) `ev:asserted` p. 2 ^cheng2018rmpflow-005
- The framework models non-Euclidean task spaces with Riemannian metrics that are not only configuration dependent but also velocity dependent. (Cheng et al., 2018) `ev:asserted` p. 2 ^cheng2018rmpflow-006
- With velocity-dependent importance weights, an obstacle close to the robot can usually be ignored if the robot is heading away from it. (Cheng et al., 2018) `ev:asserted` p. 2 ^cheng2018rmpflow-007
- The authors introduce a new class of non-physical mechanical systems, Geometric Dynamical Systems, as an extension of Geometric Control Theory. (Cheng et al., 2018) `ev:asserted` p. 2 ^cheng2018rmpflow-008
- Motion is modeled as a second-order differential equation, a motion policy mapping position and velocity to acceleration, assuming a feedback-linearized system. (Cheng et al., 2018) `ev:reported` p. 3 ^cheng2018rmpflow-009
- The authors argue that control approaches cannot model velocity-dependent metrics, which they consider critical to generating sensible obstacle avoidance motions. (Cheng et al., 2018) `ev:asserted` p. 4 ^cheng2018rmpflow-010
- RMPflow describes the tree-structured task map and the subtask policies with a data structure the authors call the RMP-tree. (Cheng et al., 2018) `ev:asserted` p. 4 ^cheng2018rmpflow-011
- To compute the policy, RMPflow first runs a forward pass propagating state from the root node to the leaf nodes. (Cheng et al., 2018) `ev:asserted` p. 4 ^cheng2018rmpflow-012
- After the forward pass, a backward pass propagates the RMPs from the leaf nodes back to the root node. (Cheng et al., 2018) `ev:asserted` p. 4 ^cheng2018rmpflow-013
- Handling the task-map structure lets users design motion policies for each subtask individually, which the authors consider easier than one global policy. (Cheng et al., 2018) `ev:asserted` p. 5 ^cheng2018rmpflow-014
- An [[Riemannian Motion Policies|RMP]] pairs a continuous desired-acceleration policy with a differentiable positive semi-definite inertia matrix that defines its directional importance. (Cheng et al., 2018) `ev:asserted` p. 5 ^cheng2018rmpflow-015
- The RMP-algebra consists of three operators, pushforward, pullback and resolve, that propagate information across the RMP-tree. (Cheng et al., 2018) `ev:asserted` p. 6 ^cheng2018rmpflow-016
- In canonical form, pullback yields the acceleration solving a least-squares problem weighted by each child node's state-dependent inertia matrix. (Cheng et al., 2018) `ev:computed` p. 6 ^cheng2018rmpflow-017
- Unlike the original RMP definition, RMPflow's pullback includes the J-dot x-dot term, which the authors call critical for consistent policy behaviors. (Cheng et al., 2018) `ev:asserted` p. 6 ^cheng2018rmpflow-018
- Resolve maps a natural-form RMP to canonical form with a Moore-Penrose pseudo-inverse, since the inertia matrix is generally only positive semi-definite. (Cheng et al., 2018) `ev:asserted` p. 6 ^cheng2018rmpflow-019
- For K subtasks, RMPflow policy generation has worst-case time complexity O(K), compared with O(K log K) for a naive implementation. (Cheng et al., 2018) `ev:computed` p. 7 ^cheng2018rmpflow-020
- Apart from the final resolve call, all RMPflow computations are matrix multiplications, leaving one matrix inversion at the root node. (Cheng et al., 2018) `ev:asserted` p. 7 ^cheng2018rmpflow-021
- The authors state that performing only one matrix inversion at the root node makes RMPflow numerically stable. (Cheng et al., 2018) `ev:asserted` p. 7 ^cheng2018rmpflow-022
- Barrier-type collision avoidance [[Riemannian Motion Policies|RMPs]] use velocity-dependent inertia matrices, so the RMP can be turned off when the robot heads away. (Cheng et al., 2018) `ev:asserted` p. 7 ^cheng2018rmpflow-023
- RMPs built with Q-functions as metrics may not satisfy GDS conditions, yet the authors report practical benefits such as escaping local minima. (Cheng et al., 2018) `ev:asserted` p. 8 ^cheng2018rmpflow-024
- The authors show that pullback retains closure: when child-node policies are structured GDSs, the parent-node dynamics belong to the same class. (Cheng et al., 2018) `ev:computed` p. 8 ^cheng2018rmpflow-025
- The authors show RMPflow is coordinate-free, meaning subtask [[Riemannian Motion Policies|RMPs]] designed for one robot can transfer to another with the same task-space behaviors. (Cheng et al., 2018) `ev:computed` p. 8 ^cheng2018rmpflow-026
- When the metric is velocity-independent, GDSs reduce to the widely studied simple mechanical systems, with the curvature term equal to the Coriolis force. (Cheng et al., 2018) `ev:computed` p. 9 ^cheng2018rmpflow-027
- For the root structured GDS, the time derivative of the Lyapunov candidate equals the negative damping quadratic form in velocity. (Cheng et al., 2018) `ev:computed` p. 10 ^cheng2018rmpflow-028
- If the root metric and damping matrices are positive definite, the system converges to a forward invariant set with zero potential gradient. (Cheng et al., 2018) `ev:computed` p. 10 ^cheng2018rmpflow-029
- The barrier-type collision avoidance policy of Section 3.6 satisfies the sufficient stability condition for 1D velocity-dependent leaf metrics. (Cheng et al., 2018) `ev:computed` p. 10 ^cheng2018rmpflow-030
- A GDS can be written with a unique asymmetric affine connection compatible with a Riemannian metric defined on the tangent bundle. (Cheng et al., 2018) `ev:computed` p. 10 ^cheng2018rmpflow-031
- The recursive pullbacks in RMPflow's backward pass perform pullbacks of task-space covectors, metrics and asymmetric affine connections without coordinates. (Cheng et al., 2018) `ev:computed` p. 11 ^cheng2018rmpflow-032
- When the task metric is Euclidean, meaning constant, RMPflow recovers Operational Space Control and its variants, according to the authors. (Cheng et al., 2018) `ev:asserted` p. 11 ^cheng2018rmpflow-033
- With only configuration-dependent task metrics, RMPflow can be viewed as energy shaping to combine multiple simple mechanical systems in geometric control. (Cheng et al., 2018) `ev:asserted` p. 11 ^cheng2018rmpflow-034
- In a 1D barrier-type example, performing pullback with the J-dot q-dot term produced behavior matching the designed desired behavior. (Cheng et al., 2018) `ev:computed` p. 12 ^cheng2018rmpflow-035
- Ignoring the J-dot q-dot term in the 1D example made the observed behavior inconsistent and unstable. (Cheng et al., 2018) `ev:computed` p. 12 ^cheng2018rmpflow-036
- Damping nonlinear in velocity recovered stability when the J-dot q-dot term was ignored, but the 1D behavior remained inconsistent. (Cheng et al., 2018) `ev:computed` p. 12 ^cheng2018rmpflow-037
- In the 2D example, curvature terms of the velocity-dependent obstacle metric produced natural avoidance, coaxing the system toward obstacle isocontours. (Cheng et al., 2018) `ev:computed` p. 13 ^cheng2018rmpflow-038
- Without curvature terms or a barrier potential, the particle in the 2D example travelled in straight lines with constant velocity. (Cheng et al., 2018) `ev:computed` p. 13 ^cheng2018rmpflow-039
- Combining the obstacle RMP with an attractor RMP produced behavior transitioning smoothly toward the goal while heading away from the obstacle. (Cheng et al., 2018) `ev:computed` p. 13 ^cheng2018rmpflow-040
- When curvature terms were ignored for both combined RMPs, the 2D trajectories oscillated near the obstacle. (Cheng et al., 2018) `ev:computed` p. 13 ^cheng2018rmpflow-041
- With a metric that was not velocity-based, the combined 2D behavior was less efficient in breaking free from the obstacle toward the goal. (Cheng et al., 2018) `ev:computed` p. 13 ^cheng2018rmpflow-042
- RMPflow was compared with OSC as potential fields with dynamics reshaping, PF-basic, and PF-nonlinear, which scales collision weights nonlinearly with proximity. (Cheng et al., 2018) `ev:reported` p. 13 ^cheng2018rmpflow-043
- Baseline collision-avoidance task spaces used control points along the robot body with isotropic metrics, rather than RMPflow's distance spaces. (Cheng et al., 2018) `ev:reported` p. 14 ^cheng2018rmpflow-044
- Across multiple settings, the isotropic-metric baselines failed to match the speed and precision achieved by RMPflow in reaching through clutter. (Cheng et al., 2018) `ev:measured` p. 14 ^cheng2018rmpflow-045
- Higher-weight baseline settings tended to have fewer collisions and better economy of motion, but at the expense of efficiency. (Cheng et al., 2018) `ev:measured` p. 14 ^cheng2018rmpflow-046
- Adding nonlinear weights as in PF-nonlinear did not seem to help performance compared with the basic potential-field baseline. (Cheng et al., 2018) `ev:measured` p. 14 ^cheng2018rmpflow-047
- The authors attribute RMPflow's performance to its non-isotropic metric, which encodes directional importance around obstacles when combining policies. (Cheng et al., 2018) `ev:asserted` p. 14 ^cheng2018rmpflow-048
- An integrated system for vision-driven dual-arm manipulation was demonstrated on an ABB YuMi robot and a Rethink Baxter robot. (Cheng et al., 2018) `ev:reported` p. 14 ^cheng2018rmpflow-049
- The system uses the real-time tracking algorithm DART, which receives robot configuration priors and sends world-state tracking updates. (Cheng et al., 2018) `ev:reported` p. 14 ^cheng2018rmpflow-050
- Tested tasks included picking up trash in clutter, reactive cabinet manipulation with human perturbation, active lead-through, and drawer pick-and-place. (Cheng et al., 2018) `ev:reported` p. 14 ^cheng2018rmpflow-051
- The authors conclude that RMPflow can generate smooth and natural motion for various tasks when proper subtask RMPs are specified. (Cheng et al., 2018) `ev:asserted` p. 14 ^cheng2018rmpflow-052
- Unlike classical recursive forward dynamics procedures, RMPflow computes the force and the inertia matrix in a single backward pass. (Cheng et al., 2018) `ev:asserted` p. 30 ^cheng2018rmpflow-053
- The experimental task-map tree treats each link frame as one forward kinematic step from the configuration space, emphasizing parallelization. (Cheng et al., 2018) `ev:reported` p. 31 ^cheng2018rmpflow-054
- The analysis suggests the attractor of the original RMP paper, lacking the curvature term, could lose stability in general. (Cheng et al., 2018) `ev:computed` p. 38 ^cheng2018rmpflow-055
- Adding the curvature correction back to the original RMP attractor makes the system provably stable, according to the authors' analysis. (Cheng et al., 2018) `ev:computed` p. 38 ^cheng2018rmpflow-056
- The velocity-dependent joint-limit metric defined in the appendix satisfies the sufficient stability condition of Theorem 2. (Cheng et al., 2018) `ev:computed` p. 40 ^cheng2018rmpflow-057
- Reaching experiments used a modeled ABB YuMi robot in simulated clutter environments with cylindrical obstacles of varying sizes. (Cheng et al., 2018) `ev:reported` p. 42 ^cheng2018rmpflow-058
- PF-basic weight scalings for obstacle and C-space metrics were low (3, 10), med (5, 50) and high (10, 100). (Cheng et al., 2018) `ev:reported` p. 42 ^cheng2018rmpflow-059
- Each method ran on 6 obstacle environments with 20 randomly sampled target locations on the opposite side of the obstacles. (Cheng et al., 2018) `ev:reported` p. 42 ^cheng2018rmpflow-060
- Results report means with one standard deviation error bars calculated across the 120 trials for each performance measure. (Cheng et al., 2018) `ev:reported` p. 43 ^cheng2018rmpflow-061
- Time to goal measures reaching a convergence state, with trials that never converge timing out after 5 seconds. (Cheng et al., 2018) `ev:reported` p. 43 ^cheng2018rmpflow-062
- RMPflow never collided in the reaching experiments, so its collision intensity and collision failure values are 0. (Cheng et al., 2018) `ev:measured` p. 43 ^cheng2018rmpflow-063
- Lower weight scalings of both baselines achieved some faster times and better goal distances by pushing directly through obstacles. (Cheng et al., 2018) `ev:measured` p. 44 ^cheng2018rmpflow-064
- The authors found little empirical difference between PF-basic and PF-nonlinear across the reaching-through-clutter performance measures. (Cheng et al., 2018) `ev:measured` p. 44 ^cheng2018rmpflow-065
- The integrated physical system ignored curvature terms, maintaining stability with sufficient damping terms and slower operating speeds instead. (Cheng et al., 2018) `ev:reported` p. 45 ^cheng2018rmpflow-066
- Generalization of these RMPs between embodiments was anecdotally pretty consistent, though the authors expect more deviation at higher speeds. (Cheng et al., 2018) `ev:asserted` p. 45 ^cheng2018rmpflow-067

## 🎯 Contributions

## 📖 Glossary

- **Riemannian Motion Policy (RMP)** — A desired-acceleration policy paired with an inertia matrix giving its directional importance.
- **RMP-tree** — Directed tree whose nodes hold RMPs and states and whose edges are task maps.
- **RMP-algebra** — The pushforward, pullback and resolve operators that propagate information across an RMP-tree.
- **Pullback** — Operator combining child natural-form RMPs into the parent via Jacobian transposes.
- **Resolve** — Operator converting a natural-form RMP to canonical form with a pseudo-inverse.
- **Geometric Dynamical System (GDS)** — Second-order dynamics defined by a possibly velocity-dependent metric, damping and potential.
- **Structured GDS** — GDS augmented with information on how its metric matrix factorizes through a map.
- **Curvature terms** — Terms arising from non-constant metrics that bend trajectories, generalizing Coriolis forces.
- **Operational Space Control (OSC)** — Task-space control reshaping dynamics into a constant-inertia spring-mass-damper system.

## ❓ Open questions

- How can learning components relax the need for carefully hand-designed subtask RMPs?
- Can Q-function-based RMPs, which may violate GDS conditions, be given stability guarantees?
- How large is the embodiment-transfer deviation at higher speeds when curvature terms are ignored?
- How does RMPflow compare with non-potential-field baselines such as sampling-based or optimization planners in clutter?
- How sensitive is performance to the hand-tuned weight functions and radii of the collision and attractor RMPs?

## 📝 Notes on reading

Version read: arXiv 1811.07049v2 (5 Apr 2019), with appendices A to F (45 pages). Fig. 2 and Fig. 3 (1D and 2D phase portraits and trajectories) and Fig. 4 (bar chart of time, length, goal distance, collision intensity and collision failure for RMPflow and PF variants) could only be described; their per-method values are not readable in the extracted text, so no numeric results from Fig. 4 were claimed. Fig. 6 (task-map tree used in experiments) is extracted as scattered symbols. Many equations in the theory and proofs are garbled by extraction; claims about them are stated in words. The integrated physical system (Appendix F) ignored curvature terms, unlike the controlled experiments, so the stability guarantees are not the ones exercised on hardware. Footnote 14 (p. 44) mentions the RMP portion also ran on an ABB IRB120 and a dual-arm Kuka platform; Appendix F (p. 45) describes smoothing Baxter collision controllers by attending to closest points to a volume around each control point. Footnote 13 notes that reaching performance is measured relative to RMPflow since feasibility is not guaranteed.

## Suggested new concepts

- Riemannian Motion Policies — the policy representation underlying RMPflow and follow-up reactive controllers.
- Geometric Dynamical Systems — a class of dynamics with velocity-dependent metrics carrying the stability analysis.
- Operational Space Control — the classical baseline RMPflow recovers when task metrics are constant.
- Velocity-dependent metrics for obstacle avoidance — the design choice credited for RMPflow's collision-free reaching.
- Reactive motion generation for manipulation — the broader lane of closed-loop policies competing with planning.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Combinación geométricamente consistente de RMPs (C.3).

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
