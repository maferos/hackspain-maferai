---
aliases: []
type: "source"
title: "SAM-6D: Segment Anything Model Meets Zero-Shot 6D Object Pose Estimation"
citekey: "Lin2023sam"
doi: "10.48550/arXiv.2311.15707"
arxiv: "2311.15707"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2311.15707"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Jiehong Lin", "Lihua Liu", "Dekun Lu", "Kui Jia"]
sha256: ["ec47a5892933d60754b29c4f7baa2d0eb7c5f4524fd50ac0aa47c5b8b7c89290"]
pdf: "Content/Papers/Lin2023sam.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[Lin2023sam.pdf]]

> [!abstract] One-sentence summary
> SAM-6D pairs SAM-based instance segmentation, scored on semantics, appearance and geometry, with a two-stage background-token point matcher to estimate 6D poses of unseen objects from RGB-D images without render-based refinement.

## Abstract

Zero-shot 6D object pose estimation involves the detection of novel objects with their 6D poses in cluttered scenes, presenting significant challenges for model generalizability. Fortunately, the recent Segment Anything Model (SAM) has showcased remarkable zero-shot transfer performance, which provides a promising solution to tackle this task. Motivated by this, we introduce SAM-6D, a novel framework designed to realize the task through two steps, including instance segmentation and pose estimation. Given the target objects, SAM-6D employs two dedicated sub-networks, namely Instance Segmentation Model (ISM) and Pose Estimation Model (PEM), to perform these steps on cluttered RGB-D images. ISM takes SAM as an advanced starting point to generate all possible object proposals and selectively preserves valid ones through meticulously crafted object matching scores in terms of semantics, appearance and geometry. By treating pose estimation as a partial-to-partial point matching problem, PEM performs a two-stage point matching process featuring a novel design of background tokens to construct dense 3D-3D correspondence, ultimately yielding the pose estimates. Without bells and whistles, SAM-6D outperforms the existing methods on the seven core datasets of the BOP Benchmark for both instance segmentation and pose estimation of novel objects. (arXiv)

## 🧠 Key ideas (atomic)

