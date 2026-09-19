---
aliases: []
type: "source"
title: "Learning Riemannian Manifolds for Geodesic Motion Skills"
citekey: "BeikMohammadi2021learning"
doi: "10.48550/arXiv.2106.04315"
arxiv: "2106.04315"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2106.04315"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Hadi Beik-Mohammadi", "Søren Hauberg", "Georgios Arvanitidis", "Gerhard Neumann", "Leonel Rozo"]
sha256: ["a0b3a8e70e3808a49527095d916ef1a7f298cdc8e1337ee10ddaf7a959d92299"]
pdf: "Content/Papers/BeikMohammadi2021learning.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[BeikMohammadi2021learning.pdf]]

> [!abstract] One-sentence summary
> The paper learns a Riemannian manifold of end-effector poses with a VAE and uses its geodesics as robot motion skills that reproduce demonstrations, avoid dynamic obstacles by rescaling the ambient metric, and combine multiple demonstrated solutions into new ones.

## Abstract

For robots to work alongside humans and perform in unstructured environments, they must learn new motion skills and adapt them to unseen situations on the fly. This demands learning models that capture relevant motion patterns, while offering enough flexibility to adapt the encoded skills to new requirements, such as dynamic obstacle avoidance. We introduce a Riemannian manifold perspective on this problem, and propose to learn a Riemannian manifold from human demonstrations on which geodesics are natural motion skills. We realize this with a variational autoencoder (VAE) over the space of position and orientations of the robot end-effector. Geodesic motion skills let a robot plan movements from and to arbitrary points on the data manifold. They also provide a straightforward method to avoid obstacles by redefining the ambient metric in an online fashion. Moreover, geodesics naturally exploit the manifold resulting from multiple--mode tasks to design motions that were not explicitly demonstrated previously. We test our learning framework using a 7-DoF robotic manipulator, where the robot satisfactorily learns and reproduces realistic skills featuring elaborated motion patterns, avoids previously unseen obstacles, and generates novel movements in multiple-mode settings. (arXiv)

## 🧠 Key ideas (atomic)

