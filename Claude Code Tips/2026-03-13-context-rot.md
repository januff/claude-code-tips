---
tweet_id: "2032519515817599047"
created: 2026-03-13
author: "AnishA_Moonka"
display_name: "Anish Moonka"
primary_keyword: "context rot"
llm_category: "context-management"
tags:
likes: 1861
views: 346633
engagement_score: 3924
url: "https://x.com/AnishA_Moonka/status/2032519515817599047"
enrichment_complete: true
has_media: false
has_links: false
has_thread_context: false
---

> [!tweet] AnishA_Moonka · Mar 13, 2026
> GPT-5.4 loses 54% of its retrieval accuracy going from 256K to 1M tokens. Opus 4.6 loses 15%.
> 
> Every major AI lab now claims a 1 million token context window. GPT-5.4 launched eight days ago with 1M. Gemini 3.1 Pro has had it. But the number on the spec sheet and the number that actually works are two very different things.
> 
> This chart uses MRCR v2, OpenAI’s own benchmark. It hides 8 identical pieces of information across a massive conversation and asks the model to find a specific one. Basically a stress test for “can you actually find what you need in 750,000 words of text.”
> 
> At 256K tokens, the models are close enough. Opus 4.6 scores 91.9%, Sonnet 4.6 hits 90.6%, GPT-5.4 sits at 79.3% (averaged across 128K to 256K, per the chart footnote). Scale to 1M and the curves blow apart. GPT-5.4 drops to 36.6%, finding the right answer about one in three times. Gemini 3.1 Pro falls to 25.9%. Opus 4.6 holds at 78.3%.
> 
> Researchers call this “context rot.” Chroma tested 18 frontier models in 2025 and found every single one got worse as input length increased. Most models decay exponentially. Opus barely bends.
> 
> Then there’s the pricing. Today’s announcement removes the long-context premium entirely. A 900K-token Opus 4.6 request now costs the same per-token rate as a 9K request, $5/$25 per million tokens. GPT-5.4 still charges 2x input and 1.5x output for anything over 272K tokens. So you pay more for a model that retrieves correctly about a third of the time at full context.
> 
> For anyone building agents that run for hours, processing legal docs across hundreds of pages, or loading entire codebases into one session, the only number that matters is whether the model can actually find what you put in. At 1M tokens, that gap between these models just got very wide.
>
> Likes: 1,861 · Replies: 73 · Reposts: 183

## Summary

This tip highlights significant differences in retrieval accuracy among leading LLMs, particularly at 1 million token context windows, using OpenAI's MRCR v2 benchmark. While models like GPT-5.4 and Gemini 3.1 Pro experience substantial performance degradation, Claude Opus 4.6 maintains a high accuracy, making it a more reliable choice for long-context tasks. Furthermore, Opus 4.6 now offers competitive pricing, eliminating long-context premiums and potentially making it a more cost-effective option compared to GPT-5.4.

## Keywords

**Primary:** `context rot` · retrieval accuracy, MRCR v2, 1 million token context window, Opus 4.6, GPT-5.4, Gemini 3.1 Pro, long-context premium, context window

---

> [!metrics]- Engagement & Metadata
> **Likes:** 1,861 · **Replies:** 73 · **Reposts:** 183 · **Views:** 346,633
> **Engagement Score:** 3,924
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2032519515817599047](https://x.com/AnishA_Moonka/status/2032519515817599047)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ℹ️ none
  thread: ℹ️ standalone
  classification: ❌ not classified
```