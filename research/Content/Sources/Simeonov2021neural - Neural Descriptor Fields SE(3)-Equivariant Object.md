---
aliases: []
type: "source"
title: "Neural Descriptor Fields: SE(3)-Equivariant Object Representations for Manipulation"
citekey: "Simeonov2021neural"
doi: "10.48550/arXiv.2112.05124"
arxiv: "2112.05124"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2112.05124"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Anthony Simeonov", "Yilun Du", "Andrea Tagliasacchi", "Joshua B. Tenenbaum", "Alberto Rodriguez", "Pulkit Agrawal", "Vincent Sitzmann"]
sha256: ["aee9e41933d196ffcc80c70510f13636ce32426886626e84be863c6a63955de9"]
pdf: "Content/Papers/Simeonov2021neural.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Simeonov2021neural.pdf]]

> [!abstract] One-sentence summary
> Neural Descriptor Fields turn occupancy-network activations into SE(3)-equivariant point and pose descriptors, so a robot can repeat a pick-and-place task on new object instances in new poses from about ten demonstrations.

## Abstract

We present Neural Descriptor Fields (NDFs), an object representation that encodes both points and relative poses between an object and a target (such as a robot gripper or a rack used for hanging) via category-level descriptors. We employ this representation for object manipulation, where given a task demonstration, we want to repeat the same task on a new object instance from the same category. We propose to achieve this objective by searching (via optimization) for the pose whose descriptor matches that observed in the demonstration. NDFs are conveniently trained in a self-supervised fashion via a 3D auto-encoding task that does not rely on expert-labeled keypoints. Further, NDFs are SE(3)-equivariant, guaranteeing performance that generalizes across all possible 3D object translations and rotations. We demonstrate learning of manipulation tasks from few (5-10) demonstrations both in simulation and on a real robot. Our performance generalizes across both object instances and 6-DoF object poses, and significantly outperforms a recent baseline that relies on 2D descriptors. Project website: https://yilundu.github.io/ndf/. (arXiv)

## 🧠 Key ideas (atomic)

