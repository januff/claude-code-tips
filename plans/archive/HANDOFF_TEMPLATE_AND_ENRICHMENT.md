# HANDOFF: Template Fixes + Enrichment Pipeline

**Created:** 2026-01-03
**Updated:** 2026-01-04
**Purpose:** Fix template issues and run comprehensive LLM enrichment

---

## Phase 1: Template Structure Fix (REDO NEEDED)

### Problem with Current Implementation

The Phase 1 changes removed engagement from the wrong place:
- ❌ Removed engagement line from tweet card (should keep)
- ❌ Left metrics in frontmatter properties (should remove)
- ❌ Placed `[!metrics]-` callout in middle (should be at bottom)

### Correct Structure

```markdown
---
created: 2025-12-26
author: "@chongdashu"
display_name: "Chong-U"
category: "context-management"
tools: ["--teleport"]
tags:
  - category/context-management
  - type/thread
  - tool/--teleport
url: "https://x.com/..."
---

> [!tweet] @chongdashu · Dec 26, 2025
> Tweet text here...
>
> Likes: 800 · Replies: 16 · Reposts: 39  ← KEEP THIS LINE

## Media

![[attachments/screenshots/tweet_123_1.png]]

## Replies

> [!reply]+ @someone · High Quality
> Reply text...

> [!metrics]- Engagement & Metadata  ← AT VERY BOTTOM
> **Likes:** 800 · **Views:** 72,244 · **Engagement Score:** 2,900
> 
> **Source:** tips · **Quality:** 9/10
> **Curated:** ✓ · **Reply:** ✗
> **ID:** [2004579780998688823](https://x.com/...)
```

### Changes Required

**In `tweet.md.j2`:**
1. Remove `likes`, `views`, `engagement_score` from frontmatter YAML
2. Restore engagement line in the `[!tweet]` callout
3. Move `[!metrics]-` section to END of file (after Replies, after Linked Resources)

---

## Phase 2: Enrichment Pipeline Inventory

### Overview of ALL Gemini Calls

| Task | Input | Output | Records | Est. Cost |
|------|-------|--------|---------|-----------|
| **Keyword Extraction** | Tweet text | keywords, primary_keyword, category, tools | 380 tweets | ~$0.02 |
| **Resource Summarization** | Fetched webpage content | summary, key_points, relevance_score | 10 links | ~$0.01 |
| **Media Download** | URLs | Local files in attachments/ | 12 media | $0 (no LLM) |
| **Video Workflow Descriptions** | Video frames | workflow_description | ~5 videos | ~$0.05 |

**Total estimated cost:** ~$0.08

### Task A: Keyword Extraction (Primary)

**Input per tweet:**
```json
{
  "tweet_text": "Not many know about this hidden command...",
  "author": "@chongdashu",
  "likes": 800,
  "current_category": "context-management"
}
```

**Output:**
```json
{
  "keywords": ["teleport", "session-resume", "cli-button", "context-transfer"],
  "primary_keyword": "teleport",
  "category": "context-management",
  "tools": ["--teleport", "Open in CLI"],
  "confidence": 0.95
}
```

**Database columns:**
- `tips.keywords_json` — Full keyword list
- `tips.primary_keyword` — For filename
- `tips.llm_category` — Refined category
- `tips.llm_tools` — JSON array

### Task B: Resource Summarization

The `links` table has 10 resolved URLs. We need to:
1. Fetch full content (if not already done)
2. Send to Gemini for summarization
3. Generate standalone resource notes

**Input:**
```json
{
  "url": "https://github.com/ComposioHQ/awesome-claude-skills",
  "title": "awesome-claude-skills",
  "content_type": "github",
  "fetched_content": "README.md contents..."
}
```

**Output:**
```json
{
  "summary": "Curated collection of Claude Code skills including...",
  "key_points": ["Skills for automation", "MCP integrations", "Custom commands"],
  "resource_type": "github-awesome-list",
  "relevance_tags": ["skills", "mcp", "automation"]
}
```

**Database columns (add to links table):**
- `links.llm_summary` — Rich summary
- `links.key_points_json` — Extracted key points
- `links.relevance_tags_json` — Tags for cross-referencing

**Export output:**
```
_resources/
├── github-composiohq-awesome-claude-skills.md
├── github-feiskyer-claude-code-settings.md
├── blog-sankalp-claude-code-2-guide.md
└── ...
```

### Task C: Media File Download (No LLM)

Currently media URLs exist but files aren't downloaded locally.

