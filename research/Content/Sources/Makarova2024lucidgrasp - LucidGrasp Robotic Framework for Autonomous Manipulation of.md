---
aliases: []
type: "source"
title: "LucidGrasp: Robotic Framework for Autonomous Manipulation of Laboratory Equipment with Different Degrees of Transparency via 6D Pose Estimation"
citekey: "Makarova2024lucidgrasp"
doi: "10.48550/arXiv.2410.07801"
arxiv: "2410.07801"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2410.07801"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Maria Makarova", "Daria Trinitatova", "Qian Liu", "Dzmitry Tsetserukou"]
sha256: ["128d8b3239171b1e4d7bd37630cfa1fb49673011d464616b2c1e915433d698f8"]
pdf: "Content/Papers/Makarova2024lucidgrasp.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 70
---

📄 PDF: [[Makarova2024lucidgrasp.pdf]]

> [!abstract] One-sentence summary
> LucidGrasp couples depth-based 6D pose estimation (OVE6D), liquid and vessel-neck segmentation, and a Unity digital twin with MoveIt! planning to let a UR3 arm autonomously manipulate transparent laboratory glassware, reaching sub-centimetre and around one-degree pose errors and completing a pipette dispensing demo.

## Abstract

Many modern robotic systems operate autonomously, however they often lack the ability to accurately analyze the environment and adapt to changing external conditions, while teleoperation systems often require special operator skills. In the field of laboratory automation, the number of automated processes is growing, however such systems are usually developed to perform specific tasks. In addition, many of the objects used in this field are transparent, making it difficult to analyze them using visual channels. The contributions of this work include the development of a robotic framework with autonomous mode for manipulating liquid-filled objects with different degrees of transparency in complex pose combinations. The conducted experiments demonstrated the robustness of the designed visual perception system to accurately estimate object poses for autonomous manipulation, and confirmed the performance of the algorithms in dexterous operations such as liquid dispensing. The proposed robotic framework can be applied for laboratory automation, since it allows solving the problem of performing non-trivial manipulation tasks with the analysis of object poses of varying degrees of transparency and liquid levels, requiring high accuracy and repeatability. (arXiv)

## 🧠 Key ideas (atomic)

