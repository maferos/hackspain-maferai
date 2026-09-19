---
aliases: []
type: "source"
title: "On-Manifold Preintegration for Real-Time Visual-Inertial Odometry"
citekey: "Forster2016manifold"
doi: "10.48550/arXiv.1512.02363"
arxiv: "1512.02363"
year: 2016
publication_type: "preprint"
url: "https://arxiv.org/abs/1512.02363"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Christian Forster", "Luca Carlone", "Frank Dellaert", "Davide Scaramuzza"]
sha256: ["214b8bee53e1fb6218c1cec1352d74c24951feec815517e6a0cc6dfcf1fd8f32"]
pdf: "Content/Papers/Forster2016manifold.pdf"
topics: ["[[Matemáticas]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 59
---

📄 PDF: [[Forster2016manifold.pdf]]

> [!abstract] One-sentence summary
> The paper develops an IMU preintegration theory on the rotation manifold SO(3) and embeds it with structureless vision factors in an iSAM2 factor graph, giving accurate real-time monocular visual-inertial odometry.

## Abstract

Current approaches for visual-inertial odometry (VIO) are able to attain highly accurate state estimation via nonlinear optimization. However, real-time optimization quickly becomes infeasible as the trajectory grows over time, this problem is further emphasized by the fact that inertial measurements come at high rate, hence leading to fast growth of the number of variables in the optimization. In this paper, we address this issue by preintegrating inertial measurements between selected keyframes into single relative motion constraints. Our first contribution is a \emph{preintegration theory} that properly addresses the manifold structure of the rotation group. We formally discuss the generative measurement model as well as the nature of the rotation noise and derive the expression for the \emph{maximum a posteriori} state estimator. Our theoretical development enables the computation of all necessary Jacobians for the optimization and a-posteriori bias correction in analytic form. The second contribution is to show that the preintegrated IMU model can be seamlessly integrated into a visual-inertial pipeline under the unifying framework of factor graphs. This enables the application of incremental-smoothing algorithms and the use of a \emph{structureless} model for visual measurements, which avoids optimizing over the 3D points, further accelerating the computation. We perform an extensive evaluation of our monocular \VIO pipeline on real and simulated datasets. The results confirm that our modelling effort leads to accurate state estimation in real-time, outperforming state-of-the-art approaches. (arXiv)

## 🧠 Key ideas (atomic)

- The paper preintegrates inertial measurements between selected keyframes into single relative motion constraints to keep visual-inertial optimization tractable in real time (Forster et al., 2016) `ev:reported` p. 2 ^forster2016manifold-001
- The authors state that the accuracy of filtering approaches to visual-inertial odometry is deteriorated by the accumulation of linearization errors (Forster et al., 2016) `ev:asserted` p. 2 ^forster2016manifold-002
- Full smoothing approaches based on nonlinear optimization are described as accurate but computationally demanding for visual-inertial odometry (Forster et al., 2016) `ev:asserted` p. 2 ^forster2016manifold-003
- The authors note it is not clear how to set the estimation window length of fixed-lag smoothing to guarantee a given performance level (Forster et al., 2016) `ev:asserted` p. 2 ^forster2016manifold-004
- The use of preintegrated IMU measurements was first proposed in earlier work, combining many inertial measurements between two keyframes into one relative motion constraint (Forster et al., 2016) `ev:cited` p. 2 ^forster2016manifold-005
- Compared with the original preintegration work, the proposed theory offers a more formal treatment of the rotation noise (Forster et al., 2016) `ev:asserted` p. 2 ^forster2016manifold-006
- The authors state that the proposed preintegration theory avoids singularities in the representation of rotations compared with the original proposal (Forster et al., 2016) `ev:asserted` p. 2 ^forster2016manifold-007
- The paper derives all Jacobians needed for its model in analytic form, reporting them in the appendix (Forster et al., 2016) `ev:reported` p. 2 ^forster2016manifold-008
- The preintegration theory is framed into a factor graph model, enabling incremental smoothing algorithms such as iSAM2 (Forster et al., 2016) `ev:asserted` p. 2 ^forster2016manifold-009
- Inspired by prior work, the authors adopt a structureless model for visual measurements that eliminates all 3D points during incremental smoothing (Forster et al., 2016) `ev:reported` p. 2 ^forster2016manifold-010
- Using the structureless model inside incremental smoothing avoids delaying the processing of visual measurements, unlike its earlier use in filtering (Forster et al., 2016) `ev:asserted` p. 2 ^forster2016manifold-011
- An implementation of the approach performs full smoothing at a rate of 100 Hz, according to the introduction (Forster et al., 2016) `ev:measured` p. 3 ^forster2016manifold-012
- The authors release their preintegrated IMU and structureless vision factors in the GTSAM 4.0 optimization toolbox (Forster et al., 2016) `ev:reported` p. 3 ^forster2016manifold-013
- EKF complexity grows quadratically in the number of estimated landmarks, so typically about 20 landmarks are tracked for real-time operation (Forster et al., 2016) `ev:cited` p. 3 ^forster2016manifold-014
- A structureless filter must delay processing a landmark's measurements until all of them are obtained, which hinders accuracy (Forster et al., 2016) `ev:cited` p. 3 ^forster2016manifold-015
- Linearization at the wrong estimate leaves only three unobservable directions, adding spurious yaw information that renders the filter inconsistent (Forster et al., 2016) `ev:cited` p. 3 ^forster2016manifold-016
- With standard IMU integration between frames, the integration must be repeated between all frames whenever the state estimate changes during optimization (Forster et al., 2016) `ev:cited` p. 4 ^forster2016manifold-017
- The original preintegration work by Lupton and Sukkarieh adopted Euler angles as the global parametrization for rotations (Forster et al., 2016) `ev:cited` p. 4 ^forster2016manifold-018
- The authors state that to their knowledge the analytic Jacobian expressions for the optimization have not been reported previously in the literature (Forster et al., 2016) `ev:asserted` p. 4 ^forster2016manifold-019
- The negative log-likelihood of a rotation can be interpreted as the squared geodesic angle between measurement and rotation weighted by inverse uncertainty (Forster et al., 2016) `ev:computed` p. 5 ^forster2016manifold-020
- Because of the structureless approach, the 3D landmarks are not among the variables estimated in the implementation (Forster et al., 2016) `ev:reported` p. 6 ^forster2016manifold-021
- Under zero-mean Gaussian noise, the MAP estimate reduces to minimizing a sum of squared residual errors weighted by their covariances (Forster et al., 2016) `ev:computed` p. 7 ^forster2016manifold-022
- Up to first order, the preintegrated rotation noise is zero-mean and Gaussian, being a linear combination of zero-mean gyroscope noise terms (Forster et al., 2016) `ev:computed` p. 9 ^forster2016manifold-023
- The preintegrated measurement covariance can be computed iteratively, updating it with each new IMU measurement rather than recomputing it from scratch (Forster et al., 2016) `ev:computed` p. 9 ^forster2016manifold-024
- A change in the bias estimate updates the preintegrated measurements through a first-order expansion, avoiding recomputation of the delta measurements (Forster et al., 2016) `ev:computed` p. 9 ^forster2016manifold-025
- IMU biases are modelled as Brownian motion, that is integrated white noise, adding a bias residual between consecutive keyframes (Forster et al., 2016) `ev:reported` p. 10 ^forster2016manifold-026
- Because landmark elimination is repeated at each Gauss-Newton iteration, the authors state the structureless model still guarantees the optimal MAP estimate (Forster et al., 2016) `ev:asserted` p. 10 ^forster2016manifold-027
- The simulated camera follows a circular trajectory of three meter radius with sinusoidal vertical motion, totalling 120 meters (Forster et al., 2016) `ev:reported` p. 11 ^forster2016manifold-028
- The simulated landmark measurements are corrupted by isotropic Gaussian noise with a standard deviation of 1 pixel to mimic a feature tracker (Forster et al., 2016) `ev:reported` p. 11 ^forster2016manifold-029
- The simulated camera runs at a rate of 2.5 Hz, simulating keyframes, with a focal length of 315 pixels (Forster et al., 2016) `ev:reported` p. 11 ^forster2016manifold-030
- The simulation evaluation uses a Monte Carlo analysis of 50 runs, each with different realizations of process and measurement noise (Forster et al., 2016) `ev:reported` p. 11 ^forster2016manifold-031
- In simulation, the accuracy of iSAM2 is practically the same as the batch nonlinear optimization estimate (Forster et al., 2016) `ev:measured` p. 11 ^forster2016manifold-032
- iSAM2 gives approximately constant update time per frame, approximately 10 milliseconds per update in the simulation experiment (Forster et al., 2016) `ev:measured` p. 11 ^forster2016manifold-033
- Orientation and position errors reported with their 3σ bounds in a single simulation confirm that the approach is consistent, per the authors (Forster et al., 2016) `ev:measured` p. 11 ^forster2016manifold-034
- Uncertainty on the unmeasurable global yaw and position slowly grows over time in the proposed estimator (Forster et al., 2016) `ev:measured` p. 11 ^forster2016manifold-035
- Consistency is tested with a chi-square acceptance test on the average NEES whose acceptance region is 5.0 to 7.0 (Forster et al., 2016) `ev:reported` p. 12 ^forster2016manifold-036
- The average NEES approaches the lower bound but remains below the 7.0 upper bound, indicating the estimator is not overconfident (Forster et al., 2016) `ev:measured` p. 12 ^forster2016manifold-037
- In simulation, the gyroscope and accelerometer biases estimated by the approach correctly track the ground-truth biases (Forster et al., 2016) `ev:measured` p. 12 ^forster2016manifold-038
- Errors from the first-order bias correction are negligible even for relatively large bias perturbations between 0.04 and 0.2 (Forster et al., 2016) `ev:measured` p. 12 ^forster2016manifold-039
- Euler-angle rotation integration error accumulates quickly when the sampling time or angular rate is large, for rates of 1 to 3 rad/s (Forster et al., 2016) `ev:measured` p. 13 ^forster2016manifold-040
- The Euler-angle negative log-likelihood changes when the reference frame is rotated, so an Euler estimator may depend on the world frame choice (Forster et al., 2016) `ev:measured` p. 13 ^forster2016manifold-041
- Experiments confirm the SO(3) parametrization is fair, with a negative log-likelihood invariant to rotations of the reference frame (Forster et al., 2016) `ev:measured` p. 13 ^forster2016manifold-042
- Using KL divergence against sampled ground-truth covariance, Euler-angle noise propagation worsens the closer trajectories get to the gimbal-lock singularity (Forster et al., 2016) `ev:measured` p. 13 ^forster2016manifold-043
- The proposed on-manifold approach accurately estimates the preintegrated measurement covariance independently of the motion of the platform (Forster et al., 2016) `ev:measured` p. 13 ^forster2016manifold-044
- The real-world pipeline combines an SVO-based high frame rate tracking front-end with an iSAM2-based optimization back-end (Forster et al., 2016) `ev:reported` p. 13 ^forster2016manifold-045
- Because the approach does not marginalize out past states, the authors state it could be readily extended to incorporate loop closures (Forster et al., 2016) `ev:asserted` p. 14 ^forster2016manifold-046
- The indoor dataset was recorded with a VI-Sensor containing an ADIS16448 MEMS IMU at 800Hz with a camera at 20Hz (Forster et al., 2016) `ev:reported` p. 14 ^forster2016manifold-047
- Indoors, the proposed approach achieves 0.3m average drift over 360m traveled, while OKVIS and MSCKF accumulate 0.7m average error (Forster et al., 2016) `ev:measured` p. 15 ^forster2016manifold-048
- The proposed approach shows significantly less drift in yaw direction than OKVIS and MSCKF in the indoor experiment (Forster et al., 2016) `ev:measured` p. 15 ^forster2016manifold-049
- Pitch and roll error is constant for all compared methods, which the authors attribute to observability of the gravity direction (Forster et al., 2016) `ev:measured` p. 15 ^forster2016manifold-050
- In a single real indoor run, estimation errors remain within the 3-sigma bounds of the estimated uncertainty (Forster et al., 2016) `ev:measured` p. 15 ^forster2016manifold-051
- The iSAM2 back-end, running 10 optimization iterations on an Intel i7 2.4 GHz laptop, averages a 10ms update time (Forster et al., 2016) `ev:measured` p. 15 ^forster2016manifold-052
- The SVO front-end requires approximately 3ms to process a frame on the laptop used in the experiments (Forster et al., 2016) `ev:measured` p. 15 ^forster2016manifold-053
- OKVIS must repeat IMU integration at every change of the linearization point, which preintegrated IMU measurements avoid (Forster et al., 2016) `ev:asserted` p. 15 ^forster2016manifold-054
- On the outdoor loop around an office building, the end-to-end error is 1.5m for the proposed approach versus 2.2m for Google Tango (Forster et al., 2016) `ev:measured` p. 16 ^forster2016manifold-055
- On a trajectory across three floors of an office building, the approach has 0.5m end-to-end error while Tango accumulates 1.4m (Forster et al., 2016) `ev:measured` p. 16 ^forster2016manifold-056
- Tango and the proposed system use different sensors, so the end-to-end errors allow only a qualitative comparison (Forster et al., 2016) `ev:asserted` p. 16 ^forster2016manifold-057
- The authors conclude their proposal improves over works integrating in a global frame because it does not commit to a linearization point during integration (Forster et al., 2016) `ev:asserted` p. 16 ^forster2016manifold-058
- The authors conclude that experiments confirm their approach is more accurate than state-of-the-art filtering and optimization-based alternatives (Forster et al., 2016) `ev:asserted` p. 16 ^forster2016manifold-059

## 🎯 Contributions

## 📖 Glossary

- **IMU preintegration** — Summarizing many inertial measurements between two keyframes into one relative motion constraint.
- **SO(3)** — The Special Orthogonal Group of 3D rotation matrices, a smooth manifold.
- **Retraction** — Map from a tangent-space increment to a neighborhood of a point on the manifold.
- **Lift-solve-retract** — Gauss-Newton on manifolds: linearize in the tangent space, solve, then retract.
- **Structureless vision factor** — Visual constraint among poses where landmarks are linearly eliminated, not estimated.
- **iSAM2** — Incremental smoothing algorithm on the Bayes tree that updates only affected variables.
- **NEES** — Normalized Estimation Error Squared, the error normalized by estimator covariance, measuring consistency.
- **Factor graph** — Bipartite graph of unknowns and probability factors representing a factored posterior.
- **Fixed-lag smoother** — Estimator optimizing a window of recent states while marginalizing older ones.

## ❓ Open questions

- How does the approach perform with slower IMU rates, where the authors suggest higher-order integration may be needed?
- How does the structureless visual model behave when loop closures are added over long trajectories?
- Can consistency be evaluated on real data with multi-run NEES rather than single-run 3-sigma bounds?
- How much of the real-world accuracy gain comes from preintegration versus the SVO front-end, given different front-ends across methods?
- Should the IMU-camera time delay be estimated online as a state instead of calibrated offline?

## 📝 Notes on reading

Read the arXiv v3 preprint (1512.02363v3, 30 Oct 2016), which states it was accepted in IEEE Transactions on Robotics (DOI 10.1109/TRO.2016.2597321); page 1 is a cover sheet, so the printed page numbers are offset by one from the paper body.

Inconsistency: the Fig. 18 caption (p. 15) gives an end-to-end error of 1.0m for the outdoor loop, while the text on p. 16 gives 1.5m; the claim uses the text value.

Equations throughout (Sections III-VII and the Appendix) are garbled by extraction and were described rather than claimed. Figures 6-13 and 15-17 are plots whose curves could only be described: Fig. 7 compares RMSE of batch and iSAM2 over 50 Monte Carlo runs; Fig. 15 shows relative translation, yaw and pitch/roll errors against OKVIS and MSCKF over segments of 10 to 360m; Fig. 16 shows per-keyframe processing time with an initial peak when the camera was static.

The simulation IMU noise parameters (footnote 2, p. 11) and the appendix Jacobians (pp. 16-18) were not claimed individually.

## Suggested new concepts

- IMU preintegration — central technique reused across optimization-based visual-inertial estimators.
- Structureless vision factors — landmark elimination pattern shared by MSC-KF and smart factors in factor graphs.
- Incremental smoothing (iSAM2) — the solver enabling real-time full smoothing in this and related work.
- Estimator consistency (NEES) — standard test for overconfidence in state estimation, relevant to any VIO evaluation.
- Optimization on manifolds — lift-solve-retract framework underlying rotation estimation in SLAM and VIO.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Ejemplo canónico de cálculo con $J_r$ en SO(3) y ruido en el álgebra.
- **[[03_aplicaciones_vision_por_computador]]** — Preintegración IMU en $SO(3)$
