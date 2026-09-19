---
aliases: []
type: "source"
title: "SE(3)-DiffusionFields"
citekey: "Urain2022se"
doi: "10.48550/arXiv.2209.03855"
arxiv: "2209.03855"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2209.03855"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Julen Urain", "Niklas Funk", "Jan Peters", "Georgia Chalvatzaki"]
sha256: ["a08c6a54bed308ed55b04cf8b476c60616af94a01946d7949bcdfe253b6c664f"]
pdf: "Content/Papers/Urain2022se.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 65
---

📄 PDF: [[Urain2022se.pdf]]

> [!abstract] One-sentence summary
> The paper learns 6DoF grasp distributions as smooth SE(3) diffusion-model energy fields and uses them as cost terms in a single gradient-based inverse-diffusion optimization that jointly selects grasp and trajectory, outperforming decoupled grasp-then-plan pipelines in simulation and on a real robot.

## Abstract

Multi-objective optimization problems are ubiquitous in robotics, e.g., the optimization of a robot manipulation task requires a joint consideration of grasp pose configurations, collisions and joint limits. While some demands can be easily hand-designed, e.g., the smoothness of a trajectory, several task-specific objectives need to be learned from data. This work introduces a method for learning data-driven SE(3) cost functions as diffusion models. Diffusion models can represent highly-expressive multimodal distributions and exhibit proper gradients over the entire space due to their score-matching training objective. Learning costs as diffusion models allows their seamless integration with other costs into a single differentiable objective function, enabling joint gradient-based motion optimization. In this work, we focus on learning SE(3) diffusion models for 6DoF grasping, giving rise to a novel framework for joint grasp and motion optimization without needing to decouple grasp selection from trajectory generation. We evaluate the representation power of our SE(3) diffusion models w.r.t. classical generative models, and we showcase the superior performance of our proposed optimization framework in a series of simulated and real-world robotic manipulation tasks against representative baselines. (arXiv)

## 🧠 Key ideas (atomic)

