---
aliases: []
type: "source"
title: "BARF: Bundle-Adjusting Neural Radiance Fields"
citekey: "Lin2021barf"
doi: "10.48550/arXiv.2104.06405"
arxiv: "2104.06405"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2104.06405"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Chen-Hsuan Lin", "Wei-Chiu Ma", "Antonio Torralba", "Simon Lucey"]
sha256: ["1261b93ddaf172e6700f2bc806deea1bde1a857dcd64dc6cc45a2fe2fee5e25a"]
pdf: "Content/Papers/Lin2021barf.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 56
---

📄 PDF: [[Lin2021barf.pdf]]

> [!abstract] One-sentence summary
> BARF trains a NeRF from imperfect or unknown camera poses by gradually enabling positional-encoding frequency bands, a coarse-to-fine schedule that recovers poses jointly with the scene on synthetic and LLFF data.

## Abstract

Neural Radiance Fields (NeRF) have recently gained a surge of interest within the computer vision community for its power to synthesize photorealistic novel views of real-world scenes. One limitation of NeRF, however, is its requirement of accurate camera poses to learn the scene representations. In this paper, we propose Bundle-Adjusting Neural Radiance Fields (BARF) for training NeRF from imperfect (or even unknown) camera poses -- the joint problem of learning neural 3D representations and registering camera frames. We establish a theoretical connection to classical image alignment and show that coarse-to-fine registration is also applicable to NeRF. Furthermore, we show that naïvely applying positional encoding in NeRF has a negative impact on registration with a synthesis-based objective. Experiments on synthetic and real-world data show that BARF can effectively optimize the neural scene representations and resolve large camera pose misalignment at the same time. This enables view synthesis and localization of video sequences from unknown camera poses, opening up new avenues for visual localization systems (e.g. SLAM) and potential applications for dense 3D mapping and reconstruction. (arXiv)

## 🧠 Key ideas (atomic)

