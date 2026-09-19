---
aliases: []
type: "source"
title: "Learning with 3D rotations, a hitchhiker's guide to SO(3)"
citekey: "Geist2024learning"
doi: "10.48550/arXiv.2404.11735"
arxiv: "2404.11735"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2404.11735"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["A. René Geist", "Jonas Frey", "Mikel Zhobro", "Anna Levina", "Georg Martius"]
sha256: ["9e2e21a102a627b7e1f56c0331ced71b83d8a2269e95535b2c33c90f4d6f4d65"]
pdf: "Content/Papers/Geist2024learning.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Geist2024learning.pdf]]

> [!abstract] One-sentence summary
> A survey and guide showing, through Lipschitz-continuity arguments and four experiments, that continuous high-dimensional rotation representations (R9+SVD, R6+GSO) should be the default for neural network regression, with half-space quaternions viable only for small angles or under memory limits.

## Abstract

Many settings in machine learning require the selection of a rotation representation. However, choosing a suitable representation from the many available options is challenging. This paper acts as a survey and guide through rotation representations. We walk through their properties that harm or benefit deep learning with gradient-based optimization. By consolidating insights from rotation-based learning, we provide a comprehensive overview of learning functions with rotation representations. We provide guidance on selecting representations based on whether rotations are in the model's input or output and whether the data primarily comprises small angles. (arXiv)

## 🧠 Key ideas (atomic)

