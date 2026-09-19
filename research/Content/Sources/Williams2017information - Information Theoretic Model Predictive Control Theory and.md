---
aliases: []
type: "source"
title: "Information Theoretic Model Predictive Control: Theory and Applications to Autonomous Driving"
citekey: "Williams2017information"
doi: "10.48550/arXiv.1707.02342"
arxiv: "1707.02342"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1707.02342"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Grady Williams", "Paul Drews", "Brian Goldfain", "James M. Rehg", "Evangelos A. Theodorou"]
sha256: ["c11163a2c07fccc4bdb7eebe92bfcc31fcfe7f366433262bc2cc320328476363"]
pdf: "Content/Papers/Williams2017information.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Williams2017information.pdf]]

> [!abstract] One-sentence summary
> The paper derives a GPU-parallel sampling-based model predictive controller (IT-MPC) from free energy and KL-divergence arguments and shows on over 100 km of real 1:5 scale dirt-track driving that it succeeds more often than a cross-entropy MPC baseline.

## Abstract

We present an information theoretic approach to stochastic optimal control problems that can be used to derive general sampling based optimization schemes. This new mathematical method is used to develop a sampling based model predictive control algorithm. We apply this information theoretic model predictive control (IT-MPC) scheme to the task of aggressive autonomous driving around a dirt test track, and compare its performance to a model predictive control version of the cross-entropy method. (arXiv)

## 🧠 Key ideas (atomic)

