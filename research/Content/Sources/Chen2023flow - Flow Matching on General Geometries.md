---
aliases: []
type: "source"
title: "Flow Matching on General Geometries"
citekey: "Chen2023flow"
doi: "10.48550/arXiv.2302.03660"
arxiv: "2302.03660"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2302.03660"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Ricky T. Q. Chen", "Yaron Lipman"]
sha256: ["5860a6f32978550acdbca99d82a1e4af6020ae76220e62951d92f8b43ac880ab"]
pdf: "Content/Papers/Chen2023flow.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 53
---

📄 PDF: [[Chen2023flow.pdf]]

> [!abstract] One-sentence summary
> Chen and Lipman extend Flow Matching to Riemannian manifolds through premetric-defined conditional flows, making training simulation-free on simple geometries and tractable on meshes and manifolds with boundaries via spectral distances.

## Abstract

We propose Riemannian Flow Matching (RFM), a simple yet powerful framework for training continuous normalizing flows on manifolds. Existing methods for generative modeling on manifolds either require expensive simulation, are inherently unable to scale to high dimensions, or use approximations for limiting quantities that result in biased training objectives. Riemannian Flow Matching bypasses these limitations and offers several advantages over previous approaches: it is simulation-free on simple geometries, does not require divergence computation, and computes its target vector field in closed-form. The key ingredient behind RFM is the construction of a relatively simple premetric for defining target vector fields, which encompasses the existing Euclidean case. To extend to general geometries, we rely on the use of spectral decompositions to efficiently compute premetrics on the fly. Our method achieves state-of-the-art performance on many real-world non-Euclidean datasets, and we demonstrate tractable training on general geometries, including triangular meshes with highly non-trivial curvature and boundaries. (arXiv)

## 🧠 Key ideas (atomic)

