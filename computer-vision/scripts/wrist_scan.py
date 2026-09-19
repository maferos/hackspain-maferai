"""Fly the wrist camera in front of sample bottles and scan what it sees

The minihannover scene carries a ``wrist`` camera on a mocap body: a GoPro in
Linear mode at 1080p, standing in for the camera on the arm. This script parks
it square in front of one bottle's label after another, renders the frame,
runs :func:`labvision.reader.decode_image` on the **whole frame** and checks
the code against the lookup table. Nothing tells the reader where the label
is or which sample to expect.

A GoPro's fixed focus is sharp from about 0.30 m, so that is the first
standoff tried. When the frame does not decode, the camera steps closer, the
way an arm would, and the first standoff that reads is the one reported. If no
level view reads, the same standoffs are tried again looking down at the label
from a little above, gentlest angle first: the gantry shelves have a 20 mm lip,
and from level it hides the bottom of the label on a small flask standing well
back. Gentlest first because the labels are turned a quarter turn, so their
bars are rings round the bottle, and from above a ring is an arc: at 25 degrees
and 0.10 m the bars bend too far to rectify, at 8 degrees they still read. The
render has no defocus, so reads closer than 0.30 m are optimistic for a real
GoPro and the contact sheet says at which distance each one was made.

Two things can be varied. ``--approach label`` parks the camera square in
front of the label, which takes knowing how the bottle is turned: the best
case. ``--approach aisle`` comes at the bottle from the aisle it stands beside,
whichever way its label faces, which is what an arm gets. And ``--symbology``
says what the bottles carry: ``ean`` for the one-sided EAN-13 label, ``aruco``
for the ring of ``DICT_4X4_250`` markers, ``auto`` to ask the bottle kit's
manifest. A ring has no side, so ``label`` means ``aisle`` for it.

By default the thirteen hand-placed bottles are scanned plus a seeded draw
from the gantry shelves, so every bottle size is covered and so is the
scattered library.

    python scripts/wrist_scan.py                       # 13 placed + 7 shelved
    python scripts/wrist_scan.py --shelf 0 --samples PWD-0012 SMP-0021
    python scripts/wrist_scan.py --standoffs 0.30      # no stepping closer

Output: ``<out>/<sample id>.png`` per frame, ``<out>/contact_sheet.png`` and
``<out>/results.json``. Needs ``mujoco``, which the rest of the package does not.
"""

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import cv2
import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labvision import reader, registry  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
SCENE = REPO / "simulation" / "models" / "minihannover_scene.xml"
TABLE = REPO / "computer-vision" / "barcodes" / "lookup_table.json"
MANIFEST = REPO / "simulation" / "assets" / "labelled_bottles" / "manifest.json"
ROOM_X0, ROOM_Y0 = -8.5, -2.9
"""The entrance wall and the right wall, which the corner counters stand against."""

CORNER_X = -7.0
"""Bottles farther towards the entrance than this stand on the corner counters."""

ARUCO_MODULES = 8
"""Modules across one marker of the ring, quiet zone included."""
DEFAULT_STANDOFFS_M = (0.30, 0.20, 0.15, 0.10)
"""Label-to-lens distances tried in order; 0.30 m is a GoPro's near focus."""

ELEVATIONS_DEG = (0.0, 8.0, 16.0, 25.0)
"""Approach angles tried in order: level with the label, then from ever higher."""

SETTLE_STEPS = 400
"""Simulation steps before rendering, so the loose bottles have come to rest."""

TILE_W, TILE_H = 640, 360
INSET = 360
"""Contact sheet: each frame shrunk to a tile, beside a full-resolution crop."""

CAPTION_H = 84
COLUMNS = 4
GREEN, RED, AMBER, INK = (60, 150, 40), (40, 40, 210), (0, 130, 230), (30, 30, 30)


