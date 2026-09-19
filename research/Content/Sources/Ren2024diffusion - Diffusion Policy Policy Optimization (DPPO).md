---
aliases: []
type: "source"
title: "Diffusion Policy Policy Optimization (DPPO)"
citekey: "Ren2024diffusion"
doi: "10.48550/arXiv.2409.00588"
arxiv: "2409.00588"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2409.00588"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Allen Z. Ren", "Justin Lidard", "Lars L. Ankile", "Anthony Simeonov", "Pulkit Agrawal", "Anirudha Majumdar", "Benjamin Burchfiel", "Hongkai Dai", "Max Simchowitz"]
sha256: ["4b81907b0a8ea7118e4922720f2e7d269d5cf00d3725e44fc6d25f49d02413f3"]
pdf: "Content/Papers/Ren2024diffusion.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Ren2024diffusion.pdf]]

> [!abstract] One-sentence summary
> DPPO fine-tunes pre-trained Diffusion Policies with PPO by treating denoising as an inner MDP, beating Q-learning and Gaussian baselines on long-horizon manipulation and transferring zero-shot to a real Franka arm.

## Abstract

We introduce Diffusion Policy Policy Optimization, DPPO, an algorithmic framework including best practices for fine-tuning diffusion-based policies (e.g. Diffusion Policy) in continuous control and robot learning tasks using the policy gradient (PG) method from reinforcement learning (RL). PG methods are ubiquitous in training RL policies with other policy parameterizations; nevertheless, they had been conjectured to be less efficient for diffusion-based policies. Surprisingly, we show that DPPO achieves the strongest overall performance and efficiency for fine-tuning in common benchmarks compared to other RL methods for diffusion-based policies and also compared to PG fine-tuning of other policy parameterizations. Through experimental investigation, we find that DPPO takes advantage of unique synergies between RL fine-tuning and the diffusion parameterization, leading to structured and on-manifold exploration, stable training, and strong policy robustness. We further demonstrate the strengths of DPPO in a range of realistic settings, including simulated robotic tasks with pixel observations, and via zero-shot deployment of simulation-trained policies on robot hardware in a long-horizon, multi-stage manipulation task. Website with code: diffusion-ppo.github.io (arXiv)

## 🧠 Key ideas (atomic)

