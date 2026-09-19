"""The sample catalogue and the invented formulas, for the formula chat.

A formula is checked against the flasks the live scan has named by their rings
(live_scan.py): an ingredient is available when the scan found a flask of it on
the bench, and it names that flask. Nothing here reads the simulator's state.
"""
from __future__ import annotations

import json
import re
from difflib import get_close_matches
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LOOKUP = REPO / "computer-vision" / "barcodes" / "lookup_table.json"
FORMULAS = REPO / "harness" / "formulas"

MIN_DOSE_G = 0.02
MAX_BATCH_G = 10.0
PICK_S = 35.0                   # rough seconds for the arm to fetch one flask, for estimates


def normalise(text: str) -> str:
    """Lower case, Greek letters spelt out, anything else a single space."""
    text = text.lower()
    for greek, word in (("α", "alpha"), ("β", "beta"), ("γ", "gamma")):
        text = text.replace(greek, word)
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


# Spanish and short names for the catalogue's liquids, so the chat understands
# them without a language model. Keys are normalised.
ALIASES = {
    "limoneno": "Limonene", "linalol": "Linalool", "citronelol": "Citronellol",
    "anetol": "Anethole", "cinamaldehido": "Cinnamaldehyde", "cinnamic aldehyde": "Cinnamaldehyde",
    "benzaldehido": "Benzaldehyde", "carvona": "Carvone", "alfa pineno": "alpha-Pinene",
    "a pinene": "alpha-Pinene", "alpha pineno": "alpha-Pinene", "beta pineno": "beta-Pinene",
    "b pinene": "beta-Pinene", "alfa terpineol": "alpha-Terpineol", "terpineol": "alpha-Terpineol",
    "acetato de bencilo": "Benzyl acetate", "alcohol feniletilico": "Phenylethyl alcohol",
    "phenethyl alcohol": "Phenylethyl alcohol", "salicilato de metilo": "Methyl salicylate",
    "acetato de linalilo": "Linalyl acetate", "leaf alcohol": "cis-3-Hexen-1-ol",
    "hexenol": "cis-3-Hexen-1-ol", "dihidromircenol": "Dihydromyrcenol",
    "butirato de etilo": "Ethyl butyrate", "acetato de isoamilo": "Isoamyl acetate",
    "benzoato de bencilo": "Benzyl benzoate", "terpinoleno": "Terpinolene",
    "gamma terpineno": "gamma-Terpinene", "mirceno": "Myrcene", "citronelal": "Citronellal",
    "hidroxicitronelal": "Hydroxycitronellal", "acetato de geranilo": "Geranyl acetate",
    "acetato de citronelilo": "Citronellyl acetate", "hexanoato de alilo": "Allyl hexanoate",
    "acetato de isobornilo": "Isobornyl acetate", "beta ionona": "beta-Ionone",
    "ionone": "beta-Ionone", "beta damascona": "beta-Damascone", "damascone": "beta-Damascone",
    "acetoacetato de etilo": "Ethyl acetoacetate", "tetrahidrolinalol": "Tetrahydrolinalool",
    "hedion": "Hedione", "methyl dihydrojasmonate": "Hedione",
}


