# Micropipeta de precisión (5–50 µL, monocanal) — asset paramétrico

Modelo generado proceduralmente (sin licencias de terceros), mismas convenciones que
`assets/reagent-bottles/`: **metros, origen en la punta (base-centro), +Z arriba** (el GLB va +Y arriba).
Longitud total 263 mm, masa 115 g. Colores de la referencia: cuerpo blanco, botón/collar/vástago azul, cono negro.

```
micropipette.blend      ← se genera con Blender (ver abajo); no puede crearse sin Blender
micropipette.glb        modelo completo (jerarquía body / plunger / ejector)
micropipette.xml        MuJoCo MJCF  (freejoint + 2 slide joints + actuadores de posición)
test_scene.xml          escena MuJoCo con suelo → python -m mujoco.viewer --mjcf test_scene.xml
micropipette.urdf       para Isaac Lab UrdfConverter / ROS
micropipette.usd        USD con UsdPhysics (rigid bodies, colliders, joints prismáticos con drive)
meshes/                 <parte>.stl/.obj (MJCF/URDF) y link_<link>.obj (uno por eslabón)
micropipette_meta.json  medidas, masas, rangos de joint, altura del site de agarre
pipette_geometry.py     geometría paramétrica (edita el dict D para cambiar medidas)
export_micropipette.py  regenera todo:  pip install trimesh mujoco usd-core && python export_micropipette.py .
build_blend.py          crea el .blend:  blender -b -P build_blend.py -- micropipette.blend
```

## Eslabones y articulaciones
| Link | Piezas | Joint | Rango (m) | Muelle |
|---|---|---|---|---|
| `body` | cono, vástago, collar, cuerpo, gancho, display, guía del eyector | freejoint | – | – |
| `plunger` | eje + botón azul superior | slide Z `pipette_plunger_slide` | −0.014 … 0 | k=350 N/m, retorna solo |
| `ejector` | botón lateral, varilla, manguito inferior | slide Z `pipette_ejector_slide` | −0.008 … 0 | k=500 N/m |

Sites MuJoCo: `pipette_grip` (centro del cuerpo, z≈0.168, punto de agarre para pinza) y `pipette_tip` (z=0).
Colisiones: primitivas (caja cuerpo, cápsula vástago, cilindros botones) en `group=3`; visual en `group=2`.

## MuJoCo
```xml
<include file="micropipette.xml"/>   <!-- meshdir="meshes" relativo al XML -->
```
```python
d.ctrl[m.actuator('pipette_plunger_act').id] = -0.014   # pulsar émbolo a fondo
```
Para ponerla en otra posición edita `pos=` del body `micropipette` o `qpos[0:7]`.

## Isaac Lab
Opción A — USD directo:
```python
from isaaclab.assets import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg
import isaaclab.sim as sim_utils
PIPETTE_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(usd_path="<ruta>/micropipette.usd",
        rigid_props=sim_utils.RigidBodyPropertiesCfg(max_depenetration_velocity=1.0),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(fix_root_link=False)),
    init_state=ArticulationCfg.InitialStateCfg(pos=(0.0, 0.0, 0.05)),
    actuators={"buttons": ImplicitActuatorCfg(joint_names_expr=[".*_slide"], stiffness=350.0, damping=0.4)},
)
```
Opción B — importar con `UrdfConverter` (`micropipette.urdf`) o `MjcfConverter` (`micropipette.xml`); ambos
generan el USD con las mismas mallas OBJ. Si solo la quieres como objeto rígido (sin botones), usa
`RigidObjectCfg` con `micropipette.glb` convertido por `MeshConverter`.

Nota: el USD se escribió con `usd-core` (UsdPhysics estándar). Al abrirlo en Isaac Sim, los colliders de
`purpose=guide` no se renderizan; si quieres convex-hull de las mallas en vez de primitivas, aplica
`CollisionAPI` a las mallas de `visuals/` desde Isaac Sim.

## Blender
`build_blend.py` construye la misma geometría en Blender (4.x/5.x): un objeto por pieza, parentados a
`Link_body / Link_plunger / Link_ejector` (empties con lock + límite en Z que reproducen los joints, así
puedes animar el pulsado con keyframes), materiales Principled, cámara y luz. Guarda `.blend` y `.glb`.

## Cambiar medidas o colores
Edita `D` / `MATERIALS` en `pipette_geometry.py` y ejecuta `export_micropipette.py`; para otro volumen
(p. ej. 100–1000 µL) sube `shaft_r0/r1`, `tip_r*` y `body_w*` ~20 %.
