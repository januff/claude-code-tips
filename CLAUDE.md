# Claude Code Tips Repository

## 🎯 First: Check CURRENT_FOCUS.md

**Before doing anything else**, read `CURRENT_FOCUS.md` in this repo. It tells you:
- Which project is currently active (may be the sibling repo)
- Where the handoff docs are
- What happened last session

This is a cross-project workspace. Work may bounce between `claude-code-tips` and `hall-of-fake`.

---

## Project Purpose

This repository is a learning resource and reference for Claude Code best practices. It contains:
- A curated collection of 397 tips from the Claude Code community
- 94 quality-filtered Obsidian notes with full enrichment
- Analysis and commentary from Claude instances
- Personal progress tracking for technique adoption

The goal is to synthesize community wisdom into actionable configurations.

## Current Date Awareness

**IMPORTANT**: Before researching, searching documentation, or looking up any information, always verify the current date. The current date context should be early January 2026. Do not default to 2024 dates or assume outdated information is current.

---

## 🔄 Claude.ai ↔ Claude Code Delegation Pattern

**CRITICAL for complex tasks:** This project uses a delegation pattern between Claude.ai Projects and Claude Code CLI.

| Claude.ai Project | Claude Code CLI |
|-------------------|-----------------|
| Planning, decisions | Execution |
| Strategy discussion | API calls, file I/O |
| Writing HANDOFF.md | Database operations |
| Reviewing results | Git commits |

**Why:** Avoids context window bloat from large JSON/API responses. Prevents compaction loss of conversational context in Claude.ai.

**Flow:**
1. Claude.ai writes tasks to `HANDOFF.md`
2. User runs `claude` → "Read HANDOFF.md and execute"
3. Claude Code commits incrementally
4. Claude.ai reviews via GitHub MCP

**MCP Best Practice:** Only enable MCPs needed for current task.

**Key file:** `HANDOFF.md` — Check this for current tasks and completed work.

---

## 🏆 Boris Cherny's Tips (Claude Code Creator)

From @bcherny's January 2, 2026 thread (45,567 likes). **These are authoritative.**

| Tip | Notes |
|-----|-------|
| **CLAUDE.md ~2.5k tokens** | Covers bash commands, style, PR template |
| **Skills = Slash commands** | `.claude/commands/` — interchangeable terms |
| **Plan mode first** | Shift+Tab twice → iterate until plan is good |
| **Auto-accept after good plan** | "Claude can usually 1-shot it" |
| **Team shares one CLAUDE.md** | Checked into git, collaboratively updated |
| **5-10 parallel Claudes** | Same repo, numbered tabs, system notifications |
| **Opus 4.5 with thinking** | "Slower but less steering = faster overall" |
| **`/permissions` over `--dangerously-skip-permissions`** | Pre-allow safe commands |
| **PostToolUse hook for formatting** | "Handles last 10% to avoid CI errors" |
| **Verification is most important** | "2-3x quality with feedback loop" |
| **Subagents** | code-simplifier, verify-app |
| **Ralph Wiggum** | Auto-restore from compaction for long-running tasks |

---

## 🔍 Research-First Heuristic

**CRITICAL for automation tasks:** The best solutions often emerge **after** the model's training cutoff.

**Before reverse-engineering or building from scratch, ALWAYS:**

1. **Search the web** for existing solutions
2. **Check GitHub** for "[tool name] API automation [current year]"
3. **Look for MCP servers** that integrate with target applications
4. **Filter by recent activity** (last 12 months)

**Why:** We spent 3+ days reverse-engineering CapCut's JSON format before discovering VectCutAPI (1.4k stars) via a simple web search.

---

## 🌐 Browser Automation: Claude-in-Chrome

Browser automation uses **Claude-in-Chrome** (native `/chrome` integration). No third-party browser extensions needed.

**Setup:** Run `/chrome` in Claude Code to enable. Uses the built-in Chrome extension.