- Current learning-from-demonstration systems would require many demonstrations spanning initial positions, orientations and mug instances to place novel mugs from any pose. (Simeonov et al., 2021) `ev:asserted` p. 1 ^simeonov2021neural-001
- The authors aim to build a robotic system that learns pick-and-place tasks for unseen objects from just a few demonstrations, about five to ten. (Simeonov et al., 2021) `ev:asserted` p. 1 ^simeonov2021neural-002
- Prior keypoint approaches hand-label large datasets of task-specific keypoints and train networks to predict their locations on new instances. (Simeonov et al., 2021) `ev:cited` p. 2 ^simeonov2021neural-003
- According to the authors, prior keypoint-prediction methods fail to generalize to new instances in the regime of few demonstrations. (Simeonov et al., 2021) `ev:cited` p. 2 ^simeonov2021neural-004
- The authors argue that in 2D correspondence methods keypoints may only lie on the object surface, hindering encoding of free-space locations. (Simeonov et al., 2021) `ev:asserted` p. 2 ^simeonov2021neural-005
- Existing 2D correspondence methods are not SE(3)-equivariant, so they are not guaranteed to give correct correspondence for instances in unseen poses. (Simeonov et al., 2021) `ev:asserted` p. 2 ^simeonov2021neural-006
- NDFs represent an object point cloud as a continuous function mapping any 3D coordinate to a spatial descriptor. (Simeonov et al., 2021) `ev:asserted` p. 2 ^simeonov2021neural-007
- In NDFs, query coordinates are not constrained to lie on the object and can potentially be occluded. (Simeonov et al., 2021) `ev:asserted` p. 2 ^simeonov2021neural-008
- A local coordinate frame is represented by a rigid set of query points whose configuration is an SE(3) pose relative to a canonical pose. (Simeonov et al., 2021) `ev:asserted` p. 2 ^simeonov2021neural-009
- The method solves feature matching and coordinate-frame pose jointly, which the authors argue is less error-prone than prior two-step processes. (Simeonov et al., 2021) `ev:asserted` p. 2 ^simeonov2021neural-010
- The authors devise a procedure that obtains query points from demonstrations, removing the need for human-annotated keypoints. (Simeonov et al., 2021) `ev:asserted` p. 2 ^simeonov2021neural-011
- On three pick-and-place tasks, NDFs achieved an overall success rate above 85% on unseen instances in out-of-distribution configurations with 10 demonstrations. (Simeonov et al., 2021) `ev:measured` p. 2 ^simeonov2021neural-012
- The point descriptor field is parameterized as the concatenation of layer-wise activations of an occupancy network conditioned on a point-cloud encoding. (Simeonov et al., 2021) `ev:asserted` p. 3 ^simeonov2021neural-013
- Latent shape codes come from a PointNet-based point cloud encoder that takes the object point cloud as input. (Simeonov et al., 2021) `ev:reported` p. 3 ^simeonov2021neural-014
- The occupancy model is trained to predict the occupancy of a complete 3D object from a partial point cloud. (Simeonov et al., 2021) `ev:reported` p. 3 ^simeonov2021neural-015
- The authors argue that category-level 3D reconstruction trains the occupancy network into a hierarchical, coarse-to-fine feature extractor. (Simeonov et al., 2021) `ev:asserted` p. 3 ^simeonov2021neural-016
- Prior work used occupancy-network activations to classify which semantic part of an object a given coordinate belongs to. (Simeonov et al., 2021) `ev:cited` p. 3 ^simeonov2021neural-017
- Translation equivariance is implemented by subtracting the point cloud's center of mass from both the input cloud and query coordinate. (Simeonov et al., 2021) `ev:reported` p. 4 ^simeonov2021neural-018
- Rotation equivariance is obtained with [[Vector Neurons]], an architecture giving the occupancy network full SO(3) equivariance. (Simeonov et al., 2021) `ev:reported` p. 4 ^simeonov2021neural-019
- Combining mean-centering with [[Vector Neurons]] yields complete SE(3) equivariance, which the authors state guarantees generalization to object poses unobserved during training. (Simeonov et al., 2021) `ev:asserted` p. 4 ^simeonov2021neural-020
- In energy-field visualizations, the minimizer for a handle reference point corresponded to handle points across different mug instances and poses. (Simeonov et al., 2021) `ev:measured` p. 4 ^simeonov2021neural-021
- Demonstrations consist of a point cloud and the world-frame pose of a nearby rigid body such as a gripper, rack or shelf. (Simeonov et al., 2021) `ev:reported` p. 4 ^simeonov2021neural-022
- A reference frame can be attached to three or more non-collinear points moving rigidly together, giving a one-to-one mapping to the frame. (Simeonov et al., 2021) `ev:asserted` p. 4 ^simeonov2021neural-023
- A Neural Pose Descriptor Field concatenates the point descriptors of a query point cloud transformed by an SE(3) pose. (Simeonov et al., 2021) `ev:asserted` p. 5 ^simeonov2021neural-024
- Placing query points near a mug handle would yield a pose descriptor sensitive to handle position across mug instances. (Simeonov et al., 2021) `ev:asserted` p. 5 ^simeonov2021neural-025
- Query points are sampled uniformly at random within the bounding box of the rigid body, a heuristic the authors find robust. (Simeonov et al., 2021) `ev:reported` p. 5 ^simeonov2021neural-026
- Pose regression optimizes a randomly initialized axis-angle rotation and translation with ADAM, minimizing the L1 distance between pose descriptors. (Simeonov et al., 2021) `ev:reported` p. 5 ^simeonov2021neural-027
- Descriptors from the K demonstrations are averaged into single pick and place descriptors used as targets at test time. (Simeonov et al., 2021) `ev:reported` p. 5 ^simeonov2021neural-028
- The final predicted pick-and-place poses are executed with off-the-shelf inverse kinematics and motion planning algorithms. (Simeonov et al., 2021) `ev:reported` p. 5 ^simeonov2021neural-029
- The environment has a Franka Panda arm on a table with a depth camera at each table corner. (Simeonov et al., 2021) `ev:reported` p. 5 ^simeonov2021neural-030
- Quantitative experiments simulate the robot environment in PyBullet, with a rack or shelf mounted on the table as placement surface. (Simeonov et al., 2021) `ev:reported` p. 5 ^simeonov2021neural-031
- Each task is given 10 demonstrations, with success measured on unseen object instances with randomly sampled initial poses. (Simeonov et al., 2021) `ev:reported` p. 5 ^simeonov2021neural-032
- The setup assumes a segmented object point cloud and a static environment fixed between demonstration time and test time. (Simeonov et al., 2021) `ev:reported` p. 6 ^simeonov2021neural-033
- The three tasks are hanging a mug on a rack by its handle and placing a bowl or bottle upright on a shelf. (Simeonov et al., 2021) `ev:reported` p. 6 ^simeonov2021neural-034
- Simulation uses ShapeNet meshes for each object class, filtering out meshes incompatible with the tasks. (Simeonov et al., 2021) `ev:reported` p. 6 ^simeonov2021neural-035
- The baseline is a pick-and-place pipeline built on Dense Object Nets, registering detected keypoints to demonstration keypoints using SVD for placement. (Simeonov et al., 2021) `ev:reported` p. 6 ^simeonov2021neural-036
- TransporterNets reached a 92% success rate at grasping the rim of a mug in tasks where top-down grasping is sufficient. (Simeonov et al., 2021) `ev:measured` p. 6 ^simeonov2021neural-037
- The authors' attempts at a 6-DoF extension of TransporterNets failed to achieve a success rate above 10%. (Simeonov et al., 2021) `ev:measured` p. 6 ^simeonov2021neural-038
- Both DON and NDF are pretrained on a dataset of 100,000 mug, bowl and bottle objects at random tabletop poses. (Simeonov et al., 2021) `ev:reported` p. 6 ^simeonov2021neural-039
- In the training setup, the DON baseline is trained with 300 RGB-D views per object carrying labeled dense correspondences. (Simeonov et al., 2021) `ev:reported` p. 6 ^simeonov2021neural-040
- NDF is trained on point clouds captured from four static depth cameras, reconstructing 3D shapes with an occupancy network. (Simeonov et al., 2021) `ev:reported` p. 6 ^simeonov2021neural-041
- A single NDF model is trained across all categories, whereas DON requires separate models for each category. (Simeonov et al., 2021) `ev:reported` p. 6 ^simeonov2021neural-042
- For upright mugs, NDF reached 0.88 overall pick-and-place success in simulation compared with 0.45 for DON. (Simeonov et al., 2021) `ev:measured` p. 6 ^simeonov2021neural-043
- For upright mugs, grasp success was 0.96 for NDF and 0.91 for DON in simulation. (Simeonov et al., 2021) `ev:measured` p. 6 ^simeonov2021neural-044
- For upright mugs, place success was 0.92 for NDF and 0.50 for DON in simulation. (Simeonov et al., 2021) `ev:measured` p. 6 ^simeonov2021neural-045
- For upright bowls, NDF reached 0.91 overall success in simulation, compared with 0.11 for DON. (Simeonov et al., 2021) `ev:measured` p. 6 ^simeonov2021neural-046
- For upright bottles, NDF reached 0.87 overall success in simulation, compared with 0.24 for DON. (Simeonov et al., 2021) `ev:measured` p. 6 ^simeonov2021neural-047
- For mugs in arbitrary poses, NDF reached 0.58 overall success in simulation, compared with 0.17 for DON. (Simeonov et al., 2021) `ev:measured` p. 6 ^simeonov2021neural-048
- For bowls in arbitrary poses, NDF reached 0.78 overall success in simulation, compared with 0.00 for DON. (Simeonov et al., 2021) `ev:measured` p. 6 ^simeonov2021neural-049
- For bottles in arbitrary poses, NDF reached 0.77 overall success in simulation, compared with 0.01 for DON. (Simeonov et al., 2021) `ev:measured` p. 6 ^simeonov2021neural-050
- The Table I caption states that NDFs perform on par with DON on grasp success for objects in upright poses. (Simeonov et al., 2021) `ev:measured` p. 6 ^simeonov2021neural-051
- DON's failures in the upright setting usually stem from insufficient keypoint precision or failed registration of test keypoints to demonstration keypoints. (Simeonov et al., 2021) `ev:measured` p. 7 ^simeonov2021neural-052
- DON placement may fail even with semantically correct keypoints when their relative locations differ too much from demonstration objects. (Simeonov et al., 2021) `ev:measured` p. 7 ^simeonov2021neural-053
- In arbitrary poses, DON performance suffered significantly despite training on a large image dataset of objects in different poses. (Simeonov et al., 2021) `ev:measured` p. 7 ^simeonov2021neural-054
- The authors attribute NDF's drop in arbitrary poses to the PointNet encoder not being perfectly robust to unobserved occlusions and disocclusions. (Simeonov et al., 2021) `ev:asserted` p. 7 ^simeonov2021neural-055
- On the upright mug task, NDF with a randomly initialized occupancy network reached 0.00 overall success versus 0.88 using all layers. (Simeonov et al., 2021) `ev:measured` p. 7 ^simeonov2021neural-056
- Using only first-layer or only last-layer occupancy network activations gave 0.65 overall success on the upright mug task. (Simeonov et al., 2021) `ev:measured` p. 7 ^simeonov2021neural-057
- The authors conclude this ablation validates treating occupancy networks as hierarchical feature extractors and 3D reconstruction as important for learning features. (Simeonov et al., 2021) `ev:asserted` p. 7 ^simeonov2021neural-058
- Scaling the query point cloud by 1.0 gave 0.88 overall success, whereas scales 0.1 and 10.0 gave 0.39 and 0.27. (Simeonov et al., 2021) `ev:measured` p. 7 ^simeonov2021neural-059
- With one demonstration, NDF reached 0.46 overall success on upright mugs, compared with 0.32 for DON. (Simeonov et al., 2021) `ev:measured` p. 8 ^simeonov2021neural-060
- With five demonstrations, NDF reached 0.70 overall success on upright mugs, compared with 0.36 for DON. (Simeonov et al., 2021) `ev:measured` p. 8 ^simeonov2021neural-061
- Real-robot experiments used ten upright pick-and-place demonstrations on mugs, bowls and bottles, then executed tasks on novel instances in varied configurations. (Simeonov et al., 2021) `ev:reported` p. 7 ^simeonov2021neural-062
- As 2D CNNs are only equivariant to shifts parallel to the image plane, 2D keypoint methods require training images from all rotations and translations. (Simeonov et al., 2021) `ev:asserted` p. 8 ^simeonov2021neural-063
- Transporter Nets are equivariant to in-plane 2D translations but struggle to predict arbitrary 6-DoF poses. (Simeonov et al., 2021) `ev:cited` p. 8 ^simeonov2021neural-064
- The authors state that applying NDFs to non-rigid objects is possible in principle but remains untested. (Simeonov et al., 2021) `ev:asserted` p. 8 ^simeonov2021neural-065
- The authors note NDFs only define transferable energy landscapes over poses and points, suggesting trajectory optimization as future work. (Simeonov et al., 2021) `ev:asserted` p. 8 ^simeonov2021neural-066
- The method assumes the placement target remains static, leaving object-centric representation of the placement target to future work. (Simeonov et al., 2021) `ev:asserted` p. 8 ^simeonov2021neural-067
- NDFs enable few-shot imitation with only task-agnostic 3D reconstruction pre-training and no further training at imitation-learning time. (Simeonov et al., 2021) `ev:asserted` p. 8 ^simeonov2021neural-068

