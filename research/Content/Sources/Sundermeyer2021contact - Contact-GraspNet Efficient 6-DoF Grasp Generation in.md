---
aliases: []
type: "source"
title: "Contact-GraspNet: Efficient 6-DoF Grasp Generation in Cluttered Scenes"
citekey: "Sundermeyer2021contact"
doi: "10.48550/arXiv.2103.14127"
arxiv: "2103.14127"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2103.14127"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Martin Sundermeyer", "Arsalan Mousavian", "Rudolph Triebel", "Dieter Fox"]
sha256: ["6bfe10128f6f0a5231afd1745064475d92084deff673c26c7393fb42b8a26465"]
pdf: "Content/Papers/Sundermeyer2021contact.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Sundermeyer2021contact.pdf]]

> [!abstract] One-sentence summary
> Contact-GraspNet predicts 6-DoF parallel-jaw grasps end to end from a scene point cloud by rooting each grasp at an observed contact point, reducing the learned pose space to 4-DoF and reaching 90.20 real-robot success in structured clutter with runtimes suitable for closed-loop grasping.

## Abstract

Grasping unseen objects in unconstrained, cluttered environments is an essential skill for autonomous robotic manipulation. Despite recent progress in full 6-DoF grasp learning, existing approaches often consist of complex sequential pipelines that possess several potential failure points and run-times unsuitable for closed-loop grasping. Therefore, we propose an end-to-end network that efficiently generates a distribution of 6-DoF parallel-jaw grasps directly from a depth recording of a scene. Our novel grasp representation treats 3D points of the recorded point cloud as potential grasp contacts. By rooting the full 6-DoF grasp pose and width in the observed point cloud, we can reduce the dimensionality of our grasp representation to 4-DoF which greatly facilitates the learning process. Our class-agnostic approach is trained on 17 million simulated grasps and generalizes well to real world sensor data. In a robotic grasping study of unseen objects in structured clutter we achieve over 90% success rate, cutting the failure rate in half compared to a recent state-of-the-art method. (arXiv)

## 🧠 Key ideas (atomic)

