---
aliases: []
type: "source"
title: "Accelerating Motion Planning via Optimal Transport"
citekey: "Le2023accelerating"
doi: "10.48550/arXiv.2309.15970"
arxiv: "2309.15970"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2309.15970"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["An T. Le", "Georgia Chalvatzaki", "Armin Biess", "Jan Peters"]
sha256: ["2c2e250afbbd35519c83342a2ff16b67637233df74a1671442d97a0505bd0132"]
pdf: "Content/Papers/Le2023accelerating.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 66
---

📄 PDF: [[Le2023accelerating.pdf]]

> [!abstract] One-sentence summary
> MPOT replaces gradient-based trajectory optimization with the Sinkhorn Step, a gradient-free, GPU-batched optimal-transport update over polytope search directions, and plans batches of smooth trajectories several times faster than CHOMP, GPMP2, STOMP, SGPMP and RRT* on point-mass, Panda and TIAGo++ benchmarks.

## Abstract

Motion planning is still an open problem for many disciplines, e.g., robotics, autonomous driving, due to their need for high computational resources that hinder real-time, efficient decision-making. A class of methods striving to provide smooth solutions is gradient-based trajectory optimization. However, those methods usually suffer from bad local minima, while for many settings, they may be inapplicable due to the absence of easy-to-access gradients of the optimization objectives. In response to these issues, we introduce Motion Planning via Optimal Transport (MPOT) -- a \textit{gradient-free} method that optimizes a batch of smooth trajectories over highly nonlinear costs, even for high-dimensional tasks, while imposing smoothness through a Gaussian Process dynamics prior via the planning-as-inference perspective. To facilitate batch trajectory optimization, we introduce an original zero-order and highly-parallelizable update rule: the Sinkhorn Step, which uses the regular polytope family for its search directions. Each regular polytope, centered on trajectory waypoints, serves as a local cost-probing neighborhood, acting as a \textit{trust region} where the Sinkhorn Step "transports" local waypoints toward low-cost regions. We theoretically show that Sinkhorn Step guides the optimizing parameters toward local minima regions of non-convex objective functions. We then show the efficiency of MPOT in a range of problems from low-dimensional point-mass navigation to high-dimensional whole-body robot motion planning, evincing its superiority compared to popular motion planners, paving the way for new applications of optimal transport in motion planning. (arXiv)

## 🧠 Key ideas (atomic)

