---
name: daily-summary
description: >
  Generate a daily summary of project activity. Reads STATUS.json, today's git log,
  database stats, and active plan progress. Produces analysis/daily/YYYY-MM-DD.md.
  Use at end of day or as the first step in the morning briefing pipeline.
disable-model-invocation: true
---

# Daily Summary

Generate `analysis/daily/YYYY-MM-DD.md` for today's date.

## Data Collection

1. **Read STATUS.json** for current project state
2. **Git log for today:**
   ```bash
   git log --since="midnight" --oneline --stat
   ```
3. **Database stats** from `data/claude_code_tips_v2.db`:
   ```sql
   -- Total counts
   SELECT COUNT(*) as total_tweets FROM tweets;
   SELECT COUNT(*) as enriched FROM tweets WHERE holistic_summary IS NOT NULL;
   SELECT COUNT(*) as threads FROM threads;

   -- New today (tweets added since yesterday)
   SELECT COUNT(*) as new_today FROM tweets
   WHERE created_at >= date('now', '-1 day');

   -- Top new tips by engagement (last 24h additions)
   SELECT text, likes, author_username FROM tweets
   WHERE created_at >= date('now', '-1 day')
   ORDER BY likes DESC LIMIT 5;
   ```
4. **Active plan progress:** if `plans/active/TASK_PLAN.md` exists, read current phase and progress

## Output Template

Write to `analysis/daily/YYYY-MM-DD.md`:

```markdown
# Daily Summary: YYYY-MM-DD

## Commits Today
- [list of commits with short descriptions]
- (or "No commits today")

## Database Changes
| Metric | Value | Change |
|--------|-------|--------|
| Tweets | N | +N new |
| Enriched | N | +N |
| Threads | N | +N |

## Notable Tips
[Top tips by engagement added recently — 1-2 sentence summary each.
Flag any that relate to techniques in LEARNINGS.md or PROGRESS.md.]

## Active Plan Progress
[Current phase, steps completed, what's next — or "No active plan"]

## Open Questions
[Things discovered that need investigation, blockers, or decisions needed]
```

## After Writing

Do NOT commit the daily summary automatically. It is an analysis artifact — the user
decides when to commit analysis files.
