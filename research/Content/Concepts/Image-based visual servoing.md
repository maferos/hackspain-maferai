---
aliases: ["IBVS", "image based visual servoing"]
type: concept
element_type: method
topic: "[[Camera-robot calibration and visual servoing]]"
topics: ["[[Camera-robot calibration and visual servoing]]"]
created: 2026-09-19
---

## Working definition

Image-based visual servoing computes the camera velocity directly from the error between current and desired image features through the pseudoinverse of an interaction matrix, without reconstructing the relative pose.

## Evidence

- [[Harish2020dfvs - DFVS Deep Flow Guided Scene Agnostic Image Based Visual#^harish2020dfvs-001]] — The authors note that image based visual servoing is robust to calibration errors but could lead the robot into a local minimum.
- [[Harish2020dfvs - DFVS Deep Flow Guided Scene Agnostic Image Based Visual#^harish2020dfvs-013]] — The predicted flow features are integrated with depth estimates from a second neural network through the interaction matrix of image based servoing.
- [[Chen2023cns - CNS Correspondence Encoded Neural Image Servo Policy#^chen2023cns-001]] — Classical IBVS methods achieve high servo precision but suffer from a small convergence basin and erroneous correspondence, according to cited prior work.
- [[Chen2023cns - CNS Correspondence Encoded Neural Image Servo Policy#^chen2023cns-007]] — The neural policy is supervised by PBVS, which the authors state intrinsically has a larger convergence basin than IBVS.
- [[Chen2023cns - CNS Correspondence Encoded Neural Image Servo Policy#^chen2023cns-039]] — In Erender the IBVS controller failed more often on scenes with a large initial rotation error between initial and desired poses.
- [[Chen2023cns - CNS Correspondence Encoded Neural Image Servo Policy#^chen2023cns-048]] — In Scene-Easy without RANSAC, the IBVS success ratio fell to 8.33 percent while CNS still reached 75.00 percent.
- [[Scherl2025vit - ViT-VS On the Applicability of Pretrained Vision#^scherl2025vit-004]] — ViT-VS is a visual servoing framework that combines image-based visual servoing with DINOv2 features, requiring no task-specific training or fine-tuning.
- [[Scherl2025vit - ViT-VS On the Applicability of Pretrained Vision#^scherl2025vit-018]] — The controller follows classical IBVS, computing camera velocity from the pseudoinverse of an interaction matrix approximated with depth-image values.
- [[Scherl2025vit - ViT-VS On the Applicability of Pretrained Vision#^scherl2025vit-031]] — The classical baseline ORB IBVS converged in 98.6 percent of unperturbed runs and 58.4 percent of perturbed runs.
- [[Scherl2025vit - ViT-VS On the Applicability of Pretrained Vision#^scherl2025vit-032]] — Under perturbation, ViT-VS achieved a relative convergence rate improvement of 31.2% over the best classical IBVS method.
- [[Scherl2025vit - ViT-VS On the Applicability of Pretrained Vision#^scherl2025vit-035]] — ViT-VS end errors are higher than those of classical IBVS methods, which the authors attribute to coarse ViT feature maps.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: extra (3 sources) · topic: Camera-robot calibration and visual servoing (drafter's packet `q5-calibration-servoing`, confirmed at the gate)
