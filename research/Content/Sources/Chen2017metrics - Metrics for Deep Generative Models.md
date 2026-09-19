---
aliases: []
type: "source"
title: "Metrics for Deep Generative Models"
citekey: "Chen2017metrics"
doi: "10.48550/arXiv.1711.01204"
arxiv: "1711.01204"
year: 2017
publication_type: "preprint"
url: "https://arxiv.org/abs/1711.01204"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Nutan Chen", "Alexej Klushyn", "Richard Kurle", "Xueyan Jiang", "Justin Bayer", "Patrick van der Smagt"]
sha256: ["3d8d7e095f419dccccb13d1c994fd0a724932505389f46fbcd1998124e6029e4"]
pdf: "Content/Papers/Chen2017metrics.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 62
---

📄 PDF: [[Chen2017metrics.pdf]]

> [!abstract] One-sentence summary
> The paper treats the latent space of importance-weighted autoencoders as a Riemannian manifold and approximates geodesics with a neural network, giving shorter, smoother, class-respecting distances and interpolations than Euclidean ones on pendulum, MNIST, robot arm and human motion data.

## Abstract

Neural samplers such as variational autoencoders (VAEs) or generative adversarial networks (GANs) approximate distributions by transforming samples from a simple random source---the latent space---to samples from a more complex distribution represented by a dataset. While the manifold hypothesis implies that the density induced by a dataset contains large regions of low density, the training criterions of VAEs and GANs will make the latent space densely covered. Consequently points that are separated by low-density regions in observation space will be pushed together in latent space, making stationary distances poor proxies for similarity. We transfer ideas from Riemannian geometry to this setting, letting the distance between two points be the shortest path on a Riemannian manifold induced by the transformation. The method yields a principled distance measure, provides a tool for visual inspection of deep generative models, and an alternative to linear interpolation in latent space. In addition, it can be applied for robot movement generalization using previously learned skills. The method is evaluated on a synthetic dataset with known ground truth; on a simulated robot arm dataset; on human motion capture data; and on a generative model of handwritten digits. (arXiv)

## 🧠 Key ideas (atomic)

