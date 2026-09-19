---
aliases: []
type: "source"
title: "Characterizing the Uncertainty of Jointly Distributed Poses in the Lie Algebra"
citekey: "Mangelson2019characterizing"
doi: "10.48550/arXiv.1906.07795"
arxiv: "1906.07795"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1906.07795"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Joshua G. Mangelson", "Maani Ghaffari", "Ram Vasudevan", "Ryan M. Eustice"]
sha256: ["259ba12a85909328a236dc39ef3606604d9101046110c81a71f203b51a11177d"]
pdf: "Content/Papers/Mangelson2019characterizing.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 60
---

📄 PDF: [[Mangelson2019characterizing.pdf]]

> [!abstract] One-sentence summary
> The paper extends Lie algebra pose-uncertainty propagation to jointly correlated poses and derives composition, inverse and relative pose operations, showing on simulation and Manhattan3500 that accounting for correlation cuts covariance error sharply.

## Abstract

An accurate characterization of pose uncertainty is essential for safe autonomous navigation. Early pose uncertainty characterization methods proposed by Smith, Self, and Cheeseman (SCC), used coordinate-based first-order methods to propagate uncertainty through non-linear functions such as pose composition (head-to-tail), pose inversion, and relative pose extraction (tail-to-tail). Characterizing uncertainty in the Lie Algebra of the special Euclidean group results in better uncertainty estimates. However, existing approaches assume that individual poses are independent. Since factors in a pose graph induce correlation, this independence assumption is usually not reflected in reality. In addition, prior work has focused primarily on the pose composition operation. This paper develops a framework for modeling the uncertainty of jointly distributed poses and describes how to perform the equivalent of the SSC pose operations while characterizing uncertainty in the Lie Algebra. Evaluation on simulated and open-source datasets shows that the proposed methods result in more accurate uncertainty estimates. An accompanying C++ library implementation is also released. This is a pre-print of a paper submitted to IEEE TRO in 2019. (arXiv)

## 🧠 Key ideas (atomic)

