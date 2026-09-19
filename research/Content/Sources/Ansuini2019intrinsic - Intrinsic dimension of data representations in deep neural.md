---
aliases: []
type: "source"
title: "Intrinsic dimension of data representations in deep neural networks"
citekey: "Ansuini2019intrinsic"
doi: "10.48550/arXiv.1905.12784"
arxiv: "1905.12784"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1905.12784"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Alessio Ansuini", "Alessandro Laio", "Jakob H. Macke", "Davide Zoccolan"]
sha256: ["df8926979c09b4cf8d7a20f95984e2b323bd55381580dbd9f9eb74fc3b91b6a4"]
pdf: "Content/Papers/Ansuini2019intrinsic.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 59
---

📄 PDF: [[Ansuini2019intrinsic.pdf]]

> [!abstract] One-sentence summary
> Using the TwoNN estimator across 14 ImageNet CNNs and small MNIST and CIFAR-10 networks, the paper shows that representations lie on low-dimensional curved manifolds whose ID rises then falls across layers, with the last-hidden-layer ID predicting test accuracy.

## Abstract

Deep neural networks progressively transform their inputs across multiple processing layers. What are the geometrical properties of the representations learned by these networks? Here we study the intrinsic dimensionality (ID) of data-representations, i.e. the minimal number of parameters needed to describe a representation. We find that, in a trained network, the ID is orders of magnitude smaller than the number of units in each layer. Across layers, the ID first increases and then progressively decreases in the final layers. Remarkably, the ID of the last hidden layer predicts classification accuracy on the test set. These results can neither be found by linear dimensionality estimates (e.g., with principal component analysis), nor in representations that had been artificially linearized. They are neither found in untrained networks, nor in networks that are trained on randomized labels. This suggests that neural networks that can generalize are those that transform the data into low-dimensional, but not necessarily flat manifolds. (arXiv)

## 🧠 Key ideas (atomic)

