---
aliases: []
type: topic
parent: Optimization and learning on manifolds
created: 2026-09-19
---

## Scope

Methods that compute or track manipulator motions online or per query: sampling-based and gradient-based model predictive control (MPPI and its variants, GPU-parallel rollouts, simulator-as-model MPC), trajectory optimization with smoothness or learned priors (GPMP-style Gaussian process planners, cost-guided sampling), and the low-level feedback laws that execute those trajectories, such as impedance control on SE(3). It covers the cost design, convergence theory and real-time engineering of these controllers. It deliberately leaves out learned end-to-end visuomotor policies, which belong to the robot-policy area, and the general Lie-group and Riemannian machinery, which belongs to the Riemannian and Lie-group methods area even when a controller here uses it.

## Concepts

- [[Model Predictive Path Integral control]] — A sampling-based model predictive controller that perturbs a nominal control sequence with noise, rolls out the samples, and moves the nominal controls toward the average of the samples weighted by their exponentiated negative cost, applying only the first input before replanning.
- [[Gaussian Process Motion Planning]] — A trajectory optimization approach that represents a robot trajectory as a sample from a Gaussian process prior over configuration, velocity and acceleration, and optimizes it against an obstacle cost weighted with the prior cost, which keeps the solution smooth.

## Subtopics

## Related topics

## ❓ Open questions

## Problems

- none yet: no problem names this topic as its topic

## History

- 2026-09-19 · Eki Gonzalez Flamarique · parent: root — new area for concepts promoted from the gap-research batch (04_huecos_y_ampliacion), confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · parent: root → Optimization and learning on manifolds — grouped under the request's three axes
