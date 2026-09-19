---
aliases: []
type: "source"
title: "CNS: Correspondence Encoded Neural Image Servo Policy"
citekey: "Chen2023cns"
doi: "10.48550/arXiv.2309.09047"
arxiv: "2309.09047"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2309.09047"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Anzhe Chen", "Hongxiang Yu", "Yue Wang", "Rong Xiong"]
sha256: ["d109af4794e5950e6d3b290edbd004d0c7fa701496abeeb41233e553e57c61b4"]
pdf: "Content/Papers/Chen2023cns.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Chen2023cns.pdf]]

> [!abstract] One-sentence summary
> CNS encodes matched keypoints as a graph and trains a graph-neural-network image servo policy purely in simulation, transferring to real scenes without fine-tuning with higher precision, convergence and mismatch robustness than IBVS and end-to-end baselines.

## Abstract

Image servo is an indispensable technique in robotic applications that helps to achieve high precision positioning. The intermediate representation of image servo policy is important to sensor input abstraction and policy output guidance. Classical approaches achieve high precision but require clean keypoint correspondence, and suffer from limited convergence basin or weak feature error robustness. Recent learning-based methods achieve moderate precision and large convergence basin on specific scenes but face issues when generalizing to novel environments. In this paper, we encode keypoints and correspondence into a graph and use graph neural network as architecture of controller. This design utilizes both advantages: generalizable intermediate representation from keypoint correspondence and strong modeling ability from neural network. Other techniques including realistic data generation, feature clustering and distance decoupling are proposed to further improve efficiency, precision and generalization. Experiments in simulation and real-world verify the effectiveness of our method in speed (maximum 40fps along with observer), precision (<0.3° and sub-millimeter accuracy) and generalization (sim-to-real without fine-tuning). Project homepage (full paper with supplementary text, video and code): https://hhcaz.github.io/CNS-home (arXiv)

## 🧠 Key ideas (atomic)

