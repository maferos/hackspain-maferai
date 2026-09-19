---
aliases: []
type: "source"
title: "IKFlow: Generating Diverse Inverse Kinematics Solutions"
citekey: "Ames2021ikflow"
doi: "10.48550/arXiv.2111.08933"
arxiv: "2111.08933"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2111.08933"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Barrett Ames", "Jeremy Morgan", "George Konidaris"]
sha256: ["8b1b41b7321275ad9039fc02b7e41c65e45365ee540ad722f971481eb1a95995"]
pdf: "Content/Papers/Ames2021ikflow.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 65
---

📄 PDF: [[Ames2021ikflow.pdf]]

> [!abstract] One-sentence summary
> IKFlow trains a conditional normalizing flow per robot to sample thousands of diverse, millimetre-accurate inverse kinematics solutions for redundant arms in milliseconds, which can seed classical solvers for exact refinement.

## Abstract

Inverse kinematics - finding joint poses that reach a given Cartesian-space end-effector pose - is a common operation in robotics, since goals and waypoints are typically defined in Cartesian space, but robots must be controlled in joint space. However, existing inverse kinematics solvers return a single solution pose, where systems with more than 6 degrees of freedom support infinitely many such solutions, which can be useful in the presence of constraints, pose preferences, or obstacles. We introduce a method that uses a deep neural network to learn to generate a diverse set of samples from the solution space of such kinematic chains. The resulting samples can be generated quickly (2000 solutions in under 10ms) and accurately (to within 10 millimeters and 2 degrees of an exact solution) and can be rapidly refined by classical methods if necessary. (arXiv)

## 🧠 Key ideas (atomic)

