---
aliases: []
type: "source"
title: "Stein Variational Ergodic Surface Coverage with SE(3) Constraints"
citekey: "Li2026stein"
doi: "10.48550/arXiv.2603.09458"
arxiv: "2603.09458"
year: 2026
publication_type: "preprint"
url: "https://arxiv.org/abs/2603.09458"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Jiayun Li", "Yufeng Jin", "Sangli Teng", "Dejian Gong", "Georgia Chalvatzaki"]
sha256: ["42d3964ca1316dc0a0b8a8606667915b992c3e741b62198642b7dea233ff55a6"]
pdf: "Content/Papers/Li2026stein.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[Li2026stein.pdf]]

> [!abstract] One-sentence summary
> The paper introduces TSVEC, a Gauss-Newton-preconditioned Stein Variational Gradient Descent on SE(3) that plans ergodic coverage trajectories over point-cloud surfaces, escaping the poor local minima that trap optimization-based planners on a six-object benchmark and a real robot drawing task.

## Abstract

Surface manipulation tasks require robots to generate trajectories that comprehensively cover complex 3D surfaces while maintaining precise end-effector poses. Existing ergodic trajectory optimization (TO) methods demonstrate success in coverage tasks, while struggling with point-cloud targets due to the nonconvex optimization landscapes and the inadequate handling of SE(3) constraints in sampling-as-optimization (SAO) techniques. In this work, we introduce a preconditioned SE(3) Stein Variational Gradient Descent (SVGD) approach for SAO ergodic trajectory generation. Our proposed approach comprises multiple innovations. First, we reformulate point-cloud ergodic coverage as a manifold-aware sampling problem. Second, we derive SE(3)-specific SVGD particle updates, and, third, we develop a preconditioner to accelerate TO convergence. Our sampling-based framework consistently identifies superior local optima compared to strong optimization-based and SAO baselines while preserving the SE(3) geometric structure. Experiments on a 3D point-cloud surface coverage benchmark and robotic surface drawing tasks demonstrate that our method achieves superior coverage quality with tractable computation in our setting relative to existing TO and SAO approaches, and is validated in real-world robot experiments. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that point-cloud ergodic coverage formulations create highly non-convex landscapes with numerous local minima that trap continuous optimization-based planners. (Li et al., 2026) `ev:asserted` p. 1 ^li2026stein-001
- Existing sampling-as-optimization methods using sampling or flow matching are said to fail to properly handle the SE(3) manifold geometry. (Li et al., 2026) `ev:cited` p. 1 ^li2026stein-002
- The authors state that flow-based and score-based sampling-as-optimization methods suffer from severe ill-conditioning in long-horizon trajectory optimization problems. (Li et al., 2026) `ev:asserted` p. 1 ^li2026stein-003
- The paper proposes TSVEC, a preconditioned SE(3) Stein Variational Gradient Descent framework for ergodic trajectory optimization with discrete point-cloud input. (Li et al., 2026) `ev:asserted` p. 1 ^li2026stein-004
- A key contribution is a principled derivation extending Stein Variational Gradient Descent from Euclidean space to the SE(3) manifold. (Li et al., 2026) `ev:asserted` p. 1 ^li2026stein-005
- Surface ergodic coverage is reformulated as a nonlinear least-squares problem to admit a Gauss-Newton preconditioner compatible with SE(3) SVGD. (Li et al., 2026) `ev:asserted` p. 1 ^li2026stein-006
- Ergodic trajectory optimization generates trajectories that asymptotically visit regions in proportion to their information content, following earlier foundational work. (Li et al., 2026) `ev:cited` p. 1 ^li2026stein-007
- Code, data, and video for the method are released publicly in a GitHub repository named tsvec. (Li et al., 2026) `ev:reported` p. 1 ^li2026stein-008
- Heat equation-driven approaches such as HEDAC are reported to perform poorly in continuous trajectory optimization, remaining heavily influenced by initialization. (Li et al., 2026) `ev:cited` p. 2 ^li2026stein-009
- Flow-based ergodic criteria using Sinkhorn divergence or Maximum Mean Discrepancy are described as prohibitively expensive for trajectory optimization with large point clouds. (Li et al., 2026) `ev:cited` p. 2 ^li2026stein-010
- Earlier sampling methods for ergodic search using SVGD are described as computationally slow and lacking awareness of SE(3) manifold constraints. (Li et al., 2026) `ev:cited` p. 2 ^li2026stein-011
- [[Gaussian Process Motion Planning|GPMP]] extensions to Lie groups use locally linear tangent-space approximations that can accumulate linearization errors over long horizons. (Li et al., 2026) `ev:cited` p. 2 ^li2026stein-012
- The authors state that Riemannian, projected and orthogonal-gradient SVGD variants are not specifically designed for the SE(3) Lie group structure. (Li et al., 2026) `ev:cited` p. 2 ^li2026stein-013
- The ergodic objective is written as a frequency-weighted nonlinear least-squares discrepancy between trajectory statistics and target distribution Fourier coefficients. (Li et al., 2026) `ev:reported` p. 2 ^li2026stein-014
- For point clouds, a smooth target is built by diffusing the cloud and applying a graph Fourier transform of the Laplace–Beltrami operator. (Li et al., 2026) `ev:cited` p. 2 ^li2026stein-015
- The method perturbs SE(3) poses by right multiplication with the matrix exponential of a six-dimensional Lie algebra vector. (Li et al., 2026) `ev:reported` p. 3 ^li2026stein-016
- The derivation shows the se(3) adjoint has zero trace, reducing the SE(3) SVGD entropy term to the trace of the vector field Jacobian. (Li et al., 2026) `ev:computed` p. 4 ^li2026stein-017
- Parallel transport of tangent vectors between particle poses is computed with the SE(3) adjoint to aggregate gradients consistently across particles. (Li et al., 2026) `ev:reported` p. 4 ^li2026stein-018
- The authors state that ergodic trajectories spanning several hundred steps cause severe ill-conditioning that necessitates preconditioners to accelerate convergence. (Li et al., 2026) `ev:asserted` p. 4 ^li2026stein-019
- The inference uses a Boltzmann likelihood whose energy sums smoothness, surface normal alignment, surface attachment and ergodic metric terms along the trajectory. (Li et al., 2026) `ev:reported` p. 4 ^li2026stein-020
- The method assumes access to a twice continuously differentiable signed distance function whose gradient is normalized to unit norm. (Li et al., 2026) `ev:reported` p. 4 ^li2026stein-021
- All energy terms are written in sum-of-squares form, which enables Gauss–Newton-style preconditioning with the residual Jacobian product as metric. (Li et al., 2026) `ev:reported` p. 5 ^li2026stein-022
- The preconditioned update solves a linear system of kernel-weighted Gauss–Newton metrics plus outer products of parallel-transported kernel gradients. (Li et al., 2026) `ev:reported` p. 5 ^li2026stein-023
- The authors describe kernel-weighted averaging of Gauss–Newton metrics as a computational compromise necessary for algorithmic feasibility of the preconditioner. (Li et al., 2026) `ev:asserted` p. 5 ^li2026stein-024
- The kernel sums per-time-step SE(3) Gaussian kernels, which the authors say simplifies computation and mitigates degradation from high-dimensional particles. (Li et al., 2026) `ev:asserted` p. 5 ^li2026stein-025
- Extending the framework to Augmented Lagrangian constrained optimization for strict constraint compliance is left by the authors for future work. (Li et al., 2026) `ev:asserted` p. 5 ^li2026stein-026
- The benchmark uses meshes with colored point-cloud regions of interest intentionally positioned at distant locations to rigorously test the optimizers. (Li et al., 2026) `ev:reported` p. 5 ^li2026stein-027
- All compared methods represented object geometry with a neural SDF implemented in JAX, with object training completing within 10 seconds. (Li et al., 2026) `ev:reported` p. 5 ^li2026stein-028
- Experiments ran on a single RTX 4080 GPU in single precision, using a CUDA-accelerated nearest-neighbor implementation with K=60. (Li et al., 2026) `ev:reported` p. 5 ^li2026stein-029
- Single-point baselines were Optax LBFGS with quaternion projection, IPOPT in Lie algebra coordinates, and the CHOMP-like Gauss–Newton planner GN. (Li et al., 2026) `ev:reported` p. 5 ^li2026stein-030
- Particle baselines were vanilla Stein Ergodic adapted to SE(3), plus Batch GN running parallel GN without the Stein variational mechanism. (Li et al., 2026) `ev:reported` p. 6 ^li2026stein-031
- Benchmark trajectories had 200 steps, producing an optimization problem with 1400 decision variables for each trajectory. (Li et al., 2026) `ev:reported` p. 6 ^li2026stein-032
- The energy weights for smoothness, alignment, attachment and ergodic terms were set to 5.0, 3.0, 3.0, and 0.1 respectively. (Li et al., 2026) `ev:reported` p. 6 ^li2026stein-033
- All methods used straight-line initialization connecting the two furthest colored point clouds, with start poses aligned to the world frame. (Li et al., 2026) `ev:reported` p. 6 ^li2026stein-034
- Particle-based methods added white noise with 0.005 variance to each via point to avoid infinitely large kernel gradients from overlapping particles. (Li et al., 2026) `ev:reported` p. 6 ^li2026stein-035
- The number of principal components in the ergodic representation was set to 300 to capture complex surface patterns. (Li et al., 2026) `ev:reported` p. 6 ^li2026stein-036
- The authors state that kernelized Stein discrepancy is too expensive and unstable, leaving no reasonable stopping criterion for TSVEC or SE. (Li et al., 2026) `ev:asserted` p. 6 ^li2026stein-037
- TSVEC was run for a fixed maximum of 1000 iterations with a step size of 0.1 in the benchmark. (Li et al., 2026) `ev:reported` p. 6 ^li2026stein-038
- Since vanilla Stein Ergodic suffers from convergence issues, it was allowed 9999 iterations, ten times more, with a step size of 0.02. (Li et al., 2026) `ev:reported` p. 6 ^li2026stein-039
- All particle-based methods used 100 particles, and the authors found that 500 particles did not incur memory issues on one GPU. (Li et al., 2026) `ev:reported` p. 6 ^li2026stein-040
- Kernel lengths were set to 0.05 for all benchmark objects except the torus, which used 0.1 for more exploration. (Li et al., 2026) `ev:reported` p. 6 ^li2026stein-041
- The authors found a mean adaptive kernel-length heuristic less effective than expected and removed it from the current framework. (Li et al., 2026) `ev:asserted` p. 6 ^li2026stein-042
- Benchmark results are mean values over 10 runs, with iteration count and final objective value as the key evaluation criteria. (Li et al., 2026) `ev:reported` p. 6 ^li2026stein-043
- L-BFGS rarely achieves satisfactory performance in the benchmark, with direct quaternion clipping causing premature termination of the optimizer. (Li et al., 2026) `ev:measured` p. 6 ^li2026stein-044
- IPOPT performs considerably better than L-BFGS but outperforms the GN planner only once, in the low surface curvature case. (Li et al., 2026) `ev:measured` p. 6 ^li2026stein-045
- GN consistently surpasses the L-BFGS and IPOPT baselines in both convergence iterations and final objective values across the benchmark. (Li et al., 2026) `ev:measured` p. 6 ^li2026stein-046
- Batch GN consistently outperforms single GN on the benchmark, which the authors note aligns with their expectations. (Li et al., 2026) `ev:measured` p. 6 ^li2026stein-047
- TSVEC consistently achieves superior performance across all benchmark scenarios, obtaining significantly better objective values than all competing approaches. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-048
- The authors attribute the convergence difficulties of Stein Ergodic to the severely ill-conditioned problem created by the 200-step trajectory. (Li et al., 2026) `ev:asserted` p. 7 ^li2026stein-049
- The authors observed that the ergodic objective exhibits slight non-smoothness due to the nearest-neighbor search required for its evaluation. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-050
- On the Pig scene, TSVEC reached a total objective of 1.07e-2, compared with 2.99e-2 for Batch GN and 3.37e-2 for GN. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-051
- On the Spot scene, TSVEC reached a total objective of 8.29e-3, compared with 1.99e-2 for Batch GN and 3.28e-1 for IPOPT. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-052
- On the Mustard Bottle scene, TSVEC reached a total objective of 9.10e-2, compared with 1.33e-1 for Batch GN. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-053
- On the Torus scene, TSVEC reached a total objective of 6.08e-2, compared with 9.10e-2 for Batch GN and 6.62e-1 for IPOPT. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-054
- L-BFGS failed on the Pig scene, where every entry of its row in the benchmark table is marked as a method failure. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-055
- The Stein Ergodic baseline reached total objectives between 3.59e-1 and 2.79e+0 across the six benchmark scenes after 9999 iterations. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-056
- GN converged in 36 to 60 iterations, taking between 0.317 and 0.525 seconds across the six benchmark scenarios. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-057
- TSVEC took between 138 and 145 seconds for its 1000 iterations across the six benchmark scenarios on one GPU. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-058
- In the real-world task, a Franka Emika Panda tracked TSVEC trajectories on a cooking pot with 22 cm diameter and 16 cm height. (Li et al., 2026) `ev:reported` p. 7 ^li2026stein-059
- TSVEC task-space trajectories were converted to joint commands with a sequential MuJoCo inverse-kinematics planner using damped least squares, warm-started each step. (Li et al., 2026) `ev:reported` p. 7 ^li2026stein-060
- In the drawing task, the GN planner is largely unable to produce recognizable characters, as it frequently becomes trapped in local minima. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-061
- In the surface drawing task, TSVEC generates trajectories that are mostly recognizable, in contrast with the Gauss–Newton planner GN. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-062
- The authors report that TSVEC substantially reduces the number of trials required to obtain usable trajectories in the drawing task. (Li et al., 2026) `ev:measured` p. 7 ^li2026stein-063
- The authors conclude that TSVEC is effective and robust for ergodic trajectory optimization on discrete point cloud surfaces with non-convexity and SE(3) constraints. (Li et al., 2026) `ev:asserted` p. 7 ^li2026stein-064

