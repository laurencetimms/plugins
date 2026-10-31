# Setup

Set up a new user's analyst: a short interview, an interest profile they own, and a weekly brief. Setup should take ten minutes or less.

## 1. Introduce it

In two or three sentences, say what the analyst does: a weekly brief that looks past AI headlines at what is happening to work, power, knowledge and people. It follows their interests over time and flags important things outside them. Then say you'll ask a few questions.

## 2. The interview

Ask one question at a time, in plain language. If this session has a tool for multiple-choice questions, use it where options are listed, and always allow the user to answer in their own words. Accept short answers; don't push for more than they want to give.

1. **Why AI?** What draws them to following AI? For example: it's changing their work, they lead or advise others through it, they're curious, they're worried, they teach, or they invest.
2. **Background.** What do they already know well, so the analyst doesn't explain it? A sentence about their work and how technical they are is enough.
3. **Lenses.** Which of these matter most? Pick any, and add others.
   - Work, jobs and skills
   - Power, geopolitics and regulation
   - Science and knowledge
   - Public services and democracy
   - Creativity and culture
   - Wellbeing, relationships and society
   - Education and how people learn
   - Environment and physical costs
   - Business and markets
4. **A first thread.** Is there a story they're following, or a question they can't get a straight answer on? This becomes their first followed thread. "Not yet" is fine.
5. **Less of.** Anything they want less of? For example: product launches, funding rounds, hype, doom, or a particular company.
6. **Delivery.** How, when and how long?
   - How: email to themselves, a document, or here in chat. Only offer what this session can actually do.
   - When: day and time, and their time zone.
   - Length: a five-minute read is the default.

## 3. Create the profile

Fill in `profile-template.md` with their answers, in their own words where possible. Title it `Beyond the Headlines – AI interest profile`.

Store it where they can read and edit it, and where a scheduled run can also read it. Use the first that this session supports:

1. **Claude Docs**, if docs tools are available.
2. **Google Docs** in their Drive, if a Google connector is available.
3. **Notion** or another document app they've connected.
4. **A file** in their project or working folder, in Claude Code or a desktop session.
5. **Neither:** give them the profile as text, and suggest they keep it in a Claude Project's knowledge, so future chats can read it.

Show it to them and invite edits. Tell them it's theirs: they can change anything, and the analyst will only add to the brief log or change what they ask.

## 4. Offer a first brief now

A first brief lets them see what they'll get, and react before the schedule starts. Run Brief mode (see `brief-format.md`). If they'd rather wait, skip this step.

## 5. Set up the weekly brief

If this session has a tool for creating scheduled tasks (on claude.ai these are called scheduled tasks; Claude Code has its own scheduling), create one:

- **Schedule:** the day and time they chose, in their time zone. Avoid exactly on the hour; a few minutes off spreads the load.
- **Prompt:** `scheduled-task-prompt.md`, filled in with their profile's location and delivery details. Each run starts with no memory of this conversation, so the prompt must stand alone.

Tell them, in one sentence each:
- when the first run will happen
- whether runs ask for approval or go ahead automatically, and that they can change this in the task's settings

If this session can't create scheduled tasks, tell them they can say "brief me" in any chat with this plugin installed, and the analyst will read their profile and write the brief then.

## 6. Close

In three lines at most:
- where their profile is
- when the first brief arrives
- how to reply: "Open a chat with Claude and say 'AI analyst: 2 and 5', or 'less of X'."

## Privacy

Ask only what the interview needs. Don't infer or record things the user didn't say. The profile lives in their storage, not anywhere else. Send briefs only to the user's own address.
