---
aliases: []
type: "source"
title: "Riemannian Adaptive Optimization Methods"
citekey: "Becigneul2018riemannian"
doi: "10.48550/arXiv.1810.00760"
arxiv: "1810.00760"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1810.00760"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Gary Bécigneul", "Octavian-Eugen Ganea"]
sha256: ["5923517615e9dd5931b3f519613dc0510502acc5db2cf6e8a76702d308f4b3ee"]
pdf: "Content/Papers/Becigneul2018riemannian.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 58
---

📄 PDF: [[Becigneul2018riemannian.pdf]]

> [!abstract] One-sentence summary
> The paper extends Adagrad, Adam and Amsgrad to Cartesian products of Riemannian manifolds with regret bounds, and shows faster training for hyperbolic WordNet embeddings.

## Abstract

Several first order stochastic optimization methods commonly used in the Euclidean domain such as stochastic gradient descent (SGD), accelerated gradient descent or variance reduced methods have already been adapted to certain Riemannian settings. However, some of the most popular of these optimization tools - namely Adam , Adagrad and the more recent Amsgrad - remain to be generalized to Riemannian manifolds. We discuss the difficulty of generalizing such adaptive schemes to the most agnostic Riemannian setting, and then provide algorithms and convergence proofs for geodesically convex objectives in the particular case of a product of Riemannian manifolds, in which adaptivity is implemented across manifolds in the cartesian product. Our generalization is tight in the sense that choosing the Euclidean space as Riemannian manifold yields the same algorithms and regret bounds as those that were already known for the standard algorithms. Experimentally, we show faster convergence and to a lower train loss value for Riemannian adaptive methods over their corresponding baselines on the realistic task of embedding the WordNet taxonomy in the Poincare ball. (arXiv)

## 🧠 Key ideas (atomic)

