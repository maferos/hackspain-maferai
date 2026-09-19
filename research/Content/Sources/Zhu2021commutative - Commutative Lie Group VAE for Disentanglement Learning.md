---
aliases: []
type: "source"
title: "Commutative Lie Group VAE for Disentanglement Learning"
citekey: "Zhu2021commutative"
doi: "10.48550/arXiv.2106.03375"
arxiv: "2106.03375"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2106.03375"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Xinqi Zhu", "Chang Xu", "Dacheng Tao"]
sha256: ["fe5b85c71e01efa74e133518531ec86815182f2f3a78a52bfd60bcf3b3c7784b"]
pdf: "Content/Papers/Zhu2021commutative.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Zhu2021commutative.pdf]]

> [!abstract] One-sentence summary
> The paper replaces the fixed vector-space latent of VAEs with an adaptive Lie group, parameterized through a learned Lie algebra basis with commutativity constraints, and reports state-of-the-art unsupervised disentanglement on DSprites and 3DShapes without statistical-independence penalties.

## Abstract

We view disentanglement learning as discovering an underlying structure that equivariantly reflects the factorized variations shown in data. Traditionally, such a structure is fixed to be a vector space with data variations represented by translations along individual latent dimensions. We argue this simple structure is suboptimal since it requires the model to learn to discard the properties (e.g. different scales of changes, different levels of abstractness) of data variations, which is an extra work than equivariance learning. Instead, we propose to encode the data variations with groups, a structure not only can equivariantly represent variations, but can also be adaptively optimized to preserve the properties of data variations. Considering it is hard to conduct training on group structures, we focus on Lie groups and adopt a parameterization using Lie algebra. Based on the parameterization, some disentanglement learning constraints are naturally derived. A simple model named Commutative Lie Group VAE is introduced to realize the group-based disentanglement learning. Experiments show that our model can effectively learn disentangled representations without supervision, and can achieve state-of-the-art performance without extra constraints. (arXiv)

## 🧠 Key ideas (atomic)

