---
aliases: ["BCH formula"]
type: concept
element_type: method
topic: "[[Lie-group kinematics and dynamics of robot arms]]"
topics: ["[[Lie-group kinematics and dynamics of robot arms]]"]
created: 2026-09-19
---

## Working definition

A series of nested Lie brackets that expresses the logarithm of a product of two group exponentials as a single Lie algebra element, used to expand, linearise or differentiate motion on matrix Lie groups.

## Evidence

- [[Boutselis2018differential - Differential Dynamic Programming on Lie Groups#^boutselis2018differential-023]] — The paper derives a second-order expansion of the state perturbations for generic classes of discrete mechanical dynamics using the Baker-Campbell-Hausdorff formula.
- [[Boutselis2018differential - Differential Dynamic Programming on Lie Groups#^boutselis2018differential-027]] — The authors remark that the Baker-Campbell-Hausdorff expansion used for the pose perturbation does not depend on the selected affine connection.
- [[Boutselis2018differential - Differential Dynamic Programming on Lie Groups#^boutselis2018differential-066]] — A direct Taylor expansion of the pose-perturbation map gives a first-order result matching the linear terms of the BCH-based expansion.
- [[Boutselis2018differential - Differential Dynamic Programming on Lie Groups#^boutselis2018differential-067]] — The authors prefer the BCH formula for quadratic terms, noting it yields a connection-independent scheme relying on simple group operations.
- [[Prabhu2020exponentially - Exponentially Stable First Order Control on Matrix Lie#^prabhu2020exponentially-024]] — To avoid needing an analytic logarithm, the authors derive the time derivative of log(g) using the Baker-Campbell-Hausdorff formula.
- [[Prabhu2020exponentially - Exponentially Stable First Order Control on Matrix Lie#^prabhu2020exponentially-051]] — The authors suggest the modified BCH formula of Lemma 3 may yield bounds when the control input does not commute with the error.
- [[Lin2023lie - Lie Neurons Adjoint-Equivariant Neural Networks for#^lin2023lie-030]] — Truncating the BCH series to third-order terms gave a Frobenius error of 0.191 on the so(3) regression test data.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 3 sources · topic: Lie-group kinematics and dynamics of robot arms (drafter's packet `q1-lie-kinematics`, confirmed at the gate)