- The authors develop a control framework based on an information theoretic interpretation of optimal control to create sampling based optimization methods. (Williams et al., 2017) `ev:asserted` p. 2 ^williams2017information-001
- The authors state that splitting control into path planning and path tracking introduces inherent limitations for driving in aggressive regimes. (Williams et al., 2017) `ev:asserted` p. 1 ^williams2017information-002
- Path planners typically use only kinematic constraints, so a planned aggressive path may not be dynamically feasible for the vehicle. (Williams et al., 2017) `ev:cited` p. 1 ^williams2017information-003
- The GPU-parallel sampling algorithm is designed to operate in a receding horizon manner within a fast control loop of 40 Hz. (Williams et al., 2017) `ev:reported` p. 2 ^williams2017information-004
- The authors state that because the method is derivative-free it can handle discontinuous cost functions that keep the vehicle on track. (Williams et al., 2017) `ev:asserted` p. 2 ^williams2017information-005
- The derivation shows that the negative free energy provides a lower bound on the standard stochastic optimal control objective. (Williams et al., 2017) `ev:computed` p. 4 ^williams2017information-006
- The optimal control distribution is constructed by augmenting the base measure with the exponentiated negative cost of the state trajectory. (Williams et al., 2017) `ev:computed` p. 4 ^williams2017information-007
- According to the derivation, control inputs drawn from the optimal distribution achieve a lower expected cost than any other control distribution. (Williams et al., 2017) `ev:computed` p. 4 ^williams2017information-008
- Minimizing the KL divergence from the optimal distribution to the controlled distribution reduces to a quadratic minimization over the control sequence. (Williams et al., 2017) `ev:computed` p. 5 ^williams2017information-009
- In the unconstrained case, the optimal open-loop control at each timestep equals the expected control under the optimal distribution. (Williams et al., 2017) `ev:computed` p. 5 ^williams2017information-010
- The authors prefer this convex formulation over the reverse KL divergence because gradient step sizes are difficult to tune in real-time control. (Williams et al., 2017) `ev:asserted` p. 5 ^williams2017information-011
- Importance sampling lets expectations under the optimal distribution be estimated from trajectories sampled around the current control estimate. (Williams et al., 2017) `ev:computed` p. 5 ^williams2017information-012
- The resulting control law is globally optimal in an information theoretic sense under the condition that the expectation can be perfectly evaluated. (Williams et al., 2017) `ev:computed` p. 6 ^williams2017information-013
- The authors note that Monte-Carlo estimation can create the appearance of local optimums due to insufficient sampling of the state space. (Williams et al., 2017) `ev:asserted` p. 6 ^williams2017information-014
- Trajectory costs are shifted so the best sampled trajectory has cost zero, which improves numerical conditioning without changing optimality. (Williams et al., 2017) `ev:computed` p. 6 ^williams2017information-015
- Low values of the inverse temperature λ cause many sampled trajectories to be rejected by the importance sampling weights. (Williams et al., 2017) `ev:computed` p. 6 ^williams2017information-016
- A base distribution built from the current plan scaled by α yields a separate control cost parameter γ equal to λ(1−α). (Williams et al., 2017) `ev:computed` p. 7 ^williams2017information-017
- Control constraints are handled by a clamping function inside the dynamics, which turns the optimization into an unconstrained problem. (Williams et al., 2017) `ev:reported` p. 7 ^williams2017information-018
- Chattering from the stochastic sampling is removed by passing the averaged control sequence through a Savitsky-Galoy convolutional filter. (Williams et al., 2017) `ev:reported` p. 7 ^williams2017information-019
- In the GPU implementation, each trajectory sample uses between 4 and 16 CUDA threads depending on the dynamics model. (Williams et al., 2017) `ev:reported` p. 7 ^williams2017information-020
- Depending on model and cost, the implementation can achieve control loops from 40-60 HZ using a few thousand samples of 2-3 second trajectories. (Williams et al., 2017) `ev:reported` p. 7 ^williams2017information-021
- Sampling 1200 trajectories of 2.5 seconds at 40 Hz corresponds to approximately 4.8 million dynamics queries every second. (Williams et al., 2017) `ev:computed` p. 7 ^williams2017information-022
- A small fraction of samples, less than one percent, are Gaussian perturbations around zero so the controller can recover from strong disturbances. (Williams et al., 2017) `ev:reported` p. 8 ^williams2017information-023
- The path integral and information theoretic optimal controls coincide when noise enters through the control input and R equals λΣ⁻¹. (Williams et al., 2017) `ev:computed` p. 9 ^williams2017information-024
- Minimizing the KL divergence yields an entire open-loop control plan, whereas the path integral equations give only a current time-step update. (Williams et al., 2017) `ev:asserted` p. 9 ^williams2017information-025
- [[Model Predictive Path Integral control|The path integral derivation]] requires control-affine dynamics, whereas the information theoretic setting allows dynamics given by an arbitrary non-linear function. (Williams et al., 2017) `ev:asserted` p. 9 ^williams2017information-026
- The authors note that ground vehicle dynamics and neural network models fall outside the control-affine class required by path integral control. (Williams et al., 2017) `ev:asserted` p. 9 ^williams2017information-027
- When optimizing a Gaussian mean, cross-entropy differs from the information theoretic approach by taking an un-weighted average over the top samples. (Williams et al., 2017) `ev:asserted` p. 10 ^williams2017information-028
- The authors argue that weighting all samples gives the information theoretic approach more discriminative power to reject costly trajectories than cross-entropy. (Williams et al., 2017) `ev:asserted` p. 10 ^williams2017information-029
- The cross-entropy MPC baseline keeps its sampling covariance constant because the simple covariance-growing methods tried did not prove satisfactory. (Williams et al., 2017) `ev:reported` p. 11 ^williams2017information-030
- The AutoRally testbed is an electric vehicle one fifth the size of a full scale car, weighing approximately 22 kg. (Williams et al., 2017) `ev:reported` p. 11 ^williams2017information-031
- The AutoRally onboard computer includes an Intel quad-core i7 processor with an Nvidia GTX-750ti graphics card for computation. (Williams et al., 2017) `ev:reported` p. 11 ^williams2017information-032
- The state estimation factor graph is optimized with GTSAM and iSAM2 for state nodes at 10Hz, matching the GPS measurements. (Williams et al., 2017) `ev:reported` p. 12 ^williams2017information-033
- A 200 Hz state estimate is generated by integrating IMU measurements to interpolate between the 10Hz GPS positions. (Williams et al., 2017) `ev:reported` p. 12 ^williams2017information-034
- Both dynamics models describe the vehicle with seven state variables, and the controls are the steering and throttle inputs. (Williams et al., 2017) `ev:reported` p. 12 ^williams2017information-035
- The system identification dataset holds 30 minutes of choreographed maneuvers driven by a human pilot in both track directions. (Williams et al., 2017) `ev:reported` p. 12 ^williams2017information-036
- The basis function model uses 21 functions extracted from a non-linear bicycle model plus 4 added by trial and error. (Williams et al., 2017) `ev:reported` p. 12 ^williams2017information-037
- Standard linear regression without Tikhonov regularization produced very large weights that made the multi-step forward simulation unstable. (Williams et al., 2017) `ev:measured` p. 12 ^williams2017information-038
- The neural network dynamics model has two fully connected hidden layers of 32 neurons, for a total of 1412 parameters. (Williams et al., 2017) `ev:reported` p. 13 ^williams2017information-039
- On the validation set, the neural network reached an R2 score of .78 compared with .68 for the basis function model. (Williams et al., 2017) `ev:measured` p. 13 ^williams2017information-040
- On the validation set, the neural network reached a mean squared error of 1.39 compared with 2.07 for the basis function model. (Williams et al., 2017) `ev:measured` p. 13 ^williams2017information-041
- The authors attribute significant inaccuracies in both dynamics models to hidden variables such as track condition and battery voltage. (Williams et al., 2017) `ev:asserted` p. 13 ^williams2017information-042
- Both controllers shared a 40 Hz control frequency, a 2 seconds time horizon, λ of 12.5, and γ of 0.1. (Williams et al., 2017) `ev:reported` p. 13 ^williams2017information-043
- The track cost includes a time-decaying impulse penalty of 10000 for vehicle positions located outside the track boundaries. (Williams et al., 2017) `ev:reported` p. 13 ^williams2017information-044
- The authors report that a track penalty without time decay is effective in simulation with perfect dynamics but fails on the real system. (Williams et al., 2017) `ev:reported` p. 13 ^williams2017information-045
- The stabilizing cost rejects any sampled trajectory whose side slip angle exceeds 0.75 radians, approximately 42 degrees. (Williams et al., 2017) `ev:reported` p. 13 ^williams2017information-046
- Each controller was tested with each dynamics model at speed targets of 6 m/s, 8.5 m/s, and 11 m/s. (Williams et al., 2017) `ev:reported` p. 14 ^williams2017information-047
- The authors collected 100 laps for 17 of the 24 test scenarios, totalling over 1700 laps and over 100 kilometers of driving. (Williams et al., 2017) `ev:measured` p. 14 ^williams2017information-048
- The other 7 settings produced controllers that were too reckless or unstable to complete the trials in their entirety. (Williams et al., 2017) `ev:measured` p. 14 ^williams2017information-049
- At the 6 m/s target, IT-MPC with either dynamics model drove at speeds from just over 1 m/s to 5.77 m/s. (Williams et al., 2017) `ev:measured` p. 14 ^williams2017information-050
- At the 6 m/s target, IT-MPC reached a 100% success rate for every combination of dynamics model and driving direction. (Williams et al., 2017) `ev:measured` p. 14 ^williams2017information-051
- At the 6 m/s target, the cross-entropy controller with the neural network achieved significantly faster speeds than the IT-MPC algorithm. (Williams et al., 2017) `ev:measured` p. 16 ^williams2017information-052
- At the 6 m/s target, the cross-entropy method with the basis function model achieved only an 83.16% success rate in one direction. (Williams et al., 2017) `ev:measured` p. 16 ^williams2017information-053
- At the 8.5 m/s target, IT-MPC with the neural network was the only method performing flawlessly both clockwise and counter-clockwise. (Williams et al., 2017) `ev:measured` p. 16 ^williams2017information-054
- At the 8.5 m/s target, IT-MPC reached maximum speeds about 1 m/s slower than the target velocity, remaining more cautious than cross-entropy. (Williams et al., 2017) `ev:measured` p. 16 ^williams2017information-055
- With the basis function model at 8.5 m/s, cross-entropy collided with a track barrier on over 50% of the trials. (Williams et al., 2017) `ev:measured` p. 16 ^williams2017information-056
- At the 11 m/s target, only counter-clockwise IT-MPC completed all 100 laps without a significant violation of the track boundaries. (Williams et al., 2017) `ev:measured` p. 16 ^williams2017information-057
- The top speed achieved by IT-MPC at the 11 m/s target was 9.06 m/s, approximately 20 miles per hour. (Williams et al., 2017) `ev:measured` p. 16 ^williams2017information-058
- At the 11 m/s target, the cross-entropy method completed laps with a low success rate of only 66.32%. (Williams et al., 2017) `ev:measured` p. 16 ^williams2017information-059
- With the neural network model, the IT-MPC controller decreases speed by performing a small slide into turns, often lifting the left front wheel. (Williams et al., 2017) `ev:measured` p. 17 ^williams2017information-060
- The controller commonly counter-steers when exiting turns, a behavior that exploits the non-linear vehicle dynamics and works only at high speeds. (Williams et al., 2017) `ev:measured` p. 17 ^williams2017information-061
- Driving clockwise at 11 m/s, the neural network model incorrectly predicted over-steer when the vehicle in fact under-steered. (Williams et al., 2017) `ev:measured` p. 17 ^williams2017information-062
- The authors suggest this clockwise modeling error is likely due to asymmetry in how the human pilot drove the training data. (Williams et al., 2017) `ev:asserted` p. 17 ^williams2017information-063
- Despite the large clockwise model error, the vehicle still completed the task close to 80% of the time at the 11 m/s target. (Williams et al., 2017) `ev:measured` p. 17 ^williams2017information-064
- Despite dry, damaged track conditions during the 8.5 m/s runs, the neural network model with IT-MPC completed all 100 laps. (Williams et al., 2017) `ev:measured` p. 17 ^williams2017information-065
- All IT-MPC failures with the neural network came from clockwise driving at 11 m/s, where systematic modeling error caused under-steer. (Williams et al., 2017) `ev:measured` p. 18 ^williams2017information-066
- The authors attribute cross-entropy boundary violations to its sampling method, which admits trajectories even when they violate the track constraint. (Williams et al., 2017) `ev:asserted` p. 18 ^williams2017information-067
- The authors conclude that the costs and dynamics of autonomous driving are well suited for a sampling based control scheme. (Williams et al., 2017) `ev:asserted` p. 18 ^williams2017information-068
- The authors argue that large impulse cost terms discourage boundary contact while still treating track collisions as a soft constraint. (Williams et al., 2017) `ev:asserted` p. 18 ^williams2017information-069

