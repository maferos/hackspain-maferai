---
aliases: []
type: "source"
title: "Deep Bingham Networks: Dealing with Uncertainty and Ambiguity in Pose Estimation"
citekey: "Deng2020deep"
doi: "10.48550/arXiv.2012.11002"
arxiv: "2012.11002"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2012.11002"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Haowen Deng", "Mai Bui", "Nassir Navab", "Leonidas Guibas", "Slobodan Ilic", "Tolga Birdal"]
sha256: ["9c71544ea46b3673bb271db44fa3cd8685ae92f04394f7c87e91d857717a3963"]
pdf: "Content/Papers/Deng2020deep.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 66
---

📄 PDF: [[Deng2020deep.pdf]]

> [!abstract] One-sentence summary
> Deep Bingham Networks regress unimodal or mixture Bingham distributions over quaternion rotations, trained with a relaxed winner-takes-all scheme against mode collapse, so one network reports multiple plausible poses with per-hypothesis uncertainty for camera relocalization and point cloud object pose estimation.

## Abstract

In this work, we introduce Deep Bingham Networks (DBN), a generic framework that can naturally handle pose-related uncertainties and ambiguities arising in almost all real life applications concerning 3D data. While existing works strive to find a single solution to the pose estimation problem, we make peace with the ambiguities causing high uncertainty around which solutions to identify as the best. Instead, we report a family of poses which capture the nature of the solution space. DBN extends the state of the art direct pose regression networks by (i) a multi-hypotheses prediction head which can yield different distribution modes; and (ii) novel loss functions that benefit from Bingham distributions on rotations. This way, DBN can work both in unambiguous cases providing uncertainty information, and in ambiguous scenes where an uncertainty per mode is desired. On a technical front, our network regresses continuous Bingham mixture models and is applicable to both 2D data such as images and to 3D data such as point clouds. We proposed new training strategies so as to avoid mode or posterior collapse during training and to improve numerical stability. Our methods are thoroughly tested on two different applications exploiting two different modalities: (i) 6D camera relocalization from images; and (ii) object pose estimation from 3D point clouds, demonstrating decent advantages over the state of the art. For the former we contributed our own dataset composed of five indoor scenes where it is unavoidable to capture images corresponding to views that are hard to uniquely identify. For the latter we achieve the top results especially for symmetric objects of ModelNet dataset. (arXiv)

## 🧠 Key ideas (atomic)

