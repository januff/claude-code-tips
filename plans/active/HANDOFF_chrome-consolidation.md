# HANDOFF: Chrome Protocol Consolidation + Fetch Rewrite

> **From:** Claude.ai Planning Instance
> **To:** Claude Code
> **Priority:** High — the bookmark fetch pipeline is currently broken
> **Estimated effort:** 2-3 hours
> **Dependencies:** Chrome extension connection (run `/chrome` → Reconnect before starting)

---

## Context

The Feb 11 evening session debugged the entire fetch pipeline and produced a detailed session report at `plans/active/SESSION_2026-02-11_fetch-and-analysis.md`. That report documents what worked, what broke, and why. This handoff turns those findings into actionable fixes.

Three problems were identified:
1. **Browser tool ambiguity** — 3 tools referenced, conflicting docs, only Claude-in-Chrome works
2. **Stale GraphQL hash** — hardcoded hash returns HTTP 400 when Twitter deploys
3. **Randomized bookmark ordering** — breaks the incremental fetch stop-at-known-ID strategy

This handoff fixes all three and runs the full pipeline end-to-end.

---

## Pre-Flight: Chrome Connection

**CRITICAL:** Only one Claude instance can hold the Chrome extension connection at a time. If the Claude.ai app is open with Chrome MCP tools, this Claude Code instance is locked out.

Before starting browser work:
1. Run `/chrome` in this terminal
2. If status shows "Extension: Installed" but tools don't respond, select "Reconnect extension"
3. Verify with `mcp__claude-in-chrome__tabs_context_mcp` — you should see browser tabs

If the user says "releasing Chrome" or "Chrome is yours," proceed. Otherwise ask.

---

## Task 1: Remove Playwriter from settings.json (5 minutes)

Remove the Playwriter MCP server config from `.claude/settings.json`. It's dead config that:
- Adds ~8.4k tokens to MCP tool definitions (context cost on every session)
- Creates confusion with three browser tools documented
- Has never successfully been used for bookmark fetching

**Remove this block:**
```json
"mcpServers": {
    "playwriter": {
      "command": "npx",
      "args": ["playwriter@latest"]
    }
  },
```

Keep the rest of settings.json (permissions, hooks) unchanged.

Commit: `chore: remove Playwriter MCP — consolidate on Claude-in-Chrome`

---

## Task 2: Rewrite bookmark_folder_extractor.js (1 hour)

The current `scripts/bookmark_folder_extractor.js` is designed for manual DevTools usage (copy cURL, paste into console). It needs to be rewritten for the Claude-in-Chrome execution flow.

### Two modes needed:

**Mode A: Self-healing fetch (primary — used by Claude-in-Chrome)**

When executed via `mcp__claude-in-chrome__javascript_tool` in the context of x.com:

1. Grab CSRF token from `document.cookie`
2. Use the standard public bearer token (hardcoded, rarely changes)
3. **Self-heal the GraphQL hash:** Make a test request with the current hash. If it returns 400, intercept the page's own `BookmarkFolderTimeline` request from the network to capture the working hash and features. Alternatively, accept the hash and features as parameters so Claude Code can capture them from `mcp__claude-in-chrome__read_network_requests` before calling the extractor.
4. Paginate ALL pages (full-scan, NOT stop-at-known-ID)
5. Return all tweets as a JSON array

**Mode B: Manual fallback (secondary — DevTools console)**

Keep the existing cURL-based auth flow as a fallback for when Chrome extension isn't available. But update the GraphQL hash and features to the current working values from the session report (Section 2).

### Pagination change: Full-scan-and-dedup

Replace the incremental strategy:
```javascript
// OLD: Stop at first known tweet ID (assumes chronological order)
if (knownIds.has(parsed.id)) {
    console.log('Hit known tweet, stopping');
    break;
}
```

With full-scan:
```javascript
// NEW: Fetch all pages, deduplicate later
// The bookmark folder ordering is randomized (not chronological)
// so we must scan everything and let the caller deduplicate against the DB
```

The function should paginate until it hits a page with no `cursor-bottom` entry (end of folder), collect everything, and return the full set. Deduplication against the DB happens in the import step, not during fetch.

### Accept hash/features as parameters

The function signature should accept optional hash and features overrides:

```javascript
async function fetchBookmarkFolder(folderId, options = {}) {
  const hash = options.hash || DEFAULT_HASH;
  const features = options.features || DEFAULT_FEATURES;
  // ...
}
```

This lets Claude Code capture the live hash from network requests and pass it in, without modifying the script.

### Current working values (from session report)

- **Hash:** `LdT6YZk9yx_o1xbLN61epw`
- **Features:** See the full object in `plans/active/SESSION_2026-02-11_fetch-and-analysis.md` Section 2

Update `DEFAULT_HASH` and `DEFAULT_FEATURES` in the script with these values.

Commit: `feat: rewrite bookmark_folder_extractor.js — self-healing hash, full-scan pagination`

---

## Task 3: Update /fetch-bookmarks command (30 minutes)

Rewrite `.claude/commands/fetch-bookmarks.md` to document the Claude-in-Chrome procedure that actually works. The current command describes a theoretical workflow; this should describe the tested, working one from session report Section 5.