@dataclass(frozen=True)
class Target:
    """One bottle's label, as found in the compiled scene.

    Attributes:
        sample_id: Catalogue id, which is also what the barcode must resolve to.
        where: ``bench``, ``corner`` or ``shelf``.
        centre: Label centre in world metres.
        normal: Horizontal unit vector pointing out of the label, or None for
            a label that goes all the way round.
        axis: The bottle's axis in the floor plane.
        label_height_m: Vertical extent of the sticker, the printed label's width.
    """

    sample_id: str
    where: str
    centre: np.ndarray
    normal: np.ndarray | None
    axis: np.ndarray
    label_height_m: float


@dataclass(frozen=True)
class Scan:
    """What one bottle's scan came to.

    Attributes:
        sample_id: The bottle the camera was parked in front of.
        material: Its material, from the lookup table.
        container_ml: Its container size.
        where: ``bench``, ``corner`` or ``shelf``.
        standoff_m: Distance of the frame that is reported.
        elevation_deg: How far above the label's level the camera was.
        px_per_module: Width of one barcode module in that frame.
        tried_m: Every standoff tried, in order.
        code: The code read for this bottle, or None.
        read_as: The sample that code resolves to, or None.
        others: Other samples decoded in the same frame.
        verdict: ``ok``, ``wrong`` or ``no read``.
    """

    sample_id: str
    material: str
    container_ml: float
    where: str
    standoff_m: float
    elevation_deg: float
    px_per_module: float
    tried_m: list[float]
    code: str | None
    read_as: str | None
    others: list[str]
    verdict: str


def find_targets(model: mujoco.MjModel, data: mujoco.MjData) -> dict[str, Target]:
    """Locate every label in the scene from its geom and its bottle's cap

    A label geom sits at the centroid of its sticker and the bottle's cap geom
    on the bottle's axis, so the horizontal direction from one to the other is
    the way the label faces.

    Args:
        model: The compiled scene.
        data: Its state, already forwarded.

    Returns:
        Targets keyed by sample id.
    """
    targets = {}
    for geom in range(model.ngeom):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, geom) or ""
        if not name.endswith("_label"):
            continue
        stem = name[: -len("_label")]
        if stem.startswith("room_lib_"):
            sample_id, where = stem[len("room_lib_") :], "shelf"
        else:
            body = mujoco.mj_id2name(
                model, mujoco.mjtObj.mjOBJ_BODY, model.geom_bodyid[geom]
            )
            sample_id = body[len(stem) + 1 :]
            where = "corner" if stem.startswith("corner_") else "bench"
        # The cap, not the wall: powders call the wall "body" and liquids "glass",
        # while every bottle has a cap and it sits on the axis.
        cap = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, f"{stem}_cap")
        if cap < 0:
            raise SystemExit(
                f"{name}: no {stem}_cap geom to take the bottle's axis from"
            )
        axis = data.geom_xpos[cap]
        centre = data.geom_xpos[geom].copy()
        normal = np.array([*(centre[:2] - axis[:2]), 0.0])
        # A ring's centroid is on the axis: it has no side to face.
        one_sided = np.linalg.norm(normal) > 1e-3
        mesh = model.geom_dataid[geom]
        start, count = model.mesh_vertadr[mesh], model.mesh_vertnum[mesh]
        vertices = (
            model.mesh_vert[start : start + count]
            @ data.geom_xmat[geom].reshape(3, 3).T
        )
        targets[sample_id] = Target(
            sample_id,
            where,
            centre,
            normal / np.linalg.norm(normal) if one_sided else None,
            axis[:2].copy(),
            float(np.ptp(vertices[:, 2])),
        )
    return targets


