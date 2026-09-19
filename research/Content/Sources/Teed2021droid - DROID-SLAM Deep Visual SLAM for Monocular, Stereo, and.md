---
aliases: []
type: "source"
title: "DROID-SLAM: Deep Visual SLAM for Monocular, Stereo, and RGB-D Cameras"
citekey: "Teed2021droid"
doi: "10.48550/arXiv.2108.10869"
arxiv: "2108.10869"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2108.10869"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Zachary Teed", "Jia Deng"]
sha256: ["0e15f20bff5f7ceac468c2899baafc8c114a3018c7a7b213eed7c402e5ccec90"]
pdf: "Content/Papers/Teed2021droid.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Teed2021droid.pdf]]

> [!abstract] One-sentence summary
> DROID-SLAM couples RAFT-style recurrent updates with a differentiable dense bundle adjustment layer, yielding a single monocular-trained deep SLAM system that beats classical and learned baselines on monocular, stereo and RGB-D benchmarks with far fewer failures.

## Abstract

We introduce DROID-SLAM, a new deep learning based SLAM system. DROID-SLAM consists of recurrent iterative updates of camera pose and pixelwise depth through a Dense Bundle Adjustment layer. DROID-SLAM is accurate, achieving large improvements over prior work, and robust, suffering from substantially fewer catastrophic failures. Despite training on monocular video, it can leverage stereo or RGB-D video to achieve improved performance at test time. The URL to our open source code is https://github.com/princeton-vl/DROID-SLAM. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that current SLAM systems lack the robustness demanded for many real-world applications, failing through lost feature tracks, optimization divergence or drift. (Teed & Deng, 2021) `ev:asserted` p. 1 ^teed2021droid-001
- Earlier end-to-end learned SLAM or VO systems are sometimes more robust, yet fall far short of classical accuracy on common benchmarks. (Teed & Deng, 2021) `ev:cited` p. 1 ^teed2021droid-002
- On the TartanAir SLAM competition, DROID-SLAM reduces error by 62% over the best prior result on the monocular track. (Teed & Deng, 2021) `ev:measured` p. 1 ^teed2021droid-003
- On the stereo track of the TartanAir SLAM competition, DROID-SLAM reduces error by 60% over the best prior result. (Teed & Deng, 2021) `ev:measured` p. 1 ^teed2021droid-004
- DROID-SLAM ranks 1st on the ETH-3D RGB-D SLAM leaderboard, outperforming the second place by 35% under the AUC metric. (Teed & Deng, 2021) `ev:measured` p. 2 ^teed2021droid-005
- On EuRoC with monocular input, DROID-SLAM reduces trajectory error by 82% among the methods that have zero failures. (Teed & Deng, 2021) `ev:measured` p. 2 ^teed2021droid-006
- On monocular EuRoC, DROID-SLAM reduces error by 43% over ORB-SLAM3, counting only the 10 out of 11 sequences ORB-SLAM3 succeeds on. (Teed & Deng, 2021) `ev:measured` p. 2 ^teed2021droid-007
- On TUM-RGBD, DROID-SLAM reduces trajectory error by 83% among the methods with zero failures on the benchmark. (Teed & Deng, 2021) `ev:measured` p. 2 ^teed2021droid-008
- On ETH-3D, DROID-SLAM successfully tracks 30 of the 32 RGB-D datasets, compared with only 19/32 for the next best system. (Teed & Deng, 2021) `ev:measured` p. 2 ^teed2021droid-009
- All results across 4 datasets and 3 modalities come from a single model trained once on monocular synthetic TartanAir video. (Teed & Deng, 2021) `ev:reported` p. 2 ^teed2021droid-010
- The system, trained only with monocular input, can use stereo or RGB-D input for improved accuracy without any retraining. (Teed & Deng, 2021) `ev:measured` p. 2 ^teed2021droid-011
- Building on RAFT, DROID-SLAM iteratively updates camera poses and depth instead of optical flow, using recurrent iterative updates. (Teed & Deng, 2021) `ev:asserted` p. 2 ^teed2021droid-012
- Unlike RAFT's two frames, its updates apply to an arbitrary number of frames, enabling joint global refinement of all poses and depths. (Teed & Deng, 2021) `ev:asserted` p. 2 ^teed2021droid-013
- Each update comes from a [[Differentiable optimization layers|differentiable Dense Bundle Adjustment layer]] that computes a Gauss-Newton step on poses and dense per-pixel depth. (Teed & Deng, 2021) `ev:reported` p. 2 ^teed2021droid-014
- The closest prior architecture DeepV2D alternates between updating depth and updating camera poses rather than performing bundle adjustment. (Teed & Deng, 2021) `ev:cited` p. 2 ^teed2021droid-015
- BA-Net optimizes a small number of coefficients combining a depth basis, whereas DROID-SLAM optimizes per-pixel depth directly. (Teed & Deng, 2021) `ev:cited` p. 2 ^teed2021droid-016
- The authors argue their method fits neither direct nor indirect categories, using the full image yet minimizing reprojection error like indirect methods. (Teed & Deng, 2021) `ev:asserted` p. 3 ^teed2021droid-017
- The authors argue that optimizing pixelwise depth, rather than a learned depth basis as DeepFactors does, lets their network generalize better to new datasets. (Teed & Deng, 2021) `ev:asserted` p. 3 ^teed2021droid-018
- For each image the system maintains a camera pose in SE(3) and an inverse depth map, both updated iteratively during inference. (Teed & Deng, 2021) `ev:reported` p. 3 ^teed2021droid-019
- Long range connections are added to the co-visibility frame graph when the camera returns to a previously mapped region, performing loop closure. (Teed & Deng, 2021) `ev:reported` p. 4 ^teed2021droid-020
- The feature extraction network has 6 residual blocks and 3 downsampling layers, producing dense feature maps at 1/8 the input resolution. (Teed & Deng, 2021) `ev:reported` p. 4 ^teed2021droid-021
- The core learned update operator is a 3 × 3 convolutional GRU that produces a pose update and a depth update each iteration. (Teed & Deng, 2021) `ev:reported` p. 4 ^teed2021droid-022
- The GRU receives global context by spatially averaging its hidden state, which the authors consider important for rejecting erroneous correspondences. (Teed & Deng, 2021) `ev:asserted` p. 5 ^teed2021droid-023
- Instead of predicting pose or depth updates directly, the GRU predicts a revision flow field with an associated confidence map. (Teed & Deng, 2021) `ev:reported` p. 5 ^teed2021droid-024
- Since each cost term includes a single depth variable, the DBA system is solved efficiently with the Schur complement. (Teed & Deng, 2021) `ev:reported` p. 5 ^teed2021droid-025
- During training, backpropagation is performed through the [[Differentiable optimization layers|Dense Bundle Adjustment layer]], which is implemented as part of the computation graph. (Teed & Deng, 2021) `ev:reported` p. 5 ^teed2021droid-026
- To remove gauge freedom during training, the first two poses are fixed to ground truth, removing the 6-dof and scale freedoms. (Teed & Deng, 2021) `ev:reported` p. 6 ^teed2021droid-027
- Each training example is a 7-frame video, sampled such that average flow between adjacent frames lies between 8px and 96px. (Teed & Deng, 2021) `ev:reported` p. 6 ^teed2021droid-028
- At inference the system runs two asynchronous threads: a frontend performing local bundle adjustment and a backend performing global bundle adjustment. (Teed & Deng, 2021) `ev:reported` p. 6 ^teed2021droid-029
- Initialization collects 12 frames, keeping a frame only when optical flow is greater than 16px, then runs 10 update iterations. (Teed & Deng, 2021) `ev:reported` p. 6 ^teed2021droid-030
- At inference, dense bundle adjustment uses a custom CUDA kernel exploiting block-sparse structure, followed by sparse Cholesky decomposition on the reduced camera block. (Teed & Deng, 2021) `ev:reported` p. 7 ^teed2021droid-031
- For RGB-D input, a term penalizing the squared distance between measured and predicted depth is added to the optimization objective. (Teed & Deng, 2021) `ev:reported` p. 7 ^teed2021droid-032
- For stereo input, the same system processes double the frames, with the left-right relative pose fixed in the DBA layer. (Teed & Deng, 2021) `ev:reported` p. 7 ^teed2021droid-033
- Evaluation focuses on camera trajectory accuracy using Absolute Trajectory Error, treating dense 3D reconstruction evaluation as outside the scope. (Teed & Deng, 2021) `ev:reported` p. 7 ^teed2021droid-034
- The network is trained for 250k steps with batch size 4, resolution 384 × 512, 7 frame clips, unrolling 15 update iterations. (Teed & Deng, 2021) `ev:reported` p. 7 ^teed2021droid-035
- Training DROID-SLAM takes 1 week on 4 RTX-3090 GPUs using monocular video from the synthetic TartanAir dataset. (Teed & Deng, 2021) `ev:reported` p. 7 ^teed2021droid-036
- On the TartanAir monocular Hard sequences, DROID-SLAM reaches an average ATE of 0.24 compared with 1.92 for TartanVO. (Teed & Deng, 2021) `ev:measured` p. 7 ^teed2021droid-037
- On TartanAir, DROID-SLAM achieves 20x lower average error than a DeepV2D baseline retrained on TartanAir by the authors. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021droid-038
- On the monocular TartanAir test set, DROID-SLAM scores 0.129 against 0.340 for SuperGlue, SuperPoint and COLMAP, a top ECCV 2020 submission. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021droid-039
- On the TartanAir stereo competition set, DROID-SLAM scores 0.047 against 0.119 for the SuperGlue, SuperPoint and COLMAP submission. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021droid-040
- DROID-SLAM runs 16x faster than the top two ECCV 2020 competition submissions, which are built on top of COLMAP. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021droid-041
- The authors report that in the monocular EuRoC setting DROID-SLAM achieves an average absolute trajectory error of 2.2cm. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021droid-042
- Recent deep learning approaches such as DeepFactors, DeepV2D and TartanVO perform poorly on EuRoC compared with classical SLAM systems. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021droid-043
- The authors attribute the poor EuRoC performance of prior deep methods to poor generalization and dataset biases causing large drift. (Teed & Deng, 2021) `ev:asserted` p. 8 ^teed2021droid-044
- D3VO evaluates on 6 of the 11 EuRoC sequences after unsupervised training on the remaining ones, which contain the same scenes. (Teed & Deng, 2021) `ev:cited` p. 8 ^teed2021droid-045
- The odometry-only DROID-SLAM variant has an average monocular EuRoC ATE of 0.186, versus 0.022 for the full system. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021droid-046
- The authors describe TUM-RGBD as notoriously difficult for monocular methods due to rolling shutter artifacts, motion blur and heavy rotation. (Teed & Deng, 2021) `ev:asserted` p. 8 ^teed2021droid-047
- On TUM-RGBD freiburg1, classical SLAM algorithms such as ORB-SLAM tend to fail on most of the sequences. (Teed & Deng, 2021) `ev:measured` p. 8 ^teed2021droid-048
- On TUM-RGBD, DROID-SLAM tracks all 9 sequences, achieving 83% lower ATE than DeepFactors, which also succeeds on all videos. (Teed & Deng, 2021) `ev:measured` p. 9 ^teed2021droid-049
- On TUM-RGBD, DROID-SLAM achieves 90% lower ATE than DeepV2D, with an average ATE of 0.038 across the freiburg1 sequences. (Teed & Deng, 2021) `ev:measured` p. 9 ^teed2021droid-050
- On the ETH3D-SLAM test split, DROID-SLAM reaches an AUC of 207.79, compared with 153.47 for BAD-SLAM, without any finetuning. (Teed & Deng, 2021) `ev:measured` p. 9 ^teed2021droid-051
- DROID-SLAM runs in real-time on 2 3090 GPUs, with tracking and local BA on the first GPU and global BA on the second. (Teed & Deng, 2021) `ev:reported` p. 9 ^teed2021droid-052
- On EuRoC the system averages 20fps by downsampling to 320 × 512 resolution and skipping every other frame. (Teed & Deng, 2021) `ev:measured` p. 9 ^teed2021droid-053
- Due to much faster camera motion on TartanAir, DROID-SLAM is unable to run in real-time, averaging 8fps on that dataset. (Teed & Deng, 2021) `ev:measured` p. 9 ^teed2021droid-054
- Results on EuRoC, TartanAir and ETH-3D, where video can be up to 5000 frames, require a GPU with 24GB memory. (Teed & Deng, 2021) `ev:reported` p. 9 ^teed2021droid-055
- The authors name memory and resource requirements as the biggest current limitation, believing culling redundant computation could drastically reduce them. (Teed & Deng, 2021) `ev:asserted` p. 9 ^teed2021droid-056
- In the stereo EuRoC setting, DROID-SLAM reaches an average ATE of 0.024 compared with 0.084 for ORB-SLAM3. (Teed & Deng, 2021) `ev:measured` p. 13 ^teed2021droid-057
- Compared with ORB-SLAM3 on stereo EuRoC, DROID-SLAM reduces the average ATE by 71% using its monocular-trained network. (Teed & Deng, 2021) `ev:measured` p. 13 ^teed2021droid-058
- Ablations on the TartanAir validation split show that the system benefits from both stereo video and global optimization. (Teed & Deng, 2021) `ev:measured` p. 13 ^teed2021droid-059
- The authors find the SLAM system unstable and prone to failure when the [[Differentiable optimization layers|DBA layer]] is not used during training. (Teed & Deng, 2021) `ev:measured` p. 13 ^teed2021droid-060

