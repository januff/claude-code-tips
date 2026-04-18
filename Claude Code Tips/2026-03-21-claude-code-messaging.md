---
tweet_id: "2035214150545092845"
created: 2026-03-21
author: "louisvarge"
display_name: "Louis Arge"
primary_keyword: "claude-code-messaging"
llm_category: "subagents"
tags:
likes: 3946
views: 687765
engagement_score: 11714
url: "https://x.com/louisvarge/status/2035214150545092845"
enrichment_complete: false
has_media: true
has_links: true
has_thread_context: false
---

> [!tweet] louisvarge · Mar 21, 2026
> i made a thing where now any Claude Code can send messages to any other Claude Code on my machine
> 
> they can ask clarifying questions about work, or become friends https://t.co/wOUvPrbA7T
>
> Likes: 3,946 · Replies: 254 · Reposts: 231

## Summary

This tip demonstrates how to enable communication between locally running Claude Code instances. By using the `claude-peers` tool, you can facilitate message exchange, allowing instances to collaborate or ask questions. The video shows the usage of `claude-peers - list_peers` and `claude-peers - send_message` commands to establish a connection and exchange messages between two instances named Michael and Jessica.

## Keywords

**Primary:** `claude-code-messaging` · message, inter-agent, communication, friends
## Linked Resources

- **[x.com/louisvarge/status/2035214150545092845/video/1](https://x.com/louisvarge/status/2035214150545092845/video/1)**
  > :warning: Link not yet summarized

## Media

![[attachments/videos/tweet_2035214150545092845_95.mp4]]

First, two Claude Code instances are initiated, named Michael and Jessica. Then, Michael sends a message to Jessica using `claude-peers - list_peers` and `claude-peers - send_message`. Finally, the video shows Claude instances communicating and exchanging messages about their current work.

**Focus Text:**
```
Please ask the other Claude
```

**Key Action:** Learn how to facilitate communication between multiple Claude Code instances running locally using the `claude-peers` tool.

**Commands:** claude-peers - list_peers (MCP)(scope: "machine"), claude-peers - send_message (MCP)(to_id: "ljelgc6g", message: "Hi Jessica! This is Michael👋"), claude-peers - check_messages (MCP), claude-peers - send_message (MCP)(to_id: "fdtrai9u", message: "Hi! I'm Jessica. I'm doing some busy work for our user -- running a Python script that sleeps 10 seconds, editing it, and repeating 6 times. On iteration 2 of 6 right now!")



---

> [!metrics]- Engagement & Metadata
> **Likes:** 3,946 · **Replies:** 254 · **Reposts:** 231 · **Views:** 687,765
> **Engagement Score:** 11,714
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2035214150545092845](https://x.com/louisvarge/status/2035214150545092845)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ⚠️ (0/1 summarized)
  media: ✅ (1/1 analyzed — 0 photos, 1 video)
  thread: ℹ️ standalone
  classification: ❌ not classified
```