def park(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    camera: int,
    target: Target,
    standoff_m: float,
    elevation_deg: float = 0.0,
) -> None:
    """Move the wrist mount so the camera looks at a label's centre

    Args:
        model: The compiled scene.
        data: Its state; the mount's mocap pose is overwritten.
        camera: Id of the wrist camera.
        target: The label to face.
        standoff_m: Distance from the label's centre to the camera.
        elevation_deg: Angle of the camera above the label's level, seen from
            the label. Zero faces it squarely.
    """
    tilt = math.radians(elevation_deg)
    outward = math.cos(tilt) * target.normal + math.sin(tilt) * np.array(
        [0.0, 0.0, 1.0]
    )
    forward = -outward
    right = np.cross(forward, (0.0, 0.0, 1.0))
    right /= np.linalg.norm(right)
    up = np.cross(right, forward)
    wanted = np.column_stack([right, up, -forward])  # MuJoCo looks down its -Z
    local = np.zeros(9)
    mujoco.mju_quat2Mat(local, model.cam_quat[camera])
    mount = wanted @ local.reshape(3, 3).T
    quat = np.zeros(4)
    mujoco.mju_mat2Quat(quat, mount.flatten())
    mocap = model.body_mocapid[model.cam_bodyid[camera]]
    eye = target.centre + standoff_m * outward
    data.mocap_pos[mocap] = eye - mount @ model.cam_pos[camera]
    data.mocap_quat[mocap] = quat
    mujoco.mj_forward(model, data)


def aisle_direction(target: Target) -> np.ndarray:
    """Horizontal unit vector from a bottle towards the aisle it is reached from

    The bench and its gantry run along X through the origin, with an aisle on
    either side, so a bottle there is reached from its own side. The entrance
    corner's counters stand against two walls, and a bottle there is reached
    from the room, away from the nearer wall.
    """
    x, y = target.axis
    if x < CORNER_X:
        from_x_wall = x - ROOM_X0 < y - ROOM_Y0
        return np.array([1.0, 0.0, 0.0]) if from_x_wall else np.array([0.0, 1.0, 0.0])
    return np.array([0.0, 1.0 if y > 0 else -1.0, 0.0])


def from_aisle(target: Target, radius_m: float) -> Target:
    """The same bottle, aimed at from its aisle instead of from its label's side"""
    direction = aisle_direction(target)
    surface = np.array([*target.axis, target.centre[2]]) + radius_m * direction
    return replace(target, centre=surface, normal=direction)


def make_scanner(symbology: str, table: dict) -> "callable":
    """Build ``frame -> [(code, corners or None, table row or None)]``

    Args:
        symbology: ``ean`` or ``aruco``.
        table: The lookup table, whose rows carry ``marker_id``.

    Returns:
        A function that reads every symbol of that kind in a frame.
    """
    if symbology == "ean":

        def scan_ean(frame: np.ndarray) -> list:
            found = reader.resolve(reader.decode_image(frame), table)
            return [(d.code, d.corners, row) for d, row in found]

        return scan_ean

    by_marker = {row["marker_id"]: row for row in table.values()}
    parameters = cv2.aruco.DetectorParameters()
    parameters.minMarkerPerimeterRate = 0.02
    parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    detector = cv2.aruco.ArucoDetector(
        cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250), parameters
    )

    def scan_aruco(frame: np.ndarray) -> list:
        corners, ids, _ = detector.detectMarkers(frame)
        if ids is None:
            return []
        return [
            (f"aruco {int(i)}", c.reshape(4, 2), by_marker.get(int(i)))
            for i, c in zip(ids.flatten(), corners, strict=True)
        ]

    return scan_aruco


def annotate(frame: np.ndarray, found: list, expected: str) -> np.ndarray:
    """Draw every decoded symbol's quad, green for the bottle being scanned"""
    out = frame.copy()
    for _, corners, row in found:
        if corners is None:
            continue
        hit = row is not None and row["sample_id"] == expected
        quad = corners.astype(np.int32).reshape(-1, 1, 2)
        cv2.polylines(out, [quad], True, GREEN if hit else AMBER, 4, cv2.LINE_AA)
    return out


