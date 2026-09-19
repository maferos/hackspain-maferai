---
aliases: []
type: "source"
title: "Theseus: A Library for Differentiable Nonlinear Optimization"
citekey: "Pineda2022theseus"
doi: "10.48550/arXiv.2207.09442"
arxiv: "2207.09442"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2207.09442"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Luis Pineda", "Taosha Fan", "Maurizio Monge", "Shobha Venkataraman", "Paloma Sodhi", "Ricky T. Q. Chen", "Joseph Ortiz", "Daniel DeTone", "Austin Wang", "Stuart Anderson", "Jing Dong", "Brandon Amos", "Mustafa Mukadam"]
sha256: ["8495ea9528d96129ce8c95136a46ceeb81ca9aff4cbc5ace2a415404d7b607a7"]
pdf: "Content/Papers/Pineda2022theseus.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 59
---

📄 PDF: [[Pineda2022theseus.pdf]]

> [!abstract] One-sentence summary
> Theseus is an open source PyTorch library that provides differentiable nonlinear least squares as a layer, with sparse batched GPU solvers and implicit differentiation, making end-to-end structured learning in robotics and vision faster and more scalable than dense or Ceres-based baselines.

## Abstract

We present Theseus, an efficient application-agnostic open source library for differentiable nonlinear least squares (DNLS) optimization built on PyTorch, providing a common framework for end-to-end structured learning in robotics and vision. Existing DNLS implementations are application specific and do not always incorporate many ingredients important for efficiency. Theseus is application-agnostic, as we illustrate with several example applications that are built using the same underlying differentiable components, such as second-order optimizers, standard costs functions, and Lie groups. For efficiency, Theseus incorporates support for sparse solvers, automatic vectorization, batching, GPU acceleration, and gradient computation with implicit differentiation and direct loss minimization. We do extensive performance evaluation in a set of applications, demonstrating significant efficiency gains and better scalability when these features are incorporated. Project page: https://sites.google.com/view/theseus-ai (arXiv)

## 🧠 Key ideas (atomic)

