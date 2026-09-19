---
aliases: []
type: "source"
title: "Kernelized Wasserstein Natural Gradient"
citekey: "Arbel2019kernelized"
doi: "10.48550/arXiv.1910.09652"
arxiv: "1910.09652"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1910.09652"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Michael Arbel", "Arthur Gretton", "Wuchen Li", "Guido Montufar"]
sha256: ["9cb96e081b7df04b8dbfeb25992b7d739cd4cbae7bc01f3f858be673df6cf478"]
pdf: "Content/Papers/Arbel2019kernelized.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Arbel2019kernelized.pdf]]

> [!abstract] One-sentence summary
> The paper estimates the Wasserstein natural gradient with a kernel (RKHS) restriction of its dual formulation and Nyström projections, giving a cheap, consistent estimator that stays robust to ill-conditioned parametrizations when training ResNets on Cifar10 and Cifar100.

## Abstract

Many machine learning problems can be expressed as the optimization of some cost functional over a parametric family of probability distributions. It is often beneficial to solve such optimization problems using natural gradient methods. These methods are invariant to the parametrization of the family, and thus can yield more effective optimization. Unfortunately, computing the natural gradient is challenging as it requires inverting a high dimensional matrix at each iteration. We propose a general framework to approximate the natural gradient for the Wasserstein metric, by leveraging a dual formulation of the metric restricted to a Reproducing Kernel Hilbert Space. Our approach leads to an estimator for gradient direction that can trade-off accuracy and computational cost, with theoretical guarantees. We verify its accuracy on simple examples, and show the advantage of using such an estimator in classification tasks on Cifar10 and Cifar100 empirically. (arXiv)

## 🧠 Key ideas (atomic)

