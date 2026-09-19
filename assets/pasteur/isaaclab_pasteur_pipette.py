"""Isaac Lab (v2.x) config for the Pasteur pipette.

Two ways in:
  A) convert the MJCF/URDF to USD once (MjcfConverter / UrdfConverter), then use UsdFileCfg
  B) drop pasteur_pipette.usd (once you export it from Blender >= 4.1 or Isaac Sim) straight into UsdFileCfg

Usage in an InteractiveSceneCfg:
    pipette: RigidObjectCfg = PASTEUR_PIPETTE_CFG.replace(prim_path="{ENV_REGEX_NS}/Pipette")
"""
import os
import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg
from isaaclab.sim.converters import UrdfConverter, UrdfConverterCfg

ASSET_DIR = os.path.dirname(os.path.abspath(__file__))
USD_PATH = os.path.join(ASSET_DIR, "usd", "pasteur_pipette.usd")


def build_usd(force: bool = False) -> str:
    """Convert the URDF (visual + 3 convex collision meshes) to USD. Idempotent."""
    if os.path.exists(USD_PATH) and not force:
        return USD_PATH
    cfg = UrdfConverterCfg(
        asset_path=os.path.join(ASSET_DIR, "pasteur_pipette.urdf"),
        usd_dir=os.path.dirname(USD_PATH),
        usd_file_name=os.path.basename(USD_PATH),
        fix_base=False,
        merge_fixed_joints=True,
        make_instanceable=True,
        collider_type="convex_hull",   # each collision mesh -> its own convex hull
        force_usd_conversion=force,
    )
    return UrdfConverter(cfg).usd_path


PASTEUR_PIPETTE_CFG = RigidObjectCfg(
    prim_path="/World/Pipette",
    spawn=sim_utils.UsdFileCfg(
        usd_path=USD_PATH,  # call build_usd() before creating the scene
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            max_depenetration_velocity=1.0,
            linear_damping=0.05,
            angular_damping=0.05,
        ),
        mass_props=sim_utils.MassPropertiesCfg(mass=0.0012),
        collision_props=sim_utils.CollisionPropertiesCfg(
            collision_enabled=True,
            contact_offset=0.001,   # thin object: tighten default offsets (m)
            rest_offset=0.0,
        ),
    ),
    # lying on the table, tip along +X, 1 cm above the surface
    init_state=RigidObjectCfg.InitialStateCfg(pos=(0.0, 0.0, 0.01), rot=(0.7071068, 0.0, 0.7071068, 0.0)),
)
