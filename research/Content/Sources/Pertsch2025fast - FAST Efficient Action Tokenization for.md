---
aliases: []
type: "source"
title: "FAST: Efficient Action Tokenization for Vision-Language-Action Models"
citekey: "Pertsch2025fast"
doi: "10.48550/arXiv.2501.09747"
arxiv: "2501.09747"
year: 2025
publication_type: "preprint"
url: "https://arxiv.org/abs/2501.09747"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Karl Pertsch", "Kyle Stachowicz", "Brian Ichter", "Danny Driess", "Suraj Nair", "Quan Vuong", "Oier Mees", "Chelsea Finn", "Sergey Levine"]
sha256: ["3739b31f5fecdde371509ff5bb13619979734e894a255a9b264253f4cc53934a"]
pdf: "Content/Papers/Pertsch2025fast.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Pertsch2025fast.pdf]]

> [!abstract] One-sentence summary
> FAST tokenizes robot action chunks by DCT plus byte pair encoding, letting autoregressive VLAs learn dexterous high-frequency tasks and match diffusion π0 while training up to 5x faster.

## Abstract

Autoregressive sequence models, such as Transformer-based vision-language action (VLA) policies, can be tremendously effective for capturing complex and generalizable robotic behaviors. However, such models require us to choose a tokenization of our continuous action signals, which determines how the discrete symbols predicted by the model map to continuous robot actions. We find that current approaches for robot action tokenization, based on simple per-dimension, per-timestep binning schemes, typically perform poorly when learning dexterous skills from high-frequency robot data. To address this challenge, we propose a new compression-based tokenization scheme for robot actions, based on the discrete cosine transform. Our tokenization approach, Frequency-space Action Sequence Tokenization (FAST), enables us to train autoregressive VLAs for highly dexterous and high-frequency tasks where standard discretization methods fail completely. Based on FAST, we release FAST+, a universal robot action tokenizer, trained on 1M real robot action trajectories. It can be used as a black-box tokenizer for a wide range of robot action sequences, with diverse action spaces and control frequencies. Finally, we show that, when combined with the pi0 VLA, our method can scale to training on 10k hours of robot data and match the performance of diffusion VLAs, while reducing training time by up to 5x. (arXiv)

## 🧠 Key ideas (atomic)

