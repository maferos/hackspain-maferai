---
aliases: []
type: "source"
title: "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World"
citekey: "Tobin2017domain"
doi: "10.48550/arXiv.1703.06907"
arxiv: "1703.06907"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1703.06907"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Josh Tobin", "Rachel Fong", "Alex Ray", "Jonas Schneider", "Wojciech Zaremba", "Pieter Abbeel"]
sha256: ["3fc98c5f4cea050686d45858e647e1b704492121fdae80f8fcd5d560c107f11f"]
pdf: "Content/Papers/Tobin2017domain.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 66
---

📄 PDF: [[Tobin2017domain.pdf]]

> [!abstract] One-sentence summary
> Training an object detector only on simulated images with heavily randomized non-realistic textures, camera and lighting yields about 1.5 cm real-world localization, enough for grasping in clutter, showing domain randomization can bridge the reality gap without real training data.

## Abstract

Bridging the 'reality gap' that separates simulated robotics from experiments on hardware could accelerate robotic research through improved data availability. This paper explores domain randomization, a simple technique for training models on simulated images that transfer to real images by randomizing rendering in the simulator. With enough variability in the simulator, the real world may appear to the model as just another variation. We focus on the task of object localization, which is a stepping stone to general robotic manipulation skills. We find that it is possible to train a real-world object detector that is accurate to $1.5$cm and robust to distractors and partial occlusions using only data from a simulator with non-realistic random textures. To demonstrate the capabilities of our detectors, we show they can be used to perform grasping in a cluttered environment. To our knowledge, this is the first successful transfer of a deep neural network trained only on simulated RGB images (without pre-training on real images) to the real world for the purpose of robotic control. (arXiv)

## 🧠 Key ideas (atomic)

