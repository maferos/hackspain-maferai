---
aliases: []
type: "source"
title: "An Analysis of SVD for Deep Rotation Estimation"
citekey: "Levinson2020analysis"
doi: "10.48550/arXiv.2006.14616"
arxiv: "2006.14616"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2006.14616"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Jake Levinson", "Carlos Esteves", "Kefan Chen", "Noah Snavely", "Angjoo Kanazawa", "Afshin Rostamizadeh", "Ameesh Makadia"]
sha256: ["638cb6f7de8f12e475ca34e0179a158fbd6fac25d736177bf92ddd494b133a70"]
pdf: "Content/Papers/Levinson2020analysis.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Levinson2020analysis.pdf]]

> [!abstract] One-sentence summary
> The paper shows, through least-squares, likelihood, gradient and noise analyses plus six benchmarks, that predicting a 9D matrix and projecting it onto SO(3) with SVD is a strong default rotation representation for neural networks.

## Abstract

Symmetric orthogonalization via SVD, and closely related procedures, are well-known techniques for projecting matrices onto $O(n)$ or $SO(n)$. These tools have long been used for applications in computer vision, for example optimal 3D alignment problems solved by orthogonal Procrustes, rotation averaging, or Essential matrix decomposition. Despite its utility in different settings, SVD orthogonalization as a procedure for producing rotation matrices is typically overlooked in deep learning models, where the preferences tend toward classic representations like unit quaternions, Euler angles, and axis-angle, or more recently-introduced methods. Despite the importance of 3D rotations in computer vision and robotics, a single universally effective representation is still missing. Here, we explore the viability of SVD orthogonalization for 3D rotations in neural networks. We present a theoretical analysis that shows SVD is the natural choice for projecting onto the rotation group. Our extensive quantitative analysis shows simply replacing existing representations with the SVD orthogonalization procedure obtains state of the art performance in many deep learning applications covering both supervised and unsupervised training. (arXiv)

## 🧠 Key ideas (atomic)

