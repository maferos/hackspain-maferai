"""Tests for the room, the bounding-box anchors and the forward-model fit.

The heart of this file is a synthetic oracle: :func:`~labvision.scene.predict_bbox`
gives the exact box a cylinder would produce, so every anchor can be scored
against ground truth it cannot see. That is what pins the accuracy claims in
the README, and what would catch a sign flip in the radius correction.
"""

import math

import numpy as np
import pytest

from labvision import scene
from labvision.camera import Camera, GeometryError, Plane

GRID = [(x, y) for x in np.linspace(6.2, 7.8, 5) for y in np.linspace(1.7, 3.3, 5)]


@pytest.fixture
def camera() -> Camera:
    return scene.default_camera()


@pytest.fixture
def bench() -> Plane:
    return scene.table_plane()


def _truth(x: float, y: float) -> np.ndarray:
    return np.array([x, y, scene.TABLE_TOP_Z])


def _errors_mm(camera: Camera, vessel: scene.Vessel, anchor: str) -> np.ndarray:
    errors = []
    for x, y in GRID:
        box = scene.predict_bbox(
            camera, _truth(x, y),
            radius=vessel.radius_m, height=vessel.silhouette_height_m(),
        )
        placed = scene.locate(box, camera, vessel=vessel, anchor=anchor)
        errors.append(np.linalg.norm(placed.position - _truth(x, y)) * 1000.0)
    return np.array(errors)


# --- the room --------------------------------------------------------------


def test_the_bench_centre_is_where_the_camera_looks(camera: Camera) -> None:
    pixel = camera.project(np.array([*scene.TABLE_CENTRE, scene.TABLE_TOP_Z]))
    assert pixel == pytest.approx((camera.intrinsics.cx, camera.intrinsics.cy))


def test_the_line_of_sight_is_three_metres_at_forty_degrees(camera: Camera) -> None:
    centre = np.array([*scene.TABLE_CENTRE, scene.TABLE_TOP_Z])
    assert float(camera.range_to(centre)) == pytest.approx(3.233, abs=1e-3)
    assert scene._elevation_deg(camera, centre) == pytest.approx(39.4, abs=0.1)


def test_the_frame_overshoots_the_far_wall(camera: Camera, bench: Plane) -> None:
    """Worth knowing before anyone trusts the top of the image: it is wall."""
    from labvision.camera import plane_footprint

    corners = plane_footprint(camera, bench)
    assert corners[:2, 1].min() > scene.ROOM_SIZE[1]
    assert corners[2:, 1].max() < scene.ROOM_SIZE[1]


# --- boxes -----------------------------------------------------------------


def test_bbox_geometry() -> None:
    box = scene.BBox.from_xywh(100.0, 200.0, 40.0, 80.0)
    assert box.as_tuple() == (100.0, 200.0, 140.0, 280.0)
    assert (box.width, box.height) == (40.0, 80.0)
    assert box.centre == (120.0, 240.0)
    assert box.bottom_centre == (120.0, 280.0)


def test_bbox_rejects_an_empty_box() -> None:
    with pytest.raises(GeometryError):
        scene.BBox(10.0, 10.0, 10.0, 20.0)


def test_bbox_around_ignores_points_that_have_no_image() -> None:
    box = scene.BBox.around([[10.0, 20.0], [np.nan, np.nan], [30.0, 50.0]])
    assert box.as_tuple() == (10.0, 20.0, 30.0, 50.0)


def test_bbox_around_needs_a_finite_point() -> None:
    with pytest.raises(GeometryError):
        scene.BBox.around([[np.nan, np.nan]])


def test_touches_frame_catches_a_clipped_box(camera: Camera) -> None:
    assert scene.BBox(0.0, 100.0, 50.0, 200.0).touches_frame(camera.intrinsics)
    assert not scene.BBox(100.0, 100.0, 150.0, 200.0).touches_frame(camera.intrinsics)


# --- vessels ---------------------------------------------------------------


def test_the_vessel_table_is_in_metres() -> None:
    for vessel in scene.VESSELS.values():
        assert 0.02 < vessel.diameter_m < 0.2
        assert 0.05 < vessel.height_m < 0.4
        assert vessel.radius_m == vessel.diameter_m / 2.0


def test_a_cap_adds_its_height_less_the_overlap() -> None:
    bottle = scene.VESSELS["bottle_1000ml"]
    assert bottle.silhouette_height_m(capped=False) == pytest.approx(0.216)
    assert bottle.silhouette_height_m() == pytest.approx(0.216 + 0.027 - 0.001)


# --- the fit ---------------------------------------------------------------


def test_the_fit_inverts_the_forward_model_exactly(camera: Camera) -> None:
    for vessel in scene.VESSELS.values():
        assert _errors_mm(camera, vessel, "fit").max() < 0.01