- The paper aims to bring techniques to neural samplers that make them powerful tools for metric learning. (Chen et al., 2017) `ev:asserted` p. 1 ^chen2017metrics-001
- Tosi et al. proposed treating the GP-LVM latent space as a Riemannian manifold, with distances given by shortest paths along the data manifold. (Chen et al., 2017) `ev:cited` p. 1 ^chen2017metrics-002
- The authors transfer the Riemannian latent space idea of Tosi et al. to neural samplers such as variational autoencoders. (Chen et al., 2017) `ev:asserted` p. 2 ^chen2017metrics-003
- The authors note that Arvanitidis et al. and Shao et al. independently worked on this topic at the same time. (Chen et al., 2017) `ev:cited` p. 2 ^chen2017metrics-004
- In robotic domains, the authors state the approach can be applied to path planning based on learned skills. (Chen et al., 2017) `ev:asserted` p. 2 ^chen2017metrics-005
- Euclidean distance in latent space implicitly assumes that latent distances are proportional to observation distances, which the authors call a fallacy. (Chen et al., 2017) `ev:asserted` p. 2 ^chen2017metrics-006
- The authors argue that stark discontinuities in the likelihood are virtually always present when latent variables adequately model the data. (Chen et al., 2017) `ev:asserted` p. 2 ^chen2017metrics-007
- Separated manifolds in observation space, such as points of different classes, may be placed directly next to each other in latent space. (Chen et al., 2017) `ev:asserted` p. 2 ^chen2017metrics-008
- The authors estimate their nonlinear latent variable models with importance-weighted autoencoders (IWAE) as the basis of their approach. (Chen et al., 2017) `ev:reported` p. 2 ^chen2017metrics-009
- The IWAE treats the inference network as a proposal distribution and obtains a tighter lower bound using importance sampling. (Chen et al., 2017) `ev:cited` p. 2 ^chen2017metrics-010
- An inflexible variational posterior directly impacts the generative model, causing both inference and generative models to underuse their capacity. (Chen et al., 2017) `ev:asserted` p. 2 ^chen2017metrics-011
- The curve length in observation space is expressed through the Jacobian of the generator, giving the metric tensor G = JT J. (Chen et al., 2017) `ev:computed` p. 3 ^chen2017metrics-012
- The latent curve is approximated by a neural network mapping a scalar time to a latent point, whose weights are optimized. (Chen et al., 2017) `ev:reported` p. 3 ^chen2017metrics-013
- The curve length integral is approximated with n equidistantly spaced sampling points of t between zero and one. (Chen et al., 2017) `ev:reported` p. 3 ^chen2017metrics-014
- The authors call the term inside the length summation the velocity, the rate of change induced by the generative model. (Chen et al., 2017) `ev:asserted` p. 3 ^chen2017metrics-015
- Boundary constraints are satisfied by shifting and rescaling the predicted curve, reducing the problem to unconstrained length minimization. (Chen et al., 2017) `ev:reported` p. 3 ^chen2017metrics-016
- A penalization term on the norm of the metric tensor is added to ensure the geodesic follows the data manifold. (Chen et al., 2017) `ev:reported` p. 3 ^chen2017metrics-017
- The smoothing is implemented as post-processing via singular-value decomposition, equivalent to a low-rank reconstruction of the metric tensor. (Chen et al., 2017) `ev:reported` p. 4 ^chen2017metrics-018
- According to the authors, a higher regularization coefficient augments the difference between the Euclidean interpolation and the path along the manifold. (Chen et al., 2017) `ev:asserted` p. 4 ^chen2017metrics-019
- The magnification factor, the square root of the metric tensor determinant, is used to visualize metric tensors for two latent dimensions. (Chen et al., 2017) `ev:reported` p. 4 ^chen2017metrics-020
- In all experiments the authors chose a Gaussian prior with zero mean and identity covariance for the latent variables. (Chen et al., 2017) `ev:reported` p. 4 ^chen2017metrics-021
- The authors used sigmoid, tanh and softplus activation functions in the generative models of their experiments. (Chen et al., 2017) `ev:reported` p. 4 ^chen2017metrics-022
- The artificial pendulum dataset contains 15,000 images of 16×16 pixels augmented with 0.05 per-pixel Gaussian noise. (Chen et al., 2017) `ev:reported` p. 4 ^chen2017metrics-023
- Along the geodesic, reconstructed pendulum images show a much more uniform rotation than along the Euclidean interpolation. (Chen et al., 2017) `ev:measured` p. 5 ^chen2017metrics-024
- For one pendulum pair, the Euclidean interpolation distance is 0.827, whereas the geodesic distance is 0.538. (Chen et al., 2017) `ev:measured` p. 5 ^chen2017metrics-025
- For the pendulum data, SVD regularization with large values of λs was necessary for the optimization to yield a path along the manifold. (Chen et al., 2017) `ev:reported` p. 5 ^chen2017metrics-026
- On the pendulum data, small values of λs lead to shorter Euclidean interpolation distances than paths along the data manifold. (Chen et al., 2017) `ev:measured` p. 5 ^chen2017metrics-027
- Over 100 pendulum pairs, average lengths of geodesics, Euclidean interpolations and manifold paths are 0.319, 0.820, and 0.353 respectively. (Chen et al., 2017) `ev:measured` p. 5 ^chen2017metrics-028
- Geodesic distances and data manifold path distances are linearly correlated with the angle between two pendulum points in observation space. (Chen et al., 2017) `ev:measured` p. 5 ^chen2017metrics-029
- MNIST experiments use a fixed binarized version with 50,000 training and 10,000 test images of 28 × 28 pixels. (Chen et al., 2017) `ev:reported` p. 6 ^chen2017metrics-030
- On MNIST, equidistance lines show that treating latent space as a Riemannian manifold enables separating classes, as geodesics between similar points are shorter. (Chen et al., 2017) `ev:measured` p. 6 ^chen2017metrics-031
- Data points of different MNIST classes are almost not separable in the latent space by their Euclidean distance. (Chen et al., 2017) `ev:measured` p. 6 ^chen2017metrics-032
- In the shown MNIST example, the Euclidean interpolation crosses four classes, whereas the geodesic crosses just two. (Chen et al., 2017) `ev:measured` p. 6 ^chen2017metrics-033
- For the MNIST pair, the Euclidean interpolation distance is 74.3, whereas the geodesic distance amounts to 62.9. (Chen et al., 2017) `ev:measured` p. 6 ^chen2017metrics-034
- Compared to the geodesic, the Euclidean interpolation leads to less smooth transitions in the MNIST reconstructions. (Chen et al., 2017) `ev:measured` p. 6 ^chen2017metrics-035
- Transitions between different MNIST classes appear as regions of higher velocity along the interpolated paths in the reconstructions. (Chen et al., 2017) `ev:measured` p. 6 ^chen2017metrics-036
- The robot arm dataset simulates a six DOF KUKA robot whose end effector moves a 0.4 meter radius circle over 6284 time steps. (Chen et al., 2017) `ev:reported` p. 7 ^chen2017metrics-037
- Robot input data were six-dimensional joint angles, obtained by inverse kinematics at each time step of the simulated movement. (Chen et al., 2017) `ev:reported` p. 7 ^chen2017metrics-038
- Gaussian noise with a standard deviation of 0.03 was added to the robot arm joint angle data. (Chen et al., 2017) `ev:reported` p. 7 ^chen2017metrics-039
- The authors report that geodesic interpolation outperforms Euclidean interpolation for the robot arm movement, shown in end effector Cartesian space. (Chen et al., 2017) `ev:measured` p. 7 ^chen2017metrics-040
- For the robot arm, the Euclidean interpolation distance is 1.48, and the geodesic distance is 0.54. (Chen et al., 2017) `ev:measured` p. 7 ^chen2017metrics-041
- Unlike prior motion planning work with task space constraints, the method does not explicitly require such constraints. (Chen et al., 2017) `ev:asserted` p. 7 ^chen2017metrics-042
- Human motion experiments use walking trials 1 to 16 of subject 35 from the CMU motion capture database. (Chen et al., 2017) `ev:reported` p. 7 ^chen2017metrics-043
- The 62-dimensional motion capture features were pre-processed to 50-dimensional vectors following Chen et al. 2015. (Chen et al., 2017) `ev:reported` p. 7 ^chen2017metrics-044
- The 6616 motion frames were augmented with Gaussian noise of standard deviation 0.03, yielding four times the original dataset size. (Chen et al., 2017) `ev:reported` p. 7 ^chen2017metrics-045
- The authors observe that the added noise smooths the latent space, seen through the magnification factor and interpolation reconstructions. (Chen et al., 2017) `ev:measured` p. 7 ^chen2017metrics-046
- For human motion, the geodesic follows the data manifold and generates a natural, smooth walking movement. (Chen et al., 2017) `ev:measured` p. 8 ^chen2017metrics-047
- The Euclidean human motion interpolation traverses two high MF areas, which cause large jumps of the movement. (Chen et al., 2017) `ev:measured` p. 8 ^chen2017metrics-048
- For the human motion pair, the Euclidean interpolation distance is 2.89, and the geodesic distance is 2.57. (Chen et al., 2017) `ev:measured` p. 8 ^chen2017metrics-049
- One circle in the human motion latent space corresponds to two steps of a walking movement in observation space. (Chen et al., 2017) `ev:measured` p. 8 ^chen2017metrics-050
- The authors conclude that latent space distances in general do not reflect the true similarity of corresponding observation space points. (Chen et al., 2017) `ev:asserted` p. 8 ^chen2017metrics-051
- The authors applied SVD to the metric tensor to produce shorter distances along the manifold compared to the Euclidean distance. (Chen et al., 2017) `ev:asserted` p. 8 ^chen2017metrics-052
- As a secondary effect, the authors state the metric can be used for smoother interpolations in the latent space. (Chen et al., 2017) `ev:asserted` p. 8 ^chen2017metrics-053
- For two-dimensional latent spaces, the magnification factor visualizes the magnitude of the generator's distortion of infinitesimal latent areas. (Chen et al., 2017) `ev:asserted` p. 8 ^chen2017metrics-054
- Future work includes facilitating use of this distance metric and applying it to models with dynamics. (Chen et al., 2017) `ev:asserted` p. 8 ^chen2017metrics-055
- The authors found that training the curve network with batch gradient descent on the length loss is prone to local minima. (Chen et al., 2017) `ev:measured` p. 10 ^chen2017metrics-056
- The curve network is pre-trained on n random Bézier curves, selecting the fit with the lowest validation value. (Chen et al., 2017) `ev:reported` p. 10 ^chen2017metrics-057
- Candidate curves are validated on maximum velocity plus path length to avoid local minima with narrow velocity spikes. (Chen et al., 2017) `ev:reported` p. 10 ^chen2017metrics-058
- Gradient-based geodesic optimization is not possible when the generative model uses piecewise linear units, whose second derivative is zero. (Chen et al., 2017) `ev:computed` p. 10 ^chen2017metrics-059
- The authors used the Adam optimizer for training in all experiments, as stated in the experiment setup appendix. (Chen et al., 2017) `ev:reported` p. 10 ^chen2017metrics-060
- The geodesic network has two tanh fully connected layers of 150 units and uses 500 sample points. (Chen et al., 2017) `ev:reported` p. 11 ^chen2017metrics-061
- The IWAEs use K = 50 importance samples for pendulum and MNIST, and K = 15 for robot arm and human motion. (Chen et al., 2017) `ev:reported` p. 11 ^chen2017metrics-062

