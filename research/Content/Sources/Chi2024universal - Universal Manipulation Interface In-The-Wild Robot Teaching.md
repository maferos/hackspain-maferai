---
aliases: []
type: "source"
title: "Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots"
citekey: "Chi2024universal"
doi: "10.48550/arXiv.2402.10329"
arxiv: "2402.10329"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2402.10329"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Cheng Chi", "Zhenjia Xu", "Chuer Pan", "Eric Cousineau", "Benjamin Burchfiel", "Siyuan Feng", "Russ Tedrake", "Shuran Song"]
sha256: ["a9452cbaf9f5d2a77d5f8b631632fa7f45ae4bbc32400be1cc939b91a36e1609"]
pdf: "Content/Papers/Chi2024universal.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Chi2024universal.pdf]]

> [!abstract] One-sentence summary
> UMI pairs a GoPro-equipped hand-held gripper with a latency-matched, relative-trajectory Diffusion Policy interface, so that in-the-wild human demonstrations train robot policies for dynamic, bimanual and long-horizon tasks that transfer zero-shot across robots and environments.

## Abstract

We present Universal Manipulation Interface (UMI) -- a data collection and policy learning framework that allows direct skill transfer from in-the-wild human demonstrations to deployable robot policies. UMI employs hand-held grippers coupled with careful interface design to enable portable, low-cost, and information-rich data collection for challenging bimanual and dynamic manipulation demonstrations. To facilitate deployable policy learning, UMI incorporates a carefully designed policy interface with inference-time latency matching and a relative-trajectory action representation. The resulting learned policies are hardware-agnostic and deployable across multiple robot platforms. Equipped with these features, UMI framework unlocks new robot manipulation capabilities, allowing zero-shot generalizable dynamic, bimanual, precise, and long-horizon behaviors, by only changing the training data for each task. We demonstrate UMI's versatility and efficacy with comprehensive real-world experiments, where policies learned via UMI zero-shot generalize to novel environments and objects when trained on diverse human demonstrations. UMI's hardware and software system is open-sourced at https://umi-gripper.github.io. (arXiv)

## 🧠 Key ideas (atomic)

