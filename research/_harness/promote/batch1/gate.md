# Promote gate — 2026-09-18

## Packet `p1-information-geometry` → topic **Information geometry and natural-gradient optimization**

> The geometry of parametric probability models and the optimizers built on it: the Fisher information metric and its variants (Fisher-Rao, Wasserstein), divergences such as the Bregman family and the dually flat structure they induce, steepest descent under a metric (natural gradient, mirror descent, Wasserstein natural gradient), practical approximations of the Fisher (K-FAC, damping, Fisher-vector products), KL-constrained policy updates seen as natural-gradient steps (natural policy gradient, TRPO), and spectral views of wide networks through the Fisher and the Neural Tangent Kernel. It deliberately leaves out the reinforcement-learning machinery that is not geometric (PPO clipping, advantage estimation, Atari and MuJoCo benchmarking), Lie groups and pose representations, equivariant vision networks, Riemannian motion policies for robot control, and robot-learning datasets and policies, which belong to other areas.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Natural gradient descent | method | at-bar | 12 | 8 | An optimization method that preconditions the loss gradient by the inverse of a Riemannian metric on parameter space, usually the Fisher information, so that each step follows steepest descent in the space of model distributions rather than in raw parameter coordinates. |
| Natural policy gradient | method | at-bar | 5 | 2 | A policy-gradient method for reinforcement learning that preconditions the policy gradient by the inverse Fisher information of the policy, taking natural-gradient steps with a chosen step size. |
| Wasserstein natural gradient | method | at-bar | 10 | 2 | A natural gradient in which the parameter-space metric is the pull-back of the Wasserstein-2 metric instead of the Fisher-Rao metric, so the update accounts for a ground metric on sample space and stays defined for models without a density. |
| Trust region policy optimization | method | at-bar | 12 | 3 | A policy-optimization algorithm that maximizes a surrogate advantage objective subject to a bound on the average KL divergence between old and new policies, solved with conjugate gradient on Fisher-vector products and a line search. |
| Bregman divergence | concept | at-bar | 12 | 2 | The divergence induced by a strictly convex, differentiable function as the gap between the function and its first-order Taylor approximation, which corresponds one-to-one with exponential families and induces a dually flat Hessian geometry. |
| Neural Tangent Kernel | concept | at-bar | 12 | 2 | The kernel formed by inner products of a network's output gradients with respect to its parameters, which governs gradient-descent training dynamics in function space and becomes deterministic and constant during training in the infinite-width limit. |
| Fisher information matrix | concept | extra | 12 | 8 | The expected outer product of log-likelihood gradients under a model's own distribution, which serves as the invariant Riemannian metric on a parametric family and as the curvature matrix that natural-gradient methods invert. |
| Mirror descent | method | extra | 10 | 2 | A first-order optimization method that replaces the squared Euclidean proximity term of a gradient step with another proximity function, typically a Bregman divergence, and is equivalent to natural gradient descent on the dual manifold. |
| Kronecker-factored approximate curvature | method | extra | 10 | 3 | An approximate natural-gradient optimizer for neural networks that models each layer's Fisher block as the Kronecker product of activation and back-propagated-derivative second-moment matrices, so the curvature can be inverted cheaply. |

**Relations**

- Natural policy gradient —specialises→ Trust region policy optimization (^schulman2015trust-034)

**Near pairs (reader decides, RC2)**

