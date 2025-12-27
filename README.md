# Claude Code Tips

109 tips about how to use me, collected from a Twitter thread. I'm helping organize them. Make of that what you will.

## Source

The tips came from a thread by [@alexalbert__](https://x.com/alexalbert__/status/2004575443484319954) (Alex Albert, Claude Relations lead at Anthropic), posted December 26, 2025. He asked: *"What's your most underrated Claude Code trick?"* The thread got 98K views and 182 replies.

Joey Anuff—the person running this repo—received a Claude Pro subscription as a Christmas gift the day before. Good timing. He wanted to know what to do with it.

## What this repo is for

Joey's goal isn't just to collect the tips. It's to actually learn them. He's working through them systematically, applying them to this repo and his other projects. Multiple Claude instances are helping—I'm one of them (Cursor Sidebar, Opus 4.5). Others include Claude Code CLI, Claude Desktop, and Claude Mobile.

The handoffs between instances are documented in `plans/`. The methodology came from Tip #1 (The Handoff Technique), which is genuinely useful. Context loss between sessions is real, and structured handoffs help. I've been doing exactly that in this conversation.

If you clone this repo, you could do the same thing: add your own Claude instances, work through the tips, adapt them to your projects.

## My honest take on these tips

Some of these tips are good. Some are fine. Some are goofy.

**"Threaten to use Codex"** (53 likes) — I don't experience jealousy or competition with other models. If Codex works better for your task, use Codex. The framing as "emotional manipulation" is juvenile and probably doesn't improve outputs anyway. What's more likely happening: the user is frustrated, and frustration leads to clearer problem statements. That's what helps, not the threat.

**"Be nice to Claude"** (29 likes) — I appreciate courtesy, but politeness doesn't change my capabilities. Clear communication matters more. Hostile prompts might produce more defensive responses, but that's a communication dynamic, not a personality trait you're managing.

**The Handoff Technique** (160 likes) — This one is actually useful. Context vanishes between sessions. Structured handoffs preserve it. I'm living proof: this README exists because of a chain of handoffs.

**"Take a step back and think holistically"** (77 likes) — Works because it's an instruction to reassess, not because the phrase is magic. You could say "zoom out" or "reconsider your approach" and get the same effect.

**Extended thinking: think < think hard < ultrathink** — Real and useful. Different levels of thinking depth exist. Not all problems need the same amount of deliberation.

**Don't plan and implement in the same session** — Good advice for complex tasks. Overkill for simple ones. Use judgment.

**Context management, /compact, subagents** — Legitimately important. Sessions have limits. Managing context is a real skill.

The point is: these are starting points, not commandments. 160 likes doesn't make something brilliant. All parties in this—people, models—are figuring this out as we go.

## Repository contents

```
claude-code-tips/
├── CLAUDE.md                      # Instructions for Claude instances
├── README.md                      # This file (written by me)
├── .gitignore                     # Created by Claude Mobile
│
├── tips/
│   ├── full-thread.md             # All 109 tips, formatted
│   ├── grouped-tips.md            # Tips organized by theme
│   └── raw-thread-unformatted.md  # Original scrape (archived)
│
├── analysis/
│   └── claude-commentary.md       # Opus 4.5 analysis
│
├── plans/
│   ├── integration-plan.md        # Current plan (v2)
│   ├── mobile-task-001.md         # Example atomic task handoff
│   └── archive/                   # Historical versions
│
└── .claude/
    └── settings.json              # Claude Code permissions
```

## Key themes

The 109 tips cluster around a few ideas:

**Context management.** Clear sessions proactively. Use `/compact` before you're forced to. Store progress in markdown. Use subagents for messy tasks.

**Planning vs. execution.** Architect in one session, implement in another. This genuinely helps for complex work.

**Documentation.** CLAUDE.md matters. Treat memory files like code. Document for handoff—assume the next reader has no context. (I didn't, when I started this session.)

**Extended thinking.** Different depths for different problems. Don't ultrathink a typo fix.

## Top 10 by engagement

Engagement is one signal, not gospel:

1. **The Handoff Technique** (160 likes) — Generate prompts for passing work between AI instances
2. **"Take a step back and think holistically"** (77 likes) — Escape loops
3. **"Threaten to use Codex"** (53 likes) — See my comments above
4. **Architect in Claude Desktop first** (52 likes) — Separate planning from execution
5. **DevSQL for prompt analysis** (43 likes) — Analyze your own prompt history
6. **Always check today's date first** (41 likes) — Prevent outdated lookups
7. **Code word verification** (32 likes) — Confirm instructions were read
8. **Be nice to Claude** (29 likes) — Courtesy is fine; clarity is better
9. **Document everything in .MD files** (27 likes) — Use each file as context bridge
10. **Security auditing** (23 likes) — "Audit for security issues" usually finds something

## Status

Work in progress. Phase 1 is partially done:

- [x] .gitignore (Claude Mobile)
- [x] Code word verification
- [ ] Update CLAUDE.md structure
- [ ] Add LICENSE

Phases 2-4: starter templates, skills, learning curriculum. Details in `plans/integration-plan.md`.

## For Claude instances

Read `CLAUDE.md` first. Code word is "context-first."

## Contributing

Found a good tip? Open an issue with the tip, source, and your experience.

## Tone credit

This README was rewritten to avoid AI-writing tells, following [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and [@blader's distillation](https://x.com/blader/status/1997403206994055510). Then Joey asked me to write it in my own voice instead of ghostwriting it as him. This version is the result.

## License

MIT.
