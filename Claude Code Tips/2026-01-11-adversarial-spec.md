---
created: 2026-01-11
author: "@0xzak"
display_name: "zak.eth"
tags:
  - type/thread
likes: 1185
views: 81534
engagement_score: 5325
url: "https://x.com/0xzak/status/2010213382494798108"
---

> [!tweet] @0xzak · Jan 11, 2026
> Just shipped adversarial-spec, a Claude Code plugin for writing better product specs.
> 
> The problem: You write a PRD or tech spec, maybe have Claude review it, and ship it. But one model reviewing a doc will miss things. It'll gloss over gaps, accept vague requirements, and let edge cases slide.
> 
> The fix: Make multiple LLMs argue about it.
> 
> adversarial-spec sends your document to GPT, Gemini, Grok, or any combination of models you want. They critique it in parallel. Then Claude synthesizes the feedback, adds its own critique, and revises. This loops until every model agrees the spec is solid.
> 
> What actually happens in practice: requirements that seemed clear get challenged. Missing error handling gets flagged. Security gaps surface. Scope creep gets caught. One model says "what about X?" and another says "the API contract is incomplete" and Claude adds "you haven't defined what happens when Y fails."
> 
> By the time all models agree, your spec has survived adversarial review from multiple perspectives.
> 
> Features:
> - Interview mode: optional deep-dive Q&A before drafting to capture requirements upfront
> - Early agreement checks: if a model agrees too fast, it gets pressed to prove it actually read the doc
> - User review period: after consensus, you can request changes or run another cycle
> - PRD to tech spec flow: finish a PRD, then continue straight into a technical spec based on it
> - Telegram integration: get notified on your phone, inject feedback from anywhere
> 
> Works with OpenAI, Google, xAI, Mistral, Groq, Deepseek. Leveraging more models results in stricter convergence.
> 
> If you're building something and writing specs anyway, this makes them better.
> 
> Check it out and let me know what you think!
> 
> https://t.co/OrFf5HUI10
>
> ---
> *@0xzak · 2026-01-14T15:25:12+00:00:*
> 4 days live and this has really picked up traction! 
> 
> 389 stars, 37 commits, 6 contributors, 7 issues closed, 5 PRs merged, 325 tests @ 92% coverage
> 
> Community shipped Codex CLI integration for ChatGPT subscribers (Gary Basin), AWS Bedrock for enterprise routing (Ross Feinstein), Gemini CLI support without API keys (Pavel Kaminsky), OpenRouter support (lunov), plugin manifest fixes (David Aronchick)
> 
> Also added: O-series model support, web search flag, configurable timeouts, interactive model selection, focus modes, personas, cost tracking, session checkpoints, task export
> 
> Thanks for all the contributions! Feels good shipping stuff that people like to use!
>
> Likes: 1,185 · Replies: 78 · Reposts: 69

## Summary

The Claude Code plugin `adversarial-spec` enhances product specifications by having multiple LLMs (GPT, Gemini, Grok, etc.) critique them in parallel until a consensus is reached. This iterative debate uncovers gaps, challenges assumptions, and surfaces edge cases that a single model review might miss, leading to more comprehensive and robust specs. Key features include interview mode, early agreement checks, user review periods, PRD-to-tech-spec flow, and Telegram integration.

## Replies

> [!reply] @Corpetty · 2026-01-12T14:48:49+00:00
> @0xzak I'm about to go HAM on this repo. Do you wanna sit on a @HashingItOutPod and wildly nerd out about specs with me?
> *6 likes*

> [!tip]+ ↩️ @0xzak · 2026-01-12T14:55:50+00:00

> @Corpetty @HashingItOutPod Lmao yeah let’s do it

> [!reply] @austinc3301 · 2026-01-11T23:52:03+00:00
> @0xzak I've been doing this by hand for months. Somehow never thought of writing a Claude plugin for it.
> *5 likes*

> [!reply] @Julien_Bouvier · 2026-01-11T14:47:10+00:00
> @0xzak have you tried/planned a similar tool but for generating a spec from an existing codebase? I work with existing codebases and now try to extend with AI, but often results are disappointing. am wondering if I should generate detailed specs to better guide the AI.
> *4 likes*

> [!tip]+ ↩️ @0xzak · 2026-01-11T16:27:21+00:00

> @Julien_Bouvier Have not. Would be interesting to experiment with though.

> [!reply] @cewh1te · 2026-01-11T14:22:33+00:00
> @0xzak awesome, i’ve been doing this manually for a while and GPT always finds some things claude misses, super useful if you’re planning something complex
> *4 likes*

