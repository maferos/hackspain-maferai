#!/usr/bin/env python3
"""Plot a propose-confirm run: where the bottles are, where we said they were.

Run from computer-vision/ after scripts/propose_confirm.py:
    python scripts/scan_plots.py ../simulation/out/scan_rail

Three figures, each answering one question:

* ``bench.png`` --- the bench from above: every bottle's true position, the
  one the fixed camera proposed, and the one the wrist refined to once it flew
  over and read the ring. This is the picture to look at first, because it
  shows *where* on the bench the placement is worse, which the summary
  statistics hide.
* ``residuals.png`` --- the same errors as offsets in millimetres, so a
  systematic bias shows up as a cloud off the origin and random error as a
  cloud around it. The two are fixed by completely different things.
* ``detail.png`` --- the same errors again with nothing exaggerated, drawn on
  the footprint of the flask they belong to. ``bench.png`` has to magnify the
  offsets to show them at all, which loses what they are worth: this one says
  whether an error is a hair or half a bottle.
* ``anatomy.png`` --- the same offsets split into the two things that make
  them: what the anchor's assumed radius does, along the line of sight, and
  what is left over. Needs the camera pose, which runs since 19 September 2026
  record.
* ``boxes.png`` --- the fixed camera's own frame with the detector's boxes on
  it, and the true silhouettes beside them.
* ``lookup.png``, with ``--table`` --- what the harness lookup table ends up
  holding: the robot's memory, and what the formula stage reads.

Colours are the two ends of a validated categorical pair: blue is truth,
orange is what we predicted. Everything is direct-labelled, so identity never
rests on colour alone.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import matplotlib
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

TRUTH = '#2a78d6'
PREDICTED = '#eb6834'
REFINED = '#4a3aa7'
INK = '#1b1d21'
MUTED = '#6f757d'
SURFACE = '#fcfcfb'
GRID = '#e3e0d8'


def style(ax) -> None:
    """Recede the furniture so the marks carry the chart."""
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9)


def by_sample(bottles: list[dict], proposals: list[dict]) -> dict[str, dict]:
    """Each named sample's own proposal: the nearest look that read its ring

    A ring can be read from more than one look --- a neighbour's view often
    catches it --- and those looks do not stand in the same place. The offset
    that means anything is the one from the proposal nearest the bottle; the
    rest are second sightings, which ``world.one_per_sample`` drops too.
    """
    truth = {b['sample_id']: b['xy'] for b in bottles}
    best: dict[str, tuple[float, dict]] = {}
    for proposal in proposals:
        sample = (proposal.get('confirm') or {}).get('sample_id')
        if not sample:
            continue
        here = truth.get(sample)
        away = math.dist(proposal['xy'], here) if here else math.inf
        if sample not in best or away < best[sample][0]:
            best[sample] = (away, proposal)
    return {sample: pair[1] for sample, pair in best.items()}


def load(run: Path) -> tuple[list[dict], list[dict], dict | None]:
    """Read one layout's scored bottles, its proposals and the fixed camera.

    Args:
        run: Directory holding propose_confirm.json.

    Returns:
        The scored bottles, the proposals, and the general camera's frame
        record --- None for a run written before it was stored.
    """
    layout = json.loads((run / 'propose_confirm.json').read_text())[0]
    return layout['scored']['bottles'], layout['proposals'], layout.get('camera')


AXES_WIDTH_IN = 11.4
"""How much of the 13-inch figure the axes get once the labels have theirs.
Only used to shape the figure, so it does not have to be exact."""

EXAGGERATION = 20
"""The errors are a few millimetres on a bench 3.5 m across, so drawn true to
scale the proposal sits exactly on the truth and the figure says nothing. The
offset is drawn this many times over, and the axes stay in real metres so
positions can still be read off."""


def bench(bottles: list[dict], proposals: list[dict], out: Path) -> None:
    """The bench from above: truth against proposal, error exaggerated."""
    named = by_sample(bottles, proposals)
    # The axes are equal-aspect, so the figure has to be the shape of what the
    # seed occupies or the drawing floats in dead canvas: a compact layout in a
    # figure cut for the whole 3.5 m bench is a strip with empty sides, and a
    # bench-shaped one in a tall figure is a strip with empty ends. The width is
    # fixed; the height is what equal aspect needs for this layout, plus the
    # inch and a half the title and the legend take.
    xs = [b['xy'][0] for b in bottles]
    ys = [b['xy'][1] for b in bottles]
    span_x, span_y = max(xs) - min(xs), max(ys) - min(ys)
    spread = span_y / span_x if len(bottles) > 1 and span_x else 0.2
    fig, ax = plt.subplots(figsize=(13, min(max(AXES_WIDTH_IN * spread + 1.6,
                                               4.4), 8.0)))
    style(ax)

    recovered, misnamed = 0, []
    for bottle in bottles:
        truth = bottle['xy']
        proposal = named.get(bottle['sample_id'])
        if bottle.get('wrong'):
            # A box of its own, and the ring read there belonged to a
            # neighbour: the pass holds a true pair of sample and position,
            # but not this bottle's. Its refined mark would sit on the
            # neighbour, so it is not drawn.
            misnamed.append(bottle)
            ax.plot(*truth, marker='s', markersize=9, color=SURFACE,
                    markeredgecolor=INK, markeredgewidth=1.6, zorder=5)
            ax.plot(*truth, marker='o', markersize=6, color=TRUTH, zorder=4)
            continue
        if proposal is None:
            ax.plot(*truth, marker='o', markersize=7, color=SURFACE,
                    markeredgecolor=MUTED, markeredgewidth=1.6, zorder=3)
            continue
        refined = (proposal.get('confirm') or {}).get('refined_xy')
        if bottle.get('error_m') is None:
            # The fixed camera never boxed this one --- the scoring paired no
            # proposal with it --- and the wrist read its ring anyway, from the
            # look it took at a neighbour. Its proposal belongs to that
            # neighbour, metres away, so there is no offset of its own to draw:
            # an open circle says the scan found it and the fixed camera did
            # not, and the refined mark says where it stands.
            recovered += 1
            ax.plot(*truth, marker='o', markersize=8.5, color=SURFACE,
                    markeredgecolor=PREDICTED, markeredgewidth=1.8, zorder=5)
            if refined:
                ax.plot(*[truth[i] + (refined[i] - truth[i]) * EXAGGERATION
                          for i in (0, 1)],
                        marker='D', markersize=4.5, color=REFINED,
                        markeredgecolor=SURFACE, markeredgewidth=0.9, zorder=6)
            continue
        shown = [truth[i] + (proposal['xy'][i] - truth[i]) * EXAGGERATION
                 for i in (0, 1)]
        ax.plot([truth[0], shown[0]], [truth[1], shown[1]],
                color=PREDICTED, linewidth=1.3, alpha=0.8, zorder=2)
        ax.plot(*truth, marker='o', markersize=6, color=TRUTH, zorder=4)
        ax.plot(*shown, marker='x', markersize=7, markeredgewidth=1.8,
                color=PREDICTED, zorder=5)
        # The wrist's correction, exaggerated the same amount so the three
        # marks are comparable. It lands on the truth even at 20x, which is
        # the point: 0.2 mm times twenty is still a fifth of a marker.
        if refined:
            ax.plot(*[truth[i] + (refined[i] - truth[i]) * EXAGGERATION
                      for i in (0, 1)],
                    marker='D', markersize=4.5, color=REFINED,
                    markeredgecolor=SURFACE, markeredgewidth=0.9, zorder=6)

    # Only the worst, and only one: at this scale neighbouring labels collide.
    worst = max((b for b in bottles if b.get('error_m')),
                key=lambda b: b['error_m'], default=None)
    if worst:
        ax.annotate(f'worst: {worst["sample_id"]}, '
                    f'{worst["error_m"] * 1000:.0f} mm',
                    worst['xy'], textcoords='offset points', xytext=(14, -14),
                    ha='left', va='top', fontsize=8.5, color=INK)

    lost = sum(1 for b in bottles if not b.get('wrong')
               and b.get('error_m') is None and b['sample_id'] not in named)
    # One or two of these are worth naming on the figure; a handful is a list.
    if len(misnamed) <= 3:
        for bottle in misnamed:
            ax.annotate(f'read as {bottle["named"]}', bottle['xy'],
                        textcoords='offset points', xytext=(11, 12),
                        ha='left', va='bottom', fontsize=8.5, color=INK)
    ax.plot([], [], 'o', color=TRUTH, markersize=6, label='true position')
    ax.plot([], [], 'x', color=PREDICTED, markersize=7, markeredgewidth=1.8,
            label=f'proposed by the fixed camera, offset {EXAGGERATION}x')
    ax.plot([], [], 'D', color=REFINED, markersize=4.5,
            markeredgecolor=SURFACE, markeredgewidth=0.9,
            label=f'refined by the wrist, offset {EXAGGERATION}x')
    if recovered:
        ax.plot([], [], 'o', color=SURFACE, markeredgecolor=PREDICTED,
                markeredgewidth=1.8, markersize=8.5,
                label=f'missed by the fixed camera, named by the wrist '
                      f'({recovered})')
    if misnamed:
        ax.plot([], [], 's', color=SURFACE, markeredgecolor=INK,
                markeredgewidth=1.6, markersize=9,
                label=f'named wrongly ({len(misnamed)})')
    if lost:
        ax.plot([], [], 'o', color=SURFACE, markeredgecolor=MUTED,
                markeredgewidth=1.6, markersize=7,
                label=f'not found ({lost})')
    ax.set_xlabel('x along the bench (m)', color=MUTED, fontsize=9)
    ax.set_ylabel('y (m)', color=MUTED, fontsize=9)
    ax.set_aspect('equal')
    # Title and legend are placed on the figure, in inches: a compact layout
    # makes the axes tall, and furniture positioned in axes fractions would
    # walk off the canvas with it.
    height = fig.get_size_inches()[1]
    fig.suptitle('Where the bottles are, where the camera put them, '
                 'and where the wrist corrected them to',
                 color=INK, fontsize=12, x=0.012, ha='left',
                 y=1 - 0.32 / height)
    fig.text(0.012, 1 - 0.62 / height,
             f'offsets drawn {EXAGGERATION}x, axes in real metres; the wrist '
             'correction still lands on the truth',
             color=MUTED, fontsize=9, ha='left')
    # Under the axes: the bench is wide and flat, and a legend inside it
    # covers bottles at either end.
    fig.legend(*ax.get_legend_handles_labels(), loc='lower center',
               bbox_to_anchor=(0.5, 0.012), frameon=False, fontsize=9,
               labelcolor=INK, ncol=3)
    fig.tight_layout(rect=(0, 0.72 / height, 1, 1 - 0.82 / height))
    fig.savefig(out, dpi=170, facecolor=SURFACE)
    plt.close(fig)


def residuals(bottles: list[dict], proposals: list[dict], out: Path) -> None:
    """Errors as offsets, so bias and scatter can be told apart."""
    named = by_sample(bottles, proposals)
    read = [b for b in bottles if b['sample_id'] in named]
    # A bottle the fixed camera never boxed has no offset of its own: the
    # proposal its ring was read from belongs to a neighbour. It still has a
    # refined position, so it joins the second cloud and not the first.
    proposed = np.array([np.array(named[b['sample_id']]['xy']) - np.array(b['xy'])
                         for b in read if b.get('error_m') is not None]) * 1000
    refined = np.array([np.array(named[b['sample_id']]['confirm']['refined_xy'])
                        - np.array(b['xy']) for b in read]) * 1000

    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    style(ax)
    limit = float(np.abs(proposed).max()) * 1.25
    for radius in (5, 10, 15):
        if radius < limit:
            ax.add_patch(plt.Circle((0, 0), radius, fill=False, color=GRID,
                                    linewidth=0.9, zorder=1))
            ax.annotate(f'{radius} mm', (0, radius), textcoords='offset points',
                        xytext=(4, 2), fontsize=8, color=MUTED)
    ax.axhline(0, color=GRID, linewidth=1)
    ax.axvline(0, color=GRID, linewidth=1)
    ax.scatter(proposed[:, 0], proposed[:, 1], s=46, color=PREDICTED,
               edgecolor=SURFACE, linewidth=1.4, zorder=4,
               label=f'fixed camera (n={len(proposed)})')
    ax.scatter(refined[:, 0], refined[:, 1], s=34, color=REFINED,
               edgecolor=SURFACE, linewidth=1.4, zorder=5,
               label='after the wrist refines'
                     + (f' (n={len(refined)})' if len(refined) != len(proposed)
                        else ''))
    mean = proposed.mean(axis=0)
    ax.plot(*mean, marker='P', markersize=12, color=INK, zorder=6)
    ax.annotate(f'mean offset {np.linalg.norm(mean):.1f} mm', mean,
                textcoords='offset points', xytext=(8, -12), fontsize=9,
                color=INK)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal')
    ax.legend(loc='lower right', frameon=False, fontsize=9, labelcolor=INK)
    ax.set_xlabel('error in x (mm)', color=MUTED, fontsize=9)
    ax.set_ylabel('error in y (mm)', color=MUTED, fontsize=9)
    ax.set_title('Predicted minus true, per bottle', color=INK, fontsize=12,
                 loc='left', pad=12)
    fig.tight_layout()
    fig.savefig(out, dpi=170, facecolor=SURFACE)
    plt.close(fig)


def vessel_radii(bottles: list[dict]) -> dict[str, tuple[str, float]]:
    """Each bottle's vessel class and the radius of its label ring, in metres

    The catalogue names the class and the kit's own label mesh gives the
    radius, so a regenerated kit needs no change here.
    """
    from labvision import registry
    from labvision.identify import DEFAULT_TABLE
    from labvision.perception import ring_geometry

    table = registry.load_table(DEFAULT_TABLE)
    classes = {row['sample_id']: row['vessel_class'] for row in table.values()}
    out = {}
    for bottle in bottles:
        vessel = classes.get(bottle['sample_id'])
        if vessel:
            out[bottle['sample_id']] = (vessel, ring_geometry(vessel)[0])
    return out


def detail(bottles: list[dict], proposals: list[dict], out: Path) -> None:
    """Every error at true scale, drawn on the flask it belongs to.

    One panel per vessel class standing on the bench, all bottles of a class
    stacked on one flask with their true position at its centre. Nothing is
    exaggerated, so the panels answer the question the magnified bench view
    cannot: how much of a bottle is the error worth.
    """
    named = by_sample(bottles, proposals)
    radii = vessel_radii(bottles)
    groups: dict[tuple[float, str], list[dict]] = {}
    for bottle in bottles:
        if bottle['sample_id'] in named and bottle['sample_id'] in radii:
            vessel, radius = radii[bottle['sample_id']]
            groups.setdefault((radius, vessel), []).append(bottle)
    if not groups:
        return
    keys = sorted(groups)

    fig, axes = plt.subplots(1, len(keys), figsize=(3.1 * len(keys), 3.9))
    for ax, key in zip(np.atleast_1d(axes), keys):
        radius, vessel = key
        rows = groups[key]
        style(ax)
        ax.grid(False)
        limit = radius * 1000 + 7
        ax.add_patch(plt.Circle((0, 0), radius * 1000, facecolor=GRID,
                                edgecolor=MUTED, linewidth=0.9, alpha=0.45,
                                zorder=1))
        for bottle in rows:
            proposal = named[bottle['sample_id']]
            refined = (np.array(proposal['confirm']['refined_xy'])
                       - np.array(bottle['xy'])) * 1000
            if bottle.get('error_m') is not None:
                offset = (np.array(proposal['xy'])
                          - np.array(bottle['xy'])) * 1000
                ax.plot(*offset, marker='x', markersize=6, markeredgewidth=1.5,
                        color=PREDICTED, zorder=4)
            ax.plot(*refined, marker='D', markersize=3.4, color=REFINED,
                    markeredgecolor=SURFACE, markeredgewidth=0.7, zorder=5)
        ax.plot(0, 0, marker='o', markersize=5, color=TRUTH, zorder=6)
        errors = [b['error_m'] * 1000 for b in rows if b.get('error_m')]
        ax.set_title(f"{vessel.replace('flask_', '').replace('ml', ' ml')}"
                     f"  ({len(rows)})",
                     color=INK, fontsize=10.5, loc='left', pad=8)
        # Inside the panel: above it the caption would sit on the top tick.
        ax.text(0.04, 0.045, f'{radius * 1000:.0f} mm radius, '
                             f'{np.median(errors):.1f} mm median',
                transform=ax.transAxes, color=MUTED, fontsize=8.5)
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_aspect('equal')
        ax.set_xticks([-20, -10, 0, 10, 20])
        ax.set_yticks([-20, -10, 0, 10, 20])
        ax.tick_params(labelsize=8)
    for ax in np.atleast_1d(axes)[1:]:
        ax.set_yticklabels([])
    first = np.atleast_1d(axes)[0]
    first.set_ylabel('millimetres from the true axis', color=MUTED, fontsize=9)
    first.plot([], [], 'o', color=TRUTH, markersize=5, label='true position')
    first.plot([], [], 'x', color=PREDICTED, markersize=6, markeredgewidth=1.5,
               label='proposed by the fixed camera')
    first.plot([], [], 'D', color=REFINED, markersize=3.4,
               markeredgecolor=SURFACE, markeredgewidth=0.7,
               label='refined by the wrist')
    fig.legend(loc='lower center', frameon=False, fontsize=9, labelcolor=INK,
               ncol=3, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle('The same errors at true scale, on the flask they belong to',
                 color=INK, fontsize=12, x=0.012, ha='left')
    fig.tight_layout(rect=(0, 0.06, 1, 0.97))
    fig.savefig(out, dpi=170, facecolor=SURFACE)
    plt.close(fig)


PROPOSAL_RADIUS_MM = 18.0
"""What :func:`labvision.perception.propose` assumes a bottle's radius to be
before the wrist has named it (``PROPOSAL_RADIUS_M``). Kept here as a number so
the figure can say what that assumption costs each flask."""


def anatomy(bottles: list[dict], proposals: list[dict], camera: dict,
            out: Path) -> None:
    """Split every offset into the anchor's two errors, drawn along the bench.

    The base anchor makes two mistakes and they point in different directions,
    which is why the arrows on ``bench.png`` can swing round halfway along a
    bench without anything about the camera changing:

    1. It pushes the ray's landing point back from the near rim of the base
       circle to the axis by :data:`PROPOSAL_RADIUS_MM`, along the line of
       sight. The bottle's real radius is not that, so what is left is
       ``(assumed - true)`` metres *along that line* --- towards the camera for
       a flask fatter than the assumption, away from it for a thinner one.
    2. The middle of the box is not the axis either: under perspective the two
       silhouette tangents of a cylinder standing off the optical axis are not
       symmetric. That one is across the line of sight and grows with the
       bottle's radius and with how far off-axis it stands.

    Three panels, the same bench and the same exaggeration in each: what was
    measured, what the first mistake accounts for, and what is left.
    """
    named = by_sample(bottles, proposals)
    radii = vessel_radii(bottles)
    eye = np.array(camera['cam_pos'][:2])
    rows = []
    for bottle in bottles:
        proposal = named.get(bottle['sample_id'])
        if (proposal is None or bottle.get('error_m') is None
                or bottle['sample_id'] not in radii):
            continue
        truth = np.array(bottle['xy'])
        offset = (np.array(proposal['xy']) - truth) * 1000
        sight = truth - eye
        sight = sight / np.linalg.norm(sight)
        term = (PROPOSAL_RADIUS_MM - radii[bottle['sample_id']][1] * 1000) * sight
        rows.append((truth, offset, term, offset - term,
                     radii[bottle['sample_id']][0]))
    if not rows:
        return

    panels = (('what the fixed camera is out by', 1),
              (f'the assumed {PROPOSAL_RADIUS_MM:.0f} mm radius, '
               'along the line of sight', 2),
              ('what is left: across it, growing away from the camera', 3))
    fig, axes = plt.subplots(3, 1, figsize=(13, 9.6), sharex=True, sharey=True)
    for ax, (label, which) in zip(axes, panels):
        style(ax)
        for truth, offset, term, rest, _ in rows:
            vector = (offset, term, rest)[which - 1] / 1000 * EXAGGERATION
            ax.annotate('', xy=truth + vector, xytext=truth,
                        arrowprops=dict(arrowstyle='-|>', linewidth=1.2,
                                        color=PREDICTED, shrinkA=0, shrinkB=0))
            ax.plot(*truth, marker='o', markersize=4.5, color=TRUTH, zorder=4)
        ax.set_title(label, color=INK, fontsize=10.5, loc='left', pad=6)
        ax.set_ylabel('y (m)', color=MUTED, fontsize=9)
        ax.set_aspect('equal')
    # An annotation's arrow does not count towards the autoscale, so the
    # limits have to be told about the tips or the longest arrows are clipped.
    tips = np.array([truth + v / 1000 * EXAGGERATION
                     for truth, *vectors, _ in rows for v in vectors]
                    + [truth for truth, *_ in rows])
    pad = 0.03
    axes[0].set_xlim(tips[:, 0].min() - pad, tips[:, 0].max() + pad)
    axes[0].set_ylim(tips[:, 1].min() - pad, tips[:, 1].max() + pad)
    # The camera stands off the bench; what matters on the bench is the x it
    # looks down, where the second error changes sign.
    for ax in axes:
        ax.axvline(eye[0], color=MUTED, linewidth=1, linestyle=(0, (4, 3)),
                   zorder=1)
    axes[2].annotate("the camera's own x", (eye[0], 0), xycoords=('data',
                     'axes fraction'), xytext=(6, 6), textcoords='offset points',
                     fontsize=8.5, color=MUTED)
    # The flask classes, where they stand: a rows layout sorts them along the
    # bench, which is what turns a size boundary into a place on the figure.
    seen: dict[str, list[float]] = {}
    for truth, _, _, _, vessel in rows:
        seen.setdefault(vessel, []).append(truth[0])
    for vessel, xs in seen.items():
        axes[0].annotate(vessel.replace('flask_', '').replace('ml', ' ml'),
                         (float(np.mean(xs)), 1.0),
                         xycoords=('data', 'axes fraction'),
                         xytext=(0, 5), textcoords='offset points',
                         ha='center', fontsize=8.5, color=MUTED)
    axes[2].set_xlabel('x along the bench (m)', color=MUTED, fontsize=9)
    height = fig.get_size_inches()[1]
    fig.suptitle('The two mistakes the anchor makes, and where each one shows',
                 color=INK, fontsize=12, x=0.012, ha='left', y=1 - 0.3 / height)
    fig.text(0.012, 1 - 0.56 / height,
             f'offsets drawn {EXAGGERATION}x; measured = radius + left over, '
             'panel by panel', color=MUTED, fontsize=9, ha='left')
    fig.tight_layout(rect=(0, 0, 1, 1 - 0.78 / height))
    fig.savefig(out, dpi=170, facecolor=SURFACE)
    plt.close(fig)


def boxes(bottles: list[dict], proposals: list[dict], frame: Path,
          out: Path) -> None:
    """The fixed camera's frame with the detector's boxes and the true ones."""
    image = plt.imread(frame)
    height, width = image.shape[:2]
    fig, ax = plt.subplots(figsize=(width / 190, height / 190))
    ax.imshow(image)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ax.spines.values():
        side.set_visible(False)

    for bottle in bottles:
        if not bottle.get('xyxy'):
            continue
        x0, y0, x1, y1 = bottle['xyxy']
        ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False,
                                   edgecolor=TRUTH, linewidth=1.1))
    for proposal in proposals:
        x0, y0, x1, y1 = proposal['xyxy']
        named = proposal.get('confirm') or {}
        ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False,
                                   edgecolor=PREDICTED, linewidth=1.4))
        if named.get('sample_id'):
            ax.annotate(named['sample_id'], (x0, y0 - 3), fontsize=6,
                        color=PREDICTED)

    ax.plot([], [], color=TRUTH, linewidth=1.6, label='true silhouette')
    ax.plot([], [], color=PREDICTED, linewidth=1.6,
            label=f'detector box ({len(proposals)})')
    ax.legend(loc='upper right', frameon=False, fontsize=9, labelcolor=INK)
    ax.set_title(f'The fixed camera at {width} x {height}, '
                 'with what the detector found',
                 color=INK, fontsize=12, loc='left', pad=10)
    fig.tight_layout()
    fig.savefig(out, dpi=170, facecolor=SURFACE)
    plt.close(fig)


def main() -> None:
    """Draw all three figures for one run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path, help='a propose_confirm output dir')
    parser.add_argument('--table', type=Path, default=None,
                        help='a harness lookup_table.json to draw as well')
    parser.add_argument('--scene-name', default='minihannover_rail_scene')
    parser.add_argument('--frame', type=Path, default=None,
                        help='the fixed camera frame; layout_00_general.jpg '
                             'in the run by default')
    args = parser.parse_args()

    bottles, proposals, camera = load(args.run)
    bench(bottles, proposals, args.run / 'bench.png')
    residuals(bottles, proposals, args.run / 'residuals.png')
    detail(bottles, proposals, args.run / 'detail.png')
    if camera:
        anatomy(bottles, proposals, camera, args.run / 'anatomy.png')
    else:
        print('no camera pose in the run; skipping anatomy.png')
    frame = args.frame or args.run / 'layout_00_general.jpg'
    if frame.exists():
        boxes(bottles, proposals, frame, args.run / 'boxes.png')
    else:
        print(f'no frame at {frame}; re-run propose_confirm with --save-frames')
    if args.table and args.table.exists():
        lookup(args.table, args.scene_name, args.run / 'lookup.png')
    found = sum(1 for b in bottles if b.get('error_m') is not None)
    print(f'{found}/{len(bottles)} bottles found, {len(proposals)} boxes; '
          f'wrote bench.png, residuals.png, detail.png and boxes.png '
          f'to {args.run}')




