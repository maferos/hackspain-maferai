---
aliases: []
type: "source"
title: "LoRA: Low-Rank Adaptation of Large Language Models"
citekey: "Hu2021lora"
doi: "10.48550/arXiv.2106.09685"
arxiv: "2106.09685"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2106.09685"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Edward J. Hu", "Yelong Shen", "Phillip Wallis", "Zeyuan Allen-Zhu", "Yuanzhi Li", "Shean Wang", "Lu Wang", "Weizhu Chen"]
sha256: ["e9a0d3128767db616085dc0f4e6e455e672e89af823e8ed1282793682787395a"]
pdf: "Content/Papers/Hu2021lora.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Hu2021lora.pdf]]

> [!abstract] One-sentence summary
> LoRA freezes pre-trained Transformer weights and trains small low-rank update matrices, matching or beating full fine-tuning on RoBERTa, DeBERTa, GPT-2 and GPT-3 with far fewer trainable parameters and no added inference latency.

## Abstract

An important paradigm of natural language processing consists of large-scale pre-training on general domain data and adaptation to particular tasks or domains. As we pre-train larger models, full fine-tuning, which retrains all model parameters, becomes less feasible. Using GPT-3 175B as an example -- deploying independent instances of fine-tuned models, each with 175B parameters, is prohibitively expensive. We propose Low-Rank Adaptation, or LoRA, which freezes the pre-trained model weights and injects trainable rank decomposition matrices into each layer of the Transformer architecture, greatly reducing the number of trainable parameters for downstream tasks. Compared to GPT-3 175B fine-tuned with Adam, LoRA can reduce the number of trainable parameters by 10,000 times and the GPU memory requirement by 3 times. LoRA performs on-par or better than fine-tuning in model quality on RoBERTa, DeBERTa, GPT-2, and GPT-3, despite having fewer trainable parameters, a higher training throughput, and, unlike adapters, no additional inference latency. We also provide an empirical investigation into rank-deficiency in language model adaptation, which sheds light on the efficacy of LoRA. We release a package that facilitates the integration of LoRA with PyTorch models and provide our implementations and model checkpoints for RoBERTa, DeBERTa, and GPT-2 at https://github.com/microsoft/LoRA. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state that a fully fine-tuned model contains as many parameters as the original, a critical deployment challenge for GPT-3 175B. (Hu et al., 2021) `ev:asserted` p. 1 ^hu2021lora-001
- Existing parameter-efficient techniques often introduce inference latency by extending model depth or reduce the model's usable sequence length. (Hu et al., 2021) `ev:cited` p. 2 ^hu2021lora-002
- The authors state that existing efficient adaptation methods often fail to match fine-tuning baselines, posing a trade-off between efficiency and model quality. (Hu et al., 2021) `ev:asserted` p. 2 ^hu2021lora-003
- Prior work by Li et al. and Aghajanyan et al. shows that learned over-parametrized models in fact reside on a low intrinsic dimension. (Hu et al., 2021) `ev:cited` p. 2 ^hu2021lora-004
- The authors hypothesize that the change in weights during model adaptation also has a low intrinsic rank, leading to the LoRA approach. (Hu et al., 2021) `ev:asserted` p. 2 ^hu2021lora-005
- LoRA constrains the update of a frozen pre-trained weight matrix W0 to a low-rank product BA with rank r much smaller than min(d, k). (Hu et al., 2021) `ev:reported` p. 4 ^hu2021lora-006
- During LoRA training the pre-trained weights W0 are frozen and receive no gradient updates, whereas A and B contain trainable parameters. (Hu et al., 2021) `ev:reported` p. 4 ^hu2021lora-007
- Matrix A is initialized with a random Gaussian and B with zero, so the update BA is zero at the beginning of training. (Hu et al., 2021) `ev:reported` p. 4 ^hu2021lora-008
- The low-rank update is scaled by alpha divided by r, with alpha set to the first r tried and not tuned. (Hu et al., 2021) `ev:reported` p. 4 ^hu2021lora-009
- At deployment the merged weight W0 plus BA can be stored explicitly, so inference proceeds as usual without additional latency by construction. (Hu et al., 2021) `ev:asserted` p. 4 ^hu2021lora-010
- Switching to another task is done by subtracting BA and adding a different pair B'A', described as a quick operation with little memory overhead. (Hu et al., 2021) `ev:asserted` p. 4 ^hu2021lora-011
- The experiments adapt only the attention weights of the Transformer, with the MLP modules frozen for simplicity and parameter efficiency. (Hu et al., 2021) `ev:reported` p. 5 ^hu2021lora-012
- The authors leave the empirical investigation of adapting MLP layers, LayerNorm layers and biases with LoRA to future work. (Hu et al., 2021) `ev:asserted` p. 5 ^hu2021lora-013
- Most experiments apply LoRA only to the query and value projection matrices Wq and Wv for simplicity. (Hu et al., 2021) `ev:reported` p. 6 ^hu2021lora-014
- On GPT-3 175B, LoRA reduces the VRAM consumption during training from 1.2TB to 350GB, according to the authors. (Hu et al., 2021) `ev:measured` p. 5 ^hu2021lora-015
- With r = 4 and only query and value matrices adapted, the GPT-3 checkpoint size is reduced roughly 10,000× from 350GB to 35MB. (Hu et al., 2021) `ev:measured` p. 5 ^hu2021lora-016
- Storing 100 adapted GPT-3 models requires about 354GB with LoRA, as opposed to about 35TB for 100 full copies. (Hu et al., 2021) `ev:computed` p. 5 ^hu2021lora-017
- The authors observe a 25% speedup during training on GPT-3 175B with LoRA compared with full fine-tuning. (Hu et al., 2021) `ev:measured` p. 5 ^hu2021lora-018
- Training throughput on GPT-3 175B is 43.1 tokens/s per V100 GPU for LoRA against 32.5 tokens/s for full fine-tuning. (Hu et al., 2021) `ev:measured` p. 5 ^hu2021lora-019
- The authors note that batching inputs from different tasks in one forward pass is not straightforward once A and B are merged into W. (Hu et al., 2021) `ev:asserted` p. 5 ^hu2021lora-020
- The evaluation covers RoBERTa, DeBERTa and GPT-2 before scaling up to GPT-3 175B, spanning natural language understanding and generation tasks. (Hu et al., 2021) `ev:reported` p. 5 ^hu2021lora-021
- On GPT-2 medium with batch size 1 and sequence length 128, AdapterH increased single forward-pass latency by 30.3% over the no-adapter baseline. (Hu et al., 2021) `ev:measured` p. 4 ^hu2021lora-022
- With batch size 32 and sequence length 512, AdapterL added 2.2% inference latency on GPT-2 medium over the no-adapter baseline. (Hu et al., 2021) `ev:measured` p. 4 ^hu2021lora-023
- The latency study shows that larger batch size and sequence length help to mitigate the inference slow-down introduced by adapter layers. (Hu et al., 2021) `ev:measured` p. 17 ^hu2021lora-024
- The authors observe that prefix tuning is difficult to optimize, with performance changing non-monotonically in the number of trainable parameters. (Hu et al., 2021) `ev:measured` p. 3 ^hu2021lora-025
- The authors suspect that reserving sequence length for adaptation makes prompt tuning less performant, since it reduces the length available for the task. (Hu et al., 2021) `ev:asserted` p. 3 ^hu2021lora-026
- On GLUE, RoBERTa base with LoRA and 0.3M trainable parameters reached an average of 87.2, above 86.4 for full fine-tuning. (Hu et al., 2021) `ev:measured` p. 6 ^hu2021lora-027
- RoBERTa large with LoRA and 0.8M trainable parameters averaged 89.0 on GLUE, against 88.9 for full fine-tuning with 355.0M parameters. (Hu et al., 2021) `ev:measured` p. 6 ^hu2021lora-028
- In the restricted Houlsby-style setup, RoBERTa large with LoRA averaged 88.6 on GLUE, above AdapterP with 3.0M parameters at 88.4. (Hu et al., 2021) `ev:measured` p. 6 ^hu2021lora-029
- DeBERTa XXL with LoRA and 4.7M trainable parameters averaged 91.3 on GLUE, compared with 91.1 for full fine-tuning with 1500.0M. (Hu et al., 2021) `ev:measured` p. 6 ^hu2021lora-030
- On the E2E NLG Challenge, GPT-2 medium with LoRA and 0.35M parameters reached 70.4 BLEU, against 68.2 for full fine-tuning. (Hu et al., 2021) `ev:measured` p. 7 ^hu2021lora-031
- With the same 0.35M trainable parameters on E2E, GPT-2 medium with LoRA scored 70.4 BLEU versus 69.7 for prefix-layer tuning. (Hu et al., 2021) `ev:measured` p. 7 ^hu2021lora-032
- GPT-2 large with LoRA and 0.77M trainable parameters reached 70.4 BLEU on E2E, compared with 68.5 for full fine-tuning. (Hu et al., 2021) `ev:measured` p. 7 ^hu2021lora-033
- On DART, GPT-2 medium with LoRA and 0.35M trainable parameters reached 47.1 BLEU, above 46.2 for full fine-tuning. (Hu et al., 2021) `ev:measured` p. 21 ^hu2021lora-034
- On WebNLG, GPT-2 medium with LoRA reached 55.3 BLEU over all categories, compared with 46.5 for full fine-tuning. (Hu et al., 2021) `ev:measured` p. 22 ^hu2021lora-035
- On GPT-3 175B, LoRA with 4.7M trainable parameters reached 73.4 WikiSQL validation accuracy, close to 73.8 for full fine-tuning. (Hu et al., 2021) `ev:measured` p. 8 ^hu2021lora-036
- On MNLI-matched, GPT-3 with LoRA and 4.7M trainable parameters reached 91.7 validation accuracy, above 89.5 for full fine-tuning. (Hu et al., 2021) `ev:measured` p. 8 ^hu2021lora-037
- On SAMSum, GPT-3 with LoRA and 4.7M parameters reached Rouge scores of 53.8/29.8/45.9, above full fine-tuning at 52.0/28.0/44.5. (Hu et al., 2021) `ev:measured` p. 8 ^hu2021lora-038
- With 37.7M trainable parameters, GPT-3 with LoRA reached 74.0 WikiSQL validation accuracy, above the 73.8 of full fine-tuning. (Hu et al., 2021) `ev:measured` p. 8 ^hu2021lora-039
- On GPT-3 175B, LoRA matches or exceeds the fine-tuning baseline on all three datasets: WikiSQL, MNLI-matched and SAMSum. (Hu et al., 2021) `ev:measured` p. 8 ^hu2021lora-040
- Prefix-embedding tuning on GPT-3 175B showed a significant performance drop when using more than 256 special tokens. (Hu et al., 2021) `ev:measured` p. 8 ^hu2021lora-041
- Prefix-layer tuning on GPT-3 175B showed a significant performance drop when using more than 32 special tokens. (Hu et al., 2021) `ev:measured` p. 8 ^hu2021lora-042
- The authors suspect that more special tokens shift the input distribution further away from the pre-training data distribution. (Hu et al., 2021) `ev:asserted` p. 8 ^hu2021lora-043
- Under an 18M parameter budget on GPT-3, adapting both Wq and Wv reached 73.7 on WikiSQL, above Wq alone at 70.4. (Hu et al., 2021) `ev:measured` p. 10 ^hu2021lora-044
- The authors suggest even a rank of four captures enough information that adapting more weight matrices is preferable to one type with larger rank. (Hu et al., 2021) `ev:asserted` p. 10 ^hu2021lora-045
- Adapting Wq and Wv with rank r = 1 on GPT-3 reached 73.4 WikiSQL accuracy, versus 73.5 at r = 64. (Hu et al., 2021) `ev:measured` p. 10 ^hu2021lora-046
- Adapting Wq alone needed a larger rank, reaching 68.8 on WikiSQL at r = 1 versus 70.5 at r = 4. (Hu et al., 2021) `ev:measured` p. 10 ^hu2021lora-047
- The authors do not expect a small rank to work for every task, giving a downstream task in a different language as an example. (Hu et al., 2021) `ev:asserted` p. 10 ^hu2021lora-048
- The learned adaptation matrices with r = 8 and r = 64 share a subspace of dimension 1 with normalized similarity above 0.5. (Hu et al., 2021) `ev:measured` p. 11 ^hu2021lora-049
- The authors interpret the non-top singular directions of the learned adaptation matrices as potentially containing mostly random noise accumulated during training. (Hu et al., 2021) `ev:asserted` p. 11 ^hu2021lora-050
- Across two random seeds at r = 64, ΔWq appears to have a higher intrinsic rank than ΔWv, sharing more common singular directions. (Hu et al., 2021) `ev:measured` p. 11 ^hu2021lora-051
- In the 48th layer of GPT-3, ΔW has a stronger correlation with W than a random matrix, indicating it amplifies features already in W. (Hu et al., 2021) `ev:measured` p. 12 ^hu2021lora-052
- Instead of repeating the top singular directions of W, ΔW only amplifies directions that are not emphasized in W. (Hu et al., 2021) `ev:measured` p. 12 ^hu2021lora-053
- The amplification factor for r = 4 is about 21.5, obtained as 6.91 divided by 0.32 from Frobenius norms. (Hu et al., 2021) `ev:computed` p. 12 ^hu2021lora-054
- For r = 64 the amplification factor is only around 2, which the authors take as evidence of a low intrinsic adaptation rank. (Hu et al., 2021) `ev:computed` p. 25 ^hu2021lora-055
- The authors suggest the low-rank adaptation matrix potentially amplifies task-specific features learned but not emphasized in the general pre-training model. (Hu et al., 2021) `ev:asserted` p. 12 ^hu2021lora-056
- On WikiSQL, combining LoRA with prefix-embedding tuning significantly outperforms both methods alone, which indicates that LoRA is somewhat orthogonal to prefix-embedding tuning. (Hu et al., 2021) `ev:measured` p. 21 ^hu2021lora-057
- LoRA combined with prefix-layer tuning performs slightly worse than LoRA alone, even with more trainable parameters. (Hu et al., 2021) `ev:measured` p. 21 ^hu2021lora-058
- In the GPT-3 hyperparameter sweep, prefix-based methods perform worse as trainable parameters increase, while the performance of LoRA stabilizes. (Hu et al., 2021) `ev:measured` p. 23 ^hu2021lora-059
- On the low-data MNLI-100 subset, GPT-3 with LoRA reached 63.8 validation accuracy, above 60.2 for full fine-tuning. (Hu et al., 2021) `ev:measured` p. 23 ^hu2021lora-060
- Prefix-embedding tuning on MNLI-100 performed only slightly better than random chance, at 37.6% versus 33.3%. (Hu et al., 2021) `ev:measured` p. 22 ^hu2021lora-061
- On GPT-2 medium with E2E, LoRA performance peaks at r = 16 for validation loss and at r = 4 for BLEU. (Hu et al., 2021) `ev:measured` p. 26 ^hu2021lora-062
- On GPT-3 175B, full fine-tuning reached 89.5 MNLI-matched validation accuracy, against 40.6 for few-shot learning with in-context examples. (Hu et al., 2021) `ev:measured` p. 17 ^hu2021lora-063
- To the authors' knowledge, no prior low-rank work considers a low-rank update to a frozen model for adaptation to downstream tasks. (Hu et al., 2021) `ev:asserted` p. 9 ^hu2021lora-064
- The authors describe the key difference from adapters as LoRA's learned weights being mergeable with the main weights during inference. (Hu et al., 2021) `ev:asserted` p. 9 ^hu2021lora-065
- The authors state that the proposed principles are generally applicable to any neural networks with dense layers, beyond Transformer language models. (Hu et al., 2021) `ev:asserted` p. 12 ^hu2021lora-066
- The authors note that they mostly depend on heuristics to select the weight matrices to apply LoRA to. (Hu et al., 2021) `ev:asserted` p. 13 ^hu2021lora-067
- The authors note that the relationship between model size and the optimal rank for adaptation is still an open question. (Hu et al., 2021) `ev:asserted` p. 24 ^hu2021lora-068

