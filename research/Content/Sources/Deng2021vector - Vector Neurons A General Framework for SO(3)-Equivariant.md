---
aliases: []
type: "source"
title: "Vector Neurons: A General Framework for SO(3)-Equivariant Networks"
citekey: "Deng2021vector"
doi: "10.48550/arXiv.2104.12229"
arxiv: "2104.12229"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2104.12229"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Congyue Deng", "Or Litany", "Yueqi Duan", "Adrien Poulenard", "Andrea Tagliasacchi", "Leonidas Guibas"]
sha256: ["e84900560ba435d6edce464e16b305a6ba972ec8c9d81f25bbe642e44618d837"]
pdf: "Content/Papers/Deng2021vector.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 64
---

📄 PDF: [[Deng2021vector.pdf]]

> [!abstract] One-sentence summary
> The paper lifts neurons from scalars to 3D vectors to build simple SO(3)-equivariant linear, non-linear, pooling, normalization and invariant layers, plugs them into PointNet and DGCNN, and shows rotation-robust classification, segmentation and implicit reconstruction.

## Abstract

Invariance and equivariance to the rotation group have been widely discussed in the 3D deep learning community for pointclouds. Yet most proposed methods either use complex mathematical tools that may limit their accessibility, or are tied to specific input data types and network architectures. In this paper, we introduce a general framework built on top of what we call Vector Neuron representations for creating SO(3)-equivariant neural networks for pointcloud processing. Extending neurons from 1D scalars to 3D vectors, our vector neurons enable a simple mapping of SO(3) actions to latent spaces thereby providing a framework for building equivariance in common neural operations -- including linear layers, non-linearities, pooling, and normalizations. Due to their simplicity, vector neurons are versatile and, as we demonstrate, can be incorporated into diverse network architecture backbones, allowing them to process geometry inputs in arbitrary poses. Despite its simplicity, our method performs comparably well in accuracy and generalization with other more complex and specialized state-of-the-art methods on classification and segmentation tasks. We also show for the first time a rotation equivariant reconstruction network. (arXiv)

## 🧠 Key ideas (atomic)

