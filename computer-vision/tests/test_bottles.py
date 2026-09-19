"""Tests for sticking sample labels onto the bottle kits."""

import math
from pathlib import Path

import cv2
import numpy as np
import pytest

from labvision import bottles, reader, registry

ASSETS = Path(__file__).parents[2] / "assets"

# Body diameter of each bottle in millimetres, from each kit's README.
DIAMETERS_MM = {
    "powder": {100.0: 46, 250.0: 60, 500.0: 74, 1000.0: 88, 2000.0: 116},
    "liquid": {10.0: 22, 20.0: 28, 30.0: 32, 50.0: 38, 100.0: 47},
}

# The label image is 484 x 236 px at 4 px per module.
LABEL_ASPECT = 484 / 236


def entries_of(phase: str) -> list[registry.Entry]:
    entries = registry.build_registry(registry.default_samples())
    return [e for e in entries if e.sample.phase == phase]


def one_entry_per_size() -> list[registry.Entry]:
    """The first liquid compound, in each of its five flask sizes."""
    return entries_of("liquid")[:5]


def a_powder_entry() -> registry.Entry:
    """A powder entry built by hand.

    Powder is no longer in the catalogue (registry v6), but the bottle kit and
    the labelling code still support it, so the code paths only a powder bottle
    exercises are tested with a hand-made entry rather than a catalogue row.
    """
    sample = registry.Sample("PWD-0001", "Vanillin", "121-33-5", "powder", 100.0, "L1")
    return registry.build_registry([sample])[0]


def vessel_class(entry: registry.Entry) -> str:
    return entry.sample.vessel_class


def bottle_mesh_radius(glb: bottles.Glb) -> float:
    document = glb.document
    mesh = document["meshes"][document["nodes"][bottles.bottle_node(glb)]["mesh"]]
    bounds = document["accessors"][mesh["primitives"][0]["attributes"]["POSITION"]]
    return bounds["max"][0]


def accessor_array(glb: bottles.Glb, index: int, width: int, dtype: str) -> np.ndarray:
    accessor = glb.document["accessors"][index]
    view = glb.document["bufferViews"][accessor["bufferView"]]
    return np.frombuffer(
        glb.buffer,
        dtype=dtype,
        count=accessor["count"] * width,
        offset=view.get("byteOffset", 0),
    ).reshape(-1, width)


def label_image(glb: bottles.Glb) -> np.ndarray:
    view = glb.document["bufferViews"][glb.document["images"][-1]["bufferView"]]
    png = glb.buffer[view["byteOffset"] : view["byteOffset"] + view["byteLength"]]
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


def test_every_catalogue_size_has_a_bottle_in_its_kit() -> None:
    assert {spec.name for spec in registry.PHASES} <= set(bottles.KITS)
    for spec in registry.PHASES:
        kit = bottles.KITS[spec.name]
        assert set(kit.files) == set(spec.containers_ml), spec.name
        for name in kit.files.values():
            assert (ASSETS / kit.directory / "glb" / name).exists(), name


def test_bottle_path_rejects_a_size_the_kit_lacks() -> None:
    sample = registry.Sample("PWD-1", "Vanillin", "121-33-5", "powder", 50.0, "L1")
    with pytest.raises(bottles.BottleError, match="no 50 ml bottle"):
        bottles.bottle_path(sample, ASSETS)


def test_bottle_path_rejects_a_phase_without_a_kit() -> None:
    sample = registry.Sample("X-1", "M", "C", "plasma", 50.0, "L1")
    with pytest.raises(bottles.BottleError, match="no kit holds plasma"):
        bottles.bottle_path(sample, ASSETS)


def test_the_same_size_means_a_different_bottle_in_each_phase() -> None:
    """100 ml is in both series; the phase decides which bottle it is."""
    liquid = registry.Sample("SMP-1", "Limonene", "5989-27-5", "liquid", 100.0, "L1")
    powder = registry.Sample("PWD-1", "Vanillin", "121-33-5", "powder", 100.0, "L1")
    assert bottles.bottle_path(liquid, ASSETS).parts[-3] == "amber-bottles"
    assert bottles.bottle_path(powder, ASSETS).parts[-3] == "agrochemical-bottles"


