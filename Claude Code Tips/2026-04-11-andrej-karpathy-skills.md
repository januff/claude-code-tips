---
tweet_id: "2042914348859867218"
created: 2026-04-11
author: "sharbel"
display_name: "Sharbel"
primary_keyword: "andrej-karpathy-skills"
llm_category: "skills"
tags:
  - type/screenshot
likes: 4693
views: 380857
engagement_score: 26712
url: "https://x.com/sharbel/status/2042914348859867218"
enrichment_complete: true
has_media: true
has_links: false
has_thread_context: false
---

> [!tweet] sharbel · Apr 11, 2026
> 🚨 Andrej Karpathy documented the exact ways LLMs fail at coding. Someone turned those observations into a single Claude config file.
> 
> It's called andrej-karpathy-skills.
> 
> +3,741 stars this week.
> 
> Why it's great:
> 
> Claude Code makes the same mistakes on every project. It over-explains. It adds code you didn't ask for. It ignores constraints you set 3 prompts ago.
> 
> Most people just accept this as the baseline. Karpathy didn't.
> 
> He catalogued the failure patterns. This repo converts every one of them into a CLAUDE.md instruction that fixes the behavior at the source.
> 
> How to use it:
> 
> Drop the CLAUDE.md file into the root of any project. Claude reads it automatically on every session.
> 
> No prompt engineering on every request. No babysitting. The behavior changes once and stays changed.
> 
> One file. Every project.
>
> Likes: 4,693 · Replies: 99 · Reposts: 472

## Summary

This Claude Code tip introduces a config file, 'andrej-karpathy-skills,' that addresses common LLM coding errors documented by Andrej Karpathy. By dropping the CLAUDE.md file into the project root, users can enforce consistent coding behavior across all sessions, eliminating the need for repeated prompt engineering or babysitting. This approach leverages Karpathy's catalogued failure patterns and provides project-level control over Claude Code's output.

## Keywords

**Primary:** `andrej-karpathy-skills` · CLAUDE.md, Karpathy, failure patterns, config file
## Media

![[attachments/screenshots/tweet_2042914348859867218_78.jpg]]

The screenshot shows a set of guidelines to improve Claude Code behavior.


**Key Action:** Learn the four principles of the "Karpathy-Inspired Claude Code Guidelines" to improve Claude Code behavior.


<details>
<summary>Full OCR Text</summary>
<pre>
Karpathy-Inspired Claude Code Guidelines
A single CLAUDE.md file to improve Claude Code behavior, derived from Andrej Karpathy's observations on LLM
coding pitfalls.

The Problems

From Andrej's post:

"The models make wrong assumptions on your behalf and just run along with them without checking. They
don't manage their confusion, don't seek clarifications, don't surface inconsistencies, don't present tradeoffs,
don't push back when they should."

"They really like to overcomplicate code and APIs, bloat abstractions, don't clean up dead code... implement a
bloated construction over 1000 lines when 100 would do."

"They still sometimes change/remove comments and code they don't sufficiently understand as side effects,
even if orthogonal to the task."

The Solution

Four principles in one file that directly address these issues:

Principle
Addresses
Think Before Coding
Wrong assumptions, hidden confusion, missing tradeoffs
Simplicity First
Overcomplication, bloated abstractions
Surgical Changes
Orthogonal edits, touching code you shouldn't
Goal-Driven Execution
Leverage through tests-first, verifiable success criteria
</pre>
</details>


---

> [!metrics]- Engagement & Metadata
> **Likes:** 4,693 · **Replies:** 99 · **Reposts:** 472 · **Views:** 380,857
> **Engagement Score:** 26,712
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2042914348859867218](https://x.com/sharbel/status/2042914348859867218)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ✅ (1/1 analyzed — 1 photo, 0 videos)
  thread: ℹ️ standalone
  classification: ❌ not classified
```