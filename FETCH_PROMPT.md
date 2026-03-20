# Fetch Bookmarks — Terminal Prompt

> **Copy-paste this into a fresh terminal Claude Code session to run a full
> bookmark fetch cycle.** Works for all three repos. Adjust the REPO and
> FOLDER_ID variables for your target.

---

## Quick Start (copy-paste)

### Claude Code Tips

```
I'm running a manual bookmark fetch for claude-code-tips.

Working directory: /Users/joeyanuff-m2/Development/claude-code-tips

Read CLAUDE.md and STATUS.json for project conventions and current state.
Then read .claude/commands/fetch-bookmarks.md and follow it exactly — all 8 phases.

Browser integration: Use Chrome DevTools MCP (chrome-devtools) if available.
Fallback: Use Claude-in-Chrome (mcp__claude-in-chrome__*) if DevTools MCP fails.

After import + enrichment + vault export, run /wrap-up, commit, and push.
Report: total fetched, new vs existing, enrichment stats, any errors.
```

### Hall of Fake

```
I'm running a manual bookmark fetch for Hall of Fake (Sora AI video archive).

Working directory: /Users/joeyanuff-m2/Development/Hall of Fake

Read CLAUDE.md and STATUS.json for project conventions and current state.
Then read .claude/commands/fetch-bookmarks.md and follow it exactly.

Browser integration: Use Chrome DevTools MCP (chrome-devtools) if available.
Fallback: Use Claude-in-Chrome (mcp__claude-in-chrome__*) if DevTools MCP fails.

After import, run the full pipeline:
- Download new video files and generate thumbnails
- Run Gemini visual analysis on new videos
- Run audio transcription
- Run clustering to update families
- Export to Obsidian vault

Run /wrap-up, commit, and push.
Report: total fetched, new vs existing, pipeline stats, any errors.
```

### Book Queue

```
I'm running a manual bookmark fetch for book-queue (reading pipeline tracker).

Working directory: /Users/joeyanuff-m2/Development/book-queue

Read CLAUDE.md, STATUS.json, and PROJECT_DECISIONS.md (especially Decision 6: tweets are primary entities, books are enrichment) for project conventions.

Browser integration: Use Chrome DevTools MCP (chrome-devtools) if available.
Fallback: Use Claude-in-Chrome (mcp__claude-in-chrome__*) if DevTools MCP fails.

PHASE A — X Bookmarks:
Read .claude/commands/fetch-bookmarks.md and follow it exactly.
Import with deterministic Python dedup (scripts/import_bookmarks.py).
Run book title extraction via Gemini (scripts/enrich_books.py).

PHASE B — Libby Reading List:
Read .claude/commands/fetch-libby.md and follow it exactly.
Navigate to libbyapp.com, extract "want to read" tag titles.
Import with deterministic dedup (scripts/import_libby.py).
Run enrichment: Thunder API metadata, sample EPUB downloads, Gutenberg full text check.

PHASE C — Cross-Reference:
Query for Libby titles that match X bookmark books (fuzzy title matching).
Note Libby-only additions and X-only discoveries.
Update source_links table for new matches.

Run /wrap-up, commit, and push.
Report: X count, Libby count, cross-reference matches, any errors.
```

---

## Browser Integration Priority

As of March 2026, there are two browser integration options:

### 1. Chrome DevTools MCP (preferred)

- **Setup**: Chrome 146+ → go to `chrome://inspect/#remote-debugging` → enable toggle
- **MCP config**: Already added as `chrome-devtools` in `~/.claude.json`
- **Connection**: Approve permission dialog in Chrome when MCP connects
- **Advantages**: No extension needed, no contention, real cookies/auth, 26 tools
- **Tools**: `navigate_page`, `evaluate_script`, `list_network_requests`, `take_screenshot`, etc.

### 2. Claude-in-Chrome (fallback)

- **Setup**: Claude-in-Chrome extension v1.0.52+ installed and signed in
- **Connection**: `mcp__claude-in-chrome__tabs_context_mcp`
- **Limitations**: Only one Claude instance can hold connection, stale locks common
- **Tools**: `javascript_tool`, `navigate`, `read_network_requests`, `computer`, etc.

### Mapping between the two

| Task | Chrome DevTools MCP | Claude-in-Chrome |
|------|-------------------|-----------------|
| Navigate | `navigate_page` | `mcp__claude-in-chrome__navigate` |
| Run JS | `evaluate_script` | `mcp__claude-in-chrome__javascript_tool` |
| Network | `list_network_requests` | `mcp__claude-in-chrome__read_network_requests` |
| Screenshot | `take_screenshot` | `mcp__claude-in-chrome__computer` (action: screenshot) |
| Tab list | `list_pages` | `mcp__claude-in-chrome__tabs_context_mcp` |
| Click | `click` | `mcp__claude-in-chrome__computer` (action: click) |

---

## Chrome Connection Policy (for unattended/scheduled use)

If running unattended (scheduled task, launchd, etc.):

1. Attempt connection **once** (DevTools MCP or Claude-in-Chrome)
2. If it fails: commit empty with `"skipped (Chrome not connected)"`, push, stop
3. **Do not**: retry, suggest restart, ask user, loop, or try alternatives

**Why:** Unattended tasks cannot fix Chrome state. Attempting to do so wastes time and creates permission prompts nobody will see.

---

## Full Pipeline Reference

```
BROWSER EXTRACTION → IMPORT → ENRICH (6 steps) → EXPORT → ANALYZE → COMMIT
```

| Phase | Browser? | Scripts |
|-------|----------|---------|
| Extract bookmarks | **YES** | `scripts/bookmark_folder_extractor.js` (injected) |
| Import to SQLite | no | `scripts/import_bookmarks.py` |
| Enrich keywords | no | `scripts/enrich_keywords.py` (Gemini) |
| Enrich summaries | no | `scripts/enrich_summaries.py` (Gemini) |
| Enrich links | no | `scripts/enrich_links.py` (Gemini + HTTP) |
| Download media | no | `scripts/download_media.py` (HTTP) |
| Analyze media | no | `scripts/enrich_media.py` (Gemini Vision) |
| Re-run summaries | no | `scripts/enrich_summaries.py` (if media was new) |
| Vault export | no | `scripts/export_tips.py` |
| Analysis | no | `scripts/analyze_new_tips.py` (Gemini) |

**Environment required:** `GOOGLE_API_KEY` in `.env` (for Gemini). Python 3.7+. SQLite3.

---

*Last updated: March 16, 2026*
