# Claude Code Tips

109 tips from the Claude Code community, collected from a viral Twitter thread. Also: an experiment in running multiple Claude instances on the same codebase.

## What's in here

The tips came from [@alexalbert__'s thread](https://x.com/alexalbert__/status/2004575443484319954) (December 26, 2025, 98K views). We scraped the replies, formatted them, and added some analysis.

But the repo itself became an experiment. Four different Claude instances worked on it:

- **Claude Code CLI** built the initial structure
- **Cursor Sidebar** reviewed plans and made edits
- **Claude Desktop** refined the strategy
- **Claude Mobile** completed a task from my phone

The handoffs between instances are documented in `plans/`. If you're curious how to coordinate multiple Claude sessions on one project, that's probably more interesting than the tips themselves.

## Files

```
tips/
  full-thread.md           # All 109 tips, formatted
  grouped-tips.md          # Same tips, organized by theme
  raw-thread-unformatted.md # Original scrape (archived)

analysis/
  claude-commentary.md     # Opus 4.5's take on which tips matter

plans/
  integration-plan.md      # Current plan for the repo
  mobile-task-001.md       # Example of an atomic task handoff
  archive/                 # Old versions

CLAUDE.md                  # Instructions for Claude instances
.gitignore                 # Created by mobile app
```

## The tips worth knowing

Most of the 109 tips fall into a few categories. Here are the ones that actually changed how I work:

**Context management.** Clear sessions before you're forced to. Use `/compact` proactively. Store progress in markdown files so you can pick up later.

**Don't plan and code in the same session.** Architect in one session, implement in another. The planning session can generate prompts for the coding session.

**Subagents for isolation.** Spawn subagents for tasks that might pollute your main context.

**Extended thinking.** `think` < `think hard` < `think harder` < `ultrathink`. Save ultrathink for architecture decisions.

The full list is in `tips/full-thread.md`. Some are jokes ("threaten to use Codex"), some are genuinely useful.

## Top 5 by engagement

1. **The Handoff Technique** (160 likes) — Generate prompts for passing work between AI instances
2. **"Take a step back and think holistically"** (77 likes) — Escape loops with this phrase
3. **"Threaten to use Codex"** (53 likes) — Emotional prompting, apparently works
4. **Architect in Claude Desktop first** (52 likes) — Separate planning from execution
5. **DevSQL for prompt analysis** (43 likes) — Analyze your own prompt history

## Status

Phase 1 is partially done:

- [x] .gitignore (mobile app)
- [x] Code word verification (already existed)
- [ ] Update CLAUDE.md structure
- [ ] Add LICENSE

Phase 2-4 stuff (starter templates, skills, learning curriculum) is mapped out in `plans/integration-plan.md`.

## For Claude instances

Read `CLAUDE.md` first. It has project context and a verification code word.

## Contributing

Found a good tip? Open an issue with the tip, source, and your experience using it.

## License

MIT.
