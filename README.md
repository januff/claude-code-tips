# Claude Code Tips

109 tips from the Claude Code community, collected from a viral Twitter thread. Also: an experiment in actually learning them.

## Source

The tips came from a thread by [@alexalbert__](https://x.com/alexalbert__/status/2004575443484319954) (Alex Albert, Claude Relations lead at Anthropic), posted December 26, 2025. He asked: *"What's your most underrated Claude Code trick?"* The thread got 98K views and 182 replies.

"Most underrated" is a good question. It surfaces the stuff power users actually rely on but don't talk about much. The day-after-Christmas timing worked out for me personally—I'd just received a Pro account as a gift and wanted to know what to do with it.

## What this repo is for

The obvious thing would be to scrape the thread, format the tips, and call it done. We did that. But the actual goal is to learn these tips systematically—not just document them.

The nightmare scenario: do all this work organizing 109 tricks and never actually absorb any of them. That would be a waste. So the plan is to have multiple Claude instances help work through the tips one at a time, applying them to this repo and my other projects as a way to internalize them.

This is a work in progress. The repo is not finished. The current state is: tips collected, analysis written, multi-instance workflow tested. What's coming: prompts for each tip, a checklist for tracking which ones I've tried, maybe interactive demos.

If you clone this, you could do the same thing—add your own Claude instances, work through the tips at your own pace, adapt them to your projects.

## Multi-instance workflow

Four different Claude instances have worked on this repo:

- **Claude Code CLI** built the initial structure
- **Cursor Sidebar (Opus 4.5)** reviewed plans, made edits, wrote this README
- **Claude Desktop** refined the integration strategy
- **Claude Mobile** completed a task from my phone (the .gitignore)

The handoffs between instances are documented in `plans/`. The methodology itself came from Tip #1 (The Handoff Technique), which turned out to be the most-liked tip in the thread.

## Repository contents

```
claude-code-tips/
├── CLAUDE.md                      # Instructions for Claude instances
├── README.md                      # You are here
├── .gitignore                     # Created by Claude Mobile
│
├── tips/
│   ├── full-thread.md             # All 109 tips, formatted
│   ├── grouped-tips.md            # Tips organized by theme
│   └── raw-thread-unformatted.md  # Original scrape (archived)
│
├── analysis/
│   └── claude-commentary.md       # Opus 4.5's take on which tips matter
│
├── plans/
│   ├── integration-plan.md        # Current plan (v2, amended)
│   ├── mobile-task-001.md         # Example atomic task handoff
│   └── archive/                   # Historical versions
│       ├── integration-plan-v1.md
│       └── integration-plan-review.md
│
└── .claude/
    └── settings.json              # Claude Code permissions
```

## Key themes

Most of the 109 tips cluster around a few ideas:

**Context management.** Clear sessions before you're forced to. Use `/compact` proactively. Store progress in markdown files so you can pick up later. Use subagents for tasks that might pollute your main context.

**Planning vs. execution.** Don't plan and code in the same session. Architect in one session, implement in another. The planning session can generate prompts for the coding session.

**Documentation as infrastructure.** CLAUDE.md is foundational. Treat memory files like code files. Document for handoff—assume the next reader has no context.

**Extended thinking.** `think` < `think hard` < `think harder` < `ultrathink`. Save ultrathink for architecture decisions.

The full list is in `tips/full-thread.md`. Some are jokes ("threaten to use Codex"), some are genuinely useful.

## Top 10 by engagement

Engagement isn't everything, but it's one signal for which tips resonated:

1. **The Handoff Technique** (160 likes) — Generate prompts for passing work between AI instances
2. **"Take a step back and think holistically"** (77 likes) — Escape loops with this phrase
3. **"Threaten to use Codex"** (53 likes) — Emotional prompting, apparently works
4. **Architect in Claude Desktop first** (52 likes) — Separate planning from execution
5. **DevSQL for prompt analysis** (43 likes) — Analyze your own prompt history
6. **Always check today's date first** (41 likes) — Prevent outdated documentation lookups
7. **Code word verification** (32 likes) — Confirm Claude read your instructions
8. **Be nice to Claude** (29 likes) — Self-explanatory
9. **Document everything in .MD files** (27 likes) — Use each file as context and bridge to next session
10. **Security auditing** (23 likes) — "Audit the codebase for security issues" always finds something

## Status

Phase 1 (foundation) is partially done:

- [x] .gitignore (Claude Mobile)
- [x] Code word verification (already existed)
- [ ] Update CLAUDE.md structure
- [ ] Add LICENSE

Phases 2-4 cover starter templates, skills, learning curriculum, and eventually a tip-collection workflow. Details in `plans/integration-plan.md`.

## For Claude instances

Read `CLAUDE.md` first. It has project context and a verification code word ("context-first").

## Contributing

Found a good tip? Open an issue with the tip, source, and your experience using it.

## Tone credit

The README was rewritten to avoid common AI-writing tells, following guidance from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and [@blader's distillation](https://x.com/blader/status/1997403206994055510) of that page into a prompt.

## License

MIT.
