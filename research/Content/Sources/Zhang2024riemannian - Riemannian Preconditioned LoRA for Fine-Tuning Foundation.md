---
aliases: []
type: "source"
title: "Riemannian Preconditioned LoRA for Fine-Tuning Foundation Models"
citekey: "Zhang2024riemannian"
doi: "10.48550/arXiv.2402.02347"
arxiv: "2402.02347"
year: 2024
publication_type: "preprint"
url: "https://arxiv.org/abs/2402.02347"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Fangzhao Zhang", "Mert Pilanci"]
sha256: ["919768cf41ad8130613619e69904914d30178339552bac0f0eb5dc5a0eaebfef"]
pdf: "Content/Papers/Zhang2024riemannian.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Zhang2024riemannian.pdf]]

> [!abstract] One-sentence summary
> The paper adds an r by r Riemannian preconditioner to LoRA gradient steps, giving stable feature learning with one learning rate and better, more learning-rate-robust fine-tuning of language and diffusion models at negligible cost.

## Abstract

Low-Rank Adaptation (LoRA) emerges as a popular parameter-efficient fine-tuning (PEFT) method, which proposes to freeze pretrained model weights and update an additive low-rank trainable matrix. In this work, we study the enhancement of LoRA training by introducing an $r \times r$ preconditioner in each gradient step where $r$ is the LoRA rank. We theoretically verify that the proposed preconditioner stabilizes feature learning with LoRA under infinite-width NN setting. Empirically, the implementation of this new preconditioner requires a small change to existing optimizer code and creates virtually minuscule storage and runtime overhead. Our experimental results with both large language models and text-to-image diffusion models show that with this new preconditioner, the convergence and reliability of SGD and AdamW can be significantly enhanced. Moreover, the training process becomes much more robust to hyperparameter choices such as learning rate. The new preconditioner can be derived from a novel Riemannian metric in low-rank matrix field. Code can be accessed at https://github.com/pilancilab/Riemannian_Preconditioned_LoRA. (arXiv)

## 🧠 Key ideas (atomic)