- The paper explores the viability of SVD orthogonalization as a procedure for producing 3D rotations in neural networks. (Levinson et al., 2020) `ev:asserted` p. 1 ^levinson2020analysis-001
- The most frequent rotation representations in deep models are classic ones, including unit quaternion, Euler angles, and axis-angle. (Levinson et al., 2020) `ev:asserted` p. 1 ^levinson2020analysis-002
- The authors state there is no universally effective rotation representation or regression architecture due to performance variations across applications. (Levinson et al., 2020) `ev:asserted` p. 1 ^levinson2020analysis-003
- Orthogonalization via SVD is rarely used for generating 3D rotations in deep learning, nor considered a benchmark for new representations. (Levinson et al., 2020) `ev:asserted` p. 2 ^levinson2020analysis-004
- The authors do not claim to be the first to introduce SVD to deep learning, focusing instead on a comprehensive study. (Levinson et al., 2020) `ev:asserted` p. 2 ^levinson2020analysis-005
- The evaluation spans point cloud alignment, object pose from images, inverse kinematics, and depth prediction from images, in supervised and unsupervised settings. (Levinson et al., 2020) `ev:reported` p. 2 ^levinson2020analysis-006
- Rotation estimation via SVD orthogonalization achieves state of the art performance in almost all of the tested application settings. (Levinson et al., 2020) `ev:measured` p. 2 ^levinson2020analysis-007
- SVD orthogonalization is the best performing method among those that can be applied in both supervised and unsupervised settings. (Levinson et al., 2020) `ev:measured` p. 2 ^levinson2020analysis-008
- SO(3) is not topologically homeomorphic to any subset of 4D Euclidean space, so parameterizations in four or fewer dimensions are discontinuous. (Levinson et al., 2020) `ev:cited` p. 2 ^levinson2020analysis-009
- Classification-based rotation methods require supervision on the classification objective, which makes them unsuitable for unsupervised settings. (Levinson et al., 2020) `ev:asserted` p. 2 ^levinson2020analysis-010
- Probabilistic rotation representations based on von Mises and Bingham distributions do not reach state of the art when a single precise rotation must be predicted. (Levinson et al., 2020) `ev:cited` p. 2 ^levinson2020analysis-011
- The closest prior approach is a continuous 6D representation mapped onto SO(3) through a partial Gram-Schmidt procedure. (Levinson et al., 2020) `ev:cited` p. 2 ^levinson2020analysis-012
- Symmetric orthogonalization via SVD is well known to be optimal in the least-squares sense for projecting onto O(n) or SO(n). (Levinson et al., 2020) `ev:cited` p. 3 ^levinson2020analysis-013
- The evaluated procedure takes a 9-dimensional network output, interprets it as a 3 × 3 matrix, and projects it onto SO(3). (Levinson et al., 2020) `ev:reported` p. 3 ^levinson2020analysis-014
- Under additive Gaussian noise on a rotation matrix, SVD special orthogonalization gives the maximum likelihood estimate of the underlying rotation. (Levinson et al., 2020) `ev:computed` p. 3 ^levinson2020analysis-015
- For SVDO, the loss gradient with respect to the input matrix is undefined when two singular values are both zero. (Levinson et al., 2020) `ev:computed` p. 4 ^levinson2020analysis-016
- For SVDO, the loss gradient with respect to the input matrix becomes large when the sum of two singular values is near zero. (Levinson et al., 2020) `ev:computed` p. 4 ^levinson2020analysis-017
- For SVDO+ with negative determinant, the gradient is undefined if the smallest singular value has multiplicity greater than 1. (Levinson et al., 2020) `ev:computed` p. 4 ^levinson2020analysis-018
- For SVDO+, the gradient is large if the two smallest singular values are close to each other or close to zero. (Levinson et al., 2020) `ev:computed` p. 4 ^levinson2020analysis-019
- To first order under small Gaussian noise, the expected reconstruction error of Gram-Schmidt orthogonalization is twice that of SVD orthogonalization. (Levinson et al., 2020) `ev:computed` p. 4 ^levinson2020analysis-020
- For 3 × 3 matrices with i.i.d. Gaussian noise, the expected squared error to the identity is 3σ2 for SVDO versus 6σ2 for Gram-Schmidt. (Levinson et al., 2020) `ev:computed` p. 4 ^levinson2020analysis-021
- In expectation, Gram-Schmidt deviates 1.5 times further from the noisy observation itself than SVD orthogonalization does. (Levinson et al., 2020) `ev:computed` p. 5 ^levinson2020analysis-022
- The authors trace the performance difference to Gram-Schmidt being greedy with respect to the starting matrix, whereas SVD is coordinate-independent. (Levinson et al., 2020) `ev:asserted` p. 5 ^levinson2020analysis-023
- The authors note that i.i.d. Gaussian noise is not necessarily reflective of a neural network's predictions. (Levinson et al., 2020) `ev:asserted` p. 5 ^levinson2020analysis-024
- SVDO+ is discontinuous only if det(M) = 0 or det(M) < 0 with a smallest singular value of multiplicity greater than 1. (Levinson et al., 2020) `ev:computed` p. 5 ^levinson2020analysis-025
- Gram-Schmidt special orthogonalization is continuous on a slightly larger domain of nonsingular matrices, at the cost of significantly greater expected error. (Levinson et al., 2020) `ev:computed` p. 5 ^levinson2020analysis-026
- SVD orthogonalization is equivariant to rotations applied on both sides, whereas Gram-Schmidt is rotation-equivariant on only one side. (Levinson et al., 2020) `ev:computed` p. 5 ^levinson2020analysis-027
- Differentiable SVD ops in PyTorch and TensorFlow allow the procedure to be used easily in popular deep learning libraries. (Levinson et al., 2020) `ev:reported` p. 5 ^levinson2020analysis-028
- SVD-Inference applies the training loss directly to the raw matrix and uses SVD special orthogonalization only at inference. (Levinson et al., 2020) `ev:reported` p. 6 ^levinson2020analysis-029
- SVD, 6D, 5D, and classic representations are trained with half the squared Frobenius distance between predicted and target rotation matrices. (Levinson et al., 2020) `ev:reported` p. 6 ^levinson2020analysis-030
- The point cloud alignment benchmark samples rotations uniformly from SO(3), so the data carry no rotation bias. (Levinson et al., 2020) `ev:reported` p. 6 ^levinson2020analysis-031
- In supervised point cloud alignment, SVD-Train reached a mean geodesic error of 1.63 degrees versus 2.24 for 6D. (Levinson et al., 2020) `ev:measured` p. 6 ^levinson2020analysis-032
- In supervised point cloud alignment, SVD-Inference performed on par with the best baseline, 6D, with a mean error of 2.64 degrees. (Levinson et al., 2020) `ev:measured` p. 6 ^levinson2020analysis-033
- The hybrid approaches 3D-RCNN and MG underperformed the top regression baselines in supervised point cloud alignment. (Levinson et al., 2020) `ev:measured` p. 6 ^levinson2020analysis-034
- The best performing point cloud alignment methods at the end of training, SVD variants and 6D, also showed fast convergence. (Levinson et al., 2020) `ev:measured` p. 6 ^levinson2020analysis-035
- ModelNet pose estimation used MobileNet image features followed by fully connected regression layers, focusing on chair and sofa categories. (Levinson et al., 2020) `ev:reported` p. 6 ^levinson2020analysis-036
- SVD-Inference performed similarly to SVD-Train on ModelNet with faster convergence, suggesting short SVD-Inference pretraining could improve convergence rates. (Levinson et al., 2020) `ev:measured` p. 6 ^levinson2020analysis-037
- The authors note that benchmarks where hybrid methods reached state of the art have strongly biased camera viewpoints. (Levinson et al., 2020) `ev:asserted` p. 6 ^levinson2020analysis-038
- On ModelNet chair images, SVD-Train achieved a mean error of 21.25 degrees, compared with 22.60 for 6D. (Levinson et al., 2020) `ev:measured` p. 7 ^levinson2020analysis-039
- On ModelNet sofa images, SVD-Train achieved a mean error of 18.01 degrees, compared with 20.25 for 6D. (Levinson et al., 2020) `ev:measured` p. 7 ^levinson2020analysis-040
- Pascal3D+ training discarded occluded or truncated objects from real images of 12 categories, augmenting them with rendered images. (Levinson et al., 2020) `ev:reported` p. 7 ^levinson2020analysis-041
- On Pascal3D+, S2-Reg was clearly the best method, ranking first on all four metrics averaged over 12 categories. (Levinson et al., 2020) `ev:measured` p. 7 ^levinson2020analysis-042
- On Pascal3D+, the SVD variants were the best performing of the regression methods that train only with a rotation loss. (Levinson et al., 2020) `ev:measured` p. 7 ^levinson2020analysis-043
- On Pascal3D+ averaged over 12 categories, SVD-Inference reached a median error of 13.0 degrees versus 12.9 for 3D-RCNN. (Levinson et al., 2020) `ev:measured` p. 7 ^levinson2020analysis-044
- SVD-Inference slightly outperformed SVD-Train on Pascal3D+, suggesting direct regression to the rotation can work well under non-uniform viewpoint priors. (Levinson et al., 2020) `ev:measured` p. 7 ^levinson2020analysis-045
- Unsupervised experiments omit methods needing classification supervision, and also SVD-Inference, which does not produce SO(3) outputs while training. (Levinson et al., 2020) `ev:reported` p. 8 ^levinson2020analysis-046
- In self-supervised point cloud alignment, the only loss is L2 on the point cloud registration after applying the predicted rotation. (Levinson et al., 2020) `ev:reported` p. 8 ^levinson2020analysis-047
- In self-supervised point cloud alignment, SVD-Train reached a mean error of 1.58 degrees versus 2.39 for the next closest baseline, 6D. (Levinson et al., 2020) `ev:measured` p. 8 ^levinson2020analysis-048
- In the inverse kinematics experiment, the network predicts rotations from a canonical T-pose, with loss on joint positions from forward kinematics. (Levinson et al., 2020) `ev:reported` p. 8 ^levinson2020analysis-049
- In human pose inverse kinematics, SVD-Train had a mean joint error of 1.61 cm versus 1.70 cm for 6D. (Levinson et al., 2020) `ev:measured` p. 8 ^levinson2020analysis-050
- In inverse kinematics, 6D came closer to SVD-Train than in other experiments, with a median error of 1.28 cm versus 1.29. (Levinson et al., 2020) `ev:measured` p. 8 ^levinson2020analysis-051
- The original unsupervised depth and ego-motion model parameterizes the rotational component of camera pose with Euler angles. (Levinson et al., 2020) `ev:cited` p. 8 ^levinson2020analysis-052
- On KITTI single-view depth after 200K steps, SVD-Train performed best in 4 of the 7 metrics. (Levinson et al., 2020) `ev:measured` p. 9 ^levinson2020analysis-053
- On KITTI, SVD-Train reached the lowest squared relative error of 2.517, compared with 3.163 for the Euler angle default. (Levinson et al., 2020) `ev:measured` p. 9 ^levinson2020analysis-054
- On KITTI, differences between the best and second best rotation representations in each metric were small. (Levinson et al., 2020) `ev:measured` p. 9 ^levinson2020analysis-055
- The authors suggest driving motion is likely mostly planar, a case for which the axis-angle representation is well suited. (Levinson et al., 2020) `ev:asserted` p. 9 ^levinson2020analysis-056
- The default Euler angle selection of the original depth and ego-motion model is outperformed in every KITTI metric. (Levinson et al., 2020) `ev:measured` p. 9 ^levinson2020analysis-057
- The authors conclude that a 9D representation with SVD projection onto SO(3) is consistently effective and often state of the art. (Levinson et al., 2020) `ev:asserted` p. 9 ^levinson2020analysis-058
- For certain matrices Gram-Schmidt can have smaller error, for example zero error when the noise matrix is upper-triangular. (Levinson et al., 2020) `ev:computed` p. 13 ^levinson2020analysis-059
- Derived expected reconstruction errors were compared against numerical simulations using 100K trials per noise level as a sanity check. (Levinson et al., 2020) `ev:computed` p. 14 ^levinson2020analysis-060
- Training the first 100K steps with SVD-Inference before switching to SVD-Train yielded much smaller gradient norms afterwards. (Levinson et al., 2020) `ev:measured` p. 15 ^levinson2020analysis-061
- S2-Reg could not be trained successfully on any unsupervised rotation experiment, coming closest with mean test errors near 90 degrees. (Levinson et al., 2020) `ev:measured` p. 16 ^levinson2020analysis-062
- For uniform-rotation experiments, where K-means clustering was ineffective, MG quantized SO(3) by uniformly sampling 1000 rotations instead. (Levinson et al., 2020) `ev:reported` p. 16 ^levinson2020analysis-063
- Exponential learning rate decay made point cloud alignment evaluation smoother, but the comparative results stayed consistent with the main experiments. (Levinson et al., 2020) `ev:measured` p. 16 ^levinson2020analysis-064
- Training point cloud alignment with geodesic loss gave SVD-Train a mean error of 2.05 degrees versus 2.29 for 6D. (Levinson et al., 2020) `ev:measured` p. 17 ^levinson2020analysis-065
- The authors found no performance difference between MobileNet and VGG16 image embeddings for the image-based pose experiments. (Levinson et al., 2020) `ev:measured` p. 17 ^levinson2020analysis-066
- The authors noticed no measurable difference in training time with SVDO+, since a small 3 × 3 SVD is efficient. (Levinson et al., 2020) `ev:measured` p. 17 ^levinson2020analysis-067

