---
aliases: []
type: "source"
title: "Closed-Loop Robotic Manipulation of Transparent Substrates for Self-Driving Laboratories using Deep Learning Micro-Error Correction"
citekey: "Fontenot2025closed"
doi: "10.48550/arXiv.2512.06038"
arxiv: "2512.06038"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2512.06038"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Kelsey Fontenot", "Anjali Gorti", "Iva Goel", "Tonio Buonassisi", "Alexander E. Siemenn"]
sha256: ["5722ae9c9a312b727900ccab4e6b252ea39a7c10f7f574266e9a7c33e9f6e5df"]
pdf: "Content/Papers/Fontenot2025closed.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 66
---

📄 PDF: [[Fontenot2025closed.pdf]]

> [!abstract] One-sentence summary
> The paper builds ASHE, a closed-loop robotic system that reloads fragile transparent glass substrates into a self-driving lab, using lateral blue illumination and a fused geometric/CNN detector to catch and correct placement errors, reaching 98.5% first-time accuracy over 130 trials.

## Abstract

Self-driving laboratories (SDLs) have accelerated the throughput and automation capabilities for discovering and improving chemistries and materials. Although these SDLs have automated many of the steps required to conduct chemical and materials experiments, a commonly overlooked step in the automation pipeline is the handling and reloading of substrates used to transfer or deposit materials onto for downstream characterization. Here, we develop a closed-loop method of Automated Substrate Handling and Exchange (ASHE) using robotics, dual-actuated dispensers, and deep learning-driven computer vision to detect and correct errors in the manipulation of fragile and transparent substrates for SDLs. Using ASHE, we demonstrate a 98.5% first-time placement accuracy across 130 independent trials of reloading transparent glass substrates into an SDL, where only two substrate misplacements occurred and were successfully detected as errors and automatically corrected. Through the development of more accurate and reliable methods for handling various types of substrates, we move toward an improvement in the automation capabilities of self-driving laboratories, furthering the acceleration of novel chemical and materials discoveries. (arXiv)

## 🧠 Key ideas (atomic)