def lookup(table: Path, scene: str, out: Path) -> None:
    """The lookup table the harness ends up with, as a readable page.

    The bench plot shows where the three positions are; this shows what was
    actually written down --- which sample, what it is, where it stands and how
    far that is from the truth. It is the robot's memory, and the thing the
    formula stage reads.

    Args:
        table: A harness lookup_table.json.
        scene: Which scene block to show.
        out: Where to write the figure.
    """
    block = json.loads(table.read_text())['scenes'][scene]
    rows = sorted(block['labels'], key=lambda e: e['position'][0])
    metrics = block['metrics']

    fig, ax = plt.subplots(figsize=(11, 0.34 * len(rows) + 2.1))
    ax.set_facecolor(SURFACE)
    ax.axis('off')
    ax.set_title(f'The lookup table for {scene}', color=INK, fontsize=12,
                 loc='left', pad=22)
    wrong = sum(b['wrong'] for b in metrics['by_decision'].values())
    ax.text(0, 1.0,
            f'{metrics["identified"]} of {metrics["gt_labels"]} identified, '
            f'{wrong} named wrongly, '
            f'median error {metrics["median_error_m"] * 1000:.1f} mm, '
            f'{metrics["confirmed_by_wrist"]} confirmed by the wrist',
            transform=ax.transAxes, color=MUTED, fontsize=9.5)

    columns = ((0.00, 'sample'), (0.13, 'material'), (0.40, 'x'), (0.50, 'y'),
               (0.60, 'ml'), (0.70, 'confidence'), (0.86, 'error'))
    top = 0.94
    for x, head in columns:
        ax.text(x, top, head, transform=ax.transAxes, color=MUTED, fontsize=8.5,
                fontweight='600')
    for i, entry in enumerate(rows):
        y = top - 0.035 - i * (0.90 / max(len(rows), 1))
        error = entry.get('error_m')
        cells = (entry['sample_id'], (entry.get('material') or '')[:24],
                 f'{entry["position"][0]:+.3f}', f'{entry["position"][1]:+.3f}',
                 f'{entry.get("container_ml", 0):.0f}',
                 f'{entry["probability"]:.3f}',
                 '-' if error is None else f'{error * 1000:.1f} mm')
        for (x, _), text in zip(columns, cells, strict=True):
            ax.text(x, y, text, transform=ax.transAxes, fontsize=8.5,
                    color=REFINED if text.startswith('SMP') else INK,
                    family='monospace' if x >= 0.40 else None)
    fig.tight_layout()
    fig.savefig(out, dpi=170, facecolor=SURFACE)
    plt.close(fig)


if __name__ == '__main__':
    main()
