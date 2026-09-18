"""Tests for sticking powder labels onto the bottle kit."""

import math
from pathlib import Path

import cv2
import numpy as np
import pytest

from labvision import bottles, reader, registry

KIT = Path(__file__).parents[2] / "assets" / "agrochemical-bottles"

# Body diameter of each bottle in millimetres, from the kit's README.
KIT_DIAMETERS_MM = {100.0: 46, 250.0: 60, 500.0: 74, 1000.0: 88, 2000.0: 116}


def powder_entries() -> list[registry.Entry]:
    entries = registry.build_registry(registry.default_samples())
    return [e for e in entries if e.sample.phase == "powder"]


def one_entry_per_size() -> list[registry.Entry]:
    return powder_entries()[: len(registry.BOTTLE_VOLUMES_ML)]


def vessel_class(entry: registry.Entry) -> str:
    return entry.sample.vessel_class


def accessor_array(glb: bottles.Glb, index: int, width: int, dtype: str) -> np.ndarray:
    accessor = glb.document["accessors"][index]
    view = glb.document["bufferViews"][accessor["bufferView"]]
    return np.frombuffer(
        glb.buffer, dtype=dtype, count=accessor["count"] * width,
        offset=view.get("byteOffset", 0),
    ).reshape(-1, width)


def label_image(glb: bottles.Glb) -> np.ndarray:
    view = glb.document["bufferViews"][glb.document["images"][-1]["bufferView"]]
    png = glb.buffer[view["byteOffset"]:view["byteOffset"] + view["byteLength"]]
    return cv2.imdecode(np.frombuffer(png, dtype=np.uint8), cv2.IMREAD_COLOR)


def seen_on_cylinder(label: np.ndarray, arc_deg: float) -> np.ndarray:
    """Project a label wrapped round a cylinder onto a head-on camera.

    Orthographic, looking straight at the label's centre: a point at angle phi
    round the bottle lands at sin(phi), so the edges of the label are squeezed.
    """
    height, width = label.shape[:2]
    half = math.radians(arc_deg) / 2
    out_width = int(round(width * math.sin(half) / half))
    x = (np.arange(out_width) + 0.5) / out_width * 2 - 1
    phi = np.arcsin(x * math.sin(half))
    map_x = ((phi / (2 * half) + 0.5) * width - 0.5).astype(np.float32)
    map_x = np.tile(map_x, (height, 1))
    map_y = np.tile(np.arange(height, dtype=np.float32)[:, None], (1, out_width))
    return cv2.remap(label, map_x, map_y, cv2.INTER_AREA, borderValue=(255, 255, 255))


def test_every_powder_size_has_a_bottle_in_the_kit() -> None:
    assert set(bottles.BOTTLE_GLB_STEMS) == set(registry.BOTTLE_VOLUMES_ML)
    for volume in registry.BOTTLE_VOLUMES_ML:
        assert bottles.bottle_path(volume, KIT).exists(), volume


def test_bottle_path_rejects_a_size_the_kit_lacks() -> None:
    with pytest.raises(bottles.BottleError, match="no 50 ml bottle"):
        bottles.bottle_path(50.0, KIT)


@pytest.mark.parametrize("volume", registry.BOTTLE_VOLUMES_ML)
def test_straight_wall_matches_the_kit_dimensions(volume: float) -> None:
    wall = bottles.straight_wall(bottles.read_glb(bottles.bottle_path(volume, KIT)))
    diameter = KIT_DIAMETERS_MM[volume] / 1000
    assert wall.radius_m == pytest.approx(diameter / 2, abs=1e-5)
    # The heel is rounded at an eighth of the diameter, and the wall starts there.
    assert wall.bottom_m == pytest.approx(0.125 * diameter, abs=1e-4)
    assert wall.top_m > wall.bottom_m + 0.04


@pytest.mark.parametrize("entry", one_entry_per_size(), ids=vessel_class)
def test_label_goes_on_the_bottle_of_its_own_size(entry: registry.Entry) -> None:
    """A 2 L barcode must never land on a 100 ml bottle."""
    labelled, _ = bottles.labelled_bottle(entry, KIT)
    bottle_bounds = labelled.document["accessors"][0]["max"]
    expected = KIT_DIAMETERS_MM[entry.sample.container_ml] / 2000
    assert bottle_bounds[0] == pytest.approx(expected, abs=1e-5)

    extras = labelled.document["nodes"][-1]["extras"]
    assert extras["code"] == entry.code
    assert extras["container_ml"] == entry.sample.container_ml
    assert extras["vessel_class"] == f"bottle_{entry.sample.container_ml:g}ml"


