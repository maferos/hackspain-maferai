---
aliases: []
type: topic
parent: Computer vision for manipulation
created: 2026-09-18
---

## Scope

Estimating the 3D rotation and translation of rigid objects relative to a camera from RGB or RGB-D images, for known (instance-level) and novel (unseen, CAD- or reference-image-based) objects: the estimator families (render-and-compare refinement, dense RGB-D fusion, point matching, direct regression), the benchmarks, datasets and error metrics used to compare them (BOP, YCB-Video, ADD/ADD-S, VSD), the synthetic training data they rely on, and the perception of transparent objects whose broken sensor depth must be completed before depth-based pose estimation or grasping. It deliberately excludes the mathematics of rotation parametrisation and equivariant networks (covered by the Lie-group and equivariance areas), camera ego-motion and SLAM, and grasp planning itself beyond its use as a downstream evaluation of pose or depth quality.

## Concepts

- [[Render-and-compare pose refinement]] — Iteratively correcting a 6D object pose estimate by rendering the object model at the current pose and letting a network compare the rendering with the observed image to predict a pose update.
- [[BOP benchmark]] — The standard benchmark for model-based 6D object pose estimation, combining real-image datasets in a unified format, symmetry-aware pose-error functions (VSD, MSSD, MSPD) and an online leaderboard run as a series of public challenges.
- [[YCB-Video dataset]] — An RGB-D video dataset of 21 household YCB objects in 92 videos with 6D pose annotations, released with PoseCNN and widely used to evaluate object pose estimators.
- [[Transparent object depth completion]] — Recovering accurate depth for transparent objects, whose refraction and specular reflection leave RGB-D sensor depth missing or wrong, typically by predicting a corrected depth map from the RGB image and the raw depth.
- [[Novel-object 6D pose estimation]] — Estimating the 6D pose of objects never seen during training, given only a CAD model or a few reference images at test time, without per-object retraining.
- [[ADD and ADD-S metrics]] — Pose-error metrics that average the distance between object model points transformed by the estimated and ground-truth poses, using corresponding points (ADD) or closest points to tolerate symmetric objects (ADD-S).
- [[Synthetic training data for 6D pose estimation]] — Training object pose estimators on large sets of images rendered from 3D object models, often physically based and physically simulated, in place of or in addition to scarce annotated real images.
- [[Category-level object pose estimation]] — Estimating the 6D pose, and usually the 3D size, of previously unseen object instances that belong to categories known at training time, without an exact CAD model of each instance.
- [[Normalized Object Coordinate Space]] — A canonical unit-cube coordinate frame in which all instances of a category are consistently oriented and scaled, so that a network can predict per-pixel canonical coordinates (a NOCS map) and recover pose and size by aligning them with observed depth.
- [[Symmetry-aware pose loss]] — A pose training loss that does not penalise predictions equivalent under an object's symmetry, either by taking the minimum over the symmetric ground-truth poses or by matching each predicted model point to the closest ground-truth point.

## Subtopics

## Related topics

## ❓ Open questions

## Problems

- none yet: no problem names this topic as its topic

## History

- 2026-09-18 · Eki Gonzalez Flamarique · parent: root — new area for concepts promoted from the research batch, confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · added 3 concepts — concepts from the gap-research batch (04_huecos_y_ampliacion), confirmed at the gate
- 2026-09-19 · Eki Gonzalez Flamarique · parent: root → Computer vision for manipulation — grouped under the request's three axes
