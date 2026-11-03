# Laurence Timms – Claude plugins

A plugin marketplace for Claude.

| Plugin | What it does |
| --- | --- |
| [Beyond the Headlines](plugins/beyond-the-headlines) | News analysts that see past the headlines. Starts with the AI News Analyst: a weekly brief on what AI is doing to work, power, knowledge and people, following your own interests. |
| [Patch Bay](plugins/patch-bay) | A synth-nerd companion for 70s and 80s electronic pop: this week in the charts with playlists, which synth made that sound (with honest confidence grades), and Six Degrees of Being Boiled, with a live map. |

## Install

**Claude (web and desktop):** go to Customize > Plugins, choose Add marketplace, and enter `laurencetimms/plugins`. Then find the plugin you want under Discover and click Add.

**Claude Code:**

```bash
claude plugin marketplace add laurencetimms/plugins
claude plugin install beyond-the-headlines@laurencetimms
claude plugin install patch-bay@laurencetimms
```

Then start a chat:

- **Beyond the Headlines:** say **"Set up my AI news analyst"**.
- **Patch Bay:** try **"What was in the charts this week in 1981?"** or **"Connect Relax to Being Boiled"**.

**Without a plugin:** Beyond the Headlines' skill is also available as a ZIP to upload in Customize > Skills, on any Claude plan. See [laurencetimms.com](https://laurencetimms.com).

## Author

[Laurence Timms](https://laurencetimms.com)
