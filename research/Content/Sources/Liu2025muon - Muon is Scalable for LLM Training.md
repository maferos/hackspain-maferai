---
aliases: []
type: "source"
title: "Muon is Scalable for LLM Training"
citekey: "Liu2025muon"
doi: "10.48550/arXiv.2502.16982"
arxiv: "2502.16982"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2502.16982"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Jingyuan Liu", "Jianlin Su", "Xingcheng Yao", "Zhejun Jiang", "Guokun Lai", "Yulun Du", "Yidao Qin", "Weixin Xu", "Enzhe Lu", "Junjie Yan", "Yanru Chen", "Huabin Zheng", "Yibo Liu", "Shaowei Liu", "Bohong Yin", "Weiran He", "Han Zhu", "Yuzhi Wang", "Jianzhou Wang", "Mengnan Dong", "Zheng Zhang", "Yongsheng Kang", "Hao Zhang", "Xinran Xu", "Yutao Zhang", "Yuxin Wu", "Xinyu Zhou", "Zhilin Yang"]
sha256: ["6b8e3b47da4db09c952a35486c905f416c57081a32b445a36a3744c441b1c7f3"]
pdf: "Content/Papers/Liu2025muon.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 59
---

📄 PDF: [[Liu2025muon.pdf]]

> [!abstract] One-sentence summary
> The paper scales the Muon optimizer to a 16B-parameter MoE model by adding weight decay and shape-aware update RMS scaling, reporting roughly half the training FLOPs of AdamW for equal loss.

## Abstract

Recently, the Muon optimizer based on matrix orthogonalization has demonstrated strong results in training small-scale language models, but the scalability to larger models has not been proven. We identify two crucial techniques for scaling up Muon: (1) adding weight decay and (2) carefully adjusting the per-parameter update scale. These techniques allow Muon to work out-of-the-box on large-scale training without the need of hyper-parameter tuning. Scaling law experiments indicate that Muon achieves $\sim\!2\times$ computational efficiency compared to AdamW with compute optimal training. Based on these improvements, we introduce Moonlight, a 3B/16B-parameter Mixture-of-Expert (MoE) model trained with 5.7T tokens using Muon. Our model improves the current Pareto frontier, achieving better performance with much fewer training FLOPs compared to prior models. We open-source our distributed Muon implementation that is memory optimal and communication efficient. We also release the pretrained, instruction-tuned, and intermediate checkpoints to support future research. (arXiv)

## 🧠 Key ideas (atomic)