def test_bottle_node_picks_the_bottle_not_its_cap() -> None:
    """The amber files list the cap first; measuring it finds no wall at all."""
    sample = entries_of("liquid")[0].sample
    glb = bottles.read_glb(bottles.bottle_path(sample, ASSETS))
    node = glb.document["nodes"][bottles.bottle_node(glb)]
    assert node["name"].startswith("Bottle_")
    assert glb.document["nodes"][0]["name"].startswith("Cap_")


@pytest.mark.parametrize("entry", one_entry_per_size(), ids=vessel_class)
def test_straight_wall_matches_the_kit_dimensions(entry: registry.Entry) -> None:
    sample = entry.sample
    wall = bottles.straight_wall(bottles.read_glb(bottles.bottle_path(sample, ASSETS)))
    diameter = DIAMETERS_MM[sample.phase][sample.container_ml] / 1000
    # The READMEs round to the millimetre.
    assert wall.radius_m == pytest.approx(diameter / 2, abs=3e-4)
    assert 0 < wall.bottom_m < 0.02
    assert wall.top_m > wall.bottom_m + 0.03


@pytest.mark.parametrize("entry", one_entry_per_size(), ids=vessel_class)
def test_label_goes_on_the_bottle_of_its_own_size(entry: registry.Entry) -> None:
    """A 2 L barcode must never land on a 100 ml bottle, nor on an amber one."""
    sample = entry.sample
    labelled, _ = bottles.labelled_bottle(entry, ASSETS)
    expected = DIAMETERS_MM[sample.phase][sample.container_ml] / 2000
    assert bottle_mesh_radius(labelled) == pytest.approx(expected, abs=3e-4)

    extras = labelled.document["nodes"][-1]["extras"]
    assert extras["code"] == entry.code
    assert extras["container_ml"] == sample.container_ml
    assert extras["vessel_class"] == sample.vessel_class


@pytest.mark.parametrize("entry", one_entry_per_size(), ids=vessel_class)
def test_label_sits_on_the_straight_wall(entry: registry.Entry) -> None:
    bottle = bottles.read_glb(bottles.bottle_path(entry.sample, ASSETS))
    wall = bottles.straight_wall(bottle)
    _, patch = bottles.labelled_bottle(entry, ASSETS, "ean13")

    radii = np.hypot(patch.positions[:, 0], patch.positions[:, 2])
    assert radii == pytest.approx(wall.radius_m + bottles.LABEL_OFFSET_M, abs=1e-6)
    assert patch.positions[:, 1].min() >= wall.bottom_m + bottles.WALL_MARGIN_M - 1e-6
    assert patch.positions[:, 1].max() <= wall.top_m - bottles.WALL_MARGIN_M + 1e-6
    assert patch.arc_deg <= bottles.MAX_ARC_DEG + 1e-6
    assert patch.module_m <= bottles.NOMINAL_MODULE_M * bottles.MAX_MAGNIFICATION + 1e-9
    # The label faces +Z and its normals point away from the bottle's axis.
    assert patch.positions[:, 2].min() > 0
    assert np.einsum("ij,ij->i", patch.normals, patch.positions).min() > 0


@pytest.mark.parametrize("phase", [spec.name for spec in registry.PHASES])
def test_bigger_bottles_get_bigger_labels(phase: str) -> None:
    patches = [
        bottles.labelled_bottle(e, ASSETS, "ean13")[1] for e in entries_of(phase)[:5]
    ]
    modules = [patch.module_m for patch in patches]
    assert modules == sorted(modules)
    assert modules[0] < modules[-1]


@pytest.mark.parametrize("entry", one_entry_per_size(), ids=vessel_class)
def test_label_is_turned_so_its_width_runs_up_the_bottle(
    entry: registry.Entry,
) -> None:
    """Ladder orientation: the long side of the label is vertical."""
    _, patch = bottles.labelled_bottle(entry, ASSETS, "ean13")
    assert patch.height_m > patch.width_m
    assert patch.height_m / patch.width_m == pytest.approx(LABEL_ASPECT, rel=1e-6)


