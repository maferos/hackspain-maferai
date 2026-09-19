---
aliases: []
type: "source"
title: "Robotic Perception of Transparent Objects: A Review"
citekey: "Jiang2023robotic"
doi: "10.48550/arXiv.2304.00157"
arxiv: "2304.00157"
year: 2023
publication_type: "preprint"
url: "https://arxiv.org/abs/2304.00157"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Jiaqi Jiang", "Guanqun Cao", "Jiankang Deng", "Thanh-Toan Do", "Shan Luo"]
sha256: ["f9a3a4445aa450bfb869beec0a2b520f41b1536d8be6d893899b5263600cb4d7"]
pdf: "Content/Papers/Jiang2023robotic.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 68
---

📄 PDF: [[Jiang2023robotic.pdf]]

> [!abstract] One-sentence summary
> A survey of the sensors, rendering platforms, datasets and methods for segmenting, reconstructing and estimating the pose of transparent objects in robotics, closing with a map of open challenges.

## Abstract

Transparent object perception is a rapidly developing research problem in artificial intelligence. The ability to perceive transparent objects enables robots to achieve higher levels of autonomy, unlocking new applications in various industries such as healthcare, services and manufacturing. Despite numerous datasets and perception methods being proposed in recent years, there is still a lack of in-depth understanding of these methods and the challenges in this field. To address this gap, this article provides a comprehensive survey of the platforms and recent advances for robotic perception of transparent objects. We highlight the main challenges and propose future directions of various transparent object perception tasks, i.e., segmentation, reconstruction, and pose estimation. We also discuss the limitations of existing datasets in diversity and complexity, and the benefits of employing multi-modal sensors, such as RGB-D cameras, thermal cameras, and polarised imaging, for transparent object perception. Furthermore, we identify perception challenges in complex and dynamic environments, as well as for objects with changeable geometries. Finally, we provide an interactive online platform to navigate each reference: \url{https://sites.google.com/view/transperception}. (arXiv)

## 🧠 Key ideas (atomic)

- Transparent objects lack salient surface features such as colour and texture, making their appearance highly dependent on the image background. (Jiang et al., 2023) `ev:asserted` p. 1 ^jiang2023robotic-001
- Transparent surfaces both reflect and refract light, which breaks the Lambertian assumption underlying optical 3D sensors such as LiDAR and RGB-D cameras. (Jiang et al., 2023) `ev:asserted` p. 1 ^jiang2023robotic-002
- The authors state that depth data captured on transparent objects is either invalid or contains unpredictable noise, complicating their perception. (Jiang et al., 2023) `ev:asserted` p. 1 ^jiang2023robotic-003
- The authors frame current research as addressing two key problems: locating transparent objects and [[Transparent object depth completion|accurately estimating their depth]]. (Jiang et al., 2023) `ev:asserted` p. 2 ^jiang2023robotic-004
- The most recent prior survey on transparent object perception, published over a decade ago, primarily focused on reconstruction methods limited to controlled environments. (Jiang et al., 2023) `ev:cited` p. 2 ^jiang2023robotic-005
- The authors claim this is the first survey specifically focused on the robotic perception of transparent objects, to the best of their knowledge. (Jiang et al., 2023) `ev:asserted` p. 2 ^jiang2023robotic-006
- Monocular RGB cameras are judged unsuitable for transparent object perception since they capture only intensity information. (Jiang et al., 2023) `ev:asserted` p. 2 ^jiang2023robotic-007
- Type I depth errors occur when light refracts through the transparent material and the camera returns the depth of the background surface. (Jiang et al., 2023) `ev:asserted` p. 3 ^jiang2023robotic-008
- Type II depth errors arise when specular highlights alter the projected infrared patterns, causing incorrect stereo matching and missing depth for the object. (Jiang et al., 2023) `ev:asserted` p. 3 ^jiang2023robotic-009
- Processing light-field data can be computationally intensive, which may limit the effectiveness and applicability of light-field cameras for transparent objects. (Jiang et al., 2023) `ev:asserted` p. 3 ^jiang2023robotic-010
- Studies cited by the review show polarised cameras outperforming conventional RGB cameras in transparent object segmentation tasks. (Jiang et al., 2023) `ev:cited` p. 3 ^jiang2023robotic-011
- Polarised cameras have yet to see widespread robotic use due to high prices, such as £2,000 for a Phoenix 5.0 MP camera. (Jiang et al., 2023) `ev:asserted` p. 3 ^jiang2023robotic-012
- Transparent materials can be opaque to thermal radiation in the range of 8 to 12 µm, due to absorption and scattering by atomic bonds. (Jiang et al., 2023) `ev:cited` p. 4 ^jiang2023robotic-013
- Compared to traditional RGB cameras, thermal cameras capture fewer arbitrary textures on transparent surfaces such as glass. (Jiang et al., 2023) `ev:asserted` p. 4 ^jiang2023robotic-014
- Thermal camera prices vary greatly, from a few hundred dollars for the FLIR ONE Pro to tens of thousands for the FLIR A65. (Jiang et al., 2023) `ev:asserted` p. 4 ^jiang2023robotic-015
- Tactile sensors are not influenced by the diverse appearance of transparent objects, making them a good complement to cameras. (Jiang et al., 2023) `ev:asserted` p. 4 ^jiang2023robotic-016
- Except for tactile sensors, all six reviewed sensor types can sense a medium or large field, suiting remote perception of transparent objects. (Jiang et al., 2023) `ev:asserted` p. 4 ^jiang2023robotic-017
- Stereo cameras and light-field cameras rely on visible light and may be less effective in low-light conditions. (Jiang et al., 2023) `ev:asserted` p. 4 ^jiang2023robotic-018
- RGB-Thermal cameras and polarised cameras can capture images of transparent objects in low-light conditions with good contrast and clarity. (Jiang et al., 2023) `ev:asserted` p. 4 ^jiang2023robotic-019
- The authors identify a trade-off where high-performance sensors, such as polarised and RGB-Thermal cameras, typically carry a high cost. (Jiang et al., 2023) `ev:asserted` p. 4 ^jiang2023robotic-020
- In Blender, the Eevee engine provides the fastest rendering speeds but often produces unrealistic results for transparent objects. (Jiang et al., 2023) `ev:asserted` p. 5 ^jiang2023robotic-021
- Since Blender 3.2, Cycles supports selective rendering of caustics in refractive object shadows, with only up to 4 refractive caustic bounces. (Jiang et al., 2023) `ev:reported` p. 5 ^jiang2023robotic-022
- In the authors' Blender rendering comparison, Eevee and Cycles (old) were unable to simulate artefacts such as caustics. (Jiang et al., 2023) `ev:measured` p. 5 ^jiang2023robotic-023
- LuxCoreRender outperformed Cycles (new) in caustic rendering quality in the authors' Blender comparison, at the cost of higher computational expense. (Jiang et al., 2023) `ev:measured` p. 5 ^jiang2023robotic-024
- The authors consider Blender and Omniverse the two most powerful simulation packages, both offering real-time and photorealistic rendering engines. (Jiang et al., 2023) `ev:asserted` p. 6 ^jiang2023robotic-025
- For segmentation and depth reconstruction tasks without robotic physics, the authors strongly recommend LuxCoreRender for its extensive documentation and photorealistic artefacts. (Jiang et al., 2023) `ev:asserted` p. 6 ^jiang2023robotic-026
- The Tom-Net dataset consists of 178k synthetic images rendered with POV-Ray and 876 real images of 14 transparent objects. (Jiang et al., 2023) `ev:cited` p. 6 ^jiang2023robotic-027
- The TransProteus dataset includes 50k synthetic Blender images and 104 real images captured with a RealSense D435 camera. (Jiang et al., 2023) `ev:cited` p. 7 ^jiang2023robotic-028
- The authors consider TransProteus one of the most challenging segmentation datasets, with 13k different objects, 500 environments and simulated liquids. (Jiang et al., 2023) `ev:asserted` p. 7 ^jiang2023robotic-029
- The RGB-T dataset contains 5,551 RGB and thermal image pairs whose raw 160×120 thermal images were upscaled to 640×480. (Jiang et al., 2023) `ev:cited` p. 7 ^jiang2023robotic-030
- Among the 11 reviewed segmentation datasets, synthetic datasets range from 9k to 100k images, mostly larger than real-world ones (49 to 10k). (Jiang et al., 2023) `ev:asserted` p. 7 ^jiang2023robotic-031
- Only the Polarised, SuperCaustics, TransTouch and TransProteus datasets provide instance segmentation labels among the reviewed transparent object datasets. (Jiang et al., 2023) `ev:asserted` p. 8 ^jiang2023robotic-032
- The authors propose Fractal Dimension and Mean Connected Components to quantitatively compare the complexity of glass-wall and window segmentation datasets. (Jiang et al., 2023) `ev:reported` p. 8 ^jiang2023robotic-033
- GSD scored the highest fractal dimension (1.076) and mean connected components (4.35) among five compared datasets, making it the most challenging. (Jiang et al., 2023) `ev:measured` p. 8 ^jiang2023robotic-034
- Early hand-crafted segmentation methods only work well under the strong assumption that the background is similar on both sides of glass edges. (Jiang et al., 2023) `ev:cited` p. 8 ^jiang2023robotic-035
- Recent transparent object segmentation studies increasingly use multi-modal information such as polarised and thermal images, whereas early work primarily relied on RGB data. (Jiang et al., 2023) `ev:asserted` p. 9 ^jiang2023robotic-036
- Complementary information such as boundaries remains less explored than feature fusion and attention mechanisms in transparent object segmentation work. (Jiang et al., 2023) `ev:asserted` p. 9 ^jiang2023robotic-037
- The main segmentation challenges are the limited scale of multi-modal datasets and the costly computation of large-scale segmentation architectures. (Jiang et al., 2023) `ev:asserted` p. 9 ^jiang2023robotic-038
- According to the authors, the most recent segmentation datasets include only 4k RGB-Polarisation images and 5k RGB-Thermal images, respectively. (Jiang et al., 2023) `ev:cited` p. 9 ^jiang2023robotic-039
- Current simulators such as Blender can provide photo-realistic RGB-D rendering but cannot simulate polarisation images or thermal images. (Jiang et al., 2023) `ev:asserted` p. 10 ^jiang2023robotic-040
- The authors suggest multi-modal simulators and domain-invariant feature learning as promising directions for Sim2Real transparent object segmentation. (Jiang et al., 2023) `ev:asserted` p. 10 ^jiang2023robotic-041
- It remains questionable whether semi-automatic labelling methods apply to transparent objects, whose appearance is inherited from the background. (Jiang et al., 2023) `ev:asserted` p. 10 ^jiang2023robotic-042
- For real-time segmentation, the authors suggest lightweight backbones on physical modalities like depth, polarisation and thermal instead of ultra-deep RGB networks. (Jiang et al., 2023) `ev:asserted` p. 10 ^jiang2023robotic-043
- Under low light, transparent objects may blend into the background due to low contrast, challenging their segmentation. (Jiang et al., 2023) `ev:asserted` p. 11 ^jiang2023robotic-044
- Traditional networks like Mask R-CNN and DeepLabv3+ have become less popular than newer encoder-decoder frameworks in recent transparent object segmentation studies. (Jiang et al., 2023) `ev:asserted` p. 11 ^jiang2023robotic-045
- ClearGrasp is the first large-scale [[Transparent object depth completion|depth reconstruction]] dataset for transparent objects, with 50k synthetic images and 286 real images. (Jiang et al., 2023) `ev:cited` p. 11 ^jiang2023robotic-046
- ClearGrasp obtained real-world depth by spraying transparent objects with rough stone textures that reflect light evenly. (Jiang et al., 2023) `ev:cited` p. 11 ^jiang2023robotic-047
- TODD has 14,659 images collected with six glass beakers and flasks in five backgrounds, annotated automatically using AprilTags. (Jiang et al., 2023) `ev:cited` p. 11 ^jiang2023robotic-048
- TransCG is a real-world dataset of 57,715 RGB-D images from 130 scenes, with depth generated using a PST optical tracker. (Jiang et al., 2023) `ev:cited` p. 12 ^jiang2023robotic-049
- The authors judge DREDS and TransCG the most challenging synthetic and real-world reconstruction datasets, based on numbers of objects and images. (Jiang et al., 2023) `ev:asserted` p. 12 ^jiang2023robotic-050
- DREDS is the only dataset providing raw depth data in simulation, enabling sim-to-real transfer for [[Transparent object depth completion|end-to-end depth reconstruction]]. (Jiang et al., 2023) `ev:asserted` p. 12 ^jiang2023robotic-051
- One visual hull refinement method takes around 46 seconds to reconstruct a transparent shape from 10 views on an RTX 2080 Ti. (Jiang et al., 2023) `ev:cited` p. 12 ^jiang2023robotic-052
- Dex-NeRF requires hours of computation for each scene, which deviates far from the real-time requirement of robotic applications. (Jiang et al., 2023) `ev:cited` p. 13 ^jiang2023robotic-053
- The authors list heavy computational cost, many required views and calibration sensitivity as disadvantages of NeRF-based transparent object reconstruction. (Jiang et al., 2023) `ev:asserted` p. 13 ^jiang2023robotic-054
- End-to-end single-view reconstruction requires large-scale datasets and is not robust to clutter, especially when two objects overlap. (Jiang et al., 2023) `ev:asserted` p. 13 ^jiang2023robotic-055
- In ClearGrasp's global optimisation, reconstructed depths become indeterministic and can take random values when regions are enclosed by occlusion boundaries. (Jiang et al., 2023) `ev:cited` p. 14 ^jiang2023robotic-056
- Single-view methods are generally more efficient than multi-view approaches due to their elimination of camera movement and lower computational costs. (Jiang et al., 2023) `ev:asserted` p. 14 ^jiang2023robotic-057
- Single-view techniques rely heavily on high-quality datasets and can suffer from poor lighting and clutter, limiting robustness compared to multi-view methods. (Jiang et al., 2023) `ev:asserted` p. 14 ^jiang2023robotic-058
- Real-world reconstruction ground truth is hard for human annotators to label, and existing approaches are time-consuming or need external markers. (Jiang et al., 2023) `ev:asserted` p. 14 ^jiang2023robotic-059
- As discussed in ClearGrasp, bright directional lighting and caustics cause mistaken surface normal and mask predictions, eventually leading to reconstruction failure. (Jiang et al., 2023) `ev:cited` p. 14 ^jiang2023robotic-060
- In cluttered transparent scenes, some image pixels could belong to more than one object because of transparency. (Jiang et al., 2023) `ev:asserted` p. 15 ^jiang2023robotic-061
- ClearPose contains over 350k labelled real-world RGB-D frames and 5M instance annotations covering 63 household objects. (Jiang et al., 2023) `ev:cited` p. 15 ^jiang2023robotic-062
- PhoCaL's manipulator-driven annotation reaches pose accuracy one order of magnitude more precise than previous vision-sensor-only pipelines. (Jiang et al., 2023) `ev:cited` p. 15 ^jiang2023robotic-063
- ClearPose and Syn-TODD both include only RGB-D images, which may limit the types of models trained and tested on them. (Jiang et al., 2023) `ev:asserted` p. 16 ^jiang2023robotic-064
- Silhouette-based and boundary-based matching pose methods have declined in popularity due to their reliance on prior information like object models or symmetry. (Jiang et al., 2023) `ev:asserted` p. 16 ^jiang2023robotic-065
- Keypoint-based transparent object pose estimation methods are susceptible to occlusions, according to the authors' comparison of pose methods. (Jiang et al., 2023) `ev:asserted` p. 17 ^jiang2023robotic-066
- The authors suggest transparent objects without distinct features can negatively influence [[Normalized Object Coordinate Space|NOCS prediction]], resulting in poor pose estimation accuracy. (Jiang et al., 2023) `ev:asserted` p. 17 ^jiang2023robotic-067
- Current transparent object manipulation research has not yet considered misalignment between the visual centroid and the centre of mass. (Jiang et al., 2023) `ev:asserted` p. 18 ^jiang2023robotic-068

## 🎯 Contributions

## 📖 Glossary

- **Lambertian assumption** — Surfaces reflect light evenly in all directions, giving uniform brightness from all viewing angles.
- **Type I depth error** — Depth sensor returns the background surface depth behind a transparent object.
- **Type II depth error** — Missing depth caused by specular highlights corrupting projected infrared stereo patterns.
- **DoLP** — Degree of Linear Polarisation: polarised light intensity relative to total light intensity.
- **AoLP** — Angle of Linear Polarisation: the orientation of the polarisation axis.
- **Caustics** — Patterns of focused light formed when rays pass through or reflect off refractive surfaces.
- **Fractal Dimension (FD)** — Measure of geometric complexity, used here to compare segmentation dataset difficulty.
- **Mean Connected Components (MCC)** — Average number of connected mask components per image, a dataset complexity metric.
- **NOCS** — Normalised Object Coordinate Space: dense 2D-3D correspondence representation for pose estimation.
- **Sim2Real gap** — Performance loss when models trained on rendered images meet real camera images.

## ❓ Open questions

- Can simulators be extended to render polarisation and thermal modalities for transparent objects?
- Do semi-automatic labelling tools work for transparent objects whose appearance comes from the background?
- How robust are transparent object segmentation models trained on small datasets in unstructured or unseen environments?
- Can domain adaptation further improve transparent object depth reconstruction beyond domain randomisation?
- How can transparent objects be reconstructed in highly cluttered scenes where pixels belong to several objects?
- Can additional modalities or robust estimators make NOCS-based pose estimation work for transparent objects?
- How should deformable, articulated or grasped transparent objects be perceived and tracked?
- Could mm-wave radar or other new sensors serve transparent object perception?

## 📝 Notes on reading

Version read: arXiv 2304.00157v2 (17 Oct 2023), typeset for IEEE Transactions on Artificial Intelligence; matches the packet identifier.

Inconsistencies inside the paper: the TOD dataset is described as 48k images in the text (p. 15) but listed as 28k (R) in Table VIII; StereOBJ-1M is 396,509 frames in the text but 393k in Table VIII; TODD is 14,659 images in the text versus 15k in Table VI; TransTouch is cited as [37] in the text but [17] in Table III; p. 12 lists DREDS, a synthetic dataset, among the real-world datasets that reach scale through automatic collection.

Table I (sensor comparison: range, night vision, price), Table II (rendering engines: speed, quality, caustics, robotic physics), Table V (segmentation methods), Table VII (reconstruction method pros and cons), Table IX (pose method pros and cons) and Table X (overview of challenges) were extracted as one cell per line; only headline statements were claimed. Figures 6, 7 and 11 were described, not claimed beyond the captions' statements.

## Suggested new concepts

- Transparent object depth completion — central task with several datasets (ClearGrasp, TransCG, DREDS) and method families worth a hub note.
- Lambertian assumption violation — explains why RGB-D sensors fail on glass and liquids, relevant to lab automation with flasks.
- Rendering engines for synthetic transparent data — Blender Cycles/LuxCoreRender vs Omniverse trade-offs matter for synthetic dataset generation.
- Multi-modal transparent sensing (polarisation, thermal, tactile) — recurring alternative to RGB-D with its own cost and range trade-offs.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — Revisión del estado del arte en transparencia
