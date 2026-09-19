r"""Build a local HTML page from the fixed-camera benchmark: numbers and examples

Reads ``results/fixedcam/<model>/metrics.json`` and the cached boxes of the
models named on the command line, and writes ``results/fixedcam/report/``:
``index.html`` plus ``img/*.jpg``. The page has, per test split, a table with
intervals, a chart of recall by apparent size, recall by bottle, and example
frames where every model's boxes are drawn on the same worktop crop.

    python scripts/fixedcam_report.py \\
        "coco-yolo26s=YOLO26s COCO (no training)" \\
        "world-l-bottles=YOLO-World L (no training)" \\
        "ft:runs/fixedcam/yolo26n_384/weights/best.pt=YOLO26n fine-tuned"

Each argument is ``<model name>=<label>``; the model name is what was passed
to ``fixedcam_bench.py run``.
"""

import argparse
import html
import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fixedcam_bench as fb  # noqa: E402
import fixedcam_models as fm  # noqa: E402

from labvision import evaluation as ev  # noqa: E402

OUT = fb.RESULTS / "report"
SPLITS = ("test", "test_open", "test_shift", "val")
SPLIT_TITLES = {
    "test": "Main test: gantry scene, nominal light and camera",
    "test_open": "Other scene: open desk, never seen in training",
    "test_shift": "Shifted: strong light changes and a degraded camera",
    "val": "Validation (where the thresholds were chosen)",
}
SERIES = ("--series-1", "--series-2", "--series-3", "--series-4", "--series-5")
EXAMPLES_PER_SPLIT = 3

STYLE = """
:root {
  color-scheme: light;
  --surface-0: #f6f5f2; --surface-1: #fcfcfb; --border: #e2e0da;
  --text-primary: #0b0b0b; --text-secondary: #52514e; --text-muted: #77756f;
  --grid: #e9e7e1;
  --series-1: #2a78d6; --series-2: #eb6834; --series-3: #1baf7a;
  --series-4: #eda100; --series-5: #e87ba4;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --surface-0: #121211; --surface-1: #1a1a19; --border: #33332f;
    --text-primary: #ffffff; --text-secondary: #c3c2b7; --text-muted: #96958c;
    --grid: #2a2a27;
    --series-1: #3987e5; --series-2: #d95926; --series-3: #199e70;
    --series-4: #c98500; --series-5: #d55181;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --surface-0: #121211; --surface-1: #1a1a19; --border: #33332f;
  --text-primary: #ffffff; --text-secondary: #c3c2b7; --text-muted: #96958c;
  --grid: #2a2a27;
  --series-1: #3987e5; --series-2: #d95926; --series-3: #199e70;
  --series-4: #c98500; --series-5: #d55181;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--surface-0); color: var(--text-primary);
  font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 1120px; margin: 0 auto; padding: 24px 16px 64px; }
h1 { font-size: 26px; margin: 8px 0 4px; }
h2 { font-size: 20px; margin: 40px 0 8px; }
h3 { font-size: 16px; margin: 24px 0 8px; color: var(--text-secondary); }
p.lead { color: var(--text-secondary); max-width: 760px; }
.card { background: var(--surface-1); border: 1px solid var(--border);
  border-radius: 10px; padding: 16px; margin: 12px 0; overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-variant-numeric: tabular-nums; }
th, td { text-align: right; padding: 6px 10px; border-bottom: 1px solid var(--grid);
  white-space: nowrap; }
th:first-child, td:first-child { text-align: left; }
th { color: var(--text-secondary); font-weight: 600; font-size: 13px; }
td.best { font-weight: 700; }
.swatch { display: inline-block; width: 10px; height: 10px; border-radius: 2px;
  margin-right: 6px; vertical-align: middle; }
.legend { display: flex; flex-wrap: wrap; gap: 14px; font-size: 13px;
  color: var(--text-secondary); margin: 4px 0 8px; }
svg text { fill: var(--text-secondary); font-size: 12px; }
.card svg { max-width: 760px; display: block; }
svg .axis { stroke: var(--border); }
svg .gridline { stroke: var(--grid); }
.tip { position: fixed; pointer-events: none; background: var(--surface-1);
  border: 1px solid var(--border); border-radius: 6px; padding: 6px 8px;
  font-size: 12px; color: var(--text-primary); display: none; z-index: 9; }
.examples { display: grid; gap: 10px; }
.examples figure { margin: 0; }
.examples img { width: 100%; height: auto; border-radius: 6px;
  border: 1px solid var(--border); display: block; }
figcaption { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
.key { font-size: 13px; color: var(--text-secondary); }
.key b.g { color: #1baf7a; } .key b.m { color: #d020d0; }
.key b.r { color: #e34948; } .key b.k { color: #8a8a8a; }
"""