- SAM-6D addresses [[Novel-object 6D pose estimation|zero-shot 6D object pose estimation]], detecting all instances of novel objects unseen during training together with their 6D poses in RGB-D images. (Lin et al., 2023) `ev:asserted` p. 4 ^lin2023sam-001
- The framework splits the task into two sub-networks: an Instance Segmentation Model that segments all instances, then a Pose Estimation Model predicting each pose. (Lin et al., 2023) `ev:asserted` p. 4 ^lin2023sam-002
- ISM prompts SAM with evenly sampled 2D grid points to generate all possible class-agnostic object proposals from the RGB image. (Lin et al., 2023) `ev:reported` p. 4 ^lin2023sam-003
- ISM uses publicly available SAM or FastSAM with a DINOv2 ViT without any network re-training or fine-tuning. (Lin et al., 2023) `ev:reported` p. 7 ^lin2023sam-004
- ISM runs SAM automatic segmentation with 32 points per side, a predicted-IoU threshold of 0.88 and a stability-score threshold of 0.85. (Lin et al., 2023) `ev:reported` p. 13 ^lin2023sam-005
- Each proposal receives an object matching score combining semantic, appearance and geometric terms, unlike methods that score object semantics alone. (Lin et al., 2023) `ev:asserted` p. 2 ^lin2023sam-006
- Object templates rendered at sampled poses are encoded with a pre-trained DINOv2 ViT backbone to obtain class and patch embeddings. (Lin et al., 2023) `ev:reported` p. 4 ^lin2023sam-007
- The semantic score averages the top K cosine similarities between the class embedding of the proposal crop and those of the templates. (Lin et al., 2023) `ev:reported` p. 4 ^lin2023sam-008
- The template yielding the highest semantic value is taken as the best-matched template for computing the appearance and geometric scores. (Lin et al., 2023) `ev:reported` p. 4 ^lin2023sam-009
- The appearance score averages patch-level cosine similarities between the proposal crop and the best-matched template, aiming to distinguish semantically similar objects that differ in appearance. (Lin et al., 2023) `ev:reported` p. 4 ^lin2023sam-010
- The geometric score is the IoU between the proposal bounding box and the projected box of the object transformed by a coarse pose. (Lin et al., 2023) `ev:reported` p. 4 ^lin2023sam-011
- Because occlusions easily affect the geometric score's reliability, a visible ratio weights it in the final object matching score. (Lin et al., 2023) `ev:reported` p. 4 ^lin2023sam-012
- The visible ratio is the fraction of best-matched template patches whose maximum cosine similarity to proposal patches reaches a threshold of 0.5. (Lin et al., 2023) `ev:reported` p. 12 ^lin2023sam-013
- The 42 ISM templates are fully visible crops from BOP PBR training images at viewpoints defined by a Blender icosphere. (Lin et al., 2023) `ev:reported` p. 12 ^lin2023sam-014
- PEM formulates pose estimation as partial-to-partial point matching, since occlusions, segmentation inaccuracies and sensor noise leave the two point sets only partially overlapping. (Lin et al., 2023) `ev:asserted` p. 5 ^lin2023sam-015
- Learnable background tokens appended to both point feature sets absorb non-overlapped points, so correspondence can be built from feature similarities. (Lin et al., 2023) `ev:asserted` p. 5 ^lin2023sam-016
- A point whose maximum assignment score falls on the background token is treated as having no valid correspondence in the other set. (Lin et al., 2023) `ev:reported` p. 5 ^lin2023sam-017
- Matched point pairs, weighted by their soft assignment scores, are used to compute the object pose with a weighted SVD. (Lin et al., 2023) `ev:reported` p. 5 ^lin2023sam-018
- PEM's Feature Extraction feeds masked crops resized to 224 × 224 into ViT-Base, concatenating patch features from four of its attention blocks. (Lin et al., 2023) `ev:reported` p. 13 ^lin2023sam-019
- Coarse Point Matching passes 196 sampled points per set through stacked Geometric Transformers combining geometric self-attention with inter-set cross-attention. (Lin et al., 2023) `ev:reported` p. 16 ^lin2023sam-020
- Coarse matching samples 6,000 triplets of point pairs, keeps the 300 hypotheses with smallest pair distances, then selects the highest pose matching score. (Lin et al., 2023) `ev:reported` p. 16 ^lin2023sam-021
- Fine Point Matching uses 2048 points per set, injecting the coarse pose through positional encodings learned by a multi-scale Set Abstract Level. (Lin et al., 2023) `ev:reported` p. 6 ^lin2023sam-022
- The authors state that Linear Transformers are more efficient but model point interactions less effectively, since they attend along the feature dimension. (Lin et al., 2023) `ev:asserted` p. 6 ^lin2023sam-023
- The Sparse-to-Dense Point Transformer applies a Geometric Transformer to sampled sparse features, then spreads the information to dense features via Linear Cross-attention. (Lin et al., 2023) `ev:reported` p. 6 ^lin2023sam-024
- PEM is trained on large-scale synthetic ShapeNet-Objects and Google-Scanned-Objects images provided by MegaPose, spanning roughly fifty thousand objects. (Lin et al., 2023) `ev:reported` p. 6 ^lin2023sam-025
- PEM is trained with ADAM for 600,000 iterations, an initial learning rate of 0.0001 with cosine annealing, and batch size 28. (Lin et al., 2023) `ev:reported` p. 6 ^lin2023sam-026
- InfoNCE loss supervises the attention matrices of both matching stages, applied to every transformer block of the coarse and fine modules. (Lin et al., 2023) `ev:reported` p. 17 ^lin2023sam-027
- Training uses two rendered templates per object, whereas evaluation follows CNOS in using 42 templates for both ISM and PEM. (Lin et al., 2023) `ev:reported` p. 6 ^lin2023sam-028
- SAM-6D is evaluated on [[BOP benchmark|the seven core BOP datasets]]: LM-O, T-LESS, TUD-L, IC-BIN, ITODD, HB and YCB-V. (Lin et al., 2023) `ev:reported` p. 6 ^lin2023sam-029
- Instance segmentation is evaluated by mean Average Precision over IoU thresholds from 0.50 to 0.95 in steps of 0.05. (Lin et al., 2023) `ev:reported` p. 6 ^lin2023sam-030
- Pose estimation is evaluated by mean Average Recall over the VSD, MSSD and MSPD error functions of [[BOP benchmark|the BOP benchmark]]. (Lin et al., 2023) `ev:reported` p. 6 ^lin2023sam-031
- With SAM and all three score terms, ISM reaches a mean segmentation mAP of 48.1 across the seven BOP datasets. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-032
- With FastSAM and all three score terms, ISM reaches a mean segmentation mAP of 44.9 on the seven BOP datasets. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-033
- The compared CNOS baseline reaches mean segmentation mAPs of 40.4 with SAM and 41.2 with FastSAM on the seven datasets. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-034
- The semantic-only SAM baseline, matching CNOS except for SAM hyperparameters that generate more proposals, reaches a mean segmentation mAP of 44.0. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-035
- Adding the appearance score to the semantic-only SAM baseline raises mean segmentation mAP from 44.0 to 45.0. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-036
- Adding the geometric score to the semantic-only SAM baseline raises mean segmentation mAP from 44.0 to 46.7. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-037
- On 2D detection, SAM-6D with FastSAM reaches a mean mAP of 47.1, above CNOS with FastSAM at 42.8. (Lin et al., 2023) `ev:measured` p. 14 ^lin2023sam-038
- With ISM masks from SAM, SAM-6D reaches a mean pose AR of 70.4 on the seven BOP core datasets. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-039
- With ISM masks from FastSAM, SAM-6D reaches a mean pose AR of 66.2 on the seven BOP core datasets. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-040
- Using the same CNOS FastSAM masks, SAM-6D reaches a mean AR of 65.3, above 62.8 for refined RGB-D MegaPose. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-041
- With CNOS FastSAM masks, refined RGB-D ZeroPose reaches a mean AR of 57.0, below the 65.3 of SAM-6D. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-042
- With supervised MaskRCNN masks, SAM-6D reaches a mean AR of 66.9, above refined RGB-D MegaPose at 57.2 and refined ZeroPose at 58.4. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-043
- With ZeroPose's zero-shot masks, SAM-6D reaches a mean AR of 62.2, above the 51.2 of refined ZeroPose. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-044
- With MaskRCNN masks on ITODD, SAM-6D reaches an AR of 31.9, below refined ZeroPose at 43.6 and refined RGB-D MegaPose at 40.4. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-045
- The PEM outperforms existing methods under various mask predictions without using the [[Render-and-compare pose refinement|time-intensive render-based refiner]] of MegaPose. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-046
- ISM masks raise PEM mean AR from 65.3 with CNOS FastSAM masks to 70.4 with SAM-based ISM masks. (Lin et al., 2023) `ev:measured` p. 7 ^lin2023sam-047
- On YCB-V, PEM with background tokens reaches an AR of 84.5 at 1.36 s per image, versus 81.4 at 4.31 s with optimal transport. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023sam-048
- Coarse Point Matching alone reaches an AR of 77.6 on YCB-V, which rises to 84.5 when Fine Point Matching is added. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023sam-049
- Removing Coarse Point Matching lowers YCB-V AR to 40.2, with proposal point sets used untransformed for learning positional encodings. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023sam-050
- The authors suggest this degradation may be attributed to the large distance between proposal and object point sets without initial poses. (Lin et al., 2023) `ev:asserted` p. 8 ^lin2023sam-051
- In fine matching on YCB-V, Sparse-to-Dense Point Transformers reach an AR of 84.5, versus 81.7 for Geometric Transformers on 196 points. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023sam-052
- Linear Transformers on 2048 dense points reach an AR of 78.4 in the fine matching module on YCB-V. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023sam-053
- The authors attribute the gaps to the high computational cost of Geometric Transformers on dense sets and ineffective feature-dimension attention in Linear Transformers. (Lin et al., 2023) `ev:asserted` p. 8 ^lin2023sam-054
- On a GeForce RTX 3090, SAM-6D takes 1.43 s per image with FastSAM and 4.37 s with SAM, averaged over the seven datasets. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023sam-055
- The SAM-based variant spends 1.57 s on pose estimation versus 0.98 s for FastSAM, which the authors attribute to more proposals from SAM. (Lin et al., 2023) `ev:measured` p. 8 ^lin2023sam-056
- The SAM-based ISM needs 2.80 s per image for instance segmentation, versus 2.35 s for CNOS with SAM on an RTX 3090. (Lin et al., 2023) `ev:measured` p. 14 ^lin2023sam-057
- Pose estimation AR on YCB-V rises from 21.8 with one template view to 84.5 with 42 template views. (Lin et al., 2023) `ev:measured` p. 18 ^lin2023sam-058
- The authors state that a single template view performs poorly because it cannot fully depict the entire object. (Lin et al., 2023) `ev:asserted` p. 17 ^lin2023sam-059
- With 8 and 16 template views, pose AR on YCB-V reaches 83.9 and 84.1, close to the 84.5 obtained with 42 views. (Lin et al., 2023) `ev:measured` p. 18 ^lin2023sam-060
- On LM-O with OVE6D's own masks, SAM-6D reaches an ADD(-S) of 74.7, above OVE6D at 56.1 and OVE6D with ICP at 72.8. (Lin et al., 2023) `ev:measured` p. 18 ^lin2023sam-061
- CNOS generates mask proposals via SAM and filters out proposals with low feature similarities against templates rendered from the object model. (Lin et al., 2023) `ev:cited` p. 3 ^lin2023sam-062
- The authors claim a two-stage pipeline, background tokens and Sparse-to-Dense Point Transformers distinguish PEM from earlier one-stage point matching work. (Lin et al., 2023) `ev:asserted` p. 3 ^lin2023sam-063
- The authors conclude that SAM-6D significantly outperforms existing methods on the seven core BOP datasets for [[Novel-object 6D pose estimation|novel-object segmentation and pose estimation]]. (Lin et al., 2023) `ev:asserted` p. 8 ^lin2023sam-064

