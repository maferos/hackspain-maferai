#!/usr/bin/env python3
"""Build the research Obsidian vault from the bibliographies of the three research docs.

Mnemos-style layout: Content/Papers/<citekey>.pdf, Content/Sources/<citekey> - <title>.md,
Topics/<topic>.md. arXiv PDFs are downloaded only when the arXiv API title matches the cited
title; everything else becomes a citation-only note. Re-runnable: existing PDFs are kept.

    python3 tools/build_vault.py            # from research/
"""
import datetime
import hashlib
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "Content" / "Papers"
SOURCES = ROOT / "Content" / "Sources"
TOPICS = ROOT / "Topics"
DOCS = {
    "01_matematicas_grupos_de_lie.md": "Matemáticas — grupos de Lie y geometría",
    "02_optimizacion_y_algoritmos.md": "Optimización y algoritmos",
    "03_aplicaciones_vision_por_computador.md": "Aplicaciones en visión por computador",
    "04_huecos_y_ampliacion.md": "Ampliación — huecos del corpus",
}
ATOM = "{http://www.w3.org/2005/Atom}"
UA = {"User-Agent": "hackspain-research-vault/0.1 (mailto:eki@mafer.ai)"}
STOP = {"a", "an", "the", "on", "of", "for", "and", "to", "in", "with", "via", "from", "by",
        "is", "are", "as", "at", "its", "towards", "toward", "into", "what", "how", "why", "do"}
TODAY = datetime.date.today().isoformat()


def ascii_fold(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def norm_title(s):
    return re.sub(r"[^a-z0-9]+", " ", ascii_fold(s).lower()).strip()


def similar(a, b):
    return SequenceMatcher(None, norm_title(a), norm_title(b)).ratio()


def split_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def distinct_ids(a, b):
    """Two refs that carry different arXiv ids or DOIs are different works (e.g. Vol. 1 / Vol. 2)."""
    return any(a[f] and b[f] and a[f].lower() != b[f].lower() for f in ("arxiv", "doi"))


def parse_bibliographies():
    refs = {}
    for doc, topic in DOCS.items():
        path = ROOT / doc
        if not path.exists():
            print(f"skip {doc}: not written yet", file=sys.stderr)
            continue
        in_bib = False
        header = None
        for line in path.read_text().splitlines():
            if line.startswith("## "):
                in_bib = "bibliograf" in line.lower()
                header = None
                continue
            if not in_bib or not line.startswith("|"):
                continue
            cells = split_row(line)
            if header is None:
                header = [ascii_fold(c).lower() for c in cells]
                continue
            if set("".join(cells)) <= set("-: "):
                continue
            row = dict(zip(header, cells))
            title = row.get("titulo", "").strip("*_ ")
            if not title:
                continue
            link_cell = row.get("enlace", "")
            m = re.search(r"\((https?://[^)\s]+)\)", link_cell)
            url = m.group(1) if m else ""
            arxiv = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}|[a-z\-]+/[0-9]{7})", link_cell)
            doi = re.search(r"(10\.\d{4,9}/[^\s)\]|]+)", link_cell)
            year = re.search(r"\d{4}", row.get("ano", "") or row.get("año", ""))
            ref = {
                "title": title,
                "authors": row.get("autores", ""),
                "year": int(year.group()) if year else None,
                "url": url,
                "arxiv": arxiv.group(1) if arxiv else None,
                "doi": doi.group(1).rstrip(".") if doi else None,
                "why": {doc: row.get("por que es relevante", "")},
            }
            key = ref["arxiv"] or (ref["doi"] or "").lower() or norm_title(title)
            dup = refs.get(key) or next((r for r in refs.values() if similar(r["title"], title) > 0.93
                                         and not distinct_ids(r, ref)), None)
            if dup:
                dup["why"].update(ref["why"])
                for f in ("arxiv", "doi", "url"):
                    dup[f] = dup[f] or ref[f]
            else:
                refs[key] = ref
    return list(refs.values())