## 🎯 Contributions

## 📖 Glossary

- **IT-MPC** — Information theoretic model predictive control: sampling-based MPC weighting trajectories by exponentiated negative cost.
- **Free energy** — Log expectation of exponentiated negative scaled trajectory cost under a base distribution.
- **Inverse temperature (λ)** — Parameter setting how sharply the optimal distribution concentrates on low-cost trajectories.
- **KL divergence** — Asymmetric measure of difference between two probability distributions.
- **Importance sampling** — Estimating expectations under one distribution using weighted samples from another.
- **Cross-entropy method (CEM)** — Stochastic optimization refitting a sampling distribution to an elite set of samples.
- **Path integral control** — Stochastic optimal control solving a linearized HJB equation through expectations over trajectories.
- **Savitsky-Galoy filter** — Convolutional filter implementing local polynomial smoothing of a sequence.
- **Side slip angle** — Angle between the vehicle velocity vector and its heading.
- **AutoRally** — Electric 1/5 scale autonomous vehicle testbed used for the experiments.

## ❓ Open questions

- How would IT-MPC perform against gradient-based MPC methods on the same aggressive driving task?
- Can the sampling covariance be adapted online so that it can both shrink and grow in a receding horizon setting?
- Would training dynamics models on multi-step prediction error reduce the clockwise under-steer failures?
- How does IT-MPC behave on highly unstable systems, where the authors note useful trajectories are difficult to sample?
- How sensitive are the results to λ, γ and the number of samples, which were tuned in simulation and a few real runs?

