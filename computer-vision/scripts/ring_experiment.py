"""Labels that go all the way round the bottle, against the ones that do not

A bottle put down by hand faces wherever it faces, and a label on one side is
invisible from the other. Two labels do not have a side:

``ean_ring``
    The EAN-13 in ladder orientation already has bars that run round the
    bottle. Stretch them to 360 degrees and every bar is a full ring: the same
    symbol, the same module size, readable from anywhere. It is read by taking
    a vertical strip down the middle of the bottle's box and handing it to
    :func:`labvision.reader.decode_scanline` --- no localiser, because there is
    nothing to localise: the code is the bottle.

``aruco_ring``
    Eight copies of one ``DICT_4X4_250`` marker, one every 45 degrees. A single
    marker is lost 10 to 20 degrees off square (``aruco_experiment.py``), so the
    copies are narrow and close together.

They are measured against the two one-sided labels, ``ean`` (what the bottles
carry today) and ``aruco`` (one marker over 90 degrees of arc), on every bottle
size, through the scene's 1080p GoPro pinhole:

1. **Reach**: the farthest the camera reads from, facing the label squarely.
2. **Coverage at half the reach**: the share of bottle orientations, every 15
   degrees round the full turn, that read --- angle alone, resolution to spare.
3. **Coverage at 0.30 m**: the same from a GoPro's near focus, which is what an
   arm that does not know how the bottle is turned would actually get.

Each frame is cropped to the bottle, as a detector's box would, before reading.

    python scripts/ring_experiment.py
    python scripts/ring_experiment.py --vessels flask_10ml bottle_2000ml
    python scripts/ring_experiment.py --plot-only

Output: ``results.json`` and ``comparison.png`` in
``simulation/out/ring_experiment/``. Needs ``mujoco`` and ``matplotlib``.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aruco_experiment import (  # noqa: E402
    DICTIONARY,
    DISTANCES_M,
    FOVY_DEG,
    HEIGHT,
    KIT,
    LABEL_OFFSET_M,
    PARKED,
    REPO,
    TABLE,
    WIDTH,
    Rig,
    farthest,
    label_wall,
)

from labvision import ean13, reader, registry  # noqa: E402

KINDS = ("ean", "ean_ring", "aruco", "aruco_ring")
TITLES = {
    "ean": "EAN-13, one side (today)",
    "ean_ring": "EAN-13 ring, 360 deg",
    "aruco": "ArUco, one side",
    "aruco_ring": "ArUco ring, 8 copies",
}
COLOURS = {
    "ean": "#9aa0a6",
    "ean_ring": "#1a73e8",
    "aruco": "#f6b26b",
    "aruco_ring": "#e8710a",
}
YAWS_DEG = tuple(range(0, 360, 15))
NEAR_FOCUS_M = 0.30
RING_COPIES = 8
ARUCO_SIDE_ARC_DEG = 90.0
MODULE_PX = 16
FOCAL_PX = HEIGHT / 2.0 / math.tan(math.radians(FOVY_DEG) / 2.0)


def write_patch(
    name: str,
    image: np.ndarray,
    radius: float,
    z_mid: float,
    height: float,
    arc_rad: float,
    out: Path,
) -> tuple[Path, Path]:
    """Write a sticker curved round the bottle, centred on -Y, with its texture

    Args:
        name: File stem.
        image: The texture; its width goes round the bottle, its height up it.
        radius: Bottle radius at the wall.
        z_mid: Height of the sticker's centre.
        height: Extent of the sticker up the bottle.
        arc_rad: Angle it spans, up to a full turn.
        out: Folder to write into.

    Returns:
        The OBJ path and the PNG path.
    """
    png = out / f"{name}.png"
    cv2.imwrite(str(png), image)
    segments = max(16, int(round(96 * arc_rad / (2.0 * math.pi))))
    r = radius + LABEL_OFFSET_M
    lines = []
    for i in range(segments + 1):
        theta = -arc_rad / 2.0 + arc_rad * i / segments
        for z in (z_mid - height / 2.0, z_mid + height / 2.0):
            lines.append(
                f"v {r * math.sin(theta):.6f} {-r * math.cos(theta):.6f} {z:.6f}"
            )
    for i in range(segments + 1):
        for v in (0.0, 1.0):
            lines.append(f"vt {i / segments:.6f} {v:.6f}")
    for i in range(segments):
        a, b, c, d = 2 * i + 1, 2 * i + 2, 2 * i + 3, 2 * i + 4
        lines.append(f"f {a}/{a} {c}/{c} {d}/{d}")
        lines.append(f"f {a}/{a} {d}/{d} {b}/{b}")
    obj = out / f"{name}.obj"
    obj.write_text("\n".join(lines) + "\n")
    return obj, png


def ring_of_bars(code: str, total_modules: int) -> np.ndarray:
    """Texture of an EAN-13 whose bars are rings: modules stacked up the image

    Args:
        code: The 13-digit code.
        total_modules: Modules the sticker's height is divided into, quiet
            zones included, so the module matches the one-sided label's.

    Returns:
        A greyscale image, one module per :data:`MODULE_PX` rows.
    """
    modules = ean13.encode_modules(code)
    quiet = total_modules - len(modules)
    column = "0" * (quiet // 2) + modules + "0" * (quiet - quiet // 2)
    rows = np.array([0 if m == "1" else 255 for m in column], dtype=np.uint8)
    return np.repeat(np.repeat(rows[:, None], MODULE_PX, axis=0), MODULE_PX * 4, axis=1)


def aruco_image(marker_id: int, copies: int) -> np.ndarray:
    """Texture of one or more copies of a marker, each with a one-module quiet zone"""
    dictionary = cv2.aruco.getPredefinedDictionary(DICTIONARY)
    marker = cv2.aruco.generateImageMarker(dictionary, marker_id, 6 * MODULE_PX * 2)
    pad = MODULE_PX * 2
    cell = cv2.copyMakeBorder(
        marker, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=255
    )
    return np.hstack([cell] * copies)


def build_scene(vessels: list[str], manifest: dict, out: Path) -> tuple[str, dict]:
    """Compose one MJCF with four differently labelled copies of every vessel

    Args:
        vessels: Vessel classes to include.
        manifest: ``labelled_bottles/manifest.json``.
        out: Folder the generated stickers are written to.

    Returns:
        The MJCF text and, per vessel, the facts the sweeps need.
    """
    table = registry.load_table(TABLE)
    code_of = {row["sample_id"]: code for code, row in table.items()}
    assets, bodies, info = [], [], {}
    for index, vessel in enumerate(vessels):
        spec = manifest["vessels"][vessel]
        sample_id = next(
            s
            for s, row in sorted(manifest["samples"].items())
            if row["vessel_class"] == vessel
        )
        marker_id = (index * 23 + 5) % 250
        radius, z_low, z_high = label_wall(vessel)
        wall, z_mid = z_high - z_low, (z_low + z_high) / 2.0
        ean_png = cv2.imread(str(KIT / "textures" / f"{sample_id}.png"))
        ean_modules = ean_png.shape[1] // 8  # the kit's textures are 8 px per module

        side_one = min(wall, radius * math.radians(ARUCO_SIDE_ARC_DEG))
        side_ring = min(wall, radius * 2.0 * math.pi / RING_COPIES)
        stickers = {
            "ean_ring": write_patch(
                f"{vessel}_ean_ring",
                ring_of_bars(code_of[sample_id], ean_modules),
                radius,
                z_mid,
                wall,
                2.0 * math.pi,
                out,
            ),
            "aruco": write_patch(
                f"{vessel}_aruco",
                aruco_image(marker_id, 1),
                radius,
                z_mid,
                side_one,
                side_one / radius,
                out,
            ),
            "aruco_ring": write_patch(
                f"{vessel}_aruco_ring",
                aruco_image(marker_id, RING_COPIES),
                radius,
                z_mid,
                side_ring,
                2.0 * math.pi,
                out,
            ),
            "ean": (
                KIT / "meshes" / f"{vessel}_label.obj",
                KIT / "textures" / f"{sample_id}.png",
            ),
        }
        parts = {p: c for p, c in spec["parts"].items() if not p.startswith("label")}
        for part in parts:
            assets.append(
                f'<mesh name="{vessel}_{part}" inertia="exact" '
                f'file="{KIT / "meshes" / f"{vessel}_{part}.obj"}"/>'
            )
        for kind, (obj, png) in stickers.items():
            assets += [
                f'<mesh name="{vessel}_{kind}" inertia="shell" file="{obj}"/>',
                f'<texture name="{vessel}_{kind}" type="2d" file="{png}"/>',
                f'<material name="{vessel}_{kind}" texture="{vessel}_{kind}" '
                f'specular="0.05"/>',
            ]
            geoms = [
                f'<geom type="mesh" mesh="{vessel}_{part}" contype="0" conaffinity="0" '
                f'rgba="{" ".join(f"{c:.3f}" for c in rgba)}"/>'
                for part, rgba in parts.items()
            ]
            geoms.append(
                f'<geom type="mesh" mesh="{vessel}_{kind}" '
                f'material="{vessel}_{kind}" contype="0" conaffinity="0"/>'
            )
            bodies.append(
                f'<body name="{kind}_{vessel}" mocap="true" '
                f'pos="{PARKED[0]} {PARKED[1]} {PARKED[2]}">{"".join(geoms)}</body>'
            )
        info[vessel] = {
            "sample_id": sample_id,
            "marker_id": marker_id,
            "radius_m": radius,
            "label_z_m": z_mid,
            "height_m": spec["height_m"],
            "container_ml": spec["container_ml"],
            "phase": spec["phase"],
            "module_mm": {
                "ean": wall / ean_modules * 1000.0,
                "ean_ring": wall / ean_modules * 1000.0,
                "aruco": side_one / 8.0 * 1000.0,
                "aruco_ring": side_ring / 8.0 * 1000.0,
            },
        }
    xml = f"""<mujoco model="ring_experiment">
  <visual>
    <headlight diffuse="0.5 0.5 0.5" ambient="0.45 0.45 0.45" specular="0 0 0"/>
    <global offwidth="{WIDTH}" offheight="{HEIGHT}"/>
    <map znear="0.002"/>
  </visual>
  <asset>{" ".join(assets)}</asset>
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


