---
aliases: []
type: "source"
title: "Contact-Aided Invariant Extended Kalman Filtering for Robot State Estimation"
citekey: "Hartley2019contact"
doi: "10.48550/arXiv.1904.09251"
arxiv: "1904.09251"
year: 2019
publication_type: "preprint"
url: "https://arxiv.org/abs/1904.09251"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Ross Hartley", "Maani Ghaffari", "Ryan M. Eustice", "Jessy W. Grizzle"]
sha256: ["b519bbd4b0182da64f3fe0ec2834e7fec89be05931f1a7cffa6dc13f999b3f5c"]
pdf: "Content/Papers/Hartley2019contact.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Hartley2019contact.pdf]]

> [!abstract] One-sentence summary
> The paper derives a contact-aided invariant EKF on a matrix Lie group for legged-robot state estimation from IMU, contact and forward-kinematic data, and shows on a Cassie biped that it converges faster and more reliably than a quaternion-based EKF.

## Abstract

Legged robots require knowledge of pose and velocity in order to maintain stability and execute walking paths. Current solutions either rely on vision data, which is susceptible to environmental and lighting conditions, or fusion of kinematic and contact data with measurements from an inertial measurement unit (IMU). In this work, we develop a contact-aided invariant extended Kalman filter (InEKF) using the theory of Lie groups and invariant observer design. This filter combines contact-inertial dynamics with forward kinematic corrections to estimate pose and velocity along with all current contact points. We show that the error dynamics follows a log-linear autonomous differential equation with several important consequences: (a) the observable state variables can be rendered convergent with a domain of attraction that is independent of the system's trajectory; (b) unlike the standard EKF, neither the linearized error dynamics nor the linearized observation model depend on the current state estimate, which (c) leads to improved convergence properties and (d) a local observability matrix that is consistent with the underlying nonlinear system. Furthermore, we demonstrate how to include IMU biases, add/remove contacts, and formulate both world-centric and robo-centric versions. We compare the convergence of the proposed InEKF with the commonly used quaternion-based EKF though both simulations and experiments on a Cassie-series bipedal robot. Filter accuracy is analyzed using motion capture, while a LiDAR mapping experiment provides a practical use case. Overall, the developed contact-aided InEKF provides better performance in comparison with the quaternion-based EKF as a result of exploiting symmetries present in system. (arXiv)

## 🧠 Key ideas (atomic)

