---
aliases: []
type: "source"
title: "Visual Servoing from Deep Neural Networks"
citekey: "Bateux2017visual"
doi: "10.48550/arXiv.1705.08940"
arxiv: "1705.08940"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1705.08940"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Quentin Bateux", "Eric Marchand", "Jürgen Leitner", "Francois Chaumette", "Peter Corke"]
sha256: ["9c6288119a284dac806811dbe8bd60274b3bcc87854cf2a99fda0a3d38573f9d"]
pdf: "Content/Papers/Bateux2017visual.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 63
---

📄 PDF: [[Bateux2017visual.pdf]]

> [!abstract] One-sentence summary
> The paper fine-tunes a pre-trained AlexNet on a synthetic, perturbation-augmented dataset built from a single real image to regress relative 6 DOF camera pose, then closes a pose-based visual servoing loop that reaches sub-millimeter precision on a real gantry robot and tolerates lighting changes and occlusions.

## Abstract

We present a deep neural network-based method to perform high-precision, robust and real-time 6 DOF visual servoing. The paper describes how to create a dataset simulating various perturbations (occlusions and lighting conditions) from a single real-world image of the scene. A convolutional neural network is fine-tuned using this dataset to estimate the relative pose between two images of the same scene. The output of the network is then employed in a visual servoing control scheme. The method converges robustly even in difficult real-world settings with strong lighting variations and occlusions.A positioning error of less than one millimeter is obtained in experiments with a 6 DOF robot. (arXiv)

## 🧠 Key ideas (atomic)

