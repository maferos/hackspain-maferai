---
aliases: []
type: "source"
title: "Gaussian Splatting SLAM"
citekey: "Matsuki2023gaussian"
doi: "10.48550/arXiv.2312.06741"
arxiv: "2312.06741"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2312.06741"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Hidenobu Matsuki", "Riku Murai", "Paul H. J. Kelly", "Andrew J. Davison"]
sha256: ["d7a1ef9b7f313156c61f23ea76423eecd3f8f7d2a795a74774dfbaf23f7a803e"]
pdf: "Content/Papers/Matsuki2023gaussian.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Matsuki2023gaussian.pdf]]

> [!abstract] One-sentence summary
> The paper builds a live monocular and RGB-D SLAM system on 3D Gaussian Splatting alone, using analytic SE(3) pose Jacobians, isotropic regularisation and covisibility-based keyframing to reach competitive tracking and fast, high-fidelity rendering.

## Abstract

We present the first application of 3D Gaussian Splatting in monocular SLAM, the most fundamental but the hardest setup for Visual SLAM. Our method, which runs live at 3fps, utilises Gaussians as the only 3D representation, unifying the required representation for accurate, efficient tracking, mapping, and high-quality rendering. Designed for challenging monocular settings, our approach is seamlessly extendable to RGB-D SLAM when an external depth sensor is available. Several innovations are required to continuously reconstruct 3D scenes with high fidelity from a live camera. First, to move beyond the original 3DGS algorithm, which requires accurate poses from an offline Structure from Motion (SfM) system, we formulate camera tracking for 3DGS using direct optimisation against the 3D Gaussians, and show that this enables fast and robust tracking with a wide basin of convergence. Second, by utilising the explicit nature of the Gaussians, we introduce geometric verification and regularisation to handle the ambiguities occurring in incremental 3D dense reconstruction. Finally, we introduce a full SLAM system which not only achieves state-of-the-art results in novel view synthesis and trajectory estimation but also reconstruction of tiny and even transparent objects. (arXiv)

## 🧠 Key ideas (atomic)

