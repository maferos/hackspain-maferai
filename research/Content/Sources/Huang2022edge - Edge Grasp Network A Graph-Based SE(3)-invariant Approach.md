---
aliases: []
type: "source"
title: "Edge Grasp Network: A Graph-Based SE(3)-invariant Approach to Grasp Detection"
citekey: "Huang2022edge"
doi: "10.48550/arXiv.2211.00191"
arxiv: "2211.00191"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2211.00191"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Haojie Huang", "Dian Wang", "Xupeng Zhu", "Robin Walters", "Robert Platt"]
sha256: ["2cf78c5bf3940fdd7ea20e3bce8e0d51e923de50f9cc24ca0acbedc08d764e80"]
pdf: "Content/Papers/Huang2022edge.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Huang2022edge.pdf]]

> [!abstract] One-sentence summary
> The paper defines a 6-DoF parallel-jaw grasp as an edge between an approach point and a contact point in a point cloud, scores all edges around each approach point with a rotation-invariant graph network, and reports higher grasp success than VGN, GIGA, PointNetGPD, VPN and Zhu et al. in simulation and on a real robot.

## Abstract

Given point cloud input, the problem of 6-DoF grasp pose detection is to identify a set of hand poses in SE(3) from which an object can be successfully grasped. This important problem has many practical applications. Here we propose a novel method and neural network model that enables better grasp success rates relative to what is available in the literature. The method takes standard point cloud data as input and works well with single-view point clouds observed from arbitrary viewing directions. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that SE(3) grasp methods can find side grasps more easily than SE(2) methods, which reason over a top-down image. (Huang et al., 2022) `ev:asserted` p. 1 ^huang2022edge-001
- The authors note that SE(3) grasp methods are generally much more complex, so SE(2) grasp models are often preferred in practice. (Huang et al., 2022) `ev:asserted` p. 1 ^huang2022edge-002
- The authors claim their model is the first SE(3) grasp detection method that incorporates SO(3) equivariance into its network. (Huang et al., 2022) `ev:asserted` p. 1 ^huang2022edge-003
- The authors argue that VGN and GIGA are trained for multiple camera views or a particular viewpoint, generalizing poorly to novel viewing directions. (Huang et al., 2022) `ev:asserted` p. 1 ^huang2022edge-004
- The method lets a user restrict grasps to a region, such as a tool handle, by choosing approach positions and contact locations there. (Huang et al., 2022) `ev:asserted` p. 1 ^huang2022edge-005
- The authors state that sample-based grasp methods often need long training and execution times because each grasp is represented and evaluated individually. (Huang et al., 2022) `ev:asserted` p. 1 ^huang2022edge-006
- The authors argue that regression-based point methods predict one grasp pose per point, which may cause ambiguity when several poses are valid there. (Huang et al., 2022) `ev:asserted` p. 2 ^huang2022edge-007
- The authors note that memory for voxel grids or SDFs grows cubically with grid resolution, severely limiting the usable resolution of volumetric methods. (Huang et al., 2022) `ev:asserted` p. 2 ^huang2022edge-008
- The grasp quality function is defined to be invariant when the point cloud and the grasp pose are transformed by the same SE(3) element. (Huang et al., 2022) `ev:asserted` p. 2 ^huang2022edge-009
- An edge grasp is a pair of cloud points, an approach point pa plus a contact point pc, whose surface normal sets finger closing direction. (Huang et al., 2022) `ev:reported` p. 2 ^huang2022edge-010
- Contact points for each approach point are sampled from its neighbors within half the gripper aperture, the distance between open fingers. (Huang et al., 2022) `ev:reported` p. 2 ^huang2022edge-011
- For each approach point, the network crops the point cloud to a ball of radius half the gripper width centred on that point. (Huang et al., 2022) `ev:reported` p. 2 ^huang2022edge-012
- Point features come from a stack of PointNetConv layers applied repeatedly over the same graph, without the successive abstraction used in PointNet++. (Huang et al., 2022) `ev:reported` p. 3 ^huang2022edge-013
- A global feature of the cropped ball is concatenated with each contact point's feature to form the edge feature representing one grasp. (Huang et al., 2022) `ev:reported` p. 3 ^huang2022edge-014
- A four-layer MLP with a sigmoid output takes each edge feature and predicts whether the corresponding edge grasp will succeed. (Huang et al., 2022) `ev:reported` p. 3 ^huang2022edge-015
- The network is translation invariant because each cropped ball is centred on its approach point, which is translated to the world origin. (Huang et al., 2022) `ev:asserted` p. 3 ^huang2022edge-016
- Rotational invariance is obtained in two ways: training with SO(3) data augmentation, or building the network from [[Vector Neurons|SO(3)-equivariant Vector Neurons]]. (Huang et al., 2022) `ev:reported` p. 3 ^huang2022edge-017
- All edge grasps sharing one approach point are evaluated in a single forward pass, but each different approach point requires separate evaluation. (Huang et al., 2022) `ev:asserted` p. 3 ^huang2022edge-018
- Several approach points are evaluated together by batching their cropped KNN graphs into one minibatch and running a single forward pass. (Huang et al., 2022) `ev:reported` p. 3 ^huang2022edge-019
- Simulation used the PyBullet grasp simulator of Breyer et al. with a Franka-Emika Panda gripper, 303 training objects, 40 test objects. (Huang et al., 2022) `ev:reported` p. 4 ^huang2022edge-020
- Each simulated test round places 5 test objects in a 30 × 30 × 30 cm3 workspace, grasping one object at a time. (Huang et al., 2022) `ev:reported` p. 4 ^huang2022edge-021
- Pixelwise Gaussian noise was added to simulated depth images, and a round ended after clearing all objects or two consecutive grasp failures. (Huang et al., 2022) `ev:reported` p. 4 ^huang2022edge-022
- The model input is a point cloud downsampled with a 4mm voxel size, with PointNetConv layers built on a KNN graph of k = 16. (Huang et al., 2022) `ev:reported` p. 4 ^huang2022edge-023
- The training set contained 3.36M labeled grasps from 3, 317 simulated scenes, with 85% used for training and 15% for testing. (Huang et al., 2022) `ev:reported` p. 4 ^huang2022edge-024
- Up to 2000 edge grasp candidates per training scene were generated from 32 approach points, each candidate labeled by a simulated grasp attempt. (Huang et al., 2022) `ev:reported` p. 4 ^huang2022edge-025
- Training used Adam with an initial learning rate of 10−4 for 150 epochs, balancing positive with negative grasp labels. (Huang et al., 2022) `ev:reported` p. 4 ^huang2022edge-026
- Both VN-EdgeGraspNet and EdgeGraspNet converged in less than 10 hours, with one SGD step taking about 0.5 seconds on a Tesla V100. (Huang et al., 2022) `ev:measured` p. 4 ^huang2022edge-027
- The authors' retrained VGN and GIGA underperformed the pretrained models of Jiang et al., so the pretrained models were used for evaluation. (Huang et al., 2022) `ev:reported` p. 4 ^huang2022edge-028
- In simulation, EdgeGraspNet and PointNetGPD were given 64 approach points and 4000 grasps sampled uniformly per scene. (Huang et al., 2022) `ev:reported` p. 4 ^huang2022edge-029
- Simulated results were averaged over 100 simulation rounds with 5 different random seeds, reporting grasp success rate and declutter rate. (Huang et al., 2022) `ev:reported` p. 5 ^huang2022edge-030
- In the simulated packed scenario, VN-EdgeGraspNet reached a 92.3 ± 1.2 grasp success rate against 88.5 ± 2.0 for GIGA-High. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-031
- In simulated piles, VN-EdgeGraspNet reached a 92.3 ± 1.5 grasp success rate, against 75.6 ± 2.3 for PointNetGPD and 74.1 ± 1.5 for GIGA-High. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-032
- In the simulated pile scenario, EdgeGraspNet reached 89.9 ± 1.8 grasp success rate and 92.8 ± 1.6 declutter rate. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-033
- Selecting sampled edge grasps at random without the learned quality score (Edge-Sample) still gave grasp success rates between 40% and 44%. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-034
- The authors suggest the Edge-Sample result shows that the edge grasp representation and sampling strategy provide a helpful bias. (Huang et al., 2022) `ev:asserted` p. 5 ^huang2022edge-035
- Both EdgeGraspNet variants outperformed all simulation baselines in every performance category by a significant margin, particularly in the pile scenario. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-036
- The packed-to-pile performance gap was smaller for the Edge Grasp Network than for baselines, which the authors suggest reflects better adaptation. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-037
- EdgeGraspNet needs 28ms per 4,000 grasps on an RTX 3090, slightly slower than VGN or GIGA but much faster than PointNetGPD. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-038
- The [[Vector Neurons|Vector Neurons version]] is about three times slower at inference than EdgeGraspNet, taking 89 ms against 28 ms. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-039
- EdgeGraspNet has 3.0 M parameters and VN-EdgeGraspNet 1.7 M, more than the 0.3 M of VGN or the 0.6 M of GIGA. (Huang et al., 2022) `ev:reported` p. 5 ^huang2022edge-040
- Using fewer approach points and grasp samples reduced grasp success somewhat but not by a huge amount, per the sample-size ablation. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-041
- With 16 approach points and 1k grasps, EdgeGraspNet reached 88.5 ± 1.7 packed grasp success rate against 92.0 ± 1.4 with 64-4k. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-042
- In test-loss curves, the [[Vector Neurons|Vector Neurons version]] learned fastest, while base EdgeGraspNet with augmentation converged to approximately the same level. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-043
- Without either [[Vector Neurons]] or data augmentation, the Edge Grasp Network overfits, which the authors take as evidence that SO(3) symmetry helps. (Huang et al., 2022) `ev:measured` p. 5 ^huang2022edge-044
- Real-robot tests used a UR5 with a Robotiq-85 gripper, an arm-mounted Occipital Structure Sensor, and a randomly selected single viewpoint. (Huang et al., 2022) `ev:reported` p. 5 ^huang2022edge-045
- On the robot, 40 approach points with 2000 grasps were sampled, grasps scoring below 0.9 were discarded, and the highest candidate executed. (Huang et al., 2022) `ev:reported` p. 5 ^huang2022edge-046
- On real household packed and pile scenes over 16 rounds, grasp success rates varied between 91.7% and 93%, closely matching simulation. (Huang et al., 2022) `ev:measured` p. 6 ^huang2022edge-047
- EdgeGraspNet reached a 100 declutter rate on both real packed and pile household scenes, clearing all 80 objects in each. (Huang et al., 2022) `ev:measured` p. 6 ^huang2022edge-048
- The authors report that most real household failures seem to be caused by collisions with other objects during grasping. (Huang et al., 2022) `ev:measured` p. 6 ^huang2022edge-049
- On the 20 hard objects of Zhu et al., VN-EdgeGraspNet reached 93.6 grasp success rate against 89.0 for Zhu et al. (Huang et al., 2022) `ev:measured` p. 6 ^huang2022edge-050
- On the hard-object pile, VN-EdgeGraspNet reached a 98.6 declutter rate against 94.0 for the method of Zhu et al. (Huang et al., 2022) `ev:measured` p. 6 ^huang2022edge-051
- On the Berkeley adversarial pile, EdgeGraspNet reached 84.4 grasp success rate, against 78.4 reported for VPN by Cai et al. (Huang et al., 2022) `ev:measured` p. 6 ^huang2022edge-052
- Baseline results for VPN, GPD and VGN on the Berkeley adversarial objects were copied directly from Cai et al., not re-run. (Huang et al., 2022) `ev:reported` p. 6 ^huang2022edge-053
- The authors state that a clear direction for future work is integrating more on-policy learning, which they believe would improve performance. (Huang et al., 2022) `ev:asserted` p. 6 ^huang2022edge-054
- In the [[Vector Neurons|Vector Neurons version]], equivariance is kept until the edge feature, then made invariant by multiplying with a network-generated matrix. (Huang et al., 2022) `ev:reported` p. 8 ^huang2022edge-055
- An ablation that skips cropping around the approach point (EdgeGraspNet-NoBall) performed worse in test loss plus accuracy than cropping. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022edge-056
- Doubling the number of approach points increases inference time about 1.7 times, from 9.6 ms at 16 points to 27.4 ms at 64. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022edge-057
- With 32 approach points fixed, increasing sampled edge grasps from 500 to 2000 leaves inference time almost unchanged at about 15.8 ms. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022edge-058
- Almost half of the failures are caused by colliding with other objects during execution, which the authors suggest collision-aware selection could mitigate. (Huang et al., 2022) `ev:measured` p. 8 ^huang2022edge-059
- The authors list occlusion from partial single-view observation as a failure source, such as capturing only one plane of a complex object. (Huang et al., 2022) `ev:asserted` p. 8 ^huang2022edge-060
- The authors state that heavily distorted observations could make proposed edge grasps inaccurate because sampling depends closely on the observed points. (Huang et al., 2022) `ev:asserted` p. 9 ^huang2022edge-061
- The authors believe binary training labels that allow dangerous grasps, with large object pose change, could cause false positives under noisy observations. (Huang et al., 2022) `ev:asserted` p. 9 ^huang2022edge-062

