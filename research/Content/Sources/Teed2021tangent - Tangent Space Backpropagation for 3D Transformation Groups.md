---
aliases: []
type: "source"
title: "Tangent Space Backpropagation for 3D Transformation Groups (LieTorch)"
citekey: "Teed2021tangent"
doi: "10.48550/arXiv.2103.12032"
arxiv: "2103.12032"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2103.12032"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Zachary Teed", "Jia Deng"]
sha256: ["645a8ac67275f2609d692fc54214a7bd0b5e24e8790957ba5953d1db322beb25"]
pdf: "Content/Papers/Teed2021tangent.pdf"
topics: ["[[Optimización y algoritmos]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 59
---

📄 PDF: [[Teed2021tangent.pdf]]

> [!abstract] One-sentence summary
> The paper introduces LieTorch, a PyTorch library that backpropagates through SO(3), SE(3) and Sim(3) in tangent spaces, giving stable gradients and GPU speedups across pose graph optimization, registration and RGB-D SLAM.

## Abstract

We address the problem of performing backpropagation for computation graphs involving 3D transformation groups SO(3), SE(3), and Sim(3). 3D transformation groups are widely used in 3D vision and robotics, but they do not form vector spaces and instead lie on smooth manifolds. The standard backpropagation approach, which embeds 3D transformations in Euclidean spaces, suffers from numerical difficulties. We introduce a new library, which exploits the group structure of 3D transformations and performs backpropagation in the tangent spaces of manifolds. We show that our approach is numerically more stable, easier to implement, and beneficial to a diverse set of tasks. Our plug-and-play PyTorch library is available at https://github.com/princeton-vl/lietorch. (arXiv)

## 🧠 Key ideas (atomic)

- The paper addresses how to perform backpropagation through computation graphs that involve the 3D transformation groups SO(3), SE(3), and Sim(3). (Teed & Deng, 2021) `ev:asserted` p. 1 ^teed2021tangent-001
- The authors state that 3D transformations do not form vector spaces, so the standard Euclidean notion of gradient does not apply to them. (Teed & Deng, 2021) `ev:asserted` p. 1 ^teed2021tangent-002
- A typical prior approach represents an SE(3) rigid body transform as a matrix treated as a vector embedded in R16. (Teed & Deng, 2021) `ev:asserted` p. 1 ^teed2021tangent-003
- The authors state that backward-pass substeps of extended functions such as the matrix exponential often contain singularities causing numerical instabilities. (Teed & Deng, 2021) `ev:asserted` p. 1 ^teed2021tangent-004
- The commonly used PyTorch3D library returns a NaN gradient for its matrix logarithm when the identity matrix is given as input. (Teed & Deng, 2021) `ev:cited` p. 6 ^teed2021tangent-005
- The authors state that, to their knowledge, no prior work has performed backpropagation on Sim(3) before this paper. (Teed & Deng, 2021) `ev:asserted` p. 2 ^teed2021tangent-006
- The approach retains the group structure and performs backpropagation directly in the tangent space of each group element instead of an embedding. (Teed & Deng, 2021) `ev:asserted` p. 2 ^teed2021tangent-007
- For a rigid body transformation in SE(3), the gradient is backpropagated as a 6-dimensional vector in a local coordinate system centered at it. (Teed & Deng, 2021) `ev:reported` p. 2 ^teed2021tangent-008
- The authors claim tangent space backpropagation avoids differentiating through singularity-ridden embedding substeps, guaranteeing numerically stable gradients for the supported groups. (Teed & Deng, 2021) `ev:asserted` p. 2 ^teed2021tangent-009
- The authors state that the gradient computation does not depend on whether rotations are represented as quaternions or as 3 × 3 matrices. (Teed & Deng, 2021) `ev:asserted` p. 2 ^teed2021tangent-010
- Differentiating exp and log through the group structure avoids storing intermediate values, which the authors say keeps computation graphs smaller. (Teed & Deng, 2021) `ev:asserted` p. 2 ^teed2021tangent-011
- The authors state that computing gradients directly in the tangent space removes the need to reproject gradients during [[Riemannian optimization|manifold optimization]]. (Teed & Deng, 2021) `ev:asserted` p. 2 ^teed2021tangent-012
- The authors describe this, to their knowledge, as the first time backpropagation is performed in Lie group tangent spaces for training neural networks. (Teed & Deng, 2021) `ev:asserted` p. 2 ^teed2021tangent-013
- LieTorch exposes 3D transformation objects with a Tensor-like interface supporting arbitrary batch shapes, indexing, and reshaping operations inside PyTorch computation graphs. (Teed & Deng, 2021) `ev:reported` p. 2 ^teed2021tangent-014
- Manifold extensions such as McTorch and Geoopt embed manifolds in Euclidean space and obtain manifold gradients through an orthogonal projection. (Teed & Deng, 2021) `ev:cited` p. 3 ^teed2021tangent-015
- Frameworks such as GTSAM are tailored to computing Jacobian matrices and cannot readily be used within computation graphs for training neural networks. (Teed & Deng, 2021) `ev:cited` p. 3 ^teed2021tangent-016
- The authors note that directly differentiating the original manifold function is not possible for all manifolds, but Lie group structure enables it. (Teed & Deng, 2021) `ev:asserted` p. 3 ^teed2021tangent-017
- The library supports Exp, Log, Inv, Mul, Adj, AdjT, Act and ActP operations, each differentiable with respect to all input arguments. (Teed & Deng, 2021) `ev:reported` p. 4 ^teed2021tangent-018
- The differential is generalized to Lie groups by replacing vector addition and subtraction with perturbations applied through the [[Exponential map|exponential map]] in the tangent space. (Teed & Deng, 2021) `ev:computed` p. 4 ^teed2021tangent-019
- For group multiplication, the derived gradient with respect to the second factor equals the upstream gradient multiplied by the adjoint of the left factor. (Teed & Deng, 2021) `ev:computed` p. 5 ^teed2021tangent-020
- The backward pass of the logarithm map multiplies the upstream gradient by the inverse left Jacobian, giving a 3-dimensional gradient for SO(3). (Teed & Deng, 2021) `ev:computed` p. 5 ^teed2021tangent-021
- For Sim(3), which lacks an analytic left Jacobian expression, the gradient is numerically approximated with a series expansion involving Bernoulli numbers. (Teed & Deng, 2021) `ev:reported` p. 5 ^teed2021tangent-022
- Standard embedding-space autodifferentiation of the SO(3) logarithm yields a 9-dimensional gradient, whereas the tangent space approach yields a 3-dimensional one. (Teed & Deng, 2021) `ev:computed` p. 5 ^teed2021tangent-023
- The authors argue that the gradient of a Taylor approximation is not necessarily a good approximation of the true gradient near singular points. (Teed & Deng, 2021) `ev:asserted` p. 6 ^teed2021tangent-024
- In the SO(3) logarithm, the inverse cosine term has a singular gradient when the input rotation is the identity. (Teed & Deng, 2021) `ev:computed` p. 6 ^teed2021tangent-025
- The implementation defines a new type for group elements and a custom gradient for every function with group inputs or outputs. (Teed & Deng, 2021) `ev:reported` p. 6 ^teed2021tangent-026
- Rotations are represented internally as unit quaternions, which the authors describe as compact and having desirable numeric properties. (Teed & Deng, 2021) `ev:reported` p. 6 ^teed2021tangent-027
- All operations involving groups include both CUDA and C++ kernels to leverage the GPU if it is available. (Teed & Deng, 2021) `ev:reported` p. 6 ^teed2021tangent-028
- The toy inverse kinematics evaluation performed 1000 runs each for SO(3) joints and for extendable R+ × SO(3) joints. (Teed & Deng, 2021) `ev:reported` p. 6 ^teed2021tangent-029
- Without tuning the forward pass, PyTorch+Autograd converged on 0.0 percent of inverse kinematics runs for both joint groups. (Teed & Deng, 2021) `ev:measured` p. 6 ^teed2021tangent-030
- PyTorch+Autograd with explicitly tuned stability converged on 99.8 percent of SO(3) inverse kinematics runs within the tolerance threshold. (Teed & Deng, 2021) `ev:measured` p. 6 ^teed2021tangent-031
- The proposed library converged on 100.0 percent of inverse kinematics runs for both joint groups without any modification. (Teed & Deng, 2021) `ev:measured` p. 6 ^teed2021tangent-032
- Pose graph rotation initialization used SGD with momentum set to 0.5 for 1000 gradient steps on a reshaped geodesic cost. (Teed & Deng, 2021) `ev:reported` p. 7 ^teed2021tangent-033
- On all four pose graph datasets, the gradient-based initialization converged to the global minimum, matching the performance of chordal relaxation. (Teed & Deng, 2021) `ev:measured` p. 7 ^teed2021tangent-034
- On two pose graph datasets, the gradient-based initializer in gtsam got stuck in a local minimum, unlike the proposed implementation. (Teed & Deng, 2021) `ev:measured` p. 7 ^teed2021tangent-035
- On the Cube pose graph, the proposed initializer took 1.21 seconds compared with 17.9 seconds for chordal+gtsam initialization. (Teed & Deng, 2021) `ev:measured` p. 7 ^teed2021tangent-036
- On the smaller Parking-Garage problem, chordal+gtsam initialization took 0.23 seconds compared with 1.18 seconds for the proposed method. (Teed & Deng, 2021) `ev:measured` p. 7 ^teed2021tangent-037
- The proposed method converged to the same pose graph solution as Autograd while consistently providing a 10-15x speedup on the GPU. (Teed & Deng, 2021) `ev:measured` p. 7 ^teed2021tangent-038
- The registration experiments used the synthetic TartanAir dataset, holding out five named scenes for testing and using the rest for training. (Teed & Deng, 2021) `ev:reported` p. 7 ^teed2021tangent-039
- Registration training pairs were sampled uniformly among frame pairs whose mean optical flow magnitude lay between 16 and 120 pixels. (Teed & Deng, 2021) `ev:reported` p. 8 ^teed2021tangent-040
- The sampled registration pairs had a median translation of 54cm and a median rotation angle of 4.7 degrees. (Teed & Deng, 2021) `ev:reported` p. 8 ^teed2021tangent-041
- For Sim(3) registration, scaling was sampled uniformly in the range [0.5, 2.0] with depth maps rescaled accordingly. (Teed & Deng, 2021) `ev:reported` p. 8 ^teed2021tangent-042
- The registration network is based on RAFT and builds a full 4D correlation volume from visual similarity between all pixel pairs. (Teed & Deng, 2021) `ev:reported` p. 8 ^teed2021tangent-043
- A [[Differentiable optimization layers|differentiable least squares layer]] performs 3 Gauss-Newton updates, and the library backpropagates through them to train the network. (Teed & Deng, 2021) `ev:reported` p. 8 ^teed2021tangent-044
- The registration network is trained with a geodesic loss summing the norm of the logarithm of each estimate-to-ground-truth error. (Teed & Deng, 2021) `ev:reported` p. 8 ^teed2021tangent-045
- Untuned PyTorch+Autograd produced NaN values and 0.0 accuracy on every SE(3) and Sim(3) registration metric. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021tangent-046
- On SE(3) registration, the analytic variant reached 78.7 translation accuracy under 1cm, compared with 78.75 for tuned Autograd. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021tangent-047
- On Sim(3) registration, the 2nd-order approximation reached 98.3 scale accuracy under 1%, compared with 98.0 for tuned Autograd. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021tangent-048
- The authors find that the order of the Sim(3) series approximation makes little difference in the final registration accuracy. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021tangent-049
- The authors state that, to the best of their knowledge, this is the first backpropagation performed on similarity transformations. (Teed & Deng, 2021) `ev:asserted` p. 8 ^teed2021tangent-050
- For RGB-D SLAM, the authors reimplemented the DeepV2D approach in PyTorch so that it could be used directly with LieTorch. (Teed & Deng, 2021) `ev:reported` p. 8 ^teed2021tangent-051
- The reimplemented DeepV2D was trained on a combination of the NYU and ScanNet datasets using 4 frame video sequences. (Teed & Deng, 2021) `ev:reported` p. 8 ^teed2021tangent-052
- Pose estimation was trained with the direct geodesic error instead of the indirect optical flow proxy loss used by the original DeepV2D. (Teed & Deng, 2021) `ev:reported` p. 8 ^teed2021tangent-053
- On the RGB-D tracking benchmark, the LieTorch DeepV2D reached an average ATE rmse of 0.105 m versus 0.113 for DeepV2D. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021tangent-054
- The authors conclude that the geodesic loss, difficult with standard backpropagation but easy with their approach, resulted in improved tracking performance. (Teed & Deng, 2021) `ev:asserted` p. 8 ^teed2021tangent-055
- When θ or σ is small, second order Taylor approximations of the [[Exponential map|exponential maps]] are used to avoid numerical issues. (Teed & Deng, 2021) `ev:reported` p. 12 ^teed2021tangent-056
- Analytic inverse left Jacobians were used for SO(3) and SE(3), whereas only the first 3 series terms were used for Sim(3). (Teed & Deng, 2021) `ev:reported` p. 14 ^teed2021tangent-057
- The Sim(3) network replaces the RAFT GRU with a single 3 × 3 convolutional GRU using a hidden state of 128 channels. (Teed & Deng, 2021) `ev:reported` p. 14 ^teed2021tangent-058
- The Sim(3) registration network applies 12 update iterations during both training and testing, as stated in the appendix architecture description. (Teed & Deng, 2021) `ev:reported` p. 14 ^teed2021tangent-059

## 🎯 Contributions


## 📖 Glossary

- **Lie group** — A group that is also a smooth manifold, e.g. rotations SO(3) or rigid motions SE(3).
- **Lie algebra** — The tangent space at the identity element of a Lie group, isomorphic to R^k.
- **Tangent space backpropagation** — Propagating gradients as vectors in each group element's local tangent space rather than an embedding.
- **Adjoint (Adj)** — Linear map relating right-action and left-action local coordinates around a group element.
- **Left Jacobian** — Matrix mapping tangent-space perturbations to manifold perturbations; its inverse differentiates the logarithm map.
- **Sim(3)** — Group of 3D similarity transformations: rotation, translation and uniform scale.
- **Embedding-space backpropagation** — Autodifferentiating group operations as matrix functions in a Euclidean space such as R16.

## ❓ Open questions

- How does tangent space backpropagation compare against other differentiable Lie group libraries released after this work?
- Can the approach extend to manifolds without Lie group structure, which the authors say are not generally amenable?
- Why does tuned Autograd reach near-equal accuracy on registration, and when does the tangent space approach give a decisive accuracy gain?
- How sensitive is Sim(3) training to the truncation of the Jacobian series in harder regimes (large scale changes, large rotations)?
- Does the geodesic-loss gain on RGB-D SLAM hold across other benchmarks and longer sequences?

## 📝 Notes on reading

Version read: arXiv preprint 2103.12032v2 (25 Mar 2021), matching the packet identifier.

The text refers to "Tab. 5" for both the inverse kinematics and the pose graph results; the inverse kinematics table has no caption number in the extraction and the pose graph results are Table 2. Table 2 error values carry flattened exponents (e.g. "5.32 × 1010" for 5.32 × 10^10), so per-cell errors were not claimed except via the text's convergence statements. The inverse kinematics tolerance threshold (1 × 10−4) is also extracted with a flattened exponent.

Table 4 compares DeepTAM, DeepV2D and the reimplementation, but the text also names the classical RGBD-SLAM method, which does not appear in the table. DeepTAM and DeepV2D each appear twice in the reference list ([40]/[41], [33]/[34]).

Eqn. 26 (main text) writes the inverse left Jacobian series with a (−1)^n factor, whereas Eqn. 70 (appendix) omits it; the sign convention is inconsistent between the two. Table 3 reports 1st, 2nd and 3rd order Sim(3) approximations while the appendix says the first 3 terms were used.

Figures 1, 2, 5 and 6 are diagrams (computation graphs, network architecture); Figures 3 and 4 are qualitative results. The pose graph code listing on p. 7 illustrates the API.

## Suggested new concepts

- Tangent space backpropagation — the core technique; reusable across differentiable SLAM, registration and pose estimation notes.
- Lie group differentiation for robotics — SO(3)/SE(3)/Sim(3) calculus (adjoint, left Jacobian) recurs across state estimation and learning papers.
- Differentiable Gauss-Newton layers — unrolled least-squares optimization inside networks, used here and in DeepV2D/RAFT-style pipelines.
- Pose graph initialization — chordal relaxation vs Riemannian gradient descent as strategies to avoid local minima.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Retropropagación en el álgebra de Lie; base conceptual de los gradientes en el tangente (A.6).
- **[[03_aplicaciones_vision_por_computador]]** — Biblioteca para retropropagar en el tangente de $SE(3)$/$Sim(3)$
