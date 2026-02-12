---
tweet_id: "2012741829683224584"
created: 2026-01-18
author: "@PerceptualPeak"
display_name: "Zac"
primary_keyword: "/fork-detect"
llm_category: "context-management"
classification: "ACT_NOW"
tags:
  - type/screenshot
  - type/thread
likes: 4632
views: 644707
engagement_score: 21340
url: "https://x.com/PerceptualPeak/status/2012741829683224584"
enrichment_complete: false
has_media: true
has_links: false
has_thread_context: true
---

> [!tweet] @PerceptualPeak · Jan 18, 2026
> holy shit it fucking WORKS. 
> 
> SMART FORKING. My mind is genuinely blown. I HIGHLY RECCOMEND every Claude Code user implement this into their own workflows. 
> 
> Do you have a feature you want to implement in an existing project without re-explaining things? As we all know, the more relevant context a chat session has, the more effectively it will be able to implement your request. Why not utilize the knowledge gained from your hundreds/thousands of other Claude code sessions? Don't let that valuable context go to waste!!
> 
> This is where smart forking comes into play. Invoke the /fork-detect tool and tell it what you're wanting to do. It will then run your prompt through an embedding model, cross reference the embedding with a vectorized RAG database containing every single one of your previous chat sessions (which auto updates as you continue to have more sessions). 
> 
> It will then return a list of the top 5 relevant chat sessions you've had relating to what you're wanting to do, assigning each a relevance score - ordering it from highest to lowest. You then pick which session you prefer to fork from, and it gives you the fork command to copy and paste into a new terminal. 
> 
> And boom, there you have it. Seamlessly efficient feature implementation. 
> 
> Happy to whip up an implementation plan & share it in a git repo if anyone is interested!
>
> ---
> *@PerceptualPeak · 2026-01-18T04:32:11+00:00:*
> Composite scoring formula being used: (best_similarity × 0.40) + (avg_similarity × 0.20) + (chunk_ratio × 0.05) + (recency × 0.25) + (chain_quality × 0.10)
>
> ---
> *@PerceptualPeak · 2026-01-18T04:22:39+00:00:*
> @DanielleFong I think you might like this
>
> ---
> *@PerceptualPeak · 2026-01-19T07:16:30+00:00:*
> Update on the repo - I won't be able to whip it up tonight. Turns out when I migrated my vector database to nomic embeddings yesterday I accidentally used the old daemon & embedded with 384 dim again as opposed to 768 🙄. OH, and to top it off I was a dum dum and didn't consider how much freaking RAM the batch sizes would eat up 🤦 soooo, migration is running now but PC is basically bricked right now until it finishes. 
> 
> Lots of very interesting comments I still want to respond to but ya boy is TIRED so it's time to sleep & refresh my brains own context window. 
> 
> Also, I think what I'll do is make a video walkthrough breaking down every aspect of the Smart Forking feature, and also the other two components of my context management system - as they all work somewhat harmoniously together. I'll go ahead and just make open source repos for all of it too cuz why not! If it can help others optimize their own workflows then that makes me happy.
>
> Likes: 4,632 · Replies: 160 · Reposts: 297

## Summary

This tip introduces "smart forking," a technique for reusing context from past Claude Code sessions to efficiently implement new features in existing projects. It leverages the `/fork-detect` tool, which uses embedding models and a vectorized RAG database to identify the most relevant previous chat sessions. By forking from these sessions, users can avoid re-explaining project details and streamline feature development.

## Keywords

**Primary:** `/fork-detect` · smart forking, embedding model, vectorized RAG database, chat sessions, relevance score
## Classification

**ACT_NOW** — Matches pending technique with 4632 likes
## Media

