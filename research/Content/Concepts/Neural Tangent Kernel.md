---
aliases: ["NTK"]
type: concept
element_type: concept
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-18
---

## Working definition

The kernel formed by inner products of a network's output gradients with respect to its parameters, which governs gradient-descent training dynamics in function space and becomes deterministic and constant during training in the infinite-width limit.

## Evidence

- [[Jacot2018neural - Neural Tangent Kernel Convergence and Generalization in#^jacot2018neural-019]] — Because the realization function of networks is not linear, the NTK is random at initialization and varies during training.
- [[Jacot2018neural - Neural Tangent Kernel Convergence and Generalization in#^jacot2018neural-021]] — Theorem 1 proves that at initialization the NTK converges in probability to a deterministic limiting kernel as layer widths grow.
- [[Jacot2018neural - Neural Tangent Kernel Convergence and Generalization in#^jacot2018neural-022]] — The limiting NTK depends only on the choice of nonlinearity, the network depth and the parameter variance at initialization.
- [[Jacot2018neural - Neural Tangent Kernel Convergence and Generalization in#^jacot2018neural-023]] — Theorem 2 proves that the NTK stays asymptotically constant during training, uniformly over a time interval, in the infinite-width limit.
- [[Jacot2018neural - Neural Tangent Kernel Convergence and Generalization in#^jacot2018neural-028]] — For a non-polynomial Lipschitz nonlinearity, the limiting NTK restricted to the unit sphere is positive definite for depth L ≥ 2.
- [[Jacot2018neural - Neural Tangent Kernel Convergence and Generalization in#^jacot2018neural-058]] — Since the NTK of large-width networks is more stable during training, larger learning rates can in principle be taken.
- [[Jacot2018neural - Neural Tangent Kernel Convergence and Generalization in#^jacot2018neural-059]] — The authors conclude that the limiting NTK is a powerful tool to understand the generalization properties of neural networks.
- [[Karakida2019pathological - Pathological spectra of the Fisher information metric and#^karakida2019pathological-041]] — The empirical FIM and the NTK share essentially the same non-zero eigenvalues, the NTK being the FIM's left-to-right reversal up to 1/N.
- [[Karakida2019pathological - Pathological spectra of the Fisher information metric and#^karakida2019pathological-042]] — Under the NTK parameterization, the derived eigenvalue statistics of the NTK become independent of the width scale M.
- [[Karakida2019pathological - Pathological spectra of the Fisher information metric and#^karakida2019pathological-044]] — Under NTK parameterization, the largest eigenvalue of the NTK depends on the sample size N, unlike its mean eigenvalue.
- [[Karakida2019pathological - Pathological spectra of the Fisher information metric and#^karakida2019pathological-046]] — According to the authors, NTK dynamics converge more slowly in the eigenspace of the relatively small eigenvalues, which are the majority.
- [[Karakida2019pathological - Pathological spectra of the Fisher information metric and#^karakida2019pathological-049]] — As the sample size increased in these experiments, most NTK eigenvalues concentrated close to zero, with the largest eigenvalues becoming outliers.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 2 sources · topic: Information geometry and natural-gradient optimization (drafter's packet `p1-information-geometry`, confirmed at the gate)