- The authors propose a trained deep neural network that estimates the pose of the current image relative to the desired image for [[Visual servoing|visual servoing]]. (Bateux et al., 2017) `ev:asserted` p. 1 ^bateux2017visual-001
- [[Visual servoing|Direct visual servoing]] was introduced to exploit the full image as the visual feature, requiring no extraction of geometric features. (Bateux et al., 2017) `ev:cited` p. 1 ^bateux2017visual-002
- The authors state that the main drawback of [[Visual servoing|direct visual servoing]] is its small convergence domain compared to classical feature-based techniques. (Bateux et al., 2017) `ev:asserted` p. 1 ^bateux2017visual-003
- The authors attribute the small convergence domain of direct visual servoing to high non-linearities between the image information and the 3D motion. (Bateux et al., 2017) `ev:asserted` p. 1 ^bateux2017visual-004
- A deep network architecture pre-trained for object classification is re-purposed by the authors to perform relative camera pose estimation. (Bateux et al., 2017) `ev:asserted` p. 1 ^bateux2017visual-005
- The proposed training process relies on a single image acquired at a reference pose, from which a simulator quickly creates a fine-tuning dataset. (Bateux et al., 2017) `ev:asserted` p. 1 ^bateux2017visual-006
- The network is integrated with a [[Position-based visual servoing|position-based visual servoing]] control scheme that the authors describe as robust to occlusions and lighting variations. (Bateux et al., 2017) `ev:asserted` p. 1 ^bateux2017visual-007
- The sub-mm positioning accuracy listed among the contributions is claimed for a 6 DOF robotic setup on planar scenes. (Bateux et al., 2017) `ev:asserted` p. 1 ^bateux2017visual-008
- The authors note that learned vision-based reaching systems require large datasets with long training times, which hinders their widespread use. (Bateux et al., 2017) `ev:cited` p. 1 ^bateux2017visual-009
- Once training is performed offline, the online computation of the pose estimate takes 50ms on a middle-end graphics card. (Bateux et al., 2017) `ev:reported` p. 2 ^bateux2017visual-010
- The authors state that the online computation cost is constant, independent of the size and complexity of the training dataset. (Bateux et al., 2017) `ev:asserted` p. 2 ^bateux2017visual-011
- The network outputs the relative pose between the current and reference images as a translation vector plus an angle/axis rotation. (Bateux et al., 2017) `ev:reported` p. 2 ^bateux2017visual-012
- To reach a desired image, the CNN estimates both desired and current poses relative to the reference image, from which their relative displacement is computed. (Bateux et al., 2017) `ev:reported` p. 2 ^bateux2017visual-013
- The resulting control scheme is [[Position-based visual servoing|pose-based visual servoing]], which is globally asymptotically stable provided the estimated displacement is stable and correct enough. (Bateux et al., 2017) `ev:cited` p. 2 ^bateux2017visual-014
- The authors argue that their approach moves the stability and convergence issues from the control part to the displacement estimation part. (Bateux et al., 2017) `ev:asserted` p. 2 ^bateux2017visual-015
- At each iteration the camera velocity is computed from the CNN-estimated displacement with a classical control law scaled by a positive gain. (Bateux et al., 2017) `ev:reported` p. 2 ^bateux2017visual-016
- A pre-trained AlexNet, trained on 1.2 million ImageNet images for 1000-class object classification, was chosen as the starting point. (Bateux et al., 2017) `ev:reported` p. 2 ^bateux2017visual-017
- The authors expect the lower AlexNet layers to act as basic image feature extractors, with only the upper layers requiring adaptation. (Bateux et al., 2017) `ev:asserted` p. 2 ^bateux2017visual-018
- The final 1000-output classification layer is replaced by a randomly initialized layer that outputs 6 floats representing the 6 DOF pose. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-019
- The network is trained with a Euclidean loss on translation error plus rotation error weighted by a scale factor β = 0.01. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-020
- The scale factor harmonizes the amplitude of translation in meters with rotation in degrees to facilitate convergence of the learning process. (Bateux et al., 2017) `ev:asserted` p. 3 ^bateux2017visual-021
- Starting from the AlexNet available in Caffe, the network was fine-tuned on a scene-specific dataset of 11000 images with various perturbations. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-022
- Fine-tuning in Caffe used a batch size of 50 images over 50 training epochs on the synthetic scene dataset. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-023
- The authors state that the method can use any CNN trained on images, leaving a thorough comparison of architectures for future work. (Bateux et al., 2017) `ev:asserted` p. 3 ^bateux2017visual-024
- The authors consider the design of the training dataset the most critical step, affecting convergence, precision and robustness of the trained network. (Bateux et al., 2017) `ev:asserted` p. 3 ^bateux2017visual-025
- The nominal dataset is generated from a single real-world image projected on a 3D plane and viewed from simulated virtual cameras. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-026
- The simulation procedure generated the 11k training images in less than half an hour, avoiding time-consuming real-world data gathering. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-027
- For comparison, the authors cite prior grasping work that needed 700 robot hours to gather 50k data points for a single task. (Bateux et al., 2017) `ev:cited` p. 3 ^bateux2017visual-028
- The first 10,000 virtual camera poses were drawn from a Gaussian around the reference pose, with a camera-plane depth of 20cm. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-029
- The Gaussian variances were 1cm for each translation axis, 10° for the x and y rotations, and 20° for z rotation. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-030
- The dataset was appended with 1,000 more elements from a second Gaussian draw whose variances were 1/100 of the first draw. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-031
- The authors state that the finer sampling around the reference pose enables the sub-millimeter precision at the end of the robot motion. (Bateux et al., 2017) `ev:asserted` p. 3 ^bateux2017visual-032
- Two perturbations were modeled in the dataset: lighting changes, both global and local, and occlusions, to obtain a more robust process. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-033
- The scene is assumed to be static under nominal conditions for each experiment, without deformations or temporal changes in structure. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-034
- Global lighting changes are modeled by an affine variation of the pixel intensities of the synthetic images. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-035
- Local lighting changes are modeled by a mixture of 2D Gaussians applied per pixel, each representing a projected directional light source. (Bateux et al., 2017) `ev:reported` p. 3 ^bateux2017visual-036
- Working only with planes in 3D space lets the authors model lights as local 2D sources, avoiding time-consuming rendering algorithms. (Bateux et al., 2017) `ev:asserted` p. 3 ^bateux2017visual-037
- Specularities are not modeled, as material and reflection properties are unknown; the method handles them as a sub-class of occlusions. (Bateux et al., 2017) `ev:asserted` p. 4 ^bateux2017visual-038
- Occlusions are synthesized by pasting a random SLIC superpixel cluster from a random Label-Me image at a random position in each altered image. (Bateux et al., 2017) `ev:reported` p. 4 ^bateux2017visual-039
- Real-world images were preferred over synthetic occlusion images to provide varied occlusions rather than ones generated from geometrical or statistical methods. (Bateux et al., 2017) `ev:asserted` p. 4 ^bateux2017visual-040
- The authors argue that a variety of occlusions in training prevents the network from overfitting and failing on real world occlusions. (Bateux et al., 2017) `ev:asserted` p. 4 ^bateux2017visual-041
- Experiments were performed on an Afma 6 DOF gantry robot in an eye-in-hand configuration, starting from an arbitrary pose each time. (Bateux et al., 2017) `ev:reported` p. 4 ^bateux2017visual-042
- In the nominal experiment the robot had to perform a translation of (1cm, −24cm, −9cm) toward the desired pose. (Bateux et al., 2017) `ev:reported` p. 4 ^bateux2017visual-043
- In the nominal experiment the required rotation was (−10°, −16°, −43°), with a camera to planar scene distance of 80cm. (Bateux et al., 2017) `ev:reported` p. 4 ^bateux2017visual-044
- In nominal conditions the [[Visual servoing|CNN-based visual servoing]] converged on the real robot without any noisy or oscillatory behaviour. (Bateux et al., 2017) `ev:measured` p. 4 ^bateux2017visual-045
- In nominal conditions the position of the system at the end of the motion was less than one millimeter from the desired one. (Bateux et al., 2017) `ev:measured` p. 4 ^bateux2017visual-046
- The nominal experiment made no efforts toward perfect lighting, but added no external lighting variations or occlusions to the scene. (Bateux et al., 2017) `ev:reported` p. 4 ^bateux2017visual-047
- For the perturbation experiment the robot captured a single image at the initial pose and the network was trained again. (Bateux et al., 2017) `ev:reported` p. 4 ^bateux2017visual-048
- During servoing, light from 3 lamps was changed independently, producing global and local lighting changes on the scene. (Bateux et al., 2017) `ev:reported` p. 4 ^bateux2017visual-049
- During the perturbation experiment various objects were added, moved and removed from the scene to create occlusions. (Bateux et al., 2017) `ev:reported` p. 4 ^bateux2017visual-050
- Despite the variety and severity of the applied perturbations, the control scheme did not diverge in the second experiment. (Bateux et al., 2017) `ev:measured` p. 5 ^bateux2017visual-051
- Under perturbations the final precision ranged from 10cm accumulated translation error at the worst perturbation to less than one millimeter back in nominal conditions. (Bateux et al., 2017) `ev:measured` p. 5 ^bateux2017visual-052
- A slower convergence was observed in the perturbation experiment when compared with the nominal conditions experiment on the robot. (Bateux et al., 2017) `ev:measured` p. 5 ^bateux2017visual-053
- Under perturbations most of the positioning error lay in the coupled translation and rotation degrees of freedom tx/ry and ty/rx. (Bateux et al., 2017) `ev:measured` p. 5 ^bateux2017visual-054
- The authors state that this coupled error keeps most of the scene in view by keeping the scene center aligned with the optical axis. (Bateux et al., 2017) `ev:asserted` p. 5 ^bateux2017visual-055
- At iterations 100 and 260 the operator's hand briefly occluded most of the scene, inducing strong spikes in the SSD and velocities. (Bateux et al., 2017) `ev:measured` p. 5 ^bateux2017visual-056
- As soon as the strong occlusion vanished, the method retrieved its converging motion instantaneously according to the authors. (Bateux et al., 2017) `ev:measured` p. 5 ^bateux2017visual-057
- Since no tracking is involved, the authors introduced no elaborate scheme to handle sudden loss of information or re-initialization. (Bateux et al., 2017) `ev:asserted` p. 5 ^bateux2017visual-058
- The perturbations observed on the network outputs were less noisy than the perturbations observed in the sum-of-squared-distances plot. (Bateux et al., 2017) `ev:measured` p. 5 ^bateux2017visual-059
- The authors conclude that the method achieves millimeter accuracy through all 6 degrees of freedom in centimeter- and meter-scale positioning tasks. (Bateux et al., 2017) `ev:asserted` p. 6 ^bateux2017visual-060
- The current framework allows a robot to visual servo with respect to a single scene, which forms the basis of the training set. (Bateux et al., 2017) `ev:asserted` p. 6 ^bateux2017visual-061
- Changing the application scene requires synthesizing a new, comparatively small training dataset and fine-tuning the network again. (Bateux et al., 2017) `ev:asserted` p. 6 ^bateux2017visual-062
- Future research will extend the method to multiple scenes, including 3D ones, toward scene-agnostic relative camera pose estimation. (Bateux et al., 2017) `ev:asserted` p. 6 ^bateux2017visual-063

