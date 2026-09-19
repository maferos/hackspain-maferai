# Promote gate — 2026-09-19

## Packet `q1-lie-kinematics` → topic **Lie-group kinematics and dynamics of robot arms**

> How the motion of articulated robots is modelled with screw and Lie group theory: forward kinematics as products of joint-screw exponentials, the choice of twist representation, recursive O(n) inverse and forward dynamics and their derivatives, Lie-algebraic tools such as the Baker-Campbell-Hausdorff formula used to linearise or differentiate motion on SE(3) and SO(3), and kinematic performance descriptors such as the manipulability ellipsoid. It does not cover learning or optimisation on manifolds in general (Riemannian optimisation, Riemannian motion policies, diffusion or flow models on Lie groups), which belong to the Riemannian and Lie-group methods area, nor rotation representations inside neural networks.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Product of exponentials formula | method | at-bar | 8 | 3 | A way of writing the forward kinematics of an open chain as a product of matrix exponentials of the joint screws, one per joint, times a reference configuration, without needing joint frames or Denavit-Hartenberg parameters. |
| Twist representations | concept | at-bar | 12 | 2 | The four ways of expressing a rigid body's velocity as a six-vector (body-fixed, spatial, hybrid and mixed), which differ in the point where velocity is measured and the frame it is resolved in, and which change the cost of recursive kinematics and dynamics algorithms. |
| Recursive Newton-Euler algorithm | method | at-bar | 12 | 4 | The standard O(n) inverse dynamics method for a kinematic tree, which propagates velocities and accelerations outward from the base in a forward pass and then accumulates wrenches back toward the base to obtain the joint forces. |
| Manipulability ellipsoid | metric | at-bar | 11 | 2 | An ellipsoid, given by a symmetric positive definite matrix such as J J^T, that describes how easily a robot in a given joint configuration can move or exert force along each task direction. |
| Baker-Campbell-Hausdorff formula | method | at-bar | 7 | 3 | A series of nested Lie brackets that expresses the logarithm of a product of two group exponentials as a single Lie algebra element, used to expand, linearise or differentiate motion on matrix Lie groups. |


## Packet `q2-lie-probability` → topic **Probability, filtering and generative models on Lie groups**

> Methods that represent and manipulate uncertainty over states living on Lie groups and other Riemannian manifolds: invariant and error-state filters on matrix Lie groups (the invariant EKF and the group-affine condition behind its guarantees, concentrated Gaussians defined through the exponential map, observability and consistency of such estimators), and generative models that learn and sample distributions on SO(3), SE(3), spheres, tori and general manifolds (Riemannian score-based and diffusion models, SE(3) diffusion for poses, grasps and protein frames). Deliberately out of scope: deterministic motion generation, control and optimization on Lie groups or Riemannian manifolds (covered by Riemannian and Lie-group methods for robot motion and optimization), the design of equivariant network architectures in themselves (Equivariant networks and rotation representations), pose-estimation pipelines and benchmarks (6D object pose estimation), and end-to-end robot policies (Visuomotor and vision-language-action robot policies), except where they are the application that a probabilistic model on a group is evaluated in.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Invariant extended Kalman filter | method | at-bar | 13 | 4 | An extended Kalman filter for states on a matrix Lie group that linearizes an invariant (left or right group) error instead of a vector difference, so that for group-affine systems the error dynamics are exactly log-linear and independent of the estimate. |
| Group-affine dynamics | concept | at-bar | 6 | 3 | The class of dynamics on a Lie group (condition (7) of Barrau and Bonnabel, which includes left- and right-invariant dynamics and reduces to affine dynamics on a vector space) for which the invariant estimation error evolves autonomously and its logarithm obeys an exact linear equation. |
| Diffusion models on Lie groups | method | at-bar | 12 | 5 | Score-based or denoising diffusion generative models whose noising and denoising processes are defined directly on a Lie group such as SO(3) or SE(3), used to sample multimodal distributions of rotations and rigid poses for pose estimation, grasping, manipulation and protein frames. |
| Riemannian diffusion models | method | at-bar | 10 | 3 | The family of diffusion and score-based generative models that extend continuous-time Euclidean diffusion to data on Riemannian manifolds by noising with manifold Brownian or Langevin dynamics and learning the reverse process, trained either by Riemannian score matching or by a Riemannian continuous-time ELBO. |

**Relations**

- Invariant extended Kalman filter —requires→ Group-affine dynamics (^yaqubi2026invariant-004)

**Near pairs (reader decides, RC2)**

