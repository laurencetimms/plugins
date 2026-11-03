#!/usr/bin/env python3
"""Patch Bay curation tool: check, merge and measure the gear graph.

Usage:
  curate.py validate [FILE]                 check a graph or staging file (default: the seed)
  curate.py merge STAGING [--write]         merge staged finds into the seed (dry run unless --write)
  curate.py report [--era 1978-1986]        health metrics for the seed graph

A staging file has the same shape as the seed: {"nodes": {...}, "edges": [...], "sources": {...}}.
Nodes and sources it references may already exist in the seed. It may also carry
"updates": [{"match": {edge fields}, "set": {fields; null removes}, "add_sources": [...], "reason": "..."}]
to correct or upgrade existing edges; each match must hit exactly one edge.
"""
import json, os, re, statistics, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import graph as G  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(HERE, "..", "data", "seed-graph.json")
KINDS = {"song", "album", "machine", "artist"}
TYPES = {  # type: (allowed from-kinds, allowed to-kinds)
    "used": ({"song", "album"}, {"machine"}),
    "credit": ({"song", "album"}, {"artist"}),
    "member": ({"artist"}, {"artist"}),
    "on": ({"song"}, {"album"}),
    "drew-on": ({"song"}, {"song"}),
    "influenced-by": ({"song"}, {"artist"}),
}
FIRSTHAND = {"magazine-interview", "interview", "credits", "video", "book-interview"}
SIZE_WARN_KB = 150
ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load(p):
    with open(p) as f: return json.load(f)


def validate(g, context=None, partial=False):
    """Return (errors, warnings). context supplies nodes/sources a staging file may reference."""
    errs, warns = [], []
    nodes = dict(context["nodes"]) if context else {}
    nodes.update(g.get("nodes", {}))
    sources = dict(context["sources"]) if context else {}
    sources.update(g.get("sources", {}))
    for n, d in g.get("nodes", {}).items():
        if not ID.match(n): errs.append(f"node id not kebab-case: {n}")
        k = d.get("kind")
        if k not in KINDS: errs.append(f"{n}: bad kind {k}"); continue
        if k in ("song", "album"):
            for f in ("title", "artist", "year"):
                if f not in d: errs.append(f"{n}: missing {f}")
            if not isinstance(d.get("year"), int) or not 1900 <= d.get("year", 0) <= 2030: errs.append(f"{n}: bad year")
        elif "name" not in d: errs.append(f"{n}: missing name")
        if "aliases" in d and not isinstance(d["aliases"], list): errs.append(f"{n}: aliases must be a list")
    for s, d in g.get("sources", {}).items():
        if not d.get("url", "").startswith("http"): errs.append(f"source {s}: missing url")
        if not d.get("kind"): errs.append(f"source {s}: missing kind")
    seen = set()
    for i, e in enumerate(g.get("edges", [])):
        tag = f"edge {e.get('from')}->{e.get('to')} ({e.get('type')})"
        for f in ("from", "to", "type", "grade", "scope", "sources", "checked"):
            if f not in e: errs.append(f"{tag}: missing {f}")
        if e.get("type") not in TYPES: errs.append(f"{tag}: bad type"); continue
        if e.get("grade") not in G.GRADES: errs.append(f"{tag}: bad grade")
        if e.get("scope") not in ("track", "album"): errs.append(f"{tag}: bad scope")
        if e.get("checked") and not DATE.match(e["checked"]): errs.append(f"{tag}: checked must be YYYY-MM-DD")
        a, b = nodes.get(e.get("from")), nodes.get(e.get("to"))
        if not a or not b: errs.append(f"{tag}: unknown node"); continue
        fk, tk = TYPES[e["type"]]
        if a["kind"] not in fk or b["kind"] not in tk: errs.append(f"{tag}: {a['kind']}->{b['kind']} not allowed for {e['type']}")
        if e.get("scope") == "album" and a["kind"] != "album": warns.append(f"{tag}: album scope on a non-album node")
        for s in e.get("sources", []):
            if s not in sources: errs.append(f"{tag}: unknown source {s}")
        if not e.get("sources"): errs.append(f"{tag}: no sources")
        if e.get("grade") == "documented" and not any(sources.get(s, {}).get("kind") in FIRSTHAND for s in e.get("sources", [])):
            warns.append(f"{tag}: documented, but no first-hand source kind ({', '.join(sorted(FIRSTHAND))})")
        key = (e.get("from"), e.get("to"), e.get("type"), e.get("role"), e.get("part"), e.get("version"))
        if key in seen: errs.append(f"{tag}: duplicate")
        seen.add(key)
        for dsp in e.get("disputes", []):
            if not {"claim", "grade", "sources"} <= set(dsp): errs.append(f"{tag}: dispute needs claim, grade, sources")
    if not partial:
        used = {n for e in g["edges"] for n in (e["from"], e["to"])}
        for n in g["nodes"]:
            if n not in used: warns.append(f"orphan node: {n}")
        if g.get("hub") not in g["nodes"]: errs.append("hub missing")
    return errs, warns


