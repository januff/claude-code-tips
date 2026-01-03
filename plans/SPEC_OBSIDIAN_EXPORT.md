# SPEC: Obsidian Export for Sibling Databases

## Overview

Export two SQLite databases to Obsidian-compatible markdown vaults, enabling cross-referencing, search, and knowledge synthesis.

### Databases

| Database | Location | Records | Content Type |
|----------|----------|---------|--------------|
| Hall of Fake | `~/Development/Hall of Fake/hall_of_fake.db` | 1,320 videos | Sora AI clips + Whisper + Gemini analysis |
| Claude Code Tips | `~/Development/claude-code-tips/data/claude_code_tips_v2.db` | 380 tweets + 60 replies | Twitter bookmarks + thread analysis |

### Goals

1. **Searchable Knowledge Base** — Full-text search across both corpora
2. **Cross-Linking** — Link related content via shared tag taxonomy
3. **Synthesis Views** — Aggregate views by topic, creator, technique
4. **Incremental Updates** — Full regeneration on demand; vault is derived artifact

---

## Architecture Decisions

### Vault Topology
- **Two fully separate vaults** — No symlinks, no bridging
- Output locations:
  - `~/Development/Hall of Fake/vaults/`
  - `~/Development/claude-code-tips/vaults/`

### Data Flow
- **One-way: DB → Vault** — Obsidian is read-only output
- Annotations/enrichments happen in SQLite via Claude Code
- No sync back from Obsidian; full regeneration on each export

### Mental Model
- **Topic-first navigation** — Content clustered by concept/technique, not source
- Tags are the connective tissue between notes
- Organic tag emergence — minimal initial taxonomy, patterns reveal themselves

---

## Folder Structure

Both vaults use **flat root** structure:

```
vaults/
├── 2024-01-15-context-management-tips.md    # Content notes in root
├── 2024-01-20-noir-detective-scene.md
├── ...
├── _dashboards/                              # Dataview dashboards
│   ├── top-by-engagement.md
│   ├── by-creator.md
│   ├── recent-additions.md
│   └── tag-index.md
├── _resources/                               # Deduped link resources (Tips only)
│   └── github-com-anthropics-claude-code.md
├── _compilations/                            # YouTube compilation notes (HoF only)
│   └── best-sora-clips-jan-2025.md
└── attachments/                              # Media files
    ├── thumbnails/
    └── screenshots/
```

---

## Filename Convention

**Format:** `{date}-{slug}.md`

- **Date:** `liked_at` if available, fallback to `posted_at`
- **Slug:** Strict ASCII, lowercase, max 50 characters
  - Remove non-ASCII characters
  - Replace spaces with hyphens
  - Strip special characters

**Examples:**
- `2024-12-15-context-management-is-everything.md`
- `2025-01-02-noir-detective-office-scene.md`

**Fallback:** If text produces invalid slug, use `{date}-{id}.md`

---

## Tag Strategy

**Type-prefixed tags** with organic emergence:

### Hall of Fake Tags
```yaml
# Style/aesthetic
tags:
  - style/noir
  - style/cinematic
  - style/retro

# Subject categories
  - subject/human
  - subject/animal
  - subject/abstract

# Format references
  - format/commercial
  - format/music-video
  - format/film-trailer
```

### Claude Code Tips Tags
```yaml
# Features/tools
tags:
  - feature/hooks
  - feature/subagents
  - feature/mcp

# Techniques
  - technique/context-management
  - technique/planning
  - technique/automation

# Content type
  - type/thread
  - type/screenshot
  - type/code-snippet
```

---

## Frontmatter Schema

### Common Fields (Both Vaults)
```yaml
---
id: "unique_identifier"
source: "hof" | "tips"
created: 2024-01-15
author: "@handle"
url: "original_url"
tags: []
---
```

### Hall of Fake Additions
```yaml
---
# Core
video_id: "abc123"
creator: "@sora_creator"
prompt: "Original Sora prompt"
duration: 15

# Engagement
likes: 1500
views: 50000
remixes: 23
is_remix: false
parent_video_id: null  # If remix

# Content flags
has_speech: true
has_local_video: true  # Controls embed rendering

# Visual analysis (flattened from JSON)
primary_subject: "detective"
subject_category: "human"
setting: "office"
era_aesthetic: "1940s noir"
style_tags: [noir, cinematic, moody]
thematic_tags: [mystery, suspense]

# Compilation appearances
featured_in:
  - title: "Best Sora Clips January 2025"
    url: "https://youtube.com/..."
    timestamp: "2:34"
---
```

