# LEARNINGS.md — Techniques Catalog for Fresh Instances

> A quick-reference catalog of Claude Code techniques, organized by adoption status.
> For fresh Claude instances to understand what's available vs. what we're already using.

**Last Updated:** March 8, 2026

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
| Codex MCP | OpenAI GPT integration | `claude mcp add --scope user --transport stdio codex -- codex mcp-server` |
| Scheduled Tasks | Desktop recurring tasks | Cron-based, survives restarts |

### Scheduled Tasks (Desktop)
Three daily fetches configured (11am local):
- `fetch-claude-code-tips` — X bookmarks + enrichment + analysis + vault export
- `fetch-hall-of-fake` — Sora likes + video processing + clustering + vault export
- `fetch-book-queue` — X bookmarks + Libby reading list + cross-reference + enrichment

Managed via `mcp__scheduled-tasks__*` tools. Task definitions at `~/.claude/scheduled-tasks/`.

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
- **PreCompact** — Auto-updates STATUS.json before compaction (active, command-type only)
- **SessionEnd** — Safety net if wrap-up wasn't called (active, command-type only)
- **PostToolUse** — Auto-format code (not yet implemented)
- **HTTP Hooks** — New alternative to command hooks. POST events to a URL, get JSON responses. Supports 8 of 17 events (PreToolUse, PostToolUse, PermissionRequest, Stop, etc.). PreCompact/SessionEnd are command-only for now. Enables web dashboards, mobile monitoring, cross-instance state via DB. See research notes for full event matrix.

### Auto-Memory (MEMORY.md)
- Path: `~/.claude/projects/<project-hash>/memory/MEMORY.md`
- First 200 lines auto-loaded every session (hard cap)
- Claude decides what's worth saving (selective, not every session)
- **Orthogonal to STATUS.json**: memory = stable patterns/preferences; STATUS.json = volatile session state
- Survives compaction (re-read from disk, never summarized)
- Per-project, machine-local, plain markdown, editable anytime

### Prompt Stashing
- `Ctrl+S` stashes current draft, lets you fire off a quick question
- Auto-restores after submission. Single-slot, session-scoped.
- `Ctrl+G` opens prompt in external editor for longer edits
- `Ctrl+R` reverse history search

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
Official Anthropic plugin (`anthropics/claude-code/plugins/ralph-wiggum`). Uses Stop hook to loop Claude on a task until completion promise is met. Solves session continuity, not compaction.

### /loop (Session-Scoped Scheduling)
Boris's new command (10.3k likes). Schedule recurring tasks for up to 3 days within a session. Good for ephemeral monitoring (PR babysitting, CI watching). NOT suitable for cross-session automation — terminal must stay open, dies on restart. Use Desktop Scheduled Tasks instead.

### Auto Mode (`--enable-auto-mode`)
Research preview expected ~March 12, 2026. Smarter than `--dangerously-skip-permissions` — handles permission prompts while blocking prompt injection. Useful for long-running unattended tasks.

### Cross-Model Review (Codex MCP)
Codex MCP installed (`~/.claude.json`). Two tools: `codex(prompt)` and `codex-reply(prompt, threadId)`. Community patterns: super-review (8-dimension parallel review), 5-expert delegator, model-agnostic PAL server. GPT-5.4 available through it.

### HTTP Hook Dashboard
Build a web server that receives PostToolUse/Stop/PreToolUse events from all 3 projects. Enables live progress monitoring from mobile, cross-project activity feed, permission management. See HTTP hooks research for full architecture.

### A-Z Style Testing (Book Queue)
Generate multiple style sheets / design options for Book Queue app. Use different models to propose designs. User toggles between them to find preferred aesthetic. Impeccable v1.1 is a potential tool for this. "Forensic style analyst" prompt (from @heyrobinai) could extract Style DNA from liked designs.

### Chief of Staff Pattern
Jim Prosser's system: overnight automations (email triage, drive times), AM Sweep (task classification + 6 parallel subagents), Time Block (geographically-optimized schedule). Key insight: **dispatch/prep/yours/skip** framework — system never sends, only drafts. Built by non-programmer in 36 hours. 130-195 hours/year saved.

---

## ⏸️ Techniques We're Watching (Not Yet Convinced)

### Persistent Memory Category (Community Solutions)
Multiple competing approaches exist — track all, adopt the right combination:
| Solution | Approach | Status |
|----------|----------|--------|
| Auto-memory (built-in) | MEMORY.md, 200-line cap | **Using now** |
| STATUS.json + PreCompact | Structured state snapshots | **Using now** |
| QMD + /recall (@ArtemXTech) | BM25/semantic search over sessions | Watching |
| Total Recall | Cross-session semantic memory via QMD | Watching |
| Ghost | Session capture → git notes → QMD | Watching |
| Claude-Mem | Auto-capture, AI-compressed, injected | Watching |
| Context Handoff | Survives both /compact and /clear | Watching |
| Smart Ralph | Spec-driven + structured compaction | Watching |
| Indexed Transcript Refs (#26771) | Compact summaries with line-range pointers | **Most promising — would close biggest gap** |

**Our position:** Keep STATUS.json hook. Watch for #26771. Re-evaluate when indexed transcript references ship. The trajectory is toward compaction + memory "just working" in 3-6 months, but not there yet.

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

### Desktop Apps Trend (@weswinder, 8k likes)
"Stop building web apps, start building desktop apps." High engagement, unclear actionability. Our projects are local-first already (SQLite, Obsidian). Watch whether this becomes a standing prerogative for new projects or remains opinion.

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

From Lenny's Podcast (March 6, 2026, ~90 min):

8. **Boris hasn't edited code by hand since Nov 2025** — ships 10-30 PRs daily
9. **200% productivity gain at Anthropic** — unprecedented in developer tooling history
10. **Underfund teams on purpose** — one engineer instead of five, forces AI delegation
11. **Unlimited tokens** — some engineers spend $100k+/mo. Token cost < salary. Don't kill ideas early.
12. **The Bitter Lesson** — general model always wins. Don't build strict orchestration; give model tools and a goal.
13. **Build for the model 6 months out** — product-market fit will be weak for months, but the model catches up
14. **`/loop` released** (10.3k likes) — session-scoped recurring tasks, up to 3 days

---

## 📊 Engagement Leaders (What Community Validates)

| Author | Likes | Topic |
|--------|-------|-------|
| @bcherny | 45,567 / 10,342 | Claude Code creator's vanilla setup / /loop |
| @DejaVuCoder | 8,700 | Claude Code 2.0 guide |
| @weswinder | 8,041 | Desktop apps over web apps |
| @thejayden | 6,342 | Chief of Staff article (Jim Prosser) |
| @DataChaz | 6,259 | Perfect prompt anatomy |
| @nicopreme | 5,311 | Visual Explainer agent skill |
| @chintanturakhia | 5,151 | Frequently-run prompt |
| @mckaywrigley | 3,141 | Agent SDK / personal AGI |
| @ArtemXTech | 2,703 | Grep Is Dead / QMD + /recall |
| @RayFernando1337 | 2,465 | Skill-creator update |
| @dickson_tsai | 2,262 | HTTP hooks (Anthropic engineer) |
| @adocomplete | 2,209 | Prompt stashing (Ctrl+S) |
| @AnishA_Moonka | 2,002 | Boris on Lenny's Podcast notes |

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