> [!reply] @realSidhuJag · 2026-01-12T17:34:56+00:00
> @0xzak It gets even better if you ensure one or a set is in the “no” camp and one is in the “yes” camp and then you want to make sure the no turns to a yes.
> *3 likes*

> [!reply] @Derpnat0r · 2026-01-11T15:56:28+00:00
> @0xzak Nice work!. Do you think there any benefits in running the adversarial-spec agains the same llm, just using different models?
> *2 likes*

> [!tip]+ ↩️ @0xzak · 2026-01-11T16:28:34+00:00

> @Derpnat0r Not sure for certain, but I’d say probably.

> [!reply] @hbruceweaver · 2026-01-11T15:06:12+00:00
> @0xzak why does this have 4o, 4-turbo, and o1 as the default openai models to use for conversation? 
> 
> compared to opus 4.5, thats like asking a team of 3 middle schoolers to review a PHD's thesis? 
> 
> like the idea tho, testing with modern models
> *2 likes*

> [!tip]+ ↩️ @0xzak · 2026-01-11T16:26:46+00:00

> @hbruceweaver You can use multiple models.

> [!reply] @sinuhet · 2026-01-11T14:39:18+00:00
> @0xzak Finally someone did what I was doing manually in my IDE (MD docs I have uploaded to Gemini 3 pro for summary). Is there a different approach to the Greenfield versus Brownfield project? How many arguing cycles are there about before the final PRD is done &amp; what costs/tokens?
> *2 likes*

> [!tip]+ ↩️ @0xzak · 2026-01-11T16:28:08+00:00

> @sinuhet It’s about 7 cycles to achieve consensus, but depends on the models you use. I found that grok is the laziest and agrees much earlier than any of the other models.

> [!reply] @0xZakk · 2026-01-11T18:06:47+00:00
> @0xzak This is sick
> *2 likes*

> [!reply] @nummanali · 2026-01-11T13:47:26+00:00
> @0xzak Awesome spec
> 
> I use this approach all the time time, across the full SDLC process
> 
> Great to see it codified in a plugin!
> *2 likes*

> [!reply] @carlosml · 2026-01-11T08:59:32+00:00
> @0xzak This is wild. Forcing LLMs to debate specs feels like hosting a tech cage match
> *2 likes*

> [!reply] @masonic_tweets · 2026-01-11T05:32:04+00:00
> @0xzak YES
> *1 likes*

> [!tip]+ ↩️ @0xzak · 2026-01-11T05:33:42+00:00

> @masonic_tweets yes

> [!reply] @juanfranblanco · 2026-01-11T05:36:33+00:00
> @0xzak Nice!!
> *1 likes*

> [!tip]+ ↩️ @0xzak · 2026-01-11T05:37:00+00:00

> @juanfranblanco thanks! try it out and lmk what you think!

> [!reply] @sinuhet · 2026-01-11T14:47:30+00:00
> @0xzak Stupid question: as not all LLM have the same speed, do they all wait until the last LLM responds before they proceed with the next step/argument? Can I see the LLM dispute in real-time?
> *1 likes*

> [!tip]+ ↩️ @0xzak · 2026-01-11T16:29:27+00:00

> @sinuhet Yeah, they all wait and you can provide feedback after each cycle.

> [!reply] @DabbaNetwork · 2026-01-12T05:32:09+00:00
> @0xzak Multi-model disagreement as a forcing function is clever.
> *1 likes*

> [!reply] @RepKeithAmmon · 2026-01-11T18:10:32+00:00
> @0xzak Does it work with OpenRouter?
> *1 likes*

> [!reply] @netdragon0x · 2026-01-11T06:15:11+00:00
> @0xzak Nice, starred. I have a dedicated planning repository for new projects that includes custom instructions for PRDs and generating Linear tasks... but it's just one model.
> *1 likes*

> [!reply] @Shenanigrahams · 2026-01-11T05:51:33+00:00
> @0xzak Always with the vibes, this one
> *1 likes*

> [!reply] @petheth · 2026-01-11T09:03:40+00:00
> @0xzak oooh! time to get some red teaming done
> *1 likes*

## Linked Resources

- [GitHub - zscole/adversarial-spec: A Claude Code plugin that iteratively refines product specifica...](https://t.co/OrFf5HUI10)
  > A Claude Code plugin that iteratively refines product specifications by debating between multiple LLMs until all models reach consensus. - zscole/adversarial-spec

> [!metrics]- Engagement & Metadata
> **Likes:** 1,185 · **Replies:** 78 · **Reposts:** 69 · **Views:** 81,534
> **Engagement Score:** 5,325
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2010213382494798108](https://x.com/0xzak/status/2010213382494798108)