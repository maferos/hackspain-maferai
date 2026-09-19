---
aliases: []
type: "source"
title: "PVNet: Pixel-wise Voting Network for 6DoF Pose Estimation"
citekey: "Peng2018pvnet"
doi: "10.48550/arXiv.1812.11788"
arxiv: "1812.11788"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1812.11788"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Sida Peng", "Yuan Liu", "Qixing Huang", "Hujun Bao", "Xiaowei Zhou"]
sha256: ["1fa219dedf1bb34a8cc236f45e3dad7c16aaffe38ca60da0e32ca98c05430d76"]
pdf: "Content/Papers/Peng2018pvnet.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 58
---

📄 PDF: [[Peng2018pvnet.pdf]]

> [!abstract] One-sentence summary
> PVNet estimates 6DoF object pose from one RGB image by predicting per-pixel unit vectors that vote for 2D keypoints via RANSAC, then solving an uncertainty-weighted PnP, which makes keypoint localization robust to occlusion and truncation.

## Abstract

This paper addresses the challenge of 6DoF pose estimation from a single RGB image under severe occlusion or truncation. Many recent works have shown that a two-stage approach, which first detects keypoints and then solves a Perspective-n-Point (PnP) problem for pose estimation, achieves remarkable performance. However, most of these methods only localize a set of sparse keypoints by regressing their image coordinates or heatmaps, which are sensitive to occlusion and truncation. Instead, we introduce a Pixel-wise Voting Network (PVNet) to regress pixel-wise unit vectors pointing to the keypoints and use these vectors to vote for keypoint locations using RANSAC. This creates a flexible representation for localizing occluded or truncated keypoints. Another important feature of this representation is that it provides uncertainties of keypoint locations that can be further leveraged by the PnP solver. Experiments show that the proposed approach outperforms the state of the art on the LINEMOD, Occlusion LINEMOD and YCB-Video datasets by a large margin, while being efficient for real-time pose estimation. We further create a Truncation LINEMOD dataset to validate the robustness of our approach against truncation. The code will be avaliable at https://zju-3dv.github.io/pvnet/. (arXiv)

## 🧠 Key ideas (atomic)

