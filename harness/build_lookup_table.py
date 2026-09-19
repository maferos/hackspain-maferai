"""Build harness/lookup_table.json: every labelled sample in a MuJoCo scene, keyed
by where its label sits in the world.

Two methods:

``vision`` (default)
    What a robot would see. Every fixed camera is rendered with depth, the
    YOLO26n Martí trained on MuJoCo renders (``labvision.detector`` backend
    ``rail``) proposes bottle boxes, ``labvision.markers`` soft-decodes the ArUco ring
    inside them into a posterior over sample ids, and the depth under the ring
    places the bottle in the world. Each entry carries that posterior as its
    ``probability``, with ``decision`` accept / rescan / reject. See
    ``harness/vision.py``. Entries are scored against the ground truth below,
    and every scene gets a ``metrics`` block.
``gt``
    Ground truth, read from the compiled model: no camera involved.

Any MJCF works. The scene is compiled and stepped through mj_forward, so attached
models, frames and includes are all resolved by MuJoCo itself. For the ground
truth, two ways a sample label shows up in a compiled scene are recognised:

- an attached labelled bottle (assets/labelled_bottles/<ID>.xml): a geom named
  ``<prefix>label`` on a body named ``<prefix><ID>``;
- a shelved bottle baked into a room: a geom named ``...stock_<ID>_label_<n>``
  (minihannover_open) or ``...lib_<ID>_label`` (minihannover).

Each label is matched to its registry row in computer-vision/barcodes/lookup_table.json
(EAN-13, ArUco marker, material, ...).

The ``rail`` weights are trained, not downloaded, and not in git: take
``yolo26n_rail_general.pt`` from the team Drive and drop it in
computer-vision/weights/ (see the README there), or pass ``--weights``. It was
trained on the rail scene's ``general`` camera. Cameras the
model was not trained on show up in ``metrics.per_camera``.

Run with the venv that has mujoco, OpenCV and ultralytics, headless:

    MUJOCO_GL=egl simulation/.venv-act/bin/python harness/build_lookup_table.py
    ... build_lookup_table.py --weights path/to/best.pt --device cuda:0
    ... build_lookup_table.py path/to/scene.xml --cameras general room_desk
    ... build_lookup_table.py --method gt          # only needs mujoco
    ... build_lookup_table.py --save-frames /tmp/frames   # annotated renders
"""

import argparse
import hashlib
import json
import re
import statistics
from pathlib import Path

import mujoco

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "computer-vision/barcodes/lookup_table.json"
OUT = Path(__file__).resolve().parent / "lookup_table.json"
DEFAULT_SCENES = (
    "simulation/models/minihannover_scene.xml",
    "simulation/models/minihannover_open_scene.xml",
    "simulation/models/minihannover_rail_scene.xml",
)

SAMPLE_ID = re.compile(r"(SMP|PWD)-\d{4}")
STOCK_LABEL = re.compile(r"(?:stock|lib)_((?:SMP|PWD)-\d{4})_label(?:_\d+)?$")


def name_of(model, kind, i):
    return mujoco.mj_id2name(model, kind, i) or ""


def label_geoms(model):
    """Yield (geom_id, sample_id, source) for every sample label in the model."""
    for g in range(model.ngeom):
        gname = name_of(model, mujoco.mjtObj.mjOBJ_GEOM, g)
        stock = STOCK_LABEL.search(gname)
        if stock:
            yield g, stock.group(1), "stock"
            continue
        if not gname.endswith("label"):
            continue
        body = name_of(model, mujoco.mjtObj.mjOBJ_BODY, model.geom_bodyid[g])
        prefix = gname[: -len("label")]
        match = SAMPLE_ID.search(body)
        if match and body.startswith(prefix):
            yield g, match.group(0), "attached"


def world_aabb(model, data, g):
    """World-frame bounding box of a mesh geom, from its actual vertices."""
    mesh = model.geom_dataid[g]
    start, count = model.mesh_vertadr[mesh], model.mesh_vertnum[mesh]
    verts = model.mesh_vert[start : start + count]
    world = data.geom_xpos[g] + verts @ data.geom_xmat[g].reshape(3, 3).T
    return world.min(axis=0), world.max(axis=0)


def rounded(v, nd=4):
    return [round(float(x), nd) for x in v]


def load_scene(path):
    model = mujoco.MjModel.from_xml_path(str(path))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    return model, data


def scan_scene(model, data, registry):
    labels = []
    for g, sample_id, source in label_geoms(model):
        lo, hi = world_aabb(model, data, g)
        body = model.geom_bodyid[g]
        # A free-jointed body (loose bottle on the worktop) can move once the sim runs;
        # positions here are the initial ones from the XML.
        movable = bool(
            any(model.jnt_type[j] == mujoco.mjtJoint.mjJNT_FREE
                for j in range(model.njnt)
                if _is_ancestor(model, model.jnt_bodyid[j], body))
        )
        entry = {
            "position": rounded((lo + hi) / 2),
            "aabb_min": rounded(lo),
            "aabb_max": rounded(hi),
            "sample_id": sample_id,
            "geom": name_of(model, mujoco.mjtObj.mjOBJ_GEOM, g),
            "body": name_of(model, mujoco.mjtObj.mjOBJ_BODY, body),
            "source": source,
            "movable": movable,
        }
        row = registry.get(sample_id)
        if row:
            entry.update(row)
        else:
            entry["unregistered"] = True
        labels.append(entry)
    labels.sort(key=lambda e: (e["sample_id"], e["geom"]))
    return labels