- The authors derive an [[Invariant extended Kalman filter|invariant extended Kalman filter]] for a system of IMU and contact sensor dynamics with forward kinematic correction measurements. (Hartley et al., 2019) `ev:reported` p. 2 ^hartley2019contact-001
- The authors show that the deterministic contact-inertial system satisfies the [[Group-affine dynamics|group affine property]], therefore its error dynamics is exactly log-linear. (Hartley et al., 2019) `ev:computed` p. 2 ^hartley2019contact-002
- With the addition of sensor noise and IMU bias, the authors state that the log-linear error system is only approximate. (Hartley et al., 2019) `ev:asserted` p. 2 ^hartley2019contact-003
- The authors argue that in many cases the InEKF is still preferred over standard QEKFs due to superior convergence and consistency properties. (Hartley et al., 2019) `ev:asserted` p. 2 ^hartley2019contact-004
- Barrau and Bonnabel showed that [[Group-affine dynamics|group affine dynamics]] on a Lie group give an estimation error satisfying a log-linear autonomous equation. (Hartley et al., 2019) `ev:cited` p. 2 ^hartley2019contact-005
- Bloesch et al. developed a quaternion-based EKF combining inertial, contact, and kinematic data to estimate base pose, velocity, and contact states. (Hartley et al., 2019) `ev:cited` p. 2 ^hartley2019contact-006
- Because the EKF linearizes about the current state estimate, the paper notes it is at best only a locally stable observer. (Hartley et al., 2019) `ev:cited` p. 4 ^hartley2019contact-007
- The authors note that an EKF initialized with a poor state estimate can diverge, according to their review of Kalman filtering. (Hartley et al., 2019) `ev:asserted` p. 4 ^hartley2019contact-008
- Linearizing about the current estimate can lead an EKF to spuriously treat unobservable states as observable, the authors note. (Hartley et al., 2019) `ev:asserted` p. 4 ^hartley2019contact-009
- Kinematic odometry estimates are typically noisy due to kinematic modeling errors, encoder noise, and foot slip, according to cited work. (Hartley et al., 2019) `ev:cited` p. 5 ^hartley2019contact-010
- Bloesch et al. proved that absolute positions and yaw angles are unobservable when a legged robot uses proprioceptive sensing only. (Hartley et al., 2019) `ev:cited` p. 6 ^hartley2019contact-011
- Unlike the decoupled state of Bloesch et al., the authors model the entire state as a single matrix Lie group. (Hartley et al., 2019) `ev:asserted` p. 6 ^hartley2019contact-012
- The authors state that the implemented filters can be run at high speeds (> 2000 Hz) for accurate local odometry. (Hartley et al., 2019) `ev:asserted` p. 6 ^hartley2019contact-013
- The filter state holds the IMU orientation, velocity, and position in the world frame plus the world positions of all contact points. (Hartley et al., 2019) `ev:reported` p. 10 ^hartley2019contact-014
- For N contact points, the state variables form the matrix Lie group SEN+2(3), which the authors describe as an extension of SE(3). (Hartley et al., 2019) `ev:reported` p. 10 ^hartley2019contact-015
- When a binary sensor indicates contact, the contact point velocity is modelled as zero plus white Gaussian noise to accommodate potential slippage. (Hartley et al., 2019) `ev:reported` p. 11 ^hartley2019contact-016
- The IMU angular velocity and linear acceleration measurements are modelled as corrupted by additive Gaussian white noise processes. (Hartley et al., 2019) `ev:reported` p. 11 ^hartley2019contact-017
- For the bias-free right-invariant filter, the linearized error dynamics matrix is time-invariant, although in general it can be time-varying. (Hartley et al., 2019) `ev:computed` p. 12 ^hartley2019contact-018
- The forward kinematic position measurement has the right-invariant observation form, so the innovation depends solely on the invariant error. (Hartley et al., 2019) `ev:computed` p. 13 ^hartley2019contact-019
- The linear observability analysis of the right-invariant filter shows that the absolute position of the robot is unobservable. (Hartley et al., 2019) `ev:computed` p. 14 ^hartley2019contact-020
- Since gravity only has a z component, the observability analysis shows that rotation about the gravity vector, yaw, is unobservable. (Hartley et al., 2019) `ev:computed` p. 14 ^hartley2019contact-021
- The authors report that their linear observability analysis agrees with the nonlinear results of Bloesch et al. with much less computation. (Hartley et al., 2019) `ev:asserted` p. 14 ^hartley2019contact-022
- By default, the discrete RIEKF has the same unobservable states as the underlying nonlinear system, according to the authors' analysis. (Hartley et al., 2019) `ev:computed` p. 14 ^hartley2019contact-023
- The QEKF linearizations depend on the state estimate, so a deviating estimate potentially reduces QEKF accuracy and consistency, the authors argue. (Hartley et al., 2019) `ev:asserted` p. 15 ^hartley2019contact-024
- The linearized observation matrix of the proposed [[Invariant extended Kalman filter|InEKF]] is independent of the state estimate, unlike the QEKF observation matrix. (Hartley et al., 2019) `ev:computed` p. 15 ^hartley2019contact-025
- The simulated Cassie-series robot slowly walked forward after a small drop, accelerating from 0.0 to 0.3 m / sec. (Hartley et al., 2019) `ev:reported` p. 15 ^hartley2019contact-026
- The Simscape Multibody simulation modelled ground contact forces with a linear force law with stiffness and damping plus Coulomb friction. (Hartley et al., 2019) `ev:reported` p. 15 ^hartley2019contact-027
- The initial IMU orientation standard deviation was set to 30.0 deg in both simulation and experimental convergence evaluations of the filters. (Hartley et al., 2019) `ev:reported` p. 15 ^hartley2019contact-028
- In simulation, each filter was run 100 times with identical measurements, noise statistics, and initial covariance but random initial orientations and velocities. (Hartley et al., 2019) `ev:reported` p. 15 ^hartley2019contact-029
- Initial Euler angle estimates in the convergence comparison were sampled uniformly from −30 deg to 30 deg for both filters. (Hartley et al., 2019) `ev:reported` p. 15 ^hartley2019contact-030
- IMU bias estimation was turned off for the simulated convergence comparison between the right-invariant EKF and the quaternion EKF. (Hartley et al., 2019) `ev:reported` p. 15 ^hartley2019contact-031
- In simulation, both filters converge for the sampled initial conditions, but the RIEKF converges considerably faster than the quaternion-based EKF. (Hartley et al., 2019) `ev:computed` p. 16 ^hartley2019contact-032
- In the simulated comparison, the estimated yaw angle does not converge for either filter because yaw is unobservable. (Hartley et al., 2019) `ev:computed` p. 16 ^hartley2019contact-033
- With deterministic dynamics, the difference between true and propagated [[Invariant extended Kalman filter|InEKF]] error states was always exactly zero regardless of the initial error. (Hartley et al., 2019) `ev:computed` p. 16 ^hartley2019contact-034
- As the initial error increases, the difference between true and propagated error states for the QEKF grows in the deterministic test. (Hartley et al., 2019) `ev:computed` p. 16 ^hartley2019contact-035
- With sensor noise, the InEKF propagated error is no longer exact, but its linearization remains more accurate than the QEKF linearization. (Hartley et al., 2019) `ev:computed` p. 16 ^hartley2019contact-036
- The covariance comparison propagated 10,000 particles while the simulated Cassie walked forward for 8 sec at an average speed of 1 m/s. (Hartley et al., 2019) `ev:reported` p. 17 ^hartley2019contact-037
- Because samples are mapped from the Lie algebra, the [[Invariant extended Kalman filter|InEKF]] closely matches the curved position distribution produced by growing yaw uncertainty. (Hartley et al., 2019) `ev:computed` p. 18 ^hartley2019contact-038
- The QEKF position uncertainty can only take a standard Gaussian ellipse shape, which may not represent the true uncertainty well. (Hartley et al., 2019) `ev:asserted` p. 18 ^hartley2019contact-039
- The InEKF modelled a completely uncertain initial yaw with a 360 deg standard deviation, which a Gaussian covariance ellipse cannot capture. (Hartley et al., 2019) `ev:computed` p. 18 ^hartley2019contact-040
- As noted by Barrau, no Lie group includes the IMU bias terms while keeping the dynamics group affine. (Hartley et al., 2019) `ev:cited` p. 18 ^hartley2019contact-041
- With IMU biases, the augmented invariant error dynamics depend on the estimated trajectory only through the noise and bias errors. (Hartley et al., 2019) `ev:computed` p. 20 ^hartley2019contact-042
- A contact point is removed by marginalization, deleting its row and column from the state matrix and the covariance. (Hartley et al., 2019) `ev:reported` p. 21 ^hartley2019contact-043
- When a new contact is made, the initial mean of the contact point is obtained through the forward kinematics relation. (Hartley et al., 2019) `ev:reported` p. 21 ^hartley2019contact-044
- The Cassie-series robot used in experiments has 20 degrees of freedom, 10 actuators, 4 springs, and 14 joint encoders. (Hartley et al., 2019) `ev:reported` p. 22 ^hartley2019contact-045
- The torso-mounted VectorNav-100 IMU provides angular velocity and linear acceleration measurements to the filters at 800 Hz on Cassie. (Hartley et al., 2019) `ev:reported` p. 22 ^hartley2019contact-046
- On the Cassie robot, the encoders provide joint angle measurements at 2000 Hz for the forward kinematic corrections. (Hartley et al., 2019) `ev:reported` p. 22 ^hartley2019contact-047
- Spring deflections on each leg, measured by encoders, serve as a binary contact sensor for the Cassie filter experiments. (Hartley et al., 2019) `ev:reported` p. 22 ^hartley2019contact-048
- On logged hardware data from walking at approximately 0.3 m / sec, each filter was run off-line 100 times with random initializations. (Hartley et al., 2019) `ev:reported` p. 22 ^hartley2019contact-049
- In the hardware experiment with bias estimation on, the RIEKF converges faster and more reliably than the QEKF in all 100 runs. (Hartley et al., 2019) `ev:measured` p. 22 ^hartley2019contact-050
- When the state estimate is initialized close to the true value, the RIEKF and QEKF have similar performance in the experiments. (Hartley et al., 2019) `ev:measured` p. 23 ^hartley2019contact-051
- Although the theoretical advantage is lost with bias estimation on, experiments indicate the RIEKF is still preferred due to less sensitivity to initialization. (Hartley et al., 2019) `ev:measured` p. 23 ^hartley2019contact-052
- In the motion capture experiment, Cassie walked untethered for 60 sec along an approximately 15 m path tracked by 18 Qualisys cameras. (Hartley et al., 2019) `ev:reported` p. 23 ^hartley2019contact-053
- In the motion capture experiment, the final position error of the InEKF accounts for less than 5% of the distance traveled. (Hartley et al., 2019) `ev:measured` p. 23 ^hartley2019contact-054
- The authors attribute the position drift to sensor noise and imperfect kinematic modeling, which may bias the forward kinematic measurements. (Hartley et al., 2019) `ev:asserted` p. 23 ^hartley2019contact-055
- Orientation ground truth came from the VectorNav-100 on-board QEKF because the motion capture orientation estimate was inaccurate. (Hartley et al., 2019) `ev:reported` p. 23 ^hartley2019contact-056
- In the long odometry experiment, Cassie walked about 200 m along a sidewalk over 7 minutes and 45 seconds. (Hartley et al., 2019) `ev:reported` p. 24 ^hartley2019contact-057
- The InEKF odometry drift stayed low enough to keep the estimate on the sidewalk for the whole long odometry experiment. (Hartley et al., 2019) `ev:measured` p. 24 ^hartley2019contact-058
- At the end of the long walk, the InEKF position estimate was within a few meters of the true position. (Hartley et al., 2019) `ev:measured` p. 24 ^hartley2019contact-059
- Cassie carried a Velodyne VLP-32C LiDAR whose point clouds were projected into the world frame using the InEKF state estimate. (Hartley et al., 2019) `ev:reported` p. 24 ^hartley2019contact-060
- Switching between left- and right-invariant error covariances through the adjoint map is exact, according to the derivation in the paper. (Hartley et al., 2019) `ev:computed` p. 28 ^hartley2019contact-061
- In the robo-centric estimator, forward kinematics measurements take the left-invariant observation form rather than the right-invariant form. (Hartley et al., 2019) `ev:computed` p. 29 ^hartley2019contact-062
- The authors suggest the robo-centric filter may be preferred in some cases since it directly estimates body-frame velocity for control. (Hartley et al., 2019) `ev:asserted` p. 29 ^hartley2019contact-063
- The authors describe the contact-aided InEKF as identical to landmark-based SLAM with contact positions acting as landmarks. (Hartley et al., 2019) `ev:asserted` p. 31 ^hartley2019contact-064
- Unlike landmark observations, forward kinematic measurements do not require solving a data association problem, the authors note. (Hartley et al., 2019) `ev:asserted` p. 31 ^hartley2019contact-065
- The authors note that replacing contacts with landmark states could give an observer that contains no unobservable states. (Hartley et al., 2019) `ev:asserted` p. 31 ^hartley2019contact-066
- The authors propose future work on an invariant smoother using IMU and contact preintegration to perform SLAM. (Hartley et al., 2019) `ev:asserted` p. 32 ^hartley2019contact-067
- The authors suggest online estimation of kinematic parameters, which may help remove biases in the forward kinematic measurements. (Hartley et al., 2019) `ev:asserted` p. 32 ^hartley2019contact-068
- For discretization, the implementation assumed a zero-order hold on the inertial measurements and performed analytical integration of the filter equations. (Hartley et al., 2019) `ev:reported` p. 34 ^hartley2019contact-069

