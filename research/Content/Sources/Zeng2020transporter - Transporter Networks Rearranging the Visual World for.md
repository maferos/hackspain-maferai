---
aliases: []
type: "source"
title: "Transporter Networks: Rearranging the Visual World for Robotic Manipulation"
citekey: "Zeng2020transporter"
doi: "10.48550/arXiv.2010.14406"
arxiv: "2010.14406"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2010.14406"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Andy Zeng", "Pete Florence", "Jonathan Tompson", "Stefan Welker", "Jonathan Chien", "Maria Attarian", "Travis Armstrong", "Ivan Krasin", "Dan Duong", "Ayzaan Wahid", "Vikas Sindhwani", "Johnny Lee"]
sha256: ["3a5e78b5c8881863845c46bda0bf8c9071aa79a59a6f9a9f4d8732690482b228"]
pdf: "Content/Papers/Zeng2020transporter.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Zeng2020transporter.pdf]]

> [!abstract] One-sentence summary
> Transporter Networks cast vision-based manipulation as predicting spatial displacements by cross-correlating deep features of a crop around the pick with an orthographic top-down scene, giving far better sample efficiency than end-to-end baselines on the new Ravens benchmark and near-99% success on two real-robot tasks.

## Abstract

Robotic manipulation can be formulated as inducing a sequence of spatial displacements: where the space being moved can encompass an object, part of an object, or end effector. In this work, we propose the Transporter Network, a simple model architecture that rearranges deep features to infer spatial displacements from visual input - which can parameterize robot actions. It makes no assumptions of objectness (e.g. canonical poses, models, or keypoints), it exploits spatial symmetries, and is orders of magnitude more sample efficient than our benchmarked alternatives in learning vision-based manipulation tasks: from stacking a pyramid of blocks, to assembling kits with unseen objects; from manipulating deformable ropes, to pushing piles of small objects with closed-loop feedback. Our method can represent complex multi-modal policy distributions and generalizes to multi-step sequential tasks, as well as 6DoF pick-and-place. Experiments on 10 simulated tasks show that it learns faster and generalizes better than a variety of end-to-end baselines, including policies that use ground-truth object poses. We validate our methods with hardware in the real world. Experiment videos and code are available at https://transporternets.github.io (arXiv)

## 🧠 Key ideas (atomic)

