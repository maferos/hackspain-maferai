---
aliases: []
type: "source"
title: "SOAP: Improving and Stabilizing Shampoo using Adam"
citekey: "Vyas2024soap"
doi: "10.48550/arXiv.2409.11321"
arxiv: "2409.11321"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2409.11321"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Nikhil Vyas", "Depen Morwani", "Rosie Zhao", "Mujin Kwun", "Itai Shapira", "David Brandfonbrener", "Lucas Janson", "Sham Kakade"]
sha256: ["d6f33bb71eab0f046d911b60800846fd3332f1dcf5f2f1434ab444ab89d0b22a"]
pdf: "Content/Papers/Vyas2024soap.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Vyas2024soap.pdf]]

> [!abstract] One-sentence summary
> The paper shows that Shampoo with power 1/2 equals Adafactor run in Shampoo's eigenbasis, and uses this to build SOAP, an optimizer running Adam in that slowly updated eigenbasis that trains 360m and 660m language models in fewer steps and less wall-clock time than AdamW and Shampoo.

## Abstract

There is growing evidence of the effectiveness of Shampoo, a higher-order preconditioning method, over Adam in deep learning optimization tasks. However, Shampoo's drawbacks include additional hyperparameters and computational overhead when compared to Adam, which only updates running averages of first- and second-moment quantities. This work establishes a formal connection between Shampoo (implemented with the 1/2 power) and Adafactor -- a memory-efficient approximation of Adam -- showing that Shampoo is equivalent to running Adafactor in the eigenbasis of Shampoo's preconditioner. This insight leads to the design of a simpler and computationally efficient algorithm: $\textbf{S}$hampo$\textbf{O}$ with $\textbf{A}$dam in the $\textbf{P}$reconditioner's eigenbasis (SOAP). With regards to improving Shampoo's computational efficiency, the most straightforward approach would be to simply compute Shampoo's eigendecomposition less frequently. Unfortunately, as our empirical results show, this leads to performance degradation that worsens with this frequency. SOAP mitigates this degradation by continually updating the running average of the second moment, just as Adam does, but in the current (slowly changing) coordinate basis. Furthermore, since SOAP is equivalent to running Adam in a rotated space, it introduces only one additional hyperparameter (the preconditioning frequency) compared to Adam. We empirically evaluate SOAP on language model pre-training with 360m and 660m sized models. In the large batch regime, SOAP reduces the number of iterations by over 40% and wall clock time by over 35% compared to AdamW, with approximately 20% improvements in both metrics compared to Shampoo. An implementation of SOAP is available at https://github.com/nikhilvyas/SOAP. (arXiv)

## 🧠 Key ideas (atomic)

