---
aliases: []
type: "source"
title: "Implicit-PDF: Non-Parametric Representation of Probability Distributions on the Rotation Manifold"
citekey: "Murphy2021implicit"
doi: "10.48550/arXiv.2106.05965"
arxiv: "2106.05965"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2106.05965"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Kieran Murphy", "Carlos Esteves", "Varun Jampani", "Srikumar Ramalingam", "Ameesh Makadia"]
sha256: ["591572aee82ee4331b42527bd3d2b4b68dbf4b7efde4be00c670f4bc40661334"]
pdf: "Content/Papers/Murphy2021implicit.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Murphy2021implicit.pdf]]

> [!abstract] One-sentence summary
> Implicit-PDF represents arbitrary pose distributions on SO(3) with an MLP scoring image-rotation pairs, recovering symmetric and near-symmetric ambiguity from single-pose supervision while staying competitive on standard pose benchmarks.

## Abstract

Single image pose estimation is a fundamental problem in many vision and robotics tasks, and existing deep learning approaches suffer by not completely modeling and handling: i) uncertainty about the predictions, and ii) symmetric objects with multiple (sometimes infinite) correct poses. To this end, we introduce a method to estimate arbitrary, non-parametric distributions on SO(3). Our key idea is to represent the distributions implicitly, with a neural network that estimates the probability given the input image and a candidate pose. Grid sampling or gradient ascent can be used to find the most likely pose, but it is also possible to evaluate the probability at any pose, enabling reasoning about symmetries and uncertainty. This is the most general way of representing distributions on manifolds, and to showcase the rich expressive power, we introduce a dataset of challenging symmetric and nearly-symmetric objects. We require no supervision on pose uncertainty -- the model trains only with a single pose per example. Nonetheless, our implicit model is highly expressive to handle complex distributions over 3D poses, while still obtaining accurate pose estimation on standard non-ambiguous environments, achieving state-of-the-art performance on Pascal3D+ and ModelNet10-SO(3) benchmarks. (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that explicitly modeling every pose ambiguity is not scalable, since enumerating all sources of pose uncertainty is unrealistic. (Murphy et al., 2021) `ev:asserted` p. 1 ^murphy2021implicit-001
- The paper introduces Implicit-PDF, a method representing arbitrary non-parametric probability distributions on SO(3) implicitly with a neural network. (Murphy et al., 2021) `ev:asserted` p. 1 ^murphy2021implicit-002
- For Bingham and Matrix Fisher distributions, the normalizing term is a hypergeometric function of a matrix argument, which is itself challenging to compute. (Murphy et al., 2021) `ev:cited` p. 3 ^murphy2021implicit-003
- The authors state that there has been little evidence of normalizing flows successfully learning arbitrary distributions on SO(3) for realistic problems. (Murphy et al., 2021) `ev:asserted` p. 3 ^murphy2021implicit-004
- The network is a multilayer perceptron that takes an image descriptor with a candidate rotation as input and outputs an unnormalized log probability. (Murphy et al., 2021) `ev:reported` p. 3 ^murphy2021implicit-005
- The conditional distribution is normalized by approximating the integral over SO(3) with a discrete sum over an equivolumetric partition of rotations. (Murphy et al., 2021) `ev:reported` p. 3 ^murphy2021implicit-006
- Single pose prediction maximizes the network output by gradient ascent from a grid-based initial guess, projecting values back onto SO(3) after each step. (Murphy et al., 2021) `ev:reported` p. 4 ^murphy2021implicit-007
- The model is trained by minimizing the negative log-likelihood of the single ground truth pose per example, without supervision on the distribution. (Murphy et al., 2021) `ev:reported` p. 4 ^murphy2021implicit-008
- During training the equivolumetric grid is rotated such that one of its points coincides with the ground truth rotation. (Murphy et al., 2021) `ev:reported` p. 4 ^murphy2021implicit-009
- The authors observed that training with randomly sampled rotations instead of an equivolumetric grid works similarly well, provided one sample matches the ground truth. (Murphy et al., 2021) `ev:measured` p. 4 ^murphy2021implicit-010
- The equivolumetric partition is still required during inference for an accurate representation of the probabilities. (Murphy et al., 2021) `ev:asserted` p. 4 ^murphy2021implicit-011
- The image descriptor comes from a pre-trained ResNet, allowing a single model to represent poses of instances from multiple categories. (Murphy et al., 2021) `ev:reported` p. 4 ^murphy2021implicit-012
- Rotations are input as 3 × 3 rotation matrices, which the authors found best to avoid [[Rotation representation continuity|discontinuities of other representations]]. (Murphy et al., 2021) `ev:reported` p. 4 ^murphy2021implicit-013
- Each element of the input rotation is positionally encoded, following the NeRF work of Mildenhall, which the authors found beneficial. (Murphy et al., 2021) `ev:reported` p. 4 ^murphy2021implicit-014
- Equivolumetric grids are generated with the Yershova method, which builds on HEALPix equal-area grids on the 2-sphere. (Murphy et al., 2021) `ev:reported` p. 4 ^murphy2021implicit-015
- The grids are generated recursively from a seed of 72 points, growing by a factor of eight each iteration. (Murphy et al., 2021) `ev:reported` p. 5 ^murphy2021implicit-016
- For evaluation, the grid after 5 subdivisions is used, containing a little more than two million points. (Murphy et al., 2021) `ev:reported` p. 5 ^murphy2021implicit-017
- The authors introduce a visualization that displays full SO(3) distributions using the Hopf fibration, with color indicating the tilt about each axis. (Murphy et al., 2021) `ev:reported` p. 5 ^murphy2021implicit-018
- The paper reports average log likelihood over test annotations, noting it is invariant to whether one or all equivalent ground truths are available. (Murphy et al., 2021) `ev:asserted` p. 5 ^murphy2021implicit-019
- Spread, or mean absolute angular deviation, is the expected geodesic distance from predicted rotations to the nearest of the known ground truths. (Murphy et al., 2021) `ev:reported` p. 5 ^murphy2021implicit-020
- SYMSOL I is a new dataset of images rendered from platonic solids, namely tetrahedron, cube, icosahedron, plus surfaces of revolution. (Murphy et al., 2021) `ev:reported` p. 5 ^murphy2021implicit-021
- SYMSOL I contains 100,000 renderings of each shape, from poses sampled uniformly at random from SO(3). (Murphy et al., 2021) `ev:reported` p. 6 ^murphy2021implicit-022
- Ground truth symmetry sets accompany each SYMSOL image but are used only for evaluation, not for training. (Murphy et al., 2021) `ev:reported` p. 6 ^murphy2021implicit-023
- SYMSOL II breaks symmetries with small markers on a sphere, a tetrahedron with one red face, and a cylinder, with 100,000 images each. (Murphy et al., 2021) `ev:reported` p. 6 ^murphy2021implicit-024
- The authors state that the distribution of a marked sphere with a hidden marker cannot be easily approximated by mixtures of unimodals. (Murphy et al., 2021) `ev:asserted` p. 6 ^murphy2021implicit-025
- Pascal3D+ consists of real images of twelve object categories whose annotations are generally disambiguated and restricted to subsets of SO(3). (Murphy et al., 2021) `ev:reported` p. 7 ^murphy2021implicit-026
- T-LESS evaluation uses Kinect RGB single-object images of texture-less industrial parts, tight-cropped and color-normalized as in Gilitschenski et al. (Murphy et al., 2021) `ev:reported` p. 7 ^murphy2021implicit-027
- Baselines include Bingham mixture methods, a unimodal matrix Fisher method, an infinite mixture over Euler angles, and direct spherical regression to Euler angles. (Murphy et al., 2021) `ev:reported` p. 7 ^murphy2021implicit-028
- A minimally informative uniform distribution over SO(3) has an average log likelihood of -2.29, which the paper uses as a reference. (Murphy et al., 2021) `ev:computed` p. 7 ^murphy2021implicit-029
- On SYMSOL I, IPDF reached an average log likelihood of 4.10, versus −0.43 for the Gilitschenski et al. baseline. (Murphy et al., 2021) `ev:measured` p. 7 ^murphy2021implicit-030
- On the icosahedron, IPDF obtained a log likelihood of 1.28, against baseline values from −2.45 to −2.29. (Murphy et al., 2021) `ev:measured` p. 7 ^murphy2021implicit-031
- On SYMSOL II, IPDF reached an average log likelihood of 7.57, compared with 3.70 for the Gilitschenski et al. baseline. (Murphy et al., 2021) `ev:measured` p. 7 ^murphy2021implicit-032
- As symmetry order increases from 12 to 24 to 60, the baselines tend to perform at the level of a uniform distribution. (Murphy et al., 2021) `ev:measured` p. 7 ^murphy2021implicit-033
- A single IPDF model was trained on all five SYMSOL I shapes, whereas baselines used a separate model per shape. (Murphy et al., 2021) `ev:reported` p. 7 ^murphy2021implicit-034
- The authors suggest that the winner-take-all strategy of Deng et al. may have hindered representing the continuous symmetries of cone and cylinder. (Murphy et al., 2021) `ev:asserted` p. 7 ^murphy2021implicit-035
- On ModelNet10-SO(3), IPDF achieved an average accuracy at 15 degrees of 0.719, above the 0.693 of Mohlin et al. (Murphy et al., 2021) `ev:measured` p. 7 ^murphy2021implicit-036
- IPDF's accuracy at 30 degrees on ModelNet10-SO(3) was 0.735, below the 0.757 of Mohlin et al. (Murphy et al., 2021) `ev:measured` p. 7 ^murphy2021implicit-037
- IPDF's average median error on ModelNet10-SO(3) was 21.5 degrees, higher than the 17.1 degrees of Mohlin et al. (Murphy et al., 2021) `ev:measured` p. 7 ^murphy2021implicit-038
- Under top-2 evaluation, IPDF's average median error on ModelNet10-SO(3) fell from 21.5 to 4.9 degrees. (Murphy et al., 2021) `ev:measured` p. 7 ^murphy2021implicit-039
- For the marked cylinder, when the red marking is visible, the network outputs a sharp peak at the correct pose. (Murphy et al., 2021) `ev:measured` p. 8 ^murphy2021implicit-040
- With the red face of the marked tetrahedron visible, the predicted distribution shows three modes for the three indistinguishable remaining faces. (Murphy et al., 2021) `ev:measured` p. 8 ^murphy2021implicit-041
- For the marked sphere with markings hidden, IPDF assigns zero probability to the half of SO(3) where the marking faces the camera. (Murphy et al., 2021) `ev:measured` p. 8 ^murphy2021implicit-042
- Unimodal methods trained with one randomly chosen ground truth among symmetric rotations tend to predict a rotation equidistant from all equivalent possibilities. (Murphy et al., 2021) `ev:measured` p. 8 ^murphy2021implicit-043
- For bathtubs with two symmetry modes separated by 180 degrees, unimodal outputs tend to lie 90 degrees from each mode. (Murphy et al., 2021) `ev:measured` p. 8 ^murphy2021implicit-044
- On Pascal3D+, IPDF achieved an average accuracy at 30 degrees of 0.837, below the 0.859 of Mahendran et al. (Murphy et al., 2021) `ev:measured` p. 8 ^murphy2021implicit-045
- IPDF's average Pascal3D+ median error was 10.3 degrees, compared with 10.1 degrees for Mahendran et al. (Murphy et al., 2021) `ev:measured` p. 8 ^murphy2021implicit-046
- The Pascal3D+ results shown for Liao et al. differ from published numbers, which the authors say were incorrectly scaled by a factor of √2. (Murphy et al., 2021) `ev:reported` p. 8 ^murphy2021implicit-047
- When bathtub symmetry annotations are incomplete, IPDF's median error ends up closer to 180 degrees, increasing the average over all categories. (Murphy et al., 2021) `ev:measured` p. 9 ^murphy2021implicit-048
- The authors state that mixture-based methods could in theory produce pose candidates, but current implementations suffer mode collapse with a fixed number of modes. (Murphy et al., 2021) `ev:asserted` p. 9 ^murphy2021implicit-049
- The authors state that on Pascal3D+ IPDF performs as well as or better than baselines, indicating unambiguous pose estimation is not sacrificed. (Murphy et al., 2021) `ev:asserted` p. 9 ^murphy2021implicit-050
- On T-LESS, IPDF obtained an average log likelihood of 9.8, above the 8.8 of Prokudin et al. (Murphy et al., 2021) `ev:measured` p. 9 ^murphy2021implicit-051
- On T-LESS, IPDF's spread was 4.1 degrees, versus 3.4 for Gilitschenski et al., whose evaluation the authors say disregards dispersion. (Murphy et al., 2021) `ev:measured` p. 9 ^murphy2021implicit-052
- All methods achieve median angular errors of less than 4 degrees on the T-LESS split used by Gilitschenski et al. (Murphy et al., 2021) `ev:measured` p. 9 ^murphy2021implicit-053
- With minor modifications, IPDF extends to 6DOF pose by appending translation coordinates to the rotation query with 10× more training samples. (Murphy et al., 2021) `ev:reported` p. 13 ^murphy2021implicit-054
- On SYMSOL I, IPDF's spread for the cone was 1.4 degrees, versus 10.1 degrees for Deng et al. (Murphy et al., 2021) `ev:measured` p. 14 ^murphy2021implicit-055
- With the coarser grid of 37 k samples, IPDF ran at 18.3 frames per second, versus 18.2 for the Liao et al. baseline. (Murphy et al., 2021) `ev:measured` p. 15 ^murphy2021implicit-056
- In ablations, SYMSOL I performance levels off after 50,000 images per shape but is greatly diminished with only 10,000 examples. (Murphy et al., 2021) `ev:measured` p. 15 ^murphy2021implicit-057
- The authors interpret the poor results with 10,000 images as overfitting, with the network assigning small probability to unseen ground truths. (Murphy et al., 2021) `ev:asserted` p. 17 ^murphy2021implicit-058
- Positional encoding benefits the three shapes with discrete symmetries but is neutral or slightly negative for the cone and cylinder. (Murphy et al., 2021) `ev:measured` p. 17 ^murphy2021implicit-059
- Rotation matrices were the optimal query format for all shapes, with axis-angle and quaternion formats comparable to each other and a fair amount worse. (Murphy et al., 2021) `ev:measured` p. 17 ^murphy2021implicit-060
- Querying with Euler angles averaged near the uniform log likelihood of −2.29, with most but not all runs failing to train. (Murphy et al., 2021) `ev:measured` p. 17 ^murphy2021implicit-061
- Gradient ascent yields optimal Pascal3D+ performance from more than 10,000 queries, whereas argmax requires more than 500,000 queries for similar results. (Murphy et al., 2021) `ev:measured` p. 17 ^murphy2021implicit-062
- The authors note that top-k evaluation cannot disentangle whether errors stem from missing symmetry annotations or from the model. (Murphy et al., 2021) `ev:asserted` p. 19 ^murphy2021implicit-063
- Symmetric ModelNet10-SO(3) categories improve dramatically with larger k, which the authors say suggests lower top-1 performance reflects missing symmetry annotations. (Murphy et al., 2021) `ev:asserted` p. 19 ^murphy2021implicit-064
- Training uses Adam with a linear warm-up to a base learning rate of 10−4 over 1000 steps, then cosine decay. (Murphy et al., 2021) `ev:reported` p. 19 ^murphy2021implicit-065
- For SYMSOL, the MLP used four fully connected layers of 256 units with ReLU activation, plus three positional encoding terms. (Murphy et al., 2021) `ev:reported` p. 20 ^murphy2021implicit-066
- The training loss normalization used 4096 points on SO(3), a coverage the authors found did not need to be particularly dense. (Murphy et al., 2021) `ev:reported` p. 20 ^murphy2021implicit-067
- For Pascal3D+, mini-batches of 64 images mixed 25% real images with 75% synthetic images from Render for CNN. (Murphy et al., 2021) `ev:reported` p. 21 ^murphy2021implicit-068
- The released code of Mohlin et al. sources its Pascal3D+ test set from ImageNet data, unlike the split used by Liao et al. (Murphy et al., 2021) `ev:reported` p. 22 ^murphy2021implicit-069

## 🎯 Contributions


## 📖 Glossary

- **SO(3)** — The group of 3D rotations, the manifold on which orientation distributions are defined.
- **Implicit representation** — A neural network that outputs a function value for any queried input point.
- **Equivolumetric grid** — A partition of SO(3) into cells of equal volume, used to normalize densities.
- **HEALPix** — Hierarchical method for generating equal-area grids on the 2-sphere.
- **Hopf fibration** — Decomposition of SO(3) into great circles over points of the 2-sphere.
- **Bingham distribution** — Parametric antipodally symmetric distribution on unit quaternions, used for rotation uncertainty.
- **Matrix Fisher distribution** — Parametric unimodal distribution over rotation matrices.
- **Spread (MAAD)** — Expected angular distance from predicted rotations to the nearest ground truth.
- **Top-k evaluation** — Scoring the best of k predicted pose candidates against the annotated ground truth.
- **SYMSOL** — Dataset of rendered symmetric (I) and marked nearly-symmetric (II) solids introduced here.
- **Positional encoding** — Mapping inputs to sines and cosines of several frequencies before the MLP.

## ❓ Open questions

- How well does the implicit approach scale to full 6DOF pose on real, cluttered images beyond the modified SYMSOL demonstration?
- Can errors from missing symmetry annotations be separated from model errors without expensive annotation?
- How should the grid resolution be chosen when a normalized distribution feeds a downstream task under a real-time budget?
- Why do more positional encoding terms eventually degrade performance, and does the optimal number depend on symmetry order?
- How much training data per shape is needed for real objects, given the overfitting seen with 10,000 images per shape?

## 📝 Notes on reading

- Version read: arXiv v2 (1 Jul 2022) with the ICML 2021 (PMLR 139) header and a supplement (pages 13–22); the packet identifier is the arXiv DOI.
- The abstract claims state-of-the-art performance on Pascal3D+ and ModelNet10-SO(3), but Table 3 shows Mahendran et al. with a higher average Acc@30 (0.859 vs 0.837) and lower average median error (10.1 vs 10.3) on Pascal3D+, and Table 2 shows Mohlin et al. with lower median error (17.1 vs 21.5) and higher Acc@30 (0.757 vs 0.735) on ModelNet10-SO(3); IPDF leads on Acc@15 and under top-k.
- The √2 in the Table 3 caption and Section S8.2 is split across lines in the extraction.
- The formulas in Table S3 (mixture-of-normals definitions) and Eqs. 1–9 are garbled in the extraction; no claims rest on them.
- Figures 1, 3, 4, 5, S1–S5 were only described in captions; Figure S4 ablation values and Figure S5 curves were not claimed numerically.
- Table S2 inference speed column is labelled 'frames/s ↓', which looks like a typo for ↑.
- Table S4 per-category ModelNet10-SO(3) values are claimed only for the bathtub row.

## Suggested new concepts

- Implicit neural density on SO(3) — a general alternative to parametric rotation distributions, reusable for pose uncertainty in robot perception.
- Equivolumetric SO(3) grids (HEALPix/Hopf) — needed for normalizing and sampling any rotation distribution.
- Symmetry-aware pose evaluation metrics — log likelihood, spread and top-k recall address missing symmetry annotations across benchmarks.
- SYMSOL dataset — a benchmark for multimodal pose distributions with known symmetry sets.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Densidades multimodales en $SO(3)$ para objetos simétricos