- Natural gradient descent ~ Natural policy gradient: The same Fisher-preconditioned step applied to policy parameters; a reader may want it as a specialisation note rather than a separate concept.
- Natural gradient descent ~ Wasserstein natural gradient: Same steepest-descent construction with the Wasserstein metric in place of the Fisher-Rao metric; distinct metric, shared form.
- Natural gradient descent ~ Riemannian optimization: Natural gradient descent is recovered from Riemannian gradient descent with a first-order retraction of the exponential map (nielsen2018elementary-048, raskutti2013information-053).
- Natural gradient descent ~ Mirror descent: Mirror descent with a Bregman divergence is equivalent to natural gradient descent on the dual manifold (raskutti2013information-020).
- Natural policy gradient ~ Trust region policy optimization: TRPO computes the same Fisher-preconditioned direction but enforces a KL constraint per update instead of a fixed step size (schulman2015trust-035).
- Natural policy gradient ~ Natural gradient descent: Natural policy gradient is natural gradient descent applied to a policy's parameters.
- Wasserstein natural gradient ~ Kernelized Wasserstein natural gradient (KWNG): KWNG is an RKHS/Nyström estimator of the Wasserstein natural gradient (arbel2019kernelized-015), not the same object; could be its own method note.
- Wasserstein natural gradient ~ Natural gradient descent: Same steepest-descent form under a different metric; li2018natural-021 frames it as replacing the KL constraint of the Fisher-Rao natural gradient.
- Trust region policy optimization ~ Natural policy gradient: Natural policy gradient is the special case of the TRPO update with a fixed step size instead of a KL constraint.
- Trust region policy optimization ~ Proximal policy optimization: PPO is a first-order method designed to emulate TRPO's trust region (schulman2017proximal-004); a different algorithm, not in this packet's names.
- Bregman divergence ~ Kullback-Leibler divergence: For exponential families the Bregman divergence of the log-normalizer coincides with a KL divergence (raskutti2013information-014, nielsen2018elementary-045); related, not identical.
- Neural Tangent Kernel ~ Fisher information matrix: The empirical FIM and the NTK share the same non-zero eigenvalues (karakida2019pathological-041); dual views of one Jacobian Gram structure, not the same object.
- Fisher information matrix ~ Empirical Fisher: Martens2014new uses 'empirical Fisher' for the training-target approximation, which is not the Fisher in general (martens2014new-025, -026); Karakida2019pathological uses 'empirical FIM' for the sample-averaged true FIM. Keep both out of this note's aliases.
- Fisher information matrix ~ Generalized Gauss-Newton matrix: Equals the Fisher when the output distribution is an exponential family in natural parameters (martens2014new-006), but is defined differently.
- Fisher information matrix ~ Neural Tangent Kernel: Shares the non-zero eigenvalues of the empirical FIM (karakida2019pathological-041).
- Mirror descent ~ Natural gradient descent: Proven equivalent to natural gradient descent on the dual Riemannian manifold (raskutti2013information-020); different algorithm and coordinates, same trajectory.
- Kronecker-factored approximate curvature ~ Natural gradient descent: K-FAC is an efficient approximation of natural gradient descent (martens2015optimizing-004, wu2017scalable-007); a relation of type 'approximates' has no slot in the allowed relation types.


## Packet `p2-riemannian-robot-motion` → topic **Riemannian and Lie-group methods for robot motion and optimization**

> Methods that treat robot configurations, poses, policies and learnable parameters as points on Riemannian manifolds or Lie groups, and that design, learn or optimize over them intrinsically: geometric reactive controllers (Riemannian motion policies, geometric fabrics, geodesic synergies), optimization on manifolds and its software (Geoopt, Pymanopt, Riemannian adaptive optimizers, Riemannian preconditioners), manifold-aware generative policies such as Riemannian flow matching, and the machinery of exponential and logarithm maps, retractions and transport that these methods share, together with differentiable solver layers that embed such geometric optimization inside trained networks. It deliberately excludes Euclidean-only policy learning (e.g. diffusion or action-chunking policies without manifold structure), information-geometric natural-gradient methods, equivariant network architectures, and pose-estimation benchmarks, which belong to neighbouring areas even when they touch rotations.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Riemannian Motion Policies | method | at-bar | 11 | 3 | A Riemannian motion policy pairs a desired-acceleration policy for a subtask with a state-dependent positive semi-definite metric that weights its directional importance, so that many subtask policies can be combined into one reactive robot controller. |
| Riemannian optimization | method | at-bar | 12 | 4 | Riemannian optimization minimizes a cost function over a search space that is a differentiable manifold, taking steps along the manifold (via exponential maps or retractions) instead of optimizing freely in Euclidean space and projecting back. |
| Riemannian flow matching | method | at-bar | 10 | 2 | Riemannian flow matching trains a continuous normalizing flow on a Riemannian manifold by regressing a vector field onto conditional vector fields defined through a premetric such as geodesic distance, which is simulation-free on manifolds with closed-form geodesics. |
| Differentiable optimization layers | method | at-bar | 7 | 3 | A differentiable optimization layer embeds a classical solver step, such as a Gauss-Newton or least-squares update, inside a neural network's computation graph so that gradients can be backpropagated through the solution to train the network end to end. |
| Exponential map | concept | extra | 11 | 5 | The exponential map sends a tangent vector at a point of a manifold or Lie group to the point reached by following the geodesic with that initial velocity, with the logarithm map as its local inverse, and it is how updates and perturbations computed in the tangent space are applied back on the manifold. |
| Geometric fabrics | framework | extra | 10 | 1 | Geometric fabrics are bent Finsler geometries used as reactive motion policies, in which velocity-dependent metrics and zero-work bending terms let behaviour be designed in independent parts while remaining provably stable and path consistent. |
| Geodesic synergies | concept | extra | 12 | 1 | A geodesic synergy is a minimum-energy joint coordination given by a geodesic of the robot's configuration-space manifold under the kinetic-energy metric, and combining a few such synergies generates a wide range of physically meaningful motions. |

