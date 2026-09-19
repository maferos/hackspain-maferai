---
aliases: []
type: "source"
title: "Learning Latent Actions to Control Assistive Robots"
citekey: "Losey2021learning"
doi: "10.48550/arXiv.2107.02907"
arxiv: "2107.02907"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2107.02907"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Dylan P. Losey", "Hong Jun Jeon", "Mengxi Li", "Krishnan Srinivasan", "Ajay Mandlekar", "Animesh Garg", "Jeannette Bohg", "Dorsa Sadigh"]
sha256: ["c8b3d3ad416187f15c05bd27c89ea3b64c4cdccbce29fbfb888b301e16b815c4"]
pdf: "Content/Papers/Losey2021learning.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Losey2021learning.pdf]]

> [!abstract] One-sentence summary
> The paper maps a 2-DoF joystick onto a 7-DoF assistive arm by learning context-conditioned latent actions from demonstrations, blending them with shared autonomy and a personalised joystick alignment, and shows faster and more accurate eating tasks with non-disabled users and two disabled users.

## Abstract

Assistive robot arms enable people with disabilities to conduct everyday tasks on their own. These arms are dexterous and high-dimensional; however, the interfaces people must use to control their robots are low-dimensional. Consider teleoperating a 7-DoF robot arm with a 2-DoF joystick. The robot is helping you eat dinner, and currently you want to cut a piece of tofu. Today's robots assume a pre-defined mapping between joystick inputs and robot actions: in one mode the joystick controls the robot's motion in the x-y plane, in another mode the joystick controls the robot's z-yaw motion, and so on. But this mapping misses out on the task you are trying to perform! Ideally, one joystick axis should control how the robot stabs the tofu and the other axis should control different cutting motions. Our insight is that we can achieve intuitive, user-friendly control of assistive robots by embedding the robot's high-dimensional actions into low-dimensional and human-controllable latent actions. We divide this process into three parts. First, we explore models for learning latent actions from offline task demonstrations, and formalize the properties that latent actions should satisfy. Next, we combine learned latent actions with autonomous robot assistance to help the user reach and maintain their high-level goals. Finally, we learn a personalized alignment model between joystick inputs and latent actions. We evaluate our resulting approach in four user studies where non-disabled participants reach marshmallows, cook apple pie, cut tofu, and assemble dessert. We then test our approach with two disabled adults who leverage assistive devices on a daily basis. (arXiv)

## 🧠 Key ideas (atomic)

