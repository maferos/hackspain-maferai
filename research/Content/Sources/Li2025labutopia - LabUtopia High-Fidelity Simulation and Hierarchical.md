---
aliases: []
type: "source"
title: "LabUtopia: High-Fidelity Simulation and Hierarchical Benchmark for Scientific Embodied Agents"
citekey: "Li2025labutopia"
doi: "10.48550/arXiv.2505.22634"
arxiv: "2505.22634"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2505.22634"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Rui Li", "Zixuan Hu", "Wenxi Qu", "Jinouwen Zhang", "Zhenfei Yin", "Sha Zhang", "Xuantuo Huang", "Hanqing Wang", "Tai Wang", "Jiangmiao Pang", "Wanli Ouyang", "Lei Bai", "Wangmeng Zuo", "Ling-Yu Duan", "Dongzhan Zhou", "Shixiang Tang"]
sha256: ["b0b27a506f9ec028871b09e93a5a3aead74e382739b65fa5092af90ab062e862"]
pdf: "Content/Papers/Li2025labutopia.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Li2025labutopia.pdf]]

> [!abstract] One-sentence summary
> LabUtopia is an Isaac Sim-based laboratory simulator with LLM-driven chemistry, procedurally generated lab scenes and a five-level benchmark, on which ACT, Diffusion Policy and π0 degrade sharply on long-horizon and shape-generalization tasks.

## Abstract

