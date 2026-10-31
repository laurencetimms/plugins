# Beyond the Headlines

News analysts that see past the headlines.

Most AI news chases attention. Sometimes the headline matters. Often it distracts from slower, subtler changes that are harder to fit into one line, but just as important. Beyond the Headlines gives you a personal analyst that looks at both, and tells you which is which.

## The AI News Analyst

The first analyst in the plugin. Each week it sends you a brief on what AI is doing to work, power, knowledge and people, both good and bad, and it follows your interests over time.

Each brief has:

- **The shape of the week**, in two or three sentences
- **Your threads:** only what's genuinely new on the stories you follow
- **A menu** of five to seven possible insights, each marked *headline* or *under-covered*
- **Outside your lanes:** up to two important stories beyond your interests, and only when they clear a stated bar
- **Sources** for everything

Pick from the menu and it does a deep dive: what the story really is, what the people closest to it are arguing about, what's known and unknown, who is affected, and what to watch.

## How it thinks

Every story gets the same questions:

1. What kind of claim is this?
2. Who is speaking, and what do they gain?
3. What is verified, what is asserted, and what is conjecture?
4. What are the people closest to it saying?
5. What is the coverage leaving out?
6. Who is affected, and how?
7. What would change the assessment?

It keeps what was reported, what experts agree on, and its own interpretation visibly apart. It's made by Anthropic, an AI company, so it says so whenever Anthropic or Claude is part of a story.

## Get started

Install the plugin.

- **Claude (web and desktop):** go to Customize > Plugins, choose Add marketplace, enter `laurencetimms/plugins`, then add Beyond the Headlines from Discover.
- **Claude Code:** run `/plugin install beyond-the-headlines --marketplace laurencetimms/plugins`

Then say:

> Set up my AI news analyst

It asks you a few questions: why you follow AI, what you already know, which lenses matter to you, a story you're following, what you want less of, and how and when you'd like your brief. Then it:

1. creates your **interest profile**, a document you own and can edit
2. offers a first brief straight away
3. sets up a **weekly scheduled task** where your Claude account supports it

To respond to a brief, open a chat and say something like `AI analyst: 2 and 5` or `less of funding rounds`. To get a brief any time, say `brief me`.

## What it works with

It works best when Claude can search the web, and has somewhere to keep your profile and a way to deliver briefs. It adapts to what you have connected:

- **Profile:** Claude Docs, Google Docs, Notion, or a file in your project. Without any of these, it gives you the profile as text to keep in a Claude Project.
- **Delivery:** email to yourself, a document, or the chat.
- **Schedule:** scheduled tasks where available. Otherwise, say `brief me` whenever you want one.

## Privacy

Your profile lives in your own storage. The analyst asks only what it needs, records only what you tell it, and sends briefs only to your own address.

## Author

[Laurence Timms](https://laurencetimms.com). Feedback and ideas for new analysts are welcome.
