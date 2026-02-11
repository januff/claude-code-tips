# HANDOFF: Autonomous Bookmark Monitor

> **From:** Claude.ai Planning Instance
> **To:** Claude Code CLI
> **Date:** 2026-02-11
> **Goal:** Build toward an autonomous daily bookmark monitor by implementing community-validated techniques as building blocks.

---

## North Star

An automated cron process that:
1. Fetches new bookmarks from the Twitter/X "Claude" folder every morning
2. Runs the full enrichment pipeline (import → keywords → summaries → links → threads)
3. Generates a morning briefing analyzing new tips against existing knowledge
4. Proposes action items: tips to experiment with, relevance to active projects (claude-code-tips + hall-of-fake), or "noted and watching"
5. Delivers the briefing (email, file, or notification — TBD)

Each phase below is a building block toward this goal. Implement in order — each phase should be committed and working before starting the next.

---

## Phase 1: Skills Best Practices Foundation

**Why first:** Every subsequent phase creates skills/commands. Doing this first makes all of them better.

**Reference tip:** @doodlestein (478 likes, Jan 14) — "Before having Claude Code create a skill.md file, tell it to read [the best practices guide]"

### Tasks

1. **Fetch the skills best practices guide** referenced in the tip:
   - URL: `https://github.com/anthropics/claude-code/blob/main/SKILLS.md` (or wherever the canonical guide lives — search if needed)
   - Save a local copy to `.claude/references/skills-best-practices.md`

2. **Audit existing commands against best practices:**
   - `.claude/commands/wrap-up.md`
   - `.claude/commands/fetch-bookmarks.md`
   - `.claude/commands/start-session.md`
   - For each: Does it use progressive disclosure? Does it have reference files? Is it under the recommended token budget?

3. **Restructure commands to use reference files:**
   - Move large inline content (like API endpoint details in fetch-bookmarks) to `.claude/references/` files
   - Skills should reference these files rather than embedding everything inline
   - Pattern: `SKILL.md` is concise instructions + pointers to reference docs

4. **Create a meta-skill for skill creation:**
   - `.claude/commands/create-skill.md` — when invoked, reads the best practices guide first, then creates the skill
   - This is what @doodlestein recommends and what his "meta skill" system does

### Commit message
```
feat: skills foundation — best practices guide, reference files, audit existing commands
```

---

## Phase 2: File-Based Planning

**Why second:** Establishes the planning backbone that prevents drift in all subsequent phases.

**Reference tip:** @anthonyriera "Planning with files" (1,941 likes, Feb 2) — "Claude will come back to those files during the whole process and get a CONSTANT reminder of what should be done."

### Architecture Decision

We do NOT install the third-party `planning-with-files` skill. Instead, we adopt the *pattern* natively, adapted to our existing conventions:

| Their pattern | Our adaptation | Why |
|---|---|---|
| `task_plan.md` | `plans/active/TASK_PLAN.md` | Keep plans dir organized |
| `architecture.md` | Already have `PROJECT_DECISIONS.md` | Don't duplicate |
| `progress.md` | `STATUS.json` + `plans/active/PROGRESS.md` | Machine-readable + human-readable |

### Tasks

1. **Create the planning skill:** `.claude/commands/plan.md`
   - When invoked with a task description, creates:
     - `plans/active/TASK_PLAN.md` — goals, steps, success criteria, known risks
     - Updates `STATUS.json` with `active_task` field
   - Instructs Claude to re-read `TASK_PLAN.md` after every major step
   - Instructs Claude to update progress in the plan file as work proceeds

2. **Add plan-awareness to existing commands:**
   - `/wrap-up` should check for active plan and note progress against it
   - `/start-session` should check for active plan and resume from where it left off

3. **Add cleanup convention:**
   - When a plan is complete, move `plans/active/TASK_PLAN.md` → `plans/archive/` with date prefix
   - The plan file itself becomes part of the project's institutional memory

### Commit message
```
feat: file-based planning — /plan command, plan-aware wrap-up and start-session
```

---

## Phase 3: Pre-Compact Hook + Automatic Wrap-Up

**Why third:** Prevents context loss during the long sessions that subsequent phases will require.