def _is_ancestor(model, ancestor, body):
    while body > 0:
        if body == ancestor:
            return True
        body = model.body_parentid[body]
    return False


def load_registry():
    table = json.loads(REGISTRY.read_text())
    return table["version"], {
        e["sample_id"]: {
            "ean13": ean,
            "aruco_marker_id": e["marker_id"],
            "material": e["material"],
            "cas": e["cas"],
            "phase": e["phase"],
            "container_ml": e["container_ml"],
            "lot": e["lot"],
            "vessel_class": e["vessel_class"],
        }
        for ean, e in table["entries"].items()
    }


def vision_labels(scan, truth, registry, by_marker, diameters):
    """Turn the scanned bottles into lookup entries and score them against the truth

    A bottle whose fused posterior is ``accept`` or ``rescan`` becomes a label
    keyed by its most probable id; ``reject`` and bottles with no ring quads are
    listed as unidentified. Each is checked against the ground-truth label
    nearest its position: the id there is what the camera was looking at.
    """
    import numpy as np

    from vision import MATCH_M, to_axis

    gt_ids = [e["sample_id"] for e in truth]
    gt_pos = np.array([e["position"] for e in truth]) if truth else np.zeros((0, 3))

    def sample_of(marker_id):
        return by_marker.get(marker_id, {}).get("sample_id")

    def truth_near(position):
        if not len(gt_pos):
            return None, None
        distance = np.linalg.norm(gt_pos - position, axis=1)
        nearest = int(np.argmin(distance))
        return gt_ids[nearest], float(distance[nearest])

    labels, unidentified, errors = [], [], []
    buckets = {d: {"count": 0, "correct": 0, "wrong": 0, "unverified": 0}
               for d in ("accept", "rescan", "reject")}
    for bottle in scan.bottles:
        surface = bottle.point
        sample_id = sample_of(bottle.marker_id)
        row = registry.get(sample_id, {}) if sample_id else {}
        diameter = diameters.get(row.get("vessel_class"))
        position = (np.median([to_axis(s.camera_position, s.point, diameter)
                               for s in bottle.sightings], axis=0)
                    if diameter else surface)
        spread = max(float(np.linalg.norm(s.point - surface)) for s in bottle.sightings)
        readings = bottle.readings
        entry = {
            "position": rounded(position),
            "surface_point": rounded(surface),
            "sample_id": sample_id,
            "probability": float(f"{bottle.probability:.6g}"),
            "decision": bottle.decision,
            "posterior": [[sample_of(i), float(f"{p:.6g}")] for i, p in bottle.posterior[:3]],
            "quads": {"total": len(readings),
                      "accepted_by_opencv": sum(r.accepted for r in readings)},
            "position_spread_m": round(spread, 4),
            "cameras": sorted({s.camera for s in bottle.sightings}),
        }
        seen_id, seen_distance = truth_near(position)
        if readings:
            bucket = buckets[bottle.decision]
            bucket["count"] += 1
            if seen_distance is None or seen_distance >= MATCH_M:
                bucket["unverified"] += 1
                entry["check"] = "no ground-truth label within 5 cm"
            elif seen_id == sample_id:
                bucket["correct"] += 1
                entry["check"] = "correct"
            else:
                bucket["wrong"] += 1
                entry["check"] = f"wrong: the label here is {seen_id}"
        if sample_id in gt_ids:
            gt = gt_pos[gt_ids.index(sample_id)]
            entry["gt_position"] = rounded(gt)
            entry["error_m"] = round(float(np.linalg.norm(position - gt)), 4)
        entry["views"] = [s.to_json(by_marker) for s in bottle.sightings]

        if bottle.decision == "reject":
            # Refused: the top id is only a guess, and without an identity there is
            # no radius to push the surface point back by.
            entry["position"] = rounded(surface)
            entry["best_guess"] = entry.pop("sample_id")
            entry["sample_id"] = None
            entry.pop("error_m", None), entry.pop("gt_position", None)
            if seen_id is not None:
                entry["nearest_gt"] = {"sample_id": seen_id, "distance_m": round(seen_distance, 4)}
            unidentified.append(entry)
        else:
            entry.update(row)
            if "error_m" in entry and entry.get("check") == "correct":
                errors.append(entry["error_m"])
            labels.append(entry)

    labels.sort(key=lambda e: e["sample_id"])
    metrics = {
        "gt_labels": len(truth),
        "boxes": sum(c["boxes"] for c in scan.per_camera.values()),
        "quads": sum(c["quads"] for c in scan.per_camera.values()),
        "bottles": len(scan.bottles),
        "identified": len(labels),
        "by_decision": buckets,
        "missed": len(set(gt_ids) - {e["sample_id"] for e in labels}),
        "unidentified_vessels": len(unidentified),
        "median_error_m": round(statistics.median(errors), 4) if errors else None,
        "max_error_m": round(max(errors), 4) if errors else None,
        "per_camera": scan.per_camera,
    }
    return labels, unidentified, metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("scenes", nargs="*", default=DEFAULT_SCENES)
    parser.add_argument("--method", choices=("vision", "gt"), default="vision")
    parser.add_argument("--phase", choices=("liquid", "powder"),
                        help="keep only this phase (default: both)")
    parser.add_argument("--cameras", nargs="+",
                        help="cameras to render (default: every fixed camera in the scene)")
    parser.add_argument("--backend", default="rail", help="labvision.detector backend")
    parser.add_argument("--weights", type=Path, help="override the backend's weights file")
    parser.add_argument("--device", help="torch device, e.g. cuda:0 (default: a GPU if any)")
    parser.add_argument("--score", type=float, help="override the detector threshold")
    parser.add_argument("--ean", action="store_true", help="also read EAN-13 inside boxes")
    parser.add_argument("--save-frames", type=Path, help="write annotated frames here")
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()

    version, registry = load_registry()
    scanner = None
    if args.method == "vision":
        from vision import VisionScanner

        manifest = json.loads((ROOT / "simulation/assets/labelled_bottles/manifest.json").read_text())
        diameters = {k: v["diameter_m"] for k, v in manifest["vessels"].items()}
        table = json.loads(REGISTRY.read_text())["entries"]
        scanner = VisionScanner(table, backend=args.backend,
                                weights=str(args.weights) if args.weights else None,
                                score=args.score, device=args.device,
                                read_ean=args.ean, frames_dir=args.save_frames)

    def keep(entries):
        return [e for e in entries if not args.phase or e.get("phase") == args.phase]

    scenes = {}
    for scene in args.scenes:
        path = Path(scene) if Path(scene).is_absolute() else ROOT / scene
        model, data = load_scene(path)
        truth = keep(scan_scene(model, data, registry))
        record = {"file": str(path.relative_to(ROOT))}
        if scanner is None:
            record.update(count=len(truth), labels=truth)
            print(f"{path.stem}: {len(truth)} labels")
        else:
            from vision import fixed_cameras

            cameras = args.cameras or fixed_cameras(model)
            scan = scanner.scan(model, data, path.stem, cameras)
            labels, unidentified, metrics = vision_labels(
                scan, truth, registry, scanner.by_marker, diameters)
            labels = keep(labels)
            record.update(cameras=cameras, count=len(labels), metrics=metrics,
                          labels=labels, unidentified=unidentified)
            print(f"{path.stem}: {metrics['identified']} identified of {metrics['gt_labels']}, "
                  f"median error {metrics['median_error_m']} m, {metrics['boxes']} boxes, "
                  f"{metrics['quads']} quads, {metrics['unidentified_vessels']} unidentified")
            for decision, bucket in metrics["by_decision"].items():
                print(f"    {decision:7s} {bucket}")
            for cam, stats in metrics["per_camera"].items():
                print(f"    {cam:20s} {stats}")
        scenes[path.stem] = record

    header = {"frame": "MuJoCo world, metres, +Z up", "method": args.method}
    if args.method == "gt":
        header["position"] = "centre of the label mesh's world bounding box, at the initial state"
    else:
        from labvision import markers
        from labvision.detector import BACKENDS

        weights = Path(scanner.detector.model.ckpt_path or args.weights
                       or BACKENDS[args.backend].weights)
        digest = hashlib.sha256(weights.read_bytes()).hexdigest() if weights.exists() else None
        if weights.is_absolute() and weights.is_relative_to(ROOT):
            weights = weights.relative_to(ROOT)
        header.update(
            detector=f"labvision.detector backend {args.backend!r}, weights {weights}, "
                     f"score >= {scanner.detector.score}",
            detector_weights={"backend": args.backend, "file": weights.name, "path": str(weights),
                              "sha256": digest, "score": scanner.detector.score},
            decoder=(f"labvision.markers: soft ArUco posterior over the catalogue, every copy "
                     f"of the ring fused across cameras (TEMPER={markers.TEMPER}); "
                     f"accept >= {markers.ACCEPT_P}, rescan >= {markers.REJECT_P}, else reject"),
            probability="posterior that sample_id is the bottle at position, under "
                        "labvision.markers' noise model. NOT calibrated yet: see "
                        "computer-vision/docs/READ_CONFIDENCE.md and metrics.by_decision",
            position="bottle axis at label height: depth under the ring quads, pushed back "
                     "by the bottle radius; surface_point is the raw point",
            position_spread_m="largest distance of one view's point from surface_point",
            gt_position="the ground-truth label centre (method gt), for scoring",
        )
    args.out.write_text(json.dumps({
        **header,
        "registry": str(REGISTRY.relative_to(ROOT)),
        "registry_version": version,
        "scenes": scenes,
    }, indent=2) + "\n")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
