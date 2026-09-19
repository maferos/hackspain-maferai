---
aliases: []
type: "source"
title: "Visualizing the Loss Landscape of Neural Nets"
citekey: "Li2017visualizing"
doi: "10.48550/arXiv.1712.09913"
arxiv: "1712.09913"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1712.09913"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Hao Li", "Zheng Xu", "Gavin Taylor", "Christoph Studer", "Tom Goldstein"]
sha256: ["f1d5a34270925e3915d558594a06626ee62a645a8c8f90d1afb70954157261c6"]
pdf: "Content/Papers/Li2017visualizing.pdf"
topics: ["[[Optimización y algoritmos]]"]
cited_in: ["[[02_optimizacion_y_algoritmos]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[Li2017visualizing.pdf]]

> [!abstract] One-sentence summary
> The paper introduces filter-normalized random-direction plots of neural loss surfaces and uses them to show how depth, skip connections, width, batch size and weight decay shape minimizer sharpness, non-convexity and generalization.

## Abstract

Neural network training relies on our ability to find "good" minimizers of highly non-convex loss functions. It is well-known that certain network architecture designs (e.g., skip connections) produce loss functions that train easier, and well-chosen training parameters (batch size, learning rate, optimizer) produce minimizers that generalize better. However, the reasons for these differences, and their effects on the underlying loss landscape, are not well understood. In this paper, we explore the structure of neural loss functions, and the effect of loss landscapes on generalization, using a range of visualization methods. First, we introduce a simple "filter normalization" method that helps us visualize loss function curvature and make meaningful side-by-side comparisons between loss functions. Then, using a variety of visualizations, we explore how network architecture affects the loss landscape, and how training parameters affect the shape of minimizers. (arXiv)

## 🧠 Key ideas (atomic)

- The paper studies how neural network architecture and training parameters shape loss landscape geometry, using a range of visualization methods. (Li et al., 2017) `ev:asserted` p. 2 ^li2017visualizing-001
- The authors state that studies of neural loss surfaces have remained predominantly theoretical because loss function evaluations are prohibitively costly. (Li et al., 2017) `ev:asserted` p. 1 ^li2017visualizing-002
- The authors report that simple visualization strategies fail to accurately capture the local sharpness or flatness of loss function minimizers. (Li et al., 2017) `ev:asserted` p. 2 ^li2017visualizing-003
- The authors argue that skip connections promote flat minimizers and prevent the transition to chaotic behavior in deep networks. (Li et al., 2017) `ev:asserted` p. 2 ^li2017visualizing-004
- Hochreiter and Schmidhuber defined flatness as the size of the connected region around a minimum where the training loss remains low. (Li et al., 2017) `ev:cited` p. 2 ^li2017visualizing-005
- Prior work showed that quantitative sharpness measures are not invariant to network symmetries, making them insufficient to determine generalization ability. (Li et al., 2017) `ev:cited` p. 3 ^li2017visualizing-006
- The authors argue that non-convexities are difficult to visualize using one-dimensional linear interpolation plots of the loss function. (Li et al., 2017) `ev:asserted` p. 3 ^li2017visualizing-007
- The authors state that 1D interpolation ignores batch normalization and invariance symmetries, so its visual sharpness comparisons may be misleading. (Li et al., 2017) `ev:asserted` p. 3 ^li2017visualizing-008
- ReLU networks are scale invariant: scaling one layer's weights by 10 with the next layer divided by 10 leaves the network unchanged. (Li et al., 2017) `ev:asserted` p. 4 ^li2017visualizing-009
- The authors argue that scale invariance makes apparent differences in random-direction plots an artifact that prevents meaningful comparisons between plots. (Li et al., 2017) `ev:asserted` p. 4 ^li2017visualizing-010
- Filter normalization rescales each filter of a random Gaussian direction to match the Frobenius norm of the corresponding filter in the parameters. (Li et al., 2017) `ev:reported` p. 4 ^li2017visualizing-011
- The sharpness experiments trained a 9-layer VGG network with batch normalization on CIFAR-10 for a fixed number of epochs. (Li et al., 2017) `ev:reported` p. 4 ^li2017visualizing-012
- The large batch size was 8192, equal to 16.4% of the CIFAR-10 training data, compared with a small batch size of 128. (Li et al., 2017) `ev:reported` p. 4 ^li2017visualizing-013
- Without weight decay, 1D interpolation shows the small-batch VGG-9 solution as wider than the sharp large-batch solution. (Li et al., 2017) `ev:measured` p. 5 ^li2017visualizing-014
- With a non-zero weight decay, the large-batch minimizer appears considerably flatter than the small-batch minimizer in 1D interpolation plots. (Li et al., 2017) `ev:measured` p. 5 ^li2017visualizing-015
- Small batches generalized better than large batches in all of the VGG-9 linear interpolation experiments reported in this section. (Li et al., 2017) `ev:measured` p. 5 ^li2017visualizing-016
- The 1D interpolation plots showed no apparent correlation between the sharpness of the minimizers and their generalization. (Li et al., 2017) `ev:measured` p. 5 ^li2017visualizing-017
- Without weight decay, VGG-9 test errors were 7.37% for small-batch training versus 11.07% for large-batch training. (Li et al., 2017) `ev:measured` p. 5 ^li2017visualizing-018
- With weight decay 5e-4, VGG-9 test errors were 6.0% for small-batch training versus 10.19% for large-batch training. (Li et al., 2017) `ev:measured` p. 5 ^li2017visualizing-019
- With zero weight decay, large-batch training produced smaller weights than small-batch training, according to the weight histograms. (Li et al., 2017) `ev:measured` p. 5 ^li2017visualizing-020
- Adding weight decay reversed this effect: the large-batch minimizer then had much larger weights than the small-batch minimizer. (Li et al., 2017) `ev:measured` p. 5 ^li2017visualizing-021
- The authors attribute the scale difference to small batches taking more weight updates per epoch, amplifying the shrinking effect of weight decay. (Li et al., 2017) `ev:asserted` p. 5 ^li2017visualizing-022
- The authors conclude that the 1D interpolation plots visualize irrelevant weight scaling rather than the endogenous sharpness of minimizers. (Li et al., 2017) `ev:asserted` p. 5 ^li2017visualizing-023
- With filter-normalized plots, small-batch and large-batch minima still differ in sharpness, but much more subtly than in un-normalized plots. (Li et al., 2017) `ev:measured` p. 5 ^li2017visualizing-024
- In filter-normalized plots, large batches produced visually sharper minima, although not dramatically so, with higher test error. (Li et al., 2017) `ev:measured` p. 6 ^li2017visualizing-025
- Using filter-normalized plots, the authors find that sharpness correlates well with generalization error across the compared VGG-9 minimizers. (Li et al., 2017) `ev:measured` p. 6 ^li2017visualizing-026
- Architecture experiments used ResNet-20/56/110, versions of them with shortcut connections removed, and Wide-ResNets, all trained on CIFAR-10. (Li et al., 2017) `ev:reported` p. 7 ^li2017visualizing-027
- Models were trained using SGD with Nesterov momentum, batch size 128, and 0.0005 weight decay for 300 epochs. (Li et al., 2017) `ev:reported` p. 7 ^li2017visualizing-028
- Deeper networks without skip connections, such as ResNet-56-noshort, required a smaller initial learning rate of 0.01 instead of 0.1. (Li et al., 2017) `ev:reported` p. 7 ^li2017visualizing-029
- When skip connections are not used, network depth has a dramatic effect on the loss surfaces of the networks studied. (Li et al., 2017) `ev:measured` p. 7 ^li2017visualizing-030
- As depth increases, the loss surface of the networks without skip connections transitions from nearly convex to chaotic. (Li et al., 2017) `ev:measured` p. 7 ^li2017visualizing-031
- ResNet-56-noshort shows dramatic non-convexities with large regions where gradient directions do not point toward the central minimizer. (Li et al., 2017) `ev:measured` p. 7 ^li2017visualizing-032
- ResNet-110-noshort displays even more dramatic non-convexities, becoming extremely steep in all of the directions shown in the plot. (Li et al., 2017) `ev:measured` p. 7 ^li2017visualizing-033
- Residual connections prevent the transition to chaotic loss landscapes as network depth increases in the ResNet experiments. (Li et al., 2017) `ev:measured` p. 7 ^li2017visualizing-034
- With skip connections, the width and shape of the 0.1-level contour is almost identical for the 20- and 110-layer networks. (Li et al., 2017) `ev:measured` p. 7 ^li2017visualizing-035
- For the shallow ResNet-20 and ResNet-20-noshort networks, the effect of skip connections on the landscape is fairly unnoticeable. (Li et al., 2017) `ev:measured` p. 7 ^li2017visualizing-036
- Test error rose from 8.18% for ResNet-20-noshort to 16.44% for ResNet-110-noshort, against 7.37% and 5.79% with skip connections. (Li et al., 2017) `ev:measured` p. 7 ^li2017visualizing-037
- The DenseNet-121 loss landscape shows no noticeable non-convexity, suggesting the effect applies to other kinds of skip connections. (Li et al., 2017) `ev:measured` p. 8 ^li2017visualizing-038
- Wide-ResNet-56 models, with filters per layer multiplied by k = 2, 4, and 8, show no noticeable chaotic behavior. (Li et al., 2017) `ev:measured` p. 8 ^li2017visualizing-039
- With shortcut connections, Wide-ResNet-56 test error fell from 5.89% at k = 1 to 3.93% at k = 8. (Li et al., 2017) `ev:measured` p. 8 ^li2017visualizing-040
- Without shortcut connections, Wide-ResNet-56 test error fell from 13.31% at k = 1 to 8.70% at k = 8. (Li et al., 2017) `ev:measured` p. 8 ^li2017visualizing-041
- The studied loss landscapes seem partitioned into a low-loss region with convex contours surrounded by a high-loss non-convex region. (Li et al., 2017) `ev:measured` p. 8 ^li2017visualizing-042
- The authors suggest this partitioning of chaotic and convex regions may explain the importance of good initialization strategies. (Li et al., 2017) `ev:asserted` p. 8 ^li2017visualizing-043
- Well-behaved landscapes are dominated by large, flat, nearly convex attractors that rise to a loss value of 4 or greater. (Li et al., 2017) `ev:measured` p. 8 ^li2017visualizing-044
- The authors hypothesize that for sufficiently deep networks with shallow attractors, the initial iterate likely lies in a chaotic region. (Li et al., 2017) `ev:asserted` p. 8 ^li2017visualizing-045
- SGD was unable to train a 156 layer network without skip connections, even with very low learning rates. (Li et al., 2017) `ev:measured` p. 8 ^li2017visualizing-046
- Across the ResNet and Wide-ResNet experiments, visually flatter minimizers consistently correspond to lower test error in the filter-normalized plots. (Li et al., 2017) `ev:measured` p. 8 ^li2017visualizing-047
- Chaotic landscapes of deep networks without skip connections result in worse training and test error than more convex landscapes. (Li et al., 2017) `ev:measured` p. 8 ^li2017visualizing-048
- The most convex landscapes, those of the Wide-ResNets with skip connections, generalize the best of all networks studied. (Li et al., 2017) `ev:measured` p. 8 ^li2017visualizing-049
- Principal curvatures of a plot along random Gaussian directions are weighted averages of the full-dimensional curvatures, with Chi-square weights. (Li et al., 2017) `ev:computed` p. 9 ^li2017visualizing-050
- Non-convexity in the reduced plot implies non-convexity in the full surface, but apparent convexity does not imply true convexity. (Li et al., 2017) `ev:computed` p. 9 ^li2017visualizing-051
- Convex-looking regions in the surface plots correspond to regions with insignificant negative Hessian eigenvalues relative to the positive ones. (Li et al., 2017) `ev:measured` p. 9 ^li2017visualizing-052
- For DenseNet, negative eigenvalues remain less than 1% the size of the positive curvatures over a large region of the plot. (Li et al., 2017) `ev:measured` p. 9 ^li2017visualizing-053
- Projecting SGD iterates onto the plane of two random directions captures almost none of the motion of the optimization trajectory. (Li et al., 2017) `ev:measured` p. 9 ^li2017visualizing-054
- The authors argue that random directions fail because optimization trajectories lie in extremely low-dimensional spaces orthogonal to random vectors. (Li et al., 2017) `ev:asserted` p. 10 ^li2017visualizing-055
- The proposed trajectory plots apply PCA to the matrix of parameter differences from the final parameters across training epochs. (Li et al., 2017) `ev:reported` p. 10 ^li2017visualizing-056
- With weight decay and small batches, the path turns nearly parallel to the contours and orbits the solution at large stepsizes. (Li et al., 2017) `ev:measured` p. 11 ^li2017visualizing-057
- Between 40% and 90% of the variation in the descent paths lies in a space of only 2 dimensions. (Li et al., 2017) `ev:measured` p. 11 ^li2017visualizing-058
- Without normalization, the appendix 1D plots for VGG-9 fail to show consistency between flatness and generalization error. (Li et al., 2017) `ev:measured` p. 14 ^li2017visualizing-059
- The authors find filter normalization more accurate than layer normalization, citing a case where a flatter layer-normalized minimum generalizes worse. (Li et al., 2017) `ev:measured` p. 14 ^li2017visualizing-060
- For ResNet-56 with SGD and weight decay 5e-4, test error was 5.89 at batch size 128 versus 10.59 at 4096. (Li et al., 2017) `ev:measured` p. 16 ^li2017visualizing-061
- VGG-9 1D plots along 10 different random filter-normalized directions are very close in shape to each other. (Li et al., 2017) `ev:measured` p. 17 ^li2017visualizing-062
- Repeated 2D plots of ResNet-56-noshort show apparent changes, but their qualitative chaotic behaviour is quite consistent across plots. (Li et al., 2017) `ev:measured` p. 17 ^li2017visualizing-063
- A 51 × 51 ResNet-56 2D contour plot takes about 1 hour on a workstation with 4 GPUs. (Li et al., 2017) `ev:reported` p. 17 ^li2017visualizing-064

## 🎯 Contributions

## 📖 Glossary

- **Filter normalization** — Rescaling each filter of a random direction to the norm of the matching filter.
- **Loss landscape** — The loss function viewed as a surface over the network's parameter space.
- **1D linear interpolation** — Plotting loss along the straight line between two parameter vectors.
- **Sharp minimizer** — A minimum where loss rises quickly under small parameter perturbations.
- **Flat minimizer** — A minimum surrounded by a wide region of low training loss.
- **Scale invariance** — Network output unchanged when weights are rescaled, e.g. under ReLU or batch normalization.
- **Skip connection** — A shortcut adding a layer's input to its output, as in ResNets.
- **Principal curvatures** — Eigenvalues of the Hessian, measuring local curvature of the loss.
- **PCA trajectory plot** — Optimizer path projected onto the top two principal components of parameter iterates.

## ❓ Open questions

- Does the correlation between filter-normalized sharpness and generalization hold beyond CIFAR-10 and image classifiers?
- Can filter-normalized sharpness be turned into a quantitative, scalar predictor of generalization error?
- Why exactly does increased width suppress chaotic landscapes in networks without skip connections?
- How much hidden non-convexity remains in directions not sampled by the two random filter-normalized directions?
- Is the initialization-in-chaotic-region hypothesis for untrainable deep networks testable directly, beyond the failed 156 layer run?

## 📝 Notes on reading

- Version read: arXiv v3 (7 Nov 2018), the NeurIPS 2018 camera-ready; the packet identifier is the arXiv record.
- All figures are loss-surface plots whose contour labels and axis ticks were extracted as columns of numbers; only captions and subfigure titles (test errors) were usable. Figure 7 (Hessian eigenvalue ratio heat maps) and Figure 9 (PCA trajectories with per-axis variance percentages) could only be described.
- Inconsistency: the contributions bullet (p. 2) says the convex-to-chaotic transition coincides with a dramatic drop in generalization error, whereas the results (pp. 7-8) show test error rising; it likely means a drop in generalization performance.
- Inconsistency: p. 7 says ResNet-56-noshort required an initial learning rate of 0.01, yet Table 2 (p. 18) lists it at 0.1 (test error 13.31, the value in Figure 5) and at 0.01 (test error 10.83).
- Appendix A.5 (p. 17) says the 251 × 251 resolution was used for ResNet-56-noshort in Figure 1, while the Figure 1 caption describes ResNet-56 with/without skip connections.
- Table 2 (p. 18) values were extracted as a flat column; they were not claimed cell by cell.

## Suggested new concepts

- Filter normalization — the paper's core method for comparable loss-surface plots, reused widely in later landscape studies.
- Loss landscape visualization — a family of methods (1D interpolation, random-direction contours, PCA trajectories) with distinct failure modes.
- Sharp vs flat minima — a recurring debate on whether minimizer sharpness predicts generalization.
- Skip connections and trainability — links architecture design to landscape smoothness and deep-network trainability.

## Por qué es relevante

- **[[02_optimizacion_y_algoritmos]]** — Geometría del paisaje de pérdida (E.2).