- Existing assistive robot work uses pre-defined input mappings in which users switch between modes to control different robot degrees of freedom. (Losey et al., 2021) `ev:cited` p. 2 ^losey2021learning-001
- The authors propose embedding high-dimensional robot actions into low-dimensional, human-controllable latent actions to make high-dimensional robots easier to control. (Losey et al., 2021) `ev:asserted` p. 2 ^losey2021learning-002
- Users with physical disabilities surveyed in prior work preferred partial autonomy during eating because it better lets them convey their own preferences. (Losey et al., 2021) `ev:cited` p. 3 ^losey2021learning-003
- Prior work pruned unnecessary control axes with Principal Component Analysis, mapping human inputs through the first few eigenvectors of demonstrated motions. (Losey et al., 2021) `ev:cited` p. 3 ^losey2021learning-004
- The robot's overall action is a linear blend of the human-commanded action and an autonomous assistive action, weighted by an arbitration parameter. (Losey et al., 2021) `ev:reported` p. 5 ^losey2021learning-005
- The autonomous assistive action moves the robot toward each candidate goal in proportion to the robot's belief that the human wants it. (Losey et al., 2021) `ev:reported` p. 5 ^losey2021learning-006
- The authors identify four properties that user-friendly latent actions should have: conditioning, controllability, consistency, and scalability. (Losey et al., 2021) `ev:asserted` p. 6 ^losey2021learning-007
- A latent action space is defined as controllable if latent action sequences can move the robot between any pair of demonstrated states. (Losey et al., 2021) `ev:asserted` p. 7 ^losey2021learning-008
- A latent action space is defined as consistent if the same latent action has a similar effect on robot behaviour in nearby states. (Losey et al., 2021) `ev:asserted` p. 7 ^losey2021learning-009
- The authors assert that only models reasoning over the robot's context when decoding inputs can interpret latent actions accurately and intuitively. (Losey et al., 2021) `ev:asserted` p. 7 ^losey2021learning-010
- The conditioned variational autoencoder loss adds a KL penalty toward a standard normal distribution to the context-conditioned action reconstruction error. (Losey et al., 2021) `ev:reported` p. 8 ^losey2021learning-011
- The robot updates its belief over a discrete set of candidate goals with Bayesian inference from the history of human inputs. (Losey et al., 2021) `ev:reported` p. 8 ^losey2021learning-012
- For shared autonomy, the decoder is conditioned on both robot state and goal belief, so latent action meaning changes with robot confidence. (Losey et al., 2021) `ev:reported` p. 9 ^losey2021learning-013
- A Lyapunov analysis shows that the blended approach yields uniformly ultimately bounded stability about the human's goal. (Losey et al., 2021) `ev:computed` p. 10 ^losey2021learning-014
- As the robot's confidence in the true goal increases, the radius of the stability bound shrinks toward the decoded-action magnitude bound. (Losey et al., 2021) `ev:computed` p. 10 ^losey2021learning-015
- An entropy term over goals is added to the training loss, rewarding latent actions that move the robot toward each goal in a context. (Losey et al., 2021) `ev:reported` p. 10 ^losey2021learning-016
- A multi-layer perceptron alignment model maps each joystick input and context to a latent action, personalising controls without changing the decoder. (Losey et al., 2021) `ev:reported` p. 11 ^losey2021learning-017
- Alignment is learned with semi-supervised learning because asking the human to label enough motion-joystick pairs is impractical in complex tasks. (Losey et al., 2021) `ev:asserted` p. 11 ^losey2021learning-018
- The alignment loss combines a supervised term on labelled queries with proportionality, reversability, and consistency priors on unlabelled motions. (Losey et al., 2021) `ev:reported` p. 13 ^losey2021learning-019
- The reversability prior expects the opposite joystick input to return the end-effector to its original pose, so users can recover from mistakes. (Losey et al., 2021) `ev:asserted` p. 13 ^losey2021learning-020
- In all reported user studies the robot was trained with a maximum of twenty minutes of kinesthetic demonstrations, entirely on the robot computer. (Losey et al., 2021) `ev:reported` p. 14 ^losey2021learning-021
- The authors note that this short training time is likely due to the cVAE model structure and may not hold in general. (Losey et al., 2021) `ev:asserted` p. 14 ^losey2021learning-022
- Latent action simulations used one-arm and two-arm planar robots with 5-DoF arms, each task trained on 10000 state-action pairs. (Losey et al., 2021) `ev:reported` p. 14 ^losey2021learning-023
- On the Sine task, cAE and cVAE obtained 1.37±1.2% and 3.74 ± 0.4% of the PCA reconstruction loss, respectively. (Losey et al., 2021) `ev:measured` p. 15 ^losey2021learning-024
- On the Sine task, unconditioned AE and VAE incurred 98.0 ± 0.6% and 100 ± 0.8% of the PCA reconstruction loss. (Losey et al., 2021) `ev:measured` p. 15 ^losey2021learning-025
- Moving between 1000 random states on the sine wave, cAE and cVAE had average end-effector errors of 0.05 ± 0.01 and 0.10±0.01. (Losey et al., 2021) `ev:measured` p. 15 ^losey2021learning-026
- On the Rotate task, cAE and cVAE reduced reconstruction loss to 0.65 ± 0.05% and 0.84 ± 0.07% of the PCA baseline. (Losey et al., 2021) `ev:measured` p. 15 ^losey2021learning-027
- On Rotate, cAE and cVAE achieved 5.4±0.1% and 5.9±0.1% of the PCA end-effector error, versus 56.8±9% and 71.5±8% for AE and VAE. (Losey et al., 2021) `ev:measured` p. 15 ^losey2021learning-028
- On Circle, the average angle between the two latent motion directions was 72±9◦ and 74±12◦ for cAE and cVAE, ideally 90◦. (Losey et al., 2021) `ev:measured` p. 16 ^losey2021learning-029
- On Circle, unconditioned AE and VAE models had average angles of 27±20◦ and 34±15◦ between their two latent motion directions. (Losey et al., 2021) `ev:measured` p. 16 ^losey2021learning-030
- On Reach, the distance between goal and final end-effector position was 0.57 ± 0.38 under VAE and 0.48 ± 0.5 with cVAE. (Losey et al., 2021) `ev:measured` p. 16 ^losey2021learning-031
- On Reach, the average start-to-goal trajectory length dropped from 5.1 ± 2.8 units with VAE to 3.1 ± 0.5 with cVAE. (Losey et al., 2021) `ev:measured` p. 16 ^losey2021learning-032
- In real-robot simulations, latent actions alone took 45% more time than LA+SA at β = 75, but only 30% more at β = 1000. (Losey et al., 2021) `ev:measured` p. 17 ^losey2021learning-033
- Without the entropy term, simulated users who changed goals could not escape the shared autonomy constraint around the wrong goal as the change came later. (Losey et al., 2021) `ev:measured` p. 17 ^losey2021learning-034
- With entropy-trained latent actions plus shared autonomy, simulated users who changed their mind could input actions that alter the robot's goal. (Losey et al., 2021) `ev:measured` p. 17 ^losey2021learning-035
- For both fast and slow simulated learners, LA+SA+Entropy improved in-task performance compared with latent actions plus shared autonomy without entropy. (Losey et al., 2021) `ev:measured` p. 17 ^losey2021learning-036
- In alignment simulations, the robot received 10 labelled motions from the simulated human plus 1000 unlabeled motions for self-supervised learning. (Losey et al., 2021) `ev:reported` p. 19 ^losey2021learning-037
- With 10 queries, each semi-supervised model using one intuitive prior performed twice as well as the supervised No Priors baseline. (Losey et al., 2021) `ev:measured` p. 20 ^losey2021learning-038
- Combining all three priors gave the lowest mean alignment error and standard deviation across the tested simulated user noise levels. (Losey et al., 2021) `ev:measured` p. 20 ^losey2021learning-039
- The authors suggest that relying on a few labelled examples in complex scenarios may lead to severe overfitting of the alignment model. (Losey et al., 2021) `ev:asserted` p. 20 ^losey2021learning-040
- In the HARMONIC marshmallow task, ten users with cVAE latent actions reached their desired morsel in 44 of the 50 total trials. (Losey et al., 2021) `ev:measured` p. 21 ^losey2021learning-041
- Compared with the High Assist baseline, cVAE users had significantly shorter trajectory length, t(158) = 9.39, p < .001. (Losey et al., 2021) `ev:measured` p. 21 ^losey2021learning-042
- Participants in the HARMONIC comparison only used cVAE; the baseline strategies were benchmarked with other participants in the HARMONIC dataset. (Losey et al., 2021) `ev:reported` p. 21 ^losey2021learning-043
- For the apple pie cooking study, the cVAE latent action model was trained with less than 7 minutes of demonstration data. (Losey et al., 2021) `ev:reported` p. 22 ^losey2021learning-044
- With cVAE, eleven participants finished the full apple pie recipe in less time than with End-Effector teleoperation, t(10) = −6.9, p < .001. (Losey et al., 2021) `ev:measured` p. 23 ^losey2021learning-045
- Participants rated cVAE as making the robot move more naturally than End-Effector teleoperation, t(10) = 3.8, p < .01. (Losey et al., 2021) `ev:measured` p. 23 ^losey2021learning-046
- In the apple pie study, participants did not indicate a clear preference between cVAE latent actions and End-Effector teleoperation. (Losey et al., 2021) `ev:measured` p. 23 ^losey2021learning-047
- The third user study crossed retargeting versus latent actions with presence or absence of shared autonomy in a 2x2 within-subjects design. (Losey et al., 2021) `ev:reported` p. 24 ^losey2021learning-048
- Across the Entree and Dessert tasks, users with shared autonomy reached their intended goals significantly more accurately, F(1, 18) = 29.9, p < .001. (Losey et al., 2021) `ev:measured` p. 25 ^losey2021learning-049
- LA+SA outperformed the other three conditions in summed Total Time and Idle Time across both eating tasks, p < .05. (Losey et al., 2021) `ev:measured` p. 25 ^losey2021learning-050
- In the alignment study, ten volunteers answered 7 queries for Avoid, 10 for Pour, and 30 for Reach & Pour. (Losey et al., 2021) `ev:reported` p. 27 ^losey2021learning-051
- Across tasks and metrics, the All Priors alignment outperformed No Align and No Priors, with the least variance of the three. (Losey et al., 2021) `ev:measured` p. 27 ^losey2021learning-052
- No Priors performance dropped significantly in the difficult Reach & Pour task compared with the simpler alignment tasks. (Losey et al., 2021) `ev:measured` p. 27 ^losey2021learning-053
- In the worst case, No Priors left participants stuck in Avoid because no joystick input mapped to their intended direction. (Losey et al., 2021) `ev:measured` p. 28 ^losey2021learning-054
- The case study recruited two adult males with disabilities, aged 28 and 42, who require assistance when eating. (Losey et al., 2021) `ev:reported` p. 28 ^losey2021learning-055
- For COVID-19 safety, the disabled participants teleoperated an on-campus robot from home with a virtual joystick and live-streamed video. (Losey et al., 2021) `ev:reported` p. 29 ^losey2021learning-056
- The alignment model was omitted in the case study because of the time constraints of the volunteer participants. (Losey et al., 2021) `ev:reported` p. 29 ^losey2021learning-057
- The authors recognise that communication delays and depth perception may affect the results of the remote case study. (Losey et al., 2021) `ev:asserted` p. 29 ^losey2021learning-058
- The Dessert task took both disabled users over 5 minutes with End-Effector control, but less than 2 minutes with LA+SA. (Losey et al., 2021) `ev:measured` p. 29 ^losey2021learning-059
- The free-form feedback of both disabled participants generally supported a subjective preference for LA+SA over End-Effector control. (Losey et al., 2021) `ev:measured` p. 30 ^losey2021learning-060
- A key limitation is that latent actions cannot be relied on when the user encounters a new task never seen during training. (Losey et al., 2021) `ev:asserted` p. 30 ^losey2021learning-061
- The authors note that retraining may let newly learned latent actions interfere with or override previously learned latent actions. (Losey et al., 2021) `ev:asserted` p. 30 ^losey2021learning-062

