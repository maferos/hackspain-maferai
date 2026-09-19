---
aliases: []
type: "source"
title: "Learnable latent embeddings for joint behavioral and neural analysis"
citekey: "Schneider2022learnable"
doi: "10.48550/arXiv.2204.00673"
arxiv: "2204.00673"
year: 2022
publication_type: "preprint"
url: "https://arxiv.org/abs/2204.00673"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Steffen Schneider", "Jin Hwa Lee", "Mackenzie Weygandt Mathis"]
sha256: ["a2bb4117aa47640fb4bcb071705708d42ffa9bb11715c4faad92d83817e2b799"]
pdf: "Content/Papers/Schneider2022learnable.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 70
---

📄 PDF: [[Schneider2022learnable.pdf]]

> [!abstract] One-sentence summary
> CEBRA shapes a contrastive learning objective with behavior or time labels to produce consistent, decodable neural latent embeddings across animals, sessions and recording modalities, with identifiability guarantees.

## Abstract

Mapping behavioral actions to neural activity is a fundamental goal of neuroscience. As our ability to record large neural and behavioral data increases, there is growing interest in modeling neural dynamics during adaptive behaviors to probe neural representations. In particular, neural latent embeddings can reveal underlying correlates of behavior, yet, we lack non-linear techniques that can explicitly and flexibly leverage joint behavior and neural data. Here, we fill this gap with a novel method, CEBRA, that jointly uses behavioral and neural data in a hypothesis- or discovery-driven manner to produce consistent, high-performance latent spaces. We validate its accuracy and demonstrate our tool's utility for both calcium and electrophysiology datasets, across sensory and motor tasks, and in simple or complex behaviors across species. It allows for single and multi-session datasets to be leveraged for hypothesis testing or can be used label-free. Lastly, we show that CEBRA can be used for the mapping of space, uncovering complex kinematic features, and rapid, high-accuracy decoding of natural movies from visual cortex. (arXiv)

## 🧠 Key ideas (atomic)

