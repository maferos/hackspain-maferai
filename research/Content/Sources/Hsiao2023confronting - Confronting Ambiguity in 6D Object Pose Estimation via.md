---
aliases: []
type: "source"
title: "Confronting Ambiguity in 6D Object Pose Estimation via Score-Based Diffusion on SE(3)"
citekey: "Hsiao2023confronting"
doi: "10.48550/arXiv.2305.15873"
arxiv: "2305.15873"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2305.15873"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Tsu-Ching Hsiao", "Hao-Wei Chen", "Hsuan-Kung Yang", "Chun-Yi Lee"]
sha256: ["55d723518b403e458b606308e2c5aef3f579e8db744ff9395939a8ccf86e2a8c"]
pdf: "Content/Papers/Hsiao2023confronting.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Hsiao2023confronting.pdf]]

> [!abstract] One-sentence summary
> The paper trains a score-based diffusion model directly on SE(3) to sample 6D object poses from a single RGB image, handling symmetry and occlusion ambiguity without symmetry annotations or 3D models, and shows it beats R3SO(3) diffusion and regression baselines on SYMSOL, SYMSOL-T and T-LESS rotation metrics.

## Abstract

Addressing pose ambiguity in 6D object pose estimation from single RGB images presents a significant challenge, particularly due to object symmetries or occlusions. In response, we introduce a novel score-based diffusion method applied to the $SE(3)$ group, marking the first application of diffusion models to $SE(3)$ within the image domain, specifically tailored for pose estimation tasks. Extensive evaluations demonstrate the method's efficacy in handling pose ambiguity, mitigating perspective-induced ambiguity, and showcasing the robustness of our surrogate Stein score formulation on $SE(3)$. This formulation not only improves the convergence of denoising process but also enhances computational efficiency. Thus, we pioneer a promising strategy for 6D object pose estimation. (arXiv)

## 🧠 Key ideas (atomic)