## 🎯 Contributions

## 📖 Glossary

- **Ergodic trajectory optimization** — Planning trajectories whose time-averaged visitation matches a target spatial distribution.
- **Ergodic metric** — Weighted Fourier-coefficient discrepancy between trajectory statistics and target distribution.
- **SVGD** — Particle-based variational inference moving particles by kernel-smoothed score plus repulsive kernel force.
- **Sampling-as-optimization (SAO)** — Using sampling over many particles to escape local optima of an objective.
- **SE(3)** — Lie group of rigid-body poses combining 3D rotation and translation.
- **Parallel transport** — Moving tangent vectors between tangent spaces while preserving their geometric meaning.
- **Gauss–Newton preconditioner** — Approximate Hessian from residual Jacobians used to rescale gradient steps.
- **Kernelized Stein discrepancy (KSD)** — Kernel-based measure of how far particles deviate from a target.
- **Neural SDF** — Neural network representing a signed distance function to an object surface.
- **TSVEC** — Task-space Stein Variational Ergodic Coverage, the method proposed in this paper.

## ❓ Open questions

- Can a cheap, stable stopping criterion replace fixed iteration counts for TSVEC, given KSD is too expensive?
- How does TSVEC scale with more particles (e.g. 500) in coverage quality, not only memory?
- Does an Augmented Lagrangian extension achieve strict surface-contact and alignment constraints without losing exploration?
- How sensitive are results to kernel length, which had to be hand-set per object (torus vs others)?
- Can drawing quality on the real robot be quantified rather than judged as recognizable?
- Would the approach transfer to tactile or force-controlled surface tasks where contact dynamics matter?