## 🎯 Contributions

## 📖 Glossary

- **Visual servoing** — control of a robot's motion using feedback from one or more cameras.
- **Direct (photometric) visual servoing** — servoing that uses the whole image intensity as the visual feature.
- **Pose-based visual servoing (PBVS)** — control law driven by an estimated 3D relative pose error.
- **Image-based visual servoing (IBVS)** — control law minimizing feature error directly in image space.
- **Interaction matrix** — matrix linking visual feature time variation to camera velocity.
- **Fine-tuning** — retraining the upper layers of a pre-trained network for a new task.
- **Angle/axis (θu)** — rotation representation as a unit axis scaled by rotation angle.
- **SLIC superpixels** — segmentation into compact clusters of similar neighbouring pixels.
- **Eye-in-hand** — configuration with the camera mounted on the robot end-effector.

## ❓ Open questions

- Does the approach generalize to non-planar 3D scenes, where the single-image plane projection no longer holds?
- How would other CNN architectures than AlexNet compare for relative pose regression in servoing?
- Can one network provide scene-agnostic relative pose estimates without per-scene fine-tuning?
- How large a convergence domain does the method have beyond the tested initial displacement?
- How does unmodeled specular reflection affect precision on non-matte surfaces?

## 📝 Notes on reading

- Version read: arXiv preprint 1705.08940v2 (7 Jun 2017), matching the identifier.
- Figures 5 and 6 (positioning error, SSD, translational/rotational errors, velocities, images) could only be described; the paper gives no per-iteration numbers beyond the text.
- Figure 7 shows sample perturbed images from the real experiments.
- Inconsistency: the conclusion claims millimeter accuracy in meter-scale positioning tasks and robustness to strong perturbations, while the only reported displacement is about 26cm in translation and the perturbation experiment shows up to 10cm accumulated translation error during perturbations.
- Only two real-robot runs on a planar scene are reported, with no quantitative comparison to photometric or feature-based servoing baselines.
- The pose-estimate timing (50ms) is stated in the related-work discussion rather than measured in the experiments section.

## Suggested new concepts

- CNN relative pose regression for servoing — a learned replacement for hand-crafted features in visual control loops.
- Single-image synthetic dataset generation — builds a training set by warping one reference image through virtual cameras.
- Superpixel occlusion augmentation — pasting segmented real-image patches as realistic synthetic occluders.
- Gaussian local-illumination augmentation — mixture of 2D Gaussians to simulate local light sources on planar scenes.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — CNN de pose relativa más PBVS, datos generados automáticamente

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