- Sampling-based motion planners need large computational budgets, which increase with problem complexity such as highly redundant robots and narrow passages. (Le et al., 2023) `ev:cited` p. 1 ^le2023accelerating-001
- Trajectory optimization can get trapped in bad local minima due to the non-convexity of complex objectives, according to the authors. (Le et al., 2023) `ev:asserted` p. 1 ^le2023accelerating-002
- MPOT is a gradient-free trajectory optimization method that optimizes a batch of smooth trajectories using a novel update rule called the Sinkhorn Step. (Le et al., 2023) `ev:reported` p. 2 ^le2023accelerating-003
- MPOT optimizes trajectories by solving a sequence of entropic-regularized optimal transport problems, each solved with the Sinkhorn-Knopp algorithm. (Le et al., 2023) `ev:reported` p. 2 ^le2023accelerating-004
- MPOT probes a structured local neighborhood around each trajectory waypoint, which effectively acts as a trust region for its updates. (Le et al., 2023) `ev:asserted` p. 2 ^le2023accelerating-005
- MPOT imposes smoothness on its trajectories through a Gaussian Process dynamics prior, following the planning-as-inference perspective. (Le et al., 2023) `ev:reported` p. 2 ^le2023accelerating-006
- MPOT does not require computing gradients from cost functions that propagate over long kinematics chains, the authors state. (Le et al., 2023) `ev:asserted` p. 2 ^le2023accelerating-007
- In a multimodal planar navigation example with three goals and five initial trajectories per goal, the total planning time was 0.12s. (Le et al., 2023) `ev:measured` p. 2 ^le2023accelerating-008
- MPOT treats every waypoint across trajectories equally, updating waypoints from multiple trajectories over multiple goals by solving a single OT instance. (Le et al., 2023) `ev:asserted` p. 2 ^le2023accelerating-009
- Cuturi proposed regularizing the optimal transport objective with an entropy term to address its poor scaling with high dimensions. (Le et al., 2023) `ev:cited` p. 3 ^le2023accelerating-010
- Mukadam et al. generalize the CHOMP smoothness cost by incorporating a Gaussian Process prior as a cost via planning-as-inference. (Le et al., 2023) `ev:cited` p. 3 ^le2023accelerating-011
- The Sinkhorn Step draws inspiration from the free-support barycenter problem, in which the mean support of empirical measures is optimized. (Le et al., 2023) `ev:reported` p. 3 ^le2023accelerating-012
- The Sinkhorn Step obtains the weighting distribution over its search directions as an entropic-regularized optimal transport plan. (Le et al., 2023) `ev:reported` p. 3 ^le2023accelerating-013
- The paper assumes cheap batch-wise function evaluation, with function derivatives being either expensive or impossible to compute. (Le et al., 2023) `ev:reported` p. 4 ^le2023accelerating-014
- The search directions come from the vertices of a regular polytope, namely a simplex, orthoplex or hypercube, inscribing the unit hypersphere. (Le et al., 2023) `ev:reported` p. 4 ^le2023accelerating-015
- The authors show that the search-direction set of every polytope in this regular family forms a positive spanning set. (Le et al., 2023) `ev:computed` p. 4 ^le2023accelerating-016
- The Sinkhorn Step update is a barycentric projection that moves optimizing points toward polytope vertices with weights from the OT plan. (Le et al., 2023) `ev:reported` p. 4 ^le2023accelerating-017
- With the optimal stepsize, the complexity bounds for d-simplex, d-orthoplex and d-cube are O(d2/ϵ2), O(d/ϵ2), and O(1/ϵ2), respectively. (Le et al., 2023) `ev:computed` p. 5 ^le2023accelerating-018
- The d-cube case shows the same complexity bound O(1/ϵ2) as the known gradient descent bound on L-smooth functions. (Le et al., 2023) `ev:computed` p. 5 ^le2023accelerating-019
- Within directional-direct search, the d-cube gives a new best-known complexity bound O(1/ϵ2), which is independent of dimension d. (Le et al., 2023) `ev:computed` p. 18 ^le2023accelerating-020
- The authors note that solving a batch update with the d-cube at each iteration is expensive in practice. (Le et al., 2023) `ev:asserted` p. 18 ^le2023accelerating-021
- The authors describe their theoretical analysis as preliminary, as many theoretical properties of Sinkhorn Step in practical settings remain unexplored. (Le et al., 2023) `ev:asserted` p. 5 ^le2023accelerating-022
- Motion planning is formulated as minimizing a KL divergence between a waypoint empirical distribution and a Gaussian Process target posterior. (Le et al., 2023) `ev:reported` p. 6 ^le2023accelerating-023
- The KL objective is not equivalent to the analysed batch optimization problem due to its second coupling term, the authors note. (Le et al., 2023) `ev:asserted` p. 6 ^le2023accelerating-024
- Unlike moment-projection methods that rely on importance sampling, MPOT optimizes the trajectory parameters directly, enforcing model constraints in the cost. (Le et al., 2023) `ev:asserted` p. 6 ^le2023accelerating-025
- For denser function evaluations, probe points are placed equidistantly along each search direction up to a probe radius. (Le et al., 2023) `ev:reported` p. 6 ^le2023accelerating-026
- MPOT applies a random d-dimensional rotation to the polytopes, sampled in batch per waypoint, to promote local exploration. (Le et al., 2023) `ev:reported` p. 6 ^le2023accelerating-027
- The OT problem is solved with a log-domain stabilized Sinkhorn algorithm using a moderately small λ = 0.01. (Le et al., 2023) `ev:reported` p. 7 ^le2023accelerating-028
- The Sinkhorn Step defines an explicit trust region that bounds each update inside the polytope convex hull. (Le et al., 2023) `ev:asserted` p. 7 ^le2023accelerating-029
- Assumption 2 is usually violated in MPOT with many more waypoints than search directions, yet MPOT still works well, the authors state. (Le et al., 2023) `ev:asserted` p. 7 ^le2023accelerating-030
- Initial trajectories are sampled from a Gaussian Process prior with a constant-velocity straight-line mean and a large covariance. (Le et al., 2023) `ev:reported` p. 7 ^le2023accelerating-031
- The point-mass benchmark comprises 1000 planning tasks, each planned with 100 parallel trajectories of horizon 64. (Le et al., 2023) `ev:reported` p. 8 ^le2023accelerating-032
- The Panda benchmark comprises 500 planning tasks among 15 obstacle-spheres of radius 10cm, each planned with 10 parallel trajectories. (Le et al., 2023) `ev:reported` p. 8 ^le2023accelerating-033
- The TIAGo++ fetch-and-place task uses 20 randomly spawned seeds, with each plan containing 128 timesteps and one trajectory per planner. (Le et al., 2023) `ev:reported` p. 8 ^le2023accelerating-034
- The state dimension is d = 4 for point-mass, d = 14 for Panda, and d = 36 for mobile manipulation. (Le et al., 2023) `ev:reported` p. 8 ^le2023accelerating-035
- MPOT uses a 4-cube polytope for the point-mass case and orthoplex polytopes for the Panda and TIAGo++ cases. (Le et al., 2023) `ev:reported` p. 8 ^le2023accelerating-036
- Baselines are CHOMP, GPMP2, RRT*, I-RRT*, STOMP and SGPMP, implemented in PyTorch except RRT* and I-RRT*, which run on CPU. (Le et al., 2023) `ev:reported` p. 8 ^le2023accelerating-037
- In the point-mass benchmark, MPOT's planning time was 0.4 ± 0.0 s, against 43.2 ± 15.2 s for RRT*. (Le et al., 2023) `ev:measured` p. 9 ^le2023accelerating-038
- In the point-mass benchmark, CHOMP planned in 0.5 ± 0.1 s but reached a success rate of 70.9 ± 16.7 percent. (Le et al., 2023) `ev:measured` p. 9 ^le2023accelerating-039
- MPOT reached a point-mass success rate of 99.2 ± 3.1 percent, with 73.6 ± 26.7 percent of parallel trajectories successful. (Le et al., 2023) `ev:measured` p. 9 ^le2023accelerating-040
- In the Panda benchmark, MPOT planned in 0.8 ± 0.1 s, against 3.1 ± 0.3 s for CHOMP. (Le et al., 2023) `ev:measured` p. 9 ^le2023accelerating-041
- In the Panda benchmark, MPOT reached 71.6 ± 23.2 percent success, above SGPMP at 67.8 ± 23.5 percent. (Le et al., 2023) `ev:measured` p. 9 ^le2023accelerating-042
- In the Panda benchmark, MPOT's parallelization quality was 60.2 ± 44.4 percent, against 58.1 ± 45.8 percent for SGPMP. (Le et al., 2023) `ev:measured` p. 9 ^le2023accelerating-043
- RRT* and I-RRT* reached perfect success on both benchmarks, but their planning time was dramatically high, the authors report. (Le et al., 2023) `ev:measured` p. 9 ^le2023accelerating-044
- The authors attribute MPOT's good performance in narrow passages to updating waypoints across all trajectories independently. (Le et al., 2023) `ev:asserted` p. 9 ^le2023accelerating-045
- The parallelization setting requires larger step sizes for gradient-based CHOMP, which incurs its inherent instability, the authors argue. (Le et al., 2023) `ev:asserted` p. 9 ^le2023accelerating-046
- As waypoints approach local minima, the OT cost matrix becomes more uniform and can be solved with one or two Sinkhorn iterations. (Le et al., 2023) `ev:measured` p. 9 ^le2023accelerating-047
- In the Panda benchmark, cost converged even without step radius annealing, though more slowly than with annealing ϵ = 0.035. (Le et al., 2023) `ev:measured` p. 9 ^le2023accelerating-048
- In mobile fetch-and-place, MPOT found its first successful solution in 1.49 ± 0.02 s, against 16.74 ± 0.21 s for CHOMP. (Le et al., 2023) `ev:measured` p. 10 ^le2023accelerating-049
- In mobile fetch-and-place, MPOT reached a 55 percent success rate, compared with 40 percent for CHOMP and GPMP2. (Le et al., 2023) `ev:measured` p. 10 ^le2023accelerating-050
- In the mobile manipulation task, RRT* and I-RRT* recovered no solution within a time budget of 1000 seconds. (Le et al., 2023) `ev:measured` p. 10 ^le2023accelerating-051
- In mobile manipulation, MPOT had worse smoothness than the baselines, at 0.022 ± 0.003 against 0.010 ± 0.001 for SGPMP. (Le et al., 2023) `ev:measured` p. 10 ^le2023accelerating-052
- The authors relate this worse smoothness to the sparse 36-orthoplex search directions, which make success rate and smoothness hard to balance. (Le et al., 2023) `ev:asserted` p. 10 ^le2023accelerating-053
- In rare cases, the Sinkhorn scaling factors still diverge despite log-domain stabilization, making MPOT terminate prematurely. (Le et al., 2023) `ev:reported` p. 10 ^le2023accelerating-054
- The authors state that their experiments do not imply that MPOT should replace prior motion planning methods. (Le et al., 2023) `ev:asserted` p. 10 ^le2023accelerating-055
- The authors suggest learned motion priors could complement MPOT with better initializations than the random GP-prior trajectories used now. (Le et al., 2023) `ev:asserted` p. 10 ^le2023accelerating-056
- All experiments were executed on a single RTX3080Ti GPU and a single AMD Ryzen 5900X CPU. (Le et al., 2023) `ev:reported` p. 25 ^le2023accelerating-057
- MPOT normalizes the cost matrix to the range [0, 1], as it is cost-sensitive due to exponential terms inside the Sinkhorn algorithm. (Le et al., 2023) `ev:reported` p. 25 ^le2023accelerating-058
- Gradient-free planners including MPOT used a binary occupancy map for obstacle costs, whereas gradient-based planners used signed distance fields. (Le et al., 2023) `ev:reported` p. 27 ^le2023accelerating-059
- Removing random polytope rotation produced a significant performance gap in the point-mass ablation, which the authors attribute to approximation bias. (Le et al., 2023) `ev:measured` p. 27 ^le2023accelerating-060
- Without annealing, MPOT converged more slowly but eventually discovered more successful local minima, nearly 80% of parallel plans. (Le et al., 2023) `ev:measured` p. 28 ^le2023accelerating-061
- Across the tested horizons and numbers of parallel trajectories, MPOT planning time remained under a minute on a single GPU. (Le et al., 2023) `ev:measured` p. 29 ^le2023accelerating-062
- On Panda, the simplex variant planned in 0.5 ± 0.0 s but reached a lower success rate of 65.8 ± 24.5 percent. (Le et al., 2023) `ev:measured` p. 29 ^le2023accelerating-063
- Using random sphere directions instead of a polytope gave comparable success but a slower planning time of 2.5 ± 0.0 s on Panda. (Le et al., 2023) `ev:measured` p. 29 ^le2023accelerating-064
- On the 10D Styblinski-Tang function, larger λ gave higher cosine similarity between Sinkhorn Step directions and true negative gradients. (Le et al., 2023) `ev:measured` p. 29 ^le2023accelerating-065
- The authors caution that the smooth-function gradient ablation may not apply to motion planning, whose costs may have ill-formed landscapes. (Le et al., 2023) `ev:asserted` p. 29 ^le2023accelerating-066

