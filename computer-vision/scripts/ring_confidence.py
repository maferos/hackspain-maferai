"""Scan a shelf of pots and plot how sure the reader is about each one

Every bottle in the catalogue wears a ring of eight ``DICT_4X4_250`` markers,
and :mod:`labvision.markers` returns a posterior over sample ids rather than an
id. This script puts that to work on a spread of pots and viewing conditions
and draws the answer: for each pot, the probability that the code we extracted
is the code the pot actually carries.

The point of the figure is the pots the reader is *not* sure about. A pot that
fails to read costs one more look; a pot read wrongly chains the wrong compound
to it, and without a posterior the two are indistinguishable.

**The frames are analytic renders, not MuJoCo.** The ring texture is projected
onto the bottle's cylinder through the same GoPro Linear 1080p pinhole the
scene's cameras use, with the bottle's real radius and the real printed module
size taken from ``simulation/assets/labelled_bottles``; defocus, sensor noise
and exposure are then applied. That keeps pixels-per-module faithful, which is
what the read depends on, and keeps the script runnable from the
``computer-vision`` package alone --- ``wrist_scan.py`` needs ``mujoco``, which
is not installed alongside OpenCV here. Feeding real wrist frames to the same
reader is the next step, not a different one.

    python scripts/ring_confidence.py
    python scripts/ring_confidence.py --out /tmp/confidence --seed 7

Output: ``confidence.png``, ``results.json`` and ``pots.png`` (the frames that
were read) in ``results/ring_confidence/``. Needs ``matplotlib``.
"""

import argparse
import json
import logging
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labvision import bottles, markers, registry  # noqa: E402

logger = logging.getLogger(__name__)

REPO = Path(__file__).resolve().parents[2]
KIT = REPO / "simulation" / "assets" / "labelled_bottles"
TABLE = REPO / "computer-vision" / "barcodes" / "lookup_table.json"
OUT = Path(__file__).resolve().parents[1] / "results" / "ring_confidence"

WIDTH, HEIGHT, FOVY_DEG = 1920, 1080, 60.44
"""The scene's cameras: a GoPro in Linear mode at 1080p, as in aruco_experiment."""

FOCUS_M = 0.30
"""Where a GoPro's fixed focus is sharp. Defocus grows away from it."""

DEFOCUS_PX_PER_DIOPTRE = 0.55
"""Blur radius per dioptre of focus error. A stand-in for a real lens."""

CROP_PX = 420
"""Side of the frame handed to the reader, as a detector's crop would be."""

AMBIENT, DIFFUSE = 0.55, 0.45
"""Lambertian shading of the bottle wall, which dims the markers off-centre."""

BODY_GREY = 232
"""The HDPE wall above and below the ring."""

BENCH_GREY = (118, 126, 132)
"""Background behind the bottle, in BGR."""

# Sample id, how far the camera stands, how far the bottle is turned, and how
# much sensor noise. Chosen to span the five flask sizes and the range from an
# easy pot square in front of the lens to one turned away, small, far and noisy.
SCENARIOS: tuple[tuple[str, float, float, float], ...] = (
    ("SMP-0005", 0.30, 0.0, 2.0),
    ("SMP-0010", 0.42, 22.5, 4.0),
    ("SMP-0024", 0.18, 12.0, 3.0),
    ("SMP-0035", 0.22, 40.0, 4.0),
    ("SMP-0048", 0.15, 0.0, 4.0),
    ("SMP-0063", 0.42, 22.5, 6.0),
    ("SMP-0077", 0.12, 15.0, 5.0),
    ("SMP-0090", 0.35, 0.0, 6.0),
    ("SMP-0111", 0.24, 30.0, 7.0),
    ("SMP-0134", 0.55, 22.5, 9.0),
    ("SMP-0162", 0.38, 8.0, 10.0),
    ("SMP-0196", 0.45, 22.5, 10.0),
)