- Analytical IK solvers such as IKFast and IKBT return all solutions for an arm but cannot handle arms above 6 DOF. (Ames et al., 2021) `ev:cited` p. 1 ^ames2021ikflow-001
- Numerical IK solvers can be applied to arms with any number of joints but return only a single solution, if any. (Ames et al., 2021) `ev:asserted` p. 1 ^ames2021ikflow-002
- The authors state that among coverage, speed and accuracy, accuracy is the least important requirement for a 7+ DOF IK solver. (Ames et al., 2021) `ev:asserted` p. 1 ^ames2021ikflow-003
- They argue approximate samples suffice because forward kinematics verification is very fast and numerical solvers seeded with them refine rapidly. (Ames et al., 2021) `ev:asserted` p. 1 ^ames2021ikflow-004
- IKFlow trains a neural network to output a diverse set of joint poses that approximately satisfy a given Cartesian goal pose. (Ames et al., 2021) `ev:reported` p. 1 ^ames2021ikflow-005
- IKFlow treats inverse kinematics as a generative modeling problem over the solution space, exploiting Normalizing Flows to model multi-modal distributions. (Ames et al., 2021) `ev:asserted` p. 1 ^ames2021ikflow-006
- IKFlow is trained once per robot and then rapidly generates hundreds to thousands of diverse approximate IK solutions. (Ames et al., 2021) `ev:measured` p. 2 ^ames2021ikflow-007
- With joint limits, the IK target space becomes Euclidean rather than a torus, allowing generic density estimators instead of torus-specific ones. (Ames et al., 2021) `ev:asserted` p. 2 ^ames2021ikflow-008
- Covering the solution space by running a single-solution IK solver from random start states takes on the order of seconds for thousands of solutions. (Ames et al., 2021) `ev:asserted` p. 2 ^ames2021ikflow-009
- The generative model was selected for sample diversity, multi-modality, conditioning on the goal pose, fast sampling and sufficient sample accuracy. (Ames et al., 2021) `ev:asserted` p. 2 ^ames2021ikflow-010
- IKFlow uses the coupling layer developed by Kingma and Dhariwal as the invertible building block of its normalizing flow. (Ames et al., 2021) `ev:reported` p. 2 ^ames2021ikflow-011
- In the conditional flow, the goal pose is passed into every coupling layer's coefficient network, which need not be inverted to invert the layer. (Ames et al., 2021) `ev:reported` p. 3 ^ames2021ikflow-012
- The authors state their conditioning formulation reduces the number of hyperparameters to tune compared with other conditioning methods such as Ardizzone et al. (Ames et al., 2021) `ev:asserted` p. 3 ^ames2021ikflow-013
- Distribution coverage is evaluated with Maximum Mean Discrepancy using an inverse multi-quadric kernel, chosen for its long tails and previous use. (Ames et al., 2021) `ev:reported` p. 3 ^ames2021ikflow-014
- The selected number of coupling layers ranges from 8 for the PR2 to 16 for Baxter across the tested kinematic chains. (Ames et al., 2021) `ev:reported` p. 3 ^ames2021ikflow-015
- The Panda network uses a coupling layer width of 9, whereas the other listed kinematic chains use a width of 15. (Ames et al., 2021) `ev:reported` p. 3 ^ames2021ikflow-016
- Demby'S et al. built a neural network IK approach but concluded it is not a fruitful path because of large error. (Ames et al., 2021) `ev:cited` p. 3 ^ames2021ikflow-017
- Ren and Ben-Tzvi used several GAN types for IK, with their best performing approach achieving 8cm of error. (Ames et al., 2021) `ev:cited` p. 4 ^ames2021ikflow-018
- Ardizzone et al. applied a deep generative approach similar to IKFlow, but only to a small planar IK problem. (Ames et al., 2021) `ev:cited` p. 4 ^ames2021ikflow-019
- IKFlow differs from the flow-based IK of Kim and Perez through conditional normalizing flows, training noise, and base-distribution sub-sampling. (Ames et al., 2021) `ev:asserted` p. 4 ^ames2021ikflow-020
- Measured on the Panda arm, IKFlow position accuracy is ∼5x better than the results reported by Kim and Perez. (Ames et al., 2021) `ev:measured` p. 4 ^ames2021ikflow-021
- Measured on the Panda arm, IKFlow orientation accuracy is ∼3x better than the results reported by Kim and Perez. (Ames et al., 2021) `ev:measured` p. 4 ^ames2021ikflow-022
- Training data are generated by uniformly sampling joint values within the joint limits and computing the corresponding poses by forward kinematics. (Ames et al., 2021) `ev:reported` p. 4 ^ames2021ikflow-023
- The authors leave sampling methods that account for joint-limit effects and self-collisions to future work, having obtained satisfactory performance without them. (Ames et al., 2021) `ev:asserted` p. 4 ^ames2021ikflow-024
- In the Panda arm width comparison, a coefficient network width of 1024 gave the highest performance among the tested widths. (Ames et al., 2021) `ev:measured` p. 4 ^ames2021ikflow-025
- The authors chose a Normal base distribution because it simplifies the Maximum Likelihood loss and is quick to sample. (Ames et al., 2021) `ev:asserted` p. 5 ^ames2021ikflow-026
- Coupling layer count and width can be found by a hyperparameter sweep over ranges such as [1, 30] and [n, n + 10]. (Ames et al., 2021) `ev:asserted` p. 5 ^ames2021ikflow-027
- Network error decreases with increased network size up to a point, beyond which increasing size does not improve performance. (Ames et al., 2021) `ev:measured` p. 5 ^ames2021ikflow-028
- For several of the tested kinematic chains, training diverged when trained with the pure Maximum Likelihood loss alone. (Ames et al., 2021) `ev:measured` p. 5 ^ames2021ikflow-029
- The authors attribute this divergence to a mismatch between the dimension of the solution manifolds and the base distribution. (Ames et al., 2021) `ev:asserted` p. 5 ^ames2021ikflow-030
- Some Cartesian poses can only be reached by fixing a joint at a specific configuration, giving solution spaces of lower dimension than joint space. (Ames et al., 2021) `ev:asserted` p. 5 ^ames2021ikflow-031
- Following SoftFlow, IKFlow adds full-dimensional noise of randomly drawn magnitude to the training data, passing that magnitude as a conditional input. (Ames et al., 2021) `ev:reported` p. 5 ^ames2021ikflow-032
- The effect of the added training noise is removed at test time by setting the noise-magnitude conditional to 0. (Ames et al., 2021) `ev:reported` p. 5 ^ames2021ikflow-033
- Points sampled from the tail of the Normal base distribution are likely to produce solutions with high error at evaluation time. (Ames et al., 2021) `ev:asserted` p. 5 ^ames2021ikflow-034
- Sub-sampling the base distribution at test time reduces tail samples but encourages less diverse solutions, so the scaling is a tuning parameter. (Ames et al., 2021) `ev:asserted` p. 6 ^ames2021ikflow-035
- The IKFlow models were built with the FrEIA framework of Ardizzone et al. and trained with the PyTorch library. (Ames et al., 2021) `ev:reported` p. 6 ^ames2021ikflow-036
- In general, a latent scaling factor of 0.25 lowers average positional error by ∼30%, at the expense of a ∼150% MMD increase. (Ames et al., 2021) `ev:measured` p. 6 ^ames2021ikflow-037
- Speed was measured as the time to sample 100 solutions for a pose, averaged over 50 randomly-sampled Cartesian poses. (Ames et al., 2021) `ev:reported` p. 6 ^ames2021ikflow-038
- Accuracy was measured over 1000 test Cartesian poses with 250 joint solutions each, comparing desired and forward-kinematics realized poses. (Ames et al., 2021) `ev:reported` p. 6 ^ames2021ikflow-039
- The MMD score averages 2500 MMD values, each computed from 50 joint solutions per method for a randomly drawn pose. (Ames et al., 2021) `ev:reported` p. 6 ^ames2021ikflow-040
- Ground truth samples for the MMD score were obtained by providing different seeds to TRAC-IK for the same Cartesian pose. (Ames et al., 2021) `ev:reported` p. 6 ^ames2021ikflow-041
- IKFlow was compared with an Invertible Neural Network and a Mixture Density Network on the railY chain3 and Panda Arm benchmarks. (Ames et al., 2021) `ev:reported` p. 6 ^ames2021ikflow-042
- The experiments covered 10 different kinematic chains across 6 different robots to evaluate generality across kinematic structures. (Ames et al., 2021) `ev:reported` p. 6 ^ames2021ikflow-043
- On both benchmarks, the IKFlow model performed considerably better than the INN and MDN models in L2 error learning curves. (Ames et al., 2021) `ev:measured` p. 6 ^ames2021ikflow-044
- The authors suggest that higher-dimensional problems are more likely to contain lower-dimensional solution spaces that introduce training instabilities. (Ames et al., 2021) `ev:asserted` p. 6 ^ames2021ikflow-045
- On the ATLAS Arm, seeding TRAC-IK with IKFlow provides the 1e-6 accuracy of TRAC-IK with one fifth of its runtime. (Ames et al., 2021) `ev:measured` p. 6 ^ames2021ikflow-046
- Average position error across the tested chains ranges from 7.72 millimeters for the Panda to 0.36 millimeters for the Valkyrie lower arm. (Ames et al., 2021) `ev:measured` p. 5 ^ames2021ikflow-047
- Average angular error across the tested chains ranges from 2.81 degrees for the Panda to 0.15 degrees for the Valkyrie lower arm. (Ames et al., 2021) `ev:measured` p. 5 ^ames2021ikflow-048
- Time to return 100 solutions for one pose ranged from 4.31 msec for the PR2 to 8.55 msec for Valkyrie whole arm and waist. (Ames et al., 2021) `ev:measured` p. 5 ^ames2021ikflow-049
- The PR2 chain obtained an MMD score of 0.2128, while the Panda obtained 0.0306 against TRAC-IK ground truth samples. (Ames et al., 2021) `ev:measured` p. 5 ^ames2021ikflow-050
- Qualitatively, IKFlow solutions for the Panda and ATLAS arm-and-waist chains cover the same space as solutions found by seeded TRAC-IK sampling. (Ames et al., 2021) `ev:measured` p. 4 ^ames2021ikflow-051
- As a reference point, the authors note that the mechanical repeatability of many industrial arms is 0.1mm. (Ames et al., 2021) `ev:asserted` p. 7 ^ames2021ikflow-052
- For the ATLAS Arm, refining IKFlow solutions with numerical optimization takes on average 0.20 ms. (Ames et al., 2021) `ev:measured` p. 7 ^ames2021ikflow-053
- IKFlow can return 500 solutions in 5ms, whereas nonlinear optimization approaches find a single solution in about 0.3 millisecond. (Ames et al., 2021) `ev:measured` p. 7 ^ames2021ikflow-054
- IKFlow runtime scales linearly with the number of requested solutions, with 4, 000 samples found in 20 milliseconds. (Ames et al., 2021) `ev:measured` p. 7 ^ames2021ikflow-055
- TRAC-IK fed random seeds takes more than a second to return 1, 000 samples, according to the authors' comparison. (Ames et al., 2021) `ev:measured` p. 7 ^ames2021ikflow-056
- TRAC-IK takes approximately 5x less time to run when seeded with an approximate solution returned by IKFlow. (Ames et al., 2021) `ev:measured` p. 7 ^ames2021ikflow-057
- Empirically, running IKFlow to generate seeds before TRAC-IK is faster than TRAC-IK alone when requesting 7 or more solutions. (Ames et al., 2021) `ev:measured` p. 7 ^ames2021ikflow-058
- The training time required for IKFlow models to reach a given position error grows with the complexity of the kinematic chain. (Ames et al., 2021) `ev:measured` p. 7 ^ames2021ikflow-059
- Training batches needed to reach 1cm of error grow exponentially with the sum of joint limit ranges, in artificially expanded joint-limit experiments. (Ames et al., 2021) `ev:measured` p. 7 ^ames2021ikflow-060
- The authors conclude that IKFlow can serve as the basis for expanded functionality of 7+ DOF kinematic chains. (Ames et al., 2021) `ev:asserted` p. 7 ^ames2021ikflow-061
- Coefficient networks are 3x1024-wide fully connected networks with Leaky-Relu activation, and all models used a softflow noise scale of 1 × 10−3. (Ames et al., 2021) `ev:reported` p. 7 ^ames2021ikflow-062
- The learning rate decayed exponentially by a factor of 0.979 after every 39000 batches during IKFlow training. (Ames et al., 2021) `ev:reported` p. 8 ^ames2021ikflow-063
- Models were trained until convergence on 2.5 million points using the Ranger optimizer with batch size 128. (Ames et al., 2021) `ev:reported` p. 8 ^ames2021ikflow-064
- The Mixture Density Network baseline used 70 and 125 mixture components for railY chain3 and the Panda arm respectively. (Ames et al., 2021) `ev:reported` p. 8 ^ames2021ikflow-065

