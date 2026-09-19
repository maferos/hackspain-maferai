---
aliases: []
type: "source"
title: "FoundationPose: Unified 6D Pose Estimation and Tracking of Novel Objects"
citekey: "Wen2023foundationpose"
doi: "10.48550/arXiv.2312.08344"
arxiv: "2312.08344"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2312.08344"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Bowen Wen", "Wei Yang", "Jan Kautz", "Stan Birchfield"]
sha256: ["2f02b05d5c6ac8ca0b0828bce7d6ffeabfa1fea5f61934a5716acdb348fecebc"]
pdf: "Content/Papers/Wen2023foundationpose.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Wen2023foundationpose.pdf]]

> [!abstract] One-sentence summary
> FoundationPose is a single RGBD render-and-compare model, trained only on LLM-augmented synthetic data, that estimates and tracks the 6D pose of unseen objects from either a CAD model or about 16 reference images, and beats task-specific methods on LINEMOD, YCB-Video, BOP and YCBInEOAT.

## Abstract

We present FoundationPose, a unified foundation model for 6D object pose estimation and tracking, supporting both model-based and model-free setups. Our approach can be instantly applied at test-time to a novel object without fine-tuning, as long as its CAD model is given, or a small number of reference images are captured. We bridge the gap between these two setups with a neural implicit representation that allows for effective novel view synthesis, keeping the downstream pose estimation modules invariant under the same unified framework. Strong generalizability is achieved via large-scale synthetic training, aided by a large language model (LLM), a novel transformer-based architecture, and contrastive learning formulation. Extensive evaluation on multiple public datasets involving challenging scenarios and objects indicate our unified approach outperforms existing methods specialized for each task by a large margin. In addition, it even achieves comparable results to instance-level methods despite the reduced assumptions. Project page: https://nvlabs.github.io/FoundationPose/ (arXiv)

## 🧠 Key ideas (atomic)

