"""Stick each powder sample's barcode label onto the bottle it belongs to.

The powder labware is the white HDPE bottle kit in
``assets/agrochemical-bottles``: one GLB per bottle size, with positions and
normals but no UVs, so a label cannot be painted onto the bottle itself. This
module adds the label the way a real one is added, as a separate sticker: a thin
curved patch that hugs the bottle's straight wall, carries its own UVs and has
the rendered label embedded as its texture. The bottle mesh is left untouched.

Which bottle a label goes on is never a choice. It follows from the sample's
``container_ml``, so a 2 L barcode cannot end up on a 100 ml bottle, and the
label is sized from the bottle it lands on: as large as the wall allows, capped
so it never wraps too far round a narrow bottle to be read.

Everything is read from the GLB rather than copied from the kit's generator, so
regenerating the kit with different dimensions needs no change here.
"""

import argparse
import json
import logging
import math
import struct
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from labvision import registry

logger = logging.getLogger(__name__)

BOTTLE_GLB_STEMS: dict[float, str] = {
    100.0: "100ml",
    250.0: "250ml",
    500.0: "500ml",
    1000.0: "1l",
    2000.0: "2l",
}
"""Kit file stem for each powder ``container_ml``, as in ``bottle_<stem>_*.glb``."""

NOMINAL_MODULE_M = 0.00033
"""Width of one EAN-13 module at 100 % magnification, 0.33 mm."""

MAX_MAGNIFICATION = 1.5
"""Largest label printed, as a multiple of nominal. The specification allows up
to 2.0; 1.5 keeps the label a label rather than a wrap on the 2 L bottle."""

MAX_ARC_DEG = 50.0
"""Most of the bottle's circumference a label may cover.

A barcode wrapped round a cylinder is squeezed towards its edges when seen
head-on, and the reader, which expects even modules, gives up quickly. Measured
over all 100 powder labels projected onto a cylinder: every one decodes up to 55
degrees of arc, 86 at 60 degrees and 72 at 75. The nominal-size label on the
46 mm bottle would span 99 degrees. 50 keeps a margin below the cliff.
"""

WALL_MARGIN_M = 0.003
"""Clearance kept between the label and either end of the straight wall."""

LABEL_OFFSET_M = 0.0002
"""How far the sticker sits off the bottle wall. Thick for paper, but it keeps
the two surfaces from z-fighting in a renderer with a coarse depth buffer."""

ARC_SEGMENTS = 32
"""Quads round the label's arc. The arc is at most 50 degrees, so each facet
turns through under 2 degrees."""

TEXTURE_MODULE_PX = 8
"""Pixels per barcode module in the embedded texture."""

_GLB_MAGIC = 0x46546C67
_CHUNK_JSON = 0x4E4F534A
_CHUNK_BIN = 0x004E4942
_FLOAT = 5126
_UNSIGNED_SHORT = 5123
_ARRAY_BUFFER = 34962
_ELEMENT_ARRAY_BUFFER = 34963


class BottleError(Exception):
    """Raised when a bottle cannot be read, or a label cannot be put on it."""


@dataclass
class Glb:
    """A binary glTF file held in memory.

    Attributes:
        document: The parsed JSON chunk.
        buffer: The binary chunk, which is buffer 0 of the document.
    """

    document: dict
    buffer: bytes


@dataclass(frozen=True)
class Wall:
    """The straight, vertical part of a bottle's side, where a label can sit.

    Attributes:
        radius_m: Outer radius of the bottle body.
        bottom_m: Height at which the wall starts, above the rounded heel.
        top_m: Height at which the wall ends and the shoulder begins.
    """

    radius_m: float
    bottom_m: float
    top_m: float