def test_liquid_labels_are_as_large_as_their_short_bottles_allow() -> None:
    """Every liquid label is bound by wall height, so it fills the wall."""
    for entry in entries_of("liquid")[:5]:
        bottle = bottles.read_glb(bottles.bottle_path(entry.sample, ASSETS))
        wall = bottles.straight_wall(bottle)
        _, patch = bottles.labelled_bottle(entry, ASSETS, "ean13")
        room = wall.top_m - wall.bottom_m - 2 * bottles.WALL_MARGIN_M
        assert patch.height_m == pytest.approx(room, abs=1e-6), entry.sample.sample_id
    # The 10 ml bottle is 52 mm tall, and its label is still over half size.
    smallest = bottles.labelled_bottle(entries_of("liquid")[0], ASSETS, "ean13")[1]
    assert smallest.module_m / bottles.NOMINAL_MODULE_M > 0.6


def test_label_triangles_face_outwards() -> None:
    patch = bottles.label_patch(bottles.Wall(0.044, 0.011, 0.136), 121, 59)
    a, b, c = (patch.positions[patch.indices.reshape(-1, 3)[:, i]] for i in range(3))
    face_normals = np.cross(b - a, c - a)
    assert np.einsum("ij,ij->i", face_normals, a).min() > 0


def test_label_corners_are_named_in_the_labels_own_frame() -> None:
    """The label is turned anticlockwise, so its top edge runs up the left side."""
    patch = bottles.label_patch(bottles.Wall(0.044, 0.011, 0.136), 121, 59)
    top_left, top_right, bottom_right, bottom_left = np.array(patch.corners_m)
    assert top_left[0] == pytest.approx(top_right[0]) and top_left[0] < 0
    assert bottom_left[0] == pytest.approx(bottom_right[0]) and bottom_left[0] > 0
    assert top_right[1] > top_left[1]
    assert bottom_right[1] > bottom_left[1]


def test_texture_is_turned_by_its_uvs_not_by_its_pixels() -> None:
    patch = bottles.label_patch(bottles.Wall(0.044, 0.011, 0.136), 121, 59)
    low = patch.positions[:, 1] == patch.positions[:, 1].min()
    leftmost = patch.positions[:, 0] == patch.positions[:, 0].min()
    # The label's left edge (u = 0) lies along the bottom of the sticker, and its
    # top edge (v = 0) runs up the sticker's left side.
    assert np.all(patch.uvs[low, 0] == 0.0)
    assert np.all(patch.uvs[leftmost, 1] == 0.0)


@pytest.mark.parametrize("phase", [spec.name for spec in registry.PHASES])
def test_labelling_leaves_the_bottle_untouched(phase: str) -> None:
    entry = entries_of(phase)[0]
    bottle = bottles.read_glb(bottles.bottle_path(entry.sample, ASSETS))
    labelled, _ = bottles.labelled_bottle(entry, ASSETS)
    assert labelled.buffer[: len(bottle.buffer)] == bottle.buffer
    assert labelled.document["meshes"][:-1] == bottle.document["meshes"]
    assert (
        labelled.document["materials"][: len(bottle.document["materials"])]
        == (bottle.document["materials"])
    )
    label_node = len(labelled.document["nodes"]) - 1
    parent = labelled.document["nodes"][bottles.bottle_node(labelled)]
    assert label_node in parent["children"]


def test_only_a_see_through_bottle_gets_a_white_back_on_its_label() -> None:
    """Through glass a one-sided label vanishes and a two-sided one reads mirrored."""
    powder, _ = bottles.labelled_bottle(a_powder_entry(), ASSETS)
    liquid, patch = bottles.labelled_bottle(entries_of("liquid")[0], ASSETS)
    assert len(powder.document["meshes"][-1]["primitives"]) == 1

    front, back = liquid.document["meshes"][-1]["primitives"]
    assert "TEXCOORD_0" in front["attributes"]
    assert "TEXCOORD_0" not in back["attributes"]
    material = liquid.document["materials"][back["material"]]
    assert "baseColorTexture" not in material["pbrMetallicRoughness"]

    points = accessor_array(liquid, back["attributes"]["POSITION"], 3, "<f4")
    normals = accessor_array(liquid, back["attributes"]["NORMAL"], 3, "<f4")
    # Between the glass and the printed face, and facing the bottle's axis.
    radii = np.hypot(points[:, 0], points[:, 2])
    printed = np.hypot(patch.positions[:, 0], patch.positions[:, 2])
    assert radii.max() < printed.min()
    assert np.einsum("ij,ij->i", normals, points).max() < 0


