---
aliases: []
type: "source"
title: "LFADS - Latent Factor Analysis via Dynamical Systems"
citekey: "Sussillo2016lfads"
doi: "10.48550/arXiv.1608.06315"
arxiv: "1608.06315"
year: 2016
publication_type: "preprint"
url: "https://arxiv.org/abs/1608.06315"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["David Sussillo", "Rafal Jozefowicz", "L. F. Abbott", "Chethan Pandarinath"]
sha256: ["3b2905a690e82bef9ef99b25078b8beef39850a7ea5050e93a5b2e3df645dad1"]
pdf: "Content/Papers/Sussillo2016lfads.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 67
---

📄 PDF: [[Sussillo2016lfads.pdf]]

> [!abstract] One-sentence summary
> LFADS is a sequential variational auto-encoder that infers single-trial latent dynamics, initial conditions and external inputs from neural spike trains, beating GPFA, vLGP and PfLDS on synthetic Lorenz and chaotic-RNN data.

## Abstract

Neuroscience is experiencing a data revolution in which many hundreds or thousands of neurons are recorded simultaneously. Currently, there is little consensus on how such data should be analyzed. Here we introduce LFADS (Latent Factor Analysis via Dynamical Systems), a method to infer latent dynamics from simultaneously recorded, single-trial, high-dimensional neural spiking data. LFADS is a sequential model based on a variational auto-encoder. By making a dynamical systems hypothesis regarding the generation of the observed data, LFADS reduces observed spiking to a set of low-dimensional temporal factors, per-trial initial conditions, and inferred inputs. We compare LFADS to existing methods on synthetic data and show that it significantly out-performs them in inferring neural firing rates and latent dynamics. (arXiv)

## 🧠 Key ideas (atomic)

