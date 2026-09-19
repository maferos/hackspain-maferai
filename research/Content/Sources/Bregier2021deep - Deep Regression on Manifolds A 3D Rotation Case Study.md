---
aliases: []
type: "source"
title: "Deep Regression on Manifolds: A 3D Rotation Case Study"
citekey: "Bregier2021deep"
doi: "10.48550/arXiv.2103.16317"
arxiv: "2103.16317"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2103.16317"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Romain Brégier"]
sha256: ["885a06f91568ca50ea5e0835193578b2fcdae0055378ec95136023e18e33bfa7"]
pdf: "Content/Papers/Bregier2021deep.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Bregier2021deep.pdf]]

> [!abstract] One-sentence summary
> The paper sets out properties a differentiable mapping onto a manifold should have for deep regression, notably connected or convex pre-images, and shows on four 3D rotation tasks that special Procrustes orthonormalization generally performs best, with small-angle rotation vectors also suitable.

## Abstract

Many machine learning problems involve regressing variables on a non-Euclidean manifold -- e.g. a discrete probability distribution, or the 6D pose of an object. One way to tackle these problems through gradient-based learning is to use a differentiable function that maps arbitrary inputs of a Euclidean space onto the manifold. In this paper, we establish a set of desirable properties for such mapping, and in particular highlight the importance of pre-images connectivity/convexity. We illustrate these properties with a case study regarding 3D rotations. Through theoretical considerations and methodological experiments on a variety of tasks, we review various differentiable mappings on the 3D rotation space, and conjecture about the importance of their local linearity. We show that a mapping based on Procrustes orthonormalization generally performs best among the mappings considered, but that a rotation vector representation might also be suitable when restricted to small angles. (arXiv)

## 🧠 Key ideas (atomic)