SCRIPT = """
const tip = document.querySelector('.tip');
document.querySelectorAll('[data-tip]').forEach(el => {
  el.addEventListener('mousemove', e => {
    tip.textContent = el.dataset.tip; tip.style.display = 'block';
    tip.style.left = (e.clientX + 12) + 'px'; tip.style.top = (e.clientY + 12) + 'px';
  });
  el.addEventListener('mouseleave', () => { tip.style.display = 'none'; });
});
"""


def pct(x: float | None) -> str:
    """Format a proportion as a percentage"""
    return "-" if x is None or x != x else f"{100 * x:.1f} %"


def ci(pair) -> str:
    """Format a 95 % interval as percentages"""
    if not pair:
        return ""
    return f"<br><span class='key'>{100 * pair[0]:.0f}-{100 * pair[1]:.0f}</span>"


def metrics_table(models: list[tuple[str, str, dict]], split: str) -> str:
    """Return the per-split table of every model's headline numbers"""
    rows = [(label, m[split]["worktop"], k) for k, (_, label, m) in enumerate(models)
            if split in m]  # fmt: skip
    if not rows:
        return "<p class='key'>Not scored on this split.</p>"
    best_ap = max(r[1]["ap50"] for r in rows)
    best_recall = max(r[1]["recall"] for r in rows)
    head = (
        "<tr><th>model</th><th>frames</th><th>AP50</th><th>AP50:95</th><th>recall</th>"
        "<th>precision</th><th>false boxes / frame</th><th>threshold</th>"
        "<th>s / frame (CPU)</th></tr>"
    )
    body = []
    for label, w, k in rows:
        body.append(
            "<tr>"
            f"<td><span class='swatch' style='background:var({SERIES[k]})'></span>"
            f"{html.escape(label)}</td>"
            f"<td>{w['frames']}</td>"
            f"<td class='{'best' if w['ap50'] == best_ap else ''}'>{pct(w['ap50'])}"
            f"{ci(w.get('ap50_ci'))}</td>"
            f"<td>{pct(w['ap'])}</td>"
            f"<td class='{'best' if w['recall'] == best_recall else ''}'>"
            f"{pct(w['recall'])}{ci(w.get('recall_ci'))}</td>"
            f"<td>{pct(w['precision'])}</td>"
            f"<td>{w['false_per_frame']:.2f}</td>"
            f"<td>{w['threshold']:.3f}</td>"
            f"<td>{w['ms_median'] / 1000:.1f}</td>"
            "</tr>"
        )
    note = (
        "<p class='key'>Models may be scored on different numbers of frames (the "
        "first N of the split); the write-up compares them on the same frames. "
        "Intervals: 95 % bootstrap over frames. Threshold: best F1 on val. "
        "Latency was measured on a throttled, shared CPU.</p>"
    )
    return f"<table>{head}{''.join(body)}</table>{note}"


