---
aliases: []
type: "source"
title: "AnyGrasp: Robust and Efficient Grasp Perception in Spatial and Temporal Domains"
citekey: "Fang2022anygrasp"
doi: "10.48550/arXiv.2212.08333"
arxiv: "2212.08333"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2212.08333"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Hao-Shu Fang", "Chenxi Wang", "Hongjie Fang", "Minghao Gou", "Jirong Liu", "Hengxu Yan", "Wenhai Liu", "Yichen Xie", "Cewu Lu"]
sha256: ["57eaa4eb9756c351d0ffeb0dbdfdf8ffd04d178cabb6de3f8d39ec201f250de7"]
pdf: "Content/Papers/Fang2022anygrasp.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Fang2022anygrasp.pdf]]

> [!abstract] One-sentence summary
> AnyGrasp is a parallel-gripper grasp perception system that predicts dense 7-DoF grasps with centre-of-mass awareness and tracks them across frames, trained on real data from 144 objects and reaching human-level bin-picking success on over 300 unseen objects.

## Abstract

As the basis for prehensile manipulation, it is vital to enable robots to grasp as robustly as humans. Our innate grasping system is prompt, accurate, flexible, and continuous across spatial and temporal domains. Few existing methods cover all these properties for robot grasping. In this paper, we propose AnyGrasp for grasp perception to enable robots these abilities using a parallel gripper. Specifically, we develop a dense supervision strategy with real perception and analytic labels in the spatial-temporal domain. Additional awareness of objects' center-of-mass is incorporated into the learning process to help improve grasping stability. Utilization of grasp correspondence across observations enables dynamic grasp tracking. Our model can efficiently generate accurate, 7-DoF, dense, and temporally-smooth grasp poses and works robustly against large depth-sensing noise. Using AnyGrasp, we achieve a 93.3% success rate when clearing bins with over 300 unseen objects, which is on par with human subjects under controlled conditions. Over 900 mean-picks-per-hour is reported on a single-arm system. For dynamic grasping, we demonstrate catching swimming robot fish in the water. Our project page is at https://graspnet.net/anygrasp.html (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that sampling-evaluation grasp detection methods, which sample candidates from the scene before evaluating them, cannot generate dense predictions. (Fang et al., 2022) `ev:asserted` p. 1 ^fang2022anygrasp-001
- Existing grasp detection methods mainly focus on static scenes, leaving dynamic grasp detection largely unexplored according to the authors. (Fang et al., 2022) `ev:asserted` p. 1 ^fang2022anygrasp-002
- AnyGrasp's geometry processing module estimates dense 7-DoF grasp configurations for a monocular perceived observation in one feed-forward pass. (Fang et al., 2022) `ev:reported` p. 1 ^fang2022anygrasp-003
- A temporal association module identifies grasp correspondences among the predicted grasp poses across every two observations in AnyGrasp. (Fang et al., 2022) `ev:reported` p. 1 ^fang2022anygrasp-004
- The authors state that their model generates accurate 7-DoF grasp poses that are continuous across space and time in 100ms. (Fang et al., 2022) `ev:asserted` p. 1 ^fang2022anygrasp-005
- AnyGrasp is trained on real-world data from only 144 objects, rather than the thousands of simulated objects used by previous work. (Fang et al., 2022) `ev:reported` p. 2 ^fang2022anygrasp-006
- In bin picking with over 300 unseen objects, AnyGrasp achieved an object completion rate of over 99.8%. (Fang et al., 2022) `ev:measured` p. 2 ^fang2022anygrasp-007
- The authors claim AnyGrasp is the first unified system for fast, accurate, 7-DoF, temporally-continuous grasp pose detection with a parallel gripper. (Fang et al., 2022) `ev:asserted` p. 2 ^fang2022anygrasp-008
- Earlier learning-based grasp representations mainly generate 4 DoF grasp poses on the camera plane, which may neglect vital grasp poses. (Fang et al., 2022) `ev:cited` p. 2 ^fang2022anygrasp-009
- Sampling-evaluation 6 DoF grasp methods usually generated only tens of grasp poses per scene, according to the authors' review. (Fang et al., 2022) `ev:cited` p. 2 ^fang2022anygrasp-010
- Existing prior-free dynamic grasping methods only guarantee a small tracked-grasp distance in image coordinates, not in object coordinates. (Fang et al., 2022) `ev:cited` p. 2 ^fang2022anygrasp-011
- The authors state it remains unclear how many training objects are actually necessary for the 6-DoF grasping problem. (Fang et al., 2022) `ev:asserted` p. 3 ^fang2022anygrasp-012
- AnyGrasp represents a parallel-jaw grasp as gripper orientation, grasp centre and minimum gripper width, called the 7-DoF grasp configuration. (Fang et al., 2022) `ev:reported` p. 3 ^fang2022anygrasp-013
- Centre-of-gravity awareness is encoded by predicting, for each grasp, a normalized vertical distance from the gripper plane to the object COG. (Fang et al., 2022) `ev:reported` p. 3 ^fang2022anygrasp-014
- If an obstacle around a grasp pose leaves no space for gripper pre-shaping, the network sets its grasp quality score to zero. (Fang et al., 2022) `ev:reported` p. 3 ^fang2022anygrasp-015
- The temporal association module produces a many-to-many association score matrix between grasp poses predicted from two observations. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022anygrasp-016
- AnyGrasp's training data combine the GraspNet-1Billion training set with 168 extra scenes composed of 104 new objects. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022anygrasp-017
- In total, 268 scenes that consist of 144 objects are used to train the AnyGrasp network. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022anygrasp-018
- Images are taken at 256 different viewpoints for each training scene, with object 6D poses annotated manually. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022anygrasp-019
- The authors add an extra approach depth of 0.5 centimeters to the original four depths to grasp small objects. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022anygrasp-020
- The stable score is the normalized perpendicular distance from the gripper plane to the object COG, where lower scores tolerate more disturbance. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022anygrasp-021
- To compute the COG for annotation, each object is assumed to be a solid rigid body with uniform density. (Fang et al., 2022) `ev:reported` p. 4 ^fang2022anygrasp-022
- Grasp association labels are annotated on pairs of adjacent-viewpoint images of static scenes, standing in for moving objects. (Fang et al., 2022) `ev:reported` p. 5 ^fang2022anygrasp-023
- The geometry processing module is based on GSNet, with a minor modification to incorporate the stable score into the network. (Fang et al., 2022) `ev:reported` p. 5 ^fang2022anygrasp-024
- During inference, the original grasp score is multiplied by one minus the stable score to give the new ranking score. (Fang et al., 2022) `ev:reported` p. 6 ^fang2022anygrasp-025
- Each grasp's temporal feature vector concatenates colour features, seed features, grasp features and pose parameters, with size C set to 256. (Fang et al., 2022) `ev:reported` p. 6 ^fang2022anygrasp-026
- The correspondence score between two grasp poses in different point clouds is the cosine similarity of their feature vectors. (Fang et al., 2022) `ev:reported` p. 6 ^fang2022anygrasp-027
- The temporal association module is trained with supervised contrastive learning, with σ = 0.1 and temperature τ = 0.1. (Fang et al., 2022) `ev:reported` p. 6 ^fang2022anygrasp-028
- Extra point-cloud collision detection is run on the top-100 predicted grasp poses, since the learned obstacle awareness is not a hard constraint. (Fang et al., 2022) `ev:reported` p. 7 ^fang2022anygrasp-029
- The collision detection and gripper-centering post-processing steps run on GPU and take 80 ms for 100 grasp poses. (Fang et al., 2022) `ev:measured` p. 7 ^fang2022anygrasp-030
- The static bin-picking experiments use a UR5 robot arm with an overhead camera and a Robotiq-85 gripper. (Fang et al., 2022) `ev:reported` p. 7 ^fang2022anygrasp-031
- Human subjects used a two-finger jaw with the robot gripper's opening width and fingertip rubber, following an open-loop grasping strategy. (Fang et al., 2022) `ev:reported` p. 7 ^fang2022anygrasp-032
- The dynamic grasping experiments use a Flexiv Rizon arm with an Intel RealSense L515 camera attached to its wrist. (Fang et al., 2022) `ev:reported` p. 7 ^fang2022anygrasp-033
- Across all object categories, AnyGrasp reached a 93.3% attempt-centric success rate, against 72.2% for DexNet 4.0. (Fang et al., 2022) `ev:measured` p. 9 ^fang2022anygrasp-034
- Human subjects using a parallel jaw reached a 93.9% attempt-centric success rate across all object categories. (Fang et al., 2022) `ev:measured` p. 9 ^fang2022anygrasp-035
- AnyGrasp's attempt-centric success rate ranged from 81.5% to 100% across the object categories of the unseen test set. (Fang et al., 2022) `ev:measured` p. 9 ^fang2022anygrasp-036
- Human subjects gave more stable performance across object categories, with grasp accuracy ranging from 91.4% to 96.6%. (Fang et al., 2022) `ev:measured` p. 9 ^fang2022anygrasp-037
- The unseen test objects range in size from 1.5×1.5×1.5 cm3 to 36×4×11.5 cm3 across common daily-life categories. (Fang et al., 2022) `ev:reported` p. 9 ^fang2022anygrasp-038
- The grasp perception system predicts grasp poses in 100ms, with overall grasp decision time of less than 200 ms. (Fang et al., 2022) `ev:measured` p. 9 ^fang2022anygrasp-039
- With a single UR5 arm and a Robotiq gripper, AnyGrasp achieves over 900 MPPH, versus 300 MPPH for a previous dual-arm system. (Fang et al., 2022) `ev:measured` p. 10 ^fang2022anygrasp-040
- Human subjects achieved on average 1,000-1,200 mean picks per hour in the static bin-picking comparison. (Fang et al., 2022) `ev:measured` p. 10 ^fang2022anygrasp-041
- The D435 camera's depth presented a larger variance than the D415, with errors of up to ±5mm. (Fang et al., 2022) `ev:measured` p. 10 ^fang2022anygrasp-042
- The authors attribute AnyGrasp's robustness to depth sensing noise mainly to training data collected with real sensors. (Fang et al., 2022) `ev:asserted` p. 10 ^fang2022anygrasp-043
- On an adversarial set of 13 DexNet2.0 objects and 49 EGAD objects, AnyGrasp's grasp accuracy decreased. (Fang et al., 2022) `ev:measured` p. 10 ^fang2022anygrasp-044
- The authors attribute adversarial-object failures mainly to the system repeating failed trials without using feedback from each trial. (Fang et al., 2022) `ev:asserted` p. 10 ^fang2022anygrasp-045
- AnyGrasp guided a robot to clean fragments of a broken clay pot, which are usually less than 3mm thick. (Fang et al., 2022) `ev:measured` p. 11 ^fang2022anygrasp-046
- In each fish-catching trial, 8 robot fish were randomly placed in the fish tank for the robot to catch. (Fang et al., 2022) `ev:reported` p. 11 ^fang2022anygrasp-047
- The AnyGrasp system achieved an average success rate of 75.5% over the five fish-catching trials. (Fang et al., 2022) `ev:measured` p. 12 ^fang2022anygrasp-048
- A heuristic baseline that tracks the nearest grasp pose across frames achieved an average fish-catching success rate of 62.5%. (Fang et al., 2022) `ev:measured` p. 12 ^fang2022anygrasp-049
- On successful grasps, the nearest-target heuristic took 12.7% more time on average than AnyGrasp's temporal association. (Fang et al., 2022) `ev:measured` p. 12 ^fang2022anygrasp-050
- In nearly half of the fish-catching failure cases, the fish slipped away although the grasp pose was good. (Fang et al., 2022) `ev:measured` p. 12 ^fang2022anygrasp-051
- Correspondence switches between two close, similar fish injected noise into the pose buffer and led to wrong predicted future grasps. (Fang et al., 2022) `ev:measured` p. 12 ^fang2022anygrasp-052
- Overall, the AnyGrasp grasp perception system can run at 7 Hz on an Nvidia 2060 GPU. (Fang et al., 2022) `ev:measured` p. 12 ^fang2022anygrasp-053
- On GraspNet-1Billion, a model trained on simulated depth with Gaussian noise still showed a large performance gap to real-data training. (Fang et al., 2022) `ev:measured` p. 12 ^fang2022anygrasp-054
- The gap between simulation-trained and real-trained models widened on the novel test scenes, especially for high-score grasp poses. (Fang et al., 2022) `ev:measured` p. 12 ^fang2022anygrasp-055
- In real bin picking, the performance of the model trained on noisy simulated data decreased a lot compared to the original model. (Fang et al., 2022) `ev:measured` p. 12 ^fang2022anygrasp-056
- The simulation-trained model could not generate grasp poses for a scene when few objects remained on the plate. (Fang et al., 2022) `ev:measured` p. 12 ^fang2022anygrasp-057
- The authors conclude that the frequently adopted [[Sim-to-real transfer|sim-to-real technology]] in the grasping community is insufficient for their setting. (Fang et al., 2022) `ev:asserted` p. 12 ^fang2022anygrasp-058
- Without the stable score, 16 in-hand slippages occurred over 25 grasp attempts on a long, heavy test object. (Fang et al., 2022) `ev:measured` p. 13 ^fang2022anygrasp-059
- With the stable score, 11 in-hand slippages occurred over 25 grasp attempts on the same long, heavy object. (Fang et al., 2022) `ev:measured` p. 13 ^fang2022anygrasp-060
- GraspNet-1Billion generates over 10M grasp poses on each object, whereas Jacquard, DexNet 2.0 and EGAD generate 100. (Fang et al., 2022) `ev:cited` p. 13 ^fang2022anygrasp-061
- Downsampling grasp poses per object by 10 times degraded performance similarly to decreasing the number of training images. (Fang et al., 2022) `ev:measured` p. 13 ^fang2022anygrasp-062
- The authors suggest that densely annotated grasp poses are of equal importance to the number of training images. (Fang et al., 2022) `ev:asserted` p. 13 ^fang2022anygrasp-063
- Downsampling the scene dimension of the training data caused larger performance degradation on the test sets than other dimensions. (Fang et al., 2022) `ev:measured` p. 13 ^fang2022anygrasp-064
- The authors suggest that scene diversity might be more important for model training, after the 2-scene model failed to converge. (Fang et al., 2022) `ev:asserted` p. 14 ^fang2022anygrasp-065
- The authors argue that 6D object pose tracking cannot handle deformable objects, unlike tracking at the level of grasp poses. (Fang et al., 2022) `ev:asserted` p. 14 ^fang2022anygrasp-066
- The authors state that AnyGrasp's closed-loop grasping is fragile to occlusion of the grasp target by the approaching robot. (Fang et al., 2022) `ev:asserted` p. 14 ^fang2022anygrasp-067
- The authors state that their method cannot adjust the grasp pose using visual or tactile feedback after contact. (Fang et al., 2022) `ev:asserted` p. 14 ^fang2022anygrasp-068
- Test objects with a large portion of transparent or black surface were excluded, since depth sensors cannot predict them well. (Fang et al., 2022) `ev:reported` p. 15 ^fang2022anygrasp-069

