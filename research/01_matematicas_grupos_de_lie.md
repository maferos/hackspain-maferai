# Parte 1 — Fundamentos matemáticos: variedades, grupos de Lie y geometría del movimiento robótico

> **Contexto.** Este documento es la parte 1 de 3 de la investigación del reto MAFER (brazos robóticos simulados en MuJoCo dentro de una escena de laboratorio AutoBio con GC-MS, espectrómetros UV-Vis-NIR y tubos de ensayo). Aquí solo se cubren **las matemáticas puras**. La optimización (gradiente natural, optimización riemanniana, algoritmos) está en [`02_optimizacion_y_algoritmos.md`](02_optimizacion_y_algoritmos.md), y las aplicaciones de visión por computador (estimación de pose, redes equivariantes en la práctica) en [`03_aplicaciones_vision_por_computador.md`](03_aplicaciones_vision_por_computador.md).

---

## 0. Mapa conceptual

```
                    Variedad diferenciable M  (§1)
                 cartas · T_pM · T*_pM · TM · dF_p
                               │
            ┌──────────────────┼─────────────────────────┐
            ▼                  ▼                         ▼
   + estructura de grupo   + métrica riemanniana g    + familia de densidades p(x|θ)
   Grupo de Lie G (§2)     Geometría riemanniana (§4)  Variedad estadística (§6)
   SO(3), SE(3), Sim(3)    M(q) = métrica cinética     métrica de Fisher, conexiones duales
   exp/log, Ad, J_l, J_r   geodésicas, Christoffel     ──► gradiente natural (Parte 2)
            │                  │
            ▼                  ▼
   Cinemática por tornillos (§3)      Dinámica en grupos de Lie (§4)
   PoE: q ∈ C  ──FK──►  T ∈ SE(3)     Euler–Poincaré, RNEA en SE(3)
   Jacobianos, singularidades,
   elipsoide de manipulabilidad
            │
            ▼
   Probabilidad en grupos de Lie (§5): gaussianas concentradas en SE(3),
   propagación de incertidumbre (pose de un tubo vista por cámara)
            │
            ▼
   Acciones de grupo y equivariancia (§7) ── Representación de rotaciones para
   G-CNN, espacios homogéneos, GDL              aprendizaje (§8): cuaterniones, 6D, SVD
            └──────────────────► Visión por computador (Parte 3)
```

**Idea central.** La configuración de un brazo vive en un espacio de juntas $\mathcal{C}$; su efector final vive en el grupo de Lie $SE(3)$; la cinemática directa es una aplicación suave $f:\mathcal{C}\to SE(3)$; la dinámica dota a $\mathcal{C}$ de una métrica riemanniana $M(q)$; y aprender o afinar movimientos exige derivar, promediar y medir incertidumbre respetando estas geometrías (no en $\mathbb{R}^n$ "a ciegas").

---

## 0.1 Convenio de notación (se mantiene en todo el documento)

| Objeto | Convenio |
|---|---|
| Giro (twist) | $\xi = \mathcal{V} = (\omega, v) \in \mathbb{R}^6$ — **rotación primero**, como en Lynch & Park. Solà et al. y Barfoot usan $(\rho,\theta)$ = (traslación, rotación); sus matrices por bloques son las nuestras con los bloques permutados. |
| Llave (wrench) | $\mathcal{F} = (m, f)$ (momento, fuerza), de modo que la potencia es $\mathcal{V}^\top\mathcal{F}$. |
| Hat / vee | $(\cdot)^\wedge:\mathbb{R}^k\to\mathfrak{g}$, $(\cdot)^\vee:\mathfrak{g}\to\mathbb{R}^k$; para $\mathfrak{so}(3)$ escribimos también $[\omega]_\times = \omega^\wedge$. |
| Exponencial | $\exp:\mathfrak{g}\to G$ (matricial); $\mathrm{Exp}(\tau) := \exp(\tau^\wedge)$, $\mathrm{Log}(X) := \log(X)^\vee$. |
| Perturbación por defecto | **Derecha (local, en el marco del cuerpo)**: $X\oplus\tau = X\,\mathrm{Exp}(\tau)$, $\;Y\ominus X = \mathrm{Log}(X^{-1}Y)$. |
| Perturbación izquierda | $\tau\oplus X = \mathrm{Exp}(\tau)X$, $\;Y\ominus X = \mathrm{Log}(YX^{-1})$. Se relacionan mediante $\mathrm{Ad}_X$: $X\,\mathrm{Exp}(\tau) = \mathrm{Exp}(\mathrm{Ad}_X\tau)\,X$. |
| Ángulo | Si $\omega\in\mathbb{R}^3$, $\theta=\lVert\omega\rVert$ y $\hat\omega=\omega/\theta$. En las fórmulas de Jacobianos **$\omega$ no está normalizado** (lleva el ángulo dentro). |

---

## 1. Variedades diferenciables, espacios tangentes y métricas riemannianas

### Intuición
Una variedad es un espacio que "localmente parece $\mathbb{R}^n$" pero cuya forma global puede ser curva o tener agujeros (una esfera, un toro, el conjunto de rotaciones). El espacio tangente $T_pM$ es la "mejor aproximación lineal" de la variedad en un punto: el lugar donde viven las velocidades. Una métrica riemanniana permite medir longitudes y ángulos de esas velocidades.

### Definiciones formales
- **Carta y atlas.** Una variedad topológica $M$ de dimensión $n$ (Hausdorff, segundo numerable) con un atlas $\{(U_\alpha,\varphi_\alpha)\}$, $\varphi_\alpha:U_\alpha\to\varphi_\alpha(U_\alpha)\subset\mathbb{R}^n$ homeomorfismos, es **suave** si todas las funciones de transición $\varphi_\beta\circ\varphi_\alpha^{-1}$ son $C^\infty$ donde están definidas.
- **Espacio tangente.** $T_pM$ puede definirse como (i) clases de equivalencia de curvas $\gamma:(-\epsilon,\epsilon)\to M$, $\gamma(0)=p$, con igual derivada en una carta; o (ii) derivaciones lineales $v:C^\infty(M)\to\mathbb{R}$ que cumplen Leibniz $v(fg)=f(p)v(g)+g(p)v(f)$. En coordenadas, la base es $\{\partial/\partial x^i|_p\}$ y $\dim T_pM=n$.
- **Espacio cotangente.** $T^*_pM = (T_pM)^*$, con base dual $\{dx^i|_p\}$. Los gradientes de funciones $df_p$ son covectores; **las fuerzas/llaves son covectores y las velocidades son vectores**.
- **Fibrado tangente.** $TM=\bigsqcup_{p\in M}T_pM$, variedad de dimensión $2n$; el estado $(q,\dot q)$ de un sistema mecánico vive en $TM$ y el estado hamiltoniano $(q,p)$ en $T^*M$.
- **Diferencial (pushforward).** Para $F:M\to N$ suave, $dF_p:T_pM\to T_{F(p)}N$, $dF_p(v)(h)=v(h\circ F)$. En coordenadas es la matriz Jacobiana $\partial F^a/\partial x^i$. El pullback $F^*$ actúa sobre covectores: $(F^*\alpha)(v)=\alpha(dF_p v)$.
- **Métrica riemanniana.** Un campo suave $g$ de productos internos $g_p:T_pM\times T_pM\to\mathbb{R}$, en coordenadas $g_p(u,v)=u^\top G(p)\,v$ con $G(p)\succ 0$. Longitud de una curva y distancia:
$$L(\gamma)=\int_a^b\sqrt{g_{\gamma(t)}(\dot\gamma,\dot\gamma)}\,dt,\qquad d(p,q)=\inf_{\gamma:p\to q}L(\gamma).$$
- **Geodésicas y mapa exponencial riemanniano.** Las geodésicas cumplen $\ddot x^k+\Gamma^k_{ij}\dot x^i\dot x^j=0$, con símbolos de Christoffel de la conexión de Levi-Civita
$$\Gamma^k_{ij}=\tfrac12 g^{kl}\left(\partial_i g_{jl}+\partial_j g_{il}-\partial_l g_{ij}\right).$$
$\mathrm{Exp}^{R}_p(v)=\gamma_v(1)$ con $\gamma_v(0)=p,\ \dot\gamma_v(0)=v$. **Ojo:** en un grupo de Lie, el exponencial de grupo (§2) coincide con el riemanniano solo si la métrica es bi-invariante (p. ej. $SO(3)$ con su métrica estándar; $SE(3)$ **no** admite métrica riemanniana bi-invariante).
- **Gradiente riemanniano.** $\operatorname{grad}f(p)=G(p)^{-1}\nabla f(p)$: convierte el covector $df$ en vector usando la métrica. Esta es exactamente la estructura del gradiente natural (§6 y Parte 2).

### Por qué importa para el brazo
Las posiciones articulares, la pose del efector (en $SE(3)$), la orientación de un tubo de ensayo y la distribución de probabilidad de una política son puntos de variedades distintas. Los errores de pose, las velocidades y los pasos de optimización viven en espacios tangentes; las fuerzas y gradientes en cotangentes. Confundir ambos (p. ej. "restar" dos matrices de rotación) produce resultados que ni siquiera pertenecen a la variedad.

