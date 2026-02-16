# LEARNINGS.md — Techniques Catalog for Fresh Instances

> A quick-reference catalog of Claude Code techniques, organized by adoption status.
> For fresh Claude instances to understand what's available vs. what we're already using.

**Last Updated:** February 16, 2026

---

## ✅ Techniques We Use Daily

### Code-Tab-as-Orchestrator
- Single Claude Code instance handles planning + execution
- Plan mode (Shift+Tab) for strategic thinking before execution
- Subagents (Task tool) for parallel work
- **Replaced:** Former chat/code delegation pattern (Jan–Feb 2026)

### Session Boundaries (STATUS.json + /wrap-up)
- `STATUS.json` — machine-readable project state, read on cold start
- `/wrap-up` command — auto-populates stats from live DB
- Pre-compact hook — auto-stages STATUS.json before compaction
- Session context files — for complex multi-session cold starts

### MCP Servers
| Server | Purpose | Notes |
|--------|---------|-------|
| GitHub MCP | Repo management, file access | Cross-repo coordination |
| Filesystem MCP | Local file operations | Read/write/search |
| Claude-in-Chrome | Browser automation | Native, no third-party extensions |

### Quality-Filtered Export
Only export content that's been fully processed:
```sql
WHERE likes > 0 OR holistic_summary IS NOT NULL
```
Keeps vaults browsable — no placeholder clutter.

### Semantic Filenames
LLM generates `primary_keyword` for readable filenames:
- ❌ `2025-12-26-2004647680354746734.md`
- ✅ `2025-12-26-openrouter-integration.md`

### Research-First Heuristic
**Always search before building.** Best solutions often emerged after model training cutoff.
- Found VectCutAPI after 3+ days of failed CapCut reverse-engineering
- Search: "[tool] API automation [year]", sort GitHub by stars

---

## 🔄 Techniques We're Experimenting With

### Link Enrichment Pipeline
1. Extract URLs from text
2. Resolve shortlinks (t.co → real URL)
3. Fetch external content
4. LLM summarize
5. Surface in exports

### Vision Analysis for Screenshots
Tweets/videos with just an image are high-signal — the author is pointing you to something important. Run vision analysis to extract content.

### Opus 4.5 with Thinking
Boris (Claude Code creator): "Slower but less steering = faster overall"

### Slash Commands (Skills)
Location: `.claude/commands/`
Active commands: `/task-plan`, `/wrap-up`, `/fetch-bookmarks`, `/start-session`
Boris uses `/commit-push-pr` dozens of times daily. Inner-loop automation.

### Hooks
- **PreCompact** — Auto-updates STATUS.json before compaction (active)
- **SessionEnd** — Safety net if wrap-up wasn't called (active)
- **PostToolUse** — Auto-format code (not yet implemented)

### Permissions (settings.json)
Pre-allow safe bash commands: `git`, `gh` pre-allowed. Avoids `--dangerously-skip-permissions`.

### Agent Teams
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: true` in settings.json. Not yet tested for pipeline work.

---

## 📋 Techniques to Try Next

### Subagents for Pipeline Work
Task tool can spawn Explore/Bash/general-purpose agents. Untested for parallel enrichment runs.

### Teleport (`&`)
Hand off terminal session to web: `claude &`

### Ralph Wiggum
Plugin for auto-restore from compaction/clear. Useful for long-running tasks.

---

## ⏸️ Techniques We're Watching (Not Yet Convinced)

### Beads (@doodlestein)
Structured task/dependency system like Jira but for agents. Very comprehensive workflow with agent swarms, Agent Mail coordination.

**Why holding:** 
- Complex setup ($550/mo in subscriptions)
- Community pushback: "subagents are a gimmick", "agents maxing 🤝 built nothing"
- Want to see more success stories before investing

### Agent SDK (@mckaywrigley)
Build custom agents outside Claude Code. "Personal AGI" pitch.

**Why holding:**
- Different use case than our archive work
- Claude Code already handles our needs

### Voice/STT Loops (Eric Buess)
"Cardio coding" — coding via voice while mobile.

**Why holding:**
- Current workflow is text-heavy
- Not high priority

---

## 🏆 Key Insights from Boris (Claude Code Creator)

From his January 2, 2026 thread (45,567 likes):

1. **CLAUDE.md should be ~2.5k tokens** — covers bash commands, style, PR template
2. **Skills = Slash commands** — interchangeable terms
3. **Plan mode first** (shift+tab twice) → then auto-accept
4. **Team shares one CLAUDE.md** — checked into git, collaboratively updated
5. **5-10 parallel Claudes** — same repo, numbered tabs, notifications
6. **Opus 4.5 with thinking** — slower but less steering = faster overall
7. **Verification is the most important tip** — "2-3x quality with feedback loop"

---

## 📊 Engagement Leaders (What Community Validates)

| Author | Likes | Topic |
|--------|-------|-------|
| @bcherny | 45,567 | Claude Code creator's vanilla setup |
| @DejaVuCoder | 8,700 | Claude Code 2.0 guide |
| @mckaywrigley | 3,141 | Agent SDK / personal AGI |
| @EricBuess | 651 | LSP + hooks + subagents + Ralph Wiggum |
| @doodlestein | 648 | Beads + agent swarms |
| @zeroxBigBoss | 509 | The Handoff technique |

---

## 🔗 Quick Reference

| File | Purpose |
|------|---------|
| `STATUS.json` | Current project state (check first) |
| `CLAUDE.md` | Project context for any Claude instance |
| `PROJECT_DECISIONS.md` | Architectural decisions |
| `PROGRESS.md` | Personal adoption tracker |
| `plans/active/` | Current task plans |

---

*For a fresh instance: Read STATUS.json, then CLAUDE.md. Reference this file for technique options.*
