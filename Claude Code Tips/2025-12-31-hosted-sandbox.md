---
tweet_id: "2006377570485543329"
created: 2025-12-31
author: "@mckaywrigley"
display_name: "Mckay Wrigley"
primary_keyword: "hosted sandbox"
category: "meta"
llm_category: "tooling"
tools: ["hooks", "skills", "subagents"]
tags:
  - category/meta
  - type/reply
  - type/thread
  - tool/hooks
  - tool/skills
  - tool/subagents
likes: 296
views: 18894
engagement_score: 1346
url: "https://x.com/mckaywrigley/status/2006377570485543329"
enrichment_complete: true
has_media: false
has_links: true
has_thread_context: true
---

> [!tweet] @mckaywrigley · Dec 31, 2025
> it's an sdk that allows you to build any kind of agent with all of the tools from claude code.
> 
> skills, subagents, hooks, etc. it's all there.
> 
> for web apps you'll want to run it in a hosted sandbox. i recommend @e2b, but anthropic has docs here: https://t.co/rWnRG22NaJ
> 
> the sandbox is basically just a virtual computer that the agent can work in. it's slightly intimidating for non-technical people, but feed the docs to claude code, have it explain things, and you'll be up and running in no time.
>
> Likes: 296 · Replies: 12 · Reposts: 17

## Summary

The Claude Agent SDK empowers developers to create sophisticated agents equipped with diverse skills and tools. To build web applications, the SDK should run within a secure, hosted sandbox environment, which acts as a virtual computer for the agent. While setting up the sandbox might seem complex initially, you can use Claude Code itself to understand the documentation and streamline the process, leveraging provider options like E2B (recommended in the tweet) or others documented by Anthropic.

## Keywords

**Primary:** `hosted sandbox` · sdk, skills, subagents, hooks, virtual computer, e2b
## Linked Resources

