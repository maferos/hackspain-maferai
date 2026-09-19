---
aliases: []
type: "source"
title: "Pathological spectra of the Fisher information metric and its variants in deep neural networks"
citekey: "Karakida2019pathological"
doi: "10.48550/arXiv.1910.05992"
arxiv: "1910.05992"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1910.05992"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Ryo Karakida", "Shotaro Akaho", "Shun-ichi Amari"]
sha256: ["4ae6aa8e8bbf77a89e67745778b20c93388359166da6bf7458fe9a99cbeac1ab"]
pdf: "Content/Papers/Karakida2019pathological.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[Karakida2019pathological.pdf]]

> [!abstract] One-sentence summary
> Using mean-field order parameters for wide random networks, the paper shows that the regression and softmax FIMs, their diagonal blocks, the NTK and an input/feature-space metric all have pathological eigenvalue spectra with a few large outliers and a near-zero bulk, which bears on learning rates, natural gradient and NTK conditioning.

## Abstract

The Fisher information matrix (FIM) plays an essential role in statistics and machine learning as a Riemannian metric tensor or a component of the Hessian matrix of loss functions. Focusing on the FIM and its variants in deep neural networks (DNNs), we reveal their characteristic scale dependence on the network width, depth and sample size when the network has random weights and is sufficiently wide. This study covers two widely-used FIMs for regression with linear output and for classification with softmax output. Both FIMs asymptotically show pathological eigenvalue spectra in the sense that a small number of eigenvalues become large outliers depending the width or sample size while the others are much smaller. It implies that the local shape of the parameter space or loss landscape is very sharp in a few specific directions while almost flat in the other directions. In particular, the softmax output disperses the outliers and makes a tail of the eigenvalue density spread from the bulk. We also show that pathological spectra appear in other variants of FIMs: one is the neural tangent kernel; another is a metric for the input signal and feature space that arises from feedforward signal propagation. Thus, we provide a unified perspective on the FIM and its variants that will lead to more quantitative understanding of learning in large-scale DNNs. (arXiv)

## 🧠 Key ideas (atomic)