## 🎯 Contributions

## 📖 Glossary

- **SLAM** — Simultaneously building a map of the environment and localizing the agent within it.
- **Bundle Adjustment (BA)** — Joint least-squares optimization of camera poses and 3D structure.
- **Dense Bundle Adjustment (DBA) layer** — Differentiable Gauss-Newton layer updating poses and per-pixel inverse depth from flow revisions.
- **Frame graph** — Graph whose edges link co-visible frames; defines which frame pairs enter optimization.
- **Absolute Trajectory Error (ATE)** — Distance between estimated and ground-truth camera trajectories after alignment.
- **Gauge freedom** — Unobservable global pose and scale of a monocular reconstruction.
- **Schur complement** — Elimination of depth variables to solve a smaller reduced camera system.
- **Correlation volume** — All-pairs feature dot products between two frames, used for correspondence lookup.
- **Direct vs indirect SLAM** — Photometric-error methods versus feature-matching methods minimizing reprojection error.

## ❓ Open questions

- Can the backend's memory demand (24GB for long videos) be cut enough for embedded or single-GPU deployment?
- How does the system behave in scenes with large dynamic objects beyond what global context pooling handles?
- Would fine-tuning on real data improve over the synthetic-only TartanAir training?
- How good is the dense 3D reconstruction itself, which the paper leaves unevaluated?
- Can inertial (IMU) measurements be added to the DBA objective as easily as depth or stereo?

