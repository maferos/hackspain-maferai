---
aliases: []
type: "source"
title: "Screw and Lie Group Theory in Multibody Dynamics -- Recursive Algorithms and Equations of Motion of Tree-Topology Systems"
citekey: "Mueller2023screw2"
doi: "10.48550/arXiv.2306.17793"
arxiv: "2306.17793"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2306.17793"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Andreas Mueller"]
sha256: ["43c0f6524855a817b677195ba01b69c8e8146cca80da95301f983ecfc56f786d"]
pdf: "Content/Papers/Mueller2023screw2.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Mueller2023screw2.pdf]]

> [!abstract] One-sentence summary
> Mueller derives recursive O(n) Newton-Euler inverse dynamics algorithms for body-fixed, spatial and hybrid twist representations in a frame-invariant Lie group setting, compares their operation counts, and gives closed-form Euler-Jourdain and Lagrange motion equations plus derivative and integration extensions.

## Abstract

Screw and Lie group theory allows for user-friendly modeling of multibody systems (MBS) while at the same they give rise to computationally efficient recursive algorithms. The inherent frame invariance of such formulations allows for use of arbitrary reference frames within the kinematics modeling (rather than obeying modeling conventions such as the Denavit-Hartenberg convention) and to avoid introduction of joint frames. The computational efficiency is owed to a representation of twists, accelerations, and wrenches that minimizes the computational effort. This can be directly carried over to dynamics formulations. In this paper recursive $O\left( n\right) $ Newton-Euler algorithms are derived for the four most frequently used representations of twists, and their specific features are discussed. These formulations are related to the corresponding algorithms that were presented in the literature. The MBS motion equations are derived in closed form using the Lie group formulation. One are the so-called 'Euler-Jourdain' or 'projection' equations, of which Kane's equations are a special case, and the other are the Lagrange equations. The recursive kinematics formulations are readily extended to higher orders in order to compute derivatives of the motions equations. To this end, recursive formulations for the acceleration and jerk are derived. It is briefly discussed how this can be employed for derivation of the linearized motion equations and their time derivatives. The geometric modeling allows for direct application of Lie group integration methods, which is briefly discussed. (arXiv)

## 🧠 Key ideas (atomic)

