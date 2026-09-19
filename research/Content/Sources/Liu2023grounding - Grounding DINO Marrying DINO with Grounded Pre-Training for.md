---
aliases: []
type: "source"
title: "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection"
citekey: "Liu2023grounding"
doi: "10.48550/arXiv.2303.05499"
arxiv: "2303.05499"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2303.05499"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Shilong Liu", "Zhaoyang Zeng", "Tianhe Ren", "Feng Li", "Hao Zhang", "Jie Yang", "Qing Jiang", "Chunyuan Li", "Jianwei Yang", "Hang Su", "Jun Zhu", "Lei Zhang"]
sha256: ["ba1c64ec2ac4fedeb50b269eadc994456a8428dbe64a8dba2673f22df0fa20b3"]
pdf: "Content/Papers/Liu2023grounding.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Liu2023grounding.pdf]]

> [!abstract] One-sentence summary
> Grounding DINO fuses language into the DETR-like detector DINO at the neck, query-initialization and head stages and pre-trains it on detection, grounding and caption data, giving a text-promptable open-set detector that reaches 52.5 AP zero-shot on COCO and 26.1 mean AP zero-shot on ODinW.

## Abstract

In this paper, we present an open-set object detector, called Grounding DINO, by marrying Transformer-based detector DINO with grounded pre-training, which can detect arbitrary objects with human inputs such as category names or referring expressions. The key solution of open-set object detection is introducing language to a closed-set detector for open-set concept generalization. To effectively fuse language and vision modalities, we conceptually divide a closed-set detector into three phases and propose a tight fusion solution, which includes a feature enhancer, a language-guided query selection, and a cross-modality decoder for cross-modality fusion. While previous works mainly evaluate open-set object detection on novel categories, we propose to also perform evaluations on referring expression comprehension for objects specified with attributes. Grounding DINO performs remarkably well on all three settings, including benchmarks on COCO, LVIS, ODinW, and RefCOCO/+/g. Grounding DINO achieves a $52.5$ AP on the COCO detection zero-shot transfer benchmark, i.e., without any training data from COCO. It sets a new record on the ODinW zero-shot benchmark with a mean $26.1$ AP. Code will be available at \url{https://github.com/IDEA-Research/GroundingDINO}. (arXiv)

## 🧠 Key ideas (atomic)

- Grounding DINO is an open-set object detector built on DINO that detects arbitrary objects specified by category names or referring expressions. (Liu et al., 2023) `ev:asserted` p. 1 ^liu2023grounding-001
- The authors design Grounding DINO around two principles, tight modality fusion based on DINO plus large-scale grounded pre-training for concept generalization. (Liu et al., 2023) `ev:asserted` p. 2 ^liu2023grounding-002
- The paper frames feature fusion in open-set detectors as occurring in three phases: neck, query initialization, and head. (Liu et al., 2023) `ev:asserted` p. 3 ^liu2023grounding-003
- OV-DETR injects language information only at the decoder inputs, which the authors classify as query-initialization fusion or phase B. (Liu et al., 2023) `ev:cited` p. 5 ^liu2023grounding-004
- The authors argue that more feature fusion in the pipeline can facilitate better alignment between different modality features. (Liu et al., 2023) `ev:asserted` p. 3 ^liu2023grounding-005
- The authors state that Transformer-based detectors such as DINO have a layer-by-layer structure consistent with language blocks, easing language interaction. (Liu et al., 2023) `ev:asserted` p. 3 ^liu2023grounding-006
- Citing RegionCLIP, the authors note that CLIP pre-trained on image-text pairs has limited efficacy for region-text detection tasks. (Liu et al., 2023) `ev:cited` p. 3 ^liu2023grounding-007
- The authors argue that GLIP's direct concatenation of category names ignores the potential influence of unrelated categories on each other. (Liu et al., 2023) `ev:asserted` p. 3 ^liu2023grounding-008
- Word-level text representation encodes multiple category names in one forward pass but introduces unnecessary dependencies among categories, per the authors. (Liu et al., 2023) `ev:asserted` p. 7 ^liu2023grounding-009
- The sub-sentence level text representation applies attention masks that block attention among unrelated category names in the concatenated prompt. (Liu et al., 2023) `ev:asserted` p. 8 ^liu2023grounding-010
- The authors state that the sub-sentence representation keeps per-word features, preserving fine-grained understanding of the input text. (Liu et al., 2023) `ev:asserted` p. 8 ^liu2023grounding-011
- The authors advocate a fully zero-shot evaluation over the partial-label protocol of training on base categories and testing on others. (Liu et al., 2023) `ev:asserted` p. 3 ^liu2023grounding-012
- The paper extends open-set detection evaluation to referring expression comprehension, where target objects are described with attributes. (Liu et al., 2023) `ev:asserted` p. 3 ^liu2023grounding-013
- Grounding DINO is a dual-encoder-single-decoder architecture with image and text backbones, a feature enhancer, query selection, and a cross-modality decoder. (Liu et al., 2023) `ev:reported` p. 6 ^liu2023grounding-014
- For the REC task, the model uses the output object with the largest score as its single predicted box. (Liu et al., 2023) `ev:reported` p. 6 ^liu2023grounding-015
- The feature enhancer uses deformable self-attention for image features, vanilla self-attention for text features, and bidirectional image-text cross-attention for fusion. (Liu et al., 2023) `ev:reported` p. 6 ^liu2023grounding-016
- Language-guided query selection picks the top 900 image tokens by their maximum dot product with text features as decoder queries. (Liu et al., 2023) `ev:reported` p. 7 ^liu2023grounding-017
- Following DINO's mixed query selection, the positional query parts are dynamic anchor boxes initialized from encoder outputs. (Liu et al., 2023) `ev:reported` p. 7 ^liu2023grounding-018
- Each cross-modality decoder layer has an extra text cross-attention layer compared with the DINO decoder layer, to inject text information. (Liu et al., 2023) `ev:reported` p. 7 ^liu2023grounding-019
- Classification uses a contrastive loss between predicted objects and language tokens, computing a focal loss on each token logit. (Liu et al., 2023) `ev:reported` p. 8 ^liu2023grounding-020
- Two variants were trained, Grounding DINO T with a Swin-T backbone and Grounding DINO L with a Swin-L backbone. (Liu et al., 2023) `ev:reported` p. 9 ^liu2023grounding-021
- Both variants use BERT-base from Hugging Face as the text backbone, with a maximum of 256 text tokens. (Liu et al., 2023) `ev:reported` p. 9 ^liu2023grounding-022
- Swin-T models were trained on 16 Nvidia V100 GPUs with a total batch size of 32. (Liu et al., 2023) `ev:reported` p. 9 ^liu2023grounding-023
- The Swin-L model was trained on 64 Nvidia A100 GPUs with a total batch size of 64. (Liu et al., 2023) `ev:reported` p. 9 ^liu2023grounding-024
- Training uses the AdamW optimizer with a learning rate of 1e-4, lowered to 1e-5 for the image and text backbones. (Liu et al., 2023) `ev:reported` p. 19 ^liu2023grounding-025
- Detection data from COCO, O365 and OpenImage are reformulated as phrase grounding by concatenating category names into text prompts. (Liu et al., 2023) `ev:reported` p. 20 ^liu2023grounding-026
- The grounding data are GoldG and RefC, both preprocessed by MDETR, with GoldG drawing images from Flickr30k entities and Visual Genome. (Liu et al., 2023) `ev:reported` p. 20 ^liu2023grounding-027
- Grounding DINO L reaches 52.5 AP on COCO zero-shot transfer without seeing any COCO images during training. (Liu et al., 2023) `ev:measured` p. 10 ^liu2023grounding-028
- In zero-shot COCO transfer under the same setting, Grounding DINO outperforms DINO by +0.5AP and GLIP by +1.8AP. (Liu et al., 2023) `ev:measured` p. 9 ^liu2023grounding-029
- Adding GoldG grounding data raises Grounding DINO T's COCO zero-shot AP from 46.7 to 48.1. (Liu et al., 2023) `ev:measured` p. 9 ^liu2023grounding-030
- After COCO fine-tuning, Grounding DINO obtains 62.6 AP on COCO minival, outperforming DINO's 62.5 AP. (Liu et al., 2023) `ev:measured` p. 10 ^liu2023grounding-031
- With 1.5× larger input images and COCO fine-tuning, Grounding DINO reaches 63.0 AP on COCO test-dev. (Liu et al., 2023) `ev:measured` p. 10 ^liu2023grounding-032
- On LVIS zero-shot, Grounding DINO T pre-trained with O365, GoldG and Cap4M reaches 27.4 AP versus 26.0 for GLIP-T. (Liu et al., 2023) `ev:measured` p. 10 ^liu2023grounding-033
- On LVIS, Grounding DINO works better than GLIP on common objects but worse on rare categories. (Liu et al., 2023) `ev:measured` p. 10 ^liu2023grounding-034
- The authors note that DETR-like models often show lower rare-category AP on LVIS, which may be a characteristic architectural limitation. (Liu et al., 2023) `ev:asserted` p. 10 ^liu2023grounding-035
- Adding Cap4M caption data gives Grounding DINO +1.8 AP on LVIS, whereas GLIP gains only +1.1 AP. (Liu et al., 2023) `ev:measured` p. 10 ^liu2023grounding-036
- The authors believe Grounding DINO has better scalability than GLIP, leaving larger-scale training as future work. (Liu et al., 2023) `ev:asserted` p. 10 ^liu2023grounding-037
- In LVIS zero-shot, Grounding DINO T scores below DetCLIPv2, which is trained on larger-scale data, at 27.4 versus 40.4 AP. (Liu et al., 2023) `ev:measured` p. 10 ^liu2023grounding-038
- Fine-tuned on LVIS, Grounding DINO T pre-trained only on O365 and GoldG outperforms DetCLIPv2-T by 1.5 AP. (Liu et al., 2023) `ev:measured` p. 11 ^liu2023grounding-039
- Grounding DINO L sets a new ODinW zero-shot record of 26.1 AP, even outperforming the giant Florence models. (Liu et al., 2023) `ev:measured` p. 12 ^liu2023grounding-040
- On ODinW zero-shot, Grounding DINO T and GLIPv2-T show similar average AP, but median AP is 11.9 versus 8.9. (Liu et al., 2023) `ev:measured` p. 11 ^liu2023grounding-041
- The authors suggest the higher median AP indicates more consistent performance across datasets than GLIPv2, which may show larger variance. (Liu et al., 2023) `ev:asserted` p. 11 ^liu2023grounding-042
- At 172M parameters, Grounding DINO T is more compact than GLIPv2, which has 232M parameters according to the authors. (Liu et al., 2023) `ev:reported` p. 12 ^liu2023grounding-043
- On ODinW full-shot, Grounding DINO with a Swin-T backbone outperforms DINO with Swin-L, 70.7 versus 68.8 average AP. (Liu et al., 2023) `ev:measured` p. 11 ^liu2023grounding-044
- Without REC data, Grounding DINO T pre-trained on O365 and GoldG outperforms GLIP-T(B) on RefCOCO val, 50.41 versus 49.96. (Liu et al., 2023) `ev:measured` p. 12 ^liu2023grounding-045
- The authors report that both GLIP and Grounding DINO do not perform well on REC benchmarks without REC training data. (Liu et al., 2023) `ev:measured` p. 12 ^liu2023grounding-046
- Adding RefCOCO/+/g to pre-training raises Grounding DINO T's RefCOCO val accuracy from 50.41 to 73.98 without fine-tuning. (Liu et al., 2023) `ev:measured` p. 12 ^liu2023grounding-047
- With fine-tuning, Grounding DINO L reaches 90.56 top-1 accuracy on RefCOCO val, above DQ-DETR's 88.63. (Liu et al., 2023) `ev:measured` p. 12 ^liu2023grounding-048
- The authors caution that the Grounding DINO L REC results might include a data leak, since COCO includes RefC validation images. (Liu et al., 2023) `ev:asserted` p. 12 ^liu2023grounding-049
- Adding RefC to pre-training raises COCO zero-shot AP to 48.5 but lowers LVIS zero-shot AP from 25.6 to 21.9. (Liu et al., 2023) `ev:measured` p. 13 ^liu2023grounding-050
- In the Swin-T O365 ablation, removing encoder fusion lowers LVIS zero-shot AP from 16.1 to 13.1. (Liu et al., 2023) `ev:measured` p. 14 ^liu2023grounding-051
- Language-guided query selection, text cross-attention and sub-sentence prompts yield LVIS gains of +3.0 AP, +1.8 AP, and +0.5 AP respectively. (Liu et al., 2023) `ev:measured` p. 13 ^liu2023grounding-052
- Language-guided query selection and the sub-sentence text prompt had minimal impact on COCO fine-tune performance in the ablation. (Liu et al., 2023) `ev:measured` p. 13 ^liu2023grounding-053
- The authors interpret the ablation as suggesting fine-tuning performance is predominantly influenced by model parameters, making model scaling a promising direction. (Liu et al., 2023) `ev:asserted` p. 13 ^liu2023grounding-054
- Among its stated limitations, the authors note that Grounding DINO cannot be used for segmentation tasks, unlike GLIPv2. (Liu et al., 2023) `ev:asserted` p. 14 ^liu2023grounding-055
- The authors note their training data is less than the largest GLIP model's, which may limit final performance. (Liu et al., 2023) `ev:asserted` p. 14 ^liu2023grounding-056
- The authors find that the model produces false positive results in some cases, which may need more techniques or data. (Liu et al., 2023) `ev:asserted` p. 14 ^liu2023grounding-057
- The authors conclude that existing open-set detectors do not work well for REC data without fine-tuning. (Liu et al., 2023) `ev:asserted` p. 14 ^liu2023grounding-058
- Initializing from a pre-trained DINO and freezing shared modules gives 26.1 LVIS zero-shot AP, above 25.6 from scratch. (Liu et al., 2023) `ev:measured` p. 21 ^liu2023grounding-059
- In training curves on O365, Grounding DINO initialized from pre-trained DINO converges faster than Grounding DINO trained from scratch. (Liu et al., 2023) `ev:measured` p. 21 ^liu2023grounding-060
- In the closed-set COCO 1× setting with ResNet-50, Grounding DINO reaches 48.1 AP, below DINO-4scale's 49.0 AP. (Liu et al., 2023) `ev:measured` p. 22 ^liu2023grounding-061
- The authors suspect that the new components may make Grounding DINO harder to optimize than the original DINO. (Liu et al., 2023) `ev:asserted` p. 22 ^liu2023grounding-062
- Grounding DINO T runs at 8.37 FPS with 464G GFLOPS, compared with 6.11 FPS and 488G for GLIP-T. (Liu et al., 2023) `ev:measured` p. 26 ^liu2023grounding-063
- On combined RefCOCO data, Grounding DINO with BERT-B outperformed or matched the BERT-L variant in most REC metrics. (Liu et al., 2023) `ev:measured` p. 24 ^liu2023grounding-064
- The authors suggest that the main limitation in enhancing REC performance lies within the detection branch rather than the language module. (Liu et al., 2023) `ev:asserted` p. 24 ^liu2023grounding-065
- On the ODinW PlantDoc dataset, Grounding DINO scores 0.36 compared with GLIP's 1.1, underperforming on some uncommon datasets. (Liu et al., 2023) `ev:measured` p. 24 ^liu2023grounding-066
- With Detic pseudo-labeled IN22K-LVIS-1M data, Grounding DINO T reaches 40.6 LVIS AP, though this may not be real zero-shot. (Liu et al., 2023) `ev:measured` p. 32 ^liu2023grounding-067
- For image editing, Grounding DINO detections are turned into masks and passed with generation prompts to a Stable Diffusion inpainting model. (Liu et al., 2023) `ev:reported` p. 26 ^liu2023grounding-068

## 🎯 Contributions

## 📖 Glossary

- **Open-set object detection** — Detecting arbitrary objects named by free-form language, beyond a fixed category list.
- **Referring expression comprehension (REC)** — Localizing the single object described by a natural-language phrase with attributes.
- **DINO (detector)** — End-to-end DETR-like Transformer detector with contrastive denoising and mixed query selection.
- **Feature enhancer** — Neck module fusing image and text features with self- and cross-attention layers.
- **Language-guided query selection** — Choosing decoder queries from image tokens most similar to the text features.
- **Cross-modality decoder** — DETR decoder with added text cross-attention in each layer.
- **Sub-sentence text representation** — Per-word text features with attention masks blocking unrelated category names.
- **ODinW** — Object Detection in the Wild benchmark collecting more than 35 real-world datasets.
- **GoldG** — MDETR-preprocessed grounding data from Flickr30k entities and Visual Genome.
- **RefC** — Shorthand for the RefCOCO, RefCOCO+ and RefCOCOg datasets together.
- **Zero-shot (this paper)** — Evaluation where the test dataset's training split is not used in training.

## ❓ Open questions

- Can DETR-like open-set detectors close the rare-category AP gap on LVIS without extra training data?
- How far does Grounding DINO's data scalability advantage over GLIP extend at larger pre-training scales?
- How can zero-shot REC performance be improved, given that the detection branch appears to be the bottleneck?
- What techniques or data would reduce the false-positive (hallucinated) detections the authors observe?
- Why does adding RefC or COCO data hurt LVIS and ODinW zero-shot results, and can this trade-off be avoided?
- Can the architecture be extended to segmentation, as GLIPv2 does?
- How well does text-prompted detection transfer to uncommon domains (e.g. PlantDoc-like categories) absent from training data?

## 📝 Notes on reading

- Version read: arXiv 2303.05499v5 (19 Jul 2024), 33 pages including appendices. The registry abstract is the v1 wording (says code will be available); the v5 PDF abstract also mentions pre-training data and releasing checkpoints.
- Hyperparameter inconsistency: the main text (p. 9) gives Hungarian matching cost weights 2.0/5.0/2.0 and loss weights 1.0/5.0/2.0 for classification/L1/GIOU, while Table 8 (p. 19) lists set cost class 1.0 and ce loss coef 2.0, i.e. swapped. Not claimed.
- Query-number ablation inconsistency: text on p. 23 says 1200 and 1500 queries slightly outperform 900 on LVIS rare classes, but Table 15 (p. 31) shows APr 9.4 for 900 vs 9.0 and 9.2. Not claimed.
- Table 5 caption (p. 12) says all models use a ResNet-101 backbone, contradicting the Swin-T/Swin-L rows in the same table.
- Minor reference slips: OV-DETR is cited as [56] and GLIP as [12] on p. 4 (elsewhere [55] and [25]); the training-curve figure on p. 21 is captioned Table 10 but referenced as Fig. 10; the closed-set COCO setting is pointed to Sec. C.2 from Sec. 4.
- Data setup not claimed separately: Grounding DINO T uses O365v1 (about 600K images) and Grounding DINO L uses O365v2 (about 1.7M images); caption data are pseudo-labeled by GLIP-T or GLIP-L to match the variant (p. 20).
- ODinW zero-shot claim on p. 11 contrasts the Cap4M-trained Grounding DINO T (22.3 avg, 11.9 median) with GLIPv2-T (22.3, 8.9); Table 18 (p. 33) gives the per-dataset GLIP-T comparison.
- Figures 1, 3, 4, 5, 6, 7, 8, 9 and 10 are architecture diagrams or qualitative visualizations and were only described, not claimed. Per-dataset ODinW tables 12 to 14 were not claimed cell by cell.

## Suggested new concepts

- Open-set object detection — core task framing shared by GLIP, OWL-ViT, DetCLIP and Grounding DINO; worth a hub note.
- Referring expression comprehension — evaluation setting the paper argues open-set detectors should be tested on.
- Language-guided query selection — distinctive mechanism for initializing DETR queries from text-image similarity.
- Grounded pre-training — reformulating detection as phrase grounding to pool detection, grounding and caption data.
- Text-prompted detection for downstream pipelines — Grounding DINO used as a front end for inpainting or grounded generation (Stable Diffusion, GLIGEN), relevant to perception pipelines that locate objects by name.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Detección de "tubo de centrífuga" por texto
