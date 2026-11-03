#!/usr/bin/env python3
"""Patch Bay gear graph tool.

Usage:
  graph.py find TEXT                      find node ids matching TEXT
  graph.py show NODE                      a node and everything linked to it
  graph.py machine NODE                   songs linked to a machine (album credits expanded)
  graph.py path FROM [TO] [--min GRADE]   shortest chain (TO defaults to the hub, Being Boiled)
  graph.py walk START [--steps N] [--seed S] [--min GRADE]   random walk -> playlist
  graph.py puzzle [--seed S]              a song pair 2-4 degrees apart, with par and a hidden solution
  graph.py stats

Options:
  --graph PATH    seed graph (default: ../data/seed-graph.json next to this script)
  --extra PATH    extra edges/nodes found this session (same JSON shape); repeatable
  --min GRADE     ignore edges weaker than GRADE: documented | reported | folklore (default folklore)
  --strict        ignore cited-influence links, and don't let a chain enter a song through one recording
                  and leave through another (only shared machines, people, samples and albums count)

Edges are walked in both directions. "on" edges (song -> its album) cost nothing,
so album-level credits connect a song without spending a hop; they are flagged.
"""
import heapq, json, os, random, sys

GRADES = ["documented", "reported", "folklore"]
PENALTY = {"documented": 0.0, "reported": 0.01, "folklore": 0.2}
STRICT = False  # set by --strict: no cited influences, no switching recordings mid-song


def load(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "data", "seed-graph.json")
    extras, rest, mn, strict = [], [], "folklore", False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--graph": path = argv[i + 1]; i += 2
        elif a == "--extra": extras.append(argv[i + 1]); i += 2
        elif a == "--min": mn = argv[i + 1]; i += 2
        elif a == "--strict": strict = True; i += 1
        else: rest.append(a); i += 1
    global STRICT
    STRICT = strict
    g = json.load(open(path))
    for p in extras:
        x = json.load(open(p))
        g["nodes"].update(x.get("nodes", {}))
        g["edges"].extend(x.get("edges", []))
        g["sources"].update(x.get("sources", {}))
    if mn not in GRADES: sys.exit(f"--min must be one of {GRADES}")
    allowed = set(GRADES[: GRADES.index(mn) + 1])
    adj = {n: [] for n in g["nodes"]}
    for e in g["edges"]:
        if e["grade"] not in allowed: continue
        if strict and is_influence(e): continue
        if e["from"] not in adj or e["to"] not in adj:
            print(f"warning: edge to unknown node skipped: {e['from']} -> {e['to']}", file=sys.stderr); continue
        adj[e["from"]].append((e["to"], e))
        adj[e["to"]].append((e["from"], e))
    return g, adj, rest, mn


def label(g, n):
    d = g["nodes"][n]
    if d["kind"] in ("song", "album"):
        return f'{"[album] " if d["kind"] == "album" else ""}{d["artist"]} - {d["title"]} ({d["year"]})'
    return f'[{d["kind"]}] {d["name"]}'


def edge_text(g, e):
    t = e["type"] + (f' ({e["role"]})' if e.get("role") else "") + (f' - {e["part"]}' if e.get("part") else "") + \
        (f' [{e["version"]}]' if e.get("version") else "")
    flags = [e["grade"]] + (["album-level"] if e.get("scope") == "album" else [])
    src = "; ".join(g["sources"][s]["url"] for s in e["sources"] if s in g["sources"])
    return f'{t} [{", ".join(flags)}]' + (f' - {e["note"]}' if e.get("note") else "") + (f"\n      source: {src}" if src else "")


def resolve(g, text):
    if text in g["nodes"]: return text
    t = text.lower()
    hits = [n for n, d in g["nodes"].items() if t in n or t in (d.get("title") or d.get("name") or "").lower()
            or any(t == a.lower() for a in d.get("aliases", []))]
    exact = [n for n in hits if any(t == a.lower() for a in g["nodes"][n].get("aliases", []))]
    if len(exact) == 1: return exact[0]
    if len(hits) == 1: return hits[0]
    sys.exit(f"'{text}' matched {len(hits)} nodes: {', '.join(hits) or 'none'}. Use an exact id (try: find).")


