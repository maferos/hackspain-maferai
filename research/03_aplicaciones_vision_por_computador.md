# Parte 3 — Aplicaciones a la visión por computador

> **Proyecto:** MAFER challenge (hackspain-maferai). Escena MuJoCo de laboratorio basada en AutoBio (brazo ALOHA, GC-MS, espectrofotómetro UV-Vis-NIR, gradilla de tubos, zonas de *spawn* donde un operario deja tubos de 50 ml).
> **Objetivo global:** modelar y ajustar (*fine-tune*) el movimiento del brazo usando teoría de grupos de Lie, geometría del espacio tangente, gradiente natural y geometría de variedades neuronales, **aplicado a través de la visión por computador**.
>
> Este documento es la **parte 3 de 3**. No repite la teoría:
> - [`01_matematicas_grupos_de_lie.md`](01_matematicas_grupos_de_lie.md): $SO(3)$, $SE(3)$, $\exp/\log$, $\mathrm{Ad}$, Jacobianos izquierdo/derecho, notación $\oplus/\ominus$.
> - [`02_optimizacion_y_algoritmos.md`](02_optimizacion_y_algoritmos.md): Gauss-Newton/Levenberg-Marquardt en variedades, retracciones, gradiente natural, Fisher, optimizadores riemannianos.
>
> Aquí se usan esas herramientas sin volver a derivarlas y el foco está en **cómo aparecen en la percepción visual y en el control guiado por visión**, y en **qué construir en este repositorio**.

**Convenciones.** $T=(R,t)\in SE(3)$; $\xi=(\rho,\phi)\in\mathfrak{se}(3)\cong\mathbb{R}^6$ (primero la traslación y luego la rotación); $\mathrm{Exp}:\mathbb{R}^6\to SE(3)$ y $\mathrm{Log}$ son su inversa (local); $[\,\cdot\,]_\times$ es la matriz antisimétrica. ${}^{a}T_{b}$ expresa el sistema $b$ en el sistema $a$. Salvo que se diga lo contrario, las perturbaciones son **por la izquierda**: $T\leftarrow \mathrm{Exp}(\delta)\,T$.

---

## Índice

1. Geometría de cámara sobre grupos de Lie
2. Estimación de pose 6D de objetos (y objetos transparentes de laboratorio)
3. Servo visual (*visual servoing*)
4. SLAM / odometría visual sobre grupos de Lie
5. Visión equivariante para manipulación
6. Políticas visuomotoras y *vision-language-action* (VLA)
7. Variedades neuronales en visión
8. Propuesta concreta para este proyecto
9. Bibliografía comentada

---

## 1. Geometría de cámara sobre grupos de Lie

### 1.1 Intuición

Una cámara es un **sistema de referencia rígido** que se mueve por el espacio, así que su pose es un elemento de $SE(3)$. Todo lo que hace la visión geométrica clásica (calibración, PnP, *bundle adjustment*, SLAM, calibración mano-ojo) consiste en **estimar elementos de $SE(3)$ a partir de residuos en píxeles**. Como $SE(3)$ no es un espacio vectorial, la forma correcta de optimizar es linealizar en el **espacio tangente** ($\mathfrak{se}(3)\cong\mathbb{R}^6$), resolver un problema lineal de 6 incógnitas por pose y volver a la variedad con $\mathrm{Exp}$ (retracción). Es exactamente el esquema de la parte 2, aplicado a la función de proyección.

### 1.2 Modelo pinhole e intrínsecos en MuJoCo

Un punto del mundo $X_w$ se pasa al sistema de la cámara con ${}^{c}T_{w}$ y después se proyecta:

$$
p_c = {}^{c}T_{w}\,X_w = R\,X_w + t,\qquad
\pi(p_c) = \begin{pmatrix} f_x\, X_c/Z_c + c_x \\ f_y\, Y_c/Z_c + c_y\end{pmatrix}.
$$

En MuJoCo una `<camera>` definida con `fovy` y `resolution="W H"` tiene intrínsecos

$$
f_y = \frac{H/2}{\tan(\mathrm{fovy}/2)},\qquad f_x=f_y\ (\text{píxeles cuadrados}),\qquad (c_x,c_y)=(W/2,\,H/2).
$$

Si la cámara se define con `focal` y `sensorsize` (como la `wrist_cam` del UR5e en AutoBio), entonces $f_x = \text{focal}_x\cdot W/\text{sensorsize}_x$ y lo mismo en $y$. **Ojo:** las cámaras de MuJoCo miran hacia $-z$ con $+y$ hacia arriba (convención OpenGL). Para pasar a la convención OpenCV ($+z$ hacia delante y $+y$ hacia abajo) hay que multiplicar por $\mathrm{diag}(1,-1,-1)$. Este es el error más habitual al conectar un estimador de pose (que siempre trabaja en convención OpenCV) con MuJoCo.

### 1.3 Jacobiano de la proyección respecto a una perturbación tangente

Perturbamos la pose de la cámara por la izquierda, ${}^{c}T_w \leftarrow \mathrm{Exp}(\delta)\,{}^{c}T_w$ con $\delta=(\rho,\phi)$. A primer orden, $\mathrm{Exp}(\delta)p_c \approx p_c + \rho + \phi\times p_c = p_c + \rho - [p_c]_\times \phi$, así que

$$
\frac{\partial p_c}{\partial \delta}\Big|_{\delta=0} = \begin{bmatrix} I_3 & -[p_c]_\times \end{bmatrix}\in\mathbb{R}^{3\times 6},
\qquad
\frac{\partial \pi}{\partial p_c} = \begin{bmatrix} f_x/Z & 0 & -f_x X/Z^2\\ 0 & f_y/Z & -f_y Y/Z^2\end{bmatrix}.
$$

El Jacobiano de reproyección (de tamaño $2\times 6$) es la regla de la cadena:

$$
J_\delta = \frac{\partial \pi}{\partial p_c}\begin{bmatrix} I_3 & -[p_c]_\times \end{bmatrix}.
$$

Respecto al punto 3D, $\partial \pi/\partial X_w = (\partial\pi/\partial p_c)\,R$. Estas son las matrices que rellenan los bloques de la matriz de Gauss-Newton del *bundle adjustment*. Con perturbación por la derecha ($T\,\mathrm{Exp}(\delta)$) el Jacobiano cambia por $\mathrm{Ad}_T$ (ver parte 1).

### 1.4 *Bundle adjustment* (BA) en la variedad

Con cámaras $\{T_i\}$, puntos $\{X_j\}$ y observaciones $u_{ij}$:

$$
\min_{\{T_i\},\{X_j\}} \sum_{(i,j)} \rho\!\left(\big\| u_{ij} - \pi(T_i X_j)\big\|^2_{\Sigma_{ij}^{-1}}\right).
$$

Cada iteración de Gauss-Newton/LM resuelve $(J^\top W J + \lambda D)\,\Delta = -J^\top W r$, con $\Delta = (\delta_1,\dots,\delta_N, \Delta X_1,\dots)$. Después se **retrae**: $T_i\leftarrow \mathrm{Exp}(\delta_i)T_i$ y $X_j\leftarrow X_j+\Delta X_j$. La estructura dispersa (bloques $6\times 6$ de cámaras y $3\times3$ de puntos) permite eliminar los puntos con el **complemento de Schur**. La variante *object-level BA* de CosyPose cambia los puntos por **poses de objetos** $\in SE(3)$ y es la que interesa si tenemos varias cámaras mirando la misma gradilla (sección 2). La variante *dense BA* de DROID-SLAM usa como residuos flujos ópticos densos (sección 4). Bibliotecas: `lietorch` (Teed & Deng, CVPR 2021) y `PyPose` (Wang et al., 2022) implementan $\mathrm{Exp}/\mathrm{Log}$ y la retropropagación en el tangente sobre PyTorch.

### 1.5 Calibración mano-ojo $AX=XB$

**Problema.** Cámara montada en la muñeca (*eye-in-hand*): $X={}^{e}T_{c}$ (efector→cámara), desconocida. Para dos poses $k,l$ del robot se miden el movimiento relativo del efector $A={}^{e_k}T_{e_l}$ (por cinemática directa) y el de la cámara $B={}^{c_k}T_{c_l}$ (por PnP sobre un patrón o por un estimador de pose). La cadena cerrada da

$$
A\,X = X\,B,\qquad A,B,X\in SE(3).
$$

Para cámara fija (*eye-to-hand*, como `table_cam_front`) la ecuación es la misma con $X={}^{b}T_{c}$ y $A$ construida con las inversas.

**Park & Martin (1994), en el álgebra de Lie.** La parte rotacional es $R_A R_X = R_X R_B$, es decir, $R_B = R_X^\top R_A R_X$. Tomando $\log$ y usando $\log(R^\top S R) = R^\top \log(S)\,R$:

$$
\alpha = R_X\,\beta,\qquad \alpha=\log(R_A)^\vee,\ \beta=\log(R_B)^\vee\in\mathbb{R}^3 .
$$

La calibración queda reducida a **alinear dos nubes de vectores del álgebra**, un problema de Procrustes ortogonal. Con $n\ge 2$ pares no paralelos:

$$
M = \sum_{i}\beta_i\,\alpha_i^\top,\qquad R_X = (M^\top M)^{-1/2}\,M^\top,
$$

y la traslación sale por mínimos cuadrados lineales de $(R_{A_i}-I)\,t_X = R_X t_{B_i} - t_{A_i}$.
**Tsai & Lenz (1989)** resuelven primero la rotación (con una parametrización eje-ángulo modificada) y luego la traslación, de forma parecida. Las dos variantes están en OpenCV (`cv::calibrateHandEye`, métodos `TSAI` y `PARK`).
**Moderno:** EasyHeC (Chen et al., RA-L 2023) evita los marcadores. Optimiza ${}^{b}T_{c}$ por **renderizado diferenciable** de la máscara del propio robot y elige automáticamente poses del brazo informativas.

**En simulación** la calibración es trivial (MuJoCo da `cam_xpos/cam_xmat`). Aun así, conviene **implementar Park-Martin y comprobarlo contra la verdad de simulación**, por tres motivos: (i) es el test de humo ideal de las utilidades de Lie de la parte 1; (ii) permite simular el error de calibración como ruido en $\mathfrak{se}(3)$ para la aleatorización de dominio; (iii) es lo que habrá que hacer en el robot real.

### 1.6 Calibración cámara-robot con incertidumbre