- Automated platforms for solubility determination and crystallization by Fakhruldeen et al. require clearly defined instructions from the operator. (Makarova et al., 2024) `ev:cited` p. 1 ^makarova2024lucidgrasp-001
- The authors state that existing vision-based laboratory automation systems mostly focus on a specific task, such as picking test tubes. (Makarova et al., 2024) `ev:cited` p. 1 ^makarova2024lucidgrasp-002
- Shared-control studies showed that operators preferred not to interfere with autonomous robot control as task complexity increased. (Makarova et al., 2024) `ev:cited` p. 1 ^makarova2024lucidgrasp-003
- The authors argue that closed-loop robot control requires high-precision perception of the environment and preliminary action verification with a digital twin. (Makarova et al., 2024) `ev:asserted` p. 1 ^makarova2024lucidgrasp-004
- Transparent and translucent objects common in laboratories complicate processing with conventional computer vision algorithms, according to the authors. (Makarova et al., 2024) `ev:asserted` p. 2 ^makarova2024lucidgrasp-005
- The authors present a robotic framework for autonomous real-time dexterous manipulation of laboratory equipment with different degrees of transparency. (Makarova et al., 2024) `ev:asserted` p. 2 ^makarova2024lucidgrasp-006
- The framework analyzes the remote environment by predicting 6D poses of objects with different degrees of transparency. (Makarova et al., 2024) `ev:reported` p. 2 ^makarova2024lucidgrasp-007
- The system also analyzes the liquid level in transparent vessels and the geometric location of the vessel neck. (Makarova et al., 2024) `ev:reported` p. 2 ^makarova2024lucidgrasp-008
- According to the authors, the speed and gripping force of the dispenser can also be varied within the framework. (Makarova et al., 2024) `ev:asserted` p. 2 ^makarova2024lucidgrasp-009
- The framework comprises a Visual Perception Module and a Decision-Making and Execution Module that interact with the real environment. (Makarova et al., 2024) `ev:reported` p. 2 ^makarova2024lucidgrasp-010
- The real environment contains a Universal Robots UR3 manipulator equipped with a Robotiq 2F-85 two-finger gripper. (Makarova et al., 2024) `ev:reported` p. 2 ^makarova2024lucidgrasp-011
- RGB and depth images of the robot's environment are captured by a RealSense D435 camera. (Makarova et al., 2024) `ev:reported` p. 2 ^makarova2024lucidgrasp-012
- Joint positions and gripper commands are transferred from the digital twin to the real UR3 robot via ROS. (Makarova et al., 2024) `ev:reported` p. 2 ^makarova2024lucidgrasp-013
- The Trajectory Planning, Trajectory Transfer and Simulated Environment components are implemented using the Unity engine. (Makarova et al., 2024) `ev:reported` p. 2 ^makarova2024lucidgrasp-014
- The RGB image is used to predict object segmentation masks as well as liquid and vessel shapes. (Makarova et al., 2024) `ev:reported` p. 2 ^makarova2024lucidgrasp-015
- Depth images combined with segmentation masks are used to obtain the 6D poses of objects. (Makarova et al., 2024) `ev:reported` p. 2 ^makarova2024lucidgrasp-016
- DenseFusion builds a single model for multiple objects but requires expensive re-training whenever a new object instance is added. (Makarova et al., 2024) `ev:cited` p. 2 ^makarova2024lucidgrasp-017
- The authors note that LatentFusion is computationally expensive since it relies on iterative optimization at inference time. (Makarova et al., 2024) `ev:cited` p. 2 ^makarova2024lucidgrasp-018
- 6D pose estimation uses the OVE6D architecture applied to a single depth image and the object segmentation mask. (Makarova et al., 2024) `ev:reported` p. 2 ^makarova2024lucidgrasp-019
- The authors state that OVE6D generalizes to new objects without any re-training of model parameters. (Makarova et al., 2024) `ev:cited` p. 3 ^makarova2024lucidgrasp-020
- OVE6D uses object viewpoints computed by its renderer from 3D mesh models preloaded into the neural network. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-021
- No additional training of the OVE6D architecture on the custom dataset was required at this stage of development. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-022
- The target objects are 7 laboratory items: a test tube, pipette, glass beaker, volumetric flask, graduated cylinder and two tube racks. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-023
- The authors state that transparency makes 6D pose recognition from RGB and depth images more challenging than for opaque objects. (Makarova et al., 2024) `ev:asserted` p. 3 ^makarova2024lucidgrasp-024
- Segmentation masks fed to OVE6D were produced by Mask R-CNN trained on a collected dataset of 2500 images. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-025
- The segmentation dataset was collected with an Intel RealSense D435 camera in the format of the LINEMOD benchmark. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-026
- ARUCO markers were only needed during the data collection phase and are not used in the framework algorithms. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-027
- The authors plan to eliminate the need to train segmentation models in future work, for example by using Vision Language Models. (Makarova et al., 2024) `ev:asserted` p. 3 ^makarova2024lucidgrasp-028
- Estimated poses are recalculated to a coordinate reference point at the robot base before transfer to the simulation via TCP/IP. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-029
- Liquid shape and vessel neck prediction follows Eppel et al., using a fully convolutional network with an ASPP decoder and Resnet101 encoder. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-030
- The final layer of the liquid network predicts vessel, vessel content and vessel neck maps from the RGB image. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-031
- Like OVE6D, the liquid and vessel neck model required no additional training on the custom dataset. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-032
- The digital twin executes planned commands in simulation with rendered objects, allowing algorithms to be validated before real robot execution. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-033
- The digital twin trajectory is planned with the MoveIt! server based on the location of the objects and the type of task. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-034
- For object picking, the planner computes only a few key robot poses: Pre-Grab, Grab, Pick, Place and PostPlace. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-035
- The Trajectory Transfer Submodule operates in real time by simultaneously running several ROS servers with task-specific message types. (Makarova et al., 2024) `ev:reported` p. 3 ^makarova2024lucidgrasp-036
- In the camera-height experiment, the camera was placed 9.5 cm horizontally from the board edge at heights of 50, 45 and 40 cm. (Makarova et al., 2024) `ev:reported` p. 4 ^makarova2024lucidgrasp-037
- At each camera height, the camera pitch angle was varied three times between 40◦ and 65◦ in 5◦ increments. (Makarova et al., 2024) `ev:reported` p. 4 ^makarova2024lucidgrasp-038
- A Kruskal-Wallis test found a statistically significant difference in position recognition accuracy between the target objects (H = 32.1, p < .001). (Makarova et al., 2024) `ev:measured` p. 4 ^makarova2024lucidgrasp-039
- Position recognition was most unstable for large transparent and translucent objects such as the flask, glass beaker and graduated cylinder. (Makarova et al., 2024) `ev:measured` p. 4 ^makarova2024lucidgrasp-040
- Smaller translucent objects such as pipette and test tube had significantly better position recognition than larger ones (Mann-Whitney U, p = .001). (Makarova et al., 2024) `ev:measured` p. 4 ^makarova2024lucidgrasp-041
- The authors suggest that the distance from the camera to the objects should be increased for stability. (Makarova et al., 2024) `ev:asserted` p. 4 ^makarova2024lucidgrasp-042
- The largest rotation error variation was observed for asymmetric objects such as the two tube racks. (Makarova et al., 2024) `ev:measured` p. 4 ^makarova2024lucidgrasp-043
- At 40 cm camera height, the mean position error averaged over all objects was 0.3 cm (SD=0.52 cm). (Makarova et al., 2024) `ev:measured` p. 4 ^makarova2024lucidgrasp-044
- At 40 cm camera height, the mean rotation error averaged over all objects was 0.54◦ (SD=1.6◦). (Makarova et al., 2024) `ev:measured` p. 4 ^makarova2024lucidgrasp-045
- With a fixed camera height, object poses were analyzed at camera distances of 9.5, 13, 24, 33, 57, 65 and 74 cm. (Makarova et al., 2024) `ev:reported` p. 4 ^makarova2024lucidgrasp-046
- A Kruskal-Wallis test found no statistically significant difference in pose errors averaged over all objects across camera distances. (Makarova et al., 2024) `ev:measured` p. 4 ^makarova2024lucidgrasp-047
- In the distance experiment, the mean absolute position error averaged over all objects was 0.18 cm. (Makarova et al., 2024) `ev:measured` p. 4 ^makarova2024lucidgrasp-048
- In the distance experiment, the mean absolute rotation error averaged over all objects was 0.39◦. (Makarova et al., 2024) `ev:measured` p. 4 ^makarova2024lucidgrasp-049
- At close distances, the glass beaker made the main contribution to X-axis position error and roll angle error. (Makarova et al., 2024) `ev:measured` p. 4 ^makarova2024lucidgrasp-050
- Mann-Whitney U tests found no significant difference between translucent and opaque objects for position (p = .52) or rotation (p = .56). (Makarova et al., 2024) `ev:measured` p. 4 ^makarova2024lucidgrasp-051
- The authors conclude that recognition of translucent objects was as reliable as recognition of the opaque ones. (Makarova et al., 2024) `ev:asserted` p. 4 ^makarova2024lucidgrasp-052
- The pose estimation algorithm showed the best results when the camera was located at a medium distance from the objects. (Makarova et al., 2024) `ev:measured` p. 5 ^makarova2024lucidgrasp-053
- The authors advise that the working area should be determined experimentally when adapting the pose estimation algorithm to another system. (Makarova et al., 2024) `ev:asserted` p. 5 ^makarova2024lucidgrasp-054
- Complex scenes included objects stacked up to four levels high, transparent objects on varied backgrounds, and one transparent object inside another. (Makarova et al., 2024) `ev:reported` p. 5 ^makarova2024lucidgrasp-055
- The algorithm successfully coped with pose detection cases where both transparent and opaque objects were partially occluded. (Makarova et al., 2024) `ev:measured` p. 5 ^makarova2024lucidgrasp-056
- For complex object combinations, only rotation errors were analyzed since the authors found position errors insignificant. (Makarova et al., 2024) `ev:reported` p. 5 ^makarova2024lucidgrasp-057
- Main detection problems occurred when tube racks were occluded by more than 60% of the observed surface. (Makarova et al., 2024) `ev:measured` p. 5 ^makarova2024lucidgrasp-058
- Detection problems also occurred when the bottom of the glass beaker, a vessel with parallel walls, was occluded. (Makarova et al., 2024) `ev:measured` p. 5 ^makarova2024lucidgrasp-059
- In complex combinations, mean roll, pitch and yaw errors were 0.6◦ (SD = 1.1◦), 1.1◦ (SD = 3.6◦) and 0.5◦ (SD = 1.5◦). (Makarova et al., 2024) `ev:measured` p. 5 ^makarova2024lucidgrasp-060
- The authors state that accuracy can be improved through fine-tuning the OVE6D model on their own dataset. (Makarova et al., 2024) `ev:asserted` p. 5 ^makarova2024lucidgrasp-061
- The dispensing task required grasping a tilted pipette, drawing liquid from a glass beaker and pouring it into a flask. (Makarova et al., 2024) `ev:reported` p. 5 ^makarova2024lucidgrasp-062
- The liquid in the glass beaker was painted after recognition for better visualization in the demonstration. (Makarova et al., 2024) `ev:reported` p. 5 ^makarova2024lucidgrasp-063
- Six key trajectory points for the dispensing task were algorithmically calculated from the recognized object poses. (Makarova et al., 2024) `ev:reported` p. 5 ^makarova2024lucidgrasp-064
- In the liquid dispensing demonstration, all operations were performed accurately and without collisions with other objects. (Makarova et al., 2024) `ev:measured` p. 6 ^makarova2024lucidgrasp-065
- Collision avoidance relied on algorithmically determined safe lifting positions over each object and dead zones around non-manipulated objects. (Makarova et al., 2024) `ev:reported` p. 6 ^makarova2024lucidgrasp-066
- The conclusions report an average position accuracy of 0.18 cm for complex object combinations in the algorithm working area. (Makarova et al., 2024) `ev:asserted` p. 6 ^makarova2024lucidgrasp-067
- The conclusions report a rotation accuracy of about 0.7◦ for complex object combinations in the algorithm working area. (Makarova et al., 2024) `ev:asserted` p. 6 ^makarova2024lucidgrasp-068
- Future work plans to use tactile sensors on the gripper to control gripping force more precisely when handling fragile objects. (Makarova et al., 2024) `ev:asserted` p. 6 ^makarova2024lucidgrasp-069
- The authors believe the system may be essential in automated chemical experiments and in medical analysis. (Makarova et al., 2024) `ev:asserted` p. 6 ^makarova2024lucidgrasp-070