def test_the_fit_is_the_default_when_dimensions_are_known(camera: Camera) -> None:
    vessel = scene.VESSELS["bottle_1000ml"]
    box = scene.predict_bbox(camera, _truth(6.4, 2.9), radius=vessel.radius_m,
                             height=vessel.silhouette_height_m())
    assert scene.locate(box, camera, vessel=vessel).residual_px is not None
    assert scene.locate(box, camera).residual_px is None


def test_the_fit_reports_its_residual(camera: Camera) -> None:
    vessel = scene.VESSELS["bottle_500ml"]
    box = scene.predict_bbox(camera, _truth(7.1, 2.2), radius=vessel.radius_m,
                             height=vessel.silhouette_height_m())
    assert scene.locate(box, camera, vessel=vessel).residual_px < 1e-6


def test_a_box_that_is_not_this_vessel_leaves_a_residual(camera: Camera) -> None:
    """The residual is the only thing that notices a mislabelled detection."""
    vessel = scene.VESSELS["bottle_2000ml"]
    box = scene.predict_bbox(camera, _truth(7.0, 2.5), radius=vessel.radius_m,
                             height=vessel.silhouette_height_m())
    wrong = scene.locate(box, camera, vessel=scene.VESSELS["bottle_100ml"])
    assert wrong.residual_px > 10.0


def test_the_fit_needs_dimensions(camera: Camera) -> None:
    with pytest.raises(GeometryError, match="radius and a height"):
        scene.locate(scene.BBox(300.0, 200.0, 340.0, 280.0), camera, anchor="fit")


# --- the anchors -----------------------------------------------------------


def test_the_radius_correction_moves_the_hit_away_from_the_camera(
    camera: Camera,
) -> None:
    vessel = scene.VESSELS["bottle_2000ml"]
    box = scene.predict_bbox(camera, _truth(7.0, 2.5), radius=vessel.radius_m,
                             height=vessel.silhouette_height_m())
    placed = scene.locate(box, camera, vessel=vessel, anchor="base")
    correction = placed.position - placed.raw_hit
    assert np.linalg.norm(correction) == pytest.approx(vessel.radius_m, abs=1e-9)
    assert float(camera.range_to(placed.position)) > float(
        camera.range_to(placed.raw_hit)
    )


def test_without_the_correction_the_base_anchor_is_short_by_a_radius(
    camera: Camera, bench: Plane,
) -> None:
    vessel = scene.VESSELS["bottle_1000ml"]
    for x, y in GRID:
        box = scene.predict_bbox(camera, _truth(x, y), radius=vessel.radius_m,
                                 height=vessel.silhouette_height_m())
        uncorrected = scene.locate(box, camera, radius=0.0, anchor="base")
        bias = np.linalg.norm(uncorrected.position - _truth(x, y))
        assert bias == pytest.approx(vessel.radius_m, rel=0.25)


def test_the_correction_beats_no_correction_by_a_factor_of_five(
    camera: Camera,
) -> None:
    vessel = scene.VESSELS["bottle_1000ml"]
    corrected = _errors_mm(camera, vessel, "base").mean()
    uncorrected = np.mean([
        np.linalg.norm(
            scene.locate(
                scene.predict_bbox(camera, _truth(x, y), radius=vessel.radius_m,
                                   height=vessel.silhouette_height_m()),
                camera, radius=0.0, anchor="base",
            ).position - _truth(x, y)
        ) * 1000.0
        for x, y in GRID
    ])
    assert uncorrected > 5.0 * corrected


def test_the_anchors_rank_as_the_readme_says(camera: Camera) -> None:
    """The fit is exact; the centre anchor beats the base anchor on exact boxes."""
    vessel = scene.VESSELS["bottle_1000ml"]
    fitted = _errors_mm(camera, vessel, "fit").mean()
    centred = _errors_mm(camera, vessel, "centre").mean()
    based = _errors_mm(camera, vessel, "base").mean()
    assert fitted < centred < based
    assert centred < 5.0
    assert based < 20.0


def test_the_centre_anchor_needs_a_height(camera: Camera) -> None:
    with pytest.raises(GeometryError, match="height"):
        scene.locate(scene.BBox(300.0, 200.0, 340.0, 280.0), camera,
                     anchor="centre")


def test_an_unknown_anchor_is_refused(camera: Camera) -> None:
    with pytest.raises(GeometryError, match="anchor"):
        scene.locate(scene.BBox(300.0, 200.0, 340.0, 280.0), camera, anchor="top")


# --- what comes out --------------------------------------------------------


def test_the_mouth_sits_a_vessel_height_above_the_base(camera: Camera) -> None:
    vessel = scene.VESSELS["bottle_250ml"]
    box = scene.predict_bbox(camera, _truth(7.2, 2.1), radius=vessel.radius_m,
                             height=vessel.silhouette_height_m())
    placed = scene.locate(box, camera, vessel=vessel)
    assert placed.mouth[2] - placed.position[2] == pytest.approx(
        vessel.silhouette_height_m()
    )