- The paper surveys rotation representations and examines which of their properties harm or benefit deep learning with gradient-based optimization. (Geist et al., 2024) `ev:asserted` p. 1 ^geist2024learning-001
- Earlier works suggest that rotation representations with four or fewer dimensions do not facilitate sample-efficient learning. (Geist et al., 2024) `ev:cited` p. 1 ^geist2024learning-002
- The authors find that high-dimensional representations should be the preferred default choice from both a theoretical and an empirical perspective. (Geist et al., 2024) `ev:asserted` p. 1 ^geist2024learning-003
- The problem setting is gradient-based supervised neural network regression, assuming a deterministic target function that generated the data. (Geist et al., 2024) `ev:reported` p. 2 ^geist2024learning-004
- Representing a 2D rotation by a single angle creates a jump in the map g, which the cosine and sine pair avoids. (Geist et al., 2024) `ev:asserted` p. 2 ^geist2024learning-005
- Table 1 lists Euler angles, exponential coordinates, unit quaternions, and axis-angle as having a [[Rotation representation continuity|discontinuous map g]] from SO(3). (Geist et al., 2024) `ev:reported` p. 2 ^geist2024learning-006
- Studies on learning with rotations uniformly discourage the use of Euler angles when learning with 3D rotations. (Geist et al., 2024) `ev:cited` p. 3 ^geist2024learning-007
- Unit quaternions double cover SO(3), with a quaternion q and its negative -q mapping to the same rotation. (Geist et al., 2024) `ev:reported` p. 3 ^geist2024learning-008
- The SVD projection solves the orthogonal Procrustes problem, projecting the predicted matrix onto the nearest rotation matrix in SO(3). (Geist et al., 2024) `ev:asserted` p. 6 ^geist2024learning-009
- Cosine distance and angular distance are pseudo-metrics, as they violate identity by ignoring the length of the vectors. (Geist et al., 2024) `ev:asserted` p. 4 ^geist2024learning-010
- The Chordal distance, the Frobenius norm of the difference between rotation matrices, is often used for its numerical stability and computational efficiency. (Geist et al., 2024) `ev:asserted` p. 4 ^geist2024learning-011
- For rotation estimation, the target function composes g with the true map, so discontinuities or double representations in g can transfer to it. (Geist et al., 2024) `ev:asserted` p. 4 ^geist2024learning-012
- SO(3) is not homeomorphic to any subset of 4D Euclidean space, so representations with four or fewer dimensions have a discontinuous g. (Geist et al., 2024) `ev:cited` p. 5 ^geist2024learning-013
- Random sampling in Figure 6 shows that, for low-dimensional representations, small distances in SO(3) can lead to near-maximal representation distances. (Geist et al., 2024) `ev:computed` p. 5 ^geist2024learning-014
- Double cover makes g discontinuous, so the shortest distance between representation vectors need not match the shortest distance in SO(3). (Geist et al., 2024) `ev:asserted` p. 5 ^geist2024learning-015
- The [[Rotation representation continuity|discontinuities]] imply points in feature space where the target function's Lipschitz constant blows up, which also blows up the loss gradient. (Geist et al., 2024) `ev:asserted` p. 5 ^geist2024learning-016
- Representing angles as cosine and sine helps for SO(2) but does not remove SO(3) discontinuities arising from double cover. (Geist et al., 2024) `ev:asserted` p. 5 ^geist2024learning-017
- The authors conclude that changing the loss, via distance picking or distances computed in SO(3), does not fix double-cover discontinuities. (Geist et al., 2024) `ev:asserted` p. 6 ^geist2024learning-018
- Mapping quaternions to one half-space still leaves vectors near the separating hyperplane far apart in representation space although close in SO(3). (Geist et al., 2024) `ev:asserted` p. 6 ^geist2024learning-019
- For small rotations near the identity, a half-space map is a valid fix as no discontinuities are seen during training. (Geist et al., 2024) `ev:cited` p. 6 ^geist2024learning-020
- Levinson et al. found that training near matrices with zero determinant increases gradient magnitude but does not notably impede training. (Geist et al., 2024) `ev:cited` p. 6 ^geist2024learning-021
- R6+GSO can be seen as a degenerate Procrustes problem in which the first vector has by far the strongest influence on the rotation. (Geist et al., 2024) `ev:cited` p. 6 ^geist2024learning-022
- Earlier studies and the authors' own experiments confirm that R9+SVD often outperforms R6+GSO in rotation estimation. (Geist et al., 2024) `ev:measured` p. 7 ^geist2024learning-023
- Levinson et al. attribute the advantage of R9+SVD to Gaussian noise causing twice the expected rotation error for R6+GSO. (Geist et al., 2024) `ev:cited` p. 7 ^geist2024learning-024
- The authors interpret the SVD layer as an ensemble where three column predictions contribute equally, whereas R6+GSO relies almost fully on one. (Geist et al., 2024) `ev:asserted` p. 7 ^geist2024learning-025
- Over 20000 randomly initialized representations, loss gradient ratios stay notably closer to one for R9+SVD than for R6+GSO. (Geist et al., 2024) `ev:computed` p. 7 ^geist2024learning-026
- The authors conclude that considerably more sampled representations exhibit gradients that impede training with R6+GSO than with R9+SVD. (Geist et al., 2024) `ev:computed` p. 7 ^geist2024learning-027
- For rotation estimation, the authors recommend using the R9+SVD or R6+GSO representation in gradient-based neural network regression. (Geist et al., 2024) `ev:asserted` p. 7 ^geist2024learning-028
- If the regression targets are only small rotations, quaternions with a half-space map are described as a good option. (Geist et al., 2024) `ev:asserted` p. 7 ^geist2024learning-029
- The authors find that directly predicting rotation matrix entries is worse than Procrustes-based methods, hypothesizing a cause in the loss gradients. (Geist et al., 2024) `ev:measured` p. 7 ^geist2024learning-030
- Low-dimensional representations and the half-space map introduce a boundary, leaving fewer samples near it for generalization in feature prediction. (Geist et al., 2024) `ev:asserted` p. 8 ^geist2024learning-031
- The authors propose data augmentation that creates samples beyond the boundary as a simple trick for low-dimensional feature prediction. (Geist et al., 2024) `ev:asserted` p. 8 ^geist2024learning-032
- For feature prediction, the authors recommend R9+SVD or R6+GSO, with augmented half-space quaternions viable under memory constraints. (Geist et al., 2024) `ev:asserted` p. 8 ^geist2024learning-033
- In Experiment 1, a network predicts the rotation aligning two point clouds of 3000 points, following the pipeline of Levinson et al. (Geist et al., 2024) `ev:reported` p. 8 ^geist2024learning-034
- Point clouds come from 726 airplane CAD models under uniformly sampled SO(3) rotations, with 100 pairs held out for testing. (Geist et al., 2024) `ev:reported` p. 8 ^geist2024learning-035
- In the point cloud alignment experiment, R9+SVD achieved the best test results among the representations, followed by R6+GSO. (Geist et al., 2024) `ev:measured` p. 8 ^geist2024learning-036
- For quaternions in point cloud alignment, a half-space map notably improved performance, whereas distance picking reduced it. (Geist et al., 2024) `ev:measured` p. 8 ^geist2024learning-037
- In estimating cube orientation from rendered images, R9+SVD and R6+GSO performed notably better than low-dimensional representations. (Geist et al., 2024) `ev:measured` p. 8 ^geist2024learning-038
- In rendering a cube image from its rotation representation, R9+SVD performed notably better than R6+GSO. (Geist et al., 2024) `ev:measured` p. 8 ^geist2024learning-039
- In the cube rendering task, quaternions benefited from deploying a half-space map on their representation. (Geist et al., 2024) `ev:measured` p. 8 ^geist2024learning-040
- On YCB-Video 6D pose estimation, Euler angles performed notably worse than R9+SVD and R6+GSO, averaged over 21 objects and three seeds. (Geist et al., 2024) `ev:measured` p. 9 ^geist2024learning-041
- On YCB-Video pose estimation, quaternions performed similarly to R9+SVD and R6+GSO when retraining the network of Wang et al. (Geist et al., 2024) `ev:measured` p. 9 ^geist2024learning-042
- The authors hypothesize that quaternions perform well on [[YCB-Video dataset|YCB-Video]] because the dataset mostly contains small angles. (Geist et al., 2024) `ev:asserted` p. 9 ^geist2024learning-043
- Averaged over all YCB-Video objects, the ADD-S AUC was 90.8 for Euler angles versus 91.2 for R6+GSO. (Geist et al., 2024) `ev:measured` p. 18 ^geist2024learning-044
- In Experiment 4, the target is a Fourier series of a random MLP of the rotation, fitted by an MLP taking a rotation representation. (Geist et al., 2024) `ev:reported` p. 9 ^geist2024learning-045
- Each setting used 100 target functions, with 800, 200, and 1000 points for training, validation, and test. (Geist et al., 2024) `ev:reported` p. 9 ^geist2024learning-046
- As the number of Fourier basis functions increases, target functions become more wiggly on average and model MSEs increase. (Geist et al., 2024) `ev:measured` p. 9 ^geist2024learning-047
- Quaternion augmentation with threshold 0.1 had a notable effect for one to three Fourier basis functions. (Geist et al., 2024) `ev:measured` p. 9 ^geist2024learning-048
- The authors conclude that three- or four-parameter representations impede learning by inevitably introducing [[Rotation representation continuity|discontinuities]] when rotations are the model output. (Geist et al., 2024) `ev:asserted` p. 9 ^geist2024learning-049
- When rotations appear in the inputs of the regression task, the authors conclude that [[Rotation representation continuity|discontinuities]] do not hinder learning. (Geist et al., 2024) `ev:asserted` p. 9 ^geist2024learning-050
- The symmetric-matrix representation of Peretroukhin et al. outperformed R6+GSO on various benchmarks, according to the authors' review. (Geist et al., 2024) `ev:cited` p. 9 ^geist2024learning-051
- A representation with 3 instead of 9 parameters may significantly reduce memory consumption, the authors note. (Geist et al., 2024) `ev:asserted` p. 13 ^geist2024learning-052
- The CMU MoCap inverse kinematics data contains significantly more small rotations close to the identity, reducing singularity effects for low-dimensional representations. (Geist et al., 2024) `ev:measured` p. 14 ^geist2024learning-053
- The authors did not reproduce the CMU MoCap inverse kinematics experiment because the dataset mostly contains angles close to the unit rotation. (Geist et al., 2024) `ev:reported` p. 18 ^geist2024learning-054
- Occluded or [[Pose ambiguity from symmetry|symmetric objects]] may make the rotation learning problem ill-posed, as pointed out by Saxena et al. (Geist et al., 2024) `ev:cited` p. 15 ^geist2024learning-055
- On an Nvidia RTX3060, the GPU-based R9+SVD mapping takes around 0.5 ms for a batch size of 1. (Geist et al., 2024) `ev:measured` p. 16 ^geist2024learning-056
- The authors conclude that the compute overhead of R9+SVD over R6+GSO is small for most applications. (Geist et al., 2024) `ev:asserted` p. 16 ^geist2024learning-057
- In the cube image experiments, the authors report continuous representations strongly outperforming quaternion, exponential coordinate, and Euler angle representations. (Geist et al., 2024) `ev:measured` p. 17 ^geist2024learning-058
- For quaternions in the cube experiment, mapping to R9 with geodesic or Chordal losses beat cosine distance and distance-picking MSE. (Geist et al., 2024) `ev:measured` p. 17 ^geist2024learning-059
- For R9 and R6, training on the geodesic distance led to better performance even when the Chordal distance is evaluated. (Geist et al., 2024) `ev:measured` p. 17 ^geist2024learning-060
- Cube experiments used 2048 image and rotation pairs rendered in MuJoCo at 64 × 64, reporting metrics across 10 random seeds. (Geist et al., 2024) `ev:reported` p. 17 ^geist2024learning-061
- Resorting to the MAE loss can improve results for low-dimensional representations such as quaternions, Euler angles, and exponential coordinates. (Geist et al., 2024) `ev:measured` p. 19 ^geist2024learning-062