- LoRA replaces a pretrained weight matrix W with W plus BA, where only the low-rank factors B and A are trained. (Zhang & Pilanci, 2024) `ev:cited` p. 1 ^zhang2024riemannian-001
- The authors propose scaling the gradient of LoRA factor A on the left by the inverse of B transpose times B. (Zhang & Pilanci, 2024) `ev:asserted` p. 1 ^zhang2024riemannian-002
- Symmetrically, the proposed update scales the gradient of LoRA factor B on the right by the inverse of A times A transpose. (Zhang & Pilanci, 2024) `ev:asserted` p. 1 ^zhang2024riemannian-003
- LoRA+ found that the learning rate of B should exceed that of A, proposing a heuristic ratio of 24 in practice. (Zhang & Pilanci, 2024) `ev:cited` p. 1 ^zhang2024riemannian-004
- The authors note that LoRA parameters live on low-rank matrices forming a quotient manifold, which motivates using [[Riemannian optimization]] tools. (Zhang & Pilanci, 2024) `ev:asserted` p. 1 ^zhang2024riemannian-005
- The scaled gradient method derives from a Riemannian metric that accounts for both the objective function and its constraints. (Zhang & Pilanci, 2024) `ev:cited` p. 1 ^zhang2024riemannian-006
- To first order, an unpreconditioned gradient step confines the LoRA weight update to the column space of B and row space of A. (Zhang & Pilanci, 2024) `ev:computed` p. 3 ^zhang2024riemannian-007
- With the preconditioner, the update becomes a projection of the full weight gradient onto the row space of A and column space of B. (Zhang & Pilanci, 2024) `ev:computed` p. 3 ^zhang2024riemannian-008
- The authors argue that this projected update better approximates full fine-tuning than the unscaled gradient descent step does. (Zhang & Pilanci, 2024) `ev:asserted` p. 3 ^zhang2024riemannian-009
- In a rank-one linear toy model, unpreconditioned gradient descent needs separate learning rates for the two LoRA factors to reach stable feature learning. (Zhang & Pilanci, 2024) `ev:computed` p. 3 ^zhang2024riemannian-010
- In the same toy model, preconditioned updates reach stable feature learning with one shared learning rate inversely proportional to width. (Zhang & Pilanci, 2024) `ev:computed` p. 4 ^zhang2024riemannian-011
- The authors state that the toy example is limited to a linear model with rank one and gradient updates without momentum. (Zhang & Pilanci, 2024) `ev:asserted` p. 4 ^zhang2024riemannian-012
- Theorem 4.1 shows that LoRA trained with preconditioned Adam achieves stable feature learning using a single learning rate of constant order. (Zhang & Pilanci, 2024) `ev:computed` p. 4 ^zhang2024riemannian-013
- For unscaled Adam, stable feature learning requires a learning rate for A inversely proportional to width, with constant order for B. (Zhang & Pilanci, 2024) `ev:cited` p. 4 ^zhang2024riemannian-014
- For scalar outputs, the authors say the preconditioner still allows same-order learning rates, though rates may need tuning across iterations. (Zhang & Pilanci, 2024) `ev:asserted` p. 13 ^zhang2024riemannian-015
- Under the Mishra and Sepulchre metric, Riemannian gradient descent right-multiplies each factor gradient by the inverse Gram matrix of the other factor. (Zhang & Pilanci, 2024) `ev:cited` p. 5 ^zhang2024riemannian-016
- In practice, a small delta times the identity is added before inversion to handle non-invertible Gram matrices of the LoRA factors. (Zhang & Pilanci, 2024) `ev:reported` p. 5 ^zhang2024riemannian-017
- The authors empirically found that scaling each single gradient in AdamW behaves better than scaling the processed gradient used in their proof. (Zhang & Pilanci, 2024) `ev:measured` p. 5 ^zhang2024riemannian-018
- According to the authors, scaled AdamW requires changing only four lines of existing optimizer code, making it simple to implement. (Zhang & Pilanci, 2024) `ev:asserted` p. 5 ^zhang2024riemannian-019
- Fine-tuning GPT-2 medium at rank 4 on A100 GPUs showed little runtime difference between scaled optimizers and their unscaled counterparts. (Zhang & Pilanci, 2024) `ev:measured` p. 6 ^zhang2024riemannian-020
- At LoRA rank 256, the runtime gap between scaled and unscaled optimizers increases compared to rank 4 but remains marginal. (Zhang & Pilanci, 2024) `ev:measured` p. 20 ^zhang2024riemannian-021
- The authors contrast their small preconditioner with Hessian-inverse second-order preconditioners, which usually involve large preconditioners and complex computation. (Zhang & Pilanci, 2024) `ev:asserted` p. 6 ^zhang2024riemannian-022
- GPT-2 experiments follow the original LoRA setup, except that learning rates are tuned individually by grid search for each method. (Zhang & Pilanci, 2024) `ev:reported` p. 6 ^zhang2024riemannian-023
- On E2E with GPT-2 medium at rank 4, scaled GD raised BLEU from 66.6 with SGD to 69.2. (Zhang & Pilanci, 2024) `ev:measured` p. 6 ^zhang2024riemannian-024
- On E2E with GPT-2 medium at rank 4, scaled AdamW reached a BLEU of 69.6 compared with 68.9 for AdamW. (Zhang & Pilanci, 2024) `ev:measured` p. 6 ^zhang2024riemannian-025
- Scaled GD closes the gap between SGD and AdamW on E2E, behaving comparably to AdamW while demanding smaller optimizer storage. (Zhang & Pilanci, 2024) `ev:measured` p. 6 ^zhang2024riemannian-026
- At LoRA rank 1 on E2E with GPT-2 medium, scaled GD raised BLEU from 35.9 with SGD to 68.2. (Zhang & Pilanci, 2024) `ev:measured` p. 22 ^zhang2024riemannian-027
- Across LoRA ranks 1, 4, 8, scaled optimizers outperformed their unscaled counterparts on most E2E evaluation metrics. (Zhang & Pilanci, 2024) `ev:measured` p. 22 ^zhang2024riemannian-028
- For GPT-2 small at rank 4 on E2E, scaled GD raised BLEU from 54.8 with SGD to 68.5. (Zhang & Pilanci, 2024) `ev:measured` p. 22 ^zhang2024riemannian-029
- The authors found lower AdamW beta values beneficial for scaled AdamW, using β1 of 0.7 with β2 of 0.8 on GPT-2. (Zhang & Pilanci, 2024) `ev:measured` p. 21 ^zhang2024riemannian-030
- On DART with GPT-2 medium at rank 4, scaled GD raised BLEU from 43.2 with SGD to 46.1. (Zhang & Pilanci, 2024) `ev:measured` p. 23 ^zhang2024riemannian-031
- On DART with GPT-2 medium at rank 4, scaled AdamW raised BLEU from 47.1 with AdamW to 47.9. (Zhang & Pilanci, 2024) `ev:measured` p. 23 ^zhang2024riemannian-032
- On WebNLG across all categories, scaled GD raised BLEU from 52.4 with SGD to 54.8 with GPT-2 medium. (Zhang & Pilanci, 2024) `ev:measured` p. 23 ^zhang2024riemannian-033
- On WebNLG across all categories, scaled AdamW raised BLEU from 55.5 with AdamW to 56.3 with GPT-2 medium. (Zhang & Pilanci, 2024) `ev:measured` p. 23 ^zhang2024riemannian-034
- Mistral 7B was fine-tuned as a 4-bit quantized model, with LoRA rank 16 factors injected into each linear layer. (Zhang & Pilanci, 2024) `ev:reported` p. 23 ^zhang2024riemannian-035
- On GLUE with 4-bit Mistral 7B at rank 16, scaled AdamW raised the average score from 88.28 with AdamW to 89.01. (Zhang & Pilanci, 2024) `ev:measured` p. 7 ^zhang2024riemannian-036
- On GLUE with 4-bit Mistral 7B at rank 16, scaled GD raised the average score from 71.21 with SGD to 80.36. (Zhang & Pilanci, 2024) `ev:measured` p. 7 ^zhang2024riemannian-037
- On the STS-B task with Mistral 7B, scaled GD scored 90.31 whereas plain SGD scored 47.64. (Zhang & Pilanci, 2024) `ev:measured` p. 7 ^zhang2024riemannian-038
- In the Mistral 7B GLUE experiments, scaled optimizers outperformed unscaled optimizers on all evaluation metrics. (Zhang & Pilanci, 2024) `ev:measured` p. 6 ^zhang2024riemannian-039
- Object generation experiments fine-tuned Stable Diffusion V1.5, injecting LoRA into the U-Net plus text encoder, following a public repository. (Zhang & Pilanci, 2024) `ev:reported` p. 7 ^zhang2024riemannian-040
- The U-Net learning rate was fixed at 1e −4, which the authors found important for generating recognizable images. (Zhang & Pilanci, 2024) `ev:reported` p. 7 ^zhang2024riemannian-041
- After fine-tuning on 6 red vase images, AdamW with a text-encoder learning rate of 1e −2 produced out-of-distribution results. (Zhang & Pilanci, 2024) `ev:measured` p. 7 ^zhang2024riemannian-042
- With default learning rates, AdamW generated only red vases for the blue vase prompt, whereas scaled AdamW produced a blue vase. (Zhang & Pilanci, 2024) `ev:measured` p. 7 ^zhang2024riemannian-043
- For a yellow chair prompt, AdamW succeeded only at learning rate 1e −6, while scaled AdamW succeeded at all tested rates. (Zhang & Pilanci, 2024) `ev:measured` p. 24 ^zhang2024riemannian-044
- For the dog object at learning rate 1e −2, AdamW generated only black images, whereas scaled AdamW produced no black images. (Zhang & Pilanci, 2024) `ev:measured` p. 24 ^zhang2024riemannian-045
- Face generation used Mix-of-Show with embedding tuning turned off, tuning only text encoder plus U-Net LoRA factors at rank 4. (Zhang & Pilanci, 2024) `ev:reported` p. 25 ^zhang2024riemannian-046
- Face experiments trained on 14 Potter images, replacing the character name in captions with a special token. (Zhang & Pilanci, 2024) `ev:reported` p. 7 ^zhang2024riemannian-047
- For the pencil sketch prompt across various step sizes, scaled AdamW generated images more resembling a pencil sketch than AdamW. (Zhang & Pilanci, 2024) `ev:measured` p. 7 ^zhang2024riemannian-048
- With LoRA fusion coefficients 0.7 or 1, scaled AdamW generated higher quality Potter images than AdamW in visual comparisons. (Zhang & Pilanci, 2024) `ev:measured` p. 25 ^zhang2024riemannian-049
- In Mix-of-Show experiments, the authors observed that SGD requires larger learning rates than AdamW to generate sensible images. (Zhang & Pilanci, 2024) `ev:measured` p. 25 ^zhang2024riemannian-050
- The authors note it is widely observed that training loss is useless for monitoring image quality when training diffusion models. (Zhang & Pilanci, 2024) `ev:asserted` p. 6 ^zhang2024riemannian-051
- For a reparameterized two-layer ReLU tuning problem, the authors show scaled GD has a convergence rate independent of data condition number. (Zhang & Pilanci, 2024) `ev:computed` p. 7 ^zhang2024riemannian-052
- Theorem 7.4 shows the maximum distance to the optimum contracts by a factor 1 −0.5η per step for step sizes up to 2/3. (Zhang & Pilanci, 2024) `ev:computed` p. 8 ^zhang2024riemannian-053
- Theorem 7.4 assumes restricted isometry constants of at most 0.01 together with an extended spectral initialization of the LoRA factors. (Zhang & Pilanci, 2024) `ev:computed` p. 8 ^zhang2024riemannian-054
- The convex reformulation of the two-layer ReLU network holds when the number of hidden neurons is at least 2Pd. (Zhang & Pilanci, 2024) `ev:cited` p. 7 ^zhang2024riemannian-055
- The authors chose a local convergence proof following Tong et al. rather than the global proof of Jia et al. (Zhang & Pilanci, 2024) `ev:asserted` p. 20 ^zhang2024riemannian-056
- Prior work showed local convergence of scaled GD, at rates independent of condition number, for matrix sensing and robust PCA. (Zhang & Pilanci, 2024) `ev:cited` p. 9 ^zhang2024riemannian-057
- LoRA can achieve fine-tuning results similar to full fine-tuning with 10,000 times fewer parameters, according to prior work. (Zhang & Pilanci, 2024) `ev:cited` p. 9 ^zhang2024riemannian-058
- The authors state they are unaware of prior work accelerating LoRA training by exploiting its low-rank matrix factorization structure. (Zhang & Pilanci, 2024) `ev:asserted` p. 9 ^zhang2024riemannian-059
- The authors claim this is the first work to apply [[Riemannian optimization]] in designing preconditioners for fine-tuning large foundation models. (Zhang & Pilanci, 2024) `ev:asserted` p. 2 ^zhang2024riemannian-060

