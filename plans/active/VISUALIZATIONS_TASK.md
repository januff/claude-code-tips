# Task Plan: README Data Visualizations

> Created: 2026-03-22
> Status: IN PROGRESS

## Goal

Generate a variety of data visualizations from the claude-code-tips database for potential inclusion in the README and COMMUNITY_MAP.md. Produce multiple options across different chart types and rendering approaches so Joey and the senior instance can review and select the best ones. This is also an opportunity to dogfood community-recommended visualization techniques from our own tip database.

## Context from Senior Instance

The database contains 562 tweets: 206 bookmarked tips (all with likes > 0) and 356 thread replies (288 with zero likes). The data supports at least three strong visualizations:

1. **Category distribution** — 13 LLM-classified categories, dominated by Tooling (147) and Prompting (91)
2. **Engagement curve** — power law distribution: 288 tweets at 0 likes, 9 at 10K+
3. **Timeline** — tweet volume and engagement by month (Dec 2025 explosion, steady through Mar 2026)
4. **Tips-to-tool pipeline** — timeline showing community hack → native feature with ~4-week velocity
5. **Community map** — team vs community engagement, top contributors

## Relevant Community Tips

From our own database, these techniques are worth trying:

- **Nico Bailon's "Visual Explainer"** (5,311 likes) — agent skill rendering concepts as rich HTML pages with CSS pattern library
- **Excalidraw + MCP** (1,170 likes) — diagram generation from prompts
- **Paul Bakaus's live-prototype in Chrome** (260 likes) — Claude generates HTML/CSS, preview directly
- **Mermaid diagrams** — GitHub renders these natively in markdown

## Success Criteria

- [ ] At least 5 different visualizations generated covering different data stories
- [ ] At least 2 different rendering approaches tried (e.g., SVG, Mermaid, HTML screenshot, matplotlib PNG)
- [ ] Each visualization saved to `assets/visualizations/` with a descriptive filename
- [ ] A summary file listing all generated visualizations with notes on which might work best in README vs COMMUNITY_MAP
- [ ] At least one visualization uses a community-recommended technique from the database

## Steps

### Phase 1: Data Extraction
- [ ] Query the database for all visualization-ready datasets:
  - Category counts (from tips table, llm_category)
  - Engagement distribution buckets
  - Monthly tweet volume + total likes
  - Team member stats (deduped handles — use `LOWER(REPLACE(handle, '@', ''))`)
  - Tips-to-tool pipeline dates (from COMMUNITY_MAP.md)
  - Bookmark vs thread reply split
- [ ] Save extracted data as JSON or CSV in `assets/visualizations/data/` for reproducibility

### Phase 2: Generate Visualizations

Try each of these, saving outputs to `assets/visualizations/`:

**Chart 1: Category Treemap or Bar Chart**
- Show the 13 tip categories sized by count
- Try: matplotlib/seaborn bar chart, SVG, and Mermaid pie chart
- Filename pattern: `category-distribution-{method}.{ext}`

**Chart 2: Engagement Power Law**
- Log-scale histogram showing the distribution from 0 to 45K likes
- Annotate the bookmarked (206) vs thread reply (356) split
- Try: matplotlib with log scale, pure SVG

**Chart 3: Timeline — Monthly Volume**
- Bar or area chart: tweets per month, Dec 2025 through Mar 2026
- Overlay: total engagement per month
- Note: some `posted_at` values have malformed dates (e.g., "Thu Jan") — filter to YYYY-MM format only

**Chart 4: Tips-to-Tool Pipeline**
- Horizontal timeline/Gantt showing community hack → native feature
- 5 documented cases: Memory, Worktrees, Ralph Wiggum, Skills, Design fluency
- Try: Mermaid gantt, SVG timeline, HTML

**Chart 5: Team vs Community**
- Bubble chart or grouped bar: 8 team members vs top 10 community voices
- Size = total likes, color = team vs community
- Shows how much signal comes from 8 people vs 463 others

**Chart 6: The Unreviewed Replies**
- Simple visual showing the 288 zero-like thread replies as a distinct mass
- Purpose: make the "hidden gems" review pass feel concrete and worth doing

### Phase 3: Summary & Review Prep
- [ ] Create `assets/visualizations/REVIEW.md` listing all generated visualizations
- [ ] For each: thumbnail description, rendering method used, recommended placement (README vs COMMUNITY_MAP vs neither), and any issues
- [ ] Note which community technique was used and how it worked

## Known Risks

- **GitHub SVG rendering quirks** — not all SVG features render correctly in GitHub markdown. Test by viewing raw file on GitHub after pushing.
- **Mermaid support** — GitHub renders Mermaid in markdown code blocks, but complex charts may not look great. Simple is better.
- **matplotlib requires Python deps** — should be fine since we already have Python in the environment, but check that matplotlib/seaborn are installed.
- **Malformed dates** — some `posted_at` values aren't ISO format. Filter to `WHERE posted_at LIKE '202%'` to be safe.
- **Handle dedup** — 15 authors have variant handles. Always use `LOWER(REPLACE(handle, '@', ''))` for any author-level aggregation.

## Progress Log

| Step | Status | Notes |
|------|--------|-------|
| Task plan created | Done | 2026-03-22 |
| | | |

## Completion

When all success criteria are met:
1. Update status to COMPLETE
2. Move this file: `plans/active/VISUALIZATIONS_TASK.md` -> `plans/archive/2026-03-22-visualizations.md`
3. Remove or update `active_task` in STATUS.json