Si los residuos se modelan como gaussianos en el tangente, $X = \mathrm{Exp}(\epsilon)\bar X$ con $\epsilon\sim\mathcal{N}(0,\Sigma)$, la covarianza de la calibración se propaga a la pose del objeto en la base del robot con los adjuntos:
${}^{b}T_o = {}^{b}T_c\,{}^{c}T_o \Rightarrow \Sigma_{b o}\approx \Sigma_{bc} + \mathrm{Ad}_{{}^{b}T_c}\,\Sigma_{co}\,\mathrm{Ad}_{{}^{b}T_c}^\top$. Así se fija de forma racional **cuánta precisión de pose hace falta** para agarrar un tubo de 50 ml con una pinza cuya holgura es de pocos milímetros.

---

## 2. Estimación de pose 6D de objetos

### 2.1 Intuición y taxonomía

Estimar la pose 6D es encontrar ${}^{c}T_o\in SE(3)$ de un objeto conocido (con CAD) o nuevo. Hay cuatro familias:

| Familia | Idea | Ejemplos |
|---|---|---|
| Regresión directa | La red predice $R$ (cuaternión/6D) y $t$ | PoseCNN |
| Correspondencias 2D-3D + PnP | La red predice puntos clave o coordenadas del objeto por píxel y $T$ se resuelve con PnP/RANSAC | PVNet, GDR-Net (PnP diferenciable "Patch-PnP") |
| RGB-D denso | Fusión de color y geometría por píxel más refinamiento iterativo | DenseFusion |
| *Render-and-compare* | Hipótesis → render → la red predice la corrección $\Delta T$ → iteración | CosyPose, MegaPose, FoundationPose |

La familia de *render-and-compare* es literalmente **un descenso en $SE(3)$**: $T_{k+1} = \mathrm{Exp}(\hat\xi_k)\,T_k$, donde $\hat\xi_k$ la predice una red a partir del par (imagen observada, imagen renderizada). Es la versión aprendida del Gauss-Newton de la sección 1.4.

### 2.2 Métodos clave

- **PoseCNN** (Xiang et al., 2017). Segmentación semántica, centro 2D más profundidad para $t$ y regresión de cuaternión para $R$. Introduce la pérdida **ShapeMatch** para objetos simétricos y el dataset YCB-Video.
- **DenseFusion** (Wang et al., CVPR 2019). Fusiona por píxel características RGB (CNN) y de la nube de puntos (PointNet). Predice una pose por píxel con confianza y añade un refinador iterativo. Es la referencia RGB-D clásica.
- **PVNet** (Peng et al., CVPR 2019). Cada píxel vota **vectores unitarios hacia puntos clave**. RANSAC da los puntos clave con incertidumbre y PnP da $T$. Es robusto a la oclusión y al truncamiento.
- **GDR-Net** (Wang et al., CVPR 2021). Predice mapas de coordenadas densas (*dense correspondences*) y una **Patch-PnP** aprendida que regresa $T$ directamente. Usa la **representación 6D** para la rotación y $t$ con escala invariante (SITE). GDRNPP ganó varias ediciones de BOP.
- **CosyPose** (Labbé et al., ECCV 2020). *Render-and-compare* iterativo más consistencia multivista con **BA a nivel de objeto** que refina a la vez cámaras y objetos.
- **MegaPose** (Labbé et al., CoRL 2022). Generaliza *render-and-compare* a **objetos nuevos** que solo tienen CAD: un clasificador de hipótesis gruesas y un refinador entrenados con datos sintéticos masivos.
- **SAM-6D** (Lin et al., CVPR 2024). *Zero-shot*: segmentación con SAM más un modelo de emparejamiento de nubes de puntos.
- **FoundationPose** (Wen et al., CVPR 2024). Modelo unificado de **estimación y seguimiento** para objetos nuevos. Funciona con CAD o con unas pocas imágenes de referencia (entonces reconstruye una representación implícita neuronal). Se entrena con datos sintéticos a gran escala, genera hipótesis, las refina con un transformer y las ordena con un *ranker* contrastivo. Fue n.º 1 en BOP (modelo conocido, objetos nuevos) en 2024. **Es la opción por defecto para este proyecto**, porque tenemos la malla exacta del tubo de 50 ml en los assets de AutoBio.

### 2.3 Representaciones de rotación y pérdidas

**Continuidad.** Zhou et al. (CVPR 2019) demuestran que toda representación de $SO(3)$ en $\mathbb{R}^d$ con $d\le 4$ (Euler, eje-ángulo, cuaternión) es **discontinua** como función inversa, lo que perjudica la regresión. La **representación 6D** (las dos primeras columnas de $R$) es continua. Se recupera $R$ con Gram-Schmidt:

$$
b_1=\frac{a_1}{\|a_1\|},\quad b_2=\frac{a_2-(b_1^\top a_2)b_1}{\|a_2-(b_1^\top a_2)b_1\|},\quad b_3=b_1\times b_2,\qquad R=[b_1\ b_2\ b_3].
$$

La alternativa de 9D más proyección SVD ($R=U\,\mathrm{diag}(1,1,\det UV^\top)V^\top$) también es continua.

**Pérdidas.**
- Geodésica (el ángulo de la rotación relativa, que es la métrica natural de $SO(3)$ vista en la parte 1):
$$ d(R_1,R_2)=\big\|\mathrm{Log}(R_1^\top R_2)\big\| = \arccos\!\frac{\mathrm{tr}(R_1^\top R_2)-1}{2}. $$
En la práctica conviene recortar el argumento del $\arccos$ a $[-1+\epsilon,\,1-\epsilon]$ (el gradiente explota en $0$ y en $\pi$) o usar la cordal $\|R_1-R_2\|_F^2 = 4(1-\cos d)$.
- **Point-matching / ADD** como pérdida: $\frac1m\sum_x\|(Rx+t)-(\hat Rx+\hat t)\|$, que acopla $R$ y $t$ en unidades físicas.
- **Simetrías:** mínimo sobre el grupo de simetría $\mathcal{S}$ del objeto, $\min_{S\in\mathcal{S}} d(R_1S, R_2)$. **Un tubo de centrífuga es casi $SO(2)$-simétrico alrededor de su eje** (salvo por la rosca y las marcas), así que la rotación en torno al eje no es observable. Hay que usar ADD-S o pérdidas "módulo simetría", o dejar de estimar una rotación completa y estimar **el eje** (un punto de $S^2$) más la posición.

### 2.4 Pose probabilística en $SO(3)$

Con simetrías y oclusiones la pose es **multimodal**. Hay tres modelos de densidad:

- **Bingham** sobre cuaterniones unitarios (antipodalmente simétrica, como exige $q\equiv -q$):
$p(q)\propto \exp(q^\top M Z M^\top q)$. Deep Bingham Networks (Deng et al., IJCV 2022) usan mezclas con varias hipótesis.
- **Fisher matricial** sobre $SO(3)$: $p(R\mid F)=\frac{1}{c(F)}\exp\!\big(\mathrm{tr}(F^\top R)\big)$, con $F\in\mathbb{R}^{3\times3}$ sin restricciones (homeomorfo a $\mathbb{R}^9$). Su moda es la proyección SVD de $F$. Mohlin et al. (NeurIPS 2020) regresan $F$ con NLL.
- **Implicit-PDF** (Murphy et al., ICML 2021): una red $f(x,R)\to\mathbb{R}$ da una densidad **no paramétrica**,
$$ p(R\mid x)\approx \frac{1}{V}\frac{\exp f(x,R)}{\sum_{i}\exp f(x,R_i)} $$
sobre una rejilla equivolumétrica de $SO(3)$ (HEALPix). Captura simetrías continuas (el tubo) como "anillos" de probabilidad.

**Relevancia aquí.** Una distribución (no un punto) permite (a) muestrear agarres robustos a la ambigüedad, (b) propagar la incertidumbre al servo visual y (c) usar la **información de Fisher** de la distribución de pose como métrica para el gradiente natural (parte 2).

### 2.5 Benchmark BOP y métricas

BOP (Hodaň et al.) unifica los datasets (LM-O, T-LESS, YCB-V, ITODD, HB, IC-BIN, TUD-L) y las métricas **VSD, MSSD y MSPD**, con recall medio $AR=\frac13(AR_{VSD}+AR_{MSSD}+AR_{MSPD})$. BOP 2023 añadió tareas de **objetos no vistos** con una fase de *onboarding* de 5 min. Métricas clásicas (se usan en §8):

$$
\mathrm{ADD}=\frac{1}{m}\sum_{x\in\mathcal{M}}\big\|(Rx+t)-(\hat Rx+\hat t)\big\|,\qquad
\mathrm{ADD\text{-}S}=\frac{1}{m}\sum_{x_1\in\mathcal{M}}\min_{x_2\in\mathcal{M}}\big\|(Rx_1+t)-(\hat Rx_2+\hat t)\big\|,
$$

y una pose se da por correcta si ADD(-S) $< 0.1\,\mathrm{diámetro}$. También se reportan el AUC de ADD-S hasta 10 cm (YCB-V), el error geodésico de rotación en grados y el error de traslación en mm.

### 2.6 Objetos transparentes de laboratorio

**Problema.** Los tubos, vasos y matraces de vidrio o plástico transparente **rompen los sensores de profundidad** (refracción y reflexión: la profundidad aparece vacía o es la del fondo) y tienen poca textura. Los métodos RGB-D ingenuos fallan.

- **ClearGrasp** (Sajjan et al., ICRA 2020). A partir de RGB-D predice normales, máscaras y bordes de oclusión y **completa la profundidad** por optimización global. Entrenado con datos sintéticos.
- **KeyPose** (Liu et al., CVPR 2020). Evita la profundidad: **estéreo RGB → puntos clave 3D** de objetos transparentes. Dataset de 15 objetos y 48 000 imágenes.
- **TransCG** (Fang et al., RA-L 2022). Dataset real de 57 715 imágenes RGB-D con profundidad de referencia (*ground truth*), más una red de completado de profundidad rápida y una demostración de agarre.
- **ClearPose** (Chen et al., ECCV 2022). Más de 350 000 fotogramas reales RGB-D con 63 objetos transparentes domésticos (incluye líquidos y oclusiones) y benchmark de pose.
- **TransNet** (2022). Pose de objetos transparentes a nivel de **categoría**.
- **LucidGrasp** (2024). Marco robótico para manipular **material de laboratorio con distintos grados de transparencia** y con líquido, mediante pose 6D.
- Revisión: *Robotic Perception of Transparent Objects: A Review* (arXiv 2304.00157).