- Group-affine dynamics ~ Log-linear error property: Suggested by Barrau2017invariant as a separate concept; it is the consequence of the group-affine condition (the other half of the same theorem), so the reader may prefer one note covering both.
- Diffusion models on Lie groups ~ Riemannian diffusion models: SO(3) and SE(3) are both Lie groups and Riemannian manifolds, so diffusion on a Lie group can be read as a special case of Riemannian diffusion; no claim states the relation explicitly, and ^bortoli2022riemannian-038 (exp-wrapped SGM on so(3)) sits between the two.
- Riemannian diffusion models ~ Riemannian Score-based Generative Models: Drafted here as a member of the family (Bortoli2022riemannian frames it so), but ^huang2022riemannian-032 distinguishes RSGMs (score matching) from RDMs (maximum likelihood); the reader may want a separate note.
- Riemannian diffusion models ~ Diffusion models on Lie groups: Diffusion on SO(3)/SE(3) is arguably a special case of diffusion on Riemannian manifolds.


## Packet `q3-trajectory-control` → topic **Trajectory optimization and model predictive control for arms**

> Methods that compute or track manipulator motions online or per query: sampling-based and gradient-based model predictive control (MPPI and its variants, GPU-parallel rollouts, simulator-as-model MPC), trajectory optimization with smoothness or learned priors (GPMP-style Gaussian process planners, cost-guided sampling), and the low-level feedback laws that execute those trajectories, such as impedance control on SE(3). It covers the cost design, convergence theory and real-time engineering of these controllers. It deliberately leaves out learned end-to-end visuomotor policies, which belong to the robot-policy area, and the general Lie-group and Riemannian machinery, which belongs to the Riemannian and Lie-group methods area even when a controller here uses it.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Model Predictive Path Integral control | method | at-bar | 11 | 4 | A sampling-based model predictive controller that perturbs a nominal control sequence with noise, rolls out the samples, and moves the nominal controls toward the average of the samples weighted by their exponentiated negative cost, applying only the first input before replanning. |
| Gaussian Process Motion Planning | method | top-down | 11 | 3 | A trajectory optimization approach that represents a robot trajectory as a sample from a Gaussian process prior over configuration, velocity and acceleration, and optimizes it against an obstacle cost weighted with the prior cost, which keeps the solution smooth. |
| Geometric impedance control | method | top-down | 9 | 1 | Impedance control for a manipulator's end-effector in which position and velocity errors are defined in the body frame from a left-invariant error function on SE(3), and the restoring wrench is the gradient of the matching potential, so the closed loop has a Lyapunov stability proof. |

**Near pairs (reader decides, RC2)**

- Model Predictive Path Integral control ~ Sampling-based model-predictive control: Suggested by Bhardwaj2021storm as the broader family (MPPI, CEM); MPPI is one member, so it may be a parent concept rather than the same thing.
- Model Predictive Path Integral control ~ Multi-step MPPI (M-MPPI): Fazlyab2026model's variant with several inner preconditioned updates per control step; could be folded in as a variant or kept separate.
- Model Predictive Path Integral control ~ Information theoretic MPC: Williams et al. 2017 derive the same cost-weighted update from a KL objective and note it coincides with path integral control only under control-affine noise; the reader may treat it as the same method or its generalisation.
- Gaussian Process Motion Planning ~ GPMP2: Mukadam et al. present GPMP2 as a successor that recasts GPMP as MAP inference solved by Gauss-Newton with a constant-velocity prior; it could be an alias of the family or a separate method.
- Gaussian Process Motion Planning ~ Stochastic-GPMP (SGPMP): A sampling-based variant used by Carvalho2023motion and Le2023accelerating; may belong under this concept or stand alone.
- Geometric impedance control ~ Impedance control: The general scheme (Hogan 1985) that this concept specialises; a reader may want a parent concept rather than merging.


## Packet `q4-geometric-finetuning` → topic **Information geometry and natural-gradient optimization**

> Optimizers and weight-space procedures that use curvature or norm geometry: Fisher-based preconditioning, Kronecker-factored and spectral-norm updates and the routines that compute them, and Fisher-weighted consolidation or merging of trained weights. Not general training recipes, learning-rate schedules or architectures.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Kronecker-factored preconditioning | method | at-bar | 12 | 5 | Preconditioning a layer's matrix-shaped gradient with the Kronecker product of two small per-dimension matrices, so that a full-matrix preconditioner is approximated with memory and compute that scale with each dimension rather than with their product. |
| Newton-Schulz orthogonalization | method | at-bar | 10 | 2 | An iterative odd-polynomial matrix routine that pushes every singular value of a matrix toward one, approximating its semi-orthogonal factor UV^T without an SVD, and so computes spectral-norm steepest-descent updates such as Muon's. |
| Elastic weight consolidation | method | top-down | 12 | 2 | A continual-learning regularizer that adds a quadratic penalty anchoring each weight to its value after earlier tasks, with a stiffness set by the diagonal Fisher information, so weights important to old tasks change slowly while the rest stay free to learn. |
| Fisher merging | method | top-down | 11 | 1 | Merging models that share an initialization by averaging their parameters with per-parameter weights given by each model's diagonal Fisher information, which maximizes the joint likelihood of their Gaussian approximate posteriors. |