## 🎯 Contributions

## 📖 Glossary

- **InEKF** — Invariant extended Kalman filter; its estimation error is invariant under a Lie group action.
- **Group affine property** — Dynamics condition making invariant error dynamics independent of the system trajectory.
- **Log-linear error** — Nonlinear invariant error exactly recovered from a linear system on the Lie algebra.
- **Right-invariant error** — Error defined as estimated state times inverse true state; expressed in world frame.
- **Left-invariant error** — Error defined as inverse true state times estimated state; expressed in body frame.
- **QEKF** — Quaternion-based error-state EKF with decoupled orientation, velocity and position errors.
- **SEN+2(3)** — Matrix Lie group extending SE(3) with velocity and N contact point positions.
- **Concentrated Gaussian** — Gaussian in the Lie algebra mapped onto the group through the exponential map.
- **Robo-centric estimator** — Filter whose state is expressed in the robot base (IMU) frame.

## ❓ Open questions

- How much does online estimation of kinematic parameters reduce the forward kinematic biases that drive position drift?
- Can an invariant smoother with IMU and contact preintegration outperform the filter for legged SLAM?
- How does the imperfect InEKF compare with the QEKF when IMU biases are large or poorly initialized?
- Can gait mode detection (standing, turning) add constraints that improve InEKF odometry?
- How well does visual-inertial-contact odometry with an InEKF perform, and can prior terrain information be incorporated?

