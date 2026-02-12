# Task Plan: Obsidian Enrichment Audit + Export Upgrade

> Created: 2026-02-12
> Status: IN PROGRESS
> Source: plans/active/HANDOFF_obsidian-enrichment-audit.md

## Goal

Audit enrichment coverage across all 468 tweets, fix gaps, and upgrade the Obsidian export
to serve as a diagnostic viewer for enrichment quality — showing what was attempted, what
succeeded, and what's missing for every note.

## Success Criteria

- [ ] Enrichment audit written to `analysis/enrichment-audit-2026-02-12.md` with coverage stats
- [ ] Empty-text tweets diagnosed and resolved (or documented if unfixable)
- [ ] Enrichment gaps filled (keywords, summaries, links, media where feasible)
- [ ] Obsidian export upgraded with enrichment sections, thread context, diagnostic footer
- [ ] Full vault re-export run with new format verified
- [ ] Obsidian CLI tested and findings documented
- [ ] Quote tweet/reply coverage assessed and documented
- [ ] Author index generated with team member identification
- [ ] All commits pushed to remote

## Steps

### Phase 1: Audit & Diagnosis (Tasks 1-2)
- [ ] Run enrichment coverage queries against DB (adapt column names to actual schema)
- [ ] Investigate empty-text tweets — check raw JSON and parser
- [ ] Write audit findings to `analysis/enrichment-audit-2026-02-12.md`
- [ ] Commit audit results

### Phase 2: Gap Fill (Task 3)
- [ ] Run `enrich_keywords.py` for tweets missing primary_keyword
- [ ] Run `enrich_summaries.py` for tweets missing holistic_summary
- [ ] Run `enrich_links.py` for links missing llm_summary
- [ ] Evaluate `enrich_media.py` — check coverage and quality
- [ ] Verify 8 newest tweets have full enrichment
- [ ] Commit enrichment results

### Phase 3: Export Upgrade (Tasks 4-5)
- [ ] Read current export code (`scripts/export_tips.py`, `scripts/obsidian_export/`)
- [ ] Add enrichment sections: Summary, Keywords, Classification
- [ ] Add Linked Resources section with resolved URLs and summaries
- [ ] Add Media section with embedded images and vision analysis
- [ ] Add Thread Context section (parent tweet, top replies)
- [ ] Add enrichment status diagnostic footer
- [ ] Add frontmatter fields (enrichment_complete, has_media, has_links, classification)
- [ ] Run full export and verify results
- [ ] Commit export upgrade + re-exported vault

### Phase 4: Analysis & Wrap-up (Tasks 6-8)
- [ ] Test Obsidian CLI capabilities and document findings
- [ ] Assess quote tweet and reply coverage gaps
- [ ] Generate author index with engagement metrics and team identification
- [ ] Commit analysis outputs

### Phase 5: Wrap Up (Task 9)
- [ ] Final commit and git push
- [ ] Update STATUS.json

## Known Risks

- Schema column names differ from handoff assumptions (already mapped — tips table has enrichment, not tweets table)
- Enrichment scripts may require API keys (Gemini, etc.) — may not be runnable
- Media vision analysis may be expensive or slow — assess before batch-running
- Obsidian CLI may not exist at the installed version
- Large export changes risk regressions in existing Dataview dashboards

## Column Mapping (handoff → actual)

| Handoff assumes | Actual column | Table |
|-----------------|---------------|-------|
| holistic_summary | holistic_summary | tips |
| primary_keyword | primary_keyword | tips |
| full_text | text | tweets |
| author_handle | handle | tweets |
| author_name | display_name | tweets |
| resolved_url | expanded_url | links |
| content_summary | llm_summary | links |
| fetched_content | raw_content | links |
| vision_analysis | vision_description | media |
| local_path | local_path | media |

## Progress Log

| Step | Status | Notes |
|------|--------|-------|
| | | |

## Completion

When all success criteria are met:
1. Update status to COMPLETE
2. Move this file: `plans/active/TASK_PLAN.md` -> `plans/archive/2026-02-12-obsidian-enrichment-audit.md`
3. Remove `active_task` from STATUS.json
