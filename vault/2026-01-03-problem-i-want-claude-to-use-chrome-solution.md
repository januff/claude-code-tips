---
created: 2026-01-03
author: "@housecor"
display_name: "Cory House"
tags:
  - type/thread
likes: 424
views: 48171
engagement_score: 444
url: "https://x.com/housecor/status/2007516621825552416"
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

## Replies

> [!reply] @pk_iv · Mon Dec 29 17:35:07 +0000 2025
> I spent all of Christmas reverse engineering Claude Chrome so it would work with remote browsers. 
> 
> Here's how Anthropic taught Claude how to browse the web (1/7) https://t.co/kBJA1DUWxA
> *2271 likes*

> [!reply] @smerchek · Sat Jan 03 18:25:33 +0000 2026
> @housecor I'd recommend the dev-browser skill to replace the playwright MCP. Seems to work just as well without context bloat: https://t.co/44R8ajxUOb
> *61 likes*

> [!reply] @mattsichterman · Sat Jan 03 21:07:59 +0000 2026
> @housecor Lock in to https://t.co/n4jDINxUkH
> *14 likes*

> [!reply] @housecor · Sat Jan 03 21:31:47 +0000 2026
> @YakutKhon Playwright MCP works cross-browser, uses the accessibility tree, and has a headless mode. 
> 
> But both have their tradeoffs.
> 
> Details here: https://t.co/89hj3ft7kc
> *6 likes*

> [!reply] @davidfano · Sat Jan 03 21:43:15 +0000 2026
> @housecor Just found playwriter and it’s pretty cool.
> *5 likes*

> [!reply] @housecor · Sat Jan 03 21:13:23 +0000 2026
> @ntkris Yes I tell it to
> *4 likes*

> [!reply] @housecor · Sat Jan 03 18:37:37 +0000 2026
> @smerchek Nice timing - Just found that repo an hour ago! Eager to try
> *3 likes*

> [!reply] @pk_iv · Sun Jan 04 13:12:21 +0000 2026
> @housecor If you're running on a VPS and don't have access to chrome, you can always use this: https://t.co/4BFmOjulpZ
> *3 likes*

> [!reply] @annanidev · Sat Jan 03 19:25:51 +0000 2026
> @housecor DevTools MCP is killer for catching those hidden bottlenecks that regular testing completely misses.
> *3 likes*

> [!reply] @housecor · Sat Jan 03 22:50:12 +0000 2026
> @davidfano yep multiple people mentioned. Eager to try
> *2 likes*

> [!reply] @housecor · Sat Jan 03 22:50:54 +0000 2026
> @TendiesOfWisdom Using a subagent still uses the same number of tokens, right? 
> 
> Perhaps I'm misunderstanding you?
> *2 likes*

> [!reply] @housecor · Sat Jan 03 21:19:33 +0000 2026
> @mattsichterman Yep, someone else mentioned too
> *1 likes*

> [!reply] @housecor · Sun Jan 04 16:27:39 +0000 2026
> @mattarderne Haven’t hit that
> *1 likes*

> [!reply] @TendiesOfWisdom · Sat Jan 03 22:04:20 +0000 2026
> @housecor Do you spin these up as subagents to protect the main context window (since they eat tokens)?
> *1 likes*

> [!reply] @decruz · Sun Jan 04 03:23:00 +0000 2026
> @housecor This is the solution:
> https://t.co/WoXSeawLyf
> *1 likes*

> [!reply] @housecor · Sun Jan 04 13:58:54 +0000 2026
> @decruz Yep, many people suggested
> *1 likes*

> [!reply] @shipitniko · Sat Jan 03 20:48:53 +0000 2026
> Feels like a quiet turning point where the browser stops being a UI for humans and starts being an API for agents
> 
> Today it is cross browser tests and perf checks
> Tomorrow it is describe the bug in plain English and an agent opens Chrome, reproduces it, profiles it, and attaches a full report to your ticket automatically
> *1 likes*

