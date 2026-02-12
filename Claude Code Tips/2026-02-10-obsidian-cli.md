---
tweet_id: "2021251878521073847"
created: 2026-02-10
author: "@kepano"
display_name: "kepano"
primary_keyword: "Obsidian CLI"
llm_category: "tooling"
classification: "ACT_NOW"
tags:
  - type/thread
likes: 4155
views: 312204
engagement_score: 10693
url: "https://x.com/kepano/status/2021251878521073847"
enrichment_complete: true
has_media: false
has_links: false
has_thread_context: true
---

> [!tweet] @kepano · Feb 10, 2026
> 1. install Obsidian 1.12
> 2. enable CLI
> 3. now OpenClaw, OpenCode, Claude Code, Codex, or any other agent can use Obsidian
>
> ---
> *@kepano · 2026-02-10T17:40:31+00:00:*
> Obsidian uses local files, so all your standard terminal commands work for editing/moving/searching files
> 
> what Obsidian CLI adds is everything else:
> 
> - interacting with the UI
> - Obsidian's internal functions, e.g. base queries
> - deterministic results like the "orphans" command
> - easily one-shot a personal plugin, now that your agent can access devtools, console, screenshots, eval, etc
> 
> See the docs:
> https://t.co/2huInNV7ac
>
> Likes: 4,155 · Replies: 138 · Reposts: 316

## Summary

This tip enables Obsidian integration with AI agents like Claude Code by leveraging Obsidian's command-line interface (CLI). By installing Obsidian 1.12 and enabling the CLI, agents can now interact with and utilize Obsidian for tasks. This allows for automated workflows and integration of your notes with external tools and processes.

## Keywords

**Primary:** `Obsidian CLI` · Obsidian, CLI, OpenClaw, OpenCode, agent
## Classification

**ACT_NOW** — High engagement (4155 likes) + directly relevant to active workflow
## Replies

> [!reply] @obsdmd · 2026-02-10T15:14:33+00:00
> Anything you can do in Obsidian you can do from the command line.
> 
> Obsidian CLI is now available in 1.12 (early access). https://t.co/B8ed2zrWHe
> *13661 likes*

> [!reply] @sadjikun · 2026-02-10T16:31:48+00:00
> @kepano actually you can use claude code with obsidian even without having to enable cli. 
> 
> just directly in your terminal. all files are accessible in your folder through agentic search of claude code. 
> im doing this since a while now.
> *19 likes*

> [!tip]+ :leftwards_arrow_with_hook: @kepano · 2026-02-10T16:39:28+00:00

> @sadjikun indeed, you can already do a lot just by working with files directly
> 
> Obsidian CLI is mainly focused on things you can't do that way, e.g. interacting with UI itself and tools for plugin development
> https://t.co/sc36GWM9oQ

> [!reply] @omarsar0 · 2026-02-10T17:15:10+00:00
> Very cool. I was already using Claude Code native tools to search and write to my Obsidian vaults but I like that this comes with native Obsidian functionality. I need to check out the features but any high level thoughts on the advantages of using this Obsidian CLI over direct access with the coding agent?
> *16 likes*

> [!tip]+ :leftwards_arrow_with_hook: @kepano · 2026-02-10T17:27:24+00:00

> @omarsar0 the CLI commands are complementary to existing terminal commands, see the docs
> 
> they do entirely different things (like plugin development tools), or deterministically + quickly retrieve info e.g. the "orphans" command is instant
> https://t.co/sc36GWMHeo

> [!reply] @gldgab · 2026-02-10T16:38:37+00:00
> @kepano Actually you don’t need Obsidian CLI to use OpenCode, Claude, or Codex.
> Just:
> 
> `cd ~/your-vault &amp;&amp; opencode|codex|copilot|other`
> *12 likes*

> [!tip]+ :leftwards_arrow_with_hook: @kepano · 2026-02-10T16:41:11+00:00

> @gldgab yes, except this lets you directly control the Obsidian UI, access devtools, do things like reload plugins, run base queries, etc
> 
> https://t.co/sc36GWM9oQ

> [!reply] @k_sharovarskyi · 2026-02-10T16:41:46+00:00
> @kepano It would be nice to have a headless cli to use on a VPS, e.g. to trigger obsidian sync. Currently, you need to install the gui version to have access to the cli
> *11 likes*

> [!tip]+ :leftwards_arrow_with_hook: @kepano · 2026-02-10T16:45:12+00:00

> @k_sharovarskyi yes

> [!reply] @renasci_michael · 2026-02-10T16:36:49+00:00
> @kepano It’s not headless so I do think this change anything
> *3 likes*

> [!tip]+ :leftwards_arrow_with_hook: @kepano · 2026-02-10T16:42:55+00:00

> @renasci_michael at minimum it radically improves plugin development because now you can do full round-tripping, including getting console logs, screenshots, run eval, etc

> [!reply] @Webhead24 · 2026-02-10T17:06:10+00:00
> @kepano Any benefit over using Notion?
> *3 likes*

> [!tip]+ :leftwards_arrow_with_hook: @kepano · 2026-02-10T17:21:49+00:00

> @Webhead24 - fast
> - free for personal use
> - all local plain text files that you own, no lock-in
> - works offline by default
> - end-to-end encrypted sync
> - extensible with plugins and themes
> - 100% user-supported
> 
> https://t.co/zcySDZGirM

> [!reply] @dvirtualshivam · 2026-02-10T17:15:31+00:00
> @kepano who would you want an agent to use obsidian?
> *2 likes*

> [!tip]+ :leftwards_arrow_with_hook: @kepano · 2026-02-10T17:46:23+00:00

> @dvirtualshivam now you can much more easily make a personal Obsidian plugin

> [!reply] @shuvro · 2026-02-10T16:49:08+00:00
> @kepano Amazing. But could you list some CLI workflows that enable it?
> 
> Otherwise, all the files are stored in a folder, and agents can read them normally.
> 
> Maybe it would be better to add some workflow examples that are only achievable via CLI?
> *1 likes*

> [!tip]+ :leftwards_arrow_with_hook: @kepano · 2026-02-10T16:54:59+00:00

> @shuvro you can find those here:
> https://t.co/sc36GWM9oQ

> [!reply] @shaped · 2026-02-10T21:47:23+00:00
> @kepano This is amazing
> Now all I need is a CLI dataview implementation which lets my agent see my notes as I see them
> *1 likes*

> [!tip]+ :leftwards_arrow_with_hook: @kepano · 2026-02-10T21:49:35+00:00

> @shaped Obsidian CLI already supports bases and you can convert dataview queries to bases queries fairly easily


---

> [!metrics]- Engagement & Metadata
> **Likes:** 4,155 · **Replies:** 138 · **Reposts:** 316 · **Views:** 312,204
> **Engagement Score:** 10,693
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2021251878521073847](https://x.com/kepano/status/2021251878521073847)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ℹ️ none
  thread: ✅ (28 replies scraped)
  classification: ✅ ACT_NOW
```