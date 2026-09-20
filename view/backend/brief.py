"""Turn an operator's brief into a real fragrance, composed on this bench.

The chat takes a brief — "something fresh and citrusy for summer, light" — and
a model turns it into a formula. What the model is asked for is deliberately
small: the creative part only, a name and a list of (compound, percent). It is
never asked for the formula JSON.

That is the whole point. ``harness/build_formulas.build_formula`` already
expands a spec that size into the harness's own format and refuses anything
wrong with it: percentages that do not sum to 100, a compound outside the
catalogue, an ingredient over its IFRA Category 4 limit. Asking a model for the
fifteen fields it would otherwise have to get right is asking it to be wrong;
asking it for the two that need taste, and letting the builder own the rest,
means a formula that reaches the queue is correct by construction.

**The palette is the bench, not the catalogue.** The model only sees compounds
the scan has named and how much is left in each, so what it writes can be made.
A brief is therefore composed when its turn comes, never when it is sent: while
the scan is still reading the bench the palette is a fraction of it, and a
formula written against that would be a formula written against ignorance.

**A rejected build is a conversation, not a failure.** The builder's complaint
goes back to the model, which tries again, up to ``ATTEMPTS`` times.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "harness") not in sys.path:
    sys.path.insert(0, str(REPO / "harness"))

import build_formulas as bf  # noqa: E402

MODEL = os.environ.get("VIEW_BRIEF_MODEL", "claude-sonnet-5")
ATTEMPTS = 3
MAX_TOKENS = 2000
# A brief the bench cannot stretch to. Fewer than this many compounds and there
# is no fragrance to write, only a mixture.
MIN_PALETTE = 4

PROMPT = """You are a perfumer composing on a specific laboratory bench.

Write one concentrate from the brief below, using ONLY the compounds on the \
palette. The bench holds nothing else, so a compound you name that is not on \
the palette cannot be fetched and the formula is thrown away.

Rules, all of them hard:
- Percentages are by weight of the concentrate and MUST sum to exactly 100.
- Use only palette compounds, spelled exactly as the palette spells them.
- No compound may exceed the grams left in its flask (the palette says how \
many; the batch is {batch} g, so a compound at P percent uses P/100 x {batch} g).
- Respect the IFRA Category 4 maximum shown for a compound that has one. It is \
a percent of the FINISHED product, and the concentrate is diluted to \
{dilution} for the product you choose, so a compound's concentrate percent \
times that dilution must stay under its limit.
- Build a real fragrance: top notes that open it, a heart that carries it, a \
base that holds it. The palette marks each compound's note.
- Between 6 and 18 compounds.

Answer with JSON and nothing else:

{{"name": "...", "family": "...", "product": "Eau de Cologne | Eau de Toilette \
| Eau de Parfum", "description": "one sentence", "ingredients": [["Compound", \
25.4], ["Compound", 16.0]]}}

PALETTE (compound | note | family | odour | grams left | IFRA cat 4 max %):
{palette}

