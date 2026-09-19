---
aliases: []
type: "source"
title: "Motion Planning Diffusion: Learning and Planning of Robot Motions with Diffusion Models"
citekey: "Carvalho2023motion"
doi: "10.48550/arXiv.2308.01557"
arxiv: "2308.01557"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2308.01557"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Joao Carvalho", "An T. Le", "Mark Baierl", "Dorothea Koert", "Jan Peters"]
sha256: ["5045a1eef8b1e29e7007877083ddf26932fa6561717242e7a0b988cda751db95"]
pdf: "Content/Papers/Carvalho2023motion.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Carvalho2023motion.pdf]]

> [!abstract] One-sentence summary
> Motion Planning Diffusion learns a diffusion prior over expert robot trajectories and samples the task posterior by guiding denoising with motion-planning cost gradients, beating a CVAE prior on success and multimodality in simulated and real Panda tasks.

## Abstract

Learning priors on trajectory distributions can help accelerate robot motion planning optimization. Given previously successful plans, learning trajectory generative models as priors for a new planning problem is highly desirable. Prior works propose several ways on utilizing this prior to bootstrapping the motion planning problem. Either sampling the prior for initializations or using the prior distribution in a maximum-a-posterior formulation for trajectory optimization. In this work, we propose learning diffusion models as priors. We then can sample directly from the posterior trajectory distribution conditioned on task goals, by leveraging the inverse denoising process of diffusion models. Furthermore, diffusion has been recently shown to effectively encode data multimodality in high-dimensional settings, which is particularly well-suited for large trajectory dataset. To demonstrate our method efficacy, we compare our proposed method - Motion Planning Diffusion - against several baselines in simulated planar robot and 7-dof robot arm manipulator environments. To assess the generalization capabilities of our method, we test it in environments with previously unseen obstacles. Our experiments show that diffusion models are strong priors to encode high-dimensional trajectory distributions of robot motions. (arXiv)

## 🧠 Key ideas (atomic)

