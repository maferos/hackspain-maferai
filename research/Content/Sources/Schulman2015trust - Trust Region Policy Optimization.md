---
aliases: []
type: "source"
title: "Trust Region Policy Optimization"
citekey: "Schulman2015trust"
doi: "10.48550/arXiv.1502.05477"
arxiv: "1502.05477"
year: 2015
publication_type: "preprint"
url: "https://arxiv.org/abs/1502.05477"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["John Schulman", "Sergey Levine", "Philipp Moritz", "Michael I. Jordan", "Pieter Abbeel"]
sha256: ["c228ad36d9d46972b898c96d58b5929c51b54cc43fd42f01d751b36f434bfa4a"]
pdf: "Content/Papers/Schulman2015trust.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Schulman2015trust.pdf]]

> [!abstract] One-sentence summary
> The paper derives a monotonic policy improvement bound for general stochastic policies and approximates it as TRPO, a KL-constrained policy update that learns locomotion gaits and Atari policies with neural networks.

## Abstract

We describe an iterative procedure for optimizing policies, with guaranteed monotonic improvement. By making several approximations to the theoretically-justified procedure, we develop a practical algorithm, called Trust Region Policy Optimization (TRPO). This algorithm is similar to natural policy gradient methods and is effective for optimizing large nonlinear policies such as neural networks. Our experiments demonstrate its robust performance on a wide variety of tasks: learning simulated robotic swimming, hopping, and walking gaits; and playing Atari games using images of the screen as input. Despite its approximations that deviate from the theory, TRPO tends to give monotonic improvement, with little tuning of hyperparameters. (arXiv)

## 🧠 Key ideas (atomic)