## 🎯 Contributions

## 📖 Glossary

- **Neural Descriptor Field (NDF)** — Neural function mapping a 3D coordinate and object point cloud to a category-level descriptor.
- **Pose descriptor field** — Concatenated point descriptors of a query point set transformed by an SE(3) pose.
- **SE(3) equivariance** — Outputs transform consistently when inputs undergo any 3D rotation and translation.
- **Occupancy network** — Neural implicit model predicting whether a 3D point lies inside a shape.
- **Vector Neurons** — Network building blocks giving point-cloud models SO(3) rotation equivariance.
- **Dense Object Nets (DON)** — Self-supervised 2D dense visual descriptors used for robotic correspondence.
- **Query points** — Rigid point set whose configuration parameterizes a local reference frame.

## ❓ Open questions

- Do NDFs transfer to non-rigid or deformable objects, as the authors suggest is possible in principle?
- Can NDF energy landscapes be integrated with trajectory optimization to transfer full trajectories rather than single poses?
- How can the placement target be represented object-centrically when it is not static between demonstration and test?
- How can the point-cloud encoder be made robust to occlusions and disocclusions unseen during training?
- What real-robot success rates does the method achieve, given that the real-world results are shown only qualitatively?

## 📝 Notes on reading

Read the arXiv v1 preprint (arXiv:2112.05124v1, 9 Dec 2021), 9 pages including references.

