---
aliases: []
type: "source"
title: "Model Predictive Path Integral Control as Preconditioned Gradient Descent"
citekey: "Fazlyab2026model"
doi: "10.48550/arXiv.2603.24489"
arxiv: "2603.24489"
year: 2026
publication_type: "preprint"
url: "https://arxiv.org/abs/2603.24489"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Mahyar Fazlyab", "Sina Sharifi", "Jiarui Wang"]
sha256: ["2db8295ac97373029d6706401869370cbec507eaab1855355b09ffec0d483e0f"]
pdf: "Content/Papers/Fazlyab2026model.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Fazlyab2026model.pdf]]

> [!abstract] One-sentence summary
> The paper derives classical MPPI as a unit-step preconditioned gradient step on a KL-regularized free-energy objective, which yields descent and stationarity guarantees and a covariance-size rule for when unit-step MPPI provably descends.

## Abstract

Model Predictive Path Integral (MPPI) control is a widely used sampling-based method for trajectory optimization, yet its convergence properties remain only partially understood. This paper provides a direct convergence analysis using variational optimization. By lifting constrained trajectory optimization to a Kullback-Leibler (KL) regularized problem over decision distributions, we derive a reduced free-energy objective defined over a parametric sampling family. For general parametric families, we derive gradient and Hessian representations of this reduced objective and analyze preconditioned gradient descent on the sampling-distribution parameters. In the fixed-covariance Gaussian case, the classical MPPI update is recovered exactly as a unit-step preconditioned gradient update. We prove descent and stationarity guarantees for the exact expectation-based iteration when the Hessian of the reduced objective is bounded in the metric induced by the preconditioner. For the Gaussian family, we further show that the preconditioned Hessian is governed by the covariance of the Gibbs-tilted distribution relative to the covariance of the sampling distribution, yielding a covariance-dependent sufficient condition for the descent of exact unit-step MPPI. Numerical experiments illustrate the theory and the effect of key hyperparameters. (arXiv)

## 🧠 Key ideas (atomic)