- Deep Bingham Networks are a generic framework that reports a family of poses instead of a single solution when pose estimation is ambiguous. (Deng et al., 2020) `ev:asserted` p. 1 ^deng2020deep-001
- Rotations are modelled by a mixture of [[Bingham distribution|anisotropic Bingham distributions]], which the authors describe as well suited to quaternion parameterizations. (Deng et al., 2020) `ev:asserted` p. 2 ^deng2020deep-002
- Translations are handled with Gaussian distributions, which the authors consider well suited to capture variability in Euclidean spaces. (Deng et al., 2020) `ev:asserted` p. 2 ^deng2020deep-003
- The work extends the authors' earlier camera relocalization method for ambiguous scenes to object pose estimation from ambiguous 3D input. (Deng et al., 2020) `ev:reported` p. 2 ^deng2020deep-004
- Unlike symmetry-aware methods, the approach tries to capture [[Pose ambiguity from symmetry|object symmetries]] in the multimodal predictions without explicit supervision of symmetry types. (Deng et al., 2020) `ev:asserted` p. 2 ^deng2020deep-005
- Prior symmetry-aware pose networks require extensive object knowledge and cannot localize against a scene without having a 3D model. (Deng et al., 2020) `ev:cited` p. 3 ^deng2020deep-006
- Mixture Density Networks directly predict Gaussian mixture parameters but suffer from problems like mode collapse and numeric instability. (Deng et al., 2020) `ev:cited` p. 3 ^deng2020deep-007
- VidLoc adapted mixture density networks to 6D relocalization but, according to the authors, incorrectly modelled rotation parameters with Gaussian distributions. (Deng et al., 2020) `ev:cited` p. 3 ^deng2020deep-008
- The closest prior work learns orientation end to end with a [[Bingham distribution]] but provides no means of dealing with mode collapse. (Deng et al., 2020) `ev:cited` p. 4 ^deng2020deep-009
- The authors state that in practice the Monte Carlo sampling scheme tends to draw pose samples around a single mode. (Deng et al., 2020) `ev:asserted` p. 4 ^deng2020deep-010
- The authors map all rotations to the northern hemisphere to handle the redundancy between a quaternion and its negation. (Deng et al., 2020) `ev:reported` p. 5 ^deng2020deep-011
- Three strategies construct the orientation matrix V: Gram-Schmidt orthonormalization, the Birdal matrix representation of quaternions, and a Cayley transformation. (Deng et al., 2020) `ev:reported` p. 5 ^deng2020deep-012
- The Birdal and Cayley strategies need a reduced number of predictions (4) to yield V, compared with Gram-Schmidt (16). (Deng et al., 2020) `ev:reported` p. 6 ^deng2020deep-013
- The Unimodal Bingham Network models the pose by a [[Bingham distribution|single Bingham distribution]] whose entropy serves as a measure of prediction uncertainty. (Deng et al., 2020) `ev:reported` p. 6 ^deng2020deep-014
- The Multimodal Bingham Network predicts a [[Bingham distribution|multimodal Bingham distribution]] to capture different modes lying in the data, thus dissolving [[Pose ambiguity from symmetry|ambiguities]]. (Deng et al., 2020) `ev:reported` p. 6 ^deng2020deep-015
- The Deep Bingham Network definitions are agnostic of the backbone and can be combined with existing networks other than those reported. (Deng et al., 2020) `ev:asserted` p. 6 ^deng2020deep-016
- The normalization constant F is read from a lookup table precomputed over a predefined range of concentration values, enabling fast inference and gradient flow. (Deng et al., 2020) `ev:reported` p. 7 ^deng2020deep-017
- The entropy of the [[Bingham distribution|predicted Bingham distribution]] is passed through a sigmoid to give an uncertainty score in the range (0, 1). (Deng et al., 2020) `ev:reported` p. 7 ^deng2020deep-018
- The unimodal network is trained by minimizing the negative log-likelihood of the ground-truth rotation under the [[Bingham distribution|predicted Bingham distribution]]. (Deng et al., 2020) `ev:reported` p. 7 ^deng2020deep-019
- The unimodal network grants predictions uncertainty information but cannot handle ambiguities such as objects with [[Pose ambiguity from symmetry|rotational symmetries]]. (Deng et al., 2020) `ev:asserted` p. 7 ^deng2020deep-020
- The authors state that their mixture model trained with the mixture Bingham loss alone easily suffers from mode collapse. (Deng et al., 2020) `ev:asserted` p. 8 ^deng2020deep-021
- In winner-takes-all training, each iteration updates only the branch that generates the prediction closest to the ground truth. (Deng et al., 2020) `ev:reported` p. 8 ^deng2020deep-022
- The selected mixture component is chosen either by the l1 distance of predicted quaternions or by the highest ground-truth probability. (Deng et al., 2020) `ev:reported` p. 8 ^deng2020deep-023
- The relaxed winner-takes-all loss weights the selected component by 1 − ϵ and spreads ϵ over the remaining components. (Deng et al., 2020) `ev:reported` p. 9 ^deng2020deep-024
- Two training schemes are proposed, combining the RWTA loss with either a cross entropy loss on weights or the mixture Bingham loss. (Deng et al., 2020) `ev:reported` p. 9 ^deng2020deep-025
- For camera relocalization, translations are modelled by mixture density networks with multivariate Gaussians whose diagonal variances are predicted. (Deng et al., 2020) `ev:reported` p. 9 ^deng2020deep-026
- Camera pose hypothesis uncertainty is the sum of normalized rotational Bingham entropy and normalized translational Gaussian entropy. (Deng et al., 2020) `ev:reported` p. 9 ^deng2020deep-027
- Relocalization models use a ResNet-34 backbone trained with ADAM for 300 epochs with a batch size of 20 images. (Deng et al., 2020) `ev:reported` p. 10 ^deng2020deep-028
- The authors created real ambiguous scenes with Google Tango and RTAB-Map, with training and test sets of 2414 and 1326 frames. (Deng et al., 2020) `ev:reported` p. 10 ^deng2020deep-029
- Evaluation adds an Oracle error, choosing the hypothesis closest to ground truth, and Self-EMD as a measure of prediction diversity. (Deng et al., 2020) `ev:reported` p. 10 ^deng2020deep-030
- On 7-Scenes and Cambridge Landmarks, the Bingham networks achieve median errors similar to single-prediction methods such as PoseNet and MapNet. (Deng et al., 2020) `ev:measured` p. 11 ^deng2020deep-031
- Especially in translation, the method outperforms the uncertainty methods Bayesian-PoseNet and VidLoc on most scenes of these non-ambiguous datasets. (Deng et al., 2020) `ev:measured` p. 11 ^deng2020deep-032
- As the most uncertain predictions are removed, the mean pose error drops on most scenes, indicating uncertainty correlates with actual error. (Deng et al., 2020) `ev:measured` p. 11 ^deng2020deep-033
- On the synthetic dining-table scene, MC-Dropout obtains a mode accuracy of 50%, whereas MBN-CE achieves 96% on average. (Deng et al., 2020) `ev:measured` p. 12 ^deng2020deep-034
- On the synthetic round-table scene, the model shows an average mode detection rate of 99.1%, compared with 24.8% for MC-Dropout. (Deng et al., 2020) `ev:measured` p. 12 ^deng2020deep-035
- Averaged over the five real ambiguous scenes at 20°/0.3m, MBN-10 reaches 0.71 correct poses, versus 0.60 for PoseNet. (Deng et al., 2020) `ev:measured` p. 12 ^deng2020deep-036
- On the Meeting Table scene at 20°/0.3m, PoseNet reaches 0.10 correct poses, while MBN-10 reaches 0.42. (Deng et al., 2020) `ev:measured` p. 12 ^deng2020deep-037
- Self-EMD of MBN ranges from 1.20 to 4.35 across the ambiguous scenes, compared with 0.06 to 0.26 for MC-Dropout. (Deng et al., 2020) `ev:measured` p. 12 ^deng2020deep-038
- On the Blue Chairs scene at a 0.2 m threshold, MBN-CE detects 0.79 of ground-truth modes, against 0.15 for MC-Dropout. (Deng et al., 2020) `ev:measured` p. 12 ^deng2020deep-039
- Ground-truth modes for two real scenes were extracted semi-automatically with autoencoder features, nearest neighbours and Riemannian Mean Shift clustering. (Deng et al., 2020) `ev:reported` p. 12 ^deng2020deep-040
- Qualitatively, MC-Dropout and the finite mixture model MBN-MB suffer from mode collapse on the synthetic and real ambiguous scenes. (Deng et al., 2020) `ev:measured` p. 14 ^deng2020deep-041
- On the Meeting Table scene, baseline camera poses fall on the opposite side of the ground truth due to its symmetric structure. (Deng et al., 2020) `ev:measured` p. 14 ^deng2020deep-042
- At 20°/0.3m, MBN oracle accuracy rises from 0.69 with 5 hypotheses to 0.84 with 50, versus 0.70 for MC-Dropout. (Deng et al., 2020) `ev:measured` p. 14 ^deng2020deep-043
- Regardless of the ResNet or Inception-v3 backbone used, MBN-CE and MBN show on average superior performance over the baseline methods. (Deng et al., 2020) `ev:measured` p. 15 ^deng2020deep-044
- For camera relocalization, the authors found l1-based branch selection to outperform selection by highest probability density. (Deng et al., 2020) `ev:measured` p. 15 ^deng2020deep-045
- In point cloud experiments, each class gets its own PointNet-based network, trained for 500 epochs with a learning rate of 0.001. (Deng et al., 2020) `ev:reported` p. 15 ^deng2020deep-046
- Point cloud predictions are evaluated by Chamfer distance, the authors deeming angular error inappropriate under potential ambiguities of the objects. (Deng et al., 2020) `ev:reported` p. 16 ^deng2020deep-047
- Point cloud evaluation uses ModelNet10, whose 10 classes have different levels of symmetry, following the original train/test split. (Deng et al., 2020) `ev:reported` p. 16 ^deng2020deep-048
- Baselines include networks trained with L1, cosine and PLoss losses in a common framework, plus PointNetLK and IT-Net. (Deng et al., 2020) `ev:reported` p. 16 ^deng2020deep-049
- On ModelNet10, UBN averages a scaled Chamfer distance of 1.477, against 1.993 for PLoss and 3.605 for L1. (Deng et al., 2020) `ev:measured` p. 16 ^deng2020deep-050
- MBN-10 obtains an average scaled Chamfer distance of 0.838 on ModelNet10, compared with 1.477 for the unimodal network. (Deng et al., 2020) `ev:measured` p. 16 ^deng2020deep-051
- PointNetLK and IT-Net reach average scaled Chamfer distances of 10.410 and 8.180 on ModelNet10 in this evaluation. (Deng et al., 2020) `ev:measured` p. 16 ^deng2020deep-052
- The authors attribute UBN's improvement to the [[Bingham distribution]] enabling an anisotropic distance that accounts for uncertainty in directions. (Deng et al., 2020) `ev:asserted` p. 17 ^deng2020deep-053
- Increasing mixture components from 5 to 10 improves results, whereas increasing them to 25 or 50 brings no further improvement. (Deng et al., 2020) `ev:measured` p. 17 ^deng2020deep-054
- The authors suggest this sweet spot indicates saturation of mode diversity, where excessive over-parameterization of modes causes complexity in learning. (Deng et al., 2020) `ev:asserted` p. 17 ^deng2020deep-055
- As the uncertainty threshold decreases, average Chamfer distances also decrease, indicating less uncertain predictions tend to align point clouds better. (Deng et al., 2020) `ev:measured` p. 17 ^deng2020deep-056
- In partial scan registration, uncertainty filtering drops 0.541 of hypotheses while average recall falls from 0.777 to 0.730. (Deng et al., 2020) `ev:measured` p. 17 ^deng2020deep-057
- For object pose estimation, probability-based branch selection gives an average Chamfer distance of 0.973, versus 1.057 with L1 selection. (Deng et al., 2020) `ev:measured` p. 18 ^deng2020deep-058
- For non-ambiguous objects all mixture components tend to agree, which could be used to indicate whether a point cloud is rotationally symmetric. (Deng et al., 2020) `ev:measured` p. 18 ^deng2020deep-059
- For object pose estimation, the Birdal construction gives an MBN Chamfer distance of 0.973, against 2.867 for Gram-Schmidt and 1.597 for Cayley. (Deng et al., 2020) `ev:measured` p. 19 ^deng2020deep-060
- For camera relocalization with UBN and MBN-MB, the skew-symmetric Cayley construction outperformed both Gram-Schmidt and the Birdal method. (Deng et al., 2020) `ev:measured` p. 19 ^deng2020deep-061
- On ModelNet10, winner-takes-all losses raise Self-EMD over the mixture Bingham loss alone, with WTA reaching 0.777 versus 0.425. (Deng et al., 2020) `ev:measured` p. 20 ^deng2020deep-062
- On ModelNet10, the RWTA loss lowers the average Chamfer distance to 0.973, from 1.237 with the mixture Bingham loss alone. (Deng et al., 2020) `ev:measured` p. 20 ^deng2020deep-063
- With the [[Rotation representation continuity|continuous 6D rotation representation]], MBN averages 0.67 correct relocalization poses at 20°/0.3m, versus 0.35 for a plain MDN. (Deng et al., 2020) `ev:measured` p. 21 ^deng2020deep-064
- The authors conclude that their model is superior to the state of the art on both tasks, obtaining consistently better mode predictions. (Deng et al., 2020) `ev:asserted` p. 21 ^deng2020deep-065
- The authors believe their solutions can be incorporated into other neural network-based pose estimation applications without heavy modifications. (Deng et al., 2020) `ev:asserted` p. 21 ^deng2020deep-066

