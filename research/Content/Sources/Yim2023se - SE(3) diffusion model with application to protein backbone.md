---
aliases: []
type: "source"
title: "SE(3) diffusion model with application to protein backbone generation"
citekey: "Yim2023se"
doi: "10.48550/arXiv.2302.02277"
arxiv: "2302.02277"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2302.02277"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Jason Yim", "Brian L. Trippe", "Valentin De Bortoli", "Emile Mathieu", "Arnaud Doucet", "Regina Barzilay", "Tommi Jaakkola"]
sha256: ["2d60cb8c5e13476ec73949482585da4a604f24e9eb990f818c7378b25d031cfd"]
pdf: "Content/Papers/Yim2023se.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Yim2023se.pdf]]

> [!abstract] One-sentence summary
> The paper builds the theory of SE(3) invariant diffusion over protein frames and turns it into FrameDiff, a score model that generates designable protein backbones up to length 500 without any pretrained structure prediction network.

## Abstract
The design of novel protein structures remains a challenge in protein engineering for applications across biomedicine and chemistry. In this line of work, a diffusion model over rigid bodies in 3D (referred to as frames) has shown success in generating novel, functional protein backbones that have not been observed in nature. However, there exists no principled methodological framework for diffusion on SE(3), the space of orientation preserving rigid motions in R3, that operates on frames and confers the group invariance. We address these shortcomings by developing theoretical foundations of SE(3) invariant diffusion models on multiple frames followed by a novel framework, FrameDiff, for learning the SE(3) equivariant score over multiple frames. We apply FrameDiff on monomer backbone generation and find it can generate designable monomers up to 500 amino acids without relying on a pretrained protein structure prediction network that has been integral to previous methods. We find our samples are capable of generalizing beyond any known protein structure. (arXiv)

## 🧠 Key ideas (atomic)