- Earlier numerical experiments empirically confirmed that the FIM's eigenvalue spectra are highly distorted, with most eigenvalues lying close to zero. (Karakida et al., 2019) `ev:cited` p. 1 ^karakida2019pathological-001
- A prior study by the same authors showed that the MSE-loss FIM spectrum becomes pathologically distorted in sufficiently wide randomly initialized fully-connected networks. (Karakida et al., 2019) `ev:cited` p. 2 ^karakida2019pathological-002
- This paper extends a previous order-parameter framework to show that several FIM variants exhibit pathological eigenvalue spectra in wide networks. (Karakida et al., 2019) `ev:asserted` p. 2 ^karakida2019pathological-003
- According to the authors, the softmax output can remove the degeneracy of the unique outliers that the regression FIM has at infinite width. (Karakida et al., 2019) `ev:asserted` p. 2 ^karakida2019pathological-004
- The analysis covers fully-connected feedforward networks with one input layer, L−1 hidden layers, and one output layer of C units. (Karakida et al., 2019) `ev:reported` p. 3 ^karakida2019pathological-005
- The weights are drawn i.i.d. from zero-mean Gaussians whose variances scale in the order of 1/M, matching usual practical random initialization. (Karakida et al., 2019) `ev:reported` p. 3 ^karakida2019pathological-006
- The N input samples are generated identically and independently from a standard normal distribution in the theory and experiments. (Karakida et al., 2019) `ev:reported` p. 3 ^karakida2019pathological-007
- The analysis assumes a non-centered network, meaning a network with bias terms or activation functions with a non-zero Gaussian mean. (Karakida et al., 2019) `ev:reported` p. 4 ^karakida2019pathological-008
- The analysis also assumes that the activation function has a polynomially bounded weak derivative, used for the backward order-parameter recurrences. (Karakida et al., 2019) `ev:reported` p. 4 ^karakida2019pathological-009
- The order parameters are computed through recurrence relations requiring L iterations of one- and two-dimensional numerical integrals. (Karakida et al., 2019) `ev:reported` p. 6 ^karakida2019pathological-010
- [[Fisher information matrix|The FIM for cross-entropy loss]] equals the regression FIM with a softmax-derived coefficient matrix Q inserted between the Jacobian and its transpose. (Karakida et al., 2019) `ev:computed` p. 5 ^karakida2019pathological-011
- For the regression FIM, the mean eigenvalue asymptotically decreases in the order of 1/M as the width M grows. (Karakida et al., 2019) `ev:cited` p. 7 ^karakida2019pathological-012
- For the regression FIM, the variance of the eigenvalue spectrum asymptotically takes a value of O(1) in sufficiently wide networks. (Karakida et al., 2019) `ev:cited` p. 7 ^karakida2019pathological-013
- For the regression FIM, the largest eigenvalue asymptotically takes a huge value of order O(M) in sufficiently wide networks. (Karakida et al., 2019) `ev:cited` p. 7 ^karakida2019pathological-014
- The authors suggest that the DNN parameter space is locally almost flat in most directions but highly distorted in a few specific directions. (Karakida et al., 2019) `ev:asserted` p. 7 ^karakida2019pathological-015
- Prior work showed that the eigenspace of the regression FIM's largest eigenvalue is spanned by the C mean-gradient vectors E[∇θfk]. (Karakida et al., 2019) `ev:cited` p. 8 ^karakida2019pathological-016
- Mean subtraction of the output in the last layer, as in batch normalization, eliminates the C largest eigenvalues from the regression FIM. (Karakida et al., 2019) `ev:cited` p. 8 ^karakida2019pathological-017
- Numerical experiments confirmed that the largest eigenvalue of the mean-subtracted regression FIM is of order 1. (Karakida et al., 2019) `ev:cited` p. 8 ^karakida2019pathological-018
- Regression FIM spectra were computed for Tanh networks with L = 3, M = 200, C = 10, N = 100 over 100 seeds. (Karakida et al., 2019) `ev:reported` p. 8 ^karakida2019pathological-019
- In this experiment the regression FIM spectrum had two populations, with the larger population corresponding to the C largest eigenvalues. (Karakida et al., 2019) `ev:measured` p. 8 ^karakida2019pathological-020
- The empirical FIM is equivalent to the Hessian of the loss around a global minimum with zero training loss, the authors remark. (Karakida et al., 2019) `ev:asserted` p. 8 ^karakida2019pathological-021
- Previous work empirically confirmed that a learning rate below 2/λmax is necessary for the steepest gradient method to converge. (Karakida et al., 2019) `ev:cited` p. 8 ^karakida2019pathological-022
- Because the largest eigenvalue increases with width and depth, the authors argue that learning rates must be carefully scaled to train DNNs. (Karakida et al., 2019) `ev:asserted` p. 8 ^karakida2019pathological-023
- The diagonal blocks of the regression FIM have eigenvalue statistics of the same order as the full-sized FIM, including O(M) largest eigenvalues. (Karakida et al., 2019) `ev:computed` p. 8 ^karakida2019pathological-024
- A diagonal block approximation of the FIM, used to decrease natural gradient cost, also suffers from a pathological spectrum. (Karakida et al., 2019) `ev:computed` p. 9 ^karakida2019pathological-025
- The authors note that eigenvalues close to zero can make the inversion of the [[Fisher information matrix|FIM]] in [[Natural gradient descent|natural gradient methods]] unstable. (Karakida et al., 2019) `ev:asserted` p. 9 ^karakida2019pathological-026
- Theorem 3.3 shows that the eigenvalue statistics of the cross-entropy FIM have the same width dependence as those of the regression FIM. (Karakida et al., 2019) `ev:computed` p. 10 ^karakida2019pathological-027
- The mean, second moment and largest eigenvalue of the cross-entropy FIM are bounded above by those of the regression FIM. (Karakida et al., 2019) `ev:computed` p. 10 ^karakida2019pathological-028
- Theorem 3.4 states that the cross-entropy FIM has C largest eigenvalues of order O(M), where C is the number of classes. (Karakida et al., 2019) `ev:computed` p. 10 ^karakida2019pathological-029
- Cross-entropy FIM experiments used L = 3, M = 1000, C = 10 and N = 100 with tanh, ReLU and linear activations. (Karakida et al., 2019) `ev:reported` p. 10 ^karakida2019pathological-030
- The predictions of Theorem 3.3 coincided with the experimental results on artificial data for sufficiently large widths. (Karakida et al., 2019) `ev:measured` p. 10 ^karakida2019pathological-031
- The C largest eigenvalues of the cross-entropy FIM disappear under mean subtraction of the network output in the last layer. (Karakida et al., 2019) `ev:computed` p. 11 ^karakida2019pathological-032
- Compared to the regression FIM, the cross-entropy FIM's C = 10 largest eigenvalues were widely spread from the bulk of the spectrum. (Karakida et al., 2019) `ev:measured` p. 11 ^karakida2019pathological-033
- The authors attribute, naively speaking, the dispersed outliers to the distributed eigenvalues of the softmax coefficient matrix Q. (Karakida et al., 2019) `ev:asserted` p. 11 ^karakida2019pathological-034
- A 3-layered network with M = 2000 and C = 2 was trained by gradient descent on Gaussian inputs labelled by a teacher network. (Karakida et al., 2019) `ev:reported` p. 12 ^karakida2019pathological-035
- The theoretical cross-entropy training loss obtained from NTK theory coincided well with the experimental results of gradient descent training. (Karakida et al., 2019) `ev:measured` p. 12 ^karakida2019pathological-036
- During cross-entropy training, the largest eigenvalue of the regression FIM F stayed unchanged, as expected from NTK theory. (Karakida et al., 2019) `ev:measured` p. 12 ^karakida2019pathological-037
- During cross-entropy training, the largest eigenvalue of the cross-entropy FIM changed dynamically, approaching zero as training proceeded. (Karakida et al., 2019) `ev:measured` p. 12 ^karakida2019pathological-038
- Theoretical bounds from Theorem 3.3, with the softmax output at each step substituted, explained the largest eigenvalue well during training. (Karakida et al., 2019) `ev:measured` p. 12 ^karakida2019pathological-039
- The authors state that estimating a critical learning rate is challenging for the cross-entropy loss, since Q and Fcross change dynamically. (Karakida et al., 2019) `ev:asserted` p. 12 ^karakida2019pathological-040
- The empirical FIM and the [[Neural Tangent Kernel|NTK]] share essentially the same non-zero eigenvalues, the NTK being the FIM's left-to-right reversal up to 1/N. (Karakida et al., 2019) `ev:computed` p. 13 ^karakida2019pathological-041
- Under the [[Neural Tangent Kernel|NTK parameterization]], the derived eigenvalue statistics of the NTK become independent of the width scale M. (Karakida et al., 2019) `ev:computed` p. 13 ^karakida2019pathological-042
- The NTK parameterization makes weight gradients comparable in order to bias gradients, adding a non-negligible bias contribution to the constants. (Karakida et al., 2019) `ev:computed` p. 13 ^karakida2019pathological-043
- Under [[Neural Tangent Kernel|NTK parameterization]], the largest eigenvalue of the NTK depends on the sample size N, unlike its mean eigenvalue. (Karakida et al., 2019) `ev:computed` p. 13 ^karakida2019pathological-044
- The authors suggest that, as the sample size increases, the training dynamics under the NTK converge non-uniformly. (Karakida et al., 2019) `ev:asserted` p. 2 ^karakida2019pathological-045
- According to the authors, [[Neural Tangent Kernel|NTK dynamics]] converge more slowly in the eigenspace of the relatively small eigenvalues, which are the majority. (Karakida et al., 2019) `ev:asserted` p. 13 ^karakida2019pathological-046
- The authors expect computations with the inverse NTK to be numerically inaccurate when the sample size is large. (Karakida et al., 2019) `ev:asserted` p. 13 ^karakida2019pathological-047
- In experiments with L = 3 and C = 2, the NTK eigenvalue spectrum became pathologically distorted as the sample size increased. (Karakida et al., 2019) `ev:measured` p. 14 ^karakida2019pathological-048
- As the sample size increased in these experiments, most [[Neural Tangent Kernel|NTK eigenvalues]] concentrated close to zero, with the largest eigenvalues becoming outliers. (Karakida et al., 2019) `ev:measured` p. 14 ^karakida2019pathological-049
- In experiments, mean subtraction in the last layer kept the NTK's whole eigenvalue spectrum within a range of O(1) when N was proportional to M. (Karakida et al., 2019) `ev:measured` p. 14 ^karakida2019pathological-050
- The mean-subtracted NTK spectrum empirically converged to a fixed distribution in the large M limit. (Karakida et al., 2019) `ev:measured` p. 14 ^karakida2019pathological-051
- For the input and feature space metric, the mean eigenvalue asymptotically decreases in the order of O(1/M) as width grows. (Karakida et al., 2019) `ev:computed` p. 15 ^karakida2019pathological-052
- For the input and feature space metric, the largest eigenvalue is of O(1) for any width M and sample size N. (Karakida et al., 2019) `ev:computed` p. 15 ^karakida2019pathological-053
- The eigenvector of the per-output input and feature metric corresponding to its largest eigenvalue is the mean gradient E[∇hfk]. (Karakida et al., 2019) `ev:computed` p. 15 ^karakida2019pathological-054
- Experiments with deep Tanh networks at M = 500 and N = 1000 showed pathological spectra for the input and feature metric, as predicted. (Karakida et al., 2019) `ev:measured` p. 15 ^karakida2019pathological-055
- With softmax output, the outliers of the input and feature space metric spread widely, in the same manner as the cross-entropy FIM. (Karakida et al., 2019) `ev:measured` p. 15 ^karakida2019pathological-056
- The authors speculate that the eigenvector of the largest eigenvalue may be related to adversarial attacks, which requires careful consideration. (Karakida et al., 2019) `ev:asserted` p. 15 ^karakida2019pathological-057
- The authors suggest care is needed about eigenvalue statistics and their influence on learning when using large-scale deep networks in naive settings. (Karakida et al., 2019) `ev:asserted` p. 15 ^karakida2019pathological-058
- The study focused on fully-connected networks, leaving the spectra of other architectures such as ResNets and CNNs for future exploration. (Karakida et al., 2019) `ev:asserted` p. 15 ^karakida2019pathological-059
- The authors state that deriving the whole eigenvalue spectrum analytically, beyond the basic statistics captured here, remains to be done. (Karakida et al., 2019) `ev:asserted` p. 15 ^karakida2019pathological-060
- The authors see extending random matrix theory to deep neural networks as a prerequisite for further progress on the spectrum bulk. (Karakida et al., 2019) `ev:asserted` p. 15 ^karakida2019pathological-061
- The analysis assumed a finite number of network output units, which the authors flag as a limit for high-dimensional multi-label classification. (Karakida et al., 2019) `ev:asserted` p. 15 ^karakida2019pathological-062
- The analysis treated order parameters as constants at finite depth, although they can explode exponentially in extremely deep chaotic networks. (Karakida et al., 2019) `ev:asserted` p. 15 ^karakida2019pathological-063
- The authors state that the condition κ2 > 0, guaranteed by non-centered networks, is crucial for their eigenvalue statistics. (Karakida et al., 2019) `ev:asserted` p. 16 ^karakida2019pathological-064

