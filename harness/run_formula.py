#!/usr/bin/env python3
"""Scan the bench, then turn a formula into the action heap it makes possible

Two phases, in the order the robot would live them. First the bench is explored
and the lookup table written; only then is the formula read, because which
ingredients are actionable is a fact about the bench, not about the recipe.

**Explore.** The greedy search is the one already in ``vision``: sightings join
the first bottle within ``MERGE_M``, the confirming pass walks the proposals
most-confident-first, and for each it tries bearings until the ring reads and
stops there. Nothing here reimplements it --- this runs
``build_lookup_table.main`` with the arguments it would have been given, so the
table carries its full header, the detector's sha256 and its metrics rather than
a thinner copy that would drift.

**Fall back loudly.** The trained weights are not in git, so on a machine without
them the vision pass cannot start. Rather than stop, the scan drops to
``--method gt`` and says so on stderr and in the report. That table is the
simulator's own labels, not perception: it is a bootstrap, and a run that used it
should never be quoted as evidence that the vision stack works.

**Do not clobber.** ``harness/lookup_table.json`` is committed, 2 MB, and came
from a real scan with weights this machine does not have. The default output goes
to ``simulation/out/`` instead, which is gitignored, and the committed table is
overwritten only when ``--in-place`` asks for it.

The heap is then built from whatever the scan produced, by
``formula_to_actions``, and written beside the table. Nothing here moves the arm:
the run ends with a plan, not a pick.

    simulation/.venv-act/bin/python harness/run_formula.py
    ... run_formula.py FRG-104 --scene minihannover_rail_scene
    ... run_formula.py --method gt        # skip the vision pass outright
    simulation/.venv/bin/python harness/run_formula.py --method gt   # light venv is enough
"""

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_lookup_table as blt  # noqa: E402
import formula_to_actions as f2a  # noqa: E402

OUT_DIR = blt.ROOT / "simulation/out"
SCENES = blt.ROOT / "simulation/models"


def stage(status: str, name: str, message: str) -> None:
    """One line per phase, in the shape verify_lookup_table.Report prints."""
    print(f"{status:4s}  {name:8s} {message}")


def shown(path: Path) -> str:
    """A path to print: repo-relative where it can be, absolute where it cannot.

    --out-dir is free to point anywhere, so relative_to is not always defined.
    """
    return str(path.relative_to(blt.ROOT) if path.is_relative_to(blt.ROOT) else path)


def scene_file(scene: str) -> Path:
    """The MJCF behind a scene, named or given as a path.

    A bare name is looked up in simulation/models; anything with a separator or
    an .xml suffix is taken as written, which is what lets a bench built
    elsewhere --- a pattern population, say --- be scanned without first being
    filed among the generated scenes. Either way the stem is the key the table
    stores the scene under.
    """
    given = Path(scene)
    path = given if given.suffix == ".xml" or given.parent != Path(".") else SCENES / f"{scene}.xml"
    if not path.is_file():
        known = ", ".join(sorted(p.stem for p in SCENES.glob("minihannover*.xml")))
        raise SystemExit(f"no scene at {shown(path)} (names known here: {known})")
    return path.resolve()


def scan(path: Path, out: Path, method: str, backend: str, weights: Path | None,
         device: str | None, confirm: str) -> str:
    """Run build_lookup_table over one scene, dropping to gt if it cannot see.

    Its ``main`` is called rather than its parts: the header it writes carries
    the detector's weights and sha256, the decoder's thresholds and the confirm
    metrics, and a copy of that prose here would be one more thing to keep in
    step. The weights missing is not an error worth stopping for --- it is the
    normal state of a machine that is not Marti's --- so the FileNotFoundError
    that ``labvision.detector.Detector`` raises turns into a second run.

    Returns:
        The method the table was actually built with, which is not always the
        one asked for.
    """
    def run(chosen: str) -> None:
        argv = [str(path), "--method", chosen, "--out", str(out)]
        if chosen == "vision":
            argv += ["--backend", backend, "--confirm", confirm]
            argv += ["--weights", str(weights)] if weights else []
            argv += ["--device", device] if device else []
        held, sys.argv = sys.argv, ["build_lookup_table.py", *argv]
        try:
            blt.main()
        finally:
            sys.argv = held

    if method == "gt":
        run("gt")
        return "gt"
    try:
        run("vision")
        return "vision"
    except FileNotFoundError as exc:
        print(f"warning: the vision pass cannot start: {exc}", file=sys.stderr)
        print("warning: falling back to --method gt, which reads the simulator's "
              "labels instead of perceiving them", file=sys.stderr)
        run("gt")
        return "gt"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("formula", nargs="?", default=f2a.DEFAULT_FORMULA,
                        help=f"formula id, file or path (default {f2a.DEFAULT_FORMULA})")
    parser.add_argument("--scene", default=f2a.DEFAULT_SCENE,
                        help=f"scene to scan and resolve against (default {f2a.DEFAULT_SCENE})")
    parser.add_argument("--method", choices=("auto", "vision", "gt"), default="auto",
                        help="auto tries vision and falls back to gt (default)")
    parser.add_argument("--backend", default="rail", help="labvision.detector backend")
    parser.add_argument("--weights", type=Path, help="override the backend's weights file")
    parser.add_argument("--device", help="torch device, e.g. cuda:0 (default: a GPU if any)")
    parser.add_argument("--confirm", choices=("auto", "arm", "mocap", "off"), default="auto",
                        help="how the confirming camera gets to a bottle (default auto)")
    parser.add_argument("--balance", type=int, default=f2a.DEFAULT_BALANCE,
                        help=f"balance to dose on (default {f2a.DEFAULT_BALANCE})")
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR,
                        help="where both artefacts go (default simulation/out)")
    parser.add_argument("--in-place", action="store_true",
                        help="write the table over the committed harness/lookup_table.json")
    args = parser.parse_args()

    path = scene_file(args.scene)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    table_path = blt.OUT if args.in_place else args.out_dir / "lookup_table.json"

    print(f"scanning {shown(path)}", flush=True)
    method = scan(path, table_path, "gt" if args.method == "gt" else "auto",
                  args.backend, args.weights, args.device, args.confirm)

    table = json.loads(table_path.read_text())
    labels = table["scenes"][path.stem]["labels"]
    print()
    stage("ok" if method == "vision" else "WARN", "scan",
          f"{len(labels)} labels, method {method}"
          + ("" if method == "vision" else
             " --- the simulator's own labels, not perception"))
    stage("ok", "table", shown(table_path))

    out = f2a.build(f2a.load_formula(args.formula), table, path.stem, args.balance)
    heap_path = args.out_dir / f"{out['formula']}_actions.json"
    heap_path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    summary = out["summary"]
    stage("ok" if summary["resolved"] else "WARN", "heap",
          f"{summary['resolved']}/{summary['ingredients']} executable, "
          f"{len(out['actions'])} actions -> {shown(heap_path)}")
    print()
    f2a.report(out)


if __name__ == "__main__":
    main()
