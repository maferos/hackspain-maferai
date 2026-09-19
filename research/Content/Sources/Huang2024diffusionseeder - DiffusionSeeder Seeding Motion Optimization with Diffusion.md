---
aliases: []
type: "source"
title: "DiffusionSeeder: Seeding Motion Optimization with Diffusion for Rapid Motion Planning"
citekey: "Huang2024diffusionseeder"
doi: "10.48550/arXiv.2410.16727"
arxiv: "2410.16727"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2410.16727"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Huang Huang", "Balakumar Sundaralingam", "Arsalan Mousavian", "Adithyavairavan Murali", "Ken Goldberg", "Dieter Fox"]
sha256: ["4ef3e01a6507493ef506da6e2da13030c351490bae308f51bad6a0efaab8893c"]
pdf: "Content/Papers/Huang2024diffusionseeder.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 65
---

📄 PDF: [[Huang2024diffusionseeder.pdf]]

> [!abstract] One-sentence summary
> DiffusionSeeder trains a depth-conditioned diffusion model to generate diverse seed trajectories for the GPU motion optimizer cuRobo, cutting planning time by 12x on average while raising success under partial observation in simulation and on a real Franka.

## Abstract

Running optimization across many parallel seeds leveraging GPU compute have relaxed the need for a good initialization, but this can fail if the problem is highly non-convex as all seeds could get stuck in local minima. One such setting is collision-free motion optimization for robot manipulation, where optimization converges quickly on easy problems but struggle in obstacle dense environments (e.g., a cluttered cabinet or table). In these situations, graph-based planning algorithms are used to obtain seeds, resulting in significant slowdowns. We propose DiffusionSeeder, a diffusion based approach that generates trajectories to seed motion optimization for rapid robot motion planning. DiffusionSeeder takes the initial depth image observation of the scene and generates high quality, multi-modal trajectories that are then fine-tuned with a few iterations of motion optimization. We integrate DiffusionSeeder to generate the seed trajectories for cuRobo, a GPU-accelerated motion optimization method, which results in 12x speed up on average, and 36x speed up for more complicated problems, while achieving 10% higher success rate in partially observed simulation environments. Our results show the effectiveness of using diverse solutions from a learned diffusion model. Physical experiments on a Franka robot demonstrate the sim2real transfer of DiffusionSeeder to the real robot, with an average success rate of 86% and planning time of 26ms, improving on cuRobo by 51% higher success rate while also being 2.5x faster. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that optimization-based motion planners, which can generate smooth paths directly, are highly sensitive to the initial seed. (Huang et al., 2024) `ev:asserted` p. 2 ^huang2024diffusionseeder-001
- The authors state that modern planner implementations resort to graph-based planning algorithms to guarantee completeness at the cost of speed. (Huang et al., 2024) `ev:asserted` p. 2 ^huang2024diffusionseeder-002
- DiffusionSeeder is a conditional DDPM that generates diverse seed trajectories to warm start the cuRobo optimization-based motion planner. (Huang et al., 2024) `ev:reported` p. 2 ^huang2024diffusionseeder-003
- DiffusionSeeder generates seed trajectories within 6 milliseconds from a raw depth image, camera pose, start joint configuration and end pose. (Huang et al., 2024) `ev:measured` p. 2 ^huang2024diffusionseeder-004
- The authors represent the partially observed environment with depth observations, which they state are faster to process than point clouds. (Huang et al., 2024) `ev:asserted` p. 2 ^huang2024diffusionseeder-005
- cuRobo falls back to a graph-based motion planner when optimization fails, which slows planning, taking up to 0.5 seconds. (Huang et al., 2024) `ev:cited` p. 3 ^huang2024diffusionseeder-006
- Motion planning policies such as MPNet and MπNet need multiple rollout steps per trajectory, resulting in longer planning time. (Huang et al., 2024) `ev:cited` p. 3 ^huang2024diffusionseeder-007
- DiffusionSeeder generates multiple full trajectories in each inference pass of the diffusion model, avoiding multi-step policy rollouts. (Huang et al., 2024) `ev:asserted` p. 3 ^huang2024diffusionseeder-008
- The planner receives a depth image, calibrated camera intrinsics and extrinsics, the start joint state, and the goal end-effector pose. (Huang et al., 2024) `ev:reported` p. 3 ^huang2024diffusionseeder-009
- The dataset was generated with cuRobo for a 7-DoF Franka robot in three scene categories: cubby, tabletop and dresser. (Huang et al., 2024) `ev:reported` p. 3 ^huang2024diffusionseeder-010
- The authors generated 15M problems with feasible, smooth cuRobo solutions of size 32×7 on 3M unique scenes. (Huang et al., 2024) `ev:reported` p. 12 ^huang2024diffusionseeder-011
- The authors sample 12 different camera poses for each training scene to help the model generalize to different viewpoints. (Huang et al., 2024) `ev:reported` p. 4 ^huang2024diffusionseeder-012
- The authors rendered 12M depth images of size 256 × 256 on 3M scenes, filtering out views where the end pose was invisible. (Huang et al., 2024) `ev:reported` p. 4 ^huang2024diffusionseeder-013
- The observation encoder is a ViT backbone with 12 layers and 12 heads, processing depth images projected to 3D. (Huang et al., 2024) `ev:reported` p. 4 ^huang2024diffusionseeder-014
- A 512-dimensional visual embedding is concatenated with a 64-dimensional problem encoding, giving a 576-dimensional environment embedding vector. (Huang et al., 2024) `ev:reported` p. 4 ^huang2024diffusionseeder-015
- The noise prediction model is a 3-level UNet of conditional residual blocks, adopted from a prior diffusion policy CNN architecture. (Huang et al., 2024) `ev:reported` p. 4 ^huang2024diffusionseeder-016
- The training loss compares true and predicted noise after mapping both through robot forward kinematics on points sampled across all links. (Huang et al., 2024) `ev:reported` p. 4 ^huang2024diffusionseeder-017
- The authors upweight the loss for trajectories that cuRobo originally solved with its graph-based planner, to emphasise harder non-linear solutions. (Huang et al., 2024) `ev:reported` p. 4 ^huang2024diffusionseeder-018
- The model was trained on 256 × 256 depth images with K = 100, α = 4 and batch size 256 for 72 epochs. (Huang et al., 2024) `ev:reported` p. 5 ^huang2024diffusionseeder-019
- Training DiffusionSeeder for 72 epochs took 2 days on 8 NVIDIA A100 GPUs, according to the authors. (Huang et al., 2024) `ev:reported` p. 5 ^huang2024diffusionseeder-020
- Using DDIM with CUDA optimization, inference takes 6ms on an RTX 4090, including the vision encoder and 5 denoising steps. (Huang et al., 2024) `ev:measured` p. 5 ^huang2024diffusionseeder-021
- For collision checking in partially observed scenes, the optimizer uses a Euclidean Signed Distance Field built by nvblox from the depth images. (Huang et al., 2024) `ev:reported` p. 5 ^huang2024diffusionseeder-022
- DiffusionSeeder uses Ndenoising = 5 and Ntrajs = 12, which the authors report as a good trade-off between quality, diversity and inference time. (Huang et al., 2024) `ev:reported` p. 5 ^huang2024diffusionseeder-023
- Evaluation uses the MπNet simulation test set of 1791 problems, with scenes of the training scene types but different configurations. (Huang et al., 2024) `ev:reported` p. 6 ^huang2024diffusionseeder-024
- Success thresholds for cuRobo and DiffusionSeeder were δt = 0.005m for translation error and δr = 2.86◦ for rotation error. (Huang et al., 2024) `ev:reported` p. 6 ^huang2024diffusionseeder-025
- With partial observations, DiffusionSeeder-50 reached 85.8% success, compared with 77.9% for cuRobo-100, on the 1791 test problems. (Huang et al., 2024) `ev:measured` p. 5 ^huang2024diffusionseeder-026
- Under partial observation, DiffusionSeeder-50 had a mean plan time of 0.017 s against 0.207 s for cuRobo-100. (Huang et al., 2024) `ev:measured` p. 5 ^huang2024diffusionseeder-027
- Compared with the best-performing cuRobo-100, DiffusionSeeder-50 is 12x faster in planning time with a 10% higher success rate. (Huang et al., 2024) `ev:measured` p. 7 ^huang2024diffusionseeder-028
- On average, DiffusionSeeder-50 is 3x faster in planning time than cuRobo-1, with a 30% higher success rate. (Huang et al., 2024) `ev:measured` p. 7 ^huang2024diffusionseeder-029
- In partially observed environments, DiffusionSeeder-50 is 4x faster than cuRobo-100 at the 75th quantile of planning time. (Huang et al., 2024) `ev:measured` p. 7 ^huang2024diffusionseeder-030
- In partially observed environments, DiffusionSeeder-50 is 36x faster than cuRobo-100 at the 98th quantile of planning time. (Huang et al., 2024) `ev:measured` p. 7 ^huang2024diffusionseeder-031
- Under the less strict threshold ˜δ, DiffusionSeeder has a success rate 3x higher than that of the sampling-based BiTStar planner. (Huang et al., 2024) `ev:measured` p. 6 ^huang2024diffusionseeder-032
- Under the less strict threshold ˜δ, DiffusionSeeder needs a planning time of 3% of that of BiTStar. (Huang et al., 2024) `ev:measured` p. 6 ^huang2024diffusionseeder-033
- Re-timed BiTStar trajectories reached a maximum jerk of 81.4 rad/s3, 21% lower than DiffusionSeeder-generated trajectories. (Huang et al., 2024) `ev:measured` p. 7 ^huang2024diffusionseeder-034
- Re-timed BiTStar trajectories had a motion time of 1.72s, being 27% slower than DiffusionSeeder-generated trajectories. (Huang et al., 2024) `ev:measured` p. 7 ^huang2024diffusionseeder-035
- DiffusionSeeder outperforms MπNet by an order of magnitude in success rate, 85.8% versus 8.3%, under partial observation. (Huang et al., 2024) `ev:measured` p. 7 ^huang2024diffusionseeder-036
- The authors hypothesize that this gain over MπNet comes from combining a learning approach with a classical motion planner. (Huang et al., 2024) `ev:asserted` p. 7 ^huang2024diffusionseeder-037
- MπNet lets the robot start moving after its first inference of about 7 ms, whereas DiffusionSeeder gives a complete trajectory in 17 ms. (Huang et al., 2024) `ev:measured` p. 7 ^huang2024diffusionseeder-038
- cuRobo's success rate increases monotonically with the number of attempts, which the authors read as inefficiency of its heuristic seed sampling. (Huang et al., 2024) `ev:measured` p. 7 ^huang2024diffusionseeder-039
- DiffusionSeeder reaches higher performance with 25 optimization iterations than cuRobo with 475, suggesting its seeds are closer to optimal collision-free trajectories. (Huang et al., 2024) `ev:measured` p. 7 ^huang2024diffusionseeder-040
- DiffusionSeeder-475 reached the highest success rate of 86.2% among the tested iteration counts under partial observation. (Huang et al., 2024) `ev:measured` p. 16 ^huang2024diffusionseeder-041
- DiffusionSeeder-25 had the lowest planning time of 15ms, with a success rate of 85.1%, under partial observation. (Huang et al., 2024) `ev:measured` p. 16 ^huang2024diffusionseeder-042
- Trajectory quality improves with more optimization iterations, at the cost of planning time rising from 15ms to 45ms. (Huang et al., 2024) `ev:measured` p. 16 ^huang2024diffusionseeder-043
- Real-robot tests used a Franka Panda across 6 scenes in 3 difficulty tiers plus an empty scene, none from the training data. (Huang et al., 2024) `ev:reported` p. 8 ^huang2024diffusionseeder-044
- On the real robot, DiffusionSeeder achieved an average success rate of 86% compared with 57% for cuRobo. (Huang et al., 2024) `ev:measured` p. 8 ^huang2024diffusionseeder-045
- In the physical Franka experiments, DiffusionSeeder had an average planning time of 26ms, compared with 65ms for cuRobo. (Huang et al., 2024) `ev:measured` p. 8 ^huang2024diffusionseeder-046
- The mean motion time of DiffusionSeeder's real-robot trajectories was higher than cuRobo's, at 42.3 versus 38.0 in Table 2. (Huang et al., 2024) `ev:measured` p. 8 ^huang2024diffusionseeder-047
- The authors hypothesize the higher motion time may be attributed to the additional loss weight on non-linear trajectories. (Huang et al., 2024) `ev:asserted` p. 8 ^huang2024diffusionseeder-048
- All cuRobo real-robot failures were due to limited view of the obstacles from a single camera. (Huang et al., 2024) `ev:measured` p. 8 ^huang2024diffusionseeder-049
- DiffusionSeeder failed in one real environment because the tree obstacle did not fully fit in the view of the camera. (Huang et al., 2024) `ev:measured` p. 8 ^huang2024diffusionseeder-050
- DiffusionSeeder generates trajectories from a fixed external camera view, making it less effective when the goal pose is occluded. (Huang et al., 2024) `ev:asserted` p. 8 ^huang2024diffusionseeder-051
- As a stated limitation, DiffusionSeeder is only trained on the Franka robot, with other robots left to future work. (Huang et al., 2024) `ev:asserted` p. 8 ^huang2024diffusionseeder-052
- The authors note a lack of thorough analysis of the forward-kinematics loss in Eq. 2 compared to a regular MSE loss. (Huang et al., 2024) `ev:asserted` p. 8 ^huang2024diffusionseeder-053
- On 500 narrow passage problems unlike the training scenes, DiffusionSeeder and cuRobo both reached a 52.4% success rate. (Huang et al., 2024) `ev:measured` p. 14 ^huang2024diffusionseeder-054
- Across 50 camera views of one cubby scene, DiffusionSeeder averaged 65.9% success compared with 60.2% for cuRobo. (Huang et al., 2024) `ev:measured` p. 15 ^huang2024diffusionseeder-055
- DiffusionSeeder performed better than cuRobo in more occluded views, which the authors take to indicate implicit scene completion ability. (Huang et al., 2024) `ev:measured` p. 15 ^huang2024diffusionseeder-056
- Cost gradient guidance improved DiffusionSeeder's success rate marginally, from 80.6% to 81.1%, in tests using cuRobo v0.7.4. (Huang et al., 2024) `ev:measured` p. 14 ^huang2024diffusionseeder-057
- With ground-truth meshes for collision checking, DiffusionSeeder-50 reached a 97% success rate against 99.7% for cuRobo-100. (Huang et al., 2024) `ev:measured` p. 16 ^huang2024diffusionseeder-058
- In fully observed environments, DiffusionSeeder-50 is 6x faster than cuRobo-100 on average in planning time. (Huang et al., 2024) `ev:measured` p. 16 ^huang2024diffusionseeder-059
- In fully observed environments, DiffusionSeeder-50 is 22x faster than cuRobo-100 at the 98th quantile of planning time. (Huang et al., 2024) `ev:measured` p. 16 ^huang2024diffusionseeder-060
- With Ntrajs = 12, the success rate of DiffusionSeeder is 1.99x higher than with Ntrajs = 1. (Huang et al., 2024) `ev:measured` p. 17 ^huang2024diffusionseeder-061
- Supplying more depth views at inference did not improve performance, likely because DiffusionSeeder is only trained on one depth image. (Huang et al., 2024) `ev:measured` p. 17 ^huang2024diffusionseeder-062
- Without cuRobo optimization, DiffusionSeeder's success rate rises from 13.2% with 8 samples to 31.5% with 1024 samples. (Huang et al., 2024) `ev:measured` p. 18 ^huang2024diffusionseeder-063
- Diffusion-only trajectories have a high maximum jerk of around 270 rad/s3, which cuRobo optimization reduces to around 106 rad/s3. (Huang et al., 2024) `ev:measured` p. 18 ^huang2024diffusionseeder-064
- On the real robot, DiffusionSeeder used 100 optimization iterations because using 50 did not give high-quality solutions. (Huang et al., 2024) `ev:reported` p. 18 ^huang2024diffusionseeder-065

