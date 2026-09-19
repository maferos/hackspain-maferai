# Parte 4 — Huecos del corpus y ampliación

> **Contexto.** Este documento es la parte 4 de la investigación del reto MAFER. Tras ingerir las fuentes de [`01_matematicas_grupos_de_lie.md`](01_matematicas_grupos_de_lie.md), [`02_optimizacion_y_algoritmos.md`](02_optimizacion_y_algoritmos.md) y [`03_aplicaciones_vision_por_computador.md`](03_aplicaciones_vision_por_computador.md) en el vault, se midió la cobertura por eje. El pilar matemático tenía 40 fuentes, pero 19 eran libros sin PDF y sin claims, y había huecos en optimización de trayectorias, *fine-tuning* geométrico, calibración y servo visual, *neural manifolds* y el contexto de laboratorio. Cada sección de abajo cubre un hueco (H1–H7) con referencias nuevas, en su mayoría verificadas en arXiv.

---

## Mapa de huecos

| Hueco | Qué faltaba en el corpus | Qué aporta esta ampliación | Refs nuevas |
| --- | --- | --- | --- |
| H1. Cinemática y dinámica en grupos de Lie | Las bases (PoE, Newton-Euler en $SE(3)$, manipulabilidad, dinámica de Park) solo estaban en libros de pago sin PDF (Murray-Li-Sastry, Lynch-Park, Featherstone). Tampoco había derivadas analíticas de la dinámica ni IK por GPU o aprendida. | Sustitutos abiertos (Mueller 2023, Blanco-Claraco 2021), derivadas de RNEA/ABA, manipulabilidad en la variedad SPD e IK moderna (IKFlow, cuRobo, PyRoki, IK diferencial en tiempo lineal). | 10 (ninguna añadida en esta revisión) |
| H2. Incertidumbre y modelos generativos en grupos de Lie | Tenía densidades en $SO(3)$ para visión (Implicit-PDF, Bingham, Fisher matricial) y libros (Chirikjian, Barfoot). No trataba la propagación de covarianza conjunta, los filtros prácticos en variedades ni la difusión/*flow matching* intrínseca en $SE(3)$. | Gaussiana concentrada y poses conjuntas, UKF-M, IEKF, difusión por *score* en variedades y en $SE(3)$, *flow matching* en grupos de Lie y agarres por MeanFlow. | 11 (+1: Lou et al., 2020, Neural Manifold ODEs) |
| H3. Optimización de trayectorias y control óptimo | CHOMP, TrajOpt y STOMP sin PDF abierto. DDP en grupos de Lie, pero sin MPC por muestreo, planificación por inferencia GP ni control de impedancia geométrico. | MPPI y STORM, MPC con simulación paralela, MPPI como gradiente precondicionado, GPMP, planificación por transporte óptimo y por difusión, impedancia en $SE(3)$ y SVGD en $SE(3)$. | 11 (+1: Anderson et al., 2014, GP en tiempo continuo) |
| H4. *Fine-tuning* geométrico de políticas | TRPO/PPO, K-FAC, LoRA y RLoRA sueltos. Faltaba la geometría del propio ajuste (olvido catastrófico, fusión por Fisher, normas modulares), el RL sobre VLA y la equivarianza a nivel de trayectoria. | EWC, fusión Fisher, MDPO, Muon/SOAP y la vista de "norma correcta", OpenVLA-OFT, SimpleVLA-RL, $\pi_{RL}$, ET-SEED. | 11 (+1: Ryu et al., 2023, Diffusion-EDFs) |
| H5. Calibración cámara-robot y servo visual | $AX=XB$ clásico (Tsai, Park) y servo visual de Chaumette sin PDF. No había calibración certificable, calibración sin marcadores ni servo visual con rasgos fundacionales. | Calibración mano-ojo certificablemente óptima y $AX=YB$ con incertidumbre, calibración sin marcadores (autosupervisada, render diferenciable, Kalib, ARC-Calib), CNS, ViT-VS y control exponencialmente estable en grupos de Lie. | 10 (ninguna añadida) |
| H6. Variedades neuronales | "Neural manifold" solo aparecía como geometría del espacio de parámetros (Fisher, NTK, pullback). No había neurociencia motora ni medidas de dimensión intrínseca, y el bloque de arquitecturas equivariantes del corpus (Vector Neurons, e3nn, SE(3)-Transformers, LieConv) no tenía hueco propio. | Métricas bayesianas y pullback, dimensión intrínseca, variedades neuronales motoras (Gallego et al.), LFADS, CEBRA, BMI estables y acciones latentes. Esta revisión añade el puente teórico neuro/IA, la geometría capa a capa de transformers y dos arquitecturas equivariantes basadas en el álgebra de Lie. | 14 (+4: Chung y Abbott, 2021; Valeriani et al., 2023; Finzi et al., 2021, EMLP; Lin et al., 2023, Lie Neurons) |
| H7. Contexto del proyecto | Pose de instancia (FoundationPose, MegaPose) y objetos transparentes sí estaban, pero no la pose por categoría, el seguimiento, los *benchmarks* de laboratorio científico ni Isaac Lab, el segundo simulador del equipo. | NOCS, 6-PACK, GenPose, DiffusionNOCS, TransNet, manipulación de líquidos transparentes, LabUtopia, ORGANA, ASHE, LAPP y ahora Orbit/Isaac Lab. | 11 (+1: Mittal et al., 2023, Orbit) |

Revisión de calidad: ninguna referencia está repetida entre las bibliografías H1-H7 ni con `corpus.txt` (se compararon identificador arXiv y título normalizado). Los 67 enlaces arXiv que ya tenían las bibliografías (66 filas más uno citado en una nota) y los 8 añadidos se comprobaron contra la API de arXiv. Todos existen y sus títulos y años coinciden.

Los siete huecos forman una cadena. H1 da el modelo del brazo: PoE, Jacobianos y dinámica escritos con $\mathrm{Ad}$ y $\mathrm{ad}$. Es la base formal de las secciones 2-4 de la Parte 1 (grupos de Lie, teoría de tornillos, dinámica riemanniana), que antes solo citaban libros sin PDF. H2 añade la incertidumbre en el tangente y amplía la sección 5 de la Parte 1 (probabilidad en grupos de Lie). La métrica de Fisher de una gaussiana concentrada, $\Sigma^{-1}$, es la misma que usa el gradiente natural del bloque B de la Parte 2. Esa métrica es también la que pondera los residuos de pose en H3 (MPPI, GPMP, impedancia en $SE(3)$, que amplían C.1-C.2 de la Parte 2) y en H4 (el *fine-tuning*, que amplía el bloque D y F.7 de la Parte 2). H3 y H4 comparten el hilo "gradiente precondicionado": MPPI se reinterpreta como descenso precondicionado, y Muon, SOAP, EWC y la fusión por Fisher son elecciones de métrica en el espacio de parámetros.

H5 y H7 conectan esa cadena con la Parte 3. H5 amplía las secciones 1.5-1.6 (calibración mano-ojo) y 3 (servo visual): sin una ${}^{b}T_{c}$ bien calibrada y con covarianza, la pose del objeto de la sección 2 no llega bien a la pinza, y la ley de control de la sección 3.4 en el álgebra de Lie tiene ahora una garantía de estabilidad exponencial. H7 cubre lo que la sección 2 de la Parte 3 dejaba fuera: la pose por categoría para frascos y viales sin CAD exacto, el seguimiento y los *benchmarks* de laboratorio (LabUtopia, ORGANA) que sitúan el proyecto junto a AutoBio. Con Orbit, además, la hoja de ruta de la sección 8 puede apoyarse tanto en MuJoCo como en Isaac Lab. La ambigüedad por simetría de esos recipientes vuelve a H2: la difusión en $SE(3)$ devuelve el anillo de poses equivalentes en vez de promediarlas.

H6 envuelve el resto. Amplía la sección 7 de la Parte 1, el bloque E de la Parte 2 y la sección 7 de la Parte 3, que trataban las "variedades neuronales" solo como geometría de parámetros y de latentes. Ahora se añaden la lectura neurocientífica (dinámica de población motora de baja dimensión, estable en el tiempo) y medidas cuantitativas (dimensión intrínseca por capa) para decidir qué rasgos visuales alimentan la política. Queda un hueco residual: las arquitecturas equivariantes (sección 5 de la Parte 3, C.6 de la Parte 2) no tienen una sección de ampliación propia. Por eso EMLP y Lie Neurons se han colocado provisionalmente en H6. Una siguiente pasada podría dedicarles un hueco H8 sobre redes equivariantes al álgebra de Lie para procesar twists y poses.

---

## H1. Cinemática y dinámica de brazos en grupos de Lie: fuentes abiertas que sustituyen a los libros de texto

### Intuición

Las secciones 3 y 4 de la Parte 1 ya exponen el producto de exponenciales (PoE), los Jacobianos espacial y del cuerpo, la manipulabilidad y el Newton–Euler geométrico. Pero todo ese material se apoya en libros y artículos clásicos sin PDF abierto (Brockett, 1984; Murray et al., 1994; Park et al., 1995; Featherstone, 2008; Lynch y Park, 2017; Yoshikawa, 1985) y en herramientas citadas solo como repositorios (mink). Por eso el corpus no puede extraer de ellos afirmaciones verificables. Este hueco se cubre con fuentes abiertas que dicen lo mismo con la misma notación y que llegan hasta el software que realmente se usará en la escena AutoBio:

1. **Tutoriales de referencia** sobre tornillos, PoE, representaciones de giros y parametrizaciones de $SE(3)$ (Mueller, 2023a; Blanco-Claraco, 2021).
2. **Dinámica recursiva en grupos de Lie y sus derivadas analíticas**, que es lo que necesitan DDP, MPC y el ajuste por gradiente (Mueller, 2023b; Carpentier y Mansard, 2018; Singh et al., 2021).
3. **Manipulabilidad como objeto geométrico**: el elipsoide de Yoshikawa es una matriz SPD, así que se aprende y se sigue sobre la variedad SPD (Jaquier et al., 2018).
4. **IK moderna**: diferencial/QP en tiempo lineal (Wingo et al., 2024), aprendida con flujos normalizantes (Ames et al., 2021) y masivamente paralela en GPU (Sundaralingam et al., 2023; Kim et al., 2025).

La idea que une todo: la cinemática directa $f:\mathcal{C}\to SE(3)$ es una aplicación suave entre variedades. La IK, la manipulabilidad y la dinámica son su diferencial ($J$), la imagen de la bola unidad por esa diferencial ($JJ^\top$) y el *pullback* de las métricas inerciales ($M=\sum J_i^\top\mathcal{G}_iJ_i$). Todo se calcula en el espacio tangente con $\mathrm{Ad}$ y $\mathrm{ad}$.

### Formalismo

**Representaciones de giros.** Mueller (2023a) distingue cuatro formas de expresar la velocidad de un cuerpo con el mismo par $(\omega,v)$: *body-fixed* $\mathcal{V}_b$, *spatial* $\mathcal{V}_s$, *hybrid* (velocidad lineal del origen del cuerpo y angular, ambas en el marco mundo) y *mixed* (angular en el cuerpo y lineal en el mundo). Se relacionan mediante la adjunta:
$$
\mathcal{V}_s=\mathrm{Ad}_T\,\mathcal{V}_b,\qquad
\mathcal{V}_h=\begin{pmatrix}R&0\\0&R\end{pmatrix}\mathcal{V}_b,\qquad
\mathrm{Ad}_T=\begin{pmatrix}R&0\\ [t]_\times R&R\end{pmatrix}.
$$
Aquí se mantiene la convención de la Parte 1, rotación primero. Esto aclara la nota de la Parte 2 sobre `mj_jacSite`: MuJoCo devuelve el Jacobiano **híbrido** (punto del *site*, ejes del mundo), y al rotarlo con $R^\top$ se obtiene el del cuerpo.

**PoE y recursión.** Con ejes de tornillo $\mathcal{S}_i$ en la configuración de referencia, $T(q)=e^{[\mathcal{S}_1]q_1}\cdots e^{[\mathcal{S}_n]q_n}M$. Mueller (2023a) muestra que esta forma y la de Denavit–Hartenberg son casos particulares de una misma recursión en árbol. De ella salen el Jacobiano geométrico y sus derivadas temporales en forma cerrada. Por ejemplo, $\dot J_{s,i}=\sum_{j<i}\mathrm{ad}_{J_{s,j}\dot q_j}J_{s,i}$, y de ahí se obtienen $\ddot T$ y los términos de aceleración sin diferenciar numéricamente.

**Parametrizaciones de $SE(3)$ y optimización en la variedad.** Blanco-Claraco (2021) es el tutorial autocontenido que falta junto a Solà et al. (2018). Compara ángulos de Euler, cuaterniones y matrices $3\times4$, y da los Jacobianos de composición, inversión, $\mathrm{Exp}$ y $\mathrm{Log}$. También da el esquema de Gauss–Newton/LM sobre $SE(3)$: $T\leftarrow T\oplus\delta$ con $\delta=-(J^\top J+\lambda I)^{-1}J^\top r$.

**Dinámica y derivadas.** La dinámica inversa $\tau=\mathrm{ID}(q,\dot q,\ddot q)$ (RNEA) y la directa $\ddot q=\mathrm{FD}(q,\dot q,\tau)=M^{-1}(\tau-b)$ (ABA) tienen formulación recursiva $O(n)$ con $\mathrm{Ad}/\mathrm{ad}$ (Mueller, 2023b). Carpentier y Mansard (2018) derivan analíticamente ambas. La observación central es que las derivadas de la directa se obtienen de las de la inversa:
$$
\frac{\partial\,\mathrm{FD}}{\partial q}=-M^{-1}\frac{\partial\,\mathrm{ID}}{\partial q}\Big|_{\ddot q=\mathrm{FD}},\qquad
\frac{\partial\,\mathrm{FD}}{\partial \dot q}=-M^{-1}\frac{\partial\,\mathrm{ID}}{\partial \dot q},\qquad
\frac{\partial\,\mathrm{FD}}{\partial \tau}=M^{-1}.
$$
Singh et al. (2021) dan expresiones cerradas en álgebra de vectores espaciales para $\partial\mathrm{ID}/\partial q$ y $\partial\mathrm{ID}/\partial\dot q$, válidas para juntas multi-GDL que son grupos de Lie (esféricas y base flotante). Para esas juntas, la derivada respecto a $q$ se toma en el tangente del grupo y no en coordenadas.

**Manipulabilidad en la variedad SPD.** El elipsoide de velocidad es $\mathbf{M}(q)=J(q)J(q)^\top\in\mathcal{S}^6_{++}$. Jaquier et al. (2018) lo tratan como punto de la variedad SPD con métrica afín-invariante, $d(\mathbf{A},\mathbf{B})=\lVert\log(\mathbf{A}^{-1/2}\mathbf{B}\mathbf{A}^{-1/2})\rVert_F$. Aprenden secuencias de elipsoides con un GMM tensorial en el tangente (vía $\mathrm{Log}_{\mathbf{A}}$) y los siguen con una ley de control que usa el **Jacobiano de manipulabilidad**, el tensor $\partial\mathbf{M}/\partial q$:
$$
\dot q = \mathcal{J}_{\mathbf{M}}^{\dagger}\,K_{\mathbf{M}}\,\mathrm{vec}\!\big(\mathrm{Log}_{\mathbf{M}}(\hat{\mathbf{M}})\big)+\big(I-\mathcal{J}_{\mathbf{M}}^{\dagger}\mathcal{J}_{\mathbf{M}}\big)\dot q_0 .
$$
Es exactamente el patrón de la Parte 1 (error en el tangente, Jacobiano, pseudoinversa), aplicado a otro grupo o variedad.

### Métodos clave

| Método | Qué aporta | Estado para el proyecto |
|---|---|---|
| Tutoriales de Mueller (2023a, 2023b) | Versión abierta y rigurosa de Murray et al. (1994), Lynch y Park (2017) y Park et al. (1995): PoE, cuatro representaciones de giros, Newton–Euler $O(n)$ y ecuaciones de movimiento en forma cerrada | Lectura de referencia para derivar $J$ y $\dot J$ |
| Blanco-Claraco (2021) | Jacobianos de $SE(3)$ listos para copiar; complementa a Solà et al. (2018) | Base de la IK por LM de la Parte 2 |
| Pinocchio: derivadas analíticas (Carpentier y Mansard, 2018; Singh et al., 2021) | $\partial\mathrm{FD}$ y $\partial\mathrm{ID}$ exactas y $O(n)$, mucho más baratas que las diferencias finitas | Necesarias para DDP en grupos de Lie (Boutselis et al., 2018; Alcan et al., 2023) |
| Manipulabilidad SPD (Jaquier et al., 2018) | Transferencia de "postura diestra" desde demostraciones | Coste secundario en el espacio nulo |
| IKFlow (Ames et al., 2021) | Flujo normalizante condicionado a la pose que muestrea miles de soluciones IK diversas en milisegundos | Semillas para IK local y multimodalidad |
| cuRobo (Sundaralingam et al., 2023) | IK y trayectorias libres de colisión, de mínimo *jerk*, con miles de semillas paralelas en GPU | Referencia de GPU; requiere GPU NVIDIA (CUDA) |
| PyRoki (Kim et al., 2025) | IK, trayectorias y *retargeting* modulares en JAX (CPU/GPU/TPU); más rápido que cuRobo en IK según sus autores | Encaja con `jaxlie` del corpus |
| IK diferencial por Lagrangiano aumentado (Wingo et al., 2024) | Resuelve la misma clase de problemas que la IK diferencial por QP (restricciones de igualdad y límites) con coste lineal en el número de juntas, recursión al estilo de Featherstone y ADMM al estilo OSQP | Alternativa rigurosa y documentada a mink en la capa reactiva |

Hay dos ejes de comparación. **Local contra global**: la IK diferencial/QP (Buss, 2004; mink; Wingo et al., 2024) es local y reactiva: en cada paso resuelve $\min_{\dot q}\tfrac12\lVert J\dot q-\mathcal{V}^\star\rVert_W^2+\tfrac{\lambda}{2}\lVert\dot q\rVert^2$ con límites articulares, y Wingo et al. (2024) muestran que su estructura de árbol permite resolverla en $O(n)$ y no en $O(n^3)$. IKFlow, cuRobo y PyRoki, en cambio, buscan muchas soluciones a la vez. **Aprendido contra optimizado**: IKFlow aprende una densidad sobre la fibra $f^{-1}(T)$ (una subvariedad de dimensión $n-6$ en brazos redundantes), mientras que cuRobo y PyRoki optimizan desde semillas paralelas. IKFlow conecta con el hilo de flujos del corpus (Chen y Lipman, 2023; Braun et al., 2024): es otro modelo generativo, pero su soporte es la variedad de soluciones de la IK.

### Por qué importa para el brazo y el proyecto

1. **Trazabilidad de afirmaciones.** Hoy el corpus afirma que PoE no tiene singularidades de parametrización y que el RNEA geométrico es $O(n)$, pero no lo respalda ningún PDF procesable. Mueller (2023a, 2023b) y Blanco-Claraco (2021) sustituyen a esos libros como fuente citable.
2. **Frontera con MuJoCo.** Los Jacobianos de MuJoCo (`mj_jacSite`, `mj_jacBody`) son híbridos. Confundirlos con los del cuerpo es un error silencioso en la IK de la Parte 2 y en el servo visual de la Parte 3, que usa la matriz de interacción por $J_b$. La taxonomía de Mueller (2023a) da la conversión exacta con $\mathrm{Ad}$.
3. **Ajuste fino por gradiente.** Para optimizar trayectorias o políticas con gradiente natural (la métrica $M(q)$ como precondicionador) hacen falta $\partial\mathrm{FD}/\partial(q,\dot q,\tau)$. Las fórmulas de Carpentier y Mansard (2018) y Singh et al. (2021) son las que usan Pinocchio y los DDP en grupos de Lie del corpus (Boutselis et al., 2018; Alcan et al., 2023; Teng et al., 2022). MuJoCo solo ofrece diferencias finitas (`mjd_transitionFD`), que valen como verificación pero no escalan.
4. **Tareas de laboratorio.** Pesar en la balanza analítica y verter desde frascos de reactivos exige posturas con buena manipulabilidad en la dirección vertical y en la de giro de la muñeca. Aprender el elipsoide de demostraciones (Jaquier et al., 2018) y seguirlo en el espacio nulo sigue el mismo marco riemanniano de Jaquier et al. (2022) y Calinon (2020) que ya está en el corpus.
5. **Visión → IK.** El estimador de pose (FoundationPose, MegaPose) entrega $T^\star\in SE(3)$ con incertidumbre. Una IK generativa (IKFlow) o paralela (PyRoki, cuRobo) da muchas configuraciones candidatas, entre las que se elige por manipulabilidad o colisión con la escena. Con la IK DLS de la Parte 2 se obtiene una sola.

**Qué no se encontró.** Los libros de Lynch y Park (2017) y de Murray et al. (1994) tienen PDF gratuito del autor pero no versión en arXiv. El artículo de Pinocchio (SII 2019), el de derivadas (RSS 2018) y el de IK diferencial en tiempo lineal (RSS 2024) solo están en HAL o en las actas, así que los dos últimos se incluyen como referencias sin arXiv. No hay artículo de mink: sigue siendo solo software. Como trabajo reciente de IK por lotes en GPU queda fuera HJCD-IK (Yasutake et al., 2025, arXiv:2510.07514).

---

## H2. Incertidumbre, probabilidad y modelos generativos en grupos de Lie

### Intuición

El corpus ya trata la pose como un elemento de $SE(3)$ y sabe linealizar en el tangente (Sola et al., 2018), pero casi siempre estima **un punto**. En un laboratorio eso no basta. Un frasco ámbar visto a contraluz, un tapón con simetría de revolución o la cubierta de vidrio de la balanza analítica producen poses ambiguas, y la ambigüedad se propaga por la cadena cámara → objeto → pinza. Hay dos preguntas que el corpus solo cubre con libros de referencia (Chirikjian, vols. 1-2; Barfoot, 2017; Wang y Chirikjian, 2008) o con densidades de $SO(3)$ para visión (Mohlin et al., 2020; Deng et al., 2022; Murphy et al., 2021):

1. **¿Cómo se representa y propaga la incertidumbre de una pose?** La respuesta moderna es la *gaussiana concentrada*: ruido gaussiano en el álgebra de Lie, llevado al grupo con $\mathrm{Exp}$. De ahí salen los filtros (EKF invariante, UKF en variedades) y la composición de poses con covarianza conjunta.
2. **¿Cómo se generan muestras de una distribución complicada sobre $SE(3)$?** Esto es lo que necesitan un generador de agarres o una política de acciones. La respuesta actual son los modelos de difusión y de *flow matching* definidos intrínsecamente en la variedad. El ruido es un movimiento browniano en el grupo, y la "dirección de denoising" (la *score*) es un vector del tangente.

Las dos preguntas usan la misma herramienta: **una densidad en el grupo se describe con objetos del espacio tangente**. La covarianza $\Sigma$ vive en $\mathfrak{se}(3)$ y la *score* $\nabla\log p$ también.

### Formalismo

**Gaussiana concentrada.** Una pose aleatoria $T\in SE(3)$ con media $\bar T$ se modela como

$$
T=\mathrm{Exp}(\xi)\,\bar T,\qquad \xi\sim\mathcal{N}(0,\Sigma),\ \Sigma\in\mathbb{R}^{6\times6},
$$

que es válida mientras $\Sigma$ sea pequeña frente al radio de inyectividad de $\mathrm{Exp}$. Para componer dos poses independientes, $T_1T_2$, a primer orden

$$
\Sigma_{12}\approx \Sigma_1+\mathrm{Ad}_{\bar T_1}\,\Sigma_2\,\mathrm{Ad}_{\bar T_1}^{\top},
$$

y Barfoot añade términos de cuarto orden cuando la incertidumbre crece. Mangelson et al. (2019) generalizan este cálculo a poses **correlacionadas**: definen la versión en el álgebra de Lie de las operaciones clásicas de Smith-Self-Cheeseman (composición cabeza-cola, inversa y cola-cola) con una covarianza conjunta $\Sigma_{12}\neq 0$. Muestran que caracterizar la incertidumbre en el álgebra de $SE(3)$ da mejores estimaciones que hacerlo en coordenadas de Euler, y publican una biblioteca en C++. Es justo el caso cámara-muñeca-objeto, donde las poses comparten errores de calibración.

**Filtros en el grupo.** El UKF en variedades (Brossard et al., 2020) solo necesita una retracción $\varphi(\chi,\xi)$ y su inversa $\varphi^{-1}_{\chi}$. Los *sigma points* se generan en el tangente, $\chi_i=\varphi(\hat\chi,\ \pm\sqrt{(d+\lambda)\Sigma}\,e_i)$, se propagan por la dinámica no lineal, y la nueva media y la covarianza se reconstruyen con $\varphi^{-1}$. No hay Jacobianos, y la misma plantilla sirve para $SO(3)$, $SE(3)$ o $SE_2(3)$. Las extensiones del EKF invariante que van más allá de Barrau y Bonnabel (2017) explotan la propiedad *group-affine*. Hartley et al. (2019) incluyen en el estado del grupo matricial $SE_{K+2}(3)$ la posición de los contactos y usan la cinemática directa como medida, de modo que la matriz de error linealizada no depende de la estimación. Yaqubi y Mattila (2026) llevan la idea a los **brazos seriales**: un IEKF por eslabón en $SE(3)$ fusiona acelerómetro, giróscopo y encoders, con coste lineal en el número de eslabones y acotación exponencial en media cuadrática demostrada con Lyapunov.

**Difusión en variedades.** El proceso directo es un movimiento browniano en la variedad $\mathcal{M}$, $\mathrm{d}X_t=\mathrm{d}B_t^{\mathcal{M}}$, y el proceso inverso es

$$
\mathrm{d}Y_t=\nabla_{\!\mathcal{M}}\log p_{T-t}(Y_t)\,\mathrm{d}t+\mathrm{d}B_t^{\mathcal{M}},
$$

donde la *score* riemanniana se aprende con *denoising score matching* sobre el núcleo de calor. De Bortoli et al. (2022) formalizan esto para variedades compactas: aproximan el núcleo por expansión en autofunciones o por Varadhan y muestrean con *geodesic random walks*. Huang et al. (2022) dan el marco variacional equivalente, con una cota ELBO en tiempo continuo para difusiones riemannianas, y demuestran que maximizarla equivale a hacer *score matching*. En $SO(3)$ el núcleo de calor es la distribución **IGSO(3)**. Su densidad sobre el ángulo $\omega$ de rotación es

$$
f_\varepsilon(\omega)=\sum_{l\ge0}(2l+1)\,e^{-l(l+1)\varepsilon/2}\,\frac{\sin\!\big((l+\tfrac12)\omega\big)}{\sin(\omega/2)}.
$$

Yim et al. (2023) la combinan con un browniano en $\mathbb{R}^3$ para difundir en $SE(3)=SO(3)\ltimes\mathbb{R}^3$ (tratado como $SO(3)\times\mathbb{R}^3$ en la difusión). Su *score* en $SO(3)$ tiene forma cerrada y es un vector del álgebra $\mathfrak{so}(3)$.

**Flow matching en grupos.** Sherry y Smets (2025) sustituyen las rectas del *flow matching* euclídeo (Chen y Lipman, 2023) por **curvas exponenciales**:

$$
g_t=g_0\,\mathrm{Exp}\!\big(t\,\mathrm{Log}(g_0^{-1}g_1)\big),\qquad u_t=\tfrac{\mathrm{d}}{\mathrm{d}t}g_t .
$$

El entrenamiento no necesita simular el proceso y funciona para cualquier grupo con exponencial sobreyectiva.

### Métodos clave

- **Mangelson et al. (2019).** Poses con distribución conjunta en $\mathfrak{se}(3)$; son las operaciones de Smith-Self-Cheeseman hechas en el álgebra.
- **Brossard et al. (2020), UKF-M.** UKF genérico en variedades mediante retracciones, con código Python/Matlab listo para usar.
- **Hartley et al. (2019).** IEKF con contacto y cinemática directa sobre $SE_{K+2}(3)$; es la plantilla de "cinemática como medida en el grupo".
- **Yaqubi y Mattila (2026).** IEKF en $SE(3)$ por eslabón para manipuladores seriales con inerciales y encoders.
- **De Bortoli et al. (2022)** y **Huang et al. (2022).** Los dos pilares teóricos de la difusión riemanniana (*score* y variacional).
- **Yim et al. (2023), FrameDiff.** Difusión en $SE(3)^N$ con IGSO(3). Aunque su aplicación es de proteínas, es la receta de referencia para difundir poses rígidas.
- **Hsiao et al. (2023).** Difusión basada en *score* en $SE(3)$ para estimación de pose 6D **ambigua** (objetos simétricos), con una *score* sustituta en el álgebra de Lie. Es el puente directo con la sección 2.4 del documento 03.
- **Sherry y Smets (2025).** *Flow matching* intrínseco en grupos de Lie.
- **Bukhari et al. (2026).** *MeanFlow* en $SO(3)\times\mathbb{R}^3$ para generar agarres con $\le 5$ evaluaciones de red, hasta 39× más rápido que las difusiones de agarre y sin ajuste extra en el robot real.

Estos trabajos completan lo que ya hay en el corpus. SE(3)-DiffusionFields (Urain et al., 2022) y EquiGraspFlow (Lim et al., 2024) usan difusión y flujos sobre $SE(3)$ para agarres. Riemannian Flow Matching Policy (Braun et al., 2024) y Diffusion Policy (Chi et al., 2023) generan acciones. Faltaba la teoría que los justifica (núcleo de calor, *score* riemanniana, curvas exponenciales) y su versión rápida de pocos pasos. En estimación, Barrau y Bonnabel (2017) y Forster et al. (2016) quedan conectados con UKF-M y con un IEKF específico para brazos.

Una pieza anterior a la difusión en variedades completa esta lista. Neural Manifold ODEs (Lou et al., 2020) define flujos continuos por cartas locales y obtiene densidades exactas en $S^2$, $SO(3)$ y espacios hiperbólicos. Es el antecedente directo de Riemannian Flow Matching y de los flujos en grupos de Lie citados arriba, y sirve para modelar la verosimilitud de una pose cuando se necesita un valor de densidad (por ejemplo, para rechazar agarres improbables) y no solo muestras.

### Por qué importa para el brazo y el proyecto

1. **Incertidumbre de percepción → agarre.** El estimador de pose (FoundationPose, MegaPose) da $\bar T_{co}$. Con Mangelson et al. se puede propagar $\Sigma$ por ${}^{w}T_{c}\,{}^{c}T_{o}\,{}^{o}T_{g}$ teniendo en cuenta la correlación con la calibración mano-ojo. Si la elipse de incertidumbre de la pinza es mayor que la holgura del cuello del frasco, el robot debe mirar de nuevo antes de agarrar.
2. **Ambigüedad por simetría.** Los frascos de reactivo y los tapones son casi simétricos por revolución. Una difusión en $SE(3)$ como la de Hsiao et al. devuelve **muestras** que cubren el anillo de poses equivalentes, en lugar de promediarlas en una pose imposible. Esto complementa Implicit-PDF (Murphy et al., 2021), que es una densidad en rejilla solo sobre $SO(3)$.
3. **Generación de agarres y acciones.** Un generador de agarres por *flow matching* en $SO(3)\times\mathbb{R}^3$ (Sherry y Smets, 2025; Bukhari et al., 2026) entrenado con datos renderizados en MuJoCo evita representaciones discontinuas (Zhou et al., 2019). Sus pocos pasos permiten replanificar en bucle cerrado. En la política, difundir el efector final en $SE(3)$ con ruido IGSO(3), y no en ángulos de Euler, es la misma idea aplicada a las acciones.
4. **Estado del brazo.** En simulación el estado es exacto, pero para *sim-to-real* se pueden añadir sensores `gyro`/`accelerometer` en MuJoCo y probar UKF-M o el IEKF por eslabón de Yaqubi y Mattila como filtro de pose del efector, con la cámara de muñeca como medida.
5. **Conexión con el gradiente natural.** Una gaussiana concentrada tiene métrica de Fisher $\Sigma^{-1}$ en el tangente. Es la métrica natural para ponderar residuos de pose en el *fine-tuning* de la parte 2.

---

## H3. Optimización de trayectorias y control óptimo para brazos: MPPI, planificación por difusión y control geométrico en $SE(3)$

### Intuición

El corpus ya describe la tríada clásica de optimización de trayectorias —CHOMP (Zucker et al., 2013), TrajOpt (Schulman et al., 2014) y STOMP (Kalakrishnan et al., 2011)—, pero sólo como citas sin PDF, y cubre bien el lado de segundo orden en grupos de Lie (DDP de Boutselis & Theodorou, 2018; DDP lie-algebraico de Alcan et al., 2023; MPC de estado de error y coste en el álgebra de Teng et al., 2022) y la capa reactiva (RMP de Ratliff et al., 2018; RMPflow de Cheng et al., 2018; *geometric fabrics* de Van Wyk et al., 2021). Falta el eslabón intermedio que hoy domina en la práctica: **optimizadores por muestreo masivamente paralelos** (MPPI y variantes) que usan la GPU o el propio simulador como modelo, **priors generativos de trayectorias** (difusión) que sustituyen la inicialización aleatoria, y **control de impedancia geométrico en $SE(3)$** que ejecuta el resultado con seguridad cuando hay contacto (la balanza analítica, el tapón de un frasco).

La idea unificadora es sencilla: toda actualización de trayectoria es un paso de descenso **medido con una métrica**. CHOMP la escribe explícitamente ($A^{-1}\nabla\mathcal U$); STOMP y MPPI la esconden en la covarianza del ruido de muestreo; y un resultado de 2026 demuestra que el paso de MPPI es, literalmente, un gradiente precondicionado. Ese es el puente con el gradiente natural de Amari (1998) y Martens (2014) que ya ocupa la Parte 2.

### Formalismo

**Gradiente covariante (CHOMP).** Sea $\xi\in\mathbb R^{N\times n}$ una trayectoria discretizada y $\mathcal U(\xi)=\mathcal F_{\text{obs}}(\xi)+\tfrac{\lambda}{2}\,\xi^\top A\,\xi$, con $A=K^\top K$ la matriz de diferencias finitas. El paso de CHOMP resuelve
$$
\xi_{k+1}=\arg\min_{\xi}\;\mathcal U(\xi_k)+\nabla\mathcal U(\xi_k)^\top(\xi-\xi_k)+\tfrac{1}{2\eta}\lVert\xi-\xi_k\rVert_A^2
\;\Longrightarrow\;
\xi_{k+1}=\xi_k-\eta\,A^{-1}\nabla\mathcal U(\xi_k).
$$
Es exactamente la forma del gradiente natural $\theta\leftarrow\theta-\eta F^{-1}\nabla L$ con la métrica de Fisher $F$ sustituida por la métrica de suavidad $A$: el paso es invariante a reparametrizaciones lineales de la trayectoria y reparte la corrección de un waypoint en colisión por toda la curva.

**La dualidad muestreo–métrica (STOMP → MPPI).** STOMP perturba con $\epsilon\sim\mathcal N(0,R^{-1})$, es decir, **muestrea con la inversa de la misma métrica**. Williams et al. (2017) formalizan esto: para controles $u=v+\epsilon$ con $\epsilon\sim\mathcal N(0,\Sigma)$ y coste de trayectoria $S(\tau)$, el control óptimo minimiza la energía libre $\mathcal F=-\lambda\log\mathbb E_{p}\big[e^{-S/\lambda}\big]$, cuya distribución óptima es la distribución de Gibbs $q^\star(\tau)\propto p(\tau)\,e^{-S(\tau)/\lambda}$. Proyectando $q^\star$ sobre la familia gaussiana (minimizando $\mathrm{KL}(q^\star\Vert q_v)$) resulta la regla de MPPI:
$$
v_t\leftarrow v_t+\sum_{k=1}^{K} w_k\,\epsilon_t^{(k)},\qquad
w_k=\frac{\exp\!\big(-S(\tau_k)/\lambda\big)}{\sum_j\exp\!\big(-S(\tau_j)/\lambda\big)} .
$$

**MPPI como gradiente precondicionado.** Fazlyab et al. (2026) elevan el problema restringido a uno regularizado con KL sobre distribuciones de decisión y obtienen un objetivo reducido de energía libre $J(\theta)$ sobre la familia de muestreo $q_\theta$. Para gaussianas de covarianza fija $\Sigma$ demuestran que la actualización clásica de MPPI **se recupera exactamente** como un paso unitario de gradiente precondicionado (con $J$ normalizado adecuadamente por la temperatura $\lambda$),
$$
v\leftarrow v-\Sigma\,\nabla_v J(v),
$$
y que la convergencia depende de la covarianza de la distribución inclinada por Gibbs relativa a $\Sigma$. Leído con la Parte 2: $\Sigma$ desempeña el papel de $F^{-1}$; elegir $\Sigma=R^{-1}$ (STOMP) o $\Sigma=A^{-1}$ (CHOMP) es elegir la métrica. La cadena CHOMP → STOMP → MPPI → gradiente natural queda así cerrada formalmente.

**Versión en grupos de Lie.** Cuando la variable es una pose $X_t\in SE(3)$ el ruido se inyecta en el álgebra, $X_t^{(k)}=\bar X_t\,\mathrm{Exp}(\epsilon_t^{(k)})$, y la media ponderada se hace en el tangente, $\bar X_t\leftarrow\bar X_t\,\mathrm{Exp}\big(\sum_k w_k\,\mathrm{Log}(\bar X_t^{-1}X_t^{(k)})\big)$, con el convenio de perturbación derecha de Solà et al. (2018). Li et al. (2026) llevan esta receta a *Stein variational gradient descent* con partículas en $SE(3)$ y un precondicionador explícito, que es el análogo en variedad de la matriz $\Sigma$ anterior.

**Control geométrico de impedancia.** Seo et al. (2022) definen el error de pose mediante una función potencial invariante a izquierda sobre $SE(3)$, $\Psi(g,g_d)$, derivan de ella los vectores de error de posición y velocidad y construyen la ley
$$
\tau = J_b^\top(q)\Big(-K_d\,e_V-\nabla\Psi(g,g_d)\Big)+\text{compensación dinámica},
$$
donde $e_V$ es el error de *twist* en el marco del cuerpo. El gradiente del potencial vuelve a ser la parte lineal de $\mathrm{Log}(g_d^{-1}g)$, como en el coste lie-algebraico de Teng et al. (2022).

### Métodos clave

- **MPPI / IT-MPC (Williams et al., 2017).** Derivación informacional (energía libre + KL) del control por integral de camino; no requiere gradientes del modelo ni del coste, así que admite costes discontinuos (colisión binaria, "el frasco se vuelca").
- **STORM (Bhardwaj et al., 2021).** MPC por muestreo en **espacio articular** para brazos en tiempo real en GPU, con costes de colisión aprendidos, límites articulares y manipulabilidad; muestra que no hace falta un controlador operacional por debajo.
- **MPPI con simulador físico paralelo (Pezzato et al., 2023).** Usa el propio simulador (IsaacGym) como modelo dinámico de los *rollouts*, lo que permite manipulación no prensil y tareas con contacto sin escribir un modelo analítico; la receta es directamente trasladable a MuJoCo/MJX.
- **GPMP2 (Mukadam et al., 2017).** Planificación como inferencia: prior de proceso gaussiano sobre trayectorias continuas y factores de colisión, resuelto como mínimos cuadrados dispersos en un grafo de factores. El prior GP induce la métrica de suavidad y enlaza con la maquinaria de Gauss–Newton de Theseus (Pineda et al., 2022).
- **MPOT (Le et al., 2023).** El *Sinkhorn Step*: actualización de orden cero, altamente paralela, que optimiza lotes de trayectorias suaves mediante transporte óptimo sobre direcciones de un politopo regular, manteniendo el prior GP de GPMP2.
- **Motion Planning Diffusion (Carvalho et al., 2023).** Aprende un modelo de difusión como prior de trayectorias y muestrea directamente la posterior añadiendo el gradiente de los costes de tarea durante el *denoising*; es la contrapartida "planificador" de Diffusion Policy (Chi et al., 2023) y de SE(3)-DiffusionFields (Urain et al., 2022).
- **DiffusionSeeder (Huang et al., 2024).** Difusión condicionada a una **imagen de profundidad** que genera semillas multimodales refinadas después con unas pocas iteraciones de cuRobo; reporta aceleraciones de ~12× (36× en escenas difíciles) y +10 % de éxito en escenas parcialmente observadas. Es el vínculo directo visión → optimizador.
- **Geometric Impedance Control (Seo et al., 2022).** Impedancia en $SE(3)$ con potencial invariante a izquierda y garantías de estabilidad, sin parametrizaciones de Euler.
- **Stein variational en $SE(3)$ (Li et al., 2026).** SVGD precondicionado con actualizaciones de partículas en $SE(3)$ para cobertura ergódica de superficies; ejemplo reciente de optimización por muestreo nativa en el grupo.
- **MPPI como gradiente precondicionado (Fazlyab et al., 2026).** Análisis de convergencia que convierte a MPPI en un método de primer orden precondicionado, dando el puente formal con el gradiente natural.

El prior de trayectoria de GPMP no sale de la nada. Anderson et al. (2014) muestran que un GP en tiempo continuo generado por una SDE lineal tiene inversa de covarianza tridiagonal por bloques, y por eso la estimación y la planificación por inferencia cuestan $O(K)$ en el número de nodos. La misma construcción se extiende a $SE(3)$ con perturbaciones en el tangente, lo que permite planificar trayectorias del efector final con coste de suavidad definido en $\mathfrak{se}(3)$.

### Por qué importa para el brazo y el proyecto

1. **MuJoCo como modelo de MPC.** Siguiendo a Pezzato et al. (2023) y STORM, un MPPI con $K$ *rollouts* paralelos en MJX / MuJoCo Playground (Zakka et al., 2025) puede planificar sobre la escena de AutoBio (Lan et al., 2025) —frascos de reactivo, balanza, fregadero— sin derivar un modelo: el simulador *es* el modelo, y los costes pueden ser no diferenciables (vuelco, derrame, contacto con el plato de la balanza).
2. **La métrica como hiperparámetro principal.** Por Fazlyab et al. (2026), la covarianza de muestreo $\Sigma$ es un precondicionador: escogerla como $A^{-1}$ (suavidad, CHOMP) o como la inversa de la inercia articular $M(q)^{-1}$ (la métrica cinética de la Parte 1) da pasos coherentes con la geometría del brazo, igual que el gradiente natural lo hace en el espacio de parámetros.
3. **Visión → semilla → optimizador → impedancia.** El pipeline de visión (pose 6D con FoundationPose, Wen et al., 2023; nube de profundidad) alimenta un prior generativo (Motion Planning Diffusion o DiffusionSeeder) que propone trayectorias multimodales; MPPI/cuRobo/GPMP2 las refina contra colisiones; y un controlador de impedancia en $SE(3)$ (Seo et al., 2022) las ejecuta con contacto suave, por encima de RMPflow como capa reactiva.
4. **Coherencia con el ajuste fino de políticas.** Los mismos pesos de Gibbs $e^{-S/\lambda}$ aparecen en el ajuste por RL de políticas de difusión (DPPO, Ren et al., 2024; ReinFlow, Zhang et al., 2025): una trayectoria refinada por MPPI puede usarse como demostración o como objetivo de destilación para la política aprendida.
5. **Poses del efector en el grupo.** Con muestreo en $\mathfrak{se}(3)$ y retracción $\mathrm{Exp}$ se evitan los promedios ingenuos de cuaterniones o ángulos de Euler, en línea con Solà et al. (2018) y con el DDP en grupos de Lie ya incluido en el corpus.

---

## H4. Fine-tuning geométrico de políticas robóticas: ¿en qué geometría viven las actualizaciones?

### Intuición

El corpus ya cubre las dos puntas del problema: por un lado, la teoría del paso "natural" (Amari 1998; Kakade 2001; Martens 2014; Martens & Grosse 2015) y sus versiones de región de confianza (TRPO, PPO, ACKTR); por otro, los modelos que queremos ajustar (OpenVLA, π0, π0.5, Octo, RDT-1B) y los métodos de RL para políticas generativas (DPPO, ReinFlow), más LoRA y su precondicionador riemanniano (Hu et al., 2021; Zhang & Pilanci, 2024). Lo que falta es la pregunta que une ambas puntas: **cuando hacemos fine-tuning de una política preentrenada, ¿con qué norma o métrica medimos el tamaño de cada paso, y respecto a qué punto de referencia?**

Hay tres respuestas distintas, y cada una corresponde a un espacio diferente:

1. **Espacio de parámetros con métrica de Fisher anclada al modelo base.** El paso no debe alejarse del preentrenamiento en las direcciones que el modelo base considera importantes. Es la idea de EWC (Kirkpatrick et al., 2016) y de la fusión ponderada por Fisher (Matena & Raffel, 2021).
2. **Espacio de políticas con divergencia de Bregman (KL).** El paso se mide en la distribución de acciones, no en los pesos. Es el descenso espejo de políticas (Tomar et al., 2020), del que TRPO/PPO son aproximaciones.
3. **Espacio de pesos por capas con normas de operador.** Cada matriz de pesos es un operador lineal, y su tamaño natural es la norma espectral, no la euclídea. Es la lectura de Adam, Shampoo, SOAP y Muon como descenso más pronunciado bajo una norma elegida (Bernstein & Newhouse, 2024; Vyas et al., 2024; Liu et al., 2025).

A esto se suma una cuarta geometría, la de la **salida**: si la política genera poses del efector en $SE(3)$ y es equivariante, el fine-tuning no tiene que volver a aprender la simetría (Tie et al., 2024).

### Formalismo

**Descenso más pronunciado bajo una norma.** Dado un gradiente $g$ y una norma $\|\cdot\|$, el paso
$$
\Delta^\star=\arg\min_{\Delta}\; g^\top\Delta+\tfrac{\lambda}{2}\|\Delta\|^2
=-\frac{\|g\|_\ast}{\lambda}\,\arg\max_{\|t\|=1} g^\top t
$$
depende sólo de la norma (su dual $\|\cdot\|_\ast$ fija la escala). Con la norma euclídea sale SGD; con $\|\Delta\|_F^2$ ponderada por la matriz de Fisher $F$ sale el gradiente natural $-\lambda^{-1}F^{-1}g$ del corpus. Bernstein & Newhouse (2024) muestran que, si se desactivan las medias móviles exponenciales, Adam es descenso más pronunciado bajo la norma "max-of-max" (de tipo $\ell_\infty$, descenso por signo) y Shampoo bajo la **norma espectral** por capa. Para una matriz $G=U\Sigma V^\top$ y la norma espectral,
$$
\Delta^\star_W=-\frac{\operatorname{tr}\Sigma}{\lambda}\,UV^\top ,
$$
es decir, el paso "ortogonaliza" el gradiente: todos sus valores singulares pasan a valer lo mismo. Muon aproxima $UV^\top$ con iteraciones de Newton-Schulz, y Liu et al. (2025) lo escalan a LLM añadiendo decaimiento de pesos y ajustando la escala de actualización por parámetro para igualar la RMS de AdamW. SOAP (Vyas et al., 2024) parte de la observación de que Shampoo (Gupta et al., 2018) equivale a Adafactor en la base propia de su precondicionador, y corre Adam en esa base que cambia lentamente.

**Ancla de Fisher contra el olvido (EWC).** Tras entrenar en la tarea $A$ con óptimo $\theta_A^\ast$, la tarea $B$ se aprende con
$$
\mathcal{L}(\theta)=\mathcal{L}_B(\theta)+\sum_i\frac{\lambda}{2}F_i\,(\theta_i-\theta^\ast_{A,i})^2 ,
$$
donde $F_i$ es la diagonal de la Fisher en $\theta_A^\ast$ (Kirkpatrick et al., 2016). Es la aproximación de Laplace de la posterior de $A$, o bien una región de confianza de Fisher centrada en el modelo base en vez de en el iterado actual. Fisher merging (Matena & Raffel, 2021) usa la misma métrica para **promediar** modelos: $\theta^\ast_i=\sum_m F^{(m)}_i\theta^{(m)}_i/\sum_m F^{(m)}_i$, la media ponderada por la precisión de cada modelo.

**Descenso espejo de políticas.** Con ventaja $A^{\pi_k}$ y paso $t_k$,
$$
\pi_{k+1}=\arg\max_{\pi}\;\mathbb{E}_{s}\!\Big[\mathbb{E}_{a\sim\pi}A^{\pi_k}(s,a)-\tfrac{1}{t_k}\,\mathrm{KL}\big(\pi(\cdot|s)\,\|\,\pi_k(\cdot|s)\big)\Big].
$$
MDPO (Tomar et al., 2020) resuelve este subproblema de forma aproximada con varios pasos de SGD sobre la política parametrizada, y así interpreta TRPO y PPO como variantes de un mismo esquema. Con el potencial de entropía, la divergencia de Bregman es exactamente la KL, lo que conecta con la geometría de la información del descenso espejo de Raskutti & Mukherjee (2013) del corpus.

### Métodos clave

- **EWC** (Kirkpatrick et al., 2016) y **Fisher merging** (Matena & Raffel, 2021): la Fisher del modelo base como métrica de "cuánto cuesta moverse". Sirven para ajustar un VLA a la escena del laboratorio sin perder las habilidades generales, y para fusionar varios adaptadores específicos de tarea (pesar, abrir frasco) en uno solo.
- **Policy mirror descent / MDPO** (Tomar et al., 2020): el marco común de NPG, TRPO y PPO. Aclara que el término $\beta\,\mathrm{KL}(\pi_\theta\|\pi_{\text{base}})$ que ya recomienda la Parte 2 (sección D.2) es un ancla fija, distinta de la KL de región de confianza al iterado $\pi_k$, y que conviene usar las dos.
- **Descenso bajo normas de operador**: la antología de Bernstein & Newhouse (2024), **SOAP** (Vyas et al., 2024; −40 % iteraciones y −35 % tiempo frente a AdamW en LM de 360M/660M) y **Muon** a escala (Liu et al., 2025; unas 2× más eficiente en cómputo que AdamW). Son la versión práctica de K-FAC y Shampoo del corpus. El precondicionador por capa se aproxima con una norma, no con la inversa de la Fisher.
- **Recetas de fine-tuning de VLA.** OpenVLA-OFT (Kim, Finn & Liang, 2025) cambia la tokenización discreta de OpenVLA por decodificación paralela, *chunks* de acciones, acciones continuas y pérdida L1. Así pasa del 76,5 % al 97,1 % en LIBERO con 26× más rendimiento, y lo valida en un ALOHA bimanual, el mismo brazo de AutoBio. En términos geométricos, mueve el fine-tuning del símplex de categorías a un espacio de acción continuo, donde la norma de la pérdida (L1) es la que define el paso.
- **RL sobre VLA (2025-2026).** SimpleVLA-RL (Li et al., 2025) aplica RL con recompensa de resultado a OpenVLA-OFT sobre veRL, supera a π0 en RoboTwin y describe el fenómeno *pushcut*: la política descubre patrones que no aparecen en las demostraciones. πRL (Chen et al., 2025) extiende la línea DPPO/ReinFlow a VLA de flujo (π0, π0.5) con dos variantes: Flow-Noise, ruido aprendible con verosimilitud exacta, y Flow-SDE, que convierte la ODE en una SDE con las mismas marginales. Ambas devuelven una $\log\pi$ tratable, que es lo que hace falta para la región de confianza en KL.
- **Salida equivariante en $SE(3)$.** ET-SEED (Tie et al., 2024) simplifica la condición de equivarianza de un proceso de difusión a nivel de trayectoria. Aprende con pocas demostraciones y generaliza a configuraciones no vistas. Complementa a Equivariant Diffusion Policy, EquiBot, SE(3)-DiffusionFields y RFMP del corpus, porque el ajuste fino sólo tiene que aprender lo que la simetría no da gratis.

Diffusion-EDFs (Ryu et al., 2023) lleva la equivarianza un paso más allá de ET-SEED: la difusión en $SE(3)$ es bi-equivariante, respecto a la pose de la escena y a la del objeto agarrado, y está construida sobre campos de descriptores equivariantes. Aprende tareas de pick-and-place con 5-10 demostraciones, lo que la convierte en una candidata para *fine-tuning* con pocos datos de laboratorio sin romper la simetría.

### Por qué importa para el brazo y el proyecto

La tabla D.6 de la Parte 2 ya fija la salida (twist o 6D), el adaptador (LoRA con precondicionador riemanniano) y el RL (PPO/DPPO/ReinFlow con `target_kl`). Esta sección añade tres decisiones concretas para ajustar π0, π0.5 u OpenVLA a las escenas de AutoBio (Lan et al., 2025): balanza analítica, frascos de reactivo y botellas ámbar.

1. **Dos anclas, dos geometrías.** Conviene combinar la KL al iterado (región de confianza, MDPO/PPO) con un ancla al modelo base. Esta puede ir en el espacio de políticas ($\beta\,\mathrm{KL}(\pi_\theta\|\pi_{\text{base}})$) o en el de parámetros (penalización EWC con la Fisher diagonal estimada sobre las demostraciones de AutoBio). La primera es más fiel; la segunda es gratis durante el SFT y no requiere muestrear la política base.
2. **Un adaptador por subtarea y fusión por Fisher.** Pesar en la balanza, destapar un frasco y colocar una botella tienen dinámicas distintas. Se pueden entrenar LoRA separados y fusionarlos con pesos de Fisher, en lugar de un único ajuste que interfiera entre tareas. La fusión es exacta sólo si los adaptadores comparten la base $W_0$, y la simetría $GL(r)$ de $BA$ obliga a fusionar $\Delta W$, no $B$ y $A$ por separado.
3. **Optimizador por capa.** Para el *action expert* de π0 o la cabeza de OFT (matrices densas pequeñas), Muon o SOAP son una alternativa barata a K-FAC. Sus pasos respetan la norma espectral de cada capa y se combinan bien con el ancla de Fisher. Los *embeddings* y los sesgos siguen con AdamW, como indican Liu et al. (2025).

Para el pipeline de visión, la receta de OpenVLA-OFT (acciones continuas + *chunks* + L1) es la base de SFT más directa. SimpleVLA-RL y πRL indican cómo seguir con RL en MuJoCo Playground cuando las demostraciones se quedan cortas, que es justo lo que AutoBio identifica como cuello de botella en la manipulación precisa de instrumentos.

---

## H5. Calibración cámara-robot y servo visual: de $AX=XB$ a los modelos fundacionales

### Intuición

El corpus ya cubre las dos piezas clásicas, pero solo como cita: la calibración mano-ojo de Tsai y Lenz (1989) y de Park y Martin (1994), y el servo visual IBVS/PBVS de Chaumette y Hutchinson (2006, 2007) junto con el servo fotométrico de Collewet y Marchand (2011). También cubre algunas variantes aprendidas: EasyHeC (Chen et al., 2023), que calibra por renderizado diferenciable; el PBVS con CNN de Bateux et al. (2017); DFVS (Harish et al., 2020), y Siame-se(3) (Felton et al., 2021), que regresa directamente un *twist* en $\mathfrak{se}(3)$. Faltan tres cosas.

1. **Qué garantías tiene el problema $AX=XB$ cuando hay ruido.** Park-Martin da una solución cerrada, pero no dice si el mínimo encontrado es global ni cómo pesar datos de distinta calidad.
2. **Cómo calibrar sin patrón**, mirando al propio brazo, con redes autosupervisadas o con modelos fundacionales que no hay que reentrenar (2023-2026).
3. **Cómo cerrar el lazo visual con controladores que tengan garantías en $SE(3)$**, y cómo sustituir los puntos característicos a mano por correspondencias aprendidas o por *features* de un ViT preentrenado.

Las tres comparten el mismo esqueleto matemático. Hay una incógnita en $SE(3)$ (el extrínseco ${}^{b}T_{c}$ o la pose relativa ${}^{c^*}T_{c}$), unos residuos en píxeles o en el álgebra, y un paso de optimización o control que vive en el espacio tangente.

### Formalismo

**Calibración como mínimos cuadrados en el grupo.** Con $n$ pares $(A_i,B_i)$ se resuelve

$$
X^\star=\arg\min_{X\in SE(3)}\sum_{i=1}^{n}\big\|\mathrm{Log}\big(A_i X B_i^{-1}X^{-1}\big)^\vee\big\|^2_{\Sigma_i^{-1}},
$$

o bien su versión robot-mundo $AX=YB$, en la que se estiman a la vez $X$ (efector→cámara) e $Y$ (base→patrón). Si se lineariza con $X\leftarrow \mathrm{Exp}(\delta)X$, cada iteración de Gauss-Newton es un paso en $\mathfrak{se}(3)$ con Jacobianos construidos con $\mathrm{Ad}$ (partes 1 y 2 del corpus). Chen et al. (2026) proponen justo este esquema iterativo en el álgebra de Lie para $AX=YB$. Mantienen las restricciones estructurales de $X$ e $Y$, actualizan los dos parámetros de forma sincronizada e introducen una **métrica de incertidumbre relativa** entre fuentes de datos (cinemática frente a visión) que repondera las iteraciones sin modelar el ruido de forma explícita. Es la contrapartida práctica de la propagación de covarianzas con adjuntos que ya aparece en §1.6 del documento 03.

**Optimalidad certificable.** Si la rotación se escribe como matriz con las restricciones cuadráticas $R^\top R=I$ y $\det R=1$, el coste anterior (en su forma algebraica) se convierte en un QCQP. Su relajación semidefinida (SDP) es *tight* cuando el ruido está acotado. Wise et al. (2020) lo demuestran para la calibración mano-ojo con cámara monocular, en la que la escala de la traslación es una incógnita más, y Wise et al. (2025) lo extienden a la calibración robot-mundo generalizada con varios sensores y varios patrones. En ese trabajo derivan además criterios de **identificabilidad**, es decir, qué movimientos del brazo hacen falta para que la solución sea única. En la práctica: se resuelve el SDP, se comprueba el rango de la solución (el certificado) y, si es de rango 1, se tiene el óptimo global y no un mínimo local de Gauss-Newton.

**Calibración sin marcadores.** Sea $p_k(q)={}^{b}T_{e}(q)\,p_k^{e}$ la posición 3D de un punto del robot dada por la cinemática directa. Si ese punto se detecta en la imagen como $u_k$,

$$
{}^{c}T_{b}^\star=\arg\min_{T}\sum_{t,k}\big\|u_{k,t}-\pi\big(T\,p_k(q_t)\big)\big\|^2 ,
$$

que es un PnP cuyos puntos 3D salen de la cinemática, no de un patrón. La alternativa densa sustituye $u_k$ por una máscara o una imagen y compara con un render diferenciable, $\mathcal{L}(T)=\|M_{\text{obs}}-\mathcal{R}(T,q)\|$, y retropropaga a $\delta\in\mathfrak{se}(3)$ como en LieTorch (Teed y Deng, 2021).

**Servo como control en el grupo.** Con error ${}^{c^*}T_{c}$, la ley $v=-\lambda\,\mathrm{Log}({}^{c^*}T_{c})^\vee$ del §3.4 del documento 03 es la versión de primer orden de un controlador en un grupo de Lie matricial. Prabhu et al. (2020) formalizan un controlador de primer orden para velocidad cartesiana en grupos de Lie matriciales, con **seguimiento exponencial global** en $SO(n)$ y $SE(n)$ (y local en cualquier grupo matricial), y lo validan en un brazo Sawyer de 7 GDL. Con eso, la PBVS "a lo Lie" pasa de ser una heurística a un resultado con garantía. Cuando el error se mide en la imagen, la ley IBVS $v=-\lambda\widehat{L}_s^{+}e$ necesita correspondencias $s\leftrightarrow s^*$; los métodos recientes cambian **de dónde salen** esas correspondencias y **quién calcula** $v$.

### Métodos clave

- **Wise et al. (2020), *Certifiably Optimal Monocular Hand-Eye Calibration*.** Relajación convexa de la calibración mano-ojo con escala desconocida y certificado de optimalidad global con ruido acotado. Es el complemento riguroso de Park y Martin (1994).
- **Wise et al. (2025), RWHEC certificable.** Resuelve $AX=YB$ con varios sensores y patrones, e incluye identificabilidad y garantías *a priori*. Aplica directamente a calibrar a la vez la cámara de muñeca y las cámaras fijas del laboratorio.
- **Chen et al. (2026), $AX=YB$ con incertidumbre.** Iteración en el álgebra de Lie con repesado según la incertidumbre relativa y un buen inicializador. Es la opción pragmática cuando el ruido de la cinemática y el de la visión son muy distintos.
- **CtRNet (Lu et al., 2023).** Estima ${}^{c}T_{b}$ sin marcadores. Un detector de *keypoints* más PnP da velocidad en inferencia, y durante el entrenamiento la silueta renderizada de forma diferenciable se compara con una segmentación del robot. Así se autosupervisa con imágenes reales sin etiquetar y se cierra la brecha sim-to-real. Es el sucesor directo de la idea de EasyHeC.
- **Differentiable Robot Rendering, "Dr. Robot" (Liu et al., 2024).** Representa el cuerpo del robot con *Gaussian Splatting* deformado por la cinemática, de modo que la imagen es diferenciable respecto a los parámetros de control. Sirve para recuperar la pose del robot a partir de imágenes y para controlar desde píxeles. Generaliza el render de mallas de EasyHeC a un modelo de apariencia completo.
- **Kalib (Tang et al., 2024).** Sin redes nuevas y sin malla. Un modelo fundacional de seguimiento de puntos sigue un punto de referencia del robot, la cinemática da su 3D y un PnP resuelve el extrínseco. Los autores reportan errores del orden de milímetros y de menos de un grado.
- **ARC-Calib (Chanrungmaneekul et al., 2025).** Totalmente autónomo y basado en modelo: el brazo ejecuta movimientos exploratorios cuyas trayectorias en la imagen imponen restricciones de coplanaridad y colinealidad, y el extrínseco se refina iterativamente sin entrenar nada. Es el análogo geométrico de la "exploración del espacio" de EasyHeC.
- **CNS (Chen et al., 2023).** Codifica las correspondencias de *keypoints* entre la imagen actual y la deseada como un grafo, y una GNN produce la velocidad de la cámara. Se entrena solo en simulación con puntos 3D aleatorios y se transfiere al robot real sin ajuste. Combina la generalidad de IBVS con la cuenca de convergencia amplia de Siame-se(3).
- **ViT-VS (Scherl et al., 2025).** IBVS clásico en el que las características son *patch embeddings* de DINOv2 emparejados por similitud coseno. No necesita entrenamiento por tarea, supera a IBVS clásico hasta en un 31,2 % relativo en escenas perturbadas e iguala a los métodos aprendidos. Para compensar la invarianza a la rotación del ViT, evalúa cuatro rotaciones discretas iniciales.
- **Prabhu et al. (2020).** Controlador de primer orden en grupos de Lie matriciales con garantía de convergencia exponencial. Es la base teórica para usar $\mathrm{Log}$ como error de servo.

### Por qué importa para el brazo y el proyecto

**1. Banco de pruebas de calibración con verdad exacta.** MuJoCo da la verdad de ${}^{b}T_{c}$ mediante `cam_xpos`/`cam_xmat` (ojo con la convención OpenGL→OpenCV, $\mathrm{diag}(1,-1,-1)$, del §1.2 del documento 03). Se pueden generar pares $(A_i,B_i)$ moviendo el brazo y estimando $B_i$ con PnP sobre un patrón renderizado, añadir ruido $\mathrm{Exp}(\epsilon)$, $\epsilon\sim\mathcal{N}(0,\Sigma)$, y comparar Park-Martin (OpenCV), Gauss-Newton en el álgebra (Chen et al., 2026) y la SDP certificable (Wise et al., 2020, 2025). La métrica es $\|\mathrm{Log}(\hat X^{-1}X_{\text{gt}})^\vee\|$. Los criterios de identificabilidad de Wise et al. dicen qué poses de la trayectoria de calibración conviene programar, que es la versión teórica de la exploración activa de EasyHeC y ARC-Calib.

**2. Calibración sin marcadores del brazo de AutoBio.** El modelo MJCF ya contiene la cadena cinemática y las mallas, justo lo que piden Kalib (cadena y punto de referencia), CtRNet y Dr. Robot (malla o apariencia). El renderizador offscreen del repositorio permite generar las máscaras y los *keypoints* sintéticos para entrenar CtRNet o validar Kalib, con SAM 2 (Ravi et al., 2024), que ya está en el corpus, como segmentador del robot. Sobre fondos cargados (balanza analítica, frascos ámbar), un método sin patrón es lo único viable en el robot real.

**3. Servo visual para la aproximación fina.** Pesar en la balanza analítica o alinear la pinza con el tapón de un frasco de reactivo exige precisión milimétrica, por encima de lo que da una pose 6D de FoundationPose (Wen et al., 2023) con una calibración imperfecta. El esquema propuesto funciona así: la pose 6D más la calibración llevan el efector a unos centímetros, y un servo cierra el último tramo. ViT-VS es el candidato de cero entrenamiento, porque solo necesita una imagen objetivo tomada con la cámara de muñeca. CNS se entrena gratis en MuJoCo con puntos aleatorios. La ley de control debe expresarse como un *twist* en $\mathfrak{se}(3)$ y convertirse en velocidades articulares con el Jacobiano del brazo (o con mink, Zakka), apoyándose en la garantía de Prabhu et al. (2020).

**4. Conexión con el aprendizaje de políticas.** El error de calibración, modelado como ruido en $\mathfrak{se}(3)$, es una forma de aleatorización de dominio (Tobin et al., 2017) para las políticas de difusión y VLA del corpus. Además, un servo con garantías puede servir de "experto" que genera demostraciones para el *fine-tuning* de esas políticas.

---

## H6. Variedades neuronales: geometría de redes y neurociencia motora

"Variedad neuronal" (*neural manifold*) tiene en la literatura dos significados que el corpus mezcla sin distinguir. **(a)** En aprendizaje automático, es la subvariedad de baja dimensión que ocupan los datos o las representaciones internas de una red, junto con la métrica que el decodificador induce sobre el espacio latente. **(b)** En neurociencia motora, es el subespacio de baja dimensión en el que se mueve la actividad de cientos de neuronas corticales cuando un animal controla el brazo. El corpus cubre bien el lado (a) en su versión "de grupo" (Falorsi et al., 2018; Zhu et al., 2021) y en su versión *pullback* aplicada a habilidades (Arvanitidis et al., 2017; Beik-Mohammadi et al., 2021, 2022). Tiene la hipótesis de la variedad (Fefferman et al., 2016), pero le faltan tres cosas: cómo **medir** la dimensión de una representación, por qué la métrica *pullback* solo tiene sentido si el modelo es **probabilístico**, y todo el lado (b). Esta sección cubre esos huecos.

### Intuición

Un brazo de 6 o 7 grados de libertad que coge un frasco de reactivo, lo lleva a la balanza y lo deja no recorre todo $\mathbb{R}^7$: las demostraciones viven en una variedad de dimensión mucho menor, parametrizada por pocas "perillas" (a qué frasco ir, a qué altura, con qué giro de muñeca). La corteza motora del primate hace lo mismo: aunque se registren $N\approx 100$ neuronas, su actividad durante un alcance queda explicada por $d\approx 10$ **modos neuronales**. Lo que controla el movimiento es la evolución temporal de esos modos (Gallego et al., 2017). Esa idea se parece mucho a la de las **sinergias** en robótica: en vez de mandar cada articulación por separado, se controlan unas pocas coordenadas latentes que mueven muchas articulaciones de forma coordinada.

La geometría importa en los dos lados. En una red, la distancia euclídea entre dos latentes $z_1,z_2$ no dice nada fiable: el decodificador puede estirar y comprimir el espacio de forma arbitraria. La distancia correcta es la longitud de la curva **decodificada**, es decir, la métrica *pullback*. Sus geodésicas son movimientos que se quedan cerca de los datos (Chen et al., 2017). En el cerebro, la variedad es la parte **estable** del código: las neuronas concretas que se registran cambian de un día a otro, pero la dinámica latente se conserva, y eso permite recalibrar un decodificador alineando variedades en lugar de reaprenderlo (Farshchian et al., 2018).

### Formalismo

**Métrica *pullback* y su versión bayesiana.** Sea $f:\mathcal{Z}\subset\mathbb{R}^d\to\mathbb{R}^D$ un decodificador con Jacobiano $J_f(z)$. La métrica inducida y la energía de una curva $\gamma:[0,1]\to\mathcal{Z}$ son

$$
G(z)=J_f(z)^\top J_f(z),\qquad
E[\gamma]=\tfrac12\int_0^1 \dot\gamma(t)^\top G(\gamma(t))\,\dot\gamma(t)\,dt ,
$$

y la geodésica es el minimizador de $E$ con extremos fijos. Chen et al. (2017) resuelven ese problema parametrizando $\gamma$ con una red pequeña y minimizando $E$ discretizada. Lo aplican a un brazo robótico simulado y a captura de movimiento humano para generalizar habilidades aprendidas. Si el decodificador es gaussiano, $x=\mu(z)+\sigma(z)\odot\epsilon$, la métrica esperada es $\bar G(z)=J_\mu^\top J_\mu + J_\sigma^\top J_\sigma$ (Arvanitidis et al., 2017, ya en el corpus). El término de varianza crece lejos de los datos y "encarece" salir de ellos. Hauberg (2018) convierte esto en un argumento de principio. Con las regularizaciones habituales, los métodos **no probabilísticos** no recuperan la estructura diferencial de la variedad: encuentran variedades casi lineales o espacios con "teletransportes". Con *priors* razonables, los métodos **probabilísticos** sí la recuperan, aunque explotarla del todo exige extensiones estocásticas de la geometría riemanniana. En la práctica, la **incertidumbre** del modelo es lo que hace que las geodésicas sigan los datos en vez de atajar por zonas vacías. Arvanitidis et al. (2021) generalizan a cualquier decodificador $p(x\mid z)$ tirando hacia atrás la **métrica de Fisher-Rao**:

$$
G_{\mathrm{FR}}(z)=J_\eta(z)^\top\, \mathcal{I}\big(\eta(z)\big)\, J_\eta(z),
$$

donde $\eta(z)$ son los parámetros de la distribución de salida e $\mathcal{I}$ es su matriz de información de Fisher. Es la misma Fisher que define el gradiente natural en el corpus (Amari, 1998; Martens, 2014). Aquí se usa sobre el **latente** y no sobre los pesos, lo que une directamente la parte de gradiente natural con la de variedades.

**Dimensión intrínseca de una representación.** Ansuini et al. (2019) estiman la dimensión $d$ de cada capa con el estimador TwoNN: si $r_1,r_2$ son las distancias de un punto a sus dos vecinos más cercanos y $\mu=r_2/r_1$, entonces localmente $F(\mu)=1-\mu^{-d}$, y $d$ sale de una regresión lineal de $-\log(1-F(\mu))$ frente a $\log\mu$. Encuentran que la dimensión intrínseca es **órdenes de magnitud menor** que el número de unidades, que sigue un perfil en "joroba" (sube en las primeras capas y baja en las últimas) y que la dimensión de la última capa predice el error de test. También observan que las variedades son **curvas**: un PCA lineal sobreestima su dimensión.

**Variedad neuronal motora.** Sea $x(t)\in\mathbb{R}^N$ la tasa de disparo de $N$ neuronas. El modelo de Gallego et al. (2017) es

$$
x(t)\approx U\,z(t),\qquad U\in\mathbb{R}^{N\times d},\ d\ll N,\qquad \dot z(t)=F\big(z(t)\big)+B\,u(t),
$$

donde las columnas de $U$ son los modos neuronales y la conducta sale de un *readout* $y(t)=W z(t)$. LFADS (Sussillo et al., 2016) aprende esto sin supervisión como un VAE secuencial. Un codificador infiere la condición inicial $g_0$, una RNN generadora evoluciona $g_t$, un controlador infiere entradas $u_t$, los factores son $f_t=W_f\,g_t$ y los *spikes* se modelan como Poisson con tasa $r_t=\exp(W_r f_t)$. Con datos de alcance de mono, LFADS recupera trayectorias latentes que predicen la cinemática del brazo mucho mejor que los *spikes* suavizados.

**Analogía con las sinergias.** En robótica, una sinergia lineal es $\dot q = S\,\dot z$ con $S\in\mathbb{R}^{n\times d}$; la versión geométrica de Jaquier & Asfour (2022, corpus) sustituye $S$ por geodésicas de la métrica de inercia. La correspondencia es directa: $U\leftrightarrow S$ (modos ↔ sinergias), $\dot z=F(z)+Bu$ ↔ primitiva dinámica en el latente, y el *readout* $W$ ↔ cinemática directa.

### Métodos clave

- **Only Bayes should learn a manifold** (Hauberg, 2018). Justifica por qué la métrica *pullback* necesita un decodificador con incertidumbre. Sin incertidumbre, las geodésicas de Beik-Mohammadi et al. (2021) no evitarían las regiones sin demostraciones.
- **Pulling back information geometry** (Arvanitidis et al., 2021). Métrica de Fisher-Rao para decodificadores no gaussianos (Bernoulli, categóricos, von Mises-Fisher). Sirve si la acción del brazo se discretiza en *tokens*, como en FAST (Pertsch et al., 2025).
- **Metrics for Deep Generative Models** (Chen et al., 2017). Geodésicas latentes con red neuronal y aplicación explícita a generalización de movimientos de brazo robótico. Es el precedente directo de Beik-Mohammadi et al. (2021).
- **Intrinsic dimension of data representations** (Ansuini et al., 2019). Da una herramienta barata (TwoNN) para medir qué dimensión tiene de verdad el latente de una política o de un codificador visual.
- **Neural manifolds for the control of movement** (Gallego et al., 2017). Marco conceptual del lado (b): modos neuronales, variedad y dinámica latente como sustrato del control motor.
- **LFADS** (Sussillo et al., 2016). Dinámica latente inferida con un VAE secuencial. La arquitectura (condición inicial + generador + entradas inferidas) es exactamente un modelo del mundo latente aplicable a trayectorias del robot.
- **CEBRA** (Schneider et al., 2022). Aprendizaje contrastivo que usa etiquetas de conducta o de tiempo para obtener *embeddings* consistentes entre sesiones y sujetos. Permite decodificar y comparar variedades entre animales o, por analogía, entre embodiments.
- **Adversarial Domain Adaptation for Stable BMIs** (Farshchian et al., 2018). Mantienen estable un decodificador de BMI alineando la representación latente entre días con CCA, con la divergencia KL o con una red adversaria. Es el equivalente neurocientífico de la adaptación de dominio *sim-to-real*.
- **Learning Latent Actions to Control Assistive Robots** (Losey et al., 2021). Un autoencoder condicionado al estado $a=\phi(s,z)$ mapea un joystick de 2 grados de libertad a un brazo de 7. Es la versión robótica de "controlar por la variedad", pensada para usuarios con interfaces de baja dimensión como una BCI.
- **Learning Action Manifold with Multi-view Latent Priors** (Xiao et al., 2026). En una VLA, predice acciones directamente sobre la variedad de acciones válidas en vez de regresar ruido o velocidad. Es la hipótesis de la variedad aplicada a la cabeza de acción, probada en LIBERO y RoboTwin 2.0.

Dos trabajos unen las dos mitades de esta sección. Chung y Abbott (2021) revisan la geometría de poblaciones neuronales (capacidad de clasificación de variedades, dimensión, desenmarañamiento) y aplican las mismas medidas a corteza y a redes profundas. Valeriani et al. (2023) miden la dimensión intrínseca capa a capa en transformers grandes y encuentran un perfil de expansión, contracción y meseta. Esto sugiere de qué capa de un ViT o una VLA conviene extraer rasgos para el control. Del lado de las arquitecturas, EMLP (Finzi et al., 2021) construye capas equivariantes para cualquier grupo matricial resolviendo restricciones sobre los generadores del álgebra de Lie, y Lie Neurons (Lin et al., 2023) opera directamente sobre elementos del álgebra con equivarianza adjunta. Son la forma natural de procesar twists en $\mathfrak{se}(3)$ como entrada o salida de una red.

### Por qué importa para el brazo y el proyecto

1. **Medir antes de modelar.** Aplicar TwoNN (Ansuini et al., 2019) a las trayectorias articulares grabadas en la escena MuJoCo/AutoBio (Lan et al., 2025) y a los *embeddings* del codificador visual (p. ej. DINO en Grounding DINO) indica qué dimensión latente usar en un VAE de movimientos o en la cabeza de acción de una política como ACT o Diffusion Policy (Zhao et al., 2023; Chi et al., 2023). Si la tarea "frasco → balanza" tiene $d\approx 4$, un latente de 32 dimensiones sobra.
2. **Geodésicas que respetan los datos.** Para interpolar o generalizar entre demostraciones (por ejemplo, frascos en posiciones nuevas), la métrica *pullback* de un decodificador **con incertidumbre** (Hauberg, 2018; Arvanitidis et al., 2017) da trayectorias que no atajan por zonas nunca vistas, como la mesa o la carcasa de la balanza. Así, Beik-Mohammadi et al. (2021) pasa de ser una curiosidad a una herramienta con justificación teórica.
3. **Fisher en el latente = gradiente natural en la política.** La métrica $G_{\mathrm{FR}}$ (Arvanitidis et al., 2021) conecta este bloque con NPG/TRPO y K-FAC del corpus (Kakade, 2001; Schulman et al., 2015; Martens & Grosse, 2015). Un *fine-tuning* por RL que se mueva en el latente de acciones puede precondicionarse con la misma geometría que define las geodésicas.
4. **Estabilidad de la variedad como receta *sim-to-real*.** Farshchian et al. (2018) y CEBRA (Schneider et al., 2022) muestran que lo estable entre sesiones es la variedad y no las unidades individuales. Trasladado al proyecto: alinear el latente visual de imágenes renderizadas con el de imágenes reales (CCA o KL sobre $z$) antes de reentrenar la política es más barato que hacer aleatorización de dominio a ciegas (Tobin et al., 2017).
5. **Control de baja dimensión y BCI.** Losey et al. (2021) y el modelo de Gallego et al. (2017) sugieren exponer el brazo mediante 2-4 "perillas" latentes, aprendidas de las demostraciones de AutoBio y condicionadas al estado. Sirven para teleoperación con *gamepad*, para una interfaz asistiva o como espacio de acción compacto para RL. Frente a las sinergias geodésicas (Jaquier & Asfour, 2022), que derivan las sinergias de la **física** (métrica de inercia), aquí se derivan de los **datos**. Lo razonable es combinarlas: un latente aprendido cuya métrica *pullback* se pondera con la matriz de inercia $M(q)$ que ya da MuJoCo.
6. **Modelo de dinámica latente.** LFADS (Sussillo et al., 2016) ofrece una arquitectura probada para inferir $z_0$ y entradas $u_t$ a partir de observaciones ruidosas. Sustituyendo *spikes* por *features* de cámara, es un filtro/modelo del mundo que puede alimentar un MPC en el latente.

---

## H7. Contexto del proyecto: pose por categoría, seguimiento, *sim-to-real* y automatización de laboratorio

### Intuición

El corpus ya cubre bien la **pose 6D a nivel de instancia**: PoseCNN, DenseFusion, PVNet, GDR-Net, CosyPose, MegaPose, FoundationPose y SAM-6D suponen que existe una malla CAD exacta del objeto (o unas pocas vistas de referencia). También cubre los objetos transparentes (ClearGrasp, KeyPose, TransCG, ClearPose, LucidGrasp) y los simuladores de laboratorio AutoBio (Lan et al., 2025) y Chemistry3D (Li et al., 2024), junto con la aleatorización de dominio (Tobin et al., 2017). Lo que falta es el **eslabón intermedio** entre estas piezas y la escena real del proyecto:

1. **Familias de objetos de tamaño variable.** Nuestros kits de frascos (el de botellas agroquímicas blancas tiene 6 tamaños, además de los frascos ámbar y los de reactivos) no son un único CAD, sino una **categoría** con variación de forma y escala. La pose por categoría estima $(R,t)$ y además el **tamaño** $s$ (o una caja 3D métrica), sin necesitar la malla exacta de cada instancia.
2. **Seguimiento temporal.** Durante un vertido o un transporte, la pose cambia de forma continua. Re-estimar desde cero en cada fotograma es caro y ruidoso. Un *tracker* propaga la pose en $SE(3)$ de un fotograma al siguiente.
3. **Sistemas completos de laboratorio.** La literatura de 2024-2026 sobre laboratorios autónomos (*self-driving labs*) y benchmarks de agentes científicos muestra qué tareas, métricas y modos de fallo importan en la práctica: líquidos, vidrio transparente, sustratos frágiles y la identificación de dispositivos y muestras mediante códigos de barras.

### Formalismo

**Espacio de coordenadas normalizado (NOCS).** Wang et al. (2019) definen, para cada categoría, un espacio canónico $\mathcal{N}=[0,1]^3$ donde toda instancia está centrada, orientada de forma consistente y escalada para que la diagonal de su caja envolvente mida 1. Una red predice, para cada píxel $u$ de la máscara del objeto, su coordenada canónica $c_u\in\mathcal{N}$. Con la profundidad se obtiene el punto 3D observado $p_u$ en el sistema de la cámara, y la pose y el tamaño se recuperan resolviendo un problema de **alineación por similitud** (Umeyama) con RANSAC:

$$
(\hat s,\hat R,\hat t)=\arg\min_{s>0,\;R\in SO(3),\;t\in\mathbb{R}^3}\ \sum_{u}\big\|p_u-(s\,R\,c_u+t)\big\|^2 .
$$

El resultado es un elemento del **grupo de similitudes** $\mathrm{Sim}(3)=\{(s,R,t)\}$, de dimensión 7, cuya álgebra añade al $\mathfrak{se}(3)$ un generador de escala: $\xi=(\rho,\phi,\sigma)\in\mathbb{R}^7$, $\mathrm{Exp}(\xi)=\big(e^{\sigma},\,\mathrm{Exp}(\phi),\,V(\phi,\sigma)\rho\big)$. Es el mismo grupo que usa EquiBot (Yang et al., 2024) para su equivarianza $\mathrm{SIM}(3)$. Los benchmarks de categoría (CAMERA y REAL275, introducidos por NOCS) reportan la **IoU 3D** de las cajas con tamaño y la fracción de poses con error menor que $n^\circ$ y $m$ cm (p. ej. $5^\circ 2\,\mathrm{cm}$, $5^\circ 5\,\mathrm{cm}$, $10^\circ 2\,\mathrm{cm}$). En la literatura se habla de pose de 9 grados de libertad cuando el tamaño es anisótropo ($s\in\mathbb{R}^3_{>0}$).

**Simetría como cociente.** Un frasco cilíndrico es invariante bajo $SO(2)$ alrededor de su eje, así que la pose observable vive en el cociente $SE(3)/SO(2)$ (y, si no hay etiqueta visible, también en $\mathrm{Sim}(3)/SO(2)$). La pérdida o la densidad debe ser invariante: $d([R_1],[R_2])=\min_{S\in SO(2)} d(R_1S,R_2)$. Este es el mismo problema que la sección 2.3 del documento 3 plantea para el tubo de centrífuga, ahora a nivel de categoría.

**Pose como distribución generativa.** GenPose (Zhang et al., 2023) plantea la pose como un **modelo generativo condicional** $p(T\mid \mathcal{P})$, donde $\mathcal{P}$ es la nube de puntos parcial. Aprende la *score* $\nabla_T\log p_\sigma(T\mid\mathcal{P})$ con un modelo de difusión, muestrea muchas hipótesis, deriva de la *score* un modelo de energía para estimar su verosimilitud, filtra las poco probables y agrega el resto. Así resuelve el problema de las **múltiples hipótesis** que plantean la simetría y la oclusión. DiffusionNOCS (Ikeda et al., 2024) aplica la difusión al **mapa NOCS denso** en vez de a la pose, y la recupera después por alineación. Así hereda la gestión de la simetría y de la incertidumbre.

**Seguimiento por puntos clave.** 6-PACK (Wang et al., 2019b) representa cada objeto con un pequeño conjunto de puntos clave 3D $\{k_j\}$ aprendidos sin anotación y anclados a la categoría. El movimiento entre fotogramas se obtiene emparejando los puntos clave y resolviendo un problema de Procrustes en $SE(3)$:

$$
\Delta T_t=\arg\min_{\Delta T\in SE(3)}\sum_j\big\|k_j^{(t)}-\Delta T\,k_j^{(t-1)}\big\|^2,\qquad T_t=\Delta T_t\,T_{t-1}.
$$

Es la versión de categoría del modo de seguimiento de FoundationPose (Wen et al., 2023), y encaja con los filtros en grupos de Lie de la parte 1 (Barrau y Bonnabel, 2017): $\Delta T_t$ es la observación y $T_t$ el estado.

### Métodos clave

- **NOCS** (Wang et al., 2019). Primer método de pose y tamaño a nivel de categoría a partir de RGB-D. Introduce el espacio canónico por categoría, el dataset sintético CAMERA (generado con mezcla de realidad consciente del contexto) y el dataset real REAL275. Es la base de todo lo que sigue.
- **6-PACK** (Wang et al., 2019b). Seguimiento 6D en tiempo real de instancias nuevas de categorías conocidas mediante puntos clave anclados. Supera a los métodos previos en el benchmark NOCS y se demuestra en manipulación en lazo cerrado.
- **GenPose** (Zhang et al., 2023). Difusión basada en *score* para la pose de categoría. Supera el 50 % y el 60 % en las métricas estrictas $5^\circ 2\,\mathrm{cm}$ y $5^\circ 5\,\mathrm{cm}$ de REAL275, generaliza a categorías nuevas que comparten simetría y se extiende al seguimiento.
- **DiffusionNOCS** (Ikeda et al., 2024). Difusión sobre mapas canónicos densos con entrada multimodal. **Se entrena solo con datos sintéticos** y generaliza a datasets reales, superando incluso a métodos entrenados en el dominio de destino. Es la demostración más directa de que el *sim-to-real* de pose por categoría es viable.
- **TransNet** (Zhang et al., 2023b). Pose por categoría de **objetos transparentes**: completado local de profundidad más estimación de normales, y un sistema robótico que hace *pick-and-place* y **vertido** con vasos transparentes. Une la línea de ClearGrasp/ClearPose con la de NOCS.
- **Manipulación de recipientes transparentes con líquido en el laboratorio** (Schober et al., 2024). Estimación por visión del volumen de líquido y un método de vertido guiado por simulación para recipientes de boca estrecha, integrado en un UR5 para automatizar cultivo celular. Publica el dataset LabLiquidVolume.
- **LabUtopia** (Li et al., 2025). Simulador de laboratorio de alta fidelidad (LabSim, con interacciones físico-químicas), generador procedural de escenas (LabScene) y benchmark jerárquico de 5 niveles (LabBench), con 30 tareas y más de 200 activos. Es el competidor natural de AutoBio y de Chemistry3D.
- **ORGANA** (Darvish et al., 2024). Asistente robótico para química que combina LLMs, químicos en el lazo y **realimentación visual**. Ejecuta tareas de solubilidad, pH, recristalización y electroquímica (incluido un plan de 19 pasos en paralelo). En el estudio con usuarios, ahorra de media un 80,3 % del tiempo.
- **ASHE** (Fontenot et al., 2025). Manipulación en lazo cerrado de sustratos de vidrio transparentes en un *self-driving lab*: un detector de micro-errores basado en *deep learning* corrige la colocación. Obtiene un 98,5 % de colocaciones correctas al primer intento en 130 ensayos y corrige todos los errores detectados.
- **LAPP** (Wolf et al., 2021). Marco *plug & play* para laboratorios farmacéuticos: cada dispositivo lleva un **código de barras** (que apunta a su protocolo de control en una base de datos) y un **marcador fiducial** (que da su pose en $SE(3)$). Un manipulador móvil hace SLAM, detecta la pose con el fiducial y lee el código con visión. Es la referencia más sólida que hemos encontrado sobre lectura de códigos en flujos robóticos de laboratorio.

El corpus trata MuJoCo, MuJoCo Playground y AutoBio, pero no el otro simulador del equipo. Orbit (Mittal et al., 2023) es el artículo de referencia de Isaac Lab: entornos de manipulación paralelos en GPU, sensores de cámara y teleoperación, y sobre él está construido IsaacLab-mlx, el port a Apple Silicon que usa el equipo. Sirve para comparar resultados entre los dos simuladores con la misma tarea.

### Por qué importa para el brazo y el proyecto

**Frascos de 6 tamaños → pose por categoría.** Con FoundationPose haría falta una malla por tamaño y un *onboarding* por instancia. Tratar el kit como una categoría con NOCS o DiffusionNOCS permite estimar $(s,R,t)\in\mathrm{Sim}(3)$ con un solo modelo. El tamaño estimado $\hat s$ sirve además de **clasificador de tamaño**, que decide la apertura de la pinza y la altura de agarre. Como tenemos las mallas de los 6 tamaños en `simulation/assets/`, podemos generar los mapas NOCS de referencia gratis en MuJoCo o Blender: basta con normalizar cada malla a la diagonal unidad y renderizar las coordenadas canónicas como color.

**Simetría y pérdidas.** Los frascos son casi $SO(2)$-simétricos. Hay que usar las pérdidas cociente de la sección anterior o un modelo generativo (GenPose), que devuelve un "anillo" de hipótesis coherente con Implicit-PDF (Murphy et al., 2021). La etiqueta o el código de barras rompe la simetría: si es visible, fija el ángulo alrededor del eje, y conviene tratarla como una observación adicional y no como ruido.

**Seguimiento para verter y pesar.** En la balanza analítica y durante el vertido, el objeto se mueve con la pinza. Un *tracker* (el modo *tracking* de FoundationPose, o 6-PACK/GenPose a nivel de categoría) da $T_t$ a la frecuencia del control. Su error $\mathrm{Log}(T_t^{-1}\hat T_t)\in\mathfrak{se}(3)$ entra directamente en el servo visual PBVS de la parte 3 y en el filtro invariante de la parte 1.

**Sim-to-real.** DiffusionNOCS aporta evidencia de que entrenar **solo** con datos sintéticos basta si la representación es canónica y la aleatorización es amplia, lo que refuerza la estrategia de Tobin et al. (2017) con las escenas renderizadas de AutoBio. Para el vidrio ámbar y los frascos transparentes, TransNet y Schober et al. (2024) indican que hay que completar la profundidad antes de alinear, porque la pose por categoría depende de $p_u$. El puente a Blender de AutoBio (con transmisión e índice de refracción) es el lugar natural para generar esos datos.

**Benchmarks y posicionamiento.** LabUtopia, AutoBio y Chemistry3D definen hoy el estado del arte en simulación de laboratorio. ORGANA y ASHE muestran que los sistemas reales dependen de la **detección y corrección de errores en lazo cerrado** más que de una pose perfecta en un único disparo. Para la demo, medir el éxito por episodio con recuperación (como ASHE) es más convincente que reportar solo ADD.

**Códigos de barras.** La literatura académica sobre lectura de códigos en robótica de laboratorio es escasa y está dominada por productos comerciales. LAPP es la excepción citable. Su patrón (fiducial para la pose y código para la identidad) encaja con nuestros 200 códigos de reactivos: un decodificador estándar de Data Matrix o QR sobre el recorte de la etiqueta, con la pose de la etiqueta obtenida de la pose del frasco, identifica el compuesto y además rompe la simetría $SO(2)$.

---

## Bibliografía comentada

| # | Título | Autores | Año | Enlace | Por qué es relevante |
|---|---|---|---|---|---|
| 1 | Screw and Lie Group Theory in Multibody Kinematics -- Motion Representation and Recursive Kinematics of Tree-Topology Systems | Andreas Mueller | 2023 | [arXiv:2306.17415](https://arxiv.org/abs/2306.17415) | **H1.** Sustituto abierto de Murray-Li-Sastry y Lynch-Park: PoE, cuatro representaciones de giros (cuerpo, espacial, híbrida, mixta) y Jacobianos recursivos con sus derivadas. |
| 2 | Screw and Lie Group Theory in Multibody Dynamics -- Recursive Algorithms and Equations of Motion of Tree-Topology Systems | Andreas Mueller | 2023 | [arXiv:2306.17793](https://arxiv.org/abs/2306.17793) | **H1.** Newton-Euler recursivo O(n) y ecuaciones de movimiento en forma cerrada con Ad y ad, versión abierta de Park et al. (1995) y Featherstone. |
| 3 | A tutorial on $\mathbf{SE}(3)$ transformation parameterizations and on-manifold optimization | José Luis Blanco-Claraco | 2021 | [arXiv:2103.15980](https://arxiv.org/abs/2103.15980) | **H1.** Tutorial con los Jacobianos de composición, Exp y Log en SE(3) y el esquema Gauss-Newton en la variedad que usa la IK por LM del proyecto. |
| 4 | Efficient Analytical Derivatives of Rigid-Body Dynamics using Spatial Vector Algebra | Shubham Singh, Ryan P. Russell, Patrick M. Wensing | 2021 | [arXiv:2105.05102](https://arxiv.org/abs/2105.05102) | **H1.** Derivadas cerradas y recursivas de la dinámica inversa para juntas que son grupos de Lie, necesarias para DDP y ajuste por gradiente. |
| 5 | Geometry-aware Manipulability Learning, Tracking and Transfer | Noémie Jaquier, Leonel Rozo, Darwin G. Caldwell et al. | 2018 | [arXiv:1811.11050](https://arxiv.org/abs/1811.11050) | **H1.** Trata el elipsoide de manipulabilidad de Yoshikawa como matriz SPD y lo aprende y sigue con el Jacobiano de manipulabilidad en la variedad SPD. |
| 6 | IKFlow: Generating Diverse Inverse Kinematics Solutions | Barrett Ames, Jeremy Morgan, George Konidaris | 2021 | [arXiv:2111.08933](https://arxiv.org/abs/2111.08933) | **H1.** IK aprendida con flujos normalizantes que muestrea la variedad de soluciones de un brazo redundante en milisegundos. |
| 7 | cuRobo: Parallelized Collision-Free Minimum-Jerk Robot Motion Generation | Balakumar Sundaralingam, Siva Kumar Sastry Hari, Adam Fishman et al. | 2023 | [arXiv:2310.17274](https://arxiv.org/abs/2310.17274) | **H1.** Referencia de IK y trayectorias libres de colisión en GPU con miles de semillas paralelas. |
| 8 | PyRoki: A Modular Toolkit for Robot Kinematic Optimization | Chung Min Kim, Brent Yi, Hongsuk Choi et al. | 2025 | [arXiv:2505.03728](https://arxiv.org/abs/2505.03728) | **H1.** Toolkit JAX (CPU/GPU/TPU) de IK, trayectorias y retargeting del autor de jaxlie; más rápido que cuRobo en IK según sus autores. |
| 9 | Analytical Derivatives of Rigid Body Dynamics Algorithms | Justin Carpentier, Nicolas Mansard | 2018 | [doi](https://doi.org/10.15607/RSS.2018.XIV.038) | **H1.** Artículo base de las derivadas analíticas de RNEA y ABA en Pinocchio (sin versión arXiv). |
| 10 | Linear-time Differential Inverse Kinematics: an Augmented Lagrangian Perspective | Bruce Wingo, Ajay Suresha Sathya, Stéphane Caron et al. | 2024 | [doi](https://doi.org/10.15607/RSS.2024.XX.110) | **H1.** IK diferencial con restricciones (la clase de problemas QP de mink) resuelta en tiempo lineal con Lagrangiano aumentado y recursión estilo Featherstone (sin versión arXiv). |
| 11 | Characterizing the Uncertainty of Jointly Distributed Poses in the Lie Algebra | Joshua G. Mangelson, Maani Ghaffari, Ram Vasudevan et al. | 2019 | [arXiv:1906.07795](https://arxiv.org/abs/1906.07795) | **H2.** Propaga covarianzas de poses correlacionadas en se(3), justo lo que necesita la cadena cámara-muñeca-objeto-pinza con errores de calibración compartidos. |
| 12 | A Code for Unscented Kalman Filtering on Manifolds (UKF-M) | Martin Brossard, Axel Barrau, Silvere Bonnabel | 2020 | [arXiv:2002.00878](https://arxiv.org/abs/2002.00878) | **H2.** UKF genérico en variedades mediante retracciones y sin Jacobianos, con código Python listo para filtrar la pose del efector o de los objetos. |
| 13 | Contact-Aided Invariant Extended Kalman Filtering for Robot State Estimation | Ross Hartley, Maani Ghaffari, Ryan M. Eustice et al. | 2019 | [arXiv:1904.09251](https://arxiv.org/abs/1904.09251) | **H2.** Extiende el EKF invariante de Barrau2017 usando la cinemática directa como medida en un grupo de Lie matricial, plantilla directa para fusionar encoders y cámara. |
| 14 | Invariant Stochastic Filtering on SE(3) for Inertial-Encoder State Estimation of Serial Rigid Manipulators | S. Yaqubi, J. Mattila | 2026 | [arXiv:2607.00026](https://arxiv.org/abs/2607.00026) | **H2.** Aplica el IEKF en SE(3) eslabón a eslabón a brazos seriales con garantías de estabilidad, el caso exacto de un manipulador de laboratorio. |
| 15 | Riemannian Score-Based Generative Modelling | Valentin De Bortoli, Emile Mathieu, Michael Hutchinson et al. | 2022 | [arXiv:2202.02763](https://arxiv.org/abs/2202.02763) | **H2.** Fundamento teórico de la difusión por score en variedades compactas como SO(3), base de los generadores de agarres y acciones del corpus. |
| 16 | Riemannian Diffusion Models | Chin-Wei Huang, Milad Aghajohari, Avishek Joey Bose et al. | 2022 | [arXiv:2208.07949](https://arxiv.org/abs/2208.07949) | **H2.** Da la formulación variacional (ELBO en tiempo continuo) de la difusión en variedades, complementaria a la visión por score. |
| 17 | SE(3) diffusion model with application to protein backbone generation | Jason Yim, Brian L. Trippe, Valentin De Bortoli et al. | 2023 | [arXiv:2302.02277](https://arxiv.org/abs/2302.02277) | **H2.** Receta de referencia para difundir poses rígidas en SE(3) con ruido IGSO(3) y score cerrada en so(3), trasladable a poses de pinza. |
| 18 | Confronting Ambiguity in 6D Object Pose Estimation via Score-Based Diffusion on SE(3) | Tsu-Ching Hsiao, Hao-Wei Chen, Hsuan-Kung Yang et al. | 2023 | [arXiv:2305.15873](https://arxiv.org/abs/2305.15873) | **H2.** Difusión en SE(3) para pose 6D ambigua de objetos simétricos, relevante para frascos y tapones de revolución del laboratorio. |
| 19 | Flow Matching on Lie Groups | Finn M. Sherry, Bart M. N. Smets | 2025 | [arXiv:2504.00494](https://arxiv.org/abs/2504.00494) | **H2.** Generaliza el flow matching a grupos de Lie con curvas exponenciales, sin simulación, para generar agarres o acciones en SE(3). |
| 20 | Fast Generative Grasping via Lie Group-Constrained MeanFlow | S. Talha Bukhari, Yi Wei, Ruiqi Ni et al. | 2026 | [arXiv:2608.26076](https://arxiv.org/abs/2608.26076) | **H2.** Genera agarres en SO(3)xR3 con 5 o menos evaluaciones de red, lo que permite replanificar agarres en bucle cerrado en tiempo real. |
| 21 | Neural Manifold Ordinary Differential Equations | Aaron Lou, Derek Lim, Isay Katsman et al. | 2020 | [arXiv:2006.10254](https://arxiv.org/abs/2006.10254) | **H2.** Flujos continuos (ODE) definidos en cartas de la variedad: densidades exactas en $S^2$, $SO(3)$ o espacios hiperbólicos, precursor de los flujos riemannianos usados para poses. |
| 22 | Information Theoretic Model Predictive Control: Theory and Applications to Autonomous Driving | Grady Williams, Paul Drews, Brian Goldfain et al. | 2017 | [arXiv:1707.02342](https://arxiv.org/abs/1707.02342) | **H3.** Derivación fundacional de MPPI por energía libre y KL, base de todo el MPC por muestreo aplicable al brazo. |
| 23 | STORM: An Integrated Framework for Fast Joint-Space Model-Predictive Control for Reactive Manipulation | Mohak Bhardwaj, Balakumar Sundaralingam, Arsalan Mousavian et al. | 2021 | [arXiv:2104.13542](https://arxiv.org/abs/2104.13542) | **H3.** MPC por muestreo en espacio articular y en GPU para manipuladores, con colisión, límites y manipulabilidad como costes. |
| 24 | Sampling-based Model Predictive Control Leveraging Parallelizable Physics Simulations | Corrado Pezzato, Chadi Salmi, Elia Trevisan et al. | 2023 | [arXiv:2307.09105](https://arxiv.org/abs/2307.09105) | **H3.** Usa un simulador físico paralelo como modelo de MPPI, receta trasladable a MuJoCo/MJX para tareas con contacto en AutoBio. |
| 25 | Model Predictive Path Integral Control as Preconditioned Gradient Descent | Mahyar Fazlyab, Sina Sharifi, Jiarui Wang | 2026 | [arXiv:2603.24489](https://arxiv.org/abs/2603.24489) | **H3.** Demuestra que la actualización de MPPI es un paso de gradiente precondicionado, puente formal entre gradientes covariantes y gradiente natural. |
| 26 | Continuous-Time Gaussian Process Motion Planning via Probabilistic Inference | Mustafa Mukadam, Jing Dong, Xinyan Yan et al. | 2017 | [arXiv:1707.07383](https://arxiv.org/abs/1707.07383) | **H3.** GPMP2 formula la planificación como inferencia con prior GP y Gauss-Newton disperso, sustituto con PDF de la familia CHOMP/TrajOpt. |
| 27 | Accelerating Motion Planning via Optimal Transport | An T. Le, Georgia Chalvatzaki, Armin Biess et al. | 2023 | [arXiv:2309.15970](https://arxiv.org/abs/2309.15970) | **H3.** Sinkhorn Step: optimización de orden cero por lotes de trayectorias suaves en alta dimensión, alternativa paralela a STOMP. |
| 28 | Motion Planning Diffusion: Learning and Planning of Robot Motions with Diffusion Models | Joao Carvalho, An T. Le, Mark Baierl et al. | 2023 | [arXiv:2308.01557](https://arxiv.org/abs/2308.01557) | **H3.** Usa difusión como prior de trayectorias y muestrea la posterior guiada por costes, uniendo planificación y modelos generativos. |
| 29 | DiffusionSeeder: Seeding Motion Optimization with Diffusion for Rapid Motion Planning | Huang Huang, Balakumar Sundaralingam, Arsalan Mousavian et al. | 2024 | [arXiv:2410.16727](https://arxiv.org/abs/2410.16727) | **H3.** Difusión condicionada a profundidad que siembra cuRobo, vínculo directo entre el pipeline de visión y el optimizador de trayectorias. |
| 30 | Geometric Impedance Control on SE(3) for Robotic Manipulators | Joohwan Seo, Nikhil Potu Surya Prakash, Alexander Rose et al. | 2022 | [arXiv:2211.07945](https://arxiv.org/abs/2211.07945) | **H3.** Control de impedancia con potencial invariante a izquierda en SE(3) para ejecutar trayectorias con contacto seguro. |
| 31 | Stein Variational Ergodic Surface Coverage with SE(3) Constraints | Jiayun Li, Yufeng Jin, Sangli Teng et al. | 2026 | [arXiv:2603.09458](https://arxiv.org/abs/2603.09458) | **H3.** SVGD precondicionado con partículas en SE(3), ejemplo reciente de optimización de trayectorias por muestreo nativa en el grupo de Lie. |
| 32 | Batch Nonlinear Continuous-Time Trajectory Estimation as Exactly Sparse Gaussian Process Regression | Sean Anderson, Timothy D. Barfoot, Chi Hay Tong et al. | 2014 | [arXiv:1412.0630](https://arxiv.org/abs/1412.0630) | **H3.** Prior GP de trayectoria en tiempo continuo con estructura tridiagonal por bloques; es la base matemática de GPMP/GPMP2 y del STEAM de Barfoot en $SE(3)$. |
| 33 | Overcoming catastrophic forgetting in neural networks | James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz et al. | 2016 | [arXiv:1612.00796](https://arxiv.org/abs/1612.00796) | **H4.** EWC: penalización cuadrática ponderada por la Fisher diagonal que ancla el fine-tuning al modelo base y evita olvidar las habilidades preentrenadas. |
| 34 | Merging Models with Fisher-Weighted Averaging | Michael Matena, Colin Raffel | 2021 | [arXiv:2111.09832](https://arxiv.org/abs/2111.09832) | **H4.** Fusiona modelos o adaptadores de tarea con una media ponderada por la Fisher, útil para combinar LoRA por subtarea del laboratorio. |
| 35 | Mirror Descent Policy Optimization | Manan Tomar, Lior Shani, Yonathan Efroni et al. | 2020 | [arXiv:2005.09814](https://arxiv.org/abs/2005.09814) | **H4.** Formula el RL de políticas como descenso espejo con KL como divergencia de Bregman y unifica TRPO y PPO en ese marco. |
| 36 | Old Optimizer, New Norm: An Anthology | Jeremy Bernstein, Laker Newhouse | 2024 | [arXiv:2409.20325](https://arxiv.org/abs/2409.20325) | **H4.** Reinterpreta Adam, Shampoo y Prodigy como descenso más pronunciado bajo normas concretas, la base teórica de elegir la geometría de cada paso. |
| 37 | Muon is Scalable for LLM Training | Jingyuan Liu, Jianlin Su, Xingcheng Yao et al. | 2025 | [arXiv:2502.16982](https://arxiv.org/abs/2502.16982) | **H4.** Escala Muon (descenso por gradiente ortogonalizado, norma espectral) con decaimiento de pesos y ajuste de escala, unas 2x más eficiente que AdamW. |
| 38 | SOAP: Improving and Stabilizing Shampoo using Adam | Nikhil Vyas, Depen Morwani, Rosie Zhao et al. | 2024 | [arXiv:2409.11321](https://arxiv.org/abs/2409.11321) | **H4.** Demuestra que Shampoo equivale a Adafactor en la base propia del precondicionador y propone correr Adam en esa base, heredero práctico de Shampoo y K-FAC. |
| 39 | Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success | Moo Jin Kim, Chelsea Finn, Percy Liang | 2025 | [arXiv:2502.19645](https://arxiv.org/abs/2502.19645) | **H4.** OpenVLA-OFT: receta de fine-tuning de VLA con acciones continuas, chunks, decodificación paralela y pérdida L1, validada en ALOHA bimanual. |
| 40 | SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning | Haozhan Li, Yuxin Zuo, Jiale Yu et al. | 2025 | [arXiv:2509.09674](https://arxiv.org/abs/2509.09674) | **H4.** RL con recompensa de resultado sobre OpenVLA-OFT que supera al SFT y descubre comportamientos nuevos, una vía para ir más allá de las demostraciones. |
| 41 | $\pi_\texttt{RL}$: Online RL Fine-tuning for Flow-based Vision-Language-Action Models | Kang Chen, Zhihao Liu, Tonghe Zhang et al. | 2025 | [arXiv:2510.25889](https://arxiv.org/abs/2510.25889) | **H4.** Extiende DPPO y ReinFlow a VLA de flujo (pi0, pi0.5) con Flow-Noise y Flow-SDE para obtener log-verosimilitudes tratables en RL online. |
| 42 | ET-SEED: Efficient Trajectory-Level SE(3) Equivariant Diffusion Policy | Chenrui Tie, Yue Chen, Ruihai Wu et al. | 2024 | [arXiv:2411.03990](https://arxiv.org/abs/2411.03990) | **H4.** Política de difusión equivariante en SE(3) a nivel de trayectoria que aprende con pocas demostraciones, de modo que el fine-tuning no tiene que reaprender la simetría. |
| 43 | Diffusion-EDFs: Bi-equivariant Denoising Generative Modeling on SE(3) for Visual Robotic Manipulation | Hyunwoo Ryu, Jiwoo Kim, Hyunseok An et al. | 2023 | [arXiv:2309.02685](https://arxiv.org/abs/2309.02685) | **H4.** Difusión bi-equivariante en $SE(3)$ (respecto a la escena y a la pinza) sobre campos de descriptores; aprende pick-and-place con 5-10 demostraciones. |
| 44 | Certifiably Optimal Monocular Hand-Eye Calibration | Emmett Wise, Matthew Giamou, Soroush Khoubyarian et al. | 2020 | [arXiv:2005.08298](https://arxiv.org/abs/2005.08298) | **H5.** Relajación SDP de la calibración mano-ojo con escala desconocida y certificado de optimalidad global, complemento riguroso de Park-Martin. |
| 45 | A Certifably Correct Algorithm for Generalized Robot-World and Hand-Eye Calibration | Emmett Wise, Pushyami Kaveti, Qilong Chen et al. | 2025 | [arXiv:2507.23045](https://arxiv.org/abs/2507.23045) | **H5.** Resuelve AX=YB con varios sensores y patrones con garantías globales y criterios de identificabilidad para planificar las poses de calibración. |
| 46 | Optimal Uncertainty-Aware Calibration for the AX=YB Problem | Yanjia Chen, Xiangfei Li, Huan Zhao et al. | 2026 | [arXiv:2605.04809](https://arxiv.org/abs/2605.04809) | **H5.** Iteración en el álgebra de Lie para AX=YB que repondera según la incertidumbre relativa entre cinemática y visión. |
| 47 | Markerless Camera-to-Robot Pose Estimation via Self-supervised Sim-to-Real Transfer | Jingpei Lu, Florian Richter, Michael C. Yip | 2023 | [arXiv:2302.14332](https://arxiv.org/abs/2302.14332) | **H5.** CtRNet estima el extrínseco cámara-robot sin marcadores con keypoints y PnP, autosupervisado con renderizado diferenciable de siluetas. |
| 48 | Differentiable Robot Rendering | Ruoshi Liu, Alper Canberk, Shuran Song et al. | 2024 | [arXiv:2410.13851](https://arxiv.org/abs/2410.13851) | **H5.** Modelo Gaussian Splatting del robot diferenciable respecto a sus parámetros de control, útil para recuperar pose y calibrar desde píxeles. |
| 49 | Kalib: Easy Hand-Eye Calibration with Reference Point Tracking | Tutian Tang, Minghao Liu, Wenqiang Xu et al. | 2024 | [arXiv:2408.10562](https://arxiv.org/abs/2408.10562) | **H5.** Calibración sin marcadores ni reentrenamiento que sigue un punto del robot con un modelo fundacional y resuelve PnP con la cinemática. |
| 50 | ARC-Calib: Autonomous Markerless Camera-to-Robot Calibration via Exploratory Robot Motions | Podshara Chanrungmaneekul, Yiting Chen, Joshua T. Grace et al. | 2025 | [arXiv:2503.14701](https://arxiv.org/abs/2503.14701) | **H5.** Calibración autónoma basada en modelo que explota restricciones de coplanaridad y colinealidad de movimientos exploratorios del brazo. |
| 51 | CNS: Correspondence Encoded Neural Image Servo Policy | Anzhe Chen, Hongxiang Yu, Yue Wang et al. | 2023 | [arXiv:2309.09047](https://arxiv.org/abs/2309.09047) | **H5.** Servo visual con GNN sobre grafos de correspondencias, entrenado solo en simulación y transferido sin ajuste al robot real. |
| 52 | ViT-VS: On the Applicability of Pretrained Vision Transformer Features for Generalizable Visual Servoing | Alessandro Scherl, Stefan Thalhammer, Bernhard Neuberger et al. | 2025 | [arXiv:2503.04545](https://arxiv.org/abs/2503.04545) | **H5.** IBVS con features DINOv2 preentrenadas que no necesita entrenamiento por tarea y es candidato directo para la aproximación fina con cámara de muñeca. |
| 53 | Exponentially Stable First Order Control on Matrix Lie Groups | Valmik Prabhu, Amay Saxena, S. Shankar Sastry | 2020 | [arXiv:2004.00239](https://arxiv.org/abs/2004.00239) | **H5.** Controlador de velocidad cartesiana en grupos de Lie matriciales con convergencia exponencial global en SE(n), base teórica de la ley PBVS con Log. |
| 54 | Only Bayes should learn a manifold (on the estimation of differential geometric structure from data) | Søren Hauberg | 2018 | [arXiv:1806.04994](https://arxiv.org/abs/1806.04994) | **H6.** Demuestra que solo los modelos probabilísticos recuperan la geometría diferencial de la variedad de datos, lo que justifica las métricas pullback con incertidumbre para geodésicas de movimiento. |
| 55 | Pulling back information geometry | Georgios Arvanitidis, Miguel González-Duque, Alison Pouplin et al. | 2021 | [arXiv:2106.05367](https://arxiv.org/abs/2106.05367) | **H6.** Tira hacia atrás la métrica de Fisher-Rao al latente para cualquier decodificador y une la geometría latente con el gradiente natural del corpus. |
| 56 | Metrics for Deep Generative Models | Nutan Chen, Alexej Klushyn, Richard Kurle et al. | 2017 | [arXiv:1711.01204](https://arxiv.org/abs/1711.01204) | **H6.** Calcula geodésicas en el latente de modelos generativos y las aplica a la generalización de movimientos de un brazo robótico. |
| 57 | Intrinsic dimension of data representations in deep neural networks | Alessio Ansuini, Alessandro Laio, Jakob H. Macke et al. | 2019 | [arXiv:1905.12784](https://arxiv.org/abs/1905.12784) | **H6.** Estima con TwoNN la dimensión intrínseca de cada capa y da una herramienta para dimensionar latentes de políticas y codificadores visuales. |
| 58 | Neural Manifolds for the Control of Movement | Juan A. Gallego, Matthew G. Perich, Lee E. Miller et al. | 2017 | [doi](https://doi.org/10.1016/j.neuron.2017.05.025) | **H6.** Marco de referencia de las variedades neuronales motoras: pocos modos neuronales cuya dinámica genera el movimiento del brazo, análogo a las sinergias robóticas. |
| 59 | LFADS - Latent Factor Analysis via Dynamical Systems | David Sussillo, Rafal Jozefowicz, L. F. Abbott et al. | 2016 | [arXiv:1608.06315](https://arxiv.org/abs/1608.06315) | **H6.** VAE secuencial que infiere la dinámica latente de poblaciones motoras durante el alcance y sirve de plantilla para modelos de dinámica latente del robot. |
| 60 | Learnable latent embeddings for joint behavioral and neural analysis | Steffen Schneider, Jin Hwa Lee, Mackenzie Weygandt Mathis | 2022 | [arXiv:2204.00673](https://arxiv.org/abs/2204.00673) | **H6.** CEBRA obtiene embeddings contrastivos consistentes entre sesiones y sujetos, una idea trasladable a alinear latentes entre simulación y realidad. |
| 61 | Adversarial Domain Adaptation for Stable Brain-Machine Interfaces | Ali Farshchian, Juan A. Gallego, Joseph P. Cohen et al. | 2018 | [arXiv:1810.00045](https://arxiv.org/abs/1810.00045) | **H6.** Estabiliza un decodificador de BMI alineando la variedad latente entre días con CCA, KL o redes adversarias, equivalente neuronal de la adaptación sim-to-real. |
| 62 | Learning Latent Actions to Control Assistive Robots | Dylan P. Losey, Hong Jun Jeon, Mengxi Li et al. | 2021 | [arXiv:2107.02907](https://arxiv.org/abs/2107.02907) | **H6.** Aprende acciones latentes de baja dimensión condicionadas al estado para controlar un brazo de 7 grados de libertad con un joystick de 2, versión robótica del control por la variedad. |
| 63 | Learning Action Manifold with Multi-view Latent Priors for Robotic Manipulation | Junjin Xiao, Dongyang Li, Yandan Yang et al. | 2026 | [arXiv:2605.11832](https://arxiv.org/abs/2605.11832) | **H6.** Trabajo de 2026 que hace que una VLA prediga acciones directamente sobre la variedad de acciones válidas, la hipótesis de la variedad aplicada a la cabeza de acción. |
| 64 | Neural population geometry: An approach for understanding biological and artificial neural networks | SueYeon Chung, L. F. Abbott | 2021 | [arXiv:2104.07059](https://arxiv.org/abs/2104.07059) | **H6.** Revisión que unifica la geometría de poblaciones (capacidad de variedades, dimensión, desenmarañamiento) en corteza y en redes profundas; el puente teórico que faltaba entre neurociencia y deep learning. |
| 65 | The geometry of hidden representations of large transformer models | Lucrezia Valeriani, Diego Doimo, Francesca Cuturello et al. | 2023 | [arXiv:2302.00294](https://arxiv.org/abs/2302.00294) | **H6.** Mide dimensión intrínseca capa a capa en transformers: expansión, contracción y meseta semántica; guía para elegir de qué capa extraer rasgos de un ViT/VLA. |
| 66 | A Practical Method for Constructing Equivariant Multilayer Perceptrons for Arbitrary Matrix Groups | Marc Finzi, Max Welling, Andrew Gordon Wilson | 2021 | [arXiv:2104.09459](https://arxiv.org/abs/2104.09459) | **H6.** EMLP: resuelve las restricciones de equivarianza con los generadores del álgebra de Lie para cualquier grupo matricial ($SO(3)$, $SE(3)$, $O(1,3)$), sin derivar la teoría de representaciones a mano. |
| 67 | Lie Neurons: Adjoint-Equivariant Neural Networks for Semisimple Lie Algebras | Tzu-Yuan Lin, Minghan Zhu, Maani Ghaffari | 2023 | [arXiv:2310.04521](https://arxiv.org/abs/2310.04521) | **H6.** Redes cuyas entradas y salidas son elementos del álgebra de Lie y que son equivariantes a la acción adjunta; procesan twists y transformaciones como datos. |
| 68 | Normalized Object Coordinate Space for Category-Level 6D Object Pose and Size Estimation | He Wang, Srinath Sridhar, Jingwei Huang et al. | 2019 | [arXiv:1901.02970](https://arxiv.org/abs/1901.02970) | **H7.** Introduce la pose y el tamaño por categoría (NOCS, CAMERA, REAL275), clave para frascos de 6 tamaños sin CAD por instancia. |
| 69 | 6-PACK: Category-level 6D Pose Tracker with Anchor-Based Keypoints | Chen Wang, Roberto Martín-Martín, Danfei Xu et al. | 2019 | [arXiv:1910.10750](https://arxiv.org/abs/1910.10750) | **H7.** Seguimiento 6D en tiempo real a nivel de categoría mediante puntos clave, útil para seguir frascos durante el transporte y el vertido. |
| 70 | GenPose: Generative Category-level Object Pose Estimation via Diffusion Models | Jiyao Zhang, Mingdong Wu, Hao Dong | 2023 | [arXiv:2306.10531](https://arxiv.org/abs/2306.10531) | **H7.** Plantea la pose por categoría como difusión condicional con múltiples hipótesis, adecuada para objetos casi simétricos como los frascos. |
| 71 | DiffusionNOCS: Managing Symmetry and Uncertainty in Sim2Real Multi-Modal Category-level Pose Estimation | Takuya Ikeda, Sergey Zakharov, Tianyi Ko et al. | 2024 | [arXiv:2402.12647](https://arxiv.org/abs/2402.12647) | **H7.** Demuestra pose por categoría entrenada solo con datos sintéticos que generaliza a datos reales, lo que respalda el pipeline sim-to-real con AutoBio. |
| 72 | TransNet: Transparent Object Manipulation Through Category-Level Pose Estimation | Huijie Zhang, Anthony Opipari, Xiaotong Chen et al. | 2023 | [arXiv:2307.12400](https://arxiv.org/abs/2307.12400) | **H7.** Une la pose por categoría con los objetos transparentes e incluye pick-and-place y vertido robótico con vasos. |
| 73 | Vision-based robot manipulation of transparent liquid containers in a laboratory setting | Daniel Schober, Ronja Güldenring, James Love et al. | 2024 | [arXiv:2404.16529](https://arxiv.org/abs/2404.16529) | **H7.** Estima el volumen de líquido por visión y vierte guiado por simulación con un UR5 en un laboratorio real, con el dataset LabLiquidVolume. |
| 74 | LabUtopia: High-Fidelity Simulation and Hierarchical Benchmark for Scientific Embodied Agents | Rui Li, Zixuan Hu, Wenxi Qu et al. | 2025 | [arXiv:2505.22634](https://arxiv.org/abs/2505.22634) | **H7.** Simulador y benchmark jerárquico de laboratorio (30 tareas, más de 200 activos), comparable a AutoBio y Chemistry3D. |
| 75 | ORGANA: A Robotic Assistant for Automated Chemistry Experimentation and Characterization | Kourosh Darvish, Marta Skreta, Yuchi Zhao et al. | 2024 | [arXiv:2401.06949](https://arxiv.org/abs/2401.06949) | **H7.** Sistema real de química robótica con LLM y realimentación visual que sirve de referencia de extremo a extremo para la automatización de laboratorio. |
| 76 | Closed-Loop Robotic Manipulation of Transparent Substrates for Self-Driving Laboratories using Deep Learning Micro-Error Correction | Kelsey Fontenot, Anjali Gorti, Iva Goel et al. | 2025 | [arXiv:2512.06038](https://arxiv.org/abs/2512.06038) | **H7.** Muestra la corrección de errores por visión en lazo cerrado para vidrio transparente en un self-driving lab (98,5 % de colocaciones correctas al primer intento). |
| 77 | Towards Robotic Laboratory Automation Plug & Play: The "LAPP" Framework | Ádám Wolf, David Wolton, Josef Trapl et al. | 2021 | [arXiv:2106.10129](https://arxiv.org/abs/2106.10129) | **H7.** Es la referencia citable sobre lectura de códigos de barras y marcadores fiduciales para identificar y localizar equipos en un laboratorio robotizado. |
| 78 | Orbit: A Unified Simulation Framework for Interactive Robot Learning Environments | Mayank Mittal, Calvin Yu, Qinxi Yu et al. | 2023 | [arXiv:2301.04195](https://arxiv.org/abs/2301.04195) | **H7.** Artículo de referencia de Isaac Lab (antes Orbit): entornos de manipulación, sensores y aprendizaje paralelo en GPU; base del port IsaacLab-mlx del equipo. |
