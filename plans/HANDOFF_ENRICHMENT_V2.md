# HANDOFF: Enrichment Iteration v2

**Created:** 2026-01-04
**Purpose:** Re-run keyword enrichment with refined prompt + add media/link analysis
**Scope:** 10 sample tweets first, then expand if results are good

---

## Context

First enrichment pass produced keywords that are too generic:
- Picked `claude-code-trick` when `underrated-trick` was in the list
- Picked `claude-sync` when `teleport` was available
- Missed actual command names like `--teleport`, `AskUserQuestionTool`, `ccc` alias

Also missing: analysis of attached media (videos, screenshots) and linked content (blog posts, docs).

---

## Task 1: Re-run Keyword Enrichment with Refined Prompt

### Update `scripts/enrich_keywords.py`

Replace the prompt with this refined version:

```python
ENRICHMENT_PROMPT = """You are analyzing a Claude Code tip tweet to extract the MOST SPECIFIC identifier for this content.

Tweet: "{tweet_text}"
Author: @{handle}
Likes: {likes}

Your goal is to find THE PRECISE TERM that uniquely identifies what this tweet is about:

PRIORITY ORDER:
1. If it mentions a SPECIFIC COMMAND or FLAG, use that exactly (e.g., "--teleport", "--sandbox", "/compact", "ccc")
2. If it mentions a SPECIFIC TOOL by name, use that (e.g., "AskUserQuestionTool", "TaskTool", "Bash")
3. If it's about a TECHNIQUE, use the most distinctive phrase from the tweet (e.g., "underrated-trick", "agent-swarms")
4. Only use generic terms as last resort

AVOID as primary_keyword:
- "claude-code" (redundant - entire vault is Claude Code tips)
- "claude-" prefix unless Claude itself is the subject
- Generic words: "tip", "trick", "hack", "workflow" unless paired with specific modifier

Return JSON only (no markdown):
{{
  "primary_keyword": "most-specific-identifier",
  "keywords": ["other", "relevant", "specific", "terms"],
  "command_or_flag": "--actual-flag-if-mentioned or null",
  "tool_name": "ActualToolName if mentioned or null", 
  "category": "one of: context-management, planning, hooks, subagents, mcp, skills, commands, automation, workflow, tooling, meta, prompting, security",
  "confidence": 0.0-1.0
}}

The primary_keyword should be what the user would type to FIND this later, or the actual command they'd USE.
Specificity beats description. Shorter is better if equally specific."""
```

### Add New Database Columns

```sql
ALTER TABLE tips ADD COLUMN command_or_flag TEXT;
ALTER TABLE tips ADD COLUMN tool_name TEXT;
```

### Clear Previous Enrichment for Re-run

```sql
UPDATE tips SET 
  primary_keyword = NULL,
  keywords_json = NULL,
  llm_category = NULL,
  llm_tools = NULL
WHERE tweet_id IN (SELECT id FROM tweets ORDER BY likes DESC LIMIT 10);
```

### Run on 10 Samples

```bash
python scripts/enrich_keywords.py --limit 10
```

### Verify with Date for Easier Matching

```sql
SELECT 
  t.posted_at,
  ti.primary_keyword, 
  ti.command_or_flag,
  ti.tool_name,
  ti.keywords_json 
FROM tips ti
JOIN tweets t ON ti.tweet_id = t.id
WHERE ti.primary_keyword IS NOT NULL 
ORDER BY t.likes DESC
LIMIT 10;
```

---

## Task 2: Media Analysis (Videos & Screenshots)

For tweets with attached media, analyze content with Gemini Vision.

### Check What Media Exists

```sql
SELECT m.tweet_id, m.media_type, m.url, m.local_path, m.vision_description
FROM media m
JOIN tweets t ON m.tweet_id = t.id
ORDER BY t.likes DESC
LIMIT 20;
```

### Create `scripts/enrich_media.py`

Reference `hall-of-fake/batch_full_analysis.py` for the Gemini vision pattern.

For each media item without `vision_description`:

**If video (local_path exists):**
1. Extract 4 frames with ffmpeg (like Hall of Fake)
2. Send to Gemini with prompt:

```
This is a screen recording from a Claude Code tutorial tweet.
Describe the WORKFLOW being demonstrated:
- What buttons/UI elements are clicked?
- What commands are typed?
- What is the end result?

Be specific about command names, flags, and UI elements.
Return JSON:
{
  "workflow_summary": "one paragraph description",
  "commands_shown": ["--teleport session_id", "claude --resume"],
  "ui_elements": ["Open in CLI button", "Cursor terminal"],
  "key_action": "the main thing being demonstrated"
}
```

**If image (screenshot):**
1. Download if only URL exists
2. Send to Gemini with prompt:

```
This is a screenshot from a Claude Code tip tweet.
Extract:
- Any visible command text or code
- Settings or configuration shown
- Key information displayed

Return JSON:
{
  "extracted_text": "literal text visible",
  "content_type": "code|settings|terminal|ui|other",
  "summary": "what this screenshot shows"
}
```

### Update Database

```sql
-- Add columns for richer media analysis
ALTER TABLE media ADD COLUMN workflow_summary TEXT;
ALTER TABLE media ADD COLUMN commands_shown TEXT;  -- JSON array
ALTER TABLE media ADD COLUMN key_action TEXT;
```

---

## Task 3: Linked Content Fetch & Summarization

For tweets with `card_url` (linked blogs, docs, GitHub repos), fetch and summarize.

### Check What Links Exist

```sql
SELECT t.id, t.card_url, t.card_title, l.summary
FROM tweets t
LEFT JOIN links l ON t.card_url = l.url
WHERE t.card_url IS NOT NULL
ORDER BY t.likes DESC
LIMIT 20;
```

### Create `scripts/enrich_links.py`

For each link not yet summarized:

1. **Fetch content** (use requests or playwright for JS-heavy sites)
2. **Send to Gemini** for summarization:

```
Summarize this linked resource from a Claude Code tip tweet.

URL: {url}
Title: {title}
Content: {first 4000 chars of content}

Return JSON:
{
  "summary": "2-3 sentence summary of what this resource covers",
  "key_points": ["main point 1", "main point 2", "main point 3"],
  "resource_type": "blog-post|github-repo|documentation|video|tool",
  "relevance_to_claude_code": "how this relates to Claude Code usage",
  "commands_or_tools_mentioned": ["any specific commands or tools"]
}
```

### Update Database

```sql
-- Ensure links table has enrichment columns
ALTER TABLE links ADD COLUMN llm_summary TEXT;
ALTER TABLE links ADD COLUMN key_points_json TEXT;
ALTER TABLE links ADD COLUMN resource_type TEXT;
ALTER TABLE links ADD COLUMN relevance TEXT;
ALTER TABLE links ADD COLUMN commands_mentioned TEXT;  -- JSON array
```

---

## Execution Order

```bash
cd ~/Development/claude-code-tips
source ~/Development/Hall\ of\ Fake/venv/bin/activate
export GOOGLE_API_KEY="..."

# 1. Re-run keyword enrichment with refined prompt
python scripts/enrich_keywords.py --limit 10 --force  # --force to overwrite

# 2. Analyze media (videos and screenshots)  
python scripts/enrich_media.py --limit 10

# 3. Fetch and summarize linked content
python scripts/enrich_links.py --limit 10

# 4. Re-export to see results
python scripts/export_tips.py --limit 10

# 5. Verify
sqlite3 data/claude_code_tips_v2.db "SELECT posted_at, primary_keyword, command_or_flag FROM tips ti JOIN tweets t ON ti.tweet_id = t.id WHERE primary_keyword IS NOT NULL LIMIT 10;"
```

---

## Expected Improvements

After this iteration, the 10 samples should have:

| Tweet (by date) | Expected primary_keyword | From |
|-----------------|-------------------------|------|
| 12-26 teleport | `--teleport` or `teleport` | video analysis |
| 12-26 underrated | `underrated-trick` | refined prompt |
| 12-27 sandbox | `--sandbox` | refined prompt |
| 12-28 spec | `AskUserQuestionTool` | refined prompt |
| 12-28 blog | `claude-2-guide` | link fetch |
| 12-30 shortcut | `ccc-alias` | refined prompt |
| 12-31 agent-sdk | `agent-sdk` | refined prompt |
| etc. | | |

---

## Reply Attributions Note

The "unknown" reply authors are a DATA GAP from original scrape — `thread_replies.reply_author_handle` is literally "unknown" for all 60 records. This requires re-scraping, not an export fix. Defer to later.

---

*Handoff created: 2026-01-04*