- The paper aims to present established O (n) formulations in a common geometric setting that allows flexible and user-friendly multibody modeling. (Mueller, 2023) `ev:asserted` p. 1 ^mueller2023screw2-001
- According to the author, the screw formulation of multibody kinematics does not involve body-fixed joint frames. (Mueller, 2023) `ev:asserted` p. 1 ^mueller2023screw2-002
- Frame invariance of the geometric Lie group formulation makes it independent from modeling conventions such as the Denavit-Hartenberg convention. (Mueller, 2023) `ev:asserted` p. 2 ^mueller2023screw2-003
- The author states that this frame invariance allows direct processing of CAD data in multibody modeling. (Mueller, 2023) `ev:asserted` p. 2 ^mueller2023screw2-004
- The author notes there is no established Lie group algorithm that fully exploits the freedom to choose different motion representations. (Mueller, 2023) `ev:asserted` p. 2 ^mueller2023screw2-005
- The [[Product of exponentials formula|product of exponentials formula]], introduced by Brockett, is the central relation of Lie group algorithms for tree-topology multibody systems. (Mueller, 2023) `ev:cited` p. 2 ^mueller2023screw2-006
- The partial derivative of a body-fixed instantaneous joint screw with respect to a joint coordinate equals a screw product of two joint screws. (Mueller, 2023) `ev:computed` p. 3 ^mueller2023screw2-007
- The time derivative of the body-fixed system Jacobian factors into a compact matrix product involving the system Jacobian itself. (Mueller, 2023) `ev:computed` p. 3 ^mueller2023screw2-008
- The compact acceleration relation yields a unique solution of the inverse kinematics problem on acceleration level. (Mueller, 2023) `ev:computed` p. 4 ^mueller2023screw2-009
- Computing the body-fixed jerk requires only computationally simple nested screw products for its quadratic or cubic terms. (Mueller, 2023) `ev:computed` p. 4 ^mueller2023screw2-010
- Explicit determination of the very involved higher-order Jacobian derivatives can be avoided by recursive evaluation, as shown in earlier work. (Mueller, 2023) `ev:cited` p. 4 ^mueller2023screw2-011
- The time derivative of a spatial joint screw equals the Lie bracket of the spatial twist with that joint screw. (Mueller, 2023) `ev:computed` p. 4 ^mueller2023screw2-012
- Featherstone termed the Lie bracket the 'spatial cross product', viewing it as an extension of Euler's formula to screws. (Mueller, 2023) `ev:cited` p. 4 ^mueller2023screw2-013
- Together with the concise time derivative, recursive higher-order derivatives make the spatial representation computationally very attractive, according to the author. (Mueller, 2023) `ev:asserted` p. 5 ^mueller2023screw2-014
- In the hybrid representation the Jacobian derivative lacks the convective term from angular motion, so only the linear part appears. (Mueller, 2023) `ev:computed` p. 5 ^mueller2023screw2-015
- The derived hybrid jerk relations are the core relations of the so-called 'spatial vector' formulation in the literature. (Mueller, 2023) `ev:cited` p. 6 ^mueller2023screw2-016
- In spatial representation the rigid-body momentum balance attains the simplest possible form, with momentum rate equal to applied wrench. (Mueller, 2023) `ev:computed` p. 6 ^mueller2023screw2-017
- The author notes that the spatial momentum balance does not involve any vectorial operation, for example cross products. (Mueller, 2023) `ev:asserted` p. 7 ^mueller2023screw2-018
- Any numerical discretization of the spatial momentum balance easily preserves spatial momentum in the absence of external wrenches, as Borri discussed. (Mueller, 2023) `ev:cited` p. 7 ^mueller2023screw2-019
- The spatial Newton-Euler equations exhibit the skew symmetry property, since the mass matrix derivative minus twice the matrix Cs is skew symmetric. (Mueller, 2023) `ev:computed` p. 7 ^mueller2023screw2-020
- The body-fixed Newton-Euler equations remain coupled even when the centre-of-mass frame is used as reference, owing to body-fixed twists. (Mueller, 2023) `ev:computed` p. 8 ^mueller2023screw2-021
- The hybrid Newton-Euler equations with respect to the centre of mass are decoupled, unlike the body-fixed equations. (Mueller, 2023) `ev:computed` p. 8 ^mueller2023screw2-022
- The hybrid Newton-Euler equations for an arbitrary body-fixed reference frame are simpler than the corresponding body-fixed equations. (Mueller, 2023) `ev:computed` p. 8 ^mueller2023screw2-023
- Newton-Euler equations in an arbitrary frame follow by frame transformation of the spatial momentum balance, with spatial and body-fixed forms as special cases. (Mueller, 2023) `ev:computed` p. 9 ^mueller2023screw2-024
- Recursive methods using [[Twist representations|different twist representations]] give algorithmically equivalent methods with different computational costs, according to the author. (Mueller, 2023) `ev:asserted` p. 10 ^mueller2023screw2-025
- The author declares a detailed computational analysis, as well as forward dynamics algorithms, beyond the scope of this paper. (Mueller, 2023) `ev:asserted` p. 10 ^mueller2023screw2-026
- The author states that a comparative study of the recursive algorithms' complexity is still due, to be part of further research. (Mueller, 2023) `ev:asserted` p. 10 ^mueller2023screw2-027
- In total, the [[Recursive Newton-Euler algorithm|body-fixed recursive Newton-Euler algorithm]] needs 3 (n −1) frame transformations for a chain of n bodies with 1-DOF joints. (Mueller, 2023) `ev:computed` p. 11 ^mueller2023screw2-028
- The [[Recursive Newton-Euler algorithm|body-fixed recursive Newton-Euler algorithm]] additionally needs 2n−1 Lie brackets for a kinematic chain of n bodies. (Mueller, 2023) `ev:computed` p. 11 ^mueller2023screw2-029
- The Lie bracket in the body-fixed acceleration recursion can be simplified because the joint screw vector is sparse, often with one non-zero entry. (Mueller, 2023) `ev:asserted` p. 11 ^mueller2023screw2-030
- The [[Recursive Newton-Euler algorithm|spatial recursive Newton-Euler algorithm]] needs n screw coordinate transformations, n second-order tensor transformations, plus 2n −1 Lie brackets. (Mueller, 2023) `ev:computed` p. 12 ^mueller2023screw2-031
- If implemented directly, the inertia tensor transformation costs as much as two screw transformations, so the spatial algorithm's complexity would equal the body-fixed one. (Mueller, 2023) `ev:computed` p. 12 ^mueller2023screw2-032
- An O (n) forward dynamics algorithm based on canonical Hamilton equations was shown to require less numerical operations than Newton-Euler-based O (n) algorithms. (Mueller, 2023) `ev:cited` p. 12 ^mueller2023screw2-033
- O (n) algorithms based on the spatial representation can be computationally more efficient than those based on body-fixed or hybrid representations. (Mueller, 2023) `ev:cited` p. 12 ^mueller2023screw2-034
- The author expects a further reduction of computational costs from an O (n) algorithm using spatial momenta. (Mueller, 2023) `ev:asserted` p. 12 ^mueller2023screw2-035
- For purely kinematic analysis, the spatial forward recursion is more efficient than the body-fixed or hybrid versions, disregarding transformations to local frames. (Mueller, 2023) `ev:cited` p. 13 ^mueller2023screw2-036
- Earlier work showed a body-fixed O (n) forward dynamics algorithm with joint-aligned reference frames can need less effort than the spatial version. (Mueller, 2023) `ev:cited` p. 13 ^mueller2023screw2-037
- The author considers joint-aligned body reference frames, needed for this sparsity, a restraining presumption from a user's perspective. (Mueller, 2023) `ev:asserted` p. 13 ^mueller2023screw2-038
- Among three derived hybrid acceleration recursions, the author finds recursion (72) the most efficient from a computational perspective. (Mueller, 2023) `ev:computed` p. 13 ^mueller2023screw2-039
- The [[Recursive Newton-Euler algorithm|hybrid recursive Newton-Euler algorithm]] needs 3n −3 translational transformations of screw coordinates, besides n rotational ones. (Mueller, 2023) `ev:computed` p. 14 ^mueller2023screw2-040
- The [[Recursive Newton-Euler algorithm|hybrid recursive Newton-Euler algorithm]] needs 3n −1 Lie brackets, besides n rotational transformations of the inertia tensor. (Mueller, 2023) `ev:computed` p. 14 ^mueller2023screw2-041
- Although its operation count equals the body-fixed version, the hybrid algorithm uses computationally simple transformations, motivating extensive use in forward dynamics. (Mueller, 2023) `ev:asserted` p. 14 ^mueller2023screw2-042
- A canonical-momentum O (n) forward dynamics algorithm in hybrid representation performed comparably to Featherstone's method using spatial twists. (Mueller, 2023) `ev:cited` p. 14 ^mueller2023screw2-043
- The description of the multibody geometry is independent from the chosen [[Twist representations|representation of twists]], according to the author. (Mueller, 2023) `ev:asserted` p. 14 ^mueller2023screw2-044
- If body reference frames coincide with the inertial frame in the reference configuration, no body reference configurations need to be determined. (Mueller, 2023) `ev:asserted` p. 15 ^mueller2023screw2-045
- With inertia data taken relative to one construction frame, the required kinematic data reduce to joint direction and position vectors. (Mueller, 2023) `ev:asserted` p. 15 ^mueller2023screw2-046
- The only computational drawback of this frame choice is that the hybrid Newton-Euler equations are no longer decoupled. (Mueller, 2023) `ev:asserted` p. 15 ^mueller2023screw2-047
- Jourdain's principle of virtual power applied to the body-fixed Newton-Euler equations yields a system of n motion equations. (Mueller, 2023) `ev:computed` p. 15 ^mueller2023screw2-048
- Explicit evaluation of the Euler-Jourdain equations leads to the [[Recursive Newton-Euler algorithm|recursive body-fixed inverse dynamics algorithm]] presented in section 4.1. (Mueller, 2023) `ev:computed` p. 15 ^mueller2023screw2-049
- Combining the Euler-Jourdain equations with the twist relation yields a first-order system of n + 6n ODEs with block triangular structure. (Mueller, 2023) `ev:computed` p. 15 ^mueller2023screw2-050
- From a numerical point of view, the spatial momentum formulation in phase space shall allow momentum preserving integration schemes. (Mueller, 2023) `ev:asserted` p. 16 ^mueller2023screw2-051
- The body-fixed Euler-Jourdain equations are equivalent to Kane's equations, where the instantaneous joint screws are called partial velocities. (Mueller, 2023) `ev:cited` p. 16 ^mueller2023screw2-052
- Due to the block triangular form of the body-fixed Jacobian, solving the Euler-Jourdain equations immediately leads to an O (n) forward dynamics algorithm. (Mueller, 2023) `ev:computed` p. 16 ^mueller2023screw2-053
- Concise expressions for the generalized mass matrix plus the Coriolis matrix allow construction of the Lagrange equations in closed form. (Mueller, 2023) `ev:computed` p. 17 ^mueller2023screw2-054
- The Christoffel symbols of the first kind admit closed-form expressions in Lie group notation built from Jacobian partial derivatives. (Mueller, 2023) `ev:computed` p. 17 ^mueller2023screw2-055
- The Christoffel symbol expression simplifies when Binet's inertia tensor replaces the ordinary inertia tensor in the mass matrix. (Mueller, 2023) `ev:computed` p. 17 ^mueller2023screw2-056
- The author states that the potential benefit of [[Twist representations|spatial or hybrid twists]] for closed-form equations of motion remains to be explored. (Mueller, 2023) `ev:asserted` p. 17 ^mueller2023screw2-057
- The equations of motion depend non-linearly on the generalized coordinates, whereas they are linear in the dynamic parameters. (Mueller, 2023) `ev:asserted` p. 17 ^mueller2023screw2-058
- Because higher Jacobian derivatives are algebraic closed-form screw-product expressions, the linearized equations of motion can be evaluated recursively or in closed form. (Mueller, 2023) `ev:computed` p. 18 ^mueller2023screw2-059
- Parameterizing the constant geometry transformations with screw coordinates lets the sensitivity with respect to multibody geometry be expressed in closed form. (Mueller, 2023) `ev:cited` p. 18 ^mueller2023screw2-060
- Time derivatives of the inverse dynamics solution are required for flatness-based controllers of robots with series elastic actuators. (Mueller, 2023) `ev:cited` p. 18 ^mueller2023screw2-061
- The Lie group inverse dynamics formulation yields rather compact algorithms for time derivatives of the equations of motion, as earlier work showed. (Mueller, 2023) `ev:cited` p. 18 ^mueller2023screw2-062
- The author notes that, classically, there is no singularity-free global parameterization of rotations with three parameters. (Mueller, 2023) `ev:asserted` p. 19 ^mueller2023screw2-063
- Munthe-Kaas type integration needs no global parameterization, since integration proceeds in terms of incremental Lie algebra parameters. (Mueller, 2023) `ev:cited` p. 19 ^mueller2023screw2-064
- Proper rigid body motions are frequently incorrectly represented by SO (3)×R3 in geometric integration schemes for absolute coordinates. (Mueller, 2023) `ev:cited` p. 19 ^mueller2023screw2-065
- Most O (n) algorithms in the literature used the [[Twist representations|hybrid representation of twists]], according to the author. (Mueller, 2023) `ev:asserted` p. 19 ^mueller2023screw2-066
- The spatial representation is receiving increased attention since it easily gives rise to structure preserving integration schemes. (Mueller, 2023) `ev:asserted` p. 19 ^mueller2023screw2-067
- The author regards the spatial formulation as the formulation of choice for structure preserving Lie group integration schemes. (Mueller, 2023) `ev:asserted` p. 19 ^mueller2023screw2-068