- UMI is a hand-held data collection and policy learning framework that transfers in-the-wild human demonstrations directly to deployable robot policies. (Chi et al., 2024) `ev:asserted` p. 3 ^chi2024universal-001
- The authors argue that teleoperation for robot data collection requires high setup costs for hardware as well as expert operators. (Chi et al., 2024) `ev:asserted` p. 1 ^chi2024universal-002
- The authors argue that unstructured in-the-wild human videos exhibit a large embodiment gap to robots, making them insufficient for robot learning. (Chi et al., 2024) `ev:asserted` p. 1 ^chi2024universal-003
- Earlier hand-held gripper systems achieved visual diversity, but their collected actions were constrained to simple grasping or quasi-static pick-and-place. (Chi et al., 2024) `ev:cited` p. 1 ^chi2024universal-004
- Hand-held devices relying on monocular structure-from-motion often struggle to recover precise global action due to scale ambiguity, motion blur or insufficient texture. (Chi et al., 2024) `ev:asserted` p. 2 ^chi2024universal-005
- The authors argue that policies unaware of latency discrepancies between collection and inference encounter out-of-distribution inputs, generating out-of-sync actions. (Chi et al., 2024) `ev:asserted` p. 2 ^chi2024universal-006
- The authors state that prior works often use simple policy representations such as MLPs, limiting their capacity to capture [[Multimodal action distributions|multimodal human action distributions]]. (Chi et al., 2024) `ev:asserted` p. 2 ^chi2024universal-007
- UMI's data collection hardware is a trigger-activated, hand-held 3D printed parallel jaw gripper with soft fingers, mounted with a GoPro camera. (Chi et al., 2024) `ev:reported` p. 4 ^chi2024universal-008
- The authors state that wrist-mounted camera videos are almost indistinguishable between human demonstrations and robot deployment, minimizing the observation embodiment gap. (Chi et al., 2024) `ev:asserted` p. 4 ^chi2024universal-009
- Because the camera is mechanically fixed relative to the fingers, mounting UMI on robots does not require [[Robot-world and hand-eye calibration (AX = YB)|camera-robot-world calibration]]. (Chi et al., 2024) `ev:asserted` p. 4 ^chi2024universal-010
- The authors observed that training with a moving wrist camera leads the policy to focus on task-relevant objects instead of background structures. (Chi et al., 2024) `ev:asserted` p. 4 ^chi2024universal-011
- UMI attaches a 155-degree Fisheye lens to the wrist-mounted GoPro camera to provide visual context for a wide range of tasks. (Chi et al., 2024) `ev:reported` p. 4 ^chi2024universal-012
- The policy receives raw Fisheye images without undistortion, since Fisheye effects preserve resolution in the center while compressing peripheral information. (Chi et al., 2024) `ev:asserted` p. 4 ^chi2024universal-013
- A pair of physical mirrors placed in the camera's peripheral view creates implicit stereo views within the same image to mitigate missing depth perception. (Chi et al., 2024) `ev:reported` p. 4 ^chi2024universal-014
- UMI records the GoPro's built-in IMU data, from accelerometer and gyroscope, into standard mp4 video files to capture rapid movements with absolute scale. (Chi et al., 2024) `ev:reported` p. 4 ^chi2024universal-015
- UMI's inertial-monocular SLAM, based on ORB-SLAM3, maintains tracking for a short period even when visual tracking fails from motion blur. (Chi et al., 2024) `ev:asserted` p. 4 ^chi2024universal-016
- In contrast to binary open-close gripper actions, finger width on the UMI gripper is continuously tracked via fiducial markers. (Chi et al., 2024) `ev:reported` p. 5 ^chi2024universal-017
- The authors found that commanding gripper width continuously significantly expands the range of tasks doable by parallel-jaw grippers. (Chi et al., 2024) `ev:asserted` p. 5 ^chi2024universal-018
- When robot base location and kinematics are known, SLAM-recovered absolute end-effector poses allow kinematics and dynamics feasibility filtering of demonstration data. (Chi et al., 2024) `ev:reported` p. 5 ^chi2024universal-019
- The assembled UMI gripper weighs 780g with a finger stroke of 80mm, according to the hardware summary in the paper. (Chi et al., 2024) `ev:reported` p. 5 ^chi2024universal-020
- The 3D printed gripper has a bill-of-materials cost of $73, while the GoPro camera with its accessories totals $298. (Chi et al., 2024) `ev:reported` p. 5 ^chi2024universal-021
- The visuomotor policy takes synchronized RGB images, 6-DoF end-effector pose with gripper width, producing sequences of end-effector pose with gripper width. (Chi et al., 2024) `ev:reported` p. 5 ^chi2024universal-022
- All experiments in the paper use [[Diffusion Policy]] as the policy learning framework, with ACT suggested as a potential drop-in replacement. (Chi et al., 2024) `ev:reported` p. 5 ^chi2024universal-023
- At inference, all observation streams are aligned to the highest-latency stream, usually the camera, by interpolating proprioception at image capture timestamps. (Chi et al., 2024) `ev:reported` p. 6 ^chi2024universal-024
- Commands are sent ahead of time to compensate for execution latency, which varies across different robot arm and gripper hardware. (Chi et al., 2024) `ev:reported` p. 6 ^chi2024universal-025
- UMI discards the first predicted actions made outdated by observation, inference and execution latency, executing only actions timestamped after tact. (Chi et al., 2024) `ev:reported` p. 6 ^chi2024universal-026
- The action representation is a relative trajectory of SE(3) transforms giving each desired pose relative to the initial end-effector pose. (Chi et al., 2024) `ev:reported` p. 6 ^chi2024universal-027
- The authors found the relative trajectory action representation more robust against tracking errors during data collection and against camera displacements. (Chi et al., 2024) `ev:asserted` p. 6 ^chi2024universal-028
- Inter-gripper relative pose comes from a map-then-localize scheme in which all demonstrations of a scene are relocalized to one shared map. (Chi et al., 2024) `ev:reported` p. 6 ^chi2024universal-029
- The cup arrangement training dataset contains 305 episodes collected by 2 demonstrators, with evaluation on 20 test cases. (Chi et al., 2024) `ev:reported` p. 7 ^chi2024universal-030
- UMI completed the narrow-domain cup arrangement task in 20/20 evaluation episodes with randomized robot and object initial states. (Chi et al., 2024) `ev:measured` p. 7 ^chi2024universal-031
- Deploying the same cup arrangement policy checkpoint on a Franka Emika FR2 robot achieved an 18/20 = 90% success rate. (Chi et al., 2024) `ev:measured` p. 7 ^chi2024universal-032
- The two Franka failures were joint limit violations, which the authors say a different robot mounting location could have avoided. (Chi et al., 2024) `ev:asserted` p. 7 ^chi2024universal-033
- Rectifying and cropping images to a 69° field of view reduced cup arrangement success to 11/20 = 55%. (Chi et al., 2024) `ev:measured` p. 7 ^chi2024universal-034
- The delta action baseline achieved a 16/20 = 80% success rate on the narrow-domain cup arrangement task. (Chi et al., 2024) `ev:measured` p. 8 ^chi2024universal-035
- The absolute action baseline achieved only 5/20 = 25% success, likely due to inaccurate calibration between SLAM and robot base frames. (Chi et al., 2024) `ev:measured` p. 8 ^chi2024universal-036
- Directly providing raw mirror images decreased cup arrangement success from 18/20 = 90% without mirrors to 17/20 = 85%. (Chi et al., 2024) `ev:measured` p. 8 ^chi2024universal-037
- Digitally reflecting the mirror content and swapping left with right mirror images achieved a 20/20 = 100% cup arrangement success rate. (Chi et al., 2024) `ev:measured` p. 8 ^chi2024universal-038
- The authors hypothesize that opposite motions in main and mirrored images might confuse vision encoders, especially those with translational equivariance. (Chi et al., 2024) `ev:asserted` p. 8 ^chi2024universal-039
- The dynamic tossing task sorts 6 YCB objects by tossing them into bins placed beyond the robot's kinematic reach range. (Chi et al., 2024) `ev:reported` p. 8 ^chi2024universal-040
- Trained on 280 demonstrations, the tossing policy with latency matching achieved 105/120 = 87.5% success, counted per object tossed. (Chi et al., 2024) `ev:measured` p. 8 ^chi2024universal-041
- Disabling inference-time latency matching reduced dynamic tossing success to 69/120 = 57.5%, with visibly more jittery robot motion. (Chi et al., 2024) `ev:measured` p. 9 ^chi2024universal-042
- For bimanual cloth folding, 250 demonstrations from two demonstrators trained one centralized policy generating actions for both arms. (Chi et al., 2024) `ev:reported` p. 9 ^chi2024universal-043
- The bimanual cloth folding policy with relative inter-gripper proprioception achieved a 14/20 = 70% success rate. (Chi et al., 2024) `ev:measured` p. 9 ^chi2024universal-044
- Removing inter-gripper proprioception reduced cloth folding success to 6/20 = 30%, often through asynchronous grasps when lifting the bottom hem. (Chi et al., 2024) `ev:measured` p. 9 ^chi2024universal-045
- A single demonstrator collected 258 dish washing demonstrations, including explicit recovery behavior when additional ketchup is added. (Chi et al., 2024) `ev:reported` p. 9 ^chi2024universal-046
- Fine-tuning a CLIP pretrained ViT-B/16 vision encoder, the seven-step dish washing policy achieved a 14/20 = 70% success rate. (Chi et al., 2024) `ev:measured` p. 9 ^chi2024universal-047
- A ResNet-34 trained from scratch learned non-reactive dish washing behavior, ignoring plate position, with 0/10 = 0% success. (Chi et al., 2024) `ev:measured` p. 10 ^chi2024universal-048
- Within 12 person-hours, 3 demonstrators collected 1400 cup arrangement demonstrations across 30 diverse physical locations. (Chi et al., 2024) `ev:reported` p. 10 ^chi2024universal-049
- The in-the-wild policy used a CLIP pretrained ViT-L/14 vision encoder, increased from ViT-B/16 to ensure model capacity. (Chi et al., 2024) `ev:reported` p. 10 ^chi2024universal-050
- In two unseen environments, a cafe table and a water fountain, the policy succeeded on 28/40 = 70% of trials with training cups. (Chi et al., 2024) `ev:measured` p. 10 ^chi2024universal-051
- The in-the-wild policy achieved 15/20 = 75% success on unseen testing cups, for a combined success of 43/60 = 71.7%. (Chi et al., 2024) `ev:measured` p. 10 ^chi2024universal-052
- A policy trained only on narrow-domain lab data with the same pretrained ViT achieved 0% success in the unseen environments. (Chi et al., 2024) `ev:measured` p. 10 ^chi2024universal-053
- The authors conclude that finetuning a large pretrained model with narrow-domain data is insufficient for producing an in-the-wild deployable policy. (Chi et al., 2024) `ev:asserted` p. 10 ^chi2024universal-054
- On cup arrangement, the UMI gripper collected demonstrations more than 3× faster than spacemouse teleoperation, at 48% of human-hand speed. (Chi et al., 2024) `ev:measured` p. 11 ^chi2024universal-055
- On dynamic tossing, UMI reached 64% of human-hand speed, while teleoperation failed to produce any successful demonstration in 15 minutes. (Chi et al., 2024) `ev:measured` p. 11 ^chi2024universal-056
- On a MoCap benchmark of 7 single-gripper and 7 bimanual tasks, mean per-gripper SLAM position error was 6.1mm. (Chi et al., 2024) `ev:measured` p. 11 ^chi2024universal-057
- The mean per-gripper SLAM absolute trajectory error in rotation was 3.5° on the MoCap ground-truth benchmark dataset. (Chi et al., 2024) `ev:measured` p. 11 ^chi2024universal-058
- The mean relative pose error between the two grippers was 10.1mm in position with 0.8° in rotation. (Chi et al., 2024) `ev:measured` p. 11 ^chi2024universal-059
- Because deployment robot kinematic limits are unknown at collection time, UMI relies on data filtering to ensure kinematic feasibility of policies. (Chi et al., 2024) `ev:asserted` p. 11 ^chi2024universal-060
- The SLAM-based action recovery inherits the requirement of visual SLAM for sufficient texture in the environment. (Chi et al., 2024) `ev:asserted` p. 11 ^chi2024universal-061
- Collecting data with UMI grippers remains less efficient than human hand demonstration, partly due to the weight and bulkiness of the gripper. (Chi et al., 2024) `ev:asserted` p. 11 ^chi2024universal-062
- The authors modified ORB-SLAM3 to continue normal SLAM operation after relocalizing to a loaded map, using that map only as initialization. (Chi et al., 2024) `ev:reported` p. 17 ^chi2024universal-063
- Optional fiducial markers with known sizes disambiguate feature matches during mapping, which the authors found significantly increases in-the-wild mapping robustness. (Chi et al., 2024) `ev:asserted` p. 17 ^chi2024universal-064
- Quasi-static tasks run at 10Hz for observation and action, while the dynamic tossing task uses 20Hz for highly reactive behavior. (Chi et al., 2024) `ev:reported` p. 17 ^chi2024universal-065
- For quasi-static tasks, the authors observed smoother behavior at 0.5x execution speed, which may arise from imperfect latency compensation. (Chi et al., 2024) `ev:asserted` p. 17 ^chi2024universal-066
- Soft fingers printed with 95A TPU provide passive mechanical compliance when deployed on robots lacking force-torque control, such as the UR5. (Chi et al., 2024) `ev:reported` p. 17 ^chi2024universal-067

