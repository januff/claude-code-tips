# Scripts

Browser-based scripts for extracting Twitter/X thread data.

## Current Status: BLOCKED

See `plans/data-ingestion-handoff.md` for full context on the data ingestion problem.

---

## Files

### `twitter_thread_extractor.js`

**Purpose:** Extract all replies from a Twitter/X thread.

**Status:** Partially working
- DOM extraction works but only captures ~20 items (Twitter's virtualized list)
- API extraction blocked (Twitter returns empty `tweet_results`)

**Usage:** Paste into browser console while on the thread page.

---

### `reference/`

Reference scripts from a different project (Sora video platform) that demonstrate working patterns for API-based data extraction with pagination. These work for Sora but the same approach fails for Twitter due to anti-bot measures.

- `browser_fetch_comments.js` — Paginated comment fetching with cursor handling
- `browser_fetch_new_likes.js` — Incremental likes fetching with deduplication

These are preserved as pattern references for potential future solutions.

---

## Needed

A reliable method to extract all ~360 replies from the thread at:
`https://x.com/alexalbert__/status/1873754311106740359`

See handoff document for attempted approaches and potential solutions.