- The authors present what they call the first online visual SLAM system based solely on the 3D Gaussian Splatting representation. (Matsuki et al., 2023) `ev:asserted` p. 2 ^matsuki2023gaussian-001
- The system uses 3D Gaussians as the only representation for tracking, mapping, keyframe management and novel view synthesis. (Matsuki et al., 2023) `ev:asserted` p. 4 ^matsuki2023gaussian-002
- The monocular method relies solely on RGB image inputs, without any pretrained monocular depth predictor or other existing tracking modules. (Matsuki et al., 2023) `ev:reported` p. 2 ^matsuki2023gaussian-003
- The authors state the monocular method can easily be extended to RGB-D SLAM when depth measurements are available. (Matsuki et al., 2023) `ev:asserted` p. 2 ^matsuki2023gaussian-004
- The authors derive an analytic Jacobian on the Lie group of camera pose with respect to a 3D Gaussians map. (Matsuki et al., 2023) `ev:computed` p. 2 ^matsuki2023gaussian-005
- To the authors' knowledge, this is the first analytical Jacobian of SE(3) camera pose with respect to 3D Gaussians in EWA splatting. (Matsuki et al., 2023) `ev:asserted` p. 4 ^matsuki2023gaussian-006
- Lie algebra is used to derive minimal Jacobians whose dimensionality matches the degrees of freedom, eliminating redundant computations. (Matsuki et al., 2023) `ev:reported` p. 4 ^matsuki2023gaussian-007
- The authors state that accurate tracking typically requires at least 50 iterations of gradient descent per frame. (Matsuki et al., 2023) `ev:asserted` p. 4 ^matsuki2023gaussian-008
- During tracking, only the current camera pose is optimised against an L1 photometric residual, without updates to the map. (Matsuki et al., 2023) `ev:reported` p. 4 ^matsuki2023gaussian-009
- Tracking additionally optimises affine brightness parameters for varying exposure and penalises non-edge or low-opacity pixels. (Matsuki et al., 2023) `ev:reported` p. 4 ^matsuki2023gaussian-010
- With depth available, tracking minimises a weighted sum of photometric and geometric residuals, with λpho = 0.9 in RGB-D experiments. (Matsuki et al., 2023) `ev:reported` p. 10 ^matsuki2023gaussian-011
- Tracking performs 100 iterations per frame, terminating early if the magnitude of the pose update becomes less than 10−4. (Matsuki et al., 2023) `ev:reported` p. 10 ^matsuki2023gaussian-012
- The Adam optimiser updates camera poses with learning rates of 0.003 for rotation and 0.001 for translation. (Matsuki et al., 2023) `ev:reported` p. 10 ^matsuki2023gaussian-013
- Keyframe covisibility is measured as the intersection over union of Gaussians observed in the current frame and the last keyframe. (Matsuki et al., 2023) `ev:reported` p. 5 ^matsuki2023gaussian-014
- A frame becomes a keyframe if covisibility drops below a threshold or its relative translation is large relative to median depth. (Matsuki et al., 2023) `ev:reported` p. 5 ^matsuki2023gaussian-015
- A keyframe is removed from the current window when its overlap coefficient with the latest keyframe drops below a threshold. (Matsuki et al., 2023) `ev:reported` p. 5 ^matsuki2023gaussian-016
- The keyframe window holds 10 keyframes for Replica and 8 keyframes for TUM in the reported configuration. (Matsuki et al., 2023) `ev:reported` p. 10 ^matsuki2023gaussian-017
- A Gaussian is marked visible from a view if used in rasterisation before the ray's accumulated alpha reaches 0.5. (Matsuki et al., 2023) `ev:reported` p. 5 ^matsuki2023gaussian-018
- The authors state that this Gaussian covisibility estimate lets the system handle occlusions without requiring any additional heuristics. (Matsuki et al., 2023) `ev:asserted` p. 5 ^matsuki2023gaussian-019
- In the monocular case, pixels without rendered depth receive new Gaussians around the median rendered depth with high variance. (Matsuki et al., 2023) `ev:reported` p. 5 ^matsuki2023gaussian-020
- Gaussians inserted within the last 3 keyframes that are unobserved by at least 3 other frames are pruned as geometrically unstable. (Matsuki et al., 2023) `ev:reported` p. 5 ^matsuki2023gaussian-021
- In addition to visibility-based pruning, the system prunes all Gaussians with an opacity of less than 0.7. (Matsuki et al., 2023) `ev:reported` p. 10 ^matsuki2023gaussian-022
- Mapping optimises over the current keyframe window plus two random past keyframes per iteration to avoid forgetting the global map. (Matsuki et al., 2023) `ev:reported` p. 5 ^matsuki2023gaussian-023
- An isotropic regularisation penalises each Gaussian's scaling parameters by their difference to the mean, which encourages sphericality. (Matsuki et al., 2023) `ev:reported` p. 5 ^matsuki2023gaussian-024
- The authors observe that under insufficient photometric constraints, Gaussians tend to elongate along the viewing direction, creating artefacts in novel views. (Matsuki et al., 2023) `ev:asserted` p. 6 ^matsuki2023gaussian-025
- Quantitative evaluation uses 3 TUM RGB-D sequences and 8 Replica sequences, with Replica used for RGB-D evaluation only. (Matsuki et al., 2023) `ev:reported` p. 6 ^matsuki2023gaussian-026
- The system ran on a desktop with an Intel Core i9 12900K and a single NVIDIA GeForce RTX 4090. (Matsuki et al., 2023) `ev:reported` p. 6 ^matsuki2023gaussian-027
- Time-critical rasterisation and gradient computation are implemented in CUDA, with the rest of the SLAM pipeline developed in PyTorch. (Matsuki et al., 2023) `ev:reported` p. 6 ^matsuki2023gaussian-028
- Tracking accuracy is reported as keyframe ATE RMSE, with scale alignment applied only in the monocular evaluation. (Matsuki et al., 2023) `ev:reported` p. 10 ^matsuki2023gaussian-029
- On TUM monocular, the method reaches an average ATE RMSE of 3.96 cm, against 7.73 cm for DROID-VO. (Matsuki et al., 2023) `ev:measured` p. 7 ^matsuki2023gaussian-030
- Among locally run monocular baselines without loop closure, DSO averages 11.0 cm and DepthCov-VO 25.2 cm ATE on TUM. (Matsuki et al., 2023) `ev:measured` p. 7 ^matsuki2023gaussian-031
- Monocular systems with loop closure remain more accurate on TUM, with DROID-SLAM at 1.70 cm and ORB-SLAM2 at 1.60 cm. (Matsuki et al., 2023) `ev:cited` p. 7 ^matsuki2023gaussian-032
- On TUM RGB-D, the method averages 1.47 cm ATE, lower than all listed RGB-D baselines without loop closure. (Matsuki et al., 2023) `ev:measured` p. 7 ^matsuki2023gaussian-033
- On the TUM fr1/desk sequence with RGB-D input, the method's 1.50 cm ATE is below ORB-SLAM2's 1.60 cm. (Matsuki et al., 2023) `ev:measured` p. 7 ^matsuki2023gaussian-034
- On Replica RGB-D, the single-process implementation achieves the best tracking result in 6 out of 8 sequences. (Matsuki et al., 2023) `ev:measured` p. 6 ^matsuki2023gaussian-035
- On Replica, the single-process implementation averages 0.32 cm ATE, while the multi-process implementation averages 0.58 cm. (Matsuki et al., 2023) `ev:measured` p. 7 ^matsuki2023gaussian-036
- The authors attribute their higher performance on real-world TUM data to optimising Gaussian positions to compensate for sensor noise. (Matsuki et al., 2023) `ev:asserted` p. 6 ^matsuki2023gaussian-037
- On Replica RGB-D, the method reports 38.94 PSNR and 0.070 LPIPS, against 35.17 and 0.124 for Point-SLAM. (Matsuki et al., 2023) `ev:measured` p. 7 ^matsuki2023gaussian-038
- On Replica RGB-D rendering, Point-SLAM's SSIM of 0.975 is higher than the method's SSIM of 0.968. (Matsuki et al., 2023) `ev:measured` p. 7 ^matsuki2023gaussian-039
- The method renders at 769 fps, while Vox-Fusion, the second best listed method, renders at 2.17 fps. (Matsuki et al., 2023) `ev:measured` p. 11 ^matsuki2023gaussian-040
- Rendering fps was computed from the average time of 100 full-resolution renderings at 1200 × 680 on Replica. (Matsuki et al., 2023) `ev:reported` p. 11 ^matsuki2023gaussian-041
- The authors note that Point-SLAM's view synthesis depends on depth-guided ray sampling, making novel-view synthesis challenging for it. (Matsuki et al., 2023) `ev:asserted` p. 7 ^matsuki2023gaussian-042
- On TUM monocular, removing the isotropic regularisation raises average ATE from 3.96 cm to 4.83 cm. (Matsuki et al., 2023) `ev:measured` p. 7 ^matsuki2023gaussian-043
- On TUM RGB-D, removing the geometric residual raises average ATE from 1.47 cm to 2.66 cm. (Matsuki et al., 2023) `ev:measured` p. 7 ^matsuki2023gaussian-044
- Removing keyframe selection raises average TUM ATE to 8.73 cm for monocular input and 1.90 cm for RGB-D input. (Matsuki et al., 2023) `ev:measured` p. 7 ^matsuki2023gaussian-045
- Without Gaussian pruning, monocular average ATE on TUM rises to 46.6 cm, compared with 3.96 cm with pruning. (Matsuki et al., 2023) `ev:measured` p. 13 ^matsuki2023gaussian-046
- On TUM RGB-D, the isotropic loss shows only a marginal difference, with 1.43 cm ATE without it versus 1.47 cm. (Matsuki et al., 2023) `ev:measured` p. 13 ^matsuki2023gaussian-047
- On Replica RGB-D, the isotropic loss lowers average ATE from 0.82 cm without it to 0.58 cm. (Matsuki et al., 2023) `ev:measured` p. 13 ^matsuki2023gaussian-048
- On TUM, the final Gaussian map occupies 2.6MB for monocular input and 3.97MB for RGB-D input. (Matsuki et al., 2023) `ev:measured` p. 7 ^matsuki2023gaussian-049
- The authors argue MLP-based iMAP is more memory efficient but struggles to express high-fidelity scenes given limited MLP capacity. (Matsuki et al., 2023) `ev:asserted` p. 7 ^matsuki2023gaussian-050
- Original Gaussian Splatting uses approximately 300-700MB for the standard novel view synthesis benchmark dataset, according to the authors. (Matsuki et al., 2023) `ev:cited` p. 14 ^matsuki2023gaussian-051
- In the convergence analysis, pose optimisation runs 1000 iterations and succeeds if it converges within 1cm of the target view. (Matsuki et al., 2023) `ev:reported` p. 8 ^matsuki2023gaussian-052
- Convergence training views form a 0.5m square, with test cameras distributed at radii ranging from 0.2m to 1.2m. (Matsuki et al., 2023) `ev:reported` p. 8 ^matsuki2023gaussian-053
- Average convergence success is 0.79 without depth and 0.82 with depth, versus 0.14 for Hash Grid SDF. (Matsuki et al., 2023) `ev:measured` p. 8 ^matsuki2023gaussian-054
- The MLP SDF baseline built on the iMAP network reaches an average convergence success ratio of 0.33 across three sequences. (Matsuki et al., 2023) `ev:measured` p. 8 ^matsuki2023gaussian-055
- The authors attribute the larger convergence basin to anisotropic Gaussians forming a smooth gradient, unlike hashing and positional encoding. (Matsuki et al., 2023) `ev:asserted` p. 8 ^matsuki2023gaussian-056
- On TUM fr3/office, the multi-process system runs at 3.2 FPS with monocular input and 2.5 FPS with RGB-D. (Matsuki et al., 2023) `ev:measured` p. 12 ^matsuki2023gaussian-057
- On Replica office1, the RGB-D system runs at 1.8 FPS multi-process and 1.1 FPS as single-process implementation. (Matsuki et al., 2023) `ev:measured` p. 12 ^matsuki2023gaussian-058
- Enabling spherical harmonics raises mean TUM RGB-D PSNR of the method from 21.89 to 24.37 in the ablation. (Matsuki et al., 2023) `ev:measured` p. 13 ^matsuki2023gaussian-059
- With spherical harmonics enabled, mean TUM RGB-D ATE marginally worsens from 1.47cm to 1.56cm in the ablation. (Matsuki et al., 2023) `ev:measured` p. 13 ^matsuki2023gaussian-060
- The authors suggest spherical harmonics may incorrectly explain non-view-directional effects caused by camera motion, degrading the trajectory estimate. (Matsuki et al., 2023) `ev:asserted` p. 13 ^matsuki2023gaussian-061
- The authors report no significant rendering-metric difference between their method and 3DGS trained offline on RGB-D ORB-SLAM poses. (Matsuki et al., 2023) `ev:measured` p. 13 ^matsuki2023gaussian-062
- On EuRoC Machine Hall with stereo depth, ATE RMSE is 0.121 m on 01-easy but 4.515 m on 04-difficult. (Matsuki et al., 2023) `ev:measured` p. 13 ^matsuki2023gaussian-063
- The authors report that Point-SLAM fails on all sequences of the EuRoC Machine Hall dataset with stereo depth. (Matsuki et al., 2023) `ev:measured` p. 13 ^matsuki2023gaussian-064
- The authors state the method has been tested only on small room-scale scenes, where larger scenes would suffer inevitable drift. (Matsuki et al., 2023) `ev:asserted` p. 15 ^matsuki2023gaussian-065
- Hard real-time operation at 30 fps on TUM sequences is not achieved, although the system runs interactively live. (Matsuki et al., 2023) `ev:asserted` p. 15 ^matsuki2023gaussian-066
- The authors name integration of loop closure for handling large-scale scenes as an interesting direction for future research. (Matsuki et al., 2023) `ev:asserted` p. 9 ^matsuki2023gaussian-067
- The authors state that by not explicitly modelling a surface, the system naturally handles transparent objects in monocular SLAM. (Matsuki et al., 2023) `ev:asserted` p. 8 ^matsuki2023gaussian-068

