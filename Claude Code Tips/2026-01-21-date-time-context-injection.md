---
tweet_id: "2013820793671536778"
created: 2026-01-21
author: "@alexhillman"
display_name: "📙 Alex Hillman"
primary_keyword: "date-time-context-injection"
llm_category: "context-management"
classification: "ACT_NOW"
tags:
  - type/thread
likes: 333
views: 33258
engagement_score: 948
url: "https://x.com/alexhillman/status/2013820793671536778"
enrichment_complete: true
has_media: false
has_links: false
has_thread_context: true
---

> [!tweet] @alexhillman · Jan 21, 2026
> When I started building my assistant I figured this one out FAST. 
> 
> Claude Code doesn't know what time it is. Or what time zone you are in. 
> 
> So when you do date time operations of ANY kind, as simple as saving something to your calendar, things get weird fast. 
> 
> My early solution has stuck thru every iteration of my JFDI system and it's dummy simple:
> 
> I use Claude Code hooks to run a bash script that generates current date time, timezone of host device, friendly day of week etc. 
> 
> Injects it silently into context. 
> 
> I never see it but date time issues vanish. 3+ most battle tested. 
> 
> Kinda wild that this isn't baked in @bcherny (thank you for CC btw it changed my life no exaggerating)
>
> Likes: 333 · Replies: 23 · Reposts: 6

## Summary

This tip addresses Claude Code's lack of inherent timezone/time awareness by leveraging Claude Code hooks. It uses a bash script to generate current date, time, and timezone information from the host device. This data is then silently injected into the Claude Code context, resolving datetime-related issues for applications like calendar integration. 

## Keywords

**Primary:** `date-time-context-injection` · timezone, bash-script, date-time-operations, hooks, context
## Classification

**ACT_NOW** — Matches pending technique with 333 likes
## Replies

> [!reply] @stolinski · 2026-01-21T02:16:02+00:00
> My clawdbot sucks at days and time. It never seems to have any clue what the current day or time is.
> *19 likes*

> [!reply] @webprofusion · 2026-01-21T13:16:10+00:00
> @alexhillman So we need an MCP current date and time server, got it.
> *7 likes*

> [!tip]+ :leftwards_arrow_with_hook: @alexhillman · 2026-01-21T13:42:39+00:00

> @webprofusion 😂 dear God no

> [!reply] @alexhillman · 2026-01-21T14:09:39+00:00
> IME the stop and tool use commands aren't the right spot for injecting a timestamp to remind CC what day/time/timezone you're in. 
> 
> Tool use is too much. 
> Stop is too late. 
> 
> UserSubmotPrompt make sure that it's injected along with MY messages. 
> 
> Which is plenty, and always ahead of an operation where the date time matters, not after. 
> 
> Also means that cachable turns aren't wasted.
> *7 likes*

> [!reply] @rezzz · 2026-01-21T11:21:14+00:00
> @alexhillman I noticed this too.
> 
> Crazy to think the computer doesn’t know time.
> 
> I like the hook idea. 
> 
> What I did was simply put in the MD file that house the instructions to always get the time and date before moving forward.
> *4 likes*

> [!tip]+ :leftwards_arrow_with_hook: @alexhillman · 2026-01-21T13:38:30+00:00

> @rezzz That works til it skips those instructions!

> [!reply] @Loster · 2026-01-21T15:40:05+00:00
> @alexhillman Yeah it's mad isn't it. It doesn't know the time. 
> 
> I'll restart a chat after not touching it for a day and Claude *thinks* it's previous actions were performed immediately before
> *4 likes*

> [!tip]+ :leftwards_arrow_with_hook: @alexhillman · 2026-01-21T15:50:30+00:00

> @Loster these things don't *know* anything

> [!reply] @dir · 2026-01-21T09:53:41+00:00
> @alexhillman It busts caching which is why it isn’t there. You lose a lot for little gain
> *3 likes*

> [!tip]+ :leftwards_arrow_with_hook: @alexhillman · 2026-01-21T14:12:17+00:00

> @dir If you put it in places that make no sense, you'd be correct. 
> 
> If you inject it along with our own user prompts, all caching preserved.

> [!reply] @startupecon · 2026-01-21T11:43:04+00:00
> @alexhillman For those curious what "silent" means, I believe add this to settings.json
> 
> {  "hooks": {  "PreToolUse": [  {  "matcher": "*",  "command": "date '+Context: %A %Y-%m-%d %H:%M %Z'"  }  ]  } }
> *3 likes*

> [!reply] @m_ashcroft · 2026-01-21T08:33:19+00:00
> @alexhillman I recently added this to my start up skill and it helps a lot
> *2 likes*

> [!reply] @daloore · 2026-01-21T14:41:05+00:00
> @alexhillman I go a little bit further. And add in relative time of the current date. 
> I. E. Next week =
> This weekend =
> Etc 
> Means I can even do dates with a dumber model
> *1 likes*

> [!tip]+ :leftwards_arrow_with_hook: @alexhillman · 2026-01-21T14:43:45+00:00

> @daloore yup i do this too! 
> 
> noticed it incorrectly identifying the day of the week in some cases, so gave it a nice lil suite of date/time references including those

> [!reply] @garybasin · 2026-01-22T02:34:01+00:00
> @alexhillman Lot of lessons in those opus system prompts
> *1 likes*


---

> [!metrics]- Engagement & Metadata
> **Likes:** 333 · **Replies:** 23 · **Reposts:** 6 · **Views:** 33,258
> **Engagement Score:** 948
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2013820793671536778](https://x.com/alexhillman/status/2013820793671536778)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ℹ️ none
  thread: ✅ (30 replies scraped)
  classification: ✅ ACT_NOW
```