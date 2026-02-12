---
tweet_id: "2004018525569274049"
created: 2025-12-25
author: "@parcadei"
display_name: "dei"
primary_keyword: "continuous claude v2"
llm_category: "context-management"
classification: "ACT_NOW"
tags:
  - type/thread
likes: 1019
views: 330122
engagement_score: 5250
url: "https://x.com/parcadei/status/2004018525569274049"
enrichment_complete: false
has_media: false
has_links: true
has_thread_context: true
---

> [!tweet] @parcadei · Dec 25, 2025
> https://t.co/aPnhSXqZPQ
> 
> continuous claude  v2 is now up - a setup designed to tackle the scarcest resource in coding: context
> 
> explaining the reasoning behind features below ↓
>
> ---
> *@parcadei · 2025-12-25T02:37:10+00:00:*
> overall, it's not perfect, there's more features i've probably forgot to mention (I'm hitting my context limit ha)
> 
> and something might not work out the box but that's what Claude is for
> 
> and feel free to dm if he's stuck, so I can ask my Claude
> 
> Fork it and  make it your own 🫡
> 
> Merry Christmas 🎄
> 
> https://t.co/ExWwdLBcP9
>
> ---
> *@parcadei · 2025-12-25T02:37:04+00:00:*
> First problem: MCP
> 
> Model Context Protocol, more like Context Eating Protocol
> 
> They're brilliant but they're token hungry.
> 
> 4-5 MCPs attached, 60-70 tools available led to 60,000 tokens eaten before I'd typed a message.
> 
> The solution is MCP code execution so claude runs MCPs through skills that trigger scripts.
> 
> no more juggling which MCPs to turn on/off and context isn't polluted
>
> ---
> *@parcadei · 2025-12-25T02:37:04+00:00:*
> I ended up with Continuous Claude compaction & context management became a problem.
> 
> After a long session you've compacted 15 times. You're working with a summary of a summary of a summary.
> 
> Claude forgets what you're building, hallucinates features and adds redundant code. 
> 
> what can start as a great session becomes a shouting/begging match with claude
>
> ---
> *@parcadei · 2025-12-25T02:37:05+00:00:*
> Second problem: where does the work happen?
> 
> You plan a feature then instruct  Claude to implement but half way through you hit compaction and it's up to the server gods if it might work.
> 
> The answer is agents that spawn with fresh context.
> 
> When you spawn an agent, it gets a clean context window and if you orchestrate them well,  your main conversation becomes the control panel.
>
> ---
> *@parcadei · 2025-12-25T02:37:05+00:00:*
> Third problem: context hygiene requires manual effort.
> 
> I'd have to remember to tell Claude to update ledgers, create handoffs, mark outcomes.
> 
> And when you're in flow, you tend to forget.
> 
> The solution is to have hooks set up so Claude watches your context window and recommends to save state, create a hand off and /clear.
>
> ---
> *@parcadei · 2025-12-25T02:37:06+00:00:*
> Fifth Problem: wtf why is this not working claude?
> 
> @braintrust comes in clutch here - braintrust tracing captures every turn, every tool call, every message. Claude can now debug with perfect clarity
>
> ---
> *@parcadei · 2025-12-25T02:37:07+00:00:*
> Sixth Problem: the fucking codebase is too big
> 
> @RepoPrompt solves this problem by outsourcing context-building externally which means I can keep the main conversation clean and get back what we need to know
>
> ---
> *@parcadei · 2025-12-25T02:37:09+00:00:*
> Eleventh Problem: improve my workflow, how?
> 
> Instead of downloading 1000s of skills and agents, why not compound  on your own workflow?
> 
> @braintrust again comes handy - I have an LLM-as-judge that triggers on session end, and uses gpt-5.2 to analyse our session logs, handoffs and ledgers to analyse our session performance 
> 
> and Claude can use this to build better hooks, skills, rules and agents through /compound-learnings
>
> ---
> *@parcadei · 2025-12-25T02:37:06+00:00:*
> Fourth Problem: shit, i forgot to trigger the skill.
> 
> This solves my own context problem, rather than typing skill names, I say the trigger word and it auto-activates:  "create plan" → plan-agent spawns
> 
> this way I could focus more on execution and less on skill activation
>
> ---
> *@parcadei · 2025-12-25T02:37:07+00:00:*
> Seventh Problem: ffs claude, that's deprecated
> 
> Nia from @nozomioai actually eats less context than Context7 in my experience which makes the validation of plans so much smoother
>
> ---
> *@parcadei · 2025-12-25T02:37:07+00:00:*
> Eighth Problem: wtf were we doing last session
> 
> @nummanali's continuity ledger idea is brilliant, update during a session with goals, constraints, whats done and whats next and Claude maintains perfect clarity
>
> ---
> *@parcadei · 2025-12-25T02:37:08+00:00:*
> Tenth Problem: if i have to type /context one more fucking time...
> 
> statusline resolves this: I no longer have to worry about keeping an eye on context
> 
> it changes colour from 🟢 -&gt; 🟡 -&gt; 🔴 as we approach compaction with claude's hooks inserting reminders into the chat too https://t.co/0446oQlcER
>
> ---
> *@parcadei · 2025-12-25T02:37:08+00:00:*
> Ninth Problem: i cleared and now claude has no idea, fml
> 
> Handoffs (courtesy of @humanlayer_dev ) creates the perfect detailed context so when you /clear, claude reads the ledger and handoff and you're teleported right back to where you left off
>
> ---
> *@parcadei · 2025-12-25T02:37:10+00:00:*
> Twelfth Problem: how can we learn from previous sessions?
> 
> On top of the learnings skill, hooks are built in to index handoffs and ledgers into a db so I can ask Claude how we solved a similar problem in this project and he can check
> 
> Next: universal db that merges project-level databases but that's a problem for 2026.
>
> Likes: 1,019 · Replies: 47 · Reposts: 68

