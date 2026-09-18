#!/usr/bin/env python3
"""Turn the barcoded sample bottles into MuJoCo models, label texture included.

The labelled bottles live as GLB in ``assets/<kit>/labelled/``, one per sample, and
MuJoCo cannot read glTF. ``convert_glb.py`` converts a GLB but drops its textures,
which here is the whole point: the label is a textured sticker. This tool keeps it.

Converting the 200 GLBs one by one would write the same bottle 20 times over, since
every sample of a size shares its bottle, its cap and even the shape of its sticker;
only the picture on the sticker differs. So the output is split the same way:

    assets/labelled_bottles/
        meshes/<vessel_class>_<part>.obj    one set per bottle size, shared
        textures/<sample id>.png            the label of one sample
        <sample id>.xml                     an MJCF body: shared meshes + its texture

Each ``<sample id>.xml`` holds one body, origin at the bottom centre, +Z up, label
facing -Y, closed with its cap. Attach it like any other asset:

    <model name="pwd_0004" file="../assets/labelled_bottles/PWD-0004.xml"/>
    <frame pos="..."><attach model="pwd_0004" body="PWD-0004" prefix="p4_"/></frame>

Bottle and cap collide (convex hull) and carry the mass, with ``inertia="exact"``
because they are thin shells. The sticker is visual only: no collision, no mass, and
its own geom, so a segmentation render tells label from bottle for free.

Which sample is which comes from ``computer-vision/barcodes/lookup_table.json``.

    python tools/build_labelled_bottles.py
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from convert_glb import Y_UP_TO_Z_UP, Glb

REPO = Path(__file__).resolve().parents[2]
TABLE = REPO / "computer-vision" / "barcodes" / "lookup_table.json"
OUT = REPO / "simulation" / "assets" / "labelled_bottles"

# Kit directory under assets/ for each phase, and where a separate cap comes from.
# The amber bottles are modelled closed; the HDPE ones are open, cap in its own file.
KIT_DIRS = {"liquid": "amber-bottles", "powder": "agrochemical-bottles"}
POWDER_CAPS = {100.0: "cap_100ml", 250.0: "cap_250ml", 500.0: "cap_500ml",
               1000.0: "cap_1l", 2000.0: "cap_2l"}

# Part name and wall density (kg/m^3) for each material the kits use.
MATERIALS = {
    "HDPE_blanco_satinado": ("body", 950),
    "PP_blanco_tapon": ("cap", 900),
    "Amber_Glass": ("glass", 2500),
    "White_PP": ("cap", 900),
    "Label_paper": ("label", 0),
    "Label_back": ("label_back", 0),
}
STICKER_PARTS = ("label", "label_back")


def parts_of(glb: Glb, lift: float = 0.0) -> dict[str, dict]:
    """Collect a GLB's triangles per material, in MuJoCo's frame.

    Args:
        glb: The model to read.
        lift: Metres to raise every vertex by, used to seat a cap on its bottle.

    Returns:
        Part name -> vertices, faces, optional UVs, colour and wall density.
    """
    pieces = defaultdict(list)
    scene = glb.json["scenes"][glb.json.get("scene", 0)]
    for root in scene["nodes"]:
        for _, world, mesh in glb.walk(root, Y_UP_TO_Z_UP):
            for prim in mesh["primitives"]:
                v = glb.accessor(prim["attributes"]["POSITION"])
                v = v @ world[:3, :3].T + world[:3, 3] + (0.0, 0.0, lift)
                f = glb.accessor(prim["indices"]).reshape(-1, 3)
                uv = None
                if "TEXCOORD_0" in prim["attributes"]:
                    uv = glb.accessor(prim["attributes"]["TEXCOORD_0"])
                pieces[prim["material"]].append((v, f, uv))

    parts = {}
    for material, chunks in pieces.items():
        rgba, name = glb.colour(material)
        part, density = MATERIALS[name]
        offsets = np.cumsum([0] + [len(v) for v, _, _ in chunks[:-1]])
        v = np.vstack([v for v, _, _ in chunks])
        f = np.vstack([f + o for (_, f, _), o in zip(chunks, offsets)])
        uv = chunks[0][2] if len(chunks) == 1 else None
        if uv is None:
            # Weld seam duplicates so the shell is closed, as inertia="exact" needs.
            _, first, inverse = np.unique(
                np.round(v, 5), axis=0, return_index=True, return_inverse=True)
            v, f = v[first], inverse.reshape(-1)[f]
            f = f[(f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2])]
        parts[part] = {"v": v, "f": f, "uv": uv, "rgba": rgba, "density": density}
    return parts


def write_obj(path: Path, part: dict) -> None:
    """Write one part as OBJ, with texture coordinates when it has them.

    glTF puts the UV origin at the top left of the image and OBJ at the bottom left,
    so v is flipped on the way out.
    """
    with path.open("w") as out:
        out.writelines(f"v {x:.6f} {y:.6f} {z:.6f}\n" for x, y, z in part["v"])
        if part["uv"] is None:
            out.writelines(f"f {a + 1} {b + 1} {c + 1}\n" for a, b, c in part["f"])
            return
        out.writelines(f"vt {u:.6f} {1 - v:.6f}\n" for u, v in part["uv"])
        out.writelines(
            f"f {a + 1}/{a + 1} {b + 1}/{b + 1} {c + 1}/{c + 1}\n" for a, b, c in part["f"])


def label_png(glb: Glb) -> bytes:
    """Pull the embedded label image out of a labelled GLB."""
    image = glb.json["images"][-1]
    view = glb.json["bufferViews"][image["bufferView"]]
    start = view.get("byteOffset", 0)
    return bytes(glb.bin[start:start + view["byteLength"]])


def sample_xml(sample_id: str, record: dict, parts: dict[str, dict]) -> str:
    """Write the MJCF of one sample: the shared meshes of its size plus its label."""
    vessel = record["vessel_class"]
    meshes, geoms = [], []
    for name, part in parts.items():
        mesh = f"{vessel}_{name}"
        r, g, b, a = part["rgba"]
        if name in STICKER_PARTS:
            # An open surface: shell inertia, and neither mass nor contacts.
            meshes.append(f'    <mesh name="{mesh}" file="meshes/{mesh}.obj" inertia="shell"/>')
            look = 'material="label"' if name == "label" else f'rgba="{r:.3f} {g:.3f} {b:.3f} 1"'
            geoms.append(f'      <geom name="{name}" type="mesh" mesh="{mesh}" {look}'
                         f' contype="0" conaffinity="0" mass="0"/>')
        else:
            meshes.append(f'    <mesh name="{mesh}" file="meshes/{mesh}.obj" inertia="exact"/>')
            geoms.append(f'      <geom name="{name}" type="mesh" mesh="{mesh}"'
                         f' rgba="{r:.3f} {g:.3f} {b:.3f} {a:.3f}" density="{part["density"]}"/>')
    return f"""<!-- Generated by tools/build_labelled_bottles.py. {record["material"]} ({record["phase"]}),
     {record["container_ml"]:g} ml, barcode {record["code"]}. Origin bottom-centre, +Z up, label facing -Y. -->