- In practice, sampling-based motion planners often suffer from sample inefficiency, as the authors note citing earlier work on trajectory smoothing. (Carvalho et al., 2023) `ev:cited` p. 1 ^carvalho2023motion-001
- Optimization-based motion planners can get trapped in local minima due to the non-convexity of complex motion planning problems. (Carvalho et al., 2023) `ev:asserted` p. 1 ^carvalho2023motion-002
- Optimization-based planners commonly require a good initialization prior and well-tuned hyperparameters to work well, according to earlier work. (Carvalho et al., 2023) `ev:cited` p. 1 ^carvalho2023motion-003
- The authors propose merging prior sampling and motion optimization into one algorithm by leveraging recent formulations of diffusion-based generative models. (Carvalho et al., 2023) `ev:asserted` p. 1 ^carvalho2023motion-004
- The trajectory diffusion model is learned from expert trajectories that were generated with an optimal motion planning algorithm. (Carvalho et al., 2023) `ev:reported` p. 1 ^carvalho2023motion-005
- The authors note that the full position and velocity state of a Franka Emika Panda arm has 14 dimensions. (Carvalho et al., 2023) `ev:asserted` p. 1 ^carvalho2023motion-006
- The paper formulates motion planning as planning-as-inference, sampling from a posterior distribution by leveraging guidance in diffusion models. (Carvalho et al., 2023) `ev:asserted` p. 1 ^carvalho2023motion-007
- The authors state that Gaussian Mixture Model priors fitted to demonstrations typically cannot capture multimodal trajectories well in high-dimensional spaces. (Carvalho et al., 2023) `ev:asserted` p. 2 ^carvalho2023motion-008
- The authors note, citing work on amortized sampling, that sampling high-dimensional trajectories is difficult for Energy-Based Models. (Carvalho et al., 2023) `ev:cited` p. 2 ^carvalho2023motion-009
- In contrast to earlier diffusion planners, MPD incorporates diffusion models as priors combined with differentiable cost likelihoods for motion planning. (Carvalho et al., 2023) `ev:asserted` p. 2 ^carvalho2023motion-010
- A trajectory is represented as a discrete-time sequence of H waypoint states, each combining configuration position with configuration velocity. (Carvalho et al., 2023) `ev:reported` p. 2 ^carvalho2023motion-011
- The method considers only states and assumes a controller, such as a PD or inverse dynamics controller, moves the robot between states. (Carvalho et al., 2023) `ev:reported` p. 2 ^carvalho2023motion-012
- Maximum-a-posteriori inference on the trajectory posterior is shown equivalent to the weighted-cost motion planning problem minus the log prior. (Carvalho et al., 2023) `ev:computed` p. 3 ^carvalho2023motion-013
- Following the Diffuser work, the diffusion model over trajectories is encoded with a temporal U-Net architecture. (Carvalho et al., 2023) `ev:reported` p. 3 ^carvalho2023motion-014
- The denoising network is trained to predict the added noise instead of the posterior mean, using a simplified loss function. (Carvalho et al., 2023) `ev:reported` p. 3 ^carvalho2023motion-015
- Since the denoising covariance approaches zero, the task log-likelihood is approximated with a first-order Taylor expansion around the denoising mean. (Carvalho et al., 2023) `ev:computed` p. 3 ^carvalho2023motion-016
- Sampling from the task-conditioned posterior becomes equivalent to sampling a Gaussian whose mean is shifted by the covariance-scaled cost gradient. (Carvalho et al., 2023) `ev:computed` p. 4 ^carvalho2023motion-017
- In practice, the authors drop the covariance scaling of the cost gradient to keep the influence of the task likelihood. (Carvalho et al., 2023) `ev:reported` p. 4 ^carvalho2023motion-018
- Start and goal states are enforced by hard setting the initial and final trajectory waypoints at every denoising step. (Carvalho et al., 2023) `ev:reported` p. 4 ^carvalho2023motion-019
- The collision cost uses a differentiable signed-distance function from collision spheres on the robot body to the closest obstacle surface. (Carvalho et al., 2023) `ev:reported` p. 4 ^carvalho2023motion-020
- Forward kinematics is implemented differentiably in PyTorch, with the kinematics Jacobian computed by automatic differentiation. (Carvalho et al., 2023) `ev:reported` p. 4 ^carvalho2023motion-021
- Joint and velocity limits are enforced by computing L2 norm joint violations as costs, with a margin on each dimension. (Carvalho et al., 2023) `ev:reported` p. 4 ^carvalho2023motion-022
- The end-effector cost is a distance on SE(3) combining squared translation error with the norm of the rotation logarithm map. (Carvalho et al., 2023) `ev:reported` p. 4 ^carvalho2023motion-023
- A Gaussian Process cost built on a holonomic system model is used to promote dynamic feasibility and smoothness of trajectories. (Carvalho et al., 2023) `ev:reported` p. 5 ^carvalho2023motion-024
- Experiments use PointMass2D Dense, PointMass3D Maze Boxes, and two 7-dof Franka Emika Panda environments called Panda Spheres and Panda Shelf. (Carvalho et al., 2023) `ev:reported` p. 5 ^carvalho2023motion-025
- To test generalization, all environments are extended with additional sphere and box obstacles that are not present during training. (Carvalho et al., 2023) `ev:reported` p. 5 ^carvalho2023motion-026
- Baselines include a GPU-parallelized RRTConnect, [[Gaussian Process Motion Planning|GPMP with a straight-line prior]], and a Conditional Variational AutoEncoder trajectory prior. (Carvalho et al., 2023) `ev:reported` p. 5 ^carvalho2023motion-027
- For a fair comparison, the CVAE encoder and decoder networks match the encoding and decoding parts of the diffusion U-Net. (Carvalho et al., 2023) `ev:reported` p. 5 ^carvalho2023motion-028
- The CVAEPosterior baseline first samples the CVAE prior, then optimizes the cost likelihood with as many steps as MPD uses. (Carvalho et al., 2023) `ev:reported` p. 5 ^carvalho2023motion-029
- Metrics report the mean and standard deviation over 100 random start-goal contexts, sampling 100 trajectories per context. (Carvalho et al., 2023) `ev:reported` p. 5 ^carvalho2023motion-030
- Success is scored 1 for a context if at least one trajectory in the batch is collision-free, and 0 otherwise. (Carvalho et al., 2023) `ev:reported` p. 6 ^carvalho2023motion-031
- Waypoint variance sums pairwise L2-distance variance between waypoints at corresponding time steps to measure how multimodal generated trajectories are. (Carvalho et al., 2023) `ev:reported` p. 6 ^carvalho2023motion-032
- In PointMass3D Maze Boxes, MPD reached a success rate of 85.0 ± 35.7 compared with 50.0 ± 50.0 for CVAEPosterior. (Carvalho et al., 2023) `ev:measured` p. 6 ^carvalho2023motion-033
- In PointMass3D Maze Boxes, GPMP with an uninformed straight-line prior achieved a success rate of 16.0 ± 36.7. (Carvalho et al., 2023) `ev:measured` p. 6 ^carvalho2023motion-034
- In Panda Spheres, MPD achieved a success rate of 100.0 ± .0, compared with 42.0 ± 49.4 for [[Gaussian Process Motion Planning|GPMP without an informed prior]]. (Carvalho et al., 2023) `ev:measured` p. 6 ^carvalho2023motion-035
- In Panda Spheres, MPD needed 1.1 ± .01 seconds of computation, compared with 194.4 ± .1 seconds for [[Gaussian Process Motion Planning|GPMP]]. (Carvalho et al., 2023) `ev:measured` p. 6 ^carvalho2023motion-036
- In Panda Spheres with extra obstacles, MPD kept a success rate of 93.0 ± 25.5 against 45.0 ± 49.8 for CVAEPosterior. (Carvalho et al., 2023) `ev:measured` p. 6 ^carvalho2023motion-037
- In PointMass2D Dense with extra obstacles, MPD reached a success rate of 79.0 ± 40.7, close to CVAEPosterior at 78.0 ± 41.4. (Carvalho et al., 2023) `ev:measured` p. 6 ^carvalho2023motion-038
- In PointMass2D Dense with extra obstacles, MPD had collision intensity 10.3 ± 8.5, higher than the .5 ± .7 of CVAEPosterior. (Carvalho et al., 2023) `ev:measured` p. 6 ^carvalho2023motion-039
- In Panda Spheres, MPD waypoint variance was 17.4 ± 3.9, compared with .03 ± .04 for CVAEPosterior. (Carvalho et al., 2023) `ev:measured` p. 6 ^carvalho2023motion-040
- In Panda Shelf with extra obstacles, MPD achieved a success rate of 99.0 ± 10.0 against 83.0 ± 37.6 for CVAEPosterior. (Carvalho et al., 2023) `ev:measured` p. 6 ^carvalho2023motion-041
- In PointMass3D Maze Boxes, RRTConnect needed 27.4 ± 26.1 seconds with sequential sampling, against .3 ± .01 seconds for MPD. (Carvalho et al., 2023) `ev:measured` p. 6 ^carvalho2023motion-042
- Dividing reported RRTConnect times by 100 makes it, on average, faster than one second per single collision-free path. (Carvalho et al., 2023) `ev:measured` p. 6 ^carvalho2023motion-043
- Expert data were generated by sampling 500 random start and goal contexts per environment with 20 trajectories per context. (Carvalho et al., 2023) `ev:reported` p. 7 ^carvalho2023motion-044
- Expert trajectories come from RRTConnect solutions smoothed with a B-spline, then refined by many Stochastic-GPMP optimization steps. (Carvalho et al., 2023) `ev:reported` p. 7 ^carvalho2023motion-045
- The Panda environments use a trajectory horizon of H = 64 with a state-space dimension of d = 14. (Carvalho et al., 2023) `ev:reported` p. 7 ^carvalho2023motion-046
- The diffusion models are trained for 25 diffusion steps, using early stopping based on inspecting the validation loss. (Carvalho et al., 2023) `ev:reported` p. 7 ^carvalho2023motion-047
- The authors found exponential noise scheduling to work better than linear scheduling for training their trajectory diffusion models. (Carvalho et al., 2023) `ev:asserted` p. 7 ^carvalho2023motion-048
- All environments, algorithms, and costs were implemented in PyTorch on a machine with an NVIDIA GeForce RTX 3090 GPU. (Carvalho et al., 2023) `ev:reported` p. 7 ^carvalho2023motion-049
- In PointMass2D Dense, DiffusionPrior reached a 98% success rate versus 46% for the CVAEPrior baseline trained on the same data. (Carvalho et al., 2023) `ev:measured` p. 7 ^carvalho2023motion-050
- The authors observed that across different planning problems, the CVAE models tended to generate fewer modes than the diffusion models. (Carvalho et al., 2023) `ev:measured` p. 7 ^carvalho2023motion-051
- Success rates obtained by sampling only from the learned priors decrease in environments with obstacles not seen during training. (Carvalho et al., 2023) `ev:measured` p. 7 ^carvalho2023motion-052
- In Panda Shelf with extra obstacles, DiffusionPrior success stayed at 100%, but its collision intensity increased from 3.6% to 5.9%. (Carvalho et al., 2023) `ev:measured` p. 7 ^carvalho2023motion-053
- For the Panda environments, MPD and CVAEPosterior have comparable computation times, since most cost is spent computing cost gradients, not diffusion sampling. (Carvalho et al., 2023) `ev:measured` p. 7 ^carvalho2023motion-054
- Across all environments, initializing GPMP with diffusion samples gave higher success rates than [[Gaussian Process Motion Planning|GPMP with a constant-velocity straight-line prior]]. (Carvalho et al., 2023) `ev:measured` p. 7 ^carvalho2023motion-055
- The authors state that RRTConnect generally produces high-jerk trajectories with higher path lengths when used as a prior for GPMP. (Carvalho et al., 2023) `ev:asserted` p. 7 ^carvalho2023motion-056
- In the real Panda Shelf task, the robot moved a bottle around unseen obstacles while maintaining a constant end-effector orientation. (Carvalho et al., 2023) `ev:reported` p. 7 ^carvalho2023motion-057
- On the real robot, 25 collision-free MPD trajectories from 3 initial configurations were executed with a joint impedance controller. (Carvalho et al., 2023) `ev:reported` p. 7 ^carvalho2023motion-058
- Of the 25 MPD trajectories executed on the real Panda robot, 19 remained collision-free with the new obstacles. (Carvalho et al., 2023) `ev:measured` p. 7 ^carvalho2023motion-059
- The authors hypothesize that the remaining 6 real-world collisions are due to the approximated sphere-based robot collision model. (Carvalho et al., 2023) `ev:asserted` p. 7 ^carvalho2023motion-060
- The authors conclude that diffusion models are better motion planning priors because they encode multimodal trajectories better than commonly used CVAEs. (Carvalho et al., 2023) `ev:asserted` p. 8 ^carvalho2023motion-061
- The authors conclude that sampling from the learned prior while optimizing the likelihood leads to improved results in finding collision-free trajectories. (Carvalho et al., 2023) `ev:asserted` p. 8 ^carvalho2023motion-062
- Future work will extend diffusion models to encode different parametrizations of trajectories for robotic movements, according to the authors. (Carvalho et al., 2023) `ev:asserted` p. 8 ^carvalho2023motion-063

