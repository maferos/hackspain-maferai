---
aliases: []
type: "source"
title: "AutoBio: A Simulation and Benchmark for Robotic Automation in Digital Biology Laboratory"
citekey: "Lan2025autobio"
doi: "10.48550/arXiv.2505.14030"
arxiv: "2505.14030"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2505.14030"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Zhiqian Lan", "Yuxuan Jiang", "Ruiqi Wang", "Xuanbing Xie", "Rongkui Zhang", "Yicheng Zhu", "Peihang Li", "Tianshuo Yang", "Tianxing Chen", "Haoyu Gao", "Xiaokang Yang", "Xuelong Li", "Hongyuan Zhang", "Yao Mu", "Ping Luo"]
sha256: ["987d557fe26642e96a1d4c9b3021c3d373717d4a5bc3f9eae48b5bc9de84df91"]
pdf: "Content/Papers/Lan2025autobio.pdf"
topics: ["[[Optimización y algoritmos]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 66
---

📄 PDF: [[Lan2025autobio.pdf]]

> [!abstract] One-sentence summary
> AutoBio extends MuJoCo with digitized lab instruments, lab-specific physics plugins and Blender PBR rendering to build a 16-task biology-lab benchmark, on which fine-tuned π0 and RDT fail most precision, instruction-following and visual-reasoning tasks.

## Abstract

Vision-language-action (VLA) models have shown promise as generalist robotic policies by jointly leveraging visual, linguistic, and proprioceptive modalities to generate action trajectories. While recent benchmarks have advanced VLA research in domestic tasks, professional science-oriented domains remain underexplored. We introduce AutoBio, a simulation framework and benchmark designed to evaluate robotic automation in biology laboratory environments--an application domain that combines structured protocols with demanding precision and multimodal interaction. AutoBio extends existing simulation capabilities through a pipeline for digitizing real-world laboratory instruments, specialized physics plugins for mechanisms ubiquitous in laboratory workflows, and a rendering stack that support dynamic instrument interfaces and transparent materials through physically based rendering. Our benchmark comprises biologically grounded tasks spanning three difficulty levels, enabling standardized evaluation of language-guided robotic manipulation in experimental protocols. We provide infrastructure for demonstration generation and seamless integration with VLA models. Baseline evaluations with two SOTA VLA models reveal significant gaps in precision manipulation, visual reasoning, and instruction following in scientific workflows. By releasing AutoBio, we aim to catalyze research on generalist robotic systems for complex, high-precision, and multimodal professional environments. The simulator and benchmark are publicly available to facilitate reproducible research. (arXiv)

## 🧠 Key ideas (atomic)

- AutoBio is a simulation framework and benchmark designed to evaluate robotic automation in biology laboratory environments. (Lan et al., 2025) `ev:asserted` p. 1 ^lan2025autobio-001
- The authors state that current VLA benchmarks remain largely confined to domestic settings, leaving a gap for science-oriented scenarios. (Lan et al., 2025) `ev:asserted` p. 1 ^lan2025autobio-002
- The authors identify transparent liquids and containers as complicating visual reasoning for robots in biology laboratory tasks. (Lan et al., 2025) `ev:asserted` p. 2 ^lan2025autobio-003
- The authors state that existing simulators lack specialized capabilities required for biological experimentation beyond out-of-the-box contact-based rigid body interactions. (Lan et al., 2025) `ev:asserted` p. 2 ^lan2025autobio-004
- Real-world instruments are converted into manipulable AutoBio assets through 3D Gaussian Splatting, CAD refinement, and texture baking. (Lan et al., 2025) `ev:reported` p. 2 ^lan2025autobio-005
- The authors develop MuJoCo plugins for thread, detent and eccentric mechanisms plus quasi-static liquid computation, rarely addressed in existing simulators. (Lan et al., 2025) `ev:reported` p. 2 ^lan2025autobio-006
- The authors state conventional blend-mode rasterization engines handle transparency poorly, motivating integration with Blender's physically based rendering pipeline. (Lan et al., 2025) `ev:asserted` p. 2 ^lan2025autobio-007
- Table 1 marks AutoBio as supporting interactive instruments and reactive displays, which the other listed benchmarks lack. (Lan et al., 2025) `ev:reported` p. 3 ^lan2025autobio-008
- Table 1 lists AutoBio with 16 tasks in the biology domain, using Blender as its render backend. (Lan et al., 2025) `ev:reported` p. 3 ^lan2025autobio-009
- The authors evaluate two open-source VLA models, π0 and RDT, on tasks across three difficulty levels. (Lan et al., 2025) `ev:reported` p. 3 ^lan2025autobio-010
- AutoBio assets are grouped into four classes, instruments, containers, racks, and robots, as listed in Table 2. (Lan et al., 2025) `ev:reported` p. 4 ^lan2025autobio-011
- The digitization pipeline begins with multi-view video capture of real instruments, then applies the PGSR algorithm to reconstruct 3DGS assets. (Lan et al., 2025) `ev:reported` p. 4 ^lan2025autobio-012
- Raw meshes from 3DGS are refined in CAD software into simplified, watertight low-poly models that preserve critical geometric features. (Lan et al., 2025) `ev:reported` p. 4 ^lan2025autobio-013
- AutoBio uses MuJoCo as its physics engine to simulate rigid-body dynamics among robots, labware, and instruments. (Lan et al., 2025) `ev:reported` p. 4 ^lan2025autobio-014
- The thread plugin replaces meshes in thread collision computation with the signed distance function of a circular helix. (Lan et al., 2025) `ev:reported` p. 5 ^lan2025autobio-015
- The paper provides an approximation to the signed distance function of an unbounded helix, since no analytical solution exists. (Lan et al., 2025) `ev:computed` p. 5 ^lan2025autobio-016
- The detent mechanism provides tactile feedback through a passive spring force based on displacement from the nearest gear position. (Lan et al., 2025) `ev:reported` p. 5 ^lan2025autobio-017
- The eccentric plugin produces orbital motion for mixers such as vortex mixers through negatively coupled rotations about two parallel axes. (Lan et al., 2025) `ev:reported` p. 5 ^lan2025autobio-018
- The quasi-static liquid module treats the liquid surface as a planar interface, neglecting wave propagation and pouring effects. (Lan et al., 2025) `ev:reported` p. 5 ^lan2025autobio-019
- Liquid deformation is described by two states, the liquid level height and the surface normal vector of the planar interface. (Lan et al., 2025) `ev:reported` p. 5 ^lan2025autobio-020
- Surface normal motion follows a damped spherical pendulum responding to external container acceleration, derived with the Euler-Lagrange equation. (Lan et al., 2025) `ev:computed` p. 5 ^lan2025autobio-021
- Liquid surface height is computed through a volume conservation constraint, refined by Newton-Bisect search from the previous height. (Lan et al., 2025) `ev:reported` p. 13 ^lan2025autobio-022
- MuJoCo's native OpenGL renderer can produce artifacts with nested transparent objects such as tubes containing liquids, due to depth sorting errors. (Lan et al., 2025) `ev:asserted` p. 6 ^lan2025autobio-023
- The advanced renderer bridges MuJoCo simulation state to Blender, using PBR shaders for transparent polyethylene, glass, and liquids. (Lan et al., 2025) `ev:reported` p. 6 ^lan2025autobio-024
- The AutoBio benchmark consists of 16 tasks categorized into three difficulty levels with increasing precision, language, and visual demands. (Lan et al., 2025) `ev:reported` p. 6 ^lan2025autobio-025
- Each task includes scene randomization, demonstration synthesis, status checking, and VLA model interfacing with prompts, proprioception, actions, and cameras. (Lan et al., 2025) `ev:reported` p. 7 ^lan2025autobio-026
- The benchmark supports Aloha arms and UR5e arms, the latter with Robotiq 2F-85 gripper or DexHand 021 end-effectors. (Lan et al., 2025) `ev:reported` p. 7 ^lan2025autobio-027
- A simplified DexHand mode fixes most degrees of freedom, actuating only the thumb MCP joint to mimic gripper open/close action. (Lan et al., 2025) `ev:reported` p. 7 ^lan2025autobio-028
- The experiments use 3 tasks per difficulty level, each with 100 demonstration trajectories generated at 50 Hz as LeRobot datasets. (Lan et al., 2025) `ev:reported` p. 7 ^lan2025autobio-029
- The total training set exceeds 792k frames of data, equivalent to 4.4 hours of continuous recording. (Lan et al., 2025) `ev:reported` p. 7 ^lan2025autobio-030
- Each configuration was trained with three seeded runs of 30000 steps at batch size 32, on 100 or 20 episodes. (Lan et al., 2025) `ev:reported` p. 8 ^lan2025autobio-031
- Total training runtime was approximately 1,500 GPU hours, with single runs taking 10 to 14 hours on an NVIDIA H800. (Lan et al., 2025) `ev:reported` p. 8 ^lan2025autobio-032
- For the Operate thermal mixer panel task, a weighted relative progress score over three parameters replaces binary success scoring. (Lan et al., 2025) `ev:reported` p. 16 ^lan2025autobio-033
- With 100 demonstrations, RDT scored 100.0 ± 0.0 on Close thermal cycler lid, versus 99.7 ± 0.3 for π0. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-034
- On Pick up centrifuge tube with 100 demonstrations, π0 scored 53.7 ± 5.9, versus 57.7 ± 1.2 for RDT. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-035
- With 100 demonstrations, π0 reached 42.7 ± 1.8 on Aspirate with pipette, whereas RDT reached 0.3 ± 0.3. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-036
- On Transfer centrifuge tube with 100 demonstrations, π0 scored 40.7 ± 5.4, compared with 2.0 ± 1.2 for RDT. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-037
- On Unscrew centrifuge tube cap with 100 demonstrations, π0 scored 21.3 ± 1.5 versus 2.7 ± 1.2 for RDT. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-038
- On Operate thermal mixer panel with 100 demonstrations, π0 scored 7.5 ± 0.6, versus 1.6 ± 0.5 for RDT. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-039
- On Screw on centrifuge tube cap with 100 demonstrations, RDT scored 8.3 ± 4.4 versus 2.0 ± 0.6 for π0. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-040
- On Load centrifuge rotor with 100 demonstrations, π0 reached 14.7 ± 1.3, versus 1.0 ± 1.0 for RDT. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-041
- RDT shows more consistent performance than π0 on the easy-level tasks in the AutoBio Table 3 evaluations. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-042
- The authors suggest π0's advantage in hard tasks likely stems from joint attention across modalities and fully trainable weights, unlike RDT's static pretrained encoders. (Lan et al., 2025) `ev:asserted` p. 8 ^lan2025autobio-043
- π0 benefits from more demonstration data across most AutoBio tasks when training grows from 20 to 100 episodes. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-044
- RDT shows limited improvement when its training data grows from 20 to 100 demonstration episodes per task. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-045
- The authors attribute the scaling difference to π0's 3B trainable parameters being data-hungry, whereas RDT's frozen backbones constrain its learning capacity. (Lan et al., 2025) `ev:asserted` p. 8 ^lan2025autobio-046
- Easy task failures primarily involve gripper slippage, according to the authors' analysis of the evaluation results. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-047
- Medium and hard tasks reveal precision limitations in the imitation learning approach of current VLAs, according to the authors. (Lan et al., 2025) `ev:asserted` p. 8 ^lan2025autobio-048
- The authors suggest compounding errors in screwing and unscrewing highlight the need to explore reinforcement learning for closed-loop performance. (Lan et al., 2025) `ev:asserted` p. 8 ^lan2025autobio-049
- In Transfer centrifuge tube, policies frequently select incorrect slots, which the authors take as a language understanding limitation. (Lan et al., 2025) `ev:measured` p. 8 ^lan2025autobio-050
- In Operate thermal mixer panel, low input resolutions obscure display numbers, which the authors link to more oscillating loss curves. (Lan et al., 2025) `ev:asserted` p. 8 ^lan2025autobio-051
- The authors suggest the need for a more efficient high-resolution vision processing pipeline for VLA models. (Lan et al., 2025) `ev:asserted` p. 8 ^lan2025autobio-052
- Current memoryless VLA architectures face difficulty when reasoning targets leave the camera view, according to the authors. (Lan et al., 2025) `ev:asserted` p. 9 ^lan2025autobio-053
- The authors indicate a need for visual chain-of-thought reasoning plus memory mechanisms to maintain execution consistency. (Lan et al., 2025) `ev:asserted` p. 9 ^lan2025autobio-054
- The concatenation experiment combines 200 Close and Open thermal cycler lid episodes, switching prompts after each subtask completes. (Lan et al., 2025) `ev:reported` p. 9 ^lan2025autobio-055
- After training on mixed Close and Open data, RDT scored 98.7 ± 0.3 on Close versus 88.0 ± 3.2 on Open. (Lan et al., 2025) `ev:measured` p. 9 ^lan2025autobio-056
- After mixed-data training, π0 scored 100.0 ± 0.0 on Close versus 96.0 ± 0.6 on Open thermal cycler lid. (Lan et al., 2025) `ev:measured` p. 9 ^lan2025autobio-057
- In trajectory concatenation, π0 scored 87.3 ± 2.7 on Open-Close, whereas RDT scored 8.7 ± 2.2. (Lan et al., 2025) `ev:measured` p. 9 ^lan2025autobio-058
- Close-Open concatenation mostly failed, with a score of 3.0 ± 1.2 for π0 versus 4.3 ± 2.8 for RDT. (Lan et al., 2025) `ev:measured` p. 9 ^lan2025autobio-059
- The authors attribute Close-Open failures to handle grip orientation differences in demonstrations at the transition location. (Lan et al., 2025) `ev:asserted` p. 9 ^lan2025autobio-060
- The authors suggest current VLAs primarily memorize trajectories during fine-tuning, with limited ability to transition between related tasks. (Lan et al., 2025) `ev:asserted` p. 9 ^lan2025autobio-061
- Blender Cycles rendering is ∼100× slower than the MuJoCo renderer, which the authors identify as a computational bottleneck. (Lan et al., 2025) `ev:reported` p. 9 ^lan2025autobio-062
- The authors state high-resolution perception may be critical for fine-grained manipulation, as the thermal mixer panel task reveals. (Lan et al., 2025) `ev:asserted` p. 9 ^lan2025autobio-063
- Manual effort for asset digitization and protocol design limits the diversity of instruments and workflows in AutoBio. (Lan et al., 2025) `ev:asserted` p. 9 ^lan2025autobio-064
- AutoBio's physics models and rendering may not fully capture the stochasticity and perceptual noise of real-world labs. (Lan et al., 2025) `ev:asserted` p. 9 ^lan2025autobio-065
- For π0, dual-arm tasks, particularly the two screw operations, tend to overfit more easily when trained on limited data. (Lan et al., 2025) `ev:measured` p. 17 ^lan2025autobio-066

## 🎯 Contributions

## 📖 Glossary

- **VLA model** — Vision-language-action policy mapping images, language and proprioception to robot actions.
- **3D Gaussian Splatting (3DGS)** — Scene representation built from Gaussian primitives, reconstructed from multi-view images.
- **Signed distance function (SDF)** — Implicit geometry giving each point's distance to a shape boundary.
- **Detent mechanism** — Mechanism with discrete click positions held by a restoring spring force.
- **Eccentric mechanism** — Off-axis rotation producing oscillating orbital motion, as in vortex mixers.
- **Quasi-static liquid** — Liquid model with a planar surface, ignoring waves and pouring.
- **Physically based rendering (PBR)** — Rendering grounded in real light behavior, handling transmission and refraction.
- **MJCF** — MuJoCo's XML format describing models, bodies, joints and assets.
- **TOPP** — Time-optimal path parameterization for dynamically feasible trajectory timing.
- **Trajectory concatenation** — Chaining separately trained subtasks by switching prompts after each completes.

## ❓ Open questions

- How well do policies trained in AutoBio transfer to real biology laboratory robots?
- Would reinforcement learning or closed-loop fine-tuning close the gap on screwing and unscrewing tasks?
- How much would high-resolution vision inputs improve the thermal mixer panel and liquid-level tasks?
- Does the quasi-static liquid approximation suffice for tasks involving pouring or fast liquid motion?
- Can generative asset and task synthesis scale instrument diversity without manual digitization effort?
- Would memory or visual chain-of-thought mechanisms fix failures when targets leave the camera view?
- How do the full 16 tasks, beyond the 9 evaluated, rank for current VLA models?

## 📝 Notes on reading

Read arXiv 2505.14030v3 (29 May 2025), matching the packet identifier; the preprint is marked as under review. Figures 1, 2, 4, 5 and 6 (framework diagram, digitization pipeline, rendering backends, task progression, asset overview) could only be described. Figures 7-9 (loss curves) were read only through the appendix bullet observations. The bounded-helix SDF (p. 12), the eccentric transformation matrix (p. 12) and the pendulum ODEs (p. 13) are partly garbled in extraction and were not claimed beyond their qualitative description. On p. 13 the normal component is printed as z = -cos ϕ, which looks like a typo for θ given x and y. The benchmark has 16 tasks but only 9 were evaluated; the other 7 tasks are not described. RDT's hard-level scores sometimes drop with more data (Load centrifuge rotor 1.7 to 1.0), consistent with its limited scaling. The Operate thermal mixer panel score is a relative progress score, not a success rate, so it is not directly comparable to the other cells of Table 3. Further details not claimed to keep volume down: helix SDF advantages over coupled hinge-slide joints (p. 12), IK/TOPP demonstration synthesis with PD control (p. 14), evaluation time limits extended by about 50 % (p. 16), Table 5 model differences (p. 16) and smoother π0 loss curves (p. 17).

## Suggested new concepts

- Digital twin of laboratory instruments — AutoBio's 3DGS-to-CAD-to-MJCF pipeline is a reusable method for lab simulation assets.
- Quasi-static liquid simulation — a cheap liquid approximation relevant to any lab-manipulation simulator on rigid-body engines.
- VLA benchmarks for scientific laboratories — AutoBio positions science labs as a distinct evaluation domain from household manipulation.
- Helix SDF thread contact — a technique for simulating screw caps and threaded parts in MuJoCo.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Origen de la escena y de la evaluación de VLAs en laboratorio (contexto, F).
- **[[03_aplicaciones_vision_por_computador]]** — Base de la escena. Muestra que la precisión es el cuello de botella de los VLA