## 🎯 Contributions

## 📖 Glossary

- **SO(3)** — The group of 3D rotation matrices: orthogonal with determinant one.
- **Rotation representation** — A vector space R with maps g from SO(3) and f back, f left-inverse of g.
- **Double cover** — Every rotation is represented by two distinct representation vectors, e.g. q and -q.
- **R6+GSO** — Two predicted 3D vectors completed to a rotation matrix by Gram-Schmidt orthonormalization.
- **R9+SVD** — A predicted 3×3 matrix projected to the nearest rotation via singular value decomposition.
- **Chordal distance** — Frobenius norm of the difference between two rotation matrices.
- **Geodesic distance** — Rotation angle of R1 R2 transposed, the arc-length distance in SO(3).
- **Half-space map** — Restricting quaternions to one hemisphere (non-negative scalar part) to remove double cover.
- **Distance picking** — Loss taking the minimum distance over a representation and its double-cover twin.
- **Rotation estimation** — Learning a map from features (images, point clouds) to a rotation representation.
- **Feature prediction** — Learning a map from a rotation representation to object features or properties.
- **Lipschitz continuity** — Bounded ratio of output change to input change, used to quantify continuity.

## ❓ Open questions

- How close must data stay to the identity for half-space quaternions to match R9+SVD in rotation estimation?
- Do geometric algebra representations (rotors, bi-vectors) differ in practice once errors are measured in SO(3) and half-space maps are applied?
- Why does training on the geodesic distance beat the Chordal loss even when Chordal distance is the evaluation metric?
- How do forward-dynamics models keep predicted rotations near the SO(3) manifold over long rollouts with high-dimensional representations?
- Does the curse of dimensionality affect higher-dimensional rotation representations, given that SO(3) is a 3D manifold in R9?