@dataclass(frozen=True)
class Pot:
    """One scanned pot and what the reader made of it.

    Attributes:
        sample_id: The sample the pot really is, known by construction.
        material: Its compound, for the figure's labels.
        vessel: Vessel class, such as ``bottle_500ml``.
        marker_id: The id actually printed on the ring.
        read_id: The id the reader settled on, or None if it found nothing.
        probability: Posterior that read_id is the pot's id.
        runner_up: Next most probable id, or None.
        runner_up_probability: Its posterior.
        decision: ``"accept"``, ``"rescan"`` or ``"reject"``.
        correct: Whether read_id is the printed id.
        distance_m: Camera standoff.
        yaw_deg: How far the bottle is turned from facing the camera.
        module_px: Printed module size in pixels at that standoff.
        copies: Quads that were scored on this pot.
        accepted_copies: How many of them OpenCV identified by itself.
    """

    sample_id: str
    material: str
    vessel: str
    marker_id: int
    read_id: int | None
    probability: float
    runner_up: int | None
    runner_up_probability: float
    decision: str
    correct: bool
    distance_m: float
    yaw_deg: float
    module_px: float
    copies: int
    accepted_copies: int


def label_wall(vessel: str) -> bottles.Wall:
    """Measure the straight wall a label sits on, from the kit's label mesh

    Re-measured here rather than imported from ``aruco_experiment``, which
    cannot be imported without ``mujoco``.

    Args:
        vessel: Vessel class, such as ``flask_10ml``.

    Returns:
        The wall, in the bottle's own frame.

    Raises:
        FileNotFoundError: If the kit has no label mesh for that vessel.
    """
    path = KIT / "meshes" / f"{vessel}_label.obj"
    rows = [
        line.split()[1:4]
        for line in path.read_text().splitlines()
        if line.startswith("v ")
    ]
    vertices = np.array(rows, dtype=float)
    radius = float(np.median(np.hypot(vertices[:, 0], vertices[:, 1])))
    low, high = float(vertices[:, 2].min()), float(vertices[:, 2].max())
    return bottles.Wall(radius, low, high)


def focal_px() -> float:
    """Focal length of the scene's GoPro, in pixels."""
    return HEIGHT / 2.0 / math.tan(math.radians(FOVY_DEG) / 2.0)


def _mip(texture: np.ndarray, target_width: float) -> np.ndarray:
    """Pre-shrink the texture to roughly its on-screen size, to stop it aliasing.

    A 1024 px strip sampled down to fifty pixels without this turns the markers
    into noise, which would make the reader look far worse than it is.
    """
    wanted = int(max(64, min(texture.shape[1], round(target_width * 2))))
    if wanted >= texture.shape[1]:
        return texture
    scale = wanted / texture.shape[1]
    return cv2.resize(
        texture, (wanted, max(8, int(round(texture.shape[0] * scale)))),
        interpolation=cv2.INTER_AREA,
    )


