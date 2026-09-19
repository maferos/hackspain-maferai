"""Render Eki's perfumery lab with the exact box of every sample bottle in view

Loads ``simulation/models/minihannover_scene.xml`` as it is committed and adds,
in memory only, extra labelled bottles from ``simulation/assets/labelled_bottles``
so every size of both kits can stand on the bench. Every catalogue sample is
already in the room once, so the extras repeat sample ids; identity is the
barcode's job, not this script's. The scene file is never written. Four sets of
frames come out:

``as_built``
    Every named camera of the scene --- the walkthrough (entrance, aisle,
    library, wash, drying_rack, far_end) at 1280 x 720, and the vision
    system's ``general`` and ``wrist`` GoPros at their own 1920 x 1080 ---
    with the bottles where the scene file puts them.
``walkthrough``
    The walkthrough cameras, with the bottles scattered at random over both
    sides of the bench, so every size is seen from every range. This is what
    the demo video would show.
``general``
    The fixed room camera as mounted, with the bottles scattered over the
    bench. The camera that proposes.
``wrist``
    The wrist camera's mocap mount flown to a random bench bottle: 0.25 to
    0.6 m from it, from nearly side-on to nearly straight down, from the aisle
    on that bottle's side. The camera that confirms, where the arm will carry it.

Every bottle of the catalogue is truth, wherever it stands: the loose ones, the
entrance corner and the 187 on the gantry shelves. Each record says ``where``
(``bench``, ``shelf`` or ``room``), so a score can ask about the bench alone
while a detector trained on these frames is never taught that a bottle on a
shelf is background.

Every frame comes with three segmentation passes: what is visible (glass that
a detector sees through is left out, so a bottle behind a balance's draft
shield still counts as visible), the sample bottles alone (their full,
unoccluded silhouette), and a per-pixel category map (sample, shelf bottle,
glassware, balance, instrument, other) used to say what a false positive
fired on. The simulator's state is used here to write the truth and nowhere
else; the detector only ever sees the RGB frame.

    python scripts/render_perfumery.py
    python scripts/render_perfumery.py --walkthrough 0 --general 200 --wrist 600

Output: ``<out>/<set>_0000.png``, ``<out>/<set>_0000_cat.png`` and ``<out>/gt.json``.
"""

import argparse
import itertools
import json
import math
import re
import sys
from pathlib import Path

import cv2
import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labvision import registry  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
SCENE = REPO / "simulation" / "models" / "minihannover_scene.xml"
BOTTLES = REPO / "simulation" / "assets" / "labelled_bottles"

WORKTOP_Z = 0.90
"""Top of the minihannover worktop, ``HEIGHT`` in ``generate_minihannover.py``."""
BENCH_X = (-2.9, 2.9)
"""Usable length of the 6 m worktop, 10 cm in from each end."""
BENCH_Y = (0.08, 0.72)
"""Distance from the bench spine a bottle may stand at: clear of the gantry's
splash glass at y = 0 and 3 cm in from the 0.75 m edge."""
BENCH_HALF = (3.0, 0.75)
"""Half length and half depth of the worktop, centred on the world origin."""

WRIST_RANGE = (0.25, 0.6)
"""Wrist camera to its target bottle, metres. 0.25 is about where a GoPro's fixed
focus stops being sharp; 0.6 is beyond where a barcode reads."""
WRIST_ELEVATION_DEG = (10.0, 75.0)
"""Wrist camera elevation above the worktop, seen from the target bottle."""
WRIST_AZIMUTH_DEG = 50.0
"""Largest turn of the wrist camera away from straight across the aisle."""

WALKTHROUGH_CAMERAS = (
    "room_entrance",
    "room_aisle",
    "room_library",
    "room_wash",
    "room_drying_rack",
    "room_far_end",
)
"""The scene's named cameras, less ``overview``, which looks through the ceiling."""
VISION_CAMERAS = ("general", "wrist")
"""The vision system's two GoPros, mounted in the scene."""
SHELF_GEOM = re.compile(r"^room_lib_((?:SMP|PWD)-\d{4})_(body|glass|cap|label)$")
"""A gantry bottle is three geoms of the room body, not a body of its own: the
wall (``body`` for HDPE, ``glass`` for amber), the cap and the label."""

