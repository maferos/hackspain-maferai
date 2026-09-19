---
aliases: []
type: "source"
title: "On the Continuity of Rotation Representations in Neural Networks"
citekey: "Zhou2019continuity"
doi: "10.48550/arXiv.1812.07035"
arxiv: "1812.07035"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1812.07035"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Yi Zhou", "Connelly Barnes", "Jingwan Lu", "Jimei Yang", "Hao Li"]
sha256: ["369c6c54101ce827b2ef84ff5bbea91fe5209ffd2749c158532d06bf4eed0633"]
pdf: "Content/Papers/Zhou2019continuity.pdf"
topics: ["[[Matemáticas]]", "[[Optimización y algoritmos]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]", "[[02_optimizacion_y_algoritmos]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Zhou2019continuity.pdf]]

> [!abstract] One-sentence summary
> The paper defines continuity of rotation representations for neural networks, proves that all 3D rotation representations in four or fewer dimensions are discontinuous, and shows that continuous 6D and 5D representations learn with lower errors in autoencoder, point cloud pose and inverse kinematics tests.

## Abstract

In neural networks, it is often desirable to work with various representations of the same space. For example, 3D rotations can be represented with quaternions or Euler angles. In this paper, we advance a definition of a continuous representation, which can be helpful for training deep neural networks. We relate this to topological concepts such as homeomorphism and embedding. We then investigate what are continuous and discontinuous representations for 2D, 3D, and n-dimensional rotations. We demonstrate that for 3D rotations, all representations are discontinuous in the real Euclidean spaces of four or fewer dimensions. Thus, widely used representations such as quaternions and Euler angles are discontinuous and difficult for neural networks to learn. We show that the 3D rotations have continuous representations in 5D and 6D, which are more suitable for learning. We also present continuous representations for the general case of the n-dimensional rotation group SO(n). While our main focus is on rotations, we also show that our constructions apply to other groups such as the orthogonal group and similarity transforms. We finally present empirical results, which show that our continuous rotation representations outperform discontinuous ones for several practical problems in graphics and vision, including a simple autoencoder sanity test, a rotation estimator for 3D point clouds, and an inverse kinematics solver for 3D human poses. (arXiv)

## 🧠 Key ideas (atomic)

- Many prior works regress 3D rotations with 3D or 4D representations such as quaternions, axis-angles, or Euler angles. (Zhou et al., 2019) `ev:cited` p. 1 ^zhou2019continuity-001
- Empirically, converged networks using 3D and 4D rotation representations still produce large errors at certain rotation angles, the authors found. (Zhou et al., 2019) `ev:measured` p. 1 ^zhou2019continuity-002
- The authors believe these large errors point to deeper topological problems related to continuity in the rotation representations. (Zhou et al., 2019) `ev:asserted` p. 1 ^zhou2019continuity-003
- Theoretical results suggest that smoother functions have lower approximation error for a given number of neurons in neural networks. (Zhou et al., 2019) `ev:cited` p. 1 ^zhou2019continuity-004
- Llanas et al. noted that piecewise continuous functions trained with gradient descent require many neurons and iterations yet give poor results. (Zhou et al., 2019) `ev:cited` p. 2 ^zhou2019continuity-005
- PoseCNN reported a high percentage of rotation errors between 90 and 180 degrees, attributing them mainly to symmetric shapes. (Zhou et al., 2019) `ev:cited` p. 2 ^zhou2019continuity-006
- The authors argue that discontinuity in quaternion or axis-angle representations could be one cause of such pose estimation errors. (Zhou et al., 2019) `ev:asserted` p. 2 ^zhou2019continuity-007
- Csiszar et al. limited rotation angles to a range that avoided the discontinuity points, achieving very low joint alignment errors. (Zhou et al., 2019) `ev:cited` p. 2 ^zhou2019continuity-008
- The authors argue [[Rotation representation continuity|continuous rotation representations]] are a better choice when real-world tasks require networks to output the full range of rotations. (Zhou et al., 2019) `ev:asserted` p. 2 ^zhou2019continuity-009
- A pair of mappings (f, g) is called a representation when f is a left inverse of g on the original space. (Zhou et al., 2019) `ev:asserted` p. 3 ^zhou2019continuity-010
- The paper calls a representation continuous when the mapping g from the original space to the representation space is continuous. (Zhou et al., 2019) `ev:asserted` p. 3 ^zhou2019continuity-011
- Representing 2D rotations by an angle in [0, 2π] is discontinuous at the identity, where directional limits give 0 and 2π. (Zhou et al., 2019) `ev:computed` p. 3 ^zhou2019continuity-012
- Representing a 2D rotation by its first column vector [cos(θ), sin(θ)] would give a continuous representation, according to the authors. (Zhou et al., 2019) `ev:asserted` p. 3 ^zhou2019continuity-013
- The authors argue that [[Rotation representation continuity|discontinuous representations]] can be harder for neural networks to fit than continuous representations. (Zhou et al., 2019) `ev:asserted` p. 3 ^zhou2019continuity-014
- The representation space is required to have Euclidean topology, consistent with the continuity of the neural network units. (Zhou et al., 2019) `ev:asserted` p. 3 ^zhou2019continuity-015
- For a continuous representation, g restricted to its image is a homeomorphism, so g topologically embeds the original space. (Zhou et al., 2019) `ev:computed` p. 3 ^zhou2019continuity-016
- If the original space is not homeomorphic to any subset of the representation space, no continuous representation exists. (Zhou et al., 2019) `ev:computed` p. 3 ^zhou2019continuity-017
- The Euler angle representation of 3D rotations is discontinuous at the identity, where azimuth directional limits give 0 and 2π. (Zhou et al., 2019) `ev:computed` p. 4 ^zhou2019continuity-018
- The quaternion representation is discontinuous at 180 degree rotations, where one branch of the mapping approaches the zero vector. (Zhou et al., 2019) `ev:computed` p. 4 ^zhou2019continuity-019
- The axis in the axis-angle representation has discontinuities at the 180 degree rotations, the authors show in a similar way. (Zhou et al., 2019) `ev:computed` p. 4 ^zhou2019continuity-020
- By embedding results in topology, RP3, and thus SO(3), embeds in R5 but not in Rd for d < 5. (Zhou et al., 2019) `ev:cited` p. 4 ^zhou2019continuity-021
- The authors conclude that no [[Rotation representation continuity|continuous representation of 3D rotations]] exists in real Euclidean spaces of four or fewer dimensions. (Zhou et al., 2019) `ev:computed` p. 4 ^zhou2019continuity-022
- The proposed continuous representation of SO(n) simply drops the last column vector of the n × n rotation matrix. (Zhou et al., 2019) `ev:asserted` p. 4 ^zhou2019continuity-023
- The mapping back to SO(n) is a Gram-Schmidt-like process whose last column is a generalized cross product. (Zhou et al., 2019) `ev:asserted` p. 5 ^zhou2019continuity-024
- For 3D rotations this construction gives a 6D representation, with the last column computed as the ordinary cross product. (Zhou et al., 2019) `ev:computed` p. 5 ^zhou2019continuity-025
- Using the 6D representation in a network can be beneficial because the mapping ensures the resulting 3x3 matrix is orthogonal. (Zhou et al., 2019) `ev:asserted` p. 5 ^zhou2019continuity-026
- With in-network orthogonalization, a 3x3 matrix representation is effectively the 6D representation plus 3 useless parameters. (Zhou et al., 2019) `ev:asserted` p. 5 ^zhou2019continuity-027
- Orthogonalizing predicted 3x3 matrices as a postprocess prevents certain applications such as forward kinematics, according to the authors. (Zhou et al., 2019) `ev:asserted` p. 5 ^zhou2019continuity-028
- For n ≥ 3, stereographic projections combined with normalization can reduce the representation dimension while keeping it continuous. (Zhou et al., 2019) `ev:computed` p. 5 ^zhou2019continuity-029
- In the authors' experiments, the dimension-reduced representation does not outperform the Gram-Schmidt-like representation from Case 3. (Zhou et al., 2019) `ev:measured` p. 5 ^zhou2019continuity-030
- The authors project as few components as possible, since they found projection nonlinearities can make learning more difficult. (Zhou et al., 2019) `ev:asserted` p. 5 ^zhou2019continuity-031
- For 3D rotations, a normalized projection on the last 4 dimensions of the flattened 6D vector gives a 5D representation. (Zhou et al., 2019) `ev:computed` p. 6 ^zhou2019continuity-032
- Up to n − 2 normalized projections can reduce the dimensionality of the Case 3 representation of SO(n) by n − 2. (Zhou et al., 2019) `ev:computed` p. 6 ^zhou2019continuity-033
- The representations generalize to the orthogonal group O(n) with an extra component indicating whether the determinant is +1 or -1. (Zhou et al., 2019) `ev:asserted` p. 6 ^zhou2019continuity-034
- For similarity transforms, the Gram-Schmidt output is multiplied by the scale α, taken as the norm of an input basis vector. (Zhou et al., 2019) `ev:asserted` p. 6 ^zhou2019continuity-035
- The sanity test encoder is an MLP of four fully-connected layers with 128-neuron hidden layers and Leaky ReLU activations. (Zhou et al., 2019) `ev:reported` p. 6 ^zhou2019continuity-036
- The sanity test loss is the L2 distance between input and output SO(3) matrices, which is invariant to the representation. (Zhou et al., 2019) `ev:reported` p. 6 ^zhou2019continuity-037
- Evaluation uses the geodesic error, defined as the minimal angular difference between the input and output rotations. (Zhou et al., 2019) `ev:reported` p. 7 ^zhou2019continuity-038
- In the sanity test, 6D and 5D representations reached mean errors of 0.49 degrees, versus 3.32 degrees for quaternions. (Zhou et al., 2019) `ev:measured` p. 7 ^zhou2019continuity-039
- In the sanity test, Euler angles performed worst, with a mean geodesic error of 6.98 degrees at 500k iterations. (Zhou et al., 2019) `ev:measured` p. 7 ^zhou2019continuity-040
- The proposed 6D and 5D representations produced no sanity-test errors higher than 2 degrees on the test rotations. (Zhou et al., 2019) `ev:measured` p. 7 ^zhou2019continuity-041
- For quaternion, axis-angle and Euler representations, certain sanity-test samples still produced errors up to 180 degrees. (Zhou et al., 2019) `ev:measured` p. 7 ^zhou2019continuity-042
- The 6D and 5D representations converged much faster than the other representations in the sanity test. (Zhou et al., 2019) `ev:measured` p. 7 ^zhou2019continuity-043
- In the autoencoder experiments, discontinuous representations can have up to 6 to 14 times higher mean errors than continuous ones. (Zhou et al., 2019) `ev:measured` p. 2 ^zhou2019continuity-044
- With geodesic loss and uniform sampling on SO(3), the 6D representation reached a mean sanity-test error of 0.45 degrees. (Zhou et al., 2019) `ev:measured` p. 13 ^zhou2019continuity-045
- Rodriguez vectors and hemisphere-constrained quaternions gave sanity-test errors significantly worse than the 5D and 6D representations. (Zhou et al., 2019) `ev:measured` p. 12 ^zhou2019continuity-046
- The point cloud rotation estimator is a weight-sharing Siamese network whose halves are simplified PointNet structures. (Zhou et al., 2019) `ev:reported` p. 7 ^zhou2019continuity-047
- The point cloud network was trained with 2,290 airplane point clouds from ShapeNet using an L2 loss on rotation matrices. (Zhou et al., 2019) `ev:reported` p. 8 ^zhou2019continuity-048
- The point cloud network was tested on 400 held-out airplane point clouds augmented with 100 random rotations. (Zhou et al., 2019) `ev:reported` p. 8 ^zhou2019continuity-049
- In point cloud pose estimation, the 6D representation had the lowest mean geodesic error, 2.85 degrees, among tested representations. (Zhou et al., 2019) `ev:measured` p. 7 ^zhou2019continuity-050
- With the 6D representation, around 95% of point cloud pose estimation errors were lower than 5 degrees. (Zhou et al., 2019) `ev:measured` p. 8 ^zhou2019continuity-051
- The Euler representation was worst for point cloud pose estimation, with around 10% of errors higher than 25 degrees. (Zhou et al., 2019) `ev:measured` p. 8 ^zhou2019continuity-052
- For point clouds, the 5D representation performed worse than 6D but outperformed the 3D and 4D representations. (Zhou et al., 2019) `ev:measured` p. 8 ^zhou2019continuity-053
- The authors hypothesize that gradient distortion from the stereographic projection makes regression harder for the 5D representation. (Zhou et al., 2019) `ev:asserted` p. 8 ^zhou2019continuity-054
- Direct 3x3 matrix regression with Gram-Schmidt orthogonalization at test time gave a mean point cloud error of 4.21 degrees. (Zhou et al., 2019) `ev:measured` p. 7 ^zhou2019continuity-055
- The authors hypothesize that the orthogonalization post-process introduces errors, making the 3x3 matrix perform worse than 6D. (Zhou et al., 2019) `ev:asserted` p. 8 ^zhou2019continuity-056
- The inverse kinematics network is a four-layer MLP with 1024 hidden neurons, trained with an L2 loss on joint positions. (Zhou et al., 2019) `ev:reported` p. 8 ^zhou2019continuity-057
- In the inverse kinematics loss, joints adjacent to the hip carry weight 10 times higher than other joints. (Zhou et al., 2019) `ev:reported` p. 8 ^zhou2019continuity-058
- The inverse kinematics data comprise 865 CMU Motion Capture clips from 37 motion categories, with 73 clips randomly held out. (Zhou et al., 2019) `ev:reported` p. 8 ^zhou2019continuity-059
- In inverse kinematics, the 6D representation had the lowest mean joint error, 1.9 cm, versus 3.3 cm for quaternions. (Zhou et al., 2019) `ev:measured` p. 7 ^zhou2019continuity-060
- In the inverse kinematics test, the 5D representation performed similarly to 6D, with a mean error of 2.0 cm. (Zhou et al., 2019) `ev:measured` p. 7 ^zhou2019continuity-061
- In inverse kinematics, the 4D and 3D representations had higher percentages of big errors exceeding 10 cm. (Zhou et al., 2019) `ev:measured` p. 8 ^zhou2019continuity-062
- Regressing 3x3 matrices without orthogonalization during training created huge inverse kinematics errors, with a mean of 22.9 cm. (Zhou et al., 2019) `ev:measured` p. 7 ^zhou2019continuity-063
- The authors suggest the unorthogonalized 3x3 matrix may cause bone lengths to scale during the forward kinematics process. (Zhou et al., 2019) `ev:asserted` p. 8 ^zhou2019continuity-064
- On the worst-error inverse kinematics frames, the 6D network still created reasonable poses, unlike the quaternion network. (Zhou et al., 2019) `ev:measured` p. 12 ^zhou2019continuity-065
- Unit quaternions are also a discontinuous representation, with the third component jumping from 1 to −1 around θ = π. (Zhou et al., 2019) `ev:computed` p. 11 ^zhou2019continuity-066
- Losses applied only where the representation is continuous, such as 5D or 6D, should avoid discontinuity problems when converting to quaternions. (Zhou et al., 2019) `ev:asserted` p. 11 ^zhou2019continuity-067

## 🎯 Contributions

## 📖 Glossary

- **SO(n)** — Special orthogonal group: n × n real matrices with orthonormal columns and determinant one.
- **Continuous representation** — A representation whose mapping from original space to representation space is continuous.
- **Homeomorphism** — Continuous bijection with a continuous inverse between two topological spaces.
- **Topological embedding** — Continuous injective map that is a homeomorphism onto its image.
- **Geodesic error** — Minimal angular difference between two rotations.
- **6D representation** — First two columns of a rotation matrix, mapped back by Gram-Schmidt and cross product.
- **Stereographic projection** — Projection of a sphere point from a fixed pole onto a hyperplane.
- **Real projective space RP3** — Quotient of R4 minus origin by scaling; homeomorphic to SO(3).

## ❓ Open questions

- Why does the 5D representation underperform 6D on point clouds, and is the stereographic gradient-distortion hypothesis correct?
- Do the continuity advantages persist in tasks with symmetric objects, where rotation ambiguity also causes large errors?
- How do the representations compare under other losses and architectures beyond MLPs and simplified PointNet?
- Would discontinuity proofs for Rodriguez vectors and hemisphere-constrained quaternions confirm their empirical weakness?

## 📝 Notes on reading

- Version read: arXiv 1812.07035v4 (8 Jun 2020); the registry lists the 2019 arXiv preprint.
- Figure 5 plots (mean error curves and percentile curves) and Figure 6 (PCA visualizations of discontinuities) could only be described; their tables (c), (f), (i) were extracted and used.
- Exponents in training settings are garbled in the extraction (learning rate "10−5", "104 iterations", "105 rotation matrices", "2.6×106 iterations", "1.14 × 106 frames"); these values were not claimed.
- Equations (2)–(11) and the dimension formulas (e.g. "n2 −n") are partly garbled; claims describe the constructions in words.
- Inconsistency: the abstract says continuous representations outperform discontinuous ones, but in the IK table Euler angles (mean 2.7 cm) beat quaternions (3.3 cm) and axis-angle (3.0 cm), and in the point cloud table the direct 3x3 matrix (4.21) beats 5D (4.78). The introduction's "always outperform" holds only for 6D/5D vs 3D/4D.
- The paper's main-text sampling (uniform axis and angle) is not uniform on SO(3); Appendix G.2 reports that uniform SO(3) sampling gives similar results.

## Suggested new concepts

- 6D rotation representation — widely adopted continuous rotation parameterization for regression in pose estimation and robot learning.
- Continuity of rotation representations — topological criterion explaining learning failures of quaternions and Euler angles.
- Gram-Schmidt orthogonalization in networks — mechanism mapping unconstrained outputs onto SO(n).
- Rotation regression — recurring task across pose estimation, inverse kinematics and grasp prediction.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — No hay representación continua de SO(3) en $\mathbb{R}^{\le4}$; propone 5D/6D.
- **[[02_optimizacion_y_algoritmos]]** — Representación 6D continua (D.4).
- **[[03_aplicaciones_vision_por_computador]]** — Justifica la representación 6D (§2.3, §6.3)

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
