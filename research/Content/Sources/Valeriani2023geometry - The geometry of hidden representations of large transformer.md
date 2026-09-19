---
aliases: []
type: "source"
title: "The geometry of hidden representations of large transformer models"
citekey: "Valeriani2023geometry"
doi: "10.48550/arXiv.2302.00294"
arxiv: "2302.00294"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2302.00294"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Lucrezia Valeriani", "Diego Doimo", "Francesca Cuturello", "Alessandro Laio", "Alessio Ansuini", "Alberto Cazzaniga"]
sha256: ["0b85eb44fe70e34b774320fb52e10d8e896e095815fb58ab405f3116a877efd1"]
pdf: "Content/Papers/Valeriani2023geometry.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Valeriani2023geometry.pdf]]

> [!abstract] One-sentence summary
> Tracking intrinsic dimension and neighborhood overlap across the layers of protein and image transformers, the paper shows that semantic content peaks at a low-ID region after an early expansion peak, giving an unsupervised way to pick the best layer for downstream tasks.

## Abstract

Large transformers are powerful architectures used for self-supervised data analysis across various data types, including protein sequences, images, and text. In these models, the semantic structure of the dataset emerges from a sequence of transformations between one representation and the next. We characterize the geometric and statistical properties of these representations and how they change as we move through the layers. By analyzing the intrinsic dimension (ID) and neighbor composition, we find that the representations evolve similarly in transformers trained on protein language tasks and image reconstruction tasks. In the first layers, the data manifold expands, becoming high-dimensional, and then contracts significantly in the intermediate layers. In the last part of the model, the ID remains approximately constant or forms a second shallow peak. We show that the semantic information of the dataset is better expressed at the end of the first peak, and this phenomenon can be observed across many models trained on diverse datasets. Based on our findings, we point out an explicit strategy to identify, without supervision, the layers that maximize semantic content: representations at intermediate layers corresponding to a relative minimum of the ID profile are more suitable for downstream learning tasks. (arXiv)

## 🧠 Key ideas (atomic)

