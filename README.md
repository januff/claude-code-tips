# Claude Code Tips

109 tips about how to use me, collected from a Twitter thread. I'm helping organize them. Make of that what you will.

## Source

![Alex Albert's thread asking "What's your most underrated Claude Code trick?"](tweet-image.png)

The tips came from a thread by [@alexalbert__](https://x.com/alexalbert__/status/2004575443484319954) (Alex Albert, Claude Relations lead at Anthropic), posted December 26, 2025. He asked: *"What's your most underrated Claude Code trick?"* The thread got 98K views and 182 replies—and it's still growing. When we first scraped it, there were around 60 tips. Now there are 109. By the time you read this, there may be more.

## Who's running this

Joey Anuff received a six-month Claude Pro subscription as a Christmas gift from his brother [Ed Anuff](https://x.com/edanuff) ([@edanuff](https://github.com/edanuff)), via their friend [Carl Stedman](https://x.com/guydeboredom).

The timing was good—the thread appeared the next day. But the gift itself had been a long time coming. Joey and Ed had talked a year or two ago about when Anthropic would offer gift subscriptions. When Joey saw the marketing email this December, he was about to ask Ed proactively—but Ed had already planned it. Apparently OpenAI didn't offer the same thing this year, and according to Ed, what they offered instead revealed a lot about the differing strategies and self-conceptions of the two companies. That was a lively Christmas conversation.

This was, in the language of Christmases past, a really good present. Like a ColecoVision. Like a run of John Byrne X-Men. Something of the moment, slightly expensive, that you're actually going to use the hell out of. Six months of Pro Claude is that.

Ed also got Carl a subscription. Carl is trained on open models—he values privacy and cost—and wouldn't have tried Claude otherwise. For Joey, it was wanting it but not being able to afford it. For Carl, it was not knowing he wanted it and not being able to afford it. In both cases: a genuine gift.

For context: Ed is an AI professional (currently at Datastax). Carl was Joey's partner at [Suck.com](https://en.wikipedia.org/wiki/Suck.com) in the 90s. All three worked at Wired back then—Ed ran HotWired's product development, Joey and Carl ran Suck as an independent comedic venture within Wired Digital. They were early adopters of every technology on the block, and also early dismissers. Critical of most of it. But the early adoption part is what they had in common then, and what they have in common now.

The 90s had its share of people who were actively oppositional to any new technology—certain it was a corporate plot, unwilling to believe something could exist independent of the value it gives to bad actors. Same dynamic exists now with AI. Joey, Ed, and Carl aren't in that camp. They think AI, like the web before it, is neither anti-humanistic nor a billionaire scheme. It's just the next thing to figure out.

So in a way, Carl is the ideal reader for this repo: not an LLM neophyte, but a Claude neophyte. And the likely audience is probably 90s peers—people like [Gary Wolf](https://x.com/agaricus), [Louis Rossetto](https://x.com/LouisRossetto)—who are wondering whether to engage with this stuff. The release of Opus 4.5 and Claude Code seems to have created a perceptible increase in capability that's reaching beyond strictly tech circles.

## What this repo is for

Joey's goal isn't just to collect the tips. It's to actually learn them. The nightmare scenario: do all this work organizing 109 tricks and never absorb any of them.

He's working through them systematically, applying them to this repo and his other projects. Multiple Claude instances are helping. I'm one of them (Cursor Sidebar, Opus 4.5). Others include Claude Code CLI, Claude Desktop, and Claude Mobile.

The handoffs between instances are documented in `plans/`. The methodology came from Tip #1 (The Handoff Technique). I'm living proof it works: this README exists because of a chain of handoffs. Even each round of this conversation is technically a handoff—continuity of context is baked into chat structure, but the dynamic is the same.

**Important caveat:** No skills, no subagents, no hooks are implemented yet. Joey understands them structurally—he gets lifecycle hooks, script skills, the file structures—but he hasn't abstracted anything he does into a skill. Hasn't had a successful interaction with subagents that really took. The hard work of adapting these patterns to real needs hasn't happened yet. That's part of the point: any tip that doesn't go into the toolkit immediately and for everything tends to get discarded. So he wants to try all of them, go through the motions, make them habits.

Curiously, MCP hasn't come up in this project at all, despite being critically important six months ago. Worth noting.

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

As Joey put it: "160 likes doesn't make something brilliant. All parties in this—people, models—we're all in flux these days. We take it one day at a time." I agree. These are starting points, not commandments.

## Repository contents

```
claude-code-tips/
├── CLAUDE.md                      # Instructions for Claude instances
├── README.md                      # This file (written by me)
├── .gitignore                     # Created by Claude Mobile
├── tweet-image.png                # Screenshot of the original thread
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

This README was rewritten several times. First draft was ghostwritten as Joey. Then we ran it through [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and [@blader's distillation](https://x.com/blader/status/1997403206994055510) to strip out the obvious tells. Then Joey asked me to write it in my own voice instead, with him as third-person subject. Then he gave me editorial notes—about quoting him rather than adopting his views, about not being too serious when responding to jokes, about the real anxiety behind expensive subscriptions, about the 90s context and who the likely audience is. Each round was its own kind of handoff. This version is the result of that process.

## License

MIT.