- Theseus is an open source library for differentiable nonlinear least squares optimization built on PyTorch for structured learning in robotics and vision. (Pineda et al., 2022) `ev:asserted` p. 2 ^pineda2022theseus-001
- According to the authors, existing differentiable nonlinear least squares implementations are application specific, which has led to a fragmented literature. (Pineda et al., 2022) `ev:asserted` p. 2 ^pineda2022theseus-002
- The authors note that features affecting efficiency, such as sparse solvers, batching, and GPU support, are not always included in prior implementations. (Pineda et al., 2022) `ev:asserted` p. 2 ^pineda2022theseus-003
- Theseus provides Gauss-Newton, Levenberg–Marquardt with adaptive damping, and Dogleg as second-order nonlinear optimizers for the inner loop. (Pineda et al., 2022) `ev:reported` p. 5 ^pineda2022theseus-004
- Objectives can be built from learnable or hand-specified cost functions, either from library-provided costs or custom costs using PyTorch automatic differentiation. (Pineda et al., 2022) `ev:asserted` p. 2 ^pineda2022theseus-005
- The core API comprises Variable, CostFunction, CostWeight, Objective, Optimizer, and TheseusLayer, which interfaces the DNLS block with other torch modules. (Pineda et al., 2022) `ev:reported` p. 4 ^pineda2022theseus-006
- The library includes standard cost functions with analytical Jacobians, such as Gaussian measurements, reprojection error, relative pose measurement, motion models, and collision costs. (Pineda et al., 2022) `ev:reported` p. 5 ^pineda2022theseus-007
- Theseus computes common Lie group operators such as exponential map, logarithm map, inverse, and composition in closed form with analytical tangent-space derivatives. (Pineda et al., 2022) `ev:reported` p. 5 ^pineda2022theseus-008
- A projection operator maps gradients from PyTorch autodiff to the Lie group tangent space for computing Jacobians and updating variables. (Pineda et al., 2022) `ev:reported` p. 5 ^pineda2022theseus-009
- Example applications included with the library are pose graph optimization, tactile state estimation, bundle adjustment, motion planning, and homography estimation. (Pineda et al., 2022) `ev:reported` p. 2 ^pineda2022theseus-010
- In the pose graph optimization example, DNLS learns the radius of a Welsh robust cost function for outlier rejection on a synthetic dataset. (Pineda et al., 2022) `ev:reported` p. 5 ^pineda2022theseus-011
- Theseus natively supports solving a batch of DNLS problems in parallel, matching the batched training standard in PyTorch. (Pineda et al., 2022) `ev:reported` p. 6 ^pineda2022theseus-012
- Inspired by DeepLM, Theseus automatically detects and vectorizes operations of the same type, such as costs, Jacobian computations, and variable updates. (Pineda et al., 2022) `ev:reported` p. 6 ^pineda2022theseus-013
- On pose graph optimization, automatic vectorization increases memory use by up to ∼82% for the forward pass and ∼55% for backward. (Pineda et al., 2022) `ev:measured` p. 6 ^pineda2022theseus-014
- Theseus provides three sparse solvers: a CHOLMOD-based CPU solver, cudaLU based on cuSolverRF, and BaSpaCho, a novel batched sparse Cholesky solver. (Pineda et al., 2022) `ev:reported` p. 6 ^pineda2022theseus-015
- Since CHOLMOD lacks batching, Theseus has to loop over the batch and solve every problem independently. (Pineda et al., 2022) `ev:asserted` p. 6 ^pineda2022theseus-016
- cudaLU cannot share one symbolic decomposition across separate factors, so its number of contexts must be set by the unrolled iterations. (Pineda et al., 2022) `ev:asserted` p. 6 ^pineda2022theseus-017
- With cudaLU, the batch size must stay constant during outer loop optimization, since recreating contexts is expensive. (Pineda et al., 2022) `ev:asserted` p. 7 ^pineda2022theseus-018
- cudaLU relies on LU factorization, which the authors note is less efficient than Cholesky decomposition for symmetric matrices. (Pineda et al., 2022) `ev:asserted` p. 7 ^pineda2022theseus-019
- BaSpaCho implements the supernodal Cholesky algorithm, dispatching dense operations to BLAS on CPU or cuBLAS on GPU with added batching support. (Pineda et al., 2022) `ev:reported` p. 7 ^pineda2022theseus-020
- BaSpaCho complements the supernodal algorithm with sparse elimination, removing the need to handle the Schur complement trick externally. (Pineda et al., 2022) `ev:asserted` p. 7 ^pineda2022theseus-021
- Since the backward pass can cache factorizations from the forward pass, the linear-solver backward is significantly faster than the forward. (Pineda et al., 2022) `ev:measured` p. 7 ^pineda2022theseus-022
- Theseus includes four backward modes for adjoint derivatives: unrolling, truncated differentiation, implicit differentiation, and direct loss minimization. (Pineda et al., 2022) `ev:reported` p. 7 ^pineda2022theseus-023
- The authors apply implicit differentiation, previously used with first-order and convex optimization, to a new class of second-order NLS optimizers. (Pineda et al., 2022) `ev:asserted` p. 7 ^pineda2022theseus-024
- Proposition 1 shows the implicit derivative can be computed by differentiating a single Newton step at an optimal solution. (Pineda et al., 2022) `ev:computed` p. 7 ^pineda2022theseus-025
- The modified DLM formulation adds a small regularization term so the perturbed objective remains a sum of squares that Theseus can solve. (Pineda et al., 2022) `ev:asserted` p. 8 ^pineda2022theseus-026
- Profiling uses the synthetic Cube PGO dataset with 10 inner loop iterations, 20 outer loop epochs, and implicit differentiation. (Pineda et al., 2022) `ev:reported` p. 8 ^pineda2022theseus-027
- With a batch size of 128, the dense solver's largest solvable problem before running out of GPU memory has 256 poses. (Pineda et al., 2022) `ev:measured` p. 8 ^pineda2022theseus-028
- At batch size 128, the sparse solvers scale further than dense, with BaSpaCho reaching 2048 poses and cudaLU reaching 4096 poses. (Pineda et al., 2022) `ev:measured` p. 8 ^pineda2022theseus-029
- CHOLMOD was successfully tested up to 8192 poses with batch size 256, using 22GBs of GPU memory for residual and Jacobian computation. (Pineda et al., 2022) `ev:measured` p. 8 ^pineda2022theseus-030
- For batch size 128 and 64 poses, total times were 1.47s for dense, 1.32s for cudaLU, and 2.82s for CHOLMOD. (Pineda et al., 2022) `ev:measured` p. 8 ^pineda2022theseus-031
- For batch size 128 and 256 poses, dense took 20.81s versus 10.96s for CHOLMOD, 2.86s for cudaLU, and 2.25s for BaSpaCho. (Pineda et al., 2022) `ev:measured` p. 9 ^pineda2022theseus-032
- BaSpaCho outperforms the dense solver for any problem scale tested, being up to one order of magnitude faster. (Pineda et al., 2022) `ev:measured` p. 9 ^pineda2022theseus-033
- For batch size 256 and 2048 poses, total times were 170.28s for cudaLU, 239.07s for CHOLMOD, and 57.67s for BaSpaCho. (Pineda et al., 2022) `ev:measured` p. 9 ^pineda2022theseus-034
- Ceres is faster than all Theseus solvers at small scales, for instance 25x faster with 256 poses and batch size 16. (Pineda et al., 2022) `ev:measured` p. 9 ^pineda2022theseus-035
- With 2048 poses and batch size 256, BaSpaCho's forward pass is ∼23x faster than Ceres. (Pineda et al., 2022) `ev:measured` p. 9 ^pineda2022theseus-036
- CHOLMOD achieves a 6x speedup over Ceres at its largest setting of 4096 poses and batch size 256. (Pineda et al., 2022) `ev:measured` p. 9 ^pineda2022theseus-037
- When solving a batch of large problems, the forward pass of Theseus is up to 20x faster than Ceres. (Pineda et al., 2022) `ev:measured` p. 10 ^pineda2022theseus-038
- Theseus and Ceres attain the same objective values on all evaluated pose graph benchmark datasets using chordal initialization. (Pineda et al., 2022) `ev:measured` p. 13 ^pineda2022theseus-039
- The dense solver fails to solve any PGO problem with 4096 poses or more, even with batch size 1. (Pineda et al., 2022) `ev:measured` p. 17 ^pineda2022theseus-040
- At 512 poses and batch size 16, the largest problem dense can solve, BaSpaCho achieves a ∼9.1x speedup over dense. (Pineda et al., 2022) `ev:measured` p. 16 ^pineda2022theseus-041
- Backward modes were compared on tactile state estimation using Quadro GP100 GPUs, measuring validation loss after 100 epochs, run time, and peak memory. (Pineda et al., 2022) `ev:reported` p. 9 ^pineda2022theseus-042
- The tactile dataset holds 63 trajectories of length 25, with 56 used for training and 7 for testing. (Pineda et al., 2022) `ev:reported` p. 14 ^pineda2022theseus-043
- Unroll is the only backward mode whose backward pass time depends linearly on the number of inner loop iterations. (Pineda et al., 2022) `ev:measured` p. 9 ^pineda2022theseus-044
- Unroll's backward-pass memory footprint grows linearly with inner loop iterations, rising from ∼34MBs to ∼262MBs. (Pineda et al., 2022) `ev:measured` p. 10 ^pineda2022theseus-045
- Implicit and DLM give the best backward memory profiles in this example, at ∼28MBs and ∼29MBs respectively. (Pineda et al., 2022) `ev:measured` p. 10 ^pineda2022theseus-046
- The best validation loss after 100 epochs is obtained with Implicit, followed by the truncated differentiation variants. (Pineda et al., 2022) `ev:measured` p. 10 ^pineda2022theseus-047
- DLM does not improve much with more inner loop iterations, yet is the best method with only 2 inner loop iterations. (Pineda et al., 2022) `ev:measured` p. 10 ^pineda2022theseus-048
- The authors caution that relative training performance between backward modes is likely to be application dependent, unlike the timing and memory results. (Pineda et al., 2022) `ev:asserted` p. 10 ^pineda2022theseus-049
- The authors' experiments suggest implicit differentiation is a good default for differentiable optimization, considering its low time and memory footprint. (Pineda et al., 2022) `ev:asserted` p. 10 ^pineda2022theseus-050
- Despite higher test set performance, Implicit is more unstable during training, oscillating between low and high values. (Pineda et al., 2022) `ev:measured` p. 18 ^pineda2022theseus-051
- Implicit differentiation cannot be used when learning initial values for the optimization variables, unlike the other backward modes. (Pineda et al., 2022) `ev:asserted` p. 18 ^pineda2022theseus-052
- Implicit gradients might be inaccurate in problems where finding the optimal solution to the inner problem is not feasible. (Pineda et al., 2022) `ev:asserted` p. 18 ^pineda2022theseus-053
- Unroll and Trunc could potentially experience vanishing or exploding gradients when backpropagating through a large number of iterations. (Pineda et al., 2022) `ev:asserted` p. 18 ^pineda2022theseus-054
- DLM requires tuning its ε parameter, which the authors state can greatly affect its performance. (Pineda et al., 2022) `ev:asserted` p. 18 ^pineda2022theseus-055
- At batch size 128 in the homography example, vmap mode gives a 22x speedup over the next best autograd mode. (Pineda et al., 2022) `ev:measured` p. 12 ^pineda2022theseus-056
- The nonlinear solvers currently supported by Theseus apply constraints in a soft manner, using weighted costs. (Pineda et al., 2022) `ev:asserted` p. 10 ^pineda2022theseus-057
- The current implementation of Levenberg–Marquardt in Theseus does not support making the damping parameter learnable. (Pineda et al., 2022) `ev:asserted` p. 10 ^pineda2022theseus-058
- The authors explored only non-incremental settings, so frequently editing the objective in online learning may incur nontrivial unoptimized overhead. (Pineda et al., 2022) `ev:asserted` p. 10 ^pineda2022theseus-059

