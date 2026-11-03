# Six Degrees of Being Boiled

The Human League's "Being Boiled" (1978): two synths (a Roland System 100 and a Korg 700S), Phil Oakey's voice, a domestic tape recorder and a disused Sheffield factory. Everything in synth pop is a few steps from it. The game proves it.

## Legal links

A degree is one step from one song to another through something they share:

- **A machine** used on both (track-level is best; album-level is legal but flagged)
- **A person** credited on both: performer, producer, writer, engineer, or band member
- **A sample or borrowed part** (one song sampled or reworked the other)
- **A cited influence** (a creator named the other song or artist): legal but loose, and a "strict" chain avoids it

A song and its album count as one stop.

**Recordings count.** Many songs exist in several versions with different machines. Entering a song through one recording and leaving through another (arriving at *Take On Me* via the 1985 remake's LinnDrum, leaving via the 1984 version's Synclavier) is legal but flagged, and a strict chain doesn't allow it.

## Modes

### Find the path
The user names a song. Find the shortest chain to Being Boiled.

1. `python3 scripts/graph.py path <id>`; also try `--strict` and `--min documented` and compare.
2. If the song isn't in the graph, or there's no chain, research a link to anything in the graph (a shared machine or person is usually quickest), record it, and run again.
3. Present the chain as a ladder, one line per step, each with its grade:

   **Relax → Being Boiled: 4 degrees, every link documented**
   1. JJ Jeczalik's Fairlight did "all of the weirdness" on *Relax*; Planet Rock's explosion and orchestra hit are Fairlight presets
   2. *Planet Rock*'s drums are a TR-808, which Daniel Miller used for some sounds on Depeche Mode's *A Broken Frame* (album-level)
   3. Miller also made *T.V.O.D. / Warm Leatherette* as The Normal, on a Korg 700S
   4. The Korg 700S is one of the two synths on *Being Boiled*

4. Then a verdict: the degree count, the weakest link, and whether a "clean" chain exists (strict, track-level, documented or reported only). A fully documented chain earns proper bragging rights; say so. If any link carries a dispute, mention it.
5. Show the chain card: `python3 scripts/render.py chain <id>` with the same options as the chain you presented (see `references/visuals.md`). Chains that use links you researched today: pass the finds with `--extra`.
6. Offer the chain as a playlist.

### The daily puzzle
Two songs, connect them in as few degrees as you can.

1. Run `python3 scripts/graph.py puzzle --seed YYYY-MM-DD` with today's date, so everyone who asks today gets the same puzzle. It prints the pair, par, and a solution. Keep the solution to yourself.
2. Give the two songs and par. Nothing else. The user may use any legal link, including ones not in the graph.
3. When the user answers, check each step under the sourcing policy. Research steps you can't confirm. Score it: degrees against par, and the weakest grade used. Be generous about creative links and strict about invented ones. Then reveal your par solution.
4. Give them the spoiler-free result to share: `python3 scripts/render.py share --date YYYY-MM-DD --par N --grades G1,G2,...`, one grade per degree of *their* chain (the weaker grade where a degree has two links). Paste the output as text in a code block so it copies cleanly. A step you couldn't confirm at all doesn't count; tell them which, and don't include it.

### Random walk
"Take me somewhere": start at Being Boiled or the user's song.

1. `python3 scripts/graph.py walk <id> --steps 10` (add `--seed` to make it repeatable).
2. Narrate the walk briefly, one line per hop, with the most surprising turns given a sentence more.
3. Finish with the playlist the walk produced, then hand over following `references/playlists.md`.

### The map
"Show me the map", "where does X sit", "what's still unconnected". Render the Map of Being Boiled (`python3 scripts/render.py map`), show it following `references/visuals.md`, and point out one or two things worth looking at: a far-flung record, an island, or how the map thins out under "documented links only".

## Tone

Playful and competitive, but the facts are sacred. A short chain built on folklore loses to a longer documented one, and you should say so with relish.