## 🎯 Contributions

## 📖 Glossary

- **3D Gaussian Splatting (3DGS)** — Scene representation of anisotropic Gaussians rendered by differentiable rasterisation instead of ray marching.
- **Splatting** — Projecting 3D Gaussians to 2D image-plane Gaussians and alpha-blending them per pixel.
- **ATE RMSE** — Root mean square of absolute trajectory error between estimated and ground-truth poses.
- **Map-centric SLAM** — SLAM that tracks against one unified, globally consistent 3D map representation.
- **Covisibility** — Overlap between the sets of map primitives visible from two camera views.
- **Overlap coefficient** — Intersection size divided by the smaller of two sets' sizes.
- **Isotropic regularisation** — Loss penalising Gaussian scale deviation from its mean, pushing Gaussians toward spheres.
- **Convergence basin** — Region of initial poses from which pose optimisation reaches the correct pose.
- **Analytic Jacobian on Lie group** — Closed-form derivative of rendering outputs with respect to minimal SE(3) pose parameters.
- **Spherical harmonics (SH)** — Basis functions encoding view-dependent colour of each Gaussian.

## ❓ Open questions

- How would a loop closure module integrate with a Gaussian map, and would it be as easy as with surfel maps?
- Can a second-order optimiser bring the system to hard real-time (30 fps) operation?
- How can surfaces or surface normals be extracted from Gaussians that do not explicitly represent a surface?
- Why does tracking accuracy degrade so strongly on the difficult, longer EuRoC sequences, and what fixes it beyond loop closure?
- Can view-dependent appearance (SH) be added without harming trajectory estimation?
- Would a unified 3DGS tracker close the rendering gap to ORB-SLAM poses plus offline 3DGS seen on TUM in Table 15?