- LFADS is introduced as a method to infer [[Neural population dynamics|latent dynamics]] from simultaneously recorded, single-trial, high-dimensional neural spiking data. (Sussillo et al., 2016) `ev:asserted` p. 1 ^sussillo2016lfads-001
- LFADS implements the hypothesis that a [[Neural population dynamics|driven nonlinear dynamical system]] provides a reasonable model of many neural processes. (Sussillo et al., 2016) `ev:asserted` p. 2 ^sussillo2016lfads-002
- The primary goal of LFADS is to infer [[Neural population dynamics|smooth dynamics]] from recorded neural spike trains on a single-trial basis. (Sussillo et al., 2016) `ev:asserted` p. 2 ^sussillo2016lfads-003
- Input inference rests on the idea that if a powerful nonlinear dynamical system cannot generate the data, an external perturbation must have occurred. (Sussillo et al., 2016) `ev:asserted` p. 2 ^sussillo2016lfads-004
- LFADS is an instantiation of a variational auto-encoder extended to sequences, following earlier sequential VAE architectures such as DRAW. (Sussillo et al., 2016) `ev:reported` p. 2 ^sussillo2016lfads-005
- LFADS assumes that the observed spikes are samples from a Poisson process with underlying rates constructed from latent factors. (Sussillo et al., 2016) `ev:reported` p. 3 ^sussillo2016lfads-006
- Firing rates are computed from the factors by an affine transformation followed by an exponential nonlinearity. (Sussillo et al., 2016) `ev:reported` p. 3 ^sussillo2016lfads-007
- The low-dimensional factors rest on the observation that [[Intrinsic dimension of neural representations|intrinsic dimensionality of neural recordings]] tends to be far lower than neurons recorded. (Sussillo et al., 2016) `ev:cited` p. 3 ^sussillo2016lfads-008
- The factors are an affine readout of the state of a recurrent nonlinear generator network started from a sampled initial condition. (Sussillo et al., 2016) `ev:reported` p. 3 ^sussillo2016lfads-009
- When an inferred input is included, the stochastic latent variable is expanded to comprise the initial condition plus the per-timestep inputs. (Sussillo et al., 2016) `ev:reported` p. 3 ^sussillo2016lfads-010
- The priors for the initial condition and the inferred inputs are diagonal Gaussian distributions with zero mean and fixed chosen variance. (Sussillo et al., 2016) `ev:reported` p. 3 ^sussillo2016lfads-011
- The authors chose the GRU as the recurrent function for all the networks used within the LFADS model. (Sussillo et al., 2016) `ev:reported` p. 3 ^sussillo2016lfads-012
- The initial-condition encoder runs a recurrent network forward and backward in time, so its output reflects the entire data history. (Sussillo et al., 2016) `ev:reported` p. 4 ^sussillo2016lfads-013
- A controller RNN receives the encoded data plus the previous factors, so it can decide when to intervene in generation. (Sussillo et al., 2016) `ev:reported` p. 4 ^sussillo2016lfads-014
- The controller initial state is defined deterministically by an affine transformation of the encoder output rather than drawn from a distribution. (Sussillo et al., 2016) `ev:reported` p. 4 ^sussillo2016lfads-015
- Information flow from the controller into the generator is limited by a KL divergence regularizer applied to the inferred input. (Sussillo et al., 2016) `ev:reported` p. 6 ^sussillo2016lfads-016
- The dimensionality of the inferred input is also explicitly limited through a hyperparameter to restrict information flow into the generator. (Sussillo et al., 2016) `ev:reported` p. 6 ^sussillo2016lfads-017
- After training, factors, rates and inferred inputs for a trial are obtained by averaging several runs to marginalize the stochastic variables. (Sussillo et al., 2016) `ev:reported` p. 6 ^sussillo2016lfads-018
- Training maximizes a lower bound on the marginal log-likelihood, equal to the Poisson reconstruction log-likelihood minus a KL penalty. (Sussillo et al., 2016) `ev:reported` p. 6 ^sussillo2016lfads-019
- The negative bound is minimized with the reparameterization trick, which back-propagates low-variance, unbiased gradient estimates for end-to-end training. (Sussillo et al., 2016) `ev:reported` p. 7 ^sussillo2016lfads-020
- Prior probabilistic sequential models such as PLDS, GCLDS or PfLDS employ linear Gaussian dynamics with a generalized linear model emission. (Sussillo et al., 2016) `ev:cited` p. 7 ^sussillo2016lfads-021
- The authors suggest that LFADS is likely one of many possible instantiations of a Deep Kalman Filter applied to neural data. (Sussillo et al., 2016) `ev:asserted` p. 7 ^sussillo2016lfads-022
- Inferred inputs in LFADS are analogous to Kalman filter innovations, though not strictly defined as a measurement-minus-readout error. (Sussillo et al., 2016) `ev:asserted` p. 7 ^sussillo2016lfads-023
- LFADS was compared against three existing methods, GPFA, vLGP and PfLDS, on synthetic spike trains generated from two deterministic nonlinear systems. (Sussillo et al., 2016) `ev:reported` p. 7 ^sussillo2016lfads-024
- The Lorenz simulation used standard parameters σ = 10, ρ = 28, β = 8/3, with Euler integration at ∆t = 0.006. (Sussillo et al., 2016) `ev:reported` p. 8 ^sussillo2016lfads-025
- The synthetic Lorenz dataset consisted of 65 conditions with 20 trials per condition, each condition run for 1s. (Sussillo et al., 2016) `ev:reported` p. 8 ^sussillo2016lfads-026
- Models were trained on 80% of the Lorenz data, 16 trials per condition, with the remaining 20% held out. (Sussillo et al., 2016) `ev:reported` p. 8 ^sussillo2016lfads-027
- To make the Lorenz dataset more challenging, the authors limited observations to 30 simulated neurons instead of 50 used previously. (Sussillo et al., 2016) `ev:reported` p. 8 ^sussillo2016lfads-028
- The Lorenz baseline firing rate was decreased from 15 spikes/sec to 5 spikes/sec relative to the earlier vLGP setup. (Sussillo et al., 2016) `ev:reported` p. 8 ^sussillo2016lfads-029
- The Lorenz dynamics were sped up by a factor of 4 relative to the earlier vLGP simulation of the same system. (Sussillo et al., 2016) `ev:reported` p. 8 ^sussillo2016lfads-030
- On the Lorenz task, LFADS reached R2 values of 0.826, 0.900 and 0.821 on the three latent dimensions. (Sussillo et al., 2016) `ev:measured` p. 9 ^sussillo2016lfads-031
- For the third Lorenz dimension, R2 was 0.015 for vLGP, 0.325 for GPFA, 0.368 for PfLDS, against 0.821 for LFADS. (Sussillo et al., 2016) `ev:measured` p. 9 ^sussillo2016lfads-032
- On the second Lorenz dimension, PfLDS achieved an R2 of 0.732 and GPFA 0.725, compared with 0.900 for LFADS. (Sussillo et al., 2016) `ev:measured` p. 9 ^sussillo2016lfads-033
- The chaotic data RNN used N = 50 units, τ = 0.025 s, γ = 2.5, with Euler integration at ∆t = 0.001 s. (Sussillo et al., 2016) `ev:reported` p. 9 ^sussillo2016lfads-034
- The data RNN is a vanilla RNN, which does not have the same functional form as the GRU generator used in LFADS. (Sussillo et al., 2016) `ev:reported` p. 9 ^sussillo2016lfads-035
- Data RNN spikes came from a Poisson process with rates from shifted, scaled tanh activity lying between 0 and 30 spikes/s. (Sussillo et al., 2016) `ev:reported` p. 9 ^sussillo2016lfads-036
- The RNN dataset had 400 conditions with 10 spiking trials each, trained on 8 trials per condition, evaluated on 2. (Sussillo et al., 2016) `ev:reported` p. 9 ^sussillo2016lfads-037
- Principal components analysis showed that 20 principal components are sufficient to capture > 95% of the data RNN variance. (Sussillo et al., 2016) `ev:measured` p. 9 ^sussillo2016lfads-038
- The latent space was restricted to 20 dimensions for every tested model, with 20 temporal factors in the LFADS case. (Sussillo et al., 2016) `ev:reported` p. 9 ^sussillo2016lfads-039
- vLGP was excluded from the RNN comparison because its Lorenz results were noticeably worse than those of the other methods. (Sussillo et al., 2016) `ev:reported` p. 9 ^sussillo2016lfads-040
- On held-out RNN data, LFADS yields a better R2 fit than GPFA for every single neuron in the comparison. (Sussillo et al., 2016) `ev:measured` p. 10 ^sussillo2016lfads-041
- On held-out RNN data, LFADS yields a better R2 fit than PfLDS for every single neuron in the comparison. (Sussillo et al., 2016) `ev:measured` p. 10 ^sussillo2016lfads-042
- The authors note that disambiguating dynamics from inputs is ill-posed in general, so they encouraged the dynamics to be simple. (Sussillo et al., 2016) `ev:asserted` p. 9 ^sussillo2016lfads-043
- To test input inference, a delta pulse of magnitude 50 was delivered to the data RNN at a random time between 0.25s and 0.75s. (Sussillo et al., 2016) `ev:reported` p. 11 ^sussillo2016lfads-044
- The LFADS model for the input experiments included an inferred input with a dimensionality of 1. (Sussillo et al., 2016) `ev:reported` p. 11 ^sussillo2016lfads-045
- Inferred inputs were extracted by running the trained LFADS system 512 times for each trial and averaging the results. (Sussillo et al., 2016) `ev:reported` p. 11 ^sussillo2016lfads-046
- For the vast majority of trials, LFADS inferred that there was an input near the time of the actual delta pulse. (Sussillo et al., 2016) `ev:measured` p. 11 ^sussillo2016lfads-047
- LFADS did a better job of inferring inputs with simpler dynamics at γ = 1.5 than with more complex dynamics at γ = 2.5. (Sussillo et al., 2016) `ev:measured` p. 11 ^sussillo2016lfads-048
- The authors attribute part of the γ = 2.5 difficulty to complex dynamics reducing the magnitude of the perturbation caused by the input. (Sussillo et al., 2016) `ev:asserted` p. 11 ^sussillo2016lfads-049
- In the γ = 2.5 case, LFADS used the inferred input more actively, also accounting for the non-input-driven dynamics. (Sussillo et al., 2016) `ev:measured` p. 11 ^sussillo2016lfads-050
- Inferred input strength for autonomous data RNNs was similar to that for pulse-driven data outside the window around the pulse. (Sussillo et al., 2016) `ev:measured` p. 11 ^sussillo2016lfads-051
- When pulses fell within the analysed window, the inferred input magnitude was higher on average than in cases without inputs. (Sussillo et al., 2016) `ev:measured` p. 11 ^sussillo2016lfads-052
- As a reference point for the input-strength analysis, the standard deviation of the Gaussian prior on the inferred input was 0.32. (Sussillo et al., 2016) `ev:reported` p. 13 ^sussillo2016lfads-053
- The authors conclude that LFADS significantly outperforms other state-of-the-art algorithms on the Lorenz and chaotic RNN synthetic examples. (Sussillo et al., 2016) `ev:asserted` p. 11 ^sussillo2016lfads-054
- The authors note that, for studying linear systems, a variety of optimal methods such as the Kalman filter already exist. (Sussillo et al., 2016) `ev:asserted` p. 11 ^sussillo2016lfads-055
- The authors state that the Poisson spiking process is the only explicit aspect of LFADS that ties it to neuroscience. (Sussillo et al., 2016) `ev:asserted` p. 11 ^sussillo2016lfads-056
- Exchanging the Poisson for a Gaussian emission distribution could let LFADS be applied to many kinds of time series data. (Sussillo et al., 2016) `ev:asserted` p. 11 ^sussillo2016lfads-057
- LFADS does not feed sampled spikes back into the generator, since spikes are viewed as noisy observations of a smooth process. (Sussillo et al., 2016) `ev:asserted` p. 14 ^sussillo2016lfads-058
- The authors state that the fastest timescale LFADS can produce is only limited by the binning of the experimental spike counts. (Sussillo et al., 2016) `ev:asserted` p. 14 ^sussillo2016lfads-059
- Spiky rates with high-frequency changes that do not generalize to held-out data are described as a clear sign of LFADS overfitting. (Sussillo et al., 2016) `ev:asserted` p. 14 ^sussillo2016lfads-060
- In this contribution LFADS is implemented as a smoother, in Kalman filter language, that cannot run in real time. (Sussillo et al., 2016) `ev:reported` p. 14 ^sussillo2016lfads-061
- The authors propose an emissions model for calcium imaging as an extremely useful extension for inferring [[Neural population dynamics|underlying firing rate dynamics]]. (Sussillo et al., 2016) `ev:asserted` p. 14 ^sussillo2016lfads-062
- The authors propose learning the inferred-input and factor dimensions automatically instead of specifying them as predetermined hyper-parameters. (Sussillo et al., 2016) `ev:asserted` p. 14 ^sussillo2016lfads-063
- The prior variance for the initial condition and inferred inputs was set to 0.1, chosen to avoid saturating network nonlinearities. (Sussillo et al., 2016) `ev:reported` p. 15 ^sussillo2016lfads-064
- A schedule on the KL divergence penalty was added so that the optimization does not quickly set the KL divergence to 0. (Sussillo et al., 2016) `ev:reported` p. 15 ^sussillo2016lfads-065
- An L2 penalty on the recurrent weights of the generator was added to encourage simple dynamics. (Sussillo et al., 2016) `ev:reported` p. 15 ^sussillo2016lfads-066
- Dropout layers were added to the inputs and to a few feed-forward connections to help avoid over-fitting. (Sussillo et al., 2016) `ev:reported` p. 15 ^sussillo2016lfads-067

