"""The formula chat: a typed request becomes a formula the arm can run.

With ANTHROPIC_API_KEY set and the ``anthropic`` package installed, Claude reads
free-form requests ("something fresh and citrusy, 3 g") and proposes a formula
from the flasks on the bench. Without it, a small parser handles the direct
forms, so the demo never depends on the network:

    FRG-101                           a catalogue formula (harness/formulas), 3 g
    5 g of FRG-102                    the same, scaled to a batch
    1.2 g linalool, 0.8 g hedione     explicit lines; Spanish names work too
    40 % limonene, 60 % linalool, total 2 g
    run / stop / what's on the bench?

Either way the proposal goes through formulation.resolve, so nothing is ever
proposed that the arm could not draw from this bench.
"""
from __future__ import annotations

import os
import re
from typing import Callable

from formulation import MAX_BATCH_G, MIN_DOSE_G, Catalogue, normalise, resolve

MODEL = os.environ.get("VIEW_CHAT_MODEL", "claude-opus-5")
DEFAULT_BATCH_G = 3.0
DEFAULT_PERCENT_TOTAL_G = 2.0
HISTORY = 12

START = re.compile(r"^\s*(run|start|go|execute|yes|ok|okay|confirm|dale|s[ií]|empieza|ejecuta|"
                   r"adelante|venga|hazlo|lanza|arranca)\b", re.I)
STOP = re.compile(r"\b(stop|abort|cancel|halt|para|parar|det[eé]n|detente|cancela|aborta)\b", re.I)
BENCH = re.compile(r"\b(bench|inventory|available|stock|shelf|ingredients|qu[eé] hay|disponibles?|"
                   r"banco|mesa|inventario|ingredientes)\b", re.I)
FRG = re.compile(r"\bFRG[- ]?(\d{3})\b", re.I)
QTY = re.compile(r"(\d+(?:\.\d+)?)\s*(mg|g|gr|grams?|gramos?|%|percent|por ?ciento)(?![a-z])", re.I)
TOTAL = re.compile(r"(?:total|batch|lote)\s*(?:of|de|:)?\s*(\d+(?:\.\d+)?)\s*(?:g|gr|grams?|gramos?)\b"
                   r"|(\d+(?:\.\d+)?)\s*(?:g|gr|grams?|gramos?)\s*(?:in total|en total|total|batch|de lote)", re.I)
BATCH = re.compile(r"(\d+(?:\.\d+)?)\s*(?:g|gr|grams?|gramos?)\b", re.I)
SPLIT = re.compile(r"[,;\n+&]|\band\b|\by\b|\bwith\b|\bcon\b", re.I)

HELP = ("Tell me a formula and the arm will pipette it into the beaker on the balance. For example "
        "\"FRG-101\", \"5 g of FRG-103\", \"1.2 g linalool, 0.8 g hedione\" or "
        "\"40 % limonene, 60 % linalool, total 2 g\". Ask \"what's on the bench?\" to see what can be used.")


def _grams(value: str, unit: str) -> float:
    return float(value) / 1000 if unit.lower() == "mg" else float(value)


def _clock(seconds: float) -> str:
    seconds = int(round(seconds))
    return f"{seconds // 60} min {seconds % 60:02d} s" if seconds >= 60 else f"{seconds} s"


def describe(formula: dict) -> str:
    """One or two sentences for a proposal; the chat shows the table itself."""
    ings = formula["ingredients"]
    ok = [i for i in ings if not i["problem"]]
    head = f"{formula['id']} · {formula['name']}: " if formula["id"] != "CHAT" else ""
    if not ok:
        return head + "none of these can be dosed on this bench." + (
            f" I don't know {', '.join(formula['unknown'])}." if formula["unknown"] else "")
    if len(ok) == len(ings):
        text = head + (f"{ok[0]['compound']} is on this bench" if len(ok) == 1
                       else f"all {len(ok)} ingredients are on this bench")
    else:
        text = head + f"{len(ok)} of {len(ings)} ingredients can be dosed here"
    trips = formula["estimate"]["trips"]
    text += (f", {formula['targetMass']:.3f} g in about {trips} draw{'s' if trips != 1 else ''} "
             f"(~{_clock(formula['estimate']['seconds'])}). Press Run or type \"run\".")
    if formula["unknown"]:
        text += f" I don't know {', '.join(formula['unknown'])}."
    return text


def describe_bench(shelf: list[dict]) -> str:
    if not shelf:
        return "There are no open flasks on this bench."
    best: dict[str, dict] = {}
    for flask in shelf:
        if flask["usableG"] > best.get(flask["compound"], {}).get("usableG", -1):
            best[flask["compound"]] = flask
    items = ", ".join(f"{name} {f['usableG']:.1f} g" for name, f in sorted(best.items()))
    return f"{len(shelf)} open flasks, {len(best)} compounds (grams that can be drawn): {items}."


