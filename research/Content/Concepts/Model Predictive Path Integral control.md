---
aliases: ["MPPI", "Model-Predictive Path Integral Control"]
type: concept
element_type: method
topic: "[[Trajectory optimization and model predictive control for arms]]"
topics: ["[[Trajectory optimization and model predictive control for arms]]"]
created: 2026-09-19
---

## Working definition

A sampling-based model predictive controller that perturbs a nominal control sequence with noise, rolls out the samples, and moves the nominal controls toward the average of the samples weighted by their exponentiated negative cost, applying only the first input before replanning.

## Evidence

- [[Fazlyab2026model - Model Predictive Path Integral Control as Preconditioned#^fazlyab2026model-002]] — Standard MPPI shifts the nominal control toward a cost-weighted average of sampled perturbed control sequences drawn from the sampling distribution.
- [[Fazlyab2026model - Model Predictive Path Integral Control as Preconditioned#^fazlyab2026model-008]] — Wagener et al. showed that an exponential-utility trajectory objective yields classical MPPI under a fixed-covariance Gaussian family with unit step size.
- [[Fazlyab2026model - Model Predictive Path Integral Control as Preconditioned#^fazlyab2026model-027]] — For the fixed-covariance Gaussian family, choosing preconditioner Σ/τ with unit step size recovers exactly the classical MPPI update.
- [[Fazlyab2026model - Model Predictive Path Integral Control as Preconditioned#^fazlyab2026model-032]] — Exact unit-step MPPI satisfies the descent guarantees of Theorem 1 when the squared whitened feasible-set diameter is below 12.
- [[Fazlyab2026model - Model Predictive Path Integral Control as Preconditioned#^fazlyab2026model-053]] — On the Dubins car task, single-step MPPI selects a suboptimal path, which the authors attribute to it not iterating until convergence.
- [[Pezzato2023sampling - Sampling-based Model Predictive Control Leveraging#^pezzato2023sampling-001]] — The authors propose an MPPI controller that uses the GPU-parallelizable IsaacGym simulator to compute the forward dynamics of the robot and environment.
- [[Pezzato2023sampling - Sampling-based Model Predictive Control Leveraging#^pezzato2023sampling-023]] — For the Panda arm, the average MPPI time to goal was 0.8s, compared with 9.6s for fabrics and 4.2s for ForcesPro MPC.
- [[Bhardwaj2021storm - STORM An Integrated Framework for Fast Joint-Space#^bhardwaj2021storm-003]] — Sampling-based methods such as MPPI and CEM make no restrictive assumptions about the cost, dynamics or policy class.
- [[Bhardwaj2021storm - STORM An Integrated Framework for Fast Joint-Space#^bhardwaj2021storm-008]] — The mean of the Gaussian policy is updated with the same equation as the Model-Predictive Path Integral Control algorithm.
- [[Bhardwaj2021storm - STORM An Integrated Framework for Fast Joint-Space#^bhardwaj2021storm-009]] — Standard implementations of MPPI on real systems generally do not update the covariance of the sampling distribution.
- [[Williams2017information - Information Theoretic Model Predictive Control Theory and#^williams2017information-026]] — The path integral derivation requires control-affine dynamics, whereas the information theoretic setting allows dynamics given by an arbitrary non-linear function.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 4 sources · topic: Trajectory optimization and model predictive control for arms (drafter's packet `q3-trajectory-control`, confirmed at the gate)
