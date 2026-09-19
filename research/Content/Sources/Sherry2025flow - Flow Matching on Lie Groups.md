---
aliases: []
type: "source"
title: "Flow Matching on Lie Groups"
citekey: "Sherry2025flow"
doi: "10.48550/arXiv.2504.00494"
arxiv: "2504.00494"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2504.00494"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Finn M. Sherry", "Bart M. N. Smets"]
sha256: ["a56811a4a749fc12d043b674e6b6935d9ccdf90bc79a136da7cc3b9f5244fb14"]
pdf: "Content/Papers/Sherry2025flow.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 54
---

📄 PDF: [[Sherry2025flow.pdf]]

> [!abstract] One-sentence summary
> The paper generalises flow matching to Lie groups with surjective exponential maps by replacing straight lines with exponential curves, giving a simple, intrinsic, simulation-free generative model on groups such as SE(2) and SO(3).

## Abstract

Flow Matching (FM) is a recent generative modelling technique: we aim to learn how to sample from distribution $\mathfrak{X}_1$ by flowing samples from some distribution $\mathfrak{X}_0$ that is easy to sample from. The key trick is that this flow field can be trained while conditioning on the end point in $\mathfrak{X}_1$: given an end point, simply move along a straight line segment to the end point (Lipman et al. 2022). However, straight line segments are only well-defined on Euclidean space. Consequently, Chen and Lipman (2023) generalised the method to FM on Riemannian manifolds, replacing line segments with geodesics or their spectral approximations. We take an alternative point of view: we generalise to FM on Lie groups by instead substituting exponential curves for line segments. This leads to a simple, intrinsic, and fast implementation for many matrix Lie groups, since the required Lie group operations (products, inverses, exponentials, logarithms) are simply given by the corresponding matrix operations. FM on Lie groups could then be used for generative modelling with data consisting of sets of features (in $\mathbb{R}^n$) and poses (in some Lie group), e.g. the latent codes of Equivariant Neural Fields (Wessels et al. 2025). (arXiv)

## 🧠 Key ideas (atomic)

