---
aliases: []
type: "source"
title: "SAM 2: Segment Anything in Images and Videos"
citekey: "Ravi2024sam"
doi: "10.48550/arXiv.2408.00714"
arxiv: "2408.00714"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2408.00714"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Nikhila Ravi", "Valentin Gabeur", "Yuan-Ting Hu", "Ronghang Hu", "Chaitanya Ryali", "Tengyu Ma", "Haitham Khedr", "Roman Rädle", "Chloe Rolland", "Laura Gustafson", "Eric Mintun", "Junting Pan", "Kalyan Vasudev Alwala", "Nicolas Carion", "Chao-Yuan Wu", "Ross Girshick", "Piotr Dollár", "Christoph Feichtenhofer"]
sha256: ["664f5c4254db441569ecfe36a2a2fa91a1ecec5f4d31b3bcc5d451193efc2c0d"]
pdf: "Content/Papers/Ravi2024sam.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Ravi2024sam.pdf]]

> [!abstract] One-sentence summary
> SAM 2 extends promptable segmentation from images to video with a streaming-memory transformer and a model-in-the-loop data engine that built the SA-V dataset, improving interactive video accuracy with fewer interactions and running faster than SAM on images.

## Abstract

We present Segment Anything Model 2 (SAM 2), a foundation model towards solving promptable visual segmentation in images and videos. We build a data engine, which improves model and data via user interaction, to collect the largest video segmentation dataset to date. Our model is a simple transformer architecture with streaming memory for real-time video processing. SAM 2 trained on our data provides strong performance across a wide range of tasks. In video segmentation, we observe better accuracy, using 3x fewer interactions than prior approaches. In image segmentation, our model is more accurate and 6x faster than the Segment Anything Model (SAM). We believe that our data, model, and insights will serve as a significant milestone for video segmentation and related perception tasks. We are releasing our main model, dataset, as well as code for model training and our demo. (arXiv)

## 🧠 Key ideas (atomic)

