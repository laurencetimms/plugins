# Visuals

All pictures come from `scripts/render.py`, which draws from the gear graph. Never draw a chain or map by hand: the script guarantees the picture matches the data and the grades.

## Chain card

`python3 scripts/render.py chain FROM [TO] [--strict] [--min documented] [--extra FINDS] [--out FILE.svg]`

An SVG "line diagram": songs as stations, the shared machine or person labelled on each join, with the part where known. The line style carries the grade (solid documented, dashed reported, dotted folklore) and each join also says its grade in words. Album-level credits, cited influences and recording switches are flagged in the header and on the join. It adapts to light and dark mode.

Render it with the same options as the chain you presented, so picture and text agree. Show it after the text ladder, not instead of it: the ladder carries the sources.

## Puzzle result

`python3 scripts/render.py share --date YYYY-MM-DD --par N --grades d,r,d`

Prints a spoiler-free result: puzzle number (#1 is 1 November 2026), degrees against par, and one coloured square per degree with a legend. Paste it in a code block.

## The Map of Being Boiled

`python3 scripts/render.py map [--artifact] [--out FILE.html]`

An interactive page built from `scripts/map-template.html`. Being Boiled at the centre, rings for each degree, every record in the graph placed on its ring and grouped by the link it reaches Being Boiled through. Albums are dashed circles; records with no chain sit on the outer dashed ring. Choosing a record lights its chain and shows each step with grades, notes and source links. Two switches, strict and documented-only, move records outward as weaker links drop away. It works at phone width and in light and dark mode.

The map shows the seed graph only, not this session's finds.

### The live map

Published as an artifact, the map gains three features that use the viewer's own Claude:

- **Ask the map**: questions answered by Claude calling the page's own lookups over the graph (search, describe, find a chain, busiest connectors, show on map). It is told to use nothing from memory.
- **Tell the story**: a short narrative of the selected chain, written only from the graph's notes.
- **Suggest leads**: for any record, especially islands, up to three hunches from Claude's memory, clearly labelled as unchecked. The viewer can save them to the page's **lead queue**, which you check in chat (see `references/leads.md`).

To publish it:

1. `python3 scripts/render.py map --artifact --out map-of-being-boiled.html` (the fragment form; the Artifact tool adds the document skeleton).
2. Publish that file with the Artifact tool, icon `map`, and `capabilities: {"sample": {}, "db": {}, "user": {}}`.
3. On a later update, republish to the same artifact (same file path in this session, or its `url` from another) and omit `capabilities` so the stored declaration carries over. The lead queue survives republishes.

Before publishing in a new session, check whether the user already has a Map of Being Boiled (`Artifact` list) and update that one rather than making a second, so their lead queue stays in one place.

As a plain file (no `--artifact`), the Claude features stay hidden and the static map is the whole page.

## Showing the output

Use whatever this session offers, in this order:

1. **The Claude app with artifacts:** publish the map as a page the user can keep and share. Show a chain card inline as an image or file preview.
2. **Any session that can send or preview files:** send the SVG or HTML file.
3. **Neither:** say where the file was written and give the chain as text.

Keep the file names readable: `chain-relax.svg`, `map-of-being-boiled.html`.
