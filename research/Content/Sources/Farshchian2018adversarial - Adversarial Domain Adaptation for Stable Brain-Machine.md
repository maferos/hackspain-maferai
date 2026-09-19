---
aliases: []
type: "source"
title: "Adversarial Domain Adaptation for Stable Brain-Machine Interfaces"
citekey: "Farshchian2018adversarial"
doi: "10.48550/arXiv.1810.00045"
arxiv: "1810.00045"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1810.00045"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Ali Farshchian", "Juan A. Gallego", "Joseph P. Cohen", "Yoshua Bengio", "Lee E. Miller", "Sara A. Solla"]
sha256: ["d4ac216f387209178af3ed577bbf1e87ef544470498718262162e06786dfaef5"]
pdf: "Content/Papers/Farshchian2018adversarial.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 59
---

📄 PDF: [[Farshchian2018adversarial.pdf]]

> [!abstract] One-sentence summary
> The paper stabilizes a fixed, day-0-trained neural-to-EMG brain-machine interface by aligning later-day neural data, and shows that an adversarial network matching reconstruction-residual distributions outperforms latent-space CCA and KL alignment while needing about a minute of data.

## Abstract

Brain-Machine Interfaces (BMIs) have recently emerged as a clinically viable option to restore voluntary movements after paralysis. These devices are based on the ability to extract information about movement intent from neural signals recorded using multi-electrode arrays chronically implanted in the motor cortices of the brain. However, the inherent loss and turnover of recorded neurons requires repeated recalibrations of the interface, which can potentially alter the day-to-day user experience. The resulting need for continued user adaptation interferes with the natural, subconscious use of the BMI. Here, we introduce a new computational approach that decodes movement intent from a low-dimensional latent representation of the neural data. We implement various domain adaptation methods to stabilize the interface over significantly long times. This includes Canonical Correlation Analysis used to align the latent variables across days; this method requires prior point-to-point correspondence of the time series across domains. Alternatively, we match the empirical probability distributions of the latent variables across days through the minimization of their Kullback-Leibler divergence. These two methods provide a significant and comparable improvement in the performance of the interface. However, implementation of an Adversarial Domain Adaptation Network trained to match the empirical probability distribution of the residuals of the reconstructed neural signals outperforms the two methods based on latent variables, while requiring remarkably few data points to solve the domain adaptation problem. (arXiv)

## 🧠 Key ideas (atomic)