## 🎯 Contributions

## 📖 Glossary

- **Inverse kinematics (IK)** — Mapping a desired end-effector pose to joint configurations that reach it.
- **Kinematic redundancy** — More joint degrees of freedom than the task space, giving infinitely many IK solutions.
- **Normalizing flow** — Generative model built from invertible layers, enabling exact density estimation and fast sampling.
- **Coupling layer** — Invertible layer that scales and shifts half the variables using a network of the other half.
- **Conditional normalizing flow** — Normalizing flow whose coupling coefficients also depend on conditioning input, here the goal pose.
- **Maximum Mean Discrepancy (MMD)** — Kernel distance between two distributions via their mean embeddings in an RKHS.
- **SoftFlow** — Adding noise of conditioned magnitude so flows can fit lower-dimensional manifolds.
- **TRAC-IK** — Open-source numerical IK solver based on nonlinear optimization, returning one solution per seed.
- **Latent scaling factor** — Multiplier shrinking base-distribution samples, trading solution diversity for accuracy.

## ❓ Open questions

- Can training cost be contained for chains with large joint-limit ranges, given the reported exponential growth in batches needed?
- Would sampling training data that accounts for joint limits and self-collisions improve accuracy near limits?
- How does IKFlow handle obstacles or collision constraints, which motivate multiple solutions but are not evaluated?
- Is the MMD estimate against seeded TRAC-IK samples a faithful measure of full solution-space coverage?
- How should the latent scaling factor be chosen per application beyond the fixed value of 0.25?