EXTRA_SAMPLES = (
    "PWD-0041", "PWD-0042", "PWD-0043", "PWD-0044", "PWD-0045",
    "PWD-0061", "PWD-0062", "PWD-0063", "PWD-0064", "PWD-0065",
    "SMP-0041", "SMP-0042", "SMP-0043", "SMP-0044", "SMP-0045",
)  # fmt: skip
"""Samples added on top of the scene's own: two of every powder bottle size and
one more of every amber size. Each also stands on the gantry, so these repeat ids."""

PARKED_Z = -5.0
"""Where an unused bottle waits, under the floor plane and out of every view."""

CATEGORIES = ("other", "sample", "shelf_bottle", "glassware", "balance", "instrument")
"""Index of each value in the category map."""
GLASSWARE = (
    "beaker", "glass", "pipette", "carboy", "funnel", "wash_", "drying",
    "jerrycan", "drum", "pot", "powder_bag", "bag_on_shelf", "sachet",
)  # fmt: skip
INSTRUMENTS = (
    "gc_ms",
    "uv_vis_nir",
    "hotplate",
    "stirrer",
    "microwave",
    "hob",
    "platform",
)

SAMPLE_GROUP = 5
"""Geom group the sample bottles are moved to, so a pass can draw them alone."""
SEE_THROUGH_GROUP = 4
"""Geom group for transparent scenery, drawn in colour but not in the visible pass."""
HIDDEN_GROUP = 3
"""Geom group no pass draws, where samples wait while others are drawn alone."""