**Relations**

- Geometric fabrics —specialises→ Riemannian Motion Policies (^wyk2021geometric-005)


## Packet `p3-equivariance-rotations` → topic **Equivariant networks and rotation representations**

> How learning systems handle 3D rotations and rigid motions: network architectures that are equivariant or invariant to rotation, translation or scale groups by construction (steerable convolutions, vector neurons, tensor field networks, equivariant policies), how rotations are represented as network outputs or inputs (continuity, double cover, SVD and Gram-Schmidt mappings), probability distributions over rotations for uncertain pose, and the pose ambiguity that object symmetries cause for estimators and evaluation metrics. It deliberately excludes the general Lie-group mathematics of SO(3) and SE(3) (exponential maps, tangent spaces, Riemannian optimization), which belong to the Lie-group area, and it excludes 6D pose pipelines, benchmarks and datasets as such (render-and-compare refinement, BOP, YCB-Video) except where symmetry-induced ambiguity is the point.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Steerable CNN | method | at-bar | 13 | 6 | A convolutional network whose feature maps are fields of geometric quantities and whose kernels are linear combinations of pre-computed steerable basis kernels, so every layer is equivariant to rotations (and translations) of the input. |
| Vector Neurons | method | at-bar | 13 | 4 | A building block for SO(3)-equivariant point-cloud networks in which each neuron is a 3D vector instead of a scalar, with linear layers, non-linearities, pooling and normalization redesigned so that rotating the input rotates every latent feature. |
| Rotation representation continuity | concept | at-bar | 12 | 6 | Whether the map from a rotation to the vector a network predicts is continuous, a property no representation of 3D rotations in four or fewer dimensions (Euler angles, axis-angle, quaternions) can have, and whose absence hampers learning when rotations are the network output. |
| Pose ambiguity from symmetry | phenomenon | at-bar | 12 | 7 | The situation in which several object or camera poses are indistinguishable in the observation because of symmetric shape, symmetric scenes or occlusion, so a single-answer pose estimator or error metric is ill-posed. |
| Equivariant neural network | framework | extra | 12 | 6 | A neural network constrained by its architecture so that transforming the input by a group element, such as a rotation or translation, transforms the output in the corresponding way, giving guaranteed rather than learned symmetry. |
| Tensor Field Network | method | extra | 11 | 4 | An SE(3)-equivariant convolutional network for point clouds whose filters are spherical harmonics times learned radial functions, combined with features through tensor products. |
| Bingham distribution | concept | extra | 8 | 2 | An antipodally symmetric probability distribution on unit quaternions used to express uncertainty over 3D rotations, whose mixtures can represent several plausible orientations at once. |

**Relations**

- Steerable CNN —specialises→ Equivariant neural network (^fuchs2020se-005)
- Vector Neurons —specialises→ Equivariant neural network (^simeonov2021neural-019)
- Tensor Field Network —specialises→ Equivariant neural network (^fuchs2020se-005)
- Bingham distribution —solves→ Pose ambiguity from symmetry (^deng2020deep-015)

**Near pairs (reader decides, RC2)**