- A hard prerequisite of NeRF and other view synthesis methods is accurate camera poses, typically obtained through auxiliary off-the-shelf algorithms. (Lin et al., 2021) `ev:asserted` p. 2 ^lin2021barf-001
- The authors state that naive pose optimization jointly with NeRF is sensitive to initialization and may degrade view synthesis quality. (Lin et al., 2021) `ev:asserted` p. 2 ^lin2021barf-002
- BARF addresses training NeRF from imperfect camera poses, framed as jointly reconstructing the 3D scene and registering the camera poses. (Lin et al., 2021) `ev:asserted` p. 2 ^lin2021barf-003
- The authors regard BARF as a type of photometric bundle adjustment that uses view synthesis as the proxy objective. (Lin et al., 2021) `ev:asserted` p. 2 ^lin2021barf-004
- Unlike traditional bundle adjustment, BARF can learn scene representations from randomly initialized network weights, without relying on local registration subprocedures. (Lin et al., 2021) `ev:asserted` p. 2 ^lin2021barf-005
- Classical SfM and SLAM systems are described as sensitive to local registration quality and prone to falling into suboptimal solutions. (Lin et al., 2021) `ev:asserted` p. 1 ^lin2021barf-006
- Concurrent work NeRF-- introduced an empirical two-stage pipeline to estimate unknown camera poses for NeRF. (Lin et al., 2021) `ev:cited` p. 3 ^lin2021barf-007
- In contrast to NeRF--, BARF is said to recover camera poses within a single course of optimization. (Lin et al., 2021) `ev:asserted` p. 3 ^lin2021barf-008
- The paper derives a steepest descent image for NeRF analogous to classical 2D image alignment, formed in practice via backpropagation. (Lin et al., 2021) `ev:computed` p. 4 ^lin2021barf-009
- In classical image alignment, coarse-to-fine strategies blur images early in registration to widen the basin of attraction. (Lin et al., 2021) `ev:asserted` p. 3 ^lin2021barf-010
- Representing images as neural networks turns image gradients into the analytical Jacobian of the network rather than a numerical estimate. (Lin et al., 2021) `ev:asserted` p. 4 ^lin2021barf-011
- The Jacobian of the k-th positional encoding amplifies gradient signals from the MLP by a factor of 2kπ. (Lin et al., 2021) `ev:computed` p. 4 ^lin2021barf-012
- The authors argue that positional encoding makes gradients from sampled 3D points incoherent, so they can cancel each other out. (Lin et al., 2021) `ev:asserted` p. 5 ^lin2021barf-013
- BARF applies a smooth mask over positional-encoding frequency bands, from low to high, acting like a dynamic low-pass filter. (Lin et al., 2021) `ev:reported` p. 5 ^lin2021barf-014
- A controllable parameter α in [0, L], proportional to optimization progress, sets the weight of each frequency component. (Lin et al., 2021) `ev:reported` p. 5 ^lin2021barf-015
- When α reaches L, full positional encoding is enabled, which the authors state is equivalent to the original NeRF model. (Lin et al., 2021) `ev:asserted` p. 5 ^lin2021barf-016
- The 2D experiment recovers homography warps for M = 5 patches of a representative ImageNet image by optimizing a neural image network. (Lin et al., 2021) `ev:reported` p. 5 ^lin2021barf-017
- In planar alignment, full positional encoding reached an sl(3) error of 0.2949 with a patch PSNR of 23.41. (Lin et al., 2021) `ev:measured` p. 6 ^lin2021barf-018
- In planar alignment, the network without positional encoding reached an sl(3) error of 0.0641 with a patch PSNR of 24.72. (Lin et al., 2021) `ev:measured` p. 6 ^lin2021barf-019
- In planar alignment, BARF reached an sl(3) error of 0.0096 with a patch PSNR of 35.30. (Lin et al., 2021) `ev:measured` p. 6 ^lin2021barf-020
- Alignment with full positional encoding produced suboptimal registration with ghostly artifacts in the recovered image representation. (Lin et al., 2021) `ev:measured` p. 5 ^lin2021barf-021
- Alignment without positional encoding registered decently but could not recover the image with sufficient fidelity. (Lin et al., 2021) `ev:measured` p. 5 ^lin2021barf-022
- In a translational alignment study, naive positional encoding gave a more nonlinear alignment landscape and a smaller basin of attraction. (Lin et al., 2021) `ev:measured` p. 9 ^lin2021barf-023
- In the same translational alignment study, BARF widened the basin of attraction compared with naive positional encoding. (Lin et al., 2021) `ev:measured` p. 9 ^lin2021barf-024
- Synthetic experiments use the 8 object-centric NeRF scenes, each with M = 100 rendered training images and ground-truth poses. (Lin et al., 2021) `ev:reported` p. 5 ^lin2021barf-025
- Synthetic camera poses were perturbed with additive noise corresponding to a standard deviation of 14.9° in rotation. (Lin et al., 2021) `ev:reported` p. 5 ^lin2021barf-026
- The synthetic setup trains a single 128-unit MLP without hierarchical sampling, on 400 × 400 images for 200K iterations. (Lin et al., 2021) `ev:reported` p. 5 ^lin2021barf-027
- For synthetic scenes, α is adjusted linearly from iteration 20K to 100K, after which all frequency bands up to L = 10 are active. (Lin et al., 2021) `ev:reported` p. 6 ^lin2021barf-028
- On synthetic scenes, registration is evaluated after Procrustes alignment of the optimized camera locations to the ground-truth poses. (Lin et al., 2021) `ev:reported` p. 6 ^lin2021barf-029
- View synthesis evaluation adds test-time photometric optimization to factor out pose error that may contaminate synthesis quality. (Lin et al., 2021) `ev:reported` p. 6 ^lin2021barf-030
- On synthetic scenes, NeRF with full positional encoding had a mean rotation error of 6.167° after pose perturbation. (Lin et al., 2021) `ev:measured` p. 7 ^lin2021barf-031
- On synthetic scenes, BARF had a mean rotation error of 0.193° against 0.202° without positional encoding. (Lin et al., 2021) `ev:measured` p. 7 ^lin2021barf-032
- The Table 2 caption states that BARF optimizes camera registration with less than 0.2° rotation error on the synthetic scenes. (Lin et al., 2021) `ev:measured` p. 7 ^lin2021barf-033
- On synthetic scenes, NeRF without positional encoding recovered alignment but its learned scene representations lacked reconstruction fidelity. (Lin et al., 2021) `ev:measured` p. 6 ^lin2021barf-034
- On the Lego scene, BARF reached a PSNR of 28.33 versus 29.28 for NeRF trained under ground-truth poses. (Lin et al., 2021) `ev:measured` p. 7 ^lin2021barf-035
- On synthetic scenes, BARF reached a mean SSIM of 0.930 against 0.936 for the reference NeRF with perfect poses. (Lin et al., 2021) `ev:measured` p. 7 ^lin2021barf-036
- The authors state BARF achieves view synthesis quality comparable to NeRF trained under ground-truth poses in all metrics. (Lin et al., 2021) `ev:measured` p. 6 ^lin2021barf-037
- Real-world experiments use the 8 forward-facing LLFF scenes, with all cameras initialized to the identity transformation. (Lin et al., 2021) `ev:reported` p. 7 ^lin2021barf-038
- The LLFF poses are themselves SfM estimates, so the pose evaluation is at most an indication of agreement with classical estimation. (Lin et al., 2021) `ev:asserted` p. 7 ^lin2021barf-039
- For LLFF, the authors hold out the last 10% of each sequence for testing instead of every 8th frame. (Lin et al., 2021) `ev:reported` p. 10 ^lin2021barf-040
- On LLFF, NeRF with full positional encoding had a mean rotation error of 84.509° from identity-initialized poses. (Lin et al., 2021) `ev:measured` p. 8 ^lin2021barf-041
- On LLFF, BARF had a mean rotation error of 0.573° relative to the SfM-estimated poses. (Lin et al., 2021) `ev:measured` p. 8 ^lin2021barf-042
- On LLFF, BARF reached a mean PSNR of 23.97 against 11.03 for NeRF with full positional encoding. (Lin et al., 2021) `ev:measured` p. 8 ^lin2021barf-043
- On LLFF, BARF's mean PSNR of 23.97 exceeded the 22.56 of the reference NeRF trained under SfM poses. (Lin et al., 2021) `ev:measured` p. 8 ^lin2021barf-044
- On LLFF, BARF reached a mean LPIPS of 0.238 against 0.283 for the reference NeRF. (Lin et al., 2021) `ev:measured` p. 8 ^lin2021barf-045
- On LLFF, NeRF with naive positional encoding diverged to incorrect camera poses, resulting in poor view synthesis. (Lin et al., 2021) `ev:measured` p. 7 ^lin2021barf-046
- On LLFF, the baseline without positional encoding reached a mean rotation error of 0.699° relative to SfM poses. (Lin et al., 2021) `ev:measured` p. 11 ^lin2021barf-047
- On LLFF, the baseline without positional encoding reached a mean PSNR of 23.82, close to BARF's 23.97. (Lin et al., 2021) `ev:measured` p. 11 ^lin2021barf-048
- The authors note BARF and the no-encoding baseline are competitive in different metrics on the LLFF scenes. (Lin et al., 2021) `ev:measured` p. 11 ^lin2021barf-049
- The authors state the optimal coarse-to-fine schedule would be data-dependent, and searching for it is out of scope. (Lin et al., 2021) `ev:asserted` p. 11 ^lin2021barf-050
- Sampling points in metric depth instead of inverse depth lowered performance for all compared methods on LLFF. (Lin et al., 2021) `ev:measured` p. 11 ^lin2021barf-051
- With metric depth sampling, the baseline without positional encoding may be slightly better than BARF. (Lin et al., 2021) `ev:measured` p. 11 ^lin2021barf-052
- The authors state BARF shares NeRF limitations, including slow optimization and rendering, rigidity assumptions and sensitivity to dense 3D sampling. (Lin et al., 2021) `ev:asserted` p. 8 ^lin2021barf-053
- The authors state that, beyond the limitations of NeRF, BARF also relies on heuristic coarse-to-fine scheduling strategies. (Lin et al., 2021) `ev:asserted` p. 8 ^lin2021barf-054
- The authors suggest many recent improvements to NeRF are potentially transferable to BARF, given its close formulation. (Lin et al., 2021) `ev:asserted` p. 8 ^lin2021barf-055
- The authors conclude that coarse-to-fine registration is necessary for joint registration and reconstruction with coordinate-based scene representations. (Lin et al., 2021) `ev:asserted` p. 8 ^lin2021barf-056