## 🎯 Contributions


## 📖 Glossary

- **DDPM** — Denoising diffusion probabilistic model; generates samples by iteratively removing learned Gaussian noise.
- **DDIM** — Denoising diffusion implicit model; non-Markovian sampler that skips denoising steps for faster inference.
- **Seed trajectory** — Initial trajectory from which a trajectory optimizer starts its iterations.
- **cuRobo** — GPU-accelerated, parallel collision-free minimum-jerk motion optimizer used as the backend.
- **ESDF** — Euclidean signed distance field; distance-to-obstacle map used for collision costs.
- **nvblox** — GPU-accelerated library building signed distance fields from depth images.
- **MπNet** — Learned motion policy predicting next joint configurations from point clouds; also a scene dataset.
- **BiTStar** — Batch informed trees; sampling-based asymptotically optimal planner.
- **Ntrajs** — Number of seed trajectories sampled from the diffusion model per problem.
- **Niters** — Number of cuRobo optimization iterations applied to the diffusion seeds.

## ❓ Open questions

- Would training on multiple views or wrist-mounted cameras make DiffusionSeeder robust to an occluded goal pose?
- How much does the forward-kinematics, non-linearity-weighted loss (Eq. 2) actually contribute compared with plain MSE?
- Does the approach transfer to robots other than the Franka without retraining from scratch?
- How would DiffusionSeeder perform on scene types, such as narrow passages, when these are included in training?
- Can cost-gradient guidance be incorporated in the denoising process so it gives more than a marginal gain?
- Why does success stop increasing monotonically beyond Ntrajs = 12, and is the linear-seed ratio the cause?