- Existing unsupervised disentanglement methods usually learn the equivariance mapping on a fixed vector space, which the authors argue is suboptimal. (Zhu et al., 2021) `ev:asserted` p. 1 ^zhu2021commutative-001
- The authors hypothesize that equivariance is more likely to be learned with an adaptive equivariant structure fitted to the data variations. (Zhu et al., 2021) `ev:asserted` p. 1 ^zhu2021commutative-002
- Previous group-based disentanglement methods use predefined group structures, which the authors describe as neither adaptive nor generalizable. (Zhu et al., 2021) `ev:cited` p. 1 ^zhu2021commutative-003
- According to the authors, previous group-based disentanglement models with predefined groups cannot be learned without any supervision. (Zhu et al., 2021) `ev:cited` p. 1 ^zhu2021commutative-004
- The authors claim this is the first work to learn unsupervised disentangled representations based on adaptive group structures, to their knowledge. (Zhu et al., 2021) `ev:asserted` p. 1 ^zhu2021commutative-005
- The authors model continuous data variations with Lie groups, parameterized through a Lie algebra to enable practical training. (Zhu et al., 2021) `ev:reported` p. 2 ^zhu2021commutative-006
- Without extra constraints like statistical independence, the group-based model achieves state-of-the-art results on the DSprites and 3DShapes datasets. (Zhu et al., 2021) `ev:measured` p. 2 ^zhu2021commutative-007
- Earlier symmetry-based models by Caselles-Dupré et al. and Quessard et al. rely on paired data with action labels for training. (Zhu et al., 2021) `ev:cited` p. 2 ^zhu2021commutative-008
- Painter et al. estimate actions with reinforcement learning but still require paired samples of elemental transformations for training. (Zhu et al., 2021) `ev:cited` p. 2 ^zhu2021commutative-009
- Group-equivariant convolution works learn predefined, usually semantic-agnostic symmetries, whereas this work discovers unknown group structures representing semantic variations. (Zhu et al., 2021) `ev:asserted` p. 2 ^zhu2021commutative-010
- The method chooses the group identity as the representation of a canonical data point, so every sample receives a group representation. (Zhu et al., 2021) `ev:reported` p. 3 ^zhu2021commutative-011
- The authors state the group can then be learned from static observations, since each observation represents a transformation from the canonical point. (Zhu et al., 2021) `ev:asserted` p. 3 ^zhu2021commutative-012
- The authors restrict attention to Lie groups, arguing that most attributes in data consist of continuous variations. (Zhu et al., 2021) `ev:asserted` p. 3 ^zhu2021commutative-013
- Lie groups are parameterized by a basis in the Lie algebra, mapped to the group through the matrix exponential. (Zhu et al., 2021) `ev:reported` p. 3 ^zhu2021commutative-014
- The Lie algebra basis is optimized as network weights to find an adaptive group structure, with each sample identified by its coordinates. (Zhu et al., 2021) `ev:reported` p. 4 ^zhu2021commutative-015
- Placing prior distributions on the Lie algebra coordinates enables sampling that simulates a distribution on the group structure. (Zhu et al., 2021) `ev:asserted` p. 4 ^zhu2021commutative-016
- Without constraints, the Lie algebra parameterization cannot guarantee decomposition of the group into subgroups each parameterized by a single coordinate. (Zhu et al., 2021) `ev:asserted` p. 4 ^zhu2021commutative-017
- Proposition 1 shows that if the basis elements pairwise commute, the exponential of their sum factorizes into one-parameter subgroups. (Zhu et al., 2021) `ev:computed` p. 4 ^zhu2021commutative-018
- The method cannot disentangle variations that no commutative Lie group represents equivariantly, such as 3D rotation decomposition along three orthogonal axes. (Zhu et al., 2021) `ev:asserted` p. 4 ^zhu2021commutative-019
- Proposition 2 shows that if basis products vanish for distinct indices, the off-diagonal Hessian of the group map is zero. (Zhu et al., 2021) `ev:computed` p. 4 ^zhu2021commutative-020
- The Hessian condition is stricter than Proposition 1, since zero mutual products imply that the basis elements commute. (Zhu et al., 2021) `ev:asserted` p. 4 ^zhu2021commutative-021
- Unlike the original Hessian Penalty on feature maps, this method penalizes only the Lie algebra basis, a simpler implementation. (Zhu et al., 2021) `ev:asserted` p. 4 ^zhu2021commutative-022
- The bottleneck-VAE, a VAE variant introduced here, forces a layer of encoder features to match a layer of decoder features. (Zhu et al., 2021) `ev:reported` p. 4 ^zhu2021commutative-023
- The bottleneck-VAE maximizes a new lower bound of the data log-likelihood built from two latent variables z and t. (Zhu et al., 2021) `ev:computed` p. 4 ^zhu2021commutative-024
- The group encoder is a two-layer MLP that produces Lie algebra coordinates using the reparameterization trick. (Zhu et al., 2021) `ev:reported` p. 5 ^zhu2021commutative-025
- The output feature of the image encoder is forwarded directly to the image decoder with a probability of 0.2. (Zhu et al., 2021) `ev:reported` p. 5 ^zhu2021commutative-026
- For each input coordinate, the exponential mapping layer learns one square Lie algebra basis matrix acting on the vector space. (Zhu et al., 2021) `ev:reported` p. 5 ^zhu2021commutative-027
- The exponential mapping layer relies on the differentiable matrix exponential implementations built into TensorFlow and PyTorch. (Zhu et al., 2021) `ev:reported` p. 5 ^zhu2021commutative-028
- The authors argue the bottleneck-VAE is essential because, without feature sharing, the encoder learns equivariance on a vector space instead. (Zhu et al., 2021) `ev:asserted` p. 5 ^zhu2021commutative-029
- A Lie Group VAE with either the decomposition constraint or the Hessian constraint on its basis is named a Commutative Lie Group VAE. (Zhu et al., 2021) `ev:reported` p. 5 ^zhu2021commutative-030
- The DSprites dataset contains 737,280 images of 64 × 64 2D shapes rendered from 5 independent generative factors. (Zhu et al., 2021) `ev:reported` p. 6 ^zhu2021commutative-031
- The 3DShapes dataset contains 480,000 images of 3D shapes at 64 × 64 generated from 6 independent factors. (Zhu et al., 2021) `ev:reported` p. 6 ^zhu2021commutative-032
- All reported disentanglement scores, using the FactorVAE metric, SAP, MIG and DCI Disentanglement, are averaged over 10 random runs. (Zhu et al., 2021) `ev:reported` p. 6 ^zhu2021commutative-033
- Ablation studies use a random 9/10 training and 1/10 test split in each run, scoring on the test set. (Zhu et al., 2021) `ev:reported` p. 6 ^zhu2021commutative-034
- In the DSprites ablation, adding the bottleneck raised the plain VAE FVM from 69.4±10.9 to 74.6±8.1. (Zhu et al., 2021) `ev:measured` p. 6 ^zhu2021commutative-035
- Adding the exponential mapping layer to the bottleneck-VAE raised DSprites FVM to 83.6±3.2 in the ablation study. (Zhu et al., 2021) `ev:measured` p. 6 ^zhu2021commutative-036
- As a potential explanation, the authors propose that the bottleneck-VAE constrains the variations encoded in the latent codes. (Zhu et al., 2021) `ev:asserted` p. 6 ^zhu2021commutative-037
- During training, the KL loss of the Lie Group VAE evolves more elastically than those of the VAE baselines. (Zhu et al., 2021) `ev:measured` p. 6 ^zhu2021commutative-038
- With group representation size 4, the DSprites FVM was 23.6±3.3, against 85.5±2.2 with size 100. (Zhu et al., 2021) `ev:measured` p. 6 ^zhu2021commutative-039
- The authors attribute the weak disentanglement at size 4 to 2 × 2 matrices, which are hard to decompose beyond two sub-transformations. (Zhu et al., 2021) `ev:asserted` p. 7 ^zhu2021commutative-040
- Once the group representation size exceeds 25, the authors report that the model easily finds a decomposition and scores saturate. (Zhu et al., 2021) `ev:measured` p. 7 ^zhu2021commutative-041
- The authors use a group representation size of 100 for all experiments other than the size ablation. (Zhu et al., 2021) `ev:reported` p. 7 ^zhu2021commutative-042
- The one-parameter decomposition constraint peaked at λdecomp 40, where DSprites SAP reached 50.8±5.0 versus 40.7±12.2 without it. (Zhu et al., 2021) `ev:measured` p. 7 ^zhu2021commutative-043
- The Hessian Penalty constraint peaked at λhessian 20, where DSprites SAP reached 54.1±1.2 versus 40.7±12.2 without it. (Zhu et al., 2021) `ev:measured` p. 7 ^zhu2021commutative-044
- At λhessian 20, the Hessian Penalty model reached a DSprites MIG of 29.7±3.1, compared with 25.4±6.1 for the decomposition constraint at λdecomp 40. (Zhu et al., 2021) `ev:measured` p. 7 ^zhu2021commutative-045
- The authors attribute the larger Hessian gain to its stronger requirement of zero mutual basis products rather than zero commutators. (Zhu et al., 2021) `ev:asserted` p. 7 ^zhu2021commutative-046
- In the reconstruction versus FactorVAE plot, the Commutative Lie Group constraints boost disentanglement at a slight cost of reconstruction quality. (Zhu et al., 2021) `ev:measured` p. 7 ^zhu2021commutative-047
- In the same reconstruction versus FactorVAE comparison, the authors observe that β-VAE models sacrifice reconstruction quality severely. (Zhu et al., 2021) `ev:measured` p. 7 ^zhu2021commutative-048
- The state-of-the-art comparison uses the whole dataset for training and evaluation, reporting the best model on the FVM score. (Zhu et al., 2021) `ev:reported` p. 7 ^zhu2021commutative-049
- On DSprites, the proposed model reached an FVM of 86.1±2.0, above Factor-VAE at 82.15±0.88 and Cascade-VAE at 81.74±2.97. (Zhu et al., 2021) `ev:measured` p. 7 ^zhu2021commutative-050
- On 3DShapes, the proposed model reached an FVM of 93.2±4.0, above the 91 reported for β-VAE by Kim and Mnih. (Zhu et al., 2021) `ev:measured` p. 7 ^zhu2021commutative-051
- The authors suggest the model has potential for further improvement if the statistical independence assumption is enforced concurrently. (Zhu et al., 2021) `ev:asserted` p. 7 ^zhu2021commutative-052
- The CelebA dataset contains 202,599 cropped real-world face images, of which the central 128 × 128 area was used. (Zhu et al., 2021) `ev:reported` p. 7 ^zhu2021commutative-053
- On CelebA, the authors report their model extracts cleaner semantic variations than FactorVAE for most of the attributes. (Zhu et al., 2021) `ev:measured` p. 8 ^zhu2021commutative-054
- The background factor learned by FactorVAE on CelebA is entangled with smile, whereas the proposed model encodes background independently. (Zhu et al., 2021) `ev:measured` p. 8 ^zhu2021commutative-055
- On CelebA the model also encodes forehead hair-style and make-up, semantics not shown in the FactorVAE traversals. (Zhu et al., 2021) `ev:measured` p. 8 ^zhu2021commutative-056
- On Mnist, the model is trained on data of a single class at a time, with images padded to 32 × 32. (Zhu et al., 2021) `ev:reported` p. 8 ^zhu2021commutative-057
- Integrating discrete latent-variable techniques into the model for unsupervised classification is left by the authors for future work. (Zhu et al., 2021) `ev:asserted` p. 8 ^zhu2021commutative-058
- On Mnist fours, the model discovered a lifting concept that controls the level of the horizontal line. (Zhu et al., 2021) `ev:measured` p. 8 ^zhu2021commutative-059
- On 3DChairs, with 86,366 images, the model achieved disentanglement quality similar to CascadeVAE in latent traversal comparisons. (Zhu et al., 2021) `ev:measured` p. 8 ^zhu2021commutative-060
- The authors conclude that a group structure, unlike a vector space, can be adaptively optimized to fit diverse data variations. (Zhu et al., 2021) `ev:asserted` p. 9 ^zhu2021commutative-061
- In their conclusion, the authors believe this model exhibits a new direction for learning disentangled representations. (Zhu et al., 2021) `ev:asserted` p. 9 ^zhu2021commutative-062