## 🎯 Contributions

## 📖 Glossary

- **Bundle adjustment** — Joint refinement of 3D structure and camera poses by minimizing reprojection or photometric error.
- **Positional encoding** — Mapping of input coordinates to sinusoids of increasing frequency before an MLP.
- **Basin of attraction** — Range of initial misalignments from which optimization converges to the correct solution.
- **Coarse-to-fine registration** — Aligning first on smooth, low-frequency signals, then adding higher-frequency detail.
- **Steepest descent image** — Jacobian of the synthesized image with respect to the warp or pose parameters.
- **Procrustes analysis** — Similarity alignment of two point sets via scale, rotation and translation.
- **LLFF** — Dataset of forward-facing real scenes captured with hand-held cameras.
- **se(3) Lie algebra** — Six-parameter tangent-space parametrization of 3D rigid camera poses.

## ❓ Open questions

- How should the coarse-to-fine schedule be chosen per scene, adaptively or by search, rather than by fixed heuristic?
- Why does the no-encoding baseline match or beat BARF on some LLFF metrics, and under metric depth sampling?
- Does BARF extend to unknown camera intrinsics, which all experiments assume known?
- How far do NeRF speed-ups and non-rigid extensions transfer to BARF's joint pose optimization?
- How should novel-view test poses be chosen when optimized poses cannot be aligned to a reference frame?

