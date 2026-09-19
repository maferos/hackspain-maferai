---
type: "topic"
title: "Optimización y algoritmos"
document: "[[02_optimizacion_y_algoritmos]]"
---

# Optimización y algoritmos

Documento de investigación: [[02_optimizacion_y_algoritmos]] · 65 fuentes, 49 con PDF.

| Fuente | Año | PDF | Por qué |
|---|---|---|---|
| [[Deray0manif - manif — small C++11 header-only library for Lie theory\|Deray0manif]] |  | — | Jacobianos analíticos en el tangente; compañero de (3). |
| [[Strasdat0sophus - Sophus — C++ implementation of Lie Groups using Eigen\|Strasdat0sophus]] |  | — | Implementación de referencia en C++/SLAM (A.6). |
| [[UtiasSTARS0liegroups - liegroups — SO2SE2SO3SE3 in numpy or pytorch\|UtiasSTARS0liegroups]] |  | — | Implementación ligera (sin mantenimiento; ver PyMLG) (A.6). |
| [[Yi0jaxlie - jaxlie — Rigid transforms + Lie groups for JAX\|Yi0jaxlie]] |  | — | $SO(3)$/$SE(3)$ en JAX con `manifold.grad` (A.6). |
| [[Zakka0mink - mink — Python inverse kinematics based on MuJoCo\|Zakka0mink]] |  | — | IK diferencial por QP nativa de MuJoCo; fijar 0.0.13 para MuJoCo 3.3.0 (F.3). |
| [[Amari1998natural - Natural Gradient Works Efficiently in Learning\|Amari1998natural]] | 1998 | — | Origen del gradiente natural y la métrica de Fisher (B.2). |
| [[Kakade2001natural - A Natural Policy Gradient\|Kakade2001natural]] | 2001 | — | Gradiente natural aplicado a políticas (B.5). |
| [[Buss2004introduction - Introduction to Inverse Kinematics with Jacobian Transpose,\|Buss2004introduction]] | 2004 | — | Análisis SVD de DLS para IK (C.1, F.3). |
| [[Absil2008optimization - Optimization Algorithms on Matrix Manifolds\|Absil2008optimization]] | 2008 | — | Texto clásico: gradiente riemanniano, retracciones, transporte vectorial, Newton y trust-regions en variedades (A). |
| [[Huynh2009metrics - Metrics for 3D Rotations Comparison and Analysis\|Huynh2009metrics]] | 2009 | — | Métricas en $SO(3)$ para pérdidas (D.4). |
| [[Kalakrishnan2011stomp - STOMP Stochastic Trajectory Optimization for Motion Planning\|Kalakrishnan2011stomp]] | 2011 | — | Optimización de trayectorias sin gradientes (C.2). |
| [[Raskutti2013information - The Information Geometry of Mirror Descent\|Raskutti2013information]] | 2013 | ✅ | Equivalencia descenso espejo ↔ gradiente natural (B.6). |
| [[Zucker2013chomp - CHOMP Covariant Hamiltonian Optimization for Motion Planning\|Zucker2013chomp]] | 2013 | — | Gradiente funcional covariante (natural) para trayectorias (C.2). |
| [[Martens2014new - New Insights and Perspectives on the Natural Gradient Method\|Martens2014new]] | 2014 | ✅ | Fisher = Gauss-Newton generalizada; amortiguamiento y trust regions (B.2). |
| [[Schulman2014motion - Motion planning with sequential convex optimization and\|Schulman2014motion]] | 2014 | — | SQP con trust region para planificación (C.2). |
| [[Martens2015optimizing - Optimizing Neural Networks with Kronecker-factored\|Martens2015optimizing]] | 2015 | ✅ | K-FAC: gradiente natural escalable (B.3). |
| [[Schulman2015trust - Trust Region Policy Optimization\|Schulman2015trust]] | 2015 | ✅ | Gradiente natural con restricción KL y CG (B.5, F.7). |
| [[Townsend2016pymanopt - Pymanopt A Python Toolbox for Optimization on Manifolds\|Townsend2016pymanopt]] | 2016 | ✅ | Toolbox de variedades con autodiff (A.6). |
| [[Arvanitidis2017latent - Latent Space Oddity on the Curvature of Deep Generative\|Arvanitidis2017latent]] | 2017 | ✅ | Métrica pullback estocástica y geodésicas latentes (E.3). |
| [[Li2017visualizing - Visualizing the Loss Landscape of Neural Nets\|Li2017visualizing]] | 2017 | ✅ | Geometría del paisaje de pérdida (E.2). |
| [[Lynch2017modern - Modern Robotics Mechanics, Planning, and Control\|Lynch2017modern]] | 2017 | — | Twists, producto de exponenciales, IK numérica en $SE(3)$ (C.1). |
| [[Schulman2017proximal - Proximal Policy Optimization Algorithms\|Schulman2017proximal]] | 2017 | ✅ | Sustituto de primer orden de la trust region; estándar para fine-tuning (B.5, D.2). |
| [[Wu2017scalable - Scalable trust-region method for deep RL using\|Wu2017scalable]] | 2017 | ✅ | K-FAC + trust region en actor-crítico, probado en MuJoCo (B.3, F.7). |
| [[Becigneul2018riemannian - Riemannian Adaptive Optimization Methods\|Becigneul2018riemannian]] | 2018 | ✅ | Adam/AMSGrad riemannianos en productos de variedades (A.5). |
| [[Boutselis2018differential - Differential Dynamic Programming on Lie Groups\|Boutselis2018differential]] | 2018 | ✅ | DDP libre de coordenadas en grupos de Lie (C.2). |
| [[Cheng2018rmpflow - RMPflow A Computational Graph for Automatic Motion Policy\|Cheng2018rmpflow]] | 2018 | ✅ | Combinación geométricamente consistente de RMPs (C.3). |
| [[Gupta2018shampoo - Shampoo Preconditioned Stochastic Tensor Optimization\|Gupta2018shampoo]] | 2018 | ✅ | Precondicionador de Kronecker por modos (B.4). |
| [[Jacot2018neural - Neural Tangent Kernel Convergence and Generalization in\|Jacot2018neural]] | 2018 | ✅ | Geometría del espacio de funciones (E.1). |
| [[Li2018natural - Natural gradient via optimal transport\|Li2018natural]] | 2018 | ✅ | Gradiente natural de Wasserstein (B.8). |
| [[Ratliff2018riemannian - Riemannian Motion Policies\|Ratliff2018riemannian]] | 2018 | ✅ | Políticas + métricas; analogía con el gradiente natural (C.3). |
| [[Sola2018micro - A micro Lie theory for state estimation in robotics\|Sola2018micro]] | 2018 | ✅ | Convención $\oplus/\ominus$ y jacobianos en el tangente usados en A.3–A.4 y C.1. |
| [[Arbel2019kernelized - Kernelized Wasserstein Natural Gradient\|Arbel2019kernelized]] | 2019 | ✅ | Estimador escalable del gradiente natural de Wasserstein (B.8). |
| [[Karakida2019pathological - Pathological spectra of the Fisher information metric and\|Karakida2019pathological]] | 2019 | ✅ | Espectro de la Fisher y relación con el NTK (E.1). |
| [[Zhou2019continuity - On the Continuity of Rotation Representations in Neural\|Zhou2019continuity]] | 2019 | ✅ | Representación 6D continua (D.4). |
| [[Calinon2020gaussians - Gaussians on Riemannian Manifolds Applications for Robot\|Calinon2020gaussians]] | 2020 | ✅ | GMM/GMR/LQR en variedades (C.4). |
| [[Kochurov2020geoopt - Geoopt Riemannian Optimization in PyTorch\|Kochurov2020geoopt]] | 2020 | ✅ | `RiemannianAdam`/`RiemannianSGD` en PyTorch (A.5–A.6). |
| [[BeikMohammadi2021learning - Learning Riemannian Manifolds for Geodesic Motion Skills\|BeikMohammadi2021learning]] | 2021 | ✅ | Geodésicas de métricas pullback como habilidades (C.4, E.3). |
| [[Hu2021lora - LoRA Low-Rank Adaptation of Large Language Models\|Hu2021lora]] | 2021 | ✅ | Adaptación de bajo rango (D.3). |
| [[Jaquier2021geometry - Geometry-aware Bayesian Optimization in Robotics using\|Jaquier2021geometry]] | 2021 | ✅ | BO en $SO(3)$, esferas, SPD (C.4, F.7 ruta C). |
| [[Teed2021tangent - Tangent Space Backpropagation for 3D Transformation Groups\|Teed2021tangent]] | 2021 | ✅ | Retropropagación en el álgebra de Lie; base conceptual de los gradientes en el tangente (A.6). |
| [[Wyk2021geometric - Geometric Fabrics Generalizing Classical Mechanics to\|Wyk2021geometric]] | 2021 | ✅ | Estabilidad garantizada con geometrías de Finsler (C.3). |
| [[BeikMohammadi2022reactive - Reactive Motion Generation on Learned Riemannian Manifolds\|BeikMohammadi2022reactive]] | 2022 | ✅ | Versión reactiva con evitación de obstáculos (C.4, E.3). |
| [[Jaquier2022riemannian - Riemannian geometry as a unifying theory for robot motion\|Jaquier2022riemannian]] | 2022 | ✅ | Marco conceptual riemanniano para movimiento robótico (C.4). |
| [[Pineda2022theseus - Theseus A Library for Differentiable Nonlinear Optimization\|Pineda2022theseus]] | 2022 | ✅ | GN/LM diferenciables con grupos de Lie como capa de red (A.6, F.5). |
| [[Teng2022error - An Error-State MPC on Connected Matrix Lie Groups for\|Teng2022error]] | 2022 | ✅ | MPC convexo de estado de error en $\mathfrak{g}$ (C.2). |
| [[Teng2022lie - Lie Algebraic Cost Function Design for Control on Lie Groups\|Teng2022lie]] | 2022 | ✅ | Costes en el álgebra con convergencia exponencial (C.2, F.4). |
| [[Urain2022se - SE(3)-DiffusionFields\|Urain2022se]] | 2022 | ✅ | Difusión en $SE(3)$ como coste de agarre + trayectoria (C.5). |
| [[Wang2022pypose - PyPose A Library for Robot Learning with Physics-based\|Wang2022pypose]] | 2022 | ✅ | `LieTensor` + optimizadores LM con trust region; librería recomendada en F. |
| [[Wang2022so - SO(2)-Equivariant Reinforcement Learning\|Wang2022so]] | 2022 | ✅ | RL equivariante para manipulación (C.6). |
| [[Zhao2022symmetry - Symmetry Teleportation for Accelerated Optimization\|Zhao2022symmetry]] | 2022 | ✅ | Explotar simetrías del paisaje de parámetros (E.4). |
| [[Alcan2023constrained - Constrained Trajectory Optimization on Matrix Lie Groups\|Alcan2023constrained]] | 2023 | ✅ | DDP con restricciones en el álgebra (C.2). |
| [[Boumal2023introduction - An Introduction to Optimization on Smooth Manifolds\|Boumal2023introduction]] | 2023 | — | Referencia moderna y gratuita; complejidad de RGD, convexidad geodésica (A). |
| [[Chen2023flow - Flow Matching on General Geometries\|Chen2023flow]] | 2023 | ✅ | Riemannian Flow Matching (C.5, F.6). |
| [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action\|Chi2023diffusion]] | 2023 | ✅ | Políticas de difusión con *action chunks* (C.5, F.6). |
| [[Black2024vision - π0 A Vision-Language-Action Flow Model for General Robot\|Black2024vision]] | 2024 | ✅ | VLA con *action expert* de flow matching (D.1). |
| [[Braun2024riemannian - Riemannian Flow Matching Policy for Robot Motion Learning\|Braun2024riemannian]] | 2024 | ✅ | RFM aplicado a políticas visuomotoras (C.5). |
| [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model\|Kim2024openvla]] | 2024 | ✅ | VLA abierto con fine-tuning LoRA (D.1). |
| [[Lim2024equigraspflow - EquiGraspFlow SE(3)-Equivariant 6-DoF Grasp Pose Generative\|Lim2024equigraspflow]] | 2024 | — | Flujos equivariantes para agarres (C.5, F.4). |
| [[Ren2024diffusion - Diffusion Policy Policy Optimization (DPPO)\|Ren2024diffusion]] | 2024 | ✅ | PPO sobre la cadena de denoising (D.2, F.7). |
| [[Wang2024equivariant - Equivariant Diffusion Policy\|Wang2024equivariant]] | 2024 | ✅ | Difusión con denoiser equivariante (C.6). |
| [[Yang2024equibot - EquiBot SIM(3)-Equivariant Diffusion Policy\|Yang2024equibot]] | 2024 | ✅ | Equivariancia a rotación/traslación/escala (C.6). |
| [[Zhang2024riemannian - Riemannian Preconditioned LoRA for Fine-Tuning Foundation\|Zhang2024riemannian]] | 2024 | ✅ | Precondicionador $r\times r$ desde una métrica riemanniana (D.3). |
| [[Lan2025autobio - AutoBio A Simulation and Benchmark for Robotic Automation\|Lan2025autobio]] | 2025 | ✅ | Origen de la escena y de la evaluación de VLAs en laboratorio (contexto, F). |
| [[Zakka2025mujoco - MuJoCo Playground\|Zakka2025mujoco]] | 2025 | ✅ | Entrenamiento masivo en GPU con MJX (alternativa en F.1). |
| [[Zhang2025reinflow - ReinFlow Fine-tuning Flow Matching Policy with Online RL\|Zhang2025reinflow]] | 2025 | ✅ | RL para políticas de flujo con ruido aprendible (D.2). |