- The paper tests whether models trained in a sufficiently varied simulation generalize to the real world with no additional training. (Tobin et al., 2017) `ev:asserted` p. 1 ^tobin2017domain-001
- System identification, tuning simulation parameters to match the physical system, is described by the authors as time-consuming and error-prone. (Tobin et al., 2017) `ev:asserted` p. 1 ^tobin2017domain-002
- [[Domain randomization]] trains a model on many randomized simulated environments instead of a single simulated environment to expose it to wide variability. (Tobin et al., 2017) `ev:asserted` p. 1 ^tobin2017domain-003
- The work focuses on transferring from low-fidelity simulated camera images, although [[Domain randomization|domain randomization]] could in principle apply to any reality-gap component. (Tobin et al., 2017) `ev:asserted` p. 1 ^tobin2017domain-004
- The authors view [[Sim-to-real transfer|sim-to-real transfer]] for object localization as a stepping stone to transferring general-purpose manipulation behaviors. (Tobin et al., 2017) `ev:asserted` p. 2 ^tobin2017domain-005
- For a range of geometric objects, a detector trained only on simulated data with simple generated textures reached around 1.5 cm real-world accuracy. (Tobin et al., 2017) `ev:measured` p. 2 ^tobin2017domain-006
- With a sufficient number of textures, pre-training the object detector on real images was found to be unnecessary. (Tobin et al., 2017) `ev:measured` p. 2 ^tobin2017domain-007
- The authors claim, to their knowledge, the first transfer of a deep network trained only on simulated RGB images to real-world robotic control. (Tobin et al., 2017) `ev:asserted` p. 2 ^tobin2017domain-008
- Compared with traditional pose estimation methods, the authors state their approach avoids the challenging problem of 3D reconstruction. (Tobin et al., 2017) `ev:asserted` p. 2 ^tobin2017domain-009
- Traditional approaches can detect full 3D object pose without assumptions about the location or size of the supporting surface, the authors note. (Tobin et al., 2017) `ev:asserted` p. 2 ^tobin2017domain-010
- Prior work found realistic RGB rendering alone had limited success for transferring models to real robotic tasks. (Tobin et al., 2017) `ev:cited` p. 2 ^tobin2017domain-011
- Unlike system-identification approaches, this method allows low-quality renderers optimized for speed and not carefully matched to real-world textures or lighting. (Tobin et al., 2017) `ev:asserted` p. 2 ^tobin2017domain-012
- Mitash and collaborators pretrained an object detector on realistic rendered images with randomized lighting, then used around 500 real-world samples. (Tobin et al., 2017) `ev:cited` p. 3 ^tobin2017domain-013
- Unlike domain adaptation and iterative learning control, the proposed method requires no additional training on real-world data. (Tobin et al., 2017) `ev:asserted` p. 3 ^tobin2017domain-014
- The authors state that their method can be combined easily with most domain adaptation techniques. (Tobin et al., 2017) `ev:asserted` p. 3 ^tobin2017domain-015
- Mordatch and collaborators showed that training a policy on an ensemble of dynamics models can improve transfer to a real robot. (Tobin et al., 2017) `ev:cited` p. 3 ^tobin2017domain-016
- Most computer vision object detection work uses realistic textures but renders objects against solid backgrounds or random photographs rather than coherent 3D scenes. (Tobin et al., 2017) `ev:asserted` p. 3 ^tobin2017domain-017
- Sadeghi and Levine transferred an image-to-control policy learned in varied simulated 3D scenes to real-world quadrotor flight. (Tobin et al., 2017) `ev:cited` p. 3 ^tobin2017domain-018
- The authors note that Sadeghi and Levine's collision-avoidance experiments do not demonstrate the ability to handle high-precision tasks. (Tobin et al., 2017) `ev:asserted` p. 3 ^tobin2017domain-019
- The authors claim to be the first to use only non-realistic textures created by a simple random generation process. (Tobin et al., 2017) `ev:asserted` p. 3 ^tobin2017domain-020
- The goal is an object detector mapping a single monocular camera frame to the Cartesian coordinates of each object of interest. (Tobin et al., 2017) `ev:reported` p. 3 ^tobin2017domain-021
- Each training sample randomizes number and shape of distractors, object positions and textures, camera pose and field of view, lights, and image noise. (Tobin et al., 2017) `ev:reported` p. 3 ^tobin2017domain-022
- Random textures are a random RGB value, a gradient between two random RGB values, or a checker pattern between two. (Tobin et al., 2017) `ev:reported` p. 3 ^tobin2017domain-023
- The table height is fixed in simulation, effectively creating a 2D pose estimation task from an uncalibrated monocular camera. (Tobin et al., 2017) `ev:reported` p. 3 ^tobin2017domain-024
- The detector does not see the color of objects of interest at training time, only their size and shape. (Tobin et al., 2017) `ev:reported` p. 3 ^tobin2017domain-025
- Images are rendered with the MuJoCo physics engine's built-in renderer, which is not intended to be photo-realistic. (Tobin et al., 2017) `ev:reported` p. 3 ^tobin2017domain-026
- Between 0 and 10 distractor objects are added to the table in each simulated training scene. (Tobin et al., 2017) `ev:reported` p. 4 ^tobin2017domain-027
- Each training sample places the camera randomly within a (10 × 5 × 10) cm box around a manually placed initial point. (Tobin et al., 2017) `ev:reported` p. 4 ^tobin2017domain-028
- The camera viewing angle is offset by up to 0.1 radians in each direction from pointing at a fixed table point. (Tobin et al., 2017) `ev:reported` p. 4 ^tobin2017domain-029
- The camera field of view is scaled by up to 5 % from the starting point during training. (Tobin et al., 2017) `ev:reported` p. 4 ^tobin2017domain-030
- The detector is a modified VGG-16 with standard convolutional layers, smaller fully connected layers of sizes 256 and 64, and no dropout. (Tobin et al., 2017) `ev:reported` p. 4 ^tobin2017domain-031
- In practice, random weight initialization of the convolutional layers worked as well as ImageNet pretraining in most cases. (Tobin et al., 2017) `ev:measured` p. 4 ^tobin2017domain-032
- The detector is trained on the L2 loss between estimated and true object positions using the Adam optimizer. (Tobin et al., 2017) `ev:reported` p. 4 ^tobin2017domain-033
- A learning rate of around 1e−4 improved convergence and helped avoid a local optimum mapping all objects to the table center. (Tobin et al., 2017) `ev:measured` p. 4 ^tobin2017domain-034
- Detectors were trained for each of eight geometric objects, with mesh representations constructed for rendering in the simulator. (Tobin et al., 2017) `ev:reported` p. 4 ^tobin2017domain-035
- Each experiment ran a small hyperparameter search over two learning rates (1e−4 and 2e−4) and three batch sizes (25, 50, and 100). (Tobin et al., 2017) `ev:reported` p. 4 ^tobin2017domain-036
- The real-world test set contains 480 webcam images of geometric objects on a table 70 cm to 105 cm from the camera. (Tobin et al., 2017) `ev:reported` p. 4 ^tobin2017domain-037
- Lighting conditions and the scene around the table were not controlled in the real-world test images. (Tobin et al., 2017) `ev:reported` p. 4 ^tobin2017domain-038
- Each of the eight objects has 60 labeled images: 20 alone, 20 with distractors, and 20 partially occluded. (Tobin et al., 2017) `ev:reported` p. 5 ^tobin2017domain-039
- In Table I, the hexagonal prism detector reached a detection error of 0.7 ± 0.5 cm with the object alone on the table. (Tobin et al., 2017) `ev:measured` p. 4 ^tobin2017domain-040
- The tetrahedron detector's error rose to 3.2 ± 5.8 cm under partial occlusion in Table I. (Tobin et al., 2017) `ev:measured` p. 4 ^tobin2017domain-041
- For several object categories, the best final performance in Table I came from a detector trained from scratch. (Tobin et al., 2017) `ev:measured` p. 4 ^tobin2017domain-042
- The object detectors localize objects to within 1.5 cm on average in the real world. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-043
- The detectors still overfit the simulated training data, where the localization error is 0.3 cm to 0.5 cm. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-044
- The authors state the accuracy is comparable to traditional single-camera pose estimation in clutter that uses higher-resolution images. (Tobin et al., 2017) `ev:asserted` p. 5 ^tobin2017domain-045
- The ablation found the method at least somewhat sensitive to all studied factors except the use of random noise. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-046
- Using a pre-trained model, relatively accurate real-world detection was achieved with as few as 5, 000 simulated training samples. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-047
- Performance of the pre-trained model improved with more simulated training samples up to around 50, 000 samples. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-048
- With large training data, random weight initialization achieved nearly the same real-world transfer performance as pre-trained weight initialization. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-049
- Using a pre-trained model can significantly improve real-world detection performance when less simulated training data is used. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-050
- With 10, 000 training examples, performance degraded significantly when fewer than 1, 000 unique textures were used in training. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-051
- The authors conclude a large number of random textures is necessary to achieve transfer in their experiments. (Tobin et al., 2017) `ev:asserted` p. 5 ^tobin2017domain-052
- With 1, 000 random textures, training on 10, 000 images performed comparably to training on only 1, 000 images. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-053
- The authors infer that in the low data regime, [[Domain randomization|texture randomization]] is more important than object position randomization. (Tobin et al., 2017) `ev:asserted` p. 5 ^tobin2017domain-054
- Incorporating distractors during training appears critical to resilience to distractors in the real world, according to the ablation. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-055
- Adding noise during pretraining appears to have a negligible effect on real-world detection error in the ablation. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-056
- Adding a small amount of random noise at training time improved convergence and made training less susceptible to local minima. (Tobin et al., 2017) `ev:measured` p. 5 ^tobin2017domain-057
- Removing distractors from training raised the average error with real distractors from 1.8 ± 1.7 cm to 7.2 ± 4.5 cm. (Tobin et al., 2017) `ev:measured` p. 6 ^tobin2017domain-058
- Without camera randomization, the object-only error was 2.0 ± 2.1 cm versus 1.3 ± 0.6 cm for the full method. (Tobin et al., 2017) `ev:measured` p. 6 ^tobin2017domain-059
- Each model compared in the Table II ablation was trained with 20, 000 simulated training examples. (Tobin et al., 2017) `ev:reported` p. 6 ^tobin2017domain-060
- Grasping was evaluated for two of the most consistently accurate detectors in 20 increasingly cluttered scenes with off-the-shelf motion planning. (Tobin et al., 2017) `ev:reported` p. 6 ^tobin2017domain-061
- On a Fetch robot, the pipeline detected and picked up the target object in 38 out of 40 trials. (Tobin et al., 2017) `ev:measured` p. 6 ^tobin2017domain-062
- A detector trained to localize a YCB Spam can ignored previously unseen food-item distractors and picked up the target in 9 of 10 trials. (Tobin et al., 2017) `ev:measured` p. 6 ^tobin2017domain-063
- The authors conclude that an object detector trained only in simulation can be accurate enough in the real world to grasp in clutter. (Tobin et al., 2017) `ev:asserted` p. 6 ^tobin2017domain-064
- Future work will explore making the technique reliable enough for contact-rich manipulation or higher-precision tasks. (Tobin et al., 2017) `ev:asserted` p. 6 ^tobin2017domain-065
- The authors suggest [[Domain randomization|domain randomization]] could be an important tool for making deep reinforcement learning policies useful on real robots. (Tobin et al., 2017) `ev:asserted` p. 6 ^tobin2017domain-066

