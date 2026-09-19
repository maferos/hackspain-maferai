---
aliases: []
type: "source"
title: "Riemannian Flow Matching Policy for Robot Motion Learning"
citekey: "Braun2024riemannian"
doi: "10.48550/arXiv.2403.10672"
arxiv: "2403.10672"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2403.10672"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Max Braun", "Noémie Jaquier", "Leonel Rozo", "Tamim Asfour"]
sha256: ["2eaa20492375c4f4584cc21c7907a384630019705e9809700d82e7795afc00cf"]
pdf: "Content/Papers/Braun2024riemannian.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 56
---

📄 PDF: [[Braun2024riemannian.pdf]]

> [!abstract] One-sentence summary
> The paper introduces RFMP, a flow-matching robot policy that respects Riemannian geometry and, on LASA proof-of-concept tasks, gives smoother trajectories than Diffusion Policies, with faster inference in most settings tested.

## Abstract

We introduce Riemannian Flow Matching Policies (RFMP), a novel model for learning and synthesizing robot visuomotor policies. RFMP leverages the efficient training and inference capabilities of flow matching methods. By design, RFMP inherits the strengths of flow matching: the ability to encode high-dimensional multimodal distributions, commonly encountered in robotic tasks, and a very simple and fast inference process. We demonstrate the applicability of RFMP to both state-based and vision-conditioned robot motion policies. Notably, as the robot state resides on a Riemannian manifold, RFMP inherently incorporates geometric awareness, which is crucial for realistic robotic tasks. To evaluate RFMP, we conduct two proof-of-concept experiments, comparing its performance against Diffusion Policies. Although both approaches successfully learn the considered tasks, our results show that RFMP provides smoother action trajectories with significantly lower inference times. (arXiv)

## 🧠 Key ideas (atomic)

