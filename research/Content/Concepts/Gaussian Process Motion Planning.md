---
aliases: ["GPMP"]
type: concept
element_type: method
topic: "[[Trajectory optimization and model predictive control for arms]]"
topics: ["[[Trajectory optimization and model predictive control for arms]]"]
created: 2026-09-19
---

## Working definition

A trajectory optimization approach that represents a robot trajectory as a sample from a Gaussian process prior over configuration, velocity and acceleration, and optimizes it against an obstacle cost weighted with the prior cost, which keeps the solution smooth.

## Evidence

- [[Mukadam2017continuous - Continuous-Time Gaussian Process Motion Planning via#^mukadam2017continuous-013]] — GPMP combines the Gaussian process trajectory representation with a gradient descent-based optimization algorithm for motion planning.
- [[Mukadam2017continuous - Continuous-Time Gaussian Process Motion Planning via#^mukadam2017continuous-014]] — The GPMP objective combines an obstacle cost functional with a GP prior cost weighted by a trade-off parameter lambda.
- [[Mukadam2017continuous - Continuous-Time Gaussian Process Motion Planning via#^mukadam2017continuous-015]] — Unlike CHOMP, GPMP augments the trajectory with velocities and accelerations, obtaining them directly from the state rather than finite differencing.
- [[Mukadam2017continuous - Continuous-Time Gaussian Process Motion Planning via#^mukadam2017continuous-016]] — The authors state GPMP's gradient-based scheme converges slowly, requiring many iterations to reach a feasible solution.
- [[Mukadam2017continuous - Continuous-Time Gaussian Process Motion Planning via#^mukadam2017continuous-026]] — GPMP employs a constant-acceleration, jerk-minimizing prior with a Markovian state of configuration position, velocity and acceleration.
- [[Mukadam2017continuous - Continuous-Time Gaussian Process Motion Planning via#^mukadam2017continuous-048]] — Compared with CHOMP, GPMP is more expensive per iteration, primarily from computing the Hessian needed for workspace acceleration.
- [[Carvalho2023motion - Motion Planning Diffusion Learning and Planning of Robot#^carvalho2023motion-027]] — Baselines include a GPU-parallelized RRTConnect, GPMP with a straight-line prior, and a Conditional Variational AutoEncoder trajectory prior.
- [[Carvalho2023motion - Motion Planning Diffusion Learning and Planning of Robot#^carvalho2023motion-035]] — In Panda Spheres, MPD achieved a success rate of 100.0 ± .0, compared with 42.0 ± 49.4 for GPMP without an informed prior.
- [[Carvalho2023motion - Motion Planning Diffusion Learning and Planning of Robot#^carvalho2023motion-036]] — In Panda Spheres, MPD needed 1.1 ± .01 seconds of computation, compared with 194.4 ± .1 seconds for GPMP.
- [[Carvalho2023motion - Motion Planning Diffusion Learning and Planning of Robot#^carvalho2023motion-055]] — Across all environments, initializing GPMP with diffusion samples gave higher success rates than GPMP with a constant-velocity straight-line prior.
- [[Li2026stein - Stein Variational Ergodic Surface Coverage with SE(3)#^li2026stein-012]] — GPMP extensions to Lie groups use locally linear tangent-space approximations that can accumulate linearization errors over long horizons.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: top-down (3 sources) · topic: Trajectory optimization and model predictive control for arms (drafter's packet `q3-trajectory-control`, confirmed at the gate)
