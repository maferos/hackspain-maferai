---
aliases: []
type: "source"
title: "BOP: Benchmark for 6D Object Pose Estimation"
citekey: "Hodan2018bop"
doi: "10.48550/arXiv.1808.08319"
arxiv: "1808.08319"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1808.08319"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Tomas Hodan", "Frank Michel", "Eric Brachmann", "Wadim Kehl", "Anders Glent Buch", "Dirk Kraft", "Bertram Drost", "Joel Vidal", "Stephan Ihrke", "Xenophon Zabulis", "Caner Sahin", "Fabian Manhardt", "Federico Tombari", "Tae-Kyun Kim", "Jiri Matas", "Carsten Rother"]
sha256: ["172781ddcbabfdf1716d080d1878fbdc7a7ab602b184c2941cfe316397726b2c"]
pdf: "Content/Papers/Hodan2018bop.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Hodan2018bop.pdf]]

> [!abstract] One-sentence summary
> BOP unifies eight RGB-D datasets, an ambiguity-aware pose-error function (VSD) and an evaluation of 15 methods into a benchmark for single-image 6D object pose estimation, finding point-pair-feature methods best and occlusion, lighting and symmetry the open problems.

## Abstract
We propose a benchmark for 6D pose estimation of a rigid object from a single RGB-D input image. The training data consists of a texture-mapped 3D object model or images of the object in known 6D poses. The benchmark comprises of: i) eight datasets in a unified format that cover different practical scenarios, including two new datasets focusing on varying lighting conditions, ii) an evaluation methodology with a pose-error function that deals with pose ambiguities, iii) a comprehensive evaluation of 15 diverse recent methods that captures the status quo of the field, and iv) an online evaluation system that is open for continuous submission of new results. The evaluation shows that methods based on point-pair features currently perform best, outperforming template matching methods, learning-based methods and methods based on 3D local features. The project website is available at bop.felk.cvut.cz. (arXiv)

## 🧠 Key ideas (atomic)