- CEBRA is a self-supervised learning algorithm that produces consistent embeddings of high-dimensional recordings using auxiliary variables such as behavior and/or time. (Schneider et al., 2022) `ev:asserted` p. 1 ^schneider2022learnable-001
- The method combines ideas from non-linear independent component analysis with contrastive learning to generate latent embeddings conditioned on behavior and/or time. (Schneider et al., 2022) `ev:asserted` p. 1 ^schneider2022learnable-002
- The authors state that non-linear representation learning tools typically rely on generative models that do not yield consistent embeddings across animals. (Schneider et al., 2022) `ev:asserted` p. 1 ^schneider2022learnable-003
- The authors note that UMAP or tSNE lack the ability to explicitly use time information, which is always available in neural recordings. (Schneider et al., 2022) `ev:asserted` p. 1 ^schneider2022learnable-004
- Label-guided VAEs such as pi-VAE do not guarantee consistent neural embeddings across animals, which the authors say limits their generalizability. (Schneider et al., 2022) `ev:cited` p. 1 ^schneider2022learnable-005
- CEBRA does not rely on data augmentation, unlike SimCLR, nor on a specific generative model that would limit its range of use. (Schneider et al., 2022) `ev:asserted` p. 1 ^schneider2022learnable-006
- CEBRA can be used in hypothesis-driven (behavior-guided), discovery-driven (time-only), or hybrid modes to shape the embedding space. (Schneider et al., 2022) `ev:asserted` p. 1 ^schneider2022learnable-007
- The encoder used in this work is a convolutional neural network trained with a contrastive objective, though another model type could be used. (Schneider et al., 2022) `ev:reported` p. 2 ^schneider2022learnable-008
- Theoretical work cited by the authors shows contrastive learning with auxiliary variables is identifiable for bijective networks using a noise contrastive estimation loss. (Schneider et al., 2022) `ev:cited` p. 2 ^schneider2022learnable-009
- Unlike other contrastive learning algorithms, the CEBRA positive and negative pair distributions can be systematically designed using time, behavior, or other auxiliary information. (Schneider et al., 2022) `ev:asserted` p. 3 ^schneider2022learnable-010
- When only discrete labels are used, the CEBRA training scheme is conceptually similar to supervised contrastive learning. (Schneider et al., 2022) `ev:asserted` p. 3 ^schneider2022learnable-011
- Specifying a variable as task-irrelevant yields an embedding space that no longer carries that information, such as trial identity for brain machine interfaces. (Schneider et al., 2022) `ev:asserted` p. 3 ^schneider2022learnable-012
- CEBRA infers latent embeddings without explicitly modeling the data generating process, unlike generative approaches such as pi-VAE or LFADS. (Schneider et al., 2022) `ev:asserted` p. 3 ^schneider2022learnable-013
- On synthetic data, CEBRA significantly outperformed tSNE, UMAP and pi-VAE at reconstructing ground truth latents (one-way ANOVA, F(3, 396)=278.31, p=3.95e-97). (Schneider et al., 2022) `ev:measured` p. 3 ^schneider2022learnable-014
- The synthetic dataset mapped a 2D latent to spiking rates of 100 neurons with four randomly initialized RealNVP blocks, then applied Poisson noise. (Schneider et al., 2022) `ev:reported` p. 11 ^schneider2022learnable-015
- Across the synthetic noise types, CEBRA showed higher, less variable reconstruction scores than pi-VAE over 100 seeds. (Schneider et al., 2022) `ev:measured` p. 18 ^schneider2022learnable-016
- The hippocampus dataset comprised CA1 recordings from four rats running on a 1.6 meter linear track, with 48 to 120 putative pyramidal neurons each. (Schneider et al., 2022) `ev:reported` p. 11 ^schneider2022learnable-017
- For the hippocampus data, spikes were binned into 25ms time windows following the preprocessing used for pi-VAE. (Schneider et al., 2022) `ev:reported` p. 11 ^schneider2022learnable-018
- The authors modified pi-VAE to take 10-time-bin (250 ms) inputs with the CEBRA encoder, calling the result conv-pi-VAE. (Schneider et al., 2022) `ev:reported` p. 16 ^schneider2022learnable-019
- Using a receptive field of 10 time bins gave conv-pi-VAE higher consistency across subjects than the original single-bin pi-VAE implementation. (Schneider et al., 2022) `ev:measured` p. 16 ^schneider2022learnable-020
- Conv-pi-VAE reached a median absolute decoding error of 11 cm on rat 1, versus 12 cm reported for the original pi-VAE. (Schneider et al., 2022) `ev:measured` p. 16 ^schneider2022learnable-021
- CEBRA-Behavior yielded significantly higher cross-subject embedding correlation than conv-pi-VAE with or without test-time labels (one-way ANOVA F(5, 67)=28, p=3.4×10−15). (Schneider et al., 2022) `ev:measured` p. 3 ^schneider2022learnable-022
- The authors note that CEBRA does not require test-time labels to produce its embeddings of neural activity. (Schneider et al., 2022) `ev:asserted` p. 3 ^schneider2022learnable-023
- Without label priors, conv-pi-VAE produced a more entangled latent, suggesting the label prior strongly shapes its output embedding structure. (Schneider et al., 2022) `ev:asserted` p. 3 ^schneider2022learnable-024
- Across repeated runs of each algorithm, CEBRA showed higher consistency than the other benchmarked methods on the hippocampus data. (Schneider et al., 2022) `ev:measured` p. 3 ^schneider2022learnable-025
- Shuffling the behavioral labels, which breaks the correlation between neural activity and position, produced an unstructured hippocampus embedding. (Schneider et al., 2022) `ev:measured` p. 3 ^schneider2022learnable-026
- CEBRA-Time hippocampus embeddings closely resembled position-based ones, suggesting time contrastive learning captured the major latent structure without labels. (Schneider et al., 2022) `ev:measured` p. 3 ^schneider2022learnable-027
- Position plus direction was the most informative label for the hippocampus data, producing the lowest loss at the same training point. (Schneider et al., 2022) `ev:measured` p. 4 ^schneider2022learnable-028
- The value of the InfoNCE loss at convergence serves as an additional goodness of fit metric to select the best labels. (Schneider et al., 2022) `ev:asserted` p. 4 ^schneider2022learnable-029
- Erroneous shuffled labels converged to considerably higher loss values than true behavioral labels in the hippocampus hypothesis tests. (Schneider et al., 2022) `ev:measured` p. 4 ^schneider2022learnable-030
- Decoding position from the position+direction CEBRA embedding gave an R2 of 73.35% versus -49.90% for shuffled labels. (Schneider et al., 2022) `ev:measured` p. 4 ^schneider2022learnable-031
- Median absolute position decoding error was 5.8 cm with the hypothesis-driven embedding versus 44.7 cm with shuffled labels. (Schneider et al., 2022) `ev:measured` p. 4 ^schneider2022learnable-032
- CEBRA-Behavior had significantly better hippocampus decoding performance than pi-VAE or conv-pi-VAE (one-way ANOVA F=131, p=3.6×10−24). (Schneider et al., 2022) `ev:measured` p. 4 ^schneider2022learnable-033
- CEBRA-Time had significantly better decoding performance than the unsupervised methods tSNE, UMAP or PCA (one-way ANOVA F=12091 p=6.95×10−42). (Schneider et al., 2022) `ev:measured` p. 4 ^schneider2022learnable-034
- The authors achieve a median absolute position decoding error of about 5 cm, compared with 12 cm reported for pi-VAE. (Schneider et al., 2022) `ev:measured` p. 4 ^schneider2022learnable-035
- Persistent co-homology of CEBRA-Behavior or -Time hippocampus embeddings revealed a ring topology with Betti numbers (1,1,0). (Schneider et al., 2022) `ev:measured` p. 5 ^schneider2022learnable-036
- Circular coordinates from the first co-cycle showed that the ring topology of the CEBRA models matches position across embedding dimensions. (Schneider et al., 2022) `ev:measured` p. 5 ^schneider2022learnable-037
- Significant Betti numbers were thresholded using the maximum lifespan across 500 CEBRA embeddings trained with shuffled labels. (Schneider et al., 2022) `ev:reported` p. 17 ^schneider2022learnable-038
- Joint multi-animal training produced more consistent embeddings across subjects (one-sided paired T-tests, Allen data p=5.99×10−5; hippocampus p=0.024). (Schneider et al., 2022) `ev:measured` p. 5 ^schneider2022learnable-039
- The authors found no loss in decoding performance when decoding from jointly trained multi-animal CEBRA embeddings. (Schneider et al., 2022) `ev:measured` p. 6 ^schneider2022learnable-040
- After pretraining on a subset of subjects, adapting CEBRA-Behavior for one step on unseen data decreased positional decoding error by 10 cm. (Schneider et al., 2022) `ev:measured` p. 6 ^schneider2022learnable-041
- Adapting a pretrained CEBRA model for 100 steps took 0.65 ± 0.13 sec on average over 40 repeated experiments. (Schneider et al., 2022) `ev:measured` p. 24 ^schneider2022learnable-042
- Adapting the pretrained network reached a lower decoding error more rapidly than training fully on the unseen individual. (Schneider et al., 2022) `ev:measured` p. 6 ^schneider2022learnable-043
- The macaque dataset recorded area 2 of somatosensory cortex during an eight-direction center-out reaching task with a manipulandum. (Schneider et al., 2022) `ev:reported` p. 11 ^schneider2022learnable-044
- In the macaque task, passive trials applied an unexpected 2N force bump to the manipulandum towards one of the eight targets. (Schneider et al., 2022) `ev:reported` p. 11 ^schneider2022learnable-045
- In primate S1 embeddings, active trials showed a clear start and stop, independently of how the models were trained. (Schneider et al., 2022) `ev:measured` p. 6 ^schneider2022learnable-046
- In primate S1 embeddings, passive trials showed a continuous trajectory through the embedding, independently of how the models were trained. (Schneider et al., 2022) `ev:measured` p. 6 ^schneider2022learnable-047
- In the primate embeddings, direction was a less prominent feature, although direction and position are entangled parameters in this task. (Schneider et al., 2022) `ev:measured` p. 6 ^schneider2022learnable-048
- Hand position and active versus passive trial type were readily decodable from 8D+ CEBRA embeddings with a kNN decoder. (Schneider et al., 2022) `ev:measured` p. 6 ^schneider2022learnable-049
- Directional information was not as decodable as position or trial type from the primate CEBRA embeddings. (Schneider et al., 2022) `ev:measured` p. 6 ^schneider2022learnable-050
- CEBRA-Behavior trained on position recovered the primate hand trajectory with an R2 of 88% on held-out test trials. (Schneider et al., 2022) `ev:measured` p. 6 ^schneider2022learnable-051
- On the same primate hand trajectory decoding, an L1 regression using all neurons achieved R2 74%. (Schneider et al., 2022) `ev:measured` p. 7 ^schneider2022learnable-052
- On the same primate hand trajectory decoding, a 16D conv-pi-VAE achieved R2 82%, below 16D CEBRA-Behavior. (Schneider et al., 2022) `ev:measured` p. 7 ^schneider2022learnable-053
- The authors describe their approach as state-of-the-art for decoding hand trajectories on this primate somatosensory dataset. (Schneider et al., 2022) `ev:asserted` p. 7 ^schneider2022learnable-054
- Visual cortex data came from the Allen Brain Observatory, using 10 repeats of Natural Movie 1 recorded with Neuropixels or 2-photon imaging. (Schneider et al., 2022) `ev:reported` p. 7 ^schneider2022learnable-055
- Frame-by-frame visual features from a pretrained DINO ViT/8 vision transformer, 768-dimensional, served as continuous behavior labels for the movie data. (Schneider et al., 2022) `ev:reported` p. 17 ^schneider2022learnable-056
- CEBRA-Behavior embeddings showed trajectories that smoothly capture the movie with either recording modality as the number of neurons increases. (Schneider et al., 2022) `ev:measured` p. 7 ^schneider2022learnable-057
- The authors conclude that there is a highly consistent latent space across Neuropixels and calcium imaging, independent of the recording method. (Schneider et al., 2022) `ev:asserted` p. 7 ^schneider2022learnable-058
- Joint training on stacked neurons across mice and modalities considerably improved consistency without lowering consistency within modality. (Schneider et al., 2022) `ev:measured` p. 7 ^schneider2022learnable-059
- In a jointly trained 32D model using 400 neurons, intra-V1 consistency was significantly higher than inter-area consistency (Welch's t-test, T(19,53)=4.55, p=0.00019). (Schneider et al., 2022) `ev:measured` p. 6 ^schneider2022learnable-060
- The authors suggest that higher intra-area consistency indicates CEBRA is not removing biological differences across visual areas. (Schneider et al., 2022) `ev:asserted` p. 7 ^schneider2022learnable-061
- CEBRA achieved greater than 95% frame decoding accuracy on Neuropixels V1 data, significantly better than naive Bayes or kNN baselines. (Schneider et al., 2022) `ev:measured` p. 7 ^schneider2022learnable-062
- Jointly trained CEBRA outperformed Neuropixels-only CEBRA training for single-frame movie decoding from V1 (one-way ANOVA, F(3,197)=5.88, p=0.0007). (Schneider et al., 2022) `ev:measured` p. 7 ^schneider2022learnable-063
- The V1 decoding analysis held out the last movie repeat as a test set, training on the other nine repeats. (Schneider et al., 2022) `ev:reported` p. 7 ^schneider2022learnable-064
- Shuffling the DINO features gave poor decoding, indicating the DINO features themselves did not drive decoding performance. (Schneider et al., 2022) `ev:measured` p. 7 ^schneider2022learnable-065
- Among the visual areas and PPC tested, decoding from V1 had the highest performance, with PPC (VISrl) the lowest. (Schneider et al., 2022) `ev:measured` p. 7 ^schneider2022learnable-066
- In V1, layers 2/3 and 5/6 showed significantly higher decoding performance than layer 4 (one-way ANOVA, F(2,12)=9.88, p=0.003). (Schneider et al., 2022) `ev:measured` p. 7 ^schneider2022learnable-067
- The authors suggest non-thalamic input layers make frame information more explicit, perhaps via feedback or predictive processing. (Schneider et al., 2022) `ev:asserted` p. 7 ^schneider2022learnable-068
- For two CEBRA models trained to convergence on sufficiently diverse data, the embeddings are consistent up to linear transformations. (Schneider et al., 2022) `ev:computed` p. 14 ^schneider2022learnable-069
- If no mapping exists between the context variable and the signal, CEBRA instead learns a default embedding uniform on the hypersphere. (Schneider et al., 2022) `ev:computed` p. 14 ^schneider2022learnable-070

## 🎯 Contributions

## 📖 Glossary

- **CEBRA** — Consistent EmBeddings of high-dimensional Recordings using Auxiliary variables; contrastive neural embedding method.
- **InfoNCE** — Contrastive loss distinguishing one positive pair from multiple negative pairs given a reference.
- **Linear identifiability** — Two trained models agree up to a linear transformation of their embeddings.
- **Consistency** — R2 of a linear regression between embeddings from different runs, subjects or sessions.
- **Hypothesis-driven mode** — CEBRA training where behavior labels define the positive pair distribution.
- **Discovery-driven mode** — CEBRA training using only time offsets to select positive pairs.
- **conv-pi-VAE** — The authors' pi-VAE variant with a convolutional encoder over 10 time bins.
- **Persistent co-homology** — Topological analysis tracking birth and death of cycles across scales.
- **Betti numbers** — Counts of connected components, loops and voids characterizing a topology.
- **DINO** — Self-supervised vision transformer used here to embed movie frames as labels.
- **Goodness of fit** — Loss minus log batch size; lower values indicate a better-fitting hypothesis.

## ❓ Open questions

- How do CEBRA latent spaces map to neural-level computations, a gap the authors acknowledge?
- Does the consistency across modalities hold for brain areas beyond mouse visual cortex and PPC?
- How does CEBRA scale to datasets too large for full-dataset positive and negative sampling on a GPU?
- How should the similarity measure be chosen when the conditional distribution of latents over time is unknown?
- Can the rapid adaptation to unseen animals support closed-loop real-time brain machine interfaces in practice?

## 📝 Notes on reading

Read the arXiv manuscript v2 (5 October 2022, 46 pages), matching the packet identifier arXiv 2204.00673; a later journal version may differ.

Figures 1-5 and Extended Data Figs. S1-S10 are known only from their captions; embedding plots, confusion matrices and decoding bar charts were not claimed beyond numbers stated in text or captions. The objective equations (Eq. 1-3) and the Supplementary Note 2 proofs are garbled by extraction; only their verbal conclusions were claimed.

Internal inconsistencies: the Fig. 2d caption gives a median absolute error of 5.8 cm while the text says about 5 cm. Supplementary Table 2 reports F-55 (supervised) and F=8 (self/unsupervised) ANOVAs, whereas the main text on p. 4 reports F=131 and F=12091 for the same decoding comparisons. Extended Data Fig. S7 reports consistency at an average position error below 14 cm (7 cm for rat 1), while Methods (p. 15) states 7 cm for the first rat. The Discussion says adaptation takes tens of steps (milliseconds), while Fig. S7 reports 0.65 sec per 100 steps.

The per-neuron-count Tukey HSD tables (Suppl. Tables 3-6) were not claimed cell by cell.

## Suggested new concepts

- Contrastive learning — the core self-supervised objective family CEBRA extends with designed positive and negative distributions.
- Identifiability in non-linear ICA — the theoretical basis for consistency guarantees across runs and animals.
- Neural latent embeddings — a recurring target representation for joint behavioral and neural analysis.
- Persistent homology for embedding validation — a topology-based check of embedding robustness reusable beyond CEBRA.
- Multi-session neural decoding — pooling animals or sessions into a shared latent space for decoding and BMI adaptation.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** CEBRA obtiene embeddings contrastivos consistentes entre sesiones y sujetos, una idea trasladable a alinear latentes entre simulación y realidad.
