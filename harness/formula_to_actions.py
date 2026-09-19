#!/usr/bin/env python3
"""Turn a formula into a heap of grounded actions: what to fetch, from where, in what words

``build_formulas.py`` writes what to make; ``build_lookup_table.py`` writes what is
on the bench and where. Neither knows about the other, and nothing reads the
formulas at all. This joins them: a formula id in, and out comes every ingredient
resolved to a real bottle, a real world position, and a line of English a robot
can be told.

**Resolve.** A formula ingredient already carries the five sample ids that hold
it --- one per flask size, because the catalogue is a 40 x 5 cross product. Only
some of those are on any given bench, so the candidates are intersected with the
scene's scanned labels and one is chosen: the smallest flask that can supply the
dose (at ``pipetting.DENSITY``, since the formula weighs grams and the flask is
sized in millilitres), preferring bottles the gripper can actually lift, and
settling ties on the ring decoder's posterior.

**Three outcomes, not two.** An ingredient is ``resolved`` only if its bottle is
a free body. The rail bench also carries welded scenery: seven of its nineteen
labelled samples are baked into the room and have no joint to move, so they are
``unliftable`` --- their position is known and their identity is certain, but a
pick would fail. Everything else is ``missing``. Nothing is dropped, because a
formula that quietly loses half its ingredients is a different formula.

**Two kinds of English, for two readers.** Each ingredient gets one ``prompt``,
phrased the way ``armlab.planner``'s offline grammar parses it, so it runs today
against the real arm. Each action also gets its own ``instruction``, one
primitive each, in the register a VLA is trained on (see AutoBio's task
prefixes): lower case, imperative, definite article, no full stop, and short
enough to survive pi0's 48-token prompt budget. Coordinates never appear in
either --- a VLA grounds position in the image, not in the prompt, and the
numbers are in the structured fields beside it.

Only ``pick`` and the move to the balance map onto skills that exist
(``armlab.skills.SKILLS``). Dosing, taring and weighing do not: the dashboard
shows those steps but no one has implemented them, and ``pipetting.py`` has
aspirate and dispense but nothing that weighs. Those actions are emitted with
``executable`` false rather than invented.

Nothing here renders or detects, so it needs only mujoco and the table: the plain
``simulation/.venv`` runs it, no GL context and no torch.

    simulation/.venv/bin/python harness/formula_to_actions.py
    ... formula_to_actions.py FRG-104 --out actions.json
    ... formula_to_actions.py FRG-101 --scene minihannover_scene
    ... formula_to_actions.py --spec          # the instruction vocabulary alone
"""

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_lookup_table import OUT, ROOT, load_scene  # noqa: E402

sys.path.insert(0, str(ROOT / "simulation/scripts"))
import rail_kinematics as rk  # noqa: E402
from pipetting import DENSITY  # noqa: E402

FORMULAS = HERE / "formulas"
DEFAULT_FORMULA = "FRG-101"
DEFAULT_SCENE = "minihannover_rail_scene"
DEFAULT_BALANCE = 2        # as in labbridge's ACTIVE_BALANCE

#: A prompt over this many words is at risk of pi0's 48-token cap (tokenizer.py
#: MAX_LEN). Sub-word pieces and the leading BOS mean tokens outrun words, so the
#: budget is checked in words with room to spare rather than guessed exactly.
MAX_PROMPT_WORDS = 30

#: One leg of a formula, in the order the dashboard shows them
#: (labbridge.mock_run.STEP_LABELS).
ORDER = ("locate", "traverse", "approach", "read_barcode", "verify_id",
         "pick", "move_to_balance", "dose", "verify_mass", "return")

#: The verbs an armlab skill carries out (armlab.skills.SKILLS). The rest are
#: narrative: the dashboard shows them, but nothing implements them.
SKILLS = {"pick": "pick", "move_to_balance": "place"}