- DPPO is a framework with chosen design decisions for fine-tuning a pre-trained diffusion-based robot policy through reinforcement learning policy gradient methods. (Ren et al., 2024) `ev:asserted` p. 1 ^ren2024diffusion-001
- Policy gradient methods have been believed to be inefficient for training Diffusion Policy in continuous control tasks, according to prior work. (Ren et al., 2024) `ev:cited` p. 1 ^ren2024diffusion-002
- DPPO treats the denoising process as a Markov Decision Process, allowing the task reward signal to propagate through the Diffusion Policy. (Ren et al., 2024) `ev:asserted` p. 2 ^ren2024diffusion-003
- Psenka et al. conjectured that policy gradient through Diffusion Policy is likely ineffective due to large action variance from denoising steps. (Ren et al., 2024) `ev:cited` p. 4 ^ren2024diffusion-004
- DPPO embeds the denoising MDP into the environment MDP, forming a larger two-layer MDP called the Diffusion Policy MDP. (Ren et al., 2024) `ev:asserted` p. 5 ^ren2024diffusion-005
- In the Diffusion Policy MDP, reward is only given at the steps where the fully denoised action is taken in the environment. (Ren et al., 2024) `ev:asserted` p. 6 ^ren2024diffusion-006
- The policy at each denoising step is a Gaussian likelihood that can be evaluated analytically and is amenable to policy gradient updates. (Ren et al., 2024) `ev:asserted` p. 6 ^ren2024diffusion-007
- DPPO instantiates the policy gradient update with Proximal Policy Optimization, applied to the two-layer Diffusion Policy MDP. (Ren et al., 2024) `ev:reported` p. 6 ^ren2024diffusion-008
- The DPPO advantage estimator applies a denoising discount that downweights the contribution of noisier denoising steps to the policy gradient. (Ren et al., 2024) `ev:asserted` p. 7 ^ren2024diffusion-009
- A value estimator depending only on the environment state gave more efficient and stable training than also valuing the denoised action. (Ren et al., 2024) `ev:measured` p. 7 ^ren2024diffusion-010
- Fine-tuning only the last few denoising steps speeds up DPPO training and reduces GPU memory usage without sacrificing final performance. (Ren et al., 2024) `ev:measured` p. 7 ^ren2024diffusion-011
- DDIM sampling can reduce the number of fine-tuned denoising steps to as few as 5, potentially improving DPPO efficiency. (Ren et al., 2024) `ev:asserted` p. 7 ^ren2024diffusion-012
- Clipping the diffusion noise to a higher minimum value, such as 0.01 to 0.1, when sampling actions helps DPPO exploration. (Ren et al., 2024) `ev:measured` p. 7 ^ren2024diffusion-013
- MLP policy heads offer a simpler setup and generally fine-tune more stably with DPPO than UNet heads. (Ren et al., 2024) `ev:measured` p. 8 ^ren2024diffusion-014
- DPPO benefits from pre-training with a larger prediction horizon Tp and fine-tuning with a smaller executed action chunk Ta. (Ren et al., 2024) `ev:measured` p. 8 ^ren2024diffusion-015
- DPPO training can be up to 2× slower in wall-clock time than training with other policy parameterizations. (Ren et al., 2024) `ev:measured` p. 8 ^ren2024diffusion-016
- On Robomimic, state-based and pixel-based policies were pre-trained with 300 and 100 provided demonstrations, respectively. (Ren et al., 2024) `ev:reported` p. 8 ^ren2024diffusion-017
- Furniture-Bench policies were pre-trained with 50 human demonstrations collected in simulation, using an action chunk size Ta = 8. (Ren et al., 2024) `ev:reported` p. 8 ^ren2024diffusion-018
- Among diffusion-based RL fine-tuning methods, DPPO is the strongest performer on Robomimic tasks, especially the challenging Transport task. (Ren et al., 2024) `ev:measured` p. 9 ^ren2024diffusion-019
- On Gym locomotion tasks, IDQL and DIPO exhibit performance competitive with DPPO among the diffusion-based RL baselines. (Ren et al., 2024) `ev:measured` p. 9 ^ren2024diffusion-020
- IDQL and DRWR are strong baselines on Lift, Can, and Square but underperform on Transport. (Ren et al., 2024) `ev:measured` p. 9 ^ren2024diffusion-021
- The authors postulate that off-policy baselines propagating gradients from imperfect Q functions suffer greater training instability in sparse-reward Robomimic tasks. (Ren et al., 2024) `ev:asserted` p. 9 ^ren2024diffusion-022
- Demo-augmented off-policy methods RLPD, Cal-QL and IBRL are significantly more sample efficient than DPPO on HalfCheetah-v2. (Ren et al., 2024) `ev:measured` p. 10 ^ren2024diffusion-023
- In Franka Kitchen, RLPD and IBRL fail to learn well, especially with the noisier Kitchen-Partial-v0 and Kitchen-Mixed-v0 demonstrations. (Ren et al., 2024) `ev:measured` p. 10 ^ren2024diffusion-024
- DPPO achieves the best overall performance across Franka Kitchen settings, especially with the Kitchen-Complete-v0 dataset. (Ren et al., 2024) `ev:measured` p. 10 ^ren2024diffusion-025
- DPPO, which uses no expert data during fine-tuning, can be sensitive to the performance of the pre-trained policy. (Ren et al., 2024) `ev:asserted` p. 10 ^ren2024diffusion-026
- On Robomimic Can and Square, RLPD and Cal-QL fail to learn at all from either PH or MH data. (Ren et al., 2024) `ev:measured` p. 10 ^ren2024diffusion-027
- DPPO runs significantly faster in wall-clock time than demo-augmented baselines as it leverages highly parallelized environment sampling. (Ren et al., 2024) `ev:measured` p. 10 ^ren2024diffusion-028
- With state input, DPPO pre-trains with 20 denoising steps and then fine-tunes the last 10 steps. (Ren et al., 2024) `ev:reported` p. 11 ^ren2024diffusion-029
- With state input on Robomimic, DPPO outperforms Gaussian and GMM policies that are also fine-tuned with the PPO objective. (Ren et al., 2024) `ev:measured` p. 11 ^ren2024diffusion-030
- With state input, DPPO reaches > 90% success rate on the challenging Robomimic Transport task after fine-tuning. (Ren et al., 2024) `ev:measured` p. 11 ^ren2024diffusion-031
- With pixel input, Gaussian-ViT-MLP does not improve on Transport from its 0% pre-trained success rate during fine-tuning. (Ren et al., 2024) `ev:measured` p. 11 ^ren2024diffusion-032
- The authors state that, to their knowledge, DPPO is the first RL algorithm to solve Transport to high (>50%) success rates. (Ren et al., 2024) `ev:asserted` p. 11 ^ren2024diffusion-033
- On Furniture-Bench, DPPO exhibits strong training stability and improves policy performance in all six task and randomness settings. (Ren et al., 2024) `ev:measured` p. 11 ^ren2024diffusion-034
- Gaussian-MLP collapses to zero success rate in all three Med-randomness Furniture-Bench tasks, except for one Lamp seed. (Ren et al., 2024) `ev:measured` p. 11 ^ren2024diffusion-035
- DPPO and Gaussian policies trained in simulated One-leg were evaluated zero-shot on physical hardware over 20 trials at 10Hz. (Ren et al., 2024) `ev:reported` p. 11 ^ren2024diffusion-036
- DPPO improves the real-world One-leg success rate to 80%, succeeding in 16 out of 20 hardware trials. (Ren et al., 2024) `ev:measured` p. 12 ^ren2024diffusion-037
- The fine-tuned Gaussian policy reaches 88% success in simulation but fails entirely on hardware with 0% success. (Ren et al., 2024) `ev:measured` p. 12 ^ren2024diffusion-038
- Gaussian fine-tuning with an auxiliary behavior-cloning loss reaches only 53% success rate in simulation and 50% in reality. (Ren et al., 2024) `ev:measured` p. 12 ^ren2024diffusion-039
- Qualitatively, fine-tuned policies are more robust and exhibit more corrective behaviors than pre-trained-only policies, especially during insertion. (Ren et al., 2024) `ev:measured` p. 12 ^ren2024diffusion-040
- Ablations indicate a sweet spot for clipping the denoising noise level, trading off too little exploration against too much action noise. (Ren et al., 2024) `ev:measured` p. 12 ^ren2024diffusion-041
- The authors identify structured exploration near the pre-training data manifold as a major factor in DPPO's improved performance. (Ren et al., 2024) `ev:asserted` p. 12 ^ren2024diffusion-042
- In the D3IL Avoid task, DPPO explores with wide coverage around the expert data manifold at the first fine-tuning iteration. (Ren et al., 2024) `ev:measured` p. 13 ^ren2024diffusion-043
- The authors conjecture that on-manifold exploration may hinder fine-tuning when aggressive, unstructured exploration is desired, as in Low-randomness Lamp. (Ren et al., 2024) `ev:asserted` p. 14 ^ren2024diffusion-044
- DPPO is not observed to be substantially better, nor any worse, than Gaussian policies in exploration from scratch. (Ren et al., 2024) `ev:measured` p. 14 ^ren2024diffusion-045
- When noise is gradually added to actions during fine-tuning in Avoid, Gaussian and GMM policy performance both collapse. (Ren et al., 2024) `ev:measured` p. 14 ^ren2024diffusion-046
- DPPO fine-tuning performance is robust to the added action noise if at least four denoising steps are used. (Ren et al., 2024) `ev:measured` p. 14 ^ren2024diffusion-047
- DPPO enjoys greater training stability than Gaussian and GMM when fine-tuning long action chunks, up to Ta = 16. (Ren et al., 2024) `ev:measured` p. 14 ^ren2024diffusion-048
- Over DPPO fine-tuning iterations, the iterative refinement through denoising steps is largely preserved rather than collapsing to one step. (Ren et al., 2024) `ev:measured` p. 14 ^ren2024diffusion-049
- The fine-tuned DPPO policy exhibits strong robustness to noise added to its sampled actions compared to the Gaussian policy. (Ren et al., 2024) `ev:measured` p. 15 ^ren2024diffusion-050
- The authors name lower sample efficiency than off-policy methods as the main limitation of DPPO. (Ren et al., 2024) `ev:asserted` p. 16 ^ren2024diffusion-051
- In the more challenging tasks, DPPO's environment-state-only advantage estimator consistently leads to the most improved fine-tuning performance. (Ren et al., 2024) `ev:measured` p. 27 ^ren2024diffusion-052
- Fine-tuning too few denoising steps, such as 3, can lead to subpar asymptotic performance and slower convergence, especially in Can. (Ren et al., 2024) `ev:measured` p. 28 ^ren2024diffusion-053
- DPPO obtains 60% success rate on One-leg after pre-training with only 10 episodes of demonstrations. (Ren et al., 2024) `ev:measured` p. 28 ^ren2024diffusion-054
- Trained from scratch, DPPO takes about 6× the wall-clock time of Gaussian training, due to multi-step denoising sampling. (Ren et al., 2024) `ev:measured` p. 29 ^ren2024diffusion-055
- Policy gradient using exact diffusion action likelihood drops to zero success rate on the more challenging Can task. (Ren et al., 2024) `ev:measured` p. 31 ^ren2024diffusion-056
- In Gym tasks, DPPO trains on average 41%, 37%, and 12% faster than DAWR, DIPO, and DQL, respectively. (Ren et al., 2024) `ev:measured` p. 31 ^ren2024diffusion-057
- With pixel input on Robomimic, DPPO-ViT-MLP trains on average 14% slower per iteration than Gaussian-ViT-MLP. (Ren et al., 2024) `ev:measured` p. 33 ^ren2024diffusion-058
- For [[Sim-to-real transfer|sim-to-real transfer]], noise with 0.03 standard deviation was added to DPPO's sampled actions to simulate an imperfect controller. (Ren et al., 2024) `ev:reported` p. 42 ^ren2024diffusion-059
- Adding such simulated controller noise to the Gaussian policy during training led to a zero task success rate. (Ren et al., 2024) `ev:measured` p. 42 ^ren2024diffusion-060

