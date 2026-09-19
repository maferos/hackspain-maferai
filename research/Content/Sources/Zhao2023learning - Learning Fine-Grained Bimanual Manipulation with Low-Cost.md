---
aliases: []
type: "source"
title: "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (ACT)"
citekey: "Zhao2023learning"
doi: "10.48550/arXiv.2304.13705"
arxiv: "2304.13705"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2304.13705"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Tony Z. Zhao", "Vikash Kumar", "Sergey Levine", "Chelsea Finn"]
sha256: ["2e2fe25860f5f9cee9e655a2714e9f2264a7a5078bcd267c16d3f39af461345a"]
pdf: "Content/Papers/Zhao2023learning.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Zhao2023learning.pdf]]

> [!abstract] One-sentence summary
> The paper pairs ALOHA, a roughly $20k open-source bimanual teleoperation rig, with ACT, a transformer CVAE policy that predicts action chunks, and learns six real fine-manipulation tasks from about 50 demonstrations each.

## Abstract

Fine manipulation tasks, such as threading cable ties or slotting a battery, are notoriously difficult for robots because they require precision, careful coordination of contact forces, and closed-loop visual feedback. Performing these tasks typically requires high-end robots, accurate sensors, or careful calibration, which can be expensive and difficult to set up. Can learning enable low-cost and imprecise hardware to perform these fine manipulation tasks? We present a low-cost system that performs end-to-end imitation learning directly from real demonstrations, collected with a custom teleoperation interface. Imitation learning, however, presents its own challenges, particularly in high-precision domains: errors in the policy can compound over time, and human demonstrations can be non-stationary. To address these challenges, we develop a simple yet novel algorithm, Action Chunking with Transformers (ACT), which learns a generative model over action sequences. ACT allows the robot to learn 6 difficult tasks in the real world, such as opening a translucent condiment cup and slotting a battery with 80-90% success, with only 10 minutes worth of demonstrations. Project website: https://tonyzhaozh.github.io/aloha/ (arXiv)

## 🧠 Key ideas (atomic)