def cmd_find(g, adj, args):
    t = " ".join(args).lower()
    for n, d in g["nodes"].items():
        name = " ".join([d.get("title") or d.get("name") or "", d.get("artist", "")] + d.get("aliases", []))
        if t in n or t in name.lower(): print(f"{n:32} {label(g, n)}")


def cmd_show(g, adj, args):
    n = resolve(g, args[0]); print(label(g, n))
    for m, e in sorted(adj[n], key=lambda x: GRADES.index(x[1]["grade"])):
        print(f"  -> {label(g, m)}\n     {edge_text(g, e)}")


def cmd_machine(g, adj, args):
    n = resolve(g, args[0]); print(label(g, n))
    for m, e in adj[n]:
        d = g["nodes"][m]
        if d["kind"] == "song":
            print(f"  {label(g, m)}  [{e['grade']}]")
        elif d["kind"] == "album":
            for s, e2 in adj[m]:
                if e2["type"] == "on" and g["nodes"][s]["kind"] == "song":
                    print(f"  {label(g, s)}  [{e['grade']}, album-level: credited on {d['title']}, track not confirmed]")


def is_influence(e):
    return e["type"] == "influenced-by" or (e["type"] == "drew-on" and "influence" in e.get("role", ""))


def weight(e):
    # A degree is one song-to-song step through a shared machine or person (two edges),
    # so each edge costs half a degree. Album membership is free. A cited influence is a
    # looser link than a shared machine, sample or credit, so it costs a full degree.
    base = 0.0 if e["type"] == "on" else (1.0 if is_influence(e) else 0.5)
    return base + PENALTY[e["grade"]] + (0.05 if e.get("scope") == "album" else 0)


def degrees(g, a, chain):
    """Count song-to-song steps: releases on the chain, with a song and its album counted once."""
    rel = lambda n: g["nodes"][n]["kind"] in ("song", "album")
    count, prev_rel = (1 if rel(a) else 0), a if rel(a) else None
    for p, e, n in chain:
        if rel(n):
            if not (e["type"] == "on" and prev_rel == p): count += 1
            prev_rel = n
    return max(count - 1, 0)


def version_switches(g, chain):
    """Songs the chain enters through one recording and leaves through another."""
    out = []
    for (_, e1, n), (_, e2, _) in zip(chain, chain[1:]):
        if g["nodes"][n]["kind"] == "song" and e1.get("version") and e2.get("version") and e1["version"] != e2["version"]:
            out.append(f'{g["nodes"][n]["title"]} ({e1["version"]} -> {e2["version"]})')
    return out


def shortest(g, adj, a, b, no_switch=None):
    """Dijkstra over (node, recording) states, so strict mode can forbid version switches."""
    no_switch = STRICT if no_switch is None else no_switch
    start = (a, None)
    dist, prev, pq, n_id = {start: 0.0}, {}, [(0.0, 0, start)], 1
    end = None
    while pq:
        d, _, st = heapq.heappop(pq)
        n, ver = st
        if n == b: end = st; break
        if d > dist.get(st, 1e9): continue
        for m, e in adj[n]:
            ev = e.get("version")
            if no_switch and ver and ev and ev != ver: continue
            nst = (m, ev if g["nodes"][m]["kind"] == "song" else None)
            w = d + weight(e)
            if w < dist.get(nst, 1e9):
                dist[nst] = w; prev[nst] = (st, e); heapq.heappush(pq, (w, n_id, nst)); n_id += 1
    if end is None: return None
    chain, st = [], end
    while st != start: pst, e = prev[st]; chain.append((pst[0], e, st[0])); st = pst
    return list(reversed(chain))