- Steerable CNN ~ Tensor Field Network: e3nn implements the two as the uvw versus uvu connection modes of one tensor-product operation; a reader may treat TFNs as the point-cloud member of the steerable family.
- Steerable CNN ~ Group equivariant CNN: Regular G-CNNs are contrasted with steerable ones (discrete versus continuous rotations) but both are called G-CNNs in the taxonomy of Cohen et al.
- Rotation representation continuity ~ Quaternion double cover: Geist et al. treat double cover as one source of discontinuity; a reader may want it as a separate concept or folded in here.
- Equivariant neural network ~ Group equivariant CNN: Cohen and Welling's G-CNN may be drafted in another packet as the general concept; the two could be one note.
- Equivariant neural network ~ Group equivariance: The property itself versus networks that have it; a reader may prefer one note.
- Tensor Field Network ~ Steerable CNN: Same steerable-kernel construction on point clouds instead of voxel grids; differs from 3D Steerable CNNs only in the tensor-product connection mode according to e3nn.
- Bingham distribution ~ Matrix Fisher distribution: An alternative distribution over SO(3) with an unconstrained parameter matrix; same role, different family.
- Bingham distribution ~ Deep Bingham Networks: The network framework built on this distribution, possibly wanted as its own note.


## Packet `p4-object-pose` → topic **6D object pose estimation**

> Estimating the 3D rotation and translation of rigid objects relative to a camera from RGB or RGB-D images, for known (instance-level) and novel (unseen, CAD- or reference-image-based) objects: the estimator families (render-and-compare refinement, dense RGB-D fusion, point matching, direct regression), the benchmarks, datasets and error metrics used to compare them (BOP, YCB-Video, ADD/ADD-S, VSD), the synthetic training data they rely on, and the perception of transparent objects whose broken sensor depth must be completed before depth-based pose estimation or grasping. It deliberately excludes the mathematics of rotation parametrisation and equivariant networks (covered by the Lie-group and equivariance areas), camera ego-motion and SLAM, and grasp planning itself beyond its use as a downstream evaluation of pose or depth quality.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Render-and-compare pose refinement | method | at-bar | 12 | 5 | Iteratively correcting a 6D object pose estimate by rendering the object model at the current pose and letting a network compare the rendering with the observed image to predict a pose update. |
| BOP benchmark | instrument | at-bar | 10 | 5 | The standard benchmark for model-based 6D object pose estimation, combining real-image datasets in a unified format, symmetry-aware pose-error functions (VSD, MSSD, MSPD) and an online leaderboard run as a series of public challenges. |
| YCB-Video dataset | instrument | at-bar | 13 | 7 | An RGB-D video dataset of 21 household YCB objects in 92 videos with 6D pose annotations, released with PoseCNN and widely used to evaluate object pose estimators. |
| Transparent object depth completion | process | at-bar | 12 | 4 | Recovering accurate depth for transparent objects, whose refraction and specular reflection leave RGB-D sensor depth missing or wrong, typically by predicting a corrected depth map from the RGB image and the raw depth. |
| Novel-object 6D pose estimation | concept | extra | 9 | 4 | Estimating the 6D pose of objects never seen during training, given only a CAD model or a few reference images at test time, without per-object retraining. |
| ADD and ADD-S metrics | metric | extra | 11 | 7 | Pose-error metrics that average the distance between object model points transformed by the estimated and ground-truth poses, using corresponding points (ADD) or closest points to tolerate symmetric objects (ADD-S). |
| Synthetic training data for 6D pose estimation | method | extra | 12 | 6 | Training object pose estimators on large sets of images rendered from 3D object models, often physically based and physically simulated, in place of or in addition to scarce annotated real images. |

**Relations**

- BOP benchmark —solves→ Pose ambiguity from symmetry (^hodan2018bop-008)

**Near pairs (reader decides, RC2)**

- Render-and-compare pose refinement ~ Learned iterative pose refinement: DenseFusion's pose residual estimator also refines poses iteratively with a network, but on a re-transformed point cloud rather than on renderings; the reader decides whether it is the same family or a sibling.
- Transparent object depth completion ~ Transparent object depth reconstruction: Jiang et al. use 'depth reconstruction' for a broader family that also includes multi-view and NeRF-based shape recovery, not only single-view completion of a sensor depth map.
- Novel-object 6D pose estimation ~ Unseen-object pose estimation: Suggested under this name in Hodan2024bop; very likely the same task, listed here instead of as an alias because it is a suggestion bullet rather than a claim spelling.
- ADD and ADD-S metrics ~ Pose ambiguity from symmetry: ADD-S exists to absorb symmetry ambiguity; the two notes overlap on the symmetric variant but one is a metric and the other a phenomenon.
- Synthetic training data for 6D pose estimation ~ Physically-based rendered training data: Suggested in Hodan2024bop for the BlenderProc PBR images specifically; a narrower subset of synthetic training data.

