---
tweet_id: "2035312729427480840"
created: 2026-03-21
author: "hasantoxr"
display_name: "Hasan Toor"
primary_keyword: "github-repos"
llm_category: "tooling"
tags:
  - type/screenshot
likes: 5594
views: 500405
engagement_score: 36076
url: "https://x.com/hasantoxr/status/2035312729427480840"
enrichment_complete: true
has_media: true
has_links: true
has_thread_context: false
---

> [!tweet] hasantoxr · Mar 21, 2026
> Best GitHub repos for Claude code that will 10x your next project:
> 
> 1. Superpowers
> https://t.co/U5Y4BK9Lap
> 
> 2. Awesome Claude Code
> https://t.co/qcgoxU3Up2
> 
> 3. GSD (Get Shit Done)
> https://t.co/WfAhllWnTR
> 
> 4. Claude Mem
> https://t.co/XLQpwdnIWN
> 
> 5. UI UX Pro Max
> https://t.co/aQtGjMzKus
> 
> 6. n8n-MCP
> https://t.co/7le1aluZXH
> 
> 7. Obsidian Skills
> https://t.co/MUaoyUnasw
> 
> 8. LightRAG
> https://t.co/ye8z4UqaMc
> 
> 9. Everything Claude Code
> https://t.co/OAU9JE46Uz
>
> Likes: 5,594 · Replies: 130 · Reposts: 849

## Summary

This tip compiles a curated list of GitHub repositories offering tools and resources to significantly enhance your Claude Code workflows. These repositories provide skills, plugins, and agent orchestrators for tasks like managing context, generating UI/UX designs, creating n8n workflows, and optimizing agent performance. By leveraging resources like the 'Superpowers' plugin, `get-shit-done-cc` CLI tool, or 'claude-mem', developers can improve efficiency and build more sophisticated applications with Claude Code.

## Keywords

**Primary:** `github-repos` · github, repos, repositories, 10x, project
## Linked Resources

