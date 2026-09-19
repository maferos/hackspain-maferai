---
aliases: []
type: "source"
title: "Overcoming catastrophic forgetting in neural networks"
citekey: "Kirkpatrick2016overcoming"
doi: "10.48550/arXiv.1612.00796"
arxiv: "1612.00796"
year: 2016
publication_type: "preprint"
url: "https://arxiv.org/abs/1612.00796"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["James Kirkpatrick", "Razvan Pascanu", "Neil Rabinowitz", "Joel Veness", "Guillaume Desjardins", "Andrei A. Rusu", "Kieran Milan", "John Quan", "Tiago Ramalho", "Agnieszka Grabska-Barwinska", "Demis Hassabis", "Claudia Clopath", "Dharshan Kumaran", "Raia Hadsell"]
sha256: ["5e181839191ab4582da2b5ff9666f5222e40b8b8d2f1cdf4fa7100b3a58d7a29"]
pdf: "Content/Papers/Kirkpatrick2016overcoming.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Kirkpatrick2016overcoming.pdf]]

> [!abstract] One-sentence summary
> The paper introduces elastic weight consolidation (EWC), a Fisher-weighted quadratic penalty that slows learning on weights important to earlier tasks, letting one fixed-capacity network learn permuted MNIST tasks and Atari games sequentially without catastrophic forgetting.

## Abstract

The ability to learn tasks in a sequential fashion is crucial to the development of artificial intelligence. Neural networks are not, in general, capable of this and it has been widely thought that catastrophic forgetting is an inevitable feature of connectionist models. We show that it is possible to overcome this limitation and train networks that can maintain expertise on tasks which they have not experienced for a long time. Our approach remembers old tasks by selectively slowing down learning on the weights important for those tasks. We demonstrate our approach is scalable and effective by solving a set of classification tasks based on the MNIST hand written digit dataset and by learning several Atari 2600 games sequentially. (arXiv)

## 🧠 Key ideas (atomic)

