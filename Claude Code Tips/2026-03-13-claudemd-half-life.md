---
tweet_id: "2032436777630540182"
created: 2026-03-13
author: "toddsaunders"
display_name: "Todd Saunders"
primary_keyword: "CLAUDE.md half life"
llm_category: "context-management"
tags:
likes: 423
views: 89702
engagement_score: 1940
url: "https://x.com/toddsaunders/status/2032436777630540182"
enrichment_complete: true
has_media: false
has_links: false
has_thread_context: false
---

> [!tweet] toddsaunders · Mar 13, 2026
> I rewrite my CLAUDE.md from scratch every few weeks.
> 
> It's the single greatest hack I've learned since being completely Claude Code pilled.
> 
> It took me a while to fully understand that CLAUDE.md has a half life.
> 
> When I first start a project, Claude follows the file very clearly. But over time, it degrades. I realized I was bloating the file by patching mistakes saying things like "don't use this import" or "never use this folder."
> 
> After a few weeks of building, my file would go from ~50 lines to ~200 lines. At points, mine even hit 1,200 lines.
> 
> But this absolutely torches claude performance if you do this.
> 
> CLAUDE.md gets injected into the context window on every single interaction. The more tokens your instructions use, the less room Claude has to reason about your actual code.
> 
> You are shrinking your context window literally for no reason, making the whole experience worse.
> 
> I've a/b tested this and realized that a  50-line file with clear architectural intent ("we use server components by default, API routes live in /api") gives Claude a deep understanding of what you want.
> 
> A 1,000-line file full of "don't do X" patches (which I had a ton of when I first started) is horrific for performance.  The model has to parse through hundreds of negations and edge cases, and the important directives get diluted.
> 
> Just move some of those to skills, or delete the things that don't matter anymore.
> 
> It's the same concept as technical debt in a codebase. Once I heard this analogy, it started to make a lot more sense to me.
> 
> You don't just keep adding if statements to handle bugs. At some point you refactor and write the code the write way. CLAUDE.md is the same.
> 
> My new rule of thumb is if my CLAUDE.md is over 150 lines, it's time to burn it down and rewrite.
> 
> For me that's generally every 2 weeks. I burn it down, re-write it, and am amazed by the performance.
>
> Likes: 423 · Replies: 37 · Reposts: 30

## Summary

This tip highlights the importance of regularly rewriting your `CLAUDE.md` file for optimal Claude performance. The key insight is that `CLAUDE.md` accumulates technical debt as you patch over mistakes with instructions like "don't do X," bloating the file and shrinking the context window available for Claude to reason about your actual code. By periodically rewriting it (around every two weeks or when it exceeds 150 lines), you ensure Claude has a concise and clear understanding of your project's architecture.

## Keywords

**Primary:** `CLAUDE.md half life` · CLAUDE.md, context window, technical debt, performance, refactor, architectural intent

---

> [!metrics]- Engagement & Metadata
> **Likes:** 423 · **Replies:** 37 · **Reposts:** 30 · **Views:** 89,702
> **Engagement Score:** 1,940
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2032436777630540182](https://x.com/toddsaunders/status/2032436777630540182)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ℹ️ none
  thread: ℹ️ standalone
  classification: ❌ not classified
```