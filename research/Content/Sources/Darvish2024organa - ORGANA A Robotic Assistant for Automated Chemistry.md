---
aliases: []
type: "source"
title: "ORGANA: A Robotic Assistant for Automated Chemistry Experimentation and Characterization"
citekey: "Darvish2024organa"
doi: "10.48550/arXiv.2401.06949"
arxiv: "2401.06949"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2401.06949"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Kourosh Darvish", "Marta Skreta", "Yuchi Zhao", "Naruki Yoshikawa", "Sagnik Som", "Miroslav Bogdanovic", "Yang Cao", "Han Hao", "Haoping Xu", "Alán Aspuru-Guzik", "Animesh Garg", "Florian Shkurti"]
sha256: ["ad20624cddfee3802a50776cbe2a63006f59f7c216444fb76459445aa69e6331"]
pdf: "Content/Papers/Darvish2024organa.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 65
---

📄 PDF: [[Darvish2024organa.pdf]]

> [!abstract] One-sentence summary
> Organa couples LLM-based dialogue with chemists, transparent-object perception and joint task-motion-scheduling planning to run solubility, recrystallization, pH and automated-polishing electrochemistry experiments on a Franka arm, cutting chemist involvement time and execution time.

## Abstract

Chemistry experiments can be resource- and labor-intensive, often requiring manual tasks like polishing electrodes in electrochemistry. Traditional lab automation infrastructure faces challenges adapting to new experiments. To address this, we introduce ORGANA, an assistive robotic system that automates diverse chemistry experiments using decision-making and perception tools. It makes decisions with chemists in the loop to control robots and lab devices. ORGANA interacts with chemists using Large Language Models (LLMs) to derive experiment goals, handle disambiguation, and provide experiment logs. ORGANA plans and executes complex tasks with visual feedback, while supporting scheduling and parallel task execution. We demonstrate ORGANA's capabilities in solubility, pH measurement, recrystallization, and electrochemistry experiments. In electrochemistry, it executes a 19-step plan in parallel to characterize quinone derivatives for flow batteries. Our user study shows ORGANA reduces frustration and physical demand by over 50%, with users saving an average of 80.3% of their time when using it. (arXiv)

## 🧠 Key ideas (atomic)