@pytest.mark.parametrize("entry", one_entry_per_size(), ids=vessel_class)
def test_label_sits_on_the_straight_wall(entry: registry.Entry) -> None:
    bottle = bottles.read_glb(bottles.bottle_path(entry.sample.container_ml, KIT))
    wall = bottles.straight_wall(bottle)
    _, patch = bottles.labelled_bottle(entry, KIT)

    radii = np.hypot(patch.positions[:, 0], patch.positions[:, 2])
    assert radii == pytest.approx(wall.radius_m + bottles.LABEL_OFFSET_M, abs=1e-6)
    assert patch.positions[:, 1].min() >= wall.bottom_m + bottles.WALL_MARGIN_M - 1e-6
    assert patch.positions[:, 1].max() <= wall.top_m - bottles.WALL_MARGIN_M + 1e-6
    assert patch.arc_deg <= bottles.MAX_ARC_DEG + 1e-6
    assert patch.module_m <= bottles.NOMINAL_MODULE_M * bottles.MAX_MAGNIFICATION + 1e-9
    # The label faces +Z and its normals point away from the bottle's axis.
    assert patch.positions[:, 2].min() > 0
    assert np.einsum("ij,ij->i", patch.normals, patch.positions).min() > 0


def test_bigger_bottles_get_bigger_labels() -> None:
    widths = [bottles.labelled_bottle(e, KIT)[1].width_m for e in one_entry_per_size()]
    assert widths == sorted(widths)
    assert widths[0] < widths[-1]


def test_label_triangles_face_outwards() -> None:
    patch = bottles.label_patch(bottles.Wall(0.044, 0.011, 0.136), 121, 59)
    a, b, c = (patch.positions[patch.indices.reshape(-1, 3)[:, i]] for i in range(3))
    face_normals = np.cross(b - a, c - a)
    assert np.einsum("ij,ij->i", face_normals, a).min() > 0


def test_label_corners_run_clockwise_from_top_left() -> None:
    patch = bottles.label_patch(bottles.Wall(0.044, 0.011, 0.136), 121, 59)
    top_left, top_right, bottom_right, bottom_left = np.array(patch.corners_m)
    assert top_left[0] < 0 < top_right[0]
    assert top_left[1] > bottom_left[1]
    assert bottom_right[0] == pytest.approx(top_right[0])


def test_labelling_leaves_the_bottle_mesh_untouched() -> None:
    entry = powder_entries()[0]
    bottle = bottles.read_glb(bottles.bottle_path(entry.sample.container_ml, KIT))
    labelled, _ = bottles.labelled_bottle(entry, KIT)
    assert labelled.buffer[: len(bottle.buffer)] == bottle.buffer
    assert labelled.document["meshes"][0] == bottle.document["meshes"][0]
    assert len(labelled.document["meshes"]) == 2
    assert labelled.document["nodes"][0]["children"] == [1]


def test_labelled_bottle_roundtrips_through_disk(tmp_path: Path) -> None:
    entry = powder_entries()[0]
    paths = bottles.write_labelled_bottles([entry], KIT, tmp_path)
    assert [p.name for p in paths] == [f"{entry.sample.sample_id}_{entry.code}.glb"]

    loaded = bottles.read_glb(paths[0])
    assert len(paths[0].read_bytes()) % 4 == 0
    label = loaded.document["meshes"][-1]["primitives"][0]
    assert set(label["attributes"]) == {"POSITION", "NORMAL", "TEXCOORD_0"}
    uvs = accessor_array(loaded, label["attributes"]["TEXCOORD_0"], 2, "<f4")
    assert uvs.min() == 0.0 and uvs.max() == 1.0
    for view in loaded.document["bufferViews"]:
        assert view["byteOffset"] % 4 == 0
        assert view["byteOffset"] + view["byteLength"] <= len(loaded.buffer)


def test_liquids_are_skipped_and_refused() -> None:
    liquid = registry.build_registry(registry.default_samples(1))[0]
    with pytest.raises(bottles.BottleError, match="only powders"):
        bottles.labelled_bottle(liquid, KIT)


def test_write_labelled_bottles_skips_liquid_rows(tmp_path: Path) -> None:
    liquid = registry.build_registry(registry.default_samples(1))
    assert bottles.write_labelled_bottles(liquid, KIT, tmp_path) == []


def test_read_glb_reports_a_missing_file(tmp_path: Path) -> None:
    with pytest.raises(bottles.BottleError, match="not found"):
        bottles.read_glb(tmp_path / "absent.glb")


def test_read_glb_rejects_a_file_that_is_not_glb(tmp_path: Path) -> None:
    path = tmp_path / "bad.glb"
    path.write_bytes(b"this is not a binary glTF file at all, just some text")
    with pytest.raises(bottles.BottleError):
        bottles.read_glb(path)


@pytest.mark.parametrize("entry", one_entry_per_size(), ids=vessel_class)
def test_embedded_label_decodes_flat_and_wrapped(entry: registry.Entry) -> None:
    """The texture on the bottle must read back as that sample's own code.

    Checked twice: flat, as embedded, and squeezed the way a camera facing the
    bottle sees it, which is what MAX_ARC_DEG exists to keep readable.
    """
    labelled, patch = bottles.labelled_bottle(entry, KIT)
    flat = label_image(labelled)
    assert {d.code for d in reader.decode_image(flat)} == {entry.code}

    wrapped = seen_on_cylinder(flat, patch.arc_deg)
    assert wrapped.shape[1] < flat.shape[1]
    assert {d.code for d in reader.decode_image(wrapped)} == {entry.code}
