---
aliases: []
type: "source"
title: "Reactive Motion Generation on Learned Riemannian Manifolds"
citekey: "BeikMohammadi2022reactive"
doi: "10.48550/arXiv.2203.07761"
arxiv: "2203.07761"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2203.07761"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Hadi Beik-Mohammadi", "Søren Hauberg", "Georgios Arvanitidis", "Gerhard Neumann", "Leonel Rozo"]
sha256: ["2684673c93b0ca7939a1b9991be34747bc5df14d6f2ba5b6f17fc3996b749d25"]
pdf: "Content/Papers/BeikMohammadi2022reactive.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[BeikMohammadi2022reactive.pdf]]

> [!abstract] One-sentence summary
> The paper learns a Riemannian metric from human demonstrations with a VAE (task space or joint space with a forward kinematics layer) and generates robot motions as geodesics, reshaping the metric with obstacle-aware ambient metrics for real-time end-effector or multiple-limb obstacle avoidance and hybrid multiple-solution trajectories on a 7-DoF arm.

## Abstract

In recent decades, advancements in motion learning have enabled robots to acquire new skills and adapt to unseen conditions in both structured and unstructured environments. In practice, motion learning methods capture relevant patterns and adjust them to new conditions such as dynamic obstacle avoidance or variable targets. In this paper, we investigate the robot motion learning paradigm from a Riemannian manifold perspective. We argue that Riemannian manifolds may be learned via human demonstrations in which geodesics are natural motion skills. The geodesics are generated using a learned Riemannian metric produced by our novel variational autoencoder (VAE), which is especially intended to recover full-pose end-effector states and joint space configurations. In addition, we propose a technique for facilitating on-the-fly end-effector/multiple-limb obstacle avoidance by reshaping the learned manifold using an obstacle-aware ambient metric. The motion generated using these geodesics may naturally result in multiple-solution tasks that have not been explicitly demonstrated previously. We extensively tested our approach in task space and joint space scenarios using a 7-DoF robotic manipulator. We demonstrate that our method is capable of learning and generating motion skills based on complicated motion patterns demonstrated by a human operator. Additionally, we assess several obstacle avoidance strategies and generate trajectories in multiple-mode settings. (arXiv)

## 🧠 Key ideas (atomic)

