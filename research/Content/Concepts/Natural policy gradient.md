---
aliases: []
type: concept
element_type: method
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-18
---

## Working definition

A policy-gradient method for reinforcement learning that preconditions the policy gradient by the inverse Fisher information of the policy, taking natural-gradient steps with a chosen step size.

## Evidence

- [[Schulman2015trust - Trust Region Policy Optimization#^schulman2015trust-034]] — The natural policy gradient is obtained as a special case of the TRPO update using a linear objective approximation with a quadratic constraint approximation.
- [[Schulman2015trust - Trust Region Policy Optimization#^schulman2015trust-035]] — Natural policy gradient treats the step size as an algorithm parameter, whereas TRPO enforces the KL divergence constraint at each update.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-009]] — ACKTR uses a Kronecker-factored approximation to natural policy gradient that allows the covariance matrix of the gradient to be inverted efficiently.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-010]] — The authors claim to be the first to extend natural policy gradient to optimize value functions via a Gauss-Newton approximation.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-017]] — The authors state that no scalable, sample-efficient and general-purpose instantiation of the natural policy gradient existed before ACKTR.

## Relations

- RELATES_TO → [[Trust region policy optimization]]
  · type: specialises
  · evidence: [[Schulman2015trust - Trust Region Policy Optimization#^schulman2015trust-034]]

## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 2 sources · topic: Information geometry and natural-gradient optimization (drafter's packet `p1-information-geometry`, confirmed at the gate)
