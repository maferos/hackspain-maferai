"""Tests for the pinhole model, the ray-plane intersection and the homography.

Two independent oracles are used where one exists: OpenCV's ``undistortPoints``
for the distortion inverse and ``findHomography`` for the DLT, the same trick
``test_ean13.py`` plays with ``python-barcode``.
"""

import cv2
import numpy as np
import pytest

from labvision.camera import (
    Camera,
    GeometryError,
    Intrinsics,
    Plane,
    apply_homography,
    homography_from_points,
    horizon_line,
    metres_per_pixel,
    pixel_to_plane,
    plane_footprint,
    plane_homography,
    plane_jacobian,
    ray_plane_intersection,
)

DISTORTION = (-0.28, 0.12, 0.001, -0.002, 0.0)


@pytest.fixture
def intrinsics() -> Intrinsics:
    return Intrinsics.from_fov(640, 480, fovy_deg=45.0)


@pytest.fixture
def camera(intrinsics: Intrinsics) -> Camera:
    return Camera.look_at(intrinsics, (7.0, 0.0, 3.0), (7.0, 2.5, 0.95))


@pytest.fixture
def bench() -> Plane:
    return Plane.horizontal(0.95)


# --- intrinsics ------------------------------------------------------------


def test_from_fov_puts_the_principal_point_at_the_image_centre(
    intrinsics: Intrinsics,
) -> None:
    assert (intrinsics.cx, intrinsics.cy) == (319.5, 239.5)


def test_from_fov_round_trips_the_field_of_view(intrinsics: Intrinsics) -> None:
    assert intrinsics.fovy_deg == pytest.approx(45.0)


def test_square_pixels_widen_the_horizontal_field_of_view(
    intrinsics: Intrinsics,
) -> None:
    assert intrinsics.fx == intrinsics.fy
    assert intrinsics.fovx_deg > intrinsics.fovy_deg


def test_from_fov_accepts_the_horizontal_field_of_view_instead(
    intrinsics: Intrinsics,
) -> None:
    by_x = Intrinsics.from_fov(640, 480, fovx_deg=intrinsics.fovx_deg)
    assert by_x.fy == pytest.approx(intrinsics.fy)


def test_from_fov_needs_exactly_one_field_of_view() -> None:
    with pytest.raises(GeometryError):
        Intrinsics.from_fov(640, 480)
    with pytest.raises(GeometryError):
        Intrinsics.from_fov(640, 480, fovy_deg=45.0, fovx_deg=60.0)


def test_from_sensor_matches_the_equivalent_field_of_view() -> None:
    # A 6 mm lens on a 1/2.5" sensor (5.7 mm wide) is about 51 degrees across.
    from_mm = Intrinsics.from_sensor(640, 480, focal_mm=6.0, sensor_width_mm=5.7)
    assert from_mm.fovx_deg == pytest.approx(50.9, abs=0.1)


def test_intrinsics_reject_nonsense() -> None:
    with pytest.raises(GeometryError):
        Intrinsics(0.0, 100.0, 10.0, 10.0, 20, 20)
    with pytest.raises(GeometryError):
        Intrinsics(100.0, 100.0, 10.0, 10.0, 0, 20)
    with pytest.raises(GeometryError):
        Intrinsics(100.0, 100.0, 10.0, 10.0, 20, 20, distortion=(1.0, 2.0))


def test_contains_uses_pixel_edges_not_centres(intrinsics: Intrinsics) -> None:
    assert intrinsics.contains((-0.5, -0.5))
    assert intrinsics.contains((639.5, 479.5))
    assert not intrinsics.contains((639.51, 200.0))


def test_normalise_inverts_denormalise_without_distortion(
    intrinsics: Intrinsics,
) -> None:
    pixels = np.array([[0.0, 0.0], [319.5, 239.5], [639.0, 479.0]])
    assert np.allclose(intrinsics.denormalise(intrinsics.normalise(pixels)), pixels)