- Diffusion-based robot policies often require solving a stochastic differential equation, making inference expensive and possibly hindering reactive motion policies (Braun et al., 2024) `ev:cited` p. 1 ^braun2024riemannian-001
- On Riemannian manifolds, computing the score function of a diffusion process is not as simple as in the Euclidean case (Braun et al., 2024) `ev:cited` p. 1 ^braun2024riemannian-002
- The authors propose the Riemannian Flow Matching Policy (RFMP) to learn sensorimotor robot skills represented by end-effector pose trajectories using flow matching (Braun et al., 2024) `ev:asserted` p. 1 ^braun2024riemannian-003
- The authors claim to pioneer the application of flow matching methods within sensorimotor robot policy learning, validated on the LASA benchmark dataset (Braun et al., 2024) `ev:asserted` p. 1 ^braun2024riemannian-004
- The paper identifies slow training, caused by integrating the associated ODE, as a shortcoming of normalizing flows used as robot policies (Braun et al., 2024) `ev:cited` p. 1 ^braun2024riemannian-005
- The authors state their [[Flow matching policy|flow matching]] choice stems from avoiding complex normalizing-flow training procedures and the computationally expensive inference of diffusion models (Braun et al., 2024) `ev:asserted` p. 2 ^braun2024riemannian-006
- RFMP accounts for full-pose trajectories by building on the [[Riemannian flow matching|Riemannian extension of flow matching]] proposed by Chen and Lipman (Braun et al., 2024) `ev:cited` p. 2 ^braun2024riemannian-007
- The paper adopts the [[Flow matching policy|Gaussian conditional flow matching]] of Lipman et al., with a probability path from a zero-mean normal toward each target sample (Braun et al., 2024) `ev:reported` p. 2 ^braun2024riemannian-008
- Riemannian conditional flow matching computes the regression loss with respect to the manifold's Riemannian metric instead of the Euclidean norm (Braun et al., 2024) `ev:cited` p. 3 ^braun2024riemannian-009
- The conditional flow uses geodesic paths between base and target samples, which have closed forms on hyperspheres, SO(3) and SPD manifolds (Braun et al., 2024) `ev:reported` p. 3 ^braun2024riemannian-010
- RFMP adapts [[Riemannian flow matching]] to policies by conditioning the parametrized vector field on the observation vector (Braun et al., 2024) `ev:reported` p. 3 ^braun2024riemannian-011
- Inspired by diffusion policies, RFMP predicts [[Action chunking|a receding horizon of actions]] to achieve temporal consistency and smoothness in the predicted actions (Braun et al., 2024) `ev:reported` p. 3 ^braun2024riemannian-012
- The observation vector combines a reference observation, a uniformly sampled context observation and the index distance between them, following Davtyan et al. (Braun et al., 2024) `ev:reported` p. 3 ^braun2024riemannian-013
- The authors state that combining reference and context observations supplies motion-direction information that a single observation lacks (Braun et al., 2024) `ev:asserted` p. 3 ^braun2024riemannian-014
- At inference, RFMP integrates the learned vector field over [0, 1] with an ODE solver and executes only the first Te predicted actions (Braun et al., 2024) `ev:reported` p. 3 ^braun2024riemannian-015
- The Euclidean case uses the DOPRI solver in torchdyn, whereas the Riemannian case uses a Riemannian Euler-based ODE solver (Braun et al., 2024) `ev:reported` p. 3 ^braun2024riemannian-016
- The RFMP vector field is a multilayer perceptron with 64 hidden units, 5 layers and learnable Swish activations, totalling 32K parameters (Braun et al., 2024) `ev:reported` p. 3 ^braun2024riemannian-017
- Training used Adam with learning rate 1e−4, weight exponential moving averaging with decay 0.999, and 200 epochs (Braun et al., 2024) `ev:reported` p. 3 ^braun2024riemannian-018
- Data were split into 80% training, 10% validation and 10% test, with the best model selected on validation performance (Braun et al., 2024) `ev:reported` p. 3 ^braun2024riemannian-019
- The base distribution is a Gaussian with σ = 1 in R2 and a wrapped Gaussian with σ = 0.5 on S2 (Braun et al., 2024) `ev:reported` p. 4 ^braun2024riemannian-020
- Experiments use the LASA dataset in R2 and projected onto the sphere S2, for trajectory-based and visuomotor policies (Braun et al., 2024) `ev:reported` p. 4 ^braun2024riemannian-021
- Each trajectory-based dataset contains M = 7 demonstrations of 200 timesteps, with prediction horizon Ta = 8 and execution horizon Te = Ta/2 (Braun et al., 2024) `ev:reported` p. 4 ^braun2024riemannian-022
- The authors observe that RFMP-reconstructed distributions closely match the original demonstrations for the letters S and W on R2 and S2 (Braun et al., 2024) `ev:measured` p. 4 ^braun2024riemannian-023
- From randomly sampled initial conditions near the demonstrations, RFMP generates trajectories that closely follow the demonstration pattern (Braun et al., 2024) `ev:measured` p. 4 ^braun2024riemannian-024
- The baseline is the Diffusion Policy CNN network with 256M parameters, trained with iDDPM and 100 denoising iterations (Braun et al., 2024) `ev:reported` p. 4 ^braun2024riemannian-025
- Unlike RFMP, Diffusion Policy trajectories from perturbed initial conditions tend to rejoin the demonstration support, giving less variance across reproductions (Braun et al., 2024) `ev:measured` p. 4 ^braun2024riemannian-026
- The authors suggest Diffusion Policy's return to the data support might partly reflect high memorization of training data, pending further investigation (Braun et al., 2024) `ev:asserted` p. 4 ^braun2024riemannian-027
- The authors hypothesize that the jerkier [[Diffusion Policy]] trajectories result from the inherent stochasticity of diffusion models during inference (Braun et al., 2024) `ev:asserted` p. 4 ^braun2024riemannian-028
- Diffusion Policy shows similar or lower dynamic time warping distance than RFMP on the unimodal trajectory-based datasets (Braun et al., 2024) `ev:measured` p. 5 ^braun2024riemannian-029
- On the S dataset in R2, trajectory-based RFMP jerkiness was 2120 ± 273 versus 8172 ± 747 for Diffusion Policy (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-030
- On the S dataset in R2, trajectory-based RFMP DTWD was 1.87 ± 0.94 versus 0.98 ± 0.22 for Diffusion Policy (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-031
- On the W dataset on S2, trajectory-based RFMP jerkiness was 4198 ± 560 versus 2944 ± 1399 for Diffusion Policy (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-032
- [[Diffusion Policy]] does not guarantee trajectories stay on the manifold, and some S-on-S2 trajectories entered the sphere (Braun et al., 2024) `ev:measured` p. 5 ^braun2024riemannian-033
- The authors state that projecting off-manifold predictions back is known to produce highly inaccurate predictions, as it disregards the intrinsic data geometry (Braun et al., 2024) `ev:cited` p. 5 ^braun2024riemannian-034
- Both RFMP and Diffusion Policy learned [[Multimodal action distributions|a multimodal pattern]] from mirrored letter-L demonstrations on S2 (Braun et al., 2024) `ev:measured` p. 5 ^braun2024riemannian-035
- On the multimodal L dataset, RFMP DTWD was 6.14 ± 6.56 versus 7.06 ± 7.73 for Diffusion Policy (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-036
- In the horizon ablation, RFMP trajectories remained smooth even with prediction horizon Ta = 2, while Diffusion Policy became jerkier (Braun et al., 2024) `ev:measured` p. 5 ^braun2024riemannian-037
- With Ta = 2 in R2, RFMP jerkiness was 3454 ± 276 versus 11905 ± 1962 for Diffusion Policy (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-038
- With Ta = 2 in R2, Diffusion Policy achieved lower DTWD than RFMP, 0.70 ± 0.07 against 1.13 ± 0.29 (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-039
- Inference times were measured on a laptop with a 2.60GHz ×12 CPU, an Nvidia Quatro T200 GPU and 31 GB RAM (Braun et al., 2024) `ev:reported` p. 5 ^braun2024riemannian-040
- In the Euclidean trajectory-based case, RFMP reduced inference time by about 30% (∼350ms) compared with Diffusion Policy (Braun et al., 2024) `ev:measured` p. 5 ^braun2024riemannian-041
- Trajectory-based inference per prediction step took 803 ± 55 ms for RFMP versus 1142 ± 17 ms for Diffusion Policy on S in R2 (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-042
- On the sphere S2, trajectory-based RFMP inference time exceeded Diffusion Policy's, at 1539 ± 23 ms versus 1147 ± 26 ms (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-043
- The authors attribute slower RFMP inference on S2 to Riemannian-specific ODE solvers, while Diffusion Policy ignores geometry and uses Euclidean solvers (Braun et al., 2024) `ev:asserted` p. 5 ^braun2024riemannian-044
- The visuomotor variant conditions RFMP on latent encodings of 48×48 grayscale images from the Diffusion Policy ResNet-18 backbone (Braun et al., 2024) `ev:reported` p. 6 ^braun2024riemannian-045
- The ResNet-18 encoder replaces global average pooling with spatial softmax pooling and BatchNorm with GroupNorm, and is trained end-to-end (Braun et al., 2024) `ev:reported` p. 6 ^braun2024riemannian-046
- The authors empirically observed that shortening the context-observation horizon to w = 50 improves temporal consistency and smoothness in visuomotor RFMP (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-047
- Visuomotor RFMP reproduces trajectories matching the demonstration patterns in both the Euclidean and the Riemannian settings (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-048
- Visuomotor RFMP performed competitively with visuomotor Diffusion Policy on DTWD despite a simpler architecture parametrizing its vector field (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-049
- For visuomotor S on S2, RFMP jerkiness was 3590 ± 353 versus 5903 ± 170 for Diffusion Policy (Braun et al., 2024) `ev:measured` p. 7 ^braun2024riemannian-050
- For visuomotor S in R2, RFMP jerkiness was 10543 ± 612, higher than 6198 ± 755 for Diffusion Policy (Braun et al., 2024) `ev:measured` p. 7 ^braun2024riemannian-051
- For visuomotor policies, RFMP reduced inference time by about 45% (∼900ms) compared with Diffusion Policy (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-052
- Visuomotor inference per step on S2 was 2351 ± 88 ms for RFMP versus 2662 ± 541 ms for Diffusion Policy (Braun et al., 2024) `ev:measured` p. 6 ^braun2024riemannian-053
- The authors conclude that RFMP achieved competitive performance with a simple MLP vector field, unlike the more powerful CNN used by Diffusion Policy (Braun et al., 2024) `ev:asserted` p. 7 ^braun2024riemannian-054
- The authors argue that smoother actions and faster inference make RFMP a compelling choice for real-time robotic applications (Braun et al., 2024) `ev:asserted` p. 7 ^braun2024riemannian-055
- Future work will evaluate RFMP in real-world robotics applications and explore more powerful vector-field representations and more informative priors (Braun et al., 2024) `ev:asserted` p. 7 ^braun2024riemannian-056

## 🎯 Contributions


## 📖 Glossary

- **Flow matching (FM)** — Simulation-free generative model regressing a vector field that transports a base density to data.
- **Conditional flow matching (CFM)** — Tractable FM loss using per-sample conditional probability paths with identical gradients.
- **Riemannian CFM (RCFM)** — CFM extended to manifolds, with geodesic flows and metric-weighted loss.
- **Diffusion Policy (DP)** — Visuomotor policy generating action sequences by iterative denoising diffusion.
- **Receding horizon** — Predict Ta future actions, execute only the first Te, then replan.
- **Wrapped Gaussian** — Gaussian defined in a tangent space and mapped onto the manifold via the exponential map.
- **Exponential / logarithmic map** — Maps between a tangent space and the manifold along geodesics.
- **LASA dataset** — Benchmark of 2D handwritten-letter motion demonstrations for learned reaching motions.
- **DTWD** — Dynamic time warping distance, used as trajectory reproduction accuracy.
- **Jerkiness** — Movement smoothness measure; lower values mean smoother trajectories.

## ❓ Open questions

- How does RFMP perform on real robots and real-world tasks rather than LASA letter trajectories?
- Would a Riemannian diffusion policy with Riemannian SDE solvers change the inference-time comparison on S2?
- Does Diffusion Policy's return to the data support reflect memorization, as the authors suggest without testing?
- Why is visuomotor RFMP jerkier than Diffusion Policy in R2 but smoother on S2?
- Would richer vector-field architectures or more informative priors improve RFMP accuracy (DTWD)?
- How does RFMP scale to full SE(3) end-effector poses and higher-dimensional action spaces, beyond S2 positions?

## 📝 Notes on reading

Version read: arXiv 2403.10672v2 (27 Aug 2024). The registry abstract says "visuomotor policies" where the PDF abstract says "sensorimotor policies".

Table layouts (Tables I–IV, p. 6–7) were flattened in extraction; values were assigned to columns by header order and cross-checked against the text (e.g. the ∼350ms Euclidean reduction matches 1142 − 803). The visuomotor ∼45% (∼900ms) reduction does not exactly match Table III (2462 vs 1355 ms on S in R2, i.e. ~1107 ms).

Internal tension: the text and conclusion say RFMP is smoother, but Table I shows higher RFMP jerkiness on W on S2 (4198 vs 2944), and Table IV shows higher RFMP jerkiness for visuomotor S and J in R2 (10543 vs 6198; 7655 vs 5588). The text itself limits the visuomotor smoothness claim to "especially for policies on S2". The claim of "significantly lower inference times" does not hold for trajectory-based S2 (1539 vs 1147 ms); no significance test is reported. The text refers to "Algorithm 8" where Algorithm 1 is meant.

Figures 1–5 show learned flows and trajectories qualitatively; they are described in claims only through the authors' textual observations. The experiments manifolds are R2 and S2 only; the orientation (S3/SO(3)) motivation is not tested.

## Suggested new concepts

- Flow matching policy — a policy class alternative to diffusion policies with ODE-based, faster inference.
- Riemannian flow matching — generative modelling on manifolds via geodesic conditional flows; relevant to pose/orientation actions.
- Action chunking with receding horizon — shared design across diffusion and flow policies affecting smoothness.
- Geometry-aware robot learning — keeping predictions on the manifold instead of post-hoc projection.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — RFM aplicado a políticas visuomotoras (C.5).