## 📝 Notes on reading

Read from arXiv v2 (2 Feb 2022), the NeurIPS 2021 version. Figure 4 (right, ETH3D successful datasets vs ATE), Figure 6 (local vs full optimization, number of keyframes) and Figure 7 (global pooling; RAFT + BA vs DBA training) are plots only described in text; no values were claimed from them. The appendix Jacobian equations (p. 14) are garbled by extraction and were not claimed. On p. 3 the text says the method combines the smoother objective of indirect approaches with the greater modeling capacity of indirect approaches; the second should likely read direct. Table 2 scores are normalized relative pose error, not ATE. Table 1 reports ATE without units. The TUM-RGBD table notes DeepTAM uses RGB-D and TartanVO uses ground-truth scale, so those comparisons are not strictly monocular. The claim that global BA runs on the second GPU also includes loop closure. Five keyframes are used in the experiments per Fig. 6 caption.

## Suggested new concepts

- Dense Bundle Adjustment layer — a differentiable optimization layer reused across learned SLAM and VO systems.
- Frame graph / co-visibility graph — central data structure for local and global optimization and loop closure.
- Differentiable optimization layers — pattern of embedding classical solvers inside trained networks.
- Sim-to-real generalization in SLAM — training only on synthetic TartanAir yet transferring to real benchmarks.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — *Dense BA* diferenciable con lietorch
