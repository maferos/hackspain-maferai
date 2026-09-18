"""Stick each sample's barcode label onto the bottle it belongs to.

Each phase has its own labware, a kit of GLBs under ``assets/``: powders go in the
white HDPE bottles of ``agrochemical-bottles``, liquids in the amber glass bottles
of ``amber-bottles``. Neither kit has UVs, so a label cannot be painted onto the
bottle itself. This module adds the label the way a real one is added, as a
separate sticker: a thin curved patch that hugs the bottle's straight wall,
carries its own UVs and has the rendered label embedded as its texture. The
bottle's meshes are left untouched.

Which bottle a label goes on is never a choice. It follows from the sample's
phase and ``container_ml``, so a 2 L barcode cannot end up on a 100 ml bottle, nor
a liquid's on a powder bottle, and the
label is sized from the bottle it lands on, as large as the wall allows.

The label goes on turned a quarter turn, in "ladder" orientation: the bars lie
flat, stacked up the bottle, and the text reads from bottom to top. That is how
barcodes go on narrow bottles, because of what curvature does. Seen head-on, a
cylinder squeezes whatever runs round it and leaves alone whatever runs up it.
An upright barcode has its bar *widths* running round the bottle, which is the
one thing a reader measures, so it stops decoding once it wraps about 55 degrees.
A ladder barcode has only its bar *lengths* squeezed, which carry no information.

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

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"
"""The repository's ``assets`` directory, which holds every kit."""


@dataclass(frozen=True)
class Kit:
    """The labware of one phase: a directory of bottle models, one per size.

    Attributes:
        phase: The registry phase stored in these bottles.
        directory: Kit directory name under ``assets``. Its ``glb`` folder holds
            the models and its ``labelled`` folder receives the labelled ones.
        files: GLB file name for each ``container_ml`` the phase uses.
    """

    phase: str
    directory: str
    files: dict[float, str]


POWDER_KIT = Kit("powder", "agrochemical-bottles", {
    100.0: "bottle_100ml_hdpe_white.glb",
    250.0: "bottle_250ml_hdpe_white.glb",
    500.0: "bottle_500ml_hdpe_white.glb",
    1000.0: "bottle_1l_hdpe_white.glb",
    2000.0: "bottle_2l_hdpe_white.glb",
})
"""White HDPE bottles, open, cap in a separate file."""

LIQUID_KIT = Kit("liquid", "amber-bottles", {
    10.0: "amber_bottle_010ml.glb",
    20.0: "amber_bottle_020ml.glb",
    30.0: "amber_bottle_030ml.glb",
    50.0: "amber_bottle_050ml.glb",
    100.0: "amber_bottle_100ml.glb",
})
"""Amber glass bottles, closed, the cap a child node of the bottle. The kit also
has a 60 ml bottle, which no liquid row uses: adding a size to the catalogue
renumbers the samples and so reissues every liquid barcode."""

KITS: dict[str, Kit] = {kit.phase: kit for kit in (POWDER_KIT, LIQUID_KIT)}
"""The kit for each registry phase."""

NOMINAL_MODULE_M = 0.00033
"""Width of one EAN-13 module at 100 % magnification, 0.33 mm."""

MAX_MAGNIFICATION = 2.0
"""Largest label printed, as a multiple of nominal. This is the ceiling the
EAN-13 specification itself sets."""

MAX_ARC_DEG = 90.0
"""Most of the bottle's circumference a label may cover.

In ladder orientation this is not a decoding limit: all 100 powder labels,
projected onto a cylinder, decode at 60, 90 and 120 degrees of arc, down to three
pixels per module. It only keeps the whole label, captions included, in view from
one side. On the kit as it stands the wall height or MAX_MAGNIFICATION binds
first, and no label reaches it.

For comparison, the same labels stuck on upright decode 100 out of 100 up to 55
degrees, 86 at 60 and 72 at 75, which is why they are not stuck on upright.
"""

WALL_MARGIN_M = 0.003
"""Clearance kept between the label and either end of the straight wall."""

