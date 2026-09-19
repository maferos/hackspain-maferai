---
aliases: []
type: "source"
title: "Proximal Policy Optimization Algorithms"
citekey: "Schulman2017proximal"
doi: "10.48550/arXiv.1707.06347"
arxiv: "1707.06347"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1707.06347"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["John Schulman", "Filip Wolski", "Prafulla Dhariwal", "Alec Radford", "Oleg Klimov"]
sha256: ["e78feadadbdbb0b601b3c2bcc81404722cd431a489b307545f9b7bea1e8c4f5b"]
pdf: "Content/Papers/Schulman2017proximal.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 65
---

📄 PDF: [[Schulman2017proximal.pdf]]

> [!abstract] One-sentence summary
> The paper introduces proximal policy optimization (PPO), a first-order policy gradient method whose clipped probability-ratio objective allows several epochs of minibatch updates per batch, matching or beating TRPO, A2C and ACER on MuJoCo and Atari benchmarks while being much simpler to implement.

## Abstract

We propose a new family of policy gradient methods for reinforcement learning, which alternate between sampling data through interaction with the environment, and optimizing a "surrogate" objective function using stochastic gradient ascent. Whereas standard policy gradient methods perform one gradient update per data sample, we propose a novel objective function that enables multiple epochs of minibatch updates. The new methods, which we call proximal policy optimization (PPO), have some of the benefits of trust region policy optimization (TRPO), but they are much simpler to implement, more general, and have better sample complexity (empirically). Our experiments test PPO on a collection of benchmark tasks, including simulated robotic locomotion and Atari game playing, and we show that PPO outperforms other online policy gradient methods, and overall strikes a favorable balance between sample complexity, simplicity, and wall-time. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that Q-learning with function approximation fails on many simple problems and remains poorly understood. (Schulman et al., 2017) `ev:asserted` p. 1 ^schulman2017proximal-001
- The authors state that vanilla policy gradient methods have poor data efficiency on reinforcement learning problems with neural network approximators. (Schulman et al., 2017) `ev:asserted` p. 1 ^schulman2017proximal-002
- The authors note that [[Trust region policy optimization|TRPO]] is not compatible with architectures that include noise, such as dropout, or parameter sharing. (Schulman et al., 2017) `ev:asserted` p. 1 ^schulman2017proximal-003
- The paper aims for an algorithm with the data efficiency and reliable performance of TRPO that uses only first-order optimization. (Schulman et al., 2017) `ev:asserted` p. 1 ^schulman2017proximal-004
- The proposed objective uses clipped probability ratios, forming a pessimistic estimate, or lower bound, of the performance of the policy. (Schulman et al., 2017) `ev:asserted` p. 1 ^schulman2017proximal-005
- The authors state that on Atari PPO performs significantly better than A2C in sample complexity, with performance similar to ACER. (Schulman et al., 2017) `ev:asserted` p. 1 ^schulman2017proximal-006
- The authors state that performing multiple optimization steps on the vanilla policy gradient loss with one trajectory often causes destructively large updates. (Schulman et al., 2017) `ev:asserted` p. 2 ^schulman2017proximal-007
- [[Trust region policy optimization|TRPO]] maximizes a surrogate objective subject to a constraint on the mean KL divergence between the old and new policies. (Schulman et al., 2017) `ev:cited` p. 2 ^schulman2017proximal-008
- [[Trust region policy optimization|TRPO]] uses a hard constraint rather than a penalty because choosing a single penalty coefficient that works across problems is hard. (Schulman et al., 2017) `ev:asserted` p. 2 ^schulman2017proximal-009
- The authors state that a fixed penalty coefficient with SGD on the penalized objective is not sufficient to emulate TRPO's monotonic improvement. (Schulman et al., 2017) `ev:asserted` p. 2 ^schulman2017proximal-010
- The clipped objective takes the minimum of the unclipped term and a term with the probability ratio clipped to [1 − ϵ, 1 + ϵ]. (Schulman et al., 2017) `ev:asserted` p. 3 ^schulman2017proximal-011
- The paper gives ϵ = 0.2 as an example value for the clipping hyperparameter of the clipped surrogate objective. (Schulman et al., 2017) `ev:reported` p. 3 ^schulman2017proximal-012
- Clipping the probability ratio removes the incentive for moving the ratio outside of the interval [1 − ϵ, 1 + ϵ]. (Schulman et al., 2017) `ev:asserted` p. 3 ^schulman2017proximal-013
- The clipped objective ignores a change in probability ratio only when that change would make the objective improve. (Schulman et al., 2017) `ev:asserted` p. 3 ^schulman2017proximal-014
- The clipped objective equals the conservative policy iteration objective to first order around the old parameters but diverges farther away. (Schulman et al., 2017) `ev:computed` p. 3 ^schulman2017proximal-015
- Without a constraint, maximizing the conservative policy iteration surrogate would lead to an excessively large policy update, according to the authors. (Schulman et al., 2017) `ev:asserted` p. 3 ^schulman2017proximal-016
- On the first Hopper-v1 policy update, the updated policy has a KL divergence of about 0.02 from the initial policy. (Schulman et al., 2017) `ev:measured` p. 4 ^schulman2017proximal-017
- In their experiments, the authors found that the KL penalty performed worse than the clipped surrogate objective. (Schulman et al., 2017) `ev:measured` p. 4 ^schulman2017proximal-018
- The adaptive KL scheme halves the penalty coefficient β when the measured KL divergence falls below dtarg/1.5. (Schulman et al., 2017) `ev:reported` p. 4 ^schulman2017proximal-019
- The adaptive KL scheme doubles the penalty coefficient β when the measured KL divergence exceeds dtarg × 1.5. (Schulman et al., 2017) `ev:reported` p. 4 ^schulman2017proximal-020
- The authors state that the adaptive KL algorithm is not very sensitive to its heuristically chosen update constants. (Schulman et al., 2017) `ev:asserted` p. 4 ^schulman2017proximal-021
- Under the adaptive KL scheme, policy updates with KL divergence significantly different from the target occasionally occur but are rare. (Schulman et al., 2017) `ev:asserted` p. 4 ^schulman2017proximal-022
- The clipped or KL-penalized surrogate losses can be computed with a minor change to a typical policy gradient implementation. (Schulman et al., 2017) `ev:asserted` p. 4 ^schulman2017proximal-023
- When policy and value function share parameters, the loss must combine the policy surrogate with a value function error term. (Schulman et al., 2017) `ev:asserted` p. 5 ^schulman2017proximal-024
- An entropy bonus can further augment the combined objective to ensure sufficient exploration, as suggested in past work. (Schulman et al., 2017) `ev:cited` p. 5 ^schulman2017proximal-025
- The truncated generalized advantage estimator used by PPO reduces to the finite-horizon estimator of Mnih et al. when λ = 1. (Schulman et al., 2017) `ev:computed` p. 5 ^schulman2017proximal-026
- In each PPO iteration, N parallel actors collect T timesteps, then the surrogate is optimized on NT timesteps for K epochs. (Schulman et al., 2017) `ev:reported` p. 5 ^schulman2017proximal-027
- The PPO surrogate loss is optimized with minibatch SGD or, usually for better performance, with the Adam optimizer. (Schulman et al., 2017) `ev:reported` p. 5 ^schulman2017proximal-028
- The surrogate objective comparison used 7 simulated robotics tasks implemented in OpenAI Gym with the MuJoCo physics engine. (Schulman et al., 2017) `ev:reported` p. 6 ^schulman2017proximal-029
- Each algorithm variant was trained for one million timesteps on every task, with 3 random seeds per environment. (Schulman et al., 2017) `ev:reported` p. 6 ^schulman2017proximal-030
- The policy was a fully-connected MLP with two hidden layers of 64 units, outputting the mean of a Gaussian distribution. (Schulman et al., 2017) `ev:reported` p. 6 ^schulman2017proximal-031
- In the surrogate objective comparison, the policy and value function did not share parameters, making coefficient c1 irrelevant. (Schulman et al., 2017) `ev:reported` p. 6 ^schulman2017proximal-032
- No entropy bonus was used in the surrogate objective comparison experiments on the MuJoCo continuous control benchmark. (Schulman et al., 2017) `ev:reported` p. 6 ^schulman2017proximal-033
- Scores were shifted so a random policy scored 0 with the best result set to 1, then averaged over 21 runs. (Schulman et al., 2017) `ev:reported` p. 6 ^schulman2017proximal-034
- Clipping with ϵ = 0.2 reached the highest average normalized score, 0.82, among all surrogate objective settings in Table 1. (Schulman et al., 2017) `ev:measured` p. 6 ^schulman2017proximal-035
- Clipping with ϵ = 0.1 reached an average normalized score of 0.76 on the continuous control benchmark. (Schulman et al., 2017) `ev:measured` p. 6 ^schulman2017proximal-036
- Clipping with ϵ = 0.3 reached an average normalized score of 0.70 on the continuous control benchmark. (Schulman et al., 2017) `ev:measured` p. 6 ^schulman2017proximal-037
- The setting without clipping or penalty scored -0.39, negative because half cheetah produced a score worse than the random policy. (Schulman et al., 2017) `ev:measured` p. 6 ^schulman2017proximal-038
- Adaptive KL with dtarg = 0.01 reached an average normalized score of 0.74, above the other two adaptive targets. (Schulman et al., 2017) `ev:measured` p. 6 ^schulman2017proximal-039
- Fixed KL penalty settings scored between 0.62 at β = 0.3 and 0.72 at β = 3. in normalized score. (Schulman et al., 2017) `ev:measured` p. 6 ^schulman2017proximal-040
- The authors also tried clipping in log space but found its performance to be no better. (Schulman et al., 2017) `ev:measured` p. 6 ^schulman2017proximal-041
- PPO was compared with tuned implementations of TRPO, CEM, vanilla policy gradient with adaptive stepsize, A2C, and A2C with trust region. (Schulman et al., 2017) `ev:reported` p. 6 ^schulman2017proximal-042
- The authors found synchronous A2C to have the same or better performance than the asynchronous A3C version. (Schulman et al., 2017) `ev:measured` p. 7 ^schulman2017proximal-043
- PPO outperforms the previous methods on almost all the continuous control environments after one million timesteps of MuJoCo training. (Schulman et al., 2017) `ev:measured` p. 7 ^schulman2017proximal-044
- PPO was trained on three Roboschool 3D humanoid tasks involving running, steering, and getting up while pelted by cubes. (Schulman et al., 2017) `ev:reported` p. 7 ^schulman2017proximal-045
- In RoboschoolHumanoidFlagrun, the target position is randomly varied every 200 timesteps or whenever the goal is reached. (Schulman et al., 2017) `ev:reported` p. 7 ^schulman2017proximal-046
- Concurrent work by Heess et al. used the adaptive KL variant of PPO to learn locomotion policies for 3D robots. (Schulman et al., 2017) `ev:cited` p. 7 ^schulman2017proximal-047
- On Atari, PPO was compared with well-tuned A2C and ACER, all using the same policy network architecture. (Schulman et al., 2017) `ev:reported` p. 8 ^schulman2017proximal-048
- Game winners were determined by averaging each scoring metric across three trials on the Arcade Learning Environment benchmark. (Schulman et al., 2017) `ev:reported` p. 8 ^schulman2017proximal-049
- On average episode reward over all of training, PPO won 30 Atari games versus 18 for ACER. (Schulman et al., 2017) `ev:measured` p. 8 ^schulman2017proximal-050
- On average episode reward over the last 100 episodes, ACER won 28 Atari games versus 19 for PPO. (Schulman et al., 2017) `ev:measured` p. 8 ^schulman2017proximal-051
- A2C won 1 Atari game under each of the two scoring metrics in the comparison with ACER and PPO. (Schulman et al., 2017) `ev:measured` p. 8 ^schulman2017proximal-052
- The authors conclude that PPO has the stability and reliability of trust-region methods but is much simpler to implement. (Schulman et al., 2017) `ev:asserted` p. 8 ^schulman2017proximal-053
- The authors state that PPO requires only few lines of code change to a vanilla policy gradient implementation. (Schulman et al., 2017) `ev:asserted` p. 8 ^schulman2017proximal-054
- The authors conclude PPO is applicable in more general settings, for example a joint architecture for policy and value function. (Schulman et al., 2017) `ev:asserted` p. 8 ^schulman2017proximal-055
- The MuJoCo benchmark used a horizon of 2048 timesteps, 10 epochs, a minibatch size of 64, and discount 0.99. (Schulman et al., 2017) `ev:reported` p. 10 ^schulman2017proximal-056
- The Roboschool experiments used 32 actors for locomotion, 128 for flagrun, 15 epochs, and a minibatch size of 4096. (Schulman et al., 2017) `ev:reported` p. 10 ^schulman2017proximal-057
- In the Roboschool experiments, the Adam stepsize was adjusted based on the target value of the KL divergence. (Schulman et al., 2017) `ev:reported` p. 10 ^schulman2017proximal-058
- The Atari experiments used a horizon of 128, 3 epochs, 8 actors, and an entropy coefficient of 0.01. (Schulman et al., 2017) `ev:reported` p. 10 ^schulman2017proximal-059
- In the Atari experiments, the clipping parameter ϵ was 0.1 × α, with α linearly annealed from 1 to 0. (Schulman et al., 2017) `ev:reported` p. 10 ^schulman2017proximal-060
- Mean final Atari scores were measured over the last 100 episodes after 40M game frames, corresponding to 10M timesteps. (Schulman et al., 2017) `ev:reported` p. 12 ^schulman2017proximal-061
- On Kangaroo, PPO reached a mean final score of 9928.7, compared with 45.3 for A2C. (Schulman et al., 2017) `ev:measured` p. 12 ^schulman2017proximal-062
- On Enduro, PPO reached a mean final score of 758.3, whereas A2C and ACER both scored 0.0. (Schulman et al., 2017) `ev:measured` p. 12 ^schulman2017proximal-063
- On Gopher, ACER reached a mean final score of 37802.3, compared with 2932.9 for PPO. (Schulman et al., 2017) `ev:measured` p. 12 ^schulman2017proximal-064
- On MontezumaRevenge, PPO reached a mean final score of 42.0, compared with 0.3 for ACER. (Schulman et al., 2017) `ev:measured` p. 12 ^schulman2017proximal-065

