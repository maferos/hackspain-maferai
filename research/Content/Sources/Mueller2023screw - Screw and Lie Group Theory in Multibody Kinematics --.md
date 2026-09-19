---
aliases: []
type: "source"
title: "Screw and Lie Group Theory in Multibody Kinematics -- Motion Representation and Recursive Kinematics of Tree-Topology Systems"
citekey: "Mueller2023screw"
doi: "10.48550/arXiv.2306.17415"
arxiv: "2306.17415"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2306.17415"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Andreas Mueller"]
sha256: ["3eab920896b2558d9f37bb6be114b69358db64388e6f830239a3da6fa821d8e4"]
pdf: "Content/Papers/Mueller2023screw.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Mueller2023screw.pdf]]

> [!abstract] One-sentence summary
> A review that uses screw and Lie group theory to formulate tree-topology multibody kinematics in joint coordinates without joint frames, deriving recursive twists and Jacobians for four twist representations.

## Abstract

After three decades of computational multibody system (MBS) dynamics, current research is centered at the development of compact and user friendly yet computationally efficient formulations for the analysis of complex MBS. The key to this is a holistic geometric approach to the kinematics modeling observing that the general motion of rigid bodies as well as the relative motion due to technical joints are screw motions. Moreover, screw theory provides the geometric setting and Lie group theory the analytic foundation for an intuitive and compact MBS modeling. The inherent frame invariance of this modeling approach gives rise to very efficient recursive $O\left( n\right) $ algorithms, for which the so-called 'spatial operator algebra' is one example, and allows for use of readily available geometric data. In this paper three variants for describing the configuration of tree-topology MBS in terms of relative coordinates, i.e. joint variables, are presented: the standard formulation using body-fixed joint frames, a formulation without joint frames, and a formulation without either joint or body-fixed reference frames. This allows for describing the MBS kinematics without introducing joint reference frames and therewith rendering the use of restrictive modeling convention, such as Denavit-Hartenberg parameters, redundant. Four different definitions of twists are recalled and the corresponding recursive expressions are derived. The corresponding Jacobians and their factorization are derived. The aim of this paper is to motivate the use of Lie group modeling and to provide a review of the different formulations for the kinematics of tree-topology MBS in terms of relative (joint) coordinates from the unifying perspective of screw and Lie group theory. (arXiv)

## 🧠 Key ideas (atomic)