- [[Riemannian flow matching|Riemannian Flow Matching]] learns continuous normalizing flows on general Riemannian manifolds by regressing an implicitly defined target vector field. (Chen & Lipman, 2023) `ev:asserted` p. 1 ^chen2023flow-001
- To address the intractability of the target field, [[Riemannian flow matching|RFM]] regresses onto conditional vector fields that push the base toward individual training examples. (Chen & Lipman, 2023) `ev:asserted` p. 1 ^chen2023flow-002
- The authors observe that the conditional vector field needed for training can be expressed explicitly in terms of a premetric on the manifold. (Chen & Lipman, 2023) `ev:asserted` p. 1 ^chen2023flow-003
- On simple geometries with closed-form geodesics, such as hyperspheres, hyperbolic space and tori, [[Riemannian flow matching|Riemannian Flow Matching]] remains completely simulation-free. (Chen & Lipman, 2023) `ev:asserted` p. 2 ^chen2023flow-004
- On general geometries the method requires forward simulation of a relatively simple ODE, without differentiating through the solver or estimating divergences. (Chen & Lipman, 2023) `ev:asserted` p. 2 ^chen2023flow-005
- Table 1 marks [[Riemannian flow matching|Riemannian Flow Matching]] as the only compared method combining simulation-free training, a closed-form target and no divergence. (Chen & Lipman, 2023) `ev:asserted` p. 2 ^chen2023flow-006
- The authors claim the first successful training of continuous-time deep generative models on triangular meshes and maze-shaped manifolds with boundaries. (Chen & Lipman, 2023) `ev:asserted` p. 2 ^chen2023flow-007
- The Riemannian Conditional Flow Matching objective is shown to differ from the marginal Flow Matching objective by a constant independent of parameters. (Chen & Lipman, 2023) `ev:computed` p. 15 ^chen2023flow-008
- A premetric is defined as a function that is non-negative, zero only at identical points, and has nonzero gradient elsewhere. (Chen & Lipman, 2023) `ev:asserted` p. 4 ^chen2023flow-009
- Theorem 3.1 proves that the flow defined by the premetric-based conditional vector field decreases the premetric exactly as the scheduler prescribes. (Chen & Lipman, 2023) `ev:computed` p. 5 ^chen2023flow-010
- Among all conditional vector fields satisfying the scheduled premetric decrease, the proposed field is the minimal norm solution. (Chen & Lipman, 2023) `ev:computed` p. 5 ^chen2023flow-011
- The paper uses a scheduler equal to one minus time, giving a conditional flow that linearly decreases the premetric toward the target. (Chen & Lipman, 2023) `ev:reported` p. 5 ^chen2023flow-012
- For general manifolds and premetrics, RCFM training needs simulation to obtain intermediate points, though it does not differentiate through them. (Chen & Lipman, 2023) `ev:asserted` p. 5 ^chen2023flow-013
- Proposition 3.2 shows that with geodesic distance as premetric and the linear scheduler, the conditional flow is a constant speed geodesic. (Chen & Lipman, 2023) `ev:computed` p. 5 ^chen2023flow-014
- On simple manifolds the intermediate point is computed in closed form using the [[Exponential map|exponential and logarithm maps]], giving a highly scalable objective. (Chen & Lipman, 2023) `ev:asserted` p. 5 ^chen2023flow-015
- In Euclidean space with the standard norm, the RCFM objective coincides with the Euclidean Flow Matching of prior works. (Chen & Lipman, 2023) `ev:computed` p. 5 ^chen2023flow-016
- For general geometries the authors propose spectral distances as premetrics, computable quickly for any pair of points after a one-time upfront cost. (Chen & Lipman, 2023) `ev:asserted` p. 5 ^chen2023flow-017
- Spectral distances offer robustness to topological noise, smoothness and global geometry awareness compared with geodesic distance, per cited work. (Chen & Lipman, 2023) `ev:cited` p. 6 ^chen2023flow-018
- Spectral distances are weighted sums of squared eigenfunction differences of the Laplace-Beltrami operator, with a monotonically decreasing weighting function. (Chen & Lipman, 2023) `ev:reported` p. 6 ^chen2023flow-019
- The infinite spectral series is truncated to the smallest k eigenvalues, whose eigenfunctions are solved once as preprocessing before training. (Chen & Lipman, 2023) `ev:reported` p. 6 ^chen2023flow-020
- The authors state that a finite-k spectral approximation suffices to satisfy the premetric properties, leading to no bias in training. (Chen & Lipman, 2023) `ev:asserted` p. 6 ^chen2023flow-021
- Solving eigenfunctions with Neumann boundary conditions ensures the conditional vector field does not leave the interior of a manifold with boundary. (Chen & Lipman, 2023) `ev:computed` p. 6 ^chen2023flow-022
- The authors find that heat-kernel approximations of the conditional score can potentially be extremely biased even with hundreds of eigenfunctions. (Chen & Lipman, 2023) `ev:computed` p. 7 ^chen2023flow-023
- On the volcano dataset, [[Riemannian flow matching|Riemannian Flow Matching]] with geodesic reached test NLL -7.93±1.67, versus -6.61±0.96 for the [[Riemannian diffusion models|Riemannian Diffusion Model]]. (Chen & Lipman, 2023) `ev:measured` p. 7 ^chen2023flow-024
- On the fire dataset, Riemannian Flow Matching reached test NLL -1.86±0.11 compared with -1.40±0.02 for CNF Matching. (Chen & Lipman, 2023) `ev:measured` p. 7 ^chen2023flow-025
- On earthquake data, [[Riemannian flow matching|Riemannian Flow Matching]] scored -0.28±0.08 test NLL, behind the Riemannian Diffusion Model at -0.40±0.05. (Chen & Lipman, 2023) `ev:measured` p. 7 ^chen2023flow-026
- The authors report sizable improvements over prior works on volcano and fire, datasets with highly concentrated regions requiring high fidelity. (Chen & Lipman, 2023) `ev:measured` p. 8 ^chen2023flow-027
- On the 7D RNA torus dataset, [[Riemannian flow matching|Riemannian Flow Matching]] reached test NLL -5.20±0.067, versus -3.70±0.592 for the [[Riemannian diffusion models|Riemannian Diffusion Model]]. (Chen & Lipman, 2023) `ev:measured` p. 8 ^chen2023flow-028
- On the Proline dataset, Riemannian Flow Matching scored 0.15±0.027 test NLL, behind the [[Riemannian diffusion models|Riemannian Diffusion Model]] at 0.12±0.011. (Chen & Lipman, 2023) `ev:measured` p. 8 ^chen2023flow-029
- Compared with Huang et al., the authors see a significant gain particularly on the 7D torus, which they attribute to dataset complexity. (Chen & Lipman, 2023) `ev:measured` p. 8 ^chen2023flow-030
- On high-dimensional tori, [[Riemannian flow matching|Riemannian Flow Matching]] shows no significant drop in log-likelihood per dimension as dimension increases. (Chen & Lipman, 2023) `ev:measured` p. 9 ^chen2023flow-031
- Computing spectral distances costs O(k) after preprocessing, where k is much smaller than the number of mesh edges. (Chen & Lipman, 2023) `ev:asserted` p. 9 ^chen2023flow-032
- Mesh experiments use the Standard Bunny and Spot the Cow, with targets built by thresholding the k-th eigenfunction. (Chen & Lipman, 2023) `ev:reported` p. 9 ^chen2023flow-033
- On Spot the Cow with k=100, the biharmonic distance gave test NLL 1.29±0.05, compared with 1.08±0.05 for the diffusion distance. (Chen & Lipman, 2023) `ev:measured` p. 9 ^chen2023flow-034
- On the Stanford Bunny with k=10, the biharmonic distance gave test NLL 1.06±0.05, compared with 1.16±0.02 for the diffusion distance. (Chen & Lipman, 2023) `ev:measured` p. 9 ^chen2023flow-035
- The authors found the biharmonic distance straightforward to use out of the box, with better smoothness properties. (Chen & Lipman, 2023) `ev:asserted` p. 9 ^chen2023flow-036
- On randomly generated maze meshes, the authors use the biharmonic distance computed with k=30 eigenfunctions. (Chen & Lipman, 2023) `ev:reported` p. 9 ^chen2023flow-037
- Sample trajectories show the learned vector field avoiding the maze boundaries on its way to different target modes. (Chen & Lipman, 2023) `ev:measured` p. 9 ^chen2023flow-038
- The authors conclude the method is completely simulation-free with zero approximation errors on simple geometries with closed-form geodesics. (Chen & Lipman, 2023) `ev:asserted` p. 9 ^chen2023flow-039
- The authors state their method still requires simulating intermediate points on general manifolds, a sequential process that can be time consuming. (Chen & Lipman, 2023) `ev:asserted` p. 18 ^chen2023flow-040
- Spectral distances need eigenfunction solvers that may be computationally expensive on complex manifolds, a stated limitation. (Chen & Lipman, 2023) `ev:asserted` p. 18 ^chen2023flow-041
- The biharmonic spectral distance on the sphere satisfies the premetric properties even with only k = 3 eigenfunctions. (Chen & Lipman, 2023) `ev:computed` p. 20 ^chen2023flow-042
- At small times near the data, the approximated heat-kernel conditional score may not have even its first significant digit correct. (Chen & Lipman, 2023) `ev:computed` p. 20 ^chen2023flow-043
- Because prior works' exact splits were unavailable, the authors used their own random 80% train, 10% validation, 10% test splits. (Chen & Lipman, 2023) `ev:reported` p. 20 ^chen2023flow-044
- Training used Adam with learning rate 1e-4 and weight exponential moving averaging with decay 0.999 across all experiments. (Chen & Lipman, 2023) `ev:reported` p. 20 ^chen2023flow-045
- During training on mesh geometries, intermediate points were obtained with 300 Euler steps followed by projection after every step. (Chen & Lipman, 2023) `ev:reported` p. 22 ^chen2023flow-046
- On a flat torus, simulation-free training ran at 104.04 iterations per second versus 6.36 with 200-step ODE/SDE simulation. (Chen & Lipman, 2023) `ev:measured` p. 23 ^chen2023flow-047
- Simulated training on the bunny mesh ran at 0.422 iterations per second, which the authors attribute partly to naive per-step projection. (Chen & Lipman, 2023) `ev:measured` p. 23 ^chen2023flow-048
- The authors report a speedup of roughly 17x for simulation-free training over iterative ODE/SDE solving, including the full training loop. (Chen & Lipman, 2023) `ev:measured` p. 23 ^chen2023flow-049
- On the 2-D Poincaré disk, the learned CNF transports samples along geodesic paths, recovering a near-optimal transport map. (Chen & Lipman, 2023) `ev:measured` p. 23 ^chen2023flow-050
- On the 1770D BCI-IV-1 SPD data, models trained with the Euclidean norm produced no valid SPD samples. (Chen & Lipman, 2023) `ev:measured` p. 24 ^chen2023flow-051
- With Riemannian geodesic and Riemannian norm, the 1770D BCI-IV-1 model reached test NLL -1209.88±53.55, with all simulated samples valid. (Chen & Lipman, 2023) `ev:measured` p. 24 ^chen2023flow-052
- The authors find that especially for larger SPD matrices, the Riemannian norm is important to keep simulated samples on the manifold. (Chen & Lipman, 2023) `ev:measured` p. 24 ^chen2023flow-053