@dataclass(frozen=True)
class LabelPatch:
    """A curved sticker mesh, in the bottle's own glTF frame (Y up, +Z front).

    Attributes:
        positions: Vertex positions in metres, shape (n, 3).
        normals: Unit vertex normals pointing away from the bottle, shape (n, 3).
        uvs: Texture coordinates with the glTF origin at top left, shape (n, 2).
        indices: Triangle vertex indices, counter-clockwise seen from outside.
        module_m: Printed width of one barcode module.
        width_m: Label width measured round the arc.
        height_m: Label height.
        arc_deg: Angle the label spans round the bottle.
    """

    positions: np.ndarray
    normals: np.ndarray
    uvs: np.ndarray
    indices: np.ndarray
    module_m: float
    width_m: float
    height_m: float
    arc_deg: float

    @property
    def corners_m(self) -> list[list[float]]:
        """Corner positions, as top-left, top-right, bottom-right, bottom-left

        Returns:
            Four (x, y, z) points in the bottle's frame, in the order a reader
            would meet them looking at the label. These are the ground-truth
            keypoints of the label quad.
        """
        bottom = self.positions[: ARC_SEGMENTS + 1]
        top = self.positions[ARC_SEGMENTS + 1 :]
        picked = (top[0], top[-1], bottom[-1], bottom[0])
        return [[round(float(c), 6) for c in p] for p in picked]


def read_glb(path: Path) -> Glb:
    """Read a binary glTF file

    Args:
        path: A ``.glb`` file with one JSON chunk and one binary chunk.

    Returns:
        The parsed document and its binary buffer.

    Raises:
        BottleError: If the file is missing or is not a two-chunk GLB.
    """
    if not path.exists():
        raise BottleError(f"bottle model not found: {path}")
    data = path.read_bytes()
    try:
        magic, _, _ = struct.unpack_from("<III", data, 0)
        json_len, json_type = struct.unpack_from("<II", data, 12)
        bin_len, bin_type = struct.unpack_from("<II", data, 20 + json_len)
    except struct.error as e:
        raise BottleError(f"truncated GLB: {path}") from e
    if (magic, json_type, bin_type) != (_GLB_MAGIC, _CHUNK_JSON, _CHUNK_BIN):
        raise BottleError(f"not a two-chunk GLB: {path}")
    document = json.loads(data[20:20 + json_len])
    start = 28 + json_len
    return Glb(document, data[start:start + bin_len])


def write_glb(glb: Glb, path: Path) -> Path:
    """Write a binary glTF file

    Args:
        glb: The document and buffer to serialise.
        path: Destination file. Parent directories are created.

    Returns:
        The path written.
    """
    text = json.dumps(glb.document, separators=(",", ":")).encode("utf-8")
    text += b" " * (-len(text) % 4)
    binary = glb.buffer + b"\x00" * (-len(glb.buffer) % 4)
    total = 12 + 8 + len(text) + 8 + len(binary)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join((
        struct.pack("<III", _GLB_MAGIC, 2, total),
        struct.pack("<II", len(text), _CHUNK_JSON), text,
        struct.pack("<II", len(binary), _CHUNK_BIN), binary,
    )))
    return path


def bottle_node(glb: Glb) -> int:
    """Find the node that carries the bottle mesh

    Args:
        glb: A bottle model from the kit.

    Returns:
        Index of the first node with a mesh.

    Raises:
        BottleError: If no node has a mesh.
    """
    for index, node in enumerate(glb.document.get("nodes", [])):
        if "mesh" in node:
            return index
    raise BottleError("bottle model has no mesh node")


def straight_wall(glb: Glb) -> Wall:
    """Measure the straight part of a bottle's side from its mesh

    The kit's bottles are lathed, so the widest vertices all lie on the straight
    wall: it begins where the heel's rounding ends and stops where the shoulder
    starts. The threads are on the neck, well inside that radius.

    Args:
        glb: A bottle model, Y up, with its origin at the centre of its base.

    Returns:
        The wall's radius and its lower and upper heights.

    Raises:
        BottleError: If the mesh has no float positions, or no wall to speak of.
    """
    document = glb.document
    mesh = document["meshes"][document["nodes"][bottle_node(glb)]["mesh"]]
    accessor = document["accessors"][mesh["primitives"][0]["attributes"]["POSITION"]]
    if accessor["componentType"] != _FLOAT or accessor["type"] != "VEC3":
        raise BottleError("bottle positions are not float VEC3")
    view = document["bufferViews"][accessor["bufferView"]]
    if "byteStride" in view:
        raise BottleError("interleaved bottle meshes are not supported")
    offset = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
    points = np.frombuffer(
        glb.buffer, dtype="<f4", count=accessor["count"] * 3, offset=offset,
    ).reshape(-1, 3)
    radii = np.hypot(points[:, 0], points[:, 2])
    radius = float(radii.max())
    heights = points[radii > radius - 1e-5, 1]
    wall = Wall(radius, float(heights.min()), float(heights.max()))
    if wall.top_m - wall.bottom_m <= 2 * WALL_MARGIN_M:
        raise BottleError("bottle has no straight wall to label")
    return wall