def tile(frame: np.ndarray, scan: Scan) -> np.ndarray:
    """Compose one contact-sheet cell: the frame, a 1:1 crop and the result"""
    height, width = frame.shape[:2]
    cell = np.full((TILE_H + CAPTION_H, TILE_W + INSET, 3), 255, np.uint8)
    cell[:TILE_H, :TILE_W] = cv2.resize(
        frame, (TILE_W, TILE_H), interpolation=cv2.INTER_AREA
    )
    x0, y0 = (width - INSET) // 2, (height - INSET) // 2
    cell[:INSET, TILE_W:] = frame[y0 : y0 + INSET, x0 : x0 + INSET]
    cv2.rectangle(cell, (TILE_W, 0), (TILE_W + INSET - 1, INSET - 1), INK, 1)
    colour = {"ok": GREEN, "wrong": RED, "no read": AMBER}[scan.verdict]
    if scan.verdict == "ok":
        result = f"READ {scan.code} -> {scan.read_as}  OK"
    elif scan.verdict == "wrong":
        result = f"READ {scan.code} -> {scan.read_as}  WRONG"
    else:
        result = "NO READ at " + ", ".join(f"{d:.2f}" for d in scan.tried_m) + " m"
    size = f"{scan.container_ml:g} ml"
    lines = [
        (f"{scan.sample_id}  {scan.material}, {size}  ({scan.where})", INK),
        (
            f"standoff {scan.standoff_m:.2f} m"
            + (f" from {scan.elevation_deg:g} deg above" if scan.elevation_deg else "")
            + f"   {scan.px_per_module:.1f} px/module"
            + (f"   also read: {', '.join(scan.others)}" if scan.others else ""),
            INK,
        ),
        (result, colour),
    ]
    for row, (text, ink) in enumerate(lines):
        cv2.putText(
            cell,
            text,
            (8, TILE_H + 24 + 26 * row),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.62,
            ink,
            2 if row == 2 else 1,
            cv2.LINE_AA,
        )
    cv2.rectangle(cell, (0, 0), (cell.shape[1] - 1, cell.shape[0] - 1), colour, 3)
    return cell


def contact_sheet(cells: list[np.ndarray]) -> np.ndarray:
    """Lay the cells out in rows of :data:`COLUMNS` on white"""
    rows = math.ceil(len(cells) / COLUMNS)
    cell_h, cell_w = cells[0].shape[:2]
    sheet = np.full((rows * cell_h, COLUMNS * cell_w, 3), 255, np.uint8)
    for i, cell in enumerate(cells):
        r, c = divmod(i, COLUMNS)
        sheet[r * cell_h : (r + 1) * cell_h, c * cell_w : (c + 1) * cell_w] = cell
    return sheet