**Hallazgo:** en esta investigación **no se ha encontrado ningún benchmark público de pose 6D específico de tubos de centrífuga en gradilla** que se parezca a esta escena. (Hay datasets recientes de material biomédico transparente, como TransBiolab, arXiv 2607.21071, que aparecen en la búsqueda pero no se han verificado en detalle.) Esto **justifica generar datos sintéticos propios en MuJoCo** (§8), aprovechando que la simulación da poses exactas gratis. En el renderizador nativo de MuJoCo la transparencia es solo *alpha blending* (no hay refracción). AutoBio incluye un **puente a Blender** con shaders PBR (transmisión e índice de refracción) justamente para los materiales transparentes, y debería usarse en la fase de *sim-to-real*.

---

## 3. Servo visual (*visual servoing*)

### 3.1 Intuición

El servo visual **cierra el lazo de control con la imagen**. En lugar de estimar una vez la pose del tubo y ejecutar una trayectoria abierta (que falla si la calibración o la pose tienen 5 mm de error), la cámara realimenta continuamente un error visual $e = s(t) - s^*$ y el controlador calcula una **velocidad del efector/cámara** $v=(\nu,\omega)\in\mathfrak{se}(3)$. Esa velocidad es, literalmente, un elemento del álgebra de Lie: el servo visual es **control en el espacio tangente**.

### 3.2 Matriz de interacción

Para un punto en coordenadas normalizadas $x=X/Z$, $y=Y/Z$ que se mueve por la velocidad de la cámara $v=(\nu,\omega)$:

$$
\dot s = L_s\,v,\qquad
L_x=\begin{bmatrix}
-\tfrac{1}{Z} & 0 & \tfrac{x}{Z} & xy & -(1+x^2) & y\\[2pt]
0 & -\tfrac{1}{Z} & \tfrac{y}{Z} & 1+y^2 & -xy & -x
\end{bmatrix}.
$$

Es el Jacobiano de la proyección de §1.3 (en coordenadas normalizadas y con el signo cambiado, porque aquí se mueve la cámara y no el punto). Para $k$ puntos se apilan las filas ($2k\times 6$). La profundidad $Z$ se toma del sensor, de la pose estimada o de su valor en el objetivo ($Z^*$).

### 3.3 IBVS y PBVS (Chaumette & Hutchinson 2006, 2007)

Si se impone un decaimiento exponencial $\dot e=-\lambda e$:

- **IBVS** (basado en imagen): $v = -\lambda\,\widehat{L_s}^{+}\,e$. Es robusto a errores de calibración, pero la trayectoria 3D puede ser rara (el clásico retroceso de la cámara ante rotaciones de $\pi$ alrededor del eje óptico) y aparecen mínimos locales y singularidades de $L_s$.
- **PBVS** (basado en posición): con $s=(t,\theta u)$ tomados de ${}^{c^*}T_{c}$,
$$ \nu = -\lambda\,R^\top\,{}^{c^*}t_{c},\qquad \omega = -\lambda\,\theta u . $$
La trayectoria cartesiana es recta, pero depende de la calidad de la estimación de pose.
- **Híbrido 2½D** (Malis-Chaumette): mezcla ambos. La parte II del tutorial cubre además la estimación de $L_s$ en línea, el seguimiento de objetivos en movimiento y el desacoplo.

### 3.4 Ley de control en el álgebra de Lie

Si se define el error directamente en el grupo, $T_e={}^{c^*}T_{c}$, y se aplica el *twist* del cuerpo

$$
v = -\lambda\,\mathrm{Log}(T_e)^\vee \in \mathbb{R}^6,
$$

entonces, como $\mathrm{Log}(T_e)$ conmuta consigo mismo, la solución es $T_e(t)=\mathrm{Exp}\!\big(e^{-\lambda t}\,\xi_0\big)$ con $\xi_0=\mathrm{Log}\,T_e(0)$. El error **converge exponencialmente a lo largo del tornillo (*screw*) geodésico** de $SE(3)$, sin singularidades de representación (salvo en el corte $\theta=\pi$). Esta ley es la "versión Lie" del PBVS, y es exactamente la que regresan redes como **Siame-se(3)** (Felton, Fromont y Marchand, ICRA 2021): una red siamesa recibe la imagen actual y la deseada y **regresa directamente $v\in\mathfrak{se}(3)$**. Se entrena solo en simulación y se combina con el servo fotométrico para la precisión final. Es el puente natural entre la parte 1 (álgebra) y este proyecto.

### 3.5 Servo directo / fotométrico

**Collewet y Marchand (IEEE T-RO 27(4):828–834, 2011)** usan como característica **la imagen completa**, $s=I(\cdot)$, y minimizan $\|I(v)-I^*\|^2$. Por la hipótesis de brillo constante, cada píxel aporta una fila $L_I = -\nabla I^\top L_x$. No necesita extraer ni emparejar características y es muy preciso, pero su cuenca de convergencia es pequeña. Su pariente en estimación es la odometría directa (DSO, §4).

### 3.6 Servo visual aprendido

- **Bateux, Marchand et al. (arXiv 1705.08940; ICRA 2018).** Una CNN estima la pose relativa entre la imagen actual y la deseada y alimenta un PBVS. El dataset se genera automáticamente con perturbaciones (oclusión, iluminación) a partir de una sola imagen.
- **Siame-se(3)** (arriba): regresión de extremo a extremo en $\mathfrak{se}(3)$.
- **DFVS** (arXiv 2003.03766): flujo óptico aprendido más profundidad aprendida, integrados con la matriz de interacción. **DeepMPCVS** (arXiv 2105.00788) añade control predictivo.
- *Nota:* el "DEFNet" del enunciado no se ha podido verificar como publicación de servo visual. Se sustituye por los trabajos anteriores, que sí están verificados.

**Para el proyecto:** los datos de entrenamiento de un servo aprendido salen gratis en MuJoCo. Se muestrea una pose de cámara objetivo cerca del tubo, se perturba con $\mathrm{Exp}(\xi)$, $\xi\sim\mathcal{N}(0,\Sigma)$, y se usa $-\lambda\xi$ como etiqueta.

---

## 4. SLAM / odometría visual sobre grupos de Lie

### 4.1 Intuición

El SLAM estima **a la vez** la trayectoria de la cámara $\{T_i\}\subset SE(3)$ (o $Sim(3)$ en monocular, por la escala) y el mapa. En este proyecto **la cámara de muñeca se mueve con el brazo**, así que las mismas herramientas sirven para (i) seguir la pose de la cámara de muñeca cuando la cinemática no es fiable, (ii) reconstruir la mesa y (iii) entender los estimadores que usan internamente FoundationPose (seguimiento) o DROID-SLAM.

### 4.2 Métodos

- **DSO – Direct Sparse Odometry** (Engel, Koltun y Cremers, TPAMI 2018). Odometría **directa** (error fotométrico, sin descriptores) sobre píxeles dispersos con gradiente. Optimiza conjuntamente poses en $SE(3)$, profundidades inversas y calibración fotométrica (exposición, viñeteado) en ventana deslizante con marginalización (complemento de Schur).
- **ORB-SLAM3** (Campos et al., T-RO 2021). Basado en características ORB. Hace BA local y global en $SE(3)$ (g2o), relocalización, cierre de bucles y **multi-mapa**. Soporta monocular, estéreo, RGB-D, *fisheye* y visual-inercial con estimación MAP completa desde la inicialización.
- **DROID-SLAM** (Teed y Deng, NeurIPS 2021). Actualizaciones recurrentes (RAFT) de flujo más una capa **Dense Bundle Adjustment** diferenciable:
$$ \min_{\{G_i\},\{d_i\}}\sum_{(i,j)}\big\|p^*_{ij}-\Pi\big(G_{ij}\circ\Pi^{-1}(p_i,d_i)\big)\big\|^2_{\Sigma_{ij}},\qquad G_{ij}=G_jG_i^{-1}, $$
resuelto con Gauss-Newton y Schur, con retracción $G\leftarrow\mathrm{Exp}(\xi)\circ G$. Se implementa con **`lietorch`**, que retropropaga los gradientes **en el espacio tangente** de $SE(3)$ y $Sim(3)$. Es el ejemplo canónico de "Lie + aprendizaje profundo" que este proyecto puede imitar.
- **Gaussian Splatting SLAM** (Matsuki et al., CVPR 2024). Seguimiento de cámara por optimización directa contra gaussianas 3D, con Jacobianos analíticos respecto a $\mathfrak{se}(3)$.

### 4.3 Filtros en grupos de Lie

- **Invariant EKF** (Barrau y Bonnabel, IEEE TAC 2017). Para sistemas "afines en el grupo", el error invariante $\eta = \hat X^{-1}X$ (o $X\hat X^{-1}$) tiene **dinámica autónoma**. Linealizada en el tangente, $\eta=\mathrm{Exp}(\zeta)$, cumple $\dot\zeta = A\,\zeta$ con $A$ **independiente de la trayectoria estimada**. El resultado son estabilidad local demostrable y una consistencia mucho mejor que la del EKF clásico.
- **Preintegración en la variedad** (Forster, Carlone, Dellaert y Scaramuzza, T-RO 2017). Resume las medidas IMU entre *keyframes* en un único factor relativo,
$$ \Delta R_{ij}=\prod_{k=i}^{j-1}\mathrm{Exp}\big((\tilde\omega_k-b_g)\Delta t\big), $$
con propagación de ruido en el tangente y correcciones de primer orden por el sesgo mediante Jacobianos derechos. Es la base de VIO/ORB-SLAM3 y GTSAM.

Todos estos filtros y optimizadores son instancias del esquema "linealizar en el tangente, resolver y retraer" desarrollado en la parte 2. **En la escena MuJoCo no hay IMU**, pero se puede simular (`<sensor><gyro/><accelerometer/>` en el sitio de la muñeca) si se quiere fusionar con la cámara de muñeca.

---

## 5. Visión equivariante para manipulación

### 5.1 Intuición

Si se desplaza o rota un tubo sobre la mesa, **el agarre correcto se desplaza o rota igual**. Una red $f$ es **equivariante** respecto a un grupo $G$ si

$$
f(g\cdot x) = \rho(g)\,f(x)\qquad \forall g\in G,
$$

y es invariante si $\rho(g)=I$. Incorporar esta simetría a la arquitectura (en vez de aprenderla con aumentación de datos) da **eficiencia de muestras** y **generalización a poses no vistas**. En la práctica, con 10 demostraciones basta para agarrar tubos en orientaciones arbitrarias. Esta sección es la aplicación más directa de la teoría de representaciones de la parte 1.

### 5.2 Arquitecturas $SE(3)$/$SO(3)$-equivariantes

