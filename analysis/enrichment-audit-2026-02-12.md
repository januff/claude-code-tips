# Enrichment Depth Audit — 2026-02-12

> Auditor: Claude Code (Opus 4.6)
> Database: data/claude_code_tips_v2.db (468 tweets)

## Overall Coverage

| Metric | Count | Coverage |
|--------|-------|----------|
| Total tweets | 468 | — |
| Has tips row (enrichment target) | 460 | 98.3% |
| Has holistic_summary | 460 | 98.3% |
| Has primary_keyword | 458 | 97.9% |
| Has llm_category | 456 | 97.4% |
| Has one_liner | 456 | 97.4% |
| Empty text | 4 | 0.9% |

**Tweets missing tips row entirely (8):** All recent imports (Feb 5-11), all high-engagement. These need enrichment.

| Tweet ID | Handle | Likes | Text Length | Posted |
|----------|--------|-------|-------------|--------|
| 2019469032844587505 | lydiahallie | 5,022 | 323 | Feb 5 |
| 2021699851499798911 | bcherny | 2,061 | 557 | Feb 11 |
| 2021517624803573928 | sharbel | 1,642 | 302 | Feb 11 |
| 2021012074160324633 | lydiahallie | 1,334 | 317 | Feb 10 |
| 2021266983086588238 | firecrawl | 974 | 258 | Feb 10 |
| 2021632916359655893 | trq212 | 631 | 200 | Feb 11 |
| 2021718924430389424 | lydiahallie | 606 | 199 | Feb 11 |
| 2021650827233169662 | _catwu | 385 | 250 | Feb 11 |

These are from key Anthropic team members — high priority for enrichment.

## Link Enrichment

| Metric | Count | Coverage |
|--------|-------|----------|
| Total links | 91 | — |
| Resolved (expanded_url) | 91 | 100% |
| Has llm_summary | 39 | 42.9% |
| Has raw_content (fetched) | 0 | 0% |
| Has resource_type | 15 | 16.5% |

**Gap:** 52 links (57.1%) have no LLM summary. Raw content was never fetched (0%).

## Media Enrichment

| Metric | Count | Coverage |
|--------|-------|----------|
| Total media items | 29 | — |
| Photos | 26 | — |
| Videos | 3 | — |
| Downloaded (local_path) | 12 | 41.4% |
| Vision analyzed | 12 | 41.4% |
| OCR text | 0 | 0% |
| Workflow summary | 10 | 34.5% |

**Gap:** 17 media items (58.6%) have no vision analysis. OCR has never been run (0%).

## Thread Context

| Metric | Count |
|--------|-------|
| Total tweets | 468 |
| Are replies | 27 (5.8%) |
| Have parent reference | 27 |
| In a thread (conversation_id != id) | 27 |
| Thread replies in DB | 2,730 |
| Tweets with scraped replies | 115 (24.6%) |
| Author replies in threads | 614 |

**Thread coverage is decent** — 115 tweets have scraped reply threads, with 2,730 total replies.

## Empty-Text Tweets (4)

All 4 are from `thread_extraction` source — replies scraped from the @alexalbert__ "underrated Claude Code trick" thread.

| Tweet ID | Handle | Likes | Analysis |
|----------|--------|-------|----------|
| 2004647680354746734 | @mutewinter | 20 | Reply text: "@alexalbert__ [t.co link]" — link/screenshot only |
| 2005213914444026211 | @keshavrao_ | 2 | Reply text: "@alexalbert__ [t.co link]" — link/screenshot only |
| 2004596323652407535 | @martingoerler | 0 | No thread_reply entry, no media, no links |
| 2004614088492712417 | @JuanCS_Dev | 0 | No thread_reply entry, no media, no links |

**Diagnosis:** These are genuinely text-light replies — users who replied with only a screenshot or link, no textual content. The scraper correctly captured the empty text. The @mutewinter reply (20 likes) likely had a screenshot that wasn't captured as media.

**Recommendation:**
- @mutewinter: Worth re-fetching — 20 likes suggests valuable content (likely a screenshot)
- Other 3: Low engagement, can be deprioritized
- Consider marking these as `attachment_only` in the DB for export handling

## Summary of Gaps

1. **8 unenriched tweets** — recent high-engagement imports, no tips row → run enrichment scripts
2. **52 links without summaries** (57%) → run `enrich_links.py`
3. **17 media without vision analysis** (59%) → run `enrich_media.py`
4. **0 OCR results** → OCR has never been run
5. **4 empty-text tweets** — genuinely attachment-only, not a parsing bug
6. **Quote tweets** — not captured in schema (see separate analysis below)
