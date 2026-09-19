# Parte 2 — Procesos de optimización y algoritmos

> **Serie de investigación MAFER Challenge.** Este documento es la parte 2 de 3.
> - Parte 1: [`01_matematicas_grupos_de_lie.md`](01_matematicas_grupos_de_lie.md) — matemática pura: grupos de Lie, álgebras, mapas `exp`/`log`, adjunta, jacobianos izquierdo/derecho, BCH, geometría riemanniana.
> - **Parte 2 (este archivo):** cómo se *optimiza* sobre esas estructuras: descenso riemanniano, Gauss-Newton en SE(3), gradiente natural, políticas geométricas para robots, fine-tuning y un pipeline práctico para nuestra escena MuJoCo.
> - Parte 3: [`03_aplicaciones_vision_por_computador.md`](03_aplicaciones_vision_por_computador.md) — estimación de pose, SLAM, percepción 6-DoF, visión → acción.
>
> Aquí **no** se re-derivan `exp`, `log`, `Ad` ni la fórmula BCH: sólo se enuncian las identidades *operativas* (retracción, jacobiano derecho en las ecuaciones normales, adjunta como transporte) y se remite a la Parte 1 para las demostraciones.

**Contexto del repositorio.** La escena `simulation/models/autobio_lab.xml` monta un brazo ALOHA izquierdo de AutoBio (`third_party/AutoBio/autobio/model/robot/aloha_left.xml`, prefijo `1/aloha:`) con **6 articulaciones de revolución** (`waist`, `shoulder`, `elbow`, `forearm_roll`, `wrist_angle`, `wrist_rotate`), **2 dedos prismáticos**, actuadores de tipo `position` (el control es una consigna articular) y un *site* de efector final `left/gripper`. MuJoCo está fijado a **3.3.0** porque AutoBio trae un plugin precompilado (`libmjlab.so.3.3.0`) y la escena corre en un entorno aparte (`.venv-autobio`, Python 3.11). Estas restricciones condicionan las recomendaciones de la sección F.

## Índice

