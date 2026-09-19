---
aliases: []
type: topic
parent: Optimization and learning on manifolds
created: 2026-09-18
---

## Scope

Methods that treat robot configurations, poses, policies and learnable parameters as points on Riemannian manifolds or Lie groups, and that design, learn or optimize over them intrinsically: geometric reactive controllers (Riemannian motion policies, geometric fabrics, geodesic synergies), optimization on manifolds and its software (Geoopt, Pymanopt, Riemannian adaptive optimizers, Riemannian preconditioners), manifold-aware generative policies such as Riemannian flow matching, and the machinery of exponential and logarithm maps, retractions and transport that these methods share, together with differentiable solver layers that embed such geometric optimization inside trained networks. It deliberately excludes Euclidean-only policy learning (e.g. diffusion or action-chunking policies without manifold structure), information-geometric natural-gradient methods, equivariant network architectures, and pose-estimation benchmarks, which belong to neighbouring areas even when they touch rotations.

## Concepts

- [[Riemannian Motion Policies]] — A Riemannian motion policy pairs a desired-acceleration policy for a subtask with a state-dependent positive semi-definite metric that weights its directional importance, so that many subtask policies can be combined into one reactive robot controller.
- [[Riemannian optimization]] — Riemannian optimization minimizes a cost function over a search space that is a differentiable manifold, taking steps along the manifold (via exponential maps or retractions) instead of optimizing freely in Euclidean space and projecting back.
- [[Riemannian flow matching]] — Riemannian flow matching trains a continuous normalizing flow on a Riemannian manifold by regressing a vector field onto conditional vector fields defined through a premetric such as geodesic distance, which is simulation-free on manifolds with closed-form geodesics.
- [[Differentiable optimization layers]] — A differentiable optimization layer embeds a classical solver step, such as a Gauss-Newton or least-squares update, inside a neural network's computation graph so that gradients can be backpropagated through the solution to train the network end to end.
- [[Exponential map]] — The exponential map sends a tangent vector at a point of a manifold or Lie group to the point reached by following the geodesic with that initial velocity, with the logarithm map as its local inverse, and it is how updates and perturbations computed in the tangent space are applied back on the manifold.
- [[Geometric fabrics]] — Geometric fabrics are bent Finsler geometries used as reactive motion policies, in which velocity-dependent metrics and zero-work bending terms let behaviour be designed in independent parts while remaining provably stable and path consistent.
- [[Geodesic synergies]] — A geodesic synergy is a minimum-energy joint coordination given by a geodesic of the robot's configuration-space manifold under the kinetic-energy metric, and combining a few such synergies generates a wide range of physically meaningful motions.

## Subtopics

## Related topics

## ❓ Open questions

## Problems

- none yet: no problem names this topic as its topic

## History

- 2026-09-18 · Eki Gonzalez Flamarique · parent: root — new area for concepts promoted from the research batch, confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · parent: root → Optimization and learning on manifolds — grouped under the request's three axes