## 🎯 Contributions

## 📖 Glossary

- **LoRA** — Parameter-efficient fine-tuning that trains an additive low-rank product BA over frozen weights.
- **Scaled GD** — Gradient descent whose factor gradients are multiplied by inverse Gram matrices of the other factor.
- **Scaled AdamW** — AdamW applied to per-step preconditioned LoRA gradients.
- **Stable feature learning** — Features and their per-step increments stay constant order as network width grows.
- **Infinite-width limit** — Asymptotic analysis of training as the number of neurons tends to infinity.
- **Quotient manifold** — Manifold of equivalence classes; here factor pairs giving the same product BA.
- **Riemannian metric** — Inner product on tangent spaces defining gradients on a manifold.
- **Restricted isometry property (RIP)** — Linear map approximately preserving Frobenius norms of all low-rank matrices.
- **LoRA fusion coefficient** — Scale alpha applied to the low-rank update when merging it into weights.

## ❓ Open questions

- Does stable feature learning with preconditioned Adam hold without the sign-preserving gradient-processing assumption proved only for momentum-free Adam?
- Why does scaling each raw gradient in AdamW work better than scaling the processed gradient analysed in Theorem 4.1?
- Can the local convergence guarantee for the reparameterized ReLU problem be extended to global convergence or to deeper nonlinear networks?
- How does the preconditioner compare with LoRA+ learning-rate ratios in a head-to-head experiment? The paper does not report one.
- Do the diffusion-model gains hold under quantitative image-quality metrics rather than visual inspection alone?
- How does runtime and memory overhead scale for LoRA ranks well above 256 or for full-weight low-rank methods?