- The paper aims to summarize basic concepts for modeling multibody systems in relative coordinates using joint screws, relating them to scattered existing formulations. (Mueller, 2023) `ev:asserted` p. 2 ^mueller2023screw-001
- The author states that, in general, rigid bodies perform screw motions that form a Lie group. (Mueller, 2023) `ev:asserted` p. 1 ^mueller2023screw-002
- According to the author, screw theory has almost completely been ignored for multibody system modeling, with only a few exceptions. (Mueller, 2023) `ev:asserted` p. 1 ^mueller2023screw-003
- A first class of prior approaches exploits rigid body velocity being a screw, giving rise to spatial vector formulations and spatial operator algebra. (Mueller, 2023) `ev:cited` p. 2 ^mueller2023screw-004
- The author states these first-class approaches only exploit algebraic properties of screws relevant for compact handling of velocities, accelerations, wrenches, and inertia. (Mueller, 2023) `ev:asserted` p. 2 ^mueller2023screw-005
- A second class of prior work recognizes that finite rigid body motions form the Lie group SE (3), with the screw algebra as Lie algebra. (Mueller, 2023) `ev:cited` p. 2 ^mueller2023screw-006
- The term [[Product of exponentials formula|product of exponentials]] has been used for open kinematic chains since Brockett introduced it in his work on robotic manipulators. (Mueller, 2023) `ev:cited` p. 2 ^mueller2023screw-007
- The author suggests early Lie group kinematics publications did not reach the multibody community, presumably because their mathematical concepts differ from classical formalisms. (Mueller, 2023) `ev:asserted` p. 2 ^mueller2023screw-008
- The author states frame invariance allows freely assigning reference frames, which drastically simplifies kinematics modeling and provides a direct link to CAD models. (Mueller, 2023) `ev:asserted` p. 2 ^mueller2023screw-009
- Denavit-Hartenberg and Sheth-Uicker two-frame conventions are used in most current multibody dynamics simulation packages that use relative coordinates, according to the author. (Mueller, 2023) `ev:asserted` p. 2 ^mueller2023screw-010
- The author states the Lie group description not only allows arbitrary placement of joint frames but makes them dispensable altogether. (Mueller, 2023) `ev:asserted` p. 2 ^mueller2023screw-011
- According to the author, geometric mechanics benefits in multibody dynamics are mainly recognized for flexible bodies undergoing large deformations. (Mueller, 2023) `ev:asserted` p. 2 ^mueller2023screw-012
- Lie group time integration schemes were modified and applied to multibody models in absolute coordinate formulation, according to the cited literature. (Mueller, 2023) `ev:cited` p. 2 ^mueller2023screw-013
- The author states that the O (n) formulations arising from this user-friendly modeling are not the topic of this paper. (Mueller, 2023) `ev:asserted` p. 3 ^mueller2023screw-014
- The paper introduces [[Twist representations|four twist definitions]], body-fixed, spatial, hybrid, and mixed, which differ by reference point and resolving frame. (Mueller, 2023) `ev:reported` p. 3 ^mueller2023screw-015
- For simplicity the paper considers a single open kinematic chain of n moving bodies interconnected by n 1-DOF lower pair joints. (Mueller, 2023) `ev:reported` p. 3 ^mueller2023screw-016
- Higher-DOF joints are modeled as combinations of 1-DOF lower pair joints, which the author says simplifies the formulation without losing generality. (Mueller, 2023) `ev:reported` p. 3 ^mueller2023screw-017
- Most technical joints are lower kinematic pairs characterized by surface contact, acting as mechanical generators of motion subgroups of SE (3). (Mueller, 2023) `ev:cited` p. 3 ^mueller2023screw-018
- The paper tabulates the 10 motion subgroups of SE (3) with their dimensions and the lower pairs or macro joints generating them. (Mueller, 2023) `ev:reported` p. 3 ^mueller2023screw-019
- Universal and constant velocity joints are not lower kinematic pairs, but the author notes they can be modeled by combining lower pair joints. (Mueller, 2023) `ev:asserted` p. 3 ^mueller2023screw-020
- In the joint screw description, revolute joints have pitch h = 0, whereas prismatic joints have infinite pitch. (Mueller, 2023) `ev:asserted` p. 4 ^mueller2023screw-021
- The paper assumes throughout that the two joint frames of each joint coincide in the reference configuration qi = 0. (Mueller, 2023) `ev:reported` p. 4 ^mueller2023screw-022
- The standard formulation requires two body-fixed joint frames per joint plus the joint screw coordinates represented in one of them. (Mueller, 2023) `ev:asserted` p. 5 ^mueller2023screw-023
- The author states the Lie group formulation is merely another approach to standard matrix kinematics, aiming at compact expressions without compromising efficiency. (Mueller, 2023) `ev:asserted` p. 6 ^mueller2023screw-024
- The standard Lie group formulation resembles the Sheth-Uicker convention, which the author notes still presumes certain alignment of joint axes. (Mueller, 2023) `ev:asserted` p. 6 ^mueller2023screw-025
- For multi-DOF joints, relative configuration can be written as one exponential of summed joint screws or as a [[Product of exponentials formula|product of exponentials]]. (Mueller, 2023) `ev:computed` p. 6 ^mueller2023screw-026
- Merging the two constant joint frame transformations splits each relative configuration into one constant reference part and one exponential variable part. (Mueller, 2023) `ev:computed` p. 7 ^mueller2023screw-027
- The [[Product of exponentials formula|body-fixed product-of-exponentials formulation]] needs only the relative reference configurations of adjacent bodies and joint screw coordinates in a body frame. (Mueller, 2023) `ev:asserted` p. 8 ^mueller2023screw-028
- In the [[Product of exponentials formula|spatial product-of-exponentials formula]], joint screws and absolute reference configurations are all expressed in the inertial frame at q = 0. (Mueller, 2023) `ev:computed` p. 8 ^mueller2023screw-029
- The zero reference formulation was first reported by Gupta using frame transformation matrices, and later introduced by Brockett as the [[Product of exponentials formula|POE formula]]. (Mueller, 2023) `ev:cited` p. 8 ^mueller2023screw-030
- The author states the spatial formulation has proven very useful for modeling, being in particular advantageous when processing CAD data. (Mueller, 2023) `ev:asserted` p. 9 ^mueller2023screw-031
- If all bodies are designed with respect to one global CAD reference system, then Ai = I and the joint screws coincide. (Mueller, 2023) `ev:computed` p. 9 ^mueller2023screw-032
- The worked example models a surgical device combining a three-body robot arm with a two-body remote center of motion mechanism. (Mueller, 2023) `ev:reported` p. 10 ^mueller2023screw-033
- In the example, the axes of joints 4 and 5 and the instrument intersect at one point, letting it pivot around an incision. (Mueller, 2023) `ev:reported` p. 10 ^mueller2023screw-034
- The remote center of motion mechanism model used in the example was created with the multibody system tool Alaska. (Mueller, 2023) `ev:reported` p. 9 ^mueller2023screw-035
- The author states the surgical mechanism example, with joint screws read from geometric parameters, shows the simplicity of the approach. (Mueller, 2023) `ev:asserted` p. 11 ^mueller2023screw-036
- The [[Twist representations|body-fixed twist]] of each body follows recursively from its predecessor's twist through an adjoint transformation plus the contribution of its joint. (Mueller, 2023) `ev:computed` p. 12 ^mueller2023screw-037
- The body-fixed Jacobian of body i depends only on q2 to qi, being independent from the first joint in the chain. (Mueller, 2023) `ev:computed` p. 13 ^mueller2023screw-038
- [[Twist representations|Body-fixed twists]] are left-invariant vector fields on SE (3), since they are unaffected by a change of the inertial frame. (Mueller, 2023) `ev:computed` p. 13 ^mueller2023screw-039
- The body-fixed system Jacobian factorizes into a screw transformation matrix times a block-diagonal matrix of joint screw coordinates. (Mueller, 2023) `ev:computed` p. 13 ^mueller2023screw-040
- The author identifies this 1-resolvent structure as the fundamental point of departure for many O (n) algorithms. (Mueller, 2023) `ev:asserted` p. 14 ^mueller2023screw-041
- Given twists of all bodies, a closed-form pseudoinverse yields joint rates, which the paper calls the generalized inverse kinematics problem. (Mueller, 2023) `ev:computed` p. 14 ^mueller2023screw-042
- The author suggests this overall inverse kinematics solution could be applied to human body models processing motion capture data. (Mueller, 2023) `ev:asserted` p. 14 ^mueller2023screw-043
- There is no frame invariant inner product on se (3), so no screw norm is invariant under a change of reference frame. (Mueller, 2023) `ev:cited` p. 14 ^mueller2023screw-044
- The author states the [[Twist representations|spatial twist recursion]] is the simplest possible, since body twists are added without any coordinate transformation. (Mueller, 2023) `ev:asserted` p. 15 ^mueller2023screw-045
- In spatial representation, the non-vanishing instantaneous joint screws are identical for all bodies, since the inertial frame is the only reference frame. (Mueller, 2023) `ev:computed` p. 15 ^mueller2023screw-046
- The spatial Jacobian of body i depends only on q1 to qi−1, since joint motion does not change its own screw axis. (Mueller, 2023) `ev:computed` p. 16 ^mueller2023screw-047
- Featherstone's O (n) forward dynamics method is the most prominent use of spatial representation in dynamics, but is not widely applied in MBS dynamics. (Mueller, 2023) `ev:cited` p. 16 ^mueller2023screw-048
- The author suggests this limited uptake may be due to the uncommon reference point, the inertial frame origin, where spatial entities are measured. (Mueller, 2023) `ev:asserted` p. 16 ^mueller2023screw-049
- The hybrid Jacobian recursion only involves relative displacements between bodies, rather than the complete relative configurations required by the body-fixed recursion. (Mueller, 2023) `ev:computed` p. 18 ^mueller2023screw-050
- With [[Twist representations|hybrid twists]], body inertia properties must be resolved in the inertial frame, so they become configuration dependent in the motion equations. (Mueller, 2023) `ev:asserted` p. 18 ^mueller2023screw-051
- The hybrid form is used in many recursive O (n) forward dynamics algorithms, where it is deemed computationally efficient because transformations involve only translations. (Mueller, 2023) `ev:cited` p. 18 ^mueller2023screw-052
- [[Twist representations|Mixed twists]] are used in multibody dynamics modeling because the Newton-Euler equations with respect to the center of mass become decoupled. (Mueller, 2023) `ev:cited` p. 19 ^mueller2023screw-053
- The mixed Jacobian cannot be derived via frame transformations, since its angular and translational parts are resolved in different frames. (Mueller, 2023) `ev:computed` p. 19 ^mueller2023screw-054
- The paper tabulates the transformations relating the [[Twist representations|four twist forms]] and the three joint screw coordinate representations to one another. (Mueller, 2023) `ev:reported` p. 20 ^mueller2023screw-055
- A cited study of end-effector twist computation suggests the spatial representation is computationally most efficient among the body-fixed, spatial, and hybrid forms. (Mueller, 2023) `ev:cited` p. 20 ^mueller2023screw-056
- According to the author, a conclusive computational analysis comparing [[Twist representations|all four twist representations]] has not yet been reported. (Mueller, 2023) `ev:asserted` p. 20 ^mueller2023screw-057
- The conclusions state that formulating kinematics without body-fixed joint frames gives maximal flexibility compared with conventions like Denavit-Hartenberg parameters. (Mueller, 2023) `ev:asserted` p. 21 ^mueller2023screw-058
- The author states these results were published over two decades but had not been presented within a uniform multibody framework. (Mueller, 2023) `ev:asserted` p. 21 ^mueller2023screw-059
- The recursive algorithms for evaluating the equations of motion are presented in an accompanying paper rather than in this one. (Mueller, 2023) `ev:asserted` p. 21 ^mueller2023screw-060
- A forthcoming paper will address general-topology multibody systems, with loop closure constraints formulated in the form of a [[Product of exponentials formula|product of exponentials]]. (Mueller, 2023) `ev:asserted` p. 22 ^mueller2023screw-061
- The author states that redundant loop constraints are still a major challenge for multibody systems with general topology. (Mueller, 2023) `ev:asserted` p. 22 ^mueller2023screw-062
- The author notes the direct product group SO (3) × R3 does not represent screw motions, though it is occasionally used for modeling. (Mueller, 2023) `ev:asserted` p. 27 ^mueller2023screw-063

