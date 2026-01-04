# HANDOFF: Quick Fixes - OCR Rendering, Media Folders, Dashboard Metrics

**Created:** 2026-01-04
**Purpose:** Fix three small bugs from enrichment v3
**Priority:** Quick fixes, should take < 10 minutes

---

## Bug 1: Full OCR Text Not Rendering as Code

**Problem:** Markdown backticks inside `<details>` tags don't render in Obsidian.

**File:** `scripts/obsidian_export/templates/tweet.md.j2`

**Fix:** Replace backticks with HTML `<pre>` tags:

```jinja
{% if m.full_ocr %}
<details>
<summary>Full OCR Text</summary>
<pre>
{{ m.full_ocr }}
</pre>
</details>
{% endif %}
```

---

## Bug 2: Videos Saved to Wrong Folder

**Problem:** `.mp4` files are being saved to `attachments/screenshots/` instead of `attachments/videos/`.

**File:** `scripts/download_media.py`

**Fix:** Route by file extension:

```python
# When determining destination path:
if media_type == 'video' or url.endswith('.mp4'):
    dest_dir = output_dir / 'attachments' / 'videos'
else:
    dest_dir = output_dir / 'attachments' / 'screenshots'
```

Also update the template to reference the correct folder for videos:

```jinja
{% if m.media_type == 'video' or m.local_path.endswith('.mp4') %}
![[attachments/videos/{{ m.local_path | basename }}]]
{% else %}
![[attachments/screenshots/{{ m.local_path | basename }}]]
{% endif %}
```

---

## Bug 3: Dashboard Shows All Zeros

**Problem:** Metrics were removed from frontmatter, but Dataview dashboards need them.

**File:** `scripts/obsidian_export/templates/tweet.md.j2`

**Fix:** Add metrics back to frontmatter (at the end, before `url`):

```yaml
---
created: {{ date }}
author: "{{ tweet.handle }}"
display_name: {{ display_name | tojson }}
{% if tweet.category %}
category: "{{ tweet.category }}"
{% endif %}
{% if tweet.tools_mentioned %}
tools: {{ tweet.tools_mentioned | tojson }}
{% endif %}
tags:
{% for tag in tags %}
  - {{ tag }}
{% endfor %}
likes: {{ tweet.likes }}
views: {{ tweet.views }}
engagement_score: {{ tweet.engagement_score }}
url: "{{ tweet.url }}"
---
```

The metrics will be:
- In frontmatter → Dataview can query them for dashboards
- In tweet card → User sees them inline
- In metrics callout → Full details at bottom

This isn't duplication for the user — frontmatter is "invisible" metadata, the visual display is separate.

---

## Execution

```bash
# 1. Apply all three fixes to templates/scripts
# 2. Re-download media to correct folders (optional - can manually move)
mv vault/attachments/screenshots/*.mp4 vault/attachments/videos/

# 3. Re-export
rm vault/*.md
python scripts/export_tips.py --limit 10

# 4. Verify dashboard shows real numbers
```

---

## Test Checklist

- [ ] Full OCR text renders as monospace in collapsed section
- [ ] `.mp4` files are in `attachments/videos/`
- [ ] `.jpg`/`.png` files are in `attachments/screenshots/`
- [ ] Dashboard shows actual likes/views/scores (not zeros)
- [ ] Video embeds still work in notes

---

*Handoff created: 2026-01-04*