def test_normalise_inverts_denormalise_with_distortion() -> None:
    """Five fixed-point steps leave a hundredth of a pixel in the corners."""
    lens = Intrinsics.from_fov(640, 480, fovy_deg=45.0, distortion=DISTORTION)
    pixels = np.array([[10.0, 10.0], [319.5, 239.5], [600.0, 400.0]])
    assert np.allclose(lens.denormalise(lens.normalise(pixels)), pixels, atol=1e-2)


def test_undistortion_agrees_with_opencv() -> None:
    """The fixed-point inverse is ours; OpenCV's is the oracle for it."""
    lens = Intrinsics.from_fov(640, 480, fovy_deg=45.0, distortion=DISTORTION)
    rng = np.random.default_rng(7)
    pixels = rng.uniform([0, 0], [640, 480], size=(200, 2))
    theirs = cv2.undistortPoints(
        pixels.reshape(-1, 1, 2), lens.matrix, lens.distortion_vector
    ).reshape(-1, 2)
    assert np.allclose(lens.normalise(pixels), theirs, atol=1e-9)


def test_distortion_agrees_with_opencv() -> None:
    lens = Intrinsics.from_fov(640, 480, fovy_deg=45.0, distortion=DISTORTION)
    rng = np.random.default_rng(8)
    ideal = rng.uniform(-0.4, 0.4, size=(200, 2))
    points = np.column_stack([ideal, np.ones(len(ideal))])
    theirs, _ = cv2.projectPoints(
        points, np.zeros(3), np.zeros(3), lens.matrix, lens.distortion_vector
    )
    assert np.allclose(lens.denormalise(ideal), theirs.reshape(-1, 2), atol=1e-9)


# --- pose ------------------------------------------------------------------


def test_look_at_builds_a_right_handed_orthonormal_frame(camera: Camera) -> None:
    assert np.allclose(camera.rotation @ camera.rotation.T, np.eye(3))
    assert np.linalg.det(camera.rotation) == pytest.approx(1.0)


def test_the_principal_ray_passes_through_the_target(camera: Camera) -> None:
    pixel = camera.project(np.array([7.0, 2.5, 0.95]))
    assert pixel == pytest.approx((camera.intrinsics.cx, camera.intrinsics.cy))


def test_look_at_rejects_an_up_vector_along_the_view(intrinsics: Intrinsics) -> None:
    with pytest.raises(GeometryError):
        Camera.look_at(intrinsics, (0.0, 0.0, 3.0), (0.0, 0.0, 0.0))


def test_image_down_is_world_down_for_a_level_camera(intrinsics: Intrinsics) -> None:
    level = Camera.look_at(intrinsics, (0.0, 0.0, 1.0), (1.0, 0.0, 1.0))
    assert np.allclose(level.forward, [1.0, 0.0, 0.0])
    assert np.allclose(level.down, [0.0, 0.0, -1.0])


def test_pan_tilt_agrees_with_look_at(intrinsics: Intrinsics) -> None:
    aimed = Camera.look_at(intrinsics, (7.0, 0.0, 3.0), (7.0, 2.5, 0.95))
    panned = Camera.from_pan_tilt(
        intrinsics, (7.0, 0.0, 3.0), pan_deg=90.0, tilt_deg=39.353
    )
    assert np.allclose(aimed.rotation, panned.rotation, atol=1e-4)


def test_from_mujoco_flips_the_opengl_frame(intrinsics: Intrinsics) -> None:
    """An identity MuJoCo xmat looks down world -Z with world +Y up."""
    converted = Camera.from_mujoco(intrinsics, (0.0, 0.0, 2.0), np.eye(3).reshape(9))
    assert np.allclose(converted.forward, [0.0, 0.0, -1.0])
    assert np.allclose(converted.down, [0.0, -1.0, 0.0])


def test_from_mujoco_round_trips_an_arbitrary_pose(camera: Camera) -> None:
    opengl = camera.rotation @ np.diag([1.0, -1.0, -1.0])
    back = Camera.from_mujoco(camera.intrinsics, camera.position, opengl)
    assert np.allclose(back.rotation, camera.rotation)