def test_a_vessel_standing_on_the_bench_is_inside_the_room(camera: Camera) -> None:
    vessel = scene.VESSELS["bottle_1000ml"]
    box = scene.predict_bbox(camera, _truth(7.0, 2.5), radius=vessel.radius_m,
                             height=vessel.silhouette_height_m())
    assert scene.locate(box, camera, vessel=vessel).inside_room


def test_the_on_table_check_waits_for_a_measured_footprint(
    camera: Camera,
) -> None:
    vessel = scene.VESSELS["bottle_1000ml"]
    box = scene.predict_bbox(camera, _truth(7.6, 3.1), radius=vessel.radius_m,
                             height=vessel.silhouette_height_m())
    assert scene.locate(box, camera, vessel=vessel).on_table is None
    off = scene.locate(box, camera, vessel=vessel, table_size=(0.5, 0.5))
    assert off.on_table is False
    on = scene.locate(box, camera, vessel=vessel, table_size=(2.0, 2.0))
    assert on.on_table is True


def test_a_box_above_the_horizon_is_not_standing_on_the_bench(
    camera: Camera,
) -> None:
    with pytest.raises(GeometryError, match="horizon"):
        scene.locate(scene.BBox(300.0, -400.0, 340.0, -300.0), camera)


# --- noise -----------------------------------------------------------------


def test_one_pixel_of_box_noise_costs_about_a_centimetre(camera: Camera) -> None:
    """The headline number: at this range and resolution, a pixel is ~9 mm."""
    vessel = scene.VESSELS["bottle_1000ml"]
    rng = np.random.default_rng(42)
    errors = []
    for x, y in GRID:
        clean = scene.predict_bbox(camera, _truth(x, y), radius=vessel.radius_m,
                                   height=vessel.silhouette_height_m())
        for _ in range(8):
            jitter = rng.normal(0.0, 1.0, 4)
            noisy = scene.BBox(*(np.array(clean.as_tuple()) + jitter))
            placed = scene.locate(noisy, camera, vessel=vessel)
            errors.append(np.linalg.norm(placed.position - _truth(x, y)))
    assert 0.003 < np.mean(errors) < 0.015


def test_the_error_budget_gets_worse_with_distance(camera: Camera) -> None:
    rows = scene.error_budget(camera, extent=1.0, steps=3)
    near = min(rows, key=lambda row: row[1])
    far = max(rows, key=lambda row: row[1])
    assert far[2] > 2.0 * near[2]


def test_the_quoted_scale_is_a_real_derivative(camera: Camera) -> None:
    """A pixel of jitter really does move the answer by metres_per_pixel."""
    vessel = scene.VESSELS["bottle_500ml"]
    box = scene.predict_bbox(camera, _truth(7.0, 2.5), radius=vessel.radius_m,
                             height=vessel.silhouette_height_m())
    placed = scene.locate(box, camera, vessel=vessel, anchor="base")
    nudged = scene.locate(
        scene.BBox(box.u_min, box.v_min, box.u_max, box.v_max + 1.0),
        camera, vessel=vessel, anchor="base",
    )
    moved = float(np.linalg.norm(nudged.position - placed.position))
    assert moved == pytest.approx(placed.metres_per_pixel, rel=0.05)


# --- the command line ------------------------------------------------------


def test_the_cli_reports_a_position(capsys: pytest.CaptureFixture[str]) -> None:
    scene.main(["--bbox", "300", "200", "340", "280", "--vessel", "bottle_1000ml"])
    out = capsys.readouterr().out
    assert "position" in out
    assert "mouth" in out


def test_the_cli_prints_the_error_budget(capsys: pytest.CaptureFixture[str]) -> None:
    scene.main([])
    out = capsys.readouterr().out
    assert "mm/px" in out
    assert f"{math.floor(scene.TABLE_TOP_Z * 100)}" in out.replace(".", "")


def test_every_powder_vessel_in_the_catalogue_has_dimensions() -> None:
    """A decoded barcode must index straight into VESSELS, or locate cannot run.

    The powder catalogue moved from the flask series to the bottle kit; this
    is what notices if it moves again, or if a sixth size is added.
    """
    from labvision import registry

    powders = {
        sample.vessel_class
        for sample in registry.default_samples()
        if sample.phase == "powder"
    }
    assert powders
    assert powders <= set(scene.VESSELS)


def test_the_liquid_flasks_are_the_known_gap() -> None:
    from labvision import registry

    liquids = {
        sample.vessel_class
        for sample in registry.default_samples()
        if sample.phase == "liquid"
    }
    assert liquids.isdisjoint(scene.VESSELS)