### Claude Code Tips Additions
```yaml
---
# Core
tweet_id: "123456789"
handle: "@tipster"
display_name: "Tip Author"

# Engagement
likes: 500
replies: 45
reposts: 120
views: 25000
engagement_score: 850

# Content flags
is_reply: false
is_thread: true
has_code: true
has_screenshot: true
has_external_link: true
needs_reply_fetch: false  # True if replies not yet captured

# Card/link preview
card_url: "https://github.com/..."
card_title: "Repository Name"
---
```

---

## Note Templates

### Tweet Note (Tips Vault)

```markdown
---
[frontmatter as above]
---

> [!tweet] @handle · Jan 15, 2024
> Tweet text preserved as-is, markdown may render
>
> Likes: 500 · Replies: 45 · Reposts: 120

## Media

![[attachments/screenshots/tweet_123456_1.png]]

```python
# Extracted code from screenshot
def example():
    pass
```

## Replies

> [!reply]+ @replier · High Quality
> This is a high-quality reply that appears prominently

> [!reply]- @another · Standard
> This reply is collapsed by default

## Linked Resources

- [[_resources/github-com-anthropics-claude-code|Claude Code Repository]]
```

### Video Note (HoF Vault)

```markdown
---
[frontmatter as above]
---

> [!video] @creator · 15s · Jan 2, 2025
> **Prompt:** A noir detective sits in a dimly lit office...
>
> Likes: 1,500 · Views: 50K · Remixes: 23

## Video

![[attachments/videos/abc123.mp4]]

## Transcript

> Whisper transcription text here, if has_speech is true

## Visual Analysis

> [!analysis]
> **Primary Subject:** Detective (human)
> **Setting:** 1940s office interior
> **Aesthetic:** Film noir, high contrast lighting
>
> **Characters:**
> - Detective: middle-aged male, fedora, smoking
>
> **Notable Objects:**
> - Desk lamp (key light source)
> - Rotary telephone
> - Whiskey glass

<details>
<summary>Full Analysis JSON</summary>

```json
{
  "characters": [...],
  "notable_objects": [...],
  "searchable_elements": [...]
}
```

</details>

## Remixes

- [[2025-01-05-noir-detective-remix-comedy|Comedy Remix]] — @remixer

## Featured In

- [[_compilations/best-sora-clips-jan-2025|Best Sora Clips January 2025]] at 2:34
```

---

## Reply Handling

Replies rendered as **inline callouts** with quality-based styling:

| Quality Score | Rendering |
|---------------|-----------|
| High (is_educational=1 or quality_score > 7) | `> [!reply]+` — Expanded by default, prominent |
| Medium (quality_score 4-7) | `> [!reply]` — Standard callout |
| Low (quality_score < 4) | `> [!reply]-` — Collapsed by default |

Include author attribution and relative timestamp in callout title.

---

## Resource Notes (Links)

Each unique URL in the `links` table becomes a standalone note in `_resources/`:

**Filename:** Slugified domain + path (e.g., `github-com-anthropics-claude-code.md`)

**Deduplication:** Same URL appearing in multiple tweets → single resource note with backlinks to all referencing tweets.

```markdown
---
url: "https://github.com/anthropics/claude-code"
content_type: "github"
title: "Claude Code Repository"
fetched_at: 2024-12-20
referenced_by:
  - "[[2024-12-15-claude-code-tips]]"
  - "[[2024-12-18-more-tips]]"
---

## Summary

[Fetched description/summary from links table]

## Referenced By

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
```
```

---

## Compilation Notes (HoF)

Each unique compilation in `used_in` table gets a note in `_compilations/`:

```markdown
---
compilation_id: "xyz789"
platform: "youtube"
url: "https://youtube.com/watch?v=..."
headline: "Best Sora Clips January 2025"
published_at: 2025-01-10
---

## Featured Videos

```dataviewjs
dv.table(
  ["Video", "Timestamp", "Creator"],
  dv.pages()
    .where(p => p.featured_in && p.featured_in.some(f => f.url.includes("xyz789")))
    .map(p => [p.file.link, p.featured_in.find(f => f.url.includes("xyz789")).timestamp, p.creator])
)
```
```

---

## Remix Linking

For videos with `is_remix: true`:

1. **Parent note** includes "Remixes" section listing all children
2. **Remix note** includes `parent_video_id` in frontmatter and wiki-link to parent
3. Bidirectional links enable navigation in both directions

```yaml
# In remix note frontmatter
is_remix: true
parent_video_id: "original_abc"
```

```markdown
## Original

