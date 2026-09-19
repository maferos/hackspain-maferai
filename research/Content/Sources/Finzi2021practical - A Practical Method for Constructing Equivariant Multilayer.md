---
aliases: []
type: "source"
title: "A Practical Method for Constructing Equivariant Multilayer Perceptrons for Arbitrary Matrix Groups"
citekey: "Finzi2021practical"
doi: "10.48550/arXiv.2104.09459"
arxiv: "2104.09459"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2104.09459"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Marc Finzi", "Max Welling", "Andrew Gordon Wilson"]
sha256: ["1070318df41d4a83e0b004626a35f513129b9472bf0e5bbf7f690c2f6adb0d96"]
pdf: "Content/Papers/Finzi2021practical.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Finzi2021practical.pdf]]

> [!abstract] One-sentence summary
> The paper reduces equivariance to any matrix group to a nullspace problem over group generators, solves it with a fast iterative method, and builds equivariant MLPs (EMLP) that beat non-equivariant baselines on physics tasks.

## Abstract

Symmetries and equivariance are fundamental to the generalization of neural networks on domains such as images, graphs, and point clouds. Existing work has primarily focused on a small number of groups, such as the translation, rotation, and permutation groups. In this work we provide a completely general algorithm for solving for the equivariant layers of matrix groups. In addition to recovering solutions from other works as special cases, we construct multilayer perceptrons equivariant to multiple groups that have never been tackled before, including $\mathrm{O}(1,3)$, $\mathrm{O}(5)$, $\mathrm{Sp}(n)$, and the Rubik's cube group. Our approach outperforms non-equivariant baselines, with applications to particle physics and dynamical systems. We release our software library to enable researchers to construct equivariant layers for arbitrary matrix groups. (arXiv)

## 🧠 Key ideas (atomic)