def label_patch(wall: Wall, modules_wide: float, modules_high: float) -> LabelPatch:
    """Build the sticker mesh for one bottle, sized to that bottle

    The label is printed as large as three limits allow: MAX_MAGNIFICATION, the
    MAX_ARC_DEG of circumference it may cover, and the height of the straight
    wall less a margin. It is centred on the wall's height and faces +Z, the
    front of a glTF model.

    Args:
        wall: The bottle's straight wall, from straight_wall.
        modules_wide: Label width in barcode modules, margins included.
        modules_high: Label height in barcode modules.

    Returns:
        The patch, two rows of vertices round the arc.

    Example:
        >>> patch = label_patch(Wall(0.023, 0.006, 0.050), 121, 59)
        >>> round(patch.arc_deg), round(patch.module_m * 1e3, 3)
        (50, 0.167)
        >>> patch = label_patch(Wall(0.058, 0.015, 0.142), 121, 59)
        >>> round(patch.arc_deg), round(patch.module_m * 1e3, 3)
        (50, 0.42)
    """
    radius = wall.radius_m + LABEL_OFFSET_M
    module = min(
        NOMINAL_MODULE_M * MAX_MAGNIFICATION,
        radius * math.radians(MAX_ARC_DEG) / modules_wide,
        (wall.top_m - wall.bottom_m - 2 * WALL_MARGIN_M) / modules_high,
    )
    width, height = module * modules_wide, module * modules_high
    arc = width / radius
    middle = (wall.bottom_m + wall.top_m) / 2
    y_bottom, y_top = middle - height / 2, middle + height / 2

    # Angle runs from +Z towards +X, which is left to right for someone facing
    # the label, so u grows with it. Bottom row first, then the top row.
    u = np.linspace(0.0, 1.0, ARC_SEGMENTS + 1)
    angle = (u - 0.5) * arc
    side = np.stack([np.sin(angle), np.zeros_like(angle), np.cos(angle)], axis=1)
    bottom = side * radius + [0.0, y_bottom, 0.0]
    top = side * radius + [0.0, y_top, 0.0]
    uv_bottom = np.stack([u, np.ones_like(u)], axis=1)
    uv_top = np.stack([u, np.zeros_like(u)], axis=1)

    k = np.arange(ARC_SEGMENTS)
    n = ARC_SEGMENTS + 1
    triangles = np.concatenate([
        np.stack([k, k + 1, k + 1 + n], axis=1),
        np.stack([k, k + 1 + n, k + n], axis=1),
    ])
    return LabelPatch(
        positions=np.concatenate([bottom, top]).astype("<f4"),
        normals=np.concatenate([side, side]).astype("<f4"),
        uvs=np.concatenate([uv_bottom, uv_top]).astype("<f4"),
        indices=triangles.reshape(-1).astype("<u2"),
        module_m=module,
        width_m=width,
        height_m=height,
        arc_deg=math.degrees(arc),
    )