- Muon, proposed by Jordan et al. in 2024, updates matrix parameters with orthogonalized gradient momentum computed through [[Newton-Schulz orthogonalization|Newton-Schulz iteration]]. (Liu et al., 2025) `ev:cited` p. 2 ^liu2025muon-001
- [[Newton-Schulz orthogonalization|A Newton-Schulz iteration]] approximately replaces the momentum matrix with its orthogonal factor from the singular value decomposition, orthogonalizing the update. (Liu et al., 2025) `ev:reported` p. 2 ^liu2025muon-002
- The authors keep the original [[Newton-Schulz orthogonalization|Newton-Schulz coefficients]] a = 3.4445, b = −4.7750, c = 2.0315, which speed convergence for small initial singular values. (Liu et al., 2025) `ev:reported` p. 3 ^liu2025muon-003
- Under the steepest-descent view, Muon offers a norm constraint that becomes the spectral norm when [[Newton-Schulz orthogonalization|the orthogonalization]] is computed exactly. (Liu et al., 2025) `ev:asserted` p. 3 ^liu2025muon-004
- The authors argue that Muon's norm constraint is more reasonable than Adam's, since weights act as operators on locally Euclidean spaces. (Liu et al., 2025) `ev:asserted` p. 3 ^liu2025muon-005
- The authors found that Muon's performance gains over AdamW diminish when scaling up to larger models trained on more tokens. (Liu et al., 2025) `ev:measured` p. 3 ^liu2025muon-006
- Without weight decay, Muon-trained weight RMS kept growing beyond the high-precision range of bf16, which might hurt model performance. (Liu et al., 2025) `ev:measured` p. 3 ^liu2025muon-007
- The authors introduced the standard AdamW weight decay mechanism into the Muon update rule, scaled by a weight decay ratio λ. (Liu et al., 2025) `ev:reported` p. 3 ^liu2025muon-008
- The weight decay ablation trained an 800M-parameter model on 100B tokens, about five times the optimal training token count. (Liu et al., 2025) `ev:reported` p. 3 ^liu2025muon-009
- In the 800M-parameter run, vanilla Muon without weight decay initially converged faster than Muon with weight decay. (Liu et al., 2025) `ev:measured` p. 3 ^liu2025muon-010
- Muon with weight decay outperformed both vanilla Muon and AdamW, reaching lower validation loss in the over-train regime. (Liu et al., 2025) `ev:measured` p. 3 ^liu2025muon-011
- Lemma 1 shows that a full-rank matrix parameter of shape [A, B] has a theoretical Muon update RMS of sqrt(1/max(A, B)). (Liu et al., 2025) `ev:computed` p. 3 ^liu2025muon-012
- When max(A, B) is large, as in dense MLP matrices, Muon updates become too small, limiting representational capacity. (Liu et al., 2025) `ev:asserted` p. 3 ^liu2025muon-013
- To keep update RMS consistent across matrix shapes, the authors scale each matrix's Muon update by the square root of max(A, B). (Liu et al., 2025) `ev:reported` p. 4 ^liu2025muon-014
- The authors observe empirically that AdamW's update RMS usually lies around 0.2 to 0.4 in practice. (Liu et al., 2025) `ev:measured` p. 4 ^liu2025muon-015
- With this RMS matching, Muon can directly reuse the learning rate and weight decay tuned for AdamW, according to the authors. (Liu et al., 2025) `ev:asserted` p. 4 ^liu2025muon-016
- Setting N to 10 yielded [[Newton-Schulz orthogonalization|a more accurate orthogonalization]] than N = 5, but did not lead to better performance. (Liu et al., 2025) `ev:measured` p. 4 ^liu2025muon-017
- The authors set momentum to 0.95, as in Jordan et al., after seeing no consistent gain from tuning it. (Liu et al., 2025) `ev:reported` p. 4 ^liu2025muon-018
- Vanilla ZeRO-1 is not directly applicable to Muon, because Muon requires the full gradient matrix to calculate updates. (Liu et al., 2025) `ev:asserted` p. 4 ^liu2025muon-019
- Distributed Muon partitions optimizer states over data parallel ranks, adding a DP gather of gradients to reconstruct full matrices. (Liu et al., 2025) `ev:reported` p. 5 ^liu2025muon-020
- Each rank runs [[Newton-Schulz orthogonalization|Newton-Schulz]] on the full gathered matrix, then discards the update except the partition matching its local parameters. (Liu et al., 2025) `ev:reported` p. 5 ^liu2025muon-021
- Muon keeps one momentum buffer versus two for AdamW, so its additional optimizer memory is half that of Distributed AdamW. (Liu et al., 2025) `ev:asserted` p. 5 ^liu2025muon-022
- The communication workload of Distributed Muon is between 1 and 1.25 times that of Distributed AdamW, by the authors' calculation. (Liu et al., 2025) `ev:computed` p. 5 ^liu2025muon-023
- The optimizer's end-to-end latency is usually 1% to 3% of the model's forward-backward pass time, which the authors call negligible. (Liu et al., 2025) `ev:asserted` p. 5 ^liu2025muon-024
- In the authors' large-scale cluster training, Distributed Muon showed no noticeable latency overhead compared with its AdamW counterparts. (Liu et al., 2025) `ev:measured` p. 5 ^liu2025muon-025
- Both Update Norm and Adjusted LR reached a validation loss of 2.789, lower than the Baseline value of 2.812. (Liu et al., 2025) `ev:measured` p. 6 ^liu2025muon-026
- The authors chose Adjusted LR for later experiments because it has lower cost than the Update Norm method. (Liu et al., 2025) `ev:asserted` p. 6 ^liu2025muon-027
- Among tested Muon update RMS settings, 0.2 and 0.4 performed similarly and much better than 0.05, 0.1 and 0.8. (Liu et al., 2025) `ev:measured` p. 14 ^liu2025muon-028
- With update RMS 0.2, Muon reached 3.325 validation loss after 2k steps, against 3.679 for the AdamW baseline. (Liu et al., 2025) `ev:measured` p. 14 ^liu2025muon-029
- The authors grid-searched AdamW hyper-parameters under a compute-optimal setup to build a strong baseline for the scaling comparison. (Liu et al., 2025) `ev:reported` p. 6 ^liu2025muon-030
- Muon directly reused the hyper-parameters optimal for the AdamW baseline, since its update RMS had been matched to AdamW. (Liu et al., 2025) `ev:reported` p. 6 ^liu2025muon-031
- Muon requires only about 52% of the training FLOPs to match AdamW performance under the compute-optimal setting. (Liu et al., 2025) `ev:measured` p. 6 ^liu2025muon-032
- The fitted scaling laws give an LM loss of 2.506 × C−0.052 for Muon, versus 2.608 × C−0.054 for AdamW. (Liu et al., 2025) `ev:computed` p. 7 ^liu2025muon-033
- Moonlight follows the DeepSeek-V3-Small architecture with 2.24B activated and 15.29B total parameters, excluding embedding parameters. (Liu et al., 2025) `ev:reported` p. 7 ^liu2025muon-034
- The final cooldown stage from 5.2T to 5.7T tokens used the highest quality data, focusing on math, code, and reasoning. (Liu et al., 2025) `ev:reported` p. 8 ^liu2025muon-035
- The authors omit multi-token prediction layers from Moonlight, noting that MTP showed no significant pretraining benefit in their experiments. (Liu et al., 2025) `ev:reported` p. 15 ^liu2025muon-036
- At 1.2T tokens, Moonlight reached 37.2 on HumanEval versus 29.3 for Moonlight-A with the same architecture. (Liu et al., 2025) `ev:measured` p. 8 ^liu2025muon-037
- Moonlight-A scored 45.3 on BBH at 1.2T tokens, above the 43.2 scored by the Muon-trained Moonlight checkpoint. (Liu et al., 2025) `ev:measured` p. 8 ^liu2025muon-038
- The authors observed that Muon especially excels on math and code tasks, inviting further investigation of this phenomenon. (Liu et al., 2025) `ev:asserted` p. 8 ^liu2025muon-039
- Fully trained on 5.7T tokens, Moonlight scored 70.0 on MMLU versus 58.3 for DeepSeek-V2-Lite on equal tokens. (Liu et al., 2025) `ev:measured` p. 9 ^liu2025muon-040
- On GSM8K, fully trained Moonlight scored 77.4, below the 79.1 of Qwen2.5-3B trained on 18T tokens. (Liu et al., 2025) `ev:measured` p. 9 ^liu2025muon-041
- Moonlight lies on the Pareto frontier of model performance versus training budget, outperforming many other models across various sizes. (Liu et al., 2025) `ev:measured` p. 9 ^liu2025muon-042
- The SVD entropy gap is more significant in router weights, which the authors take to indicate MoE models benefit more from Muon. (Liu et al., 2025) `ev:measured` p. 9 ^liu2025muon-043
- For over 90% of weight matrices at the 1.2T checkpoint, Muon-optimized matrices had higher SVD entropy than AdamW-optimized ones. (Liu et al., 2025) `ev:measured` p. 9 ^liu2025muon-044
- For most weight matrices, Muon produced flatter singular value distributions than AdamW, which the authors read as more diverse updates. (Liu et al., 2025) `ev:measured` p. 16 ^liu2025muon-045
- The 1.2T checkpoints of Moonlight and Moonlight-A were finetuned for two epochs on the tulu-3-sft-mixture dataset. (Liu et al., 2025) `ev:reported` p. 10 ^liu2025muon-046
- A model both pretrained and finetuned with Muon outperformed the other optimizer combinations in the SFT ablation studies. (Liu et al., 2025) `ev:measured` p. 9 ^liu2025muon-047
- Muon pretraining with Muon finetuning scored 68.0 on GSM8K, versus 64.6 when both stages used AdamW. (Liu et al., 2025) `ev:measured` p. 10 ^liu2025muon-048
- When the SFT optimizer differed from the pretraining optimizer, SFT with Muon showed no significant advantage over AdamW. (Liu et al., 2025) `ev:measured` p. 9 ^liu2025muon-049
- After supervised finetuning with Muon, Qwen2.5-7B scored 85.8 on GSM8K, below the 89.8 reached with Adam finetuning. (Liu et al., 2025) `ev:measured` p. 10 ^liu2025muon-050
- The authors conclude that applying Muon during pretraining is more effective than applying it during supervised finetuning. (Liu et al., 2025) `ev:asserted` p. 10 ^liu2025muon-051
- Moonlight training showed no loss spikes or gradient norm spikes, according to the training curves in Figure 7. (Liu et al., 2025) `ev:measured` p. 15 ^liu2025muon-052
- The maximum attention logit exceeded 100 in specific layers during the initial training phase of Moonlight. (Liu et al., 2025) `ev:measured` p. 16 ^liu2025muon-053
- The proportion of attention logits exceeding 100 stayed consistently low, about 10−4, indicating that extremely large logits were sparse. (Liu et al., 2025) `ev:measured` p. 16 ^liu2025muon-054
- Applying weight decay to the RMSNorm gamma parameter is crucial for training stability, preventing excessively high per-layer output RMS. (Liu et al., 2025) `ev:asserted` p. 16 ^liu2025muon-055
- The authors conclude that Muon can effectively replace AdamW as the standard optimizer for large-scale LLM training. (Liu et al., 2025) `ev:asserted` p. 11 ^liu2025muon-056
- Muon is currently used together with Adam, which still optimizes certain parameters, a hybrid the authors see as improvable. (Liu et al., 2025) `ev:asserted` p. 11 ^liu2025muon-057
- The authors propose extending Muon from the spectral norm to general Schatten norms as a promising research direction. (Liu et al., 2025) `ev:asserted` p. 11 ^liu2025muon-058
- Optimizer mismatch between pretraining and finetuning is a barrier to leveraging existing AdamW-pretrained checkpoints, according to the authors. (Liu et al., 2025) `ev:asserted` p. 11 ^liu2025muon-059

