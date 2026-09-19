#!/usr/bin/env python3
"""Promote for the research vault — Mnemos' promote skill (harness.md §4.1 step 8), ported.

Concept notes go to Content/Concepts/, their topics to Content/Topics/. The research index notes in
Topics/ and the 0x_ documents are never touched. The reader confirms at the gate before `apply`.

    PY=~/Documents/Mnemos/.venv/bin/python
    $PY tools/promote.py candidates                        # names at thresholds.promotion_bar
    $PY tools/promote.py prepare --packets packets.json    # one packet per theme -> _harness/promote/packets/
    $PY tools/promote.py find --pattern "<regex>"          # claims whose sentence matches
    $PY tools/promote.py lint --from <reply>               # drafter's own lint (C1-C9, RC4)
    $PY tools/promote.py check                             # all replies -> _harness/promote/gate.md
    $PY tools/promote.py apply --reader "<name>"           # after the reader's yes (decisions.json)
"""
import argparse
import collections
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
SOURCES = ROOT / "Content" / "Sources"
CONCEPTS = ROOT / "Content" / "Concepts"
CTOPICS = ROOT / "Content" / "Topics"
WORK = ROOT / "_harness" / "promote"
LOG = ROOT / "_harness" / "log" / "promote.jsonl"
BAR = 2
ELEMENT_TYPES = {"method", "process", "framework", "phenomenon", "concept", "metric", "instrument", "data-modality"}
REL_TYPES = {"solves", "specialises", "requires", "contradicts", "correlates"}
BAD_TITLE = re.compile(r'[/\\:*?"<>|#^\[\]]')
CLAIMS_H = "## 🧠 Key ideas (atomic)"
CLAIM_RE = re.compile(r"^- (?P<sent>.+?) \((?P<cite>[^()]*?\d{4}[a-z]?)\) `ev:\w+` p\. (?:\d+|none) \^(?P<id>[a-z0-9]+-\d{3})\s*$")
TODAY = datetime.date.today().isoformat()


def norm(name):
    k = re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()
    return re.sub(r"s\b", "", k)


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1] / max(len(a), len(b), 1)