This is a remix of [[2024-12-01-original-noir-scene|Original Noir Scene]]
```

---

## Dashboards

Four pre-built dashboards using DataviewJS in `_dashboards/`:

### top-by-engagement.md
```dataviewjs
dv.table(
  ["Note", "Likes", "Views", "Score"],
  dv.pages()
    .where(p => p.source && !p.file.path.includes("_"))
    .sort(p => p.likes, 'desc')
    .limit(50)
    .map(p => [p.file.link, p.likes, p.views, p.engagement_score || "—"])
)
```

### by-creator.md
```dataviewjs
const creators = dv.pages()
  .where(p => p.author || p.creator)
  .groupBy(p => p.author || p.creator);

for (let group of creators) {
  dv.header(3, group.key);
  dv.list(group.rows.map(p => p.file.link).slice(0, 10));
}
```

### recent-additions.md
```dataviewjs
dv.table(
  ["Note", "Created", "Author"],
  dv.pages()
    .where(p => p.source && !p.file.path.includes("_"))
    .sort(p => p.created, 'desc')
    .limit(30)
    .map(p => [p.file.link, p.created, p.author || p.creator])
)
```

### tag-index.md
```dataviewjs
const allTags = {};
dv.pages().forEach(p => {
  (p.tags || []).forEach(t => {
    allTags[t] = (allTags[t] || 0) + 1;
  });
});

const sorted = Object.entries(allTags).sort((a, b) => b[1] - a[1]);
dv.table(["Tag", "Count"], sorted.slice(0, 100));
```

---

## Video Embed Handling

**Conditional rendering** based on `local_filename` presence:

```python
if video.local_filename:
    # Embed local video
    embed = f"![[attachments/videos/{video.local_filename}]]"
else:
    # Link to source only
    embed = f"[View on Sora]({video.download_url})"
```

Thumbnails always embedded if available:
```markdown
![[attachments/thumbnails/{video_id}.jpg]]
```

---

## Implementation

### Technology Stack
- **Python 3.10+** with type hints
- **Jinja2** for note templates
- **SQLite3** for database access
- **Pathlib** for file operations

### Project Structure
```
scripts/
├── obsidian_export/
│   ├── __init__.py
│   ├── core.py           # Shared export logic
│   ├── models.py         # Dataclasses for records
│   ├── templates/        # Jinja2 templates
│   │   ├── tweet.md.j2
│   │   ├── video.md.j2
│   │   ├── resource.md.j2
│   │   └── dashboard.md.j2
│   └── utils.py          # Slug generation, date handling
├── export_tips.py        # Thin wrapper for Tips vault
└── export_hof.py         # Thin wrapper for HoF vault
```

### CLI Interface
```bash
# Full export
python scripts/export_tips.py

# Sample mode for testing
python scripts/export_tips.py --limit=10

# Specify output directory
python scripts/export_hof.py --output ~/custom/path
```

### Error Handling
- **Best effort + summary** — Export everything possible
- Log warnings for malformed records
- Generate summary report at end:
  ```
  Export complete:
    - 378/380 tweets exported
    - 2 skipped (malformed)
    - 156 resources generated
    - 4 dashboards created
  See export_errors.log for details
  ```

### JSON Parsing
- **Dynamic handling** — Parse whatever structure exists
- Flatten known fields to arrays for frontmatter
- Preserve full JSON in collapsible body section
- No strict schema enforcement; adapt to variations

---

## Database State Notes

### Hall of Fake
- 1,320 videos total
- 1,319 have visual_analysis (99.9% coverage)
- Structured entity data already in `visual_analysis` table
- `used_in` table tracks YouTube compilation appearances

### Claude Code Tips
- 380 tweets collected
- 60 thread_replies across 17 parent tweets (sparse coverage)
- `tips` table is **empty** — curation not yet done
- `links` table has resolved URLs with summaries
- `media` table has OCR text and vision descriptions

### Pre-Export Curation (Recommended)
Before full export, consider running a curation pass to:
1. Populate `tips` table with extracted commands/tools
2. Fetch missing thread replies for high-engagement tweets
3. Generate thumbnails for HoF videos without them

---

## Open Items for Implementation

1. **Thumbnail generation** — Script to extract first frame from videos
2. **Slug collision handling** — What if two notes produce same date+slug?
3. **Template refinement** — May need iteration on callout styling
4. **Cross-vault linking** — Currently separate; reconsider if needed later
5. **Curation pass tooling** — Scripts to populate `tips` table

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-02 | Initial spec created |
| 2026-01-02 | Comprehensive interview completed — 15 question rounds |
| 2026-01-02 | Full requirements documented |

---

*Spec finalized: 2026-01-02 — Ready for implementation planning*