def test_camera_rejects_a_rotation_that_is_not_one(intrinsics: Intrinsics) -> None:
    with pytest.raises(GeometryError):
        Camera(intrinsics, (0.0, 0.0, 1.0), np.eye(3) * 2.0)
    with pytest.raises(GeometryError):
        Camera(intrinsics, (0.0, 0.0, 1.0), np.diag([1.0, 1.0, -1.0]))


def test_from_correspondences_recovers_a_known_pose(camera: Camera) -> None:
    """Four markers on the bench are enough to solve for where the camera is."""
    markers = np.array([[6.0, 1.5, 0.95], [8.0, 1.5, 0.95],
                        [8.0, 3.5, 0.95], [6.0, 3.5, 0.95]])
    solved = Camera.from_correspondences(
        camera.intrinsics, camera.project(markers), markers
    )
    assert np.allclose(solved.position, camera.position, atol=1e-6)
    assert np.allclose(solved.rotation, camera.rotation, atol=1e-6)


def test_from_correspondences_needs_four_matched_points(camera: Camera) -> None:
    with pytest.raises(GeometryError):
        Camera.from_correspondences(
            camera.intrinsics, [[0.0, 0.0]] * 3, [[0.0, 0.0, 0.0]] * 3
        )
    with pytest.raises(GeometryError):
        Camera.from_correspondences(
            camera.intrinsics, [[0.0, 0.0]] * 4, [[0.0, 0.0, 0.0]] * 5
        )


# --- projection ------------------------------------------------------------


def test_projection_round_trips_through_the_ray(camera: Camera) -> None:
    rng = np.random.default_rng(3)
    pixels = rng.uniform([0, 0], [640, 480], size=(50, 2))
    points = camera.position + 2.5 * camera.pixel_ray(pixels)
    assert np.allclose(camera.project(points), pixels, atol=1e-9)


def test_points_behind_the_camera_have_no_image(camera: Camera) -> None:
    behind = camera.position - 2.0 * camera.forward
    assert np.isnan(camera.project(behind)).all()


def test_rays_are_unit_length(camera: Camera) -> None:
    rays = camera.pixel_ray(np.array([[0.0, 0.0], [639.0, 479.0]]))
    assert np.allclose(np.linalg.norm(rays, axis=-1), 1.0)


# --- ray and plane ---------------------------------------------------------


def test_intersection_of_a_vertical_ray_with_a_horizontal_plane() -> None:
    hit = ray_plane_intersection((1.0, 2.0, 3.0), (0.0, 0.0, -1.0),
                                 Plane.horizontal(0.95))
    assert np.allclose(hit, [1.0, 2.0, 0.95])


def test_a_parallel_ray_never_meets_the_plane() -> None:
    hit = ray_plane_intersection((0.0, 0.0, 3.0), (1.0, 0.0, 0.0),
                                 Plane.horizontal(0.95))
    assert np.isnan(hit).all()


def test_a_plane_behind_the_camera_is_not_a_hit() -> None:
    hit = ray_plane_intersection((0.0, 0.0, 3.0), (0.0, 0.0, 1.0),
                                 Plane.horizontal(0.95))
    assert np.isnan(hit).all()


def test_pixel_to_plane_is_vectorised(camera: Camera, bench: Plane) -> None:
    pixels = np.array([[319.5, 239.5], [200.0, 300.0], [400.0, 260.0]])
    points = pixel_to_plane(camera, pixels, bench)
    assert points.shape == (3, 3)
    assert np.allclose(points[:, 2], 0.95)


def test_pixel_to_plane_inverts_the_projection(camera: Camera, bench: Plane) -> None:
    truth = np.array([[6.4, 1.8, 0.95], [7.9, 3.2, 0.95], [7.0, 2.5, 0.95]])
    assert np.allclose(pixel_to_plane(camera, camera.project(truth), bench), truth)