## 🎯 Contributions

## 📖 Glossary

- **Fisher information matrix (FIM)** — Riemannian metric on parameter space; equals the loss Hessian near a zero-loss minimum.
- **Empirical FIM** — FIM with the input expectation replaced by the mean over N samples.
- **Neural tangent kernel (NTK)** — Gram matrix of output Jacobians; shares non-zero eigenvalues with the empirical FIM.
- **Order parameters** — Layer-wise averages of forward and backward signals, computable by recurrences in wide networks.
- **Pathological spectrum** — Eigenvalue spectrum with a few huge outliers while most eigenvalues sit near zero.
- **Pathological sharpness** — Steep local loss landscape caused by the FIM's largest eigenvalue.
- **Non-centered network** — Network with bias terms or activations with non-zero Gaussian mean.
- **NTK parameterization** — Weights written as standard Gaussians times sigma over square-root fan-in.
- **Mean subtraction** — Removing the output's input-average in the last layer, as in batch normalization.
- **Diagonal block approximation** — Keeping only layer-wise diagonal FIM blocks to cut natural gradient cost.

## ❓ Open questions

- What are the precise values of the C outliers of the cross-entropy FIM, beyond the lower and upper bounds of Theorem 3.3?
- Can the whole eigenvalue spectrum, including the bulk left after mean subtraction, be derived analytically for deep non-centered networks?
- How do these spectra change for ResNets, CNNs and other non-fully-connected architectures?
- How do the eigenvalue statistics behave when the number of output units also grows with width?
- How do the results change in extremely deep networks in the chaotic regime, where order parameters explode?
- Can a critical learning rate be estimated for cross-entropy training, where Q and Fcross change dynamically?
- Is the top eigenvector of the input-space metric related to adversarial perturbations?
- How do these eigenvalue statistics connect to generalization performance?