## 📝 Notes on reading

- Version read: arXiv 2402.02347v3 (5 Jun 2024), which carries the ICML 2024 (PMLR 235) proceedings header; the packet venue says arXiv preprint.
- Figures 1, 3 and 5-14 are image grids of diffusion generations; they are described only qualitatively and no quantitative image metric is reported. Figures 2 and 4 are runtime curves whose axis values were not claimed.
- Table 6 caption says the scaled optimizers improve all metrics uniformly, but on WebNLG unseen TER scaled GD ties SGD (.45 vs .45). Table 4 at rank 8 shows scaled AdamW METEOR 46.6 below AdamW 46.7, consistent with the text's on most metrics.
- Page 4: the second constraint of the preconditioned toy analysis is labelled with delta-1-scaled instead of delta-2-scaled (typo).
- Page 1 attributes the Riemannian metric to Mishra et al. (2012), while Section 5 derives it following Mishra and Sepulchre (2016).
- Theorem 7.4 as stated omits the local condition dist below 0.1 sigma_r used in Lemma B.3; the proof in Appendix B is dense extracted math and was not checked line by line.
- Table 7 (Mistral hyperparameters) is partly garbled in extraction; the QNLI learning-rate row has fewer values than methods.

## Suggested new concepts

- Riemannian preconditioning — a general optimization idea linking metric design on manifolds to practical gradient scaling.
- Scaled gradient descent for low-rank factorization — recurring method across matrix sensing, robust PCA and LoRA.
- Stable feature learning — infinite-width criterion used by LoRA+ and this paper to set learning rates.
- LoRA+ — competing fix for LoRA learning-rate imbalance that this paper positions against.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Precondicionador $r\times r$ desde una métrica riemanniana (D.3).

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