## 🎯 Contributions

## 📖 Glossary

- **Motion Planning Diffusion (MPD)** — Sampling trajectories from a diffusion prior while guiding denoising with planning-cost gradients.
- **Planning-as-inference** — Treating planning as sampling a trajectory posterior from a prior and task likelihood.
- **Classifier guidance** — Biasing diffusion denoising steps with the gradient of a log-likelihood term.
- **GPMP** — Gaussian Process Motion Planning: trajectory optimization with a Gaussian Process smoothness prior.
- **RRTConnect** — Bidirectional rapidly-exploring random tree planner for single-query path planning.
- **CVAE** — Conditional Variational AutoEncoder; a latent-variable generative model conditioned on context.
- **Temporal U-Net** — Convolutional U-Net over the time axis, used as a trajectory denoiser.
- **Collision intensity** — Percentage of trajectory waypoints that are in collision.
- **Waypoint variance** — Spread of sampled trajectories at matching time steps, a multimodality measure.

## ❓ Open questions

- How does MPD scale to scenes whose obstacle layout differs strongly from training, beyond a few added spheres and boxes?
- Would a more accurate collision model than spheres remove the 6 real-robot collisions?
- Why does MPD show much higher collision intensity than CVAEPosterior in PointMass2D Dense with extra obstacles?
- How sensitive are results to the dropped covariance scaling and the constant cost temperatures?
- Can the approach handle other trajectory parametrizations, such as splines or time-varying horizons?
- How much expert data is needed per environment, given the costly offline generation?