- Prior autoregressive robot policies typically tokenize continuous actions with a naive per-dimension, [[Action tokenization|per-timestep binning scheme]], as in RT-1, RT-2 and OpenVLA. (Pertsch et al., 2025) `ev:cited` p. 1 ^pertsch2025fast-001
- The authors find that per-timestep binning tokenization performs poorly when policies learn dexterous skills with high-frequency control. (Pertsch et al., 2025) `ev:measured` p. 1 ^pertsch2025fast-002
- The authors argue that highly correlated action tokens diminish the effectiveness of the next-token prediction objective used in [[Vision-language-action models|autoregressive VLAs]]. (Pertsch et al., 2025) `ev:asserted` p. 2 ^pertsch2025fast-003
- With correlated tokens, low token prediction loss can often be achieved by simply copying the most recent action token, leaving models in poor local optima. (Pertsch et al., 2025) `ev:asserted` p. 2 ^pertsch2025fast-004
- The key insight of the paper is that robot action signals need to be compressed before training to reduce correlation between consecutive tokens. (Pertsch et al., 2025) `ev:asserted` p. 2 ^pertsch2025fast-005
- FAST bases its compression on the discrete cosine transform, which is widely used for compressing continuous signals such as JPEG images. (Pertsch et al., 2025) `ev:reported` p. 2 ^pertsch2025fast-006
- FAST+ is a [[Action tokenization|universal action tokenizer]] trained on 1M real robot action trajectories covering diverse embodiments, action spaces and control frequencies. (Pertsch et al., 2025) `ev:reported` p. 2 ^pertsch2025fast-007
- The authors find that [[Action tokenization|vector-quantized action tokenizers]] fail on high-frequency tasks requiring fine-grained control, despite performing well at coarse, low-fidelity reconstruction. (Pertsch et al., 2025) `ev:asserted` p. 3 ^pertsch2025fast-008
- [[Action tokenization|Binning tokenization]] discretizes each action dimension independently into N uniform bins over the training range, most commonly with N = 256. (Pertsch et al., 2025) `ev:cited` p. 3 ^pertsch2025fast-009
- For high-frequency robot data, binning tokenization can easily produce hundreds of tokens per [[Action chunking|action chunk]], making training challenging and inference slow. (Pertsch et al., 2025) `ev:asserted` p. 3 ^pertsch2025fast-010
- The didactic case study trains a small autoregressive transformer to predict a cubic spline interpolating four randomly generated points. (Pertsch et al., 2025) `ev:reported` p. 4 ^pertsch2025fast-011
- The case study varies the sampling rate of the target signal from 25 to 800 timesteps per sequence without changing the underlying dataset. (Pertsch et al., 2025) `ev:reported` p. 4 ^pertsch2025fast-012
- With binning tokenization, prediction error rises steeply as the sampling rate increases, until the model eventually simply copies the first action. (Pertsch et al., 2025) `ev:measured` p. 4 ^pertsch2025fast-013
- The authors argue that under per-timestep tokenization the marginal information of each token approaches zero as the control frequency increases. (Pertsch et al., 2025) `ev:asserted` p. 4 ^pertsch2025fast-014
- OpenVLA worked well on the low-frequency BridgeV2 and RT-1 datasets but struggled to fit the higher-frequency DROID dataset. (Pertsch et al., 2025) `ev:cited` p. 4 ^pertsch2025fast-015
- The authors state that any sufficiently effective compression approach applied to the action targets is suited to improve VLA training speed. (Pertsch et al., 2025) `ev:asserted` p. 4 ^pertsch2025fast-016
- FAST normalizes input actions such that the 1st and 99th quantile of each action dimension in the training data map to [−1, 1]. (Pertsch et al., 2025) `ev:reported` p. 4 ^pertsch2025fast-017
- Quantiles are used for normalization to be robust to outlier actions that occasionally occur in large robot datasets. (Pertsch et al., 2025) `ev:reported` p. 4 ^pertsch2025fast-018
- After normalization, FAST applies the discrete cosine transform to each action dimension of the chunk separately, converting it to the frequency domain. (Pertsch et al., 2025) `ev:reported` p. 4 ^pertsch2025fast-019
- Insignificant DCT coefficients are omitted through a scale-and-round operation whose scaling hyperparameter trades off lossiness against compression rate. (Pertsch et al., 2025) `ev:reported` p. 4 ^pertsch2025fast-020
- After rounding, the DCT coefficient matrix is typically sparse, with only a few significant coefficients remaining per action dimension. (Pertsch et al., 2025) `ev:reported` p. 4 ^pertsch2025fast-021
- FAST flattens the sparse DCT matrix into a one-dimensional integer vector, interleaving action dimensions by including all low-frequency components first. (Pertsch et al., 2025) `ev:reported` p. 5 ^pertsch2025fast-022
- A byte pair encoding tokenizer then losslessly compresses the flattened coefficient vector into dense action tokens, squashing the zero-valued components. (Pertsch et al., 2025) `ev:reported` p. 5 ^pertsch2025fast-023
- The authors choose column-first flattening, finding that predicting low-frequency components first during autoregressive prediction leads to more stable policy rollouts. (Pertsch et al., 2025) `ev:asserted` p. 5 ^pertsch2025fast-024
- The tokenizer has only two hyperparameters: the scale applied to DCT coefficients before rounding and the BPE vocabulary size. (Pertsch et al., 2025) `ev:reported` p. 5 ^pertsch2025fast-025
- All single-dataset tokenization experiments use the same hyperparameter values, a rounding scale of 10 and a BPE vocabulary size of 1024. (Pertsch et al., 2025) `ev:reported` p. 5 ^pertsch2025fast-026
- The authors find both tokenizer hyperparameters not very sensitive, in contrast to learned vector-quantization modules needing dataset-specific hyperparameter selection. (Pertsch et al., 2025) `ev:asserted` p. 5 ^pertsch2025fast-027
- In the toy example, training on DCT-compressed target tokens achieves constantly low prediction error across a wide range of sampling frequencies. (Pertsch et al., 2025) `ev:measured` p. 5 ^pertsch2025fast-028
- Training the BPE vocabulary, the only learned component of the tokenizer, is fast, typically taking only a few minutes per dataset. (Pertsch et al., 2025) `ev:reported` p. 5 ^pertsch2025fast-029
- FAST+ was trained on approximately one million 1-second action chunks from single-arm, bi-manual and mobile manipulation robots. (Pertsch et al., 2025) `ev:reported` p. 6 ^pertsch2025fast-030
- FAST is tested with two VLA backbones: π0, based on PaliGemma-3B, and OpenVLA, built on Prismatic 7B. (Pertsch et al., 2025) `ev:reported` p. 6 ^pertsch2025fast-031
- During training, 1-second action chunks are tokenized and the resulting action tokens overwrite the least used tokens in the VLM vocabulary. (Pertsch et al., 2025) `ev:reported` p. 6 ^pertsch2025fast-032
- The evaluation suite comprises 7 tasks, 6 on real robots and 1 in simulation, targeting dexterity and zero-shot generalization. (Pertsch et al., 2025) `ev:reported` p. 6 ^pertsch2025fast-033
- The DROID policy is tested in a completely unseen environment with a new table setup, background, novel objects, viewpoint and table height. (Pertsch et al., 2025) `ev:reported` p. 7 ^pertsch2025fast-034
- FAST is compared with the naive binning tokenization of RT-2, RT-2-X and OpenVLA, and with a learned FSQ-based compression tokenizer. (Pertsch et al., 2025) `ev:reported` p. 7 ^pertsch2025fast-035
- The authors note that the FAST+ training data, the most diverse real robot dataset they could assemble, includes data from their evaluation tasks. (Pertsch et al., 2025) `ev:reported` p. 7 ^pertsch2025fast-036
- On 50 Hz shirt folding, naive tokenization needs 700 tokens per one-second chunk versus 53 for FAST, a compression of 13.2. (Pertsch et al., 2025) `ev:measured` p. 7 ^pertsch2025fast-037
- On BridgeV2 at 5 Hz, FAST reduces the average tokens per one-second chunk from 35 to 20, a compression of 1.75. (Pertsch et al., 2025) `ev:measured` p. 7 ^pertsch2025fast-038
- On DROID at 15 Hz, FAST reduces the average tokens per one-second chunk from 105 to 29, a compression of 3.6. (Pertsch et al., 2025) `ev:measured` p. 7 ^pertsch2025fast-039
- On table bussing at 20 Hz, FAST reduces the average tokens per one-second chunk from 140 to 28, a compression of 5.0. (Pertsch et al., 2025) `ev:measured` p. 7 ^pertsch2025fast-040
- FAST consistently generates roughly 30 action tokens per chunk per robot arm in each domain, about 60 tokens for the bi-manual setup. (Pertsch et al., 2025) `ev:measured` p. 7 ^pertsch2025fast-041
- The authors suggest FAST finds a representation approximating the complexity of the underlying action signal, largely independent of the data frequency. (Pertsch et al., 2025) `ev:asserted` p. 7 ^pertsch2025fast-042
- Policies trained with naive tokenization were unable to make progress on the Table Bussing (20Hz) and T-Shirt Folding (50Hz) tasks. (Pertsch et al., 2025) `ev:measured` p. 7 ^pertsch2025fast-043
- Tokenizers that compress action targets, FAST and FSQ, lead to substantially more efficient training than the [[Action tokenization|naive binning tokenization]] of prior VLAs. (Pertsch et al., 2025) `ev:measured` p. 8 ^pertsch2025fast-044
- FAST performs as well as or at times better than the FSQ baseline, particularly on the dexterous, high-frequency tasks. (Pertsch et al., 2025) `ev:measured` p. 8 ^pertsch2025fast-045
- The authors report that FAST enables the first successful training of a generalist DROID policy evaluable zero-shot in unseen environments by language prompting. (Pertsch et al., 2025) `ev:measured` p. 8 ^pertsch2025fast-046
- The DROID policy performed simple table-top tasks zero-shot across three university campuses, such as picking and placing objects and turning on faucets. (Pertsch et al., 2025) `ev:measured` p. 8 ^pertsch2025fast-047
- On test datasets unseen during its training, the FAST+ tokenizer reduces the number of action tokens by 2x across all datasets. (Pertsch et al., 2025) `ev:measured` p. 9 ^pertsch2025fast-048
- Across all tasks, the universal FAST+ tokenizer closely matches the policy performance of the dataset-specific FAST tokenizers. (Pertsch et al., 2025) `ev:measured` p. 9 ^pertsch2025fast-049
- FAST significantly boosts OpenVLA performance on the high-frequency T-shirt folding task compared with the naive tokenization originally used in OpenVLA. (Pertsch et al., 2025) `ev:measured` p. 9 ^pertsch2025fast-050
- The authors suggest their tokenization is independent of the model backbone and may be easily applied to other pre-trained autoregressive transformers. (Pertsch et al., 2025) `ev:asserted` p. 9 ^pertsch2025fast-051
- Removing the BPE step yields worse rollout performance on table bussing and T-shirt folding, though still better than naive tokenization. (Pertsch et al., 2025) `ev:measured` p. 9 ^pertsch2025fast-052
- Without BPE, a large number of repeated zero tokens dilute the learning signal and slow inference, according to the authors. (Pertsch et al., 2025) `ev:asserted` p. 9 ^pertsch2025fast-053
- On small datasets under 50 hours, Libero and T-Shirt Folding, diffusion π0 and the FAST-based π0 perform comparably. (Pertsch et al., 2025) `ev:measured` p. 9 ^pertsch2025fast-054
- On Table Bussing, the FAST-based VLA reaches high performance with 3x fewer training steps than the diffusion variant of π0. (Pertsch et al., 2025) `ev:measured` p. 9 ^pertsch2025fast-055
- In the DROID evaluations, diffusion π0 often ignores the language instructions, whereas the FAST-based π0 follows them more closely. (Pertsch et al., 2025) `ev:measured` p. 9 ^pertsch2025fast-056
- π0 with FAST needs approximately 750ms of inference per chunk, whereas diffusion π0 typically predicts one-second chunks within 100ms on an NVIDIA 4090. (Pertsch et al., 2025) `ev:measured` p. 9 ^pertsch2025fast-057
- FAST decoding typically needs 30-60 action tokens through the full 2B parameter backbone, versus 10 diffusion steps through a 300M action expert. (Pertsch et al., 2025) `ev:reported` p. 9 ^pertsch2025fast-058
- The authors did not find the slower inference to hurt performance on the static manipulation tasks, though it made evaluations significantly slower. (Pertsch et al., 2025) `ev:measured` p. 9 ^pertsch2025fast-059
- The generalist π0-FAST is trained on [[Cross-embodiment pre-training|the π0 cross-embodied data mixture]], which includes 903M timesteps from the authors' own datasets. (Pertsch et al., 2025) `ev:reported` p. 10 ^pertsch2025fast-060
- The open-source datasets BRIDGE v2, DROID and [[Open X-Embodiment dataset|OXE]] make up 9.1% of the generalist π0-FAST training mixture. (Pertsch et al., 2025) `ev:reported` p. 10 ^pertsch2025fast-061
- The generalist π0-FAST matches the zero-shot performance of diffusion π0, including on the most challenging laundry folding task. (Pertsch et al., 2025) `ev:measured` p. 10 ^pertsch2025fast-062
- The evaluated π0-FAST model required 5x fewer GPU hours for training than the diffusion π0 model from Black et al. (Pertsch et al., 2025) `ev:measured` p. 10 ^pertsch2025fast-063
- Against a compute-matched diffusion π0 checkpoint, π0-FAST clearly outperforms across tasks, which the authors attribute to its faster convergence. (Pertsch et al., 2025) `ev:measured` p. 10 ^pertsch2025fast-064
- The authors tested FAST on static robot manipulators, leaving policy performance on mobile robots, dexterous hands and humanoids to future work. (Pertsch et al., 2025) `ev:asserted` p. 11 ^pertsch2025fast-065
- The authors call for future work on speeding up inference of autoregressive VLA models to enable them to solve highly dynamic tasks. (Pertsch et al., 2025) `ev:asserted` p. 11 ^pertsch2025fast-066
- In sweeps on six datasets, FAST scales much better to high reconstruction fidelity than VQ-based tokenizers, though less efficient at low fidelities. (Pertsch et al., 2025) `ev:measured` p. 16 ^pertsch2025fast-067
- The DROID policy trains on 75k successful episodes for 240k iterations at batch size 256, taking approximately 4 days on 8xH100 GPUs. (Pertsch et al., 2025) `ev:reported` p. 17 ^pertsch2025fast-068