- Fine manipulation tasks such as opening a condiment cup lid require high precision, where millimeters of error would lead to task failure. (Zhao et al., 2023) `ev:asserted` p. 1 ^zhao2023learning-001
- Existing fine manipulation systems rely on expensive robots with high-end sensors to obtain precise state estimation, according to the cited prior work. (Zhao et al., 2023) `ev:cited` p. 1 ^zhao2023learning-002
- The authors train an end-to-end policy that maps RGB images from commodity web cameras directly to the robot actions. (Zhao et al., 2023) `ev:reported` p. 1 ^zhao2023learning-003
- The authors argue that learning a closed-loop manipulation policy is much simpler than modeling the complex physics of the whole environment for planning. (Zhao et al., 2023) `ev:asserted` p. 1 ^zhao2023learning-004
- The teleoperation setup uses two sets of low-cost, off-the-shelf robot arms that are approximately scaled versions of each other, coupled by joint-space mapping. (Zhao et al., 2023) `ev:reported` p. 2 ^zhao2023learning-005
- In ACT, the policy predicts the target joint positions for the next k timesteps rather than a single step at a time. (Zhao et al., 2023) `ev:reported` p. 2 ^zhao2023learning-006
- The authors state that predicting [[Action chunking|chunks of k actions]] reduces the effective horizon of the task k-fold, mitigating compounding errors. (Zhao et al., 2023) `ev:asserted` p. 2 ^zhao2023learning-007
- Predicting action sequences also helps with temporally correlated confounders, such as pauses in demonstrations that are hard to model with Markovian single-step policies. (Zhao et al., 2023) `ev:asserted` p. 2 ^zhao2023learning-008
- The [[Action chunking|action chunking]] policy is implemented with Transformers and trained as a conditional VAE to capture the variability in human demonstration data. (Zhao et al., 2023) `ev:reported` p. 2 ^zhao2023learning-009
- The system learns 6 fine manipulation skills in the real world, including slotting a battery with 80-90% success, from only 10 minutes of demonstrations. (Zhao et al., 2023) `ev:measured` p. 2 ^zhao2023learning-010
- A major shortcoming of behavioral cloning is compounding errors, where accumulated errors from previous timesteps drive the robot off its training distribution. (Zhao et al., 2023) `ev:cited` p. 2 ^zhao2023learning-011
- The authors argue that injecting noise during demonstration collection can directly lead to task failure in fine manipulation, reducing teleoperation dexterity. (Zhao et al., 2023) `ev:asserted` p. 2 ^zhao2023learning-012
- Unlike the system of Kim et al., ALOHA uses no special encoders, sensors, or machined components, only off-the-shelf robots and 3D printed parts. (Zhao et al., 2023) `ev:reported` p. 3 ^zhao2023learning-013
- The authors state that non-experts can assemble the ALOHA system from off-the-shelf robots and printed parts in less than 2 hours. (Zhao et al., 2023) `ev:asserted` p. 3 ^zhao2023learning-014
- The ViperX 6-DoF follower arm used in ALOHA has a working payload of 750g, a 1.5m span, and 5-8mm accuracy. (Zhao et al., 2023) `ev:reported` p. 3 ^zhao2023learning-015
- The ViperX 6-DoF follower arm used in ALOHA can be purchased off-the-shelf for around $5600 per arm. (Zhao et al., 2023) `ev:reported` p. 3 ^zhao2023learning-016
- The authors replaced the OEM fingers with custom 3D printed see-through fingers fitted with gripping tape for fine manipulation tasks. (Zhao et al., 2023) `ev:reported` p. 3 ^zhao2023learning-017
- The leader is a smaller WidowX arm costing $3300, whose joints are synchronized with the larger ViperX follower through direct joint-space mapping. (Zhao et al., 2023) `ev:reported` p. 3 ^zhao2023learning-018
- The authors report that off-the-shelf inverse kinematics fails frequently near singularities of their 6-DoF arm, which has no redundancy. (Zhao et al., 2023) `ev:asserted` p. 3 ^zhao2023learning-019
- The authors noticed better performance on precise tasks with joint-space mapping than with holding a VR controller for task-space teleoperation. (Zhao et al., 2023) `ev:asserted` p. 3 ^zhao2023learning-020
- A rubber band load balancing mechanism partially counteracts gravity on the leader side, making teleoperation sessions longer than 30 minutes possible. (Zhao et al., 2023) `ev:reported` p. 3 ^zhao2023learning-021
- Four Logitech C922x webcams stream 480×640 RGB images, with two mounted on the follower wrists and two at the front and top. (Zhao et al., 2023) `ev:reported` p. 3 ^zhao2023learning-022
- Both teleoperation and data recording in the ALOHA setup happen at a control frequency of 50Hz. (Zhao et al., 2023) `ev:reported` p. 3 ^zhao2023learning-023
- ALOHA was built within a 20k USD budget, comparable to a single research arm such as the Franka Emika Panda. (Zhao et al., 2023) `ev:reported` p. 4 ^zhao2023learning-024
- To the authors' knowledge, skills like threading a zip tie or inserting RAM are unavailable on existing teleoperation systems with 5-10x the budget. (Zhao et al., 2023) `ev:asserted` p. 4 ^zhao2023learning-025
- Recorded actions are the leader robots' joint positions rather than the follower's, since applied force is implicitly defined by their difference. (Zhao et al., 2023) `ev:reported` p. 4 ^zhao2023learning-026
- A naive [[Action chunking|action chunking]] implementation incorporates new observations abruptly every k steps, which can result in jerky robot motion. (Zhao et al., 2023) `ev:asserted` p. 5 ^zhao2023learning-027
- Temporal ensembling queries the policy at every timestep and averages overlapping chunk predictions for the same timestep with exponential weights. (Zhao et al., 2023) `ev:reported` p. 5 ^zhao2023learning-028
- According to the authors, temporal ensembling incurs no additional training cost, only extra computation at inference time. (Zhao et al., 2023) `ev:asserted` p. 5 ^zhao2023learning-029
- For faster training, the CVAE encoder leaves out image observations, conditioning only on the proprioceptive observation and the action sequence. (Zhao et al., 2023) `ev:reported` p. 5 ^zhao2023learning-030
- At test time the style variable z is set to the prior mean of zero, making the policy decode deterministically. (Zhao et al., 2023) `ev:reported` p. 5 ^zhao2023learning-031
- A ResNet18 backbone converts each 480 × 640 × 3 RGB image into 15 × 20 × 512 feature maps for the policy. (Zhao et al., 2023) `ev:reported` p. 5 ^zhao2023learning-032
- The transformer encoder input is a 1202×512 sequence combining features from four camera images, the current joint positions, and the style variable. (Zhao et al., 2023) `ev:reported` p. 6 ^zhao2023learning-033
- The authors noted that L1 reconstruction loss leads to more precise modeling of the action sequence than the more common L2 loss. (Zhao et al., 2023) `ev:asserted` p. 6 ^zhao2023learning-034
- The authors noted degraded performance when using delta joint positions as actions instead of absolute target joint positions. (Zhao et al., 2023) `ev:asserted` p. 6 ^zhao2023learning-035
- Each task gets its own ACT model with around 80M parameters, trained from scratch on that task's demonstrations. (Zhao et al., 2023) `ev:reported` p. 6 ^zhao2023learning-036
- Training one ACT policy takes around 5 hours on a single 11G RTX 2080 Ti GPU, according to the authors. (Zhao et al., 2023) `ev:reported` p. 6 ^zhao2023learning-037
- ACT inference takes around 0.01 seconds on the same single 11G RTX 2080 Ti GPU used for training. (Zhao et al., 2023) `ev:measured` p. 6 ^zhao2023learning-038
- Evaluation covers 6 real-world ALOHA tasks plus two simulated fine manipulation tasks built in MuJoCo for ease of reproducibility. (Zhao et al., 2023) `ev:reported` p. 6 ^zhao2023learning-039
- Each real-world demonstration episode takes 8-14 seconds, corresponding to 400-700 time steps at the 50Hz control frequency. (Zhao et al., 2023) `ev:reported` p. 8 ^zhao2023learning-040
- The authors record 50 demonstrations for each real-world task, except Thread Velcro, which has 100 demonstrations. (Zhao et al., 2023) `ev:reported` p. 8 ^zhao2023learning-041
- Demonstrations total around 10-20 minutes of data per task, taking 30-60 minutes of wall-clock time including resets and teleoperator mistakes. (Zhao et al., 2023) `ev:reported` p. 8 ^zhao2023learning-042
- Baselines BeT and RT-1 discretize the action space, whereas ACT directly predicts continuous actions, motivated by the precision fine manipulation requires. (Zhao et al., 2023) `ev:reported` p. 8 ^zhao2023learning-043
- ACT outperforms the best previous method in success rate on the two simulated tasks by 59%, 49%, 29%, and 20%. (Zhao et al., 2023) `ev:measured` p. 9 ^zhao2023learning-044
- On Slide Ziploc and Slot Battery, ACT achieves 88% and 96% final success, with other methods making no progress past the first stage. (Zhao et al., 2023) `ev:measured` p. 9 ^zhao2023learning-045
- On the simulated Transfer Cube task, ACT reaches 86% final success with scripted data and 50% with human data. (Zhao et al., 2023) `ev:measured` p. 8 ^zhao2023learning-046
- The authors attribute the poor performance of prior methods to compounding errors and non-Markovian behavior in the demonstration data. (Zhao et al., 2023) `ev:asserted` p. 9 ^zhao2023learning-047
- All methods drop in performance when switching from scripted data to human data in the two simulated tasks. (Zhao et al., 2023) `ev:measured` p. 9 ^zhao2023learning-048
- ACT reaches 84% success for Cup Open, 20% for Thread Velcro, 64% for Prep Tape, and 92% for Put On Shoe. (Zhao et al., 2023) `ev:measured` p. 9 ^zhao2023learning-049
- BeT, the best performing baseline, achieves zero final success on Open Cup, Thread Velcro, Prep Tape, and Put On Shoe. (Zhao et al., 2023) `ev:measured` p. 9 ^zhao2023learning-050
- In Thread Velcro, ACT success decreased by roughly half at every stage, from 92% at the first stage to 20% final success. (Zhao et al., 2023) `ev:measured` p. 9 ^zhao2023learning-051
- The authors link Thread Velcro failures to low contrast between the black cable tie and background, and its small image footprint. (Zhao et al., 2023) `ev:asserted` p. 9 ^zhao2023learning-052
- Without temporal ensembling, success averaged over four simulated settings improves from 1% at k = 1 to 44% at k = 100. (Zhao et al., 2023) `ev:measured` p. 9 ^zhao2023learning-053
- Adding [[Action chunking|action chunking]] to BC-ConvMLP and VINN gives consistent trends, suggesting chunking is generally beneficial for imitation learning in these settings. (Zhao et al., 2023) `ev:measured` p. 9 ^zhao2023learning-054
- In the temporal ensemble ablation, BC-ConvMLP gains 4% and ACT gains 3.3% in highest success rate across settings. (Zhao et al., 2023) `ev:measured` p. 9 ^zhao2023learning-055
- The authors hypothesize that temporal ensembling mostly benefits parametric methods by smoothing modeling errors, noting a performance drop for VINN. (Zhao et al., 2023) `ev:asserted` p. 9 ^zhao2023learning-056
- Removing the CVAE objective makes almost no difference in performance when training on the fully deterministic scripted data. (Zhao et al., 2023) `ev:measured` p. 10 ^zhao2023learning-057
- With human data, removing the CVAE objective drops success on the simulated tasks from 35.3% to 2%. (Zhao et al., 2023) `ev:measured` p. 10 ^zhao2023learning-058
- A user study with 6 participants compared teleoperation at 50Hz and 5Hz on threading a zip cable tie and unstacking plastic cups. (Zhao et al., 2023) `ev:reported` p. 10 ^zhao2023learning-059
- On average, participants took 33s to thread the zip tie at 5Hz, which was lowered to 20s at 50Hz. (Zhao et al., 2023) `ev:measured` p. 10 ^zhao2023learning-060
- The authors acknowledge tasks beyond the capability of either the robots or the learning algorithm, such as buttoning up a dress shirt. (Zhao et al., 2023) `ev:asserted` p. 10 ^zhao2023learning-061
- The Shadow Teleoperation System costs at least $400k, whereas ALOHA costs $18k, or $20k after adding optional add-ons such as cameras. (Zhao et al., 2023) `ev:reported` p. 14 ^zhao2023learning-062
- ALOHA recreated 14 out of the 15 Shadow Teleoperation System use cases, failing only the Baoding ball in-hand rotation task. (Zhao et al., 2023) `ev:measured` p. 14 ^zhao2023learning-063
- ALOHA struggles with tasks requiring high forces, such as lifting heavy objects, because the low-cost motors cannot generate enough torque. (Zhao et al., 2023) `ev:asserted` p. 16 ^zhao2023learning-064
- In a preliminary 10-trial candy unwrapping evaluation, the ACT policy picked up the candy 10/10 but unwrapped it 0/10. (Zhao et al., 2023) `ev:measured` p. 16 ^zhao2023learning-065
- With 10 trials given for each of 5 candies, the ACT policy successfully unwrapped 3/5 candies. (Zhao et al., 2023) `ev:measured` p. 16 ^zhao2023learning-066
- The authors believe pretraining, more data, and better perception are promising directions for extremely difficult tasks like opening a flat ziploc bag. (Zhao et al., 2023) `ev:asserted` p. 16 ^zhao2023learning-067
- ACT hyperparameters include a chunk size of 100, a beta of 10, a learning rate of 1e-5, and batch size 8. (Zhao et al., 2023) `ev:reported` p. 18 ^zhao2023learning-068