## 🎯 Contributions

## 📖 Glossary

- **Latent action** — low-DoF learned representation capturing the most salient aspects of high-DoF robot motion.
- **Conditioned variational autoencoder (cVAE)** — VAE whose decoder also takes the current context, here state and goal belief.
- **Shared autonomy** — control scheme blending human-commanded actions with autonomous assistance toward inferred goals.
- **Alignment model** — learned map from joystick inputs to latent actions matching an individual user's expectations.
- **Kinesthetic demonstration** — demonstration given by physically backdriving the robot through the desired motion.
- **Uniformly ultimately bounded stability** — guarantee that the state converges into, and stays within, a bounded ball.
- **End-effector teleoperation** — mode-switching control where joystick axes command end-effector linear or angular velocity.
- **HARMONIC dataset** — multimodal dataset of assistive human-robot collaboration used as shared autonomy baseline.

## ❓ Open questions

- How can latent actions be retrained on new tasks without interfering with or overriding previously learned latent actions?
- How much demonstration data is enough for learned latent actions to perform robustly, beyond the cVAE structure used here?
- Would the case study results with two disabled users hold in a larger, in-person study without remote latency and depth-perception issues?
- How does the full pipeline, including the personalised alignment model, perform with disabled users (the alignment was omitted in the case study)?
- Can latent actions be conditioned directly on visual perception so the goal set does not need to be specified separately?
- How should an assistive robot switch between learned latent actions and full end-effector control?