### New workflow to document:

1. **Verify Chrome connection:** `mcp__claude-in-chrome__tabs_context_mcp` — confirm you can see tabs
2. **Navigate to bookmarks:** `mcp__claude-in-chrome__navigate` to `https://x.com/i/bookmarks/2004623846088040770`
3. **Wait for page load:** 3 seconds
4. **Capture current API params:** Use `mcp__claude-in-chrome__read_network_requests` with filter `BookmarkFolderTimeline` to get the live hash and features from Twitter's own request
5. **Execute extractor:** Use `mcp__claude-in-chrome__javascript_tool` to run `bookmark_folder_extractor.js` in page context, passing the captured hash/features
6. **Extract results:** Read `window.bookmarks` (may need to extract in batches due to output size limits)
7. **Save to file:** Write to `data/new_bookmarks_YYYY-MM-DD.json`
8. **Import to DB:** Run the import script
9. **Report:** Count new vs known tweets

### Prerequisite to document:

```
> **Chrome contention:** If Claude.ai app is open, run `/chrome` → Reconnect 
> to claim the browser connection. Only one instance can hold it at a time.
```

### Remove:
- All Playwriter/Playwright references
- The "stop at first known tweet ID" incremental fetch description
- References to manual cURL copy-paste as the primary method

Commit: `docs: rewrite /fetch-bookmarks for Claude-in-Chrome + full-scan`

---

## Task 4: Update CLAUDE.md (15 minutes)

Find and replace any Playwriter references in `CLAUDE.md`:

- Remove: "Use Playwriter (remorses/playwriter) — NOT standard Playwright MCP"
- Add: "Browser automation uses Claude-in-Chrome (native `/chrome` integration). No third-party browser extensions needed."
- Add a note about Chrome contention: "Only one Claude instance can hold the Chrome extension connection at a time. Claude Code should hold it during execution sessions."

Commit: `docs: update CLAUDE.md — Claude-in-Chrome only, remove Playwriter`

---

## Task 5: Run enrichment on new tweets (30 minutes)

8 tweets from last night's fetch need enrichment:

```bash
python scripts/enrich_keywords.py
python scripts/enrich_summaries.py
python scripts/enrich_links.py
```

These are idempotent — they skip already-enriched items. Verify the 8 new tweets get keywords and summaries.

Commit: `chore: enrich 8 new tweets (keywords, summaries, links)`

---

## Task 6: Full end-to-end pipeline test (30 minutes)

This is the real test. Run the complete daily monitor:

```bash
python scripts/daily_monitor.py
```

This should:
1. **Fetch:** Attempt Chrome-based fetch (should succeed if Chrome is connected and you're on the bookmarks page)
2. **Enrich:** Run enrichment (should skip already-enriched items)
3. **Analyze:** Run LLM classification via Gemini on recent tweets
4. **Brief:** Generate morning briefing
5. **Update:** Write STATUS.json

### Success criteria:
- Fetch finds new tweets OR correctly reports "no new tweets" (not a silent failure)
- Analysis produces a reasonable distribution (not 34/36 ACT_NOW)
- Briefing is written to `analysis/daily/`
- STATUS.json reflects the run

### If fetch fails:
Check the GraphQL hash first. If it's returning 400, the hash has changed again since last night. Use the self-healing approach: capture the live request from network tab, extract the new hash, and update the script.

---

## Task 7: Update twitter-api-reference.md (15 minutes)

Update `.claude/references/twitter-api-reference.md` with:
- The self-healing hash capture approach
- The current working hash and features
- A note that bookmark folder ordering is randomized
- The full-scan-and-dedup pagination strategy

This reference doc is what the `/fetch-bookmarks` command points to for details.

Commit: `docs: update twitter-api-reference — self-healing hash, randomized ordering`

---

## Task 8: Wrap up

Run `/wrap-up` to update STATUS.json with:
- All commits from this session
- Cleared known issues (Playwriter, stale hash, randomized ordering)
- Updated key_dates

---

## Verification Checklist

Before wrapping up, verify:

- [ ] `.claude/settings.json` has no Playwriter config
- [ ] `CLAUDE.md` has no Playwriter references
- [ ] `bookmark_folder_extractor.js` uses self-healing hash + full-scan pagination
- [ ] `/fetch-bookmarks` command documents Claude-in-Chrome workflow
- [ ] `twitter-api-reference.md` documents randomized ordering and self-healing
- [ ] 8 new tweets are enriched (keywords + summaries)
- [ ] `daily_monitor.py` has been run end-to-end at least once
- [ ] STATUS.json is current

---

## Notes

- **App permissions:** The Claude.ai app now has auto-accept enabled for its code tab. This doesn't affect Claude Code in the terminal, but it's worth noting as a potential future execution path for pipeline scripts.
- **Chrome contention convention:** When the user says "releasing Chrome" or "Chrome is yours," that means the app instance has yielded the browser connection. Run `/chrome` → Reconnect to claim it.

---

*Source: Claude.ai planning instance, morning review 2026-02-12. Based on findings from SESSION_2026-02-11_fetch-and-analysis.md.*