- PointNet uses spatial transformer layers that attain only approximate pose invariance and require extensive augmentation at training time. (Deng et al., 2021) `ev:cited` p. 1 ^deng2021vector-001
- The authors state that [[Tensor Field Network|Tensor Field Networks]] and SE(3)-Transformers are hard to incorporate into existing pipelines, being restricted to convolutions. (Deng et al., 2021) `ev:cited` p. 1 ^deng2021vector-002
- The [[Vector Neurons|Vector Neuron representation]] extends classical scalar neurons to 3D vectors, so latent features become ordered sequences of 3-vectors. (Deng et al., 2021) `ev:asserted` p. 1 ^deng2021vector-003
- The authors contrast the direct mapping of input rotations to intermediate VN layers with more complex solutions based on Wigner D-matrices. (Deng et al., 2021) `ev:asserted` p. 2 ^deng2021vector-004
- A key contribution is a 3D generalization of classical activation functions, implemented through a learned direction that depends linearly on the data. (Deng et al., 2021) `ev:asserted` p. 2 ^deng2021vector-005
- [[Vector Neurons|Vector neuron versions]] of PointNet and DGCNN were implemented and tested on classification, segmentation, and reconstruction as downstream tasks. (Deng et al., 2021) `ev:reported` p. 2 ^deng2021vector-006
- The authors claim to be the first to demonstrate a 3D rotation-equivariant network for the task of 3D reconstruction. (Deng et al., 2021) `ev:asserted` p. 2 ^deng2021vector-007
- Each VN layer is required to be rotation equivariant: rotating the input vector-list features must equal rotating the layer's output. (Deng et al., 2021) `ev:asserted` p. 3 ^deng2021vector-008
- The VN linear layer left-multiplies the vector-list feature by a weight matrix, which commutes with right-multiplication by any rotation matrix. (Deng et al., 2021) `ev:computed` p. 3 ^deng2021vector-009
- The VN linear layer omits a bias term because adding a constant vector would interfere with rotation equivariance. (Deng et al., 2021) `ev:asserted` p. 3 ^deng2021vector-010
- The authors note that SE(3) equivariance can be achieved with the SO(3)-equivariant linear layer by centering the features at the origin. (Deng et al., 2021) `ev:asserted` p. 3 ^deng2021vector-011
- For each output vector neuron, the [[Vector Neurons|VN non-linearity]] learns two weight matrices that linearly map the input to a feature and a direction. (Deng et al., 2021) `ev:reported` p. 4 ^deng2021vector-012
- [[Vector Neurons|VN-ReLU]] keeps the feature unchanged when its inner product with the learned direction is non-negative, otherwise removing its component along that direction. (Deng et al., 2021) `ev:reported` p. 4 ^deng2021vector-013
- The authors note that committing the non-linearity to a fixed frame, such as the standard coordinate system, would violate rotation equivariance. (Deng et al., 2021) `ev:asserted` p. 4 ^deng2021vector-014
- In practice the unit direction is computed with a small epsilon added to the norm to avoid division by zero at the origin. (Deng et al., 2021) `ev:reported` p. 4 ^deng2021vector-015
- VN max pooling selects, per channel, the element whose feature best aligns with a data-dependent direction obtained through a learned weight matrix. (Deng et al., 2021) `ev:reported` p. 4 ^deng2021vector-016
- The authors note that mean pooling is a linear operation that respects rotation equivariance, alongside their proposed VN max pooling layer. (Deng et al., 2021) `ev:asserted` p. 4 ^deng2021vector-017
- Layer and instance normalizations are computed per sample and thus can be trivially generalized to VN networks, according to the authors. (Deng et al., 2021) `ev:asserted` p. 4 ^deng2021vector-018
- The authors argue that averaging arbitrarily rotated inputs across a batch would not necessarily be meaningful for rotation-equivariant networks. (Deng et al., 2021) `ev:asserted` p. 5 ^deng2021vector-019
- VN batch normalization is applied to the rotation-invariant 2-norms of the vector channels, rescaling each vector by its normalized norm. (Deng et al., 2021) `ev:reported` p. 5 ^deng2021vector-020
- The product of an equivariant signal with the transpose of another equivariant signal is rotation invariant, which underlies the VN invariant layer. (Deng et al., 2021) `ev:computed` p. 5 ^deng2021vector-021
- The authors note that using the Gram matrix of the vector-list as an invariant feature would result in large quadratic storage complexity. (Deng et al., 2021) `ev:asserted` p. 5 ^deng2021vector-022
- The invariant layer predicts a per-point coordinate system from each feature concatenated with the global mean, then reads the feature in it. (Deng et al., 2021) `ev:reported` p. 5 ^deng2021vector-023
- The authors argue that VN layers fit PointNet and DGCNN backbones, whereas convolution-based methods such as TFN and EGCL do not. (Deng et al., 2021) `ev:asserted` p. 5 ^deng2021vector-024
- VN-DGCNN replaces the ReLU and pooling of the DGCNN edge convolution with VN-ReLU and VN pooling on vector-list features. (Deng et al., 2021) `ev:reported` p. 5 ^deng2021vector-025
- Applying a shared VN-MLP directly to single-vector input coordinates would yield vector channels that are all linearly dependent, pointing in one direction. (Deng et al., 2021) `ev:asserted` p. 5 ^deng2021vector-026
- VN-PointNet adds an edge convolution at the input layer to map each input point to a vector-list with more than one channel. (Deng et al., 2021) `ev:reported` p. 5 ^deng2021vector-027
- The ModelNet40 dataset has 40 classes and 12,311 CAD models, of which 9,843 were used for training in classification. (Deng et al., 2021) `ev:reported` p. 6 ^deng2021vector-028
- Part segmentation used ShapeNet-part, following earlier work, which has 16 shape categories with more than 30,000 models. (Deng et al., 2021) `ev:reported` p. 6 ^deng2021vector-029
- Shape reconstruction used a ShapeNet subset from earlier work, containing 13 major categories with 50,000 models. (Deng et al., 2021) `ev:reported` p. 6 ^deng2021vector-030
- Classification and segmentation used z/z, z/SO(3) and SO(3)/SO(3) train/test settings, following the conventions of Esteves et al. (Deng et al., 2021) `ev:reported` p. 6 ^deng2021vector-031
- For reconstruction, SO(3) rotations were generated once per shape during preprocessing, and all shapes kept fixed poses during training. (Deng et al., 2021) `ev:reported` p. 6 ^deng2021vector-032
- Each VN layer has floor of N/3 vector channels where the scalar layer has N, giving roughly 2/9 times the parameters. (Deng et al., 2021) `ev:reported` p. 6 ^deng2021vector-033
- VN-PointNet discards the input spatial transformation MLP, since the VN network already accounts for rigid transformations by construction. (Deng et al., 2021) `ev:reported` p. 6 ^deng2021vector-034
- All classification and segmentation networks use mean pooling for aggregation, which the authors report performed better in practice. (Deng et al., 2021) `ev:reported` p. 6 ^deng2021vector-035
- On ModelNet40 classification, VN-DGCNN reaches test accuracy of 89.5 in both the z/z and z/SO(3) settings. (Deng et al., 2021) `ev:measured` p. 6 ^deng2021vector-036
- On ModelNet40 classification, VN-DGCNN reaches accuracy of 90.2 in the SO(3)/SO(3) setting with arbitrary rotations. (Deng et al., 2021) `ev:measured` p. 6 ^deng2021vector-037
- Under z/SO(3) on ModelNet40, the accuracy of non-equivariant DGCNN drops to 33.8, and PointNet drops to 19.6. (Deng et al., 2021) `ev:measured` p. 6 ^deng2021vector-038
- VN-PointNet reaches 77.5 accuracy in z/z, below the 85.9 of the original PointNet in the same setting. (Deng et al., 2021) `ev:measured` p. 6 ^deng2021vector-039
- VN-PointNet keeps 77.5 accuracy in the z/SO(3) setting, where test rotations are unseen during training. (Deng et al., 2021) `ev:measured` p. 6 ^deng2021vector-040
- VN-DGCNN outperforms all other equivariant or invariant methods using only point coordinates in z/SO(3) and SO(3)/SO(3) classification. (Deng et al., 2021) `ev:measured` p. 6 ^deng2021vector-041
- Methods that additionally use surface normals, such as SFCNN and LGR-Net, still achieve slightly better classification results than VN-DGCNN. (Deng et al., 2021) `ev:measured` p. 6 ^deng2021vector-042
- Even with SO(3) augmentation at training time, rotation-sensitive networks do not match the classification accuracy of VN networks. (Deng et al., 2021) `ev:measured` p. 6 ^deng2021vector-043
- On ShapeNet part segmentation, VN-DGCNN achieves 81.4 mean IoU in both the z/SO(3) and SO(3)/SO(3) settings. (Deng et al., 2021) `ev:measured` p. 7 ^deng2021vector-044
- In part segmentation, VN-DGCNN outperforms LGR-Net, which uses surface normals and reaches 80.1 mean IoU under SO(3)/SO(3). (Deng et al., 2021) `ev:measured` p. 7 ^deng2021vector-045
- For reconstruction, 300 points were subsampled from each watertight ShapeNet model and perturbed with zero-mean noise of 0.005 standard deviation. (Deng et al., 2021) `ev:reported` p. 7 ^deng2021vector-046
- The original OccNet was retrained together with the VN methods for 300k iterations, keeping the best model on the validation set. (Deng et al., 2021) `ev:reported` p. 7 ^deng2021vector-047
- VN-OccNet pairs a rotation-equivariant VN-PointNet encoder with a rotation-invariant decoder built on norm, inner-product and VN-In features. (Deng et al., 2021) `ev:reported` p. 7 ^deng2021vector-048
- VN-OccNet reaches volumetric mean IoU of 69.3 in both the I/I and I/SO(3) reconstruction settings. (Deng et al., 2021) `ev:measured` p. 8 ^deng2021vector-049
- The original OccNet reaches 71.4 volumetric mean IoU in I/I but drops to 30.9 in I/SO(3). (Deng et al., 2021) `ev:measured` p. 8 ^deng2021vector-050
- Replacing only the OccNet decoder with the invariant decoder slightly improves results, reaching 72.0, 31.0 and 59.4 mean IoU. (Deng et al., 2021) `ev:measured` p. 8 ^deng2021vector-051
- Under SO(3)/SO(3) training, OccNet generates blurry shapes, averaged shapes, or shapes with incorrect category priors in the qualitative results. (Deng et al., 2021) `ev:measured` p. 7 ^deng2021vector-052
- On aligned input shapes, VN-OccNet does not match the reconstruction quality of vanilla OccNet, falling short by a small margin. (Deng et al., 2021) `ev:measured` p. 8 ^deng2021vector-053
- The authors state that the framework has obvious generalizations to higher-dimensional pointclouds in a completely analogous way. (Deng et al., 2021) `ev:asserted` p. 8 ^deng2021vector-054
- The authors believe vector neurons could find applications in other modalities such as meshes, voxel grids, and even images. (Deng et al., 2021) `ev:asserted` p. 9 ^deng2021vector-055
- The authors suggest generalizing [[Vector Neurons|vector neurons]] to other transformation groups such as the full affine group, noting uniform scalings are straightforward. (Deng et al., 2021) `ev:asserted` p. 9 ^deng2021vector-056
- VN-LeakyReLU contracts the component parallel to the learned direction by a factor between zero and one instead of clipping it. (Deng et al., 2021) `ev:reported` p. 11 ^deng2021vector-057
- A logarithm-based VN batch normalization avoids negative norms but brings instability and can cause gradient explosion in practice. (Deng et al., 2021) `ev:asserted` p. 11 ^deng2021vector-058
- Detaching linear layers from the non-linearity leads to slightly better ModelNet40 classification results in most cases with either VN backbone. (Deng et al., 2021) `ev:measured` p. 12 ^deng2021vector-059
- Detached non-linearities double network depth and need roughly at least 1.5 times the training time of the entangled layers. (Deng et al., 2021) `ev:reported` p. 12 ^deng2021vector-060
- Trained on aligned data and tested under I/SO(3), VN-DGCNN keeps 90.0 accuracy on ModelNet40, while DGCNN falls to 16.6. (Deng et al., 2021) `ev:measured` p. 12 ^deng2021vector-061
- Trained without rotation augmentation, VN-DGCNN keeps 81.5 part segmentation mean IoU under I/SO(3), against 36.1 for DGCNN. (Deng et al., 2021) `ev:measured` p. 12 ^deng2021vector-062
- VN-MAX and mean pooling give comparable classification results, with mean pooling performing slightly better than VN-MAX in more cases. (Deng et al., 2021) `ev:measured` p. 12 ^deng2021vector-063
- In the invariant-layer ablation, improvements from adding the global mean and a 3-layer VN-MLP are minor. (Deng et al., 2021) `ev:measured` p. 12 ^deng2021vector-064