- SAM 2 is a unified model for video and image segmentation that considers an image as a single-frame video. (Ravi et al., 2024) `ev:asserted` p. 1 ^ravi2024sam-001
- The Promptable Visual Segmentation task accepts points, boxes, or masks on any video frame to define a segment whose masklet is predicted. (Ravi et al., 2024) `ev:reported` p. 1 ^ravi2024sam-002
- SAM 2 is equipped with a memory that stores information about the target object and previous interactions across video frames. (Ravi et al., 2024) `ev:asserted` p. 1 ^ravi2024sam-003
- When SAM 2 is applied to single images, its memory is empty and the model behaves like the original SAM model. (Ravi et al., 2024) `ev:asserted` p. 1 ^ravi2024sam-004
- The SAM 2 image encoder is an MAE pre-trained Hiera network that runs only once per interaction to provide unconditioned frame embeddings. (Ravi et al., 2024) `ev:reported` p. 4 ^ravi2024sam-005
- Memory attention stacks transformer blocks performing self-attention, cross-attention to stored memories and object pointers, and an MLP. (Ravi et al., 2024) `ev:reported` p. 5 ^ravi2024sam-006
- SAM 2 adds an extra head that predicts whether the object of interest is present on the current frame, for example under occlusion. (Ravi et al., 2024) `ev:reported` p. 5 ^ravi2024sam-007
- The memory bank keeps a FIFO queue of up to N recent frame memories and a queue of up to M prompted frames. (Ravi et al., 2024) `ev:reported` p. 5 ^ravi2024sam-008
- Temporal position information is embedded into the memories of the N recent frames but not into those of prompted frames. (Ravi et al., 2024) `ev:reported` p. 5 ^ravi2024sam-009
- Training samples 8-frame sequences and randomly selects up to 2 frames to prompt, simulating interactive prompting with corrective clicks. (Ravi et al., 2024) `ev:reported` p. 6 ^ravi2024sam-010
- Initial training prompts are the ground-truth mask with probability 0.5, a positive click with 0.25, or a bounding box with 0.25. (Ravi et al., 2024) `ev:reported` p. 6 ^ravi2024sam-011
- During data engine Phase 1, annotators used image-based SAM on every frame at 6 FPS, averaging 37.8 seconds per frame. (Ravi et al., 2024) `ev:measured` p. 6 ^ravi2024sam-012
- Phase 1 of the data engine collected 16K masklets across 1.4K videos using SAM per frame without any tracking model. (Ravi et al., 2024) `ev:reported` p. 6 ^ravi2024sam-013
- In Phase 2, propagating masks with SAM 2 Mask cut annotation time to 7.4 s/frame, a ∼5.1x speed up over Phase 1. (Ravi et al., 2024) `ev:measured` p. 6 ^ravi2024sam-014
- In Phase 3, the fully-featured SAM 2 in the loop reduced annotation time to 4.5 seconds per frame, a ∼8.4x speed up over Phase 1. (Ravi et al., 2024) `ev:measured` p. 6 ^ravi2024sam-015
- Phase 3 of the data engine, with the fully-featured SAM 2 in the loop, collected 197.0K masklets. (Ravi et al., 2024) `ev:reported` p. 6 ^ravi2024sam-016
- Masklets judged unsatisfactory by a separate set of verifying annotators were sent back to the annotation pipeline for refinement. (Ravi et al., 2024) `ev:reported` p. 6 ^ravi2024sam-017
- In a controlled comparison, Phase 3 annotators edited 19.04 % of frames per masklet, against 23.25 % in Phase 2. (Ravi et al., 2024) `ev:measured` p. 7 ^ravi2024sam-018
- Phase 3 annotation reached a Phase 1 Mask Alignment Score of 89.1 % against 86.4 % for Phase 2 annotation. (Ravi et al., 2024) `ev:measured` p. 7 ^ravi2024sam-019
- Automatic masklets were generated by prompting SAM 2 with a regular grid of points on the first frame, then verified by annotators. (Ravi et al., 2024) `ev:reported` p. 7 ^ravi2024sam-020
- With iterations fixed, SA-V val J&F rose from 50.0 with VOS plus SA-1B training data to 63.2 after adding all phases and Auto. (Ravi et al., 2024) `ev:measured` p. 7 ^ravi2024sam-021
- The SA-V dataset comprises 50.9K videos with 642.6K masklets, collected through the model-in-the-loop data engine. (Ravi et al., 2024) `ev:reported` p. 7 ^ravi2024sam-022
- SA-V annotations include 190.9K manual masklets and 451.7K automatic masklets generated with the data engine. (Ravi et al., 2024) `ev:reported` p. 7 ^ravi2024sam-023
- SA-V contains 53× more annotated masks than any existing VOS dataset, or 15× more without the automatic annotations. (Ravi et al., 2024) `ev:reported` p. 7 ^ravi2024sam-024
- SA-V videos were captured by crowdworkers and comprise 54% indoor and 46% outdoor scenes from diverse everyday environments. (Ravi et al., 2024) `ev:reported` p. 7 ^ravi2024sam-025
- SA-V videos range from 4 seconds to 2.3 minutes in duration, averaging 13.8 seconds and totaling 196 hours. (Ravi et al., 2024) `ev:reported` p. 20 ^ravi2024sam-026
- The disappearance rate of SA-V Manual, the share of masklets that vanish and re-appear, is 42.5%, competitive among existing datasets. (Ravi et al., 2024) `ev:measured` p. 7 ^ravi2024sam-027
- More than 88% of SA-V masks have a normalized mask area less than 0.1 relative to video resolution. (Ravi et al., 2024) `ev:measured` p. 20 ^ravi2024sam-028
- The SA-V val split contains 293 masklets in 155 videos targeting fast-moving, occluded or disappearing objects annotated at 6 FPS. (Ravi et al., 2024) `ev:reported` p. 9 ^ravi2024sam-029
- Across 9 densely annotated zero-shot video datasets, SAM 2 outperforms SAM+XMem++ and SAM+Cutie in both offline and online interactive evaluation. (Ravi et al., 2024) `ev:measured` p. 10 ^ravi2024sam-030
- The authors report that SAM 2 generates better interactive segmentation accuracy while needing more than 3× fewer interactions than baselines. (Ravi et al., 2024) `ev:measured` p. 10 ^ravi2024sam-031
- In interactive offline evaluation over 8 interacted frames, SAM 2 averages 80.3 J&F versus 74.7 for SAM+Cutie and 71.7 for SAM+XMem++. (Ravi et al., 2024) `ev:measured` p. 24 ^ravi2024sam-032
- In interactive online evaluation over 8 interacted frames, SAM 2 averages 79.8 J&F compared with 74.0 for SAM+Cutie. (Ravi et al., 2024) `ev:measured` p. 25 ^ravi2024sam-033
- With 1-click prompts on the first frame, SAM 2 averages 64.7 accuracy across 17 video datasets versus 56.9 for SAM+XMem++. (Ravi et al., 2024) `ev:measured` p. 10 ^ravi2024sam-034
- With ground-truth first-frame masks, SAM 2 averages 79.3 across 17 video datasets versus 74.1 for Cutie and 72.7 for XMem++. (Ravi et al., 2024) `ev:measured` p. 10 ^ravi2024sam-035
- On the 23 SAM benchmark datasets, SAM 2 reaches 58.9 1-click mIoU versus 58.1 for SAM, using no extra data. (Ravi et al., 2024) `ev:measured` p. 10 ^ravi2024sam-036
- SAM 2 runs the Segment Anything image task at 130.1 FPS compared with 21.7 FPS for SAM on a single A100. (Ravi et al., 2024) `ev:measured` p. 11 ^ravi2024sam-037
- Trained on the image and video mix, SAM 2 reaches 61.9 1-click mIoU on SA-23, up from 58.9 when trained on SA-1B alone. (Ravi et al., 2024) `ev:measured` p. 11 ^ravi2024sam-038
- On 14 new zero-shot video datasets evaluated as images, SAM 2 trained on the mix reaches 69.6 1-click mIoU versus 59.1 for SAM. (Ravi et al., 2024) `ev:measured` p. 11 ^ravi2024sam-039
- SAM 2 Hiera-B+ surpasses SAM on 29 of 37 image-task datasets by up to 53.9 mIoU, despite a smaller image encoder. (Ravi et al., 2024) `ev:measured` p. 28 ^ravi2024sam-040
- On SA-V val, SAM 2 Hiera-L reaches 77.9 J&F, whereas the best prior method, SwinB-DeAOT, reaches 61.4. (Ravi et al., 2024) `ev:measured` p. 11 ^ravi2024sam-041
- On MOSE val, SAM 2 Hiera-L reaches 77.9 J&F compared with 71.7 for Cutie-base+, the strongest listed prior method. (Ravi et al., 2024) `ev:measured` p. 11 ^ravi2024sam-042
- On the LVOS val long-term benchmark, SAM 2 reaches 78.0 J&F compared with 66.0 for Cutie-base. (Ravi et al., 2024) `ev:measured` p. 11 ^ravi2024sam-043
- The authors observe that most previous VOS methods peak at around the same accuracy on the open-world SA-V val and test sets. (Ravi et al., 2024) `ev:measured` p. 11 ^ravi2024sam-044
- On the DAVIS interactive benchmark with clicks, SAM 2 scores 0.86 AUC-J&F and 0.90 J&F@60s, above CiVOS with 0.83 and 0.84. (Ravi et al., 2024) `ev:measured` p. 27 ^ravi2024sam-045
- The authors note SAM 2 often segments object parts on the first click, which could penalize its score on DAVIS whole-object annotations. (Ravi et al., 2024) `ev:asserted` p. 27 ^ravi2024sam-046
- A model purely trained on existing VOS datasets performs poorly on zero-shot benchmarks, reaching 59.7 J&F on 9 zero-shot datasets. (Ravi et al., 2024) `ev:measured` p. 13 ^ravi2024sam-047
- Adding data engine data to the training mix yields a +12.1% average improvement on the 9 zero-shot video datasets. (Ravi et al., 2024) `ev:measured` p. 13 ^ravi2024sam-048
- Video segmentation accuracy follows a consistent power law relationship with the quantity of SA-V training data on all three benchmarks. (Ravi et al., 2024) `ev:measured` p. 13 ^ravi2024sam-049
- Training on the 50k most edited SA-V masklets gave 66.2 SA-V val J&F, versus 63.7 for 50k randomly sampled masklets. (Ravi et al., 2024) `ev:measured` p. 13 ^ravi2024sam-050
- Using fewer channels for memories does not cause much performance regression while making memory storage 4× smaller. (Ravi et al., 2024) `ev:measured` p. 14 ^ravi2024sam-051
- Scaling the image encoder brings gains on image and video metrics, whereas scaling memory attention only improves video metrics. (Ravi et al., 2024) `ev:measured` p. 14 ^ravi2024sam-052
- Memory ablations suggest that feeding memory features through a GRU provides no improvement, except slightly on LVOSv2. (Ravi et al., 2024) `ev:measured` p. 15 ^ravi2024sam-053
- Cross-attending to object pointers does not raise the 9 zero-shot average but significantly boosts SA-V val and LVOSv2 performance. (Ravi et al., 2024) `ev:measured` p. 15 ^ravi2024sam-054
- SAM 2 may fail to segment objects across shot changes and can lose track in crowded scenes or after long occlusions. (Ravi et al., 2024) `ev:asserted` p. 16 ^ravi2024sam-055
- SAM 2 struggles to track objects with very thin or fine details, especially when those objects are fast-moving. (Ravi et al., 2024) `ev:asserted` p. 16 ^ravi2024sam-056
- SAM 2 processes each tracked object separately, sharing only per-frame image embeddings without any inter-object communication. (Ravi et al., 2024) `ev:reported` p. 16 ^ravi2024sam-057
- The data engine relies on human annotators to verify masklet quality and to select frames that require correction. (Ravi et al., 2024) `ev:asserted` p. 16 ^ravi2024sam-058
- With 1-click prompts, SAM 2 reaches 81.9 J&F for male and 75.1 for female subjects in Ego-Exo4D people segmentation. (Ravi et al., 2024) `ev:measured` p. 20 ^ravi2024sam-059
- Restricting to clips where the person is correctly segmented shrinks the 1-click gap to 94.3 male versus 92.7 female. (Ravi et al., 2024) `ev:measured` p. 20 ^ravi2024sam-060
- At 3 clicks and with ground-truth mask prompts, the authors find minimal discrepancy in J&F across gender and age groups. (Ravi et al., 2024) `ev:measured` p. 20 ^ravi2024sam-061
- Training the released SAM 2 on 256 A100 GPUs for 108 hours corresponds to an estimated 3.89 metric tons of CO2e emissions. (Ravi et al., 2024) `ev:computed` p. 32 ^ravi2024sam-062

