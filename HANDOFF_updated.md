# Cross-Project Handoff

**For Claude Desktop or Claude.ai Project interfaces.**

## Project Knowledge Files

Add these files to your Claude.ai Project Knowledge:

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `CLAUDE.md` | Project context for Claude instances | After major changes |
| `PROJECT_DECISIONS.md` | Cross-project decisions & history | After milestones |
| `ultra_compact.json` (Hall of Fake) | Video inventory (1,320 clips) | After adding videos |

---

## Active Projects

### claude-code-tips
**Purpose:** Twitter bookmark knowledge base — tips about Claude Code

| Metric | Value |
|--------|-------|
| Tweets | 397 |
| Quality vault notes | 94 |
| Threads scraped | 70 |
| Replies | 928 |

**Key files:**
- `data/claude_code_tips_v2.db` — SQLite with FTS5
- `vault/` — Obsidian export (94 quality notes)
- `LEARNINGS.md` — Techniques catalog

**Current state:** Fully enriched, quality-filtered vault export working.

---

### Hall of Fake
**Purpose:** Sora AI video archive + CapCut automation

| Metric | Value |
|--------|-------|
| Videos | 1,320 |
| With analysis | 99.6% |
| CapCut Forge | Clone-based ✅ |

**Key files:**
- `hall_of_fake.db` — SQLite with FTS5
- `scripts/capcut_forge.py` — Project generator
- `capcut_reference/blessed_template/` — Clone source

**Current state:** CapCut Forge working. Needs audit for potential Obsidian export.

---

## Delegation Pattern

| Claude.ai Project | Claude Code CLI |
|-------------------|-----------------|
| Planning, decisions | Execution |
| Strategy discussion | API calls, file I/O |
| Writing HANDOFF.md | Database operations |
| Reviewing results | Git commits |

**Flow:**
1. Claude.ai writes tasks to `HANDOFF.md`
2. User runs `claude` → "Read HANDOFF.md and execute"
3. Claude Code commits incrementally
4. Claude.ai reviews via GitHub MCP

---

## Next Session: Hall of Fake Audit

**Goal:** Check data state, consider applying claude-code-tips patterns.

**Questions to answer:**
1. When was last Sora likes refresh?
2. Should we create Obsidian vault export?
3. Apply quality filter + semantic filenames?

**Cold-start prompt:**
```
I'm continuing work on Hall of Fake (Sora video archive).

Read CLAUDE.md and PROJECT_DECISIONS.md from Project Knowledge.

CURRENT FOCUS: Audit data state and consider applying patterns from claude-code-tips:
- Quality-filtered Obsidian export
- Semantic filenames from primary_subject
- What's New reporting

Start by querying the database for current stats.
```

---

## Quick Reference

| Repo | HANDOFF.md |
|------|------------|
| claude-code-tips | https://github.com/januff/claude-code-tips/blob/main/HANDOFF.md |
| hall-of-fake | https://github.com/januff/hall-of-fake/blob/main/HANDOFF.md |

---

*Last updated: January 5, 2026*
