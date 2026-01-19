# Current Focus

> **Quick pointer for fresh Claude instances.**
> Check this file first to know where the action is.

**Last Updated:** January 19, 2026

---

## Active Project

| Field | Value |
|-------|-------|
| **Active Repo** | `hall-of-fake` |
| **Handoff Location** | `hall-of-fake/HANDOFF.md` |
| **Claude.ai Project** | Hall of Fake |

## What Happened Recently

### January 18-19, 2026 (hall-of-fake)

**Family Browser UI Debugging Session:**
- Fixed video hover preview in Family Browser UI
- Fixed selection border visibility (green border now shows during hover)
- Fixed Shift+audio functionality with browser autoplay compliance
- Diagnosed and fixed major video playback issue:
  - Created `scripts/check_video_mapping.py` diagnostic tool
  - Discovered single-threaded server was causing timeouts
  - Switched from `TCPServer` to `ThreadingTCPServer`
  - All 821 singletons now play correctly

**Hall of Fake Current State:**
- Total Videos: 1,435
- Multi-video Families: 123 (34 manual)
- Singletons: 821
- Family Browser UI: ✅ Fully working at localhost:8765

### January 6-10, 2026 (claude-code-tips)

- Claude Code 2.1.0 release captured
- Ralph Wiggum viral breakdown documented
- Vault export duplicate file issue fixed
- Data: 424 tweets, 1,754 thread replies, 131 vault notes

## Next Steps

**Focus is now on Hall of Fake:**
1. Use Family Browser UI to assign singletons to families
2. Contact sheet generation after family changes
3. Check for new Sora likes to fetch
4. Refresh Obsidian vault export with updated families

**Deferred for claude-code-tips:**
- Bookmark refresh (fetch new content since Jan 8)
- Metrics refresh, slash commands

---

## Session Wind-Down Checklist

When ending a session, update these files:

- [x] `CURRENT_FOCUS.md` in **both repos** — point to active project
- [x] Session log — `hall-of-fake/docs/SESSION_LOG_2026-01-19.md`
- [ ] `PROGRESS.md` — technique adoption updates
- [x] `HANDOFF.md` — next tasks
- [x] Git commit and push

---

*This file exists in both repos. Always update both when switching focus.*