- Applying [[Natural gradient descent|natural gradient methods]] is challenging in practice because each parameter update requires inverting the metric tensor of the model. (Arbel et al., 2019) `ev:asserted` p. 1 ^arbel2019kernelized-001
- Inverting the metric tensor becomes infeasible for current deep learning models, which typically have millions of parameters, according to the authors. (Arbel et al., 2019) `ev:asserted` p. 1 ^arbel2019kernelized-002
- Existing efficient natural gradient algorithms often exploit a particular structure of the parametric family or a low rank decomposition of the information matrix. (Arbel et al., 2019) `ev:cited` p. 2 ^arbel2019kernelized-003
- Li et al. (2019) estimated the metric through a dual formulation inside a proximal method, which adds an extra optimization problem per update. (Arbel et al., 2019) `ev:cited` p. 2 ^arbel2019kernelized-004
- The authors use the dual formulation of the metric to obtain a closed form expression of the natural gradient as a convex functional optimization solution. (Arbel et al., 2019) `ev:asserted` p. 2 ^arbel2019kernelized-005
- The paper focuses on the Wasserstein metric because it remains well defined even when the model does not admit a density. (Arbel et al., 2019) `ev:asserted` p. 2 ^arbel2019kernelized-006
- Proposition 1 states that the continuous-time natural gradient flow is invariant to invertible smooth re-parametrizations of the model. (Arbel et al., 2019) `ev:computed` p. 3 ^arbel2019kernelized-007
- The authors argue that an ill-conditioned parametrization has little effect on the optimization when the natural gradient update rule is used. (Arbel et al., 2019) `ev:asserted` p. 3 ^arbel2019kernelized-008
- Following Li and Montufar and Chen and Li, the Wasserstein information matrix is obtained from the Wasserstein-2 metric tensor. (Arbel et al., 2019) `ev:cited` p. 3 ^arbel2019kernelized-009
- Defining the Wasserstein information matrix through distributional derivatives allows the [[Wasserstein natural gradient]] to be defined when the model has no density. (Arbel et al., 2019) `ev:asserted` p. 4 ^arbel2019kernelized-010
- Directly applying the natural gradient update becomes impractical in high dimension because it requires storing and inverting the information matrix. (Arbel et al., 2019) `ev:asserted` p. 4 ^arbel2019kernelized-011
- Proposition 3 gives a dual formulation of the [[Wasserstein natural gradient]] for implicit models as a saddle-point problem over smooth test functions. (Arbel et al., 2019) `ev:computed` p. 5 ^arbel2019kernelized-012
- Unlike the Fisher dual form, the Wasserstein dual form does not require the test functions to have zero mean under the model. (Arbel et al., 2019) `ev:computed` p. 5 ^arbel2019kernelized-013
- The Fisher dual expression can be infinite for implicit models whose distributions do not admit a density. (Arbel et al., 2019) `ev:computed` p. 5 ^arbel2019kernelized-014
- The kernelized Wasserstein natural gradient restricts the dual problem to functions in a Reproducing Kernel Hilbert Space and adds regularization terms. (Arbel et al., 2019) `ev:reported` p. 5 ^arbel2019kernelized-015
- Proposition 4 expresses the kernelized natural gradient through the unique solution of a quadratic functional optimization, avoiding explicit inversion of the metric. (Arbel et al., 2019) `ev:computed` p. 6 ^arbel2019kernelized-016
- The exact empirical minimizer requires solving a system of size Nd×Nd, which can be prohibitive when both N and d are large. (Arbel et al., 2019) `ev:asserted` p. 6 ^arbel2019kernelized-017
- The authors propose a Nyström subspace that randomly samples one partial derivative component of the kernel per basis point. (Arbel et al., 2019) `ev:reported` p. 6 ^arbel2019kernelized-018
- Using all kernel partial derivatives per basis point, as in Sutherland et al., keeps a cubic dependence on the dimension d. (Arbel et al., 2019) `ev:cited` p. 6 ^arbel2019kernelized-019
- Proposition 5 gives a closed form for the estimator, which the authors describe as a low rank approximation of the natural gradient. (Arbel et al., 2019) `ev:computed` p. 7 ^arbel2019kernelized-020
- The authors state the estimator can be applied as a plug-in estimator for any parametric family obtained as an implicit model. (Arbel et al., 2019) `ev:asserted` p. 7 ^arbel2019kernelized-021
- When λ=0, an SVD of CC⊤ yields a numerically stable form of the estimator that falls among ridgeless estimators. (Arbel et al., 2019) `ev:computed` p. 7 ^arbel2019kernelized-022
- Instead of the identity, the damping matrix is set scale-sensitively from column norms, since the identity breaks the natural gradient's self-rescaling. (Arbel et al., 2019) `ev:asserted` p. 7 ^arbel2019kernelized-023
- With limited mini-batch samples, larger ϵ values may be needed to prevent KWNG over-estimating step sizes in low curvature directions. (Arbel et al., 2019) `ev:asserted` p. 7 ^arbel2019kernelized-024
- ϵ is adjusted dynamically during training with a variant of the Levenberg-Marquardt heuristic following Martens and Sutskever. (Arbel et al., 2019) `ev:reported` p. 7 ^arbel2019kernelized-025
- The overall computational cost of the estimator is O(dNM2+qM2+M3), controlled by the number of basis points M. (Arbel et al., 2019) `ev:computed` p. 7 ^arbel2019kernelized-026
- In practice, the authors state that the number of basis points M can be chosen small, with M ≤20. (Arbel et al., 2019) `ev:asserted` p. 7 ^arbel2019kernelized-027
- In typical deep models most of the estimator's cost comes from computing T, which needs M backward passes through the model. (Arbel et al., 2019) `ev:asserted` p. 7 ^arbel2019kernelized-028
- The authors report that either a gaussian kernel or a rational quadratic kernel works well in practice for the estimator. (Arbel et al., 2019) `ev:asserted` p. 8 ^arbel2019kernelized-029
- Kernel bandwidth is set heuristically by scaling the average square distance between samples and basis points by a fixed factor. (Arbel et al., 2019) `ev:reported` p. 8 ^arbel2019kernelized-030
- Theorem 7 bounds the estimator's squared error with a rate in N depending on a difficulty parameter c, in the misspecified case. (Arbel et al., 2019) `ev:computed` p. 8 ^arbel2019kernelized-031
- In the best case where c=0, the rate matches the well-specified case with the worst smoothness parameter α=0. (Arbel et al., 2019) `ev:computed` p. 8 ^arbel2019kernelized-032
- As c tends to infinity, M must reach order dNlog(N), where the Nyström approximation loses its computational advantage. (Arbel et al., 2019) `ev:computed` p. 8 ^arbel2019kernelized-033
- The authors leave the theoretical analysis of the estimator in the unregularized case λ=0 for future work. (Arbel et al., 2019) `ev:asserted` p. 8 ^arbel2019kernelized-034
- Accuracy was assessed on multivariate normal, multivariate log-normal and hyper-sphere uniform models, whose [[Wasserstein natural gradient]] has closed form. (Arbel et al., 2019) `ev:reported` p. 8 ^arbel2019kernelized-035
- The uniform distribution on hyper-spheres does not admit a density, so the Fisher natural gradient is not defined for it. (Arbel et al., 2019) `ev:asserted` p. 8 ^arbel2019kernelized-036
- On the hyper-sphere model, the relative error of KWNG decreased as the sample size N increased, averaged over 100 runs. (Arbel et al., 2019) `ev:measured` p. 9 ^arbel2019kernelized-037
- The relative error showed a threshold in basis points M beyond which increasing M no longer decreased the error. (Arbel et al., 2019) `ev:measured` p. 9 ^arbel2019kernelized-038
- This threshold in the number of basis points increased with the dimension d of the sample space. (Arbel et al., 2019) `ev:measured` p. 9 ^arbel2019kernelized-039
- The authors state that setting M to the ceiling of d times root N seems to be a good heuristic. (Arbel et al., 2019) `ev:asserted` p. 9 ^arbel2019kernelized-040
- Similar relative error behaviour held for the normal and log-normal models, as shown in Figure 4 of the appendix. (Arbel et al., 2019) `ev:measured` p. 9 ^arbel2019kernelized-041
- The authors report that the estimator is robust to a wide choice of the kernel bandwidth σ. (Arbel et al., 2019) `ev:measured` p. 9 ^arbel2019kernelized-042
- On a multivariate normal family, [[Wasserstein natural gradient|exact WNG]] allowed larger step sizes than Euclidean gradient, giving faster convergence of the loss. (Arbel et al., 2019) `ev:measured` p. 9 ^arbel2019kernelized-043
- In that trajectory comparison, the optimal step size was 0.1 for KWNG and WNG and 0.0001 for Euclidean gradient. (Arbel et al., 2019) `ev:reported` p. 9 ^arbel2019kernelized-044
- KWNG used N = 128 samples and M = 100 basis points in the trajectory comparison, with sample dimension d = 10. (Arbel et al., 2019) `ev:reported` p. 9 ^arbel2019kernelized-045
- The dynamics of [[Wasserstein natural gradient|exact WNG]] seem to be well approximated by KWNG along the two main PCA directions of the trajectory. (Arbel et al., 2019) `ev:measured` p. 9 ^arbel2019kernelized-046
- For Cifar classification, input images are treated as latent variables and network output logits as samples from the model distribution. (Arbel et al., 2019) `ev:reported` p. 10 ^arbel2019kernelized-047
- Conditioning is controlled by a fixed invertible diagonal matrix applied to the logits, which is the identity in the well-conditioned case. (Arbel et al., 2019) `ev:reported` p. 10 ^arbel2019kernelized-048
- KWNG was compared with plain SGD, SGD with momentum, SGD with momentum and weight decay, Adam, KFAC and eKFAC. (Arbel et al., 2019) `ev:reported` p. 10 ^arbel2019kernelized-049
- The authors state that gradient clipping by norm was crucial for a stable optimization using KWNG in all experiments. (Arbel et al., 2019) `ev:reported` p. 10 ^arbel2019kernelized-050
- In the well-conditioned case, all methods achieved a similar test accuracy on both Cifar10 and Cifar100. (Arbel et al., 2019) `ev:measured` p. 10 ^arbel2019kernelized-051
- In the ill-conditioned case, methods based on the Euclidean gradient seem to suffer a drastic drop in performance. (Arbel et al., 2019) `ev:measured` p. 10 ^arbel2019kernelized-052
- On Cifar10, KWNG achieved a test accuracy in the ill-conditioned case similar to that of the well-conditioned case. (Arbel et al., 2019) `ev:measured` p. 10 ^arbel2019kernelized-053
- Increasing the number of basis points M gave KWNG a speed-up in convergence measured in number of iterations. (Arbel et al., 2019) `ev:measured` p. 10 ^arbel2019kernelized-054
- The authors report that the time cost on Cifar10 is also in favor of KWNG compared with the other optimizers. (Arbel et al., 2019) `ev:measured` p. 10 ^arbel2019kernelized-055
- On Cifar100, KWNG was also less affected by the ill-conditioning, albeit to a lower extent than on Cifar10. (Arbel et al., 2019) `ev:measured` p. 10 ^arbel2019kernelized-056
- The authors attribute the harder estimation of KWNG on Cifar100 to its larger number of classes. (Arbel et al., 2019) `ev:asserted` p. 10 ^arbel2019kernelized-057
- On Cifar100, increasing the batch size can substantially improve the training accuracy obtained with KWNG, the authors report. (Arbel et al., 2019) `ev:measured` p. 10 ^arbel2019kernelized-058
- Combining KWNG with momentum led to an improved performance in the well-conditioned classification case, according to the authors. (Arbel et al., 2019) `ev:measured` p. 10 ^arbel2019kernelized-059
- [[Kronecker-factored approximate curvature|KFAC]] also seems to suffer a drop in performance in the ill-conditioned case, which might result from its isotropic damping term. (Arbel et al., 2019) `ev:measured` p. 10 ^arbel2019kernelized-060
- The authors also observe a drop in KWNG performance when a different choice of damping term is used. (Arbel et al., 2019) `ev:measured` p. 10 ^arbel2019kernelized-061
- Using only a diagonal pre-conditioning of the gradient does not match the performance of KWNG, according to the authors. (Arbel et al., 2019) `ev:measured` p. 10 ^arbel2019kernelized-062
- The Cifar network is a residual network with one convolutional layer, 8 residual blocks and a final fully connected layer. (Arbel et al., 2019) `ev:reported` p. 29 ^arbel2019kernelized-063
- All methods in the classification experiments used a batch size of 128, with the step size selected per method. (Arbel et al., 2019) `ev:reported` p. 29 ^arbel2019kernelized-064
- For KWNG in the classification experiments, the authors set M =5 and λ=0, with ϵ adjusted adaptively. (Arbel et al., 2019) `ev:reported` p. 29 ^arbel2019kernelized-065
- The damping ϵ is updated every 5 optimizer iterations from a reduction ratio, using a decay constant ω=0.85. (Arbel et al., 2019) `ev:reported` p. 30 ^arbel2019kernelized-066
- For Dirac distribution models, the Negative Sobolev distance is infinite for any perturbation size, according to the authors' derivation. (Arbel et al., 2019) `ev:computed` p. 18 ^arbel2019kernelized-067
- For the same Dirac model, the Wasserstein information metric has a finite closed form equal to half the squared norm. (Arbel et al., 2019) `ev:computed` p. 18 ^arbel2019kernelized-068