Scientific embodied agents play a crucial role in modern laboratories by automating complex experimental workflows. Compared to typical household environments, laboratory settings impose significantly higher demands on perception of physical-chemical transformations and long-horizon planning, making them an ideal testbed for advancing embodied intelligence. However, its development has been long hampered by the lack of suitable simulator and benchmarks. In this paper, we address this gap by introducing LabUtopia, a comprehensive simulation and benchmarking suite designed to facilitate the development of generalizable, reasoning-capable embodied agents in laboratory settings. Specifically, it integrates i) LabSim, a high-fidelity simulator supporting multi-physics and chemically meaningful interactions; ii) LabScene, a scalable procedural generator for diverse scientific scenes; and iii) LabBench, a hierarchical benchmark spanning five levels of complexity from atomic actions to long-horizon mobile manipulation. LabUtopia supports 30 distinct tasks and includes more than 200 scene and instrument assets, enabling large-scale training and principled evaluation in high-complexity environments. We demonstrate that LabUtopia offers a powerful platform for advancing the integration of perception, planning, and control in scientific-purpose agents and provides a rigorous testbed for exploring the practical capabilities and generalization limits of embodied intelligence in future research. (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that established simulators predominantly focus on household environments rather than on the specific challenges of scientific experimentation. (Li et al., 2025) `ev:cited` p. 2 ^li2025labutopia-001
- Existing simulators cannot model chemical dynamics such as product formation or color changes, according to the authors' comparison in Table 1. (Li et al., 2025) `ev:asserted` p. 2 ^li2025labutopia-002
- In Table 1, LabUtopia is marked as supporting simulation of chemical processes, unlike every other compared simulator or benchmark. (Li et al., 2025) `ev:asserted` p. 4 ^li2025labutopia-003
- LabUtopia integrates three components: LabSim, a simulator; LabScene, a procedural scene generator; and LabBench, a hierarchical benchmark. (Li et al., 2025) `ev:reported` p. 2 ^li2025labutopia-004
- LabSim is a high-fidelity simulation environment built on Isaac Sim for training and evaluating embodied agents in laboratory tasks. (Li et al., 2025) `ev:reported` p. 2 ^li2025labutopia-005
- LabSim's chemical engine models reaction-driven transformations, such as color change and product generation, by combining a substance database with a reasoning model. (Li et al., 2025) `ev:reported` p. 2 ^li2025labutopia-006
- In LabSim, each asset is annotated with empirically grounded physical properties to enable contact and collision modeling. (Li et al., 2025) `ev:reported` p. 4 ^li2025labutopia-007
- Fluid simulation in LabSim uses a GPU-accelerated Position-Based Dynamics framework to support fluid-agent interactions needed for scientific manipulation. (Li et al., 2025) `ev:reported` p. 4 ^li2025labutopia-008
- The chemical engine relies on a structured database of 200 common chemical substances sourced from the PubChem repository. (Li et al., 2025) `ev:reported` p. 4 ^li2025labutopia-009
- Each database substance encodes key attributes such as color, molar mass, and pH value, allowing it to be represented as a simulation asset. (Li et al., 2025) `ev:reported` p. 4 ^li2025labutopia-010
- Given a set of reactants, LabSim uses GPT-4o to reason about potential chemical processes and infer transformations like color changes or product formation. (Li et al., 2025) `ev:reported` p. 4 ^li2025labutopia-011
- Inferred chemical changes are rendered by dynamically updating the physical state and visual properties of the involved substances in the simulation. (Li et al., 2025) `ev:reported` p. 4 ^li2025labutopia-012
- The reaction-inference prompt asks the language model to return only JSON listing reaction type, expected products, observable changes, and a confidence score. (Li et al., 2025) `ev:reported` p. 19 ^li2025labutopia-013
- After consulting chemistry and physics experts on scene fidelity, the authors selected approximately 100 high-quality scenes as LabUtopia's foundational environments. (Li et al., 2025) `ev:reported` p. 5 ^li2025labutopia-014
- The object asset library contains approximately 60 categories of laboratory equipment, such as drying ovens, centrifuges, pipettes, and balances. (Li et al., 2025) `ev:reported` p. 5 ^li2025labutopia-015
- The object asset library also contains over 80 types of transparent glassware and plasticware, including beakers, flasks, test tubes, and Petri dishes. (Li et al., 2025) `ev:reported` p. 5 ^li2025labutopia-016
- According to the abstract, LabUtopia includes more than 200 scene and instrument assets for large-scale training and evaluation. (Li et al., 2025) `ev:abstract` p. 1 ^li2025labutopia-017
- The scene generator places objects sequentially by importance and size, sampling candidate poses from a discretized grid under boundary and collision constraints. (Li et al., 2025) `ev:reported` p. 5 ^li2025labutopia-018
- Candidate layouts are scored on edge proximity, inter-object distance, and orientation alignment, with the highest-scoring configuration selected. (Li et al., 2025) `ev:reported` p. 5 ^li2025labutopia-019
- If random sampling fails to produce a valid layout within a time limit, the generator falls back to a depth-first search over placements. (Li et al., 2025) `ev:reported` p. 5 ^li2025labutopia-020
- Atomic actions such as pouring and stirring are executed by finite state machines within the automatic manipulation trajectory collection. (Li et al., 2025) `ev:reported` p. 6 ^li2025labutopia-021
- At each target keypoint of an atomic action, an RMPflow controller plans arm motion toward positions set by the objects' real-time state. (Li et al., 2025) `ev:reported` p. 6 ^li2025labutopia-022
- Task-level controllers organize atomic action controllers to generate demonstration data for imitation learning across entire experimental procedures. (Li et al., 2025) `ev:reported` p. 6 ^li2025labutopia-023
- Navigation trajectories are collected automatically with the A* algorithm planning over occupancy maps generated by Isaac Sim for each laboratory. (Li et al., 2025) `ev:reported` p. 6 ^li2025labutopia-024
- Occupancy maps mark as occupied all objects with heights between [0.1, 1.6] meters after projecting them onto the ground plane. (Li et al., 2025) `ev:reported` p. 29 ^li2025labutopia-025
- Each pixel in the navigation occupancy map corresponds to a unit length of 0.5 meters in the laboratory scene. (Li et al., 2025) `ev:reported` p. 29 ^li2025labutopia-026
- The collision detection radius used when generating ground-truth navigation paths from sampled start locations is set to 60 cm. (Li et al., 2025) `ev:reported` p. 30 ^li2025labutopia-027
- LabBench organizes its tasks into five levels of increasing complexity, from atomic actions to long-horizon and mobile manipulation tasks. (Li et al., 2025) `ev:reported` p. 7 ^li2025labutopia-028
- Level 2 short-horizon tasks require agents to perform a sequence of 2-3 atomic actions to complete a compound objective. (Li et al., 2025) `ev:reported` p. 7 ^li2025labutopia-029
- Level 3 tests generalization by evaluating agents on unseen object configurations, unfamiliar scene arrangements, or appearance variations after joint training. (Li et al., 2025) `ev:reported` p. 7 ^li2025labutopia-030
- Level 4 tasks, such as preparing a chemical solution, require high-level planning and robustness to compounding execution errors. (Li et al., 2025) `ev:asserted` p. 8 ^li2025labutopia-031
- Level 5 combines navigation with manipulation, requiring agents to traverse large laboratory environments with mobile-base control while manipulating objects. (Li et al., 2025) `ev:reported` p. 8 ^li2025labutopia-032
- Manipulation tasks use a 7-DoF Franka Emika Panda arm with a parallel gripper as the robot embodiment. (Li et al., 2025) `ev:reported` p. 8 ^li2025labutopia-033
- Navigation tasks use the Fetch mobile manipulator and a Clearpath Robotics Ridgeback base carrying a Franka Emika Panda arm. (Li et al., 2025) `ev:reported` p. 8 ^li2025labutopia-034
- During evaluation, objects are randomly placed within a 15 cm × 15 cm region, adjusted to their sizes and workspace constraints. (Li et al., 2025) `ev:reported` p. 8 ^li2025labutopia-035
- A task counts as successful if the goal state stays within tolerance continuously for 2 seconds after the final task stage completes. (Li et al., 2025) `ev:reported` p. 8 ^li2025labutopia-036
- The benchmark evaluates ACT, a CNN-based Diffusion Policy, and the vision-language-action model π0 as imitation learning baselines. (Li et al., 2025) `ev:reported` p. 8 ^li2025labutopia-037
- Manipulation tasks use three cameras, a wrist camera, a front-facing camera, and an overhead camera, each outputting 256×256 RGB images by default. (Li et al., 2025) `ev:reported` p. 9 ^li2025labutopia-038
- ACT and Diffusion Policy were trained for 200 epochs with AdamW on a single NVIDIA RTX 4090 GPU. (Li et al., 2025) `ev:reported` p. 9 ^li2025labutopia-039
- For comparison, the π0 model was implemented using JAX and trained for 30,000 steps on 8 A800 80G GPUs. (Li et al., 2025) `ev:reported` p. 9 ^li2025labutopia-040
- A fixed learning rate of 1 × 10−4 was used throughout training, with batch sizes of 128 for ACT and 64 for Diffusion Policy. (Li et al., 2025) `ev:reported` p. 9 ^li2025labutopia-041
- Action chunk lengths in the benchmark experiments were 60 for ACT, 60 for Diffusion Policy, and 8 for π0. (Li et al., 2025) `ev:reported` p. 9 ^li2025labutopia-042
- On Level-1 atomic tasks, ACT success rates ranged from 71.7 to 96.7 percent across the ten listed tasks. (Li et al., 2025) `ev:measured` p. 8 ^li2025labutopia-043
- On Level-1 atomic tasks, Diffusion Policy success rates ranged from 65.0 to 100.0 percent, with 100.0 on Close Drawer. (Li et al., 2025) `ev:measured` p. 8 ^li2025labutopia-044
- The authors attribute the high Level-1 success rates of both models to the simplicity and single-step nature of those tasks. (Li et al., 2025) `ev:asserted` p. 9 ^li2025labutopia-045
- On the Level-2 Heater Beaker task, ACT reached 86.7 percent success, compared with 25.0 percent for Diffusion Policy. (Li et al., 2025) `ev:measured` p. 8 ^li2025labutopia-046
- On Level-2 Operate Drawer and Stir w/ GlassRod, Diffusion Policy had 10.0 percent success each, versus 73.3 and 55.0 for ACT. (Li et al., 2025) `ev:measured` p. 8 ^li2025labutopia-047
- The authors observed that Diffusion Policy frequently stalled on Level-2 tasks, for example pausing during Heater Beaker's final action until timeout. (Li et al., 2025) `ev:measured` p. 9 ^li2025labutopia-048
- In Stir with GlassRod, both models showed noticeable grasping or stirring position errors, which the authors attribute to the rod's small size. (Li et al., 2025) `ev:measured` p. 9 ^li2025labutopia-049
- On Level-3 Heater Beaker, Diffusion Policy fell to 21.6 percent in-distribution and 8.3 percent out-of-distribution success. (Li et al., 2025) `ev:measured` p. 9 ^li2025labutopia-050
- On Level-3 Transport Beaker, Diffusion Policy dropped from 67.5 percent in-distribution to 15.0 percent out-of-distribution success. (Li et al., 2025) `ev:measured` p. 9 ^li2025labutopia-051
- ACT kept Level-3 out-of-distribution success between 65.0 and 96.7 percent across the six listed generalization tasks. (Li et al., 2025) `ev:measured` p. 9 ^li2025labutopia-052
- Fine-tuned π0 showed small gaps between in-distribution and out-of-distribution success on Level-3 tasks, for example 83.3 versus 85.8 on Pick. (Li et al., 2025) `ev:measured` p. 9 ^li2025labutopia-053
- The authors report that fine-tuned pretrained VLA models did not consistently outperform models trained from scratch on Level-3 tasks. (Li et al., 2025) `ev:measured` p. 9 ^li2025labutopia-054
- On Level-3 Pour Liquid, π0 reached 40.0 and 38.3 percent in-distribution and out-of-distribution success, below ACT's 75.0 and 65.0. (Li et al., 2025) `ev:measured` p. 9 ^li2025labutopia-055
- When jointly trained on objects of very different sizes, ACT's Pick success fell to 31.2 percent in-domain and 1.7 percent out-of-domain. (Li et al., 2025) `ev:measured` p. 9 ^li2025labutopia-056
- Under the same size-variation training, Diffusion Policy reached 0.0 percent out-of-domain success on both Pick and Pour Liquid. (Li et al., 2025) `ev:measured` p. 9 ^li2025labutopia-057
- The authors suggest that both models largely lack the ability to manipulate out-of-domain objects of different shapes and sizes. (Li et al., 2025) `ev:asserted` p. 10 ^li2025labutopia-058
- On Level-4 Clean Beaker, ACT achieved 14.0 percent single-stage primitive success, compared with 2.5 percent for Diffusion Policy. (Li et al., 2025) `ev:measured` p. 10 ^li2025labutopia-059
- In Clean Beaker sub-steps, ACT success fell from 99.3 percent at step A1 to 1.6 percent at step A7. (Li et al., 2025) `ev:measured` p. 10 ^li2025labutopia-060
- Diffusion Policy reached 0.0 percent success from sub-step A4 onward in all three Level-4 long-horizon tasks. (Li et al., 2025) `ev:measured` p. 10 ^li2025labutopia-061
- The authors attribute the sharp declines in later sub-steps A5–A7 to cumulative errors across complex task sequences. (Li et al., 2025) `ev:asserted` p. 10 ^li2025labutopia-062
- The authors hypothesize that Diffusion Policy's shorter prediction horizon makes it more prone to stagnation than ACT. (Li et al., 2025) `ev:asserted` p. 10 ^li2025labutopia-063
- The authors report that Diffusion Policy outputs are more jittery than ACT's, increasing the likelihood of dropping grasped objects. (Li et al., 2025) `ev:asserted` p. 10 ^li2025labutopia-064
- Using two 256×256 cameras on an NVIDIA RTX 4090 GPU, the system runs at 23 fps for liquid simulation. (Li et al., 2025) `ev:measured` p. 17 ^li2025labutopia-065
- The authors conclude that current imitation learning approaches still exhibit significant shortcomings on complex long-horizon laboratory tasks. (Li et al., 2025) `ev:asserted` p. 10 ^li2025labutopia-066
- The authors state as a limitation that the benchmark operates entirely within simulation, leaving the [[Sim-to-real transfer|sim-to-real gap]] for future work. (Li et al., 2025) `ev:asserted` p. 10 ^li2025labutopia-067
- The authors list as a limitation that LabUtopia currently supports only two robot embodiments, Fetch and Panda. (Li et al., 2025) `ev:asserted` p. 10 ^li2025labutopia-068

## 🎯 Contributions

## 📖 Glossary

- **Position-Based Dynamics (PBD)** — Particle simulation method solving positional constraints directly; used here for GPU fluid simulation.
- **ACT** — Transformer policy that predicts chunks of future robot actions from images and proprioception.
- **Diffusion Policy** — Policy generating action trajectories by iteratively denoising random samples conditioned on observations.
- **π0** — Vision-language-action model built on PaliGemma with a flow-matching action expert.
- **RMPflow** — Riemannian motion policy framework composing reactive controllers for robot arm motion generation.
- **Occupancy map** — Grid marking which floor cells are blocked by obstacles, used for path planning.
- **Action chunk** — Sequence of future actions a policy predicts and executes per inference step.
- **Single-stage primitive (SP)** — Level-4 evaluation where one policy executes the whole long-horizon task end to end.

## ❓ Open questions

- How faithful are the GPT-4o-inferred chemical outcomes, and how often does the reasoning model predict wrong products or colors?
- Do policies trained in LabSim transfer to a physical laboratory, given that no sim-to-real experiment is reported?
- Why were Level-4 and Level-5 tasks not evaluated with π0, and how would pretrained VLA models behave on long-horizon tasks?
- How are Level-5 mobile manipulation policies evaluated, since no Level-5 success rates are reported?
- Which training approaches could restore shape and size generalization, given near-zero out-of-domain success in Table 4?
- How accurate is the PBD fluid simulation for volumes and pouring compared with real liquids?

## 📝 Notes on reading

- Version read: arXiv 2505.22634v2 (7 Dec 2025), which states acceptance at NeurIPS 2025; the packet identifier is the arXiv record.
- Task counts are inconsistent: the abstract and contribution list give 30 tasks, the conclusion says more than 30 tasks, and Section 4 says LabBench comprises over 50 tasks (p. 6).
- Asset counts differ: the abstract says more than 200 scene and instrument assets, p. 3 says over 100 scenes and 100 instruments, and p. 5 says approximately 100 scenes plus about 60 equipment categories and over 80 glassware types.
- Section 5.1 says two representative models were selected but lists three (ACT, Diffusion Policy, π0).
- The limitations section says only two embodiments (Fetch and Panda) are supported, while p. 8 and p. 30 also describe a Ridgeback base with a Panda arm.
- Table 5: ACT rows for Clean Beaker and Liquid Fusion share identical A4–A7 values (42.5, 12.3, 10.6, 1.6), which may be a copy error; Table 5 also includes Liquid Fusion, which the appendix task list (Clean Beaker, Drying Beaker) does not describe.
- Table 4 is titled by task level but the text describes it as size-variation training for Pick and Pour Liquid; the setup is only briefly described.
- No Level-5 (mobile manipulation) quantitative results are reported in the main text.
- Figure 1, 2, 3 and 4 are described only (pipeline overviews, navigation maps, task hierarchy); Figure 3's caption skips panel (e). Appendix A.1.1–A.1.3 asset pages contain only image headings in the cached text.
- The ACT description on p. 8 cites reference [18], which is Mobile ALOHA, not the original ACT paper.

## Suggested new concepts

- LLM-based chemical reaction simulation — using a language model plus a property database to drive visual chemistry in simulators recurs across lab-automation work.
- Hierarchical manipulation benchmarks — graded task levels from atomic to long-horizon are a reusable evaluation design for lab robotics.
- Procedural laboratory scene generation — grid sampling with constraint-aware search fallback is directly relevant to building simulated lab scenes.
- Compounding error in long-horizon imitation learning — success collapsing over sub-steps is a central limitation for lab task policies.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H7.** Simulador y benchmark jerárquico de laboratorio (30 tareas, más de 200 activos), comparable a AutoBio y Chemistry3D.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
