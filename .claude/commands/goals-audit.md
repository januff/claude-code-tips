---
name: goals-audit
description: >
  Audit technique adoption goals against actual progress. Cross-references LEARNINGS.md
  (what we planned to try), plans/PROGRESS.md (what we adopted), and recent summaries
  (what we've been doing). Flags gaps and surfaces opportunities from high-signal tips.
  Use on-demand when you want an honest look at adoption drift.
disable-model-invocation: true
---

# Goals Audit

Compare stated goals against actual progress.

## Data Sources

Read these three files:
1. **`LEARNINGS.md`** — "Techniques to Try Next" and "Watching" sections
2. **`plans/PROGRESS.md`** — actual adoption status per technique
3. **Recent summaries** — scan `analysis/weekly/` (latest) and `analysis/daily/` (last 7 days)

Also query the database for high-signal recent tips:
```sql
SELECT text, likes, author_username, primary_keyword
FROM tweets
WHERE likes >= 100
ORDER BY created_at DESC
LIMIT 20;
```

## Analysis

### 1. Gap Detection

For each item in LEARNINGS.md "Techniques to Try Next" and PROGRESS.md with status PENDING:
- Check if any daily/weekly summary mentions it
- Check the last date it was referenced in git log:
  ```bash
  git log --all --oneline --grep="<technique keyword>" | head -3
  ```
- Flag items untouched for 3+ weeks as **stalled**

### 2. Opportunity Matching

For each high-engagement tip (100+ likes) from the DB:
- Does it relate to a PENDING or IN_PROGRESS technique in PROGRESS.md?
- Does it suggest a technique not yet on our radar?
- Flag matches as **opportunities**

### 3. Adoption Drift

Compare "Techniques We Use Daily" in LEARNINGS.md against actual recent activity:
- Are we still using what we claimed to use?
- Did something get adopted that isn't documented yet?

## Output

Print the audit directly to the conversation (do NOT write to a file unless the user asks).

Format:

```
GOALS AUDIT — YYYY-MM-DD

STALLED (planned but untouched 3+ weeks):
  - [technique]: Last referenced [date]. Status: [PENDING/IN_PROGRESS].
    Action: [drop it / revisit / blocked by X]

OPPORTUNITIES (high-signal tips matching our goals):
  - [tip summary] ([likes] likes, @[author])
    Relates to: [PROGRESS.md item]
    Action: [experiment / add to queue / watch]

UNDOCUMENTED ADOPTIONS (doing it but not tracked):
  - [technique]: Evidence in [file/commit]. Add to PROGRESS.md.

DRIFT (claimed daily use but no recent evidence):
  - [technique]: Last evidence [date]. Still using?
```

## After Audit

Ask the user if they want to update PROGRESS.md or LEARNINGS.md based on findings.
