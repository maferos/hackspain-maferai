#!/usr/bin/env python3
"""Ingest for the research vault — the Mnemos writer/checker protocol, ported.

Mnemos' ingest-writer and ingest-checker skills (harness.md §4.1 step 4), without its plumbing:
one run folder per paper under _harness/runs/<citekey>/, the text cache under _harness/cache/.

    PY=~/Documents/Mnemos/.venv/bin/python        # has PyMuPDF
    $PY tools/ingest.py cache                      # PDF -> cache text with <<page N>> markers
    $PY tools/ingest.py prepare --run <citekey>    # packet-writer.json
    $PY tools/ingest.py lint --run <citekey> --from <reply>      # writer's own lint (dry collect)
    $PY tools/ingest.py collect-writer --run <citekey>           # mint ids -> draft.md, packet-check.json
    $PY tools/ingest.py collect-checker --run <citekey>          # drop non-found, renumber gap-free
    $PY tools/ingest.py assemble --run <citekey>                 # write Content/Sources/<note>.md
    $PY tools/ingest.py status                                   # one line per paper

Rules kept from Mnemos: S3 claim shape, S4 ids minted by code and renumbered gap-free, S5 locator
within the page range, S6 only `found` enters, S7 15-25 words, RC3 closed ev: set, pass A (every
number of a claim is in the cached text). Exit codes: 0 clean · 1 SOFT only / missing reply · 2 HARD.
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
PAPERS = ROOT / "Content" / "Papers"
SOURCES = ROOT / "Content" / "Sources"
CACHE = ROOT / "_harness" / "cache"
RUNS = ROOT / "_harness" / "runs"
LOG = ROOT / "_harness" / "log" / "ingest.jsonl"
REFS = TOOLS / "references.json"
EV = {"measured", "computed", "reported", "cited", "asserted", "abstract", "TODO"}
VERDICTS = {"found", "not-found", "paraphrased"}
CLAIMS_H = "## 🧠 Key ideas (atomic)"
SECTIONS = ["## Abstract", CLAIMS_H, "## 🎯 Contributions", "## 📖 Glossary", "## ❓ Open questions",
            "## 📝 Notes on reading", "## Suggested new concepts"]
CLAIM_RE = re.compile(r"^- (?P<sent>.+?) \((?P<cite>[^()]*?\d{4}[a-z]?)\) `ev:(?P<ev>[A-Za-z]+)` p\. (?P<loc>\d+|none)(?P<id> \^\S+)?\s*$")
HEDGES = ["because", "therefore", "thus", "hence", "so that", "best", "first", "always", "never", "only"]


def prompt_version(name):
    text = (TOOLS / "prompts" / f"{name}.md").read_text()
    m = re.search(r"^prompt_version:\s*(\S+)", text, re.M)
    return m.group(1) if m else ""


def prompt_hash(name):
    return hashlib.sha256((TOOLS / "prompts" / f"{name}.md").read_bytes()).hexdigest()[:12]


def refs_by_key():
    return {r["citekey"]: r for r in json.loads(REFS.read_text())}


def run_dir(citekey):
    d = RUNS / citekey
    d.mkdir(parents=True, exist_ok=True)
    return d


def log(event, citekey, **kw):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    rec = {"t": datetime.datetime.now().isoformat(timespec="seconds"), "event": event, "citekey": citekey, **kw}
    with LOG.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def pages_of(citekey):
    text = (CACHE / f"{citekey}.txt").read_text()
    return len(re.findall(r"^<<page \d+>>$", text, re.M)), text


# ---------------------------------------------------------------- cache

def cmd_cache(a):
    import pymupdf
    CACHE.mkdir(parents=True, exist_ok=True)
    for pdf in sorted(PAPERS.glob("*.pdf")):
        out = CACHE / f"{pdf.stem}.txt"
        if out.exists() and not a.force:
            continue
        doc = pymupdf.open(pdf)
        parts = [f"<<page {i}>>\n{page.get_text('text')}" for i, page in enumerate(doc, 1)]
        text = "\n".join(parts)
        out.write_text(text)
        words = len(text.split())
        flag = "  low_yield" if words < 300 * max(1, len(doc)) / 4 else ""
        print(f"{pdf.stem}: {len(doc)} pages, {words} words{flag}")
    return 0


# ---------------------------------------------------------------- prepare

def cmd_prepare(a):
    ck = a.run
    ref = refs_by_key().get(ck)
    if not ref:
        print(f"unknown citekey {ck}", file=sys.stderr)
        return 2
    if not (CACHE / f"{ck}.txt").exists():
        print(f"no cache for {ck}: run `cache` first (no PDF → no claims)", file=sys.stderr)
        return 2
    n, _ = pages_of(ck)
    meta_path = TOOLS / "arxiv_meta.json"
    meta = json.loads(meta_path.read_text()).get(ref.get("arxiv") or "", {}) if meta_path.exists() else {}
    packet = {
        "packet": f"{ck}/packet-writer.json",
        "citekey": ck,
        "metadata": {
            "title": ref["title"],
            "year": ref["year"],
            "authors": meta.get("authors") or [x.strip() for x in re.split(r",| and ", ref["authors"]) if x.strip()],
            "venue": "arXiv preprint" if ref.get("arxiv") and not ref.get("doi") else "",
            "abstract": meta.get("summary", ""),
            "abstract_source": "arXiv" if meta.get("summary") else "",
        },
        "identifier": {"doi": ref.get("doi") or (f"10.48550/arXiv.{ref['arxiv']}" if ref.get("arxiv") else ""),
                       "arxiv": ref.get("arxiv") or ""},
        "cache": str(CACHE / f"{ck}.txt"),
        "pages": n,
        "essence": False,
        "supplement_of": None,
        "prior_read": None,
        "reply": str(run_dir(ck) / "writer-reply.json"),
    }
    (run_dir(ck) / "packet-writer.json").write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    print(run_dir(ck) / "packet-writer.json")
    return 0


# ---------------------------------------------------------------- envelope / lint

def load_envelope(path, agent):
    raw = Path(path).read_text().strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
    start = raw.find("{")
    env = json.loads(raw[start:raw.rfind("}") + 1])
    problems = []
    if env.get("agent") != agent:
        problems.append(f"HARD envelope: agent is {env.get('agent')!r}, expected {agent!r}")
    if env.get("prompt_version") != prompt_version(agent):
        problems.append(f"HARD envelope: prompt_version {env.get('prompt_version')!r} != {prompt_version(agent)!r}")
    return env, problems


def split_sections(note):
    out, cur = {}, None
    for line in note.splitlines():
        if line.startswith("## "):
            cur = line.strip()
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return out


def check_draft(ck, note, pages, cache_text):
    hard, soft = [], []
    secs = split_sections(note)
    for h in SECTIONS:
        if h not in secs:
            hard.append(f"HARD structure: missing section {h}")
    if "[[" in note:
        hard.append("HARD X1: a [[link]] in the draft")
    if "> [!abstract] One-sentence summary" not in note:
        hard.append("HARD structure: missing one-sentence summary callout")
    claims = [l for l in secs.get(CLAIMS_H, []) if l.startswith("- ")]
    if not claims:
        hard.append("HARD S3: no claims")
    if len(claims) > 70:
        soft.append(f"SOFT volume: {len(claims)} claims (> 70)")
    flat_cache = re.sub(r"\s+", " ", cache_text)
    for i, line in enumerate(claims, 1):
        m = CLAIM_RE.match(line)
        if not m:
            hard.append(f"HARD S3 claim {i}: not `- sentence (Author, year) `ev:code` p. N`: {line[:90]}")
            continue
        if m.group("id"):
            hard.append(f"HARD S4 claim {i}: carries an id; ids are minted by code")
        if m.group("ev") not in EV:
            hard.append(f"HARD RC3 claim {i}: ev:{m.group('ev')} not in {sorted(EV)}")
        loc = m.group("loc")
        if loc != "none" and not (1 <= int(loc) <= pages):
            hard.append(f"HARD S5 claim {i}: p. {loc} outside 1..{pages}")
        sent = m.group("sent")
        wc = len(sent.split())
        if not 15 <= wc <= 25:
            soft.append(f"SOFT S7 claim {i}: {wc} words")
        for num in re.findall(r"(?<![\w.])\d+(?:[.,]\d+)*%?", sent):
            if len(num) > 1 and num.rstrip("%") not in flat_cache:
                soft.append(f"SOFT pass A claim {i}: number {num} not in cached text")
        low = sent.lower()
        for w in HEDGES:
            if re.search(rf"\b{w}\b", low):
                soft.append(f"SOFT (S6 lint) claim {i}: '{w}' — keep only if the page says so")
                break
    return claims, hard, soft


def lint_reply(ck, path):
    env, problems = load_envelope(path, "ingest-writer")
    n, text = pages_of(ck)
    _, hard, soft = check_draft(ck, env.get("note", ""), n, text)
    hard = problems + hard
    return env, hard, soft


def cmd_lint(a):
    _, hard, soft = lint_reply(a.run, a.__dict__["from"])
    for l in hard + soft:
        print(l)
    print(f"{len(hard)} hard, {len(soft)} soft")
    return 2 if hard else (1 if soft else 0)


# ---------------------------------------------------------------- collect-writer

def mint(ck, claim_lines):
    base = ck.lower()
    out = []
    for i, line in enumerate(claim_lines, 1):
        out.append(re.sub(r"( \^\S+)?\s*$", f" ^{base}-{i:03d}", line, count=1))
    return out


def replace_claims(note, new_claims):
    lines, out, in_claims = note.splitlines(), [], False
    for line in lines:
        if line.startswith("## "):
            if in_claims:
                out += new_claims + [""]
            in_claims = line.strip() == CLAIMS_H
            out.append(line)
            if in_claims:
                out.append("")
            continue
        if in_claims:
            continue
        out.append(line)
    return "\n".join(out) + "\n"


def cmd_collect_writer(a):
    ck, d = a.run, run_dir(a.run)
    reply = d / "writer-reply.json"
    if not reply.exists():
        print("no writer reply: dispatch once more", file=sys.stderr)
        return 1
    env, hard, soft = lint_reply(ck, reply)
    (d / "writer-raw.txt").write_text(reply.read_text())
    if hard:
        for l in hard:
            print(l)
        log("collect-writer-refused", ck, hard=hard)
        return 2
    note = env["note"]
    secs = split_sections(note)
    claims = [l for l in secs[CLAIMS_H] if l.startswith("- ")]
    draft = replace_claims(note, mint(ck, claims))
    (d / "draft.md").write_text(draft)
    (d / "writer-meta.json").write_text(json.dumps({"not_checked": env.get("not_checked", []), "soft": soft}, ensure_ascii=False, indent=1))
    packet = {"packet": f"{ck}/packet-check.json", "draft": str(d / "draft.md"), "cache": str(CACHE / f"{ck}.txt"),
              "reply": str(d / "checker-reply.json")}
    (d / "packet-check.json").write_text(json.dumps(packet, indent=1))
    log("collect-writer", ck, claims=len(claims), soft=len(soft), not_checked=len(env.get("not_checked", [])))
    print(f"{ck}: {len(claims)} claims minted, {len(soft)} soft")
    return 0


# ---------------------------------------------------------------- collect-checker

def cmd_collect_checker(a):
    ck, d = a.run, run_dir(a.run)
    reply = d / "checker-reply.json"
    if not reply.exists():
        print("no checker reply: dispatch once more", file=sys.stderr)
        return 1
    env, problems = load_envelope(reply, "ingest-checker")
    (d / "raw-checker.txt").write_text(reply.read_text())
    draft = (d / "draft.md").read_text()
    claims = [l for l in split_sections(draft)[CLAIMS_H] if l.startswith("- ")]
    ids = [re.search(r"\^(\S+)\s*$", l).group(1) for l in claims]
    items = {}
    for it in env.get("items", []):
        cid = it.get("claim", "").lstrip("^")
        if cid in items:
            problems.append(f"HARD S6: {cid} has two verdicts")
        if it.get("verdict") not in VERDICTS:
            problems.append(f"HARD S6: {cid} verdict {it.get('verdict')!r}")
        items[cid] = it
    missing = [i for i in ids if i not in items]
    extra = [i for i in items if i not in ids]
    if missing or extra:
        problems.append(f"HARD S6: missing verdicts {missing[:5]}… extra {extra[:5]}")
    if problems:
        for p in problems:
            print(p)
        log("collect-checker-refused", ck, problems=problems)
        return 2
    kept, dropped, verdicts, doubts = [], [], [], []
    for line, cid in zip(claims, ids):
        it = items[cid]
        if it["verdict"] == "found":
            kept.append((line, cid, it))
        else:
            dropped.append({"claim": cid, "sentence": line, "verdict": it["verdict"], "quote": it.get("quote", ""), "note": it.get("note", "")})
            log("claim-dropped", ck, claim=cid, verdict=it["verdict"], sentence=line, quote=it.get("quote", ""))
        if it.get("note"):
            doubts.append(f"EV? {cid}: {it['note']}")
    new_lines = mint(ck, [l for l, _, _ in kept])
    for (line, old, it), new in zip(kept, new_lines):
        verdicts.append({"claim": re.search(r"\^(\S+)$", new).group(1), "original_claim": old, "verdict": "found",
                         "quote": it.get("quote", ""), "page": it.get("page")})
    (d / "draft.md").write_text(replace_claims(draft, new_lines))
    (d / "checker.json").write_text(json.dumps({"items": verdicts, "dropped": dropped, "doubts": doubts,
                                                "not_checked": env.get("not_checked", [])}, ensure_ascii=False, indent=1))
    log("collect-checker", ck, kept=len(kept), dropped=len(dropped))
    print(f"{ck}: kept {len(kept)}, dropped {len(dropped)}")
    for x in doubts:
        print(x)
    return 0


# ---------------------------------------------------------------- assemble

def yaml_str(s):
    return json.dumps(s if s is not None else "", ensure_ascii=False)


def cmd_assemble(a):
    ck, d = a.run, run_dir(a.run)
    if not (d / "checker.json").exists():
        print("not checked yet", file=sys.stderr)
        return 1
    ref = refs_by_key()[ck]
    old = next(SOURCES.glob(f"{ck} - *.md"), None)
    if old is None:
        print(f"no source note for {ck}: run build_vault.py first", file=sys.stderr)
        return 2
    old_text = old.read_text()
    fm_end = old_text.index("\n---", 3)
    fm = old_text[4:fm_end].splitlines()
    fm = [l for l in fm if not l.startswith(("created_by:", "ingested:", "claims:"))]
    chk = json.loads((d / "checker.json").read_text())
    fm += [f"created_by: {yaml_str('ingest-writer@' + prompt_hash('ingest-writer'))}",
           f"checked_by: {yaml_str('ingest-checker@' + prompt_hash('ingest-checker'))}",
           f"ingested: {yaml_str(datetime.date.today().isoformat())}",
           f"claims: {len(chk['items'])}"]
    why = re.search(r"## Por qué es relevante\n(.*?)(?=\n## |\Z)", old_text, re.S)
    draft = (d / "draft.md").read_text()
    body = draft[draft.index("\n---", 3) + 4:].lstrip("\n") if draft.startswith("---") else draft
    pdf_line = f"📄 PDF: [[{ck}.pdf]]\n\n" if ref.get("pdf") else ""
    extra = ""
    if why:
        extra = "\n## Por qué es relevante\n" + why.group(1).rstrip() + "\n"
    if chk["dropped"]:
        extra += f"\n<!-- ingest-checker dropped {len(chk['dropped'])} claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->\n"
    out = "---\n" + "\n".join(fm) + "\n---\n\n" + pdf_line + body.rstrip() + "\n" + extra
    old.write_text(out)
    log("assemble", ck, note=old.name, claims=len(chk["items"]), dropped=len(chk["dropped"]))
    print(f"{old.name}: {len(chk['items'])} claims, {len(chk['dropped'])} dropped")
    return 0


# ---------------------------------------------------------------- provenance tier 1 (S12)

NUM_RE = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)*%?")
PROVENANCE_FLOOR_CPP = 1200


def page_texts(ck):
    text = (CACHE / f"{ck}.txt").read_text()
    parts = re.split(r"^<<page (\d+)>>$", text, flags=re.M)
    return {int(parts[i]): re.sub(r"\s+", " ", parts[i + 1]) for i in range(1, len(parts) - 1, 2)}


def cmd_numbers(a):
    """A verdict per claim: found | drifted | numberless | low-yield | unreadable. Drifted is a candidate, never a verdict."""
    counts, rows = {}, []
    for note in sorted(SOURCES.glob("*.md")):
        t = note.read_text()
        if "\ningested:" not in t:
            continue
        ck = note.name.split(" - ")[0]
        if a.citekey and ck != a.citekey:
            continue
        try:
            pages = page_texts(ck)
        except FileNotFoundError:
            pages = None
        for line in split_sections(t).get(CLAIMS_H, []):
            m = CLAIM_RE.match(re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", line))
            if not m:
                continue
            cid = m.group("id").strip().lstrip("^")
            nums = [n for n in NUM_RE.findall(m.group("sent")) if len(n.rstrip("%")) > 1]
            loc = m.group("loc")
            if pages is None:
                v, detail = "unreadable", "no cache"
            elif not nums:
                v, detail = "numberless", ""
            elif loc == "none" or int(loc) not in pages:
                v, detail = "drifted", f"no page {loc}"
            else:
                page = pages[int(loc)]
                if len(page) < PROVENANCE_FLOOR_CPP:
                    v, detail = "low-yield", f"p. {loc} has {len(page)} chars"
                else:
                    missing = [n for n in nums if n.rstrip("%") not in page]
                    if not missing:
                        v, detail = "found", ""
                    else:
                        elsewhere = [pn for pn, pt in pages.items() if all(n.rstrip("%") in pt for n in missing)]
                        v = "drifted"
                        detail = f"{', '.join(missing)} not on p. {loc}" + (f"; on p. {elsewhere[0]}" if elsewhere else "; not in the paper")
            counts[v] = counts.get(v, 0) + 1
            rows.append({"claim": cid, "note": note.name, "verdict": v, "numbers": nums, "detail": detail})
            if a.verbose or v in ("drifted", "low-yield", "unreadable"):
                print(f"{v:<11} {cid:<34} {detail}")
    out = ROOT / "_harness" / "provenance" / "tier1.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"counts": counts, "claims": rows}, ensure_ascii=False, indent=1))
    print("tier 1: " + " · ".join(f"{k} {counts.get(k, 0)}" for k in ("found", "drifted", "numberless", "low-yield", "unreadable")))
    print(f"written {out.relative_to(ROOT)} · tier 2 (adjudicator) not run: needs the reader's release")
    return 1 if counts.get("unreadable") else 0


# ---------------------------------------------------------------- status

def cmd_status(a):
    refs = refs_by_key()
    for ck in sorted(refs):
        d = RUNS / ck
        stage = ("assembled" if any("ingested:" in p.read_text() for p in SOURCES.glob(f"{ck} - *.md")) else
                 "checked" if (d / "checker.json").exists() else
                 "checker-pending" if (d / "packet-check.json").exists() else
                 "writer-pending" if (d / "packet-writer.json").exists() else
                 "cached" if (CACHE / f"{ck}.txt").exists() else "no-pdf")
        print(f"{stage:16} {ck}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cache"); c.add_argument("--force", action="store_true")
    for name in ("prepare", "collect-writer", "collect-checker", "assemble"):
        sub.add_parser(name).add_argument("--run", required=True)
    l = sub.add_parser("lint"); l.add_argument("--run", required=True); l.add_argument("--from", required=True)
    sub.add_parser("status")
    nb = sub.add_parser("numbers"); nb.add_argument("--citekey"); nb.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    fn = {"cache": cmd_cache, "prepare": cmd_prepare, "lint": cmd_lint, "collect-writer": cmd_collect_writer,
          "collect-checker": cmd_collect_checker, "assemble": cmd_assemble, "status": cmd_status, "numbers": cmd_numbers}[a.cmd]
    sys.exit(fn(a))


if __name__ == "__main__":
    main()
