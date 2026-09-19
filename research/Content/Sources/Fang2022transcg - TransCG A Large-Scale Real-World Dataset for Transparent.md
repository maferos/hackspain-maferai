---
aliases: []
type: "source"
title: "TransCG: A Large-Scale Real-World Dataset for Transparent Object Depth Completion and a Grasping Baseline"
citekey: "Fang2022transcg"
doi: "10.48550/arXiv.2202.08471"
arxiv: "2202.08471"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2202.08471"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Hongjie Fang", "Hao-Shu Fang", "Sheng Xu", "Cewu Lu"]
sha256: ["a891405c19633d5bafa1f04661eda9ae3b5c7c896e8723aa9955fe39fecc1d9e"]
pdf: "Content/Papers/Fang2022transcg.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Fang2022transcg.pdf]]

> [!abstract] One-sentence summary
> TransCG builds a 57,715-image real-world RGB-D dataset for transparent objects with a tracker-based semi-automatic pipeline, and trains a small depth completion network (DFNet) that feeds a 6-DoF grasp detector, reaching an 80.4% grasp success rate on a real robot.

## Abstract

Transparent objects are common in our daily life and frequently handled in the automated production line. Robust vision-based robotic grasping and manipulation for these objects would be beneficial for automation. However, the majority of current grasping algorithms would fail in this case since they heavily rely on the depth image, while ordinary depth sensors usually fail to produce accurate depth information for transparent objects owing to the reflection and refraction of light. In this work, we address this issue by contributing a large-scale real-world dataset for transparent object depth completion, which contains 57,715 RGB-D images from 130 different scenes. Our dataset is the first large-scale, real-world dataset that provides ground truth depth, surface normals, transparent masks in diverse and cluttered scenes. Cross-domain experiments show that our dataset is more general and can enable better generalization ability for models. Moreover, we propose an end-to-end depth completion network, which takes the RGB image and the inaccurate depth map as inputs and outputs a refined depth map. Experiments demonstrate superior efficacy, efficiency and robustness of our method over previous works, and it is able to process images of high resolutions under limited hardware resources. Real robot experiments show that our method can also be applied to novel transparent object grasping robustly. The full dataset and our method are publicly available at www.graspnet.net/transcg (arXiv)

## 🧠 Key ideas (atomic)