## 🎯 Contributions


## 📖 Glossary

- **LFADS** — Latent Factor Analysis via Dynamical Systems; a sequential VAE for single-trial neural population dynamics.
- **Variational auto-encoder (VAE)** — Generative model trained by maximizing an evidence lower bound with an encoder approximating the posterior.
- **Generator** — The GRU decoder RNN whose state produces factors, rates and Poisson spikes.
- **Controller** — RNN that reads encoded data and current factors to emit inferred inputs to the generator.
- **Inferred input** — Stochastic per-timestep latent perturbation explaining data the autonomous generator cannot produce.
- **Temporal factors** — Low-dimensional affine readout of the generator state from which firing rates are computed.
- **PSTH** — Peri-stimulus time histogram; trial-averaged firing rate of a single neuron over time.
- **GPFA** — Gaussian-process factor analysis; smooths neural population data with Gaussian process latents.
- **PfLDS** — Poisson linear dynamical system with a nonlinear feed-forward network before the emission GLM.
- **vLGP** — Variational latent Gaussian process for recovering single-trial dynamics from spike trains.
- **Reparameterization trick** — Writing samples as deterministic functions of noise so gradients pass through sampling.

## ❓ Open questions

- How does LFADS perform on real neural recordings rather than the synthetic Lorenz and chaotic-RNN datasets tested here?
- How can inferred inputs be reliably separated from dynamics when the generating system is highly chaotic?
- Can the inferred-input and factor dimensionalities be learned automatically, for example through nuclear norm minimization?
- Can LFADS be adapted into a causal filter that runs in real time?
- What emission model would let LFADS infer firing rates from calcium imaging signals?
- How should regularizers on dynamics versus inputs be weighted for motor versus sensory-driven tasks?