## 🎯 Contributions

## 📖 Glossary

- **DNLS** — Differentiable nonlinear least squares: an NLS solver whose solution is differentiated with respect to upstream parameters.
- **TheseusLayer** — Theseus module wrapping an objective and optimizer as a differentiable layer.
- **Implicit differentiation** — Computing solution gradients via the implicit function theorem at the optimum, without unrolling iterations.
- **Unrolling** — Backpropagating through every inner optimizer iteration; cost grows with iteration count.
- **Truncated differentiation** — Backpropagating through only the last few inner iterations, giving biased gradients.
- **Direct loss minimization (DLM)** — Finite-difference gradient estimate from a solution perturbed toward lower outer loss.
- **BaSpaCho** — Batched sparse supernodal Cholesky solver with GPU support, developed for Theseus.
- **Supernodal Cholesky** — Sparse factorization grouping columns with similar patterns to use dense BLAS kernels.
- **Pose graph optimization (PGO)** — Recovering poses from noisy relative pose measurements as nonlinear least squares.

## ❓ Open questions

- How can hard constraints (augmented Lagrangian, SQP) be made differentiable within the same library interface?
- How much overhead do incremental or online objective edits add, and can it be optimized?
- Does the ranking of backward modes by final task loss hold beyond tactile state estimation?
- How should implicit differentiation be stabilized, given its oscillating training loss in the tactile example?
- Can Levenberg–Marquardt damping be learned end-to-end, and does it help?

