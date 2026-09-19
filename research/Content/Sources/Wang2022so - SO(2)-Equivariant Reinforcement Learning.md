---
aliases: []
type: "source"
title: "SO(2)-Equivariant Reinforcement Learning"
citekey: "Wang2022so"
doi: "10.48550/arXiv.2203.04439"
arxiv: "2203.04439"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2203.04439"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Dian Wang", "Robin Walters", "Robert Platt"]
sha256: ["b7cd56a41fc2f7e20c6ad560ecc456fc2fbf6039c693c8fdf020b60e5571a0a4"]
pdf: "Content/Papers/Wang2022so.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Wang2022so.pdf]]

> [!abstract] One-sentence summary
> The paper shows that rotation-invariant manipulation MDPs have invariant optimal Q-functions and equivariant optimal policies, and builds equivariant DQN, SAC and SACfD agents that learn such tasks far more sample-efficiently than data augmentation baselines.

## Abstract

Equivariant neural networks enforce symmetry within the structure of their convolutional layers, resulting in a substantial improvement in sample efficiency when learning an equivariant or invariant function. Such models are applicable to robotic manipulation learning which can often be formulated as a rotationally symmetric problem. This paper studies equivariant model architectures in the context of $Q$-learning and actor-critic reinforcement learning. We identify equivariant and invariant characteristics of the optimal $Q$-function and the optimal policy and propose equivariant DQN and SAC algorithms that leverage this structure. We present experiments that demonstrate that our equivariant versions of DQN and SAC can be significantly more sample efficient than competing algorithms on an important class of robotic manipulation problems. (arXiv)

## 🧠 Key ideas (atomic)