## 📝 Notes on reading

Version read: arXiv 2312.06741v2 (14 Apr 2024) with supplementary material (pp. 10-19); references on pp. 20-21.

Inconsistencies inside the paper:
- Table 5 (p. 7) gives the method's Replica average as PSNR 38.94 / SSIM 0.968, while the per-sequence Table 7 (p. 12) averages to PSNR 37.50 / SSIM 0.960; the LPIPS (0.070) and 769 fps agree.
- Table 15 (p. 13) lists Point-SLAM Replica PSNR as 24.37, whereas Table 5 gives 35.17.
- Table 15 shows ORB+GS with higher TUM PSNR (25.12) than the method (21.89), yet the text says no significant rendering difference.
- The timing text (p. 14) cites Table 10 for 3.2/2.5 FPS and mentions Replica office2, but these figures are in Table 9 (fr3/office) and Table 10 uses replica/office1.
- The pruning ablation text refers to 'Table 9.1'; the table is numbered Table 11.
- The abstract calls this the first application of 3DGS in monocular SLAM, while the conclusion says first SLAM method using 3D Gaussians.

Garbled extraction: Table 4 (p. 7) memory for NICE-SLAM reads '40.3.4MB' and was not claimed. Equations (3)-(6) and (19)-(34) are only partially readable in the extracted text.

Figures described only: Fig. 1 (live monocular reconstruction with wires and transparent objects), Fig. 3 (effect of isotropic regularisation on novel views), Fig. 4 and Figs. 9-16 (qualitative rendering comparisons with Point-SLAM and ESLAM), Fig. 5 and Fig. 8 (convergence funnel layout and results), Fig. 7 (self-captured scenes with Intel Realsense d455).

## Suggested new concepts

- 3D Gaussian Splatting SLAM — a new family of map-centric SLAM systems built on explicit Gaussian primitives.
- Differentiable rasterisation — contrasting rasterisation-based and ray-marching differentiable rendering matters for real-time SLAM.
- Convergence basin analysis — a reusable evaluation protocol for comparing map representations for camera localisation.
- Covisibility-based keyframe management — keyframe selection and pruning from shared visible primitives recurs across SLAM systems.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Seguimiento de cámara con Jacobianos en $\mathfrak{se}(3)$ sobre 3DGS
