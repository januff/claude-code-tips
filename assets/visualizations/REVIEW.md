# Visualization Review

> Generated: 2026-03-22
> Method: matplotlib/seaborn via Python venv
> Data source: claude_code_tips_v2.db (all queries use deduped handles)

## Generated Visualizations

### 1. category-distribution-bar.png (52KB)
**Horizontal bar chart** of 13 LLM-classified tip categories. Tooling dominates (147), followed by Prompting (91) and Meta (74). Coral accent for categories with 50+ tips, slate blue for the rest.

- **Recommended placement:** README (compact, immediately informative)
- **Notes:** Clean and readable. Count labels on bars. Could replace the text-only category table in the README.

### 2. engagement-power-law.png (62KB)
**Grouped histogram** showing likes distribution with bookmark/reply split. Log-spaced bins from 0 to 10K+. Annotates the 288 zero-like thread reply mass.

- **Recommended placement:** COMMUNITY_MAP.md or a dedicated analysis page
- **Notes:** The central story — 288 unreviewed replies as a gray mass vs. curated green bookmarks — comes through clearly. The "Curated Signal vs. Harvested Context" subtitle captures the distinction well.

### 3. timeline-monthly.png (82KB)
**Dual-axis bar + line chart.** Bars show tweet volume by month (bookmark vs. reply), line shows total engagement. The Dec 2025 reply spike is annotated.

- **Recommended placement:** README or COMMUNITY_MAP.md
- **Notes:** Tells two stories — the initial thread scrape (Dec) vs. ongoing curation (Jan-Mar), and the engagement growth despite lower volume. March 2026 has the highest engagement despite fewer tweets.

### 4. tips-to-tool-pipeline.png (49KB)
**Horizontal Gantt chart** showing 5 community-hack-to-native-feature timelines. Circle = community discovers, square = feature ships, bar = gap.

- **Recommended placement:** README (this is the signature visualization)
- **Notes:** The strongest chart conceptually. Visually demonstrates the ~6 week hack-to-feature velocity. Design Fluency shows reversed markers because it was parallel evolution (community and team converged independently) — this is actually accurate to the story.
- **Issue:** Design Fluency row has community date (Mar 4) after ship date (Feb 28), making the bar direction reversed. This accurately reflects parallel evolution but may confuse readers. Consider adding an annotation.

### 5. team-vs-community.png (124KB)
**Bubble scatter plot** on log scale. Team members on the left, community on the right, divided by a dashed line. Bubble size = sqrt(likes). Tweet count annotations for high-engagement entries.

- **Recommended placement:** COMMUNITY_MAP.md
- **Notes:** The log scale is necessary (range: 1K to 111K) but makes the gap between Boris/Thariq and everyone else less dramatic than it actually is. The Team/Community label positioning works well.

### 6. unreviewed-replies.png (27KB)
**Waffle chart** showing 562 squares: green = bookmarked tips, gray = reviewed replies, light gray = unreviewed. Legend below.

- **Recommended placement:** Internal use / task planning
- **Notes:** Makes the "hidden gems review pass" feel concrete — that light gray mass is 288 tweets nobody has looked at yet. The visual impact depends on the viewer understanding the waffle metaphor. Less effective as a README chart, more useful as a project planning artifact.

## Rendering Approaches Used

| Chart | Method | Format |
|-------|--------|--------|
| All 6 | matplotlib + seaborn | PNG @ 150 DPI |

Mermaid alternatives were considered but not generated — GitHub renders Mermaid natively in markdown, but the chart types needed (grouped bars, bubble plots, Gantt with custom markers) exceed Mermaid's capabilities. The pipeline chart could work as a Mermaid gantt but would lose the circle/square markers.

## Recommendations for README

**Include these two:**
1. `tips-to-tool-pipeline.png` — the signature chart, tells the repo's core story
2. `category-distribution-bar.png` — quick visual overview of what's in the database

**Maybe include:**
3. `timeline-monthly.png` — shows the project is alive and growing

**Save for COMMUNITY_MAP.md:**
4. `team-vs-community.png`
5. `engagement-power-law.png`

**Internal only:**
6. `unreviewed-replies.png`

## Data Files

All source data saved to `assets/visualizations/data/` as JSON for reproducibility:
- `categories.json` — 13 categories with counts and likes
- `engagement.json` — per-likes-value counts split by bookmark/reply
- `timeline.json` — monthly volume and engagement
- `team_vs_community.json` — top 30 authors deduped with team/community flag
- `bookmark_reply_split.json` — aggregate bookmark vs reply stats