- FoundationPose is a unified framework performing [[Novel-object 6D pose estimation|6D pose estimation and tracking of novel objects]] in both model-based and model-free setups using RGBD images. (Wen et al., 2023) `ev:asserted` p. 1 ^wen2023foundationpose-001
- In the model-based setup considered by the paper, a textured 3D CAD model of the novel object is provided at test time. (Wen et al., 2023) `ev:asserted` p. 1 ^wen2023foundationpose-002
- In the model-free setup considered by the paper, a set of reference images of the object is provided instead. (Wen et al., 2023) `ev:asserted` p. 1 ^wen2023foundationpose-003
- Classic instance-level pose estimation methods only work on the specific object instance determined at training time. (Wen et al., 2023) `ev:cited` p. 1 ^wen2023foundationpose-004
- A neural implicit representation allows novel view synthesis from a small number (∼16) of reference images, bridging the model-based and model-free setups. (Wen et al., 2023) `ev:asserted` p. 2 ^wen2023foundationpose-005
- The authors argue that reliance on correspondences, as in OnePose and FS6D, becomes fragile for textureless objects or under severe occlusion. (Wen et al., 2023) `ev:asserted` p. 2 ^wen2023foundationpose-006
- Synthetic training data uses 3D assets drawn from recent large-scale 3D model databases, namely Objaverse and GSO. (Wen et al., 2023) `ev:reported` p. 2 ^wen2023foundationpose-007
- From Objaverse the authors chose the Objaverse-LVIS subset, which contains more than 40K objects belonging to 1156 LVIS categories. (Wen et al., 2023) `ev:reported` p. 2 ^wen2023foundationpose-008
- The authors note that FS6D random texture pasting yields seam artifacts on the textured mesh due to random UV mapping. (Wen et al., 2023) `ev:asserted` p. 3 ^wen2023foundationpose-009
- LLM-aided texture augmentation gives a text prompt, the object shape and a randomly initialized noisy texture to TexFusion to produce an augmented model. (Wen et al., 2023) `ev:reported` p. 3 ^wen2023foundationpose-010
- A two-level hierarchical prompt strategy asks ChatGPT to describe an object's possible appearance using a template filled with its Objaverse-LVIS tag. (Wen et al., 2023) `ev:reported` p. 3 ^wen2023foundationpose-011
- The ChatGPT answer becomes the text prompt provided to the diffusion model, enabling full automation of texture augmentation at scale. (Wen et al., 2023) `ev:reported` p. 4 ^wen2023foundationpose-012
- Synthetic data generation is implemented in NVIDIA Isaac Sim, leveraging path tracing for high-fidelity photo-realistic rendering of training scenes. (Wen et al., 2023) `ev:reported` p. 4 ^wen2023foundationpose-013
- Gravity and physics simulation produce physically plausible scenes containing both original and texture-augmented versions of sampled objects. (Wen et al., 2023) `ev:reported` p. 4 ^wen2023foundationpose-014
- The object is represented by a geometry function outputting a signed distance plus an appearance function outputting color. (Wen et al., 2023) `ev:reported` p. 4 ^wen2023foundationpose-015
- Compared with NeRF, the SDF representation provides higher quality depth rendering according to the authors of this paper. (Wen et al., 2023) `ev:asserted` p. 4 ^wen2023foundationpose-016
- Neural object field learning, optimized per object without priors, can be efficiently performed within seconds according to the authors. (Wen et al., 2023) `ev:asserted` p. 4 ^wen2023foundationpose-017
- For RGBD rendering, a textured mesh is extracted once per object from the SDF zero level set with marching cubes. (Wen et al., 2023) `ev:reported` p. 4 ^wen2023foundationpose-018
- Pose translation is initialized from the 3D point located at the median depth within the detected 2D bounding box. (Wen et al., 2023) `ev:reported` p. 5 ^wen2023foundationpose-019
- Rotations are initialized from viewpoints uniformly sampled on an icosphere around the object, each augmented with discretized in-plane rotations. (Wen et al., 2023) `ev:reported` p. 5 ^wen2023foundationpose-020
- Unlike MegaPose, [[Render-and-compare pose refinement|the refiner renders a single view]] at the coarse pose, which the authors observed suffices for refinement. (Wen et al., 2023) `ev:asserted` p. 5 ^wen2023foundationpose-021
- Pose-conditioned cropping centers the observation crop on the projected object origin, sized by the projected slightly enlarged object diameter. (Wen et al., 2023) `ev:reported` p. 5 ^wen2023foundationpose-022
- The [[Render-and-compare pose refinement|refinement network]] predicts translation and rotation updates separately, each processed by its own transformer encoder before linear projection. (Wen et al., 2023) `ev:reported` p. 5 ^wen2023foundationpose-023
- The disentangled update removes the dependency on the updated orientation when applying the translation update, unlike a homogeneous pose update. (Wen et al., 2023) `ev:asserted` p. 5 ^wen2023foundationpose-024
- The pose with the highest score from a hierarchical pose ranking network is selected as the final pose estimate. (Wen et al., 2023) `ev:reported` p. 5 ^wen2023foundationpose-025
- The authors argue that scoring each hypothesis independently forces an absolute score assignment that can be difficult to learn. (Wen et al., 2023) `ev:asserted` p. 5 ^wen2023foundationpose-026
- The second comparison level applies multi-head self-attention across all hypothesis embeddings without position encoding, to stay agnostic to permutation. (Wen et al., 2023) `ev:reported` p. 6 ^wen2023foundationpose-027
- The pose ranking network is trained with a pose-conditioned triplet loss whose anchor is not shared between positive and negative samples. (Wen et al., 2023) `ev:reported` p. 6 ^wen2023foundationpose-028
- Only pose pairs whose positive sample lies within a rotation threshold of the ground truth are kept for the ranking loss. (Wen et al., 2023) `ev:reported` p. 6 ^wen2023foundationpose-029
- The authors attribute the worse performance of InfoNCE to the perfect translation assumption of prior work, which does not hold here. (Wen et al., 2023) `ev:asserted` p. 6 ^wen2023foundationpose-030
- Evaluation covers 5 datasets: LINEMOD, Occluded-LINEMOD, YCB-Video, T-LESS and YCBInEOAT, spanning dense clutter to robotic manipulation scenarios. (Wen et al., 2023) `ev:reported` p. 6 ^wen2023foundationpose-031
- Except for ablations, the same trained model and configuration is used for inference in all evaluations without any fine-tuning. (Wen et al., 2023) `ev:reported` p. 6 ^wen2023foundationpose-032
- In the model-free setup, reference images are selected from the dataset training split together with their ground-truth object pose annotations. (Wen et al., 2023) `ev:reported` p. 6 ^wen2023foundationpose-033
- On YCB-Video model-free pose estimation with 16 reference images, the method reaches a mean ADD AUC of 91.5. (Wen et al., 2023) `ev:measured` p. 6 ^wen2023foundationpose-034
- On the same YCB-Video model-free benchmark, the fine-tuned FS6D-DPM baseline reaches a mean ADD AUC of 42.1. (Wen et al., 2023) `ev:cited` p. 6 ^wen2023foundationpose-035
- Mean ADD-S AUC on YCB-Video model-free estimation is 97.4 for the method versus 88.4 for FS6D-DPM. (Wen et al., 2023) `ev:measured` p. 6 ^wen2023foundationpose-036
- On LINEMOD model-free estimation, the method reaches an average ADD-0.1d recall of 99.9 using 16 reference images without fine-tuning. (Wen et al., 2023) `ev:measured` p. 7 ^wen2023foundationpose-037
- FS6D combined with ICP refinement, which requires fine-tuning on the target dataset, reaches 91.5 average ADD-0.1d on LINEMOD. (Wen et al., 2023) `ev:cited` p. 7 ^wen2023foundationpose-038
- OnePose++ reaches 76.9 average ADD-0.1d on LINEMOD despite being given 200 RGB reference images per object. (Wen et al., 2023) `ev:cited` p. 7 ^wen2023foundationpose-039
- On the BOP datasets LM-O, T-LESS and YCB-V, the method reaches a mean AR of 83.3 in the model-based setup. (Wen et al., 2023) `ev:measured` p. 7 ^wen2023foundationpose-040
- MegaPose-RGBD, a model-based novel-object baseline, reaches a mean AR of 58.6 on the same three BOP datasets. (Wen et al., 2023) `ev:cited` p. 7 ^wen2023foundationpose-041
- The instance-level method SurfEmb with ICP reaches a mean AR of 79.7, below the 83.3 of FoundationPose. (Wen et al., 2023) `ev:measured` p. 7 ^wen2023foundationpose-042
- No re-initialization is applied after tracking is lost, unless otherwise specified, in order to evaluate long-term tracking robustness. (Wen et al., 2023) `ev:reported` p. 7 ^wen2023foundationpose-043
- On YCBInEOAT model-based tracking with ground-truth initialization, the method reaches an overall ADD AUC of 93.09. (Wen et al., 2023) `ev:measured` p. 7 ^wen2023foundationpose-044
- The instance-trained se(3)-TrackNet reaches an overall ADD AUC of 92.66 on YCBInEOAT with ground-truth pose initialization. (Wen et al., 2023) `ev:cited` p. 7 ^wen2023foundationpose-045
- Using its own pose estimation for initialization instead of ground truth, the method reaches 93.22 overall ADD AUC on YCBInEOAT. (Wen et al., 2023) `ev:measured` p. 7 ^wen2023foundationpose-046
- The authors state their unified framework is the only compared method allowing end-to-end pose estimation and tracking without external initialization. (Wen et al., 2023) `ev:asserted` p. 7 ^wen2023foundationpose-047
- On [[YCB-Video dataset|YCB-Video]] model-based pose tracking, the method reaches an all-frames ADD AUC of 96.0 without re-initialization. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-048
- In the model-free YCB-Video tracking setup with reference images, the method reaches an all-frames ADD AUC of 93.7. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-049
- Removing LLM texture augmentation lowered ADD AUC on YCB-Video model-free estimation from 91.52 to 90.83 in the ablation. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-050
- Replacing the transformer with convolutional and linear layers of similar parameter count lowered ADD AUC from 91.52 to 90.77. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-051
- Removing the two-level hierarchical comparison lowered ADD AUC on YCB-Video from 91.52 to 89.05 in the ablation study. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-052
- Replacing the pair-wise ranking loss with InfoNCE lowered ADD AUC on YCB-Video from 91.52 to 89.39 in the ablation. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-053
- Performance measured by [[ADD and ADD-S metrics|ADD and ADD-S AUC]] on YCB-Video saturates at 12 reference images for both metrics. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-054
- Even with only 4 reference images, the method yields stronger performance than FS6D equipped with 16 reference images. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-055
- The gain from increasing [[Synthetic training data for 6D pose estimation|the amount of synthetic training data]] saturates around 1M, measured by AUC on YCB-Video. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-056
- Pose estimation takes about 1.3 s for one object on an Intel i9-10980XE CPU with an NVIDIA RTX 3090 GPU. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-057
- Within pose estimation, pose initialization takes 4 ms, refinement takes 0.88 s and pose selection takes 0.42 s. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-058
- Tracking runs much faster at ∼32 Hz, since only pose refinement is needed without multiple pose hypotheses. (Wen et al., 2023) `ev:measured` p. 8 ^wen2023foundationpose-059
- The authors propose running pose estimation once for initialization, then switching to tracking mode for real-time performance. (Wen et al., 2023) `ev:asserted` p. 8 ^wen2023foundationpose-060
- At the time of submission, FoundationPose was #1 on [[BOP benchmark|the BOP leaderboard]] for [[Novel-object 6D pose estimation|6D localization of unseen objects]]. (Wen et al., 2023) `ev:measured` p. 13 ^wen2023foundationpose-061
- The whole training process over synthetic data takes about a week on 4 NVIDIA V100 GPUs. (Wen et al., 2023) `ev:reported` p. 13 ^wen2023foundationpose-062
- Each synthetic scene drops 70 to 90 randomly sampled objects, scaled from 5 to 30 cm, onto a platform with invisible walls. (Wen et al., 2023) `ev:reported` p. 14 ^wen2023foundationpose-063
- In total, [[Synthetic training data for 6D pose estimation|the synthetic training dataset for pose estimation]] contains about 600K scenes and 1.2M rendered images. (Wen et al., 2023) `ev:reported` p. 14 ^wen2023foundationpose-064
- At test time, [[Render-and-compare pose refinement|pose refinement]] runs 5 iterations for pose estimation but a single iteration for tracking. (Wen et al., 2023) `ev:reported` p. 14 ^wen2023foundationpose-065
- The approach relies on external 2D detection obtained from methods such as CNOS or Mask R-CNN for each object. (Wen et al., 2023) `ev:asserted` p. 15 ^wen2023foundationpose-066
- The authors observe that false or missing 2D detections frequently bottleneck the 6D pose estimation of their method. (Wen et al., 2023) `ev:asserted` p. 15 ^wen2023foundationpose-067
- Under combined texture-less appearance, severe occlusion and limited edge cues, the method fails to estimate the correct orientation. (Wen et al., 2023) `ev:measured` p. 15 ^wen2023foundationpose-068
- The authors name an end-to-end framework for novel object detection, 6D pose estimation and tracking as future work. (Wen et al., 2023) `ev:asserted` p. 15 ^wen2023foundationpose-069