class FormulaChat:
    """Turns chat messages into formulas and run commands.

    Args:
        catalogue: The sample catalogue.
        shelf: Returns the bench as formulation.bench reads it, now.
    """

    def __init__(self, catalogue: Catalogue, shelf: Callable[[], list[dict]]) -> None:
        self.catalogue = catalogue
        self.shelf = shelf
        self.last: dict | None = None
        self._client = None
        if os.environ.get("ANTHROPIC_API_KEY"):
            try:
                import anthropic

                self._client = anthropic.Anthropic()
            except ImportError:
                self._client = None

    @property
    def mode(self) -> str:
        return "claude" if self._client else "offline"

    def reply(self, message: str, history: list[dict] | None = None) -> dict:
        """Answer one message.

        Returns:
            ``{"reply": str, "formula": dict | None, "action": "start" | "stop" | None}``.
        """
        if self._client is not None:
            try:
                return self._claude(message, history or [])
            except Exception as exc:  # noqa: BLE001 -- network, quota, key: fall back
                answer = self._offline(message)
                answer["reply"] += f" (Claude unavailable: {type(exc).__name__}; used the offline parser.)"
                return answer
        return self._offline(message)

    # --- offline ----------------------------------------------------------

    def _offline(self, message: str) -> dict:
        text = re.sub(r"(\d),(\d)", r"\1.\2", message.strip())
        words = len(text.split())
        if STOP.search(text) and words <= 4 and not QTY.search(text):
            return {"reply": "Stopping the run.", "formula": None, "action": "stop"}
        if START.search(text) and words <= 4 and not QTY.search(text) and not FRG.search(text):
            return {"reply": "Starting.", "formula": self.last, "action": "start"}

        formula = self._catalogue_formula(text) or self._lines_formula(text)
        if formula is not None:
            self.last = formula
            return {"reply": describe(formula), "formula": formula, "action": None}
        if BENCH.search(text):
            return {"reply": describe_bench(self.shelf()), "formula": None, "action": None}
        return {"reply": HELP, "formula": None, "action": None}

    def _catalogue_formula(self, text: str) -> dict | None:
        match = FRG.search(text)
        ref = f"FRG-{match.group(1)}" if match else None
        if ref is None:
            words = f" {normalise(text)} "
            ref = next((fid for fid, f in self.catalogue.formulas.items()
                        if f" {normalise(f['name'])} " in words), None)
        if ref is None:
            return None
        source = self.catalogue.formulas.get(ref)
        if source is None:
            known = ", ".join(self.catalogue.formulas)
            return {"id": ref, "name": "unknown formula", "ingredients": [], "unknown": [f"{ref} (try {known})"],
                    "targetMass": 0.0, "runnable": False, "estimate": {"trips": 0, "seconds": 0}}
        rest = FRG.sub(" ", text)
        batch = BATCH.search(rest)
        grams = min(float(batch.group(1)), MAX_BATCH_G) if batch else DEFAULT_BATCH_G
        lines = [{"compound": i["cas"], "grams": round(i["concentrate_pct"] / 100 * grams, 3)}
                 for i in source["ingredients"]]
        return resolve(lines, self.shelf(), self.catalogue, source["id"], f"{source['name']} · {grams:g} g")

    def _lines_formula(self, text: str) -> dict | None:
        total = TOTAL.search(text)
        total_g = float(total.group(1) or total.group(2)) if total else None
        body = TOTAL.sub(" ", text)
        found = list(QTY.finditer(body))
        if not found:
            return None
        # "1.2 g linalool" or "linalool 1.2 g": whichever way round the first
        # line is written, pair each quantity with the text on that side.
        if self.catalogue.find_all(body[:found[0].start()]):
            bounds = [(found[i - 1].end() if i else 0, m.start()) for i, m in enumerate(found)]
        else:
            bounds = [(m.end(), found[i + 1].start() if i + 1 < len(found) else len(body))
                      for i, m in enumerate(found)]
        lines, percent, unknown = [], False, []
        for qty, (a, b) in zip(found, bounds):
            name = " ".join(SPLIT.sub(" ", body[a:b]).split())
            name = re.sub(r"\b(of|de|del|la|el|the|para|for)\b", " ", name, flags=re.I).strip(" .:")
            cas = self.catalogue.find(name) if name else None
            if cas is None:
                if name:
                    unknown.append(name)
                continue
            unit = qty.group(2).lower()
            is_pct = unit in ("%", "percent", "por ciento", "porciento")
            percent |= is_pct
            lines.append({"compound": cas, "value": float(qty.group(1)), "pct": is_pct,
                          "grams": None if is_pct else _grams(qty.group(1), unit)})
        if not lines:
            return None
        name = "Chat formula"
        if percent:
            total_g = total_g or DEFAULT_PERCENT_TOTAL_G
            shares = sum(line["value"] for line in lines if line["pct"]) or 100.0
            for line in lines:
                if line["pct"]:
                    line["grams"] = round(line["value"] / shares * total_g, 3)
            name = f"Chat formula · {total_g:g} g"
        formula = resolve([{"compound": line["compound"], "grams": line["grams"]} for line in lines],
                          self.shelf(), self.catalogue, "CHAT", name)
        formula["unknown"] += unknown
        return formula

    # --- Claude -----------------------------------------------------------

    TOOLS = [
        {
            "name": "propose_formula",
            "description": "Propose a formula for the arm to pipette into the beaker. The operator "
                           "sees it as a table and presses Run. Use only compounds on the bench.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Short name, e.g. 'Citrus cologne accord'."},
                    "ingredients": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "compound": {"type": "string", "description": "Name exactly as in the bench list."},
                                "grams": {"type": "number"},
                            },
                            "required": ["compound", "grams"],
                        },
                    },
                },
                "required": ["name", "ingredients"],
            },
        },
        {"name": "start_run", "description": "Start the proposed formula, when the operator says so.",
         "input_schema": {"type": "object", "properties": {}}},
        {"name": "stop_run", "description": "Stop the formulation that is running.",
         "input_schema": {"type": "object", "properties": {}}},
    ]

    def _system(self) -> str:
        shelf = describe_bench(self.shelf())
        formulas = "\n".join(
            f"- {fid} {f['name']} ({f['family']}): "
            + ", ".join(f"{i['material']} {i['concentrate_pct']:g}%" for i in f["ingredients"][:8])
            for fid, f in self.catalogue.formulas.items())
        return (
            "You are the formulation assistant of a robotic perfumery lab. A UR10e arm on a rail "
            "pipettes liquids from open flasks on the bench into a beaker on a balance, one draw of up "
            "to 1 ml (0.91 g) at a time, about 12 s per draw, dosing each ingredient in closed loop "
            "against the balance.\n\n"
            f"On the bench now: {shelf}\n\n"
            f"Catalogue formulas (percent of the concentrate):\n{formulas}\n\n"
            "Rules:\n"
            "- Only use compounds that are on the bench, spelt as listed. Never invent one.\n"
            f"- Each ingredient at least {MIN_DOSE_G:g} g; the whole batch at most {MAX_BATCH_G:g} g. "
            f"Default to about {DEFAULT_BATCH_G:g} g and at most six ingredients unless asked, so the "
            "run stays a few minutes long.\n"
            "- For a catalogue formula, keep its proportions over the ingredients that are on the bench "
            "and say which are missing.\n"
            "- Call propose_formula whenever you suggest or change a formula; the table is shown to the "
            "operator, so do not repeat it in prose. Call start_run only when the operator asks to run "
            "it, stop_run when they ask to stop.\n"
            "- Answer in the operator's language, in one to three short sentences."
        )

    def _messages(self, history: list[dict], message: str) -> list[dict]:
        out: list[dict] = []
        for item in history[-HISTORY:]:
            role = "assistant" if item.get("role") == "assistant" else "user"
            text = str(item.get("text") or "").strip()
            if item.get("formula"):
                f = item["formula"]
                text += "\n(Proposed: " + ", ".join(
                    f"{i['compound']} {i['grams']:g} g" for i in f.get("ingredients", [])) + ")"
            if not text:
                continue
            if out and out[-1]["role"] == role:
                out[-1]["content"] += "\n" + text
            else:
                out.append({"role": role, "content": text})
        while out and out[0]["role"] == "assistant":
            out.pop(0)
        if out and out[-1]["role"] == "user":
            out[-1]["content"] += "\n" + message
        else:
            out.append({"role": "user", "content": message})
        return out

    def _claude(self, message: str, history: list[dict]) -> dict:
        response = self._client.messages.create(
            model=MODEL, max_tokens=1024, system=self._system(), tools=self.TOOLS,
            messages=self._messages(history, message))
        text = " ".join(b.text for b in response.content if b.type == "text").strip()
        formula, action = None, None
        for block in response.content:
            if block.type != "tool_use":
                continue
            if block.name == "propose_formula":
                lines = list(block.input.get("ingredients") or [])
                formula = resolve(lines, self.shelf(), self.catalogue, "CHAT",
                                  str(block.input.get("name") or "Chat formula"))
                self.last = formula
            elif block.name == "start_run":
                action, formula = "start", formula or self.last
            elif block.name == "stop_run":
                action = "stop"
        if not text:
            text = describe(formula) if formula else ("Starting." if action == "start" else
                                                      "Stopping the run." if action == "stop" else HELP)
        return {"reply": text, "formula": formula, "action": action}
