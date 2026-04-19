# Claude Code Tips Repository

## 🎯 First: Read STATUS.json

**On cold start**, read `STATUS.json` and then:
- If it has an `active_task`: read its handoff doc and execute.
- If no active task and user gave direct instructions: plan (Shift+Tab) then execute.
- If exploring techniques: read `LEARNINGS.md` for what's available.
- If adding tips: use the SQLite database at `data/claude_code_tips_v2.db`, not markdown files.

Live stats are in STATUS.json. The `/wrap-up` command and pre-compact hook keep it current.

---

## Project Purpose

A learning resource and reference for Claude Code best practices. Curated tips from the Claude Code community, quality-filtered into an Obsidian vault, with analysis and commentary. The goal is to synthesize community wisdom into actionable configurations.

This is a cross-project workspace. Work may bounce between `claude-code-tips` and `hall-of-fake`. Both use the code-tab-as-orchestrator model.

---

## 🔄 Code-Tab-as-Orchestrator

The Claude Code tab is the central orchestrator. It handles planning, strategy, execution, and review in a single context — no delegation docs.

**What's project-specific about this repo's setup:**
- Pre-compact hook at `.claude/hooks/pre-compact.sh` auto-preserves STATUS.json
- Session-end hook at `.claude/hooks/session-end.sh` updates recent_changes
- `/fetch-bookmarks` skill is the primary data ingestion command
- `/wrap-up` ritual commits incrementally and pushes at session end

---

## 🔍 Research-First Heuristic

**CRITICAL for automation tasks:** The best solutions often emerge **after** the model's training cutoff.

**Before reverse-engineering or building from scratch:**

1. Search the web for existing solutions
2. Check GitHub for "[tool name] API automation [current year]"
3. Look for MCP servers that integrate with target applications
4. Filter by recent activity (last 12 months)

**Why:** We spent 3+ days reverse-engineering CapCut's JSON format before discovering VectCutAPI (1.4k stars) via a simple web search.

---

## 🌐 Browser Automation: Claude-in-Chrome

Browser automation uses **Claude-in-Chrome** via the `/chrome` integration. Setup: run `/chrome` in Claude Code.

**Chrome contention is a real constraint:** Only one Claude instance can hold the Chrome extension connection at a time. With code-tab-as-orchestrator, this is fine because the code tab holds the connection exclusively. If you start a second Claude instance that needs Chrome, coordinate — don't blindly connect.

---

## 📊 Quality-Filtered Export Pattern

**Key principle:** Only export fully processed content to keep the Obsidian vault browsable.

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

Primary paths worth knowing (run `ls` or `tree` for current detail):

- `data/claude_code_tips_v2.db` — SQLite database, FTS5 enabled
- `Claude Code Tips/` — Obsidian vault (quality-filtered notes)
- `plans/active/` — current task plans
- `analysis/` — audit reports, reviews, one-off investigations
- `scripts/obsidian_export/` — export library shared with hall-of-fake
- `.claude/commands/` — project-specific skills

See `PROJECT_DECISIONS.md` for architectural history and `LEARNINGS.md` for the techniques catalog.

---

## Useful Scripts

```bash
# What's changed recently
python scripts/whats_new.py --days 7
```

---

*See `analysis/audits/2026-04-19-CLAUDE_trimmed.md` for audit history. This trimmed version produced from the 2026-04-18 audit by applying cuts recommended by @itsolelehmann's audit prompt.*