- **[Hosting the Agent SDK](https://platform.claude.com/docs/en/agent-sdk/hosting)** · *docs*
  > Documentation for deploying Claude Agent SDK in production environments. Covers container-based sandboxing requirements, deployment patterns (ephemeral, long-running, hybrid sessions), sandbox provider options (Cloudflare, Modal, Daytona, E2B, Fly, Vercel), and guidance on resource allocation, network access, and cost optimization.

- **[Hosting the Agent SDK - Claude Docs](https://platform.claude.com/docs/en/agent-sdk/hosting)** · *documentation*
  > Documentation for deploying Claude Agent SDK in production environments. Covers container-based sandboxing requirements, deployment patterns (ephemeral, long-running, hybrid sessions), sandbox provider options (Cloudflare, Modal, Daytona, E2B, Fly, Vercel), and guidance on resource allocation, network access, and cost optimization.

- **[Hosting the Agent SDK - Claude API Docs](https://platform.claude.com/docs/en/agent-sdk/hosting)** · *documentation*
  > This document details how to host the Claude Agent SDK in a production environment, emphasizing the differences between it and stateless LLM APIs. It covers hosting requirements, including container-based sandboxing, system requirements (Python/Node.js, resource allocation, network access), and provides an overview of the SDK architecture.

- **[Hosting the Agent SDK - Claude API Docs](https://platform.claude.com/docs/en/agent-sdk/hosting)** · *documentation*
  > This Claude API documentation outlines the requirements and considerations for hosting the Agent SDK in a production environment. It emphasizes the importance of container-based sandboxing for security and resource management due to the SDK's stateful nature and command execution capabilities.

- **[Hosting the Agent SDK - Claude API Docs](https://platform.claude.com/docs/en/agent-sdk/hosting)** · *documentation*
  > The Claude Agent SDK requires a different hosting approach than stateless LLM APIs, focusing on persistent conversational state and command execution within a secure environment. This documentation outlines the hosting requirements, architecture considerations, and security best practices for deploying Claude Agent SDK-based agents in production.

## Replies

> [!reply] @stnkvcs · Wed Dec 31 14:29:21 +0000 2025
> For 2026, all I wish is to finally wrap my head around Claude Agent SDK.
> 
> Most of CC’s power comes in its ability to work with files.
> 
> How does that translate to other mediums, like a good ol’ web app? Where do the files live?
> 
> I’m only semi-technical, so this still makes my head hurt.
> 
> @trq212 @mckaywrigley I’ve seen you talk about the SDK. Please, shed some knowledge 🙏🏻
> *109 likes*

> [!reply] @_bloodbones · Wed Dec 31 16:55:40 +0000 2025
> @mckaywrigley @stnkvcs @e2b I have the agent SDK running on my own server where claude cli is installed.
> 
> Built a frontend for it. And I can now do things like fixing bugs, updating documentation, scheduling tasks, checking in on things on my server etc. on the go wherever I am. 
> 
> Been very useful. https://t.co/CRRJeTx3mn
> *5 likes*

> [!tip]+ :leftwards_arrow_with_hook: @mckaywrigley · Wed Dec 31 18:38:54 +0000 2025

> @_bloodbones @stnkvcs @e2b ahead of the game!!

> [!reply] @divyaranjan_ · Wed Dec 31 16:21:12 +0000 2025
> @mckaywrigley @stnkvcs @e2b should check out @daytonaio too! imo it’s better than e2b for a few use cases when it comes to the agent sdk.
> *3 likes*

> [!reply] @stnkvcs · Wed Dec 31 14:56:59 +0000 2025
> Yes this is what I was hoping for! But you’re spot on - it’s intimidating. I’ve built stuff with CC. This seems next level. Even Claude says it’s complicated. Especially deploying/hosting.
> 
> I have a few CC projects with niche domain expertise via skills I’d love to share with others. And the SDK seems like the way.
> 
>  This gives me hope.
> 
> Thanks Mckay! And a happy New Year 🤝
> *2 likes*

> [!tip]+ :leftwards_arrow_with_hook: @mckaywrigley · Wed Dec 31 15:01:26 +0000 2025

> a lot of the non-technical vibecoder types are mostly used to CRUD style apps that can take advantage of super easy to use serverless deployments that companies like vercel make so easy.
> 
> that architecture doesn't work for the sdk, so this is a bit of a departure from that. luckily it's not so much that it's difficult, but it's just kind of new to people who haven't done it before.
> 
> playing around for an evening should be enough to help make it click!

> [!reply] @techlifejosh · Wed Dec 31 16:06:04 +0000 2025
> @mckaywrigley @stnkvcs @e2b Awesome breakdown! Makes ton of sense. 
> 
> Curious, McKay is this your go to setup currently? Ie saw you had custom ui of agent dashboard etc. you run CC within a sandbox? 
> 
> Or are there other stacks you recommend toying with? Ie. Analysis paralysis with codex, Gemini etc
> *1 likes*

> [!tip]+ :leftwards_arrow_with_hook: @mckaywrigley · Wed Dec 31 16:11:52 +0000 2025

> @techlifejosh @stnkvcs @e2b yes. it's the best agentic harness in the world imo.
> 
> i'm all-in on this setup. anthropic has shown me enough to continue building for this future.

> [!reply] @ivanburazin · Sat Jan 03 15:06:41 +0000 2026
> @mckaywrigley @stnkvcs @e2b @mckaywrigley have you tried us at @daytonaio ? Here is a few guides how to use Agent SDK : https://t.co/rNl3bHphSb
> *1 likes*
>
> :paperclip: **[daytona.io/docs/en/claude](https://www.daytona.io/docs/en/claude/)** — Daytona is a platform for managing development environments and isolated sandboxes. Demonstrates integrating Claude Code with Daytona for running tasks in sandboxes and streaming logs programmatically through interactive terminal access, service connections, and autonomous multi-agent systems.

> [!reply] @LKorsun · Wed Dec 31 17:40:48 +0000 2025
> @mckaywrigley @stnkvcs @e2b This is what I have been looking for over the past few days, thanks @mckaywrigley
> *1 likes*

> [!reply] @markojak_ · Wed Dec 31 17:17:05 +0000 2025
> @mckaywrigley @stnkvcs @e2b I like e2b but observability is terrible
> They should have a default logging

> [!tip]+ :leftwards_arrow_with_hook: @mckaywrigley · Wed Dec 31 18:41:23 +0000 2025

> @markojak_ @stnkvcs @e2b their team is amazing and i suspect they’ll be all ears on feedback!
> 
> the sdk will drive many millions of sandboxes over there this year and community feedback can help drive it :)
> 
> cc @mlejva

> [!reply] @cmgrant0 · Wed Dec 31 14:59:06 +0000 2025
> @mckaywrigley @stnkvcs @e2b how are you handling observability wrt token usage within sessions? I have tracking tool calls and thinking traces down, but i cant for the life of me build a "/context" type of view that is reliable
> 
> the SDK is awesome though, i love inserting variables into the system prompt

> [!tip]+ :leftwards_arrow_with_hook: @mckaywrigley · Wed Dec 31 15:03:15 +0000 2025

> @cmgrant0 @stnkvcs this is a pretty good guide if for some reason you haven't seen it yet.
> 
> i do think they could improve the observability stuff though (and i anticipate they will!).
> https://t.co/K49XDZavrX
>
> :paperclip: **[platform.claude.com/docs/en/agent-sdk/cost-tracking](https://platform.claude.com/docs/en/agent-sdk/cost-tracking)** — Detailed documentation for tracking token usage and costs in Claude Agent SDK. Explains step/message concepts, usage deduplication by message ID, and provides implementation examples for building cost tracking systems and billing dashboards with proper handling of parallel tool uses and cache tokens.

> [!reply] @sean_infinnerty · Wed Dec 31 15:24:09 +0000 2025
> @mckaywrigley @stnkvcs @e2b Is it possible to use a Claude Code 20x Max subscription when running custom agents using the SDK in a hosted sandbox for personal use?
> 
> I can generate an OAuth token for using the SDK locally, but I'm trying to understand if this can be done using something like e2b?

> [!tip]+ :leftwards_arrow_with_hook: @mckaywrigley · Wed Dec 31 15:29:32 +0000 2025

> @sean_infinnerty @stnkvcs yes. you’ll just need to store the token and feed it to the sandbox.
> 
> something tells me they’ll do away with this sooner than later though haha.


---

> [!metrics]- Engagement & Metadata
> **Likes:** 296 · **Replies:** 12 · **Reposts:** 17 · **Views:** 18,894
> **Engagement Score:** 1,346
>
> **Source:** tips · **Quality:** 9/10
> **Curated:** ✓ · **Reply:** ✓
> **ID:** [2006377570485543329](https://x.com/mckaywrigley/status/2006377570485543329)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ✅ (5/5 summarized)
  media: ℹ️ none
  thread: ✅ (18 replies scraped)
  classification: ❌ not classified
```