def attach_label(
    glb: Glb,
    patch: LabelPatch,
    png: bytes,
    name: str,
    extras: dict[str, object],
) -> Glb:
    """Add a textured label to a bottle model, as a child of the bottle

    The bottle's own mesh, material and buffers are carried over unchanged; the
    label's geometry and its PNG are appended to the same binary buffer.

    Args:
        glb: The bottle model. Not modified.
        patch: Sticker mesh, from label_patch.
        png: The label image, PNG-encoded.
        name: Name given to the label's node and mesh.
        extras: Metadata stored on the label node, where a consumer can read
            which sample the label names without decoding it.

    Returns:
        A new model holding the bottle and its label.
    """
    document = json.loads(json.dumps(glb.document))
    buffer = bytearray(glb.buffer)

    def add_view(data: bytes, target: int | None) -> int:
        buffer.extend(b"\x00" * (-len(buffer) % 4))
        view = {"buffer": 0, "byteOffset": len(buffer), "byteLength": len(data)}
        if target is not None:
            view["target"] = target
        buffer.extend(data)
        document["bufferViews"].append(view)
        return len(document["bufferViews"]) - 1

    def add_accessor(array: np.ndarray, kind: str, target: int, bounds: bool) -> int:
        accessor = {
            "bufferView": add_view(array.tobytes(), target),
            "componentType": _UNSIGNED_SHORT if kind == "SCALAR" else _FLOAT,
            "count": len(array),
            "type": kind,
        }
        if bounds:
            accessor["min"] = array.min(axis=0).tolist()
            accessor["max"] = array.max(axis=0).tolist()
        document["accessors"].append(accessor)
        return len(document["accessors"]) - 1

    attributes = {
        "POSITION": add_accessor(patch.positions, "VEC3", _ARRAY_BUFFER, True),
        "NORMAL": add_accessor(patch.normals, "VEC3", _ARRAY_BUFFER, False),
        "TEXCOORD_0": add_accessor(patch.uvs, "VEC2", _ARRAY_BUFFER, False),
    }
    indices = add_accessor(patch.indices, "SCALAR", _ELEMENT_ARRAY_BUFFER, False)

    image_view = add_view(png, None)
    document.setdefault("images", []).append(
        {"bufferView": image_view, "mimeType": "image/png", "name": name},
    )
    # Nearest-neighbour magnification keeps bar edges crisp close up; mipmapped
    # minification keeps them from shimmering far away.
    document.setdefault("samplers", []).append(
        {"magFilter": 9728, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071},
    )
    document.setdefault("textures", []).append({
        "sampler": len(document["samplers"]) - 1,
        "source": len(document["images"]) - 1,
    })
    document["materials"].append({
        "name": "Label_paper",
        "pbrMetallicRoughness": {
            "baseColorTexture": {"index": len(document["textures"]) - 1},
            "metallicFactor": 0.0,
            "roughnessFactor": 0.6,
        },
    })
    document["meshes"].append({
        "name": name,
        "primitives": [{
            "attributes": attributes,
            "indices": indices,
            "material": len(document["materials"]) - 1,
        }],
    })
    document["nodes"].append({
        "name": name,
        "mesh": len(document["meshes"]) - 1,
        "extras": extras,
    })
    parent = document["nodes"][bottle_node(glb)]
    parent.setdefault("children", []).append(len(document["nodes"]) - 1)

    buffer.extend(b"\x00" * (-len(buffer) % 4))
    document["buffers"][0]["byteLength"] = len(buffer)
    return Glb(document, bytes(buffer))


def bottle_path(container_ml: float, kit_dir: Path) -> Path:
    """Locate the kit's bottle for a container size

    Args:
        container_ml: A powder container capacity from BOTTLE_VOLUMES_ML.
        kit_dir: The ``assets/agrochemical-bottles`` directory.

    Returns:
        Path of that size's bottle GLB.

    Raises:
        BottleError: If the kit has no bottle of that capacity.

    Example:
        >>> bottle_path(1000.0, Path("kit")).name
        'bottle_1l_hdpe_white.glb'
    """
    stem = BOTTLE_GLB_STEMS.get(container_ml)
    if stem is None:
        raise BottleError(f"the kit has no {container_ml:g} ml bottle")
    return kit_dir / "glb" / f"bottle_{stem}_hdpe_white.glb"