## 🎯 Contributions

## 📖 Glossary

- **Model-based setup** — Novel-object pose setting where a textured CAD model is given at test time.
- **Model-free setup** — Novel-object pose setting where only a few posed reference images are given.
- **Render-and-compare** — Refining or scoring a pose by rendering the object and comparing with the observation.
- **Neural object field** — Per-object neural SDF plus appearance network used to render novel RGBD views.
- **Pose-conditioned cropping** — Cropping the observation around the projected hypothesis pose rather than a fixed detection box.
- **ADD / ADD-S** — Average point distance metrics for pose error; ADD-S handles symmetric objects.
- **AUC** — Area under the accuracy-threshold curve of ADD or ADD-S.
- **ADD-0.1d** — Recall of poses whose ADD error is below 10% of object diameter.
- **AR (BOP)** — Average recall of VSD, MSSD and MSPD metrics from the BOP challenge.
- **Hierarchical comparison** — Two-level scoring: render-vs-observation per hypothesis, then self-attention across hypotheses.

## ❓ Open questions

- How much of the reported gain survives when 2D detection is imperfect, given detection failures frequently bottleneck the method?
- Can the unified framework be extended end-to-end to include novel object detection?
- How does the method extend to articulated, deformable or multiple interacting objects (state estimation beyond a single rigid object)?
- How robust is the model-free setup when reference poses come from SLAM rather than ground-truth annotation?
- Does the ∼32 Hz tracking rate hold on lower-power GPUs typical of mobile robots?
- What is the separate contribution of Isaac Sim path-traced realism versus LLM texture diversity to sim-to-real transfer?