## 🎯 Contributions

## 📖 Glossary

- **Symmetric orthogonalization** — Projection of a matrix onto the nearest orthogonal matrix, computed as UV^T from its SVD.
- **SVDO+** — Special orthogonalization via SVD that flips the last singular direction to land in SO(3).
- **SO(3)** — The group of 3D rotation matrices: orthogonal with determinant one.
- **Gram-Schmidt orthogonalization (GS+)** — Column-by-column orthonormalization; underlies the 6D rotation representation.
- **6D representation** — Two predicted 3D vectors mapped to a rotation through partial Gram-Schmidt.
- **SVD-Train** — Network trained with the loss applied after SVD projection onto SO(3).
- **SVD-Inference** — Network trained on the raw 9D matrix, projected with SVD only at test time.
- **Geodesic error** — Rotation angle of the relative rotation between prediction and ground truth.
- **Orthogonal Procrustes problem** — Finding the orthogonal matrix that best aligns two point sets in least squares.

## ❓ Open questions

- Does the Gaussian-noise error analysis predict relative performance when network output errors are far from i.i.d. Gaussian?
- Why does S2-Reg clearly beat SVD on Pascal3D+, and can SVD close the gap on viewpoint-biased real data?
- Would SVD-Inference pretraining followed by SVD-Train systematically improve convergence across tasks?
- How do SVD-based rotations interact with uncertainty or multimodal outputs for symmetric objects?
- Do the findings hold for larger networks or tasks where rotation is a larger share of the loss than in depth estimation?

