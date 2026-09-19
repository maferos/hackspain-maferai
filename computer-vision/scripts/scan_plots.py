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
* ``boxes.png`` --- the fixed camera's own frame with the detector's boxes on
  it, and the true silhouettes beside them.

Colours are the two ends of a validated categorical pair: blue is truth,
orange is what we predicted. Everything is direct-labelled, so identity never
rests on colour alone.
"""
import argparse
import json
from pathlib import Path

import matplotlib
import numpy as np

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


def load(run: Path) -> tuple[list[dict], list[dict]]:
    """Read one layout's scored bottles and its proposals.

    Args:
        run: Directory holding propose_confirm.json.

    Returns:
        The scored bottles and the proposals.
    """
    layout = json.loads((run / 'propose_confirm.json').read_text())[0]
    return layout['scored']['bottles'], layout['proposals']


EXAGGERATION = 20
"""The errors are a few millimetres on a bench 3.5 m across, so drawn true to
scale the proposal sits exactly on the truth and the figure says nothing. The
offset is drawn this many times over, and the axes stay in real metres so
positions can still be read off."""


def bench(bottles: list[dict], proposals: list[dict], out: Path) -> None:
    """The bench from above: truth against proposal, error exaggerated."""
    named = {p['confirm']['sample_id']: p for p in proposals
             if p.get('confirm') and p['confirm'].get('sample_id')}
    fig, ax = plt.subplots(figsize=(13, 4.4))
    style(ax)

    for bottle in bottles:
        truth = bottle['xy']
        proposal = named.get(bottle['sample_id'])
        if proposal is None:
            ax.plot(*truth, marker='o', markersize=7, color=SURFACE,
                    markeredgecolor=MUTED, markeredgewidth=1.6, zorder=3)
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
        refined = (proposal.get('confirm') or {}).get('refined_xy')
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

    missed = sum(1 for b in bottles if b.get('error_m') is None)
    ax.plot([], [], 'o', color=TRUTH, markersize=6, label='true position')
    ax.plot([], [], 'x', color=PREDICTED, markersize=7, markeredgewidth=1.8,
            label=f'proposed by the fixed camera, offset {EXAGGERATION}x')
    ax.plot([], [], 'D', color=REFINED, markersize=4.5,
            markeredgecolor=SURFACE, markeredgewidth=0.9,
            label=f'refined by the wrist, offset {EXAGGERATION}x')
    if missed:
        ax.plot([], [], 'o', color=SURFACE, markeredgecolor=MUTED,
                markeredgewidth=1.6, markersize=7,
                label=f'not detected ({missed})')
    # Under the axes: the bench is wide and flat, and a legend inside it
    # covers bottles at either end.
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.20), frameon=False,
              fontsize=9, labelcolor=INK, ncol=4)
    ax.set_xlabel('x along the bench (m)', color=MUTED, fontsize=9)
    ax.set_ylabel('y (m)', color=MUTED, fontsize=9)
    ax.set_title('Where the bottles are, where the camera put them, '
                 'and where the wrist corrected them to',
                 color=INK, fontsize=12, loc='left', pad=26)
    ax.text(0, 1.035,
            f'offsets drawn {EXAGGERATION}x, axes in real metres; the wrist '
            'correction still lands on the truth',
            transform=ax.transAxes, color=MUTED, fontsize=9)
    ax.set_aspect('equal')
    fig.tight_layout()
    fig.savefig(out, dpi=170, facecolor=SURFACE)
    plt.close(fig)


def residuals(bottles: list[dict], proposals: list[dict], out: Path) -> None:
    """Errors as offsets, so bias and scatter can be told apart."""
    named = {p['confirm']['sample_id']: p for p in proposals
             if p.get('confirm') and p['confirm'].get('sample_id')}
    rows = [(np.array(named[b['sample_id']]['xy']) - np.array(b['xy']),
             np.array(named[b['sample_id']]['confirm']['refined_xy'])
             - np.array(b['xy']))
            for b in bottles if b['sample_id'] in named]
    proposed = np.array([r[0] for r in rows]) * 1000
    refined = np.array([r[1] for r in rows]) * 1000

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
               label='after the wrist refines')
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
    parser.add_argument('--frame', type=Path, default=None,
                        help='the fixed camera frame; layout_00_general.jpg '
                             'in the run by default')
    args = parser.parse_args()

    bottles, proposals = load(args.run)
    bench(bottles, proposals, args.run / 'bench.png')
    residuals(bottles, proposals, args.run / 'residuals.png')
    frame = args.frame or args.run / 'layout_00_general.jpg'
    if frame.exists():
        boxes(bottles, proposals, frame, args.run / 'boxes.png')
    else:
        print(f'no frame at {frame}; re-run propose_confirm with --save-frames')
    found = sum(1 for b in bottles if b.get('error_m') is not None)
    print(f'{found}/{len(bottles)} bottles found, {len(proposals)} boxes; '
          f'wrote bench.png, residuals.png and boxes.png to {args.run}')


if __name__ == '__main__':
    main()
