# Sourcing policy

Gear attributions in pop music are full of confident repetition. A forum post becomes a gear site entry, then a listicle, then "common knowledge". This policy keeps Patch Bay honest and makes the honesty part of the fun.

## The three grades

Every link between a song (or album) and a machine, person or other song gets one grade.

| Grade | Means | Typical sources |
| --- | --- | --- |
| **Documented** | First-hand and specific. Someone who was there says it, or a credit names it. | Interviews with the artist, producer or engineer that name the machine and the part (e.g. Sound On Sound "Classic Tracks"); sleeve or session credits; the musician demonstrating the part on the original machine. |
| **Reported** | A reputable secondary source states it, ideally citing someone first-hand. | Wikipedia (when it cites), music-tech magazines without a direct quote, books, the manufacturer's own articles (note the interest). |
| **Folklore** | Widely claimed, but no source above stands behind it. | Gear databases built from user submissions, forums, YouTube "how to get this sound" videos, preset names. |

Folklore isn't banned. Present it as folklore: "widely said to be…, but I can't find anyone who was there saying so."

## Scope

- **Track-level:** the source ties the machine to this recording.
- **Album-level:** the machine is credited on the album but not tied to a track. Say "credited on the album; not confirmed on this track". Never upgrade an album credit to a track credit.
- Name the **part** when the source does: the bassline, the drums, the string pad.

## Rules

1. **Open the page.** A search snippet is not a source. Grade only what the opened page says.
2. **Follow citations upward.** If Wikipedia cites an interview, open the interview if you can and grade from it.
3. **Corroboration doesn't upgrade folklore.** Ten sites repeating each other are one claim. Look for an origin.
4. **Conflicts are interesting.** If sources disagree, show both with their grades. Don't pick silently.
5. **Note bias.** A manufacturer's article about its own instrument is reported, not documented, unless it quotes someone first-hand specifically.
6. **Same model, specific model.** "A Korg" or "a Roland drum machine" is not a model. Record what is said; don't fill in the model from memory.
7. **The seed can be wrong.** If you find a better source that contradicts the seed graph, say so and prefer the better source.

## Versions and disputes

- Record which recording a claim is about. A demo, the single, the album cut, a 12-inch remix and a later remake can use different machines. Never carry a credit from one version to another.
- When good sources disagree, keep the better-supported claim as the link and record the other under `disputes`, with its own grade and sources. Tell the user about both.

## Recording what you find

When research turns up a new link worth keeping for the rest of the session, write it to `patch-bay-finds.json` in the working directory in staging format (see "Session finds" in `references/gear-graph.md`), validate it, and pass it to the script with `--extra patch-bay-finds.json`. Tell the user what you added and at what grade. If the user wants finds kept for good, offer them the file to send to the plugin's maintainer.

## Showing grades to the user

Use the grade word in plain text after the claim, e.g. "TR-808 for the drums (documented)". Keep it light. One line on what the grade rests on is enough unless they ask.
