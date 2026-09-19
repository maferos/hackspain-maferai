---
aliases: []
type: "source"
title: "Scalable trust-region method for deep RL using Kronecker-factored approximation (ACKTR)"
citekey: "Wu2017scalable"
doi: "10.48550/arXiv.1708.05144"
arxiv: "1708.05144"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1708.05144"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Yuhuai Wu", "Elman Mansimov", "Shun Liao", "Roger Grosse", "Jimmy Ba"]
sha256: ["11decb0222c4c0639b5bddc3d07babe6b7f66c796c502efd0d352078aeb61e14"]
pdf: "Content/Papers/Wu2017scalable.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 70
---

📄 PDF: [[Wu2017scalable.pdf]]

> [!abstract] One-sentence summary
> ACKTR applies Kronecker-factored natural-gradient updates with a trust region to both actor and critic, reporting 2- to 3-fold sample-efficiency gains over A2C and TRPO on Atari and MuJoCo at only 10-25% extra compute per update.

## Abstract

In this work, we propose to apply trust region optimization to deep reinforcement learning using a recently proposed Kronecker-factored approximation to the curvature. We extend the framework of natural policy gradient and propose to optimize both the actor and the critic using Kronecker-factored approximate curvature (K-FAC) with trust region; hence we call our method Actor Critic using Kronecker-Factored Trust Region (ACKTR). To the best of our knowledge, this is the first scalable trust region natural gradient method for actor-critic methods. It is also a method that learns non-trivial tasks in continuous control as well as discrete control policies directly from raw pixel inputs. We tested our approach across discrete domains in Atari games as well as continuous domains in the MuJoCo environment. With the proposed methods, we are able to achieve higher rewards and a 2- to 3-fold improvement in sample efficiency on average, compared to previous state-of-the-art on-policy actor-critic methods. Code is available at https://github.com/openai/baselines (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that SGD and related first-order methods explore weight space inefficiently when training deep reinforcement learning policies. (Wu et al., 2017) `ev:asserted` p. 1 ^wu2017scalable-001
- A previously proposed distributed approach runs multiple agents in parallel but yields rapidly diminishing returns of sample efficiency as parallelism increases. (Wu et al., 2017) `ev:cited` p. 1 ^wu2017scalable-002
- The authors note that robotic interaction with the real world is typically scarcer than computation time, making sample efficiency a dominant RL concern. (Wu et al., 2017) `ev:asserted` p. 1 ^wu2017scalable-003
- Exact [[Natural gradient descent|natural gradient]] computation is intractable because it requires inverting the [[Fisher information matrix]], according to the authors. (Wu et al., 2017) `ev:asserted` p. 2 ^wu2017scalable-004
- [[Trust region policy optimization|TRPO]] avoids explicitly storing or inverting the Fisher matrix by relying on Fisher-vector products instead of the exact matrix. (Wu et al., 2017) `ev:cited` p. 2 ^wu2017scalable-005
- The authors argue [[Trust region policy optimization|TRPO]] is impractical for large models, since it typically needs many conjugate gradient steps for a single parameter update. (Wu et al., 2017) `ev:asserted` p. 2 ^wu2017scalable-006
- [[Kronecker-factored approximate curvature|K-FAC]] is described as a scalable approximation to natural gradient whose per-update cost is comparable to an SGD update. (Wu et al., 2017) `ev:cited` p. 2 ^wu2017scalable-007
- K-FAC keeps a running average of curvature information, which the authors state allows it to use small batches, unlike TRPO. (Wu et al., 2017) `ev:cited` p. 2 ^wu2017scalable-008
- ACKTR uses [[Kronecker-factored preconditioning|a Kronecker-factored approximation]] to [[Natural policy gradient|natural policy gradient]] that allows the covariance matrix of the gradient to be inverted efficiently. (Wu et al., 2017) `ev:asserted` p. 2 ^wu2017scalable-009
- The authors claim to be the first to extend [[Natural policy gradient|natural policy gradient]] to optimize value functions via a Gauss-Newton approximation. (Wu et al., 2017) `ev:asserted` p. 2 ^wu2017scalable-010
- In practice, the per-update computation cost of ACKTR is only 10% to 25% higher than that of SGD-based methods. (Wu et al., 2017) `ev:measured` p. 2 ^wu2017scalable-011
- Following A3C, the advantage function is defined as k-step returns with function approximation using a learned value network. (Wu et al., 2017) `ev:reported` p. 3 ^wu2017scalable-012
- The value network is trained with temporal difference updates that minimize the squared difference between bootstrapped k-step returns and predicted values. (Wu et al., 2017) `ev:reported` p. 3 ^wu2017scalable-013
- [[Kronecker-factored approximate curvature|K-FAC]] approximates each layer's Fisher block as the Kronecker product of activation second moments and backpropagated-derivative second moments. (Wu et al., 2017) `ev:cited` p. 3 ^wu2017scalable-014
- This approximation can be interpreted as assuming that second-order statistics of activations and of backpropagated derivatives are uncorrelated. (Wu et al., 2017) `ev:asserted` p. 3 ^wu2017scalable-015
- The [[Kronecker-factored approximate curvature|K-FAC]] approximate natural gradient update only requires computations on matrices comparable in size to the layer weight matrix. (Wu et al., 2017) `ev:computed` p. 3 ^wu2017scalable-016
- The authors state that no scalable, sample-efficient and general-purpose instantiation of the [[Natural policy gradient|natural policy gradient]] existed before ACKTR. (Wu et al., 2017) `ev:asserted` p. 4 ^wu2017scalable-017
- Modelling the critic output as a Gaussian makes the Gauss-Newton matrix equivalent to the Fisher matrix, which allows K-FAC on the critic. (Wu et al., 2017) `ev:reported` p. 4 ^wu2017scalable-018
- When actor and critic share lower layers, ACKTR builds one Fisher metric over their joint distribution by assuming independent outputs. (Wu et al., 2017) `ev:reported` p. 4 ^wu2017scalable-019
- ACKTR uses the factorized Tikhonov damping approach described in the original K-FAC work of Martens and Grosse. (Wu et al., 2017) `ev:reported` p. 4 ^wu2017scalable-020
- ACKTR computes the second-order statistics and inverses required by the Kronecker approximation asynchronously to reduce computation time. (Wu et al., 2017) `ev:reported` p. 4 ^wu2017scalable-021
- Schulman et al. observed that SGD-like natural gradient updates can cause large policy updates and premature convergence to near-deterministic policies. (Wu et al., 2017) `ev:cited` p. 5 ^wu2017scalable-022
- ACKTR adopts a trust-region formulation of K-FAC where the effective step size is capped by a maximum learning rate and a trust region radius. (Wu et al., 2017) `ev:reported` p. 5 ^wu2017scalable-023
- With shared actor-critic representations, one set of step-size hyperparameters is tuned plus a weighting of the critic loss relative to the actor loss. (Wu et al., 2017) `ev:reported` p. 5 ^wu2017scalable-024
- The authors argue TRPO's repeated Fisher-vector product computation prevents it from scaling to the larger architectures used for image observations. (Wu et al., 2017) `ev:asserted` p. 5 ^wu2017scalable-025
- Although TRPO shows better per-iteration progress than first-order policy gradient methods, it is generally less sample efficient. (Wu et al., 2017) `ev:asserted` p. 5 ^wu2017scalable-026
- The authors suggest actor-critic methods using experience replay or auxiliary objectives could potentially be combined with ACKTR for more sample efficiency. (Wu et al., 2017) `ev:asserted` p. 5 ^wu2017scalable-027
- ACKTR was evaluated on Atari 2600 discrete control tasks from OpenAI Gym, simulated by the Arcade Learning Environment. (Wu et al., 2017) `ev:reported` p. 5 ^wu2017scalable-028
- Continuous control experiments for ACKTR and the baselines used OpenAI Gym benchmark tasks simulated by the MuJoCo physics engine. (Wu et al., 2017) `ev:reported` p. 6 ^wu2017scalable-029
- The baselines were A2C, a synchronous and batched version of A3C, and the trust-region optimizer TRPO. (Wu et al., 2017) `ev:reported` p. 6 ^wu2017scalable-030
- On Atari, TRPO was limited to a smaller architecture because of the computing burden of its conjugate gradient inner loop. (Wu et al., 2017) `ev:reported` p. 6 ^wu2017scalable-031
- On six Atari games trained for 10 million timesteps, ACKTR outperformed A2C in sample efficiency by a significant margin in all games. (Wu et al., 2017) `ev:measured` p. 6 ^wu2017scalable-032
- [[Trust region policy optimization|TRPO]] could only learn two of the six Atari games, Seaquest and Pong, within 10 million timesteps. (Wu et al., 2017) `ev:measured` p. 6 ^wu2017scalable-033
- TRPO performed worse than A2C in terms of sample efficiency on the six standard Atari games. (Wu et al., 2017) `ev:measured` p. 6 ^wu2017scalable-034
- On Beamrider, Breakout, Pong and Q-bert, A2C required respectively 2.7, 3.5, 5.3, and 3.0 times more episodes than ACKTR to reach human performance. (Wu et al., 2017) `ev:measured` p. 6 ^wu2017scalable-035
- In Space Invaders, ACKTR achieved an average reward of 19723, 12 times better than the human performance level of 1652. (Wu et al., 2017) `ev:measured` p. 6 ^wu2017scalable-036
- On Breakout, Q-bert and Beamrider, ACKTR achieved 26%, 35%, and 67% larger episode rewards than A2C respectively. (Wu et al., 2017) `ev:measured` p. 6 ^wu2017scalable-037
- ACKTR was on par with Q-learning methods in sample efficiency in 36 out of 44 Atari benchmarks. (Wu et al., 2017) `ev:measured` p. 6 ^wu2017scalable-038
- In Atlantis, ACKTR learned to obtain rewards of 2 million in 1.3 hours, or 600 episodes. (Wu et al., 2017) `ev:measured` p. 6 ^wu2017scalable-039
- A2C took 10 hours and 6000 episodes to reach the same Atlantis reward level that ACKTR reached. (Wu et al., 2017) `ev:measured` p. 6 ^wu2017scalable-040
- The authors state ACKTR is 10 times more sample efficient than A2C on the Atari game Atlantis. (Wu et al., 2017) `ev:measured` p. 4 ^wu2017scalable-041
- On eight MuJoCo tasks trained for 1 million timesteps, ACKTR significantly outperformed baselines on six tasks. (Wu et al., 2017) `ev:measured` p. 6 ^wu2017scalable-042
- ACKTR performed competitively with A2C on the remaining two MuJoCo tasks, Walker2d and Swimmer, after 1 million timesteps. (Wu et al., 2017) `ev:measured` p. 6 ^wu2017scalable-043
- The authors note that continuous control tasks are sometimes more challenging than Atari due to high-dimensional action spaces and exploration. (Wu et al., 2017) `ev:asserted` p. 6 ^wu2017scalable-044
- Over 30 million timesteps, ACKTR reached the specified reward threshold faster than both baselines on all MuJoCo tasks except Swimmer. (Wu et al., 2017) `ev:measured` p. 7 ^wu2017scalable-045
- On Swimmer, TRPO achieved 4.1 times better sample efficiency than ACKTR in reaching the reward threshold. (Wu et al., 2017) `ev:measured` p. 7 ^wu2017scalable-046
- On Ant, ACKTR was 16.4 times more sample efficient than TRPO in reaching the specified reward threshold. (Wu et al., 2017) `ev:measured` p. 7 ^wu2017scalable-047
- Mean reward scores of ACKTR, A2C and TRPO were comparable, except TRPO achieved a 10% better score on Walker2d. (Wu et al., 2017) `ev:measured` p. 7 ^wu2017scalable-048
- On Ant, ACKTR crossed the 3500 reward threshold after 3660 episodes, compared with 106186 for A2C and 60156 for TRPO. (Wu et al., 2017) `ev:measured` p. 8 ^wu2017scalable-049
- The authors attribute part of the difficulty of pixel-based MuJoCo control to slower rendering, 0.5 seconds versus 0.002 seconds in Atari. (Wu et al., 2017) `ev:asserted` p. 7 ^wu2017scalable-050
- From pixels, ACKTR achieved 1.6, 2.8, and 1.7 times greater final reward than A2C on Reacher, HalfCheetah, and Walker2d. (Wu et al., 2017) `ev:measured` p. 7 ^wu2017scalable-051
- Applying ACKTR to the actor improved over A2C regardless of whether the critic used the Euclidean or Gauss-Newton norm. (Wu et al., 2017) `ev:measured` p. 7 ^wu2017scalable-052
- Using the Gauss-Newton norm for the critic gave more substantial improvements in sample efficiency than the Euclidean norm on HalfCheetah and Breakout. (Wu et al., 2017) `ev:measured` p. 8 ^wu2017scalable-053
- The Euclidean critic norm showed larger variance over random seeds, suggesting the Gauss-Newton norm helps stabilize training. (Wu et al., 2017) `ev:measured` p. 8 ^wu2017scalable-054
- Adaptive Gauss-Newton, estimating σ from the Bellman error variance, did not provide significant improvement over vanilla Gauss-Newton. (Wu et al., 2017) `ev:measured` p. 8 ^wu2017scalable-055
- ACKTR increased computing time by at most 25% per timestep over A2C, averaged over six Atari games and eight MuJoCo tasks. (Wu et al., 2017) `ev:measured` p. 8 ^wu2017scalable-056
- At Atari batch size 640, ACKTR processed 852 timesteps per second, compared with 1162 for A2C and 177 for TRPO. (Wu et al., 2017) `ev:measured` p. 8 ^wu2017scalable-057
- With batch sizes of 160 and 640, ACKTR with the larger batch performed as well as with the smaller batch. (Wu et al., 2017) `ev:measured` p. 8 ^wu2017scalable-058
- A2C experienced significant degradation in sample efficiency when using a larger batch size, unlike ACKTR. (Wu et al., 2017) `ev:measured` p. 8 ^wu2017scalable-059
- The authors suggest ACKTR has potential for large speed-ups in distributed settings that require large mini-batches. (Wu et al., 2017) `ev:asserted` p. 9 ^wu2017scalable-060
- The authors report 2- to 3-fold improvements in sample efficiency on average compared with A2C and TRPO across Atari and MuJoCo. (Wu et al., 2017) `ev:measured` p. 9 ^wu2017scalable-061
- The authors claim to be the first to train several non-trivial continuous control tasks directly from raw pixel observations. (Wu et al., 2017) `ev:asserted` p. 9 ^wu2017scalable-062
- Using 32 rather than 64 filters in the third convolutional layer saved Fisher inverse computation time without performance degradation. (Wu et al., 2017) `ev:measured` p. 11 ^wu2017scalable-063
- Atari batch sizes were 640 for ACKTR, 80 for A2C, and 512 for TRPO, chosen for better sample efficiency. (Wu et al., 2017) `ev:reported` p. 11 ^wu2017scalable-064
- For pixel inputs, separating policy and value into two networks gave better empirical performance for both ACKTR and A2C. (Wu et al., 2017) `ev:measured` p. 11 ^wu2017scalable-065
- Without orthogonal initialization of both networks, the A2C baseline failed to improve its episode reward in pixel-based experiments. (Wu et al., 2017) `ev:measured` p. 11 ^wu2017scalable-066
- Results on the remaining Atari games were obtained with a single random seed and without tuning any hyperparameters. (Wu et al., 2017) `ev:reported` p. 12 ^wu2017scalable-067
- The authors state ACKTR takes only 16 hours on a modern GPU, whereas Q-learning methods usually take days per training. (Wu et al., 2017) `ev:asserted` p. 12 ^wu2017scalable-068
- On Atari, adaptive Gauss-Newton hurt sample efficiency in Beamrider, Q-bert and Seaquest compared with vanilla Gauss-Newton. (Wu et al., 2017) `ev:measured` p. 13 ^wu2017scalable-069
- In HalfCheetah and Reacher, the exact KL change during ACKTR training stayed close to the trust region radius. (Wu et al., 2017) `ev:measured` p. 14 ^wu2017scalable-070

