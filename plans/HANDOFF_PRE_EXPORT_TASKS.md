# HANDOFF: Pre-Export Tasks

**Created:** 2026-01-03
**Purpose:** Prepare both databases for Obsidian export
**Sequence:** Curation → Thumbnails → Export Library

---

## Task 1: Claude Code Tips Curation Pass

**Goal:** Populate the empty `tips` table by analyzing tweet content

**Database:** `~/Development/claude-code-tips/data/claude_code_tips_v2.db`

**Current state:**
- `tweets` table: 380 records with full content
- `tips` table: EXISTS but EMPTY (has columns: tip_number, category, summary, is_curated, quality_rating)

**What to extract from each tweet:**

1. **category** — Classify into one of:
   - `context-management`
   - `planning`
   - `automation`
   - `hooks`
   - `subagents`
   - `mcp`
   - `skills`
   - `commands`
   - `workflow`
   - `tooling`
   - `meta` (tips about using Claude itself)
   - `other`

2. **summary** — One-sentence distillation of the tip (if it is a tip)

3. **quality_rating** — 1-10 based on:
   - Actionability (is it a concrete technique?)
   - Novelty (is it widely known or unique?)
   - Engagement correlation (likes/reposts as signal)

4. **extracted_tools** — JSON array of tools/commands mentioned:
   - Slash commands (`/clear`, `/compact`, `/resume`)
   - CLI flags (`--resume`, `--chrome`)
   - Tool names (`AskUserQuestionTool`, `Bash`)
   - Features (`hooks`, `subagents`, `LSP`)

5. **extracted_code** — Any code snippets in the tweet text

**Approach:**
```sql
-- Check current tips schema
.schema tips

-- For each tweet, analyze and INSERT into tips
-- Link via tweet_id foreign key
```

**Success criteria:**
- All 380 tweets have corresponding tips records
- Categories distributed reasonably (not all "other")
- High-engagement tweets have quality_rating >= 7
- extracted_tools populated where applicable

---

## Task 2: Hall of Fake Thumbnail Generation

**Goal:** Extract first frame from each video as thumbnail

**Database:** `~/Development/Hall of Fake/hall_of_fake.db`
**Videos:** `~/Development/Hall of Fake/videos/`

**Current state:**
- 1,435 videos downloaded
- No thumbnails directory exists

**Output:**
```
~/Development/Hall of Fake/thumbnails/
├── {video_id}.jpg
├── {video_id}.jpg
└── ...
```

**Approach:**
```bash
# Use ffmpeg to extract first frame
ffmpeg -i input.mp4 -vframes 1 -q:v 2 output.jpg
```

**Script requirements:**
- Read video paths from database (`local_filename` column)
- Skip if thumbnail already exists
- Handle missing videos gracefully
- Report: X thumbnails created, Y skipped, Z errors

**Success criteria:**
- Thumbnail exists for every video with `local_filename`
- Thumbnails are reasonable size (not full 4K, ~720p max)
- Database updated with `thumbnail_path` if column exists (or create it)

---

## Task 3: Build Export Library

**Goal:** Implement the Obsidian export per SPEC_OBSIDIAN_EXPORT.md

**Spec location:** `plans/SPEC_OBSIDIAN_EXPORT.md`

**Deliverables:**
```
scripts/
├── obsidian_export/
│   ├── __init__.py
│   ├── core.py
│   ├── models.py
│   ├── templates/
│   │   ├── tweet.md.j2
│   │   ├── video.md.j2
│   │   ├── resource.md.j2
│   │   └── dashboard.md.j2
│   └── utils.py
├── export_tips.py
└── export_hof.py
```

**Test with:**
```bash
python scripts/export_tips.py --sample 10
# Open vault/ in Obsidian, verify rendering
```

**Success criteria:**
- Sample export renders correctly in Obsidian
- Frontmatter matches spec schema
- Callouts display properly
- Dataview dashboards query successfully

---

## Execution Order

```
1. Run Task 1 (curation) in claude-code-tips repo
   └── Verify: SELECT COUNT(*) FROM tips WHERE is_curated = 1

2. Run Task 2 (thumbnails) in Hall of Fake repo
   └── Verify: ls ~/Development/Hall\ of\ Fake/thumbnails/ | wc -l

3. Run Task 3 (export library) - can start in either repo
   └── Verify: Open vault/ in Obsidian, check sample notes
```

---

## Notes

- Tasks 1 and 2 are independent — could run in parallel
- Task 3 depends on both being complete for full export
- The `--sample` flag is essential for iterating on templates
- Full regeneration means we can re-run export freely

---

*Handoff created: 2026-01-03 — Ready for Claude Code execution*