## 🎯 Contributions

## 📖 Glossary

- **Action chunking** — predicting a sequence of the next k actions from one observation instead of one action.
- **Temporal ensembling** — exponentially weighted averaging of overlapping chunk predictions made for the same timestep.
- **Compounding error** — small policy errors accumulating over time, pushing the robot outside its training distribution.
- **Joint-space mapping** — teleoperation where follower joints copy leader joints directly, without inverse kinematics.
- **Leader-follower teleoperation** — operator backdrives a leader arm whose motion a follower arm mirrors.
- **CVAE** — conditional variational autoencoder; here a generative model of action sequences given observations.
- **Style variable z** — CVAE latent summarising demonstration variability; set to zero at test time.
- **Behavioral cloning** — imitation learning cast as supervised learning from observations to actions.

## ❓ Open questions

- How does ACT perform with more than one training seed on real-world tasks, given only 1 seed and 25 trials were run?
- Would pretraining or larger datasets close the gap on tasks such as candy unwrapping and flat ziploc opening?
- Can the perception failures on low-contrast, thin objects (Thread Velcro) be fixed with better camera placement or depth sensing?
- How well does a per-task ACT policy generalize to new objects or scenes beyond the 15cm randomization line?
- Does the chunk size k = 100 transfer across tasks with different durations and control frequencies?