class Catalogue:
    """The sample catalogue (liquids only) and the five invented formulas."""

    def __init__(self, lookup: Path = LOOKUP, formulas: Path = FORMULAS) -> None:
        table = json.loads(lookup.read_text())
        self.samples: dict[str, dict] = {}
        self.compounds: dict[str, str] = {}     # CAS -> name
        for code, row in table["entries"].items():
            if row.get("phase") != "liquid":
                continue
            self.samples[row["sample_id"]] = {
                "compound": row["material"], "cas": row["cas"], "barcode": code,
                "containerMl": float(row["container_ml"]),
            }
            self.compounds.setdefault(row["cas"], row["material"])
        by_name = {normalise(name): cas for cas, name in self.compounds.items()}
        by_name.update({alias: next(c for c, n in self.compounds.items() if n == name)
                        for alias, name in ALIASES.items()})
        by_name.update({normalise(cas): cas for cas in self.compounds})
        # Longest first, so "alpha terpineol" wins over "terpineol".
        self.names = dict(sorted(by_name.items(), key=lambda kv: -len(kv[0])))
        self.formulas = {}
        for path in sorted(formulas.glob("FRG-*.json")):
            formula = json.loads(path.read_text())
            self.formulas[formula["id"]] = formula

    def find(self, text: str) -> str | None:
        """CAS of the compound a piece of text names, or None."""
        words = f" {normalise(text)} "
        for name, cas in self.names.items():
            if f" {name} " in words:
                return cas
        close = get_close_matches(words.strip(), list(self.names), n=1, cutoff=0.82)
        return self.names[close[0]] if close else None

    def find_all(self, text: str) -> list[tuple[int, str]]:
        """Every compound named in a text, as (position, CAS), in order."""
        words = f" {normalise(text)} "
        found, taken = [], [False] * len(words)
        for name, cas in self.names.items():
            for match in re.finditer(f"(?<= ){re.escape(name)}(?= )", words):
                span = range(match.start(), match.end())
                if any(taken[i] for i in span):
                    continue
                for i in span:
                    taken[i] = True
                found.append((match.start(), cas))
        return sorted(found)


def shelf_from_tracks(tracks, catalogue: Catalogue) -> list[dict]:
    """The flasks the scan has named, as the chat offers them.

    Args:
        tracks: vision_pick tracks (``World.snapshot()``).
        catalogue: The sample catalogue.
    """
    out = []
    for track in tracks:
        sample = track.sample
        info = catalogue.samples.get(sample) if sample else None
        if info is None or track.state == "lost":
            continue
        x, y = track.xy
        out.append({"sampleId": sample, "compound": info["compound"], "cas": info["cas"],
                    "containerMl": info["containerMl"], "track": track.id,
                    "x": round(float(x), 3), "y": round(float(y), 3)})
    return sorted(out, key=lambda v: (v["compound"], -v["containerMl"]))


def resolve(lines: list[dict], shelf: list[dict], catalogue: Catalogue,
            formula_id: str = "CHAT", name: str = "Chat formula") -> dict:
    """Match a requested formula to the flasks the scan has named.

    Args:
        lines: ``[{"compound": name or CAS, "grams": float}]``.
        shelf: From :func:`shelf_from_tracks`.
        catalogue: The sample catalogue.

    Returns:
        The formula as the chat shows it: every line with the flask the scan
        found for it, or the reason there is none.
    """
    merged: dict[str, float] = {}
    unknown = []
    for line in lines:
        cas = catalogue.find(str(line.get("compound", "")))
        if cas is None:
            unknown.append(str(line.get("compound")))
            continue
        merged[cas] = merged.get(cas, 0.0) + float(line.get("grams") or 0)
    ingredients = []
    for cas, grams in merged.items():
        compound = catalogue.compounds[cas]
        flasks = [v for v in shelf if v["cas"] == cas]
        best = max(flasks, key=lambda v: v["containerMl"], default=None)
        problem = None
        if grams < MIN_DOSE_G:
            problem = f"below {MIN_DOSE_G:g} g"
        elif best is None:
            problem = "not identified on the bench"
        ingredients.append({
            "id": f"ing-{normalise(compound).replace(' ', '-')}", "compound": compound, "cas": cas,
            "grams": round(grams, 3), "sampleId": best["sampleId"] if best else None,
            "problem": problem,
        })
    found = [i for i in ingredients if not i["problem"]]
    total = sum(i["grams"] for i in ingredients if i["problem"] != f"below {MIN_DOSE_G:g} g")
    return {
        "id": formula_id, "name": name, "ingredients": ingredients, "unknown": unknown,
        "targetMass": round(total, 3), "runnable": bool(found),
        "estimate": {"picks": len(found), "seconds": round(PICK_S * len(found))},
    }