- Data-driven models are usually integrated into motion optimization either as explicit sampling generators or as scalar cost fields. (Urain et al., 2022) `ev:cited` p. 1 ^urain2022se-001
- Explicit generators do not allow direct composition with other objectives, requiring two or even more separate phases during optimization. (Urain et al., 2022) `ev:cited` p. 1 ^urain2022se-002
- In decoupled pipelines, sampled grasps might be unfeasible for the problem, leading to an unsolvable trajectory optimization problem. (Urain et al., 2022) `ev:asserted` p. 1 ^urain2022se-003
- Cost functions learned through cross-entropy or contrastive divergence create large plateaus with zero or noisy slopes, making them unsuitable for gradient-based optimization. (Urain et al., 2022) `ev:cited` p. 1 ^urain2022se-004
- The authors propose learning smooth data-driven SE(3) cost functions, meaning costs that expose informative gradients in the entire space, inspired by diffusion models. (Urain et al., 2022) `ev:asserted` p. 1 ^urain2022se-005
- The authors state that [[Diffusion models on Lie groups|SE(3) diffusion models]] better cover multimodal distributions, leading to better and more sample efficient subsequent robot planning. (Urain et al., 2022) `ev:asserted` p. 2 ^urain2022se-006
- The authors state that score-based modeling was previously introduced for arbitrary Riemannian manifolds, whereas this work focuses on the Lie group SE(3). (Urain et al., 2022) `ev:asserted` p. 2 ^urain2022se-007
- The authors state that a grasp classifier trained with cross-entropy loss would not resolve the joint optimization problem due to its lack of smoothness. (Urain et al., 2022) `ev:asserted` p. 2 ^urain2022se-008
- A [[Diffusion models on Lie groups|diffusion model in SE(3)]] is a vector field that outputs a vector in R6 for any query pose, conditioned on a noise scale. (Urain et al., 2022) `ev:reported` p. 3 ^urain2022se-009
- Perturbed training grasp poses are obtained by multiplying a data pose with the exponential map of a Gaussian white noise vector. (Urain et al., 2022) `ev:reported` p. 3 ^urain2022se-010
- The derivatives of the perturbed distribution with respect to SE(3) elements are computed by automatic differentiation using the Theseus library with PyTorch. (Urain et al., 2022) `ev:reported` p. 3 ^urain2022se-011
- The inverse Langevin diffusion is adapted to SE(3) by applying each update through the exponential map, keeping samples on the manifold. (Urain et al., 2022) `ev:reported` p. 3 ^urain2022se-012
- Instead of a score vector field, SE(3)-DiF learns a scalar energy field whose negative SE(3) derivative is taken as the score function. (Urain et al., 2022) `ev:reported` p. 3 ^urain2022se-013
- The authors argue that learning an energy-based model allows evaluating generated sample quality and composing it with other cost functions. (Urain et al., 2022) `ev:asserted` p. 3 ^urain2022se-014
- The grasp model assumes access to the object pose, deferring perception of object pose and shape from point clouds to future work. (Urain et al., 2022) `ev:reported` p. 3 ^urain2022se-015
- The model is trained to jointly match the object's signed distance field and predict the grasp energy through the denoising score matching loss. (Urain et al., 2022) `ev:reported` p. 3 ^urain2022se-016
- Object shapes are represented by learnable shape codes retrieved from the object index, following the DeepSDF autodecoder approach. (Urain et al., 2022) `ev:reported` p. 3 ^urain2022se-017
- Each grasp pose is expressed as a fixed set of N 3D points around the gripper, then transformed into the object's local frame. (Urain et al., 2022) `ev:reported` p. 4 ^urain2022se-018
- A feature encoder conditioned on the shape code and noise level outputs per-point SDF predictions plus a set of additional features. (Urain et al., 2022) `ev:reported` p. 4 ^urain2022se-019
- The flattened per-point features are passed through a decoder network that outputs the scalar energy value of the grasp pose. (Urain et al., 2022) `ev:reported` p. 4 ^urain2022se-020
- Training sums the denoising score matching loss with an SDF mean squared error loss, jointly updating shape codes, encoder and decoder. (Urain et al., 2022) `ev:reported` p. 4 ^urain2022se-021
- Motion optimization seeks the trajectory minimizing a weighted sum of costs, where the learned grasp SE(3)-DiF is one cost term. (Urain et al., 2022) `ev:reported` p. 4 ^urain2022se-022
- The learned SE(3) energy is turned into a joint-space cost by composing it with the robot's forward kinematics to the end-effector. (Urain et al., 2022) `ev:reported` p. 4 ^urain2022se-023
- Trajectory generation is framed as an inverse Langevin diffusion evolving random trajectory particles toward a target distribution proportional to exp(-J). (Urain et al., 2022) `ev:reported` p. 4 ^urain2022se-024
- After the inverse diffusion, the trajectory particles are evaluated on the objective and the one with the lowest cost is chosen. (Urain et al., 2022) `ev:reported` p. 4 ^urain2022se-025
- The authors hypothesize that jointly optimizing over grasp pose and trajectory is more sample efficient than decoupled grasp and motion approaches. (Urain et al., 2022) `ev:asserted` p. 4 ^urain2022se-026
- The grasp model is trained on [[ACRONYM dataset|Acronym]] successful grasp poses for 90 different mugs, approximately 90K 6DoF grasp poses in total. (Urain et al., 2022) `ev:reported` p. 5 ^urain2022se-027
- Grasp generation is evaluated on 90 different mugs with 200 generated grasps per mug, measuring grasp success in Nvidia Isaac Gym. (Urain et al., 2022) `ev:reported` p. 5 ^urain2022se-028
- The grasp generation baselines are a VAE with classifier-based MCMC refinement, the VAE alone, and classifier MCMC from random initial poses. (Urain et al., 2022) `ev:reported` p. 5 ^urain2022se-029
- In grasp success rate, SE(3)-DiF outperforms the VAE+Refine baseline slightly, especially yielding lower variance, in the mug grasp generation experiment. (Urain et al., 2022) `ev:measured` p. 5 ^urain2022se-030
- In grasp success rate, SE(3)-DiF significantly outperforms both the VAE alone and the classifier alone in the mug grasp generation experiment. (Urain et al., 2022) `ev:measured` p. 5 ^urain2022se-031
- In the grasp generation experiment, the VAE alone generates noisy grasp poses that are often in collision with the mug. (Urain et al., 2022) `ev:measured` p. 5 ^urain2022se-032
- The authors hypothesize the classifier's low success might relate to large plateaus with close to zero slopes in regions far from good samples. (Urain et al., 2022) `ev:asserted` p. 5 ^urain2022se-033
- In grasp diversity measured by Earth Mover Distance, where lower is better, SE(3)-DiF outperforms all three baselines significantly. (Urain et al., 2022) `ev:measured` p. 5 ^urain2022se-034
- The authors suggest a reason for the diversity difference might be that VAE+Refine overfits to specific overrepresented modes of the data distribution. (Urain et al., 2022) `ev:asserted` p. 5 ^urain2022se-035
- In the picking amidst clutter task, success is measured by the robot being able to grasp the object at the end of execution. (Urain et al., 2022) `ev:reported` p. 5 ^urain2022se-036
- The motion baselines are a decoupled grasp sampling then CHOMP pipeline, the OMG-Planner, and joint optimization using a grasp classifier as cost. (Urain et al., 2022) `ev:reported` p. 5 ^urain2022se-037
- The proposed joint optimization requires 25 particles to match the success rate of the decoupled approach with 800 particles. (Urain et al., 2022) `ev:measured` p. 6 ^urain2022se-038
- The authors attribute this efficiency gap to the decoupled approach generating grasp poses that are infeasible given clutter or joint limits. (Urain et al., 2022) `ev:asserted` p. 6 ^urain2022se-039
- When a grasp classifier is used as cost term instead of SE(3)-DiF, the motion optimization problem is unable to find solutions. (Urain et al., 2022) `ev:measured` p. 6 ^urain2022se-040
- In real robot experiments, 800 trajectory particles are initialized for optimization and only the one with lowest cost is executed. (Urain et al., 2022) `ev:reported` p. 6 ^urain2022se-041
- In the real experiments, the mug pose is retrieved from an external Optitrack system, which induces small calibration errors. (Urain et al., 2022) `ev:reported` p. 6 ^urain2022se-042
- Real-world picking of a mug from various poses without clutter achieved 100% (20 successes / 20 trials) pickup success. (Urain et al., 2022) `ev:measured` p. 6 ^urain2022se-043
- Real-world picking of mugs initially placed upside down achieved 90% (18/20) success with the joint grasp and motion optimization. (Urain et al., 2022) `ev:measured` p. 6 ^urain2022se-044
- Real-world picking in occluded scenes achieved 95% (19/20) success with the joint grasp and motion optimization framework. (Urain et al., 2022) `ev:measured` p. 6 ^urain2022se-045
- Real-world picking and placing the mug in a desired pose inside the shelf achieved 100% (20/20) success. (Urain et al., 2022) `ev:measured` p. 6 ^urain2022se-046
- The authors attribute the higher real-world performance to a simpler real scene, since simulated flying obstacles were not realizable in reality. (Urain et al., 2022) `ev:asserted` p. 6 ^urain2022se-047
- As a limitation, the experiments assumed full object state knowledge, without relying on complex perception systems for the grasped objects. (Urain et al., 2022) `ev:reported` p. 6 ^urain2022se-048
- The authors note that hand-designed cost terms may not capture the relevant task description well in more complex scenarios. (Urain et al., 2022) `ev:asserted` p. 6 ^urain2022se-049
- The authors state that weighting the cost terms becomes more difficult as the number of cost terms increases. (Urain et al., 2022) `ev:asserted` p. 6 ^urain2022se-050
- As future work, the authors want to explore diffusion models for reactive motion control in robot manipulation. (Urain et al., 2022) `ev:asserted` p. 7 ^urain2022se-051
- The authors also want to explore composing multiple diffusion models to solve complex manipulation tasks with multiple hard-to-model objectives. (Urain et al., 2022) `ev:asserted` p. 7 ^urain2022se-052
- A generated grasp is counted as successful if, after closing the fingers and lifting, the mug remains close to the gripper. (Urain et al., 2022) `ev:reported` p. 13 ^urain2022se-053
- The Earth Mover Distance is computed on N = 1000 poses per distribution by solving a linear sum assignment over SE(3) pose distances. (Urain et al., 2022) `ev:reported` p. 13 ^urain2022se-054
- The classifier baseline shares the SE(3)-DiF architecture and was trained with cross-entropy plus a gradient regularizer encouraging smoother gradients. (Urain et al., 2022) `ev:reported` p. 13 ^urain2022se-055
- For robot grasp pose generation with upright objects, the overall particle success ratio was 0.62 for SE(3)-DiF versus 0.03 for classifier joint optimization. (Urain et al., 2022) `ev:measured` p. 14 ^urain2022se-056
- For flipped objects, the overall particle success ratio was 0.49 for joint SE(3)-DiF optimization versus 0.12 for sample-then-optimize with ten samples. (Urain et al., 2022) `ev:measured` p. 14 ^urain2022se-057
- The s1 success of the proposed joint optimization stays at 0.88 for both upright and flipped objects in the robot grasp experiment. (Urain et al., 2022) `ev:measured` p. 14 ^urain2022se-058
- In picking with occlusions, success in all cases increases when more initial trajectory particles are used for the gradient-based optimization. (Urain et al., 2022) `ev:measured` p. 16 ^urain2022se-059
- In picking with occlusions, the joint optimization approach outperforms the hierarchical sample-then-optimize approach in all the evaluated cases. (Urain et al., 2022) `ev:measured` p. 16 ^urain2022se-060
- The pointcloud variant PoiNt-SE(3)-DiF replaces shape codes with a VN-PointNet encoder that outputs SO(3)-equivariant features from the input pointcloud. (Urain et al., 2022) `ev:reported` p. 18 ^urain2022se-061
- The best success rate and Earth Mover Distance were achieved by SE(3)-DiF with known pose, followed by SE(3)-DiF (Rot) and PoiNt-SE(3)-DiF. (Urain et al., 2022) `ev:measured` p. 19 ^urain2022se-062
- SE(3)-DiF (Z+Rot), which infers both shape code and pose from pointclouds, was not able to achieve a high success rate. (Urain et al., 2022) `ev:measured` p. 19 ^urain2022se-063
- All diffusion-based variants except SE(3)-DiF (Z+Rot) outperformed 6DoF-GraspNet in terms of both success rate and Earth Mover Distance. (Urain et al., 2022) `ev:measured` p. 19 ^urain2022se-064
- The authors infer that 6DoF-GraspNet samples are less diverse, collapsing to some dataset modes without covering them all. (Urain et al., 2022) `ev:asserted` p. 19 ^urain2022se-065