## 📝 Notes on reading

Read the arXiv v1 preprint (2410.16727v1), which carries the CoRL 2024 header. Table 1 (p. 5) was extracted as a flat column stream; values were reassigned to columns by order (BiTStar ˜δ/δ, MπNet δ′/δ, cuRobo Natp = 1/10/100, DiffusionSeeder Niters = 25/50/100/200/475). Only headline cells were claimed. Figure 3 (p. 6) bar values (e.g. 207 vs 17 ms mean, 917 vs 25 ms at 98th quantile, partial observation) were read from a garbled chart extraction and not claimed. Inconsistencies: the real-robot section says 6 scenes plus an empty scene, then that DiffusionSeeder failed once 'among the 7 scenes'; Table 2 motion times (34.6–44.1) carry an '(s)' header that seems implausible per trajectory and may be totals across poses and trials. The abstract's '51% higher success rate' and '2.5x faster' are derived from 86% vs 57% and 26 ms vs 65 ms in the body. The p. 18 statement that cuRobo reduces jerk to around 106 rad/s3 does not exactly match the Table 1 DiffusionSeeder jerk range (89.6–108.8). Table 4 guidance results use cuRobo v0.7.4, so its 80.6% baseline differs from Table 1.

## Suggested new concepts

- Learned seeding of trajectory optimization — a recurring pattern (diffusion, RL, networks) for warm-starting optimizers that deserves a comparison note.
- Diffusion models for motion planning — several approaches (per-environment, cost-guided, scene-conditioned) differ in conditioning and speed.
- GPU-parallel motion optimization (cuRobo) — central backend for fast planning; its fallback-to-graph-planner behaviour drives latency tails.
- Partial-observation motion planning from single depth views — occlusion handling and implicit scene completion recur across planners.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H3.** Difusión condicionada a profundidad que siembra cuRobo, vínculo directo entre el pipeline de visión y el optimizador de trayectorias.