- The paper develops theoretical foundations for [[Diffusion models on Lie groups|SE(3) invariant diffusion models]] on multiple frames, applied to protein backbone generation. (Yim et al., 2023) `ev:asserted` p. 1 ^yim2023se-001
- Before this work no principled methodological framework existed for [[Diffusion models on Lie groups|diffusion on SE(3)]] that operates on frames and confers group invariance. (Yim et al., 2023) `ev:asserted` p. 1 ^yim2023se-002
- The earlier RFdiffusion model relied on a heuristic denoising loss and required pretraining on protein structure prediction. (Yim et al., 2023) `ev:cited` p. 1 ^yim2023se-003
- An SE(3) invariant process on SE(3)N can only be made translation invariant by keeping the diffusion process centered at the origin. (Yim et al., 2023) `ev:computed` p. 2 ^yim2023se-004
- FrameDiff can generate designable, diverse and novel protein monomers up to length 500 in the authors experiments. (Yim et al., 2023) `ev:measured` p. 2 ^yim2023se-005
- Compared to other methods FrameDiff achieves in-silico designability success rates that are second only to RFdiffusion, a pretrained model. (Yim et al., 2023) `ev:measured` p. 2 ^yim2023se-006
- An N residue backbone is parameterized by N orientation preserving rigid transformations, or frames, mapping fixed idealized atom coordinates. (Yim et al., 2023) `ev:reported` p. 2 ^yim2023se-007
- With an additional torsion angle psi the backbone oxygen is constructed by rotating the idealized oxygen around the Ca-C bond. (Yim et al., 2023) `ev:reported` p. 2 ^yim2023se-008
- Proposition 3.1 shows the chosen inner product identifies SE(3) with SO(3) times R3 from a Riemannian point of view. (Yim et al., 2023) `ev:computed` p. 3 ^yim2023se-009
- Under this metric the SE(3) Brownian motion splits into independent Brownian motions on SO(3) and on R3. (Yim et al., 2023) `ev:computed` p. 3 ^yim2023se-010
- The SO(3) transition density is the IGSO3 density, a series in the rotation angle of the relative rotation. (Yim et al., 2023) `ev:computed` p. 4 ^yim2023se-011
- Their expression agrees with previously proposed laws of the Brownian motion up to a two-fold deceleration of time. (Yim et al., 2023) `ev:computed` p. 4 ^yim2023se-012
- No probability measure on SE(3)N is SE(3) invariant, because no probability measure on R3N is R3 invariant. (Yim et al., 2023) `ev:computed` p. 4 ^yim2023se-013
- A projection matrix removing the center of mass turns the forward process into a process on centered SE(3)N. (Yim et al., 2023) `ev:computed` p. 5 ^yim2023se-014
- Corollary 3.7 shows the distribution produced by the reverse centered process is SO(3) invariant under an invariant initial distribution. (Yim et al., 2023) `ev:computed` p. 5 ^yim2023se-015
- The score network builds on the AlphaFold2 structure module, performing iterative frame updates over a series of layers. (Yim et al., 2023) `ev:reported` p. 5 ^yim2023se-016
- Spatial attention is performed with Invariant Point Attention, which attends to residues that are closer in coordinate space. (Yim et al., 2023) `ev:reported` p. 5 ^yim2023se-017
- A Transformer layer is included to capture interactions along the chain structure of the protein. (Yim et al., 2023) `ev:reported` p. 5 ^yim2023se-018
- Including the Transformer greatly improved training and sample quality in the authors experiments with FrameDiff. (Yim et al., 2023) `ev:measured` p. 5 ^yim2023se-019
- As a result of including the Transformer, the computational complexity of FrameDiff is quadratic in the backbone length. (Yim et al., 2023) `ev:asserted` p. 5 ^yim2023se-020
- Edge embeddings are initialized with self-conditioning using a binned pairwise distance matrix between the model predicted alpha carbon positions. (Yim et al., 2023) `ev:reported` p. 5 ^yim2023se-021
- The translation weighting makes the denoising loss a squared error between true and predicted alpha carbon coordinates. (Yim et al., 2023) `ev:computed` p. 6 ^yim2023se-022
- With the score matching loss alone FrameDiff produced backbones with plausible coarse-grained topologies in early experiments. (Yim et al., 2023) `ev:measured` p. 6 ^yim2023se-023
- Those early backbones also showed unrealistic fine-grained characteristics, such as chain breaks or steric clashes between atoms. (Yim et al., 2023) `ev:measured` p. 6 ^yim2023se-024
- A local neighborhood loss penalizes pairwise atomic distance errors only for atom pairs closer than 0.6 nm. (Yim et al., 2023) `ev:reported` p. 6 ^yim2023se-025
- Auxiliary losses are applied only when the diffusion time is sampled below a quarter of the final time. (Yim et al., 2023) `ev:reported` p. 6 ^yim2023se-026
- A high auxiliary weight of 0.25 led to improved sample quality with fewer steric clashes and chain breaks. (Yim et al., 2023) `ev:measured` p. 6 ^yim2023se-027
- Sampling uses an Euler-Maruyama discretization of the reverse process implemented as a geodesic random walk. (Yim et al., 2023) `ev:reported` p. 7 ^yim2023se-028
- Sampling trajectories are truncated early at a positive time because backbones commonly destabilized in the final steps. (Yim et al., 2023) `ev:reported` p. 7 ^yim2023se-029
- The authors explore generating from the reverse process with noise downscaled by a factor between zero and one. (Yim et al., 2023) `ev:reported` p. 7 ^yim2023se-030
- FrameDiff was trained with four layers on a filtered set of 20312 backbones taken from the Protein Data Bank. (Yim et al., 2023) `ev:reported` p. 7 ^yim2023se-031
- The FrameDiff model comprises 17.4 million parameters in the configuration used for the reported experiments. (Yim et al., 2023) `ev:reported` p. 7 ^yim2023se-032
- The reported model was trained for one week on two A100 Nvidia GPUs by the authors. (Yim et al., 2023) `ev:reported` p. 7 ^yim2023se-033
- ProteinMPNN at temperature 0.1 generates sequences whose structures are then predicted with ESMFold for self-consistency scoring. (Yim et al., 2023) `ev:reported` p. 7 ^yim2023se-034
- Diversity is reported as the number of MaxCluster clusters divided by the number of samples at a 0.5 TM-score threshold. (Yim et al., 2023) `ev:reported` p. 7 ^yim2023se-035
- Novelty is reported as pdbTM, the highest TM-score of a sample to any chain in the Protein Data Bank. (Yim et al., 2023) `ev:reported` p. 7 ^yim2023se-036
- An scRMSD below 2 was shown to be a more stringent designability filter than an scTM above 0.5. (Yim et al., 2023) `ev:cited` p. 7 ^yim2023se-037
- Chroma reported designability of 55% with 100 designed sequences on lengths between 100 and 500. (Yim et al., 2023) `ev:cited` p. 8 ^yim2023se-038
- At noise scale 1.0 with 500 steps and eight sequences, 49% of samples exceeded the 0.5 scTM threshold. (Yim et al., 2023) `ev:measured` p. 8 ^yim2023se-039
- Lowering the noise scale to 0.5 raised the scTM designability to 74% in the same sampling setting. (Yim et al., 2023) `ev:measured` p. 8 ^yim2023se-040
- Using noise scale 0.1 with 100 designed sequences raised the scTM designability to 84% of samples. (Yim et al., 2023) `ev:measured` p. 8 ^yim2023se-041
- The same setting reached 40% of samples under the more stringent scRMSD designability criterion of 2. (Yim et al., 2023) `ev:measured` p. 8 ^yim2023se-042
- With 100 sampling steps, generating a 100 amino acid backbone takes 4.4 seconds on an A100 GPU. (Yim et al., 2023) `ev:measured` p. 8 ^yim2023se-043
- Watson et al. report 150 seconds, 34-fold slower, for 100 amino acid backbones on an A4000 GPU. (Yim et al., 2023) `ev:cited` p. 8 ^yim2023se-044
- FrameDiff is able to generate designable samples without any pretraining on protein structure prediction networks. (Yim et al., 2023) `ev:measured` p. 8 ^yim2023se-045
- RFdiffusion demonstrated the capacity to generate designable sequences only when it was initialized with pre-trained weights. (Yim et al., 2023) `ev:cited` p. 8 ^yim2023se-046
- When used with decreased noise-scale, 75% of samples across a range of lengths were designable by scTM above 0.5. (Yim et al., 2023) `ev:measured` p. 9 ^yim2023se-047
- All prior works reporting this metric not involving pretrained networks have reported below 55% designability. (Yim et al., 2023) `ev:cited` p. 9 ^yim2023se-048
- The authors refrain from making state-of-the-art claims because training and evaluation differ across the compared methods. (Yim et al., 2023) `ev:asserted` p. 9 ^yim2023se-049
- The authors hypothesize that scaling FrameDiff to larger data and improving optimization would deliver designability on par with RFdiffusion. (Yim et al., 2023) `ev:asserted` p. 9 ^yim2023se-050
- For the selected designable and novel samples ESMFold was highly confident, with predicted LDDT above 0.7. (Yim et al., 2023) `ev:measured` p. 9 ^yim2023se-051
- RFdiffusion formulated the same forward diffusion process over SE(3)N but with a squared Frobenius norm rotation loss. (Yim et al., 2023) `ev:cited` p. 10 ^yim2023se-052
- FrameDiff has one quarter of the neural network weights of RFdiffusion, according to the authors comparison. (Yim et al., 2023) `ev:asserted` p. 10 ^yim2023se-053
- The same tools yield an explicit heat kernel for Brownian motion on the group SU(2). (Yim et al., 2023) `ev:computed` p. 23 ^yim2023se-054
- The neural network has 17446190 trainable weights with four layers and 256 dimensional node embeddings. (Yim et al., 2023) `ev:reported` p. 35 ^yim2023se-055
- Replacing the score matching rotation loss with a Frobenius norm loss results in a slight reduction in designability. (Yim et al., 2023) `ev:asserted` p. 35 ^yim2023se-056
- Removing monomers with more than 50% loops using DSSP left 20312 proteins in the training set. (Yim et al., 2023) `ev:reported` p. 35 ^yim2023se-057
- Reliably achieving designability of scRMSD below 2 past length 400 is only reported by RFdiffusion. (Yim et al., 2023) `ev:cited` p. 37 ^yim2023se-058
- Longer backbones past length 400 tend to be mostly helical among the samples analyzed across lengths. (Yim et al., 2023) `ev:measured` p. 37 ^yim2023se-059
- Under the FoldingDiff evaluation code FrameDiff reached 60% scTM designability against 6% for the FoldingDiff model. (Yim et al., 2023) `ev:measured` p. 38 ^yim2023se-060
- The increase from 49% to 60% designability is due to switching to alpha carbon only ProteinMPNN. (Yim et al., 2023) `ev:asserted` p. 38 ^yim2023se-061

