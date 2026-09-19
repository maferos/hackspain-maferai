---
aliases: []
type: concept
element_type: concept
topic: "[[Riemannian and Lie-group methods for robot motion and optimization]]"
topics: ["[[Riemannian and Lie-group methods for robot motion and optimization]]"]
created: 2026-09-18
---

## Working definition

The exponential map sends a tangent vector at a point of a manifold or Lie group to the point reached by following the geodesic with that initial velocity, with the logarithm map as its local inverse, and it is how updates and perturbations computed in the tangent space are applied back on the manifold.

## Evidence

- [[Becigneul2018riemannian - Riemannian Adaptive Optimization Methods#^becigneul2018riemannian-006]] — Bonnabel defines Riemannian SGD by moving along the exponential map in the direction of the negative scaled Riemannian gradient.
- [[Becigneul2018riemannian - Riemannian Adaptive Optimization Methods#^becigneul2018riemannian-007]] — When the exponential map is not known in closed form, it is common to replace it by a retraction, most often x plus v.
- [[Becigneul2018riemannian - Riemannian Adaptive Optimization Methods#^becigneul2018riemannian-010]] — The RSGD update is intrinsic to the manifold since it only involves the exponential map and the Riemannian gradient.
- [[Becigneul2018riemannian - Riemannian Adaptive Optimization Methods#^becigneul2018riemannian-043]] — Replacing the true exponential map with its first-order retraction unexpectedly led to convergence to lower loss values, in RSGD and adaptive methods.
- [[Kochurov2020geoopt - Geoopt Riemannian Optimization in PyTorch#^kochurov2020geoopt-010]] — The Riemannian gradient descent update moves the point along the exponential map of the negative learning-rate-scaled ascent direction.
- [[Kochurov2020geoopt - Geoopt Riemannian Optimization in PyTorch#^kochurov2020geoopt-030]] — Geoopt uses retraction as a first-order approximation of the exponential map during optimization, often keeping a separate expmap method.
- [[Kochurov2020geoopt - Geoopt Riemannian Optimization in PyTorch#^kochurov2020geoopt-031]] — For some manifolds, Geoopt provides variants that perform the actual exponential map instead of retraction during optimization.
- [[Chen2023flow - Flow Matching on General Geometries#^chen2023flow-015]] — On simple manifolds the intermediate point is computed in closed form using the exponential and logarithm maps, giving a highly scalable objective.
- [[Teed2021tangent - Tangent Space Backpropagation for 3D Transformation Groups#^teed2021tangent-019]] — The differential is generalized to Lie groups by replacing vector addition and subtraction with perturbations applied through the exponential map in the tangent space.
- [[Teed2021tangent - Tangent Space Backpropagation for 3D Transformation Groups#^teed2021tangent-056]] — When θ or σ is small, second order Taylor approximations of the exponential maps are used to avoid numerical issues.
- [[Wang2022pypose - PyPose A Library for Robot Learning with Physics-based#^wang2022pypose-014]] — To avoid division by zero in terms such as sin x over x, PyPose computes the exponential map with a Taylor expansion.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (5 sources) · topic: Riemannian and Lie-group methods for robot motion and optimization (drafter's packet `p2-riemannian-robot-motion`, confirmed at the gate)