**Reference tips:**
- @pauloportella_ (105 likes) — "turn this into a pre auto compact hook"
- @zarazhangrui (2,965 likes) — `/handover` command for session context preservation
- @PerceptualPeak (4,632 likes) — pre-compact hook exports transcript before compaction

### Tasks

1. **Create pre-compact hook:** `.claude/hooks/pre-compact.sh`
   ```
   Hook type: PreCompact
   Action: Run /wrap-up automatically before compaction happens
   ```
   This ensures STATUS.json is always updated, even if the user forgets.

2. **Create stop hook:** `.claude/hooks/stop.sh`
   ```
   Hook type: Stop (fires when Claude Code session ends)
   Action: Check if STATUS.json was updated this session. If not, run a minimal wrap-up.
   ```

3. **Configure hooks in `.claude/settings.json`:**
   ```json
   {
     "hooks": {
       "PreCompact": [".claude/hooks/pre-compact.sh"],
       "Stop": [".claude/hooks/stop.sh"]
     }
   }
   ```

4. **Enhance /wrap-up for hook context:**
   - When triggered by hook (vs manually), use a shorter format
   - Always update `STATUS.json`
   - If an active plan exists, note progress against it

### Important Notes
- The hook should be lightweight — avoid expensive DB queries that slow down compaction
- Pre-compact hook fires before the compaction summary is generated, so it has full context
- Test by running a session, letting it compact naturally, and verifying STATUS.json was updated

### Commit message
```
feat: automatic wrap-up — pre-compact hook, stop hook, settings.json configuration
```

---

## Phase 4: Compounding Summaries (Daily → Weekly → Goals Audit)

**Why fourth:** Builds the reporting infrastructure that the autonomous monitor will use.

**Reference tip:** @TaylorPearsonMe (225 likes, Feb 9) — "Each piece took a few minutes to set up because the building blocks were already there."

### Architecture

```
Per-session:  /wrap-up → STATUS.json + plans/active/TASK_PLAN.md
     ↓
Daily:        /daily-summary → analysis/daily/YYYY-MM-DD.md
     ↓
Weekly:       /weekly-review → analysis/weekly/YYYY-Wnn.md
     ↓
On-demand:    /goals-audit → compare weekly against LEARNINGS.md adoption targets
```

### Tasks

1. **Create `/daily-summary` command:** `.claude/commands/daily-summary.md`
   - Reads: `STATUS.json`, git log for today, any active plan progress
   - Produces: `analysis/daily/YYYY-MM-DD.md` with:
     - What changed in the DB (new tweets, enrichments)
     - What was committed
     - Notable new tips (high engagement, relevant to our workflow)
     - Open questions / things to investigate
   - This is the precursor to the morning briefing

2. **Create `/weekly-review` command:** `.claude/commands/weekly-review.md`
   - Reads: Last 7 daily summaries
   - Produces: `analysis/weekly/YYYY-Wnn.md` with:
     - Aggregate stats (tweets added, vault growth, threads scraped)
     - Top tips by engagement from the week
     - Technique adoption progress (cross-ref with PROGRESS.md)
     - Recommendations for next week