- Existing full 6-DoF grasp learning approaches often rely on complex sequential pipelines that possess several potential failure points. (Sundermeyer et al., 2021) `ev:asserted` p. 1 ^sundermeyer2021contact-001
- Model-based grasping pre-defines a set of grasps in the object frame, transforming them according to the detected 6-DoF object pose. (Sundermeyer et al., 2021) `ev:cited` p. 1 ^sundermeyer2021contact-002
- Much data-driven grasping work constrains the grasp space to planar grasping, representing grasps as oriented rectangles around each pixel. (Sundermeyer et al., 2021) `ev:cited` p. 1 ^sundermeyer2021contact-003
- Planar grasp representations need the camera to view the scene perpendicularly, which limits 3D reasoning and applications significantly. (Sundermeyer et al., 2021) `ev:asserted` p. 1 ^sundermeyer2021contact-004
- The paper tackles 6-DoF grasping of unknown objects in cluttered scenes from a partial point cloud observation of the scene. (Sundermeyer et al., 2021) `ev:reported` p. 1 ^sundermeyer2021contact-005
- Generating a diverse grasp set is crucial because different subsets of grasps are kinematically feasible depending on the object-robot relative pose. (Sundermeyer et al., 2021) `ev:asserted` p. 1 ^sundermeyer2021contact-006
- Murali et al. synthesize grasps from the segmented target object point cloud, then filter out colliding grasps using another learned model. (Sundermeyer et al., 2021) `ev:cited` p. 2 ^sundermeyer2021contact-007
- The authors argue that the multi-stage pipeline of Murali et al. is sensitive to instance segmentation errors. (Sundermeyer et al., 2021) `ev:asserted` p. 2 ^sundermeyer2021contact-008
- Contact-GraspNet directly processes a full scene point cloud or a local region around a target object instead of a segmented object. (Sundermeyer et al., 2021) `ev:reported` p. 2 ^sundermeyer2021contact-009
- A common drawback of end-to-end grasping policies is limited generalization to novel environments, since perception and control are learned indirectly together. (Sundermeyer et al., 2021) `ev:cited` p. 2 ^sundermeyer2021contact-010
- The authors state that predicting approach directions cannot easily capture high curvature areas such as mug rims or handles. (Sundermeyer et al., 2021) `ev:asserted` p. 2 ^sundermeyer2021contact-011
- The authors aim to generate stable grasps with full surface contact, since such grasps preserve knowledge about the object state. (Sundermeyer et al., 2021) `ev:asserted` p. 2 ^sundermeyer2021contact-012
- Unlike other methods, the proposed approach has no assumption that grasps are always perpendicular to a surface. (Sundermeyer et al., 2021) `ev:asserted` p. 2 ^sundermeyer2021contact-013
- The method takes a raw depth image, optionally with object masks, and generates 6-DoF grasp proposals with corresponding grasp widths. (Sundermeyer et al., 2021) `ev:reported` p. 2 ^sundermeyer2021contact-014
- The authors observe that for most predictable two-finger grasps at least one of the two contacts is visible prior to grasping. (Sundermeyer et al., 2021) `ev:asserted` p. 3 ^sundermeyer2021contact-015
- Successful 6-DoF ground truth grasps are mapped to their corresponding contact points, represented by nearby points in a recorded point cloud. (Sundermeyer et al., 2021) `ev:reported` p. 3 ^sundermeyer2021contact-016
- Rooting grasps at contact points reduces the learning problem to estimating a 3-DoF grasp rotation plus the grasp width of the gripper. (Sundermeyer et al., 2021) `ev:reported` p. 3 ^sundermeyer2021contact-017
- The authors state that their rotation representation, in contrast to axis-angle representations, has neither ambiguities nor [[Rotation representation continuity|discontinuities]]. (Sundermeyer et al., 2021) `ev:asserted` p. 3 ^sundermeyer2021contact-018
- Training uses the [[ACRONYM dataset]], which consists of 8872 meshes from ShapeNet with 17.7 million simulated grasps under varying friction. (Sundermeyer et al., 2021) `ev:reported` p. 3 ^sundermeyer2021contact-019
- Rendered points are labelled positive contacts when a non-colliding ground truth mesh contact lies within a radius of r = 5mm. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-020
- Each positive point receives the rotation and width of the closest mesh contact grasp, with translation recomputed from that point. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-021
- The network is an asymmetric U-shaped architecture built from PointNet++ set abstraction and feature propagation layers. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-022
- The network takes n=20000 random input points and predicts grasps for only m=2048 farthest points of the input. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-023
- The network has four heads with two 1D-Conv layers each, giving per-point contact success, two direction vectors and width bins. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-024
- The predicted grasp width is split into 10 equidistant grasp width bins to counteract data imbalance in training. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-025
- Approach and baseline predictions are coupled through an in-network Gram Schmidt orthonormalization, predicting only the approach component orthonormal to the baseline. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-026
- Contact success is trained with binary cross entropy, backpropagating only the top-k predictions with the largest errors, with k=512. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-027
- The pose loss is a confidence-weighted minimum average distance between five gripper points under predicted and ground truth grasps. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-028
- Width bin losses are weighted anti-proportional to bin size because small grasp widths are highly over-represented in the data. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-029
- The total loss sums contact, pose and width terms with weights α = 1, β = 10 and γ = 1. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-030
- Training uses the Adam optimizer with an initial learning rate of 0.001 and a step-wise decay to 0.0001. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-031
- The training set comprises 10000 table top scenes, each placing 8-12 grasp annotated ShapeNet models at random stable poses. (Sundermeyer et al., 2021) `ev:reported` p. 4 ^sundermeyer2021contact-032
- Training with a batch size of 3 for 144.000 iterations takes ∼40 hours on a single Nvidia V100 GPU. (Sundermeyer et al., 2021) `ev:measured` p. 4 ^sundermeyer2021contact-033
- The authors report that convergence is significantly faster than previous methods, which take up to one week on a single GPU. (Sundermeyer et al., 2021) `ev:cited` p. 4 ^sundermeyer2021contact-034
- Method and data variants are compared by executing a large number of predicted grasps in the FleX physics simulator. (Sundermeyer et al., 2021) `ev:reported` p. 5 ^sundermeyer2021contact-035
- Local regions of interest are cubes with edge length twice the largest spanning dimension, but at least 0.3m and at most 0.6m. (Sundermeyer et al., 2021) `ev:reported` p. 5 ^sundermeyer2021contact-036
- Contact-GraspNet has a run time of 0.28s for a full scene, versus ∼0.19s for a local region around a target object. (Sundermeyer et al., 2021) `ev:measured` p. 5 ^sundermeyer2021contact-037
- Grasps are selected with a contact confidence threshold of 0.23, reduced to 0.19 when an object has too few predicted grasps. (Sundermeyer et al., 2021) `ev:reported` p. 5 ^sundermeyer2021contact-038
- The most confident grasp that is kinematically reachable without robot collision with the scene is finally executed. (Sundermeyer et al., 2021) `ev:reported` p. 5 ^sundermeyer2021contact-039
- Without weighted binning in the grasp width loss, both success rate and coverage decrease in the simulated loss ablation. (Sundermeyer et al., 2021) `ev:measured` p. 5 ^sundermeyer2021contact-040
- The pose distance loss leads to increased success rates at high confidence contacts, with slightly decreased success in the low-confidence regime. (Sundermeyer et al., 2021) `ev:measured` p. 5 ^sundermeyer2021contact-041
- Training with Gaussian noise has similar performance in simulation but helps generalization to noisy sensor data. (Sundermeyer et al., 2021) `ev:measured` p. 5 ^sundermeyer2021contact-042
- Predicting grasps on full scenes without extracting local regions yields a similar average success rate but significantly lowers grasp coverage. (Sundermeyer et al., 2021) `ev:measured` p. 5 ^sundermeyer2021contact-043
- A simulated grasp counts as successful if the open gripper does not collide and the object stays gripped after shaking. (Sundermeyer et al., 2021) `ev:reported` p. 6 ^sundermeyer2021contact-044
- The authors call this success criterion conservative, as most real world grasps can slightly collide without undergoing a shaking motion. (Sundermeyer et al., 2021) `ev:asserted` p. 6 ^sundermeyer2021contact-045
- Coverage is the percentage of ground truth grasps whose base coordinates lie within 2cm of any of the generated grasps. (Sundermeyer et al., 2021) `ev:reported` p. 6 ^sundermeyer2021contact-046
- Real experiments allow a maximum of two grasp trials per object without rearrangements, also reporting the success rate after a single trial. (Sundermeyer et al., 2021) `ev:reported` p. 6 ^sundermeyer2021contact-047
- The robot experiments closely replicate the 9 cluttered scenes defined by Murali et al., with a total of 51 unseen objects. (Sundermeyer et al., 2021) `ev:reported` p. 6 ^sundermeyer2021contact-048
- The physical setup uses a 7-DoF Franka Panda robot with a parallel-jaw gripper and a tripod-mounted Intel Realsense L515 camera. (Sundermeyer et al., 2021) `ev:reported` p. 6 ^sundermeyer2021contact-049
- In cluttered scene grasping, Contact-GraspNet achieved a success rate of 90.20, compared with 80.39 for 6-DoF GraspNet plus CollisionNet. (Sundermeyer et al., 2021) `ev:measured` p. 6 ^sundermeyer2021contact-050
- In the real cluttered scenes, Contact-GraspNet reached 84.31 first-attempt success, versus 68.63 for 6-DoF GraspNet with CollisionNet. (Sundermeyer et al., 2021) `ev:measured` p. 6 ^sundermeyer2021contact-051
- Contact-GraspNet needed 59 grasp attempts in total, compared with 67 attempts for 6-DoF GraspNet combined with CollisionNet. (Sundermeyer et al., 2021) `ev:measured` p. 6 ^sundermeyer2021contact-052
- 6-DOF GraspNet alone reached a success rate of 62.7 in the cluttered scene grasping comparison reported by the authors. (Sundermeyer et al., 2021) `ev:measured` p. 6 ^sundermeyer2021contact-053
- In one example, successful grasp contacts are still found on a driller despite severe under-segmentation of the unknown objects. (Sundermeyer et al., 2021) `ev:measured` p. 6 ^sundermeyer2021contact-054
- Without weighting the grasp width bins, the width predictions mostly collapse into narrow grasp widths in the ablation. (Sundermeyer et al., 2021) `ev:measured` p. 6 ^sundermeyer2021contact-055
- Weighting the grasp width bin losses also performs better than oversampling in the ablation experiments reported by the authors. (Sundermeyer et al., 2021) `ev:measured` p. 6 ^sundermeyer2021contact-056
- Zooming into local regions allows the network to concentrate potential contact points on the object, which increases coverage. (Sundermeyer et al., 2021) `ev:measured` p. 6 ^sundermeyer2021contact-057
- Training on a small grasp dataset with 110 objects from 5 categories is not sufficient for out-of-category generalization irrespective of method. (Sundermeyer et al., 2021) `ev:measured` p. 6 ^sundermeyer2021contact-058
- Some failure cases occur for thick objects that only allow grasps almost at maximum grasp width, where predictions are less confident. (Sundermeyer et al., 2021) `ev:measured` p. 6 ^sundermeyer2021contact-059
- Injecting noise during training reduces the low-confidence effect observed for thick objects requiring near-maximum grasp widths. (Sundermeyer et al., 2021) `ev:measured` p. 6 ^sundermeyer2021contact-060
- Small objects sometimes have contact points with low confidence, possibly because of their small impact on the total loss. (Sundermeyer et al., 2021) `ev:asserted` p. 6 ^sundermeyer2021contact-061
- The authors conclude that gripper collisions are effectively avoided by considering them during training and by predicting grasps directly in scenes. (Sundermeyer et al., 2021) `ev:asserted` p. 6 ^sundermeyer2021contact-062
- The authors state that their approach can incorporate segmentation predictions but is not dependent on accurate masks itself. (Sundermeyer et al., 2021) `ev:asserted` p. 6 ^sundermeyer2021contact-063

