# Cross-Project Handoff: Hall of Fake Audit

**Date:** January 5, 2026  
**From:** claude-code-tips session  
**To:** Hall of Fake new instance  

---

## Context

I just wrapped a productive session on `claude-code-tips` where we built out a complete enrichment pipeline for Twitter bookmarks. Before expanding to other platforms, we need to audit Hall of Fake to see:

1. What's the current data state?
2. Should we apply the same patterns (Obsidian export, quality filter, link enrichment)?
3. What's working vs. what needs attention?

---

## Patterns Established in claude-code-tips

### 1. Quality-Filtered Export
Only export content that's been fully processed:
```python
WHERE likes > 0 OR holistic_summary IS NOT NULL
```
This keeps the vault browsable — no empty placeholders.

### 2. Semantic Filenames
LLM-generated `primary_keyword` for human-readable filenames:
- Bad: `2025-12-26-2004647680354746734.md`
- Good: `2025-12-26-openrouter-integration.md`

### 3. Link Enrichment (ContentUnit)
1. Extract URLs from text
2. Resolve shortlinks (t.co → real URL)
3. Fetch and LLM-summarize external content
4. Surface summaries in exports

### 4. Attachment-Only Content
Tweets/videos with just a link or screenshot are high-signal, not edge cases:
- Run vision analysis on screenshots
- Fetch and summarize linked content
- Generate keywords from extracted content

### 5. What's New Reporting
`scripts/whats_new.py` generates markdown report of recent additions.

---

## Questions for Hall of Fake Audit

1. **Data freshness:** When was the last Sora likes refresh? How many new videos since?

2. **Enrichment coverage:** What % have:
   - Whisper transcription?
   - Gemini visual analysis?
   - Full metadata?

3. **Obsidian export:** Does one exist? Should we create one?
   - Would follow same quality-filtered pattern
   - Semantic filenames from `primary_subject` or `discovery_phrase`

4. **CapCut Forge status:** Last I knew, clone-based approach was working. Any updates needed?

5. **Legal considerations:** NY AI publicity law — any new developments?

---

## Techniques to Consider Applying

| From claude-code-tips | Hall of Fake Equivalent |
|----------------------|------------------------|
| `primary_keyword` | `primary_subject` or `discovery_phrase` |
| Thread replies | Comments (already captured?) |
| Link summaries | N/A (videos are primary content) |
| Quality filter | `likes > X` AND `has_analysis` |
| Obsidian vault | New — create `vault/` folder? |

---

## Cold-Start for Tomorrow

```
I'm continuing work on Hall of Fake, my Sora video archive project.

Read CLAUDE.md and PROJECT_DECISIONS.md from Project Knowledge for context.

CURRENT FOCUS: Audit data state and consider applying patterns from claude-code-tips:
- Quality-filtered Obsidian export
- Semantic filenames
- What's New reporting

Questions to answer:
1. How many videos? What % fully analyzed?
2. When was last likes refresh?
3. Should we create an Obsidian vault export?

Start by querying the database for current stats.
```

---

## Links

- Hall of Fake repo: https://github.com/januff/hall-of-fake
- claude-code-tips repo: https://github.com/januff/claude-code-tips
- Related: `docs/PROJECT_DECISIONS.md` in both repos

---

*Created: January 5, 2026*