- Chen et al. proposed learning a flow from an easy distribution, such as white noise, to the target distribution for generative modelling. (Sherry & Smets, 2025) `ev:cited` p. 1 ^sherry2025flow-001
- Chen et al. suggest training a neural network to approximate the time-dependent vector field that induces the desired flow. (Sherry & Smets, 2025) `ev:cited` p. 1 ^sherry2025flow-002
- The authors describe the Lie group flow matching implementation as fast for many matrix Lie groups. (Sherry & Smets, 2025) `ev:abstract` p. 1 ^sherry2025flow-003
- The naive flow matching loss cannot be computed because only samples from the two distributions, not the inducing vector field, are available. (Sherry & Smets, 2025) `ev:asserted` p. 2 ^sherry2025flow-004
- Chen et al. instead define a loss on the final flow, which requires simulating the flow during training. (Sherry & Smets, 2025) `ev:cited` p. 2 ^sherry2025flow-005
- According to the authors, simulating the flow during training makes optimisation more complicated and expensive. (Sherry & Smets, 2025) `ev:asserted` p. 2 ^sherry2025flow-006
- Lipman et al. developed Flow Matching by conditioning the vector field on the end point, moving along a straight line segment. (Sherry & Smets, 2025) `ev:cited` p. 2 ^sherry2025flow-007
- The conditional flow matching loss is computable since one can sample time uniformly, the source distribution, and the target distribution. (Sherry & Smets, 2025) `ev:asserted` p. 2 ^sherry2025flow-008
- The gradients of the naive and conditional flow matching losses with respect to network parameters coincide, following Lipman et al. (Sherry & Smets, 2025) `ev:cited` p. 2 ^sherry2025flow-009
- Chen and Lipman generalised flow matching to Riemannian manifolds, defining the conditional vector field by differentiating a premetric. (Sherry & Smets, 2025) `ev:cited` p. 2 ^sherry2025flow-010
- Geodesics are only easy to compute on simple manifolds such as spheres, so other manifolds need a tractable premetric such as spectral distances. (Sherry & Smets, 2025) `ev:asserted` p. 2 ^sherry2025flow-011
- On manifolds without easy geodesics, the Riemannian flow matching conditional vector field typically still must be simulated, according to the authors. (Sherry & Smets, 2025) `ev:asserted` p. 2 ^sherry2025flow-012
- The authors generalise flow matching to Lie groups with surjective exponential maps, using a conditional flow field whose integral curves are exponential curves. (Sherry & Smets, 2025) `ev:asserted` p. 2 ^sherry2025flow-013
- On matrix Lie groups, the required products, inverses, exponentials and logarithms are given by the corresponding matrix operations. (Sherry & Smets, 2025) `ev:asserted` p. 2 ^sherry2025flow-014
- Because the method is intrinsic, all intermediate distributions of the flow live on the Lie group by construction, the authors state. (Sherry & Smets, 2025) `ev:asserted` p. 2 ^sherry2025flow-015
- The authors show that their framework generalises Euclidean flow matching by recasting it as flow matching on the translation group. (Sherry & Smets, 2025) `ev:computed` p. 2 ^sherry2025flow-016
- The proof-of-concept experiments cover three Lie groups: SE(2), SO(3), and the product group SE(2) × R2. (Sherry & Smets, 2025) `ev:reported` p. 3 ^sherry2025flow-017
- The authors propose that flow matching on Lie groups could use the latent space of Equivariant Neural Fields for image generation. (Sherry & Smets, 2025) `ev:asserted` p. 3 ^sherry2025flow-018
- The authors describe the Equivariant Neural Field latent space as more geometrically interpretable than the variational autoencoders commonly used in image generation. (Sherry & Smets, 2025) `ev:asserted` p. 3 ^sherry2025flow-019
- There does not appear to be a complete classification of Lie groups with a surjective exponential map, the authors remark. (Sherry & Smets, 2025) `ev:asserted` p. 3 ^sherry2025flow-020
- The real special linear group is an example where the exponential map fails to be surjective. (Sherry & Smets, 2025) `ev:cited` p. 3 ^sherry2025flow-021
- Special unitary groups, similarity groups and Heisenberg groups are named as Lie groups that do have a surjective exponential map. (Sherry & Smets, 2025) `ev:asserted` p. 3 ^sherry2025flow-022
- The authors argue a left-invariant metric tensor field is natural, since left-action push-forwards then become isometries. (Sherry & Smets, 2025) `ev:asserted` p. 3 ^sherry2025flow-023
- With a surjective exponential map, any two group elements can be connected by an exponential curve built from the group logarithm. (Sherry & Smets, 2025) `ev:computed` p. 4 ^sherry2025flow-024
- Proposition 1 proves that the proposed Lie group conditional vector field has the exponential curves ending in the target element as integral curves. (Sherry & Smets, 2025) `ev:computed` p. 4 ^sherry2025flow-025
- Although the loss needs a Riemannian metric, the authors were not able to find a premetric inducing their conditional vector field. (Sherry & Smets, 2025) `ev:asserted` p. 4 ^sherry2025flow-026
- The logarithmic distance premetric gives rise to the Lie group conditional vector field only in specific cases, such as bi-invariant groups. (Sherry & Smets, 2025) `ev:asserted` p. 4 ^sherry2025flow-027
- Theorem 1 states that the gradients of the Lie group naive and conditional flow matching losses with respect to network parameters coincide. (Sherry & Smets, 2025) `ev:computed` p. 4 ^sherry2025flow-028
- The proof of Theorem 1 applies a general result of Lipman et al., using that the squared norm is a Bregman divergence. (Sherry & Smets, 2025) `ev:cited` p. 4 ^sherry2025flow-029
- On the translation group Rd, the exponential curve reduces to a line segment, so the Lie group loss reduces to the Euclidean one. (Sherry & Smets, 2025) `ev:computed` p. 5 ^sherry2025flow-030
- SE(2) is defined as the group of roto-translations of the plane, with each rotation identified with an angle. (Sherry & Smets, 2025) `ev:reported` p. 5 ^sherry2025flow-031
- The paper gives closed-form exponential and logarithm maps for SE(2), with the logarithm domain restricted to angles in [−π, π). (Sherry & Smets, 2025) `ev:computed` p. 5 ^sherry2025flow-032
- Matrix representations let the method reuse existing implementations, at the cost of more memory than a hand-crafted implementation on group elements. (Sherry & Smets, 2025) `ev:asserted` p. 5 ^sherry2025flow-033
- Flow matching was implemented in PyTorch, which provides matrix multiplication, inverses and exponentials but no matrix logarithm. (Sherry & Smets, 2025) `ev:reported` p. 6 ^sherry2025flow-034
- For SO(3), represented by 3×3 orthogonal matrices with determinant 1, the logarithm is computed with Rodrigues' formula. (Sherry & Smets, 2025) `ev:reported` p. 6 ^sherry2025flow-035
- Because SO(3) is compact and admits a bi-invariant metric, flow matching on it recovers Riemannian flow matching. (Sherry & Smets, 2025) `ev:asserted` p. 6 ^sherry2025flow-036
- If flow matching works on groups G and H, it extends to powers of their product, since operations are inherited. (Sherry & Smets, 2025) `ev:asserted` p. 6 ^sherry2025flow-037
- Product-group flow matching covers the space where latent codes of Equivariant Neural Fields live, a product of SE(2) and Rd. (Sherry & Smets, 2025) `ev:cited` p. 6 ^sherry2025flow-038
- The framework can be generalised to homogeneous spaces by projecting exponential curves in the group onto the space. (Sherry & Smets, 2025) `ev:asserted` p. 6 ^sherry2025flow-039
- On homogeneous spaces there are typically infinitely many connecting group elements, so a single exponential curve must be selected. (Sherry & Smets, 2025) `ev:asserted` p. 6 ^sherry2025flow-040
- For the SE(3) homogeneous space of three-dimensional positions and orientations, prior work found a computationally convenient curve choice. (Sherry & Smets, 2025) `ev:cited` p. 6 ^sherry2025flow-041
- The vector field is learned by a multilayer perceptron with four hidden layers and a width of 64 neurons. (Sherry & Smets, 2025) `ev:reported` p. 6 ^sherry2025flow-042
- The network maps a group element and time to vector components in the tangent space with respect to a fixed left-invariant frame. (Sherry & Smets, 2025) `ev:reported` p. 6 ^sherry2025flow-043
- The learned flow is integrated with the Lie group exponential, so the flow remains on the group without constraints or projection. (Sherry & Smets, 2025) `ev:asserted` p. 6 ^sherry2025flow-044
- The authors contrast this with Riemannian flow matching, which imposes network constraints or projects back onto the manifold. (Sherry & Smets, 2025) `ev:cited` p. 6 ^sherry2025flow-045
- The authors release implementations and animations of the learned flows for all three groups in a public GitHub repository. (Sherry & Smets, 2025) `ev:reported` p. 6 ^sherry2025flow-046
- SE(2) and SO(3) points are visualised as arrows on the plane and sphere, as spaces of positions and orientations. (Sherry & Smets, 2025) `ev:reported` p. 7 ^sherry2025flow-047
- For SE(2) and SO(3), the experiments flow from a horizontal line to a vertical line and from a vertical line to a circle. (Sherry & Smets, 2025) `ev:reported` p. 7 ^sherry2025flow-048
- For SE(2) × R2, a single pair of distributions is flowed, with SE(2) and R2 components plotted separately. (Sherry & Smets, 2025) `ev:reported` p. 7 ^sherry2025flow-049
- In all cases, the flowed samples at t = 1 indeed reasonably match the target distribution, according to the authors. (Sherry & Smets, 2025) `ev:measured` p. 7 ^sherry2025flow-050
- In the simple cases that flow from lines to lines, the intermediate interpolant distributions also behave nicely, the authors report. (Sherry & Smets, 2025) `ev:measured` p. 7 ^sherry2025flow-051
- When flowing from a line to a circle, the interpolants look messier, which the authors attribute to exponential curves that can be quite intricate. (Sherry & Smets, 2025) `ev:measured` p. 7 ^sherry2025flow-052
- The authors conclude that their generalisation has an intrinsic, simple, and simulation-free implementation for many Lie groups. (Sherry & Smets, 2025) `ev:asserted` p. 9 ^sherry2025flow-053
- The authors suggest Lie group flow matching could be used for generative modelling of data combining feature sets and poses. (Sherry & Smets, 2025) `ev:asserted` p. 9 ^sherry2025flow-054

