---
aliases: []
type: "source"
title: "Symmetry Teleportation for Accelerated Optimization"
citekey: "Zhao2022symmetry"
doi: "10.48550/arXiv.2205.10637"
arxiv: "2205.10637"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2205.10637"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Bo Zhao", "Nima Dehmamy", "Robin Walters", "Rose Yu"]
sha256: ["dcfddea840928c72c2197b79691b54bc1c82375ae32441217912517b56abc7b8"]
pdf: "Content/Papers/Zhao2022symmetry.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Zhao2022symmetry.pdf]]

> [!abstract] One-sentence summary
> The paper proposes symmetry teleportation, which moves parameters along loss level sets via loss-invariant group actions to larger gradients, and shows faster convergence of gradient descent and AdaGrad on test functions, small regressions and MNIST, at some cost in generalization.

## Abstract

Existing gradient-based optimization methods update parameters locally, in a direction that minimizes the loss function. We study a different approach, symmetry teleportation, that allows parameters to travel a large distance on the loss level set, in order to improve the convergence speed in subsequent steps. Teleportation exploits symmetries in the loss landscape of optimization problems. We derive loss-invariant group actions for test functions in optimization and multi-layer neural networks, and prove a necessary condition for teleportation to improve convergence rate. We also show that our algorithm is closely related to second order methods. Experimentally, we show that teleportation improves the convergence speed of gradient descent and AdaGrad for several optimization problems including test functions, multi-layer regressions, and MNIST classification. (arXiv)

## 🧠 Key ideas (atomic)