## 🎯 Contributions

## 📖 Glossary

- **Sinkhorn Step** — zero-order batch update moving points toward polytope vertices weighted by an entropic OT plan.
- **Entropic-regularized optimal transport** — optimal transport objective with an entropy penalty, solvable quickly by Sinkhorn iterations.
- **Sinkhorn-Knopp algorithm** — iterative row and column scaling that computes an entropic optimal transport plan.
- **Regular polytope** — polytope with congruent facets; here simplex, orthoplex or hypercube inscribing a unit sphere.
- **Positive spanning set** — direction set whose nonnegative combinations reach every point of the space.
- **Planning as inference** — casting trajectory optimization as probabilistic inference over a posterior of trajectories.
- **Gaussian Process trajectory prior** — time-correlated Gaussian over trajectories, here constant-velocity, encoding smoothness and dynamics.
- **Barycentric projection** — mapping each source point to the plan-weighted average of its transported targets.
- **Directional-direct search** — derivative-free optimization evaluating the objective along a fixed set of search directions.
- **Parallelization quality (GOOD)** — percentage of parallel trajectories in a task that are successful.

## ❓ Open questions

- Does the convergence guarantee extend to the coupled KL objective with the GP transition term actually optimized by MPOT?
- How does Sinkhorn Step behave with arbitrary entropic regularization λ > 0, beyond the λ → 0 analysis?
- Can other uniform or vertex-transitive polytope families improve the balance between search-direction density and cost-matrix size in very high dimensions?
- Can learned motion priors (e.g., diffusion models) replace random GP initialization to raise success rates?
- How can smoothness be kept competitive in 36-dimensional whole-body planning, where MPOT was less smooth than baselines?
- Would a conditional Sinkhorn Step with non-uniform histograms or adaptive stepsizes help?
- Can the numerical instabilities of large entropic OT cost matrices be removed rather than mitigated?

