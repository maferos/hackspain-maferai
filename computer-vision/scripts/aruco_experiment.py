"""Measure an ArUco marker against the EAN-13 label on the same bottles

EAN-13 spends 113 modules along one axis, so on a 10 ml flask a module is
0.2 mm and the wrist camera has to come within 0.10 m. An ArUco marker from
``DICT_4X4_250`` is 8 modules a side with its quiet zone and has 250 ids, which
covers the 200 samples. This script measures what that buys, in MuJoCo, through
the same GoPro Linear 1080p pinhole as the scene's cameras, on all ten bottle
sizes:

1. **Distance.** The farthest the camera can stand, square on, and still read.
2. **Bottle turned.** How far the bottle can be turned about its own axis, so
   the marker slides round towards the silhouette, before the read is lost.
3. **Camera rolled.** Whether the read survives the camera being rolled about
   its optical axis, which is the in-plane orientation of the marker.

The marker goes where the EAN-13 label is, on the same straight wall, as large
a square as the wall height and 90 degrees of arc allow. Nothing committed is
touched: meshes come from ``simulation/assets/labelled_bottles`` and the markers
are written to the output folder.

    python scripts/aruco_experiment.py
    python scripts/aruco_experiment.py --vessels flask_10ml bottle_2000ml

Output: ``results.json``, ``results.md`` and ``contact_sheet.png`` in
``simulation/out/aruco_experiment/``. Needs ``mujoco``.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import cv2
import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labvision import reader, registry  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
KIT = REPO / "simulation" / "assets" / "labelled_bottles"
TABLE = REPO / "computer-vision" / "barcodes" / "lookup_table.json"

WIDTH, HEIGHT, FOVY_DEG = 1920, 1080, 60.44
"""The scene's cameras: a GoPro in Linear mode at 1080p."""

DICTIONARY = cv2.aruco.DICT_4X4_250
MARKER_MODULES = 6
QUIET_MODULES = 1
TEXTURE_MODULE_PX = 32
MAX_ARC_DEG = 90.0
ARC_SEGMENTS = 32
LABEL_OFFSET_M = 0.0002

DISTANCES_M = (
    0.10,
    0.15,
    0.20,
    0.30,
    0.40,
    0.50,
    0.75,
    1.0,
    1.5,
    2.0,
    2.5,
    3.0,
    4.0,
    5.0,
)
YAWS_DEG = (0, 10, 20, 30, 40, 50, 60, 70, 80)
ROLLS_DEG = (0, 30, 45, 90, 135, 180, 270)
PARKED = (0.0, 0.0, -10.0)
"""Where the bottles that are not being looked at wait, under the floor."""

CROP = 300
GREEN, AMBER, INK = (60, 150, 40), (0, 130, 230), (30, 30, 30)


def label_wall(vessel: str) -> tuple[float, float, float]:
    """Radius and height range of the EAN-13 sticker, which sits on the straight wall

    Args:
        vessel: Vessel class, such as ``flask_10ml``.

    Returns:
        ``(radius, z_low, z_high)`` in metres, in the bottle's own frame.
    """
    rows = [
        line.split()[1:4]
        for line in (KIT / "meshes" / f"{vessel}_label.obj").read_text().splitlines()
        if line.startswith("v ")
    ]
    vertices = np.array(rows, dtype=float)
    radius = float(np.median(np.hypot(vertices[:, 0], vertices[:, 1])))
    return radius, float(vertices[:, 2].min()), float(vertices[:, 2].max())


