---
aliases: []
type: "source"
title: "Chemistry3D: Robotic Interaction Benchmark for Chemistry Experiments"
citekey: "Li2024chemistry3d"
doi: "10.48550/arXiv.2406.08160"
arxiv: "2406.08160"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2406.08160"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Shoujie Li", "Yan Huang", "Changqing Guo", "Tong Wu", "Jiawei Zhang", "Linrui Zhang", "Wenbo Ding"]
sha256: ["f3588e639b4f4960e02caad7f06254b62aff65a0bdc9ba6d8374cc75c457223d"]
pdf: "Content/Papers/Li2024chemistry3d.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Li2024chemistry3d.pdf]]

> [!abstract] One-sentence summary
> Chemistry3D couples a rule-based inorganic and a data-driven organic reaction simulator with an Omniverse/Isaac Sim lab scene, so robots can manipulate containers while color, temperature and pH evolve, and demonstrates it with manipulation, LLM-driven, RL and transparent-object Sim2Real experiments.

## Abstract

The advent of simulation engines has revolutionized learning and operational efficiency for robots, offering cost-effective and swift pipelines. However, the lack of a universal simulation platform tailored for chemical scenarios impedes progress in robotic manipulation and visualization of reaction processes. Addressing this void, we present Chemistry3D, an innovative toolkit that integrates extensive chemical and robotic knowledge. Chemistry3D not only enables robots to perform chemical experiments but also provides real-time visualization of temperature, color, and pH changes during reactions. Built on the NVIDIA Omniverse platform, Chemistry3D offers interfaces for robot operation, visual inspection, and liquid flow control, facilitating the simulation of special objects such as liquids and transparent entities. Leveraging this toolkit, we have devised RL tasks, object detection, and robot operation scenarios. Additionally, to discern disparities between the rendering engine and the real world, we conducted transparent object detection experiments using Sim2Real, validating the toolkit's exceptional simulation performance. The source code is available at https://github.com/huangyan28/Chemistry3D, and a related tutorial can be found at https://www.omni-chemistry.com. (arXiv)

## 🧠 Key ideas (atomic)