def bottle_box(frame: np.ndarray, meta: dict, distance: float) -> np.ndarray:
    """Crop the frame to the bottle with a margin, as a detector's box would"""
    depth = distance + meta["radius_m"]
    half_w = int(
        np.clip(FOCAL_PX * 1.6 * meta["radius_m"] / depth + 24, 60, WIDTH // 2)
    )
    half_h = int(
        np.clip(FOCAL_PX * 0.8 * meta["height_m"] / depth + 24, 60, HEIGHT // 2)
    )
    cy, cx = HEIGHT // 2, WIDTH // 2
    return frame[cy - half_h : cy + half_h, cx - half_w : cx + half_w]


def make_readers(table: dict) -> dict:
    """One ``(crop, meta, distance) -> set of ids`` function per kind of label"""
    parameters = cv2.aruco.DetectorParameters()
    parameters.minMarkerPerimeterRate = 0.02
    parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    detector = cv2.aruco.ArucoDetector(
        cv2.aruco.getPredefinedDictionary(DICTIONARY), parameters
    )

    def sample_of(code: str | None) -> set:
        row = table.get(code) if code else None
        return {row["sample_id"]} if row else set()

    def read_aruco(crop: np.ndarray, meta: dict, distance: float) -> set:
        _, ids, _ = detector.detectMarkers(crop)
        return set() if ids is None else {int(i) for i in ids.flatten()}

    def read_ean(crop: np.ndarray, meta: dict, distance: float) -> set:
        found = reader.resolve(reader.decode_image(crop), table)
        return {row["sample_id"] for _, row in found if row}

    def read_ean_ring(crop: np.ndarray, meta: dict, distance: float) -> set:
        # The bars are rings, so the middle of the bottle is a rectified barcode
        # standing on end: take a strip a third of the bottle wide and lay it down.
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        half = max(
            3, int(FOCAL_PX * meta["radius_m"] / (distance + meta["radius_m"]) / 3)
        )
        middle = gray.shape[1] // 2
        strip = cv2.rotate(
            gray[:, middle - half : middle + half], cv2.ROTATE_90_CLOCKWISE
        )
        for scale in (1, 2, 3):
            image = (
                strip
                if scale == 1
                else cv2.resize(
                    strip, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC
                )
            )
            ids = sample_of(reader.decode_scanline(image))
            if ids:
                return ids
        return set()

    return {
        "ean": read_ean,
        "ean_ring": read_ean_ring,
        "aruco": read_aruco,
        "aruco_ring": read_aruco,
    }


def run(vessels: list[str] | None, out: Path) -> dict:
    """Run the sweeps and return the results, also written to ``results.json``"""
    manifest = json.loads((KIT / "manifest.json").read_text())
    vessels = vessels or sorted(
        manifest["vessels"],
        key=lambda v: (
            manifest["vessels"][v]["phase"],
            manifest["vessels"][v]["container_ml"],
        ),
    )
    xml, info = build_scene(vessels, manifest, out)
    rig = Rig(xml)
    readers = make_readers(registry.load_table(TABLE))
    results, wrong = {}, 0
    showcase = vessels[len(vessels) // 2]
    for vessel in vessels:
        meta = info[vessel]
        results[vessel] = {k: meta[k] for k in ("container_ml", "phase", "module_mm")}
        for kind in KINDS:
            expected = meta["marker_id"] if "aruco" in kind else meta["sample_id"]

            def reads(
                distance: float,
                yaw: float = 0.0,
                kind=kind,
                meta=meta,
                expected=expected,
                body=f"{kind}_{vessel}",
            ) -> bool:
                nonlocal wrong
                frame = rig.shoot(
                    body,
                    meta["radius_m"],
                    meta["label_z_m"],
                    distance=distance,
                    yaw_deg=yaw,
                )
                ids = readers[kind](bottle_box(frame, meta, distance), meta, distance)
                wrong += len(ids - {expected})
                return expected in ids

            reach = farthest([reads(d) for d in DISTANCES_M], DISTANCES_M)
            entry = {"reach_m": reach, "half_reach_yaws": [], "near_focus_yaws": []}
            if reach is not None:
                half = max(reach / 2.0, DISTANCES_M[0])
                entry["half_reach_m"] = half
                entry["half_reach_yaws"] = [y for y in YAWS_DEG if reads(half, y)]
            entry["near_focus_yaws"] = [y for y in YAWS_DEG if reads(NEAR_FOCUS_M, y)]
            results[vessel][kind] = entry
            if vessel == showcase:
                shot = rig.shoot(
                    f"{kind}_{vessel}",
                    meta["radius_m"],
                    meta["label_z_m"],
                    distance=0.22,
                    yaw_deg=35.0,
                )
                cv2.imwrite(
                    str(out / f"showcase_{kind}.png"), bottle_box(shot, meta, 0.22)
                )
            print(
                f"{vessel:14s} {kind:10s} module {meta['module_mm'][kind]:5.2f} mm  "
                f"reach {reach} m  turns read at half reach "
                f"{len(entry['half_reach_yaws'])}/{len(YAWS_DEG)}  at 0.30 m "
                f"{len(entry['near_focus_yaws'])}/{len(YAWS_DEG)}",
                flush=True,
            )
    results["_meta"] = {"wrong_ids": wrong, "showcase": showcase, "yaws": len(YAWS_DEG)}
    (out / "results.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(f"\nids read that were not the bottle's own: {wrong}")
    return results


def plot(results: dict, out: Path) -> Path:
    """Draw the comparison figure from the results

    Args:
        results: What :func:`run` returned or ``results.json`` holds.
        out: Folder holding the showcase crops; the figure is written there.

    Returns:
        Path of the figure.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    vessels = [v for v in results if not v.startswith("_")]
    names = [
        f"{'L' if results[v]['phase'] == 'liquid' else 'P'} "
        f"{results[v]['container_ml']:g} ml"
        for v in vessels
    ]
    turns = results["_meta"]["yaws"]
    figure = plt.figure(figsize=(16, 15))
    grid = figure.add_gridspec(4, 4, height_ratios=[1.15, 1, 1, 1], hspace=0.5)

    for column, kind in enumerate(KINDS):
        axis = figure.add_subplot(grid[0, column])
        image = cv2.imread(str(out / f"showcase_{kind}.png"))
        if image is not None:
            axis.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        axis.set_title(
            TITLES[kind], fontsize=12, color=COLOURS[kind], fontweight="bold"
        )
        axis.set_xlabel(f"{results['_meta']['showcase']}, turned 35 deg", fontsize=9)
        axis.set_xticks([])
        axis.set_yticks([])

    x = np.arange(len(vessels))
    width = 0.2
    panels = [
        (
            "Reach, facing the label squarely (m, log scale)",
            lambda r: r["reach_m"] or 0.0,
            True,
        ),
        (
            "Bottle orientations that read, at half the reach (% of a full turn)",
            lambda r: 100.0 * len(r["half_reach_yaws"]) / turns,
            False,
        ),
        (
            f"Bottle orientations that read from {NEAR_FOCUS_M:.2f} m, "
            "a GoPro's near focus (% of a full turn)",
            lambda r: 100.0 * len(r["near_focus_yaws"]) / turns,
            False,
        ),
    ]
    for row, (title, value, log) in enumerate(panels, start=1):
        axis = figure.add_subplot(grid[row, :])
        for k, kind in enumerate(KINDS):
            heights = [value(results[v][kind]) for v in vessels]
            bars = axis.bar(
                x + (k - 1.5) * width,
                heights,
                width,
                label=TITLES[kind],
                color=COLOURS[kind],
            )
            for bar, h in zip(bars, heights, strict=True):
                text = (f"{h:g}" if log else f"{h:.0f}") if h else "x"
                axis.annotate(
                    text,
                    (bar.get_x() + bar.get_width() / 2, max(h, 0.0)),
                    ha="center",
                    va="bottom",
                    fontsize=7,
                    xytext=(0, 1),
                    textcoords="offset points",
                )
        if log:
            axis.set_yscale("log")
            axis.set_ylim(0.08, 8)
            axis.axhline(NEAR_FOCUS_M, color="#d93025", linestyle="--", linewidth=1)
            axis.text(
                len(vessels) - 0.55,
                NEAR_FOCUS_M * 1.06,
                "GoPro near focus",
                color="#d93025",
                fontsize=8,
                ha="right",
            )
        else:
            axis.set_ylim(0, 112)
        axis.set_xticks(x)
        axis.set_xticklabels(names)
        axis.set_title(title, fontsize=12, loc="left")
        axis.spines[["top", "right"]].set_visible(False)
        if row == 1:
            axis.legend(ncols=4, fontsize=9, loc="upper left", frameon=False)
    figure.suptitle(
        "Labels on one side against labels all the way round "
        "(MuJoCo, GoPro Linear 1080p, L = liquid flask, P = powder bottle)",
        fontsize=14,
        y=0.995,
    )
    path = out / "comparison.png"
    figure.savefig(path, dpi=110, bbox_inches="tight")
    return path


def main() -> None:
    """Run the experiment, or only redraw its figure"""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--vessels", nargs="*", default=None)
    parser.add_argument(
        "--plot-only",
        action="store_true",
        help="redraw comparison.png from an existing results.json",
    )
    parser.add_argument(
        "--out", type=Path, default=REPO / "simulation" / "out" / "ring_experiment"
    )
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.plot_only:
        results = json.loads((args.out / "results.json").read_text())
    else:
        results = run(args.vessels, args.out)
    print("figure ->", plot(results, args.out))


if __name__ == "__main__":
    main()