## 🎯 Contributions

## 📖 Glossary

- **Reality gap** — Discrepancies between simulation and the real world that hinder transferring learned behaviors.
- **Domain randomization** — Randomizing simulator rendering and scene parameters so real data looks like another variation.
- **System identification** — Tuning simulation parameters to match the behavior of the physical system.
- **Distractor object** — A non-target object placed in the scene that the detector must ignore.
- **Domain adaptation** — Adapting a model trained in a source domain to a different target domain.
- **Iterative learning control** — Using real-world data to repeatedly improve the dynamics model driving the controller.

## ❓ Open questions

- Can domain randomization reach the precision needed for contact-rich manipulation tasks?
- Would higher-resolution frames, multiple viewpoints, stereo or depth close the remaining sim-to-real overfitting gap?
- How does domain randomization combine with domain adaptation techniques in practice?
- Does the approach extend from 2D position (fixed table height) to full 3D pose estimation?
- Which additional texture, lighting and rendering randomizations bring the largest gains?

## 📝 Notes on reading

Read the arXiv v1 preprint (1703.06907v1, 20 Mar 2017), matching the packet identifier. Table I (p. 4) marks some values with a footnote superscript 1 appended to the standard deviation in the extracted text (e.g. `0.6 ± 0.31` likely means 0.6 ± 0.3 with footnote 1, detector trained from scratch); those cells were not claimed individually. Figures 4 and 5 (p. 5) are curves of test error against training set size and number of unique textures; only the values stated in the text were claimed. Figures 1, 3, 6 and 7 are illustrative images. Large numbers are extracted with a space after the thousands comma (e.g. `10, 000`). Table II's full-method errors (e.g. 2.4 ± 3.0 cm with occlusions) do not match the per-object Table I values; Table II models used 20, 000 training examples, while the Table I training set size is not stated. The text on p. 5 says noise was added during pretraining, which is ambiguous with training.

## Suggested new concepts

- Domain randomization — core sim-to-real technique introduced here for vision, widely reused in robot learning.
- Reality gap — the recurring framing of sim-to-real transfer problems across robotics papers.
- Sim-to-real transfer — the broader problem class that domain randomization, adaptation and system identification address.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Fundamento de la aleatorización de dominio (§6.5)
