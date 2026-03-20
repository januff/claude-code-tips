---
name: fetch-bookmarks
description: >
  Fetch new bookmarks from Twitter/X using browser integration (Chrome DevTools
  MCP preferred, Claude-in-Chrome fallback). Use when the user wants to import
  new bookmarks from their Twitter Claude folder into the SQLite database.
argument-hint: twitter
disable-model-invocation: true
---

# Fetch Bookmarks — Deterministic Skill

> **Design principle:** Every phase prescribes exact tool calls. No step should
> require improvisation. If you find yourself piping shell commands or writing
> inline dedup logic, STOP — the import script handles dedup.

## Prerequisites

- Chrome 146+ with remote debugging enabled (`chrome://inspect/#remote-debugging`)
- Chrome logged into x.com
- Bookmark folder URL: `https://x.com/i/bookmarks/2004623846088040770`

## Browser Integration: Choose Your Backend

This skill supports two browser MCP backends. **Try Chrome DevTools MCP first.**

| Task | Chrome DevTools MCP (preferred) | Claude-in-Chrome (fallback) |
|------|--------------------------------|----------------------------|
| Connect/verify | `list_pages` | `mcp__claude-in-chrome__tabs_context_mcp` |
| Navigate | `navigate_page` | `mcp__claude-in-chrome__navigate` |
| Run JS | `evaluate_script` | `mcp__claude-in-chrome__javascript_tool` |
| Network | `list_network_requests` | `mcp__claude-in-chrome__read_network_requests` |
| Screenshot | `take_screenshot` | `mcp__claude-in-chrome__computer` (screenshot) |
| Wait | `sleep 3` (bash) | `mcp__claude-in-chrome__computer` (wait) |

**When to fall back:** If Chrome DevTools MCP is not available (not installed, Chrome
<146, remote debugging not enabled), use Claude-in-Chrome tools instead. The phases
below show both tool names where they differ.

---

## Phase 1: Verify Chrome Connection

**DevTools MCP:** `list_pages` — confirm you can see browser tabs.
**Claude-in-Chrome:** `mcp__claude-in-chrome__tabs_context_mcp`

If neither works, ask the user to check their Chrome setup.

---

## Phase 2: Navigate to Bookmarks Folder

**DevTools MCP:** `navigate_page`
**Claude-in-Chrome:** `mcp__claude-in-chrome__navigate`
```
url: https://x.com/i/bookmarks/2004623846088040770
```

Then wait 3 seconds for page load (bash `sleep 3` or Chrome wait tool).

---

## Phase 3: Capture Live API Parameters (Self-Healing Hash)

**DevTools MCP:** `list_network_requests`
**Claude-in-Chrome:** `mcp__claude-in-chrome__read_network_requests`

Filter for `BookmarkFolderTimeline`. From the captured request URL:
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

**DevTools MCP:** `evaluate_script`
**Claude-in-Chrome:** `mcp__claude-in-chrome__javascript_tool`

Inject the **entire contents** of `scripts/bookmark_folder_extractor.js` as a single
call. Do NOT use data URIs, script tags, or chunking — paste the full script text directly.

### Step 4c: Execute the extractor

**JS eval tool** (same as 4b):
```javascript
await fetchBookmarkFolder("2004623846088040770", {
  hash: "CAPTURED_HASH_FROM_PHASE_3",
  features: CAPTURED_FEATURES_FROM_PHASE_3
})
```

The extractor paginates all pages automatically (~20 tweets/page, 1.5s delay between pages). It stores results in `window._fetchedBookmarks`.

Wait for it to complete. It returns the total count.

---

## Phase 5: Extract Results via Browser Download

Results are in `window._fetchedBookmarks`.

> **WORKAROUND (Feb 2026):** The Claude-in-Chrome `javascript_tool` output truncates
> at ~1500 chars. Chrome DevTools MCP's `evaluate_script` may have a higher limit —
> test with `JSON.stringify(window._fetchedBookmarks).length` first. If the full
> result can be returned directly, skip the blob download workaround.
>
> If the output is too large for direct return, use the blob download approach below.

### Step 5a: Verify count

**JS eval tool:**
```javascript
window._fetchedBookmarks.length
```

### Step 5b: Try direct extraction (DevTools MCP only)