- Shampoo outperformed all other submissions in the AlgoPerf benchmark, including Adam, reducing wall-clock time by 28%. (Vyas et al., 2024) `ev:cited` p. 1 ^vyas2024soap-001
- Morwani et al. (2024) showed that Shampoo with minor modifications, such as power 1/2, is close to [[Kronecker-factored preconditioning|the optimal Kronecker approximation of Adagrad]]. (Vyas et al., 2024) `ev:cited` p. 1 ^vyas2024soap-002
- Claim 1 proves that idealized Shampoo with power 1/2 is equivalent to idealized Adafactor run in Shampoo's eigenspace. (Vyas et al., 2024) `ev:computed` p. 5 ^vyas2024soap-003
- The equivalence uses Shampoo with power 1/2 instead of power 1/4, as already recommended in practical implementations. (Vyas et al., 2024) `ev:reported` p. 4 ^vyas2024soap-004
- For the equivalence, the authors use dataset averages instead of running averages of L and R across time steps. (Vyas et al., 2024) `ev:reported` p. 4 ^vyas2024soap-005
- The equivalence also holds with momentum, although the authors omit momentum from the presentation for simplicity. (Vyas et al., 2024) `ev:asserted` p. 4 ^vyas2024soap-006
- In practice, the two idealized algorithms differ when running averages are used instead of dataset averages of L and R. (Vyas et al., 2024) `ev:asserted` p. 6 ^vyas2024soap-007
- The authors state that practical Shampoo's learning-rate adaptivity is limited to the updates of L and R. (Vyas et al., 2024) `ev:asserted` p. 6 ^vyas2024soap-008
- In Shampoo's eigenspace, Adafactor's second-moment estimates can be updated at every step because they are computationally inexpensive. (Vyas et al., 2024) `ev:asserted` p. 6 ^vyas2024soap-009
- Algorithm 3, SOAP, can be interpreted as running Adam in the eigenspace of [[Kronecker-factored preconditioning|Shampoo's preconditioner]]. (Vyas et al., 2024) `ev:asserted` p. 6 ^vyas2024soap-010
- Per layer, SOAP maintains four matrices: L of size m×m, R of size n×n, and V, M of size m×n. (Vyas et al., 2024) `ev:reported` p. 6 ^vyas2024soap-011
- SOAP's hyperparameters are the learning rate, two betas, epsilon, and a preconditioning frequency that sets how often eigenvectors are updated. (Vyas et al., 2024) `ev:reported` p. 6 ^vyas2024soap-012
- SOAP reduces the number of hyperparameters compared to Shampoo, leaving only one additional hyperparameter compared to AdamW: preconditioning frequency. (Vyas et al., 2024) `ev:asserted` p. 2 ^vyas2024soap-013
- Following Zhao et al. (2024a), SOAP runs standard AdamW for 1D layers, reducing overhead relative to standard Shampoo implementations. (Vyas et al., 2024) `ev:reported` p. 6 ^vyas2024soap-014
- Following Wang et al. (2024), SOAP computes eigenvectors of L and R using one power-method step followed by QR decomposition. (Vyas et al., 2024) `ev:reported` p. 6 ^vyas2024soap-015
- For the first iteration, SOAP initializes the eigenvectors with a standard eigenvector decomposition instead of the power-method step. (Vyas et al., 2024) `ev:reported` p. 6 ^vyas2024soap-016
- For layers with huge dimensions, such as the first and last transformer layers, SOAP fixes that rotation matrix to identity. (Vyas et al., 2024) `ev:reported` p. 7 ^vyas2024soap-017
- Fixing both rotation matrices of a 2D layer to identity recovers Adam, according to the authors. (Vyas et al., 2024) `ev:asserted` p. 7 ^vyas2024soap-018
- Hyperparameter tuning began with a learning-rate sweep, followed by two-dimensional sweeps pairing each remaining hyperparameter with the learning rate. (Vyas et al., 2024) `ev:reported` p. 7 ^vyas2024soap-019
- Throughput was measured as tokens processed per second on a single H100 GPU, using gradient accumulation for large batch sizes. (Vyas et al., 2024) `ev:reported` p. 7 ^vyas2024soap-020
- To estimate efficiency benefits, SOAP was run on .5, .625, .75 and .875 fractions of the training data. (Vyas et al., 2024) `ev:reported` p. 7 ^vyas2024soap-021
- A scaling law in the number of training points was fit through these final losses to compute efficiency benefits. (Vyas et al., 2024) `ev:reported` p. 7 ^vyas2024soap-022
- On 360m and 660m models at 2m token batch size with chinchilla-optimal token counts, SOAP outperforms AdamW and Shampoo in train loss. (Vyas et al., 2024) `ev:measured` p. 7 ^vyas2024soap-023
- With 2m batch size and preconditioning frequency 10, SOAP reduced the number of iterations by ≥40% compared to AdamW. (Vyas et al., 2024) `ev:measured` p. 7 ^vyas2024soap-024
- With 2m batch size and preconditioning frequency 10, SOAP reduced wall clock time by ≥35% compared to AdamW. (Vyas et al., 2024) `ev:measured` p. 7 ^vyas2024soap-025
- At 2m batch size, SOAP gave a ≈20% reduction in both iterations and wall clock time compared to Shampoo. (Vyas et al., 2024) `ev:measured` p. 7 ^vyas2024soap-026
- Models are trained on the C4 dataset tokenized with the T5 tokenizer, following the setup of Zhao et al. (2024c). (Vyas et al., 2024) `ev:reported` p. 18 ^vyas2024soap-027
- Decoder-only transformer models with 210m, 360m and 660m non-embedding parameters were trained, starting from the OLMo codebase. (Vyas et al., 2024) `ev:reported` p. 18 ^vyas2024soap-028
- By default, models are trained for approximately 20 times their number of parameters in tokens, the chinchilla-optimal count. (Vyas et al., 2024) `ev:reported` p. 18 ^vyas2024soap-029
- The default β1 is 0.95, which outperformed β1 = 0.9 in the authors' sweeps for the 360m model. (Vyas et al., 2024) `ev:measured` p. 18 ^vyas2024soap-030
- Shampoo baselines use the DistributedShampoo implementation of Shi et al. (2023), which exposes grafting and exponent variations as hyperparameters. (Vyas et al., 2024) `ev:reported` p. 3 ^vyas2024soap-031
- The default DistributedShampoo exponent was set to −1/2.5 for both 1D and 2D parameters, based on preliminary findings. (Vyas et al., 2024) `ev:reported` p. 19 ^vyas2024soap-032
- Additional DistributedShampoo sweeps over epsilon, beta and exponents gave no significant improvement, below .004, for the 360m model. (Vyas et al., 2024) `ev:measured` p. 19 ^vyas2024soap-033
- The paper finds that for all preconditioning frequencies tried from 1 to 100, both SOAP and Shampoo outperform AdamW. (Vyas et al., 2024) `ev:measured` p. 8 ^vyas2024soap-034
- At preconditioning frequency 1, SOAP and Shampoo are quite close in performance in the frequency ablation. (Vyas et al., 2024) `ev:measured` p. 8 ^vyas2024soap-035
- As preconditioning frequency increases, SOAP's performance degrades significantly slower than Shampoo's in the frequency ablation. (Vyas et al., 2024) `ev:measured` p. 8 ^vyas2024soap-036
- When batch size is decreased by a factor k, preconditioning frequency is increased by the same factor to keep overhead consistent. (Vyas et al., 2024) `ev:reported` p. 9 ^vyas2024soap-037
- A 360m model trained with AdamW at 256k batch size for Chinchilla-optimal tokens reached a loss of 2.842, the target loss. (Vyas et al., 2024) `ev:measured` p. 9 ^vyas2024soap-038
- SOAP consistently requires fewer steps than AdamW to reach the target loss across all batch sizes in the comparison. (Vyas et al., 2024) `ev:measured` p. 9 ^vyas2024soap-039
- The multiplicative benefit of SOAP over AdamW in steps becomes more pronounced at larger batch sizes. (Vyas et al., 2024) `ev:measured` p. 9 ^vyas2024soap-040
- SOAP follows the linear batch-size scaling trend more closely than AdamW, indicating a higher critical batch size in this setup. (Vyas et al., 2024) `ev:measured` p. 9 ^vyas2024soap-041
- At 256k batch size, SOAP reduced the number of iterations by 25% compared to AdamW. (Vyas et al., 2024) `ev:measured` p. 9 ^vyas2024soap-042
- At 256k batch size, SOAP reduced the number of iterations by approximately 10% compared to Shampoo. (Vyas et al., 2024) `ev:measured` p. 9 ^vyas2024soap-043
- At 256k batch size, SOAP achieved a wall-clock time improvement of ≥15% over AdamW for the 360m model. (Vyas et al., 2024) `ev:measured` p. 9 ^vyas2024soap-044
- The 256k batch-size comparison used a preconditioning frequency of 80 for both Shampoo and SOAP. (Vyas et al., 2024) `ev:reported` p. 10 ^vyas2024soap-045
- The authors call the smaller-batch results preliminary, noting that keeping batch size times preconditioning frequency constant may not be optimal. (Vyas et al., 2024) `ev:asserted` p. 9 ^vyas2024soap-046
- SOAP's overhead could potentially be reduced by performing L and R updates in lower precision instead of fp32. (Vyas et al., 2024) `ev:asserted` p. 9 ^vyas2024soap-047
- The authors state that diminished efficiency gains of second-order methods at smaller batch sizes are consistent with prior findings. (Vyas et al., 2024) `ev:cited` p. 9 ^vyas2024soap-048
- SOAP maintains its advantage over Adam even in extended training runs beyond Chinchilla-optimal token counts. (Vyas et al., 2024) `ev:measured` p. 10 ^vyas2024soap-049
- The extended-run comparison trains a 360m model at 2m batch size on 33.5b tokens, or 100x model size. (Vyas et al., 2024) `ev:reported` p. 11 ^vyas2024soap-050
- The one-sided eigenbasis variant of SOAP results in slightly reduced performance compared to the original SOAP optimizer. (Vyas et al., 2024) `ev:measured` p. 10 ^vyas2024soap-051
- The one-sided SOAP variant still performs on par with, or marginally better than, Shampoo in the reported experiments. (Vyas et al., 2024) `ev:measured` p. 10 ^vyas2024soap-052
- SOAP's space usage for a layer equals that of DistributedShampoo, covering L, QL, R, QR, momentum, second moment and gradient. (Vyas et al., 2024) `ev:computed` p. 11 ^vyas2024soap-053
- Using Adafactor instead of Adam as the diagonal preconditioner reduces SOAP's space usage by mn. (Vyas et al., 2024) `ev:computed` p. 11 ^vyas2024soap-054
- For standard transformer architectures, combining the factorized and one-sided variants would yield less space usage overall than AdamW. (Vyas et al., 2024) `ev:computed` p. 11 ^vyas2024soap-055
- Using Adafactor instead of AdamW inside SOAP yields very small reductions in performance in the language modeling experiments. (Vyas et al., 2024) `ev:measured` p. 11 ^vyas2024soap-056
- Even with both space-saving changes combined, the resulting optimizer outperforms AdamW with a smaller space requirement than AdamW. (Vyas et al., 2024) `ev:measured` p. 12 ^vyas2024soap-057
- The authors compute that SOAP's per-step overhead for an m × n layer is more than Shampoo's per-step overhead. (Vyas et al., 2024) `ev:computed` p. 12 ^vyas2024soap-058
- The power-iteration approach using torch.linalg.qr performs as well as fresh eigenvector decomposition with torch.linalg.eigh in the authors' experiments. (Vyas et al., 2024) `ev:measured` p. 12 ^vyas2024soap-059
- SOAP's overhead over AdamW decreases as the preconditioning frequency increases, that is, as Algorithm 4 is invoked less often. (Vyas et al., 2024) `ev:measured` p. 12 ^vyas2024soap-060
- Empirically, SOAP's overhead approaches an asymptote greater than zero instead of vanishing as preconditioning frequency grows. (Vyas et al., 2024) `ev:measured` p. 13 ^vyas2024soap-061
- The authors attribute this nonzero asymptote to additional per-layer matrix multiplications for updating L, updating R, projecting and reprojecting the gradient. (Vyas et al., 2024) `ev:asserted` p. 13 ^vyas2024soap-062
- Low precision cannot reduce the preconditioner-update overhead in PyTorch because torch.linalg.qr does not support precision lower than float32. (Vyas et al., 2024) `ev:asserted` p. 13 ^vyas2024soap-063
- Anil et al. (2020) described an algorithm essentially equivalent to SOAP for 2D layers, but provided no experiments for it. (Vyas et al., 2024) `ev:cited` p. 3 ^vyas2024soap-064
- The authors suggest that the discrepancy with the unpublished negative results of Anil et al. may be due to SOAP's implementation details. (Vyas et al., 2024) `ev:asserted` p. 3 ^vyas2024soap-065
- Unlike GaLore, SOAP maintains an exponential moving average of GGᵀ and GᵀG instead of using the SVD of the current gradient. (Vyas et al., 2024) `ev:asserted` p. 4 ^vyas2024soap-066
- On the 210m model, the best GaLore run reached a final loss of 3.12, versus 3.10 for the best Shampoo run. (Vyas et al., 2024) `ev:measured` p. 20 ^vyas2024soap-067
- The study focuses on a relatively small scale compared to recent LLMs, which are two orders of magnitude bigger. (Vyas et al., 2024) `ev:asserted` p. 14 ^vyas2024soap-068
- The authors hypothesize that SOAP's findings would generalize to larger scales due to its theoretical foundation, a hypothesis still to be validated. (Vyas et al., 2024) `ev:asserted` p. 14 ^vyas2024soap-069

## 🎯 Contributions

## 📖 Glossary

- **Shampoo** — Second-order optimizer with left and right Kronecker-factored preconditioners per weight matrix.
- **Adafactor** — Adam variant replacing the second-moment matrix with its best rank-1 approximation.
- **SOAP** — ShampoO with Adam in the Preconditioner's eigenbasis: AdamW run in Shampoo's rotated space.
- **Preconditioning frequency** — Number of steps between recomputations of the preconditioner or its eigenbasis.
- **Critical batch size** — Batch size beyond which doubling it no longer halves the required steps.
- **One-sided SOAP** — Variant rotating only the smaller side of a layer, identity on the larger.
- **Power iteration with QR** — One matrix multiplication plus QR decomposition to refresh estimated eigenvectors.
- **Grafting** — Borrowing a per-layer update magnitude from another optimizer such as Adam.

## ❓ Open questions

- Do SOAP's gains over AdamW and Shampoo hold at model scales two orders of magnitude larger than 660m?
- How does SOAP perform in other domains, such as vision?
- What trade-off between batch size and preconditioning frequency is optimal at small batch sizes?
- How much would lower-precision (below fp32) storage and updates of L, R, QL, QR reduce SOAP's overhead without hurting loss?
- How does SOAP compare with distributed or scalability-oriented Shampoo variants (Anil et al., Wang et al., Lin et al.) under a proper multi-GPU implementation?
- Can one-sided or factorized variants match full SOAP's loss at lower compute?

## 📝 Notes on reading

Version read: arXiv 2409.11321v2 (31 Jan 2025), matching the packet identifier.

Figures described, not claimed: Figure 1 (p. 3) shows train-loss curves for the 660m model versus steps and scaled wall time, plus the frequency ablation (final test loss versus preconditioning frequency 1 to 100) on the 360m model. Figure 2 (p. 8) shows the scaling-law fits used for the precise efficiency numbers; axis tick labels (e.g. 0.52, 0.565, 0.62, 0.72, 0.83, 1.06, 1.11, 1.12) seem to mark SOAP's matched-loss points but the extraction does not say so. Figure 4 left (p. 10) shows estimated steps to loss 2.842 versus batch size (256 to 2048, in thousands of tokens). Figure 7 left (p. 13) shows percent overhead over AdamW versus preconditioning frequency on a log scale.

Space and time complexity formulas on pp. 11-13 (e.g. 2m² + 2n² + 3mn space; m³ + n³ + 2m²n + 2mn² per-step overhead) lost their superscripts in extraction; they were paraphrased rather than quoted.

Minor inconsistencies: the Section 6.3 text gives a 25% iteration reduction at 256k, while the Figure 4 caption says ≥25%. Sections 8 and 9 repeat the same opening paragraph. Appendix A writes "256 batch size" where 256k is meant. The abstract says "over 40%" and "over 35%", the body says ≥40% and ≥35%. Section 6.4 text reads "maintains its advantage Adam" (missing word).

## Suggested new concepts

- Eigenbasis preconditioning — running a first-order optimizer in the eigenbasis of a second-order preconditioner links SOAP, E-KFAC and GaLore.
- Critical batch size — the paper uses it as a metric for optimizer quality; recurrent across optimizer papers.
- Kronecker-factored preconditioning — shared structure of Shampoo and KFAC, worth one hub note.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H4.** Demuestra que Shampoo equivale a Adafactor en la base propia del precondicionador y propone correr Adam en esa base, heredero práctico de Shampoo y K-FAC.