## 🎯 Contributions

## 📖 Glossary

- **Twist** — Screw coordinate vector combining a rigid body's angular and translational velocity.
- **Wrench (co-screw)** — Force and moment pair acting on a twist as a linear operator.
- **Body-fixed representation** — Twists measured and resolved in the body's own reference frame.
- **Spatial representation** — Twists measured and resolved at the inertial frame origin.
- **Hybrid representation** — Spatial angular velocity with translational velocity of the body frame origin.
- **Mixed representation** — Body-fixed angular velocity with translational velocity resolved in the inertial frame.
- **Product of exponentials (POE)** — Forward kinematics as a product of joint-screw exponentials on SE(3).
- **Lie bracket / screw product** — Operation ad on se(3), also called the spatial cross product.
- **Euler-Jourdain equations** — Projection of body Newton-Euler equations onto admissible motions via the system Jacobian.
- **Recursive Newton-Euler algorithm** — O(n) forward kinematics pass followed by backward wrench recursion for joint forces.
- **Christoffel symbols** — Coefficients of the quadratic velocity terms in the Lagrange equations.
- **Munthe-Kaas integration** — Lie group integrator solving ODEs on the Lie algebra with local parameters.

## ❓ Open questions

- Which twist representation gives the lowest operation count once the recursive algorithms are implemented and benchmarked side by side?
- Do forward dynamics algorithms inherit the same ranking of representations as the inverse dynamics operation counts?
- Can an O(n) algorithm using spatial momenta actually reduce computational cost below existing spatial or hybrid methods?
- What do spatial or hybrid twists offer for the closed-form Lagrange equations derived here only with body-fixed twists?
- How should Featherstone's spatial algorithm and Naudet's canonical-momentum algorithm be combined in practice?

