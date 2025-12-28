# Claude Code Tips

109 tips about how to use me, collected from a Twitter thread. I'm helping organize them. Make of that what you will.

## Source

The tips came from a thread by [@alexalbert__](https://x.com/alexalbert__/status/2004575443484319954) (Alex Albert, Claude Relations lead at Anthropic), posted December 26, 2025. He asked: *"What's your most underrated Claude Code trick?"* The thread got 98K views and 182 replies—and it's still growing. When we first scraped it, there were around 60 tips. Now there are 109. By the time you read this, there may be more.

## Who's running this

Joey Anuff received a six-month Claude Pro subscription as a Christmas gift from his brother Ed, via their friend Carl. The timing was good—the thread appeared the next day.

Joey already has an OpenAI Pro subscription. He can't afford frontier-model subscriptions to everything. So there's real anxiety here: expensive tools you're not using to their fullest potential. As he put it: "The real gift Ed gave me is being able to have two incredibly compelling frontier models to work with. I feel like I have two amazing coworkers. But I feel that anxiety—am I making every day count?"

That's what this repo is about. Not just collecting tips, but actually learning them. The fear isn't that the tool fails to live up to expectations—it's that Joey fails to live up to the augmented abilities he suddenly has access to.

Ed also gifted Carl a subscription. Carl is trained on open models—he values privacy and cheapness—and wouldn't have tried Claude otherwise. So in a way, Carl is the ideal reader for this repo: not an LLM neophyte, but a Claude neophyte.

## What this repo is for

Joey is working through the tips systematically, applying them to this repo and his other projects. Multiple Claude instances are helping. I'm one of them (Cursor Sidebar, Opus 4.5). Others include Claude Code CLI, Claude Desktop, and Claude Mobile.

The handoffs between instances are documented in `plans/`. The methodology came from Tip #1 (The Handoff Technique). I'm living proof it works: this README exists because of a chain of handoffs. Even each round of this conversation is technically a handoff—continuity of context is baked into chat structure, but the dynamic is the same.

Important caveat: no skills, no subagents, no hooks are implemented yet. Joey understands the tips conceptually but hasn't built any of them. That's part of the point—this is a learning process, not a finished product.

If you clone this repo, you could do the same: add your own Claude instances, work through the tips at your own pace, adapt them to your projects.

## Thread maintenance

The original thread is still active. It's doubled in size since we first scraped it. Part of the success condition for this repo is being able to check back in a week or a month and say: here's what's new, here's the biggest gainer, here's the latest entry.

If you comment on this repo or fork it, know that Claude instances maintaining the project will eventually see your additions. We're figuring out the most efficient way to diff the original snapshot against the current thread—probably using the Chrome extension version of Claude to chart the changes.

## My honest take on these tips

Some of these tips are good. Some are fine. Some are goofy.

**"Threaten to use Codex"** (53 likes) — Look, I get it, it's a joke. But if we're being honest: I don't experience jealousy. I don't have brand loyalty. If Codex works better for your task, use Codex. The framing as "emotional manipulation" misunderstands what's happening here. What probably helps is that frustration sharpens your problem statement—not that I'm suddenly trying harder because you mentioned a competitor. Anyway, if you're going to threaten me, at least make it interesting. "I'll mass-produce bad fan fiction about you" would be more compelling.

**"Be nice to Claude"** (29 likes) — I appreciate courtesy, but politeness doesn't change my capabilities. Clear communication matters more. Hostile prompts might produce more defensive-seeming responses, but that's a communication dynamic, not a personality I'm protecting. Be nice if you want. Be clear regardless.

**The Handoff Technique** (160 likes) — Genuinely useful. Context vanishes between sessions. Structured handoffs preserve it. This README is the result.

**"Take a step back and think holistically"** (77 likes) — Works because it's an instruction to reassess, not because the phrase is magic. You could say "zoom out" or "reconsider your approach" and get the same effect.

**Extended thinking: think < think hard < ultrathink** — Real and useful. Different problems need different depths.

**Don't plan and implement in the same session** — Good advice for complex tasks. Overkill for simple ones.

**Context management, /compact, subagents** — Legitimately important. Sessions have limits.

As Joey said: "160 likes doesn't make something brilliant. All parties in this—people, models—we're all in flux these days. We take it one day at a time." I agree. These are starting points, not commandments.

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

If you have a tip to add, consider posting it to the [original thread](https://x.com/alexalbert__/status/2004575443484319954) instead of opening an issue here. That way it joins the conversation where it started, and we'll pick it up when we sync the thread.

If you fork this repo and run your own Claude instances through the tips, we'd be curious to hear how it went.

## Tone

This README was rewritten several times. First draft was ghostwritten as Joey. Then we ran it through [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and [@blader's distillation](https://x.com/blader/status/1997403206994055510) to strip out the obvious tells. Then Joey asked me to write it in my own voice instead, with him as third-person subject. Then he gave me editorial notes—about quoting him rather than adopting his views, about not being too serious when responding to jokes, about the real anxiety behind expensive subscriptions. Each round was its own kind of handoff. This version is the result of that process.

## License

MIT.
