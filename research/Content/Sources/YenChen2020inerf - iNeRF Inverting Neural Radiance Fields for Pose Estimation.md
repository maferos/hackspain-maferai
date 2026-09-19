---
aliases: []
type: "source"
title: "iNeRF: Inverting Neural Radiance Fields for Pose Estimation"
citekey: "YenChen2020inerf"
doi: "10.48550/arXiv.2012.05877"
arxiv: "2012.05877"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2012.05877"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Lin Yen-Chen", "Pete Florence", "Jonathan T. Barron", "Alberto Rodriguez", "Phillip Isola", "Tsung-Yi Lin"]
sha256: ["2d87183839b327ceae2f7d46ef724c4c9239f6d82ee2252864e28d4b3ce63614"]
pdf: "Content/Papers/YenChen2020inerf.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[YenChen2020inerf.pdf]]

> [!abstract] One-sentence summary
> iNeRF estimates 6DoF camera or object pose from RGB images alone by gradient descent through a fixed NeRF, removing the need for mesh models and enabling NeRF self-supervision and category-level pose estimation.

## Abstract

We present iNeRF, a framework that performs mesh-free pose estimation by "inverting" a Neural RadianceField (NeRF). NeRFs have been shown to be remarkably effective for the task of view synthesis - synthesizing photorealistic novel views of real-world scenes or objects. In this work, we investigate whether we can apply analysis-by-synthesis via NeRF for mesh-free, RGB-only 6DoF pose estimation - given an image, find the translation and rotation of a camera relative to a 3D object or scene. Our method assumes that no object mesh models are available during either training or test time. Starting from an initial pose estimate, we use gradient descent to minimize the residual between pixels rendered from a NeRF and pixels in an observed image. In our experiments, we first study 1) how to sample rays during pose refinement for iNeRF to collect informative gradients and 2) how different batch sizes of rays affect iNeRF on a synthetic dataset. We then show that for complex real-world scenes from the LLFF dataset, iNeRF can improve NeRF by estimating the camera poses of novel images and using these images as additional training data for NeRF. Finally, we show iNeRF can perform category-level object pose estimation, including object instances not seen during training, with RGB images by inverting a NeRF model inferred from a single view. (arXiv)

## 🧠 Key ideas (atomic)