## 🎯 Contributions

## 📖 Glossary

- **SE(3)** — Lie group of 3D rigid-body poses combining rotation and translation.
- **Denoising Score Matching (DSM)** — Trains a model to match the score of noise-perturbed data distributions.
- **Annealed Langevin MCMC** — Sampling by noisy gradient steps over decreasing noise scales toward the data distribution.
- **Expmap / Logmap** — Maps between the SE(3) group and its R6 tangent vector representation.
- **Energy-based model (EBM)** — Model outputting a scalar energy whose negative gradient gives the score.
- **Earth Mover Distance (EMD)** — Optimal-transport divergence between two empirical sample distributions; lower means closer.
- **Signed distance field (SDF)** — Function giving the signed distance from a point to an object surface.
- **Decoupled grasp and motion planning** — Sampling a grasp first, then planning a trajectory to reach it.

## ❓ Open questions

- How does joint grasp and motion optimization with SE(3)-DiF degrade under real perception noise instead of known object pose and shape?
- Can cost-term weights be tuned automatically as the number of learned and hand-designed costs grows?
- Why does joint inference of shape code and pose from pointclouds (Z+Rot) fail, and can it be fixed?
- Does composing several learned diffusion cost fields remain tractable for long-horizon manipulation?
- How does the approach scale to cluttered real scenes with obstacles comparable to the simulated flying obstacles?