## 🎯 Contributions

## 📖 Glossary

- **Action tokenization** — Mapping continuous robot action sequences to discrete tokens predicted by a sequence model.
- **Action chunk** — A sequence of H future actions predicted jointly from one observation.
- **Binning (naive) tokenization** — Discretizing each action dimension per timestep into uniform bins, usually 256.
- **Discrete cosine transform (DCT)** — Frequency transform representing a signal as a sum of cosines of different frequencies.
- **Byte pair encoding (BPE)** — Lossless compression merging frequent token sequences into new vocabulary tokens.
- **FAST** — Frequency-space Action Sequence Tokenization: quantile normalization, DCT, scale-and-round, flatten, BPE.
- **FAST+** — Universal FAST tokenizer whose BPE vocabulary is trained on about one million action chunks.
- **FSQ** — Finite scalar quantization, a simpler learned alternative to VQ-VAE for compressed tokens.
- **Vision-language-action model (VLA)** — Vision-language model fine-tuned to output robot actions from images and language.
- **π0** — Flow-matching (diffusion) VLA from Physical Intelligence built on PaliGemma-3B.

## ❓ Open questions

- Does FAST policy performance transfer to mobile robots, dexterous hands and humanoids, where only offline compression was tested?
- Would Huffman coding or Lempel-Ziv methods work as well as BPE for the lossless compression stage?
- Can compression-based action encodings be combined with non-autoregressive decoding such as diffusion?
- Can LLM inference optimizations (speculative decoding, quantization, custom kernels) close the roughly 750ms versus 100ms inference gap enough for dynamic tasks?
- Why does diffusion π0 often ignore language instructions in DROID while the autoregressive FAST model follows them more closely?
- Which VLA architecture, autoregressive or diffusion decoding, gives the best trade-off in training speed, language grounding and expressiveness?