def size_chart(models: list[tuple[str, str, dict]], split: str) -> str:
    """Return an SVG line chart of recall by apparent size, one line per model"""
    buckets = ev.side_buckets()
    width, height, left, right, top, bottom = 640, 260, 44, 150, 12, 36
    plot_w, plot_h = width - left - right, height - top - bottom
    step = plot_w / (len(buckets) - 1)

    def y(v: float) -> float:
        return top + plot_h * (1 - v)

    parts = [f"<svg viewBox='0 0 {width} {height}' width='100%' role='img' "
             f"aria-label='Recall by apparent size, {split}'>"]  # fmt: skip
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        parts.append(f"<line class='gridline' x1='{left}' x2='{left + plot_w}' "
                     f"y1='{y(v):.1f}' y2='{y(v):.1f}'/>")  # fmt: skip
        parts.append(f"<text x='{left - 6}' y='{y(v) + 4:.1f}' "
                     f"text-anchor='end'>{int(v * 100)}%</text>")  # fmt: skip
    for i, b in enumerate(buckets):
        parts.append(f"<text x='{left + i * step:.1f}' y='{height - 14}' "
                     f"text-anchor='middle'>{b}</text>")  # fmt: skip
    parts.append(f"<text x='{left + plot_w / 2:.1f}' y='{height - 1}' "
                 "text-anchor='middle'>bottle side in the frame</text>")  # fmt: skip
    ends: list[tuple[float, float, int, str]] = []
    for k, (_, label, m) in enumerate(models):
        if split not in m:
            continue
        table = m[split]["worktop"]["by_side"]
        points = [
            (left + i * step, y(table[b][0] / table[b][1]), b, table[b])
            for i, b in enumerate(buckets)
            if b in table and table[b][1]
        ]
        if not points:
            continue
        path = " ".join(f"{'M' if j == 0 else 'L'}{x:.1f},{yy:.1f}"
                        for j, (x, yy, _, _) in enumerate(points))  # fmt: skip
        colour = f"var({SERIES[k]})"
        parts.append(f"<path d='{path}' fill='none' stroke='{colour}' "
                     "stroke-width='2' stroke-linejoin='round'/>")  # fmt: skip
        for x, yy, b, (found, need) in points:
            tip = f"{label}: {b}, {found}/{need} found ({100 * found / need:.0f} %)"
            parts.append(
                f"<circle cx='{x:.1f}' cy='{yy:.1f}' r='4.5' fill='{colour}' "
                f"stroke='var(--surface-1)' stroke-width='2' "
                f"data-tip='{html.escape(tip, quote=True)}'/>"
            )
        ends.append((points[-1][1], points[-1][0], k, label))
    # Direct labels at the line ends, pushed apart so they never overlap.
    placed: list[float] = []
    for yy, x, _k, label in sorted(ends):
        y_text = max(yy + 4, (placed[-1] + 15) if placed else top)
        placed.append(y_text)
        short = label.split(" (")[0].split(",")[0]
        parts.append(
            f"<text x='{x + 10:.1f}' y='{y_text:.1f}' "
            f"style='fill:var(--text-primary)'>{html.escape(short)}</text>"
        )
    parts.append("</svg>")
    legend = "".join(
        f"<span><span class='swatch' style='background:var({SERIES[k]})'></span>"
        f"{html.escape(label)}</span>"
        for k, (_, label, _) in enumerate(models)
    )
    return f"<div class='legend'>{legend}</div>{''.join(parts)}"


def kind_table(models: list[tuple[str, str, dict]], split: str) -> str:
    """Return a table of recall per bottle kind and size"""
    present = [(label, m[split]["worktop"]["by_kind"]) for _, label, m in models
               if split in m]  # fmt: skip
    if not present:
        return ""
    head = (
        "<tr><th>bottle</th>"
        + "".join(
            f"<th>{html.escape(label.split(' (')[0])}</th>" for label, _ in present
        )
        + "<th>n</th></tr>"
    )
    body = []
    for kind in ev.KINDS:
        cells = []
        n = 0
        for _, table in present:
            found, need = table.get(kind, (0, 0))
            n = max(n, need)
            cells.append(f"<td>{pct(found / need) if need else '-'}</td>")
        if n:
            body.append(f"<tr><td>{kind}</td>{''.join(cells)}<td>{n}</td></tr>")
    return f"<table>{head}{''.join(body)}</table>"