## 📝 Notes on reading

Version read: arXiv 1910.05992v2 (27 Sep 2020), a preprint; the record year is 2019.

Theorems 3.1 and 3.2 and the mean-subtraction result (Eq. 22) are restated from the authors' earlier work [32, 34]; claims resting on them are coded `ev:cited`.

Inconsistency: Section 4.2 (p. 14) describes the NTK spectra experiment as Figure 5, but the NTK spectra are shown in Figure 6 (p. 13); Figure 5 is the cross-entropy training experiment. The Figure 6 caption says deep ReLU networks, M = 1000, and 400 networks, while the text on p. 14 gives L = 3, C = 2 and (σw², σb²) = (2, 0).

Figures 3, 4, 6 and 7 are histograms and plots that could only be described from their captions and text; no per-point values were claimed. The equations of Theorems 3.1, 3.3, 5.1 and Appendices A–D are partly garbled in the extraction (sub/superscripts flattened), so exact formulas for the eigenvalue statistics were not transcribed as claims.

## Suggested new concepts

- Pathological spectrum of the Fisher information matrix — recurring result across FIM, NTK and input-space metrics in wide networks.
- Mean-field order parameters for wide networks — the tool that makes these eigenvalue statistics computable.
- Neural tangent kernel — central object linking FIM spectra to training dynamics and conditioning.
- Natural gradient with block-diagonal FIM approximation — practical method whose conditioning this paper speaks to.
- Mean subtraction / batch normalization as spectrum normalization — removes the C outliers of FIM and NTK.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Espectro de la Fisher y relación con el NTK (E.1).

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