- The most commonly used evaluation dataset, created by Hinterstoisser et al., was not intended as a general benchmark and has several limitations. (Hodan et al., 2018) `ev:cited` p. 1 ^hodan2018bop-001
- In the Hinterstoisser et al. dataset the lighting is constant and objects are easy to distinguish, unoccluded and located around the image center. (Hodan et al., 2018) `ev:cited` p. 1 ^hodan2018bop-002
- According to the authors, no standard evaluation methodology for 6D object pose estimation has emerged across the existing datasets. (Hodan et al., 2018) `ev:asserted` p. 1 ^hodan2018bop-003
- [[BOP benchmark|The benchmark]] provides eight datasets in a unified format, including two new datasets focusing on varying lighting conditions. (Hodan et al., 2018) `ev:reported` p. 2 ^hodan2018bop-004
- The datasets contain texture-mapped 3D models of 89 objects with a wide range of sizes, shapes and reflectance properties. (Hodan et al., 2018) `ev:reported` p. 2 ^hodan2018bop-005
- The benchmark datasets include 277K training RGB-D images that show isolated objects captured from different viewpoints. (Hodan et al., 2018) `ev:reported` p. 2 ^hodan2018bop-006
- The benchmark datasets include 62K test RGB-D images of scenes with graded complexity, annotated with high-quality ground-truth 6D poses. (Hodan et al., 2018) `ev:reported` p. 2 ^hodan2018bop-007
- The authors state that their pose-error function deals well with [[Pose ambiguity from symmetry|pose ambiguity]] of symmetric or partially occluded objects, unlike the Hinterstoisser function. (Hodan et al., 2018) `ev:asserted` p. 2 ^hodan2018bop-008
- An online evaluation system at bop.felk.cvut.cz allows continuous submission of new results to [[BOP benchmark|the benchmark]]. (Hodan et al., 2018) `ev:reported` p. 2 ^hodan2018bop-009
- The authors combined existing datasets to cover many practical scenarios instead of recording large amounts of new data. (Hodan et al., 2018) `ev:reported` p. 3 ^hodan2018bop-010
- The goal of the task is to estimate the 6D pose of one instance of the target object visible in the test image. (Hodan et al., 2018) `ev:reported` p. 3 ^hodan2018bop-011
- If a test image shows multiple annotated object models, each object model may define a different test target. (Hodan et al., 2018) `ev:reported` p. 3 ^hodan2018bop-012
- The task reflects an industry-relevant bin-picking scenario where a robot needs to grasp a single arbitrary instance of the required object. (Hodan et al., 2018) `ev:asserted` p. 4 ^hodan2018bop-013
- Visible Surface Discrepancy renders the object model in the estimated and ground-truth poses to obtain two distance maps. (Hodan et al., 2018) `ev:reported` p. 4 ^hodan2018bop-014
- The rendered distance maps are compared with the test image distance map to obtain masks of pixels where the model is visible. (Hodan et al., 2018) `ev:reported` p. 4 ^hodan2018bop-015
- The error eVSD is calculated only over the visible part of the model surface, so [[Pose ambiguity from symmetry|indistinguishable poses]] are treated as equivalent. (Hodan et al., 2018) `ev:asserted` p. 4 ^hodan2018bop-016
- Unlike the original definition, the new eVSD definition does not penalize small distance differences that may be caused by depth sensor imprecision. (Hodan et al., 2018) `ev:asserted` p. 4 ^hodan2018bop-017
- An estimated pose is considered correct with respect to the ground-truth pose if its eVSD error is below the threshold θ. (Hodan et al., 2018) `ev:reported` p. 5 ^hodan2018bop-018
- For robotic manipulation both tolerances need to be low, e.g. τ = 20 mm and θ = 0.3, the default evaluation setting. (Hodan et al., 2018) `ev:asserted` p. 5 ^hodan2018bop-019
- For augmented reality, the tolerance τ can be relaxed because Z-axis alignment is less important, but θ needs to stay low. (Hodan et al., 2018) `ev:asserted` p. 5 ^hodan2018bop-020
- Hinterstoisser et al. consider an estimated pose correct if [[ADD and ADD-S metrics|the eADD or eADI error]] is at most 0.1 times the object diameter. (Hodan et al., 2018) `ev:cited` p. 6 ^hodan2018bop-021
- [[ADD and ADD-S metrics|Error eADI]] can be un-intuitively low because of many-to-one vertex matching established by the search for the closest vertex. (Hodan et al., 2018) `ev:asserted` p. 6 ^hodan2018bop-022
- In Fig. 3, estimates (f)-(n) satisfy the Hinterstoisser correctness criterion but are not considered correct by the eVSD criterion. (Hodan et al., 2018) `ev:measured` p. 6 ^hodan2018bop-023
- The authors collected six publicly available datasets, reducing some to remove redundancies and re-annotating them to ensure high ground-truth quality. (Hodan et al., 2018) `ev:reported` p. 6 ^hodan2018bop-024
- The benchmark focuses primarily on the practical scenario where only object models, usable to render synthetic training images, are available. (Hodan et al., 2018) `ev:asserted` p. 6 ^hodan2018bop-025
- Only T-LESS and TUD-L include real training images of isolated, non-occluded objects among the eight benchmark datasets. (Hodan et al., 2018) `ev:reported` p. 6 ^hodan2018bop-026
- [[Synthetic training data for 6D pose estimation|Synthetic training images]] were rendered with fixed lighting conditions and a black background from viewpoints sampled on a sphere. (Hodan et al., 2018) `ev:reported` p. 6 ^hodan2018bop-027
- Across all benchmark datasets, Table 1 lists 89 objects, 62155 test images and 110793 test targets in total. (Hodan et al., 2018) `ev:reported` p. 7 ^hodan2018bop-028
- Test images are real images from a structured-light sensor, either Microsoft Kinect v1 or Primesense Carmine 1.09. (Hodan et al., 2018) `ev:reported` p. 7 ^hodan2018bop-029
- LM, also known as Linemod, contains 15 texture-less household objects with discriminative color, shape and size. (Hodan et al., 2018) `ev:reported` p. 7 ^hodan2018bop-030
- LM-O provides ground-truth annotation for all other modeled object instances in one LM test set, introducing various occlusion levels. (Hodan et al., 2018) `ev:reported` p. 7 ^hodan2018bop-031
- T-LESS features 30 industry-relevant objects with no significant texture or discriminative color, exhibiting symmetries and mutual similarities. (Hodan et al., 2018) `ev:reported` p. 7 ^hodan2018bop-032
- RU-APC includes 14 textured products from the Amazon Picking Challenge 2015, each with test images of a cluttered warehouse shelf. (Hodan et al., 2018) `ev:reported` p. 8 ^hodan2018bop-033
- TUD-L contains training and test image sequences showing three moving objects under eight lighting conditions. (Hodan et al., 2018) `ev:reported` p. 8 ^hodan2018bop-034
- TYO-L contains 21 objects captured on a table-top setup with four different table cloths and five different lighting conditions. (Hodan et al., 2018) `ev:reported` p. 8 ^hodan2018bop-035
- Hodan-15 templates were generated by applying the full circle of in-plane rotations, resulting in 11–23K templates per object. (Hodan et al., 2018) `ev:reported` p. 10 ^hodan2018bop-036
- The number of RANSAC iterations for Buch-16 was set to 10000, allowing only for a limited search in cluttered scenes. (Hodan et al., 2018) `ev:reported` p. 11 ^hodan2018bop-037
- Buch-17 has time complexity linear in the number of correspondences, since each correspondence votes in a 1-DoF rotational subgroup of SE(3). (Hodan et al., 2018) `ev:asserted` p. 11 ^hodan2018bop-038
- All methods were evaluated by their original authors on the benchmark datasets using the proposed evaluation methodology. (Hodan et al., 2018) `ev:reported` p. 11 ^hodan2018bop-039
- Only ground-truth poses in which the object is visible from at least 10% were considered in the evaluation. (Hodan et al., 2018) `ev:reported` p. 11 ^hodan2018bop-040
- Overall performance is the average of per-dataset recall scores, which avoids the overall score being dominated by larger datasets. (Hodan et al., 2018) `ev:reported` p. 11 ^hodan2018bop-041
- From the total of 62K test images, 7K were sub-sampled for evaluation, reducing test targets from 110K to 17K. (Hodan et al., 2018) `ev:reported` p. 12 ^hodan2018bop-042
- In the benchmark evaluation, the ranking of methods according to recall score is mostly stable across the datasets. (Hodan et al., 2018) `ev:measured` p. 12 ^hodan2018bop-043
- Vidal-18 is the top-performing method with an average recall of 74.6% at τ = 20 mm and θ = 0.3. (Hodan et al., 2018) `ev:measured` p. 12 ^hodan2018bop-044
- Drost-10-edge, Drost-10 and the template matching method Hodan-15 follow Vidal-18, all with average recall above 67%. (Hodan et al., 2018) `ev:measured` p. 12 ^hodan2018bop-045
- Brachmann-16 is the best learning-based method in the evaluation, with an average recall of 55.4%. (Hodan et al., 2018) `ev:measured` p. 12 ^hodan2018bop-046
- Buch-17-ppfh is the best method based on 3D local features, with an average recall of 54.0%. (Hodan et al., 2018) `ev:measured` p. 12 ^hodan2018bop-047
- Increasing the misalignment tolerance τ from 20 mm to 80 mm increases the scores only slightly for most methods. (Hodan et al., 2018) `ev:measured` p. 12 ^hodan2018bop-048
- The authors suggest that poses estimated by most methods are either of a high quality or totally off. (Hodan et al., 2018) `ev:asserted` p. 12 ^hodan2018bop-049
- The reported running times are not directly comparable because the methods were evaluated on different computers. (Hodan et al., 2018) `ev:asserted` p. 12 ^hodan2018bop-050
- Drost-10 running time can be lowered by a factor of ∼5 to 0.5 s, with average recall dropping from 68.1% to 65.8%. (Hodan et al., 2018) `ev:measured` p. 12 ^hodan2018bop-051
- All methods perform on LM by at least 30% better than on LM-O, which includes the same but partially occluded objects. (Hodan et al., 2018) `ev:measured` p. 12 ^hodan2018bop-052
- Recall scores drop swiftly already at low levels of occlusion, which the authors take as showing occlusion is a big challenge. (Hodan et al., 2018) `ev:measured` p. 12 ^hodan2018bop-053
- On the TUD-L dataset, Brachmann-16 reaches a recall of 88.67, the highest value in Table 2 for that dataset. (Hodan et al., 2018) `ev:measured` p. 13 ^hodan2018bop-054
- Varying lighting conditions present a serious challenge for methods relying on [[Synthetic training data for 6D pose estimation|synthetic training RGB images generated with fixed lighting]]. (Hodan et al., 2018) `ev:measured` p. 12 ^hodan2018bop-055
- Methods relying only on depth information, such as Vidal-18 and Drost-10, are noticeably more robust under varying lighting conditions. (Hodan et al., 2018) `ev:measured` p. 14 ^hodan2018bop-056
- Brachmann-16 scored high on TUD-L because it used real training images captured under the same range of lighting conditions. (Hodan et al., 2018) `ev:asserted` p. 14 ^hodan2018bop-057
- Very low scores of 3D-local-feature and learning-based methods on T-LESS are likely caused by [[Pose ambiguity from symmetry|object symmetries and similarities]]. (Hodan et al., 2018) `ev:asserted` p. 14 ^hodan2018bop-058
- All methods perform poorly on RU-APC, which the authors attribute likely to a higher level of noise in depth images. (Hodan et al., 2018) `ev:asserted` p. 14 ^hodan2018bop-059
- The authors identify occlusion, varying lighting conditions, and object symmetries and similarities as open problems of the field. (Hodan et al., 2018) `ev:asserted` p. 14 ^hodan2018bop-060