def example_images(
    models: list[tuple[str, str, dict]], split: str, count: int
) -> list[tuple[str, str]]:
    """Draw every model's boxes on the worktop crop of a few frames of a split

    Frames are picked evenly through the split. Each model's crop is drawn at
    its own val threshold and stacked one under the other.
    """
    folder, gt = fb.load_split(split)
    worktop = ev.Worktop.from_gt(gt)
    caches = {}
    for name, _, metrics in models:
        path = fb.RESULTS / fb.slug(name) / split / "predictions.json"
        if split in metrics and path.exists():
            caches[name] = json.loads(path.read_text(encoding="utf-8"))
    # Only frames every scored model has boxes for, spread evenly.
    frames = [f for f in gt["frames"] if all(f["file"] in c for c in caches.values())]
    if not frames:
        return []
    picks = np.linspace(0, len(frames) - 1, count + 2)[1:-1].astype(int)
    out = []
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    for index in picks:
        frame = frames[int(index)]
        u0, v0, u1, v1 = fm.worktop_roi(frame, worktop, margin_px=8)
        rows = []
        for name, label, metrics in models:
            cache = caches.get(name)
            if cache is None:
                continue
            threshold = metrics[split]["worktop"]["threshold"]
            dets = [d for d in fb.detections(cache[frame["file"]])
                    if ev.on_worktop(frame, d.box, worktop)]  # fmt: skip
            path = OUT / "img" / "_tmp.jpg"
            fb.draw_overlay(folder, frame, dets, threshold, path)
            image = cv2.imread(str(path))[v0:v1, u0:u1]
            banner = np.full((26, image.shape[1], 3), 250, np.uint8)
            cv2.putText(banner, label, (8, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                        (30, 30, 30), 1, cv2.LINE_AA)  # fmt: skip
            rows.append(np.vstack([banner, image]))
        if not rows:
            continue
        name = f"{split}_{Path(frame['file']).stem}.jpg"
        cv2.imwrite(str(OUT / "img" / name), np.vstack(rows),
                    [cv2.IMWRITE_JPEG_QUALITY, 82])  # fmt: skip
        required = sum(t.required for t in ev.truths_of(frame))
        out.append((name, f"{frame['file']}: {required} bottles to find"))
    tmp = OUT / "img" / "_tmp.jpg"
    if tmp.exists():
        tmp.unlink()
    return out


def build(models: list[tuple[str, str]]) -> Path:
    """Write the page for the given (model name, label) pairs"""
    loaded = []
    for name, label in models:
        path = fb.RESULTS / fb.slug(name) / "metrics.json"
        if not path.exists():
            print(f"skipping {name}: no {path}")
            continue
        loaded.append((name, label, json.loads(path.read_text(encoding="utf-8"))))
    sections = []
    for split in SPLITS:
        if not any(split in m for _, _, m in loaded):
            continue
        body = [f"<h2>{html.escape(SPLIT_TITLES[split])}</h2>",
                f"<div class='card'>{metrics_table(loaded, split)}</div>"]  # fmt: skip
        if split != "val":
            body += [
                "<h3>Recall by apparent size</h3>",
                f"<div class='card'>{size_chart(loaded, split)}</div>",
                "<h3>Recall by bottle</h3>",
                f"<div class='card'>{kind_table(loaded, split)}</div>",
                "<h3>Examples</h3>",
                "<p class='key'><b class='g'>green</b> found, <b class='m'>magenta"
                "</b> missed, <b class='r'>red</b> false box, <b class='k'>grey</b>"
                " bottle not required (shelf, hidden or cut by the border).</p>",
            ]
            figures = "".join(
                f"<figure><img loading='lazy' src='img/{n}' alt='{html.escape(c)}'>"
                f"<figcaption>{html.escape(c)}</figcaption></figure>"
                for n, c in example_images(loaded, split, EXAMPLES_PER_SPLIT)
            )
            body.append(f"<div class='examples'>{figures}</div>")
        sections.append("".join(body))
    page = (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>Fixed-camera detector benchmark</title>"
        f"<style>{STYLE}</style></head><body><main>"
        "<h1>Fixed-camera bottle detection</h1>"
        "<p class='lead'>Sample bottles on the bench seen by the wall GoPro "
        "(1920 x 1080, 3-4 m away) in MuJoCo renders with exact truth. Every "
        "model is scored the same way, after the worktop filter; see "
        "<code>computer-vision/docs/FIXED_CAMERA_BENCHMARK.md</code>.</p>"
        f"{''.join(sections)}<div class='tip'></div>"
        f"<script>{SCRIPT}</script></main></body></html>"
    )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    return OUT / "index.html"


def main() -> None:
    """Parse ``name=label`` arguments and build the page"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("models", nargs="+", help="<model name>=<label>")
    args = parser.parse_args()
    pairs = []
    for item in args.models:
        name, _, label = item.rpartition("=")
        pairs.append((name, label))
    print(build(pairs))


if __name__ == "__main__":
    main()