- Pose ambiguity turns the one-to-one correspondence between an image and its object pose into a one-to-many scenario, which can degrade correspondence-reliant methods (Hsiao et al., 2023) `ev:asserted` p. 1 ^hsiao2023confronting-001
- The authors argue that [[Symmetry-aware pose loss|symmetry-aware losses]] depend on symmetry annotations, which are particularly challenging to obtain for intricate shapes or occluded objects (Hsiao et al., 2023) `ev:asserted` p. 1 ^hsiao2023confronting-002
- Implicit-PDF and HyperPose-PDF implicitly model non-parametric densities on SO(3) but require exhaustive sampling across the whole SO(3) space during training (Hsiao et al., 2023) `ev:cited` p. 1 ^hsiao2023confronting-003
- The method jointly estimates rotation and translation distributions on SE(3), inspired by their correlation arising from the perspective effect of image projection (Hsiao et al., 2023) `ev:asserted` p. 2 ^hsiao2023confronting-004
- The authors state that, to their knowledge, this is the first work to apply diffusion models to SE(3) within image space (Hsiao et al., 2023) `ev:asserted` p. 2 ^hsiao2023confronting-005
- The new synthetic SYMSOL-T dataset extends SYMSOL with randomly sampled translations to test joint density estimation of object rotations and translations (Hsiao et al., 2023) `ev:reported` p. 2 ^hsiao2023confronting-006
- The R3SO(3) parametrization, prevalent in prior diffusion models for its simplicity, induces a separate diffusion process for rotation and for translation (Hsiao et al., 2023) `ev:cited` p. 2 ^hsiao2023confronting-007
- The authors state that integrating rotations and translations within SE(3) gives a diffusion process that emulates the elaborate dynamics of rigid-body motion (Hsiao et al., 2023) `ev:asserted` p. 2 ^hsiao2023confronting-008
- Non-probabilistic prior methods often need manual annotations of equivalent poses and are limited against ambiguity caused by occlusion and self-occlusion (Hsiao et al., 2023) `ev:cited` p. 3 ^hsiao2023confronting-009
- Probabilistic prior methods primarily model distributions on SO(3), leaving joint modeling of rotation and translation distributions unexplored, according to the authors (Hsiao et al., 2023) `ev:cited` p. 3 ^hsiao2023confronting-010
- IGSO(3), used by earlier [[Diffusion models on Lie groups|SO(3) diffusion models]], lacks a closed form, which the authors say poses challenges for computational efficiency (Hsiao et al., 2023) `ev:cited` p. 4 ^hsiao2023confronting-011
- Urain et al. use a closed-form joint Gaussian on R3 and SO(3) that still treats rotation and translation as separate diffusion entities (Hsiao et al., 2023) `ev:cited` p. 4 ^hsiao2023confronting-012
- The method samples 6D poses from an image-conditioned distribution using a [[Diffusion models on Lie groups|score-based generative model]] whose prior is a Gaussian distribution on SE(3) (Hsiao et al., 2023) `ev:reported` p. 4 ^hsiao2023confronting-013
- The approach uses neither 3D object models nor symmetry annotations, relying exclusively on RGB images and ground-truth poses for training (Hsiao et al., 2023) `ev:reported` p. 4 ^hsiao2023confronting-014
- The perturbation kernel is a Gaussian on the Lie group defined through the logarithm map of the relative transformation between two group elements (Hsiao et al., 2023) `ev:reported` p. 4 ^hsiao2023confronting-015
- Denoising uses a variant of the Geodesic Random Walk tailored to the Lie group context to generate samples from a noise distribution (Hsiao et al., 2023) `ev:reported` p. 4 ^hsiao2023confronting-016
- On SO(3) the closed-form score simplifies to the sampled Gaussian noise scaled by minus one over sigma squared, avoiding automatic differentiation and Jacobians (Hsiao et al., 2023) `ev:computed` p. 5 ^hsiao2023confronting-017
- The score on R3SO(3) also has this simplified closed form, as its Jacobians satisfy the same left-right transpose relation as SO(3) (Hsiao et al., 2023) `ev:computed` p. 5 ^hsiao2023confronting-018
- The authors show that SE(3) does not possess the Jacobian transpose relation that allows the simplified closed-form score on SO(3) (Hsiao et al., 2023) `ev:computed` p. 5 ^hsiao2023confronting-019
- The authors argue this may misalign the score vector and denoising direction through manifold curvature, impeding convergence and requiring additional denoising steps (Hsiao et al., 2023) `ev:asserted` p. 5 ^hsiao2023confronting-020
- On SE(2), increasing the number of sub-steps in one reverse step makes the integral of small transformations approach the inverse of the noise (Hsiao et al., 2023) `ev:computed` p. 5 ^hsiao2023confronting-021
- The proposed surrogate score on SE(3) replaces the true score in training with the sampled noise z scaled by minus one over sigma squared (Hsiao et al., 2023) `ev:reported` p. 5 ^hsiao2023confronting-022
- Separating the conditioning part from the denoising part removes the need to extract image features at every denoising step during inference (Hsiao et al., 2023) `ev:asserted` p. 5 ^hsiao2023confronting-023
- The score model is composed of multi-layer perceptron blocks whose inputs and outputs are vectors in the corresponding Lie algebra space (Hsiao et al., 2023) `ev:reported` p. 5 ^hsiao2023confronting-024
- The authors' empirical observations suggest that scale-bias conditioning does not perform satisfactorily when the network learns distributions on SO(3) (Hsiao et al., 2023) `ev:measured` p. 5 ^hsiao2023confronting-025
- A modified Fourier-based conditioning mechanism is motivated by pose distributions on SO(3) being circular and representable as periodic functions (Hsiao et al., 2023) `ev:asserted` p. 5 ^hsiao2023confronting-026
- The Fourier-based conditioning introduces no additional network parameters, as its weights are provided by the subsequent linear layer (Hsiao et al., 2023) `ev:reported` p. 5 ^hsiao2023confronting-027
- The authors state their approach is the first probabilistic model to report accuracy on the complete T-LESS dataset rather than a subset (Hsiao et al., 2023) `ev:asserted` p. 6 ^hsiao2023confronting-028
- SYMSOL comprises 250k images of five texture-less symmetric objects: tetrahedron, cube, icosahedron, cone and cylinder under random rotations (Hsiao et al., 2023) `ev:reported` p. 6 ^hsiao2023confronting-029
- On SYMSOL-T the score models are benchmarked against a direct pose regression and an iterative refinement regression, both trained with symmetry-aware losses (Hsiao et al., 2023) `ev:reported` p. 6 ^hsiao2023confronting-030
- T-LESS contains thirty texture-less industrial objects whose pose ambiguity comes from symmetries plus occlusion and self-occlusion in cluttered scenes (Hsiao et al., 2023) `ev:reported` p. 6 ^hsiao2023confronting-031
- The T-LESS training set has 50k physically based rendering images plus 37k real images, while testing uses 10k real images (Hsiao et al., 2023) `ev:reported` p. 6 ^hsiao2023confronting-032
- Besides BOP metrics MSPD, MSSD and VSD, the authors add rotation accuracy within 2, 5 and 10 degrees (Hsiao et al., 2023) `ev:reported` p. 6 ^hsiao2023confronting-033
- On SYMSOL the ResNet50 variant reaches an average spread of 0.37 degrees, against 0.70 for the Normalizing Flows baseline (Hsiao et al., 2023) `ev:measured` p. 7 ^hsiao2023confronting-034
- With the smaller ResNet34 backbone the model still averages 0.42 degrees on SYMSOL, below every ResNet50 baseline in Table 2 (Hsiao et al., 2023) `ev:measured` p. 7 ^hsiao2023confronting-035
- The ResNet50 variant performs slightly worse than ResNet34 on the cone shape, with 0.53 against 0.35 degrees of spread (Hsiao et al., 2023) `ev:measured` p. 7 ^hsiao2023confronting-036
- The authors attribute the cone discrepancy to training a single model across all shapes, which may cause mutual influence among pose distributions (Hsiao et al., 2023) `ev:asserted` p. 7 ^hsiao2023confronting-037
- On SYMSOL-T the SE(3) score model keeps rotation spread between 0.41 and 0.64 degrees across all five shapes (Hsiao et al., 2023) `ev:measured` p. 7 ^hsiao2023confronting-038
- The R3SO(3) score model encounters difficulty learning the SYMSOL-T icosahedron, with a rotation spread of 29.35 degrees (Hsiao et al., 2023) `ev:measured` p. 7 ^hsiao2023confronting-039
- For translation on SYMSOL-T, the authors report that the R3SO(3) score model takes the lead over the SE(3) score model (Hsiao et al., 2023) `ev:measured` p. 7 ^hsiao2023confronting-040
- The authors credit the R3SO(3) translation result to its assumption of independence between rotation and translation, which eliminates mutual interference (Hsiao et al., 2023) `ev:asserted` p. 7 ^hsiao2023confronting-041
- On T-LESS the [[Diffusion models on Lie groups|SE(3) diffusion model]] reaches an MSPD of 93.16, against 90.17 for GDRNPP (Hsiao et al., 2023) `ev:measured` p. 7 ^hsiao2023confronting-042
- On T-LESS the SE(3) diffusion model reaches R@2 accuracy of 47.21, against 21.60 for GDRNPP (Hsiao et al., 2023) `ev:measured` p. 7 ^hsiao2023confronting-043
- GDRNPP stays ahead on T-LESS translation at T@2, with 90.31 against 71.72 for the SE(3) diffusion model (Hsiao et al., 2023) `ev:measured` p. 7 ^hsiao2023confronting-044
- The [[Diffusion models on Lie groups|SE(3) diffusion model]] outperforms its R3SO(3) counterpart on all T-LESS metrics, for instance 93.16 against 85.73 MSPD (Hsiao et al., 2023) `ev:measured` p. 7 ^hsiao2023confronting-045
- For T-LESS, a single model with a ResNet34 backbone is trained across all 30 objects on cropped regions of interest (Hsiao et al., 2023) `ev:reported` p. 8 ^hsiao2023confronting-046
- The method assumes ground-truth bounding boxes and segmentation masks of the visible object parts are available on T-LESS (Hsiao et al., 2023) `ev:reported` p. 8 ^hsiao2023confronting-047
- The authors attribute GDRNPP's better translation to its geometry guidance derived from 3D models, which enhances depth estimation (Hsiao et al., 2023) `ev:asserted` p. 8 ^hsiao2023confronting-048
- With 5 denoising steps the SE(3) model runs at 250 FPS on T-LESS while scoring 92.40 MSPD (Hsiao et al., 2023) `ev:measured` p. 8 ^hsiao2023confronting-049
- Inference timing used JAX on an AMD Ryzen Threadripper 2990WX CPU and an RTX 2080 Ti GPU (Hsiao et al., 2023) `ev:reported` p. 8 ^hsiao2023confronting-050
- The authors suggest that these inference speeds indicate practical applicability of their models in real-time scenarios (Hsiao et al., 2023) `ev:asserted` p. 8 ^hsiao2023confronting-051
- On SYMSOL-T variants, the Edge variant with maximal translations shows greater pose uncertainty than the Centered variant for both score models (Hsiao et al., 2023) `ev:measured` p. 12 ^hsiao2023confronting-052
- The authors report the SE(3) score model shows greater robustness than the R3SO(3) model to ambiguity caused by image perspective (Hsiao et al., 2023) `ev:measured` p. 12 ^hsiao2023confronting-053
- With 100 denoising steps, SE(3) models trained with the autograd true score and the surrogate score give comparable SYMSOL-T results (Hsiao et al., 2023) `ev:measured` p. 12 ^hsiao2023confronting-054
- At 5 denoising steps, SE(3)-autograd has a tetrahedron rotation spread of 12.93 degrees, against 1.22 for SE(3)-surrogate (Hsiao et al., 2023) `ev:measured` p. 12 ^hsiao2023confronting-055
- The authors attribute the autograd drop to SE(3) curvature, which can leave the score vector not consistently pointing towards noise-free data (Hsiao et al., 2023) `ev:asserted` p. 12 ^hsiao2023confronting-056
- The MLE-trained SO(3) diffusion model of Jagvaral et al., adapted to this framework, averages 30.45 degrees on SYMSOL and fails (Hsiao et al., 2023) `ev:measured` p. 13 ^hsiao2023confronting-057
- Without Fourier conditioning, the score model with the NSO(3) distribution averages 0.51 degrees, against 1.18 with IGSO(3) (Hsiao et al., 2023) `ev:measured` p. 13 ^hsiao2023confronting-058
- Adding Fourier-based conditioning lowers the average SYMSOL spread to 0.42 degrees, compared with 0.63 for the DDPM model of Leach et al. (Hsiao et al., 2023) `ev:measured` p. 13 ^hsiao2023confronting-059
- On T-LESS, depth translation accuracy z@2 is 73.33 for the SE(3) model against 91.21 for GDRNPP (Hsiao et al., 2023) `ev:measured` p. 13 ^hsiao2023confronting-060
- The authors report that the SE(3) diffusion model predicts x and y translations on T-LESS as accurately as GDRNPP (Hsiao et al., 2023) `ev:measured` p. 14 ^hsiao2023confronting-061
- In one T-LESS failure case the model predicts one continuous symmetry for an object that should have only six discrete symmetries (Hsiao et al., 2023) `ev:measured` p. 14 ^hsiao2023confronting-062
- The authors suggest failures may arise from fitting one model to multiple objects, whose pose distributions may interfere with each other (Hsiao et al., 2023) `ev:asserted` p. 14 ^hsiao2023confronting-063
- The authors note the diffusion approach relies on a sufficient volume of data samples, without which it could mis-model pose distributions (Hsiao et al., 2023) `ev:asserted` p. 14 ^hsiao2023confronting-064
- SYMSOL-T translations along the x, y and z axes are uniformly sampled within the range of [−1, 1] (Hsiao et al., 2023) `ev:reported` p. 16 ^hsiao2023confronting-065
- Each training iteration samples 16 images, each perturbed into 256 random poses, giving 4,096 noisy samples to denoise (Hsiao et al., 2023) `ev:reported` p. 16 ^hsiao2023confronting-066
- The authors show the closed-form SE(3) score involves costly Jacobian calculation and confers no computational benefit over automatic differentiation (Hsiao et al., 2023) `ev:computed` p. 18 ^hsiao2023confronting-067