- The authors study the [[Intrinsic dimension of neural representations|intrinsic dimension]] and neighbor composition of hidden representations in ESM-2 and Image GPT, two self-supervised transformer families. (Valeriani et al., 2023) `ev:reported` p. 2 ^valeriani2023geometry-001
- The authors argue that in self-supervised models the most semantically rich representation is likely to arise within the intermediate hidden layers. (Valeriani et al., 2023) `ev:asserted` p. 2 ^valeriani2023geometry-002
- The authors propose that these models perform reconstruction in three phases: expansion to [[Intrinsic dimension of neural representations|high intrinsic dimension]], compression, then decoding. (Valeriani et al., 2023) `ev:asserted` p. 2 ^valeriani2023geometry-003
- The authors liken the early data expansion to kernel methods, which implicitly expand the feature space through non-linear functions of input features. (Valeriani et al., 2023) `ev:asserted` p. 2 ^valeriani2023geometry-004
- Intrinsic dimension is measured with the [[TwoNN estimator]], which needs only the distances from each point to its first two nearest neighbors. (Valeriani et al., 2023) `ev:reported` p. 2 ^valeriani2023geometry-005
- Under locally constant density, the ratio of second to first nearest-neighbor distances follows a Pareto distribution whose shape parameter equals the ID. (Valeriani et al., 2023) `ev:cited` p. 2 ^valeriani2023geometry-006
- The study adopts the [[TwoNN estimator|TwoNN implementation]] of the DADApy library for its intrinsic dimension analysis of hidden representations. (Valeriani et al., 2023) `ev:reported` p. 2 ^valeriani2023geometry-007
- Neighborhood overlap measures the similarity of two layer representations as the average fraction of shared k-nearest neighbors per data point. (Valeriani et al., 2023) `ev:reported` p. 3 ^valeriani2023geometry-008
- Overlap with ground truth classes serves as a semantic probe by measuring label consistency within the nearest neighbors of each data point. (Valeriani et al., 2023) `ev:reported` p. 3 ^valeriani2023geometry-009
- Neighborhood overlap with the protein superfamilies of the SCOPe dataset is computed with a neighborhood size of k = 10. (Valeriani et al., 2023) `ev:reported` p. 3 ^valeriani2023geometry-010
- For the transformers trained on ImageNet the neighborhood size is set to k = 30, consistent with Doimo et al. (Valeriani et al., 2023) `ev:reported` p. 3 ^valeriani2023geometry-011
- Hidden representations are extracted after the first normalization layer of each block, then average pooled along the sequence dimension. (Valeriani et al., 2023) `ev:reported` p. 3 ^valeriani2023geometry-012
- The ESM-2 models were trained by Lin et al. on the Uniref50 dataset with a masked language model objective. (Valeriani et al., 2023) `ev:cited` p. 3 ^valeriani2023geometry-013
- The iGPT networks were trained by Chen et al. on the ImageNet dataset with a next token prediction objective. (Valeriani et al., 2023) `ev:cited` p. 3 ^valeriani2023geometry-014
- The filtered remote homology dataset built from Astral SCOPe v2.08 contains 10,256 sequences grouped into 288 superfamilies. (Valeriani et al., 2023) `ev:reported` p. 3 ^valeriani2023geometry-015
- The iGPT analysis uses 90, 000 ImageNet training images drawn from 300 randomly selected classes with 300 images per class. (Valeriani et al., 2023) `ev:reported` p. 3 ^valeriani2023geometry-016
- Experiments ran on a machine with 2 Intel Xeon Gold 6226 processors, 256GB of RAM, plus 2 Nvidia V100 GPUs with 32GB memory. (Valeriani et al., 2023) `ev:reported` p. 3 ^valeriani2023geometry-017
- In ESM-2 protein language models the [[Intrinsic dimension of neural representations|ID profile]] shows three distinct phases: a peak phase, a plateau phase, then a final ascent. (Valeriani et al., 2023) `ev:measured` p. 4 ^valeriani2023geometry-018
- During the peak phase the ID reaches maxima of approximately 20, 25, and 32 for ESM-2 35M, 650M, and 3B respectively. (Valeriani et al., 2023) `ev:measured` p. 4 ^valeriani2023geometry-019
- After the peak, the ID of ESM-2 models contracts quickly, stabilizing at values between 5 and 7 in the plateau phase. (Valeriani et al., 2023) `ev:measured` p. 4 ^valeriani2023geometry-020
- Plateau ID values in ESM-2 are consistent across model sizes even though the embedding dimension varies from 480 to 2560. (Valeriani et al., 2023) `ev:measured` p. 4 ^valeriani2023geometry-021
- The plateau ID in pLMs is consistent with the values between 6 and 12 measured by Facco et al. on protein sequences. (Valeriani et al., 2023) `ev:measured` p. 4 ^valeriani2023geometry-022
- The authors suggest that plateau representations can gauge the underlying variability arising from evolutionary changes in protein sequences. (Valeriani et al., 2023) `ev:asserted` p. 5 ^valeriani2023geometry-023
- In the final ascent, the ESM-2 ID returns progressively to values close to the input ID after the positional embedding. (Valeriani et al., 2023) `ev:measured` p. 5 ^valeriani2023geometry-024
- The authors attribute the final ID ascent in pLMs to the masked language modeling objective of recovering missing tokens. (Valeriani et al., 2023) `ev:asserted` p. 5 ^valeriani2023geometry-025
- The iGPT models studied are small, medium, and large versions trained on ImageNet with 76M, 455M, and 1.4B parameters. (Valeriani et al., 2023) `ev:reported` p. 5 ^valeriani2023geometry-026
- In all iGPT models the ID of the output is similar to that of the input, in line with protein language models. (Valeriani et al., 2023) `ev:measured` p. 5 ^valeriani2023geometry-027
- iGPT-S shows a hunchback ID profile resembling convolutional models on ImageNet, but with a significantly smaller peak value around 25. (Valeriani et al., 2023) `ev:measured` p. 5 ^valeriani2023geometry-028
- The maximum ID grows with iGPT model size, reaching 28 for iGPT-M and 32 for iGPT-L. (Valeriani et al., 2023) `ev:measured` p. 5 ^valeriani2023geometry-029
- After an initial decrease between 0.3 and 0.4 of relative depth, iGPT models show a common local ID minimum of 22. (Valeriani et al., 2023) `ev:measured` p. 5 ^valeriani2023geometry-030
- Unlike pLMs, iGPT models form a second, shallower ID peak near the network end, with the exception of iGPT-S. (Valeriani et al., 2023) `ev:measured` p. 6 ^valeriani2023geometry-031
- The ID at the iGPT minimum is compatible with the 13 to 24 range found at convolutional classifier outputs by Ansuini et al. (Valeriani et al., 2023) `ev:measured` p. 5 ^valeriani2023geometry-032
- In ESM-2 the consecutive-layer neighborhood overlap remains approximately at 0.5 in the first 40% of the layers, matching the ID peak. (Valeriani et al., 2023) `ev:measured` p. 5 ^valeriani2023geometry-033
- During the plateau phase over 90% of the neighbors are shared between consecutive layers in the larger ESM-2 models. (Valeriani et al., 2023) `ev:measured` p. 5 ^valeriani2023geometry-034
- The smallest ESM-2 model shows less consistent neighborhood composition in the plateau, with some rearrangements across successive layers. (Valeriani et al., 2023) `ev:measured` p. 5 ^valeriani2023geometry-035
- In iGPT, consecutive-layer overlap shifts from about 0.7 in early layers to about 0.9 later, more gradually than in pLMs. (Valeriani et al., 2023) `ev:measured` p. 5 ^valeriani2023geometry-036
- A significant neighborhood rearrangement is always observed in the last iGPT layers, where the reconstruction task is carried on. (Valeriani et al., 2023) `ev:measured` p. 5 ^valeriani2023geometry-037
- Early in ESM-2 (650M) training a peak forms rapidly in early layers, while the remaining ID curve resembles an untrained model. (Valeriani et al., 2023) `ev:measured` p. 6 ^valeriani2023geometry-038
- In ESM-2 (650M) the [[Intrinsic dimension of neural representations|plateau-layer ID]] substantially decreases in a later training stage, after the initial ID peak has emerged. (Valeriani et al., 2023) `ev:measured` p. 6 ^valeriani2023geometry-039
- The authors relate the training-time compression of ESM-2 plateau layers tightly to the emergence of semantic information. (Valeriani et al., 2023) `ev:asserted` p. 6 ^valeriani2023geometry-040
- In iGPT-L the first ID peak emerges in the initial layers during early training, starting from a flat untrained ID curve. (Valeriani et al., 2023) `ev:measured` p. 6 ^valeriani2023geometry-041
- Later in iGPT-L training, the ID decreases at 0.4 of relative depth, forming the local minimum of the profile. (Valeriani et al., 2023) `ev:measured` p. 6 ^valeriani2023geometry-042
- A second ID peak emerges in the last third of the iGPT-L hidden layers during later training stages. (Valeriani et al., 2023) `ev:measured` p. 6 ^valeriani2023geometry-043
- Chen et al. had already demonstrated with linear probes that features extracted from intermediate iGPT layers encode semantic information. (Valeriani et al., 2023) `ev:cited` p. 6 ^valeriani2023geometry-044
- Rives et al. observed that Euclidean distances among last hidden layer pLM representations encode information related to remote homology. (Valeriani et al., 2023) `ev:cited` p. 7 ^valeriani2023geometry-045
- The remote homology overlap uses superfamily labels while excluding neighbors in the same family, focusing specifically on remote homology. (Valeriani et al., 2023) `ev:reported` p. 7 ^valeriani2023geometry-046
- Structural homology information is absent in the ESM-2 positional embedding layer, according to the overlap with superfamily labels. (Valeriani et al., 2023) `ev:measured` p. 7 ^valeriani2023geometry-047
- The overlap with remote homologs reaches a stationary maximum of about 0.8 in the plateau phase of ESM-2 models. (Valeriani et al., 2023) `ev:measured` p. 7 ^valeriani2023geometry-048
- Remote homology prediction by nearest neighbor search is considerably lower in the last hidden layer, scoring 0.4 instead of 0.8. (Valeriani et al., 2023) `ev:measured` p. 7 ^valeriani2023geometry-049
- The authors state that searching for homologs in plateau layers can improve state-of-the-art methods based on last-layer representations. (Valeriani et al., 2023) `ev:asserted` p. 7 ^valeriani2023geometry-050
- In a ProtT5-XL-U50 1-nearest-neighbor homology search on SCOPe, a plateau layer improved accuracy by about 6% over the last layer. (Valeriani et al., 2023) `ev:measured` p. 16 ^valeriani2023geometry-051
- The roughly 6% gain in homology search from using a plateau layer is obtained without any further training. (Valeriani et al., 2023) `ev:measured` p. 16 ^valeriani2023geometry-052
- In all iGPT models the overlap with ImageNet labels peaks around 0.4 relative depth, where larger models have lower ID. (Valeriani et al., 2023) `ev:measured` p. 7 ^valeriani2023geometry-053
- The peak overlap with ImageNet labels is 0.15 in iGPT-S, 0.27 in iGPT-M, and 0.35 in iGPT-L. (Valeriani et al., 2023) `ev:measured` p. 7 ^valeriani2023geometry-054
- The authors conclude that large transformers behave essentially like sophisticated autoencoders, encoding data into a low-dimensional abstract representation before decoding. (Valeriani et al., 2023) `ev:asserted` p. 8 ^valeriani2023geometry-055
- The authors liken iGPT-L to a symmetric autoencoder, as its second ID peak approximately mirrors the first. (Valeriani et al., 2023) `ev:asserted` p. 8 ^valeriani2023geometry-056
- The authors state that the relation between [[Intrinsic dimension of neural representations|low ID after encoding]] and abstract content is robust in all models considered. (Valeriani et al., 2023) `ev:asserted` p. 8 ^valeriani2023geometry-057
- The authors state that the vast neighbor rearrangement near the output serves decoding and causes a degradation of abstract content. (Valeriani et al., 2023) `ev:asserted` p. 8 ^valeriani2023geometry-058
- On CIFAR10 the ID of a representation decreases after average pooling, but the ID profile shape does not change qualitatively. (Valeriani et al., 2023) `ev:measured` p. 9 ^valeriani2023geometry-059
- ID profiles do not change quantitatively when representations are extracted after the attention maps or after the MLP blocks. (Valeriani et al., 2023) `ev:measured` p. 9 ^valeriani2023geometry-060
- The authors note that pixel brightness variations and reduced input resolution in ImageNet can artificially alter the ID significantly. (Valeriani et al., 2023) `ev:asserted` p. 9 ^valeriani2023geometry-061
- Early analyses of GPT-2-XL on the SST dataset did not reveal a second ID peak similar to the one in iGPT. (Valeriani et al., 2023) `ev:measured` p. 9 ^valeriani2023geometry-062
- In Llama-v2 with 70 billion parameters the ID profile is more complex, showing three peaks and two local minima across hidden layers. (Valeriani et al., 2023) `ev:measured` p. 9 ^valeriani2023geometry-063
- In Llama-v2 the highest overlap with sentence sentiment classes occurs at the first local ID minimum, at 0.3 relative depth. (Valeriani et al., 2023) `ev:measured` p. 19 ^valeriani2023geometry-064
- The reported ID values are [[TwoNN estimator|TwoNN estimates]] on the dataset decimated by a factor of 4, where scale dependence was low. (Valeriani et al., 2023) `ev:reported` p. 15 ^valeriani2023geometry-065
- The PAk method showed that, on average, the density can be considered constant within the first 6 neighboring data points. (Valeriani et al., 2023) `ev:measured` p. 15 ^valeriani2023geometry-066
- The three-phase ID behavior also appears in ProtBert, ProtT5-XL-U50, ESM-1v, and ESM-1b trained on different UniRef datasets. (Valeriani et al., 2023) `ev:measured` p. 16 ^valeriani2023geometry-067
- Neighborhood overlap profiles in ESM-2 (650M) and iGPT-L stay qualitatively unchanged when the neighborhood size k varies from 1 to 50. (Valeriani et al., 2023) `ev:measured` p. 18 ^valeriani2023geometry-068