## 📝 Notes on reading

- Version read: arXiv v2 (26 Mar 2024), including the supplementary material (pp. 13-15). The registry abstract (arXiv) differs slightly in wording from the abstract printed in v2 (e.g. the sentence on the neural implicit representation).
- Many baseline numbers in Tables 1 and 2 are adopted from prior papers ([19, 22]); they were marked `ev:cited`.
- Table 1 caption mentions a Finetuned column while the header reads Finetune-free; FS6D-DPM is marked as not finetune-free.
- Table 5 has a garbled cell (se(3)-TrackNet ADD-S for 037_scissors printed as 97s); per-object cells were not claimed.
- Figures 6 (effect of number of reference images) and 7 (effect of training data size) are plots only described in text; values were read from the text, not the curves.
- Figure 8 (BOP leaderboard screenshot) caption states a 0.03 ARCore margin over the unpublished method PoMZ; not claimed separately.
- Figure 11 illustrates the failure mode qualitatively; the failure claim rests on its caption.

## Suggested new concepts

- Render-and-compare pose refinement — shared mechanism with MegaPose, DeepIM and se(3)-TrackNet worth a comparative note.
- Neural object field for pose estimation — SDF-based per-object rendering that turns model-free into model-based pose estimation.
- LLM-aided texture augmentation — synthetic data diversity technique (LLM prompts plus texture diffusion) reusable beyond pose estimation.
- Model-free vs model-based novel object pose estimation — a recurring taxonomy across FS6D, OnePose, MegaPose and this paper.
- BOP benchmark — the standard evaluation suite (AR of VSD, MSSD, MSPD) referenced by many pose papers.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Estimador y seguidor recomendado para el tubo (§8)