**DevTools MCP:** Try `evaluate_script` with:
```javascript
JSON.stringify(window._fetchedBookmarks)
```

If the full JSON is returned, write it directly to `data/new_bookmarks_YYYY-MM-DD.json`
and skip to Step 5d.

### Step 5c: Blob download fallback (Claude-in-Chrome, or if 5b truncated)

**JS eval tool:**
```javascript
const blob = new Blob([JSON.stringify(window._fetchedBookmarks, null, 2)], {type: 'application/json'});
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'new_bookmarks_YYYY-MM-DD.json';
document.body.appendChild(a);
a.click();
document.body.removeChild(a);
URL.revokeObjectURL(url);
'Download triggered'
```

Replace `YYYY-MM-DD` with today's date.

Wait 2 seconds, then copy:
```bash
cp ~/Downloads/new_bookmarks_YYYY-MM-DD.json data/new_bookmarks_YYYY-MM-DD.json
```

### Step 5d: Validate the file

```bash
python3 -c "import json; d=json.load(open('data/new_bookmarks_YYYY-MM-DD.json')); print(f'{len(d)} tweets')"
```

Confirm the count matches Step 5a.

---

## Phase 6: Import to Database

> **CRITICAL: No browser-side dedup. No shell pipes. The Python script handles everything.**

### Step 6a: Dry run first

**Tool:** `Bash`
```bash
python3 scripts/import_bookmarks.py data/new_bookmarks_YYYY-MM-DD.json --dry-run
```

Review the output. Confirm the new/existing counts look reasonable.
Report the dry-run results to the user before proceeding.

### Step 6b: Actual import

**Tool:** `Bash`
```bash
python3 scripts/import_bookmarks.py data/new_bookmarks_YYYY-MM-DD.json
```

Parse the `IMPORT_RESULT:{...}` line from the output to get the structured result.

---

## Phase 7: Enrichment Pipeline

Run these scripts **in order**. Each depends on the previous step's output.

### Step 7a: Keyword extraction
```bash
python3 scripts/enrich_keywords.py
```

### Step 7b: Summary generation
```bash
python3 scripts/enrich_summaries.py
```

### Step 7c: Link enrichment
```bash
python3 scripts/enrich_links.py
```

### Step 7d: Media download
```bash
python3 scripts/download_media.py
```

### Step 7e: Media analysis (Gemini Vision)
```bash
python3 scripts/enrich_media.py
```

### Step 7f: Re-generate summaries (now with media context)

The summary script only processes tweets with `holistic_summary IS NULL`.
Tweets with media that was never downloaded will already have NULL summaries
(they were skipped or generated with "Media present but not analyzed").

If `enrich_media.py` analyzed new media, check whether those tweets already
have summaries. If so, clear them first:

```sql
UPDATE tips SET holistic_summary = NULL
WHERE tweet_id IN (SELECT DISTINCT tweet_id FROM media WHERE downloaded_at > 'YYYY-MM-DD');
```

Then re-run:

```bash
python3 scripts/enrich_summaries.py
```

### Step 7g: Obsidian vault export
```bash
python3 scripts/export_tips.py
```

---

## Phase 8: Report and Wrap Up

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
| "Extension not connected" | Another instance holds Chrome | Run `/chrome` → Reconnect, or switch to DevTools MCP |
| DevTools MCP "no pages found" | Remote debugging not enabled | Go to `chrome://inspect/#remote-debugging` and enable the toggle |
| DevTools MCP permission denied | Chrome blocked the connection | Approve the permission dialog in Chrome; check for "controlled by automation" banner |
| Empty results | No bookmarks in folder or wrong folder ID | Check folder in browser |
| `import_bookmarks.py` reports 0 new | All tweets already in DB | Normal if re-running same day |
| Import validation error | Malformed JSON from extraction | Check extraction output for truncation |
| Download not appearing in ~/Downloads | Browser download blocked | Check Chrome download settings; try screenshot to confirm dialog |
| `evaluate_script` returns full JSON | DevTools MCP has higher output limit | Great — skip blob download, write JSON directly to file |

## Reference

For API endpoint details, auth patterns, and the full features object, see:
**`.claude/references/twitter-api-reference.md`**

For browser integration details, see:
**`FETCH_PROMPT.md`** (root of repo) — tool mapping table, connection policy, pipeline reference