## 📝 Notes on reading

Read the arXiv v1 preprint (2006.14616v1, 25 Jun 2020, marked Preprint. Under review), matching the packet identifier.

The Related Work text on p. 3 repeats a paragraph on SVD derivatives almost verbatim in the extracted text; this looks like a duplication in the preprint itself.

Tables 1, 2, 3, 5 and 6 combine a numeric table with two plots (mean error over training, error percentiles); only the numeric columns were claimed. Figure 1 (p. 14, simulated vs derived errors), Figure 2 (p. 16, gradient norms) and the learning-rate-decay curves of Table 8 (p. 17) could only be described. Several equations (e.g. Eq. 4, 7, 8, the det(M) ≠ 0 condition on p. 5) are garbled in the extraction; statements were taken from the surrounding prose.

The full per-category Pascal3D+ results (Table 9, p. 18) were not claimed cell by cell; only the mean and ranks from Table 4 were used.

## Suggested new concepts

- SVD orthogonalization for rotation regression — a recurring design choice for rotation outputs in pose and robotics networks.
- Continuous rotation representations — links this paper with the 6D and 5D representations and discontinuity arguments.
- Gram-Schmidt vs SVD projection — a comparison with a clean theoretical error ratio worth its own note.
- Rotation representation benchmarks — point cloud alignment, ModelNet, Pascal3D+, inverse kinematics and KITTI as a shared testbed.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Ortogonalización SVD (9D) como salida óptima para rotaciones.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