### Referencias clave
- J. M. Lee, *Introduction to Smooth Manifolds*, 2ª ed., Springer GTM 218 (2012). [doi:10.1007/978-1-4419-9982-5](https://link.springer.com/book/10.1007/978-1-4419-9982-5)
- P.-A. Absil, R. Mahony, R. Sepulchre, *Optimization Algorithms on Matrix Manifolds*, Princeton UP (2008). [press.princeton.edu](https://press.princeton.edu/books/hardcover/9780691132983/optimization-algorithms-on-matrix-manifolds)
- N. Boumal, *An Introduction to Optimization on Smooth Manifolds*, Cambridge UP (2023). [doi:10.1017/9781009166164](https://doi.org/10.1017/9781009166164)

---

## 2. Grupos de Lie y álgebras de Lie

### Intuición
Un grupo de Lie es una variedad que además es un grupo, con operaciones suaves. Sus elementos son "transformaciones" (rotar, trasladar, escalar). El álgebra de Lie $\mathfrak{g}=T_eG$ es el espacio tangente en la identidad: las "velocidades infinitesimales". El exponencial "enrolla" una velocidad constante sobre el grupo, y el logaritmo la desenrolla. Solà et al. resumen el uso práctico con dos operadores, $\oplus$ y $\ominus$, que permiten tratar el grupo *localmente* como un espacio vectorial.

### Definiciones formales
- **Grupo de Lie.** $G$ variedad suave con $\mu:(g,h)\mapsto gh$ e $\iota:g\mapsto g^{-1}$ suaves. **Álgebra de Lie** $\mathfrak{g}=T_eG$ con el corchete $[A,B]=AB-BA$ (en grupos matriciales).
- **Grupos relevantes.**

| Grupo | Definición | $\dim$ | Álgebra |
|---|---|---|---|
| $SO(2)$ | $\{R\in\mathbb{R}^{2\times2}: R^\top R=I,\ \det R=1\}\cong S^1$ | 1 | $\theta^\wedge=\begin{pmatrix}0&-\theta\\ \theta&0\end{pmatrix}$ |
| $SE(2)$ | $\begin{pmatrix}R&t\\0&1\end{pmatrix}$, $R\in SO(2), t\in\mathbb{R}^2$ | 3 | $(\theta,\rho)$ |
| $SO(3)$ | $\{R\in\mathbb{R}^{3\times3}: R^\top R=I,\ \det R=1\}$ | 3 | $[\omega]_\times=\begin{pmatrix}0&-\omega_3&\omega_2\\ \omega_3&0&-\omega_1\\ -\omega_2&\omega_1&0\end{pmatrix}$ |
| $SE(3)$ | $T=\begin{pmatrix}R&p\\0&1\end{pmatrix}$ | 6 | $\xi^\wedge=\begin{pmatrix}[\omega]_\times&v\\0&0\end{pmatrix}$ |
| $Sim(3)$ | $\begin{pmatrix}sR&t\\0&1\end{pmatrix}$, $s>0$ | 7 | añade $\sigma=\log s$ (útil en SLAM monocular con escala ambigua) |

- **Exponencial de $SO(3)$ — fórmula de Rodrigues.** Con $\theta=\lVert\omega\rVert$, $\hat\omega=\omega/\theta$:
$$\mathrm{Exp}(\omega)=\exp([\omega]_\times)=I+\sin\theta\,[\hat\omega]_\times+(1-\cos\theta)\,[\hat\omega]_\times^2 .$$
Logaritmo: $\theta=\arccos\!\big(\tfrac{\operatorname{tr}R-1}{2}\big)$, $[\omega]_\times=\tfrac{\theta}{2\sin\theta}(R-R^\top)$ para $\theta\in(0,\pi)$ (casos $\theta\to0$ y $\theta=\pi$ se tratan aparte).
- **Exponencial de $SE(3)$.** Para $\xi=(\omega,v)$:
$$\mathrm{Exp}(\xi)=\begin{pmatrix}\mathrm{Exp}(\omega)&V(\omega)\,v\\0&1\end{pmatrix},\qquad V(\omega)=I+\frac{1-\cos\theta}{\theta^2}[\omega]_\times+\frac{\theta-\sin\theta}{\theta^3}[\omega]_\times^2,$$
con $\omega$ **sin normalizar**; cuando $\theta\to0$, $V\to I$ (traslación pura). Nótese que $V(\omega)=J_l(\omega)$, el Jacobiano izquierdo de $SO(3)$. Para $SE(2)$: $V(\theta)=\frac1\theta\begin{pmatrix}\sin\theta&-(1-\cos\theta)\\ 1-\cos\theta&\sin\theta\end{pmatrix}$.
- **Adjunta.** $\mathrm{Ad}_g:\mathfrak{g}\to\mathfrak{g}$, $\mathrm{Ad}_g(\tau^\wedge)=g\,\tau^\wedge g^{-1}$; transporta velocidades de un marco a otro. En nuestro convenio:
$$\mathrm{Ad}_R=R\ \ (SO(3)),\qquad \mathrm{Ad}_T=\begin{pmatrix}R&0\\ [p]_\times R&R\end{pmatrix}\ \ (SE(3)).$$
La adjunta del álgebra es su derivada: $\mathrm{ad}_\xi\eta=[\xi^\wedge,\eta^\wedge]^\vee$, con
$$\mathrm{ad}_\xi=\begin{pmatrix}[\omega]_\times&0\\ [v]_\times&[\omega]_\times\end{pmatrix},\qquad \mathrm{Ad}_{\mathrm{Exp}(\xi)}=\exp(\mathrm{ad}_\xi).$$
- **Operadores $\oplus/\ominus$ (Solà et al.).** Perturbación derecha: $X\oplus\tau=X\,\mathrm{Exp}(\tau)$, $Y\ominus X=\mathrm{Log}(X^{-1}Y)\in T_X G$ (expresado en coordenadas locales). Identidad clave: $X\,\mathrm{Exp}(\tau)=\mathrm{Exp}(\mathrm{Ad}_X\tau)\,X$, que convierte perturbaciones locales en globales.
- **Jacobianos de Lie.** Solà define la derivada de $f:G\to H$ como
$$\frac{{}^{X}\!Df(X)}{DX}=\lim_{\tau\to0}\frac{f(X\oplus\tau)\ominus f(X)}{\tau}\in\mathbb{R}^{m\times n}.$$
El **Jacobiano derecho** de $\mathrm{Exp}$ en $SO(3)$ es
$$J_r(\omega)=I-\frac{1-\cos\theta}{\theta^2}[\omega]_\times+\frac{\theta-\sin\theta}{\theta^3}[\omega]_\times^2,\qquad J_l(\omega)=J_r(-\omega)=R\,J_r(\omega),$$
$$J_r^{-1}(\omega)=I+\tfrac12[\omega]_\times+\left(\frac1{\theta^2}-\frac{1+\cos\theta}{2\theta\sin\theta}\right)[\omega]_\times^2 .$$
Propiedades de uso diario (primer orden):
$$\mathrm{Exp}(\omega+\delta)\approx\mathrm{Exp}(\omega)\,\mathrm{Exp}(J_r(\omega)\delta),\qquad \mathrm{Log}\big(\mathrm{Exp}(\omega)\,\mathrm{Exp}(\delta)\big)\approx\omega+J_r^{-1}(\omega)\,\delta .$$
En $SE(3)$ los Jacobianos son $6\times6$ con bloques $J_r(\omega)$ en la diagonal y un bloque $Q(\omega,v)$ fuera de ella (fórmula cerrada en Barfoot, y en Solà et al., App. D, con el orden $(\rho,\theta)$).
- **Fórmula BCH (Baker–Campbell–Hausdorff).**
$$\log(e^{A}e^{B})=A+B+\tfrac12[A,B]+\tfrac1{12}\big([A,[A,B]]+[B,[B,A]]\big)+\dots$$
En la práctica no se usa la serie: sus versiones "linealizadas" son precisamente $J_l^{-1}$ y $J_r^{-1}$: $\mathrm{Log}(\mathrm{Exp}(\omega)\mathrm{Exp}(\delta))\approx \omega+J_r^{-1}(\omega)\delta$ y $\mathrm{Log}(\mathrm{Exp}(\delta)\mathrm{Exp}(\omega))\approx\omega+J_l^{-1}(\omega)\delta$.
- **Topología.** $SO(3)\cong\mathbb{RP}^3$, $\pi_1(SO(3))=\mathbb{Z}_2$; $SE(3)\cong SO(3)\ltimes\mathbb{R}^3$ (producto semidirecto). El exponencial de $SO(3)$ y de $SE(3)$ es sobreyectivo.

### Por qué importa para el brazo
Cuando el controlador del brazo debe llevar la pinza desde su pose actual $T$ a la pose de agarre $T^\star$ de un tubo en la gradilla, el error correcto es $e=T^\star\ominus T=\mathrm{Log}(T^{-1}T^\star)\in\mathbb{R}^6$ (un giro en el marco de la pinza), no $T^\star-T$. Integrar velocidades medidas ($T_{k+1}=T_k\,\mathrm{Exp}(\mathcal{V}_b\Delta t)$) preserva la ortogonalidad exactamente, y los Jacobianos $J_r$ permiten derivar costes de pose para la optimización (Parte 2). La adjunta traduce giros entre el marco del mundo (la mesa del laboratorio), el del cuerpo (la pinza) y el de la cámara.

### Referencias clave
- J. Solà, J. Deray, D. Atchuthan, "A micro Lie theory for state estimation in robotics" (2018). [arXiv:1812.01537](https://arxiv.org/abs/1812.01537)
- T. D. Barfoot, *State Estimation for Robotics*, Cambridge UP (2017). [doi:10.1017/9781316671528](https://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser17.pdf)
- C. Hertzberg, R. Wagner, U. Frese, L. Schröder, "Integrating generic sensor fusion algorithms with sound state representations through encapsulation of manifolds", *Information Fusion* (2013). [arXiv:1107.1119](https://arxiv.org/abs/1107.1119) — origen de los operadores $\boxplus/\boxminus$.
- J. Solà, "Quaternion kinematics for the error-state Kalman filter" (2017). [arXiv:1711.02508](https://arxiv.org/abs/1711.02508)

---

## 3. Cinemática robótica mediante teoría de tornillos

### Intuición
Toda articulación revoluta o prismática produce un movimiento de tornillo (rotación alrededor de un eje + traslación a lo largo de él). Por el teorema de Chasles, *todo* desplazamiento rígido es un tornillo. La cinemática directa de un brazo serie es, por tanto, un producto de exponenciales de tornillos: la **fórmula del Producto de Exponenciales (PoE)** de Brockett (1984), una alternativa sin singularidades de parametrización a Denavit–Hartenberg.

### Definiciones formales
- **Espacio de configuración.** Para $n$ juntas, $\mathcal{C}\subseteq (S^1)^{r}\times\mathbb{R}^{n-r}$ ($r$ revolutas, $n-r$ prismáticas). Si las $r$ revolutas son de giro ilimitado, esa parte es el toro $T^r$. **Precisión importante:** un brazo real de 6–7 GDL (como los de la escena MuJoCo) tiene *límites articulares* (`range` en MJCF), de modo que $\mathcal{C}$ es en la práctica una caja compacta $\prod_i[q_i^{\min},q_i^{\max}]\subset\mathbb{R}^n$, topológicamente trivial. Por eso las cartas globales (ángulos articulares) funcionan bien para planificar localmente, pero los argumentos de topología global del toro no se trasladan directamente.
- **Giro y llave.** Velocidad espacial y del cuerpo de $T(t)\in SE(3)$:
$$[\mathcal{V}_s]=\dot T\,T^{-1},\qquad [\mathcal{V}_b]=T^{-1}\dot T,\qquad \mathcal{V}_s=\mathrm{Ad}_T\,\mathcal{V}_b .$$
Una llave $\mathcal{F}=(m,f)\in\mathfrak{se}(3)^*$ es un covector; bajo cambio de marco $\mathcal{F}_b=\mathrm{Ad}_T^\top\mathcal{F}_s$, y la potencia $\mathcal{V}^\top\mathcal{F}$ es invariante.
- **Eje de tornillo.** Para una revoluta con eje unitario $\hat\omega$ que pasa por un punto $q$: $\mathcal{S}=(\hat\omega,\,-\hat\omega\times q)$; para una prismática con dirección $\hat v$: $\mathcal{S}=(0,\hat v)$.
- **Producto de exponenciales.** Con $M\in SE(3)$ la pose del efector en la configuración cero:
$$T(\theta)=e^{[\mathcal{S}_1]\theta_1}e^{[\mathcal{S}_2]\theta_2}\cdots e^{[\mathcal{S}_n]\theta_n}M\quad\text{(espacio)},\qquad T(\theta)=M\,e^{[\mathcal{B}_1]\theta_1}\cdots e^{[\mathcal{B}_n]\theta_n}\quad\text{(cuerpo)},$$
con $\mathcal{B}_i=\mathrm{Ad}_{M^{-1}}\mathcal{S}_i$. La cinemática directa es la aplicación suave $f:\mathcal{C}\to SE(3)$.
- **Jacobianos espacial y del cuerpo.** $\mathcal{V}_s=J_s(\theta)\dot\theta$, $\mathcal{V}_b=J_b(\theta)\dot\theta$, con columnas
$$J_{s,i}=\mathrm{Ad}_{e^{[\mathcal{S}_1]\theta_1}\cdots e^{[\mathcal{S}_{i-1}]\theta_{i-1}}}\mathcal{S}_i,\qquad J_{b,i}=\mathrm{Ad}_{e^{-[\mathcal{B}_n]\theta_n}\cdots e^{-[\mathcal{B}_{i+1}]\theta_{i+1}}}\mathcal{B}_i,\qquad J_b=\mathrm{Ad}_{T^{-1}}J_s .$$
Geométricamente, $J_b(\theta)$ es la diferencial $df_\theta$ expresada en la trivialización izquierda de $T\,SE(3)$. Por dualidad (trabajo virtual), $\tau=J^\top\mathcal{F}$.
- **Singularidades.** $\theta$ es singular si $\operatorname{rank}J(\theta)<\min(n,6)$. Clasificación típica: de frontera (brazo totalmente extendido), internas (ejes alineados, p. ej. "wrist singularity" cuando los ejes 4 y 6 son colineales).
- **Manipulabilidad (Yoshikawa, 1985).** La imagen de la bola unidad de velocidades articulares $\lVert\dot\theta\rVert\le1$ es el elipsoide
$$\mathcal{E}=\{\dot x:\ \dot x^\top\big(J J^\top\big)^{-1}\dot x\le1\},$$
con semiejes $\sigma_i\,u_i$ (SVD $J=U\Sigma V^\top$). Índices: $w(\theta)=\sqrt{\det(JJ^\top)}=\prod_i\sigma_i$ (volumen), el número de condición $\kappa=\sigma_{\max}/\sigma_{\min}$ (isotropía, *destreza*) y $\sigma_{\min}$ (distancia a la singularidad). El elipsoide de fuerza es el dual: $\mathcal{F}^\top(JJ^\top)\mathcal{F}\le1$. Para mezclar rotación y traslación hay que escalar (unidades distintas): no existe un producto interno natural en $\mathfrak{se}(3)$.
- **Cinemática inversa diferencial.** $\dot\theta=J^\dagger\mathcal{V}+(I-J^\dagger J)\dot\theta_0$; cerca de singularidades se usa la pseudoinversa amortiguada $J^\top(JJ^\top+\lambda^2I)^{-1}$. Iteración de Newton en el grupo: $\theta\leftarrow\theta+J_b^\dagger(\theta)\,\mathrm{Log}\big(T(\theta)^{-1}T^\star\big)$.

### Por qué importa para el brazo
PoE da un modelo cinemático *coordinado-libre*, fácil de calibrar y directamente compatible con MuJoCo (que define cada junta por eje y posición). Cuando el brazo se estira para alcanzar la boca de inyección del GC-MS o el porta-cubetas del UV-Vis al fondo de la mesa alargada, se acerca a una singularidad de frontera: $\sigma_{\min}\to0$ y las velocidades articulares necesarias explotan. Maximizar $w(\theta)$ o minimizar $\kappa$ como término de coste (en el espacio nulo si el brazo es redundante) mantiene al robot diestro durante la manipulación de tubos. Las zonas de "spawn" de tubos deberían ubicarse dentro de la región de buena manipulabilidad.

### Referencias clave
- R. W. Brockett, "Robotic manipulators and the product of exponentials formula", *Mathematical Theory of Networks and Systems*, LNCIS 58 (1984). [doi:10.1007/BFb0031048](https://link.springer.com/chapter/10.1007/BFb0031048)
- K. M. Lynch, F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge UP (2017). [PDF preprint oficial](http://hades.mech.northwestern.edu/images/2/2e/MR-largefont-v2.pdf)
- R. M. Murray, Z. Li, S. S. Sastry, *A Mathematical Introduction to Robotic Manipulation*, CRC Press (1994). [Web del libro (Caltech)](https://www.cds.caltech.edu/~murray/books/MLS/)
- T. Yoshikawa, "Manipulability of Robotic Mechanisms", *IJRR* 4(2) (1985). [doi:10.1177/027836498500400201](https://journals.sagepub.com/doi/10.1177/027836498500400201)

---

## 4. Geometría riemanniana del espacio de configuración y dinámica en grupos de Lie

### Intuición
La energía cinética de un brazo es una forma cuadrática en las velocidades articulares: $K=\tfrac12\dot q^\top M(q)\dot q$. Esa matriz de masa $M(q)$ es **una métrica riemanniana** sobre $\mathcal{C}$. Con ella, el movimiento libre de fuerzas (sin gravedad, sin par) sigue **geodésicas**, y los términos de Coriolis/centrífugos no son más que los símbolos de Christoffel de esa métrica. Interpolar en línea recta en el espacio articular no es, por tanto, el camino "más corto" en energía.

### Definiciones formales
- **Métrica cinética.** Si el eslabón $i$ tiene matriz de inercia espacial $\mathcal{G}_i\in\mathbb{R}^{6\times6}$ (en su marco) y Jacobiano del cuerpo $J_i(q)$:
$$K=\tfrac12\sum_i\mathcal{V}_i^\top\mathcal{G}_i\mathcal{V}_i=\tfrac12\dot q^\top M(q)\dot q,\qquad M(q)=\sum_i J_i(q)^\top\mathcal{G}_i J_i(q)\succ0 .$$
- **Ecuaciones de Euler–Lagrange.** Con $L=K-P$:
$$M(q)\ddot q+C(q,\dot q)\dot q+g(q)=\tau,\qquad (C\dot q)_i=\sum_{j,k}\Gamma_{ijk}\dot q_j\dot q_k,$$
$$\Gamma_{ijk}=\tfrac12\left(\frac{\partial M_{ij}}{\partial q_k}+\frac{\partial M_{ik}}{\partial q_j}-\frac{\partial M_{jk}}{\partial q_i}\right),\qquad C_{ij}(q,\dot q)=\sum_k\Gamma_{ijk}\dot q_k .$$
$\Gamma_{ijk}$ son los símbolos de Christoffel de primera especie de la métrica $M$. Con $\tau=0$, $g=0$ se obtiene $\ddot q^k+\Gamma^k_{ij}\dot q^i\dot q^j=0$: **la ecuación geodésica**.
- **Pasividad.** Con la factorización de Christoffel, $\dot M-2C$ es antisimétrica. Esto es una *elección*: existen infinitas matrices $C$ con el mismo producto $C\dot q$; Wensing & Slotine (2023) muestran que las factorizaciones que cumplen la antisimetría corresponden a conexiones afines compatibles con la métrica, y cómo elegirlas.
- **Dinámica de un cuerpo rígido en $SE(3)$ (Newton–Euler en el grupo).** En el marco del cuerpo:
$$\mathcal{F}_b=\mathcal{G}_b\dot{\mathcal{V}}_b-\mathrm{ad}_{\mathcal{V}_b}^\top\mathcal{G}_b\mathcal{V}_b .$$
- **Euler–Poincaré.** Para un lagrangiano invariante por la izquierda $\ell(\xi)$ en $\mathfrak{g}$ (reducción de $TG$ a $\mathfrak{g}$), las ecuaciones de movimiento son
$$\frac{d}{dt}\frac{\partial\ell}{\partial\xi}=\mathrm{ad}^*_{\xi}\frac{\partial\ell}{\partial\xi},\qquad \dot g=g\,\xi^\wedge .$$
En $SO(3)$ con $\ell=\tfrac12\omega^\top I\omega$ se recuperan las ecuaciones de Euler $I\dot\omega=(I\omega)\times\omega$.
- **Algoritmo recursivo de Newton–Euler geométrico (Park–Bobrow–Ploen, 1995).** Con $\mathcal{A}_i$ el eje de tornillo de la junta $i$ en el marco $i$ y $T_{i,i-1}$ la transformación entre marcos:
  - *Hacia delante* ($i=1\dots n$): $\mathcal{V}_i=\mathrm{Ad}_{T_{i,i-1}}\mathcal{V}_{i-1}+\mathcal{A}_i\dot\theta_i$; $\ \dot{\mathcal{V}}_i=\mathrm{Ad}_{T_{i,i-1}}\dot{\mathcal{V}}_{i-1}+\mathrm{ad}_{\mathcal{V}_i}\mathcal{A}_i\dot\theta_i+\mathcal{A}_i\ddot\theta_i$.
  - *Hacia atrás* ($i=n\dots1$): $\mathcal{F}_i=\mathrm{Ad}^\top_{T_{i+1,i}}\mathcal{F}_{i+1}+\mathcal{G}_i\dot{\mathcal{V}}_i-\mathrm{ad}^\top_{\mathcal{V}_i}\mathcal{G}_i\mathcal{V}_i$; $\ \tau_i=\mathcal{F}_i^\top\mathcal{A}_i$.
  
  Es $O(n)$, expresado íntegramente con $\mathrm{Ad}$ y $\mathrm{ad}$; además da la forma cerrada $M(q)=\mathcal{J}^\top\mathcal{G}\mathcal{J}$ con parámetros cinemáticos e inerciales separados. Featherstone formula lo mismo con "vectores espaciales" 6D (base de los algoritmos RNEA/CRBA/ABA que usan MuJoCo y Pinocchio).
- **Geometría riemanniana como marco de control.** Las *Riemannian Motion Policies* (RMP) combinan una aceleración deseada con una métrica en cada espacio de tarea y la *retiran* (pullback) al espacio articular: $M_q=\sum_k J_k^\top A_kJ_k$.

### Por qué importa para el brazo
MuJoCo calcula internamente $M(q)$ (`mj_fullM`) y el sesgo $C\dot q+g$ (`qfrc_bias`): son exactamente los objetos de esta sección. Diseñar costes de trayectoria con la métrica $M(q)$ (distancia energética) en lugar de la euclidiana hace que los movimientos sean suaves y físicamente coherentes; la estructura $\dot M-2C$ antisimétrica garantiza estabilidad de controladores pasivos (importantes al manipular frascos frágiles). La métrica $M(q)$ también es el precondicionador natural al afinar trayectorias (enlace con el gradiente natural, Parte 2).

### Referencias clave
- F. C. Park, J. E. Bobrow, S. R. Ploen, "A Lie Group Formulation of Robot Dynamics", *IJRR* 14(6) (1995). [doi:10.1177/027836499501400606](https://doi.org/10.1177/027836499501400606)
- F. Bullo, A. D. Lewis, *Geometric Control of Mechanical Systems*, Springer (2005). [doi:10.1007/978-1-4899-7276-7](https://link.springer.com/book/10.1007/978-1-4899-7276-7)
- J. E. Marsden, T. S. Ratiu, *Introduction to Mechanics and Symmetry*, 2ª ed., Springer (1999). [doi:10.1007/978-0-387-21792-5](https://link.springer.com/book/10.1007/978-0-387-21792-5)
- P. M. Wensing, J.-J. E. Slotine, "Coriolis Factorizations and their Connections to Riemannian Geometry" (2023). [arXiv:2312.14425](https://arxiv.org/abs/2312.14425)
- R. Featherstone, *Rigid Body Dynamics Algorithms*, Springer (2008). [doi:10.1007/978-1-4899-7560-7](https://link.springer.com/book/10.1007/978-1-4899-7560-7)

---

## 5. Probabilidad en grupos de Lie

### Intuición
Una "gaussiana sobre una rotación" no puede definirse sumando ruido a una matriz $R$ (el resultado no sería una rotación). La solución estándar: una media $\bar X$ en el grupo y ruido gaussiano en el álgebra de Lie, inyectado con $\mathrm{Exp}$. Si el ruido es pequeño ("concentrado"), la densidad está bien definida y las reglas de propagación se reducen a álgebra lineal con Jacobianos de Lie y adjuntas. Para incertidumbres grandes aparecen las distribuciones "banana" que Chirikjian estudia con análisis armónico en grupos.

### Definiciones formales
- **Gaussiana concentrada** (perturbación derecha):
$$X=\bar X\,\mathrm{Exp}(\epsilon),\qquad \epsilon\sim\mathcal{N}(0,\Sigma),\ \Sigma\in\mathbb{R}^{6\times6}\ \text{para } SE(3),$$
con densidad aproximada $p(X)\propto\exp\!\big(-\tfrac12\,(X\ominus\bar X)^\top\Sigma^{-1}(X\ominus\bar X)\big)$. Barfoot & Furgale usan la perturbación **izquierda** $T=\mathrm{Exp}(\epsilon)\bar T$; se pasa de una a otra con $\Sigma_{\text{izq}}=\mathrm{Ad}_{\bar T}\Sigma_{\text{der}}\mathrm{Ad}_{\bar T}^\top$.
- **Composición de poses inciertas.** Si $T_1=\bar T_1\mathrm{Exp}(\epsilon_1)$, $T_2=\bar T_2\mathrm{Exp}(\epsilon_2)$ independientes:
$$T_1T_2=\bar T_1\bar T_2\,\mathrm{Exp}\big(\mathrm{Ad}_{\bar T_2^{-1}}\epsilon_1+\epsilon_2+O(\epsilon^2)\big)\ \Rightarrow\ \Sigma\approx\mathrm{Ad}_{\bar T_2^{-1}}\Sigma_1\mathrm{Ad}_{\bar T_2^{-1}}^\top+\Sigma_2 .$$
Barfoot & Furgale (2014) derivan además correcciones hasta cuarto orden (vía BCH) y la fusión de varias medidas de una misma pose.
- **Propagación por funciones.** Para $Y=f(X)$: $\Sigma_Y\approx J\,\Sigma_X J^\top$, con $J$ el Jacobiano de Lie de §2 (p. ej. $J=J_r^{-1}$ para $\mathrm{Log}$, o $\mathrm{Ad}$ para la composición).
- **Media en el grupo (media de Fréchet/Karcher).** $\bar X=\arg\min_X\sum_k\lVert X_k\ominus X\rVert^2$, resuelta iterando $\bar X\leftarrow\bar X\oplus\frac1N\sum_k(X_k\ominus\bar X)$.
- **Visión de Chirikjian.** Densidades $f\in L^2(G)$, convolución en el grupo
$$(f_1*f_2)(g)=\int_G f_1(h)\,f_2(h^{-1}g)\,dh ,$$
(con $dh$ la medida de Haar), que modela composición de errores cinemáticos en cadenas seriales; transformada de Fourier en grupos no conmutativos; difusión (ecuación del calor) en $SE(3)$; Wang & Chirikjian (2008) dan propagación de error de *segundo orden* y no paramétrica.
- **Filtros invariantes.** Cuando la dinámica es "afín en el grupo", el error de estimación $\eta=\bar X^{-1}X$ evoluciona de forma autónoma y el EKF invariante (IEKF) hereda garantías de estabilidad del caso lineal (Barrau & Bonnabel).

### Por qué importa para el brazo
La pose de un tubo estimada por una cámara (Parte 3) llega con una covarianza en $\mathfrak{se}(3)$. Esa incertidumbre se compone con la cinemática del brazo (más su propia incertidumbre de calibración) hasta la pinza: $T_{\text{pinza}\to\text{tubo}}=T_{\text{pinza}\to\text{mundo}}\,T_{\text{mundo}\to\text{cámara}}\,T_{\text{cámara}\to\text{tubo}}$. Con las fórmulas anteriores se obtiene la covarianza del error de agarre y se puede decidir si hace falta una segunda observación antes de insertar el tubo en el portamuestras. Nótese el efecto "banana": una pequeña incertidumbre angular en la base se transforma en una gran incertidumbre posicional en la punta de un brazo extendido (el término $[p]_\times R$ de $\mathrm{Ad}$).

### Referencias clave
- T. D. Barfoot, P. T. Furgale, "Associating Uncertainty With Three-Dimensional Poses for Use in Estimation Problems", *IEEE T-RO* 30(3) (2014). [doi:10.1109/TRO.2014.2298059](https://doi.org/10.1109/TRO.2014.2298059)
- G. S. Chirikjian, *Stochastic Models, Information Theory, and Lie Groups*, Vol. 1 (2009) [doi:10.1007/978-0-8176-4803-9](https://link.springer.com/book/10.1007/978-0-8176-4803-9) y Vol. 2 (2011) [doi:10.1007/978-0-8176-4944-9](https://link.springer.com/book/10.1007/978-0-8176-4944-9), Birkhäuser.
- Y. Wang, G. S. Chirikjian, "Nonparametric Second-order Theory of Error Propagation on Motion Groups", *IJRR* 27(11–12) (2008). [doi:10.1177/0278364908097583](https://doi.org/10.1177/0278364908097583)
- A. Barrau, S. Bonnabel, "The invariant extended Kalman filter as a stable observer", *IEEE TAC* (2017). [arXiv:1410.1465](https://arxiv.org/abs/1410.1465)
- S. Calinon, "Gaussians on Riemannian Manifolds: Applications for Robot Learning and Adaptive Control", *IEEE RAM* (2020). [arXiv:1909.05946](https://arxiv.org/abs/1909.05946)

---

## 6. Geometría de la información (puente hacia la Parte 2)

### Intuición
Una familia paramétrica de distribuciones $\{p(x\mid\theta)\}$ — por ejemplo, una política estocástica que genera trayectorias del brazo, o una red que predice la pose de un tubo — es en sí una variedad. La distancia "correcta" entre dos parámetros no es $\lVert\theta_1-\theta_2\rVert$ sino cuánto difieren *las distribuciones* que generan. Localmente, la divergencia KL induce una métrica: la **información de Fisher**.

### Definiciones formales
- **Variedad estadística.** $\mathcal{S}=\{p_\theta:\theta\in\Theta\subseteq\mathbb{R}^d\}$ con $\theta\mapsto p_\theta$ suave e inyectiva.
- **Métrica de Fisher–Rao.**
$$g_{ij}(\theta)=\mathbb{E}_{p_\theta}\!\left[\partial_i\log p_\theta(x)\,\partial_j\log p_\theta(x)\right]=-\mathbb{E}_{p_\theta}\!\left[\partial_i\partial_j\log p_\theta(x)\right],$$
$$\mathrm{KL}(p_\theta\,\Vert\,p_{\theta+d\theta})=\tfrac12\,d\theta^\top G(\theta)\,d\theta+O(\lVert d\theta\rVert^3).$$
Teorema de Chentsov: es (salvo escala) la única métrica invariante bajo estadísticos suficientes/aplicaciones de Markov.
- **Conexiones duales de Amari.** Tensor cúbico $T_{ijk}=\mathbb{E}[\partial_i\ell\,\partial_j\ell\,\partial_k\ell]$ y la familia de $\alpha$-conexiones
$$\Gamma^{(\alpha)}_{ij,k}=\mathbb{E}\!\left[\left(\partial_i\partial_j\ell+\tfrac{1-\alpha}{2}\partial_i\ell\,\partial_j\ell\right)\partial_k\ell\right],\qquad \ell=\log p_\theta .$$
$\nabla^{(\alpha)}$ y $\nabla^{(-\alpha)}$ son duales respecto a $g$: $X\,g(Y,Z)=g(\nabla^{(\alpha)}_XY,Z)+g(Y,\nabla^{(-\alpha)}_XZ)$; $\alpha=0$ es Levi-Civita. Las familias exponenciales son **dualmente planas** ($e$-plana en parámetros naturales, $m$-plana en parámetros de expectación), lo que da el teorema de Pitágoras generalizado para la KL y las proyecciones de información.
- **Gradiente natural** (una línea; desarrollo completo en la Parte 2): $\tilde\nabla L(\theta)=G(\theta)^{-1}\nabla L(\theta)$ — el gradiente riemanniano de §1 con la métrica de Fisher; es invariante a reparametrizaciones.

### Por qué importa para el brazo
Si el objetivo es afinar movimientos del brazo con políticas estocásticas (p. ej. gaussianas sobre acciones o sobre giros en $\mathfrak{se}(3)$), la métrica de Fisher dicta pasos de aprendizaje que no dependen de cómo se parametrizó la política (ángulos vs. cuaterniones, escalas de junta). Para una gaussiana concentrada en $SE(3)$ con covarianza $\Sigma$ fija, la información de Fisher respecto a la media (en coordenadas locales) es $\Sigma^{-1}$, uniendo §5 y esta sección. Véase [`02_optimizacion_y_algoritmos.md`](02_optimizacion_y_algoritmos.md) para gradiente natural, K-FAC, TRPO/NPG y optimización riemanniana.

### Referencias clave
- S. Amari, "Natural Gradient Works Efficiently in Learning", *Neural Computation* 10(2) (1998). [doi:10.1162/089976698300017746](https://doi.org/10.1162/089976698300017746)
- S. Amari, *Information Geometry and Its Applications*, Springer (2016). [doi:10.1007/978-4-431-55978-8](https://link.springer.com/book/10.1007/978-4-431-55978-8)
- F. Nielsen, "An elementary introduction to information geometry" (2018/2020). [arXiv:1808.08271](https://arxiv.org/abs/1808.08271)

---

## 7. Variedades neuronales, hipótesis de la variedad y equivariancia

### Intuición
Dos ideas geométricas estructuran el aprendizaje profundo moderno: (1) la **hipótesis de la variedad**: los datos de alta dimensión (imágenes de la escena del laboratorio, trayectorias del brazo) se concentran cerca de variedades de baja dimensión; (2) las **simetrías**: si rotar/trasladar la escena rota/traslada la respuesta correcta, la red debería respetar esa estructura (equivariancia), lo que reduce la complejidad muestral. El "blueprint" de Geometric Deep Learning organiza las arquitecturas según el dominio y su grupo de simetría.

### Definiciones formales
- **Acción de grupo.** $G\times X\to X$, $(g,x)\mapsto g\cdot x$, con $e\cdot x=x$ y $(gh)\cdot x=g\cdot(h\cdot x)$. Órbita $G\cdot x$, estabilizador $G_x=\{g: g\cdot x=x\}$.
- **Representación.** Homomorfismo $\rho:G\to GL(V)$; el grupo actúa sobre señales $f:X\to\mathbb{R}^c$ mediante $(g\cdot f)(x)=\rho(g)\,f(g^{-1}\cdot x)$.
- **Espacio homogéneo.** $X$ sobre el que $G$ actúa transitivamente; $X\cong G/H$ con $H=G_{x_0}$. Ejemplos: $S^2\cong SO(3)/SO(2)$ (direcciones de aproximación de la pinza), $\mathbb{R}^3\cong SE(3)/SO(3)$ (posiciones), $SE(3)$ actuando sobre sí mismo (poses).
- **Equivariancia e invariancia.** $\Phi$ es $G$-equivariante si $\Phi(\rho_{\text{in}}(g)x)=\rho_{\text{out}}(g)\Phi(x)$ $\forall g$; invariante si $\rho_{\text{out}}$ es trivial.
- **Convolución de grupo (G-CNN, Cohen & Welling 2016).** Para $f,\psi:G\to\mathbb{R}$:
$$(f\star\psi)(g)=\sum_{h\in G}f(h)\,\psi(g^{-1}h)\qquad\Rightarrow\qquad (L_u f)\star\psi=L_u(f\star\psi),\ \ (L_uf)(h)=f(u^{-1}h).$$
Kondor & Trivedi (2018) prueban que, para grupos compactos, **la estructura convolucional es necesaria y suficiente** para la equivariancia de capas lineales; Cohen, Geiger & Weiler (2019) generalizan a campos sobre espacios homogéneos $G/H$ con núcleos que satisfacen $\kappa(hx)=\rho_{\text{out}}(h)\kappa(x)\rho_{\text{in}}(h)^{-1}$ (núcleos *steerable*).
- **Blueprint de GDL (Bronstein et al. 2021).** Dominio $\Omega$ con grupo $G$; la red se compone de capas lineales $G$-equivariantes $B$, no linealidades puntuales $\sigma$, *pooling* local (coarsening) $P$ y una capa final $G$-invariante $A$: $f=A\circ\sigma_J\circ B_J\circ P_{J-1}\circ\cdots\circ P_1\circ\sigma_1\circ B_1$. Las "5G": grids, groups, graphs, geodesics, gauges.
- **Hipótesis de la variedad.** Formalizada por Fefferman, Mitter & Narayanan: dados datos i.i.d. en un espacio de Hilbert, existe un test con complejidad muestral controlada para decidir si hay una subvariedad de dimensión $d$, volumen $V$ y *reach* $\tau$ que los ajusta. En robótica, las configuraciones factibles/útiles del brazo y las imágenes que generan forman subvariedades de baja dimensión.

### Por qué importa para el brazo
La tarea "agarrar el tubo" es $SE(3)$-equivariante: si el tubo y la gradilla se desplazan sobre la mesa, la pose de agarre se desplaza igual. Una política o un estimador de pose equivariante generaliza a posiciones de *spawn* no vistas sin aumentar datos. Las redes con equivariancia a $SE(3)$ (3D steerable CNNs, LieConv) solo requieren $\mathrm{Exp}$/$\mathrm{Log}$ del grupo — exactamente lo desarrollado en §2. La aplicación en visión (estimación de pose 6D, nubes de puntos) se trata en [`03_aplicaciones_vision_por_computador.md`](03_aplicaciones_vision_por_computador.md).

### Referencias clave
- T. S. Cohen, M. Welling, "Group Equivariant Convolutional Networks", ICML (2016). [arXiv:1602.07576](https://arxiv.org/abs/1602.07576)
- M. M. Bronstein, J. Bruna, T. Cohen, P. Veličković, "Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges" (2021). [arXiv:2104.13478](https://arxiv.org/abs/2104.13478)
- R. Kondor, S. Trivedi, "On the Generalization of Equivariance and Convolution in Neural Networks to the Action of Compact Groups", ICML (2018). [arXiv:1802.03690](https://arxiv.org/abs/1802.03690)
- T. S. Cohen, M. Geiger, M. Weiler, "A General Theory of Equivariant CNNs on Homogeneous Spaces", NeurIPS (2019). [arXiv:1811.02017](https://arxiv.org/abs/1811.02017)
- C. Fefferman, S. Mitter, H. Narayanan, "Testing the Manifold Hypothesis", *J. AMS* 29(4) (2016). [arXiv:1310.0425](https://arxiv.org/abs/1310.0425)

---

## 8. Representación de rotaciones para el aprendizaje

### Intuición
Una red neuronal produce vectores en $\mathbb{R}^k$; una rotación vive en $SO(3)$, una variedad compacta con topología no trivial. La elección de la aplicación $\mathbb{R}^k\to SO(3)$ determina si la función que la red debe aprender es continua. Resultado clave (Zhou et al., CVPR 2019): **no existe ninguna representación continua de $SO(3)$ en $\mathbb{R}^k$ con $k\le4$**, lo que hace discontinuos (como *salida* a regresar) a los ángulos de Euler, al eje-ángulo y a los cuaterniones.

### Definiciones formales y ecuaciones
- **Ángulos de Euler.** $R=R_z(\alpha)R_y(\beta)R_x(\gamma)$. La aplicación $(\alpha,\beta,\gamma)\mapsto R$ pierde rango en $\beta=\pm\pi/2$ (*gimbal lock*). Stuelpnagel (1964): ninguna parametrización con 3 parámetros puede ser global y no singular.
- **Cuaterniones unitarios.** $q=(w,\mathbf{u})\in S^3$, $R(q)=(w^2-\mathbf{u}^\top\mathbf{u})I+2\mathbf{u}\mathbf{u}^\top+2w[\mathbf{u}]_\times$. La aplicación $S^3\to SO(3)$ es un **recubrimiento doble** ($q$ y $-q$ dan la misma rotación): $SO(3)\cong S^3/\{\pm1\}\cong\mathbb{RP}^3$. $S^3\cong SU(2)$ es el grupo de espín (recubrimiento universal). Exponencial: $q=\mathrm{Exp}(\omega)=\big(\cos\tfrac\theta2,\ \hat\omega\sin\tfrac\theta2\big)$.
- **Definición de continuidad (Zhou et al.).** Una representación es un par $(f:SO(3)\to\mathbb{R}^k$ "codificador", $g:\mathbb{R}^k\to SO(3)$ "decodificador") con $g\circ f=\mathrm{id}$; es continua si $f$ lo es. Como $f$ sería un embebimiento topológico de $\mathbb{RP}^3$ en $\mathbb{R}^k$, y $\mathbb{RP}^3$ no se embebe en $\mathbb{R}^4$, se requiere $k\ge5$.
- **Representación 6D (Gram–Schmidt).** Con $a_1,a_2\in\mathbb{R}^3$:
$$b_1=\frac{a_1}{\lVert a_1\rVert},\quad b_2=\frac{a_2-(b_1^\top a_2)b_1}{\lVert a_2-(b_1^\top a_2)b_1\rVert},\quad b_3=b_1\times b_2,\quad R=[b_1\ b_2\ b_3].$$
Codificador continuo: las dos primeras columnas de $R$. (Zhou et al. también dan una representación 5D por proyección estereográfica.)
- **Ortogonalización por SVD (9D).** Para $M\in\mathbb{R}^{3\times3}$ con $M=U\Sigma V^\top$:
$$\mathrm{SVDO}^+(M)=U\,\mathrm{diag}\big(1,1,\det(UV^\top)\big)\,V^\top=\arg\min_{R\in SO(3)}\lVert R-M\rVert_F .$$
Levinson et al. (2020) muestran que es la proyección de máxima verosimilitud bajo ruido gaussiano en $M$ y que, empíricamente, iguala o supera a 6D.
- **Matiz práctico.** Brégier (2021) destaca la conectividad/convexidad de las preimágenes de la aplicación $\mathbb{R}^k\to SO(3)$ y encuentra que la ortonormalización tipo Procrustes (SVD) suele ser la mejor, y que el vector de rotación sirve para ángulos pequeños. Geist et al. (2024) sintetizan: para **salidas** de la red usar 6D o 9D+SVD; para **entradas**, cuaterniones (con signo canónico) o matrices funcionan bien, porque la discontinuidad afecta a la *regresión* del codificador, no a la lectura de una rotación dada. Las pérdidas deberían medirse en el grupo: $d(R_1,R_2)=\lVert\mathrm{Log}(R_1^\top R_2)\rVert$ (distancia geodésica) o la de Frobenius $\lVert R_1-R_2\rVert_F$, que son equivalentes localmente.

### Por qué importa para el brazo
Si una red predice la orientación de agarre de un tubo o del tapón de un vial a partir de una imagen de la cámara de la escena, o si una política aprende acciones de orientación de la pinza, usar Euler/cuaterniones como salida produce saltos de error cerca de ciertas orientaciones (la red intenta aproximar una función discontinua). 6D/SVD eliminan ese problema; los incrementos pequeños pueden además expresarse en el álgebra ($\omega\in\mathbb{R}^3$) y aplicarse con $\oplus$, coherente con el convenio de §0.1. Esto conecta con la estimación de pose 6D de la [Parte 3](03_aplicaciones_vision_por_computador.md).

### Referencias clave
- Y. Zhou, C. Barnes, J. Lu, J. Yang, H. Li, "On the Continuity of Rotation Representations in Neural Networks", CVPR (2019). [arXiv:1812.07035](https://arxiv.org/abs/1812.07035)
- J. Levinson et al., "An Analysis of SVD for Deep Rotation Estimation", NeurIPS (2020). [arXiv:2006.14616](https://arxiv.org/abs/2006.14616)
- R. Brégier, "Deep Regression on Manifolds: A 3D Rotation Case Study", 3DV (2021). [arXiv:2103.16317](https://arxiv.org/abs/2103.16317)
- A. R. Geist, J. Frey, M. Zhobro, A. Levina, G. Martius, "Learning with 3D rotations, a hitchhiker's guide to SO(3)", ICML (2024). [arXiv:2404.11735](https://arxiv.org/abs/2404.11735)
- J. Stuelpnagel, "On the Parametrization of the Three-Dimensional Rotation Group", *SIAM Review* 6(4) (1964). [doi:10.1137/1006093](https://doi.org/10.1137/1006093)

---

## 9. Síntesis: la cadena matemática completa para el brazo del reto MAFER

1. **Estado:** $q\in\mathcal{C}$ (caja de límites articulares), $(q,\dot q)\in T\mathcal{C}$.
2. **Cinemática:** $T=f(q)=e^{[\mathcal{S}_1]q_1}\cdots e^{[\mathcal{S}_n]q_n}M\in SE(3)$; $\mathcal{V}_b=J_b(q)\dot q$.
3. **Error de tarea:** $e=T^\star\ominus T=\mathrm{Log}(T^{-1}T^\star)\in\mathbb{R}^6$; paso de IK: $\Delta q=J_b^\dagger e$ (amortiguado cerca de singularidades; vigilar $\sigma_{\min}(J_b)$).
4. **Dinámica/métrica:** $M(q)\ddot q+C\dot q+g=\tau$; $M(q)$ define la geometría energética de $\mathcal{C}$.
5. **Incertidumbre:** $T^\star=\bar T^\star\mathrm{Exp}(\epsilon)$, $\epsilon\sim\mathcal{N}(0,\Sigma)$ desde visión; propagar con $\mathrm{Ad}$ y $J_r$.
6. **Aprendizaje:** parámetros $\theta$ de una política $\pi_\theta$ (variedad estadística, métrica de Fisher) con salidas rotacionales 6D/SVD y arquitectura $SE(3)$-equivariante → optimización en la [Parte 2](02_optimizacion_y_algoritmos.md), percepción en la [Parte 3](03_aplicaciones_vision_por_computador.md).

---

## 10. Glosario español / inglés

| Español | English | Nota breve |
|---|---|---|
| Variedad diferenciable | Smooth manifold | Espacio localmente euclídeo con estructura suave |
| Carta / atlas | Chart / atlas | Coordenadas locales / colección compatible de cartas |
| Espacio tangente | Tangent space $T_pM$ | Velocidades en $p$ |
| Espacio cotangente | Cotangent space $T^*_pM$ | Gradientes, fuerzas |
| Fibrado tangente | Tangent bundle $TM$ | Espacio de estados $(q,\dot q)$ |
| Diferencial / empuje | Differential / pushforward $dF_p$ | Jacobiano intrínseco |
| Retirada | Pullback $F^*$ | Transporta covectores/métricas hacia atrás |
| Métrica riemanniana | Riemannian metric | Producto interno suave en cada $T_pM$ |
| Geodésica | Geodesic | Curva localmente de longitud mínima |
| Símbolos de Christoffel | Christoffel symbols | Coeficientes de la conexión |
| Grupo de Lie | Lie group | Grupo + variedad suave |
| Álgebra de Lie | Lie algebra $\mathfrak{g}$ | Tangente en la identidad con corchete |
| Aplicación exponencial / logaritmo | Exponential / logarithm map | $\mathfrak{g}\leftrightarrows G$ |
| Operadores sombrero / uve | Hat / vee operators | $\mathbb{R}^k\leftrightarrows\mathfrak{g}$ |
| Adjunta | Adjoint $\mathrm{Ad}_g$, $\mathrm{ad}_\xi$ | Cambio de marco de velocidades |
| Jacobiano izquierdo / derecho | Left / right Jacobian | Derivada de $\mathrm{Exp}$ |
| Perturbación izquierda / derecha | Left / right perturbation | Global / local |
| Giro (tornillo de velocidad) | Twist | $\mathcal{V}=(\omega,v)$ |
| Llave (tornillo de fuerza) | Wrench | $\mathcal{F}=(m,f)$ |
| Eje de tornillo | Screw axis | $\mathcal{S}$ |
| Producto de exponenciales | Product of exponentials (PoE) | Cinemática directa |
| Cinemática directa / inversa | Forward / inverse kinematics | $q\mapsto T$ / $T\mapsto q$ |
| Espacio de configuración | Configuration space | $\mathcal{C}$ |
| Jacobiano espacial / del cuerpo | Space / body Jacobian | $J_s$, $J_b$ |
| Singularidad | Singularity | Pérdida de rango de $J$ |
| Elipsoide de manipulabilidad | Manipulability ellipsoid | Yoshikawa |
| Destreza | Dexterity | Isotropía del elipsoide |
| Matriz de masa (inercia) | Mass (inertia) matrix $M(q)$ | Métrica cinética |
| Términos de Coriolis | Coriolis terms | $C(q,\dot q)\dot q$ |
| Newton–Euler recursivo | Recursive Newton–Euler (RNEA) | Dinámica inversa $O(n)$ |
| Gaussiana concentrada | Concentrated Gaussian | Ruido en el álgebra |
| Propagación de incertidumbre | Uncertainty propagation | $J\Sigma J^\top$ |
| Medida de Haar | Haar measure | Medida invariante en $G$ |
| Variedad estadística | Statistical manifold | Familia $p_\theta$ |
| Información de Fisher | Fisher information | Métrica de Fisher–Rao |
| Conexiones duales | Dual connections | $\nabla^{(\alpha)},\nabla^{(-\alpha)}$ |
| Gradiente natural | Natural gradient | $G^{-1}\nabla L$ |
| Acción de grupo | Group action | $G\times X\to X$ |
| Espacio homogéneo | Homogeneous space | $G/H$ |
| Equivariancia | Equivariance | $\Phi\circ\rho_{\text{in}}=\rho_{\text{out}}\circ\Phi$ |
| Hipótesis de la variedad | Manifold hypothesis | Datos cerca de subvariedades |
| Recubrimiento doble | Double cover | $S^3\to SO(3)$ |
| Bloqueo de cardán | Gimbal lock | Singularidad de Euler |

---

## 11. Bibliografía anotada (todas las entradas verificadas mediante búsqueda)

| # | Título | Autores | Año | Enlace | Por qué es relevante |
|---|---|---|---|---|---|
| 1 | A micro Lie theory for state estimation in robotics | J. Solà, J. Deray, D. Atchuthan | 2018 | [arXiv:1812.01537](https://arxiv.org/abs/1812.01537) | Referencia práctica de $\oplus/\ominus$, Jacobianos y adjuntas para SO(3), SE(3), etc. Base de la librería `manif`. |
| 2 | Associating Uncertainty With Three-Dimensional Poses for Use in Estimation Problems | T. D. Barfoot, P. T. Furgale | 2014 | [doi:10.1109/TRO.2014.2298059](https://doi.org/10.1109/TRO.2014.2298059) | Composición, fusión y propagación de incertidumbre en SE(3) (hasta 4º orden). |
| 3 | State Estimation for Robotics | T. D. Barfoot | 2017 | [PDF del autor](https://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser17.pdf) | Libro de referencia: grupos de Lie matriciales, Jacobianos cerrados de SE(3), estimación. |
| 4 | Stochastic Models, Information Theory, and Lie Groups, Vol. 1 | G. S. Chirikjian | 2009 | [doi:10.1007/978-0-8176-4803-9](https://link.springer.com/book/10.1007/978-0-8176-4803-9) | Fundamentos: procesos estocásticos, geometría diferencial, información. |
| 5 | Stochastic Models, Information Theory, and Lie Groups, Vol. 2 | G. S. Chirikjian | 2011 | [doi:10.1007/978-0-8176-4944-9](https://link.springer.com/book/10.1007/978-0-8176-4944-9) | Análisis armónico y probabilidad en grupos de Lie, aplicaciones a robótica. |
| 6 | Nonparametric Second-order Theory of Error Propagation on Motion Groups | Y. Wang, G. S. Chirikjian | 2008 | [doi:10.1177/0278364908097583](https://doi.org/10.1177/0278364908097583) | Propagación de error de segundo orden en cadenas seriales (SE(3)). |
| 7 | Robotic manipulators and the product of exponentials formula | R. W. Brockett | 1984 | [doi:10.1007/BFb0031048](https://link.springer.com/chapter/10.1007/BFb0031048) | Origen de la fórmula PoE para cinemática directa. |
| 8 | Modern Robotics: Mechanics, Planning, and Control | K. M. Lynch, F. C. Park | 2017 | [PDF preprint](http://hades.mech.northwestern.edu/images/2/2e/MR-largefont-v2.pdf) | Texto moderno con giros, PoE, Jacobianos y dinámica en SE(3); convención de este documento. |
| 9 | A Mathematical Introduction to Robotic Manipulation | R. M. Murray, Z. Li, S. S. Sastry | 1994 | [Caltech](https://www.cds.caltech.edu/~murray/books/MLS/) | Tratamiento riguroso clásico de teoría de tornillos y dinámica lagrangiana. |
| 10 | Manipulability of Robotic Mechanisms | T. Yoshikawa | 1985 | [doi:10.1177/027836498500400201](https://journals.sagepub.com/doi/10.1177/027836498500400201) | Índice y elipsoide de manipulabilidad. |
| 11 | A Lie Group Formulation of Robot Dynamics | F. C. Park, J. E. Bobrow, S. R. Ploen | 1995 | [doi:10.1177/027836499501400606](https://doi.org/10.1177/027836499501400606) | Newton–Euler recursivo y forma cerrada con operaciones de álgebra de Lie. |
| 12 | Rigid Body Dynamics Algorithms | R. Featherstone | 2008 | [doi:10.1007/978-1-4899-7560-7](https://link.springer.com/book/10.1007/978-1-4899-7560-7) | Álgebra espacial 6D; base de RNEA/CRBA/ABA de simuladores como MuJoCo. |
| 13 | Geometric Control of Mechanical Systems | F. Bullo, A. D. Lewis | 2005 | [doi:10.1007/978-1-4899-7276-7](https://link.springer.com/book/10.1007/978-1-4899-7276-7) | Sistemas mecánicos como métricas riemannianas + conexiones afines. |
| 14 | Introduction to Mechanics and Symmetry | J. E. Marsden, T. S. Ratiu | 1999 | [doi:10.1007/978-0-387-21792-5](https://link.springer.com/book/10.1007/978-0-387-21792-5) | Euler–Poincaré, reducción por simetría, mecánica en grupos de Lie. |
| 15 | Coriolis Factorizations and their Connections to Riemannian Geometry | P. M. Wensing, J.-J. E. Slotine | 2023 | [arXiv:2312.14425](https://arxiv.org/abs/2312.14425) | Relación entre elección de $C(q,\dot q)$, conexiones afines y pasividad. |
| 16 | Riemannian Motion Policies | N. D. Ratliff, J. Issac, D. Kappler, S. Birchfield, D. Fox | 2018 | [arXiv:1801.02854](https://arxiv.org/abs/1801.02854) | Políticas de movimiento como (aceleración, métrica); pullback al espacio articular. |
| 17 | Riemannian geometry as a unifying theory for robot motion learning and control | N. Jaquier, T. Asfour | 2022 | [arXiv:2209.15539](https://arxiv.org/abs/2209.15539) | Visión de conjunto de la geometría riemanniana en aprendizaje y control de robots. |
| 18 | Gaussians on Riemannian Manifolds: Applications for Robot Learning and Adaptive Control | S. Calinon | 2020 | [arXiv:1909.05946](https://arxiv.org/abs/1909.05946) | Gaussianas, geodésicas y transporte paralelo en variedades para aprendizaje robótico. |
| 19 | Introduction to Smooth Manifolds (2ª ed.) | J. M. Lee | 2012 | [doi:10.1007/978-1-4419-9982-5](https://link.springer.com/book/10.1007/978-1-4419-9982-5) | Referencia estándar de variedades, tangentes, grupos y álgebras de Lie. |
| 20 | Optimization Algorithms on Matrix Manifolds | P.-A. Absil, R. Mahony, R. Sepulchre | 2008 | [Princeton UP](https://press.princeton.edu/books/hardcover/9780691132983/optimization-algorithms-on-matrix-manifolds) | Retracciones, gradiente riemanniano en variedades matriciales (enlace con Parte 2). |
| 21 | An Introduction to Optimization on Smooth Manifolds | N. Boumal | 2023 | [doi:10.1017/9781009166164](https://doi.org/10.1017/9781009166164) | Introducción moderna a geometría y optimización en variedades. |
| 22 | Integrating generic sensor fusion algorithms with sound state representations through encapsulation of manifolds | C. Hertzberg, R. Wagner, U. Frese, L. Schröder | 2013 | [arXiv:1107.1119](https://arxiv.org/abs/1107.1119) | Operadores $\boxplus/\boxminus$ que encapsulan la variedad para algoritmos genéricos. |
| 23 | Quaternion kinematics for the error-state Kalman filter | J. Solà | 2017 | [arXiv:1711.02508](https://arxiv.org/abs/1711.02508) | Cuaterniones, perturbaciones de rotación, derivadas e integración. |
| 24 | On-Manifold Preintegration for Real-Time Visual-Inertial Odometry | C. Forster, L. Carlone, F. Dellaert, D. Scaramuzza | 2016 | [arXiv:1512.02363](https://arxiv.org/abs/1512.02363) | Ejemplo canónico de cálculo con $J_r$ en SO(3) y ruido en el álgebra. |
| 25 | The invariant extended Kalman filter as a stable observer | A. Barrau, S. Bonnabel | 2017 | [arXiv:1410.1465](https://arxiv.org/abs/1410.1465) | Error invariante en grupos de Lie y garantías de estabilidad. |
| 26 | Natural Gradient Works Efficiently in Learning | S. Amari | 1998 | [doi:10.1162/089976698300017746](https://doi.org/10.1162/089976698300017746) | Gradiente natural con la métrica de Fisher (puente a Parte 2). |
| 27 | Information Geometry and Its Applications | S. Amari | 2016 | [doi:10.1007/978-4-431-55978-8](https://link.springer.com/book/10.1007/978-4-431-55978-8) | Monografía del fundador: conexiones duales, variedades dualmente planas. |
| 28 | An elementary introduction to information geometry | F. Nielsen | 2018 | [arXiv:1808.08271](https://arxiv.org/abs/1808.08271) | Introducción autocontenida a la geometría de la información. |
| 29 | Group Equivariant Convolutional Networks | T. S. Cohen, M. Welling | 2016 | [arXiv:1602.07576](https://arxiv.org/abs/1602.07576) | G-CNN: convolución de grupo y equivariancia. |
| 30 | Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges | M. M. Bronstein, J. Bruna, T. Cohen, P. Veličković | 2021 | [arXiv:2104.13478](https://arxiv.org/abs/2104.13478) | Blueprint unificado del aprendizaje profundo geométrico. |
| 31 | On the Generalization of Equivariance and Convolution in Neural Networks to the Action of Compact Groups | R. Kondor, S. Trivedi | 2018 | [arXiv:1802.03690](https://arxiv.org/abs/1802.03690) | Convolución ⇔ equivariancia para grupos compactos. |
| 32 | A General Theory of Equivariant CNNs on Homogeneous Spaces | T. S. Cohen, M. Geiger, M. Weiler | 2019 | [arXiv:1811.02017](https://arxiv.org/abs/1811.02017) | Teoría de campos y núcleos steerable sobre $G/H$. |
| 33 | 3D Steerable CNNs: Learning Rotationally Equivariant Features in Volumetric Data | M. Weiler, M. Geiger, M. Welling, W. Boomsma, T. Cohen | 2018 | [arXiv:1807.02547](https://arxiv.org/abs/1807.02547) | Convoluciones equivariantes a SE(3) en datos volumétricos. |
| 34 | Generalizing Convolutional Neural Networks for Equivariance to Lie Groups on Arbitrary Continuous Data | M. Finzi, S. Stanton, P. Izmailov, A. G. Wilson | 2020 | [arXiv:2002.12880](https://arxiv.org/abs/2002.12880) | LieConv: equivariancia a cualquier grupo de Lie usando solo exp/log. |
| 35 | Testing the Manifold Hypothesis | C. Fefferman, S. Mitter, H. Narayanan | 2016 | [arXiv:1310.0425](https://arxiv.org/abs/1310.0425) | Formalización matemática de la hipótesis de la variedad. |
| 36 | On the Continuity of Rotation Representations in Neural Networks | Y. Zhou, C. Barnes, J. Lu, J. Yang, H. Li | 2019 | [arXiv:1812.07035](https://arxiv.org/abs/1812.07035) | No hay representación continua de SO(3) en $\mathbb{R}^{\le4}$; propone 5D/6D. |
| 37 | An Analysis of SVD for Deep Rotation Estimation | J. Levinson, C. Esteves, K. Chen, N. Snavely, A. Kanazawa, A. Rostamizadeh, A. Makadia | 2020 | [arXiv:2006.14616](https://arxiv.org/abs/2006.14616) | Ortogonalización SVD (9D) como salida óptima para rotaciones. |
| 38 | Deep Regression on Manifolds: A 3D Rotation Case Study | R. Brégier | 2021 | [arXiv:2103.16317](https://arxiv.org/abs/2103.16317) | Propiedades deseables de las aplicaciones $\mathbb{R}^k\to SO(3)$; librería RoMa. |
| 39 | Learning with 3D rotations, a hitchhiker's guide to SO(3) | A. R. Geist, J. Frey, M. Zhobro, A. Levina, G. Martius | 2024 | [arXiv:2404.11735](https://arxiv.org/abs/2404.11735) | Guía práctica: qué representación usar en entradas vs. salidas. |
| 40 | On the Parametrization of the Three-Dimensional Rotation Group | J. Stuelpnagel | 1964 | [doi:10.1137/1006093](https://doi.org/10.1137/1006093) | Ninguna parametrización 3D de SO(3) es global y no singular. |

---

*Documentos relacionados:* [`02_optimizacion_y_algoritmos.md`](02_optimizacion_y_algoritmos.md) (gradiente natural, optimización riemanniana, algoritmos de ajuste fino) · [`03_aplicaciones_vision_por_computador.md`](03_aplicaciones_vision_por_computador.md) (estimación de pose, redes equivariantes y visión para la escena del laboratorio).