- Most policy optimization algorithms fall into three categories: policy iteration methods, policy gradient methods, and derivative-free optimization methods such as CEM or CMA. (Schulman et al., 2015) `ev:cited` p. 1 ^schulman2015trust-001
- A series of approximations to the theoretically-justified algorithm yields a practical algorithm that the authors call [[Trust region policy optimization|trust region policy optimization]] (TRPO). (Schulman et al., 2015) `ev:reported` p. 1 ^schulman2015trust-002
- The single-path variant of TRPO, one of the two variants described, can be applied in the model-free setting. (Schulman et al., 2015) `ev:asserted` p. 1 ^schulman2015trust-003
- The vine variant requires the system to be restored to particular states, which is typically only possible in simulation. (Schulman et al., 2015) `ev:asserted` p. 1 ^schulman2015trust-004
- An identity from Kakade and Langford expresses the expected return of a new policy through its accumulated advantage over the old policy. (Schulman et al., 2015) `ev:cited` p. 2 ^schulman2015trust-005
- Any policy update with nonnegative expected advantage at every state is guaranteed to increase policy performance or leave it constant. (Schulman et al., 2015) `ev:computed` p. 2 ^schulman2015trust-006
- In the approximate setting, estimation and approximation error will typically leave some states with a negative expected advantage. (Schulman et al., 2015) `ev:asserted` p. 2 ^schulman2015trust-007
- The local approximation L uses the old policy's visitation frequency, ignoring changes in state visitation density caused by the policy change. (Schulman et al., 2015) `ev:reported` p. 2 ^schulman2015trust-008
- For a differentiable parameterized policy, the local approximation L matches the true expected discounted reward to first order. (Schulman et al., 2015) `ev:cited` p. 2 ^schulman2015trust-009
- Conservative policy iteration by Kakade and Langford gives explicit lower bounds on improvement, but the bound applies only to mixture policies. (Schulman et al., 2015) `ev:cited` p. 2 ^schulman2015trust-010
- The principal theoretical result extends the policy improvement bound to general stochastic policies by replacing the mixture coefficient with a distance measure. (Schulman et al., 2015) `ev:computed` p. 3 ^schulman2015trust-011
- The distance measure in Theorem 1 is the total variation divergence between old and new policies, maximized over all states. (Schulman et al., 2015) `ev:reported` p. 3 ^schulman2015trust-012
- Theorem 1 lower-bounds new-policy performance by the surrogate objective minus a penalty proportional to the squared maximum total variation divergence. (Schulman et al., 2015) `ev:computed` p. 3 ^schulman2015trust-013
- Through the relation between total variation and KL divergence, the improvement bound also holds with a penalty on the maximum KL divergence. (Schulman et al., 2015) `ev:computed` p. 3 ^schulman2015trust-014
- The paper provides two proofs of Theorem 1, one based on coupling random variables and one based on perturbation theory. (Schulman et al., 2015) `ev:reported` p. 3 ^schulman2015trust-015
- Algorithm 1, which maximizes the KL-penalized surrogate at each iteration, is guaranteed to generate a monotonically improving sequence of policies. (Schulman et al., 2015) `ev:computed` p. 3 ^schulman2015trust-016
- The monotonic improvement guarantee of Algorithm 1 assumes, for now, exact evaluation of the advantage values under the current policy. (Schulman et al., 2015) `ev:reported` p. 3 ^schulman2015trust-017
- In practice, using the penalty coefficient C recommended by the theory would make the policy step sizes very small. (Schulman et al., 2015) `ev:asserted` p. 3 ^schulman2015trust-018
- To take larger steps robustly, [[Trust region policy optimization|TRPO]] replaces the KL penalty with a trust region constraint on the KL divergence between policies. (Schulman et al., 2015) `ev:reported` p. 3 ^schulman2015trust-019
- The constraint bounding KL divergence at every point in the state space is impractical to solve due to the many constraints. (Schulman et al., 2015) `ev:asserted` p. 4 ^schulman2015trust-020
- [[Trust region policy optimization|TRPO]] instead uses a heuristic approximation that constrains the average KL divergence over states sampled from the old policy. (Schulman et al., 2015) `ev:reported` p. 4 ^schulman2015trust-021
- The single path scheme samples trajectories from the old policy and estimates each Q-value as the discounted sum of future rewards. (Schulman et al., 2015) `ev:reported` p. 4 ^schulman2015trust-022
- The vine scheme selects a rollout set of states along trajectories and performs several actions with short rollouts from each state. (Schulman et al., 2015) `ev:reported` p. 4 ^schulman2015trust-023
- The authors found that sampling vine actions from the current policy works well on continuous problems such as robotic locomotion. (Schulman et al., 2015) `ev:asserted` p. 4 ^schulman2015trust-024
- A uniform action distribution works well for vine sampling on discrete tasks such as Atari, where it can sometimes achieve better exploration. (Schulman et al., 2015) `ev:asserted` p. 4 ^schulman2015trust-025
- Using the same random number sequence across the K rollouts from a state can greatly reduce the variance of Q-value differences. (Schulman et al., 2015) `ev:asserted` p. 5 ^schulman2015trust-026
- Given the same number of Q-value samples, the vine method yields a much lower variance local estimate of the objective than single path. (Schulman et al., 2015) `ev:asserted` p. 5 ^schulman2015trust-027
- The downside of the vine method is that it must perform far more calls to the simulator for each advantage estimate. (Schulman et al., 2015) `ev:asserted` p. 5 ^schulman2015trust-028
- The vine method is limited to settings where the system can be reset to an arbitrary state in the rollout set. (Schulman et al., 2015) `ev:asserted` p. 5 ^schulman2015trust-029
- The single path algorithm requires no state resets and can be directly implemented on a physical system, according to the authors. (Schulman et al., 2015) `ev:asserted` p. 5 ^schulman2015trust-030
- Each [[Trust region policy optimization|TRPO]] update approximately solves the constrained optimization problem with the conjugate gradient algorithm followed by a line search. (Schulman et al., 2015) `ev:reported` p. 5 ^schulman2015trust-031
- [[Trust region policy optimization|TRPO]] estimates the [[Fisher information matrix]] analytically from the Hessian of the KL divergence rather than from the covariance of gradients. (Schulman et al., 2015) `ev:reported` p. 5 ^schulman2015trust-032
- The theory ignores estimation error in the advantage function, although the authors state that Kakade and Langford's arguments would still hold. (Schulman et al., 2015) `ev:asserted` p. 5 ^schulman2015trust-033
- The [[Natural policy gradient|natural policy gradient]] is obtained as a special case of the TRPO update using a linear objective approximation with a quadratic constraint approximation. (Schulman et al., 2015) `ev:computed` p. 6 ^schulman2015trust-034
- [[Natural policy gradient]] treats the step size as an algorithm parameter, whereas TRPO enforces the KL divergence constraint at each update. (Schulman et al., 2015) `ev:asserted` p. 6 ^schulman2015trust-035
- Relative entropy policy search constrains the state-action marginals, whereas TRPO constrains the conditional action distributions given each state. (Schulman et al., 2015) `ev:reported` p. 6 ^schulman2015trust-036
- The robotic locomotion experiments used the MuJoCo simulator with three simulated planar robots: a swimmer, a hopper, and a walker. (Schulman et al., 2015) `ev:reported` p. 6 ^schulman2015trust-037
- The swimmer has a 10-dimensional state space with a linear reward for forward progress minus a quadratic penalty on joint effort. (Schulman et al., 2015) `ev:reported` p. 7 ^schulman2015trust-038
- The hopper task has a 12-dimensional state space and adds a bonus of +1 to the swimmer reward for non-terminal states. (Schulman et al., 2015) `ev:reported` p. 7 ^schulman2015trust-039
- The walker task has an 18-dimensional state space with a penalty for strong foot impacts to encourage a smooth walk. (Schulman et al., 2015) `ev:reported` p. 7 ^schulman2015trust-040
- All locomotion experiments used a KL divergence bound of δ = 0.01 as the trust region step size parameter. (Schulman et al., 2015) `ev:reported` p. 7 ^schulman2015trust-041
- The compared algorithms were single path TRPO, vine TRPO, CEM, CMA, natural gradient, empirical FIM, and max KL. (Schulman et al., 2015) `ev:reported` p. 7 ^schulman2015trust-042
- The max KL variant, which uses the maximum rather than average KL divergence, was only tractable on the cart-pole problem. (Schulman et al., 2015) `ev:reported` p. 7 ^schulman2015trust-043
- Locomotion learning curves report total reward averaged across five runs of each algorithm, each with random policy initializations. (Schulman et al., 2015) `ev:reported` p. 7 ^schulman2015trust-044
- Single path and vine [[Trust region policy optimization|TRPO]] solved all of the locomotion problems, yielding the best solutions among the compared algorithms. (Schulman et al., 2015) `ev:measured` p. 7 ^schulman2015trust-045
- Natural gradient performed well on the two easier problems but was unable to generate hopping or walking gaits that made forward progress. (Schulman et al., 2015) `ev:measured` p. 7 ^schulman2015trust-046
- The authors take these results as evidence that constraining KL divergence chooses step sizes more robustly than using a fixed penalty. (Schulman et al., 2015) `ev:asserted` p. 7 ^schulman2015trust-047
- The derivative-free CEM and CMA methods performed poorly on the larger problems, as their sample complexity scales unfavorably with parameter count. (Schulman et al., 2015) `ev:measured` p. 7 ^schulman2015trust-048
- The max KL method learned somewhat more slowly than the final TRPO method, due to the more restrictive form of its constraint. (Schulman et al., 2015) `ev:measured` p. 7 ^schulman2015trust-049
- The cart-pole results suggest that the average KL divergence constraint has a similar effect to the theoretically justified maximum KL constraint. (Schulman et al., 2015) `ev:measured` p. 7 ^schulman2015trust-050
- TRPO learned all of the gaits with general-purpose policies and simple reward functions, using minimal prior knowledge. (Schulman et al., 2015) `ev:asserted` p. 7 ^schulman2015trust-051
- Most prior methods for learning locomotion typically rely on hand-architected policy classes that explicitly encode notions of balance and stepping. (Schulman et al., 2015) `ev:cited` p. 7 ^schulman2015trust-052
- TRPO was tested on the same seven Atari games used by Mnih et al. and Guo et al., with raw images as input. (Schulman et al., 2015) `ev:reported` p. 7 ^schulman2015trust-053
- The Atari policy network had two convolutional layers with 16 channels and stride 2, followed by one fully-connected layer with 20 units. (Schulman et al., 2015) `ev:reported` p. 8 ^schulman2015trust-054
- The convolutional policy network used for the Atari games had 33,500 parameters in total across all of its layers. (Schulman et al., 2015) `ev:reported` p. 8 ^schulman2015trust-055
- The 500 iterations of TRPO on Atari took about 30 hours on a 16-core computer, with slight variation between games. (Schulman et al., 2015) `ev:reported` p. 8 ^schulman2015trust-056
- On Q*bert, TRPO vine scored 7732.5, above deep Q-learning at 1952 but below UCC-I at 20025. (Schulman et al., 2015) `ev:measured` p. 8 ^schulman2015trust-057
- On Breakout, TRPO vine scored 34.2, far below deep Q-learning at 168.0 and UCC-I at 380. (Schulman et al., 2015) `ev:measured` p. 8 ^schulman2015trust-058
- On Pong, both TRPO variants scored 20.9, slightly above deep Q-learning at 20.0 and close to UCC-I at 21. (Schulman et al., 2015) `ev:measured` p. 8 ^schulman2015trust-059
- TRPO outperformed the prior methods on only some of the Atari games but consistently achieved reasonable scores across them. (Schulman et al., 2015) `ev:measured` p. 8 ^schulman2015trust-060
- Each TRPO variant was run once per Atari game, and error statistics could not be obtained due to time constraints. (Schulman et al., 2015) `ev:reported` p. 8 ^schulman2015trust-061
- The authors argue that applying the same method to locomotion and image-based game playing demonstrates the generality of TRPO. (Schulman et al., 2015) `ev:asserted` p. 8 ^schulman2015trust-062
- The analysis presents policy gradient and policy iteration methods as special limiting cases of optimizing an objective under a trust region constraint. (Schulman et al., 2015) `ev:asserted` p. 8 ^schulman2015trust-063
- The authors suggest that combining TRPO with model learning could substantially reduce its sample complexity for real-world settings with expensive samples. (Schulman et al., 2015) `ev:asserted` p. 8 ^schulman2015trust-064
- Without the line search, the algorithm occasionally computes large steps that cause a catastrophic degradation of policy performance. (Schulman et al., 2015) `ev:asserted` p. 14 ^schulman2015trust-065
- The authors found k = 10 conjugate gradient iterations quite effective, and higher k did not result in faster policy improvement. (Schulman et al., 2015) `ev:measured` p. 15 ^schulman2015trust-066
- Computing the Fisher-vector product on 10% of the data makes the Hessian-vector product cost about the same as computing the gradient. (Schulman et al., 2015) `ev:asserted` p. 15 ^schulman2015trust-067
- Continuous-control policies were Gaussian, with a neural network computing the mean and a state-independent diagonal covariance with separate log standard deviations. (Schulman et al., 2015) `ev:reported` p. 15 ^schulman2015trust-068
- The locomotion policies had 364 parameters for the swimmer, 4806 for the hopper, and 8206 for the walker. (Schulman et al., 2015) `ev:reported` p. 15 ^schulman2015trust-069

