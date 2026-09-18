# agrochemical-bottles

Kit de botes blancos tipo "bala" para agroquímicos (HDPE blanco satinado, tapón PP estriado con anillo precinto). Sin etiquetas ni texto. Escala real (1 unidad = 1 m).

| Objeto | Ø cuerpo | Alto sin tapón | Boca | Tapón (Ø × alto) |
|---|---|---|---|---|
| Bote_100mL | 46 mm | 97 mm | 28 mm | 34 × 19 mm |
| Bote_250mL | 60 mm | 131 mm | 38 mm | 44 × 22 mm |
| Bote_500mL | 74 mm | 164 mm | 45 mm | 51 × 25 mm |
| Bote_1L | 88 mm | 216 mm | 50 mm | 56 × 27 mm |
| Bote_1L_ancho | 102 mm | 182 mm | 63 mm | 69 × 32 mm |
| Bote_2L | 116 mm | 245 mm | 63 mm | 69 × 32 mm |

## Archivos

- `agro_bottles_kit.blend` — escena completa (colecciones Botes / Tapones / Escena), Blender 5.0+.
- `agro_bottles_kit.glb` — todos los botes y tapones, colocados como en la escena.
- `glb/` — un GLB por pieza, con origen en el centro de la base (`bottle_*`, `cap_*`).
- `preview.png` — render de referencia.
- `generate_agro_bottles.py` — generador (`pip install bpy`, `python generate_agro_bottles.py`). Editar la tabla `SET` para cambiar tamaños o nº de estrías.

Bote y tapón son objetos separados; para cerrar un bote, colocar el tapón en z = alto sin tapón − alto del tapón + 1 mm aprox.

## Barcode labels

`labelled/` (not in git) holds one GLB per powder sample, with its EAN-13 label attached as a separate sticker mesh on the bottle's straight wall. Generate it from `computer-vision/`:

```bash
python -m labvision.bottles
```

Each barcode goes on the bottle of its own size (100 mL, 250 mL, 500 mL, 1 L, 2 L); `Bote_1L_ancho` is not used. Details in `computer-vision/README.md`.