## 🎯 Contributions

## 📖 Glossary

- **LoRA** — Low-Rank Adaptation: frozen pre-trained weights plus a trainable low-rank update BA.
- **Rank r** — Inner dimension of the LoRA factors B and A, much smaller than layer width.
- **Intrinsic rank** — Hypothesized low effective rank of the weight change during adaptation.
- **Adapter layer** — Small bottleneck module inserted sequentially into each Transformer block.
- **Prefix-embedding tuning** — Training embeddings of special tokens prepended or inserted into the prompt.
- **Prefix-layer tuning** — Training activations of special tokens after every Transformer layer.
- **BitFit** — Baseline training only the bias vectors of a pre-trained model.
- **Amplification factor** — Ratio of norm of ΔW to norm of W projected onto ΔW's subspace.
- **Normalized subspace similarity** — Grassmann-based measure in [0, 1] of overlap between two singular subspaces.

## ❓ Open questions

- Does a small rank remain sufficient for tasks far from the pre-training distribution, such as a different language?
- Is there a principled way to choose which weight matrices receive LoRA instead of heuristics?
- How do adapting MLP layers, LayerNorm layers and biases with LoRA affect quality and efficiency?
- How does the optimal adaptation rank scale with model size?
- Does the rank-deficiency of ΔW imply that the pre-trained W itself is rank-deficient?
- How are features learned in pre-training transformed to perform well on downstream tasks?
- Can LoRA be combined with tensor-product parametrizations such as COMPACTER to improve parameter efficiency further?