- The paper presents a learning-from-demonstration approach that learns Riemannian manifolds from human demonstrations, over which geodesic curves are computed and used as a motion generator. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 18 ^beikmohammadi2022reactive-001
- The authors position their reactive motion generation as a middle ground between classical motion planning and movement primitives learned from demonstrations. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 2 ^beikmohammadi2022reactive-002
- This work extends the authors' earlier task-space Riemannian approach to joint space skills through a new VAE architecture integrating the robot's forward kinematics. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 2 ^beikmohammadi2022reactive-003
- Following prior work, the VAE-induced Riemannian metric sums pulled-back Jacobian products of both the decoder mean and the decoder variance networks. (Beik-Mohammadi et al., 2022) `ev:cited` p. 4 ^beikmohammadi2022reactive-004
- The authors describe retraining the VAE with new data to reshape the metric as time-consuming, data-intensive and executable only offline. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 5 ^beikmohammadi2022reactive-005
- The learned metric is reshaped with a problem-specific ambient metric so that geodesics are repelled from chosen regions of the ambient space. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 5 ^beikmohammadi2022reactive-006
- For task space, end-effector position and orientation are assumed conditionally independent given the latent variable, which captures their correlation. (Beik-Mohammadi et al., 2022) `ev:reported` p. 6 ^beikmohammadi2022reactive-007
- Orientations are unit quaternions modelled by a mixture of two antipodal von Mises-Fisher distributions, giving q and its negative equal density. (Beik-Mohammadi et al., 2022) `ev:reported` p. 6 ^beikmohammadi2022reactive-008
- The task-space ELBO uses scaling factors β1 and β2 to balance position and orientation log-likelihoods, an idea inspired by the β-VAE method. (Beik-Mohammadi et al., 2022) `ev:reported` p. 6 ^beikmohammadi2022reactive-009
- Training data are doubled by including each quaternion observation and its antipode, so no pre-processing of orientation signs is required. (Beik-Mohammadi et al., 2022) `ev:reported` p. 7 ^beikmohammadi2022reactive-010
- Because the task-space manifold is learned from task-space data, the model is kinematics agnostic and usable across robots when trajectories are reachable. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 7 ^beikmohammadi2022reactive-011
- RBF networks represent the variance so that the Riemannian metric takes large values in regions with little or no data. (Beik-Mohammadi et al., 2022) `ev:reported` p. 7 ^beikmohammadi2022reactive-012
- A manifold learned from joint space demonstrations is kinematics-dependent, so generated motions cannot be directly transferred to robots with different kinematics. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 7 ^beikmohammadi2022reactive-013
- The joint-space ELBO uses the change of variable theorem with a forward kinematics volume measure to transform densities from joint to task space. (Beik-Mohammadi et al., 2022) `ev:reported` p. 7 ^beikmohammadi2022reactive-014
- The [[Pullback metric|joint-space pullback metric]] composes the forward kinematics Jacobian with the Jacobians of the decoder mean and variance networks. (Beik-Mohammadi et al., 2022) `ev:reported` p. 8 ^beikmohammadi2022reactive-015
- Geodesics are penalized for crossing regions of growing VAE predictive uncertainty, so they tend to stay on the learned manifold. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 9 ^beikmohammadi2022reactive-016
- Under a Euclidean metric, geodesics correspond to straight lines, which the authors say neglect the geometry of the data manifold. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 9 ^beikmohammadi2022reactive-017
- In the synthetic R2 × S2 example, Riemannian geodesics stay within the data boundary whereas Euclidean geodesics fail to stay in the data manifold. (Beik-Mohammadi et al., 2022) `ev:measured` p. 9 ^beikmohammadi2022reactive-018
- In the 2-DOF joint space toy example, the two latent clusters arise from the two different inverse-kinematics solutions in the demonstrations. (Beik-Mohammadi et al., 2022) `ev:measured` p. 10 ^beikmohammadi2022reactive-019
- The authors state that frequent switching among latent clusters may lead to jerky geodesics, particularly in robots with a high degree of freedom. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 10 ^beikmohammadi2022reactive-020
- The task-space obstacle ambient metric adds a Gaussian-shaped cost around the obstacle position, scaled by ζ and shaped by the obstacle radius. (Beik-Mohammadi et al., 2022) `ev:reported` p. 10 ^beikmohammadi2022reactive-021
- The authors emphasize that the obstacle-aware ambient metric makes geodesics generally avoid the obstacle but acts only as a soft constraint. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 10 ^beikmohammadi2022reactive-022
- As an obstacle changes position, the VAE does not need to be retrained because only the ambient metric changes. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 10 ^beikmohammadi2022reactive-023
- The authors state that, under the task space setting, obstacles can be avoided only by the robot end-effector. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 10 ^beikmohammadi2022reactive-024
- For joint-space avoidance, the forward kinematics layer gives task-space positions of robot body points, whose ambient metrics form a block-diagonal metric. (Beik-Mohammadi et al., 2022) `ev:reported` p. 11 ^beikmohammadi2022reactive-025
- In the authors' experiments, gradient descent on curve length often got trapped in local minima depending on a non-trivial initialization. (Beik-Mohammadi et al., 2022) `ev:measured` p. 12 ^beikmohammadi2022reactive-026
- Geodesics are computed by discretizing the latent space on a uniform grid with Riemannian edge weights and running Dijkstra's algorithm. (Beik-Mohammadi et al., 2022) `ev:reported` p. 12 ^beikmohammadi2022reactive-027
- The graph-based geodesic approach is feasible only in low-dimensional latent spaces because graph memory grows exponentially with dimension. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 12 ^beikmohammadi2022reactive-028
- A cubic spline is fitted to the Dijkstra node sequence by minimizing the mean square error to obtain a smooth trajectory. (Beik-Mohammadi et al., 2022) `ev:reported` p. 12 ^beikmohammadi2022reactive-029
- In a toy comparison, the geodesic from the 50 × 50 grid showed an unnecessary deviation from the data, likely due to low resolution. (Beik-Mohammadi et al., 2022) `ev:measured` p. 12 ^beikmohammadi2022reactive-030
- In the same toy comparison, the 100 × 100 grid geodesic reached accuracy comparable to the continuous gradient descent geodesic. (Beik-Mohammadi et al., 2022) `ev:measured` p. 12 ^beikmohammadi2022reactive-031
- For dynamic obstacles, a decoded copy of the latent graph is kept in memory and the weights of points near obstacles are rescaled. (Beik-Mohammadi et al., 2022) `ev:reported` p. 12 ^beikmohammadi2022reactive-032
- Demonstrations were recorded by kinesthetic teaching at 10Hz on a 7-DOF Franka Emika Panda arm with a two-finger gripper. (Beik-Mohammadi et al., 2022) `ev:reported` p. 12 ^beikmohammadi2022reactive-033
- Geodesics were calculated on 100 × 100 graphs in the task space setting and on 50 × 50 × 50 graphs in joint space. (Beik-Mohammadi et al., 2022) `ev:reported` p. 12 ^beikmohammadi2022reactive-034
- The authors report that their Python implementation runs at 100Hz on ordinary PC hardware and readily runs in real time. (Beik-Mohammadi et al., 2022) `ev:measured` p. 13 ^beikmohammadi2022reactive-035
- Obstacles were simulated with a digital twin of the robot, since no obstacle localization system was integrated into the setups. (Beik-Mohammadi et al., 2022) `ev:reported` p. 13 ^beikmohammadi2022reactive-036
- The task-space VAE encoder and decoder each have two hidden layers of 200 and 100 units, encoding the 7-dimensional pose into 2 latent dimensions. (Beik-Mohammadi et al., 2022) `ev:reported` p. 13 ^beikmohammadi2022reactive-037
- Position variance and quaternion concentration are estimated by RBF decoder networks with 500 kernels computed by k-means over the training dataset. (Beik-Mohammadi et al., 2022) `ev:reported` p. 13 ^beikmohammadi2022reactive-038
- The authors state that manually providing antipodal quaternions during training leads to better latent space structures and reconstruction accuracy. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 13 ^beikmohammadi2022reactive-039
- The joint-space VAE uses a 3-dimensional latent space and a fixed forward kinematics layer implemented with the PyKDL library. (Beik-Mohammadi et al., 2022) `ev:reported` p. 13 ^beikmohammadi2022reactive-040
- The joint-space obstacle metric considers all robot joints plus the end-effector, but not points on the links between joints. (Beik-Mohammadi et al., 2022) `ev:reported` p. 14 ^beikmohammadi2022reactive-041
- In the task-space reach-to-grasp task, the decoded geodesic reproduced the demonstrated 90° end-effector rotation when approaching the object. (Beik-Mohammadi et al., 2022) `ev:measured` p. 14 ^beikmohammadi2022reactive-042
- A geodesic designed to cross between the two antipodal latent clusters flipped the sign of the decoded end-effector quaternion. (Beik-Mohammadi et al., 2022) `ev:measured` p. 14 ^beikmohammadi2022reactive-043
- The blue and yellow reach-to-grasp geodesics had average energies of 7.50 and 10.51, far below the cluster-crossing green geodesic. (Beik-Mohammadi et al., 2022) `ev:measured` p. 14 ^beikmohammadi2022reactive-044
- The pouring task involves 3 bottles and 3 cups, so all 9 grasp-and-pour permutations are feasible from crossing demonstrations. (Beik-Mohammadi et al., 2022) `ev:reported` p. 14 ^beikmohammadi2022reactive-045
- In the task-space pouring task, geodesics avoided a moving spherical obstacle at different time frames while following the manifold geometry. (Beik-Mohammadi et al., 2022) `ev:measured` p. 15 ^beikmohammadi2022reactive-046
- The obstacle radius was enlarged by the radius of the grasped bottle, approximated as a sphere, to prevent bottle collisions. (Beik-Mohammadi et al., 2022) `ev:reported` p. 15 ^beikmohammadi2022reactive-047
- A combination of three geodesics produced a hybrid solution that poured all three cups with a single bottle in the given order. (Beik-Mohammadi et al., 2022) `ev:measured` p. 15 ^beikmohammadi2022reactive-048
- The authors state that the task space setting cannot achieve the joint-level redundancy required for multiple-limb obstacle avoidance. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 15 ^beikmohammadi2022reactive-049
- Each end-effector pose decoded from a 150 × 150 latent grid was used to compute 100 joint configurations by inverse kinematics. (Beik-Mohammadi et al., 2022) `ev:reported` p. 15 ^beikmohammadi2022reactive-050
- In latent regions close to the demonstrations, inverse kinematics configurations had up to 90 percent chance of colliding with the obstacle. (Beik-Mohammadi et al., 2022) `ev:measured` p. 15 ^beikmohammadi2022reactive-051
- A 2-dimensional latent space proved insufficient for joint-space demonstrations, producing geodesics with unnecessary switches between demonstrated solutions. (Beik-Mohammadi et al., 2022) `ev:measured` p. 16 ^beikmohammadi2022reactive-052
- The decoded 2-dimensional latent geodesic caused jerky movements and undesirable back-and-forth motions when deployed on the robot. (Beik-Mohammadi et al., 2022) `ev:measured` p. 16 ^beikmohammadi2022reactive-053
- With a 3-dimensional latent space, the geodesic did not switch among solutions and gave stable, smooth end-effector movements. (Beik-Mohammadi et al., 2022) `ev:measured` p. 16 ^beikmohammadi2022reactive-054
- In joint-space reach-to-grasp, the decoded geodesic executed by a joint position controller generated the demonstrated grasp with 90° rotation. (Beik-Mohammadi et al., 2022) `ev:measured` p. 17 ^beikmohammadi2022reactive-055
- When the obstacle partially obstructed the joint-space solutions, a few geodesics still generated obstacle-free movements executed on the robot. (Beik-Mohammadi et al., 2022) `ev:measured` p. 17 ^beikmohammadi2022reactive-056
- With overlapping joint-space demonstrations, the geodesic navigated around the obstacle by traveling through different demonstrations to reach the target. (Beik-Mohammadi et al., 2022) `ev:measured` p. 17 ^beikmohammadi2022reactive-057
- In joint-space pouring, the decoded geodesic used a multiple-solution strategy to reproduce a trajectory not explicitly demonstrated during training. (Beik-Mohammadi et al., 2022) `ev:measured` p. 18 ^beikmohammadi2022reactive-058
- The authors observed that geodesics forced to leave the learned manifold may cause inaccurate and undesirable motions outside the manifold. (Beik-Mohammadi et al., 2022) `ev:measured` p. 18 ^beikmohammadi2022reactive-059
- The authors believe data outside the training support may be arbitrarily misrepresented in the VAE latent space, causing this generalization issue. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 18 ^beikmohammadi2022reactive-060
- The authors could not replicate a geodesic crossing an obstacle, since geodesics tended to abandon the manifold rather than cross it. (Beik-Mohammadi et al., 2022) `ev:measured` p. 19 ^beikmohammadi2022reactive-061
- A 3-dimensional latent space was necessary for smooth joint-space geodesics, which increased the complexity of computing ambient metrics and geodesics. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 19 ^beikmohammadi2022reactive-062
- RBF networks used to model predictive variances are known to scale poorly to high-dimensional settings, according to cited prior work. (Beik-Mohammadi et al., 2022) `ev:cited` p. 20 ^beikmohammadi2022reactive-063
- The latent space dimensionality was chosen from empirical observations and, as such, may vary across different tasks and spaces. (Beik-Mohammadi et al., 2022) `ev:asserted` p. 20 ^beikmohammadi2022reactive-064