- Organa is presented as an assistive robotic suite of interaction, perception, and decision-making tools that continues the authors' earlier CLAIRify system. (Darvish et al., 2024) `ev:asserted` p. 2 ^darvish2024organa-001
- The authors demonstrate Organa on four fundamental chemistry experiments: solubility screening, recrystallization, pH experimentation, and electrochemistry characterization. (Darvish et al., 2024) `ev:reported` p. 2 ^darvish2024organa-002
- Unlike CLAIRify, which reasons over only a single experiment, Organa reasons over the chemist's instructions to plan multiple experiments to run. (Darvish et al., 2024) `ev:asserted` p. 3 ^darvish2024organa-003
- Organa enables parallel task execution by solving TAMP and scheduling problems together, whereas CLAIRify only supports sequential execution. (Darvish et al., 2024) `ev:asserted` p. 3 ^darvish2024organa-004
- Organa solves task and motion planning together with scheduling by adapting the PDDLStream algorithm to certify parallel execution by multiple agents. (Darvish et al., 2024) `ev:reported` p. 3 ^darvish2024organa-005
- CLAIRify, the authors' prior work, uses GPT-3.5 to translate natural language experiments into XDL through iterative prompting for syntactic correctness. (Darvish et al., 2024) `ev:cited` p. 3 ^darvish2024organa-006
- Organa assessed the solubility of salt, sugar, and alum in water with accuracy values of 7.2%, 11.2%, and 12.3% against literature. (Darvish et al., 2024) `ev:measured` p. 5 ^darvish2024organa-007
- The authors attribute the main solubility error to robot pouring accuracy, arising from delayed response and limited resolution of scale and motor. (Darvish et al., 2024) `ev:asserted` p. 5 ^darvish2024organa-008
- For each solubility test, the robot and hardware executed a 7-step plan, with each test taking an average of 25.63 minutes. (Darvish et al., 2024) `ev:measured` p. 5 ^darvish2024organa-009
- The alum recrystallization experiment was performed by the robot and hardware as a 8-step plan with an execution time of 44.80 mins. (Darvish et al., 2024) `ev:measured` p. 5 ^darvish2024organa-010
- The red cabbage pH indicator demonstration was performed by executing a 6-step plan with a duration of 3.85 minutes. (Darvish et al., 2024) `ev:measured` p. 5 ^darvish2024organa-011
- In the electrochemistry experiment, the system measured the redox potential of a quinone solution at different pH levels to build a Pourbaix diagram. (Darvish et al., 2024) `ev:reported` p. 5 ^darvish2024organa-012
- The electrochemistry solution was a mixture of 2 mM sodium anthraquinone-2-sulfonate, 0.1 M NaCl, and 0.1 M buffer solution. (Darvish et al., 2024) `ev:reported` p. 5 ^darvish2024organa-013
- The glassy carbon working electrode was mechanically polished for 30 s using a robotic polishing station to ensure its activation. (Darvish et al., 2024) `ev:reported` p. 6 ^darvish2024organa-014
- Cyclic voltammetry used three cycles in an electrochemical window between -1.5 V and 0.5 V at a scan rate of 100 mV/s. (Darvish et al., 2024) `ev:reported` p. 7 ^darvish2024organa-015
- Organa.Perception detects and estimates the poses of objects within the electrochemistry scene, taking approximately 20 s from a view pose. (Darvish et al., 2024) `ev:measured` p. 7 ^darvish2024organa-016
- In total, three complete electrochemistry experiments were performed, each testing six buffer solutions ranging from pH 4 to pH 9. (Darvish et al., 2024) `ev:reported` p. 7 ^darvish2024organa-017
- The authors cite reported dissociation constants for anthraquinone-2-sulfonate of pKa1 = 7.68 and pKa2 = 10.92 from prior literature. (Darvish et al., 2024) `ev:cited` p. 7 ^darvish2024organa-018
- Because pKa2 lies in a corrosive region of pHs, the experiments only investigated pH values needed to solve for pKa1. (Darvish et al., 2024) `ev:reported` p. 7 ^darvish2024organa-019
- Organa obtained slope estimates of -61.3, -61.8 and -61.0 mV/pH unit for the Pourbaix region where pH < pKa1. (Darvish et al., 2024) `ev:measured` p. 7 ^darvish2024organa-020
- Across the three electrochemistry experiments, Organa estimated the dissociation constant pKa1 as 8.12, 7.86 and 8.10. (Darvish et al., 2024) `ev:measured` p. 7 ^darvish2024organa-021
- The authors attribute the comparatively high pKa1 variance to a lack of points above pH 9, avoided because of safety concerns. (Darvish et al., 2024) `ev:asserted` p. 7 ^darvish2024organa-022
- The parallel electrochemistry plan is a sequence of 19 actions, some performed by a single agent, others jointly by several agents. (Darvish et al., 2024) `ev:reported` p. 7 ^darvish2024organa-023
- On average, the sequential electrochemistry plan takes 21.67 mins to execute, while the parallel plan takes 17.10 mins. (Darvish et al., 2024) `ev:measured` p. 7 ^darvish2024organa-024
- Over 12 trials, solving the sequential planning problem took 61.52±0.1 s, while temporal task and motion planning took 186.3 ± 46.0 s. (Darvish et al., 2024) `ev:measured` p. 7 ^darvish2024organa-025
- The user study tested manual experimentation, Organa startup, Organa troubleshooting, and a CLAIRify mode where users detailed every experiment step. (Darvish et al., 2024) `ev:reported` p. 9 ^darvish2024organa-026
- Using combined data from all runs, Organa produced a pKa1 of 8.03, while chemists performing manual experiments produced 8.02. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-027
- The combined slope estimate from Organa was -61.3 mV/pH unit, while for the chemists it was -62.7 mV/pH unit. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-028
- Manual experimentation averaged over 30 minutes of chemist involvement, while Organa startup required 7.35 minutes written and 4.27 minutes spoken. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-029
- Organa troubleshooting took chemists an average of 1.30 minutes to provide feedback on errors during the electrochemistry experiment. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-030
- The CLAIRify-style workflow, in which users manually detailed each experiment step, necessitated 17.65 minutes of user involvement on average. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-031
- In 3 of 40 experiments with correct results, Organa incorrectly alerted the human, giving a false positive. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-032
- Among 8 experiments with intentionally introduced errors, Organa failed to detect an issue in only one instance, a false negative. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-033
- NASA-TLX responses indicated that Organa halved participant frustration compared with performing the electrochemistry experiment manually. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-034
- NASA-TLX responses indicated that Organa reduced participants' physical demand fourfold compared with performing the electrochemistry experiment manually. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-035
- SUS results showed Organa significantly improved over manual work in desire for frequent use, complexity, consistency, and cumbersomeness. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-036
- Custom questionnaire responses indicated unanimous agreement among chemists regarding the potential for automating repetitive lab tasks. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-037
- The post-experiment summary report generated by Organa was unanimously valued by all chemists who took part in the user study. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-038
- In the solubility experiment, Organa estimated compound solubility with 10.2 ± 2.2% mean and standard deviation values relative to literature. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-039
- Across three runs of the electrochemistry experiment, Organa yielded a Pourbaix slope value of −61.4 ± 0.5 mV /pH unit. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-040
- Across three runs of the electrochemistry experiment, Organa yielded a pKa1 value of 8.03 ± 0.17, similar to literature values. (Darvish et al., 2024) `ev:measured` p. 10 ^darvish2024organa-041
- Unlike lab automation with fixed object poses, Organa perceives and acts in a semi-structured environment where objects and poses can vary. (Darvish et al., 2024) `ev:asserted` p. 10 ^darvish2024organa-042
- The electrochemistry experiment ran as a 114(6×19) steps plan with 130.00 mins execution time, performed 2 times. (Darvish et al., 2024) `ev:measured` p. 11 ^darvish2024organa-043
- Organa.Planner gave a notable enhancement of 274 seconds (21.1%) in overall electrochemistry time compared to sequential task execution. (Darvish et al., 2024) `ev:measured` p. 11 ^darvish2024organa-044
- For testing three buffer solutions, users saved 88.4 % of time by interacting with Organa through audio versus manual experimentation. (Darvish et al., 2024) `ev:measured` p. 12 ^darvish2024organa-045
- Users did not perceive a significant increase in efficiency with Organa based on the workload and SUS studies. (Darvish et al., 2024) `ev:measured` p. 12 ^darvish2024organa-046
- The authors suggest this subjective-objective discrepancy might stem from users performing only half of the full experiment manually. (Darvish et al., 2024) `ev:asserted` p. 12 ^darvish2024organa-047
- Half the users expressed uncertainty in trusting a robot to complete the experiments autonomously from start to finish. (Darvish et al., 2024) `ev:measured` p. 12 ^darvish2024organa-048
- As a limitation, Organa currently relies primarily on independent sensor modalities for perception rather than multimodal perception. (Darvish et al., 2024) `ev:asserted` p. 13 ^darvish2024organa-049
- Defining a PDDL domain for Organa.Planner is complex, potentially making it challenging for chemists without planning expertise to modify. (Darvish et al., 2024) `ev:asserted` p. 13 ^darvish2024organa-050
- Organa.Planner lacks support for online replanning, which limits its adaptability to uncertainties in task execution, according to the authors. (Darvish et al., 2024) `ev:asserted` p. 13 ^darvish2024organa-051
- The present system lacks the capability to automatically prepare the experimental setup, such as retrieving clean beakers or inserting pump tubes. (Darvish et al., 2024) `ev:asserted` p. 13 ^darvish2024organa-052
- Organa.Reasoner uses the ReAct prompting scheme, generating thought, action, observation tuples after each experiment to propose subsequent experiments. (Darvish et al., 2024) `ev:reported` p. 13 ^darvish2024organa-053
- The planner adapts PDDLStream with PDDL2.1 durative actions and introduces a time-variant cost function to enhance task execution efficiency. (Darvish et al., 2024) `ev:reported` p. 15 ^darvish2024organa-054
- Time-varying streams linked to cost functions and timings are evaluated eagerly, while the remaining streams are evaluated optimistically. (Darvish et al., 2024) `ev:reported` p. 15 ^darvish2024organa-055
- Transparent object detection chains Grounding DINO zero-shot detection, Non-Maximum Suppression, and Segment Anything segmentation to obtain object masks. (Darvish et al., 2024) `ev:reported` p. 16 ^darvish2024organa-056
- At the experiment's conclusion, Organa automatically generates a PDF report with experiment details, failure logs with resolutions, and summary plots. (Darvish et al., 2024) `ev:reported` p. 18 ^darvish2024organa-057
- The perception evaluation dataset consists of 135 RGBD images across 17 scenes, each containing 4 transparent objects and 1 polishing plate. (Darvish et al., 2024) `ev:reported` p. 21 ^darvish2024organa-058
- The perception pipeline achieved a mean absolute position error of 3.5 cm, averaged over all objects in the dataset. (Darvish et al., 2024) `ev:measured` p. 21 ^darvish2024organa-059
- The authors explain that Grounding DINO often recognizes the brown pad as the plate rather than the entire polishing pad fixture. (Darvish et al., 2024) `ev:asserted` p. 21 ^darvish2024organa-060
- Applying radius outlier removal to point clouds improved the overall position mean absolute error from 4.5 cm to 3.5 cm. (Darvish et al., 2024) `ev:measured` p. 22 ^darvish2024organa-061
- Glass object Average Precision stayed between 90.7 and 94.9 across IoU thresholds from 0.25 to 0.75. (Darvish et al., 2024) `ev:measured` p. 22 ^darvish2024organa-062
- Plate detection Average Precision dropped from 81.4 at an IoU threshold of 0.25 to 37.1 at 0.75. (Darvish et al., 2024) `ev:measured` p. 22 ^darvish2024organa-063
- The user study recruited 8 chemists from the University of Toronto chemistry department, none previously familiar with Organa. (Darvish et al., 2024) `ev:reported` p. 29 ^darvish2024organa-064
- According to the abstract, users saved an average of 80.3% of their time when using Organa. (Darvish et al., 2024) `ev:abstract` p. 2 ^darvish2024organa-065