## 📝 Notes on reading

Read the arXiv v1 preprint (2501.09747v1, 16 Jan 2025), matching the packet identifier.

Figures 2, 3, 6, 8, 9, 11, 12 and 15 are bar or line plots whose per-task values are not recoverable from the extracted text; only the qualitative conclusions stated in the text and captions were claimed. The in-text OpenVLA and BPE ablation figures on p. 9 likewise have no readable values.

Appendix B (compression vs reconstruction trade-off) has only a heading and the Fig. 12 caption; the axis values are garbled.

Internal inconsistency: the DROID evaluation is described as 16 tasks and 44 trials (p. 18), but Table II lists 17 task rows summing to 44. The DROID training description on p. 18 says "240k iterations (≈3 episodes)", apparently meaning epochs (p. 17 says three epochs). Libero-10 (p. 6) is called Libero-Long in Appendix E.

The paper also releases FAST+ as a HuggingFace AutoProcessor (p. 6), uses BPE partly for its fixed-size vocabulary (p. 5), and applies a sampling temperature of 0.7 for bi-manual tasks (p. 17); these were left unclaimed to stay under the claim cap. The universal tokenizer mixture table (p. 16) and Table III evaluation datasets (p. 19) were not claimed cell by cell.

## Suggested new concepts

- Action tokenization — central design choice for autoregressive VLAs, with binning, VQ/FSQ and compression-based variants to compare.
- Discrete cosine transform for action compression — reusable idea linking signal compression to learning signal quality in token prediction.
- Autoregressive vs diffusion VLAs — recurring architectural trade-off in training speed, inference latency and language following.
- Action chunking — shared assumption across modern visuomotor policies that shapes tokenization and control frequency.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Tokenización DCT de acciones