- On a Riemannian manifold one is generally not given an intrinsic coordinate system, which renders sparsity or coordinate-wise updates meaningless. (Bécigneul & Ganea, 2018) `ev:asserted` p. 1 ^becigneul2018riemannian-001
- The paper argues that generalizing coordinate-wise adaptive schemes to the most agnostic Riemannian setting in an intrinsic manner is compromised. (Bécigneul & Ganea, 2018) `ev:asserted` p. 2 ^becigneul2018riemannian-002
- The authors propose adaptive algorithms with convergence analysis for a product of manifolds, where each manifold represents one coordinate of the scheme. (Bécigneul & Ganea, 2018) `ev:asserted` p. 2 ^becigneul2018riemannian-003
- The motivating application was learning symbolic embeddings in non-Euclidean spaces, including recent embedding methods in hyperbolic spaces. (Bécigneul & Ganea, 2018) `ev:asserted` p. 2 ^becigneul2018riemannian-004
- The authors note that GloVe benefits significantly from Adagrad compared to SGD, presumably because different words are sampled at different frequencies. (Bécigneul & Ganea, 2018) `ev:asserted` p. 2 ^becigneul2018riemannian-005
- Bonnabel defines Riemannian SGD by moving along the [[Exponential map|exponential map]] in the direction of the negative scaled Riemannian gradient. (Bécigneul & Ganea, 2018) `ev:cited` p. 3 ^becigneul2018riemannian-006
- When the [[Exponential map|exponential map]] is not known in closed form, it is common to replace it by a retraction, most often x plus v. (Bécigneul & Ganea, 2018) `ev:asserted` p. 3 ^becigneul2018riemannian-007
- The paper notes that the accumulation of all past squared gradients in Adagrad can also slow down learning. (Bécigneul & Ganea, 2018) `ev:asserted` p. 3 ^becigneul2018riemannian-008
- According to the paper, Reddi et al. identified a mistake in the convergence proof of Adam, which motivated the Amsgrad modification. (Bécigneul & Ganea, 2018) `ev:cited` p. 3 ^becigneul2018riemannian-009
- The RSGD update is intrinsic to the manifold since it only involves the [[Exponential map|exponential map]] and the Riemannian gradient. (Bécigneul & Ganea, 2018) `ev:asserted` p. 4 ^becigneul2018riemannian-010
- It is unclear whether the Adagrad, Adam or Amsgrad updates can be expressed in a coordinate-free or intrinsic manner on a manifold. (Bécigneul & Ganea, 2018) `ev:asserted` p. 4 ^becigneul2018riemannian-011
- Parallel-transporting a fixed tangent coordinate system along the trajectory would almost surely break gradient sparsity through the rotational component induced by curvature. (Bécigneul & Ganea, 2018) `ev:asserted` p. 4 ^becigneul2018riemannian-012
- The authors state that their proof techniques would not apply to updates defined by parallel-transporting a coordinate system in the tangent space. (Bécigneul & Ganea, 2018) `ev:asserted` p. 4 ^becigneul2018riemannian-013
- Riemannian Adagrad treats each component manifold of the Cartesian product as one coordinate of the adaptive scheme. (Bécigneul & Ganea, 2018) `ev:asserted` p. 4 ^becigneul2018riemannian-014
- The adaptivity term uses squared Riemannian norms of each component gradient in place of the scalar squared Euclidean coordinate gradients. (Bécigneul & Ganea, 2018) `ev:asserted` p. 4 ^becigneul2018riemannian-015
- The paper motivates the Riemannian norm by noting that an RSGD step in each manifold has length equal to learning rate times that norm. (Bécigneul & Ganea, 2018) `ev:computed` p. 5 ^becigneul2018riemannian-016
- The convergence analysis assumes each component manifold is geodesically complete with sectional curvature lower bounded by a non-positive constant. (Bécigneul & Ganea, 2018) `ev:reported` p. 5 ^becigneul2018riemannian-017
- The feasible parameter set is a product of compact, geodesically convex sets whose diameters are bounded by a common constant. (Bécigneul & Ganea, 2018) `ev:reported` p. 5 ^becigneul2018riemannian-018
- In Riemannian Amsgrad, the momentum term is carried to the next iterate by an arbitrary isometry between the tangent spaces. (Bécigneul & Ganea, 2018) `ev:reported` p. 5 ^becigneul2018riemannian-019
- A natural choice for this isometry is parallel transport along the update direction, followed by transport along a minimizing geodesic after projection. (Bécigneul & Ganea, 2018) `ev:asserted` p. 5 ^becigneul2018riemannian-020
- When every component manifold is the real line, Riemannian Amsgrad and the standard Euclidean Amsgrad algorithm coincide exactly. (Bécigneul & Ganea, 2018) `ev:computed` p. 5 ^becigneul2018riemannian-021
- Riemannian Adam is obtained from Riemannian Amsgrad simply by removing the max operation applied to the adaptivity term. (Bécigneul & Ganea, 2018) `ev:reported` p. 6 ^becigneul2018riemannian-022
- Theorem 1 bounds the regret of Riemannian Amsgrad for geodesically convex objectives with step sizes decaying as alpha over the square root of t. (Bécigneul & Ganea, 2018) `ev:computed` p. 6 ^becigneul2018riemannian-023
- The curvature-dependent factor in the Riemannian bound becomes equal to 1 in Euclidean space, recovering the convergence theorem of Amsgrad. (Bécigneul & Ganea, 2018) `ev:computed` p. 6 ^becigneul2018riemannian-024
- For small but non-zero curvature, the regret bound worsens by a multiplicative factor of approximately 1 + D∞|κ|/6. (Bécigneul & Ganea, 2018) `ev:computed` p. 6 ^becigneul2018riemannian-025
- Theorem 2 provides a regret bound for Riemannian AdamNC, using a geometrically decaying momentum schedule and a non-constant second-moment schedule. (Bécigneul & Ganea, 2018) `ev:computed` p. 6 ^becigneul2018riemannian-026
- Setting the momentum parameter to zero in Theorem 2 yields a convergence proof for the Riemannian Adagrad update rule. (Bécigneul & Ganea, 2018) `ev:computed` p. 6 ^becigneul2018riemannian-027
- The curvature-dependent quantity in the bounds comes from a cosine-law lemma by Zhang & Sra, valid in all Alexandrov spaces. (Bécigneul & Ganea, 2018) `ev:cited` p. 6 ^becigneul2018riemannian-028
- The authors state that the bounds significantly improve for sparse per-manifold gradients, as when just a few words are updated at a time. (Bécigneul & Ganea, 2018) `ev:asserted` p. 7 ^becigneul2018riemannian-029
- The authors suggest that the regret bounds could be improved by exploiting momentum in the proofs for a particular isometry choice. (Bécigneul & Ganea, 2018) `ev:asserted` p. 7 ^becigneul2018riemannian-030
- The experiments embed the transitive closure of the WordNet noun hierarchy in the Poincaré ball, following the setup of Nickel & Kiela. (Bécigneul & Ganea, 2018) `ev:reported` p. 7 ^becigneul2018riemannian-031
- The WordNet transitive closure used consists of 82,115 nouns and 743,241 hypernymy Is-A relations treated as directed edges. (Bécigneul & Ganea, 2018) `ev:reported` p. 7 ^becigneul2018riemannian-032
- The Poincaré model was chosen because it gives closed-form expressions for all the quantities used in the Riemannian Amsgrad algorithm. (Bécigneul & Ganea, 2018) `ev:asserted` p. 7 ^becigneul2018riemannian-033
- The loss follows Nickel & Kiela, approximating the partition function by sampling negative word pairs, whose number is fixed to 10. (Bécigneul & Ganea, 2018) `ev:reported` p. 7 ^becigneul2018riemannian-034
- Evaluation reports the loss value together with mean average precision, in both the reconstruction and the link prediction settings. (Bécigneul & Ganea, 2018) `ev:reported` p. 7 ^becigneul2018riemannian-035
- For link prediction, a validation set of 2% edges is sampled from transitive closure edges that contain no leaf node or root. (Bécigneul & Ganea, 2018) `ev:reported` p. 7 ^becigneul2018riemannian-036
- Only 5-dimensional hyperbolic spaces were studied in the experiments, following the dimension choice of Nickel & Kiela. (Bécigneul & Ganea, 2018) `ev:reported` p. 7 ^becigneul2018riemannian-037
- All methods share a burn-in phase of 20 epochs using RSGD with retraction at a fixed learning rate of 0.03. (Bécigneul & Ganea, 2018) `ev:reported` p. 7 ^becigneul2018riemannian-038
- During burn-in only, negative words were sampled according to their graph degree raised to the power 0.75. (Bécigneul & Ganea, 2018) `ev:reported` p. 7 ^becigneul2018riemannian-039
- The authors report that degree-based negative sampling during the burn-in phase improves all evaluation metrics. (Bécigneul & Ganea, 2018) `ev:measured` p. 7 ^becigneul2018riemannian-040
- After the burn-in phase, negative words are sampled uniformly when the different optimization methods start. (Bécigneul & Ganea, 2018) `ev:reported` p. 7 ^becigneul2018riemannian-041
- Riemannian Adam gave slightly better results than Riemannian Amsgrad in the experiments, so the paper mostly reports the former. (Bécigneul & Ganea, 2018) `ev:measured` p. 8 ^becigneul2018riemannian-042
- Replacing the [[Exponential map|true exponential map]] with its first-order retraction unexpectedly led to convergence to lower loss values, in RSGD and adaptive methods. (Bécigneul & Ganea, 2018) `ev:measured` p. 8 ^becigneul2018riemannian-043
- The authors suggest retraction methods may need fewer steps and smaller gradients to escape points sub-optimally collapsed on the ball border. (Bécigneul & Ganea, 2018) `ev:asserted` p. 8 ^becigneul2018riemannian-044
- All methods were run with learning rates chosen from a grid of values spanning 0.001 to 3.0 in the experiments. (Bécigneul & Ganea, 2018) `ev:reported` p. 8 ^becigneul2018riemannian-045
- Riemannian Adam and Amsgrad always used β1 = 0.9 with β2 = 0.999, as these settings achieved the lowest training loss. (Bécigneul & Ganea, 2018) `ev:reported` p. 8 ^becigneul2018riemannian-046
- Riemannian Adagrad was consistently worse in the experiments, so the authors do not report its results in the figures. (Bécigneul & Ganea, 2018) `ev:measured` p. 8 ^becigneul2018riemannian-047
- Riemannian Adam always achieves the lowest training loss among the compared methods in the WordNet embedding experiments. (Bécigneul & Ganea, 2018) `ev:measured` p. 8 ^becigneul2018riemannian-048
- In the full Riemannian setting, Riemannian Adam also outperforms all other methods on MAP for reconstruction and link prediction. (Bécigneul & Ganea, 2018) `ev:measured` p. 8 ^becigneul2018riemannian-049
- In the retraction setting, Riemannian Adam is on par with RSGD on MAP for both reconstruction and link prediction. (Bécigneul & Ganea, 2018) `ev:measured` p. 8 ^becigneul2018riemannian-050
- In the retraction setting, Riemannian Amsgrad is faster to converge in MAP for link prediction, which the authors suggest indicates better generalization. (Bécigneul & Ganea, 2018) `ev:measured` p. 8 ^becigneul2018riemannian-051
- Roy et al. proposed Riemannian counterparts of SGD with momentum and RMSprop, but provided no convergence guarantee according to the authors. (Bécigneul & Ganea, 2018) `ev:cited` p. 8 ^becigneul2018riemannian-052
- The authors argue that performing coordinate-wise adaptive operations in a tangent-space coordinate system compromises obtaining convergence guarantees, as in Roy et al. (Bécigneul & Ganea, 2018) `ev:asserted` p. 9 ^becigneul2018riemannian-053
- The Riemannian Adam of Cho & Lee for the Grassmann manifold removes the adaptive component, since its adaptivity term becomes a scalar. (Bécigneul & Ganea, 2018) `ev:cited` p. 9 ^becigneul2018riemannian-054
- The authors conclude that their derived convergence rates are similar to those of the corresponding Euclidean adaptive optimization methods. (Bécigneul & Ganea, 2018) `ev:asserted` p. 9 ^becigneul2018riemannian-055
- The authors conclude that their methods outperform popular non-adaptive methods such as RSGD on hyperbolic word taxonomy embedding. (Bécigneul & Ganea, 2018) `ev:asserted` p. 9 ^becigneul2018riemannian-056
- Like Amsgrad, Riemannian Amsgrad also has a regret bounded by a term growing with G∞ times the square root of T. (Bécigneul & Ganea, 2018) `ev:computed` p. 14 ^becigneul2018riemannian-057
- The appendix states that a factor n/α is missing in corollaries 1 and 2 of Reddi et al., calling it a mistake. (Bécigneul & Ganea, 2018) `ev:asserted` p. 15 ^becigneul2018riemannian-058