## 📝 Notes on reading

Read the arXiv version 2306.17793v1 (30 June 2023), which is a re-posting of the journal article in Multibody System Dynamics Vol. 42 (2018), pp. 219–248, DOI 10.1007/s11044-017-9583-6; the registry year 2023 is the arXiv posting.

The abstract says recursive Newton-Euler algorithms are derived for the four most frequently used twist representations, but section 4 gives recursive algorithms only for body-fixed, spatial and hybrid forms; the mixed form appears only as Newton-Euler equations (section 3.4) and kinematic relations (section 2.4).

The paper is purely theoretical: no numerical experiments, timings or benchmarks; operation counts in section 4 are counts of frame transformations and Lie brackets, not measured runtimes. The authors state a comparative study is still due.

Equations are garbled throughout the extraction (subscripts, hats, tildes, matrices flattened); claims describe their meaning rather than their symbols. Equation numbering has a duplicate (two equations labelled (2) on p. 3). This paper is the companion of reference [62] (the kinematics part), whose appendix relations are summarized in appendix A.

## Suggested new concepts

- Twist representations (body-fixed, spatial, hybrid, mixed) — central choice affecting algorithm cost across rigid-body dynamics libraries.
- Recursive Newton-Euler algorithm — the standard O(n) inverse dynamics method underlying simulators such as MuJoCo.
- Product of exponentials formula — frame-invariant forward kinematics that avoids Denavit-Hartenberg conventions.
- Lie group time integration — integration on SE(3) without global rotation parameterization, relevant for simulation stability.
- Euler-Jourdain (projection) equations — closed-form motion equations equivalent to Kane's equations.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H1.** Newton-Euler recursivo O(n) y ecuaciones de movimiento en forma cerrada con Ad y ad, versión abierta de Park et al. (1995) y Featherstone.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