## 🎯 Contributions

## 📖 Glossary

- **Muon** — Optimizer that orthogonalizes gradient momentum of matrix parameters before applying the update.
- **Newton-Schulz iteration** — Polynomial iteration that approximates a matrix's orthogonal factor without computing an SVD.
- **Update RMS** — Root-mean-square magnitude of the per-step parameter update.
- **ZeRO-1** — Distributed training scheme that partitions optimizer states across data-parallel ranks.
- **SVD entropy** — Normalized entropy of squared singular values, measuring how spread a matrix's spectrum is.
- **Moonlight** — The authors' 3B-activated/16B-total MoE model pretrained with Muon on 5.7T tokens.
- **Compute-optimal training** — Choosing model size and token count to minimise loss for a fixed FLOP budget.

## ❓ Open questions

- Can all parameters, including embeddings, LM head and norms, be optimized by Muon without an Adam companion?
- Would extending Muon to general Schatten norms improve on the spectral-norm formulation?
- What mechanism causes the pretraining-finetuning optimizer mismatch, and how can AdamW-pretrained checkpoints benefit from Muon SFT?
- Why does Muon especially help math and code benchmarks?
- Does the ~2x efficiency hold beyond the 1.5B-parameter dense scaling-law range and for MoE models directly?
- How does the upward trend in maximum attention logits under Muon interact with stability at larger scales?