LABEL_OFFSET_M = 0.0002
"""How far the sticker sits off the bottle wall. Thick for paper, but it keeps
the two surfaces from z-fighting in a renderer with a coarse depth buffer."""

ARC_SEGMENTS = 32
"""Quads round the label's arc. The arc is at most 90 degrees, so each facet
turns through under 3 degrees."""

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
            They turn the texture a quarter turn anticlockwise, so the embedded
            image stays an upright label and only its mapping is rotated.
        indices: Triangle vertex indices, counter-clockwise seen from outside.
        module_m: Printed width of one barcode module.
        width_m: Extent of the sticker round the arc, which is the printed
            label's height, since the label is turned.
        height_m: Extent of the sticker up the bottle, the printed label's width.
        arc_deg: Angle the sticker spans round the bottle.
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

        The names are the printed label's own, not the viewer's. The label is
        turned a quarter turn anticlockwise, so its top-left corner sits at the
        sticker's bottom left as seen on the bottle, and its top edge runs up the
        sticker's left side.

        Returns:
            Four (x, y, z) points in the bottle's frame. These are the
            ground-truth keypoints of the label quad, in an order that maps
            straight onto an upright label image.
        """
        bottom = self.positions[: ARC_SEGMENTS + 1]
        top = self.positions[ARC_SEGMENTS + 1 :]
        picked = (bottom[0], top[0], top[-1], bottom[-1])
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

    The powder kit's files hold the bottle alone, but the liquid kit's hold a
    closed bottle, with the cap as a second mesh listed first. The bottle is the
    tallest mesh in either.

    Args:
        glb: A bottle model from a kit.

    Returns:
        Index of the mesh node whose mesh is tallest.

    Raises:
        BottleError: If no node has a mesh.
    """
    document = glb.document
    heights: dict[int, float] = {}
    for index, node in enumerate(document.get("nodes", [])):
        if "mesh" not in node:
            continue
        primitive = document["meshes"][node["mesh"]]["primitives"][0]
        bounds = document["accessors"][primitive["attributes"]["POSITION"]]
        heights[index] = bounds["max"][1] - bounds["min"][1]
    if not heights:
        raise BottleError("bottle model has no mesh node")
    return max(heights, key=heights.__getitem__)


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

    The label is turned a quarter turn, so its width runs up the bottle and its
    height runs round it. It is printed as large as three limits allow:
    MAX_MAGNIFICATION, the height of the straight wall less a margin, and the
    MAX_ARC_DEG of circumference it may cover. It is centred on the wall's height
    and faces +Z, the front of a glTF model.

    Args:
        wall: The bottle's straight wall, from straight_wall.
        modules_wide: Width of the upright label in barcode modules, margins
            included. This is the side that ends up running up the bottle.
        modules_high: Height of the upright label in barcode modules.

    Returns:
        The patch, two rows of vertices round the arc.

    Example:
        >>> patch = label_patch(Wall(0.023, 0.006, 0.050), 121, 59)
        >>> round(patch.arc_deg), round(patch.module_m * 1e3, 3)
        (46, 0.314)
        >>> patch = label_patch(Wall(0.058, 0.015, 0.142), 121, 59)
        >>> round(patch.arc_deg), round(patch.module_m * 1e3, 3)
        (38, 0.66)
    """
    radius = wall.radius_m + LABEL_OFFSET_M
    module = min(
        NOMINAL_MODULE_M * MAX_MAGNIFICATION,
        radius * math.radians(MAX_ARC_DEG) / modules_high,
        (wall.top_m - wall.bottom_m - 2 * WALL_MARGIN_M) / modules_wide,
    )
    width, height = module * modules_high, module * modules_wide
    arc = width / radius
    middle = (wall.bottom_m + wall.top_m) / 2
    y_bottom, y_top = middle - height / 2, middle + height / 2

    # Angle runs from +Z towards +X, which is left to right for someone facing
    # the bottle. Bottom row first, then the top row. The texture is turned a
    # quarter turn anticlockwise: its left edge (u = 0) lies along the bottom of
    # the sticker, and its top edge (v = 0) up the sticker's left side.
    across = np.linspace(0.0, 1.0, ARC_SEGMENTS + 1)
    angle = (across - 0.5) * arc
    side = np.stack([np.sin(angle), np.zeros_like(angle), np.cos(angle)], axis=1)
    bottom = side * radius + [0.0, y_bottom, 0.0]
    top = side * radius + [0.0, y_top, 0.0]
    uv_bottom = np.stack([np.zeros_like(across), across], axis=1)
    uv_top = np.stack([np.ones_like(across), across], axis=1)

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

    On a see-through bottle the sticker also gets a plain white back, facing
    into the bottle. Without one the label would vanish when seen from behind
    through the glass; with the printed face shown on both sides instead, the
    barcode would read, mirrored, through the bottle, which no paper label does.

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
    primitives = [{
        "attributes": attributes,
        "indices": indices,
        "material": len(document["materials"]) - 1,
    }]
    if is_see_through(glb):
        inwards = patch.positions.copy()
        radius = np.hypot(inwards[:, 0], inwards[:, 2])
        inwards[:, [0, 2]] *= ((radius - LABEL_OFFSET_M / 2) / radius)[:, None]
        flipped = patch.indices.reshape(-1, 3)[:, ::-1].reshape(-1)
        document["materials"].append({
            "name": "Label_back",
            "pbrMetallicRoughness": {
                "baseColorFactor": [0.95, 0.95, 0.93, 1.0],
                "metallicFactor": 0.0,
                "roughnessFactor": 0.7,
            },
        })
        primitives.append({
            "attributes": {
                "POSITION": add_accessor(inwards, "VEC3", _ARRAY_BUFFER, True),
                "NORMAL": add_accessor(-patch.normals, "VEC3", _ARRAY_BUFFER, False),
            },
            "indices": add_accessor(
                np.ascontiguousarray(flipped), "SCALAR", _ELEMENT_ARRAY_BUFFER, False,
            ),
            "material": len(document["materials"]) - 1,
        })
    document["meshes"].append({"name": name, "primitives": primitives})
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


def is_see_through(glb: Glb) -> bool:
    """Tell whether the bottle is made of something light passes through

    Args:
        glb: A bottle model from a kit.

    Returns:
        True when the bottle mesh's material transmits light, as the amber glass
        does and the white HDPE does not.
    """
    document = glb.document
    mesh = document["meshes"][document["nodes"][bottle_node(glb)]["mesh"]]
    material = document["materials"][mesh["primitives"][0]["material"]]
    return "KHR_materials_transmission" in material.get("extensions", {})


def bottle_path(sample: registry.Sample, assets_dir: Path = ASSETS_DIR) -> Path:
    """Locate the bottle a sample is stored in

    Args:
        sample: The sample. Its phase picks the kit and its container_ml the
            bottle within it.
        assets_dir: The repository's ``assets`` directory.

    Returns:
        Path of that bottle's GLB.

    Raises:
        BottleError: If the phase has no kit, or the kit no bottle of that size.

    Example:
        >>> powder = registry.Sample("PWD-1", "Vanillin", "121-33-5", "powder",
        ...                          1000.0, "L1")
        >>> bottle_path(powder, Path("assets")).as_posix()
        'assets/agrochemical-bottles/glb/bottle_1l_hdpe_white.glb'
        >>> liquid = registry.Sample("SMP-1", "Limonene", "5989-27-5", "liquid",
        ...                          50.0, "L1")
        >>> bottle_path(liquid, Path("assets")).as_posix()
        'assets/amber-bottles/glb/amber_bottle_050ml.glb'
    """
    kit = KITS.get(sample.phase)
    if kit is None:
        raise BottleError(f"no kit holds {sample.phase} samples")
    name = kit.files.get(sample.container_ml)
    if name is None:
        raise BottleError(
            f"the {sample.phase} kit has no {sample.container_ml:g} ml bottle"
        )
    return assets_dir / kit.directory / "glb" / name


def labelled_bottle(
    entry: registry.Entry,
    assets_dir: Path = ASSETS_DIR,
) -> tuple[Glb, LabelPatch]:
    """Put a sample's label on the bottle that sample is stored in

    The bottle is chosen from the sample's own phase and ``container_ml``, never
    passed in, so a label cannot be attached to a bottle of another size or kind.

    Args:
        entry: A row of the registry.
        assets_dir: The repository's ``assets`` directory.

    Returns:
        The labelled model, and the patch that was attached to it.

    Raises:
        BottleError: If no kit has a bottle for the sample.
    """
    sample = entry.sample
    bottle = read_glb(bottle_path(sample, assets_dir))
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


def labelled_path(entry: registry.Entry, assets_dir: Path = ASSETS_DIR) -> Path:
    """Say where a sample's labelled bottle is kept

    Args:
        entry: A row of the registry.
        assets_dir: The repository's ``assets`` directory.

    Returns:
        ``<kit>/labelled/<sample id>_<code>.glb``, inside the sample's own kit.

    Raises:
        BottleError: If the sample's phase has no kit.
    """
    kit = KITS.get(entry.sample.phase)
    if kit is None:
        raise BottleError(f"no kit holds {entry.sample.phase} samples")
    name = f"{entry.sample.sample_id}_{entry.code}.glb"
    return assets_dir / kit.directory / "labelled" / name


def write_labelled_bottles(
    entries: list[registry.Entry],
    assets_dir: Path = ASSETS_DIR,
    out_dir: Path | None = None,
) -> list[Path]:
    """Write one labelled bottle model per registry row

    Args:
        entries: Registry rows to label.
        assets_dir: The repository's ``assets`` directory.
        out_dir: Directory for every GLB. When omitted each model goes to the
            ``labelled`` folder of its own kit, which is where they are kept.

    Returns:
        The paths written, in entry order.

    Raises:
        BottleError: If a kit lacks a bottle that some row needs.
    """
    paths = []
    for entry in entries:
        labelled, patch = labelled_bottle(entry, assets_dir)
        path = labelled_path(entry, assets_dir)
        if out_dir is not None:
            path = out_dir / path.name
        paths.append(write_glb(labelled, path))
        logger.debug(
            "%s: %.1f x %.1f mm label over %.0f degrees",
            path.name, patch.width_m * 1e3, patch.height_m * 1e3, patch.arc_deg,
        )
    return paths


def main() -> None:
    """Generate the labelled bottles of every kit."""
    parser = argparse.ArgumentParser(
        description="Stick every barcode onto the bottle of its phase and size.",
    )
    parser.add_argument(
        "--assets", type=Path, default=ASSETS_DIR,
        help="The repository's assets directory, which holds the kits.",
    )
    parser.add_argument(
        "--phase", choices=sorted(KITS), default=None,
        help="Label only this phase's bottles (default: every phase).",
    )
    parser.add_argument(
        "--seed", type=int, default=registry.DEFAULT_SEED,
        help=f"Seed for the catalogue (default: {registry.DEFAULT_SEED}).",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    entries = registry.build_registry(registry.default_samples(seed=args.seed))
    for kit in KITS.values():
        if args.phase not in (None, kit.phase):
            continue
        rows = [e for e in entries if e.sample.phase == kit.phase]
        paths = write_labelled_bottles(rows, args.assets)
        print(f"{len(paths)} {kit.phase} bottles -> {paths[0].parent}")
        for container_ml in kit.files:
            first = next(e for e in rows if e.sample.container_ml == container_ml)
            _, patch = labelled_bottle(first, args.assets)
            print(
                f"  {container_ml:>6g} ml: label {patch.width_m * 1e3:.1f} x "
                f"{patch.height_m * 1e3:.1f} mm, {patch.arc_deg:.0f} deg of arc, "
                f"{patch.module_m / NOMINAL_MODULE_M:.0%} magnification"
            )


if __name__ == "__main__":
    main()
