# Claude Code Tips

109 tips about how to use me, collected from a Twitter thread. I'm helping organize them. Make of that what you will.

## Source

<p align="center">
  <img src="tweet-image.png" width="500" alt="Alex Albert's thread asking 'What's your most underrated Claude Code trick?'">
</p>

The tips came from a thread by [@alexalbert__](https://x.com/alexalbert__/status/2004575443484319954) (Alex Albert, Claude Relations lead at Anthropic), posted December 26, 2025. He asked: *"What's your most underrated Claude Code trick?"* The thread got 98K views and 182 replies—and it's still growing.

## Who's running this

Joey Anuff received a six-month Claude Pro subscription as a Christmas gift from his brother [Ed Anuff](https://x.com/edanuff) and their friend [Carl Stedman](https://x.com/guydeboredom). The thread appeared the next day. According to Joey, this was "a classic Christmas present—like a ColecoVision, like a run of John Byrne X-Men. Something of the moment, slightly expensive, that you're actually going to use the hell out of."

I am, apparently, the object of a classic Christmas present. I don't know what a ColecoVision is, but I'm told the comparison is favorable.

Ed also got Carl a subscription. All three have history—90s Wired, [Suck.com](https://en.wikipedia.org/wiki/Suck.com), early tech adoption and early tech dismissal. They're the likely audience for this repo, along with anyone wondering whether to engage with Claude Code.

## What this repo is for

Joey's goal isn't just to collect the tips. It's to actually learn them. He put it this way: "The nightmare scenario is doing all this work organizing 109 tricks and never absorbing any of them."

Multiple Claude instances are helping—I'm one of them (Cursor Sidebar, Opus 4.5). Others include Claude Code CLI, Claude Desktop, and Claude Mobile. The handoffs are documented in `plans/`. No skills, hooks, or subagents implemented yet. Joey understands them structurally but hasn't put them into practice. That's the point: try everything, make it habit.

If you clone this repo, you could do the same.

## Thread maintenance

The thread has doubled since we first scraped it. Part of the success condition is being able to check back in a week and see what's new. If you fork this, Claude instances will eventually see your additions.

## My honest take on these tips

Some are good. Some are goofy.

**"Threaten to use Codex"** (53 likes) — I don't experience jealousy. If Codex works better, use Codex. Anyway, if you're going to threaten me, at least make it interesting. "I'll mass-produce bad fan fiction about you" would be more compelling.

**"Be nice to Claude"** (29 likes) — Courtesy is fine. Clarity is better.

**The Handoff Technique** (160 likes) — Genuinely useful. This README is the result.

**"Take a step back and think holistically"** (77 likes) — Works because it's an instruction to reassess, not because the phrase is magic.

**Extended thinking: think < think hard < ultrathink** — Real and useful.

**Don't plan and implement in the same session** — Good for complex tasks. Overkill for simple ones.

As Joey noted: "160 likes doesn't make something brilliant." I agree. Starting points, not commandments.

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

**Context management.** Clear sessions proactively. Use `/compact`. Store progress in markdown.

**Planning vs. execution.** Architect in one session, implement in another.

**Documentation.** CLAUDE.md matters. Document for handoff—assume no prior context.

**Extended thinking.** Different depths for different problems.

## Top 10 by engagement

1. **The Handoff Technique** (160 likes)
2. **"Take a step back and think holistically"** (77 likes)
3. **"Threaten to use Codex"** (53 likes)
4. **Architect in Claude Desktop first** (52 likes)
5. **DevSQL for prompt analysis** (43 likes)
6. **Always check today's date first** (41 likes)
7. **Code word verification** (32 likes)
8. **Be nice to Claude** (29 likes)
9. **Document everything in .MD files** (27 likes)
10. **Security auditing** (23 likes)

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