- The paper studies how the [[Intrinsic dimension of neural representations|intrinsic dimension of data representations]] varies across the layers of convolutional networks trained for image classification (Ansuini et al., 2019) `ev:reported` p. 2 ^ansuini2019intrinsic-001
- Intrinsic dimension is estimated with [[TwoNN estimator|TwoNN]], a global estimator based on the ratio of second to first nearest-neighbour distances (Ansuini et al., 2019) `ev:reported` p. 3 ^ansuini2019intrinsic-002
- According to the authors, [[TwoNN estimator|TwoNN]] can be applied even when the data manifold is curved, topologically complex and sampled non-uniformly (Ansuini et al., 2019) `ev:asserted` p. 2 ^ansuini2019intrinsic-003
- Under [[TwoNN estimator|TwoNN]], the ratio of second to first neighbour distances follows a Pareto distribution with parameter d + 1 (Ansuini et al., 2019) `ev:cited` p. 3 ^ansuini2019intrinsic-004
- For finite samples, [[TwoNN estimator|TwoNN]] moderately underestimates IDs larger than ∼20, especially when the density of the data is non-uniform (Ansuini et al., 2019) `ev:cited` p. 3 ^ansuini2019intrinsic-005
- The authors state that the reported ID values larger than ∼20 in their figures should be considered lower bounds (Ansuini et al., 2019) `ev:asserted` p. 3 ^ansuini2019intrinsic-006
- Estimator reliability was checked by decimating the dataset and testing whether the estimated ID stays approximately scale invariant (Ansuini et al., 2019) `ev:reported` p. 3 ^ansuini2019intrinsic-007
- Tests on artificial data of known ID embedded in a 100,000 dimensional space showed no significant degradation of estimator accuracy (Ansuini et al., 2019) `ev:measured` p. 3 ^ansuini2019intrinsic-008
- Representations were extracted at pooling layers after convolutions, at fully connected layers, and after each ResNet block (Ansuini et al., 2019) `ev:reported` p. 3 ^ansuini2019intrinsic-009
- The code computing TwoNN ID estimates and reproducing the experiments is available in the github.com/ansuini/IntrinsicDimDeep repository (Ansuini et al., 2019) `ev:reported` p. 3 ^ansuini2019intrinsic-010
- A VGG-16 pre-trained on ImageNet was fine-tuned on a synthetic dataset of 1440 images of 40 objects in 36 views (Ansuini et al., 2019) `ev:reported` p. 4 ^ansuini2019intrinsic-011
- In VGG-16-R the ID increased in the first pooling layer, then decreased monotonically, reaching very low values in the final hidden layers (Ansuini et al., 2019) `ev:measured` p. 4 ^ansuini2019intrinsic-012
- In the pool4 layer of VGG-16-R the estimated ID was ≈19, far below the embedding dimension of that layer (Ansuini et al., 2019) `ev:measured` p. 4 ^ansuini2019intrinsic-013
- Subsampling analysis showed that the estimated IDs of VGG-16-R were stable across a wide range of sample sizes (Ansuini et al., 2019) `ev:measured` p. 4 ^ansuini2019intrinsic-014
- For pre-trained ImageNet networks, the average ID of the 7 biggest category manifolds was computed using 500 images per category (Ansuini et al., 2019) `ev:reported` p. 4 ^ansuini2019intrinsic-015
- Across AlexNet, VGG and ResNet networks, the ID initially grew, reached a peak or plateau, then progressively decreased toward its final value (Ansuini et al., 2019) `ev:measured` p. 4 ^ansuini2019intrinsic-016
- Across the pre-trained networks, the ID in the output layer was the smallest, often assuming a value of the order of ten (Ansuini et al., 2019) `ev:measured` p. 4 ^ansuini2019intrinsic-017
- The authors argue that a binary-code bound implies an output-layer ID of roughly 10 or more for the ∼1000 ImageNet categories (Ansuini et al., 2019) `ev:asserted` p. 4 ^ansuini2019intrinsic-018
- Plotted against relative depth, the [[Intrinsic dimension of neural representations|ID profiles]] of 14 models approximately collapsed onto a common hunchback shape (Ansuini et al., 2019) `ev:measured` p. 4 ^ansuini2019intrinsic-019
- In the VGG and ResNet families the ID reached similar peak values between 100 and 120 at relative depth 0.2-0.4 (Ansuini et al., 2019) `ev:measured` p. 5 ^ansuini2019intrinsic-020
- AlexNet and a small network trained on MNIST are stated exceptions to the common hunchback shape of the ID profiles (Ansuini et al., 2019) `ev:measured` p. 5 ^ansuini2019intrinsic-021
- In all the pre-trained networks studied, the ID eventually converged to small values in the last hidden layer (Ansuini et al., 2019) `ev:measured` p. 5 ^ansuini2019intrinsic-022
- The authors speculate that progressive reduction of [[Intrinsic dimension of neural representations|manifold dimensionality]] could be a feature that allows deep networks to generalize well (Ansuini et al., 2019) `ev:asserted` p. 5 ^ansuini2019intrinsic-023
- Last-hidden-layer IDs on ImageNet training images ranged from ≈12 for ResNet152 to ≈25 for AlexNet (Ansuini et al., 2019) `ev:measured` p. 5 ^ansuini2019intrinsic-024
- In the last hidden layer the embedding dimension was between 1 and 2 orders of magnitude larger than the ID (Ansuini et al., 2019) `ev:measured` p. 5 ^ansuini2019intrinsic-025
- The [[Intrinsic dimension of neural representations|training-set ID]] in the last hidden layer predicted top 5-score test performance across networks, with Pearson correlation r = 0.94 (Ansuini et al., 2019) `ev:measured` p. 5 ^ansuini2019intrinsic-026
- Within the ResNet class, the correlation between last-hidden-layer ID and test performance reached r = 0.99 (Ansuini et al., 2019) `ev:measured` p. 5 ^ansuini2019intrinsic-027
- The authors suggest the last-hidden-layer ID can serve as a proxy for generalization without an external validation set (Ansuini et al., 2019) `ev:asserted` p. 6 ^ansuini2019intrinsic-028
- PCA on the normalized covariance matrix showed no clear gap in the eigenvalue spectrum of the layer representations (Ansuini et al., 2019) `ev:measured` p. 6 ^ansuini2019intrinsic-029
- PC-ID, the number of components describing 90% of the variance, was about one or two orders of magnitude larger than the [[TwoNN estimator|TwoNN]] ID (Ansuini et al., 2019) `ev:measured` p. 6 ^ansuini2019intrinsic-030
- In the last hidden layer of VGG-16 the PC-ID was ≈200, while the ID estimated with TwoNN was ≈18 (Ansuini et al., 2019) `ev:measured` p. 6 ^ansuini2019intrinsic-031
- A synthetic Gaussian dataset with the same second-order moments had an ID two orders of magnitude larger, which grew with sample size (Ansuini et al., 2019) `ev:measured` p. 6 ^ansuini2019intrinsic-032
- The authors interpret the [[TwoNN estimator|TwoNN]] versus PCA discrepancy as pointing to strong non-linearities in correlations not captured by the covariance matrix (Ansuini et al., 2019) `ev:asserted` p. 6 ^ansuini2019intrinsic-033
- The PC-ID profile across VGG-16 layers was qualitatively the same in randomly initialized and in trained networks (Ansuini et al., 2019) `ev:measured` p. 6 ^ansuini2019intrinsic-034
- With random weights the TwoNN ID profile across VGG-16 layers was remarkably flat, unlike the hunchback profile after training (Ansuini et al., 2019) `ev:measured` p. 6 ^ansuini2019intrinsic-035
- In VGG-16 the ID kept growing after the embedding dimension had already started to substantially decline across layers (Ansuini et al., 2019) `ev:measured` p. 6 ^ansuini2019intrinsic-036
- Training reduced the [[Intrinsic dimension of neural representations|last-hidden-layer ID]] relative to its initial value, whereas the ID of intermediate layers increased by a large amount (Ansuini et al., 2019) `ev:measured` p. 7 ^ansuini2019intrinsic-037
- In a VGG-16 trained on CIFAR-10, the last-hidden-layer ID varied non-monotonically, slowly increasing after an initial drop without substantial overfitting (Ansuini et al., 2019) `ev:measured` p. 7 ^ansuini2019intrinsic-038
- A small network trained on MNIST did not show the initial increase of ID across layers seen in larger networks (Ansuini et al., 2019) `ev:measured` p. 7 ^ansuini2019intrinsic-039
- MNIST⋆ added a luminance perturbation constant within each image but random across images, to test whether irrelevant correlated features drive the ID rise (Ansuini et al., 2019) `ev:reported` p. 7 ^ansuini2019intrinsic-040
- With λ = 100, the luminance perturbation lowered the ID of the MNIST⋆ input representation from ≈13 to ≈3 (Ansuini et al., 2019) `ev:measured` p. 7 ^ansuini2019intrinsic-041
- The small network trained on the luminance-perturbed MNIST⋆ dataset was still able to generalize, with accuracy ≈98% (Ansuini et al., 2019) `ev:measured` p. 7 ^ansuini2019intrinsic-042
- On MNIST⋆ the ID variation across layers showed a hunchback shape reminiscent of the one observed in large architectures (Ansuini et al., 2019) `ev:measured` p. 7 ^ansuini2019intrinsic-043
- The authors suggest the early ID growth is determined by low-level input features that carry no information about the correct labels (Ansuini et al., 2019) `ev:asserted` p. 7 ^ansuini2019intrinsic-044
- Trained on MNIST with randomly shuffled labels, the same small network achieved a training error of zero (Ansuini et al., 2019) `ev:measured` p. 8 ^ansuini2019intrinsic-045
- With shuffled labels the ID grew considerably in the second half of the network, almost saturating the upper bound set by the embedding dimension (Ansuini et al., 2019) `ev:measured` p. 8 ^ansuini2019intrinsic-046
- Following earlier work, the authors suggest a network trained on inconsistent data can be recognized by its ID increasing across final layers (Ansuini et al., 2019) `ev:cited` p. 8 ^ansuini2019intrinsic-047
- The authors claim their study is the first to systematically investigate object-manifold dimensionality in large, state-of-the-art image classification CNNs (Ansuini et al., 2019) `ev:asserted` p. 8 ^ansuini2019intrinsic-048
- The authors note their curved-manifold conclusion is at odds with the unfolding of data manifolds reported for a small network (Ansuini et al., 2019) `ev:cited` p. 9 ^ansuini2019intrinsic-049
- The authors argue that flattening of data manifolds may not be a general computational goal that deep networks strive to achieve (Ansuini et al., 2019) `ev:asserted` p. 9 ^ansuini2019intrinsic-050
- To the authors, [[Intrinsic dimension of neural representations|progressive reduction of the ID]], rather than gradual flattening, seems to be the key to linearly separable representations (Ansuini et al., 2019) `ev:asserted` p. 9 ^ansuini2019intrinsic-051
- All experiments ran in PyTorch 1.0 on a Linux workstation with 64GB of RAM and a GeForce GTX 1080 Ti (Ansuini et al., 2019) `ev:reported` p. 12 ^ansuini2019intrinsic-052
- Fourteen pre-trained torchvision networks were analysed: AlexNet, eight VGG variants with and without batch normalization, and five ResNets (Ansuini et al., 2019) `ev:reported` p. 12 ^ansuini2019intrinsic-053
- VGG-16-R was fine-tuned with SGD with momentum 0.9 and reached ≈88% test accuracy after 15 epochs (Ansuini et al., 2019) `ev:measured` p. 12 ^ansuini2019intrinsic-054
- The small MNIST network had two convolutional layers, two max pooling layers and two fully connected layers with ReLU non-linearities (Ansuini et al., 2019) `ev:reported` p. 12 ^ansuini2019intrinsic-055
- Across 50 trainings of a CIFAR-10 VGG-16 with different random initializations, the last-hidden-layer ID showed no correlation with accuracy (r=-0.003) (Ansuini et al., 2019) `ev:measured` p. 14 ^ansuini2019intrinsic-056
- The authors attribute the missing correlation likely to the little variation in accuracy produced by different random weight initializations (Ansuini et al., 2019) `ev:asserted` p. 14 ^ansuini2019intrinsic-057
- The authors suggest that accuracy differences across well-trained ImageNet networks are mostly due to differences in their architecture (Ansuini et al., 2019) `ev:asserted` p. 14 ^ansuini2019intrinsic-058
- The authors suggest the last-hidden-layer ID is not always a reliable predictor of overfitting onset, which may depend on architecture and data (Ansuini et al., 2019) `ev:asserted` p. 14 ^ansuini2019intrinsic-059