**Relations**

- Elastic weight consolidation —requires→ Fisher information matrix (^kirkpatrick2016overcoming-035)
- Fisher merging —requires→ Fisher information matrix (^matena2021merging-003)

**Near pairs (reader decides, RC2)**

- Kronecker-factored preconditioning ~ Kronecker-factored approximate curvature: K-FAC is the Fisher-based instance of the same Kronecker factorization; the reader decides whether the general idea (Shampoo, SOAP, K-FAC) deserves its own note or folds into K-FAC.


## Packet `q5-calibration-servoing` → topic **Camera-robot calibration and visual servoing**

> How a camera is tied geometrically to a robot and how image measurements then close the control loop: extrinsic hand-eye and robot-world calibration (AX = XB, AX = YB), its marker-based, markerless and certifiably optimal solvers, camera-to-robot pose estimation used as online calibration, and visual servoing controllers (image-based, position-based, direct and learned). It deliberately excludes object 6D pose estimation for its own sake, camera intrinsic calibration, and end-to-end visuomotor policies that do not servo to a goal image or pose; those belong to their own areas.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Markerless hand-eye calibration | method | at-bar | 12 | 4 | Markerless hand-eye calibration estimates the camera-to-robot transform from images of the robot itself, using keypoints, rendered masks, tracked points or exploratory motions instead of fiducial boards or tags. |
| Hand-eye calibration (AX = XB) | process | at-bar | 12 | 5 | Hand-eye calibration estimates the fixed rigid transform between a camera and a robot, or between two rigidly linked egomotion sensors, classically by solving AX = XB from paired relative motions, usually observed through a fiducial target. |
| Visual servoing | method | top-down | 12 | 5 | Visual servoing controls a robot or camera velocity in closed loop from visual feedback so that the current image, or the pose estimated from it, converges to a desired one. |
| Robot-world and hand-eye calibration (AX = YB) | process | extra | 10 | 4 | Robot-world and hand-eye calibration jointly estimates two unknown rigid transforms, the sensor-to-hand transform X and the base-to-world or target transform Y, from paired measurements related by AX = YB, and generalizes the classical AX = XB problem to multiple sensors or targets. |
| Image-based visual servoing | method | extra | 11 | 3 | Image-based visual servoing computes the camera velocity directly from the error between current and desired image features through the pseudoinverse of an interaction matrix, without reconstructing the relative pose. |
| Position-based visual servoing | method | extra | 7 | 4 | Position-based visual servoing first estimates the relative 3D pose between the current and desired camera configurations from images and then drives the robot with a Cartesian control law on that pose error. |

**Near pairs (reader decides, RC2)**

- Markerless hand-eye calibration ~ Hand-eye calibration (AX = XB): Same estimation target (camera-robot extrinsic); markerless methods replace the AX = XB objective and the fiducial target, so the reader may prefer one note with a markerless section.
- Hand-eye calibration (AX = XB) ~ Robot-world and hand-eye calibration (AX = YB): Chen2026optimal-002 states AX = YB can be transformed into AX = XB and is the more general formulation; the reader may fold one into the other.
- Hand-eye calibration (AX = XB) ~ Markerless hand-eye calibration: Solves the same extrinsic problem without markers.
- Robot-world and hand-eye calibration (AX = YB) ~ Hand-eye calibration (AX = XB): AX = XB is the special case with one unknown; Chen2026optimal-002 calls AX = YB the more general formulation.


## Packet `q6-category-pose` → topic **6D object pose estimation**

> Also covers category-level pose and size estimation of unseen instances within known object categories, its canonical-coordinate representations such as NOCS, and training losses that make pose regression tolerant to object symmetry.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Category-level object pose estimation | concept | at-bar | 11 | 7 | Estimating the 6D pose, and usually the 3D size, of previously unseen object instances that belong to categories known at training time, without an exact CAD model of each instance. |
| Normalized Object Coordinate Space | concept | at-bar | 12 | 4 | A canonical unit-cube coordinate frame in which all instances of a category are consistently oriented and scaled, so that a network can predict per-pixel canonical coordinates (a NOCS map) and recover pose and size by aligning them with observed depth. |
| Symmetry-aware pose loss | method | at-bar | 12 | 6 | A pose training loss that does not penalise predictions equivalent under an object's symmetry, either by taking the minimum over the symmetric ground-truth poses or by matching each predicted model point to the closest ground-truth point. |

