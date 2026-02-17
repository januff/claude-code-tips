---
name: fetch-bookmarks
description: >
  Fetch new bookmarks from Twitter/X using Claude-in-Chrome browser integration.
  Requires `/chrome` connection. Use when the user wants to import new bookmarks
  from their Twitter Claude folder into the SQLite database.
argument-hint: twitter
disable-model-invocation: true
---

# Fetch Bookmarks — Deterministic Skill

> **Design principle:** Every phase prescribes exact tool calls. No step should
> require improvisation. If you find yourself piping shell commands or writing
> inline dedup logic, STOP — the import script handles dedup.

## Prerequisites

- Chrome connected: run `/chrome` and verify connection
- Chrome logged into x.com
- Bookmark folder URL: `https://x.com/i/bookmarks/2004623846088040770`

> **Chrome contention:** If Claude.ai app is open, run `/chrome` → Reconnect
> to claim the browser connection. Only one instance can hold it at a time.

---

## Phase 1: Verify Chrome Connection

**Tool:** `mcp__claude-in-chrome__tabs_context_mcp`

Confirm you can see browser tabs. If not, ask the user to run `/chrome` → Reconnect.

---

## Phase 2: Navigate to Bookmarks Folder

**Tool:** `mcp__claude-in-chrome__navigate`
```
url: https://x.com/i/bookmarks/2004623846088040770
```

Then wait 3 seconds:

**Tool:** `mcp__claude-in-chrome__computer`
```
action: wait
duration: 3
```

---

## Phase 3: Capture Live API Parameters (Self-Healing Hash)

**Tool:** `mcp__claude-in-chrome__read_network_requests`
```
urlPattern: BookmarkFolderTimeline
```

From the captured request URL:
1. Parse the hash from the URL path: `/graphql/{HASH}/BookmarkFolderTimeline`
2. Parse the features from the `features=` query parameter (URL-decode, then parse JSON)

Store both values. You will pass them to the extractor in Phase 4.

If no requests are captured (page was already loaded), reload the page and wait again.

---

## Phase 4: Inject Extractor and Run

### Step 4a: Read the extractor script

**Tool:** `Read`
```
file_path: scripts/bookmark_folder_extractor.js
```

### Step 4b: Inject the entire script into page context

**Tool:** `mcp__claude-in-chrome__javascript_tool`

Inject the **entire contents** of `scripts/bookmark_folder_extractor.js` as a single `javascript_tool` call. Do NOT use data URIs, script tags, or chunking — paste the full script text directly.

### Step 4c: Execute the extractor

**Tool:** `mcp__claude-in-chrome__javascript_tool`
```javascript
await fetchBookmarkFolder("2004623846088040770", {
  hash: "CAPTURED_HASH_FROM_PHASE_3",
  features: CAPTURED_FEATURES_FROM_PHASE_3
})
```

The extractor paginates all pages automatically (~20 tweets/page, 1.5s delay between pages). It stores results in `window._fetchedBookmarks`.

Wait for it to complete. It returns the total count.

---

## Phase 5: Extract Results from Browser

Results are in `window._fetchedBookmarks`. Extract in batches of **2 tweets per call** due to `javascript_tool` output size limits.

### Step 5a: Get total count

**Tool:** `mcp__claude-in-chrome__javascript_tool`
```javascript
window._fetchedBookmarks.length
```

### Step 5b: Extract in batches

Loop from `START=0` to total, incrementing by 2:

**Tool:** `mcp__claude-in-chrome__javascript_tool`
```javascript
JSON.stringify(window._fetchedBookmarks.slice(START, START+2))
```

Collect all batches into a single JSON array in your context.

---

## Phase 6: Save JSON File

**Tool:** `Write`

Write the collected array to:
```
data/new_bookmarks_YYYY-MM-DD.json
```

Use today's date. Format as a JSON array with 2-space indent.

---

## Phase 7: Import to Database

> **CRITICAL: No browser-side dedup. No shell pipes. The Python script handles everything.**

### Step 7a: Dry run first

**Tool:** `Bash`
```bash
python3 scripts/import_bookmarks.py data/new_bookmarks_YYYY-MM-DD.json --dry-run
```

Review the output. Confirm the new/existing counts look reasonable.
Report the dry-run results to the user before proceeding.

### Step 7b: Actual import

**Tool:** `Bash`
```bash
python3 scripts/import_bookmarks.py data/new_bookmarks_YYYY-MM-DD.json
```

Parse the `IMPORT_RESULT:{...}` line from the output to get the structured result.

---

## Phase 8: Enrichment Pipeline

Run these scripts **in order**. Each depends on the previous step's output.

### Step 8a: Keyword extraction
```bash
python3 scripts/enrich_keywords.py
```

### Step 8b: Summary generation
```bash
python3 scripts/enrich_summaries.py
```

### Step 8c: Link enrichment
```bash
python3 scripts/enrich_links.py
```

### Step 8d: Obsidian vault export
```bash
python3 scripts/export_tips.py
```

---

## Phase 9: Report and Wrap Up

1. Report to the user:
   - Total tweets fetched
   - New vs existing breakdown
   - Enrichment results (keywords, summaries, links)
   - Any errors

2. The fetch log is already written by `import_bookmarks.py` to `data/fetch_logs/`. Verify it exists.

3. Run `/wrap-up` to update STATUS.json and commit.

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| HTTP 400 from extractor | Stale GraphQL hash | Reload bookmarks page, re-capture from network requests (Phase 3) |
| "Extension not connected" | Another instance holds Chrome | Run `/chrome` → Reconnect |
| Empty results | No bookmarks in folder or wrong folder ID | Check folder in browser |
| `import_bookmarks.py` reports 0 new | All tweets already in DB | Normal if re-running same day |
| Import validation error | Malformed JSON from extraction | Check batch extraction output for truncation |

## Reference

For API endpoint details, auth patterns, and the full features object, see:
**`.claude/references/twitter-api-reference.md`**
