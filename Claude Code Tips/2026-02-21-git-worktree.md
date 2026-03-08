---
tweet_id: "2025007393290272904"
created: 2026-02-21
author: "bcherny"
display_name: "Boris Cherny"
primary_keyword: "git worktree"
llm_category: "tooling"
tags:
  - type/screenshot
likes: 10946
views: 1250135
engagement_score: 28436
url: "https://x.com/bcherny/status/2025007393290272904"
enrichment_complete: true
has_media: true
has_links: true
has_thread_context: false
---

> [!tweet] bcherny · Feb 21, 2026
> Introducing: built-in git worktree support for Claude Code 
> 
> Now, agents can run in parallel without interfering with one other. Each agent gets its own worktree and can work independently.
> 
> The Claude Code Desktop app has had built-in support for worktrees for a while, and now we're bringing it to CLI too.
> 
> Learn more about worktrees: https://t.co/JFkD2DrAmT
>
> Likes: 10,946 · Replies: 430 · Reposts: 845

## Summary

Claude Code now supports Git worktrees in its CLI, mirroring existing functionality in the desktop app. This allows multiple agents to operate in parallel within separate worktrees of the same Git repository, preventing interference. The key action is using the `--worktree` flag with the `claude` command, as demonstrated in the attached image, to manage these isolated workspaces.

## Keywords

**Primary:** `git worktree` · parallel agents, CLI, desktop app
## Linked Resources

- **[Git - git-worktree Documentation](https://git-scm.com/docs/git-worktree)** · *documentation*
  > The `git-worktree` command allows you to manage multiple working trees attached to a single Git repository, enabling you to check out multiple branches concurrently. This documentation page details how to use `git worktree` to add, list, lock, move, prune, remove, repair, and unlock worktrees.

## Media

![[attachments/screenshots/tweet_2025007393290272904_39.png]]

Demonstrates the use of the `--worktree` flag in Claude CLI.

**Focus Text:**
```
$ claude --worktree

```

**Key Action:** Learn how to use the `--worktree` flag with the claude command.

**Commands:** claude --worktree

<details>
<summary>Full OCR Text</summary>
<pre>
$ claude --worktree

</pre>
</details>


---

> [!metrics]- Engagement & Metadata
> **Likes:** 10,946 · **Replies:** 430 · **Reposts:** 845 · **Views:** 1,250,135
> **Engagement Score:** 28,436
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2025007393290272904](https://x.com/bcherny/status/2025007393290272904)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ✅ (1/1 summarized)
  media: ✅ (1/1 analyzed — 1 photo, 0 videos)
  thread: ℹ️ standalone
  classification: ❌ not classified
```