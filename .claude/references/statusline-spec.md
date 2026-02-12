# Status Line Specification

> Reference doc for Claude Code status line configuration.
> Implement via `.claude/statusline.sh` or equivalent hook.

---

## Layout: Three Lines

```
LINE 1 — Project Pulse
LINE 2 — Session Mechanics
LINE 3 — Rotating Quote
```

---

## Line 1: Project Pulse

Data sources: `STATUS.json`, SQLite DB (`data/claude_code_tips_v2.db`)

| Field | Source | Format | Example |
|-------|--------|--------|---------|
| Project name | hardcoded | plain text | `claude-code-tips` |
| Active handoff | STATUS.json → active_task.handoff | 📋 short name (strip path/prefix) | `📋 obsidian-audit` |
| Tweet count | DB: `SELECT COUNT(*) FROM tweets` | 🐦 count | `🐦 468` |
| Days since fetch | STATUS.json → key_dates.last_bookmark_fetch | parenthetical relative | `(1d)` |
| Enrichment coverage | DB: % with keywords / % with summaries / % with media analysis | `enriched: NN/NN/NN` | `enriched: 98/96/??` |
| Last wrap-up | STATUS.json → updated_at | relative time | `wrapped: 2h ago` |

When no active handoff: show `📋 none`
When enrichment % is unknown or 0: show `??`

**Example:**
```
claude-code-tips | 📋 obsidian-audit | 🐦 468 (1d) | enriched: 98/96/?? | wrapped: 2h ago
```

---

## Line 2: Session Mechanics

Data sources: Claude Code environment, git, system

| Field | Source | Format | Example |
|-------|--------|--------|---------|
| Model | Claude Code env | short name | `opus-4.6` |
| Thinking level | Claude Code env (if available) | 🧠 + level | `🧠med` |
| Context usage | Claude Code env | `ctx NN%` | `ctx 54%` |
| Git branch + status | `git` commands | 🌿 branch + clean/dirty/+N | `🌿main clean` |
| Active agents | Agent teams status | name list or "solo" | `solo` or `enricher, auditor` |
| Weekly usage | Plan limit tracking | `week: used/limit` | `week: 62/100` |

Notes:
- Thinking level: show if available, omit if not exposed
- Active agents: show "solo" when no agent teammates are running. When agent teams are
  enabled, show teammate names (not just count) so you know who's doing what
- Weekly usage: may need hardcoded plan tier if API doesn't expose it. Pro plan = 100
  Opus messages/week (verify current limits). Show as fraction of weekly allowance.
- Git dirty status: "clean" if working tree is clean, "+3" if 3 uncommitted changes,
  "ahead 2" if unpushed commits exist

**Example:**
```
opus-4.6 🧠med | ctx 54% | 🌿main clean | solo | week: 62/100
```

---

## Line 3: Rotating Quote

Data source: SQLite DB

### Query:
```sql
SELECT full_text, author_handle
FROM tweets
WHERE likes > 500
  AND full_text IS NOT NULL
  AND LENGTH(full_text) < 200
ORDER BY RANDOM()
LIMIT 1;
```

### Format:
```
💬 "{truncated text}" — @handle
```

### Rules:
- Truncate to ~100 chars if needed (break at word boundary, add "…")
- Only pull from tweets with >500 likes (community-validated signal)
- Only tweets with text under 200 chars (avoid multi-paragraph threads)
- Refresh on each status line update (new quote every refresh cycle)
- Strip URLs from the displayed text (they clutter the status line)
- Strip newlines — flatten to single line

### Stretch goal:
A contextual mode where the quote is selected based on current work context.
For example, if the active handoff mentions "enrichment," prefer quotes about
data pipelines or enrichment techniques. This would use a simple keyword match
against the handoff description, not a full LLM call.

---

## Implementation Notes

### File location:
`.claude/statusline.sh` — bash script sourced by Claude Code

### Refresh strategy:
- Read STATUS.json on every refresh (it's a small file)
- Query DB sparingly — cache enrichment percentages for 5 minutes
- Git status on every refresh (fast operation)
- Quote rotation on every refresh (single random SELECT is cheap)

### Dependencies:
- `sqlite3` CLI (for DB queries)
- `jq` (for STATUS.json parsing)
- `git` (for branch/status)
- Access to `data/claude_code_tips_v2.db` (relative path from repo root)

### Emoji usage:
Minimal and functional — emojis serve as visual anchors to scan quickly:
- 📋 = active task
- 🐦 = tweet data
- 🧠 = thinking level
- 🌿 = git
- 💬 = quote

No decorative emojis. Every emoji marks a data field.

### Error handling:
- If STATUS.json is missing: show `📋 no status`
- If DB is missing: show `🐦 ?? | enriched: ??/??/??`
- If git fails: show `🌿 ??`
- If no qualifying quotes exist: show `💬 "Verification is the most important tip" — @bcherny` (hardcoded fallback)

---

## Configuration

### Claude Code settings.json addition:
```json
{
  "statusline": {
    "script": ".claude/statusline.sh",
    "refresh_interval": 30
  }
}
```

(Verify the actual settings.json key for status lines — this may differ based on
Claude Code version.)

---

*Spec written by Claude.ai planning instance, 2026-02-12.*
*For implementation by Claude Code session.*