## 🎯 Contributions

## 📖 Glossary

- **Bingham distribution** — Antipodally symmetric distribution on the unit sphere, derived from a zero-mean Gaussian.
- **Concentration matrix** — Diagonal non-positive matrix Λ setting how peaked a Bingham distribution is.
- **Mixture Density Network (MDN)** — Network that outputs the parameters of a mixture distribution for each input.
- **Mode collapse** — Failure where all mixture components or hypotheses converge on one mode.
- **Winner-takes-all (WTA)** — Multi-hypothesis training that updates only the hypothesis closest to ground truth.
- **Relaxed WTA (RWTA)** — WTA variant giving non-selected hypotheses a small ϵ share of gradient.
- **Evolving WTA (EWTA)** — WTA variant updating the top k hypotheses, with k decreasing during training.
- **Self-EMD (SEMD)** — Earth mover's distance from a multimodal prediction to its unimodal mode, measuring diversity.
- **Oracle error** — Error of the hypothesis closest to ground truth among all predictions.
- **Chamfer distance** — Point-set distance used here to score rotations of possibly symmetric objects.
- **Cayley transform** — Map from skew-symmetric matrices to special orthogonal matrices.

## ❓ Open questions

- How should the number of mixture components be chosen, given that gains saturate beyond 10 on ModelNet10?
- Why does l1-based branch selection win for relocalization while probability selection is close or better for point clouds?
- Does the lookup-table approximation of the normalization constant limit accuracy for very concentrated distributions?
- Can the object symmetry axes suggested by the spread of mixture components be extracted reliably and evaluated quantitatively?
- How well do the entropy-based uncertainties calibrate, beyond the monotone error-versus-threshold curves shown?
- Would class-agnostic training (one network for all classes) preserve the point cloud results?

