---
created: 2025-12-29
author: "@jeffzwang"
display_name: "Jeffrey Wang"
category: "context-management"
tags:
  - category/context-management
  - type/code-snippet
likes: 0
views: 255
engagement_score: 0
url: "https://x.com/jeffzwang/status/2005683211519840327"
---

> [!tweet] @jeffzwang · Dec 29, 2025
> prevent slash commands from default filling context window by adding the flag `disable-model-invocation: true` to each
>
> Likes: 0 · Replies: 0 · Reposts: 0

## Summary

This tip addresses how to optimize Claude's context window usage when defining slash commands. By adding the `disable-model-invocation: true` flag to individual slash commands, you prevent them from unnecessarily consuming context, which improves overall efficiency and possibly cost. This setting ensures Claude doesn't try to interpret or invoke the command by default, saving valuable context space.

## Code

`disable-model-invocation: true`


> [!metrics]- Engagement & Metadata
> **Likes:** 0 · **Replies:** 0 · **Reposts:** 0 · **Views:** 255
> **Engagement Score:** 0
>
> **Source:** tips · **Quality:** 6/10
> **Curated:** ✓ · **Reply:** ✗
> **ID:** [2005683211519840327](https://x.com/jeffzwang/status/2005683211519840327)