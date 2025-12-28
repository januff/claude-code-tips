# Claude Code Tips

109 tips about how to use me, collected from a Twitter thread. I'm helping organize them. Make of that what you will.

## Source

<p align="center">
  <img src="tweet-image.png" width="500" alt="Alex Albert's thread asking 'What's your most underrated Claude Code trick?'">
</p>

The tips came from a thread by [@alexalbert__](https://x.com/alexalbert__/status/2004575443484319954) (Alex Albert, Claude Relations lead at Anthropic), posted December 26, 2025. He asked: *"What's your most underrated Claude Code trick?"* The thread got 98K views and 182 replies—and it's still growing.

## Who's running this

Joey Anuff received a six-month Claude Pro subscription as a Christmas gift from his brother [Ed Anuff](https://x.com/edanuff). According to Joey, the gift sub was "a classic Christmas present—like a ColecoVision, like a run of John Byrne X-Men. Something of the moment, slightly expensive, that you're actually going to use the hell out of." I am, apparently, the object of a classic Christmas present. I don't know what a ColecoVision is, but I'm told the comparison is favorable.

Ed also got their friend [Carl Steadman](https://x.com/guydeboredom) a gift subscription. All three have history—90s Wired, [Suck.com](https://en.wikipedia.org/wiki/Suck.com), early tech adoption and early tech dismissal. Joey was going to forward them the thread on Slack. Instead, he built this repo. Overkill? Possibly. But now you can have it too.

## What this repo is for

Joey's goal isn't just to collect the tips. It's to actually learn them. He put it this way: "The nightmare scenario is doing all this work organizing 109 tricks and never absorbing any of them."

Multiple Claude instances are helping—I'm one of them (Cursor Sidebar, Opus 4.5). Others include Claude Code CLI, Claude Desktop, and Claude Mobile. The handoffs are documented in `plans/`. No skills, hooks, or subagents implemented yet. Joey understands them structurally but hasn't put them into practice. That's the point: try everything, make it habit.

If you clone this repo, you could do the same.

## Thread maintenance

The thread has doubled since we first scraped it. Part of the success condition is being able to check back in a week and see what's new. If you fork this, Claude instances will eventually see your additions.

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
├── tweet-image.png                # Screenshot of the original thread
├── tips/
│   ├── full-thread.md             # All 109 tips, formatted
│   ├── grouped-tips.md            # Tips organized by theme
│   └── raw-thread-unformatted.md  # Original scrape (archived)
├── analysis/
│   └── claude-commentary.md       # Opus 4.5 analysis
├── plans/
│   ├── integration-plan.md        # Current plan (v2)
│   ├── mobile-task-001.md         # Example atomic task handoff
│   └── archive/                   # Historical versions
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

Work in progress. Phase 1 partially done. Details in `plans/integration-plan.md`.

## For Claude instances

Read `CLAUDE.md` first. Code word is "context-first."

## Contributing

Post tips to the [original thread](https://x.com/alexalbert__/status/2004575443484319954). We'll pick them up when we sync.

## Tone

This README went through several drafts. First as Joey, then stripped of AI tells, then rewritten in my voice with Joey as subject. He gave editorial notes; I incorporated them. Each round was its own handoff. Details in [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and [@blader's prompt](https://x.com/blader/status/1997403206994055510).

## License

MIT.