## 🎯 Contributions

## 📖 Glossary

- **SE(3)** — Lie group of 3D rigid-body transformations combining rotation and translation.
- **R3SO(3)** — Parametrization treating translation in R3 and rotation in SO(3) as separate composite manifold.
- **Stein score** — Gradient of the log probability density with respect to the variable.
- **Surrogate score** — Noise-scaled score replacing the true SE(3) score to speed denoising convergence.
- **IGSO(3)** — Isotropic Gaussian on SO(3), a heat kernel without closed form.
- **Concentrated Gaussian** — Gaussian on a Lie group built by mapping small Lie-algebra noise through Exp.
- **Geodesic Random Walk** — Sampling scheme for manifolds used to run the reverse diffusion process.
- **SYMSOL-T** — SYMSOL symmetric-shape dataset extended with random translations to add perspective ambiguity.
- **MSPD / MSSD / VSD** — BOP challenge pose error metrics: projection, surface and visible-surface discrepancies.

## ❓ Open questions

- Can a single model learn distributions of many shapes or objects without mutual interference, as seen for the cone and T-LESS failures?
- Can depth (z) translation accuracy match geometry-guided methods like GDRNPP without 3D models?
- How does the method perform with detected rather than ground-truth bounding boxes and segmentation masks?
- Why does the R3SO(3) score model fail on the icosahedron, and would more training fix it?
- Does the surrogate score introduce bias in the learned distribution beyond the sampling-step analysis?