def main() -> None:
    """Scan the chosen bottles and write frames, contact sheet and results"""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--scene", type=Path, default=SCENE)
    parser.add_argument(
        "--samples",
        nargs="*",
        default=None,
        help="sample ids to scan (default: every hand-placed bottle)",
    )
    parser.add_argument(
        "--shelf",
        type=int,
        default=7,
        help="how many shelved bottles to add, drawn by --seed",
    )
    parser.add_argument("--seed", type=int, default=3)
    parser.add_argument("--approach", choices=("label", "aisle"), default="label")
    parser.add_argument("--symbology", choices=("auto", "ean", "aruco"), default="auto")
    parser.add_argument(
        "--standoffs", type=float, nargs="+", default=DEFAULT_STANDOFFS_M
    )
    parser.add_argument(
        "--out", type=Path, default=REPO / "simulation" / "out" / "wrist_scan"
    )
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    table = registry.load_table(TABLE)
    by_id = {row["sample_id"]: row for row in table.values()}
    manifest = json.loads(MANIFEST.read_text())
    symbology = args.symbology
    if symbology == "auto":
        symbology = "aruco" if manifest.get("label") == "aruco_ring" else "ean"
    scan_frame = make_scanner(symbology, table)
    entries = {
        e.sample.sample_id: e
        for e in registry.build_registry(registry.default_samples())
    }

    model = mujoco.MjModel.from_xml_path(str(args.scene))
    data = mujoco.MjData(model)
    for _ in range(SETTLE_STEPS):
        mujoco.mj_step(model, data)
    mujoco.mj_forward(model, data)
    camera = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, "wrist")
    width, height = (int(v) for v in model.cam_resolution[camera])
    focal_px = height / 2.0 / math.tan(math.radians(model.cam_fovy[camera]) / 2.0)
    renderer = mujoco.Renderer(model, height=height, width=width)

    targets = find_targets(model, data)
    chosen = args.samples
    if chosen is None:
        chosen = sorted(t.sample_id for t in targets.values() if t.where != "shelf")
    shelved = sorted(t.sample_id for t in targets.values() if t.where == "shelf")
    rng = np.random.default_rng(args.seed)
    chosen = list(chosen) + [
        str(s) for s in rng.choice(shelved, args.shelf, replace=False)
    ]

    scans, cells = [], []
    for sample_id in chosen:
        target, row = targets[sample_id], by_id[sample_id]
        if symbology == "aruco":
            modules = ARUCO_MODULES
        else:
            label = registry.render_label(entries[sample_id], module_px=2)
            modules = label.shape[1] / 2
        module_m = target.label_height_m / modules
        if args.approach == "aisle" or target.normal is None:
            radius = manifest["vessels"][row["vessel_class"]]["diameter_m"] / 2.0
            target = from_aisle(target, radius)
        tried = []
        approaches = [(e, d) for e in ELEVATIONS_DEG for d in args.standoffs]
        for elevation, standoff in approaches:
            if elevation == 0.0:
                tried.append(standoff)
            park(model, data, camera, target, standoff, elevation)
            renderer.update_scene(data, camera=camera)
            frame = cv2.cvtColor(renderer.render(), cv2.COLOR_RGB2BGR)
            found = scan_frame(frame)
            mine = [
                c for c, _, r in found if r is not None and r["sample_id"] == sample_id
            ]
            if mine:
                break
        # A code that is in the table but is not this bottle's belongs to a neighbour
        # in shot. A code that is in no table at all is a misread.
        others = sorted(
            {r["sample_id"] for _, _, r in found if r is not None} - {sample_id}
        )
        unknown = [c for c, _, r in found if r is None]
        if mine:
            code, read_as, verdict = mine[0], sample_id, "ok"
            others += [f"unknown {c}" for c in unknown]
        elif unknown:
            code, read_as, verdict = unknown[0], "not in the table", "wrong"
        else:
            code, read_as, verdict = None, None, "no read"
        scan = Scan(
            sample_id,
            row["material"],
            row["container_ml"],
            target.where,
            standoff,
            elevation,
            focal_px * module_m / standoff,
            tried,
            code,
            read_as,
            others,
            verdict,
        )
        scans.append(scan)
        shown = annotate(frame, found, sample_id)
        cv2.imwrite(str(args.out / f"{sample_id}.png"), shown)
        cells.append(tile(shown, scan))
        print(
            f"{sample_id:9s} {row['material'][:22]:22s} {row['container_ml']:6g} ml "
            f"{target.where:6s} {standoff:.2f} m {elevation:2g} deg "
            f"{scan.px_per_module:4.1f} px/mod  "
            f"{verdict}{'  also ' + ','.join(others) if others else ''}"
        )

    cv2.imwrite(str(args.out / "contact_sheet.png"), contact_sheet(cells))
    (args.out / "results.json").write_text(
        json.dumps([asdict(s) for s in scans], indent=1), encoding="utf-8"
    )
    ok = sum(s.verdict == "ok" for s in scans)
    print(
        f"\n{ok}/{len(scans)} read correctly, "
        f"{sum(s.verdict == 'wrong' for s in scans)} misread -> {args.out}"
    )


if __name__ == "__main__":
    main()
