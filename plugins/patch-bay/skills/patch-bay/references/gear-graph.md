# The gear graph

The seed focuses on British synth pop, 1978–1986. Records from outside that focus (Donna Summer, Kraftwerk, Prince, Planet Rock) are kept where they connect the graph.

## Shape

`data/seed-graph.json`:

- `hub`: `being-boiled`, the centre of Six Degrees.
- `nodes`: id → node. Kinds:
  - `song` and `album`: `title`, `artist`, `year`
  - `machine`: `name`
  - `artist`: `name` (a person or a band)
  - any node may have `aliases` (other names people use: "TR-808", "808")
- `edges`: each has `from`, `to`, `type`, `grade`, `scope` (`track` or `album`), `sources` (ids) and `checked` (the date it was last checked against its sources). Optional:
  - `role`: for credits, what the person did
  - `part`: what the machine played ("bassline", "the three plucked chorus chords")
  - `version`: which recording ("1978 original", "1985 Alan Tarney remake", "12-inch US Remix")
  - `note`: the story, in a sentence or two
  - `disputes`: other claims about the same link, each with `claim`, `grade` and `sources`. Show these to the user; disagreement is interesting.
- `sources`: id → `title`, `url`, `kind`, `accessed`. Kinds that count as first-hand: `magazine-interview`, `interview`, `credits`, `video`, `book-interview`.

Edge types:

| Type | From → to | Meaning |
| --- | --- | --- |
| `used` | song or album → machine | The machine is on the recording (album-level if scope is `album`). |
| `credit` | song or album → artist | Performer, producer, writer or engineer; `role` says which. |
| `member` | person → band | Membership. |
| `on` | song → album | The song is on the album. Costs nothing in Six Degrees. |
| `drew-on` | song → song | `role` says how: `sample`, `beat`, `melody`, or `cited influence`. |
| `influenced-by` | song → artist | A creator named this artist as an influence. |

Cited influences are the loosest links: someone said it, but nothing is shared on the record itself.

## Querying: `scripts/graph.py`

Run from this skill's directory: `python3 scripts/graph.py <command>`.

| Command | Use |
| --- | --- |
| `find TEXT` | Find node ids by name, title or alias. |
| `show NODE` | Everything linked to a node, with grades, parts, versions, notes and sources. |
| `machine NODE` | Songs a machine is linked to, with album credits expanded and flagged. |
| `path FROM [TO]` | Shortest chain; `TO` defaults to Being Boiled. Prints degrees, the weakest grade, and flags. |
| `walk START --steps N --seed S` | Random wander that backs up at dead ends, ending in a playlist. |
| `puzzle --seed S` | A song pair 2–4 strict degrees apart, with par and a solution. Same seed, same puzzle. |
| `stats` | Quick counts. |

Options:
- `--min documented|reported` drops weaker links.
- `--strict` drops cited influences and stops a chain entering a song through one recording and leaving through another (e.g. arriving at *Take On Me* via the 1985 LinnDrum and leaving via the 1984 Synclavier version). Without `--strict`, such switches are allowed but flagged.
- `--extra FILE` adds links found this session.

A **degree** is one song-to-song step through a shared machine, person or sample. A song and its album count as one stop.

## Drawing: `scripts/render.py`

Chain cards, the shareable puzzle result and the Map of Being Boiled. See `references/visuals.md`.

## Curating: `scripts/curate.py`

| Command | Use |
| --- | --- |
| `validate [FILE]` | Check the seed, or a staging file against the seed: required fields, allowed link types, known sources, duplicates, orphans, and a warning when a link marked documented has no first-hand source. |
| `merge FILE [--write]` | Merge a staging file. Dry run by default; prints every addition, upgrade and conflict. |
| `report [--era 1978-1986]` | Health metrics (below). |

A staging file has the seed's shape (`nodes`, `edges`, `sources`) and may add `updates`, which correct existing links: `{"match": {...}, "set": {...}, "add_sources": [...], "reason": "..."}`. Each match must hit exactly one link.

The report tracks:
- islands, and how many songs connect to Being Boiled
- share of links documented; share of gear links that are documented, track-level, and name a part
- median degrees to Being Boiled, loose and strict
- puzzle pairs available
- busiest connectors: the share of chains running through each node. If one node carries most chains, the game gets samey; add routes around it.
- size; above about 150 KB the graph is too big to read into a conversation without the script

## Session finds

When research turns up a link worth keeping for the session, write it to `patch-bay-finds.json` in staging format, check it with `python3 scripts/curate.py validate patch-bay-finds.json`, and pass it to `graph.py` with `--extra`. Never write to the seed during play; offer the finds file to the user, who can send it to the plugin's maintainer.

## Islands and where to look

Islands are invitations. When the user asks about something not connected, research a link under the sourcing policy, add it to the finds, and try again.

Sources that hold up best, in order:
1. Sound On Sound "Classic Tracks" and other interview-led studio features
2. Interviews from the time, such as the mu:zines archive of 80s music-tech magazines
3. Sleeve credits (Discogs credits, not user comments)
4. Wikipedia, then follow its citations upward