## 🎯 Contributions

## 📖 Glossary

- **7-DoF grasp configuration** — Parallel-gripper grasp given by 3D rotation, 3D grasp centre and gripper width.
- **Stable score** — Normalized distance from gripper plane to object centre of gravity; lower is more stable.
- **Attempt-centric success rate** — Successful grasp attempts divided by total grasp attempts.
- **Object-centric success rate** — Successfully grasped objects divided by total objects; also called completion rate.
- **MPPH** — Mean picks per hour, a throughput measure for bin picking.
- **GSNet** — Graspness-based end-to-end grasp detection network on which AnyGrasp's geometry module builds.
- **Temporal association module** — Learns per-grasp feature vectors so grasps can be matched across frames.
- **Graspable FPS** — Farthest point sampling of seed points weighted by objectness and graspability.

## ❓ Open questions

- How can closed-loop grasp perception remain reliable when the gripper occludes the grasp target during approach?
- Can tactile feedback be combined with AnyGrasp to detect slip and adjust grasps in hand?
- Which sim-to-real techniques would close the gap the authors measured between simulated and real training data?
- How many and which training objects or scenes are actually necessary for general grasping?
- How well does the generation-association approach transfer to multi-fingered or other robotic hands?
- Can the future-pose prediction handle targets that change speed, the source of several fish-catching failures?
- How can transparent or black objects, excluded from the test set, be grasped with this pipeline?