## 🎯 Contributions

## 📖 Glossary

- **6D pose** — An object's 3D position plus 3D orientation relative to a reference frame.
- **OVE6D** — Depth-based 6D pose estimator using object viewpoint encoding; generalizes to unseen meshes without retraining.
- **Digital twin** — Simulated replica of the robot and scene used to validate trajectories before execution.
- **MoveIt!** — ROS motion-planning framework used to compute robot trajectories between key poses.
- **Mask R-CNN** — Instance segmentation network producing per-object masks from RGB images.
- **LINEMOD format** — BOP benchmark dataset layout with RGB, depth, masks and 3D object meshes.
- **ASPP** — Atrous spatial pyramid pooling; dilated convolutions capturing multi-scale context in segmentation decoders.
- **Vessel neck** — Upper opening region of a container, localized to plan pouring and insertion.
- **Dead zone** — Region around a non-manipulated object that the planned trajectory must avoid.

## ❓ Open questions

- How much would fine-tuning OVE6D on the custom laboratory dataset reduce pose errors, particularly for the glass beaker and tube racks?
- How accurate is the liquid level and vessel neck prediction? The paper reports no quantitative evaluation of that network.
- How often does the full dispensing pipeline succeed over repeated trials? Only a single demonstration is described.
- Can Vision Language Models replace the trained Mask R-CNN segmentation without loss of pose accuracy?
- How does the system handle objects without available 3D mesh models, which OVE6D requires?
- Does tactile feedback on the gripper improve handling of fragile glassware as planned?

