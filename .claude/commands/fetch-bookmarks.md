---
name: fetch-bookmarks
description: >
  Fetch new bookmarks from Twitter/X using Chrome browser integration. Requires
  `claude --chrome` flag. Use when the user wants to import new bookmarks from their
  Twitter Claude folder into the SQLite database.
argument-hint: twitter
disable-model-invocation: true
---

# Fetch Bookmarks

## Prerequisites

Claude Code must be started with `--chrome`. Chrome must be open and logged into x.com.

> **Note:** Uses native `claude --chrome` integration — NOT Playwriter or Playwright MCP.

## Workflow

1. **Auth capture:** Navigate to x.com bookmarks, capture Bearer + CSRF tokens via network interception
2. **Incremental fetch:** Paginate GraphQL API, stop at first known tweet ID
3. **Save:** Write results to `data/new_bookmarks_YYYY-MM-DD.json`
4. **Report:** Count of new items found

For API endpoint details, auth caching, and fallback procedures, see:
**`.claude/references/twitter-api-reference.md`**

## Post-Fetch Processing

After fetching, run the enrichment pipeline:

1. Import to SQLite database
2. Enrich keywords (Gemini)
3. Run thread scraping for high-reply tweets
4. Enrich links (resolve, fetch, summarize)
5. Update vault export (`python scripts/export_tips.py`)
6. Run `/wrap-up` to update STATUS.json

## Notes

- Auth: Copy pattern from `scripts/bookmark_folder_extractor.js`
- Rate limit: 2-3 second delays between requests
- Commit after each batch of imports
- Cross-repo: Same Chrome auth wrapper pattern used by hall-of-fake