- **[GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub](https://github.com/hesreallyhim/awesome-claude-code)** · *github-repo*
  > This GitHub repository, 'awesome-claude-code', is a curated list of resources for enhancing the Claude Code workflow by Anthropic. It includes a wide range of tools, skills, hooks, slash commands, agent orchestrators, applications, and plugins designed to improve the Claude Code experience.

- **[GitHub - gsd-build/get-shit-done: A light-weight and powerful meta-prompting, context engineering and spec-driven development system for Claude Code by TÂCHES. · GitHub](https://github.com/gsd-build/get-shit-done)** · *github-repo*
  > The 'get-shit-done' (GSD) GitHub repository provides a lightweight system for meta-prompting, context engineering, and spec-driven development primarily for Claude Code. It helps overcome context rot and allows developers to build software using AI-powered coding tools like Claude Code, Gemini CLI, and others, trusted by engineers at major tech companies.

- **[GitHub - thedotmack/claude-mem: A Claude Code plugin that automatically captures everything Claude does during your coding sessions, compresses it with AI (using Claude's agent-sdk), and injects relevant context back into future sessions. · GitHub](https://github.com/thedotmack/claude-mem)** · *github-repo*
  > claude-mem is a Claude Code plugin that automatically captures coding session activity, compresses it using AI, and injects relevant context into future sessions, ensuring continuity of knowledge across coding sessions. It helps Claude maintain project understanding even after disconnections.

- **[GitHub - nextlevelbuilder/ui-ux-pro-max-skill: An AI SKILL that provide design intelligence for building professional UI/UX multiple platforms · GitHub](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** · *github-repo*
  > The UI UX Pro Max is an AI skill designed to provide intelligent design recommendations for building professional user interfaces and user experiences across various platforms. Version 2.0 introduces an AI-powered Design System Generator that analyzes project requirements and produces tailored design systems.

- **[GitHub - czlonkowski/n8n-mcp: A MCP for Claude Desktop / Claude Code / Windsurf / Cursor to build n8n workflows for you · GitHub](https://github.com/czlonkowski/n8n-mcp)** · *github-repo*
  > The GitHub repository `czlonkowski/n8n-mcp` hosts a Model Context Protocol (MCP) server for providing AI assistants like Claude with comprehensive access to n8n node documentation and properties. This allows the AI to understand and build n8n workflows by providing detailed knowledge about n8n's nodes, properties, operations, documentation, and example workflows.

- **[GitHub - kepano/obsidian-skills: Agent skills for Obsidian. Teach your agent to use Markdown, Bases, JSON Canvas, and use the CLI. · GitHub](https://github.com/kepano/obsidian-skills)** · *github-repo*
  > The `obsidian-skills` GitHub repository provides a set of agent skills that enable AI agents, including Claude Code, to interact with and manipulate Obsidian vaults. These skills allow agents to create, edit, and understand various Obsidian file types like Markdown, Bases, and JSON Canvas, as well as interact with Obsidian through its command-line interface.

- **[GitHub - affaan-m/everything-claude-code: The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond. · GitHub](https://github.com/affaan-m/everything-claude-code)** · *github-repo*
  > This GitHub repository provides a comprehensive system for optimizing the performance of AI agent harnesses, including Claude Code, Codex, and others. It offers tools and configurations for skills, instincts, memory optimization, security scanning, and research-first development, aiming to create production-ready agents.

## Media

![[attachments/screenshots/tweet_2035312729427480840_93.jpg]]

Demonstrates the features, installation, and sponsorship options for a software plugin named 'Superpowers'.


**Key Action:** Learn about the 'Superpowers' plugin and understand how it enhances coding agents by providing a workflow built on composable skills and initial instructions.


<details>
<summary>Full OCR Text</summary>
<pre>
README
Code of conduct
MIT license
Superpowers
Superpowers is a complete software development workflow for your coding agents, built on top of a set of
composable "skills" and some initial instructions that make sure your agent uses them.
How it works
It starts from the moment you fire up your coding agent. As soon as it sees that you're building something, it doesn't
just jump into trying to write code. Instead, it steps back and asks you what you're really trying to do.
Once it's teased a spec out of the conversation, it shows it to you in chunks short enough to actually read and
digest.
After you've signed off on the design, your agent puts together an implementation plan that's clear enough for an
enthusiastic junior engineer with poor taste, no judgement, no project context, and an aversion to testing to follow. It
emphasizes true red/green TDD, YAGNI (You Aren't Gonna Need It), and DRY.
Next up, once you say "go", it launches a subagent-driven-development process, having agents work through each
engineering task, inspecting and reviewing their work, and continuing forward. It's not uncommon for Claude to be
able to work autonomously for a couple hours at a time without deviating from the plan you put together.
There's a bunch more to it, but that's the core of the system. And because the skills trigger automatically, you don't
need to do anything special. Your coding agent just has Superpowers.
Sponsorship
If Superpowers has helped you do stuff that makes money and you are so inclined, I'd greatly appreciate it if you'd
consider sponsoring my opensource work.
Thanks!
Jesse
Installation
Note: Installation differs by platform. Claude Code or Cursor have built-in plugin marketplaces. Codex and
OpenCode require manual setup.
Claude Code Official Marketplace
Superpowers is available via the official Claude plugin marketplace
Install the plugin from Claude marketplace.
</pre>
</details>

![[attachments/screenshots/tweet_2035312729427480840_94.jpg]]

Installing and running the `get-shit-done-cc` CLI tool using npx.

**Focus Text:**
```
~$ npx get-shit-done-cc
```

**Key Action:** Install and initiate the Get Shit Done tool using the command `npx get-shit-done-cc`

**Commands:** npx get-shit-done-cc

<details>
<summary>Full OCR Text</summary>
<pre>
README
MIT license
Security
GET SHIT DONE
English 简体中文
A light-weight and powerful meta-prompting, context engineering and spec-driven development system for
Claude Code, OpenCode, Gemini CLI, Codex, Copilot, and Antigravity.
Solves context rot the quality degradation that happens as Claude fills its context window.
English | 简体中文
NPM V1.27.0
DOWNLOADS 159K/MONTH
TESTS PASSING
DISCORD JOIN
Xx
@GSD_FOUNDATION
$GSD DEXSCREENER
STARS 37K
LICENSE MIT
npx get-shit-done-cc@latest
Works on Mac, Windows, and Linux.
Terminal
~$ npx get-shit-done-cc
GSD
Get Shit Done v1.0.1
A meta-prompting, context engineering and spec-driven
development system for Claude Code by TÂCHES.
✓ Installed commands/gsd
✓ Installed get-shit-done
Done! Run /gsd:help to get started.
~$
</pre>
</details>


---

> [!metrics]- Engagement & Metadata
> **Likes:** 5,594 · **Replies:** 130 · **Reposts:** 849 · **Views:** 500,405
> **Engagement Score:** 36,076
>
> **Source:** tips · **Quality:** —/10
> **Curated:** ✗ · **Reply:** ✗
> **ID:** [2035312729427480840](https://x.com/hasantoxr/status/2035312729427480840)

```
enrichment:
  summary: ✅
  keywords: ✅
  links: ✅ (7/7 summarized)
  media: ✅ (2/2 analyzed — 2 photos, 0 videos)
  thread: ℹ️ standalone
  classification: ❌ not classified
```