## 🎯 Contributions

## 📖 Glossary

- **Geodesic** — shortest curve between two points on a Riemannian manifold under its metric.
- **Pullback metric** — Riemannian metric in latent space obtained from decoder Jacobians, M = JᵀJ.
- **Ambient space metric** — hand-designed metric on the ambient space used to reshape the learned metric.
- **Magnification factor** — log square root of the metric determinant; large where latent distances are large.
- **von Mises-Fisher distribution** — isotropic Gaussian-like distribution constrained to the unit hypersphere.
- **Quaternion antipodality** — q and -q represent the same orientation on the 3-sphere.
- **Multiple-limb obstacle avoidance** — avoiding obstacles with the whole robot body, not only the end-effector.
- **Multiple-solution task** — task demonstrated through several distinct trajectories that geodesics can combine into hybrids.

## ❓ Open questions

- How can geodesics be kept accurate when start or target points lie outside the learned data manifold?
- Can obstacle avoidance be made a hard constraint, e.g. by removing graph nodes, with theoretical grounding?
- How does a non-Euclidean latent topology affect learned Riemannian manifolds for robot motion?
- How can geodesic computation and uncertainty estimation scale to higher-dimensional latent spaces that include perceptual data such as images?
- Is there an analytical way, e.g. via relative degree, to choose the minimum latent dimensionality?
- Would Bingham or anisotropic distributions improve quaternion and position modelling?
- How would the method perform with real obstacle localization instead of simulated obstacles in a digital twin?

