---
aliases: []
type: "source"
title: "Shampoo: Preconditioned Stochastic Tensor Optimization"
citekey: "Gupta2018shampoo"
doi: "10.48550/arXiv.1802.09568"
arxiv: "1802.09568"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1802.09568"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Vineet Gupta", "Tomer Koren", "Yoram Singer"]
sha256: ["dedd4fdb7f591342eb3bcee119d7d51f3b751d7070afc0b1ba59560ef2594d64"]
pdf: "Content/Papers/Gupta2018shampoo.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Gupta2018shampoo.pdf]]

> [!abstract] One-sentence summary
> Shampoo keeps one full but moderately sized preconditioner per tensor dimension, giving an O(sqrt T) regret guarantee in the convex setting and per-step runtime close to SGD, AdaGrad and Adam on deep networks.

## Abstract

Preconditioned gradient methods are among the most general and powerful tools in optimization. However, preconditioning requires storing and manipulating prohibitively large matrices. We describe and analyze a new structure-aware preconditioning algorithm, called Shampoo, for stochastic optimization over tensor spaces. Shampoo maintains a set of preconditioning matrices, each of which operates on a single dimension, contracting over the remaining dimensions. We establish convergence guarantees in the stochastic convex setting, the proof of which builds upon matrix trace inequalities. Our experiments with state-of-the-art deep learning models show that Shampoo is capable of converging considerably faster than commonly used optimizers. Although it involves a more complex update rule, Shampoo's runtime per step is comparable to that of simple gradient methods such as SGD, AdaGrad, and Adam. (arXiv)

## 🧠 Key ideas (atomic)