def write_marker(
    vessel: str,
    marker_id: int,
    out: Path,
    max_arc_deg: float = MAX_ARC_DEG,
) -> tuple[Path, Path, float]:
    """Write a curved ArUco sticker for one vessel, facing -Y like the EAN-13 label

    Args:
        vessel: Vessel class the sticker is cut for.
        marker_id: Id within :data:`DICTIONARY`.
        out: Folder for the OBJ and the PNG.
        max_arc_deg: Most of the bottle's circumference the sticker may span.

    Returns:
        The OBJ path, the PNG path and the printed width of one module in metres.
    """
    radius, z_low, z_high = label_wall(vessel)
    side = min(z_high - z_low, radius * math.radians(max_arc_deg))
    arc = side / radius
    z_mid = (z_low + z_high) / 2.0
    total = MARKER_MODULES + 2 * QUIET_MODULES

    dictionary = cv2.aruco.getPredefinedDictionary(DICTIONARY)
    marker = cv2.aruco.generateImageMarker(
        dictionary, marker_id, MARKER_MODULES * TEXTURE_MODULE_PX
    )
    pad = QUIET_MODULES * TEXTURE_MODULE_PX
    image = cv2.copyMakeBorder(
        marker, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=255
    )
    png = out / f"aruco_{vessel}.png"
    cv2.imwrite(str(png), image)

    # Seen from outside, facing the label, image-right is +X. OBJ puts v = 0 at the
    # bottom of the image. A mirrored ArUco marker is a different marker, so the
    # experiment checks the id it reads back.
    lines = []
    r = radius + LABEL_OFFSET_M
    for i in range(ARC_SEGMENTS + 1):
        theta = -arc / 2.0 + arc * i / ARC_SEGMENTS
        for z in (z_mid - side / 2.0, z_mid + side / 2.0):
            lines.append(
                f"v {r * math.sin(theta):.6f} {-r * math.cos(theta):.6f} {z:.6f}"
            )
    for i in range(ARC_SEGMENTS + 1):
        for v in (0.0, 1.0):
            lines.append(f"vt {i / ARC_SEGMENTS:.6f} {v:.6f}")
    for i in range(ARC_SEGMENTS):
        a, b, c, d = 2 * i + 1, 2 * i + 2, 2 * i + 3, 2 * i + 4
        lines.append(f"f {a}/{a} {c}/{c} {d}/{d}")
        lines.append(f"f {a}/{a} {d}/{d} {b}/{b}")
    obj = out / f"aruco_{vessel}.obj"
    obj.write_text("\n".join(lines) + "\n")
    return obj, png, side / total