- Prior work leaves MPPI's relation to gradient methods, its guaranteed descent and its hyperparameter effects on convergence only partially understood. (Fazlyab et al., 2026) `ev:cited` p. 1 ^fazlyab2026model-001
- [[Model Predictive Path Integral control|Standard MPPI]] shifts the nominal control toward a cost-weighted average of sampled perturbed control sequences drawn from the sampling distribution. (Fazlyab et al., 2026) `ev:asserted` p. 1 ^fazlyab2026model-002
- The authors argue that stochastic optimal control or control-as-inference derivations of MPPI do not directly expose its underlying optimization structure. (Fazlyab et al., 2026) `ev:asserted` p. 1 ^fazlyab2026model-003
- The paper lifts constrained trajectory optimization to a KL-regularized distributional problem to give a variational, optimization-theoretic analysis of MPPI. (Fazlyab et al., 2026) `ev:asserted` p. 1 ^fazlyab2026model-004
- The framework yields an O(1/K) ergodic stationarity rate for the exact preconditioned-gradient iteration under a preconditioner-metric Hessian bound. (Fazlyab et al., 2026) `ev:computed` p. 1 ^fazlyab2026model-005
- The authors state the framework gives a principled basis for choosing step size, multiple inner updates, and stationarity-based stopping criteria. (Fazlyab et al., 2026) `ev:asserted` p. 1 ^fazlyab2026model-006
- A variational inference MPC framework was earlier shown to recover MPPI, CEM and CMA-ES as special cases. (Fazlyab et al., 2026) `ev:cited` p. 1 ^fazlyab2026model-007
- Wagener et al. showed that an exponential-utility trajectory objective yields [[Model Predictive Path Integral control|classical MPPI]] under a fixed-covariance Gaussian family with unit step size. (Fazlyab et al., 2026) `ev:cited` p. 2 ^fazlyab2026model-008
- CoVO-MPC used contraction theory to prove at least linear convergence of MPPI for time-varying LQR problems. (Fazlyab et al., 2026) `ev:cited` p. 2 ^fazlyab2026model-009
- The authors note the CoVO-MPC contraction result cannot extend to general nonlinear settings without extra regularity assumptions. (Fazlyab et al., 2026) `ev:asserted` p. 2 ^fazlyab2026model-010
- The authors state their convergence analysis covers general nonlinear systems and costs, with a bounded feasible set as the main requirement. (Fazlyab et al., 2026) `ev:asserted` p. 2 ^fazlyab2026model-011
- The analysis assumes the set of feasible control sequences is nonempty and compact, with a continuous trajectory objective. (Fazlyab et al., 2026) `ev:reported` p. 2 ^fazlyab2026model-012
- Without KL regularization, the lifted distributional problem collapses to a Dirac measure at a minimizer of the trajectory objective. (Fazlyab et al., 2026) `ev:computed` p. 2 ^fazlyab2026model-013
- For any fixed base distribution, the KL-regularized problem provides an upper bound on the optimal value of the original constrained problem. (Fazlyab et al., 2026) `ev:computed` p. 2 ^fazlyab2026model-014
- The authors restrict the sampling distribution to a tractable family, since unrestricted optimization over it may collapse onto the decision distribution. (Fazlyab et al., 2026) `ev:asserted` p. 2 ^fazlyab2026model-015
- For a fixed sampling distribution, the optimal decision distribution is a truncated Gibbs tilt weighting samples by exponentiated negative cost on the feasible set. (Fazlyab et al., 2026) `ev:computed` p. 2 ^fazlyab2026model-016
- The appendix proves the truncated Gibbs tilt is the unique minimizer of the KL-regularized problem, with minimum value −τ log Z(π). (Fazlyab et al., 2026) `ev:computed` p. 7 ^fazlyab2026model-017
- Under the truncated Gibbs tilt, lower-cost feasible control sequences receive larger probability mass, whereas infeasible sequences receive zero mass. (Fazlyab et al., 2026) `ev:computed` p. 3 ^fazlyab2026model-018
- Eliminating the decision distribution reduces the joint problem to minimizing a negative log-partition, or free-energy, objective over the sampling family. (Fazlyab et al., 2026) `ev:computed` p. 3 ^fazlyab2026model-019
- Unlike the original constrained trajectory problem, the reduced objective is differentiable in the distribution parameters, making it amenable to gradient-based optimization. (Fazlyab et al., 2026) `ev:computed` p. 3 ^fazlyab2026model-020
- The gradient of the reduced objective equals minus τ times the Gibbs-tilted expectation of the sampling family's score function. (Fazlyab et al., 2026) `ev:computed` p. 3 ^fazlyab2026model-021
- The Hessian of the reduced objective combines the tilted expectation of the log-density Hessian with the tilted covariance of the score. (Fazlyab et al., 2026) `ev:computed` p. 3 ^fazlyab2026model-022
- The sampled update replaces generally intractable tilted expectations with self-normalized importance weights over samples from the current sampling distribution. (Fazlyab et al., 2026) `ev:reported` p. 3 ^fazlyab2026model-023
- Theorem 1 proves monotone descent of the exact preconditioned gradient iteration for any constant step size between zero and 2/LP. (Fazlyab et al., 2026) `ev:computed` p. 4 ^fazlyab2026model-024
- Theorem 1 further shows the preconditioned gradient norm of the exact iteration converges to zero, so iterates approach stationarity. (Fazlyab et al., 2026) `ev:computed` p. 4 ^fazlyab2026model-025
- The authors suggest the preconditioned gradient norm as a natural stopping criterion for the multi-step MPPI algorithm. (Fazlyab et al., 2026) `ev:asserted` p. 4 ^fazlyab2026model-026
- For the fixed-covariance Gaussian family, choosing preconditioner Σ/τ with unit step size recovers exactly [[Model Predictive Path Integral control|the classical MPPI update]]. (Fazlyab et al., 2026) `ev:computed` p. 4 ^fazlyab2026model-027
- With preconditioner Σ/τ, the preconditioned Hessian equals the identity minus the whitened covariance of the Gibbs-tilted distribution. (Fazlyab et al., 2026) `ev:computed` p. 4 ^fazlyab2026model-028
- After preconditioning with Σ/τ, the explicit dependence of the reduced objective's curvature on the temperature τ disappears. (Fazlyab et al., 2026) `ev:computed` p. 4 ^fazlyab2026model-029
- The authors call the update that mixes the current mean with the tilted mean using step η the exact relaxed MPPI update. (Fazlyab et al., 2026) `ev:reported` p. 4 ^fazlyab2026model-030
- Theorem 2 bounds the Gaussian smoothness constant by the maximum of 1 and the squared whitened feasible-set diameter over 4 minus 1. (Fazlyab et al., 2026) `ev:computed` p. 5 ^fazlyab2026model-031
- [[Model Predictive Path Integral control|Exact unit-step MPPI]] satisfies the descent guarantees of Theorem 1 when the squared whitened feasible-set diameter is below 12. (Fazlyab et al., 2026) `ev:computed` p. 5 ^fazlyab2026model-032
- That sufficient condition is guaranteed when the smallest covariance eigenvalue is at least the squared Euclidean feasible-set diameter divided by 12. (Fazlyab et al., 2026) `ev:computed` p. 5 ^fazlyab2026model-033
- The authors conclude that overly concentrated sampling distributions can destroy the global descent guarantee, whereas sufficiently diffuse sampling is enough to ensure it. (Fazlyab et al., 2026) `ev:asserted` p. 5 ^fazlyab2026model-034
- The authors note that the self-normalized importance-sampling estimator used by the sampled update is generally biased. (Fazlyab et al., 2026) `ev:asserted` p. 5 ^fazlyab2026model-035
- With estimator bias and noise, the expected descent bound is preserved up to two terms controlled by finite-sample gradient estimation error. (Fazlyab et al., 2026) `ev:computed` p. 5 ^fazlyab2026model-036
- The authors leave a complete non-asymptotic analysis of the bias and variance of the self-normalized estimator to future work. (Fazlyab et al., 2026) `ev:asserted` p. 5 ^fazlyab2026model-037
- The LQR benchmark uses double-integrator dynamics with horizon T = 10 and initial state x0 = (2.5, 0). (Fazlyab et al., 2026) `ev:reported` p. 5 ^fazlyab2026model-038
- The LQR constraint set enforces control bounds |u| ≤ 1 together with state constraints x ∈ [−5, 5] × [−1, 1]. (Fazlyab et al., 2026) `ev:reported` p. 5 ^fazlyab2026model-039
- The LQR experiments set a budget of N = 1000 samples per iteration for the sampling-based methods. (Fazlyab et al., 2026) `ev:reported` p. 5 ^fazlyab2026model-040
- On LQR, when the smoothness constant is small, such as 0.1, a step size larger than MPPI's unit step converged faster. (Fazlyab et al., 2026) `ev:measured` p. 5 ^fazlyab2026model-041
- On the LQR benchmark, multi-step MPPI outperformed a finite-difference baseline in the right panel of Figure 1. (Fazlyab et al., 2026) `ev:measured` p. 5 ^fazlyab2026model-042
- For LQR with scalar variance, the smoothness constant has the closed form LΣ = 1 − τ/(τ + σ2λmax(Q)). (Fazlyab et al., 2026) `ev:computed` p. 8 ^fazlyab2026model-043
- In the LQR case, increasing the sampling variance σ2 increases the smoothness constant LΣ, per the closed-form expression. (Fazlyab et al., 2026) `ev:computed` p. 8 ^fazlyab2026model-044
- In the LQR case, the temperature τ has the reversed effect of the sampling variance on the smoothness constant LΣ. (Fazlyab et al., 2026) `ev:computed` p. 8 ^fazlyab2026model-045
- Experiments were implemented in Python using JAX for batched trajectory rollout and vectorized cost evaluation. (Fazlyab et al., 2026) `ev:reported` p. 7 ^fazlyab2026model-046
- The LQR GD-MPPI runs used 1000 antithetic Gaussian samples per iteration with a control mean initialized to zero. (Fazlyab et al., 2026) `ev:reported` p. 7 ^fazlyab2026model-047
- The LQR GD-MPPI runs used 20,000 inner iterations, selecting feasible samples by rejection using the state constraints. (Fazlyab et al., 2026) `ev:reported` p. 7 ^fazlyab2026model-048
- The finite-difference baseline used perturbation standard deviation 10−3, step size 10−3, and projection back onto the feasible LQR set. (Fazlyab et al., 2026) `ev:reported` p. 7 ^fazlyab2026model-049
- LQR convergence was reported as the optimality gap relative to a reference optimal value computed with CVXPY. (Fazlyab et al., 2026) `ev:reported` p. 7 ^fazlyab2026model-050
- The Dubins car task reaches xd = (6, 6, 0) from x0 = (0, 0, π/2) amid clutter with horizon T = 20. (Fazlyab et al., 2026) `ev:reported` p. 6 ^fazlyab2026model-051
- In the Dubins car task, the car moves at constant velocity v = 4, using N = 1024 samples. (Fazlyab et al., 2026) `ev:reported` p. 6 ^fazlyab2026model-052
- On the Dubins car task, [[Model Predictive Path Integral control|single-step MPPI]] selects a suboptimal path, which the authors attribute to it not iterating until convergence. (Fazlyab et al., 2026) `ev:measured` p. 6 ^fazlyab2026model-053
- On the Dubins car benchmark, MPPI with K = 1 reached an average cost of 26.14 with a runtime of 16.8 s. (Fazlyab et al., 2026) `ev:measured` p. 6 ^fazlyab2026model-054
- On the Dubins car benchmark, M-MPPI with K = 10 reached an average cost of 23.85 with a runtime of 47.8 s. (Fazlyab et al., 2026) `ev:measured` p. 6 ^fazlyab2026model-055
- On the Dubins car benchmark, Log-MPPI reached an average cost of 24.3 with a runtime of 17.1 s. (Fazlyab et al., 2026) `ev:measured` p. 6 ^fazlyab2026model-056
- On the Dubins car benchmark, sample acceptance rose from 0.75 for MPPI to 0.80 for M-MPPI with K = 10. (Fazlyab et al., 2026) `ev:measured` p. 6 ^fazlyab2026model-057
- The authors report that increasing the number of inner iterations K improves average cost on Dubins car at the expense of runtime. (Fazlyab et al., 2026) `ev:measured` p. 6 ^fazlyab2026model-058
- The reported Dubins car comparison results in Table I were averaged over 3 seeds by the authors. (Fazlyab et al., 2026) `ev:reported` p. 6 ^fazlyab2026model-059
- The authors state their analysis covers the exact expectation-based iteration, leaving finite-sample and receding-horizon closed-loop behavior for future work. (Fazlyab et al., 2026) `ev:asserted` p. 6 ^fazlyab2026model-060
- The authors conclude that these results help demystify MPPI from an optimization viewpoint and open the door to principled extensions. (Fazlyab et al., 2026) `ev:asserted` p. 6 ^fazlyab2026model-061