- [A. Optimización en variedades y grupos de Lie](#a-optimización-en-variedades-y-grupos-de-lie)
- [B. Descenso por gradiente natural](#b-descenso-por-gradiente-natural)
- [C. Aprendizaje y movimiento robótico consciente de la geometría](#c-aprendizaje-y-movimiento-robótico-consciente-de-la-geometría)
- [D. Fine-tuning de políticas robóticas con métodos geométricos](#d-fine-tuning-de-políticas-robóticas-con-métodos-geométricos)
- [E. Geometría de variedades neuronales](#e-geometría-de-variedades-neuronales)
- [F. Pipeline práctico recomendado para el proyecto MuJoCo](#f-pipeline-práctico-recomendado-para-el-proyecto-mujoco)
- [Bibliografía anotada](#bibliografía-anotada)

---

## A. Optimización en variedades y grupos de Lie

### A.1 Intuición

Un problema de robótica típico es *minimizar una función cuyo argumento no vive en $\mathbb{R}^n$*: la pose del efector final $T\in SE(3)$, una orientación $R\in SO(3)$, una trayectoria $\{T_k\}\subset SE(3)^N$. Si parametrizamos con ángulos de Euler o cuaterniones sin restricciones y usamos descenso de gradiente euclídeo, aparecen tres problemas: (i) singularidades (bloqueo de cardán), (ii) redundancias (doble recubrimiento $q\sim -q$), (iii) los pasos se salen de la variedad y hay que "re-proyectar" de forma ad hoc. La optimización riemanniana resuelve esto con una receta de tres piezas:

1. **Gradiente riemanniano** en el espacio tangente $T_xM$ (la dirección de máximo descenso *en la variedad*).
2. **Retracción** $R_x: T_xM\to M$ para "volver" a la variedad tras dar un paso en el tangente.
3. **Transporte vectorial** $\mathcal{T}_{x\to y}$ para comparar/combinar vectores tangentes en puntos distintos (necesario en momentum, gradiente conjugado, Adam, BFGS).

Para grupos de Lie las tres piezas son especialmente baratas: el tangente en cualquier punto se identifica con el álgebra de Lie (vía traslación a izquierda o derecha), la retracción es la exponencial, y el transporte es trivial (o la adjunta), como se ve abajo.

### A.2 Matemática esencial

**Gradiente riemanniano.** Sea $(M,g)$ una variedad riemanniana y $f:M\to\mathbb{R}$. El gradiente riemanniano $\operatorname{grad} f(x)\in T_xM$ se define por
$$
g_x(\operatorname{grad} f(x), \xi) = \mathrm{D}f(x)[\xi]\quad \forall\,\xi\in T_xM .
$$
Para una subvariedad embebida $M\subset\mathbb{R}^n$ con la métrica inducida, $\operatorname{grad} f(x)=P_{T_xM}\big(\nabla \bar f(x)\big)$: proyección ortogonal del gradiente euclídeo de una extensión $\bar f$ (Absil, Mahony & Sepulchre 2008, cap. 3; Boumal 2023, cap. 3).

**Retracción.** Una aplicación suave $R_x:T_xM\to M$ con $R_x(0)=x$ y $\mathrm{D}R_x(0)=\mathrm{id}$. La exponencial riemanniana es una retracción, pero no la única: en $SO(3)$ también sirven la proyección SVD de $R+\xi^\wedge$, la transformada de Cayley o $\mathrm{qf}$ (QR). Una retracción de **segundo orden** coincide con la exponencial hasta segundo orden y conserva la convergencia superlineal de métodos de Newton.

**Descenso de gradiente riemanniano (RGD).**
$$
x_{k+1} = R_{x_k}\!\big(-\alpha_k\,\operatorname{grad} f(x_k)\big).
$$
Con paso de Armijo converge a puntos críticos bajo condiciones análogas al caso euclídeo; Boumal (2023, cap. 4) da cotas de complejidad $O(1/\varepsilon^2)$ para $\|\operatorname{grad} f\|\le\varepsilon$.

**Transporte vectorial.** $\mathcal{T}_{\eta_x}(\xi_x)\in T_{R_x(\eta_x)}M$; el transporte paralelo es un caso particular (costoso). En grupos de Lie con la trivialización a derecha, un vector tangente se almacena como $\tau\in\mathfrak{g}\cong\mathbb{R}^d$ **en todos los puntos**, así que el transporte "por identidad" en coordenadas del álgebra ya es un transporte vectorial válido (no el paralelo de Levi-Civita, pero suficiente para momentum/Adam). Si se cambia de trivialización local ↔ global se usa la adjunta: $\tau^{\text{global}} = \mathrm{Ad}_X\,\tau^{\text{local}}$.

### A.3 Especialización a grupos de Lie (identidades operativas)

Adoptamos la convención "a derecha" (perturbaciones locales, en el marco del cuerpo) de Solà, Deray & Atchuthan (2018) y de la Parte 1:

$$
X\oplus\tau := X\,\mathrm{Exp}(\tau),\qquad Y\ominus X := \mathrm{Log}(X^{-1}Y)\in\mathbb{R}^d .
$$

- **Retracción:** $R_X(\tau)=X\,\mathrm{Exp}(\tau)$ (es la exponencial riemanniana para métricas bi-invariantes en $SO(3)$; en $SE(3)$ no existe métrica bi-invariante, pero sigue siendo una retracción perfectamente válida).
- **Jacobiano "en el tangente":** $\displaystyle \frac{{}^{X}\!\partial f}{\partial X} := \lim_{\tau\to0}\frac{f(X\oplus\tau)\ominus f(X)}{\tau}$. Todo se reduce a jacobianos $d\times d$.
- **Jacobiano derecho** $J_r(\tau)$: $\mathrm{Exp}(\tau+\delta\tau)\approx \mathrm{Exp}(\tau)\,\mathrm{Exp}(J_r(\tau)\delta\tau)$. Aparece en la cadena de derivadas del residuo de pose:
$$
r(X)=\mathrm{Log}(X_\star^{-1}X)\;\Rightarrow\; \frac{\partial r}{\partial \tau}\Big|_{X}=J_r^{-1}\big(r(X)\big).
$$
(La derivación de $J_r$ y de su inversa en forma cerrada para $SO(3)$/$SE(3)$ está en la Parte 1.) En la práctica, cerca del óptimo $r\approx0$ y $J_r^{-1}\approx I$, lo que justifica la aproximación "jacobiano = identidad" que usan muchos solvers.

### A.4 Gauss-Newton y Levenberg-Marquardt en SE(3)

Problema de mínimos cuadrados no lineales sobre una variable de grupo (o producto de grupos y vectores):
$$
\min_{X\in SE(3)}\;\tfrac12\sum_i \|r_i(X)\|^2_{\Sigma_i^{-1}} .
$$
**Idea clave (parametrización local en el tangente):** en cada iteración se linealiza en $\tau\in\mathbb{R}^6$ alrededor del iterado actual, $r_i(X\oplus\tau)\approx r_i(X)+J_i\tau$, se resuelve un problema *euclídeo* en $\tau$ y se retrae.

$$
\underbrace{\Big(\sum_i J_i^\top\Sigma_i^{-1}J_i + \lambda D\Big)}_{H_\lambda}\,\tau^\star = -\sum_i J_i^\top\Sigma_i^{-1} r_i,
\qquad X\leftarrow X\oplus\tau^\star .
$$

- $\lambda=0$: Gauss-Newton. $\lambda>0$: Levenberg-Marquardt (LM), con $D=I$ (amortiguamiento de Levenberg) o $D=\mathrm{diag}(H)$ (Marquardt).
- Regla de actualización de $\lambda$ por *ratio de ganancia* $\rho = \frac{F(X)-F(X\oplus\tau)}{L(0)-L(\tau)}$: si $\rho>0.75$ reducir $\lambda$, si $\rho<0.25$ aumentarlo y rechazar el paso.

```text
Algoritmo LM-en-grupo(X0, residuos r_i, jacobianos-en-tangente J_i)
  X ← X0 ; λ ← 1e-3
  repetir hasta ||g|| < ε o max_iter:
      H ← Σ J_iᵀ Σ_i⁻¹ J_i ;  g ← Σ J_iᵀ Σ_i⁻¹ r_i
      τ ← resolver (H + λ·diag(H)) τ = -g         # sistema 6×6 (o 6N×6N disperso)
      X_new ← X · Exp(τ)                            # retracción
      ρ ← (F(X) - F(X_new)) / (-(gᵀτ + ½ τᵀHτ))
      si ρ > 0: X ← X_new ; λ ← λ·max(1/3, 1-(2ρ-1)³)
      si no:    λ ← 2λ
  devolver X
```

**Pros:** convergencia cuadrática local de GN en problemas con residuos pequeños; sin singularidades de parametrización; todos los sistemas son de tamaño $6N$. **Contras:** mínimos locales (hace falta buena inicialización); $SE(3)$ no tiene métrica bi-invariante, así que la ponderación entre traslación (metros) y rotación (radianes) es una **elección de diseño** ($\Sigma_i$) que afecta al resultado.

### A.5 Adam riemanniano (Bécigneul & Ganea, 2019)

El problema: Adam usa momentos por coordenada, pero en una variedad general "coordenada" no tiene sentido intrínseco. Bécigneul & Ganea (arXiv:1810.00760) lo resuelven en **productos de variedades** $M=M_1\times\dots\times M_n$: la adaptatividad se aplica *por factor* (un escalar $v_i$ por variedad factor, no por coordenada), y el momento se transporta:

$$
\begin{aligned}
g_t^i &= \operatorname{grad}_i f(x_t),\qquad
m_t^i = \beta_1\,\tau_{t-1}^i + (1-\beta_1)\,g_t^i,\qquad
v_t^i = \beta_2 v_{t-1}^i + (1-\beta_2)\,\|g_t^i\|^2_{x_t^i},\\
x_{t+1}^i &= \mathrm{Exp}_{x_t^i}\!\Big(-\alpha\,\frac{m_t^i}{\sqrt{\hat v_t^i}}\Big),\qquad
\tau_t^i = \mathcal{T}_{x_t^i\to x_{t+1}^i}(m_t^i).
\end{aligned}
$$

Para una trayectoria de $N$ poses en $SE(3)^N$, cada pose es un factor. En grupos de Lie con trivialización a derecha, $\mathcal{T}$ es la identidad en coordenadas del álgebra, así que **Riemannian Adam en $SE(3)^N$ equivale a Adam ordinario sobre los $\tau_k\in\mathbb{R}^6$ seguido de la retracción** — con la salvedad de que la versión "correcta" usa un $v$ escalar por pose (o por bloque rotación/traslación) y no por coordenada. Implementaciones: `geoopt.optim.RiemannianAdam` (Kochurov et al., arXiv:2005.02819) y el optimizador de `pypose`.

### A.6 Bibliotecas

| Biblioteca | Lenguaje / backend | Qué aporta | Cuándo usarla aquí |
|---|---|---|---|
| **Pymanopt** (Townsend, Koep & Weichwald 2016; JMLR 17) | Python; autodiff con PyTorch/JAX/TensorFlow/Autograd | Catálogo de variedades (Stiefel, Grassmann, SPD, esferas, $SO(n)$, productos) y solvers (steepest descent, CG, trust-regions) | Prototipos de problemas *pequeños* no estocásticos (calibración, ajuste de una pose) |
| **Geoopt** (Kochurov, Karimov & Kozlukov 2020) | PyTorch | `ManifoldParameter`, `RiemannianSGD`, `RiemannianAdam`; esfera, Stiefel, Poincaré, SPD | Entrenar redes con parámetros restringidos (p.ej. matrices ortogonales, embeddings hiperbólicos) |
| **Theseus** (Pineda et al. 2022, Meta) | PyTorch | Mínimos cuadrados no lineales **diferenciables** (GN, LM, Dogleg) con grupos de Lie `th.SE3`, backward implícito/truncado/unrolled | Capa de optimización dentro de una red (p.ej. IK diferenciable, refinamiento de pose aprendido) |
| **manif** (Deray & Solà) | C++11 header-only + bindings Python | $SO(2/3)$, $SE(2/3)$, $SE_2(3)$, $\mathbb{R}^n$ con **jacobianos analíticos** en el tangente | Referencia didáctica que acompaña a "micro Lie theory"; estimadores C++ |
| **Sophus** (Strasdat) | C++/Eigen | $SO(2/3)$, $SE(2/3)$, $Sim(3)$; base de muchos SLAM | Integración con Ceres/g2o (en mantenimiento desde 2024) |
| **liegroups** (utiasSTARS) | NumPy / PyTorch | $SO(2/3)$, $SE(2/3)$ matriciales | Ya no se mantiene; sustituida por PyMLG |
| **LieTorch** (Teed & Deng, CVPR 2021) | PyTorch + kernels CUDA | *Tangent space backpropagation*: el gradiente de un elemento de grupo se representa en su álgebra | Muy eficiente en GPU; requiere compilar extensiones CUDA |
| **jaxlie** (Yi) | JAX | Dataclasses `SO3`, `SE3`; `jaxlie.manifold.grad`, `rplus`/`rminus`; compatible con `jit`/`vmap` | Pipelines JAX (y su solver hermano `jaxls`) |
| **PyPose** (Wang et al., CVPR 2023) | PyTorch | `LieTensor` (SO3, SE3, Sim3, RxSO3 y álgebras), optimizadores GN/LM con *trust region*, módulos de control (MPC, LQR) y filtros | Opción *pip* pura en PyTorch; recomendada para este repo (ver F) |

---

## B. Descenso por gradiente natural

### B.1 Intuición

El gradiente euclídeo depende de la **parametrización**: si reescalamos un parámetro, cambia la dirección de descenso. Amari (1998) propone medir el tamaño del paso no en el espacio de parámetros $\theta$ sino en el espacio de **distribuciones** $p_\theta$, usando la divergencia KL. El resultado es una dirección *invariante a reparametrizaciones* (al orden uno): el gradiente natural. Esto importa enormemente para políticas robóticas: una política gaussiana cuyo parámetro de desviación típica es pequeño es muy sensible a cambios de la media, y el gradiente natural lo "sabe".

### B.2 Matemática

Máximo descenso con restricción de KL:
$$
\delta^\star = \arg\min_{\delta}\; \mathcal{L}(\theta+\delta)\quad\text{s.a.}\quad \mathrm{KL}\big(p_\theta\,\|\,p_{\theta+\delta}\big)\le\epsilon .
$$
Como $\mathrm{KL}(p_\theta\|p_{\theta+\delta}) = \tfrac12\delta^\top F(\theta)\delta + O(\|\delta\|^3)$, con la **matriz de información de Fisher**
$$
F(\theta)=\mathbb{E}_{x\sim p_\theta}\!\big[\nabla_\theta\log p_\theta(x)\,\nabla_\theta\log p_\theta(x)^\top\big],
$$
el multiplicador de Lagrange da
$$
\tilde\nabla\mathcal{L} = F(\theta)^{-1}\nabla_\theta\mathcal{L},\qquad \theta_{k+1}=\theta_k-\eta\,F^{-1}\nabla\mathcal{L}.
$$
$F$ es el tensor métrico de Fisher-Rao: el gradiente natural **es** el gradiente riemanniano de la sección A aplicado a la variedad estadística $\{p_\theta\}$ (con la retracción trivial $\theta+\delta$).

**Visión de Martens (arXiv:1412.1193, JMLR 2020).** Para pérdidas de verosimilitud negativa con salida en familia exponencial, $F$ coincide con la matriz de **Gauss-Newton generalizada** $G = J^\top H_\ell J$ ($J$: jacobiano de la salida de la red, $H_\ell$: hessiana de la pérdida respecto a la salida). Por tanto el gradiente natural es un método de *segundo orden* aproximado, y hereda sus herramientas: amortiguamiento tipo Tikhonov $(F+\lambda I)^{-1}$, *trust regions*, ajuste de $\lambda$ por ratio de reducción (exactamente como en LM de A.4). Martens también advierte contra la **Fisher empírica** (usar las etiquetas del dataset en vez de muestrear del modelo), que no tiene las mismas garantías.

**Paralelismo explícito con A.4:** LM en $SE(3)$ resuelve $(J^\top J+\lambda D)\tau=-J^\top r$; el gradiente natural amortiguado resuelve $(F+\lambda I)\delta=-\nabla\mathcal{L}$ con $F\approx J^\top H_\ell J$. Son la misma idea en dos variedades distintas (la de poses y la de distribuciones).

### B.3 K-FAC (Martens & Grosse, 2015)

Invertir $F$ ($P\times P$ con $P$ en millones) es inviable. K-FAC (arXiv:1503.05671) aproxima el bloque de Fisher de cada capa densa $s=Wa$ como un producto de Kronecker:
$$
F_{\ell}\approx \underbrace{\mathbb{E}[a a^\top]}_{A_{\ell-1}}\otimes\underbrace{\mathbb{E}[g g^\top]}_{G_\ell},\qquad g=\nabla_s\log p,
$$
y usa $(A\otimes G)^{-1}=A^{-1}\otimes G^{-1}$, de modo que la actualización es
$$
\Delta W_\ell = -\eta\; G_\ell^{-1}\,(\nabla_{W_\ell}\mathcal{L})\,A_{\ell-1}^{-1}.
$$
Coste: invertir matrices del tamaño de la entrada y la salida de la capa (p.ej. $256\times256$), actualizables cada $T$ pasos. En RL, ACKTR (Wu et al. 2017) aplicó K-FAC a actor-crítico.

### B.4 Shampoo y parientes

Shampoo (Gupta, Koren & Singer, arXiv:1802.09568) mantiene un precondicionador por *modo* del tensor de pesos: para una matriz $W\in\mathbb{R}^{m\times n}$,
$$
L_t = L_{t-1}+G_tG_t^\top,\quad R_t=R_{t-1}+G_t^\top G_t,\quad W_{t+1}=W_t-\eta\,L_t^{-1/4}G_tR_t^{-1/4}.
$$
Estructuralmente es "K-FAC con estadísticas de gradiente en lugar de activaciones", y trabajos posteriores lo interpretan como una aproximación de Kronecker a la Fisher/Gauss-Newton. Es el tipo de precondicionador que hoy se usa en entrenamiento a gran escala.

### B.5 Gradiente natural de política (Kakade 2001) → TRPO → PPO

Para una política $\pi_\theta(a|s)$ con retorno esperado $J(\theta)$, Kakade (NIPS 2001) define
$$
F(\theta)=\mathbb{E}_{s\sim d^{\pi},\,a\sim\pi_\theta}\big[\nabla\log\pi_\theta(a|s)\nabla\log\pi_\theta(a|s)^\top\big],\qquad \tilde\nabla J = F^{-1}\nabla J,
$$
y demuestra que con aproximadores compatibles el gradiente natural apunta hacia la acción *greedy* del crítico, no sólo "a una acción mejor".

**TRPO** (Schulman et al., arXiv:1502.05477) convierte esto en un problema con *trust region* explícita:
$$
\max_\theta\; \mathbb{E}\Big[\tfrac{\pi_\theta(a|s)}{\pi_{\theta_{\text{old}}}(a|s)}\hat A(s,a)\Big]\quad\text{s.a.}\quad \bar{\mathrm{KL}}(\pi_{\theta_{\text{old}}}\|\pi_\theta)\le\delta .
$$
En la práctica: dirección $F^{-1}g$ por **gradiente conjugado** con productos Fisher-vector (sin formar $F$), paso máximo $\sqrt{2\delta/(g^\top F^{-1}g)}$ y *line search* que verifica la KL. Es literalmente gradiente natural + tamaño de paso adaptativo.

**PPO** (Schulman et al., arXiv:1707.06347) sustituye la restricción por un *clipping* de primer orden:
$$
L^{\text{CLIP}}(\theta)=\mathbb{E}\big[\min\big(\rho_t\hat A_t,\;\mathrm{clip}(\rho_t,1-\epsilon,1+\epsilon)\hat A_t\big)\big],\qquad \rho_t=\tfrac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)} .
$$
Relación: PPO es un sustituto barato de la región de confianza KL; no calcula $F$, pero la "geometría KL" sigue presente en el clipping del ratio y, en la variante con penalización adaptativa, en el término $\beta\,\mathrm{KL}$. Muchos equipos combinan PPO con *early stopping* por KL objetivo (`target_kl`), que es la aproximación práctica más cercana a un paso natural.

**Pros / contras.** Gradiente natural y TRPO: invariancia, pasos más grandes y estables, menos sensibles a la escala de las acciones. Contras: coste (CG, productos Fisher-vector), mal escalado a redes muy grandes (ViT/VLA). PPO: simple, robusto, estándar de facto en simulación masiva; pero la restricción es sólo aproximada.

### B.6 Descenso espejo (mirror descent)

Dado un potencial estrictamente convexo $\psi$ con divergencia de Bregman $D_\psi$,
$$
x_{k+1}=\arg\min_x\;\langle\nabla f(x_k),x\rangle+\tfrac1\eta D_\psi(x,x_k)\;\Longleftrightarrow\;\nabla\psi(x_{k+1})=\nabla\psi(x_k)-\eta\nabla f(x_k).
$$
Raskutti & Mukherjee (arXiv:1310.7780) prueban que el descenso espejo con $D_\psi$ **es** gradiente natural en la variedad hessiana $(\nabla^2\psi)$, en coordenadas duales. Con $\psi$ = entropía negativa se obtiene la actualización multiplicativa/exponenciada sobre el símplex, que es la forma de las políticas "soft" en RL (p.ej. mirror-descent policy optimization). Moraleja: *trust region KL, gradiente natural y descenso espejo son tres caras de la misma geometría*.

### B.7 Vista riemanniana / de Mahalanobis

Cualquier precondicionador SPD $P$ define una métrica $\langle u,v\rangle_P=u^\top P v$ y el paso $-P^{-1}\nabla f$ es el máximo descenso en esa métrica (distancia de Mahalanobis). Adam ($P=\mathrm{diag}(\sqrt{v})$), K-FAC ($P\approx$ Fisher de Kronecker), Shampoo, Newton ($P=\nabla^2 f$) y el gradiente natural ($P=F$) son todos puntos en ese espectro. En robótica aparece lo mismo en el **espacio de configuraciones**: la matriz de inercia $M(q)$ es la métrica "natural" del brazo (energía cinética $\tfrac12\dot q^\top M\dot q$), y la IK ponderada $\Delta q = M^{-1}J^\top(JM^{-1}J^\top)^{-1}\xi$ es un paso natural con métrica $M$ — la conexión que explotan RMPflow y las geometric fabrics (sección C).

### B.8 Gradiente natural de Wasserstein

En lugar de Fisher-Rao se puede usar la métrica de transporte óptimo $W_2$, que tiene en cuenta la **geometría del espacio muestral** (dos gaussianas con soporte disjunto tienen KL infinita pero $W_2$ finita). Li & Montúfar (arXiv:1803.07033) derivan la estructura riemanniana en el símplex a partir de la formulación dinámica de Wasserstein y la reproducen en el espacio de parámetros; Arbel, Gretton, Li & Montúfar (arXiv:1910.09652) dan un estimador escalable (*Kernelized Wasserstein Natural Gradient*) en un RKHS. Relevancia para robótica: acciones continuas en $\mathbb{R}^n$ o $SE(3)$ tienen una geometría de *ground metric* natural; los métodos basados en transporte (flow matching, sección C) heredan esa idea.

---

## C. Aprendizaje y movimiento robótico consciente de la geometría

### C.1 Cinemática inversa como optimización en SE(3)

**Intuición.** Queremos $q\in\mathbb{R}^6$ (las 6 articulaciones del ALOHA) tal que la pose del *site* `left/gripper`, $T(q)=\mathrm{FK}(q)\in SE(3)$, coincida con un objetivo $T_\star$. El error correcto **no** es $\|p-p_\star\|+\|\text{euler}-\text{euler}_\star\|$ sino el logaritmo del error relativo, que es un vector de $\mathbb{R}^6$ (un *twist*):

$$
e(q)=\mathrm{Log}\big(T(q)^{-1}T_\star\big)\in\mathbb{R}^6,\qquad \min_q\;\tfrac12\,e(q)^\top W e(q).
$$

**Jacobiano.** Con el jacobiano geométrico del cuerpo $J_b(q)\in\mathbb{R}^{6\times6}$ (en MuJoCo, `mj_jacSite` devuelve las partes traslacional y rotacional en el marco del mundo; se rotan al marco del *site* con $R^\top$), la linealización es $\frac{\partial e}{\partial q}\approx -J_r^{-1}(e)\,J_b(q)$. Tomando $J_r^{-1}\approx I$:

- **Pseudoinversa (Gauss-Newton):** $\Delta q = J_b^{+}\,e$.
- **Mínimos cuadrados amortiguados (DLS / Levenberg-Marquardt):**
$$
\Delta q = J_b^\top\big(J_bJ_b^\top+\lambda^2 I\big)^{-1}e\;=\;\big(J_b^\top J_b+\lambda^2I\big)^{-1}J_b^\top e .
$$
El amortiguamiento $\lambda$ acota $\|\Delta q\|$ cerca de singularidades a costa de precisión (Buss 2004 lo analiza vía SVD: los valores singulares $\sigma_i$ se reemplazan por $\sigma_i/(\sigma_i^2+\lambda^2)$).
- **Con métrica:** $\Delta q = W_q^{-1}J^\top(JW_q^{-1}J^\top+\lambda^2I)^{-1}e$; con $W_q=M(q)$ es la IK "dinámicamente consistente" (paso natural, B.7).
- **Con restricciones:** límites articulares, velocidades, colisiones → QP en $\Delta q$ (lo que hace **mink**, ver F).

```text
IK-LM(T⋆, q0):
  q ← q0
  para k = 1..K:
      T ← FK(q) ; e ← Log(T⁻¹ T⋆)             # error en el tangente (marco del efector)
      si ||e||_W < tol: salir
      J ← jacobiano_cuerpo(q)                  # 6×6
      Δq ← (JᵀWJ + λ²I)⁻¹ JᵀW e
      q ← clip(q + α Δq, q_min, q_max)         # en MuJoCo: mj_integratePos para articulaciones libres/bola
  devolver q
```

**Pros:** error intrínseco (sin singularidades de Euler), convergencia rápida, trivial de implementar. **Contras:** local; la ponderación metros/radianes ($W$) es arbitraria — una elección razonable es escalar la traslación por una longitud característica (≈0,3 m para el ALOHA).

Referencia: Lynch & Park, *Modern Robotics* (2017), cap. 6 (IK numérica con twists y producto de exponenciales); Solà et al. (arXiv:1812.01537).

### C.2 Optimización de trayectorias

Sea $\xi=\{q_1,\dots,q_N\}$ (o $\{T_1,\dots,T_N\}\subset SE(3)$). Objetivo típico: $\mathcal{U}(\xi)=\mathcal{F}_{\text{obs}}(\xi)+\lambda\,\mathcal{F}_{\text{smooth}}(\xi)$.

| Método | Idea | Geometría | Pros | Contras |
|---|---|---|---|---|
| **CHOMP** (Zucker et al., IJRR 2013, doi:10.1177/0278364913488805) | Gradiente *funcional* covariante: $\xi\leftarrow\xi-\eta A^{-1}\nabla\mathcal{U}$, $A=K^\top K$ (matriz de diferencias finitas) | Precondiciona con la métrica de suavidad → invariante a reparametrización temporal (un gradiente natural en el espacio de trayectorias) | Rápido, suave | Mínimos locales; restricciones duras sólo por proyección |
| **TrajOpt** (Schulman et al., IJRR 2014, doi:10.1177/0278364914528132) | Programación convexa secuencial (SQP con *trust region*) + colisión continua con distancias con signo | Pasos acotados en región de confianza; las poses se linealizan en el tangente | Restricciones duras, colisión continua | Más pesado; necesita solver QP |
| **STOMP** (Kalakrishnan et al., ICRA 2011) | Muestrea trayectorias ruidosas $\epsilon\sim\mathcal{N}(0,R^{-1})$ y promedia con pesos $e^{-S/\lambda}$ | Ruido con covarianza $R^{-1}$ = la misma métrica de suavidad de CHOMP | Sin gradientes (costes no diferenciables) | Muchas evaluaciones |
| **iLQR / DDP en grupos de Lie** (Boutselis & Theodorou, arXiv:1809.07883; Alcan, Abu-Dakka & Kyrki, arXiv:2301.02018) | Expansión cuadrática de dinámica y coste en el álgebra; *backward pass* de Riccati sobre errores $\tau_k=\mathrm{Log}(\bar X_k^{-1}X_k)$ | Coordenadas libres de singularidades; la dinámica de error usa $\mathrm{Ad}$ | Óptimo local de 2º orden, genera ganancias de realimentación | Requiere modelo diferenciable |
| **MPC de estado de error / coste en el álgebra** (Teng et al., arXiv:2203.08728; Teng et al., arXiv:2204.09177) | El error de seguimiento se define en $\mathfrak{g}$; con métrica invariante a izquierda el gradiente del coste es el error del álgebra → Lyapunov cuadrática | La dinámica linealizada del error vive en $\mathfrak{g}$ y puede ser convexa (QP) | Convergencia exponencial global (en el diseño de coste); MPC convexo en tiempo real | Formulación más delicada |

**Esquema iLQR en $SE(3)$ (error-state):**
```text
dado un nominal (X̄_k, ū_k), k=0..N
repetir:
  # linealizar en el tangente
  para k: A_k, B_k ← ∂/∂(τ,δu) de  Log( X̄_{k+1}⁻¹ f(X̄_k ⊕ τ, ū_k + δu) )
          (ℓ_x, ℓ_xx, ℓ_u, ℓ_uu, ℓ_ux) del coste  ℓ(X,u) = ½||Log(X_ref⁻¹ X)||²_Q + ½||u||²_R
  # backward pass (Riccati) en R^6
  V_x, V_xx ← derivadas del coste terminal
  para k = N-1..0:
      Q_uu ← ℓ_uu + B_kᵀ V_xx B_k + μI ;  K_k ← -Q_uu⁻¹ Q_ux ; d_k ← -Q_uu⁻¹ Q_u
      actualizar V_x, V_xx
  # forward pass con retracción
  X_0 ← X̄_0 ; para k: τ_k ← Log(X̄_k⁻¹ X_k) ; u_k ← ū_k + α d_k + K_k τ_k ; X_{k+1} ← f(X_k,u_k)
  line search en α ; ajustar μ (como λ en LM)
```

### C.3 Riemannian Motion Policies y RMPflow

**Intuición.** Cada subtarea (alcanzar un objetivo, evitar un obstáculo, respetar límites) se describe en *su* espacio de tareas $x_i=\phi_i(q)$ como una política de aceleración $\ddot x_i=f_i(x_i,\dot x_i)$ **más una métrica** $A_i(x_i,\dot x_i)\succeq0$ que dice en qué direcciones esa política "importa". Ratliff et al. (arXiv:1801.02854) definen el par $(f,A)$ como una RMP; RMPflow (Cheng et al., arXiv:1811.07049) las combina en un árbol mediante dos operadores:

- **pullback** (de hijo a padre, con $J=\partial\phi/\partial q$):
$$
A_q=\sum_i J_i^\top A_i J_i,\qquad f_q=A_q^{+}\sum_i J_i^\top A_i\big(f_i-\dot J_i\dot q\big).
$$
- **pushforward**: propagar $(x,\dot x)$ de padre a hijos.

La acción resultante es la solución de mínimos cuadrados ponderados $\ddot q^\star=\arg\min_{\ddot q}\sum_i\|J_i\ddot q+\dot J_i\dot q-f_i\|^2_{A_i}$ — de nuevo la estructura $(J^\top AJ)^{-1}J^\top A$ de Gauss-Newton/gradiente natural. Los autores señalan explícitamente la analogía con las transformaciones covariantes del gradiente natural. Cheng et al. dan condiciones de estabilidad cuando las RMP son *geométricas dinámicas* (GDS).

**Geometric fabrics** (Van Wyk, Ratliff et al., arXiv:2109.10443) generalizan la mecánica clásica a geometrías de Finsler "dobladas" (*bent*) y recuperan garantías de estabilidad que las RMP generales pierden; son la base de controladores reactivos de NVIDIA (y hay trabajo posterior que usa fabrics como "medio guía seguro" para aprender políticas, arXiv:2405.02250).

**Pros:** reactivo (1 kHz), composicional, interpretable; perfecto como *capa de seguridad* bajo una política aprendida. **Contras:** diseño manual de métricas; mínimos locales (no planifica).

### C.4 Geometría riemanniana para aprendizaje de habilidades

- **Gaussianas en variedades** (Calinon, arXiv:1909.05946, IEEE RAM 2020): GMM/GMR, fusión de información y LQR donde la media vive en $S^3$, $SO(3)$ o SPD y la covarianza en el tangente en la media; el cálculo de la media es un Gauss-Newton iterativo $\mu\leftarrow\mathrm{Exp}_\mu\big(\tfrac1N\sum\mathrm{Log}_\mu(x_i)\big)$.
- **Bayesian optimization geométrica** (Jaquier et al., arXiv:2111.01460, CoRL 2021): núcleos de Matérn riemannianos (vía espectro del Laplace-Beltrami) en esferas, $SO(3)$, SPD; útil para *afinar pocos parámetros* de un controlador (rigideces de impedancia, orientaciones de agarre) con muy pocas evaluaciones.
- **Teoría unificadora** (Jaquier & Asfour, arXiv:2209.15539, ISRR 2022): argumentan que la geometría riemanniana (métrica de inercia, geodésicas, sinergias) es el marco natural para generar movimientos coordinados y energéticamente eficientes.
- **Primitivas de movimiento en variedades**: ProMP de orientación (arXiv:2110.15036), habilidades estables en variedades (arXiv:2208.13267); la receta común es proyectar demostraciones al tangente de un punto base, aprender allí y retraer.
- **Variedades aprendidas** (Beik-Mohammadi et al., arXiv:2106.04315, RSS 2021; versión reactiva arXiv:2203.07761): un VAE sobre posición+orientación del efector induce una métrica *pullback* (sección E); las **geodésicas** de esa métrica son movimientos parecidos a las demostraciones, y se esquivan obstáculos deformando la métrica ambiente en línea.

### C.5 Modelos generativos en SE(3): difusión y flow matching

**Diffusion Policy** (Chi et al., arXiv:2303.04137): la política es un proceso de difusión condicional que genera bloques de acciones ("action chunks") con control de horizonte deslizante; maneja multimodalidad mucho mejor que la regresión MSE. Las acciones suelen ser euclídeas (posición + 6D de rotación).

**SE(3)-DiffusionFields** (Urain et al., arXiv:2209.03855, ICRA 2023): aprende un campo de *score* sobre $SE(3)$ para poses de agarre y lo usa como **función de coste suave** dentro de la optimización de trayectorias, resolviendo agarre y movimiento conjuntamente. El ruido se inyecta en el álgebra: $H_{t}=H\,\mathrm{Exp}(\epsilon)$, $\epsilon\sim\mathcal{N}(0,\sigma_t^2I)$, y el muestreo es Langevin con pasos retraídos $H\leftarrow H\,\mathrm{Exp}\big(\tfrac{\alpha}{2}\nabla_\tau\log p+\sqrt{\alpha}\,z\big)$.

**Riemannian Flow Matching** (Chen & Lipman, arXiv:2302.03660, ICLR 2024): entrena un campo vectorial $v_\theta(x,t)\in T_xM$ que regresa sobre un campo objetivo condicional definido por una *premétrica*; en variedades "simples" (grupos de Lie, esferas) la trayectoria objetivo es la geodésica y el objetivo es cerrado:
$$
x_t=x_0\,\mathrm{Exp}\big(t\,\mathrm{Log}(x_0^{-1}x_1)\big),\qquad u_t=\frac{\mathrm{Log}(x_t^{-1}x_1)}{1-t},\qquad
\mathcal{L}=\mathbb{E}\,\|v_\theta(x_t,t)-u_t\|^2_{x_t}.
$$
Sin simulación ni cálculo de divergencias. Aplicaciones robóticas: **RFMP** (Braun, Jaquier, Rozo & Asfour, arXiv:2403.10672) — políticas visuomotoras en variedades con trayectorias más suaves e inferencia más rápida que Diffusion Policy; **EquiGraspFlow** (Lim et al., CoRL 2024, PMLR v270) — flujos de agarre 6-DoF $SE(3)$-equivariantes por construcción.

```python
# Riemannian Flow Matching en SE(3) para acciones de pose (esquema, pypose)
import torch, pypose as pp
def rfm_loss(v_theta, obs, T1):                  # T1: poses objetivo (demos), pp.SE3 [B]
    T0 = pp.randn_SE3(T1.shape[0])               # ruido base (o prior centrado en la pose actual)
    t  = torch.rand(T1.shape[0], 1)
    d  = (T0.Inv() @ T1).Log()                   # twist geodésico en se(3), [B,6]
    Tt = T0 @ pp.se3(t * d).Exp()                # punto en la geodésica
    ut = d                                        # velocidad constante en coordenadas del cuerpo (≡ Log(Tt⁻¹T1)/(1-t))
    return ((v_theta(Tt, t, obs) - ut) ** 2).sum(-1).mean()
# Muestreo: T ← T0; para k: T ← T @ pp.se3(dt * v_theta(T, t_k, obs)).Exp()
```

### C.6 Políticas equivariantes

Si rotar/trasladar la escena debe rotar/trasladar la acción, conviene que la red lo cumpla **por construcción** ($\pi(g\cdot o)=g\cdot\pi(o)$): menos datos, mejor generalización.

- **SO(2)-Equivariant RL** (Wang, Walters & Platt, arXiv:2203.04439, ICLR 2022): DQN y SAC equivariantes para manipulación desde arriba.
- **Equivariant Diffusion Policy** (Wang et al., arXiv:2407.01812): el denoiser es equivariante (SO(2) y extensiones).
- **EquiBot** (Yang et al., arXiv:2407.01479): difusión $SIM(3)$-equivariante (rotación, traslación y escala) sobre nubes de puntos; muy eficiente en datos.

Relación con la optimización: una red equivariante restringe el espacio de parámetros a un subespacio invariante, lo que **reduce la dimensión efectiva** del problema y elimina direcciones "inútiles" del paisaje de pérdida (ver E.4).

---

## D. Fine-tuning de políticas robóticas con métodos geométricos

### D.1 Modelos base: VLA y políticas generativas

- **OpenVLA** (Kim et al., arXiv:2406.09246): VLA de 7B (Llama 2 + DINOv2/SigLIP) entrenado con 970k demostraciones; las acciones se **discretizan** en tokens (256 bins por dimensión de $\Delta$pose del efector + pinza). Soporta fine-tuning con LoRA.
- **π0** (Black et al., arXiv:2410.24164): VLM preentrenado + *action expert* entrenado con **flow matching** que genera *chunks* de acciones continuas; fine-tuning a tareas nuevas con pocas horas de datos.
- **AutoBio** (Lan et al., arXiv:2505.14030, ICLR 2026) — el benchmark cuyos assets usamos — evalúa precisamente VLAs (π0, RDT…) en protocolos de laboratorio y muestra que la precisión y las interacciones con instrumentos son el cuello de botella: justo donde un buen tratamiento de la geometría de la acción ayuda.

### D.2 Fine-tuning con RL y regiones de confianza

El fine-tuning supervisado (SFT) con demostraciones propias es el primer paso; RL sirve para superar el techo de las demostraciones. El problema técnico: PPO necesita $\log\pi_\theta(a|s)$, que una política de difusión/flujo no da de forma trivial.

- **DPPO** (Ren et al., arXiv:2409.00588, ICLR 2025): trata los $K$ pasos de denoising como un **MDP de dos niveles**; cada paso es una gaussiana con log-verosimilitud explícita, y se aplica PPO (clipping) a toda la cadena. Estable y con buena transferencia sim-to-real.
- **ReinFlow** (arXiv:2505.22094, NeurIPS 2025; código en github.com/ReinFlow/ReinFlow): inyecta **ruido aprendible** en el camino determinista de un flujo, convirtiéndolo en un proceso de Markov discreto con verosimilitud exacta; funciona con 1–4 pasos de integración y soporta π0/π0.5. Reporta ~63 % menos tiempo de reloj que DPPO.
- Fine-tuning por RL de políticas de flow matching en VLAs: arXiv:2510.09976.

**Lectura "natural-gradient".** Todas estas variantes controlan el cambio de la política en KL (clipping del ratio, `target_kl`, penalización $\beta\,\mathrm{KL}(\pi_\theta\|\pi_{\text{ref}})$ respecto al modelo base). Recomendación práctica para fine-tuning de un modelo preentrenado:
$$
\max_\theta\;L^{\text{CLIP}}(\theta)\;-\;\beta\,\mathbb{E}_s\,\mathrm{KL}\big(\pi_\theta(\cdot|s)\,\|\,\pi_{\text{base}}(\cdot|s)\big),
$$
donde el segundo término es un *ancla* (evita olvidar lo aprendido por imitación) y la KL por paso de denoising se calcula en forma cerrada entre gaussianas.

### D.3 LoRA y la perspectiva de variedades de bajo rango

LoRA (Hu et al., arXiv:2106.09685) congela $W_0$ y aprende $\Delta W=BA$ con $B\in\mathbb{R}^{m\times r}$, $A\in\mathbb{R}^{r\times n}$, $r\ll\min(m,n)$. Geométricamente, $\Delta W$ vive en la **variedad de matrices de rango $\le r$**, y la factorización $BA$ tiene una simetría $GL(r)$: $(B,A)\sim(BG,G^{-1}A)$ representa la misma $\Delta W$. El descenso de gradiente sobre $(B,A)$ no es invariante a esa simetría (depende del "gauge"), lo que produce inestabilidad y sensibilidad al learning rate.

**Riemannian Preconditioned LoRA** (Zhang & Pilanci, arXiv:2402.02347, ICML 2024) corrige esto con precondicionadores $r\times r$ derivados de una métrica riemanniana en la variedad de rango fijo:
$$
\nabla_A\leftarrow (B^\top B+\delta I)^{-1}\nabla_A,\qquad \nabla_B\leftarrow \nabla_B\,(AA^\top+\delta I)^{-1},
$$
coste despreciable ($r$ pequeño) y mucha más robustez a hiperparámetros con SGD/AdamW. Es el ejemplo más directo de "optimización consciente de la geometría" aplicable **hoy** a fine-tuning de un VLA.

### D.4 Pérdidas en SO(3)/SE(3)

Sea $R,\hat R\in SO(3)$. Métricas estándar (Huynh 2009, doi:10.1007/s10851-009-0161-2):

| Pérdida | Fórmula | Comentario |
|---|---|---|
| **Geodésica** | $d_g(R,\hat R)=\|\mathrm{Log}(R^\top\hat R)\|=\arccos\!\big(\tfrac{\mathrm{tr}(R^\top\hat R)-1}{2}\big)$ | Intrínseca, bi-invariante; gradiente singular en $0$ y $\pi$ (usar `acos` con *clamp*, o $d_g^2$ vía `Log`) |
| **Cordal** | $d_c=\|R-\hat R\|_F=2\sqrt2\,\sin(d_g/2)$ | Suave, barata, equivalente a la geodésica para ángulos pequeños; subpondera errores grandes |
| **Cuaternión** | $1-|\langle q,\hat q\rangle|$ o $\min(\|q-\hat q\|,\|q+\hat q\|)$ | Tener en cuenta el doble recubrimiento |
| **SE(3) en el tangente** | $\|\mathrm{Log}(T^{-1}\hat T)\|^2_W$ | Rotación y traslación acopladas; $W$ fija la escala |
| **SE(3) desacoplada** | $\|p-\hat p\|^2+\gamma\,d_g(R,\hat R)^2$ | Más interpretable; es lo habitual en políticas |

**Representación de salida de la red.** Zhou et al. (arXiv:1812.07035, CVPR 2019) prueban que toda representación de $SO(3)$ en $\mathbb{R}^{\le4}$ es discontinua (Euler, cuaterniones, eje-ángulo) y proponen la **representación 6D** (dos columnas + Gram-Schmidt). Recomendación: la red emite 6D o 9D (+SVD), y la pérdida es geodésica o cordal sobre la matriz resultante.

### D.5 Espacios de acción en el tangente (deltas de pose como twists)

Opciones para la salida de una política de brazo:

1. **Posiciones articulares absolutas** $q_{t+1}$: coincide con los actuadores `position` del ALOHA; sencillo pero no transfiere entre robots y es sensible a la configuración.
2. **Deltas articulares** $\Delta q$: suaves y siempre factibles; poco interpretables en la escena (la misma $\Delta q$ mueve el efector de forma distinta según $q$).
3. **Pose absoluta del efector** $T_{t+1}$: requiere IK; buena para agarres (lo que genera EquiGraspFlow/DiffusionFields).
4. **Twist del efector** $\xi_t\in\mathfrak{se}(3)\cong\mathbb{R}^6$: $T_{t+1}=T_t\,\mathrm{Exp}(\xi_t\,\Delta t)$. Es **invariante a la elección del marco mundo** si se expresa en el marco del efector, vive en un espacio vectorial (la red puede emitir $\mathbb{R}^6$ sin restricciones), y compone con IK diferencial en una línea ($\Delta q = J_b^{\dagger_\lambda}\xi\Delta t$).

Importante al entrenar sobre *chunks*: sumar twists sólo es exacto al primer orden ($\mathrm{Exp}(a)\mathrm{Exp}(b)\ne\mathrm{Exp}(a+b)$, BCH en la Parte 1); por eso es preferible expresar el *chunk* como poses relativas a la pose actual $\{T_t^{-1}T_{t+k}\}$ y convertir cada una con `Log`, en vez de acumular twists incrementales. OpenVLA y la mayoría de datasets usan "deltas de pose del efector" con rotación en Euler: conviene convertirlos a twist/6D antes de entrenar.

### D.6 Resumen de decisiones para fine-tuning

| Decisión | Opción recomendada | Motivo geométrico |
|---|---|---|
| Representación de rotación en la salida | 6D (Zhou et al.) o twist $\mathbb{R}^6$ relativo | Continuidad; espacio vectorial sin restricciones |
| Pérdida de imitación | $\|p-\hat p\|^2+\gamma\,d_g^2$ o RFM en $SE(3)$ | Métrica intrínseca |
| Adaptador | LoRA + precondicionador riemanniano $r\times r$ | Invariancia a la simetría $GL(r)$ de $BA$ |
| RL | PPO/DPPO/ReinFlow con `target_kl` + ancla KL al modelo base | Región de confianza ≈ paso natural |
| Política pequeña (MLP gaussiana) | TRPO/NPG exacto o K-FAC (ACKTR) | Asequible con < 1M parámetros |

---

## E. Geometría de variedades neuronales

### E.1 Geometría de Fisher y NTK del espacio de parámetros

Sea $f_\theta:\mathcal{X}\to\mathbb{R}^k$ la red y $J_\theta=\partial f_\theta(X)/\partial\theta\in\mathbb{R}^{Nk\times P}$ el jacobiano sobre un lote. Dos objetos gemelos:

$$
\underbrace{F=\tfrac1N J_\theta^\top H_\ell J_\theta}_{P\times P\ \text{(Fisher / GGN, espacio de parámetros)}}\qquad
\underbrace{\Theta=J_\theta J_\theta^\top}_{Nk\times Nk\ \text{(NTK empírico, espacio de funciones)}} .
$$

Comparten los valores propios no nulos (para $H_\ell=I$). El **NTK** (Jacot, Gabriel & Hongler, arXiv:1806.07572) describe la dinámica del descenso de gradiente *en el espacio de funciones*: $\dot f_t=-\Theta\,\nabla_f\mathcal{L}$; en el límite de anchura infinita $\Theta$ es constante. El gradiente natural, en cambio, produce $\dot f_t=-\Theta(\Theta+\lambda I)^{-1}\nabla_f\mathcal{L}\approx-\nabla_f\mathcal{L}$ cuando $\Theta$ es invertible: **el gradiente natural "blanquea" el NTK** y hace que todas las direcciones del espacio de funciones converjan a la misma velocidad. Karakida, Akaho & Amari (arXiv:1806.01316 y "Pathological spectra…", arXiv:1910.05992) muestran que el espectro de la Fisher en redes profundas es *patológico*: la mayoría de autovalores ≈ 0 y unos pocos enormes. Consecuencias prácticas:

- El learning rate máximo estable lo fija $\lambda_{\max}(F)$ (o de la hessiana): de ahí el valor del amortiguamiento/*warmup*.
- Las direcciones de autovalor ~0 son direcciones "planas": cambiar $\theta$ ahí apenas cambia la política. En fine-tuning esto justifica LoRA (el cambio útil vive en un subespacio de baja dimensión) y el ancla KL (medir el cambio en el espacio de distribuciones y no en $\|\Delta\theta\|$).

### E.2 Geometría del paisaje de pérdida

Li et al. (arXiv:1712.09913) introducen la *normalización por filtros* para visualizar cortes 2D del paisaje y muestran que arquitecturas con conexiones residuales producen mínimos más anchos y convexos. Dos lecciones para nuestro caso: (i) la "anchura" de un mínimo depende de la parametrización (una reparametrización de escala la cambia), por eso las medidas invariantes (Fisher, KL) son más fiables que $\|\nabla^2\mathcal{L}\|$ bruto; (ii) políticas con residuos + normalización son más fáciles de afinar con RL sin colapsar.

### E.3 Métricas pullback y geometría del espacio latente

Un decodificador $g:\mathcal{Z}\subset\mathbb{R}^d\to\mathcal{X}$ induce en el latente la métrica **pullback**
$$
G(z)=J_g(z)^\top J_g(z)\qquad\big(\text{estocástica: } \mathbb{E}[G(z)]=J_\mu^\top J_\mu+J_\sigma^\top J_\sigma\big),
$$
de modo que la longitud de una curva latente $\gamma$ es la longitud de su imagen: $L(\gamma)=\int\sqrt{\dot\gamma^\top G(\gamma)\dot\gamma}\,dt$. Arvanitidis, Hansen & Hauberg (arXiv:1710.11379, ICLR 2018) muestran que (a) la interpolación lineal en el latente atraviesa regiones sin datos, (b) añadir el término de varianza $J_\sigma$ (que crece lejos de los datos) hace que las **geodésicas eviten zonas sin soporte** — exactamente el comportamiento deseado para interpolar movimientos plausibles.

**Geodésicas latentes para movimiento.** Algoritmo (Beik-Mohammadi et al., arXiv:2106.04315):

```text
entrenar VAE sobre estados del efector x=(p, R) de demostraciones   # decoder con varianza calibrada
dado z_a=enc(x_inicio), z_b=enc(x_objetivo):
   parametrizar γ(t) con spline cúbico de K puntos de control, γ(0)=z_a, γ(1)=z_b
   minimizar la energía E(γ)=Σ_k ||g(γ(t_{k+1})) - g(γ(t_k))||² / Δt   (discretización de ∫ γ̇ᵀ G γ̇)
      + penalización de obstáculos:  G ← G + α·c_obs(g(z))·I   (métrica ambiente deformada en línea)
   ejecutar x(t)=g(γ(t)) con IK de C.1
```

Minimizar la energía (y no la longitud) da geodésicas parametrizadas a velocidad constante. En el ambiente $\mathcal{X}$ la parte de orientación debe usar distancia geodésica de $SO(3)$ (la versión de los autores decodifica posición en $\mathbb{R}^3$ y orientación en $S^3$).

### E.4 Optimización consciente de simetrías

- **Equivariancia por construcción** (C.6): reduce el espacio de hipótesis.
- **Simetrías del paisaje de parámetros:** muchas transformaciones $\theta\mapsto g\cdot\theta$ dejan $\mathcal{L}$ invariante (reescalados entre capas ReLU, $GL(r)$ en LoRA). *Symmetry teleportation* (Zhao et al., arXiv:2205.10637) aprovecha esas simetrías para "teletransportar" los parámetros dentro del conjunto de nivel hacia puntos con mayor norma de gradiente, acelerando la convergencia de SGD/AdaGrad.
- **Invariancia del optimizador:** gradiente natural, K-FAC y el precondicionador riemanniano de LoRA son (aprox.) invariantes a reparametrizaciones afines por capa; Adam no. Si el fine-tuning es inestable ante cambios de escala de la acción (metros vs radianes), es síntoma de que el optimizador no es invariante: normalizar acciones o usar métodos invariantes.

### E.5 Conexión con visión por computador

El codificador visual de un VLA induce una métrica pullback similar en el espacio de observaciones; la Parte 3 ([`03_aplicaciones_vision_por_computador.md`](03_aplicaciones_vision_por_computador.md)) trata la estimación de pose 6-DoF y cómo las poses estimadas (en $SE(3)$) alimentan los costes de esta parte. Aquí basta con notar que un estimador de pose entrenado con pérdida geodésica (D.4) produce errores directamente comparables con el residuo $\mathrm{Log}(T^{-1}T_\star)$ de la IK.

---

## F. Pipeline práctico recomendado para el proyecto MuJoCo

### F.1 Restricciones del repositorio que condicionan todo

1. **MuJoCo 3.3.0 fijo** (plugin `libmjlab.so.3.3.0` de AutoBio), entorno `.venv-autobio` (Python 3.11).
2. **MJX / MuJoCo Playground** (arXiv:2502.08844) *no* es la ruta por defecto: MJX implementa un subconjunto de MuJoCo en JAX y no ejecuta plugins nativos compilados como el de AutoBio; además arrastraría otra versión de `mujoco`. Sólo tiene sentido si se construye una escena MJCF "limpia" sin el plugin para entrenamiento masivo en GPU.
3. **mink** (IK diferencial nativa de MuJoCo) es ideal, **pero** sus versiones ≥1.0.0 exigen `mujoco>=3.3.6` (y las ≥1.1.1, `>=3.8.1`). Con MuJoCo 3.3.0 hay que **fijar `mink==0.0.13`** (última versión con `mujoco>=3.1.6`, verificado en PyPI).
4. **LieTorch** requiere compilar extensiones CUDA → evitar. Preferir **PyPose** (PyTorch, `pip install pypose`) para las partes aprendidas/diferenciables, o **jaxlie** si el stack de aprendizaje es JAX.
5. El brazo es de **6 GDL**: sin redundancia, así que no hay espacio nulo para tareas secundarias; la IK es exacta salvo singularidades (muñeca alineada, brazo extendido) → amortiguamiento obligatorio.

### F.2 Decisiones concretas

| Componente | Elección | Alternativa |
|---|---|---|
| Espacio de acción de la política | Twist del efector $\xi\in\mathbb{R}^6$ en el marco del *site* `left/gripper` (+1 escalar de pinza), escalado a $[-1,1]$ | $\Delta q\in\mathbb{R}^6$ (baseline más simple para PPO) |
| Capa de bajo nivel | IK diferencial DLS/QP (mink 0.0.13, o DLS propio con `mj_jacSite`) → consigna `ctrl` de los actuadores `position` | IK LM por lotes con PyPose |
| Coste / recompensa | residuo $\mathrm{Log}(T^{-1}T_\star)$ ponderado + suavidad + límites + éxito | pérdida geodésica desacoplada |
| Demos | Planificador: keyframes $SE(3)$ + interpolación geodésica + IK LM (C.1) | teleop |
| Imitación | Política de flow matching en $SE(3)$ (RFM, C.5) o Diffusion Policy con rotación 6D | BC gaussiana |
| RL | PPO con `target_kl`, ancla KL a la política de imitación; TRPO/NPG si la política es un MLP pequeño | DPPO/ReinFlow para políticas generativas |
| Librerías | `mujoco==3.3.0`, `mink==0.0.13`, `qpsolvers[daqp]`, `pypose`, `torch` | `jaxlie`+`jax` |

### F.3 Capa de acción: twist → articulaciones (DLS nativo)

```python
import numpy as np, mujoco

ARM = ["waist", "shoulder", "elbow", "forearm_roll", "wrist_angle", "wrist_rotate"]
PFX = "1/aloha:left/"

class TwistIK:
    """Convierte un twist en el marco del efector en consignas articulares (actuadores 'position')."""
    def __init__(self, m, lam=0.05, dt=0.02):
        self.m, self.lam, self.dt = m, lam, dt
        self.site = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_SITE, PFX + "gripper")
        jids = [m.joint(PFX + j).id for j in ARM]
        self.dof = np.array([m.jnt_dofadr[j] for j in jids])
        self.qadr = np.array([m.jnt_qposadr[j] for j in jids])
        self.lo, self.hi = m.jnt_range[jids, 0], m.jnt_range[jids, 1]
        self.jacp = np.zeros((3, m.nv)); self.jacr = np.zeros((3, m.nv))

    def __call__(self, d, xi_body):              # xi_body = (v, ω) en el marco del site
        mujoco.mj_jacSite(self.m, d, self.jacp, self.jacr, self.site)
        R = d.site_xmat[self.site].reshape(3, 3)
        # jacobiano del cuerpo: rotar ambas partes (mundo → marco del site); columnas de las 6 articulaciones
        J = np.vstack([R.T @ self.jacp[:, self.dof], R.T @ self.jacr[:, self.dof]])
        dq = J.T @ np.linalg.solve(J @ J.T + self.lam**2 * np.eye(6), xi_body * self.dt)   # DLS
        q = d.qpos[self.qadr] + dq           # articulaciones de revolución: suma directa (mj_integratePos para bolas/libres)
        return np.clip(q, self.lo, self.hi)  # → d.ctrl[actuadores del brazo]
```

Notas: `mj_jacSite` da la velocidad lineal del punto y la angular en el marco mundo; al rotar ambas con $R^\top$ se obtiene el jacobiano "cuerpo" usado con twists locales (para la parte lineal esto es la velocidad del origen del *site* expresada en su marco, que es lo que queremos). Para el error de pose usar `pp.SE3` o `mink.SE3` y su `.log()`; con MuJoCo puro, `mujoco.mju_subQuat(res, q_target, q_actual)` da el error de rotación en el marco local de `q_actual`.

**Versión mink (misma idea, con límites como QP):**
```python
import mink   # pip install "mink==0.0.13"  (compatible con mujoco 3.3.0)
cfg  = mink.Configuration(model); cfg.update(data.qpos)
ee   = mink.FrameTask(frame_name=PFX + "gripper", frame_type="site",
                      position_cost=1.0, orientation_cost=0.3, lm_damping=1.0)
post = mink.PostureTask(model=model, cost=1e-2); post.set_target_from_configuration(cfg)
limits = [mink.ConfigurationLimit(model)]
ee.set_target(T_target)                       # mink.SE3, p.ej. T_actual @ SE3.exp(xi*dt)
vel = mink.solve_ik(cfg, [ee, post], dt, "daqp", 1e-3, limits=limits)
cfg.integrate_inplace(vel, dt)                # luego copiar cfg.q[qadr] a data.ctrl
```
(Nota: la escena contiene otros cuerpos con articulaciones libres — el tubo — así que `Configuration` incluye esos GDL; la `PostureTask` y los límites los mantienen quietos, o se puede construir la configuración sobre un modelo sólo-brazo.)

### F.4 Coste y recompensa en el tangente

Para una subtarea "llevar la pinza a la pose de agarre $T_\star$ del tubo":
$$
r_t=-\big\|W^{1/2}\mathrm{Log}(T_t^{-1}T_\star)\big\|
\;-\;c_1\|\xi_t\|^2\;-\;c_2\|\xi_t-\xi_{t-1}\|^2\;-\;c_3\,\mathbb{1}[\text{colisión}]\;-\;c_4\sum_j \mathrm{barrera}(q_j)\;+\;R_{\text{éxito}}\mathbb{1}[\text{tubo levantado}],
$$
con $W=\mathrm{diag}(1/\ell^2\,I_3,\ I_3)$, $\ell\approx0{,}05$–$0{,}1$ m (1 rad de error "cuesta" como $\ell$ metros). Usar la norma (no su cuadrado) da gradientes de política más uniformes lejos del objetivo; cerca del objetivo añadir un término cuadrático para precisión. Las poses de agarre candidatas pueden venir de un modelo generativo en $SE(3)$ (EquiGraspFlow / DiffusionFields) o, en la escena conocida, del propio MJCF.

### F.5 Generación de demostraciones con optimización en SE(3)

```python
import torch, pypose as pp

def geodesic_keyframes(T_a: pp.LieTensor, T_b: pp.LieTensor, n: int):
    """Interpolación geodésica (constante en el marco del cuerpo) entre dos poses SE3."""
    d = (T_a.Inv() @ T_b).Log()                         # se(3)
    t = torch.linspace(0, 1, n).unsqueeze(-1)
    return T_a @ pp.se3(t * d).Exp()                    # [n] poses

# Fases del agarre: aproximación (pre-grasp 8 cm sobre el tubo) → descenso → cierre → elevación
# Para cada pose objetivo: IK LM (C.1) con warm start en la q anterior → trayectoria articular
# Opcional: refinar la trayectoria completa con un problema de mínimos cuadrados en PyPose/Theseus:
#   residuos = {Log(FK(q_k)^-1 T_k)}  +  {λ (q_{k+1}-2q_k+q_{k-1})}  (suavidad tipo CHOMP)
#   resolver con pp.optim.LevenbergMarquardt (trust region) o con un bucle LM propio.
```

Con 50–200 demostraciones generadas así (aleatorizando la posición del tubo con el `spawner.py` del repo) se entrena la política de imitación.

### F.6 Imitación: flow matching en SE(3) sobre *chunks*

- Observación: estado articular + pose del tubo (o imagen, si se usa el renderer; ver Parte 3).
- Acción: *chunk* de $H=8$–$16$ poses relativas $\Delta T_k=T_t^{-1}T_{t+k}$, representadas como $\mathrm{Log}(\Delta T_k)\in\mathbb{R}^6$ (no acumular twists; ver D.5).
- Pérdida: RFM (C.5) sobre cada $\Delta T_k$ o, si se usa difusión euclídea, sobre $\mathrm{Log}(\Delta T_k)$ normalizados.
- Ejecución: horizonte deslizante; el primer $\Delta T$ se convierte en twist $\xi=\mathrm{Log}(\Delta T_1)/\Delta t$ y pasa por la capa `TwistIK`.

### F.7 Fine-tuning con regiones de confianza

**Ruta A — política pequeña (MLP gaussiana sobre $\xi$):** gradiente natural exacto estilo TRPO; con ~$10^5$ parámetros el gradiente conjugado con productos Fisher-vector es barato.

```python
def fisher_vector_product(policy, obs, v, damping=1e-2):
    """F v sin formar F, usando la KL media como potencial (Hessiana de la KL = Fisher)."""
    dist = policy(obs)                                   # torch.distributions.Normal
    old  = torch.distributions.Normal(dist.mean.detach(), dist.stddev.detach())
    kl   = torch.distributions.kl_divergence(old, dist).sum(-1).mean()
    g    = torch.autograd.grad(kl, policy.parameters(), create_graph=True)
    gv   = torch.cat([x.reshape(-1) for x in g]) @ v
    Hv   = torch.autograd.grad(gv, policy.parameters())
    return torch.cat([x.reshape(-1) for x in Hv]) + damping * v

def npg_step(policy, obs, grad_J, max_kl=0.01):
    s = conjugate_gradient(lambda v: fisher_vector_product(policy, obs, v), grad_J, iters=10)
    step = torch.sqrt(2 * max_kl / (s @ fisher_vector_product(policy, obs, s))) * s
    # + line search que acepte sólo si mejora el sustituto y KL ≤ max_kl  (TRPO)
    return step
```

**Ruta B — política generativa preentrenada (flujo/difusión o VLA):** PPO con
1. `clip_eps=0.1–0.2`, `target_kl≈0.01–0.02` (parar las épocas si se supera: aproximación práctica al paso natural);
2. ancla $\beta\,\mathrm{KL}(\pi_\theta\|\pi_{\text{BC}})$ para no olvidar la imitación;
3. verosimilitudes vía DPPO (cadena de denoising gaussiana) o ReinFlow (ruido aprendible, pocos pasos);
4. si el modelo es grande, sólo LoRA + precondicionador riemanniano (D.3) y la cabeza de acción;
5. el crítico, si es un MLP, se puede entrenar con K-FAC (ACKTR) o simplemente Adam.

**Ruta C — pocos parámetros de alto nivel** (rigidez de la pinza, offset de agarre en $SO(3)$, ganancias): optimización bayesiana geométrica (Jaquier et al.) con núcleos de Matérn en $SO(3)\times\mathbb{R}^n$; 20–50 evaluaciones en simulación.

### F.8 Bucle de entrenamiento (esqueleto)

```python
env = AutoBioTubeEnv("models/autobio_lab.xml")     # wrapper propio en .venv-autobio, mujoco 3.3.0
ik  = TwistIK(env.model, lam=0.05, dt=env.control_dt)
policy = load_bc_policy()                           # F.6
ref    = copy.deepcopy(policy).eval()                # ancla KL
for it in range(N_ITERS):
    batch = rollout(env, policy, ik, n_envs=16)      # procesos CPU paralelos (gymnasium AsyncVectorEnv)
    adv   = gae(batch.rewards, batch.values, γ=0.99, λ=0.95)
    for epoch in range(10):
        loss, kl = ppo_loss(policy, batch, adv, clip=0.2) , approx_kl(policy, batch)
        loss = loss + β * kl_to(ref, policy, batch.obs)
        if kl > 1.5 * target_kl: break               # región de confianza
        opt.step(loss)                                # Adam, o Adam + precondicionador LoRA riemanniano
    log(success_rate, geodesic_err=‖Log(T⁻¹T⋆)‖, kl)
```

### F.9 Métricas y validación

- Error final de posición (mm) y **geodésico** de orientación (grados) — no errores de Euler.
- Tasa de éxito por fase (aproximación, agarre, elevación) y robustez a la aleatorización del *spawner*.
- Suavidad: jerk articular y norma de $\xi_t-\xi_{t-1}$.
- KL por iteración respecto a la política de imitación (debe permanecer acotada).
- Condición del jacobiano $\sigma_{\min}(J_b)$ a lo largo de la trayectoria (detectar cercanía a singularidades).

### F.10 Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Singularidades de muñeca del brazo de 6 GDL | DLS con $\lambda$ adaptativo ($\lambda^2=\lambda_0^2(1-(\sigma_{\min}/\epsilon)^2)$ si $\sigma_{\min}<\epsilon$) |
| Incompatibilidades de versión (mink, MJX) | `mink==0.0.13`; nada de MJX con la escena AutoBio |
| Escala metros/radianes | $W$ explícita y acciones normalizadas por componente |
| Colapso al afinar con RL | `target_kl`, ancla KL, learning rate bajo, LoRA |
| Discontinuidades de rotación | Rotación 6D o twists relativos; nunca Euler en la salida de la red |

---

## Bibliografía anotada

Todas las entradas se verificaron mediante búsqueda web (septiembre de 2026). Se omite la sede de publicación cuando no se confirmó.

| # | Título | Autores | Año | Enlace | Por qué es relevante |
|---|---|---|---|---|---|
| 1 | Optimization Algorithms on Matrix Manifolds | P.-A. Absil, R. Mahony, R. Sepulchre | 2008 | [Princeton UP](https://press.princeton.edu/books/hardcover/9780691132983/optimization-algorithms-on-matrix-manifolds) | Texto clásico: gradiente riemanniano, retracciones, transporte vectorial, Newton y trust-regions en variedades (A). |
| 2 | An Introduction to Optimization on Smooth Manifolds | N. Boumal | 2023 | [Cambridge UP](https://www.cambridge.org/core/books/an-introduction-to-optimization-on-smooth-manifolds/EAF2B35457B7034AC747188DC2FFC058) · [PDF autor](https://nicolasboumal.net/book/) | Referencia moderna y gratuita; complejidad de RGD, convexidad geodésica (A). |
| 3 | A micro Lie theory for state estimation in robotics | J. Solà, J. Deray, D. Atchuthan | 2018 | [arXiv:1812.01537](https://arxiv.org/abs/1812.01537) | Convención $\oplus/\ominus$ y jacobianos en el tangente usados en A.3–A.4 y C.1. |
| 4 | Riemannian Adaptive Optimization Methods | G. Bécigneul, O.-E. Ganea | 2018 | [arXiv:1810.00760](https://arxiv.org/abs/1810.00760) | Adam/AMSGrad riemannianos en productos de variedades (A.5). |
| 5 | Pymanopt: A Python Toolbox for Optimization on Manifolds using Automatic Differentiation | J. Townsend, N. Koep, S. Weichwald | 2016 | [arXiv:1603.03236](https://arxiv.org/abs/1603.03236) · [GitHub](https://github.com/pymanopt/pymanopt) | Toolbox de variedades con autodiff (A.6). |
| 6 | Geoopt: Riemannian Optimization in PyTorch | M. Kochurov, R. Karimov, S. Kozlukov | 2020 | [arXiv:2005.02819](https://arxiv.org/abs/2005.02819) | `RiemannianAdam`/`RiemannianSGD` en PyTorch (A.5–A.6). |
| 7 | Theseus: A Library for Differentiable Nonlinear Optimization | L. Pineda et al. | 2022 | [arXiv:2207.09442](https://arxiv.org/abs/2207.09442) · [GitHub](https://github.com/facebookresearch/theseus) | GN/LM diferenciables con grupos de Lie como capa de red (A.6, F.5). |
| 8 | Tangent Space Backpropagation for 3D Transformation Groups (LieTorch) | Z. Teed, J. Deng | 2021 | [arXiv:2103.12032](https://arxiv.org/abs/2103.12032) · [GitHub](https://github.com/princeton-vl/lietorch) | Retropropagación en el álgebra de Lie; base conceptual de los gradientes en el tangente (A.6). |
| 9 | PyPose: A Library for Robot Learning with Physics-based Optimization | C. Wang et al. | 2022 | [arXiv:2209.15428](https://arxiv.org/abs/2209.15428) · [GitHub](https://github.com/pypose/pypose) | `LieTensor` + optimizadores LM con trust region; librería recomendada en F. |
| 10 | jaxlie — Rigid transforms + Lie groups for JAX | B. Yi | — | [GitHub](https://github.com/brentyi/jaxlie) | $SO(3)$/$SE(3)$ en JAX con `manifold.grad` (A.6). |
| 11 | manif — small C++11 header-only library for Lie theory | J. Deray, J. Solà | — | [GitHub](https://github.com/artivis/manif) | Jacobianos analíticos en el tangente; compañero de (3). |
| 12 | Sophus — C++ implementation of Lie Groups using Eigen | H. Strasdat | — | [GitHub](https://github.com/strasdat/Sophus) | Implementación de referencia en C++/SLAM (A.6). |
| 13 | liegroups — SO2/SE2/SO3/SE3 in numpy or pytorch | utiasSTARS | — | [GitHub](https://github.com/utiasSTARS/liegroups) | Implementación ligera (sin mantenimiento; ver PyMLG) (A.6). |
| 14 | Natural Gradient Works Efficiently in Learning | S. Amari | 1998 | [doi:10.1162/089976698300017746](https://doi.org/10.1162/089976698300017746) | Origen del gradiente natural y la métrica de Fisher (B.2). |
| 15 | New Insights and Perspectives on the Natural Gradient Method | J. Martens | 2014/2020 | [arXiv:1412.1193](https://arxiv.org/abs/1412.1193) | Fisher = Gauss-Newton generalizada; amortiguamiento y trust regions (B.2). |
| 16 | Optimizing Neural Networks with Kronecker-factored Approximate Curvature | J. Martens, R. Grosse | 2015 | [arXiv:1503.05671](https://arxiv.org/abs/1503.05671) | K-FAC: gradiente natural escalable (B.3). |
| 17 | Scalable trust-region method for deep RL using Kronecker-factored approximation (ACKTR) | Y. Wu et al. | 2017 | [arXiv:1708.05144](https://arxiv.org/abs/1708.05144) | K-FAC + trust region en actor-crítico, probado en MuJoCo (B.3, F.7). |
| 18 | Shampoo: Preconditioned Stochastic Tensor Optimization | V. Gupta, T. Koren, Y. Singer | 2018 | [arXiv:1802.09568](https://arxiv.org/abs/1802.09568) | Precondicionador de Kronecker por modos (B.4). |
| 19 | A Natural Policy Gradient | S. Kakade | 2001 | [dblp (NIPS 2001)](https://dblp.org/rec/conf/nips/Kakade01.html) | Gradiente natural aplicado a políticas (B.5). |
| 20 | Trust Region Policy Optimization | J. Schulman et al. | 2015 | [arXiv:1502.05477](https://arxiv.org/abs/1502.05477) | Gradiente natural con restricción KL y CG (B.5, F.7). |
| 21 | Proximal Policy Optimization Algorithms | J. Schulman et al. | 2017 | [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) | Sustituto de primer orden de la trust region; estándar para fine-tuning (B.5, D.2). |
| 22 | The Information Geometry of Mirror Descent | G. Raskutti, S. Mukherjee | 2013 | [arXiv:1310.7780](https://arxiv.org/abs/1310.7780) | Equivalencia descenso espejo ↔ gradiente natural (B.6). |
| 23 | Natural gradient via optimal transport | W. Li, G. Montúfar | 2018 | [arXiv:1803.07033](https://arxiv.org/abs/1803.07033) | Gradiente natural de Wasserstein (B.8). |
| 24 | Kernelized Wasserstein Natural Gradient | M. Arbel, A. Gretton, W. Li, G. Montúfar | 2019 | [arXiv:1910.09652](https://arxiv.org/abs/1910.09652) | Estimador escalable del gradiente natural de Wasserstein (B.8). |
| 25 | Introduction to Inverse Kinematics with Jacobian Transpose, Pseudoinverse and Damped Least Squares Methods | S. R. Buss | 2004 | [UCSD](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/ikmethods/index.html) | Análisis SVD de DLS para IK (C.1, F.3). |
| 26 | Modern Robotics: Mechanics, Planning, and Control | K. M. Lynch, F. C. Park | 2017 | [PDF preprint](https://hades.mech.northwestern.edu/images/7/7f/MR.pdf) | Twists, producto de exponenciales, IK numérica en $SE(3)$ (C.1). |
| 27 | mink — Python inverse kinematics based on MuJoCo | K. Zakka | — | [GitHub](https://github.com/kevinzakka/mink) | IK diferencial por QP nativa de MuJoCo; fijar 0.0.13 para MuJoCo 3.3.0 (F.3). |
| 28 | CHOMP: Covariant Hamiltonian Optimization for Motion Planning | M. Zucker et al. | 2013 | [doi:10.1177/0278364913488805](https://doi.org/10.1177/0278364913488805) | Gradiente funcional covariante (natural) para trayectorias (C.2). |
| 29 | Motion planning with sequential convex optimization and convex collision checking (TrajOpt) | J. Schulman et al. | 2014 | [doi:10.1177/0278364914528132](https://doi.org/10.1177/0278364914528132) | SQP con trust region para planificación (C.2). |
| 30 | STOMP: Stochastic Trajectory Optimization for Motion Planning | M. Kalakrishnan et al. | 2011 | [MPI-IS](https://is.mpg.de/publications/kalakrishnan_raiic_2011) | Optimización de trayectorias sin gradientes (C.2). |
| 31 | Differential Dynamic Programming on Lie Groups | G. Boutselis, E. Theodorou | 2018 | [arXiv:1809.07883](https://arxiv.org/abs/1809.07883) · [GitHub](https://github.com/GeorgeBoutselis/DDP-LieGroups) | DDP libre de coordenadas en grupos de Lie (C.2). |
| 32 | Constrained Trajectory Optimization on Matrix Lie Groups via Lie-Algebraic DDP | G. Alcan, F. J. Abu-Dakka, V. Kyrki | 2023 | [arXiv:2301.02018](https://arxiv.org/abs/2301.02018) | DDP con restricciones en el álgebra (C.2). |
| 33 | Lie Algebraic Cost Function Design for Control on Lie Groups | S. Teng, M. Ghaffari et al. | 2022 | [arXiv:2204.09177](https://arxiv.org/abs/2204.09177) | Costes en el álgebra con convergencia exponencial (C.2, F.4). |
| 34 | An Error-State MPC on Connected Matrix Lie Groups for Legged Robot Control | S. Teng et al. | 2022 | [arXiv:2203.08728](https://arxiv.org/abs/2203.08728) | MPC convexo de estado de error en $\mathfrak{g}$ (C.2). |
| 35 | Riemannian Motion Policies | N. Ratliff, J. Issac, D. Kappler, S. Birchfield, D. Fox | 2018 | [arXiv:1801.02854](https://arxiv.org/abs/1801.02854) | Políticas + métricas; analogía con el gradiente natural (C.3). |
| 36 | RMPflow: A Computational Graph for Automatic Motion Policy Generation | C.-A. Cheng et al. | 2018 | [arXiv:1811.07049](https://arxiv.org/abs/1811.07049) | Combinación geométricamente consistente de RMPs (C.3). |
| 37 | Geometric Fabrics: Generalizing Classical Mechanics to Capture the Physics of Behavior | K. Van Wyk et al. | 2021 | [arXiv:2109.10443](https://arxiv.org/abs/2109.10443) | Estabilidad garantizada con geometrías de Finsler (C.3). |
| 38 | Gaussians on Riemannian Manifolds: Applications for Robot Learning and Adaptive Control | S. Calinon | 2019 | [arXiv:1909.05946](https://arxiv.org/abs/1909.05946) | GMM/GMR/LQR en variedades (C.4). |
| 39 | Geometry-aware Bayesian Optimization in Robotics using Riemannian Matérn Kernels | N. Jaquier et al. | 2021 | [arXiv:2111.01460](https://arxiv.org/abs/2111.01460) | BO en $SO(3)$, esferas, SPD (C.4, F.7 ruta C). |
| 40 | Riemannian geometry as a unifying theory for robot motion learning and control | N. Jaquier, T. Asfour | 2022 | [arXiv:2209.15539](https://arxiv.org/abs/2209.15539) | Marco conceptual riemanniano para movimiento robótico (C.4). |
| 41 | Learning Riemannian Manifolds for Geodesic Motion Skills | H. Beik-Mohammadi et al. | 2021 | [arXiv:2106.04315](https://arxiv.org/abs/2106.04315) | Geodésicas de métricas pullback como habilidades (C.4, E.3). |
| 42 | Reactive Motion Generation on Learned Riemannian Manifolds | H. Beik-Mohammadi et al. | 2022 | [arXiv:2203.07761](https://arxiv.org/abs/2203.07761) | Versión reactiva con evitación de obstáculos (C.4, E.3). |
| 43 | Diffusion Policy: Visuomotor Policy Learning via Action Diffusion | C. Chi et al. | 2023 | [arXiv:2303.04137](https://arxiv.org/abs/2303.04137) | Políticas de difusión con *action chunks* (C.5, F.6). |
| 44 | SE(3)-DiffusionFields | J. Urain et al. | 2022 | [arXiv:2209.03855](https://arxiv.org/abs/2209.03855) | Difusión en $SE(3)$ como coste de agarre + trayectoria (C.5). |
| 45 | Flow Matching on General Geometries | R. T. Q. Chen, Y. Lipman | 2023 | [arXiv:2302.03660](https://arxiv.org/abs/2302.03660) | Riemannian Flow Matching (C.5, F.6). |
| 46 | Riemannian Flow Matching Policy for Robot Motion Learning | M. Braun, N. Jaquier, L. Rozo, T. Asfour | 2024 | [arXiv:2403.10672](https://arxiv.org/abs/2403.10672) | RFM aplicado a políticas visuomotoras (C.5). |
| 47 | EquiGraspFlow: SE(3)-Equivariant 6-DoF Grasp Pose Generative Flows | B. Lim, J. Kim, J. Kim, Y. Lee, F. C. Park | 2024 | [PMLR v270](https://proceedings.mlr.press/v270/lim25a.html) · [GitHub](https://github.com/bdlim99/EquiGraspFlow) | Flujos equivariantes para agarres (C.5, F.4). |
| 48 | SO(2)-Equivariant Reinforcement Learning | D. Wang, R. Walters, R. Platt | 2022 | [arXiv:2203.04439](https://arxiv.org/abs/2203.04439) | RL equivariante para manipulación (C.6). |
| 49 | Equivariant Diffusion Policy | D. Wang et al. | 2024 | [arXiv:2407.01812](https://arxiv.org/abs/2407.01812) | Difusión con denoiser equivariante (C.6). |
| 50 | EquiBot: SIM(3)-Equivariant Diffusion Policy | J. Yang et al. | 2024 | [arXiv:2407.01479](https://arxiv.org/abs/2407.01479) | Equivariancia a rotación/traslación/escala (C.6). |
| 51 | OpenVLA: An Open-Source Vision-Language-Action Model | M. J. Kim et al. | 2024 | [arXiv:2406.09246](https://arxiv.org/abs/2406.09246) · [GitHub](https://github.com/openvla/openvla) | VLA abierto con fine-tuning LoRA (D.1). |
| 52 | π0: A Vision-Language-Action Flow Model for General Robot Control | K. Black et al. | 2024 | [arXiv:2410.24164](https://arxiv.org/abs/2410.24164) | VLA con *action expert* de flow matching (D.1). |
| 53 | AutoBio: A Simulation and Benchmark for Robotic Automation in Digital Biology Laboratory | Lan et al. | 2025 | [arXiv:2505.14030](https://arxiv.org/abs/2505.14030) · [GitHub](https://github.com/autobio-bench/AutoBio) | Origen de la escena y de la evaluación de VLAs en laboratorio (contexto, F). |
| 54 | Diffusion Policy Policy Optimization (DPPO) | A. Z. Ren et al. | 2024 | [arXiv:2409.00588](https://arxiv.org/abs/2409.00588) · [GitHub](https://github.com/irom-princeton/dppo) | PPO sobre la cadena de denoising (D.2, F.7). |
| 55 | ReinFlow: Fine-tuning Flow Matching Policy with Online RL | — | 2025 | [arXiv:2505.22094](https://arxiv.org/abs/2505.22094) · [GitHub](https://github.com/ReinFlow/ReinFlow) | RL para políticas de flujo con ruido aprendible (D.2). |
| 56 | LoRA: Low-Rank Adaptation of Large Language Models | E. Hu et al. | 2021 | [arXiv:2106.09685](https://arxiv.org/abs/2106.09685) | Adaptación de bajo rango (D.3). |
| 57 | Riemannian Preconditioned LoRA for Fine-Tuning Foundation Models | F. Zhang, M. Pilanci | 2024 | [arXiv:2402.02347](https://arxiv.org/abs/2402.02347) · [GitHub](https://github.com/pilancilab/Riemannian_Preconditioned_LoRA) | Precondicionador $r\times r$ desde una métrica riemanniana (D.3). |
| 58 | Metrics for 3D Rotations: Comparison and Analysis | D. Q. Huynh | 2009 | [doi:10.1007/s10851-009-0161-2](https://doi.org/10.1007/s10851-009-0161-2) | Métricas en $SO(3)$ para pérdidas (D.4). |
| 59 | On the Continuity of Rotation Representations in Neural Networks | Y. Zhou et al. | 2019 | [arXiv:1812.07035](https://arxiv.org/abs/1812.07035) | Representación 6D continua (D.4). |
| 60 | Neural Tangent Kernel: Convergence and Generalization in Neural Networks | A. Jacot, F. Gabriel, C. Hongler | 2018 | [arXiv:1806.07572](https://arxiv.org/abs/1806.07572) | Geometría del espacio de funciones (E.1). |
| 61 | Pathological spectra of the Fisher information metric and its variants in deep neural networks | R. Karakida, S. Akaho, S. Amari | 2019 | [arXiv:1910.05992](https://arxiv.org/abs/1910.05992) | Espectro de la Fisher y relación con el NTK (E.1). |
| 62 | Visualizing the Loss Landscape of Neural Nets | H. Li, Z. Xu, G. Taylor, C. Studer, T. Goldstein | 2017 | [arXiv:1712.09913](https://arxiv.org/abs/1712.09913) | Geometría del paisaje de pérdida (E.2). |
| 63 | Latent Space Oddity: on the Curvature of Deep Generative Models | G. Arvanitidis, L. K. Hansen, S. Hauberg | 2017 | [arXiv:1710.11379](https://arxiv.org/abs/1710.11379) | Métrica pullback estocástica y geodésicas latentes (E.3). |
| 64 | Symmetry Teleportation for Accelerated Optimization | B. Zhao et al. | 2022 | [arXiv:2205.10637](https://arxiv.org/abs/2205.10637) | Explotar simetrías del paisaje de parámetros (E.4). |
| 65 | MuJoCo Playground | UC Berkeley, Google DeepMind et al. | 2025 | [arXiv:2502.08844](https://arxiv.org/abs/2502.08844) | Entrenamiento masivo en GPU con MJX (alternativa en F.1). |
