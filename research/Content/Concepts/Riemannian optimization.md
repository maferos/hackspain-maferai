---
aliases: ["optimization on manifolds", "manifold optimization"]
type: concept
element_type: method
topic: "[[Riemannian and Lie-group methods for robot motion and optimization]]"
topics: ["[[Riemannian and Lie-group methods for robot motion and optimization]]"]
created: 2026-09-18
---

## Working definition

Riemannian optimization minimizes a cost function over a search space that is a differentiable manifold, taking steps along the manifold (via exponential maps or retractions) instead of optimizing freely in Euclidean space and projecting back.

## Evidence

- [[Townsend2016pymanopt - Pymanopt A Python Toolbox for Optimization on Manifolds#^townsend2016pymanopt-004]] — Optimization on manifolds, or Riemannian optimization, minimizes a cost function over a search space that admits the structure of a differentiable manifold.
- [[Townsend2016pymanopt - Pymanopt A Python Toolbox for Optimization on Manifolds#^townsend2016pymanopt-001]] — Pymanopt is a Python toolbox for optimization on manifolds that implements several manifold geometries and optimization algorithms, similarly to the Manopt Matlab toolbox.
- [[Townsend2016pymanopt - Pymanopt A Python Toolbox for Optimization on Manifolds#^townsend2016pymanopt-011]] — The authors state that combining manifold optimization with automated differentiation enables a rapid prototyping workflow that was previously unavailable to practitioners.
- [[Townsend2016pymanopt - Pymanopt A Python Toolbox for Optimization on Manifolds#^townsend2016pymanopt-013]] — The authors state that optimization on manifolds is superior to free Euclidean optimization followed by projecting parameters back onto the search space each iteration.
- [[Kochurov2020geoopt - Geoopt Riemannian Optimization in PyTorch#^kochurov2020geoopt-001]] — Geoopt is a research-oriented modular open-source package for Riemannian optimization built on top of the PyTorch dynamic computation graph backend.
- [[Kochurov2020geoopt - Geoopt Riemannian Optimization in PyTorch#^kochurov2020geoopt-026]] — Efficient Riemannian optimization in Geoopt requires update-step optimizations such as merging retractions followed by parallel transport.
- [[Kochurov2020geoopt - Geoopt Riemannian Optimization in PyTorch#^kochurov2020geoopt-049]] — The authors present Geoopt as a general-purpose optimization library for PyTorch, noting that manifold optimization appears in many applications.
- [[Kochurov2020geoopt - Geoopt Riemannian Optimization in PyTorch#^kochurov2020geoopt-058]] — Geoopt tries to fill the niche of Riemannian optimization in PyTorch, which the authors call important for geometric deep learning research.
- [[Kochurov2020geoopt - Geoopt Riemannian Optimization in PyTorch#^kochurov2020geoopt-060]] — The authors state that the main distinction between Geoopt and other Riemannian optimization solutions is in the interface.
- [[Zhang2024riemannian - Riemannian Preconditioned LoRA for Fine-Tuning Foundation#^zhang2024riemannian-005]] — The authors note that LoRA parameters live on low-rank matrices forming a quotient manifold, which motivates using Riemannian optimization tools.
- [[Zhang2024riemannian - Riemannian Preconditioned LoRA for Fine-Tuning Foundation#^zhang2024riemannian-060]] — The authors claim this is the first work to apply Riemannian optimization in designing preconditioners for fine-tuning large foundation models.
- [[Teed2021tangent - Tangent Space Backpropagation for 3D Transformation Groups#^teed2021tangent-012]] — The authors state that computing gradients directly in the tangent space removes the need to reproject gradients during manifold optimization.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 4 sources · topic: Riemannian and Lie-group methods for robot motion and optimization (drafter's packet `p2-riemannian-robot-motion`, confirmed at the gate)