## 📝 Notes on reading

The cached text is arXiv 2308.01557v2 (26 Mar 2024), matching the packet identifier.

Table I (p. 6) was extracted as a flat column of values. The RRTC rows carry 8 values instead of 10, so the VAR column appears to be missing for RRTConnect; its VAR values were not claimed. Some cells are printed oddly (e.g. `92. ± 27.1`, `99.0 ± 10.`, `18.0 ± 4.`), and S[%] cells carry standard deviations over binary per-context success.

The text on p. 7 says MPD beats CVAEPosterior in success rate under extra obstacles, but in PointMass2D Dense - Extra Obstacles the two are close (79.0 vs 78.0), and MPD collision intensity there (10.3) is much higher than CVAEPosterior (.5). In several environments CVAEPosterior also has lower collision intensity and shorter paths than MPD.

Fig. 1 shows two modes of real Panda Shelf motions sharing start and end configurations; Fig. 3 shows diffusion steps turning noise into multimodal collision-free trajectories in PointMass2D Dense - Extra Obstacles, versus CVAEPosterior trajectories. Both are described only.

The real-world experiment reports 3 start configurations with 10 samples each yet 25 collision-free trajectories after filtering; the arithmetic of filtering is not explained further.

## Suggested new concepts

- Diffusion trajectory priors — a recurring idea linking generative models to motion planning and imitation learning.
- Cost-guided diffusion sampling — the general mechanism of steering denoising with differentiable planning costs.
- Planning-as-inference — framework that unifies trajectory optimization with probabilistic priors and likelihoods.
- Gaussian Process Motion Planning — a standard optimization baseline and smoothness prior used across planning papers.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H3.** Usa difusión como prior de trayectorias y muestrea la posterior guiada por costes, uniendo planificación y modelos generativos.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