## 🎯 Contributions


## 📖 Glossary

- **6-DoF grasp** — Full gripper pose in SE(3): 3D position plus 3D orientation.
- **Contact grasp representation** — Grasp encoded at an observed contact point with rotation and width only.
- **Parallel-jaw gripper** — Two-finger gripper whose fingers close along a single baseline.
- **Approach vector** — Unit direction along which the gripper moves toward the object.
- **Baseline vector** — Unit direction connecting the two gripper fingers.
- **Grasp coverage** — Fraction of ground truth grasps within 2cm of any generated grasp.
- **ACRONYM** — Large simulated grasp dataset on ShapeNet meshes with dense grasp annotations.
- **PointNet++** — Hierarchical point set network aggregating features in local 3D neighborhoods.
- **Gram-Schmidt orthonormalization** — Procedure making two predicted vectors orthogonal unit vectors.
- **Structured clutter** — Scenes of several densely placed objects, e.g. on a table top.

## ❓ Open questions

- How does the method perform on thick objects needing near-maximum grasp width beyond noise injection?
- Can small objects be given adequate contact confidence, e.g. by loss reweighting?
- How well does the contact representation handle grasps without full surface contact, such as through mug handles?
- How does performance change beyond the 9 replicated scenes and 51 objects, for example in unstructured bins?
- Would multi-view or closed-loop use of the ∼0.19s runtime further improve first-attempt success?
- How does the method extend to grippers other than parallel-jaw grippers?