![Media](https://pbs.twimg.com/media/G-6tTiBXsAAatzC.png)

> :warning: Photo not yet analyzed

![Media](https://pbs.twimg.com/media/G-6xCE0WYAAQOfG.png)

> :warning: Photo not yet analyzed

![Media](https://pbs.twimg.com/media/G-6xV9EWMAAUdKQ.png)

> :warning: Photo not yet analyzed

## Replies

> [!reply] @PerceptualPeak · 2026-01-17T17:30:13+00:00
> Claude Code idea: Smart fork detection. 
> 
> Have every session transcript auto loaded into a vector database via RAG. Create a /detect-fork command. Invoking this command will first prompt Claude to ask you what you're wanting to do. You tell it, and then it will dispatch a sub-agent to the RAG database to find the chat session with the most relevant context to what you're trying to achieve. It will then output the fork session command for that session. Paste it in a new terminal, and seamlessly pick up where you left off.
> *336 likes*

> [!reply] @SaadNaja · 2026-01-18T19:01:00+00:00
> @PerceptualPeak so we finally stopped throwing away our own intelligence every new chat. nice
> *21 likes*

> [!tip]+ :leftwards_arrow_with_hook: @PerceptualPeak · 2026-01-18T19:52:54+00:00

> @SaadNaja Laziness dictates my life, and that includes optimizing every single one of my workflows to its maximal capacity. Less work for more output = yes plz 💅

> [!reply] @ajaybuilds · 2026-01-18T08:46:53+00:00
> @PerceptualPeak Why does this sound like a good idea that will not work in practice.
> *15 likes*

> [!tip]+ :leftwards_arrow_with_hook: @PerceptualPeak · 2026-01-18T09:59:51+00:00

> Many such cases in this space for sure. Although so far in practice it's actually proven to be very useful. I did make a couple tweaks & additions though. I changed the embedding model from all-MiniLM-L6-v2 to nomic-ai/nomic-embed-text-v1.5 as nomic allows 8192 tokens vs MiniLM's 256. (I had MiniLM already running on a daemon as the embedding model for my semantic memory system which worked just fine - but later realized after implementing that my 4KB transcript chunks were being heavily truncated). 
> 
> The second thing I did is build a custom /fork.md command with special instructions that "prime" the forked session to be a sort of "context only" forked continuation of that session. This was necessary because I had realized most sessions I'd be forking have already been compacted and thus lost a lot of the context I needed (which kinda defeated the whole purpose). Plus the forked session would always assume I was picking up where that session last left off - with it wanting to implement things I've already done. So I had to let it know, hey pal relax, you're just a clone and I'm only using you for your context lol.
> 
> The /fork.md command is a ~170 line skill file with conditional instructions based on whether or not the forked session has already been compacted. IF so, it will tell the model to first review it's own compacted summary and conduct a gap analysis in its knowledge. Once the gaps are identified, it will dispatch two sub-agents instructing them to scour the pre-compacted transcript to retrieve the gaps in it's knowledge (I have a pre-compact hook which auto exports the transcript right before compaction, then runs a script on the exported .jsonl to convert it to .md, only extracting the user & system messages along with thinking blocks - and this is what the sub-agents are scouring).  
> 
> It will then combine the agent findings with it's own post-compacted summary and generate a full detailed context report - then ask me what I'd like to work on. 
> 
> After implementing these changes this workflow's been running smooth as butter. Here's some screenshots of the /fork.md for reference:

> [!reply] @ConnorYMartin · 2026-01-18T15:06:21+00:00
> @PerceptualPeak share repo plz
> *6 likes*

> [!tip]+ :leftwards_arrow_with_hook: @PerceptualPeak · 2026-01-18T15:13:10+00:00

> @ConnorYMartin Heading up north right now for a lil day snowboarding trip - ill be sure to put together a shareable repo once i get home!

> [!reply] @jruckman · 2026-01-18T19:29:39+00:00
> @PerceptualPeak need to try this! the idea of starting a new task or line of thinking from an origin that's as close as possible in vector space to previous thinking is fascinating. been leaning on my knowledge base, but still often end up searching /resume for the most resonant starting point.
> *3 likes*

> [!tip]+ :leftwards_arrow_with_hook: @PerceptualPeak · 2026-01-18T19:44:19+00:00

> Yes, trying to sort through /resume is a hellish experience. I actually built a custom dashboard to automatically keep track of, categorize, and summarize every one of my chat sessions for this very reason. Here's some pics (i've made a few updates to it since to display all semantic memories, make token count update live & other smaller features to make it sexier - not in front of PC right now so these are screenshots from a week ago)

> [!reply] @bubu111021 · 2026-01-18T09:38:55+00:00
> @PerceptualPeak wait this could work for desktop chat history too…
> *3 likes*

> [!tip]+ :leftwards_arrow_with_hook: @PerceptualPeak · 2026-01-18T10:06:02+00:00

> @bubu111021 Oooooh good thinking!!! Does Claude desktop store the chat logs locally? Boy if so......my semantic memory database is about to get a JUICY upgrade 💦 https://t.co/rCH2t1fIHV

> [!reply] @tombielecki · 2026-01-21T22:48:38+00:00
> @PerceptualPeak what you're describing is effectively Case Based Reasoning
> *2 likes*

> [!tip]+ :leftwards_arrow_with_hook: @PerceptualPeak · 2026-01-21T23:29:21+00:00

> @tombielecki I've never heard the term before - just did some reading on it. Fascinating stuff! Yes, from what I can tell I believe you're right.

> [!reply] @palepu10100 · 2026-01-18T17:41:32+00:00
> this is wild, sounds like a game changer for anyone working with Claude Code. the way you can leverage previous sessions to streamline your workflow is just smart. makes you wonder how many hours we could save with this kind of tool. also, if you're looking for more ways to find and reach customers, you should check out First100. making sales has never been easier. keep up the awesome work!
> *2 likes*

> [!tip]+ :leftwards_arrow_with_hook: @PerceptualPeak · 2026-01-18T18:50:21+00:00

> @palepu10100 I actually love the creativity of this AI auto reply lol. Give props, compliment, then slyly throw in organic looking promotion. Not even mad at it, that's genuinely super clever &amp; I can very much see this being effective at scale. 
> 
> My project list just got updated 💅

> [!reply] @AlexBoudreaux13 · 2026-01-18T17:47:46+00:00
> @PerceptualPeak Love the idea
> 
> I’m worried finding the perfect conversation but it’s not going to have enough context window left
> 
> What if the flow gives you the fork command and a compact command based on what ur trying to build and what it knows about the past chat
> *2 likes*

> [!tip]+ :leftwards_arrow_with_hook: @PerceptualPeak · 2026-01-18T18:41:56+00:00

> Excellent question! The solution I built for this very problem involves another parallel phase of my context management/preservation system, which is all about handling seamless context transfer between sessions while maximizing relevancy. Here's how it works:
> 
> When the session wants to compact, a pre-compact hook fires & auto exports the full transcript & blocks code editing tool usage (with exceptions for updating skills files & issues bash commands to embed new learnings to semantic memory). Compaction happens, Claude tries to continue editing code, gets hit with custom error message telling it to run the /post-compact command (to which it complies). 
> 
> This triggers a multi step workflow where Claude will first examine it's own compacted summary, then identify key gaps in its knowledge. It dispatches sub-agents to scour the exported pre-compacted transcript, dynamically instructing them to ingest the self-identified relevant/forgotten context (along with identifying learnings for semantic memory updates). Then the sub-agents returns their findings to the main agent - main agent then executes custom doc update procedures (combining it's implicit post-compacted knowledge of the session with the forgotten details from the sub-agents for maximal accuracy). 
> 
> Once done it creates a https://t.co/Eyw2EtHjsm file, then a session-complete flag, then concludes the session. Stop hook fires, which runs bash to trigger VS codes file watcher extension to check for session-complete flag. If detected, it auto spawns a new Claude code terminal and auto pipes in a dynamic prompt through the bash command telling it to follow all instructions in the linked https://t.co/Eyw2EtHjsm file. New session seamlessly picks up where the old session left off & the whole thing requires zero manual intervention. 
> 
> The idea here is that doc updates & code edits in a post compacted state are flawed because it forgot all the details and as such, Opus is inclined to make a lot of assumptions. So I solve this by having a pre-compact hook export the transcript JUST before compaction, then using sub-agents to scour the transcript for all the forgotten details. 
> 
> The systems a bit heavy - you'll use an extra ~50k tokens just executing these procedures, but the result is well worth it imo. It gives me completely flawless context transfer to a fresh session & its fully automated. 
> 
> Oh by the way, a bit off topic but if you combine this automated context passthrough system with the main elements of the Ralph workflow you get absolutely incredible results. In fact, the entire smart forking system was completely one-shotted with Ralph & this automated context management system. I didn't have to make a single change once it was finished - completely worked as intended out of the box.

> [!reply] @garybasin · 2026-01-21T18:07:36+00:00
> @PerceptualPeak Have to be careful forking historical sessions that may come loaded with context that’s now out of date …
> *1 likes*

> [!tip]+ :leftwards_arrow_with_hook: @PerceptualPeak · 2026-01-21T18:20:06+00:00

> A great observation & you're 100% correct! This was a primary concern of mine as well. Which is why I implemented an aggressive recency weight as part of the composite relevancy score calculation. So far in testing I have not run into a situation where it served me up an overly outdated session.
> 
> Here's an overview of how the relevancy score is calculated:


---

> [!metrics]- Engagement & Metadata
> **Likes:** 4,632 · **Replies:** 160 · **Reposts:** 297 · **Views:** 644,707
> **Engagement Score:** 21,340
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2012741829683224584](https://x.com/PerceptualPeak/status/2012741829683224584)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ⚠️ (0/3 analyzed — 3 photos, 0 videos)
  thread: ✅ (29 replies scraped)
  classification: ✅ ACT_NOW
```