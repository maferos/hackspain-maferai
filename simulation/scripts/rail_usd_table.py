"""Author a single table component from the rail scene's layered MuJoCo visuals."""
from pxr import Gf, Kind, Sdf, Usd, UsdGeom, UsdShade


def prepare_table(stage):
    """Keep one beveled worktop, group its legs, and bind white satin material.

    The source collision slab and decorative finish overlap by design in MJCF.
    These baked USD scenes have no physics; deactivate the redundant visual slab
    rather than rendering two nearly coincident surfaces. Source MJCF is untouched.
    """
    if stage.GetPrimAtPath('/World/Table').IsValid():
        return
    meshes = [p for p in stage.Traverse() if p.IsA(UsdGeom.Mesh)]
    finish = [p for p in meshes if 'room_worktop_finish_0_id' in p.GetName()]
    slab = [p for p in meshes if 'minihannover_worktop_id' in p.GetName()]
    legs = [p for p in meshes if 'minihannover_leg_' in p.GetName()]
    if len(finish) != 1 or len(slab) != 1 or len(legs) != 6:
        raise ValueError('Expected one worktop finish, one source slab and six table legs')
    table = UsdGeom.Xform.Define(stage, '/World/Table')
    Usd.ModelAPI(table).SetKind(Kind.Tokens.component)
    table.GetPrim().SetDisplayName('Table')
    layer = stage.GetRootLayer()
    for name, mesh in [('Worktop', finish[0]), *[(f'Leg{i+1}', p) for i, p in enumerate(legs)]]:
        source = mesh.GetParent()
        if source.GetParent().GetPath() != Sdf.Path('/World'):
            raise ValueError('Expected exported table parts directly below World')
        if not Sdf.CopySpec(layer, source.GetPath(), layer, f'/World/Table/{name}'):
            raise RuntimeError(f'Could not group table part {name}')
        source.SetActive(False)
    slab[0].GetParent().SetActive(False)
    material = UsdShade.Material.Define(stage, '/World/Table/WhiteSatin')
    shader = UsdShade.Shader.Define(stage, '/World/Table/WhiteSatin/Surface')
    shader.CreateIdAttr('UsdPreviewSurface')
    shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.95, 0.95, 0.94))
    shader.CreateInput('metallic', Sdf.ValueTypeNames.Float).Set(0.0)
    shader.CreateInput('roughness', Sdf.ValueTypeNames.Float).Set(0.45)
    shader.CreateInput('ior', Sdf.ValueTypeNames.Float).Set(1.5)
    material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), 'surface')
    for prim in Usd.PrimRange(stage.GetPrimAtPath('/World/Table/Worktop')):
        if prim.IsA(UsdGeom.Mesh):
            UsdShade.MaterialBindingAPI.Apply(prim).Bind(material)