- Gradient descent is described as a first-order method that is easy to compute but suffers from slow convergence. (Zhao et al., 2022) `ev:asserted` p. 1 ^zhao2022symmetry-001
- Second-order methods such as Newton's method converge faster, but computing the Hessian can be expensive over high dimensional spaces. (Zhao et al., 2022) `ev:cited` p. 1 ^zhao2022symmetry-002
- The authors propose symmetry teleportation, which moves parameters to a point with steeper gradients using a loss-invariant symmetry transformation. (Zhao et al., 2022) `ev:asserted` p. 2 ^zhao2022symmetry-003
- After teleportation the loss stays the same, but the gradient and hence the rate of loss decay change. (Zhao et al., 2022) `ev:asserted` p. 2 ^zhao2022symmetry-004
- Teleportation relaxes the proximal term of gradient descent by allowing parameters on the same level set to be far away in Euclidean distance. (Zhao et al., 2022) `ev:asserted` p. 2 ^zhao2022symmetry-005
- Unlike Bamler and Mandt, who seek the group element minimizing the loss, this method searches symmetry orbits for points maximizing gradient norm. (Zhao et al., 2022) `ev:cited` p. 2 ^zhao2022symmetry-006
- If the group acts transitively on the level set, teleporting to the maximum-gradient point gives the same update direction as Newton's method. (Zhao et al., 2022) `ev:asserted` p. 2 ^zhao2022symmetry-007
- Earlier neural teleportation work based on quiver representation theory showed that random teleportation speeds up gradient descent experimentally and theoretically. (Zhao et al., 2022) `ev:cited` p. 3 ^zhao2022symmetry-008
- The authors do not guarantee faster convergence throughout the entire training, but claim acceleration at least for a short time after initialization. (Zhao et al., 2022) `ev:asserted` p. 3 ^zhao2022symmetry-009
- Algorithm 1 transforms parameters at epochs in a teleportation schedule to the group element maximizing gradient norm, then continues gradient descent. (Zhao et al., 2022) `ev:reported` p. 3 ^zhao2022symmetry-010
- For continuous group actions, teleportation can be implemented by parameterizing the group element and performing gradient ascent on it. (Zhao et al., 2022) `ev:asserted` p. 3 ^zhao2022symmetry-011
- For discrete groups, search algorithms or random sampling can be used to find a group element that improves gradient magnitude. (Zhao et al., 2022) `ev:asserted` p. 3 ^zhao2022symmetry-012
- The teleportation schedule is a hyperparameter defined as a set, allowing non-fixed frequencies or teleporting only at earlier epochs. (Zhao et al., 2022) `ev:reported` p. 4 ^zhao2022symmetry-013
- The Rosenbrock and Booth test functions are shown to have rotational SO(2) symmetry through explicit action maps on the plane. (Zhao et al., 2022) `ev:computed` p. 4 ^zhao2022symmetry-014
- A linear network is invariant under general linear groups acting on adjacent weight matrices through right multiplication by the inverse and left multiplication. (Zhao et al., 2022) `ev:computed` p. 4 ^zhao2022symmetry-015
- The derivation assumes bijective activations such as Leaky-ReLU, extending Sigmoid or Tanh analytically to bijective functions. (Zhao et al., 2022) `ev:reported` p. 4 ^zhao2022symmetry-016
- Assuming invertible lower-layer outputs, a multi-layer network with bijective activation has a general linear symmetry that keeps upper layer outputs invariant. (Zhao et al., 2022) `ev:computed` p. 5 ^zhao2022symmetry-017
- The derived group action for nonlinear networks depends on the network input as well as the current weights of all lower layers. (Zhao et al., 2022) `ev:asserted` p. 5 ^zhao2022symmetry-018
- Teleportation accelerates loss decay if the inverse transposed Jacobian applied to the gradient has a larger learning-rate weighted norm than before. (Zhao et al., 2022) `ev:computed` p. 5 ^zhao2022symmetry-019
- If the symmetry is a subgroup of the orthogonal group preserving the inverse learning rate, teleportation leaves the loss decay rate unchanged. (Zhao et al., 2022) `ev:computed` p. 5 ^zhao2022symmetry-020
- Under Lipschitz continuity of the gradient norm and ηL < 1, a large enough initial gradient improvement guarantees larger gradients after T more steps. (Zhao et al., 2022) `ev:computed` p. 6 ^zhao2022symmetry-021
- This sufficient condition is met when the Lipschitz constant is small, the learning rate is small, or the initial improvement is large. (Zhao et al., 2022) `ev:computed` p. 6 ^zhao2022symmetry-022
- For positive definite quadratic losses, a single teleportation to maximal gradient norm keeps every later gradient flow point maximal within its level set. (Zhao et al., 2022) `ev:computed` p. 6 ^zhao2022symmetry-023
- For these convex quadratic losses, maximizing the gradient magnitude within a level set minimizes the distance to the global minimum. (Zhao et al., 2022) `ev:computed` p. 6 ^zhao2022symmetry-024
- At a point where gradient norm is locally maximal on a level set, the gradient has the same direction as Newton's direction. (Zhao et al., 2022) `ev:computed` p. 7 ^zhao2022symmetry-025
- Teleportation over continuous groups does not require the full Hessian, differentiating with respect to parameters and then with respect to the group element. (Zhao et al., 2022) `ev:asserted` p. 7 ^zhao2022symmetry-026
- The authors state that non-transitive actions, non-optimal group elements and infrequent teleportation make the Newton connection an intuition rather than exact formulation. (Zhao et al., 2022) `ev:asserted` p. 7 ^zhao2022symmetry-027
- On the Rosenbrock function, parameters start at (−1, −1) and run 1000 steps with teleportation every 100 steps. (Zhao et al., 2022) `ev:reported` p. 7 ^zhao2022symmetry-028
- For Rosenbrock, group elements are found by 10 steps of gradient ascent on the SO(2) rotation angle. (Zhao et al., 2022) `ev:reported` p. 7 ^zhao2022symmetry-029
- Gradient descent does not reach the Rosenbrock target in 1000 steps, whereas teleportation allows large steps and reaches it much earlier. (Zhao et al., 2022) `ev:measured` p. 7 ^zhao2022symmetry-030
- On the Booth function, parameters start at (5, −5), run 10 steps with learning rate 0.08, and teleport once before epoch 5. (Zhao et al., 2022) `ev:reported` p. 8 ^zhao2022symmetry-031
- On the Booth function, teleportation moves the parameters to a trajectory with a larger convergence rate than plain gradient descent. (Zhao et al., 2022) `ev:measured` p. 8 ^zhao2022symmetry-032
- General linear teleportation uses a first-order approximation of the exponential map, replacing the group element by identity plus a matrix optimized by ascent. (Zhao et al., 2022) `ev:reported` p. 8 ^zhao2022symmetry-033
- In multilayer regression, adding teleportation clearly improves both gradient descent and AdaGrad over epochs and wall-clock time across 5 runs. (Zhao et al., 2022) `ev:measured` p. 8 ^zhao2022symmetry-034
- The authors note that GD and AdaGrad use different learning rates in the regression experiment, so they are not directly comparable. (Zhao et al., 2022) `ev:asserted` p. 8 ^zhao2022symmetry-035
- In the regression experiment, the teleported trajectory has a larger dL/dt value than the plain trajectory at the same loss values. (Zhao et al., 2022) `ev:measured` p. 8 ^zhao2022symmetry-036
- The MNIST training set is split into 48,000 examples for training and 12,000 examples for validation. (Zhao et al., 2022) `ev:reported` p. 8 ^zhao2022symmetry-037
- The MNIST model is a three-layer network with hidden dimension [512, 512], LeakyReLU activations and cross-entropy loss. (Zhao et al., 2022) `ev:reported` p. 8 ^zhao2022symmetry-038
- MNIST training runs 80 epochs with batch size of 20, teleporting after the first epoch on 4 different mini-batches. (Zhao et al., 2022) `ev:reported` p. 8 ^zhao2022symmetry-039
- On MNIST, teleportation significantly accelerates the decrease of the training loss in SGD compared with SGD alone. (Zhao et al., 2022) `ev:measured` p. 8 ^zhao2022symmetry-040
- On MNIST, the effect of teleportation on validation loss is limited, and it is detrimental for AdaGrad. (Zhao et al., 2022) `ev:measured` p. 8 ^zhao2022symmetry-041
- Teleportation on MNIST makes training faster at the beginning but leads to earlier overfit and slightly worse validation accuracy. (Zhao et al., 2022) `ev:measured` p. 8 ^zhao2022symmetry-042
- The authors suggest a possible reason: regions with large gradients have sharp minima that do not generalize well. (Zhao et al., 2022) `ev:asserted` p. 8 ^zhao2022symmetry-043
- In the MNIST schedule study, teleportation before training has the worst performance among the single teleportation epochs tested. (Zhao et al., 2022) `ev:measured` p. 9 ^zhao2022symmetry-044
- After epoch 0, a single teleportation on MNIST has a stronger effect when it is applied earlier in training. (Zhao et al., 2022) `ev:measured` p. 9 ^zhao2022symmetry-045
- With the same number of teleportations, schedules with smaller intervals between teleportations accelerate MNIST convergence more significantly. (Zhao et al., 2022) `ev:measured` p. 9 ^zhao2022symmetry-046
- Using more mini-batches to teleport on MNIST leads to a faster decrease in training loss but is more prone to overfitting. (Zhao et al., 2022) `ev:measured` p. 9 ^zhao2022symmetry-047
- One gradient ascent step on the group element has the same complexity order as a forward and backward pass of gradient descent. (Zhao et al., 2022) `ev:computed` p. 9 ^zhao2022symmetry-048
- Teleportation runtime scaled polynomially with matrix dimensions and linearly with the number of layers on a Leaky-ReLU network. (Zhao et al., 2022) `ev:measured` p. 9 ^zhao2022symmetry-049
- Although a teleportation step has the same complexity as a gradient step, runtime is dominated by teleportation due to larger constants. (Zhao et al., 2022) `ev:measured` p. 10 ^zhao2022symmetry-050
- In their experiments, the authors report convergence gains from a small number of teleportation steps without significant computational overhead. (Zhao et al., 2022) `ev:asserted` p. 10 ^zhao2022symmetry-051
- For matrix factorization, the authors argue teleportation is guaranteed to produce a better trajectory, linking larger imbalance to faster overall convergence. (Zhao et al., 2022) `ev:asserted` p. 10 ^zhao2022symmetry-052
- Algorithm 2 extends teleportation to stochastic gradient descent by applying group actions on each of the first B mini-batches. (Zhao et al., 2022) `ev:reported` p. 13 ^zhao2022symmetry-053
- For the Rosenbrock function with 2N parameters, a pairwise change of variables gives an SO(2N) symmetry, not used in experiments. (Zhao et al., 2022) `ev:computed` p. 14 ^zhao2022symmetry-054
- On both test functions, the trajectory with teleportation has a larger dL/dt than without teleportation at the same loss values. (Zhao et al., 2022) `ev:measured` p. 19 ^zhao2022symmetry-055
- In regression, GD uses learning rate 10−4 and AdaGrad uses 10−1, each run 300 steps with teleportation once at epoch 5. (Zhao et al., 2022) `ev:reported` p. 20 ^zhao2022symmetry-056
- Convergence in the speedup sweep is declared when the loss difference between consecutive steps is less than 10−3, run on one CPU. (Zhao et al., 2022) `ev:reported` p. 20 ^zhao2022symmetry-057
- When the regression converged, most combinations of teleportation learning rate and step count improved wall-clock convergence speed, giving speedup > 1. (Zhao et al., 2022) `ev:measured` p. 20 ^zhao2022symmetry-058
- More ascent steps per teleportation find a better point in parameter space but increase the cost of one teleportation. (Zhao et al., 2022) `ev:asserted` p. 20 ^zhao2022symmetry-059
- A larger learning rate for optimizing the group element improves gradient norm but is more likely to lead to divergence. (Zhao et al., 2022) `ev:asserted` p. 20 ^zhao2022symmetry-060

