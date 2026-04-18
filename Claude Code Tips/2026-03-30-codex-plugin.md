---
tweet_id: "2038670332094230851"
created: 2026-03-30
author: "dkundel"
display_name: "dominik kundel"
primary_keyword: "Codex plugin"
llm_category: "tooling"
tags:
  - type/screenshot
  - type/reply
likes: 162
views: 25092
engagement_score: 280
url: "https://x.com/dkundel/status/2038670332094230851"
enrichment_complete: true
has_media: true
has_links: false
has_thread_context: true
---

> [!tweet] dkundel · Mar 30, 2026
> We love an open ecosystem!
> 
> The Codex plugin is built on top of the Codex app server so it uses the same open-source agent harness as the rest of Codex.
> 
> It means you can run multiple Codex tasks in parallel in the background, use the same models and the same Codex code review functionality!
> 
> Claude approves.
>
> Likes: 162 · Replies: 4 · Reposts: 5

## Summary

This tip highlights the Codex plugin's open-source foundation, built on the same agent harness as the Codex app server. This allows users to leverage existing Codex functionalities like parallel task execution, model usage, and code review within the plugin environment. By understanding the qualities of a well-engineered plugin, like architecture, UX, and safety, users can optimize its performance and integrate it seamlessly with their existing workflows.

## Keywords

**Primary:** `Codex plugin` · open-source agent harness, Codex app server, parallel tasks, code review
## Media

![[attachments/screenshots/tweet_2038670332094230851_83.jpg]]

Reviewing the architecture, UX, defaults, prompting skills, and safety of a software plugin.


**Key Action:** Understanding the qualities of a well-engineered plugin, including its architecture, UX, defaults, prompting skills, and safety mechanisms.


<details>
<summary>Full OCR Text</summary>
<pre>
This is a really well-engineered plugin. The standout qualities:
- Architecture discipline the forwarder-not-orchestrator pattern for the subagent, the
clean command/skill/script layering, and the broker abstraction all show someone who's
thought carefully about where complexity belongs.
- Complete UX it's not just "call Codex." It's a full workflow: review, adversarial review,
task delegation, job tracking, result retrieval, cancellation, resume. That's a polished
developer experience.
- Smart defaults with escape hatches read-only reviews by default, optional stop-gate,
background/foreground modes, scope control (auto working-tree branch). Power users get knobs
without burdening casual users.
- The prompting skill is a differentiator bundling recipes, antipatterns, and reusable
prompt blocks for GPT-5.4 directly into the plugin means users get good Codex results without
needing to be prompt engineers themselves.
- Safety without friction grounding rules, sandbox modes, and "present verbatim, don't
auto-fix" are the right calls. It builds trust without adding annoying confirmation dialogs.

The only thing I'd flag is the operational surface area the IPC broker, socket-based app
server bridge, and session lifecycle hooks are a lot of moving parts. If something breaks in
that chain, debugging could be painful. But that's inherent to the problem being solved, not
a design flaw.

Overall: this reads like production-quality work from someone who's shipped developer tools
before. It's opinionated in the right places and flexible where it matters.

>
? for shortcuts
</pre>
</details>


---

> [!metrics]- Engagement & Metadata
> **Likes:** 162 · **Replies:** 4 · **Reposts:** 5 · **Views:** 25,092
> **Engagement Score:** 280
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✓
> **ID:** [2038670332094230851](https://x.com/dkundel/status/2038670332094230851)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ✅ (1/1 analyzed — 1 photo, 0 videos)
  thread: ⚠️ (reply — parent not in DB)
  classification: ❌ not classified
```