- PVNet targets recovering the 6DoF pose of an object, meaning its 3D rotation and translation, from a single RGB image. (Peng et al., 2018) `ev:asserted` p. 1 ^peng2018pvnet-001
- The authors note it is unclear whether end-to-end deep networks mapping images directly to pose learn sufficient feature representations for pose estimation. (Peng et al., 2018) `ev:cited` p. 1 ^peng2018pvnet-002
- Two-stage methods that regress 2D keypoints and then solve PnP have difficulty with occluded and truncated objects, since some keypoints are unseen. (Peng et al., 2018) `ev:cited` p. 2 ^peng2018pvnet-003
- The authors argue that handling occlusion and truncation requires dense predictions, meaning pixel-wise or patch-wise estimates of outputs or intermediate representations. (Peng et al., 2018) `ev:asserted` p. 2 ^peng2018pvnet-004
- Instead of regressing keypoint coordinates, PVNet predicts unit vectors pointing from each object pixel towards each keypoint. (Peng et al., 2018) `ev:reported` p. 2 ^peng2018pvnet-005
- Keypoint locations are then obtained by letting these predicted directions vote for candidate locations within a RANSAC-based scheme. (Peng et al., 2018) `ev:reported` p. 2 ^peng2018pvnet-006
- The voting design is motivated by rigid objects, where seeing some local parts allows inferring the relative directions to other parts. (Peng et al., 2018) `ev:asserted` p. 2 ^peng2018pvnet-007
- The authors argue that the vector-field representation can represent object keypoints lying outside the input image, which suits truncated objects. (Peng et al., 2018) `ev:asserted` p. 2 ^peng2018pvnet-008
- According to the authors, RANSAC-based voting prunes outlier predictions and also gives a spatial probability distribution for each keypoint. (Peng et al., 2018) `ev:asserted` p. 2 ^peng2018pvnet-009
- The contribution summary reports ADD accuracy of 86.3% versus 79% on LINEMOD and 40.8% versus 30.4% on Occlusion LINEMOD. (Peng et al., 2018) `ev:measured` p. 2 ^peng2018pvnet-010
- Heatmap-based keypoint methods have difficulty handling truncated objects since heatmaps are fixed-size and keypoints may lie outside the input image. (Peng et al., 2018) `ev:cited` p. 3 ^peng2018pvnet-011
- The authors state that regressing dense object coordinates is more difficult than keypoint detection due to the larger output space. (Peng et al., 2018) `ev:asserted` p. 3 ^peng2018pvnet-012
- The authors describe PVNet as a hybrid of keypoint-based and dense methods that combines advantages of both families. (Peng et al., 2018) `ev:asserted` p. 3 ^peng2018pvnet-013
- PVNet performs semantic segmentation and vector-field prediction, outputting an object label and a unit vector per keypoint for every pixel. (Peng et al., 2018) `ev:reported` p. 4 ^peng2018pvnet-014
- Keypoint hypotheses are generated by repeatedly choosing two random object pixels and intersecting their predicted vectors, repeated N times. (Peng et al., 2018) `ev:reported` p. 4 ^peng2018pvnet-015
- Each hypothesis is scored by counting object pixels whose predicted direction agrees with it above a threshold of 0.99. (Peng et al., 2018) `ev:reported` p. 4 ^peng2018pvnet-016
- The weighted hypotheses yield a mean and covariance per keypoint, describing its spatial probability distribution for later use in PnP. (Peng et al., 2018) `ev:reported` p. 4 ^peng2018pvnet-017
- Bounding box corner keypoints lie far from object pixels, which the authors state results in larger localization errors under vector voting. (Peng et al., 2018) `ev:asserted` p. 4 ^peng2018pvnet-018
- Keypoints are selected on the object surface with farthest point sampling, starting from the object center, until K keypoints are chosen. (Peng et al., 2018) `ev:reported` p. 5 ^peng2018pvnet-019
- Considering both accuracy and efficiency in their experiments, the authors suggest using K = 8 keypoints selected by farthest point sampling. (Peng et al., 2018) `ev:asserted` p. 5 ^peng2018pvnet-020
- Multiple instances are handled by voting for object centers, finding modes among the hypotheses, then assigning pixels to the nearest voted center. (Peng et al., 2018) `ev:reported` p. 5 ^peng2018pvnet-021
- The uncertainty-driven PnP computes pose by minimizing the Mahalanobis distance between projected 3D keypoints and the estimated keypoint distributions. (Peng et al., 2018) `ev:reported` p. 5 ^peng2018pvnet-022
- Pose is initialized by EPnP on the four keypoints with smallest covariance traces, then refined with the Levenberg-Marquardt algorithm. (Peng et al., 2018) `ev:reported` p. 5 ^peng2018pvnet-023
- The network uses a pretrained ResNet-18 backbone that stops downsampling at H/8 × W/8 and uses dilated convolutions instead. (Peng et al., 2018) `ev:reported` p. 5 ^peng2018pvnet-024
- Hypothesis generation, pixel-wise voting and density estimation are implemented in CUDA, with the final pose minimized by the Ceres solver. (Peng et al., 2018) `ev:reported` p. 5 ^peng2018pvnet-025
- [[Pose ambiguity from symmetry|Symmetric objects]] are rotated to a canonical pose during training to remove ambiguities of keypoint locations, following earlier work. (Peng et al., 2018) `ev:reported` p. 5 ^peng2018pvnet-026
- Training uses a smooth ℓ1 loss on the predicted unit vectors, with a softmax cross-entropy loss for the semantic labels. (Peng et al., 2018) `ev:reported` p. 5 ^peng2018pvnet-027
- To prevent overfitting, 10000 rendered images and another 10000 Cut and Paste images per object are added to training. (Peng et al., 2018) `ev:reported` p. 5 ^peng2018pvnet-028
- Synthetic image backgrounds are randomly sampled from SUN397, with online augmentation by cropping, resizing, rotation and color jittering. (Peng et al., 2018) `ev:reported` p. 5 ^peng2018pvnet-029
- Models are trained for 200 epochs with an initial learning rate of 0.001 halved every 20 epochs. (Peng et al., 2018) `ev:reported` p. 5 ^peng2018pvnet-030
- Truncation LINEMOD is created by randomly cropping LINEMOD images, after which 40% to 60% of the target object area remains visible. (Peng et al., 2018) `ev:reported` p. 6 ^peng2018pvnet-031
- Occlusion LINEMOD and Truncation LINEMOD are used for testing, with the tested models trained solely on the LINEMOD dataset. (Peng et al., 2018) `ev:reported` p. 6 ^peng2018pvnet-032
- The 2D projection metric counts a pose correct when the mean distance between projected model points is less than 5 pixels. (Peng et al., 2018) `ev:reported` p. 6 ^peng2018pvnet-033
- [[ADD and ADD-S metrics|The ADD metric]] counts a pose correct when the mean transformed model-point distance is less than 10% of the model diameter. (Peng et al., 2018) `ev:reported` p. 6 ^peng2018pvnet-034
- On Occlusion LINEMOD, voting-based BBox 8 keypoints reach 33.88 average ADD(-S) accuracy against 6.42 for Tekin's direct coordinate regression. (Peng et al., 2018) `ev:measured` p. 6 ^peng2018pvnet-035
- Replacing bounding box corners with FPS-selected surface keypoints raised average Occlusion LINEMOD ADD(-S) accuracy from 33.88 to 39.76. (Peng et al., 2018) `ev:measured` p. 6 ^peng2018pvnet-036
- With FPS keypoints, average Occlusion LINEMOD ADD(-S) accuracy grows from 17.96 with 4 keypoints to 39.76 with 8. (Peng et al., 2018) `ev:measured` p. 6 ^peng2018pvnet-037
- Using 12 FPS keypoints gives 39.92 average accuracy, a gap to eight keypoints the authors judge negligible. (Peng et al., 2018) `ev:measured` p. 6 ^peng2018pvnet-038
- Using uncertainty-driven PnP instead of EPnP with eight FPS keypoints raised average Occlusion LINEMOD ADD(-S) accuracy from 39.76 to 40.77. (Peng et al., 2018) `ev:measured` p. 6 ^peng2018pvnet-039
- On LINEMOD, PVNet reaches 99.00 average 2D projection accuracy, against 90.37 for Tekin and 89.3 for refined BB8. (Peng et al., 2018) `ev:measured` p. 7 ^peng2018pvnet-040
- On LINEMOD, PVNet reaches 86.27 average ADD(-S) accuracy without refinement, compared with 55.95 for Tekin and 43.6 for BB8. (Peng et al., 2018) `ev:measured` p. 7 ^peng2018pvnet-041
- Compared with methods without refinement on LINEMOD, PVNet outperforms them in ADD(-S) accuracy by a margin of at least 30.32%. (Peng et al., 2018) `ev:measured` p. 7 ^peng2018pvnet-042
- PVNet without refinement still outperforms SSD-6D, which refines its pose with edge alignment, by 7.27% in LINEMOD ADD(-S) accuracy. (Peng et al., 2018) `ev:measured` p. 7 ^peng2018pvnet-043
- On Occlusion LINEMOD, PVNet reaches 40.77 average ADD(-S) accuracy, against 30.4 for Oberweger and 24.9 for PoseCNN. (Peng et al., 2018) `ev:measured` p. 7 ^peng2018pvnet-044
- On Occlusion LINEMOD, PVNet averages 61.06 in 2D projection accuracy, compared with 60.9 for Oberweger and 17.2 for PoseCNN. (Peng et al., 2018) `ev:measured` p. 7 ^peng2018pvnet-045
- On Occlusion LINEMOD 2D projection accuracy, Oberweger scores higher than PVNet on eggbox, with 13.1 against 8.43. (Peng et al., 2018) `ev:measured` p. 7 ^peng2018pvnet-046
- The authors interpret the occlusion results as showing that vector fields let PVNet learn relations between object parts to recover occluded keypoints. (Peng et al., 2018) `ev:asserted` p. 7 ^peng2018pvnet-047
- On the Truncation LINEMOD dataset of randomly cropped images, PVNet averages 58.06 accuracy under the 2D projection metric. (Peng et al., 2018) `ev:measured` p. 8 ^peng2018pvnet-048
- On Truncation LINEMOD, PVNet averages 31.48 ADD(-S) accuracy, ranging from 12.36 for duck to 44.13 for eggbox. (Peng et al., 2018) `ev:measured` p. 8 ^peng2018pvnet-049
- The released model of Tekin et al. did not obtain reasonable results on Truncation LINEMOD, as it was not designed for this case. (Peng et al., 2018) `ev:measured` p. 8 ^peng2018pvnet-050
- Failure cases on truncated images occur when visible parts are too ambiguous, a pattern particularly obvious for small objects like duck and ape. (Peng et al., 2018) `ev:measured` p. 8 ^peng2018pvnet-051
- On [[YCB-Video dataset|YCB-Video]], PVNet reaches 73.4 ADD(-S) AUC, compared with 72.8 for Oberweger and 61.0 for PoseCNN. (Peng et al., 2018) `ev:measured` p. 8 ^peng2018pvnet-052
- On YCB-Video, PVNet reaches 47.4 in 2D projection accuracy, compared with 39.4 for Oberweger and 3.72 for PoseCNN. (Peng et al., 2018) `ev:measured` p. 8 ^peng2018pvnet-053
- The PoseCNN results reported for YCB-Video in the comparison table were obtained from the paper of Oberweger et al. (Peng et al., 2018) `ev:reported` p. 8 ^peng2018pvnet-054
- On a 480 × 640 image, PVNet runs at 25 fps on a desktop with an Intel i7 3.7GHz CPU and GTX 1080 Ti GPU. (Peng et al., 2018) `ev:measured` p. 8 ^peng2018pvnet-055
- Per-image time splits into 10.9 ms data loading, 3.3 ms forward propagation, 22.8 ms voting, and 3.1 ms uncertainty-driven PnP. (Peng et al., 2018) `ev:measured` p. 8 ^peng2018pvnet-056
- The authors conclude that vector-field prediction with RANSAC voting outperforms direct keypoint regression, especially for occluded or truncated objects. (Peng et al., 2018) `ev:asserted` p. 9 ^peng2018pvnet-057
- The authors conclude that accounting for uncertainties of predicted keypoint locations when solving PnP further improved their pose estimation results. (Peng et al., 2018) `ev:asserted` p. 9 ^peng2018pvnet-058