## 🎯 Contributions

## 📖 Glossary

- **Diffusion Policy** — A policy parameterized by a denoising diffusion model conditioned on the observation.
- **Diffusion Policy MDP** — Two-layer MDP nesting the denoising chain inside each environment step.
- **DDIM** — Denoising Diffusion Implicit Model; a sampler needing far fewer denoising steps than DDPM.
- **PPO** — Proximal Policy Optimization; on-policy policy gradient with a clipped likelihood ratio.
- **Action chunk** — Sequence of future actions predicted at once; Ta steps are executed.
- **Denoising discount** — Factor downweighting the policy gradient contribution of noisier denoising steps.
- **On-manifold exploration** — Exploration that stays close to the distribution of expert demonstration data.
- **Demo-augmented RL** — RL methods that inject offline demonstrations into online training, e.g. RLPD, IBRL.
- **Zero-shot sim-to-real** — Deploying a simulation-trained policy on hardware with no real-world data.

## ❓ Open questions

- Can DPPO's sample efficiency approach that of off-policy methods, for example through model-based planning or video prediction?
- Does DPPO benefit as expected from pre-training on large, diverse multi-task data for vision-based sim-to-real?
- How should a curriculum of denoising steps be designed to balance from-scratch training performance and wall-clock cost?
- Can DPPO recover missing modes when the pre-trained policy fails to capture all modes of highly multi-modal data?
- When aggressive unstructured exploration is needed, can DPPO's on-manifold exploration be relaxed without losing stability?
- Does DPPO transfer to non-robotics sequential settings such as multi-turn text-to-image generation or molecular design?

