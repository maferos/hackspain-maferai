---
aliases: []
type: "source"
title: "PyPose: A Library for Robot Learning with Physics-based Optimization"
citekey: "Wang2022pypose"
doi: "10.48550/arXiv.2209.15428"
arxiv: "2209.15428"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2209.15428"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Chen Wang", "Dasong Gao", "Kuan Xu", "Junyi Geng", "Yaoyu Hu", "Yuheng Qiu", "Bowen Li", "Fan Yang", "Brady Moon", "Abhinav Pandey", " Aryan", "Jiahe Xu", "Tianhao Wu", "Haonan He", "Daning Huang", "Zhongqiang Ren", "Shibo Zhao", "Taimeng Fu", "Pranay Reddy", "Xiao Lin", "Wenshan Wang", "Jingnan Shi", "Rajat Talak", "Kun Cao", "Yi Du", "Han Wang", "Huai Yu", "Shanzhao Wang", "Siyu Chen", "Ananth Kashyap", "Rohan Bandaru", "Karthik Dantu", "Jiajun Wu", "Lihua Xie", "Luca Carlone", "Marco Hutter", "Sebastian Scherer"]
sha256: ["60ee1b6d3661088763c206ffdf4a82309156946ae2ad65d9bd23a07b331bbd91"]
pdf: "Content/Papers/Wang2022pypose.pdf"
topics: ["[[Optimización y algoritmos]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Wang2022pypose.pdf]]

> [!abstract] One-sentence summary
> PyPose is an open-source PyTorch library that adds differentiable Lie groups, 2nd-order optimizers and robotics modules so perception networks and physics-based optimization can be trained end to end, with large speedups over LieTorch and Theseus.

## Abstract

Deep learning has had remarkable success in robotic perception, but its data-centric nature suffers when it comes to generalizing to ever-changing environments. By contrast, physics-based optimization generalizes better, but it does not perform as well in complicated tasks due to the lack of high-level semantic information and reliance on manual parametric tuning. To take advantage of these two complementary worlds, we present PyPose: a robotics-oriented, PyTorch-based library that combines deep perceptual models with physics-based optimization. PyPose's architecture is tidy and well-organized, it has an imperative style interface and is efficient and user-friendly, making it easy to integrate into real-world robotic applications. Besides, it supports parallel computing of any order gradients of Lie groups and Lie algebras and $2^{\text{nd}}$-order optimizers, such as trust region methods. Experiments show that PyPose achieves more than $10\times$ speedup in computation compared to the state-of-the-art libraries. To boost future research, we provide concrete examples for several fields of robot learning, including SLAM, planning, control, and inertial navigation. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that learning-based methods and physics-based optimization are typically used separately in different modules of a robotic system. (Wang et al., 2022) `ev:cited` p. 1 ^wang2022pypose-001
- The authors argue that a two-stage, decoupled front-end and back-end paradigm may only achieve sub-optimal solutions, limiting system performance and generalization. (Wang et al., 2022) `ev:asserted` p. 1 ^wang2022pypose-002
- The authors argue that mixing Python learning models with C++ optimization libraries like GTSAM increases system complexity and slows the development cycle. (Wang et al., 2022) `ev:asserted` p. 2 ^wang2022pypose-003
- LieTorch performs back-propagation in manifold tangent spaces but implements only 1st-order differentiable operations, which the authors say limits its practical use. (Wang et al., 2022) `ev:cited` p. 2 ^wang2022pypose-004
- CvxpyLayer treats convex optimization as a [[Differentiable optimization layers|differentiable neural network layer]] but does not support Lie group operations or 2nd-order optimizers. (Wang et al., 2022) `ev:cited` p. 2 ^wang2022pypose-005
- Theseus takes [[Differentiable optimization layers|non-linear optimization as network layers]] but adopts rotation matrices, which the authors call memory inefficient for practical robotic applications. (Wang et al., 2022) `ev:cited` p. 2 ^wang2022pypose-006
- PyPose is an open-source PyTorch-based library connecting learning-based perceptual models with classical algorithms that can be formulated as physics-based optimization. (Wang et al., 2022) `ev:reported` p. 2 ^wang2022pypose-007
- Among its listed contributions, PyPose provides 2nd-order optimizers such as Levenberg-Marquardt with trust region steps for end-to-end learning. (Wang et al., 2022) `ev:reported` p. 2 ^wang2022pypose-008
- The authors report that PyPose achieves more than 10× faster computation compared with state-of-the-art libraries in their experiments. (Wang et al., 2022) `ev:measured` p. 2 ^wang2022pypose-009
- The authors describe PyPose as one of the first Python libraries to comprehensively cover several robotics sub-fields where optimization is involved. (Wang et al., 2022) `ev:asserted` p. 2 ^wang2022pypose-010
- PyPose is organised around four concepts for end-to-end learning with physics-based optimization: LieTensor, Module, Function, and Optimizer. (Wang et al., 2022) `ev:reported` p. 3 ^wang2022pypose-011
- The authors state that neglecting the manifold structure of 3D transformations will lead to inconsistent gradient computation and numerical issues. (Wang et al., 2022) `ev:asserted` p. 3 ^wang2022pypose-012
- LieTensor is defined as a subclass of PyTorch's Tensor that uses Lie theory to represent 3D transformations in learning models. (Wang et al., 2022) `ev:reported` p. 3 ^wang2022pypose-013
- To avoid division by zero in terms such as sin x over x, PyPose computes the [[Exponential map|exponential map]] with a Taylor expansion. (Wang et al., 2022) `ev:reported` p. 3 ^wang2022pypose-014
- LieTensor supports automatic differentiation of any order gradient on CPU, GPU, TPU, and Apple silicon GPU devices. (Wang et al., 2022) `ev:reported` p. 3 ^wang2022pypose-015
- LieTensor supports parallel gradient computation with the vmap operator, which the authors say computes Jacobian matrices much faster. (Wang et al., 2022) `ev:reported` p. 3 ^wang2022pypose-016
- PyPose represents transformations with quaternions, which the authors note store only four scalars and have no gimbal lock issues. (Wang et al., 2022) `ev:reported` p. 3 ^wang2022pypose-017
- According to the authors, LieTorch, JaxLie, and Theseus support only Lie groups, whereas PyPose supports both Lie groups and Lie algebras. (Wang et al., 2022) `ev:cited` p. 3 ^wang2022pypose-018
- LieTensor class aliases cover the SO3, SE3, Sim3, and RxSO3 Lie groups together with their corresponding Lie algebras. (Wang et al., 2022) `ev:reported` p. 3 ^wang2022pypose-019
- In PyPose, a Module has the same functionality as a Function but also stores parameters that an optimizer can update. (Wang et al., 2022) `ev:reported` p. 4 ^wang2022pypose-020
- PyPose provides modules including a system transition function, model predictive control, a Kalman filter, and IMU preintegration. (Wang et al., 2022) `ev:reported` p. 4 ^wang2022pypose-021
- PyPose's optimizer interface exposes solver, kernel, corrector, and strategy components, illustrated with the 2nd-order Levenberg-Marquardt optimizer. (Wang et al., 2022) `ev:reported` p. 4 ^wang2022pypose-022
- Triggs' correction needs the 2nd-order derivative of the robust kernel, which the authors say can make optimizers like LM unstable. (Wang et al., 2022) `ev:cited` p. 4 ^wang2022pypose-023
- PyPose introduces a FastTriggs corrector that involves only the kernel's 1st-order derivative and is described as faster yet more stable. (Wang et al., 2022) `ev:asserted` p. 4 ^wang2022pypose-024
- Step-restricting strategies such as TrustRegion are used by passing a strategy instance to the optimizer constructor in PyPose. (Wang et al., 2022) `ev:reported` p. 5 ^wang2022pypose-025
- Runtime was benchmarked on exponential-logarithm mapping, rotation composition, and point rotation, built with the same input and output shapes for all libraries. (Wang et al., 2022) `ev:reported` p. 5 ^wang2022pypose-026
- The efficiency metric was the number of operations per second for each function and for its Jacobian with respect to x. (Wang et al., 2022) `ev:reported` p. 5 ^wang2022pypose-027
- Theseus Jacobians were computed with AutoDiffCostFunction because that method is used in its optimizers and reflects optimization performance. (Wang et al., 2022) `ev:reported` p. 5 ^wang2022pypose-028
- For the dense Jacobian of the Log(Exp(x)) operator on a CPU, PyPose was up to 37.9× faster than Theseus. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-029
- For the dense Jacobian of the Log(Exp(x)) operator on a CPU, PyPose was up to 8.8× faster than LieTorch. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-030
- For the dense Jacobian of the Log(Exp(x)) operator on a GPU, PyPose was up to 42.9× faster than Theseus. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-031
- For the dense Jacobian of the Log(Exp(x)) operator on a GPU, PyPose was up to 8.6× faster than LieTorch. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-032
- LieTorch was left out of the batched comparison because computing its batched Jacobian requires a slow Python loop. (Wang et al., 2022) `ev:reported` p. 6 ^wang2022pypose-033
- For batched operations on a CPU, PyPose was up to 1.8×, 2.8×, and 2.2× faster than Theseus for the three operations. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-034
- For batched operations on a GPU, PyPose was up to 7.4×, 32.9×, and 17.4× faster than Theseus for the three operations. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-035
- For batched Jacobians on a CPU, PyPose was up to 7.3×, 16.1×, and 11.1× faster than Theseus for the three operations. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-036
- For batched Jacobians on a GPU, PyPose was up to 3.0×, 14.4×, and 11.4× faster than Theseus for the three operations. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-037
- PyPose needed only about 1/4 to 1/2 of the memory space required by Theseus in the batched benchmarks. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-038
- The authors note that runtime usually fluctuates within 10%, and they report the average performance over multiple tests. (Wang et al., 2022) `ev:reported` p. 6 ^wang2022pypose-039
- A relative performance drop at certain batch sizes might be caused by cache misses or imbalanced Linux OS resource management, the authors suggest. (Wang et al., 2022) `ev:asserted` p. 6 ^wang2022pypose-040
- In the transformation-inverse benchmark at the smallest batch, LM reached a final error of 5.96E-5 versus 5.10E+1 for SGD. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-041
- At the largest batch size, LM's final error was 3.77E-2, compared with 6.86E+3 for SGD and 1.16E+5 for Adam. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-042
- At the largest batch size, LM had the longest runtime, 51.6, against 31.5 for SGD and 40.5 for Adam. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-043
- The authors note that 2nd-order optimizers need Jacobians, which require significant memory and may increase the runtime. (Wang et al., 2022) `ev:asserted` p. 6 ^wang2022pypose-044
- In the Garage pose graph optimization example using LM with a TrustRegion strategy, PyPose reached the same final error as Ceres and GTSAM. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-045
- In the Garage pose graph example, the error fell from 16727.20 before optimization to 1.255874 after LM optimization. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-046
- The SLAM example learns the front end self-supervised, using estimated poses and landmark positions as pseudo-labels for supervision. (Wang et al., 2022) `ev:reported` p. 6 ^wang2022pypose-047
- In the SLAM example, the front end employs SuperPoint for feature extraction and CAPS for feature matching. (Wang et al., 2022) `ev:reported` p. 6 ^wang2022pypose-048
- The LM-based PyPose backend performs bundle adjustment and back-propagates the final projection error to update the CAPS feature matcher. (Wang et al., 2022) `ev:reported` p. 6 ^wang2022pypose-049
- A CAPS network pretrained on MegaDepth was finetuned on TartanAir with only image input, in batches of 6 frames. (Wang et al., 2022) `ev:reported` p. 7 ^wang2022pypose-050
- Over 38 TartanAir sequences, mean matching accuracy rose from 19.74% to 28.27% after self-supervised training, a +43.24% improvement. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-051
- After self-supervised training, matching accuracy improved by + 49.94% on the easy sequences, compared with + 35.33% on the hard sequences. (Wang et al., 2022) `ev:measured` p. 6 ^wang2022pypose-052
- On a test sequence, the trained model ran to completion with an ATE of 0.63 m, whereas the original model quickly lost track. (Wang et al., 2022) `ev:measured` p. 7 ^wang2022pypose-053
- The planning example maps depth sensor inputs directly into kinodynamically feasible trajectories, using the SE3 LieTensor as a [[Differentiable optimization layers|differential optimization layer]]. (Wang et al., 2022) `ev:reported` p. 7 ^wang2022pypose-054
- In Matterport3D, the end-to-end planner achieved around 3× speedup on average over a traditional motion-primitives-based planning framework. (Wang et al., 2022) `ev:measured` p. 7 ^wang2022pypose-055
- In the planning experiment, the robot followed 20 manually inputted waypoints for global guidance while avoiding local obstacles autonomously. (Wang et al., 2022) `ev:reported` p. 7 ^wang2022pypose-056
- The end-to-end planning policy has been integrated and tested in the field on a real ANYmal legged robot. (Wang et al., 2022) `ev:reported` p. 7 ^wang2022pypose-057
- The control example reproduces the Diff-MPC imitation learning problem, where expert and learner LQRs share everything except linear system parameters. (Wang et al., 2022) `ev:reported` p. 7 ^wang2022pypose-058
- PyPose differentiates through MPC by applying one extra optimization iteration at the optimal point in the forward pass. (Wang et al., 2022) `ev:reported` p. 8 ^wang2022pypose-059
- PyPose and Diff-MPC achieved the same learning performance on model and trajectory losses for four trajectories with random initial conditions. (Wang et al., 2022) `ev:measured` p. 8 ^wang2022pypose-060
- PyPose's MPC backward time was always shorter than Diff-MPC's, which needs an additional LQR iteration in the backward pass. (Wang et al., 2022) `ev:measured` p. 8 ^wang2022pypose-061
- As the system dimension increased, PyPose's MPC runtime got longer due to the extra evaluation iteration in the forward pass. (Wang et al., 2022) `ev:measured` p. 8 ^wang2022pypose-062
- PyPose's IMUPreintegrator module performs differentiable IMU preintegration with covariance propagation, supporting batched operation and integration on the manifold. (Wang et al., 2022) `ev:reported` p. 8 ^wang2022pypose-063
- On a KITTI sequence, the IMU-integrated trajectory drifted from accumulated sensor noise, which PGO with GPS for every 5s segment improved. (Wang et al., 2022) `ev:measured` p. 8 ^wang2022pypose-064
- The IMU calibration network was trained on 5 EuRoC sequences and evaluated on 5 testing sequences using position and rotation RMSE. (Wang et al., 2022) `ev:reported` p. 8 ^wang2022pypose-065
- On MH_02_easy, rotation error over 1s of preintegration fell from 0.659 with standard preintegration to 0.012 with the learned calibration. (Wang et al., 2022) `ev:measured` p. 8 ^wang2022pypose-066
- The authors acknowledge that PyPose is in an early stage, with overall stability not yet mature compared to PyTorch. (Wang et al., 2022) `ev:asserted` p. 8 ^wang2022pypose-067
- The authors state that PyPose's efficiency is still not comparable with C(++)-based libraries, although it offers an alternative for robot learning. (Wang et al., 2022) `ev:asserted` p. 8 ^wang2022pypose-068
- The authors plan to add sparse block tensors, sparse Jacobian computation, and constrained optimization to PyPose in the future. (Wang et al., 2022) `ev:asserted` p. 8 ^wang2022pypose-069

## 🎯 Contributions

## 📖 Glossary

- **LieTensor** — PyPose's Tensor subclass representing 3D transformations as Lie group or Lie algebra elements.
- **Lie algebra** — Tangent space of a Lie group, where transformations are expressed as vectors.
- **Exp / Log map** — Conversions between a Lie algebra vector and its Lie group element.
- **Levenberg-Marquardt (LM)** — Damped Gauss-Newton 2nd-order least-squares optimizer.
- **Trust region** — Strategy that restricts each optimizer step to a region where the model is trusted.
- **FastTriggs** — PyPose robust-kernel corrector using only the kernel's 1st-order derivative.
- **Pose graph optimization (PGO)** — Optimizing poses linked by relative-pose constraints to reduce accumulated error.
- **IMU preintegration** — Summarizing many IMU samples between keyframes into one relative-motion constraint.
- **Differentiable MPC** — Model predictive control whose optimization can be back-propagated to learn costs or dynamics.

## ❓ Open questions

- How close can PyPose's runtime get to C(++)-based solvers such as Ceres or GTSAM once sparse Jacobians and sparse block tensors land?
- Does the FastTriggs corrector remain more stable than Triggs' correction across diverse robust kernels and real datasets? The paper gives no quantitative comparison.
- How does the extra forward-pass iteration of the MPC gradient scale for high-dimensional systems beyond the benchmark sizes shown?
- Do the self-supervised SLAM front-end gains transfer beyond TartanAir, and to full trajectories rather than one test sequence?
- How does the IMU calibration network generalize beyond the five EuRoC testing sequences?

## 📝 Notes on reading

Read the arXiv v3 preprint (24 Mar 2023), 12 pages including a supplementary with sample code for LieTensor and the LM optimizer (p. 12). Equations on pp. 3-4 are garbled in the extraction and were not claimed. The bar values of Figures 1 and 2 (pp. 4-5) are extracted without panel labels that map clearly to the three operations; claims use the numbers stated in the body text on p. 6. Figure 1 bar labels (e.g., 49.2, 43.7) do not obviously match the 37.9× and 42.9× figures in the text, since the figure normalises LieTorch as 5×. The text says matching accuracy increased by up to 50%, while Table 3 gives + 49.94% as the largest gain. Batch sizes such as 10^7 are extracted as 107, so batch-size numbers were not claimed. Table 2 time values carry no unit. Figure 5a (planning time) and Figure 6c-d (MPC runtime vs number of states) could only be described qualitatively.

## Suggested new concepts

- Differentiable optimization layers — PyPose, Theseus, CvxpyLayer and LieTorch all embed solvers in networks; a concept note would compare them.
- Lie group representations for learning — quaternion vs rotation-matrix choices affect memory, gradients and numerical stability across libraries.
- Self-supervised SLAM front-end training — using back-end bundle adjustment residuals as supervision for feature matchers.
- Learned IMU calibration — denoising IMU signals with networks trained through differentiable preintegration.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — `LieTensor` + optimizadores LM con trust region; librería recomendada en F.
- **[[03_aplicaciones_vision_por_computador]]** — Grupos de Lie y optimizadores de 2.º orden en PyTorch

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
