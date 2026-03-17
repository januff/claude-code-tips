---
tweet_id: "2033603164398883042"
created: 2026-03-16
author: "lydiahallie"
display_name: "Lydia Hallie ✨"
primary_keyword: "context: fork"
llm_category: "subagents"
tags:
  - type/screenshot
likes: 588
views: 41978
engagement_score: 1834
url: "https://x.com/lydiahallie/status/2033603164398883042"
enrichment_complete: false
has_media: true
has_links: true
has_thread_context: false
---

> [!tweet] lydiahallie · Mar 16, 2026
> Btw you can add `context: fork` to run a skill in an isolated subagent. The main context only sees the final result, not the intermediate tool calls
> 
> It gets a fresh context window with CLAUDE.md + your skill as the prompt. The `agent` field even lets you set the subagent type! https://t.co/pzVAPWHCwJ
>
> Likes: 588 · Replies: 40 · Reposts: 40

## Summary

This Claude tip introduces a technique for isolating skill execution within a sub-agent using `context: fork`.  This allows the main agent to only see the final result, hiding intermediate steps for cleaner workflow and potentially improved context management. By defining a custom skill with `context: fork` and specifying an `agent` type, you can create isolated environments with their own context windows, utilizing the SKILL.md file.

## Keywords

**Primary:** `context: fork` · isolated subagent, subagent, context window, CLAUDE.md, agent field, skill
## Linked Resources

- **[x.com/lydiahallie/status/2033603164398883042/photo/1](https://x.com/lydiahallie/status/2033603164398883042/photo/1)**
  > :warning: Link not yet summarized

## Media

![[attachments/screenshots/tweet_2033603164398883042_66.jpg]]

Defining a custom 'deep-research' skill for Claude, specifying its name, description, context, and agent, as well as steps for research.

**Focus Text:**
```
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
```

**Key Action:** Learn how to configure a custom skill in Claude by defining its properties and steps in a SKILL.md file.


<details>
<summary>Full OCR Text</summary>
<pre>
.claude/skills/deep-research/SKILL.md

---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
</pre>
</details>


---

> [!metrics]- Engagement & Metadata
> **Likes:** 588 · **Replies:** 40 · **Reposts:** 40 · **Views:** 41,978
> **Engagement Score:** 1,834
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2033603164398883042](https://x.com/lydiahallie/status/2033603164398883042)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ⚠️ (0/1 summarized)
  media: ✅ (1/1 analyzed — 1 photo, 0 videos)
  thread: ℹ️ standalone
  classification: ❌ not classified
```