## 🎯 Contributions

## 📖 Glossary

- **Flow Matching** — Simulation-free training of a vector field whose flow transports a source distribution to a target.
- **Conditional vector field** — Vector field conditioned on an end point, used to build a computable training loss.
- **Lie group** — Smooth manifold with a compatible group structure, such as rotations or roto-translations.
- **Lie group exponential** — Map from the Lie algebra to the group via one-parameter subgroups.
- **Exponential curve** — Curve g0 exp(t log(g0^-1 g1)) connecting two group elements.
- **Premetric** — Distance-like function whose gradient defines the conditional field in Riemannian flow matching.
- **Bi-invariant metric** — Metric invariant under left and right group actions; geodesics equal exponential curves.
- **SE(2)** — Special Euclidean group of planar roto-translations, i.e. positions with orientations.
- **Homogeneous space** — Manifold on which a Lie group acts transitively.
- **Equivariant Neural Fields** — Neural fields whose latent codes are sets of features attached to group poses.

## ❓ Open questions

- How does Lie group flow matching compare quantitatively (sample quality, training cost, speed) with Riemannian flow matching on the same groups?
- Does a premetric exist that induces the proposed conditional vector field on non-bi-invariant groups?
- How should a single exponential curve be selected on general homogeneous spaces where infinitely many connecting group elements exist?
- Does the method scale to generative modelling of real data, such as Equivariant Neural Field latent codes for images?
- How can flow matching be extended to Lie groups whose exponential map is not surjective, such as the real special linear group?
- Can the messier interpolants between complex distributions (line to circle) be improved by a different choice of curves?

