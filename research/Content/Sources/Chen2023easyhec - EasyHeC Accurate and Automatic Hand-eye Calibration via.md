---
aliases: []
type: "source"
title: "EasyHeC: Accurate and Automatic Hand-eye Calibration via Differentiable Rendering and Space Exploration"
citekey: "Chen2023easyhec"
doi: "10.48550/arXiv.2305.01191"
arxiv: "2305.01191"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2305.01191"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Linghao Chen", "Yuzhe Qin", "Xiaowei Zhou", "Hao Su"]
sha256: ["3ee6fbc4e634efd82861a4594dad6fd49f418e396cffa3418422c71fb5f60202"]
pdf: "Content/Papers/Chen2023easyhec.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Chen2023easyhec.pdf]]

> [!abstract] One-sentence summary
> EasyHeC calibrates an eye-to-hand camera without markers by fitting rendered robot-arm masks to segmented images and choosing informative joint poses in simulation, beating marker-based and learning-based baselines on synthetic and real data.

## Abstract

Hand-eye calibration is a critical task in robotics, as it directly affects the efficacy of critical operations such as manipulation and grasping. Traditional methods for achieving this objective necessitate the careful design of joint poses and the use of specialized calibration markers, while most recent learning-based approaches using solely pose regression are limited in their abilities to diagnose inaccuracies. In this work, we introduce a new approach to hand-eye calibration called EasyHeC, which is markerless, white-box, and delivers superior accuracy and robustness. We propose to use two key technologies: differentiable rendering-based camera pose optimization and consistency-based joint space exploration, which enables accurate end-to-end optimization of the calibration process and eliminates the need for the laborious manual design of robot joint poses. Our evaluation demonstrates superior performance in synthetic and real-world datasets, enhancing downstream manipulation tasks by providing precise camera poses for locating and interacting with objects. The code is available at the project page: https://ootts.github.io/easyhec. (arXiv)

## 🧠 Key ideas (atomic)

