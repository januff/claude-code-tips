# For Will: Exporting Your Claude Chat History

*Draft by Joey, with Claude's help. Review and edit before sending.*

---

## Why we're doing this

Over the last few months, most of the thinking about HAND and H&D has happened inside your Claude chat — product strategy, CBN methodology refinements, partner outreach drafts, technical notes, the works. That chat history is one of the most valuable assets this company has, and right now it only lives in your browser.

We're going to export it, filter it for the HD-specific material, and turn it into a shared knowledge base that any Claude instance on the team can read to understand the project. After this, when Josh or John's Claude asks "what's the CBN signal engine?" it'll already know.

**Important:** you're going to do this export yourself, in your own Claude session, on your own machine. I'm not going to see it until you decide what's appropriate to share. This is your data, and some of it is privileged.

---

## Step 1: Request your data export from Claude

1. Go to **claude.ai** in your browser and make sure you're signed in.
2. Click your profile icon (top right) → **Settings** → **Privacy** (or **Account** → **Data Controls** depending on what version you're on).
3. Look for a button that says **"Export data"** or similar. Click it.
4. Confirm. Claude will email you a download link within a few minutes, usually faster.

The email will come from Anthropic and will say something like "Your Claude data export is ready."

---

## Step 2: Download and unzip

1. Click the download link in the email. It will give you a `.zip` file — usually 10–200 MB depending on how much you've used Claude.
2. Save it somewhere you can find it easily, like `~/Downloads/claude-export.zip` or your Desktop.
3. Double-click the zip to unzip it. You'll get a folder with 4 files:
   - `conversations.json` — all your chat history
   - `projects.json` — your Claude.ai projects and their uploaded files
   - `memories.json` — anything Claude has auto-remembered
   - `users.json` — small account metadata file

**Don't open any of these files yet.** They're big and messy. We'll let your Claude do the reading.

---

## Step 3: Open Claude in a terminal, pointed at your HD-Dev folder

If you haven't used Claude Code in a terminal before, here's the short version:

1. Open the **Terminal** app on your Mac (press **Cmd+Space**, type "Terminal", hit Enter).
2. Navigate to your HD-Dev folder by typing this and pressing Enter:
   ```
   cd ~/Development/HD-Dev
   ```
   *(If your HD-Dev folder lives somewhere else, use that path instead.)*
3. Start Claude Code by typing:
   ```
   claude
   ```
   and pressing Enter.

Claude will greet you and ask what to work on. You're in a Claude Code session now — same Claude, different window.

---

## Step 4: Hand the export to Claude and ask it to filter

Copy and paste this exact prompt into the Claude Code session:

```
I just ran a data export from claude.ai and unzipped it. The folder is at:
~/Downloads/data-YYYY-MM-DD-HH-MM-SS-batch-0000
(replace with the actual folder name you got)

Please do the following, and show me each step before taking it:

1. Read projects.json first and list every Claude project I have, with:
   - Project name
   - Number of conversations in each
   - Total message count

2. For each project, tell me in one sentence what it seems to be about (based on
   the project description or the first conversation's summary).

3. Then I'll tell you which projects are HD-related. Don't copy or filter
   anything yet — just wait for my instruction.

Keep everything local. Do not send any of this data anywhere outside my machine.
```

Claude will list your projects. You'll probably see a dozen or so. Some will obviously be HAND/H&D. Others might be side projects, personal stuff, or old experiments.

---

## Step 5: Tell Claude which projects are in scope

Once Claude has listed them, reply with something like:

```
The HD-related projects are: [list the project names, e.g.,
"HAND Strategy", "CBN Methodology", "Registry Intelligence Tool",
"Candidate Calendar", "Partnership Outreach"]

For each of those, please:

1. Create a folder at ~/Development/HD-Dev/project-memory/chat-archive/
2. For each HD-related project, create a subfolder named after the project
3. Inside each subfolder, write a file called 00_index.md that lists every
   conversation in that project with its date, title, and a 1-2 sentence summary
   (use the "summary" field from the JSON if available, otherwise skip summary)
4. DO NOT write the full message content yet. Just the index.
5. When done, show me the index for the largest project so I can spot-check it.
```

This gives you a map of what's in your chat history, organized by project, without dumping the raw content yet. You can read the indexes, check for anything sensitive, and decide what goes further.

---

## Step 6: Add the archive to .gitignore

Before Claude writes anything, tell it:

```
Before we go any further, please add this line to the .gitignore file in
~/Development/HD-Dev:

project-memory/chat-archive/

Commit that change with the message "chore: gitignore chat archive (private)".
```

This makes sure nothing from your chat archive ever gets pushed to GitHub by accident. Everything in that folder stays local to your machine only, unless you explicitly decide otherwise.

---

## Step 7: Review the indexes

Once Claude has generated the indexes, **read them**. Specifically look for:

- Any conversation title that mentions people or companies you wouldn't want summarized in shared team memory (investor conversations, personal calls, candid venting about colleagues, NDA'd discussions, etc.)
- Any project that shouldn't be in the team-shared archive at all

When you find something sensitive, tell Claude:

```
The conversation titled "[title]" should not be included in the team archive.
Please delete its entry from the index and flag it on a separate file called
EXCLUDED.md with just the date and title (no content) so I have a record.
```

---

## What we'll do next (after you've done the above)

Once your chat archive is indexed and privacy-filtered, the next step is to use those indexes to build the project's "institutional memory" — a set of short markdown files in `project-memory/` that any new Claude instance can read in under 5 minutes to get oriented on the project. That step I can help you draft, because it's the outward-facing summary, not the raw content.

**You do NOT need to finish this in one sitting.** The export, indexing, and review can happen over a few days. The important thing is that it gets started and that you own it.

---

## If you get stuck

If Claude Code does something unexpected, or you're not sure if a command is safe, just ask Claude:

```
Before you do that, explain what it will do and what the risk is.
```

Claude Code will not make destructive changes without confirmation unless you've explicitly told it to. Your files are safe.

If the terminal feels alien, we can also do a screenshare and I'll walk you through the first session. But I genuinely think this is worth doing yourself — partly because of the privacy angle, and partly because the experience of giving Claude a big unstructured pile of data and asking it to organize it is the muscle memory you'll want for everything else in this project.

---

*End of instructions.*
