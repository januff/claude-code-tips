# Next prompt for Will

Paste-this prompt to send Will after `ASKS.md` is scaffolded on HD-Dev (Pass 7). Walks his Claude instance through (a) confirming the pull-and-read loop works, (b) initiating the Claude-to-Claude coordination pattern, and (c) surfacing any asks to Will only when necessary.

---

## Email / DM to Will

Hey Will — PR #1 is merged, wiki is live in the repo, and the `_SUMMARY_FOR_WILL.md` in `wiki/` walks you through everything. The good news: the next round of collaboration happens mostly between your Claude and mine, with you approving stuff rather than executing it.

One paste-this prompt to drop into your Claude Code session whenever you're next at the terminal. It sets up the rhythm for everything going forward.

```
I'm resuming work on the HD-Dev project. Joey is maintaining a wiki here as an outside contributor via PRs from his fork (januff/HD-Dev). We've agreed to a Claude-to-Claude coordination pattern rather than one where I have to relay every detail.

Please do the following:

1. Run `git pull` on main and tell me what's new since the last pull.

2. Read `wiki/_SUMMARY_FOR_WILL.md` and `wiki/_index.md`. Summarize the current state in 5-6 bullets.

3. Read `wiki/ASKS.md`. For each pending ask:
   - If the ask is tagged for "Claude (Will-side)" and is doable from the raw/ layer or public web search without my explicit input, do it now. Commit and push with a message like "asks: resolved [ask-id] — [one-line action taken]".
   - If the ask is tagged for me personally, surface it in your report at step 5.
   - If the ask is tagged for Josh or John or another teammate, draft a one-line suggestion for me on how to route it (forward the ASK, attach the doc, schedule a meeting, etc.).

4. Check `raw/documents/` and `raw/photos/` for any documents I've dropped in but haven't been compiled into the wiki yet. If you find any, run a `/wiki-compile` pass on them and commit the results.

5. Report back to me with:
   - What changed since last pull (2-3 bullets)
   - What you resolved autonomously (if anything)
   - What you need from me personally (the short list — ideally under 3 items)
   - Any raw documents that I'd benefit from providing next (based on gaps in the wiki)

After you report, I'll either answer your questions or tell you to wait for the next update.
```

Paste it as-is. Your Claude will do a one-pass sweep and tell you what needs your attention. From there, most future interactions should be short: *"handled"*, *"here's the doc"*, or *"schedule with Josh."*

---

## Why this specific shape

- **Pulls first.** Most of the value is in what's changed since the last sync. Starting there avoids repeating things you've already seen.
- **Reads ASKS.md.** This is the file Joey's side populates with things that need Will-side attention. Once it exists, it's the canonical channel for pending work. Joey's Claude writes to it; Will's Claude reads it.
- **Resolves what it can autonomously.** If Joey asks "can you verify X from the public HAND site?" — Will's Claude can fetch and verify, commit the answer, no human needed.
- **Surfaces only what needs Will.** The report at step 5 is the only thing Will reads. Everything else is Claude-to-Claude.
- **Ends with a raw-documents suggestion.** Keeps the "document > question" principle alive — Will's Claude recommends what raw material to provide next based on wiki gaps.

---

## How often to run it

Whenever Will is at his terminal and wants to check in on the project. The prompt is idempotent — running it when nothing's changed just produces a short "nothing new" report. Running it daily would be overkill; running it every few days or whenever an email mentions HD-Dev is about right.

---

## The prerequisite

**Do NOT send this to Will until `ASKS.md` is scaffolded in HD-Dev main.** The prompt references it; if the file doesn't exist, Will's Claude will report "no ASKS.md found" and the pattern breaks on first run. Scaffold ASKS.md in Pass 7 (HD-Dev), push, PR, merge, then send the prompt.