## 🎯 Contributions

## 📖 Glossary

- **Disentangled representation** — latent code where individual dimensions encode separate factors of variation in data.
- **Equivariance** — transformations of the input are reflected by corresponding transformations of the representation.
- **Lie group** — a group with a continuous, smooth structure, here realized as invertible matrices.
- **Lie algebra** — tangent vector space of a Lie group at its identity element.
- **Matrix exponential map** — maps Lie algebra elements to the corresponding Lie group elements.
- **One-parameter subgroup** — subgroup of form exp(tA), parameterized by a single real coordinate t.
- **Hessian Penalty** — regularizer driving mixed second derivatives of a generator to zero.
- **bottleneck-VAE** — VAE variant sharing a feature layer between encoder and decoder.
- **FVM** — FactorVAE metric, a supervised score of disentanglement on synthetic datasets.
- **MIG** — Mutual Information Gap, a disentanglement metric based on latent-factor mutual information.

## ❓ Open questions

- How can non-commutative variations, such as 3D rotations about orthogonal axes, be disentangled with an adaptive group structure?
- Does combining the group structure with statistical-independence constraints improve disentanglement as the authors suggest?
- Can discrete latent variables be integrated for unsupervised classification of datasets such as Mnist?
- How does the method scale to higher-resolution real-world data, where evaluation here is qualitative only?
- Why does performance drop again at higher λ values for both constraints?