- Continual learning is defined as the ability to learn consecutive tasks without forgetting how to perform previously trained tasks. (Kirkpatrick et al., 2016) `ev:asserted` p. 1 ^kirkpatrick2016overcoming-001
- Catastrophic forgetting occurs when a network trained sequentially changes the weights important for task A to meet the objectives of task B. (Kirkpatrick et al., 2016) `ev:cited` p. 1 ^kirkpatrick2016overcoming-002
- Replaying stored episodic memories for multitask learning is impractical for large numbers of tasks, as stored memories would grow with task count. (Kirkpatrick et al., 2016) `ev:asserted` p. 1 ^kirkpatrick2016overcoming-003
- Enlarged dendritic spines formed when a mouse acquires a new skill persist despite later learning of other tasks, according to cited work. (Kirkpatrick et al., 2016) `ev:cited` p. 2 ^kirkpatrick2016overcoming-004
- Cited experiments report that selectively erasing the enlarged dendritic spines causes the corresponding learned skill to be forgotten. (Kirkpatrick et al., 2016) `ev:cited` p. 2 ^kirkpatrick2016overcoming-005
- [[Elastic weight consolidation]] slows down learning on certain weights based on how important they are to previously seen tasks. (Kirkpatrick et al., 2016) `ev:asserted` p. 2 ^kirkpatrick2016overcoming-006
- The authors argue that over-parameterization makes it likely that a solution for task B lies close to the solution for task A. (Kirkpatrick et al., 2016) `ev:asserted` p. 2 ^kirkpatrick2016overcoming-007
- [[Elastic weight consolidation|EWC]] implements its constraint as a quadratic penalty, imagined as a spring anchoring parameters to the previous task's solution. (Kirkpatrick et al., 2016) `ev:asserted` p. 2 ^kirkpatrick2016overcoming-008
- The stiffness of [[Elastic weight consolidation|the EWC spring]] should be greater for parameters that matter most to performance on the previous task. (Kirkpatrick et al., 2016) `ev:asserted` p. 2 ^kirkpatrick2016overcoming-009
- From a probabilistic view, all information about task A must have been absorbed into the posterior over parameters given task A data. (Kirkpatrick et al., 2016) `ev:computed` p. 3 ^kirkpatrick2016overcoming-010
- The intractable posterior is approximated as a Gaussian with mean at the task A parameters and diagonal Fisher information precision. (Kirkpatrick et al., 2016) `ev:reported` p. 3 ^kirkpatrick2016overcoming-011
- The Fisher information matrix can be computed from first-order derivatives alone, making it easy to calculate even for large models. (Kirkpatrick et al., 2016) `ev:cited` p. 3 ^kirkpatrick2016overcoming-012
- Near a minimum, the Fisher information matrix is equivalent to the second derivative of the loss, according to the cited work. (Kirkpatrick et al., 2016) `ev:cited` p. 3 ^kirkpatrick2016overcoming-013
- In the EWC loss, a hyperparameter lambda sets how important the old task is compared to the new one. (Kirkpatrick et al., 2016) `ev:reported` p. 3 ^kirkpatrick2016overcoming-014
- For a third task, [[Elastic weight consolidation|EWC]] keeps parameters close to both previous solutions, via two penalties or one combined quadratic penalty. (Kirkpatrick et al., 2016) `ev:asserted` p. 3 ^kirkpatrick2016overcoming-015
- The supervised tasks were MNIST digit classification problems, each using a fixed random permutation of the input pixels. (Kirkpatrick et al., 2016) `ev:reported` p. 3 ^kirkpatrick2016overcoming-016
- A fully connected multilayer network was trained on each task for a fixed amount, after which no further training on that dataset was allowed. (Kirkpatrick et al., 2016) `ev:reported` p. 3 ^kirkpatrick2016overcoming-017
- Training on the permuted MNIST sequence with plain stochastic gradient descent incurs catastrophic forgetting of earlier tasks. (Kirkpatrick et al., 2016) `ev:measured` p. 3 ^kirkpatrick2016overcoming-018
- Under a fixed L2 quadratic constraint on each weight, performance on task A degrades much less severely than under plain SGD. (Kirkpatrick et al., 2016) `ev:measured` p. 4 ^kirkpatrick2016overcoming-019
- With a fixed L2 constraint on each weight, task B cannot be learned properly, as the constraint protects all weights equally. (Kirkpatrick et al., 2016) `ev:measured` p. 4 ^kirkpatrick2016overcoming-020
- With [[Elastic weight consolidation|EWC]], the network can learn task B well without forgetting task A in the permuted MNIST experiment. (Kirkpatrick et al., 2016) `ev:measured` p. 4 ^kirkpatrick2016overcoming-021
- Previous methods for deep networks achieved reasonable results on only up to two random MNIST permutations, according to cited work. (Kirkpatrick et al., 2016) `ev:cited` p. 4 ^kirkpatrick2016overcoming-022
- Stochastic gradient descent with dropout regularization alone does not scale to more tasks in the permuted MNIST sequence. (Kirkpatrick et al., 2016) `ev:measured` p. 4 ^kirkpatrick2016overcoming-023
- [[Elastic weight consolidation|EWC]] allows a large number of permuted MNIST tasks to be learned in sequence, with only modest growth in error rates. (Kirkpatrick et al., 2016) `ev:measured` p. 4 ^kirkpatrick2016overcoming-024
- Weight sharing between tasks was assessed by measuring the overlap between pairs of tasks' Fisher information matrices across network depth. (Kirkpatrick et al., 2016) `ev:reported` p. 4 ^kirkpatrick2016overcoming-025
- The overlap experiment permuted either a small 8x8 pixel square or a large 26x26 pixel square in the middle of the image. (Kirkpatrick et al., 2016) `ev:reported` p. 4 ^kirkpatrick2016overcoming-026
- For two very similar MNIST tasks, the tasks depend on similar sets of weights throughout the whole network. (Kirkpatrick et al., 2016) `ev:measured` p. 4 ^kirkpatrick2016overcoming-027
- When permuted tasks are more dissimilar, the network begins to allocate separate capacity, meaning separate weights, for the two tasks. (Kirkpatrick et al., 2016) `ev:measured` p. 4 ^kirkpatrick2016overcoming-028
- Even for large permutations, the layers of the network closer to the output are reused for both tasks. (Kirkpatrick et al., 2016) `ev:measured` p. 4 ^kirkpatrick2016overcoming-029
- Each Atari experiment consisted of ten games chosen randomly from those that DQN plays at human level or above. (Kirkpatrick et al., 2016) `ev:reported` p. 5 ^kirkpatrick2016overcoming-030
- The order of game presentation was randomized and allowed the agent to return to the same games several times. (Kirkpatrick et al., 2016) `ev:reported` p. 5 ^kirkpatrick2016overcoming-031
- The authors state that [[Elastic weight consolidation|the EWC approach]] uses a single network with fixed capacity and has minimal computational overhead. (Kirkpatrick et al., 2016) `ev:asserted` p. 5 ^kirkpatrick2016overcoming-032
- Task context is treated as the latent variable of a Hidden Markov Model, with a generative model of observations per task. (Kirkpatrick et al., 2016) `ev:reported` p. 5 ^kirkpatrick2016overcoming-033
- New generative models are added when they explain recent data better than the existing pool, inspired by the forget me not process. (Kirkpatrick et al., 2016) `ev:reported` p. 5 ^kirkpatrick2016overcoming-034
- In the Atari agent, the Fisher information matrix is computed at each task switch to form a new EWC penalty. (Kirkpatrick et al., 2016) `ev:reported` p. 5 ^kirkpatrick2016overcoming-035
- An EWC penalty was only added to games which had experienced at least 20 million frames of training. (Kirkpatrick et al., 2016) `ev:reported` p. 5 ^kirkpatrick2016overcoming-036
- The DQN agents kept separate short-term replay buffers for each inferred task, allowing off-policy learning of action values. (Kirkpatrick et al., 2016) `ev:reported` p. 5 ^kirkpatrick2016overcoming-037
- Each network layer had biases and per element multiplicative gains specific to each game, rather than shared across games. (Kirkpatrick et al., 2016) `ev:reported` p. 5 ^kirkpatrick2016overcoming-038
- Performance was the total human-normalized score across ten games, each game clipped to 1, giving a maximum of 10. (Kirkpatrick et al., 2016) `ev:reported` p. 5 ^kirkpatrick2016overcoming-039
- With plain gradient descent as in DQN, the agent never learns to play more than one game in the sequence. (Kirkpatrick et al., 2016) `ev:measured` p. 5 ^kirkpatrick2016overcoming-040
- With plain gradient descent, forgetting of old games keeps the total human-normalized score across ten games below one. (Kirkpatrick et al., 2016) `ev:measured` p. 5 ^kirkpatrick2016overcoming-041
- By using [[Elastic weight consolidation|EWC]], the Atari agents do learn to play multiple games within the sequential training schedule. (Kirkpatrick et al., 2016) `ev:measured` p. 5 ^kirkpatrick2016overcoming-042
- Providing the agent with the true task label instead of learned task recognition improved Atari performance only modestly. (Kirkpatrick et al., 2016) `ev:measured` p. 5 ^kirkpatrick2016overcoming-043
- The EWC agent does not reach the score that would have been obtained by training ten separate DQNs. (Kirkpatrick et al., 2016) `ev:measured` p. 6 ^kirkpatrick2016overcoming-044
- The authors suggest one possible reason is that consolidation relies on the Fisher information, a tractable approximation of parameter uncertainty. (Kirkpatrick et al., 2016) `ev:asserted` p. 6 ^kirkpatrick2016overcoming-045
- A single-game DQN was more robust to perturbations shaped by the inverse diagonal Fisher than to uniform weight perturbations. (Kirkpatrick et al., 2016) `ev:measured` p. 6 ^kirkpatrick2016overcoming-046
- Perturbing in the Fisher nullspace had the same effect as perturbing in the inverse Fisher space, though the approximation predicts no effect. (Kirkpatrick et al., 2016) `ev:measured` p. 6 ^kirkpatrick2016overcoming-047
- The authors conclude that the chief limitation is likely that the current implementation under-estimates parameter uncertainty. (Kirkpatrick et al., 2016) `ev:asserted` p. 6 ^kirkpatrick2016overcoming-048
- Perturbation scores were evaluated by running the agent for ten full game episodes, drawing a new perturbation every timestep. (Kirkpatrick et al., 2016) `ev:reported` p. 6 ^kirkpatrick2016overcoming-049
- This Bayesian view enables fast learning rates on parameters poorly constrained by previous tasks, with slow rates for crucial ones. (Kirkpatrick et al., 2016) `ev:asserted` p. 6 ^kirkpatrick2016overcoming-050
- To the extent that tasks share structure, networks trained with EWC reuse shared components of the network. (Kirkpatrick et al., 2016) `ev:asserted` p. 6 ^kirkpatrick2016overcoming-051
- Earlier work using a quadratic penalty to approximate old parts of the dataset has been limited to small models. (Kirkpatrick et al., 2016) `ev:cited` p. 7 ^kirkpatrick2016overcoming-052
- The cited ELLA algorithm inverts matrices sized by the number of parameters, so it was mainly applied to linear and logistic regressions. (Kirkpatrick et al., 2016) `ev:cited` p. 7 ^kirkpatrick2016overcoming-053
- [[Elastic weight consolidation|EWC]] has a run time which is linear in both the number of parameters and the number of training examples. (Kirkpatrick et al., 2016) `ev:asserted` p. 7 ^kirkpatrick2016overcoming-054
- The authors call the point estimate of the posterior's variance, as in a Laplace approximation, a significant weakness of [[Elastic weight consolidation|EWC]]. (Kirkpatrick et al., 2016) `ev:asserted` p. 7 ^kirkpatrick2016overcoming-055
- Initial explorations suggest that the local variance estimate might be improved by using Bayesian neural networks. (Kirkpatrick et al., 2016) `ev:asserted` p. 7 ^kirkpatrick2016overcoming-056
- With EWC, three values have to be stored for each synapse: the weight itself, its variance and its mean. (Kirkpatrick et al., 2016) `ev:asserted` p. 7 ^kirkpatrick2016overcoming-057
- The authors claim their work demonstrates that current neurobiological theories of synaptic consolidation scale to large-scale learning systems. (Kirkpatrick et al., 2016) `ev:asserted` p. 7 ^kirkpatrick2016overcoming-058
- In the MNIST experiments, dropout was applied with probability 0.2 to the input and 0.5 to the other hidden layers. (Kirkpatrick et al., 2016) `ev:reported` p. 10 ^kirkpatrick2016overcoming-059
- Early stopping for SGD with dropout ended a training segment when validation error increased for more than five subsequent steps. (Kirkpatrick et al., 2016) `ev:reported` p. 10 ^kirkpatrick2016overcoming-060
- Random hyperparameter search attempted 50 combinations of parameters for each MNIST experiment, reporting the best setting. (Kirkpatrick et al., 2016) `ev:reported` p. 10 ^kirkpatrick2016overcoming-061
- The Atari network had approximately four times as many parameters as the standard DQN network, with 1024 fully connected units. (Kirkpatrick et al., 2016) `ev:reported` p. 10 ^kirkpatrick2016overcoming-062
- In the Atari experiments, the EWC penalty used a scaling factor of 400 applied to the Fisher information. (Kirkpatrick et al., 2016) `ev:reported` p. 11 ^kirkpatrick2016overcoming-063
- The games were drawn from a pool of 19 Atari games where standalone DQN reached human-level performance. (Kirkpatrick et al., 2016) `ev:reported` p. 11 ^kirkpatrick2016overcoming-064
- Averaged Atari performance used 10 sets of 10 games, with 4 different random seeds run for each set. (Kirkpatrick et al., 2016) `ev:reported` p. 11 ^kirkpatrick2016overcoming-065
- The task recognition generative models are factored multinomial distributions over pixel states, parametrized as Dirichlet distributions with Bayesian updates. (Kirkpatrick et al., 2016) `ev:reported` p. 11 ^kirkpatrick2016overcoming-066
- Whenever the hold-out uniform Dirichlet-multinomial model is selected, a new generative model and a new task context are created. (Kirkpatrick et al., 2016) `ev:reported` p. 11 ^kirkpatrick2016overcoming-067
- Whenever the diagonal Fisher is recomputed for a task, one hundred mini-batches are drawn from the replay buffer. (Kirkpatrick et al., 2016) `ev:reported` p. 12 ^kirkpatrick2016overcoming-068
- The Fisher overlap is defined as one minus the Fréchet distance between two trace-normalized Fisher matrices, bounded between zero and one. (Kirkpatrick et al., 2016) `ev:reported` p. 13 ^kirkpatrick2016overcoming-069