## 🎯 Contributions

## 📖 Glossary

- **Probability ratio** — Ratio of new-policy to old-policy action probability, equal to 1 at the old parameters.
- **Clipped surrogate objective** — PPO loss taking the minimum of unclipped and ratio-clipped advantage-weighted terms.
- **Surrogate objective** — Importance-weighted advantage objective optimized in place of true policy performance.
- **Trust region policy optimization (TRPO)** — Policy optimization maximizing a surrogate under a KL-divergence constraint, solved with conjugate gradient.
- **Adaptive KL penalty** — KL-divergence penalty whose coefficient is halved or doubled to track a target KL.
- **Generalized advantage estimation (GAE)** — Advantage estimator mixing multi-step temporal-difference errors with a decay parameter λ.
- **Advantage function** — Expected return of an action minus the state value under the policy.
- **A2C** — Synchronous advantage actor-critic, the synchronous version of A3C.
- **ACER** — Actor-critic with experience replay, a sample-efficient off-policy actor-critic method.
- **Conservative policy iteration (CPI)** — Method of Kakade and Langford where the unclipped ratio surrogate was proposed.

## ❓ Open questions

- Why does ACER beat PPO on final performance in 28 Atari games while PPO learns faster over training?
- How sensitive is PPO to the clipping parameter ϵ outside the three values tested on MuJoCo?
- Does the clipped objective actually bound the KL divergence of updates, given it only removes the incentive to move the ratio?
- How does PPO compare with off-policy methods on wall-time and sample efficiency, beyond the online policy gradient baselines?
- Can clipping and an adaptive KL penalty be combined profitably, as Section 4 suggests is possible but does not test?
- How does performance change when policy and value function share parameters on continuous control, which the MuJoCo comparison did not use?