- **Vector Neurons** (Deng et al., ICCV 2021). Las neuronas pasan de ser escalares a **vectores 3D**: $V\in\mathbb{R}^{C\times3}$. Las capas lineales $V\mapsto WV$ conmutan con $V\mapsto VR$. Las no linealidades tipo ReLU se construyen con una dirección aprendida $k=UV$ y proyectan $V$ sobre el semiespacio $\langle q,k\rangle\ge0$. Es sencillo y se puede montar sobre PointNet o DGCNN.
- **e3nn** (Geiger y Smidt, 2022). Biblioteca general $E(3)$-equivariante con representaciones irreducibles (armónicos esféricos) y productos tensoriales de Clebsch-Gordan. Permite construir Tensor Field Networks, CNN esteerables 3D, etc.
- **SE(3)-Transformers** (Fuchs et al., NeurIPS 2020). Auto-atención equivariante a rototraslaciones sobre nubes de puntos y grafos.

### 5.3 Neural Descriptor Fields (NDF)

Simeonov et al. (ICRA 2022). Una red (encoder Vector Neurons más decodificador implícito) produce un **campo de descriptores** $f(x\mid P)$ para cualquier punto 3D $x$ dada la nube del objeto $P$, con

$$
f(Rx+t\mid RP+t)=f(x\mid P)\quad (\text{$SE(3)$-equivariancia}).
$$

Una pose de agarre $T$ se describe con los descriptores de un conjunto de puntos de consulta $\{q_i\}$ fijados a la pinza. **Transferir una demostración** es resolver

$$
T^\star = \arg\min_{T\in SE(3)}\sum_i\big\|f(T q_i\mid P_{\text{nuevo}}) - f(q_i^{\text{demo}}\mid P_{\text{demo}})\big\|,
$$

una **optimización en $SE(3)$** (con Adam sobre la parametrización del tangente, varios reinicios). Basta con 5–10 demostraciones por categoría. Encaja con los tubos (una categoría con variantes de 1.5, 15 y 50 ml).

### 5.4 Transporter Networks y políticas equivariantes

- **Transporter Networks** (Zeng et al., CoRL 2020). Para *pick-and-place* desde una vista cenital, la acción de colocar se obtiene por **correlación cruzada** de las características recortadas alrededor del punto de agarre con las de la escena, sobre un conjunto discreto de rotaciones:
$Q_{\text{place}}(\tau)=\psi(o[T_{\text{pick}}])\star\phi(o)[\tau]$. Es equivariante por construcción a traslaciones y a rotaciones planas ($SE(2)$) y muy eficiente en muestras. Encaja bien con "coger un tubo de la zona y dejarlo en el hueco *k* de la gradilla".
- **Equivariant Diffusion Policy** (Wang et al., CoRL 2024). La red de *denoising* es equivariante (sobre todo $SO(2)$, extendible a $SE(3)$), lo que mejora la eficiencia de muestras de Diffusion Policy.
- **EquiBot** (Yang et al., CoRL 2024). Política de difusión **$SIM(3)$-equivariante** (rotación, traslación y escala) sobre nubes de puntos con Vector Neurons.

### 5.5 Detección de agarres

- **GraspNet-1Billion** (Fang et al., CVPR 2020). 97 280 imágenes RGB-D con más de 1100 millones de agarres 6-DoF anotados analíticamente (*force closure*). Es el benchmark estándar.
- **Contact-GraspNet** (Sundermeyer et al., ICRA 2021). Cada punto de la nube es un posible **contacto**. Eso reduce el agarre 6-DoF a 4-DoF (dirección de aproximación, orientación de la base y anchura) anclados al punto. Entrenado con 17 millones de agarres simulados y con más del 90 % de éxito en objetos no vistos.
- **AnyGrasp** (Fang et al., T-RO 2023). Agarres densos de 7-DoF, robusto a la profundidad ruidosa y con **seguimiento temporal** de agarres (útil si el tubo rueda tras caer).
- **Edge Grasp Network** (Huang et al., CoRL 2022). Evaluación de agarres $SE(3)$-**invariante** basada en grafos.
- **EquiGraspFlow** (Lim et al., CoRL 2024). Modelo generativo de agarres por **flujo en la variedad $SE(3)$** con equivariancia garantizada, que conecta directamente con los *flows* riemannianos de la parte 2.

**Atención:** Contact-GraspNet y AnyGrasp **dependen de la profundidad**, que falla con tubos transparentes (§2.6). O se completa la profundidad (TransCG/ClearGrasp) o se parte de la **pose 6D con CAD** y se usan agarres predefinidos en el marco del tubo, que es la opción más robusta para un objeto conocido.

---

## 6. Políticas visuomotoras y *vision-language-action* (VLA)

### 6.1 Intuición

En lugar del pipeline modular (percepción → pose → agarre → IK → control), una **política visuomotora** aprende directamente $\pi_\theta(a_{t:t+H}\mid o_t, \ell)$: de imágenes (más propiocepción y, en los VLA, una instrucción de lenguaje $\ell$) a un **fragmento de acciones** (*action chunk*). La geometría de Lie entra por dos puertas: **cómo se representa la acción de rotación** y **cómo se hace el *fine-tuning*** (geometría del espacio de parámetros, parte 2).

### 6.2 Métodos

- **Diffusion Policy** (Chi et al., RSS 2023). La política es un proceso de *denoising* condicionado sobre un fragmento de acciones $A$:
$$ A^{k-1}=\alpha_k\big(A^k-\gamma_k\,\varepsilon_\theta(O,A^k,k)\big)+\mathcal{N}(0,\sigma_k^2 I). $$
Maneja la multimodalidad (varios agarres válidos), usa control con horizonte deslizante y es estable al entrenar. La implementación oficial convierte las rotaciones absolutas del efector a la **representación 6D** (§2.3) antes de difundirlas.
- **ACT – Action Chunking with Transformers** (Zhao et al., RSS 2023). Un CVAE con transformer predice fragmentos de **posiciones articulares absolutas** y hace *temporal ensembling*. Se diseñó para **ALOHA**, el mismo brazo de nuestra escena.
- **RT-2** (Brohan et al., 2023). Un VLM (PaLI-X/PaLM-E) se co-ajusta con datos web y robóticos. Las **acciones son tokens de texto**: $\Delta$ posición y $\Delta$ rotación del efector y la pinza, discretizados en 256 *bins*.
- **OpenVLA** (Kim et al., 2024). 7B de parámetros (Llama 2 más DINOv2 y SigLIP) entrenado con Open X-Embodiment. Usa acción de 7-D ($\Delta xyz$, $\Delta$ rotación, pinza), con 256 *bins* por dimensión definidos por cuantiles, que sobrescriben los 256 tokens menos usados del vocabulario. Se ajusta con LoRA.
- **Octo** (Octo Team, RSS 2024). Transformer generalista (800 000 trayectorias de OXE) con cabeza de **difusión** de acciones continuas. Admite nuevas observaciones y espacios de acción en el *fine-tuning*.
- **π0** (Black et al., 2024). VLM (PaliGemma) más un **experto de acciones por *flow matching*** que genera fragmentos continuos ($H=50$) a alta frecuencia. En esencia, con $A^\tau=\tau A+(1-\tau)\varepsilon$, se aprende el campo de velocidades $v_\theta(A^\tau,o)\approx A-\varepsilon$ y se integra con unos pocos pasos de Euler.
- **FAST** (Pertsch et al., 2025). Tokenizador de acciones por **DCT** más BPE que hace viables los VLA autorregresivos con datos de alta frecuencia (π0-FAST).
- **π0.5** (Physical Intelligence, 2025). Co-entrenamiento heterogéneo (web, subtareas semánticas, varios robots) para la generalización en mundo abierto.
- **RDT-1B** (Liu et al., ICLR 2025). Transformer de difusión de 1B de parámetros para **manipulación bimanual**, con espacio de acción unificado.
- **UMI** (Chi et al., RSS 2024). Muestra que la **representación de acción relativa** (trayectorias expresadas en el marco actual del efector, $T_{t}^{-1}T_{t+k}$) generaliza mejor y es agnóstica al robot. Es un argumento directo a favor de las **acciones en el grupo / en el tangente**.

### 6.3 Cómo se representa la acción del efector

| Representación | Fórmula | Ventajas | Problemas |
|---|---|---|---|
| Pose absoluta, Euler | $(x,y,z,r,p,y)$ | Simple | Discontinua y con *gimbal lock* |
| Delta de Euler/eje-ángulo (RT-2, OpenVLA) | $\Delta p,\ \Delta\theta$ | Fácil de discretizar | Mezcla marcos, no compone bien y la suma no es la del grupo |
| Pose absoluta en 6D (Diffusion Policy) | $(p, a_1, a_2)$ | Continua (Zhou et al.) | Absoluta, sensible al marco |
| **Relativa en el grupo** (UMI) | $T_t^{-1}T_{t+k}$ | Invariante al marco base | Hay que escoger una parametrización |
| **Tangente $\mathfrak{se}(3)$** | $\xi_k=\mathrm{Log}(T_t^{-1}T_{t+k})$ | Lineal, se compone con $\mathrm{Exp}$, sirve para la difusión/flujo euclídeo local | Corte en $\theta=\pi$ (irrelevante para deltas pequeños) |
| Articular (ACT, π0 en ALOHA) | $q\in\mathbb{R}^{n}$ | Sin IK | No se transfiere entre robots |

**Recomendación para el proyecto:** entrenar o ajustar con **acciones relativas en $\mathfrak{se}(3)$** (o en 6D relativo) para el efector y dejar la pinza como escalar. Es coherente con la parte 1 (retracción $\mathrm{Exp}$) y con el servo de §3.4: la política aprende "el *twist* de corrección", igual que Siame-se(3). Si se usa π0/RDT tal y como vienen en AutoBio, estos trabajan en espacio **articular**. En ese caso la geometría de Lie entra en la **supervisión auxiliar** (pérdida geodésica sobre la pose del efector por cinemática directa) y en el **optimizador** (gradiente natural / K-FAC, parte 2).

### 6.4 *Fine-tuning* con datos propios de simulación

