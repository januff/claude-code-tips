---
created: 2026-01-10
author: "@jarrodwatts"
display_name: "Jarrod Watts"
tags:
  - type/screenshot
  - type/thread
likes: 1897
views: 159457
engagement_score: 7677
url: "https://x.com/jarrodwatts/status/2009963629500870977"
---

> [!tweet] @jarrodwatts · Jan 10, 2026
> Introducing Claude Delegator!
> 
> A Claude Code plugin that lets you use GPT 5.2 powered subagents directly within Claude Code.
> 
> Ask GPT 5.2 (via codex) to architect your code, perform security audits, or make any other changes to your codebase.
> 
> Easy installation guide below ↓ https://t.co/9Wf0OX2399
>
> ---
> *@jarrodwatts · 2026-01-10T12:22:05+00:00:*
> · Add the marketplace 
> /plugin marketplace add jarrodwatts/claude-delegator
> 
> · Install the plugin 
> /plugin install claude-delegator
> 
> · Run the setup:
>  /claude-delegator:setup
> 
> Github: https://t.co/oyAArFUG3n
>
> Likes: 1,897 · Replies: 98 · Reposts: 149

## Summary

The Claude Delegator plugin enhances Claude Code by integrating GPT 5.2-powered subagents (accessible via Codex). This allows users to leverage GPT's capabilities, such as code architecture design and security audits, directly within their Claude Code environment. The key insight is using GPT as a powerful assistant for code-related tasks from within the Claude interface. Installation instructions are available in the linked resource.

## Media

![Media](https://pbs.twimg.com/media/G-TSIExasAMoaVT.jpg)







## Replies

> [!reply] @_colemurray · 2026-01-10T18:26:16+00:00
> @jarrodwatts very cool!
> 
> i applaud the hustle as well 🤣 https://t.co/fgz5PCxaBC
> *47 likes*

> [!tip]+ ↩️ @jarrodwatts · 2026-01-10T21:41:29+00:00

> @_colemurray got this idea from oh my opencode as well - thought it was really cool that after a successful install i could star it right there within the terminal

> [!reply] @stableAPY · 2026-01-10T14:46:55+00:00
> @jarrodwatts I already love it! 
> 
> way easier to call GPT 5.2 inside CC than spawning a codex cli
> *10 likes*

> [!tip]+ ↩️ @jarrodwatts · 2026-01-11T03:33:20+00:00

> @stableAPY glad you like it!

> [!reply] @AleksaMiti1 · 2026-01-10T12:37:09+00:00
> @jarrodwatts Pretty cool!
> 
> What is the reason behind it?
> *5 likes*

> [!tip]+ ↩️ @jarrodwatts · 2026-01-10T12:42:25+00:00

> @AleksaMiti1 Codex is better at things like architecture and code reviews from my experience.
> 
> In opencode, you can have subagents that use any model - i wanted to try build something like that inside of claude code
> 
> This one just has codex for now, but can easily be extended to others too

> [!reply] @LLMJunky · 2026-01-11T00:05:33+00:00
> @jarrodwatts tell your wife that you made it https://t.co/qSEAJX8nwz
> *3 likes*

> [!tip]+ ↩️ @jarrodwatts · 2026-01-11T00:16:13+00:00

> @LLMJunky Gotta let her know we’re done now
> 
> (i let the fame get to my head)

> [!reply] @anshnanda · 2026-01-10T14:26:46+00:00
> @jarrodwatts Does it use Codex CLI to delegate the agents?
> *2 likes*

> [!tip]+ ↩️ @jarrodwatts · 2026-01-10T20:39:49+00:00

> @anshnanda Yes  it does, it calls codex via MCP

> [!reply] @joelreymont · 2026-01-10T19:38:49+00:00
> @jarrodwatts This is literally 1 prompt. 
> 
> Ask Claude Code to create an oracle skill which will invoke Codex with your prompt. 
> 
> That’s it!
> *2 likes*

> [!tip]+ ↩️ @jarrodwatts · 2026-01-11T03:39:09+00:00

> @joelreymont the plugin is a bit more in-depth than that; check through the github if you're interested

> [!reply] @anshnanda · 2026-01-10T14:26:22+00:00
> @jarrodwatts This is cool.
> *1 likes*

> [!tip]+ ↩️ @jarrodwatts · 2026-01-11T03:39:28+00:00

> @anshnanda 🫡

> [!reply] @im_benhur · 2026-01-10T20:09:18+00:00
> @jarrodwatts Very keen to try this out; as a newbie here, could you help me set one up for Gemini 3.0 as well? I’m thinking like how @0xSisyphus labs did it with their plugin - use Gemini flash for documentation so you can delegate different tasks based on the nature of it
> *1 likes*

> [!tip]+ ↩️ @jarrodwatts · 2026-01-10T21:46:54+00:00

> @im_benhur @0xSisyphus that's the idea, would like to expand it to other agents and hopefully for local llms too
> 
> was hoping to get gemini supported out of the box but don't think their cli has an mcp option like codex does

> [!reply] @Barthazian · 2026-01-10T14:54:21+00:00
> @jarrodwatts does all the claude harness wokr on the gpt agent?

> [!tip]+ ↩️ @jarrodwatts · 2026-01-11T03:32:57+00:00

> @Barthazian it's inside the codex harness - the plugin in simple terms is really just letting claude run "codex &lt;prompt&gt; with some pre-made system prompts &amp; guides on when it should do that

> [!reply] @realKonark · 2026-01-10T21:35:06+00:00
> @jarrodwatts Can you resume codex agents from the MCP now? Last I checked you couldn’t

> [!tip]+ ↩️ @jarrodwatts · 2026-01-10T21:42:52+00:00

> @realKonark There is meant to be a codex-reply feature to continue a thread but i (claude) couldn't figure out how to make it work for v1, so currently its a fresh thread every delegation

> [!reply] @aaronbatilo · 2026-01-10T15:10:33+00:00
> @jarrodwatts Why not the codex MCP?

> [!tip]+ ↩️ @jarrodwatts · 2026-01-10T20:42:17+00:00

> @aaronbatilo It is using the codex mcp!
> 
> It packages up that &amp; some useful prompts &amp; delegation rules together to make it easy to use

> [!reply] @CodingWorkflow · 2026-01-11T03:10:14+00:00
> @jarrodwatts Why do you need a plugin when you can use a simple command: 
> claude mcp add codex mcp-server
> Surprised you need more!

> [!tip]+ ↩️ @jarrodwatts · 2026-01-11T03:40:17+00:00

> @CodingWorkflow its packaged up with some helpful rules, pre-made codex prompts and some other nice-to-haves that make it better than just raw dogging the mcp


> [!metrics]- Engagement & Metadata
> **Likes:** 1,897 · **Replies:** 98 · **Reposts:** 149 · **Views:** 159,457
> **Engagement Score:** 7,677
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2009963629500870977](https://x.com/jarrodwatts/status/2009963629500870977)