- The authors argue that accurate characterization of pose uncertainty is essential to robust long-term autonomy because planning and safety decisions are often predicated on it. (Mangelson et al., 2019) `ev:asserted` p. 1 ^mangelson2019characterizing-001
- The authors note that an over-confident position estimate could potentially result in a self-driving car crossing out of its lane. (Mangelson et al., 2019) `ev:asserted` p. 1 ^mangelson2019characterizing-002
- Smith, Self, and Cheeseman represented multiple uncertain spatial relationships as a stochastic map for evaluating the uncertainty of any pose relative to another. (Mangelson et al., 2019) `ev:cited` p. 1 ^mangelson2019characterizing-003
- Wang and Chirikjian and Long et al. overcame local-coordinate inconsistencies by representing each pose with exponential coordinates in the Lie algebra of SE(d). (Mangelson et al., 2019) `ev:cited` p. 2 ^mangelson2019characterizing-004
- Barfoot and Furgale showed that modeling uncertainty directly in the Lie algebra, then applying the exponential map, could simplify propagation computations. (Mangelson et al., 2019) `ev:cited` p. 2 ^mangelson2019characterizing-005
- Barfoot and Furgale derived first and second order uncertainty propagation for pose composition when the associated poses are independent. (Mangelson et al., 2019) `ev:cited` p. 2 ^mangelson2019characterizing-006
- The proposed approach drops the independence requirement because poses estimated by SLAM are rarely independent of one another. (Mangelson et al., 2019) `ev:asserted` p. 2 ^mangelson2019characterizing-007
- The paper presents a framework for representing jointly correlated poses with uncertainty characterized in the Lie algebra. (Mangelson et al., 2019) `ev:asserted` p. 2 ^mangelson2019characterizing-008
- The paper derives Lie-algebra equivalents of the SSC pose composition, pose inversion, and relative pose extraction operations under the proposed framework. (Mangelson et al., 2019) `ev:asserted` p. 2 ^mangelson2019characterizing-009
- The paper also describes how to convert alternative uncertainty parameterizations, including covariance extracted from an MLE solution, into the proposed framework. (Mangelson et al., 2019) `ev:asserted` p. 2 ^mangelson2019characterizing-010
- Defining a zero-mean Gaussian perturbation in the Lie algebra induces a distribution over SE(3) parameterized by a group mean and algebra covariance. (Mangelson et al., 2019) `ev:cited` p. 3 ^mangelson2019characterizing-011
- The authors state that the SSC coordinate-based parameterization is unable to accurately model pose uncertainty because the parameter vector is not truly Gaussian. (Mangelson et al., 2019) `ev:asserted` p. 4 ^mangelson2019characterizing-012
- The SSC operations propagate mean and covariance up to first order using Jacobians of the nonlinear composition, inverse, and relative pose functions. (Mangelson et al., 2019) `ev:cited` p. 5 ^mangelson2019characterizing-013
- Existing Lie algebra propagation methods assume that individual measurements are independent, which may not hold for poses derived from SLAM. (Mangelson et al., 2019) `ev:cited` p. 6 ^mangelson2019characterizing-014
- Correlated poses are modeled by concatenating their Lie algebra perturbation vectors into one vector described by a single joint covariance matrix. (Mangelson et al., 2019) `ev:asserted` p. 6 ^mangelson2019characterizing-015
- When the composed poses are correlated, as with Pose Graph SLAM solutions or wheel slip, the cross terms must be included. (Mangelson et al., 2019) `ev:asserted` p. 6 ^mangelson2019characterizing-016
- The authors note that Isserlis' theorem can be applied to evaluate the fourth order terms if increased accuracy is needed. (Mangelson et al., 2019) `ev:asserted` p. 6 ^mangelson2019characterizing-017
- The first order composed covariance equals the Barfoot and Furgale result plus two additional cross terms that model cross correlation. (Mangelson et al., 2019) `ev:computed` p. 7 ^mangelson2019characterizing-018
- Without accounting for correlation, the composed pose distribution under-approximates the true distribution in the trajectory simulation of Fig. 4. (Mangelson et al., 2019) `ev:measured` p. 7 ^mangelson2019characterizing-019
- Both the SSC operations and the proposed Lie algebra methods are first order approximation methods in terms of covariance. (Mangelson et al., 2019) `ev:asserted` p. 7 ^mangelson2019characterizing-020
- The authors attribute the Lie algebra accuracy advantage to Euler angles being a chart that does not cover the entire manifold. (Mangelson et al., 2019) `ev:asserted` p. 7 ^mangelson2019characterizing-021
- The composition experiment composed sequences of N noisy pose transformations whose consecutive perturbations were correlated with correlation coefficient ρ. (Mangelson et al., 2019) `ev:reported` p. 7 ^mangelson2019characterizing-022
- The Monte Carlo evaluation generated 10000 sample trajectories to assess SSC head-to-tail and Lie algebra composition with and without correlation. (Mangelson et al., 2019) `ev:reported` p. 7 ^mangelson2019characterizing-023
- In this experiment, the Lie algebra based method significantly outperformed SSC head-to-tail, which the authors attribute to accounting for SE(3) group structure. (Mangelson et al., 2019) `ev:measured` p. 7 ^mangelson2019characterizing-024
- Dropping the cross covariance terms under-approximates the true covariance when positive correlation is present in the composed perturbations. (Mangelson et al., 2019) `ev:measured` p. 7 ^mangelson2019characterizing-025
- The authors state that, as far as they know, Lie algebra derivations of the inverse and relative pose operations had not been previously published. (Mangelson et al., 2019) `ev:asserted` p. 7 ^mangelson2019characterizing-026
- The inverse pose distribution has mean equal to the inverted mean and covariance transformed by the adjoint of that inverted mean. (Mangelson et al., 2019) `ev:computed` p. 7 ^mangelson2019characterizing-027
- The relative pose covariance combines both marginal covariances and both cross covariances, all transformed by the adjoint of the inverted first mean. (Mangelson et al., 2019) `ev:computed` p. 8 ^mangelson2019characterizing-028
- Ignoring correlation leads to under- or over-estimation of uncertainty, depending on correlation sign and whether composition or relative pose is performed. (Mangelson et al., 2019) `ev:asserted` p. 8 ^mangelson2019characterizing-029
- The relative pose simulation generated M = 10000 sets of two correlated uncertain poses with covariances scaled by a parameter α. (Mangelson et al., 2019) `ev:reported` p. 8 ^mangelson2019characterizing-030
- Covariance error was measured against Monte Carlo as the square root of the trace of the squared covariance difference. (Mangelson et al., 2019) `ev:reported` p. 9 ^mangelson2019characterizing-031
- The unscented transform is presented as a better choice than first order linearization for converting coordinate-based uncertainty to the Lie algebra representation. (Mangelson et al., 2019) `ev:asserted` p. 9 ^mangelson2019characterizing-032
- In Fig. 7, the Lie algebra representation converted from SSC via the unscented transform over-approximates the true underlying distribution. (Mangelson et al., 2019) `ev:measured` p. 9 ^mangelson2019characterizing-033
- Using the coordinate-based representation, even as an intermediate step, leads to some loss of information during conversion. (Mangelson et al., 2019) `ev:asserted` p. 10 ^mangelson2019characterizing-034
- Joint Lie algebra covariance can be extracted from an MLE solution by evaluating the measurement Jacobian with respect to the perturbations rather than parameters. (Mangelson et al., 2019) `ev:asserted` p. 10 ^mangelson2019characterizing-035
- The Jacobian is evaluated numerically by perturbing the Lie algebra variables around zero and propagating them through the exponential map. (Mangelson et al., 2019) `ev:reported` p. 10 ^mangelson2019characterizing-036
- The authors claim direct extraction increases accuracy because the perturbation vector lies in a vector space, whereas the parameter vector does not. (Mangelson et al., 2019) `ev:asserted` p. 10 ^mangelson2019characterizing-037
- In the odometry sweep, accuracy of all methods drops as the number of composed poses increases. (Mangelson et al., 2019) `ev:measured` p. 10 ^mangelson2019characterizing-038
- The authors attribute the accuracy drop to first-order methods losing higher order information that builds up as more poses are compounded. (Mangelson et al., 2019) `ev:asserted` p. 10 ^mangelson2019characterizing-039
- Across trajectory lengths, the proposed method was consistently the most accurate at keeping final samples within the 99.9% covariance ellipsoid. (Mangelson et al., 2019) `ev:measured` p. 10 ^mangelson2019characterizing-040
- The number-of-poses sweep held both noise scale parameters fixed at σt = σr = 3. (Mangelson et al., 2019) `ev:reported` p. 10 ^mangelson2019characterizing-041
- Rotation noise had a much more significant effect on accuracy than translation noise in the noise parameter sweep. (Mangelson et al., 2019) `ev:measured` p. 11 ^mangelson2019characterizing-042
- Both Lie group methods consistently outperformed SSC except when rotation noise was very low and translation noise very high. (Mangelson et al., 2019) `ev:measured` p. 11 ^mangelson2019characterizing-043
- The joint Lie algebra composition was consistently more accurate than composition ignoring correlation, with induced correlation fixed at ρ = 0.4. (Mangelson et al., 2019) `ev:measured` p. 11 ^mangelson2019characterizing-044
- Pose pairs extracted from the Manhattan3500 solution had offsets ranging from 5 to 500 nodes. (Mangelson et al., 2019) `ev:reported` p. 11 ^mangelson2019characterizing-045
- On 44425 Manhattan3500 pose pairs, the proposed relative pose method had mean covariance error 0.00675104 when correlation was taken into account. (Mangelson et al., 2019) `ev:measured` p. 11 ^mangelson2019characterizing-046
- Ignoring correlation raised the mean covariance error of the proposed relative pose method to 2.05667 on the Manhattan3500 pose pairs. (Mangelson et al., 2019) `ev:measured` p. 11 ^mangelson2019characterizing-047
- Table II reports a mean normalized covariance error of 0.0493121 for the proposed relative pose method on Manhattan3500. (Mangelson et al., 2019) `ev:measured` p. 11 ^mangelson2019characterizing-048
- SSC tail-to-tail had a mean normalized covariance error of 0.28778 on the same 44425 Manhattan3500 pose pairs. (Mangelson et al., 2019) `ev:measured` p. 11 ^mangelson2019characterizing-049
- The relative pose evaluation used iSAM to solve the Manhattan 3500 dataset before extracting joint means and covariances for pose pairs. (Mangelson et al., 2019) `ev:reported` p. 12 ^mangelson2019characterizing-050
- Ignoring correlation can lead to a covariance error more than 3 orders of magnitude higher than when correlation is taken into account. (Mangelson et al., 2019) `ev:measured` p. 12 ^mangelson2019characterizing-051
- For the SSC comparison, covariance matrices were normalized by the Frobenius norm of the Monte Carlo covariance before computing error. (Mangelson et al., 2019) `ev:reported` p. 12 ^mangelson2019characterizing-052
- The authors note that the SSC comparison is imperfect because its Monte Carlo covariance is a Gaussian fit to non-Gaussian parameter vectors. (Mangelson et al., 2019) `ev:asserted` p. 12 ^mangelson2019characterizing-053
- Even in the SSC error format, the proposed Lie algebra method yields an order of magnitude lower covariance error than SSC. (Mangelson et al., 2019) `ev:measured` p. 13 ^mangelson2019characterizing-054
- The authors released an open source C++ library implementation of the method, available for download on Bitbucket. (Mangelson et al., 2019) `ev:reported` p. 13 ^mangelson2019characterizing-055
- The library applies composition, inverse, and relative pose operations to known or uncertain poses, with the compiler selecting the formulation. (Mangelson et al., 2019) `ev:reported` p. 14 ^mangelson2019characterizing-056
- Each library operation returns a new SE(3) reference object that is assumed independent from then on in later operations. (Mangelson et al., 2019) `ev:reported` p. 14 ^mangelson2019characterizing-057
- Besides SE(3), the library also implements classes for the SO(3), SE(2), and SO(2) Lie groups. (Mangelson et al., 2019) `ev:reported` p. 14 ^mangelson2019characterizing-058
- The authors suggest the methods can increase the accuracy of data association consistency checks when extracting pose uncertainty from pose graph SLAM. (Mangelson et al., 2019) `ev:asserted` p. 15 ^mangelson2019characterizing-059
- The authors state the method can compose odometry measurements that are potentially correlated, such as in the presence of wheel slip. (Mangelson et al., 2019) `ev:asserted` p. 15 ^mangelson2019characterizing-060