## 🎯 Contributions

## 📖 Glossary

- **Natural gradient** — Gradient preconditioned by an information matrix, invariant to model re-parametrization.
- **Wasserstein information matrix (WIM)** — Pull-back of the Wasserstein-2 metric tensor onto the parameter space.
- **Fisher information matrix** — Pull-back of the Fisher-Rao metric; requires model distributions with positive densities.
- **Implicit model** — Distribution defined as push-forward of a latent distribution by a parametric map.
- **Distributional gradient** — Derivative of a model with respect to parameters, defined through smooth test functions.
- **KWNG** — Kernelized Wasserstein natural gradient: dual problem restricted to an RKHS, estimated with Nyström projections.
- **Nyström subspace** — Finite-dimensional span of kernel derivative functions at a few sampled basis points.
- **Damping term D(θ)** — Diagonal regularizer on parameter change; its choice affects scale-sensitivity of the update.
- **Negative Sobolev distance** — Linearization of the Wasserstein distance; can be infinite for singular distributions.

## ❓ Open questions

- What convergence guarantees hold for the unregularized estimator with λ=0, which the experiments actually use?
- Can the estimator stay accurate for problems with many output classes, where Cifar100 results were weaker?
- How does KWNG compare in accuracy and wall-clock time on larger architectures and datasets beyond Cifar?
- Can KWNG be run stably without gradient clipping, which the authors found crucial?
- Does a similar kernel estimator of the Fisher-Rao natural gradient perform comparably on models with densities?