## 🎯 Contributions

## 📖 Glossary
- **6D pose** — 3D translation and 3D rotation of a rigid object relative to the camera.
- **Test target** — Pair of a test image and an object identifier whose pose must be estimated.
- **VSD (Visible Surface Discrepancy)** — Pose error computed only over visible model surface from rendered distance maps.
- **Distance map** — Per-pixel distance from camera center to the 3D point projecting there.
- **Misalignment tolerance τ** — Per-pixel distance difference under which surfaces count as aligned in VSD.
- **Correctness threshold θ** — Maximum VSD error for an estimated pose to count as correct.
- **ADD / ADI** — Average vertex distance errors, same-vertex or closest-vertex, from Hinterstoisser et al.
- **Point-pair features (PPF)** — Descriptors of oriented point pairs matched via hash table and local voting.
- **Recall score** — Fraction of test targets for which a correct object pose was estimated.
- **ICP** — Iterative Closest Point, a refinement aligning a model to observed 3D points.

## ❓ Open questions
- How can 6D pose methods be made robust to occlusion, given scores drop swiftly at low occlusion levels?
- How can RGB-based methods trained on fixed-lighting synthetic images cope with varying lighting at test time?
- How should methods handle object symmetries and inter-object similarities such as those in T-LESS?
- What speed/accuracy trade-offs exist for the evaluated methods when compared on identical hardware (left for future work)?
- Would synthesizing additional training images, allowed but unused here, change the ranking of image-based methods?
- Why do all methods perform poorly on RU-APC, and is depth noise the actual cause?