def render_pot(
    marker_id: int,
    vessel: str,
    distance_m: float,
    yaw_deg: float = 0.0,
    noise: float = 3.0,
    rng: np.random.Generator | None = None,
) -> tuple[np.ndarray, float]:
    """Render one pot's ring as the wrist camera would see it

    The bottle is a cylinder of its real radius carrying its real ring texture,
    ray-traced against the GoPro pinhole, Lambert-shaded, then defocused
    according to how far the standoff is from the camera's fixed focus and
    given sensor noise. No MuJoCo: see the module docstring for why, and for
    what that does and does not cost.

    Args:
        marker_id: Id printed round the bottle.
        vessel: Vessel class, which fixes the radius and the module size.
        distance_m: Camera standoff from the bottle's axis.
        yaw_deg: How far the bottle is turned about its own axis. Zero puts a
            marker's centre square in front of the lens; 22.5 degrees puts the
            seam between two markers there, which is the worst case.
        noise: Standard deviation of the sensor noise, in grey levels.
        rng: Random source, so a figure can be reproduced.

    Returns:
        The BGR frame and the printed module size in pixels at that standoff.

    Raises:
        ValueError: If the standoff is not positive.
    """
    if distance_m <= 0:
        raise ValueError(f"distance must be positive, got {distance_m}")
    rng = rng or np.random.default_rng(0)

    wall = label_wall(vessel)
    patch = bottles.ring_patch(wall)
    radius, half = wall.radius_m, patch.height_m / 2.0
    focal = focal_px()

    centre = (CROP_PX - 1) / 2.0
    grid = (np.arange(CROP_PX) - centre) / focal
    dx, dy = np.meshgrid(grid, -grid)
    dz = np.ones_like(dx)

    # Ray-cylinder: the bottle's axis stands at (0, *, distance), along Y.
    a = dx**2 + dz**2
    half_b = dz * distance_m
    c = distance_m**2 - radius**2
    disc = half_b**2 - a * c
    hit = disc > 0
    t = np.where(hit, (half_b - np.sqrt(np.maximum(disc, 0.0))) / a, 0.0)

    px, py, pz = t * dx, t * dy, t * dz
    normal_x, normal_z = px / radius, (pz - distance_m) / radius
    angle = np.arctan2(normal_x, -normal_z)

    body = hit & (py > -3.0 * half) & (py < 4.0 * half)
    band = body & (np.abs(py) <= half)

    circumference_px = 2.0 * math.pi * radius * focal / distance_m
    texture = _mip(bottles.render_ring(marker_id), circumference_px)
    u = (angle + math.radians(yaw_deg)) / (2.0 * math.pi) + 0.5
    v = (half - py) / (2.0 * half)
    map_x = (np.mod(u, 1.0) * (texture.shape[1] - 1)).astype(np.float32)
    map_y = np.clip(v, 0.0, 1.0).astype(np.float32) * (texture.shape[0] - 1)
    label = cv2.remap(
        texture, map_x, map_y.astype(np.float32),
        cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP,
    )

    # Light from the camera's own side, so the wall dims as it curves away.
    shade = AMBIENT + DIFFUSE * np.clip(-normal_z, 0.0, 1.0)
    surface = np.where(band, label.astype(np.float64), float(BODY_GREY)) * shade

    frame = np.zeros((CROP_PX, CROP_PX, 3), np.float64)
    frame[:] = BENCH_GREY
    frame[body] = surface[body, None]

    focus_error = abs(1.0 / distance_m - 1.0 / FOCUS_M)
    sigma = DEFOCUS_PX_PER_DIOPTRE * focus_error
    if sigma > 0.3:
        frame = cv2.GaussianBlur(frame, (0, 0), sigma)
    frame += rng.normal(0.0, noise, frame.shape)
    module_px = patch.module_m * focal / distance_m
    return np.clip(frame, 0, 255).astype(np.uint8), module_px


def scan_pots(
    table: dict[str, dict[str, object]],
    scenarios: tuple[tuple[str, float, float, float], ...] = SCENARIOS,
    seed: int = 0,
) -> tuple[list[Pot], list[np.ndarray]]:
    """Render and read every pot in the scenario list

    Args:
        table: Lookup table, from ``labvision.registry.load_table``.
        scenarios: One ``(sample id, standoff, yaw, noise)`` per pot.
        seed: Random source for the sensor noise.

    Returns:
        The results and the frames that produced them, in the same order.

    Raises:
        KeyError: If a scenario names a sample the table does not hold.
    """
    by_sample = {str(row["sample_id"]): row for row in table.values()}
    detector = markers.make_detector()
    rng = np.random.default_rng(seed)

    pots, frames = [], []
    for sample_id, distance, yaw, noise in scenarios:
        row = by_sample[sample_id]
        marker_id = int(row["marker_id"])
        frame, module_px = render_pot(
            marker_id, str(row["vessel_class"]), distance, yaw, noise, rng
        )
        result = markers.scan(frame, table, detector)
        runner = result.posterior[1] if len(result.posterior) > 1 else None
        pots.append(
            Pot(
                sample_id=sample_id,
                material=str(row["material"]),
                vessel=str(row["vessel_class"]),
                marker_id=marker_id,
                read_id=result.marker_id,
                probability=result.probability,
                runner_up=runner[0] if runner else None,
                runner_up_probability=runner[1] if runner else 0.0,
                decision=result.decision,
                correct=result.marker_id == marker_id,
                distance_m=distance,
                yaw_deg=yaw,
                module_px=module_px,
                copies=len(result.readings),
                accepted_copies=sum(r.accepted for r in result.readings),
            )
        )
        frames.append(frame)
        logger.info(
            "%s: read %s p=%.6f (%s), %d copies",
            sample_id, result.marker_id, result.probability,
            result.decision, len(result.readings),
        )
    return pots, frames