def print_check(errs, warns):
    for e in errs: print("ERROR  ", e)
    for w in warns: print("warning", w)
    print(f"{len(errs)} errors, {len(warns)} warnings")


def cmd_validate(args):
    p = args[0] if args else SEED
    g = load(p)
    partial = os.path.abspath(p) != os.path.abspath(SEED)
    errs, warns = validate(g, load(SEED) if partial else None, partial)
    print_check(errs, warns)
    sys.exit(1 if errs else 0)


def apply_updates(out, st, log):
    """Corrections to existing edges: {"match": {...}, "set": {...}, "add_sources": [...], "reason": "..."}."""
    for u in st.get("updates", []):
        hits = [e for e in out["edges"] if all(e.get(k) == v for k, v in u["match"].items())]
        if len(hits) != 1:
            log.append(f"UPDATE SKIPPED {u['match']}: matched {len(hits)} edges"); continue
        e = hits[0]
        before = e["grade"]
        for k, v in u.get("set", {}).items():
            if v is None: e.pop(k, None)
            else: e[k] = v
        e["sources"] = e["sources"] + [s for s in u.get("add_sources", []) if s not in e["sources"]]
        change = f"{before} -> {e['grade']}" if before != e["grade"] else "grade unchanged"
        log.append(f"update {e['from']}->{e['to']} ({e['type']}): {change}. {u.get('reason', '')}")


def merge(seed, st):
    out = json.loads(json.dumps(seed))
    log = []
    for n, d in st.get("nodes", {}).items():
        if n in out["nodes"]:
            old = out["nodes"][n]
            if {k: v for k, v in d.items() if k != "aliases"} != {k: v for k, v in old.items() if k != "aliases"}:
                log.append(f"CONFLICT node {n}: seed {old} vs staged {d} (kept seed)")
            old_al = old.get("aliases", [])
            new_al = [a for a in d.get("aliases", []) if a not in old_al]
            if new_al: old["aliases"] = old_al + new_al; log.append(f"aliases + {n}: {new_al}")
        else:
            out["nodes"][n] = d; log.append(f"node + {n}")
    for s, d in st.get("sources", {}).items():
        if s not in out["sources"]: out["sources"][s] = d; log.append(f"source + {s}")
    apply_updates(out, st, log)
    index = {(e["from"], e["to"], e["type"], e.get("role"), e.get("part"), e.get("version")): e for e in out["edges"]}
    for e in st.get("edges", []):
        k = (e["from"], e["to"], e["type"], e.get("role"), e.get("part"), e.get("version"))
        if k in index:
            old = index[k]
            old["sources"] = old["sources"] + [s for s in e["sources"] if s not in old["sources"]]
            if G.GRADES.index(e["grade"]) < G.GRADES.index(old["grade"]):
                log.append(f"upgrade {k[0]}->{k[1]}: {old['grade']} -> {e['grade']}")
                old["grade"] = e["grade"]
            old["checked"] = max(old.get("checked", ""), e.get("checked", ""))
            log.append(f"edge ~ {k[0]}->{k[1]} ({k[2]}) merged sources")
        else:
            out["edges"].append(e); index[k] = e; log.append(f"edge + {k[0]}->{k[1]} ({k[2]}, {e['grade']})")
    return out, log


