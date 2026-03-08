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

## Phase 5: Extract Results via Browser Download

Results are in `window._fetchedBookmarks`.

> **WORKAROUND (Feb 2026):** The `javascript_tool` output truncates at ~1500 chars,
> which is smaller than a single tweet (~800 chars). Batch extraction (the old
> approach) would require 67+ sequential calls for a typical folder. Instead, we
> trigger a Blob download from the browser and copy the file over.
>
> **If a future Claude-in-Chrome update lifts the output limit or adds a direct
> file-write capability, replace this phase with direct extraction.** Check the
> `javascript_tool` changelog or test with `JSON.stringify(array).length` to see
> if the limit has changed.

### Step 5a: Verify count

**Tool:** `mcp__claude-in-chrome__javascript_tool`
```javascript
window._fetchedBookmarks.length
```

### Step 5b: Trigger browser download

**Tool:** `mcp__claude-in-chrome__javascript_tool`
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

### Step 5c: Wait, then copy to project

**Tool:** `mcp__claude-in-chrome__computer`
```
action: wait
duration: 2
```

**Tool:** `Bash`
```bash
cp ~/Downloads/new_bookmarks_YYYY-MM-DD.json data/new_bookmarks_YYYY-MM-DD.json
```

### Step 5d: Validate the file

**Tool:** `Bash`
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
| "Extension not connected" | Another instance holds Chrome | Run `/chrome` → Reconnect |
| Empty results | No bookmarks in folder or wrong folder ID | Check folder in browser |
| `import_bookmarks.py` reports 0 new | All tweets already in DB | Normal if re-running same day |
| Import validation error | Malformed JSON from extraction | Check batch extraction output for truncation |
| Download not appearing in ~/Downloads | Browser download blocked or different path | Check Chrome download settings; try screenshot to confirm dialog |
| `javascript_tool` output limit increased | Claude-in-Chrome update | Test with `JSON.stringify(array).length`; if >100k works, switch back to direct extraction |

## Reference

For API endpoint details, auth patterns, and the full features object, see:
**`.claude/references/twitter-api-reference.md`**