## 🎯 Contributions

## 📖 Glossary

- **MPPI** — Model Predictive Path Integral control; sampling-based trajectory optimizer averaging cost-weighted rollouts.
- **Free-energy objective** — Negative log-partition −τ log Z of the sampling distribution under exponentiated negative cost.
- **Gibbs tilt** — Reweighting of a base distribution by exp(−cost/τ), here truncated to the feasible set.
- **Preconditioned gradient descent** — Gradient descent whose step is multiplied by a fixed positive definite matrix P.
- **Temperature τ** — KL regularization weight; smaller τ concentrates the tilted distribution on low-cost controls.
- **Self-normalized importance sampling** — Estimating expectations with sample weights divided by their sum; generally biased.
- **Ergodic stationarity rate** — Bound on the minimum gradient norm over the first K iterates.
- **M-MPPI** — Multi-step MPPI: several inner preconditioned updates of the sampling mean per control step.

## ❓ Open questions

- How large are the bias and variance of the self-normalized estimator, and what finite-sample descent guarantee follows?
- Do the guarantees carry over to receding-horizon, closed-loop MPPI rather than the exact expectation-based iteration?
- Can the analysis extend to families that also adapt the covariance, not only the mean?
- Is the diameter-based covariance condition tight, or only sufficient in practice?
- How should step size be chosen when LΣ cannot be computed explicitly, as in nonlinear tasks?

