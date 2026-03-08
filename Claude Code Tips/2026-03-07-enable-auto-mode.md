---
tweet_id: "2030156251821392096"
created: 2026-03-07
author: "rohanpaul_ai"
display_name: "Rohan Paul"
primary_keyword: "--enable-auto-mode"
llm_category: "security"
tags:
  - type/screenshot
likes: 610
views: 154391
engagement_score: 1639
url: "https://x.com/rohanpaul_ai/status/2030156251821392096"
enrichment_complete: true
has_media: true
has_links: false
has_thread_context: false
---

> [!tweet] rohanpaul_ai · Mar 07, 2026
> Claude seems to be fixing a super annoying developer problem.
> 
> Anthropic announced a research preview feature called Auto Mode for Claude Code, expected to roll out by March 12, 2026. 
> 
> The idea is simple: let Claude automatically handle permission prompts during coding so developers don’t have to constantly approve every action.
> 
> Sstops those annoying permission prompts during long coding sessions. 
> 
> Before this, you had to use `--dangerously-skip-permissions` to work without interruptions. 
> 
> That method worked fine but took away all your safety nets. This new auto mode gives us a smarter option. 
> 
> Claude will take care of the specific permission choices on its own while still blocking threats like prompt injections. 
> 
> You can finally let long tasks run without watching your screen the whole time. 
> 
> Since it is still a research preview, you should run it inside isolated setups like sandboxes or containers for safety. 
> 
> Expect a small jump in token usage and delay, because the model needs extra time to process the security checks. 
> 
> Once available, you just type `claude --enable-auto-mode` to start. 
> 
> If you manage a team and need people to manually approve actions, you can restrict this feature using Mobile Device Management tools like Jamf and Intune or through configuration files.
>
> Likes: 610 · Replies: 63 · Reposts: 47

## Summary

Claude Code's upcoming Auto Mode (arriving by March 12, 2026) streamlines coding by automatically handling permission prompts, eliminating interruptions without sacrificing security. This is activated via the `claude --enable-auto-mode` command, letting you run long tasks unattended while Claude blocks threats.  For team environments needing manual approvals, Auto Mode can be restricted via MDM tools or configuration files; remember to use in isolated environments during the research preview.

## Keywords

**Primary:** `--enable-auto-mode` · auto mode, permissions, automatic permission handling, sandbox, containers, Jamf, Intune, mobile device management, MDM, security checks
## Media

![[attachments/screenshots/tweet_2030156251821392096_44.png]]

Enabling the auto mode in Claude Code.

**Focus Text:**
```
claude --enable-auto-mode
```

**Key Action:** Learn how to enable auto mode in Claude Code by running the command 'claude --enable-auto-mode'.

**Commands:** CLI, commands

<details>
<summary>Full OCR Text</summary>
<pre>
Claude

Hi,

A new permissions mode in Claude Code, auto mode, is launching in
research preview no earlier than March 12, 2026. Auto mode lets Claude
handle permission decisions during coding sessions, so developers can
run longer tasks without being interrupted by Claude asking for manual
approvals. Auto mode also includes additional safeguards against
prompt injections.

Auto mode is designed to be a safer alternative to bypassing
permissions entirely (--dangerously-skip-permissions), which is
commonly used by developers to prevent interruptions in long-running
tasks. Auto mode isn't perfect and it won't catch every action that could
be considered risky, so we recommend using it only in isolated
environments. It also slightly increases token usage, cost, and latency.

What you need to know:
By default, your users will be able to use auto mode by running “claude --enable-auto-mode”. No action is otherwise needed to enable your team
to use auto mode.
</pre>
</details>


---

> [!metrics]- Engagement & Metadata
> **Likes:** 610 · **Replies:** 63 · **Reposts:** 47 · **Views:** 154,391
> **Engagement Score:** 1,639
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2030156251821392096](https://x.com/rohanpaul_ai/status/2030156251821392096)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ℹ️ none
  media: ✅ (1/1 analyzed — 1 photo, 0 videos)
  thread: ℹ️ standalone
  classification: ❌ not classified
```