## 📝 Notes on reading

The version read is arXiv 2504.00494v2 (3 Jul 2025). The PDF abstract restricts the generalisation to Lie groups with surjective exponential maps; the registry abstract omits this qualifier. The registry abstract calls the implementation fast, while the body says simple and simulation-free; no timing is reported. The experiments (Figs. 1-3) are qualitative only: samples from X0, the flowed interpolants and the targets on SE(2), SO(3) and SE(2) × R2, with no quantitative metric; the figures were only described, not claimed. Page 3 has a truncated sentence (variational autoencoders "to reduce the ;"). On page 4 the text says "we generalise the loss function (9)" where (3) appears to be meant. The explicit SE(2) exponential and logarithm formulas (Eqs. 11-12) and Rodrigues' formula (Eq. 13) were extracted with broken layout and are not reproduced.

## Suggested new concepts

- Flow Matching — core generative modelling technique that many related sources build on.
- Riemannian Flow Matching — the geodesic/premetric-based generalisation this paper positions itself against.
- Lie group exponential and logarithm — the operations that make the method intrinsic and simulation-free.
- Equivariant Neural Fields — proposed downstream latent space of features and poses for Lie group generative modelling.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H2.** Generaliza el flow matching a grupos de Lie con curvas exponenciales, sin simulación, para generar agarres o acciones en SE(3).
