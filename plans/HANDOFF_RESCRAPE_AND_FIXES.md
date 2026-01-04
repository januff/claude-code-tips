# HANDOFF: Re-scrape Requirements + Reply/Media Fixes

**Created:** 2026-01-04
**Purpose:** Document re-scrape requirements and apply quick template fixes
**Priority:** Re-scrape is HIGH priority — current data has significant gaps

---

## Part A: Re-scrape Requirements (HIGH PRIORITY)

### Problem 1: Missing Reply Author Handles

All 60 replies in `thread_replies` have `reply_author_handle = 'unknown'`. This breaks:
- Author attribution in notes
- Detection of self-replies (author replying to themselves)
- Future Obsidian linking like `[[@EricBuess]]`

**Requirement:** Re-scrape must capture `reply_author_handle` for every reply.

---

### Problem 2: Self-Replies Are Part of Main Content

When the original tweet author replies to themselves, those replies are **canonical additions to the main text**, not separate commentary.

**Example:** Eric Buess (@EricBuess) on 2025-12-30 Ralph Wiggum loops:
- Original tweet: "LSP + hooks + subagents + adversarial validations + Ralph Wiggum loops..."
- Self-reply 1: "Not to mention self-referential command injection, context monitoring, auto restore from clear, compaction-avoidance..."
- Self-reply 2: "I should probably do a podcast or video at some point... Coding via CarPlay with a project manager agent... voice loop or vibe loop... voicecoding.ai... theeverythingagent.ai..."

Currently:
- Self-reply 1 is in database but ABRIDGED
- Self-reply 2 is MISSING entirely

**Requirements:**
1. Detect when `reply_author_handle == original_tweet_author`
2. Mark these as `is_author_continuation = True`
3. Capture FULL TEXT (not abridged)
4. In export: Append author self-replies to main tweet text (not in Replies section)

**Template change:**
```jinja
> [!tweet] {{ tweet.handle }} · {{ date_display }}
> {{ tweet.text | replace('\n', '\n> ') }}
{% for reply in tweet.replies_list if reply.is_author_reply %}
>
> ---
> *Thread continuation ({{ reply.reply_posted_at }}):*
> {{ reply.reply_text | replace('\n', '\n> ') }}
{% endfor %}
>
> Likes: {{ tweet.likes | format_number }} · Replies: {{ tweet.replies | format_number }} · Reposts: {{ tweet.reposts | format_number }}
```

---

### Problem 3: External Links in Replies Not Captured

High-quality replies often link to external resources that add significant value.

**Example:** @GeoffreyHuntley reply linking to ghuntley.com explaining "Ralph Wiggum as a software engineer"

**Requirements:**
1. Extract URLs from reply text during scrape
2. Store in `reply_links` table or JSON field
3. Optionally fetch and summarize (like we do for main tweet card_url)
4. In export: Include as linked resources

**Schema addition:**
```sql
ALTER TABLE thread_replies ADD COLUMN extracted_urls TEXT;  -- JSON array
```

---

### Problem 4: Reply Quality Filtering Too Aggressive

Some valuable replies (like author self-replies) may be getting filtered out by quality scoring.

**Requirements:**
1. NEVER filter out author self-replies regardless of "quality" score
2. Review quality scoring logic — educational replies with external links should score higher
3. Store ALL replies, use quality score for display ordering only

---

## Part B: Quick Fixes (Apply Now)

### Fix 1: Simplify Reply Display

Remove redundant "High Quality" labels since we're only showing good replies.

**File:** `scripts/obsidian_export/templates/tweet.md.j2`

**Current:**
```jinja
{% if reply.quality_level == 'high' %}
> [!reply]+ {{ reply.reply_author_handle or 'Unknown' }} · High Quality
{% elif reply.quality_level == 'low' %}
> [!reply]- {{ reply.reply_author_handle or 'Unknown' }}
{% else %}
> [!reply] {{ reply.reply_author_handle or 'Unknown' }}
{% endif %}
```

**Fixed:**
```jinja
> [!reply] {{ reply.reply_author_handle or 'Unknown' }}{% if reply.reply_posted_at %} · {{ reply.reply_posted_at }}{% endif %}

```

No quality labels, no expand/collapse modifiers. Just show the reply.

---

### Fix 2: Semantic Media Filenames

Rename media files to match their parent note's name.

**Pipeline consideration:** Primary keyword enrichment happens AFTER media download. Two options:

**Option A: Rename after enrichment (recommended)**
```python
# In export or as separate script
def rename_media_files(tweet):
    if not tweet.primary_keyword:
        return
    
    date = format_date(tweet.posted_at)
    base_name = f"{date}-{slugify(tweet.primary_keyword)}"
    
    for i, media in enumerate(tweet.media):
        if media.local_path:
            old_path = Path(media.local_path)
            ext = old_path.suffix
            new_name = f"{base_name}_{i+1}{ext}"
            new_path = old_path.parent / new_name
            
            # Rename file
            old_path.rename(new_path)
            
            # Update database
            media.local_path = str(new_path)
```

**Option B: Two-pass download**
1. First pass: Download with temp names
2. After enrichment: Rename to semantic names

**Result:**
- Before: `tweet_2004579780998688823_1.mp4`
- After: `2025-12-26-teleport_1.mp4`

---

## Part C: Re-scrape Execution Plan

When ready to re-scrape:

```bash
# 1. Backup current database
cp data/claude_code_tips_v2.db data/claude_code_tips_v2_backup.db

# 2. Update scraping script with new requirements:
#    - Full reply author handles
#    - Full reply text (not abridged)
#    - Author self-reply detection
#    - URL extraction from replies

# 3. Re-scrape threads for existing tweets
python scripts/scrape_threads.py --update-replies

# 4. Re-run enrichment pipeline
python scripts/enrich_keywords.py --force
python scripts/enrich_media.py --force
python scripts/enrich_summaries.py --force

# 5. Rename media files
python scripts/rename_media.py

# 6. Re-export
rm -rf vault/*.md
python scripts/export_tips.py
```

---

## Test Checklist (After Re-scrape)

- [ ] Reply authors are real handles (not "unknown")
- [ ] Author self-replies appear as thread continuations in main tweet card
- [ ] Author self-replies are COMPLETE (not abridged)
- [ ] Eric Buess 12-30 tweet shows both self-reply continuations
- [ ] External links from replies are captured
- [ ] Media files named semantically (date-keyword_n.ext)
- [ ] Reply display is simplified (no quality labels)

---

## Data Quality Notes

The current scrape has these known gaps:
- Reply author handles: ALL missing
- Self-reply handling: Not distinguished
- Reply text: Some abridged
- Reply links: Not extracted
- Some self-replies: Completely missing

A proper re-scrape will significantly improve data quality before scaling to the full 380 tweets.

---

*Handoff created: 2026-01-04*