## 🎯 Contributions

## 📖 Glossary
- **Frame** — a rigid transformation in SE(3) placing one residue backbone atoms in space.
- **SE(3)** — the group of orientation preserving rigid motions, rotations combined with translations, in three dimensions.
- **IGSO3** — the transition density of Brownian motion on SO(3), a series in the rotation angle.
- **Denoising score matching** — training objective regressing a network onto the conditional score of the forward process.
- **Designability** — whether some amino acid sequence folds back to the generated backbone structure.
- **scTM / scRMSD** — self-consistency TM-score and alpha carbon RMSD between sampled and refolded backbones.
- **pdbTM** — highest TM-score of a sample against any chain in the Protein Data Bank.
- **Invariant Point Attention** — the AlphaFold2 attention module operating equivariantly on residue frames and coordinates.
- **Self-conditioning** — feeding the model own previous prediction back as an input feature during sampling.

## ❓ Open questions
- How can scRMSD designability past length 400 be improved without pretraining on structure prediction?
- How can diversity and designability be improved jointly rather than traded off through the noise scale?
- Would training on complexes and larger networks close the remaining gap to RFdiffusion?
- What does a hyperparameter search over the schedules, weights and architecture yield, which the authors leave to future work?
- Can FrameDiff be extended to conditional tasks such as motif scaffolding and probabilistic sequence-to-structure prediction?
- Do the generated novel backbones hold up under experimental characterization, which the paper does not attempt?
- How well do the Lie group results transfer to other domains named by the authors, such as robotics and lattice QCD?