#: The instruction vocabulary --- the whole contract with the model, in one
#: place. A VLA has no system prompt to explain the task in: pi0 takes a single
#: string, padded or truncated to 48 tokens, with no role to hold a preamble
#: (``openpi.models.tokenizer.PaligemmaTokenizer``), and armlab hands that string
#: over untouched (``armlab.policies.BoundPolicy.observe``). What stands in for
#: the preamble is this table being *frozen*: whatever phrasing labels the
#: demonstrations is the phrasing the policy answers to, so training and
#: inference have to read from here alike. Print it with ``--spec``.
#:
#: Fields: ``name`` the compound in lower case, ``it`` how to refer to the
#: bottle (its id, or the compound where the bench has no sample), ``named``
#: both together, ``grams`` the dose, ``balance`` which balance.
TEMPLATES = {
    "locate": "find the flask of {name} on the bench",
    "traverse": "move along the rail to the flask of {name}",
    "approach": "bring the wrist camera up to {it}",
    "read_barcode": "read the barcode on {it} with the wrist camera",
    "verify_id": "check that {it} is the flask of {name}",
    "pick": "pick up {named}",
    "move_to_balance": "put it down at balance {balance}",
    "dose": "dose {grams:.3f} g of {name}",
    "verify_mass": "check the balance reads {grams:.3f} g",
    "return": "put the flask of {name} back on the bench",
}


def load_formula(name: str) -> dict:
    """Read a formula by id, filename or path."""
    for candidate in (Path(name), FORMULAS / name, FORMULAS / f"{name}.json"):
        if candidate.is_file():
            return json.loads(candidate.read_text())
    known = ", ".join(sorted(p.stem for p in FORMULAS.glob("FRG-*.json")))
    raise SystemExit(f"no formula {name!r} in {FORMULAS.relative_to(ROOT)} (have: {known})")


def liftable(scene_file: str) -> set[str]:
    """Sample ids with a free joint, the only ones a gripper can move.

    The lookup table does not record this: it is a property of the scene, not of
    the reading. Welded stock appears in the same scan as ``room_stock_*`` geoms
    and would otherwise look identical to a bottle standing loose on the bench.
    """
    model, data = load_scene(ROOT / scene_file)
    return {b.sample_id for b in rk.bottles(model, data) if b.dynamic}


def choose(candidates: list[dict], grams: float, free: set[str]) -> dict | None:
    """The bottle to send the arm to, out of the ones this bench has.

    Liftable first --- an unliftable bottle is a fact to report, never a choice
    to make. Then the smallest flask that holds the dose, so the arm carries a
    10 ml flask for 0.03 g of Carvone rather than a 100 ml one. A flask too small
    for the dose still beats nothing, so capacity sorts as a boolean and size
    breaks it; the decoder's posterior settles the rest.
    """
    if not candidates:
        return None
    millilitres = grams / DENSITY
    return min(candidates, key=lambda e: (
        e["sample_id"] not in free,
        (e.get("container_ml") or 0.0) < millilitres,
        e.get("container_ml") or 0.0,
        -(e.get("probability") or 0.0),
        e.get("position_spread_m") or 0.0,
    ))


def phrase(verb: str, compound: str, grams: float, sample: str | None, balance: int) -> str:
    """Fill one template, in the register a VLA is trained on.

    Where the bench has no sample the id drops out of the sentence rather than
    being replaced by a placeholder: an instruction naming a bottle that is not
    there is worse than one that only names the compound.
    """
    name = compound.lower()
    return TEMPLATES[verb].format(
        name=name,
        it=sample or f"the flask of {name}",
        named=f"{sample}, the flask of {name}" if sample else f"the flask of {name}",
        grams=grams,
        balance=balance,
    )


