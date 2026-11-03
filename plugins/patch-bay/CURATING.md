# Curating the gear graph

For whoever maintains `skills/patch-bay/data/seed-graph.json`. The skill never writes to the seed during play; changes come through staging files and the curation tool.

## Scope

British synth pop, 1978–1986. Records outside that focus are welcome when they connect the graph (a shared producer, machine or sample), but harvest effort goes to the focus first.

## The loop

1. **Pick a batch.** Ten or so records, chosen to fix what the last report showed: islands, a connector carrying too many chains, thin years.
2. **Read the best source for each.** Interview-led studio pieces first (Sound On Sound "Classic Tracks" and "People"), then interviews from the time (mu:zines), then sleeve credits, then Wikipedia and its citations.
3. **Stage it.** Write a staging file: new `nodes`, `edges` and `sources`, plus `updates` for corrections to existing links. Grade each link by who said it, not where you read it: the interviewee's own words are documented; the author's narration is reported. Name the part and the recording wherever the source does. Record conflicting claims under `disputes`.
4. **Check it.** `python3 skills/patch-bay/scripts/curate.py validate STAGING.json`
5. **Dry run.** `python3 skills/patch-bay/scripts/curate.py merge STAGING.json`, and read every line of the log: additions, upgrades, conflicts.
6. **Spot-check.** Open the source for every link marked documented, and a sample of the rest.
7. **Merge.** Add `--write`.
8. **Measure.** `python3 skills/patch-bay/scripts/curate.py report --era 1978-1986`, and compare with the last report.
9. **Bump the version** in `.claude-plugin/plugin.json` and the counts in `README.md`.

## Player finds and map leads

Leads saved on the live map are checked in chat (`references/leads.md`); confirmed ones land in a finds file like any other player find.

## Player finds (files)

Players' sessions can produce a `patch-bay-finds.json` in staging format. Treat it like any other staging file: validate, dry run, and check every source yourself before merging. A find is a lead, not a fact.

## Rules of thumb

- A shorter chain built on folklore is worse than no chain.
- Never upgrade an album credit to a track credit, or carry a credit from one recording to another.
- "A Korg" is not a model. Record what the source says.
- Keep notes short. The graph should stay under about 150 KB so it can be read without the script.

## Harvest log

| Version | Date | Batch | Songs | Links | Documented | Islands |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1.0 | 2026-11-01 | First seed (Wikipedia, SOS) | 26 | 96 | 10% | 3 |
| 0.2.0 | 2026-11-01 | SOS Classic Tracks (12 records) and SOS interviews (Miller, Clarke, Numan, Foxx, Ware, McCluskey) | 39 | 241 | 50% | 2 |
| 0.3.0 | 2026-11-01 | No new data; added chain cards, puzzle results and the Map of Being Boiled | 39 | 241 | 50% | 2 |
| 0.4.0 | 2026-11-02 | No new data; the map went live (Ask the map, Tell the story, Suggest leads, lead queue checked in chat) | 39 | 241 | 50% | 2 |