## 🎯 Contributions

## 📖 Glossary

- **Natural gradient** — Steepest descent under the Fisher metric, invariant to model parameterization.
- **K-FAC** — Kronecker-factored approximate curvature; approximates each layer's Fisher block as a Kronecker product.
- **Trust region** — Constraint scaling updates so the policy's KL change stays below a radius.
- **TRPO** — Trust-region policy optimization using conjugate gradient with Fisher-vector products.
- **A2C** — Synchronous, batched version of the asynchronous advantage actor-critic (A3C) method.
- **Gauss-Newton matrix** — Curvature approximation E[J^T J] for least-squares problems; equals Fisher under Gaussian outputs.
- **Advantage function** — Relative value of an action at a state versus the state's expected value.
- **Sample efficiency** — Performance achieved per number of environment timesteps or episodes consumed.

## ❓ Open questions

- Does ACKTR realize the suggested large speed-ups in an actual distributed, large-mini-batch training setup?
- Can ACKTR be combined with experience replay or auxiliary objectives to further improve sample efficiency?
- How robust are the extended Atari results, given a single seed and no hyperparameter tuning?
- Why does ACKTR score 0.0 on Enduro and Freeway, and is this an exploration failure?
- How well do Kronecker-factored natural gradient approximations transfer to off-policy or other RL algorithms?
- How accurate is the Kronecker-factored curvature beyond the indirect KL check on two MuJoCo tasks?