## 🎯 Contributions

## 📖 Glossary

- **Self-driving lab (SDL)** — Laboratory combining data-driven experiment planning with automated experiment execution.
- **TAMP** — Task and motion planning: jointly choosing discrete actions and feasible robot motions.
- **PDDLStream** — Planner combining PDDL symbolic search with streams, declarative samplers of continuous values.
- **Durative action** — PDDL2.1 action split into start and end events, allowing concurrent execution.
- **XDL** — Hardware-agnostic XML Chemical Description Language for encoding chemistry procedures.
- **Pourbaix diagram** — Plot of redox potential against pH, with slopes revealing proton-electron reaction regimes.
- **pKa1** — First dissociation constant; pH where the Pourbaix slope changes between regimes.
- **Mechanical polishing** — Abrasive pretreatment that reactivates glassy carbon electrodes between measurements.
- **Turbidity** — Solution opaqueness, used here as a proxy for undissolved solute.
- **NASA-TLX** — Six-dimension questionnaire rating perceived workload of a task.
- **System Usability Scale (SUS)** — Ten-item Likert questionnaire measuring subjective system usability.
- **ReAct** — Prompting scheme interleaving reasoning thoughts, actions and observations for LLM agents.

## ❓ Open questions

- How does Organa behave when the plan needs to change mid-execution, given the planner has no online replanning?
- Would the pKa1 estimate converge closer to the literature 7.68 with measurements above pH 9 or more replicates?
- Can chemists without planning expertise author new PDDL domains, or can LLMs generate and validate them?
- How would the system generalise to new lab equipment beyond the four transparent vessel types and polishing plate evaluated?
- Does the 88.4% time saving hold when users run the full experiment manually rather than half of it?
- How much of the planning overhead of temporal TAMP (186.3 s vs 61.52 s) could learned heuristics remove?
- Can the robot prepare the experimental setup (fetching vessels, inserting tubes and probes) autonomously?