3. **Create `/goals-audit` command:** `.claude/commands/goals-audit.md`
   - Cross-references:
     - `LEARNINGS.md` (what we said we'd try)
     - `plans/PROGRESS.md` (what we've actually adopted)
     - Recent daily/weekly summaries (what we've been doing)
   - Flags gaps: "You said you'd try X but haven't touched it in 3 weeks"
   - Flags opportunities: "New tip Y has 4,632 likes and relates to your pending item Z"

4. **Create `analysis/` directory structure:**
   ```
   analysis/
   ├── daily/
   ├── weekly/
   └── commentary/     (existing, keep)
   ```

### Commit message
```
feat: compounding summaries — daily, weekly, goals-audit commands
```

---

## Phase 5: Cross-Model Review

**Why fifth:** Quality gate for the autonomous pipeline's outputs.

**Reference tip:** @jarrodwatts (866 likes, Jan 13) — Claude Code + Codex review loop. Multiple commenters noted a skill-based approach is simpler than MCP.

### Architecture Decision

Use a **skill-based approach**, not the `claude-delegator` MCP plugin. Rationale:
- Less context window overhead (no MCP tool descriptions loaded at startup)
- Simpler setup (no additional server process)
- Works with any model that has a CLI (codex, opencode, gemini CLI)

### Tasks

1. **Create `/review` command:** `.claude/commands/review.md`
   - Takes: a file path or git diff as input
   - Shells out to a second model (configurable — default: `codex`)
   - Prompt to reviewer: "Review this code/plan for: correctness, edge cases, missed opportunities, architectural concerns"
   - Returns review inline and saves to `analysis/reviews/`

2. **Create `/review-plan` variant:** `.claude/commands/review-plan.md`
   - Specifically for reviewing TASK_PLAN.md before execution
   - Asks the reviewer: "What's missing? What will go wrong? What would you do differently?"
   - Saves reviewer feedback, then Claude Code addresses it

3. **Make review optional in pipeline:**
   - The autonomous monitor (Phase 7) can optionally run `/review` on its morning briefing before delivery
   - This catches hallucinated analysis or missed context

### Prerequisites
- User needs `codex` CLI installed (or alternative reviewer model)
- If no reviewer available, commands should degrade gracefully (skip review, note it was skipped)

### Commit message
```
feat: cross-model review — /review and /review-plan commands
```

---

## Phase 6: Obsidian as Export Layer (Lightweight)

**Why sixth:** Keeps vault useful without over-investing. SQLite remains source of truth.

### Architecture Decision

**SQLite is the source of truth. Obsidian is a read-only export. No bidirectional sync.**

For interactive work (tagging, filtering, editing), a custom web UI over SQLite is better. The Hall of Fake project already proved this. Eventually claude-code-tips gets its own web UI too.

Obsidian serves two purposes:
1. Portable reading (mobile, offline)
2. Graph view for discovering connections between tips

### Tasks

1. **If Obsidian 1.12 is available:** Enable CLI, test basic queries from Claude Code
   - `obsidian-cli orphans` — find unlinked notes
   - `obsidian-cli query` — run base queries against the vault
   - Add to `/start-session` as an optional vault health check

2. **Improve export quality:**
   - Current export puts all 449 notes flat — consider subdirectories by topic cluster
   - Add bidirectional links between related tips (same author, same topic, tip references another tip)
   - Add adoption status tags from PROGRESS.md so vault reflects what we're using

3. **Do NOT do:**
   - Build Obsidian plugins
   - Set up bidirectional sync
   - Make Obsidian the primary interface
   - Invest heavily in Dataview queries (these are fragile and hard to maintain)

### Commit message
```
feat: obsidian export improvements — topic clusters, adoption tags, inter-note links
```

---

## Phase 7: Autonomous Bookmark Monitor (Capstone)

**Why last:** Uses everything built in Phases 1-6.

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                   CRON (daily, 7am)                  │
│                                                      │
│  1. /fetch-bookmarks                                 │
│     └── Chrome auth → GraphQL → import to SQLite     │
│                                                      │
│  2. Enrichment pipeline                              │
│     ├── enrich_keywords.py (Gemini)                  │
│     ├── enrich_summaries.py (Gemini)                 │
│     ├── enrich_links.py (fetch + summarize)          │
│     └── Thread scraping (for high-signal tweets)     │
│                                                      │
│  3. Analysis                                         │
│     ├── Compare new tips against LEARNINGS.md        │
│     ├── Compare against PROGRESS.md adoption status  │
│     ├── Cross-reference with hall-of-fake needs      │
│     └── Categorize: experiment / watch / note        │
│                                                      │
│  4. /daily-summary → morning briefing                │
│     ├── New tips summary with engagement scores      │
│     ├── Proposed actions (with rationale)             │
│     ├── Relevance to active projects                 │
│     └── Optional: /review via cross-model check      │
│                                                      │
│  5. Deliver briefing                                 │
│     ├── Write to analysis/daily/YYYY-MM-DD.md        │
│     ├── Optional: email via sendmail/API             │
│     ├── Optional: Telegram notification              │
│     └── Update STATUS.json                           │
│                                                      │
│  6. /wrap-up (automatic via hook)                    │
│                                                      │
│  7. Export vault (weekly, not daily)                  │
│     └── python scripts/export_tips.py                │
└─────────────────────────────────────────────────────┘
```

### Tasks

1. **Create the orchestrator script:** `scripts/daily_monitor.py`
   - Runs the full pipeline above
   - Handles errors gracefully (Twitter auth expired? Skip fetch, still analyze)
   - Logs everything to `analysis/daily/`
   - Respects rate limits (Gemini, Twitter GraphQL)

2. **Create the analysis engine:** `scripts/analyze_new_tips.py`
   - Input: list of tweet IDs added since last run
   - Cross-references against:
     - `LEARNINGS.md` — does this tip relate to a technique we're watching?
     - `plans/PROGRESS.md` — does this tip relate to something we've adopted or want to try?
     - Hall-of-fake needs (read via `januff/hall-of-fake/STATUS.json`)
   - Output: structured analysis with categories:
     - 🔴 **Act now** — high-signal tip directly applicable to current work
     - 🟡 **Experiment candidate** — interesting technique, worth a spike
     - 🟢 **Noted** — good to know, no action needed
     - ⚪ **Noise** — low-signal, skip

3. **Create the briefing generator:** `scripts/generate_briefing.py`
   - Takes analysis output, formats as readable morning report
   - Includes: tip summaries, engagement metrics, proposed actions, context links
   - Saves to `analysis/daily/YYYY-MM-DD-briefing.md`

4. **Set up cron:**
   ```bash
   # In user's crontab
   0 7 * * * cd ~/Development/claude-code-tips && claude --chrome -p "Run /daily-monitor" 2>&1 >> logs/monitor.log
   ```
   - Requires: Mac stays awake (or wakes for cron — `pmset` tip from the collection)
   - Requires: Chrome session with Twitter auth active
   - Fallback: if Chrome auth fails, still analyze any tips fetched manually the day before

5. **Handle the Chrome auth problem:**
   - Twitter auth tokens expire
   - Options:
     a. Accept manual refresh (open Chrome, visit Twitter, tokens refresh)
     b. Use `pmset` to wake Mac, open Chrome briefly, then run pipeline
     c. Skip fetch on auth failure, still run analysis on existing data
   - Start with (c) — the monitor is useful even without daily fetch

### Open Questions
- **Delivery mechanism:** File-only? Email? Telegram? Start with file, add notification later.
- **Frequency:** Daily is good for fetch. Analysis could be triggered on-demand too.
- **Hall-of-fake integration:** How deep? Start with just reading its STATUS.json for cross-project context.
- **Token budget:** Full pipeline (keywords + summaries + links for ~5-10 new tweets/day) is probably $0.50-1.00/day via Gemini. Acceptable?

### Commit message
```
feat: autonomous bookmark monitor — daily pipeline, analysis engine, briefing generator
```

---

## Implementation Order Summary

| Phase | Effort | Time Est. | Dependencies |
|-------|--------|-----------|--------------|
| 1. Skills foundation | Low | 30 min | None |
| 2. File-based planning | Low | 45 min | Phase 1 |
| 3. Pre-compact hooks | Low | 30 min | Phase 2 |
| 4. Compounding summaries | Medium | 1-2 hrs | Phases 1-3 |
| 5. Cross-model review | Medium | 1 hr | Phase 1 |
| 6. Obsidian export improvements | Low | 45 min | None |
| 7. Autonomous monitor | Medium-High | 3-4 hrs | Phases 1-4 |

Total estimated effort: ~8-10 hours across multiple sessions.

---

## Source of Truth Principle

Throughout all phases:
- **SQLite** (`data/claude_code_tips_v2.db`) is the single source of truth for tip data
- **STATUS.json** is the single source of truth for project state
- **LEARNINGS.md + PROGRESS.md** are the single source of truth for technique adoption
- **Obsidian vault** is a read-only export, regenerated periodically
- **`analysis/`** is append-only — daily/weekly files accumulate, never overwritten
- **`plans/active/`** has at most one active plan — completed plans move to archive

---

*This handoff is designed to be executed by Claude Code in order. Each phase produces working, committed code before the next begins. The autonomous monitor at the end uses everything built in Phases 1-6.*