- Chemistry3D is presented as a toolkit built on NVIDIA Omniverse that lets robots perform chemical experiments within 3D simulated environments. (Li et al., 2024) `ev:asserted` p. 2 ^li2024chemistry3d-001
- The authors state that a dedicated chemical 3D simulation system for robots had not yet been proposed despite considerable robot simulation research. (Li et al., 2024) `ev:asserted` p. 1 ^li2024chemistry3d-002
- The authors identify immature rendering engines for liquids and transparent objects as one challenge in building a chemical simulator for robots. (Li et al., 2024) `ev:asserted` p. 1 ^li2024chemistry3d-003
- The authors report curating a chemical dataset of over 1,000 inorganic reactions and 100,000 organic reactions for chemical simulation. (Li et al., 2024) `ev:reported` p. 2 ^li2024chemistry3d-004
- The authors state that benchmarking robotic manipulation for chemical experiments in simulation had not been previously addressed by existing work. (Li et al., 2024) `ev:asserted` p. 2 ^li2024chemistry3d-005
- In the comparison table, Chemistry3D and the CFD approach are the tools marked as supporting fluid simulation. (Li et al., 2024) `ev:asserted` p. 3 ^li2024chemistry3d-006
- Compared with the ChemGymRL benchmark, Chemistry3D is said to support realistic scene simulation for visual inputs and physical robot-object interaction. (Li et al., 2024) `ev:asserted` p. 3 ^li2024chemistry3d-007
- The inorganic simulator database includes 65 chemical substances, each characterized by color, enthalpy value and physical state. (Li et al., 2024) `ev:reported` p. 3 ^li2024chemistry3d-008
- The inorganic database also contains 65 fundamental reactions specifying reactants, products and their stoichiometric ratios. (Li et al., 2024) `ev:reported` p. 3 ^li2024chemistry3d-009
- The 65 fundamental reactions in the supplementary database fall into four types: acid-base, double displacement, redox and complexation. (Li et al., 2024) `ev:reported` p. 11 ^li2024chemistry3d-010
- The supplementary chemical table lists 69 types of chemicals and ions, covering all substances involved in the fundamental reactions. (Li et al., 2024) `ev:reported` p. 11 ^li2024chemistry3d-011
- The inorganic simulator accepts input as a dictionary with reactant names as keys and numbers of mole as values. (Li et al., 2024) `ev:reported` p. 4 ^li2024chemistry3d-012
- Through iterative reactions over various combinations, the inorganic simulator is said to generate over 1000 possible reactions. (Li et al., 2024) `ev:asserted` p. 4 ^li2024chemistry3d-013
- The representation output gives the mixture color, enthalpy change, pH, temperature change and the physical state of resulting substances. (Li et al., 2024) `ev:reported` p. 4 ^li2024chemistry3d-014
- The initial simulation step verifies that input reactants satisfy charge conservation, to confirm the set of reactants is realistic. (Li et al., 2024) `ev:reported` p. 4 ^li2024chemistry3d-015
- Complex inorganic reactions are broken down into basic reactions executed in an order set by their sequential record in the database. (Li et al., 2024) `ev:reported` p. 4 ^li2024chemistry3d-016
- The simulator identifies which ion is completely consumed first, establishing the limiting reagent that sets the reaction quantity. (Li et al., 2024) `ev:reported` p. 4 ^li2024chemistry3d-017
- Intermediate states are computed from a rate equation simplified to unit reaction order, giving an offset exponential decay over time. (Li et al., 2024) `ev:reported` p. 4 ^li2024chemistry3d-018
- The total enthalpy change is computed by multiplying the reaction quantity by the per-equation enthalpy change recorded in the database. (Li et al., 2024) `ev:reported` p. 5 ^li2024chemistry3d-019
- Temperature change is computed from the reaction heat divided by specific heat capacity of the solvent, solution density and solution volume. (Li et al., 2024) `ev:reported` p. 5 ^li2024chemistry3d-020
- Solution transparency is calculated from reactant and product concentration using an exponential model derived from solution dilution. (Li et al., 2024) `ev:reported` p. 5 ^li2024chemistry3d-021
- In the color calculation, a substance in the solid state contributes to opacity, resulting in a turbid liquid. (Li et al., 2024) `ev:reported` p. 5 ^li2024chemistry3d-022
- A negative mixing model is applied to determine the resultant color of solutions that contain no solid substance. (Li et al., 2024) `ev:reported` p. 5 ^li2024chemistry3d-023
- The simulator can convert UV/Vis spectrum information into RGB color values for visual display in the simulation. (Li et al., 2024) `ev:reported` p. 5 ^li2024chemistry3d-024
- For a blackbody radiator emission spectrum at 1000K, the spectrum-to-color conversion of the simulator yields the RGB color (255,2,0). (Li et al., 2024) `ev:computed` p. 15 ^li2024chemistry3d-025
- pH calculation interpolates the ionization constant of water from a table covering 0 to 100 degrees Celsius at standard atmospheric pressure. (Li et al., 2024) `ev:reported` p. 5 ^li2024chemistry3d-026
- The pH step ignores ionization of weak electrolytes and focuses on hydrogen or hydroxide ions from strong electrolytes. (Li et al., 2024) `ev:reported` p. 5 ^li2024chemistry3d-027
- The organic simulator draws reaction information from RXN for Chemistry and substance information from ChemSpider. (Li et al., 2024) `ev:reported` p. 5 ^li2024chemistry3d-028
- The organic simulator accepts reactants represented as SMILES strings and outputs the corresponding products for reaction product prediction. (Li et al., 2024) `ev:reported` p. 5 ^li2024chemistry3d-029
- The organic simulator is also described as capable of predicting reaction yields, which determines the component output for a reaction. (Li et al., 2024) `ev:reported` p. 5 ^li2024chemistry3d-030
- The simulator is wrapped in a container class with three methods: initialization, updating and information retrieval. (Li et al., 2024) `ev:reported` p. 6 ^li2024chemistry3d-031
- The updating method simulates sampling or mixing and outputs intermediate states via rate equations with an adjustable time step. (Li et al., 2024) `ev:reported` p. 6 ^li2024chemistry3d-032
- Chemical containers shown with a green background in the environment figure were 3D scanned from real objects. (Li et al., 2024) `ev:reported` p. 6 ^li2024chemistry3d-033
- Chemistry3D inherits support from Isaac-Sim, including integration with ROS and ROS2 for robot control within the chemical environment. (Li et al., 2024) `ev:reported` p. 7 ^li2024chemistry3d-034
- The inorganic experiments used potassium permanganate with ferrous chloride, and hydrochloric acid with iron(II) oxide. (Li et al., 2024) `ev:reported` p. 8 ^li2024chemistry3d-035
- The center of mass of the reactants determines contact points that trigger color and state transformations in the inorganic experiments. (Li et al., 2024) `ev:reported` p. 8 ^li2024chemistry3d-036
- Chemistry3D outputs temperature, enthalpy change and pH at each time step during the inorganic experiments. (Li et al., 2024) `ev:reported` p. 8 ^li2024chemistry3d-037
- Significant color changes were observed in the simulated reaction between potassium permanganate and ferrous chloride in Chemistry3D. (Li et al., 2024) `ev:measured` p. 15 ^li2024chemistry3d-038
- The authors report that the simulated reaction between hydrochloric acid and iron(II) oxide exhibited solid dissolution in Chemistry3D. (Li et al., 2024) `ev:measured` p. 15 ^li2024chemistry3d-039
- The authors state that detailed reaction progress information is available only for inorganic reactions, not for organic ones. (Li et al., 2024) `ev:reported` p. 15 ^li2024chemistry3d-040
- In the terminal output, reactant amounts fall from 10.0 to 3.207 as the brominated pyrene product rises to 13.586. (Li et al., 2024) `ev:computed` p. 15 ^li2024chemistry3d-041
- The organic experiment simulated the bromine and pyrene reaction, synchronizing chemical simulation with robotic arm simulation step by step. (Li et al., 2024) `ev:reported` p. 16 ^li2024chemistry3d-042
- A Controller Manager class manages modular picking, pouring, shaking, stirring and placing operations to ensure their sequential execution. (Li et al., 2024) `ev:reported` p. 8 ^li2024chemistry3d-043
- Picking, pouring and placing operations were successfully combined through the Controller Manager in the manipulation experiment. (Li et al., 2024) `ev:measured` p. 8 ^li2024chemistry3d-044
- Placing is decomposed into five stages: vertical ascent, horizontal translation, vertical descent, gripper release and a final vertical ascent. (Li et al., 2024) `ev:reported` p. 17 ^li2024chemistry3d-045
- The semantic segmentation dataset contains 13,731 images with 1.5k backgrounds and 7 types of transparent objects. (Li et al., 2024) `ev:reported` p. 19 ^li2024chemistry3d-046
- The object detection dataset contains 6547 images with 1.2k backgrounds and 7 types of transparent objects. (Li et al., 2024) `ev:reported` p. 19 ^li2024chemistry3d-047
- The datasets were produced from seven real transparent objects scanned in 3D, with glass material applied in Omniverse. (Li et al., 2024) `ev:reported` p. 19 ^li2024chemistry3d-048
- Three light sources illuminated the objects, with light number, intensity and color temperature adjusted to maximize reflective spots. (Li et al., 2024) `ev:reported` p. 20 ^li2024chemistry3d-049
- EfficientNet with DeepLabV3 obtained the highest scores, with IoU 0.7582, pixel accuracy 0.9917, F1 0.8558 and F2 0.8112. (Li et al., 2024) `ev:measured` p. 8 ^li2024chemistry3d-050
- The ResNet encoder with a Unet decoder reached IoU 0.7097, pixel accuracy 0.9902, F1 0.8181 and F2 0.7813. (Li et al., 2024) `ev:measured` p. 8 ^li2024chemistry3d-051
- The VGG encoder with a Unet++ decoder reached IoU 0.6963, pixel accuracy 0.9896, F1 0.8056 and F2 0.7494. (Li et al., 2024) `ev:measured` p. 8 ^li2024chemistry3d-052
- Networks trained in simulation are reported to keep robust segmentation across simple and complex backgrounds in real-world scenes. (Li et al., 2024) `ev:measured` p. 20 ^li2024chemistry3d-053
- A YOLO model trained in simulation was evaluated for object detection in both simulated and real-world environments. (Li et al., 2024) `ev:reported` p. 8 ^li2024chemistry3d-054
- The authors state that YOLO detection results are consistent with the segmentation results, confirming Chemistry3D supports visual Sim2Real. (Li et al., 2024) `ev:asserted` p. 9 ^li2024chemistry3d-055
- For embodied intelligence, the scene contained containers of KMnO4 and FeCl2 plus two empty beakers on a table. (Li et al., 2024) `ev:reported` p. 21 ^li2024chemistry3d-056
- Based on the Chemistry3D chemical knowledge base, the robot can predict potential chemical reactions among observed substances. (Li et al., 2024) `ev:reported` p. 9 ^li2024chemistry3d-057
- Upon human task directives, the robot uses a Large Language Model to generate and plan the necessary operations. (Li et al., 2024) `ev:reported` p. 9 ^li2024chemistry3d-058
- The picking RL task used PPO with 2048 environments, 3500 epochs and a learning rate of 5 × 10−4. (Li et al., 2024) `ev:reported` p. 8 ^li2024chemistry3d-059
- The RL training configuration was applied across three separate realizations, with curves showing their mean and standard deviation. (Li et al., 2024) `ev:reported` p. 22 ^li2024chemistry3d-060
- The authors state the results confirmed that robotic arms could successfully grasp chemical containers within Chemistry3D. (Li et al., 2024) `ev:asserted` p. 9 ^li2024chemistry3d-061
- The authors conclude the system enhances visualization and interactivity of chemical experiments and offers a tool for interdisciplinary research. (Li et al., 2024) `ev:asserted` p. 9 ^li2024chemistry3d-062