## 📝 Notes on reading

Read the arXiv v2 preprint (10 Nov 2019, 1904.09251v2), matching the packet identifier. Convergence results (Figures 3 and 8), linearization-accuracy curves (Figures 4 and 5), covariance particle plots (Figures 6 and 7), motion capture traces (Figures 9 and 10), the long walk overlay (Figure 11) and LiDAR maps (Figure 12) are only described in the text; no numeric values were read from them. Matrix equations throughout (state, adjoint, dynamics, observability matrix, Tables 2 and 3, Appendices A to C) are garbled by extraction and were not claimed. Table 1 noise values are legible, but only the initial orientation standard deviation was claimed. The motion capture text reports a final position error below 5% of distance traveled; no absolute error is given. The paper extends the authors' earlier conference paper on the contact-aided InEKF.

## Suggested new concepts

- Invariant extended Kalman filter — a recurring estimator family across legged and inertial navigation papers.
- Group affine dynamics — the key condition for log-linear, trajectory-independent error dynamics.
- Contact-aided inertial navigation — fusing IMU, contact and kinematics is the standard proprioceptive state-estimation setup for legged robots.
- Observability of legged robot state estimation — absolute position and yaw unobservability recurs across estimators.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H2.** Extiende el EKF invariante de Barrau2017 usando la cinemática directa como medida en un grupo de Lie matricial, plantilla directa para fusionar encoders y cámara.