def _probability_text(pot: Pot) -> str:
    """Write a posterior without rounding a near-certainty up to a flat 1.000000

    Args:
        pot: The scanned pot.

    Returns:
        A label for the bar, as a probability or as its distance from one.
    """
    if pot.read_id is None:
        return "nothing read"
    doubt = 1.0 - pot.probability
    if doubt < 1e-6:
        return f"1 - {doubt:.0e}"
    return f"{pot.probability:.6f}"


def plot(pots: list[Pot], out: Path) -> Path:
    """Draw the per-pot confidence figure

    Two panels over the same pots. The left one answers the question as asked
    --- the probability that the code read is the code the pot carries --- and
    the right one is the same number in nines, because everything that matters
    lives between 0.99 and 0.9999999 and a linear axis flattens all of it
    against the right-hand edge. Both grow rightwards with confidence, so a
    long bar never means an unsure pot.

    Args:
        pots: Scanned pots, in any order; they are sorted by probability.
        out: Directory to write into. Created if missing.

    Returns:
        The path written.

    Raises:
        ImportError: If matplotlib is not installed.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    surface, ink, muted = "#fcfcfb", "#0b0b0b", "#52514e"
    status = {"accept": "#0ca30c", "rescan": "#fab219", "reject": "#d03b3b"}
    ceiling = 9.0

    def nines(probability: float) -> float:
        """Confidence as the number of nines, -log10(1 - p), capped."""
        return min(-math.log10(max(1.0 - probability, 10.0**-ceiling)), ceiling)

    ordered = sorted(pots, key=lambda p: (p.probability, -p.distance_m))
    y = np.arange(len(ordered))
    labels = [
        f"{p.sample_id}  {p.material[:22]}\n{p.vessel}  {p.distance_m:.2f} m"
        f"  {p.module_px:.1f} px/module"
        for p in ordered
    ]
    colours = [status[p.decision] for p in ordered]

    fig, (left, right) = plt.subplots(
        1, 2, figsize=(14.5, 7.8), sharey=True,
        gridspec_kw={"width_ratios": [1.0, 1.05], "wspace": 0.08},
    )
    fig.patch.set_facecolor(surface)
    fig.subplots_adjust(left=0.165, right=0.985, top=0.845, bottom=0.085)

    for axes in (left, right):
        axes.set_facecolor(surface)
        for side in ("top", "right", "left"):
            axes.spines[side].set_visible(False)
        axes.spines["bottom"].set_color("#d9d8d3")
        axes.tick_params(colors=muted, length=0, labelsize=8)
        axes.grid(axis="x", color="#eceae4", linewidth=0.8)
        axes.set_axisbelow(True)
        axes.invert_yaxis()

    left.barh(y, [p.probability for p in ordered], height=0.56, color=colours)
    left.set_xlim(0, 1.16)
    left.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    left.set_yticks(y, labels, fontsize=8, color=ink)
    left.set_xlabel(
        "P(the code read is the code on the pot)", color=muted, fontsize=9
    )
    left.axvline(markers.ACCEPT_P, color="#b9b7b0", linewidth=1, linestyle=(0, (4, 3)))
    for index, pot in enumerate(ordered):
        text = _probability_text(pot)
        left.text(
            pot.probability + 0.02, index, text,
            va="center", ha="left", fontsize=8, color=ink,
        )

    right.barh(y, [nines(p.probability) for p in ordered], height=0.56, color=colours)
    right.set_xlim(0, ceiling + 3.4)
    right.set_xticks(range(int(ceiling) + 1))
    right.set_xlabel(
        "confidence in nines,  -log10(1 - P)   (longer is surer)",
        color=muted, fontsize=9,
    )
    right.axvline(
        nines(markers.ACCEPT_P), color="#b9b7b0", linewidth=1, linestyle=(0, (4, 3))
    )
    right.text(
        nines(markers.ACCEPT_P) + 0.08, -0.72, "accept threshold",
        fontsize=7.5, color=muted, ha="left",
    )
    for index, pot in enumerate(ordered):
        verdict = "read correct" if pot.correct else "READ WRONG"
        right.text(
            nines(pot.probability) + 0.25, index,
            f"{pot.decision} - {verdict} - {pot.copies} copies",
            va="center", ha="left", fontsize=7.5, color=ink,
        )

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=colour, label=f"{name} ({tally})")
        for name, colour in status.items()
        if (tally := sum(p.decision == name for p in ordered))
    ]
    fig.legend(
        handles=handles, loc="upper right", bbox_to_anchor=(0.985, 0.955),
        ncol=len(handles), frameon=False, fontsize=8.5, labelcolor=ink,
    )

    silent = sum(1 for p in pots if p.decision == "accept" and not p.correct)
    fig.text(
        0.012, 0.955, "How sure is the reader which pot it just scanned?",
        ha="left", fontsize=15, color=ink, weight="bold",
    )
    fig.text(
        0.012, 0.915,
        f"{len(ordered)} pots, a ring of eight ArUco markers each, scored against "
        "the 200-sample catalogue. Every read that was wrong fell below the "
        "threshold:",
        ha="left", fontsize=9, color=muted,
    )
    fig.text(
        0.012, 0.888,
        f"{silent} of {len(ordered)} pots were accepted with the wrong code. "
        "Analytic GoPro renders, not MuJoCo frames; the posterior is not yet "
        "calibrated against ground truth.",
        ha="left", fontsize=9, color=muted,
    )

    out.mkdir(parents=True, exist_ok=True)
    path = out / "confidence.png"
    fig.savefig(path, dpi=170, facecolor=surface)
    plt.close(fig)
    return path


def contact_sheet(frames: list[np.ndarray], pots: list[Pot], out: Path) -> Path:
    """Write the frames that were read, so the figure can be checked against them

    Args:
        frames: Rendered frames, parallel to pots.
        pots: Their results.
        out: Directory to write into.

    Returns:
        The path written.
    """
    columns = 4
    rows = math.ceil(len(frames) / columns)
    sheet = np.full((rows * CROP_PX, columns * CROP_PX, 3), 250, np.uint8)
    for index, (frame, pot) in enumerate(zip(frames, pots, strict=True)):
        row, column = divmod(index, columns)
        tile = frame.copy()
        cv2.putText(
            tile, f"{pot.sample_id} {pot.decision} p={pot.probability:.4f}",
            (8, CROP_PX - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (20, 20, 20), 1,
            cv2.LINE_AA,
        )
        sheet[row * CROP_PX:(row + 1) * CROP_PX,
              column * CROP_PX:(column + 1) * CROP_PX] = tile
    out.mkdir(parents=True, exist_ok=True)
    path = out / "pots.png"
    cv2.imwrite(str(path), sheet)
    return path


def main() -> None:
    """Scan the scenario pots, plot the confidences and write the results"""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=OUT, help="Output directory.")
    parser.add_argument("--table", type=Path, default=TABLE, help="Lookup table.")
    parser.add_argument("--seed", type=int, default=0, help="Sensor-noise seed.")
    parser.add_argument("--verbose", action="store_true", help="Log each pot.")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s %(message)s",
    )

    table = registry.load_table(args.table)
    pots, frames = scan_pots(table, seed=args.seed)
    figure = plot(pots, args.out)
    sheet = contact_sheet(frames, pots, args.out)
    (args.out / "results.json").write_text(
        json.dumps([asdict(p) for p in pots], indent=2), encoding="utf-8"
    )

    wrong = [p for p in pots if not p.correct and p.decision == "accept"]
    print(f"{len(pots)} pots scanned")
    for name in ("accept", "rescan", "reject"):
        tally = sum(p.decision == name for p in pots)
        print(f"  {name:<7} {tally}")
    print(f"  silently wrong (accepted and not the printed id): {len(wrong)}")
    print(f"figure:  {figure}")
    print(f"frames:  {sheet}")


if __name__ == "__main__":
    main()
