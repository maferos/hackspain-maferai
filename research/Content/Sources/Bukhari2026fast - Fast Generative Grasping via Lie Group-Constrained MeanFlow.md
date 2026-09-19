---
aliases: []
type: "source"
title: "Fast Generative Grasping via Lie Group-Constrained MeanFlow"
citekey: "Bukhari2026fast"
doi: "10.48550/arXiv.2608.26076"
arxiv: "2608.26076"
year: 2026
publication_type: "preprint"
url: "https://arxiv.org/abs/2608.26076"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["S. Talha Bukhari", "Yi Wei", "Ruiqi Ni", "Zachary Kingston", "Aniket Bera"]
sha256: ["1e264d1b846b11b8a9c36c19aa34f870f9dd1ffc928431301acb038a021b3fdd"]
pdf: "Content/Papers/Bukhari2026fast.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Bukhari2026fast.pdf]]

> [!abstract] One-sentence summary
> GraspMF trains MeanFlow on SO(3)×R3 with an algebraic semigroup consistency loss plus a flow-matching anchor, generating 6-DoF grasps in one to five network evaluations with ACRONYM success rates at or above diffusion and flow baselines at millisecond latency.

## Abstract

Grasp synthesis is a core task in robotic manipulation, for which the solution typically forms a multimodal distribution rather than a point estimate. Generative robotic grasping aims to learn this distribution with deep generative models such as diffusion and flow-based approaches. The iterative nature of such generative models makes them flexible and generalizable; however, multi-step sampling impedes the time-critical operation required in robotics. We devise an approach to fast generative grasping based on MeanFlow on the product Lie group $\mathcal{G} = \mathrm{SO}(3) \times \mathbb{R}^3$. The training objective couples a purely algebraic semigroup consistency condition with Riemannian Conditional Flow Matching on $\mathcal{G}$ that anchors the average velocity to the data distribution. The resulting Lie Group-constrained MeanFlow formulation samples reliable grasps in $\leq 5$ network evaluations, matching the grasp generation performance of state-of-the-art diffusion and flow-based models on the ACRONYM dataset at millisecond-scale inference latency (up to $39\times$ speed-up). We further demonstrate that the approach directly translates to real-world robotic grasping without additional training or domain adaptation, exhibiting robust grasp synthesis under observation noise. (arXiv)

## 🧠 Key ideas (atomic)