**Script: `scripts/download_media.py`**
```python
# For each media record with URL but no local_path:
# 1. Download image/video to data/media/
# 2. Update media.local_path in database
# 3. Export copies to vault/attachments/screenshots/
```

**After download, export should symlink or copy:**
```
vault/attachments/
├── screenshots/
│   ├── tweet_123_1.png
│   └── tweet_456_1.jpg
├── thumbnails/  (for HoF)
└── videos/      (for HoF)
```

### Task D: Video Workflow Descriptions (Bookmarked)

For media items where `media_type = 'video'` and content is instructional (screen recordings):

**Input:** 4 frames extracted from video
**Output:**
```json
{
  "workflow_description": "Demonstrates clicking 'Open in CLI' button in Claude Code Chrome interface, copying the teleport command, switching to Cursor terminal, and resuming the session with full context.",
  "steps": [
    "Click 'Open in CLI' button in top-right",
    "Copy command to clipboard",
    "Paste in Cursor terminal",
    "Session resumes with history"
  ],
  "tools_shown": ["Open in CLI", "claude --teleport", "Cursor"]
}
```

**Defer this** until after A, B, C are complete.

---

## Phase 2 Execution Order

```bash
cd ~/Development/claude-code-tips
source ~/Development/Hall\ of\ Fake/venv/bin/activate
export GOOGLE_API_KEY="..."

# 1. Fix template first
#    (Claude Code fixes tweet.md.j2)

# 2. Download media files locally
python scripts/download_media.py

# 3. Keyword enrichment (10 samples first)
python scripts/enrich_keywords.py --limit 10
python scripts/export_tips.py --limit 10
# → Verify in Obsidian

# 4. Full keyword enrichment
python scripts/enrich_keywords.py

# 5. Resource summarization
python scripts/enrich_resources.py

# 6. Full export
python scripts/export_tips.py
# → Open in Obsidian, verify:
#    - Short filenames
#    - Attachments present
#    - Resource notes in _resources/
#    - Metrics at bottom of each note
```

---

## Script Templates

### enrich_keywords.py

Reference `hall-of-fake/batch_full_analysis.py` for:
- Checkpointing
- Resume capability
- Rate limiting
- Cost tracking
- Graceful shutdown

### enrich_resources.py

```python
# For each link in links table:
# 1. Fetch content if not cached (web_fetch or use existing)
# 2. Send to Gemini with summarization prompt
# 3. Update links table with llm_summary, key_points_json
# 4. Support --limit and --resume
```

### download_media.py

```python
# For each media in media table where local_path is NULL:
# 1. Download from url to data/media/{tweet_id}_{index}.{ext}
# 2. Update media.local_path
# 3. No LLM calls needed
```

---

## Export Updates After Enrichment

### Filename generation (utils.py)
```python
def generate_filename(tweet, date_str):
    if tweet.primary_keyword:
        return f"{date_str}-{slugify(tweet.primary_keyword)}.md"
    return f"{date_str}-{slugify(tweet.text[:50])}.md"
```

### Resource notes (core.py)
```python
def export_resources(self):
    for resource in self.load_resources():
        note = self.render_template('resource.md.j2', resource=resource)
        path = self.output_dir / '_resources' / f"{slugify(resource.url)}.md"
        path.write_text(note)
```

### Attachments (core.py)
```python
def setup_attachments(self):
    # Symlink or copy media files to vault/attachments/
    screenshots_dir = self.output_dir / 'attachments' / 'screenshots'
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    for media in self.media_with_local_files:
        src = Path(media.local_path)
        dst = screenshots_dir / src.name
        if not dst.exists():
            shutil.copy(src, dst)  # or symlink
```

---

## Test Checklist

### After Template Fix:
- [ ] Frontmatter has NO likes/views/engagement_score
- [ ] Tweet card shows engagement line (Likes: X · Replies: Y)
- [ ] `[!metrics]-` callout is at VERY BOTTOM of note
- [ ] Callout shows all metadata with formatting

### After Media Download:
- [ ] `vault/attachments/screenshots/` has files
- [ ] Notes show embedded images (not broken links)

### After Keyword Enrichment (10 samples):
- [ ] Filenames are short and descriptive
- [ ] Keywords appear in tags
- [ ] Categories refined where needed

### After Resource Enrichment:
- [ ] `_resources/` folder has markdown notes
- [ ] Each resource has summary and key points
- [ ] Backlinks work from tweet notes to resources

---

*Handoff updated: 2026-01-04*