## 📝 Notes on reading

Version read: arXiv 1708.05144v2 (18 Aug 2017), matching the packet identifier.

Figures 1, 3-9 are learning curves that could only be described from their captions and the text; no per-curve values were claimed. Figure 2 caption states ACKTR reached 2 million Atlantis reward at 2.5 million timesteps versus 25 million for A2C.

Inconsistencies: human-level scores differ between Table 1 and Table 4 (Breakout 31.8 vs 30.5; Space Invaders 1652.0 vs 1,668.7; Beamrider 5775.0 vs 16,926.5; Seaquest 20182.0 vs 42,054.7), likely different human baselines (Table 4 uses 30 no-op starts from Wang et al.). The Figure 3, 4, 6 and 8 captions for MuJoCo state '1 timestep equals 4 frames', which appears copied from the Atari captions. The abstract compares to on-policy actor-critic methods, while the conclusion attributes the 2- to 3-fold gain to comparisons with both A2C and TRPO. The 36-of-44 Q-learning comparison (p. 6) rests on a single-seed, untuned subset (Appendix B); Table 4 lists roughly 49 games, so the 44 count is not directly traceable in the table. Section 5.1 says ACKTR 'consumed a lot less computation time' than Q-learning without a measured table; Appendix B gives 16 hours versus 'days'. Table 1's TRPO column is at 10 M timesteps, not 50 M, so it is not directly comparable with the ACKTR and A2C columns. Table 2 averages the top 10 episode rewards over the 3 best of 8 random seeds, a favourable selection.

The Appendix C comparison with OpenAI's A2C and TRPO baselines (Figure 6) and the Appendix D per-task MuJoCo effects of adaptive Gauss-Newton were only partially claimed.

## Suggested new concepts

- Kronecker-factored approximate curvature (K-FAC) — a reusable second-order optimizer approximation used across supervised and RL work.
- Natural policy gradient — the underlying method ACKTR scales; links Kakade, TRPO and natural actor-critic lines.
- Trust-region policy optimization — a family of KL-constrained policy updates that ACKTR, TRPO and PPO belong to.
- Gauss-Newton critic optimization — treating value-function fitting as least squares with a Fisher-equivalent curvature norm.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — K-FAC + trust region en actor-crítico, probado en MuJoCo (B.3, F.7).