## 🎯 Contributions


## 📖 Glossary

- **SE(3)** — Special Euclidean group of 3D rigid-body rotations and translations as homogeneous matrices.
- **Lie algebra** — Tangent space of a Lie group at the identity; a vector space.
- **Exponential map** — Maps a Lie algebra element to its corresponding group element.
- **Adjoint action** — Linear map moving a Lie algebra perturbation across a group element.
- **BCH formula** — Series giving the log of a product of exponentials within the algebra.
- **SSC operations** — Smith–Self–Cheeseman head-to-tail, inverse and tail-to-tail pose operations with first-order propagation.
- **Stochastic map** — Joint Gaussian over many uncertain spatial relationships stacked in one state.
- **Unscented transform** — Sigma-point method approximating a Gaussian pushed through a nonlinear function.
- **Cross covariance** — Off-diagonal covariance block coupling the uncertainty of two different poses.

## ❓ Open questions

- How much accuracy is gained by evaluating the fourth order correlated terms (e.g. via Isserlis' theorem) rather than stopping at first order?
- How do the methods behave for long compositions or high rotation noise, where lost higher order terms accumulate?
- Can the library avoid treating each operation's output as independent, so chained operations keep their correlations?
- How does direct MLE covariance extraction in the Lie algebra compare quantitatively with unscented-transform conversion from SSC?
- Do the gains on Manhattan3500 (a 2D pose graph) carry over to 3D SLAM datasets?

## 📝 Notes on reading

- Version read: arXiv v1 preprint (1906.07795, 18 Jun 2019), matching the packet identifier; submitted to IEEE TRO.
- The registry abstract spells the method's initials both "SCC" and "SSC"; the body uses SSC.
- Equation (51) for the relative pose covariance is garbled in extraction (stray minus signs at line ends); the sign of the cross terms was not claimed.
- Tables I and II print means with a ± term (e.g. 0.00675104 ± 2.2e−4); only the means were claimed. Std. dev. columns: 0.0461455 vs 2.12371 (Table I), 0.0353072 vs 0.411625 (Table II).
- Figures 4–14 (uncertainty ellipses, 99.9% ellipsoid inclusion curves, per-offset correlation and error maps) could only be described; Fig. 9 caption states rotation noise has the largest negative effect.
- Section IX-B text says the relative pose was estimated "with and without taking uncertainty into account" (p. 9), which appears to mean correlation.
- Fig. 10 legend: 3450 pose pairs at offset 50; Figs. 11–14 cover offsets 10, 100, 200 and 500.

## Suggested new concepts

- Lie algebra uncertainty propagation — recurring technique for representing pose covariance on SE(3) via tangent-space perturbations.
- Pose correlation in SLAM — cross covariance between SLAM pose estimates matters for consistent relative pose uncertainty.
- SSC stochastic map — classic coordinate-based baseline for uncertain spatial relationships, referenced across SLAM literature.
- Covariance recovery from MLE solutions — extracting marginal and joint covariances from pose graph optimizers like iSAM.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H2.** Propaga covarianzas de poses correlacionadas en se(3), justo lo que necesita la cadena cámara-muñeca-objeto-pinza con errores de calibración compartidos.