## 📝 Notes on reading

- Version read: arXiv v2 (28 Oct 2023), the NeurIPS 2023 camera-ready; the packet identifier is the arXiv DOI.
- Superscripts were lost in extraction: the d-cube vertex count appears as 2d (meaning 2 to the power d), the Sinkhorn complexity as ˜O(n2/ϵ3), and the cube case in Fig. 10 as 210 vertices; these were not claimed as printed numbers except for the O(...) bounds copied verbatim.
- The paper writes othorplex in several places (typo for orthoplex).
- Figures 3, 7 and 10 are plots only described in captions; Fig. 8 (planning time heatmaps over horizons and number of trajectories) is extracted as an unlabelled number grid, so no per-cell values were claimed.
- Table 1 SUC and GOOD are in percent; values were copied with percent written as a word.
- Appendix J.1 says MPOT-NoAnnealing reaches nearly 80% successful plans, compared against MPOT with annealing (cf. Table 1, where point-mass GOOD is 73.6 ± 26.7); the comparison is only shown in Fig. 7.
- In the mobile manipulation table, MPOT reaches 55 percent success, so nearly half of the TIAGo++ tasks still fail for all planners.
- The theory (Theorem 1) assumes uniform histograms with n = m and λ → 0, whereas the experiments use λ = 0.01 and many more waypoints than vertices.

## Suggested new concepts

- Sinkhorn Step — a reusable gradient-free batch optimizer that could apply beyond motion planning (sampling, variational inference).
- Entropic optimal transport — core machinery behind this and other OT-based robotics methods.
- Gaussian Process motion planning prior — shared by GPMP2, SGPMP and MPOT; worth a concept note on the constant-velocity GP prior.
- Batch (vectorized) trajectory optimization — GPU-parallel planning of many trajectories, relevant for dataset collection for learned planners.
- Trust-region trajectory optimization — explicit vs implicit trust regions in CHOMP, GPMP and MPOT.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H3.** Sinkhorn Step: optimización de orden cero por lotes de trayectorias suaves en alta dimensión, alternativa paralela a STOMP.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