- For a given object, the set of stable grasps forms a multimodal distribution in SE(3), motivating learned grasp distributions over point estimation. (Bukhari et al., 2026) `ev:cited` p. 1 ^bukhari2026fast-001
- The authors state that diffusion and flow inference requires tens to hundreds of integration steps, precluding the sampling rates of reactive closed-loop execution. (Bukhari et al., 2026) `ev:asserted` p. 1 ^bukhari2026fast-002
- MeanFlow predicts the average velocity over a time interval, yielding a teacher-free and simulation-free objective that supports one-step and few-step generation. (Bukhari et al., 2026) `ev:cited` p. 1 ^bukhari2026fast-003
- Woo et al. extend MeanFlow to Riemannian manifolds through an algebraic semigroup consistency objective that avoids high-variance differential terms for stable training. (Bukhari et al., 2026) `ev:cited` p. 1 ^bukhari2026fast-004
- The authors state that whether few-step manifold sampling preserves implicit grasp contact constraints lacked evaluation backed by physics-based simulation and real-world experiments. (Bukhari et al., 2026) `ev:asserted` p. 1 ^bukhari2026fast-005
- The proposed method, called GraspMF, employs MeanFlow on the product Lie group G = SO(3)×R3 for fast grasp pose generation. (Bukhari et al., 2026) `ev:reported` p. 1 ^bukhari2026fast-006
- The authors argue that the concurrent work of Zhong et al. computes a covariant derivative that can hinder training stability. (Bukhari et al., 2026) `ev:asserted` p. 2 ^bukhari2026fast-007
- The authors state that the grasp generation quality of prior diffusion and flow-based grasping methods degrades at low sampling budgets. (Bukhari et al., 2026) `ev:asserted` p. 2 ^bukhari2026fast-008
- GraspMF couples grasp generation with geometric supervision through an auxiliary shape reconstruction objective grounded on the object geometry. (Bukhari et al., 2026) `ev:reported` p. 2 ^bukhari2026fast-009
- SE(3) as a semidirect product admits no bi-invariant Riemannian metric, so prior work models grasps on the direct product SO(3) × R3. (Bukhari et al., 2026) `ev:cited` p. 3 ^bukhari2026fast-010
- The network predicts the clean grasp endpoint directly, from which the average velocity and flow map are obtained in closed form. (Bukhari et al., 2026) `ev:reported` p. 3 ^bukhari2026fast-011
- The semigroup consistency identity is purely algebraic, involving only forward network evaluations, the group exponential and the group logarithm, without network derivatives. (Bukhari et al., 2026) `ev:computed` p. 4 ^bukhari2026fast-012
- The semigroup identity alone is data-free, since a degenerate zero-displacement predictor satisfies it identically, so an explicit data anchor is required. (Bukhari et al., 2026) `ev:computed` p. 4 ^bukhari2026fast-013
- The training objective is a weighted sum of a Riemannian flow-matching anchor at the time diagonal and a semigroup consistency loss. (Bukhari et al., 2026) `ev:reported` p. 5 ^bukhari2026fast-014
- Each GraspMF inference step costs exactly one network evaluation plus one closed-form exponential and logarithm pair on the group. (Bukhari et al., 2026) `ev:reported` p. 5 ^bukhari2026fast-015
- The network adopts the lightweight SE3Dif architecture with a pose prediction head replacing the scalar energy head. (Bukhari et al., 2026) `ev:reported` p. 5 ^bukhari2026fast-016
- A VNN point cloud encoder maps the object point cloud of N = 1024 points to a conditioning descriptor. (Bukhari et al., 2026) `ev:reported` p. 5 ^bukhari2026fast-017
- The 9-D raw rotation estimate from the network output is projected onto the nearest element of SO(3) via singular value decomposition. (Bukhari et al., 2026) `ev:reported` p. 6 ^bukhari2026fast-018
- The source prior is the product of the uniform Haar measure on SO(3) and a standard isotropic Gaussian on R3. (Bukhari et al., 2026) `ev:reported` p. 6 ^bukhari2026fast-019
- The semigroup loss weight is annealed linearly from 0 to 1 over the first 1000 epochs, with the anchor weight fixed at 1. (Bukhari et al., 2026) `ev:reported` p. 6 ^bukhari2026fast-020
- Both loss terms use an ℓ1 norm on each factor instead of the squared metric norm, which performed better across all their experiments. (Bukhari et al., 2026) `ev:reported` p. 6 ^bukhari2026fast-021
- An auxiliary clipped ℓ1 signed-distance regression onto ground-truth SDF values grounds the learned flow map to the object geometry. (Bukhari et al., 2026) `ev:reported` p. 6 ^bukhari2026fast-022
- Training uses Adam with a constant learning rate of 1 × 10−4 on a single NVIDIA RTX 5080 16GB GPU. (Bukhari et al., 2026) `ev:reported` p. 6 ^bukhari2026fast-023
- On an SO(3) baseball-seam toy dataset, MeanFlow concentrates samples on the seam within three network evaluations, whereas Flow Matching requires tens of steps. (Bukhari et al., 2026) `ev:measured` p. 6 ^bukhari2026fast-024
- Training and evaluation use ten [[ACRONYM dataset|ACRONYM]] shape categories, amounting to 416 object instances with about 780 K valid grasps. (Bukhari et al., 2026) `ev:reported` p. 7 ^bukhari2026fast-025
- 90% of instances per category are used for training all methods, with the remaining 10% reserved for in-domain evaluation. (Bukhari et al., 2026) `ev:reported` p. 7 ^bukhari2026fast-026
- Baselines are SE3Dif, EquiGraspFlow, BRIDGER and VSIGD, all configured at the sampling budgets reported by their authors. (Bukhari et al., 2026) `ev:reported` p. 7 ^bukhari2026fast-027
- Success rate is measured in Isaac Gym, counting a grasp as successful if the object remains in the gripper after a 5 s shake. (Bukhari et al., 2026) `ev:reported` p. 7 ^bukhari2026fast-028
- Earth Mover's Distance is computed between 100 sampled grasps and 100 ground-truth samples using a combined rotation and translation pose distance. (Bukhari et al., 2026) `ev:reported` p. 7 ^bukhari2026fast-029
- With five sampling steps, GraspMF achieves the highest success rate in both domains, 87.40% in-domain and 71.73% out-of-domain. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-030
- GraspMF at T = 5 attains the best out-of-domain EMD of 0.4191 at an inference latency of 15.5 ms. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-031
- The closest baselines, EGF in-domain and VSIGD out-of-domain, have 1.9–2.7 percentage points lower success rate than GraspMF at T = 5. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-032
- EGF, with a higher sampling budget and an equivariance-focused architecture, incurs about 12× higher latency than GraspMF, at 187.9 ms. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-033
- VSIGD, with its shape inference design, incurs about 73× higher latency than GraspMF, at 1124.4 ms. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-034
- Single-step GraspMF reaches 81.11% in-domain and 66.34% out-of-domain success rate at a 6.3 ms inference latency. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-035
- At their reported budgets, SE3Dif, VSIGD and EGF expend 140, 140 and 80 network evaluations, against 5 for GraspMF at T = 5. (Bukhari et al., 2026) `ev:reported` p. 8 ^bukhari2026fast-036
- In the qualitative comparison on Laptop, Pencil and Car, GraspMF produces a larger fraction of successful grasps than the baseline methods. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-037
- Across sampling budgets from 1 to 100, GraspMF's out-of-domain success rate averages 70.15% with a standard deviation of 1.63. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-038
- At T = 1 and T = 5, the success rate of SE3Dif drops to 6.65% and 18.58% respectively. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-039
- At T = 1 and T = 5, the success rate of VSIGD drops to 7.04% and 20.86% respectively. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-040
- The success rate of EGF drops to 27.48% at T = 1 but remains consistent for sampling budgets of T ≥ 5. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-041
- The success rate of EGF stays strictly below that of GraspMF at every sampling budget in the out-of-domain evaluation. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-042
- BRIDGER behaves erratically at low sampling budgets before stabilizing for T ≥ 10, which the authors read as not designed for few-step sampling. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-043
- GraspMF has the lowest inference latency of all compared methods at every sampling budget in the out-of-domain evaluation. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-044
- In the success rate versus latency plot, GraspMF occupies the upper-left region, tracing the Pareto frontier for the compared methods. (Bukhari et al., 2026) `ev:measured` p. 8 ^bukhari2026fast-045
- Removing the auxiliary signed-distance objective lowers success rate by 3.8% in-domain and 5.1% out-of-domain at T = 5. (Bukhari et al., 2026) `ev:measured` p. 9 ^bukhari2026fast-046
- Holding the semigroup weight constant instead of annealing it costs 2.4% in-domain and 5.8% out-of-domain success rate. (Bukhari et al., 2026) `ev:measured` p. 9 ^bukhari2026fast-047
- Replacing SVD projection with symmetric Gram–Schmidt orthonormalization leaves in-domain success rate unchanged but forfeits 4.7% in out-of-domain success rate. (Bukhari et al., 2026) `ev:measured` p. 9 ^bukhari2026fast-048
- The Gram–Schmidt variant reduces inference latency to 13.5 ms, compared with 15.5 ms for SVD rotation projection. (Bukhari et al., 2026) `ev:measured` p. 9 ^bukhari2026fast-049
- Replacing the semigroup loss with the decomposed objective of Zhong et al. lowers in-domain success rate by 25.15 percentage points. (Bukhari et al., 2026) `ev:measured` p. 9 ^bukhari2026fast-050
- The decomposed objective lowers out-of-domain success rate by 19.44 percentage points, the largest degradation among the ablated components. (Bukhari et al., 2026) `ev:measured` p. 9 ^bukhari2026fast-051
- The authors conclude that semigroup consistency is the principal contributor to preserving implicit contact constraints under a few-step budget. (Bukhari et al., 2026) `ev:asserted` p. 9 ^bukhari2026fast-052
- Under single-view partial observation, GraspMF at T = 5 attains the highest out-of-domain success rate, 68.46%, followed by BRIDGER at 65.38%. (Bukhari et al., 2026) `ev:measured` p. 9 ^bukhari2026fast-053
- Under partial observation, BRIDGER leads in-domain with 88.84% success rate, while GraspMF at T = 5 trails at 86.08%. (Bukhari et al., 2026) `ev:measured` p. 9 ^bukhari2026fast-054
- Under partial observation, GraspMF at T = 5 is 7.8× faster than BRIDGER, at 15.5 ms versus 120.6 ms. (Bukhari et al., 2026) `ev:measured` p. 9 ^bukhari2026fast-055
- Under partial observation, GraspMF records the highest out-of-domain EMD, 0.5923, which the authors link to the view-restricted reference grasp set. (Bukhari et al., 2026) `ev:measured` p. 9 ^bukhari2026fast-056
- The authors attribute lower partial-observation performance partly to single views resolving only the camera-facing surface, leaving occluded geometry to be inferred. (Bukhari et al., 2026) `ev:asserted` p. 9 ^bukhari2026fast-057
- The real-world test uses a Franka Research 3 manipulator with a Franka Hand gripper and a wrist-mounted Orbbec Femto Mega RGB-D camera. (Bukhari et al., 2026) `ev:reported` p. 9 ^bukhari2026fast-058
- In real-world trials, GraspMF at T = 5 succeeded in 9, 9 and 10 of 10 grasps on Black Mug, Red Mug and Gray Bowl. (Bukhari et al., 2026) `ev:measured` p. 10 ^bukhari2026fast-059
- In the same real-world trials, EGF at T = 20 succeeded in 10, 8 and 10 of 10 grasps. (Bukhari et al., 2026) `ev:measured` p. 10 ^bukhari2026fast-060
- The authors conclude the model attains grasp quality comparable to multi-step diffusion and flow baselines on [[ACRONYM dataset|ACRONYM]] at up to 39× lower latency. (Bukhari et al., 2026) `ev:asserted` p. 10 ^bukhari2026fast-061
- As future work, the authors plan extensions to general matrix Lie groups such as dual-arm SE(3) × SE(3) and contact manifolds. (Bukhari et al., 2026) `ev:asserted` p. 10 ^bukhari2026fast-062