## 🎯 Contributions

## 📖 Glossary

- **Riemannian manifold** — A smooth space equipped with a smoothly varying inner product on each tangent space.
- **Exponential map** — Maps a tangent vector to the manifold point reached along the corresponding geodesic.
- **Retraction** — First-order approximation of the exponential map, often x plus v.
- **Parallel transport** — Moves a tangent vector along a curve with zero acceleration, depending on the path.
- **Geodesic convexity** — Convexity defined along geodesics, using the logarithmic map instead of vector differences.
- **Regret** — Cumulative online loss minus the loss of the best fixed feasible parameter.
- **Poincaré ball** — Model of hyperbolic space on the open unit ball with a conformal metric.
- **Holonomy** — Rotational component of parallel transport inherited from curvature.
- **Alexandrov space** — Metric space with curvature bounds, where the Zhang–Sra cosine inequality holds.
- **RAMSGRAD** — Riemannian Amsgrad with per-manifold adaptivity and momentum transported by an isometry.

## ❓ Open questions

- Can adaptive schemes be defined intrinsically on a single general Riemannian manifold, without a product structure?
- Could a specific isometry choice, such as parallel transport, tighten the regret bounds by exploiting momentum?
- Why does the retraction reach lower training loss than the exact exponential map on the Poincaré ball?
- Do the gains carry over to the Lorentz model, entailment cones or other hyperbolic embedding methods mentioned by the authors?
- Do the results hold beyond 5-dimensional embeddings and beyond the WordNet noun hierarchy?
- Why was Riemannian Adagrad consistently worse, despite its theoretical guarantees and its motivation from sparse word updates?