- The authors propose learning a Riemannian manifold from human demonstrations on which geodesics serve as natural robot motion skills. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 1 ^beikmohammadi2021learning-001
- A variational autoencoder is developed that learns a Riemannian submanifold of R3 × S3, the space of end-effector positions and orientations. (Beik-Mohammadi et al., 2021) `ev:reported` p. 1 ^beikmohammadi2021learning-002
- Geodesics, meaning shortest paths, on the learned manifold are the mechanism from which full-pose end-effector robot trajectories are generated. (Beik-Mohammadi et al., 2021) `ev:reported` p. 1 ^beikmohammadi2021learning-003
- Unlike previous works that built skill manifolds with locally smooth manifold learning, this work leverages a Riemannian formulation of the skill manifold. (Beik-Mohammadi et al., 2021) `ev:cited` p. 1 ^beikmohammadi2021learning-004
- The authors list full-pose movement encoding, adaptation to unseen or dynamic obstacles, and multiple-mode tasks as open challenges in learning from demonstration. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 1 ^beikmohammadi2021learning-005
- According to the authors, obstacle avoidance might be possible via via-points in several prior methods, but none explicitly considered this problem. (Beik-Mohammadi et al., 2021) `ev:cited` p. 2 ^beikmohammadi2021learning-006
- The authors note that previous learning frameworks generate robot motions restricted to the solutions provided for the task at hand. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 2 ^beikmohammadi2021learning-007
- Following prior work, the stochastic VAE decoder is viewed as a random projection of a deterministic manifold spanned by the mean and variance networks. (Beik-Mohammadi et al., 2021) `ev:cited` p. 3 ^beikmohammadi2021learning-008
- Geodesics under the VAE-induced metric have been shown in earlier work to be faithful to the data used for training. (Beik-Mohammadi et al., 2021) `ev:cited` p. 3 ^beikmohammadi2021learning-009
- Cited work argues that disregarding the variance contribution to the VAE metric gives an almost flat manifold geometry. (Beik-Mohammadi et al., 2021) `ev:cited` p. 3 ^beikmohammadi2021learning-010
- Following Arvanitidis et al., a manually defined ambient-space metric is included in curve length so geodesics can be pushed away from chosen regions. (Beik-Mohammadi et al., 2021) `ev:cited` p. 3 ^beikmohammadi2021learning-011
- Geodesics generally do not follow a closed-form expression in these models, requiring numerical approximations such as curve-length minimization or A∗ search. (Beik-Mohammadi et al., 2021) `ev:cited` p. 3 ^beikmohammadi2021learning-012
- Position and orientation are assumed conditionally independent given the latent variable, so all correlations between them must be captured by it. (Beik-Mohammadi et al., 2021) `ev:reported` p. 3 ^beikmohammadi2021learning-013
- End-effector positions are modelled with a Gaussian conditional distribution whose mean and variance are neural networks of the latent variable. (Beik-Mohammadi et al., 2021) `ev:reported` p. 3 ^beikmohammadi2021learning-014
- The authors disregard probability mass outside the robot workspace, arguing that the position variance tends to take small values given limited data noise. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 3 ^beikmohammadi2021learning-015
- Unit quaternions are described as convenient for orientation since they are compact, not redundant, and prevent gimbal lock, unlike Euler angles. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 3 ^beikmohammadi2021learning-016
- Orientations are modelled with a mixture of two antipodal von Mises-Fischer distributions to build an antipodal symmetric distribution over unit quaternions. (Beik-Mohammadi et al., 2021) `ev:reported` p. 4 ^beikmohammadi2021learning-017
- The authors describe the antipodal von Mises-Fischer mixture as conceptually similar to a Bingham distribution but easier to implement numerically. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 4 ^beikmohammadi2021learning-018
- The training objective weights the position and orientation log-likelihood terms with factors α and β beside the usual KL divergence term. (Beik-Mohammadi et al., 2021) `ev:reported` p. 4 ^beikmohammadi2021learning-019
- Training data are doubled by including both qn and −qn for all quaternion observations, avoiding any pre-processing of the raw orientation data. (Beik-Mohammadi et al., 2021) `ev:reported` p. 4 ^beikmohammadi2021learning-020
- Following Arvanitidis et al., radial basis function networks whose kernels reliably extrapolate over the whole space are used as the variance representation. (Beik-Mohammadi et al., 2021) `ev:reported` p. 4 ^beikmohammadi2021learning-021
- The data uncertainty is encoded by RBF networks representing the inverse position variance and the quaternion concentration, which enter the metric through their Jacobians. (Beik-Mohammadi et al., 2021) `ev:reported` p. 5 ^beikmohammadi2021learning-022
- Geodesics are penalized for crossing regions where VAE predictive uncertainty grows, which the authors say makes them follow the trend of the training data. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 5 ^beikmohammadi2021learning-023
- The authors suggest that geodesics on the learned manifold form a natural motion generation mechanism for reproducing demonstrated skills. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 5 ^beikmohammadi2021learning-024
- Under a Euclidean metric geodesics correspond to straight lines, which the authors say neglect the data manifold geometry. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 5 ^beikmohammadi2021learning-025
- Geodesics are approximated by cubic splines over latent control points, with polynomial coefficients estimated to minimize the Riemannian curve length. (Beik-Mohammadi et al., 2021) `ev:reported` p. 5 ^beikmohammadi2021learning-026
- The latent geodesic is decoded through the mean decoder networks into an end-effector trajectory that can be executed on the robot arm. (Beik-Mohammadi et al., 2021) `ev:reported` p. 5 ^beikmohammadi2021learning-027
- In a synthetic R2 × S2 example with J-shaped positions and C-shaped orientations, Riemannian geodesics stayed within the boundary near the training data. (Beik-Mohammadi et al., 2021) `ev:measured` p. 5 ^beikmohammadi2021learning-028
- In the same synthetic example, geodesics computed with the Euclidean metric failed to stay in the learned data manifold. (Beik-Mohammadi et al., 2021) `ev:measured` p. 5 ^beikmohammadi2021learning-029
- In the synthetic example the magnification factor was generally low, except on the boundary of the data manifold where predictive variance grows. (Beik-Mohammadi et al., 2021) `ev:measured` p. 5 ^beikmohammadi2021learning-030
- Obstacles are handled by scaling the ambient position metric with a Gaussian-shaped term parametrized by a cost scale, obstacle position and radius. (Beik-Mohammadi et al., 2021) `ev:reported` p. 5 ^beikmohammadi2021learning-031
- Under the obstacle-aware ambient metric geodesics generally avoid the object, but the authors emphasize this is only a soft constraint. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 6 ^beikmohammadi2021learning-032
- The obstacle approach is described as similar in spirit to CHOMP, except that it works along a low-dimensional learned manifold. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 6 ^beikmohammadi2021learning-033
- The authors emphasize that the VAE does not need to be re-trained when an obstacle changes position, as only the ambient metric changes. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 6 ^beikmohammadi2021learning-034
- For fast geodesics, the low-dimensional latent space is discretized into a uniform grid graph whose edge weights are Riemannian distances between neighbouring nodes. (Beik-Mohammadi et al., 2021) `ev:reported` p. 6 ^beikmohammadi2021learning-035
- Shortest paths on the latent grid graph are found with Dijkstra's algorithm by minimising the accumulated edge weights between start and target. (Beik-Mohammadi et al., 2021) `ev:reported` p. 6 ^beikmohammadi2021learning-036
- A cubic spline is fitted by minimizing the mean square error to the selected graph nodes to ensure a smooth trajectory. (Beik-Mohammadi et al., 2021) `ev:reported` p. 6 ^beikmohammadi2021learning-037
- Keeping a decoded latent graph in memory lets weights of graph points near moving obstacles be rescaled without querying the decoders. (Beik-Mohammadi et al., 2021) `ev:reported` p. 7 ^beikmohammadi2021learning-038
- Experiments cover a simulated pouring task and a real-world grasping scenario, both in R3×S3, with a 7-DoF Franka Emika Panda arm. (Beik-Mohammadi et al., 2021) `ev:reported` p. 7 ^beikmohammadi2021learning-039
- The real grasping demonstrations were recorded using kinesthetic teaching on the 7-DoF Franka Emika Panda robot with a two-finger gripper. (Beik-Mohammadi et al., 2021) `ev:reported` p. 7 ^beikmohammadi2021learning-040
- The simulated pouring dataset was collected using the Franka ROS Interface on Gazebo, with the robot controlled by an impedance controller. (Beik-Mohammadi et al., 2021) `ev:reported` p. 7 ^beikmohammadi2021learning-041
- The authors' Python implementation computing geodesics on a 100 × 100 grid graph runs at 100Hz on ordinary PC hardware. (Beik-Mohammadi et al., 2021) `ev:measured` p. 7 ^beikmohammadi2021learning-042
- The PyTorch encoder and decoder networks have two hidden layers with 200 and 100 neuron units in all experiments. (Beik-Mohammadi et al., 2021) `ev:reported` p. 7 ^beikmohammadi2021learning-043
- The RBF variance and concentration networks use 500 kernels calculated by k-means over the training dataset with a predefined bandwidth. (Beik-Mohammadi et al., 2021) `ev:reported` p. 7 ^beikmohammadi2021learning-044
- The VAE latent space is 2-dimensional, whereas the ambient space is 7-dimensional, corresponding to R3 × S3 end-effector poses. (Beik-Mohammadi et al., 2021) `ev:reported` p. 7 ^beikmohammadi2021learning-045
- A single neural network represents both position and orientation decoder means, with the quaternion part projected to S3 afterwards. (Beik-Mohammadi et al., 2021) `ev:reported` p. 7 ^beikmohammadi2021learning-046
- The ELBO weights α and β were found experimentally to guarantee good reconstruction of both position and quaternion data. (Beik-Mohammadi et al., 2021) `ev:reported` p. 7 ^beikmohammadi2021learning-047
- The authors state that manually providing antipodal quaternions during training leads to better latent space structures and reconstruction accuracy. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 7 ^beikmohammadi2021learning-048
- Evaluation was done extensively in simulation because the COVID-19 pandemic prohibited access to the authors' robotic labs. (Beik-Mohammadi et al., 2021) `ev:reported` p. 7 ^beikmohammadi2021learning-049
- The demonstrated grasping motion includes a 90° rotation when approaching the object to perform a side grasp. (Beik-Mohammadi et al., 2021) `ev:reported` p. 7 ^beikmohammadi2021learning-050
- A geodesic computed in the latent space produced a continuous trajectory that closely reproduces the rotation pattern observed during grasping demonstrations. (Beik-Mohammadi et al., 2021) `ev:measured` p. 7 ^beikmohammadi2021learning-051
- The learned grasping manifold was composed of two similar clusters, which the authors attribute to the antipodal encoding of quaternions. (Beik-Mohammadi et al., 2021) `ev:measured` p. 7 ^beikmohammadi2021learning-052
- The authors state that the antipodal encoding alleviates any post-processing of raw quaternion data during training or reproduction phases. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 7 ^beikmohammadi2021learning-053
- The simulated pouring task involves grasping 3 cans from 3 different positions and pouring at 3 cups in different locations. (Beik-Mohammadi et al., 2021) `ev:reported` p. 8 ^beikmohammadi2021learning-054
- In the pouring task, a geodesic switched between demonstration groups to produce a hybrid solution that was not explicitly demonstrated. (Beik-Mohammadi et al., 2021) `ev:measured` p. 8 ^beikmohammadi2021learning-055
- With 3 sets of pouring demonstrations, all 9 permutations of grasping any can and pouring any cup are reported feasible. (Beik-Mohammadi et al., 2021) `ev:measured` p. 8 ^beikmohammadi2021learning-056
- For the unseen-obstacle test, the obstacle position was selected from the training set to ensure it was in the geodesic's way. (Beik-Mohammadi et al., 2021) `ev:reported` p. 8 ^beikmohammadi2021learning-057
- In simulated pouring, geodesics avoided a moving obstacle while following the manifold geometry, shown at two time frames of one motion. (Beik-Mohammadi et al., 2021) `ev:measured` p. 8 ^beikmohammadi2021learning-058
- The authors state that graph-based geodesic computation is faster than gradient-based computation and thus more suitable for real-time motion generation. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 8 ^beikmohammadi2021learning-059
- The authors note that data lying outside the learned manifold may be arbitrarily misrepresented in the latent space of the VAE. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 9 ^beikmohammadi2021learning-060
- Conditioning on points such as new targets located outside the learned manifold was not explored in the present paper. (Beik-Mohammadi et al., 2021) `ev:reported` p. 9 ^beikmohammadi2021learning-061
- Removing graph nodes near obstacles is proposed as an unexplored hard-constraint alternative to re-weighting edges, possibly saving computation. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 9 ^beikmohammadi2021learning-062
- The obstacle avoidance formulation only considered simple obstacles, though the authors argue it can be extended to multiple dynamic obstacles. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 9 ^beikmohammadi2021learning-063
- The authors note that safe execution requires obstacle avoidance for all robot links, not just the end-effector, needing a joint-space manifold. (Beik-Mohammadi et al., 2021) `ev:asserted` p. 9 ^beikmohammadi2021learning-064