- Over 50% of respondents with a C1-C4 spinal cord injury would be willing to undergo brain surgery to restore grasp. (Farshchian et al., 2018) `ev:cited` p. 1 ^farshchian2018adversarial-001
- Turnover of neurons recorded by chronically implanted multi-electrode arrays is estimated to be on the order of 40% over two weeks. (Farshchian et al., 2018) `ev:cited` p. 1 ^farshchian2018adversarial-002
- Daily retraining can maintain BMI performance but is not viable, as it requires the user to keep adapting to a new interface. (Farshchian et al., 2018) `ev:cited` p. 1 ^farshchian2018adversarial-003
- High correlation across M1 neural signals implies the underlying motor command has much lower dimensionality than the number of recorded M1 neurons. (Farshchian et al., 2018) `ev:cited` p. 1 ^farshchian2018adversarial-004
- Sussillo et al. trained the interface with data volumes collected over several months to achieve robustness against future neural recording changes. (Farshchian et al., 2018) `ev:cited` p. 2 ^farshchian2018adversarial-005
- Dyer et al. aligned the PDF of newly predicted movements to a previously established PDF of typical movements. (Farshchian et al., 2018) `ev:cited` p. 2 ^farshchian2018adversarial-006
- Kao et al. used [[Neural population dynamics|past population dynamics]] to partially stabilize a BMI under severe loss of recorded neurons. (Farshchian et al., 2018) `ev:cited` p. 2 ^farshchian2018adversarial-007
- Pandarinath et al. extracted a single latent space from neural recordings concatenated over five months, supporting reliable kinematic prediction across sessions. (Farshchian et al., 2018) `ev:cited` p. 2 ^farshchian2018adversarial-008
- The authors develop an architecture that simultaneously trains a deep nonlinear autoencoder on M1 signals and a network predicting movement intent from its latents. (Farshchian et al., 2018) `ev:asserted` p. 2 ^farshchian2018adversarial-009
- The Adversarial Domain Adaptation Network aligns the PDF of reconstruction residuals on a later day to the PDF of the day the BMI was calculated. (Farshchian et al., 2018) `ev:asserted` p. 2 ^farshchian2018adversarial-010
- The authors expect this strategy to alleviate the user's cognitive burden, as users would no longer need to learn novel compensation strategies. (Farshchian et al., 2018) `ev:asserted` p. 2 ^farshchian2018adversarial-011
- A male rhesus monkey generated isometric torques to control a cursor in a 2D center-out task with eight peripheral targets. (Farshchian et al., 2018) `ev:reported` p. 2 ^farshchian2018adversarial-012
- A 96-channel microelectrode array was implanted into the hand area of primary motor cortex to record neural activity. (Farshchian et al., 2018) `ev:reported` p. 3 ^farshchian2018adversarial-013
- Electrodes were implanted in 14 muscles of the forearm and hand to record electromyograms quantifying each muscle's activity. (Farshchian et al., 2018) `ev:reported` p. 3 ^farshchian2018adversarial-014
- Data for the study were collected from this single monkey in five experimental sessions spanning 16 days. (Farshchian et al., 2018) `ev:reported` p. 3 ^farshchian2018adversarial-015
- The autoencoder is a fully connected network with an input layer, five hidden layers, and an output layer minimizing reconstruction MSE. (Farshchian et al., 2018) `ev:reported` p. 3 ^farshchian2018adversarial-016
- Hidden units outside the latent and output layers implement a linear readout followed by an exponential nonlinearity. (Farshchian et al., 2018) `ev:reported` p. 3 ^farshchian2018adversarial-017
- Neural spikes are binned at 50 ms intervals and smoothed with a Gaussian filter of 125 ms standard deviation to obtain firing rates. (Farshchian et al., 2018) `ev:reported` p. 3 ^farshchian2018adversarial-018
- The latent activity is mapped onto the EMGs through an LSTM layer with m units followed by a linear layer. (Farshchian et al., 2018) `ev:reported` p. 3 ^farshchian2018adversarial-019
- The training loss sums the firing-rate reconstruction MSE, weighted by a factor lambda, and the MSE of the EMG predictions. (Farshchian et al., 2018) `ev:reported` p. 3 ^farshchian2018adversarial-020
- Lambda is recomputed each training iteration as the ratio of EMG loss to reconstruction loss from the preceding iteration. (Farshchian et al., 2018) `ev:reported` p. 3 ^farshchian2018adversarial-021
- After training on the day-0 recording session, the weights of the neural AE and EMG predictor remain fixed. (Farshchian et al., 2018) `ev:reported` p. 3 ^farshchian2018adversarial-022
- CCA aligns day-k latent activity to day-0 using matrices built by concatenating averaged latent activities for each of the eight targets. (Farshchian et al., 2018) `ev:reported` p. 4 ^farshchian2018adversarial-023
- CCA requires a one-to-one correspondence between data points, restricting its application to neural data that can be matched in time across days. (Farshchian et al., 2018) `ev:asserted` p. 4 ^farshchian2018adversarial-024
- The authors argue that in real-life scenarios unstructured motor behavior interferes with establishing the correspondence CCA needs. (Farshchian et al., 2018) `ev:asserted` p. 5 ^farshchian2018adversarial-025
- KLDM approximates the day-0 and day-k latent distributions as multivariate Gaussians and minimizes the KL divergence between them. (Farshchian et al., 2018) `ev:reported` p. 5 ^farshchian2018adversarial-026
- The KLDM network shares the encoder architecture of the BMI autoencoder and is initialized with its day-0 trained weights. (Farshchian et al., 2018) `ev:reported` p. 5 ^farshchian2018adversarial-027
- KLDM aligns the latent PDFs through a translation matching the means and a rotation matching covariance eigenvectors. (Farshchian et al., 2018) `ev:asserted` p. 5 ^farshchian2018adversarial-028
- An alternative BMI replaced the AE with a Variational AE to improve on the Gaussian assumption for latent variables. (Farshchian et al., 2018) `ev:reported` p. 5 ^farshchian2018adversarial-029
- The ADAN discriminator is an autoencoder with the BMI architecture, initialized with the BMI autoencoder weights trained on day-0 data. (Farshchian et al., 2018) `ev:reported` p. 5 ^farshchian2018adversarial-030
- The ADAN aligner has one exponential hidden layer and a linear readout layer, each with n fully connected units. (Farshchian et al., 2018) `ev:reported` p. 5 ^farshchian2018adversarial-031
- The aligner weights, the n by n input-to-hidden and hidden-to-output connectivity matrices, are initialized as identity matrices. (Farshchian et al., 2018) `ev:reported` p. 5 ^farshchian2018adversarial-032
- Scalar reconstruction losses are obtained by taking the L1 norm of each column of the residual matrix. (Farshchian et al., 2018) `ev:reported` p. 6 ^farshchian2018adversarial-033
- ADAN measures dissimilarity between residual loss distributions by the absolute difference of their means, a lower bound on the Wasserstein distance. (Farshchian et al., 2018) `ev:reported` p. 6 ^farshchian2018adversarial-034
- In the reported results the interface compressed firing rates from 96 channels into 10 latent variables. (Farshchian et al., 2018) `ev:reported` p. 6 ^farshchian2018adversarial-035
- Interface performance was quantified as percentage of variance accounted for in EMG predictions on five-fold cross-validated data. (Farshchian et al., 2018) `ev:reported` p. 6 ^farshchian2018adversarial-036
- The sequentially trained interface performed worse than an EMG predictor trained directly on neural activity, a small but significant difference (p=0.006). (Farshchian et al., 2018) `ev:measured` p. 6 ^farshchian2018adversarial-037
- With simultaneous training, EMG predictions from latent variables showed no significant difference from those from full neural activity (p=0.971). (Farshchian et al., 2018) `ev:measured` p. 6 ^farshchian2018adversarial-038
- The authors conclude that supervising dimensionality reduction with movement information yields latents that better capture movement-related neural variability. (Farshchian et al., 2018) `ev:asserted` p. 6 ^farshchian2018adversarial-039
- Day-16 and day-0 latent trajectories differed by transformations including nonuniform rotation, scaling, and skewing, reflecting turnover in recorded neurons. (Farshchian et al., 2018) `ev:measured` p. 6 ^farshchian2018adversarial-040
- Despite these complex transformations, point-to-point correspondence along the trajectories allowed CCA to achieve a good alignment. (Farshchian et al., 2018) `ev:measured` p. 6 ^farshchian2018adversarial-041
- The ADAN aligner maps day-k neural activity toward day-0, and this aligned activity is then fed to the fixed BMI. (Farshchian et al., 2018) `ev:reported` p. 7 ^farshchian2018adversarial-042
- A within-day interface updated each day provides an upper bound for the potential benefits of neural domain adaptation. (Farshchian et al., 2018) `ev:asserted` p. 7 ^farshchian2018adversarial-043
- A fixed interface without domain adaptation showed a natural deterioration in performance as neural recordings gradually deteriorated. (Farshchian et al., 2018) `ev:measured` p. 8 ^farshchian2018adversarial-044
- CCA and KLDM gave comparable improvements in the performance of the fixed interface across days. (Farshchian et al., 2018) `ev:measured` p. 8 ^farshchian2018adversarial-045
- Using ADAN directly for latent space alignment did not produce better results than CCA or KLDM. (Farshchian et al., 2018) `ev:measured` p. 8 ^farshchian2018adversarial-046
- The authors attribute ADAN's better alignment to residuals amplifying the mismatch that arises when the fixed day-0 AE meets later data. (Farshchian et al., 2018) `ev:asserted` p. 8 ^farshchian2018adversarial-047
- On day-16, ADAN improved over its competitors by about 6%, small but statistically significant (one-way ANOVA with Tukey's test, p < 0.01). (Farshchian et al., 2018) `ev:measured` p. 8 ^farshchian2018adversarial-048
- The authors report being unable to reach this degree of improvement with any of the many other domain adaptation approaches they tried. (Farshchian et al., 2018) `ev:asserted` p. 8 ^farshchian2018adversarial-049
- The data-requirement analysis added 6s of data, 120 samples, per step and averaged improvement over whole 20 min days after day-0. (Farshchian et al., 2018) `ev:reported` p. 8 ^farshchian2018adversarial-050
- With ADAN, EMG prediction accuracy saturates at ∼1 min of training data for domain adaptation. (Farshchian et al., 2018) `ev:measured` p. 8 ^farshchian2018adversarial-051
- The authors consider the need for such a small training set ideal for practical applications. (Farshchian et al., 2018) `ev:asserted` p. 8 ^farshchian2018adversarial-052
- The authors state that ADAN solves domain adaptation in a way that is not task specific and is potentially applicable to unconstrained movements. (Farshchian et al., 2018) `ev:asserted` p. 9 ^farshchian2018adversarial-053
- The improvements in interface stability reported in this paper were obtained offline, without a user in the loop. (Farshchian et al., 2018) `ev:reported` p. 9 ^farshchian2018adversarial-054
- The authors note that online, closed-loop BMI performance is not particularly well correlated with offline decoding accuracy. (Farshchian et al., 2018) `ev:asserted` p. 9 ^farshchian2018adversarial-055
- Additional open and closed-loop experiments with more animals and tasks are required to fully validate the results. (Farshchian et al., 2018) `ev:asserted` p. 9 ^farshchian2018adversarial-056
- Using a VAE greatly improves the Gaussian nature of the latent variable distribution compared with the standard autoencoder. (Farshchian et al., 2018) `ev:measured` p. 13 ^farshchian2018adversarial-057
- The additional VAE constraint results in a slight deterioration of the BMI's ability to predict EMGs. (Farshchian et al., 2018) `ev:measured` p. 13 ^farshchian2018adversarial-058
- A center-and-scale baseline, T&S, applies a global translation to match means followed by a global scaling to match variances. (Farshchian et al., 2018) `ev:reported` p. 14 ^farshchian2018adversarial-059

## 🎯 Contributions


## 📖 Glossary

- **Brain-machine interface (BMI)** — System decoding movement intent from recorded neural activity into control commands.
- **Domain adaptation** — Aligning data from a shifted distribution so a fixed model still applies.
- **ADAN** — Adversarial Domain Adaptation Network aligning later-day neural data via reconstruction-residual distributions.
- **CCA** — Canonical Correlation Analysis; linear maps maximizing correlation between two paired datasets.
- **KLDM** — Alignment by minimizing KL divergence between Gaussian-approximated latent distributions.
- **%VAF** — Percentage of variance accounted for; accuracy measure for EMG predictions.
- **Neuron turnover** — Change in which neurons an implanted array records over time.
- **EMG** — Electromyogram; recorded electrical activity of a muscle.
- **Reconstruction residual** — Difference between autoencoder input and its reconstructed output.

## ❓ Open questions

- Do the offline stability gains of ADAN carry over to online, closed-loop BMI use?
- Does ADAN generalize to other animals, unstructured tasks and human users beyond one monkey?
- How does ADAN perform over horizons much longer than 16 days?
- Why does ADAN applied directly to the latent space not outperform CCA or KLDM?
- Can the aligner cope with severe channel loss rather than gradual turnover?

## 📝 Notes on reading

Read from arXiv 1810.00045v2 (15 Jan 2019), which carries the ICLR 2019 conference header; the packet identifier is the arXiv DOI. Figures 2B, 4A and 4B are only partially extracted: per-day %VAF values for the fixed, within-day, CCA, KLDM and ADAN interfaces are not readable, so no per-day numbers were claimed; the evaluated day offsets appear to be 0, 1, 3, 4 and 16. Equations 1-3 (joint loss, Gaussian KL divergence, discriminator/aligner losses) are partly garbled in the extraction and were summarized in words. Figure 3 (t-SNE and residual PDFs) and Figure S2 were only described. The abstract speaks of 'significantly long times' while the data span five sessions over 16 days from a single monkey.

## Suggested new concepts

- Adversarial domain adaptation for neural decoders — a recurring approach to recalibration-free BMIs that deserves its own note.
- Neural recording instability — neuron turnover and electrode drift are the core problem motivating decoder alignment methods.
- Latent manifold alignment — CCA- and distribution-based alignment of neural latent spaces across days is a general technique.
- Offline vs closed-loop decoder evaluation — the paper flags weak correlation between offline accuracy and online performance.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** Estabiliza un decodificador de BMI alineando la variedad latente entre días con CCA, KL o redes adversarias, equivalente neuronal de la adaptación sim-to-real.