- The authors propose a general formulation for equivariant multilayer perceptrons whose inputs and outputs transform under finite dimensional representations of a symmetry group. (Finzi et al., 2021) `ev:asserted` p. 1 ^finzi2021practical-001
- Convolutional layers, permutation equivariant deep sets, graph layers and point cloud layers all arise as special cases of the proposed general algorithm. (Finzi et al., 2021) `ev:asserted` p. 1 ^finzi2021practical-002
- The authors prove that equivariance to matrix groups reduces to M + D constraints, with M discrete generators and D the group dimension. (Finzi et al., 2021) `ev:computed` p. 1 ^finzi2021practical-003
- The paper provides a polynomial time algorithm that solves these equivariance constraints for any finite dimensional representation of the group. (Finzi et al., 2021) `ev:asserted` p. 1 ^finzi2021practical-004
- With an added bilinear layer, EMLP is a general equivariant architecture applied to a new group by specifying the group generators. (Finzi et al., 2021) `ev:asserted` p. 1 ^finzi2021practical-005
- Methods built on irreducible representations were limited to rotation groups, with SO+(1, 3) in Bogatskiy et al. (2020) the only exception. (Finzi et al., 2021) `ev:cited` p. 2 ^finzi2021practical-006
- Achieving equivariance for continuous groups with the regular representation is fundamentally challenging, since that representation is infinite dimensional. (Finzi et al., 2021) `ev:asserted` p. 2 ^finzi2021practical-007
- The explicit algorithm of van der Pol et al. (2020) scales with group size and becomes impossible for continuous groups like SO(n). (Finzi et al., 2021) `ev:cited` p. 2 ^finzi2021practical-008
- Imposing invariance for every group element reduces to one linear constraint per infinitesimal generator plus one per discrete generator. (Finzi et al., 2021) `ev:computed` p. 4 ^finzi2021practical-009
- Stacking all generator constraints into one matrix, every symmetric solution lies in its nullspace, which a singular value decomposition computes. (Finzi et al., 2021) `ev:computed` p. 4 ^finzi2021practical-010
- For the cyclic translation group Zn, solving the constraints gives n circulant basis matrices, precisely the matrix form of convolution. (Finzi et al., 2021) `ev:computed` p. 4 ^finzi2021practical-011
- For permutation equivariant maps from Rn to itself, solving the constraints yields the two-dimensional deep sets basis of Zaheer et al. (Finzi et al., 2021) `ev:computed` p. 4 ^finzi2021practical-012
- The authors note that the locality bias restricting convolution filters to 3 × 3 is not a consequence of equivariance. (Finzi et al., 2021) `ev:asserted` p. 4 ^finzi2021practical-013
- Solving just for the permutation generators, instead of the combinatorially large constraint, yields the same solutions as equivariant graph networks. (Finzi et al., 2021) `ev:computed` p. 5 ^finzi2021practical-014
- For the GCNN group of translations and 90° rotations, the solved constraint gives the G-convolutional layer embedded in a dense matrix. (Finzi et al., 2021) `ev:computed` p. 5 ^finzi2021practical-015
- Computing the equivariant basis directly with SVD is too costly for all but very small representations with dimension below 5000. (Finzi et al., 2021) `ev:asserted` p. 5 ^finzi2021practical-016
- For direct sum representations, the constraints separate into independent blocks, one per pair of input and output representations. (Finzi et al., 2021) `ev:computed` p. 5 ^finzi2021practical-017
- Unlike steerable CNNs using analytic irreducible solutions, the method needs no Clebsch-Gordan coefficients regardless of the representation used. (Finzi et al., 2021) `ev:asserted` p. 6 ^finzi2021practical-018
- The nullspace is found by gradient descent on the squared Frobenius norm of CQ, needing only matrix vector multiplies with C. (Finzi et al., 2021) `ev:asserted` p. 6 ^finzi2021practical-019
- Iterative doubling of the maximum rank means the true rank of the nullspace need not be known beforehand. (Finzi et al., 2021) `ev:asserted` p. 6 ^finzi2021practical-020
- For large discrete groups like Sn, the approach gives an exponential speedup over van der Pol et al., from O(n!) to O(n). (Finzi et al., 2021) `ev:computed` p. 6 ^finzi2021practical-021
- As a heuristic, the channels of intermediate layers are allocated uniformly between tensor ranks, while data types set the input and output layers. (Finzi et al., 2021) `ev:reported` p. 6 ^finzi2021practical-022
- EMLP uses the gated nonlinearities of Weiler et al. (2018), which reduce to Swish for scalars and regular representations. (Finzi et al., 2021) `ev:reported` p. 7 ^finzi2021practical-023
- The authors prove that gated nonlinearities are not sufficient for universality with general groups and representations, unlike pointwise nonlinearities for permutation subgroups. (Finzi et al., 2021) `ev:computed` p. 7 ^finzi2021practical-024
- To address this limitation, a cheap bilinear layer performs tensor contractions on pairs of input objects that produce a given output type. (Finzi et al., 2021) `ev:asserted` p. 7 ^finzi2021practical-025
- The synthetic O(5) invariant task regresses a scalar from two vectors in 5 dimensions, comparing EMLP-SO(5) and EMLP-O(5) against MLP baselines. (Finzi et al., 2021) `ev:reported` p. 7 ^finzi2021practical-026
- The O(3) equivariant task predicts the moment of inertia matrix from the masses and positions of 5 point masses. (Finzi et al., 2021) `ev:reported` p. 7 ^finzi2021practical-027
- The MLP baseline for the inertia task uses equivariant data augmentation, transforming inputs by a random O(3) matrix and outputs accordingly. (Finzi et al., 2021) `ev:reported` p. 7 ^finzi2021practical-028
- The Lorentz task fits the matrix element of electron muon scattering, taking four four-momenta as input and producing one scalar output. (Finzi et al., 2021) `ev:reported` p. 8 ^finzi2021practical-029
- The Lorentz task compares EMLP equivariant to SO+(1, 3), SO(1, 3) and O(1, 3) against an MLP using O(1, 3) augmentation. (Finzi et al., 2021) `ev:reported` p. 8 ^finzi2021practical-030
- Across dataset sizes and tasks, EMLP consistently outperforms the baseline MLP trained with and without data augmentation, often by orders of magnitude. (Finzi et al., 2021) `ev:measured` p. 8 ^finzi2021practical-031
- The dynamics experiment learns a 3D double spring pendulum with O(2) symmetry about the z-axis plus Hamiltonian structure. (Finzi et al., 2021) `ev:reported` p. 8 ^finzi2021practical-032
- The pendulum state space is not a homogeneous space, a setting the authors describe as very little explored in equivariance literature. (Finzi et al., 2021) `ev:asserted` p. 8 ^finzi2021practical-033
- Exploiting the O(2) symmetry and its subgroups with EMLP improves performance for both Neural ODE and HNN models on the pendulum. (Finzi et al., 2021) `ev:measured` p. 8 ^finzi2021practical-034
- The O(2) EMLP Neural ODE reached a geometric mean rollout relative error of 0.019(1), against 0.048 for the MLP Neural ODE. (Finzi et al., 2021) `ev:measured` p. 9 ^finzi2021practical-035
- The O(2) EMLP HNN reached a geometric mean rollout relative error of 0.012(2), against 0.028 for the ordinary MLP HNN. (Finzi et al., 2021) `ev:measured` p. 9 ^finzi2021practical-036
- Enforcing the continuous rotation symmetry in the EMLP-HNN models yields conservation of angular momentum about the z-axis in learned simulations. (Finzi et al., 2021) `ev:measured` p. 9 ^finzi2021practical-037
- The discrete dihedral group D6 still yields approximate angular momentum conservation, whereas the coarser D2 symmetry does not. (Finzi et al., 2021) `ev:measured` p. 9 ^finzi2021practical-038
- None of the Neural ODE models conserve angular momentum, as Noether's theorem applies to Hamiltonians and not to general ODEs. (Finzi et al., 2021) `ev:measured` p. 9 ^finzi2021practical-039
- LieConv models assume permutation equivariance, which the pivot of the double spring pendulum system breaks, unlike the general EMLP. (Finzi et al., 2021) `ev:asserted` p. 9 ^finzi2021practical-040
- Dense matrix multiplies make it slow to train EMLP models the size of convnets or large graph networks with specialized implementations. (Finzi et al., 2021) `ev:asserted` p. 9 ^finzi2021practical-041
- The authors suggest that with the right techniques this apparent generality-specialization tradeoff may be overcome in future work. (Finzi et al., 2021) `ev:asserted` p. 9 ^finzi2021practical-042
- Theorem 1 states the generator constraints are necessary and sufficient for symmetry in real Lie groups with finitely many connected components. (Finzi et al., 2021) `ev:computed` p. 12 ^finzi2021practical-043
- The authors prove that the gradient descent nullspace method converges exponentially to the correct nullspace with probability 1. (Finzi et al., 2021) `ev:computed` p. 13 ^finzi2021practical-044
- Empirically, the iterate converges to the limits of floating point precision within 300 iterations across a range of groups and tensor representations. (Finzi et al., 2021) `ev:measured` p. 13 ^finzi2021practical-045
- Theorem 2 shows that for groups like SO(2) and O(3), networks with rank-preserving tensor nonlinearities cannot approximate even simple equivariant functions. (Finzi et al., 2021) `ev:computed` p. 14 ^finzi2021practical-046
- For O(3) with a vector input, Norm-ReLU or gated networks can only output a constant and cannot fit the vector norm. (Finzi et al., 2021) `ev:computed` p. 14 ^finzi2021practical-047
- The authors state that Maron et al. (2018) basis sometimes contains linearly dependent solutions, overcounting its size when n is small. (Finzi et al., 2021) `ev:asserted` p. 15 ^finzi2021practical-048
- For the permutation group S4, the computed symmetric subspace rank for T5 tensors is 51, below the Bell number of 52. (Finzi et al., 2021) `ev:computed` p. 15 ^finzi2021practical-049
- For the Rubik's cube group in its 48 dimensional representation, the equivariant basis ranks are 2, 6 and 22 for T1 to T3. (Finzi et al., 2021) `ev:computed` p. 15 ^finzi2021practical-050
- For the Rubik's cube T4 tensors of size 5308416, the solver ran with rmax = 20 before running out of GPU memory. (Finzi et al., 2021) `ev:measured` p. 15 ^finzi2021practical-051
- The Levi-Civita symbol appears in the SO(n) basis when n = k but is absent for O(n), lacking reflection equivariance. (Finzi et al., 2021) `ev:computed` p. 16 ^finzi2021practical-052
- For T(8,0) tensors, the symmetric subspace rank is 196 for SO+(1, 3) but 105 for the full Lorentz group O(1, 3). (Finzi et al., 2021) `ev:computed` p. 16 ^finzi2021practical-053
- Replacing the objective with a conjugate transpose version and a complex SVD lets the method solve bases for groups like SU(n). (Finzi et al., 2021) `ev:asserted` p. 17 ^finzi2021practical-054
- Adding a new group to the Jax implementation requires specifying discrete generators plus a Lie algebra basis with their base representations. (Finzi et al., 2021) `ev:reported` p. 17 ^finzi2021practical-055
- For new representations, the induced Lie algebra representation can be computed automatically using autograd Jacobian vector products rather than manually. (Finzi et al., 2021) `ev:reported` p. 17 ^finzi2021practical-056
- The synthetic experiments use 3 EMLP layers of c = 384 channels, followed by a single equivariant linear layer to the output type. (Finzi et al., 2021) `ev:reported` p. 18 ^finzi2021practical-057
- All synthetic models are trained with batchsize 500 using the Adam optimizer, with baseline MLPs having 3 hidden layers of 384 units. (Finzi et al., 2021) `ev:reported` p. 18 ^finzi2021practical-058
- Training the EMLP takes a couple of minutes, whereas the baseline MLP model trains in under 1 minute on these tasks. (Finzi et al., 2021) `ev:measured` p. 18 ^finzi2021practical-059
- Each synthetic dataset separates out a test set of size 5000 and a validation set of size 1000 used for early stopping. (Finzi et al., 2021) `ev:reported` p. 18 ^finzi2021practical-060
- The double spring dataset holds 1500 trajectory chunks, split into 500 for each of the train, validation and test sets. (Finzi et al., 2021) `ev:reported` p. 18 ^finzi2021practical-061