## 📝 Notes on reading
The version read is the arXiv preprint 2302.02277v3, dated 22 May 2023, which also carries the ICML 2023 proceedings header.

Table 2 (ablations, p. 8) is garbled by the extraction: the five column headers (self-conditioning, L2D, Lbb, Ldsm, LF) and the check marks arrive as one flat list, so individual rows cannot be bound to the percentages 39%, 42%, 22%, 16% and 0%. Only the text statement that the best model incorporates all components was claimed, plus App. I.5 on the Frobenius loss.

Internal inconsistency on training time: p. 7 says the model was trained for one week on two A100 GPUs, while App. J.1 (p. 36) says the network was trained over a period of 2 weeks on two A100 GPUs. The claim follows p. 7.

Figures 1 to 7 are images; only their captions are in the cached text, so nothing beyond caption statements was claimed. Equations, algorithm listings and the Rodrigues-formula appendices (Apps. B to H) come through with broken line wrapping and symbols, so their intermediate steps were not claimed; only the proposition statements were.

Table 3 (p. 38) lists RFdiffusion noise scales 0.0, 0.5, 1.0 and FrameDiff noise scales 0.1, 0.5, 1.0 above six unlabeled value columns per row, so no individual diversity cell was claimed; only the surrounding text statements were.

## Suggested new concepts
- SE(3) diffusion — the family of diffusion models on rigid motions this paper puts on a principled footing.
- IGSO3 distribution — the SO(3) Brownian transition density reused across rotation diffusion models.
- Designability (self-consistency evaluation) — the design-fold-compare protocol that every backbone generator is scored by.
- Frame-based backbone parameterization — the AlphaFold2 representation of residues as elements of SE(3).
- Center-of-mass-free diffusion — the centering trick that buys translation invariance in generative models over point sets.
- Self-conditioning — the diffusion sampling technique feeding earlier predictions back into the network.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H2.** Receta de referencia para difundir poses rígidas en SE(3) con ruido IGSO(3) y score cerrada en so(3), trasladable a poses de pinza.

<!-- ingest-checker dropped 2 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