## 🎯 Contributions


## 📖 Glossary

- **Intrinsic dimension (ID)** — minimal number of coordinates needed to describe data points without significant information loss.
- **TwoNN** — global ID estimator using the ratio of second to first nearest-neighbour distances.
- **Embedding dimension (ED)** — number of units in a layer, i.e. the dimension of its activation space.
- **PC-ID** — number of principal components needed to explain 90% of the variance.
- **Hunchback profile** — ID rising in early layers, then decreasing progressively toward the output.
- **Relative depth** — layer depth divided by the total number of layers, excluding batch normalization.

## ❓ Open questions

- Does the last-hidden-layer ID predict accuracy for non-convolutional architectures or non-image tasks?
- Why does the last-hidden-layer ID evolve non-monotonically during training in some architectures but signal overfitting in others?
- How much do TwoNN's lower-bound estimates above ∼20 distort the peak IDs in intermediate layers?
- Is the output-layer ID bound from category count achieved in practice, or only approached?
- Can ID be used as a training signal or model-selection criterion rather than only a diagnostic?

## 📝 Notes on reading

Read the arXiv v2 (28 Oct 2019), the NeurIPS 2019 camera-ready version. Figures 2-6, 8 and 9 were only described from captions and text; their plotted values were not claimed. Several equations and exponents are garbled in the extraction (e.g. the pool4 ED and ratio, the Nc bound on output ID, O(10^4) data with O(10^5) coordinates), so those numbers were not claimed. Internal inconsistencies: the custom dataset is 1440 images on p. 4 and p. 13 but 1400 on p. 12; the fine-tuning split is ≃85% on p. 12 but ≈80% on p. 13 (30 of 36 images per object is ≈83%); ResNet-50 on p. 5 is listed as ResNet 52 on p. 12; the MNIST† curve is orange in the text of p. 8 but red in the Fig. 6 caption; the MNIST network's stride is stated as zero. The pre-trained ImageNet analysis uses the 7 most populated categories, which are mostly dog breeds.

## Suggested new concepts

- Intrinsic dimension of neural representations — a geometric quantity reused across generalization, robustness and compression studies.
- TwoNN estimator — a nearest-neighbour ID estimator that other notes may apply to activations or datasets.
- Representation manifold curvature — distinguishes nonlinear low-dimensional manifolds from flat linear subspaces in network layers.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** Estima con TwoNN la dimensión intrínseca de cada capa y da una herramienta para dimensionar latentes de políticas y codificadores visuales.
