# HANDOFF: Export Template Fixes

**Created:** 2026-01-03
**Purpose:** Fix bugs and polish identified during Obsidian review
**Test with:** `python scripts/export_tips.py --limit 10`

---

## Bug 1: Unknown Reply Authors

**Problem:** All replies show "Unknown" as author instead of actual handle.

**Location:** `scripts/obsidian_export/templates/tweet.md.j2`

**Current:**
```jinja
> [!reply]+ {{ reply.reply_author_handle or 'Unknown' }}
```

**Investigation needed:**
1. Check `thread_replies` table schema — what's the actual column name?
2. Check `models.py` — is the Reply dataclass mapping the field correctly?
3. Check `core.py` — is the query joining/fetching reply author data?

**Verify fix:**
```sql
SELECT reply_author_handle FROM thread_replies LIMIT 5;
```

---

## Bug 2: Missing Attachments

**Problem:** Notes reference `![[attachments/screenshots/...]]` but the files don't exist in `vault/attachments/`.

**Cause:** Export script generates paths but doesn't copy/symlink the actual media files.

**Fix in `core.py`:**
1. After creating vault structure, copy media files:
   - Screenshots from wherever they're stored → `vault/attachments/screenshots/`
   - For HoF: thumbnails → `vault/attachments/thumbnails/`, videos → `vault/attachments/videos/`

2. Or create symlinks to avoid duplication:
   ```python
   # Symlink approach (saves disk space)
   (vault_dir / "attachments" / "thumbnails").symlink_to(thumbnails_dir)
   ```

**Note:** Check where tips media files actually live — may be in `data/` or external URLs only.

---

## Bug 3: Number Formatting (Commas)

**Problem:** Large numbers like `72244` should display as `72,244` for readability.

**Fix in `utils.py`:**
```python
def format_number(n: int) -> str:
    """Format number with comma separators."""
    if n is None:
        return "0"
    return f"{n:,}"
```

**Update templates to use filter:**

In `tweet.md.j2` frontmatter — keep raw numbers for Dataview queries:
```yaml
likes: {{ tweet.likes }}
views: {{ tweet.views }}
```

In display text — use formatted numbers:
```jinja
> Likes: {{ tweet.likes | format_number }} · Views: {{ tweet.views | format_number }}
```

**Also update dashboards** in `dashboard_engagement.md.j2` etc.

---

## Enhancement: Property Order

**Requested order** (from user's manual arrangement):

```yaml
created
author
display_name
category
tools
tags
likes
replies
reposts
views
engagement_score
source
is_reply
is_curated
quality_rating
id
url
```

**Update `tweet.md.j2`** to output frontmatter in this exact order.

**Grouping logic:**
1. **Identity:** created, author, display_name
2. **Classification:** category, tools, tags
3. **Metrics:** likes, replies, reposts, views, engagement_score
4. **Metadata:** source, is_reply, is_curated, quality_rating
5. **Reference:** id, url

---

## Enhancement: Better Filenames (DEFERRED)

**Current:** `2025-12-26-full-tweet-text-kebabbed.md`
**Desired:** `2025-12-26-teleport.md` (1-2 keyword topic)

This requires LLM analysis to extract topic keywords. **Bookmark for later enrichment pass** — would add a `topic_keyword` column to tips table.

For now, keep current behavior.

---

## Test Checklist

After fixes, run `python scripts/export_tips.py --limit 10` and verify:

- [ ] Reply authors show actual handles (not "Unknown")
- [ ] Attachments folder has actual files (or working symlinks)
- [ ] Numbers in note body have commas (72,244 not 72244)
- [ ] Frontmatter numbers stay raw (for Dataview)
- [ ] Properties appear in requested order
- [ ] Dashboards show formatted numbers

---

## Future Enrichment Tasks (Bookmarked)

1. **Topic keywords for filenames** — LLM extracts 1-2 word topic
2. **Better summaries** — LLM writes actual useful summary
3. **Quality explanations** — LLM explains why rating is high/low
4. **Video workflow descriptions** — Gemini analyzes instructional videos in media

These require separate LLM enrichment passes and are not in scope for this fix.

---

*Handoff created: 2026-01-03*
