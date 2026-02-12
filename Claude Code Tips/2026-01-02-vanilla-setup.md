---
tweet_id: "2007179832300581177"
created: 2026-01-02
author: "@bcherny"
display_name: "Boris Cherny"
primary_keyword: "vanilla-setup"
llm_category: "meta"
tags:
  - type/thread
likes: 45567
views: 6050468
engagement_score: 56527
url: "https://x.com/bcherny/status/2007179832300581177"
enrichment_complete: true
has_media: false
has_links: false
has_thread_context: true
---

> [!tweet] @bcherny · Jan 02, 2026
> I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit.
> 
> My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to use Claude Code: we intentionally build it in a way that you can use it, customize it, and hack it however you like. Each person on the Claude Code team uses it very differently.
> 
> So, here goes.
>
> ---
> *@bcherny · Fri Jan 02 19:59:05 +0000 2026:*
> 13/ A final tip: probably the most important thing to get great results out of Claude Code -- give Claude a way to verify its work. If Claude has that feedback loop, it will 2-3x the quality of the final result.
> 
> Claude tests every single change I land to https://t.co/pEWPQoSq5t using the Claude Chrome extension. It opens a browser, tests the UI, and iterates until the code works and the UX feels good.
> 
> Verification looks different for each domain. It might be as simple as running a bash command, or running a test suite, or testing the app in a browser or phone simulator. Make sure to invest in making this rock-solid.
> 
> https://t.co/m7wwQUmp1C
>
> ---
> *@bcherny · Fri Jan 02 19:58:58 +0000 2026:*
> 1/ I run 5 Claudes in parallel in my terminal. I number my tabs 1-5, and use system notifications to know when a Claude needs input https://t.co/nmRJ5km3oZ https://t.co/CJaX1rUgiH
>
> ---
> *@bcherny · Fri Jan 02 19:58:59 +0000 2026:*
> 3/ I use Opus 4.5 with thinking for everything. It's the best coding model I've ever used, and even though it's bigger &amp; slower than Sonnet, since you have to steer it less and it's better at tool use, it is almost always faster than using a smaller model in the end.
>
> ---
> *@bcherny · Fri Jan 02 19:59:05 +0000 2026:*
> I hope this was helpful! What are your tips for using Claude Code? What do you want to hear about next?
>
> ---
> *@bcherny · Fri Jan 02 19:59:00 +0000 2026:*
> 4/ Our team shares a single https://t.co/pp5TJkWmFE for the Claude Code repo. We check it into git, and the whole team contributes multiple times a week. Anytime we see Claude do something incorrectly we add it to the https://t.co/pp5TJkWmFE, so Claude knows not to do it next time.
> 
> Other teams maintain their own https://t.co/pp5TJkWmFE's. It is each team's job to keep theirs up to date.
>
> ---
> *@bcherny · Fri Jan 02 19:59:01 +0000 2026:*
> 6/ Most sessions start in Plan mode (shift+tab twice). If my goal is to write a Pull Request, I will use Plan mode, and go back and forth with Claude until I like its plan. From there, I switch into auto-accept edits mode and Claude can usually 1-shot it. A good plan is really important!
>
> ---
> *@bcherny · Fri Jan 02 19:59:02 +0000 2026:*
> 8/ I use a few subagents regularly: code-simplifier simplifies the code after Claude is done working, verify-app has detailed instructions for testing Claude Code end to end, and so on. Similar to slash commands, I think of subagents as automating the most common workflows that I do for most PRs.
> 
> https://t.co/s2p4ZXREOi
>
> ---
> *@bcherny · Fri Jan 02 19:58:59 +0000 2026:*
> 2/ I also run 5-10 Claudes on https://t.co/pEWPQoSq5t, in parallel with my local Claudes. As I code in my terminal, I will often hand off local sessions to web (using &), or manually kick off sessions in Chrome, and sometimes I will --teleport back and forth. I also start a few sessions from my phone (from the Claude iOS app) every morning and throughout the day, and check in on them later.
>
> ---
> *@bcherny · Fri Jan 02 19:59:00 +0000 2026:*
> 5/ During code review, I will often tag @.claude on my coworkers' PRs to add something to the https://t.co/v4FOLUBHz9 as part of the PR. We use the Claude Code Github action (/install-github-action) for this. It's our version of @danshipper's Compounding Engineering https://t.co/VIQYZ2hFq5
>
> ---
> *@bcherny · Fri Jan 02 19:59:03 +0000 2026:*
> 10/ I don't use --dangerously-skip-permissions. Instead, I use /permissions to pre-allow common bash commands that I know are safe in my environment, to avoid unnecessary permission prompts. Most of these are checked into .claude/settings.json and shared with the team. https://t.co/T5h0TkND4W
>
> ---
> *@bcherny · Fri Jan 02 19:59:02 +0000 2026:*
> 7/ I use slash commands for every "inner loop" workflow that I end up doing many times a day. This saves me from repeated prompting, and makes it so Claude can use these workflows, too. Commands are checked into git and live in .claude/commands/.
> 
> For example, Claude and I use a /commit-push-pr slash command dozens of times every day. The command uses inline bash to pre-compute git status and a few other pieces of info to make the command run quickly and avoid back-and-forth with the model (https://t.co/4jZ7RK0suT)
>
> ---
> *@bcherny · Fri Jan 02 19:59:02 +0000 2026:*
> 9/ We use a PostToolUse hook to format Claude's code. Claude usually generates well-formatted code out of the box, and the hook handles the last 10% to avoid formatting errors in CI later. https://t.co/XBMG5fmK4P
>
> ---
> *@bcherny · Fri Jan 02 19:59:04 +0000 2026:*
> 12/ For very long-running tasks, I will either (a) prompt Claude to verify its work with a background agent when it's done, (b) use an agent Stop hook to do that more deterministically, or (c) use the ralph-wiggum plugin (originally dreamt up by @GeoffreyHuntley). I will also use either --permission-mode=dontAsk or --dangerously-skip-permissions in a sandbox to avoid permission prompts for the session, so Claude can cook without being blocked on me.
> 
> https://t.co/floA4sI7FR
> 
> https://t.co/klOPZPPgIU
>
> ---
> *@bcherny · Fri Jan 02 19:59:03 +0000 2026:*
> 11/ Claude Code uses all my tools for me. It often searches and posts to Slack (via the MCP server), runs BigQuery queries to answer analytics questions (using bq CLI), grabs error logs from Sentry, etc. The Slack MCP configuration is checked into our .mcp.json and shared with the team.
>
> Likes: 45,567 · Replies: 1,065 · Reposts: 5,480

## Summary

Claude Code creator Boris shares his surprisingly simple, out-of-the-box setup as an example, emphasizing that there's no single "right" way to use the tool. The key takeaway is Claude Code's adaptability; it's designed to be customized and hacked to fit individual workflows, as demonstrated by the diverse usage within the Claude Code team itself. This highlights the flexibility and user-centric approach to Claude Code's design.

## Keywords

**Primary:** `vanilla-setup` · default configuration, out-of-the-box, customization, personal setup
## Replies

> [!reply] @MikeKhristo · Fri Jan 02 22:00:09 +0000 2026
> @bcherny dude i thought you could be trusted, but light mode in terminal?
> *400 likes*

> [!tip]+ :leftwards_arrow_with_hook: @bcherny · Fri Jan 02 22:08:57 +0000 2026

> @MikeKhristo Engineers literally stop by my desk to make fun of me

> [!reply] @muxin_li · Fri Jan 02 21:55:39 +0000 2026
> @bcherny This is great! Would you consider recording a screen share (just the setup) for us visual learners?
> *63 likes*

> [!tip]+ :leftwards_arrow_with_hook: @bcherny · Fri Jan 02 22:24:06 +0000 2026

> @muxin_li Cool idea!

> [!reply] @kadokaelan · Fri Jan 02 20:47:13 +0000 2026
> no mention of skills? 👀 i wrote a collection of skills that seem useful but unclear if cc actually references or uses them. was hoping to be able to slim down my claude md in favor of skills but at same time my team uses many different coding agents so team relies on https://t.co/OZ66okpmzM
> *42 likes*

> [!tip]+ :leftwards_arrow_with_hook: @bcherny · Fri Jan 02 21:19:45 +0000 2026

> @kadokaelan Skills = slash commands, I use them interchangeably

> [!reply] @ianpatrickhines · Fri Jan 02 20:04:00 +0000 2026
> @bcherny this is an absolute goldmine
> 
> 10 concurrent claudes?
> 
> are they working in the same repo? or on different projects?
> *41 likes*

> [!tip]+ :leftwards_arrow_with_hook: @bcherny · Fri Jan 02 20:05:23 +0000 2026

> @ianpatrickhines Usually the same repo, but sometimes different repos

> [!reply] @DeeperThrill · Fri Jan 02 21:20:50 +0000 2026
> @bcherny Claude seems to suggest that when there are over some number of characters in Claude .md it doesn’t do well (40k I think?).
> 
> How big is your Claude markdown file, and is it used for coding style, general coding principles, specific ways you work, commands, or other stuff?
> *27 likes*

> [!tip]+ :leftwards_arrow_with_hook: @bcherny · Fri Jan 02 22:08:14 +0000 2026

> @DeeperThrill Our checked in https://t.co/v4FOLUBHz9 is 2.5k tokens. It covers:
> 
> - common bash commands 
> - code style conventions
> - ui and content design guidelines
> - how to do state management, logging, error handling, gating, and debugging 
> - pull request template

> [!reply] @leozc · Fri Jan 02 22:05:25 +0000 2026
> @bcherny How would you share “skills” to your team while keeping some skills personal? What is the workflow
> *20 likes*

> [!tip]+ :leftwards_arrow_with_hook: @bcherny · Fri Jan 02 22:10:26 +0000 2026

> @leozc There are four directories you can put skills in depending what you want. https://t.co/ZfbA7Yf5hN

> [!reply] @intro · Fri Jan 02 17:34:00 +0000 2026
> Meet Intro, advisors for your business, on-demand.
> 
>  - Access to 1K+ founders &amp; execs
>  - Business advice via 1:1 video calls
>  - Businesses are seeing real ROIs
> 
> Our experts —&gt; Founder of Reddit ($10B), Founder of Zillow ($12B), Founder of Sweetgreen ($4B) and 1000+ more
> *19 likes*

> [!reply] @iirfan · Fri Jan 02 20:16:32 +0000 2026
> @bcherny can we ever expect a claude code linear integration
> *12 likes*

> [!tip]+ :leftwards_arrow_with_hook: @bcherny · Fri Jan 02 22:11:52 +0000 2026

> @iirfan This exists! https://t.co/eWDDFsNPnN

> [!reply] @chansearrington · Fri Jan 02 21:28:58 +0000 2026
> @bcherny I have so many questions lol
> 
> How are you handing off from terminal TO web?
> 
> Any tips for having more “natively integrated” CLI tools? Or do they always have to go through bash to be called?
> 
> How are you getting https://t.co/02XJTsAjNR to work with Claude in chrome?
> *5 likes*

> [!tip]+ :leftwards_arrow_with_hook: @bcherny · Fri Jan 02 22:27:44 +0000 2026

> @chansearrington - Terminal =&gt; web: use &amp; to teleport the session
> - Native CLI tools: either bash or MCP works great, don't overthink it
> - https://t.co/XJ8WxOxjo0 + Claude in chrome: you have to --teleport the session locally first, for now


---

> [!metrics]- Engagement & Metadata
> **Likes:** 45,567 · **Replies:** 1,065 · **Reposts:** 5,480 · **Views:** 6,050,468
> **Engagement Score:** 56,527
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2007179832300581177](https://x.com/bcherny/status/2007179832300581177)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ℹ️ none
  thread: ✅ (17 replies scraped)
  classification: ❌ not classified
```