## 📝 Notes on reading

Version read: arXiv v2 (16 Oct 2021), which adds better baselines, GLUE experiments and more on adapter latency compared with v1.

Figures described only: Figure 1 (reparametrization diagram), Figure 2 (GPT-3 validation accuracy vs log trainable parameters on WikiSQL and MNLI-m), Figures 3, 4, 6, 7 (subspace-similarity heat maps between A matrices across ranks, seeds and layers 1/32/48/64/96), Figure 5 (adapter latency slow-down grid), Figure 8 (similarity between singular directions of Wq and ΔWq). Heat-map values were not extracted.

Inconsistencies inside the paper: Section 5 says NVIDIA Tesla V100 was used for all experiments, while the latency study (Table 1, Appendix B) uses an NVIDIA Quadro RTX8000. Section 7.3 gives the r = 4 amplification factor as 21.5, while Appendix H.4 describes it as about 20. Section 7.2 lists {Wq, Wk, Wv, Wc}, apparently a typo for Wo. Table 2 contains two RoBERTa large LoRA rows (89.0 and 88.6†); the † run uses the restricted Houlsby setup. Appendix D.1 says LoRA modules for MRPC, RTE and STS-B were initialized from the best MNLI checkpoint, but also that the restricted † runs start from pre-trained RoBERTa large.

The WikiSQL and SAMSum example counts in Appendix C are printed with broken spacing (56, 355/8, 421 and 14, 732/819) and were not claimed. The abstract's 3 times GPU memory reduction corresponds in the body to VRAM falling from 1.2TB to 350GB (up to 2/3 reduction).

## Suggested new concepts

- Low-rank adaptation — a core parameter-efficient fine-tuning method reused widely across model families.
- Parameter-efficient fine-tuning — umbrella for adapters, prefix tuning, BitFit and LoRA compared here.
- Intrinsic dimension of fine-tuning — hypothesis behind LoRA that adaptation lives in a low-dimensional subspace.
- Adapter layers — sequential bottleneck modules whose inference latency motivates LoRA's mergeable design.
- Prefix tuning — prompt-based adaptation baseline with non-monotonic scaling in trainable parameters.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Adaptación de bajo rango (D.3).

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
