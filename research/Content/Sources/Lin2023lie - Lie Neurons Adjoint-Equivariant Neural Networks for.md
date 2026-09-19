---
aliases: []
type: "source"
title: "Lie Neurons: Adjoint-Equivariant Neural Networks for Semisimple Lie Algebras"
citekey: "Lin2023lie"
doi: "10.48550/arXiv.2310.04521"
arxiv: "2310.04521"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2310.04521"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Tzu-Yuan Lin", "Minghan Zhu", "Maani Ghaffari"]
sha256: ["2d6d5ca1d3b23fe94b1a933a3c472f7ebe41c313df5bb23283d4e5d0e0801930"]
pdf: "Content/Papers/Lin2023lie.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Lin2023lie.pdf]]

> [!abstract] One-sentence summary
> Lie Neurons generalizes Vector Neurons to an adjoint-equivariant MLP over any semisimple Lie algebra, adding Killing-form, Lie-bracket and geometric-mixing layers, and beats MLP, EMLP and Vector Neurons baselines on so(3), sl(3) and sp(4) tasks such as BCH regression, rigid-body dynamics and homography-based classification.

## Abstract

This paper proposes an equivariant neural network that takes data in any semi-simple Lie algebra as input. The corresponding group acts on the Lie algebra as adjoint operations, making our proposed network adjoint-equivariant. Our framework generalizes the Vector Neurons, a simple $\mathrm{SO}(3)$-equivariant network, from 3-D Euclidean space to Lie algebra spaces, building upon the invariance property of the Killing form. Furthermore, we propose novel Lie bracket layers and geometric channel mixing layers that extend the modeling capacity. Experiments are conducted for the $\mathfrak{so}(3)$, $\mathfrak{sl}(3)$, and $\mathfrak{sp}(4)$ Lie algebras on various tasks, including fitting equivariant and invariant functions, learning system dynamics, point cloud registration, and homography-based shape classification. Our proposed equivariant network shows wide applicability and competitive performance in various domains. (arXiv)

## 🧠 Key ideas (atomic)