## 🎯 Contributions

## 📖 Glossary

- **Zero-shot 6D pose estimation** — Detecting novel objects unseen in training and estimating their 3D rotation and translation.
- **Segment Anything Model (SAM)** — Promptable foundation segmentation model with image encoder, prompt encoder and mask decoder.
- **Object matching score** — ISM score combining semantic, appearance and visibility-weighted geometric matching of a proposal.
- **Visible ratio** — Fraction of template patches matched in the proposal, estimating occlusion degree.
- **Background token** — Learnable feature appended to a point set so non-overlapping points match it.
- **Partial-to-partial point matching** — Correspondence between two point sets that each overlap only partly.
- **Sparse-to-Dense Point Transformer** — Geometric attention on sparse points, spread to dense points by linear cross-attention.
- **BOP benchmark** — Standard benchmark for detection, segmentation and 6D pose of specific rigid objects.
- **Average Recall (AR)** — BOP pose metric averaging recall over VSD, MSSD and MSPD error functions.
- **Weighted SVD** — Closed-form rigid transform from point correspondences weighted by matching probabilities.

## ❓ Open questions

- How robust is the geometric score to objects whose bounding boxes are ambiguous under symmetry or heavy occlusion?
- Why does SAM-6D trail refined baselines on ITODD with MaskRCNN masks while leading on most other datasets?
- Can the SAM-based segmentation cost (2.80 s per image) be reduced without losing the accuracy gain over FastSAM?
- Would adding a render-based refiner on top of PEM further improve accuracy, and at what runtime cost?
- How does performance degrade for objects with poor depth, such as transparent or reflective items?
- Does the method require an accurate CAD model, and how does it behave with reconstructed or noisy object models?