## 🎯 Contributions

## 📖 Glossary

- **UMI** — Universal Manipulation Interface: hand-held gripper plus policy interface for robot teaching.
- **Embodiment gap** — Mismatch in observation or action space between the demonstrator and the robot.
- **Inference-time latency matching** — Aligning observation streams and advancing commands to cancel sensor and execution delays.
- **Relative trajectory action** — Action sequence of poses expressed relative to the current end-effector pose.
- **Delta action** — Action step expressed relative to the immediately previous action; accumulates error.
- **Implicit stereo** — Depth cues from mirror views acting as extra virtual cameras in one image.
- **Inter-gripper proprioception** — Relative pose between two grippers, provided to a bimanual policy.
- **Diffusion Policy** — Visuomotor policy generating action sequences by denoising diffusion; models multimodal actions.
- **ATE / RPE** — Absolute trajectory error and relative pose error, standard SLAM accuracy metrics.
- **Kinematic-based data filtering** — Discarding demonstrations infeasible for a given robot's reach and joint limits.

## ❓ Open questions

- Can an embodiment-aware policy learning framework transfer skills from demonstrations that are valid but infeasible for the target robot hardware?
- How can action be recovered in texture-deficient environments where visual SLAM fails, for example with third-person cameras and markers?
- Would better latency matching remove the need to slow quasi-static policies to 0.5x execution speed?
- How does performance scale with the number of in-the-wild demonstrations, demonstrators and locations beyond the 1400-demo cup study?
- Can lighter or more dexterous hand-held interfaces close the throughput gap with bare-hand demonstration?
- How subjective are the manually judged success and termination criteria, and how would automatic metrics change the reported rates?