## 🎯 Contributions

## 📖 Glossary

- **Trust region** — A bound on how far each update may move the policy, here in KL divergence.
- **Surrogate objective** — Local approximation of expected return using the old policy's state visitation frequencies.
- **Total variation divergence** — Half the L1 distance between two discrete probability distributions.
- **Single path** — Estimation scheme sampling whole trajectories from the current policy; needs no state resets.
- **Vine** — Estimation scheme branching several short rollouts from a rollout set of states.
- **Common random numbers** — Reusing one noise sequence across rollouts to reduce variance of their differences.
- **Fisher-vector product** — Product of the KL Hessian with a vector, computed without forming the matrix.
- **Minorization-maximization** — Iteratively maximizing a surrogate lower bound that touches the objective at the current point.

## ❓ Open questions

- How much does the gap between the average KL constraint and the theoretically justified maximum KL constraint matter on large problems where max KL is intractable?
- How do the Atari results vary across random seeds, given only one run per game was reported?
- Can the guarantee be extended to account for advantage estimation error in the sample-based setting?
- Can TRPO learn vision-based robotic controllers that combine perception and control, as the authors propose?
- Would recurrent policies with TRPO handle partially observed settings by merging state estimation and control?
- How much could combining TRPO with learned dynamics models reduce its sample complexity on real systems?