## 🎯 Contributions


## 📖 Glossary

- **Equivariance** — transforming the input by a group element transforms the output by the corresponding representation.
- **Group representation** — a map assigning each group element an invertible matrix acting on a vector space.
- **Lie algebra** — tangent space at the identity of a Lie group, spanned by infinitesimal generators.
- **Discrete generator** — group element whose products and inverses, with the exponential map, produce the whole group.
- **Equivariant basis** — basis of the nullspace of stacked generator constraints; spans all equivariant linear maps.
- **EMLP** — equivariant MLP stacking equivariant linear, bilinear and gated nonlinearity layers for a chosen group.
- **Gated nonlinearity** — multiplies each tensor feature by a sigmoid of an associated scalar gate.
- **Krylov nullspace method** — gradient descent on the squared constraint residual followed by a small SVD.
- **Tensor representation T(p,q)** — representation on p copies of V and q copies of its dual, tensored.
- **Parity property** — some group elements act as the negative of others, zeroing odd-rank invariant tensors.

## ❓ Open questions

- Can the generality-specialization tradeoff be overcome so EMLP trains at the scale of convnets or large graph networks?
- Which nonlinearities or layer types give provable universality for general groups and non-permutation representations?
- How does the method extend to anti-linear maps for complex groups such as SU(n)?
- Can the numerical solver scale beyond the GPU memory limit hit for Rubik's cube T4 tensors?
- Can the generator-based construction be extended to infinite dimensional representations in practice?
- How well does EMLP perform on real, non-synthetic datasets rather than generated physics tasks?