- Ordinary depth sensors usually fail to construct a complete depth image in scenes that include transparent objects, according to the authors. (Fang et al., 2022) `ev:asserted` p. 1 ^fang2022transcg-001
- Many robot grasping advances heavily rely on depth from RGB-D cameras, so they are not directly applicable in scenes with transparent objects. (Fang et al., 2022) `ev:asserted` p. 1 ^fang2022transcg-002
- Polarization-based shape estimation and multi-view physical-based reconstruction of transparent objects both require specialized hardware, not a general robotic manipulation setting. (Fang et al., 2022) `ev:cited` p. 1 ^fang2022transcg-003
- The paper mainly focuses on the common setting of a robot arm equipped with an RGB-D camera. (Fang et al., 2022) `ev:asserted` p. 1 ^fang2022transcg-004
- The authors argue that the lack of real depth maps in synthetic datasets degrades the real-world performance of ClearGrasp and LIDF methods. (Fang et al., 2022) `ev:asserted` p. 2 ^fang2022transcg-005
- TransCG contains 57,715 RGB-D images of 51 transparent objects and around 200 opaque objects captured in 130 real-world scenes. (Fang et al., 2022) `ev:reported` p. 2 ^fang2022transcg-006
- The 3D mesh models of the transparent objects are also provided as part of the TransCG dataset release. (Fang et al., 2022) `ev:reported` p. 2 ^fang2022transcg-007
- The ClearGrasp real-world dataset only has 286 samples because generating the missing depth information is time-consuming and labor-consuming. (Fang et al., 2022) `ev:cited` p. 2 ^fang2022transcg-008
- The authors state that the greatest shortcoming of synthetic transparent datasets is that raw sensor information is unlikely to be obtained in simulation. (Fang et al., 2022) `ev:asserted` p. 2 ^fang2022transcg-009
- According to the authors' cross-domain tests, the generalization ability of the LIDF local implicit depth function method is very limited. (Fang et al., 2022) `ev:measured` p. 2 ^fang2022transcg-010
- The authors argue that a tiny but robust model supported by a large amount of real-world data is needed for real-world generalization. (Fang et al., 2022) `ev:asserted` p. 2 ^fang2022transcg-011
- Existing 6-DoF grasping methods rely heavily on depth images, which the authors say makes them unsuitable for transparent object grasping. (Fang et al., 2022) `ev:asserted` p. 3 ^fang2022transcg-012
- The dataset pipeline uses a robot to perform data collection after limited object-level manual annotations, to build the dataset efficiently. (Fang et al., 2022) `ev:reported` p. 3 ^fang2022transcg-013
- An optical tracker localizes the 6D pose of each transparent object in real time from several IR markers attached to it. (Fang et al., 2022) `ev:reported` p. 3 ^fang2022transcg-014
- 3D models of the training-set transparent objects are obtained by wrapping them with opaque materials and scanning them with a 3D scanner. (Fang et al., 2022) `ev:reported` p. 3 ^fang2022transcg-015
- TransCG was captured by two different cameras from 130 scenes under various background settings within a single week. (Fang et al., 2022) `ev:reported` p. 3 ^fang2022transcg-016
- The 51 collected objects include transparent, translucent and reflective objects, plus objects with dense tiny holes that can cause inaccurate depth. (Fang et al., 2022) `ev:reported` p. 3 ^fang2022transcg-017
- Besides 65 simple isolated scenes, TransCG provides 65 challenging cluttered scenes that are closer to real-world grasping environments. (Fang et al., 2022) `ev:reported` p. 3 ^fang2022transcg-018
- The authors found that attaching IR markers through a flat fixer, rather than directly to the object, can make tracking more robust. (Fang et al., 2022) `ev:reported` p. 3 ^fang2022transcg-019
- The data collection system consists of a PST optical tracker, an Intel RealSense D435 camera plus an Intel RealSense L515 camera. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022transcg-020
- Marker-to-object transformations are annotated by a human through a GUI that evaluates results in real time by rendering objects onto RGB images. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022transcg-021
- On average, the overall human effort needed to process one object for the tracking system is around 1 hour. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022transcg-022
- The tracking system is mounted on a robot arm that moves along a fixed trajectory containing 240 distinct viewpoints. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022transcg-023
- Camera extrinsic calibration of the 240 viewpoints lets object poses be recovered from a successfully tracked viewpoint when the tracker fails. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022transcg-024
- Ground-truth depth maps, transparent masks and surface normals are rendered from the collected 6D poses after raw data collection. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022transcg-025
- Blurry and improperly exposed samples are automatically removed using Laplacian operators and histograms provided in the OpenCV library. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022transcg-026
- The test set holds all scenes containing 12 randomly selected objects, giving 34,191 training samples versus 23,524 testing samples. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022transcg-027
- The authors conclude that the IR markers, placed on a fixer rather than the object surface, have minimal impact on network training. (Fang et al., 2022) `ev:asserted` p. 5 ^fang2022transcg-028
- DFNet is a U-Net with depth of four layers built from dense blocks forming CDCD, CDC and CDCU blocks. (Fang et al., 2022) `ev:reported` p. 5 ^fang2022transcg-029
- The original depth is provided as an input to every CDCD, CDC and CDCU block because empirical statistics show it is critical. (Fang et al., 2022) `ev:reported` p. 5 ^fang2022transcg-030
- DFNet uses dense up-sampling convolution instead of ordinary deconvolution layers in its CDCU blocks, inspired by AlphaPose. (Fang et al., 2022) `ev:reported` p. 5 ^fang2022transcg-031
- The training loss adds a squared depth error to a weighted cosine distance of surface normals that penalizes unsmoothness. (Fang et al., 2022) `ev:reported` p. 5 ^fang2022transcg-032
- Depths out of the range [0.3, 1.5] are treated as invalid pixels and removed from both losses to reduce outlier impact. (Fang et al., 2022) `ev:reported` p. 5 ^fang2022transcg-033
- For grasping, [[Transparent object depth completion|the refined depth from DFNet]] builds a scene point cloud that is passed to GraspNet-baseline for grasp pose detection. (Fang et al., 2022) `ev:reported` p. 5 ^fang2022transcg-034
- On the TransCG test set, DFNet reaches an RMSE of 0.018, compared with 0.019 for LIDF-Refine and 0.054 for ClearGrasp. (Fang et al., 2022) `ev:measured` p. 6 ^fang2022transcg-035
- On the TransCG test set, DFNet reaches an MAE of 0.012, compared with 0.013 for TranspareNet and 0.015 for LIDF-Refine. (Fang et al., 2022) `ev:measured` p. 6 ^fang2022transcg-036
- On the TransCG test set, TranspareNet achieves a lower REL of 0.023 than DFNet, which reaches 0.027. (Fang et al., 2022) `ev:measured` p. 6 ^fang2022transcg-037
- On the TransCG test set, TranspareNet achieves a higher δ1.05 score of 88.45 than DFNet, which reaches 83.76. (Fang et al., 2022) `ev:measured` p. 6 ^fang2022transcg-038
- DFNet has a model size of 5.2 MB, compared with 251 MB for LIDF-Refine and 934 MB for ClearGrasp. (Fang et al., 2022) `ev:measured` p. 6 ^fang2022transcg-039
- DFNet takes 0.0166s per inference on an RTX 3090 GPU, compared with 0.0182s for LIDF-Refine and 2.2813s for ClearGrasp. (Fang et al., 2022) `ev:measured` p. 6 ^fang2022transcg-040
- DFNet occupies 1.6 GB of GPU memory, less than TranspareNet at 1.9 GB and LIDF-Refine at 6.2 GB. (Fang et al., 2022) `ev:measured` p. 6 ^fang2022transcg-041
- All baselines were trained on TransCG using their released source codes and optimal hyperparameters for fair comparisons. (Fang et al., 2022) `ev:reported` p. 6 ^fang2022transcg-042
- DFNet is trained for 40 epochs with a batch size of 32 using the AdamW optimizer at initial learning rate 10−3. (Fang et al., 2022) `ev:reported` p. 6 ^fang2022transcg-043
- All compared methods scale images to 320 × 240 during both training and testing on the TransCG dataset. (Fang et al., 2022) `ev:reported` p. 6 ^fang2022transcg-044
- Unless specified, all [[Transparent object depth completion|depth completion metrics]] are calculated on the transparent areas given by the transparent masks. (Fang et al., 2022) `ev:reported` p. 6 ^fang2022transcg-045
- Though LIDF-Refine performs well on masked metrics, it may introduce shadows on areas without transparent objects, possibly from depth outliers. (Fang et al., 2022) `ev:measured` p. 6 ^fang2022transcg-046
- Trained on ClearGrasp synthetic plus Omniverse data and tested on TransCG, DFNet reaches an RMSE of 0.039, versus 0.061 for ClearGrasp. (Fang et al., 2022) `ev:measured` p. 7 ^fang2022transcg-047
- In the same synthetic-to-TransCG test, TranspareNet reaches a higher δ1.05 of 62.99 than DFNet, which reaches 56.68. (Fang et al., 2022) `ev:measured` p. 7 ^fang2022transcg-048
- Trained on TransCG and tested on ClearGrasp real-world data, DFNet reaches an RMSE of 0.041, versus 0.045 for TranspareNet. (Fang et al., 2022) `ev:measured` p. 7 ^fang2022transcg-049
- LIDF-Refine reaches an RMSE of 0.146 when trained on synthetic ClearGrasp plus Omniverse data and tested on TransCG. (Fang et al., 2022) `ev:measured` p. 7 ^fang2022transcg-050
- The authors attribute the cross-domain performance drop of LIDF-Refine to its local implicit depth function being environment-dependent. (Fang et al., 2022) `ev:asserted` p. 7 ^fang2022transcg-051
- Using DFNet on the TOD dataset with global metrics, training on TransCG gives an RMSE of 0.044 versus 0.077 for synthetic training. (Fang et al., 2022) `ev:measured` p. 7 ^fang2022transcg-052
- On ClearGrasp real-world data, DFNet trained on TransCG reaches a δ1.05 of 62.74, versus 55.08 when trained on synthetic data. (Fang et al., 2022) `ev:measured` p. 7 ^fang2022transcg-053
- On ClearGrasp real-world data, synthetic training gives DFNet a slightly lower RMSE of 0.040 than TransCG training at 0.041. (Fang et al., 2022) `ev:measured` p. 7 ^fang2022transcg-054
- The authors conclude that their real-world dataset is more universal than previous synthetic datasets for training [[Transparent object depth completion|depth completion models]]. (Fang et al., 2022) `ev:asserted` p. 7 ^fang2022transcg-055
- Real robot experiments use a UR-5 robot with an Intel RealSense D435 camera plus a Robotiq two-finger gripper. (Fang et al., 2022) `ev:reported` p. 7 ^fang2022transcg-056
- 8 transparent objects were randomly selected for robot grasping, of which 6 are completely novel objects not seen in training. (Fang et al., 2022) `ev:reported` p. 7 ^fang2022transcg-057
- Across five real robot experiments, the grasping pipeline achieved an 80.4% total success rate over 46 attempts on 37 objects. (Fang et al., 2022) `ev:measured` p. 7 ^fang2022transcg-058
- The completion rate was 100.0% in every one of the five real robot grasping experiments reported in Table V. (Fang et al., 2022) `ev:measured` p. 7 ^fang2022transcg-059
- The authors claim DFNet's compatibility with depth-based manipulation methods allows it to become a default pre-processing step for transparent objects. (Fang et al., 2022) `ev:asserted` p. 7 ^fang2022transcg-060
- According to the abstract, the DFNet method is able to process images of high resolutions under limited hardware resources. (Fang et al., 2022) `ev:abstract` p. none ^fang2022transcg-061

