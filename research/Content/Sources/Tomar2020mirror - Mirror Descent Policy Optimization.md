---
aliases: []
type: "source"
title: "Mirror Descent Policy Optimization"
citekey: "Tomar2020mirror"
doi: "10.48550/arXiv.2005.09814"
arxiv: "2005.09814"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2005.09814"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Manan Tomar", "Lior Shani", "Yonathan Efroni", "Mohammad Ghavamzadeh"]
sha256: ["b0f3962739b97c24f8a64d1aabc474fd25170d38ea72ec4c142f8c57600d7010"]
pdf: "Content/Papers/Tomar2020mirror.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Tomar2020mirror.pdf]]

> [!abstract] One-sentence summary
> The paper derives on-policy and off-policy RL algorithms (MDPO) from mirror descent theory by approximately solving trust-region updates with multiple gradient steps, relates them to TRPO, PPO and SAC, and reports on-par or better MuJoCo performance.

## Abstract

Mirror descent (MD), a well-known first-order method in constrained convex optimization, has recently been shown as an important tool to analyze trust-region algorithms in reinforcement learning (RL). However, there remains a considerable gap between such theoretically analyzed algorithms and the ones used in practice. Inspired by this, we propose an efficient RL algorithm, called {\em mirror descent policy optimization} (MDPO). MDPO iteratively updates the policy by {\em approximately} solving a trust-region problem, whose objective function consists of two terms: a linearization of the standard RL objective and a proximity term that restricts two consecutive policies to be close to each other. Each update performs this approximation by taking multiple gradient steps on this objective function. We derive {\em on-policy} and {\em off-policy} variants of MDPO, while emphasizing important design choices motivated by the existing theory of MD in RL. We highlight the connections between on-policy MDPO and two popular trust-region RL algorithms: TRPO and PPO, and show that explicitly enforcing the trust-region constraint is in fact {\em not} a necessity for high performance gains in TRPO. We then show how the popular soft actor-critic (SAC) algorithm can be derived by slight modifications of off-policy MDPO. Overall, MDPO is derived from the MD principles, offers a unified approach to viewing a number of popular RL algorithms, and performs better than or on-par with TRPO, PPO, and SAC in a number of continuous control tasks. Code is available at \url{https://github.com/manantomar/Mirror-Descent-Policy-Optimization}. (arXiv)

## 🧠 Key ideas (atomic)

- The paper proposes mirror descent policy optimization, an RL algorithm that approximately solves a trust-region problem by taking multiple gradient steps. (Tomar et al., 2020) `ev:asserted` p. 1 ^tomar2020mirror-001
- Mirror descent is a first-order optimization method for constrained convex problems, only recently investigated for policy optimization in reinforcement learning. (Tomar et al., 2020) `ev:cited` p. 1 ^tomar2020mirror-002
- The authors state that considerable gaps remain between trust-region RL algorithms analysed in tabular form and the algorithms used in practice. (Tomar et al., 2020) `ev:asserted` p. 1 ^tomar2020mirror-003
- TRPO enforces the trust-region constraint explicitly through a line search that keeps the KL divergence to the old policy below a threshold. (Tomar et al., 2020) `ev:cited` p. 1 ^tomar2020mirror-004
- Clipping the new-to-old policy ratio in PPO has been shown not to prevent ratios going out of bound, only reducing its probability. (Tomar et al., 2020) `ev:cited` p. 1 ^tomar2020mirror-005
- Earlier work proved global-optimum convergence rates for MD-style RL algorithms in the tabular case, matching the rates of mirror descent in convex optimization. (Tomar et al., 2020) `ev:cited` p. 3 ^tomar2020mirror-006
- On-policy MDPO computes its SGD updates using Monte-Carlo estimates of the advantage function gathered by following the current policy. (Tomar et al., 2020) `ev:reported` p. 3 ^tomar2020mirror-007
- Off-policy MDPO calculates its SGD update by estimating the advantage function from samples drawn from a replay buffer. (Tomar et al., 2020) `ev:reported` p. 3 ^tomar2020mirror-008
- A single SGD step on the MDPO objective reduces to vanilla policy gradient, since the KL gradient is zero at the current policy. (Tomar et al., 2020) `ev:computed` p. 3 ^tomar2020mirror-009
- Since the policy space is often Gaussian in practice, on-policy MDPO uses the closed-form KL divergence when estimating its gradient. (Tomar et al., 2020) `ev:reported` p. 3 ^tomar2020mirror-010
- Unlike TRPO, on-policy MDPO does not explicitly enforce the trust-region constraint but approximately satisfies it through multiple SGD steps. (Tomar et al., 2020) `ev:asserted` p. 4 ^tomar2020mirror-011
- On-policy MDPO uses simple SGD instead of natural gradient, avoiding the overhead of approximating the inverse Fisher information matrix. (Tomar et al., 2020) `ev:asserted` p. 4 ^tomar2020mirror-012
- On-policy MDPO uses the KL direction consistent with mirror descent in convex optimization, which differs from the direction used by TRPO. (Tomar et al., 2020) `ev:asserted` p. 4 ^tomar2020mirror-013
- On-policy MDPO anneals the step-size tk from 1 to 0 over the iterations, a schedule motivated by mirror descent theory. (Tomar et al., 2020) `ev:reported` p. 4 ^tomar2020mirror-014
- The authors argue that despite clipping, PPO does not guarantee that the trust-region constraint is always satisfied. (Tomar et al., 2020) `ev:asserted` p. 4 ^tomar2020mirror-015
- Recent results attribute most of the improved performance of PPO to code-level optimization techniques, in particular generalized advantage estimation. (Tomar et al., 2020) `ev:cited` p. 4 ^tomar2020mirror-016
- KL-PPO uses mini-batches whereas on-policy MDPO uses the entire data for its multiple gradient updates at each round. (Tomar et al., 2020) `ev:asserted` p. 4 ^tomar2020mirror-017
- The authors conjecture that the differences in batching or in the tk schedule may explain the inferior performance of KL-PPO relative to PPO. (Tomar et al., 2020) `ev:asserted` p. 4 ^tomar2020mirror-018
- Off-policy MDPO samples a batch of states from a replay buffer to emulate the uniform state sampling required by its update rule. (Tomar et al., 2020) `ev:reported` p. 5 ^tomar2020mirror-019
- Off-policy MDPO uses two neural networks to estimate the value functions, forming the advantage estimate as their difference. (Tomar et al., 2020) `ev:reported` p. 5 ^tomar2020mirror-020
- The off-policy MDPO policy update uses the reparameterization trick, replacing the objective with a loss over sampled Gaussian noise. (Tomar et al., 2020) `ev:reported` p. 5 ^tomar2020mirror-021
- The off-policy MDPO loss can be rederived by writing the mirror descent update as a KL projection onto the parameterized policy space. (Tomar et al., 2020) `ev:computed` p. 6 ^tomar2020mirror-022
- The SAC loss function is re-obtained by replacing the current policy with the uniform policy in the off-policy MDPO objective. (Tomar et al., 2020) `ev:computed` p. 6 ^tomar2020mirror-023
- The authors interpret SAC as a trust-region algorithm with respect to the uniform policy, which encourages the new policy to remain explorative. (Tomar et al., 2020) `ev:asserted` p. 6 ^tomar2020mirror-024
- The authors argue that the KL projection in SAC is dictated by the choice of Bregman divergence, whereas SAC's authors call it arbitrary. (Tomar et al., 2020) `ev:asserted` p. 6 ^tomar2020mirror-025
- The authors suggest the hard version of SAC can be regarded as an RL implementation of the follow-the-regularized-leader algorithm. (Tomar et al., 2020) `ev:asserted` p. 6 ^tomar2020mirror-026
- Mei et al. proposed ECPO, an algorithm that resembles soft off-policy MDPO except for using the forward KL direction. (Tomar et al., 2020) `ev:cited` p. 6 ^tomar2020mirror-027
- The authors state that more experiments are required to better understand the effect of the KL direction in MDPO algorithms. (Tomar et al., 2020) `ev:asserted` p. 6 ^tomar2020mirror-028
- The experiments compare on-policy and off-policy MDPO against TRPO, PPO and SAC on continuous control tasks from OpenAI Gym. (Tomar et al., 2020) `ev:reported` p. 6 ^tomar2020mirror-029
- Tabular results report final training scores averaged over 5 runs, together with their 95% confidence intervals. (Tomar et al., 2020) `ev:reported` p. 6 ^tomar2020mirror-030
- Off-policy MDPO is tested with Bregman divergences induced by two potential functions, the Shannon entropy and the Tsallis entropy. (Tomar et al., 2020) `ev:reported` p. 6 ^tomar2020mirror-031
- Across the tasks, m = 10 gradient steps per iteration seemed the best value for on-policy MDPO in the authors' experiments. (Tomar et al., 2020) `ev:measured` p. 7 ^tomar2020mirror-032
- Using a single gradient step, m = 1, led to inferior on-policy MDPO performance compared with m = 10. (Tomar et al., 2020) `ev:measured` p. 7 ^tomar2020mirror-033
- Performing multiple gradient steps per iteration in TRPO did not improve performance, sometimes performing worse than a single-step update. (Tomar et al., 2020) `ev:measured` p. 7 ^tomar2020mirror-034
- Off-policy MDPO stays close to an m-step old copy of the current policy, performing a single gradient update per iteration. (Tomar et al., 2020) `ev:reported` p. 7 ^tomar2020mirror-035
- The off-policy MDPO experiments use m = 1000, the value with the most reasonable performance across the tasks. (Tomar et al., 2020) `ev:measured` p. 7 ^tomar2020mirror-036
- The authors report that on-policy MDPO performs better than or on par with TRPO across all tasks. (Tomar et al., 2020) `ev:measured` p. 7 ^tomar2020mirror-037
- In the authors' experiments, on-policy MDPO performs better than PPO across all the tested continuous control tasks. (Tomar et al., 2020) `ev:measured` p. 7 ^tomar2020mirror-038
- On-policy MDPO can be implemented more efficiently than TRPO because it does not require the extra line-search step. (Tomar et al., 2020) `ev:asserted` p. 7 ^tomar2020mirror-039
- The authors state that the TRPO line search is an incompatible part of the computation graph in auto-diff packages such as TensorFlow. (Tomar et al., 2020) `ev:asserted` p. 7 ^tomar2020mirror-040
- With code-level optimizations and GAE, on-policy MDPO scored 5211 (± 43) on Ant-v2, against 4682 (± 278) for TRPO. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-041
- With code-level optimizations and GAE, TRPO scored 4414 (± 132) on Humanoid-v2, higher than on-policy MDPO at 3234 (± 566). (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-042
- With code-level optimizations and GAE, PPO scored 59 (± 133) on Ant-v2 at 10M timesteps, versus 5211 (± 43) for MDPO. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-043
- TRPO performed better than PPO consistently, both in the vanilla case and with code-level optimizations including GAE added. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-044
- Adding code-level optimizations and GAE improved PPO performance, but not enough to outperform TRPO given the same additions. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-045
- PPO performance improved until the standard 1M time-step mark, then decreased in some tasks, supporting earlier reports of instability. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-046
- In the loaded off-policy comparison, MDPO-KL performed on par with SAC across all the evaluated continuous control tasks. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-047
- The authors report that off-policy MDPO-Tsallis, which adds a hyper-parameter q to tune, can outperform SAC across all tasks. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-048
- The best performing Tsallis q values differ for each domain but always lie in the interval [1.0, 2.0]. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-049
- Off-policy MDPO increased performance in most tasks over on-policy MDPO, in terms of both sample efficiency and final performance. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-050
- Loaded MDPO-Tsallis reached 165882 (± 16604) on HumanoidStandup-v2 with q = 1.4, against 154765 (± 11721) for SAC. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-051
- In preliminary experiments, tuning q in SAC-Tsallis did not bring much improvement over SAC, unlike what was seen for MDPO-Tsallis. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-052
- Mei et al. reported poor performance for policy mirror descent, an algorithm close to off-policy MDPO, when compared with ECPO. (Tomar et al., 2020) `ev:cited` p. 8 ^tomar2020mirror-053
- The authors did not observe such poor performance for off-policy MDPO, although they did not use the code-base of Mei et al. (Tomar et al., 2020) `ev:measured` p. 8 ^tomar2020mirror-054
- As future work, the authors propose evaluating MDPO algorithms on discrete action problems against algorithms like DQN and PPO. (Tomar et al., 2020) `ev:asserted` p. 9 ^tomar2020mirror-055
- The authors consider investigating Bregman divergences other than KL promising, with their Tsallis work being a step in this direction. (Tomar et al., 2020) `ev:asserted` p. 9 ^tomar2020mirror-056
- All algorithms were evaluated on Hopper-v2, Walker2d-v2, HalfCheetah-v2, Ant-v2, Humanoid-v2 and HumanoidStandup-v2 across 5 random seeds. (Tomar et al., 2020) `ev:reported` p. 12 ^tomar2020mirror-057
- All off-policy experiments use an entropy coefficient of λ = 0.2 across all tasks, following the SAC paper. (Tomar et al., 2020) `ev:reported` p. 12 ^tomar2020mirror-058
- For the off-policy experiments, MDPO uses a fixed Bregman stepsize rather than the annealed schedule of the on-policy case. (Tomar et al., 2020) `ev:reported` p. 12 ^tomar2020mirror-059
- The code-level optimizations are value function clipping, reward normalization, observation normalization, orthogonal weight initialization and an annealed learning rate. (Tomar et al., 2020) `ev:reported` p. 12 ^tomar2020mirror-060
- Off-policy MDPO uses separate Q and V functions, two Q functions against overestimation bias, and soft target value updates. (Tomar et al., 2020) `ev:reported` p. 12 ^tomar2020mirror-061
- The on-policy methods use a horizon of 2048, a discount factor of 0.99 and an entropy coefficient of 0.0. (Tomar et al., 2020) `ev:reported` p. 13 ^tomar2020mirror-062
- The loaded off-policy versions use 256 hidden units per layer with minibatch size 256, against 64 in the minimal versions. (Tomar et al., 2020) `ev:reported` p. 13 ^tomar2020mirror-063
- Without code-level optimizations, MDPO-M scored 2948 (±298) on Walker2d-v2, against 2454 (±171) for TRPO-M and 424 (±92) for PPO-M. (Tomar et al., 2020) `ev:measured` p. 15 ^tomar2020mirror-064
- Without code-level optimizations, TRPO-M scored 2382 (±445) on Hopper-v2, above the 1964 (±217) reached by MDPO-M. (Tomar et al., 2020) `ev:measured` p. 15 ^tomar2020mirror-065
- Minimal MDPO-Tsallis scored 2348 (±338) on Ant-v2 with q = 2.0, against 378 (±33) for the minimal SAC. (Tomar et al., 2020) `ev:measured` p. 18 ^tomar2020mirror-066
- Although the performance of all methods overlaps, loaded MDPO achieves a higher mean score than SAC in 5 out 6 domains. (Tomar et al., 2020) `ev:measured` p. 19 ^tomar2020mirror-067
- Doing multiple gradient updates per iteration improved the Hopper-v2 score of both off-policy MDPO and SAC, as expected. (Tomar et al., 2020) `ev:measured` p. 20 ^tomar2020mirror-068
- Using the same Tsallis q for the Bregman divergence and the MDP regularizer gave the best performance in all three tested domains. (Tomar et al., 2020) `ev:measured` p. 20 ^tomar2020mirror-069

## 🎯 Contributions

## 📖 Glossary

- **Mirror descent** — First-order method minimizing a linearized objective plus a Bregman proximity term.
- **Bregman divergence** — Distance induced by a strongly convex potential; KL for negative Shannon entropy.
- **Trust-region policy optimization** — Policy updates constrained to stay close to the previous policy.
- **Tsallis entropy** — Entropy family parameterized by q; Shannon at q = 1, sparse at q = 2.
- **Code-level optimizations** — Implementation tricks such as normalization, clipping and learning-rate annealing in baseline code-bases.
- **GAE** — Generalized advantage estimation, a variance-reducing advantage estimator.
- **FTRL** — Follow-the-regularized-leader, an online learning algorithm equivalent to mirror descent in some settings.
- **Reparameterization trick** — Writing sampled actions as a deterministic function of policy parameters and noise.

## ❓ Open questions

- How does the KL direction (reverse vs forward) affect MDPO performance, given the discrepancy with Mei et al. (ECPO vs PMD)?
- Does a Tsallis-based Bregman divergence help on-policy MDPO, which was not tested because the closed form is cumbersome?
- How does MDPO perform on discrete action problems compared with DQN and PPO?
- Why does tuning q help MDPO-Tsallis but not SAC-Tsallis?
- Can exploration be incorporated into MDPO updates, and does it help in complex environments?
- Does full multi-step off-policy MDPO scale beyond Hopper-v2 given its wall-clock cost?

## 📝 Notes on reading

Version read: arXiv v5 (7 Jun 2021), matching the packet identifier 2005.09814.

Inconsistencies inside the paper: Section 5.3 says on-policy MDPO performs better than or on par with TRPO across all tasks, but Table 1 shows TRPO at 4414 (± 132) vs MDPO at 3234 (± 566) on Humanoid-v2, with non-overlapping intervals. Section 5.4 says MDPO-Tsallis can outperform SAC across all tasks, but on HalfCheetah-v2 the loaded SAC mean (11928) is above MDPO-Tsallis (11823). Section 4.1 says on-policy MDPO performs significantly better than PPO while Section 5.3 claims this across all tasks; Table 1 supports it. Appendix F.3 refers to SAC-Tsallis preliminary experiments in Table 8, but Table 8 contains no SAC-Tsallis rows; Figure 8 holds them.

The cached extraction garbles several equations (convergence rates of Shani et al., the MD closed form, the off-policy losses) and the check marks in Table 2 and Table 3; the total timesteps and replay buffer size appear as 107 and 106 (likely 10^7 and 10^6) and were not claimed. Table 1 merges the on-policy and off-policy blocks; the off-policy block rows follow the same domain order as Table 8. Figures 1-8 (learning curves) could only be described from captions.

## Suggested new concepts

- Mirror descent in reinforcement learning — unifying lens connecting TRPO, PPO, SAC and MDPO as trust-region updates.
- Code-level optimizations in policy gradient methods — recurring confound when comparing PPO and TRPO baselines.
- Tsallis entropy regularization — generalizes Shannon-entropy regularization with a tunable q, used here as a Bregman divergence.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H4.** Formula el RL de políticas como descenso espejo con KL como divergencia de Bregman y unifica TRPO y PPO en ese marco.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