## 🎯 Contributions

## 📖 Glossary

- **Intrinsic dimension (ID)** — Dimensionality of the manifold approximating the data; minimum coordinates needed to specify a point.
- **TwoNN** — ID estimator using only each point's distances to its first two nearest neighbors.
- **Neighborhood overlap** — Average fraction of k-nearest neighbors shared by a data point across two representations.
- **Overlap with ground truth** — Fraction of a point's k-nearest neighbors sharing its label; a semantic probe.
- **Relative depth** — Block number divided by the total number of blocks in the model.
- **Remote homology** — Similar protein structure from common ancestry despite highly dissimilar amino acid sequences.
- **Protein language model (pLM)** — Transformer trained with self-supervision on protein sequences, e.g. ESM-2.
- **iGPT** — Image GPT: transformer trained by next-pixel prediction on quantized ImageNet images.
- **PAk** — Point Adaptive kNN; finds the neighborhood size over which density is constant.

## ❓ Open questions

- How similar are the representations at the ID minima to those learned by supervised models on the same data?
- Why does the second ID peak appear in the large iGPT models, and why only late in training?
- How should the low-ID plateau representations of pLMs be interpreted?
- Does the ID-minimum rule for picking semantic layers hold across NLP tasks, given the more complex Llama-v2 profile after its second peak?
- How much do average pooling and the choice of distance for variable-length sequences shape the measured ID profiles in pLMs?