**Key tools:**
- `mcp__claude-in-chrome__tabs_context_mcp` — see available tabs
- `mcp__claude-in-chrome__javascript_tool` — execute JS in page context
- `mcp__claude-in-chrome__read_network_requests` — capture API calls
- `mcp__claude-in-chrome__navigate` — page navigation
- `mcp__claude-in-chrome__computer` — screenshots, clicks

**Chrome contention:** Only one Claude instance can hold the Chrome extension connection at a time. Claude Code should hold it during execution sessions. If the Claude.ai app is also connected, run `/chrome` → Reconnect to claim it.

---

## 📊 Quality-Filtered Export Pattern

**Key principle:** Only export fully processed content to keep vaults browsable.

```sql
WHERE likes > 0 OR holistic_summary IS NOT NULL
```

**Semantic filenames** from LLM-generated `primary_keyword`:
- ❌ `2025-12-26-2004647680354746734.md`
- ✅ `2025-12-26-openrouter-integration.md`

**Attachment-only content** (just a screenshot or link) is high-signal, not an edge case:
- Run vision analysis on screenshots
- Fetch and summarize linked content
- Generate keywords from extracted content

---

## Project Structure

```
/
├── CLAUDE.md                    # This file
├── HANDOFF.md                   # Current tasks for Claude Code
├── PROGRESS.md                  # Personal adoption tracker
├── LEARNINGS.md                 # Techniques catalog for fresh instances
├── README.md                    # Public-facing documentation
├── data/
│   ├── claude_code_tips_v2.db  # SQLite database with FTS5
│   └── threads/                # Scraped thread JSON files (70 threads)
├── Claude Code Tips/            # Obsidian vault (94 quality notes)
│   ├── Claude Dashboard/
│   │   └── Session Logs/       # Detailed session summaries
│   └── attachments/            # Media files
├── scripts/
│   ├── obsidian_export/        # Export library
│   ├── whats_new.py            # What's New reporting
│   └── ...
├── plans/
│   ├── archive/                # Completed handoffs
│   └── (active handoffs)
└── assets/                     # Images for README
```

## Key Files

| File | Purpose |
|------|---------||
| `HANDOFF.md` | **Check first** — Current tasks from Claude.ai |
| `PROGRESS.md` | Personal tracking of technique adoption |
| `LEARNINGS.md` | Techniques catalog (what's available vs. what we use) |
| `data/claude_code_tips_v2.db` | SQLite: tweets, replies, links, media |
| `Claude Code Tips/` | Obsidian vault (94 quality-filtered notes) |

## Data State (January 5, 2026)

| Metric | Value |
|--------|-------|
| Tweets in DB | 397 |
| Quality vault notes | 94 |
| Threads scraped | 70 |
| Total replies | 928 |
| Links resolved | 64 |
| Links with summaries | 24 |

---

## Your Task

You are a Claude instance being handed off this project. Your job depends on context:

1. **If HANDOFF.md has tasks:** Execute them in order, commit incrementally
2. **If continuing analysis:** Check `PROGRESS.md` for current adoption status
3. **If exploring techniques:** Read `LEARNINGS.md` for what's available
4. **If adding tips:** Use the SQLite database, not markdown files

---

## Extended Thinking

- "think" < "think hard" < "think harder" < "ultrathink"
- Reserve ultrathink for architectural decisions only
- Tab toggles thinking (sticky across sessions)

## Useful Commands

```bash
# Check current session context usage
/cost

# Manual compaction
/compact

# Toggle plan mode
Shift+Tab

# Toggle thinking
Tab

# What's new report
python scripts/whats_new.py --days 7
```

---

## Related Projects

| Project | Purpose | Status |
|---------|---------|--------|
| `claude-code-tips` | This repo — tip collection | Active |
| `hall-of-fake` | Sora video archive | Active |

Both projects share the Claude.ai ↔ Claude Code delegation pattern.

---

## 🚀 Cold-Start Prompt

```
I'm continuing work on claude-code-tips (Twitter bookmark knowledge base).

Read CLAUDE.md from Project Knowledge. For current tasks, check HANDOFF.md.

CURRENT FOCUS: [your focus]
```

---

## Verification

To confirm you've read these instructions, include "context-first" in your first response.

---

*Last updated: February 12, 2026*