## 📝 Notes on reading

Version read: arXiv 1608.06315v1 (22 Aug 2016), matching the packet identifier.

Figures 1 and 2 are architecture diagrams (generator; full inference model with encoder, controller and generator) whose extracted text is fragmentary. Figures 3–6 show example Lorenz and data-RNN trials and inferred traces, described only. Figure 7 is a per-neuron R2 scatter (LFADS vs GPFA, LFADS vs PfLDS); no numeric values are extractable, only the stated result that LFADS is better for every neuron. Figure 10 plots inferred against actual pulse times; Figure 11 plots inferred input RMS strength over time for the four data RNNs; their values were not claimed.

The prior standard deviation of 0.32 given for Fig. 11 is consistent with the Appendix prior variance of 0.1. All results are on synthetic data; the paper reports no real neural recordings. The equations were partially garbled by extraction but the model description in the text was sufficient.

## Suggested new concepts

- Sequential variational auto-encoder — the model class LFADS instantiates, relevant to other latent dynamics models.
- Latent dynamics inference from neural population data — the shared problem addressed by LFADS, GPFA, PfLDS and vLGP.
- Inferred inputs versus autonomous dynamics — the identifiability problem of separating external perturbations from intrinsic dynamics.
- Neural population dynamics — the dynamical-systems view of computation motivating LFADS.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** VAE secuencial que infiere la dinámica latente de poblaciones motoras durante el alcance y sirve de plantilla para modelos de dinámica latente del robot.
