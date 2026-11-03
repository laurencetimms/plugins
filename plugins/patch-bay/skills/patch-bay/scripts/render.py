#!/usr/bin/env python3
"""Patch Bay visuals, drawn from the gear graph so they always match the data.

Usage:
  render.py chain FROM [TO] [--strict] [--min GRADE] [--out FILE.svg]
      A chain card: the songs as stations, the shared machine or person on each join,
      line style by grade (solid documented, dashed reported, dotted folklore).
  render.py share --date YYYY-MM-DD --par N --grades G1,G2,...
      A spoiler-free puzzle result to paste anywhere. Grades: documented|reported|folklore
      (or d|r|f), one per degree of the player's chain, in order.
  render.py map [--artifact] [--out FILE.html]
      The Map of Being Boiled: an interactive page with rings by degree. Published as an
      artifact (--artifact, with the sample/db/user capabilities) it also offers Ask the map,
      Tell the story and Suggest leads; as a plain file those features stay hidden.

No third-party packages. Options --graph and --extra work as in graph.py.
"""
import datetime, html, json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import graph as G  # noqa: E402

LAUNCH = datetime.date(2026, 11, 1)  # Patch Bay puzzle #1
REL = ("song", "album")


def esc(s):
    return html.escape(str(s), quote=True)


def clip(s, n):
    s = str(s)
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def build_adj(g, strict=False, min_grade="folklore"):
    allowed = set(G.GRADES[: G.GRADES.index(min_grade) + 1])
    adj = {n: [] for n in g["nodes"]}
    for e in g["edges"]:
        if e["grade"] not in allowed or (strict and G.is_influence(e)): continue
        if e["from"] in adj and e["to"] in adj:
            adj[e["from"]].append((e["to"], e)); adj[e["to"]].append((e["from"], e))
    return adj


def name_of(g, n):
    d = g["nodes"][n]
    return d.get("title") or d.get("name")


def stops_of(g, start, chain):
    """Collapse a raw chain into stops (releases) and joins (what links each pair of stops)."""
    stops = [{"id": start, "album": None, "switch": None}]
    joins, cur = [], {"edges": [], "via": []}
    last_rel = start
    for i, (p, e, n) in enumerate(chain):
        kind = g["nodes"][n]["kind"]
        if kind in REL and e["type"] == "on" and p == last_rel and not cur["edges"]:
            stops[-1]["album" if kind == "album" else "song_of_album"] = n  # same stop
            last_rel = n
            continue
        cur["edges"].append(e)
        if kind in REL:
            joins.append(cur); stops.append({"id": n, "album": None, "switch": None})
            cur, last_rel = {"edges": [], "via": []}, n
        else:
            cur["via"].append(n)
    for k, j in enumerate(joins):
        real = [e for e in j["edges"] if e["type"] != "on"]
        j["grade"] = max((e["grade"] for e in real), key=G.GRADES.index) if real else "documented"
        j["album_level"] = any(e.get("scope") == "album" for e in real)
        j["influence"] = any(G.is_influence(e) for e in real)
    for k in range(1, len(stops) - 1):
        a, b = joins[k - 1]["edges"][-1].get("version"), joins[k]["edges"][0].get("version")
        if a and b and a != b: stops[k]["switch"] = f"{a} → {b}"
    return stops, joins


def join_label(g, j):
    if j["via"]:
        main = " · ".join(name_of(g, v) for v in j["via"])
    else:
        e = j["edges"][0]
        main = {"drew-on": "borrowed from", "on": "same album"}.get(e["type"], e["type"])
        if e.get("role"): main += f" ({e['role']})"
    parts = [e.get("part") for e in j["edges"] if e.get("part")]
    return main, (parts[0] if parts else "")


# ---------------------------------------------------------------- chain card (SVG)

GRADE_DASH = {"documented": "", "reported": "10 7", "folklore": "2 7"}