## 📝 Notes on reading

- Version read: arXiv 1810.00760v2 (18 Feb 2019), typeset as the ICLR 2019 conference paper; the packet's identifier is the arXiv DOI.
- Figures 2 and 3 (training loss, train MAP and validation MAP curves for exponential-map and retraction variants) are not in the extracted text; results were claimed only from the Results paragraph on p. 8.
- The Results paragraph refers to "Tab. 2", but no table appears in the paper; it presumably means Figure 2.
- Equations (theorem bounds, proof steps, closed-form Poincaré operations) are garbled in the extraction; only their verbal statements were claimed.
- The text says "the notion of convexity in Theorem 5 got replaced by ... geodesic convexity in Theorem 1"; Theorem 5 is the Euclidean Amsgrad result in appendix C.
- The Figure 1a caption calls the algorithm "Algorithm 1a" elsewhere; naming is inconsistent but refers to the same RAMSGRAD pseudocode.
- Lemma 4 is stated with a hat on v, while its proof uses v without the hat.

## Suggested new concepts

- Riemannian optimization — the general family (RSGD, retractions, geodesic convexity) that this paper extends and that recurs across hyperbolic embedding work.
- Adaptive gradient methods — Adagrad, Adam, Amsgrad and their convergence issues form a shared background for many optimizer papers.
- Hyperbolic embeddings — Poincaré and Lorentz embeddings of hierarchies are the motivating application and link several related papers.
- Product manifolds — per-manifold adaptivity relies on the product structure, a design pattern reused in mixed-curvature representation learning.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Adam/AMSGrad riemannianos en productos de variedades (A.5).

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
