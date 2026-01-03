# SPEC: Obsidian Export for Sibling Databases

## Overview

Export two SQLite databases to Obsidian-compatible markdown vaults, enabling cross-referencing, search, and knowledge synthesis.

### Databases

| Database | Records | Content Type |
|----------|---------|--------------|
| Hall of Fake | 1,435 videos | Sora AI clips + Whisper + Gemini analysis |
| Claude Code Tips | 380 tweets + 159 replies | Twitter bookmarks + thread analysis |

### Goals

1. **Searchable Knowledge Base** — Full-text search across both corpora
2. **Cross-Linking** — Link related content between databases
3. **Synthesis Views** — Aggregate views by topic, creator, technique
4. **Incremental Updates** — New content flows into vault automatically

---

## Interview Prompt

Use this with Claude Code to generate a comprehensive implementation spec:

```
Read this @SPEC_OBSIDIAN_EXPORT.md and interview me in detail using the 
AskUserQuestionTool about literally anything: 

- Vault structure and folder organization
- Note templates and frontmatter schema
- Linking strategies (internal, backlinks, MOCs)
- Tag taxonomy and metadata
- Dataview queries and aggregation views
- Incremental update workflow
- Cross-database connections
- Plugin requirements
- Export format preferences
- Sync and backup considerations

Make sure questions are not obvious. Be very in-depth and continue 
until you have enough detail to implement a complete solution.
```

---

## Known Considerations

### Hall of Fake Data

Each video record has:
- `video_id` — Unique identifier
- `title` / `discovery_phrase` — Content description
- `creator_handle` / `creator_display_name` — Attribution
- `whisper_text` — Transcription (if speech detected)
- `gemini_analysis` — Visual description, themes, techniques
- `posted_at` / `liked_at` — Timestamps
- `video_duration` — Length in seconds
- `download_url` — Source link

### Claude Code Tips Data

Each tweet has:
- `tweet_id` — Unique identifier
- `handle` / `display_name` — Author
- `text` — Tweet content
- `likes`, `replies`, `reposts`, `views` — Engagement
- `posted_at` — Timestamp
- `card_url` — Linked resource
- `is_reply`, `reply_to_id` — Thread structure

Plus enrichment:
- `links` table — Resolved URLs with summaries
- `media` table — Image analysis and OCR
- `thread_replies` — Reply conversations

### Potential Cross-Links

- **Technique mentions** — "hooks", "subagents", "LSP" in tips → related Sora clips demonstrating AI capabilities
- **Creator overlap** — Same person posting tips and creating Sora content
- **Temporal** — Tips about new features → Sora clips using those features
- **Topic clusters** — "context management", "planning", "automation"

---

## Open Questions

These should emerge from the interview:

- Single vault or separate vaults per database?
- How to handle media files (videos, images)?
- What Obsidian plugins are required/recommended?
- How to structure MOCs (Maps of Content)?
- Tag hierarchy vs flat tags?
- Daily notes integration?
- Template for each content type?
- How to handle updates (append vs regenerate)?
- Backlink density preferences?
- Canvas views for visualization?

---

*SPEC created: 2026-01-02 — Ready for interview*