## 📝 Notes on reading

- Version read: arXiv v2 (19 Aug 2021), including appendices A and B (pp. 9–12); the packet identifier is the arXiv record.
- Table 2 (p. 7): the "Mean" PSNR row for full / w/o / BARF (22.12 / 26.78 / 27.50) is identical to the Ship row; the per-scene BARF values average to about 28.84, so the printed mean PSNR looks like a copy error. No claim was made from the mean PSNR of Table 2.
- Table 5 shows the no-encoding baseline has a lower mean translation error (0.298) than BARF (0.331).
- Table 3 SSIM for BARF (0.722) is slightly below the no-encoding baseline in Table 5 (0.724).
- Figures 2, 4, 5, 8, 9, 10 and 11 are qualitative (warp visualizations, pose trajectories, basin maps) and were only described.
- Equations (9), (13)–(14) and Algorithm 1 are partly garbled by extraction; the weight schedule was paraphrased, not quoted.
- The synthetic perturbation also gives 0.26 in translational magnitude, not claimed separately.
- The Table 2 caption says BARF has less than 0.2° rotation error, which holds for the mean (0.193) but not for every scene: Materials is 0.844 and Hotdog 0.248.

## Suggested new concepts

- Coarse-to-fine positional encoding — a reusable schedule for frequency annealing in coordinate networks beyond NeRF.
- Joint pose and radiance field optimization — the general problem BARF, NeRF-- and iNeRF address, relevant to SLAM-style mapping.
- Photometric bundle adjustment — the classical direct-method family BARF positions itself within.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Optimización conjunta de NeRF y poses, de grueso a fino

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