def test_a_pixel_above_the_horizon_gives_nan(camera: Camera, bench: Plane) -> None:
    assert np.isnan(pixel_to_plane(camera, (319.5, -300.0), bench)).all()


def test_signed_distance_is_signed(bench: Plane) -> None:
    assert bench.signed_distance((0.0, 0.0, 1.95)) == pytest.approx(1.0)
    assert bench.signed_distance((0.0, 0.0, 0.0)) == pytest.approx(-0.95)


# --- error propagation -----------------------------------------------------


def test_the_jacobian_matches_finite_differences(
    camera: Camera, bench: Plane,
) -> None:
    pixel = np.array([250.0, 300.0])
    analytic = plane_jacobian(camera, pixel, bench)
    numeric = np.column_stack([
        (pixel_to_plane(camera, pixel + step, bench)
         - pixel_to_plane(camera, pixel - step, bench)) / 2.0
        for step in (np.array([1.0, 0.0]), np.array([0.0, 1.0]))
    ])
    assert np.allclose(analytic, numeric, atol=1e-6)


def test_the_jacobian_is_nan_where_there_is_no_hit(
    camera: Camera, bench: Plane,
) -> None:
    assert np.isnan(plane_jacobian(camera, (319.5, -300.0), bench)).all()


def test_a_pixel_is_worth_more_metres_further_away(
    camera: Camera, bench: Plane,
) -> None:
    near = camera.project(np.array([7.0, 1.6, 0.95]))
    far = camera.project(np.array([7.0, 3.4, 0.95]))
    assert metres_per_pixel(camera, far, bench)[0] > (
        2.0 * metres_per_pixel(camera, near, bench)[0]
    )


def test_the_worst_direction_is_worse_than_the_best(
    camera: Camera, bench: Plane,
) -> None:
    worst, best = metres_per_pixel(camera, (319.5, 239.5), bench)
    assert worst > best > 0.0


# --- horizon and footprint -------------------------------------------------


def test_the_horizon_line_separates_hits_from_misses(
    camera: Camera, bench: Plane,
) -> None:
    line = horizon_line(camera, bench)
    rng = np.random.default_rng(11)
    pixels = rng.uniform([-2000, -2000], [2000, 2000], size=(400, 2))
    side = np.column_stack([pixels, np.ones(len(pixels))]) @ line
    hits = np.isfinite(pixel_to_plane(camera, pixels, bench)).all(axis=1)
    assert np.array_equal(hits, side > 0.0)


def test_the_horizon_of_a_level_camera_is_the_principal_row(
    intrinsics: Intrinsics, bench: Plane,
) -> None:
    level = Camera.look_at(intrinsics, (0.0, 0.0, 3.0), (1.0, 0.0, 3.0))
    a, b, c = horizon_line(level, bench)
    assert a == pytest.approx(0.0)
    assert -c / b == pytest.approx(intrinsics.cy)


def test_the_footprint_brackets_what_the_camera_sees(
    camera: Camera, bench: Plane,
) -> None:
    corners = plane_footprint(camera, bench)
    assert corners.shape == (4, 3)
    assert np.isfinite(corners).all()
    centre = pixel_to_plane(camera, (319.5, 239.5), bench)
    assert corners[:, 1].min() < centre[1] < corners[:, 1].max()


# --- homography ------------------------------------------------------------


def test_the_homography_agrees_with_the_full_model(
    camera: Camera, bench: Plane,
) -> None:
    homography = plane_homography(camera, 0.95)
    plane_points = np.array([[6.0, 1.5], [8.0, 1.5], [8.0, 3.5], [6.0, 3.5]])
    world = np.column_stack([plane_points, np.full(len(plane_points), 0.95)])
    assert np.allclose(apply_homography(homography, plane_points),
                       camera.project(world))