- The paper formulates robotic manipulation as inducing a sequence of spatial displacements of objects, object parts, or end effectors. (Zeng et al., 2020) `ev:asserted` p. 1 ^zeng2020transporter-001
- End-to-end models mapping pixels to actions can learn complex manipulation skills but are known to require copious amounts of data. (Zeng et al., 2020) `ev:cited` p. 1 ^zeng2020transporter-002
- Object-centric representations still struggle with unseen object classes, occluded objects, highly deformable objects, or piles of small objects. (Zeng et al., 2020) `ev:cited` p. 1 ^zeng2020transporter-003
- Transporter Networks learn to attend to a local region, then predict its target spatial displacement via deep feature template matching. (Zeng et al., 2020) `ev:asserted` p. 1 ^zeng2020transporter-004
- The method uses 3D reconstruction to project visual data onto a spatially consistent representation to better exploit equivariance for more efficient learning. (Zeng et al., 2020) `ev:asserted` p. 1 ^zeng2020transporter-005
- On 10 tabletop tasks, Transporter Networks trained from scratch achieve greater than 90% success on most tasks using 100 expert demonstrations. (Zeng et al., 2020) `ev:measured` p. 2 ^zeng2020transporter-006
- The authors extend the method to 6DoF tasks by combining 3DoF Transporter Networks with continuous regression for the remaining degrees of freedom. (Zeng et al., 2020) `ev:reported` p. 2 ^zeng2020transporter-007
- Ravens, the authors' new simulated benchmark, features a Gym-like API with a built-in stochastic oracle to evaluate imitation learning sample efficiency. (Zeng et al., 2020) `ev:reported` p. 2 ^zeng2020transporter-008
- Object detectors and pose estimators often require object-specific training data, making them difficult to scale to applications with unseen objects. (Zeng et al., 2020) `ev:cited` p. 2 ^zeng2020transporter-009
- The paper's primary contribution is pick-conditioned placing via transporting, one of two subproblems into which pick-and-place is decomposed. (Zeng et al., 2020) `ev:asserted` p. 3 ^zeng2020transporter-010
- The method assumes no prior information about objects, such as 3D models, poses, class categories, or keypoints. (Zeng et al., 2020) `ev:reported` p. 3 ^zeng2020transporter-011
- Picking is modelled with fully convolutional networks predicting an action-value function over pixels, whose argmax gives the pick pose. (Zeng et al., 2020) `ev:reported` p. 3 ^zeng2020transporter-012
- FCNs are translationally equivariant, so translating an object in the scene also translates its picking pose. (Zeng et al., 2020) `ev:asserted` p. 3 ^zeng2020transporter-013
- RGB-D images are converted into a spatially consistent orthographic projection in which each pixel represents a fixed window of 3D space. (Zeng et al., 2020) `ev:reported` p. 3 ^zeng2020transporter-014
- Placing is formulated as template matching, cross-correlating deep features of a crop around the pick with dense features of the scene. (Zeng et al., 2020) `ev:reported` p. 4 ^zeng2020transporter-015
- The authors state the placing equation is invariant to the pick pose, enabling pick-conditioned placing to be learned from few examples. (Zeng et al., 2020) `ev:asserted` p. 4 ^zeng2020transporter-016
- Planar rotations are handled by discretizing SO(2) into k bins, running the FCN once per rotated observation with shared weights. (Zeng et al., 2020) `ev:reported` p. 4 ^zeng2020transporter-017
- Fully discretizing the six-dimensional SE(3) space to handle all rigid-object degrees of freedom becomes infeasible due to the curse of dimensionality. (Zeng et al., 2020) `ev:asserted` p. 4 ^zeng2020transporter-018
- SE(3) placing first resolves three SE(2) degrees of freedom, then regresses the remaining rx, ry, z-height values using three cross-correlation channels. (Zeng et al., 2020) `ev:reported` p. 5 ^zeng2020transporter-019
- Completing 3-disk Towers of Hanoi requires correctly sequencing 7 pick-and-place actions in the authors' setup. (Zeng et al., 2020) `ev:reported` p. 5 ^zeng2020transporter-020
- Although the method is stateless, experiments show it can learn sequencing behaviors through visual feedback. (Zeng et al., 2020) `ev:measured` p. 5 ^zeng2020transporter-021
- Extending Transporter Networks with memory to handle non-Markovian tasks is identified by the authors as interesting future work. (Zeng et al., 2020) `ev:asserted` p. 5 ^zeng2020transporter-022
- The authors' results suggest that rigid displacements can serve as a useful prior for non-rigid ones, such as rope or pile dynamics. (Zeng et al., 2020) `ev:asserted` p. 5 ^zeng2020transporter-023
- The top-down observation has a 160×320 pixel resolution, each pixel representing a 3.125×3.125mm column of the 0.5×1m tabletop workspace. (Zeng et al., 2020) `ev:reported` p. 5 ^zeng2020transporter-024
- The picking model is an hourglass encoder-decoder 43-layer ResNet with 12 residual blocks, 8-stride, followed by image-wide softmax. (Zeng et al., 2020) `ev:reported` p. 5 ^zeng2020transporter-025
- The placing model is a two-stream FCN in which each stream is an 8-stride 43-layer ResNet producing dense feature maps. (Zeng et al., 2020) `ev:reported` p. 5 ^zeng2020transporter-026
- In-plane placing rotations are discretized into k=36 angles, multiples of 10 degrees, in the SE(2) Transporter Network. (Zeng et al., 2020) `ev:reported` p. 5 ^zeng2020transporter-027
- Total inference time with both picking and placing models amounts to 200ms on an Nvidia GTX 2080 GPU. (Zeng et al., 2020) `ev:measured` p. 6 ^zeng2020transporter-028
- The training loss is cross-entropy between the models' image-wide softmax outputs versus one-hot pixel maps of demonstrated pick or place poses. (Zeng et al., 2020) `ev:reported` p. 6 ^zeng2020transporter-029
- Each model is trained on a single task from n = 1, 10, 100, or 1,000 demonstrations, without task-specific information as input. (Zeng et al., 2020) `ev:reported` p. 6 ^zeng2020transporter-030
- Ravens is built with PyBullet around a simulated UR5e with a suction gripper viewed by 3 simulated 640x480 RGB-D cameras. (Zeng et al., 2020) `ev:reported` p. 6 ^zeng2020transporter-031
- Reported results use the highest-validation-performance model per task, averaged over 100 unseen test runs, scored from 0 to 100. (Zeng et al., 2020) `ev:reported` p. 6 ^zeng2020transporter-032
- Baselines include Form2Fit, ConvMLP, plus GT-State MLP variants that consume ground-truth object poses instead of images. (Zeng et al., 2020) `ev:reported` p. 7 ^zeng2020transporter-033
- All methods, including Transporter Networks, use identical data augmentation with random SE(2) world-frame transforms in the benchmark comparisons. (Zeng et al., 2020) `ev:reported` p. 7 ^zeng2020transporter-034
- Most baselines can over-fit the demonstration training set yet generalize poorly to unseen settings with only 1,000 demonstrations. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-035
- In general, Transporter Networks achieve orders of magnitude more sample efficiency than the image-based alternatives on the benchmark. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-036
- Transporter Networks also provide better sample efficiency than multi-layer perceptrons trained with ground-truth object state. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-037
- Transporter Networks reach 100% success on block-insertion from a single demonstration, versus 17.0% for Form2Fit. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-038
- On towers-of-hanoi with 100 demonstrations, Transporter Networks reach 97.3% mean task success, versus 3.7% for Form2Fit. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-039
- On stack-block-pyramid, Transporter Networks reach 78.2% mean success with 1,000 demonstrations, versus 32.5% for Form2Fit. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-040
- On assembling-kits with unseen test objects, Transporter Networks reach 90.4% success with 100 demonstrations, versus 24.2% for Form2Fit. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-041
- On manipulating-rope, Transporter Networks reach 92.1% mean success with 1,000 demonstrations, versus 47.7% for Form2Fit. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-042
- On sweeping-piles, Transporter Networks reach 96.1% mean success with 1,000 demonstrations, versus 74.4% for GT-State MLP. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-043
- On simpler unseen objects with primitive geometries like disks or squares, Form2Fit achieves 96.3% task success. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-044
- The authors suggest Form2Fit descriptors are less capable of matching higher-resolution information than their deep template-matching model. (Zeng et al., 2020) `ev:asserted` p. 7 ^zeng2020transporter-045
- When a stack of blocks falls over, Transporter Networks can re-build it as if they had just started the task. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-046
- The authors hypothesize that equivariance to rotations and translations enables learning these recovery behaviors even with little data. (Zeng et al., 2020) `ev:asserted` p. 7 ^zeng2020transporter-047
- On translation-only block-insertion with stochastic demonstrations, Transporter Networks reach 100% success at every tested number of demonstrations. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-048
- With stochastic demonstrations, Form2Fit drops from 100% success with one demonstration to 30.0% with ten. (Zeng et al., 2020) `ev:measured` p. 7 ^zeng2020transporter-049
- In the simplified block-insertion task, most baselines perform well with deterministic demonstrations but begin to struggle with stochastic ones. (Zeng et al., 2020) `ev:measured` p. 8 ^zeng2020transporter-050
- On 6DoF block-insertion, the SE(3) Transporter Network reaches 91.0% success with 1,000 demonstrations, versus 5.0% for a 3-step GT-State MLP. (Zeng et al., 2020) `ev:measured` p. 8 ^zeng2020transporter-051
- The hybrid discrete-continuous SE(3) model is not able to generalize from one demonstration as the discrete-only SE(2) model could. (Zeng et al., 2020) `ev:measured` p. 8 ^zeng2020transporter-052
- On real UR5e robots, Transporter Networks achieve 98.9% test performance on mouthwash kit assembly, trained on 8141 human-demonstrated transitions. (Zeng et al., 2020) `ev:measured` p. 8 ^zeng2020transporter-053
- On real sweeping of Go-piece piles, Transporter Networks achieve 98.3% test performance, trained on 6759 human-demonstrated transitions. (Zeng et al., 2020) `ev:measured` p. 8 ^zeng2020transporter-054
- Real training data were collected by 13 human operators through a Unity-based remote teleoperation interface during COVID-19 lockdowns. (Zeng et al., 2020) `ev:reported` p. 8 ^zeng2020transporter-055
- The authors list sensitivity to camera-robot calibration as one current limitation of their Transporter Networks. (Zeng et al., 2020) `ev:asserted` p. 8 ^zeng2020transporter-056
- The authors state it remains unclear how to integrate torque or force actions with spatial action spaces. (Zeng et al., 2020) `ev:asserted` p. 8 ^zeng2020transporter-057
- A stated limitation of Ravens is that its rendering may not reflect real noise such as calibration inaccuracies or depth-sensor noise. (Zeng et al., 2020) `ev:asserted` p. 12 ^zeng2020transporter-058
- The authors describe packing-boxes as the hardest benchmark task, requiring tight fitting plus implicit ordering to maximize container coverage. (Zeng et al., 2020) `ev:asserted` p. 14 ^zeng2020transporter-059
- Among the two image-based baselines, Form2Fit performed better than ConvMLP on every task except sweeping-piles. (Zeng et al., 2020) `ev:measured` p. 16 ^zeng2020transporter-060
- The authors believe the gains stem from the model's inductive bias, a prior that manipulation involves rearranging 3D space. (Zeng et al., 2020) `ev:asserted` p. 16 ^zeng2020transporter-061
- For sweeping-piles, constraining the model to two translation-only poses works better than letting it choose a rotation at each pose. (Zeng et al., 2020) `ev:measured` p. 17 ^zeng2020transporter-062
- With n=1,000 training examples, the SE(3) model's roll/pitch regressions have mean absolute errors of 3 to 4 degrees each. (Zeng et al., 2020) `ev:measured` p. 18 ^zeng2020transporter-063
- In-image-plane yaw errors of about 10 degrees most often contributed to unsuccessful SE(3) model deployments in test environments. (Zeng et al., 2020) `ev:measured` p. 18 ^zeng2020transporter-064
- Without the transport operation, learned palletizing or packing policies fail to align boxes tightly enough to exceed 55% completion. (Zeng et al., 2020) `ev:measured` p. 19 ^zeng2020transporter-065
- Real sweeping needs on average 20 ± 2.5 sweeps to complete, compared with 18.1 sweeps for human teleoperation. (Zeng et al., 2020) `ev:measured` p. 21 ^zeng2020transporter-066
- A ResNet50 kit-state classifier trained on 4848 samples reaches 96.9% mean validation accuracy for detecting full, empty, or partial kits. (Zeng et al., 2020) `ev:measured` p. 23 ^zeng2020transporter-067