- [[Image-based visual servoing|Classical IBVS methods]] achieve high servo precision but suffer from a small convergence basin and erroneous correspondence, according to cited prior work. (Chen et al., 2023) `ev:cited` p. 1 ^chen2023cns-001
- [[Position-based visual servoing]], which estimates relative pose with an extra object model, suffers from imprecise object models and camera intrinsics. (Chen et al., 2023) `ev:cited` p. 1 ^chen2023cns-002
- [[Visual servoing|Implicit end-to-end servo methods]] reach precision comparable to IBVS in training scenes but generalize poorly to novel scenes. (Chen et al., 2023) `ev:cited` p. 1 ^chen2023cns-003
- The authors attribute the poor generalization of implicit end-to-end servo methods to spurious scene-specific features learned during training. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023cns-004
- CNS encodes keypoints and their correspondence between current and desired images as a graph processed by a graph neural network controller. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023cns-005
- CNS uses keypoint clustering and attentional aggregation to deal with erroneous correspondence between the current and desired images. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023cns-006
- The neural policy is supervised by [[Position-based visual servoing|PBVS]], which the authors state intrinsically has a larger convergence basin than [[Image-based visual servoing|IBVS]]. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023cns-007
- A graph convolutional gated recurrent unit implicitly models scene structure to improve convergence and robustness to intermittent correspondence. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023cns-008
- CNS predicts a distance decoupled velocity intended to prevent the policy overfitting to scenes of the specific scale used in training. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023cns-009
- The authors argue that keypoint correspondence isolates image appearance from the neural policy, so the model generalizes to novel scenes. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023cns-010
- The abstract reports that CNS runs at a maximum of 40fps when the keypoint observer is included in the loop. (Chen et al., 2023) `ev:abstract` p. 1 ^chen2023cns-011
- The policy trained in simulation can be transferred directly to novel real-world scenes without any fine-tuning. (Chen et al., 2023) `ev:measured` p. 2 ^chen2023cns-012
- CNS accepts matched keypoints from any detector-based feature matching method, such as SIFT, ORB, AKAZE or SuperGlue. (Chen et al., 2023) `ev:asserted` p. 2 ^chen2023cns-013
- A prior hyper-network servo method is not general enough because its keypoint number is fixed and it cannot handle missing keypoints. (Chen et al., 2023) `ev:cited` p. 2 ^chen2023cns-014
- The authors argue that pure convolution structures in end-to-end servo methods are translation invariant but unsuitable for estimating rotation. (Chen et al., 2023) `ev:cited` p. 2 ^chen2023cns-015
- Keypoints in the desired image are clustered with the Affinity-Propagation algorithm right after their extraction from that image. (Chen et al., 2023) `ev:reported` p. 2 ^chen2023cns-016
- Each cluster centre is chosen as the keypoint closest to the mean position of all keypoints in that cluster. (Chen et al., 2023) `ev:reported` p. 2 ^chen2023cns-017
- Graph edges come in two types, one for intra-cluster embedding aggregation and one for inter-cluster information mutation. (Chen et al., 2023) `ev:reported` p. 2 ^chen2023cns-018
- Keypoints whose correspondence is missing in the current pose are dropped from the index groups and the intra-cluster edges. (Chen et al., 2023) `ev:reported` p. 3 ^chen2023cns-019
- Clusters with no observed keypoints are dropped from the inter-cluster edges because their centre embeddings would be meaningless. (Chen et al., 2023) `ev:reported` p. 3 ^chen2023cns-020
- Without clustering, inter-cluster edges become densely connected, which the authors state consumes much memory and time with numerous keypoints. (Chen et al., 2023) `ev:asserted` p. 3 ^chen2023cns-021
- Attentional intra-cluster aggregation may lower the contribution of noisy and mismatched keypoints, which otherwise contribute equally to the control rate. (Chen et al., 2023) `ev:asserted` p. 3 ^chen2023cns-022
- Point-Transformer convolution aggregates intra-cluster keypoint features separately for the desired pose and for the current pose. (Chen et al., 2023) `ev:reported` p. 3 ^chen2023cns-023
- Two point-edge-residual convolution layers propagate information only among cluster centres, which reduces computing complexity with numerous keypoints. (Chen et al., 2023) `ev:asserted` p. 3 ^chen2023cns-024
- Unlike gated graph convolution, the proposed GConvGRU lets graph convolution directly participate in predicting the gates and the hidden state. (Chen et al., 2023) `ev:asserted` p. 3 ^chen2023cns-025
- The network predicts a velocity direction and a transformed norm, and a scalar distance prior scales the linear velocity. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023cns-026
- The norm transform is one plus ELU, decaying exponentially towards zero for negative inputs and behaving linearly for positive inputs. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023cns-027
- Supervision uses [[Position-based visual servoing|PBVS]] velocities whose linear part is divided by the ground-truth distance from scene centre to camera at the desired pose. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023cns-028
- The servo loss adds a cosine-similarity direction loss to a mean-squared-error norm loss weighted by 0.1. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023cns-029
- The graph representation lets training sample keypoints directly rather than render images, which the authors state enables faster training. (Chen et al., 2023) `ev:asserted` p. 4 ^chen2023cns-030
- Training keypoints are sampled in 3D as a union of bounded uniform distributions in elliptic cylinders, then projected to the image plane. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023cns-031
- Each keypoint receives an observable probability from three Gaussian kernels whose centres shift with camera motion along Perlin noise trajectories. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023cns-032
- Keypoints switch between observable and missing states through a kinetic Monte Carlo process with time constants drawn between 0.5 and 5. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023cns-033
- The Erender benchmark randomly places 8 to 12 YCB objects in each of 150 scenes rendered with the PyBullet engine. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023cns-034
- The Eaffine benchmark uses a single 2D image as the scene, so each rendered view is an affine transform of it. (Chen et al., 2023) `ev:reported` p. 5 ^chen2023cns-035
- In Eaffine the comparison runs started from an average initial rotation error of 44.69° and translation error of 284.6mm. (Chen et al., 2023) `ev:reported` p. 5 ^chen2023cns-036
- In Eaffine all compared models achieved a high success ratio, while CNS achieved the best servo precision among them. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023cns-037
- The authors attribute the limited precision of end-to-end baselines to coarse, repeatedly down-sampled features from a classification-pretrained CNN. (Chen et al., 2023) `ev:asserted` p. 5 ^chen2023cns-038
- In Erender the [[Image-based visual servoing|IBVS controller]] failed more often on scenes with a large initial rotation error between initial and desired poses. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023cns-039
- RAFT+IBVS performed worse than AKAZE+IBVS as initial rotation error increased, which the authors assume reflects RAFT training data. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023cns-040
- CNS succeeded in all Erender scenes and achieved the highest servo precision in most of those scenes. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023cns-041
- Without RANSAC outlier rejection, AKAZE+IBVS showed a significant performance drop in Erender, while CNS preserved a high success ratio. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023cns-042
- Real-world tests used Scene-Easy with 20 scattered objects and Scene-Hard with 3 objects that are often partially observed. (Chen et al., 2023) `ev:reported` p. 5 ^chen2023cns-043
- Real-world statistics came from 60 runs with an average initial rotation error of 86.56° and translation error of 148.8mm. (Chen et al., 2023) `ev:reported` p. 5 ^chen2023cns-044
- In Scene-Easy with RANSAC and SIFT observers, CNS reached a 100 success ratio against 98.33 percent for IBVS. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023cns-045
- In Scene-Easy with RANSAC, CNS reached a translation error of 0.308±0.162 mm, compared with 0.843±0.505 mm for IBVS. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023cns-046
- In Scene-Easy with RANSAC, CNS reached a rotation error of 0.053±0.046 degrees, compared with 0.147±0.088 degrees for IBVS. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023cns-047
- In Scene-Easy without RANSAC, the [[Image-based visual servoing|IBVS]] success ratio fell to 8.33 percent while CNS still reached 75.00 percent. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023cns-048
- In Scene-Hard with RANSAC, CNS reached a 96.67 percent success ratio compared with 70.00 percent for IBVS. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023cns-049
- CNS generated smoother trajectories than IBVS in the sampled real-world success cases shown for the Scene-Hard setup. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023cns-050
- Replacing PTConv with a point-wise MLP raised mean controller time per frame from 11.5 to 67.4 ms in Erender. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023cns-051
- Removing clustering increased the Erender translation error of CNS from 1.39±1.40 mm to 9.29±9.18 mm in the ablation. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023cns-052
- Compared with variants without GConvGRU or using GGNN, the base model improves precision by over 50% in Erender. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023cns-053
- The GConvGRU base model costs a slight increase of about 10% in network inference time over its ablated variants. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023cns-054
- The authors report that CNS achieves <0.3° and sub-millimeter servo precision in their real-world experiments. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023cns-055
- The authors conclude CNS generalizes better than learning-based methods because explicit guidance suppresses correlation between image appearance and policy. (Chen et al., 2023) `ev:asserted` p. 6 ^chen2023cns-056
- Training samples between 4 and 512 keypoints per scene, with a maximum scene size of 0.2m. (Chen et al., 2023) `ev:reported` p. 8 ^chen2023cns-057
- In real-world experiments, desired camera poses lay 0.25m to 0.3m from the scene centre because of the arm's limited workspace. (Chen et al., 2023) `ev:reported` p. 8 ^chen2023cns-058
- Among five observers tested in Erender, AKAZE and SuperGlue gave the best success ratio for the CNS controller. (Chen et al., 2023) `ev:measured` p. 9 ^chen2023cns-059
- SIFT gave the highest servo precision among observers, with a translation error of 1.379±1.263 mm. (Chen et al., 2023) `ev:measured` p. 9 ^chen2023cns-060
- ORB was the fastest observer, with a mean total time per frame of 25.62 ms against 56.60 ms for AKAZE. (Chen et al., 2023) `ev:measured` p. 9 ^chen2023cns-061
- CNS trained with perfect keypoint correspondences achieved a convergence rate of only 95.33% in the data generation ablation. (Chen et al., 2023) `ev:measured` p. 9 ^chen2023cns-062
- Combining weighted keypoint dropout, clustered keypoint distribution and keypoint mismatch gave the highest convergence rate and precision among data settings. (Chen et al., 2023) `ev:measured` p. 9 ^chen2023cns-063
- The authors state that keypoint mismatch augmentation, which mimics correspondence quality in actual use, is important for generalization. (Chen et al., 2023) `ev:asserted` p. 9 ^chen2023cns-064
- With distance decoupled velocity, the success ratio stayed at 98.67 or higher when scenes were scaled by x0.2 or x5.0. (Chen et al., 2023) `ev:measured` p. 10 ^chen2023cns-065
- Without any distance prior, the success ratio fell to 74.00 at scale x0.2 because the controller moved relatively too fast. (Chen et al., 2023) `ev:measured` p. 10 ^chen2023cns-066
- A model taking the distance prior as an input feature reached a 61.33 success ratio at scale x0.2, worse than without the prior. (Chen et al., 2023) `ev:measured` p. 10 ^chen2023cns-067
- Underestimating the distance prior as 0.25m kept full success but raised time steps to convergence from 207.8 to 432.9. (Chen et al., 2023) `ev:measured` p. 10 ^chen2023cns-068
- Overestimating the distance prior as 2.00m lowered the success ratio to 80.00, as objects may easily move out of view. (Chen et al., 2023) `ev:measured` p. 10 ^chen2023cns-069

