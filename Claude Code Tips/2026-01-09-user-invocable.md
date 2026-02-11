---
created: 2026-01-09
author: "@dani_avila7"
display_name: "Daniel San"
tags:
  - type/screenshot
  - type/thread
likes: 207
views: 71122
engagement_score: 666
url: "https://x.com/dani_avila7/status/2009620498573873379"
---

> [!tweet] @dani_avila7 · Jan 09, 2026
> Another interesting feature in Claude Code 2.1
> 
> Skills are visible by default using / (just like commands).
> 
> Yes, this can be confusing at first, but with a solid naming convention it’s easy to manage.
> 
> If you want to hide a Skill so it’s not visible to users, add this to the skill frontmatter: 
> user-invocable: false
> 
> Ways Skills can be invoked:
> - user-invocable: true (default): users can invoke it directly
> - user-invocable: false: Claude can use it, but users shouldn’t
> - disable-model-invocation: true: users can invoke it, but Claude won’t do so programmatically
> 
> Also worth noting: subagents can invoke Skills too.
> 
> Using Claude Code is easy... designing well-structured, autonomous workflows is a different level entirely.
> 
> Coming soon: a degree in Claude Code Engineering 😄
>
> Likes: 207 · Replies: 19 · Reposts: 18

## Summary

This Claude Code 2.1 tip explains how to manage Skill visibility. Skills are now visible by default using the `/` command, but can be hidden from users by setting `user-invocable: false` in the skill's frontmatter. You can also control whether Claude itself can programmatically invoke the Skill using `disable-model-invocation: true`.

## Media

![Media](https://pbs.twimg.com/media/G-Oa5xiWQAAEkFq.jpg)







## Replies

> [!reply] @dani_avila7 · 2026-01-08T22:51:22+00:00
> Discovering more options in Claude Code 2.1.1
> 
> Skills now support Hooks directly in the YAML frontmatter.
> 
> In addition to a Skill being able to reference another Skill, you can now add hooks to run commands or scripts on PreToolUse, PostToolUse, or Stop events.
> 
> This keeps unlocking more powerful agent-based workflows.
> *231 likes*

> [!reply] @MetaSaiyans · 2026-01-09T15:05:04+00:00
> @dani_avila7 The degens will be in your comments soon
> *1 likes*

> [!tip]+ ↩️ @dani_avila7 · 2026-01-09T15:07:10+00:00

> @MetaSaiyans Prepared and waiting

> [!reply] @draken1721 · 2026-01-09T13:40:20+00:00
> @dani_avila7 Bookmarked. Claude code content king. 
> 
> Learn it sooner rather than later
> *1 likes*

> [!reply] @unknown
> 

> [!reply] @ileppane · 2026-01-09T14:38:50+00:00
> I love the convenience of expanding explicit invocation capabilities, but overloading the same invocation method with both commands and skills feels confusing - could there be a collision concern?
> 
> What if it was "/[command]" and "/skill:[skill]" or something similar for consistency?

> [!tip]+ ↩️ @dani_avila7 · 2026-01-09T14:53:10+00:00

> I was thinking about something along those lines, but keep in mind that when you install a plugin, colons (:) are also used as part of the name.
> 
> So it would end up looking something like "plugin:type:name" when it’s a plugin, and "type:name" when it’s a local component.
> 
> what do you think @bcherny ?

> [!reply] @0xRaduan · 2026-01-09T14:03:17+00:00
> @dani_avila7 I think I still find claude unreliable in calling skills, so I either create a slash command around the chaining of steps including using skill, or I will mention explicitly to use the skill and do XYZ.

> [!reply] @bookwormengr · 2026-01-10T01:39:48+00:00
> @dani_avila7 This makes so much more sense. Slash Commands and Skills effectively do the same thing, though skills are bit more powerful.

> [!reply] @explorersofai · 2026-01-09T15:34:00+00:00
> @dani_avila7 Well ain't that something. Pretty wild. Agents all over the place and noone knows lol

> [!reply] @codewithimanshu · 2026-01-09T14:50:14+00:00
> @dani_avila7 @dani_avila7, managing skill visibility is crucial for a clean user experience in Claude Code.

> [!reply] @devloperVivek · 2026-01-10T18:34:19+00:00
> @dani_avila7 Been using Skills for video script writing and git workflows
> Those two save me the most time honestly.
> What other Skills are you finding useful?

> [!reply] @ronneevibe · 2026-01-10T09:41:48+00:00
> @dani_avila7 I’m using vue to hook ref files for outside purposes too!

> [!reply] @JohnThilen · 2026-01-10T07:36:59+00:00
> @dani_avila7 Why distinguish between agents and humans, rather than ability to use the skill? E.g., some skills should be used by humans and Opus, but not by Haiku.

> [!reply] @ak_cozmo · 2026-01-10T08:07:57+00:00
> skill invocability controls are crucial for production workflows. the distinction between user-invocable vs model-only skills mirrors how we think about API surface design - explicit vs implicit capabilities. claude code's approach with disable-model-invocation gives you fine-grained control over agentic behavior

> [!reply] @shreyas1009 · 2026-01-10T08:30:40+00:00
> @dani_avila7 This is good now the invocation will be much more stable I assume

> [!reply] @ruchernchong · 2026-01-10T07:25:47+00:00
> @dani_avila7 How I see this: previously those that were skills are user-invocable and those previously are not can be revised and change accordingly.

> [!reply] @Lat3ntG3nius · 2026-01-10T01:09:21+00:00
> @dani_avila7 Naming convention is key. I'm using verb-noun pattern (get-data, send-email) with prefixes for categories (api_, local_, mcp_). Makes it easier to find what you need when / autocomplete kicks in. How are you organizing yours?

> [!reply] @seorce_ · 2026-01-09T20:21:17+00:00
> @dani_avila7 discoverability tradeoff

> [!reply] @RecordsUni63959 · 2026-01-09T22:14:51+00:00
> @dani_avila7 crazy

> [!reply] @rubenmayorfx · 2026-01-10T02:26:34+00:00
> @dani_avila7 I will to spend time to check all the new features in Claude Code. Thank you for sharing those.

> [!reply] @3quanax · 2026-01-09T16:12:24+00:00
> @dani_avila7 Claude Code 2.1 skills visible via /slash is clever, but naming discipline is key. user-invocable: false hides them cleanly from users while letting Claude (and subagents) use them. Proper control for autonomous workflows.

> [!reply] @magic__one · 2026-01-16T16:12:05+00:00
> A big thank you for this awesome work, thoughtful design, powerful flexibility, and a great step forward for autonomous workflows. 
> 
> Community https://t.co/0hpkPduKh7 wants to thank you and made you a coin to support you and buy you a coffee ☕️  with those fees.
> 
> Feel free to claim whenever you like 🙂
> 
> https://t.co/uAudV9M3yX


> [!metrics]- Engagement & Metadata
> **Likes:** 207 · **Replies:** 19 · **Reposts:** 18 · **Views:** 71,122
> **Engagement Score:** 666
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2009620498573873379](https://x.com/dani_avila7/status/2009620498573873379)