- Laboratory automation and self-driving laboratories have emerged in recent years as solutions to accelerate chemical and materials discovery research. (Fontenot et al., 2025) `ev:cited` p. 1 ^fontenot2025closed-001
- Replacing a used substrate with a fresh one for the next deposition round is an important but often overlooked sub-task of an SDL. (Fontenot et al., 2025) `ev:cited` p. 1 ^fontenot2025closed-002
- Without automation, the substrate replacement process must be conducted via human intervention, which bottlenecks the SDL pipeline. (Fontenot et al., 2025) `ev:asserted` p. 1 ^fontenot2025closed-003
- Autonomous substrate replacement becomes significantly more challenging for thin, fragile, transparent glass or silica substrates often used with conductive materials. (Fontenot et al., 2025) `ev:cited` p. 2 ^fontenot2025closed-004
- Transparent object detection remains a key challenge for segmentation models such as YOLO or SAM, owing to difficulty resolving object edges in ambient lighting. (Fontenot et al., 2025) `ev:cited` p. 2 ^fontenot2025closed-005
- Existing transparent-object detection methods largely focus on 3D curved glass objects such as beakers, exploiting warping and distortion for easier detection. (Fontenot et al., 2025) `ev:asserted` p. 3 ^fontenot2025closed-006
- Transparent substrates used for materials experiments are often thin and flat, offering no curvature for detection models to hone in on. (Fontenot et al., 2025) `ev:asserted` p. 3 ^fontenot2025closed-007
- The authors argue further refinements are still required to reliably detect nearly featureless thin, flat transparent substrates within SDLs. (Fontenot et al., 2025) `ev:asserted` p. 3 ^fontenot2025closed-008
- On its hardware end, ASHE uses a 5-DOF robotic arm, a specialized deformable gripper, plus a dual-actuated substrate dispenser. (Fontenot et al., 2025) `ev:reported` p. 3 ^fontenot2025closed-009
- On its software end, ASHE classifies failed or successful placements with a fused geometric and deep learning model under lateral illumination. (Fontenot et al., 2025) `ev:reported` p. 3 ^fontenot2025closed-010
- ASHE is commanded via updates to an SQL database, enabling modular integration into an existing SDL architecture wirelessly or through serial communication. (Fontenot et al., 2025) `ev:reported` p. 4 ^fontenot2025closed-011
- ASHE uses the UFACTORY xArm 5, a 5-DOF arm chosen partly for its positional repeatability of 0.1 mm. (Fontenot et al., 2025) `ev:reported` p. 4 ^fontenot2025closed-012
- A limit switch pressed by the SDL transporter changes the SQL state variable to 1, activating the path plan of ASHE. (Fontenot et al., 2025) `ev:reported` p. 4 ^fontenot2025closed-013
- The arm first disposes used substrates into a waste bin, then grasps a fresh substrate, then places it on the transporter. (Fontenot et al., 2025) `ev:reported` p. 4 ^fontenot2025closed-014
- Vacuum grippers were avoided since they contact the top of the substrates rather than their sides. (Fontenot et al., 2025) `ev:reported` p. 4 ^fontenot2025closed-015
- Custom 3D-printed fingers use rigid PLA for positioning precision, with deformable TPU 95A tips that compress during grasping to avoid fracture. (Fontenot et al., 2025) `ev:reported` p. 4 ^fontenot2025closed-016
- The authors note that fingers with four side contact points improve grasping with deformable TPU tips, giving a more secure grasp. (Fontenot et al., 2025) `ev:asserted` p. 4 ^fontenot2025closed-017
- The dispenser stack can hold over 300 glass substrates of size 50.8 mm × 76.2 mm × 1.0 mm. (Fontenot et al., 2025) `ev:reported` p. 4 ^fontenot2025closed-018
- The dispenser is controlled by an Arduino Due microprocessor with L293D motor drivers positioning its two linear actuators. (Fontenot et al., 2025) `ev:reported` p. 4 ^fontenot2025closed-019
- A transfer plate lip approximately 0.2 mm thinner than each substrate pushes only the lower-most substrate out of the vertical hotel. (Fontenot et al., 2025) `ev:reported` p. 4 ^fontenot2025closed-020
- A vertical actuator blocks the return path, so the dispensed substrate stays in place while the horizontal actuator retracts. (Fontenot et al., 2025) `ev:reported` p. 5 ^fontenot2025closed-021
- The authors state that misplacing a substrate would cause downstream failures such as misaligned material dispensing or erroneous characterization readings. (Fontenot et al., 2025) `ev:asserted` p. 5 ^fontenot2025closed-022
- Lateral blue light illumination in the dark creates a bright boundary at substrate edges through refraction and diffusion within the substrate. (Fontenot et al., 2025) `ev:reported` p. 5 ^fontenot2025closed-023
- ASHE images the laterally illuminated transparent substrates with an Intel RealSense D435 camera after the robotic arm places them. (Fontenot et al., 2025) `ev:reported` p. 5 ^fontenot2025closed-024
- If either the geometric model or the CNN detects a failed placement, the arm removes the substrate and places a fresh one. (Fontenot et al., 2025) `ev:reported` p. 5 ^fontenot2025closed-025
- The geometric model detects transporter slot edges using Canny edge detection with a wide hysteresis threshold of (30, 300). (Fontenot et al., 2025) `ev:reported` p. 5 ^fontenot2025closed-026
- Noisy edges that do not meet a length threshold of at least 100 pixels are pruned from the slot edge map. (Fontenot et al., 2025) `ev:reported` p. 6 ^fontenot2025closed-027
- Substrate edges are obtained from a blue colour mask, Canny detection and a Hough transform, then bound by a convex hull. (Fontenot et al., 2025) `ev:reported` p. 6 ^fontenot2025closed-028
- Slot and substrate segmentation are repeated across 100 sampled RealSense frames to account for noise in the image and scene. (Fontenot et al., 2025) `ev:reported` p. 6 ^fontenot2025closed-029
- The geometric model outputs a failed placement when slot and substrate areas overlap by less than 90%, a threshold set empirically. (Fontenot et al., 2025) `ev:reported` p. 6 ^fontenot2025closed-030
- The CNN dataset consists of 1990 captured images, with 996 failure cases and 994 success cases before augmentation. (Fontenot et al., 2025) `ev:reported` p. 7 ^fontenot2025closed-031
- Images are cropped from 1920 × 1080 pixels to a 380 × 250 pixel region along the substrate edge far from the LED. (Fontenot et al., 2025) `ev:reported` p. 7 ^fontenot2025closed-032
- The authors note that cropping improves CNN performance by zooming in on regions with denser information about placement accuracy. (Fontenot et al., 2025) `ev:asserted` p. 7 ^fontenot2025closed-033
- Data augmentation generated 15 mutations per image, resulting in a total CNN dataset size of 29,850 images. (Fontenot et al., 2025) `ev:reported` p. 7 ^fontenot2025closed-034
- The dataset was split into 80% training and 20% validation subsets before augmentation to prevent data leakage. (Fontenot et al., 2025) `ev:reported` p. 7 ^fontenot2025closed-035
- A weighted cross-entropy loss was used to account for imbalance between success images and augmented failure images. (Fontenot et al., 2025) `ev:reported` p. 7 ^fontenot2025closed-036
- The CNN reshapes inputs to 96 × 96 and passes them through five convolutional layers, the last using 128 filters. (Fontenot et al., 2025) `ev:reported` p. 7 ^fontenot2025closed-037
- The model was trained with a learning rate of 1 × 10−3 and a batch size of 32 over 50 epochs. (Fontenot et al., 2025) `ev:reported` p. 8 ^fontenot2025closed-038
- At test time, the CNN returns the median placement success score across 100 frames sampled from the camera live stream. (Fontenot et al., 2025) `ev:reported` p. 8 ^fontenot2025closed-039
- The CNN classifies a placement as a success when the median score exceeds 60%, a threshold chosen after empirical testing. (Fontenot et al., 2025) `ev:reported` p. 8 ^fontenot2025closed-040
- Small rotational errors had an angle mismatch below approximately 1.7◦, while large ones exceeded approximately 5.4◦. (Fontenot et al., 2025) `ev:reported` p. 8 ^fontenot2025closed-041
- Small translational errors had a displacement below approximately 2.4 mm, while large ones exceeded approximately 5.6 mm. (Fontenot et al., 2025) `ev:reported` p. 8 ^fontenot2025closed-042
- Across 36 unique placement errors, the geometric model and the CNN performed similarly on rotational versus translational errors. (Fontenot et al., 2025) `ev:measured` p. 8 ^fontenot2025closed-043
- The geometric model correctly detected 19 of the 20 large placement errors, with only one false positive. (Fontenot et al., 2025) `ev:measured` p. 8 ^fontenot2025closed-044
- The geometric model's false positive had a counter-clockwise rotational error of 1.8◦ with a translational error of 2.7 mm. (Fontenot et al., 2025) `ev:measured` p. 8 ^fontenot2025closed-045
- The CNN correctly detected all 20 large errors, with a prediction confidence of 100% for every large-error image. (Fontenot et al., 2025) `ev:measured` p. 8 ^fontenot2025closed-046
- The geometric model correctly detected none of the 12 medium errors, outputting false positives for all 12 images. (Fontenot et al., 2025) `ev:measured` p. 8 ^fontenot2025closed-047
- The geometric model correctly detected none of the 4 small errors, outputting false positives for all 4 images. (Fontenot et al., 2025) `ev:measured` p. 8 ^fontenot2025closed-048
- The CNN correctly detected all 12 medium errors with a prediction confidence ranging from 97% to 100%. (Fontenot et al., 2025) `ev:measured` p. 8 ^fontenot2025closed-049
- The CNN correctly detected all 4 small errors with a prediction confidence ranging from 99% to 100%. (Fontenot et al., 2025) `ev:measured` p. 8 ^fontenot2025closed-050
- Both the geometric model and the CNN correctly classified the single successful placement image as a success. (Fontenot et al., 2025) `ev:measured` p. 8 ^fontenot2025closed-051
- On 10 pre-programmed placement failures, ASHE correctly classified all 10 first placement attempts as failures. (Fontenot et al., 2025) `ev:measured` p. 9 ^fontenot2025closed-052
- All 10 automated corrective procedures successfully corrected the placement failures on the second attempt, according to the vision system. (Fontenot et al., 2025) `ev:measured` p. 9 ^fontenot2025closed-053
- Across 130 reloading cycles without pre-programmed failures, ASHE classified 128 placements as successful on the first attempt. (Fontenot et al., 2025) `ev:measured` p. 9 ^fontenot2025closed-054
- A human domain expert monitored every placement result and validated all 128 success classifications as correct. (Fontenot et al., 2025) `ev:measured` p. 9 ^fontenot2025closed-055
- Across the 130 independent reloading experiments, ASHE achieved a 98.5% first-time placement accuracy for transparent glass substrates. (Fontenot et al., 2025) `ev:measured` p. 10 ^fontenot2025closed-056
- ASHE classified the remaining 2 of 130 substrates as failures, a classification the human domain expert validated. (Fontenot et al., 2025) `ev:measured` p. 10 ^fontenot2025closed-057
- Through closed-loop detection and auto-correction, 100% of the substrates were placed correctly into the target slot by the second attempt. (Fontenot et al., 2025) `ev:measured` p. 10 ^fontenot2025closed-058
- The authors note the results transfer to substrates with surface treatments such as hydrophobic Teflon coatings or hydrophilic plasma treatments. (Fontenot et al., 2025) `ev:asserted` p. 10 ^fontenot2025closed-059
- The authors state that ASHE tends to overgeneralize, classifying successfully placed substrates as failures rather than producing false positives. (Fontenot et al., 2025) `ev:asserted` p. 11 ^fontenot2025closed-060
- False negatives are considered preferable, since the automated correction mechanism reloads a substrate upon any failure classification. (Fontenot et al., 2025) `ev:asserted` p. 11 ^fontenot2025closed-061
- The hardware and software were designed and trained for one particular glass substrate size of 50.8 mm × 76.2 mm × 1.0 mm. (Fontenot et al., 2025) `ev:asserted` p. 11 ^fontenot2025closed-062
- Extending ASHE to other substrates would require redesigning the actuated dispenser along with the gripper fingers, the authors state. (Fontenot et al., 2025) `ev:asserted` p. 11 ^fontenot2025closed-063
- Extending ASHE to other substrates would also require retraining the deep learning model on a newly collected dataset. (Fontenot et al., 2025) `ev:asserted` p. 11 ^fontenot2025closed-064
- Wider adoption may be inhibited by costs, chiefly the UFACTORY xARM 5 at $6000 USD with its gripper at $2300 USD. (Fontenot et al., 2025) `ev:asserted` p. 11 ^fontenot2025closed-065
- The code and data presented in the article are publicly available on GitHub in the PV-Lab ASHE repository. (Fontenot et al., 2025) `ev:reported` p. 11 ^fontenot2025closed-066