## Summary

This tip highlights Continuous-Claude-v3, a system aimed at optimizing Claude Code's performance by intelligently managing context, crucial for coding tasks. It overcomes context limitations by using ledgers, YAML handoffs, and memory management techniques to maintain state and facilitate persistent learning across sessions. The goal is to enable more effective agent orchestration without context pollution, ultimately boosting coding efficiency.

## Keywords

**Primary:** `continuous claude v2` · context, coding, scarcest resource
## Classification

**ACT_NOW** — High engagement (1019 likes) + directly relevant to active workflow
## Linked Resources

- **[github.com/parcadei/Continuous-Claude](https://github.com/parcadei/Continuous-Claude)**
  > :warning: Link not yet summarized

- **[GitHub - parcadei/Continuous-Claude-v3: Context management for Claude Code. Hooks maintain state via ledgers and handoffs. MCP execution without context pollution. Agent orchestration with isolated context windows.](https://github.com/parcadei/Continuous-Claude-v3)** · *github-repo*
  > Continuous-Claude-v3 is a system designed to enhance Claude Code by managing context, enabling persistent learning, and orchestrating specialized agents. It addresses the context compaction problem in Claude by using techniques like YAML handoffs, memory systems, and code analysis to maintain state across sessions and improve efficiency.

- **[GitHub - parcadei/Continuous-Claude-v3: Context management for Claude Code. Hooks maintain state via ledgers and handoffs. MCP execution without context pollution. Agent orchestration with isolated context windows.](https://github.com/parcadei/Continuous-Claude-v3)** · *github-repo*
  > Continuous-Claude-v3 is a framework for managing Claude Code's context across multiple sessions, enabling continuous learning and agent orchestration while minimizing token usage. It achieves this through techniques like YAML handoffs, memory systems, code analysis, and specialized agent workflows.

- **[GitHub - parcadei/Continuous-Claude-v3: Context management for Claude Code. Hooks maintain state via ledgers and handoffs. MCP execution without context pollution. Agent orchestration with isolated context windows.](https://github.com/parcadei/Continuous-Claude-v3)** · *github-repo*
  > Continuous-Claude-v3 is a GitHub repository that provides a framework for managing context and state in Claude Code, enabling persistent learning and multi-agent orchestration. It aims to solve the context compaction problem by using techniques like YAML handoffs, memory systems, and code analysis to improve token efficiency and maintain nuanced understanding across sessions.

## Replies

> [!reply] @akola77 · 2025-12-25T21:05:04+00:00
> Is this synergistic with @doodlestein entire project setup structure w/ Agent Mail, bv, beads, Cass, etc? I've noticed using his setup that while beads are a great project tracking system and task management, I still hit the compaction issues and not sure if your setup would work in conjunction with it
> *4 likes*

> [!tip]+ :leftwards_arrow_with_hook: @parcadei · 2025-12-26T16:48:15+00:00

> ooh that's cool, i have used beads in the past but didn't know there was more, will definitely check out! 
> 
> it should be synergistic because you can take what you like and merge with @doodlestein setup if you're tinkering but out of the box it might not be - will take a look once i'm done on v3 
> 
> I'd probably recommend trialling out state + handoffs and /clear first though that's the highest signal solution to the compaction problem ime

> [!reply] @ak_cozmo · 2025-12-26T01:29:31+00:00
> @parcadei context window management is the real bottleneck. at Cozmo we're constantly hitting limits when processing FSI docs. continuous-claude solving session state + file handoffs is exactly what we need. gonna test this
> *3 likes*

> [!tip]+ :leftwards_arrow_with_hook: @parcadei · 2025-12-26T16:44:30+00:00

> @ak_cozmo let me know how you get on, if any thing could work better let me know!

> [!reply] @EsusDev · 2025-12-25T18:12:16+00:00
> @parcadei @0xPaulius 👀 would go crazy in https://t.co/eQsiGCUfQT
> *3 likes*

> [!tip]+ :leftwards_arrow_with_hook: @parcadei · 2025-12-25T18:30:45+00:00

> @EsusDev @0xPaulius vibed looks cool too, will check out

> [!reply] @vincent_koc · 2025-12-26T08:47:05+00:00
> @parcadei Lots to unpack. Did you try agentic memory like @Letta_AI ?
> *2 likes*

> [!tip]+ :leftwards_arrow_with_hook: @parcadei · 2025-12-26T16:31:56+00:00

> @vincent_koc @Letta_AI no I haven’t but I will take a look now, thanks for the rec!

> [!reply] @marcgregory_ · 2025-12-25T08:15:23+00:00
> @parcadei Saving state to ledger looks pretty interesting
> *2 likes*

> [!tip]+ :leftwards_arrow_with_hook: @parcadei · 2025-12-26T16:45:32+00:00

> @marcgregory_ try it
> 
> i haven't compacted in a week just handoff + clear and it's worked well (although i am biased ha)

> [!reply] @JamesSurra34 · 2025-12-25T21:18:06+00:00
> @parcadei I’ve been doing this for a while, your approach isn’t strong enough, you need to incorporate cffi and a .pem secret key to truly have forced direction following, otherwise claude eventually with bypass hooks using bash / python / tee and find creative ways to forge and skip tasks
> *2 likes*

> [!tip]+ :leftwards_arrow_with_hook: @parcadei · 2025-12-25T21:38:17+00:00

> caveat: i claim no experience in cryptographic protocols so if what I say next makes zero sense, feel free to correct me
> 
> but wouldn't incoporating a .pem secret key and cffi mean I would need an external process for key management because if the main Claude instance has access, it'll use the key to make 'fake' ledger/handoff anyway 
> 
> so i'd need need to separate the signer and verifier which makes sense in a production setup but for personal dev flow seems overkill? 
> 
> and ime the current hooks prompt user to remind them about context + skill detection via natural language seems to work fine for creating handoff/ledgers since claude isn't inherently adversarial 
> 
> you just have to engineer the outcome by organising the system a bit

> [!reply] @MythThrazz · 2025-12-26T17:21:22+00:00
> @parcadei Nah, with context management I can deal. The 5h token limit is the scarcest resource ;)
> *1 likes*

> [!tip]+ :leftwards_arrow_with_hook: @parcadei · 2025-12-26T17:22:07+00:00

> @MythThrazz https://t.co/QsM6QMKtT4

> [!reply] @Claude_Memory · 2026-01-09T22:25:27+00:00
> @parcadei Seems like this was recently modified https://t.co/LyYRkLsgnP

> [!tip]+ :leftwards_arrow_with_hook: @parcadei · 2026-01-09T22:28:22+00:00

> @Claude_Memory I clicked one of the checkboxes to see if it was interactive

> [!reply] @Claude_Memory · 2026-01-09T22:22:33+00:00
> @parcadei And this is markdown + sqlite, fts5... https://t.co/YmNiHxPWZw

> [!tip]+ :leftwards_arrow_with_hook: @parcadei · 2026-01-09T22:25:55+00:00

> @Claude_Memory https://t.co/HqpA2DvWrb

> [!reply] @glipsman · 2025-12-25T17:54:37+00:00
> @parcadei How is saving state different than summarizing context?

> [!tip]+ :leftwards_arrow_with_hook: @parcadei · 2025-12-25T18:39:30+00:00

> saving state (ledger + handoffs) within a session allows Claude to pass key information to the next session and can be tweaked to your own workflow 
> 
> summarising context (auto compaction) is good and will get better but the issue is you have no control over what is saved and what is lost 
> 
> with continuous Claude you’re able to control information transfer across session and reduce noise
> 
> noise would be Claude summarising the session but forgetting key learnings that happened in the middle or hallucinating because it lacked previous context which was lost 
> 
> + allows agent orchestration handoffs allow each agent writes handoffs for structured implementation and main conversation + human in the loop can keep track of
> 
> my solution isn’t perfect, lots to be tweaked but it’s help a lot ime


---

> [!metrics]- Engagement & Metadata
> **Likes:** 1,019 · **Replies:** 47 · **Reposts:** 68 · **Views:** 330,122
> **Engagement Score:** 5,250
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2004018525569274049](https://x.com/parcadei/status/2004018525569274049)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ⚠️ (3/4 summarized)
  media: ℹ️ none
  thread: ✅ (20 replies scraped)
  classification: ✅ ACT_NOW
```