- [[Hand-eye calibration (AX = XB)|Traditional hand-eye calibration methods]] rely on markers such as ArUco tags or checkerboard patterns to link robot and camera frames. (Chen et al., 2023) `ev:cited` p. 1 ^chen2023easyhec-001
- The authors argue that varying camera placements for distinct tasks require different joint pose trajectories, a task highly demanding for humans. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023easyhec-002
- According to the authors, the performance of [[Markerless hand-eye calibration|learning-based markerless calibration approaches]] largely depends on the scale and quality of their training data. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023easyhec-003
- Most learning-based calibration methods lack transparency due to their reliance on direct regression, making calibration errors challenging to diagnose. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023easyhec-004
- The authors state that traditional and learning-based methods both show uneven hand positioning error distribution across robot configurations in camera space. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023easyhec-005
- EasyHeC is presented as a [[Markerless hand-eye calibration|markerless, white-box hand-eye calibration system]] that eliminates the laborious manual design of robot joint poses. (Chen et al., 2023) `ev:asserted` p. 1 ^chen2023easyhec-006
- EasyHeC replaces the [[Hand-eye calibration (AX = XB)|transformation-equivalence objective AX = XB]] with a loss function grounded in per-pixel segmentation of the robot arm. (Chen et al., 2023) `ev:asserted` p. 2 ^chen2023easyhec-007
- The method assumes the 3D model of the robot arm is available, which the authors consider reasonable for most commonly used arms. (Chen et al., 2023) `ev:asserted` p. 2 ^chen2023easyhec-008
- The camera-to-base transformation is optimized by minimizing the discrepancy between the projected 3D arm model and the observed segmentation mask. (Chen et al., 2023) `ev:reported` p. 2 ^chen2023easyhec-009
- The authors argue that the arm mask offers substantially more evidence for estimating the transformation than traditional marker points do. (Chen et al., 2023) `ev:asserted` p. 2 ^chen2023easyhec-010
- A consistency-based joint space exploration module selects informative robot joint poses by evaluating consistency with a set of camera pose candidates. (Chen et al., 2023) `ev:reported` p. 2 ^chen2023easyhec-011
- Since joint space exploration is performed in simulation, the authors state it is free of cost and can be performed many times. (Chen et al., 2023) `ev:asserted` p. 2 ^chen2023easyhec-012
- On synthetic datasets, EasyHeC is reported to outperform a traditional-based baseline by 4 times in accuracy with a single view. (Chen et al., 2023) `ev:measured` p. 2 ^chen2023easyhec-013
- [[Markerless hand-eye calibration|Marker-free Structure-from-Motion calibration methods]] are described as unsuitable for tracking robot motion in the eye-to-hand setting. (Chen et al., 2023) `ev:cited` p. 2 ^chen2023easyhec-014
- DREAM predicts robot joint keypoints with a deep neural network and then recovers camera poses using the Perspective-n-point algorithm. (Chen et al., 2023) `ev:cited` p. 2 ^chen2023easyhec-015
- The authors state that a prior differentiable-rendering method optimizing camera pose and robot shape from one image introduces ambiguity into optimization. (Chen et al., 2023) `ev:asserted` p. 2 ^chen2023easyhec-016
- Unlike that prior differentiable-rendering method, EasyHeC assumes the robot shape is known and focuses solely on the camera pose as the variable. (Chen et al., 2023) `ev:asserted` p. 2 ^chen2023easyhec-017
- EasyHeC targets the eye-to-hand problem, estimating the SE(3) transformation between camera and robot base given known camera intrinsic parameters. (Chen et al., 2023) `ev:reported` p. 3 ^chen2023easyhec-018
- In each iteration, the observed robot arm mask is predicted from the image of the arm using the PointRend segmentation network. (Chen et al., 2023) `ev:reported` p. 3 ^chen2023easyhec-019
- In later iterations, the camera pose is optimized with the masks at all the observed joint poses, not a single one. (Chen et al., 2023) `ev:reported` p. 3 ^chen2023easyhec-020
- Masks are rendered for each individual robot link and combined, with a min function limiting their sum to a maximum of 1. (Chen et al., 2023) `ev:reported` p. 3 ^chen2023easyhec-021
- The camera transformation is optimized in Lie algebra space by gradient descent using PyTorch Autograd on the differentiable mask loss. (Chen et al., 2023) `ev:reported` p. 3 ^chen2023easyhec-022
- The PointRend mask network is trained on synthetic data generated by the SAPIEN simulator, then fine-tuned on real data. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023easyhec-023
- The camera pose is initialized with PVNet, which estimates predefined 2D keypoints through pixel-wise voting before solving the transformation with PnP. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023easyhec-024
- Exploration moves the robot to the sampled joint pose whose rendered masks show the highest variance over the camera pose candidates. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023easyhec-025
- The implementation employs nvdiffrast as the differentiable mask renderer inside the camera pose optimization of the calibration loop. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023easyhec-026
- Camera pose optimization uses the Adam optimizer with a learning rate of 3e-3 and runs for 1000 steps. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023easyhec-027
- For space exploration, 50 camera pose candidates are randomly chosen from the optimization range between step 200 and 1000. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023easyhec-028
- Exploration randomly samples 2000 joint poses, filtering out poses with self-intersection, links beyond a distance threshold, or environment collisions. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023easyhec-029
- In real-world scenarios without known calibration error, the authors propose the change in variance between exploration iterations as a stopping proxy. (Chen et al., 2023) `ev:asserted` p. 4 ^chen2023easyhec-030
- The synthetic evaluation uses SAPIEN to synthesize 100 photo-realistic scenes with different camera poses of an xArm robot arm. (Chen et al., 2023) `ev:reported` p. 4 ^chen2023easyhec-031
- The marker-based baseline used 20 manually designed joint poses per scene with a 4cm×5cm chessboard marker attached to the arm. (Chen et al., 2023) `ev:reported` p. 5 ^chen2023easyhec-032
- For the synthetic experiments, 10,000 rendered images were used to train PointRend and another 10,000 images to train PVNet. (Chen et al., 2023) `ev:reported` p. 5 ^chen2023easyhec-033
- Only 1.9% of randomly sampled joint poses gave clear marker visibility, which the authors judged impractical for the marker-based baseline. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023easyhec-034
- On the xArm synthetic dataset, the text reports average marker-based rotation and translation errors of 0.9 degrees and 2.1 cm. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023easyhec-035
- With only 1 view, EasyHeC reaches an error of 0.32 degrees and 0.5 cm on the xArm synthetic dataset. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023easyhec-036
- With 5 views, the error of EasyHeC on the xArm synthetic dataset decreases to 0.08 degrees and 0.2 cm. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023easyhec-037
- EasyHeC errors on the xArm synthetic dataset consistently decrease as the number of views increases from 1 to 5. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023easyhec-038
- DREAM's rotation error on the xArm synthetic dataset falls from 1.924 degrees with one view to 0.704 with five views. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023easyhec-039
- With five views, EasyHeC's translation error is 0.206 cm with space exploration, compared with 0.312 cm using random sampling. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023easyhec-040
- With five views on synthetic data, DREAM's translation error of 0.303 cm is higher than EasyHeC's 0.206 cm with exploration. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023easyhec-041
- The authors attribute DREAM's low accuracy to non-discriminative keypoints and keypoint detection that is not resilient to occlusion or truncation. (Chen et al., 2023) `ev:asserted` p. 5 ^chen2023easyhec-042
- The real-world Baxter dataset used contains 100 images of a real Baxter robot, with a single camera pose and 20 joint poses. (Chen et al., 2023) `ev:reported` p. 5 ^chen2023easyhec-043
- On the Baxter dataset, the camera pose was initialized manually for simplicity in light of its single camera pose. (Chen et al., 2023) `ev:reported` p. 5 ^chen2023easyhec-044
- On Baxter, EasyHeC with three views reaches a 2D PCK of 0.55 at 20 pixels, versus 0.34 for OK. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023easyhec-045
- With one view, EasyHeC scores a 2D PCK of 0.90 at 50 pixels on Baxter, versus 0.69 for OK. (Chen et al., 2023) `ev:measured` p. 5 ^chen2023easyhec-046
- At the 5cm threshold, EasyHeC's 3D PCK on Baxter is 0.65 with one view and 0.80 with two views. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023easyhec-047
- At the 5cm threshold, DREAM and OK reach 3D PCK scores of 0.08 and 0.34 on the Baxter dataset. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023easyhec-048
- Following prior conventions, the Baxter PCK tables report results on training images, while the ablation figure uses the entire dataset. (Chen et al., 2023) `ev:reported` p. 6 ^chen2023easyhec-049
- In real-world targeting, EasyHeC with PointRend segmentation reaches an error of 0.4 cm, compared with 1.5 cm for DREAM. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023easyhec-050
- Using the Segment-Anything model with manually annotated bounding box prompts lowered the real-world targeting error of EasyHeC to 0.3 cm. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023easyhec-051
- The authors note that the manual distance measurement is not highly reliable, offering a preliminary indication of the system accuracy. (Chen et al., 2023) `ev:asserted` p. 6 ^chen2023easyhec-052
- The authors state that SAM requires human intervention for mask labeling, whereas PointRend offers a fully automated calibration after pre-training. (Chen et al., 2023) `ev:asserted` p. 6 ^chen2023easyhec-053
- On the xArm synthetic dataset, space exploration consistently gave faster convergence and smaller errors than random selection of the next joint pose. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023easyhec-054
- On the Baxter dataset, space exploration produced higher PCK than random joint pose selection, especially for the 2D PCK metric. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023easyhec-055
- On the xArm synthetic dataset, errors decreased as the number of sampled joint poses increased, particularly when below 1000 poses. (Chen et al., 2023) `ev:measured` p. 6 ^chen2023easyhec-056
- Beyond 1000 sampled joint poses the errors became virtually unchanged, and the authors set the number to 2000 elsewhere. (Chen et al., 2023) `ev:measured` p. 7 ^chen2023easyhec-057
- Varying the number of sampled camera pose candidates left translation errors roughly the same on the xArm synthetic dataset. (Chen et al., 2023) `ev:measured` p. 7 ^chen2023easyhec-058
- On an RTX 4090 GPU, the overall EasyHeC runtime is 250-370s with 1000 optimization steps and 5 exploration iterations. (Chen et al., 2023) `ev:measured` p. 7 ^chen2023easyhec-059
- Space exploration accounts for 150-200s of runtime, compared with 40-50s for DR-based optimization and 60-120s for robot movement. (Chen et al., 2023) `ev:measured` p. 7 ^chen2023easyhec-060
- The authors consider this runtime acceptable compared with marker-based calibrations, which they say can take several hours to finetune. (Chen et al., 2023) `ev:asserted` p. 7 ^chen2023easyhec-061
- In applications, EasyHeC calibration transformed PVNet object poses from camera to robot base coordinates as input states for CoTPC. (Chen et al., 2023) `ev:reported` p. 7 ^chen2023easyhec-062
- Screenshots from stacking cube and peg insertion experiments show accurately aligned cubes and a successfully inserted peg using EasyHeC calibration. (Chen et al., 2023) `ev:measured` p. 7 ^chen2023easyhec-063
- The method necessitates a precise robot model, which may limit its applicability to robots enveloped in protective shells. (Chen et al., 2023) `ev:asserted` p. 8 ^chen2023easyhec-064
- The method exclusively caters to eye-to-hand calibration, although the authors state the same pipeline can be leveraged for eye-in-hand configurations. (Chen et al., 2023) `ev:asserted` p. 8 ^chen2023easyhec-065
- PointRend needs to be retrained for a new robot arm, though the authors describe this as a one-time training per arm type. (Chen et al., 2023) `ev:asserted` p. 8 ^chen2023easyhec-066
- The authors conclude that the joint space exploration strategy reduces the number of samples needed for achieving accurate calibration results. (Chen et al., 2023) `ev:asserted` p. 8 ^chen2023easyhec-067