## 🎯 Contributions

## 📖 Glossary

- **Edge grasp** — A parallel-jaw grasp defined by an approach point and a contact point in a point cloud.
- **Approach point** — The cloud point placed directly between the fingers, around which contacts are sampled.
- **Contact point** — The cloud point where a finger touches; its normal sets closing direction.
- **Vector Neurons** — A framework that makes neural layers SO(3)-equivariant by treating 3D vectors as features.
- **Grasp success rate (GSR)** — Successful grasps divided by total grasp attempts.
- **Declutter rate (DR)** — Objects removed successfully divided by total objects presented.
- **TSDF** — Truncated Signed Distance Function; a voxel grid of clipped distances to the nearest surface.
- **PointNetConv** — Graph layer computing a point feature by max-pooling an MLP over neighbor features and offsets.

## ❓ Open questions

- Would collision-aware grasp selection remove the roughly half of real-robot failures caused by collisions with neighboring objects?
- How much would on-policy learning improve the model, as the authors propose for future work?
- How does performance hold up when the simulated evaluation viewpoint differs from the training viewpoint, given all simulated methods used the viewpoint of Jiang et al.?
- Can labels that penalise dangerous grasps (large object pose change) reduce false positives under noisy observations?
- How does the method behave with heavily distorted or occluded observations where sampled edges depend on missing points?

