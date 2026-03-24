# Infographic Generation Prompts

> Data packages are in `assets/visualizations/data/`
> Each prompt below is designed for a specific interface/model

---

## Prompt 1: Claude API → Interactive HTML Infographic

**Target:** Claude Opus 4.6 via API, or a Claude Code session with preview
**Output:** Single self-contained HTML file with embedded CSS/JS
**Goal:** A beautiful, interactive data visualization that demonstrates Claude's own design capabilities

### Prompt:

```
You are creating a single-page interactive infographic for a GitHub repository called "Claude Code Tips" — a curated knowledge base of 206 community tips about Claude Code, tracked over 87 days.

Create a self-contained HTML file (no external dependencies) that presents this data beautifully and interactively. Use modern CSS (grid, flexbox, gradients, animations), vanilla JavaScript for interactivity, and inline SVG for any charts.

Design requirements:
- Dark theme with Anthropic-adjacent aesthetics (warm neutrals, terracotta/coral accents, clean typography)
- Responsive layout that works at desktop and mobile widths
- Smooth scroll sections, not a dashboard — this should feel like a narrative, not a spreadsheet
- Subtle animations on scroll (intersection observer)
- No matplotlib aesthetics. Think data journalism — NYT, The Pudding, or FiveThirtyEight quality

Sections to include:

1. HERO: "Claude Code Tips" with key stats (206 bookmarks, 87 days, 8 team members, 120+ community voices) as animated counters

2. THE PIPELINE: Interactive timeline showing how community hacks become native features in ~4-6 weeks. Show 5 events with expandable detail cards. Data:
[paste pipeline.json]

3. WHAT PEOPLE ARE BUILDING: Category breakdown as an interactive treemap or radial chart (not a bar chart). Clicking a category reveals its top keywords and sample tips. Data:
[paste categories.json]

4. THE VOICES: A network or constellation visualization showing team members (inner ring) and top community contributors (outer ring). Size = number of bookmarked tips, not likes. Hover for details. Data:
[paste community.json]

5. FOUR PRINCIPLES: Minimal cards with icons for each principle. These are project values, not data. Data:
[paste vitals.json → four_principles]

6. PROJECT STATUS: Honest status dashboard showing what works, what doesn't, and what's aspirational. Use traffic-light indicators. Data:
[paste vitals.json → automation_status]

Important: This infographic will itself be used as a demonstration of Claude's capabilities. It should be impressive enough that someone at Anthropic would want to share it. Don't hold back on the design.
```

---

## Prompt 2: NotebookLM Experiment

**Target:** Google NotebookLM
**Input files to upload:**
1. `assets/visualizations/data/pipeline.json`
2. `assets/visualizations/data/categories.json`
3. `assets/visualizations/data/community.json`
4. `README.md`
5. `COMMUNITY_MAP.md`

### Prompt:

```
These files describe a project that tracks Claude Code community tips from Twitter. I'd like you to:

1. Identify the 3 most interesting stories in this data that I might not have noticed
2. Suggest how a non-technical audience would find this data most compelling
3. What questions would a skeptical journalist ask about this dataset?
4. If you were presenting this data visually, what would your top 3 chart choices be and why?
```

---

## Prompt 3: Claude Code Session → Live Preview Infographic

**Target:** A Claude Code terminal session with `--remote-control` and preview tools
**This is the most powerful approach** because Claude can iterate on the HTML with live preview feedback

### Prompt:

```
Read the data files in assets/visualizations/data/ (pipeline.json, categories.json, community.json, vitals.json).

Create a single self-contained HTML file at assets/visualizations/infographic.html that presents this data as an interactive, scroll-driven infographic.

Design constraints:
- No external dependencies (no CDN links, everything inline)
- Dark theme, warm palette (think Anthropic brand: terracotta, cream, slate)
- Scroll-driven narrative, not a dashboard
- Use inline SVG for all data visualization (no canvas, no libraries)
- Intersection Observer for scroll animations
- Mobile-responsive

After creating it, use the preview tools to check the rendering and iterate until it looks polished.

This infographic will be published as a demonstration of Claude Code's capabilities. Quality matters more than speed.
```

---

## Prompt 4: Image Generation API → Static Infographic

**Target:** NanoBanana 2 Pro, Midjourney, or similar
**Note:** These models don't read JSON data, so the prompt needs to encode the data narratively

### Prompt:

```
Create a clean, modern data infographic poster titled "Claude Code Tips: 87 Days of Community Intelligence"

Layout: Vertical poster format, dark background (#1a1a2e), warm accent colors (terracotta #e07a5f, cream #f2cc8f, sage #81b29a)

Include these data points in an editorial infographic style:
- "206 curated tips from 128 community voices"
- "8 Anthropic team members tracked"
- "~16.6 new bookmarks per week"
- Category breakdown: Tooling (147), Prompting (91), Meta (74), Context Mgmt (58), Skills (35), Subagents (34), Automation (33), and 6 smaller categories
- "4-6 week velocity: community hack → native feature"
- Four principle badges: Watch then Adopt / Freshness First / Review Conferences / Don't Reinvent

Style: Clean data journalism aesthetic. Not corporate. Not playful. Serious but warm. Think: if The Pudding made a poster about an open-source project.
```

---

## Notes

- **Prompt 1 and 3 are the highest priority.** An interactive HTML infographic generated by Claude, about Claude, is the strongest possible demo.
- **Prompt 2 is experimental.** NotebookLM might surface patterns we missed.
- **Prompt 4 is a fallback.** Static image infographics are less impressive but easier to embed in a README.
- The data JSON files are designed to be pasted directly into prompts. They're small enough (2-8KB each) to fit in any context window.
