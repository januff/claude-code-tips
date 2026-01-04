# HANDOFF: Template Restructure + Keyword Enrichment

**Created:** 2026-01-03
**Updated:** 2026-01-03 (Phase 1 complete, added Gemini enrichment details)
**Purpose:** Restructure frontmatter and add LLM-powered keyword extraction
**Test with:** `--limit 10` sample before full run

---

## Phase 1: Template Restructure ✅ COMPLETE

- Moved metrics to collapsed `[!metrics]-` callout
- Fixed dashboard number formatting with `toLocaleString()`
- Cleaned frontmatter to 7 essential fields

**Status:** Ready for Obsidian review

---

## Phase 2: LLM Keyword Enrichment (Gemini)

### Reference Implementation

Use the pattern from `hall-of-fake/batch_full_analysis.py`:
- **Provider:** Google Gemini via `GOOGLE_API_KEY`
- **Model:** `gemini-2.0-flash-001` (fast, cheap for text analysis)
- **Features to copy:**
  - Checkpointing every N items
  - `--resume` flag
  - `--limit N` for testing
  - Rate limiting with exponential backoff
  - Graceful shutdown on Ctrl+C
  - Cost tracking

### New Script: `scripts/enrich_keywords.py`

```python
#!/usr/bin/env python3
"""
Keyword enrichment for Claude Code tips using Gemini.

Usage:
    python scripts/enrich_keywords.py --limit 10    # Test on 10 tweets
    python scripts/enrich_keywords.py               # Full run
    python scripts/enrich_keywords.py --resume      # Resume from checkpoint
"""
```

### Database Changes

Add columns to `tips` table:
```sql
ALTER TABLE tips ADD COLUMN keywords_json TEXT;      -- ["teleport", "context", "session"]
ALTER TABLE tips ADD COLUMN primary_keyword TEXT;    -- "teleport" (for filename)
ALTER TABLE tips ADD COLUMN llm_category TEXT;       -- LLM-refined category
ALTER TABLE tips ADD COLUMN llm_tools TEXT;          -- JSON array of tools
ALTER TABLE tips ADD COLUMN enrichment_model TEXT;   -- "gemini-2.0-flash-001"
ALTER TABLE tips ADD COLUMN enrichment_cost REAL;    -- Cost in USD
```

### Gemini Prompt

```
Analyze this Claude Code tip tweet and extract keywords for categorization.

Tweet: "{tweet_text}"
Author: {handle}
Likes: {likes}
Current regex-based category: {category}

Return JSON only (no markdown):
{
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "primary_keyword": "best_single_keyword",
  "category": "refined_category",
  "tools": ["tool1", "tool2"],
  "confidence": 0.9
}

Guidelines:
- keywords: 3-6 descriptive terms specific to Claude Code concepts
- primary_keyword: 1-2 words, suitable for filename (e.g., "teleport", "context-window", "handoff")
- category: One of: context-management, planning, hooks, subagents, mcp, skills, commands, automation, workflow, tooling, meta, other
- tools: Claude Code features mentioned (e.g., "/clear", "--resume", "AskUserQuestionTool", "hooks", "LSP")
- confidence: 0.0-1.0 how confident in this analysis

Good primary_keyword examples: teleport, session-resume, context-window, subagent-spawn, hook-config, handoff-pattern, plan-mode, sandbox
```

### Cost Estimate

- **Model:** gemini-2.0-flash-001
- **Input:** ~200 tokens/tweet (tweet text + prompt)
- **Output:** ~100 tokens (JSON response)
- **Pricing:** $0.10/1M input, $0.40/1M output
- **Per tweet:** ~$0.00006
- **380 tweets:** ~$0.02 total

### Execution

```bash
cd ~/Development/claude-code-tips
source ~/Development/Hall\ of\ Fake/venv/bin/activate

# Ensure GOOGLE_API_KEY is set
export GOOGLE_API_KEY="your-key-here"

# Test on 10 highest-engagement tweets
python scripts/enrich_keywords.py --limit 10

# Check results
sqlite3 data/claude_code_tips_v2.db "SELECT tweet_id, primary_keyword, keywords_json FROM tips WHERE primary_keyword IS NOT NULL LIMIT 10;"

# If good, run full enrichment
python scripts/enrich_keywords.py

# Re-export with new keywords
python scripts/export_tips.py --limit 10  # Verify filenames changed
python scripts/export_tips.py             # Full export
```

### Export Updates

After enrichment, update export to use keywords:

**In `utils.py` slugify:**
```python
def generate_filename(tweet, date_str):
    # Prefer primary_keyword if available
    if tweet.primary_keyword:
        slug = slugify(tweet.primary_keyword)
    else:
        slug = slugify(tweet.text[:50])
    return f"{date_str}-{slug}.md"
```

**In `tweet.md.j2` tags:**
```jinja
tags:
{% for tag in tags %}
  - {{ tag }}
{% endfor %}
{% if tweet.keywords %}
{% for kw in tweet.keywords %}
  - topic/{{ kw }}
{% endfor %}
{% endif %}
```

---

## Test Checklist

### After Phase 2 (10 samples):
- [ ] `primary_keyword` populated for all 10
- [ ] Keywords are specific and useful (not generic)
- [ ] Filenames use keywords (e.g., `2025-12-26-teleport.md`)
- [ ] Tags include `topic/` prefixed keywords
- [ ] Categories refined where regex was wrong
- [ ] Cost tracking shows reasonable amounts

### After Full Run:
- [ ] All 380 tweets enriched
- [ ] Total cost < $0.10
- [ ] Export produces clean filenames
- [ ] Graph view shows useful topic clusters

---

## Skill Abstraction (Future)

Both projects now use Gemini for enrichment:
- **Hall of Fake:** Visual analysis of videos
- **Claude Code Tips:** Keyword extraction from text

Consider extracting shared pattern to a skill:
```
skills/
└── llm-enrichment/
    ├── SKILL.md
    ├── gemini_client.py
    ├── checkpoint.py
    └── batch_processor.py
```

This would standardize:
- Provider configuration
- Checkpointing
- Rate limiting
- Cost tracking
- Resume capability

Defer until after both projects have stable enrichment pipelines.

---

*Handoff updated: 2026-01-03*