## 🎯 Contributions

## 📖 Glossary

- **IBVS** — Image-based visual servoing: velocity control derived directly from image keypoint errors.
- **PBVS** — Position-based visual servoing: control from estimated relative camera pose, needing object models.
- **Convergence basin** — Range of initial pose deviations from which a servo controller still reaches the target.
- **Distance decoupled velocity** — Velocity with linear part normalized by scene distance, rescaled by a scalar prior.
- **GConvGRU** — Graph convolutional GRU whose gates and candidate state are computed by graph convolution.
- **PERConv** — Point-edge-residual convolution used to exchange information among cluster-centre nodes.
- **Keypoint dropout** — Training augmentation that randomly hides keypoints to mimic missing correspondences.
- **Distance prior** — Rough scalar estimate of camera-to-scene distance used to scale predicted linear velocity.

## ❓ Open questions

- How does CNS perform when the observer yields very few keypoints, such as textureless or reflective scenes?
- Can the distance prior be estimated online instead of supplied, avoiding the failure mode under overestimation?
- Does the simulated keypoint distribution cover dynamic scenes or deformable objects, not only static rigid clutter?
- Would a learned observer trained jointly with the graph policy improve precision beyond off-the-shelf matchers?
- How does CNS behave on robots with slower control rates than the 0.04s time step used here?