## 🎯 Contributions

## 📖 Glossary

- **Catastrophic forgetting** — abrupt loss of earlier-task knowledge when a network is trained on a new task.
- **Continual learning** — learning consecutive tasks without forgetting how to perform previously trained tasks.
- **Elastic weight consolidation (EWC)** — quadratic penalty anchoring weights to old values, weighted by their Fisher information.
- **Fisher information matrix** — curvature estimate from first-order gradients; its diagonal ranks parameter importance for a task.
- **Laplace approximation** — Gaussian approximation of a posterior around its mode using local curvature.
- **Permuted MNIST** — MNIST variants where each task applies a fixed random permutation to input pixels.
- **Synaptic consolidation** — biological reduction of plasticity in synapses vital to previously learned tasks.
- **Human-normalized score** — game score rescaled so 0 is a random agent and 1 is human level.
- **Forget Me Not process** — Bayesian non-parametric procedure that adds generative models to infer unlabelled task contexts.

## ❓ Open questions

- Can a better estimate of parameter uncertainty, e.g. from Bayesian neural networks, close the gap to ten separate DQNs?
- Why does perturbing in the Fisher nullspace hurt performance as much as perturbing along the inverse Fisher?
- How does EWC behave when the number of tasks grows beyond ten, given a fixed network capacity?
- How sensitive are the results to the EWC scaling factor (400 in Atari), and how should it be set across tasks?
- Does the Fisher overlap pattern (shared output layers, separate input layers) hold for task families other than pixel permutations?