- **AutoBio** (Lan et al., ICLR 2026, arXiv 2505.14030). Simulador y benchmark de laboratorio de biología digital sobre MuJoCo, con **16 tareas en 3 niveles de dificultad**. Incluye una *pipeline* para digitalizar instrumentos, *plugins* de física para mecanismos de laboratorio (roscas, rotores...) y un **puente de renderizado a Blender (PBR)** para interfaces dinámicas y **materiales transparentes**. Usa ALOHA, UR5e con Robotiq y UR5e con mano diestra, cámara global frontal y cámaras de muñeca. Evalúa **π0 y RDT**: rinden bien en las tareas fáciles y **caen fuertemente en las de precisión, razonamiento visual y seguimiento de instrucciones** (medias y difíciles). Es la motivación directa de este proyecto: **la precisión geométrica es el cuello de botella**.
- Otros trabajos de automatización de laboratorio: **Chemistry3D** (arXiv 2406.08160), un benchmark de interacción robótica para experimentos químicos, y **LucidGrasp** (§2.6).
- **Receta de *fine-tuning*** con el harness ya presente en el repo (`third_party/AutoBio/autobio/evaluate_openpi.py`, `evaluate_rdt.py`, `simulation/third_party/AutoBio/{openpi,RoboticsDiffusionTransformer}`):
  1. Generar demostraciones con un **experto con información privilegiada** (pose exacta del tubo desde MuJoCo → agarre → IK analítica de ALOHA → trayectoria interpolada geodésicamente en $SE(3)$).
  2. Renderizar las cámaras `table_cam_front` y `wrist_cam_left` con aleatorización de dominio.
  3. Ajustar con LoRA (OpenVLA/π0) o con *full fine-tuning* del experto de acciones.
  4. Evaluar en bucle cerrado en la simulación.

### 6.5 *Sim-to-real* y aleatorización de dominio

**Tobin et al. (IROS 2017)** mostraron que un detector entrenado **solo** con renders con texturas aleatorias no realistas transfiere al mundo real con 1.5 cm de error. En MuJoCo se aleatoriza cambiando `model.mat_rgba`, `model.light_*`, `model.cam_pos/quat/fovy` y las texturas entre episodios, sin recompilar el modelo. **Aleatorizar la pose de la cámara con $\mathrm{Exp}(\xi)$, $\xi\sim\mathcal{N}(0,\Sigma_{\text{calib}})$** modela el error de calibración mano-ojo de §1.6 de forma geométricamente correcta. Para la transparencia hace falta el camino Blender/PBR de AutoBio, porque el *alpha blending* de MuJoCo no reproduce la refracción que rompe los sensores reales.

---

## 7. Variedades neuronales en visión

### 7.1 Intuición

Las imágenes de un tubo rígido visto desde todas las poses forman (idealmente) una **variedad de dimensión 6** (o de dimensión 5 si el tubo es simétrico) dentro del espacio de píxeles. Esta es la hipótesis de la variedad. Un espacio latente bien construido debería **respetar la topología y la estructura de grupo** de esa variedad: si $g\in SE(3)$ mueve el objeto, el latente debería moverse por una acción $\rho(g)$ conocida. Esto enlaza con la "geometría de variedades neuronales" del objetivo global y con la geometría de la información de la parte 2 (la métrica de Fisher induce una métrica riemanniana sobre los latentes).

### 7.2 Métodos

- **Homeomorphic VAE** (Falorsi et al., 2018). Si la variedad de datos tiene topología no trivial ($SO(3)$ no es homeomorfo a $\mathbb{R}^3$), un codificador continuo hacia un latente euclídeo **tiene que** crear agujeros o discontinuidades. La solución es usar **latentes valorados en $SO(3)$**, con distribuciones reparametrizables definidas vía $\mathrm{Exp}$ del álgebra. Es el mismo argumento topológico que el de Zhou et al. (§2.3), aplicado a los latentes.
- **Commutative Lie Group VAE** (Zhu, Xu y Tao, ICML 2021). Formula el desenmarañamiento (*disentanglement*) como aprender una **acción de grupo** sobre el latente, parametrizada por el álgebra de Lie ($z\mapsto \exp(\sum_i t_i A_i)$ con generadores que conmutan).
- **Learning Lie Group Symmetry Transformations** (Gabel et al., TAG-ML 2023). **Descubre** los generadores de un subgrupo uniparamétrico que explica las transformaciones de un dataset. Útil para averiguar qué simetrías tiene realmente la tarea (p. ej., $SO(2)$ alrededor del eje del tubo).
- **iNeRF** (Yen-Chen et al., IROS 2021). **Invierte** un NeRF: dada una imagen, busca por descenso de gradiente la pose de la cámara en $SE(3)$ que minimiza el error fotométrico entre el render y la observación. Es *render-and-compare* sin malla.
- **BARF** (Lin et al., ICCV 2021). Optimiza **a la vez** el NeRF y las poses de cámara en $\mathfrak{se}(3)$. Demuestra que la codificación posicional de alta frecuencia estropea el registro y propone un **enmascaramiento progresivo de frecuencias** (de grueso a fino), análogo a las pirámides de imagen del alineamiento clásico.
- **Gaussian Splatting SLAM** (§4.2). Seguimiento de la pose contra un mapa de gaussianas 3D con Jacobianos analíticos en $\mathfrak{se}(3)$.

### 7.3 Conexiones útiles para el proyecto

1. **Latente de pose con estructura de grupo:** si se entrena un codificador de imágenes del tubo con latente en $SO(3)\times\mathbb{R}^3$ (o $S^2\times\mathbb{R}^3$ por la simetría), el latente *es* la pose y la métrica geodésica del latente coincide con la del control.
2. **Métrica inducida:** el *pullback* de la métrica de salida (Fisher) sobre los parámetros o latentes es la métrica que usa el gradiente natural (parte 2). Se pueden medir **curvatura y distorsión** de la variedad aprendida comparando distancias latentes con errores geodésicos reales (que MuJoCo da gratis).
3. **Refinamiento tipo iNeRF/BARF con MuJoCo como renderizador:** MuJoCo no es diferenciable en el render, pero la versión *render-and-compare* aprendida (FoundationPose/MegaPose) o un renderizador diferenciable (nvdiffrast, que usa FoundationPose) permiten el mismo esquema.

---

## 8. Propuesta concreta para este proyecto

### 8.1 Qué hay ya en el repositorio (punto de partida verificado)

- **Escena:** `simulation/models/autobio_lab.xml` contiene el brazo **ALOHA** (`aloha1`, un solo brazo en el centro de la mesa), la gradilla `centrifuge_10slot` (`slot`, a ~0.3 m delante del brazo), un tubo de 50 ml con tapón de rosca, el GC-MS (a la izquierda) y el UV-Vis-NIR (a la derecha).
- **Cámaras:** `table_cam_front` (fovy 45°, 1280×960), `table_cam_left` (fovy 45°) y `table_cam_wide` (fovy 50°) en la escena, más `wrist_cam_left` en `third_party/AutoBio/autobio/model/robot/aloha_left.xml`. Intrínsecos según §1.2: para `table_cam_front`, $f_y = 480/\tan(22.5^\circ)\approx 1159$ px y $(c_x,c_y)=(640,480)$.
- **Cinemática:** `third_party/AutoBio/autobio/aloha_analytical_ik.py` ofrece IK analítica (muñeca esférica: `site_pose_to_wrist_pos` más la solución de las tres primeras articulaciones). `autobio/grasp/` tiene utilidades de cuaterniones y transformaciones.
- **Políticas:** harness de evaluación de π0 (openpi) y RDT (`evaluate_openpi.py`, `evaluate_rdt.py`).
- **Tubos que caen:** `scripts/spawner.py` hace que un operario deje tubos (una reserva de 10) en dos **zonas de spawn** a **±2.1 m** del centro, a lo largo del eje largo de la mesa.

> **Restricción importante (no explícita en el enunciado):** el ALOHA (ViperX-300) tiene un alcance de ~0.6–0.75 m (con los parámetros de la IK, $a=0.3$ m por eslabón). **Los tubos que caen en las zonas de spawn están físicamente fuera de su alcance.** Hay que elegir explícitamente una de estas opciones:
> (A) **Acotar:** en las zonas de spawn solo se hace **detección, seguimiento y estimación de pose a distancia** (con `table_cam_left`/`table_cam_wide`), y el agarre en bucle cerrado se hace con tubos dentro del área de trabajo (gradilla/`slot`).
> (B) **Transporte:** añadir una base móvil (un raíl prismático bajo `aloha1`, que es trivial en MJCF con un `<joint type="slide">`), un segundo brazo en cada extremo o una cinta transportadora.
> Recomendación para el hackathon: **(B) con un raíl lineal**. El espacio de configuración pasa a ser $\mathbb{R}\times$(articulaciones), la cámara de muñeca sigue siendo útil y la cámara global puede guiar el movimiento del raíl.

### 8.2 Pipeline visión → movimiento

```
 ┌───────────────┐   RGB(-D), K, T_bc   ┌────────────────────┐  máscara/bbox  ┌──────────────────────┐
 │ Cámaras MuJoCo │ ───────────────────▶ │ Detección/segment. │ ─────────────▶ │ Pose 6D del tubo      │
 │ front/left/    │                      │ (Grounding DINO +  │                │ FoundationPose (CAD)  │
 │ wide + muñeca  │                      │  SAM 2) o máscara  │                │ + seguimiento; o red  │
 └───────────────┘                      │  GT de MuJoCo      │                │ propia 6D/IPDF        │
                                         └────────────────────┘                └──────────┬───────────┘
                                                                                            │ ^cT_o (+Σ)
                                                                                            ▼
 ┌────────────────────────┐  T_bg*  ┌────────────────────────────┐   q(t)   ┌─────────────────────────┐
 │ Agarre objetivo en SE(3)│ ──────▶ │ IK analítica ALOHA +        │ ───────▶ │ Servo visual en se(3)    │
 │ T_bg* = T_bc·T_co·T_og  │         │ trayectoria geodésica en    │          │ v = -λ Log(^{c*}T_c)     │
 │ (agarres predefinidos    │         │ SE(3): T(s)=T0·Exp(s·ξ)     │          │ (cámara de muñeca,       │
 │  en el marco del tubo,   │         │ (parte 1) / optimización    │          │  PBVS o Siame-se(3))     │
 │  módulo simetría SO(2))  │         │ (parte 2)                   │          └────────────┬────────────┘
 └────────────────────────┘         └────────────────────────────┘                       │ demos exitosas
                                                                                            ▼
                                                        ┌──────────────────────────────────────────────┐
                                                        │ Fine-tuning de política (π0/RDT/Diffusion      │
                                                        │ Policy) con acciones relativas en se(3),       │
                                                        │ pérdida geodésica auxiliar, gradiente natural  │
                                                        └──────────────────────────────────────────────┘
```

**Detalles de cada bloque:**