## 🎯 Contributions

## 📖 Glossary

- **Self-driving laboratory (SDL)** — Automated lab where robots and software plan, run and analyse experiments with little human input.
- **Substrate** — Plate or slide onto which materials are deposited for downstream characterization.
- **Transporter** — The SDL holder that moves a substrate between subsystems; ASHE loads its target slot.
- **Lateral illumination** — Lighting a transparent substrate from its side so light emerges along its edges.
- **Leader-follower control** — Scheme where a state variable set by the SDL triggers ASHE's actions.
- **Canny edge detection** — Gradient-based edge detector using hysteresis thresholds to keep strong and connected faint edges.
- **Hough transform** — Technique that recovers straight lines or shapes from an edge image.
- **Convex hull** — Smallest convex polygon enclosing a set of points or edge segments.
- **False positive (here)** — A misplaced substrate wrongly classified as a successful placement.

## ❓ Open questions

- How does the fused detector perform on substrates of other sizes, thicknesses or materials without retraining?
- How many placement errors does the full system miss over much longer campaigns than 130 cycles?
- What is the false-negative rate of the CNN on correct placements, given the authors say it overgeneralizes failures?
- Is the relative rotation mismatch computed by the geometric model used in its decision, and with what threshold?
- Could a cheaper arm with lower repeatability than 0.1 mm still achieve comparable placement accuracy?
- How sensitive is lateral blue illumination to ambient light when the SDL enclosure is not dark?

