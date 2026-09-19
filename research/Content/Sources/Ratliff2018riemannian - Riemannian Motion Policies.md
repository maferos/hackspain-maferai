---
aliases: []
type: "source"
title: "Riemannian Motion Policies"
citekey: "Ratliff2018riemannian"
doi: "10.48550/arXiv.1801.02854"
arxiv: "1801.02854"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1801.02854"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Nathan D. Ratliff", "Jan Issac", "Daniel Kappler", "Stan Birchfield", "Dieter Fox"]
sha256: ["5e0e8497db2f909339f2d1ee39aecd69407662322ab3e595430d8a5653a9cd56"]
pdf: "Content/Papers/Ratliff2018riemannian.pdf"
topics: ["[[Matemáticas]]", "[[Optimización y algoritmos]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]", "[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[Ratliff2018riemannian.pdf]]

> [!abstract] One-sentence summary
> The paper defines Riemannian Motion Policies, acceleration policies paired with metrics whose pullback and metric-weighted combination give optimal, modular fusion of many reactive and optimization-based controllers, shown on dual-arm robots.

## Abstract

We introduce the Riemannian Motion Policy (RMP), a new mathematical object for modular motion generation. An RMP is a second-order dynamical system (acceleration field or motion policy) coupled with a corresponding Riemannian metric. The motion policy maps positions and velocities to accelerations, while the metric captures the directions in the space important to the policy. We show that RMPs provide a straightforward and convenient method for combining multiple motion policies and transforming such policies from one space (such as the task space) to another (such as the configuration space) in geometrically consistent ways. The operators we derive for these combinations and transformations are provably optimal, have linearity properties making them agnostic to the order of application, and are strongly analogous to the covariant transformations of natural gradients popular in the machine learning literature. The RMP framework enables the fusion of motion policies from different motion generation paradigms, such as dynamical systems, dynamic movement primitives (DMPs), optimal control, operational space control, nonlinear reactive controllers, motion optimization, and model predictive control (MPC), thus unifying these disparate techniques from the literature. RMPs are easy to implement and manipulate, facilitate controller design, simplify handling of joint limits, and clarify a number of open questions regarding the proper fusion of motion generation methods (such as incorporating local reactive policies into long-horizon optimizers). We demonstrate the effectiveness of RMPs on both simulation and real robots, including their ability to naturally and efficiently solve complicated collision avoidance problems previously handled by more complex planners. (arXiv)

## 🧠 Key ideas (atomic)

- The paper defines the Riemannian Motion Policy by pairing each motion policy with a Riemannian metric that defines its local geometry. (Ratliff et al., 2018) `ev:asserted` p. 1 ^ratliff2018riemannian-001
- The authors argue that many highly constrained motion generation problems are often solvable by purely local reactive motion policies. (Ratliff et al., 2018) `ev:asserted` p. 1 ^ratliff2018riemannian-002
- According to the authors, earlier local obstacle avoidance techniques had obstacle and task policies fighting each other, requiring special nullspace engineering. (Ratliff et al., 2018) `ev:asserted` p. 1 ^ratliff2018riemannian-003
- The authors derive operators for transforming and combining RMPs, proving that these operators are associative as well as optimal. (Ratliff et al., 2018) `ev:asserted` p. 2 ^ratliff2018riemannian-004
- The RMP transformation and combination operators behave analogously to natural gradient operations from the machine learning literature. (Ratliff et al., 2018) `ev:asserted` p. 2 ^ratliff2018riemannian-005
- Instead of pseudoinverses, the RMP framework uses geometrically consistent pullback operations to transform policies from one space to another. (Ratliff et al., 2018) `ev:asserted` p. 2 ^ratliff2018riemannian-006
- Instead of simply adding policies together, RMPs perform metric-weighted averages that account for the local geometry of each policy. (Ratliff et al., 2018) `ev:asserted` p. 2 ^ratliff2018riemannian-007
- The framework is demonstrated on three dual-arm manipulation platforms, both in simulation as well as on real robots. (Ratliff et al., 2018) `ev:reported` p. 2 ^ratliff2018riemannian-008
- The authors state that computationally intensive optimizers can run in a separate process and be streamed as RMPs without loss of fidelity. (Ratliff et al., 2018) `ev:asserted` p. 2 ^ratliff2018riemannian-009
- Dynamical system representations such as DMPs model second-order motion but do not concretely address combining policies across many task spaces. (Ratliff et al., 2018) `ev:cited` p. 2 ^ratliff2018riemannian-010
- Operational space control addresses combining multiple policies but, per the authors, does not address shaping the behavior of those policies. (Ratliff et al., 2018) `ev:cited` p. 2 ^ratliff2018riemannian-011
- Existing approaches often include a weight matrix on each task space term but usually do not justify the chosen metric. (Ratliff et al., 2018) `ev:asserted` p. 2 ^ratliff2018riemannian-012
- Separately computed components can be combined into a single C-space linear RMP, reducing what must be communicated to the central core. (Ratliff et al., 2018) `ev:asserted` p. 3 ^ratliff2018riemannian-013
- The dropped second-order correction is deemed unnecessary because control loops running between 100 Hz and 1 kHz take small integration steps. (Ratliff et al., 2018) `ev:asserted` p. 3 ^ratliff2018riemannian-014
- The authors claim the approach yields a provably optimal control system that transfers from one robot to another without re-tuning parameters. (Ratliff et al., 2018) `ev:asserted` p. 4 ^ratliff2018riemannian-015
- RMP addition combines policies as a metric-weighted average, applying the pseudoinverse of the summed metrics to metric-weighted accelerations. (Ratliff et al., 2018) `ev:computed` p. 4 ^ratliff2018riemannian-016
- When every metric is a scaled identity matrix, the metric-weighted combination reduces to a traditional weighted average of the policies. (Ratliff et al., 2018) `ev:computed` p. 4 ^ratliff2018riemannian-017
- The RMP pullback transforms a task space policy into configuration space with the [[Pullback metric|pullback metric]] J transpose A J. (Ratliff et al., 2018) `ev:computed` p. 4 ^ratliff2018riemannian-018
- The pullback differential equation can be viewed as a natural vector field, in analogy to the natural gradient in machine learning. (Ratliff et al., 2018) `ev:asserted` p. 4 ^ratliff2018riemannian-019
- The authors show that addition of RMPs is both commutative and associative for any RMPs defined in the same space. (Ratliff et al., 2018) `ev:computed` p. 4 ^ratliff2018riemannian-020
- The authors show that the pullback and pushforward operators are both linear with respect to the addition of RMPs. (Ratliff et al., 2018) `ev:computed` p. 4 ^ratliff2018riemannian-021
- The pullback operation is covariant to reparameterization, so integral curves created in transformed coordinates match those found directly in the original space. (Ratliff et al., 2018) `ev:computed` p. 5 ^ratliff2018riemannian-022
- The combined configuration space policy minimizes a sum of metric-weighted squared errors between desired task accelerations and Jacobian-mapped accelerations. (Ratliff et al., 2018) `ev:computed` p. 5 ^ratliff2018riemannian-023
- Each RMP corresponds to a quadratic term whose minimizer is the vector field and whose Hessian is the metric. (Ratliff et al., 2018) `ev:computed` p. 5 ^ratliff2018riemannian-024
- The target RMP pulls the end effector toward the goal with a soft-normalized position term plus damping proportional to velocity. (Ratliff et al., 2018) `ev:reported` p. 5 ^ratliff2018riemannian-025
- For the target controller, the authors have found in practice that both identity and directionally stretched metrics work well. (Ratliff et al., 2018) `ev:asserted` p. 5 ^ratliff2018riemannian-026
- RMPs express partial orientation constraints by applying target controllers to a canonical point along the appropriate axis of the end effector. (Ratliff et al., 2018) `ev:reported` p. 5 ^ratliff2018riemannian-027
- Each collision RMP uses a directionally stretched metric, since the controller does not care about motion orthogonal to the obstacle direction. (Ratliff et al., 2018) `ev:asserted` p. 6 ^ratliff2018riemannian-028
- The authors report that handling each obstacle as a separate RMP combined by RMP operations makes a substantial difference in practice. (Ratliff et al., 2018) `ev:asserted` p. 6 ^ratliff2018riemannian-029
- Redundancy resolution uses a configuration-space spring-damper controller toward a default posture configuration with an identity metric. (Ratliff et al., 2018) `ev:reported` p. 6 ^ratliff2018riemannian-030
- The redundancy controller is not covariant because it is defined in the configuration space, making it robot-dependent. (Ratliff et al., 2018) `ev:asserted` p. 6 ^ratliff2018riemannian-031
- The local controllers are effective among obstacles but need more sophisticated techniques to navigate large obstacles that warp workspace geometry. (Ratliff et al., 2018) `ev:asserted` p. 6 ^ratliff2018riemannian-032
- Evaluating the finite-horizon optimized policy can only run at low rates, e.g., 10-20 times a second, even with warm starts. (Ratliff et al., 2018) `ev:reported` p. 6 ^ratliff2018riemannian-033
- Under the RieMO framework, the Gauss-Newton Hessian approximation defines the Riemannian metric associated with the optimized MPC policy. (Ratliff et al., 2018) `ev:cited` p. 6 ^ratliff2018riemannian-034
- The heuristic long-range navigation approach requires no planning as long as the elbow of the robot is not blocked. (Ratliff et al., 2018) `ev:asserted` p. 6 ^ratliff2018riemannian-035
- The authors use the simple configuration-space retract heuristic in practice for many of their manipulation problems. (Ratliff et al., 2018) `ev:reported` p. 7 ^ratliff2018riemannian-036
- The second retract heuristic performs slightly better on some intentionally difficult environments studied in the experimental section. (Ratliff et al., 2018) `ev:measured` p. 7 ^ratliff2018riemannian-037
- For reaching forward, the arm follows guiding points from rough IK approximations that pull it into the needed homotopy class. (Ratliff et al., 2018) `ev:reported` p. 7 ^ratliff2018riemannian-038
- Simple affine policies in the unconstrained sigmoid space manifest as highly nonlinear policies in the original joint limit space. (Ratliff et al., 2018) `ev:asserted` p. 7 ^ratliff2018riemannian-039
- With superposition, symmetric acceleration contributions from two obstacles can sum to zero, so the control system ignores the obstacles. (Ratliff et al., 2018) `ev:asserted` p. 7 ^ratliff2018riemannian-040
- High weights on obstacle terms under superposition often result in sluggish behavior as the robot slows down near obstacles. (Ratliff et al., 2018) `ev:asserted` p. 7 ^ratliff2018riemannian-041
- Obstacle RMPs leave velocities perpendicular to the obstacle direction unaffected, allowing the robot to glide smoothly around obstacles. (Ratliff et al., 2018) `ev:asserted` p. 7 ^ratliff2018riemannian-042
- The metric may be viewed as a soft alternative to a null-space description, encoding trade-offs rather than hard directions of independence. (Ratliff et al., 2018) `ev:asserted` p. 7 ^ratliff2018riemannian-043
- Offboard nonlinear policies can be linearized and communicated at slower rates, e.g., 10 Hz, to a faster RMP core, e.g., 1 kHz. (Ratliff et al., 2018) `ev:asserted` p. 7 ^ratliff2018riemannian-044
- The baseline replaces each [[Pullback metric|pullback metric]] with an equivalently scaled identity metric, representing the best-scaled pseudoinverse solution. (Ratliff et al., 2018) `ev:reported` p. 8 ^ratliff2018riemannian-045
- Choosing the baseline scale as the maximum eigenvalue of the original metric led to the best performance among the tested scalings. (Ratliff et al., 2018) `ev:measured` p. 8 ^ratliff2018riemannian-046
- In practice, the uninformative baseline metrics overpowered the configuration-space controllers that were designed to stabilize the system. (Ratliff et al., 2018) `ev:measured` p. 8 ^ratliff2018riemannian-047
- The comparison used 3 cluttered environments of 4 cylindrical obstacles each, with target reaching points on the opposite side. (Ratliff et al., 2018) `ev:reported` p. 8 ^ratliff2018riemannian-048
- Increasing weights on the baseline C-space controllers made the system more stable, but the task became increasingly difficult to achieve. (Ratliff et al., 2018) `ev:measured` p. 8 ^ratliff2018riemannian-049
- The experiments used up to 150 controllers, most defined in their own task space, competing for just 7 degrees of freedom. (Ratliff et al., 2018) `ev:reported` p. 8 ^ratliff2018riemannian-050
- Fighting between baseline controllers sometimes caused catastrophic events such as obstacle collisions, seen periodically for each C-space weight setting. (Ratliff et al., 2018) `ev:measured` p. 8 ^ratliff2018riemannian-051
- RMPs successfully solved all of these reaching tasks, generating smooth, predictable, and natural motion for each of them. (Ratliff et al., 2018) `ev:measured` p. 8 ^ratliff2018riemannian-052
- The retraction experiments used 4 more cluttered environments of 4 cylindrical obstacles, with 4 to 6 manually chosen configurations each. (Ratliff et al., 2018) `ev:reported` p. 8 ^ratliff2018riemannian-053
- The IK-guided long-range navigation policy was very successful in worlds and problems where the retract heuristics were successful. (Ratliff et al., 2018) `ev:measured` p. 8 ^ratliff2018riemannian-054
- Long-range navigation was demonstrated on a physical Baxter robot picking objects from a table into a container below it. (Ratliff et al., 2018) `ev:reported` p. 8 ^ratliff2018riemannian-055
- The authors observe that the same controllers behave surprisingly consistently from robot to robot, aside from adjusting for differing length scales. (Ratliff et al., 2018) `ev:asserted` p. 8 ^ratliff2018riemannian-056
- The authors suggest data-driven heuristics such as deep learning for long-range navigation as an interesting direction for future work. (Ratliff et al., 2018) `ev:asserted` p. 8 ^ratliff2018riemannian-057
- The second retraction heuristic successfully retracts from all 20 trial configurations in the retraction experiment environments. (Ratliff et al., 2018) `ev:measured` p. 9 ^ratliff2018riemannian-058
- The simpler retraction heuristic solves all trials except two from the rightmost world, which generally has obstacles closer to the robot. (Ratliff et al., 2018) `ev:measured` p. 9 ^ratliff2018riemannian-059
- Recursive pullback and combination of RMPs over a tree of task spaces is independent of the computational path taken. (Ratliff et al., 2018) `ev:computed` p. 12 ^ratliff2018riemannian-060
- The result at the tree root is optimal with respect to a metric-weighted least-squares objective over desired task accelerations. (Ratliff et al., 2018) `ev:computed` p. 12 ^ratliff2018riemannian-061
- The obstacle avoidance RMP combines an exponentially decaying repulsive term along the distance gradient with a velocity-dependent damping term. (Ratliff et al., 2018) `ev:reported` p. 13 ^ratliff2018riemannian-062
- Near joint limits, the sigmoid pullback scales Jacobian columns toward zero, reducing the final policy's dependency on those joints. (Ratliff et al., 2018) `ev:computed` p. 14 ^ratliff2018riemannian-063
- Motion optimization reduces to a stream of RMPs formed from time-varying affine policies with Q-function Hessians as metrics. (Ratliff et al., 2018) `ev:computed` p. 15 ^ratliff2018riemannian-064

## 🎯 Contributions


## 📖 Glossary

- **Riemannian Motion Policy (RMP)** — Second-order acceleration policy paired with a state-dependent Riemannian metric.
- **Pullback** — Transforms an RMP from a task space into the domain of its task map.
- **Pushforward** — Transforms an RMP from the domain of a task map to its codomain.
- **Metric-weighted average** — Combination of RMPs weighting each policy's acceleration by its metric.
- **Directionally stretched metric** — Metric emphasizing one direction, approximately the outer product of a normalized vector.
- **Unresolved form** — Force-space RMP representation, analogous to natural parameters of a Gaussian.
- **Retract heuristic** — Policy pulling the arm back to a canonical retracted configuration among obstacles.
- **Operational space control** — Control formalism combining task-space objectives through optimal least-squares acceleration resolution.

## ❓ Open questions

- How do RMP-based local policies perform when the elbow is blocked and the retract heuristics fail?
- Can data-driven pattern recognition learn better long-range navigation heuristics than the hand-designed retract heuristics?
- How should touch and force feedback be integrated as reactive RMPs for dexterous manipulation?
- How large is the effect of dropping the curvature term in the acceleration approximation at slower control rates?
- What quantitative success rates and motion quality metrics separate RMPs from the pseudoinverse baselines beyond the qualitative video comparison?

## 📝 Notes on reading

Version read: arXiv 1801.02854v3 (25 Jul 2018), matching the packet identifier. The experiments are reported mostly qualitatively; side-by-side comparisons are deferred to a supplementary video, and no per-trial success rates are given for the baseline comparison. Figure 2 (p. 9) shows obstacle environments and retraction start configurations; its caption carries the only retraction counts (20 trials; simpler heuristic fails two). Many equations are garbled in the extraction (operator definitions on p. 4, appendix equations on pp. 10-15, cubic spline weight on p. 13); claims describe them in words only. A sentence on p. 7 is garbled (Over the we eventually blends...). The pushforward metric notation differs between the body (Eq. 12, with J+ ) and the appendix (Eq. 37, with generalized inverse and an explicit curvature term).

## Suggested new concepts

- Riemannian Motion Policy — core object reused by later RMPflow and geometric fabrics work.
- Metric-weighted policy combination — general alternative to superposition of controllers.
- Pullback of policies through task maps — geometric operator linking task and configuration spaces.
- Joint limit handling via sigmoid reparameterization — reusable trick for bounded configuration spaces.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Políticas de movimiento como (aceleración, métrica); pullback al espacio articular.
- **[[02_optimizacion_y_algoritmos]]** — Políticas + métricas; analogía con el gradiente natural (C.3).