def cmd_path(g, adj, args, mn):
    a = resolve(g, args[0]); b = resolve(g, args[1]) if len(args) > 1 else g["hub"]
    chain = shortest(g, adj, a, b)
    if chain is None:
        print(f"No chain from {a} to {b} in the graph (min grade: {mn}). Research a new link or relax --min."); return
    weakest = max((e["grade"] for _, e, _ in chain), key=GRADES.index)
    flags = []
    if any(e.get("scope") == "album" for _, e, _ in chain): flags.append("includes an album-level credit")
    if any(is_influence(e) for _, e, _ in chain): flags.append("includes a cited influence (a looser link)")
    sw = version_switches(g, chain)
    if sw: flags.append("switches recordings at " + ", ".join(sw))
    print(f"{degrees(g, a, chain)} degrees ({len([1 for _, e, _ in chain if e['type'] != 'on'])} links). "
          f"Weakest link: {weakest}." + (f" Note: {'; '.join(flags)}." if flags else ""))
    print(label(g, a))
    for _, e, n in chain:
        print(f"  --{edge_text(g, e)}\n{label(g, n)}")


def cmd_walk(g, adj, args):
    start = resolve(g, args[0]); steps, seed = 12, None
    if "--steps" in args: steps = int(args[args.index("--steps") + 1])
    if "--seed" in args: seed = args[args.index("--seed") + 1]
    rng = random.Random(seed)
    # Random depth-first wander: at a dead end, back up and try another branch.
    seen, stack, playlist, log = {start}, [start], [], []
    if g["nodes"][start]["kind"] == "song": playlist.append(start)
    while stack and len(playlist) < steps:
        n = stack[-1]
        opts = [(m, e) for m, e in adj[n] if m not in seen]
        if not opts: stack.pop(); continue
        m, e = rng.choice(opts); seen.add(m); stack.append(m); log.append((n, e, m))
        if g["nodes"][m]["kind"] == "song": playlist.append(m)
    print("Walk (each line hangs off the node it was reached from):"); print(label(g, start))
    for p, e, m in log: print(f"  {label(g, p)}\n    --{e['type']} [{e['grade']}]--> {label(g, m)}")
    print("\nPlaylist:")
    for i, s in enumerate(playlist, 1): print(f"{i:2}. {g['nodes'][s]['artist']} - {g['nodes'][s]['title']}")


def cmd_puzzle(g, adj, args):
    """Pick a song pair 2-4 degrees apart (strict links only). Same seed -> same puzzle."""
    seed = args[args.index("--seed") + 1] if "--seed" in args else None
    rng = random.Random(seed)
    strict = {n: [(m, e) for m, e in v if not is_influence(e)] for n, v in adj.items()}
    songs = sorted(n for n, d in g["nodes"].items() if d["kind"] == "song" and n != g["hub"])
    pairs = []
    for i, a in enumerate(songs):
        for b in songs[i + 1:]:
            ch = shortest(g, strict, a, b)
            if ch and 2 <= degrees(g, a, ch) <= 4: pairs.append((a, b, ch))
    if not pairs: print("No suitable pair in the graph."); return
    a, b, ch = rng.choice(pairs)
    print(f"PUZZLE: {label(g, a)}  ->  {label(g, b)}")
    print(f"PAR: {degrees(g, a, ch)} degrees")
    print("SOLUTION (do not show the user until they have answered):")
    print(label(g, a))
    for _, e, n in ch: print(f"  --{edge_text(g, e)}\n{label(g, n)}")


def cmd_stats(g, adj, args):
    from collections import Counter
    print(Counter(d["kind"] for d in g["nodes"].values()))
    print(Counter(e["grade"] for e in g["edges"]))
    print(Counter(e["type"] for e in g["edges"]))
    songs = [n for n, d in g["nodes"].items() if d["kind"] == "song"]
    reach = [s for s in songs if shortest(g, adj, s, g["hub"]) is not None]
    print(f"{len(reach)}/{len(songs)} songs connect to the hub")


def main():
    g, adj, rest, mn = load(sys.argv[1:])
    if not rest: print(__doc__); return
    c, args = rest[0], rest[1:]
    cmds = {"find": cmd_find, "show": cmd_show, "machine": cmd_machine, "walk": cmd_walk, "stats": cmd_stats, "puzzle": cmd_puzzle}
    if c == "path": cmd_path(g, adj, args, mn)
    elif c in cmds: cmds[c](g, adj, args)
    else: print(__doc__)


if __name__ == "__main__":
    main()
