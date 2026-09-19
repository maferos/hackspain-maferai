---
aliases: []
type: "source"
title: "Geometric Fabrics: Generalizing Classical Mechanics to Capture the Physics of Behavior"
citekey: "Wyk2021geometric"
doi: "10.48550/arXiv.2109.10443"
arxiv: "2109.10443"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2109.10443"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Karl Van Wyk", "Mandy Xie", "Anqi Li", "Muhammad Asif Rana", "Buck Babich", "Bryan Peele", "Qian Wan", "Iretiayo Akinola", "Balakumar Sundaralingam", "Dieter Fox", "Byron Boots", "Nathan D. Ratliff"]
sha256: ["49cabb92e79ab30d83fa7824c0bf48e452ac3de6335ca18e0576b20c6449e5f9"]
pdf: "Content/Papers/Wyk2021geometric.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 70
---

📄 PDF: [[Wyk2021geometric.pdf]]

> [!abstract] One-sentence summary
> The paper generalizes classical mechanics into geometric fabrics, bent Finsler systems that keep stability guarantees while matching RMP expressivity, and shows they outperform a hardened RMP implementation on a simulated Franka arm.

## Abstract

Classical mechanical systems are central to controller design in energy shaping methods of geometric control. However, their expressivity is limited by position-only metrics and the intimate link between metric and geometry. Recent work on Riemannian Motion Policies (RMPs) has shown that shedding these restrictions results in powerful design tools, but at the expense of theoretical stability guarantees. In this work, we generalize classical mechanics to what we call geometric fabrics, whose expressivity and theory enable the design of systems that outperform RMPs in practice. Geometric fabrics strictly generalize classical mechanics forming a new physics of behavior by first generalizing them to Finsler geometries and then explicitly bending them to shape their behavior while maintaining stability. We develop the theory of fabrics and present both a collection of controlled experiments examining their theoretical properties and a set of robot system experiments showing improved performance over a well-engineered and hardened implementation of RMPs, our current state-of-the-art in controller design. (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that classical mechanical systems have fundamentally limited expressivity when behavior is designed in parts, such as target reaching with obstacle avoidance. (Van Wyk et al., 2021) `ev:asserted` p. 1 ^wyk2021geometric-001
- Earlier work on [[Riemannian Motion Policies]] demonstrated that removing the restrictions of classical mechanics can result in powerful design tools. (Van Wyk et al., 2021) `ev:cited` p. 1 ^wyk2021geometric-002
- The authors state that [[Riemannian Motion Policies|RMPs]] sacrifice theoretical insight for expressivity, forcing practitioners to gain experience before becoming proficient. (Van Wyk et al., 2021) `ev:asserted` p. 1 ^wyk2021geometric-003
- [[Geometric fabrics]] are defined as bent Finsler geometries, where Finsler systems give velocity-dependent metrics and bending terms enable independent shaping of associated policies. (Van Wyk et al., 2021) `ev:asserted` p. 1 ^wyk2021geometric-004
- The work develops an expressive class of RMPs that are stable, path consistent, and agnostic to parameterization, which the authors call covariant. (Van Wyk et al., 2021) `ev:asserted` p. 1 ^wyk2021geometric-005
- To the authors' knowledge, geometric fabrics, results on constrained fabrics and energization, and the fabric component algebra are novel. (Van Wyk et al., 2021) `ev:asserted` p. 2 ^wyk2021geometric-006
- The authors note that Pullback Bundle Dynamical Systems require task policies to be strictly Riemannian, a subset of the HD2 geometries of fabrics. (Van Wyk et al., 2021) `ev:cited` p. 2 ^wyk2021geometric-007
- Control Lyapunov Functions project unstable systems onto a Lyapunov stable class, which the authors say introduces potentially large projection errors. (Van Wyk et al., 2021) `ev:cited` p. 2 ^wyk2021geometric-008
- The authors now view Geometric Dynamical Systems, an earlier stable class of [[Riemannian Motion Policies|RMPs]], as better expressed as Finsler systems, which are unbent fabrics. (Van Wyk et al., 2021) `ev:asserted` p. 2 ^wyk2021geometric-009
- Combining classical mechanical systems yields a combined acceleration that is a metric-weighted average of the constituent policies, with mass matrices as priority weights. (Van Wyk et al., 2021) `ev:computed` p. 3 ^wyk2021geometric-010
- Classical priority metrics cannot represent velocity-aware priorities, such as a barrier avoidance task that should forget the barrier when moving away. (Van Wyk et al., 2021) `ev:asserted` p. 3 ^wyk2021geometric-011
- In classical systems, geometric forces are intrinsically linked to the metric that also acts as priority matrix; only one of the two can be designed. (Van Wyk et al., 2021) `ev:asserted` p. 3 ^wyk2021geometric-012
- The authors state that this metric-geometry coupling results in fighting between components or forces an over-reliance on potentials and dampers. (Van Wyk et al., 2021) `ev:asserted` p. 3 ^wyk2021geometric-013
- Position-dependent potentials can induce spring-like oscillations when damping is insufficient, according to the authors' analysis of classical behavior design. (Van Wyk et al., 2021) `ev:asserted` p. 3 ^wyk2021geometric-014
- Task hierarchies with null-space projection are described as often pragmatic and somewhat artificial solutions to the metric and potential conflicts of classical systems. (Van Wyk et al., 2021) `ev:asserted` p. 3 ^wyk2021geometric-015
- [[Geometric fabrics]] are presented as a strict generalization of classical mechanics, with classical systems being one type of fabric. (Van Wyk et al., 2021) `ev:asserted` p. 3 ^wyk2021geometric-016
- Adding a modifying term to a forced, damped Finsler system keeps energy decreasing at the damping rate if and only if it does zero work. (Van Wyk et al., 2021) `ev:computed` p. 4 ^wyk2021geometric-017
- Bending terms are defined as zero-work modifications that are additionally homogeneous of degree 2 in velocity, making the unforced system geometric. (Van Wyk et al., 2021) `ev:asserted` p. 4 ^wyk2021geometric-018
- The classical constraint force keeping a system moving along a constraint surface is given as an example of a bending term. (Van Wyk et al., 2021) `ev:asserted` p. 4 ^wyk2021geometric-019
- Under equality constraints, a [[Geometric fabrics|constrained geometric fabric]] is shown to be itself a geometric fabric with a modified bending term. (Van Wyk et al., 2021) `ev:computed` p. 4 ^wyk2021geometric-020
- With a lower-bounded potential and bounded positive-definite damping, a [[Geometric fabrics|forced geometric fabric]] converges to a local minimum of the constrained potential minimization problem. (Van Wyk et al., 2021) `ev:computed` p. 5 ^wyk2021geometric-021
- The stability theorem also holds under contact models acting as equality constraints that dissipate in contact and conserve or dissipate energy on impact. (Van Wyk et al., 2021) `ev:computed` p. 5 ^wyk2021geometric-022
- Any HD2 geometry can be energized with a Finsler energy by adding only an acceleration along the direction of motion, yielding an energy-conserving system. (Van Wyk et al., 2021) `ev:computed` p. 5 ^wyk2021geometric-023
- The energized system obtained from an HD2 geometry and a Finsler energy is proven to be a [[Geometric fabrics|geometric fabric]], termed an energized fabric. (Van Wyk et al., 2021) `ev:computed` p. 5 ^wyk2021geometric-024
- The authors interpret completeness as giving independent control over priority metric design through the Finsler metric and geometric policy design through the desired geometry. (Van Wyk et al., 2021) `ev:asserted` p. 5 ^wyk2021geometric-025
- With a Euclidean energy, energization projects the geometric policy's accelerations orthogonal to the velocity, curving the system without changing its speed. (Van Wyk et al., 2021) `ev:computed` p. 5 ^wyk2021geometric-026
- The pullback of a Lagrangian's Euler-Lagrange equations of motion equals the Euler-Lagrange equations of the pulled-back Lagrangian, per the paper's derivation. (Van Wyk et al., 2021) `ev:computed` p. 5 ^wyk2021geometric-027
- A constrained energized system in generalized coordinates can be constructed by first pulling back the metric-weighted geometry and then energizing it directly there. (Van Wyk et al., 2021) `ev:computed` p. 5 ^wyk2021geometric-028
- The authors find it often useful to design fabrics in parts, each an HD2 geometric policy paired with a Finsler energy on a transform-tree node. (Van Wyk et al., 2021) `ev:asserted` p. 6 ^wyk2021geometric-029
- A fabric component pairs a Finsler energy with a force term, and components combine through scaled sums and pullbacks across differentiable maps. (Van Wyk et al., 2021) `ev:asserted` p. 6 ^wyk2021geometric-030
- Component summation is linear, and pullback across a composition of maps equals the successive pullbacks across each map. (Van Wyk et al., 2021) `ev:computed` p. 6 ^wyk2021geometric-031
- The final fabric is the energization of the root geometry formed by recursively pulling back components from child to parent and summing them. (Van Wyk et al., 2021) `ev:computed` p. 6 ^wyk2021geometric-032
- Dampers scaled by the mass matrix act solely along the direction of motion, which the authors use to regulate speed without affecting the behavior. (Van Wyk et al., 2021) `ev:asserted` p. 6 ^wyk2021geometric-033
- HD2 terms are typically designed by scaling an HD0 term, depending at most on velocity direction, by a measure of Finsler energy. (Van Wyk et al., 2021) `ev:asserted` p. 6 ^wyk2021geometric-034
- Particle experiments compare unbent Riemannian, unbent Finsler, bent Riemannian and bent Finsler systems attracting particles past a circular obstacle toward a target. (Van Wyk et al., 2021) `ev:reported` p. 6 ^wyk2021geometric-035
- Each particle system variant was run under two different speeds, vd = 2, 4, to analyze path consistency under speed changes. (Van Wyk et al., 2021) `ev:reported` p. 7 ^wyk2021geometric-036
- In every variant, all particles avoided the object and reached the target except the one shot directly at the object's local minimum. (Van Wyk et al., 2021) `ev:measured` p. 7 ^wyk2021geometric-037
- Unbent fabrics showed more pronounced changes in particle paths across the two speed levels in the obstacle-avoidance experiments. (Van Wyk et al., 2021) `ev:measured` p. 7 ^wyk2021geometric-038
- Unbent Finsler systems with a velocity-gated obstacle metric produced launching artifacts that were amplified when traveling at higher velocity. (Van Wyk et al., 2021) `ev:measured` p. 7 ^wyk2021geometric-039
- In the particle experiments, [[Geometric fabrics|geometric fabrics]] produced more consistent paths across speed levels without any launching artifacts. (Van Wyk et al., 2021) `ev:measured` p. 7 ^wyk2021geometric-040
- Finsler metrics facilitated straight-line motion to the desired location once past the obstacle by letting the system forget it as a function of directionality. (Van Wyk et al., 2021) `ev:measured` p. 7 ^wyk2021geometric-041
- Particles under Riemannian metrics were seen clinging to the obstacle even once past it, since those metrics cannot represent directional dependence. (Van Wyk et al., 2021) `ev:measured` p. 7 ^wyk2021geometric-042
- The repulsive forces of unbent fabrics consistently pushed the center particle farther out from the object than geometric fabrics did. (Van Wyk et al., 2021) `ev:measured` p. 7 ^wyk2021geometric-043
- The authors state that [[Geometric fabrics|geometric fabrics]] allow heightened obstacle avoidance behavior without shifting the system minima. (Van Wyk et al., 2021) `ev:asserted` p. 7 ^wyk2021geometric-044
- Robot experiments used one geometric fabric on a 7 degree-of-freedom Franka Panda arm, designed once and tested across a variety of problems. (Van Wyk et al., 2021) `ev:reported` p. 7 ^wyk2021geometric-045
- The fabric was compared with the authors' best-performing RMP, with both policies evaluated at 100 Hz and integrated with first-order Euler routines. (Van Wyk et al., 2021) `ev:reported` p. 7 ^wyk2021geometric-046
- The robot experiments were run only in simulation, the authors arguing that the [[Sim-to-real transfer|sim-to-real gap]] is minimal for pure motion generation. (Van Wyk et al., 2021) `ev:reported` p. 7 ^wyk2021geometric-047
- The Franka geometric fabric policy consisted of only three differently designed components, each pairing a Finsler energy with a policy. (Van Wyk et al., 2021) `ev:reported` p. 7 ^wyk2021geometric-048
- One distance-space repulsion design was deployed for joint-limit avoidance, self-collision avoidance, and object-collision avoidance on the Franka arm. (Van Wyk et al., 2021) `ev:reported` p. 8 ^wyk2021geometric-049
- In the repulsion component, geometric policies were weighted significantly higher than potentials, which acted as a soft penalty on the obstacle constraint. (Van Wyk et al., 2021) `ev:reported` p. 8 ^wyk2021geometric-050
- The repulsion potential was included to shift the system minima away from numerical singularities that arise as the distance approaches zero. (Van Wyk et al., 2021) `ev:reported` p. 8 ^wyk2021geometric-051
- In the wall barrier approach, both policies exhibited sub-millimeter convergence error when the target was 10 cm or more from the wall. (Van Wyk et al., 2021) `ev:measured` p. 8 ^wyk2021geometric-052
- RMP convergence already started degrading at ∼9 cm from the wall, whereas geometric fabric convergence began degrading only at ∼6 cm. (Van Wyk et al., 2021) `ev:measured` p. 8 ^wyk2021geometric-053
- The authors attribute the later degradation of fabrics near the wall to much of the boundary policy being encoded in a geometric policy. (Van Wyk et al., 2021) `ev:asserted` p. 8 ^wyk2021geometric-054
- [[Geometric fabrics]] on average approached the wall about 50% closer than the RMP in the wall barrier experiment. (Van Wyk et al., 2021) `ev:measured` p. 8 ^wyk2021geometric-055
- In ring constricted navigation, the ring radius decreased from 17 cm to 13 cm, with rings built from spheres of radius 2.5 cm. (Van Wyk et al., 2021) `ev:reported` p. 8 ^wyk2021geometric-056
- The [[Geometric fabrics|geometric fabric]] let the robot pass through all rings to reach its target, whereas the RMP could not pass the last two rings. (Van Wyk et al., 2021) `ev:measured` p. 8 ^wyk2021geometric-057
- The dynamic obstacle task required reaching 19 randomly generated end-effector targets, one every 5 seconds, with objects reaching speeds of up to 0.39 m/s. (Van Wyk et al., 2021) `ev:reported` p. 8 ^wyk2021geometric-058
- The robot reached 16 targets with the geometric fabric policy, compared with 11 targets with the [[Riemannian Motion Policies|RMP]], in the dynamic obstacle task. (Van Wyk et al., 2021) `ev:measured` p. 8 ^wyk2021geometric-059
- The [[Geometric fabrics|geometric fabric policy]] yielded a 0.4% collision rate versus 8.18% for the [[Riemannian Motion Policies|RMP]], measured as the percentage of time steps in collision. (Van Wyk et al., 2021) `ev:measured` p. 8 ^wyk2021geometric-060
- The authors attribute higher target acquisition to the predominantly geometric avoidance component, which stays influential without preventing optimization of the end-effector potential. (Van Wyk et al., 2021) `ev:asserted` p. 9 ^wyk2021geometric-061
- The authors state that the [[Riemannian Motion Policies|RMP]] had to balance repulsion against target acquisition, a compromise that resulted in diminished performance. (Van Wyk et al., 2021) `ev:asserted` p. 9 ^wyk2021geometric-062
- The authors state that techniques such as reinforcement learning, imitation learning and planning can naturally leverage fabrics, a point of future work. (Van Wyk et al., 2021) `ev:asserted` p. 9 ^wyk2021geometric-063
- Finsler systems with velocity-dependent metrics carry additional velocity-derived mass and Christoffel terms, which the authors describe as critical for covariance. (Van Wyk et al., 2021) `ev:computed` p. 12 ^wyk2021geometric-064
- Earlier [[Riemannian Motion Policies|RMP]] results used high gains on forcing potentials and damping terms to reject the irrelevant geometric terms that resulted from coupled metrics. (Van Wyk et al., 2021) `ev:cited` p. 12 ^wyk2021geometric-065
- Speed regulation stays stable as long as the regulation coefficient is below the energization coefficient, acting as a nonzero damper on the energized system. (Van Wyk et al., 2021) `ev:computed` p. 16 ^wyk2021geometric-066
- The constrained experiment solved a discretized program with ∆t = 0.04s using a Gauss-Newton optimizer with four iterations per time step. (Van Wyk et al., 2021) `ev:reported` p. 19 ^wyk2021geometric-067
- With the end-effector constrained to a plane, the robot maintained the constraint at the micrometer level in the supplementary constrained fabric experiment. (Van Wyk et al., 2021) `ev:measured` p. 19 ^wyk2021geometric-068
- In the plane-constrained experiment, the end-effector settled to within 1 mm of the closest point on the plane to the target. (Van Wyk et al., 2021) `ev:measured` p. 19 ^wyk2021geometric-069
- The authors note that the geometric fabric system of the robot experiments is subject to local minima since the target attractor is greedy. (Van Wyk et al., 2021) `ev:asserted` p. 19 ^wyk2021geometric-070

## 🎯 Contributions

## 📖 Glossary

- **Geometric fabric** — A Finsler geometry bent by zero-work, HD2 bending terms; strictly generalizes classical mechanics.
- **Finsler structure** — Speed-independent, positive homogeneous length measure whose energy yields velocity-dependent metrics.
- **HD2 geometry** — Differential equation whose acceleration term scales quadratically with velocity, giving speed-independent paths.
- **Bending term** — Zero-work, HD2 force that reshapes a Finsler geometry without changing energy.
- **Energization** — Adding acceleration along motion so an HD2 geometry conserves a chosen Finsler energy.
- **Pullback** — Transforming a system from a task space into generalized coordinates through a map's Jacobian.
- **Transform tree** — Tree of task spaces linked by differentiable maps, used to compose policies.
- **Fabric component** — Pair of a Finsler energy and a force term, combined by sums and pullbacks.
- **Riemannian Motion Policy (RMP)** — Acceleration policy paired with a priority metric, composed via RMPflow.
- **Path consistency** — Property that trajectories follow the same geometric path regardless of speed.

## ❓ Open questions

- How do geometric fabrics perform on physical robots, given that all Franka experiments were simulated?
- Can learned perturbations, as in DMPs, be layered on fabrics while keeping stability guarantees in practice?
- How can global navigation heuristics be learned over a nominal fabric to escape local minima of the greedy attractor?
- Can intrinsically covariant subclasses of HD2 geometries and bending terms be derived without being overly restrictive?
- How do fabrics integrate with optimal control or reinforcement learning when used as the underlying dynamics?
- How sensitive are fabric designs to their many hand-tuned gains compared with RMPs?

## 📝 Notes on reading

Version read: arXiv 2109.10443v2 (18 Jan 2022), the IEEE RA-L preprint version with appendices; pages 10-19 are appendices and references.

Fig. 1 (particle trajectories for the four system variants at two speeds), Fig. 2 (wall barrier), Fig. 3 (ring navigation), Fig. 4 (dynamic obstacles) and Fig. 5 (plane-constrained reaching) could only be described from the text.

Inconsistency on p. 7: the discussion says the unbent fabrics are in the left column, but the later sentence refers to the unbent fabrics as the right column as well as the geometric fabrics; likely a typo.

Appendix E (pp. 15-16) contains broken cross-references (Subsection ??). Many equations in the extraction are garbled (superscripts, hats and tildes lost); no claims were made on equation details beyond their stated meaning.

The cubby navigation result on p. 19 is reported from a companion paper (reference [28], Section XI), not from experiments in this paper.

## Suggested new concepts

- Geometric fabrics — core framework generalizing classical mechanics for stable, expressive reactive motion generation.
- Riemannian Motion Policies — the baseline controller framework that fabrics aim to make stable.
- Finsler geometry — velocity-dependent metric geometry underlying priority design in fabrics.
- Energy shaping — classical geometric-control approach that fabrics generalize.
- Reactive collision avoidance — shared application area for the Franka experiments on dynamic obstacles.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Estabilidad garantizada con geometrías de Finsler (C.3).