- The author states that the choice of a mapping function onto the target manifold can significantly impact downstream task performance in deep learning. (Brégier, 2021) `ev:asserted` p. 1 ^bregier2021deep-001
- Discretizing the target space into classes may be unsatisfactory for precise regression because the number of required classes grows with manifold dimension. (Brégier, 2021) `ev:asserted` p. 1 ^bregier2021deep-002
- The paper focuses on differentiable mappings, functions included as ordinary network layers that map Euclidean feature vectors onto the target manifold. (Brégier, 2021) `ev:asserted` p. 1 ^bregier2021deep-003
- Zhou et al. stated that a mapping should be surjective and admit a continuous right inverse as a notion of continuity. (Brégier, 2021) `ev:cited` p. 2 ^bregier2021deep-004
- The author argues that a mapping sending every matrix outside SO(3) to the identity satisfies Zhou's criterion yet has null derivatives almost everywhere. (Brégier, 2021) `ev:asserted` p. 2 ^bregier2021deep-005
- The target space should be a connected differentiable manifold so that small gradient displacements can reach an arbitrary target from any starting point. (Brégier, 2021) `ev:asserted` p. 2 ^bregier2021deep-006
- The mapping should be surjective so that any arbitrary output on the target manifold can be predicted by the network. (Brégier, 2021) `ev:asserted` p. 2 ^bregier2021deep-007
- A Jacobian of full rank everywhere ensures that there is always a signal to back-propagate during training of the network. (Brégier, 2021) `ev:asserted` p. 2 ^bregier2021deep-008
- The author states that the full rank Jacobian guarantee may not be essential in high dimensions but is important in low dimensional regimes. (Brégier, 2021) `ev:asserted` p. 2 ^bregier2021deep-009
- The pre-image of every target element should be connected, or even better convex, to help generalization of the regression model. (Brégier, 2021) `ev:asserted` p. 2 ^bregier2021deep-010
- If training representations lie in disconnected regions of a pre-image, some interpolated test representations will necessarily not be mapped to the target. (Brégier, 2021) `ev:asserted` p. 2 ^bregier2021deep-011
- Pre-images convexity tends to help generalization by guaranteeing that linear interpolation between training representations produces the same prediction. (Brégier, 2021) `ev:asserted` p. 3 ^bregier2021deep-012
- The supplement proves that the closest point projection onto a manifold embedded in a Euclidean space satisfies pre-images connectivity. (Brégier, 2021) `ev:computed` p. 12 ^bregier2021deep-013
- Softmax is presented as a surjective differentiable mapping onto probability distributions whose pre-image of any distribution is a convex line. (Brégier, 2021) `ev:computed` p. 3 ^bregier2021deep-014
- The Euler angle mapping is surjective but does not satisfy pre-images connectivity in general because rotations have multiple discrete pre-images. (Brégier, 2021) `ev:asserted` p. 3 ^bregier2021deep-015
- The Jacobian of the Euler angle mapping suffers from rank deficiency for some rotations, a phenomenon referred to as gimbal lock. (Brégier, 2021) `ev:asserted` p. 3 ^bregier2021deep-016
- The rotation vector mapping through the exponential map suffers from rank deficiency for input rotation vectors of angle 2πk. (Brégier, 2021) `ev:asserted` p. 3 ^bregier2021deep-017
- Restricting the rotation vector mapping to an open ball of radius below π satisfies all the properties, suiting it to limited-angle rotations. (Brégier, 2021) `ev:asserted` p. 3 ^bregier2021deep-018
- The non-zero quaternion mapping satisfies all properties except pre-images connectivity, since each pre-image consists of all nonzero scalar multiples of a quaternion. (Brégier, 2021) `ev:asserted` p. 3 ^bregier2021deep-019
- The Procrustes mapping projects an arbitrary matrix to the closest rotation matrix under the Frobenius norm using a singular value decomposition. (Brégier, 2021) `ev:reported` p. 3 ^bregier2021deep-020
- The supplement proves that the pre-image of any rotation under special Procrustes orthonormalization is a convex set of matrices. (Brégier, 2021) `ev:computed` p. 14 ^bregier2021deep-021
- The author states that Procrustes mapping can be implemented efficiently for batched GPU applications using off-the-shelf SVD cuSOLVER routines. (Brégier, 2021) `ev:asserted` p. 4 ^bregier2021deep-022
- The 6D Gram-Schmidt mapping of Zhou et al. can be expressed as a degenerate limit case of Procrustes orthonormalization. (Brégier, 2021) `ev:computed` p. 4 ^bregier2021deep-023
- The 6D mapping gives importance almost exclusively to the first column of its input matrix, unlike the Procrustes mapping. (Brégier, 2021) `ev:asserted` p. 4 ^bregier2021deep-024
- Zhou et al. showed that compressing the 6D representation into a 5D one through stereographic projection led to worse training performance. (Brégier, 2021) `ev:cited` p. 4 ^bregier2021deep-025
- Peretroukhin et al. proposed to regress 3D rotations as a list of 10 coefficients of a 4×4 symmetric matrix. (Brégier, 2021) `ev:cited` p. 4 ^bregier2021deep-026
- The supplement proves that the pre-image set of the symmetric matrix mapping is convex for any rotation it represents. (Brégier, 2021) `ev:computed` p. 16 ^bregier2021deep-027
- The paper releases RoMa, an easy-to-use and efficient PyTorch library for rotation manipulation intended to ease deep learning experiments. (Brégier, 2021) `ev:reported` p. 5 ^bregier2021deep-028
- Euler angles were excluded from the experiments because many different conventions would have had to be considered in the evaluation. (Brégier, 2021) `ev:reported` p. 5 ^bregier2021deep-029
- The symmetric matrix mapping was excluded from experiments because its implementation was found too slow for extensive evaluations. (Brégier, 2021) `ev:reported` p. 5 ^bregier2021deep-030
- The point cloud alignment network uses two Siamese naive PointNets whose concatenated features pass through a multi-layer perceptron to a mapping. (Brégier, 2021) `ev:reported` p. 5 ^bregier2021deep-031
- Point cloud alignment uses ShapeNet airplanes, with a random validation set of 400 point clouds taken from the original training set. (Brégier, 2021) `ev:reported` p. 5 ^bregier2021deep-032
- Each point cloud alignment variant was trained and tested 5 times to mitigate the variance caused by the stochastic nature of training. (Brégier, 2021) `ev:reported` p. 5 ^bregier2021deep-033
- On point cloud alignment, Procrustes achieved the lowest best-validation mean angular error of 2.90°, against 3.01° for the 6D mapping. (Brégier, 2021) `ev:measured` p. 5 ^bregier2021deep-034
- Rotation vector and quaternion mappings reached best-validation angular errors of 12.74° and 11.66°, significantly worse than the other mappings tested. (Brégier, 2021) `ev:measured` p. 5 ^bregier2021deep-035
- The author states the difference in average final error between Procrustes and 6D is too small to draw clear conclusions given run deviations. (Brégier, 2021) `ev:measured` p. 5 ^bregier2021deep-036
- Orthonormalizing at both training and test time performed better than regressing a raw matrix and orthonormalizing only at test time. (Brégier, 2021) `ev:measured` p. 5 ^bregier2021deep-037
- Training without orthonormalization gave smaller final error variance, with a maximum deviation of 0.18° for Matrix/Procrustes versus 0.91° for Procrustes. (Brégier, 2021) `ev:measured` p. 5 ^bregier2021deep-038
- The inverse kinematics task trains a multi-layer perceptron to regress 57 joint rotations of a human skeleton through a known forward kinematics function. (Brégier, 2021) `ev:reported` p. 6 ^bregier2021deep-039
- Inverse kinematics experiments use CMU MoCap data, with each variant trained under 5 different random weight initializations. (Brégier, 2021) `ev:reported` p. 6 ^bregier2021deep-040
- On inverse kinematics, Procrustes reached a best-validation mean per joint position error of 0.721cm, versus 0.796cm for the 6D mapping. (Brégier, 2021) `ev:measured` p. 6 ^bregier2021deep-041
- On inverse kinematics, quaternion and rotation vector mappings reached best-validation mean per joint position errors of 1.948cm and 1.695cm. (Brégier, 2021) `ev:measured` p. 6 ^bregier2021deep-042
- The author notes the rotation part of the original PoseNet loss is biased because antipodal unit quaternions represent the same rotation. (Brégier, 2021) `ev:asserted` p. 6 ^bregier2021deep-043
- PoseNet variants are evaluated on the Cambridge Landmarks datasets, reporting median camera position and orientation errors for each mapping. (Brégier, 2021) `ev:reported` p. 6 ^bregier2021deep-044
- A single camera localization result is reported per mapping because pre-trained weights and deterministic seeding gave negligible variance across trainings. (Brégier, 2021) `ev:reported` p. 6 ^bregier2021deep-045
- The baseline quaternion mapping trained with the original PoseNet loss reached mean errors of 2.07m and 6.74° on Cambridge Landmarks. (Brégier, 2021) `ev:measured` p. 7 ^bregier2021deep-046
- The quaternion mapping trained with the corrected quaternion loss performed worse on average, with mean errors of 2.15m and 7.63°. (Brégier, 2021) `ev:measured` p. 7 ^bregier2021deep-047
- The author conjectures the corrected loss might push outputs for nearby orientations towards opposite regions, relating to disconnected quaternion pre-images. (Brégier, 2021) `ev:asserted` p. 7 ^bregier2021deep-048
- For each Cambridge Landmarks dataset, more than 99% of ground truth quaternions are oriented in the same half-space. (Brégier, 2021) `ev:measured` p. 7 ^bregier2021deep-049
- Procrustes results were globally better than 6D or quaternion results for both the quaternion loss and the Frobenius loss. (Brégier, 2021) `ev:measured` p. 7 ^bregier2021deep-050
- With the quaternion loss, Procrustes reached mean errors of 1.84m and 6.53°, better on average than the original PoseNet baseline. (Brégier, 2021) `ev:measured` p. 7 ^bregier2021deep-051
- The rotation vector mapping achieved the best average results with the Frobenius loss, with mean errors of 1.85m and 6.30°. (Brégier, 2021) `ev:measured` p. 7 ^bregier2021deep-052
- The author conjectures rotation vector success might partly be due to target rotations typically lying less than 90° away from the identity. (Brégier, 2021) `ev:asserted` p. 7 ^bregier2021deep-053
- Applying a 180° rotation before the quaternion loss made rotation vector training fail to converge, with a mean orientation error of 150.57°. (Brégier, 2021) `ev:measured` p. 7 ^bregier2021deep-054
- Object orientation is regressed from LINEMOD image crops with a pre-trained ResNet-50 backbone trained on 200,000 synthetic crops per object. (Brégier, 2021) `ev:reported` p. 7 ^bregier2021deep-055
- The author states the object pose setup cannot reach state-of-the-art performance since it uses no real data, physically-based renderings or data-augmentation. (Brégier, 2021) `ev:asserted` p. 7 ^bregier2021deep-056
- On LINEMOD object orientation, Procrustes reached the lowest mean normalized RMS error of 0.080, against 0.084 for the 6D mapping. (Brégier, 2021) `ev:measured` p. 8 ^bregier2021deep-057
- On LINEMOD object orientation, quaternion and rotation vector mappings gave higher mean normalized RMS errors of 0.116 and 0.120. (Brégier, 2021) `ev:measured` p. 8 ^bregier2021deep-058
- Regressing an unconstrained matrix gave worse object pose errors, though Matrix/Procrustes at 0.135 still beat Matrix/Gram-Schmidt at 0.160. (Brégier, 2021) `ev:measured` p. 8 ^bregier2021deep-059
- Concurrent work argues that Procrustes orthonormalization is less sensitive to Gaussian noise than Gram-Schmidt, though only for local perturbations. (Brégier, 2021) `ev:cited` p. 8 ^bregier2021deep-060
- The author proposes that the Procrustes mapping is more linear than the 6D and quaternion mappings for typical input ranges. (Brégier, 2021) `ev:asserted` p. 8 ^bregier2021deep-061
- Numerical deviation-from-linearity tests with random normal inputs show better linearity of Procrustes compared to the quaternion and 6D mappings. (Brégier, 2021) `ev:computed` p. 8 ^bregier2021deep-062
- Defining the loss on the manifold during training performed better than regressing a representation mapped to the manifold only at test time. (Brégier, 2021) `ev:measured` p. 8 ^bregier2021deep-063
- The linearity plot suggests that a tanh-scaled rotation vector mapping to angles below π/2 has linearity similar to Procrustes. (Brégier, 2021) `ev:computed` p. 8 ^bregier2021deep-064
- The author concludes Procrustes performs best for arbitrary rotations, while rotation vector representations may be as suitable for limited rotation angles. (Brégier, 2021) `ev:asserted` p. 8 ^bregier2021deep-065
- On a toy torus regression task, the atan2 mapping reached a mean test error of 1.9 versus 21 for the identity mapping. (Brégier, 2021) `ev:measured` p. 10 ^bregier2021deep-066
- The identity mapping on the torus suffered severe overfitting, with a test position error more than 4 times higher than on training. (Brégier, 2021) `ev:measured` p. 10 ^bregier2021deep-067