## 📝 Notes on reading

- Version read: arXiv 2410.07801v3 (31 Oct 2024), a preprint.
- Figures 4, 5 and 7 (per-object position and rotation error plots) could only be described; their per-object values are not claimed.
- Inconsistency: the distance experiment says six distance markers but lists seven values (9.5, 13, 24, 33, 57, 65 and 74 cm).
- Inconsistency: the conclusions attribute 0.18 cm position accuracy to complex object combinations, but 0.18 cm is the mean from the distance experiment; the complex-combination experiment analyzed only rotation errors.
- The conclusion's about 0.7 degree rotation figure matches the mean of the reported roll, pitch and yaw errors (0.6, 1.1, 0.5).
- The first experiment motivates itself by errors increasing at shorter distance, yet the distance experiment found no statistically significant difference across distances; the text also says best results were at a medium distance.
- The pitch sweep is described as varied three times between 40 and 65 degrees in 5 degree increments, which is ambiguous (that range holds six steps).
- The Decision-Making and Execution Module lists a Trajectory Generation submodule, later called the Trajectory Planning Submodule.
- The degree sign is extracted as ◦ in the cached text; numbers are copied as extracted.

## Suggested new concepts

- Transparent object pose estimation — recurring challenge for laboratory robotics vision; this paper uses depth-only OVE6D with masks.
- Digital twin validation of robot trajectories — pattern of simulating planned actions in Unity before real execution.
- Liquid level and vessel segmentation — perception of liquid content in transparent containers for dispensing tasks.
- Key-point task formation — generating manipulation tasks from a few algorithmically computed key poses plus a motion planner.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Manipulación de material de laboratorio transparente con pose 6D