## 🎯 Contributions


## 📖 Glossary

- **6DoF pose** — Rigid 3D rotation and translation of an object relative to the camera.
- **PnP (Perspective-n-Point)** — Solving camera-object pose from 2D-3D keypoint correspondences.
- **EPnP** — Efficient closed-form PnP solver, used here to initialize the pose.
- **Vector field (keypoint)** — Per-pixel unit vectors pointing from object pixels towards a 2D keypoint.
- **RANSAC voting** — Random pairwise vector intersections generate hypotheses scored by agreeing pixel votes.
- **Farthest point sampling (FPS)** — Iteratively picks surface points farthest from the already selected set.
- **Uncertainty-driven PnP** — PnP minimizing Mahalanobis reprojection error weighted by keypoint covariances.
- **ADD / ADD-S** — Mean 3D model-point distance under estimated vs ground-truth pose; ADD-S uses closest points.
- **2D projection metric** — Pose correct when mean projected model-point error is under 5 pixels.
- **Truncation LINEMOD** — LINEMOD images cropped so only 40–60% of the target object remains.

## ❓ Open questions

- How does PVNet behave when truncation leaves visible parts too ambiguous, as in the reported duck and ape failures?
- Would a learned or data-driven keypoint selection outperform farthest point sampling on the object surface?
- How well does the RANSAC voting stage, the largest share of runtime at 22.8 ms, scale to many objects or instances per image?
- How robust is the approach to symmetric objects beyond rotating them to a canonical pose during training?
- Does training only on LINEMOD plus synthetic images limit generalization to real scenes with different lighting or clutter statistics?