## 🎯 Contributions


## 📖 Glossary

- **Sim2Real** — transferring models trained in simulation directly to real-world data or robots.
- **Omniverse / Isaac Sim** — NVIDIA simulation platform and its robotics simulator used to build Chemistry3D.
- **SMILES** — line-notation strings encoding molecular structure, used as organic simulator input.
- **Limiting reagent** — reactant consumed first, which caps how much reaction occurs.
- **Reaction quantity** — number of moles of the reaction equation that proceed.
- **Negative color mixing** — subtractive model combining absorbing solution colors into a resultant color.
- **IoU** — intersection over union between predicted and true segmentation masks.
- **PPO** — Proximal Policy Optimization, a policy-gradient reinforcement learning algorithm.
- **Controller Manager** — class sequencing modular manipulation controllers such as pick, pour and place.

## ❓ Open questions

- How close are simulated temperature, color and pH trajectories to measurements of the same reactions in a real lab?
- Were the Table 2 segmentation metrics computed on simulated or real-world test images, and how large is the sim-to-real gap numerically?
- What quantitative detection accuracy did the simulation-trained YOLO model reach on real images?
- What final success rate did the PPO picking policy reach, and do pouring or stirring tasks train as well?
- How are rate constants chosen for intermediate states, and how sensitive are visualized dynamics to that choice?
- Where do the claimed 100,000 organic reactions come from, given the organic simulator relies on RXN for Chemistry queries?
- How are fluid volumes in the particle simulation coupled to the amounts used by the chemistry simulator?

