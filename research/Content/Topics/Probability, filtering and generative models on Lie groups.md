---
aliases: []
type: topic
parent: Geometry of motion and representation
created: 2026-09-19
---

## Scope

Methods that represent and manipulate uncertainty over states living on Lie groups and other Riemannian manifolds: invariant and error-state filters on matrix Lie groups (the invariant EKF and the group-affine condition behind its guarantees, concentrated Gaussians defined through the exponential map, observability and consistency of such estimators), and generative models that learn and sample distributions on SO(3), SE(3), spheres, tori and general manifolds (Riemannian score-based and diffusion models, SE(3) diffusion for poses, grasps and protein frames). Deliberately out of scope: deterministic motion generation, control and optimization on Lie groups or Riemannian manifolds (covered by Riemannian and Lie-group methods for robot motion and optimization), the design of equivariant network architectures in themselves (Equivariant networks and rotation representations), pose-estimation pipelines and benchmarks (6D object pose estimation), and end-to-end robot policies (Visuomotor and vision-language-action robot policies), except where they are the application that a probabilistic model on a group is evaluated in.

## Concepts

- [[Invariant extended Kalman filter]] — An extended Kalman filter for states on a matrix Lie group that linearizes an invariant (left or right group) error instead of a vector difference, so that for group-affine systems the error dynamics are exactly log-linear and independent of the estimate.
- [[Group-affine dynamics]] — The class of dynamics on a Lie group (condition (7) of Barrau and Bonnabel, which includes left- and right-invariant dynamics and reduces to affine dynamics on a vector space) for which the invariant estimation error evolves autonomously and its logarithm obeys an exact linear equation.
- [[Diffusion models on Lie groups]] — Score-based or denoising diffusion generative models whose noising and denoising processes are defined directly on a Lie group such as SO(3) or SE(3), used to sample multimodal distributions of rotations and rigid poses for pose estimation, grasping, manipulation and protein frames.
- [[Riemannian diffusion models]] — The family of diffusion and score-based generative models that extend continuous-time Euclidean diffusion to data on Riemannian manifolds by noising with manifold Brownian or Langevin dynamics and learning the reverse process, trained either by Riemannian score matching or by a Riemannian continuous-time ELBO.

## Subtopics

## Related topics

## ❓ Open questions

## Problems

- none yet: no problem names this topic as its topic

## History

- 2026-09-19 · Eki Gonzalez Flamarique · parent: root — new area for concepts promoted from the gap-research batch (04_huecos_y_ampliacion), confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · parent: root → Geometry of motion and representation — grouped under the request's three axes