## 🎯 Contributions

## 📖 Glossary

- **Hand-eye calibration** — Estimating the rigid transformation between a camera and a robot frame.
- **Eye-to-hand** — Setting where the camera is fixed in the world, observing the robot.
- **Eye-in-hand** — Setting where the camera is mounted on the robot end-effector.
- **Differentiable rendering** — Rendering whose output has gradients with respect to scene parameters such as camera pose.
- **Render-and-compare** — Pose estimation by rendering a model and minimizing its difference to the observed image.
- **PCK** — Percentage of 2D or 3D keypoints within a threshold distance of ground truth.
- **Joint space exploration** — Selecting informative robot joint poses to constrain the camera pose estimate.
- **PnP** — Perspective-n-Point: recovering camera pose from 2D-3D point correspondences.

## ❓ Open questions

- How well does the mask-based objective work for robots whose visible shells differ from the available CAD model?
- Does the eye-in-hand variant, suggested but not evaluated, reach similar accuracy with manual or predefined initialization?
- How robust is the calibration to segmentation errors in cluttered scenes, beyond the PointRend and SAM comparison?
- Is the variance-change stopping criterion reliable in practice when ground-truth error is unavailable?
- Can the real-world targeting accuracy be confirmed with a measurement more reliable than manual pointer distances?

