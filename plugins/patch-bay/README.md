# Patch Bay

A synth-nerd companion for 70s and 80s electronic pop.

## What it does

**This Week in the Charts.** Give it a date ("this week in 1983", "the charts on 2 November 1984") and get the UK top 10, the story of the week, the electronic records worth noticing, and a playlist: the hits, the good stuff lower down, and records from the same months that shared the sound.

**Synth Forensics.** "What made the Blue Monday bassline?" "What else used a Jupiter-8?" Part-by-part answers, each graded:

- **documented**: someone who was there said it, or a credit names it
- **reported**: a reputable source says it
- **folklore**: widely claimed, nobody stands behind it

Album credits are never passed off as track credits, and "not known" is an acceptable answer.

**Six Degrees of Being Boiled.** Connect any song to the Human League's 1978 debut through shared machines, people and samples.

- *Find the path*: the shortest chain from your song, with the weakest link called out
- *Daily puzzle*: two songs and a par, the same for everyone that day
- *Random walk*: a wander through the graph that ends as a playlist

A short chain built on folklore loses to a longer documented one.

## Visuals

- **Chain cards.** Every Six Degrees answer comes with a line diagram of the chain: songs as stations, the shared machine or person on each join, and the line style showing how well each link is sourced.
- **A shareable puzzle result.** A spoiler-free grid of coloured squares, one per degree, to paste anywhere.
- **The Map of Being Boiled.** An interactive page with Being Boiled at the centre and every record on a ring by its distance. Tap a record to light up its chain, and switch to strict or documented-only to watch the weaker links fall away. Published as a Claude artifact, it comes alive: ask the map questions (answered from the graph, not from memory), have Claude tell the story of a chain, or ask for leads on an unconnected record and save them to a queue. Then, in chat, ask Patch Bay to "check the map's leads" and it researches, grades and marks each one.

All of them are drawn from the gear graph by a script, so the pictures always match the facts.

## Playlists

If you've connected a music service to Claude (for example the Spotify connector), Patch Bay can create the playlist there. Otherwise you get a clean track list to paste into an import tool such as TuneMyMusic or Soundiiz.

## The gear graph

A hand-checked map of British synth pop, 1978–1986, ships with the plugin, plus the records outside that focus that link it together (Donna Summer, Kraftwerk, Planet Rock). As of v0.4.0 it holds 39 songs, 8 albums, 37 machines and 84 artists, joined by 241 links. Half the links are documented, mostly from interviews with the people who made the records, and most gear links name the part the machine played.

Patch Bay researches beyond the graph as you play and keeps what it finds for the session. Two songs are still islands with no chain to Being Boiled; that's part of the game.

Maintainers: see [CURATING.md](CURATING.md).

## Install

- **Claude (web and desktop):** go to Customize > Plugins, choose Add marketplace, enter `laurencetimms/plugins`, then add Patch Bay from Discover.
- **Claude Code:** run `/plugin install patch-bay --marketplace laurencetimms/plugins`

Then start a chat and try **"What was in the charts this week in 1981?"**, **"Connect Relax to Being Boiled"** or **"Show me the map of Being Boiled"**.

## Requirements

Web search, so it can check charts and credits. Python, if available, for the graph tool; otherwise Claude reads the graph directly.

## Privacy

Patch Bay has no server of its own and collects nothing. It searches the web and reads public pages through Claude's own tools. If you publish the live Map of Being Boiled, it is a private page in your own Claude account until you share it: leads saved on it are stored in that page's own storage, with the saver's Claude account id, and are visible to whoever you share the page with. The playlist step uses a music connector, such as Spotify's, only if you have connected one.

## Licence

MIT. Built by [Laurence Timms](https://laurencetimms.com).
