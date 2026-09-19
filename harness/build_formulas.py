"""Build harness/formulas/: the olfactory profile of every liquid in the sample
catalogue, and five invented but plausible perfume formulas made only from them.

Every ingredient is matched by CAS to computer-vision/barcodes/lookup_table.json,
so a formula can only use compounds that stand on the bench, and each row lists
the sample ids (one per flask size) that hold it.

A formula is a concentrate (percent by weight, summing to 100) diluted in
ethanol to its product strength. Each ingredient is checked against the IFRA
Standards, 51st Amendment, Category 4 (fine fragrance) limit in the finished
product: concentrate % x dilution must stay at or under it. The build fails if
any formula breaks a limit, uses a compound outside the catalogue or does not
sum to 100 %.

The catalogue has no musks, woods, ambers or vanilla, so the bases rest on
Benzyl benzoate, Nerolidol, Farnesol, beta-Ionone and Hedione. The formulas are
invented for the demo, not tested on skin.

    python harness/build_formulas.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CATALOGUE = REPO / "computer-vision" / "barcodes" / "lookup_table.json"
OUT = Path(__file__).resolve().parent / "formulas"

IFRA_SOURCE = "IFRA Standards, 51st Amendment (2023), Category 4, max % in finished product"

# IFRA Category 4 limits in the finished product, percent. Compounds absent here
# have no quantitative restriction; Linalool, Limonene and the pinenes carry a
# specification standard instead (peroxide value < 20 mmol/L), and allyl esters
# one on free allyl alcohol (< 0.1 % in the ester).
IFRA_CAT4 = {
    "104-55-2": 0.25,   # Cinnamaldehyde (cinnamic aldehyde)
    "100-52-7": 0.25,   # Benzaldehyde
    "5392-40-5": 0.60,  # Citral
    "106-23-0": 0.49,   # Citronellal
    "99-49-0": 0.59,    # Carvone
    "97-53-0": 2.5,     # Eugenol
    "4602-84-0": 1.2,   # Farnesol
    "106-24-1": 4.7,    # Geraniol
    "107-75-5": 2.1,    # Hydroxycitronellal
    "106-22-9": 12.0,   # Citronellol
    "120-51-4": 4.8,    # Benzyl benzoate
    "23726-92-3": 0.043,  # beta-Damascone (rose ketones, combined)
}
IFRA_SPEC = {
    "78-70-6": "specification: peroxide value < 20 mmol/L",
    "5989-27-5": "specification: peroxide value < 20 mmol/L",
    "80-56-8": "specification: peroxide value < 20 mmol/L",
    "127-91-3": "specification: peroxide value < 20 mmol/L",
    "123-68-2": "specification: free allyl alcohol < 0.1 % in the ester",
}

# CAS -> (family, note, odour). Note is where it sits in the evaporation curve.
PROFILES = {
    "5989-27-5": ("citrus", "top", "sweet orange peel, bright, short-lived"),
    "78-70-6": ("floral", "top-heart", "fresh floral-woody, lavender, bergamot"),
    "106-24-1": ("rose", "heart", "sweet rose, geranium, slightly citrus"),
    "5392-40-5": ("citrus", "top", "sharp lemon, lemongrass"),
    "97-53-0": ("spicy", "heart-base", "clove, warm, carnation"),
    "100-52-7": ("fruity", "top", "bitter almond, cherry, marzipan"),
    "106-22-9": ("rose", "heart", "rose, waxy, geranium leaf"),
    "106-25-2": ("rose", "heart", "fresh sweet rose, neroli, lemony"),
    "104-46-1": ("spicy", "heart", "anise, liquorice, sweet"),
    "104-55-2": ("spicy", "heart", "cinnamon bark, warm, hot"),
    "99-49-0": ("aromatic", "top", "spearmint / caraway, herbal"),
    "80-56-8": ("coniferous", "top", "pine, resinous, turpentine"),
    "98-55-5": ("floral", "heart", "lilac, pine, sweet floral"),
    "4602-84-0": ("floral", "base", "linden blossom, muguet, green, soft; fixative"),
    "7212-44-4": ("woody", "base", "fresh bark, green apple, floral-woody; fixative"),
    "140-11-4": ("white floral", "heart", "jasmine, pear, banana, ethereal"),
    "60-12-8": ("rose", "heart", "rose petal, honey, soft"),
    "119-36-8": ("aromatic", "heart", "wintergreen, medicinal; ylang-tuberose facet in traces"),
    "115-95-7": ("citrus", "top", "bergamot, lavender, pear"),
    "928-96-1": ("green", "top", "freshly cut grass, green leaf"),
    "18479-58-8": ("citrus", "top-heart", "lime, metallic fresh, lavender; clean"),
    "24851-98-7": ("white floral", "heart", "transparent jasmine, citrusy, diffusive; volume"),
    "105-54-4": ("fruity", "top", "pineapple, tutti-frutti, ethereal"),
    "123-92-2": ("fruity", "top", "banana, pear drop"),
    "120-51-4": ("balsamic", "base", "faint balsamic, almost odourless; fixative, solvent"),
    "586-62-9": ("citrus", "top", "fresh pine-lime, woody-sweet"),
    "127-91-3": ("coniferous", "top", "dry pine, woody, slightly spicy"),
    "99-85-4": ("citrus", "top", "herbal lime, oily citrus peel"),
    "123-35-3": ("herbal", "top", "herbaceous, balsamic, hops, mango"),
    "106-23-0": ("citrus", "top", "citronella, lemony-green, powerful"),
    "107-75-5": ("floral", "heart", "lily of the valley (muguet), soft, sweet"),
    "105-87-3": ("rose", "heart", "fruity rose, lavender, pear"),
    "150-84-5": ("rose", "heart", "fresh rose, fruity, citrus"),
    "123-68-2": ("fruity", "top", "ripe pineapple, strong"),
    "125-12-2": ("coniferous", "top-heart", "fir needle, camphoraceous, balsamic"),
    "14901-07-6": ("powdery", "heart-base", "violet, orris, woody, raspberry"),
    "23726-92-3": ("rose", "heart", "rose, plum, blackcurrant, tobacco; very powerful"),
    "101-48-4": ("green", "top-heart", "hyacinth, green stem, earthy, honeyed"),
    "141-97-9": ("fruity", "top", "fruity-ethereal, green apple, rum"),
    "78-69-3": ("floral", "top-heart", "clean floral, lavender-bergamot, stable"),
}

STRENGTH = {"Eau de Cologne": 0.05, "Eau de Toilette": 0.12, "Eau de Parfum": 0.18}

# Concentrate, percent by weight: (compound, %). Sums to 100.
FORMULAS = [
    {
        "id": "FRG-101",
        "name": "Orange Blossom Water",
        "family": "citrus aromatic (cologne)",
        "product": "Eau de Cologne",
        "description": "Orange and bergamot over a neroli-lavender heart, with a pine-needle edge; fresh, short-lived.",
        "ingredients": [
            ("Limonene", 25.4),
            ("Linalyl acetate", 16.0),
            ("Linalool", 12.0),
            ("Dihydromyrcenol", 10.0),
            ("Hedione", 8.0),
            ("Benzyl benzoate", 5.0),
            ("gamma-Terpinene", 4.0),
            ("Tetrahydrolinalool", 4.0),
            ("Nerol", 3.0),
            ("Terpinolene", 2.0),
            ("Citral", 2.0),
            ("Geranyl acetate", 2.0),
            ("alpha-Terpineol", 2.0),
            ("Isobornyl acetate", 2.0),
            ("alpha-Pinene", 1.5),
            ("Myrcene", 0.5),
            ("Carvone", 0.3),
            ("Citronellal", 0.3),
        ],
    },
    {
        "id": "FRG-102",
        "name": "Modern Damask Rose",
        "family": "floral rose",
        "product": "Eau de Parfum",
        "description": "A full rose: petal and honey, geranium leaf, a plum-blackcurrant glow from beta-Damascone, a clove and violet trail.",
        "ingredients": [
            ("Phenylethyl alcohol", 28.0),
            ("Citronellol", 18.0),
            ("Geraniol", 12.0),
            ("Benzyl benzoate", 8.35),
            ("Hedione", 8.0),
            ("Nerol", 5.0),
            ("Geranyl acetate", 5.0),
            ("Linalool", 5.0),
            ("Citronellyl acetate", 4.0),
            ("beta-Ionone", 3.0),
            ("Eugenol", 1.5),
            ("Farnesol", 1.5),
            ("cis-3-Hexen-1-ol", 0.5),
            ("beta-Damascone", 0.15),
        ],
    },
    {
        "id": "FRG-103",
        "name": "Lily of the Valley Garden",
        "family": "green floral (lily of the valley)",
        "product": "Eau de Toilette",
        "description": "Lily of the valley in the dew: muguet and linden, transparent jasmine, cut stems and a hyacinth accent.",
        "ingredients": [
            ("Hedione", 20.0),
            ("Hydroxycitronellal", 15.0),
            ("Linalool", 10.0),
            ("Phenylethyl alcohol", 10.0),
            ("Citronellol", 8.0),
            ("Benzyl acetate", 6.0),
            ("Benzyl benzoate", 6.5),
            ("Tetrahydrolinalool", 5.0),
            ("alpha-Terpineol", 4.0),
            ("Dihydromyrcenol", 4.0),
            ("Nerolidol", 4.0),
            ("Farnesol", 3.0),
            ("Geraniol", 2.0),
            ("cis-3-Hexen-1-ol", 1.5),
            ("Phenylacetaldehyde dimethyl acetal", 1.0),
        ],
    },
    {
        "id": "FRG-104",
        "name": "Night Spice",
        "family": "spicy floral (oriental)",
        "product": "Eau de Parfum",
        "description": "Clove, cinnamon and anise on a rose-violet heart, dried down on a warm balsamic, woody-floral base.",
        "ingredients": [
            ("Benzyl benzoate", 22.0),
            ("Limonene", 10.0),
            ("Linalool", 10.0),
            ("Nerolidol", 10.0),
            ("Phenylethyl alcohol", 8.0),
            ("Hedione", 8.0),
            ("Eugenol", 6.0),
            ("beta-Ionone", 6.0),
            ("Citronellol", 5.0),
            ("Geraniol", 4.0),
            ("Linalyl acetate", 4.0),
            ("Farnesol", 3.0),
            ("Anethole", 1.5),
            ("beta-Pinene", 1.0),
            ("Cinnamaldehyde", 0.8),
            ("Methyl salicylate", 0.5),
            ("Benzaldehyde", 0.2),
        ],
    },
    {
        "id": "FRG-105",
        "name": "Green Fruit",
        "family": "fruity green floral",
        "product": "Eau de Toilette",
        "description": "Pineapple, pear and green apple over a juicy jasmine-rose heart, with cut grass and a soft violet drydown.",
        "ingredients": [
            ("Limonene", 18.0),
            ("Hedione", 15.0),
            ("Benzyl acetate", 10.0),
            ("Linalool", 10.0),
            ("Benzyl benzoate", 10.0),
            ("Dihydromyrcenol", 6.0),
            ("Nerolidol", 6.0),
            ("Geranyl acetate", 5.0),
            ("Citronellyl acetate", 4.0),
            ("beta-Ionone", 4.0),
            ("Phenylethyl alcohol", 3.0),
            ("cis-3-Hexen-1-ol", 2.0),
            ("Allyl hexanoate", 1.5),
            ("Citral", 1.5),
            ("Ethyl acetoacetate", 1.2),
            ("Ethyl butyrate", 1.0),
            ("Farnesol", 1.0),
            ("Isoamyl acetate", 0.8),
        ],
    },
]

BATCH_G = 10.0  # grams of concentrate per batch, as the dashboard's recipe


def load_catalogue() -> dict[str, dict]:
    rows = json.loads(CATALOGUE.read_text())["entries"].values()
    by_name: dict[str, dict] = {}
    for r in rows:
        if r["phase"] != "liquid":
            continue
        c = by_name.setdefault(r["material"], {"cas": r["cas"], "samples": []})
        c["samples"].append({"sample_id": r["sample_id"], "container_ml": r["container_ml"]})
    return by_name


def build_formula(f: dict, catalogue: dict[str, dict]) -> dict:
    dilution = STRENGTH[f["product"]]
    total = round(sum(p for _, p in f["ingredients"]), 6)
    if abs(total - 100.0) > 1e-6:
        raise SystemExit(f"{f['id']}: concentrate sums to {total} %, not 100 %")
    rows = []
    for name, pct in f["ingredients"]:
        if name not in catalogue:
            raise SystemExit(f"{f['id']}: {name} is not a liquid in the catalogue")
        cas = catalogue[name]["cas"]
        family, note, odour = PROFILES[cas]
        final = pct * dilution
        limit = IFRA_CAT4.get(cas)
        if limit is not None and final > limit + 1e-9:
            raise SystemExit(f"{f['id']}: {name} at {final:.4f} % breaks the IFRA limit {limit} %")
        rows.append({
            "material": name,
            "cas": cas,
            "note": note,
            "role": family,
            "concentrate_pct": pct,
            "batch_g": round(pct / 100 * BATCH_G, 4),
            "finished_pct": round(final, 4),
            "ifra_cat4_max_pct": limit,
            "ifra_note": IFRA_SPEC.get(cas),
            "samples": [s["sample_id"] for s in catalogue[name]["samples"]],
        })
    return {
        "id": f["id"],
        "name": f["name"],
        "family": f["family"],
        "description": f["description"],
        "product": f["product"],
        "concentrate_pct_in_product": round(dilution * 100, 1),
        "solvent": {"material": "Ethanol 96 % (perfumer's alcohol)", "pct_in_product": round((1 - dilution) * 100, 1)},
        "batch": {"concentrate_g": BATCH_G, "ethanol_g_for_product": round(BATCH_G * (1 - dilution) / dilution, 2)},
        "ifra": IFRA_SOURCE,
        "catalogue": str(CATALOGUE.relative_to(REPO)),
        "ingredients": rows,
    }


def main() -> None:
    catalogue = load_catalogue()
    missing = {c["cas"] for c in catalogue.values()} - PROFILES.keys()
    if missing:
        raise SystemExit(f"no olfactory profile for CAS {sorted(missing)}")
    OUT.mkdir(exist_ok=True)

    profiles = []
    for name, c in catalogue.items():
        family, note, odour = PROFILES[c["cas"]]
        profiles.append({
            "material": name, "cas": c["cas"], "family": family, "note": note, "odour": odour,
            "ifra_cat4_max_pct": IFRA_CAT4.get(c["cas"]), "ifra_note": IFRA_SPEC.get(c["cas"]),
        })
    (OUT / "olfactory_profiles.json").write_text(json.dumps(
        {"ifra": IFRA_SOURCE, "count": len(profiles), "compounds": profiles}, indent=1, ensure_ascii=False) + "\n")

    for f in FORMULAS:
        out = build_formula(f, catalogue)
        (OUT / f"{f['id']}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
        print(f"{f['id']} {f['name']}: {len(out['ingredients'])} ingredients, {out['product']}")
    print(f"{len(profiles)} profiles, {len(FORMULAS)} formulas -> {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
