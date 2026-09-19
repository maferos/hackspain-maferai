---
aliases: []
type: "source"
title: "Vision-based robot manipulation of transparent liquid containers in a laboratory setting"
citekey: "Schober2024vision"
doi: "10.48550/arXiv.2404.16529"
arxiv: "2404.16529"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2404.16529"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Daniel Schober", "Ronja Güldenring", "James Love", "Lazaros Nalpantidis"]
sha256: ["0c3521f84272eee558d44016f60cafaa1f03420d6f0031c82ef48b048f279a28"]
pdf: "Content/Papers/Schober2024vision.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Schober2024vision.pdf]]

> [!abstract] One-sentence summary
> The paper combines a two-step CNN that estimates liquid volume in transparent lab containers from one RGB image with a simulation-selected pouring motion around a fixed liquid exit point, and uses both on a UR5e to automate cell culture workflows.

## Abstract

Laboratory processes involving small volumes of solutions and active ingredients are often performed manually due to challenges in automation, such as high initial costs, semi-structured environments and protocol variability. In this work, we develop a flexible and cost-effective approach to address this gap by introducing a vision-based system for liquid volume estimation and a simulation-driven pouring method particularly designed for containers with small openings. We evaluate both components individually, followed by an applied real-world integration of cell culture automation using a UR5 robotic arm. Our work is fully reproducible: we share our code at at \url{https://github.com/DaniSchober/LabLiquidVision} and the newly introduced dataset LabLiquidVolume is available at https://data.dtu.dk/articles/dataset/LabLiquidVision/25103102. (arXiv)

## 🧠 Key ideas (atomic)

- Experiments with small amounts of solutions and active ingredients are still mostly executed manually by specialists in the lab. (Schober et al., 2024) `ev:asserted` p. 1 ^schober2024vision-001
- The proposed liquid volume estimation method uses a two-step convolutional neural network architecture that takes a single RGB image as input. (Schober et al., 2024) `ev:reported` p. 1 ^schober2024vision-002
- The authors created the LabLiquidVolume dataset of 5,451 RGB images of transparent laboratory containers manually labeled with the contained liquid volume. (Schober et al., 2024) `ev:reported` p. 1 ^schober2024vision-003
- The authors state that the two-step design keeps the new dataset relatively small by building on knowledge from publicly available datasets. (Schober et al., 2024) `ev:asserted` p. 1 ^schober2024vision-004
- The proposed pouring strategy confines the robot arm to rotate around a fixed liquid exit point to pour into small openings. (Schober et al., 2024) `ev:reported` p. 1 ^schober2024vision-005
- From a large pool of simulated pouring trajectories, the simulation that best approximates the real-world state is executed on the robot. (Schober et al., 2024) `ev:reported` p. 1 ^schober2024vision-006
- The system is showcased on automated cell culture processes, including media changing and passaging, using exclusively existing laboratory equipment. (Schober et al., 2024) `ev:reported` p. 2 ^schober2024vision-007
- The authors state that LabLiquidVolume is, to their knowledge, the first real-world dataset with liquid volume labels in transparent containers. (Schober et al., 2024) `ev:asserted` p. 2 ^schober2024vision-008
- Mottaghi et al. framed liquid volume estimation as classification over discrete container size ranges and fill percentages from single RGB images. (Schober et al., 2024) `ev:cited` p. 2 ^schober2024vision-009
- Zhu et al. combined RGB images with a customized tactile sensor, predicting liquid volume with an error of 2 mL for 40-80 mL. (Schober et al., 2024) `ev:cited` p. 2 ^schober2024vision-010
- In laboratory settings, only the detection of materials, including liquids, in transparent containers has been heavily researched, mainly by Eppel et al. (Schober et al., 2024) `ev:cited` p. 2 ^schober2024vision-011
- The authors claim to present, to their knowledge, the first vision-based liquid volume estimation approach developed for laboratory settings. (Schober et al., 2024) `ev:asserted` p. 2 ^schober2024vision-012
- Existing robotic pouring strategies tackle pouring into wide openings, such as kitchen assistant tasks, which leads to moving liquid exit points. (Schober et al., 2024) `ev:cited` p. 2 ^schober2024vision-013
- The majority of existing robotic pouring strategies cited by the authors perform a rotation around the wrist of the robot. (Schober et al., 2024) `ev:cited` p. 2 ^schober2024vision-014
- The Segmentation and Depth Estimation network is a modified DeepLab-v3 that outputs a segmentation map and a depth map from an RGB image. (Schober et al., 2024) `ev:reported` p. 3 ^schober2024vision-015
- A constant camera setup with known parameters lets the SDE network predict a 2D depth map instead of a 3D XYZ map. (Schober et al., 2024) `ev:reported` p. 3 ^schober2024vision-016
- The segmentation map predicted by the SDE network covers three classes, namely the vessel, the vessel opening, and the liquid. (Schober et al., 2024) `ev:reported` p. 3 ^schober2024vision-017
- The Liquid Volume Estimation network is a down-sampling CNN with five convolutional layers followed by four fully connected layers. (Schober et al., 2024) `ev:reported` p. 3 ^schober2024vision-018
- Wrist-only pouring rotation is not applicable for containers with small openings such as cell culture flasks, because the liquid exit point keeps changing. (Schober et al., 2024) `ev:asserted` p. 3 ^schober2024vision-019
- The proposed pouring motion first aligns the two container openings, then rotates the pouring container around the fixed liquid exit point. (Schober et al., 2024) `ev:reported` p. 3 ^schober2024vision-020
- The authors state that pre-simulated pouring results reduce the number of time-consuming real pouring attempts needed for experimentation and adaptation. (Schober et al., 2024) `ev:asserted` p. 3 ^schober2024vision-021
- The simulation search uses a 4D parameter space of pouring container, start volume, stop angle, and stop time, with constant angular velocity. (Schober et al., 2024) `ev:reported` p. 4 ^schober2024vision-022
- The chosen simulated scene minimizes a cost summing start volume mismatch, received volume mismatch against the goal, and simulated spilled volume. (Schober et al., 2024) `ev:reported` p. 4 ^schober2024vision-023
- The real-world setup includes a UR5e arm, a CytoSMART Lux3 BR microscope, an Intel RealSense D415 camera, and a CO2 incubator. (Schober et al., 2024) `ev:reported` p. 4 ^schober2024vision-024
- The autonomous cell culture process is split into three high-level workflows: analyzing cell growth, changing media, and passaging. (Schober et al., 2024) `ev:reported` p. 4 ^schober2024vision-025
- Trypsin needs only about 0.5 mL per 10 cm2, so a 1-10 mL bottle dispenser replaces pouring for adding it to flasks. (Schober et al., 2024) `ev:reported` p. 4 ^schober2024vision-026
- Pouring movements were simulated with the particle-based NVIDIA Flex library, in one scene for a cell culture flask and one for a media bottle. (Schober et al., 2024) `ev:reported` p. 4 ^schober2024vision-027
- In total, 6,805 pouring movements were simulated to form the pool from which real-world pours are selected. (Schober et al., 2024) `ev:reported` p. 4 ^schober2024vision-028
- The TransProteus dataset consists of more than 50,000 synthetic images of transparent vessels with annotated 3D models of vessels and content. (Schober et al., 2024) `ev:cited` p. 4 ^schober2024vision-029
- From TransProteus, only transparent vessels containing liquid material were used for this work, which constitutes ≈14,500 samples. (Schober et al., 2024) `ev:reported` p. 5 ^schober2024vision-030
- The Vector-LabPics dataset comprises 7,900 real-world images with pixel-wise annotation of vessels and the material they contain. (Schober et al., 2024) `ev:cited` p. 5 ^schober2024vision-031
- LabLiquidVolume images were taken with an Intel RealSense D415 camera in automation and research laboratories at a Novo Nordisk site. (Schober et al., 2024) `ev:reported` p. 5 ^schober2024vision-032
- Ground-truth liquid volumes were measured with a Mettler Toledo XSR2002S balance with an accuracy of ± 0.5 mL. (Schober et al., 2024) `ev:reported` p. 5 ^schober2024vision-033
- LabLiquidVolume covers twelve common research laboratory containers, with liquid volumes of 3 - 600 mL and camera distances of 50 - 600 mm. (Schober et al., 2024) `ev:reported` p. 5 ^schober2024vision-034
- All LabLiquidVolume images were taken from above the container so that the surface of the liquid is visible to the camera. (Schober et al., 2024) `ev:reported` p. 5 ^schober2024vision-035
- During SDE training, Vector-LabPics images were sampled with 33%, with depth loss set to zero since no depth ground truth exists. (Schober et al., 2024) `ev:reported` p. 5 ^schober2024vision-036
- The SDE network was trained for 75 epochs on TransProteus and Vector-LabPics with an Adam optimizer and a batch size of 6. (Schober et al., 2024) `ev:reported` p. 5 ^schober2024vision-037
- Each LVE network variant was trained on 80% of LabLiquidVolume for 200 epochs using a mean squared error loss. (Schober et al., 2024) `ev:reported` p. 5 ^schober2024vision-038
- Three LVE input variants were compared: segmented depth maps, segmented depth maps with vessel volume, and segmentation masks only. (Schober et al., 2024) `ev:reported` p. 5 ^schober2024vision-039
- On the TransProteus test subset, the SDE model achieved a mean IoU of 0.92 for segmentation of vessel, opening, and liquid. (Schober et al., 2024) `ev:measured` p. 5 ^schober2024vision-040
- The SDE model reached a scale-invariant log RMSE of 0.031 for depth estimation on the TransProteus test subset. (Schober et al., 2024) `ev:measured` p. 5 ^schober2024vision-041
- On 120 manually annotated real LabLiquidVolume images, SDE segmentation performance dropped to a mean IoU of 0.90. (Schober et al., 2024) `ev:measured` p. 5 ^schober2024vision-042
- Liquid segmentation reached an IoU of 91.3% inside glass vessels but a significantly lower 84.3% inside plastic objects. (Schober et al., 2024) `ev:measured` p. 5 ^schober2024vision-043
- Segmented depth maps with vessel volume gave the best LVE results, with a testing RMSE of 17.83 mL and R2 of 0.99. (Schober et al., 2024) `ev:measured` p. 6 ^schober2024vision-044
- Using segmented depth maps alone, the LVE model reached a testing RMSE of 37.90 mL and a testing R2 of 0.94. (Schober et al., 2024) `ev:measured` p. 6 ^schober2024vision-045
- Relying only on segmentation masks gave the weakest LVE results, with a testing RMSE of 53.92 mL and R2 of 0.88. (Schober et al., 2024) `ev:measured` p. 6 ^schober2024vision-046
- The depth-only LVE variant was kept for later experiments because it allows manipulating vessels of unknown volume and is more flexible. (Schober et al., 2024) `ev:asserted` p. 6 ^schober2024vision-047
- A moderate negative correlation coefficient of -0.69 was found between liquid segmentation IoU and the MAPE of volume estimation. (Schober et al., 2024) `ev:measured` p. 6 ^schober2024vision-048
- For cell culture flask pours, simulated minimum costs across 9,750 start and target volume combinations ranged from 0.05 mL to 16.5 mL. (Schober et al., 2024) `ev:computed` p. 6 ^schober2024vision-049
- The mean minimum cost over all simulated cell culture flask start and target volume combinations was 2.3 mL. (Schober et al., 2024) `ev:computed` p. 6 ^schober2024vision-050
- For start volumes below 100 mL, the simulated cost stayed smaller than 7.5 mL for every possible target volume. (Schober et al., 2024) `ev:computed` p. 6 ^schober2024vision-051
- For target volumes below 105 mL, a simulated cell culture flask pour can be found without any spilled liquid. (Schober et al., 2024) `ev:computed` p. 6 ^schober2024vision-052
- In the cell culture flask simulations, the spilled volume increases for higher stop angles and for higher received volumes. (Schober et al., 2024) `ev:computed` p. 6 ^schober2024vision-053
- In simulation, stop angle variation drives the coarse differences in poured volume, whereas stop time variation gives more subtle differences. (Schober et al., 2024) `ev:computed` p. 6 ^schober2024vision-054
- Across 50 simulated pours executed in reality with the cell culture flask, the RMSE was 10.8 mL with a MAPE of 21%. (Schober et al., 2024) `ev:measured` p. 6 ^schober2024vision-055
- The largest cell culture flask sim-to-real differences occurred for ratios of target to start volume between 0.3 and 0.7. (Schober et al., 2024) `ev:measured` p. 7 ^schober2024vision-056
- For the media bottle, sim-to-real pouring gave an RMSE of 29.2 mL, a MAPE of 52%, and a maximum difference of 52.6 mL. (Schober et al., 2024) `ev:measured` p. 7 ^schober2024vision-057
- For both containers, real pours into a small opening spilled on average less than 1 mL of liquid. (Schober et al., 2024) `ev:measured` p. 7 ^schober2024vision-058
- In 35 of the flask pours, the real spilled volume was lower than the simulated prediction, with a mean difference of 2.1 mL. (Schober et al., 2024) `ev:measured` p. 7 ^schober2024vision-059
- In the remaining 15 flask pours, the real spilled volume exceeded the simulated one, with a maximum difference of 2.4 mL. (Schober et al., 2024) `ev:measured` p. 7 ^schober2024vision-060
- The full autonomous pouring workflow with a 30 mL target gave an RMSE of 21.4 mL and a MAPE of 71.3%. (Schober et al., 2024) `ev:measured` p. 7 ^schober2024vision-061
- For a 50 mL target, the full autonomous pouring workflow gave an RMSE of 26.2 mL and a maximum error of 44.8 mL. (Schober et al., 2024) `ev:measured` p. 7 ^schober2024vision-062
- The full pouring workflow tests used random start volumes from 100 mL to 500 mL, with 20 trials per target volume. (Schober et al., 2024) `ev:reported` p. 7 ^schober2024vision-063
- The passaging workflow achieved a 90% completion rate over ten runs, with an average execution time of 841.2 s. (Schober et al., 2024) `ev:measured` p. 7 ^schober2024vision-064
- The analyzing cell growth and changing media workflows each completed all ten runs, averaging 78.3 s and 461.4 s respectively. (Schober et al., 2024) `ev:measured` p. 7 ^schober2024vision-065
- The authors argue that pouring instead of pipetting reduces the amount of disposable plastics used in the automated laboratory process. (Schober et al., 2024) `ev:asserted` p. 7 ^schober2024vision-066
- The authors conclude that incorporating depth maps alongside segmentation masks significantly enhances the performance of the liquid volume estimation model. (Schober et al., 2024) `ev:asserted` p. 8 ^schober2024vision-067
- The authors state that the setup is not suitable for precise laboratory experiments since the volume estimation and pouring simulation errors add up. (Schober et al., 2024) `ev:asserted` p. 8 ^schober2024vision-068
- The authors suggest that improving the accuracy of both elements could enable flexible automation of many research laboratory tasks. (Schober et al., 2024) `ev:asserted` p. 8 ^schober2024vision-069

## 🎯 Contributions

## 📖 Glossary

- **SDE network** — Segmentation and Depth Estimation network predicting vessel, opening and liquid masks plus depth.
- **LVE network** — Liquid Volume Estimation CNN regressing liquid volume in mL from SDE outputs.
- **Liquid exit point** — Point on the pouring container's opening where liquid leaves; used as center of rotation.
- **TCP** — Tool center point of the robot end effector.
- **Passaging** — Splitting a cell culture into new flasks to keep cells growing.
- **Scale-invariant log RMSE** — Depth error metric by Eigen et al. that ignores global scale.
- **MAPE** — Mean absolute percentage error between predicted and true values.

## ❓ Open questions

- How much would closed-loop visual feedback during pouring reduce the 21-71% MAPE of the open-loop full workflow?
- Does the LVE model generalize to containers outside the twelve types in LabLiquidVolume or to side-view cameras?
- Can the glass-versus-plastic segmentation gap be closed with more real plastic-vessel training data?
- Why does the media bottle transfer from simulation to reality so much worse than the cell culture flask?
- Which of the two error sources, volume estimation or simulated pouring, dominates the end-to-end error?

## 📝 Notes on reading

Read the arXiv preprint v1 (2404.16529, 25 Apr 2024), matching the packet identifier. The pouring kinematics (TCP coordinates as a function of pouring angle, with l, β, α and αstart) are given as equations on p. 3 and were not claimed. Figures 1-13 (architecture, pouring geometry, simulation scene, cost map, spill plots, sim-to-real scatter) could only be described from captions. Table I also lists training RMSE (13.00, 4.63, 32.94 mL) and testing MAPE per variant; only headline test values were claimed. Table II also gives average execution times (135.3 s and 124.8 s) for the 30 and 50 mL targets. The abstract says UR5 while the setup section and tables use UR5e. The dataset is named LabLiquidVolume in the text but the download URL uses LabLiquidVision. p. 5 prints the Novo Nordisk site as R&eD, likely an extraction or typesetting artifact.

## Suggested new concepts

- Liquid volume estimation from images — a recurring vision task for lab automation with distinct datasets and metrics.
- Simulation-selected robotic pouring — picking a pre-simulated trajectory by a cost function is a reusable sim-to-real pattern.
- Transparent vessel segmentation — TransProteus and Vector-LabPics underpin several lab-vision works.
- Cell culture automation — a target application with defined workflows (media change, passaging) for lab robots.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H7.** Estima el volumen de líquido por visión y vierte guiado por simulación con un UR5 en un laboratorio real, con el dataset LabLiquidVolume.
