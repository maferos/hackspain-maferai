"""Plan the current order as the harness's action heap, against the live bench.

``harness/formula_to_actions`` turns a formula into every primitive the robot
would run: ten verbs an ingredient, each with a line of English a VLA is trained
on and a flag for whether a skill exists behind it. It was written for a bench
read once into ``harness/lookup_table.json``; this feeds it the bench the
viewer's scan is looking at right now instead, so the panel plans against what
is really there rather than a file from another machine.

Nothing here reimplements the planner. Two adapters and a mapping:

- ``labels`` turns the scan's shelf into the entries ``resolve`` reads. It wants
  ``sample_id`` and ``position``; everything else it takes with ``.get``.
- ``liftable`` asks the compiled scene which bottles have a free joint, the same
  question ``formula_to_actions.liftable`` asks, but of the model already in
  memory rather than one loaded from disk. Without a scene it says every flask
  is liftable rather than none: "welded scenery" is a claim, and a plan should
  not make it about a bench it never looked at.
- ``STEP_OF`` says which of the executor's six steps owns each of the ten verbs.
  The five before ``pick`` all belong to ``locate`` because that is honestly what
  the scan does: travelling, approaching and reading the ring are one act, and
  they finish together when the flask is named.

The heap is planned once, when the order is made, and does not move afterwards:
it is the plan, and what happens to it is the steps' business.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
for extra in (REPO / "harness", REPO / "simulation" / "scripts"):
    if str(extra) not in sys.path:
        sys.path.insert(0, str(extra))

import formula_to_actions as f2a  # noqa: E402
import rail_kinematics as rk  # noqa: E402

# Which executor step crosses off each verb of the heap. Everything up to the
# pick is the scan naming the flask; the rest is one for one.
STEP_OF = {
    "locate": "locate", "traverse": "locate", "approach": "locate",
    "read_barcode": "locate", "verify_id": "locate",
    "pick": "pick", "move_to_balance": "carry", "dose": "dose",
    "verify_mass": "verify", "return": "return",
}
# The scan reads a ring at the flask's label, not at its foot. The shelf is a
# bench map in x and y only, so the height is the bench's.
LABEL_Z = 0.98


def labels(shelf: list[dict]) -> list[dict]:
    """The scan's shelf as ``formula_to_actions.resolve`` reads a lookup table.

    Args:
        shelf: From ``catalogue.shelf_from_tracks``.

    Returns:
        One entry per named flask, with the fields ``resolve`` and ``choose``
        look at: the id, where it stands, how big it is and how sure the ring
        read was.
    """
    return [{
        "sample_id": v["sampleId"],
        "position": [v["x"], v["y"], LABEL_Z],
        "container_ml": v.get("containerMl"),
        "probability": v.get("probability"),
        "position_spread_m": v.get("spreadM"),
    } for v in shelf]


def liftable(model, data) -> set[str]:
    """Sample ids the gripper could move, from the scene already compiled.

    The welded ``room_stock_*`` stock reads identically to a bottle standing
    loose, so this is the only thing that tells a plan the arm can run from one
    it cannot.
    """
    try:
        return {b.sample_id for b in rk.bottles(model, data) if b.dynamic}
    except Exception:                                   # a scene rk cannot read
        return set()


def heap(doc: dict, shelf: list[dict], model=None, data=None,
         scene: str = "the bench", balance: int = 2) -> dict | None:
    """The order's every primitive, planned against the bench as it is now.

    Args:
        doc: The order in the ``harness/formulas`` shape (``workflow.formula_json``).
        shelf: From ``catalogue.shelf_from_tracks``.
        model: The compiled scene, for which bottles have a free joint.
        data: Its state.
        scene: Named in the reason an ingredient could not be placed.
        balance: The balance the doses go to, by number.

    Returns:
        ``{"legs", "actions", "summary"}``, or None if the planner could not run
        — a missing field or a scene it cannot read is not worth failing an
        order over, since the six steps carry the run either way.
    """
    ingredients = doc.get("ingredients") or []
    if not ingredients:
        return None
    # `note` is a perfumer's mark on a written formula; one typed into the chat
    # has none, and the planner only passes it through.
    formula = {"ingredients": [{**i, "note": i.get("note") or ""} for i in ingredients]}
    entries = labels(shelf)
    free = liftable(model, data) if model is not None else set()
    if not free:
        # Nothing known about joints: assume the bench is pickable rather than
        # report every flask as welded, which is the louder of the two errors.
        free = {e["sample_id"] for e in entries}
    try:
        legs = f2a.resolve(formula, entries, free, scene)
        flat = f2a.actions(legs, balance)
    except (KeyError, TypeError, ValueError):
        return None
    for action in flat:
        action["step"] = STEP_OF.get(action["verb"])
    return {
        "legs": legs,
        "actions": flat,
        "summary": {
            "ingredients": len(legs),
            "resolved": sum(l["status"] == "resolved" for l in legs),
            "unliftable": sum(l["status"] == "unliftable" for l in legs),
            "missing": sum(l["status"] == "missing" for l in legs),
            "executable": sum(bool(a["executable"]) for a in flat),
            "actions": len(flat),
        },
    }