def cmd_merge(args):
    if not args: sys.exit("usage: curate.py merge STAGING [--write]")
    seed, st = load(SEED), load(args[0])
    errs, warns = validate(st, seed, partial=True)
    if errs: print_check(errs, warns); sys.exit("staging file has errors; nothing merged")
    out, log = merge(seed, st)
    errs2, warns2 = validate(out)
    for line in log: print(line)
    print_check(errs2, warns2)
    if errs2: sys.exit("merged graph has errors; nothing written")
    if "--write" in args:
        with open(SEED, "w") as f: json.dump(out, f, indent=1, ensure_ascii=False)
        print(f"written: {len(out['nodes'])} nodes, {len(out['edges'])} edges")
    else:
        print("dry run: add --write to apply")


def report(g, era=None):
    adj = {n: [] for n in g["nodes"]}
    for e in g["edges"]:
        adj[e["from"]].append((e["to"], e)); adj[e["to"]].append((e["from"], e))
    strict = {n: [(m, e) for m, e in v if not G.is_influence(e)] for n, v in adj.items()}
    hub = g["hub"]
    songs = sorted(n for n, d in g["nodes"].items() if d["kind"] == "song")
    r = {}
    r["nodes"] = dict(Counter(d["kind"] for d in g["nodes"].values()))
    r["edges"] = len(g["edges"])
    gear = [e for e in g["edges"] if e["type"] == "used"]
    r["documented_share"] = round(sum(e["grade"] == "documented" for e in g["edges"]) / len(g["edges"]), 3)
    r["gear_documented_share"] = round(sum(e["grade"] == "documented" for e in gear) / max(len(gear), 1), 3)
    r["gear_track_level_share"] = round(sum(e["scope"] == "track" for e in gear) / max(len(gear), 1), 3)
    r["gear_with_part_share"] = round(sum(bool(e.get("part")) for e in gear) / max(len(gear), 1), 3)
    deg, deg_strict, through = [], [], Counter()
    islands = []
    for s in songs:
        if s == hub: continue
        ch = G.shortest(g, adj, s, hub)
        if ch is None: islands.append(s); continue
        deg.append(G.degrees(g, s, ch))
        for _, _, n in ch[:-1]: through[n] += 1
        chs = G.shortest(g, strict, s, hub)
        if chs: deg_strict.append(G.degrees(g, s, chs))
    r["songs_connected"] = f"{len(deg)}/{len(songs) - 1}"
    r["islands"] = islands
    r["median_degrees"] = statistics.median(deg) if deg else None
    r["max_degrees"] = max(deg) if deg else None
    r["median_degrees_strict"] = statistics.median(deg_strict) if deg_strict else None
    pairs = 0
    for i, a in enumerate(songs):
        for b in songs[i + 1:]:
            if a == hub or b == hub: continue
            ch = G.shortest(g, strict, a, b)
            if ch and 2 <= G.degrees(g, a, ch) <= 4: pairs += 1
    r["puzzle_pairs"] = pairs
    total = len(deg) or 1
    r["busiest_connectors"] = [(n, round(c / total, 2)) for n, c in through.most_common(6)]
    r["size_kb"] = round(len(json.dumps(g, ensure_ascii=False)) / 1024, 1)
    years = Counter(g["nodes"][s]["year"] for s in songs)
    r["songs_per_year"] = dict(sorted(years.items()))
    if era:
        lo, hi = era
        r["songs_in_era"] = f"{sum(lo <= g['nodes'][s]['year'] <= hi for s in songs)}/{len(songs)}"
    return r


def cmd_report(args):
    era = None
    if "--era" in args:
        lo, hi = args[args.index("--era") + 1].split("-"); era = (int(lo), int(hi))
    g = load(SEED)
    r = report(g, era)
    for k, v in r.items(): print(f"{k:24} {v}")
    if r["size_kb"] > SIZE_WARN_KB:
        print(f"warning: graph is {r['size_kb']} KB; too big to read into a conversation without the script")


def main():
    if len(sys.argv) < 2: print(__doc__); return
    c, args = sys.argv[1], sys.argv[2:]
    {"validate": cmd_validate, "merge": cmd_merge, "report": cmd_report}.get(c, lambda a: print(__doc__))(args)


if __name__ == "__main__":
    main()