- [[Equivariant neural network|Equivariant neural networks]] structure the model architecture such that it is constrained to represent only functions with the desired invariance properties. (Wang et al., 2022) `ev:cited` p. 1 ^wang2022so-001
- The authors argue that data augmentation yields only approximate equivariance, whereas [[Equivariant neural network|equivariant networks]] guarantee it and often generalize better. (Wang et al., 2022) `ev:cited` p. 1 ^wang2022so-002
- Prior applications of equivariant architectures to reinforcement learning were limited to toy settings such as grid worlds with small finite groups. (Wang et al., 2022) `ev:cited` p. 1 ^wang2022so-003
- As its first contribution, the paper defines and analyzes a class of Markov decision processes that it calls group-invariant MDPs. (Wang et al., 2022) `ev:asserted` p. 1 ^wang2022so-004
- The paper introduces a new variation of Equivariant DQN together with equivariant variations of SAC and of learning from demonstration. (Wang et al., 2022) `ev:asserted` p. 1 ^wang2022so-005
- The authors state that Equivariant SAC outperforms data augmentation baselines so dramatically that it could make reinforcement learning feasible for more robotics problems. (Wang et al., 2022) `ev:asserted` p. 2 ^wang2022so-006
- The authors state that data augmentation methods are often less sample efficient than [[Equivariant neural network|equivariant networks]], which inject an inductive bias into the architecture. (Wang et al., 2022) `ev:asserted` p. 2 ^wang2022so-007
- The authors state that contrastive learning is limited to learning an invariant feature encoder and cannot learn equivariant functions. (Wang et al., 2022) `ev:asserted` p. 2 ^wang2022so-008
- In a G-invariant MDP, the reward function is invariant to the group action, satisfying R(s, a) = R(gs, ga) for every element g. (Wang et al., 2022) `ev:asserted` p. 4 ^wang2022so-009
- In a G-invariant MDP, the transition function is likewise invariant to the group action, satisfying T(s, a, s′) = T(gs, ga, gs′). (Wang et al., 2022) `ev:asserted` p. 4 ^wang2022so-010
- Proposition 4.1 states that the optimal Q-function of a group-invariant MDP is invariant under the joint group action on states and actions. (Wang et al., 2022) `ev:computed` p. 4 ^wang2022so-011
- Proposition 4.1 further states that the optimal policy of a group-invariant MDP is group-equivariant, meaning π∗(gs) = gπ∗(s) for any g. (Wang et al., 2022) `ev:computed` p. 4 ^wang2022so-012
- The authors note that the G-invariant MDP is a special case of an MDP homomorphism, from which Proposition 4.1 follows directly. (Wang et al., 2022) `ev:cited` p. 4 ^wang2022so-013
- The paper approximates the continuous rotation group SO(2) by its discrete cyclic subgroup Cn for MDPs whose state is an image. (Wang et al., 2022) `ev:reported` p. 4 ^wang2022so-014
- The manipulation state is a depth image centered on the gripper, oriented relative to the base reference frame rather than the gripper frame. (Wang et al., 2022) `ev:reported` p. 4 ^wang2022so-015
- The action is a five-dimensional tuple of commanded gripper aperture, xy position change, height change and gripper orientation change. (Wang et al., 2022) `ev:reported` p. 4 ^wang2022so-016
- The commanded xy displacement is treated as equivariant under rotation, whereas the aperture, height and orientation action variables are treated as invariant. (Wang et al., 2022) `ev:reported` p. 4 ^wang2022so-017
- The authors argue that the transition dynamics are Cn-invariant because Newtonian physics of the interaction is invariant to the reference frame. (Wang et al., 2022) `ev:asserted` p. 4 ^wang2022so-018
- Equivariant DQN stacks equivariant layers mapping the state image to a Q-map whose spatial dimensions index the discrete xy actions. (Wang et al., 2022) `ev:reported` p. 5 ^wang2022so-019
- The authors state their DQN design is more efficient than Mondal et al. (2020), which learns the group-action mapping with FC layers. (Wang et al., 2022) `ev:asserted` p. 5 ^wang2022so-020
- Following Proposition 4.1, Equivariant SAC models the actor as an equivariant network and the critic as an invariant network. (Wang et al., 2022) `ev:reported` p. 5 ^wang2022so-021
- The policy standard deviation variables are assumed invariant to the group operator, which the authors consider sensible in robotics domains. (Wang et al., 2022) `ev:asserted` p. 5 ^wang2022so-022
- The critic uses an equivariant state encoder producing a regular representation, which is concatenated with the action before an invariant Q network. (Wang et al., 2022) `ev:reported` p. 6 ^wang2022so-023
- By Schur's Lemma, a linear map from regular to trivial representations could overconstrain the critic to encode additional undesired symmetries. (Wang et al., 2022) `ev:computed` p. 6 ^wang2022so-024
- To avoid this overconstraint, the critic uses a non-linear maxpool over the group space to map regular to trivial representations. (Wang et al., 2022) `ev:reported` p. 6 ^wang2022so-025
- SACfD pre-populates the replay buffer with expert demonstrations generated by a hand-coded planner before training begins. (Wang et al., 2022) `ev:reported` p. 6 ^wang2022so-026
- SACfD adds an L2 term to the actor loss that penalizes the difference between sampled and expert actions on expert transitions. (Wang et al., 2022) `ev:reported` p. 6 ^wang2022so-027
- All evaluated manipulation environments use sparse rewards, giving +1 when the goal is reached and 0 otherwise. (Wang et al., 2022) `ev:reported` p. 6 ^wang2022so-028
- Equivariant DQN was evaluated on Block Pulling, Object Picking and Drawer Opening using the group C4 and a discrete action space. (Wang et al., 2022) `ev:reported` p. 6 ^wang2022so-029
- The conventional CNN DQN baseline has 3.9M trainable parameters, compared with 2.6M for the equivariant DQN network. (Wang et al., 2022) `ev:reported` p. 7 ^wang2022so-030
- For the DQN experiments, the replay buffer was pre-populated with 100 episodes of expert demonstrations at the start of training. (Wang et al., 2022) `ev:reported` p. 7 ^wang2022so-031
- Equivariant DQN learned faster than the CNN, RAD, DrQ and CURL baselines in all three evaluated DQN environments. (Wang et al., 2022) `ev:measured` p. 7 ^wang2022so-032
- Equivariant DQN converged at a higher discounted reward than the baselines in Block Pulling, Object Picking and Drawer Opening. (Wang et al., 2022) `ev:measured` p. 7 ^wang2022so-033
- Equivariant SAC was evaluated with the group C8 and continuous xy and height displacements within [−0.05m, 0.05m]. (Wang et al., 2022) `ev:reported` p. 7 ^wang2022so-034
- The conventional CNN SAC baseline has 2.6M trainable parameters, compared with 2.3M for the Equivariant SAC network. (Wang et al., 2022) `ev:reported` p. 7 ^wang2022so-035
- All SAC methods used an SO(2) buffer augmentation that adds 4 randomly rotated transitions for every new transition stored. (Wang et al., 2022) `ev:reported` p. 8 ^wang2022so-036
- Equivariant SAC outperformed the CNN SAC, RAD, DrQ and FERM baselines significantly in Block Pulling, Object Picking and Drawer Opening. (Wang et al., 2022) `ev:measured` p. 8 ^wang2022so-037
- Without the equivariant approach, Object Picking and Drawer Opening appeared to be infeasible for the baseline SAC methods. (Wang et al., 2022) `ev:measured` p. 8 ^wang2022so-038
- In Block Pulling, FERM was the only baseline other than Equivariant SAC that was able to solve the task. (Wang et al., 2022) `ev:measured` p. 8 ^wang2022so-039
- For harder tasks, all methods were augmented with SACfD and Prioritized Experience Replay instead of a standard replay buffer. (Wang et al., 2022) `ev:reported` p. 8 ^wang2022so-040
- Equivariant SACfD performed best on all four harder tasks, followed by FERM and then the other baselines. (Wang et al., 2022) `ev:measured` p. 8 ^wang2022so-041
- Only the equivariant method solved Block Stacking, House Building and Corner Picking, the three most challenging tasks evaluated. (Wang et al., 2022) `ev:measured` p. 8 ^wang2022so-042
- The authors suggest [[Equivariant neural network|equivariant models]] are important for learning from demonstration, not only for unstructured reinforcement learning. (Wang et al., 2022) `ev:asserted` p. 8 ^wang2022so-043
- Equivariant SACfD outperformed RAD and DrQ baselines modified to learn SO(2) equivariance through rotational augmentation of state and action. (Wang et al., 2022) `ev:measured` p. 9 ^wang2022so-044
- In the generalization experiment, agents trained with a fixed object orientation were evaluated with random orientations and no buffer augmentation. (Wang et al., 2022) `ev:reported` p. 9 ^wang2022so-045
- Trained on a single orientation, Equivariant SACfD generalized over random orientations, whereas none of the baselines could do so. (Wang et al., 2022) `ev:measured` p. 9 ^wang2022so-046
- A stated limitation is that G-invariant MDPs require invariant reward and transition functions, limiting use in domains like some ATARI games. (Wang et al., 2022) `ev:asserted` p. 9 ^wang2022so-047
- The authors state that with non-top-down observations or non-equivariant structures like the robot arm, the G-invariant MDP assumptions are not directly satisfied. (Wang et al., 2022) `ev:asserted` p. 9 ^wang2022so-048
- The state image carries an extra binary channel indicating whether the gripper holds an object, which is invariant to rotations. (Wang et al., 2022) `ev:reported` p. 14 ^wang2022so-049
- The simulated PyBullet workspace in which all manipulation environments are implemented measures 0.4m × 0.4m × 0.24m. (Wang et al., 2022) `ev:reported` p. 14 ^wang2022so-050
- The equivariant models were implemented using the E2CNN [[Steerable CNN|steerable CNN library]] together with PyTorch for all experiments. (Wang et al., 2022) `ev:reported` p. 14 ^wang2022so-051
- The Equivariant DQN is a 7-layer [[Steerable CNN]] in the group C4 whose output is an 18-channel 3 × 3 feature map. (Wang et al., 2022) `ev:reported` p. 14 ^wang2022so-052
- The Equivariant SAC actor is an 8-layer Steerable CNN defined in the group C8 that takes a 2-channel state image. (Wang et al., 2022) `ev:reported` p. 14 ^wang2022so-053
- The Equivariant SAC critic is a 9-layer Steerable CNN in the group C8 taking both the state image and the action. (Wang et al., 2022) `ev:reported` p. 14 ^wang2022so-054
- Visual states were 128×128 pixels covering a 0.6m × 0.6m field of view, with training run on 5 parallel environments. (Wang et al., 2022) `ev:reported` p. 15 ^wang2022so-055
- DQN training used Adam with learning rate 10−4, Huber TD loss, discount factor γ = 0.95 and batch size 32. (Wang et al., 2022) `ev:reported` p. 15 ^wang2022so-056
- SAC training used Adam with learning rate 10−3, discount factor γ = 0.99, batch size 64 and a buffer of 100,000 transitions. (Wang et al., 2022) `ev:reported` p. 16 ^wang2022so-057
- In the ablation, applying the equivariant network in the actor helped more than applying it in the critic in 5 out of 6 experiments. (Wang et al., 2022) `ev:measured` p. 18 ^wang2022so-058
- Using equivariant networks in both the actor and the critic always gave the best performance in the actor-critic ablation. (Wang et al., 2022) `ev:measured` p. 18 ^wang2022so-059
- In the symmetry-group ablation, the network defined in C8 generally outperformed the C4 network, followed by the C2 network. (Wang et al., 2022) `ev:measured` p. 18 ^wang2022so-060
- In non-symmetric tasks with fixed initial orientations, the performance gain from using the equivariant network is less significant. (Wang et al., 2022) `ev:measured` p. 18 ^wang2022so-061
- None of the rotational augmentation baselines equipped with the augmentation buffer outperformed Equivariant SACfD in any of the tasks. (Wang et al., 2022) `ev:measured` p. 19 ^wang2022so-062
- The data augmentation buffer hurt RAD and DrQ performance, which the authors attribute to redundancy of the same data augmentation. (Wang et al., 2022) `ev:measured` p. 19 ^wang2022so-063