## 📝 Notes on reading

Read arXiv v3 (9 Dec 2024), matching the packet identifier 2409.00588. Most results are learning curves in Figures 5 to 13 and A1 to A11; their per-seed values are not in the text and were described only where the text summarises them. Hyperparameter Tables A7 to A11 (pp. 43 to 46) came through the extraction as disordered cells and were not claimed. Wall-clock Tables A1 to A5 are legible; only the text summaries were claimed. Minor inconsistencies: Appendix C.7 cites Fig. A3 right for the structured-exploration ablation, but the caption making that comparison is Fig. A11; Appendix C.3 says larger action chunks give poor from-scratch training as shown in Fig. A6, which is the expert-data figure; Table A6 caption lists Obs dim - State twice. The Gaussian baseline was reported as heavily tuned, reaching about 100% on Lamp with Low randomness, which the paper uses to argue the baseline is strong. Hardware used a Franka Emika Panda arm with a Polymetis joint impedance controller at 1kHz, AprilTag state estimation from 4 cameras, and single-blind trials (pp. 40 to 42).

## Suggested new concepts

- Diffusion Policy MDP — the two-layer denoising-inside-environment MDP is the core formal device reused by later RL fine-tuning work on diffusion and flow policies.
- RL fine-tuning of behavior-cloned policies — a recurring pipeline (pre-train by imitation, improve by RL) that this paper and its baselines all instantiate.
- On-manifold exploration — a distinct explanation for why diffusion parameterizations help RL, worth tracking across papers.
- Zero-shot sim-to-real transfer — hardware deployment without real data is a key evaluation axis for manipulation policies.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — PPO sobre la cadena de denoising (D.2, F.7).
