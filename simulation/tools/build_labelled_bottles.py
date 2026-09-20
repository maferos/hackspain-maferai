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
        textures/<sample id>_cap.png        the same marker once, for the top of its cap
        <sample id>.xml                     an MJCF body: shared meshes + its texture
        meshes/<vessel_class>_shelf_<part>.obj   light stand-ins, for bottles by the hundred
        textures/shelf/<sample id>.png           the same label at half resolution
        manifest.json                            sizes, parts and samples, for generators

Each ``<sample id>.xml`` holds one body, origin at the bottom centre, +Z up, label
facing -Y, closed with its cap. Attach it like any other asset:

    <model name="pwd_0004" file="../assets/labelled_bottles/PWD-0004.xml"/>
    <frame pos="..."><attach model="pwd_0004" body="PWD-0004" prefix="p4_"/></frame>

Bottle and cap collide (convex hull) and carry the mass, with ``inertia="exact"``
because they are thin shells. The sticker is visual only: no collision, no mass, and
its own geom, so a segmentation render tells label from bottle for free.

The cap carries a second sticker, ``cap_label``: one cell of the bottle's ring (the
marker and its quiet zone) on a square inscribed in the flat top of the cap, so a
camera looking down on the bench reads the same id the ring gives from the side.
It is cut out of the ring texture rather than drawn again, so the two can never
disagree. Shelf stand-ins do without it: nobody looks down on a shelf.

The shelf stand-ins exist because the kit meshes are modelled for close-ups: a 1 L
bottle with its ribbed cap is 48 000 triangles, and the room's shelving holds
hundreds. A stand-in is the same silhouette revolved in 24 segments, 1 100 to 1 750
triangles, solid and outer wall only. It takes the same sticker mesh, so the label
sits where it does on the real bottle. ``scripts/generate_lab_room.py`` reads
``manifest.json`` to stock the shelves.

Which sample is which comes from ``computer-vision/barcodes/lookup_table.json``.

    python tools/build_labelled_bottles.py
"""

import argparse
import io
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

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
STICKER_PARTS = ("label", "label_back", "cap_label")

STICKER_LIFT = 0.0002
"""Metres a sticker floats off the surface it is stuck to, the same 0.2 mm the kits
use for the ring."""

CAP_FLAT_TOLERANCE = 0.0003
"""Vertices this close to a cap's highest point count as its flat top."""

SHELF_SEGMENTS = 24
"""Sides of a shelf stand-in. The sticker floats 0.2 mm off the true wall, and a
24-gon of the 2 L bottle dips 0.5 mm inside it between corners, so nothing pokes
through the label."""

SHELF_PROFILE_TOLERANCE = 0.0003
"""How far, in metres, the simplified silhouette may stray from the real one."""


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