## 🎯 Contributions

## 📖 Glossary

- **Geodesic** — shortest curve between two points on a Riemannian manifold under its metric.
- **Riemannian metric** — smoothly varying positive-definite inner product defining local lengths on a manifold.
- **Variational autoencoder (VAE)** — latent-variable generative model trained by maximizing an evidence lower bound.
- **Pull-back metric** — metric on latent space induced by the decoder Jacobians and ambient metric.
- **Magnification factor** — log square root of the metric determinant; large where latent distances stretch.
- **Ambient metric** — metric defined on the observation space, here reshaped around obstacles.
- **von Mises-Fischer distribution** — isotropic Gaussian-like distribution constrained to the unit sphere.
- **Antipodal symmetry** — property that q and −q represent the same orientation for unit quaternions.
- **Kinesthetic teaching** — demonstration by a human physically guiding the robot arm through the motion.
- **RBF network** — radial basis function network used here to extrapolate variance away from data.

## ❓ Open questions

- How does the method behave when conditioned on new targets that lie outside the learned manifold?
- How accurate are the reproduced motions quantitatively, given the paper reports no numeric tracking or reconstruction errors?
- Does the approach hold up on the real robot, since geodesic reproductions were executed only in simulation?
- Does the grid-graph approach scale to latent spaces beyond 2 dimensions while staying real time?
- Can obstacle avoidance be extended to all robot links via a joint-space manifold and combined ambient metric?
- How do complex obstacle shapes represented as point clouds affect real-time performance?

## 📝 Notes on reading

Read the arXiv v2 preprint (1 Jul 2021), matching the packet identifier. Results are qualitative: figures 3–9 show latent-space geodesics over magnification-factor backgrounds and decoded trajectories on a simulated Panda; no quantitative error metrics or baseline comparisons are reported. Equation (2) in the cached text reads N(z|µθ(z), …) where x is presumably meant, and the posterior in (3) reads N(x|µφ(x), …) where z is meant; these look like typos in the paper. Section III-D says the RBF networks represent the variance, while Section V-B uses a single decoder-mean network for position and orientation, modifying the metric of (21) into (25). The conclusion says evaluation was extensive in simulation; the real robot was used only to record grasping demonstrations.

## Suggested new concepts

- Pull-back Riemannian metric of generative models — central tool linking VAE decoders to geodesic motion generation.
- Geodesic motion skills — a distinct learning-from-demonstration paradigm competing with movement primitives.
- Obstacle-aware ambient metric — reusable mechanism for online obstacle avoidance without retraining a learned model.
- Antipodal quaternion encoding — practical recipe for learning orientation distributions on S3.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Geodésicas de métricas pullback como habilidades (C.4, E.3).

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