## 📝 Notes on reading

The cached text is arXiv v2 (17 Aug 2023) in IJRR template format, while the registry identifier is the arXiv DOI; the year 2022 corresponds to v1. Figures 3–5, 7–19 (latent-space magnification factors, geodesic plots, robot snapshots) could only be described. The average energy of the cluster-crossing green geodesic is extracted as "2.49 × 109" (almost certainly 2.49 × 10^9); the number was not claimed as printed. Equations (2), (9), (16), (26)–(27) are partially garbled in extraction. Section 5.3.3 refers to Fig. 18 for the obstacle placement although Fig. 18 shows the joint-space experiment, a possible cross-reference slip. The paper spells the distribution 'von Mises-Fischer'; the note uses the standard spelling. The discussion also notes that Bingham distributions may model quaternion data more accurately than von Mises-Fisher. No quantitative comparison against baseline LfD methods is provided; results are mostly qualitative.

## Suggested new concepts

- Learned Riemannian metric from VAE — central construct linking generative models and motion generation via pullback metrics with uncertainty.
- Geodesic motion generation — motion skills as shortest paths on learned manifolds, recurring across LfD work.
- Ambient metric reshaping for obstacle avoidance — retraining-free reactive avoidance mechanism reusable beyond this paper.
- Graph-based geodesic computation — Dijkstra on discretized latent grids as a real-time alternative to ODE or gradient methods.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Versión reactiva con evitación de obstáculos (C.4, E.3).

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