def silhouette(vertices: np.ndarray, faces: np.ndarray) -> list[tuple[float, float]]:
    """Trace the outer (radius, height) profile of a part that is round about +Z.

    At each of 160 heights the profile is the widest any mesh edge gets there,
    whatever is going on inside the part: inner walls, threads, the ribs of a cap.
    Edges are used rather than vertices because a lathed wall that runs straight
    for 10 cm has no vertex along it, only one long edge. The trace is then thinned
    with Ramer-Douglas-Peucker, which keeps the corners.

    Args:
        vertices: The part's vertices, +Z up, axis through the origin.
        faces: Its triangles, as vertex indices.

    Returns:
        Profile points from the bottom pole to the top pole, ready to revolve.
    """
    radius = np.hypot(vertices[:, 0], vertices[:, 1])
    height = vertices[:, 2]
    low, high = height.min(), height.max()
    edges = np.vstack([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    za, zb = height[edges[:, 0]], height[edges[:, 1]]
    ra, rb = radius[edges[:, 0]], radius[edges[:, 1]]
    span = np.where(zb == za, 1.0, zb - za)
    points = []
    for z in np.linspace(low, high, 162)[1:-1]:
        crossing = (np.minimum(za, zb) <= z) & (z <= np.maximum(za, zb))
        t = np.clip((z - za[crossing]) / span[crossing], 0.0, 1.0)
        points.append((float((ra[crossing] + t * (rb[crossing] - ra[crossing])).max()), z))
    points = [(points[0][0], low)] + points + [(points[-1][0], high)]

    def thin(chain: list) -> list:
        if len(chain) < 3:
            return chain
        (r0, z0), (r1, z1) = chain[0], chain[-1]
        length = math.hypot(r1 - r0, z1 - z0) or 1e-12
        off = [abs((r1 - r0) * (z0 - z) - (r0 - r) * (z1 - z0)) / length for r, z in chain]
        worst = int(np.argmax(off))
        if off[worst] <= SHELF_PROFILE_TOLERANCE:
            return [chain[0], chain[-1]]
        return thin(chain[:worst + 1])[:-1] + thin(chain[worst:])

    return [(0.0, low)] + thin(points) + [(0.0, high)]


def revolve(profile: list[tuple[float, float]]) -> tuple[np.ndarray, np.ndarray]:
    """Revolve a pole-to-pole profile about +Z into a closed, outward-facing mesh."""
    angles = 2 * math.pi * np.arange(SHELF_SEGMENTS) / SHELF_SEGMENTS
    vertices, rings = [], []
    for r, z in profile:
        if r == 0:
            rings.append([len(vertices)])
            vertices.append((0.0, 0.0, z))
        else:
            rings.append(list(range(len(vertices), len(vertices) + SHELF_SEGMENTS)))
            vertices.extend((r * math.cos(a), r * math.sin(a), z) for a in angles)
    faces = []
    for lo, hi in zip(rings, rings[1:]):
        for k in range(SHELF_SEGMENTS):
            k1 = (k + 1) % SHELF_SEGMENTS
            if len(lo) == 1:
                faces.append((lo[0], hi[k1], hi[k]))
            elif len(hi) == 1:
                faces.append((lo[k], lo[k1], hi[0]))
            else:
                faces += [(lo[k], lo[k1], hi[k1]), (lo[k], hi[k1], hi[k])]
    return np.array(vertices, float), np.array(faces, int)


def cap_sticker(cap: dict) -> dict:
    """A square sticker inscribed in the flat top of a cap, UVs over the whole image.

    Args:
        cap: The cap part, vertices in the bottle's frame.

    Returns:
        A part like ``parts_of`` returns: two triangles facing +Z, no mass.
    """
    v = cap["v"]
    top = v[:, 2].max()
    flat = v[v[:, 2] > top - CAP_FLAT_TOLERANCE]
    half = np.hypot(flat[:, 0], flat[:, 1]).max() / math.sqrt(2)
    z = top + STICKER_LIFT
    corners = np.array([(-half, -half, z), (half, -half, z), (half, half, z), (-half, half, z)])
    # glTF UVs, origin top left: write_obj flips them for OBJ.
    uv = np.array([(0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0)])
    faces = np.array([(0, 1, 2), (0, 2, 3)])
    return {"v": corners, "f": faces, "uv": uv, "rgba": (1.0, 1.0, 1.0, 1.0), "density": 0}


def cap_png(ring: bytes) -> bytes:
    """Cut the middle cell out of a ring texture: one marker with its quiet zone.

    The ring is a strip of square cells rolled so a marker, not a seam, sits at its
    centre (``labvision.bottles.render_ring``), so the centre square is one whole cell.
    """
    strip = Image.open(io.BytesIO(ring))
    w, h = strip.size
    if w % h:
        raise ValueError(f"ring texture {w}x{h} is not a strip of square cells")
    cell = strip.crop((w // 2 - h // 2, 0, w // 2 + h // 2, h))
    out = io.BytesIO()
    cell.save(out, format="PNG", optimize=True)
    return out.getvalue()


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
            look = (f'material="{name}"' if name in ("label", "cap_label")
                    else f'rgba="{r:.3f} {g:.3f} {b:.3f} 1"')
            geoms.append(f'      <geom name="{name}" type="mesh" mesh="{mesh}" {look}'
                         f' contype="0" conaffinity="0" mass="0"/>')
        else:
            meshes.append(f'    <mesh name="{mesh}" file="meshes/{mesh}.obj" inertia="exact"/>')
            geoms.append(f'      <geom name="{name}" type="mesh" mesh="{mesh}"'
                         f' rgba="{r:.3f} {g:.3f} {b:.3f} {a:.3f}" density="{part["density"]}"/>')
    return f"""<!-- Generated by tools/build_labelled_bottles.py. {record["material"]} ({record["phase"]}),
     {record["container_ml"]:g} ml, marker {record["marker_id"]}, barcode {record["code"]}.
     Origin bottom-centre, +Z up, the label's front facing -Y. -->
<mujoco model="{sample_id}">
  <asset>
{chr(10).join(meshes)}
    <texture name="label" type="2d" file="textures/{sample_id}.png"/>
    <material name="label" texture="label" specular="0.05" shininess="0.1"/>
    <texture name="cap_label" type="2d" file="textures/{sample_id}_cap.png"/>
    <material name="cap_label" texture="cap_label" specular="0.05" shininess="0.1"/>
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
    (args.out / "textures" / "shelf").mkdir(parents=True, exist_ok=True)

    shared: dict[str, dict[str, dict]] = {}
    manifest = {"vessels": {}, "samples": {}}
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
            parts["cap_label"] = cap_sticker(parts["cap"])
            order = sorted(parts, key=lambda name: name in STICKER_PARTS)
            shared[vessel] = {name: parts[name] for name in order}
            triangles = {"full": 0, "shelf": 0}
            for name, part in shared[vessel].items():
                write_obj(args.out / "meshes" / f"{vessel}_{name}.obj", part)
                triangles["full"] += len(part["f"])
                light = part
                if name not in STICKER_PARTS:
                    v, f = revolve(silhouette(part["v"], part["f"]))
                    light = {"v": v, "f": f, "uv": None}
                    write_obj(args.out / "meshes" / f"{vessel}_shelf_{name}.obj", light)
                triangles["shelf"] += len(light["f"])
            # The size of the bottle as the room generators know it: without the
            # cap sticker, which they do not place and which floats off the top.
            everything = np.vstack([p["v"] for name, p in shared[vessel].items()
                                    if name != "cap_label"])
            size = np.ptp(everything, axis=0)
            manifest["vessels"][vessel] = {
                "phase": record["phase"],
                "container_ml": record["container_ml"],
                "diameter_m": round(float(max(size[0], size[1])), 5),
                "height_m": round(float(size[2]), 5),
                "parts": {name: [round(float(c), 3) for c in part["rgba"]]
                          for name, part in shared[vessel].items() if name != "cap_label"},
            }
            print(f"{vessel}: {', '.join(shared[vessel])}; "
                  f"{size[0] * 1e3:.0f} x {size[1] * 1e3:.0f} x {size[2] * 1e3:.0f} mm; "
                  f"{triangles['full']} triangles, {triangles['shelf']} as a shelf stand-in")

        # What the bottle carries is written on its label node by labvision.bottles:
        # "aruco_ring", a ring of ArUco markers, or "ean13", the one-sided barcode.
        extras = next(n["extras"] for n in glb.json["nodes"]
                      if n.get("name", "").startswith("Label_"))
        manifest["label"] = extras.get("label", "ean13")
        png = label_png(glb)
        (args.out / "textures" / f"{sample_id}.png").write_bytes(png)
        (args.out / "textures" / f"{sample_id}_cap.png").write_bytes(cap_png(png))
        # Half size by box filter: every texel is the mean of four, so a module stays
        # four whole pixels wide and the bars stay sharp.
        label = Image.open(io.BytesIO(png))
        small = label.resize((label.width // 2, label.height // 2), Image.BOX)
        small.save(args.out / "textures" / "shelf" / f"{sample_id}.png", optimize=True)
        (args.out / f"{sample_id}.xml").write_text(sample_xml(sample_id, record, shared[vessel]))
        manifest["samples"][sample_id] = {
            "vessel_class": vessel, "code": code, "marker_id": record["marker_id"],
            "material": record["material"]}

    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"{len(table)} samples -> {args.out}")


if __name__ == "__main__":
    main()