## 🎯 Contributions

## 📖 Glossary

- **Symmetry teleportation** — Moving parameters along a loss level set with a loss-invariant group action.
- **Parameter space symmetry** — Group action on parameters that leaves the loss unchanged.
- **Level set** — Set of parameter values sharing the same loss value.
- **Teleportation schedule** — Set of epochs at which teleportation is applied.
- **Group orbit** — All points reachable from one point by applying group elements.
- **Transitive action** — Group action that can reach every point of a set from any other.
- **Proximal term** — Penalty keeping a new iterate close to the current one.
- **Newton's direction** — Inverse Hessian applied to the gradient.

## ❓ Open questions

- What is the exact expression for how teleportation affects the loss at later times in gradient flow, and is there a closed-form optimal destination?
- Can teleportation with discrete (permutation) symmetries reach better minima?
- How does the link to second-order methods hold under non-transitive actions, non-optimal group elements and infrequent teleportation?
- How does teleportation change generalization bounds, given the earlier overfitting seen on MNIST?
- How does teleportation integrate with Adam and RMSprop?
- Can teleportation be made cheap enough that its runtime does not dominate training?

## 📝 Notes on reading

- Version read: arXiv v3 (4 Jan 2023), which states it appeared at NeurIPS 2022; the packet venue says arXiv preprint.
- Figures 2-8 are plots whose values were extracted as axis ticks only; results were claimed from the text describing them.
- Most equations (group actions, complexity O(...) expressions, exponent-heavy learning rates) are garbled in the extraction; complexity orders were paraphrased rather than copied.
- Section 5.1 calls Proposition 5.1 a condition to accelerate; the abstract calls it a necessary condition, while the proof shows it as a sufficient speedup condition.
- Section 6.2 refers to hyperparameter K in Algorithm 2 (appendix), while the main text describes Algorithm 1.
- Figure 8 caption lists teleport steps up to 32, and the text names a grid of [1, 2, 4, 8, 16, 32].

## Suggested new concepts

- Parameter space symmetry — recurring tool for loss-landscape analysis and optimizer design across papers.
- Symmetry teleportation — an optimization technique that later work extends; worth its own note.
- Level-set optimization — moving within loss level sets as an alternative to local descent steps.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Explotar simetrías del paisaje de parámetros (E.4).

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