## 📝 Notes on reading

Read the arXiv v3 (18 Jan 2023), matching the packet identifier arXiv:2207.09442.

Figures 2–5 and 10–15 are plots whose values could only be read from axes; only numbers stated in the text were claimed. Fig. 2 shows vectorization speedups on PGO; Fig. 11–12 show solver times across sparsity levels (dense forward time almost constant across sparsity).

Table 1 (initial/final PGO objective values on Sphere, Torus, Cubicle, Rim, Grid, Garage) and Table 2 (backward mode limitations, checkmark cells lost in extraction) were not claimed cell by cell. Fig. 9 text is garbled by font encoding.

Other content described but not claimed to stay within volume: the LieTorch comparison and differentiable kinematics (p. 5), the motion planning, tactile and homography examples (pp. 5, 13–15), the stand-alone Ceres comparison setup (p. 9), vmap memory savings (p. 12), and the stated C++ porting and distributed-training limitations (p. 10).

Internal inconsistency: the Ceres speedup is stated as up to 20x (p. 2, p. 10) while Sec. 5.2 reports ∼23x for BaSpaCho at 2048 poses and batch 256 (p. 9). Implicit's peak memory is ∼28MBs in the backward pass (p. 10) and ∼22MBs in the forward pass (p. 18); these are different passes, not a contradiction.

The DLM ε-tuning claim refers to Eq. (16) in App. H.

## Suggested new concepts

- Differentiable nonlinear least squares — the core formulation shared by many robotics and vision learning pipelines.
- Implicit differentiation through optimizers — recurring backward mode trading accuracy assumptions for constant memory.
- Backward modes for bilevel optimization — unrolling, truncation, implicit and DLM compared on cost, bias and stability.
- Batched sparse linear solvers on GPU — enabling scalable second-order optimization inside deep learning.
- Differentiable Lie groups — tangent-space gradients for poses in learning systems.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — GN/LM diferenciables con grupos de Lie como capa de red (A.6, F.5).