def test_the_inverse_homography_is_pixel_to_plane(
    camera: Camera, bench: Plane,
) -> None:
    inverse = np.linalg.inv(plane_homography(camera, 0.95))
    pixels = np.array([[100.0, 400.0], [500.0, 300.0]])
    assert np.allclose(apply_homography(inverse, pixels),
                       pixel_to_plane(camera, pixels, bench)[:, :2])


def test_four_known_points_replace_the_whole_calibration(camera: Camera) -> None:
    """The point of the shortcut: no focal length, no pose, same answer."""
    markers = np.array([[6.0, 1.5], [8.0, 1.5], [8.0, 3.5], [6.0, 3.5]])
    world = np.column_stack([markers, np.full(len(markers), 0.95)])
    fitted = homography_from_points(markers, camera.project(world))
    known = plane_homography(camera, 0.95)
    assert np.allclose(fitted, known / known[2, 2], rtol=1e-6, atol=1e-8)


def test_the_dlt_agrees_with_opencv(camera: Camera) -> None:
    markers = np.array([[6.0, 1.5], [8.0, 1.5], [8.0, 3.5], [6.0, 3.5],
                        [7.3, 2.2], [6.6, 3.0]])
    world = np.column_stack([markers, np.full(len(markers), 0.95)])
    pixels = camera.project(world)
    theirs, _ = cv2.findHomography(markers, pixels)
    mine = homography_from_points(markers, pixels)
    assert np.allclose(mine, theirs / theirs[2, 2], rtol=1e-4, atol=1e-4)


def test_the_homography_refuses_to_pretend_distortion_is_projective() -> None:
    lens = Intrinsics.from_fov(640, 480, fovy_deg=45.0, distortion=DISTORTION)
    distorted = Camera.look_at(lens, (7.0, 0.0, 3.0), (7.0, 2.5, 0.95))
    with pytest.raises(GeometryError, match="distortion"):
        plane_homography(distorted, 0.95)


def test_the_dlt_rejects_too_few_or_mismatched_points() -> None:
    with pytest.raises(GeometryError):
        homography_from_points([[0.0, 0.0]] * 3, [[0.0, 0.0]] * 3)
    with pytest.raises(GeometryError):
        homography_from_points([[0.0, 0.0]] * 4, [[0.0, 0.0]] * 5)


def test_the_dlt_rejects_collinear_points(camera: Camera) -> None:
    collinear = np.array([[6.0, 1.5], [6.5, 1.5], [7.0, 1.5], [7.5, 1.5]])
    world = np.column_stack([collinear, np.full(len(collinear), 0.95)])
    with pytest.raises(GeometryError, match="degenerate"):
        homography_from_points(collinear, camera.project(world))


def test_from_mujoco_reproduces_the_hand_written_mujoco_back_projection() -> None:
    """Pins the frame conversion against the snippet measured in MuJoCo.

    Before this module existed, MuJoCo frames were back-projected with a
    hand-written expression, verified in simulation to recover object
    positions exactly. Going through Camera must not change a digit of it.
    """
    width, height, fovy = 640, 480, 45.0
    xmat = np.array([[0.0, -0.634, 0.773],
                     [1.0, 0.0, 0.0],
                     [0.0, 0.773, 0.634]])
    xmat, _ = np.linalg.qr(xmat)  # nearest orthonormal frame to those digits
    xmat *= np.sign(np.linalg.det(xmat))
    position = np.array([7.0, 0.0, 3.0])

    focal = (1.0 / np.tan(np.radians(fovy) / 2.0)) * height / 2.0
    cx, cy = (width - 1) / 2.0, (height - 1) / 2.0
    pixels = np.array([[100.0, 380.0], [319.5, 239.5], [560.0, 300.0]])
    expected = np.array([
        xmat @ np.array([(u - cx) / focal, -(v - cy) / focal, -1.0])
        for u, v in pixels
    ])
    expected /= np.linalg.norm(expected, axis=1, keepdims=True)

    camera = Camera.from_mujoco(
        Intrinsics.from_fov(width, height, fovy_deg=fovy), position, xmat
    )
    assert np.allclose(camera.pixel_ray(pixels), expected)