## 📝 Notes on reading

- Version read: arXiv 2305.15873v2 (8 Apr 2024), with supplementary material on pp. 12–20; matches the packet identifier.
- Pages 9–11 are acknowledgements and references; pp. 19–20 hold only figures (Fig. 7 SYMSOL-T visualizations, Fig. 8 T-LESS results and failures), which could only be described.
- Fig. 2 (p. 6) shows the framework (image encoder / positional embedding conditioning, MLP denoising blocks) and an SE(2) sub-step denoising illustration; described, not claimed as data.
- Inconsistency: p. 7 says both SE(3) and R3SO(3) score models outperform the regression baselines on SYMSOL-T, but Table 3 gives R3SO(3) an icosahedron rotation spread of 29.35 against 2.46 for plain regression.
- Table 3 also shows iterative regression at 29.33 on the icosahedron, not discussed in the text.
- Table 5 (p. 8) gives per-step inference times for both models (e.g. SE(3) 0.050 s at 100 steps, R3SO(3) 307 FPS at 5 steps); only headline rows were claimed.
- The Fourier-conditioning formula (Eq. 13) and SE(3) Jacobian equations (Eqs. 11, 29–33) are partly garbled in extraction; no numbers were claimed from them.
- Listing 3 comment refers to Eq. (25) while the autodiff score is Eq. (18); minor internal numbering mismatch.
- The learning-rate and noise-schedule exponents (10−4, 10−5) are rendered with a Unicode minus and were not claimed.

## Suggested new concepts

- Diffusion models on Lie groups — several papers apply score-based or DDPM diffusion on SO(3)/SE(3) for pose or robotics.
- Pose ambiguity from symmetry and occlusion — a recurring problem for 6D pose estimation that motivates distributional outputs.
- Surrogate score on SE(3) — a specific training trick trading exact scores for faster reverse-process convergence.
- SYMSOL benchmarks — standard synthetic testbeds for density estimation on SO(3) and SE(3).

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H2.** Difusión en SE(3) para pose 6D ambigua de objetos simétricos, relevante para frascos y tapones de revolución del laboratorio.
