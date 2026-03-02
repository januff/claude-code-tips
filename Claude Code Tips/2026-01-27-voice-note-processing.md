---
tweet_id: "2016047512478507444"
created: 2026-01-27
author: "remilouf"
display_name: "Rémi"
primary_keyword: "voice-note-processing"
llm_category: "automation"
tags:
likes: 375
views: 61172
engagement_score: 1843
url: "https://x.com/remilouf/status/2016047512478507444"
enrichment_complete: true
has_media: false
has_links: false
has_thread_context: false
---

> [!tweet] remilouf · Jan 27, 2026
> It is fairly simple. I go on walks every morning and usually record my rambling. It’s synced with my server automatically, transcribed and copied to an inbox in my @obsdmd vault (although I could use any frontend, it’s just text files).
> 
> A first agent scans the transcription and does a few things:
> 
> 0. Create a new daily note 
> 1. Identifies topics
> 2. Identifies (pending) decisions 
> 3. Identifies tasks -> pushed to Things Inbox
> 4. Identifies potential evergreen notes or addition to one, and suggests it (linking to the daily note). I need to tick a box to approve.
> 
> If I record other voice notes during the day it’s appended to the file.
> 
> Every evening an agent reads the notes with the notes of the previous days and 
> 
> 1. Promotes everything I approved to evergreen notes and runs another agent to find relevant links.
> 2. Checks Things and summarizes my day
> 3. Surfaces issues that have been unresolved for a while, topics I keep bringing up
> 4. Asks 3 hard questions 
> 
> If there have been changes in my evergreen notes it scans the full vault for links.
> 
> Then every week, month and quarter different agents analyze my notes and connect to other systems of record via CLIs I wrote.
> 
> I have an agent that surfaces potential blog post topics (but doesn’t write the blog post)
> 
> I also have an agent connected to a Telegram bot that has read-only access. Very nice to ask questions. Hoping to get rid of this at some point when I can run decent agents on my phone.
> 
> It’s been very helpful for me, a natural rambler who processes things by talking and not by writing. The prompts are really hard to get right at the beginning, mostly because you’re discovering your needs as you go. I would recommend you start with a very simple agent (like daily notes), iterate for a couple of weeks before moving on. Don’t build cathedrals from the get go, however tempting it is. 
> 
> Even if it’s been running for a while, I still find myself checking the transcript to make sure it didn’t forget anything. Sometimes it does, maybe a prompting skill issue. I consider the daily notes as a DRAFT, albeit a very helpful one.
> 
> Identify interfaces and places where a human is needed to prevent the whole thing from becoming an unholy mess; it can just be requiring a box to be ticked to approve.
> 
> The links suggestion is life-changing.
> 
> I plan on moving everything to open source models progressively.
>
> Likes: 375 · Replies: 14 · Reposts: 14

## Summary

This tip details an automated personal knowledge management workflow leveraging voice notes and AI agents. The user records daily ramblings which are transcribed and processed to create daily notes, identify topics and tasks, and suggest connections to evergreen notes. Agents further analyze notes daily, weekly, monthly, and quarterly, surfacing insights, unresolved issues, and potential blog posts while requiring human approval for critical actions to maintain control.

## Keywords

**Primary:** `voice-note-processing` · daily notes, evergreen notes, agent, transcription, obsidian, automatic, summarization

---

> [!metrics]- Engagement & Metadata
> **Likes:** 375 · **Replies:** 14 · **Reposts:** 14 · **Views:** 61,172
> **Engagement Score:** 1,843
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2016047512478507444](https://x.com/remilouf/status/2016047512478507444)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ℹ️ none
  thread: ℹ️ standalone
  classification: ❌ not classified
```