1. **Captura.** `mujoco.Renderer(model, H, W)`: `update_scene(data, camera="table_cam_front")`, `render()` para RGB, `enable_depth_rendering()` para profundidad y `enable_segmentation_rendering()` para los IDs de geom. Pose de la cámara: `data.cam_xpos`, `data.cam_xmat` (convertir de la convención OpenGL a OpenCV, §1.2). Pose real del tubo: `data.xpos/xquat` del cuerpo, que sirve de **etiqueta gratuita**.
2. **Detección.** Al principio, la **máscara de segmentación de MuJoCo** (oráculo). Después, Grounding DINO ("centrifuge tube") más SAM 2 para quitar el oráculo.
3. **Pose 6D.** FoundationPose con la malla del tubo de AutoBio (hay que respetar su licencia: el repo solo la referencia). Como alternativa ligera, una red propia (ResNet → $t$ más rotación 6D, o IPDF para modelar la simetría) entrenada con el dataset sintético. Salida: ${}^{c}T_o$ y, si es posible, una covarianza en el tangente.
4. **Pose en la base del robot:** ${}^{b}T_o={}^{b}T_c\,{}^{c}T_o$. En la simulación ${}^{b}T_c$ se conoce. En la validación se estima con Park-Martin (§1.5) para practicar el procedimiento real.
5. **Agarre.** Un conjunto discreto de agarres $\{{}^{o}T_{g,k}\}$ en el marco del tubo (radial al cuerpo y vertical al tapón). Por la simetría $SO(2)$ se elige la rotación alrededor del eje que **minimiza la distancia geodésica** a la orientación actual de la pinza y respeta la accesibilidad de la IK. Más adelante se puede sustituir por NDF o EquiGraspFlow.
6. **Trayectoria.** Pre-agarre → agarre con interpolación geodésica $T(s)=T_0\,\mathrm{Exp}(s\,\mathrm{Log}(T_0^{-1}T_1))$ e IK analítica en cada punto (o IK diferencial con Jacobiano geométrico, parte 1). Límites articulares y colisiones con `mj_collision`.
7. **Bucle cerrado.** En los últimos ~10 cm se hace PBVS en $\mathfrak{se}(3)$ con la cámara de muñeca: $v=-\lambda\,\mathrm{Log}({}^{c^*}T_c)^\vee$ y $\dot q = J(q)^{+}\,\mathrm{Ad}\,v$. Se actualiza ${}^{c}T_o$ con el modo *tracking* de FoundationPose.
8. **Política.** Con las demostraciones exitosas del experto (pasos 1–7) se ajusta π0 o RDT (harness de AutoBio) o una Diffusion Policy con acciones relativas en $\mathfrak{se}(3)$. Aquí entran el **gradiente natural** y las pérdidas geodésicas de la parte 2.

### 8.3 Datasets, modelos y repos candidatos

