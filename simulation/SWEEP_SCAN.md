# Escaneo inicial por barrido (rama `vision/sweep-scan`)

Estado: **programado, no ejecutado en vivo.** Hay que probarlo en una máquina
con GPU antes de fusionarlo en `main`. El detalle técnico y las tablas están en
[`vision-pick.md`](vision-pick.md), sección "The initial scan".

## Qué sustituye y por qué

El escaneo de `main` (8a4c01e) era un sobrevuelo ciego: tres pasadas fijas a lo
largo de todo el raíl, sin usar dónde estaban los botes. Arrancaba desde el
centro y se iba a un extremo sin motivo aparente, volaba alto para no tumbar
nada y por eso no leía los botes pequeños: 16 de 19 nombrados.

## Qué hace ahora

1. **Aparca.** El brazo va al extremo más cercano del raíl para no tapar la
   cámara fija, que mira el centro de la mesa desde el pasillo.
2. **YOLO hace la lista.** Lo que la cámara fija detecta con la mesa despejada
   es la lista de botes que hay que identificar, entera.
3. **Carriles** (`sweep_lanes`). Los botes se agrupan según lo lejos que están
   del raíl (0.55 m de ancho como máximo por carril). En la mesa de demo salen
   cuatro: franja trasera, el bote bajo el raíl, fila principal y borde del
   pasillo.
4. **Pasa sin parar** (`plan_sweep`, `fly`). Cada carril es un solo movimiento
   continuo: la cámara de muñeca mira de lado, a 0.45 m y 40° de cada bote, y va
   en línea recta de la vista de un bote a la del siguiente. El raíl hace el
   viaje; el brazo solo absorbe la diferencia de profundidad. Se empieza por el
   extremo más cercano, así que los carriles van en ida y vuelta.
5. **Lee todo el rato.** Se pide una lectura de anillos en cuanto llega la
   anterior y se guardan todos los anillos del encuadre. Si la máquina es lenta
   el carro frena suave (nada de tirones). Durante el barrido la muñeca tiene
   prioridad y YOLO corre cada 4 s.
6. **Botes pequeños.** Lo que quede sin nombre se vuelve a pasar más cerca y
   con más ángulo (0.40 m, 50°), solo esos. Lo que aún quede se mira uno a uno
   con el `look` antiguo. Ningún bote de la lista se queda sin trabajar.

## Cómo evita tumbar botes (`over_vessels`)

- Ninguna parte del brazo baja de 2 cm por encima del matraz más alto posible
  (13.5 cm sobre la mesa), haya o no algo detectado debajo.
- Sobre cada bote conocido que quede bajo alguna pieza del brazo: 5 cm de aire,
  contando 8 cm de holgura por el error de posición de YOLO.
- Se comprueba cada pose y cada tramo entre poses. Si no cabe, la pose se eleva
  manteniendo la mira (hasta 25 cm); si ni así, se omite ese punto; si no hay
  camino, el pase se corta y pasa por la pose de transporte.

## Medido (antes de programar el controlador)

- Brazo posado a mano en cada bote, tres posiciones a lo largo del raíl:
  **0.45 m / 40° lee 19 de 19**; más cerca y más empinado lee menos (14 a 16).
- Los anillos se leen mejor hacia los lados del encuadre que en el centro (a
  0.36 m: 0 en el centro, 12 a 0.35 m de lado). Por eso pasar de largo lee más
  que pararse delante. Ojo: es efecto de la lente pinhole del simulador; en
  hardware hay que volver a medirlo.
- Plan completo posado offline, un fotograma cada 10 cm, posiciones verdaderas:
  **19 de 19, ninguno mal, error máximo 3.1 mm**, brazo a 14 cm sobre la mesa.
- Límites del brazo: la cámara no cabe más cerca del raíl que y = -0.15 mirando
  hacia fuera, ni más lejos que y = -0.65 mirando hacia el raíl. El carro nunca
  justo encima de la cámara: ahí la IK no converge.

## No ejecutado nunca

- El barrido en vivo: el regulador de velocidad de `fly`, la prioridad de la
  muñeca en `Perception`, el visor (`view/backend/live_scan.py`).
- La lista real de YOLO en vez de las posiciones verdaderas (se desvía hasta
  6 cm y no ve el borde del pasillo).
- La segunda pasada más cercana.
- Tres cambios posteriores a la última medición: planificar cada carril desde
  los dos extremos, un arreglo en el bucle que eleva la pose cuando choca, y la
  regla de que un anillo leído con un solo marcador espera a un segundo
  fotograma antes de dar nombre (se vio una lectura falsa, `SMP-0110`, en ~130
  fotogramas). **Si una ejecución nombra pocos botes, mirar primero esta regla**:
  casi todas las lecturas al pasar son de un solo marcador.
- Ni siquiera una comprobación de sintaxis tras las últimas ediciones.

## Cómo probarlo

```bash
cd simulation
python scripts/vision_pick.py --headless --manual --light --no-browser \
    --max-time 600 --bench-map out/sweep.json
```

En el log, por orden: `parking at the end of the rail`, `the fixed camera found
N bottles`, una línea `passing K bottles at y ...` por carril (con `in R runs`
si hubo que cortarlo) y `K of K named in N reads`. `going to look at it` debería
salir pocas veces. El informe final puntúa nombres y posiciones contra el
simulador. Progreso en vivo en http://localhost:8009.