## 📝 Notes on reading

Version read: arXiv 2012.11002v1 (20 Dec 2020), matching the packet identifier. It extends the ECCV 2020 relocalization paper of Bui et al. (ref. 22).

Inconsistencies: page 17 says UBN achieves the best performance across all classes, but Table 7 (p. 16) shows lower Chamfer distances for L1 and PLoss on Chair (0.653, 0.859 vs 0.999) and on Toilet (0.609, 0.582 vs 0.846). Table 1 caption cites Bayesian-PoseNet as [18] while the text cites it as [51]. The Fig. 1 caption says DBM rather than DBN. On p. 9 the text lists Cross Entropy + RWTA first but names the schemes MBN and MBN-CE respectively, which reads reversed relative to the later usage (MBN-CE = cross entropy scheme).

Garbled extraction: Table 7 caption reads scaled by 102 (presumably 10^2); Fig. 11 axis label is garbled, so its Chamfer values were not claimed. Equations (1)-(11) and the matrix V(q) are partially garbled. Figures 4-10, 12 and 13 are plots or qualitative views and were described only in text; Fig. 8 bar values were not claimed. Several details were left out to stay under the claim cap: synthetic table scenes from 3DWarehouse, 100 random quaternions sampled per epoch, the strong influence of k in EWTA, and the cited discontinuity of rotation representations with four or fewer degrees of freedom (p. 20).

## Suggested new concepts

- Bingham distribution — the central directional distribution on unit quaternions, reused across pose-uncertainty papers.
- Mixture density networks — the base architecture whose mode collapse this paper and others try to fix.
- Winner-takes-all multi-hypothesis training — family of losses (WTA, RWTA, EWTA) for ambiguous prediction.
- Pose ambiguity from symmetry — recurring problem across object pose and camera relocalization work.
- Camera relocalization — task of regressing 6-DoF camera pose from an image, with its own benchmarks.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Mezclas de Bingham sobre cuaterniones
