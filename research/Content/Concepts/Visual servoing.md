---
aliases: []
type: concept
element_type: method
topic: "[[Camera-robot calibration and visual servoing]]"
topics: ["[[Camera-robot calibration and visual servoing]]"]
created: 2026-09-19
---

## Working definition

Visual servoing controls a robot or camera velocity in closed loop from visual feedback so that the current image, or the pose estimated from it, converges to a desired one.

## Evidence

- [[Bateux2017visual - Visual Servoing from Deep Neural Networks#^bateux2017visual-001]] — The authors propose a trained deep neural network that estimates the pose of the current image relative to the desired image for visual servoing.
- [[Bateux2017visual - Visual Servoing from Deep Neural Networks#^bateux2017visual-002]] — Direct visual servoing was introduced to exploit the full image as the visual feature, requiring no extraction of geometric features.
- [[Bateux2017visual - Visual Servoing from Deep Neural Networks#^bateux2017visual-003]] — The authors state that the main drawback of direct visual servoing is its small convergence domain compared to classical feature-based techniques.
- [[Bateux2017visual - Visual Servoing from Deep Neural Networks#^bateux2017visual-045]] — In nominal conditions the CNN-based visual servoing converged on the real robot without any noisy or oscillatory behaviour.
- [[Harish2020dfvs - DFVS Deep Flow Guided Scene Agnostic Image Based Visual#^harish2020dfvs-002]] — Direct visual servoing skips feature extraction, which helps achieve higher goal-reaching precision at the cost of a smaller convergence basin.
- [[Harish2020dfvs - DFVS Deep Flow Guided Scene Agnostic Image Based Visual#^harish2020dfvs-003]] — Classical visual servoing requires knowledge of the environment depth, which is especially difficult to obtain on robots with a monocular camera.
- [[Harish2020dfvs - DFVS Deep Flow Guided Scene Agnostic Image Based Visual#^harish2020dfvs-008]] — Several deep reinforcement learning visual servoing approaches are specific to manipulation tasks trained only on scenes with objects lying on a table.
- [[Harish2020dfvs - DFVS Deep Flow Guided Scene Agnostic Image Based Visual#^harish2020dfvs-025]] — Photometric visual servoing using true depth from the depth sensor is not able to converge in most of the benchmark environments.
- [[Lu2023markerless - Markerless Camera-to-Robot Pose Estimation via#^lu2023markerless-052]] — In visual servoing, CtRNet achieves 0.002m averaged translational error on the end-effector at a 30Hz loop rate.
- [[Scherl2025vit - ViT-VS On the Applicability of Pretrained Vision#^scherl2025vit-001]] — Classical visual servoing methods show limited robustness to image perturbations and typically require the exact target object instance, according to the authors.
- [[Scherl2025vit - ViT-VS On the Applicability of Pretrained Vision#^scherl2025vit-002]] — Learning-based visual servoing methods require task-specific training, extensive data generation or predefined object models, which the authors say hinders real-world deployment.
- [[Chen2023cns - CNS Correspondence Encoded Neural Image Servo Policy#^chen2023cns-003]] — Implicit end-to-end servo methods reach precision comparable to IBVS in training scenes but generalize poorly to novel scenes.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: top-down (5 sources) · topic: Camera-robot calibration and visual servoing (drafter's packet `q5-calibration-servoing`, confirmed at the gate)