def test_labelled_bottle_roundtrips_through_disk(tmp_path: Path) -> None:
    entry = entries_of("liquid")[0]
    paths = bottles.write_labelled_bottles([entry], ASSETS, tmp_path)
    assert [p.name for p in paths] == [f"{entry.sample.sample_id}_{entry.code}.glb"]
    assert paths[0].parent == tmp_path

    loaded = bottles.read_glb(paths[0])
    assert len(paths[0].read_bytes()) % 4 == 0
    label = loaded.document["meshes"][-1]["primitives"][0]
    assert set(label["attributes"]) == {"POSITION", "NORMAL", "TEXCOORD_0"}
    uvs = accessor_array(loaded, label["attributes"]["TEXCOORD_0"], 2, "<f4")
    assert uvs.min() == 0.0 and uvs.max() == 1.0
    for view in loaded.document["bufferViews"]:
        assert view["byteOffset"] % 4 == 0
        assert view["byteOffset"] + view["byteLength"] <= len(loaded.buffer)


def test_each_labelled_bottle_is_kept_in_its_own_kit() -> None:
    liquid, powder = entries_of("liquid")[0], a_powder_entry()
    assert bottles.labelled_path(liquid, ASSETS).parent == (
        ASSETS / "amber-bottles" / "labelled"
    )
    assert bottles.labelled_path(powder, ASSETS).parent == (
        ASSETS / "agrochemical-bottles" / "labelled"
    )


@pytest.mark.parametrize("phase", [spec.name for spec in registry.PHASES])
def test_committed_labelled_bottles_are_not_stale(phase: str) -> None:
    """The GLBs in the repo must be the ones the current catalogue produces.

    A changed barcode changes a file name, and a changed label or bottle changes
    file contents, so both are compared. Regenerate with
    ``python -m labvision.bottles`` when this fails.
    """
    entries = entries_of(phase)
    folder = bottles.labelled_path(entries[0], ASSETS).parent
    committed = {p.name for p in folder.glob("*.glb")}
    assert committed == {bottles.labelled_path(e, ASSETS).name for e in entries}
    # Every sixth row walks through all five sizes.
    for entry in entries[::6]:
        fresh, _ = bottles.labelled_bottle(entry, ASSETS)
        on_disk = bottles.read_glb(bottles.labelled_path(entry, ASSETS))
        assert on_disk.document == fresh.document, entry.sample.sample_id
        assert on_disk.buffer == fresh.buffer, entry.sample.sample_id


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

    Checked twice: flat, as embedded, and as a camera facing the bottle sees it,
    turned a quarter turn and squeezed round the cylinder.
    """
    labelled, patch = bottles.labelled_bottle(entry, ASSETS, "ean13")
    flat = label_image(labelled)
    assert flat.shape[1] > flat.shape[0]
    assert {d.code for d in reader.decode_image(flat)} == {entry.code}

    on_bottle = cv2.rotate(flat, cv2.ROTATE_90_COUNTERCLOCKWISE)
    wrapped = seen_on_cylinder(on_bottle, patch.arc_deg)
    assert wrapped.shape[1] < on_bottle.shape[1]
    assert {d.code for d in reader.decode_image(wrapped)} == {entry.code}


@pytest.mark.parametrize("arc_deg", [60, 90, 120])
def test_ladder_labels_survive_far_more_wrap_than_upright_ones(arc_deg: int) -> None:
    """Curvature squeezes bar lengths, not widths, once the label is turned."""
    entry = entries_of("liquid")[4]  # 100 ml, the widest liquid bottle
    flat = label_image(bottles.labelled_bottle(entry, ASSETS, "ean13")[0])
    on_bottle = cv2.rotate(flat, cv2.ROTATE_90_COUNTERCLOCKWISE)
    wrapped = seen_on_cylinder(on_bottle, arc_deg)
    assert {d.code for d in reader.decode_image(wrapped)} == {entry.code}


# --- The ArUco ring, which is what the kits are built with ---------------------


def test_the_ring_is_the_label_the_kits_are_built_with() -> None:
    assert bottles.LABELS[0] == "aruco_ring"
    labelled, patch = bottles.labelled_bottle(one_entry_per_size()[0], ASSETS)
    node = next(
        n for n in labelled.document["nodes"] if n.get("name", "").startswith("Label_")
    )
    assert node["extras"]["label"] == "aruco_ring"
    assert patch.arc_deg == 360.0


def test_an_unknown_label_is_rejected() -> None:
    with pytest.raises(bottles.BottleError, match="no such label"):
        bottles.labelled_bottle(one_entry_per_size()[0], ASSETS, "qr")


@pytest.mark.parametrize(
    "entry", one_entry_per_size(), ids=lambda e: e.sample.vessel_class
)
def test_ring_goes_all_the_way_round_the_straight_wall(entry: registry.Entry) -> None:
    wall = bottles.straight_wall(
        bottles.read_glb(bottles.bottle_path(entry.sample, ASSETS))
    )
    _, patch = bottles.labelled_bottle(entry, ASSETS)
    radii = np.hypot(patch.positions[:, 0], patch.positions[:, 2])
    assert radii == pytest.approx(wall.radius_m + bottles.LABEL_OFFSET_M, abs=1e-6)
    assert patch.positions[:, 1].min() >= wall.bottom_m + bottles.WALL_MARGIN_M - 1e-6
    assert patch.positions[:, 1].max() <= wall.top_m - bottles.WALL_MARGIN_M + 1e-6
    angles = np.degrees(np.arctan2(patch.positions[:, 0], patch.positions[:, 2]))
    assert angles.min() == pytest.approx(-180.0, abs=1e-3)
    assert angles.max() == pytest.approx(180.0, abs=1e-3)


@pytest.mark.parametrize(
    "entry", one_entry_per_size(), ids=lambda e: e.sample.vessel_class
)
def test_ring_cells_are_square_so_the_markers_are(entry: registry.Entry) -> None:
    _, patch = bottles.labelled_bottle(entry, ASSETS)
    assert patch.width_m / bottles.RING_COPIES == pytest.approx(
        patch.height_m, rel=1e-6
    )
    cell = bottles.ARUCO_MARKER_MODULES + 2 * bottles.ARUCO_QUIET_MODULES
    assert patch.module_m * cell == pytest.approx(patch.height_m, rel=1e-6)


def test_ring_modules_are_several_times_the_barcodes() -> None:
    """The point of the ring: a module a camera can resolve from arm's length"""
    for entry in one_entry_per_size():
        _, ring = bottles.labelled_bottle(entry, ASSETS)
        _, barcode = bottles.labelled_bottle(entry, ASSETS, "ean13")
        assert ring.module_m > 4 * barcode.module_m