- Lie group methods provide the machinery to study continuous symmetries in geometric problems of control theory, robotics, computer vision and graphics. (Lin et al., 2023) `ev:cited` p. 1 ^lin2023lie-001
- The authors state that an equivariant model generalizes over group-action variations by construction, reducing sampling complexity in learning. (Lin et al., 2023) `ev:asserted` p. 1 ^lin2023lie-002
- The paper proposes an adjoint-equivariant network architecture that processes finite-dimensional semisimple Lie algebraic input data, which frequently appears in geometric problems. (Lin et al., 2023) `ev:asserted` p. 2 ^lin2023lie-003
- The framework generalizes Vector Neurons, an SO(3)-equivariant network designed for 3-D point clouds, to data in arbitrary semisimple Lie algebras. (Lin et al., 2023) `ev:asserted` p. 2 ^lin2023lie-004
- The authors propose equivariant channel mixing layers that fuse information across the geometric dimension, which the earlier Vector Neurons work could not. (Lin et al., 2023) `ev:asserted` p. 2 ^lin2023lie-005
- The software implementation of Lie Neurons is publicly available in the UMich-CURLY LieNeurons repository on GitHub. (Lin et al., 2023) `ev:reported` p. 2 ^lin2023lie-006
- Earlier work by Finzi and colleagues constructed MLPs equivariant to arbitrary matrix groups using their finite-dimensional representations. (Lin et al., 2023) `ev:cited` p. 2 ^lin2023lie-007
- When working with so(3), the method specializes to Vector Neurons with an additional nonlinearity and a geometric mixing layer. (Lin et al., 2023) `ev:asserted` p. 2 ^lin2023lie-008
- Each Lie algebra element is represented as a real coefficient vector by expanding it over a chosen set of linearly independent basis matrices. (Lin et al., 2023) `ev:asserted` p. 3 ^lin2023lie-009
- Since the adjoint action is linear, it can be modeled as a matrix multiplication on the vector form of the Lie algebra. (Lin et al., 2023) `ev:asserted` p. 3 ^lin2023lie-010
- A Lie algebra is semisimple if and only if its Killing form is non-degenerate, a result also known as Cartan's Criterion. (Lin et al., 2023) `ev:cited` p. 3 ^lin2023lie-011
- For a compact Lie group the Killing form is negative definite, so its negative naturally provides an inner product. (Lin et al., 2023) `ev:asserted` p. 3 ^lin2023lie-012
- Lie Neurons linear layers multiply features on the right by a learnable weight, leaving the left adjoint action on the geometric dimension unaffected. (Lin et al., 2023) `ev:asserted` p. 4 ^lin2023lie-013
- The Lie Neurons linear layers ignore the bias term in order to preserve equivariance to the adjoint action. (Lin et al., 2023) `ev:asserted` p. 4 ^lin2023lie-014
- The LN-ReLU layer generalizes the Vector Neurons ReLU by replacing the standard inner product with the negative of the Killing form. (Lin et al., 2023) `ev:asserted` p. 4 ^lin2023lie-015
- The LN-Bracket layer uses the Lie bracket of two learned linear maps of the input as an equivariant nonlinear activation. (Lin et al., 2023) `ev:asserted` p. 4 ^lin2023lie-016
- The authors add a skip connection to the bracket layer because the non-commutativity captured by the bracket can be small in practice. (Lin et al., 2023) `ev:asserted` p. 4 ^lin2023lie-017
- The geometric channel mixing module left-multiplies features by a learned matrix built from two equivariant features, and currently works only for so(n). (Lin et al., 2023) `ev:asserted` p. 5 ^lin2023lie-018
- The authors conjecture the mixing module could extend to any semisimple Lie algebra, though ensuring invertibility of a learned feature may require post-processing. (Lin et al., 2023) `ev:asserted` p. 5 ^lin2023lie-019
- The proposed max pooling layer selects, for each feature channel, the element whose Killing form with a learned direction is largest. (Lin et al., 2023) `ev:asserted` p. 5 ^lin2023lie-020
- An invariant layer outputs the Killing form of each feature channel with itself, for applications that demand invariant features. (Lin et al., 2023) `ev:asserted` p. 5 ^lin2023lie-021
- The authors omit the normalization of the Vector Neurons ReLU because the norm is not well defined when the Killing form is not negative definite. (Lin et al., 2023) `ev:asserted` p. 5 ^lin2023lie-022
- For the sp(4) invariant function regression, the authors generated 10,000 training and 10,000 testing data points. (Lin et al., 2023) `ev:reported` p. 5 ^lin2023lie-023
- In sp(4) invariant function regression, Lie Neurons reached a mean squared error of 2.70 × 10−4 with 263,170 parameters. (Lin et al., 2023) `ev:measured` p. 6 ^lin2023lie-024
- The MLP 512 baseline trained with SP(4) augmentation reached errors of 0.123 on the original and 0.446 on the augmented sp(4) test set. (Lin et al., 2023) `ev:measured` p. 6 ^lin2023lie-025
- Without data augmentation, Lie Neurons kept an sp(4) invariance error of 2.00 × 10−4, against 0.374 for the augmented MLP 512. (Lin et al., 2023) `ev:measured` p. 6 ^lin2023lie-026
- In so(3) BCH formula regression, Lie Neurons reached a Frobenius error of 6.9 × 10−4 on both original and conjugated test sets. (Lin et al., 2023) `ev:measured` p. 6 ^lin2023lie-027
- EMLP reached a BCH Frobenius error of 2.6 × 10−3, about one order of magnitude larger than the error of Lie Neurons. (Lin et al., 2023) `ev:measured` p. 6 ^lin2023lie-028
- The plain MLP reached a Frobenius error of 0.017 on the original BCH test set but 0.295 on the adjoint-augmented set. (Lin et al., 2023) `ev:measured` p. 6 ^lin2023lie-029
- Truncating the [[Baker-Campbell-Hausdorff formula|BCH series]] to third-order terms gave a Frobenius error of 0.191 on the so(3) regression test data. (Lin et al., 2023) `ev:computed` p. 6 ^lin2023lie-030
- The e3nn and Vector Neurons baselines were unable to converge in the so(3) BCH formula regression experiment. (Lin et al., 2023) `ev:measured` p. 6 ^lin2023lie-031
- The authors conclude the BCH experiment demonstrates the benefits of the bracket nonlinear layer, since Lie Neurons with only ReLU layers reduce to Vector Neurons. (Lin et al., 2023) `ev:asserted` p. 6 ^lin2023lie-032
- The dynamics experiment learns the vector field of the free-rotating International Space Station as an initial value problem within Neural ODE. (Lin et al., 2023) `ev:reported` p. 7 ^lin2023lie-033
- The authors generated 10 random training trajectories, each containing 25 seconds of data and 1000 data points, from the NASA inertia tensor. (Lin et al., 2023) `ev:reported` p. 7 ^lin2023lie-034
- Learnable equivariant weights serve as an implicit representation of the inertia tensor and are rotated manually when the reference frame changes. (Lin et al., 2023) `ev:reported` p. 7 ^lin2023lie-035
- The authors assume the change of reference frame matrix is known at test time, due to the scope of the project. (Lin et al., 2023) `ev:asserted` p. 7 ^lin2023lie-036
- In the ISS dynamics experiment, the Lie Neurons network without the geometric mixing layers was unable to converge. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023lie-037
- The authors suggest this failure is likely because the inertia tensor acts on the left of the angular velocity, requiring geometric mixing. (Lin et al., 2023) `ev:asserted` p. 7 ^lin2023lie-038
- Point cloud registration regresses the SO(3) rotation aligning two noisy point clouds without correspondences, trained and evaluated on ModelNet40. (Lin et al., 2023) `ev:reported` p. 7 ^lin2023lie-039
- On unseen ISS test trajectories, Lie Neurons had a 25-second trajectory error of 0.018 rad/s, against 0.800 for the MLP. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023lie-040
- The Lie Neurons errors on unseen trajectories were identical on original and SO(3)-rotated frames, rising from 0.005 at 5 seconds. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023lie-041
- Trained and tested on a single trajectory, the MLP 25-second error rose from 0.225 to 4.130 under rotated reference frames. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023lie-042
- On a single trajectory with rotated frames, EMLP reached a 25-second error of 1.459, compared with 0.579 for Lie Neurons. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023lie-043
- Adding the geometric mixing module lowered the average ModelNet40 registration error of Vector Neurons from 2.227 to 1.934 degrees. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023lie-044
- Lie Neurons with the mixing module reached an average registration error of 1.879 degrees, similar to Vector Neurons with mixing. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023lie-045
- The special linear group SL(3) has 8 degrees of freedom and can be used to model homography transformations between images. (Lin et al., 2023) `ev:cited` p. 8 ^lin2023lie-046
- The Platonic solid task classifies tetrahedra, octahedra and icosahedra from homographies between projections of neighboring faces in an image plane. (Lin et al., 2023) `ev:reported` p. 8 ^lin2023lie-047
- With identity intrinsics, rotating the camera by R turns an inter-face homography H into RHR−1, an adjoint action in SL(3). (Lin et al., 2023) `ev:asserted` p. 8 ^lin2023lie-048
- The authors state that Lie Neurons is adjoint-equivariant by construction and does not require the Lie group to be compact. (Lin et al., 2023) `ev:asserted` p. 8 ^lin2023lie-049
- The LN-ReLU layer relies on a non-degenerate Killing form, which limits that layer to semisimple Lie algebras. (Lin et al., 2023) `ev:asserted` p. 8 ^lin2023lie-050
- In Platonic solid classification, LN-LR reached 99.56% accuracy with 134,664 parameters, against 95.76% for the MLP with 206,339. (Lin et al., 2023) `ev:measured` p. 9 ^lin2023lie-051
- Under rotated camera poses, MLP classification accuracy fell to 36.54%, whereas the LN-LR + LN-LB model kept 99.61%. (Lin et al., 2023) `ev:measured` p. 9 ^lin2023lie-052
- Training the MLP with augmentation raised its rotated-pose accuracy to 81.20% but lowered its original-pose accuracy to 81.47%. (Lin et al., 2023) `ev:measured` p. 9 ^lin2023lie-053
- For general Lie groups the adjoint representation might not be irreducible, so the linear layer may not cover all equivariant maps. (Lin et al., 2023) `ev:asserted` p. 9 ^lin2023lie-054
- The authors name finding equivariant lifts from standard sensor measurement spaces into the Lie algebraic space as important future work. (Lin et al., 2023) `ev:asserted` p. 9 ^lin2023lie-055
- The work assumes a basis can be found for the target Lie algebra, which the authors consider valid for many robotics applications. (Lin et al., 2023) `ev:asserted` p. 9 ^lin2023lie-056
- In sl(3) invariant function regression, the LN-LR + LN-LB model reached a mean squared error of 8.84 × 10−4, against 0.148 for the MLP. (Lin et al., 2023) `ev:measured` p. 15 ^lin2023lie-057
- On the SL(3)-augmented invariant regression test set, the MLP error rose to 6.493, while Lie Neurons errors stayed unchanged. (Lin et al., 2023) `ev:measured` p. 15 ^lin2023lie-058
- The LN-LB model alone performed poorly on sl(3) invariant regression, with a mean squared error of 0.557. (Lin et al., 2023) `ev:measured` p. 15 ^lin2023lie-059
- The training curves show Lie Neurons converging faster than the MLP, which the authors say indicates better data efficiency. (Lin et al., 2023) `ev:measured` p. 15 ^lin2023lie-060
- In sl(3) equivariant function regression, the 2 LN-LB model reached a mean squared error of 9.83 × 10−10 on the regular test set. (Lin et al., 2023) `ev:measured` p. 16 ^lin2023lie-061
- The MLP reached a mean squared error of 0.011 on the regular equivariant test set but 1.318 on adjoint-augmented data. (Lin et al., 2023) `ev:measured` p. 16 ^lin2023lie-062
- The authors speculate that LN-LR works better on invariant tasks because it relies on the adjoint-invariant Killing form. (Lin et al., 2023) `ev:asserted` p. 16 ^lin2023lie-063
- The authors speculate that LN-LB performs better on equivariant tasks because it leverages the adjoint-equivariant Lie bracket. (Lin et al., 2023) `ev:asserted` p. 16 ^lin2023lie-064
- Removing the residual connection from the bracket layer raised the sl(3) invariant regression mean squared error from 0.558 to 4.838. (Lin et al., 2023) `ev:measured` p. 16 ^lin2023lie-065
- Without the residual connection, sl(3) equivariant regression mean squared error rose to 0.276 from 9.6 × 10−10 with it. (Lin et al., 2023) `ev:measured` p. 16 ^lin2023lie-066
- The authors note e3nn might perform better in BCH regression with more complicated architectures, nonlinearities and further hyperparameter tuning. (Lin et al., 2023) `ev:asserted` p. 13 ^lin2023lie-067
- The EMLP baseline used a channel size of 128 per block, as memory complexity prevented increasing its feature dimension. (Lin et al., 2023) `ev:reported` p. 13 ^lin2023lie-068
- For registration, point clouds were corrupted with Gaussian noise of standard deviation 0.01 after normalization to a unit cube. (Lin et al., 2023) `ev:reported` p. 14 ^lin2023lie-069

