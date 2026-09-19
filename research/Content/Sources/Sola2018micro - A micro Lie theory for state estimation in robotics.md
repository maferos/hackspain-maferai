---
aliases: []
type: "source"
title: "A micro Lie theory for state estimation in robotics"
citekey: "Sola2018micro"
doi: "10.48550/arXiv.1812.01537"
arxiv: "1812.01537"
year: 2018
publication_type: "preprint"
url: "https://arxiv.org/abs/1812.01537"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Joan Solà", "Jeremie Deray", "Dinesh Atchuthan"]
sha256: ["93190a60ad5f390006970f684ba8590bf55ce21adc3c1cb675adc55ead17f869"]
pdf: "Content/Papers/Sola2018micro.pdf"
topics: ["[[Matemáticas]]", "[[Optimización y algoritmos]]", "[[Aplicaciones en visión por computador]]"]
cited_in: ["[[01_matematicas_grupos_de_lie]]", "[[02_optimizacion_y_algoritmos]]", "[[03_aplicaciones_vision_por_computador]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Sola2018micro.pdf]]

> [!abstract] One-sentence summary
> A tutorial that distills a minimal subset of Lie theory (Exp/Log maps, plus/minus operators, adjoints, Jacobians, tangent-space covariances) for robot state estimation, with worked ESKF and graph-SLAM examples, a formula compendium for common groups and the C++ library manif.

## Abstract

A Lie group is an old mathematical abstract object dating back to the XIX century, when mathematician Sophus Lie laid the foundations of the theory of continuous transformation groups. As it often happens, its usage has spread over diverse areas of science and technology many years later. In robotics, we are recently experiencing an important trend in its usage, at least in the fields of estimation, and particularly in motion estimation for navigation. Yet for a vast majority of roboticians, Lie groups are highly abstract constructions and therefore difficult to understand and to use. This may be due to the fact that most of the literature on Lie theory is written by and for mathematicians and physicists, who might be more used than us to the deep abstractions this theory deals with. In estimation for robotics it is often not necessary to exploit the full capacity of the theory, and therefore an effort of selection of materials is required. In this paper, we will walk through the most basic principles of the Lie theory, with the aim of conveying clear and useful ideas, and leave a significant corpus of the Lie theory behind. Even with this mutilation, the material included here has proven to be extremely useful in modern estimation algorithms for robotics, especially in the fields of SLAM, visual odometry, and the like. Alongside this micro Lie theory, we provide a chapter with a few application examples, and a vast reference of formulas for the major Lie groups used in robotics, including most jacobian matrices and the way to easily manipulate them. We also present a new C++ template-only library implementing all the functionality described here. (arXiv)

## 🧠 Key ideas (atomic)

- The authors state the selected material has proven extremely useful in modern robotics estimation, especially SLAM and visual odometry. (Solà et al., 2018) `ev:asserted` p. 1 ^sola2018micro-001
- The authors describe recent robotics efforts to formulate estimation properly as motivated by demand for precision, consistency and stability. (Solà et al., 2018) `ev:asserted` p. 1 ^sola2018micro-002
- The paper aims to simplify Lie theory beyond prior basic introductions, hence the adjective micro, at merely 17 pages. (Solà et al., 2018) `ev:asserted` p. 1 ^sola2018micro-003
- Howe's Very basic Lie theory, comprising 24 dense pages, is sometimes considered a must-read introduction according to the authors. (Solà et al., 2018) `ev:cited` p. 1 ^sola2018micro-004
- The paper puts special attention on computing Jacobians, a topic the authors note is not treated in Stillwell's book. (Solà et al., 2018) `ev:asserted` p. 2 ^sola2018micro-005
- The paper presents a selected subset of Lie theory aimed at roboticists skilled in state estimation but unfamiliar with the theory. (Solà et al., 2018) `ev:asserted` p. 2 ^sola2018micro-006
- The authors effectively relegate the Lie algebra to a second plane in favor of its isomorphic vector space Rn. (Solà et al., 2018) `ev:asserted` p. 2 ^sola2018micro-007
- The paper does not introduce the Lie bracket, a material the authors consider often not necessary for their target application areas. (Solà et al., 2018) `ev:asserted` p. 2 ^sola2018micro-008
- The paper is accompanied by manif, a new open-source C++ header-only library available on GitHub. (Solà et al., 2018) `ev:reported` p. 2 ^sola2018micro-009
- manif implements the groups SO(2), SO(3), SE(2) and SE(3), with support for creating analytic Jacobians. (Solà et al., 2018) `ev:reported` p. 2 ^sola2018micro-010
- A Lie group is defined as a smooth manifold whose elements satisfy the group axioms of closure, identity, inverse and associativity. (Solà et al., 2018) `ev:asserted` p. 2 ^sola2018micro-011
- The Lie algebra is defined as the tangent space at the identity of the Lie group's manifold. (Solà et al., 2018) `ev:asserted` p. 4 ^sola2018micro-012
- Elements of the Lie algebra can be identified with vectors in Rm, where m is the number of degrees of freedom. (Solà et al., 2018) `ev:cited` p. 4 ^sola2018micro-013
- The exponential map exactly converts Lie algebra elements into group elements, with the log map as its inverse operation. (Solà et al., 2018) `ev:cited` p. 4 ^sola2018micro-014
- Hat and vee are two mutually inverse linear isomorphisms passing between the Lie algebra and the Cartesian vector space Rm. (Solà et al., 2018) `ev:asserted` p. 4 ^sola2018micro-015
- The authors prefer Rm over the Lie algebra because Cartesian vectors can be stacked in larger state vectors. (Solà et al., 2018) `ev:asserted` p. 4 ^sola2018micro-016
- Time-differentiating the SO(3) orthogonality constraint reveals that R transpose times R-dot is a skew-symmetric matrix. (Solà et al., 2018) `ev:computed` p. 5 ^sola2018micro-017
- The closed-form exponential map of SO(3) derived from its power series is the well-known Rodrigues rotation formula. (Solà et al., 2018) `ev:computed` p. 5 ^sola2018micro-018
- The quaternion hat and vee maps include a factor 2 accounting for the double effect of the quaternion rotation action. (Solà et al., 2018) `ev:asserted` p. 6 ^sola2018micro-019
- The plus and minus operators combine one Exp or Log operation with one composition to express increments in tangent space. (Solà et al., 2018) `ev:asserted` p. 6 ^sola2018micro-020
- Because composition is non-commutative, the plus and minus operators are defined in right and left versions. (Solà et al., 2018) `ev:asserted` p. 6 ^sola2018micro-021
- By default, the authors express perturbations locally, using the right-hand forms of the plus and minus operators. (Solà et al., 2018) `ev:asserted` p. 6 ^sola2018micro-022
- The adjoint matrix linearly maps tangent vectors at a group element X onto tangent vectors at the origin. (Solà et al., 2018) `ev:asserted` p. 7 ^sola2018micro-023
- The adjoint matrix of SE(3) is derived in closed form as a block matrix built from the rotation and translation. (Solà et al., 2018) `ev:computed` p. 7 ^sola2018micro-024
- Right Jacobians on Lie groups are defined by replacing vector plus and minus with the right plus and minus operators. (Solà et al., 2018) `ev:asserted` p. 8 ^sola2018micro-025
- The right Jacobian linearly maps the local tangent space at X to the local tangent space at f(X). (Solà et al., 2018) `ev:asserted` p. 8 ^sola2018micro-026
- The Jacobian of the 3D rotation action f(R) = Rp with respect to R is derived as minus R times the skew matrix of p. (Solà et al., 2018) `ev:computed` p. 8 ^sola2018micro-027
- Left and right Jacobians of a function are related through the adjoints of the domain and codomain manifolds. (Solà et al., 2018) `ev:computed` p. 8 ^sola2018micro-028
- Covariance matrices are defined on the tangent space at the mean point, allowing Gaussian variables to be defined on manifolds. (Solà et al., 2018) `ev:asserted` p. 9 ^sola2018micro-029
- A naive covariance defined by vector subtraction is always ill-defined when the element size exceeds the manifold dimension. (Solà et al., 2018) `ev:asserted` p. 9 ^sola2018micro-030
- Global and local covariances are related by transforming with the adjoint matrix on both sides. (Solà et al., 2018) `ev:computed` p. 9 ^sola2018micro-031
- Covariance propagation through a function on manifolds uses linearization with Jacobian matrices, yielding the familiar vector-space formula. (Solà et al., 2018) `ev:computed` p. 9 ^sola2018micro-032
- Non-constant velocities are typically handled by segmenting them into piecewise constant bits and composing their exponentials sequentially. (Solà et al., 2018) `ev:asserted` p. 9 ^sola2018micro-033
- For typical manifolds, closed forms exist for elementary Jacobians of inversion, composition, exponentiation and group action. (Solà et al., 2018) `ev:asserted` p. 9 ^sola2018micro-034
- Once the elementary Jacobian blocks are found, all other Jacobians follow by the chain rule. (Solà et al., 2018) `ev:asserted` p. 9 ^sola2018micro-035
- The Jacobian of the group inverse is derived to be the negative of the adjoint matrix. (Solà et al., 2018) `ev:computed` p. 10 ^sola2018micro-036
- The composition Jacobian with respect to the first operand equals the inverse adjoint of the second operand. (Solà et al., 2018) `ev:computed` p. 10 ^sola2018micro-037
- The left and right Jacobians of a manifold are related through the adjoint matrix evaluated at the exponential of tau. (Solà et al., 2018) `ev:computed` p. 10 ^sola2018micro-038
- Group action Jacobians cannot be generalized, since group actions depend on the set being acted upon. (Solà et al., 2018) `ev:asserted` p. 10 ^sola2018micro-039
- Composite manifolds concatenate non-interacting manifolds, at the price of losing some consistency with the Lie theory. (Solà et al., 2018) `ev:asserted` p. 11 ^sola2018micro-040
- With composite manifolds, Jacobians of functions can be determined per block, requiring only knowledge of the manifold blocks. (Solà et al., 2018) `ev:asserted` p. 11 ^sola2018micro-041
- Unlike T(n)×SO(n), which chains translation and rotation, SE(n) performs translation and rotation simultaneously as a continuum. (Solà et al., 2018) `ev:asserted` p. 11 ^sola2018micro-042
- The applicative examples consider a planar robot with pose in SE(2) measuring beacon positions in its own reference frame. (Solà et al., 2018) `ev:reported` p. 12 ^sola2018micro-043
- The control noise model accounts for possible lateral wheel slippage through a nonzero lateral velocity standard deviation. (Solà et al., 2018) `ev:reported` p. 12 ^sola2018micro-044
- In the error-state Kalman filter on manifold, the estimation error and its covariance are expressed in the tangent space. (Solà et al., 2018) `ev:reported` p. 12 ^sola2018micro-045
- The only changes of the manifold ESKF relative to a regular EKF are substituting plus operators in prediction and state update. (Solà et al., 2018) `ev:asserted` p. 12 ^sola2018micro-046
- The smoothing and mapping example uses a factor graph with 3 poses, 3 beacons, 2 motion factors and 5 beacon factors. (Solà et al., 2018) `ev:reported` p. 12 ^sola2018micro-047
- The SAM problem is solved by iterative least squares using the pseudoinverse of the total Jacobian until convergence. (Solà et al., 2018) `ev:reported` p. 13 ^sola2018micro-048
- For large problems, the authors state that QR or Cholesky factorizations are required instead of the pseudoinverse. (Solà et al., 2018) `ev:cited` p. 13 ^sola2018micro-049
- Self-calibration augments the composite state with an unknown motion-sensor bias, adding one extra Jacobian column on the left. (Solà et al., 2018) `ev:reported` p. 13 ^sola2018micro-050
- Extending the examples to 3D requires only defining variables in SE(3) and R3, with the algorithm math unchanged. (Solà et al., 2018) `ev:asserted` p. 13 ^sola2018micro-051
- The robot localization and mapping applications of Section V are demonstrated as examples within the accompanying manif library. (Solà et al., 2018) `ev:reported` p. 14 ^sola2018micro-052
- The authors state they do not introduce any new theoretical material in this exposition of Lie theory. (Solà et al., 2018) `ev:asserted` p. 14 ^sola2018micro-053
- The authors believe their form of exposing Lie theory will help many researchers enter the field. (Solà et al., 2018) `ev:asserted` p. 14 ^sola2018micro-054
- For the planar rotation groups S1 and SO(2), the adjoint and right and left Jacobians are trivial scalars equal to 1. (Solà et al., 2018) `ev:computed` p. 14 ^sola2018micro-055
- The quaternion manifold S3 is a double cover of SO(3), with q and minus q representing the same rotation. (Solà et al., 2018) `ev:asserted` p. 15 ^sola2018micro-056
- Double-cover problems in the quaternion Log can be avoided by ensuring the scalar part is positive beforehand. (Solà et al., 2018) `ev:asserted` p. 15 ^sola2018micro-057
- The adjoint matrix of the 3D rotation group is derived to equal the rotation matrix R itself. (Solà et al., 2018) `ev:computed` p. 15 ^sola2018micro-058
- For SO(3), the closed-form left Jacobian is observed to equal the transpose of the closed-form right Jacobian. (Solà et al., 2018) `ev:computed` p. 15 ^sola2018micro-059
- Closed forms of the SE(3) left Jacobian and its inverse are taken from prior work by Barfoot. (Solà et al., 2018) `ev:cited` p. 17 ^sola2018micro-060
- In the translation groups, the adjoint and the right and left Jacobians all equal the identity matrix. (Solà et al., 2018) `ev:computed` p. 17 ^sola2018micro-061

## 🎯 Contributions

## 📖 Glossary

- **Lie group** — A smooth manifold whose elements satisfy the group axioms.
- **Lie algebra** — The tangent space of a Lie group at its identity element.
- **Exp / Log** — Maps between tangent vectors in Rm and group elements, and back.
- **Hat / vee** — Linear isomorphisms between the Lie algebra and the Cartesian space Rm.
- **Right plus / minus** — Operators adding or extracting increments expressed in the local tangent space.
- **Adjoint matrix** — Linear map transforming local tangent vectors into tangent vectors at the identity.
- **Right Jacobian** — Derivative mapping local tangent perturbations of the input to the output's tangent space.
- **Composite manifold** — Concatenation of non-interacting manifolds treated block-wise as one state.
- **ESKF** — Error-state Kalman filter; here the error lives in the tangent space.
- **Double cover** — Two unit quaternions, q and -q, representing the same rotation.

## ❓ Open questions

- How much is lost in practice by omitting the Lie bracket and deeper Lie algebra structure for estimation problems?
- What consistency costs arise from treating heterogeneous states as composite manifolds instead of a proper Lie group such as SE(n)?
- When should SE(n), T(n)×SO(n) or the composite parametrization be preferred for motion integration versus perturbation modeling?
- The applicative examples are not evaluated on data; how do manifold ESKF and SAM compare numerically with vector-space baselines?

## 📝 Notes on reading

The cached text is arXiv version v9 (8 Dec 2021) of arXiv:1812.01537; the metadata year is 2018. The PDF abstract differs slightly from the registry abstract (the registry version contains an extra sentence about literature written for mathematicians and physicists). The paper is a tutorial: it contains derivations and worked examples but no experimental evaluation, so no claim is tagged measured. Table I (typical Lie groups: size, dimension, constraint, Exp, composition, action) is partly garbled in extraction and was not claimed cell by cell. Figures 1-11 are conceptual illustrations (manifold and tangent space, S1 and S3 wrapping, adjoint paths, right Jacobian construction, tangent-space covariance ellipses, motion integration); Figure 12 shows the SAM factor graph. Many matrix formulas (SE(2) and SE(3) Jacobians, the Q(ρ, θ) block) are garbled in extraction and were only summarized.

## Suggested new concepts

- Lie group state estimation — central framework for on-manifold filtering and optimization in robotics.
- Right and left Jacobians on Lie groups — reusable derivative blocks for uncertainty propagation.
- Error-state Kalman filter on manifold — standard filter design for pose estimation.
- manif library — open-source implementation of SO(n)/SE(n) operations and Jacobians.
- Composite manifold — practical device for heterogeneous state vectors in factor graphs.

## Por qué es relevante

- **[[01_matematicas_grupos_de_lie]]** — Referencia práctica de $\oplus/\ominus$, Jacobianos y adjuntas para SO(3), SE(3), etc. Base de la librería `manif`.
- **[[02_optimizacion_y_algoritmos]]** — Convención $\oplus/\ominus$ y jacobianos en el tangente usados en A.3–A.4 y C.1.
- **[[03_aplicaciones_vision_por_computador]]** — Referencia práctica de $\mathrm{Exp}/\mathrm{Log}$, Jacobianos y perturbaciones usada en §1 y §3 (desarrollada en la parte 1)