| Recurso | Uso en el proyecto | Enlace |
|---|---|---|
| AutoBio (assets, IK, harness π0/RDT) | Escena, malla del tubo, evaluación | [github.com/autobio-bench/AutoBio](https://github.com/autobio-bench/AutoBio) |
| MuJoCo / Menagerie | Simulación, otros brazos (UR5e, Panda) | [github.com/google-deepmind/mujoco_menagerie](https://github.com/google-deepmind/mujoco_menagerie) |
| FoundationPose | Pose 6D y seguimiento con CAD | [github.com/NVlabs/FoundationPose](https://github.com/NVlabs/FoundationPose) |
| SAM-6D | Alternativa *zero-shot* | [github.com/JiehongLin/SAM-6D](https://github.com/JiehongLin/SAM-6D) |
| Grounding DINO / SAM 2 | Detección y segmentación abiertas | [IDEA-Research/GroundingDINO](https://github.com/idea-research/groundingdino), [facebookresearch/sam2](https://github.com/facebookresearch/sam2) |
| lietorch / PyPose | $\mathrm{Exp}/\mathrm{Log}$ y retropropagación en $SE(3)$ | [princeton-vl/lietorch](https://github.com/princeton-vl/lietorch), [pypose.org](https://pypose.org/) |
| DenseFusion | *Baseline* RGB-D entrenable con datos propios | [github.com/j96w/DenseFusion](https://github.com/j96w/DenseFusion) |
| Contact-GraspNet / GraspNet baseline | Agarres genéricos (con profundidad válida) | [NVlabs/contact_graspnet](https://github.com/NVlabs/contact_graspnet), [graspnet/graspnet-baseline](https://github.com/graspnet/graspnet-baseline) |
| NDF | Transferencia de agarres con pocas demos | [anthonysimeonov/ndf_robot](https://github.com/anthonysimeonov/ndf_robot) |
| Vector Neurons | Encoder equivariante | [FlyingGiraffe/vnn](https://github.com/FlyingGiraffe/vnn) |
| TransCG, ClearGrasp, ClearPose | Datos reales de objetos transparentes (fase *sim-to-real*) | [TransCG](https://github.com/Galaxies99/TransCG), [cleargrasp](https://github.com/Shreeyak/cleargrasp), [ClearPose](https://github.com/opipari/ClearPose) |
| OpenVLA / RDT / openpi | Políticas VLA a ajustar | [openvla/openvla](https://github.com/openvla/openvla), [thu-ml/RoboticsDiffusionTransformer](https://github.com/thu-ml/RoboticsDiffusionTransformer) |
| **Dataset propio "MAFER-Tubes-Sim"** | RGB/profundidad/máscara/pose GT desde MuJoCo, formato BOP | (a generar, §8.5 F1) |

Se recomienda guardar el dataset sintético en **formato BOP** (`scene_camera.json` con $K$ y ${}^{c}T_w$, `scene_gt.json` con ${}^{c}T_o$ en mm). Así funcionan sin cambios las herramientas `bop_toolkit` y los *loaders* de GDR-Net, CosyPose, MegaPose y FoundationPose.

### 8.4 Métricas de evaluación

| Nivel | Métrica | Definición / umbral |
|---|---|---|
| Pose | **ADD-S** (el tubo es simétrico) y ADD (con el tapón) | §2.5. Éxito si $<0.1\cdot$ diámetro; también el AUC hasta 10 cm |
| Pose | **Error geodésico de rotación** | $\arccos\frac{\mathrm{tr}(R^\top\hat R)-1}{2}$ en grados. Para el tubo, error del **eje**: $\arccos(\hat a^\top a)$ |
| Pose | Error de traslación | $\|t-\hat t\|$ en mm |
| Pose | BOP AR (VSD/MSSD/MSPD) | Si se usa el formato BOP |
| Calibración | Error de $X$ en $AX=XB$ | $\|\mathrm{Log}(X_{\text{gt}}^{-1}\hat X)\|$ (rotación en grados y traslación en mm) |
| Servo | Error final y tiempo de convergencia | $\|\mathrm{Log}({}^{c^*}T_c)\|$ al final, número de pasos y tasa de convergencia bajo perturbaciones $\mathrm{Exp}(\xi_0)$ de magnitud creciente |
| Tarea | **Tasa de éxito** | El tubo queda agarrado y levantado más de 5 cm, o insertado en el hueco correcto de la gradilla (N ≥ 50 episodios con semillas distintas) |
| Tarea | Robustez | Éxito en función de la aleatorización (iluminación, textura, error de calibración $\Sigma$) |
| Política | Suavidad | Tirón (*jerk*) y longitud geodésica de la trayectoria del efector en $SE(3)$ |
| Eficiencia | Muestras | Éxito frente al número de demostraciones (curvas de eficiencia de datos, como en AutoBio) |

### 8.5 Hoja de ruta por fases (hackathon)

| Fase | Duración orientativa | Entregable | Criterio de salida |
|---|---|---|---|
| **F0 – Base geométrica** | 0.5 días | Módulo `lie_utils` (parte 1): `Exp/Log` de $SO(3)$ y $SE(3)$, Jacobianos, conversión OpenGL↔OpenCV, $K$ desde `fovy`. Tests contra MuJoCo (proyectar `data.xpos` del tubo y comparar con la máscara de segmentación) | Error de reproyección < 1 px |
| **F1 – Datos sintéticos** | 0.5–1 día | Generador: tubos en poses aleatorias en la gradilla y en las zonas de spawn, las 4 cámaras, RGB, profundidad, máscara y pose GT en formato BOP. Aleatorización de dominio (luces, colores, $\mathrm{Exp}(\xi)$ en las cámaras) | ≥ 10 000 imágenes, validación visual |
| **F2 – Pose 6D** | 1 día | FoundationPose con la malla del tubo (inferencia) más una *baseline* propia (rotación 6D o IPDF). Evaluación ADD-S y error geodésico | ADD-S < 0.1 d en > 90 % de las vistas de la gradilla |
| **F3 – Agarre abierto** | 0.5–1 día | Agarres en el marco del tubo módulo $SO(2)$, IK analítica y trayectoria geodésica. Decisión sobre el alcance (raíl lineal, §8.1) | Éxito en bucle abierto > 70 % con pose GT y > 50 % con pose estimada |
| **F4 – Bucle cerrado** | 1 día | PBVS en $\mathfrak{se}(3)$ con la cámara de muñeca y seguimiento. Opcional: regresor tipo Siame-se(3) entrenado con pares sintéticos | Mejora de la tasa de éxito frente a F3 con ruido de calibración |
| **F5 – Política aprendida** | 1–2 días | Demos de F4 → *fine-tuning* de π0/RDT (harness de AutoBio) o Diffusion Policy con acciones relativas en $\mathfrak{se}(3)$. Comparar el optimizador estándar con el gradiente natural o K-FAC (parte 2) y la pérdida L2 con la geodésica | Curvas de éxito frente a número de demos y frente al tipo de pérdida/optimizador |
| **F6 – Extras** | si sobra tiempo | NDF/EquiGraspFlow para los agarres, latente de pose $SO(3)$ (Homeomorphic VAE) y análisis de la variedad aprendida, render Blender/PBR de vidrio para *sim-to-real* | Demo y figuras |

**Riesgos y mitigaciones.**
(i) Alcance del brazo frente a las zonas de spawn: decidirlo en F3 (§8.1).
(ii) Versión de MuJoCo fijada a 3.3.0 por el *plugin* de AutoBio: el generador de datos debe correr en `.venv-autobio`.
(iii) La simetría del tubo hace inestable la regresión de la rotación completa: usar ADD-S, IPDF o estimar el eje.
(iv) La transparencia no se reproduce en el render nativo: al principio no importa (los datos son sintéticos), pero es crítica para el *sim-to-real* (TransCG/ClearGrasp, Blender).
(v) Las GPU del hackathon: FoundationPose necesita CUDA, así que conviene tener preparada la *baseline* ligera como plan B.

---

## 9. Bibliografía comentada

Todas las entradas se han verificado con búsqueda web durante la elaboración de este documento.

| # | Título | Autores | Año | Enlace | Por qué es relevante |
|---|---|---|---|---|---|
| 1 | A micro Lie theory for state estimation in robotics | J. Solà, J. Deray, D. Atchuthan | 2018 | [arXiv:1812.01537](https://arxiv.org/abs/1812.01537) | Referencia práctica de $\mathrm{Exp}/\mathrm{Log}$, Jacobianos y perturbaciones usada en §1 y §3 (desarrollada en la parte 1) |
| 2 | Robot sensor calibration: solving AX=XB on the Euclidean group | F. C. Park, B. J. Martin | 1994 | [DOI:10.1109/70.326576](https://doi.org/10.1109/70.326576) | Calibración mano-ojo resuelta en el álgebra de Lie (§1.5) |
| 3 | A new technique for fully autonomous and efficient 3D robotics hand/eye calibration | R. Y. Tsai, R. K. Lenz | 1989 | [DOI:10.1109/70.34770](https://doi.org/10.1109/70.34770) | Método clásico de mano-ojo, incluido en OpenCV |
| 4 | EasyHeC: Accurate and Automatic Hand-eye Calibration via Differentiable Rendering and Space Exploration | L. Chen, Y. Qin, X. Zhou, H. Su | 2023 | [arXiv:2305.01191](https://arxiv.org/abs/2305.01191) | Calibración sin marcadores con renderizado diferenciable en $SE(3)$ |
| 5 | Tangent Space Backpropagation for 3D Transformation Groups (lietorch) | Z. Teed, J. Deng | 2021 | [arXiv:2103.12032](https://arxiv.org/abs/2103.12032) · [GitHub](https://github.com/princeton-vl/lietorch) | Biblioteca para retropropagar en el tangente de $SE(3)$/$Sim(3)$ |
| 6 | PyPose: A Library for Robot Learning with Physics-based Optimization | C. Wang et al. | 2022 | [arXiv:2209.15428](https://arxiv.org/abs/2209.15428) | Grupos de Lie y optimizadores de 2.º orden en PyTorch |
| 7 | PoseCNN: A Convolutional Neural Network for 6D Object Pose Estimation in Cluttered Scenes | Y. Xiang, T. Schmidt, V. Narayanan, D. Fox | 2017 | [arXiv:1711.00199](https://arxiv.org/abs/1711.00199) | Regresión directa de pose, pérdida para simetrías, YCB-Video |
| 8 | DenseFusion: 6D Object Pose Estimation by Iterative Dense Fusion | C. Wang et al. | 2019 | [arXiv:1901.04780](https://arxiv.org/abs/1901.04780) · [GitHub](https://github.com/j96w/DenseFusion) | *Baseline* RGB-D entrenable con datos propios |
| 9 | PVNet: Pixel-wise Voting Network for 6DoF Pose Estimation | S. Peng, Y. Liu, Q. Huang, H. Bao, X. Zhou | 2018 | [arXiv:1812.11788](https://arxiv.org/abs/1812.11788) | Puntos clave por votación más PnP, robusto a la oclusión |
| 10 | GDR-Net: Geometry-Guided Direct Regression Network for Monocular 6D Object Pose Estimation | G. Wang, F. Manhardt, F. Tombari, X. Ji | 2021 | [arXiv:2102.12145](https://arxiv.org/abs/2102.12145) | Patch-PnP diferenciable y rotación 6D |
| 11 | CosyPose: Consistent multi-view multi-object 6D pose estimation | Y. Labbé, J. Carpentier, M. Aubry, J. Sivic | 2020 | [arXiv:2008.08465](https://arxiv.org/abs/2008.08465) | *Render-and-compare* y BA a nivel de objeto (varias cámaras) |
| 12 | MegaPose: 6D Pose Estimation of Novel Objects via Render & Compare | Y. Labbé et al. | 2022 | [arXiv:2212.06870](https://arxiv.org/abs/2212.06870) | Pose de objetos nuevos con solo CAD |
| 13 | FoundationPose: Unified 6D Pose Estimation and Tracking of Novel Objects | B. Wen, W. Yang, J. Kautz, S. Birchfield | 2023 | [arXiv:2312.08344](https://arxiv.org/abs/2312.08344) · [GitHub](https://github.com/NVlabs/FoundationPose) | Estimador y seguidor recomendado para el tubo (§8) |
| 14 | SAM-6D: Segment Anything Model Meets Zero-Shot 6D Object Pose Estimation | J. Lin, L. Liu, D. Lu, K. Jia | 2023 | [arXiv:2311.15707](https://arxiv.org/abs/2311.15707) · [GitHub](https://github.com/JiehongLin/SAM-6D) | Alternativa *zero-shot* a FoundationPose |
| 15 | BOP Challenge 2023 on Detection, Segmentation and Pose Estimation of Seen and Unseen Rigid Objects | T. Hodaň et al. | 2024 | [arXiv:2403.09799](https://arxiv.org/abs/2403.09799) | Benchmark, métricas VSD/MSSD/MSPD y formato de datos |
| 16 | BOP: Benchmark for 6D Object Pose Estimation | T. Hodaň et al. | 2018 | [arXiv:1808.08319](https://arxiv.org/abs/1808.08319) | Definición original del benchmark y del formato |
| 17 | On the Continuity of Rotation Representations in Neural Networks | Y. Zhou, C. Barnes, J. Lu, J. Yang, H. Li | 2019 | [arXiv:1812.07035](https://arxiv.org/abs/1812.07035) | Justifica la representación 6D (§2.3, §6.3) |
| 18 | Implicit-PDF: Non-Parametric Representation of Probability Distributions on the Rotation Manifold | K. Murphy, C. Esteves, V. Jampani, S. Ramalingam, A. Makadia | 2021 | [arXiv:2106.05965](https://arxiv.org/abs/2106.05965) | Densidades multimodales en $SO(3)$ para objetos simétricos |
| 19 | Probabilistic orientation estimation with matrix Fisher distributions | D. Mohlin, G. Bianchi, J. Sullivan | 2020 | [arXiv:2006.09740](https://arxiv.org/abs/2006.09740) | Distribución de Fisher matricial en $SO(3)$ con NLL |
| 20 | Deep Bingham Networks: Dealing with Uncertainty and Ambiguity in Pose Estimation | H. Deng et al. | 2020 | [arXiv:2012.11002](https://arxiv.org/abs/2012.11002) | Mezclas de Bingham sobre cuaterniones |
| 21 | ClearGrasp: 3D Shape Estimation of Transparent Objects for Manipulation | S. Sajjan et al. | 2019 | [arXiv:1910.02550](https://arxiv.org/abs/1910.02550) · [GitHub](https://github.com/Shreeyak/cleargrasp) | Completado de profundidad para objetos transparentes |
| 22 | KeyPose: Multi-View 3D Labeling and Keypoint Estimation for Transparent Objects | X. Liu, R. Jonschkowski, A. Angelova, K. Konolige | 2019 | [arXiv:1912.02805](https://arxiv.org/abs/1912.02805) | Pose de objetos transparentes desde estéreo, sin profundidad |
| 23 | TransCG: A Large-Scale Real-World Dataset for Transparent Object Depth Completion and a Grasping Baseline | H. Fang, H.-S. Fang, S. Xu, C. Lu | 2022 | [arXiv:2202.08471](https://arxiv.org/abs/2202.08471) · [GitHub](https://github.com/Galaxies99/TransCG) | Datos reales y red rápida para el *sim-to-real* de vidrio |
| 24 | ClearPose: Large-scale Transparent Object Dataset and Benchmark | X. Chen, H. Zhang, Z. Yu, A. Opipari, O. C. Jenkins | 2022 | [arXiv:2203.03890](https://arxiv.org/abs/2203.03890) · [GitHub](https://github.com/opipari/ClearPose) | Benchmark de pose de objetos transparentes (con líquidos) |
| 25 | LucidGrasp: Robotic Framework for Autonomous Manipulation of Laboratory Equipment with Different Degrees of Transparency via 6D Pose Estimation | (ver arXiv) | 2024 | [arXiv:2410.07801](https://arxiv.org/abs/2410.07801) | Manipulación de material de laboratorio transparente con pose 6D |
| 26 | Robotic Perception of Transparent Objects: A Review | J. Jiang et al. | 2023 | [arXiv:2304.00157](https://arxiv.org/abs/2304.00157) | Revisión del estado del arte en transparencia |
| 27 | Visual servo control, Part I: Basic approaches | F. Chaumette, S. Hutchinson | 2006 | [DOI:10.1109/MRA.2006.250573](https://doi.org/10.1109/MRA.2006.250573) | IBVS, PBVS y matriz de interacción (§3) |
| 28 | Visual servo control, Part II: Advanced approaches | F. Chaumette, S. Hutchinson | 2007 | [DOI:10.1109/MRA.2007.339609](https://doi.org/10.1109/MRA.2007.339609) | Esquemas híbridos, estimación de $L_s$, seguimiento |
| 29 | Photometric visual servoing | C. Collewet, E. Marchand | 2011 | IEEE T-RO 27(4):828–834 | Servo directo sobre intensidades |
| 30 | Visual Servoing from Deep Neural Networks | Q. Bateux, E. Marchand, J. Leitner, F. Chaumette, P. Corke | 2017 | [arXiv:1705.08940](https://arxiv.org/abs/1705.08940) | CNN de pose relativa más PBVS, datos generados automáticamente |
| 31 | Siame-se(3): regression in se(3) for end-to-end visual servoing | S. Felton, E. Fromont, E. Marchand | 2021 | [DOI:10.1109/ICRA48506.2021.9561488](https://doi.org/10.1109/ICRA48506.2021.9561488) | Regresión directa del *twist* en $\mathfrak{se}(3)$ entrenada en simulación |
| 32 | DFVS: Deep Flow Guided Scene Agnostic Image Based Visual Servoing | Y. V. S. Harish et al. | 2020 | [arXiv:2003.03766](https://arxiv.org/abs/2003.03766) | Flujo aprendido más matriz de interacción |
| 33 | Direct Sparse Odometry | J. Engel, V. Koltun, D. Cremers | 2016 | [arXiv:1607.02565](https://arxiv.org/abs/1607.02565) · [GitHub](https://github.com/JakobEngel/dso) | Odometría directa fotométrica en $SE(3)$ |
| 34 | ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM | C. Campos et al. | 2020 | [arXiv:2007.11898](https://arxiv.org/abs/2007.11898) | SLAM de referencia basado en características |
| 35 | DROID-SLAM: Deep Visual SLAM for Monocular, Stereo, and RGB-D Cameras | Z. Teed, J. Deng | 2021 | [arXiv:2108.10869](https://arxiv.org/abs/2108.10869) · [GitHub](https://github.com/princeton-vl/DROID-SLAM) | *Dense BA* diferenciable con lietorch |
| 36 | The invariant extended Kalman filter as a stable observer | A. Barrau, S. Bonnabel | 2014 | [arXiv:1410.1465](https://arxiv.org/abs/1410.1465) | IEKF: error autónomo en grupos de Lie |
| 37 | On-Manifold Preintegration for Real-Time Visual-Inertial Odometry | C. Forster, L. Carlone, F. Dellaert, D. Scaramuzza | 2015 | [arXiv:1512.02363](https://arxiv.org/abs/1512.02363) | Preintegración IMU en $SO(3)$ |
| 38 | Gaussian Splatting SLAM | H. Matsuki, R. Murai, P. H. J. Kelly, A. J. Davison | 2023 | [arXiv:2312.06741](https://arxiv.org/abs/2312.06741) | Seguimiento de cámara con Jacobianos en $\mathfrak{se}(3)$ sobre 3DGS |
| 39 | Vector Neurons: A General Framework for SO(3)-Equivariant Networks | C. Deng et al. | 2021 | [arXiv:2104.12229](https://arxiv.org/abs/2104.12229) · [GitHub](https://github.com/FlyingGiraffe/vnn) | Capas equivariantes simples para nubes de puntos |
| 40 | e3nn: Euclidean Neural Networks | M. Geiger, T. Smidt | 2022 | [arXiv:2207.09453](https://arxiv.org/abs/2207.09453) | Biblioteca general $E(3)$-equivariante (irreps) |
| 41 | SE(3)-Transformers: 3D Roto-Translation Equivariant Attention Networks | F. B. Fuchs, D. E. Worrall, V. Fischer, M. Welling | 2020 | [arXiv:2006.10503](https://arxiv.org/abs/2006.10503) | Atención equivariante a $SE(3)$ |
| 42 | Neural Descriptor Fields: SE(3)-Equivariant Object Representations for Manipulation | A. Simeonov et al. | 2021 | [arXiv:2112.05124](https://arxiv.org/abs/2112.05124) · [GitHub](https://github.com/anthonysimeonov/ndf_robot) | Transferencia de agarres por optimización en $SE(3)$ con pocas demos |
| 43 | Transporter Networks: Rearranging the Visual World for Robotic Manipulation | A. Zeng et al. | 2020 | [arXiv:2010.14406](https://arxiv.org/abs/2010.14406) | *Pick-and-place* $SE(2)$-equivariante y eficiente en muestras |
| 44 | Equivariant Diffusion Policy | D. Wang et al. | 2024 | [arXiv:2407.01812](https://arxiv.org/abs/2407.01812) | Diffusion Policy con *denoiser* equivariante |
| 45 | EquiBot: SIM(3)-Equivariant Diffusion Policy for Generalizable and Data Efficient Learning | J. Yang et al. | 2024 | [arXiv:2407.01479](https://arxiv.org/abs/2407.01479) | Política equivariante a rotación, traslación y escala |
| 46 | Edge Grasp Network: A Graph-Based SE(3)-invariant Approach to Grasp Detection | H. Huang, D. Wang, X. Zhu, R. Walters, R. Platt | 2022 | [arXiv:2211.00191](https://arxiv.org/abs/2211.00191) | Evaluación de agarres invariante a $SE(3)$ |
| 47 | EquiGraspFlow: SE(3)-Equivariant 6-DoF Grasp Pose Generative Flows | B. Lim, J. Kim, J. Kim, Y. Lee, F. C. Park | 2024 | [Proyecto](https://equigraspflow.github.io/) | Flujos generativos en la variedad $SE(3)$ para agarres |
| 48 | Contact-GraspNet: Efficient 6-DoF Grasp Generation in Cluttered Scenes | M. Sundermeyer, A. Mousavian, R. Triebel, D. Fox | 2021 | [arXiv:2103.14127](https://arxiv.org/abs/2103.14127) · [GitHub](https://github.com/NVlabs/contact_graspnet) | Agarres 6-DoF anclados a contactos |
| 49 | AnyGrasp: Robust and Efficient Grasp Perception in Spatial and Temporal Domains | H.-S. Fang et al. | 2022 | [arXiv:2212.08333](https://arxiv.org/abs/2212.08333) | Agarres densos con seguimiento temporal |
| 50 | GraspNet-1Billion: A Large-Scale Benchmark for General Object Grasping | H.-S. Fang, C. Wang, M. Gou, C. Lu | 2020 | [CVF](https://openaccess.thecvf.com/content_CVPR_2020/html/Fang_GraspNet-1Billion_A_Large-Scale_Benchmark_for_General_Object_Grasping_CVPR_2020_paper.html) · [GitHub](https://github.com/graspnet/graspnet-baseline) | Benchmark estándar de agarre 6-DoF |
| 51 | Diffusion Policy: Visuomotor Policy Learning via Action Diffusion | C. Chi et al. | 2023 | [arXiv:2303.04137](https://arxiv.org/abs/2303.04137) | Política visuomotora por difusión, rotación 6D |
| 52 | Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (ACT) | T. Z. Zhao, V. Kumar, S. Levine, C. Finn | 2023 | [arXiv:2304.13705](https://arxiv.org/abs/2304.13705) | ACT y hardware ALOHA (el brazo de nuestra escena) |
| 53 | RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control | A. Brohan et al. | 2023 | [arXiv:2307.15818](https://arxiv.org/abs/2307.15818) | VLA con acciones como tokens |
| 54 | OpenVLA: An Open-Source Vision-Language-Action Model | M. J. Kim et al. | 2024 | [arXiv:2406.09246](https://arxiv.org/abs/2406.09246) · [GitHub](https://github.com/openvla/openvla) | VLA abierto ajustable con LoRA, acciones $\Delta$ discretizadas |
| 55 | Octo: An Open-Source Generalist Robot Policy | Octo Model Team et al. | 2024 | [arXiv:2405.12213](https://arxiv.org/abs/2405.12213) | Política generalista con cabeza de difusión, fácil de ajustar |
| 56 | π0: A Vision-Language-Action Flow Model for General Robot Control | K. Black et al. | 2024 | [arXiv:2410.24164](https://arxiv.org/abs/2410.24164) | VLA con *flow matching*, evaluado en AutoBio |
| 57 | π0.5: a Vision-Language-Action Model with Open-World Generalization | Physical Intelligence et al. | 2025 | [arXiv:2504.16054](https://arxiv.org/abs/2504.16054) | Co-entrenamiento heterogéneo para la generalización |
| 58 | FAST: Efficient Action Tokenization for Vision-Language-Action Models | K. Pertsch et al. | 2025 | [arXiv:2501.09747](https://arxiv.org/abs/2501.09747) | Tokenización DCT de acciones |
| 59 | RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation | S. Liu et al. | 2024 | [arXiv:2410.07864](https://arxiv.org/abs/2410.07864) · [GitHub](https://github.com/thu-ml/RoboticsDiffusionTransformer) | Modelo bimanual evaluado en AutoBio (harness en el repo) |
| 60 | Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots | C. Chi et al. | 2024 | [arXiv:2402.10329](https://arxiv.org/abs/2402.10329) | Acciones relativas en el grupo: invariancia al marco |
| 61 | AutoBio: A Simulation and Benchmark for Robotic Automation in Digital Biology Laboratory | Z. Lan et al. | 2025 | [arXiv:2505.14030](https://arxiv.org/abs/2505.14030) · [GitHub](https://github.com/autobio-bench/AutoBio) | Base de la escena. Muestra que la precisión es el cuello de botella de los VLA |
| 62 | Chemistry3D: Robotic Interaction Benchmark for Chemistry Experiments | (ver arXiv) | 2024 | [arXiv:2406.08160](https://arxiv.org/abs/2406.08160) | Otro benchmark de automatización de laboratorio |
| 63 | Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World | J. Tobin et al. | 2017 | [arXiv:1703.06907](https://arxiv.org/abs/1703.06907) | Fundamento de la aleatorización de dominio (§6.5) |
| 64 | MuJoCo: A physics engine for model-based control | E. Todorov, T. Erez, Y. Tassa | 2012 | [DOI:10.1109/IROS.2012.6386109](https://doi.org/10.1109/IROS.2012.6386109) | Simulador del proyecto |
| 65 | MuJoCo Menagerie | Google DeepMind | 2022– | [GitHub](https://github.com/google-deepmind/mujoco_menagerie) | Modelos de brazos adicionales |
| 66 | Explorations in Homeomorphic Variational Auto-Encoding | L. Falorsi et al. | 2018 | [arXiv:1807.04689](https://arxiv.org/abs/1807.04689) | Latentes en $SO(3)$ por razones topológicas (§7) |
| 67 | Commutative Lie Group VAE for Disentanglement Learning | X. Zhu, C. Xu, D. Tao | 2021 | [arXiv:2106.03375](https://arxiv.org/abs/2106.03375) | Desenmarañamiento como acción de grupo de Lie |
| 68 | Learning Lie Group Symmetry Transformations with Neural Networks | A. Gabel et al. | 2023 | [arXiv:2307.01583](https://arxiv.org/abs/2307.01583) | Descubrimiento de generadores de simetrías |
| 69 | iNeRF: Inverting Neural Radiance Fields for Pose Estimation | L. Yen-Chen et al. | 2020 | [arXiv:2012.05877](https://arxiv.org/abs/2012.05877) | Pose por inversión de un campo de radiancia en $SE(3)$ |
| 70 | BARF: Bundle-Adjusting Neural Radiance Fields | C.-H. Lin, W.-C. Ma, A. Torralba, S. Lucey | 2021 | [arXiv:2104.06405](https://arxiv.org/abs/2104.06405) · [GitHub](https://github.com/chenhsuanlin/bundle-adjusting-NeRF) | Optimización conjunta de NeRF y poses, de grueso a fino |
| 71 | Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection | S. Liu et al. | 2023 | [arXiv:2303.05499](https://arxiv.org/abs/2303.05499) · [GitHub](https://github.com/idea-research/groundingdino) | Detección de "tubo de centrífuga" por texto |
| 72 | SAM 2: Segment Anything in Images and Videos | N. Ravi et al. | 2024 | [arXiv:2408.00714](https://arxiv.org/abs/2408.00714) · [GitHub](https://github.com/facebookresearch/sam2) | Máscaras y seguimiento en vídeo para FoundationPose |

**Notas de verificación.**
- "DEFNet" (servo visual) y "LabPose" (dataset de laboratorio) **no se han podido verificar** como publicaciones y se han sustituido por trabajos existentes (entradas 30–32 y 21–26).
- En las entradas 25 y 62 los autores no se han comprobado individualmente: consúltese el arXiv.
- Los detalles numéricos de AutoBio se citan de forma cualitativa a propósito.