- iNeRF performs mesh-free 6DoF pose estimation by inverting a Neural Radiance Field, using only RGB images without object mesh models. (Yen-Chen et al., 2020) `ev:reported` p. 1 ^yenchen2020inerf-001
- Techniques built around differentiable rendering engines typically require a high-quality watertight 3D model, such as a mesh, of the object. (Yen-Chen et al., 2020) `ev:cited` p. 1 ^yenchen2020inerf-002
- iNeRF takes three inputs: an observed image, an initial estimate of the pose, and a NeRF model representing the scene or object. (Yen-Chen et al., 2020) `ev:reported` p. 1 ^yenchen2020inerf-003
- Residuals between NeRF-rendered pixels and observed pixels are backpropagated through the NeRF model to produce gradients for the estimated pose. (Yen-Chen et al., 2020) `ev:reported` p. 1 ^yenchen2020inerf-004
- The authors state that interest point-based ray sampling allows accurate pose estimation using two orders of magnitude fewer pixels than full-image sampling. (Yen-Chen et al., 2020) `ev:asserted` p. 2 ^yenchen2020inerf-005
- Adding iNeRF-annotated images without pose labels to NeRF training can reduce the number of required labeled images by 25% without losing reconstruction quality. (Yen-Chen et al., 2020) `ev:measured` p. 2 ^yenchen2020inerf-006
- The authors know of only one prior work providing [[Category-level object pose estimation|RGB-only category-level pose estimation]], the analysis-by-synthesis method of Chen et al. (Yen-Chen et al., 2020) `ev:asserted` p. 2 ^yenchen2020inerf-007
- Keypoint, CNN-based and differentiable-mesh-renderer pose estimation methods require objects' 3D models during both training and testing, which significantly limits their applicability. (Yen-Chen et al., 2020) `ev:cited` p. 2 ^yenchen2020inerf-008
- Chen et al. use single-image reconstruction with a 3D voxel-based feature volume, then estimate pose through iterative image alignment. (Yen-Chen et al., 2020) `ev:cited` p. 2 ^yenchen2020inerf-009
- The authors hypothesize that continuous implicit NeRF representations will enable higher-fidelity pose estimation than the voxel-based feature volume of Chen et al. (Yen-Chen et al., 2020) `ev:asserted` p. 2 ^yenchen2020inerf-010
- For category-level estimation, iNeRF lets pixelNeRF predict a NeRF model with a single forward pass instead of optimizing shape by gradient descent. (Yen-Chen et al., 2020) `ev:reported` p. 2 ^yenchen2020inerf-011
- The authors argue iNeRF can also perform scene-level visual localization because NeRF and iNeRF only require posed RGB images for training. (Yen-Chen et al., 2020) `ev:asserted` p. 3 ^yenchen2020inerf-012
- NeRF represents a scene as a volumetric density plus a view-dependent color, parameterized by an MLP taking 3D position and viewing direction. (Yen-Chen et al., 2020) `ev:cited` p. 3 ^yenchen2020inerf-013
- iNeRF recovers the camera pose by updating the pose, not the fixed MLP weights, to minimize the photometric loss used to train NeRF. (Yen-Chen et al., 2020) `ev:reported` p. 3 ^yenchen2020inerf-014
- iNeRF assumes the NeRF of the scene or object has already been recovered with known camera intrinsics, while the camera pose is undetermined. (Yen-Chen et al., 2020) `ev:reported` p. 3 ^yenchen2020inerf-015
- The authors note that the iNeRF loss function is non-convex over the 6DoF space of SE(3), which poses an optimization challenge. (Yen-Chen et al., 2020) `ev:asserted` p. 3 ^yenchen2020inerf-016
- The authors state iNeRF can perform 6D pose estimation with either an optimized per-scene NeRF or a NeRF predicted from few images. (Yen-Chen et al., 2020) `ev:asserted` p. 3 ^yenchen2020inerf-017
- To keep estimates on the SE(3) manifold, iNeRF parameterizes the estimated pose with exponential coordinates relative to an initial pose estimate. (Yen-Chen et al., 2020) `ev:reported` p. 4 ^yenchen2020inerf-018
- iNeRF updates the estimated relative transformation with the Adam optimizer using an exponentially decaying learning rate. (Yen-Chen et al., 2020) `ev:reported` p. 4 ^yenchen2020inerf-019
- The relative transformation is initialized near zero, each element drawn from a zero-mean normal distribution with standard deviation 10−6. (Yen-Chen et al., 2020) `ev:reported` p. 4 ^yenchen2020inerf-020
- The authors state that composing the update before the initial pose centers rotation at the initial estimate, alleviating rotation-translation coupling during optimization. (Yen-Chen et al., 2020) `ev:asserted` p. 4 ^yenchen2020inerf-021
- Computing and backpropagating the loss over all pixels of a high-resolution image requires significantly more memory than any commercial GPU provides. (Yen-Chen et al., 2020) `ev:asserted` p. 4 ^yenchen2020inerf-022
- The authors find they can recover accurate poses while sampling only 2048 rays per gradient step. (Yen-Chen et al., 2020) `ev:measured` p. 4 ^yenchen2020inerf-023
- Sampling 2048 rays per gradient step corresponds to a single forward/backward pass providing 150× faster gradient steps on a 640 × 480 image. (Yen-Chen et al., 2020) `ev:measured` p. 4 ^yenchen2020inerf-024
- Random ray sampling performed ineffectively at small batch sizes, as most randomly sampled pixels lie on flat, textureless regions with little pose information. (Yen-Chen et al., 2020) `ev:measured` p. 4 ^yenchen2020inerf-025
- Interest point sampling draws rays from interest points detected in the observed image, falling back to random sampling when too few are detected. (Yen-Chen et al., 2020) `ev:reported` p. 4 ^yenchen2020inerf-026
- The authors state interest point sampling makes optimization converge faster since less stochasticity is introduced into the ray batch. (Yen-Chen et al., 2020) `ev:asserted` p. 4 ^yenchen2020inerf-027
- The authors found interest point sampling prone to local minima, since it only considers interest points in the observed image. (Yen-Chen et al., 2020) `ev:measured` p. 4 ^yenchen2020inerf-028
- Interest region sampling draws rays from dilated masks centered on detected interest points, using a 5 × 5 morphological dilation. (Yen-Chen et al., 2020) `ev:reported` p. 4 ^yenchen2020inerf-029
- The authors find that interest region sampling speeds up the optimization when the batch size of rays is small. (Yen-Chen et al., 2020) `ev:measured` p. 5 ^yenchen2020inerf-030
- In the self-supervised scheme, iNeRF estimates poses of unposed images, which are then added to NeRF's training set for semi-supervised training. (Yen-Chen et al., 2020) `ev:reported` p. 5 ^yenchen2020inerf-031
- iNeRF was tested on 8 scenes from NeRF's synthetic dataset, with 5 test images per scene and 5 pose initializations each. (Yen-Chen et al., 2020) `ev:reported` p. 5 ^yenchen2020inerf-032
- Synthetic initial poses rotated the camera within [−40, 40] degrees about a random axis, then translated it within [−0.2, 0.2] meters per axis. (Yen-Chen et al., 2020) `ev:reported` p. 5 ^yenchen2020inerf-033
- Accuracy is reported as the percentage of predicted poses with error below 5 degrees or 5cm, a metric widely used in pose estimation. (Yen-Chen et al., 2020) `ev:reported` p. 5 ^yenchen2020inerf-034
- On the synthetic dataset, larger ray batch sizes gave better pose estimation accuracy under the same sampling strategy. (Yen-Chen et al., 2020) `ev:measured` p. 5 ^yenchen2020inerf-035
- On the synthetic dataset, larger ray batch sizes also gave faster convergence under the same sampling strategy. (Yen-Chen et al., 2020) `ev:measured` p. 5 ^yenchen2020inerf-036
- With a fixed ray batch size, interest region sampling provided better accuracy and efficiency on the synthetic dataset. (Yen-Chen et al., 2020) `ev:measured` p. 5 ^yenchen2020inerf-037
- Applying interest region sampling improves accuracy by 15% across various batch sizes on the synthetic dataset. (Yen-Chen et al., 2020) `ev:measured` p. 7 ^yenchen2020inerf-038
- Qualitative results show random sampling is inefficient because many sampled points lie on the common background, providing no gradient for matching. (Yen-Chen et al., 2020) `ev:measured` p. 5 ^yenchen2020inerf-039
- iNeRF was evaluated on 4 complex LLFF scenes, Fern, Fortress, Horns, and Room, captured with a forward-facing handheld cellphone. (Yen-Chen et al., 2020) `ev:reported` p. 5 ^yenchen2020inerf-040
- For LLFF, pose initializations followed the synthetic procedure but used random translation offsets within [−0.1, 0.1] meters along each axis. (Yen-Chen et al., 2020) `ev:reported` p. 5 ^yenchen2020inerf-041
- The batch size of rays significantly affects iNeRF's visual localization performance on the real-world LLFF scenes. (Yen-Chen et al., 2020) `ev:measured` p. 5 ^yenchen2020inerf-042
- With 1024 rays, the share of rotation errors below 5 degrees drops from 71% on synthetic data to 55% on LLFF. (Yen-Chen et al., 2020) `ev:measured` p. 5 ^yenchen2020inerf-043
- With 1024 rays, the share of translation errors below 5cm drops from 73% on synthetic data to 39% on LLFF. (Yen-Chen et al., 2020) `ev:measured` p. 5 ^yenchen2020inerf-044
- The authors suggest the weaker LLFF results may stem from NeRF's normalized device coordinate space for LLFF, or simply from differing scene content. (Yen-Chen et al., 2020) `ev:asserted` p. 5 ^yenchen2020inerf-045
- For self-supervision, NeRFs trained on 25% and 50% of Fern training data estimated the remaining training images' camera poses via iNeRF. (Yen-Chen et al., 2020) `ev:reported` p. 5 ^yenchen2020inerf-046
- All Fern NeRF models in the self-supervision study were retrained from scratch for 200k iterations using the same learning rate. (Yen-Chen et al., 2020) `ev:reported` p. 5 ^yenchen2020inerf-047
- On Fern with 50% labeled poses, adding iNeRF-estimated poses raised NeRF PSNR from 24.18 to 24.64. (Yen-Chen et al., 2020) `ev:measured` p. 5 ^yenchen2020inerf-048
- On Fern with 25% labeled poses, adding iNeRF-estimated poses raised NeRF PSNR from 21.85 to 23.89. (Yen-Chen et al., 2020) `ev:measured` p. 5 ^yenchen2020inerf-049
- A NeRF trained with 100% of the Fern ground-truth pose labels reached a PSNR of 24.94 in the benchmark. (Yen-Chen et al., 2020) `ev:measured` p. 5 ^yenchen2020inerf-050
- The authors state the PSNR gains are consistent with NeRF's well-understood sensitivity to the accuracy of its input camera poses. (Yen-Chen et al., 2020) `ev:asserted` p. 5 ^yenchen2020inerf-051
- The appendix reports that using only 10% of labeled Fern camera poses worsens the PSNR from 18.5 to 15.64. (Yen-Chen et al., 2020) `ev:measured` p. 8 ^yenchen2020inerf-052
- The authors conclude that having enough labels for a good initialization is important when self-supervising NeRF with iNeRF. (Yen-Chen et al., 2020) `ev:asserted` p. 8 ^yenchen2020inerf-053
- Category-level experiments used the ShapeNet-SRN car dataset of 3514 cars split into training, validation, and test sets. (Yen-Chen et al., 2020) `ev:reported` p. 5 ^yenchen2020inerf-054
- ShapeNet-SRN test images have 128 × 128 resolution and are rendered from 251 views on an archimedean spiral. (Yen-Chen et al., 2020) `ev:reported` p. 5 ^yenchen2020inerf-055
- The ShapeNet task estimates the relative pose between two images of an unseen instance, with translation ambiguous up to a scale. (Yen-Chen et al., 2020) `ev:reported` p. 5 ^yenchen2020inerf-056
- Image I1 was selected from views whose rotation and translation lie within 30 degrees of the randomly selected image I0. (Yen-Chen et al., 2020) `ev:reported` p. 6 ^yenchen2020inerf-057
- At test time, iNeRF aligns a NeRF predicted by a pre-trained pixelNeRF from image I0 against image I1 to estimate relative pose. (Yen-Chen et al., 2020) `ev:reported` p. 6 ^yenchen2020inerf-058
- On ShapeNet cars, iNeRF reached a mean rotation error of 4.39 degrees versus 9.27 for the feature-based SuperGlue baseline. (Yen-Chen et al., 2020) `ev:measured` p. 6 ^yenchen2020inerf-059
- On ShapeNet cars, iNeRF reached a mean translation error of 4.81 degrees versus 18.2 for the SuperGlue baseline. (Yen-Chen et al., 2020) `ev:measured` p. 6 ^yenchen2020inerf-060
- On ShapeNet cars, iNeRF's median rotation error was 2.01 degrees against 6.22 degrees for SuperGlue. (Yen-Chen et al., 2020) `ev:measured` p. 6 ^yenchen2020inerf-061
- On ShapeNet cars, iNeRF produced 8.7% outliers versus 33.3% for SuperGlue, outliers being rotation or translation errors above 20 degrees. (Yen-Chen et al., 2020) `ev:measured` p. 6 ^yenchen2020inerf-062
- The authors did not compare against Chen et al., since that method would not use the reference image and code was unavailable. (Yen-Chen et al., 2020) `ev:asserted` p. 6 ^yenchen2020inerf-063
- The Sim2Real evaluation used 10 unseen real toy cars with unknown mesh models as test data for category-level pose estimation. (Yen-Chen et al., 2020) `ev:reported` p. 6 ^yenchen2020inerf-064
- A pixelNeRF trained on the synthetic ShapeNet dataset inferred NeRF models from single real images without extra fine-tuning. (Yen-Chen et al., 2020) `ev:reported` p. 6 ^yenchen2020inerf-065
- In iterative real-world tracking, iNeRF needed less than 10 optimization iterations to converge, enabling tracking at approximately 1Hz. (Yen-Chen et al., 2020) `ev:measured` p. 7 ^yenchen2020inerf-066
- The authors state that both lighting and occlusion can severely affect iNeRF's performance and are not modeled by the current formulation. (Yen-Chen et al., 2020) `ev:asserted` p. 7 ^yenchen2020inerf-067
- iNeRF currently takes around 20 seconds to run 100 optimization steps, which prevents it from being practical for real-time use. (Yen-Chen et al., 2020) `ev:measured` p. 7 ^yenchen2020inerf-068
- The authors propose modeling appearance variation with transient latent codes as in NeRF-W, jointly optimized alongside camera pose. (Yen-Chen et al., 2020) `ev:asserted` p. 7 ^yenchen2020inerf-069