## 📝 Notes on reading

Read the arXiv v2 (7 Nov 2023) preprint. The text and tables disagree slightly on the xArm synthetic marker-based baseline: the text gives 0.9 degrees and 2.1 cm, while Table I lists 0.870 and Table II lists 2.000. The text's single-view and five-view figures (0.32 degrees / 0.5 cm; 0.08 degrees / 0.2 cm) are rounded from the Ours (SE) rows (0.322 / 0.488; 0.081 / 0.206). The "4 times" single-view accuracy gain on p. 2 matches translation (2.000 vs 0.488) but not rotation (0.870 vs 0.322, about 2.7x). On synthetic data, DREAM's translation error with one or two views is close to or below Ours (Rand), so EasyHeC's translation advantage depends on space exploration. In Table IV, Ours (3views) scores 0.90 at 10cm, below Ours (2views) at 0.95. The text says the marker-based method uses 20 views, yet Tables I and II list it only under the 1-view column. Figures 5 and 6 (ablation curves) could only be described; their plotted values were not claimed. Equations 1–5 were extracted with broken layout but are readable. Section cross-references in Fig. 2 (Sec IV-C/IV-D) disagree with the method sections (III-C/III-D).

## Suggested new concepts

- Markerless hand-eye calibration — a recurring alternative to fiducial-based calibration relevant to lab robot setups.
- Differentiable rendering for pose estimation — a general technique shared by calibration, object pose and robot state estimation.
- Active view / next-best-pose selection for calibration — links uncertainty-driven exploration across calibration papers.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Calibración sin marcadores con renderizado diferenciable en $SE(3)$

<!-- ingest-checker dropped 3 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