## 🎯 Contributions

## 📖 Glossary

- **MeanFlow** — Generative model that learns the average velocity over a time interval for few-step sampling.
- **Flow Matching** — Training a vector field to match conditional velocities along a probability path from prior to data.
- **Semigroup consistency** — Requiring one flow-map jump over [s, t] to equal the two-step composition through r.
- **Left-trivialization** — Carrying tangent vectors of a Lie group back to its Lie algebra via left multiplication.
- **NFE** — Number of network function evaluations spent to generate one sample.
- **Sampling budget (T)** — Number of integration or flow-map steps used at inference.
- **Earth Mover's Distance (EMD)** — Optimal-transport distance between sampled and ground-truth grasp sets, used as a coverage proxy.
- **ACRONYM** — Large-scale simulated grasp dataset of object meshes with expert grasp annotations.
- **Lie–Euler scheme** — Euler integration on a Lie group that freezes velocity over each step via the exponential map.

## ❓ Open questions

- Does the semigroup-anchored MeanFlow formulation extend to other manipulation Lie groups, such as dual-arm SE(3) × SE(3) or contact manifolds?
- How much of the single-step latency advantage translates into better closed-loop replanning performance, which the authors suggest but do not test?
- Can the in-domain gap to BRIDGER under partial observation be closed by rejection sampling over larger candidate populations, as the authors propose?
- How does GraspMF perform in cluttered multi-object scenes rather than on single segmented objects?
- Is the real-world evaluation (three objects, 10 trials each) enough to separate GraspMF from EGF, which scored similarly?