## 📝 Notes on reading

Read the arXiv preprint v1 (2304.13705v1, 23 Apr 2023), matching the packet identifier.

Inconsistencies inside the paper: the abstract and conclusion state 80-90% success for opening the cup and slotting the battery, but the tables give 84% (Open Cup) and 96% (Slot Battery). The abstract says 10 minutes of demonstrations, whereas Section V-B reports 10-20 minutes of data per task. The system cost is given as <$20k (Fig. 1), within a 20k USD budget (p. 4), and $18k or $20k with add-ons (Appendix A). The Fig. 10 caption says 5 real-world tasks while the text says 6. The CVAE encoder feature map in Fig. 11 is 15x20x728 while the text says 15 × 20 × 512. The text says the ensemble weight w0 is for the oldest action.

Figures only described: Fig. 8 (a)-(d) plots the chunk-size sweep, the temporal-ensemble ablation (+3.3%, +4%, -20% for VINN), the CVAE ablation (-1% scripted, -33.3% human) and user-study completion times; exact per-k values beyond those in the text were not claimed. Table I sub-task cells for baselines (e.g. BeT 60 | 16 on Touched) were summarised, not claimed cell by cell.

## Suggested new concepts

- Action chunking — a policy-output design reused widely in later imitation-learning work (diffusion policy, VLA models).
- Temporal ensembling — inference-time smoothing specific to chunked policies, distinct from ordinary action smoothing.
- ALOHA (low-cost bimanual teleoperation) — a hardware platform many later datasets and policies build on.
- Compounding error in imitation learning — the core failure mode ACT targets and a recurring theme across sources.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — ACT y hardware ALOHA (el brazo de nuestra escena)

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