## 📝 Notes on reading

- Version read: arXiv 1612.00796v2 (25 Jan 2017), the same arXiv record as the packet identifier; the later PNAS journal version was not read.
- Figure 1 is a schematic parameter-space diagram (plain SGD, uniform L2 and EWC trajectories); Figure 2 shows permuted-MNIST training curves, average performance vs number of tasks, and Fisher overlap vs depth; Figure 3 shows the Atari schedule, total human-normalized scores (EWC, EWC with true labels, SGD) and the Breakout perturbation test. No exact numbers are given in the text for these curves, so no numeric results were claimed from them.
- Figure 4 (p. 13, per-game scores for 19 games: EWC, SGD, single game) extracted as bare axis ticks; nothing was claimed from it.
- Internal cross-reference inconsistencies: the appendix says Table 1 is for "Figure 3 of the main text", but its columns 3A/3B/3C match the MNIST Figure 2; Table 2 is captioned "Hyperparameters for each of the MNIST figures" but lists Atari hyperparameters; the Discussion cites "Fig 4C" for the Fisher weakness, which appears to mean Figure 3C; Appendix 4.3 refers to "Figure 3C" for Fisher overlap, which is Figure 2C; "Appendix app:atari" is a broken reference.
- Text vs table inconsistencies in the Atari appendix: the text gives a replay buffer of 5 x 10^5 experiences while Table 2 gives memory size 50000; the text gives a target update every 3 x 10^4 time steps while Table 2 gives 7500 steps (possibly frames vs agent steps); the text gives epsilon = 1 for 5 x 10^4 steps then a linear decay over 10^6.
- Table 2 row "start EWC 20E6" is described as 5 million steps (20 million frames), consistent with the 20 million frames in the main text.
- The agent-modification list on p. 5 labels two items "(e)".
- The equations (EWC loss, task-specific gains, HMM task inference, Fréchet distance) are partly garbled in extraction; only their verbal descriptions were claimed.

## Suggested new concepts

- Elastic weight consolidation — a foundational regularization-based continual learning method likely cited by many later sources.
- Catastrophic forgetting — the central problem of continual learning, shared across supervised and reinforcement learning work.
- Fisher information as parameter importance — a reusable idea linking curvature estimates to which weights to protect.
- Task inference from observations — unsupervised detection of task switches, relevant whenever task labels are unavailable.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H4.** EWC: penalización cuadrática ponderada por la Fisher diagonal que ancla el fine-tuning al modelo base y evita olvidar las habilidades preentrenadas.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