## 📝 Notes on reading

Read the arXiv v2 preprint (10 Jul 2021), which matches the packet identifier. The paper merges three earlier conference papers (ICRA, RSS, IROS) into one journal-style formalism.

Many headline results are only in figures and were described, not claimed: Sine and Rotate consistency R2 values, final-state error versus rationality (Fig. 11), goal-change and learner curves (Figs. 12-13), alignment error bars (Fig. 14), Likert ratings (Figs. 20, 21, 27), goal error and time bars (Figs. 22, 23, 25, 31, 32) and joystick heatmaps (Fig. 26). In the Dessert task (Fig. 21), direct teleoperation users stayed in a stabbing orientation while latent action users adjusted to scooping.

Inconsistencies inside the paper: Section 3 points to Table 3 for the main variables, but the table is Table 1; the Rotate R2 sentence reports two values both labelled cVAE; the alignment metric writes x_{t-1} in the formula while defining x_{t+1} as the actual end pose; the apple pie participants are described with an age range of 27.4±11.8 years, which is a mean and SD; the simulated shared autonomy section includes a real Franka arm under simulations with simulated humans. The first user study compares its ten participants against HARMONIC baseline data from 24 other people, so the comparison is between groups. The case study has only two participants and no statistics.

## Suggested new concepts

- Latent actions for teleoperation — a recurring idea of embedding high-DoF robot actions into a joystick-sized learned space.
- Shared autonomy — arbitration between human input and autonomous assistance is a core concept for assistive robots.
- Assistive eating robots — a distinct application domain with its own tasks, users and baselines.
- Semi-supervised control alignment with intuitive priors — a reusable way to personalise input mappings from few labels.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** Aprende acciones latentes de baja dimensión condicionadas al estado para controlar un brazo de 7 grados de libertad con un joystick de 2, versión robótica del control por la variedad.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
