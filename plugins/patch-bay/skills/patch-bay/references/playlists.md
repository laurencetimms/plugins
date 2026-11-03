# Playlists

## Build

- Title it: "This Week in 1983: 23 January", "Six Degrees: Cars → Being Boiled", "Everything on a Jupiter-8".
- One line per track: artist, title, year, and why it's there.
- Name the version where it matters (single edit, 12", original 1978 recording).

## Hand over

Check what this session can reach, in this order:

1. **A music connector is available** (for example the Spotify connector for Claude, which can search and create playlists). Search for each track, match on artist, title and version, create the playlist in the user's account, and report what you couldn't match. Ask before creating it the first time in a conversation; creating a playlist puts something in the user's account.
2. **No connector.** Give the list as plain "Artist – Title" lines in a code block so it copies cleanly. Mention once that services such as TuneMyMusic or Soundiiz can import a pasted list into Spotify, Tidal, Apple Music and others, and that a Spotify connector for Claude exists if they'd like it done automatically next time.

Never ask the user for passwords or API keys. If a track isn't on the service, say so and suggest the nearest available version.