## 📝 Notes on reading

Version read: the cached text is arXiv 1502.05477v5 (20 Apr 2017), which carries the ICML 2015 proceedings header.

Inconsistency: the walker is described as having an 18-dimensional state space in the text (p. 7), but Table 2 (p. 15) lists the walker state space dimension as 20.

Table 2 lists single path (SP) computation times of 5, 35 and 100 without a unit; the vine row gives minutes (2, 14, 40), so the SP unit is presumably minutes but it is not stated.

Figure 4 (p. 7) learning curves for cart-pole, swimmer, hopper and walker and Figure 5 (p. 16) Atari learning curves were described only from axis ticks and legends; no values were claimed from them. Figure 5 plots cost (negative reward).

Table 1 (p. 8) also reports Random and Human baselines and the other single path and vine scores per game; only headline comparisons were claimed.

## Suggested new concepts

- Trust region policy optimization — foundational KL-constrained policy gradient algorithm that later methods such as PPO build on.
- Monotonic policy improvement bound — theoretical lower bound linking surrogate objective and divergence penalty to true performance.
- Natural policy gradient — related method that TRPO generalizes by enforcing a hard KL constraint.
- Conservative policy iteration — Kakade and Langford's mixture-policy scheme that TRPO's theory extends.
- Vine sampling — rollout-set estimator with common random numbers, useful where simulator resets are possible.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Gradiente natural con restricción KL y CG (B.5, F.7).
