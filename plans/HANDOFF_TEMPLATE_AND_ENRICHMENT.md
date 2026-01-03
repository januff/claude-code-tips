# HANDOFF: Template Restructure + Keyword Enrichment

**Created:** 2026-01-03
**Purpose:** Restructure frontmatter and add LLM-powered keyword extraction
**Test with:** `--limit 10` sample before full run

---

## Part 1: Template Restructure (No LLM)

### Move Metrics to Collapsed Callout

**Current frontmatter has too many fields.** Move metrics out, keep only essentials.

**Keep in frontmatter:**
```yaml
created
author
display_name
category
tools
tags
url
```

**Move to collapsed callout in note body:**
```markdown
> [!metrics]- Engagement & Metadata
> **Likes:** 800 · **Replies:** 16 · **Reposts:** 39 · **Views:** 72,244
> **Engagement Score:** 2,900
> 
> **Source:** tips · **Quality:** 9/10
> **Curated:** ✓ · **Reply:** ✗
> **ID:** [2004579780998688823](https://x.com/...)
```

**Update `tweet.md.j2`** to reflect this structure.

### Fix Dashboard Number Formatting

**Update DataviewJS in dashboard templates** to use `toLocaleString()`:

```javascript
.map(p => [
  p.file.link, 
  p.likes?.toLocaleString() || "0",
  p.views?.toLocaleString() || "0",
  p.engagement_score?.toLocaleString() || "0"
])
```

---

## Part 2: LLM Keyword Enrichment

### Goal

Single LLM pass per tweet generates multiple useful outputs:
- **Primary keyword** → filename slug (`2025-12-26-teleport.md`)
- **All keywords** → tags (with prefixes like `topic/`, `technique/`)
- **Refined category** → validate/improve regex-based category
- **Tools identified** → any Claude Code features mentioned

### New Database Columns

Add to `tips` table:
```sql
ALTER TABLE tips ADD COLUMN keywords_json TEXT;      -- ["teleport", "context", "session"]
ALTER TABLE tips ADD COLUMN primary_keyword TEXT;    -- "teleport"
ALTER TABLE tips ADD COLUMN llm_category TEXT;       -- LLM-refined category
ALTER TABLE tips ADD COLUMN llm_tools TEXT;          -- JSON array of tools
ALTER TABLE tips ADD COLUMN enrichment_notes TEXT;   -- Optional: LLM observations
```

### LLM Prompt

```
Analyze this Claude Code tip tweet and extract:

Tweet: "{tweet_text}"
Author: {handle}
Current category: {regex_category}

Return JSON:
{
  "keywords": ["keyword1", "keyword2", ...],  // 3-6 descriptive keywords
  "primary_keyword": "best_one",              // 1-2 words for filename
  "category": "refined_category",             // One of: context-management, planning, hooks, subagents, mcp, skills, commands, automation, workflow, tooling, meta, other
  "tools": ["tool1", "tool2"],                // Claude Code tools/features mentioned
  "confidence": 0.9                           // How confident in analysis
}

Keywords should be:
- Specific to Claude Code concepts when applicable
- Useful for grouping related tips
- Good for search/discovery

Examples of good keywords: teleport, session-resume, context-window, subagent, hook, CLAUDE.md, handoff, planning-mode, sandbox
```

### Enrichment Script

Create `scripts/enrich_keywords.py`:
- Load tweets from database
- Call LLM API (Claude or GPT) for each
- Store results in new columns
- Support `--limit N` for testing
- Support `--dry-run` to preview without saving

### Update Export to Use Keywords

After enrichment, update `utils.py` and templates:
- Filename: use `primary_keyword` if available, fallback to current slugify
- Tags: merge `keywords` with existing tags (add `topic/` prefix)
- Category: prefer `llm_category` over regex `category`

---

## Execution Order

### Phase 1: Template fixes (no LLM)
```bash
# Fix template structure and dashboards
# Then test:
python scripts/export_tips.py --limit 10
# Verify in Obsidian:
# - Metrics in collapsed callout
# - Dashboard numbers formatted
```

### Phase 2: Keyword enrichment (10 samples)
```bash
# Run enrichment on 10 highest-engagement tweets
python scripts/enrich_keywords.py --limit 10

# Re-export samples
python scripts/export_tips.py --limit 10

# Verify in Obsidian:
# - Filenames use keywords
# - Tags include extracted keywords
# - Categories refined
```

### Phase 3: Full enrichment (if samples look good)
```bash
python scripts/enrich_keywords.py           # All 380 tweets
python scripts/export_tips.py               # Full vault
```

---

## Test Checklist

### After Phase 1:
- [ ] Frontmatter has only: created, author, display_name, category, tools, tags, url
- [ ] Collapsed `[!metrics]-` callout shows engagement data
- [ ] Numbers in callout have commas
- [ ] Dashboard tables show formatted numbers

### After Phase 2:
- [ ] Sample filenames are short and descriptive (e.g., `2025-12-26-teleport.md`)
- [ ] Keywords appear in tags (e.g., `topic/teleport`, `topic/context`)
- [ ] Categories seem accurate
- [ ] Tools list captures Claude Code features mentioned

---

## API Considerations

- **Model:** Claude Sonnet or Haiku (fast, cheap for classification)
- **Cost estimate:** ~$0.01-0.02 per tweet → ~$4-8 for all 380
- **Rate limiting:** Add delays between calls
- **Error handling:** Log failures, continue processing

---

*Handoff created: 2026-01-03*