## 📝 Notes on reading
- Version read: arXiv preprint 1808.08319v1 (24 Aug 2018), matching the packet identifier.
- Table 3 (per-object recall, p. 13) is badly garbled in the extraction: object columns and rows are interleaved, so per-object values were not claimed.
- Fig. 1 (dataset examples and object models) and Fig. 2 (VSD quantities) could only be described; the figure numbering in the extraction is noise.
- Fig. 3 pairs eVSD values with eADI/θAD values for 16 example estimates (a)-(p); only its qualitative conclusion in the text was claimed.
- Fig. 4 curves (recall vs θ at τ = 20 and 80 mm; recall vs visible fraction) exist only as axis ticks in the extraction; claims rest on the text of p. 12.
- Naming inconsistency: the text calls the no-refinement variant Hodan-15-nr, while Table 2 labels it Hodan-15-nopso and Table 3 Hodan-15-nr.
- The "15 methods" are 15 rows of Table 2, several of which are descriptor variants of Buch-16 and Buch-17; Buch-16-si and Buch-16-shot results are omitted as inferior.
- The benchmark has eight datasets, but TYO-L was not part of the evaluation in this paper, so Table 2 covers seven.
- The Related Work cites the Hinterstoisser evaluation function as [13] on p. 3 but as [14] elsewhere.

## Suggested new concepts
- Visible Surface Discrepancy (VSD) — ambiguity-invariant pose-error function reused across later BOP challenges.
- BOP benchmark — standard dataset collection and leaderboard for 6D object pose estimation.
- Point pair features — the method family that led this evaluation; relevant for depth-based object localization.
- Pose ambiguity from symmetry — recurring difficulty for pose error metrics and learning-based estimators.
- Sim-to-real lighting gap — synthetic fixed-lighting training images failing under varying real lighting.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Definición original del benchmark y del formato