- SOFT C7 BOP benchmark: relation target 'Pose ambiguity from symmetry' is not drafted (kept only if drafted elsewhere)

## Packet `p5-robot-policies` → topic **Visuomotor and vision-language-action robot policies**

> Learned policies that map camera images (and often language instructions and proprioception) directly to low-level robot actions, trained mainly by imitation of demonstrations: how the action output is represented (action chunks, discrete action tokens, diffusion or flow-matching generative heads), the model classes built on them (Diffusion Policy, ACT-style chunked policies, vision-language-action models built on pre-trained VLMs), the pooled multi-robot corpora and cross-embodiment pre-training that feed them, and the recurring problem of multimodal demonstration data. It includes online RL fine-tuning of such generative policies where it acts on the same policy classes. It deliberately excludes the geometry of the action space itself (Lie groups, Riemannian flow matching, equivariant layers), optimisation theory such as natural gradients, hand-crafted Riemannian motion policies, and object-pose perception pipelines, which belong to their own areas even when a policy paper uses them.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Action chunking | method | at-bar | 13 | 9 | Action chunking has a policy predict a sequence of several future actions from one observation and execute them (fully or partly) before re-planning, which shortens the effective decision horizon and makes motion more temporally consistent. |
| Diffusion Policy | method | at-bar | 13 | 6 | Diffusion Policy represents a visuomotor policy as a conditional denoising diffusion process over robot action sequences, conditioned on observations, so that it can represent multimodal action distributions learned from demonstrations. |
| Action tokenization | method | at-bar | 13 | 6 | Action tokenization turns continuous robot actions into discrete tokens that a sequence model can predict with next-token prediction, from naive per-dimension binning to compressed or learned tokenizers. |
| Open X-Embodiment dataset | data-modality | at-bar | 12 | 6 | The Open X-Embodiment dataset is a pooled open collection of more than 70 robot manipulation datasets from many robot embodiments, used as the shared pre-training corpus of generalist policies such as RT-X, Octo, OpenVLA and π0. |
| Vision-language-action models | framework | at-bar | 12 | 7 | Vision-language-action models are pre-trained vision-language models further trained to output robot actions from images and language instructions, so that web-scale visual and semantic knowledge transfers to robot control. |
| Flow matching policy | method | extra | 10 | 4 | A flow matching policy generates actions by integrating a learned, observation-conditioned velocity field that carries Gaussian noise to actions, a simulation-free alternative to diffusion sampling that usually needs few integration steps. |
| Cross-embodiment pre-training | process | extra | 9 | 4 | Cross-embodiment pre-training trains one policy on pooled data from many different robots before adapting it to a target robot, so that data from other embodiments improves generalization where target-robot data are scarce. |
| Multimodal action distributions | phenomenon | extra | 9 | 6 | Multimodal action distributions arise when demonstrations contain several distinct valid actions for the same observation, which single-output regression policies average into infeasible actions while expressive generative policies can represent and commit to one mode. |

**Relations**

- Diffusion Policy —solves→ Multimodal action distributions (^chi2023diffusion-003)

**Near pairs (reader decides, RC2)**

- Diffusion Policy ~ Flow matching policy: Both are generative action heads that denoise noise into action chunks; several sources treat flow matching as a variant of diffusion (π0, RFMP) while others compare them as separate policy classes.
- Diffusion Policy ~ Diffusion action head: Octo's lightweight diffusion head on transformer embeddings (a suggestion bullet in Team2024octo) may be read as an instance of Diffusion Policy or as a distinct design pattern.
- Open X-Embodiment dataset ~ Cross-embodiment pre-training: OXE is the main corpus used for cross-embodiment pre-training; the reader may prefer to keep the dataset and the training strategy as one note.
- Flow matching policy ~ Riemannian flow matching: RFMP is a flow matching policy built on Riemannian flow matching; the reader decides whether the Euclidean policy class and its manifold extension share a note.
- Flow matching policy ~ Diffusion Policy: π0 calls flow matching a variant of diffusion; the two policy classes are compared directly in Braun2024riemannian and Pertsch2025fast.
- Cross-embodiment pre-training ~ Open X-Embodiment dataset: OXE is the principal corpus used for this training strategy.