def resolve(formula: dict, labels: list[dict], free: set[str], scene: str) -> list[dict]:
    """Every ingredient with its bottle, largest dose first.

    The ingredient array is authoring order, not dosing order --- FRG-103 lists
    Benzyl acetate at 6.0 % before Benzyl benzoate at 6.5 % --- so it is sorted
    here. Heaviest first is the perfumer's order: the small corrections go in
    last, onto a balance that is already carrying most of the batch.
    """
    by_id = {e["sample_id"]: e for e in labels}     # unique per scene, see verify_lookup_table
    out = []
    for i, ing in enumerate(sorted(formula["ingredients"],
                                   key=lambda x: -x["batch_g"])):
        grams = ing["batch_g"]
        found = [by_id[s] for s in ing["samples"] if s in by_id]
        entry = choose(found, grams, free)
        leg = {
            "i": i,
            "compound": ing["material"],
            "cas": ing["cas"],
            "grams": grams,
            "concentrate_pct": ing["concentrate_pct"],
            "note": ing["note"],
        }
        if entry is None:
            first, last = ing["samples"][0], ing["samples"][-1]
            leg |= {"status": "missing", "sample": None, "xyz": None,
                    "why": f"no {first}..{last[-4:]} in {scene}"}
        else:
            lifts = entry["sample_id"] in free
            leg |= {
                "status": "resolved" if lifts else "unliftable",
                "sample": entry["sample_id"],
                "container_ml": entry.get("container_ml"),
                "ean13": entry.get("ean13"),
                "aruco_marker_id": entry.get("aruco_marker_id"),
                "xyz": entry["position"],
                "rail_x": entry["position"][0],
                "probability": entry.get("probability"),
            }
            if not lifts:
                leg["why"] = f"{entry['sample_id']} is welded scenery, it has no free joint"
        out.append(leg)
    return out


def actions(legs: list[dict], balance: int) -> list[dict]:
    """The flat heap: every leg expanded into its primitives."""
    out = []
    for leg in legs:
        runnable = leg["status"] == "resolved"
        for verb in ORDER:
            skill = SKILLS.get(verb)
            action = {
                "i": len(out),
                "leg": leg["i"],
                "verb": verb,
                "status": leg["status"],
                "compound": leg["compound"],
                "grams": leg["grams"],
                "sample": leg["sample"],
                "xyz": leg["xyz"],
                "instruction": phrase(verb, leg["compound"], leg["grams"],
                                      leg["sample"], balance),
            }
            if skill and runnable:
                args = ({"sample_id": leg["sample"]} if skill == "pick"
                        else {"target_id": f"balance_{balance}"})
                action |= {"skill": skill, "args": args, "executable": True}
            else:
                action |= {"skill": None, "args": {}, "executable": False}
            out.append(action)
    return out


def build(formula: dict, table: dict, scene: str, balance: int) -> dict:
    if scene not in table["scenes"]:
        raise SystemExit(f"no scene {scene!r} in the table (have: "
                         f"{', '.join(sorted(table['scenes']))})")
    block = table["scenes"][scene]
    free = liftable(block["file"])
    legs = resolve(formula, block["labels"], free, scene)
    counts = {s: sum(1 for l in legs if l["status"] == s)
              for s in ("resolved", "unliftable", "missing")}
    for leg in legs:
        # Grammar-executable only where there is something to pick: armlab's
        # offline parser needs the pick and the destination in one sentence.
        leg["prompt"] = (f"pick up {leg['sample']} and bring it to balance {balance}"
                         if leg["status"] == "resolved" else None)
    return {
        "formula": formula["id"],
        "name": formula["name"],
        "product": formula["product"],
        "scene": scene,
        "scene_file": block["file"],
        "balance": f"balance_{balance}",
        "batch_g": formula["batch"]["concentrate_g"],
        "solvent": formula["solvent"]["material"],
        "ethanol_g": formula["batch"]["ethanol_g_for_product"],
        "summary": {"ingredients": len(legs), **counts,
                    "liftable_in_scene": len(free), "labelled_in_scene": len(block["labels"])},
        "ingredients": legs,
        "actions": actions(legs, balance),
    }