def log(event, **kw):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps({"t": datetime.datetime.now().isoformat(timespec="seconds"), "event": event, **kw}, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- vault reading

def ingested_notes():
    out = {}
    for p in sorted(SOURCES.glob("*.md")):
        t = p.read_text()
        if "\ningested:" in t:
            out[p.name.split(" - ")[0]] = p
    return out


def claims_of(path):
    """{claim id: (line, sentence)} for the claims of one source note."""
    out, inside = {}, False
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            inside = line.strip() == CLAIMS_H
            continue
        if inside:
            m = CLAIM_RE.match(line)
            if m:
                out[m.group("id")] = (line, m.group("sent"))
    return out


def all_claims():
    idx = {}
    for ck, p in ingested_notes().items():
        for cid, (line, sent) in claims_of(p).items():
            idx[cid] = {"note": p.stem, "path": str(p), "sentence": sent}
    return idx


def suggestions():
    by = collections.defaultdict(lambda: {"names": collections.Counter(), "sources": set(), "why": []})
    for ck, p in ingested_notes().items():
        m = re.search(r"## Suggested new concepts\n(.*?)(?=\n## |\Z)", p.read_text(), re.S)
        for line in (m.group(1) if m else "").splitlines():
            mm = re.match(r"- (.+?) — (.*)", line)
            if mm:
                e = by[norm(mm.group(1))]
                e["names"][mm.group(1).strip()] += 1
                e["sources"].add(ck)
                e["why"].append(f"{ck}: {mm.group(2).strip()}")
    return by


def existing(folder):
    return sorted(p.stem for p in folder.glob("*.md")) if folder.exists() else []


# ---------------------------------------------------------------- commands

def cmd_candidates(a):
    rows = []
    concepts = existing(CONCEPTS)
    for key, e in suggestions().items():
        if len(e["sources"]) < BAR:
            continue
        name = e["names"].most_common(1)[0][0]
        exact = [c for c in concepts if norm(c) == key]
        near = [c for c in concepts if c not in exact and lev(norm(c), key) <= 0.2]
        route = f"exact [[{exact[0]}]]" if exact else ("near " + ", ".join(near) if near else "new")
        rows.append((len(e["sources"]), name, route, sorted(e["sources"])))
    for n, name, route, srcs in sorted(rows, key=lambda r: (-r[0], r[1])):
        print(f"{n}  {name:<42} {route:<10} {', '.join(srcs)}")
    print(f"{len(rows)} names at the bar ({BAR} independent sources)")
    return 0


def claims_naming(name, idx, limit=40):
    words = [w for w in re.split(r"[^A-Za-z0-9]+", name) if len(w) > 2]
    if not words:
        return []
    pat = re.compile(r"\b" + r"\W+".join(re.escape(w[:-1] if w.lower().endswith("s") else w) for w in words), re.I)
    return [{"id": "^" + cid, "note": c["note"], "sentence": c["sentence"]}
            for cid, c in idx.items() if pat.search(c["sentence"])][:limit]


def cmd_prepare(a):
    spec = json.loads(Path(a.packets).read_text())
    sugg, idx = suggestions(), all_claims()
    notes = ingested_notes()
    (WORK / "packets").mkdir(parents=True, exist_ok=True)
    (WORK / "replies").mkdir(parents=True, exist_ok=True)
    def entries(p):
        # a name is either a string (takes the packet's status) or {"name": ..., "status": ...}
        for e in p["names"]:
            yield (e["name"], e["status"]) if isinstance(e, dict) else (e, p.get("status", "at-bar"))

    all_names = [n for p in spec for n, _ in entries(p)]
    for p in spec:
        names, srcs = [], set()
        for n, status in entries(p):
            e = sugg.get(norm(n), {"names": collections.Counter(), "sources": set(), "why": []})
            srcs |= e["sources"]
            names.append({"name": n, "status": status, "suggested_by": sorted(e["sources"]),
                          "why": e["why"], "claims": claims_naming(n, idx)})
            for c in names[-1]["claims"]:
                srcs.add(c["note"].split(" - ")[0])
        packet = {
            "packet": p["id"], "prompt_version": re.search(r"^prompt_version:\s*(\S+)", (TOOLS / "prompts" / "concept-drafter.md").read_text(), re.M).group(1),
            "status": p.get("status", "at-bar"), "topic_hint": p.get("topic_hint", ""), "vault": str(ROOT),
            "names": names, "source_notes": sorted(str(notes[s]) for s in srcs if s in notes),
            "all_names": all_names, "existing_concepts": existing(CONCEPTS), "existing_topics": existing(CTOPICS),
            "reply": str(WORK / "replies" / f"{p['id']}.json"),
        }
        out = WORK / "packets" / f"{p['id']}.json"
        out.write_text(json.dumps(packet, ensure_ascii=False, indent=1))
        print(f"{out.name}: {len(names)} names, {len(packet['source_notes'])} source notes")
    return 0


def cmd_find(a):
    pat = re.compile(a.pattern, re.I)
    for cid, c in all_claims().items():
        if pat.search(c["sentence"]):
            print(f"^{cid}  {c['sentence']}")
    return 0


def lint_reply(env, idx, taken_phrases=None):
    hard, soft = [], []
    concepts = existing(CONCEPTS)
    if env.get("agent") != "concept-drafter":
        hard.append("HARD envelope: agent")
    if not env.get("topic") or BAD_TITLE.search(env.get("topic", "")):
        hard.append(f"HARD T1: topic title {env.get('topic')!r}")
    if not env.get("scope"):
        hard.append("HARD T1: empty scope")
    taken = taken_phrases if taken_phrases is not None else collections.defaultdict(list)
    titles = [c.get("title", "") for c in env.get("concepts", [])]
    for c in env.get("concepts", []):
        t = c.get("title", "")
        if not t or BAD_TITLE.search(t):
            hard.append(f"HARD C1 {t!r}: bad title")
        if t in concepts:
            hard.append(f"HARD C1 {t}: already a concept note (route, not promote)")
        d = c.get("definition", "").strip()
        if not d or len(re.findall(r"[.!?](\s|$)", d)) != 1 or not d.endswith("."):
            hard.append(f"HARD C1 {t}: definition must be one sentence")
        if c.get("element_type") not in ELEMENT_TYPES:
            hard.append(f"HARD C2 {t}: element_type {c.get('element_type')!r}")
        ev = c.get("evidence", [])
        if len(ev) < 2:
            hard.append(f"HARD C3 {t}: fewer than two evidence claims")
        for e in ev:
            cid = e.get("id", "").lstrip("^")
            ph = e.get("phrase", "")
            if cid not in idx:
                hard.append(f"HARD C4 {t}: evidence {cid} is not a claim")
                continue
            sent = idx[cid]["sentence"]
            if not ph or re.search(r"[\[\]|`]", ph) or not re.search(r"(?<!\w)" + re.escape(ph) + r"(?!\w)", sent):
                hard.append(f"HARD C5 {t}: phrase {ph!r} not a word-bounded substring of {cid}")
                continue
            start = sent.index(ph)
            for (s0, s1, other) in taken[cid]:
                if start < s1 and s0 < start + len(ph) and other != t:
                    hard.append(f"HARD C5 {t}: phrase overlaps {other}'s phrase in {cid}")
            taken[cid].append((start, start + len(ph), t))
        for r in c.get("relations", []):
            if r.get("type") not in REL_TYPES:
                hard.append(f"HARD C7 {t}: relation type {r.get('type')!r}")
            if r.get("target") not in titles + concepts:
                soft.append(f"SOFT C7 {t}: relation target {r.get('target')!r} is not drafted (kept only if drafted elsewhere)")
            if r.get("evidence_id", "").lstrip("^") not in idx:
                hard.append(f"HARD C8 {t}: relation evidence {r.get('evidence_id')} is not a claim")
        for other in titles + concepts:
            if other != t and lev(norm(other), norm(t)) <= 0.2:
                soft.append(f"SOFT C9 {t} ~ {other} — list it under near_pairs; never merge (RC2)")
    return hard, soft


def cmd_lint(a):
    env = json.loads(Path(a.__dict__["from"]).read_text())
    hard, soft = lint_reply(env, all_claims())
    for l in hard + soft:
        print(l)
    print(f"{len(hard)} hard, {len(soft)} soft")
    return 2 if hard else (1 if soft else 0)


def load_replies():
    return [(p.stem, json.loads(p.read_text())) for p in sorted((WORK / "replies").glob("*.json"))]


def decisions():
    p = WORK / "decisions.json"
    return json.loads(p.read_text()) if p.exists() else {}


def resolved(replies, dec):
    """Apply the reader's decisions: strike, rename, retopic, topics."""
    strike, rename, retopic = set(dec.get("strike", [])), dec.get("rename", {}), dec.get("retopic", {})
    out = []
    for pid, env in replies:
        for c in env.get("concepts", []):
            if c["title"] in strike:
                continue
            c = dict(c, title=rename.get(c["title"], c["title"]))
            c["topic"] = retopic.get(c["title"], dec.get("topic_rename", {}).get(env["topic"], env["topic"]))
            out.append((pid, env, c))
    return out


def cmd_check(a):
    replies, idx, dec = load_replies(), all_claims(), decisions()
    taken = collections.defaultdict(list)
    lines, problems = [f"# Promote gate — {TODAY}", ""], []
    for pid, env in replies:
        hard, soft = lint_reply(env, idx, taken)
        problems += [f"{pid}: {h}" for h in hard]
        lines += [f"## Packet `{pid}` → topic **{env['topic']}**", "", f"> {env['scope']}", ""]
        lines += ["| Concept | Type | Status | Evidence | Sources | Definition |", "|---|---|---|---|---|---|"]
        for c in env["concepts"]:
            srcs = {idx[e['id'].lstrip('^')]['note'].split(' - ')[0] for e in c.get("evidence", []) if e['id'].lstrip('^') in idx}
            lines.append(f"| {c['title']} | {c['element_type']} | {c.get('status','')} | {len(c.get('evidence', []))} | {len(srcs)} | {c['definition']} |")
        near = [f"- {c['title']} ~ {n['name']}: {n['why']}" for c in env["concepts"] for n in c.get("near_pairs", [])]
        rels = [f"- {c['title']} —{r['type']}→ {r['target']} ({r['evidence_id']})" for c in env["concepts"] for r in c.get("relations", [])]
        if rels:
            lines += ["", "**Relations**", ""] + rels
        if near:
            lines += ["", "**Near pairs (reader decides, RC2)**", ""] + near
        if env.get("struck"):
            lines += ["", "**Struck by drafter**", ""] + [f"- {s['name']}: {s['why']}" for s in env["struck"]]
        lines += [""] + [f"- {s}" for s in soft] + [""]
    (WORK / "gate.md").write_text("\n".join(lines))
    for p in problems:
        print(p)
    print(f"gate: {WORK / 'gate.md'} · {sum(len(e['concepts']) for _, e in replies)} concepts · {len(replies)} topics · problems {len(problems)}")
    return 2 if problems else 0


def link_phrase(line, phrase, title):
    target = title if phrase == title else f"{title}|{phrase}"
    sent_end = line.rindex(" (")  # the citation parenthesis
    head = line[:sent_end]
    new_head = re.sub(r"(?<![\w\[|])" + re.escape(phrase) + r"(?![\w\]])", f"[[{target}]]", head, count=1)
    return new_head + line[sent_end:]


def cmd_apply(a):
    replies, idx, dec = load_replies(), all_claims(), decisions()
    if cmd_check(a) != 0:
        print("check fails: nothing applied", file=sys.stderr)
        return 2
    CONCEPTS.mkdir(parents=True, exist_ok=True)
    CTOPICS.mkdir(parents=True, exist_ok=True)
    items = resolved(replies, dec)
    titles = {c["title"] for _, _, c in items}
    edits = collections.defaultdict(list)  # note path -> [(claim id, phrase, title)]
    by_topic = collections.defaultdict(list)
    for pid, env, c in items:
        by_topic[c["topic"]].append((env, c))
        ev_lines = []
        for e in c["evidence"]:
            cid = e["id"].lstrip("^")
            if cid in dec.get("drop_evidence", {}).get(c["title"], []):
                continue
            n = idx[cid]
            edits[n["path"]].append((cid, e["phrase"], c["title"]))
            ev_lines.append(f"- [[{n['note']}#^{cid}]] — {n['sentence']}")
        rel_lines = []
        for r in c.get("relations", []):
            if r["target"] in titles and c["title"] not in dec.get("drop_relations", []):
                cid = r["evidence_id"].lstrip("^")
                rel_lines += [f"- RELATES_TO → [[{r['target']}]]", f"  · type: {r['type']}", f"  · evidence: [[{idx[cid]['note']}#^{cid}]]"]
        srcs = sorted({idx[e['id'].lstrip('^')]['note'].split(' - ')[0] for e in c['evidence']})
        how = f"promoted at the bar from {len(srcs)} sources" if c.get("status") == "at-bar" else f"{c.get('status')} ({len(srcs)} sources)"
        body = [
            "---",
            f"aliases: {json.dumps(c.get('aliases', []), ensure_ascii=False)}",
            "type: concept",
            f"element_type: {c['element_type']}",
            f'topic: "[[{c["topic"]}]]"',
            f"topics: {json.dumps(['[[' + c['topic'] + ']]'], ensure_ascii=False)}",
            f"created: {TODAY}",
            "---",
            "",
            "## Working definition",
            "",
            c["definition"],
            "",
            "## Evidence",
            "",
            *ev_lines,
            "",
            "## Relations",
            "",
            *rel_lines,
            "",
            "## Open questions",
            "",
            "## History",
            "",
            f"- {TODAY} · {a.reader} · created: {how} · topic: {c['topic']} (drafter's packet `{pid}`, confirmed at the gate)",
            "",
        ]
        (CONCEPTS / f"{c['title']}.md").write_text("\n".join(body))
    for topic, members in by_topic.items():
        env = members[0][0]
        meta = dec.get("topics", {}).get(topic, {"parent": "root", "reason": "new area for promoted concepts"})
        path = CTOPICS / f"{topic}.md"
        bullets = [f"- [[{c['title']}]] — {c['definition']}" for _, c in members]
        if path.exists():
            # an existing topic keeps its scope and concepts; the new concepts and a history line are appended
            t = path.read_text()
            t = t.replace("\n\n## Subtopics", "\n" + "".join(b + "\n" for b in bullets) + "\n## Subtopics", 1)
            t = t.rstrip("\n") + f"\n- {TODAY} · {a.reader} · added {len(members)} concepts — {meta['reason']}\n"
            path.write_text(t)
            continue
        body = [
            "---", "aliases: []", "type: topic", f"parent: {meta['parent']}", f"created: {TODAY}", "---", "",
            "## Scope", "", meta.get("scope", env["scope"]), "",
            "## Concepts", "", *bullets, "",
            "## Subtopics", "", "## Related topics", "", "## ❓ Open questions", "",
            "## Problems", "", "- none yet: no problem names this topic as its topic", "",
            "## History", "", f"- {TODAY} · {a.reader} · parent: {meta['parent']} — {meta['reason']}", "",
        ]
        path.write_text("\n".join(body))
    linked = 0
    for path, eds in edits.items():
        p = Path(path)
        lines = p.read_text().split("\n")
        for i, line in enumerate(lines):
            m = CLAIM_RE.match(line)
            if not m:
                continue
            for cid, phrase, title in eds:
                if cid == m.group("id") and f"[[{title}" not in line:
                    new = link_phrase(line, phrase, title)
                    if new != line:
                        linked += 1
                        line = new
            lines[i] = line
        p.write_text("\n".join(lines))
    log("apply", reader=a.reader, concepts=len(items), topics=len(by_topic), links=linked)
    print(f"applied: {len(items)} concepts in {CONCEPTS.relative_to(ROOT)}, {len(by_topic)} topics in {CTOPICS.relative_to(ROOT)}, {linked} claim links")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("candidates")
    sub.add_parser("prepare").add_argument("--packets", required=True)
    sub.add_parser("find").add_argument("--pattern", required=True)
    sub.add_parser("lint").add_argument("--from", required=True)
    sub.add_parser("check")
    sub.add_parser("apply").add_argument("--reader", required=True)
    a = ap.parse_args()
    sys.exit({"candidates": cmd_candidates, "prepare": cmd_prepare, "find": cmd_find, "lint": cmd_lint,
              "check": cmd_check, "apply": cmd_apply}[a.cmd](a))


if __name__ == "__main__":
    main()