## 🎯 Contributions

## 📖 Glossary

- **NeRF** — Neural radiance field: an MLP mapping 3D position and view direction to density and color.
- **Analysis-by-synthesis** — Estimating hidden parameters by rendering hypotheses and comparing them with observations.
- **6DoF pose** — Three-dimensional rotation plus three-dimensional translation of a camera or object.
- **SE(3)** — The group of rigid-body transformations combining 3D rotation and translation.
- **Exponential coordinates** — Screw-axis parameterization of a rigid transform that keeps updates on SE(3).
- **Interest region sampling** — Sampling rays from dilated masks around detected image interest points.
- **pixelNeRF** — A network predicting a NeRF model conditioned on one or few input images.
- **LLFF** — Local Light Field Fusion dataset of forward-facing real-world scenes.
- **PSNR** — Peak signal-to-noise ratio, a reconstruction-quality metric in decibels.
- **Category-level pose estimation** — Estimating pose for unseen instances of a known object category.

## ❓ Open questions

- Can jointly optimizing appearance latent codes with pose make iNeRF robust to lighting changes and occlusion?
- How much would faster NeRF rendering methods reduce iNeRF's 20-second-per-100-step runtime toward real-time use?
- Is the weaker LLFF performance caused by the NDC parameterization or by scene content?
- How large an initial pose error can iNeRF recover from before the non-convex loss traps it in local minima?
- How does iNeRF compare with mesh-based pose estimators on standard object benchmarks such as LineMOD?