def build_scene(
    vessels: list[str],
    manifest: dict,
    out: Path,
    max_arc_deg: float = MAX_ARC_DEG,
) -> tuple[str, dict]:
    """Compose one MJCF holding an EAN-13 and an ArUco bottle per vessel, all parked

    Args:
        vessels: Vessel classes to include.
        manifest: ``labelled_bottles/manifest.json``.
        out: Folder the marker files are written to.
        max_arc_deg: Most of the circumference an ArUco sticker may span.

    Returns:
        The MJCF text and, per vessel, what the experiment needs to know about it.
    """
    assets, bodies, info = [], [], {}
    for index, vessel in enumerate(vessels):
        spec = manifest["vessels"][vessel]
        sample_id = next(
            s
            for s, row in sorted(manifest["samples"].items())
            if row["vessel_class"] == vessel
        )
        marker_id = (index * 23 + 5) % 250
        obj, png, aruco_module = write_marker(vessel, marker_id, out, max_arc_deg)
        radius, z_low, z_high = label_wall(vessel)
        parts = {
            p: rgba for p, rgba in spec["parts"].items() if not p.startswith("label")
        }
        for part in parts:
            assets.append(
                f'<mesh name="{vessel}_{part}" inertia="exact" '
                f'file="{KIT / "meshes" / f"{vessel}_{part}.obj"}"/>'
            )
        assets += [
            f'<mesh name="{vessel}_ean" inertia="shell" '
            f'file="{KIT / "meshes" / f"{vessel}_label.obj"}"/>',
            f'<texture name="{vessel}_ean" type="2d" '
            f'file="{KIT / "textures" / f"{sample_id}.png"}"/>',
            f'<material name="{vessel}_ean" texture="{vessel}_ean" specular="0.05"/>',
            f'<mesh name="{vessel}_aruco" inertia="shell" file="{obj}"/>',
            f'<texture name="{vessel}_aruco" type="2d" file="{png}"/>',
            f'<material name="{vessel}_aruco" texture="{vessel}_aruco" '
            f'specular="0.05"/>',
        ]
        for kind in ("ean", "aruco"):
            geoms = [
                f'<geom type="mesh" mesh="{vessel}_{part}" contype="0" conaffinity="0" '
                f'rgba="{" ".join(f"{c:.3f}" for c in rgba)}"/>'
                for part, rgba in parts.items()
            ]
            geoms.append(
                f'<geom type="mesh" mesh="{vessel}_{kind}" material="{vessel}_{kind}" '
                f'contype="0" conaffinity="0"/>'
            )
            bodies.append(
                f'<body name="{kind}_{vessel}" mocap="true" '
                f'pos="{PARKED[0]} {PARKED[1]} {PARKED[2]}">{"".join(geoms)}</body>'
            )
        ean_png = cv2.imread(str(KIT / "textures" / f"{sample_id}.png"))
        ean_module = (z_high - z_low) / (
            ean_png.shape[1] / 8.0
        )  # textures are 8 px/module
        info[vessel] = {
            "sample_id": sample_id,
            "marker_id": marker_id,
            "radius_m": radius,
            "label_z_m": (z_low + z_high) / 2.0,
            "module_mm": {"ean": ean_module * 1000.0, "aruco": aruco_module * 1000.0},
            "aruco_arc_deg": math.degrees(aruco_module * 8 / radius),
        }
    xml = f"""<mujoco model="aruco_experiment">
  <visual>
    <headlight diffuse="0.5 0.5 0.5" ambient="0.45 0.45 0.45" specular="0 0 0"/>
    <global offwidth="{WIDTH}" offheight="{HEIGHT}"/>
    <map znear="0.002"/>
  </visual>
  <asset>
    {" ".join(assets)}
  </asset>
  <worldbody>
    <light pos="0 -2 3" dir="0 0.5 -1" diffuse="0.5 0.5 0.5"/>
    <geom type="plane" size="20 20 0.1" rgba="0.80 0.81 0.82 1"/>
    <geom type="box" pos="0 1.5 1.5" size="20 0.05 1.5" rgba="0.72 0.74 0.76 1"/>
    {" ".join(bodies)}
    <body name="mount" mocap="true" pos="0 -1 1">
      <camera name="gopro" fovy="{FOVY_DEG}" resolution="{WIDTH} {HEIGHT}"/>
    </body>
  </worldbody>
</mujoco>"""
    return xml, info


class Rig:
    """The compiled experiment: shows one bottle at a time and photographs it."""

    def __init__(self, xml: str) -> None:
        """Compile the scene and set up the renderer

        Args:
            xml: MJCF text from :func:`build_scene`.
        """
        self.model = mujoco.MjModel.from_xml_string(xml)
        self.data = mujoco.MjData(self.model)
        self.renderer = mujoco.Renderer(self.model, height=HEIGHT, width=WIDTH)

    def _mocap(self, body: str) -> int:
        """Mocap index of a named body"""
        return self.model.body_mocapid[
            mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, body)
        ]

    def shoot(
        self,
        body: str,
        radius: float,
        label_z: float,
        distance: float,
        yaw_deg: float = 0.0,
        roll_deg: float = 0.0,
    ) -> np.ndarray:
        """Stand one bottle at the origin and photograph its label

        Args:
            body: The bottle's body name; every other bottle stays parked.
            radius: Bottle radius, so distance is measured from the label.
            label_z: Height of the label's centre.
            distance: Label-to-camera distance in metres.
            yaw_deg: Turn of the bottle about its axis; 0 faces the camera.
            roll_deg: Roll of the camera about its optical axis.

        Returns:
            The BGR frame.
        """
        for i in range(self.model.nmocap):
            self.data.mocap_pos[i] = PARKED
        bottle = self._mocap(body)
        half = math.radians(yaw_deg) / 2.0
        self.data.mocap_pos[bottle] = (0.0, 0.0, 0.0)
        self.data.mocap_quat[bottle] = (math.cos(half), 0.0, 0.0, math.sin(half))

        roll = math.radians(roll_deg)
        right = np.array([math.cos(roll), 0.0, math.sin(roll)])
        up = np.array([-math.sin(roll), 0.0, math.cos(roll)])
        backward = np.array([0.0, -1.0, 0.0])  # the camera looks along +Y, down its -Z
        quat = np.zeros(4)
        mujoco.mju_mat2Quat(quat, np.column_stack([right, up, backward]).flatten())
        mount = self._mocap("mount")
        self.data.mocap_pos[mount] = (0.0, -(radius + distance), label_z)
        self.data.mocap_quat[mount] = quat
        mujoco.mj_forward(self.model, self.data)
        self.renderer.update_scene(self.data, camera="gopro")
        return cv2.cvtColor(self.renderer.render(), cv2.COLOR_RGB2BGR)