> [!reply] @sughanthans1 · Sat Jan 03 21:16:08 +0000 2026
> @housecor playwriter is also an option (note: not playwright)
> *1 likes*

> [!reply] @AbdMuizAdeyemo · Sat Jan 03 20:10:32 +0000 2026
> @housecor Clean breakdown.
> 
> Claude + Chrome isn’t one-size-fits-all.
> 
> Playwright for testing, DevTools for debugging, extension for quick checks.
> 
> Pick the tool to fit the task, not the other way around.
> *1 likes*

> [!reply] @ntkris · Sat Jan 03 19:59:27 +0000 2026
> @housecor Have you found a way to have it test its own changes via one of these tools? Changes via claude code I mean

> [!reply] @mattarderne · Sun Jan 04 16:00:15 +0000 2026
> @housecor What do you do when Plawright is getting locked out by cloudflare?

> [!reply] @YakutKhon · Sat Jan 03 20:12:45 +0000 2026
> @housecor Why do you rate Playwright higher than Claude Chrome extension? Isn't it harder to setup than to teach Claude Chrome? Granted it's a bit slow today, but so much easier to use and make changes

> [!reply] @nnnnicholas · Sat Jan 03 21:55:58 +0000 2026
> @housecor have you tried having claude extension do research using other ai tools? this is where i’m headed. no more copy pasting between 5 ai apps to get a pro research synthesis

> [!reply] @ashleybchae · Sun Jan 04 08:36:39 +0000 2026
> @housecor Yeah, “claude —chrome” is pretty good

> [!reply] @EphraimDuncan_ · Sun Jan 04 18:22:32 +0000 2026
> @housecor try playwriter, it’s very good and easy to setup and doesn’t use a lot of memory

> [!reply] @bitdeep_ · Sun Jan 04 13:19:09 +0000 2026
> (1) & (3) not usable.
> (2) need to be isolated, headless and use chrome unstable: 
> 
> [mcp_servers.chrome-devtools]
> command = "npx"
> args = ["-y", "chrome-devtools-mcp@latest", "--headless", "--isolated", "--executablePath", "/usr/bin/google-chrome-unstable"]
> 
> or it get locked and mess  your profiles, this way, it can test for hours.

> [!reply] @mtrajan · Sun Jan 04 13:48:11 +0000 2026
> @housecor I had expected the chrome plugin to be the first option, not there yet.

> [!reply] @Niyxuis · Sun Jan 04 08:37:28 +0000 2026
> @housecor the "use each" part is the whole game - most posts just list options, but knowing when to reach for which one cuts the decision paralysis in half

> [!reply] @jensenloke · Sun Jan 04 12:04:07 +0000 2026
> @housecor I do the same. But I think Claude in chrome can do similar things to chrome dev tools. It’s not as customizable as playwright! 
> 
> I’m trying to default to Claude in chrome for most.

> [!reply] @buildwithparas · Sat Jan 03 20:00:55 +0000 2026
> @housecor been sleeping on 1 and 2 apparently. extension handles everything i throw at it so far

> [!reply] @a_kmrx · Sun Jan 04 15:00:42 +0000 2026
> @housecor Waiting for the day Claude asks Chrome for permission to debug itself.

> [!reply] @yuanhao · Sat Jan 03 20:36:57 +0000 2026
> @housecor Playwright MCP and Chrome DevTools MCP are very slow. The Claude Chrome extension has its limitations.

> [!reply] @jonvolio · Sun Jan 04 00:50:31 +0000 2026
> @housecor Got some issues with official one aswell, did you try it? Wich one is the best overall ?


> [!metrics]- Engagement & Metadata
> **Likes:** 424 · **Replies:** 39 · **Reposts:** 10 · **Views:** 48,171
> **Engagement Score:** 444
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2007516621825552416](https://x.com/housecor/status/2007516621825552416)