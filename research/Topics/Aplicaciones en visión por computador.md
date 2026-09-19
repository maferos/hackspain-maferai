---
type: "topic"
title: "Aplicaciones en visión por computador"
document: "[[03_aplicaciones_vision_por_computador]]"
---

# Aplicaciones en visión por computador

Documento de investigación: [[03_aplicaciones_vision_por_computador]] · 72 fuentes, 61 con PDF.

| Fuente | Año | PDF | Por qué |
|---|---|---|---|
| [[Tsai1989new - A new technique for fully autonomous and efficient 3D\|Tsai1989new]] | 1989 | — | Método clásico de mano-ojo, incluido en OpenCV |
| [[Park1994robot - Robot sensor calibration solving AX=XB on the Euclidean\|Park1994robot]] | 1994 | — | Calibración mano-ojo resuelta en el álgebra de Lie (§1.5) |
| [[Chaumette2006visual - Visual servo control, Part I Basic approaches\|Chaumette2006visual]] | 2006 | — | IBVS, PBVS y matriz de interacción (§3) |
| [[Chaumette2007visual - Visual servo control, Part II Advanced approaches\|Chaumette2007visual]] | 2007 | — | Esquemas híbridos, estimación de $L_s$, seguimiento |
| [[Collewet2011photometric - Photometric visual servoing\|Collewet2011photometric]] | 2011 | — | Servo directo sobre intensidades |
| [[Todorov2012mujoco - MuJoCo A physics engine for model-based control\|Todorov2012mujoco]] | 2012 | — | Simulador del proyecto |
| [[Engel2016direct - Direct Sparse Odometry\|Engel2016direct]] | 2016 | ✅ | Odometría directa fotométrica en $SE(3)$ |
| [[Forster2016manifold - On-Manifold Preintegration for Real-Time Visual-Inertial\|Forster2016manifold]] | 2016 | ✅ | Preintegración IMU en $SO(3)$ |
| [[Barrau2017invariant - The invariant extended Kalman filter as a stable observer\|Barrau2017invariant]] | 2017 | ✅ | IEKF: error autónomo en grupos de Lie |
| [[Bateux2017visual - Visual Servoing from Deep Neural Networks\|Bateux2017visual]] | 2017 | ✅ | CNN de pose relativa más PBVS, datos generados automáticamente |
| [[Tobin2017domain - Domain Randomization for Transferring Deep Neural Networks\|Tobin2017domain]] | 2017 | ✅ | Fundamento de la aleatorización de dominio (§6.5) |
| [[Xiang2017posecnn - PoseCNN A Convolutional Neural Network for 6D Object Pose\|Xiang2017posecnn]] | 2017 | ✅ | Regresión directa de pose, pérdida para simetrías, YCB-Video |
| [[Falorsi2018explorations - Explorations in Homeomorphic Variational Auto-Encoding\|Falorsi2018explorations]] | 2018 | ✅ | Latentes en $SO(3)$ por razones topológicas (§7) |
| [[Hodan2018bop - BOP Benchmark for 6D Object Pose Estimation\|Hodan2018bop]] | 2018 | ✅ | Definición original del benchmark y del formato |
| [[Peng2018pvnet - PVNet Pixel-wise Voting Network for 6DoF Pose Estimation\|Peng2018pvnet]] | 2018 | ✅ | Puntos clave por votación más PnP, robusto a la oclusión |
| [[Sola2018micro - A micro Lie theory for state estimation in robotics\|Sola2018micro]] | 2018 | ✅ | Referencia práctica de $\mathrm{Exp}/\mathrm{Log}$, Jacobianos y perturbaciones usada en §1 y §3 (desarrollada en la parte 1) |
| [[Liu2019keypose - KeyPose Multi-View 3D Labeling and Keypoint Estimation for\|Liu2019keypose]] | 2019 | ✅ | Pose de objetos transparentes desde estéreo, sin profundidad |
| [[Sajjan2019cleargrasp - ClearGrasp 3D Shape Estimation of Transparent Objects for\|Sajjan2019cleargrasp]] | 2019 | ✅ | Completado de profundidad para objetos transparentes |
| [[Wang2019densefusion - DenseFusion 6D Object Pose Estimation by Iterative Dense\|Wang2019densefusion]] | 2019 | ✅ | *Baseline* RGB-D entrenable con datos propios |
| [[Zhou2019continuity - On the Continuity of Rotation Representations in Neural\|Zhou2019continuity]] | 2019 | ✅ | Justifica la representación 6D (§2.3, §6.3) |
| [[Campos2020orb - ORB-SLAM3 An Accurate Open-Source Library for Visual,\|Campos2020orb]] | 2020 | ✅ | SLAM de referencia basado en características |
| [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and\|Deng2020deep]] | 2020 | ✅ | Mezclas de Bingham sobre cuaterniones |
| [[Fang2020graspnet - GraspNet-1Billion A Large-Scale Benchmark for General\|Fang2020graspnet]] | 2020 | — | Benchmark estándar de agarre 6-DoF |
| [[Fuchs2020se - SE(3)-Transformers 3D Roto-Translation Equivariant\|Fuchs2020se]] | 2020 | ✅ | Atención equivariante a $SE(3)$ |
| [[Harish2020dfvs - DFVS Deep Flow Guided Scene Agnostic Image Based Visual\|Harish2020dfvs]] | 2020 | ✅ | Flujo aprendido más matriz de interacción |
| [[Labbe2020cosypose - CosyPose Consistent multi-view multi-object 6D pose\|Labbe2020cosypose]] | 2020 | ✅ | *Render-and-compare* y BA a nivel de objeto (varias cámaras) |
| [[Mohlin2020probabilistic - Probabilistic orientation estimation with matrix Fisher\|Mohlin2020probabilistic]] | 2020 | ✅ | Distribución de Fisher matricial en $SO(3)$ con NLL |
| [[YenChen2020inerf - iNeRF Inverting Neural Radiance Fields for Pose Estimation\|YenChen2020inerf]] | 2020 | ✅ | Pose por inversión de un campo de radiancia en $SE(3)$ |
| [[Zeng2020transporter - Transporter Networks Rearranging the Visual World for\|Zeng2020transporter]] | 2020 | ✅ | *Pick-and-place* $SE(2)$-equivariante y eficiente en muestras |
| [[Deng2021vector - Vector Neurons A General Framework for SO(3)-Equivariant\|Deng2021vector]] | 2021 | ✅ | Capas equivariantes simples para nubes de puntos |
| [[Felton2021siame - Siame-se(3) regression in se(3) for end-to-end visual\|Felton2021siame]] | 2021 | — | Regresión directa del *twist* en $\mathfrak{se}(3)$ entrenada en simulación |
| [[Lin2021barf - BARF Bundle-Adjusting Neural Radiance Fields\|Lin2021barf]] | 2021 | ✅ | Optimización conjunta de NeRF y poses, de grueso a fino |
| [[Murphy2021implicit - Implicit-PDF Non-Parametric Representation of Probability\|Murphy2021implicit]] | 2021 | ✅ | Densidades multimodales en $SO(3)$ para objetos simétricos |
| [[Simeonov2021neural - Neural Descriptor Fields SE(3)-Equivariant Object\|Simeonov2021neural]] | 2021 | ✅ | Transferencia de agarres por optimización en $SE(3)$ con pocas demos |
| [[Sundermeyer2021contact - Contact-GraspNet Efficient 6-DoF Grasp Generation in\|Sundermeyer2021contact]] | 2021 | ✅ | Agarres 6-DoF anclados a contactos |
| [[Teed2021droid - DROID-SLAM Deep Visual SLAM for Monocular, Stereo, and\|Teed2021droid]] | 2021 | ✅ | *Dense BA* diferenciable con lietorch |
| [[Teed2021tangent - Tangent Space Backpropagation for 3D Transformation Groups\|Teed2021tangent]] | 2021 | ✅ | Biblioteca para retropropagar en el tangente de $SE(3)$/$Sim(3)$ |
| [[Wang2021gdr - GDR-Net Geometry-Guided Direct Regression Network for\|Wang2021gdr]] | 2021 | — | Patch-PnP diferenciable y rotación 6D |
| [[Zhu2021commutative - Commutative Lie Group VAE for Disentanglement Learning\|Zhu2021commutative]] | 2021 | ✅ | Desenmarañamiento como acción de grupo de Lie |
| [[Chen2022clearpose - ClearPose Large-scale Transparent Object Dataset and\|Chen2022clearpose]] | 2022 | ✅ | Benchmark de pose de objetos transparentes (con líquidos) |
| [[DeepMind2022mujoco - MuJoCo Menagerie\|DeepMind2022mujoco]] | 2022 | — | Modelos de brazos adicionales |
| [[Fang2022anygrasp - AnyGrasp Robust and Efficient Grasp Perception in Spatial\|Fang2022anygrasp]] | 2022 | ✅ | Agarres densos con seguimiento temporal |
| [[Fang2022transcg - TransCG A Large-Scale Real-World Dataset for Transparent\|Fang2022transcg]] | 2022 | ✅ | Datos reales y red rápida para el *sim-to-real* de vidrio |
| [[Geiger2022e3nn - e3nn Euclidean Neural Networks\|Geiger2022e3nn]] | 2022 | ✅ | Biblioteca general $E(3)$-equivariante (irreps) |
| [[Huang2022edge - Edge Grasp Network A Graph-Based SE(3)-invariant Approach\|Huang2022edge]] | 2022 | ✅ | Evaluación de agarres invariante a $SE(3)$ |
| [[Labbe2022megapose - MegaPose 6D Pose Estimation of Novel Objects via Render &\|Labbe2022megapose]] | 2022 | ✅ | Pose de objetos nuevos con solo CAD |
| [[Wang2022pypose - PyPose A Library for Robot Learning with Physics-based\|Wang2022pypose]] | 2022 | ✅ | Grupos de Lie y optimizadores de 2.º orden en PyTorch |
| [[Brohan2023rt - RT-2 Vision-Language-Action Models Transfer Web Knowledge\|Brohan2023rt]] | 2023 | ✅ | VLA con acciones como tokens |
| [[Chen2023easyhec - EasyHeC Accurate and Automatic Hand-eye Calibration via\|Chen2023easyhec]] | 2023 | ✅ | Calibración sin marcadores con renderizado diferenciable en $SE(3)$ |
| [[Chi2023diffusion - Diffusion Policy Visuomotor Policy Learning via Action\|Chi2023diffusion]] | 2023 | ✅ | Política visuomotora por difusión, rotación 6D |
| [[Gabel2023learning - Learning Lie Group Symmetry Transformations with Neural\|Gabel2023learning]] | 2023 | ✅ | Descubrimiento de generadores de simetrías |
| [[Jiang2023robotic - Robotic Perception of Transparent Objects A Review\|Jiang2023robotic]] | 2023 | ✅ | Revisión del estado del arte en transparencia |
| [[Lin2023sam - SAM-6D Segment Anything Model Meets Zero-Shot 6D Object\|Lin2023sam]] | 2023 | ✅ | Alternativa *zero-shot* a FoundationPose |
| [[Liu2023grounding - Grounding DINO Marrying DINO with Grounded Pre-Training for\|Liu2023grounding]] | 2023 | ✅ | Detección de "tubo de centrífuga" por texto |
| [[Matsuki2023gaussian - Gaussian Splatting SLAM\|Matsuki2023gaussian]] | 2023 | ✅ | Seguimiento de cámara con Jacobianos en $\mathfrak{se}(3)$ sobre 3DGS |
| [[Wen2023foundationpose - FoundationPose Unified 6D Pose Estimation and Tracking of\|Wen2023foundationpose]] | 2023 | ✅ | Estimador y seguidor recomendado para el tubo (§8) |
| [[Zhao2023learning - Learning Fine-Grained Bimanual Manipulation with Low-Cost\|Zhao2023learning]] | 2023 | ✅ | ACT y hardware ALOHA (el brazo de nuestra escena) |
| [[Black2024vision - π0 A Vision-Language-Action Flow Model for General Robot\|Black2024vision]] | 2024 | ✅ | VLA con *flow matching*, evaluado en AutoBio |
| [[Chi2024universal - Universal Manipulation Interface In-The-Wild Robot Teaching\|Chi2024universal]] | 2024 | ✅ | Acciones relativas en el grupo: invariancia al marco |
| [[Hodan2024bop - BOP Challenge 2023 on Detection, Segmentation and Pose\|Hodan2024bop]] | 2024 | ✅ | Benchmark, métricas VSD/MSSD/MSPD y formato de datos |
| [[Kim2024openvla - OpenVLA An Open-Source Vision-Language-Action Model\|Kim2024openvla]] | 2024 | ✅ | VLA abierto ajustable con LoRA, acciones $\Delta$ discretizadas |
| [[Li2024chemistry3d - Chemistry3D Robotic Interaction Benchmark for Chemistry\|Li2024chemistry3d]] | 2024 | ✅ | Otro benchmark de automatización de laboratorio |
| [[Lim2024equigraspflow - EquiGraspFlow SE(3)-Equivariant 6-DoF Grasp Pose Generative\|Lim2024equigraspflow]] | 2024 | — | Flujos generativos en la variedad $SE(3)$ para agarres |
| [[Liu2024rdt - RDT-1B a Diffusion Foundation Model for Bimanual\|Liu2024rdt]] | 2024 | ✅ | Modelo bimanual evaluado en AutoBio (harness en el repo) |
| [[Makarova2024lucidgrasp - LucidGrasp Robotic Framework for Autonomous Manipulation of\|Makarova2024lucidgrasp]] | 2024 | ✅ | Manipulación de material de laboratorio transparente con pose 6D |
| [[Ravi2024sam - SAM 2 Segment Anything in Images and Videos\|Ravi2024sam]] | 2024 | ✅ | Máscaras y seguimiento en vídeo para FoundationPose |
| [[Team2024octo - Octo An Open-Source Generalist Robot Policy\|Team2024octo]] | 2024 | ✅ | Política generalista con cabeza de difusión, fácil de ajustar |
| [[Wang2024equivariant - Equivariant Diffusion Policy\|Wang2024equivariant]] | 2024 | ✅ | Diffusion Policy con *denoiser* equivariante |
| [[Yang2024equibot - EquiBot SIM(3)-Equivariant Diffusion Policy\|Yang2024equibot]] | 2024 | ✅ | Política equivariante a rotación, traslación y escala |
| [[Intelligence2025vision - π0.5 a Vision-Language-Action Model with Open-World\|Intelligence2025vision]] | 2025 | ✅ | Co-entrenamiento heterogéneo para la generalización |
| [[Lan2025autobio - AutoBio A Simulation and Benchmark for Robotic Automation\|Lan2025autobio]] | 2025 | ✅ | Base de la escena. Muestra que la precisión es el cuello de botella de los VLA |
| [[Pertsch2025fast - FAST Efficient Action Tokenization for\|Pertsch2025fast]] | 2025 | ✅ | Tokenización DCT de acciones |
