---
name: weekly-review
description: >
  Generate a weekly review by aggregating the last 7 daily summaries. Produces
  analysis/weekly/YYYY-Wnn.md with stats, top tips, adoption progress, and
  recommendations. Use at end of week or on-demand for a broader view.
disable-model-invocation: true
---

# Weekly Review

Generate `analysis/weekly/YYYY-Wnn.md` for the current ISO week.

## Data Collection

1. **Read daily summaries** from `analysis/daily/` for the last 7 days:
   ```bash
   ls -1 analysis/daily/*.md | tail -7
   ```
   If fewer than 7 exist, use all available. If none exist, fall back to git log and DB queries.

2. **Aggregate stats from database** (`data/claude_code_tips_v2.db`):
   ```sql
   -- Growth this week
   SELECT COUNT(*) FROM tweets WHERE created_at >= date('now', '-7 days');
   SELECT COUNT(*) FROM threads WHERE scraped_at >= date('now', '-7 days');

   -- Top tips by engagement this week
   SELECT text, likes, author_username FROM tweets
   WHERE created_at >= date('now', '-7 days')
   ORDER BY likes DESC LIMIT 10;
   ```

3. **Git log for the week:**
   ```bash
   git log --since="7 days ago" --oneline --stat
   ```

4. **Read `plans/PROGRESS.md`** for technique adoption status

## Output Template

Write to `analysis/weekly/YYYY-Wnn.md`:

```markdown
# Weekly Review: YYYY-Wnn

> Period: YYYY-MM-DD to YYYY-MM-DD

## Stats

| Metric | Start | End | Delta |
|--------|-------|-----|-------|
| Tweets | N | N | +N |
| Vault notes | N | N | +N |
| Threads | N | N | +N |
| Links resolved | N | N | +N |

## Top Tips This Week

[Top 5-10 tips by engagement. For each: author, likes, one-line summary.
Note which relate to techniques we're tracking.]

## Commits This Week

[Group by category: features, fixes, data operations, docs]

## Technique Adoption Progress

[Cross-reference PROGRESS.md:
- What moved from PENDING to IN_PROGRESS or ADOPTED?
- What was tried and abandoned?
- What's been stalled?]

## Recommendations for Next Week

[Based on patterns observed:
- High-signal tips worth experimenting with
- Stalled techniques to revisit or drop
- Pipeline improvements suggested by the week's work]
```

## After Writing

Do NOT commit automatically. The user reviews and commits analysis files.