## 📝 Notes on reading

Version read: arXiv 2104.09459v1 (19 Apr 2021), the preprint, matching the packet identifier.

The extraction garbles superscripts and exponents: the Rubik's cube group size appears as 4 × 1019 (4 × 10^19 in the paper), the SVD runtime O((M + D)m3), the learning rate 3 × 10−3, the Zn rank rule r = nk−1, and the T4 size 484. These numbers were not claimed as printed; the claims use wording or the unambiguous values instead. Equations in Sections 3 to 5 and Appendices B, C and H are partly garbled but their conclusions are stated in prose and claimed from there.

Figures 1 to 4 (unifying diagram, equivariant bases, EMLP layer diagram) and the Figure 5 data-efficiency curves were only described; Figure 5 test MSE values are not readable from the text, so only the qualitative outperformance statement was claimed. Figure 6 (middle) shows angular momentum error for D(2), D(6), SO(2), MLP and O(2), while Table 1 lists only O(2), SO(2), D6 and MLP; the D2 result is therefore from the text only.

Table 1 standard deviations for SO(2) and D6 N-ODEs (0.051(36), 0.036(25)) are large relative to their means. Appendix A refers to Appendix I and J for hyperparameters and datasets; these match sections I and J.

## Suggested new concepts

- Equivariant multilayer perceptron (EMLP) — a general architecture reused across many groups and physics applications.
- Equivariance constraint solving via group generators — the core reduction of infinite constraints to M + D linear equations.
- Lorentz-equivariant networks — relevant to particle physics models and compared across SO+(1,3), SO(1,3), O(1,3).
- Symmetry and conservation laws in learned dynamics — links equivariant Hamiltonians to Noether's theorem and angular momentum conservation.
- Universality of equivariant networks — the paper proves limits of gated nonlinearities, motivating bilinear layers.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** EMLP: resuelve las restricciones de equivarianza con los generadores del álgebra de Lie para cualquier grupo matricial ($SO(3)$, $SE(3)$, $O(1,3)$), sin derivar la teoría de representaciones a mano.
