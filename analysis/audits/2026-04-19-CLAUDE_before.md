# Claude Code Tips Repository

## 🎯 First: Check STATUS.json

**Before doing anything else**, read `STATUS.json` in this repo. It tells you:
- Current stats (tweet count, vault notes, etc.)
- What happened last session (recent_changes)
- What's known to be broken (known_issues)
- Active task, if any

This is a cross-project workspace. Work may bounce between `claude-code-tips` and `hall-of-fake`.

---

## Project Purpose

This repository is a learning resource and reference for Claude Code best practices. It contains:
- A curated collection of 468 tips from the Claude Code community
- 457 quality-filtered Obsidian notes with full enrichment
- Analysis and commentary from Claude instances
- Personal progress tracking for technique adoption

The goal is to synthesize community wisdom into actionable configurations.

## Current Date Awareness

**IMPORTANT**: Before researching, searching documentation, or looking up any information, always verify the current date. The current date context should be February 2026. Do not default to 2024 dates or assume outdated information is current.

---

## 🔄 Working Model: Code Tab as Orchestrator

**The Claude Code tab is the central orchestrator.** It handles planning, strategy, execution, and review in a single context. No delegation docs needed.

**Capabilities:**
- Plan mode (Shift+Tab) for strategic thinking before execution
- Direct DB access, git operations, script execution
- Claude-in-Chrome for browser automation (no contention)
- Subagents via Task tool for parallel work
- Skills/commands (`/task-plan`, `/wrap-up`, `/fetch-bookmarks`)
- Pre-compact hook auto-preserves STATUS.json

**Session boundaries:**
- Read `STATUS.json` on cold start
- Commit incrementally during work
- Run `/wrap-up` + `git push` at session end

**Historical note:** This project previously used a chat-tab/code-tab delegation pattern where Claude.ai wrote HANDOFF docs and Claude Code executed them. That pattern was retired Feb 2026 — see Decision 13 in PROJECT_DECISIONS.md.

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

**Chrome contention:** Only one Claude instance can hold the Chrome extension connection at a time. With the code-tab-as-orchestrator model, this is no longer an issue — the code tab holds the connection exclusively.

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
├── STATUS.json                  # Machine-readable project state (check first)
├── PROJECT_DECISIONS.md         # Architectural decisions log
├── LEARNINGS.md                 # Techniques catalog for fresh instances
├── PROGRESS.md                  # Personal adoption tracker
├── README.md                    # Public-facing documentation
├── data/
│   ├── claude_code_tips_v2.db  # SQLite database with FTS5
│   └── threads/                # Scraped thread JSON files
├── Claude Code Tips/            # Obsidian vault (457 quality notes)
│   ├── _dashboards/            # Dataview queries
│   └── attachments/            # Media files
├── scripts/
│   ├── obsidian_export/        # Export library (serves both projects)
│   ├── whats_new.py            # What's New reporting
│   └── ...
├── .claude/
│   ├── settings.json           # Permissions, hooks, agent teams flag
│   ├── hooks/                  # Pre-compact + session-end hooks
│   ├── references/             # Specs, analysis context docs
│   └── commands/               # Skills / slash commands
├── plans/
│   ├── active/                 # Current task plans
│   └── archive/                # Completed work
├── analysis/                   # Audit reports, reviews
└── assets/                     # Images for README
```

## Key Files

| File | Purpose |
|------|---------|
| `STATUS.json` | **Check first** — Machine-readable project state |
| `PROJECT_DECISIONS.md` | Why things are built the way they are |
| `LEARNINGS.md` | Techniques catalog (what's available vs. what we use) |
| `data/claude_code_tips_v2.db` | SQLite: tweets, replies, links, media |
| `Claude Code Tips/` | Obsidian vault (457 quality-filtered notes) |

## Data State

**Live stats are in STATUS.json.** The `/wrap-up` command and pre-compact hook keep it current.

---

## Your Task

You are a Claude instance in the code tab. Your job depends on context:

1. **If STATUS.json has an active_task:** Read its handoff doc and execute
2. **If the user gives direct instructions:** Plan (Shift+Tab) then execute
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

Both projects use the code-tab-as-orchestrator model.

---

## 🚀 Cold-Start Prompt

```
I'm continuing work on claude-code-tips (Twitter bookmark knowledge base).

Read STATUS.json for current state. Read CLAUDE.md for project conventions.

CURRENT FOCUS: [your focus]
```

---

## Verification

To confirm you've read these instructions, include "context-first" in your first response.

---

*Last updated: February 16, 2026*