BRIEF:
{brief}"""


def palette(shelf: list[dict], catalogue: dict[str, dict]) -> list[dict]:
    """The compounds this bench can actually supply, with what is left of each.

    Several flasks may hold the same compound; the one with the most in it is
    what a dose would come out of, so that is the number the model is given.

    Args:
        shelf: From ``catalogue.shelf_from_tracks`` — the flasks the scan named.
        catalogue: From ``build_formulas.load_catalogue``.
    """
    best: dict[str, float] = {}
    for flask in shelf:
        name = flask["compound"]
        best[name] = max(best.get(name, 0.0), flask.get("remainingG") or 0.0)
    out = []
    for name, grams in sorted(best.items()):
        entry = catalogue.get(name)
        if entry is None:
            continue
        family, note, odour = bf.PROFILES[entry["cas"]]
        out.append({"compound": name, "note": note, "family": family, "odour": odour,
                    "grams_left": round(grams, 2), "ifra_max_pct": bf.IFRA_CAT4.get(entry["cas"])})
    return out


def _lines(entries: list[dict]) -> str:
    return "\n".join(
        f"{e['compound']} | {e['note']} | {e['family']} | {e['odour']} | "
        f"{e['grams_left']:g} g | {e['ifra_max_pct'] if e['ifra_max_pct'] is not None else '-'}"
        for e in entries)


def _spec(text: str) -> dict:
    """The model's JSON, however it wrapped it."""
    block = re.search(r"\{.*\}", text, re.S)
    if block is None:
        raise ValueError("the model did not answer with JSON")
    spec = json.loads(block.group(0))
    if not isinstance(spec.get("ingredients"), list) or not spec["ingredients"]:
        raise ValueError("no ingredients in the model's answer")
    spec["ingredients"] = [(str(name), float(pct)) for name, pct in spec["ingredients"]]
    return spec


def _on_this_bench(spec: dict, entries: list[dict]) -> None:
    """Refuse a formula this bench cannot pour.

    The builder knows the catalogue of forty compounds and the IFRA limits; it
    has no idea which of them are standing here or how much is left in them.
    Both are facts about this bench, and both are the reason the palette exists:
    a compound that is in the catalogue but not on the bench would otherwise
    sail through, which is exactly what the palette was meant to prevent.
    """
    left = {e["compound"]: e["grams_left"] for e in entries}
    for name, pct in spec["ingredients"]:
        if name not in left:
            raise ValueError(f"{name} is not on this bench; use only the palette")
        grams = pct / 100 * bf.BATCH_G
        if grams > left[name] + 1e-9:
            raise ValueError(f"{name} at {pct} % needs {grams:.3f} g and only "
                             f"{left[name]:.3f} g is left in its flask")


def compose(brief: str, shelf: list[dict], client, formula_id: str = "BRIEF") -> dict:
    """A fragrance written from the brief, on the compounds this bench holds.

    Args:
        brief: What the operator asked for, in their own words.
        shelf: From ``catalogue.shelf_from_tracks``.
        client: An ``anthropic.Anthropic``.
        formula_id: The id the formula carries.

    Returns:
        The formula in the ``harness/formulas`` format, as ``build_formula``
        writes it.

    Raises:
        ValueError: The bench is too bare to compose on, or the model could not
            write something the builder would accept.
    """
    catalogue = bf.load_catalogue()
    entries = palette(shelf, catalogue)
    if len(entries) < MIN_PALETTE:
        raise ValueError(f"only {len(entries)} compounds on the bench: "
                         f"too few to compose a fragrance from")
    prompt = PROMPT.format(brief=brief.strip(), palette=_lines(entries), batch=bf.BATCH_G,
                           dilution=" or ".join(f"{v:.0%} ({k})" for k, v in bf.STRENGTH.items()))
    messages = [{"role": "user", "content": prompt}]
    problems = []
    for _ in range(ATTEMPTS):
        answer = client.messages.create(model=MODEL, max_tokens=MAX_TOKENS, messages=messages)
        text = "".join(b.text for b in answer.content if getattr(b, "type", "") == "text")
        try:
            spec = _spec(text)
            _on_this_bench(spec, entries)
            spec |= {"id": formula_id, "product": spec.get("product") or "Eau de Toilette"}
            spec.setdefault("family", "")
            spec.setdefault("description", "")
            # build_formula is a script's function and exits on a bad formula.
            try:
                return bf.build_formula(spec, catalogue)
            except SystemExit as exc:
                raise ValueError(str(exc)) from exc
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            problems.append(str(exc))
            messages += [{"role": "assistant", "content": text},
                         {"role": "user", "content":
                          f"That was rejected: {exc}. Fix it and answer with the JSON only."}]
    raise ValueError("; ".join(problems[-2:]) or "the model could not write a usable formula")