<mujoco model="{sample_id}">
  <asset>
{chr(10).join(meshes)}
    <texture name="label" type="2d" file="textures/{sample_id}.png"/>
    <material name="label" texture="label" specular="0.05" shininess="0.1"/>
  </asset>
  <worldbody>
    <body name="{sample_id}">
{chr(10).join(geoms)}
    </body>
  </worldbody>
</mujoco>
"""


def main() -> None:
    """Build every labelled bottle named in the lookup table."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=OUT, help="output asset directory")
    args = parser.parse_args()

    table = json.loads(TABLE.read_text())["entries"]
    (args.out / "meshes").mkdir(parents=True, exist_ok=True)
    (args.out / "textures").mkdir(parents=True, exist_ok=True)

    shared: dict[str, dict[str, dict]] = {}
    for code, record in table.items():
        record = {**record, "code": code}
        sample_id, vessel = record["sample_id"], record["vessel_class"]
        kit = REPO / "assets" / KIT_DIRS[record["phase"]]
        glb = Glb(kit / "labelled" / f"{sample_id}_{code}.glb")

        if vessel not in shared:
            parts = parts_of(glb)
            if record["phase"] == "powder":
                cap = Glb(kit / "glb" / f"{POWDER_CAPS[record['container_ml']]}_pp_white.glb")
                loose = parts_of(cap)["cap"]
                height = loose["v"][:, 2].max()
                # Screwed down, the cap overlaps the neck finish by all but a millimetre.
                seat = parts["body"]["v"][:, 2].max() - height + 0.001
                parts["cap"] = parts_of(cap, lift=seat)["cap"]
            order = sorted(parts, key=lambda name: name in STICKER_PARTS)
            shared[vessel] = {name: parts[name] for name in order}
            for name, part in shared[vessel].items():
                write_obj(args.out / "meshes" / f"{vessel}_{name}.obj", part)
            size = np.ptp(np.vstack([p["v"] for p in shared[vessel].values()]), axis=0)
            print(f"{vessel}: {', '.join(shared[vessel])}; "
                  f"{size[0] * 1e3:.0f} x {size[1] * 1e3:.0f} x {size[2] * 1e3:.0f} mm")

        (args.out / "textures" / f"{sample_id}.png").write_bytes(label_png(glb))
        (args.out / f"{sample_id}.xml").write_text(sample_xml(sample_id, record, shared[vessel]))
    print(f"{len(table)} samples -> {args.out}")


if __name__ == "__main__":
    main()