def http_get(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def arxiv_entries(query):
    url = "http://export.arxiv.org/api/query?" + query
    for attempt in range(4):
        try:
            root = ET.fromstring(http_get(url))
            break
        except Exception as e:  # rate limit / transient
            print(f"  arXiv API retry ({e})", file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    else:
        return []
    out = []
    for e in root.findall(f"{ATOM}entry"):
        aid = e.findtext(f"{ATOM}id", "")
        m = re.search(r"abs/(.+?)(v\d+)?$", aid)
        if not m:
            continue
        out.append({
            "id": m.group(1),
            "title": " ".join(e.findtext(f"{ATOM}title", "").split()),
            "summary": " ".join(e.findtext(f"{ATOM}summary", "").split()),
            "authors": [a.findtext(f"{ATOM}name", "") for a in e.findall(f"{ATOM}author")],
            "published": e.findtext(f"{ATOM}published", "")[:10],
        })
    return out


def resolve_arxiv(refs):
    ids = [r["arxiv"] for r in refs if r["arxiv"]]
    meta = {}
    for rnd in range(4):  # the API sometimes answers a batch empty under load; retry what is missing
        missing = [i for i in ids if i not in meta]
        if not missing:
            break
        size = 20 if rnd == 0 else 5
        for i in range(0, len(missing), size):
            chunk = missing[i:i + size]
            for e in arxiv_entries("id_list=" + ",".join(chunk) + f"&max_results={len(chunk)}"):
                meta[e["id"]] = e
            time.sleep(3 + 3 * rnd)
    # References cited without an arXiv link: look for an exact-title preprint.
    for r in refs:
        if r["arxiv"]:
            continue
        q = urllib.parse.quote(f'ti:"{norm_title(r["title"])}"')
        for e in arxiv_entries(f"search_query={q}&max_results=3"):
            if similar(e["title"], r["title"]) > 0.95:
                r["arxiv"] = e["id"]
                r["arxiv_found_by_title"] = True
                meta[e["id"]] = e
                break
        time.sleep(3)
    for r in refs:
        e = meta.get(r["arxiv"]) if r["arxiv"] else None
        # A cited title may be the arXiv title abbreviated after its colon ("EquiBot: SIM(3)-Equivariant ...").
        if e and (similar(e["title"], r["title"]) > 0.85
                  or norm_title(e["title"]).startswith(norm_title(r["title"]))
                  or norm_title(r["title"]).replace("ddp", "differential dynamic programming")
                  == norm_title(e["title"]) or norm_title(e["title"]).startswith(norm_title(r["title"]).replace(" rl", " reinforcement learning"))):
            r["arxiv_meta"] = e
        elif r["arxiv"]:
            r["arxiv_mismatch"] = e["title"] if e else "not returned by arXiv API"
            print(f"  ! arXiv {r['arxiv']} title mismatch for '{r['title']}': {r['arxiv_mismatch']}", file=sys.stderr)


def first_family(authors):
    first = re.split(r",| and | y |;", authors)[0].strip()
    first = re.sub(r"\bet al\.?", "", first).strip()
    parts = [p for p in first.split() if not re.fullmatch(r"[A-Z]\.(-?[A-Z]\.)?|[A-Z]\.?", p)]
    family = parts[-1] if parts else "Anon"
    family = re.sub(r"[^A-Za-z]", "", ascii_fold(family)) or "Anon"
    return family[0].upper() + family[1:]


def make_citekeys(refs):
    taken = {}
    for r in refs:
        authors = ", ".join(r["arxiv_meta"]["authors"]) if r.get("arxiv_meta") else r["authors"]
        words = [w for w in norm_title(r["title"]).split() if w not in STOP and not w.isdigit()]
        kw = (words[0] if words else "work")[:20]
        base = f"{first_family(authors)}{r['year'] or 0}{kw}"
        key, n = base, 2
        while key in taken:
            key = f"{base}{n}"
            n += 1
        taken[key] = r
        r["citekey"] = key


def download_pdfs(refs):
    PAPERS.mkdir(parents=True, exist_ok=True)
    for r in refs:
        if not r.get("arxiv_meta"):
            continue
        dest = PAPERS / f"{r['citekey']}.pdf"
        if not dest.exists():
            try:
                data = http_get(f"https://arxiv.org/pdf/{r['arxiv']}", timeout=120)
            except Exception as e:
                print(f"  ! download failed {r['arxiv']}: {e}", file=sys.stderr)
                continue
            if not data.startswith(b"%PDF"):
                print(f"  ! not a PDF: {r['arxiv']}", file=sys.stderr)
                continue
            dest.write_bytes(data)
            print(f"  + {dest.name} ({len(data) // 1024} KB)")
            time.sleep(3)
        r["pdf"] = f"Content/Papers/{dest.name}"
        r["sha256"] = hashlib.sha256(dest.read_bytes()).hexdigest()


def yaml_str(s):
    return json.dumps(s if s is not None else "", ensure_ascii=False)


def safe_filename(s, n=60):
    s = re.sub(r'[\\/:*?"<>|#^\[\]$]', "", s)
    s = " ".join(s.split())
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0]


def note_name(r):
    return f"{r['citekey']} - {safe_filename(r['title'])}"


def write_source_note(r):
    m = r.get("arxiv_meta")
    authors = m["authors"] if m else [a.strip() for a in re.split(r",(?![^()]*\))| and | y ", r["authors"]) if a.strip()]
    url = r["url"] or (f"https://arxiv.org/abs/{r['arxiv']}" if r["arxiv"] else "")
    doi = r["doi"] or (f"10.48550/arXiv.{r['arxiv']}" if r["arxiv"] and not r["doi"] else "")
    ptype = "preprint" if (r["arxiv"] and not r["doi"]) else ("book" if "book" in url or "978-" in (r["doi"] or "") else "article")
    cited_in = [f"[[{Path(d).stem}]]" for d in r["why"]]
    lines = [
        "---",
        "aliases: []",
        'type: "source"',
        f"title: {yaml_str(r['title'])}",
        f"citekey: {yaml_str(r['citekey'])}",
        f"doi: {yaml_str(doi)}",
        f"arxiv: {yaml_str(r['arxiv'] if m else '')}",
        f"year: {r['year'] or ''}",
        f"publication_type: {yaml_str(ptype)}",
        f"url: {yaml_str(url)}",
        "keywords: []",
        'status: "to-read"',
        "rating: 0",
        "authors: []",
        f"authors_unresolved: {json.dumps(authors, ensure_ascii=False)}",
        f"sha256: {json.dumps([r['sha256']] if r.get('sha256') else [])}",
        f"pdf: {yaml_str(r.get('pdf', ''))}",
        f"topics: {json.dumps(['[[' + DOCS[d].split(' — ')[0] + ']]' for d in r['why']], ensure_ascii=False)}",
        f"cited_in: {json.dumps(cited_in, ensure_ascii=False)}",
        f"created: {yaml_str(TODAY)}",
        'created_by: "build_vault.py"',
        "---",
        "",
    ]
    if r.get("pdf"):
        lines += [f"📄 PDF: [[{Path(r['pdf']).name}]]", ""]
    else:
        lines += ["> [!info] Sin PDF en el vault", "> No está en arXiv (o el título no coincidía); solo se registra la cita. Enlace: " + (url or "—"), ""]
    lines += ["## Abstract", ""]
    if m:
        lines += [f"{m['summary']} (arXiv)", ""]
    else:
        lines += ["<!-- Sin abstract registrado; rellenar con resolve.py metadata si se ingesta en Mnemos. -->", ""]
    lines += ["## Por qué es relevante", ""]
    for d, why in r["why"].items():
        lines.append(f"- **[[{Path(d).stem}]]** — {why}")
    lines += [
        "",
        "## 🧠 Key ideas (atomic)",
        "",
        "<!-- Vacío a propósito: las claims atómicas con página y `ev:` las escribe el pipeline `ingest` de Mnemos. -->",
        "",
        "## 📝 Notes on reading",
        "",
    ]
    if r.get("arxiv_found_by_title"):
        lines += [f"- Versión arXiv encontrada por título exacto: `{r['arxiv']}` (la cita original no la enlazaba).", ""]
    if r.get("arxiv_mismatch"):
        lines += [f"- ⚠️ El arXiv citado (`{r['arxiv']}`) devuelve otro título: “{r['arxiv_mismatch']}”. PDF no descargado.", ""]
    (SOURCES / f"{note_name(r)}.md").write_text("\n".join(lines))


def write_topics(refs):
    TOPICS.mkdir(exist_ok=True)
    for doc, topic in DOCS.items():
        short = topic.split(" — ")[0]
        mine = sorted((r for r in refs if doc in r["why"]), key=lambda r: (r["year"] or 0, r["citekey"]))
        if not mine:
            continue
        lines = [
            "---",
            'type: "topic"',
            f"title: {yaml_str(topic)}",
            f"document: \"[[{Path(doc).stem}]]\"",
            "---",
            "",
            f"# {topic}",
            "",
            f"Documento de investigación: [[{Path(doc).stem}]] · {len(mine)} fuentes, "
            f"{sum(1 for r in mine if r.get('pdf'))} con PDF.",
            "",
            "| Fuente | Año | PDF | Por qué |",
            "|---|---|---|---|",
        ]
        for r in mine:
            pdf = "✅" if r.get("pdf") else "—"
            why = r["why"][doc].replace("|", "\\|")
            lines.append(f"| [[{note_name(r)}\\|{r['citekey']}]] | {r['year'] or ''} | {pdf} | {why} |")
        (TOPICS / f"{short}.md").write_text("\n".join(lines) + "\n")


def write_home(refs):
    n_pdf = sum(1 for r in refs if r.get("pdf"))
    lines = [
        "# Research — Lie groups, geometric optimization & vision for robot arms",
        "",
        f"Vault generado por `tools/build_vault.py` el {TODAY}. {len(refs)} fuentes únicas, {n_pdf} PDFs de arXiv.",
        "",
        "## Documentos",
        "",
    ]
    for doc, topic in DOCS.items():
        if (ROOT / doc).exists():
            lines.append(f"- [[{Path(doc).stem}]] — {topic} · índice de fuentes: [[{topic.split(' — ')[0]}]]")
    lines += [
        "",
        "## Estructura",
        "",
        "- `Content/Papers/` — PDFs `<citekey>.pdf` (solo arXiv, título verificado contra la API de arXiv).",
        "- `Content/Sources/` — una nota por fuente con frontmatter estilo Mnemos (`source-note`).",
        "- `Topics/` — un índice por eje de investigación.",
        "",
        "## Sin PDF",
        "",
    ]
    for r in sorted(refs, key=lambda r: r["citekey"]):
        if not r.get("pdf"):
            lines.append(f"- [[{note_name(r)}\\|{r['citekey']}]] — {r['url'] or 'sin enlace'}")
    (ROOT / "Home.md").write_text("\n".join(lines) + "\n")


def main():
    refs = parse_bibliographies()
    print(f"{len(refs)} unique references")
    resolve_arxiv(refs)
    make_citekeys(refs)
    download_pdfs(refs)
    SOURCES.mkdir(parents=True, exist_ok=True)
    # Notes that went through tools/ingest.py carry `ingested:` and are never overwritten.
    ingested = {p.name.split(" - ")[0] for p in SOURCES.glob("*.md") if "\ningested:" in p.read_text()}
    for old in SOURCES.glob("*.md"):
        if old.name.split(" - ")[0] not in ingested:
            old.unlink()
    for r in refs:
        if r["citekey"] not in ingested:
            write_source_note(r)
    (ROOT / "tools" / "arxiv_meta.json").write_text(json.dumps(
        {r["arxiv"]: r["arxiv_meta"] for r in refs if r.get("arxiv_meta")}, ensure_ascii=False, indent=1))
    write_topics(refs)
    write_home(refs)
    (ROOT / "tools" / "references.json").write_text(json.dumps(
        [{k: v for k, v in r.items() if k != "arxiv_meta"} for r in refs], ensure_ascii=False, indent=1))
    print(f"done: {len(refs)} sources, {sum(1 for r in refs if r.get('pdf'))} PDFs")


if __name__ == "__main__":
    main()