## 🎯 Contributions

## 📖 Glossary

- **Transporter Network** — Model that infers pick-conditioned placements by cross-correlating deep features of a pick crop.
- **Spatial displacement** — Rigid transform moving a region of space, such as an object, from pick to place.
- **Pick-conditioned placing** — Predicting the place pose given a chosen pick pose rather than independently.
- **Spatially consistent representation** — Orthographic top-down image where object appearance stays constant across views and rigid moves.
- **Translational equivariance** — Translating the input translates the output identically, as fully convolutional networks do.
- **Ravens** — PyBullet benchmark of 10 tabletop manipulation tasks with stochastic scripted oracles.
- **Two-pose motion primitive** — Action parameterized by a start pose and an end pose, e.g. pick-place or push.
- **Form2Fit** — Prior pick-and-place method matching picks to places with dense visual descriptors.
- **Stochastic demonstrations** — Expert demos whose pick and place poses are sampled randomly from all successful ones.

## ❓ Open questions

- How can memory be added so the stateless model handles non-Markovian tasks?
- How can torque or force actions be integrated with spatial action spaces?
- Would multi-task training improve generalization to new tasks?
- Can iterative re-optimization of the SE(2) step reduce the yaw errors that dominate SE(3) failures?
- How far does the rigid-displacement prior hold for deformables and piles with complex dynamics?
- How robust is the approach to camera-robot calibration errors in real deployments?

