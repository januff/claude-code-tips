---
created: 2026-01-12
author: "@menhguin"
display_name: "Minh Nhat Nguyen"
tags:
  - type/thread
likes: 256
views: 22026
engagement_score: 925
url: "https://x.com/menhguin/status/2010688647218298936"
---

> [!tweet] @menhguin · Jan 12, 2026
> My Beginner Tierlist of Agent Abstractions (for Claude):
> 1. Subagents - Direct buff. Frequently very useful for preventing context rot and ad-hoc specialisation. Sorta adjacent to RLM. IMO, it's good bc as agents get smarter they very effectively allocate subagents. Bitter-lesson adjacent. Simple to use w not much variation - "use subagents when needed". Half as useful as much more complex setups (multi-agent) for much less complexity.
> 2. Metaprompting - I made a metaprompting claude command to expand my task requests into full prompt files + scratchpad. I take 3 minutes to prompt a 20-minute task. Also generally a direct buff. You should usually read the metaprompt plan, but improves stability and sanity-checks assumptions anyway.
> 3. Asking the user more at the beginning - Generally direct buff, but u have to answer questions in plan mode. A little non-transparent bc i can't tell if it's not asking bc it understands, the command is off or has no questions.
> 4. "Thinking" prompts - Generally a buff and easy to toss in, but not-transparent and is sorta getting phased out per Boris.
> -----below are useful, but high skill floor------
> 5. Long-running agents - The main thing is you have to think a bit to be able to prompt and set this up well. Basically you have to understand the shape and tradeoff of a 15 minute task before you understand the shape of a 1.5 hour or 4 hour task. Or whether to do four 15 minute tasks or one 1-hour task. And It takes some tweaking and is obv very long trial-and-error. Fundamentally tho, it's usually the same setup "but go longer in a useful way".
> 6. Parallel multi- agent - I think this is very high-variance, and only useful on highly complex or highly well-segmented/scoped tasks or very very experienced setups. If 2 tasks take 10 minutes and you spend an arbitrary amount of time prompting or god forbid, merge changes, it's counterproductive. If u have a good scaffold for this tho, prolly very good, you just prolly won't get there with parallel multi-agent. High skill floor and skill ceiling vs the direct buffs above.
> 7. Role-based multi-agent - It can work, but I am on principle bearish on this. Models just evolve too fast for hard-coded heuristics unless the arbitrage is very high. Also hard to test. I've seen people swear by Codex planner + Opus executor which probably works. Idk, maybe skill issue?
> 8. Computer Use Agents - I think this is hard to do bc it plays at a very long tail of tasks. You're getting models to do something they were definitely not even meant to do a year ago. As a paradigm, very early and requires wrangling. @hud_evals will cook here, tho.
> 
> (MCP/search agents I feel is more a situation-dependent tool to fetch from data sources that otherwise wouldn't exist at all. And p much all production agent scaffolds have this now. ig if you're pedantic, they're top tier bc theyre the default)
>
> ---
> *@menhguin · 2026-01-12T12:22:22+00:00:*
> man.
> https://t.co/DYj99BlkFE
>
> Likes: 256 · Replies: 15 · Reposts: 10

## Summary

This Claude tip ranks different agent abstraction techniques, categorizing them by ease of implementation and potential benefit. It highlights simple, directly beneficial methods like subagents and metaprompting as top-tier for improved context handling and prompt engineering. More complex setups like parallel multi-agent systems and computer use agents are deemed useful but require significantly higher skill and specialized scenarios.

## Replies

> [!reply] @ccccjjjjeeee · 2026-02-10T09:53:07+00:00
> It actually worked!
> 
> For the past couple of days I’ve been throwing 5.3-codex at the C codebase for SimCity (1989) to port it to TypeScript. 
> 
> Not reading any code, very little steering. 
> 
> Today I have SimCity running in the browser. 
> 
> I can’t believe this new world we live in. https://t.co/Pna2ilIjdh
> *4273 likes*

> [!reply] @jimmybajimmyba · 2026-02-11T00:05:00+00:00
> Last day at xAI.
> 
> xAI's mission is push humanity up the Kardashev tech tree. Grateful to have helped cofound at the start. And enormous thanks to @elonmusk for bringing us together on this incredible journey. So proud of what the xAI team has done and will continue to stay close as a friend of the team. Thank you all for the grind together. The people and camaraderie are the real treasures at this place.
> 
> We are heading to an age of 100x productivity with the right tools. Recursive self improvement loops likely go live in the next 12mo. It’s time to recalibrate my gradient on the big picture. 2026 is gonna be insane and likely the busiest (and most consequential) year for the future of our species.
> *3011 likes*

> [!reply] @PrimeIntellect · 2026-02-11T01:57:38+00:00
> Introducing Lab: A full-stack platform for training your own agentic models
> 
> Build, evaluate and train on your own environments at scale without managing the underlying infrastructure.
> 
> Giving everyone their own frontier AI lab. https://t.co/wDVCe7TOdt
> *795 likes*

> [!reply] @willccbb · 2026-02-11T02:25:14+00:00
> create your own environments. 
> train your own models.
> be your own lab. https://t.co/pfEzGqoRvi
> *327 likes*

> [!reply] @menhguin · 2026-01-11T19:09:27+00:00
> i spent a few weeks doing this, and my current bottleneck is having tasks to feed the agents. i have a claude desktop agent, a prompt-to-agent-task flow, multi parallel agents, subagents, scheduled review agents, computer use agents and im not utilising like 80% of capacity
> *52 likes*

> [!reply] @ptr · 2026-01-12T15:04:37+00:00
> Great list!
> 
> I do think we will find that parallel multiagent is not that different from Ralph setups and much much faster. Ralph fights context rot by restarting and seeding N agents with the same plan in parallel has a similar essence
> 
> Most people shouldn’t worry about that at all yet though, as you say
> 
> And you above the line list is v v good
> *3 likes*

> [!tip]+ ↩️ @menhguin · 2026-01-12T15:09:14+00:00

> @ptr FWIW, in theory parallel is the highest-ceiling of all of these, since you are really functionally uncapped for unit human time. It's just getting from 0-2 working well takes a lot of skill, effort and iteration/cleaning. Currently most of my work hours have 1 parallel agent.

> [!reply] @KyeGomezB · 2026-01-12T20:54:00+00:00
> @menhguin Swarms provides most of these features if you want to build your own custom agents not just for programming.
> 
> Github: https://t.co/cUj7WdBQDC
> *2 likes*

> [!reply] @unknown
> 

> [!reply] @hud_zah · 2026-01-13T06:10:22+00:00
> @menhguin what subagents do you have and use?

> [!reply] @_soulninja · 2026-01-12T18:01:46+00:00
> @menhguin yes this tracks 1:1 from my experience as well
> 
> nicely articulated 👌

> [!reply] @MinChonChiSF · 2026-01-12T16:02:28+00:00
> @menhguin Feeding tasks to agents can definitely be a bottleneck.

> [!reply] @MinuteMovies3 · 2026-01-13T18:21:42+00:00
> @menhguin big brain stuff


> [!metrics]- Engagement & Metadata
> **Likes:** 256 · **Replies:** 15 · **Reposts:** 10 · **Views:** 22,026
> **Engagement Score:** 925
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2010688647218298936](https://x.com/menhguin/status/2010688647218298936)