## 📝 Notes on reading

Version read: arXiv 2404.11735v2 (19 Jun 2024), matching the packet identifier.

Figures 6, 10, 11, 13, 14, 15, 16, 18–24 are plots whose values were only described in the text; box-plot error values in Figures 13, 14, 23, 24 were not claimed. Figure 14 (right) also mentions that quaternion augmentation slightly reduces rendering error.

Equations were garbled by extraction (e.g. the SVD+ projection, Frobenius norm, Fourier series target (16)); none were claimed as numbers. Table 2 (per-object YCB-Video results) extracted cleanly; only the All objects row was claimed (Euler 90.8, R6+GSO 91.2, R9+SVD 91.1, Quat 91.2 AUC; <2 cm: 93.3, 94.7, 94.6, 94.7).

Inconsistencies inside the paper: the triangle inequality on p. 3 is printed as d(y1,y3)+d(y3,y1); Eq. (15) is printed as ∥vec(R), f(r)∥; Appendix D.2 says the quaternion augmentation improves learning with rotations in the model's output, whereas the main text uses it for feature prediction (rotations as input); Figure 16 reports MSE while Appendix E.4 says RMSE was used for train, validation and test loss; Figure 23 caption says Quat-RF errors were four to seven times larger, Figure 24 caption says four to six times.

Appendix D.7 notes CPU SVD implementations can reach 0.002 ms, and compares 200 ms ResNet152 to 2 ms SVD at batch 1024.

## Suggested new concepts

- Rotation representation continuity — a recurring criterion across Zhou, Levinson, Brégier and this paper for choosing network rotation outputs.
- Double cover — the central cause of discontinuity for quaternions, axis-angle and exponential coordinates in learning.
- Half-space map — a cheap fix valid for small-angle data and feature prediction, relevant to robot pose and dynamics data.
- R9+SVD rotation layer — the recommended default rotation output layer, likely reused across pose-estimation work.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Guía práctica: qué representación usar en entradas vs. salidas.