## 📝 Notes on reading

- Version read: arXiv preprint 2211.00191v1 (31 Oct 2022), matching the packet identifier.
- Figure 1 (edge grasp geometry), Figure 2 (encoding pipeline), Figure 4 (test-loss curves for augmentation vs Vector Neurons), Figure 7 (NoBall ablation curves) and Figure 8 (grasp visualisations) could only be described from their captions and text; curve values are not claimed.
- The equations for the approach vector, gripper center offset and the PointNetConv update are partly garbled in the extraction (subscripts and superscripts lost); only their verbal description is claimed.
- Table VI: the text says the method outperforms VPN by between four and six percentage points; EdgeGraspNet is 84.4 and VN-EdgeGraspNet 83.0 against VPN 78.4, and VN-EdgeGraspNet has the lower GSR of the two variants here, unlike in other tables.
- The appendix text refers to "Table IX" for the fixed-approach-point inference-time result, but the relevant table is Table VIII; Table IX is the real-robot summary.
- Table IV labels the first row "EdgeGrasoNet", a typo for EdgeGraspNet.
- The simulated evaluation used a single fixed viewpoint from Jiang et al.'s training data (footnote 1), while training data used random camera views; the real-robot viewpoint was chosen randomly once and reused (footnote 3).
- Table III's 64-4k rows repeat the Table I values for both model variants.
- Simulation data used object mass 0.5 kg and gripper-object friction 0.75; the appendix states approach points for training were chosen by Farthest Point Sampling, while Section V-D says uniformly at random.

## Suggested new concepts

- Edge grasp representation — a distinct grasp parameterisation (approach point plus contact point) reusable across grasp detection methods.
- SE(3)-invariant grasp evaluation — a recurring design principle linking equivariant networks to 6-DoF grasp quality prediction.
- Vector Neurons — a general SO(3)-equivariant network framework used here and likely in other manipulation papers.
- Clutter removal benchmark (packed / pile) — the VGN/GIGA simulation protocol used for comparing 6-DoF grasp detectors.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Evaluación de agarres invariante a $SE(3)$