## 📝 Notes on reading

Version read: arXiv v2 (arXiv:1707.06347v2, 28 Aug 2017), matching the packet identifier.

Figure 1 plots one term of the clipped objective against the probability ratio for positive and negative advantages; Figure 2 interpolates several surrogates along the first Hopper-v1 update direction; Figure 3 shows MuJoCo learning curves for six algorithms over one million timesteps; Figure 4 shows PPO learning curves on three Roboschool humanoid tasks; Figure 5 shows still frames of a Flagrun policy; Figure 6 shows Atari learning curves. These were only described, not claimed per curve.

Inconsistency: Appendix B text and the captions of Figure 6 and Table 6 describe a comparison of PPO against A2C only, but Figure 6 and Table 6 also include ACER.

Section 2.1 states that multi-step optimization of the vanilla policy gradient loss gives destructively large updates, but notes the results are not shown.

Hyperparameter tables: the Roboschool Adam stepsize is printed as an asterisk (adjusted to a KL target); the Atari minibatch size is printed as 32 × 8 and Adam stepsize as 2.5 × 10−4 × α; the MuJoCo Adam stepsize is 3 × 10−4. The equations extracted as fragmented text and were read against the prose.

Only headline cells of the 49-game Table 6 were claimed.

## Suggested new concepts

- Proximal policy optimization — central on-policy RL algorithm used across robotics and RL fine-tuning; deserves its own concept note.
- Clipped surrogate objective — the key mechanism distinguishing PPO, reusable in other policy optimization methods.
- Trust region policy optimization — the direct predecessor PPO emulates, cited across policy gradient literature.
- Generalized advantage estimation — advantage estimator used by PPO and many actor-critic methods.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Sustituto de primer orden de la trust region; estándar para fine-tuning (B.5, D.2).