## 🎯 Contributions

## 📖 Glossary

- **Premetric** — Non-negative function, zero only on identical points, with nonzero gradient elsewhere.
- **Continuous normalizing flow (CNF)** — Generative model transporting a base density through an ODE-defined time-dependent vector field.
- **Conditional Flow Matching** — Regression onto per-sample conditional vector fields, equivalent in gradient to marginal Flow Matching.
- **Scheduler κ(t)** — Monotonically decreasing function from one to zero setting how fast the premetric shrinks.
- **Spectral distance** — Distance built from weighted Laplace-Beltrami eigenfunction differences, e.g. biharmonic or diffusion distance.
- **Biharmonic distance** — Spectral distance weighting eigenfunctions by inverse squared eigenvalues; smooth and tuning-free.
- **Simple geometry** — Manifold with closed-form geodesics, exponential and logarithm maps, e.g. sphere or torus.
- **Neumann boundary condition** — Eigenfunctions with vanishing normal derivative at the boundary, keeping flows inside the manifold.

## ❓ Open questions

- Can intermediate points on general manifolds be constructed in parallel or simulation-free rather than by sequential ODE solving?
- How many eigenfunctions suffice to satisfy the premetric properties on a given manifold beyond local neighborhoods?
- Would approximate eigenfunction solvers such as neural eigenfunctions keep training unbiased on large, complex meshes?
- How should the scheduler κ(t) be chosen beyond the linear choice, and does it affect sample quality?
- Why does RFM trail baselines on some datasets such as earthquake, flood and Proline?