## 📝 Notes on reading

- Version read is arXiv v4 (18 Jun 2023), which includes appendices (pp. 10–19); the registry year is 2022.
- Fig. 4 (grasp success and EMD bars), Fig. 5 (success vs number of particles for four methods), Fig. 10 and Fig. 12 could only be described; their numeric values are not in the cached text, except the 25 vs 800 particle comparison stated on p. 6.
- Sec. IV-A (p. 5) says grasp success is evaluated in Nvidia Isaac Gym, while the appendix (p. 13) and Fig. 7 mention Nvidia Isaac Sim for the same evaluation.
- The caption of Fig. 12 reads "Evaluation of the Success for picking with occlusions" although the figure reports the pointcloud grasp generation experiment; likely a copied caption.
- Table I (p. 14) gives sΩ (ratio of successful particles) and s1 (best-particle success) with ns = 100 initial samples; only headline rows were claimed.
- Simulated success numbers for the pick-and-reorient and shelf pick-and-place tasks are not given in the text; only their cost weights (Tables IV and V) appear.

## Suggested new concepts

- SE(3) diffusion models — a reusable way to learn smooth pose-space cost fields on Lie groups.
- Joint grasp and motion optimization — contrasts with decoupled grasp-then-plan pipelines across several papers.
- Motion planning as inverse diffusion — links planning-as-inference with Langevin sampling of trajectories.
- Learned cost functions for trajectory optimization — composable data-driven costs alongside hand-designed ones.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Difusión en $SE(3)$ como coste de agarre + trayectoria (C.5).