## 📝 Notes on reading

Read the arXiv v3 (5 Jan 2022) of the CoRL 2020 paper; the PDF abstract says code will be made available, the registry abstract says it is available. Tables 2, 3, 4 and 6 are extracted as flattened number streams; only cells whose row and column could be unambiguously aligned were claimed. Table 1 (task attribute check marks) is lost in extraction. Fig. 9 (interpolation/extrapolation plots), Fig. 10 (prediction heatmaps) and the training convergence plot on p. 20 could only be described. Inconsistencies: p. 5 refers to the rope task as Fig. 1e while the Fig. 1 caption lists rope as (g); the metric section on pp. 14-15 names a task manipulating-cables that is called manipulating-rope elsewhere; p. 22 says Transformer Network for Transporter Network. The claim that Transporter Networks outperform both image-based baselines in all scenarios (p. 16) sits beside Table 3 where Form2Fit ties at 100 on deterministic demos.

## Suggested new concepts

- Transporter Networks — core architecture reused and extended by later goal-conditioned and language-conditioned manipulation work.
- Ravens benchmark — simulated tabletop benchmark used to compare imitation learning sample efficiency.
- Spatial action maps — pixel-wise action-value representations that exploit equivariance for picking and placing.
- Pick-conditioned placing — decomposition of pick-and-place relevant to any lab-object rearrangement pipeline.
- Equivariance in robot learning — inductive bias credited for sample efficiency across many manipulation methods.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — *Pick-and-place* $SE(2)$-equivariante y eficiente en muestras
