---
aliases: []
type: "source"
title: "Probabilistic orientation estimation with matrix Fisher distributions"
citekey: "Mohlin2020probabilistic"
doi: "10.48550/arXiv.2006.09740"
arxiv: "2006.09740"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2006.09740"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["D. Mohlin", "G. Bianchi", "J. Sullivan"]
sha256: ["339c8fa4cccb54839deaad5cfa8239662c05ae5fc2ebfd6b9eab41d375f7e624"]
pdf: "Content/Papers/Mohlin2020probabilistic.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Mohlin2020probabilistic.pdf]]

> [!abstract] One-sentence summary
> A neural network regresses the unconstrained parameters of a matrix Fisher distribution over SO(3) and is trained with a provably convex negative log-likelihood loss, giving rotation uncertainty estimates and state-of-the-art orientation accuracy on Pascal3D+, ModelNet10-SO(3) and UPNA head pose.

## Abstract

This paper focuses on estimating probability distributions over the set of 3D rotations ($SO(3)$) using deep neural networks. Learning to regress models to the set of rotations is inherently difficult due to differences in topology between $\mathbb{R}^N$ and $SO(3)$. We overcome this issue by using a neural network to output the parameters for a matrix Fisher distribution since these parameters are homeomorphic to $\mathbb{R}^9$. By using a negative log likelihood loss for this distribution we get a loss which is convex with respect to the network outputs. By optimizing this loss we improve state-of-the-art on several challenging applicable datasets, namely Pascal3D+, ModelNet10-$SO(3)$ and UPNA head pose. (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that neural network outputs live in R^N, whose topology differs from SO(3), making continuous losses without disconnected local minima hard to design. (Mohlin et al., 2020) `ev:asserted` p. 1 ^mohlin2020probabilistic-001
- Quaternion representations have a double embedding that gives rise to two disconnected local minima in the loss, according to the authors. (Mohlin et al., 2020) `ev:asserted` p. 1 ^mohlin2020probabilistic-002
- Using Euler angles as an intermediate rotation representation causes problems due to the so-called gimbal lock, the authors note. (Mohlin et al., 2020) `ev:asserted` p. 1 ^mohlin2020probabilistic-003
- Gram-Schmidt based rotation mappings have a continuous inverse but are discontinuous when the input vectors do not span R3. (Mohlin et al., 2020) `ev:cited` p. 1 ^mohlin2020probabilistic-004
- Earlier work on [[Rotation representation continuity|rotation continuity]] shows that any rotation representation with four or fewer dimensions is discontinuous, making network generalization over rotations difficult. (Mohlin et al., 2020) `ev:cited` p. 2 ^mohlin2020probabilistic-005
- Earlier orientation uncertainty work estimated parameters of a mixture of von Mises distributions using a biternion network. (Mohlin et al., 2020) `ev:cited` p. 2 ^mohlin2020probabilistic-006
- Another prior method used a [[Bingham distribution]] over quaternions, whose parameters have to be positive semidefinite. (Mohlin et al., 2020) `ev:cited` p. 2 ^mohlin2020probabilistic-007
- The paper trains a deep neural network to output parameters of a matrix Fisher distribution over the rotation group SO(3). (Mohlin et al., 2020) `ev:reported` p. 2 ^mohlin2020probabilistic-008
- The matrix Fisher parameterization is unconstrained, so no complex functions are needed to enforce constraints on the parameters. (Mohlin et al., 2020) `ev:asserted` p. 2 ^mohlin2020probabilistic-009
- The authors state that their convex loss with bounded gradient magnitudes results in stable training, unlike [[Rotation representation continuity|discontinuous rotation losses]]. (Mohlin et al., 2020) `ev:asserted` p. 2 ^mohlin2020probabilistic-010
- The matrix Fisher density is proportional to exp(tr(F^T R)), where F is an unconstrained real three-by-three parameter matrix. (Mohlin et al., 2020) `ev:reported` p. 3 ^mohlin2020probabilistic-011
- The distribution's mode is obtained from the singular value decomposition of F, with a determinant correction ensuring a proper rotation. (Mohlin et al., 2020) `ev:cited` p. 3 ^mohlin2020probabilistic-012
- Visualizations of simple F matrices show that larger singular values correspond to more peaked matrix Fisher distributions. (Mohlin et al., 2020) `ev:computed` p. 3 ^mohlin2020probabilistic-013
- The normalizing constant a(F) equals a generalized hypergeometric function of a matrix argument, which is non-trivial to compute efficiently. (Mohlin et al., 2020) `ev:cited` p. 3 ^mohlin2020probabilistic-014
- The training loss is the negative log-likelihood of the ground-truth rotation given the network's predicted parameter matrix. (Mohlin et al., 2020) `ev:reported` p. 4 ^mohlin2020probabilistic-015
- The authors believe the loss equilibrium lying far from the origin led to instability in some experiments. (Mohlin et al., 2020) `ev:asserted` p. 4 ^mohlin2020probabilistic-016
- To move the loss equilibrium closer to the origin, the authors used a regularizing term 5% larger than analytically correct. (Mohlin et al., 2020) `ev:reported` p. 4 ^mohlin2020probabilistic-017
- To make training computationally feasible, the authors fit simple functions approximating the hypergeometric normalizer and its derivatives. (Mohlin et al., 2020) `ev:reported` p. 4 ^mohlin2020probabilistic-018
- Preliminary experiments seem to indicate that results are not so sensitive to the accuracy of the normalizer approximation. (Mohlin et al., 2020) `ev:measured` p. 4 ^mohlin2020probabilistic-019
- The authors concede that their normalizing-constant approximation is perhaps far from optimal, though it makes training computationally feasible. (Mohlin et al., 2020) `ev:asserted` p. 4 ^mohlin2020probabilistic-020
- The approach is tested on three datasets: Pascal3D+, ModelNet10-SO(3), and the UPNA head pose dataset. (Mohlin et al., 2020) `ev:reported` p. 4 ^mohlin2020probabilistic-021
- Pascal3D+ has 12 rigid object classes, with images from Pascal VOC and ImageNet annotated with class, bounding box and 3D pose. (Mohlin et al., 2020) `ev:cited` p. 5 ^mohlin2020probabilistic-022
- Pascal3D+ images are warped by a homography so they appear taken by a camera with known intrinsics pointing at the object. (Mohlin et al., 2020) `ev:reported` p. 5 ^mohlin2020probabilistic-023
- The UPNA head pose dataset contains videos of 10 people, each with 11 recordings, annotated with facial keypoints and 3D rotation. (Mohlin et al., 2020) `ev:cited` p. 5 ^mohlin2020probabilistic-024
- Lacking an official UPNA split, the authors used the last 2 people as the test set. (Mohlin et al., 2020) `ev:reported` p. 5 ^mohlin2020probabilistic-025
- UPNA face bounding boxes were derived from keypoint annotations and randomly perturbed to resemble face detector output. (Mohlin et al., 2020) `ev:reported` p. 5 ^mohlin2020probabilistic-026
- The network uses an ImageNet-pretrained ResNet-101 backbone followed by 3 fully connected layers with 512, 512 and 9 outputs. (Mohlin et al., 2020) `ev:reported` p. 5 ^mohlin2020probabilistic-027
- The object class is encoded by an embedding layer producing a 32-dimensional vector appended to the ResNet pooled activations. (Mohlin et al., 2020) `ev:reported` p. 5 ^mohlin2020probabilistic-028
- Training uses SGD with a batch size of 32 and an initial learning rate of 0.01. (Mohlin et al., 2020) `ev:reported` p. 5 ^mohlin2020probabilistic-029
- Performance is summarized by the median geodesic angle error in degrees and by Acc@Y, the fraction of errors below Y. (Mohlin et al., 2020) `ev:reported` p. 5 ^mohlin2020probabilistic-030
- For UPNA the authors report mean instead of median geodesic error, allowing more direct comparison with the Bingham-loss results. (Mohlin et al., 2020) `ev:reported` p. 6 ^mohlin2020probabilistic-031
- Without synthetic training data, the method reached a Pascal3D+ median error of 8.90 and an Acc@π/6 of 90.8. (Mohlin et al., 2020) `ev:measured` p. 6 ^mohlin2020probabilistic-032
- With synthetic training data added, the method reached a Pascal3D+ median error of 8.10 and an Acc@π/6 of 93.1. (Mohlin et al., 2020) `ev:measured` p. 6 ^mohlin2020probabilistic-033
- On Pascal3D+ the method obtained an Acc@π/12 of 74.5 without synthetic data and 78.2 with it. (Mohlin et al., 2020) `ev:measured` p. 6 ^mohlin2020probabilistic-034
- The strongest prior Pascal3D+ entry, Liao et al., reported a median error of 9.20 and an Acc@π/6 of 88.7. (Mohlin et al., 2020) `ev:cited` p. 6 ^mohlin2020probabilistic-035
- Adding the synthetic training dataset reduced the Pascal3D+ mean over per-class medians angle error by approximately 1 degree. (Mohlin et al., 2020) `ev:measured` p. 6 ^mohlin2020probabilistic-036
- The authors state that their method significantly outperforms all the prior approaches compared on Pascal3D+. (Mohlin et al., 2020) `ev:asserted` p. 6 ^mohlin2020probabilistic-037
- On the Pascal3D+ boat class, median error fell from 20.5 for the previous state-of-the-art method to 12.6 without synthetic data. (Mohlin et al., 2020) `ev:measured` p. 6 ^mohlin2020probabilistic-038
- On the Pascal3D+ aeroplane class, the method without synthetic data had higher median error, 10.2, than the prior method's 8.5. (Mohlin et al., 2020) `ev:measured` p. 6 ^mohlin2020probabilistic-039
- On the Pascal3D+ dining table class, adding synthetic data raised median error from 8.4 to 10.6. (Mohlin et al., 2020) `ev:measured` p. 6 ^mohlin2020probabilistic-040
- On the UPNA head pose dataset the method gave a mean angle error of 4.5 degrees. (Mohlin et al., 2020) `ev:measured` p. 6 ^mohlin2020probabilistic-041
- The Bingham-loss method quotes 6.3 degrees on UPNA, but its different test split makes direct comparison hard. (Mohlin et al., 2020) `ev:cited` p. 6 ^mohlin2020probabilistic-042
- The authors judge their person-disjoint UPNA test split likely more challenging than the split used in the Bingham-loss work. (Mohlin et al., 2020) `ev:asserted` p. 6 ^mohlin2020probabilistic-043
- On ModelNet10-SO(3) the method reached a median error of 17.1 degrees and an Acc@π/6 of 75.7. (Mohlin et al., 2020) `ev:measured` p. 7 ^mohlin2020probabilistic-044
- The revised Liao spherical regression numbers on ModelNet10-SO(3), using the geodesic metric, give a median error of 28.7 degrees. (Mohlin et al., 2020) `ev:cited` p. 7 ^mohlin2020probabilistic-045
- At the Acc@π/24 threshold the method scored 55.2 on ModelNet10-SO(3), against 35.2 for the revised Liao baseline. (Mohlin et al., 2020) `ev:measured` p. 7 ^mohlin2020probabilistic-046
- On ModelNet10-SO(3) the rotationally symmetric bathtub class had a median error of 89.1 degrees, against 4.0 for sofa. (Mohlin et al., 2020) `ev:measured` p. 7 ^mohlin2020probabilistic-047
- The ModelNet10-SO(3) table class, also rotationally symmetric, had a median error of 25.8 and an Acc@π/6 of 51.1. (Mohlin et al., 2020) `ev:measured` p. 7 ^mohlin2020probabilistic-048
- The authors suspect manual labeling biases Pascal3D+ dining tables toward one ambiguous pose, a bias absent from the synthetic data. (Mohlin et al., 2020) `ev:asserted` p. 7 ^mohlin2020probabilistic-049
- For the ModelNet10-SO(3) table class, the test error histogram has a U shape, indicating the network predicts one relevant pose. (Mohlin et al., 2020) `ev:measured` p. 8 ^mohlin2020probabilistic-050
- Early in training, the predicted distribution for a symmetric table is almost uniform on the plane spanned by its [[Pose ambiguity from symmetry|ambiguous axes]]. (Mohlin et al., 2020) `ev:measured` p. 8 ^mohlin2020probabilistic-051
- Late in training the network's uncertainty on the training set becomes small, which the authors call a deterioration of probabilistic modelling. (Mohlin et al., 2020) `ev:asserted` p. 8 ^mohlin2020probabilistic-052
- In the Pascal3D+ ablation, removing data augmentation raised median error from 8.9 to 10.1 degrees. (Mohlin et al., 2020) `ev:measured` p. 8 ^mohlin2020probabilistic-053
- Without augmentation, homography warping gave a median error of 10.1 against 10.0 for plain cropping on Pascal3D+. (Mohlin et al., 2020) `ev:measured` p. 8 ^mohlin2020probabilistic-054
- Removing the class embedding left the Pascal3D+ median error unchanged at 8.9 degrees in the ablation. (Mohlin et al., 2020) `ev:measured` p. 8 ^mohlin2020probabilistic-055
- The authors suggest the ablation results indicate their loss is the most significant component of the approach. (Mohlin et al., 2020) `ev:asserted` p. 8 ^mohlin2020probabilistic-056
- The authors argue homography warping should in theory let the method generalize across pinhole cameras with known intrinsics and negligible radial distortion. (Mohlin et al., 2020) `ev:asserted` p. 8 ^mohlin2020probabilistic-057
- Since the matrix Fisher distribution is unimodal, it poorly models classes with [[Pose ambiguity from symmetry|rotational symmetries]], the authors conclude. (Mohlin et al., 2020) `ev:asserted` p. 9 ^mohlin2020probabilistic-058
- As future work the authors suggest a loss for multimodal distributions that keeps the optimization properties of their loss. (Mohlin et al., 2020) `ev:asserted` p. 9 ^mohlin2020probabilistic-059
- The authors caution that owing to the small UPNA test size, reported performance might not reflect average performance for any population. (Mohlin et al., 2020) `ev:asserted` p. 9 ^mohlin2020probabilistic-060
- Training curves on ModelNet10-SO(3) show the network overfitting more on the loss than on the median error. (Mohlin et al., 2020) `ev:measured` p. 14 ^mohlin2020probabilistic-061
- The loss is proven Lipschitz continuous with α=6, meaning the L2 norm of its gradient is less than 6. (Mohlin et al., 2020) `ev:computed` p. 16 ^mohlin2020probabilistic-062
- The authors prove that the loss is convex in the network output F, since its log-normalizer Hessian is a variance matrix. (Mohlin et al., 2020) `ev:computed` p. 16 ^mohlin2020probabilistic-063
- The loss is proven to have Lipschitz continuous gradients with β=9, bounding the largest eigenvalue of its Hessian. (Mohlin et al., 2020) `ev:computed` p. 16 ^mohlin2020probabilistic-064
- The log normalizer is approximated as the maximum input plus a correction whose second-degree polynomials are fitted by moment matching at the origin. (Mohlin et al., 2020) `ev:reported` p. 17 ^mohlin2020probabilistic-065
- Increasing all 4 diagonal entries of Λ by ϵ scales the integral by exp(ϵ), so the log-gradients sum to 1. (Mohlin et al., 2020) `ev:computed` p. 17 ^mohlin2020probabilistic-066
- Naive cropping of non-square bounding boxes can cause scaling artifacts that look very similar to a rotation of the object. (Mohlin et al., 2020) `ev:asserted` p. 19 ^mohlin2020probabilistic-067

## 🎯 Contributions

## 📖 Glossary

- **SO(3)** — The special orthogonal group: all 3D rotation matrices, a closed nonlinear manifold.
- **Matrix Fisher distribution** — Unimodal distribution on SO(3) with density proportional to exp(tr(F^T R)).
- **Normalizing constant a(F)** — Integral of exp(tr(F^T R)) over SO(3); a matrix-argument hypergeometric function.
- **Geodesic distance** — Rotation angle between two rotation matrices, used here as the error metric.
- **Acc@Y** — Fraction of test samples whose geodesic error is below threshold Y.
- **Proper SVD** — SVD of F adjusted so U and V are rotations, singular values sign-corrected.
- **Principal axes** — Columns of U; the spread of the distribution is oriented around them.
- **Homography warping** — Reprojecting an image to a virtual camera whose principal axis faces the object.
- **Bingham distribution** — Antipodally symmetric distribution on the sphere, used over quaternions in prior work.

## ❓ Open questions

- Can a loss over multimodal rotation distributions keep the convexity and bounded-gradient properties of the matrix Fisher NLL?
- How much does the hand-fitted approximation of the normalizing constant cost in accuracy compared with a theoretically well-founded one?
- How can the probabilistic calibration be protected from overfitting of the loss late in training, especially for symmetric objects?
- How does the method compare with the Bingham-loss approach on UPNA under an identical, person-disjoint test split?
- Is the 5% over-weighting of the regularizing term needed generally, or only for particular datasets?

## 📝 Notes on reading

Read the arXiv v1 preprint (2006.09740v1, 17 Jun 2020, marked Under review), which matches the packet identifier; pages 12-20 are the supplementary material.

Figure 1 (p. 3) and Figure 7 (p. 15) show the same diag(5, 5, 5) visualization; Figures 2, 3, 4, 5, 8, 9, 10 and 11 were only described, not claimed. Figure 5 lists per-image errors for a random subset of Pascal3D+ test images without units.

Table 2 (p. 6) shows only 9 of the 12 Pascal3D+ classes; the full per-class table is Table 6 (p. 13). The prior method [19] is called state-of-the-art in Table 6 while Table 1 lists Liao et al. [16] with a lower median error.

Inconsistencies: the text on p. 8 refers to plots (b)-(g) of Figure 4, but the figure has panels (b)-(e) plus the histogram (f). Equation 23 (p. 18) says its denominator comes from fulfilling equation 25, which appears to mean equation 22. The main text uses s′3 = s3 det(UV) in Λ1 (p. 3) while the supplement (p. 18) writes Λ1 with s3. The abstract claims improvement on UPNA although the authors say a direct comparison is hard because test splits differ. Section 4.2 says training runs 120 epochs yet the Figure 4 histogram is taken after 50 epochs (the ModelNet10-SO(3) schedule).

The mathematical expressions in the extraction (equations 2, 8, 19, 23, 24) are partly garbled; the approximation formulas were described, not quoted.

## Suggested new concepts

- Matrix Fisher distribution — a reusable probabilistic output head for rotation regression with unconstrained parameters.
- Rotation representation continuity — explains why quaternion, Euler and low-dimensional rotation outputs hurt network regression.
- Rotational symmetry ambiguity in pose estimation — recurring failure mode for unimodal pose models (tables, bathtubs, bottles).
- Uncertainty calibration under overfitting — NLL losses become overconfident while accuracy keeps improving, as in classification.
- Perspective-correcting crop via homography — preprocessing that removes crop-induced apparent rotation.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Distribución de Fisher matricial en $SO(3)$ con NLL

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