## 📝 Notes on reading

The cached text is arXiv 2212.08333v2 (6 Jun 2023) carrying an IEEE Transactions on Robotics header; the packet venue says arXiv preprint.

Several results exist only as figures and were not claimed with numbers: the D435 vs D415 per-category success rates (Fig. 7b), the adversarial-set success rates for DexNet 4.0, AnyGrasp and humans (Fig. 8b), the sim vs real GraspNet AP curves (Fig. 13), the real bin-picking sim vs real bars (Fig. 14) and the data-downsampling AP curves (Fig. 16). Fig. 10b gives per-trial fish-catching rates (80.00%, 100.00%, 53.33%, 72.73%, 88.89%; average 75.47%), which the text rounds to 75.5%.

Table I also reports object-centric rates: DexNet 4.0 98.9%, AnyGrasp 99.8%, human 100.0%. The introduction reports success of over 93% and completion over 99.8%, consistent with Table I.

The training GPU is printed as Nvidia GTX 2080 Ti, and the grasp distance metric sets wmax = 0.01m, described as the maximum gripper width; both are reproduced as printed and may be typos in the paper. Equations (2)-(7) are partly garbled in the extraction but readable.

## Suggested new concepts

- Grasp pose tracking — tracking grasps rather than object 6D poses is a distinct approach to dynamic grasping.
- Center-of-mass aware grasping — AnyGrasp's stable score is one instance of a reusable idea for stable grasps.
- Sim-to-real gap in grasp learning — the paper gives direct evidence that real-data training outperforms noisy simulation.
- Dense grasp annotation — the trade-off between annotation density, image count and scene diversity deserves its own note.
- Attempt-centric vs object-centric success rate — two grasping metrics that are often conflated across papers.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Agarres densos con seguimiento temporal