## 📝 Notes on reading

Version read: arXiv v1 (1812.11788v1, 31 Dec 2018), matching the packet identifier; the conference version may differ.

Figures 1–5 are only described (pipeline, architecture, hypothesis spread for bounding box vs surface keypoints, qualitative Occlusion and Truncation LINEMOD results); no claims rest on them.

Inconsistencies inside the paper: the contribution list gives rounded ADD numbers (86.3% vs 79%, 40.8% vs 30.4%) while Tables 3 and 5 print 86.27 and 40.77; the 79 comparison is SSD-6D with refinement, not the best non-refined method. The text for Table 3 cites [33, 26, 39] although SSD-6D is reference [20]. The text states PVNet achieves the best performance on Occlusion LINEMOD for both metrics, yet Table 4 shows Oberweger higher on ape (69.6 vs 69.14), driller (73.8 vs 73.06) and eggbox (13.1 vs 8.43), and the average margin is only 60.9 vs 61.06. In the extracted Table 3, the duck and holepuncher rows run values together but could still be read.

Equations 2–6 were partly garbled by extraction but their meaning is recoverable from surrounding text.

## Suggested new concepts

- Keypoint vector-field voting — a dense keypoint representation reused by later pose estimators; distinct from heatmaps and coordinate regression.
- Uncertainty-weighted PnP — PnP that uses per-keypoint covariances; a general technique beyond PVNet.
- Truncation LINEMOD — a benchmark variant introduced here for truncated-object pose evaluation.
- Farthest point sampling for keypoint selection — a keypoint-definition choice shown to beat bounding box corners.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Puntos clave por votación más PnP, robusto a la oclusión