def chain_svg(g, start, chain, title_extra=""):
    stops, joins = stops_of(g, start, chain)
    W, top, step, x = 640, 104, 132, 72
    H = top + step * (len(stops) - 1) + 96
    weakest = max((j["grade"] for j in joins), key=G.GRADES.index) if joins else "documented"
    hflags = []
    if any(j["album_level"] for j in joins): hflags.append("album-level credit")
    if any(j["influence"] for j in joins): hflags.append("cited influence")
    if any(s["switch"] for s in stops): hflags.append("switches recording")
    title_extra = title_extra + "".join("  ·  " + f for f in hflags)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'xml:space="preserve" role="img" aria-label="{esc(name_of(g, start))} to {esc(name_of(g, stops[-1]["id"]))}, {len(joins)} degrees">',
           """<style>
  .bg{fill:#f6f4ef}.ink{fill:#1d1b22}.mute{fill:#6b6774}.line{stroke:#1d1b22}.card{fill:#ffffff;stroke:#e3dfd6}
  .documented{stroke:#1f8f87}.reported{stroke:#b8860b}.folklore{stroke:#d1452b}
  .t-documented{fill:#1f8f87}.t-reported{fill:#9a7008}.t-folklore{fill:#c13d24}
  .dot{fill:#ffffff;stroke:#1d1b22}.hub{fill:#1d1b22}
  @media (prefers-color-scheme: dark){
    .bg{fill:#16151a}.ink{fill:#f2efe8}.mute{fill:#a7a2b0}.card{fill:#211f27;stroke:#34313c}
    .documented{stroke:#3fb8af}.reported{stroke:#f2c14e}.folklore{stroke:#ff5a3c}
    .t-documented{fill:#3fb8af}.t-reported{fill:#f2c14e}.t-folklore{fill:#ff7a5e}
    .dot{fill:#16151a;stroke:#f2efe8}.hub{fill:#f2efe8}}
  text{white-space:pre;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
</style>""",
           f'<rect class="bg" width="{W}" height="{H}" rx="18"/>',
           f'<text class="mute" x="32" y="40" font-size="13" letter-spacing="1.5">PATCH BAY · SIX DEGREES OF BEING BOILED</text>',
           f'<text class="ink" x="32" y="70" font-size="22" font-weight="700">{len(joins)} degree{"s" if len(joins) != 1 else ""}'
           f'<tspan class="mute" font-weight="400" font-size="15">  ·  weakest link: </tspan>'
           f'<tspan class="t-{weakest}" font-weight="600" font-size="15">{weakest}</tspan>'
           f'<tspan class="mute" font-weight="400" font-size="15">{esc(title_extra)}</tspan></text>']
    for k, j in enumerate(joins):
        y1, y2 = top + step * k, top + step * (k + 1)
        dash = GRADE_DASH[j["grade"]]
        out.append(f'<line class="{j["grade"]}" x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke-width="6" '
                   f'stroke-linecap="round"{f" stroke-dasharray={chr(34)}{dash}{chr(34)}" if dash else ""}/>')
        main, part = join_label(g, j)
        flags = [j["grade"]] + (["album-level"] if j["album_level"] else []) + (["cited influence"] if j["influence"] else [])
        ym = (y1 + y2) / 2
        out.append(f'<text class="ink" x="{x + 26}" y="{ym - 6}" font-size="14" font-weight="600">{esc(clip(main, 52))}</text>')
        sub = (clip(part, 40) + "  ·  " if part else "")
        out.append(f'<text x="{x + 26}" y="{ym + 14}" font-size="12"><tspan class="mute">{esc(sub)}</tspan>'
                   f'<tspan class="t-{j["grade"]}">{esc(", ".join(flags))}</tspan></text>')
    for k, s in enumerate(stops):
        y = top + step * k
        d = g["nodes"][s["id"]]
        is_hub = s["id"] == g["hub"]
        out.append(f'<circle class="{"hub" if is_hub else "dot"}" cx="{x}" cy="{y}" r="{12 if is_hub else 10}" stroke-width="4"/>')
        if is_hub:
            out.append(f'<circle class="bg" cx="{x}" cy="{y}" r="4"/>')
        tx = x + 26
        title = ("[album] " if d["kind"] == "album" else "") + d["title"]
        out.append(f'<text class="ink" x="{tx}" y="{y - 2 + (0 if k else 0)}" font-size="17" font-weight="700" dy="-4">{esc(clip(title, 46))}</text>')
        extra = f'{d["artist"]} · {d["year"]}'
        if s.get("album") and s.get("song_of_album"):
            extra += f' · on {name_of(g, s["album"])}, alongside {name_of(g, s["song_of_album"])}'
        elif s.get("album"): extra += f' · on {name_of(g, s["album"])}'
        elif s.get("song_of_album"): extra += f' · via {name_of(g, s["song_of_album"])}'
        out.append(f'<text class="mute" x="{tx}" y="{y + 14}" font-size="13">{esc(clip(extra, 64))}</text>')
        if s["switch"]:
            out.append(f'<text class="t-folklore" x="{tx}" y="{y + 30}" font-size="12">switches recording: {esc(clip(s["switch"], 56))}</text>')
    ly = H - 34
    lx = 32
    for gname, label in (("documented", "documented"), ("reported", "reported"), ("folklore", "folklore")):
        dash = GRADE_DASH[gname]
        out.append(f'<line class="{gname}" x1="{lx}" y1="{ly}" x2="{lx + 34}" y2="{ly}" stroke-width="5" stroke-linecap="round"'
                   f'{f" stroke-dasharray={chr(34)}{dash}{chr(34)}" if dash else ""}/>')
        out.append(f'<text class="mute" x="{lx + 42}" y="{ly + 4}" font-size="12">{label}</text>')
        lx += 140
    out.append("</svg>")
    return "\n".join(out)