## 🎯 Contributions

## 📖 Glossary

- **Masklet** — a spatio-temporal segmentation mask of one object across video frames.
- **Promptable Visual Segmentation (PVS)** — segmenting an object throughout a video from prompts given on any frame.
- **Semi-supervised VOS** — tracking an object through a video given only its first-frame mask.
- **Memory bank** — FIFO store of past-frame and prompted-frame memories used to condition current predictions.
- **Object pointer** — lightweight vector from mask decoder tokens carrying high-level semantic object information.
- **J&F** — video segmentation metric averaging region similarity J and contour accuracy F.
- **Disappearance rate** — share of masklets that disappear in at least one frame and re-appear.
- **Data engine** — iterative loop where the model assists annotators and is retrained on their annotations.
- **Hiera** — hierarchical vision transformer image encoder providing multiscale features.

## ❓ Open questions

- Would explicit motion modeling reduce failures on similar-looking nearby objects and fast-moving thin structures?
- Could shared object-level context between tracked objects improve efficiency over independent per-object inference?
- Can masklet verification and correction-frame selection in the data engine be automated without losing quality?
- Does scaling the image encoder beyond Hiera-L continue to improve accuracy, as the authors expect?
- How robust is SAM 2 across shot changes and very long videos with extended occlusions?

## 📝 Notes on reading