## 🎯 Contributions


## 📖 Glossary

- **Differentiable mapping** — A layer function mapping Euclidean network outputs onto a target manifold, trainable by back-propagation.
- **Pre-image** — The set of inputs a mapping sends to one given output element.
- **SO(3)** — The group of 3D rotations, not homeomorphic to a Euclidean space.
- **Special Procrustes orthonormalization** — Projection of a matrix to its closest rotation matrix under Frobenius norm, via SVD.
- **6D mapping** — Zhou et al.'s mapping of a two-column matrix to a rotation by Gram-Schmidt orthonormalization.
- **Rotation vector** — Axis-angle representation mapped to rotations through the exponential map.
- **Gimbal lock** — Loss of Jacobian rank of Euler angle parameterizations at some rotations.
- **Full rank Jacobian** — Jacobian rank equals manifold dimension everywhere, so gradients can always move the output.

## ❓ Open questions

- Does the proposed local linearity of a mapping causally explain performance, or only correlate with it on these tasks?
- Can the pre-images connectivity/convexity criteria be quantified rather than treated as binary properties?
- How do the mappings compare on symmetric objects, which the object pose experiment excluded?
- Would a faster implementation of the symmetric matrix mapping change the ranking among mappings?
- How much of the rotation vector success in camera localization is due to weight initialization rather than the small-angle range?
- Do the conclusions transfer to manifolds with boundaries or corners, which are declared out of scope?

