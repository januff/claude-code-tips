---
created: 2026-01-23
author: "@brian_lovin"
display_name: "Brian Lovin"
tags:
  - type/thread
likes: 320
views: 21881
engagement_score: 1398
url: "https://x.com/brian_lovin/status/2014809437899522302"
---

> [!tweet] @brian_lovin · Jan 23, 2026
> The current tactics for using AI coding agents well are roughly:
> 
> 1. Give agents tools to self-verify
> 
> • MCP servers (agent-browser, playwright)
> • tests
> • tsc, linters
> 
> 2. Teach agents to build their own verification tools
> 
> Agents can write their own scripts, skills, subagents, eval frameworks, plans, and success criteria.
> 
> If you don't know what to ask, ask the agent: "what tools will you need to know you've done a good job?"
> 
> 3. Point the agent back at itself
> 
> • Turn complex workflows into reusable skills/subagents — after finishing a long session, ask the agent if there's anything you could extract into reusable skills.
> • Ask the agent to rewrite your prompts to be more clear
> • Use multiple models to evaluate each other (especially useful for evaluating plans + code review before a PR)
> • If a skill doesn't quite work, finish the task anyway, then feed the conversation back so it can improve the skill's instructions
> • If the agent asks you to do something manually, ask yourself: how do I teach the agent to answer this question on its own?
> • You can teach the agent to self-improve by writing meta-skills that update other skills/rules based on what worked (or didn't) as you close PRs.
> 
> 4. Give better context
> 
> • Attach screenshots
> • Link to docs/blog posts
> • Tell the agent to read source code for OSS dependencies
> • Link to examples of high-quality outcomes it should emulate
> 
> And if you don't know how to do anything above—ask the agent.
>
> Likes: 320 · Replies: 14 · Reposts: 20

## Summary

This tip outlines effective strategies for leveraging AI coding agents by focusing on self-verification, improvement, and enhanced context. It emphasizes equipping agents with tools for self-assessment, teaching them to build their own verification processes, and prompting them to reflect on and refine their own workflows and prompts. Key actions include utilizing MCP servers and tests for verification, extracting reusable skills from complex workflows, and providing relevant documentation and examples for improved context and outcomes.

## Replies

> [!reply] @bnj · 2026-02-10T21:10:29+00:00
> We made a tool that lets you absorb the vibe of anything you point it at and apply it to your designs
> 
> It's absurd and it just works
> 
> Style Dropper, now available in @variantui https://t.co/B3eXDntYtw
> *5119 likes*

> [!reply] @joshpuckett · 2026-02-10T14:34:36+00:00
> Interface Craft is now open. 
> 
> It’s a growing library of resources for those who are committed to crafting experiences and interfaces with uncommon care.
> 
> I hope you’ll consider joining: https://t.co/jcYLYg6pps
> *1598 likes*

> [!reply] @mrmagan_ · 2026-02-10T18:54:57+00:00
> build an agent that speaks your UI.
> 
> your charts. your forms. your seat maps.
> 
> multi-turn, streaming, interactive.
> 
> introducing tambo 1.0, the open-source generative UI toolkit for react. https://t.co/5l1IfFbjwp
> *916 likes*

> [!reply] @jenny_wen · 2026-02-10T15:20:46+00:00
> Our friend @claudeai got a few very special upgrades!!
> 
> Instead of just text, you can interact with Claude's responses. Less typing, more clicking (but also still typing if you'd like!)
> 
> 💫 @leesimin, Alex, and Chelsea. So many nice details; lots of them designed directly in code https://t.co/Hx7no9omAJ
> *914 likes*

> [!reply] @BogdanDragomir · 2026-01-23T22:17:00+00:00
> @brian_lovin 5. Treat failure as data
> *8 likes*

> [!tip]+ ↩️ @brian_lovin · 2026-01-23T22:22:07+00:00

> @BogdanDragomir Good one

> [!reply] @jonaslamis · 2026-02-10T03:26:14+00:00
> Dystopian thought of the day:  
> 
> As @alexwg champions; AIs will need rights as they approach and exceed sentience.  
> 
> But what if WE are those very AI's and our simulators have afforded us the right to die as their method of solving this conundrum?
> *4 likes*

> [!reply] @wildpinesai · 2026-01-23T22:27:37+00:00
> @brian_lovin @mmt_lvt self-verification is the unlock most people skip. agents that can run tests, check their own output, and iterate without you hovering - that's where the real productivity multiplier lives. planning + verification &gt; prompt engineering every time.
> *3 likes*

> [!reply] @tristanbob · 2026-01-24T13:00:37+00:00
> @brian_lovin This is gold advice!
> *1 likes*

> [!reply] @mrbavio · 2026-01-23T23:58:43+00:00
> @brian_lovin And use Conductor!
> *1 likes*

> [!reply] @Kannav02 · 2026-01-23T21:51:27+00:00
> @brian_lovin “Use multiple models to evaluate each other “
> 
> I use this so much, my workflow is codex 5.2 to execute the plan, and then codex 5.2 high for reviewing things i’m a bit ambigous about, works like a charm
> *1 likes*

> [!reply] @withgosha · 2026-01-24T00:15:14+00:00
> @brian_lovin its interesting to think of agents needing tools to self-verify
> *1 likes*

> [!reply] @kyle_fowler2 · 2026-01-23T22:07:12+00:00
> @brian_lovin This is gold. Self-verification has to be one of the biggest unlocks
> *1 likes*

> [!reply] @rswillif · 2026-01-23T22:19:22+00:00
> @brian_lovin Well put…the agents strongest incentive is to give you what u want, so ask it to give if what you want incrementally from foundational first principles and iterate/build context
> *1 likes*

> [!reply] @Iiterature · 2026-01-23T23:06:00+00:00
> @brian_lovin Great list. Also asking the agent to think if there are more token efficient ways of doing things after a long session.
> 
> E.g. making a script for a workflow rather than rawdogging data aggregation via MCP through inference.

> [!reply] @proxy_vector · 2026-01-24T17:14:49+00:00
> MCP servers are game changers for this. The self-verification loop is exactly what bridges the gap between "kinda works" and "actually production ready".
> 
> Been experimenting with having agents write their own playwright tests before implementing features. Sounds backwards but it forces cleaner outputs

> [!reply] @carlos__antony · 2026-01-24T06:58:52+00:00
> @brian_lovin agents get better once you stop treating them like autocomplete

> [!reply] @getpochi · 2026-01-24T03:13:50+00:00
> @brian_lovin when agent writes its own tools you kinda need maintenance. At some point prompt/skill behave like code and w/o CI they rot fastt


> [!metrics]- Engagement & Metadata
> **Likes:** 320 · **Replies:** 14 · **Reposts:** 20 · **Views:** 21,881
> **Engagement Score:** 1,398
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2014809437899522302](https://x.com/brian_lovin/status/2014809437899522302)