## 📝 Notes on reading

Read the arXiv v1 preprint (2512.06038v1, 4 Dec 2025), which matches the packet identifier.

Fractions in the results (p. 8–10) are extracted as stacked numerators and denominators (for example `19` / `20`, `128` / `130`); claims restate them as "19 of the 20" and similar.

Figure 7 (p. 9) is a matrix of 36 placement-error images with GM and CNN labels and CNN confidences; the per-image values were not claimed beyond the text summary. Figure 8 (p. 10) shows placement success scores with 25th–75th percentile error bars across 100 frames; only the counts stated in the text were claimed.

Small inconsistencies: p. 6 says the GM fails a placement if shapes have "either" an area overlap below 90%, but names no second criterion even though relative rotation mismatch is computed. The Figure 8 caption calls the plotted value the median confidence of the fused GM-CNN model, while the text and the same caption also say the score comes from the CNN's prediction confidence. The discussion's 97% to 100% confidence range for the fused model covers the medium and small CNN results reported on p. 8.

The claim that results transfer to Teflon-coated and plasma-treated substrates (p. 10) is stated without data shown.

## Suggested new concepts

- Transparent object detection — recurring computer-vision problem relevant to lab glassware and substrate handling.
- Closed-loop error correction in lab robotics — detect-and-retry pattern for reliable autonomous manipulation.
- Lateral illumination for edge detection — cheap optical trick making transparent objects visible to vision models.
- Substrate handling in self-driving laboratories — overlooked automation sub-task that bottlenecks SDL pipelines.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H7.** Muestra la corrección de errores por visión en lazo cerrado para vidrio transparente en un self-driving lab (98,5 % de colocaciones correctas al primer intento).
