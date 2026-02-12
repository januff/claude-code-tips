---
name: fetch-bookmarks
description: >
  Fetch new bookmarks from Twitter/X using Claude-in-Chrome browser integration.
  Requires `/chrome` connection. Use when the user wants to import new bookmarks
  from their Twitter Claude folder into the SQLite database.
argument-hint: twitter
disable-model-invocation: true
---

# Fetch Bookmarks

## Prerequisites

- Claude Code must have Chrome connected: run `/chrome` and verify connection
- Chrome must be open and logged into x.com
- The user's bookmark folder URL: `https://x.com/i/bookmarks/2004623846088040770`

> **Chrome contention:** If Claude.ai app is open, run `/chrome` → Reconnect
> to claim the browser connection. Only one instance can hold it at a time.

## Workflow

### 1. Verify Chrome connection

```
mcp__claude-in-chrome__tabs_context_mcp
```

Confirm you can see browser tabs. If not, ask the user to run `/chrome` → Reconnect.

### 2. Navigate to bookmarks folder

```
mcp__claude-in-chrome__navigate → https://x.com/i/bookmarks/2004623846088040770
```

Wait 3 seconds for page load.

### 3. Capture current API params (self-healing hash)

```
mcp__claude-in-chrome__read_network_requests (filter: BookmarkFolderTimeline)
```

Extract the GraphQL hash and features from the live request URL. The hash changes on every Twitter deploy — capturing it live avoids stale-hash 400 errors.

Parse the hash from the URL path: `/graphql/{HASH}/BookmarkFolderTimeline`
Parse features from the `features=` query parameter.

### 4. Execute extractor in page context

```
mcp__claude-in-chrome__javascript_tool
```

Load `scripts/bookmark_folder_extractor.js` and call:

```javascript
await fetchBookmarkFolder("2004623846088040770", {
  hash: "CAPTURED_HASH",
  features: CAPTURED_FEATURES
})
```

The extractor uses full-scan pagination (fetches ALL pages). Bookmark folder ordering is randomized, not chronological — there is no stop-at-known-ID shortcut.

### 5. Extract results

Results are stored in `window._fetchedBookmarks`. Extract in batches due to `javascript_tool` output size limits (~1000 chars).

### 6. Save and import

- Write to `data/new_bookmarks_YYYY-MM-DD.json`
- Import to SQLite: deduplicate against existing tweet IDs
- Report: count of new vs already-known tweets

## Post-Fetch Processing

After fetching, run the enrichment pipeline:

1. `python scripts/enrich_keywords.py` — Gemini keyword extraction
2. `python scripts/enrich_summaries.py` — Gemini summary generation
3. `python scripts/enrich_links.py` — resolve, fetch, and summarize linked content
4. Run thread scraping for high-reply tweets (optional)
5. `python scripts/export_tips.py` — update Obsidian vault
6. Run `/wrap-up` to update STATUS.json

## Troubleshooting

- **HTTP 400:** Hash is stale. Reload the bookmarks page and re-capture from network requests (step 3).
- **"Extension not connected":** Another Claude instance holds the connection. Run `/chrome` → Reconnect.
- **Empty results:** Check that the folder has bookmarks in the browser. The folder ID may have changed.

## Reference

For API endpoint details, auth patterns, and the full features object, see:
**`.claude/references/twitter-api-reference.md`**
