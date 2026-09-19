---
aliases: ["Newton-Schulz iteration"]
type: concept
element_type: method
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-19
---

## Working definition

An iterative odd-polynomial matrix routine that pushes every singular value of a matrix toward one, approximating its semi-orthogonal factor UV^T without an SVD, and so computes spectral-norm steepest-descent updates such as Muon's.

## Evidence

- [[Bernstein2024old - Old Optimizer, New Norm An Anthology#^bernstein2024old-064]] — The authors list SVD, sketching, Newton iteration for inverse roots and Newton-Schulz iteration as ways to compute the update.
- [[Bernstein2024old - Old Optimizer, New Norm An Anthology#^bernstein2024old-065]] — The Newton-Schulz iteration applies a cubic polynomial to each singular value, pushing values in its convergence range toward one.
- [[Bernstein2024old - Old Optimizer, New Norm An Anthology#^bernstein2024old-066]] — The iteration converges if the initial matrix has all singular values greater than zero and less than the square root of three.
- [[Bernstein2024old - Old Optimizer, New Norm An Anthology#^bernstein2024old-067]] — After first posting the paper, the authors learned that the iteration, at least for fixed coefficients, is classical.
- [[Liu2025muon - Muon is Scalable for LLM Training#^liu2025muon-001]] — Muon, proposed by Jordan et al. in 2024, updates matrix parameters with orthogonalized gradient momentum computed through Newton-Schulz iteration.
- [[Liu2025muon - Muon is Scalable for LLM Training#^liu2025muon-002]] — A Newton-Schulz iteration approximately replaces the momentum matrix with its orthogonal factor from the singular value decomposition, orthogonalizing the update.
- [[Liu2025muon - Muon is Scalable for LLM Training#^liu2025muon-003]] — The authors keep the original Newton-Schulz coefficients a = 3.4445, b = −4.7750, c = 2.0315, which speed convergence for small initial singular values.
- [[Liu2025muon - Muon is Scalable for LLM Training#^liu2025muon-004]] — Under the steepest-descent view, Muon offers a norm constraint that becomes the spectral norm when the orthogonalization is computed exactly.
- [[Liu2025muon - Muon is Scalable for LLM Training#^liu2025muon-017]] — Setting N to 10 yielded a more accurate orthogonalization than N = 5, but did not lead to better performance.
- [[Liu2025muon - Muon is Scalable for LLM Training#^liu2025muon-021]] — Each rank runs Newton-Schulz on the full gathered matrix, then discards the update except the partition matching its local parameters.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: promoted at the bar from 2 sources · topic: Information geometry and natural-gradient optimization (drafter's packet `q4-geometric-finetuning`, confirmed at the gate)