## 🎯 Contributions

## 📖 Glossary

- **Geodesic** — Locally length-minimizing curve on a Riemannian manifold.
- **Metric tensor** — Matrix G = JT J defining inner products on the latent tangent space.
- **Magnification factor (MF)** — Square root of det G; local volume distortion of the generator.
- **Velocity** — Rate of change along a latent curve as measured in observation space.
- **IWAE** — Importance-weighted autoencoder; VAE variant with a tighter importance-sampled likelihood bound.
- **Manifold hypothesis** — Assumption that high-dimensional data concentrate near low-dimensional manifolds with low-density gaps.

## ❓ Open questions

- Does the approach scale to latent spaces with more than two dimensions, where MF visualization is not available?
- How sensitive are the distances to the choice of λs and the low rank r in the SVD smoothing?
- How does the geodesic distance perform in downstream tasks such as k-nearest neighbour classification or clustering?
- Can the method be applied to GANs or to generators with piecewise linear activations?
- How does it extend to models with dynamics, as named in future work?

## 📝 Notes on reading

The version read is arXiv 1711.01204v2 (8 Feb 2018), which carries the AISTATS 2018 proceedings header. Section 4 says the experiments use three different datasets but then lists four (pendulum, MNIST, robot arm, human motion). Figures 2, 3, 6, 7, 8, 12 and 13 are latent space plots that could only be described; Figure 3 shows distances versus λs over 100 pairs with 95% confidence intervals. Equations for the curve length, SVD smoothing (Eq. 17) and Jacobian gradients are partly garbled in the extraction. The paper evaluates only single example pairs for MNIST, robot arm and human motion distances; only the pendulum has a 100-pair aggregate. The introduction claims evidence for the manifold hypothesis, but no dedicated test is reported.

## Suggested new concepts

- Riemannian latent space metric — pulls back observation space geometry to latent spaces of generative models; recurring across several papers.
- Magnification factor — a visualization tool for generator distortion, reused in later latent geometry work.
- Geodesic interpolation — alternative to linear latent interpolation with applications to motion generation for robots.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H6.** Calcula geodésicas en el latente de modelos generativos y las aplica a la generalización de movimientos de un brazo robótico.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