def labelled_bottle(entry: registry.Entry, kit_dir: Path) -> tuple[Glb, LabelPatch]:
    """Put a sample's label on the bottle that sample is stored in

    The bottle is chosen from the sample's own ``container_ml``, never passed
    in, so a label cannot be attached to a bottle of another size.

    Args:
        entry: A powder row of the registry.
        kit_dir: The ``assets/agrochemical-bottles`` directory.

    Returns:
        The labelled model, and the patch that was attached to it.

    Raises:
        BottleError: If the sample is not a powder, or the kit lacks its bottle.
    """
    sample = entry.sample
    if sample.phase != registry.POWDER.name:
        raise BottleError(
            f"{sample.sample_id} is a {sample.phase}, and only powders go in bottles"
        )
    bottle = read_glb(bottle_path(sample.container_ml, kit_dir))
    image = registry.render_label(entry, TEXTURE_MODULE_PX)
    patch = label_patch(
        straight_wall(bottle),
        image.shape[1] / TEXTURE_MODULE_PX,
        image.shape[0] / TEXTURE_MODULE_PX,
    )
    ok, png = cv2.imencode(".png", image)
    if not ok:
        raise BottleError(f"could not encode the label of {sample.sample_id}")
    extras = {
        "code": entry.code,
        "sample_id": sample.sample_id,
        "material": sample.material,
        "container_ml": sample.container_ml,
        "vessel_class": sample.vessel_class,
        "module_mm": round(patch.module_m * 1e3, 4),
        "corners_m": patch.corners_m,
    }
    labelled = attach_label(
        bottle, patch, png.tobytes(), f"Label_{sample.sample_id}", extras,
    )
    return labelled, patch


def write_labelled_bottles(
    entries: list[registry.Entry],
    kit_dir: Path,
    out_dir: Path,
) -> list[Path]:
    """Write one labelled bottle model per powder row

    Args:
        entries: Registry rows. Liquid rows are skipped, as they have no bottle.
        kit_dir: The ``assets/agrochemical-bottles`` directory.
        out_dir: Directory for the GLBs. Created if absent.

    Returns:
        The paths written, in entry order.

    Raises:
        BottleError: If the kit lacks a bottle that some powder row needs.
    """
    paths = []
    for entry in entries:
        if entry.sample.phase != registry.POWDER.name:
            continue
        labelled, patch = labelled_bottle(entry, kit_dir)
        path = out_dir / f"{entry.sample.sample_id}_{entry.code}.glb"
        paths.append(write_glb(labelled, path))
        logger.debug(
            "%s: %.1f x %.1f mm label over %.0f degrees",
            path.name, patch.width_m * 1e3, patch.height_m * 1e3, patch.arc_deg,
        )
    return paths


def main() -> None:
    """Generate the labelled powder bottles."""
    kit = Path(__file__).resolve().parents[2] / "assets" / "agrochemical-bottles"
    parser = argparse.ArgumentParser(
        description="Stick every powder barcode onto the bottle of its size.",
    )
    parser.add_argument(
        "out_dir", type=Path, nargs="?", default=kit / "labelled",
        help="Directory for the labelled GLBs (default: <kit>/labelled).",
    )
    parser.add_argument(
        "--kit", type=Path, default=kit,
        help="The agrochemical-bottles asset directory.",
    )
    parser.add_argument(
        "--seed", type=int, default=registry.DEFAULT_SEED,
        help=f"Seed for the catalogue (default: {registry.DEFAULT_SEED}).",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    entries = registry.build_registry(registry.default_samples(seed=args.seed))
    paths = write_labelled_bottles(entries, args.kit, args.out_dir)
    print(f"{len(paths)} labelled bottles -> {args.out_dir}")
    for container_ml in BOTTLE_GLB_STEMS:
        first = next(e for e in entries if e.sample.container_ml == container_ml
                     and e.sample.phase == registry.POWDER.name)
        _, patch = labelled_bottle(first, args.kit)
        print(
            f"  {container_ml:>6g} ml: label {patch.width_m * 1e3:.1f} x "
            f"{patch.height_m * 1e3:.1f} mm, {patch.arc_deg:.0f} deg of arc, "
            f"{patch.module_m / NOMINAL_MODULE_M:.0%} magnification"
        )


if __name__ == "__main__":
    main()