## 📝 Notes on reading

Version read: arXiv 2111.08933v3 (29 Aug 2022), the RA-L accepted preprint. Figure 1 (100 Panda solutions), Figure 3 (TRAC-IK vs IKFlow solution clouds), Figures 4, 5, 7 and 8 (learning curves, latent scaling trade-off, training batches vs joint-limit sum) were only described from captions and text. The parameter counts in Table I are extracted as e.g. `3.836 × 107`, meaning 10^7; they were not claimed. The Figure 2 architecture diagram is garbled LaTeX in the extraction.

Internal inconsistencies: the text (p. 7) says all kinematic chains have an MMD score under 0.05, but Table II (p. 5) gives 0.2128 for the PR2. The conclusion says rotational error is less than 1.5 degrees, but Table II gives 2.81 degrees for the Panda and 1.56 for the PR2. The abstract claims accuracy within 2 degrees, also contradicted by the Panda row. The abstract claims 2000 solutions in under 10ms, while the body reports 4, 000 samples in 20 ms and 500 in 5ms. The Fig. 6 caption says one fifth of TRAC-IK runtime, the text says approximately 5x less time; consistent.

## Suggested new concepts

- Conditional normalizing flows — the core generative mechanism reused across learned IK and other conditional sampling problems.
- Learned inverse kinematics — a family of neural IK solvers (MDN, INN, GAN, flows) worth comparing in one note.
- Maximum Mean Discrepancy — the distribution-coverage metric used to evaluate generative samplers.
- SoftFlow noise conditioning — a general fix for flows on lower-dimensional manifolds.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H1.** IK aprendida con flujos normalizantes que muestrea la variedad de soluciones de un brazo redundante en milisegundos.