## 📝 Notes on reading

The cached text is arXiv v4 (13 Feb 2020), marked as the ICLR 2020 conference version; the packet identifier is the arXiv record.

Figures 1-7 are plots whose curves could only be described; the Cifar results in Figure 3 carry no numerical accuracy values in the text, so claims about them are qualitative. The Figure 3 caption says results are averaged over 5 independent runs except for KFAC and eKFAC.

Several numbers were garbled by extraction and not claimed: the ill-conditioned condition number (printed as 107, likely 10^7), the regularization ϵ values (printed as 10−10 and 10−5), the Theorem 7 rate (printed with N and 4+c split across lines), the ceiling in the rule for M, and the weight decay value (5×10−4).

The body text on p. 10 discusses Cifar10 while Figure 3 also shows Cifar100; the Section 3 introduction numbers Sections 3.3 and 3.4 in the reverse order of the actual layout. Appendix C (pp. 18-28) holds proofs and was read only for the stated results.

## Suggested new concepts

- Wasserstein natural gradient — central object that several optimal-transport optimization papers build on.
- Nyström approximation — generic kernel acceleration reused across score estimation and natural gradient estimation.
- Parametrization invariance — the motivating property of natural gradient methods for ill-conditioned models.
- Implicit generative models — models without densities where Wasserstein geometry remains defined but Fisher geometry does not.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Estimador escalable del gradiente natural de Wasserstein (B.8).