## 📝 Notes on reading

Read the arXiv v1 preprint (2309.09047v1, 16 Sep 2023), which includes the supplementary material on pages 8 to 10. Fig. 5 (Eaffine and Erender comparisons with [11], [13] and IBVS variants) is a bar chart whose per-method values are not in the extracted text; only its caption statistics (initial RE/TE, success thresholds) were claimed. The Fig. 2 caption speaks of 7 keypoints while the case illustration text says 6 keypoints but lists indices 0 to 6. Supplementary section D says the comparison with [11], [13] used Erender (Fig. 9b), whereas the main text and Fig. 9b name it Eaffine. Section F defines WKD as similar to UDK, a typo for UKD. Real-world rotation errors printed as degrees were written out in words in the claims. The matrices in Eq. 1 and Eq. 2 are garbled in the extraction and were not claimed.

## Suggested new concepts

- Graph-based visual servoing — encoding keypoint correspondence as a graph for learned controllers recurs in servoing literature.
- Distance decoupled velocity — a scale-generalization trick relevant to any learned velocity controller.
- Sim-to-real keypoint randomization — simulating keypoint dropout and mismatch instead of rendering images is a reusable training strategy.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H5.** Servo visual con GNN sobre grafos de correspondencias, entrenado solo en simulación y transferido sin ajuste al robot real.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