## 📝 Notes on reading

- Version read: arXiv 2603.24489v2 [math.OC], dated 22 May 2026, 8 pages including appendix.
- Figure 1 (p. 5) shows ablations of Σ and τ on LQR (η = 1 vs η = 1/LΣ) and M-MPPI vs finite differences; curves were only described in the text, so no numeric claims were drawn from it.
- Figure 2 (p. 6) shows MPPI (K = 1) and M-MPPI (K = 10) trajectories on Dubins car, with safe and unsafe trajectories in blue and red.
- Table I header says "Sample acceptance rate %", but the values (0.75–0.80) look like fractions rather than percentages.
- Table I gives Log-MPPI's average cost as 24.3, with one decimal, while other rows use two.
- A sentence in the Diffusion Perspective paragraph (p. 1) is garbled in the extraction ("score estimation result from [12] that Mscore-estimation result from [12]").
- The paper states the sufficient condition as a strict inequality on the whitened diameter (< 12) but the eigenvalue condition as λmin(Σ) ≥ D²/12, which only yields ≤ 12; a minor inconsistency.
- Theorem 2 writes C ⊂ R^m while its proof uses unit vectors in R^n; notation is loose.
- The appendix calls the LQR method "GD-MPPI", while the main text uses "M-MPPI"; they appear to denote the same multi-step method.

## Suggested new concepts

- Model Predictive Path Integral control — central sampling-based MPC method that many vault sources will reference.
- Variational optimization — lifting pointwise optimization to distributions; the core device of this paper's analysis.
- Free-energy (log-partition) objective — unifies MPPI, path-integral control and Gibbs-weighted sampling methods.
- Self-normalized importance sampling — the biased estimator underlying practical MPPI updates.
- Preconditioned gradient descent — optimization lens that reframes MPPI's hyperparameters as step size and metric.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H3.** Demuestra que la actualización de MPPI es un paso de gradiente precondicionado, puente formal entre gradientes covariantes y gradiente natural.