## 📝 Notes on reading

- Version read: arXiv 2302.03660v3 (26 Feb 2024), labelled as the ICLR 2024 conference paper; the packet identifier is the arXiv DOI.
- Figure 5 (high-dimensional tori log-likelihood per dimension vs N) is only a plot; no per-dimension values were claimed.
- Figure 8's caption in the extracted text repeats the protein caption although the panels are labelled Volcano, Earthquake, Flood, Fire (likely a caption error in the paper).
- Proposition 3.2 in the main text says constant speed geodesic; the appendix restatement on p. 16 drops "constant speed".
- Algorithm 1 (p. 4) writes xt = exp_x1(κ(t) log_x1(x0)) while Algorithm 3 (p. 17) writes exp_x0(κ(t) log_x0(x1)); the two are inconsistent in notation.
- Tables 2 and 3: RFM is not best on every dataset (earthquake, flood, Proline); the abstract's state-of-the-art wording is broader than the tables.
- Table 4 is mixed: the biharmonic distance is better on some Bunny settings and worse on all Spot settings by NLL.
- Table 5 formulas and Table 6 layout were partly garbled in extraction; only clearly readable cells were claimed.

## Suggested new concepts

- Riemannian Flow Matching — core method extending Flow Matching to manifolds; likely referenced by later manifold generative models.
- Premetric — the minimal distance-like structure that makes conditional flows well defined; reusable design idea.
- Spectral distances on meshes — biharmonic and diffusion distances as cheap geodesic substitutes for learning on general geometries.
- Simulation-free training — recurring axis for comparing continuous-time generative models on manifolds.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Riemannian Flow Matching (C.5, F.6).

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