def cmd_chain(g, adj, args):
    out_path = None
    if "--out" in args:
        out_path = args[args.index("--out") + 1]; args = [a for a in args if a not in ("--out", out_path)]
    a = G.resolve(g, args[0]); b = G.resolve(g, args[1]) if len(args) > 1 else g["hub"]
    chain = G.shortest(g, adj, a, b)
    if chain is None:
        sys.exit(f"No chain from {a} to {b}; nothing to draw.")
    extra = "  ·  strict" if G.STRICT else ""
    svg = chain_svg(g, a, chain, extra)
    out_path = out_path or f"chain-{a}.svg"
    with open(out_path, "w") as f: f.write(svg)
    print(out_path)


# ---------------------------------------------------------------- share grid

SQUARE = {"documented": "🟩", "reported": "🟨", "folklore": "🟧"}
SHORT = {"d": "documented", "r": "reported", "f": "folklore"}


def cmd_share(g, adj, args):
    def opt(k, default=None):
        return args[args.index(k) + 1] if k in args else default
    day = datetime.date.fromisoformat(opt("--date", datetime.date.today().isoformat()))
    par = int(opt("--par"))
    grades = [SHORT.get(x.strip().lower(), x.strip().lower()) for x in opt("--grades").split(",") if x.strip()]
    bad = [x for x in grades if x not in SQUARE]
    if bad: sys.exit(f"unknown grades: {bad}")
    n = (day - LAUNCH).days + 1
    score = len(grades)
    verdict = "under par" if score < par else ("par" if score == par else "over par")
    clean = all(x == "documented" for x in grades)
    print(f"Patch Bay #{n} · {score}/{par} ({verdict}){' · fully documented' if clean else ''}")
    print("".join(SQUARE[x] for x in grades))
    print("🟩 documented 🟨 reported 🟧 folklore")
    print("Six Degrees of Being Boiled")


# ---------------------------------------------------------------- map (HTML)

