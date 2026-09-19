---
aliases: []
type: "source"
title: "ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM"
citekey: "Campos2020orb"
doi: "10.48550/arXiv.2007.11898"
arxiv: "2007.11898"
year: 2020
publication_type: "preprint"
url: "https://arxiv.org/abs/2007.11898"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Carlos Campos", "Richard Elvira", "Juan J. Gómez Rodríguez", "José M. M. Montiel", "Juan D. Tardós"]
sha256: ["4d119517be7565c9651fbf1e36a330d605b7a534d738558858c96feca7b99156"]
pdf: "Content/Papers/Campos2020orb.pdf"
topics: ["[[Aplicaciones en visión por computador]]"]
cited_in: ["[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Campos2020orb.pdf]]

> [!abstract] One-sentence summary
> ORB-SLAM3 is an open-source feature-based SLAM library that combines MAP-based visual-inertial initialization, higher-recall place recognition and a multi-map Atlas to reuse short-, mid-, long-term and multi-session data associations, reaching the best reported accuracy on EuRoC and TUM-VI.

## Abstract

This paper presents ORB-SLAM3, the first system able to perform visual, visual-inertial and multi-map SLAM with monocular, stereo and RGB-D cameras, using pin-hole and fisheye lens models. The first main novelty is a feature-based tightly-integrated visual-inertial SLAM system that fully relies on Maximum-a-Posteriori (MAP) estimation, even during the IMU initialization phase. The result is a system that operates robustly in real-time, in small and large, indoor and outdoor environments, and is 2 to 5 times more accurate than previous approaches. The second main novelty is a multiple map system that relies on a new place recognition method with improved recall. Thanks to it, ORB-SLAM3 is able to survive to long periods of poor visual information: when it gets lost, it starts a new map that will be seamlessly merged with previous maps when revisiting mapped areas. Compared with visual odometry systems that only use information from the last few seconds, ORB-SLAM3 is the first system able to reuse in all the algorithm stages all previous information. This allows to include in bundle adjustment co-visible keyframes, that provide high parallax observations boosting accuracy, even if they are widely separated in time or if they come from a previous mapping session. Our experiments show that, in all sensor configurations, ORB-SLAM3 is as robust as the best systems available in the literature, and significantly more accurate. Notably, our stereo-inertial SLAM achieves an average accuracy of 3.6 cm on the EuRoC drone and 9 mm under quick hand-held motions in the room of TUM-VI dataset, a setting representative of AR/VR scenarios. For the benefit of the community we make public the source code. (arXiv)

## 🧠 Key ideas (atomic)

- ORB-SLAM3 is a multi-map, multi-session system working in visual or visual-inertial modes with monocular, stereo or RGB-D sensors. (Campos et al., 2020) `ev:reported` p. 5 ^campos2020orb-001
- The system supports both pin-hole and fisheye camera models, building on the earlier ORB-SLAM2 and ORB-SLAM-VI systems. (Campos et al., 2020) `ev:reported` p. 5 ^campos2020orb-002
- Most visual odometry systems use only short-term data association, forgetting elements out of view and drifting even when revisiting the same area. (Campos et al., 2020) `ev:asserted` p. 2 ^campos2020orb-003
- The authors describe mid-term data association as the key to their better accuracy compared with visual odometry systems with loop detection. (Campos et al., 2020) `ev:asserted` p. 2 ^campos2020orb-004
- Long-term data association lets a SLAM system reset drift and correct the map using pose-graph optimization or, more accurately, bundle adjustment. (Campos et al., 2020) `ev:asserted` p. 2 ^campos2020orb-005
- DBoW2 requires three consecutive keyframes matched to the same area before checking geometric consistency, boosting precision at the expense of recall. (Campos et al., 2020) `ev:cited` p. 3 ^campos2020orb-006
- The new place recognition checks candidate keyframes for geometric consistency first, then for local consistency with three covisible keyframes. (Campos et al., 2020) `ev:reported` p. 3 ^campos2020orb-007
- The authors state this place recognition strategy increases recall and densifies data association at a slightly higher computational cost. (Campos et al., 2020) `ev:asserted` p. 3 ^campos2020orb-008
- ORB-SLAM Atlas represents a set of disconnected maps and applies place recognition, relocalization, loop closure and map merging to all of them. (Campos et al., 2020) `ev:reported` p. 3 ^campos2020orb-009
- An abstract camera representation makes the SLAM code agnostic of the camera model, adding new models through their projection, unprojection and Jacobian functions. (Campos et al., 2020) `ev:reported` p. 3 ^campos2020orb-010
- The Atlas keeps one active map for tracking and builds a single DBoW2 keyframe database for relocalization, loop closing and map merging. (Campos et al., 2020) `ev:reported` p. 5 ^campos2020orb-011
- When tracking is lost, the system tries to relocalize in all Atlas maps; otherwise a new active map is later initialized from scratch. (Campos et al., 2020) `ev:reported` p. 5 ^campos2020orb-012
- After a loop correction, a full bundle adjustment runs in an independent thread to refine the map without affecting real-time performance. (Campos et al., 2020) `ev:reported` p. 6 ^campos2020orb-013
- Besides the pin-hole model, the ORB-SLAM3 library provides the Kannala-Brandt fisheye model through a separate camera module. (Campos et al., 2020) `ev:reported` p. 6 ^campos2020orb-014
- Relocalization uses the MLPnP algorithm, which is decoupled from the camera model because it takes projective rays as input. (Campos et al., 2020) `ev:reported` p. 6 ^campos2020orb-015
- The system avoids stereo image rectification, treating the stereo rig as two monocular cameras with a constant relative SE(3) transformation. (Campos et al., 2020) `ev:reported` p. 6 ^campos2020orb-016
- For IMU initialization, pure monocular SLAM runs for 2 seconds with keyframes inserted at 4Hz, giving an up-to-scale map of 10 poses. (Campos et al., 2020) `ev:reported` p. 7 ^campos2020orb-017
- An inertial-only MAP estimation then optimizes scale, gravity direction, IMU biases and velocities while holding the up-to-scale visual trajectory constant. (Campos et al., 2020) `ev:reported` p. 7 ^campos2020orb-018
- Initialization experiments on EuRoC show the method achieves 5% scale error with trajectories of 2 seconds. (Campos et al., 2020) `ev:measured` p. 8 ^campos2020orb-019
- Visual-inertial bundle adjustment is performed 5 and 15 seconds after initialization, converging to 1% scale error. (Campos et al., 2020) `ev:measured` p. 8 ^campos2020orb-020
- VI-DSO starts with a huge scale error and requires 20-30 seconds to converge to 1% error. (Campos et al., 2020) `ev:cited` p. 8 ^campos2020orb-021
- A scale refinement optimizing only scale and gravity direction runs every ten seconds until the map exceeds 100 keyframes or 75 seconds. (Campos et al., 2020) `ev:reported` p. 8 ^campos2020orb-022
- The stereo-inertial initialization fixes the scale factor to one, removing it from the inertial-only optimization variables. (Campos et al., 2020) `ev:reported` p. 8 ^campos2020orb-023
- The visual-inertial system enters a visually lost state when fewer than 15 map points are tracked. (Campos et al., 2020) `ev:reported` p. 8 ^campos2020orb-024
- In short-term lost state the body state is estimated from IMU readings; after 5 seconds a new visual-inertial map is started. (Campos et al., 2020) `ev:reported` p. 8 ^campos2020orb-025
- If the system gets lost within 15 seconds after IMU initialization, the map is discarded to avoid inaccurate maps. (Campos et al., 2020) `ev:reported` p. 9 ^campos2020orb-026
- Using only the first candidate, raw DBoW2 queries achieve precision and recall in the order of 50-80%. (Campos et al., 2020) `ev:cited` p. 9 ^campos2020orb-027
- DBoW2 temporal and geometric consistency checks move the working point to 100% precision with 30-40% recall. (Campos et al., 2020) `ev:cited` p. 9 ^campos2020orb-028
- The authors found that the DBoW2 delay and low recall too often produced duplicated areas in the same or different maps. (Campos et al., 2020) `ev:asserted` p. 9 ^campos2020orb-029
- Place recognition queries the Atlas DBoW2 database for the three most similar keyframes, excluding keyframes covisible with the active keyframe. (Campos et al., 2020) `ev:reported` p. 9 ^campos2020orb-030
- The aligning transformation is estimated with RANSAC using Horn's algorithm on minimal sets of three 3D-3D matches. (Campos et al., 2020) `ev:reported` p. 9 ^campos2020orb-031
- Map merging first welds maps inside a covisibility window, then propagates the correction to the rest through pose-graph optimization. (Campos et al., 2020) `ev:reported` p. 10 ^campos2020orb-032
- In visual-inertial welding bundle adjustment, the two matched keyframes and their five last temporal keyframes are optimizable. (Campos et al., 2020) `ev:reported` p. 10 ^campos2020orb-033
- In the visual-inertial case, global bundle adjustment after loop closing runs only if the keyframe count is below a threshold. (Campos et al., 2020) `ev:reported` p. 11 ^campos2020orb-034
- All experiments ran on an Intel Core i7-7700 CPU at 3.6GHz with 32 GB memory, using only CPU. (Campos et al., 2020) `ev:reported` p. 11 ^campos2020orb-035
- Accuracy is measured with RMS ATE, aligning with Sim(3) in the monocular case and SE(3) in other sensor configurations. (Campos et al., 2020) `ev:reported` p. 11 ^campos2020orb-036
- On EuRoC, ORB-SLAM3 achieves more accurate results than the best literature systems in all four sensor configurations. (Campos et al., 2020) `ev:measured` p. 11 ^campos2020orb-037
- In monocular-inertial configuration on EuRoC, ORB-SLAM3 is five to ten times more accurate than MSCKF, OKVIS and ROVIO. (Campos et al., 2020) `ev:measured` p. 11 ^campos2020orb-038
- In monocular-inertial configuration, ORB-SLAM3 more than doubles the accuracy of VI-DSO and VINS-Mono on EuRoC. (Campos et al., 2020) `ev:measured` p. 11 ^campos2020orb-039
- In stereo-inertial configuration on EuRoC, ORB-SLAM3 is three to four times more accurate than Kimera and VINS-Fusion. (Campos et al., 2020) `ev:measured` p. 11 ^campos2020orb-040
- BASALT approaches ORB-SLAM3 stereo-inertial accuracy but could not complete sequence V203, where some frames from one camera are missing. (Campos et al., 2020) `ev:measured` p. 11 ^campos2020orb-041
- The authors hypothesize greater scene depth in Machine Hall sequences may cause less accurate stereo triangulation and less precise scale. (Campos et al., 2020) `ev:asserted` p. 11 ^campos2020orb-042
- Sequences V103 monocular and V203 stereo, unsolved by ORB-SLAM2, are solved by ORB-SLAM3 in most executions. (Campos et al., 2020) `ev:measured` p. 11 ^campos2020orb-043
- The authors conclude inertial integration reduces median ATE compared to pure visual solutions on EuRoC. (Campos et al., 2020) `ev:measured` p. 11 ^campos2020orb-044
- ORB-SLAM3 stereo-inertial reaches an average RMS ATE of 0.035 m on EuRoC with 0.6% average scale error. (Campos et al., 2020) `ev:measured` p. 12 ^campos2020orb-045
- ORB-SLAM3 monocular-inertial averages 0.043 m ATE on EuRoC, against 0.089 for VI-DSO and 0.110 for VINS-Mono. (Campos et al., 2020) `ev:measured` p. 12 ^campos2020orb-046
- TUM-VI consists of 28 sequences in 6 environments, recorded with a hand-held fisheye stereo-inertial rig. (Campos et al., 2020) `ev:reported` p. 11 ^campos2020orb-047
- In TUM-VI, ground truth is available only at the beginning and end, so evaluation measures accumulated drift. (Campos et al., 2020) `ev:reported` p. 11 ^campos2020orb-048
- On TUM-VI, ORB-SLAM3 extracts 1500 ORB points per image in monocular-inertial and 1000 points in stereo-inertial setups. (Campos et al., 2020) `ev:reported` p. 12 ^campos2020orb-049
- For outdoor TUM-VI sequences, points further than 20 meters from the current camera pose are discarded to limit drift. (Campos et al., 2020) `ev:reported` p. 12 ^campos2020orb-050
- On the TUM-VI benchmark, ORB-SLAM3 obtains errors below 10 cm for most of the room and corridor sequences. (Campos et al., 2020) `ev:measured` p. 12 ^campos2020orb-051
- In magistrale sequences up to 900 m long, ORB-SLAM3 errors are around 1 m except one close to 5 m. (Campos et al., 2020) `ev:measured` p. 12 ^campos2020orb-052
- In some long outdoor sequences, scarce close features may cause inertial drift, leading to errors of 10 to 70 meters. (Campos et al., 2020) `ev:measured` p. 12 ^campos2020orb-053
- VINS-Mono and BASALT, which track features with Lucas-Kanade, obtain better accuracy than ORB-SLAM3 in some slides sequences. (Campos et al., 2020) `ev:measured` p. 12 ^campos2020orb-054
- On TUM-VI room sequences, ORB-SLAM3 stereo-inertial reaches an average RMS ATE of 0.009 m across six sequences. (Campos et al., 2020) `ev:measured` p. 13 ^campos2020orb-055
- The authors state that the better accuracy of monocular over stereo in room sequences is only apparent, due to 7 DoF alignment. (Campos et al., 2020) `ev:asserted` p. 13 ^campos2020orb-056
- In multi-session experiments on the EuRoC dataset, ORB-SLAM3 more than doubles the accuracy of both CCM-SLAM and VINS-Mono. (Campos et al., 2020) `ev:measured` p. 13 ^campos2020orb-057
- Multi-session monocular and stereo SLAM can robustly process the difficult sequences V103 and V203 by exploiting the previous map. (Campos et al., 2020) `ev:measured` p. 13 ^campos2020orb-058
- Single-session stereo-inertial processing of outdoors1 still shows a drift of about 60 m, reduced when processed after magistrale2. (Campos et al., 2020) `ev:measured` p. 14 ^campos2020orb-059
- The timing experiments show that ORB-SLAM3 runs in real time at 30-40 frames and 3-6 keyframes per second. (Campos et al., 2020) `ev:measured` p. 14 ^campos2020orb-060
- The novel place recognition method takes only 10 ms per keyframe in the reported timing experiments. (Campos et al., 2020) `ev:measured` p. 14 ^campos2020orb-061
- Map merging and loop closing times remain below one second when running only a pose-graph optimization. (Campos et al., 2020) `ev:measured` p. 14 ^campos2020orb-062
- The authors do not compare running time against other systems, calling that effort beyond the scope of the work. (Campos et al., 2020) `ev:asserted` p. 14 ^campos2020orb-063
- On EuRoC sequence V202, the total time of the stereo-inertial tracking thread is 33.05±9.29 ms per frame. (Campos et al., 2020) `ev:measured` p. 15 ^campos2020orb-064
- The authors suggest using all data association types matters more for accuracy than choosing direct methods over features. (Campos et al., 2020) `ev:asserted` p. 15 ^campos2020orb-065
- In the conclusions, the authors identify low-texture environments as the main failure case of the ORB-SLAM3 system. (Campos et al., 2020) `ev:asserted` p. 15 ^campos2020orb-066
- Feature descriptor matching seems less robust for tracking than Lucas-Kanade, which uses photometric information, according to the authors. (Campos et al., 2020) `ev:asserted` p. 15 ^campos2020orb-067
- The authors conclude stereo-inertial SLAM provides the most robust and accurate solution among the four sensor configurations. (Campos et al., 2020) `ev:asserted` p. 16 ^campos2020orb-068
- In applications with slow motions or without roll and pitch rotations, IMU sensors can be difficult to initialize. (Campos et al., 2020) `ev:asserted` p. 16 ^campos2020orb-069

## 🎯 Contributions

## 📖 Glossary

- **Short-term data association** — Matching map elements obtained during the last few seconds.
- **Mid-term data association** — Matching nearby map elements whose accumulated drift is still small.
- **Long-term data association** — Matching against previously visited areas via place recognition, regardless of accumulated drift.
- **Atlas** — Multi-map representation of disconnected maps with one active map for tracking.
- **RMS ATE** — Root-mean-square absolute trajectory error after aligning estimate with ground truth.
- **Welding window** — Covisible keyframes around matched keyframes where maps are fused and locally optimized.
- **IMU preintegration** — Combining inertial measurements between frames into single relative motion constraints.
- **Mature map** — Map whose scale, IMU parameters and gravity direction are accurately estimated.
- **DBoW2** — Bag-of-binary-words library for fast keyframe place recognition.

## ❓ Open questions

- Can photometric techniques be developed that serve all four data association problems, including long-term and multi-map?
- How can low-texture environments, the main failure case, be handled without losing long-term association?
- Would sky segmentation replace the 20 m point-distance cutoff used for outdoor sequences?
- How does ORB-SLAM3 running time compare with competing systems, which the authors did not measure?
- Can single-image depth networks give reliable true-scale monocular SLAM outside their training environments?

## 📝 Notes on reading

The cached text is arXiv 2007.11898v2 (23 Apr 2021), accepted to IEEE Transactions on Robotics (DOI 10.1109/TRO.2021.3075644). The registry abstract above (arXiv) differs from the PDF abstract of this version: the registry says 2 to 5 times more accurate and 3.6 cm average accuracy on EuRoC, while the PDF abstract says two to ten times and 3.5 cm. Table II gives 0.035 m for stereo-inertial average ATE, consistent with the PDF version. The text on p. 11 writes MCSKF where Table I uses MSCKF; the claim uses MSCKF. Figure 4 (per-execution RMS ATE heat maps on EuRoC), Figure 5 (multi-session TUM-VI trajectories) and Figure 6 (outdoors1 single vs multi-session) could only be described, not read numerically. Table III, VI and VII values were extracted column by column; only headline rows were claimed. Equations 2, 4, 7 and 8 were garbled in extraction and are not claimed.

## Suggested new concepts

- Data association types in SLAM — the short/mid/long-term and multi-map taxonomy frames comparisons across SLAM and VO systems.
- Visual-inertial initialization — MAP-based inertial-only initialization is a distinct, reusable technique with its own accuracy/speed trade-offs.
- Multi-map SLAM and map merging — Atlas-style handling of tracking loss and multi-session reuse recurs across SLAM systems.
- Place recognition recall vs precision — the DBoW2 temporal-consistency trade-off matters for loop closing and map reuse.

## Por qué es relevante

- **[[03_aplicaciones_vision_por_computador]]** — SLAM de referencia basado en características