def test_ring_texture_reads_back_as_the_samples_marker() -> None:
    detector = cv2.aruco.ArucoDetector(
        cv2.aruco.getPredefinedDictionary(bottles.ARUCO_DICTIONARY),
        cv2.aruco.DetectorParameters(),
    )
    for entry in one_entry_per_size():
        labelled, _ = bottles.labelled_bottle(entry, ASSETS)
        strip = label_image(labelled)
        _, ids, _ = detector.detectMarkers(strip)
        # The strip is rolled by half a cell, so one copy is split across the seam.
        assert ids is not None and len(ids) == bottles.RING_COPIES - 1
        assert set(ids.flatten().tolist()) == {entry.marker_id}


def test_a_marker_not_a_seam_faces_the_front() -> None:
    strip = bottles.render_ring(7)
    cell = strip.shape[1] // bottles.RING_COPIES
    middle = strip[:, strip.shape[1] // 2 - cell // 2 : strip.shape[1] // 2 + cell // 2]
    detector = cv2.aruco.ArucoDetector(
        cv2.aruco.getPredefinedDictionary(bottles.ARUCO_DICTIONARY),
        cv2.aruco.DetectorParameters(),
    )
    _, ids, _ = detector.detectMarkers(
        cv2.copyMakeBorder(middle, 40, 40, 40, 40, cv2.BORDER_CONSTANT, value=255)
    )
    assert ids is not None and ids.flatten().tolist() == [7]


def test_render_ring_rejects_an_id_outside_the_dictionary() -> None:
    with pytest.raises(bottles.BottleError, match="no id"):
        bottles.render_ring(250)
