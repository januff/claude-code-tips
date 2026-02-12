---
tweet_id: "2007516621825552416"
created: 2026-01-03
author: "@housecor"
display_name: "Cory House"
primary_keyword: "Chrome DevTools MCP"
llm_category: "tooling"
tags:
  - type/thread
likes: 424
views: 48171
engagement_score: 444
url: "https://x.com/housecor/status/2007516621825552416"
enrichment_complete: true
has_media: false
has_links: false
has_thread_context: true
---

> [!tweet] @housecor · Jan 03, 2026
> Problem: I want Claude to use Chrome.
> 
> Solution: Here's 3 options and when I use each:
> 
> 1. Playwright MCP – Use as primary cross-browser testing tool
> 
> 2. Chrome DevTools MCP – Perf analysis / network debugging
> 
> 3. Official Claude Chrome extension – Quick logged-in checks
>
> Likes: 424 · Replies: 39 · Reposts: 10

## Summary

This tip provides three methods for interacting with Claude within the Chrome browser. It suggests using Playwright for cross-browser testing, Chrome DevTools for performance analysis and network debugging, and the official Claude Chrome extension for quick checks while logged in. By choosing the right tool based on the task, users can optimize their workflow when working with Claude and Chrome.

## Keywords

**Primary:** `Chrome DevTools MCP` · Playwright MCP, Claude Chrome extension, cross-browser testing, perf analysis, network debugging
## Replies

> [!reply] @pk_iv · Mon Dec 29 17:35:07 +0000 2025
> I spent all of Christmas reverse engineering Claude Chrome so it would work with remote browsers. 
> 
> Here's how Anthropic taught Claude how to browse the web (1/7) https://t.co/kBJA1DUWxA
> *2271 likes*

> [!reply] @smerchek · Sat Jan 03 18:25:33 +0000 2026
> @housecor I'd recommend the dev-browser skill to replace the playwright MCP. Seems to work just as well without context bloat: https://t.co/44R8ajxUOb
> *61 likes*

> [!tip]+ :leftwards_arrow_with_hook: @housecor · Sat Jan 03 18:37:37 +0000 2026

> @smerchek Nice timing - Just found that repo an hour ago! Eager to try

> [!reply] @mattsichterman · Sat Jan 03 21:07:59 +0000 2026
> @housecor Lock in to https://t.co/n4jDINxUkH
> *14 likes*

> [!tip]+ :leftwards_arrow_with_hook: @housecor · Sat Jan 03 21:19:33 +0000 2026

> @mattsichterman Yep, someone else mentioned too

> [!reply] @davidfano · Sat Jan 03 21:43:15 +0000 2026
> @housecor Just found playwriter and it’s pretty cool.
> *5 likes*

> [!tip]+ :leftwards_arrow_with_hook: @housecor · Sat Jan 03 22:50:12 +0000 2026

> @davidfano yep multiple people mentioned. Eager to try

> [!reply] @pk_iv · Sun Jan 04 13:12:21 +0000 2026
> @housecor If you're running on a VPS and don't have access to chrome, you can always use this: https://t.co/4BFmOjulpZ
> *3 likes*

> [!reply] @annanidev · Sat Jan 03 19:25:51 +0000 2026
> @housecor DevTools MCP is killer for catching those hidden bottlenecks that regular testing completely misses.
> *3 likes*

> [!reply] @TendiesOfWisdom · Sat Jan 03 22:04:20 +0000 2026
> @housecor Do you spin these up as subagents to protect the main context window (since they eat tokens)?
> *1 likes*

> [!tip]+ :leftwards_arrow_with_hook: @housecor · Sat Jan 03 22:50:54 +0000 2026

> @TendiesOfWisdom Using a subagent still uses the same number of tokens, right? 
> 
> Perhaps I'm misunderstanding you?

> [!reply] @decruz · Sun Jan 04 03:23:00 +0000 2026
> @housecor This is the solution:
> https://t.co/WoXSeawLyf
> *1 likes*

> [!tip]+ :leftwards_arrow_with_hook: @housecor · Sun Jan 04 13:58:54 +0000 2026

> @decruz Yep, many people suggested

> [!reply] @shipitniko · Sat Jan 03 20:48:53 +0000 2026
> Feels like a quiet turning point where the browser stops being a UI for humans and starts being an API for agents
> 
> Today it is cross browser tests and perf checks
> Tomorrow it is describe the bug in plain English and an agent opens Chrome, reproduces it, profiles it, and attaches a full report to your ticket automatically
> *1 likes*

> [!reply] @sughanthans1 · Sat Jan 03 21:16:08 +0000 2026
> @housecor playwriter is also an option (note: not playwright)
> *1 likes*


---

> [!metrics]- Engagement & Metadata
> **Likes:** 424 · **Replies:** 39 · **Reposts:** 10 · **Views:** 48,171
> **Engagement Score:** 444
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2007516621825552416](https://x.com/housecor/status/2007516621825552416)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ℹ️ none
  thread: ✅ (33 replies scraped)
  classification: ❌ not classified
```