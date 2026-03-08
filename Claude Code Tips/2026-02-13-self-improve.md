---
tweet_id: "2022336187298709653"
created: 2026-02-13
author: "@DellAnnaLuca"
display_name: "Luca Dellanna"
primary_keyword: "self-improve"
llm_category: "prompting"
tags:
  - type/screenshot
likes: 784
views: 49762
engagement_score: 4118
url: "https://x.com/DellAnnaLuca/status/2022336187298709653"
enrichment_complete: true
has_media: true
has_links: false
has_thread_context: false
---

> [!tweet] @DellAnnaLuca · Feb 13, 2026
> The easiest way to get Claude to self-improve.
> 
> One-minute setup to save you hours (days, even) down the road.
> 
> It works even in Chat and Cowork mode. https://t.co/kDx0OmMXFf
>
> Likes: 784 · Replies: 8 · Reposts: 53

## Summary

This tip presents a simple workflow for enabling Claude to self-improve its performance in current and future chats. The key action is creating a 'reflect' skill that instructs Claude to review past interactions, identify errors, suggest improvements, and learn from them. The 'reflect' skill also enables Claude to self-audit any custom skills created in the chat, adding success criteria and optimizing for efficiency, ultimately improving future performance and minimizing repeated corrections from the user.

## Keywords

**Primary:** `self-improve` · self-improvement, one-minute setup, chat, cowork
## Media

![[attachments/screenshots/tweet_2022336187298709653_33.jpg]]

Setting up Claude for self-improvement by creating a reflect skill to review and improve future chats.

**Focus Text:**
```
Create a skill called "reflect". When I type "reflect", you should:
1. Review what we've done in this chat.
2. Identify mistakes, friction, or unclear outputs.
3. Propose a short list of concrete improvements.
4. Ask me which of these you should remember for future chats.
If any skills were used in this chat, also check each one for improvements:
1. If the skill doesn't already have a self-check: add success criteria at the top
and an instruction at the bottom to verify those criteria are met before
presenting output (iterating up to 5 times if not).
2. Check the skill for conciseness and opportunities to save tokens, without
degrading clarity or functionality.
3. Propose any other improvements to the skill, and ask me whether to
apply them.

If you notice I repeatedly ask you to do similar tasks, suggest creating a reusable skill
and ask for confirmation before doing so.

Also: Proactively suggest typing "reflect" whenever you notice I've had to correct you,
clarify something twice, or seem frustrated.
```

**Key Action:** Create a 'reflect' skill for Claude to enable self-improvement through review and reflection on past interactions.


<details>
<summary>Full OCR Text</summary>
<pre>
A Simple Setup for a
Self-Improving Claude

A quick guide to set up Claude Desktop so that it learns from its mistakes
and gets better the more you use it. Great for non-technical users.

Published: 2026-02-13 by Luca Dellanna
#ai #claude

Frustrated at having to copy/paste prompts all the time, or seeing Claude making the same
mistakes? Here's a quick guide to have a self-improving setup for Claude. Great for non-
technical users.

1) Install & basic privacy

Install Claude Desktop: claude.com/download
Open Settings → Privacy and deselect "Help improve Claude" so your
conversations and preferences remain private.

2) Start a chat

Open Claude Desktop
If you have a paid plan: Click "Cowork" at the top, then start a new chat. You'll
see a prompt to select a folder. I suggest creating a "Claude" folder in your home
folder (for example, Users/yourname/Claude).
If you're on the free plan: Start a regular chat. Then (very important) paste the
following and send the message:

Copy

Add this to your memory: Every time you create or edit a skill, you must use
the present_file tool to show me the finished skill, and clearly tell me to
click "Copy to your skills" to save it. Warn me that the skill will be lost if I
don't click that button.


3) Create the "reflect" skill

A skill is a saved instruction that Claude remembers across all your future chats. It's the
basic building block to ensure that Claude gets better as you keep using it.
Paste this and send it:

Copy

Create a skill called "reflect". When I type "reflect", you should:
1. Review what we've done in this chat.
2. Identify mistakes, friction, or unclear outputs.
3. Propose a short list of concrete improvements.
4. Ask me which of these you should remember for future chats.
If any skills were used in this chat, also check each one for improvements:
1. If the skill doesn't already have a self-check: add success criteria at the top
and an instruction at the bottom to verify those criteria are met before
presenting output (iterating up to 5 times if not).
2. Check the skill for conciseness and opportunities to save tokens, without
degrading clarity or functionality.
3. Propose any other improvements to the skill, and ask me whether to
apply them.

If you notice I repeatedly ask you to do similar tasks, suggest creating a reusable skill
and ask for confirmation before doing so.

Also: Proactively suggest typing "reflect" whenever you notice I've had to correct you,
clarify something twice, or seem frustrated.

When Claude finishes, it should show you the skill and prompt you to click "Copy to your
skills." Click it.

Verify the skill was saved: Type reflect. Since you haven't done any work yet, Claude
should explain there's nothing to reflect on but describe what it will do when there is. That
confirms the skill is active and will be available in all future sessions.

How to use it

At the end of each work session, or milestone, type reflect and send the message. Then let
Claude self-improve.
</pre>
</details>


---

> [!metrics]- Engagement & Metadata
> **Likes:** 784 · **Replies:** 8 · **Reposts:** 53 · **Views:** 49,762
> **Engagement Score:** 4,118
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2022336187298709653](https://x.com/DellAnnaLuca/status/2022336187298709653)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ✅ (1/1 analyzed — 1 photo, 0 videos)
  thread: ℹ️ standalone
  classification: ❌ not classified
```