def map_data(g):
    modes = {"loose": (False, "folklore"), "strict": (True, "folklore"),
             "documented": (False, "documented"), "strict-documented": (True, "documented")}
    rels = sorted(n for n, d in g["nodes"].items() if d["kind"] in REL and n != g["hub"])
    data = {m: {} for m in modes}
    for m, (strict, mn) in modes.items():
        adj = build_adj(g, strict, mn)
        for r in rels:
            ch = G.shortest(g, adj, r, g["hub"], no_switch=strict)
            if ch is None: continue
            stops, joins = stops_of(g, r, ch)
            # albums reached only through one of their songs are drawn at the song's place
            data[m][r] = {
                "deg": len(joins),
                "stops": [s["id"] for s in stops],
                "joins": [{
                    "grade": j["grade"], "album": j["album_level"], "influence": j["influence"],
                    "via": [name_of(g, v) for v in j["via"]],
                    "label": join_label(g, j)[0], "part": join_label(g, j)[1],
                    "notes": [e["note"] for e in j["edges"] if e.get("note") and e["type"] != "on"][:2],
                    "sources": sorted({g["sources"][s]["url"] for e in j["edges"] for s in e["sources"] if s in g["sources"]}),
                } for j in joins],
                "switch": [s["switch"] for s in stops if s["switch"]],
            }
    # Angles: group releases by the connector they reach Being Boiled through, so branches form sectors.
    def branch(r):
        c = data["loose"].get(r)
        if not c: return ("~", r)
        last = c["joins"][-1]
        return (last["label"], -c["deg"], g["nodes"][r].get("year", 0), r)
    order = sorted(rels, key=branch)
    angle = {r: i / len(order) * 360 for i, r in enumerate(order)}
    nodes = {r: {"t": g["nodes"][r]["title"], "a": g["nodes"][r]["artist"], "y": g["nodes"][r]["year"],
                 "k": g["nodes"][r]["kind"], "ang": round(angle[r], 2)} for r in rels}
    hub = g["nodes"][g["hub"]]
    return {"hub": {"id": g["hub"], "t": hub["title"], "a": hub["artist"], "y": hub["year"]},
            "nodes": nodes, "modes": data, "version": g.get("version", ""), "built": g.get("built", "")}


SKELETON = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>{}</body></html>')


def graph_payload(g):
    """The graph the live map's lookups run over: nodes, edges and source URLs, without curation fields."""
    keep = ("from", "to", "type", "grade", "scope", "role", "part", "version", "note")
    return {"hub": g["hub"], "nodes": g["nodes"],
            "edges": [{k: e[k] for k in keep if k in e} for e in g["edges"]],
            "sources": {k: v["url"] for k, v in g["sources"].items()}}


def cmd_map(g, adj, args):
    """--artifact writes the publish-ready fragment (no doctype/head/body, which the Artifact tool adds)."""
    artifact = "--artifact" in args
    out_path = args[args.index("--out") + 1] if "--out" in args else "map-of-being-boiled.html"
    js = lambda obj: json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "map-template.html")) as f: tpl = f.read()
    page = tpl.replace("__DATA__", js(map_data(g))).replace("__GRAPH__", js(graph_payload(g)))
    with open(out_path, "w") as f: f.write(page if artifact else SKELETON.format(page))
    print(out_path)


def main():
    g, adj, rest, mn = G.load(sys.argv[1:])
    if not rest: print(__doc__); return
    c, args = rest[0], rest[1:]
    # re-attach options that G.load treats as positional
    raw = sys.argv[2:]
    for k in ("--out", "--date", "--par", "--grades"):
        if k in raw:
            v = raw[raw.index(k) + 1]
            args = [a for a in args if a not in (k, v)] + [k, v]
    {"chain": cmd_chain, "share": cmd_share, "map": cmd_map}.get(c, lambda *a: print(__doc__))(g, adj, args)


if __name__ == "__main__":
    main()
