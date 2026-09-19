---
aliases: ["TRPO"]
type: concept
element_type: method
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-18
---

## Working definition

A policy-optimization algorithm that maximizes a surrogate advantage objective subject to a bound on the average KL divergence between old and new policies, solved with conjugate gradient on Fisher-vector products and a line search.

## Evidence

- [[Schulman2015trust - Trust Region Policy Optimization#^schulman2015trust-002]] — A series of approximations to the theoretically-justified algorithm yields a practical algorithm that the authors call trust region policy optimization (TRPO).
- [[Schulman2015trust - Trust Region Policy Optimization#^schulman2015trust-019]] — To take larger steps robustly, TRPO replaces the KL penalty with a trust region constraint on the KL divergence between policies.
- [[Schulman2015trust - Trust Region Policy Optimization#^schulman2015trust-021]] — TRPO instead uses a heuristic approximation that constrains the average KL divergence over states sampled from the old policy.
- [[Schulman2015trust - Trust Region Policy Optimization#^schulman2015trust-031]] — Each TRPO update approximately solves the constrained optimization problem with the conjugate gradient algorithm followed by a line search.
- [[Schulman2015trust - Trust Region Policy Optimization#^schulman2015trust-032]] — TRPO estimates the Fisher information matrix analytically from the Hessian of the KL divergence rather than from the covariance of gradients.
- [[Schulman2015trust - Trust Region Policy Optimization#^schulman2015trust-045]] — Single path and vine TRPO solved all of the locomotion problems, yielding the best solutions among the compared algorithms.
- [[Schulman2017proximal - Proximal Policy Optimization Algorithms#^schulman2017proximal-003]] — The authors note that TRPO is not compatible with architectures that include noise, such as dropout, or parameter sharing.
- [[Schulman2017proximal - Proximal Policy Optimization Algorithms#^schulman2017proximal-008]] — TRPO maximizes a surrogate objective subject to a constraint on the mean KL divergence between the old and new policies.
- [[Schulman2017proximal - Proximal Policy Optimization Algorithms#^schulman2017proximal-009]] — TRPO uses a hard constraint rather than a penalty because choosing a single penalty coefficient that works across problems is hard.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-005]] — TRPO avoids explicitly storing or inverting the Fisher matrix by relying on Fisher-vector products instead of the exact matrix.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-006]] — The authors argue TRPO is impractical for large models, since it typically needs many conjugate gradient steps for a single parameter update.
- [[Wu2017scalable - Scalable trust-region method for deep RL using#^wu2017scalable-033]] — TRPO could only learn two of the six Atari games, Seaquest and Pong, within 10 million timesteps.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 3 sources · topic: Information geometry and natural-gradient optimization (drafter's packet `p1-information-geometry`, confirmed at the gate)