## 📝 Notes on reading

Version read: arXiv preprint 2103.14127v1 (25 Mar 2021), matching the packet identifier.

The abstract says the model is trained on 17 million simulated grasps; the body (p. 3) gives 17.7 million grasps for ACRONYM. The abstract says over 90% success cutting the failure rate in half; the intro (p. 2) says 90% success, 10% higher than Murali et al.; Table I (p. 6) gives 90.20 vs 80.39, which is consistent with roughly halving the failure rate. Table I values are printed without a percent sign.

The text writes parallel-yaw gripper (p. 3), evidently a typo for parallel-jaw. Iteration count is printed as 144.000 (European thousands separator). Equations (1)-(8) on pp. 3-4 are partly garbled by extraction (matrix layout, subscripts); their structure was described in words rather than transcribed. The query ball radii list on p. 4 contains a typo (0.08.0.16).

Figures 5 and 6 (p. 5) are success-coverage curves; only their captions were claimed, no numeric values were read from the plots. Figure 4 (inference pipeline) and Figure 2 (data pipeline) were used only descriptively.

## Suggested new concepts

- Contact-based grasp representation — rooting 6-DoF grasps at observed contact points is a reusable dimensionality-reduction idea for grasp learning.
- 6-DoF grasp generation — a distinct problem family (vs planar grasping) with generative and discriminative methods to compare.
- ACRONYM dataset — large simulated grasp dataset referenced as key for out-of-category generalization.
- Success-coverage metric — standard simulator evaluation of grasp quality and diversity used across grasp generation papers.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Agarres 6-DoF anclados a contactos