## 📝 Notes on reading

Read the arXiv v1 manuscript (arXiv:1707.02342v1, 7 Jul 2017), which matches the packet identifier.

Table III and the text disagree on direction: the text says CEM-BF at 6 m/s achieved 83.16% (79/95 laps) going clockwise, but Table III lists 83.16% under CC and 97.30% under C; the claim avoids naming the direction. The text reports the clockwise 11 m/s IT-MPC-NN run as close to 80% success, while Table III lists 76.00%. The text on p. 16 says the cross-entropy method must accept the top 20% of trajectories, consistent with the > 0.8 percentile eliteness threshold in Table II.

The symbol α is used both for the base-distribution mixing parameter (p. 6–7) and, in Alg. 1 and on p. 8, for the fraction of zero-mean samples; the text on p. 8 also says the warm start is in Alg. 2 while it is in Alg. 1 (p. 9 repeats this). The CEM-MPC section says it uses the sampling-based MPC method from Alg. 2, which appears to mean Alg. 1.

Many equations (pp. 3–9) are garbled by extraction; derivation claims were written from the surrounding prose. Table IV (p. 15) holds only trajectory trace images; Figs. 7–12 were only described, not claimed: they show IT-MPC trajectory traces at the three targets, a cornering time-lapse with the front left wheel lifted, predicted vs actual trajectories at 11 m/s, disturbance rejection over a hole, and clockwise 11 m/s failure trajectories.

## Suggested new concepts

- Model predictive path integral control (MPPI) — the sampling-based MPC family this paper generalizes and relates to path integral theory.
- Free energy–relative entropy duality — the theoretical bound from which the IT-MPC update law is derived.
- Cross-entropy method for MPC — the main baseline, and a widely used sampling-based planner in robotics.
- Learned vehicle dynamics models — neural network vs basis function dynamics used inside sampling-based controllers.
- AutoRally platform — a reusable 1/5 scale testbed for aggressive autonomous driving research.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H3.** Derivación fundacional de MPPI por energía libre y KL, base de todo el MPC por muestreo aplicable al brazo.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