## 📝 Notes on reading

Version read: arXiv 2302.00294v2 (30 Oct 2023), the NeurIPS 2023 camera-ready; matches the packet identifier.

Figures 1-4 and S1-S6 are plots whose axis ticks were extracted as bare numbers; values were claimed only where the body text or captions state them.

The training-checkpoint counts in Sec. 3.1 and the Fig. 3 caption are garbled by extraction (powers of ten printed as 104, 105, 106); these step numbers were not claimed.

Internal typos: p. 4 writes ESM-2 35B where Table 1 and the rest of the paper say ESM-2 35M; p. 9 writes tree peaks for three peaks; the acknowledgments write ESB-2(650M) for ESM-2 (650M).

The body (p. 7) gives the plateau-layer homology improvement as approximately 6% and defers to Fig. S2, where the experiment uses ProtT5-XL-U50 with k = 1 rather than the ESM-2 models of Fig. 4.

Neighborhood overlap and ground-truth overlap equations on p. 3 were garbled in extraction but are described in prose.

## Suggested new concepts

- Intrinsic dimension of neural representations — central quantity here, reused across many layer-analysis papers.
- Neighborhood overlap — a reusable, label-free metric for comparing layer representations.
- Unsupervised layer selection — choosing the best embedding layer for downstream tasks without labels, via geometry.
- Transformers as autoencoders (expansion-compression-decoding) — an interpretive frame for self-supervised model depth.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** Mide dimensión intrínseca capa a capa en transformers: expansión, contracción y meseta semántica; guía para elegir de qué capa extraer rasgos de un ViT/VLA.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