## 📝 Notes on reading

- Version read: arXiv 2012.05877v3 (10 Aug 2021), later than the 2020 v1 that the citekey year reflects.
- Figure 6 (synthetic and LLFF accuracy curves by sampling strategy and batch size) and Figure 9 (LLFF error histogram) are plots; only the numbers stated in their captions or the text were claimed.
- The appendix gives a loss for LineMOD (RGB to YUV, Y channel dropped), but no LineMOD experiment appears in the paper; the YUV matrix is partly garbled in extraction (0/615) and was not claimed.
- Table II reports translation errors in degrees because translation is treated as a unit direction on S2; median translation errors are 1.77 (iNeRF) and 5.4 (SuperGlue).
- Appendix IX refers to Section 5.2 (the LLFF section V-B) and states rotation perturbations of [−40, 40] degrees for LLFF, consistent with V-B reusing the synthetic procedure; it also says more than 70% of LLFF data reaches under 5 degrees and 5 cm error at batch size 2048.
- The 10% label experiment in Appendix X is ambiguous about which two conditions give PSNR 18.5 and 15.64; the claim keeps the paper's wording.
- Section V states iNeRF achieves competitive results against feature-based methods; the only feature-based baseline shown is SuperGlue on ShapeNet cars.
- The 25% label-reduction statement comes from the introduction; Table I shows 50% labels plus iNeRF at 24.64 versus 24.94 with full labels.
- Setup details also stated but not claimed to stay under the claim cap: Adam with β1 0.9, β2 0.999, initial learning rate 0.01 decaying by 0.8 every 100 steps; interest region dilation falls back to random sampling for large iteration counts; PointRend masks the background before pixelNeRF.

## Suggested new concepts

- Neural Radiance Fields — the representation iNeRF inverts; central to many pose and reconstruction papers.
- Analysis-by-synthesis pose estimation — a family of render-and-compare methods iNeRF belongs to.
- Mesh-free pose estimation — pose estimation without CAD models, a recurring requirement for novel or transparent objects.
- Ray sampling strategies for NeRF optimization — random, interest point and interest region sampling trade speed against local minima.
- Self-supervised NeRF pose labeling — using estimated poses to add unposed images to NeRF training.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Pose por inversión de un campo de radiancia en $SE(3)$