def report(out: dict) -> None:
    s = out["summary"]
    print(f"{out['formula']}  {out['name']}  ->  {out['scene']}")
    for leg in out["ingredients"]:
        mark = {"resolved": "ok  ", "unliftable": "WELD", "missing": "----"}[leg["status"]]
        where = leg["sample"] or "-"
        ml = f"{leg['container_ml']:.0f} ml" if leg.get("container_ml") else ""
        print(f"  {mark}  {leg['compound'][:26]:26s} {leg['grams']:7.3f} g  "
              f"{where:9s} {ml:7s} {leg.get('why', '')}")
    print(f"  {s['resolved']}/{s['ingredients']} executable, "
          f"{s['unliftable']} unliftable, {s['missing']} not on this bench; "
          f"{len(out['actions'])} actions")
    if not s["liftable_in_scene"]:
        print(f"  note: {out['scene']} has no free bodies at all --- its whole population is "
              f"baked into the room, and it carries no arm. Resolve against a rail scene to "
              f"get anything executable.")


def spec(balance: int) -> None:
    """Print the instruction vocabulary: the contract, and an example of each.

    Read this as the task list a demonstration set has to be labelled with. The
    policy has no other description of its job, so a template reworded after the
    demonstrations were recorded is a different task to it, however small the
    edit looks.
    """
    missing = set(ORDER) ^ set(TEMPLATES)
    if missing:
        raise SystemExit(f"ORDER and TEMPLATES disagree on: {', '.join(sorted(missing))}")
    print("Instruction templates, in the order one ingredient is worked through.")
    print("Fields: {name} compound, {it} bottle id, {named} both, {grams} dose, "
          "{balance} balance.\n")
    for verb in ORDER:
        skill = SKILLS.get(verb)
        print(f"  {verb:16s} {'-> armlab.' + skill if skill else 'narrative':20s} "
              f"{TEMPLATES[verb]}")
    print("\nFilled, for 1.600 g of Linalyl acetate held in SMP-0093:\n")
    for verb in ORDER:
        line = phrase(verb, "Linalyl acetate", 1.6, "SMP-0093", balance)
        print(f"  {len(line.split()):2d}w  {line}")
    print("\nAnd where the bench has no sample for it:\n")
    for verb in ("approach", "pick"):
        print(f"      {phrase(verb, 'Limonene', 2.54, None, balance)}")
    print(f"\nThe ingredient-level prompt, which armlab's offline grammar parses into\n"
          f"[pick, place, home]:\n\n      pick up SMP-0093 and bring it to balance {balance}\n")
    print(f"Keep every line under {MAX_PROMPT_WORDS} words: pi0 pads or truncates the "
          f"prompt to 48\ntokens and only warns when it cuts.")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("formula", nargs="?", default=DEFAULT_FORMULA,
                        help=f"formula id, file or path (default {DEFAULT_FORMULA})")
    parser.add_argument("--scene", default=DEFAULT_SCENE,
                        help=f"scene in the table to resolve against (default {DEFAULT_SCENE})")
    parser.add_argument("--table", type=Path, default=OUT,
                        help="lookup table to read (default harness/lookup_table.json)")
    parser.add_argument("--balance", type=int, default=DEFAULT_BALANCE,
                        help=f"balance to dose on (default {DEFAULT_BALANCE})")
    parser.add_argument("--out", type=Path, help="write the JSON here (default: stdout)")
    parser.add_argument("--spec", action="store_true",
                        help="print the instruction templates and exit, reading no scene")
    args = parser.parse_args()

    if args.spec:
        return spec(args.balance)

    out = build(load_formula(args.formula), json.loads(args.table.read_text()),
                args.scene, args.balance)
    text = json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(text)
        report(out)
        print(f"  -> {args.out}")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