- Over the last decade, stochastic first-order optimization methods have emerged as the canonical tools for training large-scale machine learning models. (Gupta et al., 2018) `ev:asserted` p. 1 ^gupta2018shampoo-001
- Preconditioning methods maintain a matrix, termed a preconditioner, which transforms the gradient vector before it is used to take a step. (Gupta et al., 2018) `ev:asserted` p. 1 ^gupta2018shampoo-002
- AdaGrad is a preconditioned online algorithm that uses the covariance matrix of the accumulated gradients to form its preconditioner. (Gupta et al., 2018) `ev:cited` p. 1 ^gupta2018shampoo-003
- The authors state that the dimensionality of typical machine learning problems prohibits out-of-the-box use of full-matrix preconditioning. (Gupta et al., 2018) `ev:asserted` p. 1 ^gupta2018shampoo-004
- Sketched or estimated preconditioner variants are seldom practical at large scale, as a fine approximation often demands super-linear memory and computation. (Gupta et al., 2018) `ev:cited` p. 1 ^gupta2018shampoo-005
- Shampoo retains the tensor structure of the gradient and maintains [[Kronecker-factored preconditioning|a separate preconditioner matrix for each of the gradient's dimensions]]. (Gupta et al., 2018) `ev:asserted` p. 2 ^gupta2018shampoo-006
- Shampoo updates its set of preconditioners online with the second-order statistics of the accumulated gradients, similarly to AdaGrad. (Gupta et al., 2018) `ev:asserted` p. 2 ^gupta2018shampoo-007
- Each individual Shampoo preconditioner is a full, yet moderately-sized, matrix that can be effectively manipulated in large scale learning problems. (Gupta et al., 2018) `ev:asserted` p. 2 ^gupta2018shampoo-008
- The authors analyze Shampoo in the broader framework of online convex optimization, so its convergence guarantee applies more generally than stochastic optimization. (Gupta et al., 2018) `ev:asserted` p. 2 ^gupta2018shampoo-009
- The analysis combines well-studied online optimization tools with off-the-beaten-path inequalities concerning geometric means of matrices. (Gupta et al., 2018) `ev:asserted` p. 2 ^gupta2018shampoo-010
- Shampoo was implemented in its general tensor form in Python as a new optimizer in the TensorFlow framework. (Gupta et al., 2018) `ev:reported` p. 2 ^gupta2018shampoo-011
- The authors call Shampoo extremely simple to implement, as most of its computations reduce to standard tensor operations in TensorFlow. (Gupta et al., 2018) `ev:asserted` p. 2 ^gupta2018shampoo-012
- Unlike recent methods that must know the model structure, Shampoo only needs to be informed of the tensors involved and their sizes. (Gupta et al., 2018) `ev:asserted` p. 2 ^gupta2018shampoo-013
- In experiments with state-of-the-art deep learning models, Shampoo is capable of converging considerably faster than commonly used optimizers. (Gupta et al., 2018) `ev:measured` p. 2 ^gupta2018shampoo-014
- A structure-oblivious full-matrix scheme would flatten the m by n parameter matrix and employ preconditioning matrices of size mn by mn. (Gupta et al., 2018) `ev:asserted` p. 3 ^gupta2018shampoo-015
- In the matrix case, Shampoo instead maintains [[Kronecker-factored preconditioning|smaller left and right matrices]] containing second-moment information of the accumulated gradients. (Gupta et al., 2018) `ev:asserted` p. 3 ^gupta2018shampoo-016
- Shampoo's memory in the matrix case grows with the sum of the squared dimensions rather than with the product of their squares. (Gupta et al., 2018) `ev:computed` p. 3 ^gupta2018shampoo-017
- Constructing [[Kronecker-factored preconditioning|the left and right preconditioners]] costs computation cubic in each dimension separately, substantially lower than full-matrix methods cubic in their product. (Gupta et al., 2018) `ev:computed` p. 3 ^gupta2018shampoo-018
- The one-quarter exponent arises from the analysis and induces an overall step-size decay rate of order one over the square root of t. (Gupta et al., 2018) `ev:asserted` p. 3 ^gupta2018shampoo-019
- After flattening, the matrix Shampoo update is equivalent to a gradient step preconditioned by [[Kronecker-factored preconditioning|the Kronecker product of the two root matrices]]. (Gupta et al., 2018) `ev:computed` p. 3 ^gupta2018shampoo-020
- The full-matrix version of AdaGrad is rarely used in practice due to the prohibitive memory and runtime of maintaining a full preconditioner. (Gupta et al., 2018) `ev:cited` p. 3 ^gupta2018shampoo-021
- The authors view Shampoo as a practical, provable way to approximately and implicitly use the full AdaGrad preconditioner without diagonal matrices. (Gupta et al., 2018) `ev:asserted` p. 3 ^gupta2018shampoo-022
- K-FAC approximates the Fisher matrix of each network layer by [[Kronecker-factored preconditioning|a Kronecker product of two smaller matrices]], relying on independence assumptions. (Gupta et al., 2018) `ev:cited` p. 3 ^gupta2018shampoo-023
- Unlike K-FAC, Shampoo applies in a general stochastic or online optimization setting and comes with convergence guarantees in the convex case. (Gupta et al., 2018) `ev:asserted` p. 4 ^gupta2018shampoo-024
- The authors argue Shampoo is much easier to implement than K-FAC, as it need not be tailored to the particular model or architecture. (Gupta et al., 2018) `ev:asserted` p. 4 ^gupta2018shampoo-025
- Any regret minimizing online algorithm can be converted to a stochastic optimization algorithm using an online-to-batch conversion technique. (Gupta et al., 2018) `ev:cited` p. 4 ^gupta2018shampoo-026
- Theorem 7 bounds the regret of matrix Shampoo, for gradients of rank at most r, through traces of both preconditioners' fourth roots. (Gupta et al., 2018) `ev:computed` p. 6 ^gupta2018shampoo-027
- Under mild conditions the matrix-case regret bound scales as the square root of T, which the authors call the best possible. (Gupta et al., 2018) `ev:computed` p. 7 ^gupta2018shampoo-028
- The authors omitted a projection step from Algorithm 1, as it becomes computationally expensive at large scale, in favor of a slightly looser bound. (Gupta et al., 2018) `ev:asserted` p. 7 ^gupta2018shampoo-029
- The lemma shows that the small eigenvalues of the full-matrix preconditioner do not vanish as a result of the implicit approximation. (Gupta et al., 2018) `ev:computed` p. 7 ^gupta2018shampoo-030
- Theorem 10 extends the regret guarantee to order-k tensors, and under standard assumptions the overall regret bound is of order root T. (Gupta et al., 2018) `ev:computed` p. 11 ^gupta2018shampoo-031
- Shampoo's tensor operations can be implemented using tensor contraction, a standard function in libraries such as NumPy and TensorFlow. (Gupta et al., 2018) `ev:asserted` p. 11 ^gupta2018shampoo-032
- Matrix powers were computed simply by constructing a singular value decomposition and then taking the powers of the singular values. (Gupta et al., 2018) `ev:reported` p. 12 ^gupta2018shampoo-033
- The optimizer applies the Shampoo update to each model tensor independently, which amounts to a block-diagonal preconditioner with one block per tensor. (Gupta et al., 2018) `ev:reported` p. 12 ^gupta2018shampoo-034
- Only intra-tensor correlations are captured by the implementation, while correlations between parameters in different tensors are ignored entirely. (Gupta et al., 2018) `ev:asserted` p. 12 ^gupta2018shampoo-035
- A diagonal Shampoo variant activates automatically for any tensor dimension considered too large to store its preconditioner or compute its SVD. (Gupta et al., 2018) `ev:reported` p. 12 ^gupta2018shampoo-036
- The experiments used a threshold of around 1200 per dimension to trigger the diagonal version, with no apparent sacrifice in performance. (Gupta et al., 2018) `ev:measured` p. 12 ^gupta2018shampoo-037
- The authors state that they plan to implement Shampoo in the PyTorch framework in the near future. (Gupta et al., 2018) `ev:asserted` p. 12 ^gupta2018shampoo-038
- Experiments covered image classification on CIFAR-10/100 and statistical language modeling on LM1B, using standard deep neural-network models. (Gupta et al., 2018) `ev:reported` p. 12 ^gupta2018shampoo-039
- In each experiment the authors relied on existing training code and merely replaced the TensorFlow optimizer without making other code changes. (Gupta et al., 2018) `ev:reported` p. 13 ^gupta2018shampoo-040
- All experiments worked with a mini-batch of size 128, whose averaged gradient served as the gradient in each Shampoo iteration. (Gupta et al., 2018) `ev:reported` p. 13 ^gupta2018shampoo-041
- The preconditioners were updated once per batch using the averaged gradient rather than with gradients over individual examples. (Gupta et al., 2018) `ev:reported` p. 13 ^gupta2018shampoo-042
- As a heuristic, the roots of the preconditioner matrices were recomputed once in every 20–100 steps to improve amortized runtime. (Gupta et al., 2018) `ev:reported` p. 13 ^gupta2018shampoo-043
- The authors report that the delayed preconditioner update had almost no impact on accuracy in their experiments. (Gupta et al., 2018) `ev:measured` p. 13 ^gupta2018shampoo-044
- Momentum was incorporated into the Shampoo gradient step as a running average of the gradients with a fixed setting of α = 0.9. (Gupta et al., 2018) `ev:reported` p. 13 ^gupta2018shampoo-045
- Incorporating momentum slightly improved the convergence of Shampoo, as is the case with many other first-order stochastic methods. (Gupta et al., 2018) `ev:measured` p. 13 ^gupta2018shampoo-046
- Runtime was measured as the average number of steps per second, with batches of size 128, on a Tesla K40 GPU. (Gupta et al., 2018) `ev:reported` p. 13 ^gupta2018shampoo-047
- Although Shampoo performs significantly more computation per step than SGD, AdaGrad and Adam, its actual runtime in practice is not much worse. (Gupta et al., 2018) `ev:measured` p. 13 ^gupta2018shampoo-048
- On CIFAR10 with ResNet-32, Shampoo ran 2.151 steps per second, compared with 2.184 for both SGD and Adam. (Gupta et al., 2018) `ev:measured` p. 13 ^gupta2018shampoo-049
- On CIFAR10 with the Inception network, Shampoo ran 3.506 steps per second, against 3.638 for SGD and 3.682 for AdaGrad. (Gupta et al., 2018) `ev:measured` p. 13 ^gupta2018shampoo-050
- On CIFAR100 with ResNet-55, Shampoo ran 1.249 steps per second, faster than SGD at 1.210 and Adam at 1.203. (Gupta et al., 2018) `ev:measured` p. 13 ^gupta2018shampoo-051
- On LM1B with the Attention model, Shampoo ran 3.509 steps per second, compared with 4.871 for Adam and 4.919 for SGD. (Gupta et al., 2018) `ev:measured` p. 13 ^gupta2018shampoo-052
- The CIFAR-10 residual network had 32 layers and 2.4M parameters, and it is capable of reaching a 5% test error rate. (Gupta et al., 2018) `ev:reported` p. 14 ^gupta2018shampoo-053
- The 20-layer small inception network trained on CIFAR-10 had 1.65M trainable parameters and can reach a 7.5% test error rate. (Gupta et al., 2018) `ev:reported` p. 14 ^gupta2018shampoo-054
- CIFAR-100 used a 55-layer residual network with 13.5M trainable parameters, all convolutional, which reached an error rate of 24% on test data. (Gupta et al., 2018) `ev:reported` p. 14 ^gupta2018shampoo-055
- The CIFAR-100 residual architecture used no batchnorm or dropout, and its largest layer had dimension 256, 3, 3, 256. (Gupta et al., 2018) `ev:reported` p. 14 ^gupta2018shampoo-056
- LM1B used an Attention model with 9.8M trainable parameters, whose largest fully connected tensor has dimension 2000 by 256. (Gupta et al., 2018) `ev:reported` p. 14 ^gupta2018shampoo-057
- On LM1B, Shampoo simply used the default learning rate of 1.0, while the other algorithms were run with various learning rates. (Gupta et al., 2018) `ev:reported` p. 14 ^gupta2018shampoo-058
- Diagonal Shampoo merely stores the diagonal elements of both preconditioners, so it needs memory linear in the sum of the two dimensions. (Gupta et al., 2018) `ev:computed` p. 16 ^gupta2018shampoo-059
- Each diagonal Shampoo update step could be implemented in time linear in the number of parameters of the matrix. (Gupta et al., 2018) `ev:computed` p. 16 ^gupta2018shampoo-060
- In the general tensor case, the choice between full and diagonal preconditioning can be made independently for each of the dimensions. (Gupta et al., 2018) `ev:asserted` p. 16 ^gupta2018shampoo-061
- Theorem 13 bounds the regret of diagonal Shampoo using the entry-wise infinity-norm distance to the comparator in place of the Frobenius distance. (Gupta et al., 2018) `ev:computed` p. 17 ^gupta2018shampoo-062

## 🎯 Contributions

## 📖 Glossary

- **Preconditioner** — Matrix that transforms the gradient before the optimizer takes a step.
- **Full-matrix AdaGrad** — AdaGrad using the full covariance of accumulated gradients as preconditioner.
- **Kronecker product** — Block matrix built by multiplying every entry of one matrix by another.
- **Matricization** — Reshaping a tensor into a matrix by stacking vectorized slices along one dimension.
- **Tensor contraction** — Summing a tensor product over all indices except one chosen dimension.
- **Regret** — Cumulative loss of an online learner minus that of the best fixed point.
- **Online convex optimization** — Framework where a learner faces a sequence of convex losses over rounds.
- **Online-to-batch conversion** — Turning a regret bound into a stochastic convergence rate of order regret over T.
- **Operator monotone** — Function preserving the PSD ordering between matrices.
- **Diagonal Shampoo** — Shampoo variant keeping only diagonal preconditioners for dimensions too large to store.

## ❓ Open questions

- How much does ignoring correlations between parameters in different tensors cost compared with a cross-tensor preconditioner?
- Does the convergence speed-up seen in training loss translate into better test error or generalization?
- Can the regret guarantee be extended to non-convex objectives such as deep networks, where Shampoo is actually used?
- How sensitive is Shampoo to the preconditioner root recomputation interval, the epsilon initialization and the diagonal-switch threshold?
- Why is Shampoo's step rate on LM1B clearly lower than the other optimizers while CIFAR step rates are close?
- How would Shampoo behave with larger batch sizes, distributed training or accelerators other than a Tesla K40 GPU?

## 📝 Notes on reading

Version read: arXiv v2 (1802.09568v2, 2 Mar 2018), which matches the packet identifier.

Figures 2–4 are only described, not claimed: Fig. 2 shows training loss over epochs for the ResNet-32 and Inception networks on CIFAR-10 for AdaGrad, Adam, Shampoo and Momentum; Fig. 3 shows training loss for the 55-layer ResNet on CIFAR-100 without batchnorm; Fig. 4 shows test log-perplexity over steps for the Attention model on LM1B. The claim of faster convergence rests on these curves; the paper gives no numeric convergence comparison (e.g. epochs to a target loss) in the text.

Most equations, the regret bounds of Theorems 7, 10 and 13, and the algorithm pseudocode are garbled in the extraction (exponents and operators rendered as stray glyphs); claims about them are paraphrased without the formulas.

Inconsistency: the abstract and p. 13 say Shampoo's step time is comparable to or only slightly slower than the other algorithms, but Table 1 shows LM1B at 3.509 steps per second for Shampoo versus 4.871–4.919 for the others, a notably larger gap than on CIFAR. Theorem 7 also sums the right preconditioner from t = 0 while the left one sums from t = 1, likely a typo. Test error rates quoted for the CIFAR networks are what the architectures are capable of, not results reported per optimizer.

## Suggested new concepts

- Kronecker-factored preconditioning — shared idea behind Shampoo and K-FAC, worth a note comparing the two approximations.
- Full-matrix adaptive regularization — AdaGrad-style full preconditioning that Shampoo approximates implicitly.
- Online-to-batch conversion — the bridge from regret bounds to stochastic convergence used across adaptive optimizer analyses.
- Second-order optimizers for deep learning — umbrella concept for preconditioned methods that trade compute for faster convergence.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Precondicionador de Kronecker por modos (B.4).

<!-- ingest-checker dropped 3 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