## 🎯 Contributions

## 📖 Glossary

- **Vector Neuron (VN)** — A neuron whose value is a 3D vector instead of a scalar.
- **Vector-list feature** — An ordered list of C vector neurons, i.e. a C×3 matrix.
- **SO(3)-equivariance** — Rotating the input rotates the output by the same rotation.
- **Rotation invariance** — The output stays unchanged when the input is rotated.
- **VN-ReLU** — ReLU generalization clipping the feature component opposite a learned, data-dependent direction.
- **VN-In** — Invariant layer reading features in a learned equivariant coordinate system.
- **z/SO(3)** — Train with vertical-axis rotations only, test with arbitrary rotations.
- **OccNet** — Occupancy network: neural implicit function predicting occupancy probability of 3D points.

## ❓ Open questions

- Why does VN-OccNet fall slightly short of vanilla OccNet on aligned inputs, and can the gap be closed?
- Why does VN-PointNet lose several points of accuracy against PointNet in the aligned z/z setting?
- How do vector neurons extend to meshes, voxel grids, images, or the full affine group in practice?
- Can VN max pooling be made to consistently match or exceed mean pooling?
- Is there a stable batch normalization that avoids negative norms without log/exp instability?

## 📝 Notes on reading

Read the arXiv v1 preprint (2104.12229v1, 25 Apr 2021), which includes the supplementary material on pages 11-12. Equations 6, 10-12, 24 and 29-31 are partly garbled by extraction (brackets rendered as stray glyphs); they were described in words rather than quoted. Figures 1-7 (VN lifting, linear layer, non-linearity, normalization, reconstructions) could only be described from their captions. The reconstruction encoder equation writes the point set as x1 ... x1 (likely xN), an extraction or typesetting slip. Table 1 caption cites ModelNet40 as [37] while the Datasets paragraph cites [5]. Table 8 caption refers to (13) for computing Tn, while the definition is equation 14. The abstract says the method performs comparably with state-of-the-art methods, while the introduction claims top performance on randomly rotated shapes; point-plus-normal methods remain slightly better in classification.

## Suggested new concepts

- Vector Neurons — a general building block for SO(3)-equivariant pointcloud networks, likely reused across later equivariant work.
- Rotation-equivariant pointcloud networks — a family (TFN, SE(3)-Transformers, VN) that deserves a comparison note.
- Equivariance by construction vs. by augmentation — a recurring design trade-off, quantified here on ModelNet40 and ShapeNet.
- Neural implicit reconstruction (occupancy networks) — the reconstruction setting VN-OccNet extends.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Capas equivariantes simples para nubes de puntos