- Version read: arXiv 2408.00714v2 (28 Oct 2024); results are from the improved checkpoint the authors call SAM 2.1 but refer to as SAM 2 (footnote p. 2).
- Inconsistency: the text on pp. 10 and 27 says training on the image and video mix raises SA-23 accuracy to 61.4%, while Tables 5 and 15 give 61.9 for Hiera-B+ on the mix (61.4 appears in the tables only as the Hiera-L FPS). The claim uses the table value.
- Inconsistency: p. 28 states SAM 2 surpasses SAM on 29 datasets by up to 53.9 mIoU, but the largest delta shown in Fig. 15 (p. 29) is 41.1.
- Page 2 phrases the 8.4× data-engine speed-up as relative to existing model-assisted approaches; Table 1 and p. 6 express it relative to Phase 1 (SAM per frame). The claims follow pp. 6-7.
- SA-V average video duration is 14 seconds on p. 7 and 13.8 seconds on p. 20 (rounding).
- Figures 5, 6, 12a, 13a and 14 are curves or bar charts whose values could only be read from axis ticks; only tabulated averages (Figs. 12b, 13b) were claimed.
- Table 17 (p. 31) and the Table 9/10/11 ablation rows are partly flattened by extraction; checkmark columns in Tables 7, 10 and 11 cannot be reliably mapped to rows, so row-level values were not claimed except where the text names them.

## Suggested new concepts

- Promptable Visual Segmentation — task that generalizes image promptable segmentation and semi-supervised VOS to interactive video.
- Streaming memory attention — mechanism for conditioning per-frame features on a memory bank, reusable across video models.
- Model-in-the-loop data engine — annotation strategy used by SAM and SAM 2 whose speed-ups are quantified phase by phase.
- SA-V dataset — large open video segmentation benchmark likely cited by later video segmentation and tracking work.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Máscaras y seguimiento en vídeo para FoundationPose