## 📝 Notes on reading

- Version read: arXiv preprint v1 (2608.26076v1, 26 Aug 2026), set in a generic IEEE journal template.
- The ablation text (p. 9) reports drops such as 3.8% and 5.1% in success rate; these match percentage-point differences in Table III rather than relative percentages. Likewise the 2.76% partial-observation gap to BRIDGER is in percentage points.
- The headline 39× speed-up is not derived in the text; it is consistent with SE3Dif at 600.1 ms versus GraspMF (T = 5) at 15.5 ms in Table II.
- Fig. 4 (SR, EMD and latency versus sampling budget) was only available as axis tick labels in the extraction; per-budget values for baselines other than those quoted in Sec. V-C were not claimed.
- Real-world Table V: EGF (T = 20) totals 28/30 successes, the same as GraspMF (T = 5), while GraspMF (T = 10) totals 29/30; the abstract's claim of robust real-world transfer rests on 10 trials per object on three objects.
- Table I in-domain EMD: GraspMF T = 1 (0.3698) is marginally lower than T = 5 (0.3702), while the text calls the T = 5 ID EMD competitive rather than best.
- Equations (3)–(25) were partially garbled in extraction; derivation-level claims were kept to statements made in prose.

## Suggested new concepts

- MeanFlow — few-step generative modeling via average velocity; likely to recur across fast robot policy and grasping papers.
- Generative grasp synthesis — the family of diffusion and flow grasp samplers (SE3Dif, EGF, BRIDGER, VSIGD) compared here.
- Riemannian flow matching on Lie groups — shared machinery for pose generation on SO(3)×R3 and SE(3).
- ACRONYM dataset — standard benchmark for simulated 6-DoF grasp evaluation used by many grasping papers.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H2.** Genera agarres en SO(3)xR3 con 5 o menos evaluaciones de red, lo que permite replanificar agarres en bucle cerrado en tiempo real.