## 📝 Notes on reading

Version read: arXiv 2103.16317v2 (12 Oct 2021), including the supplementary material on pages 10-17; it matches the packet identifier. Table 1 (p. 3), which summarizes which properties each SO(3) mapping satisfies, lost its check marks in extraction; its content was claimed only from the prose of section 3. Likewise the connected/convex pre-image check marks in figure 1 (p. 4) were lost. Table 2 and table 3 deviation subscripts/exponents are partly garbled (e.g. the rotation vector inverse kinematics average final error prints as 1.8400.102), so only best-validation values were claimed. Figures 2, 3 and 4 are cumulative error or linearity curves described only in text. The Table 4 camera localization row values were claimed only for the Mean row. The supplement refers to hyperparameters of equation (10) of the paper for inverse kinematics, but the main text's inverse kinematics loss is unnumbered. The object pose supplement states 85% of crops are used for testing and 15% for validation. The torus errors are in units of 10^-2 as printed in the supplement table header.

## Suggested new concepts

- Pre-images connectivity/convexity — a general design criterion for output mappings in manifold regression, beyond rotations.
- Rotation representations for deep learning — hub comparing Euler, quaternion, rotation vector, 6D and Procrustes mappings across papers.
- Special Procrustes orthonormalization — widely used SVD-based rotation mapping with proven convex pre-images.
- Mapping linearity — proposed additional factor for trainability of manifold-valued outputs.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Propiedades deseables de las aplicaciones $\mathbb{R}^k\to SO(3)$; librería RoMa.
