---
aliases: []
type: "source"
title: "Generalizing Convolutional Neural Networks for Equivariance to Lie Groups on Arbitrary Continuous Data"
citekey: "Finzi2020generalizing"
doi: "10.48550/arXiv.2002.12880"
arxiv: "2002.12880"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2002.12880"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Marc Finzi", "Samuel Stanton", "Pavel Izmailov", "Andrew Gordon Wilson"]
sha256: ["28f7498b5c078cf7b4c606818508fbc6d3e9960c7d4f7dfb3aa581aa0c893472"]
pdf: "Content/Papers/Finzi2020generalizing.pdf"
topics: ["[[Matemáticas]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 65
---

📄 PDF: [[Finzi2020generalizing.pdf]]

> [!abstract] One-sentence summary
> LieConv builds convolutional layers equivariant to any Lie group with a surjective exponential map, needing only exp and log maps, and one architecture serves images, molecules and Hamiltonian dynamics, where equivariance gives exact conservation of momentum.

## Abstract

The translation equivariance of convolutional layers enables convolutional neural networks to generalize well on image problems. While translation equivariance provides a powerful inductive bias for images, we often additionally desire equivariance to other transformations, such as rotations, especially for non-image data. We propose a general method to construct a convolutional layer that is equivariant to transformations from any specified Lie group with a surjective exponential map. Incorporating equivariance to a new group requires implementing only the group exponential and logarithm maps, enabling rapid prototyping. Showcasing the simplicity and generality of our method, we apply the same model architecture to images, ball-and-stick molecular data, and Hamiltonian dynamical systems. For Hamiltonian systems, the equivariance of our models is especially impactful, leading to exact conservation of linear and angular momentum. (arXiv)

## 🧠 Key ideas (atomic)

- The authors propose LieConv, a convolutional layer that can be made equivariant to a given Lie group by defining exp and log maps. (Finzi et al., 2020) `ev:asserted` p. 1 ^finzi2020generalizing-001
- LieConv models act on arbitrary spatial data given as collections of coordinates and values, including non-homogeneous spaces. (Finzi et al., 2020) `ev:asserted` p. 2 ^finzi2020generalizing-002
- The same network architecture is used for all transformation groups and data types, spanning images, molecular data and dynamical systems. (Finzi et al., 2020) `ev:reported` p. 2 ^finzi2020generalizing-003
- The authors state that LieConv achieves state-of-the-art performance in these domains, even compared to domain-specific architectures. (Finzi et al., 2020) `ev:asserted` p. 2 ^finzi2020generalizing-004
- The approach reduces the work needed to implement equivariance to a new group, which the authors say enables rapid prototyping. (Finzi et al., 2020) `ev:asserted` p. 2 ^finzi2020generalizing-005
- Approaches that transform kernels for each group element have computation that grows quickly with the size of the group, the authors note. (Finzi et al., 2020) `ev:asserted` p. 2 ^finzi2020generalizing-006
- Harmonic-analysis equivariant methods require working out the group representation theory, which the authors call cumbersome and limited to compact groups. (Finzi et al., 2020) `ev:asserted` p. 2 ^finzi2020generalizing-007
- The B-spline Lie group CNN of Bekkers is described as not readily applicable to point data by the authors. (Finzi et al., 2020) `ev:asserted` p. 2 ^finzi2020generalizing-008
- Analytic exp and log maps exist for T(d), SO(3), SE(d) for d = 2, 3, and the rotation-scale group, citing Eade. (Finzi et al., 2020) `ev:cited` p. 3 ^finzi2020generalizing-009
- PointConv's reordering of the computation cuts memory and computational requirements by roughly 2 orders of magnitude, according to Wu et al. (Finzi et al., 2020) `ev:cited` p. 3 ^finzi2020generalizing-010
- Evaluating a single MLP-kernel layer on typical CIFAR-10 batches would require computing 20 billion kernel values, the authors estimate. (Finzi et al., 2020) `ev:computed` p. 3 ^finzi2020generalizing-011
- Lifting maps each input point to group elements, using the stabilizer of the origin and Haar-measure sampling when the stabilizer is infinite. (Finzi et al., 2020) `ev:reported` p. 4 ^finzi2020generalizing-012
- Enumerating kernel values per group element, as in conventional group equivariant networks, is described as infeasible for irregularly sampled data. (Finzi et al., 2020) `ev:asserted` p. 4 ^finzi2020generalizing-013
- The kernel is parametrized as a continuous function on the group by a fully connected neural network with Swish activations. (Finzi et al., 2020) `ev:reported` p. 4 ^finzi2020generalizing-014
- The kernel is modelled on the Lie algebra through the logarithm map, which restricts the method to groups with surjective exponential maps. (Finzi et al., 2020) `ev:asserted` p. 4 ^finzi2020generalizing-015
- Locality is enforced with a distance defined as the Frobenius norm of the matrix logarithm of u inverse times v. (Finzi et al., 2020) `ev:reported` p. 5 ^finzi2020generalizing-016
- This distance is left invariant and is a semi-metric, since it does not necessarily satisfy the triangle inequality. (Finzi et al., 2020) `ev:computed` p. 5 ^finzi2020generalizing-017
- Restricting the convolution to a local neighbourhood preserves equivariance precisely because the distance function is left invariant. (Finzi et al., 2020) `ev:computed` p. 5 ^finzi2020generalizing-018
- Neighbourhoods based on fixed input-space regions, such as a square 3 × 3 region, would have broken equivariance, the authors note. (Finzi et al., 2020) `ev:asserted` p. 5 ^finzi2020generalizing-019
- The group convolution integral is estimated with a Monte Carlo estimator that the authors show is equivariant in distribution. (Finzi et al., 2020) `ev:computed` p. 5 ^finzi2020generalizing-020
- To handle groups that do not act transitively, inputs are lifted to pairs of a group element and an orbit identifier. (Finzi et al., 2020) `ev:reported` p. 6 ^finzi2020generalizing-021
- The authors state that, to their knowledge, they are the first to systematically address equivariance where the input space is not homogeneous. (Finzi et al., 2020) `ev:asserted` p. 6 ^finzi2020generalizing-022
- Reordering the kernel computation through the MLP's final weight matrix leads to a massive reduction in memory and compute, the appendix states. (Finzi et al., 2020) `ev:asserted` p. 13 ^finzi2020generalizing-023
- For Abelian groups covering the input in one orbit, LieConv reduces to Euclidean convolution after a projection and a change to logarithmic coordinates. (Finzi et al., 2020) `ev:computed` p. 13 ^finzi2020generalizing-024
- The log-based distance equals the geodesic distance for subgroups in the exp image whose generators commute with their transposes. (Finzi et al., 2020) `ev:computed` p. 14 ^finzi2020generalizing-025
- Among the groups considered, the SE(d) groups do not satisfy the commutation condition required for the geodesic distance property. (Finzi et al., 2020) `ev:computed` p. 15 ^finzi2020generalizing-026
- Farthest point subsampling on the group is equivariant because the distances it uses are left invariant. (Finzi et al., 2020) `ev:computed` p. 15 ^finzi2020generalizing-027
- The RotMNIST dataset consists of 12k randomly rotated MNIST digits, split into 10k for training and 2k for validation. (Finzi et al., 2020) `ev:reported` p. 7 ^finzi2020generalizing-028
- Each RotMNIST image is treated as 28 × 28 points on the plane with associated values, to which a circular center crop is applied. (Finzi et al., 2020) `ev:reported` p. 7 ^finzi2020generalizing-029
- On RotMNIST, LieConv with SE(2) equivariance achieved a classification error of 1.24%, the lowest among its tested groups. (Finzi et al., 2020) `ev:measured` p. 7 ^finzi2020generalizing-030
- LieConv with the trivial group reached 1.58% error on RotMNIST, compared with 1.42% for the SO(2)-equivariant variant. (Finzi et al., 2020) `ev:measured` p. 7 ^finzi2020generalizing-031
- [[Steerable CNN|E(2)-Steerable CNNs]] report 0.68% error on RotMNIST, lower than every LieConv variant listed in the same table. (Finzi et al., 2020) `ev:cited` p. 7 ^finzi2020generalizing-032
- The authors acknowledge that more practical equivariant methods specialized to images exist, such as the [[Steerable CNN|steerable CNNs]] of Weiler and Cesa. (Finzi et al., 2020) `ev:asserted` p. 7 ^finzi2020generalizing-033
- Trained on the full 12k examples with SO(2) augmentation, LieConv with SE(2) equivariance reached 1.13% RotMNIST error. (Finzi et al., 2020) `ev:measured` p. 18 ^finzi2020generalizing-034
- The authors state that Ti-Pooling and E(2)-Steerable CNNs appear to fold the validation set back into training after tuning. (Finzi et al., 2020) `ev:asserted` p. 17 ^finzi2020generalizing-035
- The QM9 dataset encodes small molecules as 3D spatial coordinates of each atom with atomic charges, labelled with properties such as heat capacity. (Finzi et al., 2020) `ev:reported` p. 7 ^finzi2020generalizing-036
- The authors describe QM9 as challenging because molecules have no canonical origin or orientation and targets are invariant to E(3). (Finzi et al., 2020) `ev:asserted` p. 7 ^finzi2020generalizing-037
- In the HOMO ablation, the SE(3) LieConv network achieved 26.8 meV mean absolute error, lower than the trivial, SO(3) and T(3) variants. (Finzi et al., 2020) `ev:measured` p. 8 ^finzi2020generalizing-038
- In the HOMO ablation, SO(3) LieConv had 65.4 meV mean absolute error, worse than the trivial group at 31.7 meV. (Finzi et al., 2020) `ev:measured` p. 8 ^finzi2020generalizing-039
- On the full QM9 benchmark, T(3) LieConv achieved the lowest MAE among compared methods for α, Δε, HOMO and LUMO. (Finzi et al., 2020) `ev:measured` p. 7 ^finzi2020generalizing-040
- On the full QM9 benchmark, T(3) LieConv reached a HOMO mean absolute error of 30 meV, versus 34 meV for Cormorant. (Finzi et al., 2020) `ev:measured` p. 7 ^finzi2020generalizing-041
- SchNet outperformed LieConv on several QM9 targets, for example G, with 14 meV MAE versus 22 meV for LieConv. (Finzi et al., 2020) `ev:measured` p. 7 ^finzi2020generalizing-042
- LieConv's ZPVE error on QM9 was 2.280 meV, the highest among the four methods compared in the table. (Finzi et al., 2020) `ev:measured` p. 7 ^finzi2020generalizing-043
- The equivariance demo trained LieConv models on a subset of 20k of the 100k QM9 HOMO training examples without augmentation. (Finzi et al., 2020) `ev:reported` p. 17 ^finzi2020generalizing-044
- Without data augmentation, SE(3) LieConv kept HOMO test MAE near 62 meV when random SE(3) transformations were applied to the test set. (Finzi et al., 2020) `ev:measured` p. 17 ^finzi2020generalizing-045
- The trivial LieConv model's HOMO test MAE rose from 173 to 243 meV when SE(3) transformations were applied to test data. (Finzi et al., 2020) `ev:measured` p. 17 ^finzi2020generalizing-046
- The authors conclude that [[Equivariant neural network|added equivariances]] are especially important in the low data regime of the equivariance demonstration. (Finzi et al., 2020) `ev:asserted` p. 17 ^finzi2020generalizing-047
- Noether's theorem implies that translational and rotational symmetry of a Hamiltonian lead to conservation of linear and angular momentum. (Finzi et al., 2020) `ev:cited` p. 8 ^finzi2020generalizing-048
- HLieConv models with T(2) or SO(2) symmetry conserved linear or angular momentum with relative error close to machine epsilon. (Finzi et al., 2020) `ev:measured` p. 8 ^finzi2020generalizing-049
- The authors argue that discrete symmetry approaches would be less effective, as discrete groups have no corresponding Noether conservation. (Finzi et al., 2020) `ev:asserted` p. 8 ^finzi2020generalizing-050
- The spring benchmark compares a fully connected Neural-ODE, OGN, HOGN and HLieConv on predicting point particles connected by springs. (Finzi et al., 2020) `ev:reported` p. 8 ^finzi2020generalizing-051
- HLieConv outperformed HOGN on both state rollout error and system energy conservation in the spring dynamics experiments. (Finzi et al., 2020) `ev:measured` p. 9 ^finzi2020generalizing-052
- In the data-scaling experiment, HLieConv(T2) achieved lower test MSE than FC, HFC and HOGN across all training dataset sizes. (Finzi et al., 2020) `ev:measured` p. 9 ^finzi2020generalizing-053
- Test MSE generalization improved successively as Hamiltonian, graph-network and LieConv equivariance inductive biases were added to the models. (Finzi et al., 2020) `ev:measured` p. 9 ^finzi2020generalizing-054
- A T(2)-equivariant LieConv model of the dynamics F, rather than the Hamiltonian, did not conserve linear momentum in the spring experiments. (Finzi et al., 2020) `ev:measured` p. 17 ^finzi2020generalizing-055
- The authors conclude that Noether conservation requires both modelling the Hamiltonian and incorporating the given symmetry into the model. (Finzi et al., 2020) `ev:asserted` p. 17 ^finzi2020generalizing-056
- The authors also tried an HLieConv-SE2 model but found its exponential map not numerically stable enough for second derivatives. (Finzi et al., 2020) `ev:reported` p. 19 ^finzi2020generalizing-057
- Unlike ReLUs, the Swish activations used are twice differentiable, which is a requirement for backpropagating through the Hamiltonian dynamics. (Finzi et al., 2020) `ev:reported` p. 18 ^finzi2020generalizing-058
- The kernel MLP inside each LieConv layer is a 3-layer MLP with 32 hidden units, batch norm and Swish nonlinearities. (Finzi et al., 2020) `ev:reported` p. 18 ^finzi2020generalizing-059
- The spring datasets used systems of 6 particles with masses sampled from U(0.1, 3.1) and spring constants from U(0, 5). (Finzi et al., 2020) `ev:reported` p. 19 ^finzi2020generalizing-060
- Ground-truth spring trajectories of 5 seconds with 500 evaluation timesteps were generated by RK4 integration at relative tolerance 1e-8. (Finzi et al., 2020) `ev:reported` p. 19 ^finzi2020generalizing-061
- For QM9, a separate model was trained per task for 1000 epochs with Adam, learning rate 3e-3 and batch size 100. (Finzi et al., 2020) `ev:reported` p. 20 ^finzi2020generalizing-062
- The QM9 model takes about 48 hours to train on a single 1080Ti GPU, according to the implementation details. (Finzi et al., 2020) `ev:reported` p. 20 ^finzi2020generalizing-063
- The authors believe HLieConv inductive biases may benefit systems that do not exactly preserve energy or momentum, such as control systems. (Finzi et al., 2020) `ev:asserted` p. 9 ^finzi2020generalizing-064
- The authors list time-series, geostatistics, audio and meshes as application domains left for future work with this method. (Finzi et al., 2020) `ev:asserted` p. 9 ^finzi2020generalizing-065

## 🎯 Contributions

## 📖 Glossary

- **LieConv** — Convolutional layer equivariant to a chosen Lie group via its exp and log maps.
- **Lie group** — A group whose elements form a smooth manifold, such as rotations or translations.
- **Lie algebra** — The tangent space at the group identity; a vector space of infinitesimal transformations.
- **Lifting** — Mapping input points to group elements (plus orbit identifiers) before group convolution.
- **Haar measure** — The invariant measure on a group used to sample and integrate group elements.
- **Orbit** — The set of points reachable from one point by applying all group transformations.
- **Homogeneous space** — A space where any point can be mapped to any other by the group.
- **Equivariance** — Transforming the input by g transforms the output by the same g.
- **HLieConv** — LieConv network that models a Hamiltonian, whose symmetries give conserved quantities.
- **Noether's theorem** — Each continuous symmetry of a Hamiltonian corresponds to a conserved quantity.
- **PointConv trick** — Reordering MLP-kernel convolution through its last linear layer to save memory and compute.

## ❓ Open questions

- Can LieConv be extended to Lie groups whose exponential map is not surjective?
- How does LieConv perform on time-series, geostatistics, audio or mesh data the authors list as future work?
- Do HLieConv inductive biases help systems that do not exactly conserve energy or momentum, such as control and reinforcement learning?
- Can a numerically stable SE(2) or SE(3) exponential map enable second-order training of fully equivariant Hamiltonian models?
- Why does SO(3) equivariance alone perform much worse than the trivial group on the HOMO ablation?
- Can the gap to image-specialized methods such as E(2)-Steerable CNNs on RotMNIST be closed?

## 📝 Notes on reading

- Version read: arXiv 2002.12880v3 (24 Sep 2020), whose first page carries the ICML 2020 (PMLR 119) proceedings line; the packet lists the venue as arXiv preprint.
- The introduction claims state-of-the-art performance in all domains (p. 2), but Table 1 shows several image-specialized baselines (e.g. E(2)-Steerable 0.68%, RotEqNet 1.09%) below every LieConv RotMNIST variant; the contributions bullet more cautiously says competitive on QM9.
- The text (p. 7) refers to the HOMO ablation as Table 5.2, while it is printed as Table 3 on p. 8.
- The paper calls QM9 molecules small inorganic molecules (p. 7); the claim above says only small molecules.
- Figures 6-10 (rollouts, momentum conservation curves, data-scaling curves, neighbourhood visualizations) were only described from captions; Figure 7 and 8 values were not claimed beyond the caption statements.
- Table 6 (model symmetries) uses symbols that were garbled in extraction; its per-model invariance/equivariance marks were not claimed.
- Table 5 (full 12k RotMNIST) has an incomplete caption in extraction.

## Suggested new concepts

- Lie group equivariant convolution — the general construction of convolutions on continuous groups via exp and log maps recurs across equivariant ML.
- Noether conservation in learned Hamiltonians — links model symmetry to exact conservation laws in learned dynamics.
- Lifting to group and orbit space — the handling of non-homogeneous input spaces is a reusable design idea.
- Hamiltonian neural networks — learning a scalar energy function from trajectories is a recurring modelling approach.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — LieConv: equivariancia a cualquier grupo de Lie usando solo exp/log.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