## 📝 Notes on reading

- Version read: arXiv 2402.10329v3 (6 Mar 2024), consistent with the packet identifier.
- Fig. 8(c) and Fig. 11 are extracted as scattered numbers; the per-object tossing rates, per-substep folding and dish washing rates, and the throughput bar values (111, 231, 35, 149, 237, 0 CPH) could not be reliably assigned to bars and were not claimed.
- The bimanual camera soft-synchronization bound (1/60 s) is split across lines in the extraction and was not claimed as a number.
- Inconsistencies: the introduction reports a 70% out-of-distribution success rate, while Sec. VI gives 43/60 = 71.7% and Fig. 9 shows 0.72; Sec. VI says 15 espresso cups were used in demonstrations, while Fig. A2 says 18 of 20 purchased cups were used for training.
- The dish washing ResNet-34 baseline is reported as 0/10 on p. 10, while the Fig. 8 caption states success over 20 evaluation episodes.
- Reference numbering for CLIP differs between p. 9 ([29]) and p. 10 ([30]); [30] in the bibliography is a learning-from-demonstration review, so p. 10 appears to be a citation error.
- Typos in the source: teleportation for teleoperation (p. 11), OBR-SLAM3 for ORB-SLAM3 (p. 17).
- Success and termination criteria are judged manually by an operator, and the authors acknowledge subjective elements (p. 16).
- Table A1 (p. 16) lists per-task Diffusion Policy hyperparameters; all tasks use DDIM with 50 training and 16 inference diffusion steps.

## Suggested new concepts

- Hand-held demonstration grippers — a recurring data-collection interface family (UMI, Dobb-E, grasping-in-the-wild) that trades embodiment gap against portability.
- Inference-time latency matching — a deployable-policy technique relevant to any real-robot system with heterogeneous sensor and actuator delays.
- Relative trajectory action representation — an action-space choice compared against absolute and delta actions with measured effects.
- Diffusion Policy — the policy backbone used across UMI tasks and much subsequent imitation learning work.
- Visual-inertial SLAM for demonstration capture — the action-recovery mechanism that sets UMI's tracking accuracy and texture limits.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Acciones relativas en el grupo: invariancia al marco

<!-- ingest-checker dropped 3 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