## 📝 Notes on reading

Version read: arXiv 2603.09458v3 (22 May 2026), 8 pages, matching the packet identifier. Most equations (Eqs. 1–22) are garbled by extraction; they were described in words rather than quoted. Figures 1–5 are described only in captions: Fig. 1 shows the robot drawing 'ICRA' and a heart on a pot; Fig. 2 a torus point cloud before and after graph diffusion; Fig. 3 the SE(3) SVGD parallel-transport mechanism; Fig. 4 the six benchmark objects (Mustard Bottle, Pig, Spot, Bunny, Hand, Torus); Fig. 5 the planned and IK-tracked letter 'A'. Table I (p. 7) is extracted as flattened rows; per-term energy values (Vs, Va, Vf, Ve) were not claimed individually, only total objective V, iterations and time for headline rows. Note that the paper says it does not emphasize computation time, yet Table I reports it; TSVEC is about two orders of magnitude slower than single GN per run. The real-world evaluation is qualitative: no metric or trial count is reported for 'recognizable' drawings or the reduction in trials. In Table I, TSVEC's per-term Va and Vf are not always lowest (e.g. Torus Va 6.88e-4 vs Batch GN 4.58e-4), so superiority rests on the total objective V.

## Suggested new concepts

- Stein Variational Gradient Descent on Lie groups — recurring tool for multimodal trajectory optimization with pose constraints.
- Ergodic coverage on point clouds — core formulation for surface coverage tasks such as wiping, sanding or inspection.
- Preconditioned SVGD — Gauss–Newton or Newton metrics as a fix for ill-conditioning in long-horizon particle optimization.
- Neural SDF for trajectory optimization — shared geometry representation enabling surface attachment and normal alignment costs.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H3.** SVGD precondicionado con partículas en SE(3), ejemplo reciente de optimización de trayectorias por muestreo nativa en el grupo de Lie.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