## 🎯 Contributions

## 📖 Glossary

- **Equivariance** — a function commutes with a group action: transforming the input transforms the output correspondingly.
- **Invariance** — a function output is unchanged when a group action transforms its input.
- **SO(2)** — the group of continuous planar rotations.
- **Cn** — the cyclic subgroup of SO(2) with rotations by multiples of 2π/n.
- **G-invariant MDP** — an MDP whose reward and transition functions are invariant to a group action.
- **Regular representation** — group action that cyclically permutes n feature channels, one per group element.
- **Trivial representation** — group action that leaves the feature value unchanged.
- **Steerable CNN** — convolutional network whose kernels are constrained to be equivariant to a symmetry group.
- **SACfD** — soft actor-critic with expert demonstrations in the buffer and an L2 imitation term.
- **Equivariance overconstraint** — linear regular-to-trivial maps imposing extra unwanted symmetries on the critic.

## ❓ Open questions

- How well do the equivariant agents transfer from PyBullet simulation to a physical robot?
- Can the approach be extended to observations that are not top-down, where the G-invariant MDP assumptions fail?
- How should non-equivariant structures in the image, such as the robot arm, be handled without breaking equivariance?
- Can the method extend to SE(3) or other symmetry groups beyond planar rotations?
- How does performance degrade when the reward function is only approximately rotation-invariant?

## 📝 Notes on reading

The cached text is the ICLR 2022 camera-ready version posted as arXiv 2203.04439v1, matching the packet identifier. All results (Figures 6-10, 14-18) are learning curves averaged over four runs with standard-error shading; no numeric success rates are given in text, so result claims are qualitative as the paper states them. Equations 1-4, 6-9 and the Appendix A/B proofs are partly garbled by extraction (matrices, sums, integrals); only their stated conclusions were claimed. Figure 2, 3, 4, 12 and 13 (scene, Q-map equivariance, actor/critic and network diagrams) could only be described. The abstract says equivariant DQN and SAC can be significantly more sample efficient; the body supports this with curves only.

## Suggested new concepts

- Group-invariant MDP — a reusable formalism linking MDP symmetry to invariant Q-functions and equivariant policies.
- Equivariant reinforcement learning — a line of work building symmetry into RL networks for sample efficiency in robotics.
- Equivariance vs. data augmentation — a recurring comparison on how to inject symmetry priors into learning.
- Steerable CNN — the architecture family underlying E2CNN-based equivariant models.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — RL equivariante para manipulación (C.6).

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