Inconsistency: the introduction (p. 2) claims an overall success rate above 85% on unseen instances in out-of-distribution configurations, but Table I (p. 6) gives arbitrary-pose overall success of 0.58 (mug), 0.78 (bowl) and 0.77 (bottle); only the upright-pose rows exceed 0.85.

Inconsistency: the Table I caption (p. 6) says NDFs perform on par with DON on grasp success for upright objects, while the text on p. 7 says NDFs perform significantly better on grasping; the upright grasp numbers are 0.96/0.91 (mug), 0.91/0.50 (bowl), 0.87/0.79 (bottle).

Table III (p. 7) was extracted as a flat row of numbers; columns were mapped to scales 0.1, 0.5, 1.0, 2.0, 10.0 in G/P/O order. Table IV sits on p. 8. Figures 1, 4, 5, 6, 7, 8 and 9 are qualitative visualizations only; real-robot results (Fig. 9, supplementary video) carry no numeric success rates. Equations (4) and (10) lost their concatenation operator in extraction.

## Suggested new concepts

- Neural Descriptor Fields — a reusable category-level, SE(3)-equivariant object representation for few-shot manipulation.
- SE(3)-equivariant representations for manipulation — a design principle for generalizing to unseen object poses without data augmentation.
- Few-shot imitation learning for pick-and-place — learning category-level tasks from a handful of demonstrations.
- Neural implicit representations (occupancy networks) as feature extractors — reusing reconstruction-trained networks as dense descriptors.
- Dense object correspondence for robotics — keypoint and descriptor methods such as DON that NDFs compare against.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Transferencia de agarres por optimización en $SE(3)$ con pocas demos