## 🎯 Contributions

## 📖 Glossary

- **Screw motion** — rotation about a fixed axis combined with translation along it, set by the pitch.
- **SE (3)** — Lie group of rigid body motions, the special Euclidean group in three dimensions.
- **se (3)** — Lie algebra of SE (3); the algebra of screws and twists.
- **Twist** — six-vector of a rigid body's angular and translational velocity, itself a screw.
- **Product of exponentials (POE)** — chain configuration written as a product of exponentials of joint screws.
- **Joint frame (JFR)** — body-fixed frame attached at a joint to describe relative joint motion.
- **Body-fixed reference frame (BFR)** — frame attached to a body that kinematically represents it.
- **Adjoint transformation** — 6×6 matrix transforming screw coordinates between frames under a rigid transformation.
- **Lower pair** — joint with surface contact, such as revolute, prismatic or screw joints.
- **Hybrid twist** — twist measured at the body frame but resolved in the inertial frame.
- **Mixed twist** — body-fixed angular velocity combined with body-origin translational velocity resolved in the inertial frame.
- **Zero reference formulation** — kinematics expressed from joint screws measured in a single reference configuration.

## ❓ Open questions

- Which of the four twist representations is computationally most efficient for full kinematic and dynamic analysis of general MBS?
- How can redundant loop closure constraints be handled for MBS with general (closed-loop) topology within the POE framework?
- How do the joint-frame-free formulations perform in practice for large MBS models imported from CAD?
- How well does the generalized inverse kinematics solution work on noisy motion capture data for human body models?