## 📝 Notes on reading

Version read: arXiv 2311.15707v2 (6 Mar 2024), including the supplementary material (pages 12–19), matching the packet identifier.

The text of Sec. 4.2.1 (p. 7) refers to Table 5 for the pose comparison with existing methods, but those results are in Table 2; Table 5 is the transformer ablation.

Table 8 (p. 14): the SAM-based SAM-6D detection mean (44.9) is below the FastSAM-based one (47.1), and its YCB-V value (51.9) is below CNOS with FastSAM (56.8), so the claim on p. 12 that ISM outperforms both methods holds at the mean level, not for every configuration.

Table 9 (p. 14) is not strictly monotonic in model size: FastSAM-x with ViT-L (62.0) exceeds SAM-H with ViT-L (60.5), and SAM-H with ViT-S (47.1) is slightly below SAM-L with ViT-S (47.2); the positive-correlation statement on p. 12 is a general trend.

The training set size on p. 6 is extracted with spaced digits (2, 000, 000 images across about 50, 000 objects); the exact figures were not claimed.

Table 10 lists the GPU as DeForce RTX 3090, a typo for GeForce. Section B.4 labels the Pose Estimation Model as (ISM), also a typo. Table 7 writes point per size, presumably points per side.

Equations (1)–(14) are partly garbled in extraction; formulas were described in words rather than copied. Figures 1, 3, 4–10 are architecture diagrams or qualitative visualizations and were not claimed; Fig. 7 shows ViT-Base features of 14 × 14 × 1024 reshaped to 224 × 224 × 256, and Fig. 8 shows two Set Abstract Levels with radii 0.1 and 0.2.

The detection/segmentation column of Table 2 is merged across rows in extraction; the assignment of CNOS (FastSAM) masks to MegaPose*, ZeroPose*, GigaPose and one SAM-6D row follows the table layout.

## Suggested new concepts

- Background tokens for partial point matching — a cheap alternative to optimal transport for handling non-overlapping points in registration.
- Template-based novel object segmentation — CNOS-style proposal scoring against rendered templates is a reusable pattern for model-based detection of unseen objects.
- Foundation-model pipelines for zero-shot pose — SAM and DINOv2 used without fine-tuning as front ends for 6D pose estimation.
- Coarse-to-fine point matching — two-stage correspondence where an initial pose conditions positional encodings for dense matching.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Alternativa *zero-shot* a FoundationPose

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