## 🎯 Contributions

## 📖 Glossary

- **Depth completion** — Predicting a full, accurate depth map from RGB and an incomplete or inaccurate depth map.
- **DFNet (Depth Filler Net)** — The paper's end-to-end U-Net depth completion network built from dense blocks.
- **DUC** — Dense up-sampling convolution; up-sampling via pixel shuffle instead of deconvolution layers.
- **δ threshold metric** — Percentage of pixels where max(d/d*, d*/d) stays below 1.05, 1.10 or 1.25.
- **Optical tracker** — Device tracking IR marker constellations to output an object's 6D pose in real time.
- **6-DoF grasping** — Predicting gripper position and rotation in 3D rather than a planar grasp.
- **Cross-domain experiment** — Training on one dataset and testing on another to measure generalization.

## ❓ Open questions

- Does DFNet keep its accuracy at the high input resolutions claimed in the abstract, given all experiments used 320 × 240 images?
- How much do the fixers and IR markers bias the learned depth, beyond the indirect cross-dataset argument?
- How does grasp success scale with more cluttered scenes, more novel objects, or grasp detectors other than GraspNet-baseline?
- Would the tracker-based pipeline extend to deformable or liquid-filled transparent containers?
- Why does synthetic training give slightly lower RMSE on ClearGrasp real-world data while TransCG training wins the threshold metrics?