## 📝 Notes on reading

- Version read: the cached text is the manuscript of the Multibody System Dynamics (2018) Vol. 43 article, pp. 37–70, last updated 26 May 2019, posted as arXiv 2306.17415v1 (30 Jun 2023); the packet identifier is the arXiv DOI.
- The paper is a theoretical review with no experiments; results are derivations, so claims are coded computed, asserted, reported or cited.
- Equations and matrices (e.g. eqs. 1, 5, 13, 22, 24, 33, 34, 44, 45) are garbled by the text extraction; the explicit C3 (q), body-fixed Jacobian and spatial joint screws for the RCM example (pp. 11, 21) were not claimed.
- Eq. (4) prints Si−1,1 in its middle term where Si−1,i appears intended; likely a typo in the source.
- Figures 1–9 are schematic diagrams of joint frames, the RCM mechanism and screw motion; they were described only through the text.

## Suggested new concepts

- Product of exponentials formula — central kinematic representation reused across robotics and multibody simulators.
- Zero reference formulation — enables joint-frame-free modeling directly from CAD reference configurations.
- Twist representations (body-fixed, spatial, hybrid, mixed) — recurring choice that affects the efficiency of recursive algorithms.
- Screw theory — geometric basis for joint and velocity modeling across kinematics papers.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H1.** Sustituto abierto de Murray-Li-Sastry y Lynch-Park: PoE, cuatro representaciones de giros (cuerpo, espacial, híbrida, mixta) y Jacobianos recursivos con sus derivadas.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