**Relations**

- Normalized Object Coordinate Space —solves→ Category-level object pose estimation (^wang2019pack-004)

**Near pairs (reader decides, RC2)**

- Category-level object pose estimation ~ Novel-object 6D pose estimation: Both estimate poses of objects unseen in training; category-level needs the category at training time and no CAD model, novel-object needs a CAD model or reference images at test time (^labbe2022megapose-003 contrasts them).
- Symmetry-aware pose loss ~ ShapeMatch-Loss (SLOSS): PoseCNN's closest-point loss is one instance of the general idea; kept inside this concept rather than as its own note.
- Symmetry-aware pose loss ~ ADD and ADD-S metrics: ADD-S applies the same closest-point matching as ShapeMatch-Loss, but as an evaluation metric rather than a training loss.


## Packet `q7-policies-sim` → topic **Visuomotor and vision-language-action robot policies**

> Also covers how such policies and their perception modules are trained in simulation and carried to real robots (sim-to-real transfer, domain randomization) and the simulated grasp datasets they learn from; simulator engineering itself stays out.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Sim-to-real transfer | process | at-bar | 13 | 11 | Deploying a policy or perception model trained in simulation on a physical robot, which works only insofar as the model survives the gap between simulated and real dynamics, sensing and appearance. |
| ACRONYM dataset | instrument | at-bar | 4 | 3 | A large simulated grasp dataset of ShapeNet object meshes, each with many physics-checked parallel-jaw grasps, that is widely used to train and evaluate 6-DoF grasp generators. |
| Domain randomization | method | extra | 10 | 5 | Training on many simulated environments with randomized textures, lighting, camera, geometry or dynamics, so that the real world looks like just another variation and a model trained only in simulation transfers. |

**Near pairs (reader decides, RC2)**

- Sim-to-real transfer ~ Reality gap: Tobin2017domain suggests it separately; claims use 'sim-to-real gap' for the discrepancy that this transfer must bridge. Here it is folded in, but it could stand as its own phenomenon.
- Sim-to-real transfer ~ Domain randomization: A technique for achieving sim-to-real transfer, drafted as a separate extra concept; not the same thing.
- Domain randomization ~ Synthetic training data for 6D pose estimation: Existing concept; randomized synthetic images are one kind of synthetic training data, but domain randomization also covers dynamics and policy training.


## Packet `q8-neural-manifolds` → topic **Neural manifolds in deep networks and motor neuroscience**

> The geometry of neural representations in artificial networks and in recorded brain activity: how the intrinsic dimension of hidden representations changes across layers and training, how population activity forms manifolds whose dimension, radius and separability can be measured, how latent population dynamics are inferred from spiking data, and the pullback metrics that give learned latent spaces a Riemannian geometry. It covers the estimators and theories used for these measurements (TwoNN, manifold capacity, sequential latent-variable models). It deliberately leaves out robot motion generation on Riemannian manifolds and Lie groups, natural-gradient optimisation and information geometry of parameter spaces, and brain-machine interface decoding as an engineering problem, except where they supply a construction such as the pullback metric.

| Concept | Type | Status | Evidence | Sources | Definition |
|---|---|---|---|---|---|
| Intrinsic dimension of neural representations | metric | at-bar | 13 | 4 | The number of degrees of freedom needed to describe the manifold on which a layer's (or a neural population's) activity vectors lie, typically far smaller than the number of units or neurons. |
| Pullback metric | concept | top-down | 11 | 5 | The Riemannian metric induced on a latent or configuration space by a smooth map into another metric space, computed as the Jacobian transpose times the target metric times the Jacobian so that local lengths match those measured in the target space. |
| Neural population dynamics | phenomenon | top-down | 9 | 3 | The time evolution of the joint activity of a population of neurons, viewed as trajectories of a possibly input-driven dynamical system in a low-dimensional neural state space. |
| TwoNN estimator | method | extra | 9 | 2 | An intrinsic-dimension estimator that fits the Pareto distribution followed by the ratio of each point's second to first nearest-neighbour distance, needing only those two distances per point. |
| Neural population geometry | framework | extra | 6 | 1 | An approach that describes biological or artificial neural activity through the shape and arrangement of the manifolds that population responses form in neural state space. |
| Manifold capacity | metric | extra | 6 | 1 | The critical number of linearly separable category manifolds per neuron that a representation supports, determined by the manifolds' dimension, radius and correlation structure. |

**Near pairs (reader decides, RC2)**

- Pullback metric ~ RMP pullback operator: Ratliff2018riemannian and Cheng2018rmpflow also use 'pullback' for the operator that transforms whole motion policies (force and metric) between spaces; the metric is one part of it, so the reader may want the operator kept distinct or folded in.