def make_readers(table: dict) -> dict:
    """Build one ``frame -> (ids read, outlines)`` function per symbology"""
    parameters = cv2.aruco.DetectorParameters()
    parameters.minMarkerPerimeterRate = 0.02
    parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    detector = cv2.aruco.ArucoDetector(
        cv2.aruco.getPredefinedDictionary(DICTIONARY), parameters
    )

    def read_aruco(frame: np.ndarray) -> tuple[list, list]:
        corners, ids, _ = detector.detectMarkers(frame)
        found = [] if ids is None else [int(i) for i in ids.flatten()]
        return found, [c.reshape(4, 2) for c in corners]

    def read_ean(frame: np.ndarray) -> tuple[list, list]:
        found = reader.resolve(reader.decode_image(frame), table)
        ids = [row["sample_id"] if row else f"?{d.code}" for d, row in found]
        return ids, [d.corners for d, _ in found if d.corners is not None]

    return {"aruco": read_aruco, "ean": read_ean}


def farthest(flags: list[bool], values: tuple) -> float | None:
    """Last value of the first unbroken run of reads, or None if nothing read"""
    best, started = None, False
    for flag, value in zip(flags, values, strict=True):
        if flag:
            best, started = value, True
        elif started:
            break
    return best


def main() -> None:
    """Run the three sweeps on every vessel and write the results"""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--vessels", nargs="*", default=None)
    parser.add_argument(
        "--arc",
        type=float,
        default=MAX_ARC_DEG,
        help="most arc an ArUco sticker may span, in degrees",
    )
    parser.add_argument(
        "--only",
        choices=("aruco", "ean"),
        default=None,
        help="measure one symbology only",
    )
    parser.add_argument(
        "--out", type=Path, default=REPO / "simulation" / "out" / "aruco_experiment"
    )
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    manifest = json.loads((KIT / "manifest.json").read_text())
    vessels = args.vessels or sorted(
        manifest["vessels"],
        key=lambda v: (
            manifest["vessels"][v]["phase"],
            manifest["vessels"][v]["container_ml"],
        ),
    )
    xml, info = build_scene(vessels, manifest, args.out, args.arc)
    rig = Rig(xml)
    readers = make_readers(registry.load_table(TABLE))
    if args.only:
        readers = {args.only: readers[args.only]}
    focal_px = HEIGHT / 2.0 / math.tan(math.radians(FOVY_DEG) / 2.0)

    results, cells, wrong = {}, [], 0
    for vessel in vessels:
        meta = info[vessel]
        expected = {"aruco": meta["marker_id"], "ean": meta["sample_id"]}
        results[vessel] = {
            "module_mm": meta["module_mm"],
            "aruco_arc_deg": meta["aruco_arc_deg"],
        }
        row_cells = []
        for kind, read in readers.items():
            body = f"{kind}_{vessel}"

            def reads(
                kind=kind, read=read, body=body, meta=meta, expected=expected,
                **pose: float,
            ) -> bool:
                nonlocal wrong
                frame = rig.shoot(body, meta["radius_m"], meta["label_z_m"], **pose)
                ids, _ = read(frame)
                wrong += sum(i != expected[kind] for i in ids)
                return expected[kind] in ids

            by_distance = [reads(distance=d) for d in DISTANCES_M]
            reach = farthest(by_distance, DISTANCES_M)
            entry = {"max_distance_m": reach, "max_yaw_deg": None, "rolls_read_deg": []}
            if reach is not None:
                # Half the reach, so the sweeps measure angle and not resolution.
                near = max(reach / 2.0, DISTANCES_M[0])
                entry["sweep_distance_m"] = near
                by_yaw = [reads(distance=near, yaw_deg=y) for y in YAWS_DEG]
                entry["max_yaw_deg"] = farthest(by_yaw, YAWS_DEG)
                entry["rolls_read_deg"] = [
                    r for r in ROLLS_DEG if reads(distance=near, roll_deg=r)
                ]
                entry["px_per_module_at_max"] = (
                    focal_px * meta["module_mm"][kind] / 1000.0 / reach
                )
                frame = rig.shoot(
                    body, meta["radius_m"], meta["label_z_m"], distance=reach
                )
                _, outlines = read(frame)
                for quad in outlines:
                    cv2.polylines(
                        frame, [quad.astype(np.int32).reshape(-1, 1, 2)], True, GREEN, 2
                    )
                y0, x0 = (HEIGHT - CROP) // 2, (WIDTH - CROP) // 2
                crop = frame[y0 : y0 + CROP, x0 : x0 + CROP]
            else:
                crop = np.full((CROP, CROP, 3), 235, np.uint8)
            results[vessel][kind] = entry
            cell = np.full((CROP + 56, CROP, 3), 255, np.uint8)
            cell[:CROP] = crop
            text = "no read" if reach is None else f"reads to {reach:g} m"
            cv2.putText(
                cell,
                f"{vessel} {kind.upper()}",
                (6, CROP + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                INK,
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                cell,
                text,
                (6, CROP + 44),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                GREEN if reach else AMBER,
                2,
                cv2.LINE_AA,
            )
            row_cells.append(cell)
            print(
                f"{vessel:14s} {kind:5s} module {meta['module_mm'][kind]:5.2f} mm  "
                f"reach {reach} m  yaw {entry['max_yaw_deg']} deg  "
                f"rolls {entry['rolls_read_deg']}",
                flush=True,
            )
        cells.append(np.hstack(row_cells))

    half = math.ceil(len(cells) / 2)
    columns = (
        [np.vstack(cells[:half]), np.vstack(cells[half:])] if len(cells) > 1 else cells
    )
    height = max(c.shape[0] for c in columns)
    columns = [
        cv2.copyMakeBorder(
            c, 0, height - c.shape[0], 0, 12, cv2.BORDER_CONSTANT, value=(255, 255, 255)
        )
        for c in columns
    ]
    cv2.imwrite(str(args.out / "contact_sheet.png"), np.hstack(columns))

    (args.out / "results.json").write_text(
        json.dumps(results, indent=1), encoding="utf-8"
    )
    lines = [
        "| Vessel | EAN module | ArUco module | EAN reads to | ArUco reads to | "
        "EAN max turn | ArUco max turn | ArUco rolls read |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for vessel in vessels:
        r = results[vessel]
        blank = {"max_distance_m": "-", "max_yaw_deg": "-", "rolls_read_deg": []}
        r = {"ean": blank, "aruco": blank, **r}
        lines.append(
            f"| {vessel} | {r['module_mm']['ean']:.2f} mm "
            f"| {r['module_mm']['aruco']:.2f} mm "
            f"| {r['ean']['max_distance_m']} m | {r['aruco']['max_distance_m']} m "
            f"| {r['ean']['max_yaw_deg']} deg | {r['aruco']['max_yaw_deg']} deg "
            f"| {len(r['aruco']['rolls_read_deg'])}/{len(ROLLS_DEG)} |"
        )
    (args.out / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n" + "\n".join(lines))
    print(f"\nids read that were not the bottle's own: {wrong} -> {args.out}")


if __name__ == "__main__":
    main()