## 🎯 Contributions

## 📖 Glossary

- **Adjoint action** — Conjugation of a Lie algebra element by a group element, a change of basis.
- **Killing form** — Symmetric bilinear form tr(ad_X ad_Y) on a Lie algebra, invariant under adjoint action.
- **Semisimple Lie algebra** — Lie algebra whose Killing form is non-degenerate (Cartan's Criterion).
- **Lie bracket** — Antisymmetric binary operator on a Lie algebra; the commutator for matrix groups.
- **Hat and Vee maps** — Maps between a Lie algebra element and its coefficient vector over a basis.
- **Vector Neurons** — SO(3)-equivariant MLP lifting scalar features to 3-D vector features.
- **Geometric channel mixing** — Equivariant layer mixing information across the geometric, not feature, dimension.
- **BCH formula** — Series expressing log(e^X e^Y) in terms of X, Y and nested brackets.
- **EMLP** — Equivariant MLP for arbitrary matrix groups built from finite-dimensional representations.

## ❓ Open questions

- Can the geometric channel mixing layer be extended beyond so(n) to arbitrary semisimple Lie algebras while keeping the mixing matrix invertible?
- How can raw sensor measurements in standard vector spaces be lifted equivariantly into Lie algebra inputs?
- Can linear layers be designed to cover all adjoint-equivariant maps when the adjoint representation is reducible?
- Can the change of reference frame be inferred from observed trajectories instead of being given at test time?
- How do Lie Neurons behave on non-semisimple Lie algebras such as se(3), where the Killing form is degenerate?
- Is there a counterpart to batch normalization when the Killing form is not negative definite?

## 📝 Notes on reading

The version read is arXiv v3 (6 Jun 2024), which carries the ICML 2024 (PMLR 235) proceedings header; the packet identifier is the arXiv DOI. The PDF abstract adds finite-dimensional to the registry abstract. Section 5 states experiments on so(3) and sl(3), yet an sp(4) experiment follows in Section 5.1. Tables 6 and 7 appear to swap their column labels: the invariant-regression table (Table 6) heads its last column Equivariance Error, and the equivariant-regression table (Table 7) heads it Invariance Error. Table 8 reports LN-LB values (e.g. 0.558 MSE, 4.9 × 10−5 Einv) that differ slightly from Table 6 (0.557, 1.43 × 10−5), and Platonic accuracies as fractions (0.986) rather than the 99.14% in Table 5. Figures 1 (ISS trajectories and learned vector field), 4 (comparison with existing equivariant networks), 5 (architectures) and 6 (training curves) were described only in text. The Section 3 equations (Hat and Vee maps, the symplectic definition, and the sp(4) target function) are partly garbled in the extraction.

## Suggested new concepts

- Adjoint equivariance — equivariance to conjugation on Lie algebras, distinct from the left-action equivariance of most networks.
- Killing form — the invariant bilinear form that replaces the inner product in Lie-algebraic network layers.
- Vector Neurons — the SO(3)-equivariant MLP family that Lie Neurons generalizes; likely cited by other equivariant-learning sources.
- Neural ODE — framework used here to learn rigid-body dynamics from trajectory data.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** Redes cuyas entradas y salidas son elementos del álgebra de Lie y que son equivariantes a la acción adjunta; procesan twists y transformaciones como datos.