## 📝 Notes on reading

- Version read: arXiv v1 (2106.03375, 7 Jun 2021); the PDF header states it appeared in Proceedings of the 38th ICML, PMLR 139, while the packet lists the venue as arXiv preprint.
- Figure 1 (p. 2) is a conceptual diagram contrasting vector-based and group-based disentanglement; Figure 2 (p. 5) shows the architecture and the exponential mapping layer.
- Figure 3 (p. 6) KL-divergence curves and Figure 4 (p. 7) reconstruction vs FactorVAE scatter were described only from the text; axis values were not claimed.
- Figures 5-8 are qualitative latent traversals (DSprites, 3DShapes, CelebA, Mnist, 3DChairs); no quantitative scores on the real-world datasets.
- Table 5 mixes the authors' runs with values quoted from Kim & Mnih (2018) for β-VAE and Factor-VAE on 3DShapes (91 and 89, no deviation).
- Table 2 size 100 row and Table 3 λdecomp 40 row are identical (85.5±2.2 FVM), suggesting the size ablation used the decomposition constraint at λdecomp 40; the paper does not state this.
- The CelebA traversals use λhessian = 40, not the λhessian 20 setting that peaked on DSprites.
- Proofs and implementation details are in appendices not included in this cached text.

## Suggested new concepts

- Lie group representation learning — adaptive group-structured latents as an alternative to vector-space latents for disentanglement.
- Symmetry-based disentanglement — group-theoretic definition of disentanglement shared by several cited works.
- Hessian Penalty — reusable regularizer for disentanglement, applied here to Lie algebra bases.
- Disentanglement metrics — FVM, SAP, MIG and DCI recur across disentanglement papers and deserve a comparison note.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Desenmarañamiento como acción de grupo de Lie
