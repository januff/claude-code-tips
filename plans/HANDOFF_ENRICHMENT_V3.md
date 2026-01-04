# HANDOFF: Enrichment v3 - Refined Media Analysis + Holistic Summaries

**Created:** 2026-01-04
**Purpose:** Improve media analysis structure and generate holistic tweet summaries
**Prerequisites:** Enrichment v2 complete (keywords + basic media analysis done)

---

## Context

Current media analysis is good but needs structural improvements:
- Summary mixes description with pasteable text (should be separate)
- Missing verbatim OCR for code/prompts/commands
- Tweet-level summary is just first sentence (should synthesize all content)

---

## Task 1: Refined Media Analysis Prompt

### Update `scripts/enrich_media.py`

Replace the analysis prompt with this structured version:

**For screenshots:**
```python
SCREENSHOT_PROMPT = """Analyze this screenshot from a Claude Code tutorial tweet.

Extract the following in JSON format:

{
  "summary": "One sentence: what IS this screenshot showing (UI element, settings page, terminal, etc.)",
  
  "focus_text": "The main command, prompt, or code being demonstrated. Extract VERBATIM - do not summarize. If it's a multi-line prompt or code block, preserve all lines exactly. If no specific focus text, use null.",
  
  "full_ocr": "ALL visible text in the screenshot, extracted verbatim. Preserve structure (newlines, bullets, etc.) as much as possible. This should be copy-pasteable.",
  
  "ui_context": "What part of the UI is shown (e.g., 'Claude.ai style settings', 'VS Code terminal', 'Claude Code CLI')",
  
  "workflow": "What process or action is being demonstrated",
  
  "key_action": "The main takeaway - what should the user learn to DO from this",
  
  "commands_shown": ["any", "CLI", "commands", "visible"]
}

CRITICAL: 
- focus_text must be VERBATIM, not summarized
- full_ocr must capture ALL text, not a selection
- Do not skip any visible text in prompts, code blocks, or instructions
"""
```

**For videos:**
```python
VIDEO_PROMPT = """Analyze this screen recording from a Claude Code tutorial tweet.

Extract the following in JSON format:

{
  "summary": "One sentence: what does this video demonstrate",
  
  "focus_text": "If there's a specific command or prompt being typed/shown, extract it VERBATIM. Otherwise null.",
  
  "workflow": "Step-by-step what happens in the video (First... Then... Finally...)",
  
  "key_action": "The main takeaway - what should the user learn to DO from this",
  
  "commands_shown": ["actual", "commands", "typed", "or", "executed"],
  
  "ui_elements": ["buttons", "menus", "or", "UI", "elements", "interacted", "with"]
}
"""
```

### New Database Columns

```sql
ALTER TABLE media ADD COLUMN focus_text TEXT;
ALTER TABLE media ADD COLUMN full_ocr TEXT;
ALTER TABLE media ADD COLUMN ui_context TEXT;
```

### Update Models and Export

**models.py Media class:**
```python
focus_text: Optional[str] = None
full_ocr: Optional[str] = None
ui_context: Optional[str] = None
```

**tweet.md.j2 Media section:**
```jinja
{% for m in tweet.media %}
{% if m.local_path %}
![[attachments/screenshots/{{ m.local_path | basename }}]]
{% else %}
![Media]({{ m.url }})
{% endif %}

{% if m.summary %}
{{ m.summary }}
{% endif %}

{% if m.focus_text %}
**Focus Text:**
```
{{ m.focus_text }}
```
{% endif %}

{% if m.workflow %}
**Workflow:** {{ m.workflow }}
{% endif %}

{% if m.key_action %}
**Key Action:** {{ m.key_action }}
{% endif %}

{% if m.commands_shown %}
**Commands:** {{ m.commands_shown | join(', ') }}
{% endif %}

{% if m.full_ocr %}
<details>
<summary>Full OCR Text</summary>

```
{{ m.full_ocr }}
```
</details>
{% endif %}

{% endfor %}
```

---

## Task 2: Holistic Tweet Summary Generation

After media analysis, generate a proper tweet summary that synthesizes ALL content.

### Create `scripts/enrich_summaries.py`

For each tweet, gather:
- Tweet text
- Media analysis (workflow, key_action, focus_text)
- Linked content summary (if available)
- Reply highlights (if valuable)

**Prompt:**
```python
SUMMARY_PROMPT = """Generate a holistic summary for this Claude Code tip.

TWEET TEXT:
{tweet_text}

MEDIA ANALYSIS:
{media_summaries}

LINKED CONTENT:
{link_summary}

Write a 2-4 sentence summary that:
1. States what the tip is about (technique, command, workflow)
2. Explains the key insight or action demonstrated
3. Mentions any specific commands, tools, or settings shown
4. Is useful for someone scanning to understand the value

Do NOT just repeat the tweet text. Synthesize across tweet + media + links.

Return JSON:
{{
  "summary": "Your 2-4 sentence holistic summary",
  "one_liner": "A single sentence version for quick scanning"
}}
"""
```

### Update Database

```sql
ALTER TABLE tips ADD COLUMN holistic_summary TEXT;
ALTER TABLE tips ADD COLUMN one_liner TEXT;
```

### Execution Order

```bash
# 1. Re-run media analysis with refined prompts
python scripts/enrich_media.py --limit 10 --force

# 2. Generate holistic summaries (AFTER media analysis)
python scripts/enrich_summaries.py --limit 10

# 3. Re-export
rm vault/*.md
python scripts/export_tips.py --limit 10
```

---

## Task 3: Update Export Template

The Summary section should use `holistic_summary` instead of the old regex-based summary:

**tweet.md.j2:**
```jinja
{% if tweet.holistic_summary %}
## Summary

{{ tweet.holistic_summary }}

{% elif tweet.summary %}
## Summary

{{ tweet.summary }}

{% endif %}
```

---

## Expected Output Structure

After these changes, a note should look like:

```markdown
## Summary

Demonstrates the `--teleport` command for transferring a Claude Code session from 
the web interface to a local CLI. The video shows clicking "Open in CLI" which 
copies a teleport command, then pasting it in a terminal to resume the session 
with full context. Useful for moving from browser-based exploration to local 
development.

## Media

![video thumbnail]

Video thumbnail - teleport command demo

**Focus Text:**
```
claude --teleport ts_abc123def456
```

**Workflow:** First clicks "Open in CLI" button in Claude Code web interface, 
copies the generated command, opens terminal, pastes command to resume session.

**Key Action:** Transferring web session to local CLI

**Commands:** --teleport session_id, claude --resume

<details>
<summary>Full OCR Text</summary>
...
</details>
```

---

## Test Checklist

- [ ] Screenshots have `focus_text` with VERBATIM prompt/code (not summarized)
- [ ] Screenshots have `full_ocr` with ALL visible text
- [ ] Focus text renders in code block (pasteable)
- [ ] Full OCR in collapsible `<details>` section
- [ ] Holistic summary synthesizes tweet + media + links
- [ ] Summary is actually useful (not just first sentence)

---

*Handoff created: 2026-01-04*
