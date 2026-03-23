# Senior Instance Review Notes

> Created: 2026-03-22
> Context: The terminal instance completed Phases 1-3 of the public launch task plan. This desktop instance ("senior/CTO") reviewed the output and made amendments. These notes document what was changed and why, so the terminal instance can stay aligned.

---

## What You Did Well

- **Disciplined execution.** Stuck to data queries, structural audit, and factual writing. Didn't overwrite creative direction.
- **COMMUNITY_MAP.md is excellent.** The Tips-to-Tool Pipeline section is original research that doesn't exist anywhere else. The three-tier community voice breakdown is clean.
- **README automation honesty.** "We fetch when we remember to, roughly twice a week" — exactly the right tone.
- **Sensitive content scan caught a real issue.** Email in `analysis/chrome-extension-bug-report.md`.

## What Was Changed After Review

### README.md

1. **Removed Origin Story.** The Ed/Christmas present paragraph was charming but too autobiographical. The README should be outward-facing. Joey's preference.

2. **Added "Why This Exists" section.** The README was missing the meta-narrative — *why* tracking tips matters, what this project is really about. New section frames the repo as existing in the gap between AI marketing and reality, and as a live experiment in memory/continual learning/honest documentation.

3. **Added four Project Principles.** These emerged from the conversation with Joey and weren't available to you:
   - Watch, then adopt (don't implement every trending technique immediately)
   - Freshness is the central data point (timestamps matter more than coverage)
   - Review conferences and decision conferences (periodic stepping back)
   - Don't reinvent the wheel (search our own database before building)

4. **Added "The Week in Claude" as formal aspiration.** Described as a periodic bulletin — not yet built but framed as coming soon.

5. **Corrected team stats (handle dedup).** You flagged the `bcherny` vs `@bcherny` issue but used the uncorrected numbers. Fixed:
   - Thariq: 10→12 tweets, 65,283→66,565 likes
   - Felix: 2→3 tweets, 17,660→17,908 likes
   - Anthony: 1→2 tweets, 4,395→4,926 likes

6. **Split Quick Stats into bookmarked tips (206) vs thread replies (356).** All 288 zero-like tweets are from `thread_extraction`. Every bookmarked tweet has ≥1 like. This distinction is important — thread replies are unreviewed context, not curated signal.

### COMMUNITY_MAP.md

7. **Updated stats to match deduped numbers.** Same corrections as README.

8. **Added dedup note.** Documented that 15 authors have variant handles in the database, stats are manually deduped, schema-level fix pending.

### Other

9. **Redacted email** in `analysis/chrome-extension-bug-report.md`.

10. **`multi-rewrite.md` not yet added to .gitignore** — still pending from your Phase 5 items.

## Principles for Future Work

When working on this repo, keep these in mind:

- **Always deduplicate handles** using `LOWER(REPLACE(handle, '@', ''))` in any SQL query that aggregates by author.
- **Distinguish bookmarks from thread replies** in any stats or analysis. Source `thread_extraction` and `reply_extraction` are scraped context; all other sources are curated bookmarks.
- **Don't add the Tinkertoys photo back.** README is outward-facing.
- **The four principles in the README are settled.** Don't re-derive or re-litigate them.
- **Joey prefers honest imperfection over polished fiction.** If something doesn't work yet, say so. The automation status table is the model for this.

## Next Task

See `plans/active/VISUALIZATIONS_TASK.md` — generate data visualizations for the README and COMMUNITY_MAP. Multiple chart types, multiple rendering approaches. Save everything to `assets/visualizations/` for review.