## 📝 Notes on reading

- Version read: arXiv 2502.16982v1 (technical report, 24 Feb 2025), matching the packet identifier.
- The ~2x efficiency headline (abstract, Fig. 1a caption) corresponds to the body's about 52% of training FLOPs; the Fig. 1a plot label reads 0.519x FLOPs.
- Table 7 shows Muon-SFT below Adam-SFT on all four benchmarks for Qwen2.5-7B (e.g. GSM8K 85.8 vs 89.8), yet the text calls performance on par.
- Equations 4, 5 and 7 and Lemma 1 contain square roots that are garbled in the extraction (the sqrt sign appears as a stray p); claims restate them in words.
- Figures 2, 3, 4, 7, 9 and 10 are plots; only values printed as annotations or in captions were used. Fig. 2 annotates vanilla Muon leading by 0.023 at iteration 24000 and Muon with weight decay leading by 0.017 at iteration 66000.
- Scaling-law models span 399M to 1.5B non-embedding parameters (Table 2); the ~2x claim is extrapolated to Moonlight rather than fitted on MoE models.
- Appendix D states AdamW controls the maximum attention logit better than alternative optimizers, implying Muon shows higher max logits early in training; Fig. 7c is the evidence.
- Pretraining data is only referenced to the Kimi k1.5 report; no data details are given here.

## Suggested new concepts

- Muon optimizer — a matrix-orthogonalizing optimizer increasingly used as an AdamW alternative for LLM pretraining.
- Newton-Schulz orthogonalization — the core numerical routine behind Muon and related spectral optimizers.
- Update RMS matching — a transferable recipe for sharing learning rate and weight decay across optimizers.
- Steepest descent under norm constraints — a unifying lens for comparing Adam, Muon and Shampoo-like optimizers.
- Optimizer mismatch between pretraining and finetuning — a recurring practical issue for checkpoint reuse.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H4.** Escala Muon (descenso por gradiente ortogonalizado, norma espectral) con decaimiento de pesos y ajuste de escala, unas 2x más eficiente que AdamW.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