## 📝 Notes on reading

Version read: arXiv v1 (2406.08160v1, 12 Jun 2024), matching the packet identifier; the supplementary material is pages 10 to 22 of the same file.

Inconsistencies inside the paper:
- Section 3.1 (p. 3) says the database holds 65 chemical substances, while the supplement (p. 11) says 69 types of chemicals and ions; the chemical table lists K+ twice (entries 11 and 49).
- The contributions (p. 2) claim over 1,000 inorganic and 100,000 organic reactions, but the inorganic database has 65 fundamental reactions (over 1000 only via iterative combinations, p. 4) and the 100,000 organic figure is not substantiated in the body.
- Section 3.3 (p. 7) says four common operations were selected but lists five (picking, placing, pouring, stirring, shaking).
- The KMnO4 plus FeCl2 equation differs between Fig. 6 (2KMnO4+10FeCl2+16HCl, p. 15) and the LLM answer in Fig. 12 (2KMnO4+6FeCl2+8HCl, p. 21); the Fig. 6 equation does not balance iron (10 Fe on the left, 5 FeCl3 on the right).
- In the organic terminal output (p. 15) the product amount rises by twice the reactant decrease (10.0 to 3.207 for Br2 and pyrene, product 0 to 13.586) although the written equation is 1:1.
- Supplementary table numbering collides with the main text (Table 3 Reactions, then Table 1 Reactions, Table 2 Chemicals, Table 3 RL parameters); the related-work text writes Chenaxon while the table writes Chemaxon; Cu2+ and Ag+ are listed with state s.
- Table 2 (p. 8) does not say whether the metrics were measured on simulated or real test images.

Figures only described: Fig. 10 and Fig. 11 (qualitative Sim2Real segmentation and detection examples) and Fig. 13 (RL reward and success-rate curves) give no numbers in the text; no RL success rate or YOLO metric was claimed. The Table 1 comparison matrix was extracted as a flat column of ticks; only the fluid-simulation row was claimed after reading it by column order. Equation 10 in the supplement is garbled in extraction.

## Suggested new concepts

- Chemistry-aware robot simulation — couples reaction state (color, heat, pH) to physical manipulation, a distinct design axis for lab-automation simulators.
- Sim2Real for transparent labware — synthetic glassware datasets with randomized lighting recur as a data strategy for lab perception.
- Modular manipulation primitives for lab tasks — pick, pour, stir, shake and place controllers sequenced by a manager are a reusable pattern for lab robots.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Otro benchmark de automatización de laboratorio

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