## 📝 Notes on reading

Read the arXiv v2 preprint (accepted to IEEE RA-L, June 2022), 8 pages. Table I (p. 3) lost its checkmark columns in extraction (RGB, raw depth, refined depth, scene types, auto-collection); only the #Cam., #Obj. and #Img. columns survive, so no completeness comparisons were claimed. Equations 1, 2 and 4 are partly garbled; the loss was only described. Figures 1-6 are pipeline, architecture and qualitative figures described only in words. Inconsistencies: the abstract says DFNet processes high-resolution images, but the experiments scale all images to 320 × 240 (p. 6); the text calls DFNet's generalization superior, yet in Table III TranspareNet beats DFNet on δ1.05 and δ1.10 in the synthetic-to-TransCG test, and on δ1.25 in the TransCG-to-Clear-Real test; in Table IV synthetic training beats TransCG training on RMSE and δ1.25 on Clear-Real. Table III gives δ1.10 = 83.31 for DFNet on Clear-Real while Table IV gives 83.32 for the same setting. Page 3 says 3D models are made for the training-set objects, while the intro says models of the transparent objects are provided in general.

## Suggested new concepts

- Transparent object depth completion — a recurring task in lab-automation grasping of glassware, with several competing methods (ClearGrasp, LIDF, TranspareNet, DFNet).
- Tracker-based semi-automatic dataset annotation — using optical 6D tracking plus scanned meshes to render ground truth without per-frame labeling; reusable for lab object datasets.
- Synthetic-to-real gap for transparent objects — the paper's cross-domain results quantify it and it bears on simulation-trained perception.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Datos reales y red rápida para el *sim-to-real* de vidrio

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
