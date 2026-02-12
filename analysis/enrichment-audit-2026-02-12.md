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

1. **8 unenriched tweets** — RESOLVED: created tips rows, ran all enrichment scripts
2. **52 links without summaries** (57%) → PARTIALLY RESOLVED: ran enrich_links.py (8 more summarized, now 47/91)
3. **17 media without vision analysis** (59%) → PARTIALLY RESOLVED: ran enrich_media.py (2 more, now 12/29 — only 12 have local_path)
4. **0 OCR results** → OCR has never been run (enrich_media.py populates workflow_summary, not ocr_text)
5. **4 empty-text tweets** — genuinely attachment-only, not a parsing bug
6. **Quote tweets** — not captured in schema (see analysis below)

## Post-Enrichment Coverage (after gap-fill)

| Metric | Before | After | Coverage |
|--------|--------|-------|----------|
| Holistic summaries | 460 | 468 | **100%** |
| Primary keywords | 458 | 466 | **99.6%** (2 empty-text can't be enriched) |
| Links with summaries | 39 | 47 | **51.6%** |
| Media with analysis | 10 | 12 | **41.4%** (limited by local_path availability) |

---

## Quote Tweet & Reply Coverage Analysis (Task 7)

### Quote Tweets

**Status: NOT captured.**

- The `tweets` table has a `quotes` INTEGER column (count of quote tweets), extracted from `legacy.quote_count` in the GraphQL response
- The actual quoted tweet content (`quoted_status_result`) is NOT extracted by the bookmark extractor
- No separate table exists for quote tweet relationships
- The bookmark extractor at line 178 only extracts `quotes: legacy.quote_count || 0` — the count, not the content
- The thread extractor similarly only extracts the count at line 116

**To add quote tweet capture (future work):**
1. Add a `quoted_tweets` table: `(tweet_id, quoted_tweet_id, quoted_text, quoted_author, quoted_likes)`
2. Update `parseTweet()` in `bookmark_folder_extractor.js` to extract `quoted_status_result`
3. Update the import flow to insert quoted tweet data

### Reply Coverage for Bookmarked Tweets

- **27 bookmarked tweets** (5.8%) are replies to other tweets
- All 27 have `in_reply_to_id` populated
- Parent tweets for these replies may or may not be in the DB (the referenced tweets are often from authors we don't track)

### Thread Reply Scraping

- **115 tweets** (24.6%) have scraped reply threads via `thread_replies` table
- **2,730 total thread replies** stored
- **614 author replies** (22.5% of all replies) — high-signal content
- The `twitter_thread_extractor.js` uses GraphQL API to fetch replies
- The `browser_fetch_comments.js` has nested reply parsing (depth 2)

### Gaps to Address (future handoff)

1. Add `quoted_status_result` extraction to bookmark extractor
2. Consider a `--fetch-parents` option for reply tweets to pull in the parent tweet
3. The 353 tweets (75.4%) without scraped replies could benefit from thread scraping — prioritize by engagement