## 📝 Notes on reading

- Version read: arXiv 2401.06949v2 (7 Jan 2025) preprint, matching the packet identifier.
- Abstract vs body: the abstract states users save an average of 80.3% of their time; the body (p. 12) reports 88.4 % for audio interaction over three buffer solutions. The abstract figure is not found in the body.
- Text vs figure timings: p. 7 gives 21.67 min sequential and 17.10 min parallel (averages); Fig. 5 (p. 8) gives 1,346 s (22.43 min) and 1,071 s (17.85 min) for a single buffer test. The 21.1% and 274 s figures match neither pair exactly.
- Duration discretisation on p. 7 defines 2T as up to 120 s and 3T as more than 180 s, leaving 120-180 s unassigned.
- Run counts differ: p. 7 says three complete electrochemistry experiments; p. 11 lists the electrochemistry plan as performed 2 times, and solubility as performed 2 times.
- Manual involvement is given as over 30 minutes in the text (p. 10) but 36.83 min in Fig. 7 (p. 11).
- The Pourbaix model is described with 4 parameters on p. 17; Note S7 (p. 37) adds the noise sigma as a fifth estimated parameter.
- The user-study script names Sodium Anthraquinone-1-sulfonate (p. 29) while the experiment uses anthraquinone-2-sulfonate; the manual protocol lists buffers pH 4 to 10 vs pH 4 to 9 elsewhere.
- Solubility accuracy values (7.2%, 11.2%, 12.3%) read as errors relative to literature, not accuracies.
- Figures 2, 4, 6, 7, 8 and 9 were only described (Gantt charts, Pourbaix posteriors, survey bars, architecture); per-question survey bars in Fig. 8 were not extracted.
- Supplement pages 21-49 (prompts, questionnaire, PDDL listings, sample report) were read selectively; long prompt/PDDL listings were not claimed.

## Suggested new concepts

- Temporal task and motion planning — joint TAMP and scheduling with durative actions recurs in lab automation and deserves a dedicated note.
- LLM-based chemist-in-the-loop lab assistants — Organa, CLAIRify, ChemCrow and Coscientist form a family worth comparing.
- Transparent object perception for lab robots — detection and pose estimation of glassware is a recurring bottleneck.
- Automated electrode polishing — a concrete electrochemistry pretreatment bottleneck the paper automates.
- Automatic experiment report generation — post-experiment summaries valued unanimously by users as a trust mechanism.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H7.** Sistema real de química robótica con LLM y realimentación visual que sirve de referencia de extremo a extremo para la automatización de laboratorio.