def look_at_quat(position: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Return the MuJoCo quaternion of a camera at ``position`` looking at ``target``

    MuJoCo cameras look down their -Z axis with +Y up, so the rotation's columns
    are right, up and back, in world coordinates.
    """
    forward = target - position
    forward /= np.linalg.norm(forward)
    right = np.cross(forward, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right)
    up = np.cross(right, forward)
    rotation = np.column_stack([right, up, -forward])
    quat = np.zeros(4)
    mujoco.mju_mat2Quat(quat, rotation.reshape(-1))
    return quat


def yaw_quat(yaw: float) -> np.ndarray:
    """Return the quaternion of a rotation by ``yaw`` radians about +Z"""
    return np.array([np.cos(yaw / 2), 0.0, 0.0, np.sin(yaw / 2)])


def where_is(position: np.ndarray) -> str:
    """Say whether a bottle base is on the worktop, on a shelf above it, or elsewhere"""
    x, y, z = position
    if abs(x) <= BENCH_HALF[0] and abs(y) <= BENCH_HALF[1]:
        if abs(z - WORKTOP_Z) < 0.02:
            return "bench"
        if z > WORKTOP_Z + 0.2:
            return "shelf"
    return "room"


def boxes_by_owner(
    owner: np.ndarray, count: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Pixel count and bounding box of every owner in a label image, in one pass

    Args:
        owner: (H, W) integer image, -1 where no owner is drawn.
        count: Number of owners.

    Returns:
        Pixels per owner, the (u_min, v_min) corner and the exclusive
        (u_max, v_max) corner, each with one row per owner.
    """
    flat = owner.reshape(-1)
    pixels = np.flatnonzero(flat >= 0)
    ids = flat[pixels]
    area = np.bincount(ids, minlength=count)
    low = np.zeros((count, 2), np.int64)
    high = np.zeros((count, 2), np.int64)
    if not len(ids):
        return area, low, high
    # Sort by owner once, then reduce each owner's run of pixels.
    order = np.argsort(ids, kind="stable")
    vs, us = np.divmod(pixels[order], owner.shape[1])
    present = np.flatnonzero(area)
    starts = np.concatenate([[0], np.cumsum(area[present])[:-1]])
    low[present, 0] = np.minimum.reduceat(us, starts)
    low[present, 1] = np.minimum.reduceat(vs, starts)
    high[present, 0] = np.maximum.reduceat(us, starts) + 1
    high[present, 1] = np.maximum.reduceat(vs, starts) + 1
    return area, low, high


def quat_mul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Return the quaternion product a * b"""
    out = np.zeros(4)
    mujoco.mju_mulQuat(out, a, b)
    return out


def quat_conj(q: np.ndarray) -> np.ndarray:
    """Return the conjugate of a unit quaternion, its inverse"""
    out = np.zeros(4)
    mujoco.mju_negQuat(out, q)
    return out


def category_of(name: str) -> str:
    """Name the category a scene geom belongs to, from its name"""
    if name.startswith("room_lib_"):
        return "shelf_bottle"
    if name.startswith("balance_"):
        return "balance"
    stem = name.removeprefix("room_")
    if any(stem.startswith(k) for k in INSTRUMENTS):
        return "instrument"
    if name.startswith("room_") and any(stem.startswith(k) for k in GLASSWARE):
        return "glassware"
    return "other"


class Lab:
    """Eki's scene plus the extra bottles, compiled once"""

    def __init__(self, width: int = 1920, height: int = 1080) -> None:
        """Compile the scene with the additions and index its sample bottles"""
        spec = mujoco.MjSpec.from_file(str(SCENE))
        for k, sample_id in enumerate(EXTRA_SAMPLES):
            child = mujoco.MjSpec.from_file(str(BOTTLES / f"{sample_id}.xml"))
            body = spec.worldbody.add_body(
                name=f"extra_{k}", mocap=True, pos=[0.0, 0.0, PARKED_Z]
            )
            body.add_frame().attach_body(child.body(sample_id), f"extra_{k}_", "")
        spec.visual.global_.offwidth = max(width, spec.visual.global_.offwidth)
        spec.visual.global_.offheight = max(height, spec.visual.global_.offheight)
        self.model = spec.compile()
        self.data = mujoco.MjData(self.model)
        mujoco.mj_forward(self.model, self.data)
        m = self.model

        rows = registry.build_registry(registry.default_samples())
        by_id = {r.sample.sample_id: r for r in rows}
        pattern = re.compile(r"(SMP|PWD)-\d{4}$")
        self.samples: list[dict] = []
        for b in range(m.nbody):
            name = mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_BODY, b) or ""
            match = pattern.search(name)
            if not match or name == match.group(0):
                continue
            row = by_id[match.group(0)]
            root = b
            while m.body_parentid[root] != 0:
                root = m.body_parentid[root]
            geoms = np.flatnonzero(m.geom_bodyid == b)
            radius = max(float(m.geom_aabb[g, 3:5].max()) for g in geoms)
            self.samples.append(
                {
                    "body": b,
                    "root": root,
                    "geoms": geoms,
                    "sample_id": row.sample.sample_id,
                    "phase": row.sample.phase,
                    "container_ml": row.sample.container_ml,
                    "radius": radius,
                    "movable": m.body_mocapid[root] >= 0 or m.body_jntadr[root] >= 0,
                    "anchor_geom": None,
                }
            )

        names = [
            mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_GEOM, g)
            or mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_BODY, m.geom_bodyid[g])
            or ""
            for g in range(m.ngeom)
        ]
        shelf: dict[str, dict[str, int]] = {}
        for g, name in enumerate(names):
            match = SHELF_GEOM.match(name)
            if match:
                shelf.setdefault(match.group(1), {})[match.group(2)] = g
        for sample_id, parts in sorted(shelf.items()):
            row = by_id[sample_id]
            wall = parts.get("body", parts.get("glass"))
            self.samples.append(
                {
                    "body": int(m.geom_bodyid[wall]),
                    "root": None,
                    "geoms": np.array(sorted(parts.values())),
                    "sample_id": sample_id,
                    "phase": row.sample.phase,
                    "container_ml": row.sample.container_ml,
                    "radius": float(m.geom_rbound[wall]),
                    "movable": False,
                    "anchor_geom": wall,
                }
            )

        self.geom_category = np.array(
            [CATEGORIES.index(category_of(n)) for n in names], np.uint8
        )
        sample_geoms = np.concatenate([s["geoms"] for s in self.samples])
        self.sample_geoms = sample_geoms
        """Every geom of every sample, for the passes that draw some of them alone."""
        for s in self.samples:
            if s["anchor_geom"] is None:
                self.geom_category[s["geoms"]] = CATEGORIES.index("sample")
        self.geom_owner = np.full(m.ngeom + 1, -1, np.int64)
        """Index into :attr:`samples` of the bottle each geom belongs to; the
        extra last entry is what a pixel with no geom maps to."""
        for i, s in enumerate(self.samples):
            self.geom_owner[s["geoms"]] = i

        alpha = np.where(
            m.geom_matid >= 0, m.mat_rgba[m.geom_matid][:, 3], m.geom_rgba[:, 3]
        )
        visible = m.geom_group < 3
        see_through = visible & (alpha < 0.6)
        see_through[sample_geoms] = False
        m.geom_group[see_through] = SEE_THROUGH_GROUP
        m.geom_group[sample_geoms] = SAMPLE_GROUP

        def option(groups: tuple[int, ...]) -> mujoco.MjvOption:
            opt = mujoco.MjvOption()
            opt.geomgroup[:] = [1 if g in groups else 0 for g in range(6)]
            return opt

        self.opt_rgb = option((0, 1, 2, SEE_THROUGH_GROUP, SAMPLE_GROUP))
        self.opt_visible = option((0, 1, 2, SAMPLE_GROUP))
        self.opt_samples = option((SAMPLE_GROUP,))
        self.ray_groups = np.array([1, 1, 1, 0, 1, 1], np.uint8)
        self.worktop = {g for g, n in enumerate(names) if n.startswith("room_worktop")}
        """The worktop's own geoms: a ray that meets the right height on anything
        else, such as the bottom of an empty beaker, has not found free worktop."""
        self.home_qpos = self.data.qpos.copy()
        self.home_mocap = self.data.mocap_pos.copy(), self.data.mocap_quat.copy()
        self.cameras = {
            name: mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_CAMERA, name)
            for name in VISION_CAMERAS
        }
        wrist = self.cameras["wrist"]
        self.wrist_mocap = int(m.body_mocapid[m.cam_bodyid[wrist]])
        self.wrist_local = (m.cam_pos[wrist].copy(), m.cam_quat[wrist].copy())
        self.renderers: dict[tuple[int, int], mujoco.Renderer] = {}

    def reset(self) -> None:
        """Put every bottle back where the scene file has it, and park the extras"""
        self.data.qpos[:] = self.home_qpos
        self.data.mocap_pos[:], self.data.mocap_quat[:] = self.home_mocap
        mujoco.mj_kinematics(self.model, self.data)

    def park_all(self) -> None:
        """Move every movable bottle under the floor"""
        for s in self.samples:
            if s["movable"]:
                self.place(s, 0.0, 0.0, PARKED_Z, 0.0)

    def place(self, sample: dict, x: float, y: float, z: float, yaw: float) -> None:
        """Stand a movable bottle with its base centre at (x, y, z)"""
        m, d, root = self.model, self.data, sample["root"]
        if m.body_mocapid[root] >= 0:
            d.mocap_pos[m.body_mocapid[root]] = (x, y, z)
            d.mocap_quat[m.body_mocapid[root]] = yaw_quat(yaw)
        else:
            adr = m.jnt_qposadr[m.body_jntadr[root]]
            d.qpos[adr : adr + 3] = (x, y, z)
            d.qpos[adr + 3 : adr + 7] = yaw_quat(yaw)
        mujoco.mj_kinematics(m, d)

    def is_free(self, x: float, y: float, radius: float) -> bool:
        """Say whether a bottle of this radius fits on bare worktop at (x, y)

        Rays are cast straight down from under the gantry's lowest shelf at the
        centre and round the rim; each has to land on the worktop, not on a
        balance, a tray, a beaker or another bottle.
        """
        top = 1.2
        for angle in [None, *np.linspace(0, 2 * np.pi, 8, endpoint=False)]:
            px, py = (
                (x, y)
                if angle is None
                else (
                    x + (radius + 0.015) * np.cos(angle),
                    y + (radius + 0.015) * np.sin(angle),
                )
            )
            geom = np.array([-1], np.int32)
            dist = mujoco.mj_ray(
                self.model, self.data, np.array([px, py, top]),
                np.array([0.0, 0.0, -1.0]), self.ray_groups, 1, -1, geom,
            )  # fmt: skip
            if dist < 0 or int(geom[0]) not in self.worktop:
                return False
        return True

    def scatter(
        self,
        rng: np.random.Generator,
        count: int,
        x_range: tuple[float, float],
        sides: tuple[int, ...],
    ) -> None:
        """Park every movable bottle, then stand ``count`` of them on free worktop"""
        self.park_all()
        movable = [s for s in self.samples if s["movable"]]
        for s in rng.permutation(len(movable))[:count]:
            sample = movable[s]
            for _ in range(200):
                x = rng.uniform(*x_range)
                y = rng.choice(sides) * rng.uniform(*BENCH_Y)
                if BENCH_X[0] <= x <= BENCH_X[1] and self.is_free(
                    x, y, sample["radius"]
                ):
                    self.place(sample, x, y, WORKTOP_Z, rng.uniform(-np.pi, np.pi))
                    break

    def fly_wrist(self, position: np.ndarray, target: np.ndarray) -> None:
        """Put the wrist camera at ``position``, looking at ``target``

        The camera keeps its pose relative to the mount as the scene file gives
        it, so the mount is set to whatever puts the camera where asked.
        """
        local_pos, local_quat = self.wrist_local
        mount_quat = quat_mul(look_at_quat(position, target), quat_conj(local_quat))
        offset = np.zeros(3)
        mujoco.mju_rotVecQuat(offset, local_pos, mount_quat)
        self.data.mocap_pos[self.wrist_mocap] = position - offset
        self.data.mocap_quat[self.wrist_mocap] = mount_quat
        mujoco.mj_kinematics(self.model, self.data)

    def line_of_sight(self, start: np.ndarray, end: np.ndarray, exclude: int) -> bool:
        """Say whether nothing drawn, bar one body, stands between two points"""
        gap = end - start
        length = float(np.linalg.norm(gap))
        geom = np.array([-1], np.int32)
        dist = mujoco.mj_ray(
            self.model, self.data, start, gap / length,
            self.ray_groups, 1, exclude, geom,
        )  # fmt: skip
        return dist < 0 or dist > length

    def aim_wrist_at_random_bottle(self, rng: np.random.Generator) -> bool:
        """Fly the wrist camera to a random bottle standing on the worktop

        Returns:
            False if no pose with a clear view of any bench bottle was found.
        """
        on_bench = [
            s for s in self.samples
            if s["movable"] and where_is(self.data.xpos[s["body"]]) == "bench"
        ]  # fmt: skip
        for _ in range(50):
            if not on_bench:
                return False
            bottle = on_bench[int(rng.integers(len(on_bench)))]
            base = self.data.xpos[bottle["body"]].copy()
            aim = base + np.array([*rng.normal(0.0, 0.04, 2), 0.05])
            outward = -1.0 if base[1] < 0 else 1.0
            azimuth = np.radians(rng.uniform(-WRIST_AZIMUTH_DEG, WRIST_AZIMUTH_DEG))
            elevation = np.radians(rng.uniform(*WRIST_ELEVATION_DEG))
            reach = rng.uniform(*WRIST_RANGE)
            position = aim + reach * np.array(
                [
                    np.cos(elevation) * np.sin(azimuth),
                    outward * np.cos(elevation) * np.cos(azimuth),
                    np.sin(elevation),
                ]
            )
            if self.line_of_sight(aim, position, bottle["body"]):
                self.fly_wrist(position, aim)
                return True
        return False

    def silhouettes(
        self, camera: int, width: int, height: int, sample_pass
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Pixel count and box of every sample's whole silhouette, hidden by nothing

        A sample drawn on its own shows all of itself, but one pass per sample
        is slow with 200 in the room. Two samples whose projected bounding
        boxes do not overlap cannot hide each other, so they can share a pass:
        the samples are coloured greedily so that no two of a colour overlap,
        and ``sample_pass`` runs once per colour, a handful of times per frame.

        Args:
            camera: The camera the frame is rendered from.
            width: Frame width in pixels.
            height: Frame height in pixels.
            sample_pass: Renders the samples-only segmentation and returns the
                geom id per pixel, -1 where there is none.

        Returns:
            What :func:`boxes_by_owner` returns, one row per sample.
        """
        m, d = self.model, self.data
        count = len(self.samples)
        f = (height / 2) / math.tan(math.radians(m.cam_fovy[camera]) / 2)
        to_camera = d.cam_xmat[camera].reshape(3, 3).T
        cam_pos = d.cam_xpos[camera]

        # The eight corners of every sample geom's bounding box, in the image.
        # A silhouette lies inside the rectangle its corners span. A corner
        # behind the camera has no image, and that sample gets a pass of its own.
        geoms = self.sample_geoms
        owner = self.geom_owner[geoms]
        centre, half = m.geom_aabb[geoms, :3], m.geom_aabb[geoms, 3:]
        signs = np.array(list(itertools.product((-1.0, 1.0), repeat=3)))
        local = centre[:, None, :] + signs[None, :, :] * half[:, None, :]
        rotation = d.geom_xmat[geoms].reshape(-1, 3, 3)
        world = d.geom_xpos[geoms][:, None, :] + np.einsum(
            "nij,nkj->nki", rotation, local
        )
        view = (world - cam_pos) @ to_camera.T
        depth = -view[..., 2]
        safe = np.maximum(depth, 1e-6)
        u = width / 2 + f * view[..., 0] / safe
        v = height / 2 - f * view[..., 1] / safe
        u0, v0 = np.full(count, np.inf), np.full(count, np.inf)
        u1, v1 = np.full(count, -np.inf), np.full(count, -np.inf)
        np.minimum.at(u0, owner, u.min(axis=1))
        np.minimum.at(v0, owner, v.min(axis=1))
        np.maximum.at(u1, owner, u.max(axis=1))
        np.maximum.at(v1, owner, v.max(axis=1))
        behind = np.zeros(count, bool)
        np.logical_or.at(behind, owner, (depth <= 0).any(axis=1))
        ahead = np.zeros(count, bool)
        np.logical_or.at(ahead, owner, (depth > 0).any(axis=1))
        alone = behind & ahead  # straddles the camera plane: no rectangle
        parked = np.array([d.xpos[s["body"]][2] < 0 for s in self.samples])
        in_view = (u1 > 0) & (u0 < width) & (v1 > 0) & (v0 < height) & ~behind
        candidates = np.flatnonzero((in_view | alone) & ~parked)

        area = np.zeros(count, np.int64)
        low = np.zeros((count, 2), np.int64)
        high = np.zeros((count, 2), np.int64)
        if not len(candidates):
            return area, low, high
        # Greedy colouring, largest rectangles first, on the pairwise overlap
        # table; a pixel of margin either side for rasterisation.
        a0, b0 = u0[candidates] - 1, v0[candidates] - 1
        a1, b1 = u1[candidates] + 1, v1[candidates] + 1
        overlaps = (
            (a0[:, None] < a1[None, :])
            & (a0[None, :] < a1[:, None])
            & (b0[:, None] < b1[None, :])
            & (b0[None, :] < b1[:, None])
        )
        overlaps |= alone[candidates][:, None] | alone[candidates][None, :]
        size = np.where(alone[candidates], np.inf, (a1 - a0) * (b1 - b0))
        colours: list[list[int]] = []
        for k in np.argsort(-size):
            for members in colours:
                if not overlaps[k, members].any():
                    members.append(int(k))
                    break
            else:
                colours.append([int(k)])

        for members in colours:
            m.geom_group[geoms] = HIDDEN_GROUP
            for k in members:
                m.geom_group[self.samples[candidates[k]]["geoms"]] = SAMPLE_GROUP
            pass_area, pass_low, pass_high = boxes_by_owner(
                self.geom_owner[sample_pass()], count
            )
            rows = candidates[members]
            area[rows] = pass_area[rows]
            low[rows] = pass_low[rows]
            high[rows] = pass_high[rows]
        m.geom_group[geoms] = SAMPLE_GROUP
        return area, low, high

    def render(
        self, camera: int, width: int, height: int
    ) -> tuple[np.ndarray, list, np.ndarray]:
        """Render one frame and read the truth for every sample bottle in it

        Returns:
            The RGB frame, one record per bottle that has any pixel in view, and
            the per-pixel category map.
        """
        key = (width, height)
        if key not in self.renderers:
            self.renderers[key] = mujoco.Renderer(
                self.model, height=height, width=width
            )
        r = self.renderers[key]
        d = self.data
        mujoco.mj_camlight(self.model, d)

        r.update_scene(d, camera=camera, scene_option=self.opt_rgb)
        rgb = r.render()
        r.enable_segmentation_rendering()

        def segment(option: mujoco.MjvOption) -> np.ndarray:
            r.update_scene(d, camera=camera, scene_option=option)
            # Ids need no lighting; shadows and reflections only cost time.
            r.scene.flags[mujoco.mjtRndFlag.mjRND_SHADOW] = 0
            r.scene.flags[mujoco.mjtRndFlag.mjRND_REFLECTION] = 0
            return r.render()

        geom_type = int(mujoco.mjtObj.mjOBJ_GEOM)

        def geom_ids(option: mujoco.MjvOption) -> np.ndarray:
            """Segment and keep each pixel's geom id, -1 where there is none"""
            image = segment(option)
            return np.where(image[..., 1] == geom_type, image[..., 0], -1)

        seen_ids = geom_ids(self.opt_visible)
        full_area, full_low, full_high = self.silhouettes(
            camera, width, height, lambda: geom_ids(self.opt_samples)
        )
        r.disable_segmentation_rendering()
        categories = np.where(
            seen_ids >= 0, self.geom_category[np.maximum(seen_ids, 0)], 0
        )

        cam_pos = d.cam_xpos[camera].copy()
        count = len(self.samples)
        # -1 (no geom) indexes the owner table's extra last entry, which is -1.
        seen_area, seen_low, seen_high = boxes_by_owner(
            self.geom_owner[seen_ids], count
        )
        bottles = []
        for i in np.flatnonzero(full_area):
            s = self.samples[i]
            if s["anchor_geom"] is None:
                position = d.xpos[s["body"]].copy()
            else:
                # A gantry bottle has no body of its own: take its wall geom's
                # bounding box and report the base, as the bench bottles do.
                g = s["anchor_geom"]
                box_centre = self.model.geom_aabb[g, :3]
                centre = d.geom_xpos[g] + d.geom_xmat[g].reshape(3, 3) @ box_centre
                position = centre - [0.0, 0.0, self.model.geom_aabb[g, 5]]
            if position[2] < 0:
                continue  # parked under the floor
            full_box = [*map(int, full_low[i]), *map(int, full_high[i])]
            box = full_box
            if seen_area[i]:
                box = [*map(int, seen_low[i]), *map(int, seen_high[i])]
            bottles.append(
                {
                    "sample_id": s["sample_id"],
                    "phase": s["phase"],
                    "container_ml": s["container_ml"],
                    "where": where_is(position),
                    "xyxy": box,
                    "full_xyxy": full_box,
                    "pixels": int(seen_area[i]),
                    "visible_frac": round(float(seen_area[i]) / float(full_area[i]), 3),
                    "clipped": bool(
                        full_box[0] <= 0
                        or full_box[1] <= 0
                        or full_box[2] >= width
                        or full_box[3] >= height
                    ),  # fmt: skip
                    "position": [round(float(v), 4) for v in position],
                    "distance_m": round(float(np.linalg.norm(position - cam_pos)), 3),
                }
            )
        return rgb, bottles, categories.astype(np.uint8)


def main() -> None:
    """Render the four sets and write the ground truth"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--walkthrough",
        type=int,
        default=5,
        help="random layouts per walkthrough camera",
    )
    parser.add_argument(
        "--general", type=int, default=20, help="frames from the fixed room camera"
    )
    parser.add_argument(
        "--wrist", type=int, default=40, help="frames from the wrist camera"
    )
    parser.add_argument("--no-as-built", action="store_true", help="skip as_built")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--out", default=None, help="default ../simulation/out/perfumery"
    )
    args = parser.parse_args()

    out = Path(args.out or REPO / "simulation" / "out" / "perfumery")
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    lab = Lab()
    m = lab.model
    print(
        f"{len(lab.samples)} sample bottles, "
        f"{sum(s['movable'] for s in lab.samples)} movable"
    )

    frames: list[dict] = []

    def save(set_name: str, camera: int, width: int, height: int) -> None:
        rgb, bottles, categories = lab.render(camera, width, height)
        stem = f"{set_name}_{sum(f['set'] == set_name for f in frames):04d}"
        cv2.imwrite(str(out / f"{stem}.png"), rgb[:, :, ::-1])
        cv2.imwrite(str(out / f"{stem}_cat.png"), categories)
        frames.append(
            {
                "file": f"{stem}.png",
                "categories": f"{stem}_cat.png",
                "set": set_name,
                "camera": mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_CAMERA, camera),
                "width": width,
                "height": height,
                "fovy_deg": round(float(m.cam_fovy[camera]), 3),
                "cam_pos": [round(float(v), 4) for v in lab.data.cam_xpos[camera]],
                "cam_xmat": [round(float(v), 6) for v in lab.data.cam_xmat[camera]],
                "bottles": bottles,
            }
        )
        print(
            f"{stem}: {frames[-1]['camera']}, {len(bottles)} bottles in view",
            flush=True,
        )

    walkthrough = [
        mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_CAMERA, c) for c in WALKTHROUGH_CAMERAS
    ]
    general, wrist = lab.cameras["general"], lab.cameras["wrist"]

    def resolution(camera: int) -> tuple[int, int]:
        width, height = (int(v) for v in m.cam_resolution[camera])
        return (width, height) if width > 1 else (1280, 720)

    lab.reset()
    if not args.no_as_built:
        for camera in [*walkthrough, general, wrist]:
            save("as_built", camera, *resolution(camera))

    for _ in range(args.walkthrough):
        lab.scatter(rng, int(rng.integers(14, 21)), BENCH_X, (-1, 1))
        for camera in walkthrough:
            save("walkthrough", camera, 1280, 720)

    for _ in range(args.general):
        lab.scatter(rng, int(rng.integers(14, 21)), BENCH_X, (-1, 1))
        save("general", general, *resolution(general))

    done = 0
    while done < args.wrist:
        # A few bottles near each other, so a close view holds more than one.
        x0 = rng.uniform(*BENCH_X)
        side = (int(rng.choice((-1, 1))),)
        lab.scatter(rng, int(rng.integers(4, 9)), (x0 - 0.4, x0 + 0.4), side)
        if lab.aim_wrist_at_random_bottle(rng):
            save("wrist", wrist, *resolution(wrist))
            done += 1

    gt = {"scene": str(SCENE.relative_to(REPO)).replace("\\", "/"), "frames": frames}
    (out / "gt.json").write_text(json.dumps(gt, indent=1), encoding="utf-8")
    total = sum(len(f["bottles"]) for f in frames)
    print(f"{len(frames)} frames, {total} bottle views -> {out}")


if __name__ == "__main__":
    main()
